# Nota del acto · FUSION-PUERTAS — adjudicación de `FP-12`

**Encargo:** `forense/encargos/2026-08-18-FUSION-PUERTAS.md`. **SHA de arranque:** `35c9c9f` (`origin/main`, merge de `PR #278`, `ACTO LIMPIA-CAJA`, 19/ago/2026 — verificado tras `git fetch --unshallow`, el clon había nacido superficial con `origin/main` seis días viejo en `f8eb2e3`; el mismo defecto que `ACTO FUENTE-ÚNICA-DECISIONES` y `ACTO E-HIG` ya midieron dos veces, medido aquí una tercera).

## 1 · Precondición — cierre de la fase semántica de `BARRIDO-2`

`FP-12` viaja en `DISPARADOR-B` de `FP-26` (`ADR-101(h)`), condicionado al cierre de la fase semántica de `BARRIDO-2`. Verificado: `ACTO B2-SEMANTICO` (`ADR-108`/`ADR-109`, `PR #268`) cerró esa fase — la cascada `resolve_sources` pasa a unión declarada, `FP-35`/`FP-46` ejecutadas, `data/curacion-universo/` trae productos durables regenerados (35 709 filas en `universo-declarado-t0.tsv`, verificado por comando: `wc -l data/curacion-universo/universo-declarado-t0.tsv`). Junto con el gate material cerrado por `PR #260`, la condición de `ADR-100(9)` queda satisfecha: procede adjudicar sin volver a mesa.

## 2 · Releer ambas tablas contra el universo nuevo (Tarea, paso 1)

- `data/UNIVERSO-MINIMO-FUENTE-v1_0.md` — leído completo (58 líneas). **No es una tabla de fuentes.** Es una lista procedimental de 6 niveles ("La lista, para fuentes INEGI, en orden de costo creciente") que un acto recorre antes de declarar `NO-ENCONTRADO` sobre un campo material — cero filas de datos, cero columnas, cero identificador de fuente por fila. `grep -c -E "^[0-9]\." data/UNIVERSO-MINIMO-FUENTE-v1_0.md` → 6, como su propio contrato declara.
- `data/universo-puertas-2026-08-14.tsv` — 123 líneas (122 filas + cabecera), 15 columnas (`puerta`, `clase_origen`, `institucion`, `url`, `tipo`, `cobertura_temporal`, `unidad_observacion`, `granularidad_geo`, `hay_microdato`, `condicion_acceso`, `necesidad_que_sirve`, `llave_ADR57c_si_alguna`, `clasificacion_a4`, `universo_declarado`, `fecha_sondeo`). Es un **censo de puertas** — instituciones, portales y catálogos de metadatos verificados uno por uno (`CNBV`, `IMSS`, `STPS`, `INE`, fichas RNM de `ENSAFI`/`ENFIH`, etc.), con veredicto `clasificacion_a4` por fila.
- `data/curacion-universo/*` (productos durables de `BARRIDO-2`) — inventario de **activos INEGI internos** (`activo_id`/`objeto_logico_id` por archivo de programa, ej. `CNGMD2019_M2S10.xlsx`), dominio distinto: microdato/tabulado ya identificado dentro de programas INEGI conocidos, no puertas/portales externos (`CNBV`, `IMSS`, `STPS`, catálogos ajenos a INEGI que `universo-puertas` sí cubre). **No cubre `universo-puertas`**: ninguna fila de `universo-declarado-t0.tsv` tiene equivalente de institución externa, url de puerta o `clasificacion_a4` — son ejes que el producto del barrido no mide. `FP-12` **no queda superada por los productos del barrido** (Tarea, paso 2, descartado).

## 3 · Por qué la fusión declarada tampoco se ejecuta (Tarea, paso 3)

El paso 3 de la Tarea asume que, si no hay superación, hay una fusión ejecutable — "una sola tabla, con `sha256` de cada tabla origen citado y verificación de que ninguna fila de ninguna de las dos se perdió (diff fila por fila)". Esa asunción ya fue examinada y refutada, **antes** de que `ADR-91` (17/ago) reafirmara la firma de mesa `"fusionemos"` (`ADR-79(g)`, 12/ago) como condición de `FP-12`:

`forense/notas/2026-08-13-reconcilia-puertas.md` §2.1/§COMMIT-1, `ACTO RECONCILIA-PUERTAS` (13/ago/2026), verbatim: *"No hay colisión de esquema. Los dos artefactos no comparten una sola columna ni una sola llave — no hay fila de `UNIVERSO-MINIMO-FUENTE` que 'compita' con una fila de `universo-puertas`. Cualquier lectura que buscara 'fusionarlos' en una tabla única [...] estaría fusionando una receta con su propia bitácora de cumplimiento — formas distintas por diseño, no un accidente a corregir."* Ese mismo acto declaró explícitamente, en su cierre: *"No fusiona `UNIVERSO-MINIMO-FUENTE-v1_0.md` y `universo-puertas-2026-08-12.tsv` en un solo artefacto [...] muestra que no comparten esquema y que fusionarlos sería forzar una receta y su bitácora en una sola forma."*

**Re-verificado hoy, contra el árbol vigente (`35c9c9f`), y sigue siendo cierto:**
- `UNIVERSO-MINIMO-FUENTE-v1_0.md` sigue con 0 filas de datos — es prosa + una lista de 6 niveles, sin cambio desde el 13/ago salvo el propio archivo citado arriba (58 líneas, mismas).
- `universo-puertas-2026-08-14.tsv` (vigente al día de hoy, sucesor de la versión `2026-08-12` que la nota citaba) conserva el mismo esquema de 15 columnas — ninguna columna nueva introduce una llave compartida con `UNIVERSO-MINIMO-FUENTE`.
- Ninguna fila de `universo-puertas-2026-08-14.tsv` cita `UNIVERSO-MINIMO-FUENTE` como llave o identificador — las dos apariciones de la cadena "universo minimo" en el TSV (`puertas` `RNM_ENSAFI_2023_ficha992` y `RNM_ENFIH_2019_ficha709`, columna de nota libre) son **uso del método** (cuántas de las 6 piezas del universo mínimo satisfizo esa ficha), no una fila que represente el mismo objeto que `UNIVERSO-MINIMO-FUENTE` describe. Es exactamente el uso que `ACTO RECONCILIA-PUERTAS` ya documentó: "una receta y su bitácora de cumplimiento".

Forzar una fusión de todos modos produciría una tabla incoherente: filas de puertas (institución, url, veredicto) junto a un procedimiento de 6 pasos sin fila, sin llave y sin correspondencia — exactamente el defecto que `ACTO RECONCILIA-PUERTAS` se negó a cometer. El paso 3 de la Tarea, tal como está escrito, no es ejecutable sobre estos dos objetos: no es "fusión + diff sobre datos comparables", es forzar dos géneros de documento distintos en una sola forma.

## 4 · Adjudicación de `FP-12`

`FP-12` → **`CERRADA`**, sin fusión ejecutada y sin superación declarada. Ninguna de las dos vías de su propia Tarea aplica: no está superada (dominio distinto de los productos del barrido, §2) y la fusión declarada no es una operación coherente sobre estos dos artefactos (§3, ya establecido por `ACTO RECONCILIA-PUERTAS` el 13/ago y re-verificado aquí). La firma de mesa `"fusionemos"` (`ADR-79(g)`) y su reafirmación condicional (`ADR-91`) descansaban en una premisa — que las dos tablas son fusibles — que un acto anterior a la propia reafirmación ya había medido como falsa; ninguno de los actos que citó `FP-12` después (`ADR-91`, `ADR-101(h)`) volvió a leer esa nota antes de reafirmar la condición. Se cierra citando la evidencia, no se re-abre a mesa: no hay una decisión nueva que tomar sobre si fusionar o no — ya está medido que no se puede, por diseño de los dos objetos, no por falta de esfuerzo.

**Ninguno de los dos archivos origen se toca.** No se marca `SUPERADO POR` en `data/UNIVERSO-MINIMO-FUENTE-v1_0.md` ni en `data/universo-puertas-2026-08-14.tsv` — marcarlos así sería falso: no existe una tabla fusionada que los reemplace, y no debería existir una, según lo establecido en §3. No se crea `data/universo-fuentes-v1_0.md`/`.tsv` — sería el mismo defecto que `ACTO RECONCILIA-PUERTAS` ya rehusó cometer, con datos.

## 5 · Perímetro respetado

ESCRIBE (de este acto): esta nota · la fila `FP-12` de `forense/firmas-pendientes.tsv` · una línea en `forense/hallazgos.md`. NO ESCRIBE: `data/**` (ningún archivo tocado — la adjudicación no requirió escritura de datos), `canon/`, `tests/`, `milpa/` — igual que el perímetro del encargo declara. `FP-10` (adjudicación paralela, `FP10-PRECEDENCIA`, concurrente hoy) no se toca: distinta fila, distinto encargo, distinto perímetro.

## 6 · Cierre

`python3 tests/check.py --baseline` → **LÍNEA BASE: VERDE** antes y después de este acto (21 FAIL · 118 WARN, sin cambio — este acto no mueve ningún contador de la suite). Encargo `FUSION-PUERTAS` → `CONSUMIDO`. **Ningún contador de medición sobre México se mueve.**
