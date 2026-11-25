from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex')
s=p.read_text(); a,b=s.split('\\restoregeometry',1)
a=a.replace('height=.85cm','height=.65cm').replace('height=6.2cm','height=6.0cm').replace('[5.6cm]','[5.0cm]').replace('\\Needspace{6.6cm}','\\Needspace{6.2cm}')
start=a.index('\\problemtitle{3}')
end=a.index('\\par\\endgroup',start)
x=a[start:end]
x=x.replace('\\problemtitle{4}', '\\end{minipage}\\hfill\n\\begin{minipage}[t]{.32\\linewidth}\\vspace{0pt}\\raggedright\n\\problemtitle{4}')
x=x.replace('\\problemtitle{5}', '\\end{minipage}\\hfill\n\\begin{minipage}[t]{.32\\linewidth}\\vspace{0pt}\\raggedright\n\\problemtitle{5}')
a=a[:start]+'\\noindent\\begin{minipage}[t]{.32\\linewidth}\\vspace{0pt}\\raggedright\n'+x+'\\end{minipage}\n'+a[end:]
p.write_text(a+'\\restoregeometry'+b)
Path('tmp/c3-compact/preview.tex').write_text(a+'\\end{document}')
