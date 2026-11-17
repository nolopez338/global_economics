from pathlib import Path
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex')
s=p.read_text(encoding='utf-8')
for key,width,pwidth,gwidth,body in [
('calls','.34','.25','.37',r'''\small\setlength{\tabcolsep}{2pt}
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X cc@{}}\toprule
$\cTwoOutcome{\omega}$ (outcome) & Probability & $\cTwoValue{X}$ (\cTwoValue{calls}) \\\midrule
$\cTwoOutcome{\omega_{n,j}}$ & $\cTwoMassHL{2^{-n}}$ & $\cTwoValue{n}$ \\\bottomrule
\end{tabularx}
\par\small For each integer $n\geq3$, list in lexicographic order (N before S) every length-$n$ string whose first SNS ends at call $n$. Write $\cTwoOutcome{\omega_{n,j}}$ for its $j$th string, $1\leq j\leq c_{n-1}$. The indexed row applies separately to every such string.
\par Examples: $\cTwoOutcome{\omega_{3,1}=\mathrm{SNS}}$; $\cTwoOutcome{\omega_{4,1}=\mathrm{NSNS}}$, $\cTwoOutcome{\omega_{4,2}=\mathrm{SSNS}}$. Infinite non-stopping sequences have probability zero.'''),
('reserve','.30','.30','.36',r'''\small\setlength{\tabcolsep}{2pt}
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X cc@{}}\toprule
$\cTwoOutcome{\omega}$ (outcome) & Probability & $\cTwoValue{X}$ (\cTwoValue{USD}) \\\midrule
$\cTwoOutcome{\pi_j}$ & $\cTwoMassHL{1/10!}$ & $\cTwoValue{-\min_i b_i(\pi_j)}$ \\\bottomrule
\end{tabularx}
\par\small Label the distinct slips $R_1,\ldots,R_5,P_1,\ldots,P_5$. List all their permutations lexicographically in this label order as $\cTwoOutcome{\pi_j}$, $1\leq j\leq10!$. Each indexed row is one distinct-slip order.
\par For $0\leq i\leq10$, $b_i(\pi_j)$ is receipts minus payments among its first $i$ slips, with $b_0=0$. The minimum is over these eleven balances.''')]:
 a=s.index('\\stage{'+key+'}{1}'); b=s.index('\\stage{'+key+'}{2}',a); part=s[a:b]
 start=part.index(r'\par\noindent\begin{minipage}'); end=part.index(r'\end{minipage}\par',start)+len(r'\end{minipage}\par')
 row=part[start:end].replace(r'{.33\linewidth}','{'+pwidth+r'\linewidth}',1).replace(r'{.64\linewidth}','{'+gwidth+r'\linewidth}',1)
 row=row.replace(r'\vspace{0pt}\centering',r'\vspace{0pt}\centering\setlength{\tabcolsep}{2pt}',1)
 new=r'\begin{minipage}[t]{'+width+r'\linewidth}\vspace{0pt}'+'\n'+body+'\n'+r'\end{minipage}\hfill'
 row=row.replace(r'\par\noindent',r'\par\noindent'+new,1)
 row=row.replace('height=5cm','height=4cm')
 part=part[:start]+row+part[end:]; s=s[:a]+part+s[b:]
p.write_text(s,encoding='utf-8')
