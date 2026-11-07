# Procesoare de semnal – pregătire L1 (Lucrarea de verificare 1, 10 nov 2026)

- **Cerere (7 nov 2026):** „pregătește-mă 100% pentru L1 PS”: descarcă toate cursurile și capitolele de pe Moodle,
  ia grilele vechi din Drive-ul studenților (CTI Materiale-An4 → Semestrul 1 → PS) și fă ceva din care să învăț,
  în română. Testul e grilă pe foaie.
- **Ce e L1** (din `materiale/moodle/.../Modul de notare.pdf`): 40p din notă, 10 nov 2026; se poate reface odată
  cu Lucrarea de verificare 2 (12 ian 2027) și rămâne nota de la refacere. Laborator 40p, LV2 20p.
  Curs: Bogdan Alexandrescu, laborator: Dragoș Săcăleanu.
- **Format** (din `materiale/drive/Partial/GRILE PS PARTIAL.pdf`, testul de anul trecut): 10 întrebări, variante
  a–d, pot fi mai multe corecte; întrebări teoretice copiate aproape din curs.
- **Materie:** Cursurile 1–6 (+ Capitolele 1–6): 1 Introducere PDS și sisteme PDS, 2 Procesoare DSP, încapsulări,
  alternative, 3 Reprezentarea numerelor și aritmetici, 4 Calea de date, 5 Arhitectura memoriei, 6 Adresarea datelor.
- **Materiale:** `materiale/moodle/` (tot cursul de pe Moodle, `moodle.py files 5321 --save`), `materiale/drive/`
  (Partial: grilele + cursurile de anul trecut; Examen: grile de final, scanate și capturi „grile mai vechi”).
  Drive-ul nu are chei de răspuns: răspunsurile sunt deduse din textul cursului.
- **Lucru:** `sursa/text/` = textul extras din PDF-uri; `sursa/date/cursN.json` = rezumat + grile vechi rezolvate +
  grile noi pe fiecare curs, `sursa/date/grile_scanate.json` = grilele din imagini (făcute de agenți separați,
  câte unul pe curs, apoi verificate).
- **Rezultat (7 nov 2026):** pagina de studiu `procesoare-de-semnal/l1-ps/ghid-l1-ps.html`, publicată privat la
  https://claude.ai/artifact/1baXfSd4w7so9SB5KJfX3T (merge și pe telefon). Taburi: Învață (rezumat + capcane pe
  curs), Grile (pe curs / doar vechi), Simulare (10 întrebări, ~jumătate vechi), Greșeli (în browser).
  261 de grile: 78 vechi (din Drive, cu răspunsuri deduse din curs) + noi; 23 marcate „nesigur” cu motivul.
  Se refac cu `python3 sursa/build_ghid.py` din `sursa/date/*.json` + `sursa/ghid_template.html`.
- **De știut:** fișierul GRILE.RTF din „Grile final” avea doar răspunsurile, fără variante: variantele acelor
  întrebări sunt reconstruite din curs. IEEE 754 e predat în curs cu alte cifre decât standardul real (se învață
  ca în curs). Din grilele scanate, doar 8 din 46 țin de cursurile 1–6 (restul sunt pentru LV2).
- **Status:** gata de învățat.
