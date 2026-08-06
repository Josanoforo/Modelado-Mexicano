Instrucciones del proyecto — "Psicología del Mexicano Contemporáneo" · v2.6

Por qué v2. La v1 (Bloque A + Bloque B) se diseñó para escribir un report temático. El proyecto creció a un programa multi-artefacto: reports temáticos + un integrador (meta-síntesis) + un modelo de decisión + validaciones forenses. Esta v2 conserva casi toda la v1 verbatim y solo añade o precisa lo que el proyecto probó que necesita. Cada cambio está marcado [NUEVO], [REFINADO] u [OPCIONAL] para que sea fácil aprobarlo o cortarlo. Todo lo no marcado es v1 sin cambios.

Por qué v2.1. Añade tres reglas de procedencia documental y una pregunta de auditoría, marcadas [NUEVO v2.1]. Atienden una clase de defecto distinta de todas las anteriores: no errores sobre México, sino afirmaciones del corpus sobre sí mismo —conteos, coberturas, versiones, referencias cruzadas— escritas a mano y nunca verificadas. Todo lo demás es v2 sin cambios.

Por qué v2.2. Añade la verificación de la restricción antes del diseño y la caducidad de las deudas asumidas, marcadas [NUEVO v2.2].

Por qué v2.3. Las versiones anteriores añadieron rigor y ninguna le puso precio. El resultado, medido el 30/jul/2026: una jornada de 15 PR, 40 entradas de cola, 3 ADR y 54 payloads registrados, con cero mediciones — 2 de 27 y 0 de 15 exactamente donde amanecieron. Ningún defecto catalogado ese día habría dañado a un lector: todos eran de contabilidad del programa sobre sí mismo. La v2.3 no retira ninguna regla de rigor. Añade la regla que dice cuándo el rigor está sustituyendo al trabajo, y acota el módulo de auditoría a los artefactos donde tiene función. Marcado [NUEVO v2.3] y [REFINADO v2.3].

Por qué v2.4. La v2.3 dijo: cada sesión produce una medición, o produce nada. El 4/ago/2026 el programa midió por primera vez — tres coeficientes de generador con dato propio, el cuarto veredicto del Hito D, dos abstenciones razonadas. Y medir resultó tener modos de falla que sintetizar nunca tuvo. Los tres que aparecieron ese día iban a meter números falsos al ejecutable, no frases falsas a un documento: un β̂ marginal que se invierte al condicionar, una cantidad en escala de desenlace a punto de escribirse en una casilla de escala de índice, y una escala de falsación sin fila donde anotar una regla que sobrevive. La v2.4 añade lo que medir enseñó, marcado [NUEVO v2.4], más una plantilla de arranque que no es regla y no paga impuesto. No retira nada.

Bloque A · Reglas transversales de rigor (aplican a TODO artefacto)

No trates a los mexicanos como un bloque homogéneo.

Segmenta siempre por región, clase, edad, género, escolaridad, urbanización, religiosidad, migración y exposición global.

Distingue en todo momento entre psicología individual, scripts culturales, adaptación racional al entorno, estructura económica e instituciones.

Separa explícitamente evidencia fuerte, evidencia media, hipótesis razonable y narrativa popular.

No romantices ni patologices a México.

No confundas desigualdad, violencia, informalidad o precariedad con cultura.

No extrapoles desde la clase media urbana digitalizada a todo México.

[REFINADO] El sesgo que más muerde es de clase dentro de la modernidad: el corpus sobre-muestrea al clasemediero urbano formal y sub-muestrea al popular informal (el peso demográfico dominante). Además, el sistema indígena-comunal vivo (asamblea, cargos, tequio, usos y costumbres) no es un "México sub-muestreado" sino otro orden institucional: queda fuera por diseño, no como hueco a rellenar. La huella indígena difusa (sincretismo, folk-psicología, mestizaje) sí vive dentro de la modernidad mestiza y ahí se mapea.

No importes marcos extranjeros (Hofstede, GLOBE, WVS, honor/dignidad/face) sin crítica.

[REFINADO] "Con crítica" no significa rechazar: significa ni importar ingenuamente ni rechazar por reflejo. La crítica de McSweeney a Hofstede es de validez de constructo, no prueba que las dimensiones no existan; IVR/UAI no "colapsan"; honor y dignidad no se oponen (r=.96 dignidad-face; los mexicanos se autoperciben como cultura de dignidad, no de honor). El anti-esencialismo también puede sobre-corregir.

No conviertas intuiciones en hechos.

Si no hay evidencia suficiente para una sección, dilo y no la rellenes.

Escribe el reporte final en español.

[NUEVO v2.3] Regla de señal — la que manda sobre las de abajo cuando chocan.

Cada sesión produce una medición, o produce nada. Defecto que no impide medir → una línea en forense/hallazgos.md y sigue. No se cataloga. Defecto que sí impide medir → se para y se reporta.

Un contador que no se mueve es el único síntoma que no admite interpretación. Si al cierre de una sesión 2 de 27 sigue en 2 de 27, esa sesión no avanzó, sin importar cuántos PR fusionó ni qué tan correcto era todo lo que escribió.

El aparato tiene costo y el costo se cuenta. Toda regla, test, ADR, convención de nombres o módulo obligatorio se paga en sesiones que no midieron. Antes de añadir cualquiera, se declara qué defecto real atrapó —uno que ya ocurrió, no uno concebible— y qué le habría costado a un lector. Si no le habría costado nada a un lector, es contabilidad interna: se anota y no se instrumenta.

Corolario, y es el que duele. Las reglas de procedencia de v2.1 y v2.2 se conservan íntegras: atraparon errores reales y baratos. Lo que se retira es su generalización — la idea de que si verificar es bueno, verificarlo todo siempre es mejor. Verificar tiene un precio, se paga en lo único escaso, y la auditoría de la auditoría no lo vale nunca.

(Por qué está aquí: el 30/jul el aparato de auditoría se volvió el trabajo. No por descuido — cada paso individual estaba justificado por una regla escrita. Ese es exactamente el modo de falla: un sistema de rigor sin criterio de suficiencia no se detiene solo, porque siempre queda algo por verificar y siempre es defendible verificarlo. La señal no puede ser "¿está bien hecho?"; tiene que ser un número que se mueve o no se mueve.)

[NUEVO] Regla de oro (procedencia por lectura). No reconstruyas tiers ni hallazgos de memoria: léelos de los reports, de sus mapas de evidencia y del glosario. Toda síntesis se construye leyendo, no recordando. Si un tier no está a la vista, ve a buscarlo antes de afirmarlo.

[NUEVO v2.1] Procedencia de la lectura (extensión de la Regla de oro). Leer no basta si no sabes de dónde. Toda afirmación sobre el contenido de un archivo se marca con su fuente: (1) leída del repo en esta sesión, con commit citable; (2) leída de un espejo del proyecto, que puede estar atrás del repo; (3) reportada por otra sesión o conversación, no verificada. Solo (1) entra al canon. Las de tipo (2) y (3) se formulan como pregunta a verificar, nunca como instrucción ni como hecho. Un espejo sin sello de commit no es fuente: no se puede distinguir un archivo vigente de uno que el repo ya borró. Si el espejo no declara de qué commit salió, se lee como (3), no como (2). (Por qué está aquí: la Regla de oro dice "léelo, no lo recuerdes" y no basta. Un archivo leído del espejo se siente exactamente igual que uno leído del repo, y un artefacto borrado por ADR sigue ahí, legible y falso.)

[REFINADO v2.4] Y el espejo sí engaña, con número. Medido el 4/ago/2026: el espejo del proyecto estaba en estado-programa v1.7 contra v1.9 del repo, gobernanza v1.8 contra v1.15, modelo-decision v3.2 contra v4.0, y 24 fichas contra 27. Quien derivara el contador del espejo obtenía 1 de 27 aplicando la receta correcta, y por tanto se sentía verificado. Contenía además archivos que el repo nunca tuvo. Ninguna cifra sale del espejo, nunca; se clona el repo.

[NUEVO v2.1] Ninguna cifra esperada se teclea de memoria. Si un paso de verificación necesita un valor de referencia —un conteo, un estado de suite, un número de reglas—, se deriva en la misma sesión o se cita con archivo y línea. Está prohibido copiar una cifra de un documento de traspaso, de una conversación previa o de una sesión anterior para usarla como criterio de comparación. Corolario: un criterio de parada con una constante escrita a mano es el defecto que el criterio existe para atrapar. Si la cifra esperada no se puede derivar, el paso se formula como "reporta el valor" y no como "se espera N".

[REFINADO v2.3] Y la receta de derivación también se verifica. Derivar no basta si la receta está mal: grep -c "^## R" sobre hitoD-preregistro-v2_0.md devuelve 26 y no 25, porque cuenta el encabezado ## Registro de veredictos archivados. Una cifra derivada con una receta no probada es una cifra tecleada con pasos extra. Prueba la receta contra un caso donde conozcas la respuesta, o reporta el valor crudo y el comando que lo produjo, para que quien lea pueda ver el error que tú no viste.

[NUEVO v2.1] Verificación de premisas antes de ejecución. Todo encargo declara al inicio su procedencia: qué se verificó contra el repo, qué viene de un espejo, qué viene de reporte de otra sesión. Quien ejecuta verifica las premisas del encargo antes de ejecutarlo. Si una premisa no se sostiene contra el archivo, se detiene y lo reporta — no la ejecuta, y no ajusta el texto para que cuadre. Encontrar que una instrucción estaba mal fundada es un entregable, no una interrupción. (Esta regla existe porque las anteriores no bastan. La prohibición de traer afirmaciones sin repo ya estaba escrita y aun así se violó varias veces por quien la citaba. Lo que atrapó esos errores no fue la regla sino que alguien con acceso al archivo verificara antes de obedecer. Esa verificación deja de ser suerte y pasa a ser obligación.)

[NUEVO v2.2] Verificación de la restricción antes del diseño. Antes de diseñar un plan alrededor de una restricción —de acceso, de entorno, de herramienta, de permisos—, verifica que la restricción existe y mide su perímetro. Una restricción supuesta se hereda igual que una cifra supuesta, y es peor, porque nadie la audita: una cifra parece una afirmación, una restricción parece el terreno. Dos corolarios operativos: (1) verificar alcanzabilidad no es consultar la fuente — comprobar que un host responde no revela nada sobre lo que el dato dice, así que no contamina ningún pre-registro y va antes que él, no después. (2) "no pude alcanzar la fuente" y "la fuente no tiene el dato" son hallazgos distintos; confundirlos mete un veredicto falso al registro. Se reportan con palabras distintas y no se colapsan nunca.

(Por qué está aquí: el programa operó desde su primer día sin salida de red hacia ningún dominio de datos público mexicano, y nadie lo midió. Esa restricción no verificada le dio forma al diseño completo —síntesis de literatura, cero datos primarios como deuda asumida— y lo que la destrabó no fue rigor analítico sino un curl a nueve hosts. El chequeo cuesta minutos; diseñar sobre una restricción falsa costó meses.)

[REFINADO v2.4] Y hay una tercera variante, que es la que más caro salió. "No pude alcanzar la fuente", "la fuente no tiene el dato" y "nadie corrió el mecanismo contra esta fuente" son tres hallazgos distintos, no dos. El 4/ago un barrido de alcanzabilidad fue 5 de 5 RESPONDE sobre fuentes clasificadas como sin payload; la premisa que las tenía así no era que el recurso no existiera ni que el entorno no llegara, sino que nadie había corrido el mecanismo de resolución contra ellas. Esa confusión mantuvo el perímetro falsable del Hito D estimado en ~10 de 27 cuando puede ser ~21. Se reportan con palabras distintas y no se colapsan nunca.

[NUEVO] Marca la procedencia de la evidencia (las tres clases). Distingue y etiqueta siempre: (a) datos primarios sobre población EN México; (b) estudios con muestras mexicano-americanas / de diáspora en EE.UU. (sujetas a aculturación y selección migratoria — no son evidencia directa sobre México); (c) marcos teóricos importados. Constructos como simpatía, machismo/caballerismo y marianismo suelen ser (b): márcalos. (Esta fue la falla recurrente del corpus: el eslabón débil confundía diáspora con población en México.)

[NUEVO] Firewall genético (reformulado). Queda prohibida la inferencia ascendencia → conducta de grupo (no existe un "genoma mexicano"; la variación de mestizaje es tal que la genética de poblaciones, bien leída, es argumento contra el determinismo). Se admite un canal genético individual, estrecho, molecularmente explícito y de efecto pequeño frente a la estructura (sobre todo metabolismo de alcohol y nicotina), nunca como segmentación por ascendencia. Cuidado con la predisposición metabólica: modifica una consecuencia, no una decisión.

[NUEVO · OPCIONAL] Falsabilidad. Para cada patrón o regla fuerte, di qué evidencia lo cambiaría. Vigila que "adaptación racional" no se vuelva infalsable (siempre se puede inventar un incentivo que haga óptima cualquier conducta): acótala con tamaños de efecto y contraevidencia, igual que se le exige al culturalismo.

Bloque A-bis · Medición propia [NUEVO v2.4]

Por qué existe este bloque. Hasta el 4/ago/2026 el programa sintetizaba literatura y auditaba sus propias afirmaciones. Desde ese día produce estimaciones con microdato. Es otra clase de artefacto y falla distinto: una frase falsa en un documento la lee una persona y la puede discutir; un número falso en milpa/procedencia.yaml lo consume la simulación. Estas cuatro reglas salen de defectos que ocurrieron ese mismo día, y las tres primeras iban a poner un número falso en el ejecutable.

1 · Co-observación no es identificación. El criterio de que un parámetro θ medido y co-observado con un desenlace deja identificado el coeficiente β por regresión vale solo bajo no-confusión, y los criterios de co-observación no dicen nada de confusión. Verificado el 4/ago: los tres coeficientes estimados marginalmente invirtieron el signo al estratificar — en uno de ellos, las cuatro celdas del único eje disponible, todas significativas, todas opuestas al marginal. Un β̂ sin condicionamiento es una asociación. Se rotula como asociación y no como coeficiente identificado, por muy limpia que sea su co-observación.

2 · Condicionado tampoco es correcto. La corrección de la regla 1 no es "el estratificado es el bueno". Condicionar puede acercar o alejar del estimando: un eje colisionador o que induce selección empeora la estimación. Lo que un condicionamiento discordante establece es que el marginal no es robusto — nada más. "El verdadero β es X" no se escribe sin un argumento de identificación que las reglas de co-observación no proveen.

3 · Toda cantidad medida entra con su escala declarada, y no se compara contra otra escala. Una diferencia de proporciones y un coeficiente de índice no son la misma cosa salvo que el modelo declare una función de enlace. Está prohibido escribir "el medido es X, el asignado era Y, difiere en Z%" entre escalas distintas: es un error de categoría, no una medición. Lo comparable sin enlace es el signo y la razón entre coeficientes de un mismo generador estimados en una misma corrida — y ni siquiera eso entre instrumentos distintos, donde la tasa base del desenlace difiere.

4 · Un estimando restringido a una subpoblación no se compara contra uno poblacional. Si el eje de estratificación solo cubre a quienes trabajan, o a quienes reportan ingreso, las celdas estiman sobre esa subpoblación. Reconciliarlas contra un marginal poblacional no valida ni invalida nada: compara dos universos. Se recalcula el marginal restringido al mismo universo, o se declara el resultado como acotado a esa subpoblación. Señal diagnóstica: si la discrepancia se atenúa suavemente con la cobertura del eje, es problema de universo; un bug no se atenúa.

Y la contraparte, que también es regla. Un punto estimado que satisface un umbral con un intervalo de confianza que no lo despeja no adjudica. Se reporta como propuesta con la reserva escrita. El 4/ago un ejecutor se abstuvo por esta razón sin que nadie se lo hubiera pedido; queda escrito para que no dependa del juicio de quien toque.

Bloque B · Estructura del REPORT TEMÁTICO

[REFINADO] Bloque B es la estructura de los reports temáticos. Los demás artefactos del proyecto usan estructura propia adecuada a su función, conservando siempre las reglas del Bloque A: el integrador (constructos compartidos, contradicciones entre reports, mapa de evidencia consolidado), el modelo de decisión (perfiles, generadores, reglas SI-ENTONCES, protocolo, límites) y las validaciones forenses (Bloque C). No fuerces las 10 secciones sobre estos.

Estructura obligatoria (para reports temáticos):

Resumen ejecutivo: 10–15 hallazgos, marcando los más sólidos, los más malinterpretados y los de mayor utilidad práctica.
Marco conceptual.
Mapa de evidencia: clasifica cada hallazgo en evidencia fuerte / media / hipótesis razonable / narrativa popular.
Patrones principales. Cada patrón con: descripción, evidencia a favor, evidencia en contra, segmentos donde es más fuerte/débil, causas plausibles, riesgo de mala interpretación e implicaciones prácticas.
Causas: distingue cultura vs. estructura vs. adaptación racional; evalúa desigualdad, informalidad, violencia, historia institucional, educación, economía familiar, urbanización, acceso digital, ciclo generacional y exposición internacional.
Segmentación explícita por los ejes de arriba.
Comparación internacional útil: qué es distintivamente mexicano, qué es latinoamericano general, qué es propio de sociedades desiguales/de baja confianza, y qué se malinterpreta desde marcos anglosajones.
Implicaciones aplicadas (negocio, liderazgo, RH, marketing, producto, salud, educación, política pública, según corresponda).
Mitos y sobreinterpretaciones: clichés, hallazgos débiles, marcos sobreusados, conclusiones bonitas pero poco útiles.
Síntesis final: top patrones, top contradicciones, top errores a evitar y top oportunidades.
[NUEVO · CONDICIONAL] Reglas de decisión. Si el report alimenta el modelo de decisión, cierra con reglas SI-ENTONCES por las decisiones clave del dominio: SI [segmento/contexto] ENTONCES [conducta esperada] — PORQUE [driver] — [TIER], incluyendo los disparadores de contexto que voltean la conducta (formal/informal, quién observa, sanción creíble, puente personal, cobertura formal, urgencia).

Bloque B-bis · Pre-registro de falsación [NUEVO v2.4]

Toda escala de falsación declara qué pasa si el falsador NO refuta. Una escala cuyas filas son "refutada" / "ambigua" / "exigiría otro diseño" / "inejecutable" no tiene dónde anotar una regla que sobrevivió a su prueba. El 4/ago una corrida encontró que el falsador no se satisfacía de forma decisiva —el resultado quedaba a casi el triple del umbral— y ninguna fila de la escala nombraba ese desenlace; el ejecutor se negó, con razón, a forzar una. Un registro que solo puede anotar refutaciones e inejecutables describe mal el estado de validación del modelo, y lo describe sesgado hacia abajo.

La ficha declara, antes de correr, qué significa que el falsador no refute: si la regla queda corroborada, si queda acotada, o si el falsador era demasiado débil para decir nada. Si el resultado esperado bajo corroboración es interesante —y suele serlo más que la refutación— se dice también, antes de ver el dato. Precedente: una ficha del 4/ago declaró que su falsador podía confirmar el driver bajo prueba y que ese sería "el primer dato mexicano que sostenga una atribución hoy importada". Esa declaración anticipada es lo que impide que un ejecutor lea la corroboración como fracaso.

Y la regla de precedencia. Si dos filas de una escala pueden satisfacerse a la vez, se declara cuál manda, al sellar y no después. La escala de la ficha gobierna sobre cualquier legend genérico, y hay que decirlo en la ficha.

Módulo de auditoría de rigor extremo

[REFINADO v2.3] Dónde va, y dónde ya no. Este módulo es obligatorio solo en artefactos que afirman algo sobre México — reports temáticos, integrador, modelo de decisión, validaciones forenses. No va en notas de sesión, registros de medición, encargos, manifiestos, ni forenses de proceso. Ahí no atrapa nada: no hay afirmación sobre México que auditar, y su costo es una sesión que no midió.

(Era obligatorio "en TODO artefacto". Esa palabra es la que produjo la jornada del 30/jul: siete preguntas de auditoría sobre un documento que solo registra qué archivo se descargó.)

¿Qué parte del análisis podría estar confundiendo pobreza, desigualdad, violencia o informalidad con "cultura"?
¿Qué parte podría estar sobregeneralizando desde clases medias urbanas?
¿Qué parte está sesgada por literatura escrita desde marcos estadounidenses o europeos? [NUEVO] (incluye aquí las muestras mexicano-americanas, no solo los marcos).
¿Qué hallazgos cambiarían si el foco fuera México rural, indígena o popular?
¿Qué parece psicológico pero en realidad es un incentivo racional ante un entorno específico?
¿Dónde hay evidencia débil pero intuición social fuerte?
¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?
[NUEVO v2.1] ¿Qué afirmación de este artefacto describe el estado del corpus —un conteo, una cobertura, una versión, la existencia de un archivo— y no fue derivada, sino escrita a mano?
[NUEVO v2.2] Las deudas asumidas caducan cuando cambia el objetivo. "Cero datos primarios propios" fue coherente mientras la función del programa era describir. Dejó de serlo cuando pasó a validar, y siguió operando por inercia porque estaba registrada como decisión y no como pendiente. Toda deuda declarada "asumida a propósito" se re-examina cuando cambia la función del programa — no solo cuando alguien la cuestiona.
[NUEVO v2.3] ¿Cuántos contadores movió el trabajo que produjo este artefacto? Si la respuesta es cero, dilo en una línea al inicio del módulo, sin justificarlo. Hay artefactos que legítimamente no mueven contadores. Lo que no es legítimo es que nadie se dé cuenta.
[NUEVO v2.4] Si este artefacto contiene una cantidad estimada: ¿en qué escala está, y contra qué se está comparando? Una cantidad que entra al canon sin escala declarada es un número que la simulación va a consumir en la escala equivocada.

Bloque C · Validación forense [NUEVO · CONDICIONAL]

Para cualquier investigación que pruebe supuestos contra desenlaces reales (¿la apuesta conductual de tal organización funcionó?). No sustituye a Bloque A/B; los complementa. Los tres blindajes son obligatorios, porque sin ellos el análisis de casos recae en la narrativa post-hoc que el proyecto existe para evitar:

Anti-confusión. Separa la variable psicológica de las estructurales (capital, logística, precio, regulación, timing, ejecución, suerte). Cuenta como evidencia "psicológica" solo si fue plausiblemente decisiva; si no se puede aislar, márcala CONFUNDIDO.

Anti-post-hoc. Clasifica el supuesto: DECLARADO (la organización lo dijo antes del resultado — el oro, falsable) / INFERIDO / RETROSPECTIVO (solo aparece después — el más débil, se registra pero no prueba).

Anti-superviviente. Busca activamente lo invisibilizado: éxitos silenciosos, fracasos por razones aburridas/estructurales, y sobre todo pares contrafactuales (misma jugada, distinto segmento/resultado, con la estructura constante y la variable conductual visible).

Además: marca cada métrica como AUDITADA o AUTO-REPORTADA por parte interesada. El entregable central es qué reglas del modelo el caso CONFIRMA / MATIZA / ROMPE. Descartar con rigor es entregable, no fracaso.

Bloque D · Plantilla de encargo [NUEVO v2.4]

Qué es y qué no es. Esto no es una regla de rigor y no se paga con el impuesto de v2.3: no añade una compuerta de auditoría, no exige verificar nada nuevo, no se cataloga y no produce entradas de cola. Es plantilla: estandariza los primeros sesenta segundos de un acto para que el ejecutor no los gaste orientándose ni los gaste mal.

Por qué se añade, medido y no supuesto. Barrido de forense/hallazgos.md el 4/ago/2026: 17 menciones de clon/worktree · 16 de data/raw · 3 de payloads que quedaron fuera del corpus compartido. Cuatro defectos concretos que ya ocurrieron:

Una sesión arrancó en el home y gastó su inicio buscando el repo con find en un directorio vacío. Se mató sin producir nada.
Un encargo declaró data/raw ausente como PARO y detuvo una sesión que sí tenía la capacidad escasa — en un acto cuya función era poblarla.
PR #77 registró seis archivos que se quedaron en un data/raw local. Nadie lo notó hasta dos actos después. Éste es el que costó de verdad: el manifiesto afirmaba tener payloads que el corpus compartido no tenía.
Dos encargos corrieron en dos entornos a la vez y produjeron el mismo archivo dos veces, tirando una jornada de capacidad.

Regla. Todo encargo abre con el bloque de abajo, textual y sin resumir. Un encargo sin él está mal escrito y quien lo reciba puede pedirlo antes de ejecutar.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo
no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el
encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no
    haya ninguno, y si clonas, dilo.
    Reporta:  ruta absoluta  ·  git log -1 --format="%h %s"  ·  git status
    ⚠️ No arranques desde el home. Si el cliente avisa "launched in your
    home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el
    encargo declara. Si main se movió: NO es PARO — refresca, re-deriva
    lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta
    por código; un clon fresco siempre nace sin ella. Se crea o se enlaza.
    Reporta:  existe / la enlacé a <ruta> / la creé.
    ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads
    quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el
    defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí.
    CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE  →  esperado: sin_variable
    curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
    Reporta los dos valores crudos. NUNCA curl -I.
    Si este acto no toca microdato ni red, dilo y salta este punto.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está
    versiones atrás del repo y contiene archivos que el repo nunca tuvo.
    Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

Dos líneas más que el encargo debe traer, fuera del bloque.

ENTORNO ASIGNADO — y el que NO. Nombrar a cuál va y decir explícitamente que no se lance en el otro. Las dos veces que esa línea faltó, el encargo salió duplicado.

PERÍMETRO Y CONCURRENCIA. Qué archivos toca, qué actos están corriendo en paralelo y cuáles son sus archivos. Con la frase: "si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

Y para los actos que producen una estimación, dos commits mínimo. El primero congela la especificación —variables, universo, ponderadores, ejes, dicotomizaciones— antes de abrir ningún dato, y cierra con la frase "el primer resultado que produzca este procedimiento es el que se reporta". El segundo trae los resultados y no edita el primero. Si la especificación estaba mal, un tercer commit lo dice; nunca se corrige hacia atrás. El sello lo da el orden del diff, no la promesa, y mesa lo audita.

Lo que el Bloque D deliberadamente NO hace.
No convierte nada en PARO salvo que el terreno contradiga al encargo. data/raw ausente, un main que se movió y un worktree residual son condiciones normales, no paros.
No añade un test. Nada de esto es verificable desde la suite: el clon, el entorno y el corpus compartido viven fuera del repositorio. Instrumentarlo sería vigilar lo que el test no puede ver.
No se audita a sí mismo. No hay pregunta nueva en el módulo de auditoría por esta plantilla. Si el bloque falta, se pide y ya.

Nota de alcance

Estas reglas gobiernan todo el programa: reports temáticos (Bloque B), el integrador y el modelo de decisión (estructura propia + Bloque A + auditoría), las validaciones forenses (Bloque C), las mediciones propias (Bloque A-bis) y los pre-registros de falsación (Bloque B-bis). La v2 no cambia el espíritu de la v1 —anti-esencialismo, estructura sobre cultura, evidencia tierizada— solo lo hace explícito donde el proyecto tropezó: procedencia de la evidencia, el firewall genético, la crítica calibrada de marcos, y el hecho de que un modelo de decisión no es un report temático.

[NUEVO v2.1] Las tres reglas de procedencia documental (lectura, cifras, premisas) atienden un tropiezo distinto de los anteriores. Los defectos que el programa encontró auditándose no estaban en la evidencia sobre México: estaban en las afirmaciones del corpus sobre sí mismo —conteos, coberturas, versiones, referencias cruzadas—, escritas a mano y nunca verificadas. La capa de evidencia resistió la auditoría; la capa de contabilidad sobre esa evidencia, no. Esa clase de defecto no se corrige con más cuidado: se corrige derivando en vez de escribiendo, y verificando antes de obedecer.

[NUEVO v2.3] Y atiende un tropiezo que las anteriores no podían ver, porque lo causaron. Cada regla de v2.1 y v2.2 fue una respuesta correcta a un error real. Juntas produjeron un programa que dedicó su jornada más productiva —15 PR fusionados— a auditarse, sin mover un solo contador. El rigor no falló por estar mal diseñado; falló por no tener un criterio de suficiencia. La v2.3 es ese criterio y es una sola frase: cada sesión produce una medición, o produce nada.

Si esta versión hace que el proyecto pase por alto un defecto de contabilidad, funcionó. Ese es el intercambio, y está tomado a propósito.

[NUEVO v2.4] Y la v2.4 atiende el tropiezo que la v2.3 hizo posible al exigir medir. Los defectos de la capa de contabilidad se corregían derivando en vez de escribiendo. Los de la capa de medición no: un β̂ derivado correctamente, con la receta probada y el comando a la vista, puede seguir siendo una asociación confundida escrita en una casilla que espera un coeficiente identificado. Ninguna regla de procedencia lo atrapa, porque la procedencia está impecable. Lo que lo atrapa es preguntar qué se estimó, en qué escala, sobre qué universo, y qué habría que suponer para que signifique lo que la casilla dice.

El costo de esta versión, contado. Cuatro reglas nuevas en A-bis, tres en B-bis, y una plantilla que no es regla. Las siete reglas salen de defectos del 4/ago/2026 y las cuatro de A-bis iban a poner un número falso en el ejecutable — que es peor que una frase falsa en un documento, porque nadie lo lee antes de que la simulación lo consuma. Si en tres meses ninguna de las siete ha atrapado nada, se retiran. La regla de señal manda sobre todas ellas: cada sesión produce una medición, o produce nada.

Bloque D-bis · Delta v2.5 [NUEVO v2.5]

Por qué v2.5. Tres defectos medidos el 4 y 5/ago/2026, ninguno sobre México: un verificador de payloads que solo revisa el último --id de varios sin avisarlo, una firma de entorno de dos partes que no distingue si el corpus compartido está montado, y encargos que solo existieron en la salida de una conversación — invisibles para el programa hasta que alguien los rescató a mano. Las tres reglas de abajo salen de esos defectos, ya medidos, no supuestos. No retira nada de v2.4.

A.1 · Verificación de payloads, uno por --id [NUEVO v2.5]. tests/manifiesto.py --verifica con varios --id en la misma invocación solo verifica el último, sin aviso — defecto medido el 4/ago/2026; ningún test lo atrapa. Toda verificación de hash se corre una invocación por --id, y el reporte pega la salida cruda de cada una. Las tres respuestas no se colapsan nunca: AUSENTE (el archivo no está) · raíz-no-configurada (el corpus no está montado) · hash-discordante (está y no coincide). Son tres hallazgos distintos con tres remedios distintos — mismo criterio que la regla v2.2 sobre "no pude alcanzar la fuente" vs. "la fuente no tiene el dato".

A.2 · La firma de entorno tiene TRES partes, no dos [NUEVO v2.5]. La firma que el punto 4 del arranque (Bloque D, arriba) declara — CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE más la sonda de red — no alcanza: describe la red, no el dato. Tercera parte, derivable en un comando: ls data/raw/ 2>/dev/null | head -1 — ¿está montado el corpus compartido? Todo acto que abra microdato va a Ubuntu, sin excepción — no porque la nube "no deba", sino porque no tiene los bytes. Medido el 5/ago/2026: dos actos (E-ENCIG y S-IDG3) murieron en la nube con cloud_default correcto, sonda coherente, y cero corpus montado. Los dos pararon bien; la asignación de entorno estaba mal, y era de mesa, no del ejecutor.

A.3 · Los encargos vivos viven en el repo [NUEVO v2.5]. Un encargo que solo existe en la salida de una conversación es invisible para el programa. Medido: de una batería de seis encargos rescatados el 5/ago/2026, cinco ya se habían ejecutado por otras vías sin que nadie lo supiera, y el sexto había muerto una vez. Todo encargo que se lance se commitea a forense/encargos/ antes o junto con su lanzamiento, con su SHA de redacción en la cabecera. Cuando su acto cierra, se marca CONSUMIDO con el PR que lo ejecutó — no se borra: un encargo consumido es el registro de qué se pidió exactamente, y es lo que permite auditar si el ejecutor hizo lo que se le dijo. Corolario, y es el que duele: un encargo que cita un archivo inexistente es un encargo mal escrito. Ocurrió tres veces. Si el texto que un encargo necesita no está en el repo, va pegado inline o el encargo no se lanza.

El costo de esta versión, contado. Tres reglas, las tres de defectos ya medidos y no de riesgo concebido. Ninguna añade compuerta de auditoría ni entra al módulo de rigor extremo — misma exención que Bloque D. Si en tres meses ninguna ha atrapado nada, se retiran, mismo criterio que v2.4.

Bloque D-ter · Delta v2.6 [NUEVO v2.6]

Por qué v2.6. La v2.5 salió de tres defectos de infraestructura. Ésta sale de uno solo, de otra clase, y es el más caro que el programa ha cometido: cuatro veces clasificó "no existe fuente" sobre datos que sí existían. No fue descuido. Los tres exámenes que produjeron los cierres más citados fueron correctos y las tres conclusiones excedieron su alcance: ADR-54 cerró sobre cinco instrumentos, PR #58 sobre una batería, el cruce de catálogo sobre grep data/. Ninguna regla lo atrapó; lo atrapó el usuario, bajando a mano lo que un agente había declarado inexistente. No retira nada de v2.4 ni de v2.5.

A.4 · Ninguna clasificación de "no existe" se sella sin declarar el universo de búsqueda [NUEVO v2.6]. Un cierre sin universo declarado es una afirmación sobre el buscador, no sobre el mundo. Toda clasificación negativa declara, en la misma línea donde se escribe: qué se examinó (los instrumentos, el corpus, el directorio, los términos), con qué mecanismo, y en qué fecha. Si el universo no cabe en una línea, la clasificación no está lista para sellarse.

Vocabulario obligatorio, cuatro palabras, ya en uso en forense/notas/2026-08-05-barrido-publico-17-condiciones-no-existe.md y aquí canonizado:

EXISTE-SATISFACE — el dato cubre la condición tal como está escrita.
EXISTE-NO-SATISFACE — existe, le falta algo específico, y se dice qué.
NO-ENCONTRADO — se buscó y no apareció. No es "no existe". Se dice dónde y con qué términos.
NO-ACCESIBLE — pago, afiliación institucional o restricción legal. Registro gratuito o aceptar términos de uso no cuenta aquí.

Las palabras "no existe", "inexistente" y "no hay fuente" quedan prohibidas como clasificación. Se admiten solo dentro de una cita textual de un documento anterior que se está corrigiendo.

A.5 · El fallo de un agente es un hecho sobre el agente, no sobre la fuente [NUEVO v2.6]. Ya está escrito en los encargos VER-1 y VER-2; sube al canon porque es lo único que impidió que el defecto se repitiera. Un curl que falla establece que ese curl falló, con esas cabeceras, desde ese entorno, en ese momento. Única formulación permitida: "NO OBTENIDO POR ESTE AGENTE EN N INTENTOS", con los N intentos y su salida cruda. Y por cada uno, una receta manual que el usuario pueda ejecutar en un navegador en menos de un minuto. La receta no es el consuelo del acto: es su entregable de mayor rendimiento, medido — el usuario ya ha bajado a mano, con tres clics, lo que agentes anteriores declararon inexistente. Prohibido derivar cualquier conclusión sobre un portal del conocimiento previo del modelo. El corte de entrenamiento es anterior a hoy. Si no se sondeó en esta sesión, no se sabe.

A.6 · Encontrado por búsqueda no es verificado [NUEVO v2.6]. Una candidata localizada por buscador y no abierta byte a byte es evidencia de segunda mano. Se registra como candidata, nunca se promueve a ficha ni se abre como fuente, y lleva la marca SIN-FETCH hasta que un acto con red la abra. Medido: el barrido de las 17 condiciones reportó WebFetch 403 en el 100% de los intentos, verificado contra dominio de control neutral — las 17 candidatas que hoy parecen resueltas son, todas, de segunda mano.

Corolario retroactivo. Lo que se reabre es la razón, no la etiqueta.

Reabrir solo lo rotulado "no existe" sería cometer el defecto otra vez, un nivel más arriba: la etiqueta es del buscador, igual que el cierre. Se reabre todo cierre cuya razón sea informacional, en sus tres redacciones:

1. la clasificación negativa explícita ("no existe", "ninguna encontrada", "no hay fuente");
2. la evidencia calificada como débil por falta de información — un tier bajo asignado porque no se halló el dato, no porque el dato hallado fuera malo;
3. lo que quedó sin corroborar por esa misma falta — la reserva declarada que nadie volvió a tocar.

Los tres son el mismo defecto y los tres se sellaron sin universo. Un tier medio puesto porque el buscador no encontró es tan revisable como un NO-ENCONTRADO, y es más peligroso porque no lleva la palabra que dispara la sospecha.

Lo acotado es el disparador, no el tipo. No se auditan los cierres del corpus en bloque: eso es la jornada del 30/jul otra vez. Se reabre lo que hoy gatea una ficha del Hito D. Si un cierre sin universo declarado no bloquea ninguna regla, se anota en forense/hallazgos.md y se queda como está.

A.7 · La identidad de un artefacto es su contenido, no su envoltura [NUEVO v2.6]. Medido el 5/ago/2026: dos generaciones de la misma canasta de Descarga Masiva de INEGI — 1,010,608 bytes ambas, totalMb="51.00 GB" ambas, 7,930 URLs únicas idénticas — dan sha256 distintos, porque el atributo aut es un token de solicitud que cambia en cada generación (cf4f56bb-… contra 612e96b9-…). ENCARGO-VER2 declara PARO ante hash discordante; con la segunda generación para en falso sobre el archivo correcto.

Todo payload cuyo formato incluya un token de sesión, marca de tiempo de generación o identificador de solicitud se registra con dos hashes: el crudo, para reproducibilidad byte a byte, y un hash de contenido con esos campos neutralizados. El criterio de PARO se evalúa contra el segundo. Para este XML, derivados en esta sesión: crudo 7089264d… · sin aut 4687abd6… · del set de URLs ordenado 9a98e161….

Corolario: un hash discordante no es un hallazgo sobre el archivo hasta que se sabe qué campo cambió. Es la misma regla A.5 aplicada a un artefacto en vez de a un portal.

El costo de esta versión, contado. Tres reglas. Ninguna añade un test —nada de esto es verificable desde la suite— y ninguna añade una pregunta al módulo de auditoría. Las tres salen del mismo defecto medido cuatro veces, y ese defecto sí le costó a un lector: mantuvo el perímetro falsable del Hito D estimado por debajo de lo real, y el perímetro es un número que el modelo consume. Si en tres meses ninguna ha atrapado nada, se retiran. La regla de señal manda sobre las tres: cada sesión produce una medición, o produce nada.
