# Directory Summary

## Purpose

Shared LaTeX preambles, graph macros, and visual assets for the project's 2026–2027 teaching materials and repository inventories. The four document scaffolds and their guides are in the [authoring folder](../authoring/README.md).

## Files

| File | Type | Purpose |
|---|---|---|
| [`logo.png`](logo.png) | PNG | Displays the San Bartolomé La Merced crest used in document headers. |
| [`urraca.png`](urraca.png) | PNG | School mascot bird illustration. |
| [`main.tex`](main.tex) | LaTeX | Explains preamble settings, formatting commands, links, and figures with usage examples. |
| [`preamble_exams.tex`](preamble_exams.tex) | LaTeX | Configures compact assessment layouts, adjustable table columns, subsection boxes, and score labels. |
| [`preamble_G10_T1_C2C3.tex`](preamble_G10_T1_C2C3.tex) | LaTeX | Extends the base preamble with a decision-elements table for Grade 10 Term 1 practice activities. |
| [`preamble_STRUCTURE.tex`](preamble_STRUCTURE.tex) | LaTeX | Defines repository inventory typography, directory trees, information boxes, and title pages. |
| [`preamble.tex`](preamble.tex) | LaTeX | Defines shared packages, page settings, colors, frames, images, hyperlinks, navigation, and criterion-based tasks. |
| [`README-preamble.md`](README-preamble.md) | Markdown | Summarizes this directory. |
| [`template_README.md`](template_README.md) | Markdown | Defines the structure, descriptions, relative links, and command inventory required for folder READMEs. |

## Folders

| Folder | Purpose | README |
|---|---|---|
| [`graphs/`](graphs/) | Defines reusable economic and probability graph macros, including density plots, shaded regions, and histograms. | [`README-graphs.md`](graphs/README-graphs.md) |
| [`imgs/`](imgs/) | Stores IHS, ICONTEC, and Cambridge image assets for document illustrations. | None. |

## Directory Structure

```text
preamble/
├── graphs/
├── imgs/
├── logo.png
├── urraca.png
├── main.tex
├── preamble_exams.tex
├── preamble_G10_T1_C2C3.tex
├── preamble_STRUCTURE.tex
├── preamble.tex
├── README-preamble.md
└── template_README.md
```

## Public Commands

| File | Commands |
|---|---|
| [`logo.png`](logo.png) | None. |
| [`urraca.png`](urraca.png) | None. |
| [`main.tex`](main.tex) | None. |
| [`preamble_exams.tex`](preamble_exams.tex) | `\setYColumnWidth`, `\SubsectionBox`, `\CellCenter`, `\score` |
| [`preamble_G10_T1_C2C3.tex`](preamble_G10_T1_C2C3.tex) | `\DecisionElementsTable` |
| [`preamble_STRUCTURE.tex`](preamble_STRUCTURE.tex) | `\code`, `\StructureTitlePage` |
| [`preamble.tex`](preamble.tex) | `\explicacion`, `\mostrarExplicaciones`, `\SimpleSecIniciotrue`, `\SimpleSecIniciofalse`, `\fboxC`, `\cuadro`, `\bigLink`, `\smallLink`, `\bfLink`, `\TaskHyperref`, `\smallUrl`, `\subSecLink`, `\secInicioIconMultiplier`, `\secInicioIcon`, `\secInicio`, `\background`, `\backgroundC`, `\anchoPag`, `\esp`, `\espacioImagenes`, `\fig`, `\ffig`, `\hfig`, `\hffig`, `\linkExplicacion`, `\SectionProblemsTableOfContents`, `\SectionProblemLink`, `\sml`, `\CriterionTask`, `\TOCScoredTitle`, `\sectionScored`, `\boxed` |
| [`README-preamble.md`](README-preamble.md) | None. |
| [`template_README.md`](template_README.md) | None. |


## Unified Grade 10 C1--C3 solutions

`preamble_G10_T1_C1C2C3.tex` is the authoritative presentation preamble.
See [C1--C3 migration and validation](C1C2C3-migration.md) for the complete
migration list, interfaces, dependency structure, and verification results.

Use `\input{preamble_G10_T1_C1C2C3}` in practice and solution documents.
Exams and classroom sheets additionally input `preamble_exam_layout` for
compact lists, margins, assessment columns, and headers. This layer does not
load another preamble or declare a document class.

`preamble_G10_T1_C2C3.tex` remains a compatibility wrapper. Existing general
exam consumers still use `preamble_exams.tex`; they need no migration.
