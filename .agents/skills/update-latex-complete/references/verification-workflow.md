# Complete LaTeX verification workflow

Follow these steps in order. Use the actual document and available tools; examples below are mechanics, not requirements to use a particular engine or dependency. Keep temporary builds, logs, and page images separate from delivery files.

## 1. Establish the source and impact

- Read the target and dependencies involved in the change. Identify the root `.tex`, included files, current build command/engine, bibliography/index tools if used, fonts, graph macros, and external assets. Resolve paths from the established working directory.
- Identify whether the change is local or affects a shared preamble, renderer, registry entry, or graph helper. Find affected consumers of shared behavior; include those outputs in verification. Do not compile the entire repository for a local edit. When a shared change has too many consumers to verify, narrow the implementation when practical or explicitly report coverage limits.
- Record relevant invariants: content to preserve, navigation, numbering, required structure, score totals, highlight/solution toggles, slide overlays, and intended page format. Derive these from the user and actual document rules, never an unrelated activity.

## 2. Implement and review the source change

- Make the requested edit, preserving unrelated work. Review the scoped diff for accidental deletions, changed givens, duplicate definitions, stale references, and unwanted template changes.
- Check relevant mathematics independently: formulas, substitutions, rounding, units, domains, probability totals, table values, graph coordinates, and contextual interpretations. Recheck dependent worked solutions and totals when inputs change. Do not insert private solutions into student tasks.
- Confirm affected headings, labels, links, criteria, task instructions, and table columns agree. Verify required exercise counts or assessment allocations only when applicable to this document. This content review is task-specific and must not become hard-coded validation defaults.

## 3. Build reproducibly in isolation

- Create a fresh temporary build directory under the workspace's `tmp/` or the system temporary directory. Run the established engine from the source directory so relative inputs continue to resolve. Use a directory distinct from concurrent builds. Do not run recursive `compile_all_tex.bat` or cleanup scripts for a single document.
- For a pdfLaTeX target, typical PowerShell mechanics are:

  ```powershell
  # Set these to the identified source and a fresh absolute build directory.
  Push-Location -LiteralPath $sourceDirectory
  try {
      latexmk -pdf -interaction=nonstopmode -halt-on-error "-outdir=$buildDirectory" $sourceFilename
      if ($LASTEXITCODE -ne 0) { throw 'LaTeX build failed; inspect the build log.' }
  } finally {
      Pop-Location
  }
  ```

- Use the established LuaLaTeX/XeLaTeX command instead when needed. If `latexmk` is unavailable, invoke the engine and required bibliography/index tools directly, with outputs in the build directory. Run enough passes to settle references, contents, and frame totals; normally at least two for a fresh build.
- Preserve input conventions. If a target genuinely needs `TEXINPUTS`, scope it to the build session and restore its previous value afterward. On Windows, use semicolon-separated paths and retain the empty component for default TeX search paths. Do not rewrite relative inputs to machine-specific absolute paths.
- Inspect exit status and the actual log even if a PDF exists. Stop a non-converging rerun loop, diagnose the cause, and report it if unresolved. Never keep rerunning an identical failure without a new remedy.

## 4. Resolve diagnostics

Read the final log and relevant tool outputs for:

- LaTeX/package errors, missing inputs, missing fonts/glyphs, and failed external tools;
- undefined citations/references, duplicate labels or destinations, unresolved rerun requests, and incorrect frame totals;
- overfull horizontal/vertical boxes, clipped material, float problems, and underfull boxes where they indicate poor typography.

Repair errors and relevant layout warnings. Inspect the actual location rather than suppressing warnings with `\hfuzz`, hidden diagnostics, or blanket spacing changes. A warning-free log still requires visual inspection. Record intentional, harmless residual warnings and their inspected locations.

## 5. Render and inspect every page

- Render the newly built PDF with an available local renderer. With Poppler, for example:

  ```powershell
  pdftoppm -r 140 -png $builtPdf $renderPrefix
  if ($LASTEXITCODE -ne 0) { throw 'PDF rendering failed.' }
  ```

- Open and visually inspect rendered images of **every page**, including all physical overlay pages in Beamer. Contact sheets can help overview and navigation, but inspect dense or suspect regions at sufficient resolution to read their smallest text. Text extraction, bounding boxes, or script reports do not replace looking at the images.
- Check that text, equations, tables, graphs, highlights, logos, and figures stay within intended columns and page/frame bounds. Look for overlap between elements and with headers/footers, clipping, cropped glyphs, hidden labels, cut-off axes, excessive whitespace caused by broken layout, and unreadably small type.
- Check local table widths including rules and padding, wrapping, row heights, long-cell continuation, repeated headers, baseline alignment, and formulas. Inside columns/minipages, size to local `\linewidth`; include the inter-column gap in the width budget.
- Check graph ticks, units, scales, legends, plotted features, and diagram labels against calculations. Check that table/figure placement supports the associated explanation.
- For handouts, inspect page/column breaks, orphan headings, split problems, student workspace, solution separation, and the first/last page. Preserve readable type and intended margins; split or reflow oversized content before reducing font size.
- For Beamer, inspect question-before-answer timing and first/intermediate/final states, stable table rules and cell geometry, reserved equation/diagram space, title/footer fit, and logical frame numbering across physical PDF pages. Extractable hidden text does not prove visible answer exposure; inspect actual renders.

## 6. Verify navigation and relevant variants

- Inspect contents entries, problem lists, task-to-solution links, return arrows, and example/legend links where present. Follow each affected link and verify its destination, plus each navigation pattern used by the document. Inspect PDF destinations/annotations with available tooling when useful; source labels and clean logs alone do not establish correct link behavior.
- If highlight styling, legends, graph styling, or their renderer changed, build isolated enabled/disabled variants. Verify all text, full notation, values, graph data, and labels remain with highlights off, and inspect a grayscale rendering for legibility. Preserve the delivered toggle setting.
- If solution visibility changed, build relevant student/teacher variants in isolation. Verify student pages do not expose independent answers and optional solutions match task numbers and start where intended. Do not generate unrequested variants as deliverables.
- For intentional standalone slides or other portable output, build an isolated delivery copy without relying on undeclared repository inputs. Preserve an ordinary handout's intentional shared dependencies.

## 7. Repair, repeat, and publish the matching output

- Fix discovered issues and rebuild. Recheck calculations, links, variants, and consumers implicated by the fix. Re-render the final PDF and inspect every final page; pagination or overlay changes can affect pages beyond the edited region. Repeat until relevant checks pass or a concrete blocker prevents completion.
- Persist new reusable validation code/process using the self-updating workflow in [the skill](../SKILL.md). Reuse the library on subsequent tasks; keep document-specific expected content out of it.
- Copy the successfully built and inspected PDF to the established destination beside the source unless the user specifies otherwise. Deliver only the PDF corresponding to the final source; if source changes after inspection, rebuild and inspect again before replacing the deliverable.
- Leave unrelated files and user artifacts alone. Keep inspection images and auxiliaries out of delivery folders; remove temporary files only when needed, only within the verified task-owned temporary directory.
- Report what was actually checked and remaining limits. If compiler, renderer, viewer, dependency, or link tooling is unavailable, complete feasible steps, identify precise unperformed checks, and do not claim full verification or reuse an old PDF as current.
