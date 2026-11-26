# Grade 11 — Term 3 Structure

## Overview

Grade 11 Term 3 is a LaTeX-based collection for teaching and assessing
hypothesis testing. It progresses from designing hypotheses (criteria C1–C3),
through one-sample proportion and mean tests and interpretation (C4–C7), to a
web implementation and report using two-sample tests (C8–C10). The four
top-level resource directories separate guided practice, learning evidence,
catch-up work, and a longer worked exam. There are no HTML, CSS, or JavaScript
implementations in this directory; the learning-evidence brief asks students to
create and submit those files.

Audience labels below distinguish **student-facing**, **teacher/solution**, and
**shared lesson** resources. LaTeX sources are printable lesson, assessment, or
answer-key documents; CSV files are data resources rather than generated build
outputs.

## Directory tree

```text
.
├── 1-practice_activities/                         # Shared lesson practice and reference material, mostly with worked solutions.
│   ├── G11_T3_L1_C1C2C3_practice_activity.tex    # Shared lesson: extended C1–C3 hypothesis-design practice with ten mean/proportion contexts and solutions.
│   ├── G11_T3_L1_C1C2C3_practice_activity1.tex   # Shared lesson: introductory C1–C3 activity with four solved contexts for parameters, hypotheses, and tail direction.
│   ├── G11_T3_L1_C1C2C3_practice_activity2.tex   # Shared lesson: eight solved C1–C3 tests emphasizing directional claims, changing alpha, and one- versus two-tailed comparisons.
│   ├── G11_T3_L1_C1C2C3_practice_activity3.tex   # Shared lesson: six open-ended, locally framed C1–C3 problem-design prompts with solution guidance.
│   ├── G11_T3_L2_C4_practice_activity.tex         # Shared lesson: solved C4 ladder for one-sample proportion z-tests, from basic cases to threshold/sample-size comparisons.
│   ├── G11_T3_L2_C5_practice_activity.tex         # Shared lesson: parallel solved C5 ladder for one-sample mean z-tests in count contexts.
│   ├── G11_T3_L3_C6_practice_activity.tex         # Shared lesson: solved C6 cases on decisions, contextual conclusions, Type I/II errors, and policy implications.
│   ├── G11_T3_L3_C7_practice_activity.tex         # Shared lesson: solved C7 minimum-sample-size problems with one-/two-tail and multi-alpha graphs.
│   ├── G11_T3_MATERIAL.tex                        # Shared lesson bank: twenty scaffolded hypothesis-test contexts spanning school, consumer, and economics topics.
│   └── G11_T3_summary.tex                         # Teacher/reference overview summarizing the intended progression and problem roles of the C1–C7 practice sequence.
├── 2-learning_evidences/                          # Student assessments, answer keys, a web-project brief, and its candidate/example datasets.
│   ├── G10_T3_L4_C10_dataset_1.csv                # Data: 60 delivery-time observations, split evenly among North_A, South_B, and East_C routes.
│   ├── G10_T3_L4_C10_dataset_2.csv                # Data: 60 weekly screen-time observations, split among Grade 10 STEM, arts, and sport groups.
│   ├── G10_T3_L4_C10_dataset_3.csv                # Data: 60 resale-value observations, split among Plan_A, Plan_B, and Plan_C.
│   ├── G11_T3_C1C7_midterm.tex                    # Student-facing midterm on a Grade 11 punctuality audit, assessing C1–C7 across two cohort benchmarks.
│   ├── G11_T3_C1C7_midterm_solution.tex           # Teacher material: full worked midterm key with explanations and plotted normal rejection regions.
│   ├── G11_T3_C1C7_midterm_solution_minimal.tex   # Teacher material: condensed key for the same midterm, retaining calculations/graphs with less exposition.
│   ├── G11_T3_L1_C1C2C3_exam_solution.tex         # Teacher material: model C1–C3 contexts plus guidance for six student-designed school-to-Bogotá problems.
│   ├── G11_T3_L1_C1C2C3_exam_student.tex          # Student-facing C1–C3 assessment template requiring six balanced mean/proportion hypothesis designs.
│   ├── G11_T3_L1_C4C5_exam_student.tex            # Student-facing C4–C5 assessment requiring four data-supported tests selected from six personal/local contexts.
│   ├── G11_T3_L1_C6C7_exam_solution.tex           # Teacher material: worked C6 decision/error cases and C7 minimum-sample-size cases in economic contexts.
│   ├── G11_T3_L2_C4C5_exam_solutions.tex          # Teacher material: concise five-problem C4–C5 key covering foundational, sensitivity, directional, and synthesis tests.
│   ├── G11_T3_L4_C10_dataset_1.csv                # Data: 30 study-hours observations, 15 each for groups A and B.
│   ├── G11_T3_L4_C10_dataset_2.csv                # Data: 30 delivery-time observations, 15 each for FastShip and CityExpress.
│   ├── G11_T3_L4_C10_dataset_3.csv                # Data: 30 exercise-duration observations, 15 each for weekdays and weekends.
│   ├── G11_T3_L4_C8C9C10_activity.tex             # Student-facing C8–C10 brief for an HTML/CSS/JavaScript two-sample-testing page and written report.
│   ├── G11_T3_L4_C8C9C10_dataset_1.csv            # Data: 24 numeric scores for Control and Treatment groups (dataset G11_D1).
│   ├── G11_T3_L4_C8C9C10_dataset_2.csv            # Data: 30 binary success outcomes for Method_A and Method_B (dataset G11_D2).
│   ├── G11_T3_L4_C8C9C10_dataset_3.csv            # Data: 24 time measurements for Baseline and New_Process groups (dataset G11_D3).
│   ├── G11_T3_L4_C8C9_example_mean_data.csv       # Example data: 12 paired columns of numeric observations for groups A and B.
│   └── G11_T3_L4_C8C9_example_proportion_data.csv # Example data: 20 student-level group labels and binary success outcomes.
├── 3-catch_ups/                                   # Remedial or supplementary assessment material.
│   └── suplementary_homework.tex                  # Student-facing catch-up homework: a full C1–C7 hypothesis-design/decision task using two cohort benchmarks.
└── 3-exams/                                       # Expanded worked examination resources, separate from the learning-evidence folder.
    └── G11_T3_L2_exam_solutions.tex               # Teacher material: eight worked C4–C5 proportion/mean tests with graphs and contextual interpretation.
```

`STRUCTURE.md` is this inventory and is intentionally omitted from the tree.

## Resource types and important relationships

- **LaTeX documents and shared configuration:** most practice and solution
  documents load `../../../preamble/preamble_exams.tex` (some use a flexible
  `\input@path`); the C6–C7 solution instead loads `preamble.tex`. These shared
  preambles live outside Term 3 and supply document formatting and commands.
  Several standalone assessments declare their own packages rather than loading
  a shared preamble.
- **Images and generated graphics:** standalone assessment headers reference
  `../../../preamble/logo.png`, also outside this tree. Files using
  `\IfFileExists` render a boxed “Logo” fallback, while three early learning
  evidence files reference the logo directly. Statistical diagrams are drawn
  from LaTeX/TikZ/PGFPlots code in the sources; no separate Term 3 image or media
  assets are stored here.
- **Practice progression:** the C1–C3 activities introduce parameters,
  hypotheses, and tail choice; the C4 and C5 ladders apply proportion and mean
  z-tests; C6 interprets decisions and errors; and C7 derives minimum sample
  sizes. `G11_T3_summary.tex` describes this sequence, although some filenames
  cited inside it use `L1` where the present files use `L2`/`L3` (see
  **Requires verification**).
- **Assessment variants:** the C1–C3 `exam_student` file is the blank student
  template and `exam_solution` adds model solutions/instructor guidance. The
  midterm has one student paper and two keys: a fully explained key and a
  deliberately shorter “minimal” key. The two Lesson 2 solution files are not
  duplicates: `2-learning_evidences/...exam_solutions.tex` is a concise
  five-problem set, while `3-exams/...exam_solutions.tex` expands coverage to
  eight worked C4–C5 problems.
- **Web, stylesheets, and JavaScript:** no `.html`, `.css`, or `.js` files are
  present. `G11_T3_L4_C8C9C10_activity.tex` is the specification that requires
  students to submit a main HTML file, linked stylesheet(s), JavaScript file(s),
  and a deployed-page link. It also links to external Git/GitHub Pages tutorials
  and three SharePoint datasets; those links are not local file dependencies.
- **Local datasets:** the activity brief does not name or programmatically load
  any local CSV. The `G11_T3_L4_C8C9C10_dataset_*` files nevertheless match its
  requested two-sample numerical/proportion work: score and time data support
  mean comparisons, while binary success data support a proportion comparison.
  The two `example_*` files provide smaller demonstration layouts. The three
  `G11_T3_L4_C10_dataset_*` files are additional two-group numeric datasets.
- **Downloadable documents and builds:** the directory contains editable `.tex`
  sources but no compiled PDFs or other downloadable binary documents. It also
  contains no build configuration, generated LaTeX auxiliaries, or dependency
  directories.

## Requires verification

- The three `G10_T3_L4_C10_dataset_*` files contain explicitly Grade 10 group
  names/data but are stored in Grade 11 Term 3. Their contents are clear, but
  whether their placement is intentional cannot be established from local
  references.
- `G11_T3_summary.tex` names C4–C7 practice files as Lesson 1 resources; the
  actual files are named Lesson 2 (C4/C5) and Lesson 3 (C6/C7). The summary's
  conceptual descriptions match those files, but the stale naming should be
  confirmed before treating it as a literal dependency map.

## Inventory scope

This inventory documents **32 pre-existing files** and **4 directories** below
the Term 3 root. No transient or generated item was present to exclude. Per the
requested policy, this newly created inventory is not counted or listed in its
own tree.
