# Exam Authoring Guide

## Instructions for the AI

Open [`template_exam.tex`](template_exam.tex) and start from a copy in the intended output directory. Use the copy for the new material.

Gather the grade, evidence number and title, term, learning objective, assessed criterion IDs and descriptions, questions and their data or figures, point allocations, and any grading or submission rules. Confirm whether students write on the sheet and how much space each item needs.

Replace all sample questions, values, figures, scores, policy text, and criterion descriptions with material for the new exam. Rebuild the score matrix from the questions. Match each heading's criterion points to its row, sum each criterion column, and include only the criteria actually assessed. Use the supplied passing threshold and penalty rules where applicable.

Use the current heading interface from [the exam layout](../preamble/preamble_exam_layout.tex). Write `\SubsectionBox*{Criteria assessment}` for the unnumbered heading and pass problem titles without the literal numbers shown in the scaffold. The unstarred form numbers the problems automatically. If answers belong on the sheet, reserve blank vertical space or add ruled lines below the relevant prompts within the current column width. Keep solutions out of the student copy.

### LaTeX inputs

Build the scaffold from `book2026-2027/authoring/` and the adapted copy from its own source directory. See the [build instructions](README.md#building). The scaffold's `\input@path` searches the working directory, parent directories, and nearby `preamble/` directories. For example, from `book2026-2027/seminars/`, `../preamble/` reaches the maintained inputs. Load [`preamble_exams.tex`](../preamble/preamble_exams.tex) once. It loads the common article preamble through the unified Grade 10 C1–C3 preamble and adds the exam layout. If the output directory is outside the scaffold's search range, add a working-directory-relative entry with a trailing slash to the build's TeX search path (for example, through `TEXINPUTS`, retaining the default search path). An explicit path on the first `\input` alone can leave nested inputs unresolved.

Keep the scaffold's `\graphicspath` after the preamble, and verify it finds [the logo](../preamble/logo.png) required by `\ExamHeader` as well as any question figures. Adjust that path or the figure paths in the copy if needed.

## Output Template

Keep the full-width `\ExamHeader{grade}{evidence number}{title}{term}`, `\LearningObjective{objective}{criteria}` and `\StudentInfo` in that order, before the two-column body. Retain the objective and criteria table layout with `\setYColumnWidth` and separate criteria with `\par`. In the body, keep **Criteria assessment**, the score matrix, and the scored problem blocks in order. Use `\score` and `\sml` for criterion marks in the boxed headings. Check the numbering, the fit of the matrix and figures, and the space left for answers.

Compile the adapted copy with `pdflatex` when available. Inspect the result for missing assets and layout problems.
