# CAF – Teme 1, 2, 3 (rezolvări de mână)

## Ce s-a cerut
Note comune din enunțuri: „Rezolvările se scriu de mână și se trimit (foto / scan CamScanner) prin platforma Moodle până
la data limită specificată. Nu se vor da doar rezultatele, ci vor fi incluse și calculele care au condus la acestea.”

- **Tema 1** (varianta grupele 441A, 442A; Moodle assignid 7259; termen 17 Dec 2026 08:59, la fel ca „Referate laborator”):
  1. „Se cunoaște: f(t) = a1λ1exp(−λ1t) + a2λ2exp(−λ2t). Să se determine expresiile următorilor indicatori de
     fiabilitate: R(t), F(t), z(t) și m.”
  2. „Se face o încercare de fiabilitate asupra unui eșantion de 100 circuite integrate. Defectările apar după cum
     urmează: t(h) 100 200 300 400 500 600; rCUMULAT 2 5 9 11 13 20. Să se calculeze, precizând numele indicatorilor de
     fiabilitate și unitățile de măsură: R̂(200); R̂(800); F̂(400); f̄̂(200,300); z̄̂(300,400); m̂; t̂0,2”
- **Tema 2** (assignid 8572; termen 13 Dec 2026 23:59): 1. „Se consideră diagrama de fiabilitate a unui sistem de
  telecomunicații prezentată mai jos. Să se exprime: RSIST = φ(RA...RU)” 2. „Să se calculeze RSIST pentru o structură
  fiabilistică paralel formată din n elemente Ri (i=1, ..., n).”
- **Tema 3** (assignid 8573; termen 13 Dec 2026 23:59): „a. Să se exprime RSIST = φ(RA...RZ) utilizând formula lui Bayes
  (a probabilității totale). Să se sugereze și o altă metodă de soluționare a problemei (ex: teoremele de transfigurare
  etc.). b. Să se definească și să se enumere 8 legături minimale și 8 tăieturi minimale pentru această diagramă de
  fiabilitate.”

## Livrabile
`caf/teme/CAF_Tema{1,2,3}_de_copiat.pdf` = foi de copiat de mână (2 pagini fiecare). Traian le scrie de mână, le scanează
și le încarcă. Surse: `sursa/CAF_Tema{1,2,3}.html` (Chrome headless → PDF).
Materiale: `materiale/` (enunțurile), `materiale/curs/` (Curs 1–5 de pe Moodle, cursul 5322).

## Cum s-au rezolvat (după curs 3 și 5, lab 2)
- T1.1: a1 + a2 = 1 din normare; R = a1e^(−λ1t) + a2e^(−λ2t), F = 1 − R, z = f/R, m = a1/λ1 + a2/λ2.
- T1.2 (formulele din curs 3 / lab 2): R̂(200) = 0,95; F̂(400) = 0,11; f̄̂(200,300) = 4/(100·100) = 4·10⁻⁴ h⁻¹;
  z̄̂(300,400) = 2/(91·100) = 2,2·10⁻⁴ h⁻¹; t̂0,2 = 600 h (r = n·α = 20).
  - **R̂(800): nu se poate calcula** – încercarea se oprește la 600 h și cursul spune că estimările neparametrice nu se
    extrapolează; s-a scris doar R̂(800) ≤ R̂(600) = 0,80.
  - **m̂ = 350 h** = media pe cele 20 CI defectate, cu mijlocul intervalelor (Σ = 7000 h / 20), ca în rezolvarea lab 2.
    Cu observația că 80 de CI încă funcționau, deci media pe tot lotul nu se poate estima (ar fi ≥ 550 h).
    Alternative posibile, dacă profesorul vrea altceva: capetele intervalelor → 400 h; timp total de funcționare / r
    (ipoteza exponențială) → 55000/20 = 2750 h.
- T2: citire desen: 3 blocuri în serie: (A∥B∥C∥D∥E) · [F–G ∥ ((H–I ∥ J–K)–L) ∥ ((M ∥ N–O)–(P ∥ R))] · (S ∥ T–V ∥ U).
  Etichetele „J”, „K” sunt scrise sub rândul de jos al ramurii a 2-a, „M” sub elementul de sus al ramurii a 3-a.
  În desen nu există Q, iar V există (enunțul zice RA...RU). Partea 2: R = 1 − ∏(1 − Ri), cu de Morgan.
- T3: citire desen: A în serie; N1→N2: (B–C)∥D; N1→N3: E–F; punte G–H între N2 și N3; N2→N4: (I–J)∥(K–L);
  N3→N5: M∥(N–O); punte P între N4 și N5; N4→N6: Q∥R; N5→N6: S–T; ieșire (U–V)∥W∥X∥(Y–Z).
  Bayes de două ori: întâi pe P, apoi pe G–H în fiecare caz (4 cazuri serie-paralel). Altă metodă: transfigurări
  triunghi → stea (N1–N2–N3, apoi O–N4–N5). 8 legături și 8 tăieturi minimale în PDF (graful are 144 legături minimale).

## Verificare
`sursa/verificare_diagrame.py` (+ `sursa/enumerare.c`, compilat temporar): enumerare a tuturor 2^21 (T2) și 2^26 (T3)
stări pe graful transcris, comparată cu formula pentru 4 seturi de fiabilități (3 aleatoare + toate 0,9): diferențe
≤ 2·10⁻¹², deci formulele sunt corecte pentru citirea de mai sus. Fiecare legătură/tăietură listată e verificată că e
legătură/tăietură și că e minimală. `sursa/tema1_calcule.py`: calculele T1 + verificare numerică a lui F și m la T1.1.

## Status
Rezolvări gata de copiat de mână; nu sunt încărcate.
