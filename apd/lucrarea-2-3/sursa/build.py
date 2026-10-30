import json, re, sys
from pathlib import Path

D = Path(sys.argv[1])            # folderul sursa
rez_path = Path(sys.argv[2])     # rezultate_APD.txt
obs_path = Path(sys.argv[3])     # observatii (json)
out_html = Path(sys.argv[4])

txt = rez_path.read_text(encoding="utf-8-sig", errors="replace")
obs = json.loads(obs_path.read_text(encoding="utf-8"))

def num(s):
    return float(s.replace(",", "."))

P = int(re.search(r"Procesoare logice:\s*(\d+)", txt).group(1))
windows = "Windows" in re.search(r"Sistem:\s*(.*)", txt).group(1)
sec = re.split(r"\n(?=EX)", txt)
ex4 = next(s for s in sec if s.startswith("EX4 -"))
din = next(s for s in sec if s.startswith("EX4 DINAMIC"))
ex5 = next(s for s in sec if s.startswith("EX5"))

ts = int(re.search(r"serial:\s*(\d+)", ex4).group(1))
par = [(int(n), int(t)) for n, t in re.findall(r"N=(\d+):\s*(\d+) ms", ex4)]
tsm = int(re.search(r"serial:\s*(\d+)", din).group(1))
dyn = [(int(n), int(a), int(b)) for n, a, b in re.findall(r"N=(\d+): static (\d+) ms, dinamic (\d+) ms", din)]
e5 = [(name, int(a), int(b), int(c)) for name, a, b, c in re.findall(r"(\w+): serial (\d+) ms, static (\d+) ms, dinamic (\d+) ms", ex5)]

def f2(x):
    return f"{x:.2f}".replace(".", ",")

def ex4_table():
    rows = [f"<tr><td>{n}</td><td>{t}</td><td>{f2(ts / t)}</td></tr>" for n, t in par]
    head = "<tr><th>N</th><th>T<sub>paralel</sub> (ms)</th><th>S</th></tr>"
    half = (len(rows) + 1) // 2
    return ('<div class="tabele">'
            f'<table>{head}{"".join(rows[:half])}</table>'
            f'<table>{head}{"".join(rows[half:])}</table></div>')

def din_table():
    rows = "".join(f"<tr><td>{n}</td><td>{a}</td><td>{b}</td><td>{f2(tsm / a)}</td><td>{f2(tsm / b)}</td></tr>" for n, a, b in dyn)
    return ("<table><tr><th>N</th><th>Static (ms)</th><th>Dinamic (ms)</th><th>S static</th><th>S dinamic</th></tr>"
            f"{rows}</table>")

def ex5_table():
    nume = {"mici": "Mici (40 × 100x100)", "medii": "Medii (40 × 500x500)", "mari": "Mari (8 × 2000x2000)"}
    rows = "".join(f"<tr><td>{nume.get(n, n)}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{f2(a / b)}</td><td>{f2(a / c)}</td></tr>"
                   for n, a, b, c in e5)
    return ("<table><tr><th>Imagini</th><th>Serial (ms)</th><th>Static N=4 (ms)</th><th>Dinamic N=4 (ms)</th>"
            f"<th>S static</th><th>S dinamic</th></tr>{rows}</table>")

def svg(p):
    return Path(p).read_text(encoding="utf-8").split("?>", 1)[-1] if "<?xml" in Path(p).read_text(encoding="utf-8")[:100] else Path(p).read_text(encoding="utf-8")

body2 = (D / "lab2_body.html").read_text(encoding="utf-8")
fill = {
    "G1": svg(D / "graf/g1.svg"),
    "G2": svg(D / "graf/g2.svg"),
    "EX4_INTRO": (f"Rezultate pentru 40 de imagini de 500x500 px, pe un calculator cu {P} procesoare logice. "
                  if windows else
                  f"Măsurătorile le-am făcut pe macOS ({P} procesoare logice). Pentru că System.Drawing nu este disponibil "
                  "pe macOS, am folosit o variantă a aceluiași program în care imaginile sunt citite și salvate cu biblioteca "
                  "SkiaSharp; algoritmul și împărțirea pe threaduri sunt aceleași. Rezultate pentru 40 de imagini de 500x500 px: ")
                 + f"T<sub>serial</sub> = {ts} ms, iar S = T<sub>serial</sub> / T<sub>paralel</sub>:",
    "EX4_TABEL": ex4_table(),
    "EX4_OBS": obs["ex4"],
    "DIN_INTRO": "Comparație cu varianta statică de la exercițiul 3, pe 16 imagini de dimensiuni diferite "
                 f"(de la 2000x2000 la 100x100 px, cele mari la începutul listei). T<sub>serial</sub> = {tsm} ms:",
    "DIN_TABEL": din_table(),
    "DIN_OBS": obs["din"],
    "EX5_INTRO": "Am testat variantele de la exercițiul 3 (statică) și exercițiul 4 (dinamică), cu N = 4, pe imagini mici "
                 "(40 × 100x100 px), medii (40 × 500x500 px) și mari (8 × 2000x2000 px):",
    "EX5_TABEL": ex5_table(),
    "EX5_OBS": obs["ex5"],
}
for k, v in fill.items():
    body2 = body2.replace("{{" + k + "}}", v)
assert "{{" not in body2, re.findall(r"\{\{\w+\}\}", body2)

lab3 = (D / "lab3.html").read_text(encoding="utf-8")
style = re.search(r"<style>(.*?)</style>", lab3, re.S).group(1)
body3 = re.search(r"<body>(.*?)</body>", lab3, re.S).group(1)

extra_css = """
  .graf { text-align: center; margin: 6px 0; }
  .graf svg { height: auto; }
  .g1 svg { width: 95mm; height: auto; }
  .g2 svg { width: 72mm; height: auto; }
  table { border-collapse: collapse; margin: 6px 0 8px; font-size: 9.5pt; break-inside: avoid; }
  th, td { border: 1px solid #000; padding: 2px 8px; text-align: center; }
  th { background: #eee; font-weight: normal; }
  .tabele { display: flex; gap: 24px; align-items: flex-start; }
  .nou { break-before: page; }
"""
html = (f'<!doctype html><html lang="ro"><head><meta charset="utf-8"><style>{style}{extra_css}</style></head><body>'
        f'{body2}<div class="nou">{body3}</div></body></html>')
out_html.write_text(html, encoding="utf-8")
print("ok", P, ts, len(par), len(dyn), len(e5))
