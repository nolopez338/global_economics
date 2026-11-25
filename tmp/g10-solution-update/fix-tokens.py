from pathlib import Path
p=Path('tmp/g10-solution-update/edit.py');s=p.read_text();s=s.replace(r'(?<![A-Za-z\\])(?:\d+',r'(?<![\d.])(?:\d+');p.write_text(s)
