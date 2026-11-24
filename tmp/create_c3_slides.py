from pathlib import Path
import re, json, hashlib

ROOT=Path.cwd()
WORK=ROOT/'tmp/c3-slides-20261124'
WORK.mkdir(parents=True,exist_ok=True)
DEST=ROOT/'book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C3_slides.tex'
DEST.parent.mkdir(parents=True,exist_ok=True)
practice=ROOT/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex'
classroom=ROOT/'book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex'
(WORK/'source-hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (practice,classroom)},indent=2))
starter=(ROOT/'.agents/skills/global-economics-slides/assets/beamer_starter.tex').read_text()
preamble=starter.split('% Resolve the practice')[0]
preamble=preamble.replace('% Define source-derived role colors here. No fixed lesson palette.',r'''
% Resolved coordinated palette: highlights_palette.tex, base and registry palettes.
\definecolor{GTenHLValue}{HTML}{FFBB55}
\definecolor{GTenHLSecond}{HTML}{8FD49A}
\definecolor{GTenHLOutcome}{HTML}{BC9DE0}
\definecolor{GTenHLProbability}{HTML}{86BFF0}
\definecolor{CriticalColor}{HTML}{2648BB}
\colorlet{G10T2C3FunctionColor}{GTenHLSecond!85!black}
\colorlet{MathHLSuccessColor}{GTenHLProbability!65!CriticalColor}
\definecolor{MathHLComplementColor}{HTML}{D74383}
\definecolor{MathHLCumulativeColor}{HTML}{43A5C9}
\definecolor{ExpectedValueColor}{HTML}{D6A52A}
''')
preamble+=r'''
% All aliases share the single slide-only padding parameter and disabled branch.
\newcommand{\GTenHLValue}[1]{\GEHighlight{GTenHLValue}{#1}}
\newcommand{\GTenHLSecond}[1]{\GEHighlight{GTenHLSecond}{#1}}
\newcommand{\HLMathEvent}[1]{\GEHighlight{GTenHLOutcome}{#1}}
\newcommand{\HLProbability}[1]{\GEHighlight{GTenHLProbability}{#1}}
\newcommand{\HLSuccessProbability}[1]{\GEHighlight{MathHLSuccessColor}{#1}}
\newcommand{\HLComplementProbability}[1]{\GEHighlight{MathHLComplementColor}{#1}}
\newcommand{\HLCumulativeProbability}[1]{\GEHighlight{MathHLCumulativeColor}{#1}}
\newcommand{\HLExpectedValue}[1]{\GEHighlight{ExpectedValueColor}{#1}}
\newcommand{\HLGtenCThreeFunction}[1]{\GEHighlight{G10T2C3FunctionColor}{#1}}
\newcommand{\HLMathContext}[1]{#1}
\let\I\GTenHLValue
\let\M\GTenHLSecond
\let\A\HLMathEvent
\let\S\HLSuccessProbability
\let\Q\HLComplementProbability
\let\V\HLExpectedValue
\let\T\HLGtenCThreeFunction
\let\Prob\HLProbability
\let\CDF\HLCumulativeProbability
\newcommand{\EV}[1]{\V{\mathbb E}[\M{Y_{#1}}]}
\newcommand{\Ask}[1]{\textbf{#1}\par\medskip}
\newcommand{\LegendTable}[1]{\begingroup\small
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{.34\linewidth}>{\raggedright\arraybackslash}p{.25\linewidth}>{\raggedright\arraybackslash}X@{}}
\toprule\textbf{Symbol or notation}&\textbf{Concept}&\textbf{Brief meaning}\\\midrule
#1\bottomrule\end{tabularx}\par\endgroup}
\ifGTenHighlights
\colorlet{ExpectedInk}{ExpectedValueColor!55!black}
\colorlet{ProbabilityInk}{MathHLSuccessColor!50!black}
\else\colorlet{ExpectedInk}{black}\colorlet{ProbabilityInk}{black}\fi
'''

# Balanced-brace parser retains the live default fields, context notation overrides,
# and concept inheritance rather than assuming the criterion fields are all rendered.
reg=ROOT/'book2026-2027/preamble/highlights'
def group(s,pos):
    assert s[pos]=='{'
    start=pos+1; depth=1; pos+=1
    while depth:
        if s[pos]=='{':depth+=1
        elif s[pos]=='}':depth-=1
        pos+=1
    return s[start:pos-1],pos
records={}
for fn in ('highlights_g11_t1.tex','highlights_g10_t2.tex'):
    s=(reg/fn).read_text()
    for match in re.finditer(r'\\HighlightDeclare(Concept|Context)\{([^}]+)\}\{',s):
        body,_=group(s,match.end()-1)
        fields={}
        for m in re.finditer(r'(\w+)\s*=\s*\{',body):
            fields[m[1]]=group(body,m.end()-1)[0]
        records[match[2]]=fields
def eff(key,field):
    r=records[key]
    return r.get(field) or eff(r['concept'],field)
keys=['event','variable','support','p','q','second','function','mass','cum','expected','break','transform']
overrides={'event','variable','second','mass','cum','expected','transform'}
rows=[]
for k in keys:
    key='g10-t2-default-'+k
    ctx='g10-t2-c3-coordinated-10-'+k
    if k=='function':key=ctx
    notation=records[ctx if k in overrides or k=='function' else key]['notation']
    rows.append(notation+' & '+eff(key,'name')+' & '+eff(key,'brief')+r'\\[5pt]')
for i in range(3):
    preamble+='\\newcommand{\\Legend'+['One','Two','Three'][i]+'}{\\LegendTable{%\n'+'\n'.join(rows[i*4:i*4+4])+'\n}}\n'

criterion='Models binary economic outcomes with Bernoulli random variables, interpreting success and failure in contexts such as default, gain, loss, or claim occurrence.'
preamble+=r'''
\title{Bernoulli Models and\\Individual Break-Even Analysis}
\subtitle{Grade 10 \textbar{} Term 2 \textbar{} Lesson 1 \textbar{} C3}
\author{}\date{}
\newcommand{\GEOfficialCriterion}{\textbf{C3:} '''+criterion+r'''}
\setbeamertemplate{title page}{\raggedright\vfill
{\color{GETeal}\usebeamerfont{subtitle}\insertsubtitle\par}\medskip
{\color{GEInk}\usebeamerfont{title}\inserttitle\par}\bigskip
{\normalsize\GEOfficialCriterion\par}\vfill}
% SOURCE MAP (line numbers refer to sources read 2026-11-24):
% Practice: book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex
% Classroom: book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex
% Selected ONLY worked example 1, Campus concert food stand or indoor games,
% classroom lines 220--435; Task 1 231--346, Task 2 349--432.
% Prerequisites: classroom 157--193, general tasks 198--213;
% practice Binary models and distributions 187--207 and notation reference.
% Metadata/criterion: classroom 153--158; source toggle enabled in practice.
% Registry: highlights_g10_t2.tex reference G10-T2-C3-coordinated, 2777--2781.
% Renderer: highlights_compat_ttwo.tex 525--550, defaults + notation overrides;
% inherited fields resolved above from highlights_g10_t2 and highlights_g11_t1.
% Palette aliases: highlights_palette.tex 55--74, 145--168; roles in highlights_roles.tex.
% SOURCE DISCREPANCY: 12 registered rows, but CoordinatedLegendRow suppresses
% role=context (highlights_tables.tex 169--180), so the live legend prints 11.
% User explicitly requests all 12. Include final Transformation inputs unchanged,
% uncolored, using the renderer's criterion notation override f_i(0),f_i(1).
% The other 11 rows reproduce the live renderer, including default inherited names.
% Opening and closing invoke the exact same three row macros. No context filtering.
% Transformation function name/brief are short baseline-aligned marker fragments
% split only at spaces for readable wrapping; text and color are unchanged.
\begin{document}
\section{Bernoulli models}
\begin{frame}\titlepage\end{frame}
'''
frames=[]
def frame(title,body,src='classroom worked example 1, Task 1 (231--346)'):
    n=2+len(frames)
    frames.append(f'% Frame {n}: {src}\n\\begin{{frame}}[t]{{{title}}}\n'+body+'\n\\end{frame}\n')
for i,name in enumerate(['One','Two','Three']):
    frame(f'Highlight legend ({i+1}/3)',r'\Legend'+name,'live coordinated legend; resolved rows '+str(i*4+1)+'--'+str(i*4+4))
frame('Worked example 1: the weekend choice',r'''
A student club compares two hypothetical fundraising choices for one weekend:
a \M{food stand} at a campus outdoor concert or an \M{indoor games afternoon}.

The concert either goes ahead or is cancelled. Initially it goes ahead on
\S{three out of every eight weekends}.
\medskip
Only one option would be chosen. Both depend on the \A{same concert outcome}.
All monetary amounts are net gains or losses in USD after food, room,
equipment and publicity costs, as applicable.
''','classroom 221--229: full context and assumptions')
frame('The two alternatives: state payoffs',r'''
\Ask{What does each alternative earn in each concert state?}
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}Xrr@{}}
\toprule Concert state & Food stand & Indoor games\\\midrule
Goes ahead & \M{USD 105} & \M{USD $-30$}\\[5pt]
Cancelled & \M{USD $-45$} & \M{USD 90}\\\bottomrule
\end{tabularx}
\medskip
\visible<2->{The concert draws potential players away from games. If it is cancelled,
students seek an indoor alternative.}
\visible<3->{Each alternative has one strictly positive and one strictly negative payoff.}
''','classroom 221--229: given data, not calculated answers')
frame('The questions we will answer',r'''
\textbf{Task 1 --- Establish the binary model and monetary transformations.}
\begin{enumerate}
\item Define one observation, the two states, the indicator and both monetary rules.
\item Give supports, complete PMFs and numerically ordered piecewise CDFs.
\item Identify each loss event, its probability and its contextual meaning.
\end{enumerate}
\medskip
\textbf{Task 2 --- Individual expected values.}
Calculate initial expectations; then keep payoffs fixed and vary $p\in[0,1]$.
Find each expectation formula, its own break-even threshold and sign intervals.
Draw separate labelled graphs and check endpoints and roots.
''','classroom general tasks 198--213 and worked Tasks 1 and 2')
frame('One observation, two exhaustive states',r'''
\Ask{What is one observation, and which event will be labelled success?}
\visible<2->{One observation is the club's net outcome over \textbf{one weekend}
for the chosen option.}
\medskip
\visible<3->{$\A{E}$: the concert goes ahead.\qquad
$\A{E^c}$: the concert is cancelled.}
\medskip
\visible<4->{These states are mutually exclusive (not both) and exhaustive
(one must occur). The event label \textbf{success} means $\A{E}$ occurs;
it need not mean a monetary profit.}
''')
frame('Encode the event with a Bernoulli indicator',r'''
\Ask{How do we encode the two states numerically?}
\visible<2->{\[\I{X}=\begin{cases}\I{1}&\text{on }\A{E},\\\I{0}&\text{on }\A{E^c}.\end{cases}\]
The indicator $\I{X}$ is unitless.}
\visible<3->{\[\S{p}=P(\A{E})=P(\I{X}=\I{1})=\S{\frac38},\qquad
\Q{1-p}=P(\A{E^c})=\Q{1-\frac38}=\Q{\frac58}.\]}
\visible<4->{\[\I{X}\sim\operatorname{Bernoulli}(\S{p}),\qquad
\S{p}+\Q{1-p}=1.\]
For games, success ($X=1$) gives a monetary loss of \M{USD $-30$}.}
''')
frame('From a state to money: the general rule',r'''
\Ask{How can one formula reproduce both state payoffs?}
\visible<2->{$\T{f_i}:\{0,1\}\to\mathbb R$ maps an indicator state to money.
$\M{Y_i}=\T{f_i}(\I{X})$ is net profit in USD; $i$ identifies the alternative.}
\visible<3->{\[\M{Y_i}=\M{f_i(0)}+[\M{f_i(1)}-\M{f_i(0)}]\I{X}.\]}
\visible<4->{At $\I{X}=\I{0}$ the added term vanishes: the result is $\M{f_i(0)}$.
At $\I{X}=\I{1}$ the change is added: the result is $\M{f_i(1)}$.}
\medskip
\visible<5->{Both monetary variables use this same $\I{X}$; only one alternative is chosen.}
''','classroom prerequisites 157--193 and worked transformation formulas 238--262')
for i,label,y0,y1,delta in [(1,'food stand',-45,105,150),(2,'indoor games',90,-30,-120)]:
    op='+' if delta>0 else '-'
    frame(f'Derive the {label} transformation',rf'''
\Ask{{What is $Y_{i}$ as a constant plus a coefficient times $X$?}}
$\M{{f_{i}(0)}}=\M{{{y0}}}$; $\M{{f_{i}(1)}}=\M{{{y1}}}$ USD.
\[\begin{{aligned}}
\visible<2->{{\M{{Y_{i}}}}}&\visible<2->{{=\M{{f_{i}(0)}}+[\M{{f_{i}(1)}}-\M{{f_{i}(0)}}]\I{{X}}}}\\[5pt]
&\visible<3->{{=\M{{{y0}}}+[\M{{{y1}}}-(\M{{{y0}}})]\I{{X}}}}\\[5pt]
&\visible<4->{{=\M{{{y0}}}{op}\M{{{abs(delta)}}}\I{{X}}\quad\text{{USD}}.}}
\end{{aligned}}\]
\visible<5->{{The coefficient is the change from the state-0 payoff to the state-1 payoff: $\M{{{delta}}}$ USD.}}
''')
    frame(f'Check the {label} rule at both states',rf'''
\Ask{{Does $Y_{i}={y0}{op}{abs(delta)}X$ reproduce the given payoffs?}}
\visible<2->{{\[\I{{X}}=\I{{0}}:\quad \M{{Y_{i}}}=\M{{{y0}}}{op}\M{{{abs(delta)}}}(\I{{0}})=\M{{{y0}}}\ \text{{USD}}.\]}}
\visible<3->{{\[\I{{X}}=\I{{1}}:\quad \M{{Y_{i}}}=\M{{{y0}}}{op}\M{{{abs(delta)}}}(\I{{1}})=\M{{{y1}}}\ \text{{USD}}.\]}}
\medskip
\visible<4->{{Cancellation gives \M{{USD ${y0}$}}; going ahead gives \M{{USD ${y1}$}}.
The rule matches both states and has the required units.}}
''')
frame('Support, PMF and CDF: three different questions',r'''
\Ask{Which values occur, how much mass has each, and how much accumulates?}
\visible<2->{\textbf{Support:} values with positive probability:
$\I{S_X}=\{x\in\mathbb R:P(X=x)>0\}$;
$\M{S_{Y_i}}=\{y\in\mathbb R:P(Y_i=y)>0\}$.}
\medskip
\visible<3->{\textbf{PMF:} $\Prob{m_Z(z)}=P(Z=z)$ is the mass at one value.
It is zero at all other values. These discrete models have PMFs, not ordinary densities.}
\medskip
\visible<4->{\textbf{CDF:} $\CDF{F_Z(t)}=P(Z\leq t)$ adds all masses at or below $t$.
Order values numerically and include the mass at the cutoff.
The left limit $F_Z(t^-)=P(Z<t)$ excludes that cutoff.}
''','classroom 163--193; practice binary-model prerequisite 187--207; legend CDF definition')
frame('The distribution of the indicator',r'''
\Ask{What are the complete PMF and ordered CDF of $X$?}
\visible<2->{For $0<p<1$, $\I{S_X}=\{\I{0},\I{1}\}$.}
\visible<3->{\[
\Prob{m_X(x)}=\begin{cases}\Q{1-p}&x=\I{0},\\\S{p}&x=\I{1},\\0&\text{otherwise},\end{cases}
\qquad
\CDF{F_X(t)}=\begin{cases}0&t<\I{0},\\\Q{1-p}&\I{0}\leq t<\I{1},\\1&t\geq\I{1}.\end{cases}
\]}
\visible<4->{Initially: $\Prob{m_X(0)}=\Q{5/8}$ and $\Prob{m_X(1)}=\S{3/8}$.
At $t=0$ the CDF includes $5/8$; at $t=1$ it includes both masses.}
''')
frame('Food stand: support and complete PMF',r'''
\Ask{Which payoffs can $Y_1$ take, and which state supplies each mass?}
\visible<2->{For $0<p<1$, $\M{S_{Y_1}}=\{\M{-45},\M{105}\}$ USD.}
\visible<3->{\[\Prob{m_{Y_1}(y)}=\begin{cases}
\Q{1-p}&y=\M{-45}\quad(X=0),\\
\S{p}&y=\M{105}\quad(X=1),\\
0&\text{otherwise}.
\end{cases}\]}
\visible<4->{Initially: $\Prob{m_{Y_1}(-45)}=\Q{5/8}$ and
$\Prob{m_{Y_1}(105)}=\S{3/8}$. The two masses sum to 1.}
''')
frame('Food stand: build its ordered CDF',r'''
\Ask{As the USD cutoff $t$ increases, when does each mass enter?}
\visible<2->{The values are ordered $\M{-45}<\M{105}$.
Below $-45$ there is no mass; at $-45$ include $1-p$; at $105$ include the rest.}
\visible<3->{\[\CDF{F_{Y_1}(t)}=\begin{cases}
0&t<\M{-45},\\
\Q{1-p}&\M{-45}\leq t<\M{105},\\
1&t\geq\M{105}.
\end{cases}\]}
\visible<4->{Initially the middle level is $\Q{5/8}$.
In particular $F_{Y_1}(-45)=5/8$ and $F_{Y_1}(105)=1$.
The inequalities include each jump at its payoff.}
''')
frame('Indoor games: support and complete PMF',r'''
\Ask{Which payoff is lower, and which indicator state produces it?}
\visible<2->{For $0<p<1$, $\M{S_{Y_2}}=\{\M{-30},\M{90}\}$ USD.
The lower payoff comes from $\I{X}=\I{1}$, because the concert draws players away.}
\visible<3->{\[\Prob{m_{Y_2}(y)}=\begin{cases}
\S{p}&y=\M{-30}\quad(X=1),\\
\Q{1-p}&y=\M{90}\quad(X=0),\\
0&\text{otherwise}.
\end{cases}\]}
\visible<4->{Initially: $\Prob{m_{Y_2}(-30)}=\S{3/8}$ and
$\Prob{m_{Y_2}(90)}=\Q{5/8}$.}
''')
frame('Indoor games: order money, not state labels',r'''
\Ask{Why is the middle CDF level $p$, rather than $1-p$?}
\visible<2->{The numerical order is $\M{-30}<\M{90}$.
The first jump is the mass of $Y_2=-30$, which comes from $X=1$.}
\visible<3->{\[\CDF{F_{Y_2}(t)}=\begin{cases}
0&t<\M{-30},\\
\S{p}&\M{-30}\leq t<\M{90},\\
1&t\geq\M{90}.
\end{cases}\]}
\visible<4->{Initially the middle level is $\S{3/8}$.
Thus $F_{Y_2}(-30)=3/8$ and $F_{Y_2}(90)=1$.
A CDF accumulates payoffs in numerical order, even when the transformation decreases.}
''')
frame('At probability endpoints, support changes',r'''
\Ask{Does a value with zero probability belong to the support?}
\visible<2->{No. Support contains only positive-mass values.
The same PMF and CDF formulas remain valid at $p=0$ and $p=1$.}
\medskip
\begin{tabularx}{\linewidth}{@{}lXXX@{}}
\toprule & $\I{S_X}$ & $\M{S_{Y_1}}$ (USD) & $\M{S_{Y_2}}$ (USD)\\\midrule
$0<p<1$ & \GERevealCell{3}{$\{\I{0},\I{1}\}$} & \GERevealCell{3}{$\{\M{-45},\M{105}\}$} & \GERevealCell{3}{$\{\M{-30},\M{90}\}$}\\[5pt]
$p=0$ & \GERevealCell{4}{$\{\I{0}\}$} & \GERevealCell{4}{$\{\M{-45}\}$} & \GERevealCell{4}{$\{\M{90}\}$}\\[5pt]
$p=1$ & \GERevealCell{5}{$\{\I{1}\}$} & \GERevealCell{5}{$\{\M{105}\}$} & \GERevealCell{5}{$\{\M{-30}\}$}\\\bottomrule
\end{tabularx}
''','classroom indicator endpoints 280--285; practice positive-mass support qualifications and notation reference')
frame('Food stand: identify the loss event',r'''
\Ask{When does the chosen food stand produce a loss?}
\visible<2->{A loss means $\M{Y_1}<0$. Of the two payoffs, only $\M{-45}$ is negative.}
\visible<3->{\[\{\M{Y_1}<0\}=\{\I{X}=\I{0}\}=\A{E^c},\qquad
\Prob{P(Y_1<0)}=\Q{1-p}=\Q{\frac58}\quad\text{initially}.\]}
\visible<4->{Cancellation produces a food stand loss of \M{USD 45}.
In the model, five out of eight weekends produce a food stand loss.
This is a probability interpretation, not a guarantee about any particular eight weekends.}
\medskip
\visible<5->{The loss event is a condition on an observation; the support is a set of payoff values.}
''')
frame('Indoor games: identify the loss event',r'''
\Ask{When does the chosen games afternoon produce a loss?}
\visible<2->{Only the payoff $\M{-30}$ is negative; it occurs when the concert goes ahead.}
\visible<3->{\[\{\M{Y_2}<0\}=\{\I{X}=\I{1}\}=\A{E},\qquad
\Prob{P(Y_2<0)}=\S{p}=\S{\frac38}\quad\text{initially}.\]}
\visible<4->{Three out of eight weekends produce a games afternoon loss in this model.
The loss is \M{USD 30}, because the concert draws potential players away.}
\medskip
\visible<5->{Here the Bernoulli ``success'' event is precisely the monetary loss event.
The label success describes $E$, not whether the club earns money.}
''')
frames.append('\n\\section{Individual expectations}\n')
frame('Task 2: probability-weighted net profit',r'''
\Ask{What is the expected net profit per weekend for each alternative?}
\visible<2->{Expectation weights each payoff by its probability:
\[\EV{i}=\S{p}\M{f_i(1)}+\Q{1-p}\M{f_i(0)}.\]}
\visible<3->{It is a \V{probability-weighted average} in USD, interpreted per weekend.
The expectation operator $\V{\mathbb E}$ differs from the event $\A{E}$.}
\medskip
\visible<4->{First use $\S{p}=\S{3/8}$ and $\Q{1-p}=\Q{5/8}$.
Then hold both state payoffs fixed and vary $p\in[0,1]$, analysing each alternative separately.}
''','classroom Task 2, 349--432; expected-value prerequisite')
frame('Food stand: initial expected value',r'''
\Ask{At $p=3/8$, what is the food stand's expected net profit?}
\[\begin{aligned}
\visible<2->{\EV{1}}&\visible<2->{=\M{105}(\S{\tfrac38})+\M{(-45)}(\Q{\tfrac58})}\\[6pt]
&\visible<3->{=\frac{315-225}{8}=\frac{90}{8}}\\[6pt]
&\visible<4->{=\V{\frac{45}{4}}=\V{11.25}\ \text{USD}.}
\end{aligned}\]
\visible<5->{The food stand has an \V{expected gain of USD 11.25 per weekend}.
Its possible individual payoffs remain \M{USD $-45$} and \M{USD 105}.}
''','classroom 350--365, initial food stand expectation')
frame('Indoor games: initial expected value',r'''
\Ask{At $p=3/8$, what is the games afternoon's expected net profit?}
\[\begin{aligned}
\visible<2->{\EV{2}}&\visible<2->{=\M{-30}(\S{\tfrac38})+\M{90}(\Q{\tfrac58})}\\[6pt]
&\visible<3->{=\frac{-90+450}{8}=\frac{360}{8}}\\[6pt]
&\visible<4->{=\V{45}\ \text{USD}.}
\end{aligned}\]
\visible<5->{The games afternoon has an \V{expected gain of USD 45 per weekend}.
Its possible individual payoffs remain \M{USD $-30$} and \M{USD 90}.}
''','classroom 366--373, initial games expectation')
for i,lab,y0,y1,delta in [(1,'food stand',-45,105,150),(2,'indoor games',90,-30,-120)]:
    op='+' if delta>0 else '-'
    expanded=r'\M{105}\S{p}-\M{45}+\M{45}\S{p}' if i==1 else r'\M{-30}\S{p}+\M{90}-\M{90}\S{p}'
    frame(f'{lab.capitalize()}: let the probability vary',rf'''
\Ask{{With state payoffs fixed, how does $\mathbb E[Y_{i}]$ depend on $p$?}}
\[\begin{{aligned}}
\visible<2->{{\EV{{{i}}}}}&\visible<2->{{=\S{{p}}\M{{f_{i}(1)}}+\Q{{1-p}}\M{{f_{i}(0)}}}}\\[5pt]
&\visible<3->{{=\M{{{y1}}}\S{{p}}+\M{{({y0})}}(\Q{{1-p}})}}\\[5pt]
&\visible<4->{{={expanded}}}\\[5pt]
&\visible<5->{{=\M{{{y0}}}{op}\M{{{abs(delta)}}}\S{{p}}\quad\text{{USD}},\quad 0\leq p\leq1.}}
\end{{aligned}}\]
\visible<6->{{Changing $p$ changes the weights, while the two monetary payoffs stay fixed.}}
''','classroom 374--400: expectation formulas')
    root=r'\frac3{10}' if i==1 else r'\frac34'
    mid=r'150p=45' if i==1 else r'-120p=-90'
    ratio=r'\frac{45}{150}' if i==1 else r'\frac{-90}{-120}'
    frame(f'{lab.capitalize()}: its own break-even threshold',rf'''
\Ask{{For which probability is this alternative's expected net profit zero?}}
\[\begin{{aligned}}
\visible<2->{{\EV{{{i}}}=\V{{0}}}}&\visible<2->{{\iff\M{{{y0}}}{op}\M{{{abs(delta)}}}\S{{p}}=\V{{0}}}}\\[6pt]
&\visible<3->{{\iff {mid}}}\\[6pt]
&\visible<4->{{\iff\S{{p}}=\S{{{ratio}}}=\S{{{root}}}.}}
\end{{aligned}}\]
\visible<5->{{Thus $\S{{p_{i}^*}}=\S{{{root}}}$ is the \S{{individual break-even probability}}.
It makes this alternative's expectation zero.}}
''','classroom 380--400: individual zero equations')
frame('Food stand: positive and negative expectations',r'''
\Ask{On which probability intervals is the expected net profit positive or negative?}
\visible<2->{\[\begin{aligned}
\EV{1}>0&\iff -45+150p>0\\
&\iff150p>45\iff p>\S{\tfrac3{10}}.
\end{aligned}\]}
\visible<3->{Expected net gain: $\S{p}\in\S{(\tfrac3{10},1]}$.
Dividing by positive $150$ keeps the inequality direction.}
\visible<4->{\[\EV{1}<0\iff150p<45\iff p<\S{\tfrac3{10}}.\]
Expected net loss: $\S{p}\in\S{[0,\tfrac3{10})}$.
At $p=3/10$, the expectation is \V{zero}.}
''','classroom 401--410: food stand sign intervals')
frame('Indoor games: why the inequality reverses',r'''
\Ask{Solve $90-120p>0$. What happens when we divide by $-120$?}
\visible<2->{\[\EV{2}>0\iff-120p>-90\iff p<\S{\tfrac34}.\]
Dividing by \M{$-120$} reverses $>$ to $<$: multiplication or division by
a negative number reverses numerical order (for example, $2>1$ but $-2<-1$).}
\visible<3->{Expected net gain: $\S{p}\in\S{[0,\tfrac34)}$.}
\visible<4->{\[\EV{2}<0\iff-120p<-90\iff p>\S{\tfrac34}.\]
Expected net loss: $\S{p}\in\S{(\tfrac34,1]}$.
At $p=3/4$, the expectation is \V{zero}.}
''','classroom 411--418: games intervals and negative division')

# Fixed-bounds graphs reproduce the two separate classroom EVGraph datasets.
# Inherit practice's expectation ink, probability ink and dotted root projection.
for i,lab,y0,y1,root,rootnum in [(1,'Food stand',-45,105,r'\frac3{10}',.3),(2,'Indoor games',90,-30,r'\frac34',.75)]:
    lo=min(y0,y1)-.2*abs(y1-y0); hi=max(y0,y1)+.2*abs(y1-y0)
    def coord(p,y):return f'({1.5+8*p:.3f},{1+(y-lo)/(hi-lo)*3.7:.3f})'
    zero=1+(0-lo)/(hi-lo)*3.7
    graph=rf'''
\Ask{{How do the state payoffs and the zero threshold determine this graph?}}
\centering
\begin{{tikzpicture}}[x=1cm,y=1cm]
\path[use as bounding box] (0,0) rectangle (12,5.35);
\draw[black!15,step=.5] (1.5,1) grid (9.5,4.7);
\draw[->] (1.5,1)--(9.9,1);
\draw[->] (1.5,1)--(1.5,4.9);
\node[anchor=west,font=\small,text=ExpectedInk] at (1.5,5.12) {{Expected net profit (USD): $\EV{{{i}}}$}};
\node[font=\small,text=ProbabilityInk] at (5.6,.25) {{Probability $\S{{p}}=P(\A{{E}})$}};
\node[below,font=\small] at (1.5,1) {{$0$}};
\node[below,font=\small] at (9.5,1) {{$1$}};
\visible<2->{{
\fill[ExpectedInk] {coord(0,y0)} circle (2pt);
\fill[ExpectedInk] {coord(1,y1)} circle (2pt);
\node[left,font=\small] at {coord(0,y0)} {{$\V{{{y0}}}$}};
\node[right,font=\small] at {coord(1,y1)} {{$\V{{{y1}}}$}};
}}
\visible<3->{{\draw[ExpectedInk,very thick] {coord(0,y0)}--{coord(1,y1)};}}
\visible<4->{{
\draw[black,dashed] (1.5,{zero:.3f})--(9.5,{zero:.3f});
\node[left,font=\small] at (1.5,{zero:.3f}) {{$\V{{0}}$}};
\node[right,font=\small] at (9.5,{zero:.3f}) {{Zero}};
}}
\visible<5->{{
\draw[ProbabilityInk,thick,dotted] {coord(rootnum,0)}--({1.5+8*rootnum:.3f},1);
\fill[black] {coord(rootnum,0)} circle (2.4pt);
\node[below,font=\small] at ({1.5+8*rootnum:.3f},1) {{$\S{{p_{i}^*}}=\S{{{root}}}$}};
\node[anchor=west,font=\small] at (10,3.2) {{Break-even}};
\node[anchor=west,font=\small] at (10,2.65) {{$\bigl(\S{{{root}}},\V{{0}}\bigr)$}};
}}
\end{{tikzpicture}}
'''
    frame(f'{lab}: expected-value graph',graph,'classroom 420--426 graphs; practice BreakEvenGraph semantic strokes; fixed bounds across overlays')
    op='+' if i==1 else '-'; delta=150 if i==1 else 120
    pos=r'(\frac3{10},1]' if i==1 else r'[0,\frac34)'
    neg=r'[0,\frac3{10})' if i==1 else r'(\frac34,1]'
    frame(f'{lab}: connect graph, algebra and meaning',rf'''
\Ask{{Do the graph's endpoints and root agree with the formula?}}
\visible<2->{{\[\begin{{aligned}}
\EV{{{i}}}(0)&={y0}{op}{delta}(0)=\V{{{y0}}},\\[4pt]
\EV{{{i}}}(1)&={y0}{op}{delta}(1)=\V{{{y1}}}\quad\text{{USD}}.
\end{{aligned}}\]}}
\visible<3->{{Root check: $\displaystyle {y0}{op}{delta}({root})=\V{{0}}$.
The endpoint expectations equal the given state payoffs.}}
\medskip
\visible<4->{{Above the zero line, $p\in\S{{{pos}}}$: \V{{expected net gain}}.
Below it, $p\in\S{{{neg}}}$: \V{{expected net loss}}.}}
''','classroom 427--432 endpoint/root checks and sign interpretations')
frame('Expectation describes an average, not a guarantee',r'''
\Ask{Does positive expectation guarantee profit on one weekend? Does break-even mean every payoff is zero?}
\visible<2->{No. At $p=3/8$, both expectations are positive, but the food stand still loses
\M{USD 45} with probability \Q{$5/8$}; games still lose \M{USD 30} with probability \S{$3/8$}.}
\medskip
\visible<3->{At its own break-even probability, each alternative has \V{zero long-run average}
net profit, although every realized payoff is nonzero:
\M{$-45$ or $105$} for food; \M{$-30$ or $90$} for games (USD).}
\medskip
\visible<4->{Both alternatives depend on the same concert outcome. Only one is chosen;
each threshold describes that alternative's individual expectation.}
''','classroom 427--432 and context 229; loss probabilities 325--345')
frames.append('\n\\section{Synthesis}\n')
frame('From one event to an individual threshold',r'''
\A{Binary event} $E$: concert goes ahead
$\longrightarrow$ \I{indicator} $X\in\{0,1\}$.
\medskip
\T{State-to-money rule} $f_i$ gives $\M{Y_i}=f_i(X)$ in USD.
\medskip
\Prob{Distribution and loss probability}: order the monetary payoffs;
attach the correct state masses and identify $\{Y_i<0\}$.
\medskip
\V{Expectation}: weight payoffs by their probabilities.
Hold payoffs fixed to obtain a line in $\S{p}$.
\medskip
\S{Individual break-even threshold}: solve $\mathbb E[Y_i]=0$;
interpret its positive and negative intervals as average net gains and losses.
''','synthesis of selected worked example 1, Tasks 1--2 only')
frames.append('\n\\section{Highlight recap}\n')
for i,name in enumerate(['One','Two','Three']):
    frame(f'Highlight recap ({i+1}/3)',r'\Legend'+name,'retrieval/consolidation: identical opening legend rows '+str(i*4+1)+'--'+str(i*4+4))

text=preamble+''.join(frames)+'\\end{document}\n'
# Whole-phrase live function markers need wrap-safe baseline fragments in legends.
for phrase in ['Transformation function','Maps indicator states to monetary outcomes.']:
    text=text.replace('\\HLGtenCThreeFunction{'+phrase+'}', ' '.join('\\HLGtenCThreeFunction{'+w+'}' for w in phrase.split()))
DEST.write_text(text,encoding='utf-8')
print(DEST)
print('logical frames:',text.count('\\begin{frame}'))
print('legend rows:')
print('\n'.join(rows))

