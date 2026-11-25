from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex'); s=p.read_text(); a,b=s.split('\\restoregeometry',1)
a=a.replace('height=6.0cm','height=5.6cm').replace('\\Needspace{6.2cm}','\\Needspace{5.9cm}')
a=a.replace('cs:.97,.72','cs:.97,.70').replace('cs:.97,.54','cs:.97,.50').replace('cs:.97,.36','cs:.97,.30').replace('cs:.97,.18','cs:.97,.10')
a=a.replace('\\begingroup\\small\n\\textit{Complete Independent','\\begingroup\\small\\setlength{\\parskip}{0pt}\n\\textit{Complete Independent')
p.write_text(a+'\\restoregeometry'+b); Path('tmp/c3-compact/preview.tex').write_text(a+'\\end{document}')
