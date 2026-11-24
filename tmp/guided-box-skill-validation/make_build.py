from pathlib import Path
base=Path('.agents/skills/global-economics-classroom-activity')
s=(base/'assets/template_classroom_activity.tex').read_text(encoding='utf-8')
s=s.replace('\\def\\input@path{{../../../preamble/}{../../../../book2026-2027/preamble/}}', '\\def\\input@path{{C:/Users/orlan/Desktop/SanBartolo/global_economics/book2026-2027/preamble/}}')
needle='\\par\\clearpage % Flush Guided Example before restoring all helper definitions.'
test=r'''
% Representative validation only: not part of the reusable scaffold.
\Needspace{30\baselineskip}
\task{Task 3 --- Response dimensions and corresponding representations.}{}
\subtaskheading{1}{Numerical and symbolic responses}
\guidedpair{
\textbf{Case A: calculations.}\par
Supply the count: $n=\guidedresponsebox{12mm}$ units.
\[
q=\guidedresponsebox[12mm]{16mm},\qquad
x=\guidedresponsebox[10mm]{35mm}
\]
Complete the numerator:
\[
q=\frac{\guidedresponsebox[9mm]{12mm}}{12}.
\]
}{
\textbf{Case B: calculations.}\par
Supply the count: $n=\guidedresponsebox{12mm}$ units.
\[
\begin{aligned}
q&=\guidedresponsebox[12mm]{16mm}\\[4pt]
x&=\guidedresponsebox[10mm]{35mm}\\[4pt]
u&=\frac{3}{\guidedresponsebox[9mm]{12mm}}
\end{aligned}
\]
}
\Needspace{22\baselineskip}
\subtaskheading{2}{Events and graphs}
\guidedpair{
\textbf{Case A: event and graph.}\par
Name the event: \guidedresponsebox[10mm]{45mm}.
\par\nopagebreak[4]
\begin{tikzpicture}[x=7mm,y=7mm]
\draw[step=1,black!15] (0,0) grid (6,3);
\draw[->] (0,0)--(6.5,0) node[right] {$t$};
\draw[->] (0,0)--(0,3.5) node[above] {$v$};
\end{tikzpicture}
}{
\textbf{Case B: event and graph.}\par
Name the event: \guidedresponsebox[10mm]{45mm}.
\par\nopagebreak[4]
\begin{tikzpicture}[x=7mm,y=7mm]
\draw[step=1,black!15] (0,0) grid (6,3);
\draw[->] (0,0)--(6.5,0) node[right] {$t$};
\draw[->] (0,0)--(0,3.5) node[above] {$v$};
\end{tikzpicture}
}
\Needspace{12\baselineskip}
\guidedpair{
\subtaskheading{3}{Case A meaning}
Interpret the quantity in context over repeated observations.
\par\nopagebreak[4]\noindent
\guidedresponsebox[25mm]{\dimexpr\linewidth-1pt\relax}
}{
\subtaskheading{3}{Case B meaning}
Interpret the quantity in context over repeated observations.
\par\nopagebreak[4]\noindent
\guidedresponsebox[25mm]{\dimexpr\linewidth-1pt\relax}
}
'''
s=s.replace(needle,test+'\n'+needle)
s=s.replace('\\endgroup\n\n% Exactly five UNSOLVED',r'''\endgroup
\ifdefined\guidedresponsebox\errmessage{Guided response helper leaked}\fi
\ifdefined\guidedpair\errmessage{Guided pair helper leaked}\fi

% Exactly five UNSOLVED''')
s=s.replace('\\end{document}',r'''% Test that appended material cannot see the response helpers.
\ifdefined\guidedresponsebox\errmessage{Response helper reached appended material}\fi
\ifdefined\guidedpair\errmessage{Pair helper reached appended material}\fi
\end{document}''')
Path('tmp/guided-box-skill-validation/representative.tex').write_text(s,encoding='utf-8')
