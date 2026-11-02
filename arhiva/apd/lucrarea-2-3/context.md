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
- **How it was built:** the cloud chat wrote the HTML. The Mac chat ran the measurement on 30 Oct 2026
  (`~/.dotnet/dotnet run -c Release` in `apd/lucrarea-2-3/masurare/`, macOS 26.7.1), wrote the three observations
  (`sursa/observatii.json`) from the real numbers, built the PDF with `sursa/build.py` and printed it with Chrome headless:
  `python3 sursa/build.py sursa sursa/rezultate_APD.txt sursa/observatii.json /tmp/combined.html`, then
  `Google Chrome --headless --no-pdf-header-footer --print-to-pdf=... file:///tmp/combined.html`.
  Rebuilding from these files gives the same PDF text. The program generates its test images in `$TMPDIR/APD_Masurare`
  with a fixed seed (40 × 500x500 for Ex 4, 16 mixed sizes with the large ones first for the dynamic test,
  40 × 100x100 / 40 × 500x500 / 8 × 2000x2000 for Ex 5). Times vary a little between runs.
- **Results (if asked):** Ex 4: speedup 2,32 at N=3, then 2,1–3,2 (max 3,15 at N=15), never near 8.
  Dynamic vs static on mixed sizes: N=4 204 vs 402 ms; static gives the big images (start of the list) to thread 0.
  Ex 5 (N=4): speedup 2,5–5,5. Small images had the largest speedup, but their times are only 8–44 ms, so that
  isn't reliable (this differs from the "little gain on small images" we expected). Equal sizes: static ≈ dynamic
  (125/121, 338/345 ms). Lab 3 Ex 1, mixed sizes, N=4: threads took 9, 4, 2 and 1 images.
- **Code changes on 30 Oct:** Lab 2's code (written 16 Oct, never committed before) was aligned with the PDF:
  `Exercitiul4b.cs` now uses `lock` and marks taken images (it was a `Mutex` + counter), and `Exercitiul5.cs` makes
  40 / 40 / 8 images (it was 10 of each). Lab 3's `.cs` files were written from the code in the PDF, with the `...`
  parts filled in. Everything compiles; Lab 2/3 weren't run (System.Drawing is Windows-only).
- **`sursa/` also has:** `rezultate_APD.txt` (raw measurement output), `observatii.json`, and `imagini-test/`
  (the Source/FinalImages from running the Lab 2 code on Windows on 16 Oct: `a…h.bmp` for Ex 1–4, 10 images
  each of 100x100 / 500x500 / 2000x2000 for Ex 5, from before the 40/40/8 change).
- **Status:** PDF done on 30 Oct 2026. Upload to Moodle not confirmed in chat.
- **Materials:** `materiale/Lucrarea 2 APD.pdf` (Lab 2 handout). Still missing: the Lucrarea 3 handout and the
  Moodle screenshot (never saved on the Mac).
