# PIm – Tema de laborator (15 puncte), grupa 441A

- **Moodle:** „Tema de laborator (15 puncte)”, assignid 6800, curs 5319. Termen: **6 dec 2026, 23:59**. Max 3 fișiere, orice tip.
- **Cerința (verbatim):** „Firma la care lucrați ca inginer face instruirea echipelor de programare prin cursuri interne,
  realizate prin rotație de către angajați. Ați fost solicitat să faceți verificarea cunoștințelor (teoretice și practice –
  programare Python) dobândite de colegi prin proiectarea unui test de examinare care sa verifice cunoștințele acumulate,
  corespunzătoare unui subiect de curs, pentru a cărui rezolvare sunt necesare aproximativ 30 de minute. Livrabilul pe care
  trebuie sa îl realizați este testul de examinare și baremul de corectare aferent acestuia.
  Grupa 441A: Măsuri obiective de calitate, cu referință, pentru imagini.
  Dacă folosiți pentru realizarea acestei temei sisteme generative bazate pe inteligență artificială (de tipul ChatGPT)
  trebuie să includeți in documentația livrabilului succesiunea de prompt-uri folosite și comentarii cu privire la
  corecțiile ce au fost necesare.”
- **Materia folosită** (`materiale/`): `handouts4.pdf` (curs 4, slide-urile 39–52 „Măsurarea calității imaginilor”:
  MSE, MAE, SNR, PSNR, praguri SNR 25/30 dB, SSIM), `cartePAI-04-filtrare.pdf` (rel. 3.5–3.8), `lab3-PI.zip` (MSE în
  Lab 3), `lab-pi.zip` (Lab 4: funcții mse/psnr, `lena.png`).
- **Livrabil** (`pi/tema-laborator/`): `Test_PIm_Masuri_calitate_FileMitita_Traian.pdf` (1 pag.: teorie 3 p, calcul pe
  imagine 3×3 2,5 p, Python 3,5 p, oficiu 1 p) și `Barem_PIm_Masuri_calitate_FileMitita_Traian.pdf` (2 pag.: răspunsuri,
  punctaje parțiale, soluția Python, secțiunea „Prompt-uri folosite și corecții”).
- **Decizii:** notația și PSNR cu max f0 ca la curs (255 acceptat în barem); SSIM doar la teorie (nu e în laboratoare);
  filtrare cu `boundary='symm'`; secțiunea despre AI e în barem, nu în test (testul e pentru colegi).
- **Surse** (`sursa/`): `test.html`, `barem.html`, `solutie_subiect3.py` + `output_solutie.txt`,
  `verificare_subiect2.py` + `output_verificare_subiect2.txt`, `lena.png`.
- **Status:** gata, neîncărcat. 20 nov: Traian o verifică și o încarcă singur (link: https://curs.upb.ro/2026/mod/assign/view.php?id=61891); PDF-urile copiate și în ~/Desktop/PIm tema de laborator/.
