from pathlib import Path
import re, textwrap
root=Path('tmp/g10-c2-format-check')
s=(root/'before.tex').read_text(encoding='utf-8')
# Preserve paragraph boundaries and every original token. A percent at each
# newly inserted structural break prevents TeX from creating a space token.
commands=r'par|noindent|Needspace|addvspace|nopagebreak|begin|end|hfill|toprule|midrule|bottomrule|hline|setlength|foreach|endgroup|vspace|rule|hrulefill'
lines=[]
for line in s.splitlines():
    # Existing comments are retained verbatim.
    m=re.search(r'(?<!\\)%',line)
    code=line[:m.start()] if m else line
    comment=line[m.start():] if m else ''
    code=re.sub(r'(?<=[^\s])(?=\\(?:'+commands+r')\b)', '%\n', code)
    # Split graph key/value lists only after commas outside nested braces.
    chunks=[]
    depth=0
    for char in code:
        chunks.append(char)
        if char=='{': depth+=1
        elif char=='}': depth-=1
        elif char==',' and ('\\begin{axis}' in line or '\\GTenPMFGraph[' in line or '\\pgfplotsset' in line or '\\blankgraph' in line):
            # Main graph options are at depth 0 (or depth 2 for a style).
            level=2 if '\\pgfplotsset' in line else (1 if '\\newcommand' in line else 0)
            if depth==level: chunks.append('%\n')
    code=''.join(chunks)
    parts=code.splitlines()
    if comment:
        if parts: parts[-1]+=comment
        else: parts=[comment]
    for part in parts or ['']:
        # Replace existing inter-word spaces with newlines; never split tokens.
        if len(part)>110 and not part.lstrip().startswith('%'):
            wrapped=textwrap.wrap(part,width=110,break_long_words=False,break_on_hyphens=False,replace_whitespace=False,drop_whitespace=True)
            lines.extend(wrapped)
        else: lines.append(part)
(root/'structured.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'format.yaml').write_text('defaultIndent: "  "\nindentPreamble: 1\nlookForAlignDelims:\n  tabular: 0\n  tabularx: 0\n',encoding='utf-8')
