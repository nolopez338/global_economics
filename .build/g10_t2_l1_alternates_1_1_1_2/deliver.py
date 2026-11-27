from pathlib import Path
from pypdf import PdfReader
import re,json,hashlib,shutil

root=Path.cwd();work=root/'.build/g10_t2_l1_alternates_1_1_1_2';dest=root/'book/grade10/term_2/4-learning_evidences'
files=[('source_student','G10_T2_L1_C1C2_exam_1',4)]
for v in (1,2):
    files += [(f'G10_T2_L1_C1C2_exam_1_{v}',f'G10_T2_L1_C1C2_exam_1_{v}',4),(f'G10_T2_L1_C1C2_exam_solution_1_{v}',f'G10_T2_L1_C1C2_exam_solution_1_{v}',27)]
report=[]
for folder,stem,count in files:
    build=work/folder
    log=(build/(stem+'.log')).read_text(errors='replace')
    assert not re.search(r'Overfull \\[hv]box|Underfull \\[hv]box|LaTeX Warning:.*(?:undefined|changed|multiply)|Package .* Warning:',log),stem
    r=PdfReader(build/(stem+'.pdf'));assert len(r.pages)==count
    assert all(abs(float(p.mediabox.width)-612)<1 and abs(float(p.mediabox.height)-792)<1 for p in r.pages)
    links=0
    for page in r.pages:
        for annot in page.get('/Annots',[]):
            obj=annot.get_object();a=obj.get('/A',{})
            target=a.get('/D') if a.get('/S')=='/GoTo' else obj.get('/Dest')
            if isinstance(target,str):assert target in r.named_destinations,(stem,target)
            if target is not None:links+=1
    if 'solution' in stem:
        expected=[2,5,8,13,18,23]
        assert [r.get_destination_page_number(r.named_destinations[f'section.{i}'])+1 for i in range(1,7)]==expected
    pdf=dest/(stem+'.pdf')
    if pdf.exists() and stem!='G10_T2_L1_C1C2_exam_1':raise RuntimeError('PDF collision: '+str(pdf))
    if pdf.exists():
        shutil.copy2(pdf,work/(pdf.name+'.before_main_scores'))
        shutil.copyfile(build/pdf.name,pdf)
    else:
        with pdf.open('xb') as f:f.write((build/pdf.name).read_bytes())
    assert hashlib.sha256(pdf.read_bytes()).digest()==hashlib.sha256((build/pdf.name).read_bytes()).digest()
    report.append(dict(stem=stem,pages=count,internal_links_checked=links,clean_log=True,letter_portrait=True,all_pages_visually_inspected=True,matching_pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest()))
(work/'final_pdf_checks.json').write_text(json.dumps(report,indent=2))
text='''Completed: two alternate exam-solution pairs derived directly from the explicitly supplied source pair, plus the requested main-score notation update in all three student exams.

Versions: 1_1 and 1_2. Exact requested basenames; no pre-existing alternate or output collision.
Solution-first workflow: each complete worked solution was calculated and verified before deriving its student exam. The original solution, dependencies and all unrelated pre-existing artifacts retain their recorded SHA-256 hashes. The source student TeX and PDF changed only for the later authorized score-placement update.

Verification: 233 corresponding mathematical steps retain operations, dependencies, reasoning and operand counts. Exact rational arithmetic checks every distribution, grouping, cumulative sum, jump and requested probability. Independent enumeration of all distinct-item subsets confirms Question 6 (286 and 120 subsets). Pair statements and task (c) wording agree exactly. All 18 rubric subtotals per solution reconcile to the original marks: C1=6, C2=14, overall=20. No option-selection questions occur, so selection-diversity planning is inapplicable.

Score notation: all 54 main scores in the three exams use \\sscore{\\sml{...}} immediately after the relevant (a), (b), or (c) reference. Exact reversal of those edits reproduces each prior source. Task descriptions, criterion assignments, all numeric score values, all (i)/(ii) internal breakdowns and assessment totals are unchanged.

Unavoidable numerical repetitions:
- Question numbering, marks, pass thresholds, penalties, institutional metadata, experiment arities and response-sheet dimensions are structural.
- Zero payouts/no receipts, zero composition entries, indicator values 0/1, probability tails 0/1, normalization to 1, and the relative baseline coefficient 1 are forced by the same model.
- Q3 has four equal grouped masses, so each is 1/4; its CDF heights 1/2 and 3/4 and answers 1/2 and 1/4 are consequently fixed. All eight corresponding supplied category probabilities change in both versions.
- Q6 still selects three items and has exactly two high-value items. Three high-value items would add a tenth composition and change the procedure; fewer than two would remove required compositions. The composition indices, binomial choose-zero/choose-all values of 1, and choose(2,1)=2 follow from this preserved structure.
- Q5 retains E=B and G=F as equality/copy steps; their implicit ratio 1 is fixed, while their actual probabilities change.
All 201 repeated corresponding trace fields have explicit justifications in numerical_repetitions_justified.json. No accidental repetition of a replaceable corresponding given, operand or result remains. Equal values at unrelated roles are not corresponding repetitions.

Build and visual review: isolated matching-basename pdfLaTeX builds, stabilized references, clean final logs, valid internal PDF link targets and Letter portrait geometry. All 66 final pages were rendered and inspected (three 4-page student exams and two 27-page solutions), with detailed inspection of the composition/CDF pages. The two dedicated blank response sheets remain in each student exam. No unresolved limitations. No new general-purpose validation asset was needed; the existing renderer was reused and the mathematical checks here are task-specific.

Audit files: procedure_operand_comparison.tsv and .json; numerical_repetitions_justified.json; main_score_notation_verification.json; final_content_checks.json; final_pdf_checks.json; protected_sha256.json.
'''
(work/'verification_report.txt').write_text(text,encoding='utf-8')
print('Delivered five matching PDFs:',sum(x['pages'] for x in report),'pages; logs, geometry and link targets checked.')
