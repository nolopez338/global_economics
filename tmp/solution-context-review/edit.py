from pathlib import Path
import re
p=Path('book2026-2027/grade11/term_2/4-learning_evidences/G11_T2_L1_C1C2_exam_solution.tex')
s=p.read_text(encoding='utf-8')
Path('tmp/solution-context-review/original.tex').write_text(s,encoding='utf-8')
s=s.replace('Use contiguous groups in this order:', 'Use full-width section headings in this order:').replace('Columns are Symbol, Concept, Type and Meaning in context.', 'The three columns are Symbol, Concept and Meaning in context.')
means=[r'\CtwoMean{mean October} \CtwoMean{electricity bill}',r'\CtwoMean{mean October} \CtwoMean{interest credit}',r'\CtwoMean{mean delivery fee}']
spreads=[r'\CtwoSD{spread of October} \CtwoSD{electricity bills}',r'\CtwoSD{spread of October} \CtwoSD{interest credits}',r'\CtwoSD{spread of delivery fees}']
props=[r'\PP{proportion of all} \PP{eligible businesses} \PP{that used electronic} \PP{invoicing for their} \PP{October electricity bills}',r'\PP{proportion of all} \PP{eligible accounts} \PP{that had mobile banking} \PP{activated on October 31}',r'\PP{proportion of all} \PP{eligible deliveries} \PP{that included optional} \PP{parcel insurance}']
scopes=['200,000 registered retail businesses operating in Medellin throughout October 2026','500,000 positive-balance personal savings accounts at the Cartagena branch network on October 31, 2026','100,000 completed deliveries by the platform\'s registered couriers in Bogota on November 2, 2026']
for i in range(3):
    # Limit prose edits to the two requested worked tasks.
    for task in ['c1a','c2a']:
        pat=r'(\\worked\{[^\n]+\}\{sol:p'+str(i+1)+task+r'\})(.*?)(?=\\secInicio)'
        m=re.search(pat,s,re.S); assert m
        block=m[2]
        for old,new in [('of October bills',r'of \CtwoSD{October bills}'),('of October interest',r'of \CtwoSD{October interest}'),('of delivery fees',r'of \CtwoSD{delivery fees}')]: block=block.replace(old,new)
        # Supply contextual meaning where only generic mean labels appeared.
        block=block.replace(r'\CtwoMean{population} \CtwoMean{mean}',r'\CtwoMean{population} '+means[i])
        if i==0:
            block=block.replace(r'\CtwoMean{mean} \CtwoMean{bill}',means[i]).replace('initially unknown mean at', 'initially unknown '+means[i]+' at')
        if i==1: block=block.replace(r'\CtwoMean{mean} \CtwoMean{October} \CtwoMean{interest}',means[i])
        block=block.replace(['Mean October electricity bill','Mean October interest credit','Mean delivery fee'][i],means[i])
        block=block.replace(['Initially unknown mean October electricity bill.','Initially unknown mean October interest credit.','Initially unknown mean delivery fee.'][i],'Initially unknown '+means[i]+'.')
        block=block.replace(['known spread of individual October electricity bill values.','known spread of individual October interest credit values.','known spread of individual delivery fee values.'][i],r'known \CtwoSD{population standard} \CtwoSD{deviation}, the '+spreads[i]+'.')
        block=block.replace('known individual-value spread.',r'known \CtwoSD{population standard} \CtwoSD{deviation}, the '+spreads[i]+'.')
        block=block.replace(['Fraction of all eligible businesses that used electronic invoicing in October','Fraction of all eligible accounts that had mobile banking activated on October 31','Fraction of all eligible deliveries that included optional parcel insurance'][i],props[i])
        block=block.replace('the same fixed mean, established by the population investigation.','the same fixed '+means[i]+', established by the population investigation; unavailable for initial estimation.')
        if task=='c2a':
            block=block.replace(r'\keytable{p{.12\linewidth}p{.19\linewidth}p{.18\linewidth}K}',r'\keytable{p{.12\linewidth}p{.24\linewidth}K}')
            block=block.replace(r'\textbf{Symbol}&\textbf{Concept}&\textbf{Type}&\textbf{Meaning in context}\\\midrule',r'\textbf{Symbol}&\textbf{Concept}&\textbf{Meaning in context}\\\midrule'+'\n'+r'\multicolumn{3}{l}{\textbf{Population parameters}}\\')
            block=block.replace('&Population parameters&','&').replace('&Sample statistics&','&').replace('&Procedure settings&','&')
            block=block.replace(r'$\CtwoPoint{\bar x}$&',r'\multicolumn{3}{l}{\textbf{Sample statistics}}\\'+'\n'+r'$\CtwoPoint{\bar x}$&')
            block=block.replace(r'$\CtwoConfidence{C}$&',r'\multicolumn{3}{l}{\textbf{Procedure settings}}\\'+'\n'+r'$\CtwoConfidence{C}$&')
            block=block.replace('spread of sample means.',r'spread of sample means, using known $\CtwoSD{\sigma}$ and the initial sample size $\CtwoSize{n}$.')
            # p is contextual C1 information, not an additional C2 table row.
            block=block.replace(r'\keytable{p{.12\linewidth}p{.24\linewidth}K}',r'The unknown $\PP{p}$ is the '+props[i]+'. Its denominator is all '+scopes[i]+'.\n\n'+r'\keytable{p{.12\linewidth}p{.24\linewidth}K}',1).replace('\\n\\n','\n\n')
        s=s[:m.start(2)]+block+s[m.end(2):]
# Add compact contextual definitions to the matching summary entries without changing their tables.
for i in range(3):
    needle=r'\par\textbf{\hyperref[sol:p'+str(i+1)+r'c1a]{C1 Task 1}}\par'
    start=s.index(needle); end=s.index(r'\secInicio',start)
    b=s[start:end]
    marker=r'\keytable{p{.29\linewidth}KK}'
    contextual=r'Here $\CtwoMean{\mu}$ is the '+means[i]+r'; $\CtwoSD{\sigma}$ is the \CtwoSD{population standard} \CtwoSD{deviation}, the '+spreads[i]+r'; and $\PP{p}$ is the '+props[i]+'.\n'
    b=b.replace(marker,contextual+marker,1)
    s=s[:start]+b+s[end:]
for i in range(3):
    start=s.index(r'\par\textbf{\hyperref[sol:p'+str(i+1)+r'c2a]'); end=s.index(r'\Needspace',start)
    b=s[start:end].replace('Initially unknown; the target of estimation.','Initially unknown '+means[i]+'; the target of estimation.')
    val=['60','36','8'][i]
    b=b.replace(r'$\CtwoSD{'+val+r'}$ thousand COP (known).',r'$\CtwoSD{'+val+r'}$ thousand COP (known); '+spreads[i]+'.')
    b=b.replace(r'the same fixed $\CtwoMean{\mu}$',r'the same fixed '+means[i]+r', $\CtwoMean{\mu}$')
    s=s[:start]+b+s[end:]
p.write_text(s,encoding='utf-8')
