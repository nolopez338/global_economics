from pathlib import Path
import re
import hashlib

root = Path('book2026-2027/grade10/term_1/2-class_activities')
source = root / 'G10_T1_L1_C6C7_classroom_activity.tex'
original = source.read_bytes()
parts = re.split(r'(?=\\section\{)', original.decode('utf-8').replace('\r\n','\n'))
assert len(parts) == 15

def intro(s, heading, text):
    # Keep the original table and subsequent scaffolding.
    return re.sub(r'\\section\{[^}]*\}.*?(?=\\begin\{center\})',
                  lambda _: '\\section{' + heading + '}\n' + text + '\n', s, count=1, flags=re.S)

def values(s, mapping):
    # Replace only complete numerical tokens, without cascading replacements.
    return re.sub(r'(?<![\w.])(?:' + '|'.join(re.escape(k) for k in sorted(mapping, key=len, reverse=True)) + r')(?![\w.])',
                  lambda m: mapping[m[0]], s)

parts[0] = parts[0].replace('10th Grade - 1st Term: C6 \\& C7 Expected Monetary Value',
                           'Grade 10 - Term 1: C6 \\& C7\\\\Expected Monetary Value - Version 2')
parts[1] = parts[1].replace('The probabilities must satisfy',
    'All probabilities are nonnegative: $P(S_j)\\geq0$. They must satisfy')
parts[1] = parts[1].replace('For each alternative, calculate its Expected Monetary Value:',
    'In every exercise, choose an alternative before the external state is known. '
    'The same state probabilities apply to all alternatives. All table entries are monetary payoffs, '
    'and higher values are better. All payoffs and EMVs are in \\textbf{thousand USD}.\n\n'
    'For each alternative, calculate its Expected Monetary Value:')
parts[1] = parts[1].replace('A threshold probability occurs when two alternatives have equal',
    'A possible switching threshold occurs when two alternatives have equal')
parts[1] = parts[1].replace('The threshold divides the feasible probability range into regions in',
    'An equality is a decision threshold only if the tied alternatives attain the highest EMV. '
    'There may be no feasible threshold, or several thresholds. Decision thresholds divide the feasible probability range into regions in')
parts[1] = parts[1].replace('p{0.2\\columnwidth}p{0.20\\columnwidth}p{0.2\\columnwidth}',
    'p{0.13\\columnwidth}p{0.48\\columnwidth}p{0.18\\columnwidth}')
parts[1] = parts[1].replace('4--6 & Practice & C6', '4 & Scaffolded Practice & C6 \\\\\n\t\t\t5--6 & Independent Practice & C6')
parts[1] = parts[1].replace('9--12 & Practice & C7', '9 & Independent Practice & C7 \\\\\n\t\t\t10 & Dominance Practice & C7 \\\\\n\t\t\t11--14 & Practice & C7')

parts[2] = r'''\section{Solved Example: Museum Gallery}
A museum must choose an expanded gallery ($A_1$) or a compact gallery ($A_2$)
before regional tourism is known. Tourism may be busy ($S_1$) or quiet ($S_2$).
Visitor records give estimated probabilities of 70\% and 30\%, respectively.
\begin{center}
\renewcommand{\arraystretch}{1.3}\small
\begin{tabular}{lr@{\qquad}cc}
\cmidrule{1-4}
Alternative && $S_1$ & $S_2$ \\
& $P(S_j)$: & 70\% & 30\% \\
\cmidrule{1-4}
\multicolumn{2}{l}{Expanded gallery ($A_1$)} & 62 & 8 \\
\multicolumn{2}{l}{Compact gallery ($A_2$)} & 39 & 26 \\
\cmidrule{1-4}
\end{tabular}
\end{center}
All payoffs and EMVs are in thousand USD. Which gallery should the museum
choose using Expected Monetary Value?
\subsection{Solution}
\textbf{Step 0: Identify the probabilities}
\[
P(S_1)=0.7,\qquad P(S_2)=0.3.
\]
Both are nonnegative. Check they sum to $1$:
\[
P(S_1)+P(S_2)=0.7+0.3=1.
\]
\textbf{Step 1.1: Calculate the EMV of $A_1$}

Multiply each payoff by its state's probability and add:
\[
\begin{aligned}
EMV(A_1)&=P(S_1)P_{ay}(A_1,S_1)\\
&\quad+P(S_2)P_{ay}(A_1,S_2)\\
&=(0.7)(62)+(0.3)(8)\\
&=43.4+2.4=45.8.
\end{aligned}
\]
The expanded gallery has an EMV of $45.8$ thousand USD, equivalent to
\$45,800.

\textbf{Step 1.2: Calculate the EMV of $A_2$}
\[
\begin{aligned}
EMV(A_2)&=P(S_1)P_{ay}(A_2,S_1)\\
&\quad+P(S_2)P_{ay}(A_2,S_2)\\
&=(0.7)(39)+(0.3)(26)\\
&=27.3+7.8=35.1.
\end{aligned}
\]
The compact gallery has an EMV of $35.1$ thousand USD, equivalent to
\$35,100.

\textbf{Step 2: Apply the Bayes decision criterion}

Compare both EMVs:
\[
R^*=\max\{45.8,35.1\}=45.8
\]
\[
A^*_{\mathrm{Bayes}}=\arg\max_i EMV(A_i)=A_1.
\]
Choose the expanded gallery: its expected monetary payoff is \$45,800,
compared with \$35,100 for the compact gallery.

\textbf{Extended payoff table}
\begin{center}
\small\renewcommand{\arraystretch}{1.5}
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lccc}
\toprule
Alternative & $S_1\;(0.7)$ & $S_2\;(0.3)$ & EMV \\
\midrule
$A_1$ & 62 & 8 & $0.7(62)+0.3(8)=45.8$ \\
$A_2$ & 39 & 26 & $0.7(39)+0.3(26)=35.1$ \\
\midrule
Highest EMV &&& $45.8$ \\
\bottomrule
\end{tabular}
\end{center}
\[
A^*_{\mathrm{Bayes}}=\arg\max_i EMV(A_i)=A_1.
\]
'''

parts[3] = intro(parts[3], 'Guided Practice: Orchard Lease', r'''
A grower must lease a hillside orchard ($A_1$) or a valley orchard ($A_2$)
before seasonal rainfall is known. Rainfall may be ample ($S_1$), moderate
($S_2$), or scarce ($S_3$). Weather records give estimated probabilities
of 40\%, 35\%, and 25\%, respectively. Payoffs and EMVs are in thousand USD.
''')
parts[3] = values(parts[3], {'0.5':'0.4','0.3':'0.35','0.2':'0.25',
    '90':'96','30':'34','-15':'-18','65':'68','45':'48','20':'24'})
parts[3] = parts[3].replace('Demand','Rainfall').replace('High ($S_1$)', 'Ample ($S_1$)').replace('Medium ($S_2$)', 'Moderate ($S_2$)').replace('Low ($S_3$)', 'Scarce ($S_3$)')
parts[3] = parts[3].replace('Large production', 'Hillside ($A_1$)').replace('Medium production','Valley ($A_2$)')

parts[4] = intro(parts[4], 'Scaffolded Practice: Campsite Plan', r'''
A campsite owner must choose open pitches ($A_1$), covered pitches ($A_2$),
cabins ($A_3$), or a fixed lease ($A_4$) before the summer weather is known.
Weather records estimate dry weather ($S_1$) at 55\% and wet weather ($S_2$)
at 45\%. The fixed lease guarantees the same payoff in either state.
Payoffs and EMVs are in thousand USD.
''')
parts[4] = values(parts[4], {'0.6':'0.55','0.4':'0.45','88':'94','-12':'-16','64':'70','14':'18','42':'46','30':'32','20':'24'})
parts[4] = parts[4].replace('Demand','Weather').replace('High ($S_1$)','Dry ($S_1$)').replace('Low ($S_2$)','Wet ($S_2$)')
for a,b in [('Large production','Open pitches ($A_1$)'),('Medium production','Covered pitches ($A_2$)'),('Small production','Cabins ($A_3$)'),('Maintain production','Fixed lease ($A_4$)')]:
    parts[4]=parts[4].replace(a,b)

parts[5] = intro(parts[5], 'Independent Practice: Translation Rights', r'''
A publisher must choose worldwide translation rights ($A_1$), selected
language rights ($A_2$), regional rights ($A_3$), or a fixed license ($A_4$)
before overseas interest in a novel is known. Interest may be strong ($S_1$),
steady ($S_2$), or weak ($S_3$). Reader research estimates probabilities
of 45\%, 25\%, and 30\%, respectively. The fixed license guarantees the
same payment in all states. Payoffs and EMVs are in thousand USD.
''')
parts[5]=values(parts[5], {'72':'78','38':'42','8':'12','58':'62','45':'49','20':'23','40':'44','35':'37','28':'31','22':'26'})
parts[5]=parts[5].replace(r'49\%',r'45\%')
parts[5]=parts[5].replace('Demand','Overseas interest').replace('the coffee shop','the publisher')
parts[5]=parts[5].replace('criterion?\\vspace{-4mm}', 'criterion?\n\\vspace{2.5cm}')

parts[6] = intro(parts[6], 'Independent Practice: Irrigation Plan', r'''
A greenhouse cooperative must select intensive irrigation ($A_1$),
balanced irrigation ($A_2$), or minimal irrigation ($A_3$) before the dry
season. The external water supply may be abundant ($S_1$), adequate ($S_2$),
limited ($S_3$), or restricted ($S_4$). Reservoir research estimates the
probabilities as 25\%, 30\%, 25\%, and 20\%, respectively.
Payoffs and EMVs are in thousand USD.
''')
parts[6]=values(parts[6], {'95':'102','70':'76','30':'34','-10':'-14','72':'79','58':'63','38':'41','18':'21','48':'52','45':'47','35':'39','25':'29'})
parts[6]=parts[6].replace(r'29\%',r'25\%').replace(r'34\%',r'30\%')
parts[6]=parts[6].replace('Demand','Water supply').replace('the company','the cooperative')
parts[6]=parts[6].replace('criterion? \\vspace{-3mm}', 'criterion?\n\\vspace{3cm}')

parts[7] = r'''\section{Solved Example: Wildlife Hide}
A reserve must choose an open hide ($A_1$) or a sheltered hide ($A_2$)
before the season's visibility is known. Visibility may be clear ($S_1$)
or misty ($S_2$). Let $p$ be the reserve manager's subjective probability
of clear visibility, based on judgment; mist has probability $1-p$,
where $0\leq p\leq1$. Payoffs and EMVs are in thousand USD.
Find how the preferred hide changes with $p$.
\begin{center}
\renewcommand{\arraystretch}{1.3}\small
\begin{tabular}{lr@{\qquad}cc}
\cmidrule{1-4}
Alternative && $S_1$ & $S_2$ \\
& $P(S_j)$: & $p$ & $1-p$ \\
\cmidrule{1-4}
\multicolumn{2}{l}{Open hide ($A_1$)} & 68 & 8 \\
\multicolumn{2}{l}{Sheltered hide ($A_2$)} & 48 & 38 \\
\cmidrule{1-4}
\end{tabular}
\end{center}
\subsection*{Step 1.1: Calculate the EMV of $A_1$}
For the open hide:
\[
\begin{aligned}
EMV(A_1)&=p(68)+(1-p)(8)\\
&=68p+8-8p=60p+8.
\end{aligned}
\]
Its expected payoff is $60p+8$ thousand USD.
\subsection*{Step 1.2: Calculate the EMV of $A_2$}
For the sheltered hide:
\[
\begin{aligned}
EMV(A_2)&=p(48)+(1-p)(38)\\
&=48p+38-38p=10p+38.
\end{aligned}
\]
Its expected payoff is $10p+38$ thousand USD.
\subsection*{Step 2: Find the threshold probability}
Equate the two EMV functions:
\[
EMV(A_1)=EMV(A_2)
\]
\[
\begin{aligned}
60p+8&=10p+38\\
50p&=30\\
p&=\frac{30}{50}=\frac35=0.6.
\end{aligned}
\]
\subsection*{Step 3: Perform the sensitivity analysis}
The difference is $EMV(A_1)-EMV(A_2)=50p-30$.
Compare on both sides of $p=\frac35$:
\[
\begin{aligned}
p<\tfrac35&\Rightarrow EMV(A_1)<EMV(A_2)\\
&\Rightarrow\text{choose }A_2,\\[2mm]
p>\tfrac35&\Rightarrow EMV(A_1)>EMV(A_2)\\
&\Rightarrow\text{choose }A_1,\\[2mm]
p=\tfrac35&\Rightarrow EMV(A_1)=EMV(A_2)\\
&\Rightarrow\text{indifferent.}
\end{aligned}
\]
At the threshold both EMVs are $44$ thousand USD. Thus:
\[
\boxed{A^*_{\mathrm{Bayes}}=
\begin{cases}
A_2 & 0\leq p<\frac35,\\
\text{Indifferent} & p=\frac35,\\
A_1 & \frac35<p\leq1.
\end{cases}}
\]
Choose the sheltered hide below a 60\% subjective chance of clear
visibility, and the open hide above it; either is optimal at 60\%.
'''

parts[8]=intro(parts[8], 'Guided Practice: Art Workshop', r'''
An art school must book a courtyard ($A_1$) or an indoor studio ($A_2$)
before workshop-day weather is known. Weather may be dry ($S_1$) or rainy
($S_2$). Let $p$ be the coordinator's subjective probability of dry weather,
based on judgment; rain has probability $1-p$, with $0\leq p\leq1$.
Payoffs and EMVs are in thousand USD. Find the preferred venue for every
$p$ and the probability at which the coordinator is indifferent.
''')
parts[8]=values(parts[8], {'50':'58','10':'6','40':'43','20':'31'})
for a,b in [('Launch new campaign','Courtyard'),('Keep current strategy','Indoor studio'),
    ('launching the new campaign','booking the courtyard'),('keeping the current strategy','booking the indoor studio'),
    ('the manager','the coordinator'),('strong sales','dry weather')]:
    parts[8]=parts[8].replace(a,b)

parts[9]=intro(parts[9], 'Independent Practice: Apiary', r'''
A beekeeper must choose a meadow apiary ($A_1$) or woodland apiary
($A_2$) before flowering conditions are known: favorable ($S_1$) or
poor ($S_2$). Let $p$ be the beekeeper's subjective probability of
favorable conditions, based on judgment; poor conditions have probability
$1-p$, $0\leq p\leq1$. Payoffs and EMVs are in thousand USD.
Find the preferred apiary for every $p$, including indifference.
''')
parts[9]=values(parts[9], {'70':'76','10':'12','45':'51','30':'32'})
parts[9]=parts[9].replace('Produce large quantity','Meadow apiary').replace('Produce small quantity','Woodland apiary')

parts[10]=intro(parts[10], 'Dominance Practice: Archive', r'''
An archive must choose full service ($A_1$) or basic service ($A_2$)
before grant funding is known: ample ($S_1$) or limited ($S_2$).
Let $p$ be the director's subjective probability of ample funding,
based on judgment; limited funding has probability $1-p$,
$0\leq p\leq1$. Payoffs and EMVs are in thousand USD.
Which service is preferred for every $p$? Does a feasible switching
threshold exist? If none exists, explain why.
''')
parts[10]=values(parts[10], {'50':'57','40':'44','45':'49','35':'36'})
parts[10]=parts[10].replace('Prepare large fleet','Full service').replace('Prepare small fleet','Basic service')

parts[11]=intro(parts[11], 'Practice: Vineyard Layout', r'''
A vineyard must choose hillside vines ($A_1$), mixed plots ($A_2$), or
sheltered vines ($A_3$) before growing conditions are known. Conditions
may be favorable ($S_1$) or adverse ($S_2$). Let $p$ be the grower's
subjective probability of favorable conditions, based on judgment;
adverse conditions have probability $1-p$, where $0\leq p\leq1$.
Payoffs and EMVs are in thousand USD. Compare all three EMV functions
and give the preferred layout over the whole feasible interval,
including all optimal ties. Check whether each pairwise intersection
actually changes the optimal decision.
''')
parts[11]=values(parts[11], {'80':'86','10':'6','60':'66','30':'26','40':'46','35':'36'})
parts[11]=parts[11].replace('Large quantity','Hillside vines').replace('Medium quantity','Mixed plots').replace('Small quantity','Sheltered vines')

parts[12]=intro(parts[12], 'Practice: Archaeological Survey', r'''
A survey firm must choose extensive fieldwork ($A_1$) or a limited survey
($A_2$) before land-access permits are decided. Access may be full ($S_1$),
partial ($S_2$), or denied ($S_3$). Let $p$ be the director's subjective
probability of full access, based on judgment, with $0\leq p\leq1$.
Conditional on access not being full, the director assigns probability
$\alpha=0.25$ to partial access and $1-\alpha=0.75$ to denial.
Thus the state probabilities are $p$, $0.25(1-p)$, and $0.75(1-p)$.
Payoffs and EMVs are in thousand USD. Determine the preferred survey
for every $p$ and identify the indifference threshold.
''')
parts[12]=values(parts[12], {'0.4':'0.25','0.6':'0.75','80':'92','55':'60','5':'12','50':'62','40':'44','25':'28'})
parts[12]=parts[12].replace('Large quantity','Extensive ($A_1$)').replace('Small quantity','Limited ($A_2$)')

parts[13]=intro(parts[13], 'Practice: Mineral Exploration', r'''
An exploration firm must choose deep drilling ($A_1$), mixed drilling
($A_2$), shallow drilling ($A_3$), or a surface survey ($A_4$) before
the site's mineral grade is known. Grade may be rich ($S_1$) or lean
($S_2$). Let $p$ be the geologist's subjective probability of rich grade,
based on judgment; lean grade has probability $1-p$, with $0\leq p\leq1$.
Payoffs and EMVs are in thousand USD. Compare all four EMV functions
and give the preferred plan over the whole feasible interval, including
all optimal ties. Check whether each pairwise intersection actually
changes the optimal decision.
''')
parts[13]=values(parts[13], {'90':'78','5':'8','75':'73','25':'23','55':'63','40':'33','35':'48','45':'38'})
parts[13]=parts[13].replace('Very large quantity','Deep drilling').replace('Large quantity','Mixed drilling').replace('Medium quantity','Shallow drilling').replace('Small quantity','Surface survey')

parts[14]=intro(parts[14], 'Practice: Marina Berth Agreement', r'''
A marina must choose a seasonal berth agreement ($A_1$) or an annual
berth agreement ($A_2$) before coastal sailing conditions are known.
Conditions may be excellent ($S_1$), fair ($S_2$), or stormy ($S_3$).
Let $p$ and $q$ be the manager's subjective probabilities of excellent
and fair conditions, based on judgment. Stormy conditions have
probability $1-p-q$. The feasible domain is
\[
p\geq0,\qquad q\geq0,\qquad p+q\leq1.
\]
Payoffs and EMVs are in thousand USD. Construct both EMV functions,
find the indifference line, and determine the region in the feasible
domain where each agreement is preferred, including the tie case.
''')
parts[14]=values(parts[14], {'80':'84','55':'56','5':'9','50':'54','40':'41','25':'29'})
parts[14]=parts[14].replace('Large number of tickets','Seasonal berths').replace('Small number of tickets','Annual berths')

# Tighten the two worked examples without changing their calculation steps.
parts[2] = parts[2].replace(r'''\[
P(S_1)=0.7,\qquad P(S_2)=0.3.
\]
Both are nonnegative. Check they sum to $1$:''',
    r'The probabilities are $P(S_1)=0.7$ and $P(S_2)=0.3$. Both are nonnegative. Check their sum:')
for i in (1,2):
    parts[2] = parts[2].replace(
        rf'''EMV(A_{i})&=P(S_1)P_{{ay}}(A_{i},S_1)\\
&\quad+P(S_2)P_{{ay}}(A_{i},S_2)\\''',
        rf'''EMV(A_{i})&=\sum_{{j=1}}^2P(S_j)P_{{ay}}(A_{i},S_j)\\''')
parts[2] = parts[2].replace(r'''R^*=\max\{45.8,35.1\}=45.8
\]
\[
A^*_{\mathrm{Bayes}}=\arg\max_i EMV(A_i)=A_1.''',r'''\begin{aligned}
R^*&=\max\{45.8,35.1\}=45.8,\\
A^*_{\mathrm{Bayes}}&=\arg\max_i EMV(A_i)=A_1.
\end{aligned}''')
parts[2] = parts[2].replace('\\textbf{Extended payoff table}\n\\begin{center}',
    '\\textbf{Extended payoff table}\\vspace{-3mm}\n\\begin{center}')
parts[2] = parts[2].replace(r'''\end{center}
\[
A^*_{\mathrm{Bayes}}=\arg\max_i EMV(A_i)=A_1.
\]''', r'''\end{center}\vspace{-3mm}
Thus $A^*_{\mathrm{Bayes}}=A_1$: choose the expanded gallery.''')
parts[2] = parts[2].replace('Thus $A^*_{\\mathrm{Bayes}}=A_1$: choose the expanded gallery.', '')
parts[7] = parts[7].replace('For the open hide:\n','').replace('For the sheltered hide:\n','')
parts[7] = parts[7].replace(r'''Equate the two EMV functions:
\[
EMV(A_1)=EMV(A_2)
\]''', r'Set $EMV(A_1)=EMV(A_2)$:')
parts[7] = parts[7].replace(r'''p<\tfrac35&\Rightarrow EMV(A_1)<EMV(A_2)\\
&\Rightarrow\text{choose }A_2,\\[2mm]
p>\tfrac35&\Rightarrow EMV(A_1)>EMV(A_2)\\
&\Rightarrow\text{choose }A_1,\\[2mm]
p=\tfrac35&\Rightarrow EMV(A_1)=EMV(A_2)\\
&\Rightarrow\text{indifferent.}''',r'''p<\tfrac35&\,\Rightarrow\, EMV(A_1)<EMV(A_2)\,\Rightarrow\, A_2,\\[2mm]
p>\tfrac35&\,\Rightarrow\, EMV(A_1)>EMV(A_2)\,\Rightarrow\, A_1,\\[2mm]
p=\tfrac35&\,\Rightarrow\, EMV(A_1)=EMV(A_2)\,\Rightarrow\,\text{tie.}''')
parts[8] = parts[8].replace('For the Courtyard alternative:\n','').replace('For the Indoor studio alternative:\n','')
parts[8] = parts[8].replace('The threshold occurs when the two alternatives have the same expected\n\tvalue:',
                           'Set the two EMVs equal:')
parts[8] = parts[8].replace('Thus, the expected payoff from booking the courtyard is', 'Courtyard EMV:')
parts[8] = parts[8].replace('Thus, the expected payoff from booking the indoor studio is', 'Indoor studio EMV:')
parts[8] = parts[8].replace('Therefore, the coordinator is indifferent between the two alternatives when\n\tthe subjective probability of dry weather is',
                           'Indifference occurs at the dry-weather probability')
# Keep complete exercises together and reserve room for independent working.
# The original used explicit column/page breaks; retain that design locally.
compact = r'''\begingroup
\small\linespread{1.05}\selectfont
\setlength{\parskip}{3pt}
\setlength{\abovedisplayskip}{5pt}
\setlength{\belowdisplayskip}{5pt}
\setlength{\abovedisplayshortskip}{3pt}
\setlength{\belowdisplayshortskip}{3pt}
'''
parts[1] = parts[1].replace(r'\newpage', '\\endgroup\n\\newpage')
parts[1] = compact + parts[1]
parts[1] = parts[1].replace('p{0.13\\columnwidth}p{0.48\\columnwidth}p{0.18\\columnwidth}',
                          'p{0.17\\columnwidth}p{0.44\\columnwidth}p{0.18\\columnwidth}')
for i in range(2,15):
    parts[i] = re.sub(r'\\(?:columnbreak|newpage)\s*','',parts[i])
    parts[i] = re.sub(r'\\vspace\{(?:2\.5|3)cm\}', '',parts[i])
    if i in (2,7,8):
        parts[i] = re.sub(r'(\\subsection\*?\{[^\n]+\})',
                          lambda m: '\\vspace{-3mm}\n'+m[0]+'\\vspace{-1mm}', parts[i])
        parts[i] = compact + parts[i] + '\n\\endgroup\n'
    if i!=2 and i!=10:
        parts[i] = '\n\\columnbreak\n' + parts[i]
    if i==9:
        parts[i] += '\n\\vspace{3.5cm}\n'
parts[8] = parts[8].replace(r'\quad\Rightarrow\quad',r'\,\Rightarrow\,')
result=''.join(parts)
result=result.replace(r'\begin{multicols}{2}',r'\begin{multicols*}{2}').replace(r'\end{multicols}',r'\end{multicols*}')
result=result.replace(r'\cmidrule{1-12}',r'\cmidrule{1-5}').replace(r'\cmidrule{1-9}',r'\cmidrule{1-5}')
result=result.replace('($A_1$) ($A_1$)', '($A_1$)').replace('($A_2$) ($A_2$)', '($A_2$)')
result=result.replace('All payoffs are expressed in thousands of dollars.', 'All payoffs and EMVs are in thousand USD.')
result=result.replace('thousand dollars', 'thousand USD')
result=result.replace('EV(', 'EMV(').replace('EMMV(', 'EMV(')
result=result.replace('Expected Value criterion','Expected Monetary Value criterion')
result=result.replace('expected value of', 'EMV of')
# Small local adjustments to inherited equations that exceed a column.
result=result.replace(r'\underline{\hspace{4cm}}',r'\underline{\hspace{3cm}}')
result=result.replace(r'\longrightarrow \qquad \boxed{',r'\boxed{')
target=root / 'G10_T1_L1_C6C7_classroom_activityV2.tex'
target.write_text(result,encoding='utf-8')
assert source.read_bytes()==original
print('Created',target)
print('Original SHA256',hashlib.sha256(original).hexdigest())
