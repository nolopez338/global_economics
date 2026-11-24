from pathlib import Path
from fractions import Fraction as F
import re
import pypdfium2 as pdfium
from PIL import ImageChops
base=Path('tmp/c3-writing-boxes-20261124')
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex')
old=(base/'baseline.tex').read_text(encoding='utf-8')
new=p.read_text(encoding='utf-8')
wmark=r'\stageheading{Worked example}'
gmark=r'\stageheading{Guided Example}'
imark=r'\stageheading{Independent Practice}'
assert old[:old.index(wmark)]==new[:new.index(r'\begingroup'+'\n% Positive spacing')]
assert old[old.index(imark):]==new[new.index(imark):]
def content(s):
    s=re.sub(r'%[^\n]*','',s)
    s=re.sub(r'\\setlength\{\\[^}]+\}\{[^}]+\}|\\(?:vspace|Needspace)\{[^}]+\}|\\(?:begingroup|endgroup|clearpage|par)\b','',s)
    return re.sub(r'\s+','',s)
assert content(old[old.index(wmark):old.index(gmark)])==content(new[new.index(wmark):new.index(gmark)])
guided=new[new.index(gmark):new.index(imark)]
assert len(re.findall(r'\\underline',guided))==1 # local bold subtask heading helper only
assert not re.search(r'\\vspace\{-|\\(?:small|footnotesize|scriptsize|resizebox|scalebox)\b',guided)
assert len(re.findall(r'\\calcblank\b',old[old.index(gmark):old.index(imark)]))==len(re.findall(r'\\calcblank\b',guided))-1+2 # 2 short blanks promoted to fraction boxes
# Independent private arithmetic, supports and sorted cumulative masses.
prob=F(2,7)
for lo,hi,mean,root in [(-24,72,F(24,7),F(1,4)),(-54,126,F(-18,7),F(3,10))]:
    slope=hi-lo
    assert (1-prob)*lo+prob*hi==mean
    assert F(-lo,slope)==root
    assert lo+slope*root==0
    assert (1-prob)+prob==1
    assert lo<0<hi
    assert lo+slope*(root/2)<0<lo+slope*((1+root)/2)
    assert lo+slope*0==lo and lo+slope==hi
before=pdfium.PdfDocument(base/'baseline.pdf')
after=pdfium.PdfDocument(base/'build/G10_T2_L1_C3_classroom_activity.pdf')
assert len(after)==6
texts=[page.get_textpage().get_text_range() for page in after]
assert 'Checks.' in texts[2] and 'Guided Example' not in texts[2]
assert texts[3].startswith('Guided Example') and 'Task 1' in texts[3]
assert 'Task 2' in texts[4] and 'At break-even' in texts[4]
assert texts[5].startswith('Independent Practice')
for page in after:
    assert tuple(round(x) for x in page.get_size())==(612,792)
assert ImageChops.difference(before[5].render(scale=1.5).to_pil(),after[5].render(scale=1.5).to_pil()).getbbox() is None
print('PASS: unchanged surrounding source, worked content, independent page pixels; six-page distribution; letter size; private guided arithmetic.')
print('Page 3 opening:',repr(texts[2][:100]))
