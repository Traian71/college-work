"""Face pagina de previzualizare (un singur HTML, Leaflet de pe cdnjs) din static/ + demo.json.

Utilizare: python3 construieste_previzualizare.py <folder-aplicatie> <demo.json> <folder-iesire>
"""
import shutil
import sys
from pathlib import Path

aplicatie, demo, iesire = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
static = aplicatie / "static"
html = (static / "index.html").read_text(encoding="utf-8")
corp = html.split("<!--continut-->")[1].split("<!--/continut-->")[0]
css = (static / "vendor" / "leaflet.css").read_text(encoding="utf-8") + (static / "app.css").read_text(encoding="utf-8")
js = (static / "app.js").read_text(encoding="utf-8")
pagina = f"""<title>Văzduh</title>
<style>
{css}
</style>
{corp}
<script>window.VAZDUH_DEMO = true;</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
{js}
</script>
"""
iesire.mkdir(parents=True, exist_ok=True)
(iesire / "index.html").write_text(pagina, encoding="utf-8")
shutil.copy(demo, iesire / "demo.json")
shutil.copy(static / "harta.json", iesire / "harta.json")
print("previzualizare:", iesire)
