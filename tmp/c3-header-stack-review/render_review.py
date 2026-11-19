from pathlib import Path
import subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
root=Path('tmp/c3-header-stack-review')
pdf=root/'stacked.pdf'
subprocess.run(['pdftotext','-bbox',str(pdf),str(root/'bbox.html')],check=True)
subprocess.run(['pdftoppm','-scale-to','1300','-png',str(pdf),str(root/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
ns={'x':'http://www.w3.org/1999/xhtml'}
import re
xml=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', (root/'bbox.html').read_text(encoding='utf-8'))
pages=ET.fromstring(xml).findall('.//x:page',ns)
crops=[]
for n,page in enumerate(pages,1):
    im=Image.open(root/f'page-{n:02}.png').convert('RGB')
    sx=im.width/float(page.attrib['width']); sy=im.height/float(page.attrib['height'])
    words=page.findall('x:word',ns)
    heads=[w for w in words if w.text in ('Calculation','Symbol','Design')]
    if n==2:
        heads += [w for w in words if w.text=='Confidence' and float(w.attrib['yMin'])>200]
    for w in heads:
        x=0 if im.height>im.width else im.width*.50
        y=float(w.attrib['yMin'])*sy
        crop=im.crop((int(x),max(0,int(y-14)),im.width,min(im.height,int(y+125))))
        label=Image.new('RGB',(crop.width,crop.height+24),'white')
        label.paste(crop,(0,24)); ImageDraw.Draw(label).text((5,4),f'Page {n}',fill='black')
        crops.append(label)
for start in range(0,len(crops),8):
    batch=crops[start:start+8]
    canvas=Image.new('RGB',(1000,sum(c.height+8 for c in batch)), '#dddddd')
    y=0
    for c in batch:
        canvas.paste(c,(0,y));y+=c.height+8
    canvas.save(root/f'headers-{start//8+1}.png')
print('Pages:',len(pages),'header crops:',len(crops))
