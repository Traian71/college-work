# Construieste iom/lab4/L4_PLNTA2026.ipynb din notebook-ul profesorului si il ruleaza pe kernelul PLNTA.
# Rulare: ~/miniconda3/envs/PLNTA/bin/python arhiva/iom/lab4/sursa/rezolva_lab4.py (din radacina repo-ului)
import nbformat
from nbclient import NotebookClient

SRC = "arhiva/iom/lab4/materiale/L4_PLNTA2026_profi.ipynb"
DST = "iom/lab4/L4_PLNTA2026.ipynb"

nb = nbformat.read(SRC, as_version=4)
c = nb.cells

c[2].source = """# comenzi de rulat in terminal, nu in notebook (le-am rulat deja)
# conda activate PLNTA
# pip install spacy
# python -m spacy download ro_core_news_sm"""

c[4].source = """#importul bibliotecii
import string

text = "Pe 12 noiembrie 2026, Traian și Matei au vizitat Muzeul Național de Artă din București! A fost interesant? Da, foarte; au stat acolo 3 ore."
print(text)
#convertirea in litere mici
text = text.lower()
print(text)
#eliminarea semnelor de punctuatie
text = text.translate(str.maketrans('', '', string.punctuation))
print(text)
#tokenizarea
tokens = text.split()
print(tokens)"""

c[10].source = """#!pip install -U spacy
#!python -m spacy download ro_core_news_sm   (modelul e deja instalat in mediul PLNTA)"""

note = {
    4: "**Observație:** după fiecare pas textul se schimbă: întâi toate literele devin mici (și numele proprii, "
       "ex. „traian”, „bucurești”), apoi dispar semnele de punctuație, iar la final textul e împărțit în cuvinte "
       "după spații. Cifrele rămân, pentru că nu fac parte din `string.punctuation`.",
    6: "**Observație:** în text apar „bun” și „frumos” (+2) și „dezamăgitor” (−1), deci scorul este 1 și "
       "sentimentul este pozitiv.",
    8: "**Justificare:** rezultatul este negativ (scor −1), deși textul e mai mult pozitiv. Tokenizarea simplă "
       "păstrează cuvintele exact cum apar, iar „bună” și „frumoasă” nu sunt în lexicon (acolo sunt doar formele "
       "de bază „bun” și „frumos”). Singurul cuvânt găsit este „dezamăgitor”, de aceea scorul iese −1. "
       "Problema se rezolvă prin lematizare.",
    11: "**Observație:** spaCy aduce fiecare cuvânt la forma de bază (ex. „Filmul” → „film”, „fost” → „fi”), "
        "astfel cuvintele pot fi comparate direct cu lexiconul.",
    13: "**Observație:** acum „bună” devine „bun” și „frumoasă” devine „frumos”, deci sunt recunoscute în lexicon. "
        "Scorul este 2 − 1 = 1, sentiment pozitiv, ceea ce corespunde sensului real al propoziției.",
}
for i in sorted(note, reverse=True):
    c.insert(i + 1, nbformat.v4.new_markdown_cell(note[i]))

# ultima celula (lexiconul .pkl) nu poate rula: fisierul ro_sentiment_lexicon.pkl nu a fost primit
skip = {id(x) for x in c if "ro_sentiment_lexicon.pkl" in x.source}
for x in c:
    if id(x) in skip or (x.cell_type == "code" and not x.source.strip()):
        x.metadata["tags"] = ["skip-execution"]

nb.metadata["kernelspec"] = {"display_name": "PLNTA", "language": "python", "name": "plnta"}

client = NotebookClient(nb, kernel_name="plnta", timeout=300, skip_cells_with_tag="skip-execution")
client.execute()
for x in c:
    x.metadata.pop("tags", None)
    x.metadata.pop("execution", None)
nbformat.write(nb, DST)
print("scris", DST)
