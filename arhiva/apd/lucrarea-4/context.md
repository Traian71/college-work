# APD – Lucrarea 4 (reducerea paralelă, sortarea, recursivitate)

- **Handout:** `materiale/Lucrarea 4 APD.pdf`, primit pe 13 nov 2026 împreună cu materialele de la IS Lab 4.
- **Cerință:** exercițiile 1–7. Ex. 1–6: suma unui vector în versiunile V1 (N threaduri fără sincronizare), V1 + mutex,
  V2 (P partiții), V3 (N/2 threaduri + Barrier), V4 = V2 + V3, V5 (threaduri recursive). Pentru fiecare se măsoară timpul și se verifică
  corectitudinea față de varianta serială. Ex. 7: minim, maxim și medie, serial și paralel.
- **Moodle:** pe 13 nov nu exista încă temă pentru Lucrarea 4 (Lucrarea 2&3 a avut o temă separată, „Lucrarea 2&3 APD1”, în cursul
  Inginerie software). Formatul n-a fost cerut, așa că am făcut ca la 2&3: un PDF cu rezolvările + codul.
- **Rezolvat 13 nov (Traian a cerut „Da, rezolv-o”):**
  - Codul: `apd/lucrarea-4/L4/Program.cs`, un singur program ca în fișă (namespace L4). N și P se pot da ca argumente.
    `Console.ReadKey()` e păstrat; pe Mac l-am rulat cu `echo x | script -q /dev/null dotnet run ...`.
  - Corecturi față de codul din fișă: un Stopwatch pentru fiecare versiune (la V1 fișa pornea timerSeq);
    `Init()` înainte de fiecare versiune (V3 și V5 scriu în `a`); la V5 copiii primesc `pos = p.pos + i` (fișa avea `pos = i`, care dă sumă
    greșită: urmărit pe hârtie, la N = 128 ar ieși 407).
  - Rulat pe Mac (M2, 8 procesoare logice, .NET 8 Release) cu N = 128, P = 16 și N = 1024, P = 16; ieșirea e în `sursa/rezultate_L4.txt`.
    V1 n-a dat niciun rezultat greșit în 10 rulări, nici la 1024 și nici la 8192: threadurile pornesc unul după altul.
    În PDF explic de ce cursa există totuși. Cu N = 8192, V3 (4096 de threaduri cu barieră) nu termina, deci tabelul rămâne la 128 și 1024.
  - PDF: `apd/lucrarea-4/Lucrarea_4_APD.pdf` (7 pagini), construit din `sursa/build_l4.py` (extrage metodele din Program.cs) + Chrome headless.
- **Status:** gata, neîncărcat; de urcat când apare tema pe Moodle.
