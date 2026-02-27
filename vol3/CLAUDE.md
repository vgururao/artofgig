# CLAUDE.md — vol3 (The Yakverse Chronicles)

## Purpose

Scripts for generating a print/ebook manuscript from the Vol 3 web content in `../docs/`.

## Files

| File | Role |
|------|------|
| `generate_docx.py` | Main generator: reads docs/*.html, outputs .docx to manuscripts/ |

## Build

```bash
python3 vol3/generate_docx.py
```

Run from the `artofgig/` root (or any directory — uses absolute paths).

## Output

- `Publishing/manuscripts/artofgig/artofgig_vol3_YYYYMMDD.docx` — main manuscript
- `Publishing/manuscripts/artofgig/images/` — exported chapter images

## Chapter order

13 chapters in reading order (hardcoded in `generate_docx.py`):
1. Prelude
2. The Shadow's Journey
3. Always Be Strategizing
4. Making it Interesting
5. The Two Shadows of the Hero
6. Maneuvers vs. Melees
7. The Twelve Eigenconversations
8. The Shtickbox Affair
9. The Medium is the Client
10. And So it Begins
11. Staying With the Questions
12. Infinity Gig
13. Endgame

## Named paragraph styles (Vellum-targetable)

- **BodyText** — all body paragraphs
- **ChapterMeta** — the "in which..." subtitle below each chapter title
- **ChapterImage** — paragraphs containing embedded images

## Constraints

- Python 3.9 compatible (no backslashes inside f-string expressions)
- Requires: `python-docx`, `beautifulsoup4`, `lxml`
