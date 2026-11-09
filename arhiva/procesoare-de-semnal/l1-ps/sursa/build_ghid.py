# Pune rezumatele si grilele din date/*.json in ghid_template.html -> procesoare-de-semnal/l1-ps/ghid-l1-ps.html
# Rulare: python3 build_ghid.py (din orice folder)
import json, re, unicodedata
from pathlib import Path

D = Path(__file__).resolve().parent
OUT = D.parents[3] / "procesoare-de-semnal/l1-ps/ghid-l1-ps.html"


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


cursuri, grile, vazute = [], [], {}


def adauga(q, curs, tip):
    if not q.get("variante") or not q.get("corecte"):
        return
    cheie = norm(q["intrebare"]) + "|" + "|".join(sorted(norm(v) for v in q["variante"]))
    if cheie in vazute:
        alt = vazute[cheie]
        if q.get("sursa") and q["sursa"] not in alt["sursa"]:
            alt["sursa"] += "; " + q["sursa"]
        return
    g = {"id": f"c{curs}-{tip[0]}{len(grile)}", "curs": curs, "tip": tip, "sursa": q.get("sursa", ""),
         "intrebare": q["intrebare"].strip(), "variante": [v.strip() for v in q["variante"]],
         "corecte": sorted(set(q["corecte"])), "explicatie": q.get("explicatie", "").strip(),
         "sigur": q.get("sigur", True), "figura": q.get("figura", "")}
    vazute[cheie] = g
    grile.append(g)


for n in range(1, 7):
    f = D / "date" / f"curs{n}.json"
    if not f.exists():
        continue
    c = json.loads(f.read_text(encoding="utf-8"))
    cursuri.append({"curs": n, "titlu": c.get("titlu", ""), "rezumat": c.get("rezumat", []),
                    "capcane": c.get("capcane", [])})
    for q in c.get("grile_vechi", []):
        adauga(q, n, "vechi")

sc = D / "date" / "grile_scanate.json"
if sc.exists():
    for q in json.loads(sc.read_text(encoding="utf-8")).get("grile", []):
        if 1 <= q.get("curs", 0) <= 6:
            adauga(q, q["curs"], "vechi")

# din grilele noi pastram doar cateva pe curs, pe subiectele care apar si in grilele vechi (cerut pe 9 nov)
NOI_ALESE = {1: [3, 4, 5, 11, 16, 24], 2: [0, 1, 3, 8, 12, 24], 3: [2, 3, 6, 9, 20, 21],
             4: [6, 7, 12, 16, 17, 19], 5: [1, 3, 8, 12, 16, 25], 6: [2, 8, 9, 11, 17, 25]}
for n in range(1, 7):
    f = D / "date" / f"curs{n}.json"
    if f.exists():
        noi = json.loads(f.read_text(encoding="utf-8")).get("grile_noi", [])
        for i in NOI_ALESE[n]:
            adauga(noi[i], n, "nou")

esential = {e["curs"]: e for e in json.loads((D / "date" / "esential.json").read_text(encoding="utf-8"))}
for c in cursuri:
    c["esential"] = esential.get(c["curs"], {}).get("puncte", [])

formule = D.parents[3] / "procesoare-de-semnal/l1-ps/formule-calcul-l1-ps.md"
data = {"cursuri": cursuri, "grile": grile,
        "formule": formule.read_text(encoding="utf-8") if formule.exists() else ""}
html = (D / "ghid_template.html").read_text(encoding="utf-8")
html = html.replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(OUT, f"{len(cursuri)} cursuri, {len(grile)} grile "
      f"({sum(g['tip'] == 'vechi' for g in grile)} vechi, {sum(not g['sigur'] for g in grile)} nesigure)")
