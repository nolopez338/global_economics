from pathlib import Path
p=Path('book2026-2027/grade11/term_2/4-learning_evidences/G11_T2_L1_C1C2_exam_solution.tex')
s=p.read_text(encoding='utf-8')
for old,new in [('Its denominator is all 200,000 registered retail businesses operating in Medellin throughout October 2026.','Its denominator is all 200,000 eligible businesses defined above.'),('Its denominator is all 500,000 positive-balance personal savings accounts at the Cartagena branch network on October 31, 2026.','Its denominator is all 500,000 eligible accounts defined above.'),("Its denominator is all 100,000 completed deliveries by the platform's registered couriers in Bogota on November 2, 2026.",'Its denominator is all 100,000 eligible deliveries defined above.')]: s=s.replace(old,new)
for i in [1,2,3]:
 needle=r'\par\textbf{\hyperref[sol:p'+str(i)+r'c2a]{C2 Task 1}}\par'
 s=s.replace(needle,r'\Needspace{22\baselineskip}'+'\n'+needle)
s=s.replace(r'\subsection*{Problem 3: Create an integrated scenario from scratch}',r'\Needspace{10\baselineskip}'+'\n'+r'\subsection*{Problem 3: Create an integrated scenario from scratch}')
p.write_text(s,encoding='utf-8')
