# Construieste PDF-ul (HTML) pentru APD Lucrarea 4 din Program.cs si rezultate_L4.txt.
# Rulare: python3 build_l4.py <out.html>, apoi Chrome --headless --print-to-pdf
import html, re, sys
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[3]
cod = (ROOT / "apd/lucrarea-4/L4/Program.cs").read_text(encoding="utf-8")
rez = (D / "rezultate_L4.txt").read_text(encoding="utf-8")
sistem = rez.splitlines()[0].replace("Sistem: ", "")
rulari = {}
for bloc in rez.split("=== L4 ")[1:]:
    n = int(bloc.split()[0])
    rulari[n] = [l for l in bloc.splitlines()[1:] if l.strip() and not l.startswith("^D")]


def metoda(nume):
    """Extrage din Program.cs metoda 'public static ... nume(' cu tot corpul ei."""
    i = re.search(rf"\n[ \t]*public static [^\n]* {nume}\(", cod).start() + 1
    j = cod.index("{", i)
    nivel = 0
    for k in range(j, len(cod)):
        nivel += {"{": 1, "}": -1}.get(cod[k], 0)
        if nivel == 0:
            break
    linii = cod[i:k + 1].splitlines()
    ind = min(len(l) - len(l.lstrip()) for l in linii if l.strip())
    return "\n".join(l[ind:] for l in linii)


def pre(*nume):
    return "<pre>" + html.escape("\n\n".join(metoda(n) for n in nume)) + "</pre>"


def t(n, eticheta):
    """timpul (ms) din linia cu eticheta data, pentru rularea cu N = n"""
    for l in rulari[n]:
        if eticheta in l:
            return float(re.search(r"time = ([\d,]+) ms", l).group(1).replace(",", "."))


def v1_medie(n):
    v = [float(re.search(r"time = ([\d,]+)", l).group(1).replace(",", ".")) for l in rulari[n] if "ParV1 time" in l]
    return sum(v) / len(v)


def f(x):
    return f"{x:.2f}".replace(".", ",")


def iesire(n, *etichete):
    return "<pre class=\"out\">" + html.escape("\n".join(l for l in rulari[n] if any(e in l for e in etichete))) + "</pre>"


randuri = [("Serial", "Seq time", "O(N)"), ("V1 (fără sincronizare, medie 10 rulări)", None, "–"),
           ("V1 + mutex", "ParV1 + mutex", "O(N), acces serializat"), ("V2 (P partiții)", "ParV2", "O(N/P) + O(P)"),
           ("V3 (barieră)", "ParV3", "O(log N)"), ("V4 = V2 + V3", "ParV4", "O(N/P) + O(log P)"),
           ("V5 (recursiv)", "ParV5", "O(log N)")]
tabel = ""
for nume, et, cpx in randuri:
    a = v1_medie(128) if et is None else t(128, et)
    b = v1_medie(1024) if et is None else t(1024, et)
    tabel += f"<tr><td>{nume}</td><td>{cpx}</td><td class='n'>{f(a)}</td><td class='n'>{f(b)}</td></tr>"

css = """
@page { size: A4; margin: 18mm 17mm; }
body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.4; color: #000; }
h1 { font-size: 16pt; margin: 0 0 4px; } h2 { font-size: 12.5pt; margin: 16px 0 6px; break-after: avoid; }
p { margin: 5px 0; } ul { margin: 4px 0; padding-left: 20px; } li { margin: 2px 0; }
code { font-family: Menlo, Consolas, monospace; font-size: 9.5pt; }
pre { font-family: Menlo, Consolas, monospace; font-size: 8.3pt; line-height: 1.3; background: #f4f4f4; border: 1px solid #ccc; padding: 6px 8px; white-space: pre-wrap; break-inside: avoid; }
pre.out { background: #1e1e1e; color: #e6e6e6; }
table { border-collapse: collapse; margin: 6px 0; font-size: 10pt; break-inside: avoid; } td, th { border: 1px solid #888; padding: 3px 8px; } th { background: #e8e8e8; }
td.n { text-align: right; }
.cap { color: #333; font-size: 10pt; }
"""

doc = f"""<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>Lucrarea 4 APD</title><style>{css}</style></head><body>
<h1>Lucrarea 4 – Reducerea paralelă. Sortarea. Recursivitate</h1>
<p class="cap">Laborator Algoritmi Paraleli și Distribuiți – rezolvarea exercițiilor · File-Mitita Traian, 441A</p>
<p>Toate versiunile sunt în același program (<code>L4/Program.cs</code>), ca în fișa de laborator. Vectorul are elementele egale cu 1,
deci suma corectă este N. Am rulat cu <b>N = 128, P = 16</b> (valorile din fișă) și cu <b>N = 1024, P = 16</b>,
pe {html.escape(sistem)}. N și P se pot da la rulare: <code>L4.exe &lt;N&gt; &lt;P&gt;</code>.</p>
<p>Două corecturi față de codul din fișă: fiecare versiune are propriul <code>Stopwatch</code> (în fișă, la V1 se pornea <code>timerSeq</code>
și se afișa <code>timerPar1</code>), iar înainte de fiecare versiune vectorul se reinițializează cu <code>Init()</code>, pentru că V3 și V5
scriu sumele parțiale chiar în vectorul <code>a</code>.</p>

<h2>EXERCIȚIUL 1 – Versiunea paralelă V1</h2>
<p>N threaduri, fiecare adună elementul său la variabila partajată <code>sTemp</code>, fără sincronizare:</p>
{pre("ReductionParV1", "ThreadFunctionV1")}
{iesire(128, "Seq time", "ParV1 time", "V1:")}
<ul>
<li><b>Timp:</b> în medie {f(v1_medie(128))} ms la N = 128 și {f(v1_medie(1024))} ms la N = 1024, față de {f(t(128, "Seq time"))} ms serial.
Aproape tot timpul înseamnă crearea și pornirea a N threaduri, pentru o singură adunare fiecare.</li>
<li><b>Corectitudine:</b> în cele 10 rulări suma a ieșit corectă de fiecare dată (și la N = 1024). Asta nu înseamnă că V1 e corectă:
<code>sTemp += a[idx]</code> înseamnă citire, adunare și scriere, nu o operație atomică. Dacă două threaduri citesc aceeași valoare
a lui <code>sTemp</code>, una dintre adunări se pierde. Pe calculatorul meu fiecare thread termină adunarea înainte să pornească
următorul (pornirea unui thread durează mult mai mult decât o adunare), de aceea eroarea nu a apărut, dar rezultatul nu e garantat.</li>
</ul>

<h2>EXERCIȚIUL 2 – V1 cu mutex</h2>
<p>Accesul la <code>sTemp</code> se protejează cu un <code>Mutex</code>, deci un singur thread modifică suma la un moment dat:</p>
{pre("ThreadFunctionV1Mutex")}
{iesire(128, "ParV1 + mutex")}
<p>Rezultatul este corect garantat. Timpul ({f(t(128, "ParV1 + mutex"))} ms la N = 128, {f(t(1024, "ParV1 + mutex"))} ms la N = 1024)
este practic cel al lui V1: accesul la <code>sTemp</code> este serializat, deci execuția este de fapt serială, plus costul threadurilor și al mutex-ului.</p>

<h2>EXERCIȚIUL 3 – Versiunea paralelă V2</h2>
<p>Cele N elemente se împart în P = 16 partiții de N/P elemente; fiecare thread calculează serial suma partiției sale în
<code>pSum[idx]</code>, iar threadul principal adună sumele parțiale după <code>Join</code>:</p>
{pre("ReductionParV2", "ThreadFunctionV2")}
{iesire(128, "ParV2")}
<p>Rezultatul este corect (fiecare thread scrie doar în <code>pSum[idx]</code>, nu există variabilă modificată de mai multe threaduri).
Timp: {f(t(128, "ParV2"))} ms la N = 128 și {f(t(1024, "ParV2"))} ms la N = 1024, mult mai puțin decât V1, pentru că se creează doar 16 threaduri.
Pentru vectori atât de mici rămâne totuși mai lent decât varianta serială: costul pornirii threadurilor e mai mare decât adunările.</p>

<h2>EXERCIȚIUL 4 – Versiunea paralelă V3 (barieră)</h2>
<p>N/2 threaduri, log₂N pași; la fiecare pas toate threadurile se sincronizează la barieră, apoi threadurile cu
<code>idx % (2·i) == 0</code> adună elementul aflat la distanța i:</p>
{pre("ReductionParV3", "ThreadFunctionV3")}
{iesire(128, "ParV3")}
<p>Rezultatul este corect (suma totală ajunge în <code>a[0]</code>). Timpul este cel mai mare: {f(t(128, "ParV3"))} ms la N = 128 și
{f(t(1024, "ParV3"))} ms la N = 1024. Deși complexitatea teoretică e O(log N), pe un CPU cu 8 procesoare cele N/2 threaduri nu pot lucra
toate în același timp, iar fiecare pas așteaptă la barieră toate threadurile. Cu N = 8192 (4096 de threaduri) programul nu a mai terminat.</p>

<h2>EXERCIȚIUL 5 – Versiunea paralelă V4 = V2 + V3</h2>
<p>Fiecare din cele P threaduri calculează suma partiției sale (ca la V2), apoi sumele parțiale din <code>pSum</code> se reduc în
log₂P pași cu barieră (ca la V3), de aceea P trebuie să fie putere a lui 2:</p>
{pre("ReductionParV4", "ThreadFunctionV4")}
{iesire(128, "ParV4")}
<p>Rezultatul este corect. Timp: {f(t(128, "ParV4"))} ms la N = 128 și {f(t(1024, "ParV4"))} ms la N = 1024, apropiat de V2:
cu P = 16 partea finală are doar log₂16 = 4 pași în loc de 16 adunări, diferență mică față de costul pornirii threadurilor și al barierei.</p>

<h2>EXERCIȚIUL 6 – Versiunea paralelă V5 (recursivă)</h2>
<p>Fiecare thread își împarte partiția în două și pornește câte un thread pentru fiecare jumătate, până la partiții de 2 elemente;
după <code>Join</code> pe cei doi copii adună cele două sume parțiale. Nu mai e nevoie de barieră, pentru că părintele așteaptă copiii:</p>
{pre("ReductionParV5", "ThreadFunctionV5")}
<p>În codul din fișă copiii primeau <code>pos = i</code>, adică poziția față de începutul vectorului, nu față de partiția părintelui.
Pentru jumătatea a doua a vectorului, copiii ar fi lucrat tot pe începutul vectorului, iar suma ar fi ieșit greșită (urmărind pașii pe hârtie, la N = 128 ar ieși 407 în loc de 128), așa că am folosit <code>pos = p.pos + i</code>.</p>
{iesire(128, "ParV5")}
<p>Rezultatul este corect. Timp: {f(t(128, "ParV5"))} ms la N = 128 și {f(t(1024, "ParV5"))} ms la N = 1024: se creează în total
aproape N threaduri, la fel ca la V1, deci și timpul e de același ordin.</p>

<h2>EXERCIȚIUL 7 – Minim, maxim și medie</h2>
<p>Pentru acest exercițiu vectorul are valori aleatoare între 0 și 999. Varianta serială parcurge vectorul o dată pentru minim,
o dată pentru maxim și o dată pentru sumă; media = suma / N. Varianta paralelă folosește ideea de la V2: fiecare din cele P threaduri
calculează minimul, maximul și suma partiției sale, iar threadul principal le combină după <code>Join</code>:</p>
{pre("MinSeq", "MaxSeq")}
{pre("MinMaxMediePar", "ThreadFunctionMinMax")}
{iesire(128, "B:", "Seq:", "Par:")}
{iesire(1024, "Seq:", "Par:")}
<p>Ambele variante dau același minim, maxim și aceeași medie. Și aici varianta paralelă e mai lentă pentru N mic,
din cauza pornirii celor 16 threaduri.</p>

<h2>Comparația timpilor (ms)</h2>
<table><tr><th>Versiune</th><th>Complexitate</th><th>N = 128</th><th>N = 1024</th></tr>{tabel}</table>
<p>Toate versiunile sincronizate dau suma corectă. Pentru vectori mici, varianta serială e cea mai rapidă. Dintre cele paralele,
V2 și V4 sunt cele mai rapide, pentru că folosesc puține threaduri. V1, V3 și V5 creează un număr de threaduri proporțional cu N,
deci timpul lor crește cu N, chiar dacă V3 are teoretic complexitatea cea mai mică.</p>
</body></html>"""

Path(sys.argv[1]).write_text(doc, encoding="utf-8")
print("ok", sys.argv[1])
