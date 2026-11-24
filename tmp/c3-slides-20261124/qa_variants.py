from pathlib import Path
import subprocess,concurrent.futures
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;R=W/'variant-inspection'
def render(job):
    v,n=job;target=R/f'{v}-{n:02}'
    subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1200','-png',str(W/v/'build/lesson.pdf'),str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return target.with_suffix('.png')
for v in ['disabled','grayscale']:
    jobs=[(v,n) for n in range(1,42)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:files=list(pool.map(render,jobs))
    for start in range(0,len(files),8):
        canvas=Image.new('RGB',(1600,1920),'#d9dfe1');d=ImageDraw.Draw(canvas)
        for j,path in enumerate(files[start:start+8]):
            im=Image.open(path).convert('RGB');im.thumbnail((790,445))
            x=(j%2)*800;y=(j//2)*480;canvas.paste(im,(x,y+25));d.text((x+10,y+5),path.stem,fill='black')
        canvas.save(R/f'sheet-{v}-{start//8+1:02}.png')
print('Rendered all final frames in both temporary variants')
