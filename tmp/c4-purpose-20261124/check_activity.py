"""Checks specific to this C4 revision; not a reusable validation library."""
from pathlib import Path
from decimal import Decimal as D
import re,json
s=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex').read_text(encoding='utf-8')
blocks=re.findall(r'\\QuestionsTasks\[.*?\]\{(.*?)\n\}',s,re.S)
assert len(blocks)==8
for block in blocks:
    assert not re.search(r'\$|\\\[|\\(?:bar|sigma|alpha|mu|sqrt)|\[[0-9]|half-width|critical value|invert|normal-based|z procedure',block),block
assert not re.search(r'10\\%|sampling fraction|finite.population|skew|outlier|independence|random sampl|normality|assumptions',s,re.I)
assert s.count('\\textbf{Practical conclusion.}')==9
assert s.count('but omitted that spread from the published report')==6
assert len(re.findall(r'\\subsubsection\*\{C4 -- Stage',s))==9
labels=re.findall(r'\\label\{([^}]+)\}',s)
assert len(labels)==len(set(labels))
forward=[(410,80,[64,256],['1.96','2.576']), (74,12,[36,144],['1.96','2.576']), (120,27,[81,324],['1.645','1.96'])]
results=[]
for mean,spread,counts,zs in forward:
    for n in counts:
        for z in zs:
            se=D(spread)/D(n).sqrt(); e=D(z)*se
            lo=D(mean)-e; hi=D(mean)+e; width=2*e
            for x in (lo,hi):
                assert format(x.normalize(),'f') in s, x
            results.append(dict(mean=mean,spread=spread,n=n,z=z,SE=str(se),margin=str(e),lower=str(lo),upper=str(hi),width=str(width)))
reports=[
('390.4','429.6','1.96',80,64,410),('404.392','445.608','2.576',80,100,425),
('68.848','79.152','2.576',12,36,74),('75.5325','80.4675','1.645',15,100,78),
('115.065','124.935','1.645',27,81,120),('121.1','130.9','1.96',30,144,126),
('416.84','443.16','1.645',80,100,430),('405.2','424.8','1.96',60,144,415),
('69.06','74.94','1.96',12,64,72),('76.136','83.864','2.576',18,144,80),
('117.065','126.935','1.645',24,64,122),('124.848','135.152','2.576',32,256,130),
('56.08','63.92','1.96',16,64,60),('57.06','62.94','1.96',12,64,60)]
for lo,hi,z,spread,n,mean in reports:
    lo,hi,z=map(D,(lo,hi,z)); mid=(lo+hi)/2; e=(hi-lo)/2
    assert mid==mean and e>0
    assert (z*spread/e)**2==n
    assert e*D(n).sqrt()/z==spread
    assert mid-z*spread/D(n).sqrt()==lo and mid+z*spread/D(n).sqrt()==hi
assert (D('1.96')*80/20)**2==D('61.4656')
for n in (60,64):
    e=D('1.96')*80/D(n).sqrt()
    assert round(D(410)-e)==390 and round(D(410)+e)==430
Path('tmp/c4-purpose-20261124/math-audit.json').write_text(json.dumps(results,indent=2))
print('PASS: narrative tasks, prerequisite cleanup, nine purposes, 12 forward constructions, 14 exact inverse recoveries including advanced audits, rounded-report examples, unique source labels.')
