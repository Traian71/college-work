# Construieste PDF-ul pentru APD Lucrarea 5 din L5/Program.cs si rezultate_L5.txt.
# Rulare: python3 build_l5.py  (scrie l5.html langa script si PDF-ul in apd/lucrarea-5/)
import html, re, subprocess, tempfile
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[3]
OUT = ROOT / "apd/lucrarea-5/Lucrarea_5_APD.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cod = (ROOT / "apd/lucrarea-5/L5/Program.cs").read_text(encoding="utf-8")
rez = (D / "rezultate_L5.txt").read_text(encoding="utf-8")
sistem = rez.splitlines()[0].replace("Sistem: ", "")
rulari = {}
for bloc in rez.split("=== L5 ")[1:]:
    cheie = " ".join(bloc.split()[:2])
    rulari[cheie] = [l.rstrip() for l in bloc.splitlines()[1:] if l.strip() and not l.startswith("^D")]
MIC, MARE, CRASH = rulari["43 100000"], rulari["1000000 1000000"], rulari["43 1000000"]


def metoda(nume):
    i = re.search(rf"\n[ \t]*(public|private) static [^\n]* {nume}\(", cod).start() + 1
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


def iesire(linii, *etichete):
    return "<pre class=\"out\">" + html.escape("\n".join(l for l in linii if any(e in l for e in etichete))) + "</pre>"


def timpi(linii, n):
    """(QuickSort, QuickSortPar, MergeSort, MergeSortPar) in ms pentru dimensiunea n"""
    q = m = None
    for l in linii:
        if l.startswith(f"N = {n}: QuickSort ="):
            q = [float(x.replace(",", ".")) for x in re.findall(r"= ([\d,]+) ms", l)]
        if l.startswith(f"N = {n}: MergeSort ="):
            m = [float(x.replace(",", ".")) for x in re.findall(r"= ([\d,]+) ms", l)]
    return q + m


def pivot(linii, n):
    for l in linii:
        if l.startswith(f"N = {n}: primul pivot"):
            a, b = re.findall(r"in (\d+) si (\d+)", l)[0]
            return int(a), int(b)


def f(x):
    return f"{x:.2f}".replace(".", ",")


def fn(n):
    return f"{n:,}".replace(",", ".")


def tabel(linii, dims, coloane):
    cap = "".join(f"<th>{c}</th>" for c in ["N"] + [c[0] for c in coloane])
    r = ""
    for n in dims:
        t = timpi(linii, n)
        cel = "".join(f"<td class='n'>{c[1](t)}</td>" for c in coloane)
        r += f"<tr><td class='n'>{fn(n)}</td>{cel}</tr>"
    return f"<table><tr>{cap}</tr>{r}</table>"


QCOL = [("QuickSort (ms)", lambda t: f(t[0])), ("QuickSortPar (ms)", lambda t: f(t[1])),
        ("accelerare", lambda t: f(t[0] / t[1]))]
MCOL = [("MergeSort (ms)", lambda t: f(t[2])), ("MergeSortPar (ms)", lambda t: f(t[3])),
        ("accelerare", lambda t: f(t[2] / t[3]))]
CCOL = [("QuickSort", lambda t: f(t[0])), ("QuickSortPar", lambda t: f(t[1])),
        ("MergeSort", lambda t: f(t[2])), ("MergeSortPar", lambda t: f(t[3]))]

t1m, t1M = timpi(MARE, 1000000), timpi(MARE, 100000)
t1k = timpi(MARE, 1000)
tm1 = timpi(MIC, 100000)
p100k, p1m = pivot(MARE, 100000), pivot(MARE, 1000000)

css = """
@page { size: A4; margin: 17mm 17mm; }
body { font-family: Arial, sans-serif; font-size: 10.8pt; line-height: 1.4; color: #000; }
h1 { font-size: 16pt; margin: 0 0 4px; } h2 { font-size: 12.5pt; margin: 14px 0 5px; break-after: avoid; }
p { margin: 5px 0; } ul { margin: 4px 0; padding-left: 20px; } li { margin: 2px 0; }
code { font-family: Menlo, Consolas, monospace; font-size: 9.3pt; }
pre { font-family: Menlo, Consolas, monospace; font-size: 8.2pt; line-height: 1.28; background: #f4f4f4; border: 1px solid #ccc; padding: 5px 8px; white-space: pre-wrap; break-inside: avoid; margin: 5px 0; }
pre.out { background: #1e1e1e; color: #e6e6e6; }
table { border-collapse: collapse; margin: 6px 0; font-size: 10pt; break-inside: avoid; } td, th { border: 1px solid #888; padding: 3px 8px; } th { background: #e8e8e8; }
td.n { text-align: right; }
.cap { color: #333; font-size: 10pt; }
.doua { display: flex; gap: 14px; } .doua > div { flex: 1; }
"""

doc = f"""<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>Lucrarea 5 APD</title><style>{css}</style></head><body>
<h1>Lucrarea 5 – Implementarea algoritmilor paraleli. Sortarea. Recursivitate</h1>
<p class="cap">Laborator Algoritmi Paraleli și Distribuiți – rezolvarea exercițiilor · File-Mitita Traian, 441A</p>
<p>Cele patru sortări sunt în același program (<code>L5/Program.cs</code>), cu codul din fișă. Programul sortează întâi vectorul de 64 de elemente
din fișă cu toate cele patru variante, apoi verifică sortarea pentru mai multe lungimi și măsoară timpii.
L-am rulat de două ori: cu valori între 0 și 42, ca în fișă, și cu valori între 0 și 999.999, pe {html.escape(sistem)}.
Fiecare timp este media a 3 rulări pe același vector de intrare. Înainte de măsurători fiecare sortare se rulează o dată nemăsurat,
pentru că prima rulare după pornirea programului e mai lentă.</p>

<h2>EXERCIȚIUL 1 – QuickSort serial</h2>
<p>Am folosit <code>QuickSort</code>, <code>Partition</code> și <code>Swap</code> exact ca în fișă (pivotul este ultimul element al partiției).
Pentru verificare, o funcție parcurge vectorul sortat și verifică că fiecare element e mai mic sau egal cu următorul:</p>
{pre("EsteSortat")}
{iesire(MARE, "QuickSort corect")}
<p>Sortarea este corectă pentru toate lungimile încercate, inclusiv pentru cazurile limită cu 1 și 2 elemente.</p>

<h2>EXERCIȚIUL 2 – QuickSort paralel</h2>
<p>După prima partiționare, cele două părți se sortează în două threaduri, fiecare cu <code>QuickSort</code> serial, apoi se așteaptă cu <code>Join</code>:</p>
{pre("QuickSortPar")}
<p>Corectitudinea față de varianta serială: ambele variante pornesc de la o copie a aceluiași vector, iar o funcție compară element cu element
rezultatul paralel cu cel serial. Rezultatul a fost identic la toate dimensiunile (<code>egal cu serial: True</code>).</p>
<p><b>Valori între 0 și 999.999:</b></p>
{tabel(MARE, [1000, 10000, 100000, 1000000], QCOL)}
<ul>
<li>La N = 1000 varianta paralelă e mai lentă ({f(t1k[1])} față de {f(t1k[0])} ms), pentru că pornirea celor două threaduri costă mai mult decât sortarea.</li>
<li>Accelerarea nu poate trece de 2, pentru că se folosesc doar două threaduri. În plus, prima partiționare (O(N)) se face serial, iar
cele două părți nu sunt egale: depind de unde cade pivotul. La N = 100.000 primul pivot a împărțit vectorul în {fn(p100k[0])} și {fn(p100k[1])}
elemente, aproape egal, și accelerarea a fost {f(t1M[0] / t1M[1])}. La N = 1.000.000 împărțirea a fost {fn(p1m[0])} și {fn(p1m[1])}, iar threadul cu partea
mare a lucrat mult mai mult, deci accelerarea a scăzut la {f(t1m[0] / t1m[1])}.</li>
</ul>
<p><b>Valori între 0 și 42 (ca în fișă):</b></p>
{tabel(MIC, [1000, 10000, 100000], QCOL)}
<ul>
<li>Aici vectorul are foarte multe valori egale (la N = 100.000, fiecare valoare apare de aproximativ 2300 de ori). Cu <code>a[j] &lt;= pivotValue</code>,
o partiție în care toate elementele sunt egale cu pivotul se împarte în 0 și restul, adică exact cazul cel mai defavorabil din fișă: QuickSort devine O(N²).
La N = 100.000 durează {f(tm1[0])} ms, față de {f(t1M[0])} ms cu valori diferite.</li>
<li>La N = 1.000.000 adâncimea recursivității ajunge la zeci de mii de apeluri, iar programul se oprește cu <code>Stack overflow</code> chiar în threadul
creat de <code>QuickSortPar</code> (threadurile create au o stivă mai mică decât threadul principal):</li>
</ul>
<pre class="out">{html.escape(chr(10).join(l for l in CRASH if "Stack overflow" in l or "Repeat" in l))}
   at L5.Program.QuickSort(Int32, Int32)
   ...
   at L5.Program+&lt;&gt;c__DisplayClass12_0.&lt;QuickSortPar&gt;b__0()</pre>
<p>De aceea tabelul cu valori 0–42 se oprește la 100.000.</p>

<h2>EXERCIȚIUL 3 – MergeSort serial</h2>
<p>Am folosit <code>MergeSort</code> și <code>Merge</code> ca în fișă; verificarea se face cu aceeași funcție <code>EsteSortat</code>, pe aceleași
lungimi (partea <code>MergeSort corect</code> din ieșirea de la Exercițiul 1). Sortarea este corectă pentru toate lungimile. Spre deosebire de QuickSort, MergeSort împarte mereu vectorul la jumătate, deci
nu depinde de valori: cu valori 0–42 a funcționat la fel de bine (chiar mai repede).</p>

<h2>EXERCIȚIUL 4 – MergeSort paralel</h2>
<p>Cele două jumătăți se sortează în două threaduri, iar după <code>Join</code> threadul principal face <code>Merge</code>:</p>
{pre("MergeSortPar")}
<p>Rezultatul a fost identic cu cel serial la toate dimensiunile.</p>
<div class="doua"><div><p><b>Valori între 0 și 999.999:</b></p>{tabel(MARE, [1000, 10000, 100000, 1000000], MCOL)}</div>
<div><p><b>Valori între 0 și 42:</b></p>{tabel(MIC, [1000, 10000, 100000], MCOL)}</div></div>
<p>Accelerarea este aproape constantă, în jur de {f(t1m[2] / t1m[3])}, pentru că jumătățile sunt mereu egale. Nu ajunge la 2 pentru că ultimul
<code>Merge</code> (N elemente) se face serial, după ce s-au terminat ambele threaduri.</p>

<h2>Comparație QuickSort – MergeSort (ms, valori între 0 și 999.999)</h2>
{tabel(MARE, [1000, 10000, 100000, 1000000], CCOL)}
<ul>
<li>Serial, QuickSort este mai rapid ({f(t1m[0])} față de {f(t1m[2])} ms la N = 1.000.000): lucrează în același vector, pe când MergeSort
alocă vectorii <code>L</code> și <code>R</code> la fiecare <code>Merge</code>.</li>
<li>Paralel, QuickSortPar a fost mai rapid ({f(t1m[1])} față de {f(t1m[3])} ms), dar câștigul lui depinde de pivot. MergeSortPar are o accelerare
mai stabilă, pentru că împarte mereu în două jumătăți egale.</li>
<li>Cu multe valori egale (0–42), MergeSort e de departe mai bun: QuickSort ajunge la O(N²) și poate depăși stiva, MergeSort rămâne O(N log N).</li>
</ul>
</body></html>"""

(D / "l5.html").write_text(doc, encoding="utf-8")
with tempfile.TemporaryDirectory() as t:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={t}/p", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT}", (D / "l5.html").as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(OUT)
