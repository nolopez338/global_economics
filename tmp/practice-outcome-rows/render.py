from pypdf import PdfReader
from pathlib import Path
import subprocess
pdf=Path('tmp/practice-outcome-rows/G10_T2_L1_C2_practice_activity.pdf')
r=PdfReader(pdf)
pages=[]
for i,p in enumerate(r.pages,1):
 text=p.extract_text()
 if 'Probability' in text and ('(outcome)' in text):
  pages.append(i)
  subprocess.run(['pdftoppm','-f',str(i),'-l',str(i),'-r','110','-png','-singlefile',str(pdf),str(pdf.parent/f'row-{i}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print(pages)
