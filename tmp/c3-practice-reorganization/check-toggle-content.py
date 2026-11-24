from pypdf import PdfReader
from pathlib import Path
import re
base=Path('tmp/c3-practice-reorganization')
a=PdfReader(base/'build/G10_T2_L1_C3_practice_activity.pdf');b=PdfReader(base/'off/highlights-off.pdf')
# Check identical mathematical symbol/value character inventories after removing pagination.
texts=[]
for doc in [a,b]:
 pages=[]
 for p in doc.pages:
  t=p.extract_text();t=re.sub(r'\n\d+\s*$','',t);pages.append(t)
 texts.append(''.join(pages))
from collections import Counter
ca,cb=[Counter(re.sub(r'\s','',t)) for t in texts]
print('Highlight variants retain matching character inventories:',ca==cb)
print('Differences:',ca-cb,cb-ca)
