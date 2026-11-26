from pathlib import Path
import re
import sys
from PIL import Image, ImageDraw
p=Path(__file__).parent/'build'
frames=[tuple(map(int,x)) for x in re.findall(r'\\beamer@framepages\s*\{(\d+)\}\{(\d+)\}',(p/'lesson.nav').read_text())]
print(frames)
prefix=sys.argv[1] if len(sys.argv)>1 else 'page'
files=sorted(p.glob(prefix+'-*.png'))
files=[f for f in files if re.fullmatch(prefix+r'-\d+\.png',f.name)]
for batch in range(0,len(frames),9):
    group=frames[batch:batch+9]
    out=Image.new('RGB',(1800,((len(group)+2)//3)*365),'#dddddd')
    d=ImageDraw.Draw(out)
    for j,(a,b) in enumerate(group):
        out.paste(Image.open(files[b-1]).resize((600,338)),((j%3)*600,(j//3)*365))
        d.text(((j%3)*600+5,(j//3)*365+341),f'Frame {batch+j+1}: pages {a}-{b}',fill='black')
    out.save(p/f'{prefix}-contact-{batch//9+1}.png')

