ENCARGO · ACTO MAESTRA37-N2 · GUARDIA-TSV-Y-CAPA2-LISTAS
SHA de redacción: `8f49eab8` (`origin/main`, merge PR #511) · 3/sep/2026, dirección (Fable, maestra-37) · v2.12 · COMPUERTA: ninguna.

ARRANQUE punto 1: reporta `git rev-list --count origin/main` y `test -f .git/shallow && echo SHALLOW`; si SHALLOW, `git fetch --unshallow origin` antes de nada (defecto medido por MAESTRA37-N1, ADR-319).

ENTORNO ASIGNADO: NUBE. NO en UBUNTU: todo es código y TSV versionados; la verificación contra corpus de las 6 filas de FP-246 es un sucesor de caja, no este acto.

Punto 4: no toca red ni microdato — dilo y sáltalo.

MODELO SUGERIDO: Opus (edita dos herramientas con regresión byte a byte).

CARRILES: MAESTRA37-L1 corriendo en caja — toca tools/inventario_reactivos*.py, tools/busca_reactivos.py, .claude/commands/mapea.md, data/inventario-*; este acto no toca ninguno. Colisión sólo en hallazgos.md, tablero y cabecera de gobernanza (append; renumera quien fusiona segundo).

FIRMAS DE MESA — verbatim. El ejecutor propaga, no decide (SELLA-3). La firma de mesa es el merge de este PR (declarado por mesa el 3/sep/2026: «mi firma es el PR mergeado»).

* FP-258 y FP-246 · FIRMA DE MESA, verbatim, 3/sep/2026: «D6 · FP-258 / FP-246 — infraestructura (encargo N2, ya entregado) a, reparar.» Lectura de dirección, declarada: «a, reparar» = reparar las dos — FP-258 por la vía (ii) (lector/escritor propio que preserva el crudo, la única opción de esa fila que es una reparación y no una normalización de notas ajenas) y FP-246 por la vía (a) (reparar el script). Mesa firma esta lectura al fusionar el PR; si no era ésa, el ejecutor PARA y reporta al recibir enmienda de dirección.

═══ VERIFICACIÓN DE EXISTENCIA (A.8), contestada por dirección contra `8f49eab8` ═══
(1) ESTRUCTURA. Registro del curador: `data/curacion-registro/` (`GUIA-CURADOR-REGISTRO.md`, `INFRAESTRUCTURA-v1_0.md` D1-D3). Vista generada de la cola: `tools/vista_cola_adquisicion.py` + `tests/check.py::T26` (vista contra función, no registro contra sí mismo). Verificación capa 2: `tools/curador_registro/via_capa2.py`. Suite: `tests/check.py`; validador del curador: `tools/curador_registro/baseline.py`.

(2) CONTENIDO — los dos defectos siguen vivos y uno creció:
* FP-258. Round-trip `csv.reader`→`csv.writer` (tab, `QUOTE_MINIMAL`) sobre `data/curacion-registro/cola-adquisicion-registro.tsv`: 112 líneas, 4 distintas tras el round-trip: 29, 47, 63, 94. La fila declaraba 3 (29, 47, 94); la 63 es la de CompraNet que MAESTRA36-A2 editó línea por línea (ADR-314). Ningún test lo vigila: T26 compara vista contra función.
* FP-246. `tools/curador_registro/via_capa2.py:174` `entrada = por_id.get(idm)` → `:176` `ID_NO_EN_MANIFIESTO`. `relaciones.tsv` hoy: 6 filas con `;` en `id_manifiesto` (`awk` por columna, no `grep` de subcadena). Las seis declaran `capa2_manifiesto = SI` y ninguna ha pasado por esa vía.

(3) COBERTURA RETROACTIVA. Ambos defectos medidos el 2-3/sep sobre tablas que nacieron el 29/ago–1/sep; ningún acto desde entonces los reparó (`grep -c 'FP-258\|FP-246' canon/gobernanza-v1_15.md` → sólo las entradas que los abren, ADR-293/ADR-310).

SPEC POR PIEZA (un PR, un ADR, un recibo). Cada pieza es dos commits: COMMIT-1 congela el control (el round-trip actual y la lista de 6 filas, con salida cruda) antes de editar código; COMMIT-2 trae el código y la regresión.

P1 (FP-258, vía (ii)) · `tools/curador_registro/tsv_crudo.py`: lector/escritor de TSV que preserva bytes (split por `\t`, sin quoting, sin normalizar comillas); `tools/vista_cola_adquisicion.py` lo adopta con regresión byte a byte de la vista (`diff` vacío contra la vista actual en `origin/main`). Test nuevo `T26-bis` en `tests/check.py`: round-trip del registro con el lector propio → 0 líneas distintas; y un control que documenta que el round-trip `csv` da 4 (para que el día que alguien lo "arregle" con `csv` se vea). No normaliza las 4 notas. `baseline.json` no se recongela salvo que la única entrada nueva sea de este acto y se declare.

P2 (FP-246, vía (a)) · `via_capa2.py`: `id_manifiesto` se parte por `;`, cada id se resuelve por separado, la fila entra a `estados_verificacion` sólo si TODOS coinciden y la salida enumera por id (`COINCIDE`/`AUSENTE`/`raiz-no-configurada`/`hash-discordante`, sin colapsar — A.1). Regresión: sobre las filas SIN lista, salida byte a byte idéntica a la de `origin/main` en modo lectura (`--escribe` no se usa); sobre las 6 con lista, en nube devuelve `raiz-no-configurada` por id (no hay corpus) — declarado, no escondido. Sucesor de caja: correrlo con corpus sobre las 6 (29 payloads) y cerrar la fila.

P3 · Tablero: FP-258 y FP-246 → FIRMADA con la letra verbatim de arriba y la lectura de dirección; EJECUTADA sólo tras la regresión en verde (FP-246 queda FIRMADA, no EJECUTADA: la verificación con corpus es sucesor de caja); FP-272 recibo. hallazgos.md: una línea con el 3→4 de FP-258.

PERÍMETRO Y CONCURRENCIA. Toca: `tools/curador_registro/tsv_crudo.py` (nuevo) · `tools/vista_cola_adquisicion.py` · `tools/curador_registro/via_capa2.py` · `tests/check.py` (T26-bis) · `data/INFRAESTRUCTURA-v1_0.md` (registra el módulo nuevo, T27) · `forense/notas/2026-09-03-MAESTRA37-N2-{control,cierre}.md` · `forense/hallazgos.md` · `forense/firmas-pendientes.tsv` · A.3 · cascada. NO toca: `data/curacion-registro/*.tsv` (ni una línea; el registro no se normaliza), `data/manifiesto.yaml`, `data/raw/**`, `milpa/**`, `tools/inventario_reactivos*.py`, `tools/busca_reactivos.py`, `.claude/commands/**`, la cola de encargos. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR CANDIDATOS (deriva, no heredes): ADR máx 319 al redactar → candidato ADR-320 (MAESTRA37-L1 puede tomarlo antes; entonces 321); FP máx 270 → FP-272 (271 es el recibo de L1; si L1 no ha fusionado, toma 271 y decláralo).

CONTADOR: tests utilizables en nube +1 (T26-bis) · filas del curador verificables por capa 2: 0 → 6 (verificación real en caja, sucesor) · dominios abiertos 0 → 0 · cargas al motor 0 · medición de modelo: cero directo, declarado (infraestructura; se lanza porque corre en paralelo a L1 sin competir por la caja, no porque mida).

Lo que NO hace. No edita ninguna fila de ningún TSV del registro; no verifica contra corpus; no toca la cola ni L10; no mide; no decide.

Sucesores. Caja: `via_capa2.py` sobre las 6 filas con corpus montado → FP-246 EJECUTADA.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA37-N2 · GUARDIA-TSV-Y-CAPA2-LISTAS`, rama
`claude/fp-258-fp-246-repair-vmy8j5`, `PR #513` contra `main` (sin fusionar por el
ejecutor — el merge es firma de mesa, declarado en el propio encargo).

- **P1 (FP-258, vía ii)**: `tools/curador_registro/tsv_crudo.py` (nuevo) +
  `tools/vista_cola_adquisicion.py` adoptado, regresión byte a byte en verde. `T26-bis`
  nuevo en `tests/check.py`. Control re-medido: 4 líneas distintas hoy (no 3 — la fila
  63 de CompraNet, `ADR-314`, se sumó después de que `FP-258` se abriera).
- **P2 (FP-246, vía a)**: `tools/curador_registro/via_capa2.py` parte `id_manifiesto`
  por `;`; regresión en modo lectura idéntica salvo el contador `AUSENTE` (54 → 83).
  Discrepancia medida: las 6 filas resuelven `AUSENTE`, no `RAIZ_NO_CONFIGURADA` — ningún
  id declara `raiz` propia en el manifiesto.
- **P3**: `FP-258 → FIRMADA-EJECUTADA`, `FP-246 → FIRMADA` (NO EJECUTADA), `FP-272`
  recibo. Línea 3→4 en `forense/hallazgos.md`.
- **Cascada**: `ADR-320`, `L0` recifrado, `canon/registro-rotulos.tsv` censado.
- **Nota de cierre**: `forense/notas/2026-09-03-MAESTRA37-N2-cierre.md`.

`python3 tests/check.py --baseline` → **LÍNEA BASE VERDE**, 19 FAIL sin cambio frente a
`tests/baseline.json`. Perímetro verificado con `git diff --stat origin/main..HEAD`:
ningún archivo fuera de la lista declarada cambió.
