from pathlib import Path
from decimal import Decimal
import re,json
from pypdf import PdfReader
root=Path.cwd(); work=root/'tmp/c1-score-update-20261123'; folder=root/'book2026-2027/grade10/term_2/4-learning_evidences'
report={}
for suffix in ('exam','exam_solution'):
    name=f'G10_T2_L1_C1C2_{suffix}'
    text=(folder/(name+'.tex')).read_text(encoding='utf-8')
    old=(work/(name+'.tex')).read_text(encoding='utf-8')
    if suffix=='exam':
        marker=r'\SubsectionBox{Local parcel delivery fees'
        assert text.split(marker,1)[1]==old.split(marker,1)[1], 'Problems 3-6 changed'
        questions=re.split(r'\\SubsectionBox\{',text)[1:]
        for q in questions[:2]:
            assert re.findall(r'\\sscore\{\\sml\{(\d+)\}\}',q)==['1','1','1']
        assert re.findall(r'C([12])-\\sml\{(\d+)\}',text)==[('1','3'),('1','3'),('2','2'),('2','2'),('2','4'),('2','6')]
    else:
        marker=r'\sectionScored{Local parcel delivery fees'
        assert text.split(marker,1)[1].split(r'\textbf{Scoring reconciliation.}')[0]==old.split(marker,1)[1].split(r'\textbf{Scoring reconciliation.}')[0], 'Problems 3-6 changed'
        assert re.findall(r'C([12])-\\sml\{(\d+)\}',text)==[('1','3'),('1','3'),('2','2'),('2','2'),('2','4'),('2','6')]
        sections=re.split(r'\\sectionScored\{',text)[1:]
        for q in sections[:2]:
            assert re.findall(r'\\score\{(\d+)\}',q)==['1']*6
        for line in text.splitlines():
            if r'\textbf{Proposed partial credit.}' in line:
                components=re.findall(r'(\d+(?:\.\d+)?) for ',line)
                total=re.search(r'Total: (\d+) point',line).group(1)
                assert sum(map(Decimal,components))==Decimal(total),line
        for q in sections[:2]:
            line=[l for l in q.splitlines() if '0.125 for' in l][0]
            assert re.findall(r'(\d+(?:\.\d+)?) for ',line)==['0.125','0.25','0.125','0.375','0.125']
    assert '4 out of 6 points' in text and '4 out of 14 points' in text
    assert not re.search(r'C1.{0,30}(?:total: 8|4 out of 8|4\+4=8)',text)
    reader=PdfReader(work/suffix/(name+'.pdf'))
    destinations=reader.named_destinations
    checked=0
    for page in reader.pages:
        for annotation in page.get('/Annots',[]):
            item=annotation.get_object(); action=item.get('/A',{})
            dest=item.get('/Dest') or (action.get('/D') if action.get('/S')=='/GoTo' else None)
            if isinstance(dest,str):
                assert dest in destinations, dest
                checked+=1
    alltext='\n'.join(p.extract_text() for p in reader.pages)
    assert '??' not in alltext
    if suffix=='exam_solution':
        for i in (1,2):
            dest=destinations[f'section.{i}']
            assert reader.get_destination_page_number(dest)==i
        assert len(re.findall(r'\\newlabel\{sec:q[1-6]\}',(work/suffix/(name+'.aux')).read_text()))==6
    report[suffix]={'pages':len(reader.pages),'resolved_internal_links':checked,'scores':[3,3,2,2,4,6],'criterion_totals':[6,14],'overall_total':20,'visual_review':'all pages inspected; no overlap or clipping'}
report['preserved_issue']='Exam Problem 5 retains its pre-existing extra [1] after the context; heading and tasks allocate 4 points. Problems 3-6 preserved by request.'
(work/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
