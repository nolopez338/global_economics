# Catalog

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_catalog.tex](highlights_catalog.tex), [highlights_g10_t1.tex](highlights_g10_t1.tex), [highlights_g10_t2.tex](highlights_g10_t2.tex), [highlights_g11_t1.tex](highlights_g11_t1.tex), [highlights_g11_t2.tex](highlights_g11_t2.tex).

All datasets use the same three declarations. Values containing commas, math or commands must be braced. Commands store tokens without expanding role wrappers, so highlighting and local palettes are evaluated when typeset.

```tex
\HighlightDeclareConcept{stable-meaning-id}{
  role={semantic-role}, name={Concept}, notation={$x$},
  brief={Short meaning.}, definition={General definition.}, source={repository/path.tex}}
\HighlightDeclareContext{unique-context-id}{
  concept={stable-meaning-id}, grade={10}, term={2}, criteria={1,2},
  variant={default}, notation={$x_i$}, examples={}, source={repository/path.tex}}
\HighlightDeclareReference{G10-T2-example-variant}{
  status={available}, members={unique-context-id}}
\HighlightReference{G10-T2-example-variant}[concise]
```

This is syntax only; do not add invented mathematics or references by copying the example. A concept ID is independent of grade, term, criterion, notation and color. Declare it once in its owning dataset. Context IDs identify particular usage and preserve all criteria together, variant, contextual notation, registered introductory interpretations and provenance. Contexts may override `name`, `brief`, `definition` and supply `meaning`; `display` stores original specialized legacy cell text and `legacy-key` supports the historical Term 1 row interfaces; general definitions remain distinct from `meaning` and `examples`. Empty examples mean no registered interpretation, not permission to invent one.

`\HighlightConceptField{id}{field}`, `\HighlightContextField{id}{field}` and `\HighlightReferenceField{id}{field}` expose stored fields. Every record has `id`; concepts also have an automatically maintained `contexts` list. `\HighlightEffectiveField{context}{field}` uses a context override or its concept's field. Use this effective lookup for inherited display fields; the raw context lookup intentionally returns only fields stored on that context. `source` contains repository-relative provenance, sometimes a source directory when coverage spans several activities. Multiple sources are semicolon-separated. Raw provenance strings are metadata; escape underscores before typesetting them.

References explicitly list **context IDs**, each of which names its concept. Declarations reject duplicate IDs, unknown keys, invalid statuses, contexts with missing concepts and references with missing members. `renderer` optionally names a historical registry renderer; `\HighlightReference` itself uses the common schemas. `\PracticeHighlightLegend` keeps the historical presentation. Do not infer reference availability from a concept's presence in an introduction.

`\HighlightForEachMember{key}{callback}` calls the callback with each context ID in declared order; Term 1 adapters use it to avoid a second membership list. `\HighlightSelectReference{key}` resets selection; `\HighlightAppendReference{key}` adds members without repeats. `\HighlightSelect{grade}{term}` selects `G<grade>-T<term>-full` references: grade is `all`, `10`, `11`; term is `all`, `1`, `2`, `3`. `\SpecificHighlightCollectUnion` is the maintained selector alias. `\SpecificHighlightUnion{grade}{term}{concise|detailed}` selects then renders. Explicit pending references emit “Reference not yet available.” without an empty table. Unknown references raise errors.

Within unions, context IDs are unique; rows are grouped by stable concept ID. Notation, brief meanings, definitions and example statements are added once per exact token value, preserving declaration order. Identical example statements print once with all selected grade/term/criterion labels; deduplication happens before adding those labels. Different meanings never merge merely because notation or color matches. Context-specific notation and interpretations survive; source-scoped introductory prerequisites are explicitly listed in the appropriate full reference. G11 Term 2 prerequisites do not make a G10 or Term 3 reference available. Combined-only C1/C2, C1/C3, C4/C5 and C6/C7 references remain combined. Full references exclude presentation-only legacy/slide/default adapters and the alternate school context unless that reference is explicitly requested.

Selection reads declared membership directly. It never temporarily redefines a table-rendering command. Shared tables own layout; adapters own historical schemas. Dataset documents inventory keys and edit boundaries without duplicating mathematical definitions.

The design count shared by trial and sampling contexts uses `design-count`; the Student t model index and one-sample `df` notation use `degrees-of-freedom`. Their context-specific notation, assumptions and source definitions remain separate fields under those shared identities.
