# Instrucciones del proyecto — "Psicología del Mexicano Contemporáneo" · v2.14 · VERSIÓN OPERATIVA

Este texto es normativo y es el que viaja en el proyecto y en el repo (A.9). La historia de cada regla —el defecto que la motivó, con fecha, PR y hallazgo— vive íntegra en `instrucciones-proyecto-v2_14-HISTORIA.md` (repo) y no se repite aquí. Los rótulos (A.N, A-bis N, D-N, E.N) son los mismos en los dos cuerpos.

## 0 · Mandato de dirección

Antes de declarar cualquier decisión pendiente, **revisa el repo**: contexto, decisiones anteriores relacionadas, dependencias, qué desbloquea. Preséntala en lenguaje de Recursos Humanos para que mesa decida fácil. Hemos perdido tiempo por asegurar que algo existe o no existe sin revisar el repo a detalle.

## 1 · Regla de señal (manda sobre todas las demás cuando chocan)

- **Cada sesión produce una medición, o produce nada.** Un contador que no se mueve es el único síntoma que no admite interpretación. Desde v2.14, una medición sin fila en la vista no cuenta como producida hasta que se registre (E.7).
- Defecto que no impide medir → una línea en `forense/hallazgos.md` y sigue. Defecto que sí impide medir → PARO y se reporta.
- **El aparato tiene costo.** Toda regla, test o módulo nuevo declara qué defecto real ya ocurrido atrapa y qué le habría costado a un lector. Si no le habría costado nada a un lector, se anota y no se instrumenta. Verificar tiene precio; la auditoría de la auditoría no lo vale nunca.
- Los encargos salen de la **demanda** (`corrida0.py demanda`), no de la cola de deuda.

## 2 · Procedencia (nada se recuerda: se lee, se deriva, se cita)

- **Regla de oro.** Tiers, hallazgos y cifras se leen del repo, no se reconstruyen de memoria.
- **Tres tipos de lectura (v2.1).** (1) leída del repo en esta sesión con commit citable — la única que entra al canon; (2) leída de un espejo del proyecto; (3) reportada por otra sesión. (2) y (3) se formulan como pregunta a verificar, nunca como hecho. **Ninguna cifra sale del espejo, nunca**: se clona el repo.
- **Ninguna cifra esperada se teclea.** Se deriva en la sesión o se cita con archivo y línea. Un criterio de parada con una constante a mano es el defecto que el criterio existe para atrapar. **La receta también se verifica**: prueba el comando contra un caso conocido o reporta el valor crudo con el comando.
- **Verificación de premisas.** Todo encargo declara la procedencia de sus premisas; quien ejecuta las verifica antes de obedecer. Si una premisa no se sostiene, PARA y reporta — no ajusta el texto para que cuadre. Encontrar un encargo mal fundado es entregable.
- **Verificación de la restricción antes del diseño.** Una restricción supuesta se hereda como una cifra supuesta, y peor: parece el terreno. Se mide antes de diseñar alrededor.
- **Tres hallazgos distintos que nunca se colapsan:** "no pude alcanzar la fuente" · "la fuente no tiene el dato" · "nadie corrió el mecanismo contra esta fuente".

## 3 · Reglas sobre México (aplican a todo artefacto que afirme algo sobre México)

- No trates a los mexicanos como bloque homogéneo: segmenta por región, clase, edad, género, escolaridad, urbanización, religiosidad, migración, exposición global. El sesgo que más muerde es de clase dentro de la modernidad (sobre-muestreo del clasemediero urbano formal). El sistema indígena-comunal vivo es otro orden institucional: fuera por diseño; la huella indígena difusa sí se mapea.
- Distingue siempre psicología individual, scripts culturales, adaptación racional, estructura económica e instituciones. **No confundas desigualdad, violencia, informalidad o precariedad con cultura.** No romantices ni patologices.
- Separa evidencia fuerte / media / hipótesis razonable / narrativa popular. No conviertas intuiciones en hechos; si no hay evidencia para una sección, dilo y no la rellenes.
- Marcos importados (Hofstede, GLOBE, WVS, honor/dignidad/face) **con crítica**: ni ingenuamente ni por reflejo. El anti-esencialismo también sobre-corrige.
- **Procedencia de la evidencia, tres clases etiquetadas siempre:** (a) datos primarios en México; (b) muestras mexicano-americanas / diáspora (no son evidencia sobre México: simpatía, machismo/caballerismo, marianismo suelen ser (b)); (c) marcos teóricos importados.
- **Firewall genético.** Prohibida la inferencia ascendencia → conducta de grupo. Solo canal individual, molecular, de efecto pequeño (alcohol, nicotina), nunca como segmentación.
- **Falsabilidad.** Para cada patrón fuerte, qué evidencia lo cambiaría. "Adaptación racional" no es infalsable: acótala con tamaños de efecto.
- Todo en español.

## 4 · Medición propia (A-bis)

1. **Co-observación no es identificación.** Un β̂ sin condicionamiento es una asociación y se rotula así.
2. **Condicionado tampoco es correcto.** Un condicionamiento discordante solo establece que el marginal no es robusto.
3. **Toda cantidad entra con su escala declarada y no se compara contra otra escala** sin función de enlace. Comparable sin enlace: signo y razón entre coeficientes del mismo generador en la misma corrida.
4. **Un estimando restringido a una subpoblación no se compara contra uno poblacional.** Se recalcula al mismo universo o se declara acotado.
5. **El estimador es de la celda.** Ningún cómputo global (la matriz hoy, cualquiera mañana) es estimador por defecto de una celda que no lo adjudicó bajo el contrato celda-D (ADR-68). La matriz compone (ADR-91/ADR-531) y compite como candidato.
6. **Un piso no vencido es el estimador adjudicado de su celda y se adopta salvo veto de mesa** (firma 17/sep/2026). Pisos: en cruces, marginales públicos de la misma ola sin interacción; en marginales, la ola anterior por eje. Un piso no identifica nada: acota a los retadores. Los retadores son credencial para emitir donde no hay piso.
- Un punto que satisface un umbral con un IC que no lo despeja **no adjudica**: propuesta con reserva.

## 5 · Estructura de artefactos

- **Report temático (Bloque B):** resumen ejecutivo (10–15 hallazgos, marcando sólidos, malinterpretados y útiles) · marco conceptual · mapa de evidencia por tier · patrones (descripción, a favor, en contra, segmentos, causas, riesgo de mala lectura, implicaciones) · causas (cultura vs estructura vs adaptación) · segmentación explícita · comparación internacional (distintivamente mexicano / latinoamericano / desigual-baja confianza / malinterpretado desde marcos anglosajones) · implicaciones aplicadas · mitos · síntesis (top patrones, contradicciones, errores, oportunidades) · si alimenta el modelo, reglas SI-ENTONCES: SI [segmento] ENTONCES [conducta] — PORQUE [driver] — [TIER], con disparadores de contexto.
- **Integrador, modelo de decisión y validaciones forenses** usan estructura propia + §3 + módulo de auditoría. No se fuerzan las secciones de B.
- **Pre-registro de falsación (B-bis).** Toda escala declara qué pasa si el falsador NO refuta (corroborada / acotada / falsador débil), antes de ver el dato. Si dos filas pueden satisfacerse a la vez, se declara cuál manda, al sellar.
- **Validación forense (Bloque C).** Anti-confusión (aísla lo psicológico de capital, logística, precio, regulación, timing, suerte; si no se aísla: CONFUNDIDO) · anti-post-hoc (DECLARADO / INFERIDO / RETROSPECTIVO) · anti-superviviente (pares contrafactuales). Métricas AUDITADA o AUTO-REPORTADA. Entregable: qué reglas CONFIRMA / MATIZA / ROMPE.
- **Módulo de auditoría de rigor extremo — solo en artefactos que afirman algo sobre México** (reports, integrador, modelo, forenses; no en notas, registros, encargos). Preguntas: ¿pobreza/violencia/informalidad confundidas con cultura? ¿sobregeneralización desde clase media urbana? ¿sesgo de marcos o muestras estadounidenses/europeas? ¿qué cambia con foco rural/indígena/popular? ¿qué parece psicológico y es incentivo racional? ¿dónde hay evidencia débil e intuición fuerte? ¿qué sería peligroso leído simplista? [v2.1] ¿qué afirmación sobre el estado del corpus fue escrita a mano y no derivada? [v2.2] ¿qué deuda "asumida a propósito" caducó al cambiar la función del programa? [v2.3] ¿cuántos contadores movió este trabajo? (si cero, dilo en una línea al inicio) [v2.4] ¿en qué escala está cada cantidad y contra qué se compara?

## 6 · Aparato de actos (Bloque D)

**ARRANQUE (lo ejecuta la skill `/acto`; no se transcribe en el encargo; si falta, se pide):**
1. REPO: localiza el clon existente; no clones salvo que no haya; reporta ruta · `git log -1` · `git status`. No arranques desde el home.
2. SHA: compara con el que el encargo declara; si main se movió no es PARO: refresca, re-deriva, reporta.
3. `data/raw` AUSENTE NO ES PARO: se crea o enlaza. Si el acto descarga, verifica al cerrar que los payloads quedaron en el corpus compartido (defecto PR #77).
4. ENTORNO: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` + sonda `curl` a inegi (nunca `-I`) + `ls data/raw | head -1` (tres partes, A.2). Todo veredicto negativo declara cuántos archivos examinó (A.13).
5. ESPEJO: prohibido derivar cifras del espejo del proyecto.

**VERIFICACIÓN DE EXISTENCIA (la contesta quien escribe el encargo, con comandos):** (1) estructura — qué tablas gobiernan, derivado de `data/INFRAESTRUCTURA-v1_0.md`; si el índice no cubre el dominio, ese hueco es el entregable; (2) contenido — comando y salida que demuestran que lo pedido no existe ya, con vocabulario A.4; (3) cobertura retroactiva — fecha de nacimiento de la tabla vs fecha del trabajo. Si (2) o (3) revelan trabajo hecho, el encargo no se lanza.

**Cabecera obligatoria del encargo (formato corto, D-12):** SHA de redacción · ENTORNO asignado y el que NO · **una sola sesión** (D-17) · compuerta · MODELO SUGERIDO (D-13: Sonnet para recetas sin juicio; Opus para medidores y lotes; Fable para dirección y decisiones; se puede subir, nunca bajar en actos que miden) · firmas de mesa verbatim · verificación de existencia · spec congelable por pieza · PERÍMETRO Y CONCURRENCIA con la frase «si te encuentras escribiendo fuera de esta lista, PARA» · FP/ADR/NC candidatos (deriva al cierre, no heredes; renumera quien fusiona segundo) · CONTADOR (`cuenta_gen2 = SI … no adopta` si mide) · lo que NO hace · sucesores.

- **D-10.** `/acto` ejecuta: ARRANQUE, compuerta contra `origin/main` (si no se cumple, se niega con cero commits), 0-bis A.3, cascada de cierre (ADR, cabecera de gobernanza, recifrado L0, registro-rotulos, T25, `check.py --baseline` VERDE o PARO), cierre anti-PR#77, `## NO-CORRIDO / RESERVAS`, `## CONSUMIDO`.
- **D-11.** Lotes: hasta cuatro piezas afines del mismo entorno = un encargo, un PR, un ADR. Una pieza que PARA no tumba el lote, salvo PARO de entorno.
- **D-14.** Gate para automatizar: ¿qué defecto real ya observado evita? ¿puede cambiar una medición o decisión? ¿cuesta menos que corregirlo? Un "no" → no se automatiza. No se construye base central, servidor de provenance, motor de workflows, DAG engine ni ADR por subcomando trivial.
- **D-15.** Spec en dos capas: humana (`forense/prereg-caja/*-spec-v*.md` con sidecar) + `spec.yaml` (contrato ejecutable normativo; `NO-APLICA` es un valor). Ningún parámetro vive en dos sitios.
- **D-16.** La suite adjudica por FAIL; los WARN nuevos se listan como estado y no adjudican; ninguna cabecera aserta totales de WARN.
- **D-17.** ENTORNO ASIGNADO no identifica una sesión: el encargo nombra sesión o rama; `/acto` PARA si el encargo ya está archivado en otra rama viva.
- **Actos que producen una estimación: dos commits mínimo** — el primero congela la spec antes de abrir dato ("el primer resultado que produzca este procedimiento es el que se reporta"); el segundo trae resultados y no edita el primero. Con reserva de evaluación: tres (E.6).

## 7 · Reglas A (cada una con falsador a tres meses)

- **A.1** Tres estados de verificación de hash que nunca se colapsan: AUSENTE · raíz-no-configurada · hash-discordante; salida cruda pegada.
- **A.2** La firma de entorno tiene tres partes (variable, sonda, corpus montado). Todo acto que abra microdato va a caja.
- **A.3** Los encargos vivos viven en el repo: se archivan verbatim antes o con su lanzamiento (0-bis) y se marcan CONSUMIDO con su PR. Un encargo que cita un archivo inexistente está mal escrito: el texto va inline o no se lanza. Todo adjunto viaja con sha256.
- **A.4** Ninguna clasificación negativa sin universo declarado (qué, con qué mecanismo, cuándo). Vocabulario: EXISTE-SATISFACE · EXISTE-NO-SATISFACE · NO-ENCONTRADO (dónde, con qué términos) · NO-ACCESIBLE. Prohibido "no existe".
- **A.5** El fallo de un agente es un hecho sobre el agente: "NO OBTENIDO POR ESTE AGENTE EN N INTENTOS" + receta manual de un minuto. Prohibido concluir sobre un portal desde memoria.
- **A.6** Encontrado por búsqueda no es verificado: `SIN-FETCH` hasta que un acto lo abra. Se reabre lo que hoy gatea una ficha, no el corpus en bloque; la razón que se reabre es la informacional (negativo explícito, tier bajo por falta de información, reserva sin corroborar).
- **A.7** La identidad de un artefacto es su contenido: dos hashes (crudo y con tokens neutralizados); el PARO se evalúa contra el segundo.
- **A.8** Ningún encargo se escribe sin verificar qué ya existe: estructura, contenido y cobertura retroactiva (§6).
- **A.9** Una versión de instrucciones no está sellada hasta que está en los dos lados (proyecto y repo), y el ADR lo declara con la fecha del pegado.
- **A.10** Todo sello porta su universo (SHA, corpus, denominador); un sello cuyo universo creció queda VENCIDO EN ALCANCE — no refutado, no borrado, no vigente para el territorio nuevo. Se reactiva por re-sello, nunca editando el viejo. Una conclusión no puede ser más ancha que su universo.
- **A.12** El tablero de firmas se deriva, no se recuerda: toda ranura o pendiente de mesa añade su fila a `forense/firmas-pendientes.tsv` en el mismo commit; toda firma dada se marca FIRMADA con su ADR/PR.
- **A.13** Un negativo producido por un comando que no examinó archivos no es un negativo: se declara el conteo de archivos.
- **A.14** Lo que no se corrió se asienta: `## NO-CORRIDO / RESERVAS` antes de `## CONSUMIDO` ("Ninguno." es obligatorio), con razón (PARO-ENTORNO · PARO-PREMISA · FUERA-DE-PERÍMETRO · SUSTITUIDO-POR · DIFERIDO-A · NO-VERIFICABLE-AQUÍ · DECISIÓN-DE-MESA-PENDIENTE), impacto y sucesor; filas NC en `forense/no-corrido.tsv`. **Política de cero ramas:** un acto termina con su rama fusionada o borrada.
- **A.15** Ningún negativo sobre existencia de variable sin consultar el inventario por instrumento completo, con patrón y conteo; specs en nube listan secciones leídas del índice; **los mapas de códigos se verifican por archivo y por texto de pregunta, no por nombre de variable** (`hs02g`, `P5_6`/`P5_7`).
- **A.16** El marcador de estado vive en el campo (token por prefijo), no en la prosa.
- **A.17** Un bloqueador citado por nombre se re-verifica de **estado** antes de heredarlo: leer la fila de `<id>` y comprobar que sigue ABIERTA.
- (A.11 libre; rótulos disputados y series ajenas —`ref.A.N` de refutaciones— en `canon/registro-rotulos.tsv`.)

## 8 · Generaciones numéricas (Bloque E)

- **E.1** GEN1 es historia, no autoridad: no se reescribe ni es fuente de GEN2. Toda cifra declara su generación o se asume GEN1.
- **E.2** Ningún número entra a GEN2 sin cadena nacida con él: SPEC → CALC → INPUTS con hash → CÓDIGO FIJADO → ENTORNO → EJECUCIÓN → RESULT (tipo, unidad, tolerancia) → USO. Tres preguntas que no se colapsan: ¿se reproduce? ¿pasó validación independiente? ¿se adopta? — **la adopción es por merge de mesa, y por bloque:** el merge del PR que trae un bloque ES la adopción; un bloque no se degrada slot por slot.
- **E.3** Una corrida sellada es evidencia histórica: no se reescribe (`run` se niega; no existe `--force`); reejecutar es un CALC nuevo. `verify` responde en dos ejes: RESULTADO (REPRODUCE · NO-REPRODUCE · NO-EJECUTABLE, con tolerancia por tipo) y CONTEXTO (IDENTICO · DISTINTO · NO-VERIFICABLE); NO-VERIFICABLE no se degrada a NO-REPRODUCE.
- **E.4** Contador derivado, no reportado: `corrida0.py status` desde los TSV derivados. La máquina marca CANDIDATO-VENCIDO; solo el humano declara VENCIDO-EN-ALCANCE.
- **E.5** Los cálculos van después del aparato: seis checks del GO en `origin/main` antes de cualquier corrida real; códigos y ponderadores se resuelven desde codebook y se congelan en COMMIT-1 antes de cualquier microdato; adivinar códigos para un preflight verde está prohibido; ausencia de desenlace comparable → NO-CONSTRUIBLE, no veredicto.
- **E.6** Reserva de evaluación: se declara antes de derivarla; tres commits (spec sin microdato → emisiones selladas → R y adjudicación); el orden del diff es el sello; un R derivado antes del COMMIT-2 degrada el piloto a factibilidad y se declara; el único código autorizado a tocar la ola reservada se congela en COMMIT-1 con guardia de una sola variable de agrupación; nada en scratch; un cruce visto se declara consumido y no se relanza sobre él.
- **E.7** Toda corrida sellada entra a la vista en el mismo acto que la sella, o su CONTADOR dice "sellada en disco, no registrada"; ningún veredicto de replay se publica sin asiento en `forense/replay-evidencia.tsv`; una vista bloqueada se destraba asentando evidencia corrida por corrida en procesos aislados — nunca forzando ni excluyendo.

## 9 · Caducidad y sello

- Toda regla de proceso (A.3 en adelante, D-16, D-17, E.7(1)) caduca a los tres meses si no atrapa nada, y se anota. No caducan las de contenido (§3), las de medición (§4) ni E.1–E.3, E.6, E.7(2)-(3) mientras convivan generaciones. Cuando el defecto de una regla desaparece, su falsador se revisa entonces, no a los tres meses.
- **Sello de esta versión (A.9):** este cuerpo operativo se pega en el proyecto de Claude antes de lanzar `GEN2-V214`; mesa lo declara con fecha; el ADR cita esa línea verbatim, actualiza `instrucciones_vigentes` a v2.14 y archiva el cuerpo histórico como `instrucciones-proyecto-v2_14-HISTORIA.md`. Los dos cuerpos comparten rótulos; ante duda de sentido, manda el histórico y se corrige este.
