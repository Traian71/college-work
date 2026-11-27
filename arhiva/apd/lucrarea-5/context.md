# APD – Lucrarea 5 (sortarea paralelă: QuickSort și MergeSort)

- **Handout:** `materiale/Lucrarea 5 APD.pdf` (Moodle, cursul Inginerie software 5320, secțiunea 23–29 nov, pus vineri 27 nov 2026 10:04).
- **Cerință:** Ex. 1 QuickSort serial + verificare pe vectori de diverse lungimi; Ex. 2 QuickSort paralel (2 threaduri după prima
  partiționare), timp + corectitudine față de serial; Ex. 3 MergeSort serial + verificare; Ex. 4 MergeSort paralel, timp, corectitudine,
  comparație cu QuickSort.
- **Cerut 27 nov 2026:** „rezolvă și celelalte lucrări… și dă-le upload… în manieră de student, doar cu ce ni se dă din laboratoare”.
- **Rezolvare:** `apd/lucrarea-5/L5/Program.cs` (un singur program cu toate 4 sortările, codul din fișă neschimbat) + `apd/lucrarea-5/Lucrarea_5_APD.pdf`
  (3 pagini, ca la L4: cod, ieșiri, tabele, observații). PDF construit cu `sursa/build_l5.py` din Program.cs + `sursa/rezultate_L5.txt`.
- **Rulare:** `~/.dotnet/dotnet bin/Release/net8.0/L5.dll <MAXV> <NMAX>` (cu `dotnet run -- args` prin `script` argumentele nu ajungeau).
  Configurații: `43 100000` (valori 0–42 ca în fișă), `1000000 1000000` (valori 0–999.999), `43 1000000` (arată stack overflow-ul).
  Timpi = media a 3 rulări + o rulare de încălzire nemăsurată (fără ea, primul QuickSort serial ieșea de 2× mai lent din cauza JIT și
  accelerarea părea >2 cu 2 threaduri).
- **Rezultate (M2, 27 nov):** valori mari, N = 10⁶: QuickSort 64,5 / Par 43,9 ms (pivot 69%/31%), MergeSort 97,8 / Par 53,1 ms.
  Valori 0–42: QuickSort devine O(N²) (multe egale, `<=` în Partition), 103,6 ms la 10⁵ vs 6,2 ms MergeSort; la 10⁶ `Stack overflow`
  în threadul din QuickSortPar (stivă mai mică decât threadul principal). Toate rezultatele paralele egale cu cele seriale.
- **Moodle:** pe 27 nov nu există temă pentru Lucrarea 5 (nici pentru L4). Status: gata, neîncărcat.
