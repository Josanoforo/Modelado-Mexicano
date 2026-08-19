# ACTO FICHA-R51-D3 · COMMIT B — la corrida, con la especificación de COMMIT A tal cual

**No edita `forense/bbis-r5-1-d3-v1_0.md` (COMMIT A, `8fd94aa`).** Es el primer resultado que produce el procedimiento congelado ahí, y es el que se reporta — conforme a su §12. Si la especificación estaba mal, lo dice un commit posterior; nunca se corrige hacia atrás.

**Reproducible:** `python3 tests/ficha_r51_d3.py`. Salida cruda completa, sin editar: `forense/notas/2026-08-19-ficha-r51-d3-salida.txt`.

**Veredicto PROPUESTO: fila `B` — `EJERCIDA_INDECISA`. Mesa adjudica en acto propio; este commit no firma.** No se escribe en las columnas `estado`/`veredicto` de `forense/registro-llaves-identificacion-v1_0.md` ni en el bloque append-only de `hitoD-preregistro`.

---

## 0 · Chequeos de consistencia de COMMIT A §5.7 — corridos antes de leer ningún resultado como válido

**(c) Ancho de llave derivado, no supuesto** (mecanismo de ACTO J, no `zfill(10)` fijo):

| ola | ancho `folioviv` en `concentradohogar` | ancho `numren` en `poblacion` |
|---|---|---|
| 2018 | **10** | **1** |
| 2022 | **10** | **2** |

**Hallazgo colateral, no anticipado por la cadena `E4c` y declarado aquí:** además del truncamiento de `folioviv` en `poblacion`/`ingresos` de 2018 que Commit 3 §3.4 documentó, **`numren` también cambia de ancho entre olas** — `1` carácter en 2018, `2` en 2022. Dentro de cada ola es consistente entre `poblacion` e `ingresos` (verificado por la tasa de join, §0(b) abajo), así que no rompió nada aquí; pero un acto que normalizara `numren` a un ancho fijo heredado de una ola rompería el join persona↔ingreso de la otra **en silencio**, exactamente como pasó con `folioviv`. El script deriva ambos anchos de la tabla dueña de cada ola.

**(b) Reproducción exacta del universo de `R5.1-D2` — condición de PARO si fallaba:**

| | `R5.1-D2` Commit 8 §1 | esta corrida | |
|---|---|---|---|
| 65+ clasificables 2018 | 20,751 | **20,751** | ✅ |
| 65+ clasificables 2022 | 28,626 | **28,626** | ✅ |
| 65+ excluidas (0 filas en `ingresos`) 2018 | 1,834 | **1,834** | ✅ |
| 65+ excluidas 2022 | 1,348 | **1,348** | ✅ |
| T 2018 | 6,160 | **6,160** | ✅ |
| T 2022 (deflactado) | 8,877 | **8,877** | ✅ |
| T 2022 (nominal) | 8,922 | **8,922** | ✅ |

Reproduce exacto en las siete celdas. **No hubo PARO.** La reproducción es independiente: `tests/ficha_r51_d3.py` se escribió desde cero para este acto — la cadena `E4c` corrió con un script de scratch que nunca se commiteó (Commit 9 §8 lo declara). Es la primera vez que este universo se reconstruye de forma auditable en el árbol.

**(a) `n_estratos_singleton` = 0 / 0 en las seis corridas de DiD** (cuatro de corresidencia, dos de transferencia) — sin advertencia de singleton que leer. Se pasaron todas las unidades de la ola con `grupo=None` fuera del universo, como el contrato de `diff_ultimate_cluster` exige.

**(§5.8) Mecanismo de búsqueda declarado.** Ninguna búsqueda de este acto sobre microdato produjo un `NO-ENCONTRADO`: todas las columnas y claves que la especificación nombra (`P032`, `P040`, `P044`/`P104`, `clase_hog`, `est_dis`, `upm`, `factor`, `gasto_mon`, `tot_integ`, `edad`, `numren`) se localizaron por lectura estructurada del CSV (`csv.DictReader` sobre el ZIP, encoding `utf-8-sig`), no por `grep`. **Defecto de lectura atrapado y declarado:** los CSV de INEGI traen BOM UTF-8; leerlos como `latin-1` produce la primera columna con el nombre `'ï»¿folioviv'` y un `KeyError`/índice equivocado — se corrigió con `utf-8-sig` antes de calcular nada.

---

## 1 · Hogares mixtos — las cifras del clon, re-derivadas (COMMIT A §5.1)

| ola | umbral | hogares con ≥1 65+ clasificada | con exactamente 1 | con ≥2 | **mixtos** | **% de los de ≥2** |
|---|---|---|---|---|---|---|
| 2018 | nominal = deflactado (misma base) | 16,469 | 12,286 | 4,183 | **1,312** | **31.4%** |
| 2022 | nominal | 22,363 | 16,274 | 6,089 | **2,201** | **36.1%** |
| 2022 | **deflactado (primario)** | 22,363 | 16,274 | 6,089 | **2,194** | **36.0%** |

**Las tres cifras que el encargo cita como antecedente se re-derivan exactas.** 1,312 / 31.4% (2018) y 2,201 / 36.1% (2022 nominal) coinciden con `2026-08-11-…commit3:90`; 2,194 (2022 deflactado) coincide con `…commit4-diseno-resuelto` §2. **El antecedente era correcto** — se dice así, no se busca una discrepancia que no existe.

**Composición de los universos (COMMIT A §5.2), umbral deflactado:**

| ola | `U1` ACOTADO (sin mezcla) | `U1` T | `U1` C | `U2` completo (any-member) | `U2` T | `U2` C |
|---|---|---|---|---|---|---|
| 2018 | 15,157 | 4,509 | 10,648 | 16,469 | 5,821 | 10,648 |
| 2022 | 20,169 | 6,120 | 14,049 | 22,363 | 8,314 | 14,049 |

> ### ⚠️ El hallazgo de composición que gobierna la lectura de todo lo demás: **la poda cae ENTERA sobre el brazo de tratamiento.**
>
> `U1` C = `U2` C en las dos olas — **exactamente el mismo número de hogares de comparación**, 10,648 y 14,049. Todo el recorte se lo lleva T: **−22.5%** en 2018 (5,821 → 4,509) y **−26.4%** en 2022 (8,314 → 6,120).
>
> No es una casualidad de esta muestra: es **aritmético por construcción**. Un hogar mixto tiene, por definición, al menos una persona T — así que bajo la regla *any-member* siempre cae en T, y al excluirlo se resta solo de T. **La exclusión de mixtos no es una poda simétrica del universo: es una poda del grupo tratado.** Ni el commit3, ni el commit4, ni el benchmark, ni la firma `D-1b` lo dicen con estas palabras; queda dicho aquí porque es la forma concreta que toma, en este dato, la advertencia de Hamoudi-Thomas que §5 desarrolla.

---

## 2 · Corresidencia — las cuatro corridas (COMMIT A §5.3)

Desenlace: `concentradohogar.clase_hog ∈ {3 Ampliado, 4 Compuesto}`. Brecha = `p_T − p_C`. Dirección predicha por sustitución = la brecha **se achica** (el grupo nuevo-elegible converge hacia el siempre-elegible).

| corrida | `d_pre` (2018) | `d_post` (2022) | **DiD (θ̂)** | SE | IC95% | singleton |
|---|---|---|---|---|---|---|
| **`U1` × deflactado — PRIMARIA** | −1.85pp | −3.66pp | **−1.82pp** | 1.68pp | (−5.11pp, +1.48pp) | 0/0 |
| `U1` × nominal *(sens. i)* | −1.85pp | −3.52pp | −1.68pp | 1.68pp | (−4.97pp, +1.62pp) | 0/0 |
| `U2` × deflactado *(sens. ii)* | −2.92pp | −3.73pp | −0.81pp | 1.53pp | (−3.82pp, +2.19pp) | 0/0 |
| `U2` × nominal *(sens. i+ii)* | −2.92pp | −3.66pp | −0.74pp | 1.53pp | (−3.74pp, +2.26pp) | 0/0 |

**Escala del resultado primario, leída contra §6:** la brecha **crece** 1.82pp entre 2018 y 2022 — **signo contrario al predicho por sustitución**. Magnitud muy por debajo de 10pp, con el IC95% completo dentro de (−5.11pp, +1.48pp): no roza la frontera de 10pp por ningún extremo. **No es distinguible de cero** (el IC contiene 0) — pero para la fila A eso es una pregunta distinta de la que importa, y se dice para que no se confunda: la fila A pide `<10pp o signo contrario`, no `≠0`.

**Reproducción independiente de `R5.1-D2`, no buscada pero verificable:** las dos corridas `U2` reproducen **exactas, hasta el centésimo de punto porcentual y en los dos extremos del IC**, las dos filas de corresidencia de `E4c` Commit 8 §2 (−0.81pp con IC (−3.82, +2.19) deflactado; −0.74pp con IC (−3.74, +2.26) nominal). `U2` es, por construcción, la regla de hogar que `R5.1-D2` usó. Un script escrito desde cero reproduce el resultado de otro que nunca se commiteó.

**Efecto de la regla de hogar — descriptivo, con su reserva.** Excluir los mixtos **duplica** el punto: −0.81pp → −1.82pp, una diferencia de 1.01pp ≈ 0.6 SE de la corrida primaria. **No se reporta como un contraste estimado con su propio intervalo**, porque `U1` y `U2` son universos distintos y A-bis regla 4 prohíbe reconciliarlos: la comparación es descriptiva y se lee como *efecto de la regla*, nunca como verificación cruzada. Lo que sí se puede afirmar sin cruzar universos: **los cuatro puntos y sus cuatro intervalos caen en la misma fila de la escala**, y ninguno se acerca a 10pp. **La elección de umbral no mueve nada** (0.14pp entre deflactado y nominal en `U1`, 0.07pp en `U2`) — las 45 personas reclasificadas no alcanzan a mover ninguna conclusión, igual que en `R5.1-D2`.

---

## 3 · El marginal recalculado sobre el universo ACOTADO (COMMIT A §5.4 — A-bis regla 4)

Proporción ponderada de `clase_hog ∈ {3,4}`, **sin partir por grupo**, sobre los tres universos:

| ola | `U1` (ACOTADO) | `U2` (any-member) | universo completo de hogares |
|---|---|---|---|
| 2018 | **0.4232** *(N̂ = 6,882,108 · n = 15,157)* | 0.4182 *(N̂ = 7,474,924 · n = 16,469)* | 0.2525 *(N̂ = 34,400,515 · n = 74,647)* |
| 2022 | **0.4126** *(N̂ = 8,441,709 · n = 20,169)* | 0.4099 *(N̂ = 9,370,342 · n = 22,363)* | 0.2526 *(N̂ = 37,560,123 · n = 90,102)* |

**Por qué la firma exigía este recálculo, visible en la tabla:** el universo con personas 65+ corresiste a **~42%**, y el universo completo de hogares a **~25%** — **17 puntos porcentuales de diferencia**. Un estimando de `U1` reconciliado contra el marginal poblacional de hogares no valida ni invalida nada: compara dos poblaciones. Los tres se reportan juntos, con su `N̂` y su `n` pegados, y **no se restan uno de otro**.

Dato descriptivo que la tabla deja ver y que no estaba en la lista de nadie: la corresidencia del universo completo es **plana entre olas** (0.2525 → 0.2526), mientras la de los universos con 65+ **baja** ~1pp. No se interpreta aquí — es descriptivo, sobre universos que no se comparan entre sí, y no entra a ninguna fila de la escala.

---

## 4 · Transferencia `P040` — intocado por la regla de hogar (COMMIT A §5.5)

| corrida | `d_pre` | `d_post` | **DiD (θ̂)** | SE | IC95% | singleton |
|---|---|---|---|---|---|---|
| `U3` × deflactado | −16.28pp | −13.96pp | **+2.32pp** | 0.9095pp | (+0.54pp, +4.10pp) | 0/0 |
| `U3` × nominal | −16.28pp | −13.96pp | +2.32pp | 0.9089pp | (+0.54pp, +4.10pp) | 0/0 |

**Reproduce exacto** `E4c` Commit 8 §2, como tenía que hacerlo: ninguna de las dos reglas de hogar toca este desenlace, que es persona-nivel. La brecha **se achica** 2.32pp — dirección predicha, magnitud <10pp, decisivo frente a 0 y frente a 10pp.

**Enganche entre desenlaces (Commit 4 §6) — verificado, no aplica.** El patrón que activaría la lectura *"confundido por composición del hogar"* exige que **ambos** desenlaces se muevan en la dirección de convergencia a la vez. Aquí no ocurre: transferencia converge (+2.32pp), corresidencia **diverge** (−1.82pp). Direcciones distintas — la reserva no se activa. Con la poda de `U1` la divergencia es mayor que en `R5.1-D2`, así que la conclusión de Commit 8 §7 se sostiene con más holgura, no menos.

---

## 5 · La compuerta de monto — recalculada sobre el universo primario (COMMIT A §5.6)

Razón = media ponderada(`P104`) / media ponderada(`gasto_mon` per cápita), trimestral/trimestral, pesos corrientes de 2022, factor de `concentradohogar`. **Misma metodología sellada de Commit 9 §4 — no una medida nueva.**

| población | n elegibles | n con `P104`>0 | recepción efectiva | `P104` medio | `gasto_mon` pc medio | **RAZÓN** |
|---|---|---|---|---|---|---|
| **(a)** `R5.1-D2` — personas T (todas) | 8,877 | 6,497 | 73.2% | $5,100.83 | $17,560.54 | **29.05%** |
| **(b)** `R5.1-D3` — personas T en hogar T de `U1` | 6,654 | 4,632 | 69.6% | $5,076.66 | $19,193.61 | **26.45%** |

**(a) reproduce `R5.1-D2` con exactitud de centavo** — $5,100.83, $17,560.54 y 29.05% coinciden dígito por dígito con Commit 9 §4 y Commit 10 §2.

**Reproducción del intervalo, también exacta.** El IC95% de la razón se calculó con la linealización estándar de cociente (`z_i = w_i·(monto_i − R̂·gasto_pc_i)/Σ(w·gasto_pc)`) reducida por conglomerado último — implementada desde cero en este acto, sin ver el script de Commit 10 (que nunca se commiteó). Resultado para (a): **IC95% = (26.16%, 31.94%), SE = 1.47pp, 93 estratos singleton** — las cuatro cifras coinciden **exactas** con la "variante A — solo dominio" que Commit 10 §3 publicó. *(Se marca `EXPLORATORIA`: el IC de la razón no está en la lista cerrada de COMMIT A §5.6 — se calculó porque sin intervalo una compuerta no se despeja, y se etiqueta en vez de colarse.)*

**El resultado nuevo: (b) = 26.45%, IC95% (23.15%, 29.75%), SE 1.69pp.**

> **La compuerta NO se sostiene, y se aleja del piso en vez de acercarse.** Recalcular el monto sobre el universo primario de `R5.1-D3`, como A-bis regla 4 exige, **empeora** la razón: de 29.05% a **26.45%**, con el intervalo **entero** por debajo del piso heredado de 33% — y más lejos de él que el de `R5.1-D2` (límite superior 29.75% vs. 31.94%).

**Por qué baja, medido y no supuesto.** El numerador casi no se mueve ($5,100.83 → $5,076.66, −0.5%); el que se mueve es el **denominador**: el `gasto_mon` per cápita medio sube de $17,560.54 a $19,193.61 (**+9.3%**). Es consecuencia directa del hallazgo de composición de §1: los hogares que la poda elimina son hogares con **dos o más** personas 65+ (todo mixto tiene ≥2 por definición) — hogares más grandes, y por tanto de gasto per cápita **más bajo**. Excluirlos deja un universo de hogares tratados sistemáticamente **más pequeños y con más gasto por cabeza**, contra el cual la misma pensión cubre una fracción menor.

**Medianas, secundarias y no promovidas** (§5.6 lo exigía por escrito): (a) mediana `P104` $5,606.55 / mediana `gasto_mon` pc $12,225.05 = 45.86%; (b) $5,576.08 / $13,417.31 = 41.56%. Ambas quedan por encima del piso, ambas siguen siendo secundarias. *(Commit 10 §2 estableció que el "48.6%" de Commit 9 era una razón de medianas **sin ponderar**, no un estimador de diseño; mi cálculo usa medianas ponderadas por `factor` y da 45.86% para la misma población (a), contra los $12,226.06 interpolados de Commit 10 — la diferencia de un peso en el denominador es interpolación vs. función escalón, y la razón coincide en 45.86%. No se promueve ninguna de las dos.)*

---

## 6 · La advertencia Hamoudi-Thomas, al acta, con su dirección — y lo que este dato le añade

Firma `D-1b`, verbatim: *"la exclusión condiciona en composición endógena y sesga hacia cero, por eso la sensibilidad no es opcional."*

**Lo que la firma predice:** si el programa **causa** hogares mixtos (una persona recién elegible acaba viviendo con otra que ya lo era), excluirlos borra eventos de corresidencia inducidos por el tratamiento y **sesga hacia cero** una señal de sustitución — conservador para `EJERCIDA`.

**Lo que este dato añade, y hay que decirlo sin forzarlo a confirmar la predicción:**

1. **La poda es asimétrica y entera sobre el brazo tratado** (§1): −22.5% / −26.4% de T, 0% de C. La advertencia de endogeneidad no es abstracta aquí — el condicionamiento se aplica, literalmente, solo a las unidades tratadas.
2. **El punto no se acercó a cero: se alejó** (−0.81pp → −1.82pp). Eso **no refuta** a Hamoudi-Thomas: su predicción es sobre el sesgo de una **señal de sustitución**, y aquí no hay ninguna — el signo es contrario a sustitución en las cuatro corridas. Lo que la poda hizo fue agrandar un efecto **de signo contrario**, que no es lo que la advertencia gobierna.
3. **Ninguno de los dos puntos es distinguible de cero**, y la diferencia entre ellos (1.01pp) es menor que un SE. **La lectura honesta es que esta corrida no puede decidir si la poda sesgó nada** — tiene el signo "equivocado" para la predicción y la magnitud dentro del ruido. Se dice así.
4. **Donde la poda sí movió algo medible es en la compuerta de monto** (§5): −2.60pp de razón, por composición de tamaño de hogar. Ése es el canal por el que la exclusión de mixtos afectó de verdad el veredicto de este diseño — y **no** es el canal que la advertencia anticipaba.

**Por eso la sensibilidad no era opcional, y el registro lo muestra:** sin `U2` corriendo al lado, este acto habría reportado −1.82pp como si fuera el resultado, sin saber que la regla de hogar duplica el punto ni que el brazo de comparación no se toca.

---

## 7 · Reservas de identificación — A-bis, tal como COMMIT A §7 las dejó escritas

- **Llave (ii) de `ADR-57(c)`** (experimento natural con grupo de comparación sobre encuestas repetidas). **Supuesto de tendencias paralelas: escrito, NO verificado.** El placebo 2014→2018 que Commit 4 §4.3 declaró factible **sigue sin correr** — reserva, no ejecución. Un DiD sin este supuesto verificado es una asociación con más pasos; queda escrito, no comprado.
- **A-bis regla 2:** no se estratificó por ningún eje. Los dos declarados en Commit 1 §2.7 (ámbito urbano/rural, sexo) **no se ejecutaron**.
- **A-bis regla 3:** los DiD son diferencias de proporciones (pp); la razón monto/gasto es un cociente adimensional con su piso propio. **No se comparan entre sí** — son compuertas independientes.
- **A-bis regla 4:** el estimando primario está **acotado a `U1`** ("hogares 65+ sin mezcla T/C"), el rótulo viaja pegado a toda cifra de §2 y §5(b), y el marginal se recalculó sobre ese universo (§3).
- **Identificación de `P032`:** exitosa por el mismo criterio ya declarado en Commit 1 §2.1 — **inferencia por exclusión** (los programas no contributivos tienen código propio, `P044`/`P104` y `P045`), no etiqueta literal "contributivo" en el catálogo. Mismo estatus epistémico que en `R5.1-D2`: ni mejorado ni degradado por este acto.
- **Tamaño de muestra:** ninguna celda bajo el 5% del universo relevante. La más chica, `U1`-T-2018, es 4,509 de 15,157 = **29.7%**. **Sin fila `D` por tamaño.**

---

## 8 · Veredicto PROPUESTO — la escala de §6 aplicada en su orden

Precedencia sellada: **`A → E → B → C → D`**.

- **`A`** — conjunción de tres. (1) DiD <10pp o de signo contrario: **se satisface** (corresidencia −1.82pp, signo contrario; transferencia +2.32pp, <10pp y decisivo). (3) identificación exitosa: **se satisface**. (2) **monto documentado como suficiente: NO se sostiene** — 26.45% sobre el universo primario, IC95% (23.15%, 29.75%) entero bajo el piso de 33%. **`A` no se satisface.**
- **`E`** — exige DiD >20pp decisivo. Ninguna corrida se acerca. **No se satisface**, y además heredaría la misma cláusula de monto.
- **`B`** — *"DiD entre 10 y 20pp, **o monto insuficiente**, o las dos medidas dan direcciones opuestas sin significancia clara"*. **Se satisface por la cláusula de monto insuficiente**, que por la precedencia sellada gana sobre `A` y sobre `E` **sin excepción por magnitud del DiD**.
- **`C`/`D`** — no se llegan a evaluar (la precedencia se detiene en `B`).

> ### **Fila `B` — Ambiguo, no refuta ni confirma. Vocabulario del registro de llaves: `EJERCIDA_INDECISA`.**
>
> **Igual que `R5.1-D2`, por la misma compuerta y por una razón que este acto midió: no es que el criterio firmado haya fallado — es que no gobernaba esa compuerta.**

**Regla de adjudicación entre corridas, declarada al sellar y respetada:** adjudica la primaria (`U1` × deflactado). **Las tres sensibilidades caen en la misma fila** — no hay discrepancia de fila que reportar como reserva. La discrepancia que sí hay es de **magnitud** (el punto se duplica al podar), y está reportada en §2 y §6 con su reserva de universo.

**La firma que falta, con su renglón abierto.** El veredicto de arriba es **PROPUESTO**. La firma de mesa que lo convertiría en registro —`estado`/`veredicto` de la fila `R5.1-D3`, y `llaves de identificación ejercidas` de `1 de 3` a `2 de 3`— queda anotada como **`FP-69`, ABIERTA**, con el precedente exacto de cómo se firma (`ACTO ADJ-4` sobre `R5.1-D2`, 13/ago/2026) y con la reserva que debe viajar con ella: **el supuesto de tendencias paralelas está escrito y NO verificado** — el placebo 2014→2018 sigue sin correr.

**La contraparte de A-bis, verificada explícitamente:** ¿algún punto satisface un umbral con un IC que no lo despeja? **No, para lo que decide.** El umbral de 10pp lo despejan los cuatro IC de corresidencia y los dos de transferencia por márgenes amplios; el piso de 33% lo despeja por debajo el IC de la razón (b), entero. La falta de significancia de la corresidencia frente a **cero** es una pregunta distinta de si cruza **10pp**, y no bloquea esta fila.

---

## 9 · Lo que este acto NO movió, y el contador que no puede mover

**Contadores movidos por COMMIT B: cero.** `13 de 27` (Hito D), `11 de 15` (condicionales), `15 coeficientes, cero medidos`, `4 de 144` — intactos. El único contador que este acto tocó fue el **denominador** de `llaves de identificación ejercidas` (`1 de 2` → `1 de 3`), en COMMIT A, al dar de alta la fila `R5.1-D3` como `SELLADA_NO_EJERCIDA`. **El numerador no se mueve porque este acto propone y no firma.**

**La premisa "14 de 27" del encargo y de `ADR-110(a)` no se sostiene** — declarado ya en COMMIT A §10, antes de ver ningún resultado, y no reconstruido después:

1. `ADR-67(c)` selló, verbatim, que un veredicto del diseño por regla de elegibilidad *"NO cuenta como veredicto de `R5.1`"*, que *"el denominador **27 no se toca**"* y que la métrica del renglón nuevo es *"llaves de identificación ejercidas"*.
2. Con independencia de la firma, **la mecánica lo impide**: `T18`/`T20` derivan el contador de un `set` de identificadores `RX.Y` extraídos con `_VEREDICTO_CANONICO`; `R5.1` **ya está en ese conjunto** desde el 4/ago/2026 (veredicto `A`, `ADR-58(c)`), así que una línea nueva para `R5.1` no incrementaría nada — y una línea escrita `` `R5.1-D3` → veredicto `X` `` **no coincide con el patrón** y entraría **invisible** al bloque append-only, sin disparar siquiera el guardia de forma sospechosa.

Registrado como **`FP-68`, ABIERTA**. No se adjudica desde aquí: decidir si `ADR-110(a)` corrige a `ADR-67(c)` o si arrastraba una premisa vencida es firma de mesa.

---

## 10 · Lo que queda abierto — nombrado, no despachado

- **La compuerta de monto sigue siendo lo que bloquea a `R5.1`, y ningún diseño de esta familia la ha atacado.** `R5.1-D2` y `R5.1-D3` comparten población de tratamiento a nivel persona (`P032` > umbral) — personas con pensión contributiva, por construcción mejor cubiertas que la población que motivó los estudios de crowding-out. El encargo del 13/ago pedía un instrumento que *"ataque eso o repetirá el resultado"*; la firma `D-1` no lo atacaba, y el resultado se repitió. **Un `R5.1-D4` que quiera salir de `B` tiene que mover la definición de tratamiento o el criterio de monto, no la regla de hogar ni el deflactor.** Es hallazgo de este acto, no propuesta de encargo: no se abre fila de mesa por esto — se deja escrito para quien redacte el siguiente.
- **Placebo 2014→2018:** declarado factible por Commit 4 §4.3, sigue sin correr en ningún acto.
- **Estratificación por los dos ejes de Commit 1 §2.7:** sigue sin correr.
- **`numren` de ancho variable entre olas** (§0): declarado aquí, sin auditar si algún acto previo del repo lo normalizó a un ancho fijo heredado. Mismo tratamiento que Commit 3 §3.4 dio a `folioviv`: se deja constancia, no se audita el resto del repo desde este perímetro.

---

## 11 · Módulo de auditoría de rigor extremo — no aplica

Este artefacto **no afirma nada sobre México** en el sentido del Bloque B: es un registro de medición, y el módulo es obligatorio solo en reports temáticos, integrador, modelo de decisión y validaciones forenses (`instrucciones-proyecto` v2.3, refinado). Se anota que no aplica en vez de omitirlo en silencio.

**Contadores que este COMMIT movió: cero** (v2.3 exige decirlo en una línea, sin justificarlo).

**Cantidad estimada y su escala (v2.4):** los seis DiD están en **puntos porcentuales de diferencia de proporciones**, sobre los universos `U1`/`U2`/`U3` declarados en COMMIT A §3; la razón monto/gasto es un **cociente adimensional** de dos medias ponderadas trimestrales en pesos corrientes de 2022. No se comparan entre sí.

---

*COMMIT B del `ACTO FICHA-R51-D3` (Bloque A-bis/D). No edita COMMIT A. Primer y único resultado que produce el procedimiento — no se corrige hacia atrás. Veredicto PROPUESTO a mesa: fila `B`, `EJERCIDA_INDECISA`. Este acto no firma.*
