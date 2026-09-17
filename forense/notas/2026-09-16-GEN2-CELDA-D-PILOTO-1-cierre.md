# ACTO `GEN2-CELDA-D-PILOTO-1` · nota de cierre

**16/sep/2026 · CAJA · `ADR-538` (candidato) · `PR #849`.**
Encargo verbatim: `forense/encargos/2026-09-16-GEN2-CELDA-D-PILOTO-1.md` (0-bis `A.3`, commit `20b458f`).
Spec vigente: `forense/prereg-caja/DIN-ahorro-solo-informal-lxe8-spec-v1_2.md` (`sha256 427117ee…`).

---

## 1 · Qué se pidió, qué se hizo, y en qué orden

Tres commits, **y el orden es el sello**. No se declara: **lo prueba el registro**.

| pieza | commit | qué quedó |
|---|---|---|
| `COMMIT-1` | `3461c46` | spec `v1.0` + sidecar + `spec.md`/`spec.yaml`. **Cero microdato.** |
| *(ajeno)* | `4e5f8e1` | **checkpoint de una sesión concurrente** (Sonnet) que comiteó archivos míos en vuelo sin editarlos |
| `COMMIT-1-bis` | `3422a30` | spec `v1.1` — `FP-379` |
| *(resguardo)* | `3385ea5` | 12 capturas `L-solo` de la tanda luego superada |
| `COMMIT-1-ter` | `ef3f9e8` | spec `v1.2` — `FP-379 · ENMIENDA` |
| `COMMIT-2a` | `2053b25` | `medidor.py` + 64 capturas `L-solo` bajo el prompt de nueve |
| **`COMMIT-2`** | **`c169edc`** | **emisiones selladas — `R` NO existe en el árbol** |
| `COMMIT-3a` | `39bf1af` | contrato y medidor del árbitro |
| **`COMMIT-3`** | **`18b9914`** | **`R` del cruce, adjudicación, celda-D, catálogo, test** |

**El falsador del piloto no se disparó.** El sello de `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` lleva
`RESULT-DIN-LXE8-G-R-EXISTE-AL-CERRAR = "NO"` y `…-G-C2-CRUCE-2024-DERIVADO = "NO"`; la segunda no es prosa
sino una guardia mecánica (`_Guardia`) que marcaría `SI` si alguien agrupara ENIF 2024 por dos ejes a la vez.

---

## 2 · El resultado

### 2.1 · Las ocho celdas

`R` = árbitro, ENIF 2024, desenlace `D9` (nueve tipos de cuenta). `d` en **puntos porcentuales**.

| celda | | `n₂₄` | `R` | IC95 | EE(R) | `C1` | `C2` | `C3` | `d(C1)` | `d(C2)` | `d(C3)` | veredicto |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| `L1xE1` | <15 000 × 18-29 | 992 | **0.4910** | `[0.4432, 0.5372]` | 0.02399 | 0.5210 | 0.4868 | 0.3000 | 3.00 | 0.42 | 19.10 | C3-NO-VENCE-A-LOS-DOS-PISOS |
| `L1xE2` | <15 000 × 30-44 | 1402 | **0.4554** | `[0.4184, 0.4918]` | 0.01873 | 0.4636 | 0.4287 | 0.3200 | 0.82 | 2.67 | 13.54 | C3-NO-VENCE-A-LOS-DOS-PISOS |
| `L1xE3` | <15 000 × 45-59 | 1194 | **0.3341** | `[0.3019, 0.3665]` | 0.01648 | 0.3720 | 0.3778 | 0.2550 | 3.79 | 4.37 | 7.91 | C3-NO-VENCE-A-LOS-DOS-PISOS |
| `L1xE4` | <15 000 × 60+ | 1057 | **0.3255** | `[0.2869, 0.3644]` | 0.01979 | 0.2875 | 0.3236 | 0.2400 | 3.80 | 0.19 | 8.55 | C3-NO-VENCE-A-LOS-DOS-PISOS |
| `L2xE1` | ≥15 000 × 18-29 | 1932 | **0.4000** | `[0.3682, 0.4304]` | 0.01587 | 0.4495 | 0.4026 | 0.3000 | 4.95 | 0.26 | 10.00 | C3-NO-VENCE-A-LOS-DOS-PISOS |
| `L2xE2` | ≥15 000 × 30-44 | 2854 | **0.3333** | `[0.3065, 0.3601]` | 0.01367 | 0.3620 | 0.3478 | 0.2200 | 2.87 | 1.45 | 11.33 | C3-NO-VENCE-A-LOS-DOS-PISOS |
| `L2xE3` | ≥15 000 × 45-59 | 2217 | **0.3241** | `[0.2975, 0.3515]` | 0.01378 | 0.3141 | 0.3014 | 0.2350 | 1.00 | 2.27 | 8.91 | C3-NO-VENCE-A-LOS-DOS-PISOS |
| `L2xE4` | ≥15 000 × 60+ | 1844 | **0.2527** | `[0.2237, 0.2820]` | 0.01488 | 0.2436 | 0.2537 | 0.1950 | 0.92 | 0.10 | 5.77 | C3-NO-VENCE-A-LOS-DOS-PISOS |

### 2.2 · Veredicto de celda-D: **`SIN-CANDIDATO-SUPERIOR`**

* **8/8 celdas `PUNTUADA`**, **0 `INDECIDIBLE`**. Ninguna diferencia cayó por debajo de `0.5·EE(R)`.
* `C3` (`L-solo`) **pierde contra los dos pisos en las ocho celdas**.
* `MAE`: **`C2` 1.4668 pp** · `C1` 2.6439 pp · `C3` 10.6394 pp.
* skill `C3` vs `C1` = **-3.024** · vs `C2` = **-6.254** (se reportan, **no adjudican**).
* `champion_actual = NINGUNO`. **Este acto no adopta nada.** Adoptar es de mesa.

**`B-bis`, declarado antes de correr y ahora leído:**

* **Nadie vence a `C1`** → la **persistencia** queda corroborada como piso en `DIN`.
* **Nadie vence a `C2`** → *los candidatos ensayados no superaron este piso, bajo esta evaluación, en estas ocho
  celdas.* **Y eso es todo lo que dice** (`H5`): **no** identifica ausencia de interacción, **ni** ausencia de
  información aprovechable por otros métodos, **ni** una propiedad de la población. Un piso no vencido acota a los
  **retadores**, no al **fenómeno**.

**El resultado sustantivo, dicho sin adorno:** el piso **puramente marginal y sin interacción** —`C2`, construido
sólo con siete cifras públicas y una fórmula log-aditiva— es **el mejor de los tres**, y le saca casi el doble de
precisión a la persistencia temporal. La interacción `localidad × edad`, tal como estos candidatos la explotan,
**no aporta información que ninguno sepa usar**.

**Límite que la evaluación se impone (`H5`).** Si el ganador se **elige** con las ocho celdas, esa misma evaluación
no lo valida de forma independiente. Aquí **no hay ganador**, así que la reserva se aplica al piso corroborado:
lo que está acreditado es **selección más desempeño conjunto**, nunca desempeño independiente.

### 2.3 · `C5` · diagnóstico puro, fuera de competencia

`|p_nacional − R|` por celda, con `p_nacional = 0.357153` (`milpa/tramite.yaml:1312`, **clase `DERIVADO`, sin IC
propio, no es `MEDIDO`**): de **2.31 pp** (`L1xE3`) a **13.39 pp** (`L1xE1`). El emisor sigue siendo el árbitro con
otro nombre (`tramite.yaml:712`) y **no entra en ninguna adjudicación**.

---

## 3 · Lo que la lectura por archivo encontró, y que cambió el diseño

### 3.1 · `P5_6_k` no mide lo mismo en las dos olas — y paró la ejecución a media máquina

`A.15c` ordenaba verificar los códigos **por archivo** antes del `COMMIT-1`. Se hizo, contra **dos fuentes
independientes**: el FD de cada payload (`enif_2021_estructura_del_archivo.xlsx` hoja `TModulo` filas 291-370;
`enif_2024_fd.xlsx` hoja `TMODULO` filas 384-475) y el diccionario de datos de cada zip.

| variable | ola | texto verbatim del FD |
|---|---|---|
| `P5_6_1` | **2021** | «¿Con su cuenta o tarjeta de nómina … **tiene tarjeta de débito**…?» |
| `P5_7_1` | **2021** | «De julio de 2020 a la fecha, ¿usted **guardó o ahorró** en su cuenta o tarjeta de nómina…?» |
| `P5_6_1` | **2024** | «De junio de 2023 a la fecha, ¿usted **guardó o ahorró** en su cuenta o tarjeta de nómina…?» |

**El equivalente palabra por palabra de `p5_6_k` (2024) es `P5_7_k` (2021), para los NUEVE valores de `k`.** En 2021
no hay `P5_6_6/7` **porque un depósito a plazo fijo y un fondo de inversión no llevan tarjeta de débito** — la
ausencia era un artefacto de la pregunta equivocada, no del constructo. En 2024, `P5_7_*` es otra pregunta por
completo (razones de adquisición, `P5_7_01…P5_7_10,P5_7_99`).

**Consecuencia:** «los siete códigos comunes» de la firma `D2(a)` eran el subconjunto de **rótulos** que coincide
entre dos preguntas distintas, **no** la intersección del constructo — que es de **nueve**.

**Cómo se manejó, que es la parte que importa.** Las specs `v1.0` y `v1.1` **resolvieron el hallazgo por su cuenta**,
sustituyendo la variable con la corrección escrita en el cuerpo. Eso era **decisión de mesa, no del ejecutor**. La
sesión **paró con cero emisiones producidas**, cortó la elicitación a media tanda para no gastar más, y escaló con la
evidencia cruda. La **`FP-379 · ENMIENDA`** ratificó el match y **venció `D2(a)` por premisa falsa**. `NC-0304`, CERRADA.

**El marginal sellado del árbitro es correcto y no se toca:** en 2024 esos rótulos **sí** son la pregunta de ahorro.

### 3.2 · Tres premisas más, corregidas por archivo

1. **`FAC_PER` no existe en ENIF 2021.** El ponderador de `TMODULO` en esa ola es **`FAC_ELE`** («Factor de
   expansión», FD `5,C,fac_ele`) — el **mismo objeto** que `fac_per` en 2024, con otro nombre. El encargo y el
   diseño v1.1 lo declaraban `FAC_PER` para las dos olas.
2. **`EDAD` (2021) vs `EDAD_V` (2024)**, y `98`/`99` son **centinelas de no-especificación**, no edades: salen del
   universo sin imputar, y su conteo se emite como `RESULT` propio (**36** en 2021, **10** en 2024) en vez de
   esconderse en el denominador.
3. **El `n` del cruce era `DESCONOCIDO`.** Las **ocho cotas inferiores de Fréchet–Hoeffding** sobre los márgenes
   sellados son `0`: los márgenes publicados eran compatibles con una celda vacía, y el «≈ 980» del diseño v1.1 §1
   era un punto bajo un supuesto. **Medido: 8/8 con soporte**, `n₂₁` de 1 097 a 2 679 y `n₂₄` de 992 a 2 854, todas
   muy por encima del umbral de 200. La promesa de v1.1 §4 de verificarlo «en `COMMIT-1` con los marginales del FD»
   **era imposible** y queda corregida, no cumplida a medias.

### 3.3 · Un `NO-REPRODUCE` con la causa identificada hasta la fila

Control declarado **antes** del dato (spec §0.8): re-derivar los marginales del árbitro con esta receta y cotejar.

| grupo | `n` (aquí) | re-derivado | sellado | Δ |
|---|---:|---:|---:|---|
| `L1` | 4645 | 0.409076 | 0.409255 | `-1.787e-04` |
| `L2` | 8847 | 0.331066 | 0.329868 | `+1.198e-03` |
| `E1` | 2924 | 0.432063 | 0.432063 | `-9.723e-08` |
| `E2` | 4256 | 0.375709 | 0.375709 | `+7.676e-08` |
| `E3` | 3411 | 0.327505 | 0.327505 | `+4.698e-07` |
| `E4` | 2901 | 0.277212 | 0.277317 | `-1.055e-04` |
| `NAC` | 13492 | 0.357935 | 0.357153 | `+7.823e-04` |

**Veredicto: `NO-REPRODUCE`**, `|Δ|` máximo `1.198e-03`. **Pero `E1`, `E2` y `E3` reproducen a `1e-7`**, y el patrón
lo explica entero. El archivo de 2024 trae **13 502** filas, con `edad_v = 98` en **10** (no hay `99`) y `= 97` en **5**.
**El asiento sellado usó DOS universos distintos, y ninguno es el de esta spec:**

* eje `localidad`: `n = 13 502`, cobertura `1.000000` → **no excluyó los 10 centinelas**; usó el archivo entero.
* eje `edad`: `n = 13 487`, cobertura `0.998889` → excluyó **15** filas: los 10 centinelas **más los 5 de
  `edad_v = 97`**, es decir trató «97 años y más» como **no clasificable**.

Cuadra exacto: `E4` `2 901 = 2 896 + 5`; `L1` `4 645 = 4 646 − 1` y `L2` `8 847 = 8 856 − 9` (los 10 centinelas,
repartidos 1/9). **Que las tres celdas de edad que ningún criterio toca reproduzcan a `1e-7` prueba que el resto de
la cadena —payload, filtros, ponderador, dicotomización, agregación— sí reproduce la receta del árbitro.**

**No se ajustó nada** para hacer coincidir las cifras: la `§3.1` de la spec lo prohíbe expresamente, y estaba
congelada en `3461c46` —**byte a byte idéntica a la de `v1.0`**, `sha256` del bloque `470824e43dce2622…`— antes de
abrir un solo byte de microdato.

---

## 4 · La cadena de firmas, sin resumir

| # | instrumento | fecha | HEAD al llegar | estado del trabajo | ¿rehacer? |
|---|---|---|---|---|---|
| 1 | `FP-378` + `D2(a)` | 17/sep | *(lanzamiento)* | — | — |
| 2 | correctivo pre-emisión (`H1`…`H6`) | 17/sep | *(lanzamiento)* | — | — |
| 3 | **`FP-379`** | 16/sep | `3461c46` | `medidor.py` sin escribir · **0 `RESULT`** · `C2` sin una línea | **No.** La forma multiplicativa **nunca se implementó** |
| 4 | **`FP-379 · ENMIENDA`** ← rige | 16/sep | `3385ea5` | `medidor.py` sin escribir · **0 `RESULT`** · 0 microdato · 0 `R` | **Sólo `C3`**: 18 capturas a `SUPERADO-POR-SPEC`, re-elicitación desde cero |

**Ninguna cifra de este piloto se calculó jamás bajo un diseño vencido**, y es verificable por el árbol:
`data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/resultados.json` **no existe en ningún commit anterior
a `c169edc`**. Tres specs humanas en **archivo propio** (`v1.0` `f54c3170…`, `v1.1` `bb9999b2…`, `v1.2` `427117ee…`)
y **ninguna editada in situ** (`E.3`, precedente `NC-0094`).

**`FP-379` pasa a `FIRMADA`** en `forense/firmas-pendientes.tsv`, con la `ENMIENDA` verbatim y su `ejecutada_en`.

---

## 5 · Un defecto de proceso propio (`NC-0308`)

`v1.0` y `v1.1` se congelaron **antes** de abrir un solo byte. **`v1.2` no:** el medidor se corrió en seco contra el
microdato real **antes** de comitear esa versión, y `E.5` lo prohíbe. Se declara, no se esconde — precedente de la
casa: `milpa/tramite-ola5-propuesta-v0.yaml:1380`.

**Lo que acota el daño, y es verificable, no una promesa:**

1. La **`§3.1`** —universo y filtros, justo la sección que produce el `NO-REPRODUCE` de §3.3— es **byte a byte
   idéntica** a la de `v1.0`, congelada en `3461c46`. `sha256` del bloque: `470824e43dce2622…` en las dos.
2. Los **grados de libertad entre `v1.1` y `v1.2` son de mesa**, literalmente escritos en la `ENMIENDA`.
3. **Nada se selló** en esa corrida en seco: ni `resultados.json`, ni `ejecucion.json`, ni `sello.json`.

**Lo único que el defecto sí tocó:** siete `RESULT` de **conteo** (`n` por marginal de 2024) añadidos tras la corrida
en seco. **No son estimandos**: son el censo que `A.13` exige de todo negativo, y sin ellos el `NO-REPRODUCE` de §3.3
no sería auditable sin recalcularlo. Se añadieron **con la declaración al lado** (spec §0.9).

---

## 6 · Los seis checks del GO de `E.5`, por nombre

| check | emisiones | árbitro |
|---|---|---|
| `PAYLOAD-RESUELTO` | 4/4 `COINCIDE` | 2/2 `COINCIDE` (uno es el `resultados.json` sellado de las emisiones, como input de repo con su `sha256`) |
| `CONTRATO-EJECUTABLE-COMPLETO` | esquema `ENDURECIDO` | esquema `ENDURECIDO` |
| `OUTPUTS-VALIDADOS` | **221/221** | **168/168** |
| `CALC-INMUTABLE` | `SIN-SELLO-PREVIO` al correr | `SIN-SELLO-PREVIO` al correr |
| `SELLO-COMPLETO` | `COINCIDE` | `COINCIDE` |
| `VERIFY-CONTEXTO+RESULTADO` | **`CONTEXTO=IDENTICO · REPRODUCE`** | **`CONTEXTO=IDENTICO · REPRODUCE`** |

`spec-check`: **40 OK · 0 FAIL · 317 718 filas examinadas** (emisiones) y **20 OK · 0 FAIL** (árbitro).

---

## 7 · `C3` · lo que costó, y lo que se conserva

* **64 capturas** `L-solo`, 8 celdas × `k = 8`, orden contrabalanceado semilla 42, **0 rechazos**, **64/64
  extraíbles** por la regla congelada `tools/extrae_l_v1_1.py::extraer_valor`.
* `modelo_real = NO-REPORTADO-POR-EL-CLIENTE` — **`FP-239`**, conocida y abierta: el CLI no emite la clave `model`
  en `--output-format json`. Se declara `null`, no se inventa.
* **18 capturas de la tanda anterior conservadas**, `SUPERADO-POR-SPEC`, con manifiesto propio
  (`corridas-L/CD-DIN-MANIFIESTO-SUPERADAS-v1_0.json`). **No se borran, no se editan, no se reusan**: la spec `v1.2`
  es la única fuente de verdad del prompt. Son historia auditable de lo que costó el diseño vencido.
* **Costo:** unidad medida **$0.282 por invocación `opus`**; la tanda superada consumió **≈ $5** de los **$18.05**
  proyectados, y la tanda vigente los 64.
* **`L+corpus`: DIFERIDO** (`NC-0311`) — por **costo y tiempo**, *no* por falta de mandato. Sólo se vuelve necesario
  si `L-solo` venciera a algún piso, y no venció a ninguno.
* **El intervalo al 80 % NO se extrae** (`NC-0307`): la regla congelada devuelve un punto, y escribir una segunda
  regla **después** de leer las 64 capturas sería post-hoc. Viaja íntegro en el texto crudo, para un sucesor que
  pre-registre la suya.

---

## 8 · Productos, y lo que NO se movió

* **Dos corridas GEN2 selladas**, `cuenta_gen2 = PENDIENTE-DE-MESA` en las dos: el encargo autoriza **medir**, no
  contar, y `FP-367`/`FP-368` piden `OBJETO` explícito que su lanzamiento no trae. **389 `RESULT` GEN2** nuevos.
* **La celda-D** se actualiza sólo en lo que el cierre autoriza: `resultado` por candidato, `momentos_holdout_refs`
  (de `RESERVADA` al id de la corrida sellada), `estado_decidibilidad: PUNTUADA`, `margen_material: 1.466786` y las
  dos estampas. **El cuerpo firmado no se edita.** 4/4 celdas-D validan contra el contrato v0.5 §3.
  *Nota:* el enum de `tests/test_celdas_d.py` no admite `SIN-CANDIDATO-SUPERIOR`, que es el **veredicto**; viaja en
  `margen_material` y en el `CALC`.
* **El catálogo de momentos estrena su primera fila con estimador derivado:** `M23`
  (`dinero.ahorro.via_informal`, `HOLDOUT`, `estatus_disponibilidad: DERIVADO-Y-SELLADO-GEN2`). Antes: **22 de 22
  `NO-VERIFICADO`**; ahora **22 de 23**. Columna `spec_ref` nueva; las 22 legado la reciben como `NO-APLICA` **sin
  que ninguno de sus otros campos cambie un byte**. Escrito a mano con tabuladores: **el módulo `csv` despoja
  comillas y corrompe los TSV de este proyecto**.
* **El test lo prueba, no la prosa:** `tests/test_celda_d_piloto_consumidor.py`, **9/9**. Verifica que
  `milpa/src/momentos.py` y `tools/corrida0.py` leen la fila **sin cambiar código**, que las 22 legado se leen
  idénticas, que `spec_ref` apunta a rutas que existen, que la regla consumidora existe de verdad en `tramite.yaml`,
  que **el muro sigue en pie** (`valor_de(M23)` lanza `HoldoutTocado`) y que el catálogo es **append-only de
  verdad**: ningún id sellado cambió de rol.
* **NO se tocó:** `milpa/tramite.yaml` · `milpa/tramite-ola5-propuesta-v0.yaml` · `milpa/src/` · el marcador · el
  crosswalk · `FP-376` (viene firmada y no se re-firma) · `tests/baseline.json`. **Adopción al motor: cero.**

---

## 9 · Concurrencia y numeración

* **Una sesión concurrente (Sonnet) escribió en esta misma rama** mientras el acto corría: `4e5f8e1` es un
  **checkpoint de resguardo** que comiteó archivos míos en vuelo **sin editarlos**. Se declara porque es un hecho del
  historial, no un problema: ninguna emisión ni ningún `R` se produjo ahí.
* **`origin/main` se movió** y ya traía `ADR-534`. Se **fusionó antes de numerar** (`d57aaad`) y el candidato pasó de
  `534` a **`535`**. Dos ramas remotas tienen `534` redactado. **Regla de la casa: renumera quien fusiona segundo.**
* **Las filas `NC` colisionaron** (`NC-0312`): la spec `v1.2`, congelada, cita `NC-0283`…`NC-0287` porque al
  redactarse el máximo era `NC-0282`; `GEN2-TRAMITE-4` ya ocupaba hasta `NC-0292`. **La spec sellada no se edita**
  (`E.3`); el mapa vive en `NC-0312`: `0283→0304 · 0284→0305 · 0285→0306 · 0286→0307 · 0287→0308` — **la cadena completa, porque renumeró TRES veces**: `0283…0287` (lo que la spec congelada cita) → `0293…0297` (primera colisión, con `GEN2-TRAMITE-4`) → `0300…0304` (segunda, con `GEN2-ESQUEMA-E1-CAPA-1` y `GEN2-EMISOR-ESTADO-1`) → `0304…0308` (tercera, con `GEN2-CORTE-EDAD-1`).

---

## 10 · Dos hallazgos abiertos sobre una guardia ajena

* **`NC-0309`** — el catálogo se declara *«append-only por construcción»* (`milpa/src/momentos.py::sellar_catalogo`),
  pero `tests/test_motor_holdout.py::test_a2` compara la firma **completa** de roles contra el commit de sello, de
  modo que **añadir un id nuevo la rompe aunque no reasigne ningún rol** — que es literalmente lo que esa guardia
  dice querer atrapar. **`tests/test_motor_holdout.py` está fuera del perímetro de este acto y NO se editó**: el
  perímetro estaba mal calculado, y saberlo vale más que el atajo. `tests/check.py` **no corre ese archivo**, así que
  no aparece en la línea base. La propiedad correcta queda comprobada **desde dentro del perímetro** por
  `tests/test_celda_d_piloto_consumidor.py::AppendOnlyDeVerdad`. Corrección mínima propuesta: que `test_a2` compare
  sólo los ids presentes en el commit de sello.
* **`NC-0310`** — `test_c` del mismo archivo **ya fallaba antes** y no lo causó este acto: el catálogo y
  `milpa/src/motor.py` entraron en el **mismo** commit `017ac24`. Verificado por comando.

---

## 11 · Sucesores

1. **Adopción** — es de mesa. `champion_actual = NINGUNO` y **nada entra al motor por este piloto**.
2. **`L+corpus`** sobre estas 8 celdas — hoy *moot*; requiere además construir la entrada del paquete-corpus.
3. **La guardia `test_a2`** (`NC-0309`), con perímetro abierto sobre `tests/test_motor_holdout.py`.
4. **Regla de extracción de intervalos de elicitación**, pre-registrada antes de mirar capturas (`NC-0307`).
5. **Consumo por el marcador por segmento**, *gated* a `NC-0275` resuelta.
6. **El hueco de vocabulario** «persistencia» en el enum `estrategia` (`NC-0305`).

**CONTADOR, sin disfraz (regla de señal v2.3):** **+2 corridas GEN2 selladas**, **389 `RESULT`**, **1 celda-D
adjudicada sin campeón**, **1 fila de catálogo con estimador derivado**. **Cero adopciones. Cero cambios al motor.**

---

## 12 · Un defecto propio que sólo se ve después de cerrar (`NC-0313`)

**`verify` sobre el `CALC` de emisiones da `NO-REPRODUCE` de forma permanente a partir del `COMMIT-3`.** Medido:

```
VERIFY CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001
  CONTEXTO: IDENTICO
  220 de 221 RESULT REPRODUCE con delta 0
  [5/5 RESULT NO-REPRODUCE] RESULT-DIN-LXE8-G-R-EXISTE-AL-CERRAR
      (tipo=texto): sellado='NO' · hoy='SI'
```

**La causa es de diseño y es mía:** ese `RESULT` es un **snapshot del estado del árbol**, no una función de los
inputs sellados. Pregunta «¿existe ya el directorio del `CALC` del árbitro?». Al sellar el `COMMIT-2` la respuesta
era `NO`; después del `COMMIT-3` es `SI`. **Por construcción no puede replicar** una vez que el árbol avanza, y el
`CALC` está sellado y es `CALC-INMUTABLE`: no se reescribe (`P4`).

**Ninguna cifra del piloto se mueve.** Los 220 `RESULT` sustantivos —`C1`, `C2`, `C3`, coberturas, marginales,
control del árbitro, `C4`, `C5`— replican **exactos**, con `CONTEXTO=IDENTICO`.

**Y el volteo no es señal de rotura: es exactamente la prueba que el falsador existía para dar.** Un `"NO"` sellado
en `c169edc` **más** un `"SI"` hoy acreditan, juntos, que `R` **no existía** cuando las emisiones se sellaron y **sí
existe** después. Eso es el orden que el acto tenía que demostrar. Lo que queda roto no es el piloto sino la
**lectura mecánica**: un lector automático de `verify` verá `NO-REPRODUCE` sobre este `CALC` y tiene que saber por
qué — por eso esta sección y la fila `NC-0313`.

**Lección para el sucesor, escrita para que no se repita:** un falsador **de orden** se asienta en `ejecucion.json`
o en el sello —donde el commit ya viaja— o como un `RESULT` de texto que **nombre el commit en que se evaluó**.
Nunca como un booleano recalculable sobre el árbol vivo.

