# ENCARGO · ACTO MAESTRA32-E5 · PROPAGA-FIRMAS-Y-COLA

**SHA de redacción:** `f10b277` (main, merge PR #393, verificado hoy sin commits posteriores) · **Redactado:** 30/ago/2026, dirección maestra-32 · **Instrucciones vigentes:** v2.11 · **Estado:** LISTO PARA LANZAR — las firmas F-175/F-170/F-172 ya vienen dadas; las RANURAS R-168/R-AGREGA/R-169/R-ENTERADOS son opcionales y **fail-closed**: la que llegue VACÍA se deja ABIERTA en el tablero, declarada, sin inventar (precedente `ADR-220`: M-LECTURAS vacía se respetó vacía).

**ENTORNO ASIGNADO: NUBE (`cloud_default`).** NO se lanza en UBUNTU — este acto no toca microdato; todos los insumos están versionados.

**Rótulo y salto declarado:** `MAESTRA32-E5`. El número **E4 queda reservado** para `MAESTRA32-E4 · RE-EMPAREJA`, sucesor declarado en los cierres de E2/E3 y aún no lanzado — el salto es a propósito, no un hueco (mismo patrón que v2.9 con A.10/A.11).

**Serie MAESTRA32.** Nada corre en paralelo con este acto.

---

## FIRMAS DE MESA YA DADAS — verbatim de la conversación de dirección, 30/ago/2026. El ejecutor PROPAGA, no reinterpreta (patrón SELLA-3, ADR-76/ADR-79).

**F-175 · `FP-175` → FIRMADA.** Letra de mesa: **"a y b"** — se autorizan LAS DOS ramas de extractor, con la razón de mesa verbatim: *"Si no acabamos algo lo olvidamos."* Secuencia operativa fijada por dirección: **(a) primero** (formatos estadísticos `.dta/.sav/.rdata/.dbf`, el encargo E3 ya redactado), **(b) después** (PDFs ficha-descriptiva + los 46 FD no-xlsx de `FP-173`); el encargo de la rama (b) **se redacta al cierre de E3(a)** para heredar sus aprendizajes — esa redacción pendiente queda registrada DENTRO de la fila-grito (abajo), no en la memoria de nadie.

**F-170 · `FP-170` → FIRMADA.** Letra de mesa: **"de acuerdo"** con la recomendación de dirección — se recibe **N=12/30** como cifra correcta para gatear la fase de cálculo, y las **3 filas SIN-CLASIFICAR** (G3, G4, evidencia_experimental_terceros) **NO se fuerzan**: quedan declaradas tal cual.

**F-172 · `FP-172` → FIRMADA.** Letra de mesa: **"firmar cola diferida hoy"**, con la condición de mesa verbatim: *"asegurar que quede claro que correremos las siguientes cuando haya caja — no quiero que se nos vaya entre las grietas."* Se firma: (i) las mediciones promovibles sobre los `EXISTE-SATISFACE` de `data/cruce-inverso-v1_1.tsv` van a **cola diferida de medición**, prioridad a las que tocan pares del motor — la lista concreta la deriva del tsv el encargo medidor cuando se redacte (deriva, no heredes); (ii) la orden de adquisición ENCUCI/ENIF/ENNViH queda en la misma cola; (iii) **nada de esto corre sin caja**, y el registro anti-grietas es la fila-grito de abajo, no una tsv nueva — verificado hoy contra `data/INFRAESTRUCTURA-v1_0.md:240-242`: las 6 colas `.tsv` existentes están todas en la lista de "tablas que nadie lee"; el mecanismo que sí grita en cada corrida es una fila `ABIERTA` del tablero bajo `T-FIRMAS` (A.12: "el WARN seguirá gritándolo en cada corrida hasta que alguien lo atienda").

---

## RANURAS OPCIONALES — mesa las llena antes de lanzar, o quedan ABIERTA

**R-168 — [FIRMA M — VACÍA].** `FP-168`. Propuesta de dirección, respaldada por benchmark web del 30/ago (fuentes en la nota de cierre): **`nivel_ic = 0.95`** (estándar unánime en evaluación de modelos 2025-2026: percentil bootstrap 95%, típicamente 10,000 resamples) y **`seed = 42`** (entero fijo declarado; aparece literal como convención en la literatura de bootstrap pareado). Nota de diseño que viaja al ADR, no a la firma: la práctica vigente privilegia el **bootstrap pareado por celda** sobre IC por brazo, y para el lado L (no-determinismo del LLM) k≥3 corridas por ítem con bootstrap por conglomerados — insumo para el pre-registro del duelo, no cambia `scoring-adv1-m3.py` hoy.

**R-AGREGA — [FIRMA M — VACÍA].** Segunda vuelta de M-AGREGA, re-informada por benchmark web del 30/ago: la vía **estándar** (compuesto media/suma de ítems → un solo β̂, o factor scores) **requiere reabrir el microdato** — no existe opción estándar sin caja; y el ítem único post-hoc queda desaconsejado (pesos/cargas sample-specific). Opciones:
- **(a′)** Mantener sin consumir **+ pre-registrar HOY** la re-estimación compuesta (θ = media simple de ítems, chequeo de unidimensionalidad en la corrida) como entrada de la cola Ubuntu — la vía estándar, ejecutada cuando vuelva la caja.
- **(b′)** Todo lo de (a′) **más** un `valor_ejecutable` **interino** por par multi-ítem: media ponderada por varianza inversa de los β̂ por ítem, **solo punto, sin IC** (los ítems comparten encuestados; sin covarianza el IC agregado sería inválido — se escribe `ic: NO-DERIVABLE-SIN-COVARIANZA`), rótulo `ASOCIACION-MEDIDA·AGREGADA-CONVENCION-INTERINA`, **SUPERADA automáticamente** por la compuesta cuando corra. Mueve ejecutables 3→5 hoy.
- **VACÍA = (a′)** (fail-closed: la cola se registra igual; ningún valor entra sin firma).

**R-169 — [FIRMA M — VACÍA].** `FP-169`: mesa **ratifica** la lectura ya propagada (falsador del 8/sep acotado al cruce #363, NO se dispara; palanca #1 queda B-bis sin fuente, no se re-especifica — la condición de reapertura no se satisface bajo la lectura más defendible, con la alternativa ya declarada en `perimetro-alcanzable-v1_0.md §2 C2`) → FIRMADA; o marca "lectura alternativa" y la fila queda ABIERTA con esa anotación.

**R-ENTERADOS — [FIRMA M — VACÍA].** Bloque de lecturas: `FP-171 · FP-173 · FP-174 · FP-178` — mesa escribe "enterado ×4" (o tacha las que firma). Sus gateas ya corrieron o no aplican (E5/ADR-214 corrió; E2 corrió con N=0).

---

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

**A.2, tercera parte:** `ls data/raw/ 2>/dev/null | head -1` — reporta el valor crudo; para este acto se espera ausente y no importa. **Regla de lectura:** campos YAML íntegros con `yaml.safe_load`; en la caja, `command grep` siempre y todo negativo con su conteo de archivos (A.13).

---

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (maestra-32, 30/ago/2026, contra `f10b277`) ═══

**1 · ESTRUCTURA.** Dominios 7 (sellar decisión: ADR + cascada) y 9 (decisión de mesa) de `data/INFRAESTRUCTURA-v1_0.md`; fila "lancé un encargo" de la tabla X→Y (`forense/encargos/convencion.md`). Tablas gobernantes: `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` · `forense/encargos/` · `canon/registro-rotulos.tsv`; con R-AGREGA=(b′), además `milpa/procedencia.yaml` (solo sección `coeficientes_generador_sellados`) por la vía que `ADR-220` ya sancionó.

**2 · CONTENIDO.** (i) Las nueve filas destino están hoy no-firmadas — verificado por `csv.DictReader` sobre las 174 filas del tablero: `ABIERTA` = `FP-168, 170, 171, 172, 173, 174, 175, 178`; `FIRMADA-PARCIAL` = `FP-169`. Ninguna otra fila no-FIRMADA existe, así que **NO-ENCONTRADO** una fila de cola-Ubuntu previa (universo: las 9 filas no-firmadas leídas íntegras + conteo por estado del tablero completo). (ii) **E3 NO está archivado** — `ls forense/encargos/ | command grep -c MAESTRA32` → **2** (solo E1 y E2, listado completo del directorio a la vista): la grieta A.3 es real y este acto la repara. (iii) Las 6 colas `.tsv` de `data/` figuran, todas, en la lista "tablas que nadie lee" del propio índice (`INFRAESTRUCTURA:240-242`) — por eso la cola NO va en tsv nueva.

**3 · COBERTURA RETROACTIVA.** El tablero nació el 14/ago (`6e0f2a1`) — todas las filas destino nacieron después (25-28/ago), sin brecha. La convención de encargos es anterior a E3 (redactado 28/ago): su no-archivado no es hueco de estructura sino omisión de lanzamiento — exactamente lo que A.3 predijo de un encargo que vive solo en una conversación.

═══════════════════════════════════════════════════════════════════

## 0-bis · A.3

Primer commit: este encargo verbatim (con las ranuras tal como mesa las entregó) en `forense/encargos/2026-08-30-MAESTRA32-E5-PROPAGA-FIRMAS-Y-COLA.md`. Al cerrar, `## CONSUMIDO` con el PR.

## Pasos

**Paso 1 · Archiva E3 (repara la grieta A.3).** Copia verbatim el encargo `MAESTRA32-E3 · EXTRACTOR-DTA` (texto adjunto al lanzamiento de este acto; dirección lo entrega íntegro) a `forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md`, añadiendo SOLO cabecera: `RANURA M-EXTRACTOR: FIRMADA "a y b" (mesa, 30/ago/2026) — secuencia a→b; estado: EN-COLA-UBUNTU · GATED-ENTORNO (requiere corpus montado, A.2 tercera parte)`. El cuerpo no se edita.

**Paso 2 · Tablero (mismo commit que lo que propaga, A.12).**
- `FP-175` → FIRMADA con F-175 verbatim (letra, razón de mesa, secuencia a→b, rama-b-por-redactar → fila-grito).
- `FP-170` → FIRMADA con F-170 verbatim.
- `FP-172` → FIRMADA con F-172 verbatim (cola diferida; condición de mesa citada; registro → fila-grito).
- Ranuras llenas → `FP-168` FIRMADA (valores de R-168) · `FP-169` FIRMADA (ratificación) · `FP-171/173/174/178` FIRMADA (R-ENTERADOS). Ranura vacía → la fila queda como está, y la nota de cierre lo declara en una línea.
- **Fila-grito nueva (rango pre-asignado `FP-179`, re-deriva el máximo):** `qué_se_firma:` "Mesa dispara la COLA-UBUNTU cuando la caja con corpus vuelva. Entradas, cada una con su encargo o su redacción pendiente: (1) `MAESTRA32-E3` rama (a), encargo archivado, listo; (2) rama (b) PDF-FD — **dirección redacta al cierre de E3(a)**; (3) mediciones diferidas de `FP-172` — encargo medidor por redactar, lista derivable de `data/cruce-inverso-v1_1.tsv` veredicto=EXISTE-SATISFACE, prioridad pares del motor; (4) re-estimación compuesta de los 2 pares multi-ítem (θ = media de ítems, unidimensionalidad en la corrida) — pre-registrada por R-AGREGA; (5) `APERTURA-ENFIH-ENSAFI` (`canon/APERTURA-FASE-CALCULO-v1_2.md §3`), la palanca grande declarada desde el 12/ago." `estado: ABIERTA` **a propósito** — es el grito diario de T-FIRMAS hasta que la caja vuelva; cerrarla sin lanzar la cola sería recrear la grieta. `gatea:` el lanzamiento de cada entrada; se marca por entrada, no en bloque.

**Paso 3 · Rama (b′) de R-AGREGA — SOLO con esa letra.** Script (pegado con salida en la nota): lee los 2 pares multi-ítem de `coeficientes_generador_sellados` con `yaml.safe_load`; por ítem, parsea `beta_hat` e IC; peso = 1/var con var = ((sup−inf)/(2·1.96))²; escribe `valor_ejecutable` = media ponderada, `ic: "NO-DERIVABLE-SIN-COVARIANZA (ítems del mismo encuestado)"`, `rotulo: ASOCIACION-MEDIDA·AGREGADA-CONVENCION-INTERINA`, `superada_por:` puntero a la entrada (4) de la fila-grito. Cualquier IC no parseable = **PARO-reporta**, no se adivina peso. Actualiza `tests/test_matriz_sellados.py` (partición 3→5 override / 10 fallback) y corre `tests/check.py --baseline` → **VERDE obligatorio**; FAIL nuevo = PARO-reporta.

**Paso 4 · ADR y cascada.** Candidato re-derivado con el comando de la casa (hoy daría 222 — **deriva, no heredes**; renumera quien fusiona segundo). El ADR trae: las tres firmas F verbatim, las ranuras que llegaron llenas verbatim, las que llegaron vacías declaradas, el respaldo web de R-168/R-AGREGA en dos líneas con las fuentes de la nota, y la creación de la fila-grito con su razón (colas tsv muertas, `INFRAESTRUCTURA:240-242`). Cabecera de gobernanza · recifrado L0 de `estado-programa` (y "ejecutables 3→5" SOLO si b′ corrió, derivado del test) · `registro-rotulos`: `MAESTRA32-E5` censado (token pelado `E5` colisiona con habitantes previos — se censa, no se reclama, D-6) · `tests/check.py` `_T25_ARCHIVOS_CONOCIDOS` para los archivos nuevos · nota de cierre `forense/notas/2026-08-30-propaga-firmas-cierre.md` con A.13 en todo conteo y las URLs de los benchmarks web citadas.

## B-bis

Acto de propagación: no corre falsador; el desenlace por ranura está escrito arriba. Divergencia entre letra y árbol = PARO-reporta.

## PERÍMETRO Y CONCURRENCIA

Archivos que este acto puede tocar, y ningún otro: `forense/encargos/2026-08-30-MAESTRA32-E5-PROPAGA-FIRMAS-Y-COLA.md` · `forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md` (solo crear con cabecera) · `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · `canon/registro-rotulos.tsv` · `tests/check.py` (solo `_T25_ARCHIVOS_CONOCIDOS`) · `forense/notas/2026-08-30-propaga-firmas-cierre.md` · **solo con b′:** `milpa/procedencia.yaml` (solo los 2 pares de la sección sellados) y `tests/test_matriz_sellados.py`. Concurrencia: ninguna. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

## FP pre-asignadas

`FP-179`–`FP-180` (máximo hoy `FP-178`, re-deriva). Uso: fila-grito (179); buffer (180). Renumera quien fusiona segundo.

## CONTADOR

Firmas propagadas: hasta 9 filas (3 seguras + hasta 6 por ranura) · grieta A.3 reparada (E3 archivado) · cola-Ubuntu registrada con 5 entradas bajo WARN diario · **solo con b′: ejecutables 3→5**. Sin b′: cero directo en el motor, declarado.

## Lo que este acto NO hace

No lanza ninguna entrada de la cola (todas requieren caja). No redacta la rama (b) ni el encargo medidor (registrados como redacción pendiente, con dueño: dirección). No toca Hito D, censos vencidos, `limite_c2`, `FP-152`. No corre el piloto ni el scoring — eso viene en los encargos nube siguientes (PILOTO-T1T2, ETIQUETA-v1_2), gateados a este merge.

## Sucesores declarados, no lanzados

`MAESTRA32-E6 · PILOTO-T1T2` y `MAESTRA32-E7 · ETIQUETA-v1_2` (nube, dirección los redacta tras este merge) · `MAESTRA32-E4 · RE-EMPAREJA` (reservado, tras extractores) · toda la fila-grito.

## CONSUMIDO

Ejecutado en la rama `claude/maestra32-e5-firmas-cola-vroay4`. Esta sesión NO abre PR — commitea y pushea a la rama designada, mismo patrón que `MAESTRA32-E2` para no repetir el defecto ya visto en el acto E9. Número de PR: N/D desde esta sesión; quien fusione (dirección, u otra sesión con permiso de abrir PR) llena este campo al abrirlo. Resultado: `MAESTRA32-E3 · EXTRACTOR-DTA` archivado verbatim (grieta `A.3` reparada); `FP-175`/`FP-170`/`FP-172` → `FIRMADA`; fila-grito `FP-179` nueva, `ABIERTA`; las cuatro ranuras opcionales (`R-168`, `R-AGREGA`, `R-169`, `R-ENTERADOS`) llegaron vacías y se dejaron vacías (`FP-168`/`FP-169`/`FP-171`/`FP-173`/`FP-174`/`FP-178` sin cambio); `ADR-222`; `tests/check.py --baseline` VERDE. Detalle completo: `forense/notas/2026-08-30-propaga-firmas-cierre.md`.
