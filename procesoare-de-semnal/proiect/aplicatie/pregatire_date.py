"""Pregătește setul de date pe care îl redă simulatorul: date/masuratori.csv (timp, statie, parametru, valoare).

  python3 pregatire_date.py --sursa reale --zile 30   date reale pentru București (necesită internet):
        PM2.5/PM10, temperatură și umiditate de la cel mai apropiat senzor Sensor.Community (SDS011 + BME280)
        de fiecare stație, NO2 și CO din modelul CAMS (Open-Meteo) pentru coordonatele stației
  python3 pregatire_date.py --sursa demo --zile 8     date sintetice, fără internet, pentru teste și demonstrații
"""
import argparse
import csv
import io
import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

DIR = Path(__file__).resolve().parent
PAS = 600  # un eșantion la 10 minute
ORA_LOCALA = ZoneInfo("Europe/Bucharest")


def scrie(randuri, fisier):
    fisier.parent.mkdir(parents=True, exist_ok=True)
    with open(fisier, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timp", "statie", "parametru", "valoare"])
        for t, statie, parametru, valoare in sorted(randuri):
            w.writerow([datetime.fromtimestamp(t, timezone.utc).isoformat(), statie, parametru, valoare])
    print(f"{len(randuri)} măsurători scrise în {fisier}")


# ---------------- date sintetice ----------------

def gauss(h, centru, latime):
    return math.exp(-((h - centru) / latime) ** 2)


def date_demo(statii, zile, sfarsit, seed=7):
    rnd = random.Random(seed)
    start = sfarsit - zile * 86400
    # cât de stagnant e aerul în fiecare zi (vânt slab, inversiune termică); ultima zi se încarcă seara
    stagnare = [rnd.uniform(0.75, 1.5) for _ in range(zile + 2)]
    stagnare[-2], stagnare[-3] = 1.55, 1.15
    randuri = []
    zgomot = {}
    for t in range(start, sfarsit + 1, PAS):
        local = datetime.fromtimestamp(t, ORA_LOCALA)
        h = local.hour + local.minute / 60
        zi = (t - start) / 86400
        k = int(zi)
        s = stagnare[k] + (stagnare[k + 1] - stagnare[k]) * (zi - k)
        trafic = 0.45 + 0.6 * gauss(h, 8, 1.6) + 0.75 * gauss(h, 18.5, 2.0)
        incalzire = 0.65 + 0.55 * gauss(h, 21, 3) + 0.3 * gauss(h, 7, 2) + 0.35 * gauss(h, 1, 3)
        amestec = 1 - 0.3 * gauss(h, 14, 3)
        temp = 3.5 + 4 * math.sin(2 * math.pi * (h - 9) / 24) + 1.5 * math.sin(zi)
        umid = min(97, 82 - 12 * math.sin(2 * math.pi * (h - 9) / 24) + 4 * math.sin(1.3 * zi))
        fond = 13 * s * incalzire * amestec
        for st in statii:
            x = 1 + (sum(map(ord, st["id"])) % 21 - 10) / 100  # mică diferență între stații de același tip
            if st["tip"] == "trafic":
                intens = 1.25 if st["id"] in ("unirii", "victoriei", "basarab") else 1.0
                pm25 = fond * x + 9 * trafic * s * intens
                pm10 = pm25 * 1.35 + 11 * trafic * intens
                no2 = 20 + 60 * trafic * s ** 0.7 * intens
                co = 0.35 + 0.85 * trafic * intens
            elif st["tip"] == "parc":
                pm25 = fond * 0.8 * x
                pm10 = pm25 * 1.25 + 3
                no2 = 10 + 14 * trafic
                co = 0.25 + 0.15 * trafic
            elif st["tip"] == "scoala":
                pm25 = fond * x + 4 * trafic * s
                pm10 = pm25 * 1.3 + 6 * trafic
                no2 = 16 + 42 * trafic * s ** 0.7
                co = 0.3 + 0.45 * trafic
            else:  # industrial
                intens = 1.3 if st["id"] == "pallady" else 1.0
                pm25 = fond * 1.1 * x + 6 * intens
                pm10 = pm25 * 1.55 + 14 * intens
                no2 = 24 + 32 * trafic
                co = 0.4 + 0.45 * trafic
            reale = {"pm25": pm25, "pm10": pm10, "no2": no2, "co": co,
                     "temp": temp + rnd.gauss(0, 0.3), "umid": umid + rnd.gauss(0, 1.5)}
            for p, v in reale.items():
                cheie = (st["id"], p)
                zgomot[cheie] = 0.85 * zgomot.get(cheie, 0) + rnd.gauss(0, 0.05)
                if p in ("temp", "umid"):
                    valoare = v
                else:
                    valoare = v * (1 + zgomot[cheie])
                    if p in ("pm25", "pm10"):
                        # senzorul optic numără și apa din particule: supraestimează la umiditate mare
                        valoare *= 1 + (0.4 / 1.65) / (100 / min(reale["umid"], 95) - 1)
                    valoare *= 1 + rnd.gauss(0, 0.04)
                    if rnd.random() < 0.006:
                        valoare *= rnd.uniform(2.5, 4)  # vârf fals (praf ridicat, eroare de citire)
                if rnd.random() < 0.004:
                    valoare = -200  # lipsă, marcată ca în setul UCI
                randuri.append((t, st["id"], p, round(valoare, 3 if p == "co" else 1)))
    return randuri


# ---------------- date reale ----------------

def distanta_km(a, b):
    return 6371 * math.hypot(math.radians(a[0] - b[0]), math.radians(a[1] - b[1]) * math.cos(math.radians(a[0])))


def date_reale(statii, zile, sfarsit):
    import requests
    sesiune = requests.Session()
    sesiune.headers["User-Agent"] = "vazduh/1.0 (proiect studentesc UPB)"

    live = sesiune.get("https://data.sensor.community/airrohr/v1/filter/area=44.4268,26.1025,20", timeout=30).json()
    senzori = {}
    for m in live:
        tip = m["sensor"]["sensor_type"]["name"].lower()
        if tip in ("sds011", "bme280"):
            senzori[(tip, m["sensor"]["id"])] = (float(m["location"]["latitude"]), float(m["location"]["longitude"]))
    print(f"{len(senzori)} senzori Sensor.Community găsiți în București")

    def cel_mai_apropiat(st, tip):
        candidati = [(distanta_km((st["lat"], st["lon"]), poz), id_) for (t, id_), poz in senzori.items() if t == tip]
        return min(candidati) if candidati else (None, None)

    randuri = []
    zile_arhiva = [(datetime.fromtimestamp(sfarsit, timezone.utc).date() - timedelta(days=i)).isoformat()
                   for i in range(zile, 0, -1)]
    for st in statii:
        for tip, coloane in (("sds011", {"P2": "pm25", "P1": "pm10"}),
                             ("bme280", {"temperature": "temp", "humidity": "umid"})):
            dist, id_ = cel_mai_apropiat(st, tip)
            if id_ is None or dist > 3:
                print(f"  {st['nume']}: niciun senzor {tip} la mai puțin de 3 km")
                continue
            print(f"  {st['nume']}: {tip} #{id_} la {dist:.1f} km")
            for zi in zile_arhiva:
                url = f"https://archive.sensor.community/{zi}/{zi}_{tip}_sensor_{id_}.csv"
                r = sesiune.get(url, timeout=30)
                if r.status_code != 200:
                    continue
                medii = {}
                for rand in csv.DictReader(io.StringIO(r.text), delimiter=";"):
                    t = int(datetime.fromisoformat(rand["timestamp"]).replace(tzinfo=timezone.utc).timestamp())
                    for col, p in coloane.items():
                        try:
                            medii.setdefault((t - t % PAS, p), []).append(float(rand[col]))
                        except (KeyError, ValueError):
                            pass
                randuri += [(t, st["id"], p, round(sum(v) / len(v), 1)) for (t, p), v in medii.items()]

        r = sesiune.get("https://air-quality-api.open-meteo.com/v1/air-quality", timeout=30, params={
            "latitude": st["lat"], "longitude": st["lon"], "timezone": "GMT", "past_days": min(zile, 92),
            "forecast_days": 1, "hourly": "nitrogen_dioxide,carbon_monoxide"}).json()["hourly"]
        for i, ora in enumerate(r["time"]):
            t0 = int(datetime.fromisoformat(ora).replace(tzinfo=timezone.utc).timestamp())
            if t0 > sfarsit:
                break
            for p, col, scala in (("no2", "nitrogen_dioxide", 1), ("co", "carbon_monoxide", 0.001)):
                if r[col][i] is not None:
                    randuri += [(t0 + k * PAS, st["id"], p, round(r[col][i] * scala, 3)) for k in range(6)]
    return randuri


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sursa", choices=("reale", "demo"), default="reale")
    ap.add_argument("--zile", type=int, default=30)
    ap.add_argument("--sfarsit", help="ultimul moment, ISO (implicit: acum)")
    ap.add_argument("--iesire", default=str(DIR / "date" / "masuratori.csv"))
    a = ap.parse_args()
    statii = json.loads((DIR / "statii.json").read_text(encoding="utf-8"))
    sfarsit = int(datetime.fromisoformat(a.sfarsit).timestamp()) if a.sfarsit else int(datetime.now().timestamp())
    sfarsit -= sfarsit % PAS
    randuri = date_reale(statii, a.zile, sfarsit) if a.sursa == "reale" else date_demo(statii, a.zile, sfarsit)
    scrie(randuri, Path(a.iesire))
