# Classroom Print Activity Layout and Build Guide

Use [the LaTeX scaffold](../assets/template_print.tex) from the intended source directory. Its margins, table, and response space are editable starting points.

## Shared inputs

Load the [shared preamble](../../../../book2026-2027/preamble/preamble.tex) once with `\input{preamble.tex}`. It declares the article class and loads geometry, tables, lists, TikZ, PGFPlots, and navigation helpers.

Run pdfLaTeX from the directory containing the activity's `.tex` file. The scaffold's `\input@path` searches `../../../preamble/` for source files in `book2026-2027/<grade>/<term>/<activity-folder>/` and `../../../../book2026-2027/preamble/` when building from the skill's `assets/` directory. For another location, adjust the relative preamble path in the copy or prepend the absolute shared preamble directory to `TEXINPUTS` for the build. This lookup also resolves `\input{graphs/...}` and nested inputs. Use a trailing slash on the directory and retain an empty search component for TeX's default paths. In a Windows PowerShell build session, set it as follows.

```powershell
$env:TEXINPUTS = 'C:/path/to/repo/book2026-2027/preamble/;'
```

On POSIX shells use `:` in place of `;`. The pdfLaTeX `-output-directory` option places build artifacts elsewhere while the command still runs from the source directory.

## Page layout

- Set paper size and normal margins with `\geometry{...}` after the preamble and before `\begin{document}`. Set page numbering with `\pagestyle{plain}` or `\pagestyle{empty}` as the brief requires. Let page count follow the work students need to do and the available print area.
- Use section headings for the stages the lesson needs. Wrap a short problem in a top-aligned `minipage` of width `\linewidth` to keep the prompt, data, and response area together, as shown in the scaffold. For a long problem, remove the `minipage` and allow breaks between tasks or between a task and the next data block.
- Place small tables and figures in the text near the task they support. Size tables to `\linewidth`, which accounts for list indentation. Use `tabularx` with wrapping `X` columns or paragraph-width columns for longer text. If a table must span pages, use `longtable` with repeated headings. Check row height, answer lines, and blank space at print size.
- Set `\printsolutionstrue` when the brief calls for review pages. The optional Solutions block uses `\clearpage` to start on a fresh page. When using `\newgeometry` on the student pages, replace that `\clearpage` with `\restoregeometry`, which starts a fresh page and restores the normal margins. Scope student-only spacing changes with a group that ends before the Solutions heading.
- For a longer PDF, use shared navigation commands where useful. Use `\TaskHyperref{label}{text}` for a link to an existing label or `\SectionProblemLink{label}{title}` for a numbered problem link. Put labels after the corresponding numbered heading or `\item`.

## Graphs

1. Consult the [shared graph guide](../../../../book2026-2027/preamble/graphs/README-graphs.md) to find a suitable command. Open its definition and verify the arguments, their order and meaning, and any required inputs or libraries.
2. Add only the `\input{graphs/...}` lines used by the document, including inputs required by the chosen commands, after the preamble. Use local TikZ or PGFPlots when no shared command fits.
3. Check axes, units, labels, plotted values, and annotations against the context, task, and any solution. Check readability at the printed size.

## Build and inspect

Run from the source directory.

```text
pdflatex -interaction=nonstopmode -halt-on-error activity.tex
```

Repeat the build when cross-references or navigation need a second pass. To keep build artifacts separate, create a temporary directory and add `-output-directory` with its absolute path.

Inspect the log for missing inputs and overfull boxes. Inspect the rendered pages for page breaks, clipping, table legibility, and room to write. If solutions are included, verify that their first page follows the last student page, normal layout has resumed, and every answer matches its worksheet number and task label. For a student-only build, verify that the PDF ends with the student pages.
