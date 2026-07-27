# Grade 10 — Term 1 Structure

## Overview

`term_1` is a LaTeX source collection for a Grade 10 Global Economics unit on decision analysis. It progresses from C1–C2 practice (identifying decision components and constructing payoff tables), through C1–C10 assessments and worked solutions, to criterion-specific recovery activities and supplementary material. Files described as **student-facing** are worksheets, assessments, or briefs intended to receive student work; files described as **teacher material** expose worked answers or instructional solution sets. There are no local HTML pages, stylesheets, JavaScript programs, datasets, configuration files, or standalone media: the JavaScript item is a student project *brief*, not an implementation.

## Directory tree

```text
.
├── 1-practice_activities/                                      # Student practice and an instructor-facing contents summary for Lesson 1 decision components/payoff tables.
│   ├── G10_T1_L1_C1-C2_practice_activity1.tex                  # Student-facing C1–C2 workbook: 21 scenarios spanning direct, variable, fixed, and hybrid payoff models, with guided interpretations and computed tables.
│   ├── G10_T1_L1_C1-C2_practice_activity2 - Copy.tex           # Compact alternate/legacy Activity 2: 14 terse scenario notes and partial calculations based largely on Activity 1 contexts; unlike the full Activity 2, it is not a nine-problem worked worksheet.
│   ├── G10_T1_L1_C1-C2_practice_activity2.tex                  # Student-facing worked C1–C2 activity with nine new contexts (food truck through emergency supplies), each identifying decision elements and building a payoff table.
│   └── G10_T1_summary.tex                                      # Teacher/contributor summary that inventories the modeling categories and scenario counts in the two Lesson 1 practice activities.
├── 2-learning_evidences/                                       # Student assessments/project briefs and paired teacher solution documents for Lessons 1–3.
│   ├── G10_T1_L1_exam.tex                                      # Student-facing Learning Evidence 1 exam: three decision problems assessing C1–C5 via payoff tables, expected value, maximax, and maximin.
│   ├── G10_T1_L1_exam_solution.tex                             # Teacher material with full C1–C5 workings for the exam’s cafeteria, delivery-cooperative, and sports-center problems.
│   ├── G10_T1_L1_practice_exam.tex                             # Student-facing two-problem C1–C5 practice exam on recreation-center memberships and fundraiser menu plans.
│   ├── G10_T1_L1_practice_exam_solution.tex                    # Teacher material with complete decision-component, payoff, maximax, maximin, and expected-value solutions to that practice exam.
│   ├── G10_T1_L2_C6_activity.tex                               # Student-facing four-problem C6 activity applying maximum opportunity/minimax regret to bakery, farm-storage, theater, and another payoff-table case.
│   ├── G10_T1_L2_C6_activity_solution.tex                      # Teacher material giving full and abbreviated minimax-regret solutions for the four C6 problems.
│   ├── G10_T1_L2_C7_activity.tex                               # Student-facing ten-problem C7 expected-value activity, from one-project choices to multi-alternative and joint-state decisions.
│   ├── G10_T1_L2_C7_activity_solution.tex                      # Teacher material with worked expected-value analysis for all ten C7 activity problems.
│   ├── G10_T1_L2_midterm.tex                                   # Student-facing Lesson 2 midterm assessing C1–C7 across payoff construction, classical criteria, regret, and expected-value problems.
│   ├── G10_T1_L2_midterm_solution.tex                          # Teacher material with worked solutions to eight midterm scenarios, including bakery, shipping, theater, inventory, routing, marketing, production, and zoning choices.
│   ├── G10_T1_L2_mock_midterm.tex                              # Student-facing mock midterm for C1–C7; uses a smaller alternate set of logistics, inventory, routing, production, and zoning problems.
│   ├── G10_T1_L2_mock_midterm_solution.tex                     # Teacher material with full solutions for the mock midterm’s five scenarios.
│   ├── G10_T1_L3_proyect.tex                                   # Student-facing project brief requiring a JavaScript decision-analysis tool, presentation, and decision-tree defense for C8–C10; includes specifications and solved examples, but no JavaScript source.
│   ├── G10_T1_L3_proyect_problems.tex                          # Student-facing bank of ten project datasets/tasks for comparing Bayes, Maximin, and Minimax Regret and constructing decision trees.
│   ├── G10_T1_L3_proyect_problems_solutions.tex                # Teacher material with extensive worked C8/C9 solutions and C10 evidence guidance for all ten project problems.
│   └── G10_T1_L3_proyect_problems_solutions_min.tex            # Teacher-facing condensed solution variant: shorter calculations/recommendations for the same ten project problems rather than the full explanatory treatment.
├── 3-catch_ups/                                                 # Criterion-by-criterion recovery worksheets (student-facing) and their teacher answer keys for C1–C7.
│   ├── G10_T1_C1_catchUp.tex                                   # Student-facing ten-problem C1 recovery activity on formulating choices under uncertainty and using expected value.
│   ├── G10_T1_C1_catchUp_soution.tex                           # Teacher answer key for C1, with expected-value computations and recommendations (`soution` is the stored filename).
│   ├── G10_T1_C2_catchUp.tex                                   # Student-facing ten-problem C2 recovery activity identifying alternatives, events, consequences, and states of nature.
│   ├── G10_T1_C2_catchUp_soution.tex                           # Teacher answer key supplying the C2 decision-component interpretations (`soution` is the stored filename).
│   ├── G10_T1_C3_catchUp.tex                                   # Student-facing ten-problem C3 recovery activity for turning narrative and supplied data into payoff tables.
│   ├── G10_T1_C3_catchUp_soution.tex                           # Teacher answer key with constructed payoff tables and supporting calculations for C3 (`soution` is the stored filename).
│   ├── G10_T1_C4_catchUp.tex                                   # Student-facing ten-problem C4 recovery worksheet applying the optimistic maximax rule without probabilities.
│   ├── G10_T1_C4_catchUp_soution.tex                           # Teacher key showing each row maximum and maximax choice for C4 (`soution` is the stored filename).
│   ├── G10_T1_C5_catchUp.tex                                   # Student-facing ten-problem C5 recovery worksheet applying the conservative maximin rule without probabilities.
│   ├── G10_T1_C5_catchUp_solution.tex                          # Teacher key showing each row minimum and maximin recommendation for C5.
│   ├── G10_T1_C6_catchUp.tex                                   # Student-facing ten-problem C6 recovery worksheet using maximum opportunity/minimax regret.
│   ├── G10_T1_C6_catchUp_soution.tex                           # Teacher key with regret tables and minimum-of-maximum-regret choices for C6 (`soution` is the stored filename).
│   ├── G10_T1_C7_catchUp.tex                                   # Student-facing ten-problem C7 recovery activity comparing alternatives with probabilities and expected value.
│   └── G10_T1_C7_catchUp_solution.tex                          # Teacher key with worked expected values for the ten C7 scenarios.
└── 4-extra_material/                                            # Supplementary exercises, alternate/reference answers, and worked enrichment material for Lessons 1–3.
    ├── G10_T1_L1_V2_solution.tex                               # Teacher material: alternate C1–C5 exam solution version with changed state sets/probabilities and expanded alternatives relative to the main Lesson 1 exam key.
    ├── G10_T1_L1_supplementary.tex                             # Student-facing five-problem C1–C5 supplementary assessment (smoothie, shirts, streaming, courier, and water-utility decisions).
    ├── G10_T1_L1_supplementary_hard_solution.tex               # Teacher material for a harder parallel five-problem set (coffee cart, bookstore, meal subscriptions, and more complex joint-state cases), not the direct key to the student supplementary sheet.
    ├── G10_T1_L1_supplementary_solution.tex                    # Teacher key matching the standard supplementary contexts and providing full C1–C5 calculations.
    ├── G10_T1_L2_C6_activity_supplementary.tex                 # Student-facing seven-problem supplementary C6 assessment using increasingly large minimax-regret payoff tables.
    ├── G10_T1_L2_C6_activity_supplementary_solution.tex        # Teacher key with state maxima, regret tables, and minimax-regret choices for those seven C6 problems.
    ├── G10_T1_L2_MATERIAL.tex                                  # Teacher/instructional worked set combining four C6 minimax-regret examples and ten C7 expected-value examples, with cross-criterion comparisons.
    ├── G10_T1_L2_reference_midterm.tex                         # Teacher reference solution set for C1–C7, organized around café, cafeteria, logistics, investment, production, bookstore, and related decisions; it is not a blank student midterm.
    └── G10_T1_L3_MATERIAL.tex                                  # Teacher/instructional worked Lesson 3 material for C8 method comparison, C9 staged decision trees, and C10 end-to-end analysis.
```

## Important relationships

* All entries are standalone LaTeX documents. Solution files are teacher companions to the like-named student assessment/activity unless a different relationship is explicitly noted above; none is loaded by another file in this directory.
* Most solution, supplementary, and material documents load the shared `preamble/preamble_exams.tex` located outside `term_1`. Catch-up keys reach it with `../../../preamble/preamble_exams.tex`; most other keys/materials use `../../preamble/preamble_exams.tex`.
* The practice activities and summary load the external shared `preamble.tex` through a multi-directory `\input@path`. Activity 2, its compact copy, and the summary additionally load three shared graph-macro files: `graphs/uniform_linear_probability_distributions.tex`, `graphs/probability_distribution_graphs.tex`, and `graphs/normal_distribution_graphs.tex`. They define reusable graph commands; no graph image files are stored here.
* Student assessment sheets that define their own page layout embed the shared `preamble/logo.png` via relative paths. There are no images or other media physically inside `term_1`.
* `G10_T1_L3_proyect.tex` specifies interactive web-page elements and JavaScript functions as student deliverables. The directory contains no HTML, CSS, or JavaScript implementation to which the brief links.
* `G10_T1_L3_proyect_problems.tex` supplies the ten datasets/tasks used by the full and minimal project solution documents. `G10_T1_L3_MATERIAL.tex` is separate worked enrichment rather than a generated build artifact.
* No generated LaTeX outputs (`.aux`, `.log`, `.out`, `.toc`, or PDFs), dependency directories, editor caches, or meaningful hidden files are present. `STRUCTURE.md` is intentionally omitted from the inventory tree because it is this inventory document.

## Classification summary

* **Student-facing pages/documents:** blank activities, exams, midterms, catch-ups, supplementary worksheets, and project briefs/problem banks identified above.
* **Teacher materials:** all worked `solution`/`soution` files, reference/material sets, and the practice summary.
* **Stylesheets / JavaScript / data / configuration / local media:** none present. LaTeX preambles, graph definitions, and the logo are shared dependencies outside this directory.
* **Generated or build-related files:** none present.
