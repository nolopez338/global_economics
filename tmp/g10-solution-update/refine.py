from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex')
s=p.read_text()
# Complete category names and standalone letters are outcomes, not amounts.
s=s.replace('Write $K$ for kept and $C$ for cancelled.',r'Write $\GTenHLOutcome{K}$ for \GTenHLOutcome{kept} and $\GTenHLOutcome{C}$ for \GTenHLOutcome{cancelled}.')
s=s.replace('cargo '+r'\GTenHLOutcome{bicycle}',r'\GTenHLOutcome{cargo bicycle}')
# Count-only expressions have no monetary units. Leave them unmarked instead
# of suggesting they are dollar values; composition labels share outcome ink.
lines=s.splitlines(); countdisplay=False
for i,l in enumerate(lines):
 if any(t in l for t in ['There are $','giving $','Their counts sum to','Feasible counts satisfy','The number of subsets','equally likely unordered subsets']):
  l=re.sub(r'\\GTenHLValue\{([^{}]+)\}',r'\1',l)
 if '\\binom{9}' in l:
  l=re.sub(r'\\GTenHLValue\{([^{}]+)\}',r'\1',l)
 if ' & ' in l and '\\binom4' in l:
  l=re.sub(r' & (\d+)(\\\\)$',r' & $\\GTenHLValue{\1}$\2',l)
 if 'Likelihood relationships: the numerators' in l:
  l=l.replace('GTenHLValue','GTenHLProbability')
 # Constants multiplying the unknown a are unmarked; the unknown itself and
 # its solved value retain the shared unknown-parameter treatment.
 l=re.sub(r'\\GTenHLProbability\{(\d+|\\tfrac12)\}(?=\\GTenHLParameter|\(\\GTenHLProbability)',r'\1',l)
 l=re.sub(r'\\GTenHLParameter\{(\d+)\}(?=\\GTenHLParameter)',r'\1',l)
 # Consistent units in prose, including mathematical support statements.
 if i>90 and not any(x in l for x in ['\\CreditDescription','\\sectionScored','\\subsection','\\begin{axis}']):
  l=re.sub(r'(?<![A-Za-z{])USD(?![A-Za-z}])',r'\\GTenHLValue{USD}',l)
 # Plain percentages in conclusions remain visibly probability quantities.
 l=re.sub(r'(?<![\w.{])\d+(?:\.\d+)?\\%',lambda m:r'\GTenHLProbability{'+m[0]+'}',l)
 lines[i]=l
s='\n'.join(lines)+'\n'
p.write_text(s)
# The key is the governing source. Check context and instruction text after
# removing only the new semantic/formatting wrappers.
orig=Path('tmp/g10-solution-update/original.tex').read_text()
def plain(t):
 # Remove single-argument semantic macros using balanced braces.
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
for q in range(1,7):
 for t in range(1,4):
  pat=rf'\\label\{{sol:q{q}t{t}\}}\n\n([^\n]+)'
  assert plain(re.search(pat,orig)[1])==plain(re.search(pat,s)[1]),(q,t)
oldrows=re.findall(r'(?m)^([^\n]+ & [\d.]+)\\\\$',orig)
newrows=re.findall(r'(?m)^([^\n]+ & [\d.]+)\\\\$',s)
assert [plain(x) for x in oldrows]==[plain(x) for x in newrows]
assert re.findall(r'\\label\{[^}]+\}',orig)==[x for x in re.findall(r'\\label\{[^}]+\}',s) if x!=r'\label{tab:highlight-legend}']
print('PASS: 6 verbatim contexts, 18 verbatim instructions, scoring rows and all original labels preserved.')
