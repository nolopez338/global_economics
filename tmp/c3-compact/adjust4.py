from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex'); s=p.read_text(); a,b=s.split('\\restoregeometry',1)
a=a.replace('height=5.6cm','height=5.3cm').replace('[5.0cm]','[4.7cm]').replace('\\Needspace{5.9cm}','\\Needspace{5.7cm}').replace('[7mm]{14mm}','[6mm]{14mm}').replace('{.32\\linewidth}','{.325\\linewidth}')
p.write_text(a+'\\restoregeometry'+b); Path('tmp/c3-compact/preview.tex').write_text(a+'\\end{document}')
