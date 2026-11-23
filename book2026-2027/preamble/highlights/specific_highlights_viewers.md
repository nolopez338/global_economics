# Viewers

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [specific_highlights_view.tex](specific_highlights_view.tex), [specific_highlights_tone_view.tex](specific_highlights_tone_view.tex), [specific_highlights_g11_tone_view.tex](specific_highlights_g11_tone_view.tex).

All three are article documents using `../preamble.tex`, marker/registry loaders, A3 portrait with 20 mm margins, needspace and shared table calls. Build from `book2026-2027/preamble/highlights/` with `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=<isolated-directory> <viewer>.tex`. No mathematical table body belongs in a viewer.

The combined English viewer owns nine top-level sections in order: Introduction; Grade 10; Grade 11; Grade 10 Term 1; Grade 10 Term 2; Grade 10 Term 3; Grade 11 Term 1; Grade 11 Term 2; Grade 11 Term 3. Introduction repeats all/Grade 10/Grade 11 concise unions. Grade sections repeat all-term and each term's detailed unions. The populated Term 1 and Term 2 overview references start on fresh pages so their headings stay with the first large entry. Populated term sections print Full Term Reference first, then available individual criteria numerically, then combined entries and variants. Both Term 3 grade subsections and both top-level Term 3 Full Term Reference subsections remain pending with no fabricated tables or criterion headings.

`\PreviewSection`, `\PreviewSubsection`, `\PreviewFullTerm`, `\PreviewTenTone`, `\PreviewLegend` and `\PreviewBackToContents` control hierarchy, heading reservations and navigation. Anchors use `preview:`; the contents anchor is `preview:contents`. Criterion anchors are preserved where practical. Full repeated tables are intentional and must not be replaced by links.

The Grade 10 Term 1 viewer groups decision/financial models, decisions without probabilities, sensitivity, and comparison/filtering/implementation, calling `\GTenToneReference`. The Grade 11 Term 1 viewer calls `\COneToneCatalog`, registered legends and `\COneToneDetailedReference`, grouping continuous models, moments/sampling, Student t/comparison and investigation. Their return anchors are `tone:contents`, unique within each separate PDF. All three call `\HighlightViewerLongtableFix` for the installed longtable footer behavior; its implementation is shared in the table module.

Edit titles, hierarchy, spacing reservations and navigation here. Read [tables](specific_highlights_tables.md) for pagination, [catalog](specific_highlights_catalog.md) for selection, and dataset files for mathematical changes. Verify links and repeated headers in the final rendered PDFs, not just source labels.
