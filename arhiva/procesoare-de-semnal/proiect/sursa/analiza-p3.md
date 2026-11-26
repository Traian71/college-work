# P3: minusuri, îmbunătățiri, piață (note de lucru, 26 nov 2026)

Note pentru PDF-ul P3 (SWOT + scurt state-of-the-art). Faptele marcate „neverificat” nu s-au putut confirma.

## Minusurile variantei P0–P2 și ce am schimbat

1. **Setul de date nu e relevant.** UCI „Air Quality”: Italia, 2004–2005, o singură stație, fără PM2.5/PM10, senzori
   cu oxizi metalici care derivă. Nu arată diferențe între zone din București.
   → Date reale din București: Sensor.Community (SDS011 + BME280, același hardware ca nodul din P1; arhivă zilnică
   deschisă, deci luni de date pentru prognoză) + CAMS prin Open-Meteo pentru NO₂ și CO (model, ~11 km).
   RNMCA (calitateaer.ro) dă API gratuit la cerere: bun ca referință pentru calibrare. În `pregatire_date.py`.
2. **Senzorii ieftini greșesc la umiditate mare.** SDS011 numără și apa din particule; iarna în București RH e 80–95%.
   → Corecție κ-Köhler cu umiditatea de la BME280: C = 1 + (κ/1,65)/(100/RH − 1), κ = 0,4 (Crilley et al. 2018,
   AMT 11:709). Validată pe OPC-N2, nu pe SDS011, deci trebuie calibrată local lângă o stație RNMCA.
3. **Prelucrare prea simplă.** Doar eliminarea lui −200 și medie mobilă: vârfurile false intrau în medii și puteau da
   alerte false. → Validare de domeniu, filtru median cauzal (3) apoi medie mobilă (3), numărarea vârfurilor,
   completitudine (media orară e validă doar cu ≥75% din eșantioane). Totul în timp real, la sosirea datelor.
4. **Praguri folosite greșit.** Comparam valori orare cu limite pe 24 h sau pe an. → „Acum” folosește indicele
   european EEA (benzile revizuite după OMS 2021, pe valori orare); limitele din Legea 104/2011 se verifică doar pe
   perioada lor (PM10 media pe 24 h, NO₂ pe oră, CO media pe 8 h).
5. **Fără prognoză**, deși concurenții au. → Prognoză pe 24 h: profilul zilnic al stației + persistență, combinat cu
   CAMS corectat local când serverul are internet, cu interval de incertitudine și „cel mai curat interval” al zilei.
   Claude primește cifrele calculate și scrie doar explicația și recomandarea.
6. **Arhitectură.** Oricine putea trimite date (fără cheie); interfață cu Chart.js, fără hartă. → Cheie de acces la
   `/api/ingest`, SQLite în modul WAL, hartă vectorială proprie (90 KB, fără servere de hărți), grafice SVG proprii
   în loc de Chart.js: pagina se încarcă mai repede.
7. **Acoperire mică.** → Estimare PM2.5 pe cartiere prin interpolare IDW (afișată ca estimare) + strat opțional cu
   senzorii cetățenilor (Sensor.Community).
8. **Nodul fizic** (pentru P4): Wi-Fi nesigur pe stradă, alimentare, soare și ploaie. → LoRaWAN sau NB-IoT,
   panou solar, carcasă cu ecran de radiații.

## Ce există deja (state of the art)

- **RNMCA / calitateaer.ro**: stații de referință. În București puține și cu goluri (1 aprilie 2024: niciuna din cele
  7 nu raporta toți poluanții, Spotmedia). Pe 11 dec. 2025 Comisia a trimis România la CJUE pentru numărul și
  amplasarea punctelor de măsurare. API gratuit, la cerere.
- **InfoAer PMB**: 44 de senzori din 2023, necertificați, valori contestate în presă.
- **Airly**: senzori proprii, campania #ȘcolileRespiră (senzori în școli). API gratuit ~100 cereri/zi, fără drept de
  redistribuire.
- **IQAir AirVisual, aqicn/WAQI**: agregatoare (stații oficiale + senzori), prognoză pe ore sau zile.
- **uRADMonitor** (rețea românească), **Aerlive.ro** (Ecopolis, agregă PMB și RNMCA).
- **Google Air Quality API** (fostul BreezoMeter): model la 500 m, prognoză 96 h, plătit după 10.000 apeluri/lună.
- **Plume Labs**: cumpărat de AccuWeather (2022), senzorul Flow nu se mai vinde.
- **CAMS Europe**: model 0,1° (~11 km), prognoză 4 zile, gratuit prin Open-Meteo doar pentru uz necomercial.
- **Context**: CJUE C-638/18 (30 aprilie 2020), depășirea sistematică a limitei zilnice PM10 în București
  (2007–2016). Directiva (UE) 2024/2881 coboară limitele până în 2030 (transpunere până la 11 dec. 2026).

## Cum ne diferențiem

- Hiperlocal pe tipuri de loc (intersecții, parcuri, școli, zone industriale), cu forme diferite pe hartă.
- Transparență: semnalul brut lângă cel filtrat, vârfurile eliminate, corecția de umiditate, completitudinea.
- Prognoză locală + explicație pe înțeles (Claude) + cel mai curat interval pentru ieșit, alergat, aerisit.
- O singură hartă pentru surse diferite (rețea proprie, cetățeni, oficial), cu sursa marcată.
- Ușoară: fără framework, hartă vectorială proprie, merge repede pe orice telefon.

## Funcții de adăugat

1. Notificări pentru o stație urmărită (școala copilului, 7:30 dimineața), ca PWA.
2. „Traseu curat”: două trasee pe jos sau cu bicicleta comparate după expunere.
3. Raport lunar pentru primărie sau școală: zile cu PM10 > 50 (max. 35/an), ore cu NO₂ > 200 (max. 18/an).
4. Widget pentru site-ul școlii sau al asociației de proprietari.
5. API deschis cu datele prelucrate.
6. Calibrare automată a nodurilor față de cea mai apropiată stație RNMCA (regresie cu umiditate și temperatură).
7. Detecția defectelor: valoare blocată, derivă, umiditate 99% constant.
8. Scenarii: cât ar scădea NO₂ într-o zi fără mașini (diferența stație de trafic / parc).

## SWOT (schelet)

- **S**: noduri ieftine (ESP32, SDS011, BME280) și hartă hiperlocală; prelucrare de semnal transparentă; prognoză cu
  explicații; date deschise și reale.
- **W**: precizia senzorilor ieftini (umiditate, derivă), fără certificare; NO₂ și CO din model, nu măsurate; puține
  noduri; dependență de servicii externe (Claude, Open-Meteo); un singur server.
- **O**: interes public mare (CJUE, directiva 2030, rețeaua oficială criticată); școli și primării care caută date;
  date deschise (Sensor.Community, CAMS); finanțări smart-city.
- **T**: concurenți mari (Airly, IQAir, Google); licențe (Airly fără redistribuire, Open-Meteo necomercial, WAQI cere
  anunț); vandalism și defecte la noduri; încredere publică scăzută în senzori (cazul PMB); costul API-ului Claude.
