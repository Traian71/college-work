# Procesoare de semnal – Proiect 2026

- **Temă (aleasă de Traian):** „Monitorizarea parametrilor de mediu în zone urbane, cu date preluate de la senzori cu
  raportare într-o aplicație web.”
- **Materiale (din Teams, echipa 04-ETTI-L-CTI-INF-A4-S1-PSPr…, canal General → Shared, de la Irina Petra MANCIU):**
  `materiale/Instructiuni realizare proiecte_202610.pdf` (liniile generale P0–P6, evaluare: documentație 40p,
  susținere 30p, funcționalitate 30p) și `materiale/Instrucțiuni și termene pentru etape de proiect_2026.pdf`.
  Pe Teams mai e și `PS_Proiect_2026.xlsx` (nedescărcat, probabil lista temelor).
- **Termene:**
  - 15/11/2026: P0, P1, P2 pe Moodle, o pagină PDF, nume `Pr2026 –Nume_StudentID_P0_P1_P2.pdf` → **încărcat 7 nov
    2026** (`procesoare-de-semnal/proiect/Pr2026 –File-Mitita_131451_P0_P1_P2.pdf`, status submitted).
  - 16–27/11: discuție pe P0–P2.
  - 30/11/2026: P3 (analiza SWOT) + un scurt studiu state-of-the-art, `Pr2026 –Nume_StudentID_Analiza.pdf`.
  - Susținere posibilă 7–18/12/2026. Bonus 5p pentru respectarea termenelor de încărcare.
- **Decizii P0–P2 (luate de mine, se pot schimba):** senzori pentru temperatură, umiditate, CO, NO₂, PM2.5/PM10;
  prelucrare (valori lipsă, medie mobilă, medii orare/zilnice, praguri din Legea 104/2011); aplicație web Flask +
  SQLite + Chart.js. **P2 = date din seturi de date folosite ca simulator de senzori** (UCI „Air Quality”, valori
  lipsă = −200), cu un nod fizic ESP32 + BME280 ca extensie posibilă, același format JSON.
- StudentID 131451 = `idnumber` din profilul Moodle.
- Sursa: `sursa/P0_P1_P2.html`, tipărită în PDF cu Chrome headless.
- **26 nov 2026:** discuția pe P0–P2 era la 17:00 și s-a mutat la 18:30. Traian a avut laborator 15–17, lucrează full-time și
  stă departe (mai sunt colegi în situație similară), deci a trimis profesoarei un mesaj pe Teams cerând susținere online.
  Mesajul e în `sursa/mesaj-teams-2026-11-26.txt`.
  Profesoara: online nu, dar se poate discuta mâine la laborator (dacă sunt doar 3). Traian: nu mai e nevoie, au
  laborator cu ea săptămâna viitoare. Ea a întrebat cine sunt ceilalți 2 și a zis că încearcă să ajungă mai
  devreme, iar Traian a răspuns că nu mai e cazul să se grăbească, rămân și o așteaptă (o neînțelegere:
  au aflat de mutare abia la facultate).
  Captura: `materiale/teams-2026-11-26.png`. **P0–P2 se prezintă tot azi, după 18.**
- **De reținut la date:** setul UCI „Air Quality” e o singură stație (un an, orar) și NU are PM2.5/PM10, doar CO,
  NOx, NO2, benzen, temperatură și umiditate. Pentru PM și mai multe stații reale se potrivește UCI „Beijing
  Multi-Site Air Quality” (12 stații, orar, PM2.5, PM10, NO2, CO, SO2, O3, temperatură și altele).
