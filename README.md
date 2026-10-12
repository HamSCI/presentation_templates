# HamSCI AI Project Template

A starter scaffold for AI-assisted research, writing, and software projects in the HamSCI
community. It makes AI governance the default rather than an afterthought: every instantiated
project carries the HamSCI Generative AI Use Agreement, a mandatory session log, and a `/commit`
workflow that records what AI did before the work is committed.

HamSCI spans funded research groups, student projects, and volunteer working groups. The
template is built for all three. The policy stack is tiered, so a volunteer project deletes the
institutional and funder sections outright instead of inheriting rules that do not apply to it.

The same scaffold supports:

- **Writing projects** (papers, proposals, reports, theses), typically with an `overleaf/` submodule
- **Software projects** (analysis pipelines, instrument software, dashboards), flat or with code submodules
- **Hardware and instrument projects** (PSWS, Grape, magnetometer, receiver work)
- **Mixed projects**, in any combination

New to Claude Code or to AI-use policy? Start with [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md).

## Use as a GitHub Template

```bash
gh repo create HamSCI/my-new-project --template HamSCI/ai_project_template --private --clone
```

or click **Use this template** on the GitHub repository page. Keep the repository private while
the work is unpublished.

## After Instantiation

1. **Replace the placeholders.** Find them all with `grep -rn '{{' --exclude-dir=.git .` and work
   through `CLAUDE.md`, `.claude/rules/ai-governance.md`, `ai/ai_usage_log.md`, and
   `CITATION.cff`. Clear the existing entries in `ai/ai_usage_log.md`; they belong to the
   template's own development. Common placeholders:
   - `{{PROJECT_NAME}}`, `{{PROJECT_TITLE}}`, `{{PROJECT_GOAL}}`, `{{PROJECT_PERIOD}}`, `{{REPO_NAME}}`
   - `{{LEAD_NAME_CALLSIGN_AND_AFFILIATION}}`, `{{COLLABORATORS}}`, `{{WORKING_GROUP}}`, `{{YOUR_NAME}}`
   - `{{INSTITUTION}}`, `{{POLICY_DATE}}`, `{{FUNDER}}`, `{{FUNDER_AND_GRANT_NUMBER}}`
   - `{{YYYY-MM-DD}}` in `CITATION.cff`

   Deleting a policy tier in step 2 removes several of these, so trim the tiers first if you
   already know the project is unfunded or has no institution behind it.
2. **Trim the policy tiers.** In `.claude/rules/ai-governance.md`, delete Tier 2 if no
   institutional policy governs the work, and Tier 3 if the project is unfunded. Tier 1 stays.
3. **Prune the optional rule files.**
   - `rm .claude/rules/latex-writing.md` if the project has no LaTeX
   - `rm .claude/rules/python-code.md` if the project has no Python
4. **Add project-specific folders** such as `manuscript/`, `src/`, `notes/`, `data/`, `posters/`.
5. **Add submodules if needed.**
   - Overleaf manuscript: `git submodule add https://git.overleaf.com/<id> overleaf`
   - HamSCI code repo: `git submodule add git@github.com:HamSCI/<repo>.git <path>`
6. **Update `LICENSE` and `CITATION.cff`** for the new project, and delete
   `docs/GETTING_STARTED.md` once the project is running.

### Record which template commit you started from

`.claude/template.json` arrives describing this template. Turn it into a project record: set
`"role": "project"`, `"upstream": "HamSCI/ai_project_template"`, `"upstream_branch": "main"`, `"synced_commit"` to the
template commit you instantiated from (the tip of `main` that day), and `"synced_on"`; list in
`"customized"` the files whose placeholders you filled in, and in `"not_adopted"` any template
files you deleted; remove `repo` and `siblings`. From then on, a session-start check reports when
this template changes and `/template-sync` adopts the changes. If you skip this step, the first
Claude session notices and offers to do it.

## What This Template Provides

| File | Purpose |
|---|---|
| `CLAUDE.md` | Project instructions Claude Code reads first in every session. Imports the binding rules. |
| `.claude/rules/ai-governance.md` | The tiered policy stack, logging requirements, and disclosure rules. |
| `.claude/rules/hamsci-data.md` | Callsign attribution, station-location privacy, community datasets, volunteer credit. |
| `.claude/rules/latex-writing.md` | Optional. Scoped to `.tex`, `.bib`, `.cls`, `.sty`. |
| `.claude/rules/python-code.md` | Optional. Scoped to `.py`, `pyproject.toml`, `requirements*.txt`. |
| `.claude/commands/commit.md` | The `/commit` workflow: log the session, then commit each changed repo (submodules first) on a feature branch and open a pull request. |
| `ai/ai_usage_log.md` | Append-only record of every substantive AI-assisted session. |
| `docs/GETTING_STARTED.md` | Onboarding for participants new to Claude Code or to AI governance. |
| `.github/ISSUE_TEMPLATE/` | Bug, enhancement, and question templates matching HamSCI house style. |
| `CITATION.cff`, `LICENSE` | Citation metadata and an MIT license, ready to edit. |
| `.gitignore` | LaTeX and Python build artifacts, bulk data formats, credentials, local Claude state. |

## The Rules That Always Apply

Whatever else a HamSCI project changes about this scaffold, these stay:

- **Never fabricate.** No invented citations, data, numbers, callsigns, or attributions.
- **Humans own the science.** A human reviews AI output before it enters an artifact, and the
  scientific claims are the authors'.
- **AI is not an author.** Never in an author block, an acknowledgment, or a `CITATION.cff`.
- **Log before you commit.** Every substantive session, in `ai/ai_usage_log.md`, with a real
  timestamp.
- **Disclose AI use in published outputs**, naming the tool and describing what it did.
- **Protect contributors.** Operator personal data, unpublished collaborator data, and
  ITAR/EAR-controlled material never go to an external AI tool.

## License

MIT. See [`LICENSE`](LICENSE). Projects instantiated from this template may choose any license;
replace the `LICENSE` file with the one your project needs.

## Contributing

Issues and pull requests are welcome at
https://github.com/HamSCI/ai_project_template. If you maintain a HamSCI project that needed a
rule this template does not have, that is worth an issue.
