---
name: global-economics-slides
description: Create student-facing LaTeX Beamer decks for live Global Economics lessons from practice activities, pasted excerpts, or lesson briefs.
---

# Global Economics Slides

## Plan the lesson

1. Treat a supplied practice activity, including a newly authored one, as lesson input. Plan from its introduction. A pasted excerpt or a brief with a topic and learning objective can also be the input. For a brief, use clearly illustrative economic or financial examples. If a faithful adaptation of a named practice requires contents you cannot access, ask for the relevant excerpt.
2. Open with the topic and any supplied grade, term, lesson, and criterion. Preserve official criterion wording when available. When working from a topic or brief without official wording, state a clear **Learning objective** without presenting it as an official criterion.
3. Begin the teaching sequence with the motivating situation. Identify what students are studying, ask for a prediction or interpretation, and give students an overlay to respond before revealing the explanation. Split longer explanations into frames with one main idea each. Keep the source notation, definitions, assumptions, values, units, and scope, and include its quick check when present.
4. If the introduction covers only part of the criterion, teach the missing part through one representative worked application from the practice. Keep the remaining exercise bank for independent practice. Use side-by-side table columns for paired concepts, displayed equations for short calculations, and a separate comparison frame when it helps students interpret a change. Reveal answers, worked steps, and conclusions in teaching order. End with a compact summary of the relationships students should remember.

## Build and deliver

- Copy the [standalone Beamer starter](assets/beamer_starter.tex). Replace its illustrative frames and role colors to suit the lesson. Keep the theme, macros, and highlight definitions inline in every deck. Use standard LaTeX packages and keep compilation independent of the practice source, repository preambles, and other skills.
- Keep the 12 pt, 16:9 layout, white canvas, ink `132A3E`, teal `17675E`, pale teal footer `EAF2F1`, bold titles, approximately 9 mm side margins, and hidden navigation icons. Group frames under short section labels. The footer shows that section and the logical frame number over the total.
- Reveal content with `\visible<2->{...}` or an equivalent that reserves its space. In a table, reveal within cells so the column widths, rows, and rules stay put. Split crowded frames before reducing type size.
- Use `\GEHighlight{<role color>}{<short text or math>}` for key phrases, symbols, or values. Define each role's color in the deck and reuse the marker across prose, tables, and equations. For several roles, introduce a compact legend and reuse it in the summary when useful. Give roles readable labels and distinct notation wherever applicable so students can follow without color.
- Honor the requested destination. For book lessons, default to `book<year>/grade<grade>/term_<term>/3-slides/G<grade>_T<term>_L<lesson>_<criteria>_slides.tex`, using the book year and criterion naming from the task context. Deliver the `.tex` and, when LaTeX is available, the matching PDF.
- Compile in an isolated build directory using only the deck source and standard LaTeX packages. Run Beamer twice or until frame totals settle, then copy the PDF to the delivery folder. Check the arithmetic, units, and interpretation. Inspect early and final overlays for answer timing, table fit, and stable placement. Verify that the footer shows the current section, repeats the logical frame number through its overlays, and ends at the correct total. Report any verification you could not run.

## Worked storyboard for Grade 11, Term 2, Lesson 1, C1

**Learning objective** — Distinguish population parameters from sample statistics by interpreting the notation for means, standard deviations, and proportions.

1. **Electricity bills.** Start with all May electricity bills for small shops in one district. Ask which bills form the population and which form the sample when 40 bills are drawn at random. Reveal both groups, then pair the unknown population mean `\mu` with `\bar{x}=210` thousand COP for the sample.
2. **Quick check.** Ask which population mean a fresh random draw from the same list estimates. Reveal that the target is still the May mean for small shops in the original district. Next ask what changes when the list covers two districts. Reveal that the target is the May mean for small shops across both districts. The two target means can coincide numerically.
3. **Market survey.** Use this application to extend the lesson to standard deviations and proportions. The population consists of 1,200 June-licensed stalls. In the first random sample of 60, mean June sales are 4.8 million COP, the standard deviation is 1.2 million COP, and 18 stalls accept digital payment. Ask students to identify the three sample summaries and compute the payment share, then reveal `\hat{p}=18/60=30\%`.
4. **Pair the notation.** Reveal side by side the population and sample mean June sales (`\mu` / `\bar{x}`), standard deviation of June sales (`\sigma` / `s`), and proportion accepting digital payment (`p` / `\hat{p}`). Use green-family markers for sample roles and red-family markers for population roles. Use a compact legend with separate labels for the group, mean, standard deviation, and proportion within each family. Reuse those markers for the contextual labels, symbols, and values.
5. **Compare draws.** A fresh random draw from the same list gives 5.1 million COP, 1.0 million COP, and 25%, respectively. Ask what changed, then reveal second draw minus first draw as `+0.3` million COP, `-0.2` million COP, and `-5` percentage points.
6. **Summarize.** The parameters of the defined population are fixed. The sample statistics can vary across draws. Revisit the paired symbols and their roles.
