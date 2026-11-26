---
name: global-economics-readme
description: Create or incrementally update one Global Economics folder README from its path, following the live repository README template and verified source contents.
---

# Global Economics README

Input: one target folder, absolute or relative to the repository root. Example:
`$global-economics-readme book/grade10/term_1/1-practice_activities`.
Optional `--force` requests full hashing and semantic review.

Work only on that folder's immediate summary README. Preserve an existing
`README.md` or `README-*.md` name. Inspect multiple candidates and choose the
clearly identifiable directory summary; ask only when genuinely ambiguous.
Never change source documents, child READMEs, or the template.

## Workflow

1. Read **the live** `book/preamble/template_README.md` on every
   invocation; it is authoritative. Read the existing README when present.
   The Grade 10 Term 1 practice README is a domain vocabulary/content example,
   not a structural authority. Do not copy its omissions, compressed headings,
   stale claims, or LaTeX-only inventory restriction.
2. Run `python .agents/skills/global-economics-readme/scripts/readme.py TARGET`
   from the repository root (or supply `--root ROOT`). It prints the plan path,
   change report, and review requirements. If selection is ambiguous, inspect
   candidates and rerun with `--readme NAME`. Read the plan and follow
   [the review contract](references/workflow.md).
3. Review only `review` inputs and affected folder summaries. A baseline or
   `--force` requires all inputs. A template change requires full conformance
   review but permits reuse of valid source analyses. A manually edited or
   missing output always requires reconciliation. Do not reread unchanged
   semantic sources just to confirm an unchanged run.
4. Fill the plan's `analysis` with verified English descriptions, public
   definitions (including aliases/variants), and every explicit heading in
   source order and hierarchy. Read contents; imports and uses are not
   definitions. Inspect custom LaTeX section definitions and register any
   consulted sources as dependencies. Keep accurate existing prose where
   supported. Inspect immediate child READMEs for folder descriptions; for
   children without one, inspect sufficient maintained content and register
   those files as dependencies. Report unreadable/unsupported material;
   never certify an incomplete analysis. Mark the listed review keys in
   `verified`, set `conformance` to the plan's template hash after checking
   every current template instruction, and set `reconciled` true after
   checking any manual edits. Do not acknowledge checks you did not perform.
5. Run `python .agents/skills/global-economics-readme/scripts/readme.py TARGET
   --commit PLAN`. The helper checks inventories, ordering, links, exclusions,
   placeholders, structure, and concurrent edits; writes only changed bytes
   atomically; and commits verified cache state last. If inputs changed, rescan
   and retry at most twice, then report concurrent edits. If the live template
   requires a rendering rule the helper cannot express, adapt and test the
   helper before committing; never silently override the template.

Derive the README's own entry from its six final sections, without recursively
summarizing the inventory. Keep Unicode headings verbatim, repetitions and
hierarchy intact. Use relative forward-slash links. Apply live exclusions in
all sections even for tracked artifacts or old descriptions. Do not include
cache files. The helper screens using nanosecond mtime and size; `--force`
also detects timestamp-preserving edits. Ordinary screening is an optimization,
not proof against those edits.

Finish with the README path, created/updated/already current, reviewed versus
reused input counts, and material limitations. An unchanged rerun must reuse
analyses and preserve README bytes and mtime.
