# Tema 18 – Sistem de organizare a unei firme IT

```mermaid
classDiagram
    direction TB
    class FirmaIT {
        -nume : String
        -adresa : String
        +adaugaEchipa(e : Echipa)
        +eliminaEchipa(e : Echipa)
    }
    class Echipa {
        -nume : String
        +adaugaMembru(a : Angajat)
        +eliminaMembru(a : Angajat)
    }
    class Proiect {
        -denumire : String
        -termen : String
        -stare : String
        +adaugaParticipant(a : Angajat)
        +schimbaStare(s : String)
    }
    class Angajat {
        -nume : String
        -prenume : String
        -salariu : Real
        +participaLa(p : Proiect)
    }
    class Programator {
        -limbaj : String
        +scrieCod()
    }
    class Tester {
        -tipTestare : String
        +testeaza(p : Proiect)
    }
    class Analist {
        -domeniu : String
        +analizeazaCerinte(p : Proiect)
    }
    class Manager {
        -experientaAni : Integer
        +coordoneaza(p : Proiect)
    }

    FirmaIT "1" *-- "1..*" Echipa : contine
    Echipa "1" o-- "1..*" Angajat : are
    Echipa "1" -- "1..*" Proiect : dezvolta
    Angajat "1..*" -- "0..*" Proiect : participa la
    Manager "1" -- "0..*" Proiect : responsabil de
    Angajat <|-- Programator
    Angajat <|-- Tester
    Angajat <|-- Analist
    Angajat <|-- Manager
```

## Logica relațiilor

- **FirmaIT – Echipă: compunere (1 – 1..\*).** Echipele fac parte din firmă și nu există fără ea.
- **Echipă – Angajat: agregare (1 – 1..\*).** O echipă are mai mulți angajați, dar angajatul există și separat și poate fi mutat în altă echipă.
- **Echipă – Proiect: asociere (1 – 1..\*).** O echipă dezvoltă unul sau mai multe proiecte, iar fiecare proiect este dezvoltat de o echipă.
- **Angajat – Proiect: asociere (1..\* – 0..\*).** Un angajat poate participa la mai multe proiecte, iar un proiect are mai mulți angajați.
- **Manager – Proiect: asociere (1 – 0..\*).** Fiecare proiect are un singur manager responsabil, iar un manager poate răspunde de mai multe proiecte.
- **Generalizare: Programator, Tester, Analist, Manager → Angajat.** Toate rolurile au în comun nume, prenume, salariu și participarea la proiecte, deci le moștenesc din Angajat; fiecare rol are în plus atributele și metodele lui specifice.

Atributele sunt private (-), iar metodele publice (+).
