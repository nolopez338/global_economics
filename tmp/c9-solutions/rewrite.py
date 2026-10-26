from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import re, json

root = Path.cwd()
p = root / 'book2026-2027/grade11/term_1/2-class_activities/G11_T1_C9_classroom_activity.tex'
backup = Path('tmp/c9-solutions/original.tex')
original = backup.read_bytes() if backup.exists() else p.read_bytes()
marker = b'\\textbf{\\large Solutions}'
prefix = original[:original.index(marker)]
Path('tmp/c9-solutions/original.tex').write_bytes(original)
D = lambda x: Decimal(str(x))
def fixed(x, places=2):
    return f'{D(x).quantize(D(10)**-places, rounding=ROUND_HALF_UP):.{places}f}'
def num(x):
    return format(D(x).normalize(), 'f')
def math(s): return '\\[\n'+s+'\n\\]\n'
def step(n, title, s):
    block=f'\\par\\textbf{{Step {n}: {title}.}}\\nopagebreak\\enspace '+s+'\n'
    if n in (2,3) or title=='Interpretation' or title=='Back-transform to contextual units':
        block='\\par\\noindent\\begin{minipage}{\\linewidth}\n'+block+'\\end{minipage}\\par\n'
    return block
audit=[]
def errors(t,n,unit='',prob=False,label=''):
    t,n=D(t),D(n); e=abs(t-n); places=4 if prob else 2
    unittex=rf'\ \text{{{unit}}}' if unit else ''
    a,b=(fixed(t,4),fixed(n,4)) if prob else (num(t),num(n))
    es=fixed(e,4) if prob else num(e)
    audit.append(dict(label=label,t=str(t),normal=str(n),EA=fixed(e,places),EPt=fixed(100*e/abs(t)),EPn=fixed(100*e/abs(n))))
    return '\\par\\noindent\\begin{minipage}{\\linewidth}\n'+(('\\par\\textit{'+label+' comparison.}\n') if label else '')+math(r'E_A=|r_T-r_N|,\qquad E_{Pt}=\frac{100E_A}{|r_T|},\qquad E_{Pn}=\frac{100E_A}{|r_N|}.')+(
        'Here $r_T$ and $r_N$ are the '+('displayed probabilities' if prob else 'unrounded contextual cutoffs')+' being compared.\n')+math(
        rf'\begin{{aligned}}'+'\n'+
        rf'E_A&=|{a}-({b})|={es}'+(rf'\approx {fixed(e,places)}' if not prob and D(fixed(e,places))!=e else '')+unittex+r',\\'+'\n'+
        rf'E_{{Pt}}&=\frac{{100|{a}-({b})|}}{{|{a}|}}=\frac{{100({es})}}{{{num(abs(t)) if not prob else fixed(abs(t),4)}}}\approx {fixed(100*e/abs(t))}\%,\\'+'\n'+
        rf'E_{{Pn}}&=\frac{{100|{a}-({b})|}}{{|{b}|}}=\frac{{100({es})}}{{{num(abs(n)) if not prob else fixed(abs(n),4)}}}\approx {fixed(100*e/abs(n))}\%.'+'\n'+r'\end{aligned}')+'\\end{minipage}\\par\n'

intro=r'''\textbf{\large Solutions}\\
Use the supplied approximation $X_T=m+aT$, $T\sim t_\nu$, and $X_N=m+aZ$, with $\nu=n-1$: the stated $a$ is used directly as the scale. Write $F_\nu(c)=P(T<c)$ and $\Phi(c)=P(Z<c)$. Since both models are continuous, including or excluding an endpoint does not change a probability.

Read positive $t$ critical values to three decimals from the row for $\nu$ and right-tail column $\alpha$: the entry $t^*$ means $P(T>t^*)=\alpha$. These printed critical values approximate the underlying distribution. In the calculations below, the associated table probabilities are used as the working values. Equalities in subsequent arithmetic are exact for those selected table values; the resulting model probabilities and cutoffs remain approximations.

For direct normal calculations, first round each standardized boundary to two decimals, then read the CDF to four decimals. For inverse normal calculations, choose the closest printed CDF entry. At cumulative targets $0.0500$ and $0.9500$, the printed entries at magnitudes $1.64$ and $1.65$ are equally close: consistently choose $|z|=1.64$. Thus $\Phi(1.64)=0.9495$ is used for a $0.9500$ target, and $\Phi(-1.64)=1-0.9495=0.0505$ for a $0.0500$ target.

Comparison errors measure differences between the two model results, not errors against observed truth. Use displayed table probabilities for direct errors and unrounded back-transformed cutoffs for inverse errors. Keep absolute values in percentage denominators; a zero denominator would make that percentage undefined. Report probabilities and their absolute differences to four decimals, contextual cutoffs and their absolute differences to two decimals with units, and percentage errors to two decimals.
\begingroup
\begin{enumerate}[leftmargin=*,label=\textbf{\arabic*.},itemsep=12pt,parsep=3pt,topsep=5pt]
'''
out=[intro]
def direct(title, n,m,a,event,meaning,std,twork,nwork,t,norm,interpret):
    out.append(rf'\item \begin{{minipage}}[t]{{\linewidth}}\textbf{{{title} ($\nu={n-1}$).}}\nopagebreak'+'\n')
    out.append(step(1,'Information and event',rf'$n={n}$, $m={m}$, $a={a}$, so $\nu=n-1={n}-1={n-1}$. '+meaning+math(event))+'\\end{minipage}\\par\n')
    out.append(step(2,'Standardize',math(r'c=\frac{x-m}{a}.')+'Subtract the model location and divide by its positive scale; this preserves the direction of the inequalities.\n'+math(std)))
    out.append(step(3,"Student's $t$ probability",twork))
    out.append(step(4,'Normal probability',nwork))
    out.append(step(5,'Comparison errors',errors(t,norm,prob=True,label=title)))
    out.append(step(6,'Interpretation',interpret))

direct('Bus arrivals',7,2,6,r'P(X<-9.658).',
    'The quantity is arrival-time deviation in minutes. A negative deviation means early arrival; the event is a left tail.',
    r'c=\frac{-9.658-2}{6}=\frac{-11.658}{6}=-1.943.',
    'In row $6$, column $\\alpha=0.05$, the entry is $t^*=1.943$:\n'+math(r'P(T>1.943)\approx0.0500.')+'Symmetry gives the same area to the left of the negative critical value:\n'+math(r'p_T=P(T<-1.943)=P(T>1.943)\approx\boxed{0.0500}.'),
    'Round the standardized boundary: $-1.943\\to z=-1.94$. The table gives $\\Phi(1.94)=0.9738$. Use symmetry to find the negative cumulative area:\n'+math(r'\Phi(-z)=1-\Phi(z).')+math(r'p_N=\Phi(-1.94)=1-\Phi(1.94)=1-0.9738=\boxed{0.0262}.'),
    '.05','.0262',
    'The threshold means arriving more than $9.658$ minutes early (about $9.66$ minutes). The $t$ model assigns about $5.00\\%$ to this event, and the normal model about $2.62\\%$. The normal probability is lower by $0.0238$, or $2.38$ percentage points.')

direct('Shipping costs',16,-15,40,r'P(X>-49.64).',
    'Cost deviation is in thousand USD. The negative threshold is $49.64$ thousand USD below budget. We need the area to its right, including less negative and positive deviations.',
    r'c=\frac{-49.64-(-15)}{40}=\frac{-49.64+15}{40}=\frac{-34.64}{40}=-0.866.',
    'Row $15$, column $\\alpha=0.20$, gives $t^*=0.866$:\n'+math(r'P(T>0.866)\approx0.2000.')+'Symmetry transfers this to the left tail; taking its complement gives the requested right tail:\n'+math(r'\begin{aligned}P(T<-0.866)&=P(T>0.866)\approx0.2000,\\p_T=P(T>-0.866)&=1-P(T<-0.866)\\&\approx1-0.2000=\boxed{0.8000}.\end{aligned}'),
    'Round $-0.866\\to z=-0.87$. The table gives $\\Phi(0.87)=0.8078$. First use symmetry, then the right-tail complement:\n'+math(r'\Phi(-z)=1-\Phi(z),\qquad P(Z>z)=1-\Phi(z).')+math(r'\begin{aligned}\Phi(-0.87)&=1-0.8078=0.1922,\\p_N=P(Z>-0.87)&=1-\Phi(-0.87)\\&=1-0.1922=\boxed{0.8078}.\end{aligned}'),
    '.8','.8078',
    'The chance of a cost deviation exceeding $-49.64$ thousand USD is about $80.00\\%$ under $t$ and $80.78\\%$ under normal. Both exceed $0.5$ because $-49.64<-15=m$: each model is symmetric about $-15$, so the area to the right of a threshold below that centre includes the right half plus some of the left half. The normal probability is higher by $0.0078$, or $0.78$ percentage points.')

direct('Water demand',20,10,20,r'P(27.22<X<44.58).',
    'Water-use deviation is in cubic metres. Both positive bounds mean use above forecast, and both bounds are above the model location $10$.',
    r'\begin{aligned}c_L&=\frac{27.22-10}{20}=\frac{17.22}{20}=0.861,\\c_U&=\frac{44.58-10}{20}=\frac{34.58}{20}=1.729.\end{aligned}',
    'Row $19$ gives $t^*=0.861$ in column $\\alpha=0.20$, and $t^*=1.729$ in column $\\alpha=0.05$. Thus\n'+math(r'P(T>0.861)\approx0.2000,\qquad P(T>1.729)\approx0.0500.')+'Each left cumulative area is one minus its right tail. Subtracting the lower cumulative area removes values below the interval:\n'+math(r'P(c_L<T<c_U)=F_\nu(c_U)-F_\nu(c_L).')+math(r'\begin{aligned}F_{19}(0.861)&\approx1-0.2000=0.8000,\\F_{19}(1.729)&\approx1-0.0500=0.9500,\\p_T&\approx0.9500-0.8000=\boxed{0.1500}.\end{aligned}'),
    'Round each boundary separately: $0.861\\to z_L=0.86$ and $1.729\\to z_U=1.73$. The CDF entries are $\\Phi(0.86)=0.8051$ and $\\Phi(1.73)=0.9582$. Subtract cumulative areas:\n'+math(r'P(z_L<Z<z_U)=\Phi(z_U)-\Phi(z_L).')+math(r'p_N=\Phi(1.73)-\Phi(0.86)=0.9582-0.8051=\boxed{0.1531}.'),
    '.15','.1531',
    'Water use is between $27.22$ and $44.58$ cubic metres above forecast with probability about $15.00\\%$ under $t$ and $15.31\\%$ under normal. The normal probability is higher by $0.0031$, or $0.31$ percentage points.')

direct('Harvest forecasts',9,-2,4,r'P(-11.224<X<-5.556).',
    'Harvested-mass deviation is in tonnes. Both negative bounds represent shortfalls below forecast, and both lie below the model location $-2$.',
    r'\begin{aligned}c_L&=\frac{-11.224-(-2)}{4}=\frac{-11.224+2}{4}=\frac{-9.224}{4}=-2.306,\\c_U&=\frac{-5.556-(-2)}{4}=\frac{-5.556+2}{4}=\frac{-3.556}{4}=-0.889.\end{aligned}',
    'In row $8$, column $\\alpha=0.025$ gives $t^*=2.306$, and column $\\alpha=0.20$ gives $t^*=0.889$:\n'+math(r'P(T>2.306)\approx0.0250,\qquad P(T>0.889)\approx0.2000.')+'By symmetry these are the cumulative areas at the corresponding negative bounds. Use cumulative subtraction:\n'+math(r'P(c_L<T<c_U)=F_\nu(c_U)-F_\nu(c_L).')+math(r'\begin{aligned}F_8(-2.306)&=P(T>2.306)\approx0.0250,\\F_8(-0.889)&=P(T>0.889)\approx0.2000,\\p_T&\approx0.2000-0.0250=\boxed{0.1750}.\end{aligned}'),
    'Round $-2.306\\to z_L=-2.31$ and $-0.889\\to z_U=-0.89$. The positive CDF entries are $\\Phi(2.31)=0.9896$ and $\\Phi(0.89)=0.8133$. Use symmetry before subtracting:\n'+math(r'\Phi(-z)=1-\Phi(z),\qquad P(z_L<Z<z_U)=\Phi(z_U)-\Phi(z_L).')+math(r'\begin{aligned}\Phi(-2.31)&=1-0.9896=0.0104,\\\Phi(-0.89)&=1-0.8133=0.1867,\\p_N&=0.1867-0.0104=\boxed{0.1763}.\end{aligned}'),
    '.175','.1763',
    'A shortfall between $5.556$ and $11.224$ tonnes (about $5.56$ to $11.22$ tonnes below forecast) has probability about $17.50\\%$ under $t$ and $17.63\\%$ under normal. The normal probability is higher by $0.0013$, or $0.13$ percentage points.')

direct('Weekly revenue alerts',5,1,3,r'P(X<-5.396\text{ or }X>5.599).',
    'Revenue deviation is in thousands of dollars. The negative limit marks revenue below plan; the positive limit marks revenue above plan. An alert is in either of two disjoint tails.',
    r'\begin{aligned}c_L&=\frac{-5.396-1}{3}=\frac{-6.396}{3}=-2.132,\\c_U&=\frac{5.599-1}{3}=\frac{4.599}{3}=1.533.\end{aligned}',
    'In row $4$, column $\\alpha=0.05$ gives $t^*=2.132$, and column $\\alpha=0.10$ gives $t^*=1.533$:\n'+math(r'P(T>2.132)\approx0.0500,\qquad P(T>1.533)\approx0.1000.')+'Symmetry gives $P(T<-2.132)=P(T>2.132)$. A value cannot be in both alert tails, so their probabilities are added:\n'+math(r'P(T<c_L\text{ or }T>c_U)=F_\nu(c_L)+[1-F_\nu(c_U)].')+math(r'p_T\approx0.0500+0.1000=\boxed{0.1500}.'),
    'Round $-2.132\\to z_L=-2.13$ and $1.533\\to z_U=1.53$. The table gives $\\Phi(2.13)=0.9834$ and $\\Phi(1.53)=0.9370$. Use symmetry for the left tail and a complement for the right:\n'+math(r'\Phi(-z)=1-\Phi(z),\qquad P(Z>z)=1-\Phi(z).')+math(r'\begin{aligned}\Phi(-2.13)&=1-0.9834=0.0166,\\P(Z>1.53)&=1-0.9370=0.0630.\end{aligned}')+'Add these disjoint tail areas:\n'+math(r'\begin{aligned}p_N&=\Phi(z_L)+[1-\Phi(z_U)]\\&=0.0166+0.0630=\boxed{0.0796}.\end{aligned}'),
    '.15','.0796',
    'An alert means revenue more than $5.396$ thousand dollars below plan or more than $5.599$ thousand dollars above plan (about $5.40$ below or $5.60$ above). Its probability is about $15.00\\%$ under $t$ and $7.96\\%$ under normal. The normal probability is lower by $0.0704$, or $7.04$ percentage points.')

# Each inverse solution develops its own lookup, arithmetic and endpoint errors.
def normal_lookup(q):
    q=D(q)
    values={D('.1'):(-1.28,'0.1003',r'\Phi(-1.28)=1-\Phi(1.28)=1-0.8997=0.1003',
        r'The adjacent entry $\Phi(-1.29)=1-0.9015=0.0985$ is farther from $0.1000$.'),
      D('.9'):(1.28,'0.8997',r'\Phi(1.28)=0.8997',r'The adjacent entry $\Phi(1.29)=0.9015$ is farther from $0.9000$.'),
      D('.05'):(-1.64,'0.0505',r'\Phi(-1.64)=1-0.9495=0.0505',r'The entry $\Phi(-1.65)=1-0.9505=0.0495$ is equally close; choose $-1.64$ by the stated tie convention.'),
      D('.95'):(1.64,'0.9495',r'\Phi(1.64)=0.9495',r'The entry $\Phi(1.65)=0.9505$ is equally close; choose $1.64$ by the stated tie convention.'),
      D('.025'):(-1.96,'0.0250',r'\Phi(-1.96)=1-\Phi(1.96)=1-0.9750=0.0250',r'This printed entry matches the target.'),
      D('.975'):(1.96,'0.9750',r'\Phi(1.96)=0.9750',r'This printed entry matches the target.'),
      D('.01'):(-2.33,'0.0099',r'\Phi(-2.33)=1-\Phi(2.33)=1-0.9901=0.0099',r'The adjacent entry $\Phi(-2.32)=1-0.9898=0.0102$ is farther from $0.0100$.'),
      D('.99'):(2.33,'0.9901',r'\Phi(2.33)=0.9901',r'The adjacent entry $\Phi(2.32)=0.9898$ is farther from $0.9900$.')}
    return values[q]

def inverse(title,n,m,a,unit,quantity,qs,tcrit,event,target_explanation,interpret,central=None):
    m,a=D(m),D(a); nu=n-1; interval=len(qs)==2
    out.append(rf'\item \begin{{minipage}}[t]{{\linewidth}}\textbf{{{title} ($\nu={nu}$).}}\nopagebreak'+'\n')
    out.append(step(1,'Information and required cutoffs',rf'$n={n}$, $m={num(m)}$, $a={num(a)}$, so $\nu=n-1={n}-1={nu}$. '+quantity+math(event)+target_explanation)+'\\end{minipage}\\par\n')
    std=math(r'c=\frac{x-m}{a}.')
    if interval:
        std+='Apply the formula separately to the lower and upper unknown limits:\n'+math(r'\begin{aligned}'+rf'c_L&=\frac{{L-({num(m)})}}{{{num(a)}}}'+(rf'=\frac{{L+{num(-m)}}}{{{num(a)}}}' if m<0 else '')+r',\\'+rf'c_U&=\frac{{U-({num(m)})}}{{{num(a)}}}'+(rf'=\frac{{U+{num(-m)}}}{{{num(a)}}}' if m<0 else '')+r'.\end{aligned}')
    else:
        std+=math(rf'c=\frac{{x-({num(m)})}}{{{num(a)}}}'+(rf'=\frac{{x+{num(-m)}}}{{{num(a)}}}' if m<0 else '')+'.')
    std+='A negative standardized cutoff lies below the model location $m$; a positive one lies above it. The numerical standardized values are found from the probability targets before back-transformation.'
    out.append(step(2,'Standardize the unknowns',std))
    ts=[]; ns=[]; twork=[]; nwork=[]
    labels=['Lower','Upper'] if interval else ['Cutoff']
    for label,q,tc in zip(labels,qs,tcrit):
        q=D(q); tc=D(tc); alpha=min(q,1-q); c=-tc if q<D('.5') else tc
        z,entry,eq,explanation=normal_lookup(q); z=D(z)
        ts.append(c); ns.append(z)
        sub=',L' if label=='Lower' else ',U' if label=='Upper' else ''
        twork.append(rf'\par\textit{{{label}.}} Seek $F_{{{nu}}}(c_{{T{sub}}})={fixed(q,4)}$. '+
          (rf'This is below $0.5$, so the cutoff is negative. By symmetry use right-tail column $\alpha={num(alpha)}$.' if c<0 else rf'This is above $0.5$, so the cutoff is positive. The right-tail column is $\alpha=1-{fixed(q,4)}={num(alpha)}$.')+
          rf' Row ${nu}$, column $\alpha={num(alpha)}$, gives $t^*={fixed(tc,3)}$:'+math(rf'P(T>{fixed(tc,3)})\approx{fixed(alpha,4)}.')+
          (math(rf'F_{{{nu}}}(-{fixed(tc,3)})=P(T>{fixed(tc,3)})\approx{fixed(q,4)},\qquad c_{{T{sub}}}=-{fixed(tc,3)}.') if c<0 else math(rf'F_{{{nu}}}({fixed(tc,3)})=1-P(T>{fixed(tc,3)})\approx1-{fixed(alpha,4)}={fixed(q,4)}.')+math(rf'c_{{T{sub}}}={fixed(c,3)}.')))
        nwork.append(rf'\par\textit{{{label}.}} The left cumulative target is $\Phi(c_{{N{sub}}})={fixed(q,4)}$. '+('It requires a negative $z$ because the target is below $0.5$.' if z<0 else 'It requires a positive $z$ because the target is above $0.5$.')+
            (' For a negative lookup use $\Phi(-z)=1-\Phi(z)$.' if z<0 else '')+math(eq+'.')+explanation+math(rf'c_{{N{sub}}}={fixed(z,2)}.'))
    out.append(step(3,"Student's $t$ cutoffs",''.join(twork)))
    out.append(step(4,'Normal cutoffs',''.join('\\par\\noindent\\begin{minipage}{\\linewidth}\n'+w+'\\end{minipage}\\par\n' for w in nwork)))
    back=math(r'x=m+ac.')+'Multiply each selected standardized cutoff by the scale, then add the location. Retain the unrounded result for the comparison errors.\n'
    xt=[]; xn=[]
    for label,t,z in zip(labels,ts,ns):
        tt=a*t; nn=a*z; rt=m+tt; rn=m+nn; xt.append(rt);xn.append(rn)
        var='L' if label=='Lower' else 'U' if label=='Upper' else 'x'
        back+=('\\par\\textit{'+label+' back-transformation.}\n')+math(rf'\begin{{aligned}}{var}_T&={num(m)}+{num(a)}({fixed(t,3)})={num(m)}+({num(tt)})\\&={num(rt)}\approx\boxed{{{fixed(rt)}\ \text{{{unit}}}}},\\{var}_N&={num(m)}+{num(a)}({fixed(z,2)})={num(m)}+({num(nn)})\\&={num(rn)}\approx\boxed{{{fixed(rn)}\ \text{{{unit}}}}}.\end{{aligned}}')
    if interval:
        back+='The two completed intervals, in '+unit+', are\n'+math(rf'\boxed{{({fixed(xt[0])},\ {fixed(xt[1])})\quad(t)}},\qquad\boxed{{({fixed(xn[0])},\ {fixed(xn[1])})\quad(N)}}.')
    out.append(step(5,'Back-transform to contextual units',back))
    out.append(step(6,'Comparison errors',''.join(errors(t,z,unit,label=label+' cutoff' if interval else 'Cutoff') for label,t,z in zip(labels,xt,xn))))
    out.append(step(7,'Interpretation',interpret))

inverse('Cold-storage sensors',11,-2,6,'degrees Celsius',
 'The quantity is a sensor reading deviation in degrees Celsius; negative values mean below the reference reading.',
 ['.1'],['1.372'],r'P(X<x)=0.10.',
 'This is already a left-tail target: $P(X<x)=0.1000$; its complement is $P(X>x)=1-0.10=0.90$.',
 'About $10\\%$ of reading deviations lie below $-10.23$ degrees Celsius under $t$, or below $-9.68$ degrees Celsius under normal. These are deviations below the reference, not absolute storage temperatures. The normal cutoff is closer to the mean deviation by about $0.55$ degrees Celsius.')
inverse('Rail journey delays',24,3,8,'minutes',
 'The quantity is journey-time deviation in minutes; positive values mean journeys longer than scheduled.',
 ['.975'],['2.069'],r'P(X>x)=0.025.',
 'Convert the right tail to a left cumulative target before lookup:'+math(r'P(X<x)=1-P(X>x)=1-0.025=0.9750.'),
 'About $2.5\\%$ of journeys exceed a delay of $19.55$ minutes under $t$, or $18.68$ minutes under normal. Both positive cutoffs mean late arrival; the normal cutoff is about $0.87$ minutes lower.')
inverse('Electricity forecasting',19,10,40,'kWh',
 'The quantity is electricity-use deviation in kWh. Negative deviations mean use below forecast; positive deviations mean above forecast.',
 ['.05','.95'],['1.734','1.734'],r'P(L<X<U)=0.90\quad\text{with equal excluded tails}.',
 'A central interval splits the excluded probability equally:'+math(r'\alpha=\frac{1-\text{central probability}}{2}=\frac{1-0.90}{2}=\frac{0.10}{2}=0.05.')+'The lower and upper left cumulative targets are therefore'+math(r'P(X<L)=0.0500,\qquad P(X<U)=1-0.05=0.9500.'),
 'The central $90\\%$ limits are $(-59.36,79.36)$ kWh under $t$ and $(-55.60,75.60)$ kWh under normal, with approximately $5\\%$ in each excluded tail. The lower endpoint is below forecast and the upper endpoint above it. The normal interval extends less far from the mean at both ends, by $3.76$ kWh per endpoint.')
inverse('Packaging inspection',6,-.5,1.5,'g',
 'The quantity is package mass deviation in grams. Negative deviations mean below target mass; positive deviations mean above target.',
 ['.025','.975'],['2.571','2.571'],r'P(X<L)=P(X>U)=0.025.',
 'The central probability is $1-0.05=0.95$. Split the excluded area equally:'+math(r'\alpha=\frac{1-\text{central probability}}{2}=\frac{1-0.95}{2}=\frac{0.05}{2}=0.025.')+'The left cumulative targets are'+math(r'P(X<L)=0.0250,\qquad P(X<U)=1-0.025=0.9750.'),
 'The limits are $(-4.36,3.36)$ g under $t$ and $(-3.44,2.44)$ g under normal, enclosing approximately $95\\%$ of mass deviations with $2.5\\%$ in each tail. The lower limits are below target and the upper limits above target. Each normal endpoint is about $0.92$ g closer to the mean; the percentage errors differ because the endpoint magnitudes differ.')
inverse('Processing-time alerts',13,1,5,'minutes',
 'The quantity is processing-time deviation in minutes. Negative deviations mean processing faster than target; positive deviations mean slower.',
 ['.05','.9'],['1.782','1.356'],r'P(X<L)=0.05,\qquad P(X>U)=0.10.',
 'The two tails are unequal, so use their specified probabilities separately. Do not split $0.15$ into equal tails. The lower target is already cumulative; complement the upper right tail:'+math(r'P(X<L)=0.0500,\qquad P(X<U)=1-0.10=0.9000.')+'The area between the limits is $1-0.05-0.10=0.85$.',
 'The alert limits are $(-7.91,7.78)$ minutes under $t$ and $(-7.20,7.40)$ minutes under normal. Each model leaves approximately $5\\%$ below its lower limit, $10\\%$ above its upper limit, and $85\\%$ between them. The negative lower limits mean faster processing and positive upper limits mean slower processing. Normal moves the lower endpoint inward by $0.71$ minutes and the upper endpoint inward by $0.38$ minutes; the unequal tails give unequal distances from the mean.')
inverse('Hospital waiting',13,1,5,'minutes',
 'The quantity is waiting-time deviation from schedule in minutes. Negative deviations mean earlier than scheduled.',
 ['.1'],['1.356'],r'P(X<x)=0.10.',
 'The requested probability is already a left cumulative target: $P(X<x)=0.1000$. The remaining area is $P(X>x)=1-0.10=0.90$.',
 'About $10\\%$ of waiting-time deviations lie below $-5.78$ minutes under $t$, or below $-5.40$ minutes under normal. Thus the thresholds represent about $5.78$ or $5.40$ minutes earlier than scheduled, respectively. The normal cutoff is $0.38$ minutes closer to the mean.')
inverse('Production tolerance',21,0,12,'units',
 'The quantity is production-output deviation in units. Negative deviations mean below target output; positive deviations mean above target.',
 ['.025','.975'],['2.086','2.086'],r'P(L<X<U)=0.95\quad\text{with equal excluded tails}.',
 'Calculate the area in each tail first:'+math(r'\alpha=\frac{1-\text{central probability}}{2}=\frac{1-0.95}{2}=\frac{0.05}{2}=0.025.')+'The corresponding left cumulative targets are'+math(r'P(X<L)=0.0250,\qquad P(X<U)=1-0.025=0.9750.'),
 'The central $95\\%$ limits are $(-25.03,25.03)$ units under $t$ and $(-23.52,23.52)$ units under normal, leaving approximately $2.5\\%$ in each tail. They describe output below and above target, symmetrically because $m=0$. Each normal endpoint is about $1.51$ units closer to the target.')
inverse('Electricity peak',16,3,7,'MW',
 'The quantity is peak-demand deviation in MW. A positive deviation means peak demand above forecast.',
 ['.99'],['2.602'],r'P(X>x)=0.01.',
 'Convert the right-tail condition to the left cumulative target:'+math(r'P(X<x)=1-P(X>x)=1-0.01=0.9900.'),
 'About $1\\%$ of peak-demand deviations exceed $21.21$ MW above forecast under $t$, or $19.31$ MW above forecast under normal. The normal cutoff is about $1.90$ MW lower; each cutoff refers to its own model probability.')
inverse('Transit reliability',9,-1,3,'minutes',
 'The quantity is arrival-time deviation in minutes. Negative deviations mean early arrival; positive deviations mean late arrival.',
 ['.05','.975'],['1.860','2.306'],r'P(X<L)=0.05,\qquad P(X>U)=0.025.',
 'The alert tails are unequal: use $0.05$ for the lower tail and $0.025$ for the upper tail separately. The left cumulative targets are'+math(r'P(X<L)=0.0500,\qquad P(X<U)=1-0.025=0.9750.')+'The enclosed area is $1-0.05-0.025=0.925$, not a central interval with equal tails.',
 'The alert limits are $(-6.58,5.92)$ minutes under $t$ and $(-5.92,4.88)$ minutes under normal. Approximately $5\\%$ of journeys are earlier than the lower limit and $2.5\\%$ are later than the upper limit, leaving $92.5\\%$ between each model\'s limits. Normal moves the early limit toward the mean by $0.66$ minutes and the late limit toward the mean by about $1.04$ minutes.')
inverse('Shipping weight',11,2,4,'kg',
 'The quantity is shipment-mass deviation in kg. Negative deviations mean below target mass; positive deviations mean above target.',
 ['.01','.99'],['2.764','2.764'],r'P(L<X<U)=0.98\quad\text{with equal excluded tails}.',
 'Calculate each excluded tail:'+math(r'\alpha=\frac{1-\text{central probability}}{2}=\frac{1-0.98}{2}=\frac{0.02}{2}=0.01.')+'The left cumulative targets are'+math(r'P(X<L)=0.0100,\qquad P(X<U)=1-0.01=0.9900.'),
 'The central $98\\%$ limits are $(-9.06,13.06)$ kg under $t$ and $(-7.32,11.32)$ kg under normal, with approximately $1\\%$ below each lower limit and $1\\%$ above each upper limit. Lower limits mean mass below target; upper limits mean mass above target. Each normal endpoint is about $1.74$ kg closer to the mean deviation, so the normal interval is narrower.')

out.append('\\end{enumerate}\n\\endgroup\n\\end{document}\n')
replacement=''.join(out).replace('\n','\r\n').encode('utf-8')
p.write_bytes(prefix+replacement)
assert p.read_bytes()[:len(prefix)] == prefix
assert len(re.findall(rb'\\item ',replacement))==15
Path('tmp/c9-solutions/audit.json').write_text(json.dumps(audit,indent=2))
print('Rewrote 15 solutions; unchanged prefix bytes:',len(prefix))
for item in audit: print(item)

