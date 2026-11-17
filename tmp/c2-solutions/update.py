from pathlib import Path
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C2_classroom_activity.tex')
s=Path('tmp/c2-solutions/original.tex').read_text(encoding='utf-8')
head,sol=s.split('\n\\ifprintsolutions\n',1)
head=head.replace('\\printsolutionsfalse % Set \\printsolutionstrue to append the complete review solutions.','\\printsolutionstrue % Set \\printsolutionsfalse for the original student-only handout.')
head=head.replace('Disable instructional highlights throughout this activity.','Disable instructional highlights on all student pages.')
sol=sol.replace('  \\clearpage\n  \\stageheading{Solutions}',r'''  \clearpage
  % Scope highlights and restore colors already neutralized in the preamble.
  \begingroup
  \GTenHighlightstrue
  \colorlet{cTwoMassColor}{blue!75!black}
  \colorlet{cTwoCDFColor}{cyan!65!blue!80!black}
  \colorlet{cTwoGuideColor}{cTwoMassColor!35}
  \small
  \stageheading{Solutions}''',1)
sol=sol.replace('  \\task{1}{Let $X$ be the additional late fee for one completed rental, in USD; exclude the prepaid\n    rental charge. The support is $S_X=\\{0,6,12,18,24\\}$, with $p_X(x)=0$ elsewhere.',r'''  \task{1}{Let $\cTwoValue{X}$ be the \cTwoValue{additional late fee} for one completed rental, in
    \cTwoValue{USD}; exclude the prepaid rental charge. The support is
    $\cTwoValue{S_X}=\cTwoValue{\{0,6,12,18,24\}}$, with $\cTwoMassHL{p_X(x)}=\cTwoMassHL{0}$ elsewhere.''')
# Add semantic treatment to the guided solution's plain table values.
import re
sol=re.sub(r'(?m)^(    \\cTwoOutcome\{.*?\} & \$\\cTwoMassHL\{.*?\}\$ & )\$(-?\d+)\$',r'\1$\\cTwoValue{\2}$',sol)
sol=re.sub(r'(?m)^    \$(\d+)\$ & \$([\d.]+)\$ & (.*?) \\\\',r'    $\\cTwoValue{\1}$ & $\\cTwoMassHL{\2}$ & \3 \\\\',sol)
# Explain every grouped mass before accumulating.
adds={3:r'''  \textbf{Grouping.} Mutually exclusive outcomes with the same payment are added:
  $\cTwoMassHL{p_X(0)}=\cTwoMassHL{0.20}$,
  $\cTwoMassHL{p_X(4)}=\cTwoMassHL{0.12}+\cTwoMassHL{0.18}=\cTwoMassHL{0.30}$,
  $\cTwoMassHL{p_X(9)}=\cTwoMassHL{0.15}+\cTwoMassHL{0.10}=\cTwoMassHL{0.25}$,
  and $\cTwoMassHL{p_X(15)}=\cTwoMassHL{0.25}$.
''',4:r'''  \textbf{Grouping.} The missing probability is valid because $0\leq0.35\leq1$.
  The first three counts give masses $\cTwoMassHL{0.15},\ \cTwoMassHL{0.20},\ \cTwoMassHL{0.35}$.
  Both 3 and 4 claims reach the cap, so
  $\cTwoMassHL{p_X(15)}=\cTwoMassHL{0.20}+\cTwoMassHL{0.10}=\cTwoMassHL{0.30}$.
''',5:r'''  \textbf{Grouping.} Independence gives $P(\mathrm{NNN})=0.7^3=0.343$,
  each one-buyer sequence probability $0.3(0.7)^2=0.147$,
  each two-buyer sequence probability $(0.3)^2(0.7)=0.063$, and
  $P(\mathrm{BBB})=(0.3)^3=0.027$. Hence
  $\cTwoMassHL{p_X(7)}=3(\cTwoMassHL{0.147})=\cTwoMassHL{0.441}$ and
  $\cTwoMassHL{p_X(14)}=3(\cTwoMassHL{0.063})=\cTwoMassHL{0.189}$;
  the other masses are $\cTwoMassHL{0.343}$ at 0 USD and $\cTwoMassHL{0.027}$ at 16 USD.
''',6:r'''  \textbf{Outcome calculations.} In table order, independence gives
  $0.20(0.4)=0.08$, $0.20(0.6)=0.12$, $0.30(0.4)=0.12$,
  $0.30(0.6)=0.18$, $0.50(0.4)=0.20$ and $0.50(0.6)=0.30$.
  Applying $R_1+R_2-7$ gives $10,17,-7,0,0,7$ USD, respectively.
  Only the two break-even outcomes merge:
  $\cTwoMassHL{p_X(0)}=\cTwoMassHL{0.18}+\cTwoMassHL{0.20}=\cTwoMassHL{0.38}$.
'''}
for n,a in adds.items():
 start=sol.index('  \\problemtitle{'+str(n)+'}')
 at=sol.index('  $\\cTwoValue{S_X}',start)
 sol=sol[:at]+a+sol[at:]
# Replace terse accumulation lists with explicit additions in the same task.
seqs=[(['0.50','0.18','0.12','0.08','0.12'],['0.50','0.68','0.80','0.88','1']),(['0.2','0.3','0.25','0.25'],['0.2','0.5','0.75','1']),(['0.15','0.20','0.35','0.30'],['0.15','0.35','0.70','1']),(['0.343','0.441','0.189','0.027'],['0.343','0.784','0.973','1']),(['0.12','0.38','0.30','0.08','0.12'],['0.12','0.50','0.80','0.88','1'])]
pat=r'\\task\{2\}\{Accumulate.*?mass(?:es)?\.\}'
matches=list(re.finditer(pat,sol,re.S))
assert len(matches)==5,len(matches)
for m,(mass,cum) in reversed(list(zip(matches,seqs))):
 chain=r'\cTwoCDFHL{'+cum[0]+'}'
 for i in range(1,len(mass)):
  chain+=r';\ '+r'\cTwoCDFHL{'+cum[i-1]+r'}+\cTwoMassHL{'+mass[i]+r'}=\cTwoCDFHL{'+cum[i]+'}'
 text=r'\task{2}{Use $\cTwoCDFHL{F_X(x)}=P(\cTwoValue{X}\leq x)$ and accumulate in increasing support order: $'+chain+r'$. Below the minimum, no mass is included.}'
 sol=sol[:m.start()]+text+sol[m.end():]
# Expand requested CDF evaluations into sums, then keep the existing contextual readings.
repls={
'$F_X(9)=0.75$':r'$\cTwoCDFHL{F_X(9)}=P(X\leq9)=0.20+0.30+0.25=\cTwoCDFHL{0.75}$',
'$F_X(10)=0.7$':r'$\cTwoCDFHL{F_X(10)}=P(X\leq10)=0.15+0.20+0.35=\cTwoCDFHL{0.70}$',
'$F_X(14)=0.973$':r'$\cTwoCDFHL{F_X(14)}=P(X\leq14)=0.343+0.441+0.189=\cTwoCDFHL{0.973}$',
'$F_X(0)=0.5$':r'$\cTwoCDFHL{F_X(0)}=P(X\leq0)=0.12+0.38=\cTwoCDFHL{0.50}$'}
for a,b in repls.items(): sol=sol.replace(a,b)
sol=sol.replace('\\cTwoOutcome{1 claims}','\\cTwoOutcome{1 claim}')
# Reuse semantic roles on quantity names and units in independent explanations.
for name in ['buyback payment','total payout','total revenue','signed net result']:
 sol=sol.replace('be the '+name,'be the \\cTwoValue{'+name+'}')
sol=sol.replace('in USD.',r'in \cTwoValue{USD}.')
sol=sol.replace('\\textbf{PMF check.}',r'\textbf{\cTwoMassHL{PMF} check.}').replace('\\textbf{CDF check.}',r'\textbf{\cTwoCDFHL{CDF} check.}')
# State the jump identity in every check, alongside each numerical jump list.
sol=sol.replace('reproduce the PMF.',r'reproduce the PMF: $\cTwoCDFHL{F_X(a)}-\cTwoCDFHL{F_X(a^-)}=\cTwoMassHL{p_X(a)}$ at each supported value $a$.')
sol=sol.replace('\\fi\n\\end{document}', '  \\endgroup % Restore the student-page highlight and graph settings.\n\\fi\n\\end{document}')
p.write_text(head+'\n\\ifprintsolutions\n'+sol,encoding='utf-8')
print('Updated existing solution block; five accumulation tasks expanded.')

