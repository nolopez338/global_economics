# Classroom Activity Layout and Build Guide

Copy the [LaTeX scaffold](../assets/template_classroom_activity.tex) to the intended source directory. Every activity has exactly one fully worked example, one guided example, and five unsolved independent exercises, with the mandatory three-level structural heading hierarchy below and boxed criteria, and no semantic instructional highlights in the printable portion. These counts apply to the whole activity, not to each problem family. Use the matching practice source for mathematical content. The [G11 C2 practice source](../../../../book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex) and [G11 C2 classroom reference](../../../../book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C2_classroom_activity.tex) demonstrate the transformations below. The G11 classroom reference supplies table/layout principles across grades and topics; its C2 symbols, classifications, and formulas are examples, not requirements. Do not inherit its problem-count discrepancies, nonstandard General assessment tasks heading, stale comments, or conflicting task instructions. The five required sections and fixed counts in the skill take precedence.

## Content and highlight rules

- Keep the five section headings in the scaffold. Number the worked example 1, the guided example 2, and the five independent exercises 3–7. Do not duplicate blocks per family; cover source families within these seven problems.
- Give the single worked example a complete solution with clear, step-by-step reasoning, intermediate results, checks, and interpretation.
- Give the single guided example structured prompts and sufficient workspace for each required step. Students complete the key reasoning and final answer.
- Leave all five independent exercises unsolved in the student handout with only numbered titles, concise self-contained descriptions, and optional compact given-data tables. The first three (problems 3–5) consolidate core skills. The last two (problems 6–7) are slightly more challenging within the same topic and assessment criterion; do not import unrelated advanced material.
- Never include semantic instructional highlights, semantic highlight commands, or highlight legends in the printable activity. All three structural heading levels, including bold underlined subtask titles, and criterion boxes are explicitly permitted. This exception does not permit semantic styling of concepts, notation, values, or mathematics. Remove highlight wrappers while preserving their text or mathematics. Remove highlight-only legends, labels, and navigation; retain any substantive notation or explanation in ordinary form. Do not copy highlight definitions or imports. Preserve ordinary headings, bold task labels, tables, and mathematical layout.
- Inspect commands inherited from the shared preamble and nested inputs before using them. For example, the current year-local `\boxed` produces a shaded box: display the result as ordinary mathematics instead. Replace other highlight-producing uses locally without editing shared files. Unused formatting definitions in the required shared preamble do not justify using highlights in the activity.

## Concise task language

Every task and reusable procedure uses at most three numbered steps. Consolidate related actions while preserving the source's mathematical scope. General tasks is a short list of required mathematical outputs only: omit explanations, teaching commentary, justification requests, and verification/check instructions. Required contextual interpretations remain outputs. Apply the same three-step limit and prompt restrictions to task-specific instructions. Keep reasoning and appropriate checks in the worked solution; keep useful scaffolding and workspace in the guided example.

Independent descriptions supply every given needed for General tasks: context, observation period where relevant, definitions, values, units, constraints, and necessary assumptions. Any essential problem-specific output belongs directly in the description. Do not repeat task prompts or add procedural hints, starter calculations, checklists, response lines, blank answer tables, graph templates, reserved workspace, or instructions about separate paper or where to solve. These rules apply across topics without requiring this lesson's mathematics.

## Shared inputs

Load the activity's year-local `preamble.tex` once. It declares the 11 pt article class. Run pdfLaTeX from the source directory. The scaffold searches `../../../preamble/` from `<year>/<grade>/<term>/2-class_activities/` and `../../../../book2026-2027/preamble/` from its own `assets/` directory. In a classroom activity, keep only the lookup for its own year. For scratch builds, replace the relative lookup or prepend the absolute year-local preamble directory to `TEXINPUTS`. A trailing path separator retains TeX's default search paths. The lookup also resolves `graphs/...` and nested inputs.

```powershell
$env:TEXINPUTS = 'C:/path/to/repo/book2026-2027/preamble/;'
```

Use `:` as the search-path separator on POSIX systems.

## Print layout

- After the shared preamble, apply `\geometry{letterpaper,margin=0.25in}`. Keep the same margins for every printable page. Start with `\linespread{1.04}` and 4 pt paragraph spacing.
- Use a compact centered title and course metadata. Put each complete official criterion in `\criterionbox{code}{verbatim statement}`: white fill, .4 pt `black!45` border, 2 mm corners, 6 pt horizontal / 5 pt vertical padding, and natural wrapping within local `\linewidth`. Keep plain bold `\problemtitle` titles and right-aligned family labels for problems 1–7. Apply the three-level heading hierarchy below.
- Inspect existing helpers and packages before adding definitions; reuse the shared preamble's TikZ, xcolor, and tcolorbox. The scaffold defines its helpers inside a local printable-activity group after `\begin{document}`. End it only after `\par\clearpage`, before any existing appended solutions, to restore their own formatting. When adapting an existing file, preserve its solution helpers and settings; use activity-only names or local replacements rather than globally redefining shared helpers.
- Pair related reference or instructional tables in top-aligned `.49\linewidth` minipages separated by `\hfill`, with `\vspace{0pt}` at each start, when this improves scanning. Keep related groups together in logical order. Use full-width blocks for wide or tall content. Keep each prompt close to its data and response space. For a short block that must stay together, reserve its measured height with `\Needspace` before the block. Allow long problems to break at task boundaries.
- Size tables to the local `\linewidth`. Use wrapping `tabularx` columns as needed and `longtable` with repeated headings for multi-page tables. In the guided example, leave blank cells, lines, or space for calculations or sketches when needed. Let the content determine the page count.
- Use `\workspace{<height>}` for adjustable blank working space and `\responseline` for short answers. The scaffold's heights are starting points: expand them to fit the actual reasoning, calculations, tables, or graphs. Keep guided prompts next to their response spaces; reserve the measured prompt-plus-workspace block before its subtask heading, as the scaffold does for the final interpretation. Independent problems follow one another compactly without answer space.
- For graphs, consult the year-local [graph guide](../../../../book2026-2027/preamble/graphs/README-graphs.md) and check the chosen command's arguments and dependencies. Load the graph inputs the activity uses. Check axes, units, labels, plotted values, and annotations at print size.

## Three-level structural heading hierarchy

Inspect the definitions and uses in the [G10 C3 heading reference](../../../../book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex). Its section border, compact task nodes, and bold underlined stages define the style; its negative vertical spacing is not part of this convention. Use the scaffold's local helpers across topics.

| Level and placement | Required appearance | Numbering and relationship |
| --- | --- | --- |
| `\stageheading{title}` for the five exact sections | Centered `\large`, bold black text; compact `black!10` node; black 0.2 pt border; 2 mm corners; 3 pt inner padding; zero outer padding | Unnumbered, once each in the prescribed order; contains tasks and problem blocks |
| `\task{Task n --- Full title.}{optional instructions}` in General tasks and worked/guided examples | Calls `\taskheading`; left-aligned bold black text; compact `black!5` node; `draw=none`; 2 mm corners; 3 pt inner padding; zero outer padding | Keep General tasks identifiers and repeat their sequence in each example; task numbers do not continue problem numbers |
| `\subtaskheading{n}{Short title}` for worked solution and guided scaffold stages | Left-aligned black `\textbf{\underline{n. Short title.}}`; no shading or surrounding box | Restart at 1 within each task; at most three stages; use corresponding stage numbers in parallel cases |

Task nodes contain a ragged-right `varwidth` capped at `\dimexpr\linewidth-6pt\relax`, so long titles wrap at the local full or minipage width and short ones keep a compact background. Put the entire task title in the first argument of `\task`; the second argument is unshaded optional accompanying instructions, often `{}`. Do not shade a task's content panel. Use `\subtaskheading` for numbered stages, not for every case label, table group, or explanatory sentence. It appends the final period; omit that period in its title argument. Keep underlined titles concise enough to fit the local width because `\underline` is unbreakable. Instructions and mathematical conditions follow outside the underline:

```latex
\task{Task 2 --- Calculate totals and differences.}{}
\subtaskheading{1}{Calculations}
Use the given quantities in each case.
% Tables and calculations follow; guided versions retain blanks/workspace.
\subtaskheading{2}{Interpretation}
State the required contextual meanings.
```

Preserve ordinary `enumerate` items in General tasks and the reusable procedure. They list required outputs/procedure steps rather than solution/scaffold subheadings. Problem titles remain plain bold, continuously numbered 1–7; they do not acquire task shading or subtask underlining. Independent exercises remain descriptions and givens only: never introduce task/subtask prompts there.

Use the same positive 4 pt before-spacing and positive `\smallskip` after-spacing for the three heading helpers. They reserve opening space with `\Needspace` and discourage a break after the heading with `\nopagebreak[4]`. These are starting reservations, not guarantees for arbitrarily tall content: reserve a measured opening block before its heading when necessary, and let long content break at meaningful task/stage boundaries. Do not copy negative `\vspace` adjustments from the reference.

For corresponding subtask headings in paired blocks, use two top-aligned `.49\linewidth` minipages, each starting with `\vspace{0pt}` and its heading, separated by `\hfill`, as in the guided scaffold. The same number in both cases represents one parallel stage. Keep short titles to matching line counts; if either title cannot fit, use a shared heading above the pair. Start each subsequent corresponding stage as a fresh pair, rather than stacking all stages inside unequal-height columns. Reserve enough space for the pair before it begins; minipages cannot split across pages.

## Exactly two table-style families

### 1. Opening notation/formula reference table

This is a plain notation reference, not a highlight legend. Use **Symbol | Concept | Formula**, booktabs horizontal rules (`\toprule`, `\midrule`, `\bottomrule`), no vertical rules, and no surrounding grid. Preserve every needed definition and formula, including any substantive content unwrapped from a source highlight legend.

Start locally with `\small`, `\tabcolsep=3pt`, `\extrarowheight=0pt`, `\parskip=0pt`, and `\arraystretch=1`. Use ragged-right wrapping columns, initially `.21\linewidth`, `.34\linewidth`, and flexible `X`, with `@{}` outer padding. Remove unnecessary explicit row gaps and use compact inline mathematics where legible. If a formula is too long, break it meaningfully, reallocate widths, or use full width; never drop content to make it fit.

The scaffold's `\NotationReferenceTable{<rows>}` implements these defaults. It can be called in each of two top-aligned half-width blocks or at full width:

```latex
\noindent\begin{minipage}[t]{.49\linewidth}
\vspace{0pt}
\NotationReferenceTable{
  $a$ & First quantity & [Definition and units] \\
  $b$ & Second quantity & [Definition and units] \\
}
\end{minipage}\hfill
\begin{minipage}[t]{.49\linewidth}
\vspace{0pt}
\NotationReferenceTable{
  $T$ & Total & $T=a+b$ \\
  $d$ & Difference & $d=a-b$ \\
}
\end{minipage}\par
```

These symbols and relations only illustrate layout. Replace them with the actual topic's notation and formulas. Each `tabularx` uses its **local** `\linewidth`, including inside minipages; do not use `\textwidth` there.

### 2. General instructional and problem tables

Use the ruled family demonstrated by the reference's `\ExampleInformationTable` and `\GuidedEstimationTable` as the default for information, calculations, worked examples, guided examples, and problem tables throughout the printable handout. This intentionally generalizes those example tables. The reference still has booktabs tables and older four-column macros elsewhere; these inconsistencies do not define additional default styles.

Start locally with `\small`, `\tabcolsep=4pt`, and `\arraystretch=1.16`. The scaffold also resets `\extrarowheight` and `\parskip` to zero locally to avoid inherited spacing. Use wrapping ragged-right columns, vertical column rules, and `\hline` between rows. For three-column information tables start with `.14\linewidth`, `.32\linewidth`, and `X`. For compact calculation tables start with `.10\linewidth`, `.20\linewidth`, and `X`. Adjust widths and the number of columns to those genuinely needed; a two- or four-column ruled table is still this family, not a third style. Retain local `\linewidth` sizing and repeat headings in separate blocks or on new pages of `longtable`.

The scaffold provides `\InformationTable{<rows>}` and `\CalculationTable{<rows>}` as width variants of the same ruled helper. Calculation widths have optional overrides: `\CalculationTable[.14\linewidth][.24\linewidth]{<rows>}` is used in the half-width guided blocks so the Symbol and Concept headings fit without reducing the font. The `.10/.20/X` starting allocation suits the full-width calculation table. `\ClassroomRuledTable{<first width>}{<second width>}{<headings>}{<rows>}` allows other three-column headings and width allocations. Each body row ends in `\\ \hline`. `\TableGroup{<short title>}` produces a bold three-column spanning row with its own horizontal rule; for a different column count adapt the `\multicolumn` count. Long spanning headings need a wrapping `p{...}` column sized to the available inner width rather than an unbreakable `l` cell.

```latex
\InformationTable{
  \TableGroup{Given quantities}
  $a$ & First quantity & [Value, units, and contextual meaning] \\ \hline
  $b$ & Second quantity & [Value, units, and contextual meaning] \\ \hline
  \TableGroup{Derived quantities}
  $T$ & Total & [Value, units, and contextual meaning] \\ \hline
}
\CalculationTable{
  \TableGroup{Case A}
  $T$ & Total & $T=a+b$\par $=12+8=20$ units.\par
    The two quantities together account for 20 units. \\ \hline
}
```

These are reusable structural examples, not required topic content. For paired case blocks, use the same `.49\linewidth` minipage arrangement above. Call the table helper separately in each block to repeat the column headings, and give each case a clear spanning heading. Show shared information once before the cases; separate values that differ by case, team, or confidence level.

## Compact by structure, preserving reasoning

| Before | After |
| --- | --- |
| Opening reference with explicit row gaps and wide padding | Plain booktabs notation reference, local compact settings, two `.49\linewidth` blocks when legible |
| Symbol / Concept / Type / Meaning, with repeated classification cells | Symbol / Concept / In context..., with classifications retained as bold full-width `\multicolumn` group headings and horizontal rules |
| Calculation / Result / Meaning in separate narrow columns | One broad column containing formula, numerical substitution, result with units, then contextual meaning |
| Separate rows for every closely related intermediate quantity | A coherent combined row that retains every calculation; for example, both endpoint calculations and the final interval in the interval row |
| Shared values repeated in each case | Shared information once, then clearly titled case blocks with repeated column headings |
| A long explanation inflates a narrow table cell | Complete explanatory calculation and interpretation immediately beside or below the table |

Use short paragraphs or aligned mathematics to preserve the calculation sequence inside broad cells. Keep every necessary definition, classification, formula, intermediate step, check, unit, and interpretation. Consolidation changes structure, not mathematical or pedagogical coverage. When moving a calculation outside a table, retain its connection to the relevant quantity. Keep related groups in source order unless the learning progression requires a change.

Guided tables must stay partially blank, leaving key reasoning and final answers for students. The reference's explicit row gaps (such as `\\[10pt]` or `\\[16pt]`) are adjustable starting points, not universal heights: size each blank row for the expected handwritten calculation and explanation. Independent tables contain given data only; omit blank answer cells, response lines, graph templates, and reserved workspace. Supply no independent solutions.

Semantic consolidation, column-width allocation, and side-by-side placement are the primary compacting methods. Do not prescribe indiscriminate font reduction, scaled tables (`\resizebox`/`\scalebox`), fixed page counts, or copied negative vertical spacing. Use full-width tables and natural page breaks when necessary. Minipages and `tabularx` cannot split across pages: divide long content at meaningful group/task boundaries or use full-width `longtable` in the same family.

After changing a table, rewrite task instructions to match the actual headings, group titles, case blocks, and blank response spaces. Do not retain a source instruction requiring a Type column or separate Calculation/Result/Meaning columns after merging them. A task to create a table independently must describe the intended ruled structure consistently.

## Build and inspect

This scaffold creates the printable student activity only, including its required fully worked example. It contains no separate solutions template or review toggle. Existing appended solutions belong to a different solution-authoring skill: preserve their source and appearance, leave their formatting in place, and scope these activity helpers so they cannot affect those pages. Capture a baseline and compare solution renders after updating.

Use the five headings exactly once in this order: **Equations and basic procedure**, **General tasks**, **Worked example**, **Guided Example**, **Independent Practice**. Copy the scaffold's local structural commands for reproducible styling; do not apply any of these three activity heading styles to existing appended solutions. Include each complete official criterion verbatim in its own `\criterionbox` with the code bold.

Run pdfLaTeX from the source directory, using the complete LaTeX verification workflow.

```powershell
pdflatex -interaction=nonstopmode -halt-on-error activity.tex
```

Use `-output-directory` with an existing absolute directory to keep build files separate. Repeat a build if its cross-references require another pass.

Before delivery:

- Check every task and reusable procedure has at most three numbered steps and that General tasks lists only mathematical outputs. Student prompts must contain no justification or verification requests.
- Count exactly one worked example, one guided example, and five independent exercises on the student pages. Check the worked solution is complete and explains every step.
- Check the guided prompts leave meaningful work for students and have sufficient response space. Check every independent exercise is unsolved, self-contained, and compact, with no repeated tasks, hints, answer areas, or solving-location instructions.
- Verify independent exercises 1–3 (problems 3–5) consolidate core skills and exercises 4–5 (problems 6–7) add modest challenge within the same topic and criterion.
- Verify all five exact section titles and their order, centered large bold black text, compact `black!10` fill, black 0.2 pt borders, 2 mm corners, 3 pt inner padding, and zero outer padding. Verify complete verbatim criteria in their unchanged rounded white boxes.
- Verify task titles pass through `\task` to `\taskheading`, with left-aligned bold black text, compact `black!5` fill, no visible border, 2 mm corners, 3 pt inner padding, zero outer padding, and title-only shading. Inspect long-title wrapping within both full and half local widths.
- Verify numbered worked/guided stages are bold underlined titles without boxes or shading, with instructions outside the underline. Check task/subtask numbering independently of problem numbers 1–7, the three-step limit, paired heading alignment, and ordinary numbered lists in General tasks. Independent practice must not gain repeated task prompts.
- Inspect every heading at all three levels on every rendered page for appearance, wrapping, positive spacing, alignment, clipping, overlap, and protection with opening content at page breaks. Check that reservations fit actual opening tables/pairs and no negative spacing was copied.
- Inspect definitions, imports, nested inputs, and renders for semantic instructional highlights or legends; preserve their prohibition for concepts, notation, values, and mathematics. All three heading levels and criterion boxes are structural exceptions only.
- Check logs for missing inputs and overfull boxes. Inspect fixed margins, legible tables, heading spacing, clean page breaks, and sufficient guided workspace with compact independent flow.
- Render the compiled PDF and inspect every page: wrapping in both half-width and full-width tables, complete and legible formulas, continuous grid alignment, local widths within margins, repeated headings and case titles, natural page breaks, sufficient guided workspace, and compact independent flow without reserved blank space. Confirm exactly the two style families and that every task instruction matches the displayed tables. Fix overfull boxes rather than hiding their warnings or shrinking the whole table.
- When updating a document with appended solutions, verify their content and rendered appearance remain unchanged and activity styles do not reach those pages. Do not add solutions or review variants.
