import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'book2026-2027/seminars/term_1/second_learning_evidence'
REVIEW = Path(__file__).resolve().parent
sources = json.loads((REVIEW / 'sources.json').read_text(encoding='utf-8'))
byid = {s['id']: s for s in sources}
with (BASE / 'resultados_criterios.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
csv_hash = hashlib.sha256((BASE / 'resultados_criterios.csv').read_bytes()).hexdigest()

def esc(s):
    s = unicodedata.normalize('NFC', s)
    return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_', '{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}.get(c,c) for c in s)

def cite(s, pages):
    return rf'\evid{{{s}}}{{{pages}}}'

def claim(text, s, pages):
    return esc(text) + ' ' + cite(s, pages) + '.'

groups = []
def group(number, title, members, membership, ids, rowids, criteria, problem, ideas, note=''):
    assert len(criteria) == 6
    groups.append(dict(number=number,title=title,members=members,membership=membership,ids=ids,rows=rowids,criteria=criteria,problem=problem,ideas=ideas,note=note))

group(1, 'Turnos y filas de Asobartolina',
      'Thomas Álvarez, Nicolás Álvarez y Juan Felipe Ojeda', cite('S01','1'), ['S01'], [1,19], [
    claim('Organizaron el recorrido de estudiantes que compran o calientan loncheras y tres hallazgos sobre colados, pérdida de tiempo y falta de regulación', 'S01','1--2'),
    claim('Compararon las filas de Asobartolina con la presión en debates y la extensión de guías, y seleccionaron la primera oportunidad con 9 puntos frente a 7 y 6', 'S01','2--4'),
    claim('Reformularon D1 para garantizar turnos equitativos y reducir la espera al comprar alimentos o calentar loncheras durante los descansos', 'S01','4--5'),
    claim('Relacionaron normas sociales y acción colectiva con claridad del flujo y señalética, y dejaron pendiente verificar el peso de la confusión espacial', 'S01','5'),
    claim('Registraron once ideas, incluidas una línea delimitada con supervisión y una zona de microondas con fichas, aunque la autoría y la escucha aparecen como anónimas', 'S01','6--8'),
    claim('Contrastaron negar la atención a colados y delimitar la fila con supervisión, señalando supuestos sobre autorización del personal, aceptación de monitores y protección del descanso', 'S01','8'),
], claim('El equipo identifica desorden y colados en la compra de alimentos y el uso de microondas, con pérdida del tiempo disponible para comer y descansar', 'S01','1--2'), [
    claim('Proponen delimitar la fila con supervisión estudiantil y una norma de no atención a quienes se cuelan, como posibilidad por explorar', 'S01','7--8'),
    claim('Proponen una zona independiente de microondas con fichas que limiten el tiempo por usuario', 'S01','7'),
], 'Thomas Álvarez figura como integrante del PDF, pero no tiene fila propia en este CSV; no se lo confunde con otro alumno ni se le asigna una fila inexistente ' + cite('S01','1') + '.')

group(2, 'Espera y convivencia en Asobartolina',
      'Patrik Ayala y Gabriel Galán', cite('S02','1') + '; ' + cite('S03','1'), ['S02','S03'], [2,11], [
    claim('Reunieron perfiles, experiencias de espera de 5 a 9 minutos y una comparación entre observaciones y testimonios sobre filas, colados y conflictos', 'S02','1--2'),
    esc('Identificaron reducir el tiempo de espera como necesidad principal, pero no se identificó una comparación de oportunidades con matriz de priorización en los PDF legibles ') + cite('S02','2') + '; ' + cite('S03','1--3') + '.',
    claim('Definieron y revisaron D1 para reducir la espera y los conflictos por colados de estudiantes de décimo al comprar o reclamar durante el descanso', 'S02','2--3'),
    claim('Conectaron el diseño de servicios y los flujos físicos con normas de convivencia y resolución pacífica de conflictos', 'S02','3'),
    claim('Documentaron cinco propuestas y un registro de pregunta y ampliación, con ideas de fila exprés, señalización, campaña y combinaciones grupales', 'S02','4'),
    claim('Contrastaron la fila exprés y los turnos por colores con supuestos sobre pago anticipado y respeto de marcas, y plantearon condiciones de sencillez y acceso sin teléfono', 'S02','4--5'),
], claim('Describen pérdida del descanso y conflictos asociados con colados y desorganización al comprar o reclamar en Asobartolina', 'S02','1--2'), [
    claim('Proponen una fila exprés para reclamar pedidos prepagados', 'S02','4'),
    claim('Proponen una campaña gráfica de concientización sobre el respeto de la fila', 'S02','4'),
], 'Las portadas coinciden en ambos integrantes y en la situación investigada; las grafías Patrik y Patrick dentro de la entrega se conservan como variante del mismo nombre, sin inferir un integrante adicional ' + cite('S02','1 y 4') + '; ' + cite('S03','1') + '.')

group(3, 'Concentración y uso de audífonos',
      'Sebastián González Mojica y Emilio José Barón Romero', cite('S04','1') + '; ' + cite('S05','1'), ['S04','S05'], [3,12], [
    claim('Organizaron estudiantes, docentes, contexto y recorrido del uso de audífonos, junto con cuatro hallazgos sobre ocultamiento, trabajo individual y diversidad de beneficios percibidos', 'S04','3--4'),
    claim('Compararon claridad sobre el uso de audífonos, dinamismo pedagógico y acuerdos tecnológicos, y priorizaron la primera oportunidad con 9 puntos', 'S04','5--8'),
    claim('Revisaron una pregunta que anticipaba permitir audífonos y formularon D1 sobre gestionar la concentración durante el trabajo autónomo manteniendo la comunicación docente', 'S05','2--3'),
    claim('Vincularon autorregulación del aprendizaje con participación y acuerdos de convivencia, distinguiendo conceptos consultados de hipótesis y verificaciones institucionales pendientes', 'S05','4--5'),
    esc('No se identificó un registro de ideación de C9 en los dos PDF accesibles y legibles revisados ') + cite('S04','1--8') + '; ' + cite('S05','1--6') + '.',
    esc('No se identificó un contraste de ideas de C10 con evidencia del usuario en los dos PDF accesibles y legibles revisados ') + cite('S04','1--8') + '; ' + cite('S05','1--6') + '.',
], claim('El proyecto aborda la gestión de la concentración en el trabajo individual y la tensión entre el uso de audífonos, las normas y la comunicación en clase, sin asumir que la música beneficia a todos', 'S04','3--4') + ' ' + cite('S05','2--3'), [
    esc('No se identificaron ideas de solución desarrolladas como propuestas del equipo en los PDF revisados, que documentan C5--C8 y dejan el desafío abierto ') + cite('S04','1--8') + '; ' + cite('S05','2--6') + '.',
], 'La mención de autorregulación y acuerdos en C8 describe conocimientos para comprender D1; no se transforma en evidencia de ideación o de implementación.')

group(4, 'Hábitos y calidad del sueño',
      '«Isa» y «Lucio», nombres de autoría tal como aparecen en el PDF', cite('S06','7 y 10'), ['S06'], [4,8], [
    claim('Organizaron diez respuestas sobre sueño, un recorrido del estudiante y hallazgos sobre bienestar y horarios, con legibilidad parcial en la tabla de hallazgos', 'S06','1--4'),
    claim('Compararon mejorar la calidad del sueño y establecer un horario, eligieron la segunda opción por 8 puntos frente a 6 y reconocieron que faltaba justificar por completo los puntajes', 'S06','4--5'),
    claim('Formularon D1 sobre generar buenos hábitos de sueño en estudiantes de décimo con mala calidad de descanso y registraron una revisión de su claridad', 'S06','6'),
    claim('Relacionaron administración del tiempo y psicología de los hábitos para comprender los horarios de sueño, con pendientes sobre los beneficios de mantenerlos estables', 'S06','6--7'),
    claim('Enumeraron tres ideas de Isa y tres de Lucio, y combinaron sus aportes en un horario sin pantallas y un planeador con relajación', 'S06','7--8'),
    claim('Examinaron las dos propuestas grupales mediante supuestos, preguntas pendientes y condiciones de adaptación a responsabilidades y preferencias individuales', 'S06','8--9'),
], claim('El documento relaciona horarios de sueño irregulares, actividades escolares, uso de pantallas y cansancio durante la jornada', 'S06','2--4'), [
    claim('Proponen calcular el tiempo de tareas y organizar un horario personal que incluya apagar las pantallas antes de dormir', 'S06','7'),
    claim('Proponen un planeador de obligaciones que incorpore una pausa de relajación al finalizar las tareas', 'S06','8'),
], 'Las filas 4 (Lucio Barrero Sánchez) y 8 (Ana Isabella Colorado Parrado) comparten S06, pero este no declara sus nombres completos: la equivalencia de «Isa» y «Lucio» con esas identidades queda pendiente, sin convertirla en pertenencia plenamente verificada; las páginas PDF 4, 5, 6 y 10 presentan líneas o texto de tablas superpuestos y el resumen se limita a texto recuperable y pasajes narrativos.')

group(5, 'Búsqueda en objetos perdidos',
      'Miguel Ángel Caballero Hernández y Juan Ignacio Rodríguez Rodríguez', cite('S07','1'), ['S07'], [5,24], [
    claim('Organizaron el recorrido de búsqueda en objetos perdidos y cuatro hallazgos apoyados en una tabla de quince encuestados y registros de observación', 'S07','3--5'),
    claim('Compararon clasificación física y reducción de hurto o pérdida, y eligieron la primera con 9 puntos frente a 7 reconociendo que no resolvería la desaparición de objetos', 'S07','5--6'),
    claim('Ajustaron D1 para facilitar la búsqueda visual y física de pertenencias de estudiantes de Ciclo V sin desordenar la mesa', 'S07','6--7'),
    claim('Relacionaron significantes visuales del diseño de experiencia y orden de la metodología 5S para comprender una clasificación sostenible y comprensible', 'S07','7'),
    claim('Registraron seis propuestas individuales y dos modificaciones grupales, con preguntas y aportes de Miguel e Ignacio sobre inventario virtual y mantenimiento del orden', 'S07','8'),
    claim('Contrastaron señalética e inventario web con supuestos de uso, resistencia del material y carga administrativa, y dejaron pendiente la disposición estudiantil para mantener el orden', 'S07','9'),
], claim('Identifican una mesa de objetos perdidos que se desorganiza rápidamente y dificulta encontrar pertenencias, con efectos para estudiantes y personal de apoyo', 'S07','3--5'), [
    claim('Proponen un inventario virtual accesible mediante la página del colegio', 'S07','8'),
    claim('Proponen una dinámica rotativa de estudiantes responsables de ayudar a organizar la mesa', 'S07','8'),
], 'La tabla C10 de la página PDF 9 presenta palabras apretadas y superpuestas en una celda; el párrafo de cierre permite verificar los límites resumidos, sin reconstruir lo que no se distingue con claridad ' + cite('S07','9') + '.')

group(6, 'Compra en cafetería durante el descanso',
      'Sebastián Lozano y Alejandro Camargo', cite('S08','1 y 3'), ['S08'], [6,15], [
    claim('Integraron el recorrido de compra y cinco hallazgos sobre espera, efectos en el descanso, colados, momento de compra y diferencias de acceso a dinero o tiquetes', 'S08','9--10'),
    claim('Priorizaron provisionalmente la oportunidad de la cafetería con 7 puntos y mantuvieron sin datos las alternativas sobre agua y baños', 'S08','11--12'),
    claim('Reformularon D1 para que los estudiantes de décimo compren su comida durante el descanso sin perderlo ni llegar tarde, sin atribuir toda la demora a la fila', 'S08','13--14'),
    claim('Conectaron decisiones económicas bajo incertidumbre con la prueba de universalización de Kant para examinar decisiones de compra y respeto del turno', 'S08','14'),
    claim('Registraron seis ideas individuales y dos colaborativas, junto con preguntas cruzadas y ampliaciones que combinaron autopedido, separación de entrega y pedidos con número', 'S08','15--17'),
    claim('Contrastaron IC1 e IC2 con las diferencias de pago y compra, ajustaron el acceso con carnet o tiquete y conservaron la posibilidad de pedir en la fila', 'S08','17--18'),
], claim('El equipo identifica filas y colados que hacen perder descanso, dificultan comer y pueden ocasionar llegadas tardías a clase', 'S08','6--10'), [
    claim('Proponen una pantalla de autopedido con carnet, tiquete o efectivo y recogida en una ventanilla separada, aún por verificar', 'S08','16 y 18'),
    claim('Proponen pedidos anticipados con número de turno, conservando la posibilidad de pedir en la fila para quien no lo hizo antes', 'S08','16 y 18'),
])

group(7, 'Separación de residuos en el patio',
      'Pablo José Del Cairo Bolaños y Nicolás Clavijo González', cite('S09','1'), ['S09'], [7,9], [
    claim('Relacionaron estudiantes, personal de aseo y recorrido de disposición de residuos con siete hallazgos y un supuesto, respaldados por observaciones y diez encuestas', 'S09','4--10'),
    claim('Compararon clasificación, acceso a canecas y carga de limpieza, y resolvieron el empate de 8 puntos entre A y B a favor de aprender a clasificar por su viabilidad', 'S09','11--12'),
    claim('Delimitaron D1 para ayudar a estudiantes de sexto a undécimo a identificar la caneca de cada residuo en el patio durante los descansos', 'S09','12'),
    claim('Conectaron significantes del diseño con el código de colores de separación de residuos y señalaron que faltaba verificar los rótulos y colores del patio', 'S09','13'),
    claim('Registraron seis ideas individuales, dos combinaciones grupales y aportes cruzados que modificaron la ubicación de canecas y la continuidad del mensaje visual', 'S09','14--15'),
    claim('Contrastaron información visual y agrupación de canecas, conservaron señales rápidas de entender y ajustaron la reubicación para no dejar zonas sin acceso cercano', 'S09','15'),
], claim('Describen residuos mezclados y basura en el piso durante los descansos, dudas para clasificar y trabajo adicional para las personas de aseo', 'S09','4 y 7--10'), [
    claim('Proponen que la información de cada empaque acompañe al estudiante desde la tienda hasta la caneca mediante la misma imagen y color', 'S09','14'),
    claim('Proponen estudiantes guías rotativos por grado que respondan dudas y reciban comentarios semanales del PAE sobre la separación', 'S09','14'),
])

group(8, 'Limpieza y conservación de graderías',
      'Andrés Camilo Maldonado Lemus, Carlos Samuel López Castrillón y Thomas Enrique Díaz Garzón', cite('S10','1 y 3'), ['S10','S11','S12','S13'], [10,14,17], [
    esc('Organizaron usuarios, recorrido y cuatro hallazgos sobre residuos en graderías a partir de una encuesta de treinta estudiantes ') + cite('S10','1--2') + '; ' + cite('S11','1--2') + '.',
    claim('Compararon acceso a recipientes, cultura ciudadana y reducción de empaques, y seleccionaron la primera oportunidad con 9 puntos, reconociendo el mantenimiento como limitación', 'S10','2--3'),
    esc('No puede verificarse C7 con un PDF de esta etapa, porque el enlace correspondiente S12 es un DOCX accesible y los PDF revisados solo aportan la encuesta y C5--C6 ') + cite('S10','1--3') + '; ' + cite('S11','1--2') + '.',
    esc('No puede verificarse C8 con un PDF de esta etapa, porque S12 está disponible en DOCX y no se cuenta con una versión PDF paginada de ese trabajo dentro de los enlaces del CSV ') + cite('S10','1--3') + '; ' + cite('S11','1--2') + '.',
    esc('No puede verificarse C9 con un PDF de esta etapa, porque S13 es un DOCX accesible y no debe confundirse esa limitación de formato con ausencia de trabajo del equipo ') + cite('S10','1--3') + '; ' + cite('S11','1--2') + '.',
    esc('No puede verificarse C10 con un PDF de esta etapa, porque el enlace S13 no aporta una versión PDF paginada y no se atribuyen sus afirmaciones a páginas inexistentes ') + cite('S10','1--3') + '; ' + cite('S11','1--2') + '.',
], claim('El grupo identifica acumulación recurrente de envolturas y envases en las graderías, y recoge opiniones que relacionan el abandono de residuos con hábitos y acceso a canecas', 'S10','1--2'), [
    esc('No se identificó un conjunto de ideas de solución en los PDF de este equipo: S10 declara que todavía no diseña una solución y S11 registra la encuesta; las posibles ideas de S13 quedan fuera de la verificación paginada en PDF ') + cite('S10','3') + '; ' + cite('S11','1--2') + '.',
], 'S11 no tiene lista de autores: se incorpora como anexo compartido en las filas 10, 14 y 17, por su mismo cuestionario de siete preguntas, treinta respuestas y correspondencia con las referencias P1--P7 de S10; los DOCX S12 y S13 son accesibles y su texto se inspeccionó para confirmar la continuidad e integrantes, pero no se usa para inventar citas PDF ni para afirmar ausencia de contenido.')

group(9, 'Tiempo y organización de cafetería',
      'Sofía Guampe G. y Nicolás Ospina R., según la portada', cite('S14','1'), ['S14'], [13,20], [
    claim('Organizaron contexto, recorrido y cinco hallazgos con observaciones y quince encuestas, distinguiendo sugerencias de resultados y reconociendo fechas y mediciones faltantes', 'S14','1--5'),
    claim('Compararon reducir la espera y mejorar el orden, conservaron sin datos la viabilidad y eligieron provisionalmente reducir la espera en el almuerzo', 'S14','6--7'),
    claim('Revisaron D1 para reducir el tiempo de espera de estudiantes de bachillerato que compran o reclaman durante el almuerzo, sin imponer un medio específico', 'S14','8'),
    claim('Relacionaron población y muestra con participación y escucha, aclarando que las conexiones se prepararon como apoyo y que faltaba conocer al personal', 'S14','9'),
    claim('Presentaron seis ideas y dos combinaciones como propuestas para explorar, con preguntas y aportes rotulados como propuestos y no como participación ya realizada', 'S14','10--11'),
    claim('Examinaron pedidos anticipados e información visible de productos mediante supuestos, condiciones de acceso y preguntas sobre causas de la demora y funcionamiento', 'S14','12--13'),
], claim('Describen esperas que dificultan comprar, comer y regresar a clase a tiempo, apoyándose en quince respuestas y observaciones cuya fecha no quedó registrada', 'S14','1--5'), [
    claim('Proponen explorar pedidos anticipados con reclamo diferenciado e información clara, sin imponer aplicación ni salida anticipada de clase', 'S14','10--13'),
    claim('Proponen combinar turnos por llegada con acuerdos claros y consulta a usuarios sobre el respeto del turno', 'S14','11'),
], 'La portada abrevia apellidos; la correspondencia con Sofía Guampe Granados y Nicolás Ospina Ramírez se sustenta conjuntamente en los nombres de la portada y el mismo enlace de las filas 13 y 20, sin tomar la tabla propuesta de participación como prueba de conversación efectuada ' + cite('S14','1 y 11') + '.')

group(10, 'Organización de responsabilidades académicas',
      'Julián Maldonado, único autor nombrado en la entrega', cite('S15','1 y 7'), ['S15'], [16], [
    claim('Describió los olvidos de materiales y entregas y reunió perspectivas de un estudiante y un profesor sobre carga académica, prioridades y utilidad de anotar pendientes', 'S15','1--2'),
    claim('Comparó priorizar tareas y anotar responsabilidades, y escogió registrar los pendientes por 8,5 puntos frente a 7,5 señalando que hay que consultar y actualizar las anotaciones', 'S15','2--4'),
    claim('Formuló un desafío sobre herramientas para evitar olvidos de estudiantes de bachillerato en sus espacios de estudio y justificó su relación con el registro de responsabilidades', 'S15','5'),
    claim('Relacionó psicología cognitiva y diseño UX/UI para comprender memoria y atención y orientar herramientas sencillas de consulta de pendientes', 'S15','5--6'),
    claim('Propuso mini tablero, chatbot y web, y atribuyó la discusión y revisión de las dos propuestas mejoradas a ChatGPT, sin presentar esa revisión como colaboración entre estudiantes', 'S15','6--7'),
    claim('Analizó el tablero y el sistema chatbot-web mediante lo conocido, supuestos de consulta y pendientes sobre ubicación, actualización y acceso a WhatsApp e internet', 'S15','7--8'),
], claim('La entrega identifica olvidos de trabajos, fechas y materiales escolares y la dependencia de préstamos de compañeros como respuesta temporal', 'S15','1--2'), [
    claim('Propone un mini tablero visual en el colegio para consultar pendientes y retirar información de actividades cumplidas, especialmente para quien no dispone de celular', 'S15','7'),
    claim('Propone un chatbot de WhatsApp que envíe recordatorios y enlaces a una web con tareas, materiales y fechas', 'S15','7'),
], 'El CSV conserva literalmente «MALDONADO BAQUERO JULIÁN ALEJAND...» y el PDF solo identifica a «Julián Maldonado»; el enlace permite asociar la entrega a la fila 16, pero no verificar la ampliación del nombre truncado ni todos sus apellidos ' + cite('S15','1') + '.')

group(11, 'Acceso a alimentación saludable y asequible',
      'Santiago Ospina Ramírez y Juan José Méndez', cite('S16','1') + '; ' + cite('S17','1') + '; ' + cite('S18','2--4'), ['S16','S17','S18'], [18,21], [
    claim('Organizaron contexto, recorrido y cuatro hallazgos sobre hábitos alimentarios, coste y disponibilidad, reconociendo que no documentaron acciones individuales del antes y después ni respuestas textuales', 'S16','1--5 y 10--11'),
    claim('Compararon disponibilidad en cafetería, barreras económicas y alimentación a lo largo del día, mantuvieron datos faltantes y priorizaron provisionalmente la primera oportunidad', 'S16','5--11'),
    claim('Delimitaron D1 al acceso a alternativas saludables y asequibles en la cafetería durante los descansos, dejando fuera otros momentos de alimentación', 'S17','1--3'),
    claim('Conectaron accesibilidad económica y análisis de precios con calidad nutricional, indicando que faltaban los materiales consultados y datos de oferta, precios y preferencias', 'S17','3--5'),
    claim('Registraron seis ideas individuales y dos colaborativas con preguntas y aportes de ambos integrantes, y aclararon que algunas propuestas excedían el alcance de D1', 'S18','1--4'),
    claim('Contrastaron ampliar el menú y promover alternativas menos procesadas con supuestos de compra, preferencias, precios y recursos, sin dar por demostrada la aceptación de las propuestas', 'S18','4--6'),
], claim('Describen dificultades para acceder a comida saludable y asequible y una observación de diez estudiantes en una sola fecha, cuyos resultados no generalizan a toda la institución', 'S16','1--4 y 10--11'), [
    claim('Proponen ampliar el menú de la cafetería con alimentos saludables, variados y asequibles', 'S18','3 y 5'),
    claim('Proponen alternativas menos procesadas acompañadas de campañas sobre agua y verduras, reconociendo que no está documentada esa preferencia específica', 'S18','3 y 5--6'),
], 'Los tres PDF coinciden en proyecto y autores, por lo que se verifican conjuntamente; S18 corrige el contexto de «vacaciones» a «descansos escolares» sin presentar datos nuevos, y su página PDF 7 está vacía, no ilegible ' + cite('S18','1 y 7') + '.')

group(12, 'Higiene y estado de los baños',
      '«Pedro y Santiago», nombres declarados en la portada', cite('S19','1'), ['S19'], [22,25], [
    claim('Organizaron perfiles, testimonios y una comparación entre olores, limpieza, daños y necesidades de usuarios de los baños', 'S19','1--3'),
    claim('Identificaron como necesidad baños limpios y en buen estado, pero no se identificó una matriz comparativa de oportunidades en el PDF legible', 'S19','1--4'),
    claim('Formularon y revisaron D1 para mejorar limpieza, olores y mantenimiento de baños usados por estudiantes de décimo durante la jornada', 'S19','3'),
    claim('Relacionaron higiene, microorganismos y saneamiento de Ciencias Naturales con responsabilidad colectiva y cuidado de espacios comunes', 'S19','3'),
    claim('No se identificó un registro de ideación C9 en el PDF legible, que finaliza con la verificación de C7--C8', 'S19','1--4'),
    claim('No se identificó un contraste de ideas C10 con evidencia del usuario en el PDF legible', 'S19','1--4'),
], claim('El documento aborda malos olores, suciedad y daños en los baños que producen incomodidad y hacen que algunos estudiantes eviten utilizarlos', 'S19','1--3'), [
    claim('Plantean mejorar el control y los horarios de aseo, como posibilidad mencionada y no como medida implementada', 'S19','2--3'),
    claim('Plantean reparar sanitarios, lavamanos y otras instalaciones en mal estado', 'S19','2'),
], 'Las filas 22 (Pedro Martín Ramírez Barrero) y 25 (Santiago Tapias López) comparten S19 y el nombre del archivo alude a «pedro y tape», pero el PDF solo dice «Pedro y Santiago»; se verifica ese equipo nominal y se deja pendiente la identidad completa de sus autores, especialmente el apellido de Santiago, sin fusionarlo con Santiago Ospina del grupo 11.')

group(13, 'Orden en las filas de compra y reclamo',
      'Tomás Rincón, trabajo individual', cite('S20','1 y 7'), ['S20'], [23], [
    claim('Integró el recorrido de compra y reclamo con tres hallazgos sobre colados, saturación del personal y pérdida del descanso, referidos a observaciones y entrevistas', 'S20','1--3'),
    claim('Comparó tres oportunidades e integró el orden y la prevención de colados con la delimitación y el acompañamiento, reconociendo permisos y disponibilidad como límites', 'S20','3--5'),
    claim('Retiró barandas y vigilancia de la pregunta inicial y formuló D1 sobre evitar colados y ordenar el flujo de compra y reclamo en ambos descansos', 'S20','5'),
    claim('Relacionó normas y autorregulación ciudadana con escasez, demanda, coste de oportunidad e incentivos, distinguiendo conocimientos de hipótesis de aceptación', 'S20','6'),
    claim('Registró tres ideas individuales y dos ampliaciones apoyadas en ciudadanía y economía, aclarando que el contraste fue individual aunque la tabla use la etiqueta de combinación grupal', 'S20','7--8'),
    claim('Contrastó supervisión y fila rápida, ajustó turnos breves y pago físico y dejó pendiente verificar disposición de monitores y capacidad del personal para separar flujos', 'S20','8--10'),
], claim('Describe colados y congestión en las dos filas de compra y reclamo, con saturación operativa y pérdida del tiempo de descanso', 'S20','2--3'), [
    claim('Propone un canal único con demarcación y cintas móviles, apoyado por un monitor en la entrada', 'S20','8'),
    claim('Propone una fila rápida para productos preempacados con efectivo exacto o ficha física, separada de los almuerzos', 'S20','8--10'),
], 'La etiqueta «combinación grupal/revisión» de la tabla no demuestra otros integrantes: la portada nombra solo a Tomás y la nota de C9 declara expresamente trabajo individual ' + cite('S20','1 y 7--8') + '.')

titles = {
'S01':'Álvarez y Ojeda, C5--C10','S02':'Ayala y Galán, acumulativo C3--C10',
'S03':'Ayala y Galán, Encuesta SBLM','S04':'González y Barón, C5--C6',
'S05':'González y Barón, Proyecto C7--C8','S06':'Isa y Lucio, hábitos de sueño',
'S07':'Caballero y Rodríguez, proyecto','S08':'Lozano y Camargo, C1--C10',
'S09':'Del Cairo y Clavijo, residuos','S10':'Díaz, Maldonado y López, C5--C6',
'S11':'Encuesta de graderías, 30 estudiantes','S12':'López, Díaz y Maldonado, C7--C8 (DOCX)',
'S13':'Maldonado, López y Díaz, C9--C10 (DOCX)','S14':'Guampe y Ospina, cafetería',
'S15':'Julián Maldonado, organización académica','S16':'Ospina y Méndez, C5--C6',
'S17':'Ospina y Méndez, C7--C8','S18':'Ospina y Méndez, C9--C10',
'S19':'Pedro y Santiago, baños','S20':'Tomás Rincón, filas'}

preamble = r'''\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[spanish,es-nodecimaldot]{babel}
\usepackage{lmodern,microtype}
\usepackage[margin=2.05cm]{geometry}
\usepackage{xcolor,enumitem,longtable,booktabs,array}
\usepackage{titlesec,fancyhdr}
\usepackage[unicode,colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!55!black]{hyperref}
\usepackage{xurl}
\definecolor{Ink}{HTML}{243B53}
\titleformat{\section}{\Large\bfseries\color{Ink}}{}{0pt}{}
\titleformat{\subsection}{\normalsize\bfseries\color{Ink}}{}{0pt}{}
\titlespacing*{\section}{0pt}{0pt}{9pt}
\titlespacing*{\subsection}{0pt}{9pt}{4pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\setlength{\emergencystretch}{3em}
\setlist[itemize]{leftmargin=1.2em,itemsep=4pt,topsep=3pt}
\setlist[description]{leftmargin=0pt,labelsep=0.6em,itemsep=6pt,style=unboxed}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small Seminarios · Primer período · 2026--2027}
\fancyhead[R]{\small Resumen documental}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\newcommand{\evid}[2]{(\csname src#1\endcsname, páginas PDF #2)}
\makeatletter
\newcommand{\sourceurl}[2]{\hyper@linkurl{#2}{#1}}
\makeatother
\hypersetup{pdftitle={Resumen de trabajos de seminarios, primer período},pdfauthor={Síntesis documental de entregas}}
'''

out = [preamble]
for s in sources:
    # Percent signs are catcode 12 inside detokenize only when they reach TeX;
    # use a catcode group to preserve the exact percent-encoded CSV URL.
    out.append(r'\begingroup\catcode`\%=12' + '\n' +
        r'\expandafter\gdef\csname src' + s['id'] + r'\endcsname{\sourceurl{' + s['url'] + '}{' + esc(titles[s['id']]) + '}}' + '\n' + r'\endgroup' + '\n')

out.append(r'''\begin{document}
\begin{center}
{\LARGE\bfseries\color{Ink} Resumen de los trabajos de seminarios}\\[5pt]
{\large Primer período · Segunda evidencia de aprendizaje}\\[3pt]
Curso 2026--2027 · Revisión documental: 12 de noviembre de 2026
\end{center}

\subsection*{Alcance y lectura de las fuentes}
Este documento resume lo que se pudo verificar en las entregas; no reevalúa, califica ni modifica resultados del CSV o archivos de estudiantes. Las guías C5--C6, C7--C8 y C9--C10 se usaron únicamente para interpretar los criterios, nunca como evidencia de trabajo realizado.

El registro de cobertura comprende \textbf{25 filas de estudiantes, 20 enlaces distintos, 18 PDF y 2 DOCX}; los PDF suman \textbf{146 páginas}, leídas mediante extracción completa de texto y revisión de sus páginas renderizadas, incluidas tablas y páginas vacías. Los enlaces son locales y conservan los destinos del CSV: para abrirlos se necesita acceso a esas rutas. Los anexos finales relacionan cada fila, cada enlace y su estado.

\textbf{Convención de citas:} todas las referencias indican la posición de página dentro del PDF, comenzando en 1, y no una sección ni una etiqueta impresa. Cuando falta numeración impresa, la posición sigue contando; S18, por ejemplo, tiene una séptima página vacía. Los títulos de las citas son enlaces a la fuente y el registro de fuentes muestra el nombre de archivo completo.

\textbf{Numeración y pertenencia:} no se identificó un número de grupo declarado en las entregas PDF ni un conflicto de números; por tanto, los números 1--13 son \textit{números asignados para este documento}, en orden de primera aparición de sus enlaces en el CSV. El campo \texttt{No} identifica una fila, nunca un grupo. Los equipos permanecen separados aunque investiguen cafetería, residuos u otros problemas similares. Los grupos 4 y 12 tienen autoría nominal verificable, pero identidad completa pendiente; la fila 16 conserva su nombre truncado.

\textbf{Límites de interpretación:} una propuesta escrita no demuestra que se haya implementado ni que funcione, y un guion de participación no demuestra una conversación efectuada. Los porcentajes descritos, cuando aparecen, pertenecen al relato del equipo y no son resultados de una nueva evaluación. Los DOCX se registran como accesibles, pero no se convierten en PDF de entrega ni reciben páginas PDF inventadas.

\subsection*{Contenido}
\begin{itemize}
\item Trece secciones de equipos o autores documentales, cada una con C5--C10, problema e ideas identificables.
\item Casos pendientes y limitaciones: identidades, fuentes, legibilidad y evidencia faltante.
\item Anexo A: cobertura de las 25 filas del CSV.
\item Anexo B: registro de los 20 enlaces distintos y su lectura.
\end{itemize}
''')

for g in groups:
    out += [r'\clearpage'+'\n', r'\section*{Grupo '+str(g['number'])+': '+esc(g['title'])+'}'+'\n',
            r'\textit{Número asignado para este documento.}'+'\n\n',
            r'\textbf{Integrantes documentados:} '+esc(g['members'])+' '+g['membership']+'.\n\n',
            r'\textbf{Fuentes enlazadas:} '+ '; '.join(rf'\hyperlink{{fuente-{s}}}{{{s}}}: \csname src{s}\endcsname' for s in g['ids'])+'.\n\n',
            r'\begin{description}'+'\n']
    for c, text in zip(range(5,11),g['criteria']):
        out.append(rf'\item[\textbf{{C{c}}}] '+text+'\n')
    out += [r'\end{description}'+'\n',r'\subsection*{Problema abordado}'+'\n'+g['problem']+'\n',
            r'\subsection*{Ideas de solución}'+'\n'+r'\begin{itemize}'+'\n']
    for idea in g['ideas']: out.append(r'\item '+idea+'\n')
    out.append(r'\end{itemize}'+'\n')
    if g['note']: out.append(r'{\small\textbf{Nota de verificación:} '+(g['note'] if '\\' in g['note'] else esc(g['note']))+'}\n')

out.append(r'''\clearpage
\section*{Casos pendientes y limitaciones}
\subsection*{Identidades y relaciones entre entregas}
\begin{itemize}
\item \textbf{Filas 4 y 8, grupo 4:} el CSV asocia S06 con Lucio Barrero Sánchez y Ana Isabella Colorado Parrado, mientras que el PDF usa «Lucio» e «Isa» y no presenta una lista de nombres completos; falta confirmar la equivalencia, especialmente la de «Isa», sin atribuirle automáticamente el nombre de la fila 8 \evid{S06}{7 y 10}.
\item \textbf{Filas 22 y 25, grupo 12:} la portada solo declara «Pedro y Santiago»; el enlace común y el nombre de archivo no prueban por sí solos que los apellidos sean Ramírez Barrero y Tapias López, por lo que esa identificación permanece pendiente \evid{S19}{1}.
\item \textbf{Fila 16, grupo 10:} el nombre del CSV está truncado como «MALDONADO BAQUERO JULIÁN ALEJAND...» y el PDF solo nombra «Julián Maldonado»; queda pendiente verificar su identidad completa, sin ampliar el registro original \evid{S15}{1}.
\item \textbf{Integrante fuera del CSV:} Thomas Álvarez está expresamente nombrado en el grupo 1, pero no figura entre las 25 filas y no se le inventa un registro \evid{S01}{1}.
\item \textbf{Autoría anónima y participación:} el grupo 1 nombra a sus integrantes en portada pero deja anónimos autores de ideas y registros de escucha; no se verifican aportes individuales a partir de esas etiquetas \evid{S01}{1 y 7--8}.
\item \textbf{Anexo sin autores:} S11 no declara integrantes; se conserva asociado al grupo 8 mediante los tres enlaces compartidos del CSV y la correspondencia de cuestionario y registros con S10, sin atribuirle una portada inexistente \evid{S10}{1--3}; \evid{S11}{1--2}.
\end{itemize}

\subsection*{Fuentes, legibilidad y evidencia no verificable}
\begin{itemize}
\item \textbf{Acceso:} ninguno de los 20 enlaces locales resultó inaccesible; no hubo fallos de extracción que se interpretaran como ausencia de contenido.
\item \textbf{S06, legibilidad parcial:} en la página PDF 4 hay líneas superpuestas en la tabla de hallazgos; en la 5, en las tablas de criterios y comparación; en la 6, en la tabla de disciplinas; y en la 10, en la tabla de ideas, por lo que la revisión se apoya en texto recuperable, listas y explicaciones narrativas y no asegura la lectura de cada celda como tabla \evid{S06}{4--6 y 10}.
\item \textbf{S07, celda con superposición:} la tabla de la página PDF 9 tiene palabras superpuestas en la fila del inventario virtual; sus límites generales se verificaron con el párrafo de cierre, sin reconstruir el texto que no se distingue \evid{S07}{9}.
\item \textbf{S18, página vacía:} la página PDF 7 se inspeccionó y no contiene contenido visible; es una página vacía y no evidencia de un fallo de lectura \evid{S18}{7}.
\item \textbf{Grupo 8, formatos distintos:} S12 (C7--C8) y S13 (C9--C10) son DOCX accesibles; su texto permite reconocer continuidad y nombres, pero no se dispone de PDF de esas etapas en los enlaces del CSV, de modo que C7--C10 y las ideas se dejan pendientes de verificación paginada en PDF, sin afirmar que esos archivos no tengan trabajo.
\item \textbf{Grupo 3, C9 y C10:} no se identificaron registros de esas etapas ni ideas de solución en los PDF legibles enlazados, que desarrollan C5--C8 \evid{S04}{1--8}; \evid{S05}{1--6}.
\item \textbf{Grupo 12, C9 y C10:} no se identificaron esas etapas en S19, que finaliza con la verificación de C7--C8; su descripción de necesidades no incluye una matriz de priorización C6 \evid{S19}{1--4}.
\item \textbf{Grupo 2, C6:} se identifica la necesidad prioritaria de reducir espera, pero no una matriz comparativa de oportunidades en los PDF revisados, aunque S03 lleve C5--C6 en su título \evid{S02}{1--5}; \evid{S03}{1--3}.
\item \textbf{Propuestas y hechos:} el grupo 9 rotula como propuestas varias preguntas y aportes de participación; no se afirman como conversación efectuada \evid{S14}{10--11}; el autor del grupo 10 atribuye las propuestas mejoradas a discusión con ChatGPT \evid{S15}{7}; Tomás Rincón declara trabajo individual pese a usar «combinación grupal/revisión» en una fila \evid{S20}{7--8}.
\end{itemize}

\subsection*{Cierre de cobertura}
Se contabilizaron las 25 filas y cada una tiene al menos un enlace; \textbf{no hay estudiantes sin trabajo enlazado en este CSV}. Esto no elimina las identidades pendientes ni implica que todas las etapas estén documentadas. No se identificaron conflictos de numeración ni relaciones entre equipos que justifiquen nuevas fusiones. Persisten únicamente las limitaciones e identidades indicadas arriba y los pendientes propios de cada propuesta que las secciones describen con sus fuentes.

\clearpage
\section*{Anexo A. Cobertura de cada fila del CSV}
Se conserva el nombre de \texttt{ESTUDIANTES} tal como está registrado, incluido el truncamiento de la fila 16. «V» indica correspondencia documental con el equipo; «P» indica identidad completa pendiente. La pertenencia se comprueba en las páginas de integrantes citadas, junto con los enlaces asociados, y no a partir de porcentajes o resultados Yes/No.

\small\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}p{0.045\linewidth}>{\raggedright\arraybackslash}p{0.34\linewidth}p{0.065\linewidth}>{\raggedright\arraybackslash}p{0.16\linewidth}>{\raggedright\arraybackslash}p{0.30\linewidth}@{}}
\toprule
Fila & ESTUDIANTES & Grupo & Fuentes enlazadas & Estado y respaldo de pertenencia \\
\midrule
''')
rowgroup = {r:g for g in groups for r in g['rows']}
pending = {4,8,16,22,25}
for r in rows:
    n=int(r['No']); g=rowgroup[n]
    ids=[s['id'] for s in sources if r['No'] in s['rows']]
    status=('P: nombre incompleto; ' if n in pending else 'V: ')+g['membership']
    out.append(f"{n} & {esc(r['ESTUDIANTES'])} & {g['number']} & {', '.join(ids)} & {status} \\\\\n")
    if n == 13:
        out.append(r'''\bottomrule\end{tabular}\normalsize
\clearpage\section*{Anexo A. Cobertura del CSV (continuación)}
\small
\begin{tabular}{@{}p{0.045\linewidth}>{\raggedright\arraybackslash}p{0.34\linewidth}p{0.065\linewidth}>{\raggedright\arraybackslash}p{0.16\linewidth}>{\raggedright\arraybackslash}p{0.30\linewidth}@{}}
\toprule Fila & ESTUDIANTES & Grupo & Fuentes enlazadas & Estado y respaldo de pertenencia \\
\midrule
''')
out.append(r'\bottomrule\end{tabular}\normalsize'+'\n')

out.append(r'''\clearpage
\section*{Anexo B. Registro de enlaces y lectura}
Los identificadores S01--S20 se asignan por primera aparición del enlace, deduplicando el campo completo con un parser CSV compatible con celdas multilínea. Cada título de fuente abre el destino original y cada nombre de archivo permite reconocer la entrega. «Leído» comprende texto completo y revisión de páginas renderizadas en PDF; las limitaciones parciales se individualizan aquí.
\titleformat{\subsection}{\small\bfseries\color{Ink}}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{6pt}{2pt}
\setlength{\parskip}{3pt}
''')
for s in sources:
    ident=s['id']
    status = f"PDF accesible, leído e inspeccionado visualmente: páginas PDF 1--{s['pages']}" if 'pages' in s else 'DOCX accesible; texto inspeccionado para continuidad e integrantes, sin paginación PDF y sin uso como evidencia sustantiva en esta síntesis de PDF'
    if ident=='S06': status += '; tablas parcialmente legibles en páginas PDF 4, 5, 6 y 10, con apoyo en texto recuperable y narrativa'
    if ident=='S07': status += '; superposición parcial en una celda de la página PDF 9, con apoyo en el cierre narrativo'
    if ident=='S18': status += '; página PDF 7 vacía y revisada'
    if ident=='S11': status += '; no declara autores, se asocia por CSV y correspondencia del cuestionario con S10'
    out += [rf'\subsection*{{\hypertarget{{fuente-{ident}}}{{{ident}}}: \csname src{ident}\endcsname}}'+'\n',
            r'{\small\textbf{Archivo:} '+r'\texttt{'+esc(s['filename']).replace(r'\_',r'\_\allowbreak{}')+'}'+'\n\n',
            r'\textbf{Filas vinculadas:} '+', '.join(s['rows'])+'. '+esc(status)+'.}\n']

out += [r'\end{document}'+'\n']
tex=''.join(out)
(BASE/'seminars_summary.tex').write_text(tex,encoding='utf-8')
ledger = {'csv_rows':len(rows),'distinct_links':len(sources),'pdf_count':18,'pdf_pages':sum(s.get('pages',0) for s in sources),'docx_count':2,
          'csv_sha256':csv_hash,'sources':sources,'groups':groups,
          'row_coverage':[{'row':r['No'],'student':r['ESTUDIANTES'],'group':rowgroup[int(r['No'])]['number'],'status':'identity_pending' if int(r['No']) in pending else 'verified','sources':[s['id'] for s in sources if r['No'] in s['rows']]} for r in rows]}
(REVIEW/'coverage_evidence_ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
assert set(rowgroup)==set(range(1,26))
assert len(re.findall(r'\\item\[\\textbf\{C(?:5|6|7|8|9|10)\}\]',tex))==78
assert all('\\evid{' in c for g in groups for c in g['criteria'])
for s in sources:
    assert hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()==s['sha256'], s['id']
assert hashlib.sha256((BASE/'resultados_criterios.csv').read_bytes()).hexdigest()==csv_hash
print(f'Wrote {BASE / "seminars_summary.tex"}; 13 sections, 78 criterion entries, 25 covered rows, 20 links, source hashes unchanged')
