from docx import Document
from pathlib import Path
from docx.oxml.ns import qn
p=Path('book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx');d=Document(p)
for i,s in enumerate(d.sections):print('SECTION',i,s.start_type)
for ti in [10,22,23]:
 for r in d.tables[ti].rows:
  for el in r._tr.trPr.findall(qn('w:cantSplit')):r._tr.trPr.remove(el)
# Keep the institutional Experience heading with its first action.
for ti in [9,21]:
 for c in d.tables[ti].rows[0].cells:
  for pa in c.paragraphs:pa.paragraph_format.keep_with_next=True
# Preserve blank reference fields as one unit rather than spilling a blank row.
for r in d.tables[11].rows:
 for c in r.cells:
  for pa in c.paragraphs:pa.paragraph_format.keep_with_next=True
# Empty trailing paragraphs should occupy minimal space, avoiding a blank terminal page.
from docx.shared import Pt
for pa in reversed(d.paragraphs):
 if pa.text or pa._p.xpath('.//w:sectPr'):break
 pa.paragraph_format.space_before=Pt(0);pa.paragraph_format.space_after=Pt(0);pa.paragraph_format.line_spacing=Pt(1)
 for run in pa.runs:run.font.size=Pt(1)
d.save(p)
