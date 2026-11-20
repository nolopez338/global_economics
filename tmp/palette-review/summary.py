from pathlib import Path
import re
root=Path.cwd(); d=root/'book2026-2027/preamble/graphs';p=d/'specific_highlights.md';s=p.read_text();tex=(d/'specific_highlights.tex').read_text()
s=s.replace('groups, means, standard deviations, then proportions.','groups, means, standard deviations, variances, then proportions.')
s=s.replace('omits the separate size rows.','omits the separate size rows. Both variants include variance.')
s=s.replace('`G11T2C1Sample` / `#173B17` | $\\mathcal{P}$','`G11T2C1SampleGroup` / `#56A86B` | $\\mathcal{P}$')
s=s.replace('| Proportion |', '| Variance | $s^2$: squared sample spread. | `G11T2C1SampleVariance` / `#6B8E23` | $\\sigma^2$: squared population spread. | `G11T2C1PopulationVariance` / `#B54A45` |\n| Proportion |',1)
s=s.replace('and `\\GradeElevenCOneLegendProportions`, assembled','`\\GradeElevenCOneLegendVariances`, and `\\GradeElevenCOneLegendProportions`, assembled').replace('The table passes steps 2, 3, 4, and 5 to its four row helpers.','The table passes steps 2, 3, 4, and 5 to its four arguments and inserts the variance helper at step 4 before proportions.')
s=s.replace('and locally compacts marker padding to 0.6 mm horizontally / 0.3 mm vertically, without changing body markers.','and retains the shared marker padding. Practice-local padding overrides apply when selected by the caller.')
s=s.replace('its first argument records the semantic binding.','its first argument records the semantic binding. Rows with role `context` are omitted by `\\CoordinatedOmitRow`; all other rows use `\\CoordinatedPrintRow`. Catalog data below include these unprinted reference entries, while the selection lists show only effective printed rows.')
a=s.index('It maps `G11T2C1PopulationMean`');b=s.index('Loading the registry alone',a)
s=s[:a]+'It maps `ExpectedValueColor` to `MathHLExpectedValueColor` (gold `#D6A52A`), `CtwoEndpointColor` to `MathHLBoundsColor`, and `CtwoWidthColor` to `MathHLWidthColor`. Population means and population proportions retain their coral and pink defaults; no probability, success, complement, confidence or variance color is overridden. Existing expectation, endpoint and width calls follow the selected palette. '+s[b:]
s=s.replace('| `MathHLComplementColor` | `GTenHLProbability!65!CtwoCriticalColor` |','| `MathHLSuccessColor` | `GTenHLProbability!65!CtwoCriticalColor` (xcolor HTML conversion `6495DD`) |\n| `MathHLComplementColor` | `G11T2C1PopulationProportion` (`#D74383`) |')
s=s.replace('`G11T2C1PopulationSD!55!white`','`G11T2C1PopulationVariance` (`#B54A45`)').replace('`G11T2C1SampleSD!55!white`','`G11T2C1SampleVariance` (`#6B8E23`)')
s=s.replace('| `MathHLTailColor` |','| `MathHLExpectedValueColor` | HTML `D6A52A` |\n| `MathHLPoissonMeanColor` | HTML `D95F50` |\n| `MathHLTailColor` |',1)
s=s.replace('Population mean and expectation share violet only under this opt-in mapping; the legacy population-mean default remains coral.','Population mean stays coral (`#FF765C`); expectation is violet by default and gold under the opt-in palette. Poisson interval mean has its own coral identifier (`#D95F50`).')
s=s.replace('| `probability` | `\\HLPopulationProportion` | `GTenHLProbability` |','| `probability` | `\\HLProbability` (forwards to `\\GTenHLProbability`) | `GTenHLProbability` (`#86BFF0`) |\n| `probability.success` | `\\HLSuccessProbability` | `MathHLSuccessColor` |\n| `proportion.population` | `\\HLPopulationProportion` | `G11T2C1PopulationProportion` (`#D74383`) |')
s=s.replace('| `expectation` | `\\HLPopulationMean` | `ExpectedValueColor` |','| `expectation` | `\\HLExpectedValue` | `ExpectedValueColor` |\n| `mean.population` | `\\HLPopulationMean` | `G11T2C1PopulationMean` |\n| `mean.poisson` | `\\HLPoissonMean` | `MathHLPoissonMeanColor` |')
s=s.replace('| `group.sample` | `\\HLSampleGroup` | `G11T2C1Sample` |','| `group.sample` | `\\HLSampleGroup` | `G11T2C1SampleGroup` (`#56A86B`) |')
s=s.replace('`p` / `probability`','`p` / `probability.success`').replace('`break` / `probability`','`break` / `probability.success`').replace('`proppop` / `probability`','`proppop` / `proportion.population`').replace('`planning` / `probability`','`planning` / `proportion.population`').replace('`lambda` / `expectation`','`lambda` / `mean.poisson`').replace('`meanpop` / `expectation`','`meanpop` / `mean.population`')
s=s.replace('$E(X)$, $\\mathbb E[Y_i]$, $\\mu$ | Expected value or model mean:', '$E(X)$, $\\mathbb E[Y_i]$ | Expected value:')
s=s.replace('| `break` /', '| `meanpop` / `mean.population` | $\\mu$ | Population or model mean: Mean of the population or specified model, in original units. |\n| `break` /',1)
s=s.replace('Row order is the order printed by each general key.','Catalog order follows the source data; `context` entries are reference-only and do not print. Effective printed selections appear below.')
# Replace row-order prefixes using actual source selections, preserve notation descriptions.
for m in re.finditer(r'practicehighlightlegend@([^\\]+)\\endcsname\{%([\s\S]*?)(?=\\expandafter\\newcommand\\csname practicehighlightlegend@|\Z)',tex):
 key,body=m.groups()
 if not key.endswith('-coordinated'):continue
 ids=re.findall(r'\\CoordinatedLegendEntry\{(\d+)\}\{([^}]+)\}',body)
 printed=[]
 for grade,eid in ids:
  row=re.search(r'coordinatedrow@'+grade+'@'+eid+r'\\endcsname\{%\s*\\CoordinatedLegendRow\{([^}]+)\}',tex)
  assert row,(key,eid)
  if row[1]!='context':printed.append(eid)
 pattern=r'(- `'+re.escape(key)+r'`: )[^\n]*?(\. Notation:|\.\s*$)'
 s,n=re.subn(pattern,lambda x:x[1]+', '.join('`'+i+'`' for i in printed)+x[2],s,flags=re.M)
 assert n==1,(key,n)
s=s.replace('its setup palette makes population means violet and population fractions blue','its setup palette leaves population means coral and population fractions pink')
s=s.replace("C3's one-argument `\\FailureProb` now forwards to complementary probability; its expectation/probability graph inks retain their darker mixes and black disabled variants.","C3's one-argument `\\SuccessProb` forwards to `\\HLSuccessProbability` and `\\FailureProb` to `\\HLComplementProbability`; names, values and substitutions follow these wrappers. Its probability/break-even graph ink is `MathHLSuccessColor!50!black`; expectation ink is `ExpectedValueColor!55!black`, with black disabled variants.")
s=s.replace('and from the legacy coral population-mean default; the coordinated population-mean alias below reuses this violet.','and from the coral population-mean color. The coordinated palette changes expectation to gold, while leaving population mean coral.')
s += '''\n### Probability-role reconciliation and preview\n\nGeneral event probabilities and PMF masses use `\\HLProbability` / `\\GTenHLProbability`, light blue `GTenHLProbability` (`#86BFF0`). Success-model parameters (including individual break-even thresholds) use `\\HLSuccessProbability`, the former complement mix `GTenHLProbability!65!CtwoCriticalColor`; complement parameters use `\\HLComplementProbability`, the former registry success pink `#D74383`. The prior registry success wrapper was `\\HLPopulationProportion`; its population-fraction meaning retains pink. The prior C3 `\\SuccessProb` forwarding to general blue was inconsistent with that registry and now uses the dedicated success wrapper. A symbol such as $p_X(x)$ is a mass, not automatically a success parameter; unknown $q$ retains the unknown role. Cumulative probability and confidence remain separate roles.\n\nThe success mix and complement alias are captured at registry load time, before any caller-scoped palette command. xcolor converts the success mix to HTML `6495DD`; the exact mix expression is authoritative. Confidence stays `CtwoConfidenceColor` (`#55C8F0`) through `\\CtwoConfidence` / `\\HLConfidence`, visibly more cyan than the general light blue at the unchanged fill opacity. Neither palette command changes these roles.\n\n[specific_highlights_view.tex](specific_highlights_view.tex) renders every registered key once, including legacy `G10-T2-C1`. Its per-entry group prevents palette leakage; coordinated entries additionally group their own palette selection. The preview uses A3 portrait and enabled highlights; G10 C10 remains an explicit pending notice, not a registry entry.\n'''
with p.open('w',encoding='utf8',newline='') as f:f.write(s.replace('\n','\r\n'))
keys=set(re.findall(r'practicehighlightlegend@([^\\]+)\\endcsname',tex));preview=(d/'specific_highlights_view.tex').read_text();calls=re.findall(r'\\PreviewLegend\{([^}]+)\}',preview)
assert keys==set(calls),(keys-set(calls),set(calls)-keys)
assert len(calls)==len(set(calls))
assert all('`'+k+'`' in s for k in keys)
print(len(keys),'registered legends, each previewed once and documented.')
