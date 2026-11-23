# Layout and build mechanics

The starter follows title → complete consolidated legend → classroom worked examples → brief synthesis. Replace placeholders with the paired sources and a faithful resolved snapshot of the live legend. Keep all required definitions inline.

## Legend resolution and layout

Trace the practice legend identifier through the registry membership, chosen renderer, context overrides, inherited fields, role wrappers, and palette aliases. The renderer is part of the authority: a context-only row deliberately excluded by that renderer is not a missing printed legend row. Record both membership and rendered-row inventory in temporary notes or comments. Preserve every printed row, notation, name, and meaning; split into consecutive frames using Symbol or notation | Concept | Brief meaning. Repeat headers and keep readable widths. Do not force long tables into one slide or add a competing detailed opening reference.

## Slide highlight renderer

The inline length `\GEHighlightVerticalPadding` is the single slide-level control for padding above and below content. Use `\setlength{\GEHighlightVerticalPadding}{.5mm}` by default: `.5mm` per side, 1 mm total added height. The common `ge marker` style consumes it as `inner ysep=\GEHighlightVerticalPadding`. Every semantic wrapper must delegate to `\GEHighlight`, directly or through aliases such as `\HighlightStroke`, including prose, equations, tables, substituted values, results, and diagram labels. Remove hard-coded or wrapper-local vertical-padding overrides from slide renderers.

Keep `baseline=(gehl.base)` on text/math nodes and `\mathpalette\GEHighlightMath` with `$\m@th#1#2$` for display, text, script, and scriptscript sizing. Padding is independent of math style. Preserve role colors, `.32` fill opacity, opaque ink text, `.6mm` horizontal padding, 1 mm corners, no outline, and the plain-content disabled branch. Inline the parameter and renderer in every standalone deck. This default is for slides only: preserve consolidated registry membership/mapping and printable practice/classroom renderers.

Inspect wrapped prose, fractions, subscripts/superscripts, table rows/rules, equation blocks, substitutions/results, and graph-label nodes. Check early/intermediate/final overlays for clearance, clipping, baselines, and stable reserved geometry. Reflow blocks or adjust local row/label spacing if taller markers crowd content, without shrinking text, removing content, or changing overlay timing. Compile and inspect a disabled copy; do not introduce padding into its plain-content branch.

## Stable reveals and diagrams

Keep the question visible while reasoning, substitution, calculation, and interpretation appear in order. Reserve final dimensions with explicit `\visible<2->{...}` or equivalent. For paragraph cells, `\GERevealCell{2}{...}` enters horizontal mode before the reveal. Keep rules, rows, relation signs, alignment separators, and operators outside markers/reveals as appropriate. Use fixed-width or X prose columns, numeric alignment for values, and split wide tables instead of scaling.

Use paired `.485\textwidth` columns when useful and local `\linewidth` inside them. Give TikZ diagrams fixed bounds across overlays. Redraw source diagrams with original axes, units, precision, identifiers, and full datasets. Transfer semantic graph treatments from the practice to the classroom data, including coordinate components. Do not accidentally import the practice's different example data or identifiers. Explain concepts as they become necessary within the selected classroom examples; preserve explanatory comparisons and conclusions.

## Portable build and inspection

1. Copy the final `.tex` and any essential delivered assets into an isolated temporary directory, preventing accidental success through repository search paths. Clear inherited `TEXINPUTS`/`BIBINPUTS` additions that point into the repository for this check. Standard TeX distribution packages remain available.
2. Create a `build` subdirectory and run from the isolated directory:

   ```text
   pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build lesson.tex
   ```

   Use a suitable installed engine if the source language requires it. Run at least twice and repeat if references/totals still change or the log requests reruns. Stop and diagnose repeated failures rather than looping indefinitely. Compare settled auxiliary files or extracted footer totals across runs. Resolve overfull boxes, undefined references, missing characters, and errors. Copy only the matching PDF beside the delivered source.
3. Read `.nav` entries `\beamer@framepages{first}{last}` to map logical frames to physical PDF pages. `\inserttotalframenumber` counts frames, while PDF pages include overlays. Keep the opening legend numbered; avoid `noframenumbering`, `allowframebreaks`, or counter manipulation unless explicitly required and verified.
4. Render selected pages with `pdftoppm -f <page> -l <page> -scale-to 1600 -png <pdf> <prefix>` or another available renderer. Inspect first, middle, and last overlays of representative frames plus every suspected layout/timing risk. Text extraction can check wording and footer numbers, but Beamer may leave visually hidden text extractable: verify answer timing in rendered overlays. Compare stable elements across overlays, including table rules and long cells.
5. If a compiler or renderer is unavailable, deliver portable source and identify unperformed checks. Never reuse an older PDF as if it matched the new source.

6. Compile isolated enabled/disabled copies using the starter toggle, preserving its delivered setting. Render both and a grayscale copy to check that table text, full notation, associated values, component roles, diagrams, and labels remain understandable without highlights.
