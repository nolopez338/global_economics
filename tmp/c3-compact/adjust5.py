from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex'); s=p.read_text(); a,b=s.split('\\restoregeometry',1)
a=a.replace('height=5.3cm','height=5.1cm').replace('[4.7cm]','[4.5cm]').replace('\\Needspace{5.7cm}','\\Needspace{5.5cm}')
a=a.replace('cs:.97,.90','cs:.97,.92').replace('cs:.97,.70','cs:.97,.71').replace('cs:.97,.30','cs:.97,.29').replace('cs:.97,.10','cs:.97,.08')
a=a.replace('\\addvspace{2pt}','\\addvspace{1pt}').replace('\\nopagebreak[4]\\vspace{2pt}','\\nopagebreak[4]\\vspace{1pt}')
a=a.replace('\\textbf{Problem 2 --- Delivery charges', '\\Needspace{7cm}\n\\textbf{Problem 2 --- Delivery charges')
p.write_text(a+'\\restoregeometry'+b); Path('tmp/c3-compact/preview.tex').write_text(a+'\\end{document}')
