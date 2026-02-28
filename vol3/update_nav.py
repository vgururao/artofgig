#!/usr/bin/env python3
"""Update all 13 Yakverse Chronicles chapter HTML files to use book-nav.

For each chapter this script:
  1. Adds <link href="book-nav.css" rel="stylesheet"/> to <head>
  2. Inserts top <nav class="book-nav"> immediately after <body>
  3. Replaces <nav class="chapter-nav">...</nav> (or existing bottom book-nav)
     with a fresh bottom book-nav, anchored to </main>
  4. Removes the old inline keyboard-nav <script> block
  5. Adds float nav HTML + <script src="book-nav.js"></script> before </body>

Idempotent: safe to run multiple times.

Usage:
    python3 vol3/update_nav.py [--dry-run]
"""
import re
import sys
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"

# Ordered chapter sequence: (filename, prev_file, prev_label, next_file, next_label)
# None for prev/next = disabled edge
CHAPTERS = [
    ("prelude.html",                     "toc.html",                       "Table of Contents",          "the_shadow_s_journey.html",        "The Shadow\u2019s Journey"),
    ("the_shadow_s_journey.html",        "prelude.html",                   "Prelude",                    "always_be_strategizing.html",      "Always Be Strategizing"),
    ("always_be_strategizing.html",      "the_shadow_s_journey.html",      "The Shadow\u2019s Journey",  "making_it_interesting.html",       "Making it Interesting"),
    ("making_it_interesting.html",       "always_be_strategizing.html",    "Always Be Strategizing",     "the_two_shadows_of_the_hero.html", "The Two Shadows of the Hero"),
    ("the_two_shadows_of_the_hero.html", "making_it_interesting.html",     "Making it Interesting",      "maneuvers_vs_melees.html",         "Maneuvers vs. Melees"),
    ("maneuvers_vs_melees.html",         "the_two_shadows_of_the_hero.html","The Two Shadows of the Hero","the_twelve_eigenconversations.html","The Twelve Eigenconversations"),
    ("the_twelve_eigenconversations.html","maneuvers_vs_melees.html",      "Maneuvers vs. Melees",       "the_shtickbox_affair.html",        "The Shtickbox Affair"),
    ("the_shtickbox_affair.html",        "the_twelve_eigenconversations.html","The Twelve Eigenconversations","the_medium_is_the_client.html","The Medium is the Client"),
    ("the_medium_is_the_client.html",    "the_shtickbox_affair.html",      "The Shtickbox Affair",       "and_so_it_begins.html",            "And So it Begins"),
    ("and_so_it_begins.html",            "the_medium_is_the_client.html",  "The Medium is the Client",   "staying_with_the_questions.html",  "Staying With the Questions"),
    ("staying_with_the_questions.html",  "and_so_it_begins.html",          "And So it Begins",           "infinity_gig.html",                "Infinity Gig"),
    ("infinity_gig.html",                "staying_with_the_questions.html","Staying With the Questions", "endgame.html",                     "Endgame"),
    ("endgame.html",                     "infinity_gig.html",              "Infinity Gig",               None,                               None),
]

TOC_FILE = "toc.html"


def make_inline_nav(prev_file, prev_label, next_file, next_label):
    """Return a single-line <nav class="book-nav"> string."""
    if prev_file:
        left = (
            '<a class="nav-link nav-prev" href="{f}">'
            '<span class="nav-arrow">&larr;</span>'
            '<span class="nav-label">{l}</span>'
            '</a>'
        ).format(f=prev_file, l=prev_label)
    else:
        left = ('<span class="nav-link nav-prev disabled">'
                '<span class="nav-arrow">&larr;</span>'
                '<span class="nav-label">\u2014</span>'
                '</span>')

    center = '<a class="nav-link nav-toc" href="{f}">Table of Contents</a>'.format(f=TOC_FILE)

    if next_file:
        right = (
            '<a class="nav-link nav-next" href="{f}">'
            '<span class="nav-label">{l}</span>'
            '<span class="nav-arrow">&rarr;</span>'
            '</a>'
        ).format(f=next_file, l=next_label)
    else:
        right = ('<span class="nav-link nav-next disabled">'
                 '<span class="nav-label">\u2014</span>'
                 '<span class="nav-arrow">&rarr;</span>'
                 '</span>')

    return (
        '<nav class="book-nav">'
        '<div class="nav-left">{left}</div>'
        '<div class="nav-center">{center}</div>'
        '<div class="nav-right">{right}</div>'
        '</nav>'
    ).format(left=left, center=center, right=right)


def make_float_nav(prev_file, next_file):
    """Return float nav HTML block."""
    if prev_file:
        float_prev = (
            '<a class="float-nav float-nav-prev" href="{f}" title="Previous chapter">'
            '<span class="float-nav-chevron">&lsaquo;</span>'
            '<span class="float-nav-label">Prev</span>'
            '</a>'
        ).format(f=prev_file)
    else:
        float_prev = ('<span class="float-nav float-nav-prev disabled">'
                      '<span class="float-nav-chevron">&lsaquo;</span>'
                      '<span class="float-nav-label">Prev</span>'
                      '</span>')

    toc_btn = (
        '<a class="float-nav-btn float-nav-toc" href="{f}" title="Table of Contents">'
        '<span class="float-nav-chevron">&and;</span>'
        '<span class="float-nav-label">ToC</span>'
        '</a>'
    ).format(f=TOC_FILE)

    if next_file:
        next_btn = (
            '<a class="float-nav-btn float-nav-next" href="{f}" title="Next chapter">'
            '<span class="float-nav-chevron">&rsaquo;</span>'
            '<span class="float-nav-label">Next</span>'
            '</a>'
        ).format(f=next_file)
    else:
        next_btn = ('<span class="float-nav-btn float-nav-next disabled">'
                    '<span class="float-nav-chevron">&rsaquo;</span>'
                    '<span class="float-nav-label">Next</span>'
                    '</span>')

    return (
        '{prev}\n'
        '<div class="float-nav-right">{toc}{nxt}</div>\n'
        '<script src="book-nav.js"></script>'
    ).format(prev=float_prev, toc=toc_btn, nxt=next_btn)


def update_chapter(html, prev_file, prev_label, next_file, next_label):
    """Apply all nav transformations to a chapter HTML string. Idempotent."""
    nav = make_inline_nav(prev_file, prev_label, next_file, next_label)

    # 1. Add book-nav.css link (skip if already present)
    css_link = '<link href="book-nav.css" rel="stylesheet"/>'
    if css_link not in html:
        html = html.replace(
            '<link href="style.css" rel="stylesheet"/>',
            '<link href="style.css" rel="stylesheet"/>\n' + css_link,
        )

    # 2. Bottom book-nav (BEFORE inserting top nav to avoid regex confusion).
    #    Split on the LAST </main>; work only on the tail of before_main.
    parts = html.rsplit('</main>', 1)
    if len(parts) == 2:
        before_main, after_main = parts
        # Search only the last 2000 chars — the nav is always near the end.
        SEARCH_LEN = 2000
        tail = before_main[-SEARCH_LEN:]
        head = before_main[:-SEARCH_LEN]
        # Remove existing nav (chapter-nav or book-nav) at the tail end.
        tail = re.sub(
            r'\n?<nav class="(?:chapter-nav|book-nav)">.*?</nav>\s*$',
            '',
            tail,
            flags=re.DOTALL,
        )
        before_main = head + tail.rstrip('\n') + '\n' + nav + '\n'
        html = before_main + '</main>' + after_main

    # 3. Remove old inline keyboard-nav <script> block
    html = re.sub(
        r'\n?<script>\s*\(function\(\)\s*\{.*?location\.href.*?\}\)\(\);\s*</script>',
        '',
        html,
        flags=re.DOTALL,
    )

    # 4. Top book-nav: remove existing (if any) then insert right after <body>.
    #    The removal pattern anchors to <body>, so it can't stray into content.
    html = re.sub(
        r'(<body>)\n<nav class="book-nav">.*?</nav>',
        r'\1',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = html.replace('<body>', '<body>\n' + nav, 1)

    # 5. Float nav: replace existing block (or insert) before </body>.
    #    Use string search to avoid regex newline accumulation on re-runs.
    float_block = make_float_nav(prev_file, next_file)
    FLOAT_MARKER = 'class="float-nav float-nav-prev'
    body_end = html.rfind('</body>')
    if FLOAT_MARKER in html:
        # Find the opening < of the float-nav-prev element and replace to </body>
        marker_pos = html.index(FLOAT_MARKER)
        elem_start = html.rfind('<', 0, marker_pos)
        html = html[:elem_start].rstrip('\n') + '\n' + float_block + '\n' + html[body_end:]
    else:
        html = html[:body_end].rstrip('\n') + '\n' + float_block + '\n</body>' + html[body_end + len('</body>'):]

    return html


def main():
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        print("DRY RUN — no files will be written\n")

    for fname, prev_file, prev_label, next_file, next_label in CHAPTERS:
        path = DOCS / fname
        if not path.exists():
            print(f"  SKIP (not found): {fname}")
            continue
        original = path.read_text(encoding='utf-8')
        updated = update_chapter(original, prev_file, prev_label, next_file, next_label)
        if updated == original:
            print(f"  unchanged: {fname}")
        elif dry_run:
            print(f"  would update: {fname}")
        else:
            path.write_text(updated, encoding='utf-8')
            print(f"  updated: {fname}")

    print("\nDone.")


if __name__ == '__main__':
    main()
