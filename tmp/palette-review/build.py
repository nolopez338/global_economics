from pathlib import Path
import subprocess,concurrent.futures,json
root=Path.cwd();out=root/'tmp/palette-review'
paths=sorted((root/'book2026-2027/grade10/term_2/1-practice_activities').glob('*.tex'))
paths += [root/'book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex']
def build(p):
 target=out/p.stem;target.mkdir(exist_ok=True)
 with (target/'console.txt').open('w') as log:
  for i in range(2):
   r=subprocess.run(['pdflatex','-interaction=batchmode','-halt-on-error','-file-line-error','-output-directory='+target.as_posix(),p.name],cwd=p.parent,stdout=log,stderr=subprocess.STDOUT)
   if r.returncode:break
 result={'source':str(p.relative_to(root)),'exit':r.returncode,'build':str(target)}
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(build,paths))
(out/'build-results.json').write_text(json.dumps(results,indent=2))
