# Construieste raportul RC (HTML) din codul placilor si capturile din Packet Tracer.
# Rulare: uv run --no-project --with pillow python build_rc.py <out.html>, apoi Chrome --headless --print-to-pdf
import base64, html, io, sys
from pathlib import Path
from PIL import Image

D = Path(__file__).resolve().parent
ROOT = D.parents[3]
RC = ROOT / "apd/proiect-027/RC"
CAP = D / "capturi"


def img(nume, box=None, latime="100%"):
    im = Image.open(CAP / nume)
    if box:
        x0, y0, x1, y1 = box
        im = im.crop((x0, y0 if y0 >= 0 else im.height + y0, x1 if x1 > 0 else im.width, y1 if y1 > 0 else im.height + y1))
    b = io.BytesIO(); im.save(b, "PNG")
    return f'<img style="width:{latime}" src="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}">'


def fig(continut, text):
    return f'<div class="fig">{continut}<p>{text}</p></div>'


cod_a = (RC / "sursa_A.py").read_text(encoding="utf-8")
cod_m = (RC / "membru.py").read_text(encoding="utf-8")

css = """
@page { size: A4; margin: 17mm 17mm; }
body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.4; color: #000; }
h1 { font-size: 16pt; margin: 0 0 4px; } h2 { font-size: 13pt; margin: 16px 0 6px; break-after: avoid; }
p { margin: 5px 0; } ul { margin: 4px 0; padding-left: 20px; } li { margin: 2px 0; }
code { font-family: Menlo, Consolas, monospace; font-size: 9.5pt; }
pre { font-family: Menlo, Consolas, monospace; font-size: 8pt; line-height: 1.3; background: #f4f4f4; border: 1px solid #ccc; padding: 6px 8px; white-space: pre-wrap; }
table { border-collapse: collapse; margin: 6px 0; font-size: 10pt; } td, th { border: 1px solid #888; padding: 3px 8px; } th { background: #e8e8e8; }
td.n { text-align: right; }
.fig { break-inside: avoid; margin: 8px 0 12px; } .fig img { display: block; margin: 0 auto; border: 1px solid #bbb; }
.fig p { font-size: 9.5pt; font-style: italic; margin: 4px 0 0; }
.cap { color: #333; font-size: 10pt; }
"""

doc = f"""<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>Tema 027 RC</title><style>{css}</style></head><body>
<h1>Tema 027 – RC: Înscrierea și retragerea dintr-un grup care primește un semnal</h1>
<p class="cap">File-Mitita Traian · Cisco Packet Tracer 9.0.1, modulul Programming, Python 3</p>

<h2>1. Topologia</h2>
<p>Cinci plăci SBC-PT (A, B, C, D, E) legate la un switch 2960, toate în subrețeaua 192.168.1.0/24.
În Packet Tracer 9 placa SBC vine doar cu Wireless și Bluetooth, așa că pe fiecare am pus modulul <b>PT-IOT-NM-1CFE</b>
(un port FastEthernet) în tabul Physical și am legat portul <code>FastEthernet0</code> la switch.</p>
<table><tr><th>Placă</th><th>Rol</th><th>Adresă IPv4</th><th>Port switch</th></tr>
<tr><td>A</td><td>sursa semnalului, ține lista membrilor</td><td>192.168.1.1/24</td><td>Fa0/1</td></tr>
<tr><td>B</td><td>membru de la început</td><td>192.168.1.2/24</td><td>Fa0/2</td></tr>
<tr><td>C</td><td>membru, se retrage în timpul rulării</td><td>192.168.1.3/24</td><td>Fa0/3</td></tr>
<tr><td>D</td><td>membru de la început</td><td>192.168.1.4/24</td><td>Fa0/4</td></tr>
<tr><td>E</td><td>se înscrie după începerea fluxului</td><td>192.168.1.5/24</td><td>Fa0/5</td></tr></table>
{fig(img("topologie.png", (60, 180, 900, 640), "85%"), "Fig. 1 – Topologia în Packet Tracer: toate legăturile sunt active (verde). Fișierul salvat este Tema027_RC_FileMitita_Traian.pkt.")}

<h2>2. Protocolul la nivel de aplicație</h2>
<p>Toate mesajele sunt text, în datagrame UDP pe portul 5000. Distribuția către grup se face prin
<b>câte o datagramă unicast pentru fiecare membru</b> din lista lui A.</p>
<table><tr><th>Mesaj</th><th>De la → la</th><th>Conținut</th></tr>
<tr><td><code>DATA;n;x</code></td><td>A → fiecare membru</td><td>indicele eșantionului n și valoarea x[n] = A_s · sin(2π·n / (T·fs))</td></tr>
<tr><td><code>JOIN</code> / <code>LEAVE</code></td><td>membru → A</td><td>cerere de înscriere / retragere</td></tr>
<tr><td><code>ACK;JOIN;k</code> / <code>ACK;LEAVE;k</code></td><td>A → membru</td><td>confirmarea schimbării; k = indicele următorului eșantion la A în acel moment</td></tr>
<tr><td><code>END;80</code></td><td>A → membri</td><td>sfârșitul fluxului</td></tr></table>
<ul>
<li>Semnalul: A_s = 10, T = 4 s, fs = 2 eșantioane/s, deci un eșantion la 0,5 s și 8 eșantioane pe perioadă; A trimite 80 de eșantioane (40 s).</li>
<li><b>A nu suspendă generarea</b>: bucla din <code>main()</code> generează și trimite eșantioanele, iar cererile JOIN/LEAVE sunt tratate în
callback-ul <code>onUDPReceive</code>, care doar modifică lista și trimite confirmarea. Pentru fiecare eșantion, A trimite către o copie a listei din acel moment.</li>
<li>Membrii repetă JOIN (sau LEAVE) la 1 s până primesc ACK. B, C și D cer înscrierea imediat; <b>E</b> cere înscrierea la 15 s după pornire,
iar <b>C</b> se retrage la 45 s după pornire. Fiecare membru notează primul și ultimul indice primit.</li>
</ul>

<h2>3. Rularea</h2>
<p>Am pornit programele în ordinea B, C, D, E (la câte ~8 s) și apoi A, ca să existe membri de la începutul fluxului:
B 11:21:57, C 11:22:05, D 11:22:13, E 11:22:20, A 11:22:28. Așa, cererea lui E (11:22:35) vine după începerea fluxului,
iar retragerea lui C (11:22:50) vine în timpul rulării.</p>

<h3>Rezultate la cele două evenimente</h3>
<table><tr><th>Eveniment</th><th>Indicele următor la A în momentul schimbării</th><th>Indicele observat la membru</th><th>Concluzie</th></tr>
<tr><td>E se înscrie (JOIN)</td><td class="n">16</td><td>primul primit de E: <b>16</b></td><td>E primește exact de la eșantionul următor</td></tr>
<tr><td>C se retrage (LEAVE)</td><td class="n">46</td><td>ultimul primit de C: <b>45</b></td><td>C nu mai primește nimic după cerere (0 eșantioane în plus)</td></tr></table>

<h3>Eșantioane primite de fiecare membru</h3>
<table><tr><th>Membru</th><th>Primul indice</th><th>Ultimul indice</th><th>Eșantioane primite</th></tr>
<tr><td>B</td><td class="n">1</td><td class="n">79</td><td class="n">79</td></tr>
<tr><td>C</td><td class="n">1</td><td class="n">45</td><td class="n">45</td></tr>
<tr><td>D</td><td class="n">2</td><td class="n">79</td><td class="n">78</td></tr>
<tr><td>E</td><td class="n">16</td><td class="n">79</td><td class="n">64</td></tr></table>

<h3>Variația numărului de trimiteri per eșantion (la A)</h3>
<table><tr><th>Eșantioane</th><th>Membri în listă</th><th>Trimiteri per eșantion</th><th>Nr. eșantioane</th></tr>
<tr><td>n = 0</td><td>–</td><td class="n">0</td><td class="n">1</td></tr>
<tr><td>n = 1</td><td>C, B</td><td class="n">2</td><td class="n">1</td></tr>
<tr><td>n = 2 … 15</td><td>C, B, D</td><td class="n">3</td><td class="n">14</td></tr>
<tr><td>n = 16 … 45</td><td>C, B, D, E</td><td class="n">4</td><td class="n">30</td></tr>
<tr><td>n = 46 … 79</td><td>B, D, E</td><td class="n">3</td><td class="n">34</td></tr>
<tr><th colspan="3" style="text-align:left">Total datagrame DATA</th><th class="n">266</th></tr></table>
<p>Verificare: 0 + 2 + 3·14 + 4·30 + 3·34 = 266, același total afișat de A la final.</p>

<h3>Interpretare</h3>
<ul>
<li>Indicele „următor” notat de A la JOIN este chiar primul eșantion primit de E (16), deci înscrierea are efect de la următorul eșantion generat,
fără eșantioane pierdute sau primite în plus.</li>
<li>La LEAVE, ultimul eșantion primit de C este 45 = 46 − 1: după tratarea cererii, A nu mai trimite către C.
Nicio datagramă DATA nu era „pe drum” spre C în momentul retragerii (0 eșantioane primite după LEAVE).</li>
<li>Numărul de trimiteri per eșantion urmează numărul de membri: 3 → 4 după înscrierea lui E → 3 după retragerea lui C.
Pentru că distribuția e prin unicast, traficul lui A crește liniar cu numărul de membri.</li>
<li>Generarea nu s-a oprit în timpul cererilor: eșantioanele au rămas la ~0,5 s unul de altul (coloana t din ieșirea lui A).</li>
</ul>

<h2>4. Capturi din simulare</h2>
{fig(img("A_1.png", (0, 0, 0, 0), "88%"), "Fig. 2 – Rularea de referință la A: pornire fără membri (n = 0, 0 trimiteri), apoi JOIN de la C, B, D (indicii următori 1, 1, 2) și 3 trimiteri per eșantion. La n = 16 apare JOIN-ul lui E, după care fiecare eșantion se trimite de 4 ori.")}
{fig(img("E_sus.png", (0, 0, 0, 200), "88%"), "Fig. 3 – La E: cererea JOIN, confirmarea cu indicele următor 16 și primul eșantion primit, n = 16 (același indice).")}
{fig(img("A_3.png", (0, 260, 0, 560), "88%"), "Fig. 4 – La A: LEAVE de la 192.168.1.3 (C) când indicele următor era 46; de la n = 46 se trimite doar către B, D, E (3 trimiteri).")}
{fig(img("C_jos.png", (0, -260, 0, 0), "88%"), "Fig. 5 – La C: ultimul eșantion primit este n = 45, confirmarea LEAVE are indicele 46, iar după LEAVE nu mai sosește nimic.")}
{fig(img("A_5.png", (0, -150, 0, 0), "88%"), "Fig. 6 – Rezumatul de la A: numărul de eșantioane după numărul de trimiteri și totalul de 266 de datagrame DATA.")}
{fig(img("B_jos.png", (0, -82, 0, 0), "88%") + img("D_jos.png", (0, -82, 0, 0), "88%") + img("E_jos.png", (0, -82, 0, 0), "88%"), "Fig. 7 – Rezumatele lui B, D și E după mesajul END: primul și ultimul indice primit și numărul de eșantioane.")}

<h2>5. Codul plăcilor</h2>
<p><b>Placa A</b> (proiectul Sursa_A, main.py):</p>
<pre>{html.escape(cod_a)}</pre>
<p><b>Plăcile B, C, D, E</b> (proiectele Membru_B … Membru_E, main.py). Codul e același, se schimbă doar
<code>JOIN_DUPA</code> și <code>LEAVE_DUPA</code>: B, D: 0 și −1; C: 0 și 45; E: 15 și −1.</p>
<pre>{html.escape(cod_m)}</pre>
</body></html>"""

Path(sys.argv[1]).write_text(doc, encoding="utf-8")
print("ok", sys.argv[1])
