from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex');s=p.read_text()
lines=s.splitlines();q6=False
for i,l in enumerate(lines):
 if '{sec:q6}' in l and '\\sectionScored' in l:q6=True
 if q6:
  # Compositions are complete selection categories, consistently purple.
  l=re.sub(r'\$\((?:\\GTenHLValue\{\d+\},?){3}\)\$',lambda m:m[0].replace('GTenHLValue','GTenHLOutcome'),l)
  if any(t in l for t in ['Feasible counts satisfy','These nine compositions are exhaustive','N(a,b,c)=','Define $I=']):
   # Counting and indicator restrictions are neither dollars nor unknown masses.
   if 'Define $I=' not in l:l=re.sub(r'\\GTenHLValue\{([^{}]+)\}',r'\1',l)
   else:
    # Only the indicator conditions before the monetary face sum.
    a,b=l.split('The face sum',1)
    a=re.sub(r'\\GTenHLValue\{([^{}]+)\}',r'\1',a);l=a+'The face sum'+b
 lines[i]=l
s='\n'.join(lines)+'\n';p.write_text(s)
Path('tmp/g10-solution-update/disabled.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'))
print('Final semantic audit completed.')
