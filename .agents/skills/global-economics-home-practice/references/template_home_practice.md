# Home Practice Activities Authoring Guide

## Source and shared inputs

Copy the [LaTeX scaffold](../assets/template_home_practice.tex) into the intended source directory. Replace the bracketed placeholders and remove unused optional blocks.

Keep the scaffold's `\input@path` setup and load the [shared preamble](../../../../book2026-2027/preamble/preamble_exams.tex) once. It initializes the document class and loads the shared layout and navigation commands. The relative search paths cover the scaffold's directory and typical activity directories under `book2026-2027/`.

When the output source directory is outside that search range, add the absolute `book2026-2027/preamble/` directory to `TEXINPUTS` for the build session. Include the trailing slash on the directory and an empty path component for TeX's default search paths. This also resolves nested inputs. In PowerShell, use a semicolon as the path separator and replace the placeholder path below. On systems with a POSIX shell, use a colon as the separator.

```powershell
$env:TEXINPUTS = 'C:/path/to/repo/book2026-2027/preamble/;'
```

## Section layout

Keep the title, linked contents, **Evaluated criteria**, and a brief instruction to try each task before opening its solution in the unnumbered front matter. Use `\section` for the four required stages, even for a short activity.

1. **Introduction** — Start with a short, accessible example. Add a quick check about a distinction or a meaningful change where it helps.
2. **Notation Reference and Practice Procedure** — Summarize the relevant notation, definitions, formulas, or representations, then give reusable steps for choosing an approach, reasoning through the task, and interpreting or checking the result.
3. **General Worked Problems** — Use numbered problem subsections with self-contained prompts and criterion-linked worked solutions. Where the topic supports a follow-up, ask how a meaningful change to the initial application affects the reasoning and what the available information supports.
4. **Advanced Problems** — Build on the same reasoning at the requested level. Ask students to connect ideas, compare cases or representations, or justify a conclusion under more demanding conditions. Use the linked problem pattern here too.

When distinct concepts, methods, or problem families need separate framing, replace the single General Worked Problems section with two or more consecutive `\section{General Worked Problems --- [Descriptive Focus]}` blocks. Give each block its own section label and linked problem list. This is the only split that adds numbered top-level sections. Keep Advanced Problems last and organize all other material within the four stages using subsections. Put requested independent practice in a distinct subsection within the appropriate stage.

## Navigation

- Keep `\phantomsection\label{toc}` immediately before `\tableofcontents` for the return arrows. Add an unnumbered front-matter heading to the contents with `\addcontentsline` immediately after its heading if it should appear there.
- Label each numbered group section and problem subsection just after its heading. At the start of each group, use `\SectionProblemsTableOfContents` with one `\SectionProblemLink{problem-label}{problem title}` per problem. Separate rows with `\\` and omit the final row break.
- Use `\QuestionsTasks[group-label]{entries}` for tasks with linked solutions. Each comma-separated entry takes the form `{criterion suffix}/{solution label}/{task text}`. Brace all three fields to protect commas and slashes in them. The command adds `C` to the first field, so pass the suffix of the actual ID, including any subcriterion suffix. Use full IDs in **Evaluated criteria**.
- Give each linked solution a unique label immediately after its heading. With the shared preamble, a starred solution heading supplies its own hyperlink target. End the solution with `\secInicio[problem-label][group-label]` to provide return links to the contents, the problem, and the group heading above its problem list. For a solution placed elsewhere, use the original problem and group labels for those returns.
- For independent tasks whose solutions are absent from the activity PDF, use a plain criterion-labeled list and point any return navigation to existing anchors. Use the linked task command when solutions appear elsewhere in the same PDF.

## Graphs

Use the [shared graph index](../../../../book2026-2027/preamble/graphs/README-graphs.md) to discover graph commands. Open the selected macro's definition to confirm its arguments, units or conventions, and dependencies. Add the required `\input{graphs/...}` lines after the shared preamble. Load only the graph files and dependencies used by the activity. Use local TikZ or PGFPlots when no shared command fits.

Place a graph beside its calculation or table when both remain legible. Use two top-aligned `minipage` blocks with `\vspace{0pt}` at the start of each and leave room for the gap between them. Size the graph to its local `\linewidth`. Stack the blocks when the axes, labels, or reasoning need more width. Check that labels, units, scales, domains, and highlighted features agree with the mathematics.

## Build and inspect

Run pdfLaTeX from the activity's source directory so relative inputs resolve from there. Set `$activitySource` to the source filename and `$buildDirectory` to an existing absolute temporary directory to keep build artifacts separate from the source.

```powershell
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$buildDirectory" "$activitySource"
```

Repeat until the contents and cross-references resolve and the log has no undefined references, duplicate destinations, or requests to rerun. Inspect the PDF for legible equations, tables, and graphs, and for clipping or awkward page breaks. Follow the contents entries, problem list links, task links, and return arrows to confirm that each lands at the intended heading or contents.

As a final check, compare the source headings with the numbered entries in the compiled contents. Verify Introduction, Notation Reference and Practice Procedure, General Worked Problems, and Advanced Problems in that order, with Advanced Problems last. If the count exceeds four, verify that every extra heading comes from replacing the single General Worked Problems section with consecutive focused groups and that each group has a linked problem list. Confirm that front matter is unnumbered and that any independent practice sits within its stage.
