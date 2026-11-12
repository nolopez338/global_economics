exec(open('tmp/highlight-audit/update.py',encoding='utf-8').read().split('for p in (slides, practice):')[0])
import difflib,json
for p in (slides,practice):
    old=(root/'tmp/highlight-audit'/('original-'+p.name)).read_text(encoding='utf-8')
    new=p.read_text(encoding='utf-8')
    pos=0; count=0
    while (m:=hl.search(new,pos)):
        e=endgroup(new,m.end()-1);body=new[m.end():e-1]
        assert not hl.search(body),(p.name,body)
        assert '&' not in body and '\\\\' not in body,(p.name,body)
        if m[0].startswith('\\GTenHLProbability'):
            assert not re.search(r'[=<>+]|\\(?:leq|geq|in)(?![A-Za-z])',body),(p.name,body)
        pos=e;count+=1
    # Compare contents after erasing wrappers; review every remaining difference.
    d=list(difflib.unified_diff(unmark(old).splitlines(),unmark(new).splitlines(),n=0))
    (root/'tmp/highlight-audit'/('content-diff-'+p.stem+'.txt')).write_text('\n'.join(d),encoding='utf-8')
    print(p.name, count,'markers; unwrapped diff:','\n'.join(d))
