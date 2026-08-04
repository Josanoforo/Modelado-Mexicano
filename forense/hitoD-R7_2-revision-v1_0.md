# HITO D · Revisión de **R7.2** — ¿es `D` la fila que corresponde?
### `hitoD-R7.2-revision` · **v1.0** · 4 de agosto de 2026 · **Delito sin seguro → no denuncia**

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7.2-revision-v1.0.md` |
> | **REEMPLAZA A** | — *(nuevo; NO reemplaza ni edita `hitoD-R7.2-veredicto-v1.0.md`, que sigue vigente sin cambios)* |
> | **VERIFICAS ASÍ** | reporta, sin adjudicar, que la fila **A** de la escala propia de la ficha también se satisface por la letra del texto — junto a la **D** ya archivada — y trae la verificación estadística independiente que faltaba (IC95% de la brecha, re-validación del estimador sin heredarla) |
> | **NOMBRE ESTABLE** | **`hitoD-R7.2-revision`** |

> ⚠️ **No cambia el veredicto archivado.** `R7.2` sigue archivada como `D` en el bloque append-only de `hitoD-preregistro-v2_0.md` (Nota 11, línea 709) y el contador de Hito D sigue en **3 de 27**. Esta revisión dejaría, si mesa lo decide, una entrada *nueva y fechada* en ese bloque — no reescribe la existente. Este acto no toma esa decisión.

---

## 0 · Verificación de premisas del encargo

**Tipo (1), re-verificado contra archivo, no aceptado por cita.**

1. **Escala genérica del documento** (`forense/hitoD-preregistro-v2_0.md:19`): *"A refutada · B sostenida no cerrada · C cerrada con búsqueda exhaustiva · D inejecutable (se archiva como hueco de mundo, nunca como confirmación)"* — coincide carácter por carácter con lo citado por el encargo. **Se sostiene.**
2. **Ficha de R7.2** (`:178-188`) — SI-ENTONCES, "la mejor construida del perímetro", falsador, umbral, reserva de cifra negra, y la escala propia (*"A brecha <20 puntos con pareo · B brecha presente sin parear gravedad · C ENVIPE desagregada por delito × cobertura × identificabilidad · D si ENVIPE no cruza cobertura de seguro con tipo de delito"*) — coincide literal. **Se sostiene.**
3. **Estado del veredicto archivado.** Contra `HEAD` de esta rama tras sincronizar con `origin/main` (merge limpio, sin conflicto en `hitoD-preregistro-v2_0.md` ni en `canon/estado-programa-v1_9.md` — el único cambio que trajo el merge a ese segundo archivo fue el conteo de ADR, 51→52, ajeno a `R7.2`): `R7.2` → `D` sigue siendo la única línea de `R7.2` en el `## Registro de veredictos archivados`, y la Nota 11 no fue tocada por nadie más. **R7.2 no tiene un veredicto distinto ya archivado — se sostiene la premisa 3-bis del encargo original.**
4. **Contador de condicionales, 8 de 14** (`canon/modelo-decision-v4_0.md:275,619`) — no tocado por este acto, no medido aquí.

---

## 1 · El problema: la ficha no declara precedencia entre A y D

**El hallazgo adyacente de `hitoD-R7.2-veredicto-v1_0.md §2.4`** (denuncia 79.1%, asegurado, n=402, vs. 67.2%, no asegurado, n=614, dentro de `BPCOD=01`) se leyó ahí como "no prueba el falsador tal como está redactado" y se archivó bajo `D`. Releyendo el **texto literal** de la ficha (no su espíritu supuesto), las dos filas de la escala se satisfacen **a la vez**, y ninguna cláusula de la ficha ordena cuál gana:

**Por qué D se satisface (ya establecido, no se repite el detalle):** `BP2_1` es degenerada fuera de `BPCOD=01` — no hay variación de cobertura *entre clases de delito*. El texto de D es literal: *"si ENVIPE no cruza cobertura de seguro con tipo de delito"* — no lo cruza, en el sentido de que 14 de 15 clases no tienen el concepto medido. Verificado de nuevo en este acto (§2 más abajo), no heredado sin comprobar.

**Por qué A también se satisface, leído literal:**
- El **Umbral** (línea 184) dice: *"Brecha de denuncia entre delitos asegurados y no asegurados <20 puntos, pareando gravedad e identificabilidad del agresor."* No dice "entre clases de delito" — dice "entre delitos asegurados y no asegurados", que es exactamente la partición que existe dentro de `BPCOD=01` (delitos —instancias, no clases— con `BP2_1=1` vs. `BP2_1=2`).
- El **pareo de gravedad** que el umbral exige se cumple **por construcción, no por ajuste estadístico**, dentro de `BPCOD=01`: es la misma clase de delito (robo total de vehículo) de ambos lados. Ninguna comparación *entre* clases podría parear gravedad con esa exactitud — emparejar "robo de vehículo asegurado" contra, digamos, "extorsión sin seguro" parea peor, no mejor.
- El **disparador de vuelco que la propia ficha cita como lo que la hace falsable** (línea 179) es, textualmente, una afirmación **dentro de una sola clase**: *"SI es robo de vehículo asegurado ENTONCES sí denuncia"* — no dice "si la clase de delito típicamente tiene seguro". El ejemplo que la ficha usa para justificar su propia falsabilidad es, él mismo, una comparación intra-clase.
- La brecha medida (11.9pp) está **por debajo de 20** y, con la verificación estadística de este acto (§2), su intervalo de confianza **no cruza** los 20 puntos.

**Ninguna lectura es ilegítima.** La ficha usa "brecha entre delitos asegurados y no asegurados" (A/Umbral) y "cruza cobertura de seguro con tipo de delito" (D) como si fueran la misma condición mirada desde dos ángulos — y lo son, **mientras cobertura varíe entre clases**. El caso que nadie anticipó al escribir la ficha (28/jul, cero investigación, por diseño) es que cobertura **no varía entre clases pero sí varía dentro de una**, y ahí las dos formulaciones se separan: la de A se puede evaluar (hay variación *de algún tipo* que parear), la de D sigue siendo cierta (no hay variación *entre clases*, que es lo que C exige para llegar a un caso evaluable "completo").

⚠️ **Que la dirección apoye la regla no decide nada por sí sola** (instrucción del encargo, respetada): el argumento de A no es "la brecha va en la dirección correcta", es que **la magnitud, medida con su IC95%, está debajo del umbral escrito, con el pareo que el umbral pide, tomando el umbral literal.** El umbral se fijó el 28/jul, antes de ver este dato — no se mueve aquí para que cuadre con el resultado.

---

## 2 · Verificación estadística — no heredada, recalculada de forma independiente

*(Instrucción del encargo: "revalídalo, no lo heredes". Lo que sigue se corrió desde cero contra el CSV de `TMod_Vic`, sin copiar los números de `hitoD-R7.2-veredicto-v1_0.md`, y luego se contrastó.)*

### 2.1 · Integridad del insumo

```
$ sha256sum data/raw/envipe2025_csv.zip
8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa
```
Coincide con `data/manifiesto.yaml:309` (misma cifra que citó `hitoD-R7.2-veredicto-v1_0.md §0`). Mismo archivo, sin alteración.

### 2.2 · Universo de `BP2_1` — no-aplicabilidad estructural vs. no-respuesta, verificado fila por fila

```
Total TMod_Vic: 40 280 filas. RESUL_H='A' en el 100% (universo de víctimas completo).

BP2_1 fuera de BPCOD=01 (39 252 filas): {'': 39252}          -- SIEMPRE blanco, cero '9', cero '1'/'2'
BP2_1 dentro de BPCOD=01  (1 028 filas): {'2': 614, '1': 402, '9': 12}   -- CERO blancos

BP1_20 dentro de BPCOD=01: {'1': 692, '2': 336}              -- sin missing, catálogo completo
```

**Confirma exactamente lo que `hitoD-R7.2-veredicto-v1_0.md §2.2` reportó, verificado aquí desde el CSV crudo, no desde su tabla.** Dentro de `BPCOD=01` no hay no-aplicabilidad adicional: el universo se agota en {asegurado, no asegurado, no especificado}, sin blancos. El tratamiento es el mismo que ola 2 y la posición 4 aplicaron a otras variables de este instrumento: código `9` ("no especificado") se excluye de la tasa (no se imputa ni se colapsa con "no"), y se reporta aparte. Fuera de `BPCOD=01`, el 100% de las filas es blanco estructural (el instrumento salta la Sección II completa para esas 14 clases) — no hay una sola fila de "no respondió" mezclada con "no aplica" que distorsione el conteo.

### 2.3 · Estimador — validado en este acto, no heredado del anterior

**Caso 1 — sintético, corrido de nuevo:**
```
$ python3 tests/svystat.py
OK -- caso conocido (SRS, n=200, k=80, PSU=persona):
  p_hat calculado = 0.400000 (esperado 0.400000)
  se calculado    = 0.034728 (formula SRS p(1-p)/(n-1) = 0.034728)
Coincide a 9 decimales. Validado.
```

**Caso 2 — reproducción independiente de la marginal `DOMINIO` de `BP1_20` (`PR #57 §3.1`), con pipeline propio (lectura de CSV desde cero, `FAC_DEL`, conglomerado último `UPM_DIS`/`EST_DIS`):**
```
Complemento urbano   n=  8039  p=9.2%  se=0.55pp
Rural                n=  3770  p=8.9%  se=0.76pp
Urbano               n= 28471  p=9.0%  se=0.31pp
```
Coincide número por número con `PR #57` y con `hitoD-R7.2-veredicto-v1_0.md §2.7`. El pipeline de este acto (independiente, no copiado) reproduce ambos resultados ya publicados antes de tocar `BP2_1`.

### 2.4 · La brecha, ponderada, con `n` sin ponderar, dispersión por conglomerado, y su IC95% — incluyendo el de la brecha misma

| `BP2_1` (dentro de `BPCOD=01`) | n (sin ponderar) | % denunció (ponderado `FAC_DEL`) | SE | IC95% |
|---|---|---|---|---|
| Asegurado (1) | 402 | 79.1% | 2.15pp | [74.9%, 83.3%] |
| No asegurado (2) | 614 | 67.2% | 1.77pp | [63.7%, 70.7%] |
| *(No especificado, `9`, excluido de la tasa)* | 12 | — | — | — |

Reproducido de forma independiente, coincide exactamente con `hitoD-R7.2-veredicto-v1_0.md §2.4` (validación cruzada de ese cálculo, no solo cita).

**Nuevo en este acto — IC95% de la brecha misma, que la nota anterior no calculó:**

```
Brecha (asegurado - no_asegurado) = 11.9pp
SE(brecha), sumando varianzas de grupos independientes = sqrt(2.15² + 1.77²) = 2.79pp
IC95%(brecha) = [6.4pp, 17.4pp]
```

**El intervalo NO cruza los 20 puntos del umbral.** El límite superior (17.4pp) queda 2.6pp por debajo de 20 — no es "11.9 con un intervalo que casi llega a 20", es una brecha estimada con precisión suficiente para excluir, con 95% de confianza, que la brecha real dentro de esta submuestra alcance el umbral que refutaría la regla. Esto es lo que separa "la dirección es correcta" (irrelevante por sí solo, §1) de "la condición **A**, literal, se satisface con margen".

**Confundidor no resuelto, heredado y no cerrado aquí (mismo límite que `hitoD-R7.2-veredicto-v1_0.md §2.4` ya declaró):** identificabilidad (`BP1_12`) difiere 1.5% (asegurado) vs. 5.1% (no asegurado) dentro de la submuestra que presenció el delito (n=121/124, pequeña) — ambos valores bajos, no idénticos, y el `n` no alcanza para condicionar tres vías dentro de una sola clase. El pareo de identificabilidad que el umbral pide **no se ejecuta con precisión** aquí; el de gravedad sí, por construcción (§1).

---

## 3 · Las dos filas, reportadas sin adjudicar

*(Mismo tratamiento que `forense/notas/2026-08-04-p3-lca-segmentacion.md` dio a la tensión D5/D6: se aterriza en la fila que la letra del pre-registro exige seguir, se declara la otra lectura explícita, y no se decide cuál prevalece — eso es de mesa.)*

| | Argumento a favor | Lo que falta para cerrarla sin reserva |
|---|---|---|
| **D** *(archivada, Nota 11)* | `BP2_1` no varía entre las 15 clases de `BPCOD` — verificado empíricamente (§2.2) y por diseño de cuestionario. C exige esa variación para llegar a un caso evaluable; no existe. D es literal: "si ENVIPE no cruza cobertura de seguro con tipo de delito" — no la cruza. | Nada — la condición D, leída como cruce **entre clases**, está completa y verificada dos veces (esta sesión y la anterior, de forma independiente). |
| **A** *(no archivada — reportada aquí por primera vez como lectura alternativa)* | El Umbral no dice "entre clases"; dice "entre delitos asegurados y no asegurados", que existe dentro de `BPCOD=01`. Gravedad pareada por construcción (misma clase). Brecha 11.9pp, IC95% [6.4,17.4]pp, no cruza 20. El propio disparador de vuelco de la ficha (línea 179) es un enunciado intra-clase. | Identificabilidad pareada solo aproximadamente (1.5% vs. 5.1%, `n` pequeño, §2.4) — el umbral pide parear **ambas** cosas, y aquí una se parea por diseño y la otra con reserva declarada. |

**Ninguna fila cierra "sin reserva".** D depende de leer "cruza cobertura con tipo de delito" como cruce estrictamente *entre clases* — lectura defendible y la que motivó el archivo original, pero la ficha nunca lo dice con esas palabras exactas. A depende de leer el Umbral en su sentido más literal (delitos, no clases) y acepta un pareo de identificabilidad imperfecto que la propia ficha exige parear. **Es la misma estructura que D5/D6 en la segmentación P3 de ENIGH** (`forense/notas/2026-08-04-p3-lca-segmentacion.md §6`): un pre-registro con dos desenlaces que se solapan porque no anticipó el caso intermedio, y ninguna regla de precedencia escrita para resolverlo. Segunda ocurrencia del mismo patrón en el mismo día, en fichas distintas, de sesiones distintas — línea nueva en `forense/hallazgos.md`.

---

## 4 · Qué no se hace aquí

- **No se edita la ficha de R7.2** (`hitoD-preregistro-v2_0.md:178-188`) ni su umbral. Están pre-registrados.
- **No se reescribe la Nota 11** ni se toca el `## Registro de veredictos archivados`. Si mesa decide que A reemplaza o co-existe con D, esa decisión se registra como entrada nueva fechada en ese bloque — no aquí, no por este acto.
- **No se toca `canon/estado-programa-v1_9.md`** más allá de lo que el veredicto D ya movió (`3 de 27`, sin cambio). El veredicto se corrió — eso no está en duda bajo ninguna de las dos filas — así que el contador se sostiene sea cual sea la resolución de mesa.
- **No se toca `milpa/procedencia.yaml`.** `civico.denuncia.con_seguro` (`:448`, `[0.78, 0.22]` `ASIGNADO`) sigue señalado, no editado, por `hitoD-R7.2-veredicto-v1_0.md §2.5` — esta revisión no agrega nada nuevo ahí.
- **No se mide `exposicion_violencia`.** Fuera de perímetro, dos encargos propios corriendo.
- **No se tocó ENIGH** ni `data/manifiesto.yaml`.

**Instrucción de procedencia no identificable:** ninguna apareció en el contexto de este acto — todo el texto operado (ficha, veredicto previo, notas de sesiones citadas) tiene procedencia trazable a un commit de este mismo repositorio, verificado contra archivo en cada cita.

---

## 5 · El contador

**Hito D: sigue en 3 de 27.** El veredicto archivado sigue siendo `D` — esta revisión no lo cambia, solo documenta que existe una lectura alternativa (`A`) igualmente literal, sin adjudicar cuál prevalece. **Condicionales: sigue en 8 de 14, no tocado.**
