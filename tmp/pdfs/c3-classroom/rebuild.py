from pathlib import Path
import math

root = Path.cwd()
out = root/'book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex'
preamble = r'''% Mathematical and graphical reference: ../1-practice_activities/G11_T2_L1_C3_practice.tex
% User scope: retain the existing three independent exercises; exactly two tasks per problem.
\makeatletter
\def\input@path{{../../../preamble/}}
\makeatother
\input{preamble.tex}
\geometry{letterpaper,margin=0.25in}
\pagestyle{empty}
\linespread{1.04}
\setlength{\parskip}{4pt}
\raggedbottom
\newcommand{\stageheading}[1]{\par{\centering\large\bfseries #1\par}}
\newcommand{\problemtitle}[2]{\par\textbf{#1. #2}\par}
\newcommand{\task}[2]{\par\textbf{#1} #2\par}
\newenvironment{datagrid}[1]{\par\begingroup\small\setlength{\tabcolsep}{4pt}\setlength{\parskip}{0pt}\renewcommand{\arraystretch}{1.16}\tabularx{\linewidth}{#1}\hline}{\endtabularx\par\endgroup}
\pgfplotsset{relation/.style={width=.94\linewidth,height=7.4cm,axis lines=left,
 grid=major,major grid style={black!15},tick label style={font=\small},
 label style={font=\small},scaled ticks=false,enlargelimits=false,clip=true,
 tick label style={/pgf/number format/1000 sep={}}}}
% Reference label format, ordinary grayscale typography, five IDs per graph.
\newcommand{\PointLabel}[7]{%
 \node[font=\small,inner sep=2pt,anchor=#7] (point#1)
 at (axis description cs:#5,#6) {#1: $(#3,\,#4)$};
 \draw[black!70,line width=.35pt,shorten <=2.5pt] (axis cs:#2)--(point#1);
}
\newcommand{\LabelTemplates}{%
 \node[anchor=east,font=\small] at (axis description cs:.97,.93) {A: $(\underline{\hspace{.65cm}},\,\underline{\hspace{.65cm}})$};
 \node[anchor=east,font=\small] at (axis description cs:.97,.83) {B: $(\underline{\hspace{.65cm}},\,\underline{\hspace{.65cm}})$};
 \node[anchor=east,font=\small] at (axis description cs:.97,.73) {C: $(\underline{\hspace{.65cm}},\,\underline{\hspace{.65cm}})$};
 \node[anchor=east,font=\small] at (axis description cs:.97,.63) {D: $(\underline{\hspace{.65cm}},\,\underline{\hspace{.65cm}})$};
 \node[anchor=east,font=\small] at (axis description cs:.97,.53) {E: $(\underline{\hspace{.65cm}},\,\underline{\hspace{.65cm}})$};}
\newcommand{\workarea}{\begin{minipage}[t]{.49\linewidth}\vspace{0pt}
 \textbf{Calculation workspace}\par\smallskip
 \begin{tikzpicture}\draw[black!40] (0,0) rectangle (9.65,6.5);\end{tikzpicture}
 \end{minipage}}
\newcommand{\normalpanel}[2]{\begin{minipage}[t]{.32\linewidth}\vspace{0pt}\centering
 \textbf{$C=#1\%$}\par\medskip
 \begin{tikzpicture}\begin{axis}[width=.95\linewidth,height=5.4cm,
 xmin=-4,xmax=4,ymin=0,ymax=.46,enlargelimits=false,axis lines=left,
 xlabel={$z$ (unitless)},ylabel={Density},xtick={-#2,#2},
 xticklabels={$-#2$,$+#2$},ytick={0,.2,.4},
 tick label style={font=\small},label style={font=\small}]
 \addplot[draw=none,fill=black!18,domain=-#2:#2,samples=161]
 {exp(-x*x/2)/sqrt(2*pi)}\closedcycle;
 \addplot[black,thick,domain=-4:4,samples=201] {exp(-x*x/2)/sqrt(2*pi)};
 \draw[dashed] (axis cs:-#2,0)--(axis cs:-#2,.33)
 (axis cs:#2,0)--(axis cs:#2,.33);
 \node at (axis cs:0,.17) {$#1\%$};
 \end{axis}\end{tikzpicture}\par
 $-z^*=-#2,\quad +z^*=+#2$
 \end{minipage}}
\begin{document}
{\centering{\Large\bfseries C3: Anatomy of a confidence interval\par}
Global Economics | Grade 11 | Term 2 | Lesson 1\par}
\textbf{C3} Identifies the components of a confidence interval, including point estimate, critical value, standard error, and margin of error, explaining how each component affects precision and reliability.
'''
parts = [preamble]
def add(s):
    if s.strip(): parts.append(s.rstrip())
conf = [80,90,95,99,99.9]
zs = [1.282,1.645,1.960,2.576,3.291]
ids = 'ABCDE'
def graph(title, xl, yl, opts, points=None, curve=None, kind=0):
    s = '\\begin{minipage}[t]{.49\\linewidth}\\vspace{0pt}\\centering\\textbf{'+title+'}\\par\\smallskip\n'
    s += '\\begin{tikzpicture}\\begin{axis}[relation,xlabel={'+xl+'},ylabel={'+yl+'},'+opts+']\n'
    if points is None:
        s += '\\LabelTemplates\n'
    else:
        s += curve+'\n'
        s += '\\addplot[only marks,mark=*,mark size=2pt] coordinates {'+' '.join(f'({x:.9f},{y:.9f})' for x,y in points)+'};\n'
        positions = {
            1:[(.25,.92,'west'),(.30,.72,'west'),(.45,.53,'west'),(.70,.35,'west'),(.98,.21,'east')],
            3:[(.96,.94,'east'),(.02,.73,'west'),(.02,.55,'west'),(.36,.24,'west'),(.35,.08,'west')],
            4:[(.34,.12,'east'),(.44,.40,'east'),(.52,.62,'east'),(.68,.82,'east'),(.98,.56,'east')],
            5:[(.10,.50,'west'),(.12,.64,'west'),(.22,.78,'west'),(.66,.48,'west'),(.98,.96,'east')],
        }
        for i,(x,y) in enumerate(points):
            lx,ly,anchor = positions[kind][i]
            sx = str(int(x)) if kind==1 else f'{x:.3f}'
            sy = f'{y:g}' if kind==4 else f'{y:.3f}'
            s += f'\\PointLabel{{{ids[i]}}}{{{x:.9f},{y:.9f}}}{{{sx}}}{{{sy}}}{{{lx}}}{{{ly}}}{{{anchor}}}\n'
    return s+'\\end{axis}\\end{tikzpicture}\\end{minipage}\n'

def graphs1(sig, ns, unit, worked):
    add(r'\par\smallskip')
    se = [sig/math.sqrt(n) for n in ns]; mo = [1.96*v for v in se]
    nx = math.ceil(max(ns)*1.06/100)*100
    sy = math.ceil(max(se)*1.15); my = math.ceil(max(mo)*1.15)
    ticks = ','.join(str(round(nx*i/4)) for i in range(5))
    for k,(title,xl,yl,opts,pts,curve,kind) in enumerate([
      ('Standard error vs sample size',r'$n$ (sampled units)',f'SE ({unit})',f'xmin=0,xmax={nx},ymin=0,ymax={sy},xtick={{{ticks}}}',list(zip(ns,se)),rf'\addplot[black,domain={ns[0]}:{ns[-1]},samples=180] {{{sig}/sqrt(x)}};',1),
      ('Margin of error vs sample size',r'$n$ (sampled units)',f'MoE ({unit})',f'xmin=0,xmax={nx},ymin=0,ymax={my},xtick={{{ticks}}}',list(zip(ns,mo)),rf'\addplot[black,domain={ns[0]}:{ns[-1]},samples=180] {{1.960*{sig}/sqrt(x)}};',1),
      ('Margin of error vs standard error',f'SE ({unit})',f'MoE ({unit})',f'xmin=0,xmax={sy},ymin=0,ymax={my}',list(zip(se,mo)),rf'\addplot[black,domain=0:{max(se)}] {{1.960*x}};',3),
    ]):
        add(graph(title,xl,yl,opts,pts if worked else None,curve,kind))
        add('\\hfill' if k==0 else ('\\par\\medskip' if k==1 else ''))

def graphs2(sig,n,unit,worked):
    add(r'\par\smallskip')
    se=sig/math.sqrt(n); mo=[z*se for z in zs]
    mx=math.ceil(max(mo)*1.07)
    def cdfcurve(scale):
        # Exact normal CDF sampled numerically; no external plotting dependencies.
        coords=' '.join(f'({z*scale:.9f},{100*math.erf(z/math.sqrt(2)):.9f})' for z in [1.20+i*(3.40-1.20)/180 for i in range(181)])
        return '\\addplot[black] coordinates {'+coords+'};'
    for k,(title,xl,yl,opts,pts,curve,kind) in enumerate([
      ('Confidence level vs margin of error',f'MoE ({unit})',r'$C$ (\%)',f'xmin=0,xmax={mx},ymin=79,ymax=101,ytick={{80,85,90,95,99.9}}',list(zip(mo,conf)),cdfcurve(se),4),
      ('Critical value vs margin of error',f'MoE ({unit})',r'$z^*$ (unitless)',f'xmin=0,xmax={mx},ymin=0,ymax=3.6,ytick={{0,1,2,3}}',list(zip(mo,zs)),rf'\addplot[black,domain=0:{max(mo)}] {{x/{se}}};',5),
      ('Confidence level vs critical value',r'$z^*$ (unitless)',r'$C$ (\%)','xmin=0,xmax=3.6,ymin=79,ymax=101,xtick={0,1,2,3},ytick={80,85,90,95,99.9}',list(zip(zs,conf)),cdfcurve(1),4),
    ]):
        add(graph(title,xl,yl,opts,pts if worked else None,curve,kind))
        add('\\hfill' if k==0 else ('\\par\\medskip' if k==1 else ''))

def model():
    return r'Assume a simple random sample of independent observations from a much larger population, known population SD, and a normal population or approximately normal sample mean.'
def task1(sig,ns,unit,worked=False):
    add(r'\task{Task 1:}{Illustrate the relationships between standard error, margin of error, and sample size.}')
    add(f'Hold $\\sigma={sig}$ {unit} and $C=95\\%$ ($z^*=1.960$) fixed. '+model())
    add(r'Use $\mathrm{SE}=\sigma/\sqrt n$ and $\mathrm{MoE}=z^*\times\mathrm{SE}$. '+
        'Cases A--E correspond, in order, to $n='+','.join(map(str,ns))+r'$. Each of the three graphs uses these five cases and five coordinate labels. SE and MoE use '+unit+'.')
    if not worked:
        add(r'Complete the three relationship graphs, each with five plotted points, their coordinate labels, and the relationship curve. Keep each ID attached to the same case. Retain unrounded intermediate values; write calculated coordinates to three decimals. The workspace is for calculations within this task.')
    else:
        add(r'\textbf{Solution.} For A, $\mathrm{SE}=30/\sqrt{25}=6.000$ and $\mathrm{MoE}=1.960(6.000)=11.760$ thousand COP. The remaining substitutions supply the other plotted coordinates.')
        add(r'\begin{datagrid}{|l|r|X|X|}ID&$n$&SE (thousand COP)&MoE (thousand COP)\\\hline')
        for i,n in enumerate(ns):
            se=sig/math.sqrt(n)
            add(f'{ids[i]}&{n}&${sig}/\\sqrt{{{n}}}={se:.3f}$&$1.960({se:.3f})={1.96*se:.3f}$\\\\\\hline')
        add(r'\end{datagrid}')
    graphs1(sig,ns,unit,worked)
    if not worked: add(r'\hfill\workarea\par')

def task2(sig,n,unit,worked=False):
    add(r'\task{Task 2:}{Illustrate the relationships between confidence level, critical value, and margin of error.}')
    add(f'Hold $n={n}$ and $\\sigma={sig}$ {unit} fixed, so $\\mathrm{{SE}}=\\sigma/\\sqrt n$ stays fixed. '+model())
    add(r'Use $\mathrm{MoE}=z^*\times\mathrm{SE}$. Cases A--E are the five supplied pairs below; the ID stays the same across all three graphs. MoE uses '+unit+r'; $z^*$ is unitless and $C$ is a percentage.')
    add(r'\begin{datagrid}{|l|X|X|X|X|X|}ID&A&B&C&D&E\\\hline $C$ (\%)&80&90&95&99&99.9\\\hline $z^*$&1.282&1.645&1.960&2.576&3.291\\\hline\end{datagrid}')
    if worked:
        add(r'\textbf{Solution.} $\mathrm{SE}=30/\sqrt{100}=3.000$ thousand COP. Thus the five margins are $1.282(3)=3.846$, $1.645(3)=4.935$, $1.960(3)=5.880$, $2.576(3)=7.728$ and $3.291(3)=9.873$ thousand COP.')
    else:
        add(r'Complete the three relationship graphs with five labeled points and the relationship curves. Use true numerical spacing, including near 100\%. Retain unrounded intermediate values; write calculated coordinates to three decimals. The workspace is for calculations within this task.')
    graphs2(sig,n,unit,worked)
    if not worked: add(r'\hfill\workarea\par')

add(r'\stageheading{Worked example}\problemtitle{1}{Weekly household grocery spending}')
add(r'An analyst estimates the district mean weekly household grocery bill. For the explanatory intervals, the common point estimate is $\bar{x}=84$ thousand COP.')
task1(30,[25,100,400,900,1600],'thousand COP',True)
add(r'''\par\clearpage
\textbf{Problem 1 --- Task 1 solution continued}\par
Both SE and MoE decrease as $n$ increases because they are proportional to $1/\sqrt n$. The continuous sample-size curves guide the eye between integer sizes. MoE vs SE is a line through the origin with slope $1.960$; confidence and population SD stay fixed.

\textbf{Explanatory confidence-interval comparison}\par
These three intervals use $\bar{x}\pm\mathrm{MoE}=84\pm1.960(30/\sqrt n)$, in thousand COP:
\[
\begin{aligned}
n=25:&\quad84\pm11.760=[72.240,95.760],\\
n=400:&\quad84\pm2.940=[81.060,86.940],\\
n=1600:&\quad84\pm1.470=[82.530,85.470].
\end{aligned}
\]
\begin{center}\begin{tikzpicture}\begin{axis}[
width=.9\linewidth,height=9cm,xmin=70,xmax=98,ymin=.3,ymax=3.8,
axis x line=bottom,axis y line=none,xtick={70,72,76,80,84,88,92,96,98},ytick=\empty,
xlabel={Weekly grocery spending (thousand COP)},scaled ticks=false,clip=false]
\draw[dashed,black!55] (axis cs:84,.55)--(axis cs:84,3.5);
\node[above] at (axis cs:84,3.5) {Shared point estimate $\bar{x}=84.000$};
\foreach \lo/\hi/\y/\n in {72.240/95.760/3/25,81.060/86.940/2/400,82.530/85.470/1/1600}{
\draw[thick] (axis cs:\lo,\y)--(axis cs:\hi,\y);
\draw (axis cs:\lo,\y-.07)--(axis cs:\lo,\y+.07)
(axis cs:\hi,\y-.07)--(axis cs:\hi,\y+.07);
\fill (axis cs:84,\y) circle (2pt);
\node[above] at (axis cs:\lo,\y+.07) {\lo};
\node[above] at (axis cs:\hi,\y+.07) {\hi};
\node[anchor=west] at (axis cs:70,\y-.25) {$n=\n$};
}
\end{axis}\end{tikzpicture}\end{center}
The same numerical scale and centre show the decreasing widths directly. Increasing sample size reduces sampling uncertainty and gives greater precision at the same nominal 95\% confidence.
\clearpage
\textbf{Problem 1 --- Weekly household grocery spending continued}
''')
task2(30,100,'thousand COP',True)
add(r'''\par\clearpage
\textbf{Problem 1 --- Task 2 solution continued}\par
At fixed SE, $z^*=\mathrm{MoE}/3$ is a line through the origin. Higher confidence requires a larger cutoff and margin, while SE stays unchanged.
The smooth confidence curves use $100[2\Phi(z^*)-1]$, or $100[2\Phi(\mathrm{MoE}/3)-1]$, where $\Phi$ is the standard normal CDF. The five points use the nominal supplied percentages. Rounding the cutoffs causes a very small difference between these points and the theoretical curves.

\textbf{Explanatory standard normal illustrations}\par
The panels correspond to cases A, C and E of Task 2. Each uses the same horizontal scale $-4\le z\le4$ and density scale $0\le f(z)\le0.46$.
\par\bigskip
\normalpanel{80}{1.282}\hfill\normalpanel{95}{1.960}\hfill\normalpanel{99.9}{3.291}
\par\bigskip
Each shaded central region is bounded by $-z^*$ and $+z^*$. The central labels give nominal confidence; the rounded cutoffs enclose approximately 80.01574\%, 95.00042\% and 99.90017\%, respectively.
As confidence increases, the cutoffs move outward under the same curve. The larger margin gives a wider interval around the same point estimate: nominal long-run coverage rises while precision decreases.
\clearpage
''')
problems=[
 (2,'Delivery charges for local businesses',24,[36,100,225,400,900],100,'thousand COP','A business association estimates the mean charge for a local delivery.'),
 (3,'Weekly market-stall revenue',45,[25,100,225,625,1600],225,'thousand COP','A market office estimates mean weekly revenue per stall.'),
 (4,'Freight handling fees',72,[36,144,324,576,1296],144,'USD','A port analyst estimates the mean handling fee per container.'),
 (5,'Monthly internet costs',35,[49,100,196,400,1225],196,'thousand COP','A district estimates mean monthly internet expenditure per small business.'),
]
for num,title,sig,ns,n,unit,context in problems:
    if num==2: add(r'\stageheading{Guided Example}')
    if num==3: add(r'\stageheading{Independent Practice}')
    add(f'\\problemtitle{{{num}}}{{{title}}}\n{context}')
    task1(sig,ns,unit)
    add(f'\\clearpage\n\\textbf{{Problem {num} --- {title} continued}}')
    task2(sig,n,unit)
    if num!=5: add(r'\clearpage')
add(r'\end{document}')
text='\n'.join(parts)
start=text.index(r'\foreach \lo/\hi/\y/\n')
end=text.index(r'\end{axis}', start)
block=text[start:end]
body=block[block.index('{',block.index('1600'))+1:]
body=body.rsplit('}',1)[0]
expanded=''
for lo,hi,y,n in [('72.240','95.760','3','25'),('81.060','86.940','2','400'),('82.530','85.470','1','1600')]:
    b=body
    for key,val in [(r'\lo',lo),(r'\hi',hi),(r'\y',y),(r'\n',n)]:
        import re
        b=re.sub(re.escape(key)+r'(?![A-Za-z])',lambda m:val,b)
    expanded+=b
text=text[:start]+expanded+text[end:]
out.write_text(text,encoding='utf-8')
print(out)
