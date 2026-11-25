from pathlib import Path
from pypdf import PdfReader, PdfWriter
import pdfplumber
root=Path('tmp/c3-compact')
baseline=PdfReader('book2026-2027/grade11/term_2/2-class_activities/tmp/c3-compact-baseline/G11_T2_L1_C3_classroom_activity.pdf')
final=PdfReader(root/'final-build/G11_T2_L1_C3_classroom_activity.pdf')
assert len(baseline.pages)==31 and len(final.pages)==29
w=PdfWriter()
for p in baseline.pages[6:]: w.add_page(p)
w.write(root/'baseline-solutions.pdf')
w=PdfWriter()
for p in final.pages[4:]: w.add_page(p)
w.write(root/'final-solutions.pdf')
w=PdfWriter()
for p in final.pages[:4]: w.add_page(p)
w.write(root/'final-activity.pdf')
assert 'Solutions' in final.pages[4].extract_text()
with pdfplumber.open(root/'final-build/G11_T2_L1_C3_classroom_activity.pdf') as d:
    for i,p in enumerate(d.pages[:4]):
        assert (p.width,p.height)==(612,792)
        footer=[v for v in p.extract_words() if v['top']>765]
        assert len(footer)==1 and footer[0]['text']==str(i+1)
        assert abs((footer[0]['x0']+footer[0]['x1'])/2-306)<.1
        content=[v for v in p.extract_words() if v['top']<765]
        print('Activity',i+1,'Letter; centered footer',i+1,'; content/footer gap',round(footer[0]['top']-max(v['bottom'] for v in content),1),'pt')
print('Solutions start on physical page 5; 25 solution pages retained.')
