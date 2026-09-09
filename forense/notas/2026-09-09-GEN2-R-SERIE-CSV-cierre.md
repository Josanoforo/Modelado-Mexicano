# `ACTO GEN2-R-SERIE-CSV` · cierre — tres árbitros `R` con cadena GEN2, y el dictamen viejo reproducido al bit

**9 de septiembre de 2026** · CAJA (Ubuntu) con corpus montado · Opus · rama `acto/gen2-r-serie-csv` · base `origin/main = 071406a` (`PR #655`).

---

## 1 · Los tres `R` con cadena, y el veredicto de los tres controles

**Los tres controles positivos pasan, y pasan al bit: `Δ = +0` exacto en las tres celdas.**

Un medidor escrito de cero — congelado antes de abrir un solo byte de microdato, sin haber leído `tools/arbitra.py` ni los JSON de GEN1 — reconstruye los tres puntos `R` que GEN1 selló, hasta el último dígito de `float64`. La rama pre-declarada que se cumplió es `REPRODUCE` (`|Δ| ≤ 1.0e-9`), no la de tolerancia.

| celda | ola | `R` (`RESULT-R-<celda>-PUNTO`) | `EE` | IC95 (conglomerado último) | `CV` | `n` | control vs GEN1 |
|---|---|---|---|---|---|---|---|
| `CIV-M-10` | ENVIPE 2021 (delitos de **2020**) | **`0.20493399286059008`** | `0.004773433` | `[0.195578, 0.214290]` | 2.33 % | 32 967 | **`REPRODUCE`** · `Δ = +0` |
| `CIV-M-12` | ENVIPE 2023 (delitos de **2022**) | **`0.20811159524290274`** | `0.004760266` | `[0.198782, 0.217442]` | 2.29 % | 31 012 | **`REPRODUCE`** · `Δ = +0` |
| `CIV-M-13` | ENVIPE 2024 (delitos de **2023**) | **`0.19461180215093080`** | `0.005391415` | `[0.184045, 0.205179]` | 2.77 % | 33 108 | **`REPRODUCE`** · `Δ = +0` |

`VEREDICTO-CV = CV-ACEPTABLE` en las tres (la regla `CV ≥ 30 % ⇒ SKIP` de `PROCEDIMIENTO-R-v1_0.md` §1 / `FP-79` no dispara: el peor `CV` es 2.77 %). `ESTADO = CALCULADO` en las tres. `corrida0 verify` → **`REPRODUCE`** con **`CONTEXTO: IDENTICO`** en las tres, 38 de 38 `RESULT` cada una.

**Qué vale y qué no vale este control.** Vale como **validación independiente del punto**: dos implementaciones escritas sin verse — la de GEN1 en `tools/arbitra.py` y la de este acto, derivada sólo de `codificacion-R-v1_0.tsv` — coinciden bit a bit sobre el mismo archivo. **No** vale como validación del `EE`: el `EE` de GEN1 no se comparó, porque su IC salió de un bootstrap sin semilla comparable y compararlo fabricaría un desacuerdo sin significado. Y **no** es la validación independiente formal del registro (`validacion_independiente: NO-HECHA`, `NC-0096`).

Cadena `E.2` completa por celda: `SPEC` (`prereg-caja-R-ENVIPE-SERIE`, `sha b9a29cf6…`) → `CALC-R-<celda>` → `INPUTS` (4, con `sha256` del manifiesto verificado en `preflight`) → `CÓDIGO FIJADO` (`script_blob_sha256 e1e563d0…`, **el mismo en las tres**) → `ENTORNO` (`firma_entorno` en `ejecucion.json`) → `EJECUCIÓN` (`corrida_id` propio) → `RESULT` con tipo/unidad/tolerancia → `USO`: **ninguno todavía**, y ése es el único eslabón abierto (`NC-0092`, es decisión de mesa por diseño).

---

## 2 · La premisa del encargo sobre la tabla ciega no se sostiene — y se corrige con fuente, no con criterio

El encargo dice que el estimando primario es *«`R` tal como lo define la tabla ciega (variable, codificación, universo, ponderador, diseño EST/UPM)»*. Verificado contra el archivo, **`espec-R-ciega-v1_2.tsv` define dos de esos cinco** y declara los otros tres literalmente `NO ESTIMADO EN ESTE ACTO`:

```
$ awk -F'\t' '$1=="CIV-M-10"' forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv
  variable = BP1_23 · escala = binaria · cv_arbitro = BP1_23
  universo = "NO ESTIMADO EN ESTE ACTO -- censo de existencia sobre inventario de reactivos…"
  estimador = "NO ESTIMADO EN ESTE ACTO"   ·   ponderador = "NO ESTIMADO EN ESTE ACTO"
```

Idéntico en `CIV-M-12`, `CIV-M-13` y en `marco-M-congelado-v1_2.tsv`. El hueco **no** lo llenó el ejecutor: lo llena `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv` (`sha cf5dfb18…`), fechada 31/ago y 1/sep/2026 — anterior a esta sesión y a este encargo —, y cada uno de sus seis elementos se verificó contra el codebook de cada ola antes de congelar (§2 y §2.1 de la sellada). Esto importa por una razón concreta: es lo que hace que la codificación **no sea una palanca** del ejecutor, que conocía los tres resultados GEN1 desde el primer minuto (§0.3 de la sellada, `ADR-46`).

**Salvedad que viaja con el resultado:** `codificacion-R-v1_0.tsv` sigue en `estado = PROPUESTA`, no `SELLADA`. Tres `R` sellados descansan hoy sobre una propuesta. Se declara, no se disimula → **`FP-370`** y `NC-0095`.

---

## 3 · El embudo, ola por ola — contado antes y después de cada filtro

| | `CIV-M-10` (2021) | `CIV-M-12` (2023) | `CIV-M-13` (2024) |
|---|---:|---:|---:|
| filas de `TMod_Vic` | 37 156 | 35 135 | 37 614 |
| `BP1_23` en blanco / `b` (fuera, **no** imputadas) | 3 962 | 3 957 | 4 262 |
| `BP1_23 = 99` NS/NR (fuera) | 227 | 166 | 244 |
| código fuera del catálogo de la ola | **0** | **0** | **0** |
| `BP1_23 ∈ {01..09}` = universo candidato | 32 967 | 31 012 | 33 108 |
| sin ponderador (`FAC_DEL` ≤ 0 o no finito) | **0** | **0** | **0** |
| sin diseño (`EST_DIS` o `UPM_DIS` vacío) | **0** | **0** | **0** |
| **`n` de `U_R`** | **32 967** | **31 012** | **33 108** |
| de `U_R`, delitos de HOGAR (`BPCOD 01..04`) | 13 717 | 12 303 | 13 345 |
| de `U_R`, delitos PERSONALES (`BPCOD 05..15`) | 19 250 | 18 709 | 19 763 |
| masa de `FAC_DEL` sobre `U_R` | 26 433 277 | 25 461 157 | 29 887 247 |
| estratos `EST_DIS` · UPM `(EST,UPM)` | 597 · 9 903 | 602 · 9 745 | 600 · 9 654 |
| estratos con **una sola UPM** | 19 | 33 | 20 |
| `n` de `U1` (homologado a la ola 2025) | 16 798 | 16 283 | 17 297 |
| estratos de `U1` con una sola UPM | 48 | 54 | 50 |

⚠️ **`N-BPCOD-05-15` de esta familia NO es el mismo contador que el homónimo de `CALC-ENVIPE-0001`.** Aquí cuenta dentro de `U_R` (o sea, ya filtrado por `BP1_23 ∈ {01..09}`); allá contaba sobre la tabla completa antes del filtro de denuncia. Los dos están declarados en su unidad; se dice aquí para que nadie los cruce.

### 3.1 · Una premisa de la tabla de codificación, contestada con un número: **`0` en las tres**

`codificacion-R-v1_0.tsv` define el universo de `R` **sin** exigir `BP1_20 = 2`, apoyándose en que «`BP1_23` es `b` (blanco) para quien SÍ denunció, caso que ya queda fuera por código no válido». La spec no dio eso por bueno: pre-declaró el contador `N-INCONSISTENTES-BP1-20` (filas con `BP1_23 ∈ {01..09}` **y** `BP1_20 ≠ 2`) para medir si la ruta implícita y la explícita coinciden.

**`N-INCONSISTENTES-BP1-20 = 0` en las tres olas.** La premisa se sostiene, y ahora se sostiene con una cifra en vez de con una frase. Si hubiera salido `> 0`, el estimando no habría cambiado — pero la reconciliación con GEN1 habría empezado por ahí.

### 3.2 · `METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA` en las tres: los IC son **límite inferior**

19, 33 y 20 estratos de `U_R` tienen una sola UPM (48, 54 y 50 en `U1`). Conforme a la regla pre-declarada, **no se colapsaron con otro estrato** (decisión de diseño que esta spec no está autorizada a tomar) y **no se descartaron** (sesgaría el punto): entran al punto y aportan varianza cero. **Consecuencia que viaja con toda cifra de IC de este lote: los IC son límite inferior de la anchura verdadera, no IC exactos.**

---

## 4 · Hallazgo del lote: **el descriptor de `EST_DIS`/`UPM_DIS` está mal en las tres olas, de tres formas distintas**

`PERFIL-DISENO` se pre-declaró como `RESULT` porque el descriptor de INEGI ya había mentido sobre estas dos columnas en la ola 2025. Lo hizo otra vez, en las tres:

| ola | descriptor dice | el archivo trae | qué está mal |
|---|---|---|---|
| 2021 | `EST_DIS` Numérico(3) **`001..303`** | 598 valores, `001`…**`606`**, largo 3 | **el rango declarado es la mitad del real** |
| 2021 | `UPM_DIS` Numérico(5) | 10 332 valores, largo **5** | coincide |
| 2023 | `EST_DIS` Alfanumérico(3) `001..595` | 604 valores, `001`…**`607`**, largo 3 | rango declarado corto |
| 2023 | `UPM_DIS` Alfanumérico(**5**) | `0000001`…`0013099`, largo **7** | **la longitud declarada está mal** |
| 2024 | `EST_DIS` Carácter(3) `001..607` | 601 valores, `001`…**`905`**, largo 3 | rango declarado corto |
| 2024 | `UPM_DIS` Carácter(**7**) | `000001`…`900147`, largo **6** | **la longitud declarada está mal** |

**Por qué no mordió:** el medidor trata las dos como **llaves de texto opacas** — nunca `int()`, nunca `zfill()`, nunca re-relleno al ancho del descriptor. Un medidor que hubiera normalizado `UPM_DIS` al ancho declarado habría **partido o fundido conglomerados en silencio** en 2023 y 2024, y el IC de diseño habría salido mal **sin ningún error**. `PERFIL-DISENO` confirma además que dentro de cada ola la longitud es consistente (`len` único, `bordes_con_espacio = 0` en las tres), que es la condición bajo la cual tratarlas como cadenas es seguro.

**Nada se corrigió y nada se usó del descriptor**: la discrepancia se mide, se sella como `RESULT` de texto y se reporta.

---

## 5 · La serie parcial — **sólo en el estimando secundario homologado**

`A-bis.4`: el primario y el secundario **no se comparan entre sí** y no se calcula ningún delta entre ellos. Están en la misma corrida porque salen de la misma lectura del mismo archivo, no porque sean comparables — `U_R` incluye delitos de hogar y el código `09`; `U1` no.

La serie que sigue es **sólo** `p(C1, U1)`: unidad DELITO, `BPCOD 05..15`, `BP1_20 = 2`, denominador `{01..08}`, ponderador `FAC_DEL`, mismo universo y misma codificación primaria que `RESULT-ENVIPE-DEN-P-C1-U1` de `CALC-ENVIPE-0001`. El IC es el **bootstrap de UPM en estrato**, semilla `20260909`, 2 000 réplicas — **el mismo método que fijó el IC de la ola 2025**, replicado aquí precisamente para que la columna no mezcle dos métodos.

| ola | **delitos de** | `p(C1,U1)` | IC95 (bootstrap) | `n` |
|---|---|---:|---|---:|
| ENVIPE 2021 | **2020** | `0.239890` | `[0.228350, 0.251226]` | 16 798 |
| *ENVIPE 2022* | *2021* | — **NO MEDIDA** — | | |
| ENVIPE 2023 | **2022** | `0.243799` | `[0.232411, 0.255911]` | 16 283 |
| ENVIPE 2024 | **2023** | `0.226945` | `[0.213112, 0.241137]` | 17 297 |
| ENVIPE 2025 | **2024** | `0.231689` | `[0.219191, 0.244462]` | 20 225 |

**Cuatro cantidades fechadas, no una tendencia.** El recorrido completo de los cuatro puntos es `0.0169` (de `0.226945` a `0.243799`) y la anchura de los IC va de `0.0229` a `0.0280`: **el recorrido entero de la serie cabe dentro de un solo intervalo**, y los cuatro se traslapan entre sí. **Ninguna transferencia, ninguna estabilidad temporal y ninguna extrapolación se adjudican aquí** — eso se contrata en `F5`.

Tres advertencias que viajan con la tabla, y ninguna es opcional:

1. **La ola se llama 20NN y mide delitos de 20NN−1.** El eje de la tabla es el **año de delito**, no el nombre de la ola. Confundirlos desplaza la serie un año entero.
2. **Falta el año de delito 2021** (`envipe2022_csv`, en el corpus, no medida: no es una de las tres plazas de la demanda). `NC-0093`.
3. **La serie completa espera al trío DBF.** Las olas 2012–2020 son `GEN2-R-SERIE-DBF`, gateado al merge de éste. Hasta que corra, esto son **cuatro** puntos, no trece.

### 5.1 · Lo que vale el código `08`, medido en cada ola

`DELTA-C2-C1` = lo que vale meter «actitud hostil de la autoridad» dentro de miedo/desconfianza, sobre `U1`:

| ola | `p(C1,U1)` | `p(C2,U1)` | **`DELTA-C2-C1`** |
|---|---:|---:|---:|
| 2021 | `0.239890` | `0.278742` | **`+0.038852`** |
| 2023 | `0.243799` | `0.282021` | **`+0.038222`** |
| 2024 | `0.226945` | `0.259877` | **`+0.032932`** |
| 2025 (`CALC-ENVIPE-0001`) | `0.231689` | `0.267243` | **`+0.035555`** |

Es una decisión de codificación que vale entre 3.3 y 3.9 puntos de proporción, estable en las cuatro olas — más que la variación de la propia serie entre 2020 y 2024. Se reporta como descripción; **no** autoriza a preferir una codificación sobre la otra.

---

## 6 · Perímetro, concurrencia y pisadas — reportadas, no resueltas a mano

**Tocado:** `forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.{md,sha256}` · `forense/prereg-caja/R-ENVIPE-SERIE-control-gen1.py` · `data/corrida0/CALC-R-CIV-M-{10,12,13}/**` · los tres TSV derivados · esta nota · `forense/no-corrido.tsv` · `forense/hallazgos.md` · 0-bis · cascada. **Nada fuera de esa lista.**

**Lectura del perímetro que se declara**, porque el encargo permite dos ubicaciones y se eligió una: el script de control vive en `forense/prereg-caja/R-ENVIPE-SERIE-control-gen1.py` porque el perímetro autoriza el glob `forense/prereg-caja/R-ENVIPE-SERIE*` y el control es un artefacto del lote, no de una corrida. **`tools/` no está en el perímetro y no se tocó.**

**Una escritura fuera de la lista enumerada, declarada y no disimulada.** El perímetro del encargo enumera `forense/prereg-caja/R-ENVIPE-SERIE*`, `data/corrida0/CALC-R-*/`, los TSV re-derivados, `forense/notas/`, `forense/no-corrido.tsv`, el 0-bis y **la cascada** — y `tests/` no aparece por nombre. Sellar tres corridas deja `tests/test_corrida0.py::T-STATUS-SMOKES` en ROJO, porque ese falsador **cablea los contadores esperados** (`7`/`644`/`516`) y este acto los mueve a `10`/`758`/`630`. Se actualizaron esos tres números, con el párrafo de premisa que la casa ya usa para los tres actos anteriores que hicieron lo mismo, **leyendo «cascada» como el paso 5 de `/acto` la define** (que nombra `tests/check.py` explícitamente) y bajo el paso 6 (la suite en VERDE o PARO-reporte). Se dice aquí para que mesa lo revise como lectura de perímetro y no lo descubra en el diff: **es lo único escrito fuera de la lista enumerada, y no toca ninguna aserción del falsador, sólo la cifra que ya no correspondía.** Suite en VERDE en los dos relojes: `TZ=UTC python3 tests/check.py --baseline` y el local (CST) dan **`LÍNEA BASE: VERDE`**, `3 FAIL · 990 WARN`, sin entrada nueva.

### 6.1 · Un defecto del re-derivado, encontrado al pisarlo — y que volvió a ocurrir el mismo día en otro PR

`corrida0 registro --escribe` **sin** `--verifica` deja las columnas `resultado_replay` y `contexto_replay` en `NO-VERIFICADO` para **todas las corridas que ya las traían llenas**. Es decir: re-derivar «como manda la casa» para añadir tres filas **borra veredictos de replay ajenos**, en silencio y con el comando correcto.

Se encontró midiéndolo sobre `origin/main = 071406a` (14 filas se habrían blanqueado) y se evitó corriendo con `--verifica`. **Y volvió a ocurrir, en otro acto, mientras éste cerraba:** `origin/main` avanzó a `a94317e` (`PR #656`, `GEN2-FIRMAS-ADOPCION-1`) con **las 14 filas ya blanqueadas a `NO-VERIFICADO`**. Sobre el árbol fusionado, la re-derivación de este acto **con** `--verifica` las vuelve a llenar. Estado final, medido contra `origin/main = a94317e`:

- `data/corrida0/resultados.tsv` → **cero pisadas** (1 413 filas idénticas fuera de las nuevas).
- `data/corrida0/usos.tsv` → **idéntico byte a byte al de `origin/main`** (`git diff --stat` vacío): este acto **no adopta nada**, y las dos adopciones del programa (`NC-0053` y `NC-0084`) llegan intactas del merge.
- `data/corrida0/corridas.tsv` → **14 filas ajenas cambian, y ninguna pierde información**: las 14 pasan de `NO-VERIFICADO` a un veredicto real — doce a `REPRODUCE`/`REPLICA-RESULTADO`/`NO-REPRODUCE` con su contexto, y `CALC-0001`/`CALC-0002` a `NO-EJECUTABLE` porque sus payloads (CIDE/LAPOP) viven en la raíz `descargas_mx`, **que esta caja no lee**.

**El defecto de fondo, ahora con dos instancias en el mismo día:** dos columnas de un artefacto marcado `# DERIVADO — NO EDITAR` **dependen del entorno y de la bandera** con que se corre la derivación. Gana quien re-derivó al último, y el diff no dice que la causa fue la caja ni la bandera. No se resolvió a mano (un `DERIVADO` no se edita) → **`NC-0094`**, para un acto con `tools/` en su perímetro.

### 6.2 · Concurrencia declarada

**`FIRMAS-ADOPCION-1` fusionó primero, y colisionó en tres numeraciones.** Al terminar la cascada, `git fetch --prune` mostró `origin/main` **7 commits adelante** (`PR #656`). Se hizo `git merge origin/main` de inmediato y se aplicó la regla de la casa —**renumera quien fusiona segundo**— en las tres colisiones, ninguna resuelta por inferencia:

- **`ADR-432` → `ADR-433`.** `cierre_acto.py` Fase A había dado candidato `432` sin ninguna rama remota accesible que lo trajera redactado; `PR #656` lo tomó primero.
- **`NC-0089`…`NC-0094` → `NC-0092`…`NC-0097`.** `PR #656` abrió `NC-0089`/`-0090`/`-0091`. Las seis filas propias y **sus referencias internas** se remapearon en **un solo paso con un diccionario** — no seis reemplazos sucesivos, que se habrían pisado entre sí. Las referencias a `NC` ajenos (`NC-0018`, `NC-0087`) no se tocaron.
- **`FP-370`** no colisiona: el máximo en `origin/main` sigue siendo `FP-369`.

Conflictos resueltos con la convención de la casa —**la entrada de `origin/main` primero, la propia después, verbatim, sin reordenar**— en `forense/no-corrido.tsv`, `canon/registro-rotulos.tsv` y `canon/gobernanza-v1_15.md`. En la línea `L0`, la anotación propia va delante (es la nueva) y la de `PR #656` recibe `{cita-historica}`. `tests/test_corrida0.py::T-STATUS-SMOKES` se tomó **entero del lado de `origin/main`** (que ya lo había re-pineado a `8`/`787`/`517`/`2`) y sobre eso se sumaron los tres `CALC-R`: **`11`/`901`/`631`**, con la adopción **sin moverse en `2`**. Las tres cifras se leyeron de `corrida0 status` sobre el árbol fusionado, no se calcularon a mano.

---

## 7 · Contadores

Leídos de `corrida0 status` sobre el árbol **fusionado** con `PR #656`, no calculados a mano: `N_corridas_selladas` **8 → 11** · `N_resultados_sellados` **787 → 901** · `N_resultados_gen2_sellados` **517 → 631** (`+114 = 3 × 38`, ids todos propios) · `N_resultados_gen2_adoptados_activos` **2 → 2** (sin cambio: este acto no adopta; las dos adopciones vivas son `NC-0053` y `NC-0084`, ambas ajenas) · `resultados_con_validacion_independiente` **0**, sin cambio (`NC-0096`) · `N_corridas_requeridas` 86, sin cambio.

`cuenta_gen2 = SI` para los tres, con la firma de mesa del 9/sep/2026 **con OBJETO explícito** citada verbatim en `etiquetas.cuenta_gen2_firma` de cada `spec.yaml` (estándar `FP-367`/`FP-368`). El contador **ya los cuenta** por la etiqueta de la spec (`motivo_cuenta_gen2 = etiqueta de la spec`); lo que **no** se escribió es la fila de `data/corrida0/decisiones.tsv`, porque ese archivo **no está en el perímetro** y lo tiene en el suyo el trámite `FIRMAS-ADOPCION-1` que corre en paralelo. Queda en `## NO-CORRIDO`, con su impacto exacto: **ningún contador se queda quieto**; lo que falta es la fila del artefacto de mesa.

---

## 8 · Lo que este acto NO hizo, con su razón

Ni una sola ola DBF (encargo hermano). Ni un byte de `milpa/`, del marcador o de las capturas `L`. Ni un JSON de `corridas-R/` reescrito o borrado: los tres siguen con sus bytes intactos y su `sha256` original — el registro los marcará `SUPERADO` cuando la sucesión se propague, que es otro acto. Ninguna adopción, ninguna transferencia, ninguna causalidad, ningún `tier` movido.

Y no se abrió `tools/arbitra.py` en ningún momento de la sesión. **Ése es el motivo por el que las tres líneas `Δ = +0` del §1 significan algo.**
