# Print Handout Authoring Guide

## Instructions for the AI

Open [`template_print.tex`](template_print.tex) and start from a copy in the intended output directory. Use the copy for the new material.

Gather the grade and term, topic, ordered problem contexts, data and any required figures, and the classifications and parameters expected in the answer table. Confirm print or page constraints.

Replace the example grade and term, problem text, values, any example graphs, and the bracketed table placeholders. Resize the problem list and table together. For each problem, use its list number as the Context, identify the Type and Distribution, and state defining parameters, support, or other relevant properties in Characterization. Verify the numbering and that each classification follows from the given context.

### LaTeX inputs

Build the scaffold from `book2026-2027/authoring/` and the adapted copy from its own source directory. See the [build instructions](README.md#building). The scaffold's `\input@path` searches the working directory, parent directories, and nearby `preamble/` directories. For example, from `book2026-2027/seminars/`, `../preamble/` reaches the maintained inputs. Load [`preamble_exams.tex`](../preamble/preamble_exams.tex) once. It loads the common article preamble through the unified Grade 10 C1–C3 preamble and adds the exam layout. If the output directory is outside the scaffold's search range, add a working-directory-relative entry with a trailing slash to the build's TeX search path (for example, through `TEXINPUTS`, retaining the default search path). An explicit path on the first `\input` alone can leave nested inputs unresolved.

Open the [uniform and linear](../preamble/graphs/uniform_linear_probability_distributions.tex), [distribution comparison](../preamble/graphs/probability_distribution_graphs.tex), or [normal distribution](../preamble/graphs/normal_distribution_graphs.tex) input for any graph macro you use. Keep its `\input{graphs/...}` line after the exam preamble. Drop unused graph inputs from the copy.

## Output Template

Keep `\pagestyle{empty}` and the compact **Problem Descriptions** page first, using the local `\newgeometry` and numbered list. Keep the page break and `\restoregeometry` before **Solutions**, then the centered full-width `tabularx` with Context, Type, Distribution, and Characterization in that order. Preserve the centered fixed-width columns and wrapping `X` column. The scaffold displays its centered problem heading directly, with title metadata available in the source. Check print fit and legibility, especially wrapping in the solution table.

Compile the adapted copy with `pdflatex` when available. Inspect the result for missing assets and layout problems.
