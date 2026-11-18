from pathlib import Path
from pypdf import PdfReader
r=Path('tmp/c1_classroom_layout')
a=PdfReader(r/'original.pdf'); b=PdfReader(r/'G10_T2_L1_C1_classroom_activity.pdf')
print('Pages:',len(a.pages),'->',len(b.pages))
for i in range(3):
    assert a.pages[i].extract_text()==b.pages[i].extract_text()
print('First three student pages: identical text.')
for name,pdf in [('original',a),('updated',b)]:
    names=pdf.named_destinations; links=[]
    for page in pdf.pages:
        for ref in page.get('/Annots',[]):
            annot=ref.get_object()
            if annot.get('/Subtype')=='/Link':
                links.append(annot)
                dest=annot.get('/Dest') or annot.get('/A',{}).get('/D')
                if isinstance(dest,str): assert dest in names, dest
    print(name,'navigation link annotations:',len(links),'named destinations:',len(names))
log=(r/'G10_T2_L1_C1_classroom_activity.log').read_text(errors='replace')
assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning'])
print('No overfull boxes, undefined references, or LaTeX warnings.')
