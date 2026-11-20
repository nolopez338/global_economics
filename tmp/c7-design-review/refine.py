from pathlib import Path
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L2_C7_practice.tex')
s=p.read_text(encoding='utf-8-sig')
s=s.replace('0.98564','0.98567').replace('1.0513>1','1.0514>1')
s=s.replace('A cooperative will estimate mean reference-week earnings for its 20,000 couriers. Known population SD is 80 thousand COP. Assume no extreme skew or outliers and complete responses to a simple random sample without replacement. Candidate designs are A: 100 at 90\\%; B: 256 at 95\\%; C: 400 at 99\\%. Each usable record costs 8,000 COP; there are no other costs.', 'A cooperative will estimate mean weekly earnings for 20,000 couriers, with known population SD 80 thousand COP and no extreme skew or outliers. Assume complete responses to simple random sampling without replacement. Designs: A, 100 at 90\\%; B, 256 at 95\\%; C, 400 at 99\\%. Cost is 8,000 COP per usable record, with no other costs.')
s=s.replace('The parameter $\\mu$ is mean earnings in thousand COP. The known-$\\sigma$ normal model is supported by random sampling, the stated shape and fractions at most 2\\%. Hold the population, $\\HLPopulationSD{\\sigma=80}$, units, method and unit cost fixed. Sizes and confidence change. No observed means exist, so compare projected precision, not endpoints.', 'Estimate $\\HLPopulationMean{\\mu}$, mean earnings in thousand COP, using the known-$\\sigma$ normal model. Random sampling, the stated shape and fractions at most 2\\% support it. Hold the population, $\\HLPopulationSD{\\sigma=80}$, method and unit cost fixed; change $n,C$. Without observed means, compare projected precision.')
s=s.replace('Use $z_{.90}\\approx1.64485362695$, $z_{.95}\\approx1.95996398454$ and $z_{.99}\\approx2.57582930355$, retaining full calculator precision. For each row, $SE=80/\\sqrt n$, $E=z_CSE$, $W=2E$; cost $=8{,}000n$ COP.', 'Store $z_{.90}=\\Phi^{-1}(0.95)$, $z_{.95}=\\Phi^{-1}(0.975)$ and $z_{.99}=\\Phi^{-1}(0.995)$ at full precision. Use $SE=80/\\sqrt n$, $E=z_CSE$, $W=2E$; cost $=8{,}000n$ COP.')
s=s.replace('SE, margin and width are thousand COP. A fails every constraint. C meets SE and confidence but fails margin and width: higher confidence more than offsets its size advantage over B. Indeed', 'SE, margin and width are thousand COP. A fails all constraints. C meets SE and confidence but fails margin and width:')
s=s.replace('Recommend B among the candidates: it meets every requirement and costs less than C.', 'Recommend B: it meets every requirement at lower cost than C.')
s=s.replace('\\textbf{Allowing a new design.} Use $C_0=0.95$, because a larger confidence multiplier requires at least as many records for these precision caps. The three size bounds are', '\\textbf{A new design.} Use $C_0=0.95$; higher confidence cannot reduce the required size. The bounds are')
s=s.replace('Thus $n_{\\min}=\\lceil\\max(177.777\\ldots,245.8534\\ldots)\\rceil=246$. At 246, $SE\\approx5.1006$, $E\\approx9.9970$, $W\\approx19.9940$; at 245, $E\\approx10.0174>10$ and $W\\approx20.0348>20$. Monotonicity establishes minimality. The new 95\\% design costs 1,968,000 COP, saving 80,000 COP over B. Sampling 1.23\\% of the roster supports approximate independence.', 'Thus $\\HLObservationCount{n_{\\min}}=\\lceil\\max(177.777\\ldots,245.8534\\ldots)\\rceil=\\HLObservationCount{246}$. At 246, $SE\\approx5.1006$, $E\\approx9.9970$, $W\\approx19.9940$; at 245, $E\\approx10.0174>10$, $W\\approx20.0348>20$. Monotonicity establishes minimality. This 95\\% design costs 1,968,000 COP, saving 80,000 COP over B; its fraction is 1.23\\%.')
s=s.replace('The fourth C6 target is explicit: with fixed margin cap 10, $C(n)=2\\Phi(10\\sqrt n/80)-1$ must be at least 0.95. This is equivalent to the margin inequality. Confidence alone supplies no precision bound. These model-based assurances do not guarantee small realized error or freedom from nonresponse bias.', 'For C6\'s fourth target, fixed margin cap 10 gives $C(n)=2\\Phi(10\\sqrt n/80)-1\\ge0.95$, equivalent to the margin inequality. Confidence alone supplies no precision bound. The model guarantees neither small realized error nor absence of bias.')
# Comparison tables: semantic roles are selected by each column's meaning.
import re
start=s.index('\\section{General Worked Problems}')
a,b=s[:start],s[start:]
roles={
'n': ['HLObservationCount','HLStandardError','HLMarginOfError','HLIntervalWidth','HLIntervalBounds'],
'Cmean':['HLConfidence','HLCriticalValue','HLMarginOfError','HLIntervalWidth','HLIntervalBounds'],
'study':['','HLStandardError','HLMarginOfError','HLIntervalWidth','HLSampleMean','HLIntervalBounds'],
'survey':['','HLSampleProportion','HLMarginOfError','HLIntervalWidth','HLIntervalBounds'],
'design':['','HLConfidence','HLStandardError','HLMarginOfError','HLIntervalWidth','','']}
def style_table(m):
 t=m.group(0)
 if '$n$ & ' in t: rr=roles['n']
 elif '$C$ & $z^*$' in t: rr=roles['Cmean']
 elif 'Study & SE' in t: rr=roles['study']
 elif 'Survey & Centre' in t: rr=roles['survey']
 elif 'Design & $C$' in t: rr=roles['design']
 else: return t
 pre,body=t.split('\\midrule\n',1)
 data,post=body.split('\\bottomrule',1)
 rows=data.strip().split('\\\\\n')
 styled=[]
 for row in rows:
  end=''
  if row.endswith('\\\\'): row=row[:-2];end='\\\\'
  cells=row.split(' & ')
  for i,c in enumerate(cells):
   if i>=len(rr) or not rr[i]: continue
   c=c.strip()
   if c.startswith('$') and c.endswith('$'): c='$\\'+rr[i]+'{'+c[1:-1]+'}$'
   else: c='\\'+rr[i]+'{'+c+'}'
   cells[i]=c
  styled.append(' & '.join(cells)+end)
 return '\\begingroup\\tikzset{gten marker/.append style={inner xsep=.6mm,inner ysep=.2mm}}\n'+pre+'\\midrule\n'+'\\\\\n'.join(styled)+'\\bottomrule'+post+'\\endgroup'
b=re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}',style_table,b,flags=re.S)
s=a+b
# Match names to marked symbols and values, without changing task answer boundaries.
s=s.replace('Population; sample mean & Target average; observed centre.', '\\HLPopulationMean{Population mean}; \\HLSampleMean{sample mean} & Target average; observed centre.')
s=s.replace('Population; sample share & Target fraction; observed centre.', '\\HLPopulationProportion{Population share}; \\HLSampleProportion{sample share} & Target fraction; observed centre.')
s=s.replace('Variability inputs & Known population SD; planning share.', '\\HLPopulationSD{Population SD}; \\HLModelControl{planning share} & Known spread; assumed share.')
# Use palette for graph stroke only when enabled, preserving all labels/data off.
s=s.replace('\\addplot[black,thick,mark=|]', '\\addplot[draw=\\ifGTenHighlights CtwoWidthColor\\else black\\fi,thick,mark=|]')
p.write_text(s,encoding='utf-8')
