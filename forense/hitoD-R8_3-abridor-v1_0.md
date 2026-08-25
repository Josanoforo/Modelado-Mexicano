# HITO D · Falsador `R8.3` — ficha-abridor: resultados y **propuesta** de veredicto

### `hitoD-R8.3-abridor` · **v1.0** · 25 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R8_3-abridor-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R8.3-abridor`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La corrida (COMMIT 2) del falsador de `R8.3` bajo la spec congelada en `hitoD-R8.3-especificacion`, y la **propuesta** de fila que de ella se sigue. |
> | **QUÉ NO ES** | **No archiva nada.** No escribe en el bloque `## Registro de veredictos archivados` de `hitoD-preregistro-v2_0.md`. **No mueve el contador de Hito D.** La adjudicación es de mesa. |
> | **VERIFICAS ASÍ** | que cada cifra de aquí sale de `forense/notas/2026-08-25-r8-3-abridor-salida.txt`, y que el árbol de decisión que las lee estaba escrito **antes** (commit `5713fe7`, que este archivo no edita). |

**Acto:** `ACTO PACK-UBUNTU-2` (abridor 1 de 2), 25/ago/2026, entorno **UBUNTU**, sobre `origin/main = 151cf04`.

---

## 1 · Qué se ejecutó

La spec congelada de `hitoD-R8.3-especificacion` §4, sin una sola desviación: estimando principal restringido al estrato **SIN PUENTE**, tres ejes de enforcement, controles por **estratificación** (nunca regresión), varianza por conglomerado último sobre `I_PSU` con `tests/svystat.py`.

Instrumento principal: **WVS Wave 7 México 2018**, 1741 filas, 454 UPM, ponderador `W_WEIGHT`. Corroboración: **ISSP 2017 `ZA6980`**, 44492 filas, 30 países.

**Dos defectos de la propia corrida, corregidos antes de que produjeran cifra y declarados aquí:** (i) las máscaras de celda con `Q288R`/`Q144` perdidos lanzaban `boolean value of NA is ambiguous` — se coercen a `False` explícitamente; (ii) el ponderador del ISSP leído como categórico traía una **etiqueta de valor** (`"No weighting/ CH: Design weight…"`) en vez de un número — se relee numérico. Ninguno de los dos alteró una cifra ya reportada: ambos abortaban la corrida.

---

## 2 · Resultado del eje que manda (eje 2 — contexto de entidad)

Contexto construido como la spec ordenó: proporción ponderada de `ENFORCEMENT ALTO` (`Q70 ∈ {A great deal, Quite a lot}`) **dentro de cada entidad**, entidades con `n ≥ 30`, corte en la mediana. Resultado del reparto: **19 entidades elegibles de 31** (12 excluidas por `n < 30`), mediana **24.3483%**, 9 entidades en contexto ALTO y 10 en BAJO. El rango real de enforcement entre entidades elegibles va de **13.6577%** (Chiapas) a **30.5270%** (Coahuila): hay variación que contrastar, no un contexto único disfrazado de dos.

**Estimando principal, estrato SIN PUENTE:**

| cantidad | valor |
|---|---|
| `p(confía en el desconocido \| SIN PUENTE, contexto ALTO)` | **4.5580%** |
| `p(confía en el desconocido \| SIN PUENTE, contexto BAJO)` | **5.0002%** |
| **`d`** | **−0.4422 pp** |
| SE | 1.4872 pp |
| **IC95%** | **[−3.3572, +2.4727]** |
| UPM · estratos · singleton | 454 · 1 · **0** |

Secundaria, universo completo (cantidad **distinta**, no comparable con la anterior — A-bis regla 4): `d = +0.3041 pp`, IC95% [−3.2972, +3.9054].

**Los mismos controles del Umbral, sobre este eje** (ingreso `Q288R` × victimización `Q144`), sin promover ninguna celda a *"el verdadero valor"* (A-bis regla 2):

| ingreso | víctima | n | `d` (pp) | IC95% | \|d\|<10 |
|---|---|---|---|---|---|
| Low | No | 292 | −0.6387 | [−5.5272, +4.2497] | sí |
| Low | Yes | 115 | +0.2031 | [−7.8572, +8.2634] | sí |
| Medium | No | 332 | +2.5947 | [−3.6460, +8.8355] | sí |
| Medium | Yes | 146 | −3.3096 | [−11.3764, +4.7573] | sí |
| High | No | 63 | **−12.9408** | [−24.2641, −1.6176] | **no** |
| High | Yes | 32 | +8.2619 | [−7.3754, +23.8991] | sí |

La única celda que excede 10 puntos lo hace **en signo negativo** —menos confianza en desconocidos donde el enforcement es más creíble—, con `n = 63`. No rescata la regla: se aparta del umbral en la dirección **contraria** a la que el mecanismo predice.

---

## 3 · Resultado del eje individual (eje 1), leído con la asimetría pre-declarada

| contraste | `d` (pp) | IC95% | \|d\|<10 |
|---|---|---|---|
| SIN PUENTE · `Q70` tribunales | +5.0961 | [+0.1544, +10.0378] | sí |
| SIN PUENTE · `Q69` policía | +7.8283 | [+2.8623, +12.7942] | sí |
| universo completo · `Q70` | +14.2489 | [+9.7122, +18.7857] | no |
| universo completo · `Q69` | +12.4199 | [+7.7891, +17.0508] | no |

La spec declaró, antes de medir, que este eje **infla `d`** por método común —desenlace y contexto son dos reactivos de confianza del mismo informante— y que por tanto sesga **en contra** de la fila `A`. Se lee como se pre-registró: los dos contrastes del estrato SIN PUENTE quedan **por debajo de 10 aun con el sesgo en contra**, lo que es evidencia conservadora **a favor** de `A`; los dos del universo completo superan 10 pero, por la misma razón pre-declarada, **no pueden por sí solos negar `A`** (no distinguen «la confianza responde al enforcement» de «la persona confiada confía en todo»).

Los seis controles sobre este eje están en la salida cruda: cinco de seis celdas con `|d| < 10`; la excepción (`High`/`No`, `d = +10.5117`) trae IC95% [−8.2256, +29.2491] con `n = 63` — indecisa, no contraria.

---

## 4 · Eje 3 (ISSP, multipaís): apunta al revés, y **no adjudica**

35037 casos útiles de 44492, 30 países. Contexto por confianza media en tribunales nacionales (`v36`, 0–10), corte en la mediana (**5.6192**):

`p(confía \| país ALTO) = 65.1202%` · `p(confía \| país BAJO) = 48.4959%` · **`d = +16.6243 pp`**, IC95% [+15.4758, +17.7727] bajo supuesto MAS.

**México, nunca disuelto en el agregado:** `p = 58.0645%`, IC95% [54.5882, 61.5409], `n = 775`; posición **contexto BAJO** (`enf = 3.5755` contra mediana 5.6192) — el segundo país más bajo de los 30, sólo por encima de Croacia.

**Por qué esto no adjudica, exactamente como se pre-declaró:** (i) `ZA6980` **no trae ni un reactivo de victimización** (0 de 356 etiquetas, con control positivo que sí devuelve `v35`/`v36`/`v9`), así que no puede satisfacer el conjunto de controles que el Umbral nombra; (ii) el contraste es **entre países**, confundido con todo lo que separa a un país de otro — es correlación ecológica, no el contraste que la ficha pide; (iii) sin UPM en el archivo, el SE va bajo MAS y **subestima el error**. Se reporta porque apunta en dirección contraria al eje 2 y ocultarlo sería elegir la evidencia.

**Advertencia de escala (A-bis regla 3).** `v35` del ISSP y `Q57`/`Q61` de WVS **no están en la misma escala y no se comparan aquí**: el reactivo del ISSP reparte 4 categorías donde *"usually be trusted"* cuenta como confianza, y en el archivo de WVS México sólo **179 de 1738** respuestas sustantivas de `Q57` eligen *"Most people can be trusted"* (conteo crudo, sin ponderar, ofrecido como conteo y no como estimación). Que dos «cifras de confianza interpersonal» del mismo país disten decenas de puntos por diferencia de reactivo y de corte es exactamente el fenómeno que `ADR-64` diagnosticó al cerrar `conf.06`; esta corrida lo vuelve a exhibir y por eso **no mezcla las dos escalas en ninguna cantidad**.

---

## 5 · Propuesta de veredicto

Aplicando el árbol congelado en `hitoD-R8.3-especificacion` §5 al eje que esa spec declaró rector:

> `|d| = 0.4422 pp < 10` **y** el IC95% [−3.3572, +2.4727] **despeja** el umbral por ambos extremos.

Eso es, literalmente, la condición **CONFIRMA** del árbol. La ficha del pre-registro dice: *"donde el riesgo de fraude baja (enforcement creíble), la confianza en desconocidos debe subir aunque no haya puente. **Si no sube, es rasgo.**"* En el contraste contextual **no sube**: se mueve −0.44 puntos, y la precisión alcanza para descartar incluso una subida de 3 puntos.

**PROPUESTA: fila `A`** — el falsador se satisface, y con él cae el `PORQUE` de la regla (`G1`: *la desconfianza es cálculo, no rasgo*). **Esta ficha no lo archiva.**

### 5.1 · Reservas, que viajan pegadas a la propuesta

1. **Piso de la tasa base.** En el estrato SIN PUENTE, `p(confía en el desconocido) = 4.6256%` (IC95% [3.2345, 6.0166]). Con una base tan baja, un umbral de «10 puntos» es **exigente de cumplir en contra** y por tanto **fácil de cumplir a favor** de `A`. La prueba **no es vacía** —el eje 1 alcanzó `p_T = 16.2927%` en una celda y produjo un `d = +10.5117`, así que diferencias de ese tamaño **sí son alcanzables** en este estrato—, pero el poder para distinguir «no responde» de «no puede subir» es limitado, y se declara.
2. **Proxy, no equivalencia.** El Umbral pide **disposición a transar**; `Q61` mide **confiar** en gente conocida por primera vez. Ningún instrumento del corpus mide transar con desconocidos. Declarado en la spec antes de medir.
3. **Asociación, no identificación** (A-bis regla 1). Ninguna cifra de aquí es coeficiente identificado; estratificar no la promueve (regla 2).
4. **Diseño.** El archivo de WVS no trae variable de estrato: la corrida usa **un solo estrato** con 454 UPM. `n_estratos_singleton = 0` en todas las corridas, leído y reportado como la propia `svystat` exige.
5. **Cobertura del eje 2.** 12 de 31 entidades quedan fuera por `n < 30`; el contraste contextual habla de las 19 elegibles, no de la República entera.
6. **Ola única.** No hay contraste temporal: WVS7 es la única ola de WVS en el corpus.
7. **El eje 3 apunta al revés** (§4) y su desacuerdo queda abierto, no resuelto por este acto.

### 5.2 · Precedencia y compuertas, ya resueltas en la spec

- **`R1.3` está archivado** (5/ago/2026, desenlace `E`) y su falsador **no se satisfizo**: el riesgo que `R8.3` debía heredar **no se materializó**, así que esta prueba se juega sola. Declarado antes de medir.
- **`conf.06` está cerrado** (`ADR-64`): la condición pre-registrada de la fila `D` caducó, la precondición de `C` quedó satisfecha, y `B` no aplica porque este acto usa fuente nueva. Si a la vez hubiera motivo para `C`, la spec ya declaró que manda `A`.

---

## 6 · Lo que este acto NO hizo

No escribió en el bloque `## Registro de veredictos archivados`. **No movió el contador de Hito D**, que sigue en las mismas líneas y las mismas fichas distintas que tenía al abrir. No adjudicó causalidad. No descargó nada. No editó la spec congelada. No colapsó «no pude abrir el payload» con «el dato no está»: los 7 payloads de este acto verificaron **COINCIDE** uno por uno.
