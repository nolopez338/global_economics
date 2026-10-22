# Compilation verification — 2026-10-22

All six standalone documents passed fresh pdfLaTeX compilation from this
directory with `-interaction=nonstopmode -halt-on-error -file-line-error`.
Build artifacts and logs are in `build/`; final PDFs are beside their sources.
Repeated passes resolved the auxiliary-file and cross-reference warnings.

| Source | Result | Pages | Remaining warnings |
| --- | --- | ---: | --- |
| G10_T2_L1_C1-C5_practice_activity1.tex | PASS | 38 | None |
| G10_T2_L1_C1-C5_practice_activity2.tex | PASS | 23 | None |
| G10_T2_L2_C6C7_practice_acticity.tex | PASS | 13 | Existing array column Y/C redefinitions |
| G10_T2_L3_C8_practice.tex | PASS | 6 | Existing array column Y/C redefinitions |
| G10_T2_L3_C9_practice.tex | PASS | 5 | Existing array column Y/C redefinitions |
| G10_T2_L3_C10_practice.tex | PASS | 4 | Existing array column Y/C redefinitions |

## Changes

- Corrected four preamble paths to `../../../preamble/preamble_exams.tex`.
  Its nested `preamble.tex` resolves through the existing input search paths.
- Added `practice_support.inc` with local title, section, and numbered-problem
  helpers, plus graphics paths to the existing 2025–2026 preamble assets.
  The documents contain no direct image inclusions requiring further repair.
- Started bare problem items explicitly before subsection headings, avoiding
  missing-item and improper-prevdepth errors.
- Added missing criteria link labels in Activity 2 and replaced its trailing
  introductory line break with a paragraph break.
- Split three long probability displays across lines to prevent overflow.
- Preserved educational content, original source filenames, and shared preambles.
  Activity 1 required no source changes.

The remaining `array` warnings originate in the shared preamble, which
redefines Y and C after loading the general preamble. They are nonfatal and
were retained to avoid changing unrelated documents. Final logs contain no
undefined references, missing glyphs, or overfull/underfull box warnings.

All 89 pages were rendered to PNG for a contact-sheet layout review; first
pages were also inspected at a larger scale. Preview images are in `build/`.

## Rebuild (PowerShell, from this directory)

```powershell
New-Item -ItemType Directory -Force build | Out-Null
Get-ChildItem -Filter 'G10*.tex' | ForEach-Object {
    $source = $_
    1..2 | ForEach-Object {
        & pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build $source.Name
        if ($LASTEXITCODE -ne 0) { throw "Compilation failed: $($source.Name)" }
    }
    Copy-Item -LiteralPath (Join-Path build ($source.BaseName + '.pdf')) -Destination ($source.BaseName + '.pdf') -Force
}
```
