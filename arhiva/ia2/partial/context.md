# IA2 – lucrarea de la curs (parțial), miercuri 25 nov 2026

- **Cerere (23 nov 2026):** Traian vrea un conspect mic pentru lucrarea de la curs de miercuri, cât să ia o notă de trecere
  „de bun simț”. Are 2 zile (luni, marți). Apoi a confirmat: **intră cursurile 1–7** (fără RNN). Are voie cu o **foaie de formule scrisă de mână, cât ½ pagină**.
- **Ce știm:** `_curs_proinfo.pdf`: „20 puncte: lucrare în săptămânile 6-7 (fără redare)”, laborator 40 p, final 40 p. Pe Moodle
  (curs 5318) forumul Announcements e gol. Teams nu s-a putut verifica (cerea logare în browser pane). Cursurile predate: 1–8
  (curs8 = RNN, urcat pe 17 nov).
- **Test anul trecut** (Drive „CTI Materiale-An4 / Semestrul 1 / IA2-RF / Test intermediar”, în `materiale/drive-ani-trecuti/`):
  2 variante, câte 2 probleme: forward pass rețea mică (sigmoid/ReLU) + teorie activări; cost CE cu softmax / MSE + un pas SGD
  pentru x = Ay + b cu A_ij = w_{i-j}. Rezolvarea din Drive are greșeli: la v2 h2 calculat cu w21 în loc de w12 (corect h2 = −0,5 →
  h4 = 0, o1 = 0, o2 = −1,5), la SGD lipsesc bias-urile, la v1 O1 = 1,0997 (nu 1,1006). Verificat în Python.
  În Drive mai sunt `Examen/Ce_s_a_dat.jpg` (salvat) și „Final exemplu” + „Foaie de formule Final” (pentru finalul din ianuarie, nedescărcate).
- **Livrabil:** `ia2/partial/Conspect_IA2_lucrare_curs.pdf` (17 pagini), copiat pe Desktop. Refăcut pe 23 nov la cererea lui:
  nimic criptic, fiecare formulă explicată pe românește, scheme pentru fiecare rețea și calcul, pașii pe rânduri separate,
  culori calde (nu albastru), mult spațiu. Capitole: 1 neuronul, 2 rețeaua (cu explicația indicilor w_ji, w_j0, a_j, z_j),
  3 activări (grafice + plusuri/minusuri + răspunsuri gata făcute), 4 cost, 5 gradient descent + backprop (optimizatorii explicați pe larg cu notația din curs 5: momentum, Nesterov,
  AdaGrad cu exemplu numeric, RMSProp, Adam cu corecția; adăugat pe 24 nov la cererea lui),
  6 subiectele de anul trecut rezolvate cu scheme (fiecare cu enunțul integral transcris + schema originală decupată din poză,
  `sursa/enunt/`; adăugat tot pe 23 nov la cererea lui), 7 restul (regularizare, CNN, clasificare, PCA/ICA), 8 foaia de formule (½ A4).
- **24 nov:** la V1 P2 c) (SGD) a cerut fără tabel: acum pașii sunt scriși explicit, cum cere enunțul — ieșiri, erori $x_i - t_i$ (fără notația $e_i$, la cererea lui),
  E = 0,4354, apoi (la cererea lui) E scris complet cu ponderile și fiecare din cele 8 derivate desfăcută paranteză cu paranteză
  (½·2·(paranteza)·ce rămâne, cu parametrul colorat; „0” unde nu apare), apoi pasul pe fiecare parametru. Conspectul are acum 17 pagini.
- **Surse:** `sursa/build_conspect.py` (rulează `python3 build_conspect.py`) = `conspect_template.html` (text, KaTeX din CDN)
  + `scheme.py` (toate schemele SVG) → `conspect.html` → PDF cu Chrome headless.
- **Materiale:** `materiale/curs1–8.pdf`, `_curs_proinfo.pdf` (Moodle), `materiale/drive-ani-trecuti/`.
- **Status:** gata, de învățat. Nu se încarcă nimic.
