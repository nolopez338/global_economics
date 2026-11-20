from pathlib import Path
import re
p=Path('book2026-2027/preamble/graphs/specific_highlights_view.tex');s=p.read_text();s=re.sub(r'\\Needspace\{20\\baselineskip\}\n\\noindent\\textbf\{Grade [^\n]+\}\n','',s);p.write_bytes(s.replace('\n','\r\n').encode())
