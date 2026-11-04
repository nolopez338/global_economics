# 2026–2027 Global Economics Authoring

Choose the skill by the requested deliverable. A request to make an activity printable sets a delivery constraint. Independent criterion-linked work still uses Home Practice Activities, while numbered contexts followed by a characterization table use Print Handout.

| Deliverable | Skill | Guide | LaTeX scaffold | Build working directory |
| --- | --- | --- | --- | --- |
| Student exam with objectives, criteria, scored questions, and answer space | [global-economics-exam](../../.agents/skills/global-economics-exam/SKILL.md) | [Exam](template_exam.md) | [template_exam.tex](template_exam.tex) | Scaffold from this folder. Adapted exam from its source directory. |
| Worked scoring key preserving the source exam's wording, order, numbering, and points | [global-economics-exam-solution](../../.agents/skills/global-economics-exam-solution/SKILL.md) | [Exam solution](template_exam_solution.md) | [template_exam_solution.tex](template_exam_solution.tex) | Scaffold from this folder. Adapted key from its source directory. |
| Independent criterion-linked work with worked examples, solutions, and graphs where appropriate | [global-economics-home-practice](../../.agents/skills/global-economics-home-practice/SKILL.md) | [Home Practice Activities](template_home_practice.md) | [template_home_practice.tex](template_home_practice.tex) | Scaffold from this folder. Adapted activity from its source directory. |
| Numbered problem descriptions followed by a Context, Type, Distribution, and Characterization table | [global-economics-print](../../.agents/skills/global-economics-print/SKILL.md) | [Print handout](template_print.md) | [template_print.tex](template_print.tex) | Scaffold from this folder. Adapted handout from its source directory. |

## Building

Run pdfLaTeX from the working directory in the table, passing the source filename. For a smoke build, create a temporary output directory and pass its absolute path with `-output-directory`.

```text
pdflatex -interaction=nonstopmode -halt-on-error template_exam.tex
```

Repeat until contents and references resolve for the exam solution and home practice activity. The [shared preambles and assets](../preamble/README-preamble.md) are in the sibling `preamble/` directory. The scaffolds already search `../preamble/` from here. When adapting a copy, keep that directory reachable for nested inputs and graphs. For the exam, also check that the graphics search path reaches `logo.png`.

The [year's recursive Windows build](../compile_all_tex.bat) also finds these scaffolds and runs `latexmk -pdf` from each source directory.

The PDFs in this folder are existing preview snapshots. Use the paired guides and LaTeX sources for authoring.
