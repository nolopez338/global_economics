# Grade 10 — Term 3 Structure

## Overview

This directory contains the source materials for Grade 10 Term 3 probability instruction. The sequence moves from practice on discrete and continuous distributions (criteria C0–C7), through student assessments and their teacher solution sets, to catch-up work and a C8–C10 web/data-modeling project. All printable resources are LaTeX source files; the only local data assets are three CSV datasets supplied for the project. There are no HTML, CSS, JavaScript, compiled PDFs, or build/configuration files in this directory.

The inventory below documents **32 existing files in 4 directories**. `STRUCTURE.md` itself is the inventory document and is intentionally omitted from the tree.

## Directory tree

```text
.
├── 1-practice_activities/                         # Student practice, consolidated worked material, contexts, and a teacher-oriented summary for C0–C10.
│   ├── G10_T3_C0_practice_activity.tex            # Student-facing worked practice on discrete PMFs: validity, unknown probabilities, event sums, graphs, and contextual interpretations.
│   ├── G10_T3_C1C2C3_practice_activity_context.tex # Student-facing contextual set joining C1 density validity, C2 uniform mixtures, and C3 triangular investment models.
│   ├── G10_T3_C1_practice_activity.tex            # Student-facing C1 progression from geometric area review to validating and using uniform and linear PDFs, including parameterized domains.
│   ├── G10_T3_C2_practice_activity.tex            # Student-facing C2 practice on uniform and piecewise-uniform PDFs, unknown constants/endpoints, complements, and multi-interval models.
│   ├── G10_T3_C3_practice_activity.tex            # Student-facing C3 practice using geometry—not integration—for linear, triangular, piecewise-linear, and parameterized densities.
│   ├── G10_T3_C4_practice_activity.tex            # Student-facing C4 worked comparisons of mean, variance, and standard deviation for uniform, triangular, and normal distributions.
│   ├── G10_T3_C5_practice_activity.tex            # Student-facing C5 guide and nine worked problem types for reading the standard-normal table and combining tails/intervals.
│   ├── G10_T3_C6_practice_activity.tex            # Student-facing C6 contextual normal problems organized by left-tail, right-tail, central-band, and two-region cases after standardization.
│   ├── G10_T3_C7_practice_activity.tex            # Student-facing C7 inverse-normal applications for upper/lower percentiles and symmetric central intervals in real contexts.
│   ├── G10_T3_Contexts.tex                        # Standalone explanatory article comparing real-life continuous-PDF models, geometric calculations, assumptions, limitations, and references.
│   ├── G10_T3_MATERIAL.tex                        # Consolidated worked C1–C10 problem collection; the original edition uses integration in early density solutions.
│   ├── G10_T3_MATERIAL_V2.tex                     # Revised consolidated C1–C10 collection replacing early integration-based work with geometric area reasoning and revising some models.
│   └── G10_T3_summary.tex                         # Teacher-oriented pedagogical summary of the C0–C7 practice files, including progression, strengths, gaps, and suggested improvements.
├── 2-learning_evidences/                          # Lesson assessments, alternate versions, teacher solutions, a computational project brief, and its input datasets.
│   ├── G10_T3_C1C7_midterm.tex                    # Student midterm assessing C1–C7 with original numerical parameters and contextual density/normal-distribution tasks.
│   ├── G10_T3_C1C7_midtermV2.tex                  # Alternate student midterm with revised header/rubric, shifted numerical parameters, and reformatted C5 questions.
│   ├── G10_T3_C1C7_midterm_solution.tex           # Teacher solution set for the original C1–C7 midterm, with full derivations, graphs, and a minimal C5–C7 answer section.
│   ├── G10_T3_C1C7_midterm_solutionV2.tex         # Teacher solution set matching the V2 midterm's changed endpoints, scenarios, distribution parameters, and answers.
│   ├── G10_T3_L1_C1C2C3_exam.tex                 # Student Learning Evidence 1 exam: 17 C1–C3 density-validity, uniform, piecewise-uniform, and linear/triangular tasks.
│   ├── G10_T3_L1_C1C2C3_exam_solution.tex        # Teacher worked solutions to the C1–C3 exam, including geometric derivations and plotted density regions.
│   ├── G10_T3_L1_C4_exam.tex                     # Student C4 Learning Evidence 2 on matching/drawing uniform, triangular, and normal distributions by mean and spread.
│   ├── G10_T3_L1_C4_examV2.tex                   # Non-credit practice version of the C4 assessment with changed distributions, graph ranges, and answer options.
│   ├── G10_T3_L1_C4_examV2_solution.tex          # Teacher worked answers for the altered C4 V2 practice set, organized problem by problem.
│   ├── G10_T3_L1_C4_exam_solution.tex            # Concise teacher answer key for the original C4 exam, grouped into matching and drawing problems and retaining the exam-style header.
│   ├── G10_T3_L1_C4_exam_solution_long.tex       # Expanded teacher solution for the original C4 exam with an evaluated-criterion overview and individual explanations for all 18 tasks.
│   ├── G10_T3_L1_C5_exam_solution.tex            # Teacher C5 worked solution set covering six standard-normal table patterns, including symmetry, complements, intervals, and tail unions.
│   ├── G10_T3_L4_C8C9C10_activity.tex            # Student Learning Evidence 4 brief requiring an HTML/CSS/JavaScript modeling webpage, AI-development evidence, deployment, and a statistical report.
│   ├── G10_T3_L4_C8C9C10_dataset_1.csv           # C9 test data: 30 measurements labeled as a uniform-like process (12.4–26.3).
│   ├── G10_T3_L4_C8C9C10_dataset_2.csv           # C9 test data: 30 measurements labeled as a triangular-like process (5.2–20.3), concentrated near the middle.
│   └── G10_T3_L4_C8C9C10_dataset_3.csv           # C9 test data: 30 measurements labeled as a normal-like process (42.1–65.2), centered in the mid-50s.
├── 3-catch_ups/                                   # Remedial C5–C7 assessment material and its teacher solution companion.
│   ├── G10_T3_C5C6C7_catch_up.tex                # Student catch-up sheet on standard-normal probabilities, contextual standardization, and inverse-normal cutoffs/intervals.
│   └── G10_T3_C5C6C7_catch_upsolutions.tex       # Teacher solutions for the catch-up sheet, with full calculations, distribution graphs, and a minimal-answer recap.
└── 4-extra_material/                              # Standalone student reference material supplementing the normal-distribution work.
    └── normal-table.tex                           # Printable standard-normal reference sheet with table-reading directions, identities, a shaded curve, and Φ values through z = 3.09.
```

## Resource roles

- **Student-facing pages/materials:** the practice activities, context article, assessment sheets, catch-up sheet, project brief, datasets, and normal-table reference are intended for learners. In this repository they are printable LaTeX sources rather than web pages.
- **Teacher materials:** files containing `solution`/`solutions` provide answer keys or worked derivations. `G10_T3_summary.tex` is explicitly a pedagogical review rather than student exercises.
- **Lesson and assessment resources:** `1-practice_activities/` develops criteria C0–C7 and also contains consolidated C1–C10 material; `2-learning_evidences/` holds formal or practice assessment variants; `3-catch_ups/` provides remediation.
- **Stylesheets and JavaScript:** none are stored here. The C8–C10 brief requires students to create HTML, CSS, and JavaScript, but those deliverables are not part of this directory.
- **Images and media:** no image file is stored here. Several assessment sources request a shared `logo.png` outside this subtree or through the shared LaTeX search path; graphs are generated in LaTeX with TikZ/PGFPlots or shared graph macros.
- **Data and configuration:** the three CSV files are the only local datasets. There are no local configuration files.
- **Downloadable documents:** no compiled PDF or office-document download is checked in; the `.tex` files are sources from which printable documents can be built.
- **Generated/build files:** none are present or inventoried.

## Important relationships

- Nearly every LaTeX document imports a shared preamble (`preamble_exams.tex` or `preamble.tex`) using relative search paths. Those shared files live outside `term_3` and supply document classes, packages, layout commands, and assessment helpers; the two `G10_T3_MATERIAL*.tex` files directly input `../../../preamble/preamble_exams.tex`.
- C4–C7 assessments and solution sets also import shared graph libraries such as `graphs/probability_distribution_graphs.tex`, `graphs/normal_distribution_graphs.tex`, and `graphs/uniform_linear_probability_distributions.tex`. These external macro files generate reusable uniform, triangular, and normal plots; they are not assets contained in this tree.
- Assessment headers in the midterm, C1–C4 exams, and catch-up sheet reference `logo.png` through the preamble/graphics search paths. The C8–C10 activity instead checks `../../../preamble/logo.png` explicitly and displays a placeholder if it is unavailable. No local copy of the logo exists.
- `G10_T3_C1C7_midterm_solution.tex` corresponds to `G10_T3_C1C7_midterm.tex`; their `V2` counterparts form the alternate pair. V2 changes actual model bounds, means/spreads, wording, and layout—not merely the filename.
- `G10_T3_L1_C4_exam_solution.tex` and `G10_T3_L1_C4_exam_solution_long.tex` both answer the original C4 exam: the former is a compact grouped key, while the latter gives full per-question explanations. `G10_T3_L1_C4_examV2_solution.tex` is specifically paired with the numerically different V2 practice exam.
- `G10_T3_C5C6C7_catch_upsolutions.tex` is the worked companion to `G10_T3_C5C6C7_catch_up.tex`; both cover the same three criteria, while the solution source additionally loads shared graph macros.
- The C8–C10 activity instructs students to build a separate interactive webpage. Its C9 data-modeling mode is expected to accept all three adjacent CSV datasets, estimate a suitable uniform/triangular/normal model, and compare a fitted PDF with an empirical histogram. No resulting HTML, CSS, JavaScript, report, or deployed-site configuration is included here.
- `normal-table.tex` supports the standard-normal work in C5–C7 as a standalone printable reference. Some practice and solution documents embed their own shorter Φ tables, so they do not directly `input` this file.
- `G10_T3_MATERIAL_V2.tex` is a substantive pedagogical revision of `G10_T3_MATERIAL.tex`: it preserves the C1–C10 collection structure while changing early continuous-density solutions to geometry-based methods and replacing at least one nonlinear model with a piecewise-constant one.

## Verification notes

- Every item could be identified confidently from its contents; **no entry requires manual verification**.
- No transient or generated item was present in the tree. In particular, there were no `.DS_Store`, editor-cache, compiler-auxiliary, temporary, dependency, compiled PDF, or LaTeX build-output files to exclude.
