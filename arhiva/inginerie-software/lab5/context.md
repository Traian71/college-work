# Inginerie Software – Lab 5 (diagrame de secvență și colaborare)

- **Handout:** `materiale/IS Laborator 4 - Diagrame Sequence si Collaboration(Interaction).pdf` (Moodle, IS_Laborator_5, pus vineri 27 nov 2026 16:25).
- **Exercițiu (din fișă):** „Sa se elaboreze o diagrama de tip secventa reprezentand scenariul de promovare a unui student la un curs la care
  participa (participare la curs, laborator, sustinerea examen, eventual re-evaluare/restanta, plata taxe etc).”
- **Teams:** pe 27 nov n-am putut verifica (Teams cerea sign-in în browser pane). La Lab 4 instrucțiunea reală de pe Teams era alta decât fișa,
  deci de verificat General din ISo-A când e logat.
- **Rezolvare (27 nov):** diagramă de secvență în app.diagrams.net, ca la Lab 4: obiecte s:Student, sec:Secretariat, p:Profesor, c:Catalog,
  15 mesaje numerotate cu sintaxa din fișă ([condiție] *[iterații] nr : var := operație(arg)), perioade de activare, un mesaj către sine
  (8 : notaExamen := corecteaza(lucrare)), mesaje de răspuns punctate, bloc `alt` [notaExamen ≥ 5] promovare / [notaExamen < 5] restanță
  (plată taxă, chitanță, susținere restanță, notă). Generată cu `sursa/drawio/genereaza.py` → `.drawio` + link `#R`, printscreen editor
  cu Chrome headless 1440×900.
- **Livrabil:** `inginerie-software/lab5/IS_Lab5_secventa_promovare_student_FileMitita_Traian.png`.
- **Moodle:** pe 27 nov nu există încă assignment IS_Laborator_5. Status: gata, neîncărcat.
