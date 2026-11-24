from pathlib import Path
import re

root = Path('book2026-2027/seminars/term_2')
common = r'''\section*{Documento acumulativo e integridad de la evidencia}
Continúen el \textbf{documento acumulativo en LaTeX} en \guidelink{https://www.overleaf.com/}{Overleaf} o su editor habitual; entreguen fuente y PDF actualizado. Distingan \textbf{P1} y \textbf{P2}. Enlacen evidencias, decisiones, versiones y resultados por códigos o referencias internas, con fuentes y fechas reales.

Distingan \concept{observaciones y comentarios}, \concept{interpretaciones}, \concept{supuestos} e \concept{ideas}; identifiquen simulaciones y límites. \instruction{Usen IA solo para código LaTeX, formato y organización de contenido propio.} No inventen evidencias.

Actualicen la \textbf{bitácora} por sesión: fecha, aportes, evidencias, compromisos, responsables, plazos, estados y acuerdos. Las guías admiten proyectos físicos, digitales, comunicativos, de servicios o procedimentales. Adapten medios y extensión a la evidencia necesaria; los formatos sugeridos son opciones.
'''

data = [
('C1C2', 'Coevalúen propuestas y fundamenten decisiones', r'''Recuperen el reto D1 (P1, C7) y los hallazgos H sobre el usuario (P1, C5). Participen en la evaluación de propuestas de otros equipos y usen lo aprendido para formular alternativas y justificar decisiones del proyecto propio.''', r'''
\section*{C1 de P2. Observen, pregunten y propongan alternativas}
\begin{enumerate}[series=pasos]
\item \textbf{Antes: preparen la coevaluación.} Lean el \guidelink{file:checklist_evaluativo_feria.pdf}{checklist de coevaluación}. Acuerden quién observa, pregunta y registra, con participación de todo el equipo. Identifiquen grupo evaluador, curso y proyectos evaluados. Usen los espacios según las propuestas observadas, sin inventar datos para llenar casillas.
\item \textbf{Durante: escuchen y documenten.} Observen la explicación y los recursos de cada equipo. Formulen preguntas para aclarar usuario, necesidad, funcionamiento, respaldo o viabilidad. Registren preguntas, respuestas y hechos localizables por proyecto; separen lo visto u oído de su interpretación. Eviten juicios como «es excelente» sin indicar qué los respalda.
\item \textbf{Evalúen con el instrumento intacto.} Atiendan sus siete categorías: comprensión de la problemática; claridad y organización de la información; dominio y conocimiento del tema; innovación y pertinencia de la solución; viabilidad e impacto; comunicación y uso de recursos; gestión del tiempo y trabajo en equipo. En cada ítem usen \textbf{E = Se evidencia, P = Parcialmente, A = Aún no se evidencia, N = No se observa}. Vinculen las marcas a sus notas; si algo no se observó, no lo conviertan en una afirmación de inexistencia. Estas categorías son del checklist: \textbf{no equivalen a C1--C10 de P2}.
\item \textbf{Después: elaboren alternativas.} Completen por proyecto los campos \textbf{Problemática, Fortaleza, Mejora concreta, Solución alternativa y Cómo o por qué}. Expliquen cómo funcionaría la alternativa o por qué ayudaría. Desarrollen alternativas con mecanismos distintos, a partir de lo observado, las preguntas y las ideas propias; identifiquen a qué problemática responde cada una y su origen. No basta cambiar el nombre o la apariencia de una idea.
\end{enumerate}

\section*{Entregables de C1}
Incorporen el checklist diligenciado y legible, con sus marcas y campos completos para los proyectos observados, y las notas vinculadas. La evidencia específica de C1 es \textbf{Solución alternativa y Cómo o por qué}, junto con una elaboración propia que explique la variedad de mecanismos y su relación con las problemáticas. Las demás categorías contextualizan la evaluación; una marca por sí sola no demuestra C1.

\newpage
\section*{C2 de P2. Comparen y justifiquen una selección}
\begin{enumerate}[resume=pasos]
\item \textbf{Analicen la retroalimentación.} Revisen las marcas y los campos Problemática, Fortaleza y Mejora concreta junto con sus respaldos. Compartan respetuosamente las devoluciones con los equipos evaluados; registren las aclaraciones recibidas y qué cambió en su interpretación. Si reciben comentarios sobre su proyecto, identifiquen su procedencia. No atribuyan comentarios que no recibieron.
\item \textbf{Conecten con el proyecto propio.} Expliquen qué aprendizajes de la coevaluación son pertinentes para su usuario y D1, y cuáles no pueden trasladar sin comprobarlos. Retomen sus ideas de P1 y desarrollen alternativas propias (por ejemplo, ALT1, ALT2). Citen las propuestas ajenas que inspiraron una idea y expliquen la adaptación, sin presentarlas como creación del equipo.
\item \textbf{Comparen opciones con el mismo marco.} Organicen una comparación que identifique cada alternativa y su mecanismo, el valor esperado para el usuario y su respaldo, la viabilidad (recursos, tiempo, acceso y condiciones) y la coherencia con D1. Pueden usar una matriz o un análisis por opciones. Marquen «sin datos» cuando falte evidencia y señalen cómo obtenerla; las marcas del checklist no sustituyen esta comparación.
\item \textbf{Justifiquen la selección.} Expliquen qué opción eligen para el proyecto propio, frente a las opciones descartadas, y qué evidencias o condiciones pesaron en la decisión. Distingan la evidencia del usuario de lo aprendido al observar otros proyectos. Si dependen de un supuesto decisivo, declaren la elección provisional y qué falta comprobar. Registren el acuerdo y los compromisos en la bitácora.
\end{enumerate}

\section*{Entregables de C2}
Agreguen al documento acumulativo el análisis del checklist (marcas respaldadas y campos \textbf{Problemática, Fortaleza y Mejora concreta}, relacionados con las alternativas), la comparación propia y la selección argumentada para su proyecto. Incluyan referencias a observaciones, preguntas, comentarios y condiciones de viabilidad. Expliquen qué aprendizaje adoptan y qué decisión justifican con él. \textbf{El instrumento aporta insumos; la comparación y la decisión propias evidencian C2}.

\section*{Resultado y continuidad}
Conserven el instrumento original y sus notas en una sección de coevaluación, e identifiquen alternativas, elección y supuestos en la sección del proyecto propio. En C3--C4 representarán y materializarán esa elección. La bitácora permitirá revisar la colaboración en C9.

\section*{Verificación final}
\begin{itemize}[label=\checkbox]
\item Respetamos categorías, escala y campos del checklist, sin confundirlos con C1--C10.
\item Las marcas tienen respaldo y distinguimos observación, comentario e interpretación.
\item Las alternativas explican mecanismos; la selección propia compara valor, viabilidad y coherencia.
\item El documento acumulativo enlaza coevaluación, decisiones y bitácora.
\end{itemize}
'''),
('C3C4', 'Representen y construyan la primera versión', r'''Recuperen D1 y los H de P1, las alternativas y la selección propia fundamentada en la coevaluación de C1--C2 de P2. Identifiquen qué aprendizaje adoptaron y qué supuesto necesita exploración. C3 comunica la propuesta; C4 la convierte en una primera versión que se puede recorrer.''', r'''
\section*{C3 de P2. Representen la propuesta elegida}
\begin{enumerate}[series=pasos]
\item \textbf{Delimiten lo que deben comunicar.} Identifiquen usuario, necesidad, contexto y relación con la propuesta elegida en C2. Expliquen qué busca lograr la persona y cómo respondería la solución; distingan el funcionamiento previsto de lo ya comprobado.
\item \textbf{Hagan comprensibles las partes o pasos.} Representen componentes, secuencia, acciones del usuario y respuestas de la solución. Pueden usar bocetos anotados, diagramas, pantallas, guiones, mapas de servicio u otro medio pertinente. Incluyan conexiones, entradas y resultados previstos cuando sean necesarios para entender el funcionamiento. El formato debe servir a su proyecto.
\item \textbf{Incorporen y expliquen R1.} Den a la representación un código, título y fecha; inclúyanla legible en el documento acumulativo con una explicación que enlace D1, los H pertinentes y la selección de C2. Señalen la función o interacción que construirán primero, por qué es relevante y qué queda fuera de esta versión.
\end{enumerate}

\section*{Entregables de C3}
Una representación R1 anotada y su explicación, incorporadas en la sección C3 del documento acumulativo. Deben permitir comprender \textbf{usuario, necesidad, funcionamiento, partes o pasos y relación con la propuesta elegida}, así como el alcance de la primera construcción. Conserven su fuente editable si se elaboró fuera de LaTeX. Esta evidencia describe la propuesta; la construcción se registra por separado en C4.

\newpage
\section*{C4 de P2. Materialicen la primera versión de baja fidelidad}
\begin{enumerate}[resume=pasos]
\item \textbf{Traduzcan R1 en algo que se pueda usar o recorrer.} Identifiquen qué partes deben existir para mostrar una función o interacción relevante, qué acción hará la persona y qué respuesta podrá percibir. Elijan recursos accesibles al equipo: por ejemplo, un modelo físico, pantallas enlazadas, una pieza comunicativa, una representación de servicio o un procedimiento ejecutable. No necesitan construir toda la solución final.
\item \textbf{Acuerden cómo iniciar la construcción.} Abran PL1 con tareas vinculadas a R1, responsables y roles, recursos y acceso, plazos y dependencias. Registren las condiciones aún no resueltas. Conserven este punto de partida para el seguimiento de C6: el plan ayuda a construir, pero no sustituye el prototipo de C4.
\item \textbf{Construyan V1 y hagan un recorrido interno.} Ejecuten la función o interacción para revisar que se puede mostrar. Identifiquen partes operativas, partes simuladas y partes pendientes; si alguien del equipo simula una respuesta, expliquen cómo. Anoten dificultades de construcción y decisiones. Este recorrido sirve para revisar la versión dentro del equipo; \textbf{no equivale a la prueba con usuarios, pares o docentes de C7}.
\item \textbf{Documenten la versión real.} Registren fecha, código V1 y su relación con R1. Incluyan fotos, capturas, un registro de ejecución, una secuencia anotada u otro soporte que muestre la acción y su respuesta. Si el prototipo queda fuera del PDF, indiquen cómo acceder a él y conserven en el documento evidencia comprensible. Actualicen PL1 y la bitácora con lo realizado y sus pendientes.
\end{enumerate}

\section*{Entregables de C4}
El \textbf{prototipo V1 de baja fidelidad disponible para recorrer una función o interacción}, más su registro en la sección C4 del documento acumulativo: identificación y fecha, relación con R1, evidencia de uso, alcance, simulaciones y limitaciones. Adj unten el registro inicial PL1 y enlacen la bitácora. El soporte debe mostrar lo materializado, no solo una intención o un dibujo sin interacción representable.

\section*{Resultado y continuidad}
Conserven R1 y V1 como referencias de origen. C4 materializa la primera versión; durante la continuación de la construcción, C5 justificará decisiones aplicadas y C6 mostrará cómo organizan y ejecutan el trabajo. Pueden revisar R1 si cambia la propuesta, conservando las versiones y sus motivos.

\section*{Verificación final}
\begin{itemize}[label=\checkbox]
\item R1 comunica usuario, necesidad, funcionamiento, partes o pasos y elección de C2.
\item V1 permite mostrar o recorrer una función relevante y reconoce lo simulado.
\item Separamos los entregables de representación y construcción.
\item Incorporamos R1, V1, PL1 y bitácora al documento acumulativo con referencias.
\end{itemize}
'''),
('C5C6', 'Continúen la construcción y documenten el avance', r'''Recuperen R1, V1 y PL1 (P2, C3--C4), D1 y los H pertinentes (P1). Continúen el mismo proceso: \textbf{C4 materializa la primera versión; C5 aplica y justifica decisiones en el prototipo; C6 organiza y ejecuta su construcción}. Desarrollen C5 y C6 de manera articulada: una decisión puede cambiar las tareas y el avance puede exigir revisar una decisión.''', r'''
\section*{C5 de P2. Apliquen y justifiquen decisiones en el prototipo}
\begin{enumerate}[series=pasos]
\item \textbf{Identifiquen necesidades de diseño.} Recorran V1 y consulten los H y las decisiones previas. Localicen una dificultad o requisito pertinente de diseño, funcionalidad, accesibilidad o experiencia de usuario. Expliquen para quién importa y qué evidencia lo respalda; si es una hipótesis del equipo, declárenla.
\item \textbf{Decidan y construyan.} Elijan soluciones pertinentes y aplíquenlas mientras continúan la construcción. Expliquen por qué cada decisión responde al requisito y qué condiciones o alternativas consideraron. Pueden intervenir componentes, instrucciones, secuencias, interacciones o medios de acceso según el proyecto. Coordinen recursos y tareas con C6 a medida que trabajan.
\item \textbf{Hagan visible la aplicación.} Identifiquen la versión resultante como V2 (o con el código que corresponda a su historial). Localicen las decisiones en fotos, capturas, secuencias, registros de ejecución u otros soportes. Vinculen cada decisión con el principio, la necesidad o dificultad, su fundamento y el paso de R1 afectado. Señalen qué observarían en C7 para comprobar su efecto; no afirmen todavía que mejoró el uso.
\end{enumerate}

\section*{Entregables de C5}
Incorporen en C5 un \textbf{registro de decisiones aplicadas y justificadas}, enlazado a la versión construida y a sus soportes: principio pertinente, dificultad o requisito, fuente, decisión, ubicación y señal para la prueba. Mantengan disponible el prototipo. Remitan a V1 en C4 sin volver a entregar su construcción como evidencia nueva; C5 debe mostrar la aplicación razonada en el desarrollo del prototipo.

\newpage
\section*{C6 de P2. Organicen, ejecuten y sigan la construcción}
\begin{enumerate}[resume=pasos]
\item \textbf{Coordinen el trabajo real.} Retomen PL1 y acuerden tareas de construcción vinculadas a las decisiones de C5. Precisen responsables, roles, recursos disponibles y necesarios, acceso, tiempos y dependencias. Comprueben su disponibilidad y distribuyan el trabajo según lo que requiere el avance.
\item \textbf{Ejecuten y registren el avance.} Realicen las tareas y actualicen su estado con fecha: terminada, en curso, bloqueada o pendiente, según corresponda. Indiquen qué se hizo, quién lo hizo y dónde se ve el resultado en el prototipo o sus registros. No marquen como realizada una tarea solo porque fue asignada. Conserven la planificación inicial para compararla con la ejecución.
\item \textbf{Ajusten la organización durante la construcción.} Registren obstáculos y cambios de recursos, roles, secuencia o plazos; expliquen su motivo y efecto en el avance. Relacionen los cambios con decisiones de C5 y acuerdos de bitácora. Si no fue necesario reorganizar, justifiquen cómo el seguimiento confirmó que podían continuar.
\item \textbf{Cierren el estado disponible para C7.} Identifiquen la versión que podrán probar, la función o interacción disponible y sus límites o simulaciones. Señalen qué recursos de prueba están confirmados y qué falta gestionar. Preparar la prueba puede figurar en PL1, pero no reemplaza la evidencia de construcción ejecutada.
\end{enumerate}

\section*{Entregables de C6}
Agreguen a C6 \textbf{PL1 con historial de seguimiento y evidencia de ejecución}: tareas, responsables y roles, recursos, plazos, estado fechado, avance realizado y referencias a resultados. Incluyan el balance entre lo previsto y lo realizado y los ajustes de organización con su motivo; enlacen la bitácora. \textbf{Un plan sin avance documentado no evidencia por sí solo C6}. No dupliquen el registro de V1 de C4 ni sustituyan la justificación de C5 por una lista de tareas.

\section*{Resultado y continuidad}
Dejen disponibles el prototipo identificado (V2 o versión vigente), su evidencia de funcionamiento, R1 con cambios si corresponde, las decisiones de C5 y sus señales observables, PL1 actualizado y la bitácora. En C7 elegirán una prueba pertinente con usuarios, pares o docentes; en C8 aplicarán ajustes sustentados en los resultados y limitaciones.

\section*{Verificación final}
\begin{itemize}[label=\checkbox]
\item Las decisiones están aplicadas, localizadas y justificadas en el prototipo.
\item PL1 y la bitácora muestran ejecución, estados y ajustes de organización.
\item Distinguimos lo construido en C4, las decisiones de C5 y la gestión de C6.
\item La versión disponible y sus registros permiten preparar C7 sin atribuir resultados aún no observados.
\end{itemize}
'''),
('C7C8', 'Prueben el prototipo e implementen ajustes', r'''Recuperen la versión disponible al cierre de C5--C6, sus decisiones y señales observables, PL1 y la bitácora. Consulten D1 y los H de P1. El recorrido interno de construcción ayuda a preparar la prueba, pero C7 requiere una prueba efectivamente realizada con usuarios, pares o docentes.''', r'''
\section*{C7 de P2. Elijan, realicen y documenten una prueba pertinente}
\begin{enumerate}[series=pasos]
\item \textbf{Definan qué necesitan comprobar y por qué.} Vinculen el propósito a D1, una decisión o un supuesto. Pueden comprobar funcionamiento, comprensión, facilidad de uso, accesibilidad u otro aspecto justificado. Elijan una tarea que permita observarlo: por ejemplo, usar un objeto, navegar una interacción, interpretar un mensaje, recorrer un servicio o ejecutar un procedimiento.
\item \textbf{Preparen el registro PR1.} Identifiquen versión y fecha, contexto, participantes o perfiles y por qué son pertinentes, sin datos personales innecesarios. Escriban la tarea y la consigna, el procedimiento, los recursos, quién facilita y registra, y las señales observables con las que analizarán el resultado. Aclaren qué puede y qué no puede comprobar la prueba elegida.
\item \textbf{Realicen la prueba con las personas indicadas.} Permitan que intenten la tarea; registren ayudas, intervenciones, simulaciones e incidencias que puedan influir en el resultado. Recojan comentarios sobre momentos concretos, mediante preguntas abiertas. Identifiquen las condiciones reales y cualquier diferencia frente a lo previsto. Una conversación sobre la idea o el recorrido habitual del equipo no sustituyen la prueba del prototipo.
\item \textbf{Registren y analicen lo ocurrido.} Vinculen a PR1 observaciones de acciones y resultados, comentarios como citas o paráfrasis identificadas e interpretaciones del equipo, en apartados distintos. Contrasten las señales previstas con lo observado y expliquen qué pudieron comprobar, qué no y por qué. No generalicen más allá de los participantes y condiciones de la prueba.
\end{enumerate}

\section*{Entregables de C7}
Incluyan en C7 \textbf{PR1 realizado}: propósito y justificación, versión, fecha, participantes o perfiles, tarea, procedimiento previsto y ejecutado, señales observables, resultados y retroalimentación. Añadan soportes pertinentes (notas de observación, capturas, registros de ejecución u otros) con códigos y fuentes. Separen \textbf{observaciones, comentarios e interpretaciones}. El registro debe permitir reconstruir la prueba y sus límites; un protocolo sin ejecución no es suficiente.

\newpage
\section*{C8 de P2. Implementen y documenten ajustes sustentados}
\begin{enumerate}[resume=pasos]
\item \textbf{Decidan a partir de la evidencia.} Revisen PR1 y las limitaciones identificadas. Para cada ajuste, citen la observación, comentario o condición que lo motiva; expliquen qué deciden y por qué lo priorizan según la necesidad del usuario y los recursos. Las sugerencias pueden analizarse y descartarse con razones; no todas deben implementarse.
\item \textbf{Apliquen los cambios.} Construyan la versión ajustada, identificada como V3 o el código siguiente de su historial. Conserven la versión probada. Registren el antes y el después del elemento, paso o interacción afectada, mediante soportes adecuados al proyecto. Localicen la modificación y relacionen evidencia, decisión y cambio visible o ejecutable.
\item \textbf{Distingan expectativa de comprobación.} Expliquen el efecto que esperan de cada ajuste y qué permitiría comprobarlo. La prueba de la versión anterior no demuestra por sí sola que la nueva funciona mejor. Si realizan otra prueba, identifíquenla por separado (por ejemplo, PR2), con su versión, fecha, participantes, procedimiento y resultados, siguiendo el registro de C7. Si no la realizan, dejen el efecto como pendiente de comprobación.
\item \textbf{Documenten los pendientes.} Señalen cambios no implementados, razones y consecuencias para el alcance actual. Actualicen PL1 y la bitácora con el trabajo ejecutado y los acuerdos. No presenten propuestas futuras como ajustes ya realizados.
\end{enumerate}

\section*{Entregables de C8}
Incorporen en C8 el \textbf{prototipo ajustado disponible} y un registro que enlace, para cada ajuste implementado: evidencia motivadora, decisión y justificación, versiones, antes y después, ubicación del cambio y efecto esperado. Añadan resultados comprobados solo si existe una nueva prueba identificada, y pendientes justificados. Pueden usar una tabla, secuencia comentada u otro soporte legible; debe permitir verificar el cambio y su origen. Una lista de recomendaciones sin aplicación no sustituye esta evidencia.

\section*{Resultado y continuidad}
Conserven versiones, PR1 y las pruebas adicionales si existen, el registro de ajustes, PL1 y la bitácora en el documento acumulativo. C9--C10 retomarán lo realizado hasta C8 para hacer el balance de colaboración, explicar el valor diferencial y analizar retroalimentación final.

\section*{Verificación final}
\begin{itemize}[label=\checkbox]
\item La prueba fue realizada y permite reconstruir tarea, versión, participantes y resultados.
\item Separamos observación, comentario e interpretación con sus fuentes.
\item Los ajustes están implementados y muestran su evidencia, decisión, antes y después.
\item Diferenciamos efectos esperados, resultados comprobados y pendientes justificados.
\end{itemize}
'''),
('C9C10', 'Reflexionen y sustenten el cierre del proyecto', r'''Revisen el trabajo desarrollado hasta C8: D1 y los H de P1; coevaluación y selección, representación, versiones, decisiones, seguimiento, pruebas y ajustes de P2. El propósito es hacer un balance verificable del proyecto y de la colaboración, explicar su valor y analizar retroalimentación final.''', r'''
\section*{C9 de P2. Reconstruyan y valoren la colaboración}
\begin{enumerate}[series=pasos]
\item \textbf{Revisen la bitácora y contrasten sus registros.} Identifiquen aportes de cada integrante, compromisos, estados y resultados. Relaciónenlos con alternativas, decisiones, construcción, pruebas o ajustes. Si faltan registros, declaren la limitación; cualquier reconstrucción posterior debe identificarse como tal y citar su respaldo, sin inventar entradas pasadas.
\item \textbf{Sinteticen cómo trabajaron juntos.} Expliquen quién aportó qué y qué ocurrió con los compromisos: cumplidos, reprogramados o pendientes, con sus razones. Describan dificultades, acuerdos y cómo resolvieron desacuerdos de manera constructiva. Si no hubo un desacuerdo registrado, expliquen cómo escucharon razones para acordar una decisión real.
\item \textbf{Reflexionen con evidencia.} Relacionen los acuerdos y dificultades con sus efectos en el trabajo realizado. Expliquen qué aprendieron sobre cooperación, organización y comunicación, qué práctica les ayudó y qué podrían mejorar en otro proyecto. Distingan el hecho registrado de la interpretación del equipo y recojan las perspectivas de sus integrantes.
\end{enumerate}

\section*{Entregables de C9}
Agreguen en C9 una \textbf{síntesis verificable de colaboración}, por integrante y como equipo, sustentada en códigos o referencias a la bitácora y a los productos: aportes, compromisos y sus estados, acuerdos, dificultades y aprendizajes. Expliquen la relación entre colaboración y resultados, y declaren vacíos de registro. Conserven la bitácora completa; una valoración general como «trabajamos bien» sin respaldo no evidencia el criterio.

\newpage
\section*{C10 de P2. Expliquen el valor y analicen retroalimentación final}
\begin{enumerate}[resume=pasos]
\item \textbf{Construyan una explicación comparativa.} Retomen usuario y necesidad inicial de D1 y sus H. Comparen la solución disponible al cierre de C8 con la forma previa de atender la necesidad o con alternativas identificadas en C1--C2. Expliquen qué aporta de diferente, para quién y mediante qué característica, función o interacción concreta.
\item \textbf{Sustenten el alcance del valor.} Relacionen cada afirmación con rasgos demostrables del prototipo, resultados de pruebas y ajustes hasta C8. Identifiquen las versiones: distingan lo observado en la versión probada del beneficio esperado de un ajuste posterior. Expliquen limitaciones y condiciones de viabilidad; si algo no se comprobó, indíquenlo.
\item \textbf{Presenten el balance y reciban retroalimentación.} Compartan la explicación y las evidencias pertinentes con pares o docentes mediante una demostración, conversación, recorrido comentado u otro formato adecuado. Registren fecha, quién retroalimenta o su perfil, fortalezas, aspectos por mejorar y posibles pasos futuros, con referencia al trabajo presentado. Esta devolución final no reemplaza la prueba de C7 ni demuestra por sí sola el funcionamiento de una versión.
\item \textbf{Analicen y cierren.} Separen los comentarios recibidos de la interpretación del equipo. Expliquen qué aceptan, cuestionan o dejan pendiente y por qué, contrastándolo con sus evidencias. Cierren distinguiendo \textbf{lo realizado, lo aprendido y lo pendiente}. Los posibles pasos futuros son recomendaciones razonadas; \textbf{no constituyen una nueva fase obligatoria de construcción} ni deben presentarse como mejoras ya implementadas.
\end{enumerate}

\section*{Entregables de C10}
Incorporen en C10 la \textbf{explicación del valor diferencial}, con referente de comparación, necesidad inicial, evidencias del prototipo, pruebas y ajustes, versiones y límites. Añadan el registro de retroalimentación final y su análisis (fortalezas, aspectos por mejorar y posibles pasos futuros), con fuentes identificadas, y el balance de realizado, aprendido y pendiente. Conserven el soporte usado para presentar el trabajo o una descripción que permita reconstruir qué mostraron.

\section*{Resultado de cierre}
Entreguen el documento acumulativo en LaTeX y su PDF actualizado con las secciones C1--C10, la bitácora y referencias legibles a los soportes y versiones disponibles. El cierre sintetiza el trabajo hasta C8 y la reflexión de C9--C10; no requiere preparar una feria ni construir una versión adicional.

\section*{Verificación final}
\begin{itemize}[label=\checkbox]
\item La colaboración se sustenta en bitácora, aportes, compromisos y acuerdos reales.
\item El valor diferencial responde a la necesidad inicial y cita evidencias y versiones.
\item Recibimos y analizamos retroalimentación sin confundirla con resultados de prueba.
\item El balance distingue lo realizado, lo aprendido y lo pendiente, sin inventar logros.
\end{itemize}
''')]

for index, (code, title, start, body) in enumerate(data, 1):
    path = root / f'{code}-Activity.tex'
    old = path.read_text(encoding='utf-8')
    preamble = old.split(r'\hypersetup{pdftitle=')[0]
    criteria = re.search(r'(\\concept\{C\d+\.\}.*?)(?=\n\n)', old, re.S).group(1)
    pair = code.replace('C', '', 1).replace('C', '--C')
    pair = 'C' + pair
    heading = f'{pair}. {title}'
    result = preamble + '\\hypersetup{pdftitle={' + heading + '},pdfsubject={Emprendimiento e Innovación, Grado 10, Periodo 2}}\n\n'
    result += r'\begin{document}' + '\n\n' + r'\begin{center}' + '\n'
    result += r'{\Large\bfseries\color{HeadingColor} ' + heading + r'\par}' + '\n'
    result += r'''\vspace{3pt}
Emprendimiento e Innovación \enspace|\enspace Grado 10 \enspace|\enspace Periodo 2\\
''' + f'Guía {index} de 5\n' + r'\end{center}' + '\n\n'
    result += r'\section*{Objetivo y punto de partida}' + '\n' + criteria + '\n\n' + start + '\n\n' + common + body + '\n' + r'\end{document}' + '\n'
    result = result.replace('Adj unten', 'Adjunten')
    path.write_text(result, encoding='utf-8')
    print(path)
