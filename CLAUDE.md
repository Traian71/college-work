# Rules for college assignments

These are homework tasks I hand in myself. Every deliverable has to look like something a student
wrote in about an hour.

- **Do exactly what the task asks, nothing more.** If it says "pseudocode and flowchart", give
  pseudocode and a flowchart. No complexity analysis, correctness proofs, test tables, traces,
  code implementations or extra diagrams unless the task asks for them.
- **Max 2 pages** unless the task or I say otherwise.
- **Deliverable format is whatever the teacher asks for in that lab** (e.g. an Excel workbook if the
  lab says Excel). When the lab doesn't say, use a PDF.
- **No extra files.** A task folder holds only the deliverable (PDF, PNG, code), no Markdown/README, nothing
  else: no scripts, tests, image exports or zips. Everything else goes in `arhiva/` (see below).
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
- Mac: the repo is at `~/college/college-work` (the only clone, there's none on the Desktop). `dotnet` is at
  `~/.dotnet/dotnet`, not on PATH. Use Chrome for PDFs.

## Git is the backup: push everything

The container gets wiped, so whatever isn't pushed is lost. At the end of every task (and after every fix),
push everything to `main`, not just the deliverable.

- `arhiva/<materie>/<task>/` holds everything except the deliverable:
  - `context.md`: what the task asked (verbatim if possible), the due date, where the deliverable is and what was
    uploaded, the decisions and my requests along the way, and the status. Keep it short and update it when
    something changes.
  - `materiale/`: every file I sent for the task (lab PDFs, sheets, teacher code, screenshots of the task,
    recordings, zips), exactly as received. Save them here at the start of the task, before working.
  - `sursa/`: working files (generators, HTML/Markdown sources, measurement outputs, old versions).
- If I ask about an old task, read its `arhiva/.../context.md` first.
- The Mac chat does the same for anything it produces (e.g. measurement results).
- Only skip what can be recreated and isn't material: `.DS_Store`, Office lock files, virtual envs, `bin/`, `obj/`,
  `__pycache__` (all in `.gitignore`). Files over 100 MB can't go to GitHub: ask me, and note them in `context.md`.


## Moodle (curs.upb.ro/2026), Mac only

`instrumente/moodle.py` talks to Moodle through the mobile app API. The token is in the Mac's Keychain
(`moodle-upb-token`; the calendar feed URL is `moodle-upb-calendar`), never in the repo or in chat.

- `due` lists what's due or overdue and not submitted; `show <assignid>` the task text and accepted file types;
  `files <courseid> [--grep lab]` + `get <url> <file>` download handouts (save them to `arhiva/.../materiale/`);
  `submit <assignid> <file>` shows what it would upload, `--yes` actually submits.
- "Check my Moodle": run `due`, then for each item say what you can do alone and what needs me.
- **Never submit without my OK for that exact assignment and file**, even if I asked for "everything".
- A weekly scheduled task (`moodle-weekly-check`, Mondays 08:30) runs `due` and sends a macOS notification.
- Token expired: sign me in via UPB Login in the browser pane, then fetch
  `admin/tool/mobile/launch.php?service=moodle_mobile_app&passport=x&urlscheme=moodlemobile&confirmed=1` from the
  signed-in page and decode the `moodlemobile://token=` link (base64, token after `:::`).
