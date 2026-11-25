from pathlib import Path
import re
orig=Path('tmp/g10-solution-update/original.tex').read_text();s=Path('book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex').read_text()
def plain(t):
 pat=re.compile(r'\\(?:GTenHL(?:Value|Second|Third|Outcome|Probability|Parameter)|HLCumulativeProbability|CreditDescription|textbf)\{')
 while (m:=pat.search(t)):
  pos=m.end();depth=1;j=pos
  while depth:
   if t[j]=='{':depth+=1
   if t[j]=='}':depth-=1
   j+=1
  t=t[:m.start()]+t[pos:j-1]+t[j:]
 return re.sub(r'\\(?:boldmath|noindent|par|nopagebreak)\b','',t).strip()
for q in range(1,7):
 pat=rf'\\sectionScored[^\n]+\{{sec:q{q}\}}\n\n(.*?)\n\n'
 assert plain(re.search(pat,orig,re.S)[1])==plain(re.search(pat,s,re.S)[1]),q
 for t in range(1,4):
  pat=rf'\\label\{{sol:q{q}t{t}\}}\n\n([^\n]+)'
  assert plain(re.search(pat,orig)[1])==plain(re.search(pat,s)[1]),(q,t)
pat=r'\\textbf\{Proposed partial credit\.\}(.*?)\\end\{minipage\}'
a=re.findall(pat,orig,re.S);b=re.findall(pat,s,re.S)
assert len(a)==len(b)==18
for x,y in zip(a,b):
 assert re.findall(r' & (.*?)\\\\',x)==re.findall(r' & (.*?)\\\\',y)
 assert [plain(z) for z in re.findall(r'([^\n]+) & ',x)]==[plain(z) for z in re.findall(r'([^\n]+) & ',y)]
assert re.findall(r'\\label\{[^}]+\}',orig)==[x for x in re.findall(r'\\label\{[^}]+\}',s) if x!=r'\label{tab:highlight-legend}']
print('PASS: final contexts, instructions, all credit descriptions/allocations/totals, and original labels.')
