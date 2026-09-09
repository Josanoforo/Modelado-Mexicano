# `ACTO GEN2-C0-D · EL MARCADOR` — nota de cierre

**9 de septiembre de 2026 · CAJA (UBUNTU), Opus · rama `acto/gen2-c0-d-marcador` · base `main = b711ee0` (`PR #647`)**

Encargo archivado verbatim (0-bis A.3): `forense/encargos/2026-09-09-GEN2-C0-D-MARCADOR.md`.
Compuerta `PRIMERA-SILLA fusionado`: **CUMPLIDA**, verificada por producto (§7).

---

## 0 · El veredicto de la pareada, y el destino del hallazgo — primero, como el encargo manda

> **`RESULT-C0D-VEREDICTO-PAREADA = NO-DISCRIMINA`**
> **`RESULT-C0D-ADJUDICACION-HALLAZGO = EXPLICADO-POR-METRICA`**

```
media d_i = |err_pp(L_CORPUS)| − |err_pp(L_SOLO)|  =  +4.6978 pp
IC95 bootstrap sobre celdas (seed 42, 10 000 réplicas)  =  [ −0.8022 , +11.2747 ]
n_LL = 13   ·   cae la rama 3 de §4 (ic_lo ≤ 0 ≤ ic_hi)
```

**El hallazgo del 8/sep —`L_CORPUS 19.60 · L_SOLO 11.69 · M 4.51`, el corpus empeorando al LLM— no sobrevive como veredicto.** No porque las cifras estuvieran mal: **este acto las reproduce al cuarto decimal** (§2). No sobrevive porque eran **marginales**, y la comparación de primera clase que D-2/`FP-348` exige es **pareada**. Al parear celda con celda, el intervalo cruza cero.

**Y el límite de alcance de P1 NO muerde para esta rama.** El sucesor «re-captura `L_CORPUS` con corpus GEN2» está pre-declarado en §5.3 de la spec **sólo para la rama `CONFIRMADO-CON-ALCANCE`**, que no cayó. `RESULT-C0D-ADJUDICACION-SUCESOR = NO-APLICA`, escrito por la máquina y no por el ejecutor. Dicho esto, la re-captura sigue siendo deseable por otra razón —y ésa sí la mide este acto: **435 payloads entraron al manifiesto después de la ventana de captura** (§6). Eso no es un sucesor que este veredicto exija; es una fila de deuda que se abre honestamente (`NC-0077`).

**Lo que sí sobrevive al pareo, y es el resultado duro del día:**

```
|err_pp(L_SOLO)|   − |err_pp(M)|  =  + 7.2287 pp   IC95 [ +0.7499 , +16.6527 ]   n=13
|err_pp(L_CORPUS)| − |err_pp(M)|  =  +11.9265 pp   IC95 [ +4.1377 , +21.3208 ]   n=13
```

**Los dos brazos de `L` yerran significativamente más que `M`, pareado y con IC que excluye cero.** Sobre estas 14 celdas, y con este alcance, **`M` le gana a `L` con corpus y sin corpus** — y lo que la pareada no puede distinguir es cuál de los dos `L` es peor.

---

## 1 · Qué se pidió y qué salió

| pieza | pedido | entregado |
|---|---|---|
| **P1** | spec del marcador, `COMMIT-1` antes de mirar nada, con B-bis completa | **HECHO.** `prereg-caja-C0D-MARCADOR` v1.0 congelada (`COMMIT-1`), y **v1.1 sucesora** (`COMMIT-3`) porque la v1.0 estaba mal contra el dato (§3) |
| **P2** | el CALC corre, sella, verifica | **HECHO, dos veces.** `CALC-C0D-MARCADOR` selló y **PARÓ por su propia guardia**; `CALC-C0D-MARCADOR-v2` selló 152 `RESULT` y `verify` da **REPRODUCE** |
| **P3** | adjudicación escrita, veredicto primero | **HECHO.** §0 |
| **P4** | adopciones del marcador con el patrón de PRIMERA-SILLA | **CERO, y medido, no supuesto.** El marcador no tiene consumidor posible en la superficie que el registro reconoce (§5). `NC-0024`/`NC-0026` **no se cierran**: su objeto está fuera del perímetro de este acto (§5.2) |

**Contador: NO se mueve, y por DOS razones, ninguna de ellas «se me olvidó» (§4).**

---

## 2 · El control positivo que nadie pidió y que decide si esto vale

El `MAE_pp` **marginal** de este marcador reproduce D4 al cuarto decimal:

| corredor | este acto (`MAE-MARGINAL`) | dirección, 8/sep | n |
|---|---|---|---|
| `L_SOLO` | **11.6925** | 11.69 | 13 |
| `L_CORPUS` | **19.6040** | 19.60 | 14 |
| `M` | **4.5066** | 4.51 | 14 |

**No es una coincidencia amable: es la condición para que el resto del acto signifique algo.** Si el marcador no reprodujera las cifras vigentes, su pareada sería una tercera cifra sin genealogía. Las reproduce, así que la pareada habla del mismo objeto.

Y con eso a la vista, la tabla que el programa no tenía — **la fila `d_i` es nueva; las tres de la izquierda existían pero nunca se habían restado por celda**:

| celda | encuesta | `R` | `err_pp L_SOLO` | `err_pp L_CORPUS` | `err_pp M` | **`d_i`** |
|---|---|---:|---:|---:|---:|---:|
| CIV-M-01 | ENVIPE 2012 | 0.25900 | −1.2749 | +4.1001 | +3.5314 | **+2.8252** |
| CIV-M-02 | ENVIPE 2013 | 0.24340 | +60.6600 | +53.9934 | +5.0913 | **−6.6667** |
| CIV-M-04 | ENVIPE 2015 | 0.24367 | *ausente* | +61.3832 | +5.0645 | *ausente* |
| CIV-M-10 | ENVIPE 2021 | 0.20493 | +17.0066 | +49.8066 | +8.9379 | **+32.8000** |
| CIV-M-12 | ENVIPE 2023 | 0.20811 | +1.6888 | +25.5013 | +8.6201 | **+23.8125** |
| CIV-M-13 | ENVIPE 2024 | 0.19461 | +18.3960 | +9.9763 | +9.9701 | **−8.4196** |
| DIN-M-01 | ENNViH 2002 | 0.15558 | +5.3794 | +18.1919 | +1.9223 | **+12.8125** |
| FAM-M-01 | ENIF 2018 | 0.55719 | −28.8443 | −32.9693 | −9.9486 | **+4.1250** |
| FAM-M-05 | ENIGH 2016 | 0.04746 | −0.1334 | −0.1584 | −0.1765 | **+0.0250** |
| FAM-M-06 | ENIGH 2018 | 0.04729 | +0.1465 | −0.0035 | −0.1591 | **−0.1429** |
| FAM-M-07 | ENIGH 2020 | 0.04378 | +0.9100 | +0.7850 | +0.1919 | **−0.1250** |
| TRA-M-02 | ENCUCI 2020 | 0.12602 | +2.5225 | +2.3975 | −4.0907 | **−0.1250** |
| TRA-M-03 | ENCIG 2013 | 0.04454 | +7.7962 | +7.6712 | +4.0580 | **−0.1250** |
| TRA-M-07 | ENCIG 2021 | 0.07182 | +7.2435 | +7.5185 | +1.3303 | **+0.2750** |

**Siete `d_i` positivos y seis negativos.** El `+4.70` de media lo cargan tres celdas —`CIV-M-10 (+32.80)`, `CIV-M-12 (+23.81)`, `DIN-M-01 (+12.81)`— y el resto lo diluye. Eso es literalmente lo que §5.2 pre-declaró como `EXPLICADO-POR-METRICA`: *«no es una diferencia por celda sino la sombra de unas pocas celdas con error grande»*. La rama se escribió antes de ver esta tabla.

### 2.1 · El universo sí estaba desigual — pero no alcanza a explicar nada

`RESULT-C0D-UNIVERSOS-IDENTICOS = NO`. `CIV-M-04` tiene punto en `L_CORPUS` y **no** en `L_SOLO`, así que D4 comparaba un `MAE` de 14 celdas contra uno de 13. Igualado el universo:

| corredor | `MAE` marginal | `MAE` común (n=13) |
|---|---:|---:|
| `L_SOLO` | 11.6925 | 11.6925 |
| `L_CORPUS` | 19.6040 | **16.3902** |
| `M` | 4.5066 | 4.4637 |

`L_CORPUS` baja **3.21 pp** al quitar la celda que sólo él tenía —y era una de sus peores (`+61.38 pp`)—. **Pero el orden no cambia** (`M < L_SOLO < L_CORPUS` en ambos), así que la rama `EXPLICADO-POR-UNIVERSO` (§5.1) **no dispara**, tal como su condición mecánica exige. Se reporta porque es verdad y porque A-bis 4 obliga, no porque adjudique.

---

## 3 · El acto pagó una spec equivocada, y su propia guardia lo cobró

`CALC-C0D-MARCADOR` (spec **v1.0**) corrió, selló 151 `RESULT` con `exit_code 0`, y se paró solo:

```
RESULT-C0D-CONTROL-CONVERGENCIA-L = DIVERGE   (28 de 28 puntos, todos "uno-ausente")
RESULT-C0D-CONTROL-MAXDIF-L       = 0.0
RESULT-C0D-N-UNIVERSO-COMUN       = 0
RESULT-C0D-ADJUDICACION-HALLAZGO  = NO-ADJUDICA-POR-CONTROL     ← §5.4, pre-declarada
```

**`maxdif = 0.0` junto a 28 divergencias es la firma exacta del defecto: ningún par de números discrepó — un lado del par nunca existió.**

**La causa, medida:** `valor_extraido` es `null` en las 224 capturas crudas, **por diseño**. El punto `L` del agregado vigente sale de `L-extraido-v1_2.tsv`, porque `agregado_v1_2.py` **sobreescribe `_leer_l_variante` por monkeypatch**. La spec v1.0 citó *verbatim* la regla del módulo **base** `agregado_v1_1` — y una spec puede citar verbatim la fuente equivocada y seguir siendo verbatim. El propio agregado lo declara en su salida:

> *«Sigue siendo cierto que `valor_extraido` es null en las 224 capturas crudas … El punto de L de este agregado se lee de `L-extraido-v1_2.tsv` … no de `valor_extraido`.»*

**Lo que importa aquí no es el error, sino qué lo atrapó.** Sin la guardia congelada **antes** del dato, la pareada habría salido sobre `n = 0` y `n = 0` se lee como *falta de cobertura*, no como *lectura rota*: el acto habría reportado `NO-ESTIMABLE-POR-COBERTURA` y nadie habría mirado el lector. `NC-0074`.

**`v1.1` corrige la fuente y nada más.** Ni una rama de veredicto se reescribió: reescribir una rama después de ver que el dato no llegó es exactamente el vicio que el pre-registro existe para impedir. Los bytes de `v1.0` y de su corrida quedan intactos y siguen verificando; `registro()` deriva `SUPERADO→CALC-C0D-MARCADOR-v2` por el campo `repite_de`.

**Y `v1.1` añade la guardia recíproca** (§3.5, `RESULT-C0D-CONTROL-CORRESPONDENCIA`): cada llave `(celda, variante, índice)` del TSV tiene que tener su captura y cada captura su fila. Salió `CORRESPONDE`. Es el mismo defecto mirado desde el otro lado.

---

## 4 · Contador — no se mueve, y las dos razones son distintas

| contador | antes | después |
|---|---|---|
| `N_corridas_selladas` | 5 | **5** |
| `N_resultados_gen2_sellados` | 315 | **315** |
| `N_resultados_gen2_adoptados_activos` | 1 | **1** |
| `dependencias_numericas_legacy_activas` | 204 | **204** |
| `corredores_envueltos_legacy` | 8 | **10** |
| `SELLADA-SIN-ADOPTAR` (T35) | 442 | **442** |
| `WARN` de la suite | 659 | **666** |
| `no_corrido_abiertas` | 37 | **43** |

**Razón 1 — falta la FIRMA, y el encargo lo previó.** El encargo escribió: *«`cuenta_gen2` del CALC-C0D viaja como FIRMA en el mensaje de lanzamiento (mismo estándar: autoridad, fecha, objeto) o el contador no lo cuenta y se dice.»* **En el mensaje de lanzamiento no viaja ninguna firma de contador.** La única firma citada es D-2/`FP-348`, que autoriza *la comparación*, no *el conteo*: no nombra `CALC-C0D-MARCADOR` como objeto, y una firma que no nombra su objeto no firma nada (precedente: «la compuerta se verifica por producto, no por rótulo»). `spec.yaml` declara `cuenta_gen2: PENDIENTE-DE-MESA` y `data/corrida0/decisiones.tsv` **no se toca**: escribir ahí la fila sería falsificar una firma de mesa. **`FP-367`.**

**Razón 2 — y ésta no la levanta ninguna firma sola: regla E.1.** El registro clasificó **las dos** corridas como `envuelto_legacy = SI`, con este motivo derivado por la máquina:

```
cuenta_gen2 = NO · envuelto_legacy = SI
motivo: regla E.1 (ACTO GEN2-T9, D-1): input LEGACY GEN1
        IN-R-CIV-M-01=forense/prereg-duelo-v2/corridas-R/CIV-M-01.json,
        IN-M-CIV-M-01=forense/prereg-duelo-v2/corridas-M/M-CIV-M-01.json, …
```

**Es correcto y es estructural, no un accidente de este acto.** El marcador mide corredores del duelo; sus insumos *son* los artefactos del duelo, que son GEN1. Un marcador GEN2 del duelo GEN1 es, por la regla E.1, un corredor envuelto legacy — y por eso `corredores_envueltos_legacy` sube 8 → **10**, que es el único contador que este acto mueve.

**Consecuencia honesta: aunque mesa firme el contador, `N_corridas_selladas` no sube mientras la regla E.1 mande**, porque la firma de mesa manda sobre la etiqueta *y* sobre E.1, pero firmar «cuenta» un CALC cuyos insumos son GEN1 es una decisión distinta de firmar uno cuyos insumos son corpus. **Las dos cosas se ponen delante de mesa por separado** (`FP-367`, `NC-0075`) en vez de pedir una firma que borre el diagnóstico de E.1 sin decirlo.

---

## 5 · P4 · Adopciones: cero, y por qué eso es el resultado y no una omisión

### 5.1 · El marcador no tiene ranura

El registro reconoce un consumidor por el cruce de `_ids_corrida0_declarados()` (nodos con `corrida0_resultado_id`/`corrida0_generacion` en `milpa/tramite.yaml` y `milpa/procedencia.yaml`) contra las filas de demanda que `cmd_demanda` enumera. Leídas en el árbol, esas filas son de **cuatro** clases y de ninguna más:

```
milpa/tramite.yaml:<regla>:<conducta>                    ← una p de conducta
milpa/procedencia.yaml:coeficientes_generador_sellados:… ← un coeficiente
milpa/procedencia.yaml:asignados_{coeficiente,probabilidad}:…
milpa/src/celdas.py:CORTES_C1:<eje>  ·  milpa/catalogo-momentos-v0_1.tsv:<id>
```

El marcador produce **errores en puntos porcentuales, diferencias pareadas, `MAE`, intervalos y veredictos**. Ninguno es una probabilidad de conducta, un coeficiente de generador, un corte de `C1` ni un momento. **No hay dónde citarlo**, y forzar la cita en una ranura que significa otra cosa sería miscategorizar para mover un número.

Es exactamente lo que `NC-0072` (PRIMERA-SILLA) ya había medido —*«la segunda silla necesita un CALC, no otra cita»*— y este acto lo **confirma sobre un caso nuevo**: no es que falte voluntad de citar; es que la clase de cantidad no encaja. `NC-0076`.

**Y el tablero no es superficie de adopción:** `forense/tablero/*.md` es Markdown que el registro **no lee** (`_ids_corrida0_declarados` sólo abre `TRAMITE` y `PROCEDENCIA`; verificado por comando). Una fila de tablero es documentación, no adopción — decirlo evita que alguien la escriba creyendo que baja el WARN.

**`NC-0053` → sigue CERRADA**, y el precedente de PRIMERA-SILLA **no** pasa a «patrón en uso» desde aquí: un patrón entra en uso cuando se usa, y este acto no tuvo dónde usarlo. Se dice, en vez de declarar un uso que no existe.

### 5.2 · `NC-0024` y `NC-0026` no se cierran — premisa del encargo verificada contra el árbol

El encargo pide `NC-0024/0026 → CERRADAS con cita`. **Las dos filas nombran a `C0-D` como sucesor, pero su objeto está fuera del perímetro que este mismo encargo declara** (*«No toca capturas L, motor M, CALC previos ni sus sellos»*):

- **`NC-0024`** — *«el marcador por segmento (celda con `x != vacío`, **M por motor matricial** y R por IC de la entrada `_ejes_`)»*. Su propia fila declara: *«Depende de **C0-C** (motor y emisor limpios)»*. **`C0-C` no existe en el árbol** (`gh pr list`: ningún acto `C0-C`; `git ls-remote`: sólo `main` y esta rama). Además, las capturas del duelo no traen segmentación: las 14 celdas tienen `x = vacío` y ningún insumo de este marcador puede llenarlo.
- **`NC-0026`** — *«la envoltura por celda de `tools/emite_m.py` que consuma la regla de ola previa estricta»*. Su propia fila ya dice por qué no se puede aquí: *«cablearlas a `emite_celda` cambiaría la M que el emisor produce hoy, y con ella las `corridas-M` ya selladas … escribirla y cablearla sería salirse del perímetro»*. Es literalmente la frase que el perímetro de este encargo prohíbe.

**Cerrarlas «con cita» sin ejecutar su objeto sería cerrar deuda por decreto.** Se dejan `ABIERTA`, con el sucesor re-apuntado y la razón medida, y se dice aquí en vez de en un renglón de tabla. `NC-0075`.

---

## 6 · Alcance, `B`, y dos cosas que salieron mejor de lo esperado

**Alcance (§0.3 de la spec).** Los dos brazos se capturaron en la **misma ventana** (1–2/sep/2026), mismo modelo `claude-opus-4-6`, misma `k = 8`, misma temperatura 1.0 — **eso es lo que hace lícita la pareada**: el brazo no está confundido con la fecha ni con el modelo. Y el corpus que vio `L+corpus` es el del 1–2/sep: **`RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES = 435`** entradas de manifiesto con `fecha_descarga > 2026-09-02`. La re-captura con corpus GEN2 no la exige este veredicto (§0), pero 435 payloads de diferencia son motivo propio: `NC-0077`.

**Una reserva sobre un `RESULT` que salió pobre y no se retoca.** `RESULT-C0D-ALCANCE-CORPUS-CAPTURA` dice `fecha_congelacion=sin-params · modelo=None`, porque muestrea **una** captura y la primera celda del marco (`CIV-M-01`) pertenece a la familia de archivos que trae `modelo_real` (nulo) en vez de `params`. **La cifra del acto no depende de ese campo** —los metadatos correctos están medidos y citados en §0.3 de la spec sellada, sobre las 424 capturas— pero el `RESULT` es más pobre de lo que debería. Sellado está y sellado se queda: `NC-0078`.

**El piso `B`, con la guardia de A-bis 4 puesta.** Cubre **2 de 14** celdas, como la spec congeló:

| celda | conmensurabilidad | brecha observadas | `B` PERSISTENCIA | `err_pp(B)` | `err_pp(M)` |
|---|---|---:|---:|---:|---:|
| FAM-M-06 | **PISO-CONMENSURABLE** | **0.0000 pp** | 0.047459 | **+0.0173** | −0.1591 |
| FAM-M-07 | **PISO-CONMENSURABLE** | **0.0000 pp** | 0.047285 | **+0.3510** | +0.1919 |

**La brecha es exactamente cero**: `RESULT-B-ENIGH-<ola>-P` de `CALC-B-0001` y el `R` del duelo son **el mismo número**, llegado por dos cadenas de medición independientes (ENIGH vía `CALC-B-0001`; `corridas-R` vía el procedimiento del duelo). Es la validación cruzada más limpia que este acto produjo, y **nadie la pidió**: la guardia se congeló para poder *descartar* `B` si no era conmensurable, y resultó ser un control positivo.

Y el dato incómodo: **en `FAM-M-06` la línea base tonta yerra `+0.0173 pp` donde `M` yerra `−0.1591 pp` y `L` yerra entre `+0.15` y `−0.004`.** Con `n = 2`, `RESULT-C0D-B-VEREDICTO = NO-ADJUDICA-POR-N`: se cita, no se ordena. Extender `B` al resto del marco es lo que convertiría esto en una comparación — y es un acto propio (`NC-0079`).

---

## 7 · Compuerta, verificada por producto

```
$ git merge-base --is-ancestor 5d2e1cc origin/main   → 5d2e1cc ES ANCESTRO
$ git cat-file -e origin/main:forense/notas/2026-09-09-GEN2-PRIMERA-SILLA-cierre.md  → PRESENTE
$ git cat-file -e origin/main:forense/encargos/2026-09-09-GEN2-PRIMERA-SILLA.md      → PRESENTE
$ git show origin/main:canon/gobernanza-v1_15.md | grep '^\*\*ADR-424'               → línea 7438
```

`PR #647` fusionado. **Y este acto consume de PRIMERA-SILLA lo que aquélla dejó**: el patrón de cita (que resultó inaplicable, §5.1, y ése es el hallazgo), y los contadores verdaderos —5 / 315 / 1 / 204— que son la línea «antes» de §4, tomados de `status` y no de prosa.

---

## 8 · A.13 — qué se examinó, y con qué

| veredicto | qué se examinó | comando |
|---|---|---|
| «la pareada `L↔L` no existe en el árbol» | `agregado_v1_3.py` completo | `grep -c "L_SOLO_vs_L_CORPUS\|L_solo_vs_L_corpus"` → `0` |
| «`B` cubre 2 de 14» | las 14 filas del marco + los 90 ids de `CALC-B-0001` | lectura de `marco-M-sorteado-v1_3.tsv` y `resultados.json` |
| «los dos brazos, misma ventana» | los 424 archivos de `corridas-L/` | conteo por `(variante, fecha_congelacion, modelo)` |
| «`valor_extraido` es null» | las 8 réplicas de `CIV-M-01 L-solo` y las 224 vía el control | `RESULT-C0D-CONTROL-CONVERGENCIA-L` sobre 28 puntos |
| «reproduce D4» | los 3 `MAE-MARGINAL` contra las 3 cifras del 8/sep | `CALC-C0D-MARCADOR-v2`, corrida sellada |
| «el marcador no tiene ranura» | `_ids_corrida0_declarados` y las filas de `cmd_demanda` | lectura de `tools/corrida0.py:278,327,340,359,548,602,2636-2696` |
| «el tablero no es superficie» | `TRAMITE`/`PROCEDENCIA`/`PROPUESTA` en el código; `forense/tablero/` | `grep -rn "corrida0_resultado_id\|RESULT-" forense/tablero/` → 0 |
| «`C0-C` no existe» | PR abiertos y ramas remotas | `gh pr list --state all`; `git ls-remote --heads origin` (1 rama ≠ main: la mía) |
| «contador no cuenta, y por dos» | las dos filas de `corridas.tsv` | `cuenta_gen2=NO · envuelto_legacy=SI · motivo: regla E.1` |
| suite | `tests/check.py --baseline` | §9 |

---

## 9 · Suite

**Línea base al arrancar** (`main = b711ee0`, `TZ=UTC`): **3 FAIL · 659 WARN**, `LÍNEA BASE: VERDE`.
**Al cerrar** (`TZ=UTC`): **3 FAIL · 666 WARN**, `LÍNEA BASE: VERDE`. **Este acto no agrega ni quita FAIL.**

Los 3 `FAIL` son los mismos preexistentes y ninguno está en el perímetro: `T06` (2, Gini y confianza interpersonal divergentes en el corpus) y `T08` (1, siete reports sin mapa de evidencia). Deuda declarada desde `MAESTRA38-N4`.

**Un cuarto `FAIL` aparece sin `TZ=UTC` y es un falso rojo por huso horario**, sobre un encargo **ajeno** a este acto:

```
sin TZ (CST):  4 FAIL · 659 WARN · LÍNEA BASE: ROJO
    · T-YAMEDIDO: forense/encargos/2026-09-08-GEN2-TRAMITE-BANDEJA.md: cita `R8.3` …
TZ=UTC:        3 FAIL · 659 WARN · LÍNEA BASE: VERDE
```

`T-YAMEDIDO` compara la fecha del nombre del encargo contra «hoy», y a las 21:26 CST el «hoy» local (8/sep) todavía alcanza a un encargo del 8/sep que en UTC (9/sep) ya es de ayer. **Ni el archivo ni la regla son de este acto** y no se tocan; se declara para que nadie lo lea como daño de este PR. `NC-0080`.

**El WARN se mueve `659 → 666`, y sólo en los dos tests que vigilan las filas que este acto abrió:**

```
· T34 T-NO-CORRIDO: 37 -> 43   (+6)   las seis NC nuevas que quedan ABIERTAS (NC-0074 nace CERRADA)
· T22 T-FIRMAS:     50 -> 51   (+1)   FP-367, la firma de contador pendiente
· T35 T-REPRO:     443 -> 443   (0)
```

**Ningún otro test cambia ni una unidad, y `T35` es el que importa: no se mueve.** Es coherente con §4 y §5 — el marcador no cuenta (regla E.1 + firma ausente), así que sus 152 `RESULT` **no entran** al universo `SELLADA-SIN-ADOPTAR`, y al no adoptar nada tampoco lo bajan: `442 → 442`. Los `+7` son deuda que este acto **declara**, no defecto que introduce: es exactamente para lo que `T34` y `T22` existen.

---

## 10 · Higiene

- Todos los `git add` por ruta explícita, nunca `-A` ni `.`.
- `registro --escribe` corrido **una sola vez**, después de sellar las dos corridas; ninguna otra escritura de TSV.
- **Nada fuera del perímetro.** En particular: no se tocó `corridas-L/`, `corridas-M/`, `corridas-R/`, `agregado_v1_*.py`, `tools/emite_m.py`, `milpa/tramite.yaml`, `milpa/procedencia.yaml`, ni ningún `sello.json` previo.
- `data/corrida0/decisiones.tsv` **no se tocó**: la firma de contador es de mesa (§4).
- La spec `v1.0` y su corrida quedan **intactas y verificando**; `v1.1` las supera por `repite_de`, sin editar un byte hacia atrás.
- Las cuatro premisas del encargo se verificaron contra el árbol **antes** de congelar la spec, y las que no se reprodujeron están en §0.2 y §0.3 de la sellada, no descubiertas al escribir esta nota.
