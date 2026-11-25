from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex')
s=p.read_text(); a,b=s.split('\\restoregeometry',1)
# Apply diagram geometry and spacing locally; global definitions stay intact.
a=a.replace('\\pagestyle{plain}\n','\\pagestyle{plain}\n\\setlength{\\parskip}{1pt}\n\\renewcommand{\\normalpanel}[2]{%\n \\par\\noindent\\begin{tikzpicture}\\begin{axis}[\n width=.80\\linewidth,height=.85cm,scale only axis,\n xmin=-4,xmax=4,ymin=0,ymax=.46,enlargelimits=false,axis lines=left,\n xtick={-#2,0,#2},xticklabels={$-#2$,0,$+#2$},ytick={0,.4},\n tick label style={font=\\footnotesize},label style={font=\\small},\n title={$C=#1\\%\\qquad -z^*=-#2,\\quad +z^*=+#2$},\n title style={font=\\small,yshift=-2pt}]\n \\addplot[draw=none,fill=black!18,domain=-#2:#2,samples=161]\n {exp(-x*x/2)/sqrt(2*pi)}\\closedcycle;\n \\addplot[black,thick,domain=-4:4,samples=201] {exp(-x*x/2)/sqrt(2*pi)};\n \\draw[dashed] (axis cs:-#2,0)--(axis cs:-#2,.33)\n (axis cs:#2,0)--(axis cs:#2,.33);\n \\node[font=\\small] at (axis cs:0,.17) {$#1\\%$};\n \\end{axis}\\end{tikzpicture}\\par}\n')
a=a.replace('height=4.6cm','height=3.2cm')
a=a.replace('\\guidedresponsebox{12mm}','\\guidedresponsebox[7mm]{14mm}')
p.write_text(a+'\\restoregeometry'+b)
Path('tmp/c3-compact/preview.tex').write_text(a+'\\end{document}')
