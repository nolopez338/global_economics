from pathlib import Path
from fractions import Fraction as Q
import re, json
from collections import Counter
from pypdf import PdfReader
from PIL import Image, ImageOps, ImageDraw
base=Path('tmp/c3-revision')
script=(base/'revise.py').read_text(encoding='utf8')
ns={'Q':Q}
exec('data=['+script.split('data=[',1)[1].split('\ndef frac',1)[0],ns)
data=ns['data']
expected=[[(Q(0),Q(3,8),0),(Q(3,8),Q(1),1)],[(Q(0),Q(3,7),1),(Q(3,7),Q(1),0)],[(Q(0),Q(1,2),1),(Q(1,2),Q(1),0)],[(Q(0),Q(1,2),0),(Q(1,2),Q(1),1)],[(Q(0),Q(1,3),0),(Q(1,3),Q(2,5),1),(Q(2,5),Q(1),2)],[(Q(0),Q(2,7),0),(Q(2,7),Q(1),1)]]
expected[3]=[(Q(0),Q(2,5),0),(Q(2,5),Q(1),1)]
initial=[[56,60],[70,60],[45,60],[160,260],[Q(436,5),92,80],[80,110,80]]
report=[]
for d,intervals,ev in zip(data,expected,initial):
 alts=d['alts']
 def values(p):return [Q(a)+(b-a)*p for _,a,b in alts]
 assert values(d['p'])==ev,(d['key'],values(d['p']))
 for left,right,best in intervals:
  for p in [left+(right-left)*Q(j,20) for j in range(1,20)]:
   vals=values(p); assert vals[best]==max(vals),(d['key'],p,vals,best)
 for index in range(len(intervals)-1):
  p=intervals[index][1]; vals=values(p)
  assert vals[intervals[index][2]]==vals[intervals[index+1][2]]==max(vals)
 assert values(0)[intervals[0][2]]==max(values(0))
 assert values(1)[intervals[-1][2]]==max(values(1))
 for _,a,b in alts:
  for p in [Q(0),Q(1),d['p'],Q(1,2)]:
   masses={}
   for amount,mass in [(a,1-p),(b,p)]: masses[amount]=masses.get(amount,0)+mass
   assert sum(masses.values())==1 and all(m>=0 for m in masses.values())
   support={y for y,m in masses.items() if m>0}
   assert support==({a} if p==0 else {b} if p==1 else {a,b})
   lo,hi=sorted([a,b])
   for t in [lo-1,lo,Q(lo+hi,2),hi,hi+1]:
    actual=sum(m for y,m in masses.items() if y<=t)
    formula=(0 if t<lo else (1 if t>=hi else (1-p if a<b else p)))
    assert actual==formula
   assert sum(y*m for y,m in masses.items())==a+(b-a)*p
 report.append({'context':d['key'],'initial_expected_values':[str(v) for v in ev],'decision_intervals':[(str(l),str(r),i+1) for l,r,i in intervals]})
src=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex').read_text(encoding='utf8')
assert len(re.findall(r'\\section\{',src))==4
assert len(re.findall(r'\\QuestionsTasks\[',src))==6
assert 'Reversed indicator' not in src and 'Three sales categories' not in src
assert src.count('% \\GTenHighlightsfalse')==1
plots=re.findall(r'\\addplot\[decision\w+,domain=0:1,samples=2\]\{(-?\d+)\+(-?\d+)\*x\}',src)
assert [(int(a),int(m)) for a,m in plots]==[(a,b-a) for d in data for _,a,b in d['alts']]
pdf=PdfReader(base/'G10_T2_L1_C3_practice_activity.pdf')
names=pdf.named_destinations
links=0
for pi,page in enumerate(pdf.pages):
 for ann in page.get('/Annots',[]):
  obj=ann.get_object(); action=obj.get('/A',{})
  if action.get('/S')=='/GoTo':
   dest=action['/D']; assert dest in names,(pi,dest)
   assert 0<=pdf.get_destination_page_number(names[dest])<len(pdf.pages)
   links+=1
text='\n'.join(page.extract_text() for page in pdf.pages)
off=PdfReader(base/'off/off.pdf')
def normalized(t):return re.sub(r'\s+','',t).replace('\u00ad','')
# Highlight strokes can change line breaks and hyphenation but must preserve tokens.
ontext=normalized(text).replace('-','')
offtext=normalized('\n'.join(page.extract_text() for page in off.pages)).replace('-','')
assert Counter(ontext)==Counter(offtext),'Enabled/disabled content differs'
# Page numbers may move with the narrower disabled strokes; compare mathematical/content text by words below.
print('Enabled/disabled pages:',len(pdf.pages),len(off.pages))
for token in ['Bernoulli','favorable','dominated','right-continuous','PMF','CDF']:
 assert token in text and token in '\n'.join(p.extract_text() for p in off.pages)
print('Verified',links,'internal links; all destinations exist.')
print('Pages:',[(i+1,p.extract_text().splitlines()[0].encode('ascii','replace').decode()) for i,p in enumerate(pdf.pages)])
(base/'verification.json').write_text(json.dumps({'math':report,'pages':len(pdf.pages),'internal_links':links},indent=2))
imgs=sorted(base.glob('page-*.png'))
for start in range(0,len(imgs),6):
 canvas=Image.new('RGB',(1000,2100),'#ddd'); draw=ImageDraw.Draw(canvas)
 for j,path in enumerate(imgs[start:start+6]):
  im=Image.open(path).convert('RGB'); im.thumbnail((490,670))
  x=(j%2)*500+(500-im.width)//2; y=(j//2)*700+25
  canvas.paste(im,(x,y)); draw.text((x,y-19),path.stem,fill='black')
 canvas.save(base/f'contact-{start//6+1}.png')
print('Mathematical and graph checks passed for all six contexts.')
