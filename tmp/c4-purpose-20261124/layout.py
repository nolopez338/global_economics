from pathlib import Path
import re
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex')
s=p.read_text(encoding='utf-8')
s=s.replace('The inverse tasks help you check how the C4 interval is constructed.','The report audits help you check how the C4 interval is constructed.')
# Moderate positive display spacing keeps full derivations and their decisions together.
for i in (1,2,3):
    for letter in ('a','c'):
        label=f'\\label{{sol:c4-{i}-{letter}}}'
        a=s.index(label)+len(label); b=s.index('\\secInicio',a)
        s=s[:b]+'\\endgroup\n'+s[b:]
        s=s[:a]+'\n\\begingroup\n\\setlength{\\abovedisplayskip}{6pt}\n\\setlength{\\belowdisplayskip}{6pt}\n\\setlength{\\abovedisplayshortskip}{3pt}\n\\setlength{\\belowdisplayshortskip}{4pt}\n\\setlength{\\parskip}{4pt}\n'+s[a:]
s=s.replace('For each supplied confidence level, $z^*\\approx\\Phi^{-1}((1+C)/2)$.\nUse the supplied cutoffs in the numerical calculations. The formulas are','Use $z^*\\approx\\Phi^{-1}((1+C)/2)$ with the supplied numerical cutoffs. The formulas are')
s=re.sub(r'Every interval remains centered at .*?an actual new sample could have a different sample mean\.\n','',s,flags=re.S)
s=s.replace('The normal-based construction is $[L,U]=[\\bar x-z^*\\sigma/\\sqrt n,\\bar x+z^*\\sigma/\\sqrt n]$, using the population spread known to the analyst, not a spread estimated from this sample.', 'The analyst used the normal interval $[L,U]=[\\bar x-z^*\\sigma/\\sqrt n,\\bar x+z^*\\sigma/\\sqrt n]$ with known population spread $\\sigma$.')
for i,u,units in [(1,'thousand COP','couriers'),(2,'USD per pallet','pallets'),(3,'USD per shipment','shipments')]:
    a=s.index(f'\\label{{sol:c4-{i}-c}}'); b=s.index('\\par\\noindent',a)
    part=s[a:b]
    part=re.sub(r'Each report estimates .*?The recovered',f'All monetary calculations below are in {u}; $n$ counts {units}. The recovered',part,flags=re.S)
    s=s[:a]+part+s[b:]
# Begin Stage 3 on its own question page, rather than split a narrative report.
for i in (1,2,3):
    marker='},\n{4}/{sol:c4-'+str(i)+'-c}'
    s=s.replace(marker,'}\n}\n\\clearpage\n\\QuestionsTasks[sec:general-worked]{\n{4}/{sol:c4-'+str(i)+'-c}',1)
p.write_text(s,encoding='utf-8')
