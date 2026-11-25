from pathlib import Path
p=Path('tmp/g10-solution-update/edit.py')
s=p.read_text().replace("probability=('P(' in x", "x=re.sub(r'\\\\binom([0-9A-Za-z])([0-9A-Za-z])',r'\\\\binom{\\1}{\\2}',x)\n x=re.sub(r'\\\\binom([0-9A-Za-z])(?=\\{)',r'\\\\binom{\\1}',x)\n probability=('P(' in x")
s=s.replace("p.write_text(s)","s=re.sub(r'([\\^_])(\\\\(?:GTenHL\\w+|HLCumulativeProbability)\\{[^{}]*\\})',r'\\1{\\2}',s)\ns=s.replace(r'\\noindent\\textbf{',r'\\noindent\\textbf{\\boldmath ')\np.write_text(s)")
p.write_text(s)
