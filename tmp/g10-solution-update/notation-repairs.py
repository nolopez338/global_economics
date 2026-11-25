from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex');s=p.read_text()
s=re.sub(r'([ZLH])_\{\\GTenHLValue\{(\d+)\}\}',r'\\GTenHLOutcome{\1_\2}',s)
s=re.sub(r'\\binom\{\\GTenHLProbability\{(\d+)\}\}',r'\\binom{\1}',s)
s=s.replace(r'^{\GTenHLProbability{3}}',r'^{3}')
ls=s.splitlines()
for i,l in enumerate(ls):
 if l.startswith(r'\GTenHLParameter{a}+'):
  ls[i]=l.replace(r'\GTenHLParameter{1}',r'\GTenHLProbability{1}')
s='\n'.join(ls)+'\n';p.write_text(s)
Path('tmp/g10-solution-update/disabled.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'))
