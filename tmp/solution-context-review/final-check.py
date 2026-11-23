from pathlib import Path
p=Path('tmp/solution-context-review/check-pdf.py')
s=p.read_text().replace("root/'disabled/disabled.pdf'","root/'enabled/G11_T2_L1_C1C2_exam_solution.pdf'").replace("root/'disabled/disabled.aux'","root/'enabled/G11_T2_L1_C1C2_exam_solution.aux'").replace('disabled build','highlighted build')
Path('tmp/solution-context-review/check-final-pdf.py').write_text(s)
