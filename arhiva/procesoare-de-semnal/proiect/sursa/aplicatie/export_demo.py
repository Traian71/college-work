"""Rulează serverul pe datele demonstrative și salvează răspunsurile API în demo.json (pentru previzualizare).

Utilizare: python3 export_demo.py <folder-aplicatie> <masuratori.csv> <demo.json>
"""
import csv
import json
import os
import sys
import tempfile
import time

aplicatie, fisier_csv, iesire = sys.argv[1:4]
os.environ["VAZDUH_DB"] = os.path.join(tempfile.mkdtemp(), "demo.db")
os.environ["VAZDUH_CAMS"] = "0"
os.environ.pop("ANTHROPIC_API_KEY", None)
sys.path.insert(0, aplicatie)
import server  # noqa: E402

client = server.app.test_client()
with open(fisier_csv, encoding="utf-8") as f:
    randuri = list(csv.DictReader(f))
t0 = time.time()
for i in range(0, len(randuri), 5000):
    lot = [{"statie": r["statie"], "timp": r["timp"], "parametru": r["parametru"], "valoare": float(r["valoare"])}
           for r in randuri[i:i + 5000]]
    rezultat = client.post("/api/ingest", json=lot).get_json()
print(f"ingest {len(randuri)} rânduri în {time.time() - t0:.1f}s, ultimul lot: {rezultat}")

stare = client.get("/api/stare").get_json()
statii = {s["id"]: client.get(f"/api/statie/{s['id']}").get_json() for s in stare["statii"]}
demo = {"demo": True, "stare": stare, "statii": statii}
json.dump(demo, open(iesire, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("demo.json:", os.path.getsize(iesire) // 1024, "KB")
for s in stare["statii"]:
    print(f"{s['nume']:26} nivel={s['nivel']} dom={s['dominant']} pm25={s['ultim'].get('pm25')} pm10={s['ultim'].get('pm10')} no2={s['ultim'].get('no2')} umid={s['ultim'].get('umid')}")
print("alerte:", [(a['nume'], a['text'], a['valoare']) for a in stare["alerte"]])
print("oras:", stare["oras"])
d = statii["unirii"]
print("prognoza model:", d["prognoza"]["model"], "fereastra:", d["prognoza"]["fereastra"])
print("ai:", d["ai"])
print("calitate:", d["calitate"])
print("puncte serie:", len(d["serii"]["timp"]))
