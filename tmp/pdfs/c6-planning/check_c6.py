from pathlib import Path
from pypdf import PdfReader
from collections import Counter
import re
base=Path('tmp/pdfs/c6-planning')
a=PdfReader(base/'build/G11_T2_L2_C6_practice.pdf');b=PdfReader(base/'off-build/nohighlights.pdf')
# This activity's eight adjacent-integer decisions, checked directly against the inequalities.
from statistics import NormalDist
from math import sqrt
D=NormalDist(); z95=D.inv_cdf(.975); z90=D.inv_cdf(.95)
cases=[('mean SE',144,1,1.5,64),('proportion SE',.16,1,.025,256),('mean margin',144,z95,3,62),('proportion margin',.16,z95,.04,385),('mean width',225,2*z90,5,98),('proportion width',.25,2*z95,.06,1068),('mean confidence',144,z95,2,139),('proportion confidence',.21,z90,.03,632)]
for name,v,k,cap,n in cases:
    good=k*sqrt(v/n); bad=k*sqrt(v/(n-1))
    assert good<=cap and bad>cap,(name,good,bad)
    print(name,n,'passes',good,'previous fails',bad)
for n,v,e,c0 in [(139,144,2,.95),(632,.21,.03,.9)]:
    good=2*D.cdf(e*sqrt(n/v))-1;bad=2*D.cdf(e*sqrt((n-1)/v))-1
    assert good>=c0 and bad<c0
    print('Confidence',n,good,'previous',bad)
s=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L2_C6_practice.tex').read_text()
assert re.findall(r'\\section\{([^}]+)\}',s)==['Introduction','Notation Reference and Practice Procedure','General Worked Problems','Advanced Problems']
labels=re.findall(r'\\label\{([^}]+)\}',s);assert len(labels)==len(set(labels))
assert s.count('\\subsubsection*{Worked solution (C6)}')==8
assert s.count('% \\GTenHighlightsfalse')==1
print('Structure, eight core solutions, unique labels, original toggle: PASS')
# Compare the full extracted content as a multiset of non-whitespace characters:
# line wrapping, word spacing and physical page numbers can differ when markers are off.
t1=''.join(p.extract_text() for p in a.pages);t2=''.join(p.extract_text() for p in b.pages)
c1=Counter(re.sub(r'\s','',t1));c2=Counter(re.sub(r'\s','',t2))
print('Enabled pages',len(a.pages),'disabled pages',len(b.pages))
print('Text character differences',dict(c1-c2),dict(c2-c1))
assert dict(c1-c2)=={'s':5,'!':3} and dict(c2-c1)=={'r':5,'\x12':3,'\x13':3}
print('Only the visually checked square-root and large-parenthesis font extraction differences remain; all other content agrees: PASS')

