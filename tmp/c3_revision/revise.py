from pathlib import Path
import re

p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex')
s=p.read_text()
intro=r'''
\stageheading{Equations and basic procedure}
A confidence interval estimates an unknown population mean $\mu$ and shows the uncertainty around a sample mean. Its width depends on population variability, sample size, and confidence.
\begingroup
\small\setlength{\tabcolsep}{3pt}\setlength{\extrarowheight}{0pt}
\setlength{\parskip}{0pt}\renewcommand{\arraystretch}{1}
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{.12\linewidth}>{\raggedright\arraybackslash}p{.23\linewidth}>{\raggedright\arraybackslash}X@{}}
\toprule
\textbf{Symbol} & \textbf{Concept} & \textbf{Definition and formula}\\\midrule
$\mathrm{CI}$ & Confidence interval & Range estimating $\mu$: $[\bar{x}-\mathrm{MoE},\bar{x}+\mathrm{MoE}]$; in the measured units.\\
$\bar{x}$ & Point estimate & Sample mean estimating $\mu$; centre of the interval, in the measured units.\\
$C$ & Confidence level & Nominal long-run percentage of intervals covering $\mu$ under the model.\\
$z^*$ & Critical value & Positive standard normal cutoff with central area $C/100$ when $C$ is a percentage; unitless.\\
$\mathrm{SE}$ & Standard error & Standard deviation of sample means: $\mathrm{SE}=\sigma/\sqrt n$; in the measured units.\\
$\mathrm{MoE}$ & Margin of error & Distance from the estimate to either endpoint: $\mathrm{MoE}=z^*\mathrm{SE}$; in the measured units.\\
$\sigma$ & Population standard deviation & Known spread of individual population values; in the measured units.\\
$n$ & Sample size & Number of sampled units; a positive integer count.\\
\bottomrule
\end{tabularx}\par\endgroup

\textbf{Common assumptions.} Unless stated otherwise, use a simple random sample of independent observations from a much larger population, known $\sigma$, and a normal population or approximately normal sample mean.

\stageheading{General tasks}
\task{Task 1:}{Investigate SE, MoE, and sample size with $\sigma$ and confidence fixed.}
Calculate SE and MoE for the five sample sizes, assigned A--E in the stated order. In the grid, draw (top left) SE vs $n$, (top right) MoE vs $n$, and (bottom left) MoE vs SE. Here ``$y$ vs $x$'' places $x$ horizontally and $y$ vertically. Draw the decreasing $1/\sqrt n$ curves for the first two relationships and the line $\mathrm{MoE}=z^*\mathrm{SE}$ for the third. Continuous sample-size curves guide the eye between integer sizes.

\task{Task 2:}{Investigate confidence, critical value, and MoE with $n$ and $\sigma$ fixed.}
Calculate the fixed SE and the MoE for each supplied $(C,z^*)$ pair. Use these five cases in every problem:
\begin{datagrid}{|l|X|X|X|X|X|}ID&A&B&C&D&E\\\hline
$C$ (\%)&80&90&95&99&99.9\\\hline
$z^*$&1.282&1.645&1.960&2.576&3.291\\\hline\end{datagrid}
Draw (top left) confidence vs MoE, (top right) critical value vs MoE, and (bottom left) confidence vs critical value. Use increasing confidence curves and the line $z^*=\mathrm{MoE}/\mathrm{SE}$.

\textbf{For both tasks.} Plot all five cases in each relationship graph, label A--E with their $(x,y)$ coordinates, and draw the corresponding curve or line. Keep each ID attached to the same case within a task. Use true numerical spacing, including confidence levels near 100\%; follow the supplied axes and scales. SE and MoE have the context's monetary units; $n$ counts sampled units, $C$ uses percent, and $z^*$ is unitless. Use the supplied rounded cutoffs, retain unrounded intermediate results, and report calculated coordinates to three decimals; keep given counts and percentages as supplied. The bottom-right cell is calculation workspace in student problems; supplementary illustrations appear only in the worked example.
\clearpage
'''
marker=r'\pgfplotsset{relation/.append style={height=5.5cm}}'
s=s.replace(marker,intro+'\n'+marker,1)
# Consolidate each problem's givens ahead of its first task; retain all grids and solutions.
ns=['25,100,400,900,1600','36,100,225,400,900','25,100,225,625,1600','36,144,324,576,1296','49,100,196,400,1225']
sigmas=[30,24,45,72,35]
fixed=[100,100,225,144,196]
units=['thousand COP','thousand COP','thousand COP','USD','thousand COP']
for i in range(5):
    start=s.index('\\problemtitle{'+str(i+1)+'}')
    end=s.index(r'\end{document}',start) if i==4 else s.index('\\problemtitle{'+str(i+2)+'}',start)
    block=s[start:end]
    a=block.index(r'\task{Task 1:}')
    b=block.index(r'\textbf{Solution.}',a) if i==0 else block.index(r'\par\smallskip',a)
    givens=(f'Population SD is known: $\\sigma={sigmas[i]}$ {units[i]}; the common assumptions apply. '
            f'For Task 1, fix $C=95\\%$ ($z^*=1.960$) and use $n={ns[i]}$ for A--E, respectively. '
            f'For Task 2, fix $n={fixed[i]}$ and the same $\\sigma$, using the five general $(C,z^*)$ cases.\n')
    block=block[:a]+givens+r'\task{Task 1:}{Apply general Task 1 to the five sample sizes above.}'+'\n'+block[b:]
    a=block.index(r'\task{Task 2:}')
    b=block.index(r'\textbf{Solution.}',a) if i==0 else block.index(r'\par\smallskip',a)
    block=block[:a]+f'\\task{{Task 2:}}{{Apply general Task 2 with $n={fixed[i]}$ and the five general confidence cases.}}\n'+block[b:]
    s=s[:start]+block+s[end:]

start=s.index(r'\centering\begin{tikzpicture}\begin{axis}[',s.index(r'\textbf{Explanatory confidence-interval comparison}'))
end=s.index(r'\end{axis}\end{tikzpicture}\par',start)+len(r'\end{axis}\end{tikzpicture}\par')
chart=r'''\centering\begin{tikzpicture}\begin{axis}[
width=.98\linewidth,height=4.6cm,xmin=.45,xmax=3.65,ymin=70,ymax=100,
axis x line=bottom,axis y line=left,xtick={1,2,3},
xticklabels={$n=25$,$n=400$,$n=1600$},ytick={70,75,80,84,90,95,100},
tick label style={font=\footnotesize},label style={font=\footnotesize},
ylabel={Weekly spending (thousand COP)},scaled ticks=false,clip=false]
\draw[dashed,black!65] (axis cs:.45,84)--(axis cs:3.65,84);
\node[font=\footnotesize,anchor=south] at (axis cs:2.2,97.5) {Shared estimate $\bar{x}=84$};
'''
for x,lo,hi in [(1,'72.240','95.760'),(2,'81.060','86.940'),(3,'82.530','85.470')]:
    chart+=f'\\draw[thick] (axis cs:{x},{lo})--(axis cs:{x},{hi});\n'
    chart+=f'\\draw[line width=1.3pt] (axis cs:{x-.16:.2f},{lo})--(axis cs:{x+.16:.2f},{lo})\n(axis cs:{x-.16:.2f},{hi})--(axis cs:{x+.16:.2f},{hi});\n'
    chart+=f'\\fill (axis cs:{x},84) circle (2.6pt);\n'
    for val,anchor in [(lo,'north'),(hi,'south')]:
        chart+=f'\\node[font=\\footnotesize,anchor={anchor},inner sep=2pt] at (axis cs:{x},{val}) {{{val}}};\n'
chart+=r'\end{axis}\end{tikzpicture}\par'
s=s[:start]+chart+s[end:]
start=s.index('Both SE and MoE decrease')
end=s.index(r'\clearpage',start)
s=s[:start]+r'''SE and MoE are proportional to $1/\sqrt n$; MoE vs SE has slope $1.960$. Larger samples give narrower intervals and greater precision at the same 95\% confidence.
'''+s[end:]
start=s.index('At fixed SE,')
end=s.index(r'\clearpage',start)
s=s[:start]+r'''At fixed SE, MoE increases with $z^*$. Higher confidence requires a larger $z^*$, producing wider intervals and lower precision. The shaded regions show the nominal confidence levels; rounded cutoffs produce slightly different areas.

The panels show cases A, C and E on shared scales: $-4\le z\le4$ and $0\le f(z)\le0.46$.
'''+s[end:]
p.write_text(s)
