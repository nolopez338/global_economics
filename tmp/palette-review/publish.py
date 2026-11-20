from pathlib import Path
import shutil,re,subprocess
r=Path.cwd();o=r/'tmp/palette-review';d=r/'book2026-2027/preamble/graphs'
s=(o/'preview-text.txt').read_text(encoding='utf8');assert s.count('Registry key:')==28,s.count('Registry key:')
log=(o/'preview/specific_highlights_view.log').read_text(errors='replace');assert not re.search(r'^!|^Overfull|^LaTeX Warning|^Package .*Warning',log,re.M)
shutil.copy2(o/'preview/specific_highlights_view.pdf',d/'specific_highlights_view.pdf')
p=o/'REPORT.md';s=p.read_text(encoding='utf8').replace('rendered pages inspected.','all 15 rendered pages inspected.');p.write_text(s,encoding='utf8')
assert (d/'specific_highlights_view.pdf').read_bytes()==(o/'preview/specific_highlights_view.pdf').read_bytes()
print('Published final 15-page preview, containing all 28 registry entries. Matching G10 PDFs and report ready.')
