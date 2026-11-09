---
name: global-economics-practice-highlights
description: Add or revise instructional highlights in any LaTeX mathematics document across topics, levels, and document types. Use consistent visual markers to connect mathematical ideas across representations while preserving the source and the reasoning readers are expected to supply.
---

# Instructional Highlights for LaTeX Mathematics

## Choose and apply instructional roles

1. Read the target document and identify what the reader needs to distinguish or connect. Choose a small set of roles grounded in the document's reasoning and assign each role a consistent visual treatment. Name and explain the roles in a short legend near their first substantial use. Preserve meaningful labels, notation, and units so the document remains understandable in grayscale and with markers disabled.
2. Highlight short fragments where the visual connection helps the reader follow the mathematics. Carry each role across prose, notation, equations, tables, diagrams, and graphs where it helps connect those representations. Choose markers by the mathematical meaning in context. Identical symbols or values can serve different roles. Concentrate guidance in explanations and worked solutions. Leave the reasoning that independent or assessed tasks ask students to supply for them to work out.
3. Preserve the source wording, mathematical meaning, data, results, numbering, and links. Apply markers in each fragment's existing text or math mode. In equations, keep alignment tokens, line breaks, relations, and binary operators outside wrappers. In tables, diagrams, and graphs, mark displayed content or use supported visual styling options. Keep table separators, underlying expressions, coordinates, scales, and data intact. Avoid nested markers and check that the added width fits the layout.

## Integrate with LaTeX

- Inspect the target's preamble, inputs, markers, and legends. Reuse an existing highlighting mechanism if it meets the instructional and layout needs.
- In this repository, inspect `book2026-2027/preamble/graphs/highlights.tex` for the current renderer. Load it after the shared preamble using the target's input paths if it is needed and has not already been loaded. `\HighlightStroke{color}{fragment}` takes a valid LaTeX color name available in the target and a short fragment in its current mode. Treat palette names as implementation identifiers and define the meaning of each treatment in the target's legend.
- Use `book2026-2027/preamble/graphs/specific_highlights.tex` only when the target uses or needs the shared legend registry. Load it after the renderer if needed. Call a registered entry with `\PracticeHighlightLegend{key}`. The registry looks up the entry as `\csname practicehighlightlegend@<key>\endcsname`. Follow the current key conventions in the file. The base key is `G<grade>-T<term>-C<criterion>[-C<criterion>...]`, with all applicable criteria in numerical order. Use a lesson or variant suffix only to distinguish legends for the same base key. Reuse a matching entry when its key and legend fit, and preserve unrelated entries. A document without course metadata can use a local legend.

## Verify the target

- Make a second pass over the highlighted source, including documents that already had markers. Check wrappers, inputs, and legend calls for duplication. Reuse or revise existing markup in place so repeating the same edit adds nothing.
- Compile with the target's existing LaTeX engine, build directory, and input paths. Review the diff for source preservation, then inspect the build log and rendered output for legend placement, equation alignment, legible table and graph labels, and overflow.
- Check a temporary build with markers disabled. For the shared renderer, put `\GTenHighlightsfalse` after the shared inputs. If the target's mechanism lacks a disable switch, temporarily suppress the styling while preserving the displayed content. Check that the text and mathematics remain readable and the labels and legend still convey their meaning.
