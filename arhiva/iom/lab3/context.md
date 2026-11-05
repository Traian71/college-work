# IOM – Lab 3 (frequency analysis of speech, "L3_AnalizaInFrecventa")

- **Task:** the lab sheet `L3_AnalizaInFrecventa.docx` (original in `materiale/`): FFT amplitude spectrum of an "a"
  frame from `casa1.wav`, spectrogram, formants, a GUI for exercise 5, and a bonus (exercise 6) with my own
  recordings of the 7 model words (vin, merg, măr, casă, mâine, bun, nor). Asked to solve it the same way as lab 2.
- **Deliverable:** `iom/lab3/`:
  - `L3_AnalizaInFrecventa.docx`: the filled sheet (ex. 1–5, with the spectrum and spectrogram plots).
  - `lab3.py`: exercises, in `#%%` cells, using the sheet's code.
  - `GUI_ex5.py`: Tkinter GUI (same structure as lab 2's GUI): file, start/stop of the frame, spectrogram window,
    shows the frame, the amplitude spectrum (n = next power of 2) and the spectrogram.
  - `semnale/casa1.wav`: copied from lab 2.
  As in lab 2, the upload is this folder zipped.
- **Results:** frame 9600–9760 (20 ms, n = 256); spectrogram of 9300–10200 has 6 frames; formants F1 ≈ 800 Hz,
  F2 ≈ 1600 Hz (sheet says 850 / 1500 for "a", female voice).
- **Sources:** `sursa/completeaza_fisa.py` fills the sheet and makes `sursa/spectru.png`, `sursa/spectrograma.png`;
  `sursa/gui_fig.png` is a test render of the GUI.
- **Status (5 Nov 2026):** ex. 1–5 done. Bonus (ex. 6) not done: it needs my recordings. Not uploaded yet.
