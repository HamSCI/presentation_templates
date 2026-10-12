# AI Usage Log: {{PROJECT_NAME}}

This log records every substantive AI-assisted session on the project "{{PROJECT_TITLE}}".

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

<!-- Append new entries below this line, newest at the bottom.
     On instantiating a new project from this template, delete every entry below:
     they belong to the template's own development, not to your project. -->

## [2026-09-22 20:43 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5
- **Session Purpose**: Create the HamSCI `ai_project_template` by adapting
  `w2naf-academia/ai_project_template` for general HamSCI use: restructure the AI policy stack
  into three tiers so volunteer and student projects are not forced to carry institutional and
  funder sections, add HamSCI-specific rules for callsign attribution and station-location
  privacy, and add a getting-started onramp, LICENSE, CITATION.cff, and issue templates matching
  HamSCI house style.
- **Sections/Files Affected**: `README.md`, `CLAUDE.md`, `LICENSE`, `CITATION.cff`, `.gitignore`,
  `.claude/rules/ai-governance.md`, `.claude/rules/hamsci-data.md` (new),
  `.claude/rules/latex-writing.md`, `.claude/rules/python-code.md`, `.claude/commands/commit.md`,
  `.claude/settings.json`, `ai/ai_usage_log.md`, `docs/GETTING_STARTED.md`,
  `.github/ISSUE_TEMPLATE/` (bug_report, feature_request, question)
- **Nature of Contribution**: Scaffolding, drafting, and adaptation of an existing template
- **Human Review Status**: Pending review by N. A. Frissell (W2NAF)
- **Git Hash**: d1983ff

## [2026-10-01 16:26 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5
- **Session Purpose**: Update the template so that every commit goes on a feature branch and
  through a pull request that a human reviews and merges, replacing the earlier
  "commit to main, ask before pushing" workflow.
- **Sections/Files Affected**: `.claude/commands/commit.md` (steps 6 to 9 rewritten for branch, PR, pointer bump, push order), `CLAUDE.md` (Commits and push paragraphs; Submodules order), `.claude/rules/python-code.md`, `.claude/rules/ai-governance.md`, `docs/GETTING_STARTED.md`, `README.md`
- **Nature of Contribution**: Edit
- **Human Review Status**: Pending review
- **Git Hash**: d96b578 (branch pr-workflow, PR HamSCI/ai_project_template#1), merged as 4276dd1

## [2026-10-01 17:46 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5
- **Session Purpose**: Stop the AI usage log from forcing a second pull request per change. The
  Git Hash field is now filled in once, on the change's own branch; a merge commit keeps that
  SHA valid, so no post-merge "merged SHA" update is needed.
- **Sections/Files Affected**: `.claude/commands/commit.md` (Git Hash and submodule pointer-bump steps)
- **Nature of Contribution**: Edit
- **Human Review Status**: Pending review
- **Git Hash**: ee16043 (PR HamSCI/ai_project_template#3)

## [2026-10-10 12:08 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5 (1M context)
- **Session Purpose**: Make committing rendered output standing guidance, at NAF's direction
  (2026-10-10): memo and report PDFs and final figures capture the results of the code in
  human-readable form and must be committed, or past work is hard to look back on.
- **Sections/Files Affected**: `CLAUDE.md` (new "Rendered Output" section), `.claude/rules/latex-writing.md` (compiled PDF is not a build artifact), `.claude/rules/python-code.md`, `.claude/commands/commit.md` (step 2b), `.gitignore`.
- **Nature of Contribution**: Edit (workflow guidance).
- **Human Review Status**: Pending review.
- **Notes**: The `.gitignore` no longer ignores `figs/` and `figures/` by default; the opposite default.
- **Git Hash**: 81753cf, branch `commit-rendered-output`

## [2026-10-10 12:35 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5 (1M context)
- **Session Purpose**: Narrow the committed-output rule to curated documents, at NAF's direction
  (2026-10-10): "I'm looking more to capture PDFs that are memos, notes, or some more curated
  level of analysis", not large generated outputs such as figure batches.
- **Sections/Files Affected**: `CLAUDE.md` ("Curated Documents"), `.claude/commands/commit.md` (step 2b), `.claude/rules/python-code.md`, `.gitignore` (`figs/` and `figures/` are ignored again, as before the earlier PR).
- **Nature of Contribution**: Edit (workflow guidance).
- **Human Review Status**: Pending review.
- **Git Hash**: febc1c6, branch `curated-documents-only`

## [2026-10-10 15:01 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5 (1M context)
- **Session Purpose**: Make projects check their upstream ai_project_template for workflow and
  rule changes, at NAF's direction (2026-10-10), so repositories stop drifting from their
  template unnoticed.
- **Sections/Files Affected**: `.claude/template.json` (new: this template's record and the
  sibling templates it watches); `.claude/hooks/template_check.sh` (new: session-start check,
  read-only, once a day, silent on failure); `.claude/settings.json` (registers the hook);
  `.claude/commands/template-sync.md` (new: applies template changes as changes, through a PR);
  `CLAUDE.md` ("Template Updates"); `README.md` (instantiation step for the record).
- **Nature of Contribution**: Code generation, drafting.
- **Human Review Status**: Pending review.
- **Notes**: The check script was tested on scratch repositories (behind, current, freshly
  instantiated, unreachable upstream) and on this template. Hook format checked against the
  Claude Code hooks documentation. Project hooks run without a trust prompt; this one only reads
  `.claude/template.json` and makes one public HTTPS request to GitHub.
- **Git Hash**: 4887dfb, branch `template-sync-tooling`

## [2026-10-10 15:14 UTC]
- **Tool**: Claude (Anthropic), claude-opus-5-5 (1M context)
- **Session Purpose**: Fix a flaw in the template check found before rolling it out: comparing
  commit SHAs alone made templates flag each other indefinitely (marking a sibling reviewed is
  itself a commit the siblings see) and flagged projects for template changes with nothing to
  adopt.
- **Sections/Files Affected**: `.claude/hooks/template_check.sh` (asks GitHub's compare API which
  files changed and ignores `.claude/template.json`, `ai/ai_usage_log.md` and, in a project, its
  `not_adopted` files; falls back to flagging if the file list is unavailable; names the changed
  files in its notice); `.claude/commands/template-sync.md` (record and log are never taken from
  the template; companion changes only need marking reviewed); `.claude/template.json` (sibling
  template-sync tooling, the companion of this template's own, marked reviewed).
- **Nature of Contribution**: Code generation, edit.
- **Human Review Status**: Pending review.
- **Notes**: Tested on scratch repositories (behind: flagged with file list; only ignorable
  changes: silent) and on the live w2naf-academia template (flags both siblings' tooling PRs).
- **Git Hash**: f59d373, branch `template-check-filter`
