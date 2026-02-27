# Status: Art of Gig

## Project
- **Title:** Art of Gig
- **Source:** Art of Gig Substack (retired)
- **Type:** Newsletter essays → 3-volume book series
- **Status:** in-progress (Vol 3 manuscript pipeline active)

## Editions

### Vol. 1: Foundations
| Format | Status | Notes |
|--------|--------|-------|
| Site   | existing | Marketing page at artofgig.com |
| Ebook  | existing | Kindle on Amazon; .epub in vol1/ (gitignored) |
| Print  | existing | Paperback on Amazon |

### Vol. 2: Superstructures
| Format | Status | Notes |
|--------|--------|-------|
| Site   | existing | Marketing page at artofgig.com |
| Ebook  | existing | Kindle on Amazon; .epub in vol2/ (gitignored) |
| Print  | existing | Paperback on Amazon |

### Vol. 3: The Yakverse Chronicles
| Format | Status | Notes |
|--------|--------|-------|
| Site   | done | Full text at artofgig.com (13 stories in docs/) |
| Ebook  | in-progress | .docx generated; next: Vellum import |
| Print  | in-progress | .docx generated; next: Vellum import |

## Folder layout
- `vol1/` — gitignored; Vol 1 EPUBs, PSD, rough cuts
- `vol2/` — gitignored; Vol 2 EPUBs, PSD, rough cuts
- `vol3/` — tracked; `generate_docx.py` for manuscript generation
- `book/` — gitignored; legacy rough cuts (Yakverse Rough Cuts still here)
- `docs/` — tracked; GitHub Pages site (artofgig.com)

## Notes
- artofgig.com is a static site (hosted via GitHub Pages, CNAME in docs/)
- Git repo tracks: docs/, vol3/, CLAUDE.md, status.md only
- Large binaries (vol1/, vol2/, book/, images/) are gitignored
- Substack export in artofgig-export-2021-05-12-ynbimvor8y/ (gitignored)
- Build docs: `git add docs/ && git commit && git push`
- Build manuscript: `python3 vol3/generate_docx.py`

## Instructions for Agents
After each work session, update this file:
1. Change the **Status** field to reflect current state (e.g., `legacy`, `in-progress`, `blocked`, `done`)
2. Update the Editions table for the relevant edition
3. Add dated notes at the bottom describing what was done

## Session notes

### 2026-02-27
- Reorganized repo: created vol1/, vol2/, vol3/ directories
- Moved EPUBs, PSDs, rough cuts from book/ into vol1/ and vol2/
- Updated .gitignore to exclude all binary/archive directories
- Created CLAUDE.md at project root and vol3/CLAUDE.md
- Created vol3/generate_docx.py — reads docs/*.html, outputs .docx to Publishing/manuscripts/artofgig/
  - First successful run: artofgig_vol3_20260227.docx (1.8MB), 15 images exported
- Website upgrade (docs/):
  - Added OG + Twitter Card meta tags to all 13 chapter pages + index.html
  - Fixed <title> tags to "The Yakverse Chronicles | Chapter Name" format
  - Added keyboard left/right arrow navigation to all chapter pages
  - Updated footer text on all chapter pages
  - Added ≤600px mobile breakpoint to style.css
