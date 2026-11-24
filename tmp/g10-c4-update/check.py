from pathlib import Path
from math import comb
import re
from pypdf import PdfReader

base=Path('tmp/g10-c4-update/build')
pdf=PdfReader(base/'G10_T2_L1_C4_practice_activity.pdf')
off=PdfReader(base/'off.pdf')
assert len(pdf.pages)==len(off.pages)==13
dest=pdf.named_destinations
count=0
for page in pdf.pages:
    for obj in page.get('/Annots',[]):
        a=obj.get_object()
        name=a.get('/A',{}).get('/D',a.get('/Dest'))
        if isinstance(name,str):
            assert name in dest,name
            assert 0 <= pdf.get_destination_page_number(dest[name]) < 13
            count+=1
outline=str(pdf.outline)
assert 'Evaluated criteria' not in outline
assert 'Evaluated criteria' in pdf.pages[0].extract_text()
assert 'Evaluated criteria' not in (base/'G10_T2_L1_C4_practice_activity.toc').read_text()
# Check every source label against its actual PDF destination and page.
aux=(base/'G10_T2_L1_C4_practice_activity.aux').read_text()
labels={k:(int(page)-1,target) for k,page,target in re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}\{[^}]*\}\{([^}]+)\}',aux)}
for k,(page,target) in labels.items():
    assert target in dest,(k,target)
    assert pdf.get_destination_page_number(dest[target])==page,(k,page)
for i,(a,b) in enumerate(zip(pdf.pages,off.pages)):
    norm=lambda p: re.sub(r'\s+','',p.extract_text())
    assert norm(a)==norm(b),f'Highlight-off text differs on page {i+1}'
cases=[(3,.5,2,2,.3750),(5,.1,1,1,.3281),(4,.8,3,3,.4096),(6,.4,2,4,.7258),(6,.05,0,1,.9672),(8,.25,1,8,.8999),(10,.2,2,4,.5914),(7,.15,2,7,.2834),(10,.2,1,2,.5704)]
for n,p,a,b,expected in cases:
    value=sum(comb(n,k)*p**k*(1-p)**(n-k) for k in range(a,b+1))
    assert round(value,4)==expected,(n,p,value)
print(f'Checked {count} internal links, {len(labels)} source destinations, criteria exclusion, identical highlight-off text on 13 pages, and 9 probability results.')
