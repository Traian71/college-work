# Inginerie Software – Lab 3 (Borland Together Architect)

- **Task:** the handout is `inginerie-software/LAB3/ISLaborator3.PDF` (titled "Laborator 5. Borland Together
  Architect"). Install Together Architect 2006, go through its GettingStarted tutorial, then build a project like
  the tutorial's Library example (`LibraryNumePrenume`): use case diagram, class diagram, and so on.
  `Alocare_exercitii_lucrarea3_IS.xlsx` says which exercise/theme each student got. Due date not recorded.
- **Files (still in `inginerie-software/LAB3/`, not yet sorted into deliverable vs `materiale/`):**
  - `diagrame-tema20.puml` / `.png`: Tema 20 – Sistem pentru administrarea unei fabrici, made with PlantUML on
    30 Oct 2026: use case, class, sequence and collaboration diagrams (Mutare mașină pe altă linie).
  - `ISLaborator3.PDF`, `Alocare_exercitii_lucrarea3_IS.xlsx`: materials received for the lab.
- **Not in git (over GitHub's 100 MB limit, left out on 2 Nov 2026 by my decision):** the two installers that came
  with the lab files. They're only on the Mac, in `inginerie-software/LAB3/` (ignored in `.gitignore`):
  - `Borland Together Archtect 2006.zip`: 382,004,321 bytes, 23 files, runs
    `WINDOWS\TEC_ARCHITECT_2006_WINDOWS.exe`. SHA-256 `c710ed50ec2c5a145ac1573c097d62705249ad4a425e206a2e1d37289db5fdfc`.
  - `jdk-8u73-windows-i586.exe`: Java 8u73 for 32-bit Windows, 190,314,072 bytes (Oracle Java archive).
    SHA-256 `c98792ea96512b03238a60616a5cefe936832718d6453fff2a545615fbdf0d87`.
  If they're lost, get them again from the teacher / Moodle (Together) and the Oracle Java archive (JDK 8u73).
- **How it was decided (Mac chat, 30 Oct 2026):**
  - The allocation sheet gives FILE-MITIŢĂ Traian (441A) number **20**. The lab sheet itself only has 5.1 (read
    the tutorial) and 5.2 (Library-like project), so 20 was taken to mean **Tema 20 from the lab 2 list** (factory
    administration, same model as the lab 2 class diagram). This was an assumption, not confirmed by the teacher.
  - Project name used: `FabricaFileMititaTraian` (following the `LibraryNumePrenume` rule).
  - Together can't run on the Mac: the zip also has `MACOSX/TEC_ARCHITECT_2006_MAC_OSX.ZIP`, but its launcher is a
    PowerPC binary needing Apple Java 1.3+, dead on Apple Silicon. Options considered: Visual Paradigm CE (native,
    can sync sequence → communication), or Windows 11 ARM in UTM to run the Windows installer. I didn't want
    installs, so the diagrams were written in **PlantUML** instead (paste each `@startuml` block into
    plantuml.com/plantuml to edit/re-export). The four renders were stitched into one PNG with headless Chrome.
  - Moodle accepted image files only, so the hand-in is `diagrame-tema20.png`.
- **Status:** PNG ready on 30 Oct 2026 for upload; whether it was uploaded isn't recorded.
