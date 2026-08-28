# Estado del motor · los 15 pares generador×coeficiente, reconciliados · v1.0

`ACTO MAESTRA31-E10 · RECONCILIA-MOTOR`, 27/ago/2026. Encargo: `forense/encargos/2026-08-27-MAESTRA31-E10-RECONCILIA-MOTOR.md` (dirección, maestra-31, archivado por A.3 antes de ejecutar; GATED a que `PR #390`/`ACTO MAESTRA31-E9 · ESTIMA-RUTAC` fusionara — cumplido, `merge commit 7c2096d`).

**Universo declarado (A.10):** clon propio `/home/user/Modelado-Mexicano`, rama `claude/reconcilia-motor-contador-field-uktyd7`, `HEAD = c87ad39` (un commit propio — el archivo de este encargo — sobre `7c2096d`, merge de `PR #390`). Entorno **NUBE** (`cloud_default`); `data/raw` ausente y no se usa; sin red, sin API, sin microdato. Todas las cifras de este documento se derivaron por comando contra este clon, nunca contra el espejo.

Secciones consultadas, las tres con `yaml.safe_load` y lectura íntegra de cada campo (nunca `grep` de subcadena ni `sed` de una línea):

- `milpa/procedencia.yaml:coeficientes_generador_medidos` (línea 884, sección **A**, 6 entradas)
- `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.detalle` (línea 1108, sección **B**, 15 filas)
- `milpa/procedencia.yaml:asignados_coeficiente.detalle` (línea 837, sección **C**, 6 filas-generador / 15 pares)
- `canon/modelo-decision-v4_0.md` §2.1-2.2 (líneas 422-460) — cláusulas falsables y tabla de coeficientes de los 7 generadores
- `forense/escalas-eleccion-ciega-v1_0.md` (52 líneas, íntegro) — Paso 2 de `FP-149`/`ADR-173`
- `forense/firmas-pendientes.tsv` filas `FP-149`, `FP-152`, `FP-176` (leídas con `csv.DictReader`, columna por columna, no como texto plano)
- `forense/cobertura-motor.md`, `forense/censo-estimabilidad-coeficientes-v1_2.md` (conteo de referencias a la sección A, ver §4)

**Denominador de este documento: 15** — los pares `gen.coef` de `rutas_estimabilidad_coeficiente.detalle`, que es también la unidad nativa de `coeficientes_generador_medidos` (por nombre) y de `asignados_coeficiente.detalle` (sumando los `coefs` de sus 6 filas-generador: `G1(2)+G2(2)+G3(3)+G4(4)+G5(3)+G6(1)=15`, verificado por comando en §4). **No es la misma unidad que "30 parámetros"** — ver §4, no se fuerza la equivalencia.

---

## 0 · Mapeo — Paso 1, antes de contar nada

### 0.1 · Sección A (`coeficientes_generador_medidos`, 6 entradas) → pares `gen.coef` de B

Derivado por `yaml.safe_load`, comparando cada `clase:` completa (no solo si la clave "suena" a GATE) y cruzando `beta_hat` presente/ausente:

| Clave de A (línea) | `clase:` (resumen) | ¿`beta_hat`? | Par `gen.coef` de B al que mapea |
|---|---|---|---|
| `G1_radio_confianza` (885) | MEDIDO·β̂, 3 ítems, marginal | SÍ (891) | `G1.radio_confianza` — match literal |
| `G1_confianza_institucional` (934) | MEDIDO·β̂, 1 ítem, marginal, TRUNCADO | SÍ (940) | `G1.confianza_institucional` — match literal |
| `G3_familismo_apoyo` (966) | MEDIDO·β̂, 1 ítem, marginal | SÍ (972) | `G3.familismo_apoyo` — match literal |
| `G4_exposicion_violencia` (994) | MEDIDO·β̂, condicional(ejes) | SÍ (1001) | `G4.exposicion_violencia` — match literal |
| `G4_confianza_institucional_justicia` (1025) | MEDIDO·β̂, condicional(ejes), por institución | SÍ (1032) | `G4.confianza_institucional` — **no es match literal, resuelto abajo (0.2)** |
| `G3_horizonte_temporal` (1060) | **GATE·ID-X** — "NO es una estimación" | **NO** (campo `beta_hat` no existe; hay `gate_id_x`) | `G3.horizonte_temporal` — match literal de nombre, pero sin β̂ (ver 0.3) |

### 0.2 · El caso que no casa por nombre: `G4_confianza_institucional_justicia` vs `G4.confianza_institucional`

Abierto completo, no forzado. Tres piezas de evidencia, las tres apuntan a la misma conclusión:

1. **`canon/modelo-decision-v4_0.md:458`** (tabla de coeficientes, §2.2), citado íntegro: `G4 | \`exposicion_violencia 0.70\` · \`confianza_institucional[justicia] −0.40\` · \`horizonte_temporal −0.20\` · \`sens_estatus −0.15\``. El nombre **canónico** del coeficiente de G4 ya lleva el calificador `[justicia]` — no es un sub-componente nuevo, es el nombre completo del coeficiente tal como el modelo lo declara. Es el mismo patrón que `G1a` usa para el suyo: `canon/modelo-decision-v4_0.md:454`, `confianza_institucional[financiera] −0.60` (y la nota de la línea 460 lo confirma explícitamente: *"`G4` no comparte este problema: usa `confianza_institucional[justicia]`, componente nombrado, sin selección variable"*). `rutas_estimabilidad_coeficiente.detalle` y `asignados_coeficiente.detalle` simplemente no repiten el calificador entre corchetes en su clave YAML (`gen: G4` ya desambigua de `G1`), pero el coeficiente que nombran es el mismo.
2. **`asignados_coeficiente.detalle[3]` (línea 853)**: `G4.coefs.confianza_institucional = -0.40` — coincide exacto con el valor `ASIGNADO` que la propia entrada `A.G4_confianza_institucional_justicia` (línea 1027, campo `antes`) cita como lo que su β̂ intentaría eventualmente compararse contra: *"ASIGNADO -- coeficiente de generador (G4 -0.40, canon/modelo-decision-v4_0.md:396)..."*. Un solo slot `-0.40` en todo el motor; ambas entradas apuntan a él.
3. **Universo de la medición** (línea 1028, campo `universo`, y línea 1032, campo `beta_hat`): los 7 ítems medidos (`AP5_4_01/02/03/05/06/07/11` — Tránsito, Preventiva, Estatal, Ministerial/Judicial, MP y Fiscalías Estatales, FGR, Jueces) son exactamente las instituciones de justicia/seguridad — el universo del `[justicia]` canónico, no una sub-dimensión más estrecha de un `confianza_institucional` genérico de G4 que exista aparte. No hay, en `canon/modelo-decision-v4_0.md` §2.2, ningún segundo coeficiente `G4.confianza_institucional[algo-más]` del que `[justicia]` sea una fracción.

**Veredicto: NO es AMBIGUO — es el mismo coeficiente**, con el nombre completo en A (`_justicia`, heredado del calificador canónico) y el nombre corto en B/C (donde `gen: G4` ya lo desambigua de `G1.confianza_institucional[financiera]`). Coincide, además, con cómo `ACTO MAESTRA31-E9` ya trató el par en `procedencia.yaml:1120` (nota: *"ver milpa/procedencia.yaml:coeficientes_generador_medidos.G4_confianza_institucional_justicia"*) — este acto no inventa la equivalencia, la confirma contra `modelo-decision-v4_0.md`, que ninguno de los actos anteriores había citado para este punto específico.

### 0.3 · `G3_horizonte_temporal`: el GATE no produce β̂

Aunque el nombre casa limpio con `G3.horizonte_temporal` (única fila `RUTA-I` de B), la entrada de A es una **compuerta de identificación**, no una medición: campo `clase` (línea 1061) dice explícitamente *"GATE·ID-X ... NO es una estimación: el gate detiene el acto antes de cruzar exposición contra desenlace"*, y el campo `estimando` (dentro de esa misma entrada) dice, verbatim: *"NINGUNO. ... no se calculó RR, razón de riesgo ni intervalo de confianza... El contador 0 de 15 no se mueve."* No tiene campo `beta_hat` (verificado: la clave no existe en el dict de Python). Este par **no cuenta como β̂ medido** en la tabla de §1 — cuenta como "intento documentado, sin resultado", categoría distinta tanto de "medido" como de "sin intentar", y se anota así en la celda.

### 0.4 · Pares de B sin ninguna entrada en A (9 de 15)

`G2.sens_estatus` · `G2.aversion_riesgo` · `G3.aversion_riesgo` · `G4.horizonte_temporal` · `G4.sens_estatus` · `G5.familismo_apoyo` · `G5.familismo_obligacion` · `G5.radio_confianza` · `G6.deferencia`. Ninguno tiene clave correspondiente en `coeficientes_generador_medidos` (verificado por comando, §1 abajo) — no hay ambigüedad que resolver en estos 9, simplemente no hay intento de medición registrado en A. (Dos de ellos, `G5.familismo_apoyo` y `G5.radio_confianza`, comparten *fuente de la θ* con pares que sí tienen β̂ propio — `G3.familismo_apoyo` y `G1.radio_confianza` respectivamente — pero eso es solo la columna 2 (escala de la θ) de la tabla en §1; no hay β̂ medido para el coeficiente de **G5** en ninguno de los dos casos, verificado: ninguna clave `G5_familismo_apoyo` ni `G5_radio_confianza` existe en A.)

---

## 1 · La tabla — 15 pares, 4 columnas

Convenciones: **col.1** `¿β̂ medido?` = SÍ solo si A tiene una entrada con campo `beta_hat` real (no un gate); **col.2** `¿escala θ declarada?` = SÍ si `escala_derivada` (campo completo, leído entero) termina en `ELEGIDA-CIEGA`, NO si termina en `SUBDETERMINADA-PERSISTENTE`; **col.3** `¿escala del generador declarada?` = si `canon/modelo-decision-v4_0.md` §2.1-2.2 declara una forma funcional/unidad numérica para la **salida del generador** (no para la θ) — distinta de la columna 2, ver §2; **col.4** `ruta` = campo `ruta:` de B, ya corregido por E9.

| # | gen.coef (línea B) | 1·β̂ medido | 2·escala θ | 3·escala generador | 4·ruta |
|---|---|---|---|---|---|
| 1 | `G1.confianza_institucional` (1112) | **SÍ** — A:934, −0.0645 [IC95% −0.0744,−0.0546], n=37755 (4/ago, Encargo W) | **SÍ** — ELEGIDA-CIEGA, proporción[0,1]/identidad, ancla `condicionales_confianza_institucional.financiera` | **NO** | RUTA-A |
| 2 | `G1.radio_confianza` (1113) | **SÍ** — A:885, 3 ítems AP5_1_1/2/3 (−0.0102/−0.0113/−0.0269, IC en A:891), n hasta 13393 | **SÍ** — ELEGIDA-CIEGA, ancla `condicionales_escalares.radio_confianza` | **NO** | RUTA-A |
| 3 | `G2.sens_estatus` (1114) | NO — sin entrada en A | NO — SUBDETERMINADA-PERSISTENTE | **NO** | SIN-RUTA |
| 4 | `G2.aversion_riesgo` (1115) | NO — sin entrada en A | NO — SUBDETERMINADA-PERSISTENTE | **NO** | SIN-RUTA |
| 5 | `G3.horizonte_temporal` (1116) | NO — **intentado y bloqueado**, A:1060 GATE·ID-X, cero β̂ producido (§0.3) | NO — SUBDETERMINADA-PERSISTENTE | **NO** | RUTA-I |
| 6 | `G3.aversion_riesgo` (1117) | NO — sin entrada en A | NO — SUBDETERMINADA-PERSISTENTE | **NO** | SIN-RUTA |
| 7 | `G3.familismo_apoyo` (1118) | **SÍ** — A:966, +0.0279 [IC95% 0.0029,0.0529], n=11464 (4/ago, Encargo W) | **SÍ** — ELEGIDA-CIEGA, ancla `condicionales_escalares.familismo_apoyo` | **NO** | RUTA-A |
| 8 | `G4.exposicion_violencia` (1119) | **SÍ** — A:994, marginal +16.614pp [IC95% 13.995,19.234], n=13023 (MESA-E1, 4/ago) | **SÍ** — ELEGIDA-CIEGA, ancla `condicionales_escalares_exposicion_violencia.exposicion_violencia` | **NO** — ASIGNADO 0.70 sin forma/enlace, `modelo-decision:458` | RUTA-A |
| 9 | `G4.confianza_institucional` (1120) | **SÍ** — A:1025 (`..._justicia`, §0.2), 7 ítems, β̂ en A:1032 (−4.683 a −11.269pp, todos IC95% excluyen 0), n por ítem 3672-9843 (MESA-E1, 4/ago) | **SÍ** — ELEGIDA-CIEGA, ancla `condicionales_confianza_institucional.justicia-policía` | **NO** — ASIGNADO −0.40 sin forma/enlace, `modelo-decision:458` | RUTA-A |
| 10 | `G4.horizonte_temporal` (1121) | NO — sin entrada en A | NO — SUBDETERMINADA-PERSISTENTE | **NO** | SIN-RUTA |
| 11 | `G4.sens_estatus` (1122) | NO — sin entrada en A | NO — SUBDETERMINADA-PERSISTENTE | **NO** | SIN-RUTA |
| 12 | `G5.familismo_apoyo` (1123) | NO — sin entrada en A (θ comparte fuente con `G3.familismo_apoyo`, pero G5 no tiene β̂ propio, §0.4) | **SÍ** — ELEGIDA-CIEGA, ancla `condicionales_escalares.familismo_apoyo` | **NO** | SIN-RUTA |
| 13 | `G5.familismo_obligacion` (1124) | NO — sin entrada en A | NO — SUBDETERMINADA-PERSISTENTE | **NO** | SIN-RUTA |
| 14 | `G5.radio_confianza` (1125) | NO — sin entrada en A (θ comparte fuente con `G1.radio_confianza`, pero G5 no tiene β̂ propio, §0.4) | **SÍ** — ELEGIDA-CIEGA, ancla `condicionales_escalares.radio_confianza` | **NO** | SIN-RUTA |
| 15 | `G6.deferencia` (1126) | NO — sin entrada en A | NO — SUBDETERMINADA-PERSISTENTE | **NO** | SIN-RUTA |

**Evidencia de la columna 3 (uniforme, las 15 filas — tres fuentes independientes, ninguna de este acto):**

- `canon/modelo-decision-v4_0.md:448-450`: *"Los quince coeficientes son `ASIGNADO`. Ninguno es medido... un coeficiente es una elasticidad, y el corpus es transversal — da estados, no ritmos... El signo de los generadores está bien sostenido por el corpus. La magnitud no."*
- `forense/escalas-eleccion-ciega-v1_0.md:17,30`: criterio 2 del propio procedimiento de Paso 2 ("naturaleza declarada de la salida del generador") se aplicó a las 15 filas y **no produjo nada en ninguna**: *"criterio 2 no produce nada (ningún generador de `canon/modelo-decision-v4_0.md` §2.1 declara escala numérica en su cláusula falsable — verificado sobre la tabla completa del §2.1 leída para este acto)"*.
- `forense/firmas-pendientes.tsv` fila `FP-149` (FIRMADA, `ADR-173`): *"...ninguna forma funcional ni funcion de enlace (ningun ADR de D-ABC la ha sellado a la fecha). Esto gatea/bloquea cualquier comparacion futura de magnitud entre un beta medido y su ASIGNADO correspondiente... hasta que mesa selle una funcion de enlace o adjudique via otra ruta."* — el gate sigue activo hoy: ningún ADR posterior a `ADR-173` sella esa función de enlace (verificado, `grep -n "función de enlace\|funcion de enlace" canon/gobernanza-v1_15.md` entre `ADR-173` y el máximo actual, sin hits que la sellen).

**Nota sobre la columna 2 vs. columna 3 — no son la misma cosa, y confundirlas es el error que A-bis 3 prohíbe.** `ELEGIDA-CIEGA` (columna 2) es una convención *impuesta* para la θ (proporción ponderada `[0,1]`, enlace identidad) elegida precisamente **porque** ningún criterio anterior — incluido "la salida del generador declara su propia escala" (criterio 2, el que llenaría la columna 3) — produjo nada. Que la columna 2 diga SÍ no implica que la columna 3 diga SÍ: son extremos distintos de la misma relación (θ vs. salida del generador), y el criterio 3 que resuelve la columna 2 es explícitamente el que se usa *cuando* la columna 3 no tiene respuesta.

---

## 2 · La intersección y las tres cifras, por separado

Derivado por comando sobre la tabla de §1 (no a mano):

```
col.1 (β̂ medido):                5 de 15  -- G1.confianza_institucional, G1.radio_confianza,
                                             G3.familismo_apoyo, G4.exposicion_violencia,
                                             G4.confianza_institucional
col.2 (escala θ = ELEGIDA-CIEGA): 7 de 15  -- los 5 de arriba + G5.familismo_apoyo + G5.radio_confianza
col.3 (escala generador declarada): 0 de 15 -- ninguna fila, ver evidencia de §1
col.1 ∧ col.2 (β̂ Y escala θ):     5 de 15  -- exactamente el mismo conjunto que col.1
                                             (los 5 con β̂ son, sin excepción, los 5 cuya θ
                                             también resolvió ELEGIDA-CIEGA)
col.1 ∧ col.2 ∧ col.3:            0 de 15
```

**No se fusionan en un número.** Son tres preguntas distintas con tres remedios distintos:

- **7 de 15 topados por falta de dato, sin ningún intento registrado** (columnas 1 y 2 ambas NO): `G2.sens_estatus`, `G2.aversion_riesgo`, `G3.aversion_riesgo`, `G4.horizonte_temporal`, `G4.sens_estatus`, `G5.familismo_obligacion`, `G6.deferencia`. El remedio sería un reactivo/instrumento nuevo — el mismo techo que `censo-estimabilidad-coeficientes-v1_2.md` ya documentó para estas filas bajo `SIN-RUTA`.
- **2 de 15 con θ resuelta pero sin β̂ propio** (columna 2 SÍ, columna 1 NO): `G5.familismo_apoyo`, `G5.radio_confianza` — la θ tiene escala porque comparte fuente con un par hermano ya medido (`G3.familismo_apoyo`, `G1.radio_confianza`), pero **G5 mismo** no tiene una medición propia. El remedio sería una medición nueva sobre G5, no un cambio de escala.
- **1 de 15 intentado y bloqueado por el propio diseño de identificación** (`G3.horizonte_temporal`, GATE·ID-X): no es "falta de dato" en el sentido de "nadie lo intentó" — se intentó, con n reales, y el gate lo detuvo antes de cruzar exposición contra desenlace (§0.3). Remedio distinto de los dos anteriores: no es un instrumento nuevo, es una pregunta de si vale la pena una llave de identificación distinta.
- **5 de 15 con β̂ Y escala de θ, topados únicamente por falta de escala del generador** (columnas 1 y 2 ambas SÍ, columna 3 NO): `G1.confianza_institucional`, `G1.radio_confianza`, `G3.familismo_apoyo`, `G4.exposicion_violencia`, `G4.confianza_institucional` — exactamente las 5 filas `RUTA-A`. Esto es lo más avanzado que hay en el motor, y ninguno de los 5 se puede escribir en el ejecutable hoy: falta la función de enlace entre la escala del β̂ (diferencia de proporciones/puntos porcentuales del desenlace) y la escala del coeficiente `ASIGNADO` del generador (una elasticidad sin unidad declarada) — el gate de `FP-149`, todavía activo (§1).
- **0 de 15 completos** (columnas 1, 2 y 3 las tres SÍ): ver §3.

Total de las cuatro categorías mutuamente excluyentes: 7 + 2 + 1 + 5 = 15. Cuadra.

---

## 3 · La pregunta que cierra la jornada

> *De los 15 pares, ¿cuántos están topados por falta de dato, cuántos por falta de escala del generador, y cuántos ya están completos y nadie lo había notado?*

Con la tabla de §1 y el recuento de §2 delante:

- **Topados por falta de dato** (ningún β̂, o β̂ intentado y bloqueado): **8 de 15** (los 7 sin ningún intento + `G3.horizonte_temporal`, el GATE).
- **Topados únicamente por falta de escala del generador** (ya tienen β̂ y escala de θ, les falta solo la función de enlace del lado del generador): **5 de 15** — las 5 `RUTA-A`.
- **Con θ resuelta pero sin β̂ propio de G5** (categoría intermedia que no es ninguna de las dos anteriores, ver §2): **2 de 15**.
- **Ya completos, con las tres columnas satisfechas, y nadie lo había notado: CERO.**

**El rendimiento del acto es cero.** No hay ningún par de los 15 que hoy tenga β̂ medido, escala de θ declarada y escala del generador declarada a la vez — porque la columna 3 nunca se satisface para ninguna fila, con o sin este acto: es un bloqueo estructural del propio `canon/modelo-decision-v4_0.md` (§2.2: "los quince coeficientes son ASIGNADO... ninguna fuente citada publica elasticidades"), gateado formalmente por `FP-149` desde el 25/ago, no algo que este acto de conteo pudiera haber movido. La expectativa que el propio encargo insinúa en su CONTADOR — *"si resulta que algunos pares ya estaban completos... ése es el contador"* — **no se cumple**: lo que sí se confirma es la mitad de esa hipótesis (5 pares llegaron mucho más lejos de lo que ningún censo previo mostraba, por la brecha de perímetro de §4), pero ninguno cruza la meta completa, porque la meta completa exige algo — la función de enlace del generador — que ningún acto de conteo puede producir; eso es una decisión de escala que le corresponde a mesa o a un acto de diseño, no a una reconciliación de censos.

Esto es, en sí mismo, la reconciliación de la brecha de perímetro: `cobertura-motor.md` y `censo-estimabilidad-coeficientes-v1_2.md` (que nunca leyeron la sección A, ver §4) medían solo la columna 4 (ruta) y no podían ver que 5 de las 9 filas que su propio vocabulario `RUTA-A`/`RUTA-C` ya distinguía como "asociación estimada" tenían, de hecho, tanto β̂ como escala de θ completos desde el 25/ago — un estado más avanzado que "ruta estimable", pero que ninguna columna de esos dos censos preguntaba.

---

## 4 · Granularidad — 15 pares vs. "30 parámetros" (declarado, no forzado)

`forense/perimetro-alcanzable-v1_0.md` §1.1 (líneas 9-28) ya derivó, por comando, de dónde sale "30": **4 `medidos` + 6 `derivados` + 13 `asignados_probabilidad` + 1 `evidencia_experimental_terceros` + 6 `asignados_coeficiente` = 30** — una suma a través de **cinco secciones distintas** de `procedencia.yaml`, cada una contada en su propia unidad nativa (`asignados_coeficiente` aporta **6** a esa suma, contando por generador, no por coeficiente). Verificado en este acto, por comando propio, que las 6 filas de `asignados_coeficiente.detalle` sí contienen 15 pares `gen.coef` en sus diccionarios `coefs` (`G1(2)+G2(2)+G3(3)+G4(4)+G5(3)+G6(1)=15`, ver §1 de este documento) — y que esos 15 son exactamente los mismos 15 `gen.coef` de `rutas_estimabilidad_coeficiente.detalle` (cruce por comando: `B - C = ∅`, `C - B = ∅`).

**Las dos cifras no son comparables como si fueran la misma unidad.** "12 de 30" (`ACTO MAESTRA31-E3`) cuenta alcanzabilidad a través de cinco secciones heterogéneas del archivo; "15 pares" (este acto) cuenta una sola sección con dos vistas (`B` y `C`) que ya coinciden exactamente entre sí. Este acto no re-deriva "12 de 30" ni propone una tabla de correspondencia entre ambas cifras — eso sería forzar una equivalencia que el propio `hallazgos.md:512` (26/ago, `ACTO MAESTRA31-E3`) ya identificó como un hallazgo de granularidad genuino, no un error a resolver aquí.

---

## Qué NO hace este documento

No estima ningún coeficiente nuevo — los β̂ citados en la tabla ya existían en `milpa/procedencia.yaml` antes de este acto, medidos el 4/ago/2026. No adjudica `FP-176` (si escribir un β̂ ya medido en la escala ya declarada requiere firma propia) — la cita en §1/§2 y la deja donde está. No escribe ningún coeficiente en `milpa/` — la única edición a `milpa/procedencia.yaml` que este acto hace es la línea `1127` (`reparto:`), fuera de este documento. No toca `canon/modelo-decision-v4_0.md`. No re-corre `cobertura-motor.md`, `censo-estimabilidad-coeficientes-v1_2.md` ni `perimetro-alcanzable-v1_0.md`, aunque §3-§4 de este documento muestren que los dos primeros están vencidos en alcance (nunca leyeron la sección A) — eso se declara, no se corrige aquí (sería el "décimo acto de índice de la jornada" que el propio encargo prohíbe). No compara "15 pares" contra "30 parámetros" como si fueran la misma unidad (§4).
