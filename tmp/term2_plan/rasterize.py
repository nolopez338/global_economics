import pypdfium2 as pdfium
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
out=Path('tmp/term2_plan/render');out.mkdir(exist_ok=True)
d=pdfium.PdfDocument('tmp/term2_plan/updated.pdf')
thumbs=[]
for i,p in enumerate(d):
 im=p.render(scale=1.5).to_pil();im.save(out/f'page-{i+1}.png')
 th=im.copy();th.thumbnail((350,500));canvas=Image.new('RGB',(370,530),'#cccccc');canvas.paste(th,((370-th.width)//2,20));ImageDraw.Draw(canvas).text((8,505),f'Page {i+1}',fill='black');thumbs.append(canvas)
cols=4;rows=(len(thumbs)+cols-1)//cols
sheet=Image.new('RGB',(cols*370,rows*530),'white')
for i,im in enumerate(thumbs):sheet.paste(im,((i%cols)*370,(i//cols)*530))
sheet.save(out/'overview.png')
print('Pages:',len(d))
