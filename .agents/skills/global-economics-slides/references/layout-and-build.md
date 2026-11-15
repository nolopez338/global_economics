# Layout and build mechanics

The starter demonstrates title → progressive detailed reference → lesson insertion point → concise closing legend. Replace neutral placeholders with permitted source material; they are not source content. Use the optional layout patterns below as needed.

## Stable reveals

The starter defines separate `\GEDetailedNotationReference` and `\GEConciseHighlightLegend` bodies, sharing the same source-derived role macros. The detailed table begins on logical frame 2; use `\GERevealCell{<first overlay>}{<content>}` within cells, keeping rules and row breaks outside. Briefly establish the source introductory situation in a reserved panel before revealing contextual interpretations. For example, situation 1 at overlay 1 precedes its meaning at overlay 3; situation 2 at overlay 4 precedes its meaning at overlay 5. Adapt the teaching sequence to the source rather than revealing arbitrary rows.

Preserve the four detailed columns: **Symbol or notation | Concept | Definition | Meaning in the introductory examples**. Use concise bullets identifying the relevant introductory examples, and distinguish general definitions from those interpretations. Translate headers and example labels consistently. Split a crowded detailed reference across consecutive opening frames with repeated headers, stable widths, and matching roles; keep source setups beside the relevant rows. Do not shrink or scale it to force a single-frame fit.

The closing is a separate three-column **Symbol or notation | Concept | Brief meaning** table, fully visible with no reveal wrappers. Keep it concise and readable within one frame: no derivations, worked calculations, or long definitions. It summarizes the opening, so compare shared notation and roles rather than identical geometry or wording. Reuse existing table identities and shared macros on reruns; do not accumulate duplicate tables or legacy aliases that print an extra legend.

Check logical frame 1 is the title, detailed reference begins at 2 and continues consecutively if split, lesson content follows, and concise legend is last with one fully visible overlay. Any criterion continuation, summary, or final check precedes that closing legend. Inspect opening overlays for stable geometry and for source situation setup before each dependent contextual bullet. Source permission includes the two tables and introduction's examples, not the rest of a separate notation section's procedures or other worked problems.

Use explicit overlay indices when questions and answers share a frame. Keep the question visible through the final overlay. Reserve the answer's final height and width with `\visible<2->{...}`. In multiline equations, put `\visible` around individual lines in `aligned` rather than removing rows. Keep `&`, line breaks, and operators outside highlights. Use `\text{...}` for prose in math markers. The starter uses `\mathpalette` so subscripts and display math retain their mathematical sizes.

For prose tables, `\GERevealCell` enters horizontal mode before a hidden paragraph cell to avoid a spacing change on its first visible overlay. Keep rules and row breaks outside reveals:

```latex
\begin{tabularx}{\linewidth}{@{}*{2}{>{\raggedright\arraybackslash}X}@{}}
  \toprule
  \textbf{Task} & \textbf{Response} \\
  \midrule
  % Replace both arguments with the source question and its answer.
  \GERevealCell{1}{Source question} &
  \GERevealCell{2}{Source answer} \\
  \bottomrule
\end{tabularx}
```

Reserve the entire final table on every overlay. Use fixed-width or `X` columns for prose and `r`/`c` for short numbers. Split wide tables into intelligible stages with repeated identifiers instead of scaling them down. Never reveal a whole table after a differently sized placeholder.

For paired content, use `\begin{columns}[T,onlytextwidth]` with two `\begin{column}{.485\textwidth}` blocks. Use `\linewidth` within columns. Align headings and keep long equations out of narrow columns.

For diagrams, specify a fixed TikZ bounding box across overlays and reveal nodes/edges without changing their coordinates. Use source quantities and labels only. Apply `\GEHighlight` to short diagram labels with matching roles. Keep axes, units, relationships, and necessary legends explicit. Prefer small inline drawings to repository-specific graph macros.

## Portable build and inspection

1. Copy the final `.tex` and any essential delivered assets into an isolated temporary directory, preventing accidental success through repository search paths. Clear inherited `TEXINPUTS`/`BIBINPUTS` additions that point into the repository for this check. Standard TeX distribution packages remain available.
2. Create a `build` subdirectory and run from the isolated directory:

   ```text
   pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build lesson.tex
   ```

   Use a suitable installed engine if the source language requires it. Run at least twice and repeat if references/totals still change or the log requests reruns. Stop and diagnose repeated failures rather than looping indefinitely. Compare settled auxiliary files or extracted footer totals across runs. Resolve overfull boxes, undefined references, missing characters, and errors. Copy only the matching PDF beside the delivered source.
3. Read `.nav` entries `\beamer@framepages{first}{last}` to map logical frames to physical PDF pages. `\inserttotalframenumber` counts frames, while PDF pages include overlays. Keep the opening reference numbered; avoid `noframenumbering`, `allowframebreaks`, or counter manipulation unless explicitly required and verified.
4. Render selected pages with `pdftoppm -f <page> -l <page> -scale-to 1600 -png <pdf> <prefix>` or another available renderer. Inspect first, middle, and last overlays of representative frames plus every suspected layout/timing risk. Text extraction can check wording and footer numbers, but Beamer may leave visually hidden text extractable: verify answer timing in rendered overlays. Compare stable elements across overlays, including table rules and long cells.
5. If a compiler or renderer is unavailable, deliver portable source and identify unperformed checks. Never reuse an older PDF as if it matched the new source.

6. Compile isolated enabled/disabled copies using the starter toggle, preserving its delivered setting. Render both and a grayscale copy to check that table text, full notation, associated values, component roles, diagrams, and labels remain understandable without highlights.
