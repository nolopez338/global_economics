# Procedure diagrams for home practice

## Structural model and teaching sequence

Identify procedure families before composing their pictures. For each family, record meaningful stage identities/headings and logical order; common inputs and outputs; parallel cases, alternatives, variables or methods; branches, merges, checks and possible extensions. Use one family when adequate. Different mathematics may need another family, with a brief explanation of the relationship. A family is a reasoning structure, not a fixed formula, grade, step count or visual theme.

Declare the stage structure once, independently of values and presentation. In the default layout, stages run left to right as tall rectangular containers. Cases occupy numbered horizontal lanes, stacked vertically inside each stage. Corresponding case content has the same vertical center across stages. One common source may occupy a shared node with several outgoing edges. Use a single lane for a simple procedure; do not manufacture cases or empty stages.

Preserve the activity's four-stage structure, front matter, exact criteria, legends and navigation:

1. **Introduction:** concise legend first, then at least two introductory examples. Immediately after a relevant example, introduce its family through a detailed diagram using its actual data. Explain what every quantity, symbol, unit, lane, arrow, intermediate result and output represents. Distinguish a general rule from its numerical application and show the substitutions that make transitions understandable. Introduce every distinct family before using its compact form.
2. **Notation Reference and Practice Procedure:** keep the four-column notation reference and example links. Match the reusable written steps explicitly to the introductory stage names and order, then show a concise generalized diagram for each family using symbolic notation. Refer back to the detailed introduction rather than repeating it.
3. **Worked solutions:** include a compact procedure summary after the reasoning and before `\secInicio`, for every general, follow-up and advanced worked task. Supply that problem's actual inputs, substitutions, important intermediate values, results and units. Separate distinct procedures into summaries, or label a clearly divided composite. Compact removes repeated explanations, not the mathematical chain.

Diagrams complement written justification. Never introduce unexplained notation or add completed summaries to independent/assessed tasks whose solutions are withheld.

## Portable loading and ownership

The single authoritative implementation is [assets/practice_procedure_diagrams.tex](../assets/practice_procedure_diagrams.tex). The scaffold inputs `practice_procedure_diagrams.tex` by filename. When creating an activity, copy that asset **beside the activity source**, once per source directory, and keep it with the activity's support files when sharing or moving it. This is an intentional deployed snapshot, not another authoritative implementation. It needs no skill-directory lookup, machine-specific path, network, shell escape or externalization. The repository preamble remains a declared repository dependency.

From the repository root, for example (replace only the destination):

```powershell
$skillDirectory = '.agents/skills/global-economics-home-practice'
$activityDirectory = 'book/grade10/term_2/1-practice_activities'
$deployedAsset = Join-Path $activityDirectory 'practice_procedure_diagrams.tex'
if (-not (Test-Path -LiteralPath $deployedAsset)) {
    Copy-Item -LiteralPath "$skillDirectory/assets/practice_procedure_diagrams.tex" -Destination $deployedAsset
}
# Copy/adapt the scaffold separately, preserving existing activity sources.
```

For an existing deployment, compare it against the canonical asset and inspect all local consumers before updating. Preserve local changes: merge deliberately, or retain the customized snapshot and explain the difference. Do not overwrite on every generation, silently update neighboring activities, or edit a deployed copy as though it were the master. The header records the asset version; update it for future API changes. If using a different support subdirectory, change the activity's explicit input accordingly and test from its source directory. Do not depend on `TEXINPUTS` pointing to the skill's assets.

Load after the shared preamble and highlight renderer, before `\begin{document}`:

```tex
\input{preamble_exams.tex}
\input{highlights/highlights.tex}
% \GTenHighlightsfalse % preserve an existing toggle's state
\input{practice_procedure_diagrams.tex}
```

The asset explicitly loads TikZ, `amsmath`, `xparse`, and TikZ's `arrows.meta`/`positioning` libraries. Its input guard permits a repeated input without redeclaration. Its `PP` commands, `/ppd` configuration keys and `ppd/...` TikZ styles are namespaced. Diagram options, styles, lengths and stage locations are locally scoped; only family declarations, the load guard and a unique diagram counter persist. Automatic diagram prefixes allow stage/case identifiers to repeat safely across pictures. Use simple letter-led ASCII identifiers containing letters, digits or hyphens; stage IDs must be unique within a family, and cell IDs unique within a picture. Do not put problem text, mathematics, spaces or punctuation into IDs.

## Small API

| Invocation | Purpose |
| --- | --- |
| `\PPDeclareFamily{id}{declarations}` | Declare a reusable stage sequence in the preamble; an existing ID is an error, avoiding silent replacement. |
| `\PPStage{id}{heading}` | A named stage rectangle in a family declaration. |
| `\PPExtension{id}{heading}{short label}` | Another stage at this exact point in the declaration, with a meaningful extension label beneath its heading. Same neutral visual convention. |
| `\begin{PracticeProcedure}[options]{family}{lane count} ... \end{PracticeProcedure}` | Render that family and provide its content/connections. Positive integer lane count. Non-floating and unbreakable; split large pictures into linked panels. |
| `\PPCell{stage}{lane}{content}` | Wrapped, centered content in a numbered lane (`1` is the top lane). |
| `\PPShared{stage}{content}` | One shared node centered across the stage's lanes. Use instead of repeating a common source, or for a merged output. |
| `\PPConnect[TikZ options]{source}{destination}{label}` | Directed connection; endpoint is `stage-1`, `stage-2`, etc., or `stage-shared`. Declare nodes before connecting. Empty label `{}` draws an unlabelled arrow. Repeat connections to branch/merge. |
| `\PPAnnotation[TikZ options]{stage}{short explanation}` | Wrapping annotation below that stage's rectangle. One per stage; leave room in the page budget. |
| `\PPPanel{stage}{lane}{content}` | Same placement as `PPCell`, explicitly marking an optional small mathematical table or graph panel. The activity supplies its content/dependencies. |

Content is ordinary text-mode LaTeX: inline mathematics, units, prose, `\\`, `\par`, `\(\begin{aligned}...\end{aligned}\)`, `gathered`, `tabular`, or a local graph sized to the cell's `\linewidth`. Prose wraps. TeX does **not** automatically break long math expressions: insert meaningful line breaks, distribute a calculation across stages, or split the panel. Avoid display environments with large surrounding skips inside a cell. Use the established semantic macros in the current text/math mode, including distinct component roles in a composite expression; keep relations, operators, alignment tokens and line breaks outside highlight wrappers.

### Layout options

Defaults are applied afresh for each picture; place overrides after `mode` so they win.

| Option | Default / meaning |
| --- | --- |
| `mode=detailed` | More room for introductory reasoning: 32 mm lane height, 14 mm heading height. |
| `mode=compact` | Default: 24 mm lane height, 14 mm heading height. Same structure and normal document font; the author supplies shorter content. |
| `stage width=auto` | Equal widths using the enclosing `\linewidth`, number of stages and column gaps, including an allowance for frame strokes. Or supply a dimension such as `48mm`. |
| `column gap=8mm` | Space between adjacent stage rectangles, including arrow/label room. |
| `padding=2mm` | Inner horizontal margin; clearance budget for headings and cells. |
| `lane height=...` | Center-to-center vertical spacing, shared across all stages. Choose for the tallest lane content. |
| `heading height=...` | Same heading band across every stage; increase for long or extension headings. |
| `annotation gap=3mm` | Clearance below frames before annotations. |

No mode changes mathematical meaning, node selection or highlight state. Both retain the same normal-size font. The asset warns if boxed content is taller than its reserved height; it does not auto-shrink or auto-paginate. Also inspect standard overfull-box warnings and actual renders. A common width, heading band and lane grid deliberately keep content aligned; use panels when uniform width leaves a mathematically dense stage unreadable. Not every family needs the same physical dimensions.

The environment leaves 3 mm of positive clearance after each picture so the repository's upward-offset return-navigation box cannot erase a frame border. Keep diagrams before the return command; do not counteract this clearance with negative spacing.

Connections normally run east to west. `ppd/mapping` makes a dashed directed mapping; `ppd/correspondence` makes a dotted undirected correspondence. Add a short label whenever the meaning of a line would be ambiguous. Other options include `bend left=12`, `out=0,in=180`, and `ppd/from anchor=south,ppd/to anchor=north`. Use these for real logical branching/checks, not decorative crossings. Keep labels short; widen gaps before labelling busy routes. Neutral frames and connections remain visible in grayscale and with highlights disabled. The asset never assigns instructional meaning to a color or tests the highlight switch to remove content.

## Runnable detailed/compact example

Save the following beside a copied asset and compile from that directory with the repository's normal preamble search path (see the [authoring guide](template_home_practice.md)). This is an isolated API demonstration, not a complete student activity. A scaffold-based activity must retain both legends, at least two introductory examples, all four required stages and navigation.

```tex
\input{preamble_exams.tex}
\input{highlights/highlights.tex}
% \GTenHighlightsfalse
\input{practice_procedure_diagrams.tex}
\PPDeclareFamily{travel}{%
  \PPStage{given}{Known quantities}%
  \PPStage{speed}{Rate and substitution}%
  \PPStage{check}{Result and check}}
\newcommand{\TravelEdges}{%
  \PPConnect{given-1}{speed-1}{}%
  \PPConnect{speed-1}{check-1}{}}
\begin{document}
A journey covers 120 km in 2 hours at constant speed.
\begin{PracticeProcedure}[mode=detailed]{travel}{1}
  \PPCell{given}{1}{Distance $d=120\,\mathrm{km}$\\Time $t=2\,\mathrm{h}$}
  \PPCell{speed}{1}{General rule: $v=d/t$\\Apply: $v=120/2$}
  \PPCell{check}{1}{$v=60\,\mathrm{km/h}$\\$60\times2=120\,\mathrm{km}$}
  \TravelEdges
\end{PracticeProcedure}
Each rectangle groups a reasoning stage; the single lane follows this journey.
Arrows carry the known quantities into the rate calculation and then the
result into the distance check. Here $v$ is distance per hour, not total distance.
\begin{PracticeProcedure}[mode=compact]{travel}{1}
  \PPCell{given}{1}{$d=120\,\mathrm{km}$\\$t=2\,\mathrm{h}$}
  \PPCell{speed}{1}{$v=d/t=120/2$}
  \PPCell{check}{1}{$v=60\,\mathrm{km/h}$\\$vt=120\,\mathrm{km}$}
  \TravelEdges
\end{PracticeProcedure}
\end{document}
```

### Parallel cases, shared inputs and a merge

Use actual case names in the nodes; lane numbers are implementation positions. For example, two tariffs share a fixed fee and usage but have different unit rates. Declare once, then reuse the same stage list for detailed, generalized and worked versions:

```tex
% Preamble:
\newcommand{\TariffStages}{%
  \PPStage{given}{Shared inputs}%
  \PPStage{model}{Model and calculation}%
  \PPStage{cost}{Cost and check}}
\PPDeclareFamily{tariffs}{\TariffStages}
\PPDeclareFamily{tariffs-credit}{\TariffStages
  \PPExtension{credit}{Payable amount}{Membership credit}}
% In document:
\begin{PracticeProcedure}[mode=compact,lane height=30mm,
  heading height=20mm]{tariffs}{2}
  \PPShared{given}{$F=8$ credits\\$q=12$ units}
  \PPCell{model}{1}{A: $r_A=1.5$ credits/unit\\$C_A=8+1.5(12)=26$}
  \PPCell{model}{2}{B: $r_B=2$ credits/unit\\$C_B=8+2(12)=32$}
  \PPCell{cost}{1}{A: 26 credits\\$26-8=18=1.5(12)$}
  \PPCell{cost}{2}{B: 32 credits\\$32-8=24=2(12)$}
  \PPConnect{given-shared}{model-1}{}
  \PPConnect{given-shared}{model-2}{}
  \PPConnect{model-1}{cost-1}{}
  \PPConnect{model-2}{cost-2}{}
\end{PracticeProcedure}
```

For a comparison task, put a `\PPShared` output in a subsequent comparison stage and connect both `cost-1` and `cost-2` into it. Include its explicit conclusion (for these data, A costs 6 credits less than B); do not merge distinct outputs merely for visual symmetry. Shared content replaces lane cells in that stage; do not overlap the two.

## Advanced variants and linked panels

Retain the base family's stage identities, order, lane order and conventions wherever the reasoning is equivalent:

- Additional alternatives add numbered lanes with visible names. In the tariff example, C with rate 2.5 gives $8+2.5(12)=38$ credits in lane 3.
- Extra calculation within a stage becomes an explicitly labelled substep there, e.g. “Usage charge: 18; add fee: 18+8=26”. Keep the same stage ID.
- A new operation becomes `\PPExtension` at the appropriate position. In `tariffs-credit` above, a common 6-credit membership credit gives payable amounts 20, 26 and 32 credits; label that operation and show the subtraction. If the new operation belongs between base stages, declare the extended list with those same base IDs/headings and insert the extension there. Do not append an out-of-order step for coding convenience.
- Branch and rejoin only when the mathematics warrants it. Keep common inputs and unchanged reasoning shared. Use a short meaningful extension label rather than unrelated colors or frame styles.

If a variant genuinely changes the method, declare and introduce another family. Briefly explain how it relates; never conceal the difference or invent steps to force it into the base family.

When a complete diagram is too wide/tall, split at a meaningful stage boundary. Factor its stage declaration into named fragments and compose the complete family and panel families from them. Keep original stage IDs/headings, case order and continuation symbols. For example, the first panel can contain `given` and `model`, and the second `cost` and `credit`; identify the boundary values $C_A,C_B,C_C$ and their units in both the outgoing note and incoming explanation. Explicitly title “Panel 1 of 2 — continues with Cost and check” and “Panel 2 of 2 — continues from $C_i$” so no missing arrow is mistaken for a disconnected method. A second panel's first cell may carry the same boundary value deliberately; that is a continuation, not repeated independent inputs. Never silently omit a stage when splitting.

Keep frames comfortably within the page. Each picture is one box and cannot split across a page; choose a page break before it or split panels if its height approaches usable page height. Do not use tiny fonts, whole-picture `resizebox`/`scalebox`, negative spacing or crowded arrows to repair overflow. Short annotations belong outside frames; substantive reasoning belongs in the written explanation or stage cells.

Optional tables/graphs use `\PPPanel` in the same grid. For example:

```tex
\PPPanel{cost}{1}{\begin{tabular}{@{}lr@{}}
  Units & Cost (credits)\\
  0 & 8\\12 & 26
\end{tabular}}
```

Define graph dependencies in the activity and size axes and labels to local `\linewidth`; do not scale the whole diagram or give graph decorations new semantic colors. A graph needing substantial space belongs beside the written solution or in its own linked panel.

## Coordination and validation

[math-legend-highlight](../../math-legend-highlight/SKILL.md) establishes the shared semantic roles and complementary legends; [math-practice-highlights](../../math-practice-highlights/SKILL.md) applies them to all diagram content and verifies the existing toggle. This asset supplies neutral structure only. Preserve complete symbols and each component's role inside mixed expressions. Highlighted and unhighlighted diagrams must contain exactly the same mathematics, case labels, equations, values, units, notes and connections. Labels, line conventions and extension wording carry meaning independently of color.

Use [update-latex-complete](../../update-latex-complete/SKILL.md) for builds, log review, mathematical checks, every-page rendering, navigation and enabled/disabled/grayscale inspection. Reuse its render helper. When changing this asset or its scaffold integration, compile isolated representative documents with the actual repository preamble and a copied deployment beside a scaffold-based activity. Exercise detailed/compact versions of the same family, two cases sharing inputs, three-case extensions with an added step, a genuinely different family, long headings and multiline mathematics, repeated pictures, tables or graphs when supported, branching/merging, and linked panels. Check stage centers and borders, padding, arrows/labels, formula wrapping, page boundaries and continuation relationships at normal reading size. Fix demonstrated issues and rebuild affected variants. Check that no absolute skill input or undeclared asset search path is required. Never use existing classroom activities as test fixtures for a skill update.
