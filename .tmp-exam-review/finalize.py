from pathlib import Path
import re,subprocess
p=Path('book2026-2027/grade11/term_1/3-learning_evidences/G11_T1_L1_C1C2C3C4_examV2_solution.tex')
s=p.read_text(encoding='utf-8')
old=subprocess.check_output(['git','show','HEAD:'+p.as_posix()]).decode('utf-8')
oldnav=list(re.finditer(r'\\QuestionsTasks\{\s*\{([^}]+)\}',old))
# Keep the original navigation identifiers and subsection headings.
matches=list(re.finditer(r'\\QuestionsTasks\{\s*\{([^}]+)\}',s))
for i,m in reversed(list(enumerate(matches))):
    s=s[:m.start(1)]+oldnav[i].group(1)+s[m.end(1):]
for label,title in [
('subsec:c4-find-rate-orders','C4.9 - Number of orders'),
('subsec:c4-find-rate-economic-update','C4.9 - Average number of updates per minute'),
('subsec:c4-compare-rates-economic','C4.10 - Comparing detection rates'),
('subsec:c4-exponential-50-percent-interval','C4.10 - Finding a 50\\% probability interval')]:
    s=s.replace('\\label{'+label+'}', '\\label{'+label+'}\n\t\t\\subsection*{'+title+'}',1)
s=s.replace('\\label{subsec:identifying-probability-distributions-c1-solution}', '\\label{subsec:identifying-probability-distributions-c1-solution}\n\t\t\\label{subsec:identifying-probability-distributions-c1-characterization}')
# Put each task solely in the existing navigation wrapper, preserving its words.
parts=list(re.finditer(r'\\sectionScored\s*\n',s))
for i,m in reversed(list(enumerate(parts[:12]))):
    end=s.index('\\QuestionsTasks',m.end())
    block=s[m.start():end]
    if i==0:
        task='For each context, characterize the random variable and identify the appropriate probability distribution.'
        block=block.replace(task,'',1)
    else:
        key='On average,' if i==8 else 'Find the average' if i==9 else 'From the moment' if i==11 else 'Determine'
        block=block[:block.index(key)].rstrip()+'\n\n\t\t'
    s=s[:m.start()]+block+s[end:]
s=s.replace('\\text{ by }\\frac{1}{60}\\approx0.0167.', '\\text{ by }\\frac{1}{60}\\text{ (1.67 percentage points)}.')
s=s.replace('The density decreases\n\t\tlinearly', 'Under the intended linear model, the density decreases\n\t\tlinearly')
s=s.replace('The random variable \\(X\\) has support', 'The random variable \\(X\\) has support',1)
s=s.replace('Its density rises linearly to a peak', 'Under the intended triangular model, its density rises linearly to a peak',1)
# Explicitly report ambiguities in the original wording of the density problems.
s=s.replace('Let the endpoint heights be \\(2h\\) and \\(h\\).',r'''Let the endpoint heights be \(2h\) and \(h\).
        Here ``twice as common'' must refer to density: exact values of a
        continuous random variable each have probability zero. Also, ``steadily''
        does not mathematically specify linearity; without that intended model,
        the probability is not uniquely determined.''')
s=s.replace('Let the peak height be \\(H\\).',r'''Let the peak height be \(H\).
        The words ``steadily'' and ``no observations exactly at either limit''
        do not by themselves establish straight segments or zero endpoint
        density. Thus the numerical answer uses the intended triangular model;
        the literal statement alone does not uniquely determine it.''')
s=s.replace('Context & Class. & Distribution & Context & Class. & Distribution', 'Context & Class. & Distribution & Context & Class. & Distribution')
s=s.replace('\\subsection{Identifying Probability Distributions from Contexts \\hfill C1--5}', '\\subsection{Identifying Probability Distributions from Contexts \\hfill C1--5}\n\t\tThese are candidate models subject to the qualifications in the detailed solution.')
s=s.replace('\\subsection{Charging Time for an Electric Vehicle \\hfill C2--3}', '\\subsection{Charging Time for an Electric Vehicle \\hfill C2--3}\n\t\tUnder the intended linear model:')
s=s.replace('\\subsection{Daily Sales Revenue of a Local Business \\hfill C2--4}', '\\subsection{Daily Sales Revenue of a Local Business \\hfill C2--4}\n\t\tUnder the intended triangular model:')
p.write_text(s,encoding='utf-8')
print('Restored navigation, removed repeated tasks, documented model ambiguities.')
