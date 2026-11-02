# APD – Lucrarea 2 & 3 (Moodle: "Lucrarea 2&3 APD1")

- **Task:** upload ONE PDF with the solutions to the exercises from Lucrarea 2 and Lucrarea 3.
  Due 1 Nov 2026, 23:00. (A UML diagram from Inginerie Software was sent by mistake. It doesn't belong here.)
- **Deliverable:** `apd/lucrarea-2-3/Lucrarea_2_3_APD.pdf` (8 pages). The code for each exercise is in
  `lucrarea-2/` and `lucrarea-3/` (one VS project with a menu, like Lucrarea 1), and the measurement program
  is in `masurare/`.
- **Lucrarea 2** (grayscale images, System.Drawing):
  - Ex 1: I/O sets and graph A→B→C→D. It can't be parallelized for a single image.
  - Ex 2: Bi→Ci→Di chains, parallel by Bernstein's conditions.
  - Ex 3: static partition with 2, 3 and N threads (N from args).
  - Ex 4: Stopwatch for serial vs N=1..20, plus dynamic allocation with `lock`.
  - Ex 5: small, medium and large images.
- **Lucrarea 3:**
  - Ex 1: teacher code plus an analysis of the output.
  - Ex 2: `static int next` and a minimal lock.
  - Ex 3: an array of locks.
  - Ex 4: two lists with `_lock1`/`_lock2`.
- **Measurements:** run on the MacBook (8 logical processors). System.Drawing doesn't work on macOS, so the
  same program was ported to SkiaSharp. The PDF says this. Tserial = 318 ms for 40 × 500x500 images. The speedup
  plateaus around 2–3. Dynamic beats static on mixed sizes.
- **How it was built:** the cloud chat wrote the HTML. The Mac chat ran the measurement, filled in the
  observations, built the PDF with `sursa/build.py` and printed it with Chrome headless, then restructured
  the code. `sursa/` here has the working files. `Lucrarea_3_singur_vechi.pdf` is the earlier Lab 3-only PDF
  (superseded).
- **Status:** PDF done on 30 Oct 2026. Upload to Moodle not confirmed in chat.
- **Materials missing:** the Lucrarea 2 and Lucrarea 3 PDFs, the Moodle screenshot, and `rezultate_APD.txt`
  (raw measurement output, on the Mac Desktop).
