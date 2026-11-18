from pathlib import Path
root=Path.cwd(); out=root/'tmp/pdfs/c2-storyboard'; out.mkdir(exist_ok=True,parents=True)
p=root/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex'
s=p.read_text(encoding='utf-8'); (out/'practice-before.tex').write_text(s,encoding='utf-8')
a=s.index('\\subsection*{Highlight legend}'); b=s.index('\\endgroup',a)
part=s[a:b]; part=part.replace('variable $X$',r'variable $\cTwoValue{X}$').replace('value $x$',r'value $\cTwoValue{x}$')
s=s[:a]+part+s[b:]; p.write_text(s,encoding='utf-8')
slide=root/'book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C2_slides.tex'
old=slide.read_text(encoding='utf-8'); (out/'slides-before.tex').write_text(old,encoding='utf-8')
preamble=old[:old.index('\\definecolor{Mass}')]
# Always reserve marker padding; only background opacity changes, so highlights never shift cells.
preamble += r'''
\usetikzlibrary{calc}
\definecolor{Mass}{HTML}{86BFF0}
\definecolor{Cumulative}{HTML}{43A5C9}
\definecolor{Quantity}{HTML}{FFBB55}
\definecolor{Outcome}{HTML}{BC9DE0}
\colorlet{cTwoMassColor}{blue!75!black}
\colorlet{cTwoCDFColor}{cyan!65!blue!80!black}
\colorlet{cTwoGuideColor}{cTwoMassColor!35}
% Base graph palette stays fixed when temporary instructional highlights clear.
\newcommand<>{\H}[2]{\begingroup
  \alt#3{\def\GEOpacity{.32}}{\def\GEOpacity{0}}%
  \ifGTenHighlights\else\def\GEOpacity{0}\fi
  \tikzset{ge marker/.append style={fill opacity=\GEOpacity}}%
  \GEHighlight{#1}{#2}\endgroup}
\newcommand{\cTwoValue}[1]{\GEHighlight{Quantity}{#1}}
\newcommand{\cTwoOutcome}[1]{\GEHighlight{Outcome}{#1}}
\newcommand{\cTwoMassHL}[1]{\GEHighlight{Mass}{#1}}
\newcommand{\cTwoCDFHL}[1]{\GEHighlight{Cumulative}{#1}}
\newcommand{\Blank}[1]{\rule{0pt}{.66cm}#1}
% Fixed-size drawing area. x = 1 cm / USD; y = 3.1 cm / probability unit.
\newcommand{\GraphStart}[1]{\begin{tikzpicture}[x=1cm,y=3.1cm]
\path[use as bounding box] (-1.85,-.28) rectangle (5.65,1.24);
\foreach \y in {0,.25,.5,.75,1}{\draw[gray!15] (-1,\y)--(5.3,\y);
\node[anchor=east,font=\small] at (-1.1,\y) {\pgfmathprintnumber{\y}};}
\draw[->] (-1,0)--(5.5,0); \draw[->] (-1,0)--(-1,1.12);
\foreach \x in {0,2,4}{\draw (\x,0)--(\x,-.025);\node[below,font=\small] at (\x,-.025){\x};}
\node[anchor=south west,font=\small] at (-1,1.13){#1};
\node[font=\small] at (2,-.22){$x$ (USD)};}
\newcommand{\GraphEnd}{\end{tikzpicture}}
\newcommand{\Step}[4]{\draw[cTwoCDFColor,thick,#4] (#1,#3)--(#2,#3);}
\newcommand{\Open}[2]{\draw[cTwoCDFColor,fill=white,thick] (#1,#2) circle[radius=2pt];}
\newcommand{\Closed}[2]{\fill[cTwoCDFColor] (#1,#2) circle[radius=2pt];}
\newcommand{\FullCDF}{\Step{-1}{0}{0}{<-}\Step{0}{2}{.15}{}\Step{2}{4}{.75}{}\Step{4}{5.3}{1}{->}
\Open{0}{0}\Open{2}{.15}\Open{4}{.75}\Closed{0}{.15}\Closed{2}{.75}\Closed{4}{1}}
\title{Constructing PMF and CDF Tables and Graphs}
\subtitle{Grade 10 · Term 2 · Lesson 1 · 2026--2027}
\author{}\date{}
\newcommand{\GEOfficialCriterion}{\textbf{C2:} Interprets PMFs and CDFs by verifying their defining properties and using them to calculate point, interval, cumulative, and complementary probabilities in financial contexts.}
\setbeamertemplate{title page}{\raggedright\vfill{\color{GETeal}\usebeamerfont{subtitle}\insertsubtitle\par}\medskip{\color{GEInk}\usebeamerfont{title}\inserttitle\par}\bigskip{\normalsize\GEOfficialCriterion\par}\vfill}
% SOURCE MAP / explicit user storyboard (supersedes default opening/closing references).
% Reference 1: ../1-practice_activities/G10_T2_L1_C2_practice_activity.tex
% sec:intro / tab:highlight-legend: exact four-row concise table, updated quantity atoms.
% Preamble cTwoCDF, cTwoCombined, cTwoMass/Phantom/Step/Included/Excluded:
% graph palette, pale shadows, endpoint conventions and equal stacked scales.
% graphs/G10_T2_bar_graphs.tex: PMF black borders, pale fill, numerical spacing.
% Reference 2: ../2-class_activities/G10_T2_L1_C2_classroom_activity.tex
% Worked example 1 "Museum kiosk payments", Tasks 1 and 2 and following CDF questions.
% Sole worked example; repeated Payment fees / task wording removed in presentation.
% Frame map: 1 metadata/C2; 2 practice concise legend; 3 outcome statement/table;
% 4 PMF grouping/check; 5 PMF bars; 6 CDF accumulation; 7 CDF steps;
% 8 at-most-3; 9 at-most-5; 10 stacked PMF-to-CDF overlay translations.
% Motion: y coordinates in physical cm, matching 2 cm per probability unit in both panels.
% Copies interpolate BOTH panel separation (2.8 cm) and cumulative baseline shift.
% Native Beamer overlays only: advance PDF pages; no JavaScript/animation viewer needed.
\begin{document}
\section{Museum kiosk payments}
\begin{frame}\titlepage\end{frame}
\begin{frame}[t]{Highlight legend}
\small
'''
legend=part[part.index('\\noindent'):]
legend=legend.replace('p{.43\\linewidth}','p{.35\\linewidth}').replace('p{.13\\linewidth}','p{.12\\linewidth}')
preamble+=legend+r'''
\end{frame}
'''
frames=[]
def frame(title,body,ov=None):
    frames.append('\\begin{frame}'+(' <'+ov+'>' if ov else '')+'[t]{'+title+'}\n'+body+'\n\\end{frame}\n')
def vis(n,s): return rf'\visible<{n}->{{{s}}}'
def h(spec,role,s): return rf'\H<{spec}>{{{role}}}{{{s}}}'
def table(headers,rows,widths):
    cols='@{}'+''.join(r'>{\raggedright\arraybackslash}p{'+str(w)+r'\linewidth}' for w in widths)+'@{}'
    return '\\begin{tabular}{'+cols+'}\\toprule\n'+' & '.join(headers)+r'\\\midrule'+'\n'+'\n'.join(' & '.join(r'\Blank{'+x+'}' if j==0 else x for j,x in enumerate(row))+r'\\' for row in rows)+'\n\\bottomrule\\end{tabular}'
def cols(left,right,l='.44',r='.52'):
    return rf'\begin{{columns}}[T,onlytextwidth]\begin{{column}}{{{l}\textwidth}}'+left+rf'\end{{column}}\begin{{column}}{{{r}\textwidth}}'+right+r'\end{column}\end{columns}'
names=['Cash','Debit card','Credit card','Mobile wallet']; probs=['0.15','0.25','0.35','0.25']; fees=['0','2','2','4']
rows=[]; statement=r'\visible<1-13>{A customer makes one payment at a museum kiosk.\par\medskip'
for i,(name,pr,fee) in enumerate(zip(names,probs,fees)):
    n=2+i*3
    statement+=h(str(n)+'-'+str(n+2),'Outcome',name)+': probability '+h(str(n+1)+'-'+str(n+2),'Mass',pr)+', fee '+h(str(n+2),'Quantity',fee+' USD')+r'.\par'
    rows.append([vis(n,h(str(n)+'-'+str(n+2),'Outcome',name)),vis(n+1,h(str(n+1)+'-'+str(n+2),'Mass',pr)),vis(n+2,h(str(n+2),'Quantity',fee))])
statement+=r'\medskip No other processing charges apply.\par $X$ is the processing fee in USD; support $S_X=\{0,2,4\}$.}'
frame('Museum kiosk payments: complete outcomes',cols(statement,table(['Complete outcome','Probability','$X$ (USD)'],rows,[.43,.27,.20]),'.49','.49'), '1-15')
# Grouping sequence
orows=[]
for i,(name,pr,fee) in enumerate(zip(names,probs,fees)):
    spec=['2-3','4-5','4-5','6-7'][i]
    orows.append([h(spec,'Outcome',name),h(spec,'Mass',pr),h(spec,'Quantity',fee)])
left=r'\visible<1-8>{'+table(['Complete outcome','Probability','$X$ (USD)'],orows,[.43,.27,.20])+'}'
rows=[]
for n,x,pr,calc in [(2,'0','0.15',h('3','Mass','0.15')),(4,'2','0.60',h('5','Mass','0.25')+' + '+h('5','Mass','0.35')+' = '+h('5','Mass','0.60')),(6,'4','0.25',h('7','Mass','0.25'))]:
    rows.append([vis(n,h(f'{n}-{n+1}','Quantity',x)),vis(n+1,h(str(n+1),'Mass',pr)),r'\visible<'+str(n+1)+'-8>{'+calc+'}'])
right=table(['$x$ (USD)','$p_X(x)$',r'\visible<1-8>{Probability calculation}'],rows,[.19,.23,.48])
frame('Group outcomes with the same fee',cols(left,right,'.44','.54')+r'\medskip\visible<5-8>{Debit and credit are mutually exclusive outcomes with the same 2 USD fee, so their probabilities add.}\par\visible<8>{All masses are nonnegative; $0.15+0.60+0.25=1$.}', '1-9')
# Clean two-column PMF helper
def pmftable(specs=['0','0','0'],reveals=[1,1,1]):
    return table(['$x$ (USD)','$p_X(x)$'],[[vis(n,h(sp,'Quantity',x)),vis(n,h(sp,'Mass',p))] for sp,n,x,p in zip(specs,reveals,['0','2','4'],['0.15','0.60','0.25'])],[.38,.48])
body=r'\visible<2-6>{\GraphStart{$p_X(x)$}'
for n,x,p in [(3,0,'.15'),(4,2,'.60'),(5,4,'.25')]:
    body+=rf'\visible<{n}->{{\draw[black,fill=cTwoMassColor!20] ({x-.55},0) rectangle ({x+.55},{p});\node[above] at ({x},{p}) {{'+h(str(n),'Mass',p[0:] if p[0]!='.' else '0'+p)+r'};\node[below] at ('+str(x)+r',-.025){'+h(str(n),'Quantity',str(x))+r'};}'
body+=r'\GraphEnd\par\small '+h('3-5','Mass','PMF bars: individual masses')+'}'
frame('Construct the PMF graph',cols(pmftable(['3','4','5']),body,'.30','.67'), '1-7')
# CDF table cumulative building
intervals=[r'x<0',r'0\leq x<2',r'2\leq x<4',r'x\geq4']; cum=['0','0.15','0.75','1']
rows=[]
for i,(iv,val) in enumerate(zip(intervals,cum)):
    n=2+2*i
    rows.append([vis(n,h(f'{n}-{n+1}','Quantity','$'+iv+'$')),vis(n+1,h(str(n+1),'Cumulative',val))])
ctable=table(['Cutoff interval','$F_X(x)$'],rows,[.56,.32])
calc=r'\begin{overlayarea}{\linewidth}{1.5cm}\only<3>{Below 0: no mass is included.}\only<5>{$F_X(x)='+h('5','Mass','0.15')+'='+h('5','Cumulative','0.15')+r'$.}\only<7>{$F_X(x)='+h('7','Mass','0.15')+'+'+h('7','Mass','0.60')+'='+h('7','Cumulative','0.75')+r'$.}\only<9>{$F_X(x)='+h('9','Cumulative','0.75')+'+'+h('9','Mass','0.25')+'='+h('9','Cumulative','1')+r'$.}\end{overlayarea}'
frame('Accumulate the PMF through each cutoff',cols(r'\visible<1-9>{'+pmftable(['5,7,9','7,9','9'])+'}',ctable+calc,'.38','.58'),'1-10')
def cdftable(specs=['0']*4):
    return table(['Cutoff interval','$F_X(x)$'],[[h(sp,'Quantity','$'+iv+'$'),h(sp,'Cumulative',v)] for sp,iv,v in zip(specs,intervals,cum)],[.58,.28])
body=r'\visible<2->{\GraphStart{$F_X(x)$}'
for n,code in [(3,r'\Step{-1}{0}{0}{<-}\Open{0}{0}'),(4,r'\Step{0}{2}{.15}{}\Open{2}{.15}\Closed{0}{.15}'),(5,r'\Step{2}{4}{.75}{}\Open{4}{.75}\Closed{2}{.75}'),(6,r'\Step{4}{5.3}{1}{->}\Closed{4}{1}')]:
    body+=rf'\visible<{n}->{{{code}}}'
    val=cum[n-3]; xx=[-.5,1,3,4.7][n-3]
    body+=rf'\visible<{n}>{{\node[above] at ({xx},{val}) {{'+h(str(n),'Cumulative',val)+'};}'
body+=r'\GraphEnd}'
frame('Construct the CDF from left to right',cols(r'\visible<1-7>{'+cdftable(['3','4','5','6'])+'}',body,'.32','.67'),'1-8')
for cutoff,value,percent,plateau in [(3,'0.75','75',r'\draw[Cumulative,line width=3pt,opacity=.45] (2,.75)--(4,.75);'),(5,'1','100',r'\draw[Cumulative,line width=3pt,opacity=.45] (4,1)--(5.3,1);')]:
    g=r'\GraphStart{$F_X(x)$}\FullCDF'+rf'\visible<2->{{\node[below] at ({cutoff},0) {{'+h('2-4','Quantity',str(cutoff))+r'};}'
    g+=rf'\visible<3->{{{plateau}}}\visible<4->{{\draw[gray,dashed] ({cutoff},0)--({cutoff},{value})--(-1,{value});\fill[cTwoCDFColor] ({cutoff},{value}) circle[radius=2pt];\node[left,fill=white] at (-1,{value}) {{'+h('4','Cumulative',value)+r'};}\GraphEnd'
    q=rf'What is the probability that the fee is at most {cutoff} USD?\par\medskip'
    q+=r'\visible<5->{\['+rf'P(X\leq {cutoff})=F_X({cutoff})'+'\]'+r'\['+f'={value}={percent}'+r'\%'+r'\]}'
    q+=rf'\visible<6->{{The processing fee is at most {cutoff} USD for {percent}\% of payments.}}'
    if cutoff==3:q+=r'\par\visible<6->{Although $P(X=3)=0$, the CDF includes the supported fees 0 and 2 USD below the cutoff.}'
    frame(f'Read the CDF: at most {cutoff} USD',cols(g,q,'.60','.37'),'1-6')
# Stacked: direct physical coordinates avoid pgfplots panel scale/bbox ambiguities.
stack=r'''\centering
\begin{tikzpicture}[x=1.35cm,y=1cm]
\path[use as bounding box] (-1.9,-.55) rectangle (5.65,5.42);
% Both panels: plot width 8.505 cm; 2 cm per probability unit; baseline separation 2.8 cm.
\foreach \base/\label in {0/{p_X(x)},2.8/{F_X(x)}}{
  \foreach \v in {0,.25,.5,.75,1}{\draw[gray!15] (-1,{\base+2*\v})--(5.3,{\base+2*\v});
  \node[anchor=east,font=\small] at (-1.1,{\base+2*\v}){\pgfmathprintnumber{\v}};}
  \draw[->] (-1,\base)--(5.5,\base);\draw[->] (-1,\base)--(-1,{\base+2.2});
  \foreach \a in {0,2,4}{\draw (\a,\base)--(\a,{\base-.045});\node[below,font=\small] at (\a,{\base-.045}){\a};}
  \node[anchor=east,font=\small] at (-1.15,{\base+1.1}){$\label$};
  \node[font=\small] at (5.1,{\base-.35}){$x$ (USD)};
}
% The original lower stems remain on every overlay.
\foreach \a/\m in {0/.15,2/.60,4/.25}{\draw[cTwoMassColor,thick] (\a,0)--(\a,{2*\m});\fill[cTwoMassColor] (\a,{2*\m}) circle[radius=1.5pt];}
\node[font=\small,anchor=west] at (0,5.15){$F_X(a)-F_X(a^-)=p_X(a)$};
\visible<2->{\draw[cTwoCDFColor,thick,<-] (-1,2.8)--(0,2.8);}
'''
# 9 positions including initial, and full panel distance + baseline, never horizontal travel.
for a,m,b,start,place in [(0,.15,0,3,12),(2,.60,.15,13,22),(4,.25,.75,23,32)]:
    for k in range(9):
        shift=(2.8+2*b)*k/8
        stack+=rf'\only<{start+k}>{{\draw[cTwoGuideColor,densely dashed,line width=.9pt] ({a},{shift:.6f})--({a},{shift+2*m:.6f});}}'+'\n'
    stack+=rf'\visible<{place}->{{\draw[cTwoGuideColor,densely dashed,line width=.9pt] ({a},{2.8+2*b})--({a},{2.8+2*(b+m)});}}'+'\n'
    right={0:2,2:4,4:5.3}[a]; y=2.8+2*(b+m)
    stack+=rf'\visible<{place}->{{\draw[cTwoCDFColor,thick'+(',->' if a==4 else '')+rf'] ({a},{y})--({right},{y});}}'+'\n'
# Endpoint markers painted AFTER every moving and placed guide, including initial open 0.
stack+=r'\visible<2->{\draw[cTwoCDFColor,fill=white,thick] (0,2.8) circle[radius=2pt];}'+'\n'
for a,y,n in [(0,3.1,12),(2,4.3,22),(4,4.8,32)]:
    stack+=rf'\visible<{n}->{{\fill[cTwoCDFColor] ({a},{y}) circle[radius=2pt];}}'+'\n'
for a,y,n in [(2,3.1,12),(4,4.3,22)]:
    stack+=rf'\visible<{n}->{{\draw[cTwoCDFColor,fill=white,thick] ({a},{y}) circle[radius=2pt];}}'+'\n'
stack+=r'''\node[font=\small,anchor=west] at (-.7,-.48){\textcolor{cTwoMassColor}{PMF stems}\quad\textcolor{cTwoGuideColor}{Dashed: translated masses}\quad\textcolor{cTwoCDFColor}{CDF steps}};
\end{tikzpicture}'''
frame('Connecting the PMF and CDF',stack,'1-32')
slide.write_text(preamble+''.join(frames)+'\\end{document}\n',encoding='utf-8')
print('Updated',p,slide)
