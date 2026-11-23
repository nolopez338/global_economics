from pathlib import Path
p=Path('tmp/solution-context-review/check-pdf.py')
s=p.read_text()
s=s.replace("s=Path(","aux=(root/'disabled/disabled.aux').read_text()\ndestinations={m[1]:m[2] for m in re.finditer(r'\\\\newlabel\\{([^}]+)\\}[^\\n]*?\\{(section[^}]+)\\}\\{\\}\\}',aux)}\ns=Path(")
s=s.replace('label in r.named_destinations','destinations[label] in r.named_destinations').replace('r.named_destinations[label]','r.named_destinations[destinations[label]]').replace("r.named_destinations[f'sol:p{i}c2a']","r.named_destinations[destinations[f'sol:p{i}c2a']]")
p.write_text(s)
