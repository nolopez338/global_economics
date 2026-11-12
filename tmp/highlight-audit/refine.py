exec(open('tmp/highlight-audit/update.py',encoding='utf-8').read().split('for p in (slides, practice):')[0])

for p in (slides,practice):
    s=p.read_text(encoding='utf-8')
    # Flatten math-in-text markers in captions and labels without changing roles.
    pos=0; out=''
    while (m:=hl.search(s,pos)):
        e=endgroup(s,m.end()-1)
        out+=s[pos:m.end()]+unmark(s[m.end():e-1])+'}'
        pos=e
    s=out+s[pos:]
    s=s.replace('The chance of an outcome or event, expressed without units.',
                'Outcome/event probabilities and PMF expressions; no units. Relations stay unmarked.')
    if p==slides:
        s=s.replace(r'$\GTenHLProbability{P(\omega)}$, $\GTenHLProbability{P(X}=\GTenHLProbability{x)}$;\newline',
                    r'$\GTenHLProbability{P(\omega)}$, $\GTenHLProbability{p_X(x)}$;\newline')
    else:
        s=s.replace(r'$\GTenHLProbability{P(X}=\GTenHLProbability{x)}$, $\GTenHLProbability{p_{X}(x)}$',
                    r'$\GTenHLProbability{p_X(x)}$, $\GTenHLProbability{q_i}$')
    # Probability powers are short atoms, not merely a highlighted base.
    s=re.sub(r'\\GTenHLProbability\{(0\.[0-9]+)\}\^([23])',r'\\GTenHLProbability{\1^\2}',s)
    s=s.replace(r'\GTenHLProbability{p_{',r'\GTenHLProbability{p_{')
    p.write_text(s,encoding='utf-8')

# Missing masses remain parameters while unknown; normalize their algebra.
s=practice.read_text(encoding='utf-8')
s=s.replace('$q$',r'$\GTenHLParameter{q}$').replace('$c$',r'$\GTenHLParameter{c}$')
s=s.replace('$c+2c+3c=6c=1$',r'$\GTenHLParameter{c}+\GTenHLParameter{2c}+\GTenHLParameter{3c}=\GTenHLParameter{6c}=1$')
# Role-specific values in text, preserving the original text and arithmetic.
replacements={
    r'at 0 and $\GTenHLProbability{0.400}$ at 1': r'at \GTenHLThird{0} and $\GTenHLProbability{0.400}$ at \GTenHLThird{1}',
    'The diagnostic product describes BNN:': r'The diagnostic product describes \GTenHLOutcome{BNN}:',
    'BNN and NBN both give one buyer and 5 USD.': r'\GTenHLOutcome{BNN} and \GTenHLOutcome{NBN} both give one buyer and \GTenHLSecond{5 USD}.',
    'only BNN starts': r'only \GTenHLOutcome{BNN} starts',
    'where B means buying a notebook and N means not buying.': r'where \GTenHLOutcome{B} means buying a notebook and \GTenHLOutcome{N} means not buying.',
    'select exactly BBN, BNB, and NBB,': r'select exactly \GTenHLOutcome{BBN}, \GTenHLOutcome{BNB}, and \GTenHLOutcome{NBB},',
    'that begin with B.': r'that begin with \GTenHLOutcome{B}.',
    'For BB, BN, NB, and NN in order,': r'For \GTenHLOutcome{BB}, \GTenHLOutcome{BN}, \GTenHLOutcome{NB}, and \GTenHLOutcome{NN} in order,',
    'The outcomes S, FS, FFS, and so on': r'The outcomes \GTenHLOutcome{S}, \GTenHLOutcome{FS}, \GTenHLOutcome{FFS}, and so on',
    '$1,2,3,\\ldots$': r'$\GTenHLValue{1,2,3,\ldots}$',
    '$0.216+0.432+0.288+0.064=1$': r'$\GTenHLProbability{0.216}+\GTenHLProbability{0.432}+\GTenHLProbability{0.288}+\GTenHLProbability{0.064}=1$',
}
for a,b in replacements.items(): s=s.replace(a,b)
# Numbers in simple assignments outside probability expressions follow variable roles.
for role in ('Value','Second','Third'):
    s=re.sub(r'(\\GTenHL'+role+r'\{[A-Z]\}=)(-?\d+)(?![\d.])',lambda m:m[1]+wrap(role,m[2]),s)
practice.write_text(s,encoding='utf-8')
