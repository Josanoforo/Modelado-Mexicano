# `ACTO MAESTRA38-L5` · `civico.protesta.agravio_urbano` (`R7.4`) multi-ola LAPOP — resultados

**Pieza 2 de 3 del `ACTO MAESTRA38-LOTE-LAPOP`.** Ejecuta, sin editarla, la spec sellada
`prereg-caja-S5-L5` (`sha256 74816097008b84a14a04d83dbcce850f0bb3644ae34bfe0867ab5d928ded1eb6`,
verificado al arrancar y al cerrar). Base `origin/main = a5350e59`. Entorno **UBUNTU con corpus**.
Olas: **2004, 2006, 2019** (lista cerrada de spec §1; 2021 y 2023 no traen variable de protesta).

---

## 0 · A.8 — qué midieron `L9`/`L11`, y qué es lo nuevo aquí

`ya_medido.py civico.protesta.agravio_urbano` → **`MEDIDA-EN: L11, L9, S5`**.
`L9 §4` (LAPOP 2019) y `L11 §2` (ENCUCI 2020) midieron **dos de los cuatro** antecedentes —
agravio y entorno — y su contraste `C2` (agravio dentro de urbano) está **sellado y cargado al
motor** (Enmienda `D2-d`, `civico.protesta.agravio_urbano_encuci2020`, `CARGADA-A-MOTOR`, tier
`FUERTE`). **Nada de eso se reabre aquí.** Lo nuevo de esta pieza son los antecedentes que `L9`
declaró ausentes de su instrumento —**falla estatal** (`AOJ12`) y **red previa** (`CP6`/`CP9`)— y
el intento de medir los tres antecedentes no espaciales **juntos** (`C_completo`).

## 1 · Diseño por ola — y dos hallazgos que la spec no tenía

| ola | n | estrato | conglomerado (PSU) | ponderador |
|---|---|---|---|---|
| 2004 | 1 556 | `mestrat` (4) | `msec` (127 códigos · **131** pares estrato×PSU · tamaño mediano 12) | **ninguno** |
| 2006 | 1 560 | `ESTRATOPRI` (4) | `UPM` (130 × 12) | **ninguno** |
| 2019 | 1 580 | `estratopri` (4) | `upm` (**129**) | `wt` **constante = 1** |

**Hallazgo 1 — `wt` de 2004 no es «un ponderador sin etiqueta»: está vacía.** Spec §2 la daba por
existente («`wt` existe (ambos formatos), sin etiqueta en el inventario»). Contra el `.dta`:
**0 válidos de 1 556 filas**, todas `NaN`. La ola 2004 **no se puede ponderar**. Sale **sin
ponderar**, declarado — el criterio que §2 y `S2-L2 §1.0` ya fijaban para 2006, que aquí aplica
también a 2004. Un inventario que lista la columna no prueba que la columna tenga datos.

**Hallazgo 2 — 2004 no trae `upm`/`estratopri`/`cluster`.** Spec §2 decía «`mestrat` (estrato) sin
UPM/clúster visible». El conglomerado sí existe, con otro nombre: **`msec` («Sección electoral»)**,
127 códigos, 131 pares `(mestrat, msec)`, tamaño mediano **12** — exactamente la estructura del
`UPM` de 2006 (130 × 12). Se usa `(mestrat, msec)` como llave de conglomerado. Sin esto el IC de
2004 habría salido de un remuestreo de personas, que estrecha el IC de mentira.

**Hallazgo 3 — `ur`/`UR` no es «`tamano`=5».** En 2019, `ur`=rural incluye `tamano` 1,2,3,4
(12/74/121/98) y sólo 12 de los 35 de `tamano`=5; en 2006 `UR`=rural=324 contra `TAMANO`=5=384.
Son dos dicotomizaciones distintas. La spec pide `tamano` (§3) y así se midió; `ur` se reporta en
paralelo como verificación cruzada, **sin sustituirla**. En 2004 `ur` también está **vacía** (0
válidos): su análogo es `mzona` («Tipo de localidad»), que se reporta en paralelo y se declara.

## 2 · Dicotomizaciones — los cortes que la spec dejó «pendientes de codebook», resueltos

Resueltos por el censo A.4 de este acto contra el mapa de códigos del propio `.dta`/`.sav`
(`data/l4-l5-l18-censo-v1_0.json`), no inventados:

| indicador | corte | fuente del corte |
|---|---|---|
| `AGRAVIO` | `vic1`/`VIC1`=1; 2019 `vic1ext`=1 **o** `vicbar4a`=1 | códigos 1 Sí / 2 No |
| `FALLA_ESTATAL` = BAJA | `aoj12` ∈ {3 Poco, 4 Nada} | escala 1 Mucho … 4 Nada |
| `RED_PREVIA` | `cp6` **o** `cp9` ∈ {1,2,3} | escala 1 semanal … 4 Nunca |
| `URBANO` | `tamano` ∈ {1,2,3,4} | 1 capital … 5 área rural |
| protesta | 2004/2006 `prot1`/`PROT1`=1; 2019 `prot3`=1 | 1 algunas veces / 2 casi nunca / 3 nunca |

`LAPOP-E8` (variable `e8` en 2004, la misma en mayúsculas en 2006) queda **fuera** del indicador de
red previa, per spec §0.4: es aprobación
normativa de que **otros** participen (escala 1–10), no asistencia propia. Se reporta como eje
secundario y no entra a ninguna celda del falsador.

**Marginales por ola (2004 / 2006 / 2019).** `AGRAVIO`=1: 268 / 312 / 622 · `FALLA BAJA`:
1 023 / 977 / 1 141 · `RED_PREVIA`=1: 856 / 1 078 / 761 · `URBANO`=0 (rural): **382 / 384 / 35** ·
protesta=1: 120 / 132 / 112. Los de 2004 y 2006 son **hallazgo nuevo** (ningún acto anterior los
verificó), no guardia heredada; el de 2019 reproduce la guardia de `L9 §0.5` (`prot3` válidos
1 576, «sí» 112): **OK**.

## 3 · Resultados

Guardia de celda pre-registrada: numerador `< 10` ⇒ `NO-ESTIMABLE`.

| ola | contraste | urbano (num/n) | rural (num/n) | `d` | IC95 | |
|---|---|---|---|---|---|---|
| 2004 | `C_completo` | 17/108 | **3**/14 | — | — | **`NO-ESTIMABLE`** (num 3) |
| 2004 | `C_agravio` | 27/225 | **5**/32 | — | — | **`NO-ESTIMABLE`** (num 5) |
| 2004 | `C_falla` | 66/769 | 14/222 | +2.276 pp | `[−3.573, +7.216]` | contiene 0 |
| 2004 | `C_red` | 64/631 | 18/196 | +0.959 pp | `[−7.385, +7.599]` | contiene 0 |
| 2006 | `C_completo` | 21/130 | **3**/21 | — | — | **`NO-ESTIMABLE`** (num 3) |
| 2006 | `C_agravio` | 32/261 | **4**/46 | — | — | **`NO-ESTIMABLE`** (num 4) |
| 2006 | `C_falla` | 80/756 | 12/180 | +3.915 pp | `[−1.172, +8.819]` | contiene 0 |
| 2006 | `C_red` | 75/771 | 23/267 | +1.113 pp | `[−3.757, +5.429]` | contiene 0 |
| 2019 | `C_completo` | 20/212 | **1**/1 | — | — | **`NO-ESTIMABLE`** (num 1) |
| 2019 | `C_agravio` | 63/609 | **2**/12 | — | — | **`NO-ESTIMABLE`** (num 2) |
| 2019 | `C_falla` | 68/1 115 | **2**/23 | — | — | **`NO-ESTIMABLE`** (num 2) |
| 2019 | `C_red` | 65/747 | **2**/11 | — | — | **`NO-ESTIMABLE`** (num 2) |

En 2019 **toda** la columna rural colapsa: la ola tiene **35** personas en `tamano`=5, y el
subgrupo de alto riesgo se reduce a **1**. La spec anticipó exactamente esto («es razonable
esperar que la rama rural del subgrupo caiga bajo la guardia de numerador»), y cayó.

## 4 · Veredicto `B-bis`

> ## **`NO-DISCRIMINA`**, y con una declaración que la spec exige por escrito:
> ### **el corazón de la regla no se midió.**

`C_completo` es **`NO-ESTIMABLE` en las tres olas**. Por spec §4, el veredicto sale entonces de las
diagnósticas tomadas juntas — y de las doce celdas diagnósticas, **cuatro** son estimables
(`C_falla` y `C_red` en 2004 y 2006). Las cuatro van en **signo positivo** (+2.28, +0.96, +3.92,
+1.11 pp) y **las cuatro contienen 0**. Ninguna refuta, ninguna corrobora.

**Lo que esto NO autoriza, por precedencia de spec §4:** «si las tres van limpias y en el mismo
signo positivo, se reporta como corroboración **del patrón por partes**, nunca como corroboración
de `C_completo` — no se sustituye lo compuesto por la suma de lo simple». Aquí ni siquiera van
limpias: los cuatro IC cruzan el cero. **Que los cuatro puntos sean positivos no es evidencia a
favor de la regla.** Es ruido con un signo.

**Y lo que sigue sin medirse, declarado:** que los tres antecedentes **juntos** — agravio, falla
estatal palpable y red previa — sean los que el entorno urbano canaliza hacia la protesta. Es el
`SI` completo de la regla, y ninguna de las tres olas tiene suficientes rurales de alto riesgo
para estimarlo. `R7.4` sigue **acotada**, exactamente como `L9` la dejó; esta pieza no la cierra
ni la mueve, y añade que el hueco **no es de instrumento sino de tamaño de celda**: los reactivos
sí existen (ése era el hallazgo de spec §0.3, y se confirma), lo que no existe es la `n`.

### 4.1 · Fila `B-bis`: qué significa que el falsador no refute

No refutar aquí **no es evidencia a favor**. Con `C_completo` no estimable y las cuatro
diagnósticas cruzando el cero, el resultado es compatible con que la regla sea cierta, con que sea
falsa, y con que el entorno urbano no tenga nada que ver. Lo único que este acto establece con
firmeza es **por qué** no se pudo medir: el subgrupo rural que cumple los tres antecedentes tiene
14, 21 y 1 personas en las tres olas. Un acto sucesor que quiera cerrar `R7.4` necesita una fuente
con sobremuestra rural, no otra ola de LAPOP.

## 5 · `C_agravio` — una tensión interna de la spec sellada, declarada y no resuelta a mano

Spec §3.1 define las diagnósticas como «una por antecedente, **2×2 cada una, contra `URBANO`**», y
llama a la primera `C_agravio = agravio × entorno`, «repite el diseño ya corrido de `L9`/`L11`». Pero
spec §0.3 dice que esta pieza «no repite `C2` (agravio-en-urbano, ya `CORROBORADA` dos veces) **ni
vuelve a intentar `C1`** con el mismo diseño de dos factores que ya cayó por guardia».

Las dos frases no pueden cumplirse a la vez: `C_agravio` **contra `URBANO`** *es* la forma de `C1`.
Se ejecutó §3.1 —la sección que pre-registra las celdas— con la forma que §3.1 fija (restringir a
`AGRAVIO=1`, contrastar por entorno), y el resultado es `NO-ESTIMABLE` en las tres olas, **igual
que el `C1` de `L9`**, por la misma razón y con numeradores del mismo orden (5, 4, 2 contra el 7 de
`L9`). No se computó la forma `C2` (agravio dentro de urbano), porque §0.3 la excluye
explícitamente y añadir una celda que la spec no pre-registró es tan defecto como omitir una que sí.

**Consecuencia declarada:** la «replicación de tercera ola» que §3.1 anuncia para `C_agravio`
**no ocurrió** — no porque se omitiera, sino porque la única forma de `C_agravio` que la spec
pre-registra cae por guardia en las tres olas. Queda como fila de firmas (`FP-314`) para que mesa
decida si una versión futura de la spec debe fijar la forma `C2`.

> **Esto lo atrapó la verificación adversarial de este mismo acto, y corrigió el artefacto, no sólo
> la prosa.** La primera versión de `data/l5-protesta-multiola-v1_0.json` afirmaba en
> `notas_spec.C_agravio_es_replicacion` que `C_agravio` «repite el diseño ya corrido y sellado por
> `L9 §4` (+5.60 pp) y `L11 §2` (+3.72 pp)». Es falso: esas dos cifras son el `C2` de `L9`, y lo que
> este medidor calcula es el `C1`. El JSON que mesa consume decía «esto es lo mismo que ya se
> corroboró» sobre un cruce que en realidad reprodujo el diseño que **ya había fallado**. El campo
> se reescribió como `C_agravio_NO_es_la_replicacion_que_la_spec_anuncia` y el medidor se re-corrió.
> Ninguna cifra ni ningún veredicto cambió — `C_agravio` es `NO-ESTIMABLE` en las dos lecturas.
> Detalle en `forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-verificacion.md`.

## 6 · `PROT2` de 2006 — pieza separada, y con una reserva que la spec no anticipó

Spec §1.2 trata `PROT1` y `PROT2` como «dos piezas separadas, no se promedian ni se combinan» por
tener ventana temporal distinta. El censo A.4 añade algo más grave: **`PROT2` está gateada por
`PROT1 ∈ {1,2}`** — 217 elegibles, 209 válidos. No es sólo otra ventana: su universo está
**anidado en el desenlace**. Sobre ese subuniverso la pregunta ya no es «quién protesta» sino
«quién, de los que alguna vez protestaron, lo hizo el último año». **Un eje anidado en el desenlace
no refuta ni corrobora la regla general**, así que `PROT2` se reporta como descriptivo con esa
reserva escrita y **no entra a ningún veredicto**. (`L9` ya había registrado el gateo de `PROT2` en
su censo A.4; esta pieza lo confirma y saca la consecuencia.)

## 7 · `se_mueve_si` — verbatim de spec §5

> Si entre quienes cumplen los tres antecedentes no-espaciales (víctimas, con confianza baja en la
> justicia, con membresía en organización) la tasa de protesta en entorno urbano **no es mayor** que
> en entorno rural, la regla se rompe — verbatim de `N5 §2.8`, ahora con la celda formalizada en §3.1
> y su guardia anticipada en §3.1/§4. Si `C_completo` cae por guardia (`NO-ESTIMABLE`),
> `se_mueve_si` se lee sobre las tres diagnósticas juntas, per §4.

**Cayó por guardia en las tres olas.** Leído sobre las diagnósticas: no se cumple la condición de
ruptura (los puntos van al signo que la regla predice) **ni** la de sostén (ningún IC excluye 0).

## 8 · Reservas y qué NO hace

Asociación transversal, sin identificación causal. 2004 y 2006 van **sin ponderar** — el IC no
incorpora efecto de diseño más allá del conglomerado documentado. Los cortes de `FALLA_ESTATAL`,
`RED_PREVIA` y `URBANO` salen del mapa de códigos del propio archivo, no de un codebook: no hay
codebook de 2004/2006 en el manifiesto (sólo «technical information»), y así se declara.

No mueve el tier de `civico.protesta.agravio_urbano` (`[MEDIA-FUERTE]`) ni el de
`_encuci2020` (`FUERTE`, `CARGADA-A-MOTOR`) ni el de `_lapop2019` (`SELLADA-SIN-CARGA`). No reabre
`D2-d` ni la fila `D` de `R7.4` (`ADR-158`), que corrió sobre datos de **evento**, no de persona.
No dice nada sobre `civico.autodefensa.agravio_rural`. No reabre `FP-298` (`EJECUTADA`).
No toca `milpa/tramite.yaml`, manifiesto, cola, relaciones, staging ni ninguna spec.
