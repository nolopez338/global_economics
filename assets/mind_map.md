# Mind-map developer guide

This is the primary README for the shared `assets/js/mind_map*.js` and `assets/css/mind_map*.css` system. It describes reusable presentation code, not lesson content.

## Purpose and architecture

A mind-map page is progressively enhanced from an ordered list inside `[data-mind-map-presentation]`. The **core** creates `window.MindMap` and its feature registry. **Presentation** turns `[data-mind-map-slide]` children into keyboard-accessible regular, presentation, and fullscreen slides. **Effects** supplies a declarative effect registry; highlight and concept-move implementations plug into it. **Criteria** and **pre-transition** are optional presentation lifecycle integrations. **Solution-step** preserves keyboard operation of collapsible `<details>` steps. Probability, payoff, and curriculum-outline CSS provide feature-specific visual systems. **Graph-popout** clones supported graphs into draggable, resizable floating windows while preserving SVG accessibility metadata.

CSS is layered: `mind_map.css` owns the base layout and typography API; a feature visual sheet comes next; behavior sheets follow. JavaScript is layered core → registries/implementations → lifecycle controller → independent enhancements. All scripts are classic scripts and should use `defer`.

## JavaScript module reference

| File | Required? | Responsibility and when to include | Dependencies, hooks, and loading order |
|---|---|---|---|
| `mind_map.js` | Required for registered features | Creates `window.MindMap`, discovers roots, and registers per-root features. Include on every enhanced mind map. | First. Root: `[data-mind-map-presentation]`. |
| `mind_map_presentation.js` | Required for presentation mode | Slide navigation, progress editing, keyboard handling, native fullscreen, focus and criteria/pre-transition lifecycle. | After core and optional effect implementations. Uses `[data-mind-map-presentation]`, `[data-mind-map]`, `[data-mind-map-slide]`, start/previous/next/fullscreen/exit controls, progress hooks, and optional `[data-mind-map-slide-scroll]`. |
| `mind_map_effects.js` | Optional | Parses and runs declarative effect groups and forward/backward transitions. Include only for animated effects. | Before effect implementations and presentation. Uses `data-mind-map-effect-groups` and `data-mind-map-transition-forward/backward` JSON. |
| `mind_map_effect_highlights.js` | Optional | Registers word, element, and clear-highlight effects. | After `mind_map_effects.js`; before presentation. Uses effect JSON plus generated `data-mind-map-effect-word/element` hooks. |
| `mind_map_effect_concept_move.js` | Optional | Registers animated movement between matching source/destination concepts. | After effects registry; before presentation. Uses `data-mind-map-move-source`, `data-mind-map-move-destination`, and optional `data-mind-map-concept`. |
| `mind_map_criteria.js` | Optional marker | Registers the criteria integration extension point; presentation owns dialog behavior. Include when criteria controls are present. | After core, before presentation. Hooks: `.mind-map-criteria` and its criteria data consumed by presentation. |
| `mind_map_pre_transitions.js` | Optional marker | Registers staged pre-transition support; presentation advances stages. | After core, before presentation. Pair with `.mind-map-pre-transition` markup and its presentation data. |
| `mind_map_solution_steps.js` | Optional | Makes `.solution-step > summary` reliably toggle with Enter/Space without leaking the keystroke to slide navigation. | Independent; load after markup (normally deferred, after presentation). Requires native `<details class="solution-step"><summary>…`. |
| `mind_map_graph_popouts.js` | Optional | Adds accessible launchers and draggable/resizable floating clones for density, procedure, and mini graphs. | Independent but expects one presentation root and probability visual CSS. Load after presentation/solution scripts. Selects `figure.density-graph`, `figure.procedure-figure`, and `svg.procedure-mini-graph`; SVG `<title>`/`<desc>` and figure captions provide names. |

Typical order is `mind_map.js`, `mind_map_effects.js` (if used), effect implementations, criteria/pre-transition markers, `mind_map_presentation.js`, then solution-step and graph-popout enhancements. MathJax may load asynchronously; keep the project's `math-render.js` integration before it.

## CSS module reference

| File | Scope | Responsibility, dependencies, and customization |
|---|---|---|
| `mind_map.css` | Shared; required | Base card, timeline, nodes, help, focus state, and all `--mind-map-font-*` defaults. Load first. Customize semantic variables on a presentation root. |
| `mind_map_presentation.css` | Shared behavior | Toolbars, slide isolation, scroll containers, fullscreen controls, responsive and print behavior. Load after visual sheets unless a feature explicitly needs to override it. Consumes presentation JS state classes/attributes. Customize presentation font variables, not internal state selectors. |
| `mind_map_criteria.css` | Feature-specific | Criteria pills and accessible modal/dialog presentation. Load after base when criteria are used; depends on criteria hooks and presentation lifecycle. Customize criteria/dialog variables and theme tokens. |
| `mind_map_pre_transitions.css` | Feature-specific | Overlay used for staged pre-transitions. Load after base with pre-transition JS/markup. Customize the overlay's theme tokens; typography inherits semantic variables. |
| `mind_map_effect_highlights.css` | Feature-specific | Word/element highlight animation registered by highlight JS. Load after base when those effects occur. Customize highlight color data/theme tokens. |
| `mind_map_effect_concept_move.css` | Feature-specific | Runtime concept movers and hidden transition destinations. Load with concept-move JS. Customize movement color/theme tokens rather than geometry state hooks. |
| `mind_map_probability_visuals.css` | Shared feature system | Probability concepts, density/distribution/procedure graphs, solution steps, tables, and graph-popout UI. Load after base and before presentation. Its JS features are solution steps and graph popouts. Customize graph, step, procedure, table, task, and popout variables. |
| `mind_map_payoff_visuals.css` | Shared feature system | Grade 10 payoff, comparison, decision, equation, table, and model visuals. Load after base and before presentation. Customize panel/table/equation variables and existing color tokens. |
| `mind_map_curriculum_outline.css` | Shared feature system | Curriculum-outline grids, captions, decision rules, and presentation sizing. Load after base and before presentation. Customize visual-caption, table, and list variables. |

Recommended order: base project styles → `mind_map.css` → one or more visual feature sheets → effect/criteria/pre-transition sheets → `mind_map_presentation.css` → a small page-root variable override. Do not override runtime classes merely to change text size.

## Centralized font-size variables

Defaults live on `[data-mind-map-presentation]` in `mind_map.css`. `rem` is preferred for ordinary UI text, `clamp()` for viewport-responsive display text, `px` for SVG user-coordinate labels, and `%`/`em` only when a role deliberately scales relative to its parent.

| Variable | Default | Role / main selectors | Normal scope |
|---|---|---|---|
| `--mind-map-font-body` | `1rem` | Root body text | Global |
| `--mind-map-font-intro-eyebrow` | `0.78rem` | `.mind-map-eyebrow` | Global |
| `--mind-map-font-intro-title` | `clamp(1.65rem, 4vw, 2.5rem)` | `.mind-map-intro h2` | Global/page |
| `--mind-map-font-intro-description` | `1rem` | intro description | Global |
| `--mind-map-font-slide-title` | `1.2rem` | node and feature slide `h3` | Global/page |
| `--mind-map-font-step-label` | `0.78rem` | `.mind-map-step-label` | Global |
| `--mind-map-font-step-marker` | `1rem` | timeline numbered marker | Global |
| `--mind-map-font-node-body` | `1rem` | `.mind-map-node` | Global/page |
| `--mind-map-font-section-heading` | `1.05rem` | merged-section `h4` | Global |
| `--mind-map-font-panel-heading` | `0.95rem` | card/panel headings | Global/feature |
| `--mind-map-font-panel-body` | `0.98rem` | card/panel copy | Global/feature |
| `--mind-map-font-list` | `1rem` | node lists, legends, decision rules | Global |
| `--mind-map-font-table-heading` | `0.76rem` | node/procedure table headings | Global/page |
| `--mind-map-font-table-body` | `0.74rem` | node, procedure, payoff, summary tables | Global/page |
| `--mind-map-font-equation` | `1.08rem` | `.equation`, MathJax, payoff formulae | Global/page |
| `--mind-map-font-graph-label` | `13px` | SVG axis/tick/function/point/annotation text and `tspan` | Global/page |
| `--mind-map-font-graph-title` | `13px` | visible `.graph-title` text | Global/page |
| `--mind-map-font-graph-caption` | `0.78rem` | density/distribution/procedure captions | Global/page |
| `--mind-map-font-mini-graph-label` | `13px` | procedure mini-graph text and `tspan` | Global/page |
| `--mind-map-font-solution-step` | `clamp(0.75rem, 1.05vw, 0.88rem)` | `.solution-step` explanatory text | Global/page |
| `--mind-map-font-solution-step-heading` | `0.82rem` | solution-step `h4` | Global/page |
| `--mind-map-font-solution-step-number` | `0.72rem` | `.step-number` circle | Global/page |
| `--mind-map-font-solution-step-equation` | `92%` | MathJax inside a step | Global/page |
| `--mind-map-font-procedure-heading` | `0.78rem` | procedure-card `h5` | Global/page |
| `--mind-map-font-procedure-body` | `0.72rem` | procedure-card body | Global/page |
| `--mind-map-font-task` | `0.88rem` | task boxes, key ideas, concept keys | Global/page |
| `--mind-map-font-presentation-control` | `1rem` | presentation buttons | Global |
| `--mind-map-font-progress-counter` | `clamp(0.9rem, 1.5vw, 1.05rem)` | toolbar/fullscreen progress | Global |
| `--mind-map-font-criteria-control` | `0.78rem` | criteria pills/controls | Global |
| `--mind-map-font-dialog` | `clamp(1.05rem, 2.2vw, 1.6rem)` | dialog/modal copy | Global |
| `--mind-map-font-dialog-title` | `clamp(1.5rem, 4vw, 2.75rem)` | dialog/modal title | Global |
| `--mind-map-font-dialog-control` | `1.5rem` | dialog close control | Global |
| `--mind-map-font-dialog-title-print` | `1rem` | printed inline dialog title | Global |
| `--mind-map-font-dialog-print` | `0.95rem` | printed inline dialog copy | Global |
| `--mind-map-font-graph-popout-launcher` | `0.7rem` | popout launcher/placeholder | Global/page |
| `--mind-map-font-graph-popout-title` | `0.8rem` | floating graph title | Global/page |
| `--mind-map-font-graph-popout-control` | `1.25rem` | floating graph controls/icons | Global/page |
| `--mind-map-font-help` | `0.9rem` | help, notes, instructional text | Global |
| `--mind-map-font-visual-caption` | `0.82rem` | non-graph visual caption/legend | Global |
| `--mind-map-font-badge` | `0.82rem` | compact metadata badges | Global |
| `--mind-map-font-icon` | `1.35rem` | semantic decorative icons | Global |
| `--mind-map-font-feature-symbol` | `2rem` | large visual symbols | Feature/page |
| `--mind-map-font-feature-value` | `1.7rem` | emphasized visual values | Feature/page |
| `--mind-map-font-inline-emphasis` | `1.1em` | inline sample-space emphasis | Feature/page |
| `--mind-map-font-page-heading-mobile` | `clamp(1.75rem, 9vw, 2.5rem)` | presentation-adjacent mobile page heading | Global |
| `--mind-map-font-presentation-body` | `clamp(1.15rem, 2.2vw, 1.75rem)` | node body while presenting | Global/page |
| `--mind-map-font-presentation-title` | `clamp(1.8rem, 4.5vw, 3.8rem)` | slide title while presenting | Global/page |
| `--mind-map-font-presentation-section-heading` | `clamp(1.25rem, 2.6vw, 2rem)` | section heading while presenting | Global/page |
| `--mind-map-font-presentation-label` | `clamp(0.9rem, 1.6vw, 1.15rem)` | step/criteria labels while presenting | Global/page |

## Developer customization examples

```css
/* Graph text only */
.my-lesson { --mind-map-font-graph-label: 16px; --mind-map-font-graph-title: 17px; --mind-map-font-graph-caption: 1rem; --mind-map-font-mini-graph-label: 14px; }
```

```css
/* Solution steps only */
.my-lesson { --mind-map-font-solution-step: 1rem; --mind-map-font-solution-step-heading: 1.05rem; --mind-map-font-solution-step-number: .9rem; --mind-map-font-solution-step-equation: 105%; }
```

```css
/* All primary reading text */
.my-lesson { --mind-map-font-body: 1.1rem; --mind-map-font-node-body: 1.1rem; --mind-map-font-list: 1.1rem; --mind-map-font-panel-body: 1.1rem; --mind-map-font-presentation-body: 1.35rem; }
```

Scope overrides by adding a unique class to the presentation root—never `body`—so other lessons retain shared defaults:

```html
<section class="my-lesson" data-mind-map-presentation>…</section>
```
```css
.my-lesson { --mind-map-font-graph-label: clamp(14px, 1.5vw, 18px); }
```

To restore a shared default, remove the override. During temporary experiments, explicitly copy the default from the table, or use `--mind-map-font-graph-label: revert;` only when an ancestor does not also redefine it.

## Adding a new text role

1. Name the semantic role `--mind-map-font-<role>`; do not name it after one lesson or a numeric size.
2. Define a sensible default once in the typography API at the top of `mind_map.css`.
3. Map every equivalent selector—including responsive, `!important`, SVG `text`/`tspan`, cloned popout, and MathJax variants—to that property.
4. Preserve responsive behavior by storing `clamp()` in the property rather than repeating it in selectors.
5. Add the variable, default, selectors, units, and expected scope to the table above.
6. Search all `mind_map*.css` and affected inline SVG for unexplained hardcoded sizes. Inline SVG text should use semantic classes; avoid `font-size` attributes.

## Testing checklist

- [ ] Regular page view retains timeline layout and readable text.
- [ ] Presentation mode navigation, focus, scrolling, and progress work.
- [ ] Native fullscreen keeps every slide reachable.
- [ ] Narrow/mobile viewports have no horizontal page scrolling.
- [ ] Light and dark themes retain contrast.
- [ ] MathJax equations wrap or scroll inside their containers and do not clip.
- [ ] SVG axis, tick, function, point, annotation, title, and `tspan` text is readable and does not overlap or clip.
- [ ] Mini and procedure graphs remain legible.
- [ ] Floating graph popouts inherit graph variables; controls do not overlap titles.
- [ ] Expanded and collapsed solution steps work by pointer and keyboard.
- [ ] Enlarged text wraps without clipping, overflow, or toolbar/control overlap.
