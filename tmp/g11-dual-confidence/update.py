from pathlib import Path
import re
from decimal import Decimal as D
root=Path('book/grade11/term_2/4-learning_evidences')
e=root/'G11_T2_L1_C1C2_exam_1.tex'
s=root/'G11_T2_L1_C1C2_exam_solution_1.tex'
exam=e.read_text(encoding='utf-8'); sol=s.read_text(encoding='utf-8')
oldexam=exam; oldsol=sol
start=exam.index('Ten subsequent independent studies')
end=exam.index('Complete all five',start)
description=r'''Ten subsequent independent studies each use 196 businesses, the same known population standard deviation and both the 80\% and 98\% normal confidence procedures. These are additional studies, separate from both samples above. Each study builds both intervals around its own sample mean. The 98\% interval is wider and contains that study's 80\% interval. A later comprehensive investigation of the entire September population establishes its mean bill as 315 thousand COP. Repeated samples do not establish this value. The table records mutually exclusive retrospective coverage categories for these same ten studies.

\examtable{Kr}{
\textbf{Intervals covering the later established mean}&\textbf{Studies}\\\midrule
Both confidence levels&5\\
Only the 98\% level&3\\
Neither confidence level&2\\}

'''
exam=exam[:start]+description+exam[end:]
exam=exam.replace('initially unknown mean at 98\\% confidence.', 'initially unknown mean at 80\\% and 98\\% confidence.',1)
start=sol.index('Ten subsequent independent studies'); end=sol.index('Complete all five',start)
sol=sol[:start]+description.replace('\\examtable','\\keytable')+sol[end:]
# Restrict all subsequent edits to Problem 1 and its summary.
p1start=sol.index('\\sectionScored{Retail electricity'); p1end=sol.index('\\sectionScored{Savings-account')
p=sol[p1start:p1end]
p=p.replace('initially unknown mean at 98\\% confidence.', 'initially unknown mean at 80\\% and 98\\% confidence.')
p=p.replace(r'at \CtwoConfidence{98\%} \CtwoConfidence{confidence}.',r'at \CtwoConfidence{80\%} and \CtwoConfidence{98\%} \CtwoConfidence{confidence}.')
# Reuse the established dual-level procedure-setting rows of Problem 2.
settings_start=r'$\CtwoConfidence{C}$&'
a=p.index(settings_start); b=p.index('\\\\}',a)+4
q=sol[sol.index('\\sectionScored{Savings-account'):]
c=q.index(settings_start); d=q.index('\\\\}',c)+4
p=p[:a]+q[c:d]+p[b:]
# Add the 80% worked table and interpretation by adapting the existing 98% work.
a=p.index(r'\textbf{\CtwoConfidence{98\%} confidence}'); b=p.index(r'\secInicio',a)
work98=p[a:b]
work80=work98
for x,y in [('98\\%','80\\%'),('2.326','1.282'),('16.282','8.974'),('293.718','301.026'),('326.282','318.974'),('32.564','17.948')]:
    work80=work80.replace(x,y)
p=p[:a]+work80+r'\Needspace{22\baselineskip}'+'\n'+work98+r'''The \CtwoConfidence{98\%} interval contains the \CtwoConfidence{80\%} interval: both use the same center and SE, while the larger critical value increases the margin and full width, giving less precision at higher confidence.

'''+p[b:]
# Replace endpoint excerpts and endpoint-based counting with category-based work.
a=p.index('Ten subsequent independent studies',p.index(r'\worked{C2 Task 3'))
b=p.index(r'\Needspace{14\baselineskip}',a)
coverage=r'''Ten subsequent independent studies each use \CtwoSize{196} businesses, the same known \CtwoSD{population standard deviation} and both the \CtwoConfidence{80\%} and \CtwoConfidence{98\%} normal confidence procedures. These are additional studies, separate from samples A and B. Each study builds both intervals around its own sample mean. Its \CtwoConfidence{98\%} interval is wider and contains its \CtwoConfidence{80\%} interval.
\end{probleminfoexcerpt}

\begin{probleminfoexcerpt}
A later comprehensive investigation of the entire September population establishes its \CtwoMean{mean bill} as \CtwoMean{315} thousand COP. Repeated samples do not establish this value. The categories below concern coverage of that same fixed population mean by these ten subsequent studies only.
\end{probleminfoexcerpt}

\keytable{Kr}{
\textbf{Intervals covering the later established mean}&\textbf{Studies}\\\midrule
Both confidence levels&\CtwoCoverage{5}\\
Only the \CtwoConfidence{98\%} level&\CtwoCoverage{3}\\
Neither confidence level&\CtwoCoverage{2}\\}

\keytable{p{.12\linewidth}KK}{
\textbf{Level}&\textbf{Covering and missing counts}&\textbf{Coverage and absolute difference}\\\midrule
$\CtwoConfidence{80\%}$&Cover: $\CtwoCoverage{5}$; miss: $\CtwoCoverage{3+2=5}$&$\CtwoCoverage{5}/\CtwoCoverage{10}\times100\%=\CtwoCoverage{50\%}$; $|\CtwoCoverage{50}-\CtwoConfidence{80}|=\CtwoError{30}$ percentage points.\\
$\CtwoConfidence{98\%}$&Cover: $\CtwoCoverage{5+3=8}$; miss: $\CtwoCoverage{2}$&$\CtwoCoverage{8}/\CtwoCoverage{10}\times100\%=\CtwoCoverage{80\%}$; $|\CtwoCoverage{80}-\CtwoConfidence{98}|=\CtwoError{18}$ percentage points.\\}

The categories sum to $5+3+2=10$. The \CtwoConfidence{80\%} procedure covers the later-established mean of \CtwoMean{315} thousand COP in five studies, \CtwoError{30} percentage points below nominal confidence. The \CtwoConfidence{98\%} procedure covers it in eight studies, \CtwoError{18} percentage points below nominal confidence. Nesting excludes a category where only the narrower interval covers. Samples A and B are excluded from both denominators.

\textbf{Consistency with the retained studies.} Their sample means, in study order, are 300, 312, 320, 334, 302, 318, 308, 330, 298 and 316 thousand COP. Comparing each distance from \CtwoMean{315} with the margins \CtwoMoE{8.974} and \CtwoMoE{16.282}, studies 2, 3, 6, 7 and 10 cover at both levels; 1, 5 and 8 cover only at 98\%; 4 and 9 cover at neither. Each study's intervals have full widths \CtwoWidth{17.948} and \CtwoWidth{32.564} thousand COP and its own sample mean as center.

'''
p=p[:a]+coverage+p[b:]
# Rubrics are adapted only after verifying the complete mathematical work.
means=[300,312,320,334,302,318,308,330,298,316]
assert D(98)/D(196).sqrt()==7
for z,m,l,u,w in [('1.282','8.974','301.026','318.974','17.948'),('2.326','16.282','293.718','326.282','32.564')]:
    margin=D(z)*7
    assert (margin,D(310)-margin,D(310)+margin,2*margin)==tuple(map(D,(m,l,u,w)))
assert [sum(abs(D(x)-315)<=m for x in means) for m in [D('8.974'),D('16.282')]]==[5,8]
assert abs(50-80)==30 and abs(80-98)==18
p=p.replace('0.5 complete procedure settings at all requested levels.', '0.5 complete procedure settings (0.25 per confidence level).')
p=p.replace('0.4 point estimate; 0.4 correct margins using known SD; 0.6 endpoints and intervals; 0.3 full widths; 0.3 units and contextual mean interpretation.', '0.4 shared point estimate; 0.4 margins using known SD (0.2 per level); 0.6 endpoints and intervals (0.3 per level); 0.3 full widths (0.15 per level); 0.3 units and contextual mean interpretations (0.15 per level).')
p=p.replace('0.25 correct covering counts; 0.25 coverage percentages; 0.25 absolute differences in percentage points; 0.25 valid coverage/finite-study interpretation.', '0.25 covering counts (0.125 per level); 0.25 coverage percentages (0.125 per level); 0.25 absolute differences in percentage points (0.125 per level); 0.25 valid coverage/finite-study interpretation for both levels, excluding A and B.')
sol=sol[:p1start]+p+sol[p1end:]
# Adapt summary tables using Problem 2's existing two-level conventions.
a=sol.index(r'\label{summary:p1}'); b=sol.index(r'\subsection*{Problem 2:',a)
summary=sol[a:b]
row=r'$\CtwoConfidence{98\%}$ & $\CtwoSignificance{0.02}$'
pos=summary.index(row)
summary=summary[:pos]+r'$\CtwoConfidence{80\%}$ & $\CtwoSignificance{0.20}$ & $\CtwoSignificance{0.10}$ & $\CtwoCritical{1.282}$\\'+'\n'+summary[pos:]
c=summary.index(r'\keytable{p{.30\linewidth}K}'); d=summary.index(r'\Needspace{7\baselineskip}',c)
q=sol[sol.index(r'\label{summary:p2}'):]
qa=q.index(r'\keytable{p{.30\linewidth}KK}'); qb=q.index(r'\Needspace{7\baselineskip}',qa)
table=q[qa:qb]
for x,y in [('110','310'),('5.128','8.974'),('9.304','16.282'),('104.872','301.026'),('100.696','293.718'),('115.128','318.974'),('119.304','326.282'),('10.256','17.948'),('18.608','32.564')]: table=table.replace(x,y)
summary=summary[:c]+table+summary[d:]
pos=summary.index(r'$\CtwoConfidence{98\%}$ & $\CtwoCoverage{8}')
summary=summary[:pos]+r'$\CtwoConfidence{80\%}$ & $\CtwoCoverage{5}/\CtwoCoverage{10}$ & $\CtwoCoverage{50\%}$ & $\CtwoError{30}$\\'+'\n'+summary[pos:]
summary=summary.replace('Count subsequent intervals with', r'At $\CtwoConfidence{98\%}$, covering count $\CtwoCoverage{5}+\CtwoCoverage{3}=\CtwoCoverage{8}$; the wider interval contains the $\CtwoConfidence{80\%}$ interval. Coverage concerns $\CtwoMean{315}$ thousand COP. Count subsequent intervals with')
sol=sol[:a]+summary+sol[b:]
# Preserve all other content exactly, including Problems 2 and 3.
assert exam[exam.index('\\SubsectionBox{Savings-account'):]==oldexam[oldexam.index('\\SubsectionBox{Savings-account'):]
for begin,end in [(r'\sectionScored{Savings-account',r'\label{summary:p1}'),(r'\subsection*{Problem 2:',r'\end{document}')]:
    assert sol[sol.index(begin):sol.index(end)]==oldsol[oldsol.index(begin):oldsol.index(end)]
for path,content in [(e,exam),(s,sol)]:
    with path.open('w',encoding='utf-8',newline='\n') as f: f.write(content)
print('Verified calculations, retained-study coverage, and unchanged Problems 2 and 3; updated both sources.')
