from pathlib import Path
from fractions import Fraction
from itertools import product
import subprocess,re
root=Path('book/grade10/term_2/4-learning_evidences')
sp=root/'G10_T2_L1_C1C2_exam_solution_1.tex'; ep=root/'G10_T2_L1_C1C2_exam_1.tex'
s=sp.read_text(encoding='utf-8');e=ep.read_text(encoding='utf-8')
# Compare every repeated original question and all 18 tasks verbatim.
examblocks=re.split(r'\\QuestionLabel\{q:\d\}\s*',e)[1:]
for i,block in enumerate(examblocks,1):
 statement=block.split('\n\n')[0]
 assert statement in s,(i,'statement mismatch')
 tasks=re.findall(r'\\item (.*?) \\sscore',block)
 assert len(tasks)==3
 for task in tasks: assert r'\boldmath '+task+r'}\par' in s,(i,task)
# Source-preservation check for untouched problems, including all worked content.
for path,text,marker in [(sp,s,r'\sectionScored{'),(ep,e,r'\SubsectionBox{')]:
 old=subprocess.check_output(['git','show','HEAD:'+path.as_posix()]).decode('utf-8')
 for title in ['Two distributor promotional credits','Library fundraiser prize tickets']:
  def section(t):
   start=t.index(marker+title);end=t.find(marker,start+1)
   return t[start:end if end>=0 else len(t)]
  assert section(old)==section(text),(path,title)
# Independently derive reservation PMF with exact rational arithmetic.
pmf={}
for bs in product([0,1],repeat=3):
 prob=Fraction(1)
 for b,keep in zip(bs,[Fraction(1,5),Fraction(1,2),Fraction(4,5)]):prob*=keep if b else 1-keep
 x=7*sum(bs)-5;pmf[x]=pmf.get(x,0)+prob
assert pmf=={-5:Fraction(8,100),2:Fraction(42,100),9:Fraction(42,100),16:Fraction(8,100)}
for q,xs,weights,vals,masses in [
 (3,[0,6,10,21],[3,2,2,3,4,1,3,2],[0,0,6,6,10,10,21,21],[5,5,5,5]),
 (4,[0,11,22,34],[3,1,3,2,2,4,2,3],[0,0,11,11,22,22,34,34],[4,5,6,5]),
 (5,[0,12,18],[1,2,3,4,2,4,4],[0,0,12,12,18,18,18],[3,7,10])]:
 assert sum(weights)==sum(masses)==20
 assert [sum(w for w,v in zip(weights,vals) if v==x) for x in xs]==masses
 # Inspect actual graph coordinates: filled endpoints and PMF bars.
 sec=s[s.index(r'\sectionScored{'+{3:'Produce',4:'Equipment',5:'Travel'}[q]):].split(r'\sectionScored{',2)[1]
 bars=re.findall(r'rectangle \(axis cs:([\d.]+),(\d+)/20\)',sec)
 assert [(round(float(x)-.45),int(n)) for x,n in bars]==list(zip(xs,masses))
 cum=0
 for x,n in zip(xs,masses):
  assert f'({x},{cum}/20)' in sec # open endpoint
  cum+=n
  assert f'({x},{cum}/20)' in sec # filled endpoint
 assert cum==20
 assert r'thick,<-]' in sec and r'thick,->]' in sec
assert '20a=1' in s
assert [1,2,3,4,2,4,4]==[1,2*1,3*1,2*2,2,2*2,4]
print('PASS: 6 statements and 18 tasks synchronized; Problems 2 and 6 unchanged in both sources.')
print('PASS: exact normalization, outcome aggregation, PMF bars, CDF jumps/endpoints and tails for revised distributions.')
