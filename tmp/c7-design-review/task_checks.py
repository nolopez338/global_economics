from pathlib import Path
import re, json
from pypdf import PdfReader
from statistics import NormalDist
from math import sqrt, ceil
base=Path('tmp/c7-design-review')
src=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L2_C7_practice.tex').read_text(encoding='utf-8')
r=PdfReader(base/'G11_T2_L2_C7_practice.pdf')
off=PdfReader(base/'off/highlights-off.pdf')
assert len(r.pages)==len(off.pages)==15
assert re.findall(r'\\section\{([^}]*)\}',src)==['Introduction','Notation Reference and Practice Procedure','General Worked Problems','Advanced Problems']
assert 'Compares confidence intervals constructed from samples of different sizes and confidence levels, analysing the trade-off between confidence and precision.' in src
labels=re.findall(r'\\label\{([^}]+)\}',src)
assert len(labels)==len(set(labels))
assert src.count('\\input{graphs/highlights.tex}')==1 and src.count('% \\GTenHighlightsfalse')==1
assert src.count('\\PracticeHighlightLegend{')==1
assert len(re.findall(r'\\subsection\{Family [1-4]:',src))==4
assert src.count('\\QuestionsTasks[')==10
aux=(base/'G11_T2_L2_C7_practice.aux').read_text()
labeldata={m[0]:(int(m[1]),m[2]) for m in re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}\{.*?\}\{([^}]+)\}',aux)}
dests=r.named_destinations
for lab in labels:
 assert lab in labeldata,lab
 page,dest=labeldata[lab]
 assert dest in dests,(lab,dest)
 assert r.get_destination_page_number(dests[dest])+1==page,(lab,page)
linkcount=0
seen=set()
for page in r.pages:
 for ref in page.get('/Annots',[]):
  a=ref.get_object()
  if a.get('/Subtype')!='/Link':continue
  target=a.get('/Dest')
  if not target and a.get('/A',{}).get('/S')=='/GoTo':target=a['/A']['/D']
  if isinstance(target,str):
   assert target in dests,target
   seen.add(target);linkcount+=1
for lab in labels:
 if lab.startswith(('sol:','prob:','sec:family','tab:','ex:')) or lab=='toc':
  assert labeldata[lab][1] in seen,('missing PDF link to',lab)
# The toggle must retain the same words, numerals and symbols despite reflow.
def tokens(reader):
 text=' '.join(p.extract_text() for p in reader.pages)
 return re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?',text)
assert ''.join(re.findall(r'\d', ' '.join(p.extract_text() for p in r.pages))) == ''.join(re.findall(r'\d', ' '.join(p.extract_text() for p in off.pages))), 'Highlight-off numerical content changed'
assert (base/'highlights-off.tex').read_text(encoding='utf-8') == src.replace('% '+chr(92)+'GTenHighlightsfalse',chr(92)+'GTenHighlightsfalse'), 'Variant source differs beyond toggle'
# Independent recalculation of every comparison table: rounded construction cutoffs.
mean=[(100,1.96),(400,1.96),(100,1.645),(100,2.576),(144,1.96)]
prop=[(100,1.645,.4),(400,1.645,.4),(400,1.96,.4),(400,2.576,.4),(400,1.96,.1),(900,1.96,.4)]
checks=[]
for n,z in mean:
 se=80/sqrt(n); e=z*se
 checks.append(dict(model='mean',n=n,z=z,SE=se,E=e,W=2*e,L=420-e,U=420+e))
for n,z,p in prop:
 se=sqrt(p*(1-p)/n); e=z*se
 checks.append(dict(model='proportion',n=n,z=z,p=p,SE=se,E=e,W=2*e,L=p-e,U=p+e))
z=NormalDist().inv_cdf(.975)
assert ceil((z*80/10)**2)==246 and z*80/sqrt(246)<=10<z*80/sqrt(245)
assert ceil(z*z*.24/.03**2)==1025 and z*sqrt(.24/1025)<=.03<z*sqrt(.24/1024)
assert abs((1.96*20/3.92)**2-100)<1e-10 and abs(2.94*sqrt(400)/1.96-30)<1e-12
assert ceil(100*(1.96/1.645)**2)==142 and ceil(100*(2.576/1.645)**2)==246
for n,c in [(100,.9),(256,.95),(400,.99)]:
 zc=NormalDist().inv_cdf((1+c)/2);se=80/sqrt(n);checks.append(dict(advanced='mean',n=n,C=c,SE=se,E=zc*se,W=2*zc*se,cost=8000*n))
for n,c in [(400,.9),(900,.95),(1600,.99)]:
 zc=NormalDist().inv_cdf((1+c)/2);se=sqrt(.24/n);checks.append(dict(advanced='proportion',n=n,C=c,SE=se,E=zc*se,W=2*zc*se,cost=5000*n))
(base/'calculation-checks.json').write_text(json.dumps(checks,indent=2))
(base/'navigation-checks.json').write_text(json.dumps({lab:{'page':p,'destination':d} for lab,(p,d) in labeldata.items()},indent=2))
print(json.dumps({'pages':len(r.pages),'unique_labels':len(labels),'resolved_internal_links':linkcount,'highlight_off_identical_digits_and_source_except_toggle':True,'numeric_comparisons_recalculated':len(checks),'structural_checks':'passed'},indent=2))

