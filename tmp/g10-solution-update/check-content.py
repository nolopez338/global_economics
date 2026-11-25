from pathlib import Path
import re
orig=Path('tmp/g10-solution-update/original.tex').read_text()
s=Path('book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex').read_text()
# Exact credit allocations and totals, independent of semantic markup.
pat=r'\\textbf\{Proposed partial credit\.\}(.*?)\\end\{minipage\}'
a=re.findall(pat,orig,re.S);b=re.findall(pat,s,re.S)
assert len(a)==len(b)==18
for x,y in zip(a,b):
 assert re.findall(r' & (.*?)\\\\',x)==re.findall(r' & (.*?)\\\\',y)
assert re.findall(r'\\label\{[^}]+\}',orig)==[x for x in re.findall(r'\\label\{[^}]+\}',s) if x!=r'\label{tab:highlight-legend}']
variant=s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment')
Path('tmp/g10-solution-update/disabled.tex').write_text(variant)
print('PASS: all 18 credit allocations/totals and all original navigation labels preserved. Context/instruction checks already passed.')
