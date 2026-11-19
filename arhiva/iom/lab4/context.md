# IOM – Lab 4 (NLP pentru text, "L4_PLNTA2026")

- **Task:** the teacher's notebook `L4_PLNTA2026_profi.ipynb` (original in `materiale/`), 5 "Aplicații":
  preprocessing (own text with named entities and punctuation, print after each step), lexicon sentiment analysis,
  ex. 3 "run on «Experiența a fost foarte bună și frumoasă…» and justify the result", spaCy lemmatisation
  (`ro_core_news_sm`), sentiment analysis on lemmas. The teacher's code already solves ex. 2, 4 and 5.
- **Asked (19 Nov 2026):** install what's needed, put in my own text, and add brief student explanations in Romanian.
- **Environment:** conda env `PLNTA` (Python 3.12, from conda-forge because the default channel's ToS isn't accepted),
  spaCy 3.8 + `ro_core_news_sm`, pandas, Jupyter kernel `plnta` (shown as "PLNTA").
- **Deliverable:** `iom/lab4/L4_PLNTA2026.ipynb`, run with its outputs saved. Ex. 1 uses my own text (Traian, Matei,
  Muzeul Național de Artă, București, a date), with short notes after ex. 1–5. Results: ex. 2 positive (+1), ex. 3
  negative (−1, because "bună"/"frumoasă" aren't in the lexicon), ex. 5 positive (+1 after lemmatisation).
  The terminal commands in the first cell and the `!python -m spacy download` line are commented out.
- **Not run:** the last cell loads `ro_sentiment_lexicon.pkl`, which we don't have.
- **Sources:** `sursa/rezolva_lab4.py` builds and runs the notebook from the original.
- **Status:** done, not uploaded (the Moodle assignment hasn't been checked).
