from pathlib import Path
from fractions import Fraction as F
import re, hashlib, json

ROOT=Path.cwd()
BASE=ROOT/'book2026-2027/grade10/term_1/3-learning_evidences'
ref=BASE/'G10_T1_C1C2C3C4C5C6C7_exam_solution.tex'
out=BASE/'G10_T1_C1C2C3C4C5C6C7_examV2_solution.tex'
source=ref.read_text(encoding='utf-8')
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ref,ROOT/'book2026-2027/preamble/preamble_exams.tex']}
# Reuse formatting helpers only; never execute the original authoring script.
helpers=(ROOT/'tmp/build_g10_solution.py').read_text(encoding='utf-8')
exec(helpers[helpers.index('def table('):helpers.index('# Parse every')])
exec(helpers[helpers.index('def extrema('):helpers.index('course=r')])

titles=['Community Science Sessions','Kayak Rentals','Bicycle Assembly','Solar Installation','Equipment Leasing','Festival Meals','Laundry Capacity','Juice Production','Coffee Roasting','Farm Visitor Facilities','Translation Capacity','Mobile Game Release','Timber Supply Agreement']
slugs=[t.lower().replace(' ','-') for t in titles]
criteria=[[(1,3),(2,6)],[(1,3),(3,6)]]+[[(4,2)]]*3+[[(5,2)]]*3+[[(6,2)]]*3+[[(7,3)]]*2
data={
3:dict(names=['Large factory','Standard line','Compact line','Licensed production'],states=['Boom','Stable market','Recession'],values=[[132,53,-27],[91,63,19],[61,47,33],[26,26,26]],context='A bicycle manufacturer must select an assembly plan before market conditions are known. Licensed production earns a fixed royalty regardless of the market state.'),
4:dict(names=['Regional rollout','Town rollout','Village rollout','Service agreement'],states=['Rapid adoption','Moderate adoption','Slow adoption'],values=[[168,51,-39],[108,69,17],[73,52,31],[35,35,35]],context='A solar installer must select an installation programme before customer adoption is known. The service agreement pays a fixed profit under every adoption state.'),
5:dict(names=['Buy large fleet','Buy medium fleet','Lease small fleet','Pool equipment'],states=['Peak utilisation','Busy utilisation','Routine utilisation','Quiet utilisation'],values=[[156,81,21,-46],[113,85,41,11],[77,63,49,25],[54,51,39,32]],context='A construction-equipment business must choose a fleet plan before next season\'s rental utilisation is known.'),
6:dict(names=['Full menu','Balanced menu','Limited menu'],states=['Crowded','Average attendance','Sparse attendance'],values=[[87,37,-16],[65,54,21],[43,41,34]],context='A festival caterer must select a meal-preparation plan before attendance is known.'),
7:dict(names=['Build plant','Upgrade machines','Lease machines','Contract service'],states=['Heavy workload','Routine workload','Light workload'],values=[[126,47,-32],[94,73,19],[69,61,38],[41,41,41]],context='A commercial laundry must select its capacity plan before hotel orders are known. A contracted service provides a fixed profit under every workload state.'),
8:dict(names=['Large batch','Staged batches','Small batch'],states=['Exceptional sales','Brisk sales','Ordinary sales','Poor sales'],values=[[1080,610,230,-270],[810,730,510,150],[530,550,480,390]],context='A juice producer must choose its daily production plan before sales are known.'),
9:dict(names=['Specialty roast','Blended roast','Everyday roast'],states=['Export boom','Regular exports','Export slump'],values=[[98,49,-17],[74,63,27],[51,53,42]],context='A coffee roaster must choose a roasting plan before export conditions are known.'),
10:dict(names=['Visitor centre','Covered terrace','Picnic shelter','Lease to operator'],states=['Busy season','Typical season','Quiet season'],values=[[117,43,-29],[89,64,23],[63,57,40],[32,32,32]],context='A farm must select visitor facilities before seasonal attendance is known. Leasing to an operator earns a fixed profit under all attendance states.'),
11:dict(names=['Permanent staff','Staff plus freelancers','Core staff'],states=['Order rush','Busy orders','Routine orders','Few orders'],values=[[137,81,29,-43],[99,86,59,17],[65,67,61,48]],context='A translation agency must choose a capacity plan before client orders are known.'),
12:dict(names=['Wide release','Limited release'],states=['Viral uptake','Moderate uptake','Low uptake'],values=[[108,44,-10],[58,64,30]],context='A game developer must choose a wide release or a limited release before player uptake is known.'),
13:dict(names=['Spot sales','Reserved supply'],states=['Scarce timber','Balanced supply','Abundant timber'],values=[[30,66,94],[85,46,40]],context='A timber merchant must choose spot sales or a reserved-supply agreement before next season\'s timber availability is known.')}
probs={9:['0.35','0.40','0.25'],10:['0.25','0.45','0.30'],11:['0.15','0.35','0.25','0.25']}

def replace_all(text,mapping):
    return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m[0]],text)

sections=re.split(r'\\clearpage\s*\n(?=\\sectionScored)',source)
assert len(sections)==15
header=sections[0].replace('C1--C7 Catch-up Exam Solutions','C1--C7 Catch-up Exam Solutions -- Version 2')
header=header.replace('% Source: G10_T1_C1C2C3C4C5C6C7_exam.tex (questions and assessment rules).','% Version 2 worked-solutions exam, adapted from G10_T1_C1C2C3C4C5C6C7_exam_solution.tex.\n% New contexts and data; assessment rules and mathematical models retained.')

# Preserve the full first two worked-solution structures with new data and contexts.
maps1={'Craft Workshop':titles[0],'craft-workshop':slugs[0],'craft studio':'community science centre','Pottery':'Astronomy','pottery':'astronomy','Weaving':'Robotics','weaving':'robotics','workshop':'session','tourist demand':'family demand','Tourist demand':'Family demand','Strong':'Busy','strong':'busy','Weak':'Quiet','weak':'quiet',
'30(12+6)+80=540+80=620':'28(14+5)+90=532+90=622','18(12+2)+80=252+80=332':'17(14+3)+90=289+90=379','24(15+6)+50=504+50=554':'23(17+5)+65=506+65=571','16(15+2)+50=272+50=322':'14(17+3)+65=280+65=345',
'12 USD':'14 USD','80 USD':'90 USD','15 USD':'17 USD','50 USD':'65 USD','6 USD':'5 USD','2 USD':'3 USD','30 participants':'28 participants','18 with':'17 with','24 or 16':'23 or 14','620':'622','332':'379','554':'571','322':'345'}
p1=replace_all(sections[1],maps1)
p1=p1.replace('a astronomy session','an astronomy session').replace('the studio cannot control it','the centre cannot control it')
maps2={'Guided Cycling Tours':titles[1],'guided-cycling-tours':slugs[1],'tour operator':'kayak rental business','Town route':'Single kayaks','town route':'single kayaks','Countryside route':'Tandem kayaks','countryside route':'tandem kayaks','route':'rental type','places':'rentals','place':'rental','Strong':'Busy','strong':'busy','Weak':'Quiet','weak':'quiet',
'90(32+8)-90(18)-500=3600-1620-500=1480':'84(36+7)-84(20)-540=3612-1680-540=1392',
'60(32+3)-60(18)-650=2100-1080-650=370':'56(36+4)-56(20)-620=2240-1120-620=500',
'70(45+8)-70(26)-500=3710-1820-500=1390':'66(49+7)-66(29)-540=3696-1914-540=1242',
'40(45+3)-40(26)-650=1920-1040-650=230':'38(49+4)-38(29)-620=2014-1102-620=292',
'90 rentals':'84 rentals','90 places':'84 rentals','60 with':'56 with','70 or 40':'66 or 38','32 USD':'36 USD','45 USD':'49 USD','8 USD':'7 USD','3 USD':'4 USD','18 USD':'20 USD','26 USD':'29 USD','500 USD':'540 USD','650 USD':'620 USD','1480':'1392','370':'500','1390':'1242','230':'292','1,480':'1,392'}
p2=replace_all(sections[2],maps2)
# Correct grammar after substituting plural alternatives.
p2=p2.replace('a single kayaks or a tandem kayaks','single kayaks or tandem kayaks').replace('The single kayaks sells','Single kayaks sell').replace('the tandem kayaks sells','tandem kayaks sell').replace('the single kayaks earns','single kayaks earn')
p2=p2.replace('Single kayaks sell 84 rentals','Single kayaks generate 84 rentals').replace('tandem kayaks sell 66 or 38','tandem kayaks generate 66 or 38').replace('$q_{ij}$ is rentals sold','$q_{ij}$ is the number of rentals sold')

def sensitivity(n):
    d=data[n]; v=d['values']; a,b=(F(1),F(1,2)) if n==12 else (F(2),F(1))
    limit=1/(a+b); slopes=[a*r[0]+b*r[1]-(a+b)*r[2] for r in v]; ints=[F(r[2]) for r in v]
    t=(ints[1]-ints[0])/(slopes[0]-slopes[1]); tie=ints[0]+slopes[0]*t
    assert 0<t<limit
    def tex(x):
        x=F(x)
        return str(x.numerator) if x.denominator==1 else r'\frac{'+str(x.numerator)+'}{'+str(x.denominator)+'}'
    prob=r'\left(p,\frac p2,1-\frac{3p}{2}\right)' if n==12 else '(2p,p,1-3p)'
    dom=r'0\le p\le1,\quad 0\le p/2\le1\iff0\le p\le2,\quad 0\le1-3p/2\le1\iff0\le p\le\frac23' if n==12 else r'0\le2p\le1\iff0\le p\le\frac12,\quad 0\le p\le1,\quad 0\le1-3p\le1\iff0\le p\le\frac13'
    res='The mutually exclusive and exhaustive state probabilities sum to one:\n'+r'\[P(S_3)=1-'+('p-p/2=1-3p/2' if n==12 else '2p-p=1-3p')+r',\qquad\boldsymbol{q}='+prob+r'.\]'+'\nEvery probability must lie in $[0,1]$:\n'+r'\['+dom+r'.\]'+'\nTheir intersection is '+r'$\boxed{0\le p\le '+tex(limit)+r'}$.'+'\nThe remaining part of $[0,1]$, '+r'$'+tex(limit)+r'<p\le1$' +', is infeasible because $P(S_3)<0$. No decision is valid there.\n'
    if n==13: res+=r'For $p>\frac12$, $P(S_1)>1$ as well.'+'\n'
    res+='Expected profits are in thousand USD:\n'+r'\begin{align*}'+'\n'
    for i,(r,s,c) in enumerate(zip(v,slopes,ints),1):
        terms=[str(r[0])+('p' if n==12 else '(2p)'),str(r[1])+('(p/2)' if n==12 else 'p'),str(r[2])+('(1-3p/2)' if n==12 else '(1-3p)')]
        res+=f'E_{i}&=EMV(A_{i})='+('+'.join(terms)).replace('+-','-')+r'\\&='+tex(a*r[0])+'p+'+tex(b*r[1])+'p'+('+' if c>=0 else '')+tex(c)+('+' if -(a+b)*c>=0 else '')+tex(-(a+b)*c)+'p='+tex(c)+('+' if s>=0 else '')+tex(s)+'p'+(r',\\' if i==1 else '.')+'\n'
    res+=r'\end{align*}'+'\nEquating the two linear EMVs gives\n'+r'\[E_1=E_2\iff '+tex(slopes[0]-slopes[1])+'p='+tex(ints[1]-ints[0])+r'\iff\boxed{p='+tex(t)+r'}.\]'+'\n'
    res+=r'This is the only threshold, since the slopes differ, and $0<'+tex(t)+'<'+tex(limit)+r'$. At the tie, $E_1=E_2='+tex(tie)+r'$ thousand USD.'+'\n'
    res+=r'The difference $E_1-E_2='+tex(ints[0]-ints[1])+('+' if slopes[0]-slopes[1]>=0 else '')+tex(slopes[0]-slopes[1])+r'p$ is '+('negative below the threshold and positive above it.' if n==12 else 'positive below the threshold and negative above it.')+'\n'
    res+=r'At $p=0$, $(E_1,E_2)=('+','.join(tex(c) for c in ints)+r')$; at $p='+tex(limit)+r'$, $(E_1,E_2)=('+','.join(tex(c+s*limit) for c,s in zip(ints,slopes))+r')$.'+'\nBoth feasible endpoints agree with the rule:\n'
    low,high=(1,0) if n==12 else (0,1)
    res+=r'\[\boxed{\begin{cases}'+'\n'+r'\text{'+d['names'][low]+r' }(A_'+str(low+1)+r'),&0\le p<'+tex(t)+r',\\'+'\n'+r'\text{Both alternatives tied},&p='+tex(t)+r',\\'+'\n'+r'\text{'+d['names'][high]+r' }(A_'+str(high+1)+r'),&'+tex(t)+r'<p\le'+tex(limit)+r'.'+'\n'+r'\end{cases}}\]'+'\nEither alternative is optimal at the tie. Expected profit is not guaranteed profit.\n'
    return res

doc=header+'\\clearpage\n'+p1+'\\clearpage\n'+p2
summaries=[]
for n in range(3,14):
    d=data[n]; slug=slugs[n-1]; c,pts=criteria[n-1][0]
    unit='USD' if n==8 else 'thousand USD'
    doc+='\n\\clearpage\n'+f'\\sectionScored{{{titles[n-1]}}}{{C{c}-\\sml{{{pts}}}}}{{sec:{slug}}}\n'
    doc+=d['context']+' The possible states, in column order, are '+', '.join(d['states'])+f'. Profits are in {unit}.'+(' No probabilities are available.' if n<=8 else '')+'\n'
    rows=[]
    if n in probs: rows.append(['$P(S_j)$']+probs[n])
    rows += [[f'{name} ($A_{i}$)']+v for i,(name,v) in enumerate(zip(d['names'],d['values']),1)]
    doc+=table(['Alternative']+[f'$S_{j+1}$' for j in range(len(d['states']))],rows)
    if n>=12: doc+=r'Suppose $P(S_1)='+('p$ and $P(S_2)=p/2$' if n==12 else '2p$ and $P(S_2)=p$')+'; determine $P(S_3)$ from the sum-to-one condition.\n'
    question={4:'What would the optimistic decision be? What would the conservative decision be? Justify your answer.',5:'What decision would be selected using the Minimax Regret criterion? Justify your answer.',6:'What decision would be selected using the EMV or Bayes criterion? Justify your answer.',7:r'State the preferred alternative for every probability value ($0\le p\le1$).'}[c]
    doc+=f'\\QuestionsTasks[sec:{slug}]{{\n{{{c}}}/{{sol:{slug}-c{c}}}/{{{question} \\score{{{pts}}}}}\n}}\n'
    doc+=solhead(slug,c,pts,{4:'Maximax and Maximin',5:'Minimax Regret',6:'EMV / Bayes',7:'Probability sensitivity analysis'}[c])+enumtext(d['names'],d['states'])
    if c==4:
        full='All profits are in thousand USD. Find the largest and smallest payoff in every row:\n'+extrema(n)
        full+='Maximax focuses on the best possible profit and ignores the downside. Maximin protects the best worst-case profit and may forgo a large gain. Without probabilities, neither criterion estimates likelihoods or expected profit.\n'
        short=extrema(n,True)
    elif c==5: full=regret(n); short=regret(n,True)
    elif c==6: full=emv(n); short=emv(n,True)+'Expected profit is not guaranteed profit.\n'
    else: full=sensitivity(n); short=full
    doc+=full+nav(slug)
    summaries.append(enumtext(d['names'],d['states'])+short+nav(slug))

doc+='\n\\clearpage\n'+sections[14].split('\\subsection{',1)[0]
old_summaries=re.split(r'(?=\\subsection\{)',sections[14])[1:]
# Keep concise, fully recalculated first-model summaries in the inherited format.
s1=replace_all(old_summaries[0],maps1).replace('$30(12+6)+80=622$','$28(14+5)+90=622$').replace('$18(12+2)+80=379$','$17(14+3)+90=379$').replace('$24(15+6)+50=571$','$23(17+5)+65=571$').replace('$16(15+2)+50=345$','$14(17+3)+65=345$')
s2=replace_all(old_summaries[1],maps2)
for old,new in [('90(32+8)-90(18)-500=1392','84(36+7)-84(20)-540=1392'),('60(32+3)-60(18)-650=500','56(36+4)-56(20)-620=500'),('70(45+8)-70(26)-500=1242','66(49+7)-66(29)-540=1242'),('40(45+3)-40(26)-650=292','38(49+4)-38(29)-620=292')]: s2=s2.replace(old,new)
s2=s2.replace('Town ($A_1$)','Single ($A_1$)').replace('Countryside ($A_2$)','Tandem ($A_2$)').replace('The single kayaks earns','Single kayaks earn')
doc+=s1+s2
for n,summary in enumerate(summaries,3):
    if n in [3,6,8,9,12,13]: doc+='\\clearpage\n'
    c,pts=criteria[n-1][0]
    doc+=f'\\subsection{{{titles[n-1]} \\hfill C{c}--{pts}}}\n\\label{{summary:{slugs[n-1]}}}\n'+summary
doc+='}\n\\end{document}\n'
# The inherited navigation helper has negative top spacing and an opaque box.
# Reserve space locally so it cannot cover the preceding conclusion.
doc=doc.replace('\n\\secInicio[','\n\\par\\vspace{4mm}\n\\secInicio[')
doc=doc.replace('{\\small\nThe numbered summaries','{\\small\\setlength{\\parskip}{2pt}\nThe numbered summaries')
assert [sum(v for cs in criteria for k,v in cs if k==i) for i in range(1,8)]==[6]*7
assert len(re.findall(r'\\sectionScored\{',doc))==14
out.write_text(doc,encoding='utf-8')
for p,h in hashes.items(): assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
print(out)
