from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex'); s=p.read_text(); a,b=s.split('\\restoregeometry',1)
start=a.index('\\renewcommand{\\normalpanel}')
end=a.index('% Structural styles',start)
a=a[:start]+a[end:]
a=a.replace('height=3.2cm','height=4.6cm')
needle='\\begingroup\\small\\setlength{\\parskip}{0pt}'
runin=r'''\begingroup\small\setlength{\parskip}{0pt}
% Run short task titles into their instructions within the independent columns.
% Keep the same compact node and route every title through \taskheading.
\renewcommand{\taskheading}[1]{%
    \par\Needspace{2\baselineskip}\addvspace{1pt}%
    \noindent\tikz[baseline=(title.base)]{%
        \node[fill=black!5,draw=none,text=black,rounded corners=2mm,
            inner sep=3pt,outer sep=0pt] (title) {%
            \begin{varwidth}{\dimexpr\linewidth-6pt\relax}%
                \raggedright\bfseries\strut #1\strut
            \end{varwidth}};}\nobreak\hspace{3pt}}
'''
a=a.replace(needle,runin.rstrip())
p.write_text(a+'\\restoregeometry'+b); Path('tmp/c3-compact/preview.tex').write_text(a+'\\end{document}')
