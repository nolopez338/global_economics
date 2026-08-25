# Mind-map module inventory

All scripts are deferred classic scripts and load in this order: `mind_map.js`, optional `mind_map_effects.js`, effect implementations, optional criteria/pre-transition integrations, and `mind_map_presentation.js`. CSS starts with `mind_map.css`, followed by only the visual and behavior styles used by the page.

| Page | Presentation | Criteria | Effects | Pre-transition | Visual system | MathJax |
|---|---:|---:|---|---:|---|---:|
| `assets/html/mind_map.html` | yes | yes | word highlight | no | none | yes |
| `assets/html/curriculum_outline.html` | yes | no | none | no | curriculum outline | yes |
| `grade10/src/G10_curriculum_outline.html` | yes | no | none | no | curriculum outline | no |
| `grade11/src/G11_curriculum_outline.html` | yes | no | none | no | curriculum outline | no |
| `grade10/src/pages/term1/g10-t1-c1c2c3-intro1.html` | yes | no | word/element/clear highlight; concept move | no | payoff/decision | yes |
| `grade10/src/pages/term1/g10-t1-c1c2c3-intro2.html` | yes | no | element highlight | yes | payoff/decision | yes |
| `grade10/src/pages/term1/g10-t1-introduction.html` | yes | yes | none | no | payoff/decision | no |
| `grade11/src/pages/term1/g11-t1-c1-intro.html` | yes | no | none | no | probability | yes |
| `grade11/src/pages/term1/g11-t1-c2-intro.html` | yes | no | none | no | probability | yes |
| `grade11/src/pages/term1/g11-t1-c2-intro2.html` | yes | no | none | no | probability plus graph popouts | yes |

The exact imports are declared in each page head. `g10_payoff_intro.css` remains as a two-line compatibility shim for external links; repository pages use `mind_map_payoff_visuals.css` directly.
