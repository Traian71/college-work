# Proiect APD1 + IS + RC – Tema 027

- **Moodle:** „Predare teme proiect APD1 + IS + RC” (curs Inginerie software, assignid 7573, cmid 66380).
  Termen Moodle 15 Jan 2027; în listă: termen predare săptămâna 10, prezentare în săptămânile 9–10.
  Se încarcă **un singur ZIP**: un document APD+IS, separat unul RC, cod sursă și prezentarea execuției.
- **Tema aleasă de mine pe Moodle: 027** (12 nov 2026; Claude recomandase 004, dar era deja aleasă 027).
- **Enunț APD1 027:** Merge Sort pe CPU în C#; blocuri sortate secvențial cu Merge Sort, apoi interclasare pe perechi pe niveluri;
  la fiecare nivel un producător pune perechile într-o BlockingCollection cu capacitate limitată, consumatorii interclasează
  în intervale disjuncte; CompleteAdding; Join înainte de nivelul următor; intervalul fără pereche copiat înainte de swap;
  3 capacități × 2 lungimi, B și K constante; Ts = Merge Sort secvențial cu interclasare pe perechi; încălzire + ≥5 măsurări;
  S, E = S/p, C = p·Tp, p = producători + consumatori. Verificare și cu duplicate.
- **Enunț IS 027:** schema fluxului perechilor; pseudocodul unui nivel; diagrama de stări a consumatorului.
- **Enunț RC 027:** 5 plăci SBC-PT (A–E) la un switch, aceeași subrețea; A generează sinusoidă (A_s, T, fs) cu indice + valoare
  în fiecare datagramă, ține lista membrilor din JOIN/LEAVE și confirmă; unicast UDP către fiecare membru; E se înscrie după start,
  C se retrage în timpul rulării; la A indicele următor la fiecare schimbare vs primul primit de E / ultimul primit de C;
  variația numărului de trimiteri per eșantion. Predare: .pkt, codul plăcilor, raport cu tabel, capturi cu explicații.
- **Făcut (12 nov):**
  - APD: `apd/proiect-027/MergeSortCoada/Program.cs` (B = 512, K = 4, p = 5, capacități 1/8/64, n = 1M și 4M).
    Rezultate în `sursa/rezultate_APD.txt` (MacBook Air M2): S ≈ 1,40–1,53. Cu B = 4096 ieșea S ≈ 1,25–1,35, de aceea B = 512.
  - IS: diagrame PlantUML (online, `sursa/diagrame/*.puml` + png), pseudocod în document.
  - Document: `apd/proiect-027/Tema027_APD_IS_FileMitita_Traian.pdf` (6 pagini), din `sursa/build_apd_is.py` + Chrome headless.
  - RC: codul plăcilor `apd/proiect-027/RC/sursa_A.py` și `membru.py` (A_s = 10, T = 4 s, fs = 2, 80 de eșantioane;
    C pleacă la 25 s, E intră la 15 s după pornirea programului lor), testat offline cu `sursa/pt/sim_offline.py`.
- **Packet Tracer:** pluginul cisco-pt-mcp nu era încărcat în PT. Portul 7531 era ținut de o sesiune Claude veche din VS Code (10 nov),
  oprită de mine. `sursa/pt/pt_daemon.py` pornește puntea și primește comenzi pe 127.0.0.1:7532.
- **Rămas:** simularea în PT (încărcat pluginul, topologie, codul în plăci, rulare, capturi, .pkt), documentul RC, ZIP, upload.
