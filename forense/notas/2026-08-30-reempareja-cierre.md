# Nota de cierre · MAESTRA32-E4 · RE-EMPAREJA · COMMIT-2

Corrida única de `tools/reempareja.py` (congelado en COMMIT-1, `forense/notas/2026-08-30-reempareja-spec.md`) contra `data/inventario-reactivos-v1_2.tsv` ∪ `data/inventario-reactivos-ext-v1_0.tsv` ∪ `data/inventario-fd-v1_1.tsv`:

```
$ python3 tools/reempareja.py
```

Salida completa (stdout+stderr) preservada íntegra abajo — el primer y único resultado que produjo el procedimiento, per B-bis. Escribió `data/emparejamiento-motor-v1_2.tsv`.

## Resultado — 2 de 9 `EXISTE-SATISFACE` nuevo

**`G5.familismo_apoyo`** y **`G5.radio_confianza`** suben a `EXISTE-SATISFACE`, ambos co-observados en `endireh2016`; `G5.familismo_apoyo` además co-observa en `eder2017`. Los 7 pares restantes no llegan a `EXISTE-SATISFACE`. Detalle por par abajo (§ Tabla de deltas).

## A.13 · Filas examinadas por tabla

```
inventario-reactivos-v1_2:     178246 filas de datos (3 líneas de comentario + 1 encabezado)
inventario-reactivos-ext-v1_0:  63345 filas de datos (4 líneas de comentario + 1 encabezado)
inventario-fd-v1_1:             17094 filas de datos (3 líneas de comentario + 1 encabezado)
universo total examinado:      258685 filas
```

Cada una de las 258,685 filas se corrió contra las listas cerradas de término de los 9 pares, vía `id` y vía `texto`, exactamente como en la re-corrida de E6 (`forense/notas/2026-08-30-etiqueta-v1_2-cierre.md:110-399`) — comando y conteo re-derivados arriba, no heredados. Ningún negativo de este acto (p. ej. `G2.aversion_riesgo` → `NO-ENCONTRADO`) se declara sin este universo al lado (A.4/A.13).

## Tabla de deltas por par (`v1_1` → `v1_2`, universo declarado arriba)

Veredicto de `v1_1` re-derivado por comando directamente de `data/emparejamiento-motor-v1_1.tsv` (archivo intocable, solo leído) con la misma función `veredicto_par` — no heredado de la nota de cierre de E6, para no propagar un error de transcripción:

| par | veredicto `v1_1` | veredicto `v1_2` | movimiento | co-observación `v1_2` |
|---|---|---|---|---|
| `G5.familismo_apoyo` | `EXISTE-NO-SATISFACE` | **`EXISTE-SATISFACE`** | SUBE | `eder2017`, `endireh2016` |
| `G5.radio_confianza` | `EXISTE-NO-SATISFACE` | **`EXISTE-SATISFACE`** | SUBE | `endireh2016` |
| `G5.familismo_obligacion` | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` | igual | — |
| `G2.sens_estatus` | `NO-ENCONTRADO` | `EXISTE-NO-SATISFACE` | SUBE | — |
| `G2.aversion_riesgo` | `NO-ENCONTRADO` | `NO-ENCONTRADO` | igual | — |
| `G3.aversion_riesgo` | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` | igual | — |
| `G4.horizonte_temporal` | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` | igual | — |
| `G4.sens_estatus` | `NO-ENCONTRADO` | `EXISTE-NO-SATISFACE` | SUBE | — |
| `G6.deferencia` | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` | igual | — |

**B-bis verificado, no violado:** las 9 filas suben o quedan iguales, ninguna baja. 2 pares llegan a `EXISTE-SATISFACE` (0 antes); 2 pares suben de `NO-ENCONTRADO` a `EXISTE-NO-SATISFACE` (`G2.sens_estatus`, `G4.sens_estatus` — ambos por el mismo hit: 2 filas `(sin-instrumento-derivable)` de la tabla ext que matchean "estatus" vía `texto`, sin co-observación por carecer de instrumento identificado); 5 pares quedan exactamente igual. El pre-registro de (d) en `forense/notas/2026-08-30-reempareja-spec.md` se cumplió: no hubo PARO.

## Candidatos nuevos por par y por tabla de origen (`v1_2` vs `ext`)

Control positivo primero: los candidatos de tabla `inventario-reactivos-v1_2` (34) e `inventario-fd-v1_1` (136) en la salida de este acto son **idénticos en conteo** a los de `data/emparejamiento-motor-v1_1.tsv` (34 y 136 respectivamente, comando `csv.DictReader` + filtro `veredicto_candidato=='CANDIDATO'` agrupado por `tabla`) — cero candidatos nuevos ni perdidos de esas dos tablas, como exige (d). Los **545** `DESCARTADO-con-razón` tampoco cambian de conteo (`v1_1`: 545; `v1_2`: 545) — ninguna de las 481 filas nuevas de `ext` cayó en una clave ya registrada de `DESCARTES` (que empareja por `(variable_id, instrumento, término)` exacto). Todo candidato nuevo, sin excepción, viene de `inventario-reactivos-ext-v1_0`:

| par | candidatos `v1_2`(reactivos) | candidatos `fd-v1_1` | candidatos `ext-v1_0` (nuevos) | de esos, `ext` sin instrumento |
|---|---|---|---|---|
| `G5.familismo_apoyo` | 1 | 44 | **142** | 76 |
| `G5.radio_confianza` | 28 | 41 | **143** | 76 |
| `G5.familismo_obligacion` | 1 | 36 | **138** | 76 |
| `G2.sens_estatus` | 0 | 0 | **2** | 2 |
| `G2.aversion_riesgo` | 0 | 0 | **0** | 0 |
| `G3.aversion_riesgo` | 0 | 13 | **52** | 52 |
| `G4.horizonte_temporal` | 0 | 2 | **0** | 0 |
| `G4.sens_estatus` | 0 | 0 | **2** | 2 |
| `G6.deferencia` | 4 | 0 | **2** | 0 |
| **total** | **34** | **136** | **481** | **284** |

`481` candidatos nuevos en total, `170` heredados sin cambio (`34+136`) → `651` `CANDIDATO` en `data/emparejamiento-motor-v1_2.tsv` (`545` `DESCARTADO-con-razón` + `651` `CANDIDATO` = `1196` filas totales, `wc -l` = `1208` con las 12 líneas de cabecera/comentario). `0` `CIRCULAR-EXCLUIDO` en ambas corridas.

**Candidatos de `ext` que caen en filas sin instrumento (`(sin-instrumento-derivable)`): 284 de 481 (59.0%).** Esas 284 nunca pueden por sí solas mover un par a `EXISTE-SATISFACE` (§4 de la spec exige instrumento identificado) — son el techo de etiqueta declarado por la dirección en el encargo, ahora cuantificado por par: domina en `G5.familismo_apoyo`/`radio_confianza`/`familismo_obligacion` (76 cada uno, mismas filas de desenlace compartidas por los tres pares G5) y en `G3.aversion_riesgo` (52, el 100% de sus candidatos nuevos — este par sigue en `EXISTE-NO-SATISFACE` en vez de subir más porque **todos** sus candidatos de `ext` carecen de instrumento).

## Detalle de los 2 `EXISTE-SATISFACE` nuevos — lectura del recorte (spec §3.2)

**`G5.familismo_apoyo` × `eder2017`** (Encuesta Demográfica Retrospectiva 2017): θ = `financia_8` "Préstamo familiar" (término `préstamo familiar`, 2 filas vía id+texto sobre el mismo `variable_id`); desenlace = batería extensa de `corresidencia` (`padre_cor`/`madre_cor`/`hnos_cor`/`suegro_cor`/`suegra_cor`/`hij_cor_1..15`/`cor_union1..6`/`parien_cor`, todas "Corresidencia con —"). Lectura del recorte: coherente y limpio — `eder2017` es una encuesta dedicada a transiciones familiares/hogar, "préstamo familiar" y una batería completa de corresidencia con cada tipo de pariente son operacionalizaciones directas de familismo de apoyo y de hogar extendido, sin homónimo aparente.

**`G5.familismo_apoyo`/`G5.radio_confianza` × `endireh2016`** (Encuesta Nacional sobre la Dinámica de las Relaciones en los Hogares 2016): θ de `familismo_apoyo` = `p4_8_2`/`p4_8_3` "¿usted recibe dinero de familiares...?" — lectura limpia. θ de `radio_confianza` = 5 filas `p6_24_10`/`p7_27_10`/`p8_19_10`/`p10_15_10`/`p13_21_13`, todas la misma frase repetida por módulo: *"No acudió a una autoridad o institución no confía en las autoridades del gobierno"* (razón de no denunciar violencia). Desenlace compartido = `p3_2`/`p4ab_2` "¿Su actual esposo o pareja vive con usted? / ¿desde cuándo NO vive con usted?" y `p18_4` "¿Usted cuida a sus nietos(as) o sobrinos(as)…?".

**RESERVA declarada, no bloqueante — homónimo probable sin cribar en `endireh2016`:** `p18_4` (cuidado de nietos/sobrinos) y `p4_8_2`/`p4_8_3` (dinero de familiares) leen limpio. Pero `p6_24_10`/etc. ("confía en las autoridades del gobierno") mide **confianza institucional** — un constructo ya modelado aparte en el ejecutable (`G4.confianza_institucional[justicia]`, `FP-185`) — no "radio de confianza interpersonal" (círculo de amistades/vecinos/desconocidos, ancla `ENCUCI 2020 SEC_4_5 AP5_1_1-3`, `milpa/procedencia.yaml:280-293`); y `p3_2`/`p4ab_2` ("¿su esposo vive con usted?") preguntan residencia conyugal en contexto de violencia doméstica, no "hogar extendido"/corresidencia con familia ampliada. Ambos leen como el mismo tipo de homónimo que `DESCARTES` ya excluyó en otras filas (p. ej. `P2_6_3`/`enut2019`/"cuidador" — cuidador contratado, polo opuesto de carga de cuidado familiar) — pero `DESCARTES` empareja por `(variable_id, instrumento, término)` exacto, así que no puede cubrir automáticamente filas nuevas de `endireh2016` con `variable_id` distinto, aunque el patrón sea el mismo. Esta lectura es un spot-check de este cierre, no una recuración de `DESCARTES` — no re-etiqueta la tabla ext ni cambia el veredicto (`0` cambios a criterios, per COMMIT-1(b)); el veredicto mecánico `EXISTE-SATISFACE` se reporta tal cual produjo el procedimiento congelado. Pero un medidor de caja sucesor sobre `G5.radio_confianza` en particular **no debe correr β̂ directo sobre `endireh2016` sin antes hacer la misma curación manual de homónimo que E2 ya hizo para `v1_2`/`fd-v1_1`** — riesgo concreto: si el único instrumento co-observado resulta ser homónimo, el par vuelve a `EXISTE-NO-SATISFACE` real. `G5.familismo_apoyo` es más robusto porque co-observa también en `eder2017`, que no muestra este problema.

## Intocables — `git diff --stat` vacío, verificado

```
$ git diff --stat -- data/emparejamiento-motor-v1_0.tsv data/emparejamiento-motor-v1_1.tsv \
    data/inventario-reactivos-v1_2.tsv data/inventario-reactivos-ext-v1_0.tsv \
    data/inventario-fd-v1_1.tsv forense/notas/2026-08-28-empareja-spec.md \
    tools/etiqueta_v1_2.py tools/inventario_reactivos_ext.py
(sin salida)
```

## CONTADOR

Pares con `EXISTE-SATISFACE` nuevo: **2 de 9** (`G5.familismo_apoyo`, `G5.radio_confianza`, con la reserva de homónimo declarada arriba sobre `endireh2016`). Candidatos nuevos aportados por la tabla ext: **481** (`284` sin instrumento, `197` con instrumento identificado).

## Salida cruda del script (única corrida, `python3 tools/reempareja.py`)

```
# G5.familismo_apoyo: theta hits id=0 texto=12 | desenlace hits id=2 texto=176
# G5.radio_confianza: theta hits id=27 texto=11 | desenlace hits id=2 texto=176
# G5.familismo_obligacion: theta hits id=0 texto=0 | desenlace hits id=2 texto=176
# G2.sens_estatus: theta hits id=253 texto=12 | desenlace hits id=0 texto=0
# G2.aversion_riesgo: theta hits id=0 texto=0 | desenlace hits id=0 texto=0
# G3.aversion_riesgo: theta hits id=0 texto=0 | desenlace hits id=1 texto=67
# G4.horizonte_temporal: theta hits id=0 texto=8 | desenlace hits id=0 texto=0
# G4.sens_estatus: theta hits id=253 texto=12 | desenlace hits id=0 texto=0
# G6.deferencia: theta hits id=4 texto=2 | desenlace hits id=0 texto=0

# ===== veredicto A.4 por par (co-observación exige instrumento identificado, NO '(raiz)'/'(sin-instrumento-derivable)') =====
G5.familismo_apoyo: theta_candidatos_reales=12 (instrumentos=['eder2017', 'endireh2016', 'enfih2019', 'enif2015', 'enif2024', 'enut2019', 'enut2024'], +placeholder=[]) | desenlace_candidatos_reales=175 (instrumentos=['eder2017', 'elcos2012', 'enasem2018', 'enasem2021', 'enasem2024', 'enasic2022', 'endireh2016'], +placeholder=['(sin-instrumento-derivable)']) | co_observacion_instrumento_identificado=['eder2017', 'endireh2016'] | veredicto=EXISTE-SATISFACE
G5.radio_confianza: theta_candidatos_reales=37 (instrumentos=['encup2012', 'endireh2016', 'enif2012', 'enif2015'], +placeholder=[]) | desenlace_candidatos_reales=175 (instrumentos=['eder2017', 'elcos2012', 'enasem2018', 'enasem2021', 'enasem2024', 'enasic2022', 'endireh2016'], +placeholder=['(sin-instrumento-derivable)']) | co_observacion_instrumento_identificado=['endireh2016'] | veredicto=EXISTE-SATISFACE
G5.familismo_obligacion: theta_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | desenlace_candidatos_reales=175 (instrumentos=['eder2017', 'elcos2012', 'enasem2018', 'enasem2021', 'enasem2024', 'enasic2022', 'endireh2016'], +placeholder=['(sin-instrumento-derivable)']) | co_observacion_instrumento_identificado=[] | veredicto=EXISTE-NO-SATISFACE
G2.sens_estatus: theta_candidatos_reales=2 (instrumentos=[], +placeholder=['(sin-instrumento-derivable)']) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[] | veredicto=EXISTE-NO-SATISFACE
G2.aversion_riesgo: theta_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[] | veredicto=NO-ENCONTRADO
G3.aversion_riesgo: theta_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | desenlace_candidatos_reales=65 (instrumentos=['enfih2019', 'enif2012', 'enif2015', 'enif2018', 'enif2024'], +placeholder=['(sin-instrumento-derivable)']) | co_observacion_instrumento_identificado=[] | veredicto=EXISTE-NO-SATISFACE
G4.horizonte_temporal: theta_candidatos_reales=2 (instrumentos=['enif2018', 'enif2024'], +placeholder=[]) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[] | veredicto=EXISTE-NO-SATISFACE
G4.sens_estatus: theta_candidatos_reales=2 (instrumentos=[], +placeholder=['(sin-instrumento-derivable)']) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[] | veredicto=EXISTE-NO-SATISFACE
G6.deferencia: theta_candidatos_reales=6 (instrumentos=['encup2012', 'endireh2003', 'endireh2016'], +placeholder=[]) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[] | veredicto=EXISTE-NO-SATISFACE

# total filas escritas en data/emparejamiento-motor-v1_2.tsv: 1196

# FILAS_EXAMINADAS_POR_TABLA (A.13)
# inventario-reactivos-v1_2: 178246
# inventario-reactivos-ext-v1_0: 63345
# inventario-fd-v1_1: 17094

# DELTAS_JSON
[["G5", "familismo_apoyo", "EXISTE-SATISFACE", ["eder2017", "endireh2016"]], ["G5", "radio_confianza", "EXISTE-SATISFACE", ["endireh2016"]], ["G5", "familismo_obligacion", "EXISTE-NO-SATISFACE", []], ["G2", "sens_estatus", "EXISTE-NO-SATISFACE", []], ["G2", "aversion_riesgo", "NO-ENCONTRADO", []], ["G3", "aversion_riesgo", "EXISTE-NO-SATISFACE", []], ["G4", "horizonte_temporal", "EXISTE-NO-SATISFACE", []], ["G4", "sens_estatus", "EXISTE-NO-SATISFACE", []], ["G6", "deferencia", "EXISTE-NO-SATISFACE", []]]
```

## Sucesores declarados, no lanzados por este acto

- **Medidor de caja por `G5.familismo_apoyo`** (co-observación robusta, `eder2017`+`endireh2016`) — el candidato con lectura más limpia.
- **Medidor de caja por `G5.radio_confianza`** — condicionado a que ese sucesor primero haga la curación de homónimo declarada arriba sobre `p6_24_10`/etc. de `endireh2016` (confianza institucional vs. interpersonal); si tras esa curación no queda co-observación válida, el par vuelve a `EXISTE-NO-SATISFACE`.
- **`ETIQUETA-ext`** — no se dispara: ningún candidato dominante de los 2 pares nuevos cae en fila sin instrumento (ambas co-observaciones usan instrumento identificado, `eder2017`/`endireh2016`); el techo de etiqueta de `ext` (284 candidatos sin instrumento, 59.0% de sus 481) queda cuantificado arriba mas no es decisivo para estos 2 movimientos.

## No tocado por este acto

`milpa/**`, `milpa/procedencia.yaml`, `G3.horizonte_temporal` (coeficiente del ejecutable, ADR-225), ningún payload de `data/raw`, ninguna medición (β̂/α), `data/INFRAESTRUCTURA-v1_0.md`.
