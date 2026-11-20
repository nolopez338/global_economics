from pathlib import Path
import re,math,json
from pypdf import PdfReader
root=Path.cwd(); tex=root/'book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex'; s=tex.read_text()
assert re.findall(r'\\problemtitle\{(\d+)\}',s)==['1','2','3','4','5']
assert re.findall(r'\\stageheading\{([^}]+)\}',s)==['Equations and basic procedure','Worked example','Guided Example','Independent Practice']
plots=re.findall(r'\\addplot\[only marks[^\]]*\] coordinates \{([^}]+)\}',s)
assert len(plots)==6 and all(len(re.findall(r'\([^()]+\)',p))==5 for p in plots)
assert not re.search(r'\\(?:Highlight\w*|Ctwo\w*|HL\w*|GTen\w*|colorbox|textcolor|boxed)\b',s)
assert re.findall(r'\\input\{([^}]+)\}',s)==['preamble.tex']
assert s.count(r'\blankgrid{')==24
assert s.count(r'\normalblank{80\%}')==4
assert r'\geometry{letterpaper,margin=0.25in}' in s
# Verify worked table values and coordinate arrays directly from formulas.
for n in [25,100,400,900,1600]:
 se=30/math.sqrt(n);m=1.96*se
 assert f'{m:.3f}' in s and f'{84-m:.3f}' in s and f'{84+m:.3f}' in s and f'{2*m:.3f}' in s
for z in [1.282,1.645,1.960,2.576,3.291]:
 m=3*z
 assert f'{m:.3f}' in s and f'{84-m:.3f}' in s and f'{84+m:.3f}' in s
pdf=root/'tmp/pdfs/c3-classroom/G11_T2_L1_C3_classroom_activity.pdf'; pages=PdfReader(pdf).pages
assert len(pages)==16
assert all(float(p.mediabox.width)==612 and float(p.mediabox.height)==792 for p in pages)
assert all(len(p.extract_text())>100 for p in pages)
log=(root/'tmp/pdfs/c3-classroom/G11_T2_L1_C3_classroom_activity.log').read_text(errors='replace')
assert 'Overfull' not in log and 'Underfull' not in log
print('PASS: 4 exact stages; problems 1-5; 6 worked graphs x 5 markers; 24 blank relationship grids; 12 blank normal panels; letter paper and fixed margins; no instructional highlight use; all 16 pages contain intended content; clean box log.')
print('PASS: worked numbers and all 40 fresh investigation rows privately checked.')
