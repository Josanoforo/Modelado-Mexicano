# HITO D, R7.2 — "delito sin seguro → no denuncia": falsación pre-registrada, veredicto D

*4 de agosto de 2026. Sesión-tipo Ubuntu microdato (ENVIPE). Mueve el contador de Hito D — el OTRO contador congelado, distinto al de condicionales (`8 de 14`, no tocado aquí).*

⚠️ **CONTAMINACIÓN DE MICRODATO, declarada para esta sesión.** Abre microdato de ENVIPE 2025, tabla `TMod_Vic` — ya abierta por la sesión que produjo `PR #57` (`forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md`, rama `sesion/cal-conf-faseb-pos4-exposicion-violencia`), fusionada a `main` en `f08c01d`/`6a09a37`. Esta sesión reutiliza esa apertura — no es la primera en tocar la tabla — y queda contaminada para pre-registrar cualquier acto posterior contra ella que no esté ya escrito.

**Procedencia.** Tipo (1) para todo lo verificado en esta sesión contra archivo, en `origin/main` `6a09a37` (`git fetch`/worktree nuevo desde ahí; `a05650f`, el commit que el encargo cita como verificado por "maestra #17", es ancestro directo — `git merge-base --is-ancestor a05650f HEAD` confirma, y `git diff a05650f HEAD -- forense/hitoD-preregistro-v2_0.md canon/estado-programa-v1_9.md` no da salida). Tipo (3) hasta contrastarlas: la premisa del encargo sobre el contenido de la ficha R7.2 (líneas 178-188) — verificada, se sostiene literal (§0).

---

## 0 · Verificación de premisas del encargo

1. **Ficha R7.2, citada literal contra archivo.** `forense/hitoD-preregistro-v2_0.md:178-188` coincide carácter por carácter con lo que el encargo cita: SI-ENTONCES, "la mejor construida del perímetro", falsador, umbral (brecha <20pp pareando gravedad e identificabilidad), reserva de cifra negra, escala A-D propia de la ficha. **Se sostiene.**
2. **Contador de Hito D: 2 de 27, `R1.1`→`D`, `R3.2`→`B`.** Verificado contra `canon/estado-programa-v1_9.md:93` y contra el bloque append-only de `hitoD-preregistro-v2_0.md` (líneas 693-694 antes de esta sesión) — coinciden. **Se sostiene.**
3. **Contador de condicionales: 8 de 14.** Verificado contra `canon/modelo-decision-v4_0.md:275,619` — vigente tras `CAL-CONF` Fase B pos. 5-6 (`forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md`). **No se toca**: este acto no mide ninguna de las 14 condicionales declaradas.
4. **`TMod_Vic` — universo y ponderador, heredados de `PR #57`, re-verificados aquí, no copiados a ciegas.** 40 280 filas, `RESUL_H='A'` en el 100%, ponderador `FAC_DEL`. Re-verificado en esta sesión:
   ```
   $ python3 tests/manifiesto.py --verifica | grep envipe2025_csv
   envipe2025_csv [data_raw]: COINCIDE -- sha256 y tamaño (17600019 bytes) verificados contra data/manifiesto.yaml
   ```
   Mismo hash que reportó `PR #57` — mismo archivo en disco, sin alteración entre sesiones (riesgo real: dos incidentes previos de `data/raw` compartido sobreescrito entre sesiones concurrentes, `forense/hallazgos.md` 2026-08-03; no ocurrió aquí, verificado por coincidencia exacta de hash).

---

## 1 · Las tres variables — verificadas por descriptor literal, no por parecido de nombre

*(Lección `CAAS`/`CEU` del 3/ago, `forense/hallazgos.md:62` — verificar el descriptor antes de asumir qué mide una variable por su nombre corto.)*

| Concepto que pide la ficha | Variable(s) | Descriptor literal (diccionario de datos) | Tabla |
|---|---|---|---|
| Tipo de delito | `BPCOD` | *"Códigos para delitos"* | `TMod_Vic` |
| Cobertura de seguro | `BP2_1` | *"Vehículo robado asegurado"* — no "cobertura de seguro" en general | `TMod_Vic` |
| Identificabilidad del agresor | `BP1_12_1`…`BP1_12_5` | *"Delincuentes desconocidos"* / *"conocidos de vista solamente"* / *"de poco trato"* / *"cercanos"* / *"familiar(es)"* | `TMod_Vic` |
| (robustez, no primaria) | `BP1_13` | *"Reconocimiento de los (las) delincuentes"* | `TMod_Vic` |

Ninguna se asumió por nombre: `BP2_1` no es "seguro contra el delito" en general — es, literal y exclusivamente, si el vehículo robado estaba asegurado. Verificado además contra el cuestionario (`cuest_modulo_envipe2025.pdf`): la pregunta 2.1 vive en *"SECCIÓN II. ROBO TOTAL DE VEHÍCULO (Código 01)"*, y tras responderla el módulo **termina** ("TERMINE MÓDULO").

**Elección de `BP1_12` sobre `BP1_13` como proxy de identificabilidad, declarada:** el mecanismo de la regla es miedo a represalia de un agresor **identificable**, lo que exige saber **quién es** (relación previa: desconocido/conocido de vista/poco trato/cercano/familiar), no solo poder reconocer una cara desconocida si se la volviera a ver (`BP1_13`). `BP1_13` se reporta como robustez.

---

## 2 · Hallazgo estructural: `BP2_1` es degenerada fuera de `BPCOD=01` — verificado contra el microdato, no solo contra el texto del cuestionario

```
n válido de BP2_1, por BPCOD (Counter sobre las 40 280 filas):
  01 (robo total de vehículo): 1 028
  02..15 (las 14 clases restantes): 0

Total BP2_1 válido = 1 028 == n(BPCOD='01') = 1 028. Exacto.
```

**1 028 de 40 280 filas (2.6%) tienen `BP2_1` observable, y el 100% de ellas son `BPCOD=01`.** No es no-respuesta: es un blanco estructural — el instrumento no formula la pregunta para ninguna otra clase de delito. La instrucción de salto del cuestionario ya lo anticipaba textualmente (*"SI EL CÓDIGO DEL DELITO ES 02, 03, 10, 11, 14 o 15 TERMINE EL MÓDULO"*, antes de llegar a la Sección II), pero esta sesión no se conformó con el texto: lo verificó contra el dato, siguiendo la misma disciplina que `PR #57 §0.2` aplicó al universo de `BP1_20`/`BP1_23`/`BP1_28`.

**Segunda capa, verificada en el mismo acto: la identificabilidad (`BP1_12`) tampoco es universal.** Su `n` válido por `BPCOD` va de 0 (07 fraude bancario, 08 fraude al consumidor — el cuestionario salta directo a la pregunta de denuncia sin pasar por la descripción del delincuente) a 100% (05 asalto en calle/transporte, 11-14 delitos de contacto violento — el cuestionario asume "Sí" en "¿estuvo presente?"/"¿pudo observar?"), pasando por fracciones minoritarias (3-25%) en las clases de robo sin contacto — incluida la que aquí importa, `BPCOD=01` (24.8% válido, n=255 de 1 028).

---

## 3 · Por qué el veredicto es **D**

La condición C de la propia ficha —*"ENVIPE desagregada por delito × cobertura × identificabilidad"*— exige que la **cobertura varíe entre clases de delito**, tal como el propio falsador lo redacta en plural (*"una clase de delito sin cobertura... o una con cobertura..."*). Eso no existe: `BPCOD` varía (15 clases), pero cobertura de seguro solo está definida, como concepto medido, para una de ellas. No hay una categoría "delitos sin cobertura de seguro" poblada por el instrumento fuera de `BPCOD≠01` — construirla habría sido fabricar el cruce que la fuente no da, exactamente lo que el encargo instruye no hacer.

**Veredicto: `D`** — *"si ENVIPE no cruza cobertura de seguro con tipo de delito"*, aplicado literal. Es un `D` por diseño de instrumento (ENVIPE solo formula "¿estaba asegurado?" donde el seguro contra ese delito es, en México, un producto real y extendido — el automotriz), no por hueco de dato accidental ni de mercado — mismo tipo de hallazgo que `hitoD-R1.1` documentó ("hueco de mercado, no de dato"), aquí trasladado al diseño del instrumento.

---

## 4 · Hallazgo adyacente, declarado y no adjudicado — no cambia el veredicto

Dentro de `BPCOD=01`, la comparación que la fuente sí da (denuncia por cobertura, ponderada `FAC_DEL`, IC95% por conglomerado último `UPM_DIS`/`EST_DIS`):

| `BP2_1` | n | % denunció | SE | IC95% |
|---|---|---|---|---|
| Asegurado | 402 | 79.1% | 2.15pp | [74.9%, 83.3%] |
| No asegurado | 614 | 67.2% | 1.77pp | [63.7%, 70.7%] |

Brecha de 11.9pp, dirección predicha por el "vuelco" que la ficha cita como lo que la hace falsable (*"SI es robo de vehículo asegurado ENTONCES sí denuncia"*). **No prueba el falsador tal como está redactado** (compara clases de delito, no subgrupos de una sola). Confundidor declarado, no descartado: identificabilidad dentro de esta submuestra (n=121/124, pequeña) es 1.5% vs. 5.1% — ambos bajos, no pareados con precisión por tamaño de muestra insuficiente para condicionar tres vías dentro de una sola clase.

**Conexión ya viva en `milpa/procedencia.yaml`, señalada, no editada (fuera de perímetro):** `civico.denuncia.con_seguro` (línea 448) trae `[0.78, 0.22]` `ASIGNADO`, nota propia *"ENVIPE no publica esta condicional en esa forma"* — el 79.1% medido aquí queda a 1.1pp de ese asignado. `civico.denuncia.sin_seguro` (líneas 346,361) usa la cifra negra (0.93) como `no_denuncia`, con su propia reserva ya escrita señalando la misma confusión que esta ficha previene. Ninguno de los dos ids se edita aquí — anomalía de "dos ids, una regla" ya conocida (`forense/hallazgos.md:42`), decisión de mesa si amerita acto aparte.

Tabla completa de las 15 clases de delito (denuncia y % conocido, contexto declarado, no prueba del falsador) y el detalle completo del veredicto: `forense/hitoD-R7_2-veredicto-v1_0.md`.

---

## 5 · Estimador validado contra caso conocido, antes de calcular nada nuevo

Reutilizado `tests/svystat.py` sin modificar (caso sintético SRS, coincide a 9 decimales). Antes de tabular `BPCOD`/`BP2_1`/`BP1_12` (que ninguna sesión anterior había tocado), esta sesión reprodujo con su propio pipeline la tabla marginal de `DOMINIO` de `BP1_20` que `PR #57 §3.1` ya publicó sobre la misma tabla:

```
Complemento urbano: n=8 039  p=9.2%  SE=0.55pp
Rural:               n=3 770  p=8.9%  SE=0.76pp
Urbano:              n=28 471 p=9.0%  SE=0.31pp
```

Coincide número por número. Valida lectura de CSV, ponderador y estimador contra un resultado ya publicado y a su vez validado, antes de aplicar el mismo pipeline a variables nuevas.

---

## 6 · El contador

**Hito D: 2 de 27 → 3 de 27.** `R7.2` → veredicto `D`, archivado en el bloque append-only de `hitoD-preregistro-v2_0.md`, narrado en su Nota 11, detalle en `hitoD-R7_2-veredicto-v1_0.md`. Propagado a `canon/estado-programa-v1_9.md` (§L5, §7, y el conteo derivado de reglas del motor sin corrida: 47→46 de 49, 25→24 de 27).

**Condicionales medidas sobre atributos: sigue en 8 de 14, sin cambio.** Este acto no midió ninguna de las 14 condicionales declaradas en `canon/modelo-decision-v4_0.md §1.1.F` — no hay nada que mover ahí.

**Corrección de staleness encontrada al tocar `canon/estado-programa-v1_9.md §7`, no buscada:** la línea *"Siguiente en el orden"* seguía listando `R3.2` como pendiente pese a estar archivada desde el 29/jul — nunca se retiró de esa lista al cerrarse. Corregida de paso, con nota explícita en el propio archivo (no se investiga aquí la causa raíz).

**No se toca `milpa/procedencia.yaml` ni `canon/modelo-decision-v4_0.md`** — señalados en §4, no editados, fuera del perímetro de un acto de Hito D. **No se toca ENIGH** — otra sesión Ubuntu corre P3 sobre ese instrumento. **No se mide `exposicion_violencia`** — ese parámetro sigue sin reactivo verificado y es otro encargo (`forense/hallazgos.md`, entrada 2026-08-04, `PR #57`).

---

## 7 · Límite de lectura declarado

Leídos completos en esta sesión: `forense/hitoD-preregistro-v2_0.md` (líneas 1-30, 160-206, 670-694 y el cuerpo completo de Notas 5-10 para el molde), `forense/hitoD-R3_2-veredicto-v1_0.md` completo (molde de estructura), `canon/estado-programa-v1_9.md` (líneas 1-15, 90-125, 180-217), `canon/modelo-decision-v4_0.md` (líneas 680-695, el rótulo de `R7.2`), `milpa/procedencia.yaml` (líneas 340-370, 440-460), `forense/hallazgos.md` (entradas 2026-07-31 y 2026-08-04 citadas), `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md` completa, `instrucciones-proyecto-v2.md` (Bloque A), `fd_envipe2025.pdf` (índice de tablas, sección `TMod_Vic` completa), `cuest_modulo_envipe2025.pdf` completo (preguntas 1.1-2.1 y las instrucciones de salto), diccionario de datos de `TMod_Vic` completo (543 filas), catálogos de `BPCOD`/`BP2_1`/`BP1_12_1..5`/`BP1_13`. Se corrió `tests/manifiesto.py --verifica` y `python3 tests/check.py` (19 FAIL · 84 WARN, sin cambio neto frente a la corrida previa a esta sesión — ninguna de las dos cifras se movió por este acto). No se editó `milpa/procedencia.yaml`, `canon/modelo-decision-v4_0.md`, `data/manifiesto.yaml` ni ningún artefacto de ENIGH — todos se leyeron cuando aplicaba, ninguno se tocó.
