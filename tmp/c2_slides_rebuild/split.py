from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8')
# Move Task 1's temporary calculations into the reserved area under the right table.
a=s.index(r'\begin{overlayarea}{\linewidth}{.65cm}')
b=s.index(r'\end{overlayarea}',a)+len(r'\end{overlayarea}')
panel=s[a:b]
panel=panel.replace('{.65cm}','{1.15cm}').replace(r'\small',r'\fontsize{9.5}{10}\selectfont')
panel=panel.replace(' minutes: spread of means across repeated independent samples of 49 trips.',' minutes.')
s=s[:a]+s[b:]
end=s.index(r'\end{columns}\endgroup}',s.index(r'\newcommand{\InfoTables}'))
insert=s.rfind(r'\end{tabularx}\end{column}',s.index(r'\newcommand{\InfoTables}'),end)
s=s[:insert]+s[insert:].replace(r'\end{tabularx}\end{column}',r'\end{tabularx}\par\smallskip\ifReference\else '+panel+r'\fi\end{column}',1)
# Split dense Task 2 rows while keeping exactly the same completed reference.
def getframe(title):
 a=s.index(r'\begin{frame}[t]{'+title+'}')
 b=s.index(r'\end{frame}',a)+len(r'\end{frame}')
 return a,b,s[a:b]
a,b,f=getframe('Task 2 -- Point estimate and margin of error')
tab=f.index(r'\begin{tabularx}')
header=f[tab:f.index(r'\midrule',tab)+len(r'\midrule')]
point,margin=f[f.index(r'\midrule',tab)+len(r'\midrule'):f.index(r'\bottomrule',tab)].split(r'\\\midrule',1)
base=f[:tab]
f1=base.replace('Point estimate and margin of error','Point estimate')+header+point+r'\\\bottomrule\end{tabularx}\end{frame}'
f2=base.replace('Point estimate and margin of error','Margin of error')+header+margin+r'\bottomrule\end{tabularx}\end{frame}'
# Margin frame carries the completed point input from the preceding frame.
f2=f2.replace(r'\csname Input5\endcsname{2}',r'\csname Input5\endcsname{1}')
s=s[:a]+f1+'\n'+f2+s[b:]
a,b,f=getframe('Task 2 -- Build the confidence interval')
x=f.index(r'\R{8}')
y=f.index(r'\bottomrule',x)
endpoints=f[:x]+r'\\\bottomrule\end{tabularx}\end{frame}'
assembled=f[:f.index(r'\R{2}{$\CtwoEndpoint{L}')]+f[x:y]+r'\bottomrule\end{tabularx}\end{frame}'
assembled=assembled.replace('Build the confidence interval','Assemble the confidence interval')
# Remap assembly stages so the new logical frame starts with an empty solution.
for orig,new in [(10,4),(9,3),(8,2)]:assembled=assembled.replace('\\R{'+str(orig)+'}','\\R{'+str(new)+'}')
s=s[:a]+endpoints+'\n'+assembled+s[b:]
a,b,f=getframe('Task 2 -- Full width and interval interpretation')
x=f.index(r'\R{6}{We')
interp=f[x:f.rindex(r'\end{frame}')]
width=f[:x]+r'\end{frame}'
base=f[:f.index(r'\begin{tabularx}')]
interpret=base.replace('Full width and interval interpretation','Interpret the interval')+interp.replace(r'\R{6}',r'\R{2}')+r'\end{frame}'
width=width.replace('Full width and interval interpretation','Full width')
s=s[:a]+width+'\n'+interpret+s[b:]
# Coverage evidence needs slightly tighter vertical spacing, with no content loss.
s=s.replace(r'\begin{column}{.37\textwidth}'+ '\n'+r'\R{2}{Later',r'\begin{column}{.37\textwidth}\setlength{\parskip}{0pt}'+ '\n'+r'\R{2}{Later')
s=s.replace(r'\par\medskip'+ '\n'+r'\begin{columns}[T,onlytextwidth]\begin{column}{.60\textwidth}',r'\par\smallskip'+ '\n'+r'\begin{columns}[T,onlytextwidth]\begin{column}{.60\textwidth}')
p.write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/lesson.tex').write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/handout.tex').write_text(s.replace('[12pt,aspectratio=169]','[handout,12pt,aspectratio=169]'),encoding='utf8')
