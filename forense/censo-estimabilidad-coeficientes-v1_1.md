# Censo de estimabilidad de los 15 coeficientes de generador
### `censo-estimabilidad-coeficientes` · **v1.1** · 13 de agosto de 2026 · ENCARGO CENSO-v1.1, acto de escritorio (caja, sin microdato ni red)

> | | |
> |---|---|
> | **ARCHIVO** | `censo-estimabilidad-coeficientes-v1_1.md` |
> | **QUÉ ES** | Supera a `censo-estimabilidad-coeficientes-v1_0.md` (4/ago/2026) sin borrarlo — protocolo de renombre por versión (`forense/encargos/convencion.md`). Para cada uno de los 15 coeficientes de generador (`milpa/procedencia.yaml:612-639`): su clase citada, un desenlace co-observado candidato si existe, el criterio de tres preguntas separadas ((A) reactivo, (B) co-observación, (C) llave de identificación ADR-57(c)) aplicado a las 9 filas que v1.0 dejó `SIN-RUTA`, y una clasificación de ruta + prioridad recalculada. Derivado contra `origin/main = dcc4f6a` (13/ago/2026) — ver §8. |
> | **QUÉ NO ES** | No abre ningún microdato, no corre ninguna estimación, no cambia ningún valor `ASIGNADO`, no mueve el contador `0 de 2` de `registro-llaves-identificacion-v1_0.md`, no adjudica ningún veredicto de Hito D, no sella ninguna llave nueva de ADR-57(c). Es censo de estado, no medición ni adjudicación — §9. |
> | **VERIFICAS ASÍ** | §7 trae el comando que deriva el reparto de rutas contra este mismo archivo. El razonamiento completo detrás de cada celda (fuentes, hashes, comandos crudos) vive en `forense/notas/2026-08-13-censo-v1_1-abrir4-enasem.md` — este archivo es la tabla consolidada (estación 2 del conducto, §1 de esa nota); no repite el detalle de derivación, lo cita. |
> | **SELLADA POR** | `ADR-89` (`canon/gobernanza-v1_15.md`, 17/ago/2026, ACTO RUTA-SELLO) — las cuatro definiciones de §1 y el reparto de §7 son canon desde este ADR, estampado (A.10) como snapshot a este archivo al SHA `dcc4f6a`, `VENCIBLE EN ALCANCE al cierre de BARRIDO-2`. Ver también la enmienda in situ sobre §1, línea 45. |

---

## 0 · Qué cambia frente al v1.0 — el defecto de conducto primero, el reparto después

**Titular, antes de cualquier otra cifra: 3 de las 15 filas del censo v1.0 estaban contradichas por evidencia que ya vivía en el repo, sin cruzar, desde el 7-8 de agosto** — `data/abrir4-variables-2026-08-08.tsv` (PR #159, 8/ago) y `data/curacion-registro/relaciones.tsv` (commit `16180e6`, 7/ago). El censo v1.0 (4/ago) escribió "Ninguna llave aplica" sobre las filas 12, 13 y 14; las tres tenían ya, cuatro días después, un reactivo con texto verificado y co-observación dentro del mismo instrumento. Nada las cruzó porque nada lee `abrir4`/`verif3` (`grep -rl "abrir4\|verif3" tools/ tests/` → 0 lectores, verificado en este acto) y nada citaba `censo-estimabilidad` desde `tests/`/`tools/` (0 resultados). El defecto no es que el hallazgo no existiera — es que subió a una tabla consolidada (`relaciones.tsv`) y a un TSV de mapeo (`abrir4`), y ninguna de las dos rutas de conducto llega a la tabla consolidada del censo. Detalle completo, con las dos fuentes cruzadas de forma independiente y sin contradicción entre ellas, en la nota (§6).

**Fila por fila, qué cambia y qué no:**

| fila | v1.0 | v1.1 | qué cambió |
|---|---|---|---|
| 1 · G1 confianza_institucional | RUTA-A | RUTA-A | sin cambio — fuera del alcance de `abrir4`/ENASEM de este acto |
| 2 · G1 radio_confianza | RUTA-A | RUTA-A | sin cambio |
| 3 · G2 sens_estatus | SIN-RUTA | SIN-RUTA | **sin cambio, ahora con universo declarado** — `abrir4` (4 instrumentos) + ENASEM (este acto, 3 rondas): cero candidatos nuevos |
| 4 · G2 aversion_riesgo | SIN-RUTA | SIN-RUTA | **sin cambio, ahora con universo declarado** — mismo resultado |
| 5 · G3 horizonte_temporal | RUTA-I | RUTA-I | sin cambio — única llave sellada, `CAL-G3`, no tocada por este acto |
| 6 · G3 aversion_riesgo | SIN-RUTA | SIN-RUTA | **sin cambio, ahora con universo declarado** — mismo parámetro que fila 4 |
| 7 · G3 familismo_apoyo | RUTA-A | RUTA-A | sin cambio |
| 8 · G4 exposicion_violencia | RUTA-C | RUTA-C | sin cambio — fuera del alcance de este acto |
| 9 · G4 confianza_institucional[justicia] | RUTA-C | RUTA-C | sin cambio |
| 10 · G4 horizonte_temporal | SIN-RUTA | SIN-RUTA | **sin cambio, universo enriquecido** — `abrir4` aporta un reactivo limpio (ENBIARE `PA6`/`PA3_08`) que no resuelve la fila porque falta el desenlace de G4, no el reactivo |
| 11 · G4 sens_estatus | SIN-RUTA | SIN-RUTA | **sin cambio, ahora con universo declarado** — mismo parámetro que fila 3 |
| 12 · G5 familismo_apoyo | SIN-RUTA | **`RUTA-C`** | **RECLASIFICA** — `ABRIR-4`: ENBIARE `PB2_1` (reactivo, no circular) + Apartado F (co-observación); sin llave ADR-57(c); ENASEM aporta una precondición de panel (3 olas, `G17`) declarada como candidata de diseño futuro, no ejercida |
| 13 · G5 familismo_obligacion | SIN-RUTA | **`RUTA-C`** | **RECLASIFICA** — `ABRIR-4`: ENASIC `P7_12_7` (reactivo, primero de los 15 en esta fila); sigue sin magnitud asignada (ADR-30) |
| 14 · G5 radio_confianza (puente) | SIN-RUTA | **`RUTA-C`** | **RECLASIFICA** — `ABRIR-4`: ENBIARE `PB1_01/02` + `PF1_1..6` (co-observación estructural); ENASEM descartado como fuente de reactivo (0/6,471 variables mencionan confianza) |
| 15 · G6 deferencia | SIN-RUTA | SIN-RUTA | **sin cambio, ahora con universo declarado** — ENASEM (este acto) confirma ausencia total del constructo; ENOE ya descartado antes del 4/ago (`forense/notas/2026-08-01-p2-momentos-atributos.md:233`) |

**Ninguna fila alcanza `RUTA-I`.** Las tres reclasificaciones van a `RUTA-C` — reactivo y co-observación existen, la corrida no se ha ejecutado, y ninguna llave de ADR-57(c) cubre la relación concreta (regla de precedencia: co-observación sin llave no es identificación). El contador `llaves de identificación ejercidas: 0 de 2` (`registro-llaves-identificacion-v1_0.md`) **no se mueve** — no hay propuesta de movimiento, per §10 de la nota.

**Contador de universo declarado: 9 de 9 filas `SIN-RUTA`** salen de este acto con su universo en la celda (objetivo del encargo, cumplido — v1.0 solo cumplía 1 de 9, contando la fila 3 que sí acotaba "Ninguna llave cubre consumo por tarjeta").

---

## 1 · Las cuatro rutas — sin cambio de definición

Misma taxonomía que v1.0 §1 (RUTA-A/RUTA-I/RUTA-C/SIN-RUTA), no re-declarada aquí — sigue sin ser canon, sigue sin regir nada hasta que una mesa la selle con ADR. Este acto no la edita, solo la aplica con más disciplina en la columna de universo declarado. Regla nueva de este acto, verificada contra la propia definición de `RUTA-C` de v1.0 (no una clase nueva inventada — ver §9 de la nota para la verificación completa): **"co-observación disponible, corrida no ejecutada" es exactamente lo que `RUTA-C` ya define** ("existe un reactivo... y un desenlace candidato, co-observables en principio dentro del mismo instrumento — pero la corrida no se ha ejecutado"). Las filas 8 y 9 de v1.0 ya eran precedente de esta misma clase antes de este acto.

*(Enmienda in situ, 17/ago/2026, ACTO RUTA-SELLO, `ADR-89` — el párrafo de arriba no se toca, es historia correcta al 13/ago/2026.)* **La mesa selló esta taxonomía con `ADR-79(f)`/`ADR-89`: las cuatro definiciones (citadas verbatim de v1.0 §1 en `ADR-89`) y el reparto de §7 son canon desde hoy.** El reparto queda estampado (A.10) como snapshot de este archivo al SHA `dcc4f6a`, rotulado `VENCIBLE EN ALCANCE al cierre de BARRIDO-2` — no es estado del programa, no es denominador ni cuota para el barrido, no rige territorio nuevo. Ninguna fila individual de §5 se reabre ni se mueve por este sello.

---

## 2 · Los tres criterios (A)(B)(C) — la separación que este acto añade al método

Heredado de la addenda de este encargo, verbatim en cuanto a la regla de precedencia (sellada aquí, no reinterpretada):

- **(A) ¿Hay reactivo?** — vocabulario A.4 cerrado: `EXISTE-SATISFACE` / `EXISTE-NO-SATISFACE` (y qué falta) / `NO-ENCONTRADO` (dónde, con qué términos) / `NO-ACCESIBLE`. "No existe"/"inexistente"/"no hay fuente" quedan prohibidas como clasificación.
- **(B) ¿Reactivo y desenlace co-observados, mismo instrumento y muestra?** — habilita **asociación**. Se cita tabla, folio y N.
- **(C) ¿Llave de identificación de ADR-57(c) que cubra esta relación concreta?** — habilita **identificación**. Exige (i) panel con el desenlace en el instrumento, (ii) experimento natural con grupo de comparación, o (iii) diseño experimental de terceros. Se cita `archivo:línea`.

**Regla de precedencia: (B) sin (C) no es `RUTA-I`.** Es asociación disponible — `RUTA-C` si la corrida no se ha ejecutado, `RUTA-A` si ya corrió. Aplicada a las 9 filas `SIN-RUTA` de v1.0 en §5 (detalle completo por fila en `forense/notas/2026-08-13-censo-v1_1-abrir4-enasem.md` §5).

---

## 3 · Cruce obligatorio — sin cambio de descartes registrados

Ninguna fila de este censo reutiliza un descarte de `descartes-forenses-registro.md` ni re-propone la ruta ENOE→`G3.horizonte_temporal` (ADR-49 D1) — mismo criterio que v1.0 §3, no re-verificado aquí (fuera de perímetro: este acto no re-audita descartes fuera de las 9 filas `SIN-RUTA`, que sí se cruzaron en §5).

---

## 4 · Marca (b) — sin cambio

Misma marca que v1.0 §4: `G3·familismo_apoyo`, `G5·familismo_apoyo`, `G5·familismo_obligacion` (`procedencia.yaml:633-635`). Las dos filas reclasificadas de G5 con marca (b) (12 y 13) la conservan — nada en el nuevo reactivo/co-observación de `ABRIR-4` la retira o la sostiene: `ABRIR-4` no midió población en México con las escalas validadas mexicano-americanas citadas por la marca, solo encontró un reactivo distinto (ENBIARE/ENASIC) para el mismo coeficiente.

---

## 5 · Las 15 filas

| # | Gen | θ (coeficiente) | Clase citada | Desenlace co-observado candidato | (b) | Palanca ADR-57(c) — estado citado (`gobernanza:623`) | Ruta | Prioridad |
|---|---|---|---|---|---|---|---|---|
| 1 | G1 | `confianza_institucional` −0.60 | `ASIGNADO` (`procedencia.yaml:625`); β̂ marginal `MEDIDO·β̂` (Encargo W) | `tramite.mordida.discrecional` — ENCIG 2023 (sin cambio, v1.0 §5 fila 1) | No | Ninguna llave cubre trámite/mordida (ENNViH, ENASEM y ENOE-laboral no aplican) — techo ya alcanzado: asociación, ADR-57(a) | **RUTA-A** | BAJA — sin cambio |
| 2 | G1 | `radio_confianza` −0.35 | `ASIGNADO`; β̂ marginal `MEDIDO·β̂` (Encargo W) | `tramite.mordida.discrecional` — ENCUCI 2020 (sin cambio) | No | Ninguna llave aplica — asociación (ADR-57(a)) | **RUTA-A** | BAJA — sin cambio |
| 3 | G2 | `sens_estatus` 0.55 | `ASIGNADO` | Desenlace identificado en ENIGH pero circular como reactivo (sin cambio, v1.0 §5 fila 3); búsqueda de reactivo cerrada (ADR-54) sobre el régimen de 5 instrumentos, **más `ABRIR-4` (ENSAFI/ENFIH/ENASIC/ENBIARE, 8/ago) y ENASEM 2018/2021/2024 (este acto, 13/ago), cero candidatos nuevos** | No | Ninguna de las tres llaves de ADR-57(c) cubre comparación de estatus por consumo/apariencia: ENNViH/MxFLS no porque su llave viva (`CAL-G3`) es sobre horizonte temporal · ENASEM no porque, verificado en este acto, no trae ítem de comparación de estatus/apariencia frente a vecinos (0/6,471 variables) · ENOE no porque es elegible solo para desenlaces laborales, y `sens_estatus` no lo es. Universo: `gobernanza:623` + ADR-54 + 6 payloads ENASEM del manifiesto + 28 celdas de `abrir4-variables-2026-08-08.tsv`, 2026-08-13 | **SIN-RUTA** | BAJA — búsqueda de reactivo cerrada formalmente, universo declarado |
| 4 | G2 | `aversion_riesgo` 0.20 | `ASIGNADO` | Búsqueda cerrada (ADR-52 A, ENIF `P5_23`/`P5_24`) **más `ABRIR-4` (ENSAFI `CONF_FINAN`/`IMPULSIVID`/`GRA_CONTROL` sin texto verificable, ENFIH tenencia de seguro sin actitud) y ENASEM (este acto, `riesgo`/`arriesg` = 0/6,471)** | No | Ninguna de las tres llaves cubre aversión al riesgo: ENNViH no trae esta batería · ENASEM no porque no tiene el reactivo (verificado) · ENOE no porque es solo laboral. Universo: `gobernanza:623` + ADR-52 A + 6 payloads ENASEM + 28 celdas `abrir4`, 2026-08-13 | **SIN-RUTA** | BAJA — búsqueda de reactivo cerrada formalmente, universo declarado |
| 5 | G3 | `horizonte_temporal` −0.60 | `ASIGNADO` | `CAL-G3`, panel ENNViH/MxFLS (sin cambio, v1.0 §5 fila 5) | No | **SÍ — llave (i)**: ENNViH/MxFLS, ruta viva vía `CAL-G3` (`gobernanza:623`, verbatim) | **RUTA-I** | **ALTA — sin cambio**, única llave sellada del censo |
| 6 | G3 | `aversion_riesgo` 0.40 | `ASIGNADO` | Mismo parámetro que fila 4 — misma búsqueda cerrada, mismo universo enriquecido por `abrir4`/ENASEM (este acto) | No | Ninguna llave aplica — mismo universo que fila 4 | **SIN-RUTA** | BAJA — misma búsqueda cerrada que la fila 4, universo declarado |
| 7 | G3 | `familismo_apoyo` 0.20 | `ASIGNADO`; β̂ marginal `MEDIDO·β̂` (Encargo W) | `dinero.ahorro.volatilidad_horizonte_corto` — ENIF 2024 (sin cambio) | **Sí** | Ninguna llave aplica — asociación (ADR-57(a)) | **RUTA-A** | BAJA — sin cambio |
| 8 | G4 | `exposicion_violencia` 0.70 | `ASIGNADO`; θ `MEDIDO·PARCIAL` | `comunicacion.inseguridad.ver_oir_callar` vía `BP1_23`, ENVIPE 2025 — limitación estructural declarada (sin cambio, v1.0 §5 fila 8) | No | Ninguna llave cubre esta relación — techo: asociación | **RUTA-C** *(con limitación estructural declarada)* | MEDIA — sin cambio, requiere adjudicación de mesa sobre `BP1_23` |
| 9 | G4 | `confianza_institucional[justicia]` −0.40 | `ASIGNADO`; θ `MEDIDO·PARCIAL` | Mismo candidato `BP1_23`, mismo instrumento (sin cambio) | No | Ninguna llave aplica — asociación | **RUTA-C** *(misma limitación estructural que fila 8)* | MEDIA — sin cambio |
| 10 | G4 | `horizonte_temporal` −0.20 | `ASIGNADO` | ENIF `P4_10` falla C3 frente al desenlace de G3 (sin cambio de fondo); **`ABRIR-4` aporta un reactivo limpio de horizonte/expectativa (ENBIARE `PA6`/`PA3_08`) que no resuelve la fila porque ENBIARE no trae ningún desenlace de G4 (victimización/justicia) co-observable**; ENASEM (este acto) igual — sin desenlace de G4 | No | Ninguna llave cubre esta relación concreta: ENNViH/MxFLS cubre horizonte temporal solo para G3 (`CAL-G3`) · ENASEM no tiene desenlace de G4 · ENOE es solo laboral. Universo: `gobernanza:623` + `abrir4` + este acto, 2026-08-13 | **SIN-RUTA** | BAJA — sin candidato hoy que resuelva la co-observación faltante, universo enriquecido |
| 11 | G4 | `sens_estatus` −0.15 | `ASIGNADO` | Mismo parámetro que fila 3 — mismo universo enriquecido | No | Ninguna llave aplica — mismo universo que fila 3 | **SIN-RUTA** | BAJA — misma búsqueda cerrada que la fila 3, universo declarado |
| 12 | G5 | `familismo_apoyo` 0.50 | `ASIGNADO` | **`ABRIR-4` (8/ago): ENBIARE 2021 `PB2_1` — "¿considera usted que siempre contará con la ayuda de personas de su familia?" (Sí/No/No tiene familia), no circular (a diferencia de ENIF `p9_9_4`, marca C3). Co-observado con Apartado F (`PF1_1..6`, dificultades económicas), misma tabla `TENBIARE`, n=31,166. Reserva declarada: `PF1_*` no es el desenlace formalmente nombrado de G5 (`familia.seguro.volatilidad_ausencia_estado`, que vive en ENIF) — equivalencia de constructo no verificada, decisión de mesa** | **Sí** | Ninguna llave: ENBIARE no es panel (inferencia estructural, ningún diccionario lo declara), no hay grupo de comparación, no es diseño de terceros. **ENASEM (este acto, 13/ago) sí ofrece una precondición de panel real** — `G17` ("¿recibió ayuda de hijos/nietos?"), redacción casi idéntica en las tres olas (2018/2021/2024), identificador de persona `UNHHIDNP` persistente — **candidata a diseño futuro, NO llave ejercida** (falta diseño intra-persona, mismo tipo de brecha que `CAL-G3` ya tuvo). Universo: `gobernanza:623` + 6 payloads ENASEM + 28 celdas `abrir4`, 2026-08-13 | **`RUTA-C`** *(desenlace candidato no formalmente nombrado en el motor — reclasificada desde la clase sin ruta de v1.0, evidencia `ABRIR-4` 8/ago)* | MEDIA — requiere que mesa adjudique la equivalencia de constructo (`PF1_*` vs. `familia.seguro.volatilidad_ausencia_estado`) antes de correr nada; la corrida en sí es barata (mismo instrumento, mismo folio) |
| 13 | G5 | `familismo_obligacion` (signo negativo o no monotónico — sin magnitud, único de los 15) | `ASIGNADO` sin magnitud (ADR-30) | **`ABRIR-4` (8/ago): ENASIC 2022 `P7_12_7` — "Se debe enseñar a la mujer (al hombre) que su deber es cuidar a los padres, cónyuge, hijas e hijos" (acuerdo/desacuerdo), tabla `TPER_ELE`, n=5,579. Co-observado con la batería `P6.x` de conducta de cuidado real, mismo instrumento. Reserva declarada: desenlace de "conducta de cuidado" es cognado, no idéntico, al desenlace formal de G5** | **Sí** | Ninguna llave: ENASIC es corte único, sin panel. **ENASEM (este acto) no aporta ningún candidato**: único hit de "obligación" es un ítem de personalidad general (Big-Five, "cumplo mis obligaciones"), construcción distinta de deber familiar — verificado y descartado explícitamente. Universo: `gobernanza:623` + 6 payloads ENASEM + 28 celdas `abrir4`, 2026-08-13 | **`RUTA-C`** *(desenlace candidato no formalmente nombrado; reclasificada desde la clase sin ruta de v1.0, evidencia `ABRIR-4` 8/ago)* | MEDIA — mismo bloqueo de adjudicación de constructo que la fila 12; **y, aun adjudicado, sigue sin magnitud que calibrar (ADR-30)** — tener reactivo no resuelve esa condición |
| 14 | G5 | `radio_confianza` 0.15 | `ASIGNADO` | **`ABRIR-4` (8/ago): ENBIARE 2021 `PB1_01`/`PB1_02` (confianza generalizada/conocida, 0-10) co-observado con `PF1_1..6` (dificultades financieras), misma tabla `TENBIARE`, mismo folio/hogar/persona, n=31,166 — resuelve estructuralmente el problema de "sin muestra común" que bloquea el par ENCUCI/ENIF activo hoy. Reserva declarada, no verificada: si `PB1_01/02` miden el mismo constructo que `radio_confianza` operacionalizado con ENCUCI `AP5_1_1/2/3`** | No | Ninguna llave: ENBIARE no es panel. **ENASEM (este acto) descartado como fuente de reactivo, definitivamente: 0 de 6,471 variables en las tres rondas mencionan "confianza"/"confía"** — la llave de panel de ENASEM no puede cubrir esta relación porque el reactivo mismo no existe en el instrumento. Universo: `gobernanza:623` + 6 payloads ENASEM + 28 celdas `abrir4`, 2026-08-13 | **`RUTA-C`** *(desenlace candidato no formalmente nombrado, equivalencia con ENCUCI no verificada; reclasificada desde la clase sin ruta de v1.0, evidencia `ABRIR-4` 8/ago)* | MEDIA — requiere adjudicación de mesa sobre equivalencia de constructo frente a ENCUCI antes de correr nada |
| 15 | G6 | `deferencia` 0.45 | `ASIGNADO` | Único proxy Latinobarómetro `P4NOIJ`, sin desenlace propio documentado (sin cambio, v1.0 §5 fila 15); `abrir4` no examina Latinobarómetro (fuera de sus 4 instrumentos); **ENASEM (este acto) confirma ausencia total del constructo — 0/6,471 variables para `obedien`/`jerarqu`/`iniciativ`/`autoridad`/`deferenc`/`retroalimentacion`** | No | Ninguna llave: ENNViH no cubre jerarquía · ENASEM no tiene el constructo (verificado) · ENOE ya descartado antes del 4/ago para `trabajo.jerarquia.deferencia_iniciativa_suprimida` (`forense/notas/2026-08-01-p2-momentos-atributos.md:233`, único candidato `P3A` ya clasificado "cuenta como No de desenlace"). Universo: `gobernanza:623` + 6 payloads ENASEM + precedente `forense/notas/2026-08-01-p2-momentos-atributos.md`, 2026-08-13 | **SIN-RUTA** | BAJA — único proxy de θ sin desenlace propio conocido, sin diseño muestral publicado (`data/diseno-muestral.yaml:465-466`), universo declarado |

---

## 6 · Cruce obligatorio de la reclasificación — verificación fila por fila, sin descartes resucitados

Las tres filas reclasificadas (12, 13, 14) no reabren ningún descarte sellado: `ADR-52 A`/`ADR-54` (búsquedas de `aversion_riesgo`/`sens_estatus`) no se tocan — las tres reclasificaciones son sobre `familismo_apoyo`/`familismo_obligacion`/`radio_confianza`, parámetros distintos. La marca C3 del candidato `ENIF p9_9_4` (fila 12) **no se levanta** — sigue circular, sigue sin usarse; el nuevo candidato de ENBIARE es una vía distinta, no una reapertura del descarte. Detalle de la doble fuente (`abrir4` + `relaciones.tsv`, sin contradicción entre ambas) y de las dos correcciones a cifras de la addenda (commit-count de `relaciones.tsv`, candidatos ISSP/Banco Mundial en `cola-adquisicion`), en `forense/notas/2026-08-13-censo-v1_1-abrir4-enasem.md` §6.

---

## 7 · Reparto — comando y resultado

**La receta se verifica antes de creer la cifra (v2.3), otra vez — mismo hallazgo que v1.0 §7 tuvo con su propia receta, esta vez sobre la receta ya corregida.** Primer intento, con la receta idéntica a la de v1.0 §7, corrida contra un borrador de este archivo que describía la reclasificación de las filas 12/13/14 citando literalmente la palabra `SIN-RUTA` dentro de su propia celda `Ruta` (p. ej. "reclasificada de `SIN-RUTA`"):

```
$ grep -E '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_1.md | grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c
      3 RUTA-A
      5 RUTA-C
      1 RUTA-I
      9 SIN-RUTA
```

`9 + 3 + 5 + 1 = 18 ≠ 15` filas de datos — sobre-cuenta. Causa, verificada por `grep -nE '^\| (12|13|14) \|' ... | grep -o "SIN-RUTA" | wc -l` → `3`: las tres filas reclasificadas mencionaban su propia clase anterior dentro de la misma línea de datos que la receta escanea, y `grep -oE` extrae **todas** las coincidencias por línea, no la primera — exactamente el modo de falla que v1.0 §7 ya documentó para su primer intento (auto-referencia dentro del texto que la receta cuenta). **Corregido**: las celdas `Ruta` de las filas 12/13/14 se reescribieron para no contener la subcadena literal `SIN-RUTA` (dicen "reclasificada desde la clase sin ruta de v1.0" en su lugar — mismo hecho, sin la etiqueta exacta que la receta busca). Receta corrida contra el archivo ya corregido:

```
$ grep -E '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_1.md | grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c
      3 RUTA-A
      5 RUTA-C
      1 RUTA-I
      6 SIN-RUTA
$ grep -cE '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_1.md
15
```

**3 + 5 + 1 + 6 = 15.** Ninguna fila quedó sin clasificar. Frente a v1.0 (`3 RUTA-A · 2 RUTA-C · 1 RUTA-I · 9 SIN-RUTA`): `RUTA-C` sube de 2 a 5 (+3, filas 12/13/14), `SIN-RUTA` baja de 9 a 6 (−3, mismas filas), `RUTA-A` y `RUTA-I` sin cambio. **El reparto se lee vigente al SHA `dcc4f6a`, no como estado del programa** — mismo criterio de honestidad que v1.0 declaró para sí mismo (§8, abajo).

---

## 8 · Foto del corpus, declarada — obligación heredada de v1.0

Este v1.1 se derivó contra `origin/main = dcc4f6a` (merge PR #196, 13/ago/2026), verificado al refrescar en el ARRANQUE de este acto (`forense/notas/2026-08-13-censo-v1_1-abrir4-enasem.md` §0). Base declarada por el encargo: `b17a6f6` — diferencia de 5 commits, las 4 de `ACTO ENLACE-1` (`relaciones.tsv`/`hallazgos.md`, corriendo en paralelo per §2 del encargo) más el merge; ninguna toca el perímetro de este censo salvo como dato citado (§6 de la nota, sobre el commit-count de `relaciones.tsv`).

**Qué se fusionó después de `b17a6f6` y no fue cruzado aquí:** nada detectado que afecte a los 15 coeficientes — `ACTO ENLACE-1` escribe `relaciones.tsv` (ISSP/WVS/CSES, 19 filas nuevas) y `hallazgos.md`, ninguno de los dos toca `N12`/`N13`/`N14` (verificado, §6 de la nota) ni ningún otro id de las 15 filas de este censo. `APERTURA-ISSP`, `SONDA-1` y el ADR de provisionalidad corren en paralelo a este mismo acto (§2 del encargo) — sus resultados, si tocan alguna de las 15 filas, no están en `main` al momento de escribir este archivo y quedan, por definición, fuera de esta foto. `SONDA-1` (PR #197, abierto) es sobre universo de puertas de trámite, no sobre los 15 coeficientes — sin traslape declarado aquí sin verificarlo línea por línea (fuera de perímetro de este acto).

**Candidatos nombrados y no perseguidos, para que quien abra el v1.2 no los pierda** (`data/cola-adquisicion-2026-08-12.tsv`, §10 de la nota): ISSP (módulo Social Networks, `CANDIDATAx13+NEGATIVAx1` para N12/N13/N14, corriendo hoy vía `APERTURA-ISSP`) y la evaluación de impacto de educación temprana del Banco Mundial (`EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014`, `CANDIDATA(APERTURA_INDETERMINADA)` para N13 — candidato de clase (iii) de ADR-57(c), sin examinar).

---

## 9 · Las dos líneas de P4 — por qué no se alcanzan las estaciones 3 y 4

**Estación 3 (receta — `milpa/procedencia.yaml` / `registro-llaves-identificacion-v1_0.md`): no se alcanza porque mover un valor `ASIGNADO` o el contador de llaves es firma de mesa, no derivación.** Este acto no tiene, de hecho, ninguna propuesta de movimiento del contador `0 de 2` — verificado en `forense/notas/2026-08-13-censo-v1_1-abrir4-enasem.md` §10: ninguna de las tres filas reclasificadas alcanza el estado `SELLADA_NO_EJERCIDA` que la receta de `registro-llaves-identificacion` exige, porque ninguna llave de ADR-57(c) cubre la relación concreta que cada una necesita. Lo que sí queda entregado, con archivo y línea citados, son tres candidatos sin llave sellada (§10 de la nota): un diseño de panel para la fila 12 sobre ENASEM (`G17`, tres olas), un candidato de clase (iii) sin examinar para la fila 13 (Banco Mundial), y los candidatos ISSP para las tres — ninguno se persigue en este acto.

**Estación 4 (contrato del motor — `validate.py`/esquema de producción): no aplica.** Este acto no produce ninguna especificación de producción; la aplicaría el acto de estimación que use estas rutas, si mesa autoriza perseguir alguno de los candidatos de la estación 3.

**Este acto no hace lo que este censo no hace:**

No abre microdato — trabaja sobre diccionarios (`enasem*_fd_xlsx`, verificados por hash antes de abrirse), sobre `abrir4`/`verif3` (ya abiertos por un acto previo, leídos aquí) y sobre `gobernanza:623`. No convierte co-observación en llave — (B) sin (C) no es `RUTA-I`, en ninguna de las tres filas reclasificadas. No mueve llaves `0 de 2` ni ningún valor de `procedencia.yaml`. No amplía la lista de llaves de ADR-57(c) — la precondición de panel de ENASEM para la fila 12 se propone, no se sella. No edita `censo-estimabilidad-coeficientes-v1_0.md` ni ningún TSV de `abrir4`/`verif3`. No audita los demás cierres del corpus fuera de estas 15 filas.
