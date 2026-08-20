# El motor adaptativo por celda: seleccionar el estimador, no imponerlo
### Propuesta sin sello · v0.5 · 20/ago/2026

> | | |
> |---|---|
> | **ARCHIVO** | `propuesta-motor-adaptativo-celda-v0_5.md` |
> | **REEMPLAZA A** | `propuesta-motor-adaptativo-celda-v0_4.md` — se conserva, no se borra. v0.1-v0.4 son historia de esta propuesta; no se editan (v0.4 gana un banner de una línea que apunta aquí, patrón exacto del banner que v0.3 ya lleva) |
> | **CLASE** | Corrección de vocabulario, ordenada por `ADR-128` (D-4/D-5/D-6). Aplica sobre el contrato ya adoptado (v0.4, vigente desde `ADR-71(d)`; `ADR-128(d)` confirma que sigue vigente y sube a v0.5 aquí) — no reabre la tesis, no reabre la celda-D como unidad, no reabre ninguna de las cinco colisiones de vocabulario ya resueltas (v0.2/v0.3 §1) |
> | **ORIGEN** | `ACT-PIL-1 · CONTRATO-v0_5` (encargo, 20/ago/2026), gateado por la fusión de `PR #295` (`ACTO SELLA-ADV`, `ADR-128`) — compuerta verificada en este acto: `D-2`/`D-4`/`D-5` legibles en `ADR-128` (`canon/gobernanza-v1_15.md`, entrada `ADR-128`) |
> | **QUÉ CAMBIA DE v0.4** | §3: `rol` se abre a `BASELINE_INGENUO`/`ENSAMBLE` (+ campo hermano `variante_corredor` para las dos dietas de información de `L`); `resultado` se parte en `resultado` (prosa, sin cambio) + `estado_decidibilidad` (enum nuevo, cerrado y validado); nace `margen_material` (opcional, número o `PENDIENTE-DERIVACION`); `vocabulario_version` sube a `0.5` (`0.4` sigue siendo un valor válido). Fuera del contrato YAML de celda-D pero parte del mismo acto: el espacio de rótulos `D` entra a `canon/registro-rotulos.tsv` y al vigía `T25` de `tests/check.py` |
> | **QUÉ NO DECIDE** | Sin cambio respecto a v0.4: ningún valor de ningún parámetro; la granularidad D de ningún eje; M1 (la relación con `propuesta-motor-matriz-v0_1.md`) sigue abierta. Nuevo en v0.5: no fija ningún `margen_material` real ni banda TOST — `D-iv` del careo lo reserva al acto de pre-registro, sobre los EE reales del set; no escribe ninguna celda-D; no construye el marco de 40-60 candidatas de `ADV1-M1` |

---

## 0 · La tesis, en cuatro eslabones — sin cambio respecto a v0.4

Ver v0.4 §0 (que remite a v0.3 §0). Esta versión no toca la tesis, ni la celda-D como unidad, ni ninguna de las cinco colisiones de vocabulario resueltas en v0.2/v0.3 §1.

## 1 · Cinco colisiones de vocabulario resueltas — sin cambio respecto a v0.4

Ver v0.3 §1.

## 2 · La celda-D — sin cambio respecto a v0.4

Ver v0.3 §2.

---

## 3 · El contrato de una celda-D — cinco cambios, ordenados por `ADR-128`

**El defecto que esta versión corrige, verificado antes de escribir una línea de vocabulario nuevo:** el diseño v2 del piloto adversarial L-vs-M (`ADR-128(e)`, adoptando el careo `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B completo) introduce cinco corredores — `L-solo`, `L+corpus`, `M`, `B`, `E` (la propia ficha del careo los agrupa como "cuatro corredores: **L** en dos variantes etiquetadas, **M**, **B**, **E**" — se cuentan cinco aquí porque es al nivel de *candidato* dentro de una celda-D, no de corredor-agregado, donde el contrato necesita distinguirlos) — y un mecanismo de veredicto de dos niveles (`ADR-128(e)`, `D-4`/`M4`/`M5`) que el vocabulario de v0.4 no tiene dónde declarar. Cuatro huecos verificados, cuatro correcciones; una quinta pieza de infraestructura (el registro de rótulos) que el propio `D-6` exige para que el espacio `D` no quede fuera del vigía que ya cubre `M`/`E`.

### (a) · `rol` se abre a `BASELINE_INGENUO` y `ENSAMBLE`

Hoy `rol: BASELINE | CHALLENGER | COMPLEMENTO`, y ninguno de los tres sirve para los corredores `B` o `E`: `COMPLEMENTO` está definido desde v0.3 §3.1 como "no compite, no gana ni pierde", y el validador le exige `resultado: NO-APLICA` — pero `B` (el baseline tonto obligatorio del careo §B: tasa base de la última ola pública o persistencia) **sí compite**, es la vara contra la que se mide el skill de todos los demás (`M3`: `skill = 1 − error/error(B)`). `BASELINE` y `CHALLENGER` tampoco sirven: son roles que un candidato adquiere *por celda*, no una etiqueta fija de corredor.

Se añaden dos valores:
- **`BASELINE_INGENUO`** — corredor `B`: tasa base de la última ola pública o persistencia.
- **`ENSAMBLE`** — corredor `E`: combinación mecánica `L⊕M` pre-registrada, por script.

Los corredores `L` y `M` **no** reciben un valor de `rol` propio — siguen usando `BASELINE`/`CHALLENGER`/`COMPLEMENTO` exactamente como antes, asignados por quien escriba cada celda según cuál de los dos juega cuál papel en esa comparación específica; eso es precisamente lo que T4 de este acto declara que no se decide aquí. Las dos variantes de `L` —`L-solo` (sin corpus tierizado) y `L+corpus` (con él)— no son un rol distinto: son el mismo rol (`BASELINE` o `CHALLENGER`, según la celda) con distinta dieta de información, y esa diferencia es precisamente una de las mediciones que el piloto produce (`M2`: "columna extra de la tubería, vale casi tanto como el duelo"). Se distinguen en un campo hermano, `variante_corredor: L-solo | L+corpus`, opcional — no se duplica el enum de `rol` para expresar una distinción que no es de rol.

**Los tres valores viejos no cambian de significado; las tres celdas existentes no se tocan** — ninguna de las tres usa hoy `BASELINE_INGENUO`, `ENSAMBLE` ni `variante_corredor`, y no tiene por qué: son celdas `CALIBRACION_CONJUNTA`/`COMPARACION` anteriores al piloto ADV-DUELO, no candidatas suyas.

### (b) · `resultado` se parte en dos — misma cirugía que v0.4 hizo sobre `fuerza`

v0.4 partió `fuerza` en dos campos por una razón declarada en su propio §3: *"un campo intentando cargar dos preguntas independientes, con mecanismo para una sola."* `resultado` tiene hoy exactamente ese defecto: carga "quién ganó" **y** la narrativa completa de la adjudicación — las tres celdas existentes lo traen con párrafos de 200 a 900 palabras (ver `data/curacion-registro/celdas-d/*.yaml`, campo `resultado` de cada candidato), y el propio validador declara por escrito, en su docstring, que "no valida el valor libre de `resultado` … fuera del caso `COMPLEMENTO`."

**`resultado` se queda exactamente como está: prosa, no validada** (salvo la regla ya existente de v0.3: `rol: COMPLEMENTO` exige `resultado: NO-APLICA`). Los tres archivos sellados siguen pasando sin tocarse.

**Nace `estado_decidibilidad`**, a nivel `celda_d` (no por candidato — es un veredicto de la celda, el segundo nivel que `D-4`/`M4` exige: "dos niveles de veredicto: cinco casillas al nivel del piloto; `PUNTUADA / INDECIDIBLE / SKIP:<motivo> / CONTROL-MEMORIA` al nivel de la celda"), enum cerrado y **sí validado**:

```
estado_decidibilidad: PUNTUADA | INDECIDIBLE | SKIP:<motivo> | CONTROL-MEMORIA | NO-APLICA
```

⚠️ **`INDECIDIBLE` lleva las dos condiciones de `ADV1-M3`, citadas verbatim de la ficha** (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B, `M3`): **"`INDECIDIBLE` si ambos caen dentro del IC de R o si `|d_L−d_M| < 0.5·EE(R)`."** Son dos condiciones disyuntivas (basta que se cumpla una), no una — quien adjudique una celda del piloto y aplique sólo la segunda dejaría sin marcar como `INDECIDIBLE` el caso en que ambos corredores aciertan dentro del intervalo del árbitro pero su distancia entre sí *no* es pequeña frente a `EE(R)`; ese caso también es `INDECIDIBLE` por la primera condición, y un validador de valor único no puede atraparlo — se declara aquí en vez de dejarlo como trampa para quien escriba la primera celda del piloto. `NO-APLICA` es el valor correcto para toda celda que no sea del piloto ADV-DUELO — exactamente el caso de las tres celdas existentes.

**Regla de compatibilidad, la que resuelve la tensión entre "obligatorio" y "las tres celdas no se tocan":** `estado_decidibilidad` es obligatorio **cuando `vocabulario_version: 0.5`**; no se exige, y no se lee, en una celda declarada `vocabulario_version: 0.4`. El mecanismo no es nuevo — es el mismo que v0.4 §3 regla 3 ya declaró para los conjuntos cerrado/extensible de esa versión: *"los conjuntos … se citan por número de versión, no por nombre."* Las tres celdas existentes declaran `vocabulario_version: 0.4` y no se editan en este acto (T1/T2), así que quedan exactamente donde v0.4 las dejó: sin `estado_decidibilidad`, válidas. Cualquier celda nueva que se declare bajo `vocabulario_version: 0.5` sí lo exige. Sin esta compuerta, "obligatorio" sin condición rompería los tres archivos sellados — el mismo defecto que este acto existe para no repetir (§3, T3 abajo).

### (c) · Nace `margen_material` — opcional, con ausencia declarada

```
margen_material: <número> | PENDIENTE-DERIVACION
```

Opcional: puede estar ausente, exactamente como está ausente hoy de las tres celdas existentes. Cuando el concepto aplica pero el número todavía no existe, **`PENDIENTE-DERIVACION` es el valor correcto — legal y explícito, no una omisión del campo.** La razón es `D-iv` del careo, verbatim: *"la banda TOST y el margen material NO se firman ahora: el acto de pre-registro los deriva de los EE reales del set … firmar una constante a ciegas sería el defecto v2.1 de siempre."* Fijar hoy un número, en un acto que por T4 no escribe ninguna celda-D, sería exactamente ese defecto.

Cuando el número exista, **entra como número**, interpretado sobre la escala que la propia celda ya declara en `criterio_adjudicacion.escala` — **nunca como prosa dentro de `criterio_adjudicacion.texto`**, donde ningún script lo lee (el validador no valida `texto` libre, igual que no valida `resultado` libre; un número enterrado en prosa ahí es, en la práctica, indistinguible de no tener margen material declarado).

### (d) · `vocabulario_version` sube a `0.5`

El mecanismo ya existe, v0.4 §3 regla 3: *"los conjuntos cerrados/extensibles de esta versión se citan por número de versión, no por nombre."* `vocabulario_version: 0.5` es el valor correcto para toda celda que use `BASELINE_INGENUO`/`ENSAMBLE`/`variante_corredor`/`estado_decidibilidad`/`margen_material`; `0.4` sigue siendo válido — es lo que las tres celdas existentes ya declaran, y no se les pide subir de versión para seguir pasando.

### (e) · El espacio `D` entra al registro y al vigía

`D-6` (`ADR-128`) fija la convención: *"lo que ya está en uso se registra … no se renombra … un vigía lo hace mecánico."* Hoy `canon/registro-rotulos.tsv` censa los espacios `M` y `E`, y `tests/check.py` (`T25`) sólo vigila esos dos (`_T25_ROTULO_BARE = re.compile(r"(?<![A-Za-z0-9_-])(M|E)-?(\d{1,2})(?![A-Za-z0-9_.])")`). El espacio `D` es, desde `ADR-128`, un espacio de rótulo real y vivo, con dos habitantes: `D-1`…`D-6` (`ACTO SELLA-ADV`, firmas de mesa) y `D-i`…`D-iv` (careo §C). Se registra igual que `M`/`E`: filas nuevas en `canon/registro-rotulos.tsv` para los diez rótulos, y el regex de `T25` se extiende de `(M|E)` a `(M|E|D)`.

**Derivado, no supuesto — mi propia cuenta, sobre la entrada `ADR-128` de `canon/gobernanza-v1_15.md` completa (título + incisos (a)-(g) + "Lo que este ADR NO hace" + "Cascada" + cierre "→ Vigente"):**

| rótulo | apariciones | dónde |
|---|---|---|
| `D-1` | 1 | título/preámbulo, en el rango `` `D-1`…`D-6` `` |
| `D-2` | 1 | inciso (d): "`D-2` de mesa lo confirma" |
| `D-4` | 5 | título/preámbulo ×2 ("sella `D-4`", "que `D-4` adopta completo"); inciso (b) ×1 ("que `D-4` adopta completa"); inciso (e) ×2 ("(e) `D-4`, `D-5` y `D-6` sellados", "`D-4` — se adopta el diseño v2") |
| `D-5` | 3 | título/preámbulo ×1; inciso (e) ×2 ("… `D-5` y `D-6` sellados", "`D-5` — los cuatro corredores") |
| `D-6` | 6 | título/preámbulo ×2 ("y `D-6`", rango `` `D-1`…`D-6` ``); inciso (e) ×2 ("… y `D-6` sellados", "`D-6` — convención de rótulos"); inciso (g) ×1 ("`D-6` firma la convención"); "Lo que este ADR NO hace" ×1 ("`D-6` lo prohíbe explícitamente") |
| `D-iv` | 1 | "Lo que este ADR NO hace": "`D-iv` del careo ya lo advierte" |

Coincide exacto con `1×D-1, 1×D-2, 5×D-4, 3×D-5, 6×D-6, 1×D-iv` — los dos sistemas de rótulo (`M`/`E` ya vigilados, `D` todavía no) conviven, verificado, dentro de la misma entrada de ADR. Ese es el hueco que esta letra cierra.

### 3.1 · `rol: COMPLEMENTO` — un candidato que no compite (H1/H2) — sin cambio respecto a v0.4

Ver v0.3 §3.1.

### 3.2-3.9 · Resto del contrato — sin cambio respecto a v0.4

Ver v0.4 §3.2-3.9 (que remite a v0.3 §3.2-3.9, con la nota de que "D6 (fuerza/calibrado)" sigue siendo la misma categoría de decisión, sólo renombrada). Nada de esto se toca aquí.

---

## 4 · Relación con `propuesta-motor-matriz-v0_1.md` — sin cambio respecto a v0.4

Ver v0.3 §4. M1 sigue abierta.

## 4-bis · Celdas-D semilla — a diferencia de v0.4, esta versión NO reescribe los archivos

v0.4 reescribió las dos celdas-D semilla de entonces con su vocabulario nuevo, directamente en `data/curacion-registro/celdas-d/*.yaml` (v0.4 §4-bis). **Esta versión hace lo opuesto, por instrucción explícita del encargo (`ACT-PIL-1 · CONTRATO-v0_5`, T1/T2/T3): las tres celdas-D hoy en disco — `G5.familismo_obligacion.actitud`, `G5.radio_confianza.encuci_vs_enbiare`, `G5.obligacion_medida.conducta` — no se editan.** Pueden no tocarse precisamente porque `estado_decidibilidad` (§3(b) arriba) sólo es obligatorio bajo `vocabulario_version: 0.5`, y las tres siguen declarando `0.4` — la compuerta de compatibilidad que v0.4 mismo estableció (citar por versión, no por nombre) es lo que hace posible que v0.5 amplíe el vocabulario sin forzar una reescritura. Verificado en este acto (T3 del encargo, salida cruda pegada en la nota de cierre): las tres siguen validando contra el contrato ampliado, sin editarse.

## 5 · Vertical piloto — sin cambio respecto a v0.4

Ver v0.3 §5.

## 6 · Ejemplo trabajado — sin cambio respecto a v0.4

Ver v0.3 §6.

## 7 · Lo que esta propuesta no resuelve

Todo lo que v0.4 §7 ya declaraba, sin cambio, más: el contenido final de `margen_material` para ninguna celda real — `D-iv` lo reserva al acto de pre-registro sobre los EE reales del set, y ese acto no es éste; el marco de 40-60 candidatas de `ADV1-M1` — es el primer acto de la serie `ACT-PIL`, no éste; si `L`/`M` deberían, en algún acto futuro, tener sus propios valores de `rol` en vez de compartir `BASELINE`/`CHALLENGER` — no se vio evidencia de esa necesidad al escribir esta versión, y no se decide sin ella.

## 8 · Preguntas para mesa

Ninguna pregunta nueva. Las diez de v0.3 §8 y la de v0.4 §8 siguen resueltas como estaban; ninguna se reabre aquí. Este acto no abre fila de tablero (`FP-NN`) — es la aplicación mecánica de cinco decisiones ya firmadas (`D-2`, `D-4`, `D-5`, `D-6` de `ADR-128`), no una pregunta nueva.

## 9 · Módulo de auditoría

**1-6** · No aplican, igual que v0.1-v0.4.

**7 · ¿Qué conclusión sería peligrosa simplificada?** Las de v0.4, sin cambio, más una octava: *"abrir `rol` a `BASELINE_INGENUO`/`ENSAMBLE` y separar `resultado`/`estado_decidibilidad` ya deja el contrato listo para correr el piloto"* — no lo deja: el marco de 40-60 candidatas no existe (`ADV1-M1`), ningún `margen_material` real está derivado (`D-iv`), y ninguna celda-D del piloto se ha escrito. El cascarón queda listo para recibirlas, que es distinto de estar poblado. Y una novena, específica de `estado_decidibilidad`: *"con el enum cerrado, `INDECIDIBLE` ya está bien aplicado en cualquier celda que lo use"* — el validador sólo verifica que el valor elegido sea uno de los cinco legales; verificar que **cuál** de los cinco se eligió respeta las dos condiciones verbatim de `ADV1-M3` es un juicio sobre el dato de esa celda, no algo que un validador de esquema pueda comprobar.

**8 · ¿Qué fue derivado y qué no?** Derivado o verificado de primera mano en este acto: `v0_5` `NO-ENCONTRADO` (`ls propuesta-motor-adaptativo-celda-v0_*.md` sobre el SHA de arranque, re-verificado, sólo v0.1-v0.4 presentes); `BASELINE_INGENUO`/`ENSAMBLE`/`estado_decidibilidad` ausentes de `tests/test_celdas_d.py`, verificado por lectura completa del archivo, no sólo por conteo de coincidencias; el censo de rótulos `D` sobre la entrada completa de `ADR-128` (tabla en §3(e) arriba); la cita verbatim de `ADV1-M3` y de `D-iv`, leídas de `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`; que las tres celdas-D existentes no declaran `estado_decidibilidad` ni `margen_material` ni `variante_corredor`, verificado leyendo los tres archivos completos; que `milpa/src/motor.py` no lee `rol`, `resultado`, `estado_decidibilidad`, `margen_material` ni `vocabulario_version` de ninguna celda — sólo `estado_operativo`, `tipo_adjudicacion` e `id` —, verificado leyendo el módulo completo, lo que explica por qué corre idéntico antes y después de este acto (T4, hash de salida pegado en la nota de cierre). **No derivado por esta sesión, incorporado tal cual por instrucción explícita del encargo:** la clasificación de los cinco corredores del careo §B y el diseño de las cinco casillas de `M5` — esta sesión no diseñó el piloto ADV-DUELO, sólo le da vocabulario de contrato.

**Contadores movidos por el trabajo que produjo esta versión: 0.** Ninguna celda-D se ejecuta ni se escribe; este acto amplía un vocabulario de contrato para que el piloto tenga dónde escribir, no mide nada del programa.

**(v2.4) Cantidades y escalas:** ninguna cantidad estimada nueva se transcribe en esta versión.

---

## Changelog

**v0.4 → v0.5 · 20/ago/2026 (`ACT-PIL-1 · CONTRATO-v0_5`, `ADR-129`).**
1. §3(a): `rol` gana `BASELINE_INGENUO` y `ENSAMBLE`; nace el campo hermano opcional `variante_corredor: L-solo | L+corpus`. Los tres valores viejos y las tres celdas existentes no se tocan.
2. §3(b): `resultado` se parte — se queda como prosa no validada; nace `estado_decidibilidad` (enum cerrado, validado, obligatorio sólo bajo `vocabulario_version: 0.5`).
3. §3(c): nace `margen_material`, opcional, número o `PENDIENTE-DERIVACION`.
4. §3(d): `vocabulario_version` acepta `0.4` y `0.5`.
5. §3(e): el espacio de rótulos `D` entra a `canon/registro-rotulos.tsv`; `tests/check.py` `T25` extiende su regex de `(M|E)` a `(M|E|D)`.
6. `tests/test_celdas_d.py` actualizado en consecuencia (detalle y salida cruda: nota de cierre del acto).
7. Ningún otro cambio: `data/curacion-registro/celdas-d/*.yaml` no se toca, `milpa/src/` no se toca, ningún `margen_material` real se fija, ninguna celda-D nueva se escribe, ningún contador de medición sobre México se mueve.
