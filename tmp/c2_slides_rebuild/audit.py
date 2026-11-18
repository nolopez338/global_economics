from pathlib import Path
import re
from decimal import Decimal
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex').read_text(encoding='utf8')
s=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex').read_text(encoding='utf8')
def unwrap(t):
 pat=re.compile(r'\\Ctwo(?:Confidence|Critical|SE|SD|Size|MoE|Endpoint|Point|CI|Width|Significance|Coverage)\{')
 while (m:=pat.search(t)):
  j=m.end(); depth=1
  while depth:
   if t[j]=='{':depth+=1
   elif t[j]=='}':depth-=1
   j+=1
  t=t[:m.start()]+t[m.end():j-1]+t[j:]
 return t

def legendbodies(t):
 return re.findall(r'\\toprule\s*\\textbf\{Symbol\} & \\textbf\{Concept\} & \\textbf\{Formula\}(.*?)\\bottomrule',t,re.S)[:2]
def norm(t):return re.sub(r'\s+','',re.sub(r'\[\d+pt\]','',unwrap(t)))
a,b=legendbodies(p),legendbodies(s)
assert len(a)==len(b)==2
assert [norm(x) for x in a]==[norm(x) for x in b], 'legend mismatch'
assert s.count(r'\BothLegends')==3 # definition + opening + closing
assert Decimal('1.960')*Decimal(14)/Decimal(49).sqrt()==Decimal('3.920')
assert Decimal(40)-Decimal('3.92')==Decimal('36.08')
assert Decimal(40)+Decimal('3.92')==Decimal('43.92')
assert Decimal('43.92')-Decimal('36.08')==Decimal('7.84')
assert sum(Decimal(l)<=41<=Decimal(u) for l,u in [('36.08','43.92'),('38.08','45.92'),('41.08','48.92'),('34.08','41.92'),('37.08','44.92')])==4
assert 'household' not in s.lower()
assert r'\mu_{\rm sim}' not in s and r'\mu_{\mathrm{sim}}' not in s
assert s.count(r'% \GTenHighlightsfalse % Uncomment')==1
assert r'\input{' not in s
print('PASS: exact legend row content, formulas, blanks and division; shared reuse; mathematics; standalone source; preserved enabled toggle.')
