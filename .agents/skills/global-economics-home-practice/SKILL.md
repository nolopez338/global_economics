---
name: global-economics-home-practice
description: Author or adapt student-facing LaTeX math practice activities for any grade, term, topic, or combination of criteria in Global Economics.
---

# Global Economics Home Practice Activities

1. Identify the grade, term, topic, target difficulty, criterion IDs and descriptions, and any supplied tasks, data, or solution requirements. Use the criterion wording from the brief and ask for missing wording when it is essential. When adapting an activity, use the source supplied for that adaptation.
2. Start from the [LaTeX scaffold](assets/template_home_practice.tex) and use the [authoring guide](references/template_home_practice.md) for inputs, navigation, graphs, and builds. Keep the title, linked contents, **Evaluated criteria**, and brief instructions to attempt each task before opening its solution in the front matter, outside the numbered sequence. List the actual criterion IDs and descriptions and label nonconsecutive IDs explicitly.

## Required activity structure

Use these numbered top-level sections in this order for every activity, including short activities.

1. **Introduction** — Present the concise highlight legend as the very first instructional content, with only a brief heading or one-sentence lead-in before it. Then introduce the topic through at least two short, accessible introductory examples. Give enough context to understand the notation, quantities, units, and relationships used later. These motivating examples are distinct from the full problems in General Worked Problems. Where useful, add a quick check about a distinction or meaningful change.
2. **Notation Reference and Practice Procedure** — Present the detailed notation reference, distinguishing general definitions from contextual meanings in concise bullets linked explicitly to the relevant introductory examples (for example, “Example 1: …”). Follow the table with a reusable procedure for choosing an approach, carrying out the reasoning, and interpreting or checking the result.
3. **General Worked Problems** — Give students self-contained, criterion-linked problems with worked solutions. Supply the information, units, and constraints each task needs. Where the topic supports it, pair an initial application with a follow-up that changes a meaningful input, assumption, constraint, or representation. Ask students to explain how the change affects their reasoning and what conclusions the available information supports.
4. **Advanced Problems** — Extend the same reasoning at a level appropriate to the brief. Ask students to coordinate ideas, compare cases or representations, or justify a conclusion under more demanding conditions.

When distinct concepts, methods, or problem families benefit from separate treatment, replace **General Worked Problems** with two or more consecutive sections titled **General Worked Problems — [Descriptive Focus]**. Split when each group needs its own conceptual framing or approach. Place all groups between **Notation Reference and Practice Procedure** and **Advanced Problems**. This split is the sole permitted reason to add numbered top-level sections. All four stages are required, and **Advanced Problems** always comes last.

Use subsections for material within a stage, including numbered problem subsections. Give each worked-problem group its own linked problem list. Keep requested independent practice in a distinct subsection within the appropriate stage, and place its solutions as specified in the brief.

## Tables, highlights, and companion responsibilities

Use [math-legend-highlight](../math-legend-highlight/SKILL.md) for concept and notation identification, the shared semantic mapping, both table designs, and their hierarchy, anchors, and navigation. Use [math-practice-highlights](../math-practice-highlights/SKILL.md) afterward to apply that mapping throughout instructional content, including markup, renderers, diagrams, toggles, and validation. This skill owns the activity structure and introductory examples. Resume completed handoffs without circular invocation or repeated work.

The concise schema is **Symbol or notation | Concept | Brief meaning**. The detailed schema is **Symbol or notation | Concept | Definition | Meaning in the introductory examples**. Translate all headings and example labels consistently into the document's language. Keep concise entries short and limited to essential notation, without extended explanations, derivations, or worked calculations. In the detailed final column, use brief bullets explicitly linked to the relevant introductory examples; do not force an irrelevant example into a row. Avoid repeating lengthy explanations across tables and introduction. Both tables use the same mapping but serve different purposes.

Reuse existing tables, labels, macros, registry entries, and mapping on reruns. Preserve complete notation and component roles in composite expressions, consistent concept–notation–value highlighting where useful, existing toggle settings, grayscale legibility, and content with highlights disabled. Tables must not reveal answers or reasoning required in independent or assessed tasks.

## Solutions and final checks

- In each worked solution, connect the scenario to the mathematical model, state the rule or formula, show substitutions and intermediate reasoning as applicable, and interpret the result in context. Use equations, tables, graphs, or diagrams where they clarify the reasoning.
- Recalculate results and check that the tasks address the listed criteria. Follow the guide to compile and inspect the layout and the contents, problem, task-to-solution, and return links. Check graphs against the calculations and remove unused placeholders and inputs.
- Verify the numbered top-level headings in the source and compiled contents. Check that all four stages appear in order, **Advanced Problems** comes last, and any extra top-level sections come solely from replacing **General Worked Problems** with consecutive titled groups, each with its own linked problem list. Confirm the front matter is unnumbered and independent practice sits within its stage.

- Verify the instructional order: concise legend first in Section 1 → at least two contextual introductory examples → detailed four-column reference in Section 2 → reusable procedure. Check example-linked bullets, shared mapping, concise versus detailed scope, links, and absence of accidental duplicates.
