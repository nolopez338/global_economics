from docx import Document
p='book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx';d=Document(p)
for ti in [10,22,23]:
 for r in d.tables[ti].rows:
  for c in r.cells:
   for pa in c.paragraphs[:4]:pa.paragraph_format.keep_with_next=None
# Keep only each action's opening description with its first criterion.
for ti in [10,22,23]:
 for r in d.tables[ti].rows:r.cells[1].paragraphs[3].paragraph_format.keep_with_next=True
d.save(p)
