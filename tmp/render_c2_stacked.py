from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import subprocess, json
pdf = Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.pdf').resolve()
out = Path('tmp/pdfs/c2-stacked')
out.mkdir(parents=True,exist_ok=True)
subprocess.run(['pdftotext','-layout',str(pdf),str(out/'text.txt')],check=True)
pages = (out/'text.txt').read_text(encoding='utf-8').split('\f')
selected = [i+1 for i,t in enumerate(pages) if 'Connecting the PMF and CDF' in t]
assert len(selected)==12, selected
for n in selected:
    text = pages[n-1]
    assert 'How to read the stacked graphs.' in text, n
    assert 'Midpoint correspondence' in text and 'Bottom: PMF stems' in text,n
    subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','110','-png','-singlefile',str(pdf),str(out/f'page-{n}')],check=True)
for group in range(4):
    nums = selected[group*3:group*3+3]
    ims=[]
    for n in nums:
        im=Image.open(out/f'page-{n}.png').convert('RGB')
        im.thumbnail((900,1300))
        ims.append(im)
    panel=Image.new('RGB',(sum(im.width for im in ims),max(im.height for im in ims)), '#cccccc')
    x=0
    for im in ims:
        panel.paste(im,(x,0)); x+=im.width
    panel.save(out/f'review-{group+1}.png')
print(json.dumps({'connection_pages':selected,'page_count':len(pages)-1,'pairs_kept_with_reading_on_one_page':12}))
