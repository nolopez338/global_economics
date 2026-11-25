from pathlib import Path
p=Path('book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex');s=p.read_text()
s=s.replace(r'\HLCumulativeProbability{4},\HLCumulativeProbability{22},\HLCumulativeProbability{34},\HLCumulativeProbability{46},\HLCumulativeProbability{47},\HLCumulativeProbability{75},\HLCumulativeProbability{84}',r'\HLCumulativeProbability{4},\allowbreak\HLCumulativeProbability{22},\allowbreak\HLCumulativeProbability{34},\allowbreak\HLCumulativeProbability{46},\allowbreak\HLCumulativeProbability{47},\allowbreak\HLCumulativeProbability{75},\allowbreak\HLCumulativeProbability{84}')
p.write_text(s)
Path('tmp/g10-solution-update/disabled.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'))
