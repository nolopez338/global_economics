"""Task-specific checks and audit export for this two-pair generation."""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,csv

root=Path.cwd();work=root/'.build/g10_t2_l1_alternates_1_1_1_2';dest=root/'book/grade10/term_2/4-learning_evidences'
models=json.loads((work/'models.json').read_text())
traces=json.loads((work/'procedure_operand_comparison.json').read_text())
# Q2(c) explicitly adds the two qualifying ordered-outcome probabilities.
for v in ('0','1','2'):
    d=models[v]['2'];step=next(s for s in traces[v]['2'] if s['role']=='answer.0')
    operands=[d['ps'][i] for i in d['groups'][4]]
    step.update(operation='add',operand_count=2,operands=operands,dependencies='outcome.5,outcome.7',reasoning='Two ordered pairs have the target sum')
(work/'procedure_operand_comparison.json').write_text(json.dumps(traces,indent=2))
rows=[];repeats=[]
for q in map(str,range(1,7)):
    ds=[models[v][q] for v in ('0','1','2')]
    for k in ds[0]:
        if k not in ('p','r','unit','cost','values','ratios','counts','bonus','cap'):continue
        vals=[d[k] if isinstance(d[k],list) else [d[k]] for d in ds]
        for i,t in enumerate(zip(*vals)):
            if len(set(map(str,t)))<3:
                assert (k=='values' and all(x==0 for x in t)) or (q=='6' and k=='counts' and i==2 and list(t)==[2,2,2]),(q,k,i,t)
    for t in zip(*(traces[v][q] for v in ('0','1','2'))):
        assert len({(x['role'],x['operation'],x['operand_count'],x['dependencies'],x['reasoning']) for x in t})==1
        for kind,vals in [('result',[x['result'] for x in t])]+[(f'operand.{i}',[x['operands'][i] for x in t]) for i in range(t[0]['operand_count'])]:
            if len(set(vals))<3:
                assert len(set(vals))==1,('Accidental repeated replaceable value',q,t[0]['role'],kind,vals)
                value=vals[0]
                if q=='3' and value in ('1/4','1/2','3/4'):
                    why='Four equal positive grouped masses force 1/4; cumulative sums and boundary answers force 1/2 and 3/4.'
                elif value=='0':why='Null monetary outcomes, empty sums, zero composition counts, indicator off, or lower probability tail.'
                elif value=='1':why='Probability normalization, baseline relative weight, indicator on, or binomial choose-zero/choose-all identity.'
                elif q=='6' and value=='2':why='Two high-value items are necessary for precisely the same nine feasible compositions; composition counts and binomial factors follow.'
                elif value in ('2','3'):why='Fixed binary/ternary experiment arity, three selected items, or composition/support indices required by the source method.'
                else:raise AssertionError((q,t[0]['role'],kind,vals))
                repeats.append(dict(question=q,role=t[0]['role'],field=kind,value=value,justification=why))
        rows.append([q,t[0]['role'],t[0]['operation'],t[0]['operand_count'],t[0]['dependencies'],t[0]['reasoning']]+[str(x['operands']) for x in t]+[x['result'] for x in t])
with (work/'procedure_operand_comparison.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f,delimiter='\t');w.writerow(['Question','Step','Operation','Operand count','Dependencies','Reasoning','Source operands','1_1 operands','1_2 operands','Source result','1_1 result','1_2 result']);w.writerows(rows)
(work/'numerical_repetitions_justified.json').write_text(json.dumps(repeats,indent=2))

for v in ('1','2'):
    exam=(dest/f'G10_T2_L1_C1C2_exam_1_{v}.tex').read_text(encoding='utf-8')
    sol=(dest/f'G10_T2_L1_C1C2_exam_solution_1_{v}.tex').read_text(encoding='utf-8')
    statements=json.loads((work/f'version_{v}_statements.json').read_text())
    for q in map(str,range(1,7)):
        assert statements['questions'][q] in exam and statements['questions'][q] in sol
        assert statements['task_c'][q] in exam and statements['task_c'][q] in sol
    sections=re.split(r'(?=\\SubsectionBox\{)',exam)[1:]
    expected=[['1','1','1'],['1','1','1'],['0.5','1','0.5'],['0.5','1','0.5'],['1','2','1'],['1.5','3','1.5']]
    for section,values in zip(sections,expected):assert re.findall(r'\\sscore\{\\sml\{([\d.]+)\}\}',section)==values
    rubrics=re.findall(r'\\textbf\{Proposed partial credit\.\}(.*?)\\bottomrule',sol,re.S)
    assert len(rubrics)==18
    for table,total in zip(rubrics,[F(x) for group in expected for x in group]):
        pts=re.findall(r'\\CreditDescription\{[^\n]*?\} & ([\d.]+)\\\\',table)
        assert sum(map(F,pts))==total,(v,pts,total)
        assert r'\textbf{'+str(float(total)).rstrip('0').rstrip('.')+'}' in table
    assert sum(F(x) for s in expected[:2] for x in s)==6
    assert sum(F(x) for s in expected[2:] for x in s)==14

hashes=json.loads((work/'protected_sha256.json').read_text())
allowed={str((dest/f'G10_T2_L1_C1C2_exam_1.{ext}').relative_to(root)) for ext in ('tex','pdf')}
changed=[]
for rel,digest in hashes.items():
    if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest:
        changed.append(rel);assert rel in allowed,('Protected artifact changed',rel)
(work/'final_content_checks.json').write_text(json.dumps({'mapped_steps':len(rows),'justified_repeated_fields':len(repeats),'all_replaceable_givens_differ':True,'all_replaceable_operands_and_results_differ':True,'pair_statements_exact':True,'rubric_totals_reconciled':True,'protected_artifacts':len(hashes),'authorized_changes':changed},indent=2))
print('PASS:',len(rows),'corresponding steps;',len(repeats),'explicitly justified structural repetitions; exact pair statements; scores 6+14=20; protected artifacts verified.')
