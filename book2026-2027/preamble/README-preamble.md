# Directory Summary

## Purpose

Shared LaTeX preambles, document templates, and visual assets for the project's 2026–2027 teaching materials and repository inventories.

## Files

| File | Type | Purpose |
|---|---|---|
| [`logo.png`](logo.png) | PNG | Displays the San Bartolomé La Merced crest used in document headers. |
| [`main.tex`](main.tex) | LaTeX | Explains preamble settings, formatting commands, links, and figures with usage examples. |
| [`preamble_exams.tex`](preamble_exams.tex) | LaTeX | Configures compact assessment layouts, adjustable table columns, subsection boxes, and score labels. |
| [`preamble_G10_T1_C2C3.tex`](preamble_G10_T1_C2C3.tex) | LaTeX | Extends the base preamble with a decision-elements table for Grade 10 Term 1 practice activities. |
| [`preamble_STRUCTURE.tex`](preamble_STRUCTURE.tex) | LaTeX | Defines repository inventory typography, directory trees, information boxes, and title pages. |
| [`preamble.tex`](preamble.tex) | LaTeX | Defines shared packages, page settings, colors, frames, images, hyperlinks, navigation, and criterion-based tasks. |
| [`README-preamble.md`](README-preamble.md) | Markdown | Summarizes this directory. |
| [`template_exam_solved.tex`](template_exam_solved.tex) | LaTeX | Demonstrates scored exam sections, criterion-linked tasks, and worked probability solutions with graphs. |
| [`template_exam.tex`](template_exam.tex) | LaTeX | Provides an exam layout with a school header, learning objective, assessment criteria, student details, and scored questions. |
| [`template_practice.tex`](template_practice.tex) | LaTeX | Demonstrates criterion-linked practice tasks, worked probability solutions, and graph command examples. |
| [`template_print.tex`](template_print.tex) | LaTeX | Provides a printable problem sheet followed by a solution characterization table. |
| [`template_README.md`](template_README.md) | Markdown | Defines the structure, descriptions, relative links, and command inventory required for folder READMEs. |
| [`urraca.png`](urraca.png) | PNG | Displays a colorful bird illustration. |

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
├── main.tex
├── preamble_exams.tex
├── preamble_G10_T1_C2C3.tex
├── preamble_STRUCTURE.tex
├── preamble.tex
├── README-preamble.md
├── template_exam_solved.tex
├── template_exam.tex
├── template_practice.tex
├── template_print.tex
├── template_README.md
└── urraca.png
```

## Public Commands

| File | Commands |
|---|---|
| [`logo.png`](logo.png) | None. |
| [`main.tex`](main.tex) | None. |
| [`preamble_exams.tex`](preamble_exams.tex) | `\setYColumnWidth`, `\SubsectionBox`, `\CellCenter`, `\score` |
| [`preamble_G10_T1_C2C3.tex`](preamble_G10_T1_C2C3.tex) | `\DecisionElementsTable` |
| [`preamble_STRUCTURE.tex`](preamble_STRUCTURE.tex) | `\code`, `\StructureTitlePage` |
| [`preamble.tex`](preamble.tex) | `\explicacion`, `\mostrarExplicaciones`, `\SimpleSecIniciotrue`, `\SimpleSecIniciofalse`, `\fboxC`, `\cuadro`, `\bigLink`, `\smallLink`, `\bfLink`, `\TaskHyperref`, `\smallUrl`, `\subSecLink`, `\secInicioIconMultiplier`, `\secInicioIcon`, `\secInicio`, `\background`, `\backgroundC`, `\anchoPag`, `\esp`, `\espacioImagenes`, `\fig`, `\ffig`, `\hfig`, `\hffig`, `\linkExplicacion`, `\SectionProblemsTableOfContents`, `\SectionProblemLink`, `\sml`, `\CriterionTask`, `\TOCScoredTitle`, `\sectionScored`, `\boxed` |
| [`README-preamble.md`](README-preamble.md) | None. |
| [`template_exam_solved.tex`](template_exam_solved.tex) | None. |
| [`template_exam.tex`](template_exam.tex) | None. |
| [`template_practice.tex`](template_practice.tex) | None. |
| [`template_print.tex`](template_print.tex) | None. |
| [`template_README.md`](template_README.md) | None. |
| [`urraca.png`](urraca.png) | None. |
