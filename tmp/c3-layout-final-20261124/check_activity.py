from pathlib import Path
from fractions import Fraction as Q
import re
import pypdfium2 as pdfium
root=Path(__file__).resolve().parents[2]
base=Path(__file__).parent
p=root/'book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex'
old=(base/'baseline.tex').read_text()
new=p.read_text()
start=r'\stageheading{Worked example}'
guided=r'\stageheading{Guided Example}'
independent=r'\stageheading{Independent Practice}'
assert new[:new.index(r'\begingroup',new.index(r'\end{minipage}\par',new.index(r'\stageheading{General tasks}'))) ] == old[:old.index(start)]
assert old[old.index(independent):] == new[new.index(independent):]
def content(x):
    x=re.sub(r'\\(?:vspace|Needspace)\{[^}]*\}', '',x)
    x=re.sub(r'\\(?:newpage|clearpage|par|endgroup)\b', '',x)
    return re.sub(r'\s+', '',x)
assert content(old[old.index(start):old.index(guided)]) == content(new[new.index(start):new.index(guided)])
g=new[new.index(guided):new.index(independent)]
assert r'\underline{\hspace' not in g
assert r'\responseline' not in g
assert not re.search(r'\\vspace\{-',new[new.index(start):new.index(independent)])
assert len(re.findall(r'\\subtaskheading\{[123]\}',g))==6
assert r'\geometry{letterpaper,margin=0.25in}' in new
assert r'\documentclass[11pt]{article}' in (root/'book2026-2027/preamble/preamble.tex').read_text()
for f0,f1,expect,zero in [(-24,72,Q(24,7),Q(1,4)),(-54,126,Q(-18,7),Q(3,10))]:
    slope=f1-f0
    assert Q(f0)+slope*Q(2,7)==expect
    assert -Q(f0,slope)==zero
    assert f0+slope*zero==0
    assert Q(5,7)+Q(2,7)==1
    assert f0<0<f1
    for t,want in [(zero/2,-1),((zero+1)/2,1)]:
        assert (f0+slope*t)*want>0
doc=pdfium.PdfDocument(base/'build/G10_T2_L1_C3_classroom_activity.pdf')
before=pdfium.PdfDocument(base/'baseline.pdf')
assert len(doc)==6
text=[page.get_textpage().get_text_range() for page in doc]
assert 'Guided Example' in text[3]
assert 'Independent Practice' in text[5]
assert 'break-even, the long-run average' in text[2]
assert 'realized payoff' in text[4]
assert 'Guided Example' not in text[2]
for i in [5]:
    assert doc[i].render(scale=1).to_pil().tobytes()==before[i].render(scale=1).to_pil().tobytes(),f'Page {i+1} rendering changed'
print('PASS: six pages; section pagination; worked content and sequence; unchanged prefix and independent source; identical independent page 6; guided response and heading checks; private rational arithmetic.')


