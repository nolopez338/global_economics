exec(open('tmp/highlight-audit/update.py',encoding='utf-8').read().split('for p in (slides, practice):')[0])
s=practice.read_text(encoding='utf-8').replace(r'\GTenHLThird{c}',r'\GTenHLParameter{c}')
s=s.replace(r'2\GTenHLParameter{c}',r'\GTenHLParameter{2c}').replace(r'3\GTenHLParameter{c}',r'\GTenHLParameter{3c}').replace(r'6\GTenHLParameter{c}',r'\GTenHLParameter{6c}')
# The powers in the telescoping check are probability masses, not trial counts.
start=s.index('All masses are positive. To check their sum')
end=s.index('The graphs use Version 1.',start)
chunk=unmark(s[start:end])
chunk=re.sub(r'2\^\{(?:[^{}]|\{[^{}]*\})*\}',lambda m:wrap('Probability',m[0]),chunk)
# Mark free trial/partial-sum indices, keeping the blue atoms protected.
chunk=re.sub(r'\$m\$',lambda m:'$'+wrap('Value','m')+'$',chunk)
chunk=chunk.replace(r'\sum_{t=1}^{m}',r'\sum_{\GTenHLValue{t}=1}^{\GTenHLValue{m}}')
s=s[:start]+chunk+s[end:]
s=s.replace(r'$1-2^{-m}$',r'$1-\GTenHLProbability{2^{-m}}$').replace('$m$',r'$\GTenHLValue{m}$')
s=s.replace('All masses are positive and the first $\\GTenHLValue{m}$ terms', 'All masses are positive and the first $\\GTenHLValue{m}$ terms')
# Existing numerical factors in the diagnostic are probabilities too.
s=s.replace(r'=0.4\times0.6\times0.6$',r'=\GTenHLProbability{0.4}\times\GTenHLProbability{0.6}\times\GTenHLProbability{0.6}$')
s=s.replace('The only negative bonus is $-3$ USD.',r'The only negative bonus is $\GTenHLValue{-3}$ \GTenHLValue{USD}.')
practice.write_text(s,encoding='utf-8')
s=slides.read_text(encoding='utf-8')
s=s.replace(r'$0.28+0.31=\GTenHLProbability{0.59}$',r'$\GTenHLProbability{0.28}+\GTenHLProbability{0.31}=\GTenHLProbability{0.59}$')
slides.write_text(s,encoding='utf-8')

# Build disabled copies without touching either original toggle.
for p in (slides,practice):
    s=p.read_text(encoding='utf-8')
    assert s.count('% \\GTenHighlightsfalse % Uncomment')==1
    dest=root/'tmp/highlight-audit'/('disabled-'+p.name)
    dest.write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'),encoding='utf-8')
