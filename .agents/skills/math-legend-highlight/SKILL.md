---
name: math-legend-highlight
description: "Design or refine complementary concise highlight legends and detailed notation references for mathematics documents across topics and native formats, with a shared semantic mapping, hierarchy, anchors, and navigation. Use for table design or placement; use math-practice-highlights for applying an established mapping throughout content."
---

# Math Legend Highlight

Design two complementary tables from the document's mathematics: a concise highlight legend for quick reference and a detailed notation reference for fuller definitions and introductory interpretations. Work in the native format; conversion to LaTeX is not required. Do not assume a topic, course, level, palette, notation system, or row count. Translate headings consistently into the document's language.

## Inspect before editing

Read the mathematical content, introductory material, notation, examples, exercises, and solutions, including relevant included files. Inspect the preamble or styling setup, navigation, and established build/export instructions.

Identify:

- Concepts readers must distinguish or connect, essential symbols and their contextual meanings, and relationships across prose, expressions, equations, tables, and diagrams.
- Existing semantic highlight roles, colors, markup, toggles and their current settings, legends, registry entries, and renderers.
- The boundary between instructional explanations or worked solutions and reasoning that independent or assessed tasks require students to supply.

When related documents must be coordinated, inspect them together and identify the designated reference, if any. Preserve that reference's source, rendered appearance, and shared dependencies; do not change a shared role or renderer merely to align other documents. Establish one semantic and notation mapping for the requested set, reusing the reference's treatments for matching concepts and resolving inconsistent conventions without changing mathematical meaning.

Find existing tables, mappings, labels, macros, and registry entries before creating anything. On reruns, refine or relocate each table in place, retaining its identity and navigation targets. Add only a missing complementary table; do not accumulate duplicate tables, subsections, toggles, inputs, or registry entries.

## Design the shared mapping and complementary tables

Choose a small, coherent set of key terms and semantic highlight roles needed to understand this document. Assign roles by mathematical meaning in context, not by matching tokens, numbers, or words. Distinguish objects, quantities, operations, conditions, representations, or logical roles only where the topic needs those distinctions. The same symbol can have different meanings; different symbols can express the same role. Avoid global replacement based on symbol spelling.

Use these student-facing schemas, translated consistently:

| Table | Columns | Purpose |
| --- | --- | --- |
| Concise highlight legend | Symbol or notation · Concept · Brief meaning | Short entries for essential notation and brief meanings; no extended explanations, derivations, or worked calculations. |
| Detailed notation reference | Symbol or notation · Concept · Definition · Meaning in the introductory examples | Distinguish a general mathematical definition from the symbol's meaning in the introductory situations. |

In the detailed table's final column, use concise bullets explicitly linked to the introductory examples, such as “Example 1: …” and “Example 2: …”, wherever applicable. Link only relevant examples; do not force every example into every row. Use actual source situations, quantities, and relationships, not invented contexts. Report missing examples when adapting a source; creation or revision of examples belongs to the document's authoring workflow and requires authorization.

Both tables share one concept–notation–highlight mapping. They have distinct purposes and are not accidental duplicates: reuse roles and notation, but do not copy long definitions into the concise legend. The detailed reference may include additional relevant notation while preserving all shared roles. Include units, domains, and assumptions in the appropriate cells when needed, without adding irrelevant columns or empty filler.

Highlight each concept's name, complete notation, and associated values where instructionally useful with the same treatment as in the body. A color swatch or highlighted concept name alone is insufficient. Preserve distinct component roles inside composite expressions, including numerical substitutions; keep connecting operators outside wrappers. Include accessible meanings and check every notation against prose, formulas, tables, diagrams, and worked solutions. Labels and definitions must remain sufficient in grayscale and with highlights disabled. Neither table may reveal answers or reasoning students are expected to derive independently.

Choose related but distinguishable color families for related concepts; verify their appearance using the actual renderer rather than relying on palette names. Briefly explain family relationships in student-facing language while retaining each row's conceptual meaning. For example, confidence level / C / 95% / central probability 0.95 share one role, while critical value / z* / 1.96 share a distinct role; this illustrates the rule without prescribing these concepts or colors for every topic. Do not assign every probability or area the same role.

Reuse a suitable legend, registry entry, renderer, and palette. Adapt a matching prose legend into a table when appropriate. Create a new entry only when needed. Before changing a shared definition, inspect its callers and other uses; preserve unrelated entries and verify affected consumers. Prefer a document-specific entry when changing a shared one would alter unrelated material.

## Establish placement, hierarchy, and handoffs

Place the concise legend at the nearest suitable opening instructional location, before substantial highlighted examples. Put the detailed reference where readers have already encountered the introductory situations it interprets. Preserve native heading conventions; no fixed opening subsection title is required. A brief heading or one-sentence lead-in is enough. Avoid repeating lengthy explanations across the two tables and introduction.

Course-specific section numbering belongs to the authoring skill. For Global Economics practices, [global-economics-home-practice](../global-economics-home-practice/SKILL.md) owns the activity structure and at least two introductory examples: concise legend first in Section 1, examples next, detailed reference then reusable procedure in Section 2. For decks, [global-economics-slides](../global-economics-slides/SKILL.md) owns the source-faithful sequence, stable progressive opening reference beginning on logical frame 2, and fully visible concise closing legend. These are format-specific placements, not universal section rules for mathematics documents.

Reuse existing heading labels and navigation targets; add unique anchors only for missing tables. Update local indexes and return links to the actual locations, preserving compatible anchors when moving material. Reuse a table's macro or registry entry for its intended purpose; do not invoke the same complete table as both complementary references. Preserve distinct legends serving unrelated purposes.

This skill owns concept and notation identification, the shared semantic mapping, both table designs, placement, hierarchy, anchors, and navigation. Establish those once before handing document-wide application to [math-practice-highlights](../math-practice-highlights/SKILL.md), which owns markup, renderer integration, diagrams, toggles, and highlighting validation. The authoring skills coordinate these responsibilities in that order. If both companions are active, resume the next unfinished responsibility without circular invocation or repeating completed design work. A local markup correction using an adequate mapping does not require redesigning tables.

Reuse existing wrappers and preserve toggle settings while styling the tables. Keep complete symbols together, avoid nested wrappers, and retain all content with styling off. If the companion is unavailable, use the native renderer and existing toggle for these tables, inspect the tables and relevant body examples, and report any uncompleted document-wide work. Do not convert formats just to apply this workflow. For LaTeX integration, read [references/latex.md](references/latex.md).

## Preserve content and layout

Preserve existing mathematical meaning, wording, values, notation, assumptions, exercises, solutions, labels, and hyperlink targets except for the requested tables, explicitly requested notation coordination, and necessary structural changes. Report suspected mathematical errors separately; do not silently correct them without authorization.

Keep each heading and its table together when practical; split a long detailed reference sensibly with repeated column headings. Prioritize early placement, readable type, adequate spacing, and sensible page breaks. Adapt column widths, wording, or page breaks while preserving the schemas before shrinking text. Preserve titles, contents, learning objectives or criteria, practice guidance, and existing solution page breaks or reserved space unless rendered inspection demonstrates a necessary adjustment.

## Validate and deliver

- Follow the established build or export process. Review the source diff or the native format's equivalent comparison for content preservation and unintended edits.
- Check for accidental duplicate tables, labels, inputs, toggles, registry entries, and wrappers. Verify both schemas, shared semantic mapping, concise entries, general definitions versus example-linked bullets, and placement appropriate to the authoring workflow. Confirm reruns reuse both tables and their supporting definitions.
- Inspect rendered opening pages for heading hierarchy, legibility, overflow, spacing, and page breaks. Verify contents links, table anchors, and return navigation in the output, including targets retained from moved content.
- For a highlight toggle, build temporary enabled and disabled versions and inspect both. Check content retention and legibility with highlights off and in grayscale. Preserve the original source setting; use isolated copies or build overrides that retain relative dependency resolution.
- For coordinated documents, verify notation and semantic treatments against the reference and across all targets. Verify the reference source is unchanged and compare its rendered output before and after supporting edits.
- When shared definitions change, check affected consumers for compatibility, building/rendering them where needed. Remove temporary validation artifacts according to project conventions; preserve pre-existing files and intended deliverables.

Deliver the revised source, necessary supporting legend or styling changes, and compiled/exported document when supported. Give a concise account of structural changes, validation performed, suspected errors, and unresolved limitations. If tools cannot build, render, or verify navigation, state exactly which checks remain unverified; do not claim they passed.
