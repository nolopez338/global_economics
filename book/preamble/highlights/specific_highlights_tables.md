# Tables

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_tables.tex](highlights_tables.tex).

`\HighlightConciseTable{rows}` uses **Symbol or notation | Concept | Brief meaning**. `\HighlightDetailedTable{rows}` uses **Symbol or notation | Concept | Definition | Meaning in the introductory examples**. `\HighlightRenderSelected{concise|detailed}` renders the prepared union; `\SpecificHighlightUnionRows{schema}` prints selected concept rows. Collection happens before longtable, never by intercepting a row renderer.

Both use nonfloating longtable, top-aligned ragged paragraph columns, repeated `\endfirsthead` / `\endhead` schemas, a continuation footer and bottom rule. Concise widths are .30/.23/remainder (.47 minus four column spacings). The detailed table measures its body notation at natural width, including highlight-box padding and deliberate paragraph breaks, with a minimum wide enough for the two-line header “Symbol or / notation”. It subtracts that width and six column spacings from the local `\linewidth`, then shares the remaining width among Concept, Definition and introductory meanings in the existing 22:23:25 proportions; the final column takes the exact remainder. The measurement uses a discarded tabular, without changing row renderers or registry collection. Its existing longtable footer fix is scoped to the detailed table group. Spacing is 4 pt tabcolsep and arraystretch 1.16. Definitions and example meanings occupy separate columns; blank example cells preserve missing interpretations.

Historical specialized schemas remain: `\CoordinatedLegendTable`, `\GradeElevenCOneLegendTable`, `\GTenToneHighlightLegend`, `\GTenToneReference`, `\COneToneLegendTable`, `\COneToneDetailedReference`, plus their row/header helpers. Local criterion notation overrides remain scoped in adapters. Slide cells use `\PracticeHighlightLegendCell{step}{content}`, whose default prints all content. `\SpecificHighlightCatalog{all|10|11}` selects explicit Term 2 introduction records; its historical entry points remain available. Tables no longer own mathematical catalog bodies.

Viewers reserve space with needspace before headings; group headings in `\COneToneCatalog` end with starred row breaks to keep the first entry attached. Longtable can break between rows, not inside an oversized row. Check all final pages after changing memberships or prose. `\HighlightViewerLongtableFix` applies the existing two-replacement footer patch once, explicitly selected by all three viewers; ordinary consumers do not alter longtable output merely by loading the registry; do not suppress fit warnings. Practice or slide schemas should not be globally replaced merely to change union layout.

Dependencies are catalog selections, role wrappers, array, booktabs, longtable, etoolbox, needspace, varwidth and the shared preamble. Edit layout here and hierarchy in viewers; source data belongs to datasets.

[Detailed table layout fixture](tests/detailed_table_layout.tex) checks rendered notation width including highlight padding, the two-line-header minimum, a smaller local width and font, disabled highlights, deliberate union paragraph breaks, and spacing isolation. Its opening comments give the isolated build command; inspect its PDF alongside representative consumer documents.
