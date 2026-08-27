- **SHA de redacción:** `6d213a6` (declarado por dirección; `main` se movió a `e5a36ab` — PR #382, ACTO MAESTRA31-E1 · RELOJ-CRUCE — antes de que este acto arrancara; diferencia reportada en la nota de cierre, no bloquea)
- **Entorno asignado:** NUBE (`cloud_default`); NO Ubuntu
- **Estado:** CONSUMIDO — dirección interrumpió el paso 2 (transfer verbatim truncado a media frase) y el paso 3 (P1/P2/P4/P5/P6/P7 ya resueltos o vigentes en el árbol) tras verificación, y redirigió el acto a ejecutar solo el PASO 4. Ver nota de cierre.

---

ENCARGO E2 · REGISTRA-PENDIENTES — que los siete heredados dejen de vivir solo en un chat
Dirección (maestra-31), 26/ago/2026 · Redactado contra main = 6d213a6 (clon propio, no espejo). GATED: no arranca hasta que PR #381 (ACTO MAESTRA30-E9 · SCORING-V2) esté FUSIONADO — porque P1 del transfer se cierra con ese PR y este acto tiene que registrarlo cerrado, no abierto.
ENTORNO ASIGNADO: NUBE (cloud_default). NO lanzar en UBUNTU — ahí corre MAESTRA31-E1 y este acto no necesita el corpus: no abre microdato, no llama red, no descarga. Rótulo: ACTO MAESTRA31-E2 (D-6). El token pelado E2 colisiona (hay habitantes previos censados); se censa, no se reclama.
════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════
Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.
1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.
2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.
3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. Este acto no la usa — repórtalo y sigue.
4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: cloud_default Este acto no toca microdato ni red: dilo y salta la sonda, con la razón escrita. ⚠️ Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo de este acto declara cuántos archivos examinó el comando que lo produjo.
5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.
════════════════════════════════════════════════════════════════════
═══ VERIFICACIÓN DE EXISTENCIA — CONTESTADA por dirección (clon propio, 6d213a6, 26/ago/2026) ═══
1 · ESTRUCTURA — y aquí el índice sí falla, y cerrarlo es entregable de este acto.
grep -c "firmas-pendientes"    data/INFRAESTRUCTURA-v1_0.md  →  0
grep -c "cruce-oferta-demanda" data/INFRAESTRUCTURA-v1_0.md  →  0
grep -ci "transfer"            data/INFRAESTRUCTURA-v1_0.md  →  0
(A.13: 1 archivo examinado, 44 032 bytes)
El índice de infraestructura no lista el tablero de firmas, el TSV del cruce, ni la convención de transfers. Los tres existen y los tres se usan. La causa es derivable, no misteriosa: el índice nació 2026-08-24 23:56:48 (7848b97) y forense/firmas-pendientes.tsv nació 2026-08-25 00:06:21 (523306f) — diez minutos después, en otro commit. El índice describe el árbol que tenía enfrente. Regla de conducto (ADR-70(c)): el índice se actualiza cuando un acto descubre que le falta algo, y este es ese acto.
Gobernantes reales: forense/firmas-pendientes.tsv (A.12, 167 filas en main) · forense/encargos/convencion.md · el precedente de transfers commiteados, abajo.
2 · CONTENIDO — el entregable NO existe. Comando y salida cruda:
find . -path ./.git -prune -o -type f -iname "*TRANSFER*" -print
  → forense/TRANSFER-EMISOR-M-2026-08-20.md
  → forense/TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md
  → forense/historico/TRANSFER-maestra-7.md
  → forense/historico/TRANSFER-maestra-8.md
  → forense/historico/TRANSFER-maestra-9.md
  → forense/notas/2026-08-18-b2-transfer.md
(A.13: 2 152 archivos en el universo del find)
Resultado A.4: NO-ENCONTRADO — el transfer maestra-30 → maestra-31 no está en el repo. Los cinco anteriores sí: hay precedente y hay sitio. Y sus siete pendientes (P1–P7) no tienen fila de tablero:
grep -ic "SCORING-V2"    forense/firmas-pendientes.tsv  →  0
grep -ic "shortlist"     forense/firmas-pendientes.tsv  →  0
(A.13: 1 archivo examinado, 168 líneas)
Es exactamente el defecto de A.3: "de una batería de seis encargos rescatados el 5/ago, cinco ya se habían ejecutado por otras vías sin que nadie lo supiera." Aquí no son encargos sino decisiones de mesa, y A.12 dice lo mismo de ellas: el tablero se deriva, no se recuerda.
3 · COBERTURA RETROACTIVA. El tablero nació 25/ago 00:06; el transfer es del 26/ago. No hay brecha: nada de lo que este acto registra es anterior a la tabla que lo gobierna. El índice sí es anterior al tablero (10 min) — declarado arriba, y por eso su silencio no prueba que el tablero no exista.
⚠️ Si al ejecutar (2) o (3) revelan que el trabajo ya está hecho, total o parcialmente: el encargo NO se ejecuta como está. Se reescribe sobre el faltante real o se cancela, y se reporta. Descubrirlo ahí es el rendimiento de este bloque.
════════════════════════════════════════════════════════════════════
OBJETO
Que las decisiones de mesa heredadas sobrevivan a la conversación que las produjo. Tres entregables mecánicos y cero juicio nuevo: commitear el transfer verbatim, abrir fila de tablero por cada pendiente que hoy sea decisión de mesa sin resolver, y cerrar el hueco del índice de infraestructura.
Este acto no adjudica ninguno de los pendientes. Los hace visibles.
PASOS
0-bis · A.3. Commitea este encargo íntegro y verbatim en forense/encargos/2026-08-26-MAESTRA31-E2-REGISTRA-PENDIENTES.md antes de tocar nada. ## CONSUMIDO al cerrar, con el número de PR.
1 · Compuerta cero. PR #381 fusionado. Verifica por comando que FP-168 existe y que el ADR máximo es 209; si no, PARA.
2 · Commitea el transfer, verbatim. Archivo: forense/TRANSFER-2026-08-26-maestra-30-a-31.md. El texto íntegro va pegado inline al final de este encargo (A.3: si el texto que un encargo necesita no está en el repo, va inline o el encargo no se lanza). Única edición permitida: una cabecera de una línea que declare procedencia (adjunto de dirección, recibido 26/ago), su sha256, y que P1 ya cerró con PR #381. Precedente exacto: ADR-151, que commiteó un adjunto de mesa íntegro con una cabecera de una línea como única edición. No se corrige el cuerpo ni aunque contenga cifras que hoy sabemos rancias — se anotan en la nota de cierre, no se editan hacia atrás.
Dirección ya midió dos rancias y las declara aquí para que no las descubras como defecto tuyo: el §5 dice FP-157…166 cuando el máximo real en main era 167; y el §4·P3 dice «reloj ~8/sep» cuando el falsador es la fecha exacta 2026-09-08 con condición escrita. Ninguna se edita.
3 · Filas de tablero, derivadas y no supuestas (A.12). Para cada uno de P1–P7, verifica primero contra el árbol si sigue siendo una decisión de mesa sin resolver, y solo entonces abre fila. La clasificación que dirección propone —a confirmar o refutar por comando, no a obedecer—:
	pendiente	propuesta	por qué
P1	fusionar el PR de E9	NO abre fila	cerrado con PR #381; se anota en la nota de cierre
P2	lectura de mesa del marcador v1.1 (a/b/c)	abre fila	decisión de mesa, sin resolver, con opciones ya nombradas
P3	shortlist del cruce oferta↔demanda	abre fila	decisión de mesa con reloj; cita la fila FP-169 de E1, que corre en paralelo sobre el mismo falsador — no la dupliques
P4	R10.3, la 27ª — cierre ético	abre fila	decisión de mesa expresamente diferida; la fila la hace visible sin convocarla
P5	corredor E / operador ⊕	abre fila	⊕ está sellado (ADR-141); lo abierto es si mesa paga un re-sello. Verifica ese matiz antes de redactar la fila
P6	higiene permanente	NO abre fila	es política vigente, no decisión abierta — decláralo
P7	A.9 vivo (v2.11 pegada)	NO abre fila	es regla vigente, no decisión abierta — decláralo
Si tu verificación contradice cualquiera de las siete líneas, manda tu verificación: la premisa de dirección estaba mal fundada y eso es entregable.
Rango asignado: FP-170 en adelante. FP-169 es de MAESTRA31-E1, que corre en paralelo — no lo tomes.
4 · Cierra el hueco del índice. Añade a data/INFRAESTRUCTURA-v1_0.md las tres entradas ausentes, con el mismo formato de las filas existentes (quién la escribe / vía / esquema / quién la lee / trampa conocida): forense/firmas-pendientes.tsv · data/curacion-registro/cruce-oferta-demanda-v0_1.tsv · la convención de transfers de forense/ + forense/historico/. Regla de conducto ADR-70(c), citada. No hagas un barrido del índice completo — solo las tres que este acto descubrió que faltaban. Perseguir el resto es la jornada del 30/jul otra vez.
5 · Cierre. Nota forense/notas/2026-08-26-registra-pendientes-cierre.md con los conteos A.13 (filas abiertas, pendientes descartados con su razón, entradas de índice añadidas) · ADR (máximo re-derivado por conteo entero; candidatea máximo+1; renumera quien fusiona segundo) · recifrado §L0 de estado · censo del rótulo en canon/registro-rotulos.tsv y tests/check.py si T25 lo exige · python3 tests/check.py --baseline VERDE (🚫 jamás --freeze; espera WARN nuevos de T22 por cada fila ABIERTA — eso es el mecanismo funcionando, no un defecto) · PR.
RANURAS
Ninguna. Este acto no pide firma de mesa: registra decisiones que mesa ya declaró en el transfer y las hace derivables. Las filas nacen ABIERTA porque están abiertas, no porque este acto las abra.
PERÍMETRO Y CONCURRENCIA
Toca: forense/encargos/2026-08-26-MAESTRA31-E2-REGISTRA-PENDIENTES.md (nuevo) · forense/TRANSFER-2026-08-26-maestra-30-a-31.md (nuevo) · forense/notas/2026-08-26-registra-pendientes-cierre.md (nuevo) · forense/firmas-pendientes.tsv (FP-170+ solamente) · data/INFRAESTRUCTURA-v1_0.md (tres entradas nuevas, nada más) · canon/gobernanza-v1_15.md · canon/estado-programa-v1_10.md · canon/registro-rotulos.tsv · tests/check.py (solo _T25_ARCHIVOS_CONOCIDOS).
NO toca: forense/hitoD-preregistro-v2_0.md · forense/prereg-duelo-v2/** · el marcador · milpa/** · data/manifiesto.yaml · data/curacion-registro/cruce-oferta-demanda-v0_1.tsv · los cinco transfers ya commiteados · FP-169.
Concurrencia: MAESTRA31-E1 · RELOJ-CRUCE corre en UBUNTU en paralelo. Colisión posible solo en gobernanza / estado / registro-rotulos / tests/check.py. Rangos de tablero pre-asignados para evitarla. ADR: renumera quien fusiona segundo, con el máximo re-derivado contra el árbol ya fusionado, no por aritmética.
"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."
PROHIBIDO
Adjudicar cualquiera de los siete pendientes · editar el cuerpo del transfer (ni sus cifras rancias) · convocar R10.3 o rozarla de cualquier forma · abrir fila para P6/P7 sin declarar por qué la abriste contra la propuesta de dirección · hacer barrido del índice de infraestructura más allá de las tres entradas · tomar FP-169 · red, API, microdato · derivar cifra alguna del espejo.
CONTADOR
Filas de tablero abiertas, derivadas por verificación contra el árbol y no copiadas del transfer, más las tres entradas de índice. Hito D, tiers y llaves: sin movimiento, por diseño. Si al verificar resulta que menos de dos pendientes siguen abiertos, el contador es ese número y se dice: encontrar que el trabajo ya estaba hecho es entregable, no fracaso.
TEXTO VERBATIM A COMMITEAR (paso 2) — no editar, salvo la cabecera de una línea
(pegado inline conforme a A.3: el texto que este encargo necesita no está en el repo)

NOTA: el bloque de texto verbatim del transfer que dirección pegó a continuación de este encargo llegó truncado a media frase ("...el programa llamó a un mode") al final de §5/cierre — corte de contexto en la transcripción, no un artefacto del repo. No se completó, no se editó, no se commiteó como archivo separado: un documento "verbatim" con un final fabricado dejaría de ser verbatim. Dirección, consultada, ordenó PARAR ese paso; ver forense/notas/2026-08-26-registra-pendientes-cierre.md para la resolución completa (paso 2 y paso 3 cancelados por hallazgo, solo se ejecuta el paso 4).

```markdown
# TRANSFER · maestra-30 → maestra-31 — dirección, "Psicología del Mexicano Contemporáneo"
**26/ago/2026, cierre de jornada.** Todo lo de abajo está **derivado del repo en `main = 6d213a6`** con comandos en la sesión de maestra-30 (clase 1), no de memoria. Suite en main: **LÍNEA BASE VERDE**. Tablero: **0 ABIERTA**. Contador: **26 de 27 · 14D·4B·4A·2E·2C**. ADR máximo: **208**. Llaves de identificación: 5/5. Repo: `github.com/Josanoforo/Modelado-Mexicano`.
---
## §0 · Protocolo de arranque para maestra-31 (no negociable)
1. **Clona el repo y deriva de ahí.** El espejo del proyecto NO es fuente de cifras: medido en maestra-30, estaba 3+ versiones atrás con **129 archivos de la capa 25–26/ago ausentes** (control positivo: Hito D del espejo ≠ repo). Toda cifra con comando a la vista.
2. **Instrucciones vigentes: v2.11** (v2.10 + A.13), pegadas en el proyecto el 26/ago (A.9 cumplida). Si emites v2.12, se pega en el mismo acto que la sella.
3. **Sonda tu caja al abrir** (A.2, dos valores crudos): la caja de dirección de maestra-30 dio `inegi → 403 · github → 200` — no es UBUNTU; la tuya mídela, no la asumas.
4. **Rótulos D-6:** tus actos se declaran `ACTO MAESTRA31-E{n}`; los tokens pelados `E{n}` colisionan.
5. **Decisiones de mesa:** antes de declararlas pendientes, revisa el repo (contexto, decisiones previas, dependencias, qué desbloquean) y preséntalas en lenguaje RRHH — cabecera de las instrucciones del proyecto.
6. **Encargos:** formato Bloque D íntegro (ARRANQUE 5 puntos + VERIFICACIÓN DE EXISTENCIA contestada por quien escribe, verbatim), RANURAS de mesa llenas y como líneas propias, entorno asignado **y el que NO**, A.3 como paso 0-bis, ADR "renumera quien fusiona segundo" con máximo por conteo entero, contador por parser, dos-commits para toda estimación con la frase de sello, `command grep` en UBUNTU.
7. **CONTADOR de sesión de dirección: declárelo** (cero si no mide — maestra-30 cerró en cero directo, con las mediciones del día producidas por los actos).
## §1 · Lo que maestra-30 dejó FUSIONADO (PRs #371–#380, todos verificados en main)
| PR | Acto | Qué quedó |
|---|---|---|
| #371 | E2 · PREP-L-RUN | `lanzamiento-L-v1_0.md` (sha `37262417…`): hash-gate §0, driver §3, muralla §6 |
| #372 | E1 · CIERRA-FP157 | `R3.4 → B` archivado (:1186), enmienda Respaldo-2, FP-157 FIRMADA |
| #373 | E4 · DISEÑO-ENSAFI | ENSAFI **MAPEADO** (sección literal "VARIABLES DE DISEÑO ESTADÍSTICO" en la FD) |
| #374 | E3 · EJERCE-LLAVE-COMPARTAMOS | `EXP-COMPARTAMOS-1 → EJERCIDA_CORROBORA`: ITT **+1.1009 pp** [IC95 +0.6423, +1.5595], N=16,560, G=238; adopción +11.47 pp; llaves 5/5 |
| #375 | E5 · SELLA-FP164 | Octava clase del registro de llaves estrenada; FP-164 FIRMADA |
| #376 | CORRE-R10.1-v2 Fase B | κ pasó el gate con codificador humano (Jonatan); **`R10.1 → C`**; contador 25; ADR-205 |
| #377 | E6 · L-RUN | **Primera vez del programa en API**: 120 llamadas `L-solo` (claude-opus-4-6, temp 1.0, k=8, cero descartes), extractor congelado ANTES de aplicarse (103 con valor·17 null·118 citan fuente), **FP-165 FIRMADA** (no más API; L+corpus permanente no-ejecutado; corredor E inejecutable), ADR-206 |
| #378 | E7 · R-SCORING | **El primer marcador del programa** (`marcador-piloto-v1_0.md`, PILOTO SIN VEREDICTO), corridas-R (9 computadas + 6 con reserva pre-declarada, 0 SKIP), `_scoring-intento.json` (falla cerrada verbatim), FP-166 ABIERTA→, ADR-207 |
| #379 | E10 · R21-ADJUDICA | **`R2.1 → D`** bajo RANURA M-R21 (censo ADR-190 en cero EXISTE-SATISFACE, ≈112 resultados A.13); contador **26 de 27**; v1 techo intacto; reaperturas sembradas VENCIBLE EN ALCANCE |
| #380 | E8 · M-EMITE-Y-RESELLO | FP-166 **FIRMADA** caminos (ii)+(iv): `construir_crosswalk` reparado (encuesta + token exacto, con test), `crosswalk…v1_1.tsv` (v1_0 SUPERADO), **`enlace-M-v1_0.md` sellado con resultado honesto: 0 EMITE sobre las 15 sorteadas** (pasada sobre las 60 — leer el doc para el conteo total), enmienda **F1** del scoring (hash nuevo `63418cc8…`, fila `## F1 · enmienda 2026-08-26` en el prereg), enmienda §5 del lanzamiento, ADR-208 |
**Historia operativa del día que la nueva maestra debe conocer:** (a) la caja "UBUNTU" del corredor L resultó ser **Windows 11/Git Bash** — mesa la designó; el corpus vive en la caja UBUNTU real (`/home/pc0/…`); (b) una API key tocó el chat de Claude Code y se **quemó y rotó** en el acto — regla de la casa: *toda clave que toque cualquier chat queda quemada*; (c) `ANTHROPIC_API_KEY` en el entorno hizo que Claude Code mismo facturara a créditos de consola — se resolvió borrando la variable (User + bashrc) y `/login` por suscripción; (d) el SDK 1.1.0 retiró `temperature` de la firma → viajó por `extra_body`, probado en el cable con `999→400`.
## §2 · El marcador v1.0, en cuatro líneas (para no re-derivarlo mal)
9 de 15 celdas con árbitro R computable (6 con reserva pre-declarada: DIN-07/EMP-02/04/05 sin-microdato, DOC-06 sin-payload, TIC-06 spec-inconsistente). `L-solo` vs `R`: **1/9 en banda TOST y 1/9 en IC80 — solo CIV-08** (62.00% vs 61.88%±0.270, margen 0.015 pp, reportado con reserva); desviación mediana **14.40 pp**, máxima **57.95 pp** (TIC-08: 32.5% vs 90.45%). CV máx 11.73% → **0 SKIP**. Cuatro corredores vacíos con causa medida: L+corpus (FP-165) · M NO-EMITE×15 (bug de subcadena del crosswalk, ya reparado en #380, + enlace que dio 0 emitibles) · B SIN_BASELINE×15 (publicada=NO en las 9, rama 3 del corredor — diseño del sorteo) · E inejecutable (ADR-141 exige tres). El scoring **falló cerrado** («…se requiere exactamente 1 corredor L/corpus; hay 0») y por eso las casillas ADV1-M5 v2 fueron no-evaluables (s = skill contra B). Nota-al-margen ya detectada: el v1.0 cita FP-163 como "no firmada" — el tablero la tiene **FIRMADA** (ADR-199); v1.1 lo corrige.
## §3 · EN VUELO al momento del transfer: `E9 · SCORING-V2` (UBUNTU, gated a #380 — ya satisfecho)
Mesa lo lanzó; su A.3 debe aparecer como `forense/encargos/2026-08-26-E9-SCORING-V2.md`. Produce: `corridas-M/` (con enlace en 0-emite se esperan **15×NO-EMITE citando fila del enlace**, corrido dos veces idéntico), el scoring **arrancando de verdad** bajo el contrato F1, y **`marcador-piloto-v1_1.md`** (v1.0 intacto + cabecera SUPERADO; corrección de la cita FP-163; PILOTO SIN VEREDICTO verbatim).
**CHECKLIST DE REVISIÓN DEL PR DE E9 (para mesa, con maestra-31 verificando por comando):**
1. A.3 commiteado **antes** de ejecutar; rótulo `ACTO MAESTRA30-E9` (fue redactado en maestra-30) o `MAESTRA31` si relanzado — coherente en todos los archivos (T25/D-6).
2. **COMMIT-1 primero**: configuración congelada ANTES de correr, con `delta`/`nivel_ic`/`seed` **citados del prereg con línea** — si el prereg no los fija, el acto debió PARAR, no inventarlos. Frase de sello verbatim presente.
3. Scoring: si volvió a fallar la validación con el contrato F1, el PARO es correcto y el defecto es de E8 — no aceptar un rodeo.
4. Marcador v1.1: escalas declaradas (A-bis 3), IC/banda "como caen", comparación L↔M solo si M≥1 punto (hoy: no habrá), casillas `no evaluable` con causa (B ausente), **cero adjudicación** (D-i).
5. Sin fila de tablero nueva salvo hallazgo A.12 genuino; ADR candidatea **209** (renumera si algo se le adelantó); recifrado §L0; suite `--baseline` **VERDE**; nada corregido hacia atrás.
## §4 · PENDIENTES Y DECISIONES DE MESA (heredados explícitos — lo prometido en el último turno de maestra-30)
**P1 · Fusionar el PR de E9** con el checklist de §3. Es el único acto vivo.
**P2 · Lectura de mesa del marcador v1.1 — la decisión estratégica del duelo.** Con B ausente por diseño y M en 0-emite sobre las 15, ADV1-M5 v2 seguirá no-evaluable. Opciones a preparar cuando mesa pida (ninguna urgente; D-i vigente, el piloto NO adjudica): (a) aceptar el piloto como quedó y cerrar la fase con lectura de mesa; (b) re-especificar ADV1-M5 (v3) con casillas que no dependan de skill-vs-B — re-sello mayor; (c) leer en `enlace-M-v1_0.md` cuántas de las **60** emiten y decidir si vale un segundo sorteo condicionado a emitibles — **ojo: condicionar el sorteo a M cambia el estimando; es decisión de diseño de mesa, no de acto**. Maestra-31 arma el brief RRHH con los tres costos cuando se lo pidan.
**P3 · Shortlist del cruce oferta↔demanda — reloj ~8/sep.** Nota base: `forense/notas/2026-08-25-cruce-oferta-demanda.md` (verifica ahí el plazo exacto al abrir). Compromiso heredado de dirección: preparar la adjudicación (tabla de candidatos con evidencia, letra por candidato, RANURA) **cuando mesa lo pida** — no lanzarla sola.
**P4 · `R10.3` — la 27ª y última ficha: cierre ético deliberado del programa. NO SE TOCA** hasta que mesa convoque expresamente el acto de cierre. Ningún encargo debe rozarla.
**P5 · Corredor `E` / operador `⊕`:** re-sello declarado como *opción futura no ejercida* en FP-165. Solo se mueve si mesa lo pide; el contrato F1 ya lo dejó opcional.
**P6 · Higiene permanente:** no más llamadas API (FP-165, definitivo) · toda clave que toque un chat se quema y rota · el pack de conocimiento al proyecto es **subida selectiva por encargo** (decisión de mesa 26/ago; el know-how no se regala) · espejo jamás fuente de cifras.
**P7 · A.9 vivo:** v2.11 está pegada; cualquier versión nueva se pega en el mismo acto que la sella, con fecha declarada en el ADR.
## §5 · Referencias rápidas (paths, todos en main `6d213a6`)
Instrucciones: proyecto (v2.11) — Gobernanza: `canon/gobernanza-v1_15.md` (ADR-1…208) — Estado/mapa vivo: `canon/estado-programa-v1_10.md` §L0 — Tablero: `forense/firmas-pendientes.tsv` (FP-157…166 todas FIRMADA) — Duelo: `forense/prereg-duelo-v2/` (prereg+F1, lanzamiento-L, corridas-L 120, corridas-R, marcador v1.0, enlace-M, `_scoring-intento.json`) + `forense/crosswalk-pregunta-regla-v1_1.tsv` — Hito D: `forense/hitoD-preregistro-v2_0.md` (Registro :1156+; parser T18; README:36) — Censo R2.1: `forense/R21-censo-fuentes-v1_0.md` — Encargos A.3 del día: `forense/encargos/2026-08-26-*.md` — Experimento Compartamos: registro de llaves (octava clase, FP-164).
**Cierre de maestra-30.** Jornada de diez actos fusionados sin un rojo final: el programa llamó a un mode[TEXTO TRUNCADO EN LA TRANSCRIPCIÓN ORIGINAL — corte de contexto, no un artefacto del repo. NO commiteado como archivo separado por orden de dirección tras hallazgo; ver nota de cierre de este acto.]
```

## CONSUMIDO — PR #383, ver `forense/notas/2026-08-26-registra-pendientes-cierre.md`
