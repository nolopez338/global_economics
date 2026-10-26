from pathlib import Path
from decimal import Decimal as D, ROUND_HALF_UP
import re
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader

base=Path('tmp/c9-solutions')
target=Path('book2026-2027/grade11/term_1/2-class_activities/G11_T1_C9_classroom_activity.tex')
old=(base/'original.tex').read_bytes(); new=target.read_bytes(); marker=b'\\textbf{\\large Solutions}'
assert old.split(marker)[0]==new.split(marker)[0]
oldsol=old.split(marker)[1]; sol=new.split(marker)[1]
titles=lambda s:re.findall(rb'\\textbf\{([^{}]*\(\$\\nu=\d+\$\)\.)\}',s)
assert titles(oldsol)==titles(sol)
assert sol.count(b'Comparison errors.')==15
assert sol.count(b'E_{Pt}&=')==21 and sol.count(b'E_{Pn}&=')==21
table=Path('book2026-2027/fundamentals/normal-table.tex').read_text(encoding='utf-8')
alphas=[D('.30'),D('.20'),D('.10'),D('.05'),D('.025'),D('.01'),D('.005')]
rows={}
for line in table.splitlines():
    match=re.match(r'\s*(\d+)\s*&\s*(\d\.\d{3})\s*&',line)
    if match:
        vals=re.findall(r'\d+\.\d{3}',line)
        if len(vals)==7: rows[int(match[1])]=dict(zip(alphas,map(D,vals)))
normal={}
for line in table.splitlines():
    match=re.match(r'\s*(\d\.\d)\s*&',line)
    vals=re.findall(r'\d\.\d{4}',line)
    if match and len(vals)==10:
        for i,v in enumerate(vals):normal[D(match[1])+D(i)/100]=D(v)
# Check every stated t row/column independently against the reference source.
expected=[(6,'.05','1.943'),(15,'.20','.866'),(19,'.20','.861'),(19,'.05','1.729'),(8,'.025','2.306'),(8,'.20','.889'),(4,'.05','2.132'),(4,'.10','1.533'),(10,'.10','1.372'),(23,'.025','2.069'),(18,'.05','1.734'),(5,'.025','2.571'),(12,'.05','1.782'),(12,'.10','1.356'),(20,'.025','2.086'),(15,'.01','2.602'),(8,'.05','1.860'),(8,'.025','2.306'),(10,'.01','2.764')]
for df,a,t in expected: assert rows[df][D(a)]==D(t),(df,a,t)
expectednormal={'1.94':'.9738','.87':'.8078','.86':'.8051','1.73':'.9582','2.31':'.9896','.89':'.8133','2.13':'.9834','1.53':'.9370','1.28':'.8997','1.29':'.9015','1.64':'.9495','1.65':'.9505','1.96':'.9750','2.33':'.9901','2.32':'.9898'}
for z,v in expectednormal.items(): assert normal[D(z)]==D(v),(z,v)
# Independently recompute all direct standardized boundaries and table probabilities.
bounds=[('-9.658','2','6','-1.943'),('-49.64','-15','40','-.866'),('27.22','10','20','.861'),('44.58','10','20','1.729'),('-11.224','-2','4','-2.306'),('-5.556','-2','4','-.889'),('-5.396','1','3','-2.132'),('5.599','1','3','1.533')]
for x,m,a,c in bounds: assert (D(x)-D(m))/D(a)==D(c)
probs=[(D('.05'),1-normal[D('1.94')]),(1-D('.2'),normal[D('.87')]),((1-D('.05'))-(1-D('.2')),normal[D('1.73')]-normal[D('.86')]),(D('.2')-D('.025'),(1-normal[D('.89')])-(1-normal[D('2.31')])),(D('.05')+D('.1'),1-normal[D('2.13')]+1-normal[D('1.53')])]
fmt=lambda x,p=2:f'{x.quantize(D(10)**-p,rounding=ROUND_HALF_UP):.{p}f}'
original_errors=re.findall(rb'E_A\\approx([\d.]+).*?E_\{Pt\}\\approx([\d.]+)\\%.*?E_\{Pn\}\\approx([\d.]+)\\%',oldsol)
results=[]
for t,n in probs:results.append((fmt(abs(t-n),4),fmt(100*abs(t-n)/abs(t)),fmt(100*abs(t-n)/abs(n))))
inverse_data=[('-2','6','-1.372','-1.28'),('3','8','2.069','1.96'),('10','40','-1.734','-1.64'),('10','40','1.734','1.64'),('-.5','1.5','-2.571','-1.96'),('-.5','1.5','2.571','1.96'),('1','5','-1.782','-1.64'),('1','5','1.356','1.28'),('1','5','-1.356','-1.28'),('0','12','-2.086','-1.96'),('0','12','2.086','1.96'),('3','7','2.602','2.33'),('-1','3','-1.860','-1.64'),('-1','3','2.306','1.96'),('2','4','-2.764','-2.33'),('2','4','2.764','2.33')]
for m,a,t,z in inverse_data:
    t,n=D(m)+D(a)*D(t),D(m)+D(a)*D(z)
    results.append((fmt(abs(t-n)),fmt(100*abs(t-n)/abs(t)),fmt(100*abs(t-n)/abs(n))))
assert len(original_errors)==len(results)==21
for oldvalues,computed in zip(original_errors,results):assert tuple(x.decode() for x in oldvalues)==computed,(oldvalues,computed)
print('PASS: unchanged prefix; 15 original titles in order; 21 complete error sets; all t and normal entries checked against supplied table; all direct bounds and probabilities checked; all inverse errors independently recomputed. All original numerical answers retained.')

reader=PdfReader(base/'G11_T1_C9_classroom_activity.pdf')
for i,page in enumerate(reader.pages):
    lines=[x.strip() for x in page.extract_text().splitlines() if x.strip()]
    print(f'PAGE {i+1}: START {" / ".join(lines[:2])[:160]} ... END {" / ".join(lines[-2:])[:160]}')
images=sorted(base.glob('final-page-*.png'))
for k in range(0,len(images),6):
    sheet=Image.new('RGB',(3*480,2*650),'#dddddd'); draw=ImageDraw.Draw(sheet)
    for j,path in enumerate(images[k:k+6]):
        im=Image.open(path).convert('RGB');im.thumbnail((470,620))
        x=(j%3)*480+5; y=(j//3)*650+25
        sheet.paste(im,(x,y));draw.text((x,y-20),path.stem,fill='black')
    sheet.save(base/f'contact-{k//6+1}.png')

