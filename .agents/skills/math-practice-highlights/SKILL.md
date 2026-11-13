---
name: math-practice-highlights
description: Apply and validate semantic instructional highlights in mathematical practice documents across topics, levels, and native formats. Connect concepts, notation, and values while preserving content and assessment boundaries.
---

# Math Practice Highlights

Own the general highlighting workflow: document-wide application of an agreed semantic mapping, detailed markup mechanics, renderer integration, diagram styling, toggle behavior, and validation. Work in the native format; the LaTeX integration below is conditional guidance.

## Establish the guide and shared mapping

Inspect the complete source, dependencies, existing styles, toggles, guides and legends before editing. When the guide or legend is missing, inadequate, or inconsistent, read and apply [math-key-terms-highlight-guide](../math-key-terms-highlight-guide/SKILL.md) first, then resume here. That skill identifies concepts, notation and relationships; designs the semantic mapping and authoritative conceptual legend; and owns opening placement, hierarchy, anchors and navigation. This skill applies the agreed mapping throughout the document.

If both skills are already active, continue with the next unfinished responsibility rather than invoking either again. Share one semantic mapping, one authoritative legend per guide, and the existing styling infrastructure. Reuse completed work on reruns. If the companion is unavailable, establish a concise conceptual legend locally and continue this standalone workflow; report the limitation.

## Choose and apply instructional roles

1. Read the target document and confirm what the reader needs to distinguish or connect. Reuse the guide's agreed semantic roles and authoritative legend. If either needs redesign, complete the guide responsibility above first; then apply each role's consistent visual treatment. Preserve meaningful labels, notation, and units so the document remains understandable in grayscale and with markers disabled.
2. Highlight short fragments where the visual connection helps the reader follow the mathematics. Carry each role across prose, notation, equations, tables, diagrams, and graphs where it helps connect those representations. Choose markers by the mathematical meaning in context. Identical symbols or values can serve different roles. Concentrate guidance in explanations and worked solutions. Leave the reasoning that independent or assessed tasks ask students to supply for them to work out.
3. Preserve the source wording, mathematical meaning, data, results, numbering, and links. Apply markers in each fragment's existing text or math mode. In equations, keep alignment tokens, line breaks, relations, and binary operators outside wrappers. In tables, diagrams, and graphs, mark displayed content or use supported visual styling options. Keep table separators, underlying expressions, coordinates, scales, and data intact. Avoid nested markers and check that the added width fits the layout.

Treat a concept's name, complete notation, and associated numerical values as one semantic role wherever instructional highlighting is appropriate. Whenever a symbol is highlighted, highlight its associated name and values in the relevant explanation, table or worked calculation. Audit prose, notation, substitutions, intermediate calculations, results, table headings, diagrams and graph labels.

Determine roles by mathematical meaning in context, never by global token or number replacement. The same value may be a margin in one calculation and a width in another. Preserve each component's role inside a composite formula, including numerical substitutions. For example, in MoE = z* × SE, each quantity retains its own treatment. Keep wrappers short, leave connecting operators and alignment syntax outside them, and keep meaningful accents and subscripts with their complete symbol.

Use related color families when helpful, but visibly distinguish distinct concepts. For example, confidence level, C, 95% and the equivalent central probability 0.95 share a treatment; standard normal critical value, z*, and 1.96 share another. Related blue shades could express that relationship in an interval lesson; these concepts and blue are not requirements for other topics. Assign graph regions by meaning: tail and cumulative probabilities do not automatically have the confidence-level role.

Choose colors using the actual renderer, including its opacity and background. Inspect readable glyph contrast and useful distinctions at normal viewing size. Retain labels, notation and units so color is never the only means of understanding. Reuse the existing toggle and preserve its setting. With highlights disabled, retain all text and mathematical content, including diagram labels and legends. Concentrate guidance in explanations and worked solutions; do not expose answers or reasoning students must supply in independent or assessed tasks.

## Integrate with LaTeX

- Inspect the target's preamble, inputs, markers, and legends. Reuse an existing highlighting mechanism if it meets the instructional and layout needs.
- In this repository, inspect `book2026-2027/preamble/graphs/highlights.tex` for the current renderer. Load it after the shared preamble using the target's input paths if it is needed and has not already been loaded. `\HighlightStroke{color}{fragment}` takes a valid LaTeX color name available in the target and a short fragment in its current mode. Treat palette names as implementation identifiers and define the meaning of each treatment in the target's legend.
- Whenever you add instructional highlighting, ensure the document has exactly one toggle near the top, immediately after the input or definition that makes `\GTenHighlightsfalse` available. For a new toggle, add `% \GTenHighlightsfalse % Uncomment to disable instructional highlights.` and leave it commented. When revisiting a document, reuse its existing toggle and preserve whether it is commented or active.
- Make all document-specific instructional styling, including graph highlights where present, honor `\ifGTenHighlights`. If the target does not use the shared renderer, provide the same switch with highlighting enabled by default. When disabled, suppress the styling while retaining the text, equations, tables, graph data and labels, and legend text. Commenting out or removing the toggle must restore the default highlighted rendering.
- Use `book2026-2027/preamble/graphs/specific_highlights.tex` only when the target uses or needs the shared legend registry. Load it after the renderer if needed. Call a registered entry with `\PracticeHighlightLegend{key}`. The registry looks up the entry as `\csname practicehighlightlegend@<key>\endcsname`. Follow the current key conventions in the file. The base key is `G<grade>-T<term>-C<criterion>[-C<criterion>...]`, with all applicable criteria in numerical order. Use a lesson or variant suffix only to distinguish legends for the same base key. Reuse a matching entry when its key and legend fit, and preserve unrelated entries. A document without course metadata can use a local legend.

## Verify the target

- Make a second pass over the highlighted source, including documents that already had markers. Check wrappers, inputs, and legend calls for duplication. Reuse or revise existing markup in place so repeating the same edit adds nothing.
- Build or export with the established native toolchain. For LaTeX, compile with the target's existing engine, build directory, and input paths. Review the diff for source preservation, then inspect the build log and rendered output for legend placement, equation alignment, legible table and graph labels, and overflow.
- Build isolated enabled and disabled copies using the native styling mechanism; for LaTeX, compile temporary copies with the same toggle commented and uncommented. Check the default rendering and verify that the disabled build retains readable content, including graph labels and the legend. Preserve the toggle's source setting after verification.

- For other native formats, use their established styles and export workflow with the same semantic mapping and content-preserving toggle behavior; do not convert merely to use LaTeX commands.
- Review source differences for preserved content and check concept–symbol–value agreement across representations. Before shared-definition edits, inspect their consumers, preserve unrelated registry entries and reference documents, and verify affected outputs. Compare designated reference renders before and after supporting changes.
- Validate the actual rendered palette, including distinct roles in related families and mixed-role substitutions. Check accessibility with disabled highlights and grayscale. Reuse existing wrappers, inputs, toggles and guides on reruns; no duplicate work should accumulate. Deliver revised native sources and supported exports, stating precisely which checks could not be completed.
