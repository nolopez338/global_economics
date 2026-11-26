from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).parent/'build'
pages=[4,5,6,8,9,10,12,13,14,27,28,30,31,33,34,35,37,38,40,41,47,48,49,51,52,54,55,57,58,61,62,63,65,66,70,71,73,74,76,77]
files=sorted(p.glob('page-*.png'))
for offset in range(0,len(pages),10):
    group=pages[offset:offset+10]
    out=Image.new('RGB',(1600,((len(group)+1)//2)*470),'#ddd')
    d=ImageDraw.Draw(out)
    for j,num in enumerate(group):
        out.paste(Image.open(files[num-1]).resize((800,450)),((j%2)*800,(j//2)*470))
        d.text(((j%2)*800+5,(j//2)*470+451),f'PDF page {num}',fill='black')
    out.save(p/f'overlays-{offset//10+1}.png')
