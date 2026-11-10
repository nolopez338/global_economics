# Classroom Activity Layout and Build Guide

Copy the [LaTeX scaffold](../assets/template_classroom_activity.tex) to the intended source directory. The [C1 practice source](../../../../book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex) illustrates how to identify families. Use the [C1 classroom source](../../../../book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.tex) and its [rendered PDF](../../../../book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.pdf) as visual references.

## Shared inputs

Load the activity's year-local `preamble.tex` once. It declares the 11 pt article class. Run pdfLaTeX from the source directory. The scaffold searches `../../../preamble/` from `<year>/<grade>/<term>/2-class_activities/` and `../../../../book2026-2027/preamble/` from its own `assets/` directory. In a classroom activity, keep only the lookup for its own year. For scratch builds, replace the relative lookup or prepend the absolute year-local preamble directory to `TEXINPUTS`. A trailing path separator retains TeX's default search paths. The lookup also resolves `graphs/...` and nested inputs.

```powershell
$env:TEXINPUTS = 'C:/path/to/repo/book2026-2027/preamble/;'
```

Use `:` as the search-path separator on POSIX systems.

## Print layout

- After the shared preamble, apply `\geometry{letterpaper,margin=0.25in}`. Keep the same margins for every student and solution page. Start with `\linespread{1.04}` and 4 pt paragraph spacing.
- Use a compact centered title and course metadata, with the criterion statement clearly identified below. Use `\stageheading` for the four centered headings, `\problemtitle` for gray numbered problem titles with right-aligned family labels, and `\task` for bold inline task labels. Reserve enough space to keep each heading with the opening content. The scaffold uses `\Needspace` and positive spacing for those transitions.
- Pair short worked or guided tasks in top-aligned `0.48\linewidth` minipages separated by `\hfill` when the pair is easy to scan. Use full-width blocks for wide or tall content. Keep each prompt close to its data and response space. For a short block that must stay together, reserve its measured height with `\Needspace` before the block. Allow long problems to break at task boundaries.
- Size tables to the local `\linewidth`. Use wrapping `tabularx` columns as needed and `longtable` with repeated headings for multi-page tables. Leave blank cells, lines, or space for calculations or sketches when the task calls for them. Let the content determine the page count.
- For graphs, consult the year-local [graph guide](../../../../book2026-2027/preamble/graphs/README-graphs.md) and check the chosen command's arguments and dependencies. Load the graph inputs the activity uses. Check axes, units, labels, plotted values, and annotations at print size.

## Build and inspect

Run pdfLaTeX from the source directory. The scaffold defaults to `\printsolutionsfalse` for the student PDF. To build a review PDF from the same source, use `\printsolutionstrue` or override the switch at document start with a separate job name.

```powershell
pdflatex -interaction=nonstopmode -halt-on-error activity.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=activity-review '\AtBeginDocument{\printsolutionstrue}\input{activity.tex}'
```

Use `-output-directory` with an existing absolute directory to keep build files separate. Repeat a build if its cross-references require another pass.

Check the logs for missing inputs and overfull boxes. Inspect the rendered pages for fixed margins, legible tables, clear spacing between stage headings and problem titles, clean page breaks, and room for student work. Verify that the review has the same student pages followed by a fresh Solutions page. Check every guided and independent answer against the student problem number, family, task labels, and givens.

