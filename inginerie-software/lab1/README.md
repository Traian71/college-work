# Merge Sort (sortare prin interclasare)

**Inginerie Software** – Proiectați algoritmul Merge Sort și reprezentați-l prin pseudocod și schemă logică,
evidențiind etapele recursive și procesul de interclasare.

Merge Sort folosește metoda **Divide et Impera**:

1. **Divide** – secvența `A[st..dr]` se împarte în două jumătăți, la mijlocul `mij = (st + dr) div 2`;
2. **Stăpânește** – fiecare jumătate se sortează **recursiv**; recursivitatea se oprește când secvența
   are un singur element (`st = dr`);
3. **Combină** – cele două jumătăți sortate se **interclasează** într-o singură secvență sortată.

## Pseudocod

```text
subalgoritm MergeSort(A, st, dr)
    dacă st < dr atunci
        mij ← (st + dr) div 2              // divide
        MergeSort(A, st, mij)              // apel recursiv – jumătatea stângă
        MergeSort(A, mij + 1, dr)          // apel recursiv – jumătatea dreaptă
        Interclasare(A, st, mij, dr)       // combină
    sfârșit dacă                           // altfel: un element, deja sortat
sfârșit subalgoritm

subalgoritm Interclasare(A, st, mij, dr)
    i ← st;  j ← mij + 1;  k ← 1
    cât timp i ≤ mij și j ≤ dr execută
        dacă A[i] ≤ A[j] atunci
            B[k] ← A[i];  i ← i + 1
        altfel
            B[k] ← A[j];  j ← j + 1
        sfârșit dacă
        k ← k + 1
    sfârșit cât timp
    cât timp i ≤ mij execută               // ce a rămas în stânga
        B[k] ← A[i];  i ← i + 1;  k ← k + 1
    sfârșit cât timp
    cât timp j ≤ dr execută                // ce a rămas în dreapta
        B[k] ← A[j];  j ← j + 1;  k ← k + 1
    sfârșit cât timp
    pentru p ← 1, k − 1 execută            // copiere înapoi în A
        A[st + p − 1] ← B[p]
    sfârșit pentru
sfârșit subalgoritm
```

Apel inițial: `MergeSort(A, 1, n)`.

Exemplu:

```text
38 27 43 3  →  38 27 | 43 3  →  38 | 27 | 43 | 3       (divizare, apeluri recursive)
            →  27 38 | 3 43  →  3 27 38 43             (interclasare, la revenire)
```

## Schema logică

Portocaliu – apeluri recursive, albastru – interclasare, verde – cazul de bază.

```mermaid
%%{init: {"flowchart": {"wrappingWidth": 400}}}%%
flowchart TD
    S(["START<br/>MergeSort(A, st, dr)"]) --> C{"st < dr ?"}
    C -- NU --> BAZA["caz de bază:<br/>un element, deja sortat"]
    C -- DA --> M

    subgraph DIV ["① Divide"]
        M["mij ← (st + dr) div 2"]
    end
    subgraph STAP ["② Stăpânește – apeluri recursive"]
        R1[["MergeSort(A, st, mij)"]]
        R2[["MergeSort(A, mij + 1, dr)"]]
    end
    subgraph COMB ["③ Combină"]
        I[["Interclasare(A, st, mij, dr)"]]
    end

    M --> R1
    R1 --> R2
    R2 --> I
    I --> E(["STOP"])
    BAZA --> E

    NOTA>"autoapel: se reia<br/>schema de la START"]
    R1 -.- NOTA
    R2 -.- NOTA

    classDef divide fill:#fff9c4,stroke:#f57f17,color:#000
    classDef recursiv fill:#ffe0b2,stroke:#e65100,color:#000
    classDef interclasare fill:#bbdefb,stroke:#0d47a1,color:#000
    classDef baza fill:#c8e6c9,stroke:#1b5e20,color:#000
    classDef nota fill:#fff,stroke:#e65100,stroke-dasharray:4 3,color:#000
    class M divide
    class R1,R2 recursiv
    class I interclasare
    class BAZA baza
    class NOTA nota
```

```mermaid
%%{init: {"flowchart": {"wrappingWidth": 400}}}%%
flowchart TD
    S(["START<br/>Interclasare(A, st, mij, dr)"]) --> I0["i ← st<br/>j ← mij + 1<br/>k ← 1"]

    I0 --> C1{"i ≤ mij și j ≤ dr ?"}
    C1 -- DA --> C2{"A[i] ≤ A[j] ?"}
    C2 -- DA --> T1["B[k] ← A[i]<br/>i ← i + 1"]
    C2 -- NU --> T2["B[k] ← A[j]<br/>j ← j + 1"]
    T1 --> K1["k ← k + 1"]
    T2 --> K1
    K1 --> C1

    C1 -- NU --> C3{"i ≤ mij ?"}
    C3 -- DA --> T3["B[k] ← A[i]<br/>i ← i + 1<br/>k ← k + 1"]
    T3 --> C3

    C3 -- NU --> C4{"j ≤ dr ?"}
    C4 -- DA --> T4["B[k] ← A[j]<br/>j ← j + 1<br/>k ← k + 1"]
    T4 --> C4

    C4 -- NU --> P0["p ← 1"]
    P0 --> C5{"p ≤ k − 1 ?"}
    C5 -- DA --> T5["A[st + p − 1] ← B[p]<br/>p ← p + 1"]
    T5 --> C5
    C5 -- NU --> E(["STOP"])

    classDef interclasare fill:#bbdefb,stroke:#0d47a1,color:#000
    class C1,C2,T1,T2,K1,C3,T3,C4,T4 interclasare
```
