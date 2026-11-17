---
name: global-economics-classroom-activity
description: Create print-ready LaTeX classroom activities from existing Global Economics practice activities, with exactly one worked example, one guided example, five independent exercises, and no highlights.
---

# Global Economics Classroom Activities

## Fixed activity requirements

Every classroom activity contains exactly **one worked example, one guided example, and five independent practice exercises** in total, regardless of the number of source problem families. The worked example has a complete solution with clear, step-by-step reasoning. The guided example has structured prompts and sufficient workspace for students to complete the solution. All five independent exercises remain unsolved in the student handout and have appropriate workspace: exercises 1–3 consolidate the lesson's core skills; exercises 4–5 are slightly more challenging while staying within the same topic and assessment criterion.

Classroom activities must never contain instructional highlights, highlighted text or mathematics, semantic highlight commands, or highlight legends. This applies to every stage and any optional review solutions. When adapting source material, remove all highlighting while preserving its content and ordinary document formatting. Do not invoke highlight-authoring skills or copy highlight definitions, imports, commands, or legends into the activity.

## Find the practice source

Use the user-supplied practice activity `.tex`, or match the grade, term, lesson, and criterion to an `_practice_activity.tex` in `1-practice_activities`. Ask for the source if the match is missing or ambiguous. In the current collection, use the matching `_classroom_activity.tex` and `.pdf` names in the sibling `2-class_activities` directory.

Read the criterion statement, notation, procedure, and every core Worked Problems section, including General Worked Problems. Identify each core problem family and record its givens, ordered tasks, essential representations, solution steps, and final interpretation. Plan coverage of those core skills within the fixed total of one worked example, one guided example, and five independent exercises; combine related tasks within a coherent example or distribute families across the five exercises as appropriate. Do not multiply the counts by family. Exclude separately labeled Advanced Problems from default coverage; the last two independent exercises should add modest difficulty within the core topic and criterion.

Inspect source highlighting before reuse. Unwrap highlighted text and mathematics into their ordinary content, remove highlight-only legends and associated labels or navigation, and retain substantive notation definitions, explanations, and mathematics in plain form. Preserve ordinary headings, bold task labels, tables, alignment, and document layout. Check custom macros and nested inputs for hidden highlighting; use plain equivalents locally without changing shared repository files.

## Build the four stages

Retain the source criterion, notation, and reasoning demands. Vary contexts and values while preserving the mathematical structure, task sequence, and solution procedure within each family. Supply the givens, constraints, and units students need. Use these exact headings once each, in order.

1. **Equations and basic procedure** — Condense the formulas or rules, notation, ordered steps, conditions, and checks students will use.
2. **Worked example** — Include exactly one fully solved example for the entire activity. Explain each step, show intermediate results, and include checks and a final interpretation.
3. **Guided Example** — Include exactly one fresh example for the entire activity. Provide structured prompts, a starter calculation, or partially filled tables where helpful, with sufficient workspace at each step. Leave the key reasoning and final answer for students to complete.
4. **Independent Practice** — Include exactly five fresh, unsolved exercises with fewer hints and appropriate workspace for calculations, representations, and interpretations. The first three consolidate the lesson's core skills. The last two are slightly more challenging while remaining aligned with the same topic and assessment criterion.

Number problems continuously: worked example 1, guided example 2, and independent exercises 3–7. Independent exercises 1–3 (problem numbers 3–5) consolidate; independent exercises 4–5 (problem numbers 6–7) add modest challenge. Keep family coverage in source order where compatible with this progression. Use consistent family and task labels where the same structure recurs. Do not add extra examples or exercises to cover more families. Keep all four stages free of highlights and highlight legends.

For Grade 10 Term 2 Lesson 1 C1, Type A starts with supplied outcomes and probabilities. Type B calculates ordered outcome probabilities from independent events. Both then define the variable, map outcomes to values, list the support, build and check the PMF, and find and interpret an event probability. Use one complete worked example that models the common procedure and one guided example that scaffolds its use with the other starting structure. Distribute both families across exactly five independent exercises, with the first three consolidating and the last two adding modest difficulty within C1. This still yields exactly one worked example, one guided example, and five independent exercises, all without highlights. Derive the family structure for other topics from their own sources.

## Lay out and verify the handout

Adapt the [LaTeX scaffold](assets/template_classroom_activity.tex) using the [layout and build guide](references/template_classroom_activity.md). Use the practice source for the mathematics and the classroom reference for compatible visual style only; existing documents may have different counts or highlighting and do not override this skill. Keep the four headings above and the fixed letter-paper margins on every page. Use ordinary bold titles without shaded or colored highlight backgrounds.

Check the family coverage and solve every new problem privately to verify correctness. Use the `\ifprintsolutions` toggle to produce the student handout and, when requested, a review version with solutions starting on a fresh page. The student pages always contain exactly one worked example, one guided example, and five independent exercises; all five independent exercises stay unsolved there. Optional review pages contain solutions to those existing problems, not additional examples or exercises. Match every guided and independent problem number and task label in the review solutions. Compile and inspect the rendered pages.

Before delivery, verify:

- Exactly one worked example includes a complete, clear, step-by-step solution, checks, and interpretation.
- Exactly one guided example provides structured prompts and sufficient workspace for students to finish the solution.
- Exactly five independent exercises remain unsolved in the student handout, each with appropriate workspace. The first three consolidate core skills; the last two are slightly more challenging within the same topic and assessment criterion.
- No instructional highlights, highlighted text or mathematics, semantic highlight commands, or highlight legends remain anywhere in the activity or optional review pages. Inspect local definitions, imports, nested inputs, and the rendered pages; do not rely only on command-name searches. Remove inherited highlighting from used macros locally or replace their uses with plain formatting. Preserve underlying content and ordinary formatting.
- Fixed margins, legibility, page breaks, and workspace suit the required calculations, tables, graphs, and explanations. Optional review solutions begin on a fresh page and match problems 2–7.

