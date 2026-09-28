# ENCARGO · ACTO GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1 · El mapa de dominios (1 396 afirmaciones, columna vertebral del tablero de carriles) sigue en v1.1, anterior a todo lo medido y dictaminado esta semana: `gen2_existente`, `estado_corpus`, `siguiente_operacion` y `clase` están desactualizados para cientos de filas, y las 611 «instrumento sin equivalencia» nunca se cruzaron con el mapa de instrumentos alternos. Y el manifiesto sigue con 554 payloads sin licencia pese a CORPUS-LICENCIAS-1. Este acto produce el mapa v1.2 por objeto y cierra las licencias, con latitud de guía

> ENTORNO: **NUBE** — lee sellados, vistas, mapa, tabla de reglas, mapa de instrumentos alternos, manifiesto y portales de términos; no abre microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `9d2550b9` (re-deriva al abrir) · una sesión, rama propia; PR por bloque (mapa · licencias) · MODELO: **Opus** · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto · D-21 aplica.
CONTADOR: cero mediciones; no adopta. Mueve los derivados del mapa (afirmaciones por clase, `mapa11_dominios_medidos` solo si su script lee el mapa y no el catálogo) y `payloads_sin_licencia`; declara antes/después. **NC solo por D-19.**

## 1 · OBJETIVO
(P1) **Mapa de dominios v1.2** (`canon/mapa-dominios-v1_2.tsv`; v1.1 intacta): por afirmación, `gen2_existente` desde los RESULT sellados y registrados en la vista (llave lógica, instrumento, ola, dominio) — incluyendo lo de esta semana (RELEVO-TRAMITE, PISOS ENCIG, CALC-ALTERNOS, PISOS-DOMINIOS, C1 lote 3 suspensiones); `estado_corpus` y `reserva` desde el manifiesto por id (A.15); `siguiente_operacion` con el vocabulario del tablero (FIRMA · RESERVA · ADQUISICION · CALC · EDITORIAL · NADA); `clase` re-dictaminada donde el mapa de instrumentos alternos encontró otro instrumento (las 611 INSTRUMENTO-SIN-EQUIVALENCIA se cruzan por texto de pregunta con `mapa-instrumentos-alternos-v1_0.tsv` y con `reglas-contrastadas-v1_1.tsv`; lo que pase a MEDIBLE-EN-CORPUS se declara con el reactivo). Ninguna afirmación cambia de dominio ni de report. Test: v1.2 tiene las mismas 1 396 filas y llaves que v1.1 (solo cambian columnas de estado), y `tablero_carriles.py` la lee sin cambios de esquema.
(P2) **Licencias.** [EJECUTADO] a `9d2550b9`: 554 payloads con `licencia` vacía pese a CORPUS-LICENCIAS-1 consumido. Primero, dónde escribió LICENCIAS-1 (¿otro campo, otro archivo, un lote no aplicado?) y por qué la vista no lo ve: hallazgo con cita. Después, terminar: licencia por portal con página de términos sellada (regla por dominio de `url_origen`), NO-DETERMINABLE con búsqueda citada donde no haya términos, unificación de grafías, y el test huérfano que rechaza payloads nuevos sin licencia. Los 598 residuales que TRAMITE-FIRMAS-21 mandó a LICENCIAS-2 (R50) son estos: no hay un tercer acto.
(P3) **Cierre.** Conteos por comando: afirmaciones por clase antes/después, cuántas ganaron `gen2_existente`, cuántas pasaron de sin-equivalencia a medible, licencias resueltas / NO-DETERMINABLE; el tablero de carriles regenerado con el mapa v1.2 (por el canal) y una línea en la nota con qué carriles cambian de semáforo por eso.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: `mapa-dominios-v1_2.tsv` con 1 396 filas y llaves idénticas a v1.1 (test) · toda afirmación con RESULT registrado en la vista tiene `gen2_existente` no vacío (cruce por comando: faltantes 0) · `licencia` vacía en el manifiesto: 0, y «no declarada por la fuente» sin universo: 0 · test huérfano de licencias verde · `tablero_carriles.py --actualiza` corre sobre v1.2 sin error · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
ADENDA-1 de TRAMITE-FIRMAS-21 (R50 (a): licencias residuales; reservas de olas; R09 D1) · A.4, A.15, A.16, A.17 · §3 (nada cambia de dominio ni de report sin cita) · E.7 (solo lo registrado en la vista cuenta como GEN2 existente). Ninguna firma nueva; el mapa no adopta.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `9d2550b9` · `mapa-dominios-v1_1.tsv`: 1 396 filas; `clase`: MEDIBLE-EN-CORPUS 235, MEDIBLE-CON-ADQUISICIÓN 717 (611 INSTRUMENTO-SIN-EQUIVALENCIA), NO-MEDIBLE-POR-DISEÑO 420, NO-CONSTRUIBLE 24. `mapa-instrumentos-alternos-v1_0.tsv`: 64 pares. Manifiesto: `licencia` vacía 554; campo `reserva` que empieza por RESERV: **0** (antes 175: el nombre o el valor cambió con TRAMITE-FIRMAS-21; verificar por id, no asumir).
- [EJECUTADO] Tablero de carriles: 31 carriles, 7 rojos, 21 amarillos, 0 verdes, 3 grises; su cadena de procedencia declara que la unión carril ↔ cifra pasa por dominio × instrumento porque el catálogo no trae `report`: el mapa v1.2 puede llevar `resultado_id` por afirmación y hacer esa unión directa (PROPUESTO-POR-DIRECCIÓN; decide tú si cabe en el esquema sin romper el test).
- [LEÍDO] Encargo CORPUS-LICENCIAS-1 (consumido): pedía 0 vacías al cierre; el manifiesto no lo refleja. Su nota dice dónde escribió: léela antes de repetir trabajo.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'MAPA-DOMINIOS-V1-2\|LICENCIAS-2\|MAPA-DOMINIOS-Y-LICENCIAS'` → 0. Consumidos y citados: MAPA-DOMINIOS v1.0/v1.1 (actos de cobertura), MAPA-INSTRUMENTOS-ALTERNOS-1, CORPUS-LICENCIAS-1, CORPUS-COMPLETO-1, TABLERO-CARRILES-1. En vuelo: CIERRE-Y-PRODUCTO-3 (nube: lee el mapa v1.1; si tu v1.2 llega antes de su informe, lo cita; coordina por archivo), MEDICION-CARRILES-2 y VALIDACION-Y-2027-1 (caja: sus RESULT entran a v1.3), el `[deriva]`.

## 5 · PIEZAS
P2 primero (es acotada y la vista la espera), luego P1, luego P3. Rama prevista: afirmación con RESULT sellado pero sin fila en la vista → «sellado en disco, no registrado» (no cuenta como existente; NC para el canal solo si es D-19, si no, línea de hallazgo); portal sin términos → NO-DETERMINABLE con urls y fecha.

## 6 · LATITUD — de guía
Esquema de v1.2 (columnas nuevas permitidas si el test de llaves pasa), orden, PR, si añades `resultado_id` por afirmación: tuyos. PREGUNTA A MESA: ninguna. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato · b) editar v1.1, sellos, el catálogo, campos del manifiesto distintos de `licencia`; cambiar dominio o report de una afirmación · c) adoptar; inventar una licencia; marcar `gen2_existente` sin fila en la vista · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Existente solo con fila en la vista» protege **adoptar** (E.7) · «Licencia solo con página de términos sellada» protege **borrar/adoptar** · «Llaves y dominios intactos» protege **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `canon/mapa-dominios-v1_2.tsv` (+ test), `data/manifiesto.yaml` (solo `licencia`), `data/raw/` (páginas de términos), `tools/manifiesto.py` (≤ 10 líneas si hace falta), test huérfano de licencias, `forense/analisis/mapa-dominios-1-2/`, nota, L0, cascada. Ajeno: `canon/catalogo-*`, `reglas-contrastadas-*`, vistas, sellos, `tools/tablero_carriles.py` (solo si el esquema nuevo lo exige, ≤ 10 líneas declaradas). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no adopta, no descarga microdato, no cambia el semáforo del tablero (lo regenera el canal). Sucesores: mapa v1.3 con lo que MEDICION-CARRILES-2 selle; frente público cuando las licencias estén en cero. Módulo de auditoría v2.16: **sí** en la nota del mapa (afirma qué del corpus es medible sobre México): ¿qué afirmación sobre el corpus fue escrita a mano y no derivada? El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

- **P2 · «licencia por portal con página de términos sellada … NO-DETERMINABLE con búsqueda citada»** (598 payloads) · NO-VERIFICABLE-AQUÍ — la red del entorno de nube deniega todos los portales (curl `000` en 14 hosts, incluido inegi.org.mx; WebFetch EGRESS_BLOCKED); sin página sellada no se escribe licencia (PARO c), y NO-DETERMINABLE afirmaría «la fuente no tiene términos» cuando lo que hay es «no pude alcanzar la fuente» (§2) · `payloads_sin_licencia` 598 → 598; «licencia vacía = 0» no se cumple · sin NC nueva: se reusa NC-260928-GEN2-CORPUS-LICENCIAS-1-1997-01, que sigue ABIERTA con la receta (red permitida o caja + una línea por portal en `aplica_licencias.py`).
- **P1 · 66 afirmaciones que solo se unen a CALC sellados en disco sin fila en la vista** · reserva, no pieza omitida: rama prevista §5, rotuladas «sellado en disco, no registrado»; línea en `forense/hallazgos.md` · no cuentan como GEN2 existente (E.7) · sucesor: mapa v1.3, tras el registro del canal (`deriva_mapa_v1_2.py --escribe` re-corre tal cual).
- **«`check.py --baseline` VERDE»** · NO-VERIFICABLE-AQUÍ — la sesión corre `--rapido` (0 FAIL · 467 WARN); la suite completa la juzga el CI del PR (P-A de /acto) · ninguno · CI del PR.

## CONSUMIDO

Ejecutado por PR #1312 (ADR-260928-GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1-5024-01): P1 completo (mapa v1.2); P2 parcial (22 grafías; 598 sin licencia por red denegada, NC-260928-GEN2-CORPUS-LICENCIAS-1-1997-01 sigue abierta); P3 completo.
