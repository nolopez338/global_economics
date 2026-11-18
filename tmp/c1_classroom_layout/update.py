from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.tex')
s=p.read_text(encoding='utf-8')
start=s.index('\\ifprintsolutions\n\\clearpage')
a,b=s[:start],s[start:]
ref=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex').read_text(encoding='utf-8')
helpers=ref[ref.index('% Solution rows are indivisible'):ref.index('\\begin{document}')]
b=b.replace('\\section*{Solutions}', '\\input{graphs/G10_T2_bar_graphs.tex}\n'+helpers+'\\section*{Solutions}',1)
b=re.sub(r'\\begin\{tabularx\}.*?\\end\{tabularx\}\n', '', b, flags=re.S)
b=b.replace('\\clearpage\n\\section*{Solutions (continued)}\n','')
# Labels, probability calculations, values, grouped outcomes, masses, and grid steps.
data=[
(3,'A',['Early','On time','Slightly late','Very late'],['0.18','0.47','0.23','0.12'],[2,2,0,-3],[-3,0,2],['Very late','Slightly late','Early and on time'],['0.12','0.23','0.18+0.47=0.65'],['0.12','0.23','0.65'],1,1),
(4,'F',[r'\mathrm{KK}',r'\mathrm{KC}',r'\mathrm{CK}',r'\mathrm{CC}'],['0.80\\cdot0.65=0.52','0.80\\cdot0.35=0.28','0.20\\cdot0.65=0.13','0.20\\cdot0.35=0.07'],[6,3,3,0],[0,3,6],[r'\(\mathrm{CC}\)',r'\(\mathrm{KC}\) and \(\mathrm{CK}\)',r'\(\mathrm{KK}\)'],['0.07','0.28+0.13=0.41','0.52'],['0.07','0.41','0.52'],3,3),
(5,'C',['Orchard','Cooperative','Wholesaler','Grocery'],['0.28','0.19','0.31','0.22'],[14,18,14,22],[14,18,22],['Orchard and wholesaler','Cooperative','Grocery'],['0.28+0.31=0.59','0.19','0.22'],['0.59','0.19','0.22'],5,2),
(6,'M',[r'\mathrm{HS}',r'\mathrm{HN}',r'\mathrm{RS}',r'\mathrm{RN}'],['0.30\\cdot0.25=0.075','0.30\\cdot0.75=0.225','0.70\\cdot0.25=0.175','0.70\\cdot0.75=0.525'],[0,6,-6,0],[-6,0,6],[r'\(\mathrm{RS}\)',r'\(\mathrm{HS}\) and \(\mathrm{RN}\)',r'\(\mathrm{HN}\)'],['0.175','0.075+0.525=0.600','0.225'],['0.175','0.600','0.225'],3,6),
(7,'R',['Front gate','Main aisle','Side aisle','Rear row','Outdoor row'],['0.12','0.23','0.18','0.27','0.20'],[0,0,10,10,20],[0,10,20],['Front gate and main aisle','Side aisle and rear row','Outdoor row'],['0.12+0.23=0.35','0.18+0.27=0.45','0.20'],['0.35','0.45','0.20'],5,10),
(8,'D',[r'\mathrm{RR}',r'\mathrm{RN}',r'\mathrm{NR}',r'\mathrm{NN}'],['0.15\\cdot0.40=0.06','0.15\\cdot0.60=0.09','0.85\\cdot0.40=0.34','0.85\\cdot0.60=0.51'],[15,12,12,0],[0,12,15],[r'\(\mathrm{NN}\)',r'\(\mathrm{RN}\) and \(\mathrm{NR}\)',r'\(\mathrm{RR}\)'],['0.51','0.09+0.34=0.43','0.06'],['0.51','0.43','0.06'],3,3)]
def hl(kind,t,math=False):
    t='\\GTenHL'+kind+'{'+str(t)+'}'
    return '\\('+t+'\\)' if math else t
def calc(t):
    if '=' in t:
        lhs,rhs=t.split('=')
        return '\\('+lhs+'\\)\\newline '+hl('Probability','='+rhs,True)
    return hl('Probability',t,True)
def table(head,rows,pmf=False):
    widths='.18' if pmf else '.32'
    second='.32' if pmf else '.40'
    return '\\begin{tabularx}{\\linewidth}{|>{\\raggedright\\arraybackslash}p{'+widths+'\\linewidth}|>{\\raggedright\\arraybackslash}p{'+second+'\\linewidth}|>{\\raggedright\\arraybackslash}X|}\n\\hline\n'+head+' \\\\ \\hline\n'+'\n'.join(' & '.join(row)+' \\\\ \\hline' for row in rows)+'\n\\end{tabularx}'
for n,var,labels,probs,vals,xs,groups,calcs,masses,ystep,xstep in data:
    pat=r'(\\problemtitle\{'+str(n)+r'\}.*?)(?=\\problemtitle|\\fi)'
    m=re.search(pat,b,re.S); block=m.group(1)
    if n!=3: block='\\clearpage\n'+block
    if n>=4: block=block.replace('\\problemtitle{'+str(n), '\\section*{Solutions (continued)}\n\\problemtitle{'+str(n),1)
    mathlabels=[('\\('+v+'\\)' if v.startswith('\\') else v) for v in labels]
    rows=[[hl('Outcome',l),calc(pr),hl('Value',v,True)] for l,pr,v in zip(mathlabels,probs,vals)]
    head=hl('Outcome','Complete outcome')+' & '+hl('Probability','Probability')+' & '+hl('Value',var,True)+' (USD)'
    cats=','.join(('$'+l+'$' if l.startswith('\\') else l) for l in labels)
    pv=','.join(pr.split('=')[-1] for pr in probs)
    common=r'width=\linewidth,height=4.7cm,rotate=35,xlabel={\GTenHLOutcome{Outcome}},xhighlight=GTenHLOutcome'
    gp='\\GTenOutcomeProbabilityGraph['+common+r',ylabel={\GTenHLProbability{Probability}},yhighlight=GTenHLProbability,color=GTenHLProbability!32]{'+cats+'}{'+pv+'}'
    gv='\\GTenOutcomeValueGraph['+common+',ystep='+str(ystep)+r',ylabel={$\GTenHLValue{'+var+r'}(\GTenHLOutcome{\omega})$ \GTenHLValue{(USD)}},yhighlight=GTenHLValue,color=GTenHLValue!32]{'+cats+'}{'+','.join(map(str,vals))+'}'
    outcome='\n\\GTenSolutionOutcomes{'+table(head,rows)+'}{\n'+gp+'\n}{\n'+gv+'\n}\n'
    block=block.replace('\\task{2}',outcome+'\n\\task{2}',1)
    head=hl('Value',var.lower(),True)+' (USD) & Outcomes giving that value & Calculation and '+hl('Probability',r'\(p_'+var+'('+var.lower()+')\)')
    rows=[[hl('Value',x,True),hl('Outcome',g),calc(c)] for x,g,c in zip(xs,groups,calcs)]
    graph=r'\GTenPMFGraph[width=\linewidth,height=4.7cm,xstep='+str(xstep)+r',xlabel={\GTenHLValue{$'+var.lower()+r'$ (USD)}},ylabel={\GTenHLProbability{Probability}},xhighlight=GTenHLValue,yhighlight=GTenHLProbability,color=GTenHLProbability!32]{'+','.join(map(str,xs))+'}{'+','.join(masses)+'}'
    pmf='\n\\GTenSolutionPMF{'+table(head,rows,True)+'}{\n'+graph+'\n}\n'
    block=block.replace('\\task{3}',pmf+'\n\\task{3}',1)
    b=b[:m.start()]+block+b[m.end():]
p.write_text(a+b,encoding='utf-8',newline='\n')
assert p.read_text(encoding='utf-8').split('\\ifprintsolutions\n\\clearpage')[0]==a
print('Updated only solutions; six complete-outcome rows and six grouped PMF rows.')
