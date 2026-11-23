# Renderer

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_renderer.tex](highlights_renderer.tex), [highlights.tex](highlights.tex).

`\HighlightStroke{color}{fragment}` and the captured command alias `\GTenHLStroke` draw a TikZ rectangle behind one short fragment in its current mode. The `gten marker` style uses rounded corners 1 mm, no outline, fill opacity .32, text opacity 1, inner padding 1.5 mm horizontally / .8 mm vertically, and outer separation zero. The node baseline is the content baseline.

In math, `\GTenHLMathStroke` uses `\mathpalette` with local `\GTenHLCurrentColor` and zero `\mathsurround`; display, text and script sizes follow their surroundings. In text, the node contains ordinary text. Use `\text{...}` for prose inside math. Do not nest markers; keep alignment tokens, row breaks, relations and binary operators outside short wrapped atoms.

`\ifGTenHighlights` is the only shared switch. `\GTenHighlightstrue` is the initial default; `\GTenHighlightsfalse` returns the complete fragment unchanged. The repeated-input guard prevents accidental resets. Graph helpers must test the same switch and preserve curves, values and labels when fills are disabled. `\COneTonePracticePalette` owns opt-in density/area styles; see [palette behavior](specific_highlights_palette.md).

The renderer requires TikZ without package options. It does not load tables or records. Color definitions belong to the palette, semantic meanings to roles, and mathematical entries to datasets. Changing marker padding affects every caller: compile practices, slides and all viewers, including disabled and grayscale variants.
