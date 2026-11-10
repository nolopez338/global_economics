---
name: global-economics-classroom-activity
description: Create print-ready LaTeX classroom activities from existing Global Economics practice activities across grades, terms, lessons, and criteria.
---

# Global Economics Classroom Activities

## Find the practice source

Use the user-supplied practice activity `.tex`, or match the grade, term, lesson, and criterion to an `_practice_activity.tex` in `1-practice_activities`. Ask for the source if the match is missing or ambiguous. In the current collection, use the matching `_classroom_activity.tex` and `.pdf` names in the sibling `2-class_activities` directory.

Read the criterion statement, notation, procedure, and every core Worked Problems section, including General Worked Problems. Treat each core section as one required problem family. In source order, identify a representative structure for each family and record its givens, ordered tasks, essential representations, solution steps, and final interpretation. Exclude separately labeled Advanced Problems from default coverage.

## Build the four stages

Retain the source criterion, notation, and reasoning demands. Vary contexts and values while preserving the mathematical structure, task sequence, and solution procedure within each family. Supply the givens, constraints, and units students need. Use these exact headings once each, in order.

1. **Equations and basic procedure** — Condense the formulas or rules, notation, ordered steps, conditions, and checks students will use.
2. **Worked example** — Include one fully solved example per family, with reasoning, intermediate results, checks, and interpretation.
3. **Guided Example** — Include one fresh example per family. Use prompts, a starter calculation, or partially filled tables where helpful. Leave the key reasoning and final answer for students.
4. **Independent Practice** — Include at least two fresh problems per family with fewer hints and the same level of reasoning.

Keep families in source order within each stage and group multiple independent problems by family. Number problems continuously. Use the same family labels and task labels across the worked, guided, and independent stages so students can match each problem to its model.

For Grade 10 Term 2 Lesson 1 C1, Type A starts with supplied outcomes and probabilities. Type B calculates ordered outcome probabilities from independent events. Both then define the variable, map outcomes to values, list the support, build and check the PMF, and find and interpret an event probability. This yields two worked, two guided, and at least four independent problems. Derive the family structure for other topics from their own sources.

## Lay out and verify the handout

Adapt the [LaTeX scaffold](assets/template_classroom_activity.tex) using the [layout and build guide](references/template_classroom_activity.md). Use the practice source for the mathematics and the classroom reference for the visual style. Keep the four headings above and the fixed letter-paper margins on every page.

Check the family coverage and solve every new problem. Use the `\ifprintsolutions` toggle to produce a student handout and, when requested, a review version with solutions starting on a fresh page. Match every guided and independent problem number and task label in the review solutions. Compile and inspect the rendered pages for legibility, page breaks, and room to work.

