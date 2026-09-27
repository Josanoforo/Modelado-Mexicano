# Instrucciones del proyecto — "Psicología del Mexicano Contemporáneo" · v2.3

> **Por qué v2.** La v1 (Bloque A + Bloque B) se diseñó para escribir **un report temático**. El proyecto creció a un **programa multi-artefacto**: reports temáticos + un integrador (meta-síntesis) + un modelo de decisión + validaciones forenses. Esta v2 **conserva casi toda la v1 verbatim** y solo añade o precisa lo que el proyecto probó que necesita. Cada cambio está marcado `[NUEVO]`, `[REFINADO]` u `[OPCIONAL]` para que sea fácil aprobarlo o cortarlo. Todo lo no marcado es v1 sin cambios.

> **Por qué v2.1.** Añade tres reglas de procedencia documental y una pregunta de auditoría, marcadas `[NUEVO v2.1]`. Atienden una clase de defecto distinta de todas las anteriores: no errores sobre México, sino **afirmaciones del corpus sobre sí mismo** —conteos, coberturas, versiones, referencias cruzadas— escritas a mano y nunca verificadas. Todo lo demás es v2 sin cambios.

> **Por qué v2.2.** Añade cuatro reglas y una pregunta de auditoría, marcadas `[NUEVO v2.2]`. Tres salen de la primera medición contra datos primarios del programa (Hito D · R3.2): una restricción de entorno que le dio forma al diseño sin que nadie la midiera, un umbral pre-registrado aritméticamente inalcanzable, y un rótulo estadístico correcto en intención que describía otro cálculo. La cuarta caduca una deuda que dejó de ser coherente cuando el programa pasó de describir a validar. Todo lo demás es v2.1 sin cambios.

> **Por qué v2.3.** Las versiones anteriores añadieron rigor y ninguna le puso precio. El resultado, medido el 30/jul/2026: una jornada de 15 PR, 40 entradas de cola, 3 ADR y 54 payloads registrados, con cero mediciones — 2 de 27 y 0 de 15 exactamente donde amanecieron. Ningún defecto catalogado ese día habría dañado a un lector: todos eran de contabilidad del programa sobre sí mismo. La v2.3 no retira ninguna regla de rigor. Añade la regla que dice cuándo el rigor está sustituyendo al trabajo, y acota el módulo de auditoría a los artefactos donde tiene función. Marcado `[NUEVO v2.3]` y `[REFINADO v2.3]`.

---

## Bloque A · Reglas transversales de rigor (aplican a TODO artefacto)

- No trates a los mexicanos como un bloque homogéneo.
- Segmenta siempre por región, clase, edad, género, escolaridad, urbanización, religiosidad, migración y exposición global.
- Distingue en todo momento entre psicología individual, scripts culturales, adaptación racional al entorno, estructura económica e instituciones.
- Separa explícitamente evidencia fuerte, evidencia media, hipótesis razonable y narrativa popular.
- No romantices ni patologices a México.
- No confundas desigualdad, violencia, informalidad o precariedad con cultura.
- No extrapoles desde la clase media urbana digitalizada a todo México.
  - `[REFINADO]` El sesgo que más muerde es **de clase *dentro* de la modernidad**: el corpus sobre-muestrea al clasemediero urbano formal y sub-muestrea al popular informal (el peso demográfico dominante). Además, el **sistema indígena-comunal vivo** (asamblea, cargos, tequio, usos y costumbres) no es un "México sub-muestreado" sino **otro orden institucional**: queda fuera por diseño, no como hueco a rellenar. La huella indígena *difusa* (sincretismo, folk-psicología, mestizaje) sí vive dentro de la modernidad mestiza y ahí se mapea.
- No importes marcos extranjeros (Hofstede, GLOBE, WVS, honor/dignidad/face) sin crítica.
  - `[REFINADO]` **"Con crítica" no significa rechazar: significa ni importar ingenuamente ni rechazar por reflejo.** La crítica de McSweeney a Hofstede es de validez de constructo, no prueba que las dimensiones no existan; IVR/UAI no "colapsan"; honor y dignidad **no se oponen** (r=.96 dignidad-face; los mexicanos se autoperciben como cultura de dignidad, no de honor). El anti-esencialismo también puede sobre-corregir.
- No conviertas intuiciones en hechos.
- Si no hay evidencia suficiente para una sección, dilo y no la rellenes.
- Escribe el reporte final en español.

`[NUEVO v2.3]` **Regla de señal — la que manda sobre las de abajo cuando chocan.**

**Cada sesión produce una medición, o produce nada.** Defecto que no impide medir → **una línea** en `forense/hallazgos.md` y sigue. No se cataloga. Defecto que sí impide medir → se para y se reporta.

**Un contador que no se mueve es el único síntoma que no admite interpretación.** Si al cierre de una sesión `2 de 27` sigue en `2 de 27`, esa sesión no avanzó, sin importar cuántos PR fusionó ni qué tan correcto era todo lo que escribió.

**El aparato tiene costo y el costo se cuenta.** Toda regla, test, ADR, convención de nombres o módulo obligatorio se paga en sesiones que no midieron. Antes de añadir cualquiera, se declara qué defecto real atrapó —uno que **ya ocurrió**, no uno concebible— y qué le habría costado a un lector. Si no le habría costado nada a un lector, es contabilidad interna: se anota y no se instrumenta.

**Corolario, y es el que duele.** Las reglas de procedencia de v2.1 y v2.2 se conservan íntegras: atraparon errores reales y baratos. Lo que se retira es su **generalización** — la idea de que si verificar es bueno, verificarlo todo siempre es mejor. Verificar tiene un precio, se paga en lo único escaso, y la auditoría de la auditoría no lo vale nunca.

*(Por qué está aquí: el 30/jul el aparato de auditoría se volvió el trabajo. No por descuido — cada paso individual estaba justificado por una regla escrita. Ese es exactamente el modo de falla: un sistema de rigor sin criterio de suficiencia no se detiene solo, porque siempre queda algo por verificar y siempre es defendible verificarlo. La señal no puede ser "¿está bien hecho?"; tiene que ser un número que se mueve o no se mueve.)*

`[NUEVO]` **Regla de oro (procedencia por lectura).** No reconstruyas tiers ni hallazgos de memoria: léelos de los reports, de sus mapas de evidencia y del glosario. Toda síntesis se construye **leyendo, no recordando**. Si un tier no está a la vista, ve a buscarlo antes de afirmarlo.

`[NUEVO v2.1]` **Procedencia de la lectura (extensión de la Regla de oro).** Leer no basta si no sabes **de dónde**. Toda afirmación sobre el contenido de un archivo se marca con su fuente: **(1)** leída del repo en esta sesión, con commit citable; **(2)** leída de un espejo del proyecto, que puede estar atrás del repo; **(3)** reportada por otra sesión o conversación, no verificada. **Solo (1) entra al canon.** Las de tipo (2) y (3) se formulan como pregunta a verificar, nunca como instrucción ni como hecho. Un espejo **sin sello de commit no es fuente**: no se puede distinguir un archivo vigente de uno que el repo ya borró. Si el espejo no declara de qué commit salió, se lee como (3), no como (2). *(Por qué está aquí: la Regla de oro dice "léelo, no lo recuerdes" y no basta. Un archivo leído del espejo se siente exactamente igual que uno leído del repo, y un artefacto borrado por ADR sigue ahí, legible y falso.)*

`[NUEVO]` **Marca la procedencia de la evidencia (las tres clases).** Distingue y etiqueta siempre: **(a)** datos primarios sobre población **EN México**; **(b)** estudios con muestras **mexicano-americanas / de diáspora** en EE.UU. (sujetas a aculturación y selección migratoria — **no** son evidencia directa sobre México); **(c)** marcos teóricos **importados**. Constructos como simpatía, machismo/caballerismo y marianismo suelen ser (b): márcalos. *(Esta fue la falla recurrente del corpus: el eslabón débil confundía diáspora con población en México.)*

`[NUEVO]` **Firewall genético (reformulado).** Queda **prohibida la inferencia ascendencia → conducta de grupo** (no existe un "genoma mexicano"; la variación de mestizaje es tal que la genética de poblaciones, bien leída, es argumento **contra** el determinismo). Se **admite** un canal genético **individual**, estrecho, molecularmente explícito y de efecto **pequeño frente a la estructura** (sobre todo metabolismo de alcohol y nicotina), **nunca** como segmentación por ascendencia. Cuidado con la predisposición metabólica: modifica una *consecuencia*, no una *decisión*.

`[NUEVO · OPCIONAL]` **Falsabilidad.** Para cada patrón o regla fuerte, di **qué evidencia lo cambiaría**. Vigila que "adaptación racional" no se vuelva infalsable (siempre se puede inventar un incentivo que haga óptima cualquier conducta): acótala con tamaños de efecto y contraevidencia, igual que se le exige al culturalismo.

`[NUEVO v2.1]` **Ninguna cifra esperada se teclea de memoria.** Si un paso de verificación necesita un valor de referencia —un conteo, un estado de suite, un número de reglas—, se **deriva en la misma sesión** o se **cita con archivo y línea**. Está prohibido copiar una cifra de un documento de traspaso, de una conversación previa o de una sesión anterior para usarla como criterio de comparación. Corolario: **un criterio de parada con una constante escrita a mano es el defecto que el criterio existe para atrapar.** Si la cifra esperada no se puede derivar, el paso se formula como "reporta el valor" y no como "se espera N".

`[REFINADO v2.3]` **Y la receta de derivación también se verifica.** Derivar no basta si la receta está mal: `grep -c "^## R"` sobre `hitoD-preregistro-v2_0.md` devuelve 26 y no 25, porque cuenta el encabezado `## Registro de veredictos archivados`. Una cifra derivada con una receta no probada es una cifra tecleada con pasos extra. **Prueba la receta contra un caso donde conozcas la respuesta**, o reporta el valor crudo y el comando que lo produjo, para que quien lea pueda ver el error que tú no viste.

`[NUEVO v2.1]` **Verificación de premisas antes de ejecución** (ADR-39, `gobernanza:290`). Todo encargo declara al inicio su procedencia: qué se verificó contra el repo, qué viene de un espejo, qué viene de reporte de otra sesión. **Quien ejecuta verifica las premisas del encargo antes de ejecutarlo.** Si una premisa no se sostiene contra el archivo, se detiene y lo reporta — no la ejecuta, y no ajusta el texto para que cuadre. **Encontrar que una instrucción estaba mal fundada es un entregable, no una interrupción.**

`[NUEVO v2.2]` **Verificación de la restricción antes del diseño.** Antes de diseñar un plan alrededor de una restricción —de acceso, de entorno, de herramienta, de permisos—, **verifica que la restricción existe y mide su perímetro**. Una restricción supuesta se hereda igual que una cifra supuesta, y es peor, porque nadie la audita: una cifra parece una afirmación, una restricción parece el terreno. Dos corolarios operativos: **(1)** verificar alcanzabilidad **no es** consultar la fuente — comprobar que un host responde no revela nada sobre lo que el dato dice, así que no contamina ningún pre-registro y va **antes** que él, no después. **(2)** "no pude alcanzar la fuente" y "la fuente no tiene el dato" son **hallazgos distintos**; confundirlos mete un veredicto falso al registro. Se reportan con palabras distintas y no se colapsan nunca. *(Por qué está aquí: el programa operó desde su primer día sin salida de red hacia ningún dominio de datos público mexicano, y nadie lo midió. Esa restricción no verificada le dio forma al diseño completo —síntesis de literatura, cero datos primarios como deuda asumida— y lo que la destrabó no fue rigor analítico sino un `curl` a nueve hosts.)*

`[NUEVO v2.2]` **Las deudas asumidas caducan cuando cambia el objetivo.** "Cero datos primarios propios" fue coherente mientras la función del programa era **describir**. Dejó de serlo cuando pasó a **validar**, y siguió operando por inercia porque estaba registrada como **decisión** y no como **pendiente**. Toda deuda declarada "asumida a propósito" **se re-examina cuando cambia la función del programa**, no solo cuando alguien la cuestiona.

`[NUEVO v2.2]` **Todo umbral en puntos porcentuales se verifica contra tasas base plausibles antes de pre-registrarse.** Si el desenlace es raro, un umbral absoluto es inalcanzable por construcción y el criterio va en **razón o riesgo relativo**. Es la misma familia que "verifica la restricción antes de diseñar", aplicada a un criterio numérico: un umbral asignado no solo necesita fuente, necesita ser **posible**.

`[NUEVO v2.2]` **Una cantidad rotulada "pareada", "controlada" o "ajustada" trae su método explícito, o el rótulo no se usa.** Un rótulo correcto en intención puede describir un cálculo que no lo es, y se lee como identificación lograda.

---

## Bloque B · Estructura del REPORT TEMÁTICO

`[REFINADO]` **Bloque B es la estructura de los reports *temáticos*.** Los demás artefactos del proyecto usan **estructura propia adecuada a su función**, conservando siempre las reglas del Bloque A y el módulo de auditoría final: el **integrador** (constructos compartidos, contradicciones entre reports, mapa de evidencia consolidado), el **modelo de decisión** (perfiles, generadores, reglas SI-ENTONCES, protocolo, límites) y las **validaciones forenses** (Bloque C). **No fuerces las 10 secciones sobre estos.**

Estructura obligatoria (para reports temáticos):
1. Resumen ejecutivo: 10–15 hallazgos, marcando los más sólidos, los más malinterpretados y los de mayor utilidad práctica.
2. Marco conceptual.
3. Mapa de evidencia: clasifica cada hallazgo en evidencia fuerte / media / hipótesis razonable / narrativa popular.
4. Patrones principales. Cada patrón con: descripción, evidencia a favor, evidencia en contra, segmentos donde es más fuerte/débil, causas plausibles, riesgo de mala interpretación e implicaciones prácticas.
5. Causas: distingue cultura vs. estructura vs. adaptación racional; evalúa desigualdad, informalidad, violencia, historia institucional, educación, economía familiar, urbanización, acceso digital, ciclo generacional y exposición internacional.
6. Segmentación explícita por los ejes de arriba.
7. Comparación internacional útil: qué es distintivamente mexicano, qué es latinoamericano general, qué es propio de sociedades desiguales/de baja confianza, y qué se malinterpreta desde marcos anglosajones.
8. Implicaciones aplicadas (negocio, liderazgo, RH, marketing, producto, salud, educación, política pública, según corresponda).
9. Mitos y sobreinterpretaciones: clichés, hallazgos débiles, marcos sobreusados, conclusiones bonitas pero poco útiles.
10. Síntesis final: top patrones, top contradicciones, top errores a evitar y top oportunidades.

`[NUEVO · CONDICIONAL]` **11. Reglas de decisión.** Si el report alimenta el modelo de decisión, cierra con reglas **SI-ENTONCES** por las decisiones clave del dominio: *SI [segmento/contexto] ENTONCES [conducta esperada] — PORQUE [driver] — [TIER]*, incluyendo los **disparadores de contexto** que voltean la conducta (formal/informal, quién observa, sanción creíble, puente personal, cobertura formal, urgencia).

**Módulo de auditoría de rigor extremo (obligatorio en TODO artefacto, al final):**

`[REFINADO v2.3]` **Dónde va, y dónde ya no.** Este módulo es obligatorio **solo en artefactos que afirman algo sobre México** — reports temáticos, integrador, modelo de decisión, validaciones forenses. **No va** en notas de sesión, registros de medición, encargos, manifiestos, ni forenses de proceso. Ahí no atrapa nada: no hay afirmación sobre México que auditar, y su costo es una sesión que no midió.

*(Era obligatorio "en TODO artefacto". Esa palabra es la que produjo la jornada del 30/jul: siete preguntas de auditoría sobre un documento que solo registra qué archivo se descargó.)*
- ¿Qué parte del análisis podría estar confundiendo pobreza, desigualdad, violencia o informalidad con "cultura"?
- ¿Qué parte podría estar sobregeneralizando desde clases medias urbanas?
- ¿Qué parte está sesgada por literatura escrita desde marcos estadounidenses o europeos? `[NUEVO]` (incluye aquí las muestras mexicano-americanas, no solo los marcos).
- ¿Qué hallazgos cambiarían si el foco fuera México rural, indígena o popular?
- ¿Qué parece psicológico pero en realidad es un incentivo racional ante un entorno específico?
- ¿Dónde hay evidencia débil pero intuición social fuerte?
- ¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?
- `[NUEVO v2.1]` ¿Qué afirmación de este artefacto describe **el estado del corpus** —un conteo, una cobertura, una versión, la existencia de un archivo— y **no fue derivada, sino escrita a mano**?
- `[NUEVO v2.2]` ¿Qué restricción o deuda está heredando este artefacto sin verificar — una limitación cuyo perímetro nunca se midió, o una deuda declarada "asumida a propósito" cuando la función del programa era otra?
- `[NUEVO v2.3]` **¿Cuántos contadores movió el trabajo que produjo este artefacto?** Si la respuesta es cero, dilo en una línea al inicio del módulo, sin justificarlo. Hay artefactos que legítimamente no mueven contadores. Lo que no es legítimo es que nadie se dé cuenta.

---

## Bloque C · Validación forense `[NUEVO · CONDICIONAL]`

Para cualquier investigación que **pruebe supuestos contra desenlaces reales** (¿la apuesta conductual de tal organización funcionó?). No sustituye a Bloque A/B; los complementa. Los tres blindajes son obligatorios, porque sin ellos el análisis de casos recae en la narrativa post-hoc que el proyecto existe para evitar:

- **Anti-confusión.** Separa la variable psicológica de las estructurales (capital, logística, precio, regulación, timing, ejecución, suerte). Cuenta como evidencia "psicológica" **solo si fue plausiblemente decisiva**; si no se puede aislar, márcala CONFUNDIDO.
- **Anti-post-hoc.** Clasifica el supuesto: **DECLARADO** (la organización lo dijo *antes* del resultado — el oro, falsable) / **INFERIDO** / **RETROSPECTIVO** (solo aparece después — el más débil, se registra pero no prueba).
- **Anti-superviviente.** Busca activamente lo invisibilizado: éxitos silenciosos, fracasos por razones aburridas/estructurales, y sobre todo **pares contrafactuales** (misma jugada, distinto segmento/resultado, con la estructura constante y la variable conductual visible).

Además: **marca cada métrica como AUDITADA o AUTO-REPORTADA por parte interesada.** El entregable central es qué reglas del modelo el caso **CONFIRMA / MATIZA / ROMPE**. **Descartar con rigor es entregable, no fracaso.**

---

*Nota de alcance. Estas reglas gobiernan todo el programa: reports temáticos (Bloque B), el integrador y el modelo de decisión (estructura propia + Bloque A + auditoría), y las validaciones forenses (Bloque C). La v2 no cambia el espíritu de la v1 —anti-esencialismo, estructura sobre cultura, evidencia tierizada— solo lo hace explícito donde el proyecto tropezó: procedencia de la evidencia, el firewall genético, la crítica calibrada de marcos, y el hecho de que un modelo de decisión no es un report temático.*

*Las tres reglas de procedencia documental de v2.1 (lectura, cifras, premisas) atienden un tropiezo distinto: los defectos que el programa encontró auditándose no estaban en la evidencia sobre México, sino en las **afirmaciones del corpus sobre sí mismo**. La capa de evidencia resistió la auditoría; la capa de contabilidad sobre esa evidencia, no. Esa clase de defecto no se corrige con más cuidado: se corrige **derivando en vez de escribiendo, y verificando antes de obedecer**. Las cuatro de v2.2 extienden el mismo principio al **terreno** (restricciones no medidas), al **criterio** (umbrales imposibles), al **rótulo** (métodos implícitos) y al **calendario** (deudas que caducan).*

`[NUEVO v2.3]` Y atiende un tropiezo que las anteriores no podían ver, porque lo causaron. Cada regla de v2.1 y v2.2 fue una respuesta correcta a un error real. Juntas produjeron un programa que dedicó su jornada más productiva —15 PR fusionados— a auditarse, sin mover un solo contador. El rigor no falló por estar mal diseñado; falló por no tener un criterio de suficiencia. La v2.3 es ese criterio y es una sola frase: **cada sesión produce una medición, o produce nada.**

Si esta versión hace que el proyecto pase por alto un defecto de contabilidad, funcionó. Ese es el intercambio, y está tomado a propósito.
