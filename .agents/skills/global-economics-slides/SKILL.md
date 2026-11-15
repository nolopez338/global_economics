---
name: global-economics-slides
description: Create standalone student-facing LaTeX Beamer lessons from a Global Economics practice activity, using its introduction, complementary notation tables, and exactly one full worked example.
---

# Global Economics Slides

## Source and autonomy

Accept a practice supplied by path or clearly identified in the task, including a newly authored activity. Locate it and follow applicable repository instructions. Infer language, grade, term, lesson, criteria, book year, and destination from the source and task context. Make routine pedagogical and technical decisions autonomously. Ask only for essential missing information or genuinely ambiguous source identity, boundaries, or metadata. A topic-only brief is insufficient: obtain the identified practice instead of inventing a lesson.

**All instructional content must come from the introduction (including its introductory examples), concise highlight legend, detailed notation reference, and exactly one selected full worked example from that same practice.**

- Locate the introduction's structural boundaries: include its subsections, introductory examples, motivating situations, quick checks, and answers; stop at the next peer section. Separately locate the concise legend and detailed notation reference, including a reference in a separate section. Permission to use either table does not extend to the rest of its section or its cross-references.
- Inventory available worked examples and solution links. Select one clear, representative example that best reinforces or applies the introduction, preferring complete available solutions. Keep its statement, related tasks, reasoning, calculations, and contextual conclusions together across as many frames as needed. Do not combine examples. When one model offers alternative wordings, choose one wording/context and its matching shared solution, rather than teaching all alternatives.
- Read metadata and official criterion wording elsewhere only for the opening and objective. Read referenced macros, legends, and assets to decode or reproduce permitted content, honoring source-local overrides. This does not authorize importing unrelated instructional material from those dependencies.
- Permit the concise legend and detailed notation reference even when the latter is separate from the introduction, but exclude the rest of Section 2's practice procedures, unrelated worked examples, advanced problems, and external explanations. Introductory examples belong to the permitted introduction and do not count toward the exactly-one-full-worked-example limit.
- Summaries, diagrams, and classroom questions may reorganize or represent permitted material, but must add no substantive explanations, situations, data, exercises, or extensions. Derive an unprinted quick-check answer only from its permitted givens. Report missing solutions or prerequisites; ask only if the gap prevents a faithful deck. Never fill it from excluded sections.
- If an older source lacks either required table, has fewer than two introductory examples, or lacks a situation needed for an interpretation, report the specific gap. Adapt available material faithfully; do not invent missing situations, definitions, or table content. Faithful condensation or reformatting of permitted source material is allowed, with missing content disclosed. Revise the practice itself only when source revision is also authorized.
- If the allowance covers only part of the official criterion, preserve the scope and report the coverage limitation. The criterion wording does not authorize extra teaching content.

Before drafting, keep a working source map: introduction boundaries and introductory-example anchors, both table locations (including any separate reference), selected full example identifier and solution locations, metadata, and frame-to-source locators. Store it in source comments or temporary notes, not student-facing slides. Audit all instructional fragments against it.

## Lesson decisions

The title is always the first slide, with the topic, available lesson metadata, and verbatim official criterion wording with its identifier. Preserve each wording for multiple criteria; place any necessary criterion continuation after the consecutive opening detailed-reference frames, never between title and reference. Do not invent unavailable official wording or metadata; disclose missing fields. Distinguish any paraphrased learning objective from the official text and keep it within the allowance.

Use the introduction as the foundation. Begin the detailed reference on logical frame 2. Within those opening frames, briefly establish each source introductory situation before revealing interpretations that depend on it; a compact source-derived setup above the table or a reserved situation panel may precede its contextual bullets. Use the source's own example identifiers consistently. Continue with the remaining introduction and selected full worked example, without repeating setups unnecessarily. If a source situation is missing, disclose the gap rather than inventing one.

Include all introduction quick checks, with answers revealed after a response opportunity. Develop exactly one worked example through setup, tasks, reasoning, calculations, and contextual conclusions. Preserve definitions, notation, assumptions, values, precision, units, and contextual boundaries. When the selected example develops an introductory situation, identify the transition into the complete application rather than repeating its setup unnecessarily.

Use one main idea per frame. Split long explanations and calculations into readable stages. Use paired columns for comparisons, displayed equations for calculations, and locally drawn diagrams when they clarify permitted content. Place a compact summary derived solely from the introduction and selected example, and any final interpretation check, before the mandatory closing legend. Nothing follows that final legend. Adapt the intervening frame count and sequence to the material; there is no fixed storyboard.

## Opening detailed reference and closing concise legend

Use this logical sequence: **title → progressive detailed notation reference beginning on frame 2 → remaining lesson content → concise highlight legend last**. Nothing follows the final legend. The opening reference may span consecutive frames for readability; repeat column meanings and necessary identifiers. Do not insert unrelated frames into that opening sequence or shrink an overcrowded table into one frame.

Use the detailed schema **Symbol or notation | Concept | Definition | Meaning in the introductory examples**. Distinguish general definitions from concise contextual bullets explicitly linked to relevant source examples (“Example 1: …”, “Example 2: …”). Do not force an irrelevant example into a row. Translate headings and example labels consistently. Reveal concepts, complete notation, definitions, and contextual meanings in a meaningful teaching order using stable cell overlays that reserve final dimensions. Establish each source introductory situation before revealing the dependent interpretations. Table rules, column widths, row heights, and semantic treatments remain stable within each frame.

End with the distinct concise schema **Symbol or notation | Concept | Brief meaning**. Show the complete closing legend immediately, without progressive reveals, readably within one logical frame. Include essential notation and short meanings only; omit extended explanations, derivations, and worked calculations. It summarizes the opening reference rather than copying its complete table. Use concise wording and appropriate column proportions; do not use tiny fonts or scaling to force fit.

Both tables use one source-faithful concept–notation–highlight mapping, including associated values where useful and component roles within composite expressions. Neither may expose answers students should derive independently. [math-legend-highlight](../math-legend-highlight/SKILL.md) owns concept/notation identification, mapping, table designs, hierarchy, anchors, and navigation. [math-practice-highlights](../math-practice-highlights/SKILL.md) owns mapping application, markup, renderers, diagrams, toggles, and validation. This slides skill owns source boundaries, frame sequence, progressive presentation, and the closing summary. Reuse completed mapping and table design; consult a companion only for its unfinished responsibility, without circular invocation or importing excluded source material.

## Visual system

Copy [assets/beamer_starter.tex](assets/beamer_starter.tex), retaining its inline preamble. Replace neutral metadata and the empty criterion before delivery, then author source-derived frames. Read [references/layout-and-build.md](references/layout-and-build.md) for optional mechanical patterns and build checks.

| Element | Default |
| --- | --- |
| Canvas | `beamer`, `12pt`, `aspectratio=169`, white background |
| Colors | Ink `132A3E`; teal structure/accent `17675E`; pale teal footer `EAF2F1` |
| Typography | T1 Latin Modern sans serif text; standard Beamer math; body `\normalsize`; frame titles `\Large\bfseries` |
| Opening | Left aligned, vertically balanced with `\vfill`; teal bold metadata, `\medskip`, ink `\huge\bfseries` topic, `\bigskip`, normal-size official criterion; omit author/date unless supplied |
| Content | Top-aligned `[t]` frames, ragged-right prose, 9 mm side margins; title top skip `.5em`, bottom skip `.25em`; paragraph skip `.35em`, no indent; `\medskip` between conceptual blocks |
| Tables/comparisons | Top-aligned paired columns `.485\textwidth` each; tables at local `\linewidth`; ragged-right prose cells, aligned numeric cells; `booktabs` horizontal rules, no vertical rules; `\arraystretch=1.22`, `\tabcolsep=4pt` |
| Equations | Centered displays; `aligned` at relation signs; above/below display skips `6pt plus 2pt minus 2pt`; operators outside highlights |
| Footer | Full width, height `3ex`, depth `1.3ex`, 9 mm side insets; teal `\footnotesize`; short current section left, logical `frame/total` right; title included in total; hidden navigation icons; no automatic section-divider frames |
| Highlights | Baseline-aligned rounded marker, 1 mm corners; role-color fill at `.32` opacity; opaque ink text; `.6mm` horizontal and `.3mm` vertical padding, no outline |

Use readable text and restrained emphasis. Use `\small` only for compact legends or table labels when needed. Split crowded frames before reducing type size; avoid `shrink`, whole-frame scaling, and decoration unrelated to instruction.

## Semantic highlights and overlays

Derive roles from permitted content and its highlight guide. Preserve meaningful conceptual color families and distinctions when available; there is no mandated topic palette. Define all used role colors and highlight macros inline in each deck. Exclude unrelated registry material while preserving essential permitted notation across the detailed opening reference and concise closing legend. Use `\GEHighlight{<role color>}{<short text or math>}` consistently across contextual descriptions, symbols, values, tables, equations, and diagram labels. Labels and notation must communicate meaning in grayscale and with highlights disabled. Preserve source toggle settings; use the inline highlight switch for standalone decks and retain every textual and mathematical element when disabled. Do not nest markers or highlight entire derivations.

Present each question/task before its answer. Reveal reasoning, substitutions, results, and interpretations in teaching order with `\visible` or an equivalent that reserves space. Reveal table content within cells, keeping widths, rows, and rules stable; `\GERevealCell{<first overlay>}{<content>}` handles paragraph-cell mode. Reserve equation and diagram space likewise. Check headings, legends, captions, repeated tables, and earlier overlays for accidental answer exposure. Avoid shifting content and overlays without a teaching purpose. The final overlay must form a complete, coherent frame. Use logical Beamer frame counters, never physical PDF page numbers, so all overlays retain the same frame number.

## Destination and portability

Honor an explicit destination. Otherwise inspect neighboring directories and filenames, derive the corresponding slides folder in the same book/grade/term, and retain lesson, criterion ordering, and meaningful variant suffixes. The usual pattern is `book<year>/grade<grade>/term_<term>/3-slides/G<grade>_T<term>_L<lesson>_<criteria>_slides.tex`; follow actual local conventions when they differ. Do not invent metadata merely to satisfy this pattern.

Keep theme, macros, highlight definitions, role colors, and styling inline in every delivered `.tex`. Use standard packages and local drawings where practical. Inline or reproduce required representations; if an external asset is essential, supply a portable copy beside the deck with relative references. Compiling must not require the practice source, repository preambles, another skill, or absolute resource paths.

Deliver `.tex` and, when LaTeX is available, a matching PDF beside it. Keep auxiliaries and inspection images in an isolated build directory. Report the selected example, any coverage limitation, validation results, and unperformed checks.

## Operational validation checklist

- [ ] Audit the source map: all instructional content comes from the introduction and its introductory examples, both permitted tables (including a separate reference), and exactly one full worked example; no leakage from the rest of Section 2, cross-references, procedures, unrelated examples, or advanced problems. Report missing source tables or situations.
- [ ] Verify mathematical accuracy, notation, assumptions, precision, units, and interpretations. Surface source inconsistencies instead of silently changing substantive givens.
- [ ] Check summaries, questions, and diagrams for new substantive content; verify official wording and report coverage gaps.
- [ ] Verify title first; progressive detailed reference beginning on logical frame 2 and continuing consecutively if needed; remaining lesson; distinct concise legend last with nothing after it. Check both schemas and shared mapping, situation-before-interpretation timing, stable cell geometry, readable opening frames, and fully visible single-frame closing content without reveals.
- [ ] Compile portable delivery sources in isolation at least twice and until references and frame totals settle. Resolve errors, relevant warnings, missing glyphs, and overfull boxes.
- [ ] Render and inspect representative early, intermediate, and final overlays, covering opening, quick checks, dense tables/equations, the worked example, and summary. Expand inspection for any timing or layout risk.
- [ ] Check clipping, readability, table fit, stable placement, answer timing, short section labels, and logical frame numbering across overlays and at the final total.
- [ ] Inspect temporary enabled/disabled and grayscale renders for retained content, readable notation, and component roles; preserve the delivered source toggle setting.
- [ ] Fix discovered problems and recheck affected frames. Report checks that could not run; do not claim compilation or visual inspection without performing it.
