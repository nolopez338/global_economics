# Exam Solution Authoring Guide

## Instructions for the AI

Open [`template_exam_solution.tex`](template_exam_solution.tex) and start from a copy in the intended output directory. Use the copy for the new material.

Gather the source exam if available, including all prompts, figures, subparts, objectives, criteria, point values and grading policies. For a solution document authored from a brief, gather the assessment items and mark scheme. Use supplied grading rules and flag missing allocations or conflicts for clarification.

When adapting an exam, preserve its question wording, order, numbering, and point values, including subpart and criterion splits. Reproduce any context, data, or graphs needed to understand the questions. If the source numbering differs from the automatic sequence, carry the original identifiers explicitly in the corresponding headings or task text. The first field of a `\QuestionsTasks` entry is a criterion number, so it cannot carry the question identifier by itself.

Replace the sample topics, questions, values, graphs, criteria, and rubric text. Give a worked solution for every item and subpart, with the method, result, and any required justification or units. Indicate what earns each mark, including partial credit where applicable. Reconcile the marks in the prompts, solution headings, and rubric with the section scores and the source exam's criterion and overall totals.

### LaTeX inputs

Build the scaffold from `book2026-2027/authoring/` and the adapted copy from its own source directory. See the [build instructions](README.md#building). The scaffold's `\input@path` searches the working directory, parent directories, and nearby `preamble/` directories. For example, from `book2026-2027/seminars/`, `../preamble/` reaches the maintained inputs. Load [`preamble_exams.tex`](../preamble/preamble_exams.tex) once. It loads the common article preamble through the unified Grade 10 C1–C3 preamble and adds the exam layout. If the output directory is outside the scaffold's search range, add a working-directory-relative entry with a trailing slash to the build's TeX search path (for example, through `TEXINPUTS`, retaining the default search path). An explicit path on the first `\input` alone can leave nested inputs unresolved.

Open the [uniform and linear](../preamble/graphs/uniform_linear_probability_distributions.tex), [distribution comparison](../preamble/graphs/probability_distribution_graphs.tex), or [normal distribution](../preamble/graphs/normal_distribution_graphs.tex) input for any graph macro you use. Keep the corresponding `\input{graphs/...}` lines after the exam preamble and drop unused graph inputs from the copy.

## Output Template

Keep the title, linked contents with the `toc` anchor, **Learning objective**, **Criteria assessment**, **Evaluated criteria**, and scored sections in that order. Use `\sectionScored{title}{criterion scores}{label}` for each scored problem, followed by its context, `\QuestionsTasks`, and worked subsections with `\score` markers. Supply braced `{criterion number}/{solution label}/{prompt with points}` entries. Give each worked subsection a unique `\phantomsection` and `\label`, and keep its `\secInicio` link pointing back to the problem. Keep paired minipages for graph-and-work layouts where they fit.

Compile the adapted copy with `pdflatex` when available, repeating until the contents and references resolve. Inspect the result for missing assets and layout problems.
