from pathlib import Path
import subprocess
r=Path.cwd();o=r/'tmp/palette-review'
for d in sorted(o.glob('G10*')):
 pdf=d/(d.name+'.pdf')
 if pdf.exists() and 'C3_' not in d.name:subprocess.run(['pdftoppm','-f','2','-l','2','-singlefile','-scale-to','1100','-png',str(pdf),str(d/'legend-cont')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
