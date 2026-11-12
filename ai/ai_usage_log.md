# AI Usage Log: HamSCI Presentation Templates

This log records every substantive AI-assisted session on the project "HamSCI Presentation Templates".

Required by the HamSCI Generative AI Use Agreement, and by any institutional or funder policy
that applies to this project (see `.claude/rules/ai-governance.md`).

**This log is the source of truth for what AI did on this project.** A disclosure paragraph in a
manuscript, poster, or software release summarizes this log truthfully. Keep it current: an
entry written from memory weeks later is not a record.

## Entry format

```
## [YYYY-MM-DD HH:MM TZ]
- **Tool**: Claude (Anthropic), <exact-model-id>
- **Session Purpose**: What the session set out to accomplish
- **Sections/Files Affected**: Specific files, sections, or documents touched
- **Nature of Contribution**: Draft / Edit / Analysis / Code generation / Research / Scaffolding
- **Human Review Status**: Reviewed and verified / Partially reviewed / Pending review
- **Git Hash**: <filled in after committing>
```

The date and time come from the system clock via `date`, never from an estimate. The `/commit`
command produces this format and appends it in the right order.

---

<!-- Append new entries below this line, newest at the bottom. -->

## [2026-10-12 13:04 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5
- **Session Purpose**: Create HamSCI/presentation_templates from the HamSCI ai_project_template
  and add the HamSCI oral presentation template: the original PowerPoint file, the LaTeX Beamer
  theme developed for hamsci-petram talks, a worked example talk, and usage instructions with a
  style guide. Poster templates to follow.
- **Sections/Files Affected**: CLAUDE.md, README.md, CITATION.cff, .claude/template.json,
  .claude/rules/ai-governance.md (Tier 2 Scranton; no funder tier), .claude/rules/python-code.md
  (removed), ai/ai_usage_log.md; oral/README.md, oral/pptx/hamsci_oral_template.pptx,
  oral/beamer/ (beamerthemeHamSCI.sty with new \hamscitakeaway, \hamscisource,
  \hamscisectionframe; hamsci_banner.png, hamsci_logos.png), oral/example/ (hamsci_example_talk
  .tex/.pdf, latexmkrc, make_preview.sh, preview.png)
- **Nature of Contribution**: Scaffolding, code generation (LaTeX theme and example), documentation drafting
- **Human Review Status**: Pending review
- **Git Hash**: fe93708 (PR HamSCI/presentation_templates#1)

## [2026-11-05 21:18 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5
- **Session Purpose**: Add the HamSCI and University of Scranton PowerPoint poster templates
  supplied by N. A. Frissell, after finding why each was ~70 MB and cutting them to ~5 MB
  without visible loss of quality.
- **Sections/Files Affected**: poster/pptx/hamsci_poster_template.pptx and
  poster/pptx/hamsci_scranton_poster_template.pptx (banner image re-encoded; nothing else
  changed), poster/tools/shrink_pptx.py (new), poster/README.md (new), poster/preview.png (new,
  rendered with LibreOffice), notes/2026-11-05_poster_templates.md (new), README.md, CLAUDE.md
- **Nature of Contribution**: Analysis (file-size diagnosis, image-quality comparison), code
  generation (shrink script), documentation drafting
- **Human Review Status**: Pending review (shrunk files verified in LibreOffice only; needs a
  check in PowerPoint)
- **Git Hash**: ca90bee (PR HamSCI/presentation_templates#2)

## [2026-11-12 15:43 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5
- **Session Purpose**: Add AGU-compliant 44 in wide versions of the HamSCI and Scranton poster
  templates (AGU26 limits posters to 44 in wide), keeping the 48 × 36 in originals. A first
  attempt shrank the whole design evenly to 44 × 33 in; N. A. Frissell chose a 44 × 36 in layout instead,
  with the same height and font sizes and narrower columns.
- **Sections/Files Affected**: poster/pptx/hamsci_poster_template_44in.pptx and
  poster/pptx/hamsci_scranton_poster_template_44in.pptx (new, generated),
  poster/tools/make_44in_templates.py (new), poster/tools/scale_pptx.py (new; evenly shrinks a
  finished poster to a new width), poster/README.md, README.md, CLAUDE.md,
  notes/2026-11-07_agu_44in_posters.md (new)
- **Nature of Contribution**: Code generation (layout and scaling scripts), layout design,
  documentation drafting
- **Human Review Status**: Pending review (checked in LibreOffice only; needs a check in
  PowerPoint; AGU26 height limit not confirmed, agu.org refused automated fetch)
- **Git Hash**: <filled in after committing>
