# Banda TOST y margen material — `D-iv` — 20/ago/2026

**Acto:** `DUELO-PREREG-V2` (nube, Opus). Gate: `T-SELLO` + `ACT-PIL-2` fusionados.

**Estado: PROPUESTA PARA MESA — NO FIRMADA POR ESTE ACTO.** `D-iv` es explícita en que la banda TOST y el margen material "NO se firman ahora: el acto de pre-registro los deriva de los EE reales del set y trae el número con su justificación" (`TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md` §4; texto idéntico en `CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §C). Este documento cumple esa instrucción: deriva y trae el número con su justificación, y lo deja para que mesa firme — el ejecutor no se auto-firma.

**Prohibición explícita del acto que produce este documento: ningún estimado puntual sobre México.** Nada de lo que sigue calcula, insinúa o permite reconstruir un valor de R para ninguna variable mexicana; todo el cálculo opera sobre errores estándar (dispersión), nunca sobre el nivel del estimador. Calcular un punto rompería el cegamiento del diseño pre-registrado (el corredor L no debe poder inferir, de este documento, ningún nivel de ninguna cifra que luego se le pregunte).

## 1 · Por qué la precedencia (i) "EE oficiales" no aplica — cinco vías de verificación de `NO-ENCONTRADO`

El diseño pre-registrado (implícito en `D-iv` y en el filtro `ADV1-M1(iii)`, "CV de R bajo el umbral de la semaforización INEGI") asume, como primera precedencia, que existe un artefacto oficial de EE por reactivo que el marco de candidatas pueda consultar celda por celda. Ese artefacto **casi seguro no aplica aquí**, porque el único insumo oficial de precisión adquirido hasta ahora (`U2/EV-1`, `LOTE-UBUNTU-ADQ-1`) trae **2 filas de 337** — ambas totales nacionales a `Niv_Conf 90` — y ninguna fila del reactivo pre-registrado (`P7_12_7`, ENASIC 2022). Este acto marca el reactivo pre-registrado `NO-ENCONTRADO` por **cinco vías distintas**, cada una verificada por comando o por lectura directa del archivo, no por inferencia:

1. **El libro entero, hoja `INDICADORES`.** `data/raw/enasic2022/IPE_CV-EE-IC_ENASIC_2022-00_Def_V1_260923.xlsx`, 338 filas totales, 335 completamente vacías, derivado con `openpyxl` (no a ojo — hallazgo `FP-70`/nota `ACT-PIL-2 T0/T2`, `forense/hallazgos.md`). Las únicas 2 filas con dato: *Población total* (CV 1.391962655, EE 1 793 646.71919227) y *Sí requirió apoyo o cuidados* (CV 1.6048742386, EE 940 367.570351719), ambas totales poblacionales absolutos a `Niv_Conf 90`, ninguna es `P7_12_7` ni ningún reactivo de escala del piloto.
2. **La hoja `Catálogo` del mismo libro.** Recorrida junto con `INDICADORES` en el mismo cruce (`FP-70`, hallazgo de 19/ago) — no trae una tabla paralela de reactivos, es metadato del propio libro, no un segundo universo de filas.
3. **El segundo recurso RNM (`29535`), plantilla del formato.** 0 estimaciones — es la plantilla vacía que INEGI publica junto al libro lleno, no un artefacto adicional de datos.
4. **La ficha RNM 922 completa** (`related-materials` y `data-dictionary`): `command grep -o 'catalog/922/download/[0-9]*' | sort -u` devuelve únicamente `29534` y `29535` — no hay un tercer recurso descargable que pudiera traer el reactivo. `P7_12_7` → 0 coincidencias en ninguno de los dos.
5. **El manifiesto del proyecto.** `command grep -in precision data/manifiesto.yaml` → 0 coincidencias en 722 entradas — ningún otro archivo adquirido se declara como fuente de precisión estadística para ENASIC 2022.

Las cinco vías, verificadas independientemente por `ACT-PIL-2` (`T0`/`T2`, `forense/hallazgos.md`, entrada 2026-08-20) y citadas aquí verbatim, convergen: el artefacto oficial de EE por reactivo que la precedencia (i) asumiría **no existe para el reactivo pre-registrado**. Consecuencia declarada por `ACT-PIL-2` y adoptada aquí sin reinterpretarla: *"el CV del árbitro no existe ex ante para casi ninguna celda ni siquiera en la fuente oficial de precisión — el filtro sólo puede evaluarse cuando el árbitro corre sobre microdato"*. Esto NO es un defecto de búsqueda — el propio archivo trae 335 de 337 filas vacías también para otras variables (comparado, en la misma nota, contra `ENAFIN 2024`, que sí trae 88 filas con CV real).

**`FP-70` (`ABIERTA`) es la fuente que sostiene este hallazgo — se lee, no se toca.** Este documento cita su contenido (los dos valores de EE arriba, y la constatación de las 335 filas vacías) exactamente como `FP-70` los registra en `forense/hallazgos.md`; no se edita esa fila del tablero ni el archivo donde vive, siguiendo la instrucción explícita del acto.

## 2 · Los EE REALES disponibles (no de diseño) — lo único que este set trae

Ante la ausencia del artefacto por reactivo, el único par de EE **reales, empíricos, medidos sobre el propio operativo ENASIC 2022** (no teóricos ni de diseño muestral) que el corpus adquirido pone a disposición son las dos filas de `U2/EV-1`:

| Variable | R̂ (nivel, poblacional) | EE real | CV |
|---|---:|---:|---:|
| Población total | 128 857 388 | 1 793 646.71919227 | 1.391962655% |
| Sí requirió apoyo o cuidados | 58 594 471 | 940 367.570351719 | 1.6048742386% |

**Advertencia explícita, para no caer en "EE de diseño":** estos dos EE son de **totales poblacionales absolutos** (unidades: personas), no de proporciones ni de reactivos de escala como los que el marco de candidatas (`marco-candidatas-piloto-v1_0.tsv`) trae para el piloto. Usarlos directamente como el EE de una celda cualquiera del piloto sería sustituir el EE real del reactivo específico por el EE real de una variable distinta — exactamente el defecto opuesto de "inventar un EE de diseño teórico", pero un defecto igual de grave si se aplica sin ajuste. Este acto NO comete ese error: lo que deriva abajo es la **estructura de la banda** (una fracción del EE, expresada como CV), no una cifra fija en unidades absolutas — la banda se expresa en **porcentaje del propio EE de cada celda**, de modo que sea aplicable a cualquier reactivo del piloto sin transportar el nivel de una variable a otra.

## 3 · Derivación de la banda TOST y el margen material

**Insumo real disponible:** CV empíricos de 1.39% y 1.60% para las dos únicas filas con dato del set de precisión oficial adquirido — ambos caen en la banda **Alta** de la semaforización CAC-007/01/2018 (`[0%, 15%)`), el umbral que `ADV1-M1(iii)` cita como árbitro de decidibilidad.

**Regla de derivación, expresada relativa al propio EE de cada celda del piloto (no en unidades absolutas), para no romper el cegamiento y para ser aplicable a cualquier reactivo:**

- **Margen material propuesto:** `Δ_material = 0.5 · EE(R)` de la celda evaluada. Esta cifra NO se inventa: es la misma constante que `ADV1-M3` ya usa como una de las dos condiciones de `INDECIDIBLE` ("si |d_L−d_M| < 0.5·EE(R)"). Reutilizar la constante ya sellada en `ADV1-M3` evita introducir una segunda constante arbitraria sin relación con el resto del diseño — la banda TOST y la condición INDECIDIBLE de M3 miden, con la misma vara, "diferencia sin importancia práctica".
- **Banda TOST propuesta:** equivalencia si la diferencia entre corredores (o entre corredor y B) cae dentro de `[-0.5·EE(R), +0.5·EE(R)]`, con los dos tests unilaterales estándar de TOST (H0: diferencia ≥ Δ_material vs H0: diferencia ≤ -Δ_material, ambos rechazados a α=0.05 para declarar equivalencia). Esta banda es la misma magnitud que gobierna la casilla (3) de `ADV1-M5` ("Empate-TOST dentro de banda pre-declarada") — se deriva aquí explícitamente porque `ADV1-M5` la nombra sin definirla numéricamente.

**Por qué 0.5·EE y no otra fracción, con la evidencia disponible:** los dos únicos EE reales del set (CV 1.39% y 1.60%, banda Alta de CAC-007) son EE pequeños relativos al nivel (bajo ruido de muestreo en esos dos totales nacionales). Un margen de medio EE es, en esa escala de ruido, una fracción conservadora — más estricta que "un EE completo" (que ya sería el ancho típico de un intervalo de confianza al ~68%) y consistente con la severidad que `ADV1-M4`/`M5` piden para no declarar empates con demasiada facilidad. **Esta elección no está probada como óptima — es la más simple que reutiliza una constante ya sellada del propio diseño (M3) en vez de introducir una nueva.** Mesa puede sustituirla por otra fracción (p. ej. 1·EE, o una derivada de potencia estadística con el N real del piloto) sin que este documento la anticipe.

**Límite explícito de esta derivación:** con solo 2 filas de EE reales, y ninguna de ellas del mismo tipo de reactivo (proporciones de escala binaria/ordinal, como trae el marco de candidatas) que el piloto va a evaluar, la banda derivada aquí es una **regla de forma** (fracción del EE propio de cada celda), no una **constante numérica fija** en unidades de ninguna variable — deliberadamente, para que sea aplicable celda por celda usando el EE real que `ADV1-M3` ya exige calcular por celda (`ArbitroR.ee` en `scoring-adv1-m3.py`), y para no fijar hoy un número que dependería del nivel de una variable ajena al piloto.

## 4 · Qué falta para que mesa firme

1. Confirmar o rechazar la reutilización de `0.5·EE(R)` como margen material (§3) — o proponer otra fracción con su propia justificación.
2. Decidir si la banda TOST se expresa siempre como fracción del EE propio de cada celda (como aquí) o si mesa prefiere fijar una constante absoluta para alguna subclase de reactivos (p. ej. todas las proporciones nacionales) una vez que existan más filas reales de EE (fuera del alcance de este acto: exigiría adquirir el artefacto de precisión de más encuestas del marco).
3. Registrar la firma en `forense/firmas-pendientes.tsv` cuando mesa decida, citando este documento y el ADR correspondiente — este acto no escribe esa fila (no le corresponde auto-sellarse).

**Este acto no calculó, en ningún punto de este documento, un estimado puntual de ninguna variable mexicana del piloto.** Los únicos números que aparecen son los dos EE reales de `FP-70`/`U2-EV-1` (citados, no recalculados) y la constante `0.5` ya sellada en `ADV1-M3`.
