from pathlib import Path
from docx import Document
from pypdf import PdfReader
p=Path('book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx');d=Document(p)
print('BASELINE PAGES',len(PdfReader('tmp/term2_plan/baseline.pdf').pages))
for ti,ri in [(10,0),(22,0),(23,0)]:
 c=d.tables[ti].rows[ri].cells[1]
 for j,p in enumerate(c.paragraphs):
  print(ti,j,repr(p.text[:110]),'font',[(r.font.name,r.font.size.pt if r.font.size else None) for r in p.runs[:2]],'spacing',p.paragraph_format.space_after,'keep',p.paragraph_format.keep_with_next)
print('rows',[(i,[r._tr.xml[:100] for r in t.rows[:1]]) for i,t in enumerate(d.tables) if i in (10,22,23)])
