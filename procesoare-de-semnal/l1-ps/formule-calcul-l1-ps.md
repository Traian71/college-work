# PS L1 – toate calculele care pot pica

Formatele și convențiile sunt **exact ca în Cursul 3 și Cursul 4** (aceleași exemple ca în slide-uri și în grilele vechi).
Toate exemplele de mai jos sunt verificate numeric.

---

## 0. Ce trebuie să știi pe de rost

Ponderile sunt scrise **în ordinea în care citești biții, de la stânga la dreapta** (primul bit = cel mai mare).

**Întreg pe 8 biți** (aritmetică întreagă):

| bit | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
|---|---|---|---|---|---|---|---|---|
| pondere | **−2⁷** | 2⁶ | 2⁵ | 2⁴ | 2³ | 2² | 2¹ | 2⁰ |
| valoare | **−128** | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

→ 10100100 = −128 + 32 + 4 = **−92** (aduni ponderile de sub biții de 1).

**Fracționar pe 8 biți** (virgula e imediat după primul bit):

| bit | 1 | • | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
|---|---|---|---|---|---|---|---|---|---|
| pondere | **−2⁰** | | 2⁻¹ | 2⁻² | 2⁻³ | 2⁻⁴ | 2⁻⁵ | 2⁻⁶ | 2⁻⁷ |
| valoare | **−1** | | 0,5 | 0,25 | 0,125 | 0,0625 | 0,03125 | 0,015625 | 0,0078125 |

→ 10110000 = −1 + 0,25 + 0,125 = **−0,625**.

Pentru alte lungimi pornești de la puterea cea mai mare și cobori: 16 biți întreg = −2¹⁵ (−32768), 2¹⁴ (16384), …, 2⁰;
exponent pe 3 biți = −4, 2, 1; pe 5 biți = −16, 8, 4, 2, 1; pe 6 biți = −32, 16, 8, 4, 2, 1.
Alte puteri utile: 2⁸ = 256, 2¹⁰ = 1024, 2¹⁵ = 32768, 2¹⁶ = 65536; 2⁻⁸ = 0,00390625.

**Regula de aur (complement față de 2):** bitul cel mai din stânga (MSB) are pondere **negativă**; restul pozitive.
Aduni ponderile biților care sunt 1. Atât.

- MSB = 0 → număr pozitiv; MSB = 1 → număr negativ.
- **Scurtătură:** valoare = (citit fără semn) − 2ᴺ dacă MSB = 1. Ex: 10100100 fără semn = 164 → 164 − 256 = **−92**.
- **Negare:** inversezi toți biții și aduni 1. Ex: 92 = 01011100 → 10100011 + 1 = **10100100** = −92.
- **Extensia semnului:** când lungești un număr, copiezi MSB-ul la stânga (1101 = 11111101 = −3).

---

## 1. Virgulă fixă – aritmetică întreagă (N biți)

Ponderi: **−2ᴺ⁻¹, 2ᴺ⁻², …, 2¹, 2⁰**. Pe 8 biți: −128, 64, 32, 16, 8, 4, 2, 1.

- Interval: **[−2ᴺ⁻¹, 2ᴺ⁻¹ − 1]** → pe 8 biți: −128 … 127; pe 16 biți: −32768 … 32767.
- Pasul (rezoluția) = 1.

| Binar (8 biți) | Calcul | Zecimal |
|---|---|---|
| 01010011 | 64 + 16 + 2 + 1 | **83** (exemplul 1 din curs) |
| 10101100 | −128 + 32 + 8 + 4 | **−84** (exemplul 2 din curs) |
| 10100100 | −128 + 32 + 4 | **−92** (grila veche) |
| 11001001 | −128 + 64 + 8 + 1 | **−55** |
| 11111111 | −128 + 127 | **−1** |
| 10000000 | −128 | **−128** (cel mai negativ, „NMAX”) |
| 01111111 | 127 | **127** (cel mai mare) |

**Capcană:** 164 este citirea *fără semn* a lui 10100100, deci varianta greșită din grilă.

---

## 2. Virgulă fixă – aritmetică fracționară (N biți, format Q1.N−1)

Virgula este imediat după bitul de semn. Ponderi: **−2⁰, 2⁻¹, 2⁻², …, 2⁻⁽ᴺ⁻¹⁾** → pe 8 biți: −1, 0,5, 0,25, 0,125,
0,0625, 0,03125, 0,015625, 0,0078125.

- **Formula rapidă:** valoare = (valoarea ca întreg cu semn) / 2ᴺ⁻¹. Ex: 10110000 = −80 → −80 / 128 = **−0,625**.
- Interval: **[−1, 1 − 2⁻⁽ᴺ⁻¹⁾]** (−1 se poate reprezenta, +1 nu).
- Pasul (cel mai mic număr pozitiv) = **2⁻⁽ᴺ⁻¹⁾**: pe 8 biți 2⁻⁷ = 0,0078125; pe 16 biți 2⁻¹⁵; pe 32 biți 2⁻³¹.

| Binar (8 biți) | Calcul | Zecimal |
|---|---|---|
| 01010000 | 0,5 + 0,125 | **0,625** (exemplul 1 din curs, grila veche) |
| 10101000 | −1 + 0,25 + 0,0625 | **−0,6875** (exemplul 2 din curs) |
| 10110000 | −1 + 0,25 + 0,125 | **−0,625** (grila veche) |
| 10100000 | −1 + 0,25 | **−0,75** |
| 11010000 | −1 + 0,5 + 0,125 | **−0,375** |
| 01100000 | 0,5 + 0,25 | **0,75** |
| 01000000 | 0,5 | **0,5** |
| 10000000 | −1 | **−1** |
| 01111111 | 1 − 2⁻⁷ | **0,9921875** (cel mai mare) |

**Zecimal → binar fracționar:** înmulțești cu 2ᴺ⁻¹, rotunjești la întreg, scrii întregul în complement față de 2.
Ex: −0,375 pe 8 biți → −0,375 · 128 = −48 → 48 = 00110000 → inversat + 1 = **11010000**.

**Întreg vs fracționar = același hardware.** Diferența principală e **modul în care se tratează rezultatul înmulțirii**
(ce jumătate din produs păstrezi): la întregi partea de jos, la fracționar partea de sus (Curs 3 și 4).

---

## 3. Virgulă mobilă (formatul din curs)

Cuvântul are **mantisa (M) în stânga** și **exponentul (E) în dreapta**:

| Mantisă: −2⁰ • 2⁻¹ 2⁻² 2⁻³ 2⁻⁴ … | Exponent: −2ᵏ⁻¹ … 2¹ 2⁰ |
|---|---|

- **Mantisa** = număr **fracționar** în complement față de 2 (ca la secțiunea 2).
- **Exponentul** = număr **întreg** în complement față de 2 (ca la secțiunea 1).
- **valoare = mantisa × 2^exponent**

**Pașii (mereu aceiași):**
1. Tai cuvântul: primii m biți = mantisa, ultimii k biți = exponentul (enunțul îți spune m și k).
2. Exponent: ponderi −2ᵏ⁻¹ … 1 (pe 3 biți: −4, 2, 1; pe 5 biți: −16, 8, 4, 2, 1; pe 6 biți: −32, 16, 8, 4, 2, 1).
3. Mantisă: ponderi −1, 0,5, 0,25, 0,125, 0,0625, …
4. Înmulțești mantisa cu 2^E (E pozitiv = mut virgula la dreapta, E negativ = la stânga).

### Exemplele din curs (mantisă 10 biți, exponent 6 biți)

| Cuvânt | Mantisă | Exponent | Valoare |
|---|---|---|---|
| 0110100000 000011 | 0,5 + 0,25 + 0,0625 = 0,8125 | 3 | 0,8125 × 8 = **6,5** |
| 0100000000 111110 | 0,5 | −32+16+8+4+2 = −2 | 0,5 × ¼ = **0,125** |
| 1110100000 000011 | −1 + 0,5 + 0,25 + 0,0625 = −0,1875 | 3 | −0,1875 × 8 = **−1,5** |
| 1100000000 111110 | −1 + 0,5 = −0,5 | −2 | −0,5 × ¼ = **−0,125** (grila veche) |

### Din grilele vechi (mantisă 5 biți, exponent 3 sau 5 biți)

| Cuvânt | Format | Mantisă | Exponent | Valoare |
|---|---|---|---|---|
| 10010 001 | 5 + 3 | −1 + 0,125 = −0,875 | 1 | **−1,75** |
| 01001 011 | 5 + 3 | 0,5 + 0,0625 = 0,5625 | 3 | **4,5** |
| 10100 001 | 5 + 3 | −1 + 0,25 = −0,75 | 1 | **−1,5** |
| 11101 11001 | 5 + 5 | −1+0,5+0,25+0,0625 = −0,1875 | −16+8+1 = **−7** | −0,1875 × 2⁻⁷ ≈ −0,00146 |
| 01000 111 | 5 + 3 | 0,5 | −4+2+1 = −1 | **0,25** |

**Atenție:** dacă grila întreabă doar „valoarea exponentului”, răspunsul e doar E (ex: −7), nu valoarea finală.

### Zecimal → virgulă mobilă (invers)
Scrii numărul ca **M × 2^E** cu M între −1 și 1 (de obicei |M| ≥ 0,5), apoi codezi M fracționar și E întreg.
- 3,25 = 0,8125 × 2² → M = 01101, E = 010 → **01101010** (5 + 3).
- −3 = −0,75 × 2² → M = −0,75 = 10100, E = 010 → **10100010** (5 + 3).

### Limitele unui format în virgulă mobilă (ex. 5 + 3)
- Mantisă: de la −1 la 1 − 2⁻⁴ = 0,9375. Exponent: de la −4 la 3.
- Cel mai mare număr: 0,9375 × 2³ = **7,5**; cel mai negativ: −1 × 2³ = **−8**.
- Cel mai mic număr pozitiv: 2⁻⁴ × 2⁻⁴ = 2⁻⁸ = **0,0039**.
- Gama dinamică: 7,5 / 0,0039 = 1920 ≈ **65,7 dB**.

---

## 4. Gama dinamică și precizia

**Gama dinamică = cel mai mare număr / cel mai mic număr (pozitiv) reprezentabil.** În decibeli: **GD[dB] = 20 · log₁₀(GD)**.

| Format | Max | Min | Gama dinamică | dB |
|---|---|---|---|---|
| Fix fracționar 8 biți | 1 − 2⁻⁷ | 2⁻⁷ | 127 | 42,1 |
| Fix fracționar 16 biți | 1 − 2⁻¹⁵ | 2⁻¹⁵ | 32767 | **90,3** |
| Fix fracționar 32 biți (curs) | 1 − 2⁻³¹ | 2⁻³¹ | **≈ 2,15 × 10⁹** | **≈ 187** |
| Mobil 32 biți: 24 mantisă + 8 exp. (curs) | 3,40 × 10³⁸ | 5,88 × 10⁻³⁹ | **≈ 5,79 × 10⁷⁶** | **> 1535** |

- Regulă rapidă la virgulă fixă: **≈ 6 dB pe bit** (6,02 · (N − 1) dB). Întregii pe N biți au aceeași gamă (2ᴺ⁻¹ − 1).
- Din curs: telecom ~**50 dB** e suficient; audio de înaltă fidelitate ~**90 dB**.
- La același număr de biți, **virgula mobilă are gamă dinamică mult mai mare**.

**Precizia:**
- **Eroarea de cuantizare** = eroarea introdusă când treci la un format cu mai puțini biți (ex. 1,325 → 1,33: eroare 0,005).
- **Precizia maximă [biți] = log₂(|valoarea maximă| / |eroarea maximă de cuantizare|)**.
- Virgulă fixă: precizia maximă = **numărul de biți din format**.
- Virgulă mobilă: precizia maximă = **numărul de biți din mantisă** (24 la formatul pe 32 de biți).

**IEEE 754 (cum e dat în curs):** precizie simplă **32 biți = 24 mantisă + 8 exponent**; precizie dublă **64 biți =
52 mantisă + 12 exponent** (în curs, nu în standardul real). Mantisa și exponentul sunt numere cu semn.

---

## 5. Calea de date: înmulțire, biți de gardă, deplasări (Curs 4)

**Multiplicatorul:** n biți × n biți → produs pe **2n biți** (16 × 16 → 32). Dacă unul dintre operanzi nu poate fi cel
mai negativ număr (NMAX), ajung **2n − 1 biți**. Mantise de 24 × 24 biți → produs cu mantisa de **48** biți.
- Aritmetică fracționară: produsul are **de două ori mai mulți biți după virgulă**; se păstrează jumătatea de sus
  (+ deplasare la stânga cu 1 bit, ca să scapi de al doilea bit de semn).

**Biți de gardă = biți acumulator − biți produs.**
- DSP16xx (AT&T): acumulator 36, produs 32 → **4 biți de gardă**.
- ADSP-21xx (Analog Devices): 40 − 32 → **8 biți de gardă**.
- DSP5600x (Motorola): acumulator 56, produs 48 → **8**.
- **Cu n biți de gardă poți aduna până la 2ⁿ valori fără depășire** (4 biți → 16 valori, 8 biți → 256).
- La final se scalează: cu 4 biți de gardă pe un procesor de 16 biți, se înmulțește cu 2⁻⁴ înainte de scriere.

**Deplasări (shifter):**
- **Deplasare la stânga cu k biți** = × 2ᵏ (intră 0 în dreapta; aritmetică = logică).
- **Deplasare aritmetică la dreapta** = ÷ 2 (copiază **bitul de semn** în stânga): 010010 → **001001**; 110100 → 111010.
- **Deplasare logică la dreapta**: intră **0** în stânga, fără extensie de semn: 110100 → 011010.
- **Rotație** = deplasare circulară (bitul care iese intră în partea cealaltă), de obicei cu un bit.
- Scalarea ieșirii cu o putere a lui 2 o face **deplasatorul**.

---

## 6. Depășire, saturare, trunchiere, rotunjire (Curs 4)

**Depășire (overflow):** rezultatul nu mai încape → valoare greșită și departe de cea corectă.
Exemplul din curs, cu 2 cifre zecimale: 50 + 45 + 20 = 115 → rămâne **15**.

**Saturare:** la depășire, rezultatul e înlocuit cu **cel mai mare pozitiv** (sau **cel mai mic negativ**) reprezentabil.
Același exemplu → **99**. Tot greșit, dar mult mai aproape. Circuitul se numește **limitator**.
Pe 8 biți: 100 + 50 → saturat la **127**; −100 − 50 → **−128**.

**Trunchiere:** arunci biții cei mai puțin semnificativi. Rezultatul e **întotdeauna ≤ originalul** → introduce un
**bias (deplasament, componentă continuă)**.
- Acumulator 36 biți → memorie 16 biți: se aruncă cei mai de jos **20** de biți.
- Grila veche: 0010101 „trunchiat cu 4 biți” (se aruncă 4 biți) → 001 = **1**. Dacă înseamnă „păstrând 4 biți”: 0010 = 2.

**Rotunjire la cea mai apropiată valoare (convențională):** aduni jumătate de LSB din formatul de ieșire și apoi trunchiezi.
La egalitate (exact la jumătate) rotunjește **mereu în sus** → bias mic, dar există.

**Rotunjire convergentă** (ADSP-21xx, DSP5600x): ca mai sus, **dar la egalitate** decide bitul care devine LSB:
LSB = 0 → **în jos** (rămâne așa); LSB = 1 → **în sus** (+1). Media erorilor e 0, deci fără bias.

Cum lucrezi o grilă „rotunjire convergentă păstrând k biți”:
1. Desparți: primii k biți (păstrați) | restul (aruncați).
2. Restul < 100…0 → jos (păstrezi cei k biți). Restul > 100…0 → sus (+1).
3. Restul = 100…0 (exact jumătate) → te uiți la ultimul bit păstrat: 0 → rămâne; 1 → +1.

| Valoare | Păstrezi | Aruncat | Convergentă | La cea mai apropiată |
|---|---|---|---|---|
| 1010011000 | 6: 101001 | 1000 = jumătate, LSB = 1 | **101010** | 101010 |
| 11101010 | 6: 111010 | 10 = jumătate, LSB = 0 | **111010** | 111011 |
| 10100101 | 4: 1010 | 0101 < jumătate | **1010** | 1010 |
| 01101000 | 4: 0110 | 1000 = jumătate, LSB = 0 | **0110** | 0111 |
| 01101100 | 4: 0110 | 1100 > jumătate | **0111** | 0111 |

(Primele trei sunt grile vechi, cu răspunsurile 101010, 111010, 1010.)

**Ordinea obișnuită într-un DSP:** multiplicare → acumulare → deplasare → rotunjire.

---

## 7. Adresare – calcule (Curs 6)

- `*R5` = conținutul memoriei de la adresa din R5 (R5 nu se schimbă).
- `*R5++` = folosește adresa din R5, **apoi** R5 = R5 + 1 (post-incrementare). `*R5--` → apoi R5 − 1.
- `*R5++R17` = folosește R5, apoi **R5 = R5 + R17** (R17 = registru offset/modificator, poate fi negativ).
- `-(R0)` (Motorola) = **întâi** R0 = R0 − 1, apoi accesează (pre-decrementare).
- `X:(R5 + N6)` = adresa efectivă R5 + N6, **R5 și N6 nu se modifică** (indexare). `*-AR1(1)` → adresa AR1 − 1.
- `AX0 = DM(1000)` = directă la memorie (ia ce e la adresa 1000); `AX0 = 1234` = imediată; `P = X*Y` = implicită;
  `SUBF R1, R2` = directă la registru.
- Grila veche cu `A0 = A0 + *R3++`: A0 primește A0 + (valoarea din memorie de la adresa din R3), iar **R3 crește doar
  cu 1** (în grilă răspunsul era R3 = 0x100, deci pornea de la 0x0FF). Întrebarea „cât devine R3” nu ține de A0.

**Modulo (buffer circular):** adresa nouă = start + (offset + pas) **mod L**. Ex: **16 mod 5 = 1**; 14 mod 12 = 2.
- Bufferul începe la o graniță de **k cuvinte, k = cea mai mică putere a lui 2 ≥ L**: L = 48 → granița 64;
  L = 256 → adrese 0, 256, 512 …

**Inversarea biților (FFT radix-2):** scrii indicele în binar pe log₂N biți și îl citești invers.
- N = 8: 0, 4, 2, 6, 1, 5, 3, 7 (ex: 1 = 001 → 100 = 4; 3 = 011 → 110 = 6).
- N = 16: 0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15.

---

## 8. Capcane frecvente la calcule

- Citești numărul **fără semn** (164 în loc de −92). MSB = 1 → număr negativ, mereu.
- La fracționar, MSB valorează **−1**, nu −0,5.
- La virgulă mobilă, **exponentul e și el cu semn** (111110 = −2, nu 62).
- Ordinea e **mantisă, apoi exponent** (stânga → dreapta).
- Biți de gardă = **acumulator − produs**, nu acumulator − cuvântul de date.
- Deplasarea **aritmetică** la dreapta păstrează semnul, cea **logică** pune 0.
- Trunchierea dă mereu ceva **≤** originalul; rotunjirea convergentă la egalitate depinde de **LSB-ul păstrat**.
