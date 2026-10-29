from PIL import Image, ImageDraw
from pathlib import Path
import pdfplumber
p=Path('tmp/g10-solution-build')
images=sorted(p.glob('final-*.png'))
for k in range(0,len(images),4):
    sheet=Image.new('RGB',(2060,2680),'#999999')
    draw=ImageDraw.Draw(sheet)
    for j,img in enumerate(images[k:k+4]):
        im=Image.open(img).convert('RGB')
        im.thumbnail((1010,1300))
        x=(j%2)*1030+10; y=(j//2)*1340+30
        sheet.paste(im,(x,y))
        draw.text((x,y-20),f'Page {k+j+1}',fill='black')
    sheet.save(p/f'contact-{k//4+1}.png')
d=pdfplumber.open(p/'G10_T1_C1C2C3C4C5C6C7_exam_solution.pdf')
print('Pages:',len(d.pages))
for i,page in enumerate(d.pages):
    txt=page.extract_text()
    words=page.extract_words()
    assert all(w['x0']>=0 and w['x1']<=page.width and w['top']>=0 and w['bottom']<=page.height for w in words)
    print(i+1,txt[:65].replace('\n',' | '))
