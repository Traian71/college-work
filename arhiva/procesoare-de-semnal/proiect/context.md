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

## P3 + aplicația „Văzduh” (26 nov 2026)

- **Cerere:** găsește minusurile din P0–P2 (setul de date, calitate, eficiență) și îmbunătățește produsul; caută
  API-uri cu date reale și concurenții (Airly etc.), cum ne vindem mai bine; prognoze AI cu Claude; aplicație web
  simplă și modernă (stil iOS/Notion, se încarcă repede) cu hartă, stații cu semne diferite pe tip, backend care
  primește JSON-uri de la un script Python. Previzualizare ca artefact. Traian o pune pe ThinkCentre-ul lui, cu
  tunel Cloudflare (partea de infrastructură o face el).
- **Termen P3:** 30/11/2026, `Pr2026 –Nume_StudentID_Analiza.pdf` (SWOT + scurt SOTA). PDF-ul nu e făcut încă:
  conținutul e în `sursa/analiza-p3.md`.
- **Aplicația:** `procesoare-de-semnal/proiect/aplicatie/`
  - `server.py`: Flask. `POST /api/ingest` (JSON `{statie, timp, parametru, valoare}` sau listă; cheie în antetul
    `X-Cheie` dacă e setat `CHEIE_INGEST`), `GET /api/stare`, `GET /api/statie/<id>`, `GET /api/comunitate`.
  - `prelucrare.py`: validare (−200 = lipsă), corecție de umiditate κ-Köhler, median 3 + medie mobilă 3 cauzale,
    medii orare cu completitudine 75%, indicele EEA (benzile noi, orare), limitele Legii 104/2011.
  - `prognoza.py`: profil zilnic + persistență (+ CAMS de la Open-Meteo dacă e internet), cel mai curat interval,
    texte de la Claude (`claude-opus-5-5`, effort low, structured output, fallbacks) cu cache pe oră; fără
    `ANTHROPIC_API_KEY` scrie texte după reguli.
  - `pregatire_date.py`: `--sursa reale` (Sensor.Community + Open-Meteo, netestat aici: containerul nu avea acces
    la acele site-uri) sau `--sursa demo` (date sintetice). `simulator.py`: redă CSV-ul spre server.
  - `statii.json`: 18 stații (6 trafic, 5 parcuri, 4 școli, 3 industrial), coordonate aproximative.
  - `static/`: `index.html`, `app.css`, `app.js` (fără framework), `harta.json` (contur ANCPI CC BY 4.0, cartiere
    OSM ODbL, din pachetele npm @nspot; generat cu `sursa/aplicatie/construieste_harta.py`), `vendor/leaflet`.
- **Pornire:** `pip install -r requirements.txt`, `python3 pregatire_date.py --sursa reale --zile 30`,
  `CHEIE_INGEST=... ANTHROPIC_API_KEY=... python3 server.py` (port 5000), apoi
  `python3 simulator.py --cheie ... --interval 600` (timp real; implicit 10 s între seturi).
- **Testat aici:** server + simulator prin HTTP, toate rutele, previzualizarea pe desktop/telefon, luminos/întunecat.
- **Previzualizare (date demonstrative):** https://claude.ai/artifact/4fGRNyKrKr5kX7mQzb7PNC (privat), fișierele în
  `sursa/previzualizare/`, refăcute cu `sursa/aplicatie/export_demo.py` + `construieste_previzualizare.py`.
