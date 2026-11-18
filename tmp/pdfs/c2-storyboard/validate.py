from pathlib import Path
from PIL import Image,ImageDraw
import re,json
p=Path('tmp/pdfs/c2-storyboard/final-render')
groups=[[2,3,9,16,17,18,22,25,26],[27,28,29,30,31,32,33,34,35],[38,40,42,43,44,45,46,48,51],[52,54,55,56,57,58,60,61,63],[64,65,66,70,74,75,76,80,84],[85,86,87,90,94,95]]
for i,ns in enumerate(groups):
    c=Image.new('RGB',(2700,535*((len(ns)+2)//3)),'#dddddd');d=ImageDraw.Draw(c)
    for j,n in enumerate(ns):
        c.paste(Image.open(p/f'page-{n:02}.png').convert('RGB'),(j%3*900,j//3*535+22));d.text((j%3*900+8,j//3*535+3),f'PDF page {n}',fill='black')
    c.save(p/f'contact-{i}.png')
a=(p/'slides.txt').read_text(encoding='utf-8');b=(p/'slides-off.txt').read_text(encoding='utf-8')
x=re.sub(r'\s+','',a);y=re.sub(r'\s+','',b)
print('Slides enabled/disabled text identical ignoring whitespace:', x==y)
if x!=y:
    import difflib
    print('First differences:',list(difflib.unified_diff(a.splitlines(),b.splitlines()))[:30])
# Verify all 27 explicit motion coordinates against requested physical displacement.
s=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C2_slides.tex').read_text(encoding='utf-8')
for a,m,b,start in [(0,.15,0,3),(2,.60,.15,13),(4,.25,.75,23)]:
    for k in range(9):
        shift=(2.55+2*b)*k/8
        text=rf'\only<{start+k}>{{\draw[cTwoGuideColor,densely dashed,line width=.9pt] ({a},{shift:.6f})--({a},{shift+2*m:.6f});}}'
        assert text in s,(a,k)
print('All 27 motion positions preserve x and stem length, including panel gap and cumulative shift.')
# Fixed table rule positions within each sequence.
def rules(n,x0,x1):
    im=Image.open(p/f'page-{n:02}.png').convert('RGB'); ys=[]
    for yy in range(95,460):
        count=sum(1 for r,g,b in [im.getpixel((xx,yy)) for xx in range(x0,x1)] if r<100 and g<120 and b<140)
        if count>(x1-x0)*.8:ys.append(yy)
    return ys
for first,last,x0,x1 in [(3,17,465,830),(18,25,55,385),(27,33,55,270),(34,43,395,805),(44,50,55,280)]:
    a,b=rules(first,x0,x1),rules(last,x0,x1)
    print('Stable table rules',first,last,a==b,a,b)
Image.open(p/'page-95.png').convert('L').save(p/'stack-gray.png')
Image.open(p/'page-02.png').convert('L').save(p/'legend-gray.png')
