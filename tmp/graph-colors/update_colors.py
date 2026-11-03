from pathlib import Path
import re

p = Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex')
text = p.read_text(encoding='utf-8')
# Each entry follows its local explanation, including the second/third variables.
roles = ['Value','Value','Second','Third','Value','Second','Third',
         'Value','Value','Value','Value','Value','Value','Value','Value',
         'Second','Value','Value','Value','Value','Value','Value','Value',
         'Value','Second','Value','Second']
i = 0
def update(m):
    global i
    kind, opts, data = m.groups()
    role = roles[i]
    i += 1
    is_value = kind == 'OutcomeValue'
    is_pmf = kind == 'PMF'
    xrole = role if is_pmf else 'Outcome'
    yrole = role if is_value else 'Probability'
    def axis_label(a):
        name, content = a.groups()
        r = xrole if name == 'xlabel' else yrole
        if r'\omega' in content:
            content = re.sub(r'\$([XYZBI])\(\\omega\)\$ (.*)',
                lambda v: '$\\GTenHL'+r+'{'+v[1]+'}(\\GTenHLOutcome{\\omega})$ '
                    +'\\GTenHL'+r+'{'+v[2]+'}', content)
        elif ', continuing' in content:
            first, rest = content.split(', continuing', 1)
            content = '\\GTenHL'+r+'{'+first+'}, continuing'+rest
        else:
            content = '\\GTenHL'+r+'{'+content+'}'
        return name+'={'+content+'}'
    opts = re.sub(r'(xlabel|ylabel)=\{(.*?)\}(?=,|$)', axis_label, opts)
    if not is_pmf:
        opts += r',xlabel={\GTenHLOutcome{Outcome}}'
    if not is_value:
        opts += r',ylabel={\GTenHLProbability{Probability}}'
    opts += ',xhighlight=GTenHL'+xrole+',yhighlight=GTenHL'+yrole+',color=GTenHL'+yrole+'!32'
    return '\\GTen'+kind+'Graph['+opts+']'+data

text = re.sub(r'\\GTen(OutcomeProbability|OutcomeValue|PMF)Graph\[([^\]]*)\](.*)', update, text)
assert i == len(roles) == 27
text = text.replace(r'\input{graphs/G10_T2_bar_graphs.tex}', r'''\input{graphs/G10_T2_bar_graphs.tex}
% Graph markers follow the local written roles: outcomes on category labels;
% variable values on numerical ticks; bar fills and height labels follow the
% vertical quantity (blue for probabilities, the variable marker for values).
% Grouped PMFs keep probability blue; axis labels and captions identify units.''')
p.write_text(text, encoding='utf-8', newline='\n')
