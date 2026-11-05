# CAF – Lucrarea 3 (parametric reliability indicators)

- **Task:** `desfasurarea lucrarii 3.pdf`: 24 photodiode failure times (exhaustive test). I. identify the time-to-failure
  law with exponential, Weibull and normal probability papers; II. compute the law's parameters; fill the table
  (risk 0.01 / 0.2 / 0.5 / 0.995 × the 3 laws, accepted or not, K-S test); answer the 4 questions. Asked to solve it
  like lab 2 (Excel workbook).
- **Deliverable:** `caf/Lucrarea 3/CAF L3 rezolvare.xlsx`, sheets `Aplicatie` (data, F of each law, K-S, parameters,
  the table, conclusion, 3 probability-paper charts) and `Intrebari` (the 4 answers). Not uploaded yet.
- **How it was solved:** the lab's DOS app (`sursa/caf_L3_aplicatie.zip`, EMI.EXE, Turbo Pascal, runs in DOSBox) was
  not run. Its method was rebuilt instead: maximum-likelihood estimators (as its messages say) and the K-S test with
  the critical values from its `RISC.DTA` (Koziol-Byar table; for a complete sample the column is the Kolmogorov
  quantile x(p)). Accept if √n·Dmax ≤ x(p), with Dmax = max |i/n − F(ti)| (only at the failure points, like the app).
- **Results:** λ = 0.001821 1/h; Weibull β = 2.974, α = 1.953e8 (η = 613.7 h); normal μ = 549 h, σ = 198.6 h (MLE,
  divided by n). √n·Dmax: exp 1.591, Weibull 0.437, normal 0.423. Exponential rejected at 0.01 / 0.2 / 0.5, accepted at
  0.995; Weibull and normal accepted at all; normal adopted (smallest gap).
- **Checked against the app (5 Nov 2026):** I ran it; at 0.995 the exponential is accepted ("se încadrează fix la
  fix"). The first version used the two-sided supremum (1.795) and said "respinsă"; switched to |i/n − F(ti)|, which
  only changes that cell. Weibull at 0.01 is still close (0.437 vs 0.441).
- **Sources:** `sursa/genereaza_l3.py` builds the workbook (formulas, no cached values, like lab 2; β is a fixed
  value checked by the likelihood-equation cell). `sursa/grafice_excel.png` = the charts as rendered by Excel.
  Note: Excel's PDF export on this Mac drops the scatter markers and adds an "Oracle Restricted" header; in Excel itself
  the charts are fine.
- **Materials:** `materiale/` = copies of the files in `caf/Lucrarea 3/` (they were committed there earlier).
