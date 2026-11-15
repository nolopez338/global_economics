# Review plan contract

The standard-library helper has two phases. Scan writes a disposable plan under
`.cache/global-economics-readme/<sha256(repository-relative-target)>/plan.json`.
Only successful commit writes `state.json`. Missing, corrupt or incompatible
state means baseline review. Target identity is repository-relative, so moving
the checkout does not invalidate it. Repository-root targets cannot have a
repository-local cache outside themselves; the helper reports this constraint
instead of silently violating cache placement. Select a subfolder for that case.

The plan includes input metadata/hashes, directory/child-README membership,
added/content_changed/removed/unchanged reports, cached analyses, and review
keys. Source files use `file:NAME`; folders use `folder:NAME`; consulted sources
use `dep:repository/relative/path`. The output README is never a source input.

Edit only these plan fields:

- `analysis.purpose`: concise one-sentence folder role and intended use.
- `analysis.files.NAME`: `{ "type": "LaTeX", "description": "Defines ….",
  "commands": ["\\Command", "\\Variant"], "sections": [
  {"level": 1, "title": "Exact Unicode heading", "description": "Explains …."}
  ] }`. Empty commands/sections render as `None.`. Levels are source hierarchy,
  not guessed document numbering. Markdown includes explicit headings; LaTeX
  includes repeated and custom section commands. No filename-only guesses.
- `analysis.folders.NAME`: `{ "description": "Provides ….",
  "readme": "README-child.md" }`; use null when absent. Multiple child README
  candidates require inspecting and selecting the summary; do not modify them.
- `analysis.dependencies`: repository-relative path to list of affected owners,
  e.g. `{"book2026-2027/preamble/sections.tex": ["file:lesson.tex"]}`.
  Include every additional source actually consulted, including child contents,
  the vocabulary example if used, and custom macro definitions. A changed or
  removed dependency invalidates its owners. To register a new dependency,
  rerun scan with repeatable `--dependency PATH=OWNER` arguments **before reading
  it**, then fill the new plan. Carry forward previous edits if still valid.
  This fingerprints dependencies before review and detects concurrent edits.
  Remove unused dependency entries and their input records by rescanning with
  `--drop-dependency PATH` once no descriptions rely on them.
- `verified`: all keys in `review` that you have actually reviewed.
- `conformance`: exact template hash, after checking the full live template.
- `reconciled`: true once any existing/manual README changes are reconciled.

Descriptions and titles are plain text; the renderer escapes Markdown table
content and preserves Unicode. Inline relative Markdown links are supported
in descriptions and validated, including their targets. Use exact public
command names without surrounding backticks; the renderer adds them. Do not
put generated artifact references in any description.

When only metadata changes, hashes permit semantic reuse. A changed dependency
invalidates its owners; membership changes require checking affected summaries.
Folder keys change when immediate child README candidates/content change.
The summary purpose must be reconsidered whenever the plan says
`summary_review`; unchanged analyses may still be reused. Template updates
require conformance review of the complete rendered result. Helper/schema
updates conservatively require a new baseline. Read errors stop scan/commit;
semantic limitations stop certification and must be reported to the user.

Commit prints reviewed/reused input counts (excluding the output README), plus
status/path. It refuses stale plans even for timestamp-preserving content edits
by fully hashing the snapshot again before replacement. If interrupted after
README replacement but before cache commit, the next scan reconciles the output;
the previous cache is never marked current prematurely. Plan files are not
trusted source facts: agent verification remains necessary.
