# Nota · ACTO SELLA-AGO25-F (continuación) — la hoja de las diez letras, ejecutada

25/ago/2026. Entorno **NUBE** (`cloud_default`). Modelo Opus. Rama `claude/encargo-1-sella-ago25-f-75gu88`. Encargo: `forense/encargos/2026-08-25-SELLA-AGO25-F-HOJA.md`. Continúa directamente `ADR-165`/`forense/notas/2026-08-25-sella-f.md`, que reportó las ocho letras originales sin ruling verbatim en el árbol — la hoja llegó después, con esas ocho resueltas y dos nuevas (`L9`/`L10`, de `ACTO BIBLIOTECARIO-56`).

## 1 · ARRANQUE

Mismo SHA que `ADR-165` (`origin/main = 8aff7cb`, sin movimiento entre los dos actos). CONTADOR: cero directo. `data/raw`: no aplica. Entorno: NUBE, sonda saltada. Espejo: nada.

## 2 · Letra por letra

### L1/`FP-127`, opción `b` — "mantener con nota + acto de escalas"

El β de `CAL-G3-PUNTUAL` (+0.0146, signo opuesto al `−0.60` asignado) **no se toca**: sigue `PROPUESTO`, sin escribir en `milpa/procedencia.yaml`. Se añade `forense/registro-llaves-identificacion-v1_0.md §11`: nota descriptiva `MEDIDO·ACOTADO` (etiqueta de este registro, no una clase nueva de `milpa/`) junto a la fila `CAL-G3`, y discrepancia de signo declarada explícitamente al lado del `−0.60` que cita esa misma fila. Fila nueva `FP-135`, `FIRMADA`, sin ejecutar: el acto `ESCALA-ASIGNADOS` que declare la escala de los 15 coeficientes `ASIGNADO` de `milpa/procedencia.yaml`.

### L2/`FP-128`, sí

`forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md`: cabecera cambia de "PROPUESTA (no sellada)" a "SELLADA", con una línea fechada nueva citando esta firma. El cuerpo operativo (§0 en adelante) no se toca. `FP-128` cierra `FIRMADA`, `ejecutada_en` = 25/ago/2026.

### L3/`FP-129`, opción `b` y L4/`FP-130`, opción `a`

`forense/ficha-r34-conda-v2-spec.md §9` (nueva, append-only — §1-§8 intactos):

- **L4=`a`.** Grep de «activas» sobre el archivo: **4 coincidencias** (líneas 82, 93, 95, 101), verificado antes de escribir la enmienda. Las cuatro viven dentro de §3, en el razonamiento que ya **descartaba** el constructo (iii) («cuentas activas trimestrales... NO EXISTE») y elegía (ii) («cuentas que utilizaron CoDi durante el trimestre»). **Cero sitios vivos que enmendar** — el término sellado que la ficha usa ya era el textual antes de esta firma; L4 confirma la elección como decisión de mesa, no como cautela del acto.
- **L3=`b`.** Mesa rechaza declarar función de enlace `cuenta↔persona` (opción `a`, que `A-bis regla 3` prohibiría de todos modos sin ella) y rechaza dejar la condición A congelada en fila A3 sin veredicto (opción `c`, el estado que la ficha traía). Ordena re-especificar **ambos lados en la misma unidad**, buscando en los Informes Banxico ya adquiridos (los mismos IdMF que §3 ya cita) una serie que reporte el mismo constructo para CoDi y SPEI sin mezclar cuentas con personas físicas. Esta ficha no localiza esa serie — es trabajo del acto sucesor. Fila nueva `FP-136`, `FIRMADA`, sin ejecutar.
- `FP-104` se actualiza (columna `qué_se_firma`, apéndice fechado) citando ambas letras; sigue `ABIERTA` — la fila `A3` de §5 de la ficha no se retira hasta que `FP-136` produzca la serie homogénea.

### L5/`FP-63`, sí

La cadena verbatim `AUTORIZO DESTRUIR mm-purga.git` llega en el mensaje de la hoja como autorización dada de mesa — primera vez que aparece así en todo el árbol; hasta hoy solo existía dentro de la definición de la propia compuerta (`forense/notas/2026-08-19-fp63-verificacion-espejo.md:267`, `forense/notas/2026-08-19-caja-residuos-cierre.md:93`, `canon/gobernanza-v1_15.md:2349,2409`). Se registra en `ADR-166` (`canon/gobernanza-v1_15.md`). **No se ejecuta ninguna acción destructiva desde NUBE** — la instrucción del propio acto (L5: "NO destruyas desde NUBE") se respeta. Fila nueva `FP-137`, `FIRMADA`, entorno **UBUNTU**, `ejecutada_en` vacío: ejecutar la destrucción con la cadena citada, cuando corra en el entorno correcto.

### L6/`FP-24`, "firmar la propuesta"

Verificado contra el árbol antes de escribir nada: **esta letra ya está ejecutada.** `FP-24` está `FIRMADA` desde `ADR-93` (17/ago/2026, `PR #249`) — la política de pares de `ENLACE-2` ya es texto canónico. Y su ejecución concreta sobre las 20 filas con par de `data/curacion-registro/relaciones.tsv` **ya corrió**, el 18/ago/2026: `FP-46` (verificada en el tablero, `ejecutada_en` lleno) cita `ADR-109`/`PR #268`/`ACTO B2-SEMANTICO`, que adjudicó las 20 filas por la condición literal de `ADR-93` sobre material E2 — ENFIH (8) y ENBIARE (3) satisfacen la regla (existe entrada distinta del manifiesto, `enfih2019_bd_csv_zip` y `enbiare2021_bd_csv_zip`, que evidencia el mismo objeto: 527 y 305 nombres comunes), ENSAFI (9) no la satisface (una sola entrada en todo el manifiesto). **Ninguna acción nueva se ejecuta para esta letra** — mesa reafirma una decisión ya sellada y ya ejecutada; ninguna fila del tablero se toca.

*(Nota metodológica: un cruce directo de `data/curacion-registro/relaciones.tsv` por `necesidad_id`+`fuente` no reproduce en esta sesión los conteos exactos "ENSAFI 9 · ENFIH 8 · ENBIARE 3" que `FP-24`/`FP-46` citan — el esquema del archivo pudo cambiar desde el 18/ago. No se reabre la adjudicación de `FP-46` sobre esa base: la fila ya tiene `ejecutada_en` con cita verificable a un ADR real, y reabrirla sin evidencia de que esté mal sería exactamente el tipo de sobre-corrección que este programa evita. Se declara la discrepancia de conteo para quien audite `FP-46` directamente, no se actúa sobre ella aquí.)*

### L7/`FP-131`, sí

`forense/notas/2026-08-25-eval-compartamos.md §7.1`: cabecera de la sección pasa de "PROPUESTA MÍNIMA — escrita, no implementada" a "PROPUESTA-SELLADA, 25/ago/2026 (`ACTO SELLA-AGO25-F`, L7/`FP-131`, firma de mesa verbatim "sí") — escrita, no implementada". El texto de las tres piezas de la propuesta (§7.1, numerales 1-3) no se toca. `FP-131` cierra `FIRMADA`, `ejecutada_en` = 25/ago/2026. No se implementa código en `milpa/`: fila nueva `FP-138`, `FIRMADA`, sin ejecutar.

### L8/`FP-132`, "el que el acto propuso"

El único candidato que `ACTO EVAL-COMPARTAMOS-LLAVE3` dejó nombrado sin afirmar (§8 de su nota) es el parecido entre `Q15_2_mean_formal`/`Q15_2_mean_people` (reactivos del brazo de seguimiento del RCT de Compartamos) y `confianza_institucional` (`G1`)/`radio_confianza` (`G1`,`G5`) del modelo. Mesa toma ese candidato por instrucción directa — asumiendo el riesgo que el acto se negó a asumir solo, que es exactamente la clase de decisión que `ADR-57(c)` reserva a mesa. Registrado en `forense/registro-llaves-identificacion-v1_0.md §12`, citando esta firma. **No ejerce la llave**: `preregistro_ref` de `EXP-COMPARTAMOS-1` sigue `NINGUNO` — falta abrir el reactivo, verificar escala/universo, y escribir la spec B-bis, trabajo de un acto propio. `FP-132` cierra `FIRMADA` como decisión de mesa; la llave sigue `SELLADA_NO_EJERCIDA`.

**`data/curacion-registro/necesidad-objeto-modelo.tsv` no se edita.** Verificado: sus 37 filas no tienen una fila para `confianza_institucional`(`G1`)/`radio_confianza`(`G1`,`G5`) a la que asignar esta fuente. Crear una fila ahí es un acto de curación de datos con su propio proceso — escribirla aquí, sin ese proceso, fabricaría una fila del curador por fuera de su propio mecanismo. Se declara pendiente para el acto de curación, no se fabrica.

### L9/`FP-133`, opción `c`

El marco de candidatas del piloto (60 filas / 50 puntuables) **no se poda ni se re-congela**. Mesa ordena que `ACT-PIL-3` (el sorteo, aún sin correr) se diseñe para que su propio mecanismo respete el tope del 20% de candidatas publicadas sin tirar filas `SI` del marco existente. `FP-133` cierra `FIRMADA`, `ejecutada_en` = 25/ago/2026 (decisión registrada). El rediseño del sorteo mismo no se ejecuta aquí — fila nueva `FP-139`, `FIRMADA`, sin ejecutar.

### L10/`FP-134`, opción `a`

Las 8 filas del marco que el diseño de dos pasos de `FP-93` no alcanza por construcción (`DIN-07`, `DIN-08`, `DIN-09`, `DIN-10`, `DIN-12` — Encuesta de Competencias Financieras, Banxico/CNBV; `DOC-03`, `DOC-05`, `DOC-06` — CNBV/BMV/HR Ratings) se extienden con un segundo universo de búsqueda propio de esas fuentes, en vez de marcarse no-evaluables. `FP-134` cierra `FIRMADA`, `ejecutada_en` = 25/ago/2026. Construir el índice nuevo no se ejecuta aquí — fila nueva `FP-140`, `FIRMADA`, sin ejecutar.

## 3 · Actualizaciones al tablero (`forense/firmas-pendientes.tsv`)

- `FP-127`, `FP-128`, `FP-129`, `FP-130`, `FP-131`, `FP-132`, `FP-133`, `FP-134`: `ABIERTA` → `FIRMADA`, con `firmada_en` (cita verbatim de la hoja) y `ejecutada_en` llenos.
- Seis filas nuevas, todas `FIRMADA` con `ejecutada_en` vacío: `FP-135` (escalas de asignados), `FP-136` (serie homogénea Banxico), `FP-137` (destrucción UBUNTU de `mm-purga.git`), `FP-138` (hook en `milpa/`), `FP-139` (rediseño del sorteo), `FP-140` (segundo índice Banxico/CNBV/BMV).
- `FP-104`, `FP-63`: nota fechada añadida, `estado` sin cambio.
- `FP-24`, `FP-46`: sin cambio — ya resueltas antes de este acto.
- 141 filas de datos.

## 4 · ADR y cascada

`ADR-166` (`canon/gobernanza-v1_15.md`), candidateado contra el máximo verificado (`165`, `ADR-165`, mismo acto): único `166`, sin huecos → `166`, a re-verificar por quien fusione. `canon/estado-programa-v1_10.md`: conteo de ADR recifrado `165→166`, línea `L0` y línea de suite actualizadas.

## 5 · Tests

`CHECK_SELFCHECK_CHILD=1 python3 tests/check.py --baseline`:

```
19 FAIL · 139 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

`T22` neto **−2**: ocho filas salen de la rama (a) (`ABIERTA`) con `ejecutada_en` lleno; seis filas nuevas entran a la rama (c) (`FIRMADA` sin ejecutar). Ninguna otra categoría se mueve.

## 6 · Perímetro respetado

Tocado: `forense/firmas-pendientes.tsv`, `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md` (cabecera), `forense/ficha-r34-conda-v2-spec.md` (§9, nueva), `forense/registro-llaves-identificacion-v1_0.md` (§§11-12, nuevas), `forense/notas/2026-08-25-eval-compartamos.md` (cabecera §7.1), `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`, esta nota, el encargo.
No tocado: `milpa/` (ningún archivo), `data/curacion-registro/relaciones.tsv`, `data/curacion-registro/necesidad-objeto-modelo.tsv`, `data/diseno-muestral.yaml`, `forense/marco-candidatas-piloto-v1_0.tsv`.

## 7 · Para mesa

- **`FP-135`-`FP-140`** son seis actos sucesores nuevos, todos `FIRMADA` sin ejecutar: escalas de asignados, serie homogénea CoDi/SPEI, destrucción de `mm-purga.git` (requiere UBUNTU), hook del motor en `milpa/`, rediseño del sorteo de `ACT-PIL-3`, segundo índice Banxico/CNBV/BMV.
- **`FP-104`** sigue `ABIERTA`: la condición A de R3.4 no re-corre hasta que `FP-136` entregue la serie homogénea.
- **La discrepancia de conteo en `L6`/`FP-24`** (§2 arriba) queda declarada para quien audite `FP-46` directamente — no se reabre aquí sin evidencia de que la adjudicación ya ejecutada esté mal.
