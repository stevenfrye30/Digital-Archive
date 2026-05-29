# v133 — Steven's developer handbook & learning roadmap

A beginner-friendly handbook that uses your **own** ecosystem
(Digital Archive / Atlas / Workspace / Glyphs / Daily-Reader) as the
teaching material. The goal: understand how these projects work, then
build a small parallel archive yourself — with AI as a **tutor and
reviewer**, not the builder.

This is documentation only. **No features, no redesign, no ingestion, no
restricted files, no `MUKTIKA_108` change, no public-count change, no app
behavior change.** It is consistent with the v132 project-wide audit
(`reports/v132_project_wide_stabilization_audit.md`) — read that first
for the formal map; read this for the plain-English learning path.

> How to use this: skim §1–§5 once to get the shape. Then live in §6
> (daily workflow) and §10 (the 4-week plan). §9 (Archive Lab) is the
> project you'll actually build to learn.

---

## 1. The big picture

You have **one ecosystem, three layers, plus two extra surfaces.** Think
of it like a building:

* **Workspace = the foyer / front door.** A public website that links to
  everything else. Local copy: `workspace-hub/`. Live at
  `stevenfrye30.github.io/Workspace/`.
* **Digital Archive = the library.** The big collection of texts and the
  "Reading Room" website that displays them. Local copy:
  `Digital-Archive/03_web_app/`. Live at
  `stevenfrye30.github.io/Digital-Archive/`. **This is your main
  teaching example.**
* **Atlas = the back office / operating system.** Rules, schemas, and a
  registry that organize the ecosystem. Mostly behind the scenes. Local:
  `Atlas/`; its small public site is `Atlas/_published/atlas_site/`
  (`stevenfrye30.github.io/Atlas/`).
* **Glyphs = one finished exhibit room.** A self-contained world about
  early writing systems. Local: `glyphs/`. Live at
  `stevenfrye30.github.io/Glyphs/`.
* **Daily-Reader = a little machine in the back.** A small **service**
  (not just a web page) that sends/prints a daily reading. Local:
  `Digital-Archive/04_landing/_deploy/`.

**How they relate:** Workspace is the entrance and links out to the
others. Atlas organizes and feeds Workspace through scripts. Digital
Archive holds the actual texts. Glyphs is a standalone world. Daily-Reader
pulls from the archive to produce a daily reading.

**Static sites vs. server behavior:**

* **Static sites** (just files a browser reads — HTML/CSS/JS/JSON):
  Workspace, Digital Archive, Glyphs, the Atlas published site. These run
  on GitHub Pages.
* **Server behavior:** Daily-Reader is a **Python service** (it has a
  `Procfile`) — it *runs code on a server*, so it is **not** a GitHub
  Pages static site. (Atlas's *engine* is Python too, but it runs locally
  on your machine, not on Pages.)

**Reference systems vs. active learning projects:**

* **Reference systems (stable — don't keep expanding now):** Digital
  Archive, Atlas, Workspace, Glyphs, Daily-Reader. Treat these as a
  finished, AI-assisted system you *study*.
* **Active learning project (what you build):** **Archive Lab** (§9) — a
  brand-new tiny archive you make from scratch.

---

## 2. Basic web concepts, using your project

* **A website** is a set of files a browser opens and displays. The
  Reading Room is a website.
* **A static site** is a website made of plain files (HTML/CSS/JS/JSON)
  with no server doing work — the browser does everything. The Digital
  Archive Reading Room is static: it's mostly one big `index.html` plus
  data files.
* **GitHub Pages** is a free service that takes the files in a GitHub
  repo and serves them as a website. It only serves files — **it does not
  run Python.** That's why all the heavy Python scripts run on *your*
  computer and only their *output* (data files) gets published.
* **localhost** means "this computer." When you run a local server, the
  site is at `http://localhost:8765/` — visible only to you, for testing
  before publishing.
* **A local server** is a small program that serves your files to your
  browser. `python -m http.server 8765` is one. You need it because some
  browser features (like fetching data files) don't work when you just
  double-click an HTML file.
* **HTML** is the *structure/content* of a page (headings, text,
  buttons). In the archive, `index.html` defines the Reading Room.
* **CSS** is the *styling* (colors, fonts, layout). In the archive, the
  CSS lives inside `<style>` blocks in `index.html`.
* **JavaScript (JS)** is the *behavior* (clicks, loading data, building
  the page on the fly). In the archive, JS builds the 108 Map, opens a
  text when you click, etc.
* **JSON** is a *data format* — structured text the JS reads. The
  archive's texts are stored as JSON (compressed as `.json.gz`).
* **Python scripts** are *tools that run on your computer* to prepare data
  (clean texts, build the search index, gzip data, check safety). Their
  output is what gets published; the scripts themselves don't run online.
* **Git** is a *time machine + save system* for your files. It records
  snapshots ("commits") so you can see history and undo.
* **GitHub** is a website that *stores your Git repos online* and (via
  Pages) can publish them.
* **A repo (repository)** is one project tracked by Git.
  `Digital-Archive/03_web_app/` is a repo.
* **A commit** is one saved snapshot with a message describing the change.
* **Pushing** means uploading your local commits to GitHub.
* **Deployment** means making the new version live. For your Pages sites,
  deployment = `git push` (Pages then serves the new files).

---

## 3. How the Digital Archive works (high level)

* **Folder structure (the parent `Digital-Archive/`):**
  * `01_library/` — the curated, canonical texts (source of truth).
  * `02_raw_sources/` — original raw files (~940 MB), kept for proof.
  * `03_web_app/` — **the published Reading Room** (this is the repo).
  * `04_landing/` — the Daily-Reader app.
  * `05_scripts/` — Python tools (cleanup, index, gzip, safety, restricted
    tooling under `local_only/`).
  * `06_workspace/` — scratch/working area.
* **`index.html`** — the whole Reading Room: structure (HTML), styling
  (CSS in `<style>`), and behavior (JS in `<script>`) all in one big file.
* **CSS** — inside `index.html`; controls the parchment look, the 108-Map
  chips, etc.
* **JavaScript** — inside `index.html`; loads data, renders text families,
  builds the Muktikā 108 Map, opens readers, handles search/filter.
* **Data folders** — `03_web_app/data/` holds the public texts as
  **gzipped JSON** (`*.json.gz`). The app downloads and unzips them in the
  browser. Some canonical lists (like `MUKTIKA_108`) are written directly
  inside `index.html`.
* **Public data JSON** — the only text that ships publicly. It is
  public-domain / cleanly-licensed material.
* **reports/** — markdown write-ups of each version (`vNNN_*.md`),
  including the Upanishads series and the v132 audit.
* **scripts/** — `05_scripts/` (one level up from the repo). The key
  safety tool is `check_no_restricted_text.py`.
* **Reading Room** — the public experience: browse by tradition, open a
  text, read with footnotes and source info.
* **Source-family pages** — some texts are grouped into a "family" (e.g.
  "The Upanishads") with multiple editions/translations and special views.
* **Upanishads architecture** — the worked example: a "Muktikā 108 Map"
  showing all 108 Upanishads as chips. **44 are active** (readable now),
  **64 are future** (identified source, not yet readable), **0 still
  needed**. This count is stable; don't change it casually.
* **Public vs. local restricted mode** — the public site shows only
  metadata for not-yet-public texts (never the copyrighted text). On your
  **own computer only**, with an explicit opt-in, you can read lawfully
  obtained restricted copies. This "local mode" is hard-blocked on the
  public site (`github.io`).
* **Why restricted text must never be committed** — committing
  copyrighted text would publish it to the open web (a legal/ethical
  problem). So restricted files live in a gitignored folder
  (`data/_restricted/`), and `check_no_restricted_text.py` blocks them
  from ever being committed. This is the single most important safety rule.

---

## 4. How Atlas works (high level)

* **Conceptual graph / relation map** — Atlas is the "operating system":
  it models how things in the ecosystem relate (a registry/graph), and it
  governs structure (schemas, naming, rules).
* **Governance vs. published site** — Atlas has two parts: (1) local
  engine + governance docs + registry (on your computer, in `Atlas/`),
  and (2) a small published site (`Atlas/_published/atlas_site/`).
* **Why Atlas should not disrupt Digital Archive** — the layers are
  intentionally independent. Atlas must not reach into the archive's data.
  Cross-layer connections are only allowed as **named, scripted, one-way,
  reversible** flows (e.g. a sync script copying a registry to Workspace).
* **What is deferred** — whether Atlas's local engine code eventually
  joins the published repo or stays local is an open question (see v132
  R5). Leave it deferred for now.
* **How Atlas might eventually connect safely** — through an explicit
  export step (Atlas produces a JSON file; Workspace/archive read it),
  never a live import. If a change ever needs to touch two repos at once,
  that's a signal the boundary is wrong — stop and reconsider.

---

## 5. How Workspace works (high level)

* **Public foyer / navigation hub** — `workspace-hub/` is the front door:
  a dashboard that links to the worlds (Pantheons, Sound Map, Phonos,
  Cosmos), the archive shelf, and out to Atlas, Digital Archive, Glyphs.
* **What it should link to** — finished, public-facing surfaces and a
  curated doorway into selected texts.
* **What it should not become** — it must **not** hold raw corpus data,
  parser/extraction code, heavy build tooling, or unstable experiments.
  Those belong in Digital Archive (data) or Atlas (engine). Keep the foyer
  small and stable.

---

## 6. Daily safe workflow (beginner checklist)

A repeatable loop for making a small, safe change to the Reading Room.

1. **Open the project** — open the folder
   `C:\Users\steve\Documents\Claude Workspace\Digital-Archive\03_web_app`
   in your editor.
2. **Run it locally:**
   ```
   cd "C:\Users\steve\Documents\Claude Workspace\Digital-Archive\03_web_app"
   python -m http.server 8765
   ```
   * `cd "..."` = "change directory" — move the terminal into the repo
     folder (quotes are needed because the path has spaces).
   * `python -m http.server 8765` = start a local web server on port
     8765, serving the files in this folder.
3. **Check the browser** — open `http://localhost:8765/` and use the
   feature you changed. Look for anything broken. (Refresh after edits.)
4. **See what you changed:**
   ```
   git status
   ```
   * Lists which files are new, modified, or staged. Your starting map
     before committing.
   ```
   git diff
   ```
   * Shows the exact line-by-line changes you made (the "before/after").
     Read it so you know precisely what you're about to commit.
5. **Run the safety check (required before any commit):**
   ```
   python ..\05_scripts\check_no_restricted_text.py
   ```
   * Scans the repo for restricted/copyrighted/local-only files. It must
     print **PASS**. If it fails, **do not commit** — find and remove the
     flagged file.
6. **Stage only the specific files you mean to commit:**
   ```
   git add index.html
   git add reports\my_report.md
   ```
   * `git add <file>` = mark a specific file to be included in the next
     commit. Name files explicitly.
7. **Commit (save a snapshot with a message):**
   ```
   git commit -m "short clear message about the change"
   ```
   * `-m "..."` = the message describing *why* the change exists.
8. **Push (publish):**
   ```
   git push origin main
   ```
   * Uploads your commit to GitHub's `main` branch. For a Pages site,
     this makes it live (after a short delay).
9. **Check GitHub Pages** — open the live URL
   (`https://stevenfrye30.github.io/Digital-Archive/`), wait ~1 minute,
   hard-refresh, and confirm your change appears.

**Why not `git add -A` in `03_web_app`?** `git add -A` stages
*everything*, including ~260 stray diagnostic files (screenshots, scratch
scripts) and — dangerously — any restricted file you forgot to delete.
You could publish things you never meant to. **Always stage explicit
files by name**, and let `check_no_restricted_text.py` be your backstop.

---

## 7. How to recover when something breaks

* **Read the error message slowly.** Errors usually name the file and a
  reason ("command not found", "file not found", a Python traceback's
  *last* line). Read the last line first.
* **`git status`** — your first move when confused. It shows what's
  changed/staged so you know where you are.
* **`git diff`** — shows exactly what you altered; often the bug is right
  there in the diff.
* **Undo an unstaged edit** (you changed a file but haven't committed):
  ```
  git checkout -- index.html      # discard changes to this file
  ```
  (or `git restore index.html` — same effect on newer Git).
* **Unstage a file you added but haven't committed:**
  ```
  git restore --staged index.html
  ```
* **Avoid panic-committing.** If something feels wrong, **stop**. Don't
  commit "to save it." Run `git status` and `git diff` first. A messy
  working folder is safe as long as you don't commit/push it.
* **What to paste when asking AI for help:** (1) the exact command you
  ran, (2) the **full** error text, (3) the output of `git status`, and
  (4) what you expected to happen. That's enough for a precise answer.

---

## 8. AI-use rules (tutor, not builder)

For your handmade learning project, AI is a **tutor and reviewer**:

**AI may:**
* Explain what existing code does, in plain language.
* Review code *you* wrote and point out issues.
* Suggest the next small step.
* Help you debug (by explaining the error and asking guiding questions).
* Write **tiny** example snippets (a few lines) to illustrate a concept.

**AI should not:**
* Directly write or rewrite large files in your handmade project
  (**Archive Lab**). That's your job — typing builds understanding.
* Generate the whole project for you.

**Your commitments:**
* **You type the code yourself** when learning.
* You can **explain every change** in your own words before committing.
* Before accepting an AI suggestion, **ask the AI to quiz you** or make
  you explain the file first ("ask me what this function does before you
  tell me").
* When stuck, ask for a *hint*, then a *bigger hint*, then the answer —
  in that order.

(The existing reference systems — Digital Archive, Atlas, etc. — are
different: there, AI may edit directly, because you're studying a finished
system, not learning by building it.)

---

## 9. Handmade parallel archive plan — "Archive Lab"

**Working name:** Archive Lab.
**Purpose:** a small archive you build yourself, from scratch, to
understand how the Digital Archive works.
**Where:** a brand-new folder *outside* the main archive (suggested:
`C:\Users\steve\Documents\Claude Workspace\projects\archive-lab\`). Do
**not** build it inside `Digital-Archive/` — keep your learning sandbox
separate so you can't break the real system.

**Rules:** AI advises/explains/quizzes/reviews; **you type the code**;
start tiny; **no copyrighted/restricted text** (use public-domain
excerpts or obvious placeholders); no complex architecture at first; no
Atlas graph at first; no automation at first.

**Staged versions:**

* **v0.1 — one-page archive.** `index.html` + `style.css`; one manually
  typed public-domain excerpt or placeholder; simple navigation links.
  *Goal: see HTML + CSS render in the browser.*
* **v0.2 — multiple pages.** A homepage, a "text list" page, and one
  reader page; links between them. *Goal: understand pages + relative
  links.*
* **v0.3 — data-driven archive.** A `texts.json` file; JavaScript reads
  it and renders the list of texts from data instead of hand-written
  HTML. *Goal: separate data from presentation (like the real archive).*
* **v0.4 — simple reader.** Click a text → show its title, source, and
  content; add simple Previous/Next. *Goal: events + showing the right
  data.*
* **v0.5 — GitHub Pages deployment.** Add a `README.md`, a clean repo
  structure, push to GitHub, enable Pages, and view it online. *Goal: the
  full local → GitHub → live loop.*
* **v0.6 — compare with the Digital Archive.** List what the real archive
  does that Archive Lab doesn't yet (search, families, gzip, footnotes,
  integrity, restricted mode). Pick **one** improvement and do only that.
  *Goal: learn to scope and resist over-building.*

---

## 10. Four-week learning roadmap

**Week 1 — HTML, CSS, files/folders, localhost, editing safely**
* Learn: how an HTML page is structured; basic CSS; folders/paths;
  running `python -m http.server` and opening `localhost`.
* Inspect: the top of `Digital-Archive/03_web_app/index.html` (the
  `<head>`, the `<style>` block, the first chunk of HTML).
* Exercises: build Archive Lab **v0.1**; change a heading and a color and
  see it update in the browser.
* By the end you can explain: what HTML vs. CSS do; what `localhost` and a
  local server are; why you test locally before publishing.

**Week 2 — JavaScript basics and DOM manipulation**
* Learn: variables, functions, arrays/objects; how JS finds and changes
  page elements (the DOM); click handlers.
* Inspect: a small JS function in `index.html` (e.g. one that builds a
  chip or opens a text) — just read and trace it.
* Exercises: build Archive Lab **v0.2**; add a button that shows/hides a
  paragraph with JavaScript.
* By the end you can explain: what JS adds beyond HTML/CSS; what "the DOM"
  is; how a click makes something happen.

**Week 3 — JSON data and rendering archive entries**
* Learn: JSON shape (objects, arrays, key/value); fetching/reading a JSON
  file; looping over data to build HTML.
* Inspect: how the real archive stores texts as data (the idea of
  `.json.gz`) and how `MUKTIKA_108` is a data array inside `index.html`.
* Exercises: build Archive Lab **v0.3** and **v0.4** (load `texts.json`,
  render a list, click to read).
* By the end you can explain: why data is separate from presentation; how
  JS turns a JSON list into a page; what your reader does on click.

**Week 4 — Git/GitHub/GitHub Pages and safe maintenance**
* Learn: `git status` / `diff` / `add` / `commit` / `push`; what a repo
  and a commit are; how Pages publishes; the safety check habit.
* Inspect: `git log --oneline` in `03_web_app` (read the vNNN history);
  the `.gitignore`; `check_no_restricted_text.py` (read what it blocks).
* Exercises: build Archive Lab **v0.5** (publish online); practice the §6
  loop end-to-end on Archive Lab (never on the real archive yet).
* By the end you can explain: the local → GitHub → live flow; why Pages
  doesn't run Python; why `git add -A` is risky; why restricted text must
  never be committed.

---

## 11. "Things I should be able to explain" checklist

Tick these off as you learn — they're the real test of understanding:

* What file controls the Digital Archive homepage? *(→ `index.html`)*
* Where does the Digital Archive load its text data from? *(→ gzipped
  JSON in `data/`, plus inlined arrays like `MUKTIKA_108` in
  `index.html`)*
* What is the difference between public mode and local restricted mode?
* Why does GitHub Pages **not** run Python? *(it only serves static
  files; Python runs on your computer to prepare data)*
* What does `git status` show? What does `git diff` show?
* Why is committing restricted files dangerous? *(it would publish
  copyrighted text to the open web)*
* What does JavaScript do in the reader? *(loads data, builds the page,
  handles clicks/search)*
* Why shouldn't I use `git add -A` in `03_web_app`?
* What is the public Muktikā count, and why shouldn't I change it
  casually? *(44 / 108)*
* Which projects are static sites, and which one is a server service?
  *(static: Workspace, Digital Archive, Glyphs, Atlas site; service:
  Daily-Reader)*

---

## 12. Recommended next step — v134

**v134: Create Archive Lab v0.1 as a *guided learning session*.** Instead
of generating the project, Claude acts as a tutor: it asks you to create
each file and type small pieces of code yourself, explains each concept as
you go, quizzes you on what you wrote, and only reviews/corrects after you
attempt it. Outcome: a one-page Archive Lab you built and can fully
explain — the first real step toward maintaining your own archive.

---

### Audit confirmations
* Changed in this pass: **documentation only** — this handbook + the
  Digital-Archive build-marker bump. No app behavior, no `MUKTIKA_108`,
  no public count (still 44 / 108), no restricted material.
* `check_no_restricted_text.py`: **PASS**; nothing under
  `data/_restricted/`, no `*.local.json`, no copyrighted text committed.
* Consistent with `reports/v132_project_wide_stabilization_audit.md`.
