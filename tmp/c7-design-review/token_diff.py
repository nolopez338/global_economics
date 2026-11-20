from pypdf import PdfReader
from difflib import SequenceMatcher
import re
p='tmp/c7-design-review/'
a=' '.join(x.extract_text() for x in PdfReader(p+'G11_T2_L2_C7_practice.pdf').pages)
b=' '.join(x.extract_text() for x in PdfReader(p+'off/highlights-off.pdf').pages)
a=re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?',a);b=re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?',b)
for tag,i,j,k,l in SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
 if tag!='equal': print(tag,a[max(0,i-4):min(len(a),j+4)],b[max(0,k-4):min(len(b),l+4)])
