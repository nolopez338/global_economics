from pathlib import Path
from copy import deepcopy
from urllib.parse import urlsplit,urlunsplit,unquote,quote
import os,re,json,zipfile,shutil
from lxml import etree
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
root=Path.cwd(); work=root/'tmp/term2_plan'
path=root/'book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx'
shutil.copy2(path,work/'original.docx')
en={
1:('Population parameters and sample statistics','What changes when a market association redraws 60 stalls from its 1,200-stall June list? Students identify the population and sample, pair means, standard deviations and digital-payment proportions with their symbols, and compare the two draws. Their annotated comparisons distinguish fixed parameters from variable statistics and explain why expanding the population changes the target.'),
2:('Point estimates intervals and confidence','How informative is a single estimate of weekly locker rental charges? Students calculate the standard error, margin and interval for 64 customers, then count which supplied simulated intervals capture the separate, known simulation mean. They report observed coverage and its departure from nominal confidence, explaining why confidence describes repeated sampling rather than the probability of a realized interval.'),
3:('Components of a confidence interval','How does sample size or confidence change uncertainty in household grocery spending? Students tabulate standard errors, critical values and margins, then plot their relationships with sample size and confidence on labeled numerical axes while holding the estimate fixed. Their graphs and explanations distinguish centre, margin and full width, and connect precision with nominal coverage.'),
4:('Normal interval for a mean with known variance','Do courier earnings support a population mean above 400 thousand COP? From a random sample of 64 of 2,400 members and known variance 6,400, students obtain the population standard deviation, justify a normal interval, and compute its standard error and 95% bounds. Their interpretation explains why the interval includes values below the benchmark and estimates a population mean rather than individual earnings.'),
5:('Interval for a population proportion','Is a lender’s first-year default rate below 20%? Using 50 defaults among 400 sampled loans from an 8,000-loan cohort, students check the sampling fraction and both outcome counts, then calculate a 98% one-proportion z interval. Their conclusion identifies the population, expresses the margin in percentage points, and assesses the benchmark using the interval.'),
6:('Planning sample size for a precision target','How many cargo records or households are needed for a stated precision? Students solve the margin-of-error inequality for a mean clearance time, round upward and check the adjacent sample size, then compare pilot-based and conservative plans for a household subsidy proportion. Their justified plans distinguish minutes from percentage points and explain why greater assumed variability requires more observations.'),
7:('Confidence and precision','What does a larger rider survey buy a transit authority? Students construct mobile-ticket-use intervals for samples of 100 and 400 riders with the same observed 40% share, then compare 90% and 99% confidence. Their comparison of margins and widths separates the effects of sample size and confidence and identifies a plan meeting the authority’s coverage and precision requirements.'),
8:('Student’s t interval for a mean','How precisely can a logistics centre estimate mean loading time with an unknown population standard deviation? For 12 sampled loads from 400, students check the design and sample shape, select the t cutoff with 11 degrees of freedom, and calculate the 95% interval using the sample standard deviation. Their interpretation supports labour planning while distinguishing uncertainty in the mean from variability in individual loads.'),
9:('Validity and limitations of inference','Can a bank generalize from the first 120 volunteers among 600 customers? Students audit undercoverage, voluntary response, the sampling fraction, skew and an unverified extreme value, then contrast rare loan defaults and invoices clustered within firms. Their written redesign explains why a larger sample or a small sampling fraction alone cannot establish validity and identifies the checks each interval procedure needs.'),
10:('Integrated economic investigation','Does mean weekly net fee revenue exceed 12.90 thousand USD per merchant? Students plan random selection from 500 merchants, analyse the 16 supplied weekly totals, justify a t interval, and check its achieved margin against the 0.50-thousand-USD target. Their evidence brief assesses the benchmark, states assumptions and limits, and explains how a quarter-long study would handle repeated merchant records.')}
es={
1:('Parámetros poblacionales y estadísticos muestrales','¿Qué cambia al volver a seleccionar 60 puestos de la lista de 1.200 puestos de junio de una asociación? Los estudiantes identifican población y muestra, relacionan medias, desviaciones estándar y proporciones de pago digital con sus símbolos y comparan ambas muestras. Sus comparaciones anotadas distinguen parámetros fijos de estadísticos variables y explican por qué ampliar la población cambia el objeto de la estimación.'),
2:('Estimación puntual por intervalos y confianza','¿Cuánta información aporta una estimación del alquiler semanal de casilleros? Los estudiantes calculan el error estándar, el margen y el intervalo para 64 clientes y cuentan cuáles intervalos simulados suministrados contienen la media conocida de la simulación, distinta de la media poblacional original. Informan la cobertura observada y su diferencia frente a la confianza nominal y explican que la confianza describe muestreos repetidos, no la probabilidad de un intervalo ya calculado.'),
3:('Componentes de un intervalo de confianza','¿Cómo cambia la incertidumbre sobre el gasto familiar en alimentos al variar el tamaño muestral o la confianza? Los estudiantes tabulan errores estándar, valores críticos y márgenes y grafican sus relaciones con el tamaño muestral y la confianza en ejes numéricos rotulados, manteniendo fija la estimación. Sus gráficas y explicaciones distinguen centro, margen y amplitud total y relacionan la precisión con la cobertura nominal.'),
4:('Intervalo normal para una media con varianza conocida','¿Los ingresos de una cooperativa de mensajeros respaldan una media poblacional superior a 400 mil COP? Con una muestra aleatoria de 64 de sus 2.400 miembros y varianza conocida de 6.400, los estudiantes obtienen la desviación estándar poblacional, justifican el intervalo normal y calculan su error estándar y sus límites al 95%. Su interpretación explica por qué el intervalo incluye valores inferiores al referente y estima una media poblacional, no ingresos individuales.'),
5:('Intervalo para una proporción poblacional','¿La proporción de incumplimiento de una entidad durante el primer año es inferior al 20%? Con 50 incumplimientos en 400 préstamos seleccionados de una cohorte de 8.000, los estudiantes verifican la fracción muestral y ambos conteos y calculan un intervalo z del 98% para una proporción. Su conclusión identifica la población, expresa el margen en puntos porcentuales y evalúa el referente mediante el intervalo.'),
6:('Planificación del tamaño muestral','¿Cuántos registros de carga u hogares se necesitan para una precisión dada? Los estudiantes despejan el tamaño muestral en la desigualdad del margen para el tiempo medio de despacho aduanero, redondean hacia arriba y verifican el tamaño vecino; luego comparan planes basados en un piloto y en una proporción conservadora para un subsidio de energía. Sus planes justificados distinguen minutos de puntos porcentuales y explican por qué una mayor variabilidad supuesta exige más observaciones.'),
7:('Confianza y precisión','¿Qué gana una autoridad de transporte al ampliar una encuesta de pasajeros? Los estudiantes construyen intervalos de uso de tiquetes móviles con muestras de 100 y 400 pasajeros y la misma proporción observada del 40%, y luego comparan confianzas del 90% y del 99%. Su comparación de márgenes y amplitudes separa los efectos del tamaño muestral y de la confianza e identifica un plan que cumple las metas de cobertura y precisión.'),
8:('Intervalo t de Student para una media','¿Con qué precisión puede un centro logístico estimar el tiempo medio de carga si desconoce la desviación estándar poblacional? Para 12 cargas seleccionadas de 400, los estudiantes revisan el diseño y la forma muestral, eligen el valor t con 11 grados de libertad y calculan el intervalo del 95% usando la desviación estándar muestral. Su interpretación orienta la planificación laboral y distingue la incertidumbre sobre la media de la variabilidad de cargas individuales.'),
9:('Validez y limitaciones de la inferencia','¿Puede un banco generalizar a partir de los primeros 120 voluntarios entre 600 clientes? Los estudiantes examinan subcobertura, respuesta voluntaria, fracción muestral, asimetría y un valor extremo sin verificar, y contrastan casos de pocos incumplimientos e invoices agrupadas por empresa. Su rediseño escrito explica por qué ampliar la muestra o tener una fracción muestral pequeña no basta para validar la inferencia e identifica las verificaciones que exige cada procedimiento.'),
10:('Investigación económica integrada','¿El ingreso neto medio semanal por comisiones supera 12,90 mil USD por comercio? Los estudiantes planifican una selección aleatoria entre 500 comercios, analizan los 16 totales semanales suministrados, justifican un intervalo t y verifican el margen obtenido frente a la meta de 0,50 mil USD. Su informe evalúa el referente, explicita supuestos y limitaciones y explica cómo un estudio trimestral trataría registros repetidos del mismo comercio.')}
es[9]=(es[9][0],es[9][1].replace('invoices','facturas'))
d=Document(path)
links=json.loads((work/'links.json').read_text())
modified=set()
def replace(p,text,boldlead=None):
 prop=deepcopy(p.runs[-1]._r.rPr) if p.runs and p.runs[-1]._r.rPr is not None else None
 p.clear()
 if boldlead:
  r=p.add_run(boldlead);r._r.insert(0,deepcopy(prop)) if prop is not None else None;r.bold=True
 r=p.add_run(text);r._r.insert(0,deepcopy(prop)) if prop is not None else None;r.bold=False
 modified.add(p._p)
def target(href):
 s=urlsplit(href)
 if s.scheme or s.netloc:return href
 full=(root/'grade11/src'/unquote(s.path)).resolve()
 rel=os.path.relpath(full,path.parent).replace('\\','/')
 return urlunsplit(('','',quote(rel,safe='/'),s.query,s.fragment))
for lang, groups, descs in [('en',[(10,0,range(1,5)),(10,1,range(5,8)),(10,2,range(8,11))],en),('es',[(22,0,range(1,5)),(22,1,range(5,8)),(23,0,range(8,11))],es)]:
 for ti,ri,criteria in groups:
  c=d.tables[ti].rows[ri].cells[1]
  intro=('Use each practice to connect an economic question with a justified estimate. Students compare reasoning, revise an interpretation and retain their annotated work as formative evidence; linked classroom activities and slides support the sequence. Practice also provides optional independent review.' if lang=='en' else 'Usar cada práctica para conectar una pregunta económica con una estimación justificada. Los estudiantes comparan razonamientos, revisan una interpretación y conservan el trabajo anotado como evidencia formativa; las actividades de clase y diapositivas enlazadas apoyan la secuencia. La práctica también permite el repaso autónomo opcional.')
  replace(c.paragraphs[3],intro)
  for j,num in enumerate(criteria):
   title,body=descs[num];p=c.paragraphs[4+2*j]
   replace(p,body,f'C{num} – {title}. ')
   p=c.paragraphs[5+2*j];p.clear();modified.add(p._p)
   labels={'Practice Activity':'Actividad de práctica','Classroom Activity':'Actividad de clase','Slides':'Diapositivas'}
   for k,kind in enumerate(['Practice Activity','Classroom Activity','Slides']):
    if k:p.add_run('  |  ')
    l=next(x for x in links if x['label']==f'C{num} – {kind}')
    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),d.part.relate_to(target(l['href']),RT.HYPERLINK,is_external=True))
    r=OxmlElement('w:r');rp=OxmlElement('w:rPr')
    for tag,attr,val in [('rFonts','ascii','Century Gothic' if lang=='en' else 'Calibri'),('sz','val','19'),('color','val','0563C1'),('u','val','single')]:
     el=OxmlElement('w:'+tag);el.set(qn('w:'+attr),val);rp.append(el)
    r.append(rp);t=OxmlElement('w:t');t.text=f'C{num} – '+(kind if lang=='en' else labels[kind]);r.append(t);h.append(r);p._p.append(h)
# Add concise diagnostic purpose/reflection without importing any reference topics or arrangements.
for ti,txt in [(8,'Purpose: identify what students already distinguish about samples and populations. Before calculating, each student records a proposed estimate and a question about its precision; revisit this response after the activities to explain what evidence changed the interpretation.'),(20,'Propósito: identificar qué distinguen los estudiantes sobre muestras y poblaciones. Antes de calcular, cada estudiante registra una estimación propuesta y una pregunta sobre su precisión; retomar esta respuesta después de las actividades para explicar qué evidencia cambió la interpretación.')]:
 c=d.tables[ti].cell(0,0);p=c.add_paragraph();p._p.insert(0,deepcopy(c.paragraphs[0]._p.pPr));r=p.add_run(txt)
 r.font.name='Century Gothic' if ti==8 else 'Calibri';from docx.shared import Pt;r.font.size=Pt(10.5)
 modified.add(p._p)
# Snapshot changed paragraphs; all other paragraph XML must remain identical.
base=Document(work/'original.docx')
base_unchanged=[etree.tostring(p) for p in base.element.xpath('//w:p')]
unchanged=[etree.tostring(p) for p in d.element.xpath('//w:p') if p not in modified]
# Existing paragraphs outside the exact edit set are preserved in order.
bi=iter(base_unchanged)
for p in unchanged:
 assert any(x==p for x in bi),'Unexpected non-target paragraph change'
d.save(path)
(work/'descriptions.json').write_text(json.dumps({'en':en,'es':es},ensure_ascii=False,indent=2),encoding='utf8')
print('Updated',path,'; edited paragraphs',len(modified))
