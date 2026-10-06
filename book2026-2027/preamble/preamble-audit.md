# Preamble command audit

Scope: the current working-tree versions of `G11_T1_L1_C1C2C3C4_examV2.tex`, `G11_T1_L1_C1C2C3C4_examV2_solution.tex`, and `G11_T1_C6C7_practice_activity.tex` in Grade 11, Term 1. Classification is relative to this reference set, not to every document in the repository.

## General layer

| Definitions | Decision and dependency evidence |
|---|---|
| `secInicio`, `SectionProblemsTableOfContents`, `SectionProblemLink`, `sml`, `score`, `sectionScored`, `boxed`, `QuestionsTasks` | Retained: called directly by the reference documents. |
| `secInicioIcon`, `secInicioIconMultiplier`, `ifSimpleSecInicio`, generated `SimpleSecIniciotrue` / `SimpleSecIniciofalse`, and initial false setting | Retained: navigation depends on the icon, its scale, and both conditional branches. |
| `CriterionTask`, `TaskHyperref` | Retained: `QuestionsTasks` emits criterion tasks, which use colored internal links. |
| `l_questions_tasks_entry_seq`; `l_questions_tasks_criterion_tl`, `l_questions_tasks_label_tl`, `l_questions_tasks_description_tl`, `l_questions_tasks_navigation_tl`; `questions_tasks_emit:nnn`, generated `questions_tasks_emit:VVV`, `questions_tasks_navigation:n` | Retained: complete parsing, emission, and navigation dependency chain for `QuestionsTasks`, including the surrounding expl3 syntax switches. |
| `TOCScoredTitle` | Retained: used by `sectionScored`; it also calls `score`. |
| `OriginalTableOfContents`, redefined `tableofcontents`, begin-document hook | Retained: both non-exam references use the table of contents; the hook preserves its link coloring after tocloft initialization. |
| Colors `links`, `links2`, `links3`, `tocLinkDark`, `darkgold`, `darkred`, `taskLinkDarkBlue` | Retained: navigation, hyperlink configuration, contents, problem tables, and task links depend on them. |
| `arraystretch` redefinition | Retained: global table formatting used by the reference documents. |
| Boolean `explicaciones`, `explicacion`, `mostrarExplicaciones` | Archived together: no reference usage or retained-command dependency. |
| Colors `popUp`, `popUpIn`, `backgroundC`, `backgroundCC`, `borders`, `padding` | Archived: used only by archived definitions, or unused in the reference dependency set. |
| mdframed styles `estiloGeneral`, `code`; `fboxC`, `cuadro`; listings style `python` | Archived: unused styles and framing commands, with supporting custom colors preserved in the same archive. |
| `bigLink`, `smallLink`, `bfLink`, `smallUrl`, `subSecLink` | Archived: no reference usage; framed variants retain `fboxC` in the archive. |
| `background`, `backgroundC`, `anchoPag`, `esp` | Archived: no reference usage or retained-command dependency. The color and command named `backgroundC` are distinct definitions; both were preserved. |
| `espacioImagenes`, `fig`, `ffig`, `hfig`, `hffig`, `linkExplicacion` | Archived: complete image-helper chain, including `linkExplicacion` → `hffig`, image offsets, frame, and color dependencies. |

The archived general definitions are in `preamble-unused.tex`, in their original relative order, with their source definitions and associated comments unchanged. Packages and global page, list, graphics, hyperlink, and frame configuration remain active.

## Exam layer

| Definitions | Decision and dependency evidence |
|---|---|
| `ExamHeader`, `StudentInfo`, `LearningObjective`, `SubsectionBox` | Retained: directly used by the exam reference. |
| `CellCenter`, column type `C` | Retained: required by `ExamHeader`. |
| `YColumnWidth`, `setYColumnWidth`, default width initialization, column types `Y` and `Z` | Retained: required by `LearningObjective`. |
| `alphenum` environment and its enumitem configuration | Archived together in `preamble_exams-unused.tex`: not used by the reference set. |
| `input@path`, table spacing, `arraystretch`, itemize/enumerate configuration | Retained: file resolution and exam layout configuration. |

Inheritance remains `preamble_exams.tex` → `preamble_G10_T1_C2C3.tex` → `preamble.tex`. The intermediate module's `DecisionElementsTable` and its expl3 helpers were inspected and left unchanged: they belong to an external module, not either audited file. The graph modules loaded by the solution and practice references were also checked for dependencies on removed definitions and left unchanged.

## Validation

Each reference was compiled with pdfLaTeX three times before and after the reorganization, in separate temporary output directories. Baselines used the user's existing local edits, not the Git versions. No reference source or existing PDF was changed by validation.

| Reference | Pages | Build | Render comparison |
|---|---:|---|---|
| Exam V2 | 3 | Passed; no undefined control sequences | Every page identical at 100 dpi |
| Exam V2 solution | 18 | Passed; no undefined control sequences | Every page identical at 100 dpi |
| C6/C7 practice activity | 15 | Passed; no undefined control sequences | Every page identical at 100 dpi |

Named destination sets and per-page annotation counts were unchanged. Recorder output confirmed that neither archive was loaded. Removed source spans were checked for verbatim preservation in the archive files. Existing typesetting warnings are outside this organizational change.
