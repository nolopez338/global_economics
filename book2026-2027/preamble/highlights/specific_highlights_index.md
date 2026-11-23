# Index

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights.tex](highlights.tex), [specific_highlights.tex](specific_highlights.tex).

Canonical source directory: `book2026-2027/preamble/highlights/`. Import `highlights/highlights.tex` and, when needed, `highlights/specific_highlights.tex` through the shared preamble search path. Start here before editing. Read the relevant module and its live callers; these documents describe interfaces, not a second mathematical catalog.

| Task | Edit | Read next |
|---|---|---|
| Change marker geometry or switch | `highlights_renderer.tex` | [Renderer](specific_highlights_renderer.md) |
| Change colors, snapshots or overrides | `highlights_palette.tex` | [Palette](specific_highlights_palette.md) |
| Add/change a semantic wrapper | `highlights_roles.tex` | [Roles](specific_highlights_roles.md) |
| Change identity, declarations or union selection | `highlights_catalog.tex` | [Catalog](specific_highlights_catalog.md) |
| Edit mathematical data/membership | `highlights_g10_t1.tex`, `highlights_g10_t2.tex`, `highlights_g11_t1.tex`, `highlights_g11_t2.tex` | [G10 T1](specific_highlights_g10_t1.md), [G10 T2](specific_highlights_g10_t2.md), [G11 T1](specific_highlights_g11_t1.md), [G11 T2](specific_highlights_g11_t2.md) |
| Change schemas or pagination | `highlights_tables.tex` | [Tables](specific_highlights_tables.md) |
| Maintain a historical entry | `highlights_compat.tex` and its three adapters | [Compatibility](specific_highlights_compat.md) |
| Change hierarchy/navigation | three `specific_highlights_*view.tex` files | [Viewers](specific_highlights_viewers.md) |
| Validate an edit | source plus isolated builds | [Editing](specific_highlights_editing.md) |

Ordinary markers: shared preamble → `highlights.tex`. This loads palette declarations, renderer and base roles only. Legends/records: then `specific_highlights.tex`; it initializes registry palette/roles, loads catalog, datasets in the order G11 T1 → G10 T1 → G10 T2 → G11 T2 (shared concepts before dependent contexts), tables, then compatibility adapters. Keep the existing document disable switch immediately after the marker loader. Repeated loader input is guarded and does not reset the switch.

Historical `tone_highlight_colors.tex`, `tone_specific_highlights.tex`, `g11_tone_highlights.tex` and `specific_highlights_unions.tex` remain compatibility entry points. Dataset modules assume the public registry loader; they are not standalone documents. No JSON/YAML catalog or generated Markdown mathematical authority is used.
