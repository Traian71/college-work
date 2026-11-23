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
- **Livrabil:** `ia2/partial/Conspect_IA2_lucrare_curs.pdf` (4 pagini), copiat pe Desktop. Sursa: `sursa/conspect.html`
  (Chrome headless → PDF). Pagina 1: formule și teorie (activări, cost, SGD, backprop). Pagina 2: subiectele de anul trecut,
  corectate. Pagina 3: regularizare, CNN (cu exemplu de calcul), clasificare, PCA/ICA, plus planul de învățat (RNN scos, 23 nov). Pagina 4: foaia de formule de copiat de mână, într-un dreptunghi de 210×148 mm (½ A4).
- **Materiale:** `materiale/curs1–8.pdf`, `_curs_proinfo.pdf` (Moodle), `materiale/drive-ani-trecuti/`.
- **Status:** gata, de învățat. Nu se încarcă nimic.
