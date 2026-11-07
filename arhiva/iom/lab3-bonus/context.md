# IOM – Lab 3 bonus (exercise 6: formants of my own vowels)

- **Task (Moodle "Bonus ex 6 lab3", due 20 Nov 2026, .zip):** "Încărcați arhiva cu codul folosit pentru afișarea
  spectrogramelor cât și fișierul word în care ați notat frecvențele formanților." Exercise 6 of the L3 sheet: record
  the model words (vin, merg, măr, casă, mâine, bun, nor) and find the formants of each vowel.
- **Recording:** `materiale/inregistrare_cuvinte.m4a` (sent 7 Nov 2026 as „Aleea Arieșul Mare.m4a”, 48 kHz stereo,
  10.9 s, the 7 words in order with pauses). Converted with `afconvert -f WAVE -d LEI16@8000 -c 1` to
  `iom/lab3-bonus/semnale/cuvinte.wav` (8 kHz mono, like casa1.wav).
- **Deliverable:** `iom/lab3-bonus/` zipped as `lab3_bonus.zip`:
  - `ex6.py`: same style as lab3.py: reads the wav, for each word a spectrogram (Hamming 160) and the amplitude
    spectrum (n = 256) of a 20 ms frame from the middle of the vowel (`start_vocala`).
  - `L3_AnalizaInFrecventa.docx`: the lab 3 sheet (ex. 1–5 as already uploaded) with the ex. 6 table filled.
  - `semnale/cuvinte.wav`.
- **Formants (F1 / F2, Hz):** i 290/2200, e 480/1810, ă 560/1110, a 790/1290, â 320/1160, u 290/700, o 390/1000.
  Found with energy segmentation (7 words), then per-frame LPC estimates over each vowel checked against the
  spectrogram (`sursa/tracks.png`, `sursa/frames.py`); frames picked where the vowel is stable. The LPC part is only
  my check, not in the handed-in code (the sheet reads formants from the spectrogram/spectrum).
- **Status:** uploaded 7 Nov 2026 via `moodle.py submit 7196` → submitted.
