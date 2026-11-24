from pathlib import Path
base=Path('.agents/skills/global-economics-classroom-activity')
p=base/'assets/template_classroom_activity.tex'
s=p.read_text(encoding='utf-8')
s=s.replace('% subtask titles, and white criterion boxes are structural styles. Semantic','% subtask titles, white criterion boxes, and neutral guided response boxes are\n% permitted structural/response-area styles. Semantic')
s=s.replace('\\newcommand{\\responseline}{\\par\\noindent\\rule{0pt}{1.55em}\\hrulefill\\par}\n','').replace('\\newcommand{\\workspace}[1]{\\par\\noindent\\rule{0pt}{#1}\\par\\nopagebreak[4]}\n','')
a=s.index('% Exactly one guided example;')
b=s.index('% Exactly five UNSOLVED',a)
s=s[:a]+r'''% Exactly one guided example. Preserve its actual context, givens, values,
% task order, intermediate calculations, representations, explanations, and
% interpretations when updating; replace only response areas and layout.
\begingroup % Guided Example ONLY: helpers cannot reach other activity sections.
% Guided response boxes: neutral writing areas, never semantic highlights.
% Width and height are minimum dimensions; the invisible 0 anchors the baseline.
% Nothing visible belongs inside: no placeholders, underlines, hints, or answers.
\newcommand{\guidedresponsebox}[2][9mm]{%
    \tikz[baseline=(answer.base)]{%
        \node[fill=black!1,draw=black!25,line width=.3pt,
            rounded corners=2mm,inner sep=0pt,outer sep=.3pt,
            minimum width=#2,minimum height=#1] (answer) {\phantom{0}};}}
% Reserve measured prompt+pair height BEFORE its heading. Each call starts a
% fresh paired row; do not stack subsequent stages in unequal-height columns.
\NewDocumentCommand{\guidedpair}{+m +m}{%
    \par\noindent\begin{minipage}[t]{.49\linewidth}\vspace{0pt}\raggedright
        #1
    \end{minipage}\hfill
    \begin{minipage}[t]{.49\linewidth}\vspace{0pt}\raggedright
        #2
    \end{minipage}\par\addvspace{4pt}}
\stageheading{Guided Example}
\problemtitle{2}{[Guided problem title]}{Type A}
[Fresh context, givens, units, and constraints. Illustrative structure: two
cases share a first quantity of 15 units; second quantities are 6 and 9 units.
Replace with the actual topic's givens and case structure.]
\task{Task 1 --- Shared quantity, units, and meaning.}{}
\subtaskheading{1}{Shared information}
\InformationTable{
    \TableGroup{Shared information}
    $a$ & First quantity & 15 units.\par
      Meaning: \par\nopagebreak[4]
      \guidedresponsebox[18mm]{\dimexpr\linewidth-1pt\relax} \\ \hline
}
% All dimensions are adjustable starting points, not universal handwriting sizes.
% Numbers: 12mm x 9mm; fractions: 16mm x 12mm; expressions: 35mm x 10mm;
% event names: 45mm x 10mm; interpretations: local width x 22mm or taller.
% Place all prompts, supplied steps, and units OUTSIDE the empty boxes.
\Needspace{22\baselineskip}
\task{Task 2 --- Totals, differences, and contextual meanings for each case.}{}
\guidedpair{
    \subtaskheading{1}{Case A calculations}
    \CalculationTable[.14\linewidth][.24\linewidth]{
        \TableGroup{Case A}
        $b$ & Second quantity & 6 units. [Contextual meaning.] \\ \hline
        $T$ & Total & $T=a+b=15+6=$\par\nopagebreak[4]
          \guidedresponsebox{12mm} \\ \hline
        $d$ & Difference & \guidedresponsebox[18mm]{\dimexpr\linewidth-1pt\relax} \\ \hline
    }
}{
    \subtaskheading{1}{Case B calculations}
    \CalculationTable[.14\linewidth][.24\linewidth]{
        \TableGroup{Case B}
        $b$ & Second quantity & 9 units. [Contextual meaning.] \\ \hline
        $T$ & Total & \guidedresponsebox[18mm]{\dimexpr\linewidth-1pt\relax} \\ \hline
        $d$ & Difference & \guidedresponsebox[18mm]{\dimexpr\linewidth-1pt\relax} \\ \hline
    }
}
% Fresh paired row aligns the next stage despite unequal calculation heights.
% Break at meaningful stage boundaries; never prescribe reference page numbers.
\Needspace{12\baselineskip}
\guidedpair{
    \subtaskheading{2}{Case A interpretation}
    [Required contextual meaning.]\par\nopagebreak[4]
    \noindent\guidedresponsebox[22mm]{\dimexpr\linewidth-1pt\relax}
}{
    \subtaskheading{2}{Case B interpretation}
    [Required contextual meaning.]\par\nopagebreak[4]
    \noindent\guidedresponsebox[22mm]{\dimexpr\linewidth-1pt\relax}
}
% When needed, add corresponding graphs in a fresh paired row within the same
% stage. Preserve every original representation and supplied intermediate step.
\par\clearpage % Flush Guided Example before restoring all helper definitions.
\endgroup

'''+s[b:]
p.write_text(s,encoding='utf-8')

p=base/'SKILL.md';s=p.read_text(encoding='utf-8')
s=s.replace('All three heading levels (including bold underlining) and criterion boxes are explicitly permitted structural styling, distinct from prohibited semantic instructional highlights:', 'All three heading levels (including bold underlining), criterion boxes, and neutral guided response boxes are explicitly permitted structural or response-area styling, distinct from prohibited semantic instructional highlights:')
s=s.replace('Keep guided tables partially blank with adequate writing space; explicit row gaps are adjustable starting points.', 'In Guided Example tables, put empty guided response boxes in student-answer cells with adequate handwriting space; row gaps alone do not replace the boxes.')
pos=s.index('### Three structural heading levels')
s=s[:pos]+'''### Guided response boxes

Inspect the actual local helpers and rendered Guided Example PDF of the [G10 T2 L1 C3 reference](../../../book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex) before adapting its response-area styling. Generalize across grades, terms, topics, and criteria; do not import its mathematics or fixed page distribution. Call these **guided response boxes**, never semantic highlights. Their neutral styling is permitted while semantic color coding and highlight legends remain prohibited.

Replace student answer underlines in the Guided Example with empty writing boxes; preserve bold underlined numbered subtask headings. Use `fill=black!1`, `draw=black!25`, `line width=.3pt`, and `rounded corners=2mm`, matching the section-heading corner radius. Students write directly inside: no visible placeholders, underlines, hints, or answers inside boxes. Keep supplied prompts and steps outside them. Preserve the Guided Example's context, givens, values, task order, intermediate calculations, representations, explanations, and interpretations.

Use the scaffold's adjustable-width/height baseline-anchored helper inside a group confined to the Guided Example, flushed before its end. Helpers and any spacing changes must not affect worked examples, independent exercises, criterion boxes, or appended solutions. Size for expected numbers, fractions, algebraic expressions, event names, and verbal interpretations; fractions need extra vertical clearance and longer responses need wider or multiline-height boxes. Preserve mathematical baselines and spacing, including fraction bars, delimiters, aligned equations, and table rows. See the layout guide for usage and starting dimensions.

Keep each prompt with its response area and every heading with opening content. Place corresponding case headings, calculations, graphs, and response areas in top-aligned paired blocks; begin subsequent corresponding stages in fresh paired rows. Use meaningful stage boundaries for page breaks, positive spacing, readable type, fixed margins, and comfortable handwriting space. Never force the reference's page numbers or compact by negative spacing, smaller fonts, scaling, or omitted steps.

'''+s[pos:]
s=s.replace('All three heading levels, including bold underlined numbered titles, and criterion boxes are permitted structural styles;', 'All three heading levels, including bold underlined numbered titles, criterion boxes, and neutral guided response boxes are permitted structural or response-area styles;')
s=s.replace('- Exactly one guided example provides structured prompts and sufficient workspace for students to finish the solution.', '- Exactly one guided example provides structured prompts and empty guided response boxes for students to finish the solution. Verify the exact neutral fill/border/line/corner settings; no visible placeholders, answer underlines, hints, or answers inside boxes; bold underlined numbered headings remain.\n- Check numerical, fractional, algebraic, event-name, and verbal response sizes, extra fractional clearance, wider or multiline-height writing areas, mathematical baselines, and local helper scope. Preserve all original guided content and task order.\n- Inspect every rendered page for box appearance, handwriting clearance, alignment, wrapping, clipping, overlap, and page breaks. Keep prompts with boxes, headings with opening content, and corresponding cases/calculations/graphs/response areas top-aligned in fresh paired stage rows. Use meaningful breaks and positive spacing without shrinking type, scaling, negative spacing, omitted steps, or fixed reference pagination.')
p.write_text(s,encoding='utf-8')

p=base/'references/template_classroom_activity.md';s=p.read_text(encoding='utf-8')
s=s.replace('All three structural heading levels, including bold underlined subtask titles, and criterion boxes are explicitly permitted.', 'All three structural heading levels, including bold underlined subtask titles, criterion boxes, and neutral guided response boxes are explicitly permitted structural or response-area styling.')
s=s.replace('In the guided example, leave blank cells, lines, or space for calculations or sketches when needed.', 'In the Guided Example, use empty guided response boxes for student answers and retain required graphing space.')
s=s.replace('- Use `\\workspace{<height>}` for adjustable blank working space and `\\responseline` for short answers. The scaffold\'s heights are starting points: expand them to fit the actual reasoning, calculations, tables, or graphs. Keep guided prompts next to their response spaces; reserve the measured prompt-plus-workspace block before its subtask heading, as the scaffold does for the final interpretation. Independent problems follow one another compactly without answer space.', '- Use the Guided Example-only `\\guidedresponsebox[<height>]{<width>}` and `\\guidedpair{<left>}{<right>}` helpers described below. Reserve the measured prompt-plus-response block before its heading. Independent problems follow one another compactly without answer space.')
s=s.replace("Guided tables must stay partially blank, leaving key reasoning and final answers for students. The reference's explicit row gaps (such as `\\\\[10pt]` or `\\\\[16pt]`) are adjustable starting points, not universal heights: size each blank row for the expected handwritten calculation and explanation.", 'Guided tables use empty guided response boxes for key reasoning and final answers. Size their boxes and rows for the expected handwritten calculation and explanation; explicit row gaps alone are not response areas.')
s=s.replace('All three heading levels and criterion boxes are structural exceptions only.', 'All three heading levels, criterion boxes, and neutral guided response boxes are permitted structural or response-area styles only.')
pos=s.index('## Exactly two table-style families')
s=s[:pos]+r'''## Guided response boxes

Inspect the local helpers and actual rendered Guided Example pages of the [G10 C3 reference](../../../../book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex) before adaptation. Its `\writingbox` uses a TikZ node with an invisible `\phantom{0}` baseline anchor; its short, calculation, probability, and word variants demonstrate adjustable response dimensions. Adopt the neutral response-area styling across grades, terms, topics, and criteria, without importing its mathematics, fixed page distribution, or compact spacing settings.

Call these **guided response boxes**, not semantic highlights. They are explicitly permitted neutral response areas; semantic color coding and highlight legends remain forbidden. Replace guided student-answer underlines with boxes, retaining bold underlined numbered subtask headings. Use exactly `fill=black!1`, `draw=black!25`, `line width=.3pt`, and `rounded corners=2mm` (the section-heading radius). Students write directly inside. Interiors contain no visible placeholders, underlines, hints, or answers; invisible baseline anchors are allowed. Prompts, units, supplied calculations, and explanations stay outside.

The scaffold defines `\guidedresponsebox[<height>]{<width>}` only inside a Guided Example group. Its default minimum height is 9 mm; both dimensions are adjustable. `baseline=(answer.base)` with `\phantom{0}` preserves the surrounding text/math baseline while TikZ reserves the box's real height/depth. Do not hide dimensions with `\smash`, force overlap, or scale the equation. Check inline math, fraction numerators/denominators, displays, and aligned rows at their actual sizes. Increase positive row spacing where needed.

| Expected handwritten response | Starting width and height; adjust to actual response |
| --- | --- |
| Short number | 12 mm by 9 mm |
| Fraction | 16 mm by 12 mm, with extra vertical clearance for both levels and the bar |
| Algebraic expression | 35 mm by 10 mm or wider/taller for its terms |
| Event name | 45 mm by 10 mm or wider for natural language |
| Verbal interpretation | Local available width by 22 mm or taller for multiple handwritten lines |

```latex
% Inside the Guided Example group only:
Count: \guidedresponsebox{12mm}.
\[
  r=\guidedresponsebox[12mm]{16mm},\qquad
  z=\guidedresponsebox[10mm]{35mm}
\]
Name the event: \guidedresponsebox[10mm]{45mm}.
\par\Needspace{8\baselineskip}
\subtaskheading{2}{Interpretation}
State the contextual meaning.\par\nopagebreak[4]
\noindent\guidedresponsebox[22mm]{\dimexpr\linewidth-1pt\relax}
```

These examples illustrate response shapes, not required mathematics. In table cells use the cell's local `\linewidth`, reserving room for the stroke/outer separation as above. Break a long prompt or equation naturally before its box if needed. A multiline box is an empty taller writing area, without printed ruling or placeholder text.

Use `\guidedpair` for corresponding case headings, calculations, graphs, and response areas in top-aligned blocks. Each call creates a fresh row of `.49\linewidth` minipages beginning with `\vspace{0pt}`. Start every subsequent corresponding stage in another call, so unequal calculation heights do not stagger later headings. Use a shared stage heading if matching headings cannot fit. Reserve each measured heading/prompt/pair with `\Needspace` before it starts; keep prompts with their response areas and headings with opening content. Use full width if paired content would crowd handwriting or clip mathematics.

Preserve the existing Guided Example's context, givens, values, task order, intermediate calculations, representations, explanations, and interpretations. Change response areas and layout without deleting or solving steps. Break pages at meaningful stage boundaries; let content and comfortable handwriting space determine pagination. Keep fixed margins, readable type, and positive spacing. Do not copy reference page numbers or compact by negative spacing, smaller fonts, scaling, or omitted steps. Flush the Guided Example before closing its group. Its helpers and spacing settings must not affect worked examples, independent exercises, criterion boxes, or appended solutions.

'''+s[pos:]
s=s.replace('- Check the guided prompts leave meaningful work for students and have sufficient response space.', '- Check guided response boxes have the exact neutral fill, border, line width, and 2 mm corners; interiors are empty without visible placeholders, underlines, hints, or answers. Preserve bold underlined numbered headings. Verify adequate number, fraction, algebraic, event-name, and verbal handwriting space, extra fraction clearance, and wider or multiline areas for long responses.\n- Inspect every rendered page for box appearance, baselines, handwriting clearance, alignment, wrapping, clipping, overlap, and page breaks. Verify top-aligned case headings/calculations/graphs/response areas, fresh paired stage rows, prompt/box and heading/opening-content protection, positive spacing, readable type, and fixed margins. No fixed reference pagination, negative spacing, smaller fonts, scaling, or omitted steps.\n- Verify Guided Example-only helper scope and unchanged context, givens, values, task order, intermediate calculations, representations, explanations, and interpretations. Check guided prompts leave meaningful work for students and have sufficient response space.')
p.write_text(s,encoding='utf-8')
