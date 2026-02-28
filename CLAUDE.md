# CLAUDE.md — Art of Gig

## Project overview

**Art of Gig** is a three-volume book series on the independent consulting life by Venkatesh Rao.
The live website is at [artofgig.com](https://artofgig.com), hosted via GitHub Pages.

Only `docs/`, `vol3/`, and project-level config files are tracked in git.
Large binaries (EPUBs, PSDs, MOBIs, PDFs) are gitignored.

---

## Volumes

### Vol 1: Foundations
- **Status:** Published (Kindle + paperback on Amazon)
- **Folder:** `vol1/` — gitignored; contains `ArtOfGig1.epub`, `vol1.psd`, `rough_cuts/`
- **Site:** artofgig.com (marketing page in `docs/index.html`)

### Vol 2: Superstructures
- **Status:** Published (Kindle + paperback on Amazon)
- **Folder:** `vol2/` — gitignored; contains `ArtPfGig2.epub`, `vol2.psd`, `rough_cuts/`
- **Site:** artofgig.com (marketing page in `docs/index.html`)

### Vol 3: The Yakverse Chronicles
- **Status:** Online only — full text live at artofgig.com
- **Folder:** `vol3/` — tracked (scripts only); outputs go to `Publishing/manuscripts/artofgig/`
- **Site:** 13 story chapters in `docs/*.html`
- **Build:** `python3 vol3/generate_docx.py` → `Publishing/manuscripts/artofgig/artofgig_vol3_YYYYMMDD.docx`

---

## Folder layout

```
artofgig/
├── .gitignore          ← ignores vol1/, vol2/, book/, archives, binaries
├── CLAUDE.md           ← this file
├── README.md
├── CNAME
├── status.md
│
├── vol1/               ← GITIGNORED — Vol 1 EPUBs, PSD, rough cuts
├── vol2/               ← GITIGNORED — Vol 2 EPUBs, PSD, rough cuts
├── vol3/               ← TRACKED — scripts for Vol 3 manuscript generation
│   ├── CLAUDE.md
│   ├── generate_docx.py
│   └── update_nav.py   ← updates book-nav in all 13 chapter HTML files
│
├── book/               ← GITIGNORED — legacy; Yakverse Rough Cuts still here
│
└── docs/               ← TRACKED — GitHub Pages site source
    ├── index.html      (3-box card grid: Vol 1/2/3)
    ├── style.css       (site styles + book-nav overrides)
    ├── book-nav.css    (synced from online_book_builder/)
    ├── book-nav.js     (synced from online_book_builder/)
    ├── vol3_cover.html (Vol 3 front matter)
    ├── vol3_title.html (Vol 3 front matter)
    ├── toc.html        (Vol 3 table of contents)
    ├── *.html          (13 Yakverse chapter pages, all with book-nav)
    └── images/         (chapter illustrations)
```

---

## Website

The live site is `docs/`. Deploy by committing and pushing:

```bash
git add docs/ && git commit -m "Update artofgig site" && git push
```

GitHub Pages serves from `docs/` on the `main` branch. CNAME points to artofgig.com.

---

## Manuscript pipeline (Vol 3)

```bash
python3 vol3/generate_docx.py
```

Reads all 13 chapter HTML files from `docs/`, strips web chrome, outputs clean `.docx`
to `../manuscripts/artofgig/artofgig_vol3_YYYYMMDD.docx`.
Images exported to `../manuscripts/artofgig/images/`.
Intended for import into Vellum for ebook/print production.

---

## Constraints

- `docs/style.css` is hand-edited — never auto-overwrite
- `docs/images/` is chapter illustration source — do not modify
- `book/` and `vol1/`, `vol2/` contain large binaries — gitignored, never commit
- Python 3.9 compatibility in all scripts (no backslashes in f-string expressions)

## Nav update workflow

To update nav on all 13 chapters (e.g. after changing sequence or labels):
```bash
python3 vol3/update_nav.py
```
Idempotent — safe to run multiple times.

To sync nav CSS/JS from the shared library:
```bash
python3 /Users/Venkat/Dropbox/Code/Publishing/online_book_builder/sync.py docs/
```

## Next session priorities

1. **Vellum import** — open `artofgig_vol3_YYYYMMDD.docx` in Vellum, check style
   mapping (BodyText, ChapterMeta, ChapterImage), adjust as needed for ebook/print layout.

## After each work session

Update `status.md` to reflect current state.
