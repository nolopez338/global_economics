from pathlib import Path
import re

p = Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex')
s = p.read_text(encoding='utf-8')
s = s.replace(r'width=.98\linewidth,height=9cm,', r'width=.86\linewidth,height=4.8cm,scale only axis,')
s = s.replace(r'ytick={0,.25,.5,.75,1},ylabel={Probability},grid=major,', r'ytick={0,.25,.5,.75,1},grid=major,')
s = s.replace(r'legend style={at={(.5,-.2)},anchor=north,legend columns=3,', r'legend style={at={(.5,-.27)},anchor=north,legend columns=2,')
s = s.replace('cTwoPhantom/.style={cTwoGuideColor,densely dashed,line width=1.5pt},', 'cTwoPhantom/.style={cTwoGuideColor,densely dashed,line width=.9pt},')
s = s.replace(r'\newcommand{\cTwoPhantom}[3]{%', r'''% Coordinates are saved inside their own axes, then joined after both axes end.
\tikzset{cTwoCorrespondence/.style={gray!55,line width=.25pt,-{Stealth[length=2.5pt,width=2pt]}}}
\newcommand{\cTwoCorrespondence}[1]{%
\draw[cTwoCorrespondence] (cTwoMassMid-#1) -- (cTwoShadowMid-#1);}
\newcommand{\cTwoPhantom}[3]{%
\coordinate (cTwoShadowMid-#1) at (axis cs:#1,{#3+(#2)/2});''')
s = s.replace(r'\newcommand{\cTwoMass}[2]{%', r'''\newcommand{\cTwoMass}[2]{%
\coordinate (cTwoMassMid-#1) at (axis cs:#1,{(#2)/2});''')
start = s.index(r'\newcommand{\cTwoConnectionReading}')
end = s.index(r'\begin{document}', start)
s = s[:start] + r'''\newcommand{\cTwoConnectionReading}{%
\textbf{How to read the stacked graphs.} The top graph shows the CDF and pale
dashed PMF shadows; the bottom graph shows the original blue PMF stems.
The plotting areas have identical horizontal limits, support ticks, numerical
spacing, widths and vertical scales. Stems show isolated masses, not positive
probability at every point along a segment. Each shadow represents a jump size:
it translates the mass vertically from $0$ to $\cTwoCDFHL{F_X(a^-)}$, keeping
its horizontal coordinate and physical length. Its top is $\cTwoCDFHL{F_X(a)}$, so
$\cTwoCDFHL{F_X(a)}-\cTwoCDFHL{F_X(a^-)}=\cTwoMassHL{p_X(a)}$.
Thin upward arrows show correspondence from each bottom stem's midpoint
$(a,p_X(a)/2)$ to its top shadow's midpoint $(a,F_X(a^-)+p_X(a)/2)$,
including the smallest support value, where $F_X(a^-)=0$.
Shadows are neither extra masses nor extra CDF values at the cutoff.
CDF filled points give the included values; open points exclude the lower
heights. Pale shadow top dots sit behind the CDF endpoint markers.}

''' + s[end:]
pattern = re.compile(r'\\begin\{center\}\\begin\{tikzpicture\}\n\\begin\{axis\}\[cTwoCombined,(.*?)\]\n(.*?)\\end\{axis\}\\end\{tikzpicture\}\\end\{center\}', re.S)
count = 0
def convert(m):
    global count
    count += 1
    opts, body = m.groups()
    masses = re.findall(r'\\cTwoMass\{([^}]+)\}\{([^}]+)\}\n', body)
    assert masses
    body = re.sub(r'\\cTwoMass\{[^}]+\}\{[^}]+\}\n', '', body)
    body = re.sub(r'\\addlegendimage.*?\\addlegendentry\{[^}]+\}\n', '', body)
    # One shared option style guarantees identical axis geometry and support.
    return (r'\begin{center}\begin{minipage}{\linewidth}\centering'+'\n'
        + r'\begin{tikzpicture}'+'\n'
        + r'\pgfplotsset{cTwoSupport/.style={'+opts+'}}\n'
        + r'\begin{axis}[cTwoCombined,cTwoSupport,name=cTwoTop,anchor=south west,'+'\n'
        + r'ylabel={$\cTwoCDFHL{F_X(x)}$},yticklabel={$\cTwoCDFHL{\pgfmathprintnumber{\tick}}$}]'+'\n'
        + body + r'\end{axis}'+'\n'
        + r'\begin{axis}[cTwoCombined,cTwoSupport,at={(cTwoTop.south west)},'+'\n'
        + r'anchor=north west,yshift=-1.65cm,ylabel={$\cTwoMassHL{p_X(x)}$},'+'\n'
        + r'yticklabel={$\cTwoMassHL{\pgfmathprintnumber{\tick}}$}]'+'\n'
        + ''.join(r'\cTwoMass{'+a+'}{'+v+'}\n' for a,v in masses)
        + r'\addlegendimage{cTwoStep}\addlegendentry{Top: CDF steps}'+'\n'
        + r'\addlegendimage{cTwoPhantom,mark=*}\addlegendentry{Top: PMF shadows (jump sizes)}'+'\n'
        + r'\addlegendimage{cTwoMass,mark=*}\addlegendentry{Bottom: PMF stems}'+'\n'
        + r'\addlegendimage{cTwoCorrespondence}\addlegendentry{Midpoint correspondence}'+'\n'
        + r'\end{axis}'+'\n'
        + ''.join(r'\cTwoCorrespondence{'+a+'}\n' for a,v in masses)
        + r'\end{tikzpicture}\end{minipage}\end{center}')
s = pattern.sub(convert, s)
assert count == 12, count
s = s.replace(r'\textbf{Same distribution, two representations.}', r'\textbf{Same distribution: CDF above, PMF below.}')
p.write_text(s, encoding='utf-8')
print(f'Converted {count} connection graphs.')
