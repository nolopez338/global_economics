from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8')
a=s.index(r'\begin{column}{.35\textwidth}',s.index(r'\newcommand{\InfoTables}'))
b=s.index(r'\end{columns}\endgroup}',a)
part=s[a:b].replace(r'p{.23\linewidth}>{\raggedright\arraybackslash}p{.38\linewidth}',r'p{.19\linewidth}>{\raggedright\arraybackslash}p{.48\linewidth}')
s=s[:a]+part+s[b:]
s=s.replace('Uncertainty in the mean duration: centre-to-endpoint distance.','Uncertainty in mean duration: centre-to-endpoint distance.')
s=s.replace("The span of plausible mean durations describes the estimate's precision.",'The interval span describes precision.')
s=s.replace(r'\end{tabularx}\par\smallskip\end{frame}',r'\end{tabularx}\end{frame}')
s=s.replace(r'\R{6}{Study 3 misses because',r'\R{6}{Study 3 misses:').replace(r'\R{2}{Later established population mean:',r'\R{2}{Later established mean:')
p.write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/lesson.tex').write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/disabled.tex').write_text(s.replace('[12pt,aspectratio=169]','[handout,12pt,aspectratio=169]').replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'),encoding='utf8')
