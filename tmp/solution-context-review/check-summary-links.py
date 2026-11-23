from pathlib import Path
p=Path('tmp/solution-context-review/check-final-pdf.py')
s=p.read_text().replace("['toc','sec:p1','sec:p2','sec:p3']+", "['toc','sec:p1','sec:p2','sec:p3','summary:p1','summary:p2','summary:p3']+").replace('All 19 contents, problem and worked-task destinations resolve.','All 22 contents, problem, worked-task and summary destinations resolve.')
p.write_text(s)
