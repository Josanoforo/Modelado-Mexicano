# GEN2-PENDIENTES-4 · nota de cierre · 29/sep/2026

ADR `ADR-260928-GEN2-PENDIENTES-4-12d9-01` · NUBE (`ENTORNO-DERIVADO = NUBE`) · MODO AUTÓNOMO-AMPLIO (cláusula v1.0) · base `9d2550b9` · 0-bis `12d9fa63` · PR #1326.

Contadores: cero mediciones; no adopta. `no_corrido_abiertas` 334 → 284, sólo por cierres con cita; `celdas_validadas` 219 → 219 (Δ0).

## ARRANQUE
- **Base.** El acto arrancó sobre `origin/main` = `9d2550b9`; durante el acto entraron cinco merges de `origin/main` a la rama (`git log --first-parent --merges 12d9fa63..HEAD`). Al escribir esto, `git rev-list --count HEAD..origin/main` → 0.
- **Entorno.** `python3 tools/entorno.py --arranque` → `ENTORNO-DERIVADO = NUBE` · `senal-corpus: montado=NO archivos_examinados=0` · red `DENEGADA-POR-POLITICA (http_code=000, http_connect=403)` · `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (la variable no distingue nubes, A.2). Igual al que declara el encargo. El acto no abre microdato ni necesita red: lo que consultó de GitHub (estado de PR y CI) fue por la herramienta MCP.
- **Duplicado.** El PR #1326 es el de este acto; una sola rama, `claude/new-session-snmood`.

## Premisas que cayeron (logística y estado; el objetivo sigue alcanzable, se replantea y se declara)
- **«Solo 7» decisiones de mesa.** El título del encargo clasifica las 239 NC de «MESA (2026-10-05)» en 7 decisiones de mesa, 171 «encargo por escribir», 39 recetas personales y 18 que esperan al canal o a una hoja, y su perímetro prevé un «append de las 7» en `firmas-pendientes.tsv`. Leídas por objeto, salió otra cosa: 154 NC absorbidas por 16 encargos (contra 171), 40 acciones de titular (contra 39), 23 del canal (contra 18) y **42 NC que piden una decisión** (contra 7), que ni la delegación de PENDIENTES-3 ni la ADENDA-1 cubren (irreversible, firma nueva o la cláusula de lote estricto de una FP viva). Se agruparon en 28 renglones (D1–D28), cada uno con opciones, recomendación y texto de firma listo, de modo que mesa puede sellar en bloque con la recomendación por defecto. No cambia qué se mide ni una firma: es un hallazgo sobre el inventario.
- **Apéndice de firmas de 24 filas, no de 7.** 22 ABIERTA (una por renglón sin FP viva: D1, D2, D4, D6, D8, D9, D11–D26) y 2 FIRMADA: `FP-260928-GEN2-PENDIENTES-4-12d9-01` (las dos autorizaciones de la ADENDA-1) y `-02` (la delegación de PENDIENTES-3 y la regla A.14, que PENDIENTES-3 no asentó). A.12: una firma que viaja verbatim en un encargo la asienta el acto que lo ejecuta. Los renglones D3, D5, D7, D10, D27 y D28 citan la FP ya existente que los gobierna.
- **«`MESA-DECISION` ≤ renglones de la hoja».** Contra filas NC daría 42 > 28, porque varias NC comparten un renglón. INTERPRETACIÓN-DECLARADA (cláusula v1.0 §2): se cuentan renglones distintos citados por dueños `MESA-DECISION` (28) contra los renglones de la hoja (28); el test falla si un renglón queda sin NC o sin opciones y texto de firma.
- **Delegación de NC-0212 y NC-0338.** El encargo dice que la delegación de PENDIENTES-3 «ya estaba firmada; aquí se ejecuta». NC-0212 se cierra con la opción a de su fila en `pendientes-3/decididas-por-delegacion.tsv` y NC-0338 con la opción b, ambas reversibles y sin reescribir nada sellado (E.3). No se llevaron a mesa.
- **NC `…-8fdf-04`, nacida en un acto hermano.** Pedía decidir la regla ROJO del tablero; la FP `…-8fdf-01` ya estaba FIRMADA (ADENDA-2) y ejecutada por `ADR-260928-GEN2-MEDICION-CARRILES-2-8fdf-05` (`tools/tablero_carriles.py:57` define NARANJA y `:62` fija que ROJO viene después). Se cerró por firma; el renglón D29 que la llevaba a mesa se eliminó (A.17).
- **NC-0029.** Cerrada por diseño: regla 6 (`canon/MEMORIA-OPERATIVA.md:10`) y ADENDA-1 letra (a); sus residuales ya estaban descompuestos y cerrados.
- **Rutas que no existen.** `…-c6aa-03` y `…-f926-05` esperaban publicar en `data/derivados/` (`ls data/derivados` → no existe en `main`); se dejaron con dueño `CANAL (derivados/auto-*)` y no con una ruta inventada.
- **Cláusula de lote estricto (`…-7d98-01`).** Impide re-proyectar filas que el canal ya publicó sin una firma nueva. Por eso `GEN2-TUBERIA-CORRIDA0-2` P3(a) entrega diagnóstico y opciones (§5-bis) y no la re-proyección.

## P1 · cierres con cita
44 NC cerradas por este acto: 43 de las 334 iniciales y `…-8fdf-04`. Por tipo (`conteos_pendientes_4.py`): producto 17 · diseño 15 · firma 8 · duplicada 4. Cada cierre lleva `cerrado_por` con la forma `GEN2-PENDIENTES-4 · CERRADA (<tipo>: <cita>)`, sin paréntesis anidados, y `fecha_cierre` 2026-09-29.
- **Cómo se verificaron.** 43 de los 44 tienen sus archivos `verif-reproduce` y `verif-suficiencia` en `forense/analisis/pendientes-4/evidencia/` (comando re-corrido y suficiencia de la cita); la 44.ª (`…-8fdf-04`) nació después de la investigación y se verificó por lectura de `tools/tablero_carriles.py:57,62` y de la FP `…-8fdf-01`. Antes de aplicar, la sesión volvió a correr los comandos de las citas.
- **Tasa de corrección.** 16 de los 44 (36 %) se reescribieron al re-correr su comando: un «cierre por firma» que era sólo la recomendación de la delegación (NC-0251, NC-0412, NC-0212, NC-0338), cifras vencidas (554 sin licencia contra 111 en `forense/analisis/corpus-licencias-1/sin-licencia-base.tsv`), comandos que no se reproducen (NC-0294, NC-0296), una cita parafraseada como literal (5573-01), una NC duplicada de otra que este mismo acto cierra (3fc6-02, reescrita como producto) y referencias sin objeto verificable (df0d-04, e0db-05, NC-0070, c6f4-03, 23e3-01, e7be-05). Ninguna cita entra al libro sin haber corrido su comando.
- **Aplicación por línea.** `aplica_dictamen_pendientes_4.py` reescribe el libro por línea física y lo lee con `csv.DictReader`; contra el libro previo al dictamen, 307 líneas cambiadas: 263 sólo en `sucesor` y 44 con cierre (`estado`, `cerrado_por`, `fecha_cierre`). Ninguna otra fila se tocó.

## P2 · 16 encargos PROPUESTOS
En `forense/encargos/cola/PROPUESTOS/2026-09-29-<ROTULO>.md`, cada uno con su sidecar `.cuerpo.sha256` (`tools/sella_sha256.py --cuerpo`), plantilla v2.2 (diez secciones, premisas rotuladas, compuertas con lo que protegen, bloque EN-VUELO, PAROS cerrados) y sus NC absorbidas en §4. **No se lanzan**: dirección los revisa y mesa los lanza adjuntando el `.md`; `/acto` los archiva entonces con su 0-bis. El sucesor de cada NC es `DIRECCION-ENCARGO (<ROTULO>)`.

| Encargo | Entorno | Modo | NC absorbidas |
|---|---|---|---|
| GEN2-ADQUISICION-DOCUMENTAL-1 | NUBE | ABIERTO | 8 |
| GEN2-C1-SUCESORES-2011-2021-1 | CAJA | RÍGIDO | 11 |
| GEN2-CALC-ALTERNOS-LOTE-2 | CAJA | ABIERTO | 4 |
| GEN2-CORRECCION-C3-1 | NUBE | ABIERTO | 12 |
| GEN2-CURACION-CORPUS-2 | CAJA | ABIERTO | 15 |
| GEN2-FALSADOR-PLANTILLA-V22-1 | NUBE | ABIERTO | 1 |
| GEN2-MARCADOR-Y-SERIES-2 | NUBE | ABIERTO | 12 |
| GEN2-PISOS-DOMINIOS-Y-REGLAS-2 | CAJA | ABIERTO | 11 |
| GEN2-PISOS-DOMINIOS-Y-REGLAS-3 | CAJA | ABIERTO | 11 |
| GEN2-PRODUCTO-CANON-2 | NUBE | ABIERTO | 9 |
| GEN2-RELEVO-TRAMITE-CAJA-2 | CAJA | RÍGIDO | 6 |
| GEN2-REPLAYS-Y-RECIBOS-CAJA-1 | CAJA | RÍGIDO | 4 |
| GEN2-TRAMITE-ARCHIVO-2 | NUBE | ABIERTO | 7 |
| GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1 | NUBE | ABIERTO | 14 |
| GEN2-TUBERIA-CORRIDA0-2 | NUBE | ABIERTO | 16 |
| GEN2-TUBERIA-TESTS-Y-CHECK-2 | NUBE | ABIERTO | 13 |
| **Total** | | | **154** |

- **Reparto.** Se agrupó por objeto y entorno (D-11: hasta cuatro piezas afines por encargo). NC-0418 quedó aislada por su objeto. Las que piden CAJA van a encargos CAJA; los tres RÍGIDOS son los que sellan CALC nuevos o corren gates de validación, y por eso su latitud es sólo logística (D-18).
- **Concurrencia declarada.** Cada encargo lista en su bloque EN-VUELO los archivos que otro PROPUESTO o un acto en vuelo también toca (p. ej. `TESTS-Y-CHECK-2` sobre `cmd_verify`; `PISOS-3` P3(c) escribe `verificaciones-texto` v1_2; `PRODUCTO-CANON-2` escribe el mapa de dominios v1_3; `CURACION-CORPUS-2` verifica en caja lo de `fa42-03`).
- **Los dos últimos.** `CURACION-CORPUS-2` (15 NC: reservas, inventarios v_N+1, filas ciegas, residual, U5, INPC, CONAPO, Intercensal, términos INEGI, afirmaciones sin cola, CNBV/Banxico NO-ACCESIBLE) y `TUBERIA-CORRIDA0-2` (16 NC: caché y derivación compartida, `corrida0 ensayo` con guarda de libro vivo, vista y canal, citas C1, `RAICES_ESCANEABLES`, delta de 35 pares) se redactaron al final; su §5-bis deja a mesa las opciones que la cláusula `…-7d98-01` no permite decidir aquí.
- **Auditoría de las premisas.** `python3 forense/analisis/pendientes-4/audita_leido_pendientes_4.py forense/encargos/cola/PROPUESTOS/2026-09-29-*.md` → 16 archivos · 41 líneas `[LEÍDO]` · 41 sin discrepancia · 0 con hallazgo. La primera pasada dio 7 discrepancias: cuatro reales, ya corregidas antes (una cita a un cuerpo de PR degradada a `[REPORTADO]`; la cita de `TRAMITE-4.md` sin las FP que decía; «203» archivos de `canon/L0` corregido a 205; «seis CALC ARBITRO-MARGINALES» en lugar de los que decía) y tres falsos positivos del auditor (énfasis markdown, marcadores `#` de comentario y rangos `:NNN` sueltos), que se arreglaron en el script. El script sólo comprueba que la cita esté donde el encargo dice: no prueba que la premisa sea cierta.
- **Premisas `[EJECUTADO]`.** Son 122 en los 16 encargos y el auditor no las cubre. Muestra de 10 (semilla 2026, comando de sólo lectura re-corrido al cierre): las 10 coinciden con lo que el encargo dice haber obtenido. El resto no se re-ejecutó en bloque: el ejecutor de cada encargo las re-verifica antes de obedecer (§0).

## P3 · dueños, hojas y firmas
- **Lista cerrada de dueños.** Token al inicio del `sucesor` (A.16): `DIRECCION-ENCARGO (<ROTULO>)` · `MESA-ACCION (<fecha>)` · `MESA-DECISION (<hoja>#D<n>)` · `CANAL (<rama>)` · `CAJA (<encargo>)` · `ADQUISICION (…)` · `APERTURA (…)`; el `EN-CURSO` de un acto en vuelo se mantiene con su rama. `tests/test_pendientes_4_duenos.py` exige, además del token, encargo archivado (PROPUESTOS incluidos) y ancla `#D<n>` existente. Sin dueño de la lista: 0.
- **`forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md`.** 28 renglones (D1–D28) para 42 NC. Cada uno trae opciones, recomendación y texto de firma; su FP queda ABIERTA en `forense/firmas-pendientes.tsv`.
- **`forense/analisis/pendientes-4/hoja-recetas-pendientes-4.md`.** 24 acciones con identidad (A01–A24) para 40 NC, cada una con la receta de un minuto: quién, dónde y qué comando o clic. Ninguna se ejecutó aquí: son acciones de titular (correo, registro con identidad, Actions).
- **Canal.** 23 NC quedan con `CANAL (derivados/auto-*)`: lo que el job de derivados ya publicó se cerró con cita; lo demás espera un run.
- **Dueños que se mantienen.** APERTURA 17 (expedientes de `forense/prereg-aperturas`), ADQUISICION 7 y CAJA 1 ya tenían un dueño válido y no se tocaron.
- **Delegación.** `decididas-por-delegacion-pendientes-4.tsv` (328 filas: ABSORBE-EN-ENCARGO 154 · CIERRA 44 · DECISION-DE-MESA 42 · RECETA-DE-MESA 40 · ESPERA-CANAL 23 · MANTIENE-DUENO 21 · ESPERA-APERTURA 3 · ESPERA-ADQUISICION 1) deja escrito por fila qué se decidió por delegación y qué vuelve a mesa.

## P4 · conteos antes/después
`python3 forense/analisis/pendientes-4/conteos_pendientes_4.py --lee forense/analisis/pendientes-4/conteos-pendientes-4-antes.json` (el «antes» se derivó sobre `9d2550b9` antes de tocar el libro).

| | antes | después |
|---|---|---|
| ABIERTA | 334 | 284 |
| con «encargo por escribir» o «cierre por diseño propuesto» | 174 | 0 |
| dueño `MESA` | 239 | 0 |
| sin token de dueño | 2 | 0 |
| `EN-CURSO` | 42 | 0 |
| `DIRECCION-ENCARGO` | 0 | 154 |
| `MESA-DECISION` | 0 | 42 |
| `MESA-ACCION` | 0 | 40 |
| `CANAL` | 0 | 23 |
| `APERTURA` | 18 | 17 |
| `ADQUISICION` | 27 | 7 |
| `CAJA` | 6 | 1 |

- **Descomposición 334 → 284.** −43 cierres de este acto sobre las 334 · −14 cierres de otros actos (todos de `GEN2-TUBERIA-TABLERO-INSUMOS-1`, #1319) · +7 filas nuevas ABIERTA que llegaron por merge (`…68b3-01` de APERTURAS-PREREGISTRADAS-1; `…f926-02`, `-03` y `-05` de VALIDACION-Y-2027-1; `…c6aa-01`, `-02` y `-03` de TABLERO-INSUMOS-1), todas dictaminadas aquí. La 44.ª cierre propia (`…8fdf-04`) no cuenta en las 334: nació y se cerró dentro del acto.
- **Filas del libro.** 1 092 al arrancar → 1 102 (10 filas nuevas de actos hermanos, ninguna de este acto: el encargo no abre NC).
- **Clases de `nc_por_clase.py --json`** (284): ESPERA-DIRECCION-ENCARGO 154 · ESPERA-MESA-DECISION 42 · ESPERA-MESA-ACCION 40 · ESPERA-CANAL 23 · ESPERA-APERTURA 17 · ESPERA-ADQUISICION 7 · ESPERA-ACTO-NOMBRADO 1. No aparece SIN-ASIGNAR ni VENCIDA-CANDIDATA.

## «Hecho», por comando
- `python3 tests/test_pendientes_4_duenos.py --libro` → `libro: 1102 filas · 284 ABIERTA · fuera de la lista cerrada: 0 · con frase prohibida: 0 · MESA-DECISION: 42 NC en 28 renglones distintos ≤ renglones de la hoja 28 · renglones sin opciones/firma: 0 · renglones sin NC: 0`.
- `python3 tests/test_pendientes_4_duenos.py` → `OK test_pendientes_4_duenos (A-F + árbol real)`: sidecar, plantilla y NC listadas de cada PROPUESTO.
- `python3 tools/nc_por_clase.py --json` → ASIGNAR = SIN-ASIGNAR: 0 · VENCIDA = VENCIDA-CANDIDATA: 0 (el clasificador usa esos nombres, no «ASIGNAR» ni «VENCIDA»).
- `python3 tools/cierre_acto.py --encargo forense/encargos/2026-09-28-GEN2-PENDIENTES-4.md --sin-suite` → dictaminadas 44 · FALTA-DICTAMEN 0 · RUTA-SIN-SUCESOR 0.
- `python3 tests/check.py --rapido` → 0 FAIL (tras añadir a `_T25_ARCHIVOS_CONOCIDOS` los tres encargos propuestos que citan rótulos de mesa sin prefijo de espacio, con el comentario de dónde sale cada mención).
- `python3 tests/check.py --baseline` → ver el CI del PR (el juez de la suite completa).

## Para mesa
1. `forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md`: 28 renglones con opciones y texto de firma. Cada firma asienta su FP.
2. `forense/analisis/pendientes-4/hoja-recetas-pendientes-4.md`: 24 acciones de titular con receta.
3. Los 16 encargos de `forense/encargos/cola/PROPUESTOS/`: se lanzan sólo adjuntando su `.md`.

## Límites declarados
- **Cobertura de los cierres.** Las citas que dependen de un PR se verificaron por el estado del PR en la herramienta MCP de GitHub; no se leyeron logs de run ni se corrió Actions.
- **Cobertura de las premisas.** Las 122 `[EJECUTADO]` de los PROPUESTOS sólo se muestrearon (10); las 41 `[LEÍDO]` se comprobaron mecánicamente. Ninguna premisa `[EXISTE]`, `[SUPUESTO]` o `[REPORTADO]` lleva un verbo de funcionamiento (lo comprueba el test de plantilla).
- **Sin olas reservadas.** El acto no abrió ni derivó ningún dato: el corpus no estaba montado y no se leyó ningún tabulado ni comunicado de una ola reservada.
- **Sin subagentes en la redacción.** Los 16 encargos, las hojas y la re-verificación de los cierres se hicieron directamente en la sesión; los subagentes de redacción se interrumpieron por el límite de sesión y el operador pidió ejecutar sin ellos. La investigación previa (`evidencia/`: 42 `research`, 34 `verif-reproduce`, 34 `verif-suficiencia` y 2 consolidados) quedó archivada.
- **Tres copias de la lista de dueños.** `tools/nc_por_clase.py`, `tests/test_nc_cierre_hacia_atras.py` y `tests/test_pendientes_4_duenos.py`: una línea de `forense/hallazgos.md`; no se unificaron (fuera de perímetro).

## Cruce con actos en vuelo
Entraron en `main` mientras corría el acto: #1310 (`GEN2-VALIDACION-Y-2027-1`), #1313 (`GEN2-APERTURAS-PREREGISTRADAS-1`), #1312 y #1321 (`GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1`), #1319 (`GEN2-TUBERIA-TABLERO-INSUMOS-1`) y las hijas de `GEN2-MEDICION-CARRILES-2` (#1311, #1314, #1316, #1317, #1324, #1327 y #1336). Cinco merges de `origin/main` a la rama. Las 7 filas ABIERTA nuevas de esos actos se dictaminaron aquí (sólo su `sucesor`); sus filas CERRADAS (`…f926-01`, `…f926-04`) y las 14 que cerró TABLERO-INSUMOS-1 no se tocaron. Fuera del perímetro propio sólo se escribió lo que la cascada permanente exige (D-21): ADR, L0, registro de rótulos, hallazgos, fila del test en el censo de guardias, `_T25_ARCHIVOS_CONOCIDOS`, el registro de bloqueos del hook y el pie de cierre del encargo de este acto. No se editó ningún otro encargo archivado, sello, vista ni RESULT.
