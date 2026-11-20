from pathlib import Path
import math,json
root=Path.cwd(); out=root/'book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex'
scaffold=(root/'.agents/skills/global-economics-classroom-activity/assets/template_classroom_activity.tex').read_text()
pre=scaffold[scaffold.index(r'\makeatletter'):scaffold.index(r'\begin{document}')]
pre=pre.replace(r'{../../../preamble/}{../../../../book2026-2027/preamble/}',r'{../../../preamble/}')
# Keep scaffold helpers and plain table families; adapt only the data-table column count.
pre+=r'''
\newenvironment{datagrid}[1]{\par\begingroup\small\setlength{\tabcolsep}{4pt}\setlength{\parskip}{0pt}\renewcommand{\arraystretch}{1.16}\tabularx{\linewidth}{#1}\hline}{\endtabularx\par\endgroup}
\newcommand{\linespace}[1]{\foreach \i in {1,...,#1}{\responseline}}
\newcommand{\blankgrid}[1]{\begin{minipage}[t]{.49\linewidth}\vspace{0pt}\textbf{#1}\par\smallskip\centering
\begin{tikzpicture}[x=1cm,y=1cm]\draw[step=.5,black!18,very thin] (0,0) grid (8,5.5);\draw[->] (0,0)--(8.2,0);\draw[->] (0,0)--(0,5.7);\end{tikzpicture}\par\vspace{.5cm}\end{minipage}}
\newcommand{\emptywork}[1]{\par\begin{tikzpicture}\draw[black!40] (0,0) rectangle (19.8,#1);\end{tikzpicture}\par}
\pgfplotsset{relation/.style={width=.96\linewidth,height=6.6cm,axis lines=left,grid=major,major grid style={black!15},tick label style={font=\small},label style={font=\small},scaled ticks=false,enlargelimits=false,clip=true}}
\newcommand{\normalpanel}[3]{\begin{minipage}[t]{\linewidth}\vspace{0pt}\centering\textbf{#1: $C=#2\%$}\par
\begin{tikzpicture}\begin{axis}[width=\linewidth,height=2.8cm,xmin=-4,xmax=4,ymin=0,ymax=.46,axis lines=left,xlabel={$z$ (unitless)},ylabel={Density},xtick={-#3,0,#3},xticklabels={$-#3$,$0$,$+#3$},ytick={0,.2,.4},tick label style={font=\small},label style={font=\small},scaled ticks=false]
\addplot[draw=none,fill=black!18,domain=-#3:#3,samples=100] {exp(-x*x/2)/sqrt(2*pi)}\closedcycle;
\addplot[black,domain=-4:4,samples=150] {exp(-x*x/2)/sqrt(2*pi)};
\draw[dashed] (axis cs:-#3,0)--(axis cs:-#3,.32) (axis cs:#3,0)--(axis cs:#3,.32);
\node at (axis cs:0,.17) {$C=#2\%$};\end{axis}\end{tikzpicture}\end{minipage}\par}
\newcommand{\normalblank}[1]{\begin{minipage}[t]{.32\linewidth}\vspace{0pt}\textbf{#1}\par\centering\begin{tikzpicture}[x=.65cm,y=8cm]\draw[step=1,black!15,very thin] (-4,0) grid (4,.45);\draw[->] (-4,0)--(4.15,0);\draw[->] (-4,0)--(-4,.47);\foreach \x in {-4,-2,0,2,4}{\draw (\x,0)--(\x,-.008) node[below,font=\small]{\x};}\foreach \y in {0.2,0.4}{\node[left,font=\small] at (-4,\y){\y};}\node[below] at (0,-.05){$z$ (unitless)};\end{tikzpicture}\par\vspace{.7cm}\end{minipage}}
'''
s=[pre,r'''\begin{document}
{\centering{\Large\bfseries C3: Anatomy of a confidence interval\par}Global Economics | Grade 11 | Term 2 | Lesson 1\par}
\textbf{C3} Identifies the components of a confidence interval, including point estimate, critical value, standard error, and margin of error, explaining how each component affects precision and reliability.
\stageheading{Equations and basic procedure}
\textbf{Model and controls.} Estimate a population mean $\mu$ from a simple random sample of independent observations (or a negligible fraction of a much larger population). The population SD $\sigma$ is known. The population is normal or the sample mean is approximately normal. Hold $\bar{x}$ fixed for these comparisons; actual sample means can change between samples.
\noindent\begin{minipage}[t]{.49\linewidth}\vspace{0pt}
\NotationReferenceTable{
$n$ & Sample size & Positive integer count \\
$\mu,\bar{x}$ & Population mean; point estimate & $\bar{x}$ estimates fixed $\mu$ \\
$\sigma$ & Individual population SD & Known; in data units \\
$\mathrm{SE}$ & SD of sample means & $\sigma/\sqrt n$ \\
$\mathrm{MoE}$ & Margin from centre & $z^*\mathrm{SE}$ \\
$L,U,W$ & Bounds; full width & $L=\bar{x}-\mathrm{MoE}$; $U=\bar{x}+\mathrm{MoE}$; $W=U-L=2\mathrm{MoE}$ \\
}\end{minipage}\hfill
\begin{minipage}[t]{.49\linewidth}\vspace{0pt}
\NotationReferenceTable{
$C$ & Nominal confidence & Decimal in formulas; \% on axes \\
$Z,\Phi$ & Standard normal; CDF & $Z\sim N(0,1)$; $\Phi(z)=P(Z\le z)$ \\
$z^*$ & Positive unitless cutoff & $\Phi^{-1}((1+C)/2)$ \\
$(1-C)/2$ & Area in each tail & Outside ideal cutoffs $\pm z^*$ \\
$C_{\rm normal}$ & Coverage using rounded $z^*$ & $2\Phi(z^*)-1$ \\
}\end{minipage}
\textbf{Supplied values (use these throughout):} $80\%:1.282$; $90\%:1.645$; $95\%:1.960$; $99\%:2.576$; $99.9\%:3.291$.
\textbf{Rounding.} Keep square roots and intermediate values unrounded; use the supplied three-decimal $z^*$. Report SE, MoE, endpoints and widths to three decimals in the stated units. Plot using unrounded calculations where possible. Sample sizes are integers.
\begin{enumerate}[leftmargin=*,itemsep=2pt,topsep=2pt]
\item \textbf{A: vary sample size.} Fix $\sigma$, $C$ and $\bar{x}$. Calculate SE and MoE for the five supplied sample sizes; record substitutions and results. Construct graphs 1--3 below.
\item \textbf{B: vary confidence.} Fix $\sigma$, $n$ and $\bar{x}$. Calculate the common SE, then $z^*$ and MoE for the five confidence choices. Construct graphs 4--6 and the three normal panels.
\item Calculate both endpoints and width for every row in A and B. Check symmetry about $\bar{x}$ and $U-L=2\mathrm{MoE}$. Explain how the components affect precision and reliability, using numerical comparisons.
\end{enumerate}
\textbf{Required graphs in every problem; exactly five calculated points on each.}
1. SE vs sample size; 2. MoE vs sample size; 3. MoE vs SE;
4. confidence level vs MoE; 5. critical value vs MoE; 6. confidence level vs critical value.
\textbf{Axes and curves.} ``A vs B'' means A vertically and B horizontally. Label numerical axes and units (counts, monetary units, \%, or unitless). Use actual numerical spacing, including 99\% and 99.9\%. Filled dots denote the five calculated pairs; any theoretical curve must be a separate unmarked line. A continuous sample-size curve only guides the eye between integer sizes.
At fixed $C$, $\mathrm{MoE}=z^*\mathrm{SE}$ has slope $z^*$; at fixed SE, $z^*=\mathrm{MoE}/\mathrm{SE}$ has slope $1/\mathrm{SE}$. Confidence curves follow $100[2\Phi(z^*)-1]$ or $100[2\Phi(\mathrm{MoE}/\mathrm{SE})-1]$ on percentage axes, not straight joins of nominal points.
\textbf{Interpretation.} Narrower intervals mean greater precision. Confidence describes long-run capture of the fixed $\mu$ by repeated-sample intervals under the model, not the probability of $\mu$ after seeing one interval. Rounded cutoffs give theoretical coverage slightly different from nominal $C$.
\clearpage
\stageheading{Worked example}
\problemtitle{1}{Weekly household grocery spending}{A and B}
An analyst estimates the district's mean weekly household grocery bill. The known population SD is $\sigma=30$ thousand COP. Hold $\bar{x}=84$ thousand COP fixed. Assume the model on page 1.
\task{A. Vary sample size.}{Fix $C=95\%$, so $z^*=1.960$. Use $n=25,100,400,900,1600$: the endpoints and three informative intermediate sizes.}
For each row, $\mathrm{SE}=30/\sqrt n$, then $\mathrm{MoE}=1.960(30/\sqrt n)$. At $n=400$, $\sqrt{400}=20$, $\mathrm{SE}=30/20=1.500$, and $\mathrm{MoE}=1.960(1.500)=2.940$ thousand COP. The consolidated table retains every substitution; all SE and MoE values are in thousand COP.
\begin{datagrid}{|r|X|X|}\textbf{$n$ (households)}&\textbf{SE: substitution and result}&\textbf{MoE: substitution and result}\\\hline
25&$30/\sqrt{25}=6.000$&$1.960(6.000)=11.760$\\\hline
100&$30/\sqrt{100}=3.000$&$1.960(3.000)=5.880$\\\hline
400&$30/\sqrt{400}=1.500$&$1.960(1.500)=2.940$\\\hline
900&$30/\sqrt{900}=1.000$&$1.960(1.000)=1.960$\\\hline
1600&$30/\sqrt{1600}=0.750$&$1.960(0.750)=1.470$\\\hline\end{datagrid}
''']
def coords(xs,ys):return ' '.join(f'({x:.9f},{y:.9f})' for x,y in zip(xs,ys))
def graph(title,xlabel,ylabel,opts,points,curve='',labels=''):
 return r'\begin{minipage}[t]{.49\linewidth}\vspace{0pt}\centering\textbf{'+title+r'}\par\begin{tikzpicture}\begin{axis}[relation,xlabel={'+xlabel+'},ylabel={'+ylabel+'},'+opts+']\n'+curve+r'\addplot[only marks,mark=*,mark size=2pt] coordinates {'+points+'};\n'+labels+r'\end{axis}\end{tikzpicture}\end{minipage}'
ns=[25,100,400,900,1600]; se=[30/math.sqrt(n) for n in ns]; moe=[1.96*x for x in se]
s+=[graph('1. Standard error vs sample size','$n$ (households)','SE (thousand COP)','xmin=0,xmax=1700,ymin=0,ymax=6.6,xtick={0,400,800,1200,1600}',coords(ns,se),r'\addplot[black,domain=25:1600,samples=150] {30/sqrt(x)};'),r'\hfill',graph('2. Margin of error vs sample size','$n$ (households)','MoE (thousand COP)','xmin=0,xmax=1700,ymin=0,ymax=13,xtick={0,400,800,1200,1600}',coords(ns,moe),r'\addplot[black,domain=25:1600,samples=150] {58.8/sqrt(x)};'),r'\par\medskip',graph('3. Margin of error vs standard error','SE (thousand COP)','MoE (thousand COP)','xmin=0,xmax=6.5,ymin=0,ymax=13',coords(se,moe),r'\addplot[black,domain=0:6.4] {1.960*x};'),r'''\hfill\begin{minipage}[t]{.49\linewidth}\vspace{0pt}
\textbf{Read and check the graphs.}\par
Dots are the five table rows; unmarked lines are the theoretical relationships. The origin on graph 3 is part of the line, not a sixth calculated point. Finite samples do not reach SE $=0$.\par
Graphs 1 and 2 decrease and flatten: additional households bring diminishing reductions in uncertainty. Quadrupling $n$ from 100 to 400 halves SE from 3.000 to 1.500 and MoE from 5.880 to 2.940 thousand COP.\par
Graph 3 has unitless slope $1.960$; $2.940/1.500=1.960$. Population variability $\sigma=30$ stays fixed even as uncertainty in the mean falls. Nominal confidence remains 95\%; precision improves.\end{minipage}
\clearpage
\textbf{Problem 1 continued --- B. Vary confidence}\par
Fix $n=100$, $\sigma=30$ thousand COP and $\bar{x}=84$ thousand COP. First $\mathrm{SE}=30/\sqrt{100}=3.000$ thousand COP for every confidence choice. Look up $z^*$, then multiply by this common SE.
\begin{datagrid}{|r|r|X|}\textbf{$C$ (\%)}&\textbf{$z^*$ (unitless)}&\textbf{MoE: substitution and result (thousand COP)}\\\hline
80&1.282&$1.282(3.000)=3.846$\\\hline
90&1.645&$1.645(3.000)=4.935$\\\hline
95&1.960&$1.960(3.000)=5.880$\\\hline
99&2.576&$2.576(3.000)=7.728$\\\hline
99.9&3.291&$3.291(3.000)=9.873$\\\hline\end{datagrid}
''']
cs=[80,90,95,99,99.9];zs=[1.282,1.645,1.960,2.576,3.291];ms=[3*z for z in zs]
# Accurate theoretical normal curve sampled with erf, distinct from the five nominal dots.
zz=[1.2+i*(2.2/120) for i in range(121)];cc=[100*math.erf(z/math.sqrt(2)) for z in zz]
s += [graph('4. Confidence level vs margin of error','MoE (thousand COP)','$C$ (\\%)','xmin=3.5,xmax=10.3,ymin=78,ymax=101,ytick={80,85,90,95,100}',coords(ms,cs),r'\addplot[black,no marks] coordinates {'+coords([3*z for z in zz],cc)+'};'),r'\hfill',graph('5. Critical value vs margin of error','MoE (thousand COP)','$z^*$ (unitless)','xmin=0,xmax=10.3,ymin=0,ymax=3.5',coords(ms,zs),r'\addplot[black,domain=0:10.2] {x/3};'),r'\par\medskip',graph('6. Confidence level vs critical value','$z^*$ (unitless)','$C$ (\\%)','xmin=1.1,xmax=3.5,ymin=78,ymax=103,ytick={80,85,90,95,100}',coords(zs,cs),r'\addplot[black,no marks] coordinates {'+coords(zz,cc)+'};',r'\node[above right,font=\small] at (axis cs:1.282,80){A};\node[above left,font=\small] at (axis cs:1.960,95){M};\node[below left,font=\small] at (axis cs:3.291,99.9){E};'),r'''\hfill\begin{minipage}[t]{.49\linewidth}\vspace{0pt}
\normalpanel{A}{80}{1.282}
\normalpanel{M}{95}{1.960}
\normalpanel{E}{99.9}{3.291}
\end{minipage}
\clearpage
\textbf{Problem 1 continued --- Normal panels and interval components}\par
Graph 6 and the three adjacent panels use matching A, M and E labels: A is the lower endpoint $(1.282,80)$; M is the representative interior case $(1.960,95)$; E is the upper endpoint $(3.291,99.9)$. The 95\% case is not the arithmetic midpoint. All panels use $-4\le z\le4$ and density $0$ to $0.46$, with cutoffs $-z^*$ and $+z^*$.
The central grayscale labels show nominal $C$. Actual shaded areas with rounded cutoffs are $100[2\Phi(z^*)-1]\approx80.01574\%,95.00042\%,99.90017\%$, respectively. Larger $z^*$ moves both cutoffs outward under the same normal curve.
\par
\textbf{Read and check the graphs.}\par
Graph 5 is a line through the origin: $z^*=\mathrm{MoE}/3$, with slope $1/3$ per thousand COP. Check $7.728/3=2.576$.\par
Graphs 4 and 6 are nonlinear and flatten towards 100\%. Their five dots use nominal percentages; the unmarked curves use the normal CDF. The tiny discrepancy comes from rounded $z^*$, not a change of axes.\par
In graph 6, A is the lower endpoint $(1.282,80)$, M is the representative interior case $(1.960,95)$, and E is the upper endpoint $(3.291,99.9)$. M is not the arithmetic midpoint. The panels are beside graph 6.\par
Increasing confidence raises the cutoff and margin while SE and the centre stay fixed. This increases reliability as nominal long-run coverage, with less precision.\par\task{Endpoints and widths.}{Every row uses $L=84-\mathrm{MoE}$, $U=84+\mathrm{MoE}$ and $W=2\mathrm{MoE}$. At A's $n=400$: $L=84-2.940=81.060$, $U=84+2.940=86.940$ and $W=2(2.940)=5.880$ thousand COP.}
\begin{datagrid}{|l|>{\raggedleft\arraybackslash}X|>{\raggedleft\arraybackslash}X|>{\raggedleft\arraybackslash}X|>{\raggedleft\arraybackslash}X|}\textbf{Investigation / setting}&\textbf{MoE}&\textbf{$L$}&\textbf{$U$}&\textbf{$W$}\\\hline
A: $n=25$&11.760&72.240&95.760&23.520\\\hline
A: $n=100$&5.880&78.120&89.880&11.760\\\hline
A: $n=400$&2.940&81.060&86.940&5.880\\\hline
A: $n=900$&1.960&82.040&85.960&3.920\\\hline
A: $n=1600$&1.470&82.530&85.470&2.940\\\hline
B: $C=80\%$&3.846&80.154&87.846&7.692\\\hline
B: $C=90\%$&4.935&79.065&88.935&9.870\\\hline
B: $C=95\%$&5.880&78.120&89.880&11.760\\\hline
B: $C=99\%$&7.728&76.272&91.728&15.456\\\hline
B: $C=99.9\%$&9.873&74.127&93.873&19.746\\\hline\end{datagrid}
All numerical columns above are in thousand COP. For B at 99\%: $L=84-7.728=76.272$, $U=84+7.728=91.728$ and $W=2(7.728)=15.456$. Thus the interval is $[76.272,91.728]$ thousand COP.
\textbf{Checks.} $(76.272+91.728)/2=84$ and $91.728-76.272=15.456$. The 95\%, $n=100$ row agrees in both investigations because all controls coincide. Each endpoint pair is symmetric, all widths are positive, and monetary units agree throughout.
\textbf{Interpret in context.} $\bar{x}=84$ locates the grocery-bill estimate; known $\sigma=30$ describes individual household spread, whereas SE describes repeated-sample means. The multiplier $z^*$ converts SE to a margin; the margin determines each bound and half the width. At fixed 95\%, increasing $n$ from 100 to 400 halves the interval width from 11.760 to 5.880 thousand COP without changing nominal coverage.
At fixed $n=100$, raising confidence from 90\% to 99\% widens the interval from 9.870 to 15.456 thousand COP: endpoints move outward and precision falls. A nominal 99\% procedure captures the fixed district mean in about 99\% of repeated samples under the model; it does not assign a 99\% probability to that fixed mean in this observed interval.
''']
# Every fresh problem has identical A, B and components requirements, with no solutions in independent pages.
problems=[(2,'Delivery charges for local businesses','A business association estimates the mean charge for a local delivery.',24,72,'thousand COP',[36,100,225,400,900],100),(3,'Weekly market-stall revenue','A market office estimates mean weekly revenue per stall.',45,180,'thousand COP',[25,100,225,625,1600],225),(4,'Freight handling fees','A port analyst estimates the mean handling fee per container.',72,310,'USD',[36,144,324,576,1296],144),(5,'Monthly internet costs','A district estimates mean monthly internet expenditure per small business.',35,125,'thousand COP',[49,100,196,400,1225],196)]
validation=[]
for num,title,context,sd,mean,unit,nn,base in problems:
 guided=num==2
 validation.append(dict(problem=num,A=[dict(n=n,SE=sd/math.sqrt(n),MoE=1.96*sd/math.sqrt(n),L=mean-1.96*sd/math.sqrt(n),U=mean+1.96*sd/math.sqrt(n),W=3.92*sd/math.sqrt(n)) for n in nn],B=[dict(C=c,z=z,SE=sd/math.sqrt(base),MoE=z*sd/math.sqrt(base),L=mean-z*sd/math.sqrt(base),U=mean+z*sd/math.sqrt(base),W=2*z*sd/math.sqrt(base),coverage_percent=100*math.erf(z/math.sqrt(2))) for c,z in zip(cs,zs)]))
 s+=[r'\clearpage']
 if num==2:s += [r'\stageheading{Guided Example}']
 if num==3:s += [r'\stageheading{Independent Practice}']
 s += [rf'\problemtitle{{{num}}}{{{title}}}{{A and B}}',context+rf' Known population SD: $\sigma={sd}$ {unit}; fixed point estimate: $\bar{{x}}={mean}$ {unit}. The opening model assumptions apply.',rf'\task{{A. Vary sample size.}}{{Hold $\sigma={sd}$ {unit}, $C=95\%$ and $\bar{{x}}={mean}$ {unit} fixed. Use exactly $n={",".join(map(str,nn))}$. Calculate SE and MoE, and construct graphs 1--3 with exactly five points each.}}']
 if guided:
  s += [rf'\textbf{{1. Controls and starter.}} The first size gives $\mathrm{{SE}}={sd}/\sqrt{{{nn[0]}}}=4.000$ {unit}. Complete its margin and the remaining rows, showing substitutions. $z^*=$ \rule{{1cm}}{{.3pt}}.',r'\begin{datagrid}{|r|X|X|}\textbf{$n$}&\textbf{SE: calculation and units}&\textbf{MoE: calculation and units}\\\hline']
  for i,n in enumerate(nn):s += [str(n)+('&$24/\sqrt{36}=4.000$&' if i==0 else '&&')+r'\rule{0pt}{.65cm}\\\hline']
  s += [r'\end{datagrid}',r'\textbf{2. Plot.} Number and label axes with actual spacing. Plot five distinct points per graph; identify any theoretical line separately.']
 else:s += [r'\textbf{Calculations (show substitutions and units).}',r'\emptywork{3.8}']
 s += [r'\par\blankgrid{1. Standard error vs sample size}\hfill\blankgrid{2. Margin of error vs sample size}\par',r'\blankgrid{3. Margin of error vs standard error}\hfill\begin{minipage}[t]{.49\linewidth}\vspace{0pt}\textbf{A: interpretation and numerical comparisons}\par']
 if guided:s += [r'\textbf{3. Explain.} What changes and what stays fixed? Compare two rows and describe the shapes, precision and nominal coverage.']
 s += [r'\linespace{7}\end{minipage}',r'\clearpage',rf'\textbf{{Problem {num} continued --- B. Vary confidence}}',rf'Fix $n={base}$, $\sigma={sd}$ {unit} and $\bar{{x}}={mean}$ {unit}. Use exactly $C=80\%,90\%,95\%,99\%,99.9\%$ and the supplied critical values. Calculate SE, $z^*$ and MoE. Construct graphs 4--6 with exactly five points each.']
 if guided:
  s += [r'\textbf{4. Complete the confidence table.} The fixed SE is \rule{1.4cm}{.3pt} with units \rule{2cm}{.3pt}. Leave it unchanged across these rows.',r'\begin{datagrid}{|r|r|X|}\textbf{$C$ (\%)}&\textbf{$z^*$}&\textbf{MoE: calculation and units}\\\hline']
  for i,(c,z) in enumerate(zip(cs,zs)):s += [str(c)+('&1.282&' if i==0 else '&&')+r'\rule{0pt}{.65cm}\\\hline']
  s += [r'\end{datagrid}',r'\textbf{5. Plot and connect.} Use nominal percentages for the dots and true numerical spacing. Identify the 80\%, 95\% and 99.9\% points on graph 6 with A, M and E.']
 else:s += [r'\textbf{Calculations (show substitutions and units).}',r'\emptywork{3.8}']
 s += [r'\par\blankgrid{4. Confidence level vs margin of error}\hfill\blankgrid{5. Critical value vs margin of error}\par',r'\blankgrid{6. Confidence level vs critical value}\hfill\begin{minipage}[t]{.49\linewidth}\vspace{0pt}\textbf{B: interpretation and numerical comparisons}\par']
 if guided:s += [r'\textbf{6. Explain.} Compare two confidence choices. What happens to SE, the margin, precision and reliability? Which graph is linear, and what is its slope?']
 s += [r'\linespace{7}\end{minipage}',r'\clearpage',rf'\textbf{{Problem {num} continued --- Normal panels and interval components}}',r'Construct three standard normal panels for 80\%, 95\% and 99.9\%, using identical scales ($-4\le z\le4$, density $0$ to $0.46$). Shade the central region in grayscale; label $C$ and both cutoffs $-z^*$ and $+z^*$. Connect them to the corresponding points of graph 6. Explain why 95\% is a representative interior case and distinguish nominal confidence from coverage with rounded cutoffs.',r'\par\normalblank{80\%}\hfill\normalblank{95\%}\hfill\normalblank{99.9\%}\par']
 if guided:
  s += [r'\textbf{7. Complete intervals and checks.} For all five rows in A and all five in B, calculate $L$, $U$ and $W$. Show an endpoint substitution and a symmetry/width check below the table.',r'\begin{datagrid}{|l|X|X|X|}\textbf{Setting}&\textbf{$L$}&\textbf{$U$}&\textbf{$W$}\\\hline']
  for n in nn:s += [rf'A: $n={n}$&&&\rule{{0pt}}{{.65cm}}\\\hline']
  for c in cs:s += [rf'B: $C={c}\%$&&&\rule{{0pt}}{{.65cm}}\\\hline']
  s += [r'\end{datagrid}',r'\linespace{2}',r'\textbf{8. Conclude.} Identify the point estimate, critical value, SE, margin, endpoints and width in this context. Use numbers to distinguish greater precision from greater reliability and interpret confidence in repeated sampling.',r'\linespace{3}']
 else:
  s += [r'For every setting in A and B, calculate both interval endpoints and full width, with units. Include numerical checks. Identify and interpret the point estimate, critical value, SE, margin, endpoints and width. Explain the graph shapes, precision and reliability with numerical comparisons and a correct repeated-sampling interpretation.',r'\textbf{Interval calculations and checks}',r'\emptywork{6.5}',r'\textbf{Components, normal-panel explanation and conclusions}',r'\linespace{5}']
s += [r'\end{document}']
out.write_text('\n'.join(s),encoding='utf-8')
# Private verification remains outside the student handout.
for p in validation:
 for family in ['A','B']:
  assert len(p[family])==5
  for r in p[family]:
   assert math.isclose(r['U']-r['L'],r['W']) and r['MoE']>0
 assert all(p['A'][i]['SE']>p['A'][i+1]['SE'] for i in range(4))
 assert all(p['B'][i]['MoE']<p['B'][i+1]['MoE'] for i in range(4))
(root/'tmp/pdfs/c3-classroom/private_verification.json').write_text(json.dumps(validation,indent=2))
print(out);print('Privately checked all 40 fresh investigation rows, endpoints, widths and monotonicity.')

