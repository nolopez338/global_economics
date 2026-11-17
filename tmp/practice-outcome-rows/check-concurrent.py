from pathlib import Path
ns={}
exec(Path('tmp/practice-outcome-rows/check.py').read_text().split('assert strip(a)')[0],ns)
a=ns['strip'](ns['a']);b=ns['strip'](ns['b'])
a=a.replace('Variable | Value | Support of the variable $X$.','Variable | Value | Support of the random variable $X$.',1)
assert a==b
print('PASS: aside from the concurrent legend wording edit, all changes are confined to the 11 PMF rows.')
