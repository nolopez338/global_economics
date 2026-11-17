from pathlib import Path
import re

p = Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex')
s = p.read_text(encoding='utf-8')
Path('tmp/g11-c2-plain-before.tex').write_text(s, encoding='utf-8')

old = r'Use these exact Type labels: \textbf{Sample statistics} for sample mean $\bar{x}$, sample standard deviation $s$ (only when provided or relevant), sample size $n$, and standard error $\mathrm{SE}$; \textbf{Population parameters} for population mean $\mu$ and population standard deviation $\sigma$; \textbf{Procedure Settings} for confidence level $C$, significance level $\alpha$, tail area $\alpha/2$, and critical value $z^*$. Follow this organizational convention for $n$ and $\mathrm{SE}$.'
new = r'Arrange three contiguous groups in this order: \textbf{Population parameters} (population mean $\mu$, then population standard deviation $\sigma$); \textbf{Sample statistics} (sample mean $\bar{x}$, sample standard deviation $s$ only when provided or relevant, sample size $n$, then standard error $\mathrm{SE}$); \textbf{Procedure Settings} (confidence level $C$, significance level $\alpha$, tail area $\alpha/2$, then critical value $z^*$). Write each exact Type label only on the first row of its group, leave the remaining Type cells blank, and insert a horizontal rule between groups. Follow this organizational convention for $n$ and $\mathrm{SE}$.'
assert old in s
s = s.replace(old,new,1)
old = r'Use the exact Type labels \textbf{Sample statistics} ($\bar{x}$, $s$ only when provided or relevant, $n$, $\mathrm{SE}$), \textbf{Population parameters} ($\mu$, $\sigma$), and \textbf{Procedure Settings} ($\CtwoConfidence{C}$, $\CtwoSignificance{\alpha}$, $\CtwoSignificance{\alpha}/2$, $\CtwoCritical{z^*}$).'
new = r'Arrange three contiguous groups in this order, with rows in the order listed: \textbf{Population parameters} ($\mu$, $\sigma$); \textbf{Sample statistics} ($\bar{x}$, $s$ only when provided or relevant, $n$, $\mathrm{SE}$); \textbf{Procedure Settings} ($\CtwoConfidence{C}$, $\CtwoSignificance{\alpha}$, $\CtwoSignificance{\alpha}/2$, $\CtwoCritical{z^*}$). Write each exact Type label once, on the first row of its group; leave subsequent Type cells blank and insert a horizontal rule between groups.'
assert old in s
s=s.replace(old,new,1)

a=s.index(r'\section{General Worked Problems}')
b=s.index(r'\section{Advanced Problems}')
general=s[a:b]

start=general.index('    A city takes')
end=general.index(r'\end{minipage}',start)
general=general[:start]+r'''    A city chooses 100 market stalls by chance to estimate the mean weekly stall fee across the city. The sample mean is 106 thousand COP, and the known population standard deviation is about 25.51 thousand COP. Assume that one stall's fee does not influence another's and that averages from fresh samples of 100 stalls follow a balanced bell shape: averages near the population mean are most common, with averages farther above or below it becoming equally less common. The city uses 95\% confidence. Its suggested lower and upper fees extend equally below and above the sample mean by 1.960 times the spread of averages across fresh samples of 100 stalls.

    The diagram shows the suggested lower and upper fees at 95\% confidence from five separately generated samples of 100 stalls each. These come from an imagined market whose population mean stays at 104 thousand COP, with the same population standard deviation. These samples are separate from the city's original sample. The dashed line marks that mean; each horizontal line joins the suggested lower and upper fees from one fresh sample.
''' + general[end:]

start=general.index('A utility takes')
end=general.index(r'\QuestionsTasks',start)
general=general[:start]+r'''A utility chooses 100 household accounts by chance from one billing month. Both reports use this same sample, whose mean bill is 120 thousand COP. The known population standard deviation is 38 thousand COP. Assume that one household's bill does not influence another's and that averages from fresh samples of 100 accounts follow a balanced bell shape: averages near the population mean are most common, with averages farther above or below it becoming equally less common. Each report suggests lower and upper bills equally far below and above the sample mean. The table gives the confidence used and how many times the spread of averages across fresh samples to extend on each side. Task 1 also asks you to record the significance for each report and share it equally between the lower and upper sides.

\begin{center}
\begin{tabular}{@{}lcc@{}}
    \toprule
    Confidence & How many times the spread & \shortstack{Distance from lower to upper bill\\(thousand COP)} \\
    \midrule
    90\% & 1.645 & \\
    99\% & 2.576 & \\
    \bottomrule
\end{tabular}
\end{center}

The reports give the lower and upper bills to the nearest thousand COP. The stated confidence applies before the amounts are changed for reporting.

In a separate, imagined exercise, the population mean stays at 120 thousand COP and the population standard deviation is again 38 thousand COP. Individual bills follow a balanced bell shape, with bills near the mean most common and bills farther above or below it equally less common. The utility generates 100 fresh samples of 100 accounts each. For each fresh sample, it uses both 90\% and 99\% confidence and the numbers in the table to suggest lower and upper bills, keeping every digit. In 11 of the 100 suggestions at 90\% confidence, the fixed population mean falls outside the suggested lower and upper bills; at 99\% confidence, this happens in 2 of the 100 suggestions. The utility checks whether the mean lies between the suggested bills before changing the amounts for reporting, and checks each confidence separately. These generated samples are separate from the original household sample.


''' + general[end:]

start=general.index('A transit agency takes')
end=general.index(r'\QuestionsTasks',start)
general=general[:start]+r'''A transit agency chooses 36 weekday passenger trips by chance on one bus route. Their sample mean is 34 minutes. Assume that one trip's time does not influence another's and that trip times follow a balanced bell shape: times near the population mean are most common, with times farther above or below it becoming equally less common. The known population standard deviation is 12 minutes. The agency uses 90\% confidence. Its suggested lower and upper times extend equally below and above the sample mean by 1.645 times the spread of averages across fresh samples of 36 trips. The significance is the part left over from the chosen confidence.

To study this approach, the agency generates 20 fresh samples of 36 trips each from an imagined population with a mean that stays at 35 minutes and the same standard deviation. Trip times again follow the balanced bell shape described above. These generated samples are separate from the original passenger sample. The table groups the fresh samples by the order in which they were generated and counts how often 35 minutes lies between the suggested lower and upper times at 90\% confidence.

\begin{center}
\begin{tabular}{@{}lcccc@{}}
    \toprule
    Samples in order & 1--5 & 6--10 & 11--15 & 16--20 \\
    \midrule
    Suggestions with 35 minutes between their ends & 5 & 4 & 3 & 5 \\
    \bottomrule
\end{tabular}
\end{center}

''' + general[end:]

start=general.index('A repair cooperative takes')
end=general.index(r'\QuestionsTasks',start)
general=general[:start]+r'''A repair cooperative chooses 64 completed appliance repairs by chance from a specified month. This one sample has a mean repair time of 50 minutes. Assume that one repair's time does not influence another's and that repair times follow a balanced bell shape: times near the population mean are most common, with times farther above or below it becoming equally less common. The known population standard deviation is 16 minutes. Use this same sample to suggest lower and upper repair times at exactly three choices of confidence: 90\%, 95\%, and 99\%. Extend equally below and above the sample mean by 1.645, 1.960, and 2.576 times the spread of averages across fresh samples of 64 repairs, respectively. Keep the sample mean, the 64 repairs, the population standard deviation, and the spread of averages across fresh samples the same for all three choices. Keep every digit when working out the times and writing their lower and upper ends.

In a separate, imagined exercise, repair times in a population follow the balanced bell shape described above, with a mean that stays at 51 minutes and the same standard deviation of 16 minutes. From each of 200 fresh samples of 64 repairs, three suggestions are made, one at each confidence, keeping every digit. Each suggestion extends equally below and above that fresh sample's own mean. Each sample appears in exactly one row of the table, according to which suggestions have the fixed population mean between their lower and upper times. These generated samples are separate from the cooperative's original sample.

\begin{center}
\begin{tabular}{@{}lr@{}}
    \toprule
    What happens to the three suggestions from one fresh sample & Number of samples \\
    \midrule
    All three have the fixed population mean between their ends & 178 \\
    Only those at 95\% and 99\% confidence have it between their ends & 12 \\
    Only the one at 99\% confidence has it between its ends & 7 \\
    None of the three has it between its ends & 3 \\
    \bottomrule
\end{tabular}
\end{center}

''' + general[end:]

def regroup(m):
    rows=m.group(1).strip().splitlines()
    assert len(rows)==9
    # Preserve every cell except repeated Type labels; move whole rows.
    rows=[rows[i] for i in [0,3,1,2,8,4,5,6,7]]
    out=[]
    for i,row in enumerate(rows):
        cells=row.split(' & ')
        assert len(cells)==4
        if i not in (0,2,5):
            cells[2]=''
        if i in (2,5):
            out.append(r'    \midrule')
        out.append('    '+' & '.join(cells).strip())
    return '\\InformationTable{\n'+'\n'.join(out)+'\n}'
general,n=re.subn(r'\\InformationTable\{\n(.*?)\n\}',regroup,general,flags=re.S)
assert n==4
s=s[:a]+general+s[b:]
p.write_text(s,encoding='utf-8')
print('Updated four descriptions, four grouped tables, and two instructions.')
