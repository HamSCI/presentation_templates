# 2026-11-05 to 2026-11-07: AGU-compliant 44 in poster templates

**Request (N. A. Frissell):** AGU is requiring posters no more than 44 in wide this year. Add 44 in
versions of the poster templates as the AGU-compliant option, and keep the 48 in originals.

**First attempt (2026-11-05), replaced:** shrinking the whole design evenly by 44/48 gave 44 × 33 in, with
every font at 11/12 size. N. A. Frissell chose a 44 × 36 in layout instead (2026-11-07). The even-shrink tool
was kept for converting finished posters (below).

**What was done**
- `poster/tools/make_44in_templates.py` builds `hamsci_poster_template_44in.pptx` and
  `hamsci_scranton_poster_template_44in.pptx` (44 × 36 in) from the 48 × 36 in files. Nothing
  vertical changes: font sizes, y positions and heights all match the 48 in version (checked in
  the XML). Horizontally:
  - the author bar and footer bar shrink to 44 in;
  - the banner photo is cropped 4 in (8.333 %) at the right, where it is plain sky, using
    `<a:srcRect r>`, so it is not squashed and the image pixels are untouched;
  - the title box loses 4 in from its right edge (keeps its left edge, clear of the silhouettes);
  - the conference-name box moves 4 in left;
  - the columns keep their margins and gaps and narrow from 15.33 in to 14.00 in;
  - the logo group (all five logos are in `Group 1`) stays centred on the slide;
  - layout and master placeholders are scaled horizontally by 44/48.
  The script finds shapes by name. Both templates use the same top-level shape names; only the
  names of the logos inside the group differ, and the script does not use those.
- `poster/tools/scale_pptx.py` evenly shrinks a finished poster to a new width (44 × 33 in from 48 × 36 in),
  for people who have already built a poster on the 48 in template.
- Docs: poster/README.md, README.md, CLAUDE.md.

**AGU height limit not checked:** agu.org refused automated fetches (HTTP 403).

**Verification:** rendered with LibreOffice: both PDFs are 3168 × 2592 pt (44 × 36 in); visually
checked the banner, columns and footer for both versions. Not yet opened in PowerPoint.

**Open:** check the 44 in files in PowerPoint; confirm AGU26's height limit. `poster/preview.png`
still shows the 48 in versions.
