# Tema 20 – Sistem pentru administrarea unei fabrici

```mermaid
classDiagram
    direction LR
    class Fabrica {
        -nume : String
        -adresa : String
        +adaugaSectie(s : Sectie)
        +eliminaSectie(s : Sectie)
    }
    class Sectie {
        -cod : String
        -denumire : String
        +adaugaLinie(l : LinieProductie)
        +eliminaLinie(l : LinieProductie)
    }
    class LinieProductie {
        -cod : String
        -denumire : String
        -stare : String
        +adaugaMasina(m : Masina)
        +eliminaMasina(m : Masina)
    }
    class Masina {
        -serie : String
        -model : String
        -stare : String
        +mutaPeLinie(l : LinieProductie)
        +inlocuiesteCu(m : Masina)
        +getStare() String
    }
    class Operator {
        -nume : String
        -prenume : String
        -calificare : String
        +supravegheaza(m : Masina)
    }
    class InterventieMentenanta {
        -data : String
        -tip : String
        -descriere : String
        -cost : Real
        +inregistreaza()
    }

    Fabrica "1" *-- "1..*" Sectie : contine
    Sectie "1" *-- "1..*" LinieProductie : contine
    LinieProductie "0..1" o-- "1..*" Masina : foloseste
    Masina "1..*" -- "1..*" Operator : supravegheat de
    Masina "1" -- "0..*" InterventieMentenanta : are
```

## Logica relațiilor

- **Fabrica – Secție: compunere (1 – 1..\*).** Secțiile fac parte din fabrică și nu există fără ea.
- **Secție – LinieProducție: compunere (1 – 1..\*).** Fiecare linie aparține unei singure secții; dacă secția dispare, dispar și liniile ei.
- **LinieProducție – Mașină: agregare (0..1 – 1..\*).** O linie folosește mai multe mașini, dar mașina există și fără linie: poate fi mutată pe altă linie (`mutaPeLinie`) sau înlocuită (`inlocuiesteCu`). 0..1 pentru că o mașină poate fi temporar nealocată.
- **Operator – Mașină: asociere (1..\* – 1..\*).** Un operator supraveghează mai multe mașini, iar o mașină are cel puțin un operator.
- **Mașină – IntervențieMentenanță: asociere (1 – 0..\*).** O intervenție se face pe o singură mașină, iar o mașină poate avea mai multe intervenții (istoricul mentenanței periodice).

Atributele sunt private (-), iar metodele publice (+).
