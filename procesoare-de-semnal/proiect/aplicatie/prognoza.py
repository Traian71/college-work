"""Prognoza pe 24 de ore și textele scrise de Claude.

Modelul numeric: profilul zilnic al stației (mediana pe fiecare oră din ultimele 7 zile) corectat cu
nivelul din ultimele ore (persistență care se stinge în timp). Dacă serverul are internet, se combină
cu prognoza CAMS (Open-Meteo), corectată local. Claude primește cifrele deja calculate și scrie doar
explicația și recomandarea, pe înțelesul oricui.
"""
import json
import math
import os
import time
from datetime import datetime, timezone
from statistics import mean, median
from zoneinfo import ZoneInfo

import prelucrare as pr

ORA_LOCALA = ZoneInfo("Europe/Bucharest")
MODEL = os.environ.get("VAZDUH_MODEL", "claude-opus-5-5")
FOLOSESTE_CAMS = os.environ.get("VAZDUH_CAMS", "1") == "1"
_cache_cams, _cache_comunitate = {}, {"timp": 0, "date": []}


def ora_locala(t):
    return datetime.fromtimestamp(t, ORA_LOCALA)


def hh(t):
    return ora_locala(t).strftime("%H:%M")


def profil_zilnic(orare):
    pe_ora = {}
    for t, v in orare.items():
        pe_ora.setdefault(ora_locala(t).hour, []).append(v)
    profil = {h: median(v) for h, v in pe_ora.items()}
    abatere = {h: median(abs(x - profil[h]) for x in v) for h, v in pe_ora.items()}
    return profil, abatere


def cams(statie):
    """Prognoza CAMS de la Open-Meteo pentru coordonatele stației (fără cheie API). None dacă nu e internet."""
    if not FOLOSESTE_CAMS:
        return None
    cheie = statie["id"]
    if cheie in _cache_cams and time.time() - _cache_cams[cheie][0] < 3600:
        return _cache_cams[cheie][1]
    try:
        import requests
        r = requests.get("https://air-quality-api.open-meteo.com/v1/air-quality", timeout=4, params={
            "latitude": statie["lat"], "longitude": statie["lon"], "timezone": "GMT",
            "hourly": "pm2_5,pm10,nitrogen_dioxide", "past_days": 3, "forecast_days": 2})
        r.raise_for_status()
        h = r.json()["hourly"]
        ore = [int(datetime.fromisoformat(t).replace(tzinfo=timezone.utc).timestamp()) for t in h["time"]]
        date = {p: {o: v for o, v in zip(ore, h[c]) if v is not None}
                for p, c in (("pm25", "pm2_5"), ("pm10", "pm10"), ("no2", "nitrogen_dioxide"))}
    except Exception:
        date = None
    _cache_cams[cheie] = (time.time(), date)
    return date


def prognoza(statie, istoric, acum):
    """istoric: {parametru: {ora_unix: medie_orara}} pe ultimele 7 zile."""
    ora0 = acum - acum % 3600
    ore = [ora0 + k * 3600 for k in range(1, 25)]
    externe = cams(statie)
    rezultat = {"ore": ore, "model": "profil zilnic + persistență" + (" + CAMS" if externe else "")}
    for p, orare in istoric.items():
        if len(orare) < 24:
            continue
        profil, abatere = profil_zilnic(orare)
        recente = [t for t in sorted(orare) if t > acum - 3 * 3600]
        asteptat = mean(profil.get(ora_locala(t).hour, 0) for t in recente) if recente else 0
        r = mean(orare[t] for t in recente) / asteptat if recente and asteptat > 0 else 1
        r = min(max(r, 0.4), 2.5)
        valori, jos, sus = [], [], []
        for k, t in enumerate(ore, start=1):
            h = ora_locala(t).hour
            f = profil.get(h, mean(profil.values())) * (1 + (r - 1) * math.exp(-k / 6))
            if externe and externe.get(p):
                comune = [o for o in orare if o in externe[p] and externe[p][o] > 0]
                if len(comune) >= 12 and t in externe[p]:
                    factor = min(max(median(orare[o] / externe[p][o] for o in comune), 0.3), 3)
                    f = 0.5 * f + 0.5 * externe[p][t] * factor
            d = abatere.get(h, 0) * (1 + k / 24) + 1
            valori.append(round(f, 1))
            jos.append(round(max(0, f - d), 1))
            sus.append(round(f + d, 1))
        rezultat[p] = {"valoare": valori, "jos": jos, "sus": sus}
    rezultat["fereastra"] = fereastra_buna(rezultat)
    return rezultat


def fereastra_buna(prog):
    """Cele mai curate 2 ore consecutive între 07:00 și 22:00, în următoarele 24 de ore.
    Fiecare oră primește scorul poluantului cel mai apropiat de limita clasei „Moderat”."""
    poluanti = [p for p in ("pm25", "pm10", "no2") if p in prog]
    if not poluanti:
        return None
    ore = prog["ore"]
    scor = [max(prog[p]["valoare"][i] / pr.PRAGURI_INDICE[p][2] for p in poluanti) for i in range(len(ore))]
    candidati = [(mean(scor[i:i + 2]), ore[i]) for i in range(len(ore) - 1) if 7 <= ora_locala(ore[i]).hour <= 20]
    if not candidati:
        return None
    _, start = min(candidati)
    return {"start": start, "sfarsit": start + 7200}


# ---------- texte: Claude dacă există cheie, altfel reguli simple ----------

SISTEM = (
    "Ești componenta de prognoză a aplicației Văzduh, care arată calitatea aerului în București. "
    "Primești în JSON valorile măsurate și o prognoză numerică deja calculată de server. "
    "Scrie pentru locuitori, în română cu diacritice, simplu și fără jargon. "
    "rezumat: cel mult două propoziții despre cum e aerul acum și cum evoluează în următoarele 24 de ore, "
    "cu cifre rotunjite și orele importante. "
    "recomandare: o propoziție practică, de exemplu când e bine de ieșit, de alergat sau de aerisit casa, "
    "și ce ar trebui să evite persoanele sensibile dacă e cazul. "
    "Folosește doar cifrele primite. Poți pomeni cauze obișnuite (traficul de la orele de vârf, încălzirea "
    "locuințelor, aerul stagnant noaptea) doar ca posibile, nu ca sigure. Fără emoji."
)

SCHEMA = {
    "type": "object",
    "properties": {"rezumat": {"type": "string"}, "recomandare": {"type": "string"}},
    "required": ["rezumat", "recomandare"],
    "additionalProperties": False,
}


def are_cheie():
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def intreaba_claude(date):
    import anthropic
    client = anthropic.Anthropic()
    try:
        raspuns = client.beta.messages.create(
            model=MODEL,
            max_tokens=4000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
            system=SISTEM,
            messages=[{"role": "user", "content": json.dumps(date, ensure_ascii=False)}],
        )
    except (anthropic.APIConnectionError, anthropic.RateLimitError, anthropic.APIStatusError):
        return None
    if raspuns.stop_reason != "end_turn":
        return None
    text = next((b.text for b in raspuns.content if b.type == "text"), None)
    return json.loads(text) if text else None


def din_cache(con, cheie, calculeaza, durata=3600):
    rand = con.execute("SELECT creat, continut FROM cache_ai WHERE cheie=?", (cheie,)).fetchone()
    if rand and time.time() - rand[0] < durata:
        return json.loads(rand[1])
    rezultat = calculeaza()
    if rezultat.get("sursa") == "claude":
        with con:
            con.execute("INSERT OR REPLACE INTO cache_ai VALUES (?,?,?)",
                        (cheie, int(time.time()), json.dumps(rezultat, ensure_ascii=False)))
    return rezultat


def text_statie(con, statie, istoric, prog, acum):
    def reguli():
        return dict(reguli_statie(statie, prog, acum), sursa="reguli")

    def calculeaza():
        if not are_cheie():
            return reguli()
        date = {
            "statie": {"nume": statie["nume"], "tip": statie["tip"], "sector": statie.get("sector")},
            "ora_curenta": hh(acum),
            "acum": statie["ultim"],
            "indice_acum": pr.NIVELURI[statie["nivel"]] if statie["nivel"] is not None else None,
            "ultimele_24h_pm25": [round(v) for t, v in sorted(istoric.get("pm25", {}).items()) if t > acum - 86400],
            "prognoza": {p: {"ore": [hh(t) for t in prog["ore"]], "valori": prog[p]["valoare"]}
                         for p in ("pm25", "pm10", "no2") if p in prog},
            "cel_mai_curat_interval": ({"de_la": hh(prog["fereastra"]["start"]), "pana_la": hh(prog["fereastra"]["sfarsit"])}
                                       if prog.get("fereastra") else None),
            "praguri_indice_european_pm25": pr.PRAGURI_INDICE["pm25"],
        }
        text = intreaba_claude(date)
        return dict(text, sursa="claude", model=MODEL) if text else reguli()

    return din_cache(con, f"statie:{statie['id']}:{acum // 3600}", calculeaza)


NUME = {"pm25": "PM2.5", "pm10": "PM10", "no2": "NO₂"}


def reguli_statie(statie, prog, acum):
    dom = statie.get("dominant") or "pm25"
    v = statie["ultim"].get(dom)
    if v is None or dom not in prog or statie["nivel"] is None:
        return {"rezumat": "Încă nu sunt destule date pentru o prognoză.", "recomandare": ""}
    valori, ore = prog[dom]["valoare"], prog["ore"]
    i_max, i_min = valori.index(max(valori)), valori.index(min(valori))
    rezumat = f"Acum {NUME[dom]} are {v:.0f} µg/m³, nivel {pr.NIVELURI[statie['nivel']].lower()}."
    if dom == "no2":
        rezumat = rezumat[:-1] + ", din cauza traficului."
    if valori[i_max] > v * 1.2:
        rezumat += f" Urcă spre {valori[i_max]:.0f} în jurul orei {hh(ore[i_max])}, apoi scade."
    elif valori[i_min] < v * 0.8:
        rezumat += f" Scade spre {valori[i_min]:.0f} până pe la {hh(ore[i_min])}."
    else:
        rezumat += " Rămâne cam la fel în următoarele ore."
    f = prog.get("fereastra")
    recomandare = f"Cel mai curat interval pentru ieșit sau aerisit: {hh(f['start'])}–{hh(f['sfarsit'])}." if f else ""
    if pr.nivel(dom, valori[i_max]) >= 3:
        recomandare += " Persoanele sensibile ar trebui să evite efortul afară la orele de vârf."
    return {"rezumat": rezumat, "recomandare": recomandare.strip()}


def rezumat_oras(con, statii, alerte, acum):
    cu_date = [s for s in statii if s["nivel"] is not None]
    if not cu_date:
        return None
    nivel = round(median(s["nivel"] for s in cu_date))
    curat = min(cu_date, key=lambda s: (s["nivel"], s["ultim"].get(s["dominant"], 0)))
    poluat = max(cu_date, key=lambda s: (s["nivel"], s["ultim"].get(s["dominant"], 0)))
    baza = {"nivel": nivel, "cel_mai_curat": curat["id"], "cel_mai_poluat": poluat["id"]}

    def reguli():
        text = (f"Cel mai curat aer e acum la {curat['nume']}, iar cel mai încărcat la {poluat['nume']}"
                f" ({NUME[poluat['dominant']]} {poluat['ultim'][poluat['dominant']]:.0f} µg/m³).")
        if alerte:
            text += f" {len(alerte)} {'depășire' if len(alerte) == 1 else 'depășiri'} ale limitelor legale în ultimele 24 de ore."
        return dict(baza, text=text, sursa="reguli")

    def calculeaza():
        if not are_cheie():
            return reguli()
        date = {"ora_curenta": hh(acum), "indice_oras": pr.NIVELURI[nivel],
                "statii": [{"nume": s["nume"], "tip": s["tip"], "pm25": s["ultim"].get("pm25"),
                            "pm10": s["ultim"].get("pm10"), "no2": s["ultim"].get("no2"),
                            "indice": pr.NIVELURI[s["nivel"]]} for s in cu_date],
                "depasiri_legale_24h": [f"{a['nume']}: {a['text']}" for a in alerte]}
        text = intreaba_claude(date)
        if not text:
            return reguli()
        return dict(baza, text=f"{text['rezumat']} {text['recomandare']}".strip(), sursa="claude", model=MODEL)

    return din_cache(con, f"oras:{acum // 3600}", calculeaza)


def senzori_comunitate():
    """Senzorii cetățenilor din rețeaua Sensor.Community, pe o rază de 15 km de centru (cache 5 minute)."""
    if time.time() - _cache_comunitate["timp"] < 300:
        return _cache_comunitate["date"]
    date = []
    try:
        import requests
        r = requests.get("https://data.sensor.community/airrohr/v1/filter/area=44.4268,26.1025,15", timeout=6,
                         headers={"User-Agent": "vazduh/1.0 (proiect studentesc UPB)"})
        r.raise_for_status()
        for m in r.json():
            valori = {v["value_type"]: v["value"] for v in m.get("sensordatavalues", [])}
            if "P1" in valori and "P2" in valori:
                date.append({"id": m["sensor"]["id"], "lat": float(m["location"]["latitude"]),
                             "lon": float(m["location"]["longitude"]), "pm10": float(valori["P1"]),
                             "pm25": float(valori["P2"]), "timp": m.get("timestamp")})
    except Exception:
        date = _cache_comunitate["date"]
    _cache_comunitate.update(timp=time.time(), date=date)
    return date
