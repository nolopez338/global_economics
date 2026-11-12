exec(open('tmp/highlight-audit/update.py',encoding='utf-8').read().split('for p in (slides, practice):')[0])
for p in (slides,practice):
    s=p.read_text(encoding='utf-8')
    s=s.replace('Outcome/event probabilities and PMF expressions; no units. Relations stay unmarked.',
                'Probability expressions and PMF masses, without units.')
    # Keep padding local; the shared palette and renderer remain unchanged.
    toggle='% \\GTenHighlightsfalse % Uncomment to disable instructional highlights.'
    s=s.replace(toggle,toggle+'\n% Compact markers keep dense notation aligned within the existing layout.\n'+r'\tikzset{gten marker/.append style={inner xsep=.6mm,inner ysep=.3mm}}')
    # Relations adjacent to digits still belong outside the probability marker.
    def split_rel(m):
        content=m[1]
        parts=re.split(r'(\\(?:leq|geq|in|le|ge)(?![a-zA-Z])|[=<>+])',content)
        return ''.join(part if i%2 else wrap('Probability',part) for i,part in enumerate(parts) if part)
    s=re.sub(r'\\GTenHLProbability\{(P\([^{}]*\))\}',split_rel,s)
    if p==practice:
        original=(root/'tmp/highlight-audit'/('original-'+p.name)).read_text(encoding='utf-8')
        graph_lines=[l for l in original.splitlines() if l.startswith('\\GTen') and 'Graph[' in l]
        idx=0; result=[]
        for line in s.splitlines():
            if line.startswith('\\GTen') and 'Graph[' in line:
                old=graph_lines[idx];idx+=1
                # Graph data/category lists are rendered by the graph's own role styling.
                line=line[:line.index(']{')]+old[old.index(']{'):]
            result.append(line)
        s='\n'.join(result)+'\n'
    p.write_text(s,encoding='utf-8')
