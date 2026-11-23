# Compat

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_compat.tex](highlights_compat.tex), [highlights_compat_ttwo.tex](highlights_compat_ttwo.tex), [highlights_compat_g10.tex](highlights_compat_g10.tex), [highlights_compat_g11.tex](highlights_compat_g11.tex).

`highlights_compat.tex` loads three guarded adapters in order: Term 2, Grade 11 Term 1, Grade 10 Term 1. This justified extra module split keeps retained historical table bodies reviewable without mixing them into new records. Adapters read record fields; they preserve specialized schemas, criterion-local notation overrides, registry destinations, slide reveal interfaces and public helper names.

| Historical interface | Current destination |
|---|---|
| `highlights.tex`, `\HighlightStroke`, `\GTenHLStroke`, `\GTenHL...`, `\HLExpectedValue`, toggle | Public loader → renderer/base roles/palette |
| `specific_highlights.tex`, `\PracticeHighlightLegend{key}`, `practicehighlightlegend@<key>` | Registry loader → three compatibility adapters |
| `tone_highlight_colors.tex` | Palette initialization, captured Tone/Ttwo names |
| `tone_specific_highlights.tex`, `\GTenToneHL`, `tonecatalog@...`, `tonerow@...`, `tonenotation@...`, `toneexample@...` | Registry loader; roles/tables plus G10 adapter reading G10 T1 records |
| `g11_tone_highlights.tex`, `\COneTone...`, `g11tone@...` | Registry loader; G11 adapter reading G11 T1 records |
| `specific_highlights_unions.tex`, `\SpecificHighlightUnion`, `\SpecificHighlightCollectUnion`, `\SpecificHighlightUnionRows` | Registry loader; catalog selector and shared tables |
| `coordinatednotation@<grade>@<id>`, `coordinatedrow@...`, `\CoordinatedLegendEntry` | Term 2 adapter → compatibility-default context fields; local overrides preserved |
| `\Ctwo...`, `\HL...`, explicit `\CtwoTtwo...`, `\HLTtwo...` | Role initializer; forwarding remains dynamic |
| Existing color names, including `G11T2C1...`, `G11TtwoCone...`, `MathHL...`, `MathHLTtwo...`, `CtwoTtwo...`, `GTenTtwo...` | Palette module; see its complete binding inventory |

All registered keys, including combined, coordinated, legacy and slides variants, are listed in the four dataset documents. `\PracticeHighlightLegend` errors on unknown keys; explicit pending availability belongs to `\HighlightReference`, and does not create an old-style criterion renderer. The school context is a declared variant; `\GTenToneSchoolContext` retains its historical local override behavior.

Supported repeated sequences include `highlights.tex` → `specific_highlights.tex`, repeated registry/marker loading, and either Term 1 compatibility loader after the public registry. Guards retain `GTenHighlightLoaded`, `PracticeHighlightRegistryLoaded`, `GTenToneColorsLoaded`, `GTenToneRegistryLoaded`, `COneToneRegistryLoaded` and `SpecificHighlightUnionsLoaded` where relevant. Canonical resolution uses `highlights/<module>` through the preamble `\input@path`, then `../highlights/<module>` for the historical graphs working directory, then a bare filename for standalone viewers in this directory. Historical `graphs/` shims delegate to `highlights/<module>` or `../highlights/<module>` without setting any implementation guard.

Maintain adapters when preserving old presentation; add new mathematical data in datasets. Do not repoint a captured color alias or convert a forwarding command to a snapshot by accident. Existing practice callers remain supported by the historical entry points; later adaptation tasks can update their canonical imports.

Historical path loaders retained for existing non-Olympiad consumers: [`graphs/highlights.tex`](../graphs/highlights.tex), [`graphs/specific_highlights.tex`](../graphs/specific_highlights.tex), [`graphs/tone_highlight_colors.tex`](../graphs/tone_highlight_colors.tex), [`graphs/tone_specific_highlights.tex`](../graphs/tone_specific_highlights.tex), [`graphs/g11_tone_highlights.tex`](../graphs/g11_tone_highlights.tex), and [`graphs/specific_highlights_unions.tex`](../graphs/specific_highlights_unions.tex). These files contain no palettes, mathematical records, or adapter implementations.

The `G10-T2-C3-coordinated` legend adapter inserts its context-specific transformation-function row immediately after the secondary-variable row, reading notation, name and brief from `g10-t2-c3-coordinated-10-function`. It reuses `\CoordinatedLegendRow` and the shared table; other legend adapters retain their existing mappings.
