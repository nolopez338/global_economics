# Book folder rename verification

The teaching collection is now `book/`. URL prefixes, filenames, query strings and anchors were retained.

- 2,892 original files accounted for; missing files: 0.
- The old directory no longer exists.
- 159 text files and 11 compressed LaTeX source maps updated.
- 342 PDFs inspected; seven updated. Six retain pixel-identical pages. Only page 8 of `book/grade11/term_2/STRUCTURE.pdf` changes visually, to shorten two printed paths.
- Six Excel workbooks updated: five source-note cells and one stored cloud-origin path. Every other ZIP entry is byte-identical; formulas, cached values, styles and native workbook features are preserved.
- Test fingerprints were refreshed only after verifying the former URL spelling reproduced the previous hashes.
- 2,814 affected reference occurrences checked; 2,273 resolved locally.
- Remaining literal references outside Git metadata: 0.

Published URLs were mapped to files in this checkout; live deployment availability was not checked. The stored `https://d.docs.live.net/` cloud-origin URL in `book/olympiad/Cambridge/2026-cambridge-stage4.xlsx` was updated, but the remote cloud copy was not checked. Missing targets below were absent at their former paths too. Filenames and historical folder numbering were preserved.

## References requiring attention

| Result | Target | First source | Occurrences |
|---|---|---|---|
| example path; not checked | `book/preamble/sections.tex` | `.agents/skills/global-economics-readme/references/workflow.md:29` | 1 |
| missing before rename | `book/grade10/term_1/1-practice_activities/G10_T1_L1_C1C2_practice_activity1-alternate-descriptions.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:679` | 1 |
| missing before rename | `book/grade10/term_1/1-practice_activities/G10_T1_L1_C1C2_practice_activity1.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:680` | 1 |
| missing before rename | `book/grade10/term_1/1-practice_activities/G10_T1_L1_C1C3_practice_activity2-alternate-descriptions.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:681` | 1 |
| missing before rename | `book/grade10/term_1/1-practice_activities/G10_T1_L1_C1C3_practice_activity2.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:682` | 1 |
| missing before rename | `book/grade10/term_1/1-practice_activities/G10_T1_L2_C4C5_practice_activity3.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:683` | 3 |
| missing before rename | `book/grade10/term_1/1-practice_activities/G10_T1_L2_C6C7_practice_activity4.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:684` | 1 |
| missing before rename | `book/grade10/term_1/4-extra_material/G10_T1_C1C2_practice_activity1_print1_solved.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:696` | 22 |
| missing before rename | `book/grade10/term_1/4-extra_material/G10_T1_C1C3_practice_activity2_print1_solved.pdf` | `teacher/assets/js/databases/materials-data-base.js:88` | 9 |
| missing before rename | `book/grade10/term_1/4-extra_material/G10_T1_survey.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:697` | 1 |
| missing before rename | `book/grade10/term_1/PGF-02-R39_G10_Global_T1_2026-2027-plain.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:673` | 1 |
| missing before rename | `book/grade10/term_1/PGF-02-R39_G10_Global_T1_2026-2027.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:674` | 1 |
| missing before rename | `book/grade10/term_1/STRUCTURE.pdf` | `book/grade10/term_1/5-extra_material/PGF-02-R39_G10_Global_T1_2026-2027-plain.tex:675` | 1 |
| missing before rename | `book/grade10/term_2/1-practice_activities/G10_T2_L3_C10_practice_activity.pdf` | `teacher/assets/js/databases/materials-data-base.js:594` | 7 |
| missing before rename | `book/grade10/term_2/2-class_activities/G10_T2_L1_C4_classroom_activity.pdf` | `grade10/src/G10_T2.html:217` | 9 |
| missing before rename | `book/grade10/term_2/2-class_activities/G10_T2_L2_C5_classroom_activity.pdf` | `grade10/src/G10_T2.html:260` | 9 |
| missing before rename | `book/grade10/term_2/2-class_activities/G10_T2_L2_C6_classroom_activity.pdf` | `grade10/src/G10_T2.html:283` | 9 |
| missing before rename | `book/grade10/term_2/2-class_activities/G10_T2_L2_C7_classroom_activity.pdf` | `grade10/src/G10_T2.html:306` | 9 |
| missing before rename | `book/grade10/term_2/2-class_activities/G10_T2_L3_C10_classroom_activity.pdf` | `teacher/assets/js/databases/materials-data-base.js:606` | 7 |
| missing before rename | `book/grade10/term_2/2-class_activities/G10_T2_L3_C8_classroom_activity.pdf` | `grade10/src/G10_T2.html:349` | 9 |
| missing before rename | `book/grade10/term_2/2-class_activities/G10_T2_L3_C9_classroom_activity.pdf` | `grade10/src/G10_T2.html:372` | 9 |
| missing before rename | `book/grade10/term_2/3-slides/G10_T2_L1_C4_slides.pdf` | `grade10/src/G10_T2.html:213` | 9 |
| missing before rename | `book/grade10/term_2/3-slides/G10_T2_L2_C5_slides.pdf` | `grade10/src/G10_T2.html:256` | 9 |
| missing before rename | `book/grade10/term_2/3-slides/G10_T2_L2_C6_slides.pdf` | `grade10/src/G10_T2.html:279` | 9 |
| missing before rename | `book/grade10/term_2/3-slides/G10_T2_L2_C7_slides.pdf` | `grade10/src/G10_T2.html:302` | 9 |
| missing before rename | `book/grade10/term_2/3-slides/G10_T2_L3_C10_slides.pdf` | `teacher/assets/js/databases/materials-data-base.js:600` | 7 |
| missing before rename | `book/grade10/term_2/3-slides/G10_T2_L3_C8_slides.pdf` | `grade10/src/G10_T2.html:345` | 9 |
| missing before rename | `book/grade10/term_2/3-slides/G10_T2_L3_C9_slides.pdf` | `grade10/src/G10_T2.html:368` | 9 |
| missing before rename | `book/grade10/term_2/4-learning_evidences/G10_T2_L1_C3C4_exam.pdf` | `teacher/assets/js/databases/materials-data-base.js:426` | 7 |
| missing before rename | `book/grade10/term_2/4-learning_evidences/G10_T2_L1_C3C4_exam_solution.pdf` | `teacher/assets/js/databases/materials-data-base.js:432` | 7 |
| missing before rename | `book/grade10/term_2/4-learning_evidences/G10_T2_L2_C5C6C7_exam.pdf` | `teacher/assets/js/databases/materials-data-base.js:519` | 7 |
| missing before rename | `book/grade10/term_2/4-learning_evidences/G10_T2_L2_C5C6C7_exam_solution.pdf` | `teacher/assets/js/databases/materials-data-base.js:525` | 7 |
| missing before rename | `book/grade10/term_2/4-learning_evidences/G10_T2_L3_C8C9C10_exam.pdf` | `teacher/assets/js/databases/materials-data-base.js:612` | 7 |
| missing before rename | `book/grade10/term_2/4-learning_evidences/G10_T2_L3_C8C9C10_exam_solution.pdf` | `teacher/assets/js/databases/materials-data-base.js:618` | 7 |
| missing before rename | `book/grade10/term_2/5-extra_material/G10_T1_outline.pdf` | `grade10/src/G10_T1.html:27` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L1_C2_practice_activity.pdf` | `grade10/src/G10_T3.html:152` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L1_C3_practice_activity.pdf` | `grade10/src/G10_T3.html:175` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L1_C4_practice_activity.pdf` | `grade10/src/G10_T3.html:198` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L2_C5_practice_activity.pdf` | `grade10/src/G10_T3.html:246` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L2_C6_practice_activity.pdf` | `grade10/src/G10_T3.html:269` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L2_C7_practice_activity.pdf` | `grade10/src/G10_T3.html:292` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L3_C10_practice_activity.pdf` | `grade10/src/G10_T3.html:381` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L3_C8_practice_activity.pdf` | `grade10/src/G10_T3.html:335` | 2 |
| missing before rename | `book/grade10/term_3/1-practice_activities/G10_T3_L3_C9_practice_activity.pdf` | `grade10/src/G10_T3.html:358` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L1_C1_classroom_activity.pdf` | `grade10/src/G10_T3.html:125` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L1_C2_classroom_activity.pdf` | `grade10/src/G10_T3.html:148` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L1_C3_classroom_activity.pdf` | `grade10/src/G10_T3.html:171` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L1_C4_classroom_activity.pdf` | `grade10/src/G10_T3.html:194` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L2_C5_classroom_activity.pdf` | `grade10/src/G10_T3.html:242` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L2_C6_classroom_activity.pdf` | `grade10/src/G10_T3.html:265` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L2_C7_classroom_activity.pdf` | `grade10/src/G10_T3.html:288` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L3_C10_classroom_activity.pdf` | `grade10/src/G10_T3.html:377` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L3_C8_classroom_activity.pdf` | `grade10/src/G10_T3.html:331` | 2 |
| missing before rename | `book/grade10/term_3/2-class_activities/G10_T3_L3_C9_classroom_activity.pdf` | `grade10/src/G10_T3.html:354` | 2 |
| missing before rename | `book/grade10/term_3/3-learning_evidences/` | `book/grade11/term_1/README.md:164` | 1 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L1_C1_slides.pdf` | `grade10/src/G10_T3.html:121` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L1_C2_slides.pdf` | `grade10/src/G10_T3.html:144` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L1_C3_slides.pdf` | `grade10/src/G10_T3.html:167` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L1_C4_slides.pdf` | `grade10/src/G10_T3.html:190` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L2_C5_slides.pdf` | `grade10/src/G10_T3.html:238` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L2_C6_slides.pdf` | `grade10/src/G10_T3.html:261` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L2_C7_slides.pdf` | `grade10/src/G10_T3.html:284` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L3_C10_slides.pdf` | `grade10/src/G10_T3.html:373` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L3_C8_slides.pdf` | `grade10/src/G10_T3.html:327` | 2 |
| missing before rename | `book/grade10/term_3/3-slides/G10_T3_L3_C9_slides.pdf` | `grade10/src/G10_T3.html:350` | 2 |
| missing before rename | `book/grade10/term_3/5-extra_material/G10_T3_outline.pdf` | `grade10/src/G10_T3.html:25` | 2 |
| missing before rename | `book/grade11/term_1/1-practice_activities/G11_T1_C1_practice_activity1.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:206` | 8 |
| missing before rename | `book/grade11/term_1/1-practice_activities/G11_T1_C1_practice_activity1_print0.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:207` | 2 |
| missing before rename | `book/grade11/term_1/1-practice_activities/G11_T1_C1_practice_activity1_print1.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:208` | 2 |
| missing before rename | `book/grade11/term_1/1-practice_activities/G11_T1_C2_practice_activity2.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:209` | 12 |
| missing before rename | `book/grade11/term_1/2-learning_evidences/G11_T1_C1C2C3C4_exam0_solution.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:215` | 2 |
| missing before rename | `book/grade11/term_1/2-learning_evidences/G11_T3_C1C7_midterm_solution.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:216` | 2 |
| missing before rename | `book/grade11/term_1/4-extra_material/G11_T1_C1_practice_activity1_print1.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:220` | 2 |
| missing before rename | `book/grade11/term_1/4-extra_material/G11_T1_C1_practice_activity1_print1_solved.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:221` | 2 |
| missing before rename | `book/grade11/term_1/4-extra_material/normal-table.pdf` | `book/grade11/term_1/PGF-02-R39_G11_Global_T1_2026-2027-plain.tex:222` | 2 |
| missing before rename | `book/grade11/term_2/2-class_activities/G11_T2_L2_C5_classroom_activity.pdf` | `grade11/src/G11_T2.html:295` | 9 |
| missing before rename | `book/grade11/term_2/2-class_activities/G11_T2_L2_C6_classroom_activity.pdf` | `grade11/src/G11_T2.html:318` | 9 |
| missing before rename | `book/grade11/term_2/2-class_activities/G11_T2_L2_C7_classroom_activity.pdf` | `grade11/src/G11_T2.html:341` | 9 |
| missing before rename | `book/grade11/term_2/2-class_activities/G11_T2_L3_C10_classroom_activity.pdf` | `grade11/src/G11_T2.html:439` | 9 |
| missing before rename | `book/grade11/term_2/2-class_activities/G11_T2_L3_C8_classroom_activity.pdf` | `grade11/src/G11_T2.html:393` | 9 |
| missing before rename | `book/grade11/term_2/2-class_activities/G11_T2_L3_C9_classroom_activity.pdf` | `grade11/src/G11_T2.html:416` | 9 |
| missing before rename | `book/grade11/term_2/3-slides/G11_T2_L1_C4_slides.pdf` | `grade11/src/G11_T2.html:239` | 9 |
| missing before rename | `book/grade11/term_2/3-slides/G11_T2_L2_C5_slides.pdf` | `grade11/src/G11_T2.html:291` | 9 |
| missing before rename | `book/grade11/term_2/3-slides/G11_T2_L2_C6_slides.pdf` | `grade11/src/G11_T2.html:314` | 9 |
| missing before rename | `book/grade11/term_2/3-slides/G11_T2_L2_C7_slides.pdf` | `grade11/src/G11_T2.html:337` | 9 |
| missing before rename | `book/grade11/term_2/3-slides/G11_T2_L3_C10_slides.pdf` | `grade11/src/G11_T2.html:435` | 9 |
| missing before rename | `book/grade11/term_2/3-slides/G11_T2_L3_C8_slides.pdf` | `grade11/src/G11_T2.html:389` | 9 |
| missing before rename | `book/grade11/term_2/3-slides/G11_T2_L3_C9_slides.pdf` | `grade11/src/G11_T2.html:412` | 9 |
| missing before rename | `book/grade11/term_2/4-learning_evidences/G11_T2_L1_C3C4_exam.pdf` | `teacher/assets/js/databases/materials-data-base.js:1326` | 7 |
| missing before rename | `book/grade11/term_2/4-learning_evidences/G11_T2_L1_C3C4_exam_solution.pdf` | `teacher/assets/js/databases/materials-data-base.js:1332` | 7 |
| missing before rename | `book/grade11/term_2/4-learning_evidences/G11_T2_L2_C5C6C7_exam.pdf` | `teacher/assets/js/databases/materials-data-base.js:1419` | 7 |
| missing before rename | `book/grade11/term_2/4-learning_evidences/G11_T2_L2_C5C6C7_exam_solution.pdf` | `teacher/assets/js/databases/materials-data-base.js:1425` | 7 |
| missing before rename | `book/grade11/term_2/4-learning_evidences/G11_T2_L3_C8C9C10_exam.pdf` | `teacher/assets/js/databases/materials-data-base.js:1512` | 7 |
| missing before rename | `book/grade11/term_2/4-learning_evidences/G11_T2_L3_C8C9C10_exam_solution.pdf` | `teacher/assets/js/databases/materials-data-base.js:1518` | 7 |
| missing before rename | `book/grade11/term_2/5-extra_material/G11_T1_outline.pdf` | `grade11/src/G11_T1.html:26` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L1_C1_practice.pdf` | `grade11/src/G11_T3.html:127` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L1_C2_practice.pdf` | `grade11/src/G11_T3.html:150` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L1_C3_practice.pdf` | `grade11/src/G11_T3.html:173` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L1_C4_practice.pdf` | `grade11/src/G11_T3.html:196` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L2_C5_practice.pdf` | `grade11/src/G11_T3.html:248` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L2_C6_practice.pdf` | `grade11/src/G11_T3.html:271` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L2_C7_practice.pdf` | `grade11/src/G11_T3.html:294` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L3_C10_practice.pdf` | `grade11/src/G11_T3.html:394` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L3_C8_practice.pdf` | `grade11/src/G11_T3.html:348` | 2 |
| missing before rename | `book/grade11/term_3/1-practice_activities/G11_T3_L3_C9_practice.pdf` | `grade11/src/G11_T3.html:371` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L1_C1_classroom_activity.pdf` | `grade11/src/G11_T3.html:123` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L1_C2_classroom_activity.pdf` | `grade11/src/G11_T3.html:146` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L1_C3_classroom_activity.pdf` | `grade11/src/G11_T3.html:169` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L1_C4_classroom_activity.pdf` | `grade11/src/G11_T3.html:192` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L2_C5_classroom_activity.pdf` | `grade11/src/G11_T3.html:244` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L2_C6_classroom_activity.pdf` | `grade11/src/G11_T3.html:267` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L2_C7_classroom_activity.pdf` | `grade11/src/G11_T3.html:290` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L3_C10_classroom_activity.pdf` | `grade11/src/G11_T3.html:390` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L3_C8_classroom_activity.pdf` | `grade11/src/G11_T3.html:344` | 2 |
| missing before rename | `book/grade11/term_3/2-class_activities/G11_T3_L3_C9_classroom_activity.pdf` | `grade11/src/G11_T3.html:367` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L1_C1_slides.pdf` | `grade11/src/G11_T3.html:119` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L1_C2_slides.pdf` | `grade11/src/G11_T3.html:142` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L1_C3_slides.pdf` | `grade11/src/G11_T3.html:165` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L1_C4_slides.pdf` | `grade11/src/G11_T3.html:188` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L2_C5_slides.pdf` | `grade11/src/G11_T3.html:240` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L2_C6_slides.pdf` | `grade11/src/G11_T3.html:263` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L2_C7_slides.pdf` | `grade11/src/G11_T3.html:286` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L3_C10_slides.pdf` | `grade11/src/G11_T3.html:386` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L3_C8_slides.pdf` | `grade11/src/G11_T3.html:340` | 2 |
| missing before rename | `book/grade11/term_3/3-slides/G11_T3_L3_C9_slides.pdf` | `grade11/src/G11_T3.html:363` | 2 |
| missing before rename | `book/grade11/term_3/5-extra_material/G11_T3_outline.pdf` | `grade11/src/G11_T3.html:23` | 2 |
| missing before rename | `book/preamble/Global_Economics_cover_artwork_irregular.png` | `book/preamble/global_economics_cover.tex:29` | 1 |
| missing before rename | `book/preamble/Global_Economics_cover_tex.tex` | `book/preamble/global_economics_cover.tex:14` | 1 |
| optional LaTeX search path absent | `../../book/preamble` | `book/preamble/preamble_exams.tex:10` | 1 |
| template or dynamic path; not checked | `book/grade$` | `teacher/authoring/tests/materials-workflow.test.js:261` | 2 |
| template or dynamic path; not checked | `teacher/authoring/book/grade$` | `teacher/authoring/tests/materials-workflow.test.js:270` | 1 |

## Validation

- Schedule generation consistency check: passed for all four datasets.
- Materials validator: all 522 dated and 140 base records valid; no duplicate keys. Existing empty-material warnings remain.
- Math and slide checks: passed.
- Authoring tests: 45 of 46 pass. The existing calendar CSS test fails because `.cycle-day.term-3` lacks the expected `--term-3-code` color rule. The CSS and this test are unchanged from HEAD.
- No commit or push performed.

## Final preservation audit

- All 2,892 original files remain present. The tracked-file audit verified 2,805 files against HEAD, allowing only folder replacements, the verified PDF changes, the six package-preserving workbook updates, and four URL-dependent snapshot files.
- Existing unrelated teacher deletions and untracked work were retained.
- Final scan covered 342 PDFs (including compressed objects), 16 ZIP/Office packages, compressed LaTeX maps, case variants and UTF-16 strings. No former-folder references remain outside Git metadata.
- 127 distinct concrete targets were already missing. They are listed above; no missing resources were fabricated and no filenames were changed.
- Five spreadsheet source-note cells were verified with the bundled spreadsheet library and rendered for inspection. The sixth workbook change affects only its stored cloud-origin path.
