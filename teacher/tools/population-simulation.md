# Two independent population and sample lessons

- `general_fundamentals/population_sample_simulation.html`: public simulation only; opens without a password, uses independent untruncated Normal(μ, σ) draws and unique `Generated N` labels, and loads no survey or student data. Restored from Git commit `b55a1838`, with generated labels and an explicitly artificial context. Apply changes the model while preserving observation identities and selection configurations; Reset restores μ = 170 cm, σ = 8 cm, 95% confidence, and an empty collection. Negative draws are mathematically possible under the untruncated teaching model. The interval targets the generating mean using known σ, rather than a national mean or the displayed collection mean.
- `general_fundamentals/population_sample_simulation_restricted.html`: school survey lesson, retaining its password gate, actual observations, step-1 names, filters, fitting, and generated extensions. Details follow below.

Both pages open directly as local files or through static hosting from the repository root (for example, `python -m http.server 8000`). Grade 11 Term 2/3 “Open Interactive Simulation” links describe general estimation and intentionally continue to open the public simulation.

Simulation verification: `node --test --test-isolation=none teacher/tools/population-simulation-only.test.cjs` and `node teacher/tools/population-simulation-only.browser.cjs`. The browser suite checks local-file and HTTP loading, request isolation, keyboard controls, focus, Reset, parameter changes, sampling, confidence intervals, studies, and desktop/narrow layouts. Browser screenshots are saved under `tmp/population-verification/simulation-*`.

## Survey population and sample lesson

Open `general_fundamentals/population_sample_simulation_restricted.html` directly or through static hosting. The page initially loads only `assets/js/population-lesson-gate.js`. After a correct password it loads `assets/data/survey_data_extended.js`, `assets/js/survey-simulation-core.js`, and `assets/js/population-simulation.js`, in that order, then opens and initializes the lesson. It needs no XLSX parser, network service, or new runtime dependency.

## Classroom password gate and security boundary

Enter the exact password `321654` with the Enter button or Enter key. Every open or reload requires entry again; successful authentication is never persisted. The lesson container starts hidden, and no survey data or application initialization runs until entry succeeds. Focus starts on the labeled password field, returns there after a wrong entry, and moves to the lesson heading after opening. Feedback is a live status message.

Incorrect submissions accumulate in localStorage under `population-lesson-password-failures` for this browser profile and origin (or browser-defined local-file storage scope). Before five failures, the form reports remaining attempts. The fifth failure disables the form and persistently displays “Access blocked after five incorrect attempts.” Reloading or reopening the page retains failures and lockout. A correct entry before lockout resets failures to zero. Reset simulation only resets lesson state and never reads or changes gate storage. The gate checks storage reads and writes; unavailable, unwritable, or invalid persistent storage keeps access closed with an explanation. Direct local-file use works where the browser permits the necessary storage. Closing a private-browsing profile may discard its storage according to browser policy.

**This is a client-side classroom gate, not secure authentication or protection for personal data.** The hardcoded password is inspectable. Browser lockout can be bypassed by changing/clearing storage or using another browser profile. The downloadable JavaScript contains student names and remains accessible independently of the gate. Genuine protection requires server-side authentication and authorization for the data files themselves. Static hosting and a browser password form cannot provide that protection.

## Regeneration

From the repository root:

```powershell
node teacher/tools/export-survey-simulation.cjs
```

The converter uses the repository's pinned SheetJS and existing survey parser. It does not write the workbook. The export includes its SHA-256 fingerprint, reference date, derivation assumptions, field classifications, answer statuses, and derived issue summaries. The current workbook contains 206 questionnaire rows; questionnaire IDs, rather than incompletely populated student IDs, are the unique source keys. Schema version 2 includes `student_name`, joined to each exported record exclusively by `questionnaire_id`. Names come from `Clean answers`; blank or unavailable names become null. Student identification numbers, identity audit rows, and free text remain excluded. Actual observation labels, the inspector, and pointer tooltips use names only in step 1, falling back to anonymous questionnaire labels. Steps 2–4 retain anonymous labels. Synthetic observations always use clearly generated labels and never inherit a name. Names use canvas text and DOM `textContent`; accents are preserved and markup is never interpreted. The serializer escapes `<` as an additional precaution.

`Clean answers` cells and actual headers override the dictionary's obsolete blank-template introduction. Units and allowed meanings come from dictionary field rows, checked against the derivation formulas and stored values. Stored fractions remain fractions. Derived fields remain dated workbook snapshots (currently November 1, 2026); estimates are explicitly distinguished from source responses and exact derivations. No age is recomputed using today's date.

The export preserves one row per questionnaire, including rows without a usable selected variable. Blanks, unavailable answer statuses, invalid numerical domains, and zero-denominator ratios become null. Valid zeros and full stored numerical precision remain intact. Answer statuses on derived numerical fields describe their source dependencies; a derived value is not relabeled as directly observed. Scores, identifiers, ranks, flags, cyclical date codes, dates, and text remain unsupported in the simulation selector regardless of numeric storage. Numeric selectors include continuous quantities and actual counts, with explicit integer status and domains. The count model is an approximation, not a claim that counts are Gaussian.

## Reveal and filters

Grade and group options come from exported rows. All grades + A includes both 10A and 11A. Matching counts include every questionnaire; usable counts exclude only unavailable values for the selected field. Each selection fits all usable actual values, creates a deterministic seeded Fisher–Yates queue keyed by field/grade/group, and clears the collection, selections, histogram state, studies, and tooltip. Reset repeats this sequence for the current selection and retains panel positioning/visibility and confidence preference. Revealing retains equal values from different questionnaire IDs. A batch reveals every remaining actual record first, then generates precisely its remainder. The introduction still presents 20 observations, extending small actual queues with labeled generated values as needed. Empty queues disable additions and cannot generate.

Drawing samples and independent studies never consume or shuffle the reveal queue. Random samples select displayed observation IDs uniformly without replacement; independent studies draw fresh values from the fitted generator and leave the collection and fit untouched. Studies clear when the model, sample size, or confidence changes.

## Fitting and generation

The single Gaussian uses maximum-likelihood variance (denominator n). Two-component EM is considered only at n ≥ 30. Five deterministic quantile initializations use pairs (0.2,0.8), (0.3,0.7), (0.1,0.6), (0.4,0.9), and (0.15,0.85). EM uses log-sum-exp responsibilities, a 400-iteration limit, and relative log-likelihood tolerance `1e-8 × (1 + |log likelihood|)`. Fits with decreasing likelihood, nonconvergence, component expected counts below `max(5, 0.05n)`, or variances at/below `max(1e-4 × overall variance, (32ε|mean|)²)` are rejected. BIC uses 2 parameters for one Gaussian and 5 for a mixture; a valid mixture must improve BIC by **more than 6**. Otherwise the single Gaussian wins. A mixture is labeled “two-component normal mixture”; no bimodality is asserted.

For a mixture, μ = Σwₖμₖ and σ² = Σwₖ[σₖ² + (μₖ − μ)²]. The fit summary separates these underlying moments from transformed generator moments and the displayed collection's empirical mean. Synthetic values choose a component by its weight and use independent Box–Muller draws. They never enter a refit. Singletons and constants use exactly their recorded value with zero variation; empty selections have no generator.

Continuous draws outside a variable's valid domain are rejected, not clamped. Positive measurements reject zero. Continuous precision remains unquantized because the questionnaire permits decimals; displayed rounding does not alter recorded values. Counts reject outside half-integer limits, then round to the nearest integer. Rejection applies to the full mixture, so component proportions may change after truncation. Generator moments use truncated-normal integrals for continuous fields and CDF cell probabilities for integer fields; integer sums cover ±10 component standard deviations, with negligible omitted tail mass. The normal CDF uses a numerical approximation (about 1e-7 absolute error). These resulting moments supply the plug-in z-interval, rather than silently using the pre-transformation moments.

The interval is a model-based approximation for the fitted generator mean, not an interval establishing a national mean or claiming truly known population σ. It ignores survey-selection and fitting uncertainty; small-n and nonnormal-mixture nominal coverage can differ substantially. At zero variance the interval collapses and nominal normal coverage is explicitly marked inapplicable. Independent studies illustrate generator coverage only.

## Verification

```powershell
node --test --test-isolation=none teacher/tools/population-simulation.test.cjs
node teacher/tools/population-simulation.browser.cjs
```

The second command needs development-time Playwright and installed Edge (neither is a page dependency). If Playwright is supplied outside the repository, set `NODE_PATH` to its package directory. Core checks compare the export against the source workbook, including every retained cell, name-to-questionnaire reconciliation, reordered rows, missing/hostile names, student-ID exclusions, nulls/zeros, every numerical variable across grade/group combinations, seeded reveal order and batch exhaustion, small/constant fallbacks, deterministic EM, and simulated moments (80,000 seeded draws per representative variable).

Browser checks cover exact password matching, button/Enter submission, remaining-attempt feedback, fifth-attempt lockout, reload/reopen persistence, success resetting failures, fresh authentication on reload, unavailable storage, deferred data loading/initialization, gate focus and keyboard access, real-name tooltips, missing-name fallback, text injection safety, synthetic and later-step anonymity, and direct `file://` loading, all four lesson steps, the introduction and +1/+10/+100/+1000, exhaustion messages, stacked histogram provenance and interactions, keyboard/pointer window changes, random sampling, inspector and keyboard access, calculations, studies and clearing, filter/reset invalidation, edge-case fixtures, Options focus and positioning, and 1440/390/320-pixel gate and lesson layouts. Screenshots under `tmp/population-verification` support visual review; console errors fail the check. Source and selection remain independently encoded: teal/orange fills with blue selection rings, plus textual provenance in the inspector, tooltips, and bin counts.
