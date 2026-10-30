# Rules for college assignments

These are homework tasks I hand in myself. Every deliverable has to look like something a student
wrote in about an hour.

- **Do exactly what the task asks, nothing more.** If it says "pseudocode and flowchart", give
  pseudocode and a flowchart. No complexity analysis, correctness proofs, test tables, traces,
  code implementations or extra diagrams unless the task asks for them.
- **Max 2 pages** unless the task or I say otherwise.
- **No extra files.** A task folder holds only the deliverable (PDF, PNG, code), no Markdown/README, nothing
  else: no scripts, tests, image exports or zips.
- **Plain student style.** Short explanations, simple formatting. No table of contents, no
  specification tables, no "documentation" structure.
- **Ask before adding anything extra.** One line, before building it, not after.
- Write in the task's language (usually Romanian, with diacritics).
- One folder per subject, named after it (e.g. `inginerie-software/`), one subfolder per task.

## Two chats

- **Cloud chat (from my iPhone)** is the main one. I send it the tasks and files. It solves them, pushes to
  `main` and sends me the deliverables in the chat, ready to upload.
- It can't reach my Mac. When a step has to run on the Mac (an IDE, real measurements, local apps), it does
  everything else first. Then it ends with one ready-to-paste message for the Mac chat: the context, the repo
  path, the exact steps, what to push and what to give back. It does this only when it's needed.
- **Mac chat (Claude Code running locally on the Mac)** only takes over those handoffs. It runs the steps,
  pushes to `main` and copies the deliverable to my Desktop.
- Mac: the repo is at `~/Desktop/college-work`. `dotnet` may not be on PATH (Rider's SDK). Use Chrome for PDFs.
