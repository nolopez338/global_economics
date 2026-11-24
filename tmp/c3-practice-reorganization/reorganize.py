from pathlib import Path
from fractions import Fraction as F
import re
root=Path('book2026-2027/grade10/term_2/1-practice_activities')
p=root/'G10_T2_L1_C3_practice_activity.tex'
s=Path('tmp/c3-practice-reorganization/original.tex').read_text()
def frac(x):
 x=F(x); return str(x.numerator) if x.denominator==1 else rf'\frac{{{x.numerator}}}{{{x.denominator}}}'
def h(n,title): return rf'\needspace{{8\baselineskip}}\paragraph{{{n}. {title}.}}'+'\n'
def pair(blocks):
 out=''
 for j in range(0,len(blocks),2):
  if j+1<len(blocks): out+='\\PracticeColumnPair{\n'+blocks[j]+'}{\n'+blocks[j+1]+'}\n'
  else: out+='\\noindent\\begin{minipage}[t]{.48\\linewidth}\n'+blocks[j]+'\\end{minipage}\\par\n'
 return out
macro=r'''% Corresponding alternatives share a row; all inherited spacing is retained.
\NewDocumentCommand{\PracticeColumnPair}{+m +m}{%
\par\noindent\begin{minipage}[t]{.48\linewidth}#1\end{minipage}\hfill
\begin{minipage}[t]{.48\linewidth}#2\end{minipage}\par}
'''
s=s.replace('\\begin{document}',macro+'\\begin{document}',1)
# Keep physical graph dimensions; add explicit payoff ticks and plotted endpoints.
s=s.replace('xtick={0,1},extra x ticks=', 'ytick={#2,0,#3},\n xtick={0,1},extra x ticks=')
s=s.replace('\\addplot[black,only marks,mark=*] coordinates {(#4,0)};', '\\addplot[black,only marks,mark=*,forget plot] coordinates {(0,#2) (1,#3)};\n\\addplot[black,only marks,mark=*] coordinates {(#4,0)};')
t1=r'''\textbf{Task 1 --- Establish the binary model and monetary transformations.}
\begin{enumerate}
\item \textbf{Binary model and monetary transformations.} Present the shared observation, period, event $E$, complement $E^c$, indicator $X$, Bernoulli model and initial $p=P(E)$. Then give each monetary variable's state payoffs in USD and derive $Y_i=f_i(X)=f_i(0)+[f_i(1)-f_i(0)]X$.
\item \textbf{Supports, PMFs, and ordered CDFs.} Give the indicator's set-builder support, complete PMF and piecewise CDF, including support cases at $p=0,1$. Then give the monetary supports, complete PMFs (zero elsewhere) and numerically ordered piecewise CDFs, with endpoint support cases.
\item \textbf{Initial probabilities and loss events.} State the initial indicator probabilities. For each $Y_i$, give both initial masses, identify $\{Y_i<0\}$ in terms of $X$ and $E$ or $E^c$, calculate its probability and interpret it in context. All alternatives share $X$; no independence is assumed.
\end{enumerate}'''
t2=r'''\textbf{Task 2 --- Individual expected values.}
\begin{enumerate}
\item \textbf{Initial expected values.} Calculate and interpret every monetary expectation at the supplied probability before sensitivity analysis.
\item \textbf{Expectation formulas and sign intervals.} Hold payoffs fixed and vary only $p\in[0,1]$. For each $Y_i$, derive $\mathbb E[Y_i]=p f_i(1)+(1-p)f_i(0)$, solve its exact break-even equation, and solve both strict sign inequalities with correct directions and endpoints. Explain positive, negative and zero expectation.
\item \textbf{Graphs.} Give a separate labelled graph for each variable, showing its expectation line, zero line, endpoint payoffs and exact break-even probability. Finish with endpoint and root checks, and distinguish expected profit from realized profit.
\end{enumerate}'''
s=re.sub(r'\\textbf\{Task 1 --- Establish the binary model and monetary transformations\.\} Identify[^\n]+',lambda m:t1,s)
s=re.sub(r'\\textbf\{Task 2 --- Analyse each expected value separately\.\} For EVERY[^\n]+',lambda m:t2,s)
start=s.index('\\textbf{Task 1',s.index('\\subsection{Reusable practice procedure}'))
end=s.index('\\enlargethispage',start)
proc=t1+'\n'+r'''For $0<p<1$, $S_X=\{0,1\}$; at $p=0$ only 0 remains and at $p=1$ only 1 remains.
Monetary supports contain positive-mass values: $f_i(0)$ only at $p=0$, $f_i(1)$ only at $p=1$.
For ordered amounts $a<b$ and $q=P(Y_i=a)$,
\[
F_{Y_i}(t)=\begin{cases}0,&t<a,\\q,&a\leq t<b,\\1,&t\geq b.\end{cases}
\]
Here $q=1-p$ if $a=f_i(0)$, and $q=p$ if $a=f_i(1)$.
Check total mass 1, right continuity, units and opposite strict payoff signs.
'''+t2+'\n'+r'''Use $p_i^*=-f_i(0)/[f_i(1)-f_i(0)]$. For an increasing expectation,
gain occurs on $(p_i^*,1]$ and loss on $[0,p_i^*)$; for a decreasing expectation,
gain occurs on $[0,p_i^*)$ and loss on $(p_i^*,1]$. Dividing by a negative slope reverses inequalities.
Equality is break-even. Group corresponding steps across alternatives before moving to the next subtask.
Each analysis uses its own payoffs and threshold; all alternatives share $X$.
'''
s=s[:start]+proc+s[end:]
for key in ['inventory','coffee','energy','manufacturing','restaurant','agriculture']:
 original=Path('tmp/c3-practice-reorganization/original.tex').read_text()
 a=original.index(r'\label{sol:c3-'+key+'-model}')
 b=original.index('\\secInicio',a)
 old=original[a:b]
 shared=old[old.index('\n')+1:old.index('\\[S_X')]
 prob=re.search(r'\\SuccessProb\{(\\frac\{\d+\}\{\d+\})\}',shared)[1]
 num,den=map(int,re.findall(r'\d+',prob)); pr=F(num,den); pq=1-pr
 shared=re.sub(r'This unitless indicator is Bernoulli, with.*',lambda m:rf'This unitless indicator has $\Indicator{{X}}\sim\operatorname{{Bernoulli}}(\SuccessProb{{p}})$, initially $\SuccessProb{{p}}=\SuccessProb{{{prob}}}$.',shared,flags=re.S)
 data=[(int(i),int(v0),int(v1)) for i,v0,v1 in re.findall(r'with \$f_(\d)\(0\)=\\Money\{(-?\d+)\}\$ and \$f_\d\(1\)=\\Money\{(-?\d+)\}',old)]
 names=re.findall(r'\\paragraph\{\$A_\d\$: ([^}]+)\.\}',old)
 stage1=[];support=[];pmf=[];cdf=[];loss=[];initial=[];formula=[];signs=[];graphs=[];checks=[]
 for (i,v0,v1),name in zip(data,names):
  d=v1-v0; rootp=F(-v0,d); r=frac(rootp); ev=pr*v1+pq*v0
  lo,hi=sorted([v0,v1]); q=r'\FailureProb{1-p}' if v0==lo else r'\SuccessProb{p}'
  e=rf'\ExpectedValue{{\mathbb E}}[\Money{{Y_{i}}}]'
  line=rf'\Money{{{v0}}}'+('+' if d>0 else '-')+rf'\Money{{{abs(d)}}}\SuccessProb{{p}}'
  title=rf'\textbf{{$Y_{i}$: {name}.}}'+'\n'
  stage1.append(title+rf'''The \Money{{monetary consequence}} is $\Money{{Y_{i}}}=\TransformationFunction{{f_{i}}}(\Indicator{{X}})$ in USD.
\[
\begin{{gathered}}
f_{i}(0)=\Money{{{v0}}},\quad f_{i}(1)=\Money{{{v1}}},\\
\Money{{Y_{i}}}=\Money{{f_{i}(0)}}+[\Money{{f_{i}(1)}}-\Money{{f_{i}(0)}}]\Indicator{{X}}\\
=\Money{{{v0}}}+[\Money{{{v1}}}-(\Money{{{v0}}})]\Indicator{{X}}\\
=\Money{{{v0}}}{'+' if d>0 else '-'}\Money{{{abs(d)}}}\Indicator{{X}}\quad\text{{USD}}.
\end{{gathered}}
\]
One payoff is a loss and the other a gain.
''')
  support.append(title+rf'''\[
\begin{{aligned}}
S_{{Y_{i}}}&=\{{y\in\mathbb R:P(Y_{i}=y)>0\}}\\
&=\{{\Money{{{lo}}},\Money{{{hi}}}\}}\quad(0<p<1).
\end{{aligned}}
\]
At $p=0$, $S_{{Y_{i}}}=\{{\Money{{{v0}}}\}}$; at $p=1$, $S_{{Y_{i}}}=\{{\Money{{{v1}}}\}}$ (USD).
''')
  pmf.append(title+rf'\[m_{{Y_{i}}}(y)=\begin{{cases}}\FailureProb{{1-p}},&y=\Money{{{v0}}},\\\SuccessProb{{p}},&y=\Money{{{v1}}},\\0,&\text{{otherwise}}.\end{{cases}}\]'+'\n')
  cdf.append(title+rf'\[F_{{Y_{i}}}(t)=\begin{{cases}}0,&t<{lo},\\{q},&{lo}\leq t<{hi},\\1,&t\geq {hi}.\end{{cases}}\]'+'\n')
  state=0 if v0<0 else 1; lp=pq if state==0 else pr; event='E^c' if state==0 else 'E'; mass=r'\FailureProb{1-p}' if state==0 else r'\SuccessProb{p}'
  loss.append(title+rf'''\[
\begin{{gathered}}
m_{{Y_{i}}}(\Money{{{v0}}})=\FailureProb{{{frac(pq)}}},\quad m_{{Y_{i}}}(\Money{{{v1}}})=\SuccessProb{{{frac(pr)}}},\\
\{{Y_{i}<0\}}=\{{\Indicator{{X}}=\Indicator{{{state}}}\}}={event},\\
P(Y_{i}<0)={mass}= {frac(lp)}\quad\text{{initially}}.
\end{{gathered}}
\]
The {name} alternative produces a net loss when ${event}$ occurs, in a proportion ${frac(lp)}$ of observations in the stated period under the initial model.
''')
  interpretation='expected net gain' if ev>0 else 'expected net loss' if ev<0 else 'break-even'
  initial.append(title+rf'''\[
\begin{{aligned}}
{e}&=\Money{{{v1}}}\left(\SuccessProb{{{frac(pr)}}}\right)\\
&\quad +(\Money{{{v0}}})\left(\FailureProb{{{frac(pq)}}}\right)\\
&=\ExpectedValue{{{frac(ev)}\ \text{{USD}}}}.
\end{{aligned}}
\]
This is \ExpectedValue{{{interpretation}}}'''+(rf' of $\ExpectedValue{{{frac(abs(ev))}\ \text{{USD}}}}$ per stated period as a long-run average.' if ev else ': zero expected net profit per stated period.')+'\n')
  formula.append(title+rf'''\[
\begin{{aligned}}
{e}&=\SuccessProb{{p}}\Money{{f_{i}(1)}}+(\FailureProb{{1-p}})\Money{{f_{i}(0)}}\\
&=\SuccessProb{{p}}(\Money{{{v1}}})+(\FailureProb{{1-p}})(\Money{{{v0}}})\\
&={line}\quad\text{{USD}}.
\end{{aligned}}
\]
\[
\begin{{aligned}}
{e}=0&\iff {v0}{'+' if d>0 else '-'}{abs(d)}p=0\\
&\iff {d}p={-v0}\\
&\iff p=p_{i}^*={r}.
\end{{aligned}}
\]
''')
  pos=rf'({r},1]' if d>0 else rf'[0,{r})'; neg=rf'[0,{r})' if d>0 else rf'({r},1]'
  signs.append(title+rf'''\[
\begin{{aligned}}
{e}>0&\iff {d}p>{-v0}\\
&\iff p{'>' if d>0 else '<'}{r}\\
&\iff p\in {pos},\\
{e}<0&\iff {d}p<{-v0}\\
&\iff p{'<' if d>0 else '>'}{r}\\
&\iff p\in {neg}.
\end{{aligned}}
\]
'''+('Dividing by the negative slope reverses both inequalities.\n' if d<0 else '')+rf'At $\SuccessProb{{p}}={r}$, {"$"+e+"$"} is \ExpectedValue{{zero}}: break-even.'+'\n')
  graphs.append(rf'''\needspace{{25\baselineskip}}\paragraph{{$Y_{i}$: graph.}}
\begin{{center}}\BreakEvenGraph{{{i}}}{{{v0}}}{{{v1}}}{{{rootp.numerator}/{rootp.denominator}}}\end{{center}}
The line joins $(0,{v0})$ and $(1,{v1})$; its zero is $p_{i}^*={r}$.
''')
  checks.append(rf'$Y_{i}$: $\mathbb E[Y_{i}](0)={v0}$ and $\mathbb E[Y_{i}](1)={v1}$ USD; at $p_{i}^*={r}$, ${v0}+({d})({r})=0$.')
 t1sol=h(1,'Binary model and monetary transformations')+shared+'\n'+pair(stage1)+h(2,'Supports, PMFs, and ordered CDFs')+r'''
\[S_X=\{x\in\mathbb R:P(X=x)>0\}=\{0,1\}\quad(0<p<1).\]
\[m_X(x)=\begin{cases}\FailureProb{1-p},&x=0,\\\SuccessProb{p},&x=1,\\0,&\text{otherwise},\end{cases}\qquad
F_X(t)=\begin{cases}0,&t<0,\\\FailureProb{1-p},&0\leq t<1,\\1,&t\geq1.\end{cases}\]
At $p=0$, $S_X=\{0\}$; at $p=1$, $S_X=\{1\}$. The formulas remain valid at both endpoints.
'''+pair(support)+pair(pmf)+pair(cdf)+r'''Each PMF totals $(1-p)+p=1$. CDF thresholds are numerically ordered,
right-continuous and include each jump at its threshold. At $p=0,1$, zero-mass jumps disappear.
Monetary supports are in USD; indicator values are unitless.
'''+h(3,'Initial probabilities and loss events')+rf'Initially $P(X=0)=\FailureProb{{{frac(pq)}}}$ and $P(X=1)=\SuccessProb{{{frac(pr)}}}$.\n'+pair(loss)+'All monetary variables are functions of the same $X$; no independence is asserted.\n'
 loc=s.index(r'\label{sol:c3-'+key+'-model}')+len(r'\label{sol:c3-'+key+'-model}')
 stop=s.index('\\secInicio',loc)
 s=s[:loc]+'\n'+t1sol+s[stop:]
 loc=s.index(r'\label{sol:c3-'+key+'-decision}')+len(r'\label{sol:c3-'+key+'-decision}')
 stop=s.index('\\secInicio',loc)
 t2sol='Keep the event, its complement and the indicator from Task 1.\n'+h(1,'Initial expected values')+rf'Use the supplied $\SuccessProb{{p}}=\SuccessProb{{{frac(pr)}}}$ for every alternative.\n'+pair(initial)+h(2,'Expectation formulas and sign intervals')+'Hold all state payoffs fixed; vary only $p=P(E)\\in[0,1]$.\n'+pair(formula)+pair(signs)+r'''Positive \ExpectedValue{expectation} means \ExpectedValue{expected net gain}; negative
\ExpectedValue{expectation} means \ExpectedValue{expected net loss}; zero is break-even.
'''+ '\\clearpage\n'+h(3,'Graphs')+'\\clearpage\n'.join(graphs)+'\n\\textbf{Endpoint and root checks.} '+ '\n\n'.join(checks)+r'''

Each observation realizes one state payoff. An \ExpectedValue{expected profit} is a long-run average,
not a guarantee of realized profit. At break-even, zero expectation coexists with nonzero realized payoffs.
'''
 s=s[:loc]+'\n'+t2sol+s[stop:]
# Introductory examples: move existing initial calculations before sensitivity;
# group existing formula/sign work, then existing full-size graphs, without new practice tasks.
for label,nextlabel in [('ex:intro-one','ex:intro-two'),('ex:intro-two',None)]:
 start=s.index('\\label{'+label+'}')
 end=s.index('\\clearpage\n\\subsection',start) if nextlabel else s.index('\\subsection{Binary models',start)
 chunk=s[start:end]
 para=chunk.index('\\needspace{25')
 prefix=chunk[:para]
 pieces=re.split(r'\\needspace\{25\\baselineskip\}\\paragraph\{\$Y_\d\$: its own break-even threshold\.\}',chunk[para:])[1:]
 assert len(pieces)==2
 ini=[];sens=[];gs=[]
 for i,b in enumerate(pieces,1):
  k=b.index('Initially,'); g=b.index('\\begin{center}')
  ini.append(rf'\textbf{{$Y_{i}$: initial expectation.}}'+'\n'+b[k:g])
  sens.append(rf'\textbf{{$Y_{i}$: its own break-even threshold.}}'+'\n'+b[:k])
  gs.append(b[g:])
 # existing sensitivity equations are full width, so keep readable full-width blocks here.
 revised=prefix+'\\paragraph{Initial expected values.}\n'+pair(ini)+'\\paragraph{Expectation formulas and sign intervals.}\n'+''.join(sens)+'\\paragraph{Graphs.}\n'+''.join(gs)
 s=s[:start]+revised+s[end:]
# Put introductory loss statements after the existing distribution explanation.
s=s.replace('For $i=1,2$, $\\{Y_i<0\\}=\\{X=0\\}=E^c$ has probability $1-p$, initially 0.6.\n','')
s=s.replace('and 1 from its positive value onward.','and 1 from its positive value onward.\nFor $i=1,2$, $\\{Y_i<0\\}=\\{X=0\\}=E^c$ has probability $1-p$, initially 0.6.')
p.write_text(s,encoding='utf-8')
print('Updated',p,'lines',len(s.splitlines()))
