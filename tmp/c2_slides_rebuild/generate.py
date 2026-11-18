from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
old=p.read_text(encoding='utf-8')
head=old[:old.index('% SOURCE MAP')]
roles=old[old.index('\\definecolor{PopulationMean}'):old.index('\\tikzset{ge marker')]
meta=old[old.index('\\title{'):old.index('\\begin{document}')]
practice=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex').read_text(encoding='utf-8')
# Reuse the exact local override's table bodies, with the deck's inline renderer.
parts=practice.split('\\begin{tabularx}{\\linewidth}',2)
tables=[]
for part in parts[1:]:
    tables.append('\\begin{tabularx}{\\linewidth}'+part.split('\\end{tabularx}',1)[0]+'\\end{tabularx}')
s=head+'''% SOURCE MAP / user-directed sequence:
% Legend: practice.tex, document-local practicehighlightlegend@G11-T2-C2 override.
% Example: classroom_activity.tex, problem 1, narrative + data + Tasks 1--3.
% No guided/independent exercises. Legacy simulation labels normalized to
% mu_known: the same fixed population mean, later established as 41 minutes.
'''+roles+r'''
\definecolor{Error}{HTML}{28AFA2}
\newif\ifGTenHighlights
\GTenHighlightstrue
% \GTenHighlightsfalse % Uncomment to disable instructional highlights.
% Transparent markers retain identical dimensions before activation and with
% highlights disabled. Visibility and instructional activation are independent.
\tikzset{ge marker/.style={rectangle,rounded corners=1mm,draw=none,
 fill=#1,fill opacity=\GEOpacity,text opacity=1,text=GEInk,
 inner xsep=.6mm,inner ysep=.3mm,outer sep=0pt}}
\makeatletter
\newcommand{\GEHighlightMath}[2]{\tikz[baseline=(gehl.base)]
 \node[ge marker=\GECurrentRole](gehl){$\m@th#1#2$};}
\newcommand{\GEHighlight}[2]{\begingroup
 \def\GEOpacity{0}\ifGTenHighlights\def\GEOpacity{.32}\fi
 \def\GECurrentRole{#1}\ifmmode\mathpalette\GEHighlightMath{#2}
 \else\tikz[baseline=(gehl.base)]\node[ge marker=#1](gehl){#2};\fi\endgroup}
\makeatother
\newcommand{\GEPlain}[1]{{\GTenHighlightsfalse\GEHighlight{white}{#1}}}
\newcommand{\At}[3]{\alt<#1->{\GEHighlight{#2}{#3}}{\GEPlain{#3}}}
\newcommand{\R}[2]{\leavevmode\visible<#1->{#2}}
'''
for name,role in [('Mean','PopulationMean'),('Point','SampleMean'),('SD','PopulationSD'),('Size','SampleSize'),('Confidence','Confidence'),('Significance','Confidence'),('Critical','Critical'),('SE','StandardError'),('MoE','MarginError'),('Endpoint','Endpoint'),('CI','Endpoint'),('Width','Width'),('Coverage','Coverage'),('Error','Error')]:
 s+=rf'\newcommand{{\Ctwo{name}}}[1]{{\GEHighlight{{{role}}}{{#1}}}}'+'\n'
s+=r'''\newcommand{\CtwoCoverCount}{\CtwoCoverage{N_{\rm cover}}}
\newcommand{\CtwoTotalCount}{\CtwoCoverage{N}}
\newcommand{\LegendStyle}{\small\setlength{\parskip}{0pt}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.12}}
'''
for name,table in zip(['LeftLegend','RightLegend'],tables):s+=rf'\newcommand{{\{name}}}{{\begingroup\LegendStyle'+table+'\\par\\endgroup}\n'
s+=r'''\newcommand{\BothLegends}{\begin{columns}[T,onlytextwidth]
\begin{column}{.49\textwidth}\LeftLegend\end{column}
\begin{column}{.49\textwidth}\RightLegend\end{column}\end{columns}}
'''
# Shared Task 1 tables: same complete reference repeated in Task 2.
rows=[(2,'PopulationMean',r'\mu','Population mean','Mean duration of all cycling trips in the month'),(3,'PopulationMean',r'\mu_{\mathrm{known}}','Later established population mean','41 minutes'),(4,'PopulationSD',r'\sigma','Population standard deviation','14 minutes'),(5,'SampleMean',r'\bar{x}','Sample mean','40 minutes'),(6,'SampleSize','n','Sample size','49 trips'),(7,'StandardError',r'\mathrm{SE}','Standard error','2 minutes'),(9,'Confidence','C','Confidence level',r'95\% = 0.95'),(11,'Confidence',r'\alpha','Significance level','0.05'),(13,'Confidence',r'\alpha/2','Tail area','0.025'),(15,'Critical','z^*','Critical value','1.960')]
s+=r'''
\newif\ifReference
\Referencefalse
% In reference mode all entries are visible; each frame supplies input activation.
\newcommand{\IR}[6]{\ifReference
 \At{\csname Input#1\endcsname}{#2}{$#3$}&\At{\csname Input#1\endcsname}{#2}{#4}&\At{\csname Input#1\endcsname}{#2}{#5}\\\midrule
 \else
 \At{#1}{#2}{$#3$}&\At{#1}{#2}{#4}&\R{#1}{\At{#1}{#2}{#5}}\\\midrule
 \fi}
\newcommand{\InfoTables}{\begingroup
\fontsize{10}{11.4}\selectfont\setlength{\parskip}{0pt}\setlength{\tabcolsep}{2pt}\renewcommand{\arraystretch}{1.03}
\begin{columns}[T,onlytextwidth]
'''
for subset in [rows[:6],rows[6:]]:
 s+=r'\begin{column}{.49\textwidth}\begin{tabularx}{\linewidth}{@{}p{.14\linewidth}p{.39\linewidth}X@{}}\toprule'+'\n'+r'\textbf{Symbol}&\textbf{Concept}&\textbf{In context...}\\\midrule'+'\n'
 for j,(step,role,sym,concept,context) in enumerate(subset):
  if j==0 or (step==5):
   group='Population parameters' if step==2 else 'Sample statistics' if step==5 else 'Procedure Settings'
   s+=r'\multicolumn{3}{@{}l}{\textbf{'+group+r'}}\\\midrule'+'\n'
  # break long concepts into short highlighted pieces, avoiding overwide TikZ nodes
  concept=concept.replace('Later established population mean',r'Later established\par population mean').replace('Population standard deviation',r'Population standard\par deviation')
  concept=concept.replace(r'\par',r'}\par\At{'+str(step)+r'}{'+role+r'}{') if False else concept
  # IR uses fragment-wise highlighting for wrapped text via helper
  s+=rf'\IR{{{step}}}{{{role}}}{{{sym}}}{{{concept}}}{{{context}}}{{}}'+'\n'
 s+=r'\end{tabularx}\end{column}'+'\n'
s+=r'\end{columns}\endgroup}'+'\n'
# TikZ nodes cannot paragraph-wrap. Split each text field at spaces into individual markers.
s=s.replace(r'\At{\csname Input#1\endcsname}{#2}{#4}',r'\Words{\csname Input#1\endcsname}{#2}{#4}').replace(r'\At{\csname Input#1\endcsname}{#2}{#5}',r'\Words{\csname Input#1\endcsname}{#2}{#5}').replace(r'\At{#1}{#2}{#4}',r'\Words{#1}{#2}{#4}').replace(r'\At{#1}{#2}{#5}',r'\Words{#1}{#2}{#5}')
s=s.replace(r'Later established\par population mean','Later established population mean').replace(r'Population standard\par deviation','Population standard deviation')
s+=r'''\ExplSyntaxOn
\NewDocumentCommand{\Words}{mmm}{\seq_set_split:Nnn \l_tmpa_seq {~}{#3}\seq_map_inline:Nn \l_tmpa_seq {\At{#1}{#2}{##1}\space}}
\ExplSyntaxOff
'''
for step,*_ in rows:s+=rf'\expandafter\def\csname Input{step}\endcsname{{99}}'+'\n'
s+=meta+r'\begin{document}'+'\n'+r'\section{Highlight guide}\begin{frame}\titlepage\end{frame}'+'\n'
def frame(title,body,opts='t'):
 global s
 s+=rf'\begin{{frame}}[{opts}]{{{title}}}'+'\n'+body+'\n'+r'\end{frame}'+'\n'
frame('Key terms and highlight guide -- left table',r'\begin{minipage}{.76\linewidth}\LeftLegend\end{minipage}')
frame('Key terms and highlight guide -- right table',r'\begin{minipage}{.76\linewidth}\RightLegend\end{minipage}')
frame('Key terms and highlight guide',r'\BothLegends')
p1=r'An initial study estimated the then unknown average duration of all cycling trips in a specified month. A random sample of 49 trips averaged 40 minutes; the known population standard deviation was 14 minutes. The report used 95\% confidence.'
p2=r"Five subsequent independent studies sampled the same month's population, each using 49 trips, the same standard deviation and 95\% procedure. A later comprehensive population investigation established an average of 41 minutes, enabling retrospective interval assessment."
studyrows=[(1,40,'36.08','43.92'),(2,42,'38.08','45.92'),(3,45,'41.08','48.92'),(4,38,'34.08','41.92'),(5,41,'37.08','44.92')]
data=r'\begin{tabular}{@{}rrrr@{}}\toprule Study & $\bar{x}$ (min) & $L$ (min) & $U$ (min)\\\midrule'+'\n'+''.join(f'{i}&{m}&{l}&{u}'+r'\\'+'\n' for i,m,l,u in studyrows)+r'\bottomrule\end{tabular}'
s+=r'\section{Cycling study}'+'\n'
frame('Investigate the cycling interval',r'\small '+p1+'\par\medskip\n'+r'\begin{columns}[T,onlytextwidth]\begin{column}{.60\textwidth}'+p2+r'\end{column}\begin{column}{.37\textwidth}'+data+r'\end{column}\end{columns}')
# Task 1, 16 overlays: result/calculation panel disappears on following overlay.
narr=r'''\small
\begin{minipage}[t][1.65cm][t]{\linewidth}
An initial study estimated the then unknown \At{2}{PopulationMean}{average duration} of \At{2}{PopulationMean}{all cycling trips} in a \At{2}{PopulationMean}{specified month}.
A random sample of \At{6}{SampleSize}{49 trips} averaged \At{5}{SampleMean}{40 minutes}; the known \At{4}{PopulationSD}{population standard deviation} was \At{4}{PopulationSD}{14 minutes}. The report used \At{9}{Confidence}{95\% confidence}.
\end{minipage}
\begin{minipage}[t][.65cm][t]{\linewidth}
\R{3}{A later comprehensive population investigation established an average of \At{3}{PopulationMean}{41 minutes}.}
\end{minipage}
\InfoTables
\begin{overlayarea}{\linewidth}{1.0cm}\small
\only<7>{$\CtwoSE{\mathrm{SE}}=\dfrac{\CtwoSD{14}}{\sqrt{\CtwoSize{49}}}=\CtwoSE{2}$ minutes: spread of means across repeated independent samples of 49 trips.}
\only<9>{$\CtwoConfidence{C}=\CtwoConfidence{95\%}=\CtwoConfidence{0.95}$.}
\only<11>{$\CtwoSignificance{\alpha}=1-\CtwoConfidence{0.95}=\CtwoSignificance{0.05}$.}
\only<13>{$\CtwoSignificance{\alpha}/2=\CtwoSignificance{0.05}/2=\CtwoSignificance{0.025}$.}
\only<15>{$\CtwoCritical{z^*}=\CtwoCritical{1.960}$: standard normal critical value for two-sided \CtwoConfidence{95\%} confidence.}
\end{overlayarea}
\onslide<16>
'''
frame('Task 1 -- Link the narrative to the information',narr)
# Each Task 2 frame repeats the completed two-table reference, reset to plain.
s+=r'\section{Interval solution}'+'\n'
def task2(title,active,body):
 setup=r'\Referencetrue'+'\n'
 for step in [r[0] for r in rows]:setup+=rf'\expandafter\def\csname Input{step}\endcsname{{{active.get(step,99)}}}'+'\n'
 setup+=r'\InfoTables\medskip\small'+'\n'
 frame(title,setup+body)
def est(rowspec):
 return r'\begin{tabularx}{\linewidth}{@{}p{.10\linewidth}p{.18\linewidth}X@{}}\toprule\textbf{Symbol}&\textbf{Concept}&\textbf{Calculation, Result and meaning in context}\\\midrule'+rowspec+r'\bottomrule\end{tabularx}'
task2('Task 2 -- Point estimate and margin of error',{5:2,7:5,15:5},est(r'''\At{2}{SampleMean}{$\bar{x}$}&\Words{2}{SampleMean}{Point estimate}&\R{2}{$\CtwoPoint{\bar{x}}=\CtwoPoint{40}$ minutes.}\par\R{3}{One estimate of the mean cycling-trip duration.}\\\midrule
\At{4}{MarginError}{$\mathrm{MoE}$}&\Words{4}{MarginError}{Margin of error}&\R{4}{$\CtwoMoE{\mathrm{MoE}}=\CtwoCritical{z^*}\times\CtwoSE{\mathrm{SE}}$}\par\R{5}{$=\CtwoCritical{1.960}\times\CtwoSE{2}$}\R{6}{$=\CtwoMoE{3.92}$ minutes.}\par\R{7}{Uncertainty in the mean duration: centre-to-endpoint distance.}\\'''))
task2('Task 2 -- Build the confidence interval',{5:3,7:99,15:99},est(r'''\At{2}{Endpoint}{$\mathrm{CI}$}&\Words{2}{Endpoint}{Confidence interval}&
\R{2}{$\CtwoEndpoint{L}=\CtwoPoint{\bar{x}}-\CtwoMoE{\mathrm{MoE}}$}\R{3}{$=\CtwoPoint{40}-\CtwoMoE{3.92}$}\R{4}{$=\CtwoEndpoint{36.08}$ min.}\par
\R{5}{$\CtwoEndpoint{U}=\CtwoPoint{\bar{x}}+\CtwoMoE{\mathrm{MoE}}$}\R{6}{$=\CtwoPoint{40}+\CtwoMoE{3.92}$}\R{7}{$=\CtwoEndpoint{43.92}$ min.}\par
\R{8}{$\CtwoCI{\mathrm{CI}}=[\CtwoEndpoint{L},\CtwoEndpoint{U}]$}\R{9}{$=[\CtwoEndpoint{36.08},\CtwoEndpoint{43.92}]$ minutes.}\par
\R{10}{Plausible values for the fixed population mean under the model.}\\'''))
task2('Task 2 -- Full width and interval interpretation',{9:5},est(r'''\At{2}{Width}{$W$}&\Words{2}{Width}{Full width}&\R{2}{$\CtwoWidth{W}=\CtwoEndpoint{U}-\CtwoEndpoint{L}=2\CtwoMoE{\mathrm{MoE}}$}\par\R{3}{$=\CtwoEndpoint{43.92}-\CtwoEndpoint{36.08}=2(\CtwoMoE{3.92})$}\R{4}{$=\CtwoWidth{7.84}$ minutes.}\par\R{5}{The span of plausible mean durations describes the estimate's precision.}\\''')+r'''\R{6}{We are \CtwoConfidence{95\% confident} that the population mean cycling-trip duration lies in $[\CtwoEndpoint{36.08},\CtwoEndpoint{43.92}]$ minutes, a range of plausible values under the model.}''')
# Task 3 study-by-study evidence, same fixed table across overlays.
s+=r'\section{Coverage evidence}'+'\n'
p2h=r"\At{8}{Coverage}{Five subsequent independent studies} sampled the \At{2}{PopulationMean}{same month's population}, each using 49 trips, the same standard deviation and \At{9}{Confidence}{95\% procedure}. A later comprehensive population investigation established an average of \At{2}{PopulationMean}{41 minutes}, enabling retrospective interval assessment."
dat=r'\begin{tabular}{@{}rrrrl@{}}\toprule Study&$\bar{x}$ (min)&$L$ (min)&$U$ (min)&Check\\\midrule'+'\n'
for i,m,l,u in studyrows:
 k=i+3
 dat+=rf'\At{{{k}}}{{Coverage}}{{{i}}}&{m}&$\At{{{k}}}{{Endpoint}}{{{l}}}$&$\At{{{k}}}{{Endpoint}}{{{u}}}$&\R{{{k}}}{{\CtwoCoverage{{'+('Miss' if i==3 else 'Cover')+r'}}}\\'+'\n'
dat+=r'\bottomrule\end{tabular}'
frame('Task 3 -- Assess the subsequent intervals',r'\small '+p2h+r'''\par\medskip
\begin{columns}[T,onlytextwidth]\begin{column}{.60\textwidth}'''+dat+r'''\end{column}\begin{column}{.37\textwidth}
\R{2}{Later established population mean: $\CtwoMean{\mu_{\mathrm{known}}}=\CtwoMean{41}$ minutes.}\par
\R{3}{Inclusive coverage condition: $\CtwoEndpoint{L_i}\leq\CtwoMean{41}\leq\CtwoEndpoint{U_i}}$.\par
\R{6}{Study 3 misses because $\CtwoEndpoint{L_3}=\CtwoEndpoint{41.08}>\CtwoMean{41}$.}
\end{column}\end{columns}
\begin{overlayarea}{\linewidth}{1.1cm}
\only<4>{$\CtwoEndpoint{36.08}\leq\CtwoMean{41}\leq\CtwoEndpoint{43.92}$: study 1 covers.}
\only<5>{$\CtwoEndpoint{38.08}\leq\CtwoMean{41}\leq\CtwoEndpoint{45.92}$: study 2 covers.}
\only<7>{$\CtwoEndpoint{34.08}\leq\CtwoMean{41}\leq\CtwoEndpoint{41.92}$: study 4 covers.}
\only<8>{$\CtwoEndpoint{37.08}\leq\CtwoMean{41}\leq\CtwoEndpoint{44.92}$: study 5 covers.}
\R{9}{$\CtwoCoverCount(\CtwoConfidence{95\%})=\CtwoCoverage{4},\qquad\CtwoTotalCount(\CtwoConfidence{95\%})=\CtwoCoverage{5}$.}
\end{overlayarea}''')
frame('Task 3 -- Observed coverage and absolute error',r'''\small
Four of the five subsequent intervals contain the later established fixed mean $\CtwoMean{\mu_{\mathrm{known}}}=\CtwoMean{41}$ minutes.
\[
\CtwoCoverCount(\CtwoConfidence{95\%})=\CtwoCoverage{4},\qquad\CtwoTotalCount(\CtwoConfidence{95\%})=\CtwoCoverage{5}.
\]
\begin{overlayarea}{\linewidth}{1.5cm}
\R{2}{$\CtwoCoverage{\mathrm{Cov}}(\CtwoConfidence{95\%})=\dfrac{\CtwoCoverage{4}}{\CtwoCoverage{5}}\times100\%$}\R{3}{$=\CtwoCoverage{80\%}$.}\par\medskip
\R{4}{$\CtwoError{E_{\rm abs}}(\CtwoConfidence{95\%})=|\CtwoCoverage{80}-\CtwoConfidence{95}|$}\R{5}{$=\CtwoError{15}$ \CtwoError{percentage points}.}
\end{overlayarea}
\R{6}{The \CtwoCoverage{observed coverage} across five subsequent intervals is \CtwoCoverage{80\%}, \CtwoError{15 percentage points} below nominal \CtwoConfidence{95\%}. This finite-run discrepancy is consistent with the stated model.}
''')
frame('Task 3 -- What confidence means',r'''\small
\R{1}{\CtwoConfidence{Nominal 95\% confidence} describes the procedure's long-run coverage: under the model, about 95\% of intervals from repeated fresh samples cover the fixed population mean.}\par\medskip
\R{2}{Each realized interval either contains that fixed parameter or misses it. Confidence is not a probability assigned to an already calculated interval.}\par\medskip
\R{3}{It is not the percentage of individual cycling-trip durations inside that interval.}\par\medskip
\R{4}{\CtwoCoverage{Finite-run observed coverage} need not equal nominal confidence or approach it monotonically as studies are added.}
''')
s+=r'\section{Highlight guide}'+'\n'
frame('Key terms and highlight guide',r'\BothLegends')
s+=r'\end{document}'+'\n'
s=s.replace(r'\par\medskip\n',r'\par\medskip'+'\n')
p.write_text(s,encoding='utf-8')
Path('tmp/c2_slides_rebuild/lesson.tex').write_text(s,encoding='utf-8')
print('Written',len(s),'characters')
