# G11 T2 C1 highlight ecosystem gaps

Source-editing notes only; no compilation, rendering, testing or validation performed. The ecosystem remains authoritative and read-only. Only the existing practice and this report are written; no duplicate practice activity is created.

## Existing support reused

- Canonical imports follow `preamble/highlights/specific_highlights_index.md`, “Canonical source directory” and “Ordinary markers”. The existing disable-switch comment and palette invocation stay in place.
- `preamble/highlights/highlights_compat_ttwo.tex:89`, `practicehighlightlegend@G11-T2-C1`, supplies the required Sample / Population side-by-side presentation, including both variance rows. It is invoked before Introduction at `subsec:c1-key-terms` / `tab:highlight-legend`. No special-layout replacement is needed. The coordinated renderer at line 688 is the ordinary single-table layout and is deliberately not used for this opening.
- `preamble/highlights/highlights_tables.tex:74`, `HighlightDetailedTable`, supplies the full-width four-column reference and repeated headings. Its rows are explicitly enumerated locally at `tab:notation-reference`; no concept union is used.
- `preamble/highlights/highlights_catalog.tex:95`, `HighlightEffectiveField`, supplies existing definitions with concept fallback. Mean definitions use the context's `meaning` field to avoid the unrelated simulation qualification of `CoordinatedPopulationMeanMeaning` (`highlights_compat_ttwo.tex:227`). Contextual interpretations remain local.

## Missing or insufficient symbol-level support

| Requirement and source anchor | Gap | Local handling |
| --- | --- | --- |
| `highlights_g11_t2.tex:756`, `g11-t2-c1-coordinated-11-population` | Population group and N are bundled under group.population; no separate C1 population-size record or dedicated population-size role. | Separate rows for the population and N. Use existing `HLPopulationGroup` for sets and existing `HLObservationCount` / count.design for N and n, with explicit population/sample size names. No shared role or mapping is invented. |
| `highlights_g11_t2.tex:744`, sample; line 768, size | X and Xi share a record; n lacks separate indexed-size records. | Explicit X, X1, X2, Xi, X2D and n, n1, n2, ni rows. Whole samples use `HLSampleGroup`; sizes use `HLObservationCount`. The opening examples and procedure use these wrappers by meaning. Mixed group descriptions such as “40 selected bills” retain the group role; standalone size values use count.design. |
| `highlights_g11_t2.tex:782`, obs | Observation definition includes alternative xi notation; no symbol-specific yj definition record. | yj has its own row with the existing observation definition and bill-charge interpretation. No extra observation notation is introduced. |
| `highlights_g11_t2.tex:794`, meanpop; line 808, meansample | No individual 1D/2D population mean or 1/2/2D sample mean context records; sample notation bundles generic and indexed means. | Explicit rows for mu, mu1D, mu2D, x-bar, x-bar1, x-bar2, x-bar2D and x-bari, using existing measure wrappers and field lookups. Interpretations distinguish redraws from population redefinition, linked to `subsec:c1-quick-check`; no numerical means are invented. |
| `highlights_g11_t2.tex:821` through line 885, spread and proportion contexts | General records are available, but do not supply bill-specific interpretations; no contextual values for s, sigma, p or p-hat. | Existing definitions plus local Example 1 meanings; no spread or proportion values supplied. Generic indexed spread/proportion forms not introduced here are not assigned fictional example meanings. |
| `highlights_g11_t2.tex:847`, variance; line 860, varsample; `highlights_compat_ttwo.tex:89` | Both variance partners exist in the opening ecosystem presentation but are absent from the actual introductory narrative. | Retain separate sigma-squared and s-squared rows and shared definitions. Final cells explicitly state that no introductory interpretation or numerical value is supplied; do not infer squared bill spreads or add a new introductory example. |
| All C1 coordinated contexts, `highlights_g11_t2.tex:744–897`, `examples={}` | No ecosystem-provided electricity-bill, redraw or population-redefinition example links/interpretations. | Practice-local bullet meanings link to `subsec:c1-population-and-sample` and `subsec:c1-quick-check`. Reuse actual 40-bill draws and 210 thousand COP only where already stated. |
| `highlights_tables.tex:49`, `hl_union_print:n` | Default record rendering joins notation by concept, so cannot guarantee one row per specific notation. | Pass explicit symbol rows to the existing `HighlightDetailedTable`; do not select a union or add substitute concepts. |

## Special-layout boundary

The required special opening layout is supported directly by `G11-T2-C1`; it needs no ecosystem change. Its fixed cells are not field-driven and its N cell uses the population-group treatment (`highlights_compat_ttwo.tex:108`). The existing presentation is preserved as requested. The expanded reference and local introductory size notation distinguish N as a count through `HLObservationCount`; this limitation of the immutable opening helper is reported rather than patched or replaced. Variance aliases in that presentation are ecosystem palette aliases (`highlights_palette.tex:129–155`), while reference rows use the existing variance wrappers.

Questions, solutions, labels, navigation and toggles are outside these local table edits. No Olympiad material is included. This report records implementation gaps, not verification results.
