---
name: math-key-terms-highlight-guide
description: "Revise an existing mathematics document with an opening Key terms and highlight guide subsection, a conceptual legend table, and consistent semantic highlights. Use when adding, relocating, or refining this guide across mathematics topics, levels, and native document formats; ordinary highlighting alone does not require this skill."
---

# Math Key Terms Highlight Guide

Create or refine one opening subsection titled **Key terms and highlight guide**. Derive its concise explanation and legend table from the document's mathematics. Work in the native format; conversion to LaTeX is not required. Do not assume a subject, course, level, repository, notation system, palette, row count, or table schema.

## Inspect before editing

Read the mathematical content, introductory material, notation, examples, exercises, and solutions, including relevant included files. Inspect the preamble or styling setup, navigation, and established build/export instructions.

Identify:

- Concepts readers must distinguish or connect, essential symbols and their contextual meanings, and relationships across prose, expressions, equations, tables, and diagrams.
- Existing semantic highlight roles, colors, markup, toggles and their current settings, legends, registry entries, and renderers.
- The boundary between instructional explanations or worked solutions and reasoning that independent or assessed tasks require students to supply.

When related documents must be coordinated, inspect them together and identify the designated reference, if any. Preserve that reference's source, rendered appearance, and shared dependencies; do not change a shared role or renderer merely to align other documents. Establish one semantic and notation mapping for the requested set, reusing the reference's treatments for matching concepts and resolving inconsistent conventions without changing mathematical meaning.

Find any existing matching guide or legend before creating anything. On repeat runs, refine or relocate it in place, retaining its identity and navigation targets; do not add another subsection, table, toggle, input, or registry entry.

## Design the conceptual guide

Choose a small, coherent set of key terms and semantic highlight roles needed to understand this document. Assign roles by mathematical meaning in context, not by matching tokens, numbers, or words. Distinguish objects, quantities, operations, conditions, representations, or logical roles only where the topic needs those distinctions. The same symbol can have different meanings; different symbols can express the same role. Avoid global replacement based on symbol spelling.

Make the table a conceptual reference connecting key terms or mathematical objects, representative notation where relevant, brief accessible meanings, and their highlight treatment. Choose columns to suit the content. Include units, domains, assumptions, or paired relationships only when useful; omit irrelevant columns and empty template cells. Highlight each concept's name, complete symbol or notation, and representative numerical value where useful, using exactly the same treatment as in the document. Treat the concept, its notation and associated values as one semantic role wherever highlighting is appropriate. Include a concise meaning, not merely a color label. Highlighting only concept names, color samples, or a separate treatment cell is insufficient. Include the notation readers need, and check agreement between every legend symbol and its use in prose, formulas, tables, diagrams, and worked solutions. Terms, notation, and explanations must remain sufficient to understand it in grayscale and with highlighting disabled; color names alone are insufficient.

Choose related but distinguishable color families for related concepts; verify their appearance using the actual renderer rather than relying on palette names. Briefly explain family relationships in student-facing language while retaining each row's conceptual meaning. For example, confidence level / C / 95% / central probability 0.95 share one role, while critical value / z* / 1.96 share a distinct role; this illustrates the rule without prescribing these concepts or colors for every topic. Do not assign every probability or area the same role.

Reuse a suitable legend, registry entry, renderer, and palette. Adapt a matching prose legend into a table when appropriate. Create a new entry only when needed. Before changing a shared definition, inspect its callers and other uses; preserve unrelated entries and verify affected consumers. Prefer a document-specific entry when changing a shared one would alter unrelated material.

## Establish the opening hierarchy

Place the guide first within the existing Introduction, before substantial highlighted examples and detailed notation or procedure references. Use normal document numbering: an Introduction numbered 1 should yield subsection 1.1 without hard-coding the number. If there is no Introduction, or the document uses another structural system, use the nearest suitable opening location and its conventions.

Before the table, write a short student-facing explanation introducing the central objects or ideas and the relationships needed to read the document. Present the table as the guide to terms, notation, and highlights used throughout. Do not duplicate later definitions, derivations, examples, or procedures.

Preserve existing introductory material after the guide. Add subsection headings only as needed for a clear hierarchy, without rewriting that material. Add a unique label or anchor following local conventions; preserve any existing guide target when refining it. Make the guide the first entry of an existing introduction index or subsection navigation, and add return navigation following existing conventions.

Keep exactly one authoritative legend for this guide by moving or consolidating a matching legend and updating its call sites. Preserve distinct legends serving unrelated purposes, and preserve existing hyperlink targets or provide compatible anchors when moving content.

## Integrate highlights without changing the task

Reuse existing highlight markup. Add or revise short highlights in instructional explanations and worked solutions only where needed to connect the guide to the document. Do not expose answers or supply reasoning expected in independent or assessed tasks. Avoid wrapping whole equations or paragraphs when a short meaningful span suffices. Treat composite expressions by contextual meaning: highlight distinct semantic components individually, leaving connecting operations outside the wrappers. Keep each visually complete symbol together, including meaningful accents, indices, exponents, and other necessary attachments; preserve mathematical typography and avoid changing a component's role merely because it occurs inside another quantity's formula.

Honor an existing highlight toggle and preserve its source setting. If introducing highlights without a toggle, add one following project conventions or, where none exist, the native format's styling mechanism. Turning highlights off must retain every mathematical and textual element, including the guide. Avoid nested or duplicate wrappers.

This skill owns identification of key terms, concepts, notation and relationships; semantic mapping design; and the authoritative opening guide's explanation, conceptual table, placement, hierarchy, anchors and navigation. When document-wide highlighting or corrections beyond the guide are required, establish the guide and semantic mapping first, then read and apply [math-practice-highlights](../math-practice-highlights/SKILL.md). That skill owns the general workflow, application throughout the document, detailed markup mechanics, renderer integration, diagram styling, toggles and highlighting validation.

If both skills are already active, continue with the next unfinished responsibility rather than invoking either again. Share one semantic mapping, one authoritative legend per guide, and the existing styling infrastructure; reuse completed work on reruns. If the companion skill is unavailable, retain a standalone workflow: apply the agreed mapping with the native format's existing markup and toggle, use the short component-level rules above, build/export and inspect the guide and relevant body examples, and report any uncompleted document-wide work. Do not inherit subject-specific assumptions or require conversion to LaTeX. Use an appropriate format skill for native editing/export where available. For LaTeX-specific integration, read [references/latex.md](references/latex.md).

## Preserve content and layout

Preserve existing mathematical meaning, wording, values, notation, assumptions, exercises, solutions, labels, and hyperlink targets except for the new guide, explicitly requested notation coordination, and necessary structural changes. Report suspected mathematical errors separately; do not silently correct them without authorization.

Keep the heading, explanation, and complete table together when practical. Prioritize early placement, readable type, adequate spacing, and sensible page breaks. Adapt table structure or placement before shrinking text. Preserve titles, contents, learning objectives or criteria, practice guidance, and existing solution page breaks or reserved space unless rendered inspection demonstrates a necessary adjustment.

## Validate and deliver

- Follow the established build or export process. Review the source diff or the native format's equivalent comparison for content preservation and unintended edits.
- Check for duplicate legends, labels, inputs, toggles, registry entries, and highlight wrappers. Verify the guide precedes substantial highlighted examples and detailed references, and that a repeat run would reuse the same guide and supporting definitions.
- Inspect rendered opening pages for heading hierarchy, legibility, overflow, spacing, and page breaks. Verify contents links, guide anchors, and return navigation in the output, including targets retained from moved content.
- For a highlight toggle, build temporary enabled and disabled versions and inspect both. Check content retention and legibility with highlights off and in grayscale. Preserve the original source setting; use isolated copies or build overrides that retain relative dependency resolution.
- For coordinated documents, verify notation and semantic treatments against the reference and across all targets. Verify the reference source is unchanged and compare its rendered output before and after supporting edits.
- When shared definitions change, check affected consumers for compatibility, building/rendering them where needed. Remove temporary validation artifacts according to project conventions; preserve pre-existing files and intended deliverables.

Deliver the revised source, necessary supporting legend or styling changes, and compiled/exported document when supported. Give a concise account of structural changes, validation performed, suspected errors, and unresolved limitations. If tools cannot build, render, or verify navigation, state exactly which checks remain unverified; do not claim they passed.
