---
name: update-specific-highlights-summary
description: Maintain the coordinated specific_highlights_XX.md documentation family from the repository's live LaTeX legend registry and shared highlights. Use for summary maintenance, not legend design or LaTeX authoring; no parameters required.
---

# Update Specific Highlights Summary

Start at [specific_highlights_index.md](../../../book/preamble/highlights/specific_highlights_index.md) and update only the affected `specific_highlights_XX.md` family documents beside it. Do not recreate the removed monolithic summary or proposal, or create another overview. Do not modify LaTeX sources, palettes, legends, unrelated documentation, or authoring skills. Invocation requires no arguments or follow-up information.

## Locate and read

Resolve this loaded skill's absolute location and walk its ancestors to find the repository containing `.agents/skills/update-specific-highlights-summary` and `book`. Anchor to that repository, independently of the process working directory; do not select another checkout from the current directory. A `.git` directory or worktree file can corroborate the root but is not required. If the root is ambiguous or missing, report the limitation rather than guessing.

Read these small files directly on every invocation, using absolute paths from the resolved root:

- `book/preamble/highlights/specific_highlights.tex`: public registry loader; follow its live catalog, dataset, table and compatibility dependencies.
- `book/preamble/highlights/highlights.tex`: public marker loader; follow its live palette, renderer and role dependencies.
- `book/preamble/highlights/specific_highlights_index.md`, if present: initial presentation reference, never authority over LaTeX.

Follow additional local dependencies only to resolve legend content or color behavior. Do not build a persistent source cache. If a required source is missing or a definition cannot be resolved, report the specific gap; do not invent a mapping or claim full currency. Keep the output untouched when required sources are missing. For a partially unresolved definition, either retain the output with a clear limitation in the report or explicitly mark the unresolved portion in the summary; never present stale material as verified.

## Reconcile the reference

Inspect actual definitions, aliases, helper calls, optional branches, nested redefinitions, groups, and `colorlet` overrides. Comments and search/extraction results are supporting evidence, not a LaTeX interpreter. Trace each registered `practicehighlightlegend@...` key to its effective content, including aliases and slide variants. Trace wrapper calls to the color identifiers they actually reference; names and prefixes do not determine criterion usage.

Maintain coordinated English module references with relative source links. Keep the index and editing guide short. Detailed inventories belong to their owning module documents, each with authoritative source links, dependencies, edit boundaries and an index backlink. Point to LaTeX records rather than creating a second editable mathematical catalog. Preserve accurate explanations and useful organization, adapting sections as legend families evolve. Include:

- Loading order and guards, registry invocation, and unknown-key behavior.
- Every live registered key and its presentation differences, with pointers to authoritative concept/context records and explicit memberships. Remove obsolete entries and mappings; keep shared definitions that remain live even if one registry consumer disappears. Do not hard-code counts or a fixed family list.
- Semantic wrappers and their actual color identifiers; relevant base colors with exact source identifiers and hex values; command/color aliases and exact xcolor mix expressions.
- Local palette overrides, where they are applied, their grouping/scope, and differences from shared defaults. Distinguish a palette command's caller-controlled scope from a legend's grouped invocation.
- Shared row helpers, their arguments (including optional defaults/branches), row order, and reveal behavior where these affect the legend. Describe local helper redefinitions separately from shared behavior.
- Highlight toggles, default state, fill/text opacity, and relevant shared text/math rendering behavior.

Preserve semantic distinctions: nominal confidence, significance level, observed coverage, individual-observation spread, standard error, margin of error, endpoints, and full width. Preserve additional distinctions as the registry evolves. Retain enough representative notation and values to explain mappings without copying the entire implementation.

Keep base hex values, xcolor mixing expressions, and final translucent marker appearance distinct. An opacity applies after color selection/mixing; a base hex is not the final displayed marker color. Do not infer a fixed final hex without resolving the rendering background. Never describe a local override as a global default.

## Validate and write

Cross-check the draft against the live registry and effective definitions, not only the previous summary:

- Every key, including aliases and variants, appears; removed entries no longer appear as current definitions.
- Colors, wrappers, aliases, scoped overrides, representative values, helper branches, reveal behavior, and row orders agree with the sources.
- Relative source links resolve from the output's directory. Tables have consistent cells (escape literal pipes), math delimiters balance, and LaTeX command names and keys remain exact.

Compare the complete proposed content with the existing file before writing. If unchanged, do not open it for writing, touch its modification time, or add timestamps. Prefer targeted edits that retain accurate presentation and existing newline style. Create the Markdown if absent. Confirm a second reconciliation would make no changes; when testing an unchanged rerun, verify both bytes and modification time remain identical.

Report the updated file, or that it was already current, plus any unresolved limitations. Do not claim validation beyond checks actually performed.
