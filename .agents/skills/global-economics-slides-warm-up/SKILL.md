---
name: global-economics-slides-warm-up
description: Create or update a prerequisite warm-up of at most two minutes in an existing Global Economics LaTeX Beamer lesson, using its corresponding practice. Use for warm-up insertion or revision across grades, terms, topics, and criteria; full lesson authoring belongs to global-economics-slides.
---

# Global Economics Slides Warm-up

Extend an existing deck with one focused prior-knowledge exercise. Preserve the lesson and practice; this is not a request to regenerate the deck.

## Resolve sources and editing mode

- Accept a slides path, a practice path, or both. Read applicable repository instructions. Infer the missing partner from actual neighboring filenames, deck source comments, and document metadata: book year, grade, term, lesson, criteria, and meaningful variant suffixes. Typical sibling folders are `3-slides` and `1-practice_activities`, with `_slides.tex`, `_practice.tex`, or `_practice_activity.tex` suffixes; verify rather than mechanically substitute. If both paths are supplied, confirm their instructional correspondence. Do not silently choose an unrelated variant or create a missing deck. Ask only when essential source identity or an instructional boundary remains unresolved.
- Read both sources, including relevant definitions or inputs, to identify actual student tasks, assumed prerequisites, notation, language, and mathematical demands. Distinguish what the lesson teaches from what students can already use. Topic titles and criterion wording alone do not establish the task type or prerequisite.
- Use [global-economics-slides](../global-economics-slides/SKILL.md) for established Beamer, highlight, reveal, numbering, and portability conventions. Reuse the existing deck; do not copy its starter, import additional classroom examples, or reapply its full authoring sequence. This skill supplies the warm-up content allowance and placement.
- Route ordinary changes through [update-latex-complete](../update-latex-complete/SKILL.md) and its linked verification workflow. For an explicit fast/source-only request, use [update-latex-fast](../update-latex-fast/SKILL.md) instead: its no-verification boundary overrides the checks and PDF delivery below. Make pedagogical choices during source editing, then stop without post-edit checking.

## Choose a two-minute entry point

Choose **one** useful prerequisite or thinking move with a specific connection to the upcoming lesson. Students must be able to attempt it before learning that lesson; a new formula or procedure taught later is not assumed prior knowledge merely because it appears in the practice introduction or opening legend.

| Actual practice demands | Preferred warm-up |
| --- | --- |
| Predominantly procedural | A brief calculation, simplification, comparison, estimate, or recognition of a useful mathematical relationship. |
| Predominantly mathematization | A short familiar situation asking students to identify quantities, choose variables, state an assumption, select a representation, or explain how it could be modeled. |
| Mixed | The most useful entry point; combine calculation and interpretation only if both fit comfortably. |

Use one focused exercise with at most two tightly connected micro-prompts. Favor accessible numbers, concise wording, and familiar representations. Avoid lengthy contexts, full derivations, substantial graph construction, research, or tools unless clearly appropriate and feasible within the same limit. A fresh miniature exercise within verified source scope is allowed. Do not reuse an upcoming example's or independent exercise's givens to reproduce or reveal its answer.

Budget **at most 120 seconds total**, including reading, thinking/calculating, and a brief answer check and connection. Allocate each part explicitly in source comments; for example, 15 s reading + 65 s work + 40 s check/connection = 120 s. Adapt these allocations to the actual task and learners; a nominal time label does not make a long task feasible. Show a simple student work-time cue on the prompt, in the deck's language, matching the allotted work time.

## Integrate narrowly

- Find an existing warm-up by its content, headings, comments, and overlays, including language variants. Update it in place instead of adding a duplicate. Default placement is after the **complete consecutive opening highlight legend** and before the first instructional example; honor explicit placement.
- Default to two logical frames: student prompt, then concise answer/check with a short connection to the lesson. A single frame with a stable answer overlay is also acceptable. Keep the answer hidden until the intended reveal, including in titles, diagrams, captions, and hints. For open modeling, give one defensible response with its assumptions and acknowledge relevant alternatives rather than implying uniqueness.
- Match the deck's language, visual style, mathematical notation, semantic highlights, footer, and logical frame numbering. Reuse existing macros and toggle settings; keep standalone definitions inline and avoid introducing repository inputs or absolute resource paths. Reserve overlay geometry with the deck's stable reveal mechanism. Allow totals to update normally; do not manipulate counters or add automatic section-divider frames.
- Preserve all existing lesson content and the complete opening legend. Do not rewrite the preamble, redesign an adequate legend, change shared mappings, or modify the practice. Consult the slide skill's linked highlight companions only if a local integration issue requires them, without expanding scope.
- Add concise LaTeX comments beside the warm-up recording both repository-relative source paths, relevant task/section anchors, chosen prerequisite, instructional connection, and realistic reading/work/check time allocations and total. Keep implementation notes out of student-facing content.

## Verify and deliver

In complete mode, follow the linked update workflow for scoped source review, mathematics, isolated compilation, rendered inspection, relevant variants, and repair. In particular, verify:

- The exercise activates a supported prerequisite, fits the actual practice demands, and does not require the lesson's new learning or expose upcoming answers.
- Calculations, assumptions, units, and any modeling alternatives are defensible; the entire activity can realistically finish within two minutes, with a matching student cue.
- The opening legend and lesson content remain intact, the warm-up occurs once at the intended location, and the answer is visibly hidden until its reveal.
- Readable layout, stable first/final and any intermediate overlays, footer/section labels, logical frame numbers and settled totals, and standalone portability are preserved.

Deliver the modified `.tex` and a matching PDF when compilation and inspection are available and appropriate. Report checks that could not run; never present a stale PDF as revised. Briefly explain why the selected prerequisite prepares students for this particular lesson. In fast mode, deliver only the source and change explanation, with the fast workflow's required unverified-status statement.
