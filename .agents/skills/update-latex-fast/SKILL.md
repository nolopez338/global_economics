---
name: update-latex-fast
description: Make fast source-only edits to existing Global Economics LaTeX files for manual review. Use for fast or explicitly unverified updates; never compile, render, test, review, or validate the result.
---

# Update LaTeX Fast

Apply the requested edit and stop. The user will manually revise the result. This mode deliberately omits every verification step, including lightweight checks.

## Source-only workflow

1. Identify the requested `.tex` file and read only the source, applicable instructions, and dependencies needed to implement the change. Use targeted searches to locate the edit, existing macros, or their definitions. These reads support editing; do not expand them into an audit.
2. Edit the source directly, keeping the change within the requested scope. Preserve unrelated user edits. Change an included `.tex` definition only when the request requires it; prefer a local adjustment over altering shared behavior.
3. Report the edited source path and a short description of the change. Explicitly say: **Not compiled or verified; ready for manual review.** Then finish.

## Hard boundary: no verification

- Do not run any LaTeX engine, `latexmk`, build script, PDF export, or background compilation. Do not launch a tool or editor flow that automatically builds on save.
- Do not render, open, inspect, regenerate, copy, or replace a PDF. Leave existing PDFs and build artifacts untouched; do not present an old PDF as revised output.
- Do not run linters, syntax checks, validators, tests, calculations for checking correctness, link checks, layout checks, toggle comparisons, or content audits.
- Do not inspect logs, review a diff, reread the edited file to check the result, or perform a post-edit search as a substitute for validation. Do not run repository-wide scans or checklists.
- Do not create validation helpers, validation reports, or temporary builds. Do not invoke the complete workflow as a final step.
- A failed edit operation may be retried to apply the requested edit; that does not authorize checking the resulting document. Report a tool failure if the change cannot be applied.

When using an authoring or highlighting skill for implementation guidance, use only its relevant source-editing conventions and skip compilation, verification, and delivery-PDF stages under this explicit fast-mode request. If the user subsequently requests verification, use [update-latex-complete](../update-latex-complete/SKILL.md) for that work; do not silently switch modes.

## Project conventions to retain while editing

- Follow the target's language, grade/term/criterion metadata, neighboring filename conventions, class, and existing organization. An update does not request a different activity template or a rewritten lesson.
- Reuse the target's shared preamble and relative inputs. Many handouts use `book2026-2027/preamble/preamble_exams.tex`; standalone Beamer decks can intentionally keep preambles and macros inline. Do not convert one arrangement into the other.
- Retain existing labels and navigation when moving content. Documents may use `\QuestionsTasks`, `\SectionProblemsTableOfContents`, `\SectionProblemLink`, and `\secInicio` for task, solution, and return links.
- Reuse existing table helpers, graph commands, and local widths (`\linewidth` inside columns/minipages). Keep calculations, units, notation, and reasoning unless the requested change concerns them. Prefer reflow, useful column widths, or splitting content over indiscriminate font reduction.
- Preserve highlight mappings and toggle settings where present. Shared definitions may live in `preamble/graphs/highlights.tex` and `specific_highlights.tex`. Classroom activities intentionally omit instructional highlights; do not import them from a practice source. Concise legends and detailed notation references have distinct purposes; do not merge or duplicate them incidentally.
- Preserve Beamer overlay timing, reserved dimensions, and logical frame numbering. Do not insert new substantive instructional content merely to solve a layout request.

These are implementation conventions, not a checklist to verify afterward.
