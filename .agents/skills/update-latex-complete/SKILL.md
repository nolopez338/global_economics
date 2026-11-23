---
name: update-latex-complete
description: Update existing Global Economics LaTeX sources with compilation, mathematical and structural checks, rendered-page inspection for fit and overlap, and reusable validation-tool maintenance. Use for complete, verified, or print-ready updates; exclude explicitly fast source-only edits.
---

# Update LaTeX Complete

Deliver revised source and a matching, inspected PDF. Perform the ordered process in [references/verification-workflow.md](references/verification-workflow.md), including repair and rechecking. Compilation alone does not establish visual correctness.

## Scope and project conventions

- Identify the target, requested change, document type, and intended output. Preserve unrelated user edits, language, metadata, criteria, content boundaries, and naming conventions. Do not turn a narrow update into a template migration or pedagogical redesign.
- Read the actual class, preamble, included definitions, relevant neighboring conventions, and applicable instructions. Reuse shared macros and relative inputs; retain intentional inline preambles and portability in standalone Beamer decks. Inspect consumers before changing a shared definition and verify affected consumers afterward.
- Preserve task/solution navigation and stable labels. Common commands include `\QuestionsTasks`, `\SectionProblemsTableOfContents`, `\SectionProblemLink`, and `\secInicio`; read their current definitions before changing their usage.
- Preserve mathematical meaning, units, assumptions, answer boundaries, and official criterion wording. Check changed calculations and dependent results. Keep independent/assessed work unsolved in student copies.
- Respect document-specific formatting. Classroom activities omit instructional highlights; other documents may use shared highlight renderers and the legend registry under `book2026-2027/preamble/highlights/`. Preserve existing toggle settings and concept-notation-value roles. Concise legends and detailed references serve different purposes. Do not impose either on a document that does not need it.
- Prefer suitable local widths, wrapping, semantic consolidation, and splitting oversized material over tiny fonts, whole-table/frame scaling, or negative-spacing patches. Beamer reveals should reserve dimensions and preserve logical frame numbers.
- Consult an available authoring, legend, or highlight skill only for an applicable responsibility. Apply relevant document rules without restarting completed work or importing unrelated content requirements.

## Self-updating validation assets

This skill owns reusable validation assets. Store executable helpers in `scripts/` and reusable procedures in `references/`; these are skill assets even though they are not placed in the `assets/` directory. Reserve `assets/` for fixtures or other non-executable supporting files when needed. Do not create empty folders or placeholder tools.

Whenever this workflow creates a new general-purpose validation function, script, or process:

1. Look for an existing helper or procedure in this skill and relevant repository tooling before creating another. Extend the suitable one when possible.
2. Separate general mechanics from document-specific expectations. Accept file paths, page ranges, tolerances, and expected values as arguments or caller-supplied data. Never bake a particular exercise, grade, formula, answer, heading, criterion, or page count into the reusable validator.
3. Save the reusable implementation here before finishing the task, including helpers initially developed in a temporary directory or inline command. Save executable code in `scripts/` and a non-code process in `references/`. Do not merely describe an unsaved function in the final response. Content-specific checks stay with the current task, outside this reusable library.
4. Document purpose, dependencies, exact invocation, inputs, outputs, failure behavior, and limits in a linked reference or the helper's help text. Describe what it detects and what still requires visual or mathematical inspection. Avoid claiming automatic overlap detection when it only checks boxes or warnings.
5. Exercise new or changed code on a representative passing input and a known failing input in an isolated temporary directory. For a written process, apply it to the current document and refine ambiguous or unworkable steps. Retain lightweight reusable test fixtures only when they materially support maintenance; no student submissions or generated course PDFs belong in the skill.
6. Add or update a direct link in the **Validation asset index** below, stating when to use the resource. Preserve existing entries and avoid redundant tools. A saved file without a discoverable entry is incomplete maintenance.

Persist only generally useful validation mechanics: for example, log diagnostics, PDF page-bound checks, link-target inspection, render orchestration, or overlay comparison. A check for one activity's exercise count or one equation's numerical result is not general merely because it is implemented in Python. A configurable comparison mechanism can be reusable; its lesson-specific expectations are not skill defaults.

Keep helpers local and narrowly scoped: no automatic downloads, document modification, repository cleanup, or external uploads as validation side effects. Use available dependencies and report missing ones. If saving an asset is prevented by permissions, finish unaffected document work and disclose the unsaved asset and limitation; do not claim the library was updated.

## Validation asset index

- [Verification workflow](references/verification-workflow.md): ordered source, build, log, mathematical, navigation, visual, variant, and final-delivery checks for LaTeX handouts and Beamer slides. Use on every complete update. This is the initial reusable process; add concrete helpers here as they are developed and exercised.

- [PDF review renderer](scripts/render_pdf_review.py): render every PDF page plus numbered contact sheets for manual fit/overlap review. Requires Python, pypdfium2 and Pillow; use the bundled workspace Python. Run `python render_pdf_review.py input.pdf output-directory --dpi 90`; CLI help documents arguments, outputs, failures and limits. This does not detect overlap or replace inspecting the images.

- [PDF rendering comparison](scripts/compare_pdf_rendering.py): compare every page of two PDFs using the same PDFium renderer with zero pixel tolerance. Use for visual-preservation refactors; optional page-count and physical-size assertions, per-page images and JSON reports support inspection. CLI help documents dependencies and limitations. Does not replace content review or manual inspection.

## Delivery

Link the revised `.tex` and verified matching PDF. Summarize the change, checks actually performed, remaining issues or unperformed checks, and any validation assets added or improved. Never call a document fully verified when compilation, relevant consumer checks, or visual inspection could not run. Do not deliver a stale PDF as matching revised source.
