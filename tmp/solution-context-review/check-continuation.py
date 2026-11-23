from pathlib import Path
p=Path('tmp/solution-context-review/check-final-pdf.py')
s=p.read_text().replace('text=r.pages[page].extract_text()',"text=r.pages[page+(1 if i==2 else 0)].extract_text()")
s=s.replace('Each detailed C2 table remains together on its worked-task page in the highlighted build.','Each detailed C2 table remains intact; Problem 2 uses its continuation page.')
p.write_text(s)
