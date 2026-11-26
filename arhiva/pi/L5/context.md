# PI – Lab 5 (Operații de vecinătate – filtre adaptive)

- **Task:** ex. 6.1 „Filtrarea de netezire direcțională adaptivă”: write the filter function (means on the
  4 directions 0°/45°/90°/135°, pick the one closest to the central pixel) and the function that walks the image;
  lena.png → grayscale → additive Gaussian noise → MSE; scipy averaging filter → MSE; adaptive filter → MSE.
  Started from the template in the lab HTML (the .ipynb in the folder is an older version with different exercises).
- **Deliverable:** `pi/L5/ex6.1.py` (template filled in as is, Gaussian noise σ=20, 5×5 window).
- **Result (one run):** MSE with noise ≈ 400, averaging ≈ 94, adaptive ≈ 147.
- **Materials:** the lab .ipynb/.html, lena images and the bilateral flowchart, kept in `pi/L5/`.
- **Ex. 6.2** „Adaptare prin comutare”: average filter applied only when |pixel − 5×5 mean| < T, otherwise the
  pixel stays. Deliverable `pi/L5/ex6.2.py`, T = 60 (≈3σ of the noise; T=20 → MSE ≈ 340, T=30 → 254, T=60 → 103,
  T=100 → 94, i.e. it tends to plain averaging).
- Style: matched to the solved Lab 4 notebook (`pi/L_4_archive`), on Traian's request.
- **Ex. 6.3** „Filtrul LLMMSE” (Lee): alpha = 1 − σn²/σ²(local), set to 0 when negative, result
  alpha·f + (1−alpha)·mean, 7×7 window, σn = 20. Deliverable `pi/L5/ex6.3.py`. MSE: noise ≈ 400,
  7×7 averaging ≈ 136, Lee ≈ 80.
- **Status:** 6.1, 6.2, 6.3 done 26 Nov 2026.
