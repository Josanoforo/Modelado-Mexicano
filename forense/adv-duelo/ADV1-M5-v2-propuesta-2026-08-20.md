> **Cabecera de procedencia (aparato de este acto, `SELLA-M5-V2`, no del adjunto):**
> - **Dirección:** adjunto entregado por mesa al lanzar este acto (`SELLA-M5-V2`, nube, Opus, 20/ago/2026).
> - **Benchmark web:** 20/ago/2026, cuatro campos — ver §9 del cuerpo abajo para las fuentes citadas.
> - **`sha256` del adjunto original** (nombre de subida ADV1M5v2propuesta20260820.md, tal como llegó): `f4d8ad2f282fb0c4f82cc6803a817342acd0fbbd8f539a4a6d84981fc1a536cf`
> - **`diff` contra el adjunto:** ninguna diferencia de cuerpo — esta cabecera y el salto de línea final son la única diferencia admisible (doctrina `FP-57`).

---

# `ADV1-M5 v2` · PROPUESTA — eje unificado, márgenes declarados y secuencia fija

> | | |
> |---|---|
> | **ESTADO** | **PROPUESTA. NO SELLADA.** Requiere firma de mesa sobre §4 (la secuencia) y §3 (dónde se dibujan las líneas). El ejecutor que la reciba **no la sella por su cuenta**. |
> | **QUÉ ES** | Una **capa de traducción** sobre `ADV1-M5`, no un reemplazo. El párrafo original de `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B **queda intacto y sigue siendo la fuente**; esta capa dice cómo se computa. Patrón `A.10` corolario 1: lo superado no se edita, se re-emite con alcance nuevo. |
> | **POR QUÉ** | Las cinco casillas se solapan porque miden **tres comparaciones sobre tres ejes** (L vs M · L/M vs B · L/M vs R). `DUELO-PREREG-V2` paró correctamente ahí y abrió la pregunta a mesa (`forense/prereg-duelo-v2/mesa-pendientes.md` §2). |
> | **PROCEDENCIA DEL DISEÑO** | Benchmark web, 20/ago/2026, cuatro campos. Fuentes en §9. **Ninguna cifra de este documento se inventa**: `Δ` lo deriva el acto de pre-registro (`D-iv`) y lo firma mesa. |

---

## 1 · Qué se conserva verbatim y qué se traduce

**Lo que se conserva sin tocar una palabra** — es lo que `D-ii` firmó y es lo más valioso del párrafo original:

| Cláusula original (verbatim del careo §B) | Estado en v2 |
|---|---|
| (1) *«NO licencia "el motor sobra" (procedencia, contrafactuales e interpretabilidad no se puntuaron)»* | **Conservada literal**, atada a su posición |
| (2) *«NO licencia "M es bueno" salvo skill material sobre B»* | **Conservada literal — y ahora la impone la mecánica**: el paso 1 de la secuencia es esa condición. Deja de ser advertencia y pasa a ser compuerta |
| (4) *«ninguno utilizable v1; re-tierización dirigida sin coronación»* | **Conservada literal** |
| (5) *«el fenómeno no es predecible con estas herramientas hoy; consecuencia propia, y es la casilla que el FFC dice esperar»* | **Conservada literal** |
| Cláusula de alcance: *«ningún resultado autoriza abandonar L ni M para usos no muestreados — el duelo mide estimación de cantidades encuestables y nada más»* | **Conservada literal, y gobierna las cinco** |

**Lo que se traduce, y por qué:**

| Del original | A v2 | Razón |
|---|---|---|
| Cinco casillas como categorías a elegir | Cinco **lecturas publicables** de una posición de intervalo | Las categorías se solapaban; las posiciones no pueden |
| Tres ejes de comparación | **Un eje**: habilidad relativa a `B` | Es como los cuatro campos del benchmark lo resolvieron |
| (3) «Empate-TOST» | **Dos casillas**: `EQUIVALENTES` e `INDETERMINADO` | «No se vio diferencia» ≠ «son equivalentes». El original las fundía |
| `E` sin casilla | **`E` es una fila más** de la misma tabla | En los hubs de pronóstico el ensamble no tiene categoría propia: tiene su habilidad relativa al mismo baseline |
| Unidad ambigua (¿celda o piloto?) | **Celda**: estado de decidibilidad. **Piloto**: el veredicto | (5) dice *«en la mayoría»* y (4) dice *«v1»* — las cinco eran del piloto |
| Precedencia no declarada | **Secuencia fija, §4** | El benchmark: se pre-especifica y no se sigue leyendo cuando se rompe |

---

## 2 · El eje único

Ya existe en el diseño firmado y ya está implementado. `ADV1-M3`: `s = 1 − error_corredor / error_baseline`, con `B` como baseline. Implementado en `forense/prereg-duelo-v2/scoring-adv1-m3.py:74` (`def skill`).

**Cada corredor recibe su `s` contra el mismo `B`:** `s_L-solo` · `s_L+corpus` · `s_M` · `s_E`.

- `s > 0` → mejor que el baseline ingenuo
- `s = 0` → igual
- `s < 0` → peor

**La comparación entre corredores es una diferencia sobre ese mismo eje:** `Δs = s_A − s_B`, con su propio intervalo.

**El intervalo del agregado se obtiene por remuestreo sobre celdas** (pareado: las mismas celdas para todos los corredores), no de la incertidumbre del árbitro celda a celda.
⚠️ **Esto tiene una consecuencia sobre `FP-83` y hay que decirla:** el problema de los árbitros de censo —sin error muestral, `EE(R)=0`, banda de indecidibilidad indefinida— **afecta la decidibilidad por celda, no el veredicto agregado.** Con `R` determinista los errores de esa celda son exactos, y la variación que produce el intervalo del agregado es entre celdas. **`FP-83` deja de bloquear el veredicto del piloto; sigue abierta para la etiqueta por celda.** Propuesta, no decisión.

---

## 3 · Los márgenes — declarados antes, derivados después

Dos líneas sobre el eje, dibujadas **antes de ver un solo resultado**:

- **Línea del mínimo: `s = 0`.** No se negocia: es la definición del baseline.
- **Banda de indiferencia: `±Δ` sobre `Δs`.** **No se fija aquí.** `D-iv` (FIRMADA 19/ago) ordena: *«La banda TOST y el margen material NO se firman ahora: el acto de pre-registro los deriva de los EE reales del set y trae el número con su justificación»*. El acto la deriva; **mesa la firma**.

**Regla dura del benchmark, y aplica a las dos líneas:** el estimado puntual **nunca adjudica**. En no-inferioridad, la conclusión se toma por la posición del intervalo, y no puede concluirse si solo el punto cae del lado bueno. Aquí igual.

---

## 4 · La secuencia fija — esto es lo que mesa firma

Declarada al sellar y **no después**. Se detiene donde se rompe: ninguna afirmación confirmatoria por debajo del primer paso que no se supera.

```
PASO 0 (siempre, en paralelo, nunca gatea)
  Cobertura contra R: ¿qué fracción de celdas puntuadas tiene el
  valor real dentro del intervalo de cada corredor?
  → alimenta la LECTURA (5) y el resultado de calibración al 80%.
  Se publica con la misma prominencia que el marcador (ADV1-M4).

PASO 1 · ¿Algún corredor supera a B?
  Para cada corredor, IC de s contra la línea 0.
  ├─ NINGÚN IC despeja 0 por arriba ──────► LECTURA (4). LA SECUENCIA TERMINA.
  │                                          No se lee quién quedó más cerca.
  └─ Al menos uno lo despeja ─────────────► sigue al PASO 2.

PASO 2 · Entre los que superaron a B: ¿equivalentes o distintos?
  IC de Δs contra ±Δ.
  ├─ IC entero dentro de ±Δ ──────────────► LECTURA (3a) EQUIVALENTES
  ├─ IC entero fuera por el lado de L ────► LECTURA (1)
  ├─ IC entero fuera por el lado de M ────► LECTURA (2)
  └─ IC ni dentro de ±Δ ni excluye 0 ─────► LECTURA (3b) INDETERMINADO

PASO 3 · E se reporta siempre, como fila de la misma tabla.
  s_E con su IC contra la línea 0 y contra s_L y s_M.
  No abre casilla nueva y no gatea nada.
```

**Por qué el paso 1 va primero, y no es criterio nuestro.** Lo dice el texto original: la casilla (2) ya condiciona su lectura a *«skill material sobre B»*. La secuencia **implementa una precedencia que el careo ya había escrito** y que nadie había leído como tal. Y coincide con cómo `ADV1-M3` y `ADV1-M6` definen todo lo demás relativo a `B`.

**Por qué el paso 0 no gatea.** Un corredor puede superar a `B` y aun así fallar contra `R` — `B` puede estar todavía más lejos. En el hub de COVID pasó exactamente eso: la mayoría superó al baseline ingenuo y aun así los pronósticos fueron poco confiables en las fases clave. (4) y (5) son independientes y **las dos tienen que poder reportarse a la vez.**

---

## 5 · Tabla de veredictos por posición del intervalo

| # | Posición | Lectura publicable | Cláusula que la acota (verbatim del original) |
|---|---|---|---|
| **(4)** | Ningún IC de `s` despeja 0 | Ninguno utilizable v1 | *«re-tierización dirigida sin coronación»* |
| **(1)** | `IC(Δs)` entero fuera de `+Δ` | En estos momentos el canal LLM quedó más cerca del dato | *«NO licencia "el motor sobra" (procedencia, contrafactuales e interpretabilidad no se puntuaron)»* |
| **(2)** | `IC(Δs)` entero fuera de `−Δ` | El motor transportó mejor que la memoria del LLM | *«NO licencia "M es bueno" salvo skill material sobre B»* — ya garantizado por el paso 1 |
| **(3a)** | `IC(Δs)` entero dentro de `±Δ` | Equivalentes dentro de la banda pre-declarada | Hallazgo positivo, no ausencia de hallazgo |
| **(3b)** | `IC(Δs)` ni dentro ni excluyendo 0 | Indeterminado — el piloto no tuvo potencia para distinguirlos | **No se reporta como empate.** Si estaba subpotenciado, la diferencia real puede seguir siendo sustancial |
| **(5)** | Cobertura contra `R` baja en la mayoría | El fenómeno no es predecible con estas herramientas hoy | *«consecuencia propia, y es la casilla que el FFC dice esperar»* · se reporta **siempre**, junto a la que salga de los pasos 1-2 |

**Gobierna sobre las seis, verbatim del original:** *«ningún resultado autoriza abandonar L ni M para usos no muestreados — el duelo mide estimación de cantidades encuestables y nada más.»*

---

## 6 · Las tres correcciones que el benchmark marca como error, no como opción

1. **El punto nunca adjudica.** Solo la posición del intervalo. Ya está en `A-bis` del programa (*«un punto estimado que satisface un umbral con un IC que no lo despeja no adjudica»*) y el benchmark lo confirma como estándar.
2. **«Empataron» y «son equivalentes» son casillas distintas.** El original las fundía en (3). Un desenlace inconcluyente significa solo que no se vio diferencia significativa; con potencia baja la diferencia real puede ser sustancial.
3. **La secuencia se declara al sellar.** Reclamar equivalencia después de fallar en probar superioridad no se acepta salvo que se haya diseñado así desde el principio.

---

## 7 · Qué cambia aguas abajo, y qué no

**Cambia poco, y eso es señal buena.** `scoring-adv1-m3.py` **ya calcula las cinco condiciones por separado** y dejó la composición como parámetro configurable pendiente de mesa (su propio encabezado lo dice). Lo que falta es **la función de composición**: la secuencia de §4, unas decenas de líneas.

**No cambia:** el marco de candidatas · el sorteo · la tubería `L` · los corredores `B` y `E` · el contrato celda-D v0.5 · ningún test de motor.

**Desbloquea:** `D-ii` (*«firmada antes de la primera celda»*) queda satisfecha al sellar esto → **la primera celda puntuada del piloto deja de estar bloqueada.**

**Toca, y hay que declararlo:** `FP-83` (ver §2 — deja de bloquear el agregado) · `FP-91` (la casilla (4) es uno de los umbrales de `ADV1-M6`; **esta propuesta no lo adjudica**).

---

## 8 · Lo que esta propuesta NO hace

No edita el párrafo original del careo. No fija `Δ`. No adjudica `FP-91` ni `FP-79`/`FP-80`/`FP-83`. No decide qué emite el corredor `M` — eso es la sesión `EMISOR-M`. No sella nada: **mesa firma §3 y §4, o esto no rige.**

---

## 9 · Procedencia del benchmark — 20/ago/2026, cuatro campos

- **No-inferioridad y equivalencia.** Los seis desenlaces definidos por posición del IC contra el margen; la conclusión no se toma por el estimado puntual; superioridad dentro de un ensayo de no-inferioridad solo si se diseñó así desde el inicio; un desenlace inconcluyente no es equivalencia. — *Non-inferiority Trial (ScienceDirect Topics)* · *NephJC, «Understanding the vortex of non-inferiority trials»* · *Br J Cancer, «Interpreting the results of noninferiority trials»* · *FDA, «Non-Inferiority Clinical Trials to Establish Effectiveness»* · *CONSORT extension, JAMA 2006*.
- **Multiplicidad / secuencia fija.** Ordenamiento jerárquico pre-definido sin ajuste de alfa; las afirmaciones se detienen en el primer paso no superado; el orden puede fijarse por relevancia de la consecuencia. — *FDA, «Multiple Endpoints in Clinical Trials»* · *Huque & Alosh, «A flexible fixed-sequence testing method»* · *EMA, «Points to consider on multiplicity issues»*.
- **Hubs de pronóstico.** Habilidad relativa a un baseline neutral como eje común; el ensamble como fila más, no como categoría; superar al baseline y aun así fallar contra la realidad son compatibles. — *Cramer et al., PNAS 2022, «Evaluation of individual and ensemble probabilistic forecasts of COVID-19 mortality»* · *CDC CFA, COVID-19 Ensemble Forecasts* · *«Challenges of COVID-19 Case Forecasting in the US, 2020–2021»*.
- **Equivalencia + significancia combinadas.** Los cuatro desenlaces del cruce; «distinto de cero **y** equivalente» es celda legítima, no conflicto. — *Lakens, «Equivalence Tests», SPPS 2017* · *Lakens, Scheel & Isager, AMPPS 2018* · *Kruschke, «Doing Bayesian Data Analysis»*.
