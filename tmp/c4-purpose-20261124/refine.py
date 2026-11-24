from pathlib import Path
import re
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex')
s=p.read_text(encoding='utf-8')
for i,c1,c2,n1,n2,z1,z2,pop,unit in [
    (1,95,99,64,256,'1.96','2.576',"the cooperative's mean reference-week earnings",'thousand COP'),
    (2,95,99,36,144,'1.96','2.576',"the importer's mean quarterly charge",'USD per pallet'),
    (3,90,95,81,324,'1.645','1.96',"the insurer's mean processing charge",'USD per shipment')]:
    a=s.index('At each row\'s confidence level',s.index(f'\\label{{sol:c4-{i}-a}}'))
    b=s.index('\\textbf{Practical conclusion.}',a)
    text=f"At each row's stated confidence level, the bounds estimate {pop}, not a range of individual values. With the observed mean and population spread fixed, increasing $n$ from {n1} to {n2} halves width: $\\sqrt{{{n1}/{n2}}}=1/2$. Raising confidence from {c1}\\% to {c2}\\% increases width by $z_2^*/z_1^*={z2}/{z1}\\approx {'1.3143' if i<3 else '1.1915'}$ at either count.\n"
    s=s[:a]+text+s[b:]
# The recovered results and the reconstructions already show every value and unit.
s=re.sub(r'Thus \$\\bar x=([^$]+)\$ (.*?) and the analyst used the positive population SD \$\\sigma=([^$]+)\$ \2\.',r'Recovered: $\\bar x=\1$ and $\\sigma=\3$ \2.',s)
s=s.replace(' The interval estimates $\\mu$, not individual values.','')
old=[
"Report 3 is the priority for the coordinator: its observed average is 430 versus 415 thousand COP and its population spread is 80 versus 60 thousand COP. It combines a higher observed center with greater individual variability. The differing confidence levels and overlapping intervals do not establish an ordering of population means; neither report assigns an earnings range to every courier.",
"Prioritize the warehouse in Report 4: its observed average of 80 USD per pallet exceeds Report 3's 72 USD, and its population spread of 18 USD exceeds 12 USD. These spreads describe individual charges; the averages describe the records' centers. Different confidence levels and overlapping intervals do not prove an ordering of the population means or that every pallet costs more.",
"Prioritize the operation in Report 4: its observed average is 130 versus 122 USD per shipment and its population spread is 32 versus 24 USD. Higher individual variability accompanies its higher observed center. The different confidence levels and overlapping intervals do not prove an ordering of population means or a higher charge on every shipment."]
new=[
"Prioritize Report 3: its observed average is 430 versus 415 thousand COP, and its population spread is 80 versus 60 thousand COP. It has the higher observed center and greater individual variability; these intervals do not prove an ordering of population means or rank every courier's earnings.",
"Prioritize Report 4: its observed average is 80 versus 72 USD per pallet, and its population spread is 18 versus 12 USD. It has the higher observed center and greater individual variability; these intervals do not prove an ordering of population means or rank every pallet charge.",
"Prioritize Report 4: its observed average is 130 versus 122 USD per shipment, and its population spread is 32 versus 24 USD. It has the higher observed center and greater individual variability; these intervals do not prove an ordering of population means or rank every shipment charge."]
for a,b in zip(old,new):
    assert a in s
    s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
