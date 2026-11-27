# Minimal student response guides

Read when guides are requested or students must answer on the exam. Apply across grades, topics and criteria; include only the labels, blank tables, empty boxes and graph areas needed for the assessed work.

## Coverage without assistance

- Map each required calculation and interpretation to adequate response space, keeping separately assessed subparts identifiable. Label blocks by question number and task letter, retaining any assessed subpart identifiers. Use short labels; do not repeat instructions already stated in General tasks (when present) or the question.
- Provide structure only: no starter calculations, formulas to complete, procedural hints, intermediate results, derived support values, completed entries or example answers. Choose enough blank rows without displaying derived classifications or results. Combine spaces only when all assessed outputs remain identifiable.
- Keep prompts outside empty response boxes. Table headers may name required outputs; body cells stay blank. Use vertical column dividers only, without horizontal rules, including header or outer horizontal rules. Preserve row heights and handwriting space.
- For requested graphs, provide only blank axes, light grids and a suitable uniform numerical scale. Choose a practical range and regular ticks; do not mark derived support values, special answer locations or plotted results. Axis names and units may identify the requested quantities without revealing results.

## Layout and helpers

Response pages inherit the question pages' paper size, orientation and margins unless explicitly instructed otherwise. End `multicols` and use `\clearpage` for dedicated response pages if needed; do not introduce a new geometry merely to gain space. Respect an explicitly requested response-page count. Compact through concise labels, shared instructions, column widths and top-aligned side-by-side blocks. Preserve legible type and practical handwriting space; avoid excessive font reduction, scaled tables, tiny graphs and negative spacing. If the page count cannot be met legibly with every required space, report the conflict rather than omitting spaces.

The [scaffold](../assets/template_exam.tex) supplies these local helpers; definitions alone do not add a response guide:

- `\ExamResponseBox[height]{width}`: empty baseline-anchored writing area with `fill=black!1`, `draw=black!25`, `line width=.3pt`, `rounded corners=2mm`. Width and height are minimum dimensions; size them for numbers, fractions, algebra, and verbal responses. Allow border clearance within the local width. Keep labels outside.
- `\ExamResponseTable{column specification}{headers}{blank rows}`: local-width `tabularx` with vertical dividers chosen in the specification. Use wrapping columns and explicit positive row heights; never insert `\hline`, booktabs rules, filled cells or derived row labels. For example, the following is a usage illustration, not required exam content or a fixed row count:

~~~latex
\textbf{\ref*{q:ordered}(a)}\par\nopagebreak[4]
\ExamResponseTable{@{}X|X@{}}
  {\textbf{Calculation} & \textbf{Interpretation}}
  {\rule{0pt}{24mm} & \\}
% Alternative for a single writing area; choose only the structure needed:
% \noindent\ExamResponseBox[30mm]{\dimexpr\linewidth-1pt\relax}
~~~

For paired blocks use top-aligned minipages starting with `\vspace{0pt}`, sized to fit with a positive gap. Start later corresponding blocks in a new paired row so unequal content does not stagger their alignment. Keep each label or prompt with its response area, reserving the measured block height with `\Needspace`; allow long guides to break at task boundaries.

For a blank graph, the loaded PGFPlots package supports an `axis` with `axis lines=left`, `grid=major`, `grid style={black!10,line width=.2pt}`, explicit numeric `xmin`, `xmax`, `ymin`, `ymax`, and regular `xtick distance`/`ytick distance`. Set readable width and height for the local block and leave out `\addplot`, answer nodes and data coordinates. Set the numerical range from the verified task privately, without exposing the derived values as special ticks or labels.

## Verify before delivery

Check coverage against the final prompts and scoring ledger, including each assessed calculation and interpretation. Inspect all rendered guide pages for empty cells and boxes, vertical-only table rules, sufficient rows and writing height, readable graph ticks, wrapping, alignment, clipping, overlap and useful page breaks. Confirm matching paper size, orientation and margins, the requested response-page count, and no answer leakage from headings, row labels, graphs or inherited helpers. Preserve the exam's mathematical checks, scoring reconciliation and compilation requirements.
