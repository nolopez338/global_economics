from docx import Document
p='book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx';d=Document(p)
for ti in [10,22,23]:
 for r in d.tables[ti].rows:
  for pa in r.cells[1].paragraphs:
   if pa.text.startswith(tuple(f'C{i} – ' for i in range(1,11))):pa.paragraph_format.keep_together=True
# Prevent orphaned evidence labels.
for ti in [10,22,23]:
 for r in d.tables[ti].rows:
  for pa in r.cells[1].paragraphs:
   if pa.text in ['Evidence Description:','DESCRIPCIÓN DE LA EVIDENCIA']:pa.paragraph_format.keep_with_next=True
d.save(p)
