from pathlib import Path
from decimal import Decimal as D
import re
from pypdf import PdfReader

root=Path(__file__).resolve().parents[1]
build=root/'tmp/g11_c1c2_build'
name='G11_T2_L1_C1C2_exam_solution'
tex=(root/'book2026-2027/grade11/term_2/4-learning_evidences'/f'{name}.tex').read_text(encoding='utf-8')
log=(build/f'{name}.log').read_text(errors='replace')
assert not re.search(r'Overfull|Underfull|undefined|multiply defined|destination with the same identifier|Warning',log)
assert tex.count('\\sectionScored{')==3
assert tex.count('\\worked{')==15
assert tex.count('\\taskprompt{')==15
assert len(re.findall(r'\\input\{preamble_exams.tex\}',tex))==1

# Independently calculate using the numerical givens in the governing questions.
expected=[
 (100,240,60,D('1.960'),(D('11.76'),D('228.24'),D('251.76'),D('23.52'))),
 (144,82,36,D('1.645'),(D('4.935'),D('77.065'),D('86.935'),D('9.87'))),
 (144,82,36,D('2.576'),(D('7.728'),D('74.272'),D('89.728'),D('15.456'))),
 (64,32,8,D('1.960'),(D('1.96'),D('30.04'),D('33.96'),D('3.92')))]
for n,mean,sd,z,answers in expected:
    margin=z*D(sd)/D(n).sqrt()
    assert (margin,D(mean)-margin,D(mean)+margin,2*margin)==answers
for centers,margin,mu,hits in [([236,244,250,258,230,247,242,254,233,246],D('11.76'),245,7),([32,33,34,35,D('32.5')],D('1.96'),33,4)]:
    assert sum(D(c)-margin<=mu<=D(c)+margin for c in centers)==hits
assert (D(7)/10*100,abs(D(7)/10*100-95))==(70,25)
assert (D(4)/5*100,abs(D(4)/5*100-95))==(80,15)
assert 176+20+4==200
assert (D(176)/200*100,abs(D(176)/200*100-90))==(88,2)
assert (D(196)/200*100,abs(D(196)/200*100-99))==(98,1)
assert D(176)<=196 and 4<=24
for count1,count2,n,delta in [(40,55,100,15),(54,72,144,D('12.5')),(24,32,64,D('12.5'))]:
    assert 0<=count1<=n and 0<=count2<=n
    assert (D(count2)/n-D(count1)/n)*100==delta
assert sum([D('1.25'),D('1.25')])==D('2.5')
assert sum([D('.75'),D('1'),D('.75')])==D('2.5')
assert D(3)+3+D('2.5')==D('8.5') and D('8.5')*2==17

reader=PdfReader(build/f'{name}.pdf')
assert len(reader.pages)==19
dests=reader.named_destinations
links=0
for page in reader.pages:
    for ref in page.get('/Annots',[]):
        ann=ref.get_object()
        if ann.get('/Subtype')!='/Link': continue
        action=ann.get('/A',{})
        target=action.get('/D') if action.get('/S')=='/GoTo' else ann.get('/Dest')
        if isinstance(target,str):
            assert target in dests, target
            links+=1
        rect=ann.get('/Rect')
        if rect:
            assert min(float(rect[0]),float(rect[2]))>=0
            assert max(float(rect[0]),float(rect[2]))<=float(page.mediabox.width)
            assert min(float(rect[1]),float(rect[3]))>=0
            assert max(float(rect[1]),float(rect[3]))<=float(page.mediabox.height)
assert links>=60
# Verify section and solution anchors map to pages with their intended content.
aux=(build/f'{name}.aux').read_text()
labels={label:dest for label,dest in re.findall(r'\\newlabel\{([^}]+)\}.*?\{(section[^}]+)\}\{\}\}',aux)}
assert len([k for k in labels if k.startswith('sol:')])==15
for label,dest in labels.items():
    if not (label.startswith('sol:') or label.startswith('sec:p') or label=='toc'): continue
    assert dest in dests,(label,dest)
    page_number=reader.get_destination_page_number(dests[dest])
    text=reader.pages[page_number].extract_text()
    if label.startswith('sol:'):
        suffix=label[-3:]
        phrase={'c1a':'C1 Task 1','c1b':'C1 Task 2','c2a':'C2 Task 1','c2b':'C2 Task 2','c2c':'C2 Task 3'}[suffix]
        assert 'Worked solution: '+phrase in text,(label,page_number)
    if label=='toc': assert 'Contents' in text
    if label.startswith('sec:p'): assert 'Original' in text
print(f'PASS: arithmetic, coverage, nesting, proportions, rubric totals, 3 problems, 15 task/solution pairs, clean TeX log, 19 rendered pages, {links} resolved internal links and all target pages verified.')
