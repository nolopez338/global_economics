from pathlib import Path
import re, shutil

root = Path.cwd()
slides = root/'book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C1_slides.tex'
practice = root/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex'
hl = re.compile(r'\\GTenHL(?:Value|Second|Third|Outcome|Probability|Parameter)\{')

def endgroup(s, start, op='{', cl='}'):
    depth = 1
    for j in range(start+1, len(s)):
        if s[j] == op and (j == 0 or s[j-1] != '\\'): depth += 1
        if s[j] == cl and (j == 0 or s[j-1] != '\\'):
            depth -= 1
            if depth == 0: return j+1
    raise ValueError(s[start:])

def unmark(s):
    while (m := hl.search(s)):
        e = endgroup(s, m.end()-1)
        s = s[:m.start()] + s[m.end():e-1] + s[e:]
    return s

def wrap(role, s): return '\\GTenHL'+role+'{'+s+'}'

def math(s):
    # Normalize complete probability atoms before protecting existing markers.
    # The relation in an event remains outside the blue fragments.
    s = s.replace(r'\GTenHLProbability{P}(', 'P(').replace(r'\GTenHLProbability{p}_', 'p_')
    pat = re.compile(r'(?<![A-Za-z\\])(?:P\(|p_(?:\{(?:[^{}]|\{[^{}]*\})*\}|[A-Z])\()')
    pos = 0
    while (m := pat.search(s, pos)):
        e = endgroup(s, m.end()-1, '(', ')')
        atom = unmark(s[m.start():e])
        pieces = re.split(r'(\\(?:leq|geq|in|le|ge)\b|[=<>+]|\\cap\b)', atom)
        marked = ''.join(p if i%2 else wrap('Probability', p) for i,p in enumerate(pieces) if p)
        s = s[:m.start()] + marked + s[e:]
        pos = m.start()+len(marked)
    saved = []
    def protect(m):
        e = endgroup(s, m.end()-1)
        return e
    # Hide marked fragments and text commands; never nest wrappers.
    pattern = re.compile(r'\\(?:GTenHL(?:Value|Second|Third|Outcome|Probability|Parameter)|text|mathrm|textbf|phantom)\{')
    pos = 0; out = ''
    while (m := pattern.search(s, pos)):
        e = protect(m)
        out += s[pos:m.start()] + f'§{len(saved)}§'
        saved.append(s[m.start():e]); pos=e
    s = out+s[pos:]
    s = re.sub(r'\\(?:omega|Omega)(?:_(?:\{[^{}]*\}|[a-z0-9]))?', lambda m: wrap('Outcome',m[0]), s)
    s = re.sub(r'(?<![A-Za-z\\])q_(?:\{[^{}]*\}|[a-z0-9])', lambda m: wrap('Probability',m[0]), s)
    roles = {'X':'Value','x':'Value','F':'Value','f':'Value','T':'Value','t':'Value','G':'Value','g':'Value','B':'Value','b':'Value','S':'Value','Y':'Second','y':'Second','E':'Second','e':'Second','D':'Second','I':'Second','Z':'Third','z':'Third','C':'Third','c':'Third'}
    def variable(m):
        token = m[0]; role = roles[token[0]]
        if token.startswith('S_'):
            sub = token[2:].strip('{}'); role=roles.get(sub,'Value')
        return wrap(role,token)
    s = re.sub(r'(?<![A-Za-z\\])(?:S_[XYZFECBTGI]|[XxFfTtGgBbSYyEeDIZzCc](?:_(?:\{[^{}]*\}|[a-z0-9]))?)(?![A-Za-z])', variable, s)
    # Restore protected fragments (new wrappers never contain a placeholder).
    s = re.sub(r'§(\d+)§', lambda m:saved[int(m[1])], s)
    return s

def transform(s):
    # Math spans only, including display environments and graph-label math.
    pattern = re.compile(r'(?<!\\)\$(.*?)(?<!\\)\$|\\\[(.*?)\\\]', re.S)
    return pattern.sub(lambda m: '$'+math(m[1])+'$' if m[1] is not None else '\\['+math(m[2])+'\\]', s)

for p in (slides, practice):
    shutil.copy2(p, root/'tmp/highlight-audit'/('original-'+p.name))

s=slides.read_text(encoding='utf-8')
start=s.index(r'\begin{frame}[t]{General model: Mapping, PMF and checks}')
end=s.index(r'\end{frame}',start)+len(r'\end{frame}')
s=s[:start]+transform(s[start:end])+s[end:]
slides.write_text(s,encoding='utf-8')
# Then audit and propagate across all remaining frames and reusable macros.
# Do not reprocess the already audited frame.
s=s[:start]+s[start:end]+s[end:] if False else slides.read_text(encoding='utf-8')
start=s.index(r'\begin{frame}[t]{General model: Mapping, PMF and checks}')
end=s.index(r'\end{frame}',start)+len(r'\end{frame}')
s=transform(s[:start])+s[start:end]+transform(s[end:])
slides.write_text(s,encoding='utf-8')
practice.write_text(transform(practice.read_text(encoding='utf-8')),encoding='utf-8')
