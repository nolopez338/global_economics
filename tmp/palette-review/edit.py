from pathlib import Path
import re
root=Path.cwd(); folder=root/'book2026-2027/preamble/graphs'
for name in ['highlights.tex','specific_highlights.tex','specific_highlights_view.tex','specific_highlights.md']:
 (root/'tmp/palette-review'/('original-'+name)).write_bytes((folder/name).read_bytes())
def save(p,s):
 with p.open('w',encoding='utf-8',newline='') as f:f.write(s.replace('\r\n','\n').replace('\n','\r\n'))
p=folder/'highlights.tex';s=p.read_text();s=s.replace('known masses/results; Parameter', 'general probabilities and known masses/results (not the dedicated success or\n% complement roles in the registry); Parameter');save(p,s)
p=folder/'specific_highlights.tex';s=p.read_text();s=s.replace(r'\colorlet{MathHLComplementColor}{GTenHLProbability!65!CtwoCriticalColor}',r'''% Exact swap of the previous registry success/complement colors, captured at load.
% Keep general masses on GTenHLProbability and population proportions unchanged.
\colorlet{MathHLSuccessColor}{GTenHLProbability!65!CtwoCriticalColor}
\colorlet{MathHLComplementColor}{G11T2C1PopulationProportion}''')
s=s.replace(r'\expandafter\newcommand\csname coordinatedrole@probability\endcsname[1]{\HLPopulationProportion{#1}}',r'''\newcommand{\HLProbability}[1]{\GTenHLProbability{#1}}
\newcommand{\HLSuccessProbability}[1]{\HighlightStroke{MathHLSuccessColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@probability\endcsname[1]{\HLProbability{#1}}
\expandafter\newcommand\csname coordinatedrole@probability.success\endcsname[1]{\HLSuccessProbability{#1}}
\expandafter\newcommand\csname coordinatedrole@proportion.population\endcsname[1]{\HLPopulationProportion{#1}}''')
# Grade 10 uses are general probability except the success-model parameter and its threshold.
lines=s.splitlines()
for i,line in enumerate(lines):
 if 'coordinatednotation@10@' in line or 'coordinatedrow@10@' in line or (r'\CoordinatedLegendRow{probability}' in line and i<490):
  success=('@10@p\\' in line or '@10@break\\' in line or 'Success}' in line or 'break-even}' in line)
  lines[i]=line.replace(r'\HLPopulationProportion',r'\HLSuccessProbability' if success else r'\HLProbability')
  if success:lines[i]=lines[i].replace(r'\CoordinatedLegendRow{probability}',r'\CoordinatedLegendRow{probability.success}')
s='\n'.join(lines)+'\n'
# Grade 11 population fractions and planning inputs retain the original pink role.
s=s.replace('% 10/p: probability\n','% 10/p: probability.success\n').replace('% 10/break: probability\n','% 10/break: probability.success\n')
s=s.replace('% 11/proppop: probability\n','% 11/proppop: proportion.population\n').replace('% 11/planning: probability\n','% 11/planning: proportion.population\n')
s=s.replace(r'\CoordinatedLegendRow{probability}{\csname coordinatednotation@11@',r'\CoordinatedLegendRow{proportion.population}{\csname coordinatednotation@11@')
s=s.replace('% Only the C2/C3 practice documents consume these semantic wrappers.','% C2/C3 and coordinated practice documents consume these semantic wrappers.')
s=s.replace('% Canonical roles add no load-time redefinition of legacy colors or wrappers.','% Canonical roles add no load-time redefinition of legacy colors or wrappers.')
save(p,s)
p=folder/'specific_highlights_view.tex';s=p.read_text();s=s.replace(r'\PreviewLegend{G10-T2-C1-coordinated}{Coordinated version}',r'''\PreviewLegend{G10-T2-C1-coordinated}{Coordinated version}
\PreviewLegend{G10-T2-C1}{Legacy registered variant}''')
# Remove repeated combined catalogs at the end.
last=s.index('\\clearpage\n\n\\PreviewLegend{G11-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-C10-coordinated}',s.index('\\section{Grade 11}'))
s=s[:last]+r'\end{document}'+'\n';save(p,s)
p=root/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex';s=p.read_text();(root/'tmp/palette-review/original-C3.tex').write_bytes(p.read_bytes());s=s.replace(r'\newcommand{\SuccessProb}[1]{\GTenHLProbability{#1}}',r'\newcommand{\SuccessProb}[1]{\HLSuccessProbability{#1}}').replace(r'{GTenHLProbability!50!black}',r'{MathHLSuccessColor!50!black}');save(p,s)
print('Edited palette, semantic registry, preview, C3 forwarding and graph ink.')
