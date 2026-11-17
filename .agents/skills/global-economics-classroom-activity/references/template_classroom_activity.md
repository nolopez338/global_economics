# Classroom Activity Layout and Build Guide

Copy the [LaTeX scaffold](../assets/template_classroom_activity.tex) to the intended source directory. Every activity has exactly one fully worked example, one guided example, and five unsolved independent exercises, with no highlights anywhere. These counts apply to the whole activity, not to each problem family. The [C1 practice source](../../../../book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex) illustrates how to identify families. Use the [C1 classroom source](../../../../book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.tex) and its [rendered PDF](../../../../book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.pdf) as visual references only where compatible with the fixed counts and prohibition on highlights.

## Content and highlight rules

- Keep the four stage headings in the scaffold. Number the worked example 1, the guided example 2, and the five independent exercises 3–7. Do not duplicate blocks per family; cover source families within these seven problems.
- Give the single worked example a complete solution with clear, step-by-step reasoning, intermediate results, checks, and interpretation.
- Give the single guided example structured prompts and sufficient workspace for each required step. Students complete the key reasoning and final answer.
- Leave all five independent exercises unsolved in the student handout and provide workspace appropriate to each task. The first three (problems 3–5) consolidate core skills. The last two (problems 6–7) are slightly more challenging within the same topic and assessment criterion; do not import unrelated advanced material.
- Never include instructional highlights, highlighted text or mathematics, semantic highlight commands, or highlight legends, including on optional review pages. Remove highlight wrappers while preserving their text or mathematics. Remove highlight-only legends, labels, and navigation; retain any substantive notation or explanation in ordinary form. Do not copy highlight definitions or imports. Preserve ordinary headings, bold task labels, tables, and mathematical layout.
- Inspect commands inherited from the shared preamble and nested inputs before using them. For example, the current year-local `\boxed` produces a shaded box: display the result as ordinary mathematics instead. Replace other highlight-producing uses locally without editing shared files. Unused formatting definitions in the required shared preamble do not justify using highlights in the activity.

## Shared inputs

Load the activity's year-local `preamble.tex` once. It declares the 11 pt article class. Run pdfLaTeX from the source directory. The scaffold searches `../../../preamble/` from `<year>/<grade>/<term>/2-class_activities/` and `../../../../book2026-2027/preamble/` from its own `assets/` directory. In a classroom activity, keep only the lookup for its own year. For scratch builds, replace the relative lookup or prepend the absolute year-local preamble directory to `TEXINPUTS`. A trailing path separator retains TeX's default search paths. The lookup also resolves `graphs/...` and nested inputs.

```powershell
$env:TEXINPUTS = 'C:/path/to/repo/book2026-2027/preamble/;'
```

Use `:` as the search-path separator on POSIX systems.

## Print layout

- After the shared preamble, apply `\geometry{letterpaper,margin=0.25in}`. Keep the same margins for every student and solution page. Start with `\linespread{1.04}` and 4 pt paragraph spacing.
- Use a compact centered title and course metadata, with the criterion statement clearly identified below. Use `\stageheading` for the four centered headings, `\problemtitle` for plain bold numbered problem titles with right-aligned family labels, and `\task` for bold inline task labels. Do not shade or color text or mathematics as highlights. Reserve enough space to keep each heading with the opening content. The scaffold uses `\Needspace` and positive spacing for those transitions.
- Pair short worked or guided tasks in top-aligned `0.48\linewidth` minipages separated by `\hfill` when the pair is easy to scan. Use full-width blocks for wide or tall content. Keep each prompt close to its data and response space. For a short block that must stay together, reserve its measured height with `\Needspace` before the block. Allow long problems to break at task boundaries.
- Size tables to the local `\linewidth`. Use wrapping `tabularx` columns as needed and `longtable` with repeated headings for multi-page tables. Leave blank cells, lines, or space for calculations or sketches when the task calls for them. Let the content determine the page count.
- Use `\workspace{<height>}` for adjustable blank working space and `\responseline` for short answers. The scaffold's heights are starting points: expand them to fit the actual reasoning, calculations, tables, or graphs. Keep guided prompts next to their response spaces and give every independent exercise enough room for a full solution.
- For graphs, consult the year-local [graph guide](../../../../book2026-2027/preamble/graphs/README-graphs.md) and check the chosen command's arguments and dependencies. Load the graph inputs the activity uses. Check axes, units, labels, plotted values, and annotations at print size.

## Build and inspect

Run pdfLaTeX from the source directory. The scaffold defaults to `\printsolutionsfalse` for the student PDF, containing exactly one complete worked example, one guided example, and five unsolved independent exercises. To build a requested review PDF from the same source, use `\printsolutionstrue` or override the switch at document start with a separate job name. Review answers belong only on separate solution pages for the existing problems 2–7; they do not add student examples or exercises. Both versions must remain entirely free of highlights and highlight legends.

```powershell
pdflatex -interaction=nonstopmode -halt-on-error activity.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=activity-review '\AtBeginDocument{\printsolutionstrue}\input{activity.tex}'
```

Use `-output-directory` with an existing absolute directory to keep build files separate. Repeat a build if its cross-references require another pass.

Before delivery:

- Count exactly one worked example, one guided example, and five independent exercises on the student pages. Check the worked solution is complete and explains every step.
- Check the guided prompts leave meaningful work for students and have sufficient response space. Check every independent exercise is unsolved and has appropriate workspace.
- Verify independent exercises 1–3 (problems 3–5) consolidate core skills and exercises 4–5 (problems 6–7) add modest challenge within the same topic and criterion.
- Inspect the LaTeX, local definitions, imported content, and rendered pages for instructional highlights, highlighted text or mathematics, semantic highlight commands, and highlight legends. Remove all such content or formatting while preserving underlying mathematical and explanatory content. Check for indirect highlighting through custom macros as well as direct formatting commands.
- Check logs for missing inputs and overfull boxes. Inspect fixed margins, legible tables, heading spacing, clean page breaks, and room for student work.
- If requested, verify that the review has the same student pages followed by a fresh Solutions page, also without highlights. Check each answer for problems 2–7 against the student problem number, family, task labels, and givens.

