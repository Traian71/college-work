"""Simulatorul de senzori: citește date/masuratori.csv și trimite măsurătorile ca JSON către server,
ca și cum ar veni în timp real de la stații.

  python3 simulator.py                         # trimite istoricul, apoi câte un set la 10 secunde
  python3 simulator.py --interval 2 --cheie X  # mai repede, cu cheia de acces a serverului

Timpii sunt mutați astfel încât ultimele --ore-live ore din fișier să cadă începând de acum.
"""
import argparse
import csv
import json
import time
import urllib.request
from datetime import datetime, timezone
from itertools import groupby
from pathlib import Path

DIR = Path(__file__).resolve().parent


def trimite(url, cheie, lot):
    corp = json.dumps(lot).encode()
    cerere = urllib.request.Request(url + "/api/ingest", data=corp, method="POST",
                                    headers={"Content-Type": "application/json", "X-Cheie": cheie})
    with urllib.request.urlopen(cerere, timeout=30) as r:
        return json.loads(r.read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:5000")
    ap.add_argument("--fisier", default=str(DIR / "date" / "masuratori.csv"))
    ap.add_argument("--cheie", default="")
    ap.add_argument("--interval", type=float, default=10, help="secunde între două seturi de măsurători")
    ap.add_argument("--ore-live", type=float, default=6, help="câte ore de la final se redau în timp real")
    a = ap.parse_args()

    with open(a.fisier, encoding="utf-8") as f:
        randuri = [(int(datetime.fromisoformat(r["timp"]).timestamp()), r) for r in csv.DictReader(f)]
    randuri.sort(key=lambda x: x[0])
    ultim = randuri[-1][0]
    inceput_live = ultim - int(a.ore_live * 3600)
    decalaj = int(time.time()) - inceput_live
    decalaj -= decalaj % 600

    def mesaj(t, r):
        return {"statie": r["statie"], "timp": datetime.fromtimestamp(t + decalaj, timezone.utc).isoformat(),
                "parametru": r["parametru"], "valoare": float(r["valoare"])}

    istoric = [mesaj(t, r) for t, r in randuri if t < inceput_live]
    for i in range(0, len(istoric), 2000):
        rezultat = trimite(a.url, a.cheie, istoric[i:i + 2000])
        print(f"istoric {min(i + 2000, len(istoric))}/{len(istoric)}  acceptate {rezultat['acceptate']}", end="\r")
    print()

    for t, grup in groupby([x for x in randuri if x[0] >= inceput_live], key=lambda x: x[0]):
        lot = [mesaj(t, r) for _, r in grup]
        rezultat = trimite(a.url, a.cheie, lot)
        ora = datetime.fromtimestamp(t + decalaj).strftime("%H:%M")
        print(f"{ora}  {len(lot)} măsurători  acceptate {rezultat['acceptate']}  respinse {rezultat['respinse']}")
        time.sleep(a.interval)
