from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex')
s=p.read_text(encoding='utf-8')
macros=r'''
% Solution rows are indivisible; every child uses its own local linewidth.
\newcommand{\GTenSolutionOutcomes}[3]{%
  \par\medskip\noindent\begin{minipage}{\linewidth}
  \begin{minipage}[t]{.40\linewidth}\vspace{0pt}\small
    \setlength{\tabcolsep}{3pt}#1
  \end{minipage}\hfill%
  \begin{minipage}[t]{.28\linewidth}\vspace{0pt}#2\end{minipage}\hfill%
  \begin{minipage}[t]{.28\linewidth}\vspace{0pt}#3\end{minipage}
  \end{minipage}\par\medskip}
\newcommand{\GTenSolutionPMF}[2]{%
  \par\medskip\noindent\begin{minipage}{\linewidth}
  \begin{minipage}[t]{.68\linewidth}\vspace{0pt}\small
    \setlength{\tabcolsep}{4pt}#1
  \end{minipage}\hfill%
  \begin{minipage}[t]{.30\linewidth}\vspace{0pt}#2\end{minipage}
  \end{minipage}\par\medskip}
'''
s=s.replace(r'\begin{document}',macros+'\n'+r'\begin{document}',1)
# Only edit worked solutions that already have outcome / grouped PMF tables.
pat=r'(\\workedsolution\{[^\n]+\})(.*?)(?=\\secInicio)'
def wrap_fragments(t):
    # Highlight each word in long names so the table can wrap naturally.
    return re.sub(r'\\GTenHLOutcome\{([^{}]+)\}', lambda m: ' '.join(r'\GTenHLOutcome{'+w+'}' for w in m[1].split()) if ' ' in m[1] else m[0], t)
def table(cols, rows):
    # Permit line breaks within the existing inline calculations.
    t='\n'.join(rows)
    t=t.replace(r'\times',r'\times\allowbreak ').replace('+',r'+\allowbreak ').replace('=',r'=\allowbreak ')
    t=wrap_fragments(t)
    return r'\begin{tabularx}{\linewidth}{'+cols+'}\n'+t+'\n'+r'\end{tabularx}'
def apply(m):
    lead,b=m[1],m[2]
    ts=list(re.finditer(r'\\begin\{center\}\s*(\\begin\{tabularx\}.*?\\end\{tabularx\})\s*\\end\{center\}',b,re.S))
    if not ts:return m[0]
    panels=list(re.finditer(r'\\begin\{minipage\}\[t\]\{[^\n]+\}\s*\\centering\s*(\\GTen(?:OutcomeProbability|OutcomeValue|PMF)Graph[^\n]+)\s*(\\par\\small .*?)\s*\\end\{minipage\}',b,re.S))
    gs=[(g[1],g[2]) for g in panels]
    def graph(g):return g[0]+'\n'+g[1]+'\n'
    prob=[g for g in gs if g[0].startswith(r'\GTenOutcomeProbabilityGraph')]
    vals=[g for g in gs if g[0].startswith(r'\GTenOutcomeValueGraph')]
    pmfs=[g for g in gs if g[0].startswith(r'\GTenPMFGraph')]
    # Claims and investment originally supplied only the grouped graph.
    if not prob:
        if 'daily-insurance' in lead:
            cats,ps,vs,unit,sym='No claims,One claim,Two claims','.7,.2,.1','0,1,2','claims','X'
        else:
            cats,ps,vs,unit,sym='20 USD loss,Break-even,30 USD gain','.2,.5,.3','-20,0,30','USD','G'
        opts=r'width=\linewidth,height=4.7cm,rotate=35,xlabel={\GTenHLOutcome{Outcome}},xhighlight=GTenHLOutcome,'
        prob=[(r'\GTenOutcomeProbabilityGraph['+opts+r'ylabel={\GTenHLProbability{Probability}},yhighlight=GTenHLProbability,color=GTenHLProbability!32]{'+cats+'}{'+ps+'}', '')]
        vals=[(r'\GTenOutcomeValueGraph['+opts+r'ylabel={$\GTenHLValue{'+sym+r'}(\GTenHLOutcome{\omega})$ \GTenHLValue{('+unit+r')}},yhighlight=GTenHLValue,color=GTenHLValue!32]{'+cats+'}{'+vs+'}', '')]
    replacements=[]
    pi=0
    for ti,t in enumerate(ts):
        raw=t[1]
        rows=raw.splitlines()[1:-1]
        if 'Outcomes giving that value' in raw:
            new=r'\GTenSolutionPMF{'+table(r'@{}>{\raggedright\arraybackslash}p{.18\linewidth}>{\raggedright\arraybackslash}p{.30\linewidth}>{\raggedright\arraybackslash}X@{}',rows)+'}{\n'+graph(pmfs[pi])+'}'
            pi+=1
        else:
            # Split the multi-variable table into a row for each variable.
            header=rows[1].removesuffix(r' \\').split(' & ')
            has_names='Names in Versions' in raw
            prefix=''
            if has_names:
                names=[r'\toprule',header[0]+' & '+header[1]+r' \\',r'\midrule']
                for row in rows[3:-1]:
                    if ' & ' in row:
                        cs=row.removesuffix(r' \\').split(' & ')
                        names.append(cs[0]+' & '+cs[1]+r' \\')
                names.append(r'\bottomrule')
                prefix=table(r'@{}l>{\raggedright\arraybackslash}X@{}',names)+'\n'
            vi=3 if has_names else 2
            new=prefix
            for j,v in enumerate(vals):
                selected=[r'\toprule',header[0]+' & '+header[2 if has_names else 1]+' & '+header[vi+j]+r' \\',r'\midrule']
                for row in rows[3:]:
                    if ' & ' in row:
                        cs=row.removesuffix(r' \\').split(' & ')
                        selected.append(cs[0]+' & '+cs[2 if has_names else 1]+' & '+cs[vi+j]+r' \\')
                    else:selected.append(row)
                new+=r'\GTenSolutionOutcomes{'+table(r'@{}>{\raggedright\arraybackslash}p{.28\linewidth}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}p{.20\linewidth}@{}',selected)+'}{\n'+graph(prob[0])+'}{\n'+graph(v)+'}\n'
        replacements.append((t.start(),t.end(),new))
    # Delete the old graph rows in their entirety, retaining every caption in new rows.
    start=b.rfind(r'\Needspace{6.8cm}',0,panels[0].start())
    end=panels[-1].end()
    tail=re.match(r'\\par\\medskip',b[end:])
    if tail:end+=tail.end()
    replacements.append((start,end,''))
    for a,z,n in sorted(replacements,reverse=True): b=b[:a]+n+b[z:]
    return lead+b
s=re.sub(pat,apply,s,flags=re.S)
p.write_text(s,encoding='utf-8')
print('Outcome rows:',s.count(r'\GTenSolutionOutcomes{'),'PMF rows:',s.count(r'\GTenSolutionPMF{'))
