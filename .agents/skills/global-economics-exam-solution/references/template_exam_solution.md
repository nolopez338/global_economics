# Exam Solution LaTeX and Build Guide

## Shared inputs

Copy the [solution-key scaffold](../assets/template_exam_solution.tex) to the key's intended source directory. Load the [shared exam preamble](../../../../book2026-2027/preamble/preamble_exams.tex) once with `\input{preamble_exams.tex}`. It supplies the document class, common packages, exam formatting, and navigation commands.

The scaffold searches relative to the directory where pdfLaTeX runs. Its `\input@path` covers the skill's `assets/` directory and common source directories within the book. For a different layout, run from the key's source directory and prepend the absolute path to the shared `preamble/` directory to `TEXINPUTS`. This also resolves nested preamble and graph inputs. Keep the empty path component for TeX's default search paths. For example, in PowerShell:

```powershell
$env:TEXINPUTS = 'C:/path/to/repo/book2026-2027/preamble/;'
```

Resolve source-specific figure paths from the key's source directory, or copy the required assets into that directory and use relative paths. The build output directory controls where pdfLaTeX writes files.

## Scored headings and navigation

- Use `\sectionScored{title}{criterion scores}{label}` when its automatic numbering matches the source. Omit the question number from the title in this case. Format each heading allocation as `[criterion ID]-\sml{[points]}` and use `\score{[points]}` beside prompts and solution headings. Include each criterion's allocation where the source provides a split.
- When the automatic sequence would change a source identifier, use an explicit scored heading and add a linked contents entry. With the shared preamble, `\section*` creates a hyperlink destination at the heading.

```latex
\section*{[Original question ID and title] \score{[Criterion ID]-\sml{[Points]}}}
\label{sec:source-question}
\addcontentsline{toc}{section}{[Original question ID and title]}
```

- For linked multipart prompts with one criterion per task, use `\QuestionsTasks[section-label]{entries}`. Each entry is `{criterion number}/{solution label}/{original subpart label, prompt, and marks}`. Separate entries with commas and brace each field to protect embedded commas or slashes. Supply the numeric part of the criterion ID in the first field because the macro adds `C`. Keep the source subpart identifier in the prompt field and the question identifier in its section heading. If the macro cannot represent the source labels or criterion allocation faithfully, use a source-labeled list or blocks with `\hyperref[solution-label]{...}` links.
- Give each linked solution a unique `\label` immediately after its `\subsection*` heading. For a target without a heading, use `\phantomsection` followed by `\label`. Use `\secInicio[][section-label]` at the end of a solution to link back to the contents and question. Keep the `toc` label immediately before the table of contents.

## Figures and wide work

Preserve original figures in the prompt. For a reusable graph, start with the [graph workflow](../../../../book2026-2027/preamble/graphs/README-graphs.md). Open the chosen command's definition to confirm its argument order, meanings, units, and dependencies. After the exam preamble, import only the graph files used by the key and any required dependencies with `\input{graphs/<file>.tex}`.

Pair a figure and its calculation or completed table in top-aligned minipages when both are legible at normal size. Give each minipage enough width for its contents and keep their combined widths below `\linewidth`. Use `aligned` or `align*` to break long derivations and give wider work the full text width. For genuinely wide work, use a `landscape` environment from the shared preamble.

## Build and inspect

Run from the directory containing the key's `.tex` file. Use its filename as the job name so the PDF has the same basename. For a temporary build, create a temporary directory first and pass its absolute path with `-output-directory`.

```powershell
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error exam_solutions.tex
```

Rerun until the contents, links, and references stabilize. Check the final log for unresolved or duplicate destinations, missing inputs, and overfull boxes. Inspect the PDF at normal size for readable calculations, figures and tables, sensible page breaks, and numbering and marks that match the source. Check that contents entries lead to question headings, task links lead to the corresponding solutions, and return links lead to the correct question and contents.
