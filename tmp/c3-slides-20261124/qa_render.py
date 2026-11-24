from pathlib import Path
import re,subprocess,json,concurrent.futures
from PIL import Image,ImageOps,ImageDraw
W=Path(__file__).resolve().parent
P=W/'final-v3'
nav=(P/'build/lesson.nav').read_text()
ranges=[tuple(map(int,m)) for m in re.findall(r'\\beamer@framepages\s*\{(\d+)\}\{(\d+)\}',nav)]
print('frames',len(ranges),'pages',ranges[-1][-1])
assert len(ranges)==41
R=W/'inspection';R.mkdir(exist_ok=True)
(R/'frame-pages.json').write_text(json.dumps(ranges))
def render(job):
    pdf,page,name=job
    target=R/name
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1600','-png',str(pdf),str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return target.with_suffix('.png')
jobs=[]
for n,(a,b) in enumerate(ranges,1):jobs.append((P/'build/lesson.pdf',b,f'final-{n:02}'))
for n in [6,8,9,10,11,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]:
    a,b=ranges[n-1]
    for p in sorted(set([a,(a+b)//2])):
        jobs.append((P/'build/lesson.pdf',p,f'overlay-{n:02}-{p-a+1}'))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(render,jobs))
def sheets(files,prefix):
    for start in range(0,len(files),6):
        canvas=Image.new('RGB',(1600,1440),'#d9dfe1');d=ImageDraw.Draw(canvas)
        for j,path in enumerate(files[start:start+6]):
            im=Image.open(path).convert('RGB');im.thumbnail((790,445))
            x=(j%2)*800;y=(j//2)*480
            canvas.paste(im,(x,y+25));d.text((x+10,y+5),path.stem,fill='black')
        canvas.save(R/f'{prefix}-{start//6+1:02}.png')
sheets(sorted(R.glob('final-*.png')),'sheet-finals')
sheets(sorted(R.glob('overlay-*.png')),'sheet-overlays')
print('Rendered',len(jobs),'pages and contact sheets')



