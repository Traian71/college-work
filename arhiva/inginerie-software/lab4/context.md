# Inginerie Software – Lab 4 (Moodle IS_Laborator_4, assignid 8567, cmid 71837)

- **Task (din „IS Laborator 3 - Diagrame Activitate si Use Case.pdf”, Exercitii laborator):** „Sa se elaboreze o diagrama de tip
  activitate si una de tip use case reprezentand scenariul de promovare a unui student la un curs la care participa
  (participare la curs, laborator, sustinerea examen, eventual re-evaluare/restanta, plata taxe etc).”
- **Moodle:** deschis 13 nov 2026, termen 24 nov 2026 00:00; acceptă doar imagini, max 2 fișiere.
- **Materiale:** cele două PDF-uri de la IS în `materiale/` (fișa de laborator + comparația diagramă logică / activitate / use case).
  „Lucrarea 4 APD.pdf” a venit în același mesaj, dar e de la APD: e în `arhiva/apd/lucrarea-4/materiale/`.
- **Rezolvare (13 nov):** PlantUML (online, plantuml.com), ca la Lab 3. Surse în `sursa/*.puml`.
  - Activitate: benzi Student / Cadru didactic / Secretariat; fork-join curs ∥ laborator; decizii laborator promovat,
    nota ≥ 5 (altfel taxă restanță → restanță → nota ≥ 5, altfel reface cursul), mulțumit de notă (altfel re-evaluare); nota în catalog.
  - Use case: actori Student, Cadru didactic, Secretariat; include (laborator → teme, examen → corectare, restanță → taxă),
    extend (restanță → examen dacă nota < 5, re-evaluare → consultă nota).
- **Predat:** `inginerie-software/lab4/IS_Lab4_diagrama_activitate_FileMitita_Traian.png` și `..._use_case_...png`,
  încărcate pe Moodle pe 13 nov 2026 (status submitted, ambele fișiere confirmate).
