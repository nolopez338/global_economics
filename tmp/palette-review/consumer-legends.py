from pathlib import Path
import subprocess,json,re
r=Path.cwd();o=r/'tmp/palette-review'
for d in sorted(o.glob('G10*')):
 pdf=d/(d.name+'.pdf')
 if not pdf.exists():continue
 text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode('utf8');pages=text.split('\f');legend=next(i+1 for i,t in enumerate(pages) if 'Symbol or notation' in t)
 subprocess.run(['pdftoppm','-f',str(legend),'-l',str(legend),'-singlefile','-scale-to','1200','-png',str(pdf),str(d/'legend')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 print(d.name,'legend page',legend)
