# Completeaza tabelul de la ex. 6 (bonus) in fisa L3 deja rezolvata (ruleaza din radacina repo-ului).
# Formantii sunt masurati pe cadrele de 20 ms din ex6.py (start_vocala), vezi context.md.
import docx

FISA_IN = 'iom/lab3/L3_AnalizaInFrecventa.docx'
FISA_OUT = 'iom/lab3-bonus/L3_AnalizaInFrecventa.docx'

formanti = [
    ('i (vin)', 290, 2200),
    ('e (merg)', 480, 1810),
    ('ă (măr)', 560, 1110),
    ('a (casă)', 790, 1290),
    ('â (mâine)', 320, 1160),
    ('u (bun)', 290, 700),
    ('o (nor)', 390, 1000),
]

d = docx.Document(FISA_IN)
celula = d.tables[2].rows[14].cells[1]
tab = celula.tables[0]
for i, (voc, f1, f2) in enumerate(formanti):
    rand = tab.rows[1] if i == 0 else tab.add_row()
    rand.cells[0].text = voc
    rand.cells[1].text = f'F1 ≈ {f1} Hz, F2 ≈ {f2} Hz'

p = celula.paragraphs[-1]
p.text = ('Codul: ex6.py, semnalul: semnale/cuvinte.wav (înregistrarea mea, 8 kHz). Pentru fiecare cuvânt am '
          'afișat spectrograma și spectrul de amplitudine al unui cadru de 20 ms (n = 256) de pe la mijlocul '
          'vocalei, iar formanții i-am citit din benzile de energie din spectrogramă și din vârfurile spectrului.')
d.save(FISA_OUT)
print(FISA_OUT)
