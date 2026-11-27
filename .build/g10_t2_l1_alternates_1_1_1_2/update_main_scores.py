from pathlib import Path
import re,json

root=Path.cwd()
dest=root/'book/grade10/term_2/4-learning_evidences'
work=root/'.build/g10_t2_l1_alternates_1_1_1_2'
report={}
pattern=re.compile(r'Complete general tasks \(a\) and \(b\) for (C[12])\. \\textbf\{Marks:\} \(a\) ([\d.]+); \(b\) ([\d.]+)\.')
for suffix in ('1','1_1','1_2'):
    path=dest/f'G10_T2_L1_C1C2_exam_{suffix}.tex'
    backup=work/(path.name+'.before_main_scores')
    before=backup.read_bytes() if backup.exists() else path.read_bytes()
    text=before.decode('utf-8')
    matches=list(pattern.finditer(text))
    assert len(matches)==6
    original_allocations=[m.groups() for m in matches]
    def replacement(m):
        criterion,a,b=m.groups()
        return f'Complete general tasks (a) \\sscore{{\\sml{{{a}}}}} and (b) \\sscore{{\\sml{{{b}}}}} for {criterion}.'
    after=pattern.sub(replacement,text)
    c_pattern=re.compile(r'\\item ([^\r\n]*?) \\sscore\{\\sml\{([\d.]+)\}\}')
    after,c_count=c_pattern.subn(lambda m:f'\\item \\sscore{{\\sml{{{m[2]}}}}} {m[1]}',after)
    assert c_count==6
    reverse=re.compile(r'Complete general tasks \(a\) \\sscore\{\\sml\{([\d.]+)\}\} and \(b\) \\sscore\{\\sml\{([\d.]+)\}\} for (C[12])\.')
    reconstructed=reverse.sub(lambda m:f'Complete general tasks (a) and (b) for {m[3]}. \\textbf{{Marks:}} (a) {m[1]}; (b) {m[2]}.',after)
    reconstructed=re.sub(r'\\item \\sscore\{\\sml\{([\d.]+)\}\} ([^\r\n]*)',lambda m:f'\\item {m[2]} \\sscore{{\\sml{{{m[1]}}}}}',reconstructed)
    assert reconstructed==text, 'Unrelated text changed'
    # Includes each internal (i)/(ii) breakdown, heading and matrix unchanged.
    assert re.findall(r'\\textbf\{Allocation:\}[^\r\n]*',text)==re.findall(r'\\textbf\{Allocation:\}[^\r\n]*',after)
    assert after.count(r'\sscore{\sml{')==18
    if not backup.exists():
        with backup.open('xb') as f:f.write(before)
    path.write_bytes(after.encode('utf-8'))
    report[suffix]={'main_allocations':original_allocations,'main_c_scores':re.findall(r'\\item \\sscore\{\\sml\{([\d.]+)\}\}',after),'exact_round_trip':True,'internal_allocations_unchanged':True,'C1_total':6,'C2_total':14,'overall':20}
(work/'main_score_notation_verification.json').write_text(json.dumps(report,indent=2))
print('Updated 18 (a)/(b) references in three files. All 54 main task scores use inline notation; exact reversal matches each prior source.')
