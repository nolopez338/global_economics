# Home Practice Activities Authoring Guide

## Source and shared inputs

Copy the [LaTeX scaffold](../assets/template_home_practice.tex) into the intended source directory. Replace the bracketed placeholders and remove unused optional blocks.

Also copy [practice_procedure_diagrams.tex](../assets/practice_procedure_diagrams.tex) beside the source; its explicit input is already in the scaffold. This deployed snapshot travels with the activity. Reuse an existing copy, compare before updating, and preserve local modifications. The skill asset is the authoritative implementation; no build should search the skill directory implicitly. Read [Procedure diagrams](procedure_diagrams.md) for the API, detailed/compact examples, deployment/update policy, panels and validation cases.

Keep the scaffold's `\input@path` setup and load the [shared preamble](../../../../book/preamble/preamble_exams.tex) once. It initializes the document class and loads the shared layout and navigation commands. The relative search paths cover the scaffold's directory and typical activity directories under `book/`.

When the output source directory is outside that search range, add the absolute `book/preamble/` directory to `TEXINPUTS` for the build session. Include the trailing slash on the directory and an empty path component for TeX's default search paths. This also resolves nested inputs. In PowerShell, use a semicolon as the path separator and replace the placeholder path below. On systems with a POSIX shell, use a colon as the separator.

```powershell
$env:TEXINPUTS = 'C:/path/to/repo/book/preamble/;'
```

## Section layout

Keep the title, linked contents, **Evaluated criteria**, and a brief instruction to try each task before opening its solution in the unnumbered front matter. Use `\section` for the four required stages, even for a short activity.

After `\maketitle`, set `\setcounter{tocdepth}{1}` and `\setcounter{secnumdepth}{2}`, then put `\phantomsection\label{toc}` immediately before `\tableofcontents`. Follow with `\section*{Evaluated criteria}` and a `description` list containing explicit criterion IDs and exact wording, then preserve the activity-specific **How to practise** instructions. **Evaluated criteria** must remain visible and unnumbered, outside the numbered activity sequence, and must never appear in the contents or PDF outline. Never use `\addcontentsline{toc}{section}{Evaluated criteria}` or any equivalent contents or outline insertion. Insert `\clearpage` before `\section{Introduction}\label{sec:introduction}` and begin its instructional content with `\subsection*{Highlight legend}`.

1. **Introduction** — Make the concise highlight legend the first instructional content, with at most a brief heading or one-sentence lead-in before it. Follow it with at least two short, accessible introductory examples that establish the notation, quantities, units, and relationships used later. These are motivating situations, distinct from General Worked Problems. Add a quick check where it helps.
2. **Notation Reference and Practice Procedure** — Present the detailed notation reference with general definitions and separate contextual meanings in concise example-linked bullets. Follow it with reusable steps for choosing an approach, reasoning through the task, and interpreting or checking the result.
3. **General Worked Problems** — Use numbered problem subsections with self-contained prompts and criterion-linked worked solutions. Where the topic supports a follow-up, ask how a meaningful change to the initial application affects the reasoning and what the available information supports.
4. **Advanced Problems** — Build on the same reasoning at the requested level. Ask students to connect ideas, compare cases or representations, or justify a conclusion under more demanding conditions. Use the linked problem pattern here too.

When distinct concepts, methods, or problem families need separate framing, replace the single General Worked Problems section with two or more consecutive `\section{General Worked Problems --- [Descriptive Focus]}` blocks. Give each block its own section label and linked problem list. This is the only split that adds numbered top-level sections. Keep Advanced Problems last and organize all other material within the four stages using subsections. Put requested independent practice in a distinct subsection within the appropriate stage.

## Complementary tables and introductory examples

The scaffold includes separate three-column concise and four-column detailed tables, with labels `tab:highlight-legend` and `tab:notation-reference`. Reuse them and any existing equivalents on reruns. Preserve a single concept–notation–highlight mapping across both; use shared role macros, not duplicated table bodies. [math-legend-highlight](../../math-legend-highlight/SKILL.md) owns that design and navigation; [math-practice-highlights](../../math-practice-highlights/SKILL.md) owns body markup, renderer integration, diagrams, toggles, and validation. Apply the design once, then the markup; do not loop between skills.

Use **Symbol or notation | Concept | Brief meaning** for the concise legend and **Symbol or notation | Concept | Definition | Meaning in the introductory examples** for the detailed reference. Translate these headers and example labels consistently; Spanish equivalents are given in the legend skill's LaTeX reference. The concise legend contains short meanings and essential notation only. Keep derivations and worked calculations out of it. The detailed table separates general definitions from what each symbol represents in actual introductory situations; use concise bullets such as “Example 1: …”, linked to the corresponding example anchor. Include only relevant examples per row.

Replace each introductory-example placeholder with a short motivating situation, enough givens and units to interpret its notation, and an accessible relationship or interpretation. Do not turn these into extra full worked problems. Do not repeat long explanations in table cells. Tables must not expose answers required in later independent tasks. Keep the front matter and numbered top-level stages intact; any introduction index must not displace the first instructional legend.

The scaffold loads the existing renderer once and places the commented disable toggle immediately after it. Define topic-specific role macros as needed, reuse them in tables and body, and preserve any existing toggle setting when adapting an activity. Highlights off must retain all text and notation. Preserve component roles in composite expressions, including substitutions.

## Procedure families and diagrams

Before composing diagrams, establish each family's meaningful stage names/order, common inputs/outputs, parallel cases or methods, branches, merges, checks and extension points. Declare the structure separately from problem-specific wording/values with `\PPDeclareFamily` and `\PPStage`. Reuse one family where adequate; introduce another only when the reasoning genuinely differs. The [diagram guide](procedure_diagrams.md) owns implementation guidance and runnable examples; the scaffold has clearly marked example invocations rather than a mandatory mathematical model.

After a relevant introductory example, use `PracticeProcedure[mode=detailed]` with its actual data. Explain quantities, symbols, units, cases, arrows, intermediate values and outputs, distinguishing general formulas from substitutions. Introduce every family before its compact use. Preserve the first instructional legend and at least two introductory examples.

In the Practice Procedure subsection, match the written procedure explicitly to the introductory stage names and order and give a generalized compact diagram per family, referring back to the introduction. In every worked task, including follow-ups and advanced solutions, place its actual-value compact summary after the reasoning and before return navigation. Several distinct procedures need appropriate separate summaries or a divided composite. Keep enough substitutions and intermediate values to connect inputs to outputs; diagrams do not replace written justification. Do not supply completed diagrams for unsolved independent or assessed tasks.

Retain the base family's stage identities/order and aligned lanes in variants. Add alternatives as lanes, label an extra calculation inside its existing stage, or insert a meaningfully labelled `\PPExtension` at the correct logical point for a new operation. Branch/rejoin as the mathematics requires; common inputs and unchanged reasoning remain shared. A genuinely different method needs another introduced family and a brief relationship explanation. Consistency concerns reasoning, not identical dimensions or box counts.

Use tall neutral stage rectangles from left to right with parallel cases vertically stacked in consistent lanes. Adapt widths, gaps, padding and explicit math wrapping; split large diagrams at meaningful stage boundaries into clearly linked panels preserving stage identities, case order and continuation quantities. Do not use tiny fonts, whole-diagram scaling, negative spacing or crowded arrows. Reuse semantic roles in all diagram content; neutral frames and connections remain readable with highlights off and in grayscale.

## Navigation

- Keep `\phantomsection\label{toc}` immediately before `\tableofcontents` for the return arrows. Keep **Evaluated criteria** out of both the contents and PDF outline; its starred heading does not need a contents insertion or bookmark command.
- Label each numbered group section and problem subsection just after its heading. At the start of each group, use `\SectionProblemsTableOfContents` with one `\SectionProblemLink{problem-label}{problem title}` per problem. Separate rows with `\\` and omit the final row break.
- Use `\QuestionsTasks[group-label]{entries}` for tasks with linked solutions. Each comma-separated entry takes the form `{criterion suffix}/{solution label}/{task text}`. Brace all three fields to protect commas and slashes in them. The command adds `C` to the first field, so pass the suffix of the actual ID, including any subcriterion suffix. Use full IDs in **Evaluated criteria**.
- Give each linked solution a unique label immediately after its heading. With the shared preamble, a starred solution heading supplies its own hyperlink target. End the solution with `\secInicio[problem-label][group-label]` to provide return links to the contents, the problem, and the group heading above its problem list. For a solution placed elsewhere, use the original problem and group labels for those returns.
- For independent tasks whose solutions are absent from the activity PDF, use a plain criterion-labeled list and point any return navigation to existing anchors. Use the linked task command when solutions appear elsewhere in the same PDF.

## Graphs

Use the [shared graph index](../../../../book/preamble/graphs/README-graphs.md) to discover graph commands. Open the selected macro's definition to confirm its arguments, units or conventions, and dependencies. Add the required `\input{graphs/...}` lines after the shared preamble. Load only the graph files and dependencies used by the activity. Use local TikZ or PGFPlots when no shared command fits.

Place a graph beside its calculation or table when both remain legible. Use two top-aligned `minipage` blocks with `\vspace{0pt}` at the start of each and leave room for the gap between them. Size the graph to its local `\linewidth`. Stack the blocks when the axes, labels, or reasoning need more width. Check that labels, units, scales, domains, and highlighted features agree with the mathematics.

## Build and inspect

Run pdfLaTeX from the activity's source directory so relative inputs resolve from there. Set `$activitySource` to the source filename and `$buildDirectory` to an existing absolute temporary directory to keep build artifacts separate from the source.

```powershell
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$buildDirectory" "$activitySource"
```

Repeat until the contents and cross-references resolve and the log has no undefined references, duplicate destinations, or requests to rerun. Inspect the PDF for legible equations, tables, and graphs, and for clipping or awkward page breaks. Follow the contents entries, problem list links, task links, and return arrows to confirm that each lands at the intended heading or contents.

As a final check, compare the source headings with the numbered entries in the compiled contents. Verify Introduction, Notation Reference and Practice Procedure, General Worked Problems, and Advanced Problems in that order, with Advanced Problems last. If the count exceeds four, verify that every extra heading comes from replacing the single General Worked Problems section with consecutive focused groups and that each group has a linked problem list. Confirm that front matter is unnumbered and that any independent practice sits within its stage.

Confirm **Evaluated criteria** is visible and unnumbered in the rendered front matter but absent from the compiled contents and PDF outline entries. Inspect the source and scaffold for any equivalent contents or outline insertion, not just the literal prohibited command.

Verify concise legend → at least two introductory examples → detailed reference in Section 2 → practice procedure in the source and PDF. Inspect both table schemas, linked contextual bullets, shared semantic treatments, enabled/disabled highlights, grayscale readability, and no duplicate tables or anchors.

Verify detailed introduction → symbolic procedure → every actual-value worked summary for each family, including variants. Check shared-source arrows, corresponding lane alignment, stage/container fit, long labels and multiline equations, clean branch/merge paths, panel continuations and page boundaries. Follow [update-latex-complete](../../update-latex-complete/SKILL.md) and the [diagram validation cases](procedure_diagrams.md#coordination-and-validation) when the asset or integration changes.
