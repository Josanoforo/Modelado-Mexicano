# `ACTO GEN2-C0-B · LA BASE` — nota de cierre

**8 de septiembre de 2026 · CAJA (UBUNTU), corpus montado, Opus · rama `acto/gen2-c0-b` · base `origin/main = 017ac24` (`PR #645`)**

Encargo archivado verbatim (0-bis A.3): `forense/encargos/2026-09-08-GEN2-C0-B.md`.
Firmas que gobiernan, ya selladas en el árbol y sólo citadas: **«Vamos a darle»** (8/sep/2026), **D-2 / FP-348** (FIRMADA) y **`T9`** (*«Nada de promediar ni ajustar tendencias. Es modelo nuevo y va a `C0-B` con spec propia antes de que ninguna cifra suya entre a un veredicto»*).

---

## 0 · Qué se pidió y qué salió

| pieza | pedido | entregado |
|---|---|---|
| **P1** | ensayo `B` sobre remesas ENIGH 2016→2022, spec congelada, `CALC-B-0001` corre/sella/verifica | **HECHO.** `prereg-caja-B-REMESAS` v1.0 sellada; `CALC-B-0001` **SELLADA**, 90 RESULT, `verify REPRODUCE` (`CONTEXTO=IDENTICO`) |
| **P2** | una spec propia por cada regla con `serie_olas` | **HECHO (specs, sin CALC).** `prereg-caja-S17` (`R5.1`) y `prereg-caja-S18` (`R3.1`), congeladas. Ningún CALC de modulación corrió — se dice, como el encargo autoriza |
| **P3** | diseñar el campo de cita y **adoptar UNA vez de verdad** | **PARCIAL, y el resultado es un hallazgo.** El formato queda derivado y documentado; la adopción **NO se escribe**, por la rama pre-declarada `NO-ADOPTABLE-POR-GRANO`; y la derivación destapó que el `WARN` que el encargo esperaba ver bajar **no puede bajar hoy** (§5) |
| **P4** | registro y traspaso a `C0-D` | **HECHO.** §8 |

**CONTADOR, sin adornos: la mitad se movió y la otra no.** `CALC-B-0001` es una medición GEN2 real, sellada, con cadena completa y `verify REPRODUCE` — ésa es la primera mitad. La segunda —*«el número que llevaba todo el día en 211 sin silla empieza a bajar»*— **no se movió, y no por falta de trabajo: por tres hechos mecánicos del cableado que §5 mide uno por uno, con control positivo.**

---

## 1 · P1 · La serie, medida bajo GEN2 por primera vez

Proporción ponderada de hogares con `concentradohogar.remesas > 0`, ponderador `factor`, universo completo, una ola a la vez. `CALC-B-0001--098298ca327f`, sello `COINCIDE`.

| ola | `P` (GEN2) | IC95 (GEN2, bootstrap propio) | `N` | hogares expandidos | `P` GEN1 publicada | Δ |
|---|---|---|---|---|---|---|
| 2016 | 0.04745859252351374 | [0.04509768667793412, 0.049758949295394074] | 70 311 | 32 974 661 | 0.047459 | **−4.08 × 10⁻⁷** |
| 2018 | 0.04728548395278385 | [0.045101998543258824, 0.04945005747884082] | 74 647 | 34 400 515 | 0.047285 | **+4.84 × 10⁻⁷** |
| 2020 | 0.04377543852935772 | [0.04189453269692633, 0.04577270040945591] | 89 006 | 35 749 659 | 0.043775 | **+4.39 × 10⁻⁷** |
| 2022 | 0.04569409956405095 | [0.043772848428537396, 0.047770249605883566] | 90 102 | 37 560 123 | 0.045694 | **+9.96 × 10⁻⁸** |

**Control positivo, no buscado y por eso más fuerte:** las cuatro olas reproducen la serie GEN1 de `milpa/tramite.yaml:851-856` **dentro del redondeo a seis decimales con que está publicada**, y `N` y hogares expandidos coinciden **EXACTO** en las cuatro. Dos implementaciones independientes, separadas por semanas y por generación de aparato, sobre los mismos payloads, dan el mismo número. Los IC95 no coinciden dígito a dígito y **no se esperaba que lo hicieran** (§3 de la spec sellada: método de IC elegido por el ejecutor sobre ranura vacía, distinto del de la corrida GEN1); sí se solapan en las cuatro.

**Las dos guardias que PARAN se midieron y no mordieron:** `N-NULOS-REMESAS = 0` y `N-SIN-DISENO = 0` en las cuatro olas. La afirmación de `milpa/tramite.yaml` (*«`remesas` trae cero nulos en las 6 olas, verificado, no supuesto»*) **se volvió a medir en vez de heredarse**, y resultó cierta para las cuatro del universo.

## 2 · P1 · El ensayo `B` — y el hallazgo está en el brazo que se abstiene

| brazo | objetivo | estado | fuente | error (`P_B − P_obs`) | ¿dentro del IC95? | margen al borde |
|---|---|---|---|---|---|---|
| `OPERATIVO` | 2018 | **`SIN_BASELINE`** | — | — | — | — |
| `OPERATIVO` | 2020 | **`SIN_BASELINE`** | — | — | — | — |
| `OPERATIVO` | 2022 | `EMITE` | `RESULT-B-ENIGH-2020-P` | −0.001918661 | **SÍ** | **+2.59 × 10⁻⁶** ⚠ |
| `PERSISTENCIA` | 2018 | `EMITE` | `RESULT-B-ENIGH-2016-P` | +0.000173109 | **SÍ** | +0.001991465 |
| `PERSISTENCIA` | 2020 | `EMITE` | `RESULT-B-ENIGH-2018-P` | +0.003510045 | **NO** | −0.001512784 |
| `PERSISTENCIA` | 2022 | `EMITE` | `RESULT-B-ENIGH-2020-P` | −0.001918661 | **SÍ** | **+2.59 × 10⁻⁶** ⚠ |

`N-PREDICCIONES`: `OPERATIVO` = **1**, `PERSISTENCIA` = **3**. Lecturas B-bis: `OPERATIVO` = **`PISO-ALTO`**, `PERSISTENCIA` = **`MIXTO`**.

**Los dos brazos hicieron exactamente lo que §5.3 de la spec pre-declaró, incisos 1 a 4, sin una sola sorpresa** — lo cual, dicho con todas sus letras, es consecuencia de que el ensayo **no era ciego** (§7).

### 2.1 · `ROZA-EL-BORDE`, y por qué el `PISO-ALTO` no vale lo que parece

Los dos aciertos de 2022 son **el mismo acierto** (los dos brazos seleccionan la ola 2020) y caen dentro del IC95 por **2.59 × 10⁻⁶** — dos órdenes de magnitud por debajo del umbral `1e-4` que la spec declaró para el rótulo **`ROZA-EL-BORDE`**, y muy por debajo de lo que dos bootstraps con semillas distintas se separan.

**Consecuencia que hay que decir en voz alta: el `PISO-ALTO` del brazo `OPERATIVO` descansa sobre UNA sola predicción, ganada al filo.** No es una lectura robusta y no se debe citar como si lo fuera. La spec lo previó y lo prohibió contar como decisión limpia; se cumple aquí.

### 2.2 · El hallazgo real: `B` no podía hablar en dos de tres objetivos

La versión que **este corpus tiene** de ENIGH 2016 y de ENIGH 2018 declara `Modified: 2021-11-29` en sus doce archivos de metadatos: es la re-publicación de la Nueva Serie. Bajo el corte informativo que la firma `D-2`/`FP-348` exige —lo que se podía saber antes de que la ola objetivo empezara— esas versiones **no existían** en 2017-12-31 ni en 2019-12-31, y el selector las excluye por `NO_DISPONIBLE_AL_CORTE`.

Eso es un resultado sobre **disponibilidad**, no sobre persistencia, y tiene consecuencia directa para `C0-D`: **si `L` y `M` van a competir contra `B` «bajo el mismo corte informativo», en dos de estos tres objetivos el piso no es «la tasa de ayer» sino la abstención.** Competir contra una abstención no es competir. `C0-D` tiene que decidir qué significa ganarle a `B` cuando `B` se calla — y esa decisión es de mesa, no de un ejecutor.

## 3 · Dos premisas del encargo que no se reprodujeron, y un defecto del payload

1. **«ENIGH 2016-2024 ya está en corpus (34 entradas de manifiesto, verificado)».** Son **SEIS** entradas (2012, 2014, 2016, 2018, 2020, 2022), no 34, y **ENIGH 2024 no existe** en ninguna de las dos raíces — `data_raw` 0 coincidencias, y el censo del día (`forense/censo-raiz/2026-09-08.txt`, 466 en disco / 4 nuevos / 462 ya registrados) 0 coincidencias, de modo que es `AUSENTE-EN-RAIZ` y no `NO-VERIFICADO`. **No bloqueó:** el rango que el propio encargo nombra (2016→2022) está íntegro.
2. **El metadato de ENIGH 2022 declara el período de 2021.** Los **17** archivos `metadatos/*.txt` de `enigh2022_nc_csv.zip` traen `Temporal: 2021-08-11-2021-11-28`, incompatible con su propio `Identifier: …ENIGH-2022-NS` y con el patrón de sus tres olas hermanas. Es sistemático en el payload, no una errata de un archivo. **No se corrigió y no se usó:** el período operativo se deriva del año de la ola, y los cuatro `Temporal` se sellaron verbatim como RESULT de texto para que el defecto viva en `resultados.json` y no sólo en esta prosa.

## 4 · P2 · Las dos specs de modulación, y una convergencia que cambia el mapa

`prereg-caja-S17` (`R5.1`, ENIGH, 6 olas, celdas `FAM-M-05/06/07`) y `prereg-caja-S18` (`R3.1`, ENCIG, 8 olas, celdas `TRA-M-02/03/07`) quedan congeladas. **Ninguna produce cifras** y ningún CALC de modulación corrió: `T9` exige spec antes que cifra, y este acto entrega la spec.

Dos cosas salieron de escribirlas que no estaban en el encargo:

**(a) La modulación por ola y el selector `B` son la MISMA operación.** «Última ola estrictamente anterior; sin anterior, abstente» —la regla que la ADENDA de mesa del 8/sep instaló en `NC-0025`— es, palabra por palabra, lo que `seleccionar_baseline` hace. Y para `R5.1` **operan sobre la misma serie**. De ahí: lo que `CALC-B-0001` mide como error de la línea base en los objetivos 2018 y 2020 **es** el error que `M` comete al modular `FAM-M-06` y `FAM-M-07`. Un ensayo mide las dos cosas.

**(b) Y sin embargo no tienen el mismo contrato.** La modulación **no exige disponibilidad al corte**; el selector `B` **sí**. Por eso `B` se abstiene en dos objetivos donde la modulación emitiría sin parpadear. Es una diferencia real, no de implementación, y `C0-D` la hereda escrita en `prereg-caja-S17` §4 en vez de descubrirla a mitad de una comparación.

**Dos veredictos de constructibilidad (A.15), con inventario citado:**

- `R5.1`: **`CONSTRUIBLE`**, tres de tres celdas modulan (previas 2014, 2016, 2018), `N-SIN-PREVIA = 0`, `N-ORIGEN-ARBITRO = 0`. Dos reservas declaradas: el ponderador cambia de nombre (`factor_hog` → `factor`) entre 2014 y 2016, y la serie es GEN1 (bajo `E.1` una modulación que la consuma no cuenta como medición GEN2 por sí sola).
- `R3.1`: **`CONSTRUIBLE` en 2 de 3 celdas.** `TRA-M-02` sale **`NO-CONSTRUIBLE-SIN-CROSSWALK`**: su árbitro es **ENCUCI 2020** y la serie es **ENCIG**, así que modularla es un crosswalk entre instrumentos — justo lo que el selector hermano prohíbe por escrito (*«un crosswalk entre instrumentos tiene que resolverse antes y estar documentado por el consumidor: este selector no lo decide por semejanza»*). La ADENDA de `NC-0025` no cubre este caso: rotula la reutilización de `R` dentro de una serie, no el salto de instrumento. Hallazgo propio de esta spec.
- Además, `S18` deja armado el guard que hoy no muerde: tres de las ocho olas de ENCIG (2013, 2017, 2021) son `ORIGEN-ARBITRO` (`metodo: R-json`), y **ninguna de las tres celdas actuales modula con una de ellas** — pero muerde en cuanto el marco sortee una celda con árbitro en 2014-2015, 2018-2019 o 2022-2023.

## 5 · P3 · La primera silla — la derivación, y por qué la silla sigue vacía

El encargo pidió elegir el caso **por derivación, no heredado**. La derivación se hizo entera y produjo tres hechos mecánicos. Los tres se midieron con control positivo; ninguno es una impresión.

### 5.1 · El formato del campo, y la única ranura que el registro reconoce

El formato ya existe y no había que inventarlo: `corrida0_resultado_id: RESULT-…` más `corrida0_generacion: GEN2` (la señal **independiente** que `GEN2-PRE-E5` separó a propósito). Lo que **no** estaba escrito en ningún lado, y sale de esta derivación, es **dónde puede vivir**:

> El recolector de marcas (`_ids_corrida0_declarados`) construye la llave del consumidor empujando contexto **sólo** al bajar por la clave `entonces`, y tomando el nombre de `conducta`/`id`/`clave` del nodo. El recorrido de demanda (`_consumidores_conductas`) construye `milpa/tramite.yaml:{regla.id}:{conducta}`. **Las dos llaves coinciden en una sola forma: una conducta con `p:` dentro del `entonces` de una regla de `milpa/tramite.yaml`.** Cualquier cita puesta en otro sitio —una entrada de `medidos:` de `procedencia.yaml`, una entrada de `serie_olas`, un nodo del archivo de propuesta— es invisible para el registro: no genera fila en `usos` y no mueve ningún contador.

### 5.2 · Hallazgo 1 — ninguno de los 211 RESULT sellados encaja en esa ranura

Cruce mecánico: los **211** valores de RESULT GEN2 sellados contra los **191** valores materializados por consumidores activos de `milpa/tramite.yaml` + `milpa/procedencia.yaml`. **Coincidencias exactas: 0.**

No es casualidad, es diseño: los tres CALC sellados producen *deltas*, *marginales de antecedente* y *veredictos*, y **sus propias specs declaran por escrito que la regla NO se mueve** (`CALC-0002`: «no falsa `R10.3`»; `CALC-0003-v2`: «`R4.4` NO se mueve»; `CALC-0001`: «ninguna se mueve»). **Ninguno de los 211 es una probabilidad de conducta del motor**, y por lo tanto ninguno puede ocupar la única ranura que el registro reconoce.

El primero que sí lo es nació hoy: **`RESULT-B-ENIGH-2022-P`**, que mide exactamente la cantidad que `milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:recibe_remesas` materializa con `p: 0.045694` (fila `RES-0035` de `usos.tsv`, `tipo_uso = conducta_p_medido`).

### 5.3 · Hallazgo 2 — el `WARN SELLADA-SIN-ADOPTAR` **no puede bajar**: lee la llave equivocada

`tests/check.py::t35_repro` decide si un RESULT está sin adoptar así:

```
usos_por_result = Counter(u["resultado_id"] for u in usos)
...
if usos_por_result.get(rid, 0) == 0:      # rid es un id de OFERTA: "RESULT-…"
    sellada_sin_adoptar.append((rid, calc))
```

Pero `usos.resultado_id` es un id del lado **DEMANDA** (`RES-0001`…`RES-0205`), mientras que `rid` es un id del lado **OFERTA** (`RESULT-…`). **Los dos espacios de llaves son disjuntos por construcción.** Medido:

```
llaves de usos: 205 · llaves OFERTA: 348 · intersección: 0
usos con resultado_id que empieza en "RESULT-": 0
```

La marca de adopción no vive en `usos.resultado_id` sino en **`usos.corrida0_resultado_id`**. Control positivo, con la firma de mesa y la cita **simuladas en memoria** (nada escrito, `git status --porcelain` vacío después):

| escenario | adoptados | `dependencias_legacy_activas` | `SELLADA-SIN-ADOPTAR` (llave de HOY) | `SELLADA-SIN-ADOPTAR` (llave correcta) |
|---|---|---|---|---|
| árbol real | 0 | 205 | **211** | 211 |
| + firma de mesa simulada para `CALC-B-0001` | 0 | 205 | **301** | 301 |
| + firma **y cita** simuladas | **1** | **204** | **301** ← no se mueve | **300** ← sí se mueve |

**Conclusión, con el número a la vista: con el código de hoy, el `WARN` no baja ni con una adopción real y correcta.** La premisa del encargo —*«el `WARN SELLADA-SIN-ADOPTAR` baja en ≥1 por primera vez»*— **no es alcanzable por ningún acto** hasta que ese `Counter` se construya sobre `corrida0_resultado_id`. `tests/check.py` **no está en el perímetro de este acto**, así que no se toca: se mide, se declara y se pasa con sucesor nombrado (`FP-364`, `NC-0068`).

### 5.4 · Hallazgo 3 — el único candidato real choca contra el grano, y la cita NO se escribe

`CALC-B-0001` midió `RESULT-B-ENIGH-2022-P = 0.04569409956405095` contra el `0.045694` que el motor materializa: **`Δ = +9.956 × 10⁻⁸`**.

La spec `prereg-caja-B-REMESAS` §6 pre-declaró **tres** ramas antes de correr, y el resultado cayó en la de en medio: **`NO-ADOPTABLE-POR-GRANO`**. La re-medición GEN2 **sí** reproduce la cifra sellada al grano con que `milpa/` materializa sus probabilidades (seis decimales), pero **no** al grano con que `verify` compara (`tolerancia.abs = 1e-10`), y `T35 (c)` usa **esa segunda** tolerancia para comparar el valor materializado por el consumidor contra el RESULT. Escribir la cita habría metido a sabiendas un `FAIL` nuevo en la línea base.

**Por eso `milpa/` no se tocó en este acto.** No se aflojó `tolerancia.abs` para que pasara, no se redondeó ningún RESULT, no se reescribió el `p` del motor y no se firmó `data/corrida0/decisiones.tsv`. La spec dejó escrito, antes de ver el número, qué se haría en cada rama; se hizo eso.

**El diagnóstico preciso, para quien lo arregle:** un solo campo (`tolerancia.abs`) sirve hoy a dos preguntas distintas — *«¿esta corrida se reproduce a sí misma?»* (donde `1e-10` es correcto y aflojarlo es perder sensibilidad) y *«¿el consumidor materializa este RESULT?»* (donde el grano lo fija `milpa/`, en seis decimales). Separarlas —una `tolerancia_adopcion` declarada por la spec, o que la adopción compare contra el RESULT **redondeado al grano del consumidor**— desbloquea la primera silla sin tocar la reproducibilidad de nadie. Es cambio en `tools/` + `tests/`: fuera de perímetro, va con sucesor (`FP-365`, `NC-0069`).

### 5.5 · Qué queda listo para que la silla se ocupe

Todo menos el cambio de código. `CALC-B-0001` está sellada y verificada; su RESULT-2022 es la primera probabilidad de conducta GEN2 del programa; el consumidor está identificado por su fila de `usos` (`RES-0035`); el formato de la cita y su única ranura válida están derivados y escritos aquí; y la magnitud exacta del hueco (`9.956 × 10⁻⁸`) está sellada en `resultados.json`. **Con dos cambios de una línea cada uno (§5.3 y §5.4) y una fila de firma de mesa, la adopción se escribe y los tres contadores se mueven a la vez.** `NC-0053` sigue **ABIERTA**, ahora con precedente medido y patrón copiable en vez de diseño pendiente.

## 6 · Contadores

| contador | antes | después | por qué |
|---|---|---|---|
| corridas GEN2 selladas en el árbol | 102 | **103** | `CALC-B-0001` |
| RESULT sellados en el árbol | 886 | **976** | +90 |
| `N_corridas_selladas` | 3 | 3 | `cuenta_gen2 = PENDIENTE-DE-MESA`: este acto **no firma** `decisiones.tsv` |
| `N_resultados_gen2_sellados` | 211 | 211 | ídem — con la firma simulada sería **301** |
| `N_resultados_gen2_adoptados_activos` | 0 | 0 | §5.4: la cita no se escribe |
| `dependencias_numericas_legacy_activas` | 205 | 205 | ídem — con firma y cita sería **204** |
| `no_corrido_abiertas` | 36 | ver §7 | dos cierran, dos abren |

**Lo que mesa puede firmar hoy, en una línea, para que 211 → 301:** una fila en `data/corrida0/decisiones.tsv` con objeto `CALC-B-0001` y `cuenta_gen2=SI`. Escribirla desde aquí sería falsificar una firma de mesa, y ese archivo no está en el perímetro de este acto.

## 7 · Registro de filas

- **`NC-0025`** (modulación por ola demostrada sobre 2 reglas, sin spec) → **CERRADA** por `prereg-caja-S17` + `prereg-caja-S18`.
- **`NC-0028`** (B instalado y no consumido; sin cifra B real) → **CERRADA** por `CALC-B-0001`, con `snapshot` e `disponible_desde` documentados, que es exactamente lo que la fila pedía.
- **`NC-0053`** sigue **ABIERTA**, con la línea de precedente de §5.
- **`NC-0068`** (nueva): el `WARN SELLADA-SIN-ADOPTAR` lee `usos.resultado_id` en vez de `usos.corrida0_resultado_id`; no puede bajar. Sucesor: `FP-364`.
- **`NC-0069`** (nueva): `tolerancia.abs` sirve a dos preguntas distintas y bloquea la primera adopción real. Sucesor: `FP-365`.
- **`NC-0070`** (nueva): `R3.1` / `TRA-M-02` `NO-CONSTRUIBLE-SIN-CROSSWALK`; ningún CALC de modulación corrió en este acto.
- **`FP-364`**, **`FP-365`**, **`FP-366`** abiertas (§5.3, §5.4 y la firma de contador de `CALC-B-0001`).

## 8 · P4 · Traspaso a `C0-D`

Lo que `C0-D` consume de aquí, sin tener que releer nada:

1. **El piso `B`, medido.** Serie GEN2 de cuatro olas (§1) y el error de la línea base por objetivo y por brazo (§2). Es el piso común que la firma `D-2`/`FP-348` pide.
2. **Una advertencia sobre ese piso.** El `PISO-ALTO` del brazo `OPERATIVO` es **una** predicción ganada por `2.59 × 10⁻⁶` (§2.1). El brazo `PERSISTENCIA` es `MIXTO`: 2 de 3. **`C0-D` debe comparar ola a ola y nunca agregar** — es literalmente lo que la lectura `MIXTO` de la spec significa.
3. **La pregunta que `C0-D` no puede esquivar:** en 2 de 3 objetivos `B` **se abstiene** bajo el corte informativo real (§2.2). Qué significa «ganarle a `B`» cuando `B` se calla es decisión de mesa.
4. **El patrón de cita de P3**, con su única ranura válida (§5.1) y los dos cambios de una línea que lo desbloquean (§5.3, §5.4).
5. **El estado de las corroboradas post-`SUCESORAS`: hay dato, no `SIN-DATO-AÚN`.** `PR #645` fusionó antes de que este acto arrancara, así que la ORDEN DE CAJA quedó cumplida de hecho. `CALC-0003-v4` (143 RESULT, `VERIFY REPRODUCE`) es el sello vigente; `C3` y `C4` siguen **CORROBORADA** con el margen adelgazado (`C3` IC-LO +0.090029 → **+0.014702**; `C4` +0.027643 → **+0.012579**), `C1`/`b3b` sigue **NO-DISCRIMINA** y **`R4.4` no se mueve**. Reserva heredada: `CALC-0003-v3`/`v4` siguen **sin firma de contador** (`FP-362`), igual que `CALC-B-0001`.
6. **Las dos specs de modulación** (§4), con la convergencia `B` ≡ modulación y la diferencia de contrato entre las dos.

## 9 · Contaminación declarada (ADR-46)

**El ensayo `B` de P1 no fue ciego, y la vía de contaminación fue el procedimiento obligatorio del propio encargo.** Ejecutar P2 («leerla del NC completo») obligó a abrir `milpa/tramite.yaml:850-856`, que publica la serie GEN1 observada de las seis olas **con sus IC95** — es decir, la respuesta del ensayo, antes de congelar su spec.

Se declaró en `prereg-caja-B-REMESAS` §0.2 **antes** de congelar, con la tabla de los seis valores verbatim, y §5.3 pre-declaró qué era derivable de lo ya leído y qué seguía desconocido. El criterio B-bis se ancló a una cantidad **no elegible** por esta sesión —el IC95 que la propia corrida mide— precisamente para que la contaminación no tuviera dónde morder. Aun así: **mesa debe leer los aciertos de §2 sabiendo que quien escribió el criterio ya conocía la serie.**

Nivel adicional de exploración de estructura, declarado: se abrieron los diccionarios de datos y los metadatos de las cuatro olas de ENIGH (nombres de columnas, tipos, `Modified`, `Temporal`) antes de congelar la spec — necesario para nombrar variables reales, y del mismo tipo que `GEN2-E5-0` ya hizo para sus tres specs.

## 10 · A.13 — qué se examinó, y con qué

| veredicto | archivos examinados | comando |
|---|---|---|
| «6 entradas ENIGH, no 34» | `data/manifiesto.yaml` (1 572 entradas) + 399 entradas de `data_raw` | `yaml.safe_load` + `ls \| command grep -icE "enigh"` |
| «ENIGH 2024 AUSENTE-EN-RAIZ» | los 2 anteriores + `forense/censo-raiz/2026-09-08.txt` (466 en disco) | `command grep -iE "enigh"` → 0 |
| «`Temporal` de 2022 declara 2021» | 17 `metadatos/*.txt` del zip de 2022 (y 12+12+17 de las otras tres) | lectura directa del zip, conteo por valor |
| «0 coincidencias RESULT↔motor» | 211 RESULT sellados × 191 valores materializados | cruce en memoria sobre `_filas_registro` |
| «las dos llaves son disjuntas» | 205 llaves de `usos` × 348 de OFERTA | intersección de conjuntos → 0 |
| «el `WARN` no baja con una adopción» | árbol completo, 3 escenarios | monkey-patch en memoria; `git status --porcelain` vacío después |
| serie GEN2 | 4 CSV de `concentradohogar` (70 311 + 74 647 + 89 006 + 90 102 filas) | `CALC-B-0001`, sello `COINCIDE` |

## 11 · Higiene e incidentes de sesión

1. **`.claude/` espurio.** Un `cd forense/prereg-caja` (para verificar los sidecars con `sha256sum -c`) hizo que el cliente creara `forense/prereg-caja/.claude/`. Se borró limpio **dentro** del sandbox y se verificó ausente antes de cualquier `git add`. Nada se indexó: todos los `git add` de este acto son por ruta explícita, nunca `-A` ni `.`.
2. **El medidor no arrancaba, y el primer `run` falló sin sellar nada.** `medidor_fallo: AttributeError: 'NoneType' object has no attribute '__dict__'` — `_selector()` ejecutaba los bytes verificados del selector en un módulo no registrado en `sys.modules`, y `@dataclass` resuelve anotaciones por ahí. Arreglado en `COMMIT-1-bis`, **antes de cualquier sello y sin tocar semántica** (ni variables, ni universo, ni ponderador, ni transformación, ni estimando, ni los 90 RESULT, ni la tolerancia, ni la semilla). No es corrección hacia atrás: no había nada sellado que corregir.
3. **`CONTEXTO=IDENTICO` funciona.** `verify` de `CALC-B-0001` dio `REPRODUCE` con `CONTEXTO=IDENTICO` — el arreglo de `FP-358` (`GEN2-CHECADOR-2`, `PR #644`) está en `main` y este acto lo hereda, tal como la cabecera del encargo preveía en su nota de concurrencia.
4. **Un solo worktree, una sola rama, cero colisiones.** Guard 0.c limpio en los tres sitios; al arrancar no había ningún PR abierto en el repo.
