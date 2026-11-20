from pathlib import Path
from pypdf import PdfReader
p=Path('tmp/pdfs/c3-classroom/G11_T2_L1_C3_classroom_activity.pdf')
for i,x in enumerate(PdfReader(p).pages):
 t=x.extract_text(); print(i+1,len(t),t[:95].replace('\n',' / '), ' ... ', t[-70:].replace('\n',' / '))
