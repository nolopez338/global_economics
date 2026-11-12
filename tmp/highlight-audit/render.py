from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
import pdfplumber,json
base=Path('tmp/highlight-audit')
report={}
for kind in ('slides-on','slides-off','practice-on','practice-off'):
    files=list((base/kind).glob('*.pdf'))
    if not files: continue
    path=files[0]
    try: doc=pdfium.PdfDocument(path)
    except Exception as e:
        print(kind,str(e)); continue
    rows=4 if 'slides' in kind else 3
    cols=4
    thumbw=480 if 'slides' in kind else 330
    thumbh=290 if 'slides' in kind else 480
    for start in range(0,len(doc),rows*cols):
        sheet=Image.new('RGB',(cols*thumbw,rows*thumbh),'#c8c8c8')
        draw=ImageDraw.Draw(sheet)
        for n in range(start,min(start+rows*cols,len(doc))):
            im=doc[n].render(scale=1.25).to_pil().convert('RGB')
            im.thumbnail((thumbw-10,thumbh-24))
            x=((n-start)%cols)*thumbw;y=((n-start)//cols)*thumbh
            sheet.paste(im,(x+5,y+20));draw.text((x+5,y+3),f'{kind} page {n+1}',fill='black')
        sheet.save(base/f'{kind}-contact-{start//(rows*cols)+1}.png')
    # Detailed views of every overlay on the first general model.
    if 'slides' in kind:
        for n in range(3,9):
            doc[n].render(scale=2.5).to_pil().save(base/f'{kind}-slide4-overlay{n-2}.png')
    with pdfplumber.open(path) as pdf:
        outside=[];blue=0
        for i,page in enumerate(pdf.pages):
            for c in page.chars:
                if c['x0'] < -1 or c['x1']>page.width+1 or c['top'] < -1 or c['bottom']>page.height+1:
                    outside.append([i+1,c['text'],round(c['x0'],1),round(c['top'],1)])
            for r in page.rects:
                color=r.get('non_stroking_color')
                if isinstance(color,(tuple,list)) and len(color)==3 and abs(color[0]-.5255)<.01 and abs(color[1]-.749)<.01: blue+=1
        report[kind]={'pages':len(pdf.pages),'outside_page':outside[:30],'blue_rectangles':blue}
        text='\n'.join(p.extract_text() or '' for p in pdf.pages)
        (base/f'{kind}-text.txt').write_text(text,encoding='utf-8')
    print(kind,len(doc),'pages')
(base/'render-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
