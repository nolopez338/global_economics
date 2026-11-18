from pathlib import Path
import subprocess
root=Path.cwd()
src=root/'book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex'
out=root/'tmp/pdfs/c2_restatements'
s=src.read_text(encoding='utf-8')
disabled=out/'disabled.tex'
disabled.write_text(s.replace('% \\GTenHighlightsfalse %','\\GTenHighlightsfalse %'),encoding='utf-8')
for name,file in [('disabled',disabled)]:
    r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(out),str(file)],cwd=src.parent,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (out/(name+'-build.txt')).write_bytes(r.stdout)
    print(name,r.returncode, r.stdout.decode(errors='replace')[-500:])
