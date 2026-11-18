from pathlib import Path
import re
p=Path('tmp/pdfs/c2-storyboard')
a=re.sub(r'\s+','',(p/'practice-final.txt').read_text(encoding='utf-8'))
b=re.sub(r'\s+','',(p/'practice-off-final.txt').read_text(encoding='utf-8'))
assert a.replace('-','')==b.replace('-','')
r=p/'VALIDATION.md'
s=r.read_text(encoding='utf-8').replace('Full-document raw text differs in ordering/pagination, so no claim of exact full-document text equivalence.','Full-document extracted text differs only by one line-break hyphen in information; it matches after ignoring whitespace and hyphenation.')
r.write_text(s,encoding='utf-8')
print('Practice full content retained, ignoring whitespace and line-break hyphenation.')
