# Construieste documentul APD + IS (HTML) din codul C#, rezultatele masurarii si diagrame.
# Rulare: python3 build_apd_is.py <out.html>, apoi Chrome --headless --print-to-pdf
import base64, html, sys
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[3]
cod = (ROOT / "apd/proiect-027/MergeSortCoada/Program.cs").read_text(encoding="utf-8")
rez = (D / "rezultate_APD.txt").read_text(encoding="utf-8")


def img(nume, cls=""):
    b = base64.b64encode((D / "diagrame" / nume).read_bytes()).decode()
    return f'<img class="{cls}" src="data:image/png;base64,{b}">'


linii = [l.split(";") for l in rez.splitlines() if l[:1].isdigit()]
tabel = "".join(
    f"<tr><td>{int(n):,}".replace(",", ".") + f"</td><td>{c}</td><td>{ts}</td><td>{tp}</td><td>{s}</td><td>{e}</td><td>{cc}</td></tr>"
    for n, c, ts, tp, s, e, cc in linii)

pseudocod = """SORTARE(v, n, B, K, c):
    sorteaza fiecare bloc [i*B, min((i+1)*B, n)) cu Merge Sort secvential
    sursa <- v ; dest <- vector nou de n elemente
    w <- B
    cat timp w < n:
        NIVEL(sursa, dest, n, w, K, c)
        w <- 2*w
    rezultatul este in sursa

NIVEL(sursa, dest, n, w, K, c):
    coada <- BlockingCollection noua, cu capacitatea c
    porneste PRODUCATORUL:
        pentru st = 0; st + w < n; st = st + 2*w:
            coada.Add(Pereche(st, st + w, min(st + 2*w, n)))   // asteapta daca coada e plina
        coada.CompleteAdding()                                  // finalul listei
    porneste K CONSUMATORI; fiecare executa:
        pentru fiecare p luat din coada (Take):                 // asteapta daca coada e goala
            interclaseaza sursa[p.st, p.mij) cu sursa[p.mij, p.dr) in dest[p.st, p.dr)
        // iese cand coada e inchisa si golita
    Join(producator) ; Join(consumator 1..K)
    st <- (n div 2w) * 2w
    daca st < n si st + w >= n:                                 // interval fara pereche
        copiaza sursa[st, n) in dest[st, n)
    interschimba sursa si dest"""

css = """
@page { size: A4; margin: 18mm 17mm; }
body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.4; color: #000; }
h1 { font-size: 16pt; margin: 0 0 4px; } h2 { font-size: 13pt; margin: 16px 0 6px; } h3 { font-size: 11.5pt; margin: 12px 0 4px; }
p { margin: 5px 0; } ul { margin: 4px 0; padding-left: 20px; } li { margin: 2px 0; }
pre { font-family: Menlo, Consolas, monospace; font-size: 8pt; line-height: 1.3; background: #f4f4f4; border: 1px solid #ccc; padding: 6px 8px; white-space: pre-wrap; }
pre.consola { background: #1e1e1e; color: #e6e6e6; font-size: 8.5pt; }
table { border-collapse: collapse; margin: 6px 0; font-size: 10pt; } td, th { border: 1px solid #888; padding: 3px 8px; text-align: right; } th { background: #e8e8e8; }
img { display: block; margin: 6px auto; max-width: 100%; }
.fig { text-align: center; font-size: 9.5pt; font-style: italic; margin-bottom: 8px; }
.cap { color: #333; font-size: 10pt; }
.nobreak { break-inside: avoid; }
h2, h3 { break-after: avoid; }
pre.pseudo { break-inside: avoid; }
img.mic { max-height: 105mm; }
"""

doc = f"""<!doctype html><html lang="ro"><head><meta charset="utf-8"><title>Tema 027 APD + IS</title><style>{css}</style></head><body>
<h1>Tema 027 – APD1 + IS</h1>
<p class="cap">File-Mitita Traian · Merge Sort paralel cu producător–consumator (BlockingCollection)</p>

<h2>1. APD1 – Merge Sort cu BlockingCollection</h2>
<p><b>Ideea.</b> Vectorul se împarte în blocuri consecutive de <b>B = 512</b> elemente, care se sortează fiecare cu Merge Sort
secvențial. Apoi blocurile se interclasează două câte două, pe niveluri (lățimea w = 512, 1024, 2048, …). La fiecare nivel:</p>
<ul>
<li>un thread <b>producător</b> pune în <code>BlockingCollection&lt;Pereche&gt;</code> (cu capacitate limitată) descrierile perechilor:
<code>(st, mij, dr)</code> = intervalele <code>[st, mij)</code> și <code>[mij, dr)</code>; la final apelează <code>CompleteAdding()</code>;</li>
<li><b>K = 4 consumatori</b> iau perechile din coadă (<code>GetConsumingEnumerable</code>) și le interclasează în vectorul destinație,
în intervale disjuncte, deci nu e nevoie de <code>lock</code>;</li>
<li>threadul principal face <code>Join</code> pe toți, copiază intervalul fără pereche (dacă există) și apoi schimbă rolurile vectorilor sursă/destinație.</li>
</ul>
<p>p = 1 producător + 4 consumatori = <b>5 threaduri</b>. Referința Ts este același algoritm (blocuri + interclasare pe perechi), executat secvențial.
Timpul paralel include pornirea și terminarea threadurilor, operațiile pe coadă, copierea și alocarea vectorului auxiliar.
Copiile vectorului nesortat se fac înainte de cronometrare; pentru fiecare configurație: o rulare de încălzire + 5 măsurări, media aritmetică.</p>

<h3>Codul sursă (Program.cs)</h3>
<pre>{html.escape(cod)}</pre>

<h3>Execuția programului</h3>
<p>Rulat pe MacBook Air (Apple M2, 8 procesoare logice), .NET 8, configurația Release. Ieșirea programului:</p>
<pre class="consola">{html.escape(rez.strip())}</pre>
<p>Verificarea compară rezultatul paralel cu referința secvențială (și referința cu <code>Array.Sort</code>), pentru valori oarecare și pentru
valori din [0, 100), adică cu multe duplicate. Toate cazurile sunt corecte.</p>

<div class="nobreak">
<h3>Rezultate (B = 512, K = 4 consumatori, p = 5)</h3>
<table><tr><th>n</th><th>capacitate coadă</th><th>Ts (ms)</th><th>Tp (ms)</th><th>S = Ts/Tp</th><th>E = S/p</th><th>C = p·Tp (ms)</th></tr>{tabel}</table>
</div>
<h3>Interpretare</h3>
<ul>
<li>Accelerarea e mică (S ≈ 1,4–1,5 față de p = 5). Sortarea blocurilor de 512 elemente se face secvențial (cum cere tema), iar asta înseamnă
9 din cele ~20 de niveluri ale sortării pentru n = 1.000.000. Doar interclasările sunt paralele.</li>
<li>Pe ultimele niveluri sunt puține perechi (pe ultimul nivel una singură), deci lucrează un singur consumator și ceilalți așteaptă la coadă.</li>
<li>La n = 4.000.000 accelerarea e puțin mai mare, pentru că sunt mai multe niveluri de interclasare (partea paralelă e mai mare).</li>
<li>Capacitatea 1 e ușor mai lentă: producătorul se blochează după fiecare <code>Add</code> până ia un consumator perechea.
Între 8 și 64 aproape nu e diferență, pentru că producătorul pune doar descrieri mici (3 întregi), mult mai repede decât se fac interclasările.</li>
<li>Eficiența e ≈ 0,3 și costul C ≈ 3,3–3,6 × Ts: producătorul stă aproape tot timpul (e numărat în p), iar consumatorii așteaptă pe nivelurile cu puține perechi.</li>
</ul>

<h2>2. IS – Schema fluxului perechilor</h2>
<div class="nobreak">{img("flux_perechi.png", "mic")}
<p class="fig">Fig. 1 – Fluxul perechilor la un nivel: producător → coadă cu capacitate limitată → consumatori → intervale disjuncte din vectorul destinație</p></div>

<h2>3. IS – Pseudocodul execuției unui nivel</h2>
<pre class="pseudo" style="font-size:8.5pt">{html.escape(pseudocod)}</pre>

<h2>4. IS – Diagrama de stări a consumatorului</h2>
<div class="nobreak">{img("stari_consumator.png", "mic")}
<p class="fig">Fig. 2 – Consumatorul așteaptă când coada e goală, interclasează când primește o pereche și se termină după închiderea și golirea cozii</p></div>
<p>Diagramele au fost realizate online, cu PlantUML (plantuml.com).</p>
</body></html>"""

Path(sys.argv[1]).write_text(doc, encoding="utf-8")
print("ok", sys.argv[1])
