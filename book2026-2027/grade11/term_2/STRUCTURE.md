# Grade 11 — Term 2 Structure

## Overview

This directory contains the LaTeX sources for a Grade 11 statistics unit on confidence-interval planning and inference in economic and financial contexts. Its four collections separate worked practice, formal learning evidence and assessments, criterion-specific catch-up work, and supplementary lesson material. Student-facing question sheets generally have a corresponding teacher-facing worked-solution source; no compiled PDFs, datasets, web assets, or build configuration are stored here.

`STRUCTURE.md` is this inventory document and is intentionally omitted from the inventory counts and tree below.

## Directory tree

```text
.
├── 1-practice_activities/                         # Worked lesson practice organized by lesson and assessment criterion.
│   ├── G11_T2_L2_C6_practice.tex                 # Worked C6 practice on required and additional sample sizes for means with known population spread.
│   ├── G11_T2_L2_C7_practice.tex                 # Worked C7 practice constructing and interpreting confidence intervals for proportions.
│   ├── G11_T2_L3_C10_practice.tex                # Worked C10 hypothesis-test conclusions for mean parameters, including Type I and II errors.
│   ├── G11_T2_L3_C8_practice.tex                 # Worked C8 small-sample t-interval examples for means with unknown variance.
│   └── G11_T2_L3_C9_practice.tex                 # Worked C9 comparisons of t- and z-intervals for means when variance is unknown.
├── 2-learning_evidences/                          # Student assessments, project briefs, practice assessments, and teacher solutions.
│   ├── G11_T2_L1_exam.tex                        # Student-facing Lesson 1 exam on sample summaries and mean intervals with known population standard deviation.
│   ├── G11_T2_L1_exam_practice.tex               # Student-facing two-problem practice exam using grouped loading times and raw cafeteria-demand data.
│   ├── G11_T2_L1_exam_practice_solution.tex      # Teacher-facing worked solutions to the Lesson 1 practice exam.
│   ├── G11_T2_L1_exam_solution.tex               # Teacher-facing worked solutions to the Lesson 1 exam's subsidy, order-rate, and loading-time problems.
│   ├── G11_T2_L2_C6_activity.tex                 # Student-facing C6 activity with six mean sample-size and margin-of-error planning problems.
│   ├── G11_T2_L2_C6_activity_solution.tex        # Teacher-facing worked solutions to all six C6 activity problems.
│   ├── G11_T2_L2_C7_activity.tex                 # Student-facing C7 activity assessing proportion intervals in five applied contexts plus follow-up problems.
│   ├── G11_T2_L2_C7_activity_solution.tex        # Teacher-facing worked solutions for the C7 activity's contextual and numbered problems.
│   ├── G11_T2_L2_midterm.tex                     # Student-facing midterm covering sample statistics, parameters, confidence intervals, interpretation, and sample size.
│   ├── G11_T2_L2_midterm_solution.tex            # Teacher-facing fully worked solutions to the standard midterm.
│   ├── G11_T2_L2_mock_midterm.tex                # Student-facing standard mock midterm on mean/proportion intervals and sample-size planning.
│   ├── G11_T2_L2_mock_midterm_hard.tex           # Student-facing harder mock with more demanding multi-step inference and planning tasks.
│   ├── G11_T2_L2_mock_midterm_hard_solution.tex  # Teacher-facing worked solutions to the harder mock midterm.
│   ├── G11_T2_L2_mock_midterm_solution.tex       # Teacher-facing worked solutions to the standard mock midterm.
│   ├── G11_T2_L2_reference_midterm.tex           # Worked reference midterm for confidence and interval estimation; it is labeled as solutions, not a blank student paper.
│   ├── G11_T2_L3_proyect.tex                     # Student-facing project brief for presenting and defending an AI-generated confidence-interval web page.
│   ├── G11_T2_L3_proyect_Excel.tex               # Alternative student project brief for an Excel confidence-interval tool with CSV input, dashboards, and simple macros.
│   ├── G11_T2_L3_proyect_problems.tex            # Student-facing set of ten t-interval calculation, interpretation, and decision problems for the project unit.
│   └── G11_T2_L3_proyect_problems_solutions.tex  # Teacher-facing detailed and concise solutions to the ten project-unit problems.
├── 3-catch_ups/                                   # Criterion-by-criterion remediation sheets and their teacher solution companions.
│   ├── G11_T2_C1_catchUp.tex                     # Student-facing C1 practice computing sample means and standard deviations in ten finance contexts.
│   ├── G11_T2_C1_catchUp_solution.tex            # Teacher-facing worked solutions to the ten C1 problems.
│   ├── G11_T2_C2_catchUp.tex                     # Student-facing C2 practice distinguishing sample statistics from population parameters.
│   ├── G11_T2_C2_catchUp_solution.tex            # Teacher-facing detailed and minimal solutions to the ten C2 classification problems.
│   ├── G11_T2_C3_catchUp.tex                     # Student-facing C3 practice comparing point and interval estimates and their decision risk.
│   ├── G11_T2_C3_catchUp_solution.tex            # Teacher-facing contextual explanations for the ten C3 problems.
│   ├── G11_T2_C4_catchUp.tex                     # Student-facing C4 practice interpreting interval bounds, confidence, plausibility, and comparisons.
│   ├── G11_T2_C4_catchUp_solution.tex            # Teacher-facing worked interpretations and decisions for the ten C4 problems.
│   ├── G11_T2_C5_catchUp.tex                     # Student-facing C5 practice constructing mean intervals when long-run population spread is known.
│   ├── G11_T2_C5_catchUp_solution.tex            # Teacher-facing calculations and interpretations for the ten C5 interval problems.
│   ├── G11_T2_C6_catchUp.tex                     # Student-facing C6 practice planning sample sizes, interval widths, and precision upgrades.
│   ├── G11_T2_C6_catchUp_solution.tex            # Teacher-facing worked sample-size solutions for the twelve C6 planning scenarios.
│   ├── G11_T2_C7_catchUp.tex                     # Student-facing C7 practice building, comparing, and using confidence intervals for proportions.
│   └── G11_T2_C7_catchUp_solution.tex            # Teacher-facing step-by-step solutions and recommendations for the C7 proportion problems.
└── 4-extra_material/                              # Supplementary Lesson 1 assessment work and consolidated Lesson 3 worked material.
    ├── G11_T2_L1_supplementary.tex               # Student-facing extra Lesson 1 problems on known-spread mean intervals across confidence levels and samples.
    ├── G11_T2_L1_supplementary_solution.tex      # Teacher-facing worked solutions to the supplementary Lesson 1 problem set.
    └── G11_T2_L3_MATERIAL.tex                    # Consolidated worked Lesson 3 material for C8 t-intervals, C9 t-versus-z comparison, and C10 mean conclusions.
```

## Resource categories

- **Student-facing pages:** the unsuffixed exams, activities, mock exams, project briefs, project problems, catch-up sheets, and supplementary sheet are printable LaTeX assessment or lesson sources.
- **Teacher materials:** every `_solution.tex` or `_solutions.tex` source supplies worked answers. `G11_T2_L2_reference_midterm.tex`, the five practice sources, and `G11_T2_L3_MATERIAL.tex` also contain worked solutions despite not consistently using a solution suffix.
- **Lesson and assessment resources:** Lesson 1 introduces known-spread intervals; Lesson 2 develops criteria C6–C7 and midterm assessment; Lesson 3 develops unknown-variance t inference and conclusions (C8–C10). Catch-ups remediate C1–C7 individually.
- **Stylesheets and JavaScript:** none are stored in this directory. The AI web-page project describes a deliverable but does not include its HTML, CSS, or JavaScript implementation.
- **Images and media:** none are stored locally. Sixteen standalone assessment sheets reference the shared logo outside this directory.
- **Data and configuration:** no separate datasets or configuration files are present. Numeric observations and grouped tables are embedded directly in the LaTeX sources; the Excel project only specifies CSV import as a student deliverable.
- **Downloadable documents:** all 41 inventoried files are `.tex` source documents. There are no prebuilt PDF, Word, spreadsheet, or other downloadable binaries here.
- **Generated/build-related files:** none are present or intentionally version-controlled in this tree.

## Important relationships

- Twenty-five sources use a shared `preamble_exams.tex` to provide document setup and custom commands such as `\ExamTitleBlock`, `\ExamSection`, and `ExamProblems`; the remaining sixteen define their own `article` preamble and directly reference the shared `logo.png`.
- Both shared resources live outside `term_2`, under `book2026-2027/preamble/`. The sixteen standalone sources consistently refer to the logo as `../../../preamble/logo.png` from their immediate subdirectories.
- Nine shared-preamble sources use `../../../preamble/preamble_exams.tex`, which resolves from their subdirectories to the repository's `book2026-2027/preamble/` directory. Sixteen instead use `../../preamble/preamble_exams.tex`; from the source-file directory that points to a nonexistent `grade11/preamble/`. Whether those sixteen are compiled from a working directory that makes the reference valid **requires verification**.
- Student/teacher pairs share the same problem contexts: Lesson 1 exam and practice, C6 and C7 activities, standard and hard mock midterms, project problems, each C1–C7 catch-up, and Lesson 1 supplementary work each connect to the correspondingly named solution source.
- `G11_T2_L2_reference_midterm.tex` is a worked reference rather than the answer key for either named mock. `G11_T2_L2_mock_midterm_solution.tex` and `G11_T2_L2_mock_midterm_hard_solution.tex` are the direct keys for those two mocks.
- `G11_T2_L3_MATERIAL.tex` consolidates worked C8, C9, and C10 content; the three Lesson 3 practice files split those criteria into separate documents. The C8/C9 practice is confidence-interval work, while C10 focuses on inference conclusions and decision errors.
- The two Lesson 3 project briefs are alternative implementation tracks: one asks students to present an AI-generated web page, while the other asks for an Excel workbook with imported CSV observations, dashboard output, and macros. Neither implementation nor dataset is included here.
- LaTeX compilation is the only build relationship visible in this directory. There are no HTML pages, stylesheets, scripts, package manifests, build scripts, or compiled outputs to connect locally.

## Inventory notes

- **Documented:** 41 existing files and 4 directories (excluding the `term_2` root and this inventory file).
- **Excluded:** no transient or generated items were found; there were no `.DS_Store`, editor-cache, LaTeX auxiliary, temporary, dependency, or compiled PDF files to omit.
- **Requires verification:** the intended compilation working directory for the sixteen sources whose shared-preamble path is `../../preamble/preamble_exams.tex`.
