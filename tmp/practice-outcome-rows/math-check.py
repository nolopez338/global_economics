from pathlib import Path
from fractions import Fraction
from collections import defaultdict
ns={}
exec(Path('tmp/practice-outcome-rows/edit.py').read_text().split('for key,rows in data.items():')[0],ns)
expected={
'fees':{0:'0.1',1:'0.5',2:'0.4'},'bike':{0:'0.1',1:'0.5',2:'0.4'},'recycling':{0:'0.1',2:'0.35',5:'0.35',9:'0.2'},'claims':{0:'0.25',2:'0.2',4:'0.3',6:'0.25'},'notebooks':{0:'0.125',5:'0.375',10:'0.375',12:'0.125'},'investment':{-4:'0.12',0:'0.38',4:'0.2',6:'0.18',10:'0.12'},'refund':{0:'1/6',2:'1/3',5:'1/2'},'prize':{0:'1/35',2:'6/35',4:'3/35',5:'6/35',10:'19/35'},'maintenance':{0:'28/128',1:'27/128',3:'9/128',4:'9/128',5:'1/128',6:'54/128'}}
for k,rows in ns['data'].items():
 totals=defaultdict(Fraction)
 for w,pr,x in rows:totals[int(x)]+=Fraction(pr)
 assert dict(totals)=={x:Fraction(v) for x,v in expected[k].items()}, k
 assert len({w for w,pr,x in rows})==len(rows)
print('PASS: all nine finite outcome tables have unique outcomes and aggregate exactly to the existing PMFs.')
