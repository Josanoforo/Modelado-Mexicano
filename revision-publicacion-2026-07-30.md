# Revisión estratégica de publicación · 30/jul/2026

**Propuesta sin sello.** Derivada en sesión contra HEAD `c3adff8` (verificado: `git log -1`). Este documento no modifica ningún artefacto; propone texto. El sello lo da otra sesión (protocolo §2).

---

## 0 · Verificación de premisas del encargo (ADR-39) — hallazgos primero

Re-derivado en esta sesión, todo DATO salvo marca contraria:

| Premisa | Veredicto | Evidencia |
|---|---|---|
| HEAD `c3adff8`, main única* | ✅ Sostiene | `git log`, `git branch -a`. *Existe además la rama de trabajo de esta sesión de revisión, creada por la plataforma |
| 83 archivos · 31 reports · 5 + 23 forenses | ✅ Sostiene | `git ls-files | wc -l`; los 23 incluyen `historico/` (3) y `notas/` (4) |
| Suite 19 FAIL · 84 WARN · base VERDE en `c6dd7ee` | ✅ Sostiene | `python3 tests/check.py --baseline` corrido en sesión; `baseline.json` head = `c6dd7ee` |
| LICENSE / CITATION / CODE_OF_CONDUCT inexistentes | ✅ Sostiene | `ls` en raíz |
| `instrucciones-proyecto-v2.md` = v2.2 vigente | ✅ Sostiene | cabecera del archivo; `gobernanza` la cita como la subida más reciente |
| **H1** repo público desde 29/jul | ⚠️ Aceptado como DATO del encargo (procedencia 1) | No re-verificable desde esta sesión (acceso autenticado). **SUPUESTO [S1]:** público desde 29/jul; **reporta el valor** exacto (GitHub → Insights/Settings) y si hay forks |
| **H2** sin licencia = "peor de dos mundos" | ⚠️ Sostiene con matiz | Sin LICENSE el estado legal es *máximamente restrictivo*: nadie puede reutilizar nada legalmente. El daño es a lectores legítimos (citar, forkear); **no** es una puerta abierta al mal uso — el mal uso serio ignora licencias de todos modos. La urgencia de H2 es real pero su mecanismo es otro |
| **H3** README anuncia estado falso 18·110 | ❌ **No se sostiene como está escrita — pero el diagnóstico es correcto con otra línea, y peor** | `README.md:46` fecha las cifras: «Primera corrida de la suite · 28/jul/2026». Es afirmación histórica fechada, no de estado vigente. **La afirmación de estado falsa real es `README.md:40`:** «**1 de 27** reglas del perímetro con prueba de falsación corrida (`R1.1` → `B`)». Contra el registro append-only (`hitoD-preregistro:558-559`): **`R1.1` → `D`** y **`R3.2` → `B`** — dos corridas, no una (`estado:192`: «2 de 27»), y el veredicto `B` atribuido a la regla equivocada. Además `README.md:73-75` presenta en presente conteos de T03 (44) y T10 (65) que `estado:124` ya superó (T03 = 18 WARN hoy) |
| **H4** discrepancia 25 vs 27 | ✅ Sostiene | `grep -c "^## R[0-9]"` = 25; `hitoD-preregistro:8` dice 27; FAIL T17 congelado en baseline |
| **H5** «ninguna mención de asistencia de IA en todo el repo… cero coincidencias en canon» | ❌ **Falsa en su literalidad** | `gobernanza:317` (ADR-41): «De 25 commits, **21 tienen a Claude como autor**…»; ADR-43 define el esquema de co-autoría `Claude <modelo>`; `cola.yaml:2` y `protocolo §3` nombran a «el chat» y a «CC» como actores del proceso. Y el `git log` público lo muestra: **21 commits con Claude como autor, 12 Jonas, 4 corpus** (derivado en sesión). **Lo que sí falta —y es el punto de fondo de H5— es disclosure orientado al lector:** nada en README, CONTRIBUTING ni en los 31 reports le dice a quien llega frío que el corpus se produjo con asistencia de modelos. Consecuencia estratégica: **la opción "no declarar" no existe** — ya es público, verificable con un `git log` de treinta segundos. La única decisión viva es si el marco lo pone el autor o se lo pone un crítico |

**Hallazgo no pedido por el encargo:** no existe ADR que registre la decisión de hacer público el repositorio. Es el patrón exacto de ADR-42(1) —«el control cambió de semántica sin ADR»— aplicado al programa entero: la función pasó de privado-descriptivo a público-auditable sin pasar por gobernanza. Propuesta de ADR-44 en Fase 5. Confianza **Alta** (ausencia verificada por lectura completa de `gobernanza §4`).

---

## 1 · EL EJE — regla v2.2 sobre toda deuda asumida por decisión

«Toda deuda declarada asumida a propósito se re-examina cuando cambia la función del programa.» La función cambió el 29/jul. Dictamen una por una (fuentes: `gobernanza §5`, `estado §4`, `cola.yaml`, cabeceras de `modelo`):

| # | Deuda / decisión | Registro | Dictamen bajo función pública | Conf. |
|---|---|---|---|---|
| 1 | Cero datos primarios propios | gob §5 «asumida a propósito» | **Ya había caducado** — la propia v2.2 la caducó al pasar de describir a validar. La publicación la caduca por segunda vez: ahora es además una promesa pública (README:42 la declara). PENDIENTE con ruta (CAL-G3 pre-registrada, `hitoD-preregistro` Nota 7) | Alta |
| 2 | PD-01 · 14 descartes, no reconstruir | gob §5 cerrada | **Sigue decisión.** Publicar no cambia el argumento: un descarte fabricado es indistinguible de uno real, y fabricarlo *para lectores* sería peor. Ya está declarada; defendible tal cual | Alta |
| 3 | Sistema indígena-comunal fuera (ADR-10) | gob §5 cerrada por diseño | **Sigue decisión**, pero su defensa vivía en documentos interiores (`modelo §0.2`, instrucciones). Con lectores, necesita estar en el aviso de portada o se leerá como omisión, no como diseño. Caduca *la forma*, no el fondo | Alta |
| 4 | 15 coeficientes / 74 números ASIGNADOS | gob §5 abierta con ruta | **Sigue decisión** *condicionada a que la portada lo diga* — lo dice (README:34, derivable de `modelo §6/§7`). La condición nueva es que la portada sea verificada por test (rama vi) | Alta |
| 5 | 8 refutaciones sin objeto, incl. `ref.A.02` MUY_FUERTE | gob §5 «decisión pendiente» | **Caducó → pendiente urgente.** En privado era una disyuntiva aplazable; en público, una batería que declara inaplicable su única refutación MUY_FUERTE («los mexicanos son flojos», 2,207 h/año) es lo primero que un crítico citará. Decidir por ADR: declarar alcance y retirarlas es la opción honesta y barata | Alta |
| 6 | Baseline congelado con la autodeclaración falsa de `hitoD-preregistro:8` (T17), «por decisión de mesa» | `estado:212`, cola D-01 | **Caducó.** Deuda de mesa privada; en público es *un pre-registro cuya portada dice 27 y contiene 25*, congelado a sabiendas. Exactamente lo que la pregunta #8 persigue, en el artefacto más sensible. Resolver D-01 por ADR y escribir las 2 fichas faltantes (R3.1, R3.4) la elimina de raíz | Alta |
| 7 | MILPA Fase 1 pospuesta por decisión | gob §5 / estado §7 | **Sigue decisión; caduca su presentación.** Publicar spec+plan de algo que no existe convierte el posponer en promesa pública abierta (rama de Fase 4). Banner de estado, no retiro | Media |
| 8 | D-02/D-03 «no se tocan: son el blanco» | `modelo` v3.1 cabecera | **Sigue decisión** — es la disciplina del pre-registro y está declarada en el propio archivo. Defendible en público tal cual; incluso es de lo mejor que un auditor puede encontrar | Alta |
| 9 | Honor «híbrido» abierto por decisión | gob §5.1 | **Sigue decisión** (posición matizada declarada en el casillero). Sin cambio | Media |
| 10 | R10.3: veredicto `D` preferible por límite ético | `estado:184` | **Sigue decisión.** Publicable y defendible; es un ejemplo a favor | Alta |
| 11 | conf.02 / conf.05 / conf.06 | casillero S5 | Pendientes con casillero, no decisiones. Sin cambio de clase; conf.06 ya bloquea cifras y así debe leerse en público | Alta |
| 12 | «El repo es privado / esto solo lo leemos nosotros» | **ningún registro** | **Restricción nunca verificada (v2.2).** Todo el tono del registro —nombres, autocríticas con hash, rutas de máquina en `cola.yaml:83`, deudas «de mesa»— se escribió asumiendo lector interno, y esa asunción jamás se declaró ni se midió. Desde el 29/jul es falsa. Es la restricción-fantasma de este momento, análoga al «sin salida de red» que v2.2 documenta | Alta |
| 13 | «El README se mantiene a mano» | ningún registro | Nunca fue decisión: es deuda no declarada. → PENDIENTE (rama vi, T-README) | Alta |

---

## FASE 1 · Qué es esto, para un extraño

**Lo que el lector frío encuentra:** un modelo de decisión sobre conducta de poblaciones mexicanas —6 perfiles, 7 generadores, 49 reglas SI-ENTONCES con tiers— construido por síntesis de literatura, más un aparato inusualmente severo para intentar romperlo: suite de 18 tests con línea base, pre-registros de falsadores escritos antes de buscar, registro append-only de veredictos, 43 ADR que documentan cada reversa, y un historial forense que registra los errores propios con fecha, hash y nombre (caso «pelón», ADR-38; TRANSFER-8 con siete premisas falsas; «5 de 5 afirmaciones de estado comprobadas resultaron falsas», CONTRIBUTING:42).

**Lo que el programa cree ser vs. lo que el lector entenderá.** El programa se narra como *modelo + aparato*. Un lector externo competente verá las proporciones invertidas: el modelo tiene 144 números con 4 medidos (97.2% no medido, `modelo §6`), 0 de 15 coeficientes medidos, y 2 de 27 falsadores corridos. Eso no es un artefacto validado y el propio repo lo dice (`modelo §7`, «lectura correcta de este marcador»). Lo que **sí** es de primer nivel —y raro en cualquier disciplina— es el aparato: la maquinaria de auto-refutación y su registro de fallos.

**Dictamen sobre la tesis del README («T11 es el que justifica el repo entero»): se sostiene, y la evidencia más fuerte es nueva.** La primera vez que el programa tocó dato primario (R3.2 contra ENCIG 2023, `hitoD-R3_2-veredicto`), el resultado fue que las probabilidades del propio motor quedaron **refutadas en escala** —el valor asignado estaba 4x–34x por encima de lo medido— y el umbral pre-registrado resultó aritméticamente inalcanzable. Es decir: el primer contacto del modelo con la realidad degradó al modelo, y el aparato lo registró sin anestesia y generó tres reglas nuevas de rigor (v2.2). **El producto publicable es el aparato de falsación con el modelo como banco de pruebas — no al revés.** Confianza **Alta**.

**La brecha para el extraño:** sin aviso de portada, el lector no sabe cuál de las dos cosas está mirando. El lector benévolo verá un modelo a medio validar; el hostil verá «un particular publicó, con asistencia de IA y bajo nombre real, 144 números sobre los mexicanos, de los cuales inventó 74». Las dos lecturas se bloquean con el mismo artefacto: el aviso de alcance de Fase 5.

---

## FASE 2 · Mapa de aristas (12)

Obligatorias: **(i)** legal y licencias · **(ii)** autoría y disclosure de IA · **(iii)** riesgo de daño y mal uso · **(iv)** epistémico y reputacional · **(v)** modelo económico Patreon · **(vi)** integridad de la portada.

Elegidas: **(vii)** gobernanza de la publicación (la decisión sin ADR; qué cambia en el protocolo con lectores) · **(viii)** higiene de exposición (datos de máquina y persona en el árbol y la historia) · **(ix)** integridad del gate público (el medidor como superficie de ataque con contribuyentes externos) · **(x)** sostenibilidad y cadencia (bus factor 1, jornadas de madrugada, y lo que Patreon les hace) · **(xi)** citabilidad y versionado (cómo se cita esto sin tergiversarlo) · **(xii)** idioma y audiencia (corpus mixto ES/EN contra la regla «Español»).

Descartadas explícitamente: *datos personales de terceros* (no hay microdato en el árbol; `data/manifiesto.yaml` + `.gitignore` implementan «manifiesto y checksum, nunca el payload» — diseño correcto, verificado); *seguridad de cadena de suministro* (suite en stdlib pura, sin dependencias); *infraestructura y costos* (repo estático); *marca/registro* (prematuro); *accesibilidad/SEO* (markdown plano, prematuro).

---

## FASE 3 · Desarrollo rama por rama

### (i) Legal y licencias

**Estado:** cero licencias. Default GitHub: todos los derechos reservados. `data/manifiesto.yaml` cita los Términos de Libre Uso del INEGI para ENCIG (con la honestidad de anotar «texto completo no verificado»). `milpa-plan:128` promete «la licencia prohíbe el uso para scoring de personas» para un sistema que no existe; hoy nada lo implementa.

**Sub-rama código (`tests/`, workflows).** Opciones: MIT / Apache-2.0 / GPL. Es una suite de ~1,000 líneas en stdlib; la cláusula de patentes de Apache no aporta y GPL no protege nada que importe aquí. **MIT.** Preferirías Apache-2.0 solo si esperas que la suite se convierta en producto adoptado por terceros con riesgo de patentes — no es el caso.

**Sub-rama corpus (reports, forense, canon, milpa — obra de texto).** Por qué no la misma que el código: una licencia de software habla de código objeto, binarios y linking; sobre prosa produce ambigüedad pura. Opciones reales:
1. **CC BY 4.0** — máxima citabilidad y reutilización académica. Coste: cualquier consultora puede empaquetar y vender el corpus mañana; renuncias a toda palanca comercial.
2. **CC BY-NC 4.0** — bloquea reuso comercial (incluido el empaquetado por terceros y buena parte del mal uso *formal*: un scoring comercial que reproduzca el texto viola la licencia). Coste: fricción real para citas en contextos corporativos, y la frontera «NC» es notoriamente ambigua.
3. **CC BY-SA 4.0** — copyleft. No bloquea scoring (un scoring no «comparte» nada) y añade fricción; descartada.
4. **Licencia a medida tipo RAIL con cláusula anti-scoring** — la cláusula que `milpa-plan` prometía. Coste: no estándar, espanta reuso legítimo, y su ejecutabilidad real es débil.

**Sobre la ejecutabilidad de la cláusula anti-scoring — dicho sin adornos:** el derecho de autor protege la *expresión*, no los hechos ni las ideas. Las 49 reglas como proposiciones, los valores, los mecanismos — cualquiera puede reimplementarlos sin copiar texto y ninguna licencia lo impide (INFERENCIA jurídica general, confianza Media; verificar con abogado — y ojo: mi análisis usa doctrina angloamericana; la LFDA mexicana difiere en derechos morales y régimen de cita). La defensa técnica real contra el scoring no es contractual: es que **el propio repo documenta que 74 de los números son ASIGNADOS y 0 coeficientes están medidos** — un despacho que construya scoring sobre números que la fuente marca como inventados queda indefendible ante cualquier auditoría, y conviene decírselo en la cara (NOTICE de Fase 5). La cláusula se incluye igual: su función es normativa y reputacional (fija la posición del autor *antes* del primer abuso), no preventiva.

**Sub-rama datos públicos.** INEGI (ENCIG, ENOE, ENIGH…): Términos de Libre Uso — atribución obligatoria, no implicar aval de INEGI; compatibles con cualquiera de las opciones porque el payload nunca se commitea y las estadísticas derivadas son hechos. ENNViH/MxFLS (la ruta de CAL-G3): **no es INEGI**; requiere registro y sus términos de uso no están en el repo — **reporta el valor** antes de commitear cualquier derivado.

**Recomendación:** MIT para `tests/` y workflows; **CC BY-NC 4.0** para todo lo demás, con NOTICE anti-scoring declarativo. Asimetría decisiva: relajar NC→BY después es trivial y siempre posible; recorrer el camino inverso es imposible para las copias ya licenciadas. Empezar restrictivo cuesta poco (el público objetivo hoy —académicos, curiosos, futuros mecenas— no es comercial). **Preferirías CC BY** si la meta dominante fuera adopción académica y citas rápidas — es la pregunta 2 de la Fase 9.
**Riesgo:** prob. Media, severidad Media; lo dispara cualquier reuso comercial temprano. **Segundo orden:** la licencia decide qué puede cobrar Patreon (rama v) y qué puede exigirse a un fork hostil (rama iv). **Señal temprana de que se tuerce:** aparece un derivado comercial y la reacción es litigiosa en vez de reputacional — sería gastar el activo equivocado.

### (ii) Autoría y disclosure de IA

**Estado (corregido por §0):** la asistencia de IA está *registrada hacia adentro* (ADR-41/43, git log con Claude como autor de 21 commits, protocolo que reparte roles entre «chat», «CC» y humano) y *ausente hacia afuera* (ni README, ni CONTRIBUTING, ni los reports). Esa combinación es la peor disponible salvo una: mentir. La historia git ya lo cuenta; cualquier crítico lo encontrará en minutos.

**Qué se declara:** (1) el hecho — corpus, canon y suite redactados con asistencia intensiva de modelos Claude, bajo dirección, decisión y verificación humanas; (2) el método — el reparto exacto de roles que `protocolo §3` ya define (el chat propone y no escribe hechos; CC escribe; la suite verifica; el humano decide en mesa); (3) la implicación honesta — los errores documentados del programa incluyen la clase de error típica de LLM (afirmar contenido de archivos sin verificar: caso «pelón»), y el aparato de verificación existe en buena parte *por eso*; (4) la trazabilidad — commit por commit vía trailers desde ADR-43.

**Granularidad — opciones:** (a) AUTHORSHIP.md a nivel repo + línea en README + entrada en CITATION; (b) además, cabecera por report; (c) además, nota fechada anexada a cada uno de los 31 reports. **Recomendación: (a).** (b) y (c) chocan con el carácter append-only —31 notas fechadas idénticas son ruido que degrada el registro— y no añaden información: la procedencia por archivo ya vive en `git log --follow`. **Preferirías (c)** si algún report circulara suelto fuera del repo (PDF, reimpresión); en ese caso la nota viaja con el artefacto.
**Riesgo si no se hace:** prob. Alta, severidad Alta — es el único defecto que puede contaminar retroactivamente el activo principal (el aparato), porque el descubrimiento por terceros convierte «no lo dijo» en «lo ocultó». Lo dispara un solo tuit con captura del git log. **Segundo orden:** el disclosure bien hecho *fortalece* la rama (iv): un programa que documenta sus propios errores de IA con hash es más creíble, no menos. **Señal temprana:** cualquier pregunta pública sobre autoría que llegue antes que el AUTHORSHIP.md.

### (iii) Riesgo de daño y mal uso

**Estado:** el modelo emite afirmaciones probabilísticas sobre segmentos por clase, región, género y escolaridad. Frenos hoy: las seis prohibiciones duras de `modelo §5.0` (normas internas, no condiciones de uso), `whitepaper §7.3` (gobierna un sistema inexistente), y —irónicamente— la ausencia de licencia, que prohíbe formalmente todo reuso. Nada de eso detiene a un actor decidido.

**Usos abusivos plausibles, por facilidad:**
1. **Cobranza y originación de crédito popular** — el más fácil. `milpa/procedencia.yaml:194` trae literalmente `dinero.credito.scoring_alternativo` con valores; R1.6/R1.7 describen el techo de mora y el daño downstream. Quién: fintechs de nicho, despachos de cobranza. Facilidad: Media — las p están ahí, aunque el repo mismo las marca ASIGNADO.
2. **Operación político-electoral** — el más grave. R7.6 y el hallazgo Ascencio-Chang (0.06→0.63 bajo percepción de monitoreo) son, leídos al revés, **un manual de cómo hacer eficaz la compra de voto: fabricar percepción de observabilidad**. Quién: consultoras de campaña. Facilidad: Media-Alta — no requiere números, solo el mecanismo. Este es el caso donde el corpus documenta un arma, no un rasgo.
3. **Segmentación laboral/aseguradora** (perfiles como proxy de riesgo). Facilidad: Baja-Media; los perfiles son cualitativos.
4. **Targeting migratorio/estatal** — improbable hoy (el Estado tiene mejores datos), severidad extrema si ocurre.

**Verificación pedida por el encargo:** `modelo §5` sí dice algo y es sustantivo (seis prohibiciones, incluida «ninguna afirmación sobre "el mexicano" sin segmento» y la prohibición de burbuja), pero **son prohibiciones sobre lo que el modelo emite, no sobre lo que el lector hace**. No hay una línea dirigida al usuario del repo. Insuficiente para exposición pública. Confianza **Alta**.

**Opciones:** (1) NOTICE declarativo + prohibición en licencia NC (recomendada); (2) retirar los YAML con p (`tramite.yaml`, `procedencia.yaml`) — coste: amputa el aparato de trazabilidad que es el activo, y ya son clonables; renuncia inaceptable; (3) no hacer nada y confiar en §5 — deja al autor sin posición declarada el día del primer abuso. **Recomendación: (1)**, más un párrafo específico en el aviso de portada sobre la lectura dual de R7.6 (nombrar el riesgo es la única mitigación disponible para conocimiento ya público). **Preferirías (2)** solo si apareciera evidencia de uso operativo real de esos YAML. **Señal temprana:** tráfico/forks desde dominios corporativos de cobranza o consultoría política; menciones del repo en pitch decks.

### (iv) Epistémico y reputacional

**Estado:** superficie de ataque de un auditor hostil, en orden: (1) `README:40` — la portada contiene una afirmación de estado falsa *en un proyecto cuya tesis es que eso no debe poder pasar*; (2) 74 ASIGNADOS / 0 coeficientes medidos; (3) constructos (b) de diáspora estructurando el esquema (el propio módulo de auditoría del modelo lo confiesa: «se está reestructurando el esquema sobre medición de diáspora»); (4) ADR-10 leído como «dejaron fuera a los indígenas»; (5) el título del programa —«Psicología del Mexicano Contemporáneo»— viola la regla de su propio Bloque A («ninguna afirmación sobre "el mexicano" sin segmento»); un auditor con humor lo usará de epígrafe; (6) autoría IA sin disclosure de portada.

**Defensa que existe:** tierización con procedencia (a)/(b)/(c); pre-registro antes de búsqueda; los FAIL a la vista y congelados con explicación (ADR-42); R3.2 auto-refutando la escala del motor; sesgo de clase declarado en `modelo §0.2`; ADR-10 argumentado como error categorial, no como omisión. **Defensa que no existe:** revisión externa de cualquier tipo; credencial del autor; datos primarios (uno en curso); y la portada — que hoy juega para el otro equipo.

**Opciones:** (1) remediar portada + avisos y *esperar* la auditoría hostil como evento positivo (el aparato está construido exactamente para eso); (2) buscar activamente revisión externa temprana (invitar a 2-3 investigadores a romperlo, registrando veredictos en el pre-registro); (3) bajar el perfil del modelo en portada y presentar el repo como «aparato de falsación con caso de estudio». **Recomendación: (1) ya, (2) antes del Patreon** — una auditoría externa *invitada y sobrevivida* es el único sustituto disponible de credenciales. **Preferirías (3)** si el autor decide que el modelo nunca será el producto; es media reescritura de identidad y no urge. **Señal temprana:** la primera crítica pública que cite `README:40` o el git log antes de que estén remediados — a partir de ahí toda respuesta parece control de daños.

### (v) Modelo económico Patreon

**Estado:** cero menciones de Patreon en el repo (grep corrido — correcto: la intención vive fuera). Audiencia aún inexistente.

**Qué se cobra si el repo es abierto.** Lo que no se puede cobrar: las conclusiones (abiertas, y NC no cambia eso para lectura). Lo cobrable sin envenenar el programa: **el proceso en vivo** — bitácora comentada, sesiones de falsación narradas (la corrida de R3.2 es, contada bien, un thriller de datos), voto de mecenas sobre el *orden* de la cola (nunca sobre veredictos ni umbrales), acceso anticipado a borradores no-canon, derivados pedagógicos (la masterclass ausente, visualizaciones), y agradecimiento en CITATION. La regla dura que lo protege: **el dinero puede elegir qué se prueba antes, jamás qué resultado se archiva ni cuándo se detiene una sesión.** Escribirla en el protocolo *antes* del primer mecenas.

**El conflicto, nombrado:** un Patreon premia publicar con cadencia; este programa premia detenerse, verificar y archivar derrotas. El registro histórico (derivado del git log: sesiones de 23:47 a 05:31) muestra jornadas que terminan rehaciendo lo hecho. **Resolución propuesta, no solo declarada:** vender exactamente lo que el programa produce de verdad — *veredictos honestos como espectáculo*. Un `D` o un `B` bien narrado es contenido de la misma calidad que un `A`; la cadencia comprometida es de **proceso** («una corrida de falsador documentada al mes, gane o pierda»), nunca de hallazgos. Esto convierte el incentivo perverso en alineado: al mecenas se le vende la honestidad, así que falsificarla destruye el producto. **Riesgo residual real:** sesgo de selección — elegir falsadores «taquilleros» en vez de informativos. Ya hay criterio interno que lo detecta: `estado:206` ordena «por valor informativo y no por facilidad» (R3.2 → R5.1 → R7.2). **Señal temprana:** la cola se reordena y el orden nuevo correlaciona con drama, no con ese criterio.

**Opciones:** (1) Patreon de proceso como arriba; (2) contenido exclusivo permanente — rompe la apertura y crea dos clases de lector sobre un corpus cuya legitimidad es la transparencia; descartada con nombre; (3) no monetizar hasta tener el primer coeficiente MEDIDO y una auditoría externa sobrevivida — la opción conservadora. **Recomendación: (3) como secuencia y (1) como forma** — abrir el Patreon con CAL-G3 medido es abrir con un producto verdadero. **Preferirías (2)** solo para derivados que nunca tocan el canon (cursos, PDFs de diseño).

### (vi) Integridad de la portada

**Estado:** un defecto activo (`README:40`, falso contra el registro), dos vigencias vencidas presentadas en presente (T03/T10 en §Falsos positivos), y cifras correctas pero tecleadas (README:34 cuadra contra `modelo §6/§7` — verificado en sesión — pero nada lo vigila; README:21-22 «31 reports / 5 forenses» cuadra — verificado — ídem). En un programa cuya tesis es «deriva, no escribas», la portada es hoy el único artefacto de estado sin test. T14/T15/T16/T17 vigilan `estado` y `gobernanza`; nadie vigila README.

**Opciones:** (1) **T-README**: test que extrae las cifras de bloques marcados del README y las compara contra derivación (mismo molde que T16); coste: una tarde; (2) generar el bloque de estado del README desde `bitacora.py` (ya deriva FAIL/WARN, HEAD, versiones); coste: bajo, pero acopla README a un script que aún muta; (3) política «README sin cifras»: portada solo cualitativa + enlace a `estado` — elimina la clase de defecto entera al precio de una portada menos potente. **Recomendación: (1) ya, (2) después.** El molde existe; la regla de la casa («todo principio nuevo nace con su test», ADR-32) lo exige. **Preferirías (3)** si el mantenimiento demuestra que la portada muta más rápido que la suite. **Señal temprana:** el segundo defecto de cifra en README tras implementar T-README — significaría que el test tiene el perímetro mal medido, el defecto de T05.

### (vii) Gobernanza de la publicación

**Estado:** publicación sin ADR (§0). El protocolo de sesión, la mesa, la cola — todo asume dos actores y cero espectadores. **Falta:** ADR-44 registrando qué se decidió, cuándo, y qué obliga (los artefactos de Fase 5 como requisitos de salida); política de contribución externa (CONTRIBUTING gobierna *cómo* se cambia, no *quién* — hoy un PR de un extraño es un evento sin protocolo); estado real de protecciones de rama — **reporta el valor** (no derivable del árbol; Settings → Branches). **Opciones:** (1) ADR-44 + PRs externos solo-lectura de facto (se agradecen, se procesan como encargos de mesa); (2) abrir contribución con CODEOWNERS y revisión obligatoria; (3) congelar main a un solo escritor. **Recomendación: (1)** — el programa no tiene ancho de banda para (2) y (3) es (1) sin decirlo. **Señal:** el primer PR externo; si toma más de una sesión decidir qué hacer con él, faltó el protocolo.

### (viii) Higiene de exposición

**Estado:** `cola.yaml:83` publica ruta de máquina personal (`/mnt/c/Users/PC0/Downloads/...`, con nombre de usuario del equipo); correo personal y nombre en toda la historia (decisión ya consumada al publicar bajo nombre real); TRANSFER-maestra-* revisados por grep: proceso, sin datos de terceros. Los reports sobre desaparecidos y salud mental operan sobre agregados — sin individuos identificables (INFERENCIA por muestreo de grep, no lectura íntegra de los 31; confianza Media). **Qué hacer:** editar `cola.yaml` (es canon vivo, no append-only) anonimizando la ruta, con nota; asumir que la ruta ya es pública (la historia la conserva y ADR-41 prohíbe reescribirla — correctamente). Daño residual: trivial (un nombre de usuario local no es credencial). Para commits futuros: considerar el correo noreply de GitHub. **Señal:** cualquier aparición futura de rutas `/mnt/c/` o similares en un diff — candidato a exención pre-commit en la disciplina de sesión.

### (ix) Integridad del gate público

**Estado:** `verify.yml` corre `check.py --baseline`; ADR-42 documenta que verde = «nada nuevo», no «sano». Dos exposiciones nuevas con lectores: (1) el checkmark verde de Actions **comunica «passing» a cualquier visitante** que jamás leerá ADR-42 — la semántica privada del verde caducó (regla v2.2, fila 6 de la tabla eje); (2) un PR puede editar `baseline.json`, `check.py` y el defecto en el mismo diff, y el CI pasa — el medidor es parte de la superficie editable. `protocolo §4.2` lo prohíbe, pero es disciplina sin test, y la cola I-03 ya registra que el baseline ni siquiera identifica la versión del check que lo produjo. **Opciones:** (1) declarar la semántica del verde en README (una línea, ya redactada en Fase 5) + regla de revisión: ningún PR toca `tests/baseline.json` junto con otra cosa; (2) branch protection + revisión obligatoria para `tests/`; (3) job adicional informativo que corre `check.py` sin `--baseline` y publica el conteo completo en el log. **Recomendación: (1)+(3)** ya (coste ~cero), (2) cuando exista el primer contribuyente externo. **Señal:** un PR externo que toque `tests/` — tratarlo como evento de gobernanza, no como parche.

### (x) Sostenibilidad y cadencia

**Estado:** un humano + modelos; commits de esta semana entre las 23:47 y las 05:31 (derivado del log); el protocolo de sesión nació precisamente porque «el programa gastaba la primera hora de cada sesión reconstruyendo». La publicación añade espectadores; el Patreon añadiría acreedores. **Riesgo:** prob. Media-Alta, severidad Media — degradación de rigor por fatiga es exactamente la clase de error que el registro ya documenta (TRANSFER-8, siete premisas falsas, nació de una jornada así); con lectores, cada error de fatiga es público. **Opciones:** (1) tope de cadencia autoimpuesto en protocolo (p. ej., una sesión de canon por día; ninguna sesión de canon tras medianoche — el registro muestra que ahí viven los defectos); (2) sin cambios, confiar en la suite como red; (3) buscar segundo mantenedor. **Recomendación: (1)**; la suite atrapa clases conocidas de error, no las nuevas, y las nuevas nacen de madrugada. **Señal:** dos correcciones consecutivas cuya causa raíz sea un commit posterior a las 00:00.

### (xi) Citabilidad y versionado

**Estado:** versionado por archivo (ADR-36) impecable; a nivel repo: sin tags ni releases (**reporta el valor** — no lo verifiqué), sin CITATION.cff, sin DOI. Quien cite hoy citará «el repo», que muta a diario — tergiversación garantizada por diseño. **Opciones:** (1) CITATION.cff con instrucción de citar por commit + nombre estable del artefacto; (2) además, releases fechados (v2026.07) como fotos citables; (3) además, DOI vía Zenodo. **Recomendación: (1) ya, (2) al abrir Patreon, (3) solo si aparece interés académico real.** **Señal:** la primera cita pública que atribuya al programa una afirmación de una versión superada.

### (xii) Idioma y audiencia

**Estado:** regla de la casa «Español» (`estado §5`); 6 de los 31 reports llevan título y presumiblemente cuerpo en inglés (derivado del listado: Humor, Population Genomics, Health/Body, Non-Family Social Capital, Psychology of Migration, Report 26). Menor, pero un auditor que busque incoherencias la encontrará en el `ls`. Los nombres de archivo con acentos y dobles guiones bajos sobreviven en GitHub; molestan en shells ajenos. **Recomendación:** una línea en el aviso de portada («el corpus es principalmente en español; N reports conservan el idioma de su corrida original») — es append-only, no se renombra ni se traduce. Coste: una frase. **Señal:** ninguna; esta rama no puede torcerse, solo quedar sin declarar.

---

## FASE 4 · El corpus, por clase de artefacto

**Reports temáticos (31).** Publicables tal cual **con aviso global al frente del repo**, no editados (append-only). El aviso debe decir tres cosas que la suite ya sabe: 7 carecen de mapa de evidencia (T08 los nombra — todo constructo suyo es DERIVADO), 8 usan marco importado como causa sin marca (c) (T09), y ninguna cifra de un report individual debe citarse sin cruzar contra `glosario`/`modelo` (la regla de la casa, dicha al lector). No se audita report por report: la suite ya lo hace en cada push y sus hallazgos están congelados a la vista.

**Forenses y forenses de proceso (5 + 23).** ¿Activo o pasivo? El caso pasivo es real: son munición literal —«5 de 5 afirmaciones comprobadas resultaron falsas», un hallazgo falso propagado en 17 segundos con hashes— y un crítico perezoso puede citarlos sin contexto. El caso activo: son **el único componente del repo que no se puede fingir** — nadie fabrica dos meses de errores propios fechados, con hash, contra su propio interés; sin credenciales ni datos primarios, la honestidad procesal verificable es el único capital del programa, y es exactamente el capital que la literatura de integridad científica no puede comprar. **Dictamen: activo, con una condición no negociable — la portada los enmarca antes de que el lector los encuentre.** La diferencia entre «mira cuántos errores cometió» y «mira lo que hace cuando se equivoca» la decide quién cuenta la historia primero. Confianza **Alta**.

**Canon — `modelo-decision-v3_3`.** ¿Entera, capada, o con gate? Ya es pública desde ayer: capar ahora no retira nada (clonable) y emite la peor señal disponible (esconder lo que ya se vio). El documento es autocontenido *con sus límites dentro* (§0.1 procedencia, §0.2 frontera, §5 prohibiciones, §7 marcador honesto) — está mejor blindado que cualquier resumen que se publique de él. El riesgo real es el *quote-mining* de reglas sueltas sin tier; se mitiga con el NOTICE y con la instrucción de cita de §9, elevada al aviso de portada. **Dictamen: entera.** Confianza **Alta**.

**MILPA.** ¿Publicar una promesa es deuda? Sí — deuda de expectativa, la única clase que este programa aún no cataloga. Pero el whitepaper contiene las fronteras duras (§7.3, la prohibición de salida a individuo real) que conviene tener públicas *antes* de que exista el sistema — son el pre-registro ético. **Dictamen: se queda, con banner de estado en los tres documentos vía README** («diseño; no existe implementación; Fase 1 pospuesta por decisión» — el README:24 ya lo dice a medias). Retirarla señalaría que las promesas del repo se administran, que es peor que tener una abierta y fechada.

**tests/ y CI.** Lo más defendible del repo, y **sí: es la portada** — en el sentido de que el pitch verdadero del programa es «clona y corre `python3 tests/check.py`». Ningún otro artefacto le da al extraño verificación en treinta segundos. El README debería subir esa invitación (ya la insinúa en la línea 10) y explicar el verde de ADR-42 en una línea.

**`instrucciones-proyecto-v2.md`.** Verificado: la copia commiteada es v2.2 y coincide con la vigente que gobernanza cita (DATO, cabecera + changelog). Publicable; junto con la suite, es de lo más citable que hay aquí.

**Qué no debe estar público:** una sola cosa, menor — la ruta de máquina en `cola.yaml:83` (rama viii). Se edita en HEAD con nota; retirarla de la historia exigiría reescribirla, lo que ADR-41 prohíbe con razón. Implicación de que ya se pudo clonar: se asume pública; daño trivial. **Nada más del árbol amerita retiro.** Confianza **Alta** (barrido de grep por rutas, correos, nombres; lectura de cola, manifiesto, TRANSFER).

---

## FASE 5 · Lo que falta escribir

Orden de escritura = orden de esta lista. Cada uno con la falla concreta que previene.

**1 · LICENSE (raíz, MIT — cubre `tests/` y `.github/`).** Previene: inutilizabilidad legal del único artefacto ejecutable. Escribe: el autor (es una elección de titular). Borrador literal:

```
MIT License

Copyright (c) 2026 Jonas <REPORTA EL VALOR: nombre legal completo>

Se aplica a los archivos *.py de tests/ y a .github/workflows/.
El resto del repositorio se licencia según LICENSE-CORPUS.md.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**2 · LICENSE-CORPUS.md.** Previene: reuso comercial sin control y ausencia de posición declarada ante el mal uso. Borrador literal:

```markdown
# Licencia del corpus

Todo el contenido de este repositorio, salvo los archivos cubiertos por
LICENSE (código en tests/ y .github/), se publica bajo
**Creative Commons Atribución-NoComercial 4.0 Internacional (CC BY-NC 4.0)**.
Texto legal: https://creativecommons.org/licenses/by-nc/4.0/legalcode.es

**Atribución requerida:** "Psicología del Mexicano Contemporáneo", Jonas
<REPORTA EL VALOR: forma de cita preferida>, con el hash de commit de la
versión citada. Ver CITATION.cff.

Los datos externos referidos en data/manifiesto.yaml conservan los términos
de sus fuentes (p. ej., Términos de Libre Uso del INEGI). Este repositorio
no redistribuye microdatos.

## Aviso de uso (NOTICE)

Este corpus y su modelo NO deben usarse para evaluar, puntuar o tomar
decisiones sobre personas reales — crédito, contratación, aseguramiento,
cobranza, focalización política o migratoria — ni sobre segmentos como
proxy de personas. Dos razones, en orden de importancia:

1. **No funciona para eso, y el propio repositorio lo documenta:** de los
   144 números del modelo, la mayoría lleva etiqueta ASIGNADO (juicio, no
   medición) y ningún coeficiente de generador está medido (`modelo §6`).
   Cualquier sistema de decisión construido sobre estos valores hereda esa
   procedencia, y este aviso es citable en su contra.
2. Las reglas del dominio cívico (`modelo §3.7`) documentan mecanismos de
   manipulación electoral con fines de falsación. Usarlas operativamente
   invierte su propósito. Quien lo haga no podrá alegar ignorancia: este
   aviso existe desde antes.

Este aviso es una condición declarada del autor sobre el uso previsto. La
licencia CC BY-NC prohíbe además todo uso comercial sin permiso expreso.
```

**3 · AUTHORSHIP.md.** Previene: el descubrimiento hostil de lo que el git log ya muestra. Borrador literal:

```markdown
# Autoría y asistencia de IA

Este programa se produce con asistencia intensiva de modelos de lenguaje
(Claude, Anthropic), bajo dirección, decisión y verificación humanas.
No es una nota al margen: es parte del método, y está registrado.

**Quién hace qué** (protocolo de sesión, `canon/protocolo-sesion-v1_0.md`):

- **El humano (Jonas)** decide: alcance, decisiones de mesa, ADRs, qué
  entra al canon y qué se descarta. Ninguna regla, tier o veredicto se
  archiva sin decisión humana.
- **Los modelos** redactan, sintetizan literatura, proponen hipótesis y
  ejecutan encargos. El chat tiene prohibido escribir hechos sobre el
  repo en un traspaso (protocolo §3): es un generador de sospechas
  falsables, no una fuente.
- **La suite (`tests/check.py`)** verifica: 18 tests que vigilan conteos,
  procedencia, tiers y afirmaciones del corpus sobre sí mismo, en cada
  push (CI).

**Trazabilidad:** desde ADR-41/ADR-43 (`canon/gobernanza-v1_11.md §4`),
cada commit registra autor humano y modelo co-autor con esquema fijo. La
historia previa —21 de los primeros 25 commits con el modelo como autor—
se conserva sin reescribir: es el registro fiel de cómo se hizo.

**Lo que esto implica para el lector:** la clase de error típica de un
modelo de lenguaje —afirmar el contenido de un archivo sin haberlo
verificado— ocurrió aquí, está documentada con hash y fecha (ADR-38,
caso "pelón"), y buena parte del aparato de verificación de este repo
existe como respuesta. La confianza que este corpus pide no es "lo
escribió un humano": es "todo lo que afirma es derivable, y lo que no,
está marcado".
```

**4 · Aviso de alcance y limitaciones — bloque para el frente del README** (previene las lecturas hostiles de Fase 1; se inserta después de la línea 8):

```markdown
## Antes de leer nada — alcance y límites

- **Qué es esto:** una síntesis de literatura con tiers de evidencia y un
  modelo de decisión **en proceso de falsación** — no un artefacto validado.
  De 144 números, 4 están medidos; de 15 coeficientes, 0 (`modelo §6`).
  2 de 27 falsadores pre-registrados se han corrido (`hitoD-preregistro`,
  bloque de veredictos).
- **Qué no es:** una herramienta para decidir sobre personas. Ver el aviso
  de uso en LICENSE-CORPUS.md.
- **Sesgo declarado:** el corpus sobre-muestrea al clasemediero urbano
  formal y sub-muestrea al popular informal (`modelo §0.2`). El sistema
  indígena-comunal vivo queda fuera **por diseño**: es otro orden
  institucional, no un hueco (ADR-10).
- **El verde del CI no significa "sin defectos":** significa "ningún
  defecto nuevo frente a una línea base congelada" que hoy contiene
  19 FAIL y 84 WARN conocidos y explicados (ADR-42, `gobernanza §4`).
- **Escrito con asistencia de IA, bajo decisión humana:** ver AUTHORSHIP.md.
- **Cómo citar sin tergiversar:** por commit y nombre estable de artefacto
  (CITATION.cff). Ninguna regla del modelo se cita sin su tier y su marca
  de procedencia (`modelo §9`).
- Parte del corpus (6 de 31 reports) conserva el idioma inglés de su
  corrida original.
```

**5 · CITATION.cff.** Previene: citas que atribuyan al programa versiones o afirmaciones que no son suyas. Borrador literal:

```yaml
cff-version: 1.2.0
message: >-
  Cite este repositorio por commit y por nombre estable del artefacto
  (p. ej. "modelo §3.7, commit c3adff8"), nunca por "el repo" sin versión:
  el contenido cambia a diario y los tiers de evidencia son parte de la
  afirmación. Citar una regla sin su tier tergiversa la fuente.
title: "Psicología del Mexicano Contemporáneo — corpus, modelo de decisión y aparato de falsación"
type: dataset
authors:
  - family-names: "REPORTA EL VALOR"
    given-names: "Jonas"
notes: >-
  Producido con asistencia de modelos de lenguaje (Claude, Anthropic) bajo
  dirección y verificación humanas; ver AUTHORSHIP.md. El modelo NO es un
  artefacto validado: ver el aviso de alcance en README.md.
repository-code: "https://github.com/josanoforo/modelado-mexicano"
license: CC-BY-NC-4.0
date-released: "2026-07-30"
```

**6 · ADR-44 (para `gobernanza`, sella otra sesión).** Previene: que el mayor cambio de función del programa quede sin registro, contra ADR-42(1). Borrador:

```markdown
**ADR-44 · El repositorio es público; la función del programa pasa de
privado-descriptivo a público-auditable.** El repo quedó público el
29/jul/2026 sin registro de decisión — mismo patrón que ADR-42(1): cambio
de semántica sin gobernanza. Este ADR lo registra y fija sus requisitos de
salida: (a) LICENSE + LICENSE-CORPUS + AUTHORSHIP.md + CITATION.cff +
aviso de alcance en README existen en el árbol; (b) por regla v2.2, toda
deuda "asumida a propósito" queda re-examinada a esta fecha (dictamen en
revision-publicacion-2026-07-30.md); (c) el README no contiene ninguna
cifra de estado no vigilada por test (T-README); (d) ninguna decisión de
mesa futura asume lector interno. → Estado: propuesto.
```

---

## FASE 6 · Pre-mortem — 18 meses después, salió mal

**1 · El descubrimiento (reputacional, el más probable).** Sep/2026: un investigador tuitea capturas: `README:40` falso contra el propio registro de veredictos + `git log` con Claude como autor + «144 números, 74 inventados». El hilo se titula «pseudociencia generada por IA sobre "el mexicano"». El aparato —que habría sido la respuesta— queda contaminado como coartada. *Evitable hasta:* el día en que alguien lo vea antes de que esté corregido. *Señal que lo delataba:* este documento. Probabilidad Alta si no se remedia esta semana; el costo de remediación es de horas.

**2 · El manual de campaña (daño a terceros, no al autor).** Feb/2027, precampañas: una consultora electoral opera R7.6 al revés — fabrica percepción de monitoreo del voto en municipios focalizados, citando internamente «evidencia académica» del repo. Votantes de perfiles 2-3 pierden autonomía efectiva. Nadie viola ninguna licencia: usaron el mecanismo, no el texto. *Evitable hasta:* nunca del todo — el conocimiento ya es público en la literatura fuente; lo único controlable era que el repo lo sirviera *sin* el aviso que hace citable la mala fe. *Señal:* tráfico y forks anómalos sin issues ni contacto.

**3 · El Patreon devora al registro (daño causado por el Patreon).** Mediados de 2027: 140 mecenas, cadencia mensual prometida de «hallazgos». Dos meses secos (veredictos `D`, un dato que no llega). La sesión de octubre estira un umbral *después* de ver el resultado para que un falsador «salga». Un mecenas con ojo —de esos que pagan precisamente por el rigor— cruza el diff contra el pre-registro y lo publica. El programa pierde lo único que vendía. *Evitable hasta:* el diseño de la promesa (cadencia de proceso vs. cadencia de hallazgos). *Señal:* la primera vez que una fecha de publicación aparezca en una discusión sobre un umbral.

**4 · La cita zombi (daño a terceros por vía académica).** 2027: una tesis o una nota de política pública cita «49 reglas del comportamiento del mexicano (GitHub, consultado mayo 2027)» sin tiers ni procedencia, y de ahí salta a un documento de diseño de programa social. Las reglas ASIGNADAS se vuelven «evidencia» por lavado de cita. *Evitable hasta:* la publicación de CITATION.cff y del aviso de cita con tier. *Señal:* la primera cita externa — buscarlas activamente cada mes, no esperarlas.

**5 · El abandono verde (daño difuso).** 2028: el programa se detuvo (fatiga; rama x). El repo queda arriba, CI verde para siempre (nada nuevo contra un baseline congelado en 2026), badge incluido. Lectores nuevos leen el verde como salud y el silencio como estabilidad. El artefacto miente por inercia estructural, no por acto. *Evitable hasta:* hoy, con una línea en el aviso (qué significa el verde) y una decisión de cierre digno pre-escrita (qué se archiva si el programa para — un «ADR de hibernación» que puede redactarse en 10 líneas cuando toque). *Señal:* tres meses sin commit con issues abiertos.

---

## FASE 7 · Escenarios de remediación

**A · Remediar en caliente (dejarlo arriba, parchar por gravedad).** Qué: los 6 artefactos de Fase 5 + fix de README:40 + cola.yaml, en 1-2 sesiones. Coste: horas. Exposición residual: la ventana entre hoy y el merge (días). Señal pública: un observador que ya lo haya visto verá el diff — y en *este* programa, un diff que corrige la portada con nota fechada es coherencia, no vergüenza: es literalmente el método aplicado a sí mismo. **Recomendado.**

**B · Repliegue parcial.** No hay candidatos: la Fase 4 no encontró ningún artefacto cuyo retiro reduzca riesgo real (todo lo clonable ya se clonó [S1]; lo único retirable con ganancia es una ruta de máquina, que se edita, no se retira). Retirar los YAML de MILPA o capar el modelo emitiría señal de ocultamiento sin recuperar nada. **Descartado con nombre.**

**C · Repliegue total y relanzamiento.** ¿Es posible? Mecánicamente sí (Settings → private). Epistémicamente no: los clones existen [S1], la historia con sus 21 commits de Claude ya fue observable, y el relanzamiento «limpio» sería indistinguible de una edición de imagen — en un programa cuya moneda es no editar la imagen. Además rompería los enlaces del único día de exposición. Coste: alto; ganancia: cero verificable. **Descartado.**

**Decisiones que se encarecen por día:** disclosure de IA (cada día aumenta la probabilidad de que otro lo narre primero — es la única con reloj real); fix de README:40 (mismo reloj); licencia (cada visitante que llega y no puede reutilizar es un lector legítimo perdido, y los clones sin licencia quedan en limbo legal permanente). **Decisiones que ya no se pueden tomar:** anonimato o seudónimo (consumada); retirar del conocimiento público cualquier contenido del árbol al 30/jul (consumada); reescribir la historia de autoría (prohibida por ADR-41, correctamente — sería falsificar procedencia).

---

## FASE 8 · Priorización y plan

Orden por (impacto × irreversibilidad) / coste:

**Hoy, mientras está expuesto:**
1. Fix `README:40` (+ retirar el presente de T03/T10 o fecharlos). Criterio derivable: la línea cita el bloque `## Registro de veredictos archivados` y su conteo coincide con `grep -c` sobre ese bloque.
2. `AUTHORSHIP.md` (borrador arriba). Criterio: existe y README lo enlaza.
3. `LICENSE` + `LICENSE-CORPUS.md`. Criterio: `ls` los encuentra; GitHub muestra licencia.
4. Aviso de alcance en README (borrador arriba).
5. `cola.yaml:83` anonimizada con nota.
6. `CITATION.cff`.
7. ADR-44 propuesto a sesión de canon.
   Verificación global del lote: `python3 tests/check.py --baseline` VERDE sin FAIL nuevos.

**Antes de abrir el Patreon (2–4 semanas):**
8. T-README en la suite (molde T16). Criterio: test presente y en verde; prueba negativa incluida (ADR-40.c).
9. Resolver cola D-01 por ADR y escribir las fichas R3.1 y R3.4. Criterio derivable: `grep -c "^## R[0-9]" forense/hitoD-preregistro-v2_0.md` = 27 y el FAIL T17 desaparece de la corrida completa (no solo del baseline).
10. ADR sobre las 8 refutaciones sin objeto (declarar alcance y retirarlas, o ampliar — decidir, no aplazar). Criterio: la batería no contiene refutaciones sin objeto sin ADR que las gobierne.
11. CAL-G3 ejecutada si los términos de ENNViH lo permiten (**reporta el valor**). Criterio: `procedencia.yaml` registra el primer coeficiente de generador con clase MEDIDO, derivado del archivo.
12. Declarar semántica del verde en README (línea del aviso) + job informativo de suite completa en CI.
13. Auditoría externa invitada (2-3 lectores hostiles de buena fe), veredictos al pre-registro.

**Se declara como limitación conocida y se publica igual:** 74 ASIGNADOS y 0 coeficientes medidos; sesgo de clase; ADR-10; los 19 FAIL · 84 WARN congelados; los 7 reports sin mapa y los 8 con (c) sin marca; el corpus mixto ES/EN. Todo ya está declarado dentro; el trabajo es moverlo a la portada, no producirlo.

**Se retiene indefinidamente:** nada del árbol actual (Fase 4); `data/raw/` sigue fuera por diseño; y toda salida futura de MILPA queda detrás del gate de ADR-37 — eso ya está decidido, solo se reafirma.

**Semana 8 (puerta de decisión):** con 1–13 en verde → abrir Patreon (forma de la rama v). Si 9 o 10 siguen abiertos → no abrir: serían las dos deudas caducadas de la tabla eje cobrándose con intereses delante de clientes.

---

## FASE 9 · Cierre

**Las 5 preguntas que cambiarían el diagnóstico:**
1. ¿Desde cuándo exactamente es público el repo y cuántos clones/forks hubo? (GitHub Insights — cambia la urgencia real de todo lo anterior.)
2. ¿La meta dominante es citabilidad académica o programa personal con audiencia? (Decide BY vs BY-NC y cuánto pesa la auditoría externa.)
3. ¿Cuántas horas semanales sostenibles hay de verdad? (Decide cadencia, Patreon entero, y la regla de medianoche.)
4. ¿Está el autor dispuesto a que el disclosure de IA sea lo segundo que lea todo visitante? Si la respuesta es no, el repo no debe estar público — todo lo demás es secundario a esto.
5. ¿MILPA se va a construir en los próximos 12 meses o es aspiracional? (Decide si la spec es promesa fechada o se re-etiqueta como diseño de archivo.)

**Veredicto en 5 líneas.** El repo se queda arriba: no hay nada retirable que reduzca riesgo y el repliegue emitiría la única señal peor que los defectos. El activo publicable es el aparato de falsación con su registro de errores; el modelo es su banco de pruebas, y la portada debe decirlo. Las urgencias reales son dos y se arreglan en horas: la portada que hoy contradice la tesis del programa (README:40) y el disclosure de IA que el git log ya hizo público sin marco. La licencia es dual (MIT + CC BY-NC 4.0 con NOTICE anti-scoring declarativo, sabiendo que su fuerza es normativa). El Patreon solo funciona vendiendo el proceso —veredictos honestos, gane o pierda— y se abre cuando T-README esté verde, el pre-registro diga la verdad sobre sí mismo, y exista el primer coeficiente MEDIDO.

**Lo que un asesor complaciente no habría dicho:**
- El modelo probablemente nunca será el producto. La única medición primaria que existe (R3.2) encontró tus números 4x–34x fuera de escala — y esa historia, bien contada, vale más que las 49 reglas juntas.
- Tu portada comete hoy el defecto exacto que tu programa existe para hacer imposible, y lleva un día siendo pública. Antes de cualquier estrategia, eso.
- El título del programa viola tu propio Bloque A. Un auditor lo pondrá de epígrafe. Ten la respuesta escrita antes (la tienes: §0.2 — pero está en la página 2, no en el título).
- Las reglas de clientelismo son dual-use y las publicaste sin aviso: documentaste el mecanismo que hace eficaz la compra de voto. Nombrarlo en el NOTICE no lo neutraliza, pero deja constancia de qué lado estás — y hoy no hay constancia.
- El encargo que comisionó esta revisión traía dos premisas falsas (H3 tal como estaba escrita, H5 en su literalidad) pese a declararse verificado contra HEAD. La regla de ADR-39 aplicó también contra ti.

---

## MÓDULO DE AUDITORÍA (Bloque A, sobre este artefacto)

1. **¿Confunde pobreza/desigualdad/violencia con cultura?** El análisis de mal uso (rama iii) trata a los segmentos como *víctimas potenciales de operaciones estructurales* (cobranza, clientelismo), no como portadores de rasgos — consistente con el corpus. Riesgo residual: la lista de abusos podría leerse como catálogo de vulnerabilidades «de los pobres»; el mecanismo citado es siempre estructural (observabilidad del voto, CAT, acceso).
2. **¿Sobregeneraliza desde clase media urbana?** Sí, en un punto: el «lector externo» que modelo en las Fases 1 y 4 es académico/técnico urbano. El lector Patreon plausible puede ser otro público, con otra lectura de los forenses. SUPUESTO no verificable hasta que exista audiencia.
3. **¿Sesgo por marcos extranjeros?** Sí, declarado: el análisis de licencias y ejecutabilidad (rama i) razona desde doctrina angloamericana de copyright. La LFDA mexicana (derechos morales irrenunciables, régimen de cita distinto) puede mover detalles. INFERENCIA, confianza Media; verificar con abogado mexicano antes de sellar las licencias.
4. **¿Qué cambiaría con foco rural/indígena/popular?** El pre-mortem 2 y 4 pesan más: los segmentos peor medidos por el modelo son los que un uso operativo dañaría más y los que menos capacidad tienen de replicar al repo. Refuerza la recomendación del NOTICE, no la cambia.
5. **¿Qué parece psicológico y es incentivo?** El conflicto Patreon se trató íntegro como estructura de incentivos, nunca como carácter del autor. El diseño «cadencia de proceso» es la corrección del incentivo, no una exhortación a la virtud.
6. **¿Evidencia débil, intuición fuerte?** Las estimaciones de probabilidad del pre-mortem y las «facilidades» de mal uso (rama iii) son juicio sin base actuarial — están marcadas por su lenguaje (Alta/Media), no derivadas. Igual que los umbrales de ADR-37: asignadas y dichas.
7. **¿Conclusión peligrosa si se usa simplista?** Dos: «los forenses son un activo» sin su condición (la portada enmarca primero) invita a exhibir vulnerabilidad sin marco; y «NC se puede relajar después» sin su segunda mitad (BY no se puede revertir para copias ya licenciadas) invita a un default permisivo irreversible.
8. **¿Qué afirmación mía sobre el estado del corpus no fue derivada?** Derivé en sesión: conteo de archivos, reports, forenses (23 con subdirectorios), suite 19·84, baseline head, registro de veredictos, fichas (25), autores de commits (21/12/4), cifras de README contra `modelo §6/§7`, presencia/ausencia de LICENSE/CITATION/CoC, versión de instrucciones, `milpa-plan:128`, `whitepaper §7.3`, `cola.yaml:83`. **No derivadas, marcadas donde se usan:** visibilidad pública y su fecha ([S1], del encargo — **reporta el valor**); existencia de protecciones de rama (**reporta el valor**); tags/releases (**reporta el valor**); términos de ENNViH (**reporta el valor**); conteo de clones/forks (**reporta el valor**); que los 6 reports con título en inglés tengan *cuerpo* en inglés (INFERENCIA por título, no leídos íntegros).
9. **(v2.2) ¿Qué deuda asumida caducó aquí porque cambió la función?** Tres, dictaminadas en la tabla eje: el baseline con la autodeclaración falsa congelada «por decisión de mesa» (fila 6 — una mesa que ya no es privada), la semántica interna del verde de CI (fila 6/rama ix), y las 8 refutaciones sin objeto (fila 5). Y una del propio encargo: su método de verificación de H5 (grep sobre README/CONTRIBUTING/canon) heredó un perímetro nunca medido — no incluyó `git log` ni leyó ADR-41, y por eso afirmó un «cero menciones» falso. La restricción del instrumento le dio forma a la conclusión, el patrón exacto que v2.2 cataloga.

**Pregunta específica del encargo — ¿dónde traté la publicación como decisión futura?** Revisado contra el texto: las formulaciones «elegir licencia», «antes de abrir el Patreon» y «auditoría invitada» refieren a decisiones genuinamente futuras, no a la publicación. La Fase 7 evalúa repliegue como remediación de un hecho consumado, no como alternativa a publicar. No encontré tratamiento de la publicación como pendiente; si algún lector lo encuentra, es defecto de este artefacto y se corrige con nota fechada.
---

## Nota de reconciliación — 30/jul/2026, antes del merge

La FASE 5 de este documento propone un artefacto, `LICENSE-CORPUS.md`, que
**no se creará**. La decisión `D-05` se cerró el 30/jul manteniendo un
`LICENSE` dual único (MIT + CC BY-NC-SA 4.0), ya en `main`. Toda mención a
`LICENSE-CORPUS.md` en este documento se lee como propuesta descartada, no
como referencia a un archivo del repositorio.

De la FASE 5 se adopta únicamente el argumento del NOTICE anti-scoring, que
se integra a `USO-ACEPTABLE.md`. Reconciliación completa en el Eje F del
plan maestro.

Nota escrita antes del sello: el documento aún no había entrado al canon, así
que editarlo aquí no viola append-only. A partir del merge, no se edita.
