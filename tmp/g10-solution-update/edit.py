from pathlib import Path
import re
root=Path.cwd()
p=root/'book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex'
s=(root/'tmp/g10-solution-update/original.tex').read_text()
pre=r'''\input{highlights/highlights.tex}
% \GTenHighlightsfalse % Uncomment to disable instructional highlights.
\input{highlights/specific_highlights.tex}
\CoordinatedTermTwoPalette
\tikzset{gten marker/.append style={inner xsep=.6mm,inner ysep=.3mm}}
\usepackage{varwidth}
\usepackage{needspace}
% Natural cell widths, bounded locally so long descriptions can wrap.
\newcommand{\CreditDescription}[1]{\begin{varwidth}[t]{.72\linewidth}\raggedright#1\end{varwidth}}
% Match the reference practice graph treatments; the toggle also controls ink.
\colorlet{keyMassColor}{blue!75!black}
\colorlet{keyCDFColor}{cyan!65!blue!80!black}
\colorlet{keyMassFill}{GTenHLProbability!32!white}
\ifGTenHighlights\else
  \colorlet{keyMassColor}{black}
  \colorlet{keyCDFColor}{black}
  \colorlet{keyMassFill}{black!15}
\fi
'''
s=s.replace('\\input{preamble_exams.tex}\n','\\input{preamble_exams.tex}\n'+pre)
legend=r'''
\section*{Highlight legend}
\phantomsection\label{tab:highlight-legend}
\begin{center}
\begin{tabular}{@{}lll@{}}\toprule
\textbf{Symbol or notation} & \textbf{Concept} & \textbf{Brief meaning}\\\midrule
$\GTenHLOutcome{\omega}$ & \GTenHLOutcome{Outcome} & One complete result or category.\\
$\GTenHLValue{X},\GTenHLValue{x},\GTenHLValue{S_X}$ & \GTenHLValue{Variable and support} & Values and cutoffs in \GTenHLValue{USD}.\\
$\GTenHLSecond{N},\GTenHLSecond{Y}$ & \GTenHLSecond{Other quantities} & Count kept; adjusted payout in USD.\\
$\GTenHLProbability{P},\GTenHLProbability{p_X(x)}$ & \GTenHLProbability{Probability / PMF} & Unitless likelihood or point mass.\\
$\HLCumulativeProbability{F_X(x)}$ & \HLCumulativeProbability{Cumulative probability / CDF} & Mass at or below a cutoff.\\
$\GTenHLParameter{a}$ & \GTenHLParameter{Unknown parameter} & Baseline mass to determine in Question 5.\\
\bottomrule\end{tabular}
\end{center}
'''
s=s.replace('\\clearpage\n\\sectionScored{Online',legend+'\n\\clearpage\n\\sectionScored{Online',1)
# Keep each heading with the complete indivisible credit table. Natural widths
# come from varwidth cells rather than a stretching X column.
pat=r'\\noindent\\begin\{minipage\}\{\\linewidth\}\n\\textbf\{Proposed partial credit\.\}.*?\\end\{minipage\}'
def credit(m):
 t=m.group().replace('\\begin{minipage}{\\linewidth}','\\begin{minipage}{\\linewidth}\\centering',1)
 t=t.replace(r'\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X r@{}}',r'\begin{tabular}{@{}l r@{}}').replace(r'\end{tabularx}',r'\end{tabular}')
 lines=t.splitlines()
 for i,line in enumerate(lines):
  if ' & ' in line:
   a,b=line.split(' & ',1); lines[i]=r'\CreditDescription{'+a+'} & '+b
 return '\n'.join(lines)
s,n=re.subn(pat,credit,s,flags=re.S); assert n==18,n
# Preserve all original instructions, including every verification clause.
s,n=re.subn(r'(\\label\{sol:q\dt\d\}\n\n)([^\n]+)',lambda m:m[1]+r'\noindent\textbf{'+m[2]+'}\\par\\nopagebreak',s); assert n==18,n
# Question descriptions already occur in the correct position. Continuation
# pages explicitly link to their common givens without duplicating the text.
s=re.sub(r'(\\textbf\{Question (\d) --- continued\})',lambda m:m[1]+r'\quad\hyperref[sec:q'+m[2]+r']{Original description}',s)
# Apply native semantic macros only inside the mathematical body, never to
# coordinates, scores, navigation identifiers or table allocations.
head,body=s.split('\\sectionScored{Online',1); body='\\sectionScored{Online'+body
roles={'v':'GTenHLValue','p':'GTenHLProbability','c':'HLCumulativeProbability','o':'GTenHLOutcome','a':'GTenHLParameter','s':'GTenHLSecond'}
def hl(role,x): return '\\'+roles[role]+'{'+x+'}'
# Tokens include complete functions/fractions and numerical atoms. Unchanged
# punctuation/operators and alignment tokens remain outside the markers.
tok=re.compile(r'(F_X\([^)]*\)|p_X\([^)]*\)|\\mathrm\{[KC]+\}|S_X|\\(?:tfrac|frac)(?:\{[\d]+\}|\d)(?:\{[\d]+\}|\d)|(?<![\d.])(?:\d+(?:\.\d+)?(?:/\d+)?(?:\\%)?)|(?<![A-Za-z\\])[XxNYa](?![A-Za-z]))')
def mathmark(x,default='v',q=0):
 if any(c in x for c in ['\\score','\\sml']):return x
 x=re.sub(r'\\binom([0-9A-Za-z])([0-9A-Za-z])',r'\\binom{\1}{\2}',x)
 x=re.sub(r'\\binom([0-9A-Za-z])(?=\{)',r'\\binom{\1}',x)
 probability=('P(' in x or 'p_X(' in x)
 cumulative='F_X(' in x
 support='S_X' in x
 if probability:default='p'
 if cumulative:default='c'
 if support:default='v'
 # For a probability event, color its random variable and cutoff as values.
 event_spans=[m.span() for m in re.finditer(r'P\([^)]*\)',x)]
 def sub(m):
  z=m[0]; r=default
  if z.startswith('F_X'): r='c'
  elif z.startswith('p_X'):r='p'
  elif z.startswith('\\mathrm'):r='o'
  elif z in ['X','x','S_X']:r='v'
  elif z in ['N','Y']:r='s'
  elif z=='a' and q==5:r='a'
  elif z=='a':return z
  elif any(a<=m.start()<b for a,b in event_spans):r='v'
  return hl(r,z)
 return tok.sub(sub,x)
lines=body.splitlines(); q=0; table=None; colroles=[]; display=False; in_credit=False
for i,line in enumerate(lines):
 qm=re.search(r'\\sectionScored.*\{sec:q(\d)\}',line)
 if qm:q=int(qm[1])
 if '\\textbf{Proposed partial credit.' in line:in_credit=True
 if in_credit:
  if '\\end{minipage}' in line:in_credit=False
  continue
 if '\\begin{tabular}' in line:table=True;colroles=[]
 if '\\end{tabular}' in line:table=None
 if any(v in line for v in ['\\sectionScored','\\subsection*','Question total:','Scoring reconciliation.']):continue
 # Identify roles from actual table headers; underlying cells remain intact.
 if table and ' & ' in line:
  cells=line.split(' & ')
  if not colroles:
   if 'Ordered outcome' in line or 'Ordered credit outcome' in line:colroles=['o','p','p']
   elif 'Complete outcomes' in line or 'Ordered outcomes' in line:colroles=['v','o','p']
   elif 'Category' in line:colroles=['o','p','v']
   elif 'Subset count' in line:colroles=['o',None,'p','v','v','s','v']
   elif 'Cutoff interval' in line:colroles=['v','c']
   else:colroles=['v','p']
  out=[]
  for j,c in enumerate(cells):
   r=colroles[min(j,len(colroles)-1)]
   if r:
    c=re.sub(r'\$([^$]+)\$',lambda m:'$'+mathmark(m[1],r,q)+'$',c)
    # Named outcome cells and bare monetary cells in the composition table.
    if colroles==['o','p','v'] and j==0 and not ('Category' in c):c=hl('o',c)
    if len(colroles)==7 and j>=3:c=re.sub(r'^\d+$',lambda m:'$'+hl(r,m[0])+'$',c)
   c=c.replace(' (USD)',' ('+hl('v','USD')+')')
   out.append(c)
  lines[i]=' & '.join(out); continue
 # Never transform graph coordinates. Axis text is transformed separately.
 if any(z in line for z in ['\\draw[','\\addplot[']):continue
 default='v'
 if any(z in line for z in ['probability $','probabilities sum','Normalization:','masses sum','likelihood relationships:']):default='p'
 if 'cumulative numerators' in line:default='c'
 if q==5 and (display or 'Set $a=' in line):default='a'
 if '\\[' in line or '\\begin{align*}' in line:display=True;lines[i]=line;continue
 if '\\]' in line or '\\end{align*}' in line:display=False;lines[i]=line;continue
 if display:
  line=mathmark(line,default,q)
 else:
  line=re.sub(r'\$([^$]+)\$',lambda m:'$'+mathmark(m[1],default,q)+'$',line)
 # Select contextual phrases and quantities; do not color narrative sentences.
 # These are explicit numerical givens / monetary quantities, not rubric points.
 line=re.sub(r'(?<![\w.])\d+(?:\.\d+)? USD',lambda m:hl('v',m[0]),line)
 line=re.sub(r'(?<![\w.])\d+(?:\.\d+)?\\%',lambda m:hl('p',m[0]),line) if '$' not in line else line
 if line.startswith(('A small seller','A retailer','\\textbf{Basic Type','\\textbf{Advanced Type')):
  line=re.sub(r'(?<![\w.])0\.\d+',lambda m:hl('p',m[0]),line)
  for term in ['buyer keeps it','cancels it','walking courier','bicycle','cargo bicycle','motorcycle','refrigerated van','no service','remote diagnosis','software reset','minor repair','major repair','replacement','store credit','cash refund']:
   # Only whole words; no nesting or overlapping names.
   line=re.sub(r'(?<![\w{])'+re.escape(term)+r'(?![\w}])',lambda m:hl('o',m[0]),line)
 for phrase,role in [('random variable','v'),('support','v'),('net contribution','v'),('total loyalty credit','v'),('handling fee','v'),('final payout','v'),('account credit','v'),('PMF','p'),('CDF','c')]:
  # Avoid macro names; match standalone prose only.
  line=re.sub(r'(?<![A-Za-z\\{])'+phrase+r'(?![A-Za-z}])',lambda m:hl(role,m[0]),line)
 lines[i]=line
body='\n'.join(lines)+'\n'
s=head+body
# Numerical sequences that are shared monetary givens are values, even though
# the final entry alone carries the unit in the original prose.
for seq in ['0, 0, 2, 4, 7, 11, 16 and 23','0, 2, 4, 6, 10, 15, 15 and 25','0, 2, 5, 9, 14 or 20']:
 # Mark short fragments separately so the sentence can wrap.
 for prefix in [seq.rsplit(' ',1)[0]]:
  s=s.replace(prefix, re.sub(r'\d+',lambda m:hl('v',m[0]),prefix))
# Probability lists in shared context; marks are not involved.
for seq in ['0.2, 0.5 and 0.3','0.4, 0.4 and 0.2']:
 s=s.replace(seq,re.sub(r'0\.\d+',lambda m:hl('p',m[0]),seq))
s=s.replace('fill=black!15','fill=keyMassFill,draw=keyMassColor')
s=s.replace('\\addplot[thick','\\addplot[keyCDFColor,thick').replace('\\addplot[only marks','\\addplot[keyCDFColor,only marks')
s=s.replace('xlabel={$x$ (USD)}','xlabel={$\\GTenHLValue{x}$ (\\GTenHLValue{USD})},\n xticklabel={ $\\GTenHLValue{\\pgfmathprintnumber{\\tick}}$}')
# Add appropriate y-axis tick treatment locally to each graph.
s=s.replace('ylabel={$\\GTenHLProbability{p_X(x)}$}', 'ylabel={$\\GTenHLProbability{p_X(x)}$},yticklabel={$\\GTenHLProbability{\\pgfmathprintnumber{\\tick}}$}')
s=s.replace('ylabel={$\\HLCumulativeProbability{F_X(x)}$}', 'ylabel={$\\HLCumulativeProbability{F_X(x)}$},yticklabel={$\\HLCumulativeProbability{\\pgfmathprintnumber{\\tick}}$}')
s=re.sub(r'([\^_])(\\(?:GTenHL\w+|HLCumulativeProbability)\{[^{}]*\})',r'\1{\2}',s)
s=s.replace(r'\noindent\textbf{',r'\noindent\textbf{\boldmath ')
p.write_text(s)
print('Updated 18 task instructions and 18 credit tables; semantic body markup applied.')
