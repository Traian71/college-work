# Construieste PDF-ul din README.md (markdown -> HTML cu marked.js -> PDF cu Chrome headless).
# Rulare: python3 build.py   (din orice folder)
import json, subprocess, tempfile
from pathlib import Path

D = Path(__file__).resolve().parent
OUT = D.parents[3] / "retele-de-calculatoare/lucrarea-2-3/Lucrarea_2_3_RC.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

md = (D / "README.md").read_text(encoding="utf-8")

html = """<!doctype html><html lang="ro"><head><meta charset="utf-8">
<base href="%s/">
<style>
  @page { size: A4; margin: 16mm 16mm; }
  body { font-family: "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; line-height: 1.4; color: #111; }
  h1 { font-size: 17pt; margin: 0 0 2px; }
  h1 + p { margin-top: 0; color: #444; }
  h2 { font-size: 14pt; margin: 18px 0 6px; border-bottom: 1px solid #999; }
  h3 { font-size: 11.5pt; margin: 14px 0 4px; }
  table { border-collapse: collapse; margin: 6px 0; font-size: 9.5pt; }
  th, td { border: 1px solid #888; padding: 3px 7px; text-align: left; }
  th { background: #eee; }
  pre { background: #f4f4f4; padding: 6px 10px; font-size: 9pt; line-height: 1.25; }
  code { font-family: Menlo, monospace; font-size: 9pt; }
  img { max-width: 100%%; max-height: 120mm; display: block; margin: 6px 0; border: 1px solid #ccc; }
  .lipsa { border: 1px dashed #999; color: #777; padding: 30px; text-align: center; margin: 6px 0; }
  h3, table, pre, img { break-inside: avoid; }
</style></head><body><div id="c"></div>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script>
  document.getElementById("c").innerHTML = marked.parse(%s);
  const imgs = [...document.images];
  Promise.all(imgs.map(i => i.complete ? Promise.resolve() : new Promise(r => { i.onload = i.onerror = r; })))
    .then(() => imgs.filter(i => !i.naturalWidth).forEach(i => {
      const d = document.createElement("div"); d.className = "lipsa";
      d.textContent = "[captura Packet Tracer: " + i.getAttribute("src") + "]"; i.replaceWith(d);
    }));
</script></body></html>""" % (D.as_uri(), json.dumps(md))

with tempfile.TemporaryDirectory() as t:
    page = Path(t) / "rc.html"
    page.write_text(html, encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={t}/prof",
                    "--virtual-time-budget=8000", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT}", page.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(OUT)
