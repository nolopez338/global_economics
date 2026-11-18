from pathlib import Path
from decimal import Decimal as D

root = Path.cwd()
target = root/'book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C2_classroom_activity.tex'
original = (root/'tmp/c2-solutions/original.tex').read_text(encoding='utf-8')
reference = (root/'book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex').read_text(encoding='utf-8')
imports = r'''
% Highlight infrastructure is used only by the appended solutions.
\input{graphs/highlights.tex}
% \GTenHighlightsfalse % Uncomment to disable instructional highlights.
\input{graphs/specific_highlights.tex}
\newcommand{\CtwoSignificance}[1]{\CtwoConfidence{#1}}
\definecolor{CtwoErrorColor}{HTML}{28AFA2}
\newcommand{\CtwoError}[1]{\HighlightStroke{CtwoErrorColor}{#1}}
\newcommand{\CtwoCI}[1]{\CtwoEndpoint{#1}}
\newcommand{\CtwoCoverCount}{\CtwoCoverage{N_{\rm cover}}}
\newcommand{\CtwoTotalCount}{\CtwoCoverage{N}}
'''
def helper(name, new):
    start = reference.index('\\newcommand{\\'+name+'}')
    end = reference.index('\n}\n', start)+3
    return reference[start:end].replace('\\'+name, '\\'+new)

helpers = helper('InformationTable','SolutionInformationTable') + '\n' + helper('TaskTwoTable','SolutionTaskTwoTable')
def h(role, text): return '\\Ctwo'+role+'{'+str(text)+'}'
def m(role,text): return '$'+h(role,text)+'$'
def num(v): return format(D(v).normalize(),'f')
def row(*cells): return ' & '.join(cells)+r' \\[6pt]'+'\n'
def math(s): return '$'+s+'$'
levels = {'90':('0.90','0.10','0.05','1.645'), '95':('0.95','0.05','0.025','1.960'), '99':('0.99','0.01','0.005','2.576')}
problems = [
 (2,'Two reports on weekly printing costs','district mean weekly printing cost for all school offices in the specified week','offices','thousand COP','88','32','86','100','3.2',['90','99']),
 (3,'Repeated estimates of locker rental charges','mean weekly locker rental charge for all sports-centre customers in the specified week','customers','thousand COP','70','20','72','64','2.5',['95']),
 (4,'Two reports on monthly pet-care spending','district mean monthly pet-care spending for all registered households in the specified month','households','thousand COP','148','42','145','144','3.5',['90','99']),
 (5,'Studies of clinic waiting times','mean waiting time for all clinic appointments in the specified month','appointments','minutes','27','14','26','49','2',['90']),
 (6,'Three confidence levels for library processing times','mean processing time for all books returned to the library in the specified month','books','minutes','25','15','24','100','1.5',['90','95','99']),
]
out = [r'''
% Appended review only: the original classroom body above is preserved verbatim.
\clearpage
\newgeometry{margin=0.65in,top=0.55in,bottom=0.65in}
\begingroup
\linespread{1.12}\selectfont
\setlength{\parskip}{4pt}
\CtwoPracticeIntervalPalette
\section*{Solutions}
Solutions to problems 2--6. Problem 1 already has its worked solution in the activity.
The highlighted names, symbols, substitutions, and results use the practice document's semantic roles.
In every problem, $\CtwoMean{\mu_{\mathrm{known}}}$ is the later established value of the same fixed population mean $\CtwoMean{\mu}$.
''']
for idx,p in enumerate(problems):
    k,title,context,objects,unit,known,sd,x,n,se,cs = p
    if idx: out.append(r'\clearpage'+'\n')
    out.append('\\subsection*{'+str(k)+'. '+title+'}\n\\subsubsection*{Task 1 solution. Organize the information and calculate SE}\n')
    out.append('\\SolutionInformationTable{\n')
    out.append(row(m('Mean',r'\mu'),h('Mean','Population mean'),'Population parameters','The '+context+', in '+unit+'; fixed and initially unknown.'))
    out.append(row(m('Mean',r'\mu_{\mathrm{known}}'),h('Mean','Later established')+' '+h('Mean','population mean'),'',m('Mean',known)+' '+unit+'; established by the later comprehensive population investigation.'))
    out.append(row(m('SD',r'\sigma'),h('SD','Population')+' '+h('SD','standard deviation'),'',m('SD',sd)+' '+unit+'; known spread of individual observations.'))
    out.append('\\midrule\n')
    out.append(row(m('Point',r'\bar{x}'),h('Point','Sample mean'),'Sample statistics',m('Point',x)+' '+unit+'; the initial point estimate of '+m('Mean',r'\mu')+'.'))
    out.append(row(m('Size','n'),h('Size','Sample size'),'',m('Size',n)+' '+objects+' in the initial sample and each subsequent study.'))
    out.append(row(m('SE',r'\mathrm{SE}'),h('SE','Standard error'),'',math(h('SE',r'\mathrm{SE}')+'='+h('SD',r'\sigma')+r'/\sqrt{'+h('Size','n')+'}')+r'\par'+math('='+h('SD',sd)+r'/\sqrt{'+h('Size',n)+'}='+h('SE',se))+' '+unit+'. Spread of means across repeated independent samples of '+n+' '+objects+'.'))
    out.append('\\midrule\n')
    settings = [ ('Confidence','C','Confidence level',0),('Significance',r'\alpha','Significance level',1),('Significance',r'\alpha/2','Tail area',2),('Critical','z^*','Critical value',3)]
    for j,(role,sym,label,col) in enumerate(settings):
        vals=[]
        for c in cs:
            vals.append(m('Confidence',c+r'\%')+': '+math(h(role,sym)+'='+('1-'+h('Confidence',levels[c][0])+'=' if col==1 else h('Significance',levels[c][1])+'/2=' if col==2 else '')+h(role,levels[c][col])))
        out.append(row(m(role,sym), ' '.join(h(role,w) for w in label.split()), 'Procedure Settings' if j==0 else '',r'\par '.join(vals)+'.'))
    out.append('}\n')
    out.append('The observations are independent and random, '+m('SD',r'\sigma')+' is known, and the sample mean is normally distributed under the stated model. No sample SD is required.\n')
    for ci,c in enumerate(cs):
        z=levels[c][3]; moe=num(D(z)*D(se)); lo=num(D(x)-D(moe)); up=num(D(x)+D(moe)); width=num(2*D(moe))
        out.append('\\clearpage\n\\subsubsection*{Task 2 solution'+(' (continued)' if ci else '')+'. Calculate MoE and state the interval}\n')
        out.append('\\textbf{'+m('Confidence',c+r'\%')+' confidence}\n\\SolutionTaskTwoTable{\n')
        if ci==0:
            out.append(row(m('Point',r'\bar{x}'),h('Point','Point estimate'),math(h('Point',r'\bar{x}')+r'=\sum x_i/'+h('Size','n'))+r'\par Given sample mean',m('Point',x)+r'\par '+unit,'Estimates the population mean.'))
            out.append('\\midrule\n')
        else:
            out.append('\\multicolumn{5}{@{}l}{Shared '+h('Point','point estimate')+': '+m('Point',r'\bar{x}')+'='+m('Point',x)+' '+unit+r'.}\\[6pt]'+'\n\\midrule\n')
        out.append(row(m('MoE',r'\mathrm{MoE}'),h('MoE','Margin of error'),math(h('MoE',r'\mathrm{MoE}')+'='+h('Critical','z^*')+r'\times'+h('SE',r'\mathrm{SE}'))+r'\par'+math('='+h('Critical',z)+r'\times'+h('SE',se)),m('MoE',moe)+r'\par '+unit,'Distance from centre to either bound.'))
        for sym,sign,val,word in [('L','-',lo,'Lower'),('U','+',up,'Upper')]:
            out.append(row(m('Endpoint',sym),h('Endpoint',word)+' '+h('Endpoint','endpoint'),math(h('Endpoint',sym)+'='+h('Point',r'\bar{x}')+sign+h('MoE',r'\mathrm{MoE}'))+r'\par'+math('='+h('Point',x)+sign+h('MoE',moe)),m('Endpoint',val)+r'\par '+unit,word+' bound for the population mean.'))
        out.append(row(m('CI',r'\mathrm{CI}'),h('CI','Confidence')+' '+h('CI','interval'),math(h('CI',r'\mathrm{CI}')+'=['+h('Endpoint','L')+','+h('Endpoint','U')+']')+r'\par'+math('=['+h('Point',x)+'-'+h('MoE',moe)+',')+r'\par'+math(h('Point',x)+'+'+h('MoE',moe)+']'),math('['+h('Endpoint',lo)+',')+r'\par'+math(h('Endpoint',up)+']')+r'\par '+unit,'Plausible values for the population mean under the model.'))
        out.append(row(m('Width','W'),h('Width','Full width'),math(h('Width','W')+'='+h('Endpoint','U')+'-'+h('Endpoint','L'))+r'\par'+math('='+h('Endpoint',up)+'-'+h('Endpoint',lo))+r'\par'+math('=2'+h('MoE',r'\mathrm{MoE}')+'=2('+h('MoE',moe)+')'),m('Width',width)+r'\par '+unit,'Total span; smaller width means greater precision.'))
        out.append('}\n')
        out.append('We are '+h('Confidence',c+r'\%')+' confident that the '+context+' lies between '+m('Endpoint',lo)+' and '+m('Endpoint',up)+' '+unit+'. Under the model, '+h('Confidence',c+r'\%')+' of intervals constructed by this procedure would cover the fixed '+m('Mean',r'\mu')+' in the long run. This is not a probability assigned to the fixed mean after calculating this interval.\n')
    out.append('\\clearpage\n\\subsubsection*{Task 3 solution. Calculate coverage, absolute error, and interpret confidence}\n')
    out.append('For these subsequent studies, an interval covers exactly when '+math(h('Endpoint','L_i')+r'\leq'+h('Mean',r'\mu_{\mathrm{known}}')+r'\leq'+h('Endpoint','U_i'))+', including equality. The later established mean is '+m('Mean',known)+' '+unit+'. Each interval is centred on its own study sample mean.\n')
    if k==3:
        out.append('Studies 1, 2, 4, and 5 cover: '+math(h('Endpoint','64.1')+r'\leq'+h('Mean','70')+r'\leq'+h('Endpoint','73.9'))+', '+math(h('Endpoint','67.1')+r'\leq'+h('Mean','70')+r'\leq'+h('Endpoint','76.9'))+', '+math(h('Endpoint','63.1')+r'\leq'+h('Mean','70')+r'\leq'+h('Endpoint','72.9'))+', and '+math(h('Endpoint','65.1')+r'\leq'+h('Mean','70')+r'\leq'+h('Endpoint','74.9'))+'. Study 3 misses because its '+h('Endpoint','lower endpoint')+' '+m('Endpoint','70.1')+' exceeds '+m('Mean','70')+'.\n')
    if k==5:
        out.append('The counts by study-order block are '+m('Coverage','4,5,4,3')+'. Add them cumulatively to assess how observed coverage changes as studies are added.\n')
    if k==6:
        out.append('The mutually exclusive categories total '+math(h('Coverage','219')+'+'+h('Coverage','18')+'+'+h('Coverage','10')+'+'+h('Coverage','3')+'='+h('Coverage','250'))+'. Sum the relevant categories for each level; the denominator is '+m('Coverage','250')+' studies at each level.\n')
    entries = {2:[('90','200-23',177,200),('99','200-5',195,200)],3:[('95','4',4,5)],4:[('90','150-17',133,150),('99','150-3',147,150)],5:[('90','4',4,5),('90','4+5',9,10),('90','4+5+4',13,15),('90','4+5+4+3',16,20)],6:[('90','219',219,250),('95','219+18',237,250),('99','219+18+10',247,250)]}[k]
    for c,calc,count,total in entries:
        cov=D(count)/D(total)*100; err=abs(cov-D(c)); exact=(100*count)%total==0
        cv=num(cov) if exact else f'{cov:.2f}'; ev=num(err) if exact else f'{err:.2f}'
        out.append('\\Needspace{10\\baselineskip}\n\\textbf{'+m('Confidence',c+r'\%')+' confidence'+(' -- first '+str(total)+' studies' if k==5 else '')+'}\n')
        out.append('\\begin{align*}\n'+r'\CtwoCoverCount('+h('Confidence',c+r'\%')+')&='+'+'.join(h('Coverage',v) for v in calc.split('+'))+'='+h('Coverage',count)+r',\qquad \CtwoTotalCount('+h('Confidence',c+r'\%')+')='+h('Coverage',total)+r';\\'+'\n')
        # Minus in count calculations remains an operator outside wrappers.
        out[-1]=out[-1].replace(h('Coverage',calc), '-'.join(h('Coverage',v) for v in calc.split('-'))) if '-' in calc else out[-1]
        out.append(h('Coverage',r'\mathrm{Cov}')+'('+h('Confidence',c+r'\%')+')&='+r'\frac{'+h('Coverage',count)+'}{'+h('Coverage',total)+r'}\times100\%'+('=' if exact else r'\approx')+h('Coverage',cv+r'\%')+r';\\'+'\n')
        out.append(h('Error',r'E_{\rm abs}')+'('+h('Confidence',c+r'\%')+')&='+r'\left|'+(h('Coverage',cv) if exact else r'\frac{'+h('Coverage',100*count)+'}{'+h('Coverage',total)+'}')+'-'+h('Confidence',c)+r'\right|'+('=' if exact else r'\approx')+h('Error',ev)+r'\ \text{percentage points}.'+'\n\\end{align*}\n')
        direction = 'below' if cov<D(c) else 'above' if cov>D(c) else 'equal to'
        out.append('Here '+m('Coverage',count)+' of '+m('Coverage',total)+' subsequent intervals cover the '+context+': observed coverage is '+direction+' nominal '+h('Confidence',c+r'\%')+' confidence'+('.\n' if direction=='equal to' else ' by '+h('Error',ev)+' '+h('Error','percentage points')+'.\n'))
    if k==5:
        out.append('The cumulative rates are '+m('Coverage',r'80\%,90\%,86.67\%,80\%')+' (the third is rounded); absolute errors are '+m('Error','10,0,3.33,10')+' '+h('Error','percentage points')+'. Thus the rate first reaches nominal confidence and then moves away. The final covering count is '+math(h('Coverage','4')+'+'+h('Coverage','5')+'+'+h('Coverage','4')+'+'+h('Coverage','3')+'='+h('Coverage','16'))+' out of '+m('Coverage','20')+'. More studies do not guarantee monotonic convergence.\n')
    if len(cs)>1:
        out.append('For each study the intervals share its sample mean and '+h('SE','SE')+'. Increasing '+h('Confidence','confidence')+' increases '+m('Critical','z^*')+', '+h('MoE','MoE')+', and '+h('Width','full width')+'. The narrower interval lies inside each wider partner, so covering counts cannot decrease with confidence on these same studies. '+('The categories respect nesting: a study in ``all three'' counts at every level; ``only 95\\% and 99\\%'' counts at those two levels; ``only 99\\%'' counts once at 99\\%; ``none'' counts at no level. ' if k==6 else '')+'\n')
    out.append('These are retrospective studies of the same fixed population and target period. Finite-run '+h('Coverage','observed coverage')+' need not equal '+h('Confidence','nominal confidence')+' or approach it monotonically as studies are added. Under the model, confidence describes long-run coverage of the sampling procedure, including the one used for the initial report. Each realized interval either covers or misses the fixed mean; coverage is not the fraction of individual observations inside the initial interval. A smaller finite-run '+h('Error','absolute error')+' does not establish superior long-run performance.\n')
out.append('\\par\\clearpage\n\\endgroup\n\\restoregeometry\n')
updated = original.replace('\\usepackage{needspace}',imports+'\n'+helpers+'\n\\usepackage{needspace}',1).replace('\\end{document}', ''.join(out)+'\\end{document}')
target.write_text(updated,encoding='utf-8')
print('Appended solutions for problems 2--6.')
