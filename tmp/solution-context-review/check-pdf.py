from pathlib import Path
from pypdf import PdfReader
import re
root=Path('tmp/solution-context-review')
r=PdfReader(root/'disabled/disabled.pdf')
aux=(root/'disabled/disabled.aux').read_text()
destinations={m[1]:m[2] for m in re.finditer(r'\\newlabel\{([^}]+)\}[^\n]*?\{(section[^}]+)\}\{\}\}',aux)}
s=Path('book2026-2027/grade11/term_2/4-learning_evidences/G11_T2_L1_C1C2_exam_solution.tex').read_text(encoding='utf-8')
for label in ['toc','sec:p1','sec:p2','sec:p3']+[f'sol:p{i}{task}' for i in range(1,4) for task in ['c1a','c1b','c2a','c2b','c2c']]:
 assert destinations[label] in r.named_destinations, label
 dest=r.named_destinations[destinations[label]]
 page=r.get_destination_page_number(dest)
 assert 0<=page<len(r.pages)
print('All 19 contents, problem and worked-task destinations resolve.')
for i in [1,2,3]:
 dest=r.named_destinations[destinations[f'sol:p{i}c2a']]; page=r.get_destination_page_number(dest)
 text=r.pages[page].extract_text()
 for heading in ['Population parameters','Sample statistics','Procedure settings']:
  assert heading in text,(i,heading)
print('Each detailed C2 table remains together on its worked-task page in the disabled build.')
print('SE checks:',60/(100**.5),36/(144**.5),8/(64**.5))
