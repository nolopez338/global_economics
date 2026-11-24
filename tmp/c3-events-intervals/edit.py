from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex')
s=p.read_text(encoding='utf-8')
# Protect the already correct event markers before extending the same role.
saved=[]
def protect(m):
    saved.append(m[0]); return f'@@EVENT{len(saved)-1}@@'
s=re.sub(r'\\HLMathEvent\{(?:\\\{Y_i<0\\\}|E\^c|E|Event|Complement|Net-loss event)\}',protect,s)
# A complete condition denotes an event here; its internal symbols are no
# longer standalone indicator values, so avoid nesting the indicator marker.
s=re.sub(r'\\\{\\Indicator\{X\}=\\Indicator\{([01])\}\\\}',r'\\{X=\1\\}',s)
s=re.sub(r'\\\{(?:Y_(?:i|[123])<0|X=[01])\\\}',lambda m:r'\HLMathEvent{'+m[0]+'}',s)
# E in math is the event; the E in \mathbb E remains the expectation operator.
s=re.sub(r'(?<![A-Za-z])E(?:\^c)?(?![A-Za-z])',lambda m:m[0] if s[max(0,m.start()-8):m.start()].endswith('\\mathbb ') else r'\HLMathEvent{'+m[0]+'}',s)
for i,v in enumerate(saved): s=s.replace(f'@@EVENT{i}@@',v)
# All mathematical intervals in this document use these endpoints. This
# deliberately excludes coordinate pairs, supports, and grouping brackets.
endpoint=r'(?:0|1|\\frac\{\d+\}\{\d+\}|p_i\^\*)'
interval=re.compile(r'(?<!\\left)([\[(])('+endpoint+r'),('+endpoint+r')([\])])')
s,n=interval.subn(lambda m:r'\left'+m[1]+m[2]+','+m[3]+r'\right'+m[4],s)
# Names of the two states are provided in the questions already; use the
# same role for both without choosing E or giving any requested loss mapping.
names=['high campus-market attendance','campus-market attendance below its target',
       'a home-internet disruption','home-internet disruption','no disruption',
       'high inquiry volume','low inquiry volume','high enrollment','low enrollment',
       'high demand','low demand','the fair is cancelled','the fair goes ahead',
       'the fair going ahead','its cancellation','the ceremony is cancelled',
       'the ceremony goes ahead','the ceremony going ahead','disruption']
# Restrict prose edits to text outside math and existing commands' arguments
# that contain instructional highlights, while retaining table/link text.
pattern=re.compile('|'.join(re.escape(x) for x in sorted(names,key=len,reverse=True)),re.I)
parts=re.split(r'(\$[^$]*\$|\\HLMathEvent\{[^{}]*\})',s)
for i,part in enumerate(parts):
    if part.startswith('$') or part.startswith('\\HLMathEvent{'): continue
    part=pattern.sub(lambda m:r'\HLMathEvent{'+m[0]+'}',part)
    # Concept names, including headings and reminders, but no command keys.
    part=re.sub(r'(?<![A-Za-z:-])(?:event|events|complement)(?![A-Za-z:-])',lambda m:r'\HLMathEvent{'+m[0]+'}',part)
    parts[i]=part
s=''.join(parts)
p.write_text(s,encoding='utf-8',newline='\r\n')
print('Sized intervals:',n)
