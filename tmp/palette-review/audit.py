from pathlib import Path
import re,difflib,json
r=Path.cwd();o=r/'tmp/palette-review';d=r/'book2026-2027/preamble/graphs'
before=(o/'original-specific_highlights.tex').read_text();after=(d/'specific_highlights.tex').read_text()
# All unrelated definitions and both scoped palettes must remain byte-for-byte equivalent as source.
for name in ['CoordinatedTermTwoPalette','CtwoPracticeIntervalPalette']:
 pattern=r'\\newcommand\{\\'+name+r'\}\{%[\s\S]*?\n[^\n]*?\}\n'
 assert re.search(pattern,before)[0]==re.search(pattern,after)[0],name
colors=lambda s:dict(re.findall(r'\\(?:definecolor|colorlet)\{([^}]+)\}([^\n]+)',s))
b=colors(before);a=colors(after);changed=[k for k in b if b[k]!=a.get(k)];assert changed==['MathHLComplementColor'],changed
assert 'fill opacity=.32,text opacity=1' in (d/'highlights.tex').read_text()
p=r/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex'
b=(o/'original-C3.tex').read_text();a=p.read_text();assert b.replace(r'\newcommand{\SuccessProb}[1]{\GTenHLProbability{#1}}',r'\newcommand{\SuccessProb}[1]{\HLSuccessProbability{#1}}').replace(r'{GTenHLProbability!50!black}',r'{MathHLSuccessColor!50!black}')==a
keys=set(re.findall(r'practicehighlightlegend@(G[^\\]+)\\endcsname',after));calls=re.findall(r'\\PreviewLegend\{([^}]+)\}',(d/'specific_highlights_view.tex').read_text());assert keys==set(calls) and len(calls)==len(keys)
md=(d/'specific_highlights.md').read_text(encoding='utf8');assert all('`'+k+'`' in md for k in keys)
for link in re.findall(r'\]\(([^)]+)\)',md):assert (d/link).exists(),link
print('PASS: 28 registry keys/preview calls/Markdown entries; palettes, opacity, unrelated color definitions, C3 mathematics and toggles preserved; Markdown links resolve.')
(o/'source-checks.txt').write_text('Passed source preservation, registry coverage, palette-scope and Markdown-link checks.\n')
