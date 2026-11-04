# Home Practice Activities Authoring Guide

## Instructions for the AI

Open [`template_home_practice.tex`](template_home_practice.tex) and start from a copy in the intended output directory. Use the copy for the new material.

Use this guide for independent, criterion-linked work, including activities delivered on paper. Write prompts students can follow independently.

Gather the grade and term, topic, criterion IDs and descriptions, target skills and difficulty, activities or source questions, and any supplied data, graphs or desired solutions. Identify which tasks need a worked example, solution, or graph.

Replace sample topics, questions, values, answers, and graphs. Pair each activity with the appropriate criterion and show the intermediate reasoning and interpretation. Recalculate results and ensure plots match the model, axes, ranges, and highlighted intervals. Replace the graph command demonstrations with relevant plotting activities or omit that section when graph work is outside the brief.

### LaTeX inputs

Build the scaffold from `book2026-2027/authoring/` and the adapted copy from its own source directory. See the [build instructions](README.md#building). The scaffold's `\input@path` searches the working directory, parent directories, and nearby `preamble/` directories. For example, from `book2026-2027/seminars/`, `../preamble/` reaches the maintained inputs. Load [`preamble_exams.tex`](../preamble/preamble_exams.tex) once. It loads the common article preamble through the unified Grade 10 C1–C3 preamble and adds the exam layout. If the output directory is outside the scaffold's search range, add a working-directory-relative entry with a trailing slash to the build's TeX search path (for example, through `TEXINPUTS`, retaining the default search path). An explicit path on the first `\input` alone can leave nested inputs unresolved.

Open the [uniform and linear](../preamble/graphs/uniform_linear_probability_distributions.tex), [distribution comparison](../preamble/graphs/probability_distribution_graphs.tex), or [normal distribution](../preamble/graphs/normal_distribution_graphs.tex) input for any graph macro you use. Keep its `\input{graphs/...}` line after the exam preamble. Drop unused graph inputs from the copy.

## Output Template

Keep the title, linked contents with the `toc` anchor, **Evaluated criteria**, and **Worked Solution Examples** in order. Follow with a graph section when appropriate. Use numbered problem subsections and `\SectionProblemsTableOfContents` with `\SectionProblemLink` entries pointing to their labels. Use `\QuestionsTasks[section-label]` with braced `{criterion number}/{solution label}/{task text}` entries, unique anchored labels for worked subsubsections, and `\secInicio[problem-label][section-label]` for return navigation. Keep side-by-side minipages for a graph and calculation or table when both fit. Check task coverage and the contents, problem and return links.

Compile the adapted copy with `pdflatex` when available, repeating until the contents and references resolve. Inspect the result for missing assets and layout problems.
