from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex');s=p.read_text()
s=s.replace('Count kept; adjusted payout in USD.','Counts; adjusted payout in USD.')
# Q2's grouped table: numerical totals, ordered outcomes, probabilities.
a=s.index('The complete mapping and grouped');b=s.index('\\end{tabular}',a)
t=s[a:b];ls=t.splitlines()
for i,l in enumerate(ls):
 if ' & ' in l:
  c=l.split(' & ');c[0]=c[0].replace('GTenHLOutcome','GTenHLValue');c[1]=c[1].replace('GTenHLProbability','GTenHLOutcome');ls[i]=' & '.join(c)
s=s[:a]+'\n'.join(ls)+s[b:]
lines=s.splitlines();task=0;question=0;display=False
for i,l in enumerate(lines):
 m=re.search(r'\\sectionScored.*\{sec:q(\d)\}',l)
 if m:question=int(m[1])
 m=re.search(r'\\label\{sol:q\dt(\d)\}',l)
 if m:task=int(m[1])
 if '\\[' in l:display=True
 if '\\]' in l:display=False
 if task==3 and display and l.startswith('='):
  l=l.replace('GTenHLValue','GTenHLProbability').replace('GTenHLParameter','GTenHLProbability')
 if 'Exhaustiveness check:' in l:l=l.replace('GTenHLValue','GTenHLProbability')
 if '\\item Range: all tabulated heights' in l:l=l.replace('GTenHLValue','HLCumulativeProbability')
 if 'Jump--mass agreement:' in l:
  # The differenced numerators are masses; the F notation remains cumulative.
  l=re.sub(r'\\HLCumulativeProbability\{(\d+)\}',r'\\GTenHLProbability{\1}',l)
 if question==6:
  if '\\binom{' in l and not ' & ' in l:
   l=re.sub(r'\\GTenHLValue\{(\d+)\}',r'\1',l)
  if 'Feasible counts satisfy' in l:
   l=re.sub(r'\\(?:GTenHLValue|GTenHLProbability)\{(\d+)\}',r'\1',l)
  if 'Label the physical tickets' in l:
   l=re.sub(r'([ZLH])_\\GTenHLValue\{(\d+)\}',r'\\GTenHLOutcome{\1_\2}',l)
  if 'N(a,b,c)' in l:
   # The composition count is not the number of kept orders.
   l=l.replace(r'\GTenHLSecond{N}(a,b,c)',r'N(a,b,c)')
 # Keep the original heading with the beginning of its checks.
 if '\\textbf{PMF checks.}' in l:
  l=l.replace(r'\textbf{PMF checks.}',r'\Needspace{5\baselineskip}\textbf{PMF checks.}')
 lines[i]=l
s='\n'.join(lines)+'\n';p.write_text(s)
Path('tmp/g10-solution-update/disabled.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'))
