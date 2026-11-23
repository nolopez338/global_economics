---
name: global-economics-slides
description: Create standalone student-facing LaTeX Beamer lessons with a live consolidated highlight legend, step-by-step classroom worked examples, and a brief synthesis.
---

# Global Economics Slides

## Sources and scope

Identify the corresponding practice and classroom activity from the requested book year, grade, term, lesson, and criterion. Follow applicable repository instructions; infer routine metadata, language, and destination from the request and sources. Ask only about essential unresolved source identity or boundaries. A topic-only brief does not authorize an invented lesson.

Use the practice to identify the applicable consolidated highlight legend and semantic mapping. Use **all examples explicitly designated as worked examples in the classroom activity** as the main instructional content, unless the user selects a narrower set. Keep each example's context and identifiers distinct. Exclude guided examples, independent exercises, and their solutions unless explicitly requested. Read prerequisite definitions, instructions, and assumptions only as needed to explain the selected examples faithfully. The practice introduction is not a required teaching sequence or an additional content allowance.

Preserve context, assumptions, tasks, data, notation, formulas, calculations, precision, units, graphs, explanatory diagrams, comparisons, interpretations, and conclusions. Reorganize or condense faithfully; add no unrelated situations, exercises, or substantive extensions. Report missing solutions or prerequisites and substantive source inconsistencies instead of silently inventing replacements. Do not modify source activities without authorization. Official criterion wording does not expand instructional scope.

Keep a source map in deck comments or temporary notes: both activity paths, example boundaries and identifiers, solution and prerequisite locations, registry identifier and renderer, metadata, and frame-to-source locations. Audit instructional fragments against it.

## Sequence and classroom development

Default sequence: **title → complete consolidated highlight legend → step-by-step classroom worked example(s) → brief synthesis**.

The title is the first frame and includes the topic, available lesson metadata, and verbatim official criterion wording with its identifier. Preserve each criterion when multiple apply. Disclose missing metadata or official text. If criterion continuation is necessary, place it after the consecutive opening legend frames.

Immediately after the title, show the applicable live consolidated legend using **Symbol or notation | Concept | Brief meaning**. Resolve the source identifier through the shared registry and renderer definitions, including source-local overrides, inherited fields, palette aliases, and intentional renderer filtering. Preserve every rendered row, registered concept, notation, meaning, and semantic color. Do not replace it with a manually chosen subset or a new palette. Split the complete legend across consecutive readable frames with repeated headers; never omit rows or use unreadable text to force fit. If selection is missing or ambiguous, report the specific gap instead of inventing a legend. Inline a faithful resolved snapshot for portability, recording its origin in comments.

Introduce and connect concepts when needed in each classroom example. Develop **context and question → relevant concept and notation → formula → substitution → calculation → graphical representation → contextual interpretation**. Use as many readable frames as necessary; preserve source comparisons and explanatory diagrams. Present tasks before revealing answers; use stable overlays for progressive reasoning and results. End with a short synthesis derived from the selected examples. A detailed notation reference or closing legend is optional only when it serves a teaching purpose; neither is a required opening or closing, and neither should duplicate content gratuitously.

Reuse the established mapping. Consult [math-legend-highlight](../math-legend-highlight/SKILL.md) only for unresolved table/mapping design and [math-practice-highlights](../math-practice-highlights/SKILL.md) only for unresolved application mechanics. These companions do not expand source scope or override this sequence.

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
| Highlights | Baseline-aligned rounded marker, 1 mm corners; role-color fill at `.32` opacity; opaque ink text; `.6mm` horizontal padding; `\GEHighlightVerticalPadding=.5mm` above and below content, no outline |

Use readable text and restrained emphasis. Use `\small` only for compact legends or table labels when needed. Split crowded frames before reducing type size; avoid `shrink`, whole-frame scaling, and decoration unrelated to instruction.

## Semantic meaning and stable overlays

Apply the consolidated mapping throughout prose, equations, substituted values, results, tables, and diagrams. Use the corresponding practice's graph treatments where they implement that mapping: curves, markers, shading, axis notation, and coordinate components must follow their mathematical roles. Preserve axis orientation, data, units, and precision. Distinguish nominal confidence from model coverage when rounded cutoffs differ. Copy required definitions inline; never invent a palette. Labels and notation must remain understandable in grayscale and with highlights disabled. Keep all content when the inline switch is off and preserve the source's delivered toggle setting.

Use the single slide-only length `\GEHighlightVerticalPadding` (default `.5mm` per side) through `ge marker` for every highlight wrapper in prose, equations, tables, substitutions, results, and diagram labels. Keep the parameter and renderer inline. Preserve baseline alignment and all mathematical styles, including subscripts/superscripts. Keep registry semantics, printable practice/classroom padding, colors, opacity, horizontal padding, corners, and disabled behavior unchanged. See [renderer mechanics](references/layout-and-build.md#slide-highlight-renderer).

Use short baseline-aligned highlights; do not nest markers or highlight entire derivations. Keep relation signs, alignment separators, and line breaks outside markers. Present questions before answers, checking captions, diagrams, and earlier tables for premature exposure. Use explicit indices and space-reserving `\visible` or equivalent; `\GERevealCell` handles paragraph cells. Reserve final equation/table geometry and fixed diagram bounds on every overlay. The final overlay must form a complete coherent frame. Use logical Beamer frame counters, never physical PDF page numbers.

## Destination and portability

Honor an explicit destination. Otherwise inspect neighboring directories and filenames, derive the corresponding slides folder in the same book/grade/term, and retain lesson, criterion ordering, and meaningful variant suffixes. The usual pattern is `book<year>/grade<grade>/term_<term>/3-slides/G<grade>_T<term>_L<lesson>_<criteria>_slides.tex`; follow actual local conventions when they differ. Do not invent metadata merely to satisfy this pattern.

Keep theme, macros, highlight definitions, role colors, and styling inline in every delivered `.tex`. Use standard packages and local drawings where practical. Inline or reproduce required representations; if an external asset is essential, supply a portable copy beside the deck with relative references. Compiling must not require the practice source, repository preambles, another skill, or absolute resource paths.

Deliver `.tex` and, when LaTeX is available, a matching PDF beside it. Keep auxiliaries and inspection images in an isolated build directory. Report the selected example, any coverage limitation, validation results, and unperformed checks.

## Validation checklist

- [ ] Verify paired sources and the selected classroom worked-example boundaries; include all designated examples unless narrowed by the user. Exclude guided/independent work and unrelated practice material. Record prerequisites and the frame source map.
- [ ] Resolve the exact legend identifier, renderer, overrides, inherited meanings, palette, and intentional filtering. Compare all rendered rows against the complete consecutive opening legend; disclose missing/ambiguous definitions.
- [ ] Verify title and verbatim official criteria, title → legend → worked examples → synthesis order, readable three-column legend, and any optional reference's teaching purpose.
- [ ] Check all tasks, calculations, assumptions, precision, units, graphs, explanatory comparisons, interpretations, and conclusions against sources. Surface substantive source inconsistencies.
- [ ] Check semantic roles in text, substitutions, results, axes, markers, shading, curves, and coordinate components. Preserve source orientation and identifiers; distinguish nominal and theoretical quantities.
- [ ] Verify the single inline `\GEHighlightVerticalPadding` length (`.5mm` per side by default) reaches every highlight wrapper, with no conflicting slide defaults. Preserve registry semantics, printable renderers, other marker properties, baseline alignment, math styles, and disabled behavior.
- [ ] Compile isolated portable sources at least twice and until references and frame totals settle. Resolve errors, relevant warnings, missing glyphs, and overfull boxes.
- [ ] Render and inspect all final logical frames plus representative early/intermediate overlays, covering the title, entire legend, tasks, dense tables/equations, graphs, comparisons, and synthesis. Expand inspection for layout/timing risks.
- [ ] Check clipping, highlight clearance above/below content, baseline alignment (including subscripts/superscripts), readability, stable placement, task-before-answer timing, section labels, and logical frame totals.
- [ ] Compile and inspect temporary highlights-disabled and grayscale versions for retained content and understandable roles; preserve the delivered toggle setting.
- [ ] Fix and recheck affected frames. Report actual validation, coverage limitations, and any checks that could not run.
