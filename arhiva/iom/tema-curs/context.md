# IOM – Tema de curs (Moodle "Tema curs", assignid 7374, due 12 Dec 2026, one .zip)

- **Task (verbatim summary):** pick a subject in the IOM field (one from the course, deeper, or a related new one).
  1) written document, word/pdf, 5 pages, Times New Roman / Calibri / Arial 12 pt, 1.5 spacing, 2.5 cm margins,
  justified; 2) a 5-minute recorded oral presentation with 4–6 slides (keywords, figures, no long text). The slides are
  uploaded on Moodle and contain the link to the recording. Optional: present live in the week-12 course.
  Announced on Teams (IO-Ma team, Andreea Griparis, 6 Nov 2026).
- **Topic (chosen by Claude, 7 Nov 2026, Traian asked me to pick):** „Recunoașterea automată a vorbirii: de la
  parametrii semnalului vocal la rețelele neuronale” – builds on courses 2–3 (voice-based HMI, short-time parameters,
  spectrum, cepstral/LPC) and labs 2–3; uses Traian's own recording of „casă” (lab 3 bonus) for a spectrogram figure.
- **Files:**
  - `iom/tema-curs/Tema_curs_IOM_FileMitita_Traian.pdf`: 5 pages exactly (Chrome print of `sursa/document.html`,
    TNR 12, line-height 1.725 ≈ Word's 1.5 lines, 2.5 cm, justify). Sections: introducere, parametri (cadre,
    energie/ZCR/F0, spectru, formanți, MFCC, LPC), clasic (DTW, HMM-GMM, Viterbi), rețele neuronale (DNN-HMM, CTC,
    codor–decodor, Whisper 680.000 h, WER), asistent vocal (wake word → ASR → NLU → TTS), provocări, concluzii, 6 refs.
  - `iom/tema-curs/Prezentare_IOM_FileMitita_Traian.pptx`: 6 slides (python-pptx, `sursa/build_slides.py`), the
    script is in each slide's notes. Slide 1 has a placeholder „[link de adăugat]” for the recording link:
    rebuild with `uv run --no-project --with python-pptx --with scipy --with numpy --with matplotlib python
    arhiva/iom/tema-curs/sursa/build_slides.py "<link>"`.
  - `Script_prezentare.pdf` (here, not handed in): what to read per slide, ~560 words ≈ 4.5–5 min.
  - Copies of all three in `~/Desktop/IOM tema curs/`.
- **Careful:** opening the pptx in the work-managed PowerPoint and exporting/saving adds the Oracle sensitivity label
  („Confidential – Oracle Restricted”). The pptx built by the script is clean; don't upload a version saved from
  that PowerPoint without checking.
- **Status (7 Nov):** document, slides and script ready. Waiting for Traian's recording + link; then rebuild slides with
  the link, zip PDF + PPTX, `moodle.py submit 7374`.
- **Alegerea temei (13 nov):** profesoara cere completarea fișierului de alegere a temei (link pe Moodle) până pe 1.12.2026.
  Traian completează singur, pe rândul lui (44, 441_sgB), titlul: „Recunoașterea automată a vorbirii: de la parametrii semnalului vocal la rețelele neuronale”.
