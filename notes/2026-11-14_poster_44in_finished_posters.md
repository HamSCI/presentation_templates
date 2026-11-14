# 2026-11-14: Converting finished posters to 44 × 36 in

**Request (N. A. Frissell):** convert his CEDAR 2026 HamSCI poster and Steve Cerwin's WWVB poster,
both built on the 48 × 36 in template, to AGU's 44 in limit for AGU 2026, and contribute the tool
here.

**What was added:** `poster/tools/poster_44in.py`, a third route between the two existing ones:

| Route | Result |
|---|---|
| Start from a `_44in` template, paste content | 44 × 36 in, full-size fonts, by hand |
| `poster_44in.py` (new) | 44 × 36 in; template geometry; column content at 0.915, title, bars and footer at full size |
| `scale_pptx.py` | 44 × 33 in; everything at 11/12 |

Content between the 0.59 in side margins is mapped linearly from 48 in to 44 in, which puts the
three template columns exactly where `make_44in_templates.py` puts them (0.59, 15.00, 29.41 in;
14.00 in wide). Pictures and groups scale about their centre; text boxes get the new edge and
width; fonts, indents and fixed spacing scale by the same factor, so no text re-wraps. A full-width
banner photo is cropped at the right (combined with any crop already on it); without one, the
title widens to the margins and keeps its font.

**Why fonts scale:** a first version kept every font and only narrowed the boxes. On Cerwin's poster
the title wrapped into the author bar and two columns overflowed. Scaling the content fonts by the
width factor is the only change that guarantees no re-wrap without hand work; `--keep-fonts` keeps
the first behavior for anyone who will re-flow by hand.

**Verification:** both posters rendered with LibreOffice at 3168 × 2592 pt (44 × 36 in) and checked
visually, panel by panel. Not yet opened in PowerPoint. A first version broke the slide XML when it
added the banner crop (fixed; the slide XML is now parsed after every build).

**Not included:** the poster-specific edits and the repair for a corrupt picture in Cerwin's file
stay in the AGU 2026 repository (`w2naf-academia/2026_agu_fall_meeting`, private).
