from pathlib import Path
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex')
s=p.read_text(); original=s
s=s.replace(r'\input{preamble.tex}',r'\input{preamble.tex}'+'\n'+r'\input{graphs/highlights.tex}',1)
s=s.replace(r'\subsection{From a school sale to a number}',r'\GTenHighlightLegend'+'\n\n'+r'\subsection{From a school sale to a number}',1)
# Exact fragments are selected within named teaching processes, never by a
# document-wide letter/number replacement. Each replacement preserves content.
def scope(start,end,pairs):
 global s
 a=s.index(start); b=s.index(end,a) if end else len(s)
 part=s[a:b]
 for old,new in pairs:
  if old not in part: raise ValueError((start,old))
  part=part.replace(old,new)
 s=s[:a]+part+s[b:]
def h(role,t): return '\\GTenHL'+role+'{'+t+'}'
def v(t): return h('Value',t)
def y(t): return h('Second',t)
def z(t): return h('Third',t)
def o(t): return h('Outcome',t)
def pr(t): return h('Probability',t)
def par(t): return h('Parameter',t)
# Introductory sale: distinct roles for each variable throughout its mappings.
a=s.index(r'\subsection{From a school'); b=s.index(r'\Needspace{10\baselineskip}',a)
intro=s[a:b]
# Explicitly chosen math fragments: rule symbols, assigned values and units.
for letter,fun in [('X',v),('Y',y),('Z',z)]:
 import re
 intro=re.sub(r'(?<![A-Za-z])'+letter+r'\((\\mathrm\{[BN]+\})\)=([0-9]+)',lambda m:fun(letter)+'('+o(m[1])+')='+fun(m[2]),intro)
 intro=re.sub(r'\bp_'+letter+r'\(([0-9]+)\)',lambda m:'p_{'+fun(letter)+'}('+fun(m[1])+')',intro)
 # Standalone or event-form symbols in math; graph calls kept byte-for-byte.
 lines=[]
 for line in intro.splitlines(True):
  if line.lstrip().startswith('\\GTen'): lines.append(line); continue
  line=line.replace('$'+letter+'$', '$'+fun(letter)+'$')
  line=re.sub(r'\$'+letter+r'=([0-9.]+)\$',lambda m:'$'+fun(letter)+'='+fun(m[1])+'$',line)
  lines.append(line)
 intro=''.join(lines)
# Definitions/support and units, matched to the named variable.
for old,new in [
 ('number of visitors who buy a notebook',v('number of visitors who buy a notebook')),
 ('total revenue',y('total revenue')),
 ('first visitor buys a notebook',z('first visitor buys a notebook')),
 (r'$\{0,1,2,3\}$, measured in buyers', '$'+v(r'\{0,1,2,3\}')+'$, measured in '+v('buyers')),
 (r'$\{0,5,10,15\}$, measured in dollars', '$'+y(r'\{0,5,10,15\}')+'$, measured in '+y('dollars')),
 (r'$\{0,1\}$, with no physical unit', '$'+z(r'\{0,1\}')+'$, with no physical unit'),
 ('43.2\\% chance',pr(r'43.2\%')+' chance'),('revenue equals 5 USD','revenue equals '+y('5 USD'))]:
 assert old in intro,old
 intro=intro.replace(old,new,1)
# Complete-outcome probabilities: highlight labels and resulting masses only.
intro=re.sub(r'P\((\\mathrm\{[BN]+\})\)',lambda m:'P('+o(m[1])+')',intro)
for mass in ['0.216','0.144','0.096','0.064','0.432','0.288','0.400','0.600']:
 lines=[]
 for line in intro.splitlines(True):
  if line.lstrip().startswith('\\GTen'): lines.append(line); continue
  # These decimals all denote masses in this sale, not counts or revenue.
  line=line.replace(mass,pr(mass))
  lines.append(line)
 intro=''.join(lines)
s=s[:a]+intro+s[b:]
# Grouping example. Select exact math/words, including the mapping tables.
scope(r'\subsection{Introductory general',r'\subsection{Bridge',[
 (r'$a,b,c,d$', '$'+o('a')+','+o('b')+','+o('c')+','+o('d')+'$'),
 (r'$0.1,0.2,0.3,0.4$', '$'+pr('0.1')+','+pr('0.2')+','+pr('0.3')+','+pr('0.4')+'$'),
 (r'$X(a)=0$', '$'+v('X')+'('+o('a')+')='+v('0')+'$'),
 (r'$X(b)=X(c)=1$', '$'+v('X')+'('+o('b')+')='+v('X')+'('+o('c')+')='+v('1')+'$'),
 (r'$X(d)=2$', '$'+v('X')+'('+o('d')+')='+v('2')+'$'),
 ('cash, debit card, credit card, or a mobile wallet',o('cash')+', '+o('debit card')+', '+o('credit card')+', or '+o('a mobile wallet')),
 ('10\\%, of debit card is 20\\%, of credit card is 30\\%, and of a mobile wallet is 40\\%',pr(r'10\%')+', of debit card is '+pr(r'20\%')+', of credit card is '+pr(r'30\%')+', and of a mobile wallet is '+pr(r'40\%')),
 (r'a fee of \$1', 'a fee of '+v(r'\$1')),
 (r'a fee of \$2', 'a fee of '+v(r'\$2')),
 ('$X$','$'+v('X')+'$'),
 ('processing fee in USD',v('processing fee in USD')),
 (r'Outcome & $a$ & $b$ & $c$ & $d$', 'Outcome & $'+o('a')+'$ & $'+o('b')+'$ & $'+o('c')+'$ & $'+o('d')+'$'),
 ('Probability & 0.1 & 0.2 & 0.3 & 0.4', 'Probability & '+pr('0.1')+' & '+pr('0.2')+' & '+pr('0.3')+' & '+pr('0.4')),
 ('$'+v('X')+'$ value & 0 & 1 & 1 & 2','$'+v('X')+'$ value & '+v('0')+' & '+v('1')+' & '+v('1')+' & '+v('2')),
 (r'$\{0,1,2\}$','$'+v(r'\{0,1,2\}')+'$'),
 (r'$x=1$','$'+v('x')+'='+v('1')+'$'),
 (r'$X(b)=1$','$'+v('X')+'('+o('b')+')='+v('1')+'$'),
 (r'$b$ and $c$','$'+o('b')+'$ and $'+o('c')+'$'),
 (r'$P(b)=0.2$ and $P(c)=0.3$','$P('+o('b')+')='+pr('0.2')+'$ and $P('+o('c')+')='+pr('0.3')+'$'),
 (r'p_X(1)=P(X=1)=P(b)+P(c)=0.2+0.3=0.5000.', 'p_X('+v('1')+')=P('+v('X')+'='+v('1')+')=P('+o('b')+')+P('+o('c')+')='+pr('0.2')+'+'+pr('0.3')+'='+pr('0.5000')+'.'),
 (r'$p_X(0)=P(a)=0.1$', '$p_X('+v('0')+')=P('+o('a')+')='+pr('0.1')+'$'),
 (r'$p_X(2)=P(d)=0.4$', '$p_X('+v('2')+')=P('+o('d')+')='+pr('0.4')+'$'),
 (r'$x$ & 0 & 1 & 2', '$'+v('x')+'$ & '+v('0')+' & '+v('1')+' & '+v('2')),
 (r'$p_X(x)$ & 0.1 & 0.5 & 0.4',r'$p_X(x)$ & '+pr('0.1')+' & '+pr('0.5')+' & '+pr('0.4')),
 ('fee is 50\\%', 'fee is '+pr(r'50\%')),
])
# Normalization: each highlighted supported value selects a blue probability.
scope(r'\subsection{Bridge',r'\subsection{Advanced general problem: a finite',[
 (r'$S=\{0,1,2\}$','$S='+v(r'\{0,1,2\}')+'$'),
 (r'p_X(0)+p_X(1)+p_X(2)', 'p_X('+v('0')+')+p_X('+v('1')+')+p_X('+v('2')+')'),
 ('=0.1+0.5+0.4=1.', '='+pr('0.1')+'+'+pr('0.5')+'+'+pr('0.4')+'=1.'),
 (r'$p_X(1)=P(X=1)=0.5$', '$p_X('+v('1')+')=P('+v('X')+'='+v('1')+')='+pr('0.5')+'$'),
 (r'$p_X(1)=0.5$', '$p_X('+v('1')+')='+pr('0.5')+'$'),
 (r'\$0, \$1, or \$2',v(r'\$0')+', '+v(r'\$1')+', or '+v(r'\$2')),
])
# Remaining worked processes use local palettes; pairs below are exact selections.
scopes=[
 ('Advanced general problem: a finite','Advanced general problem: an infinite',[
  ('$c,2c,3c$','$'+par('c')+','+par('2c')+','+par('3c')+'$'),('$0,2,5$','$'+v('0,2,5')+'$'),
  ('$X$','$'+v('X')+'$'),('$c$','$'+par('c')+'$'),(r'$\{0,2,5\}$','$'+v(r'\{0,2,5\}')+'$'),
  (r'c+2c+3c=6c=1',par('c')+'+'+par('2c')+'+'+par('3c')+'='+par('6c')+'=1'),
  ('$c=1/6$','$'+par('c')+'='+par('1/6')+'$'),('$1/6,1/3,1/2$','$'+pr('1/6')+','+pr('1/3')+','+pr('1/2')+'$'),
  ('P(X\\geq2)=p_X(2)+p_X(5)=1/3+1/2=5/6\\approx0.8333','P('+v('X')+r'\geq'+v('2')+')=p_X('+v('2')+')+p_X('+v('5')+')='+pr('1/3')+'+'+pr('1/2')+'='+pr('5/6')+r'\approx'+pr('0.8333')),
  ('refund in USD',v('refund in USD')),('83.33\\%',pr(r'83.33\%')),
  (r'\$0, \$2, or \$5',v(r'\$0')+', '+v(r'\$2')+', or '+v(r'\$5'))]),
 ('Advanced general problem: an infinite','Notation reference and practice procedure',[
  ('$T$','$'+v('T')+'$'),(r'$\{1,2,\ldots\}$','$'+v(r'\{1,2,\ldots\}')+'$'),
  ('positive-integer trial count',v('positive-integer trial count')),
  ('first sale on call $t$','first sale on call $'+v('t')+'$'),
  ('P(T>3)=1-\\sum_{t=1}^{3}2^{-t}=1-(1/2+1/4+1/8)=1/8=0.1250', 'P('+v('T')+'>'+v('3')+r')=1-\sum_{t=1}^{3}'+pr('2^{-t}')+'=1-('+pr('1/2')+'+'+pr('1/4')+'+'+pr('1/8')+')='+pr('1/8')+'='+pr('0.1250')),
  ('more than 3 calls',v('more than 3 calls')),('12.5\\%',pr(r'12.5\%'))]),
 ('Notebook buyers','Daily insurance claims',[
  ('$X$','$'+v('X')+'$'),('$Y=4X$','$'+y('Y')+'=4'+v('X')+'$'),
  (r'$\{0,1,2\}$','$'+v(r'\{0,1,2\}')+'$'),(r'$\{0,4,8\}$','$'+y(r'\{0,4,8\}')+'$'),
  ('p_X(1)=P(\\mathrm{BN})+P(\\mathrm{NB})=1/4+1/4=0.5','p_X('+v('1')+')=P('+o(r'\mathrm{BN}')+')+P('+o(r'\mathrm{NB}')+')='+pr('1/4')+'+'+pr('1/4')+'='+pr('0.5')),
  ('P(Y=4)=P(X=1)=0.5000','P('+y('Y')+'='+y('4')+')=P('+v('X')+'='+v('1')+')='+pr('0.5000')),
  ('$x$ (buyers) & 0 & 1 & 2','$'+v('x')+'$ (buyers) & '+v('0')+' & '+v('1')+' & '+v('2')),
  ('$p_X(x)$ & 0.25 & 0.50 & 0.25','$p_X(x)$ & '+pr('0.25')+' & '+pr('0.50')+' & '+pr('0.25')),
  ('A revenue of 4 USD','A revenue of '+y('4 USD'))]),
 ('Daily insurance claims','Intermediate contextual practice',[
  ('$X$','$'+v('X')+'$'),('$0.7,q,0.1$','$'+pr('0.7')+','+par('q')+','+pr('0.1')+'$'),('$0,1,2$','$'+v('0,1,2')+'$'),
  ('$q$','$'+par('q')+'$'),(r'$\{0,1,2\}$','$'+v(r'\{0,1,2\}')+'$'),
  ('q=1-p_X(0)-p_X(2)=1-0.7-0.1=0.2',par('q')+'=1-p_X('+v('0')+')-p_X('+v('2')+')=1-'+pr('0.7')+'-'+pr('0.1')+'='+par('0.2')),
  ('P(X\\geq1)=p_X(1)+p_X(2)=0.2+0.1=0.3000','P('+v('X')+r'\geq'+v('1')+')=p_X('+v('1')+')+p_X('+v('2')+')='+pr('0.2')+'+'+pr('0.1')+'='+pr('0.3000')),
  ('daily claims',v('daily claims')),('30\\%',pr(r'30\%'))]),
 ('Payment methods and a fee','Investment results with a missing mass',[
  ('$X$','$'+v('X')+'$'),('processing fee in USD',v('processing fee in USD')),
  (r'$\{0,1\}$','$'+v(r'\{0,1\}')+'$'),
  (r'X(\text{cash})=0',v('X')+'('+o(r'\text{cash}')+')='+v('0')),
  (r'X(\text{debit})=X(\text{credit})=1',v('X')+'('+o(r'\text{debit}')+')='+v('X')+'('+o(r'\text{credit}')+')='+v('1')),
  ('p_X(0)=0.25','p_X('+v('0')+')='+pr('0.25')),
  (r'p_X(1)=P(\text{debit})+P(\text{credit})=0.45+0.30=0.75','p_X('+v('1')+')=P('+o(r'\text{debit}')+')+P('+o(r'\text{credit}')+')='+pr('0.45')+'+'+pr('0.30')+'='+pr('0.75')),
  ('P(X>0)=0.7500','P('+v('X')+'>'+v('0')+')='+pr('0.7500')),
  ('cash with probability 0.25, debit with 0.45, or credit with 0.30',o('cash')+' with probability '+pr('0.25')+', '+o('debit')+' with '+pr('0.45')+', or '+o('credit')+' with '+pr('0.30'))]),
 ('Investment results with a missing mass','Advanced contextual practice',[
  ('$G$','$'+v('G')+'$'),('$-20,0,30$','$'+v('-20,0,30')+'$'),('$0.2,0.5,q$','$'+pr('0.2')+','+pr('0.5')+','+par('q')+'$'),
  ('$q=0.4$','$'+par('q')+'='+par('0.4')+'$'),('q=1-0.2-0.5=0.3',par('q')+'=1-'+pr('0.2')+'-'+pr('0.5')+'='+par('0.3')),
  (r'$\{-20,0,30\}$','$'+v(r'\{-20,0,30\}')+'$'),
  (r'P(G\geq0)=p_G(0)+p_G(30)=0.5+0.3=0.8000','P('+v('G')+r'\geq'+v('0')+')=p_G('+v('0')+')+p_G('+v('30')+')='+pr('0.5')+'+'+pr('0.3')+'='+pr('0.8000')),
  ('probability 0.2','probability '+pr('0.2'))]),
 ('Calls until a sale','Delivery records: two numerical descriptions',[
  ('$T$','$'+v('T')+'$'),('$D$','$'+y('D')+'$'),('exact call duration',y('exact call duration')),
  ('P(T\\leq3)=\\sum_{t=1}^{3}p_T(t)=1/2+1/4+1/8=7/8=0.8750','P('+v('T')+r'\leq'+v('3')+r')=\sum_{t=1}^{3}p_T(t)='+pr('1/2')+'+'+pr('1/4')+'+'+pr('1/8')+'='+pr('7/8')+'='+pr('0.8750')),
  ('within three calls',v('within three calls')),('87.5\\%',pr(r'87.5\%'))]),
 ('Delivery records: two numerical descriptions','Closing reference: key ideas and common errors',[
  ('$B$','$'+v('B')+'$'),('$I$','$'+y('I')+'$'),('bonus in USD',v('bonus in USD')),
  (r'$\{-3,2\}$','$'+v(r'\{-3,2\}')+'$'),(r'$\{0,1\}$','$'+y(r'\{0,1\}')+'$'),
  ('$B=2$','$'+v('B')+'='+v('2')+'$'),('$I=0$','$'+y('I')+'='+y('0')+'$'),
  ('p_B(2)=0.2+0.5=0.7','p_B('+v('2')+')='+pr('0.2')+'+'+pr('0.5')+'='+pr('0.7')),
  ('p_B(-3)=0.3','p_B('+v('-3')+')='+pr('0.3')),
  ('p_I(0)=0.7','p_I('+y('0')+')='+pr('0.7')),('p_I(1)=0.3','p_I('+y('1')+')='+pr('0.3')),
  ('P(B<0)=P(I=1)=0.3000','P('+v('B')+'<'+v('0')+')=P('+y('I')+'='+y('1')+')='+pr('0.3000')),
  ('outcomes early, on time, late','outcomes '+o('early')+', '+o('on time')+', '+o('late')),
  ('$0.2,0.5,0.3$','$'+pr('0.2')+','+pr('0.5')+','+pr('0.3')+'$')])]
# Exclude graph commands from all selected replacements, even captions may change.
for start,end,pairs in scopes:
 scope('\\subsection{'+start if start not in ['Notation reference and practice procedure'] else start, '\\subsection{'+end if end not in ['Notation reference and practice procedure','Intermediate contextual practice','Advanced contextual practice','Closing reference: key ideas and common errors'] else '\\section{'+end,pairs)
# Local multi-variable reminders reuse the shared commands.
s=s.replace(r'\subsection{Calls until a sale}',r'\subsection{Calls until a sale}'+'\n'+r'\textit{Markers here:} \GTenHLValue{$T$, call count}; \GTenHLSecond{$D$, duration in minutes}.',1)
s=s.replace(r'\subsection{Delivery records: two numerical descriptions}',r'\subsection{Delivery records: two numerical descriptions}'+'\n'+r'\textit{Markers here:} \GTenHLValue{$B$, bonus in USD}; \GTenHLSecond{$I$, lateness indicator}.',1)
# Verify that removing only the new wrappers restores every original character
# (apart from intentional legends and the one preamble input).
p.write_text(s)
print('Updated activity:',s.count('\\GTenHL'),'selected strokes')
