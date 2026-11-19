from docx import Document
from lxml import etree
D=Document('book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx')
def props(e):return [(etree.QName(x).localname,dict(x.attrib)) for x in e] if e is not None else []
for i,t in enumerate(D.tables):
 if i in [9,10,11,21,22,23,24]:print('TABLE',i,'trpr',[props(r._tr.trPr) for r in t.rows])
for i,p in enumerate(D.paragraphs):print('P',i,repr(p.text),props(p._p.pPr), 'breaks',p._p.xpath('.//w:br/@w:type'))
for ti in [10,22,23]:
 for ri,r in enumerate(D.tables[ti].rows):
  for ci,c in enumerate(r.cells):
   print('CELL',ti,ri,ci,[(i,p.paragraph_format.keep_with_next,p.paragraph_format.keep_together,p.paragraph_format.page_break_before) for i,p in enumerate(c.paragraphs)])
