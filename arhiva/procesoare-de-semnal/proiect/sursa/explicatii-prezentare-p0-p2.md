# Explicații pentru discuția pe P0–P2 (26 nov 2026)

## PM2.5 și PM10
- Particule în suspensie (praf, fum, funingine). Cifra = diametrul maxim în µm. PM10 < 10 µm (praf de drum,
  șantiere, frâne/anvelope), PM2.5 < 2,5 µm (arderi: diesel, sobe, industrie), ajung adânc în plămâni.
- µg/m³. Legea 104/2011: PM10 50 µg/m³ medie zilnică, PM2.5 25 µg/m³ medie anuală.
- Senzor optic (SDS011): laser + fotodiodă, lumina împrăștiată de particule dă impulsuri, din ele se
  calculează concentrația.

## Date
- Dataset = tabelul cu măsurători; datasheet = foaia de catalog a senzorului.
- UCI „Air Quality”: o stație, fără PM. Pentru PM și mai multe stații: UCI „Beijing Multi-Site Air Quality”.
- Scriptul trimite câte o măsurătoare (JSON: stație, timp, parametru, valoare) la câteva secunde.

## Media mobilă și filtrul median (fereastră de 3, PM10: 40 42 41 90 43 44, 90 = vârf fals)
- Media mobilă: y[n] = (x[n] + x[n-1] + x[n-2]) / 3, filtru FIR trece-jos. Rezultat: 41 / 57,7 / 58 / 59.
  Netezește zgomotul mic, dar vârful se „întinde” pe vecini.
- Filtrul median: sortezi fereastra și iei valoarea din mijloc (neliniar). Rezultat: 41 / 42 / 43 / 44.
  Vârful dispare complet, iar schimbările reale care durează se păstrează.
- Ordinea: scoatem valorile lipsă (−200) → median (vârfuri) → medie mobilă (zgomot) → medii orare/zilnice → praguri.
  Ajută la: fără alerte false din cauza unui singur vârf, grafice curate, medii corecte.
