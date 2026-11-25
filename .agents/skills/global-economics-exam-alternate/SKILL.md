---
name: global-economics-exam-alternate
description: Create a requested number of alternate Global Economics LaTeX exam–solution pairs from an existing pair, changing data and context while preserving procedures, assessment structure, and difficulty. Use a solution-first workflow; not for authoring a new exam without a source pair.
---

# Global Economics Exam Alternate

Read applicable repository `AGENTS.md` instructions and both the [exam skill](../global-economics-exam/SKILL.md) and [solution skill](../global-economics-exam-solution/SKILL.md), including their linked templates and build guides. Reuse their authoring and verification guidance; the rules below govern alternate generation and its solution-first order. Adapt the source pair rather than resetting its layout to a scaffold.

## Establish the source pair

Accept two inputs: an existing source exam `.tex` path and the number of alternate versions to create as a positive integer. If the count is missing or invalid, ask for it before generation. Find the companion source solution in the same directory by appending `_solution` to the exam stem: `G10_T2_L1_C1C2_exam.tex` pairs with `G10_T2_L1_C1C2_exam_solution.tex`.

If the solution is missing, report its expected path and request it. Stop pair generation; do not invent a source solution or substitute an exam-first workflow.

Read both sources and relevant included dependencies. Verify agreement on questions, data, numbering, criteria, and point allocations. Resolve a material discrepancy that leaves governing content unclear with a focused question before generating any alternate pairs. Identify the source solution process for every question and subpart. Derive every requested version from this original pair, never from a previous alternate.

## Allocate unused shared indices

Create the requested number of exam–solution pairs, each with its own unused shared index. Save beside the originals as:

- `<exam_stem>_<n>.tex`
- `<exam_stem>_solution_<n>.tex`

For each pair, choose the smallest positive integer `n` available for both basenames, excluding indices already allocated to this batch. Either existing member occupies the index, even without its partner. Matching PDFs and other existing build outputs also occupy it; check intended output locations as well as the source directory. For example, index 1 gives `G10_T2_L1_C1C2_exam_1.tex` and `G10_T2_L1_C1C2_exam_solution_1.tex`.

Record the pre-existing source, dependency, alternate, and output artifacts that this work could affect, so unchanged contents can be verified afterward. Recheck availability immediately before writing; create new artifacts without overwriting existing ones. If a collision occurs, select the next available shared index. Use isolated build output directories to prevent auxiliary-file collisions. Leave the original pair, shared dependencies, and existing alternates unchanged; any changed figures or included content need new, unused paths.

## Plan selection outcomes across versions

For each question whose worked procedure selects an option (such as an investment, project, strategy, or answer choice), identify the available options and the source's correct selection. Plan outcomes across the source and requested alternates independently for each such question: select every feasible option before repeating an outcome, then distribute selections as evenly as feasible, counting the source. For four feasible options with the first selected in the source, three alternates should select the second, third, and fourth.

Change the selected outcome through coherent replacement data and verified calculations; merely reordering or renaming options does not count. Preserve the source's selection rule and relevant tie behavior. A unique-winner question must have the intended option as its actual unique winner. Verify selections that share data or depend on sequential decisions together, and make their plans jointly feasible.

Do not force selections that require a different assessed method, new assumptions, or changed difficulty. Explain any infeasible selections or coupled-decision limitations and diversify among feasible outcomes.

## Author and verify each alternate solution first

For every version, use the solution skill to write a complete alternate worked solution, with each new question before its worked answer. Here, that skill's instruction to preserve original questions means exact agreement with the **new alternate questions**, once established; changing source numbers and narrative context is intentional.

Preserve:

- Learning objectives, assessed criteria, question count, order, numbering, and subpart structure.
- Task marks, question and criterion totals, overall marks, and grading policies.
- Mathematical model and concepts, required methods, the same procedure as defined below, and comparable difficulty.
- Language, institutional information, and response instructions unless the user requests changes.

Change replaceable numerical problem data throughout the worked procedure and adapt narrative context, plus the answers, calculations, units, labels, tables, graphs, and diagrams needed for consistency. Choose coherent, self-contained contexts fitting the same mathematical model. Context changes are optional; numerical variation is required.

**Same procedure** means the same sequence of mathematical operations, dependencies, and reasoning steps, with the same number of operands at each corresponding step. For example, a source step adding two numbers must remain an addition of two numbers, and both replaceable operands must change. Do not add or remove operands or regroup operations to obtain numerical variation. Preserve mathematically relevant feasible domains, signs, integrality, grouping patterns, number of solutions, ties, boundary behavior, and rounding demands wherever they determine the assessed procedure or comparable difficulty. Avoid new assumptions, concepts, shortcuts, or special values that eliminate an assessed step.

Distinguish replaceable problem data from fixed structural numbers before choosing data:

- Every replaceable numerical given and procedural operand must differ from its corresponding value in the original source and every other requested alternate. This includes probabilities, frequencies, counts, coefficients, likelihood ratios, monetary amounts, thresholds, bonuses, and caps, as well as intermediate values reused as operands. Compare corresponding roles and steps, not unrelated occurrences of the same numeral.
- Preserve question numbering, marks, institutional dates, mathematical constants, probability normalization to 1, and any values necessarily fixed by the required method. A value is not fixed merely because it appeared in the source. Constraints such as integrality, ties, or grouping patterns preserve the relevant relationships; they do not by themselves exempt the underlying replaceable values from change.
- Changing only contexts, labels, monetary scales, or the order of unchanged data is insufficient. Choose coherent replacement data that vary the operands throughout the procedure and also produce different intermediate and final numerical results wherever mathematically feasible.
- Explicitly identify and justify every unavoidable numerical repetition, including fixed structural values and results forced by the method or preserved relationships. Group equivalent fixed repetitions under a shared justification where appropriate. Never silently retain a replaceable value; if the combined constraints prevent variation, explain the specific limitation instead of claiming full numerical variation.

Recalculate all intermediate and final results from the new givens rather than applying blind numerical substitutions. Work every subpart, checking reasoning, units, interpretation, and planned selection outcomes. Map corresponding solution steps across the source and all requested alternates, recording each step's operation, dependencies, reasoning, operand count, operand values, and result. Use this comparison to verify both procedural equivalence and numerical differences in operands and results, with explicit justifications for unavoidable repetitions. Revise the data and recalculate affected steps and dependent decisions to resolve accidental repeated operands or results wherever feasible. Verify each complete solution and its comparison before deriving its student exam.

## Derive each student exam

For each verified alternate solution, use the exam skill to create the student document from its question statements. Match wording, data, units, figures, numbering, subparts, and marks exactly across each pair. Exclude worked answers and solution-only annotations from the student exam.

Preserve the source exam's layout conventions, institutional header, instructions, scoring structure, and answer-space arrangement. Reconcile the score matrix with the final scored tasks and questions.

## Validate and deliver

Verify that the requested number of complete pairs was produced, each with a distinct shared index. For every question in every version, compare its mathematical model, methods, subpart structure, assessed criteria, marks, difficulty, and procedure-affecting data characteristics with the original source. Review the solution-step mapping to confirm the same sequence of operations, dependencies, and reasoning steps and the same operand count at every corresponding step. Check that every replaceable given and procedural operand differs from its counterpart in the source and every other requested alternate, and that intermediate and final results differ wherever mathematically feasible. Resolve accidental numerical repetitions by revising data and recalculating dependent work; verify the explicit justification for each unavoidable repetition and the preservation of fixed structural numbers. Check every calculation and final answer, exact agreement within each exam–solution pair, and reconciliation of task marks, question totals, criterion totals, and overall marks. Confirm that calculated selections support the planned diversity, including tie behavior and coupled decisions. Verify that pre-existing artifacts remain unchanged.

For every pair, follow both referenced skills' build guides and visual-inspection requirements. Build and inspect the student exam PDF as required by the exam skill; compile and inspect the solution PDF when requested. Honor an explicit source-only request and disclose verification not performed. Preserve matching basenames when delivering PDFs and avoid overwriting pre-existing build outputs.

Report links and shared indices for all generated pairs, plus any unresolved limitations. Include a compact account of unavoidable numerical repetitions and their justifications, referring to the solution-step comparison where needed. When selection questions exist, include a compact table of the selected outcomes in the source and each alternate, identifying any feasibility or diversity limitations.

## Example invocation

```text
Use $global-economics-exam-alternate to create 3 alternate versions of
book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam.tex
```
