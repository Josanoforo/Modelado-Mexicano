# COMMIT-2 · cierre de MARCO-M-CORRIGE-Y-CENSA (ACTO C′)

`ACTO MAESTRA32-E15 · MARCO-M-CORRIGE-Y-CENSA-TRANSFERENCIA`, 31/ago/2026.
Corrida única siguiendo exactamente la receta de
`forense/notas/2026-08-31-marco-M-v1_1-spec.md` (COMMIT-1), sin
reescribirla sobre la marcha. Salida:
`forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv`, 8 filas de datos +
cabecera.

## Las dos correcciones (C1, C2), aplicadas y verificadas

**C1 (variable, `TRA-M-02`)**: `AP5_1_1` → `AP5_17|AP5_18`. Cita doble
verificada por lectura directa: `milpa/procedencia.yaml:888`
(`coeficientes_generador_medidos.G1_radio_confianza.fuente`) — *"reactivo
AP5_1_1/2/3 ... x desenlace tramite.mordida.discrecional (AP5_17 o
AP5_18='1', universo con contacto AP5_16_1..10)"* — y
`forense/notas/2026-08-04-w-coeficientes-generador-paso1.md:114-121,151` —
*"Desenlace: `tramite.mordida.discrecional` — compuesto: 1 si
`AP5_17='1'` **o** `AP5_18='1'` ... **C3:** `AP5_1_*` y `AP5_17`/`AP5_18`
son variables distintas"*. `AP5_1_1` es el primer ítem de la batería de θ
(confianza 0-10) del PREDICTOR, no el desenlace — exactamente el defecto
que describe el encargo.

**C2 (ponderador, `TRA-M-02`)**: `NO_ENCONTRADO_1944_LINEAS_REVISADAS` →
`FAC_SEL`. Cita verificada por lectura directa:
`forense/notas/2026-08-30-compuesta-spec.md:52` — *"Ponderador: **FAC_SEL**.
Estrato: `EST_DIS`. UPM: `UPM_DIS`. Fuente:
`forense/notas/2026-08-04-w-coeficientes-generador-paso1.md` §1.1/§3.1."*
— dentro de la sección `### G1.radio_confianza` de ese documento. El
universo de búsqueda de `MAESTRA32-E13` (`procedencia.yaml`, 1944 líneas,
+ `tramite.yaml`, 46) fue correcto para lo que buscó — el dato vive en un
tercer archivo, fuera de ese universo. `EST_DIS`/`UPM_DIS` (diseño de
estrato/UPM) no tienen columna propia en el esquema de `candidatos-marco-M`
— quedan citados en `razon`, no inventada una columna nueva fuera del
perímetro del objeto (`ola_calibracion, grado_sellado, grado_transferencia,
transferencia, razon`, cinco columnas, ninguna más).

**Inconsistencia observada, NO corregida** (fuera del alcance C1/C2):
`cv_arbitro` de `TRA-M-02` sigue `AP5_1_1/AP5_1_2/AP5_1_3` (la batería de
θ), ahora desalineada de `variable` ya corregida. Tocarla habría sido una
tercera corrección no autorizada por el encargo — queda declarada en la
columna `razon` de la fila, no silenciada.

`v1_0` queda intacto — ver INTOCABLES abajo (A.10).

## Método ejecutado (spec (a)-(e))

**(a)** `milpa/tramite.yaml:45` confirma `p: 0.62` con `clase: ASIGNADO`
para `paga_mordida`; `fuente:` en la línea 50 cita únicamente `ENCIG2023`
como ancla de encuesta/ola (ninguna otra candidata en esa lista) →
`ola_calibracion(tramite.mordida.discrecional) = ENCIG 2023`, fijada por
regla, no por adivinanza.

**(b)-(c)** Búsqueda por `variable_id` (comparación case-insensitive) sobre
la unión de los cuatro inventarios, filtrada por prefijo de familia del
campo `instrumento` (`encig`/`encuci`/`envipe`/`enif`), con una excepción
verificada para ENNViH/MxFLS (ver hallazgo cr27 abajo). Comando base:
`python3` leyendo cada TSV línea a línea, `csv`/split por `\t`, comparando
`variable_id.upper()` contra la lista cerrada de (b) del spec.

## A.13 — filas examinadas por inventario (comando, no estimación)

| inventario | archivo | filas de datos examinadas (sin cabecera/comentarios) |
|---|---|---|
| v1_2 | `data/inventario-reactivos-v1_2.tsv` | 178 247 |
| ext-v1_0 | `data/inventario-reactivos-ext-v1_0.tsv` | 63 346 |
| fd-v1_1 | `data/inventario-fd-v1_1.tsv` | 17 095 |
| fd-ext-v1_0 | `data/inventario-fd-ext-v1_0.tsv` | 10 636 |
| **total** | | **269 324** |

## Resultado por estadística de la lista cerrada (b)

**Categoría A — produce fila de tabla:**

- **`P8_3_1` (ENCIG, desenlace de `tramite.mordida.discrecional` vía
  `G1_confianza_institucional`)**: 36 filas con ese `variable_id` en todo
  el corpus; **6 filas tras el filtro de familia `encig*` y excluir la
  propia ola de calibración (2023)**: `encig2013` (1 fila, 1 payload),
  `encig2015` (3, 2 payloads), `encig2017` (3, 2 payloads), `encig2019`
  (3, 2 payloads), `encig2021` (7, 5 payloads), `encig2025` (5, 4 payloads).
  Las **30 filas restantes de las 36** son `elcos2012`, `endireh2016`,
  `enfih2019` — **colisión de mnemónico entre instrumentos distintos**
  (`P8_3_1` no significa lo mismo fuera de ENCIG; mismo patrón de riesgo
  que la colisión `AP7_1` ENCUCI/ENVIPE ya documentada en
  `procedencia.yaml:466-469`), descartadas por el filtro de familia de (c)
  del spec, no perseguidas por `texto_reactivo` (vacío en el 100% de las
  filas de método `INSPECT_ZIP`, verificado). → **6 filas nuevas**
  `TRA-M-03`..`TRA-M-08`.
- **`AP5_17`/`AP5_18` (ENCUCI, desenlace vía `G1_radio_confianza`)**: 1
  fila cada una en todo el corpus, ambas en el único payload
  `BD_ENCUCI2020_dbf.zip` (`encuci2020`) — **cero colisiones, cero otras
  olas**: ENCUCI no tiene una segunda ola en este corpus (consistente con
  `VERIFICACIÓN §2(iii)` del encargo, que solo nombra `ENCUCI 2020`). →
  **0 filas nuevas** (la única transferencia de esta estadística ya es
  `TRA-M-02`, transferencia DE INSTRUMENTO contra `ENCIG 2023`, corregida
  arriba).

**Categoría B — buscada, censada aquí, NO produce fila de tabla** (spec
(e): ninguna de estas tres estadísticas tiene una regla compilada en
`milpa/*.yaml` — verificado `ls milpa/*.yaml` → solo `procedencia.yaml`,
`refutations.yaml`, `tramite.yaml`; confirmado además por el propio cierre
de `MAESTRA32-E13`, que documentó que `cargar_reglas()` solo carga el
dominio `tramite`):

- **`BP1_23` (ENVIPE, desenlace compartido de `G4_exposicion_violencia` y
  `G4_confianza_institucional_justicia`, calibración ENVIPE 2025)**: 49
  filas en total, **todas** dentro de la familia `envipe*` (cero
  colisiones cross-familia) — **13 olas distintas de 2025**: 2012-2024,
  cada una con payload propio (`bd_envipe...`, mayoría con variante
  `_csv`). `envipe2011` **excluida** deliberadamente: su `variable_id` real
  es `BP1_23_1`/`BP1_23_2` (ítem desdoblado), no coincide con `BP1_23`
  exacto — el id cambió de forma entre 2011 y 2012, límite declarado en
  spec (c) (sin `texto_reactivo` para verificar por sinónimo).
- **`p4_10`/`P4_10` (ENIF, desenlace de `G3_familismo_apoyo`, calibración
  ENIF 2024)**: 71 filas con ese `variable_id` en todo el corpus; **1 fila
  tras el filtro de familia `enif*`** y excluir la ola de calibración
  (2024): `enif2021` (`enif_2021_bd_csv.zip`). Las **70 filas restantes**
  son colisión de mnemónico masiva y cruda: `elcos2012`, `enasic2022`,
  `encig2011`, `endireh2006`, `enfih2019`, `enpol2021`, y **siete olas de
  MOCIBA** (2015, 2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024, 2025) —
  `P4_10` es un mnemónico genérico (pregunta 4, ítem 10) que se repite por
  coincidencia posicional en decenas de instrumentos no relacionados; el
  filtro de familia de (c) las descarta correctamente, dato que por sí
  solo justifica exigir prefijo de familia y no solo `variable_id` pelado.
- **`cr27` (ENNViH/MxFLS, desenlace del par sellado `G3.horizonte_temporal`
  vía `CAL-G3`, calibración olas 2-3 = 2005-06→2009-12)**: **6 filas, 3
  payloads** — `ennvih/ehh02dta_all.zip` (2 filas: `iiib_cr.dta`,
  `p_cr.dta`), `ennvih/ehh05dta_all.zip` (2 filas), `ennvih/ehh09dta_all.zip`
  (2 filas). Las tres traen `instrumento = "(sin-instrumento-derivable)"`
  en el inventario (la etiqueta v1_2 no resolvió nombre+ola para ENNViH,
  a diferencia de ENCIG/ENCUCI/ENVIPE/ENIF) — el filtro de prefijo de (c)
  NO las habría encontrado; se identificaron por `payload_id` (`ennvih/
  ehh0Ndta_all.zip`) cruzado contra `data/manifiesto.yaml:468-533`, que
  nombra `ehh02` = `ennvih1_2002_hogar_dta` (**ENNViH-1, 2002, ola 1**),
  y contra `forense/notas/2026-08-24-cal-g3-puntual-cierre.md:34-46`, que
  usa `ehh05`/`ehh09` para las olas 2 (2005-06) y 3 (2009-12) — las
  MISMAS dos olas de `ola_calibracion`. **Resultado real: 1 ola distinta
  de la calibración (ENNViH-1, 2002/ola 1) — no 0.** `texto_reactivo` SÍ
  está poblado aquí (`"TIENE AHORROS"`/`"TIENE AHORROS?"`, método
  `INSPECT_STATA`, no `INSPECT_ZIP`) — confirma semánticamente que es el
  mismo reactivo, sin depender solo del `variable_id`.

**Nota de honestidad de proceso**: una primera pasada de este acto, filtrando
únicamente por `instrumento.lower().startswith("ennvih")`, dio **0** hits
para `cr27` — resultado que se habría reportado como "familia ausente del
corpus" si no se hubiera verificado por `payload_id` como respaldo (el
mismo tipo de verificación cruzada que exige A.13 para todo negativo). El
negativo original era producto de un filtro que no examinó la forma real
del campo `instrumento` para esa familia, no una ausencia real — corregido
antes de escribir esta nota, no después.

## Conteo — B-bis

`transferencia=SI` en la tabla resultante: `TRA-M-02` (transferencia de
instrumento, ENCUCI↔ENCIG) + `TRA-M-03`..`TRA-M-08` (transferencia de ola,
ENCIG 2013/2015/2017/2019/2021/2025) = **7 celdas**. `TRA-M-01` es
`transferencia=NO` (es la propia ola de calibración). Categoría B (14
hallazgos: 13 BP1_23 + 1 p4_10; el hallazgo de `cr27` es un hallazgo, no
una fila — ver arriba) NO cuenta para este umbral (spec (e): no son
ejecutables por `emitir_binaria`, contarlas sería falso positivo de "el
marco-M puede crecer").

**Veredicto B-bis: `1-7` → corto.** Las 7 celdas nombradas arriba (`TRA-M-02`,
`TRA-M-03`, `TRA-M-04`, `TRA-M-05`, `TRA-M-06`, `TRA-M-07`, `TRA-M-08`) no
alcanzan el umbral `≥8` de "el marco-M puede llegar a tamaño de sorteo real
bajo D-D" — el tamaño de sorteo seguirá dependiendo, como con `N_elegibles=2`
de `MAESTRA32-E13`, de la regla de `<15 → identidad` si D-D habilita estas
celdas sin sumar más.

## CONTADOR

Celdas de transferencia encontradas: **N = 7** (incluido en la tabla,
`transferencia=SI`) · defectos de v1_0 corregidos con cita: **2** (C1, C2 —
ambos sobre `TRA-M-02`).

## `grado_dependencia` — NO tocado, D-D sigue pendiente

`TRA-M-01`/`TRA-M-02` conservan `P1` (la desviación declarada de
`MAESTRA32-E13`, intacta). Las 6 filas nuevas llevan `grado_dependencia =
PENDIENTE-D-D` — asignarles `P0`/`P1` habría sido adjudicar la misma
decisión de mesa que el encargo explícitamente reserva. `grado_sellado` (la
columna nueva que SÍ deriva mecánicamente de
`forense/notas/2026-08-20-act-pil-2-marco.md:125`) queda `P0` para
`ENCIG 2021/2023` y `ENCUCI 2020` (los tres pares nombrados literalmente en
la lista P0 que tocan este censo) y `P1` para `ENCIG 2013/2015/2017/2019/2025`
(misma familia, otra ola, no nombrados en la lista).

## INTOCABLES — verificación final

```
$ git diff --stat main -- forense/prereg-duelo-v2/candidatos-marco-M-v1_0.tsv \
    forense/prereg-duelo-v2/marco-M-congelado-v1_0.tsv \
    forense/prereg-duelo-v2/marco-M-sorteado-v1_0.tsv \
    forense/prereg-duelo-v2/CONGELADO-M-v1_0.sha256 \
    forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv \
    forense/prereg-duelo-v2/sorteo_v2.py \
    forense/prereg-duelo-v2/tests_sorteo_v2.py \
    forense/prereg-duelo-v2/sorteo_marco_m.py \
    forense/prereg-duelo-v2/tests_sorteo_marco_m.py \
    milpa/
(sin salida -- ninguno de estos archivos cambió)
```

## Lo que este acto NO hizo (recordatorio del objeto)

No congeló v1_1, no sorteó, no emitió M, no calculó R, no decidió
`grado_dependencia`, no editó `v1_0`. Sucesores declarados en el encargo
(`MARCO-M-CONGELA-v1_1`/`MARCO-M-SORTEA-v1_1` con D-D dentro, `EMITE-M`,
`R-MARCO-M`, `L-MARCO-M`) siguen sin lanzar.
