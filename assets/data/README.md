# Raw survey transcription: first batch

Cleaning has **NOT** been performed. This batch covers **questions 1–18 only** from `assets/data/pdf/Encuesta-10A.pdf`. No other PDF, filtered dataset, or populated clean template was produced.

## Files and sources

- `survey_raw_data.xlsx`: full-template raw database. `Questionnaires` contains one row per questionnaire, `Data dictionary` describes all fields, and `Instructions` explains the transcription stage. All 169 original template columns remain in their original order, followed by 11 provenance/transcription columns. Fictional example records and unused template rows are excluded.
- `transcription_manifest.csv`: UTF-8 CSV with one row per questionnaire, stable key, PDF pages, workbook sheet/row, completion status, and outstanding scan-reading uncertainties. Row numbers locate the present workbook and must be refreshed after sorting or adding records; IDs remain stable.
- `README.md`: scope, conventions, uncertainty index, and handoff instructions.
- Source scan: `assets/data/pdf/Encuesta-10A.pdf`.
- Reference question wording, requested units, and option order: `book2026-2027/fundamentals/G10_T1_survey.tex`.
- Full source template: `outputs/survey_template/Global_Economics_Survey_Database.xlsx`.

The original PDF and template were preserved. Their SHA-256 values were checked before and after authoring:

| Source | SHA-256 |
| --- | --- |
| `Encuesta-10A.pdf` | `9f2077a2e534d28d41d7fccf071115dc870689b1f5395e099c7614f2664d04af` |
| Full database template | `aa866b5de7a9b8804ca48c0f3fc376967b79e4c052d8503bc145a51d5cf96ecb` |

## Coverage and questionnaire boundaries

There are **17 questionnaires covering all 17 PDF pages**, with no omitted or repeated pages. All pages were visually inspected, including enlarged crops of uncertain entries. Each page has a separate student header and the complete Q1–Q18 layout; no questionnaire continuation pages occur in this PDF. Thus questionnaire sequence 1–17 corresponds to page 1–17 **in this batch only**. Do not extend this assumption to future PDFs. Q19–Q21 were excluded.

Windows OCR was run on all 17 page images as an aid. It recovered mainly printed text and was unreliable for handwriting. Original-response transcription is based on visual inspection, including dates, units, colored marks, cancellations, and faint entries. Unresolved readings remain explicitly flagged; “Completed” means the page was inspected and transcribed, not that every answer was legible or usable.

## Stable IDs and reruns

IDs are `Encuesta-10A-0001` through `Encuesta-10A-0017`, assigned by questionnaire order in the source PDF. The stable natural key is **(`source_pdf`, `questionnaire_sequence`)**, not student name, workbook row, or PDF page alone. A student can have multiple questionnaires.

When rerunning this batch, update records matching that key rather than appending them. Preserve existing records for other sources. The batch was rebuilt twice during verification and remained at 17 unique records. Future batches must first establish their own questionnaire boundaries, then use their PDF basename and questionnaire sequence. Expand the table, copy the template diagnostic/validation patterns, extend duplicate-ID formula bounds, and regenerate manifest row references. Do not renumber this batch when adding another PDF. If a source PDF is replaced or reordered, reconcile it against its prior manifest before changing any identity.

## Original-response conventions

- All original-response values are stored as text. Leading zeros, ranges, decimal punctuation, words, units, approximations, and incomplete responses remain as observed. No midpoint, unit conversion, number-word conversion, date repair, or missing-answer inference was performed.
- A truly blank answer remains an empty cell and has `Missing` status. A written zero remains the text `0`. Blank ranking option cells mean no visible option mark and are not individually treated as missing answers.
- `[illegible]` retains an unreadable portion alongside readable handwriting. Bracketed descriptions such as `[crossed out: illegible]`, `[scribbled-out mark: illegible]`, `[dot]`, `[pink]`, and `[left of box]` describe visible features; they are editorial annotations, not student words. Obscured cancelled content is not guessed. A readable replacement and an unreadable prior mark are both retained.
- Q1 year, month, and day are separate original fields. No validated Excel birth date was created.
- Every Q16–Q18 option has its own original mark field. Numerals, ticks, filled marks, colors, and nearby written numbers are preserved with their option associations. Multiple visible mark layers are recorded together, without choosing which layer governs.
- Page 11 has a legend consisting of purple square + `1`, yellow/orange square + `2`, and pink/magenta square + `3`. Its observed appearance is preserved in `q16_legend_original` and referenced in Q17/Q18 legend fields. The colored option X marks remain color descriptions. **The legend was not decoded into numeric ranks.** No other separate handwritten legend was observed; those legend fields remain blank.
- `source_grade_original` preserves the complete handwritten Grade line, including the date-like entry on page 10. Clear grade/section components are recorded separately. Pages **5, 10, and 11** use grade 10 and section A inferred from the filename, explicitly labelled in both provenance columns and general notes. Page 6 retains its written lowercase section `a`.

## Preliminary statuses and expected template warnings

Every questionnaire has a preliminary status for each of Q1–Q18: 306 statuses in total.

| Status | Transcription-stage meaning |
| --- | --- |
| `Valid` | Legible response without an apparent response-format problem. This is a preliminary assessment, not a cleaned or independently validated value. |
| `Missing` | No visible answer. Blank original remains blank. |
| `Ambiguous` | Reading, units/text, range, approximation, incomplete ranking, or conflicting/overlapping marks require later interpretation. The issue describes the observation without resolving it. |
| `Invalid` | Reserved for a definite hard-rule violation; none assigned in this batch. |
| `Corrected` | Not used during transcription. |
| `Not applicable` | Not inferred from blank or unclear phone answers; none assigned in this batch. |

The current counts are **251 Valid, 51 Ambiguous, and 4 Missing**. ALL validated/corrected answer fields and ALL correction-explanation fields are empty, including for `Valid` answers. The instructions and status dictionary clarify this stage-specific meaning of Valid.

The template's diagnostic formulas are retained. `Validated answer missing` and `Unresolved` are **expected** because cleaning is deferred. Original ranking checks can flag colored, symbolic, compound, or nonnumeric marks. These warnings do not authorize filling a validated value. No values were supplied merely to clear a check. The optional plausibility diagnostics read validated values and therefore do not establish that these raw answers are plausible.

## Known uncertainties and observed response problems

The manifest and `outstanding_scan_reading_uncertainties` identify unresolved scan readings; per-question issue descriptions provide the details. IDs below use the final four digits and correspond to source pages in this batch.

| Questionnaire suffix / page | Reading uncertainty or notable observed problem |
| --- | --- |
| 0001 / 1 | Q6 has only an isolated ink dot, possibly stray. Q8, Q11, Q12 and Q13 are blank. Q14 says `1 month`; Q16 only has rank 1. |
| 0002 / 2 | Both surnames are partly illegible in faint pencil. Units are included in several numerical responses; Q8 says `1h` although minutes were requested. |
| 0003 / 3 | Height is `1.69` without a unit; intended unit remains unresolved. |
| 0004 / 4 | Q16/Q17 black numerals overlap pink check marks. Both layers are preserved; precedence/cancellation is unresolved. |
| 0005 / 5 | Q1 year contains only `20`. Crossed-out content in Q10/Q16/Q17 is obscured. Height literally says `1.60cm`. Grade line blank. |
| 0006 / 6 | Q1 birth year visibly says `2026`; retained despite being unusual for grade 10. Q2 has a faint `0` beside `3`, with uncertain cancellation. |
| 0007 / 7 | Unit-bearing commute response preserved; no unresolved scan reading recorded. |
| 0008 / 8 | Ticks plus numbers outside boxes. Five Q17 boxes and six Q18 boxes are ticked; all marks retained. |
| 0009 / 9 | Final surname partly illegible. Q4 `20-30min`, Q5 `7-6`, Q6 `2-3` preserved. Q16 Other is marked but its specification line is blank. |
| 0010 / 10 | Grade line reads `8/14TH/2026`, with TH superscript. Q6 has readable `1h` plus faint/erased illegible marks. Q16 lacks rank 3. |
| 0011 / 11 | Colored X marks and legend retained, without decoding. Hue descriptions remain purple, yellow/orange, and pink/magenta. Grade line blank. Q8 `1hours` and Q14 `1 month` retain their units. |
| 0012 / 12 | Final surname partly illegible; readable portions retained. |
| 0013 / 13 | Dark filled marks in Q16 Arts and Q17 Video games obscure earlier content. Cancellation is uncertain; each question retains four visibly marked options. Other text is preserved as `psicology`. |
| 0014 / 14 | Books response `~80` is approximate. Q18 only has Combination marked 1. |
| 0015 / 15 | Middle surname partly illegible. Q17 Movies has overwritten readable 3. Height `1.74` has no unit. |
| 0016 / 16 | Obscured crossed-out content in Q2 and Q6 retained alongside readable `1` and `2.5`. |
| 0017 / 17 | Crossed-out content in Q1 year, Q4 and Q10 is illegible; readable adjacent replacements retained. Height `1.67` has no unit. |

## Handoff to the cleaning conversation

Provide these three output files, the original `Encuesta-10A.pdf`, the reference `.tex`, and the full database template. Use the manifest to navigate to the scan and workbook record. Start with scan-reading uncertainties and metadata provenance; resolve them only using adequate evidence. Preserve all original-response fields, IDs, source keys, and observed mark/color associations.

The separate conversation may decide normalization, validity, ranking interpretation, and evidence-based corrections, then populate validated fields and correction explanations according to its authorization. It must document those decisions and retain these raw originals. If a clean/filter-only template is used later, `outputs/survey_template/Global_Economics_Clean_Data_Mining_Template.xlsx` is an existing reference file, **not populated by this transcription batch**. No filtering or cleaning should be inferred from the preliminary statuses here.

Verification covered 17 unique source keys/IDs, pages 1–17 exactly once, 17 manifest rows matching workbook rows 2–18, all 306 question statuses, preservation of every original template question column, empty validated/correction fields, no fictional records, a bounded 17-record Excel table, formula error scanning, rendered workbook views, and unchanged source hashes. Native Excel/Google Sheets interactive behavior was not separately tested.

## Second transcription batch: Grade 10B

**Grade 10B has been transcribed but not cleaned.** This section extends the first-batch documentation above; its 17-record counts, page-specific examples and cleaning status describe Grade 10A. All Grade 10A original values, statuses, notes, validated/correction fields and diagnostic formulas remain unchanged.

### Coverage and reconciliation

- Source: `assets/data/pdf/Encuesta-10B.pdf`, **22 original PDF pages**.
- **22 questionnaires**, one independent questionnaire on every page under the fixed **one-page-one-questionnaire** assumption. Exact coverage: **pages 1–22 inclusive**, each visually inspected in full. Enlarged crops were used for difficult handwriting and overwritten answers. Transcription was visual; no unverified OCR output was accepted.
- Page N corresponds to `Encuesta-10B-NNNN`, with four-digit zero padding: page 1 = `Encuesta-10B-0001`, page 22 = `Encuesta-10B-0022`. No pages were merged, split, skipped or renumbered.
- No blank, wholly unreadable or non-questionnaire pages were found. All 22 contain the Q1–Q18 form and responses. Incomplete identity/date fields and incomplete or nonstandard rankings are documented below and in the workbook.
- Workbook: `Questionnaires` rows **19–40**, exactly one Grade 10B row per original page. Manifest: **22 Grade 10B entries**, one per source page, with matching row references.
- Updated database totals: **39 questionnaires = 17 Grade 10A + 22 Grade 10B**. There are no other source batches, fictional examples or unused template rows in these counts. The full 180-column layout and three worksheet names/order are retained; the record table is `A1:FX40`.
- All **396 Grade 10B Q1–Q18 preliminary statuses** are present: **292 Valid and 104 Ambiguous**. No Corrected statuses are used. Valid is the existing preliminary transcription assessment, not evidence of cleaning. Ambiguous describes ranges, text/units, overwritten material, incomplete/extra rankings or uncertain marks without resolving them.

### Metadata exceptions and reading uncertainties

- Page 3: only grade `10` is written; group B is inferred from the filename and explicitly labelled.
- Page 10: name and Grade lines are blank. Student name remains blank; grade 10 and group B are filename-inferred and labelled. Questionnaire ID remains `Encuesta-10B-0010`.
- Page 12: birth year/day include illegible cancellations; only `10` below the year box and `01` above the day box are retained, without reconstructing a birth date.
- Page 15: the Grade line says `14-08-09`; it is retained in `source_grade_original`. Grade 10 and group B are filename-inferred and labelled.
- Page 16: the Grade line says `9°b`, conflicting with the Grade 10B filename. The written grade `9` and lowercase group `b` are retained with written provenance. The source-page ID remains `Encuesta-10B-0016`; batch counts are by source PDF, not normalized grade.
- Page 17: the middle surname is partly illegible, retained as `Chi[illegible]one` without expansion.
- Page 18: green speckles occur across the page; their significance is uncertain. No separate handwritten legend was observed.

The manifest's outstanding-reading field and each question's issue description are the detailed handoff. “Completed” means visually inspected and transcribed, including explicit illegibility annotations; it does not mean all readings are certain. Unresolved readings are retained as follows:

| Grade 10B page / suffix | Outstanding reading or visible correction issue |
| --- | --- |
| 2 / 0002 | Q7: earlier response under a white correction patch cannot be read. |
| 3 / 0003 | Q4: meaning of trailing dots uncertain. Q12: overwritten first mark illegible. Q16: small Arts marks illegible; cancellation uncertain. Section absent; B inferred from filename. |
| 6 / 0006 | Q15: overwritten strokes around 3; earlier content uncertain. Q16–Q18: X and adjacent 1 retained without selecting a governing mark. |
| 7 / 0007 | Q7/Q8: overwritten content. Q16/Q17: scribbled-out marks illegible. Q16 Other: cancelled text illegible. Q18 Listening: overlapping strokes. |
| 8 / 0008 | Q4/Q8: earlier content beneath white correction patches is unreadable. |
| 10 / 0010 | Name and grade line blank; grade 10 and section B inferred from filename. |
| 12 / 0012 | Q1: crossed-out year/day content illegible; year replacement contains only 10. Q17: earlier Movies mark obscured by correction patch. |
| 13 / 0013 | Q12: angled digit appears to be 1 but could be 7; retained with reading uncertainty. |
| 15 / 0015 | Q6: cancelled responses illegible. Q16–Q18: X plus small numerals retained without deciding precedence. Grade line is date-like 14-08-09; grade/group inferred from filename. |
| 16 / 0016 | Q10: overwritten earlier content uncertain. Written grade 9°b conflicts with Grade 10B filename; written metadata retained. |
| 17 / 0017 | Name: middle surname partly illegible; readable portions retained. Q10: crossed-out earlier response illegible. |
| 18 / 0018 | Green speckles across page; significance uncertain. Q8: cancelled content illegible. Q10: overlapping strokes. Q15: overwritten numeral illegible. Q16–Q18: X plus nearby numerals retained. |
| 20 / 0020 | Q9 and several Q17 marks are faint; read as 5 and the separately recorded option numerals, respectively. |
| 22 / 0022 | Q10: crossed-out earlier response illegible. |

Legible response-format problems also remain for the separate cleaning stage: ranges, `1.80 aprox`, `15+ aprox`, `300+`, `IDK`, hour responses to minute/day questions, textual `Oneday`, literal height entries with decimal punctuation and units, and incomplete/extra/repeated rankings. For example, page 3 height literally reads `17.7`, page 5 `1.80cm`, and page 16 `1.75cm`; none has been repaired or converted. See all per-question issues in the workbook; the manifest focuses on outstanding scan readings and metadata exceptions.

### Ranking transcription and cleaning handoff

Every Q16–Q18 option has its own original mark field. Ticks, X marks, small/adjacent numerals, white correction patches and scribbled-out content are retained with the option where observed. No separate handwritten color/symbol legend was observed in Grade 10B; all three Grade 10B legend fields remain blank. Adjacent numbers are transcribed as visible marks, not decoded or selected as governing ranks. Page 21 numbers every option beyond 1–3; all written numbers are retained. Pages 13 and 16 have only single ticks/X marks, and pages 1 and 20 have extra/repeated ranks. No missing ranks were inferred.

**All Grade 10B validated/corrected answer fields and all correction-explanation fields are blank, even where the preliminary status is Valid.** Missing-validated-value and unresolved warnings are expected. No midpoint, unit conversion, number-word conversion, legend decoding, date reconstruction, normalization or clean-data population has been performed. No existing Grade 10B later-stage cleaned values were found, so there was no cleaning-stage conflict to preserve. Grade 10A's prior uncleaned status remains unchanged. The filtered dataset and source template were not modified.

For a rerun, match Grade 10B using **(source_pdf, original 1-based source_page_numbers)**. Here `questionnaire_sequence` equals that original page. Update the same row, preserve its existing ID and preserve all other batches. Never assign one ID to multiple pages or multiple IDs to one page. If later-stage cleaned values are present, preserve the entire affected record and report the conflict instead of replacing or clearing it. Refresh workbook row references only if row positions actually change.

Grade 10B is ready for the separate cleaning conversation with the documented reading uncertainties and metadata conflicts still open. Use these three handoff files, the original Grade 10B scan, reference questionnaire and full structural template. Resolve uncertain readings only with adequate scan/student evidence; otherwise retain the uncertainty. Preserve every raw original, observed mark association, page reference and ID while making any separately authorized cleaning decisions.

A rerun was verified to retain 22 Grade 10B records and 39 total records without duplicate workbook or manifest keys.

Verification: pages 1–22 were inspected and accounted for; 22 unique page keys and expected IDs occur exactly once in both workbook and manifest; row references match rows 19–40; all 396 statuses are present; validated/correction fields are empty; prior Grade 10A cells, styles, formulas and cached results compare unchanged. Native validation and conditional-format ranges are extended through row 40, and the Excel table covers only the 39 real records. Unrelated workbook package parts are preserved. Source PDF/template and filtered dataset remain unchanged. Native Excel interactive behavior was not separately tested.


## Third transcription batch: Grade 10C

**Grade 10C has been transcribed but not cleaned.** Earlier sections retain their batch-specific counts and documented cleaning status. All 39 Grade 10A/10B records, including values, notes, statuses, validated/correction fields, formulas and cached results, remain unchanged.

### Coverage and totals

- Source: `assets/data/pdf/Encuesta-10C.pdf`, **22 original PDF pages and 22 questionnaires**. All pages **1–22 inclusive** were visually inspected in full; enlarged crops were inspected for difficult names, units and overwritten marks. No pages were merged, split, skipped or renumbered. No OCR-derived answer was accepted.
- Page N = `Encuesta-10C-NNNN`; IDs run from `Encuesta-10C-0001` through `Encuesta-10C-0022`. Original 1-based page numbers are recorded separately.
- Workbook: `Questionnaires` rows **41–62**. Manifest: **22 Grade 10C page entries** with matching row references.
- Updated database total: **61 questionnaires = 17 Grade 10A + 22 Grade 10B + 22 Grade 10C**. The three worksheets and 180-column structure are retained; table range is `A1:FX62`.
- No blank, wholly unreadable or non-questionnaire pages. Page **12** has a blank Grade line; grade 10 and group C are explicitly filename-inferred. Page **16** gives grade 10 without a group; C is explicitly filename-inferred. Other written grade/group text, including case, remains in source metadata.
- All **396 Grade 10C Q1–Q18 preliminary statuses** are present: **290 Valid, 105 Ambiguous, 1 Invalid**. No Corrected status is used. Page 20 Q9 literally says `90`, outside the printed -10 to 10 scale; it is retained unchanged. Valid remains a preliminary transcription assessment only.

### Outstanding readings and exceptional responses

The following are unresolved scan readings or metadata exceptions. “Completed” means visually reviewed and transcribed, not that the response is certain or cleaned. Per-question issue descriptions also identify legible ranges, textual quantities, unit-bearing answers and incomplete/conflicting option marks.

| Grade 10C page / suffix | Outstanding reading or metadata exception |
| --- | --- |
| 1 / 0001 | Q16 Business and Q17 Other: X and overlapping 1-like strokes; intended mark uncertain. |
| 4 / 0004 | Q16 Education: faint erased/cancelled mark illegible; cancellation uncertain. |
| 5 / 0005 | Name: surname appears Jinde, reading uncertain. Q16 Social Sciences and Q17 Sports have overwritten strokes; earlier content uncertain. |
| 7 / 0007 | Q3: zero has overlapping strokes; earlier content uncertain. Q9: scribbled-out content illegible. |
| 8 / 0008 | Name: final surname appears Bop, reading uncertain. Q16 Law: faint partly erased 1. Q17 Sports/Friends: erased or smudged marks illegible; Movies/Music overwritten. Q18: faint/overwritten numerals. |
| 9 / 0009 | Name: first name and last surname partly illegible. Q7: reads 1d h; final unit-like stroke uncertain. Q16 Engineering: overwritten numeral read as 2; earlier strokes uncertain. |
| 11 / 0011 | Q16–Q18: X marks and numbers left of boxes retained separately; intended precedence uncertain. Q17 has four X-marked options. |
| 12 / 0012 | Grade line blank; grade 10 and group C inferred from filename. |
| 13 / 0013 | Name: surname read as Golán, uncertain. Q16–Q18: filled boxes may obscure earlier content; adjacent numerals preserved without choosing governing marks. |
| 15 / 0015 | Q16/Q17: filled boxes and adjacent I/II/III strokes retained as visible symbols. Q17 Friends faint shading/erasure uncertain. Q18 Diagrams: overwritten numeral read as 2; earlier content illegible. |
| 16 / 0016 | Group absent from Grade line; C inferred from filename. |
| 17 / 0017 | Name: final surname read as castillón, uncertain. Q4 has N/A plus seconds and 0.1m outside box. Q11 separator looks colon-like. Q12 IDK plus arrow and 27 Per year retained without choosing an answer. |
| 18 / 0018 | Q17 Video games/Reading: overwritten numerals read as 2/3; earlier strokes illegible. |
| 19 / 0019 | Name: surname partly illegible. Q1 year final digit appears 0 and extends outside box; uncertain. Q16 Engineering/Q17 Sports/Q18 Practicing have dark overlapping strokes; earlier content uncertain. |
| 21 / 0021 | Q11: middle height digit overwritten/illegible. Q16 Engineering and Other: overwritten 4-like marks; reading and cancellation uncertain. Q18 has only two marked options. |
| 22 / 0022 | Q16 Engineering: faint erased/smudged mark illegible; Humanities: overwritten 3, earlier content uncertain. Q16 Other text retained as phsycology; spelling/letter reading uncertain. |

All visible Q16–Q18 option marks are retained in separate original fields, including purple numerals, X marks, filled graphite boxes, adjacent numbers or I/II/III-like strokes, faint erasures and overwriting. No separate handwritten legend was observed; all three Grade 10C legend fields remain blank. The symbols and adjacent numerals have not been decoded or selected as governing ranks. Additional handwritten `Dance` on page 1 Q17 Other and page 4 Q17 Art/Other is retained with its option.

Examples of uncleaned responses include page 2 Q7 `9h`, page 3 Q14 `8months.`, page 11 Q12 `I DON'T KNOW`, page 16 Q12 `a lot`, page 17 Q4 `N/A` plus `seconds` and `0.1m` outside the box, and page 21 Q14 `N/A` plus `I dont know`. Literal decimal heights, ranges, crossed-out material and conflicting marks remain unchanged. Page 18 Q11 includes a sad-face symbol beside `162`. Page 21 Q11 retains the unreadable middle digit rather than selecting a height.

### Cleaning handoff and reruns

**Every Grade 10C validated/corrected answer field and correction-explanation field is blank, including for Valid responses.** No conversions, midpoints, textual-quantity interpretations, ranking decoding, date reconstruction, inferred answers or cleaned data were generated. No prior Grade 10C records or cleaned values were found, so there was no cleaning-stage conflict. The earlier batches' documented cleaning status remains unchanged. The filtered dataset and source/reference files were not modified.

For reruns, use **(source_pdf, original 1-based source_page_numbers)** as the stable key. Here questionnaire_sequence equals original page number. Update the existing matching row and preserve its ID/order; append only missing page keys. Preserve any later cleaned values and report their conflict before altering that record. Manifest row references must match the actual workbook rows.

The separate cleaning conversation should start with the reading uncertainties above and the per-question factual issues, using this workbook, manifest, README, original Grade 10C scan, questionnaire reference and structural template. Preserve every original answer, option-mark association, source/page key and ID. Expected missing-validated/unresolved diagnostics do not authorize filling cleaned values.

Verification: 22 unique Grade 10C page keys/IDs cover pages 1–22 exactly once; 61 total workbook and manifest records; matching workbook rows 41–62; all 396 new statuses; blank new validated/correction fields; prior rows 1–40 preserved verbatim at XML level. Unrelated workbook package parts, including the dictionary, instructions, styles and shared strings, remain unchanged. Table and native validation/conditional-format ranges extend through row 62. New records were rendered and inspected. Native Excel interactive behavior was not separately tested.


## Fourth transcription batch: Grade 10D

**Grade 10D has been transcribed but not cleaned.** Earlier sections retain their batch-specific counts and cleaning status. All 61 prior Grade 10A/10B/10C records, including original answers, metadata, statuses, notes, validated/correction fields, formulas and cached results, remain unchanged.

### Coverage and reconciliation

- Source: `assets/data/pdf/Encuesta-10D.pdf`, **19 original PDF pages**. All pages **1–19 inclusive** were visually inspected in full, with enlarged crops for uncertain names, long digit strings, separators and marks. No OCR-derived answers were accepted.
- **19 separate page-keyed questionnaire records**, one per page under the required one-page-one-questionnaire rule. No pages were merged, split, omitted or renumbered. Page N = `Encuesta-10D-NNNN`; IDs run from `Encuesta-10D-0001` through `Encuesta-10D-0019`.
- **18 pages contain Q1–Q18 forms. Page 6 is exceptional:** it contains Q19–Q21 material and a drawing only, with no student header or Q1–Q18 form. Its independent ID remains `Encuesta-10D-0006`; all 18 question statuses are Missing and original response fields are blank. It was not attached to another page. Q19–Q21 content was excluded from transcription.
- Workbook: `Questionnaires` rows **63–81**. Manifest: **19 Grade 10D records**, one per original page, with corresponding workbook row references.
- Updated database total: **80 records = 17 Grade 10A + 22 Grade 10B + 22 Grade 10C + 19 Grade 10D**. The Grade 10D count includes the flagged page 6 placeholder. Three worksheets and all 180 columns remain in their original order; table range is `A1:FX81`.
- All **342 Grade 10D Q1–Q18 statuses** are present: **267 Valid, 57 Ambiguous, 18 Missing**. No Corrected statuses were used. Valid is the existing preliminary transcription assessment, not a cleaned value.

### Metadata exceptions and outstanding readings

- Page **5** writes `9°D`. The written grade 9/group D are retained despite the Grade 10D filename.
- Page **7** writes grade `9` without a group. Grade 9 is retained; group D is explicitly filename-inferred.
- Pages **6 and 11** have no written grade/group. Grade 10 and group D are explicitly filename-inferred. Page 6 also has no student name; its name stays blank.
- Page **19** has cancelled, unreadable material before the readable `10°D`; both are retained in the original Grade-line field.

“Completed” means the page was visually inspected and transcribed, including explicit uncertainty. Page 6 uses `Completed with missing Q1–Q18 form/responses`. Unresolved readings and metadata exceptions are indexed below and in the manifest; per-question issue descriptions additionally describe ranges, textual quantities, units and incomplete/conflicting option marks without resolving them.

| Grade 10D page / suffix | Outstanding reading or metadata exception |
| --- | --- |
| 1 / 0001 | Q8: adjacent face/scribbled symbol uncertain. Q10: crossed-out earlier mark illegible. |
| 3 / 0003 | Name: final surname partly illegible. Q5/Q9: long strings of zeros/looped digits extend outside boxes; exact digit count unclear, readable portions retained. Q18: printed option boxes blank; an additional hand-drawn box below options is marked X beside Idk. |
| 4 / 0004 | Name: middle surname partly illegible; readable Mo retained. |
| 5 / 0005 | Name: middle surname partly illegible; readable lachan retained. Written grade 9°D conflicts with Grade 10D filename; written grade retained. Q6 literally reads 3> without reordering the symbol. |
| 6 / 0006 | No student header or Q1–Q18 responses on this page. Grade 10/group D inferred solely from filename; student name missing. Q19–Q21 excluded. |
| 7 / 0007 | Written grade 9 conflicts with Grade 10D filename; written grade retained. Group absent, D inferred from filename. |
| 9 / 0009 | Q10: 7 written over a white correction patch; earlier response unreadable. Curved stroke at left edge retained in issue notes; significance uncertain. |
| 10 / 0010 | Q5: isolated dot to the right of 6; significance uncertain. |
| 11 / 0011 | Grade line blank; grade 10/group D inferred from filename. Q1 month has crossed-out June plus 06 above; both retained. |
| 12 / 0012 | Q11: separator between 1 and 50 appears colon-like; retained without interpretation. |
| 13 / 0013 | Q2/Q3/Q7: zero-like ovals with diagonal slashes retained without deciding whether slash is cancellation or digit style. Q10: scribbled-out earlier mark illegible. |
| 16 / 0016 | Q16 Natural Sciences: faint/smudged mark read as 1; uncertain. Q18 only Listening and Practicing marked; no third mark inferred. |
| 17 / 0017 | Q10: final digit 5 overwritten; earlier strokes uncertain. Q12: scribbled-out mark illegible. Q16–Q18: filled/overwritten marks and adjacent numerals retained without selecting precedence; Q17 Friends scribbled-out content illegible. |
| 19 / 0019 | Grade line has illegible cancelled content before 10°D. Q10: 5, a scribbled-out mark and a 4 with crossing strokes remain visible; cancellation/precedence uncertain. Q16 Business/Q17 Friends: overlapping strokes. Q18 only Listening has X. |

### Original marks and cleaning handoff

Q16–Q18 option marks are recorded separately. X marks, filled/overwritten marks, adjacent numerals and cancellations remain as observed. Page 15's pink/magenta numerals retain their color annotations. No separate handwritten color/symbol legend was observed; all Grade 10D legend fields remain blank. No marks were decoded into numeric rankings.

Page 3 Q18 has blank printed option boxes plus an additional hand-drawn box marked X beside `Idk` below the printed options. The additional original response is retained in general notes and the Q18 issue description, without assigning it to a printed option. Page 3 Q16 has text on the Other line despite its blank box; no option mark was inferred. Page 7 Q17 writes 1–5 across five options. Page 16 Q18 has two marked options; page 19 Q18 has only an X at Listening. Missing ranks were not supplied.

Written responses such as `∞ lol`, long strings of zeros/looped digits, `Idk`, `many`, `3>`, `>30`, `7~8`, `1h-2h`, `1month`, decimal heights, literal `1.63cm`/`1,53cm`/`1.65cm`, and the colon-like height `1:50` remain unconverted and uninterpreted. Slashed zero-like marks on page 13 and competing/cancelled country answers on page 19 remain unresolved. White correction patches and unreadable cancellations use explicit annotations, while genuinely missing answers stay blank.

**All new Grade 10D validated/corrected fields and correction-explanation fields are blank, including for Valid responses.** No conversions, midpoint calculations, textual-quantity interpretation, ranking decoding, date reconstruction, inferred responses, filtering or clean-data population were performed. No pre-existing Grade 10D records or cleaned values were found, so there was no cleaning-stage conflict to preserve. Earlier batches' documented cleaning status is unchanged. The filtered dataset, source scans, questionnaire reference and structural templates were not modified.

For a rerun, match **(source_pdf, original 1-based source_page_numbers)**; questionnaire_sequence equals the original page in this batch. Update the same matching record, preserving its ID/order, and append only missing page keys. Preserve and report any later cleaned-value conflict rather than clearing those fields. Refresh manifest row references only to match actual workbook rows.

The separate cleaning conversation should use these three handoff files, the original Grade 10D scan, reference questionnaire and structural template. Begin with page 6, written-grade conflicts and outstanding reading uncertainties. Preserve original answers, source/page keys, IDs and option-mark associations while making any separately authorized cleaning decisions. Expected unresolved/missing-validated diagnostics do not authorize filling cleaned values.

Verification covered 19 unique Grade 10D keys/IDs and exact page coverage 1–19; 80 total workbook/manifest records; matching rows 63–81; all 342 statuses; blank new validated/correction fields; unchanged prior cells, styles, formulas and cached values; unchanged dictionary/instructions and unrelated workbook package parts. Table, native validation and conditional-format ranges extend through row 81. New workbook views were rendered and inspected. Reapplying the prepared batch retained 19 Grade 10D and 80 total records without duplicates. Native Excel interactive behavior was not separately tested.

## Grades 10E and 11A–11E: transcription batches 5–10 (2026-10-31)

All six scans were visually inspected page by page for **Q1–Q18 only**. Enlarged crops were reviewed for uncertain handwriting and marks. **All six groups have been transcribed but have not been cleaned.** This addition preserves the earlier documentation above, including the recorded cleaning status of Grades 10A–10D.

### Coverage and reconciliation

| Source batch | PDF pages / page-keyed questionnaires | Original page coverage | IDs | Workbook rows | Cleaning handoff |
| --- | ---: | --- | --- | --- | --- |
| 10E | 22 | 1–22, inclusive | Encuesta-10E-0001 through Encuesta-10E-0022 | 82–103 | Transcribed; not cleaned |
| 11A | 20 | 1–20, inclusive | Encuesta-11A-0001 through Encuesta-11A-0020 | 104–123 | Transcribed; not cleaned |
| 11B | 19 | 1–19, inclusive | Encuesta-11B-0001 through Encuesta-11B-0019 | 124–142 | Transcribed; not cleaned |
| 11C | 20 | 1–20, inclusive | Encuesta-11C-0001 through Encuesta-11C-0020 | 143–162 | Transcribed; not cleaned |
| 11D | 23 | 1–23, inclusive | Encuesta-11D-0001 through Encuesta-11D-0023 | 163–185 | Transcribed; not cleaned |
| 11E | 22 | 1–22, inclusive | Encuesta-11E-0001 through Encuesta-11E-0022 | 186–207 | Transcribed; not cleaned |

Sources are `assets/data/pdf/Encuesta-10E.pdf`, `Encuesta-11A.pdf`, `Encuesta-11B.pdf`, `Encuesta-11C.pdf`, `Encuesta-11D.pdf`, and `Encuesta-11E.pdf` in the same PDF directory. Each original PDF page has exactly one independent record. Pages were never merged, split, omitted or renumbered; questionnaire_sequence and source_page_numbers both equal the original 1-based page. Numbering restarts at 0001 for each PDF.

**126 records added; 0 existing target records updated. Updated database and manifest total: 206 page-keyed records**, comprising the unchanged 80 previous records (10A 17, 10B 22, 10C 22, 10D 19) plus 10E 22, 11A 20, 11B 19, 11C 20, 11D 23 and 11E 22. These are 102 records from Grade 10 source files and 104 from Grade 11 source files; written-grade conflicts remain unresolved. Counts include flagged non-Q1–Q18 page records and do not assert that all pages contain complete student questionnaires.

Workbook: `Questionnaires` rows 82–207; three worksheets and all 180 columns retain their order. Table, native validation and conditional-format coverage extend through row 207 (`A1:FX207`). Manifest contains one matching entry for every source/page key and actual workbook row.

### Exceptional pages and metadata

- **11B page 18 / Encuesta-11B-0018 (row 141):** Q19–Q21 material/drawing only; no student header or Q1–Q18 form. Kept as an independent record; name and original Q1–Q18 responses blank, all 18 statuses Missing. No content was attached to another page.
- **11C page 5:** Name and Grade lines blank; name remains missing, grade 11/section C explicitly filename-inferred.
- **11C page 17:** Written `10°E` conflicts with filename 11C. Written grade 10/section E and literal Grade-line text retained alongside the unchanged 11C source/page/ID; no reassignment or duplicate made.
- **11D page 11:** Grade line contains `19/8/26`; grade 11/section D explicitly filename-inferred.
- **11D page 23:** Scanned upside down; visually inspected after rotation, with original page number 23 unchanged.
- **11E page 13:** Written section looks G, uncertain, conflicting with filename E; original text retained, filename-based section explicitly labelled unresolved.
- Other absent/overwritten grade lines are retained in source_grade_original; grade/group provenance fields identify inference from filenames. No student answer was inferred.

### Outstanding reading uncertainties and observed exceptions

“Completed” means visually inspected and transcribed, including explicit uncertainty; it does not mean cleaned or resolved. The following is an indexed reading/metadata handoff. Factual descriptions of ranges, units, textual quantities, repeated ranks, missing responses and symbols also appear in the workbook per-question issue fields.

| Group / original page | Reading uncertainty or observation retained |
| --- | --- |
| 10E / 2 | Group absent; E inferred from filename. Q14 overwritten numeral read as 9; prior strokes uncertain. |
| 10E / 3 | Q1 month overwritten, read as 10; prior strokes uncertain. Q10–Q15 have adjacent dash-like/curved strokes; significance uncertain. |
| 10E / 6 | Q17 bracket between Video games and Music says Simultaneously; both option marks retained as written, without choosing a governing rank. |
| 10E / 7 | Q1 year overlapping initial strokes; readable 2010 retained. Q5 reads 7.3-7; punctuation/meaning unresolved. |
| 10E / 9 | Q16 Business: faint erased mark illegible; cancellation uncertain. |
| 10E / 12 | Q9: thick red mark illegible. Q16 Humanities: overwritten red numeral appears 1, earlier content uncertain. |
| 10E / 13 | Q16 Social Sciences: faint erased mark illegible; cancellation uncertain. |
| 10E / 14 | Name: middle surname partly illegible. Grade line blank; grade/group inferred from filename. Q4 blank. Q16–Q18 X marks and numbers left of boxes retained without selecting precedence. |
| 10E / 15 | Name: final surname read as Barreache, uncertain. Q10 literally 2.5; fractional response retained. |
| 10E / 16 | Q16 X and adjacent numerals retained without choosing precedence. |
| 10E / 17 | Name: middle surname partly illegible. |
| 10E / 18 | Q7 cancellation illegible and replacement appears 4; uncertain. |
| 10E / 20 | Q1 year has trailing comma-like mark; meaning uncertain. |
| 10E / 22 | Q16–Q18 X and adjacent numbers retained without choosing precedence. Q17 Art has small isolated dot, significance uncertain. |
| 11A / 1 | Q16–Q18 X and adjacent numerals retained without choosing precedence. |
| 11A / 3 | Q16–Q18 blue X marks and adjacent numerals retained without choosing precedence. |
| 11A / 6 | Grade line blank; grade 11 and A inferred from filename. |
| 11A / 10 | Q1 cancelled year illegible; month 04 crossed out with 09 above. Q16 Business/Q17 Sports scribbled/overlapping X marks and adjacent 1 retained. |
| 11A / 13 | Grade blank; grade/group filename-inferred. Q16 Business overwritten 1; earlier strokes uncertain. |
| 11A / 15 | Name: final surname partly illegible. Q16–Q18 X and adjacent numerals retained; Q17 Sports also X-marked without adjacent numeral. |
| 11A / 16 | Name: surnames faint, read as Alba Alvarez; uncertain. |
| 11A / 17 | Q16–Q18 turquoise filled boxes obscure any earlier content; no numeric rank inferred. |
| 11A / 18 | Q12: readable 80 with white patch/erased strokes to right; earlier content unreadable. |
| 11A / 19 | Q10: overwritten numeral read as 4; earlier strokes uncertain. |
| 11A / 20 | Q16 Business scribbled-out mark illegible, 1 written at right. Q17 Sports overwritten 1; earlier content uncertain. |
| 11B / 2 | Q10: readable 7 with faint 0-like stroke to right; cancellation/meaning uncertain. Q17 Video games overwritten numeral read as 1. |
| 11B / 4 | Grade blank; grade/group filename-inferred. |
| 11B / 7 | Q1 month cancelled content illegible; 7 above box retained. |
| 11B / 8 | Name: surname read as Nora, uncertain. Q1 year appears 2001, final digit uncertain. Q2 zero overlapping loops. Q16 initial marks overlap earlier strokes. |
| 11B / 11 | Group absent; B filename-inferred. Q6 separator appears colon-like. Q14 has adjacent 47 and 15; cancellation/precedence uncertain. |
| 11B / 13 | Q1 final year digit uncertain. Q7/Q14 overwritten numerals read as 4/6; earlier content uncertain. |
| 11B / 14 | Q16 Business/Q17 Sports/Q18 Combination: overwritten/tick-like marks and adjacent 1 retained without selecting precedence. |
| 11B / 17 | Name: surname read as Onshuus, uncertain. Grade blank, inferred from filename. Q8/Q12/Q15 scribbled-out content illegible. |
| 11B / 18 | EXCEPTION: Q19–Q21 material/drawing only; no Q1–Q18 form or student header. Separate record, not merged. Grade/group filename-inferred; name missing. |
| 11B / 19 | Grade line blank; grade/group filename-inferred. Q1 month 5 over white patch; earlier content unreadable. |
| 11C / 3 | Name: middle surname read as Siolo, uncertain. Grade component has overlapping/4-like stroke; retained with uncertainty. |
| 11C / 5 | Name and Grade lines blank. Grade 11 and C filename-inferred; name remains missing. |
| 11C / 7 | Q7 has an adjacent dot of uncertain significance. Q17 Movies has a faint erased mark of uncertain content. |
| 11C / 8 | Q2 small hook-like mark is illegible. Q17 Video games contains a faint erased mark of uncertain content. |
| 11C / 11 | Grade digits overwritten and illegible; C readable. Q16–Q18 use X marks without a stated ranking legend; faint background/erased lines also visible. |
| 11C / 12 | Surname read as Nkoonejad, uncertain. Q16–Q18 contain repeated numbers across more than three options. |
| 11C / 14 | Surname read as Ciri, uncertain. Q16 Natural Sciences annotated (chemestry). Numerous faint erased marks in Q16–Q18 retained separately; their content/status is uncertain. |
| 11C / 16 | Q16–Q18 retain both box X marks and adjacent numerals; no conversion. |
| 11C / 17 | Written grade 10°E conflicts with source filename 11C; retained. Q16 Engineering crossed-out box mark with adjacent 1. Q17 Music cancelled illegible mark. Other numerals mostly outside boxes. |
| 11C / 18 | Q1 month has faint ticks to left of 5. Q17 Friends box and Q18 Practicing/Discussing boxes partly obscured/erased; response content, if any, unreadable. Q18 only one clearly marked option. |
| 11C / 20 | Q12 appears 99 with a heavily overwritten second digit, uncertain. |
| 11D / 1 | Q12 appears 8, overwritten. Q16 Other marked 1 with description line blank. |
| 11D / 2 | Q14 first digit overwritten; appears 128. Box X marks and adjacent numerals retained separately. |
| 11D / 3 | Box X marks and adjacent numerals retained separately. |
| 11D / 4 | Q16 Arts and Q17 Movies/Reading have overlapping marks; numerals/cancellations uncertain. Q18 uses X marks without stated legend. |
| 11D / 5 | Q16 only two numbered options; Q17 four options including 4. Extensive faint background drawing visible. |
| 11D / 6 | Surname appears Amorsocho, uncertain. Q1 month DEC crossed out with 12 written above. |
| 11D / 7 | Q1 year has unreadable marks above; month stacked 0 and 8; day has overlapping/stacked 24 and apparent 14, cancellation uncertain. |
| 11D / 8 | Grade digits overlap; read as 11D, uncertain. |
| 11D / 11 | Grade line contains 19/8/26, not a grade/section; Grade 11/D filename-inferred. Q1 month first digit overwritten, read as 0, uncertain. |
| 11D / 12 | Q10 second digit overwritten, appears 0, uncertain. Q16 only Engineering numbered. |
| 11D / 14 | Q16 Law contains overlapping 1/X-like mark; cancellation/content uncertain. |
| 11D / 15 | Q16–Q18 each have only two options marked, with X in boxes and adjacent 1/3. |
| 11D / 16 | Q7 blank. Q11 separator appears colon-like; retained as 1:72. |
| 11D / 18 | Q1 final year digit appears 1, uncertain. Q16–Q18 contain black filled/scribbled boxes as well as numerals; no stated legend; not decoded. |
| 11D / 19 | Q2/Q3 use slashed zero-like marks. Q17/Q18 repeat numerals across more than three options. |
| 11D / 20 | Q2/Q3 slashed zero-like marks. Q16 Medicine/Arts box borders partly erased; no readable response marks there. |
| 11D / 21 | Grade digits heavily overwritten; D readable. Q4 first digit appears 3, overwritten. Q16 Business and Social Sciences have overlapping/cancelled marks of uncertain status. |
| 11D / 22 | Name read as Tomás Rodríguez Sastoque, uncertain. Q10 appears 61 with overwritten first digit, uncertain. Q16 Other and Q18 Discussing overlapping marks; Q16–Q18 only two clearly marked options each. |
| 11D / 23 | Page scanned upside down; reviewed after rotation; original page number preserved. |
| 11E / 1 | Q1 year reads 2027; month final digit uncertain. Q16–Q18 use X marks without stated ranking legend; Q17 has seven X-marked options. |
| 11E / 5 | Q17 Other numbered 1 without description. |
| 11E / 6 | Q8 has an illegible cancelled mark before 60min. Q10 has 4 and an illegible scribbled-out mark to right. |
| 11E / 7 | Q10 has scribbled/cancelled 3 followed by 4. Q12 cancelled illegible mark before 4. Q13 blank. |
| 11E / 8 | Q1 year contains only separated digits 2 6. Q16–Q18 number all options with repeated numbers. Q17 Other numbered without text. |
| 11E / 10 | Q16 adds a separate hand-drawn box labelled Aeronautic with 3 [blue], beside the printed options; retained as additional option in notes. Q10 cancelled illegible mark before 6. Q17 Video games box erased with small unreadable blue remnant. |
| 11E / 11 | Grade written Eleventh; section E filename-inferred. Q12 blank. Q16–Q18 have repeated numerals on more than three options. |
| 11E / 12 | Q16–Q18 each contain one X-marked option without stated ranking legend. Q17 Other description absent. |
| 11E / 13 | Written section looks G, uncertain, conflicts with E filename; retained. |
| 11E / 14 | Q10 6 crossed out followed by 7. Q16–Q18 preserve adjacent numbers and box X marks. |
| 11E / 15 | Surname read as Rekhan, uncertain. Q16 numbers 1–10; Q17 numbers 1–8; Q18 numbers 1–7; retained as marks without conversion. |
| 11E / 16 | Q16 Other text Gastronomy with its box blank. Q17 Music X accompanied by NO at left, conflicting marks retained. X marks have no stated ranking legend. |
| 11E / 17 | Box X marks and adjacent numerals retained separately. |
| 11E / 18 | Q2 blank. Q4 overlapping cancelled text appears 1.30H with 90 to right; uncertain. Q7 cancelled 4 followed by 6. Q10 small dash before 5 has uncertain significance. |
| 11E / 19 | Grade section overwritten; E/B-like strokes uncertain. Q16 Humanities and Q17 Reading boxes partly erased; no readable answer marks there. |
| 11E / 20 | Q1 year contains only 09. |
| 11E / 21 | Surname read as Guauta, uncertain. Q4 first digit looks 7 or 1, followed by :30; no unit written. |
| 11E / 22 | Q16 diagonal stroke extends from Medicine 1 across Business box; unclear whether independent mark. Q18 Discussing has a small red dot of uncertain significance; Practicing contains overlapping extended strokes. |

### Preliminary question statuses and marks

| Batch | Valid | Ambiguous | Missing | Invalid |
| --- | ---: | ---: | ---: | ---: |
| 10E | 306 | 88 | 1 | 1 |
| 11A | 311 | 49 | 0 | 0 |
| 11B | 277 | 46 | 18 | 1 |
| 11C | 302 | 58 | 0 | 0 |
| 11D | 334 | 79 | 1 | 0 |
| 11E | 318 | 75 | 3 | 0 |

All 2,268 new Q1–Q18 statuses are present. No Corrected statuses were used. Valid remains a preliminary transcription assessment; it does not populate a validated value. Missing responses stay blank and have Missing status; unreadable writing uses `[illegible]` with readable portions retained. Ranges, approximation signs, units, textual quantities, conflicting answers, cancellations and overwritten digits remain unconverted.

Q16–Q18 option marks are stored separately as original text, including visible colors, X/tick/filled/scribbled marks, erased traces, outside-box numerals and adjacent annotations. No symbols or colors were decoded, and no rank was inferred. 10E page 6 writes `Simultaneously` beside a bracket between Video games and Music; retained in notes and q17_legend_original. No other separate handwritten ranking/color/symbol legend was observed. 11E page 10 adds a hand-drawn Q16 box marked `3` [blue], labelled `Aeronautic`; this additional option is retained in general notes and Q16 issue description without assigning it to a printed option. 11C page 14 annotates Natural Sciences `(chemestry)`; the original annotation is retained beside that option.

For cleaning review, the following table indexes all new non-Valid question statuses; the exact original and factual issue description remain in the workbook. This includes readable ranges/units and mark patterns as well as reading uncertainties.

| Group / original page | Questions requiring later review |
| --- | --- |
| 10E / 1 | Q12: Ambiguous, Q14: Ambiguous, Q15: Ambiguous |
| 10E / 2 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q11: Ambiguous, Q12: Ambiguous, Q14: Ambiguous |
| 10E / 3 | Q1: Ambiguous, Q10: Ambiguous, Q11: Ambiguous, Q12: Ambiguous, Q13: Ambiguous, Q14: Ambiguous, Q15: Ambiguous |
| 10E / 4 | Q5: Ambiguous, Q11: Ambiguous |
| 10E / 5 | Q11: Ambiguous |
| 10E / 6 | Q8: Ambiguous, Q11: Ambiguous, Q14: Ambiguous, Q17: Ambiguous |
| 10E / 7 | Q1: Ambiguous, Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q12: Ambiguous, Q13: Ambiguous, Q15: Ambiguous |
| 10E / 8 | Q1: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 10E / 9 | Q16: Ambiguous |
| 10E / 10 | Q16: Ambiguous |
| 10E / 11 | Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 10E / 12 | Q8: Ambiguous, Q9: Ambiguous, Q14: Ambiguous, Q16: Ambiguous |
| 10E / 13 | Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous |
| 10E / 14 | Q4: Missing, Q7: Invalid, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 10E / 15 | Q10: Ambiguous |
| 10E / 16 | Q4: Ambiguous, Q5: Ambiguous, Q11: Ambiguous, Q16: Ambiguous |
| 10E / 17 | Q11: Ambiguous |
| 10E / 18 | Q1: Ambiguous, Q2: Ambiguous, Q3: Ambiguous, Q7: Ambiguous, Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 10E / 19 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q7: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q13: Ambiguous, Q16: Ambiguous |
| 10E / 20 | Q1: Ambiguous, Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q8: Ambiguous, Q11: Ambiguous |
| 10E / 21 | Q4: Ambiguous, Q6: Ambiguous, Q11: Ambiguous, Q17: Ambiguous |
| 10E / 22 | Q8: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11A / 1 | Q5: Ambiguous, Q6: Ambiguous, Q7: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11A / 2 | Q16: Ambiguous |
| 11A / 3 | Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11A / 4 | Q4: Ambiguous |
| 11A / 6 | Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11A / 7 | Q5: Ambiguous, Q11: Ambiguous |
| 11A / 8 | Q11: Ambiguous |
| 11A / 10 | Q1: Ambiguous, Q16: Ambiguous, Q17: Ambiguous |
| 11A / 11 | Q5: Ambiguous, Q6: Ambiguous, Q8: Ambiguous |
| 11A / 13 | Q11: Ambiguous, Q16: Ambiguous |
| 11A / 14 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q18: Ambiguous |
| 11A / 15 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q7: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q12: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11A / 17 | Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11A / 18 | Q12: Ambiguous |
| 11A / 19 | Q10: Ambiguous, Q11: Ambiguous |
| 11A / 20 | Q16: Ambiguous, Q17: Ambiguous |
| 11B / 1 | Q11: Ambiguous |
| 11B / 2 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q8: Ambiguous, Q10: Ambiguous, Q11: Ambiguous, Q14: Ambiguous, Q16: Ambiguous, Q17: Ambiguous |
| 11B / 4 | Q4: Ambiguous |
| 11B / 5 | Q11: Ambiguous |
| 11B / 6 | Q11: Ambiguous |
| 11B / 7 | Q1: Ambiguous, Q4: Ambiguous, Q11: Ambiguous |
| 11B / 8 | Q1: Ambiguous, Q2: Ambiguous, Q16: Ambiguous, Q17: Ambiguous |
| 11B / 9 | Q11: Ambiguous |
| 11B / 10 | Q11: Ambiguous |
| 11B / 11 | Q6: Ambiguous, Q14: Ambiguous |
| 11B / 13 | Q1: Ambiguous, Q7: Ambiguous, Q14: Ambiguous |
| 11B / 14 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q7: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q13: Ambiguous, Q14: Ambiguous, Q15: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11B / 16 | Q9: Invalid, Q11: Ambiguous |
| 11B / 17 | Q8: Ambiguous, Q10: Ambiguous, Q11: Ambiguous, Q12: Ambiguous, Q15: Ambiguous |
| 11B / 18 | Q1: Missing, Q2: Missing, Q3: Missing, Q4: Missing, Q5: Missing, Q6: Missing, Q7: Missing, Q8: Missing, Q9: Missing, Q10: Missing, Q11: Missing, Q12: Missing, Q13: Missing, Q14: Missing, Q15: Missing, Q16: Missing, Q17: Missing, Q18: Missing |
| 11B / 19 | Q1: Ambiguous |
| 11C / 1 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q7: Ambiguous, Q8: Ambiguous, Q11: Ambiguous |
| 11C / 4 | Q4: Ambiguous, Q6: Ambiguous, Q8: Ambiguous, Q11: Ambiguous |
| 11C / 5 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q11: Ambiguous |
| 11C / 7 | Q1: Ambiguous, Q4: Ambiguous, Q7: Ambiguous, Q11: Ambiguous, Q17: Ambiguous |
| 11C / 8 | Q2: Ambiguous, Q17: Ambiguous |
| 11C / 9 | Q17: Ambiguous |
| 11C / 11 | Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11C / 12 | Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11C / 14 | Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11C / 15 | Q5: Ambiguous, Q9: Ambiguous, Q11: Ambiguous |
| 11C / 16 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11C / 17 | Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11C / 18 | Q1: Ambiguous, Q5: Ambiguous, Q12: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11C / 19 | Q1: Ambiguous, Q11: Ambiguous |
| 11C / 20 | Q11: Ambiguous, Q12: Ambiguous |
| 11D / 1 | Q12: Ambiguous, Q16: Ambiguous |
| 11D / 2 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q7: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q14: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11D / 3 | Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11D / 4 | Q4: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q12: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11D / 5 | Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous |
| 11D / 6 | Q1: Ambiguous, Q11: Ambiguous |
| 11D / 7 | Q1: Ambiguous |
| 11D / 8 | Q11: Ambiguous |
| 11D / 9 | Q1: Ambiguous, Q11: Ambiguous, Q16: Ambiguous |
| 11D / 10 | Q5: Ambiguous, Q6: Ambiguous, Q8: Ambiguous, Q11: Ambiguous |
| 11D / 11 | Q1: Ambiguous |
| 11D / 12 | Q1: Ambiguous, Q4: Ambiguous, Q10: Ambiguous, Q12: Ambiguous, Q16: Ambiguous |
| 11D / 13 | Q4: Ambiguous, Q8: Ambiguous, Q10: Ambiguous |
| 11D / 14 | Q11: Ambiguous, Q16: Ambiguous |
| 11D / 15 | Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11D / 16 | Q4: Ambiguous, Q5: Ambiguous, Q7: Missing, Q8: Ambiguous, Q11: Ambiguous |
| 11D / 18 | Q1: Ambiguous, Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11D / 19 | Q2: Ambiguous, Q3: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11D / 20 | Q2: Ambiguous, Q3: Ambiguous, Q4: Ambiguous, Q5: Ambiguous, Q12: Ambiguous |
| 11D / 21 | Q4: Ambiguous, Q16: Ambiguous |
| 11D / 22 | Q4: Ambiguous, Q8: Ambiguous, Q10: Ambiguous, Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 1 | Q1: Ambiguous, Q10: Ambiguous, Q11: Ambiguous, Q12: Ambiguous, Q15: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 3 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q7: Ambiguous, Q8: Ambiguous, Q11: Ambiguous |
| 11E / 4 | Q11: Ambiguous |
| 11E / 5 | Q11: Ambiguous |
| 11E / 6 | Q4: Ambiguous, Q5: Ambiguous, Q6: Ambiguous, Q8: Ambiguous, Q10: Ambiguous |
| 11E / 7 | Q10: Ambiguous, Q12: Ambiguous, Q13: Missing |
| 11E / 8 | Q1: Ambiguous, Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 10 | Q4: Ambiguous, Q8: Ambiguous, Q10: Ambiguous, Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous |
| 11E / 11 | Q4: Ambiguous, Q11: Ambiguous, Q12: Missing, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 12 | Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 14 | Q10: Ambiguous, Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 15 | Q4: Ambiguous, Q8: Ambiguous, Q11: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 16 | Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 17 | Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |
| 11E / 18 | Q2: Missing, Q4: Ambiguous, Q5: Ambiguous, Q7: Ambiguous, Q10: Ambiguous |
| 11E / 20 | Q1: Ambiguous, Q4: Ambiguous, Q8: Ambiguous, Q11: Ambiguous |
| 11E / 21 | Q4: Ambiguous, Q11: Ambiguous |
| 11E / 22 | Q1: Ambiguous, Q4: Ambiguous, Q6: Ambiguous, Q16: Ambiguous, Q17: Ambiguous, Q18: Ambiguous |

### Cleaning handoff and preservation

**Every new validated/corrected value and correction-explanation field is blank, including for Valid responses, across 10E and 11A–11E.** No unit conversion, midpoint calculation, textual-quantity interpretation, date reconstruction, ranking decoding, inferred answer, filtering or cleaned-data generation was performed. No existing records or cleaned values from these six groups were found before appending, so no pre-existing cleaned-value conflict arose.

All 80 previous questionnaire records retain their values, statuses, notes, validated data, formulas, cached values and cell styles unchanged. Existing manifest entries and README documentation are preserved verbatim. Dictionary/instructions, unrelated workbook package parts, filtered dataset, scans, reference questionnaire and structural templates were not modified.

The separate cleaning task should begin with 11B page 18, metadata conflicts (especially 11C page 17 and 11E page 13), overwritten/illegible entries, and the indexed question issues above. Preserve original response text, option associations, IDs and source/page keys while making separately authorized cleaning decisions. Formula diagnostics such as Validated answer missing/Unresolved are expected at this transcription-only stage and do not authorize filling validated fields.

For reruns use **(source_pdf, original 1-based source_page_numbers)** as the stable key. Preserve matching IDs and row order; update transcription fields in place and append only absent pages. Preserve and report any later cleaned-value conflict instead of clearing validated/correction fields. Match manifest row references to actual workbook rows.

Verification checked all 126 unique new source/page keys and independent IDs; exact six-PDF page coverage; 206 workbook and manifest records; matching workbook row references; all new question statuses; blank new validated/correction fields; unchanged prior rows, styles, formulas and caches; unchanged reference/filtered files; and extended native ranges. Prepared-batch replay retained 126 target keys and 206 total records without duplicates. Before/after workbook views were rendered and inspected. Native Excel interactive behavior was not separately tested.
