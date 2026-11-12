# HamSCI Presentation Templates

## Project Overview
Presentation templates shared across HamSCI projects. The first is the oral presentation
template: the original 16:9 PowerPoint file and a LaTeX Beamer theme that reproduces it, with a
worked example talk and instructions. The poster template is a PowerPoint file in two sizes, 48 × 36 in and AGU-compliant
44 × 36 in, and two
versions, HamSCI blue for everyone and purple for University of Scranton authors. The audience is every HamSCI
member who gives a talk, from students to volunteers to faculty.

**Lead**: Nathaniel A. Frissell, W2NAF, University of Scranton
**Collaborators**: HamSCI community members who contribute templates
**HamSCI Working Group**: none
**Institution**: University of Scranton
**Funder**: none dedicated; shared HamSCI infrastructure (see `.claude/rules/ai-governance.md`)
**Project period**: ongoing, from October 2026

## Project Goal
Give HamSCI talks and posters a common, recognizable design that is easy to use in PowerPoint or
LaTeX, with the instructions and house style needed to use it well.

## Standing Rules

These two are binding on every HamSCI project and are imported here so they load into context
automatically:

@.claude/rules/ai-governance.md
@.claude/rules/hamsci-data.md

`.claude/rules/latex-writing.md` applies to `.tex`, `.bib`, `.cls`, and `.sty` files, through
its own `paths:` frontmatter. The only Python is the small standalone `poster/tools/shrink_pptx.py`
(Pillow only), so the template's `python-code.md` was not adopted.

## Repository Structure

```
presentation_templates/
├── CLAUDE.md                     ← this file; project instructions for Claude
├── README.md                     ← overview and license notes
├── LICENSE                       ← MIT, for the LaTeX and docs (not the images)
├── CITATION.cff
├── .claude/                      ← settings, /commit, /template-sync, rules
├── .github/ISSUE_TEMPLATE/
├── ai/ai_usage_log.md            ← mandatory AI session log
├── docs/GETTING_STARTED.md       ← onboarding for contributors new to Claude Code
└── oral/                         ← oral presentation template
    ├── README.md                 ← how to use it, theme commands, style guide
    ├── pptx/hamsci_oral_template.pptx
    ├── beamer/                   ← beamerthemeHamSCI.sty, hamsci_banner.png, hamsci_logos.png
    └── example/                  ← hamsci_example_talk.tex/.pdf, latexmkrc, make_preview.sh, preview.png
├── poster/                       ← poster template (PowerPoint only so far)
│   ├── README.md                 ← how to use it; keeping poster files small
│   ├── pptx/                     ← hamsci_[scranton_]poster_template.pptx (48 in) and _44in.pptx (AGU)
│   ├── tools/shrink_pptx.py      ← re-encodes oversized opaque PNGs as cropped JPEGs
│   ├── tools/make_44in_templates.py ← builds the 44 × 36 in AGU templates from the 48 in ones
│   ├── tools/scale_pptx.py       ← shrinks a finished poster evenly to a new width (48 → 44 × 33 in)
│   └── preview.png
└── notes/                        ← dated session notes
```

## Template Rules

- **The PowerPoint file is the reference design.** The Beamer theme reproduces it; a change to
  one is carried to the other, or an issue is opened for it.
- **Rebuild the example with every theme change**, in the same commit: run
  `oral/example/make_preview.sh`, which rebuilds the PDF and `preview.png`.
- **Keep the theme backward compatible.** HamSCI talks in other repositories use it. Rename or
  remove a command only with the lead's agreement, and record the change in the version string of
  `\ProvidesPackage`.
- **Images are not MIT-licensed.** The partner logos and the silhouette photograph are used with
  permission for HamSCI presentations; do not add images whose reuse terms are unknown.
- **Keep the PowerPoint files small.** Before committing a changed `.pptx`, check its size; if
  it has grown past ~10 MB, run `poster/tools/shrink_pptx.py` on it, check it in PowerPoint and
  regenerate `poster/preview.png`. The two poster versions differ only in accent color and
  Scranton affiliation; carry any other change to both. The `_44in` files are generated from
  the 48 in ones with `poster/tools/make_44in_templates.py`; edit the 48 in file and regenerate them.
- **Example content is placeholder text.** The placeholder callsigns (KC4AAA, KC4USV) come from
  the PowerPoint template; never attribute example work to a real operator.

## Working Conventions

**Session notes.** Keep one dated notes file per working session in `notes/`, named
`YYYY-MM-DD_<topic>.md`, recording what was decided, why, what it depends on, and what is still
open. Write them for a reader with no context, which in practice means a future Claude session
and a future you.

**Commit the curated, human-readable record.** Memos, notes, reports and other curated write-ups of the analysis are
committed as PDFs next to their source (LaTeX or Markdown), rebuilt in the same commit so the two
never disagree. They show what was concluded without anyone having to rebuild anything, and the
commit history becomes a readable record of what was done. Figures a memo or paper includes are
committed with that document. The rule is about curated documents, not bulk output: batches of
generated figures, per-event plot sets, galleries and image compilations stay out of git and are
regenerated by committed scripts. Also out: LaTeX intermediates (`.aux`, `.log`, `.bbl` and the
like), caches, scratch output, and raw data. A curated PDF over 50 MB needs a decision first.

**Commits.** Use the `/commit` command. It logs the AI session, then commits each changed repo
(submodules first) on a feature branch and opens a pull request. Prefix AI-assisted commits with
`[AI-assisted]`. Reference tracking issues (`refs #N`, or `closes #N` only when completion is
yours to declare).

**Every change goes through a pull request.** Branch from `origin/main`, commit on the branch,
push the branch, and open a PR with `gh pr create`. A human maintainer reviews and merges.
Claude never commits or pushes directly to `main` and never merges.

**Pushing a feature branch and opening its PR is standing permission** once the user has approved
the commit. Any other push needs explicit instruction. Never force-push or hard-reset. Fetch and
verify remote state before any push.

**Project boards and issue status are human-curated.** Read them freely; propose changes and
name the exact command rather than running it.

## Submodules (optional)

If the project includes submodules (an Overleaf manuscript, a separate code repository, a
hardware design repo), the commit and push order is fixed:

1. Commit **inside** the submodule, on its own feature branch
2. Push the submodule branch and open its PR
3. After that PR merges, commit the updated submodule pointer in this repo, on this repo's branch
4. Push this repo's branch and open or update its PR

Never point this repo at an unmerged submodule branch commit.

Never the reverse at either stage. A parent pushed ahead of its submodule looks correct on the
machine that did it and breaks for every clone, because the recorded pointer names a commit no
remote has. Verify before pushing a parent:

```bash
git -C <submodule> branch -r --contains HEAD   # empty output = local only; push the submodule first
```

Add submodules with:

```bash
git submodule add https://git.overleaf.com/<id> overleaf      # Overleaf manuscript
git submodule add git@github.com:HamSCI/<repo>.git <path>     # HamSCI code repo
```

The `/commit` workflow auto-detects submodules via `git submodule status`.

## Template Updates

This repository follows an `ai_project_template`; `.claude/template.json` records which one and
which of its commits was last adopted. A session-start hook (`.claude/hooks/template_check.sh`,
registered in `.claude/settings.json`) checks that template at most once a day and, if it has
moved on, says so at the start of the session. When it does, tell the user and offer
`/template-sync`, which applies the template's changes **as changes**, on a branch and through a
PR, without overwriting project-specific content. The check is read-only and silent when offline.

A workflow improvement made here that other projects would want belongs upstream too: propose it
to the template in the same session.

## AI Governance

Every substantive AI session is logged in `ai/ai_usage_log.md` **before** the work is committed.
Use `/commit`, which enforces the ordering. The full policy stack is in
`.claude/rules/ai-governance.md`, which is imported above.
