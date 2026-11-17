from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
for name,pages in [('student',range(1,4)),('solutionsA',range(4,7)),('solutionsB',range(7,9))]:
 imgs=[]
 for i in pages:
  im=Image.open(f'tmp/c2-solutions/enabled/page-{i}.png').convert('RGB'); im.thumbnail((620,810)); imgs.append(im)
 out=Image.new('RGB',(len(imgs)*640,840),'#cccccc')
 for j,im in enumerate(imgs): out.paste(im,(j*640,20))
 out.save(f'tmp/c2-solutions/{name}.png')
for i in range(1,4):
 a=Image.open(f'tmp/c2-solutions/baseline/page-{i}.png'); b=Image.open(f'tmp/c2-solutions/student/check-{i}.png'); c=Image.open(f'tmp/c2-solutions/enabled/page-{i}.png')
 assert a.tobytes()==b.tobytes()==c.tobytes(),i
print('All 3 student pages pixel-identical in baseline, disabled, and enabled PDFs at 110 dpi.')
