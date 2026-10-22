from pathlib import Path
import re
root=Path.cwd()
out=root/'.exam-build-check/c8c9c10-solution'
exam=(root/'book2026-2027/grade10/term_1/3-learning_evidences/G10_T1_L2_C8C9C10_exam.tex').read_text()
s=r'''\makeatletter
\def\input@path{{./}{../}{../../}{../../../}{../../../../}{preamble/}{../preamble/}{../../preamble/}{../../../preamble/}}
\makeatother
\input{preamble_exams.tex}
% Only the shared exam preamble is needed; it already supplies TikZ and tables.
\tikzset{
 cNine survivor/.style={draw,align=center,font=\small,text width=65mm,minimum height=9mm},
 cNine selected/.style={cNine survivor,very thick,fill=black!8},
 cNine eliminated/.style={align=center,font=\small,text width=48mm},
 cNine keep/.style={->,thick},cNine discard/.style={->,dashed}}
\title{Grade 10 -- Term 1\\Decision-Making Under Uncertainty\\Exam Solutions}
\author{}\date{}
\begin{document}
\maketitle
\setcounter{tocdepth}{1}\setcounter{secnumdepth}{2}
\phantomsection\label{toc}\tableofcontents
\section*{Learning objective}
Compare decision criteria and their limitations, and construct and interpret decision trees for staged filtering under uncertainty.
\section*{Criteria assessment}
This exam assesses C8 and C9. Answer individually on separate paper. Questions 1--2 assess C8; each question is worth 3 points: 1 point for task (a) and 2 points for task (b). Questions 3--5 assess C9; each problem is worth 2 points: 1 point for the filtering tree and interpretation and 1 point for the supporting table. Each criterion totals 6 points. A \textbf{minimum of 4 points} is required to pass each criterion. Partial credit is available for correct comparisons, filtering stages, and justified reasoning even if later conclusions contain errors.
\section*{Evaluated criteria}
\begin{enumerate}[label=\textbf{C\arabic*},start=8]
\item Compares the Maximax, Maximin, Minimax Regret, and EMV/Bayes decision criteria by contrasting their information requirements, risk orientations, recommended alternatives, and limitations.
\item Constructs and interprets decision trees for staged filtering rules, applying decision criteria in the specified order to identify the final alternative.
\end{enumerate}
'''
def table(rows):
 return '\\begin{center}\n\\begin{tabular}{lll}\\toprule\nCriterion & Recommended alternative(s) & Deciding statistic and value\\\\ \\midrule\n'+'\n'.join(a+' & $'+b+'$ & '+c+r'\\' for a,b,c in rows)+'\n\\bottomrule\\end{tabular}\n\\end{center}\n'
def anchor(q,part,title):
 return f'\\phantomsection\\label{{sol:q{q}{part}}}\n\\subsection*{{{title}}}\n'
def nav(q):return f'\\secInicio[sec:q{q}]\n'
for q,title in [(1,'Repair Workshop Plans'),(2,'Community Market Stall')]:
 block=exam.split('\\SubsectionBox{'+str(q)+'. ')[1].split('\\SubsectionBox{')[0]
 body=block.split('}\n',1)[1]
 stem,rest=body.split('\\begin{enumerate}',1)
 tasks=re.split(r'\\item\s*',rest.split('\\end{enumerate}')[0])[1:]
 s+=f'\\clearpage\n\\sectionScored{{{title}}}{{C8-\\sml{{3}}}}{{sec:q{q}}}\n'+stem
 s+='\\QuestionsTasks{\n'+',\n'.join('{8}/{sol:q'+str(q)+p+'}/{'+t.strip()+'}' for p,t in zip('ab',tasks))+'\n}\n'
 s+=anchor(q,'a','(a) Original recommendations '+r'\score{1}')
 if q==1:
  s+=table([('Maximax','A_1','Row maximum: 120'),('Maximin','A_3','Row minimum: 35'),('Minimax Regret','A_2','Maximum regret: 35'),('EMV/Bayes','A_4','EMV: 63')])
  s+=r'''All deciding values are in thousand USD. Maximax pursues the greatest upside; Maximin protects the worst outcome; Minimax Regret limits missed profit; EMV uses the forecast probabilities to maximize expected profit. Regret benchmarks use all four original alternatives, with state bests $(120,75,35)$; no eligibility restriction applies in (a).
'''+nav(q)+anchor(q,'b','(b) Subsidy and eligibility '+r'\score{2}')+r'''
The changed low-demand payoffs are $-20+s$ and $10+s$. Over the entire allowed integer range:
\begin{center}\begin{tabular}{lll}\toprule
Alternative & Nonnegative-profit condition & Eligible integer subsidies\\\midrule
$A_1$ & $-20+s\ge0$ & $20\le s\le30$\\
$A_2$ & $10+s\ge0$ & $0\le s\le30$\\
$A_3$ & Minimum $35\ge0$ & $0\le s\le30$\\
$A_4$ & Minimum $20\ge0$ & $0\le s\le30$\\\bottomrule
\end{tabular}\end{center}
Thus the eligible set is $\{A_2,A_3,A_4\}$ for $0\le s\le19$ and all four alternatives for $20\le s\le30$.
The row minima over this range are
\[
m_1(s)=-20+s,\quad m_2(s)=10+s,\quad m_3=35,\quad m_4=20.
\]
These formulas hold because the changed low payoff remains the smallest in each affected row. To select $A_2$ alone requires $10+s>35$, hence $s>25$. At $s=25$, $A_2$ and $A_3$ tie at 35; for $s\le24$, $A_3$ wins. Since $m_1\le10$ and $m_4=20$, neither can obstruct the strict win. Therefore the smallest integer subsidy is $\boxed{s=26}$, or \$26,000.

At $s=26$, all four alternatives are eligible. The updated payoffs and statistics (thousand USD) are:
\begin{center}\begin{tabular}{lrrrrrrr}\toprule
 & High & Normal & Low & Max & Min & Max regret & EMV\\\midrule
$A_1$ &120&25&6&120&6&50&40.2\\
$A_2$ &85&65&36&85&36&35&63.2\\
$A_3$ &50&45&35&50&35&70&44\\
$A_4$ &70&75&20&75&20&50&63\\\bottomrule
\end{tabular}\end{center}
Regret benchmarks are computed over the eligible set $\{A_1,A_2,A_3,A_4\}$ using the changed payoffs: $b=(120,75,36)$. Subtract each payoff from its state benchmark:
\[
r_1=(0,50,30),\quad r_2=(35,10,0),\quad
r_3=(70,30,1),\quad r_4=(50,0,16).
\]
Their largest entries give the maximum regrets above. The affected EMVs are
\[
EMV(A_1)=0.2(120)+0.6(25)+0.2(6)=40.2,
\]
\[
EMV(A_2)=0.2(85)+0.6(65)+0.2(36)=63.2.
\]
The other EMVs remain 44 and 63. Consequently:
'''+table([('Maximax','A_1','Row maximum: 120'),('Maximin','A_2','Row minimum: 36'),('Minimax Regret','A_2','Maximum regret: 35'),('EMV/Bayes','A_2','EMV: 63.2')])+nav(q)
 else:
  s+=table([('Maximax','C_1','Row maximum: 80'),('Maximin','C_2','Row minimum: 32'),('Minimax Regret','C_1','Maximum regret: 22'),('EMV/Bayes','C_2','EMV: 38.4')])
  s+='All values are in hundred USD. Regret benchmarks use both original stalls, with state bests $(80,32)$. Only EMV uses the probabilities; the other criteria compare upside, downside, or missed profit.\n'+nav(q)+anchor(q,'b','(b) Guaranteed profit threshold '+r'\score{2}')+r'''
For every allowed integer $48\le g\le80$, both stalls are eligible. Using the full eligible set $\{C_1,C_2\}$, the state bests remain $(80,32)$. Thus
\[
r(C_1)=(0,22),\quad R(C_1)=22,\qquad
r(C_2)=(80-g,0),\quad R(C_2)=80-g.
\]
For $C_2$ alone to minimize maximum regret,
\[
80-g<22\quad\Longleftrightarrow\quad g>58.
\]
At $g=58$, both maximum regrets equal 22, so both stalls must be retained. For $48\le g\le57$, $C_1$ wins; for $59\le g\le80$, $C_2$ wins alone. The smallest integer guarantee is therefore $\boxed{g=59}$ hundred USD, or \$5,900. The increase from 48 is $(59-48)\times\$100=\$1,100$ in high-attendance profit.

At $g=59$, $C_2$ has payoffs $(59,32)$, row maximum 59, row minimum 32, maximum regret 21, and
\[
EMV(C_2)=0.4(59)+0.6(32)=23.6+19.2=42.8.
\]
$C_1$ remains unchanged: maximum 80, minimum 10, maximum regret 22, and EMV $0.4(80)+0.6(10)=38$. All four updated recommendations are:
'''+table([('Maximax','C_1','Row maximum: 80'),('Maximin','C_2','Row minimum: 32'),('Minimax Regret','C_2','Maximum regret: 21'),('EMV/Bayes','C_2','EMV: 42.8')])+r'''There are no ties at $g=59$; the boundary tie at $g=58$ belongs to Minimax Regret only.
'''+nav(q)
# C9: original data, followed by fixed-summary filtering tables and vertical trees.
configs=[(3,'Book Fair Stock','D',[(1,'EMV/Bayes: keep 2 highest EMVs',[(1,65),(2,65),(3,65)],[(4,59),(5,53),(6,43)]),(2,'Maximin: select highest Min',[(3,20)],[(1,0),(2,10)])], 'The book fair selects $D_3$: it shares the highest EMV of 65 and has the highest minimum profit, 20 hundred USD, among the retained plans.'),
(4,'Refill Shop Expansion','F',[(1,'Minimax Regret: keep 5 lowest',[(3,25),(2,30),(4,35),(1,45),(5,45)],[(6,55)]),(2,'EMV/Bayes: keep 4 highest',[(4,70),(3,68.5),(2,64.5),(5,64)],[(1,61)]),(3,'Maximax: keep 2 highest Max',[(2,105),(3,95)],[(4,85),(5,75)]),(4,'Maximin: select highest Min',[(3,25)],[(2,15)])], 'The refill shop selects $F_3$: after the regret, EMV, and upside filters, its minimum profit of 25 thousand USD exceeds $F_2$\'s 15.'),
(5,'School Supply Orders','H',[(1,'Maximin: keep 4 highest Min',[(5,45),(6,40),(4,35),(3,25)],[(2,15),(1,0)]),(2,'Minimax Regret: keep 3 lowest',[(3,25),(4,35),(5,45)],[(6,55)]),(3,'Maximax: keep 2 highest Max',[(3,95),(4,85)],[(5,75)]),(4,'EMV/Bayes: select highest EMV',[(4,70)],[(3,68.5)])], 'The school supplier selects $H_4$: after the downside, regret, and upside filters, its EMV of 70 hundred USD exceeds $H_3$\'s 68.5.')]
for q,title,L,stages,interpretation in configs:
 block=exam.split('\\SubsectionBox{'+str(q)+'. ')[1].split('\\SubsectionBox{')[0]
 stem=block.split('}\n',1)[1].split('Apply these stages')[0]
 s+=f'\\clearpage\n\\sectionScored{{{title}}}{{C9-\\sml{{2}}}}{{sec:q{q}}}\n'+stem
 s+=r'''Use the supplied summary statistics directly, including the original maximum regrets; no statistic is recalculated after filtering. Compare only survivors at each stage and retain all cutoff ties.
'''
 s+='\\begin{enumerate}\n'+''.join('\\item '+rule+'.\n' for _,rule,_,_ in stages)+'\\end{enumerate}\n'
 s+='\\QuestionsTasks{\n{9}/{sol:q'+str(q)+'tree}/{Construct the filtering tree and give a one-sentence interpretation. \\score{1}},\n{9}/{sol:q'+str(q)+'table}/{Construct a supporting table with rules, values, survivors, eliminations, and final choice. \\score{1}}\n}\n'
 s+=anchor(q,'table','Supporting filtering table '+r'\score{1}')
 s+=r'''\begin{center}\small
\begin{tabularx}{\textwidth}{@{}c >{\raggedright\arraybackslash}p{0.24\textwidth} >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}p{0.23\textwidth}@{}}
\toprule
Step & Rule & Survivors (relevant values) & Eliminated (values)\\\midrule
'''
 s+='0 & Initial alternatives & $'+','.join(f'{L}_{i}' for i in range(1,7))+'$ & ---\\\\\n'
 def vals(xs):return ', '.join(f'${L}_{i}({v})$' for i,v in xs)
 for n,rule,kept,elim in stages:
  s+=f'{n} & {rule} & '+('\\textbf{Selected:} ' if n==len(stages) else '')+vals(kept)+' & '+vals(elim)+r'\\'+'\n'
 s+='\\bottomrule\\end{tabularx}\n\\end{center}\n'
 if q==3:s+='The second-ranked EMV is 65, shared by $D_1,D_2,D_3$, so all three survive the first stage. The final comparison uses only their minima $0,10,20$.\n'
 if q==4:s+='At the first cutoff, $F_1$ and $F_5$ both have regret 45, and both survive. Later cutoffs have no ties.\n'
 if q==5:s+='The cutoffs are Min 25, maximum regret 45, and Max 85; the final EMV comparison is 70 versus 68.5. There are no cutoff or final ties.\n'
 s+=nav(q)+anchor(q,'tree','Filtering tree and interpretation '+r'\score{1}')
 s+='\\begin{center}\n\\begin{tikzpicture}[>=Stealth]\n\\node[cNine survivor] (s0) at (0,0) {All six $'+L+'_i$};\n'
 prev='s0'
 for n,rule,kept,elim in stages:
  y=-1.65*n
  style='cNine selected' if n==len(stages) else 'cNine survivor'
  s+=f'\\node[{style}] (s{n}) at (0,{y}) '+'{'+('\\textbf{Selected:} ' if n==len(stages) else '')+'$'+','.join(f'{L}_{i}' for i,_ in kept)+'$};\n'
  s+=f'\\draw[cNine keep] ({prev}) -- node[right,font=\\small] '+'{'+rule+f'}} (s{n});\n'
  s+=f'\\node[cNine eliminated] (e{n}) at (6,{y}) '+'{Eliminate $'+','.join(f'{L}_{i}' for i,_ in elim)+'$};\n'
  s+=f'\\draw[cNine discard] (s{n}) -- (e{n});\n'
  prev=f's{n}'
 s+='\\end{tikzpicture}\n\\end{center}\n'+interpretation+'\n'+nav(q)
s+=r'''\section*{C10}
\href{https://nolopez338.github.io/global_economics/grade10/src/pages/term1/g10-t1-c10dashboard.html}{C10 example solution.}
\end{document}
'''
path=root/'book2026-2027/grade10/term_1/3-learning_evidences/G10_T1_L2_C8C9C10_exam_solution.tex'
path.write_text(s)
print(path)
