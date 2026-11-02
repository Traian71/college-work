# APD – Lucrarea 1 (threads in C#)

- **Task:** solve exercises 1–8 from the Lucrarea 1 lab sheet, simply, using the examples from the text,
  so they can be pasted into Visual Studio (2019 at college).
- **Done:** 2 Oct 2026. Deliverable: `apd/lucrarea-1/` (C# code).
- **What's there:** each exercise is its own class with a `Run()` method, and `Program.cs` asks which one to run
  (1–8). This was needed because separate `Main`s in one VS project gave a "duplicate Main" error.
  - Ex 1–2: create and start threads.
  - Ex 3–5: sum of an array, with one thread per element, two halves, then K partitions.
  - Ex 6: the last thread prints the sum.
  - Ex 7–8: arrays of child threads with `Join`.
- **Materials missing:** the original Lucrarea 1 PDF (send it again to archive it in `materiale/`).
