# C2 highlights ecosystem gaps

Scope: source-only adaptation of `G10_T2_L1_C2_practice_activity.tex`. The ecosystem is authoritative and was left read-only. No Olympiad material was adapted.

## Reused support

- Canonical imports follow [the ecosystem index](../../../preamble/highlights/specific_highlights_index.md): `highlights/highlights.tex` and `highlights/specific_highlights.tex`.
- The opening legend uses `\PracticeHighlightLegend{G10-T2-C2-coordinated}` before Introduction. Source anchors: [highlights_g10_t2.tex](../../../preamble/highlights/highlights_g10_t2.tex), `\HighlightDeclareReference{G10-T2-C2-coordinated}`; [highlights_compat_ttwo.tex](../../../preamble/highlights/highlights_compat_ttwo.tex), `practicehighlightlegend@G10-T2-C2-coordinated`.
- Existing local wrappers remain aliases of shared quantity, outcome, probability and cumulative roles. Source anchor: [highlights_roles.tex](../../../preamble/highlights/highlights_roles.tex), `\GTenHLValue`, `\GTenHLOutcome`, `\GTenHLProbability`, `\HLCumulativeProbability`.
- The expanded reference uses shared notation/definition/name/brief lookups where applicable: `g10-t2-c2-coordinated-10-variable`, `-support`, `-mass`, `-cum`, `-cutoff` in [highlights_g10_t2.tex](../../../preamble/highlights/highlights_g10_t2.tex), and `\HighlightContextField` / `\HighlightEffectiveField` in [highlights_catalog.tex](../../../preamble/highlights/highlights_catalog.tex).

## Missing reusable support and local fallbacks

1. **Individual notation fields within compound records.** The C2 `-variable` record groups X and x; `-cum` groups inclusive CDF, left limit and probability notation. They support the meanings, but do not expose separate fields for each notation with its individual definition. Local fallback: individual rows for X, x, F_X(x), F_X(a), F_X(a^-), and the concrete introductory expressions; use existing wrappers and the shared full definition where applicable. Source anchors: `\HighlightDeclareContext{g10-t2-c2-coordinated-10-variable}` and `\HighlightDeclareContext{g10-t2-c2-coordinated-10-cum}`. No replacement mapping was introduced.
2. **A standalone jump/graph-correspondence record.** The C2 cumulative record defines inclusive and strict probabilities but has no dedicated jump-size or translated-shadow field. Local fallback: a separate jump-expression row preserves the existing identity, payment-fee values, and shadow interpretation using the existing mass/CDF wrappers. The full graph-convention prose and `\cTwoConnectionReading` remain local and unchanged. Source anchors: ecosystem C2 `-mass` and `-cum` records; practice `\cTwoConnectionReading`, “From bars to stems”, and `tab:notation-reference`.

Payment-fee and refund-request interpretations remain local because the C2 records have empty `examples` fields. This is document-specific content rather than a missing semantic role. The local repeated-header longtable uses `\COneToneDetailedHeaders` from [highlights_tables.tex](../../../preamble/highlights/highlights_tables.tex); it does not use concept-union collection, which would combine distinct symbol rows.

No missing semantic mapping, wrapper, color or table-header support remains for this adaptation. The reusable field-granularity and jump-record gaps above remain in the read-only ecosystem and are covered locally. No shared records, commands, colors, references, renderers, documentation or compatibility loaders were changed.

Not compiled or verified; ready for manual review.
