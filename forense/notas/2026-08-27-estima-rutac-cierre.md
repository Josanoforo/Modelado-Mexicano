# Nota de cierre · ACTO MAESTRA31-E9 · ESTIMA-RUTAC — el acto pivota: la premisa era falsa por partida doble

Fecha: 2026-08-27. Worktree `/home/pc0/mm-maestra31-e9-estima-rutac`, rama `acto/maestra31-e9-estima-rutac`. Esta nota sustituye al COMMIT-2/cierre que el encargo original preveía (estimar dos asociaciones nuevas). Por decisión de dirección, ya tomada y con autorización explícita y acotada (ver abajo), **no se corre COMMIT-2**: correr una tercera estimación sobre el mismo par θ/desenlace no añadiría nada a lo que `forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md` ya midió el 4/ago/2026 — exactamente el patrón que `COMMIT-1` de este mismo acto (`forense/notas/2026-08-27-estima-rutac-spec.md §0`) ya había recomendado no repetir. En vez de correr una medición redundante, este acto cierra como **hallazgo**: dos verificaciones adicionales, hechas por dirección y un agente previo tras `COMMIT-1`, encontraron que la VERIFICACIÓN DE EXISTENCIA del propio encargo (`forense/encargos/2026-08-27-MAESTRA31-E9-ESTIMA-RUTAC.md`, líneas 25-53) tenía dos premisas falsas, no solo la que `COMMIT-1` ya había detectado.

---

## Los cuatro hallazgos

### Hallazgo 1 — el β̂ ya existe (ya detectado por COMMIT-1, re-confirmado aquí)

El encargo afirma, verbatim (línea 37): *"Resultado A.4: NO-ENCONTRADO — ningún artefacto del árbol estima estos dos coeficientes."* Esto es falso. `milpa/procedencia.yaml`, sección `coeficientes_generador_medidos:` (línea 884), tiene dos entradas ya medidas:

- `G4_exposicion_violencia` (línea 994): `clase: "MEDIDO·β̂(diferencia de proporciones), condicional(ejes), universo=disparadores AP7_3 no denunciantes"`. `beta_hat` (línea 1001): marginal **+16.614pp [IC95% 13.995,19.234]**, más condicionamiento por edad (4 celdas), dominio (3), ESTRATO (4) y formalidad (4 de 5, sin_pago SIN SOPORTE) — **0 de 15 celdas con soporte invierten signo**.
- `G4_confianza_institucional_justicia` (línea 1025): mismo patrón, 7 ítems `AP5_4_01/02/03/05/06/07/11`, cada uno con β̂ marginal e IC (línea 1032), condicionamiento por edad y dominio (49 celdas).

Ambas usan como desenlace `BP1_23` (`TMod_Vic`), universo restringido a disparadores de `AP7_3` no denunciantes (`n=13023`), y están fundamentadas en `forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md`, un acto que ya siguió la regla de dos commits del Bloque D y que ya cita la adjudicación de mesa, verbatim (§1 de esa nota): *"(i) `BP1_23` se habilita como desenlace de estas dos estimaciones únicamente, con universo declarado 'entre disparadores de `AP7_3`' y disciplina A-bis 4 completa"* — designada `MESA-E1` en esa nota. Es decir: la adjudicación de mesa que el encargo describe como *"pendiente adjudicación de mesa"* (nota de la fila RUTA-C, `procedencia.yaml:1119` antes de este acto) ya se había dado, el **4/ago/2026**, veintitrés días antes de que se redactara este encargo.

La misma sección `rutas_estimabilidad_coeficiente.detalle` es internamente inconsistente sobre este punto: clasifica `G1.confianza_institucional`, `G1.radio_confianza` y `G3.familismo_apoyo` como `RUTA-A` con la nota *"β̂ marginal ya corrido, Encargo W — no re-abre ruta, ver ADR-57(a)"* — la tabla sí tiene una categoría para "ya medido, no se re-mide". Los dos renglones de G4 cumplían el mismo criterio (β̂ marginal ya corrido, con nombre de acto y fecha) pero quedaban en `RUTA-C` con nota *"pendiente adjudicación de mesa"*, sin que nada en el archivo explicara la diferencia de trato entre un renglón y otro con el mismo hecho detrás.

**Por qué la nota quedó sin refrescar — verificado, no solo inferido.** `forense/escalas-eleccion-ciega-v1_0.md` §"Propagación" (línea 52) declara explícitamente el perímetro del Paso 2 (25/ago, ver Hallazgo 2 abajo): *"cada resultado se escribe en `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.detalle`, campo `escala_derivada` de esa fila (única, sin tocar `escala_asignado`/`escala_fuente`/`nota`/`ruta`/`prioridad`)"*. Es decir: el acto que sí llegó a tocar estas filas el 25/ago tenía prohibido, por su propio diseño, tocar `ruta:`/`nota:`. La nota de G4 quedó vieja no por descuido de ese acto — quedó vieja porque ningún acto posterior al 4/ago tuvo en su perímetro actualizar esos dos campos específicos, hasta este.

### Hallazgo 2 — la escala también ya está resuelta (no detectado por COMMIT-1; encontrado después, por dirección y un agente previo)

El OBJETO del encargo (líneas 61-68) construye su hipótesis central citando, verbatim, el campo `escala_derivada` de las dos filas G4:

> `escala_derivada: SUBDETERMINADA (ACTO ESCALAS-COMPLETAS-P1, 25/ago/2026)`

Esta cita es un fragmento truncado. El campo real, completo, antes de este acto (`procedencia.yaml:1119`, y su gemelo en `:1120`), decía:

> `"SUBDETERMINADA (Paso 1, ACTO ESCALAS-COMPLETAS-P1, 25/ago/2026) -- extremo theta DECLARADO (...); extremo del generador (salida de G4) NO declarado, canon/modelo-decision-v4_0.md §2.1-2.2 (líneas 422-460)... Sin el segundo extremo no hay forma funcional que forzar -- forma pendiente de Paso 2. -- Paso 2 (este acto, 25/ago/2026, forense/escalas-eleccion-ciega-v1_0.md §4): ELEGIDA-CIEGA -- proporción ponderada [0,1], enlace identidad, criterio 3 (convención sellada, ancla = θ pareja ya fijada: milpa/procedencia.yaml:condicionales_escalares_exposicion_violencia.exposicion_violencia (ENVIPE 2025))."`

Confirmado contra `forense/escalas-eleccion-ciega-v1_0.md` (Paso 2 de `FP-149`/`ADR-173`, firmado por mesa el 25/ago, procedimiento mecánico aplicado a las 15 filas por igual, §4, tabla, filas `G4.exposicion_violencia` y `G4.confianza_institucional`, líneas 41-42 de ese archivo): para las 7 filas con θ ya en mano (incluidas ambas de G4), el criterio 3 ancla forma = proporción ponderada `[0,1]`, enlace = identidad. Es decir: forma funcional + función de enlace + rango del parámetro **ya están declarados y propagados** a `procedencia.yaml`, sellados el 25/ago — **dos días antes** de que se redactara este encargo (27/ago) y **de que se committeara `COMMIT-1`** de este mismo acto.

`COMMIT-1` (`forense/notas/2026-08-27-estima-rutac-spec.md §6`) también citó solo el fragmento truncado — leyó `escala_derivada` como un solo token (`SUBDETERMINADA`) y construyó §6 entero ("Ningún ADR de D-ABC ha sellado función de enlace entre las dos escalas a la fecha de este commit") sobre esa lectura parcial, sin abrir el string completo del campo. Ver "Nota correctiva sobre §6" abajo.

### Hallazgo 3 (menor) — cita interna desfasada

La nota original de las dos filas RUTA-C citaba `procedencia.yaml:396-413 (limite_c2)`. Verificado: la clave `limite_c2:` vive hoy en la línea **471** (span 471-489, 19 líneas), no en 396-413. Lo que sí vive en 396-413 es contenido real de `exposicion_violencia` (final de `antes`, `fuente`, `n_util`, arranque de `eje_condicionante`) — correcto en su propio lugar, pero no es `limite_c2`. Antes de este acto, la cita se repetía 4 veces en el archivo (líneas 996, 1021, 1056 y 1119 — la última era la nota RUTA-C que este acto reemplaza); después del commit de reclasificación de este acto quedan 3 (996, 1021, 1056), porque la cuarta ocurrencia vivía precisamente en el texto que se reemplazó. La cita desactualizada no se corrige en las 3 ocurrencias restantes — fuera del perímetro acotado de este acto (autorización explícita solo para `ruta:`/`nota:` de las dos filas G4 de `rutas_estimabilidad_coeficiente.detalle`).

### Hallazgo 4 (menor) — `FP-152` con columna final stale

`forense/firmas-pendientes.tsv`, fila `FP-152` (Paso 2 de `ESCALAS-COMPLETAS`), tiene en su última columna (`encargo`, que en esta fila lleva una nota libre en vez de ruta de archivo): *"ACTO ESCALAS-COMPLETAS-P1, 25/ago/2026 (Paso 1 completo, ver FP-149). Paso 2 sigue sin ejecutar."* Esto es stale: Paso 2 sí se ejecutó el mismo 25/ago/2026 (ver Hallazgo 2, `forense/escalas-eleccion-ciega-v1_0.md`, 15 filas resueltas: 7 `ELEGIDA-CIEGA` + 8 `SUBDETERMINADA-PERSISTENTE`, propagado a `procedencia.yaml`). Se documenta como observación, **no se corrige**: `FP-152` (y `FP-149`) están fuera del perímetro autorizado de este acto (la autorización de dirección fue explícita: "NO edites FP-149 ni FP-152 — documenta esto como observación en el nuevo hallazgo, no lo corrijas ahí").

---

## Corrección al reparto de `rutas_estimabilidad_coeficiente.detalle` (observación, no editada)

La línea `reparto:` (`procedencia.yaml:1127`) sigue diciendo `"RUTA-A=3 · RUTA-I=1 · RUTA-C=2 · SIN-RUTA=9 -- suma 15"` después del commit de reclasificación de este acto. Con las dos filas de G4 reclasificadas a `RUTA-A`, el reparto real es `RUTA-A=5 · RUTA-I=1 · RUTA-C=0 · SIN-RUTA=9`. La autorización de dirección para este acto fue estrictamente acotada a los campos `ruta:`/`nota:` de las dos filas G4 ("NO toques ninguna otra fila ni ninguna otra sección de `milpa/procedencia.yaml`") y la línea `reparto:` es una sección distinta, fuera de esos dos renglones — así que queda intocada, y esta nota deja registrada la inconsistencia resultante para que un acto sucesor (o mesa) decida si refrescarla.

---

## A.13 — conteos y comandos de cada afirmación

| # | Afirmación | Tipo | Comando | Resultado |
|---|---|---|---|---|
| 1 | El array `coeficientes_generador_medidos` tiene entradas para G4 | positiva (refuta A.4 del encargo) | `command grep -n "^coeficientes_generador_medidos:\|^  G4_" milpa/procedencia.yaml` | `884:coeficientes_generador_medidos:`, `994:  G4_exposicion_violencia:`, `1025:  G4_confianza_institucional_justicia:` — 2 entradas, ambas examinadas línea a línea (994-1023 y 1025-1058, 65 líneas) |
| 2 | `rutas_estimabilidad_coeficiente.detalle` tiene exactamente 15 filas, de las cuales 2 eran RUTA-C (antes del commit) | positiva/negativa | `command grep -n "^    - {gen:" milpa/procedencia.yaml` acotado al rango 1112-1126 (`sed -n '1112,1126p'`) | 15 filas (1112-1126); `command grep -c "ruta: RUTA-C"` (pre-commit) → 2; post-commit → 0 |
| 3 | `escala_derivada` de las dos filas G4 contenía más texto que "SUBDETERMINADA (...)" | positiva | `sed -n '1119,1120p' milpa/procedencia.yaml \| wc -c` antes del commit; lectura completa del campo (no truncada por línea) | cada campo `escala_derivada` medía >1400 caracteres, con el fragmento "Paso 2 (...): ELEGIDA-CIEGA..." presente en ambas — verificado por lectura íntegra del string, no por grep de subcadena (un grep de "SUBDETERMINADA" sin `-o` habría dado falso positivo de "campo = SUBDETERMINADA a secas") |
| 4 | `forense/escalas-eleccion-ciega-v1_0.md` declara explícitamente que Paso 2 no toca `ruta`/`nota` | positiva | lectura íntegra del archivo (52 líneas, `wc -l`) — sección "Propagación", línea 52 | cita verbatim confirmada: "sin tocar `escala_asignado`/`escala_fuente`/`nota`/`ruta`/`prioridad`" |
| 5 | La cita `procedencia.yaml:396-413 (limite_c2)` no corresponde a donde vive `limite_c2:` hoy | negativa (la cita no señala lo que dice señalar) | `command grep -n "limite_c2" milpa/procedencia.yaml` (52 líneas de contexto revisadas: 460-490) | `limite_c2:` vive en la línea 471 (span 471-489, 19 líneas); la cita señalaba 396-413 (18 líneas), rango que contiene el final de `antes`/`fuente`/`n_util`/arranque de `eje_condicionante`, no `limite_c2` |
| 6 | La cita `procedencia.yaml:396-413` se repetía 4 veces antes del commit de este acto | positiva | `command grep -c "procedencia.yaml:396-413" milpa/procedencia.yaml` (pre-commit, sobre 1187 líneas totales del archivo) | 4 ocurrencias (líneas 996, 1021, 1056, 1119); post-commit → 3 (996, 1021, 1056) |
| 7 | `FP-152` columna final dice "Paso 2 sigue sin ejecutar" | positiva | `command grep -n "^FP-152" forense/firmas-pendientes.tsv` (1 de 173 líneas del archivo, 172 filas de datos + cabecera, la fila exacta) | confirmado verbatim en la última columna de esa fila |
| 8 | El β̂ medido el 4/ago usa `BP1_23` como desenlace, universo n=13023 | positiva (contexto de Hallazgo 1) | lectura íntegra de `forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md` (§1, §4-§7, §13) — 91,182 filas de `TPer_Vic2` universo poblacional NO es el universo de esta medición | universo restringido confirmado, n=13023 (`procedencia.yaml:997`), no 91,182 |
| 9 | No existe ningún ADR previo que adjudique el paso de escribir el β̂ ya medido en la escala ya declarada | negativa | `command grep -n "ADR-" forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md forense/escalas-eleccion-ciega-v1_0.md` — ningún ADR en ninguno de los dos documentos adjudica explícitamente "escribir el β̂ de `coeficientes_generador_medidos` en el campo `escala_derivada`/valor final del coeficiente G4" | ningún hit que adjudique ese paso específico (ver "Pendiente para mesa" abajo) |

Todo comando corrido con `command grep`/`sed`/`wc` contra los archivos reales del worktree (`/home/pc0/mm-maestra31-e9-estima-rutac`), nunca contra el espejo, con la salida a la vista arriba.

---

## Nota correctiva sobre `forense/notas/2026-08-27-estima-rutac-spec.md §6` (COMMIT-1)

`COMMIT-1` de este acto ya está committeado (`dc1d57f`) y, por la regla de dos commits del Bloque D, **no se reescribe**. Se declara aquí el error, no se edita el archivo original.

`§6` de `COMMIT-1` afirma: *"Ningún ADR de D-ABC ha sellado función de enlace entre las dos escalas a la fecha de este commit"* y construye la escala del procedimiento (diferencia de proporciones, [-100pp,+100pp]) explícitamente como algo que "no es la escala del coeficiente G4... Ningún ADR de D-ABC ha sellado función de enlace". Esa frase es correcta respecto de la escala DEL β̂ MARGINAL que `COMMIT-1` estaba a punto de producir (diferencia de proporciones del desenlace, que en efecto no tiene función de enlace sellada contra 0.70/−0.40) — pero es **engañosa** respecto del estado de las dos filas G4 de `rutas_estimabilidad_coeficiente.detalle`, cuyo campo `escala_derivada` sí tenía, desde el 25/ago (dos días antes), forma funcional (proporción ponderada [0,1]) y función de enlace (identidad) declaradas para la θ misma (no para el β̂ marginal del generador). `COMMIT-1` leyó el campo `escala_derivada` como si dijera solo "SUBDETERMINADA" (la primera palabra del string), sin abrir el resto del campo — el mismo tipo de error de lectura truncada que produjo el Hallazgo 2. La distinción que falta en `COMMIT-1 §6`: la escala de la θ (ya `ELEGIDA-CIEGA`, 25/ago) y la escala del β̂/coeficiente del GENERADOR (nunca declarada, sigue sin función de enlace) son dos cosas distintas — el error fue tratarlas como si el campo hablara solo de la segunda cuando en realidad documenta el estado de la primera.

---

## El veredicto del PASO 3 del encargo original, actualizado

El encargo pedía (PASOS/3): *"Con la escala declarada delante, di si el coeficiente se puede o no se puede escribir en `milpa/` — y por qué. Si la respuesta es que no, nombra exactamente qué le falta a `modelo-decision-v4_0.md` para que se pudiera: forma funcional, función de enlace, rango del parámetro, o las tres."*

**Actualizado:** para la **θ** de ambos coeficientes G4 (no para el β̂/salida del generador), las tres piezas que el encargo preguntaba si faltaban — forma funcional, función de enlace, rango del parámetro — **ya están declaradas**, desde el 25/ago/2026, por `ACTO ESCALAS-COMPLETAS-P1` Paso 2 (`forense/escalas-eleccion-ciega-v1_0.md §4`, criterio 3: proporción ponderada `[0,1]`, enlace identidad). No falta nada de lo que el encargo original preguntaba a nivel de escala de la θ.

Lo que **sigue sin adjudicar** — y este acto lo declara como pendiente, no lo decide — es un paso distinto y más específico: **¿escribir el β̂ ya medido el 4/ago en la escala ya declarada el 25/ago es, por sí mismo, un paso que requiere una adjudicación de mesa aparte?** Hay razón para pensar que probablemente sí (A-bis 3 del propio encargo prohíbe comparar el β̂ en escala de diferencia de proporciones contra el 0.70/−0.40 ASIGNADO como si fueran la misma magnitud — escribir un número final en `milpa/` exigiría resolver esa comparación, no solo declarar la escala de la θ), y ningún ADR revisado (`ADR-173`, el que sella `FP-149`/Paso 1+2+3 de `ESCALAS-COMPLETAS`; ni el par de notas del 4/ago y 25/ago) adjudica explícitamente ESE paso final — escribir el β̂ del generador (no solo declarar la escala de su θ) en `milpa/`. Este acto NO lo decide: lo declara pendiente, en `FP-176` (abajo).

---

## `FP-176`

Ver fila nueva en `forense/firmas-pendientes.tsv`. Resumen: este acto encontró que la premisa de su propio encargo era falsa por partida doble (A.4 "NO-ENCONTRADO" falso desde el 4/ago — el β̂ ya estaba medido; "SUBDETERMINADA" falso desde el 25/ago — la escala de la θ ya estaba declarada, cita truncada), corrigió las dos filas `RUTA-C`→`RUTA-A` de G4 en `milpa/procedencia.yaml` (solo campos `ruta:`/`nota:`), y deja abierta ante mesa la pregunta de si escribir el β̂ ya medido en la escala ya declarada requiere una adjudicación propia.

---

## Qué NO hizo este acto

No corrió `COMMIT-2` (ninguna estimación nueva — decisión de dirección, autorizada explícitamente, documentada arriba). No creó `data/estima-rutac-v1_0.tsv` (no hay estimación nueva que reportar en ese formato; el β̂ ya vive en `milpa/procedencia.yaml`, no se duplica). No tocó ningún otro campo de las dos filas G4 (`escala_asignado`, `escala_fuente`, `escala_derivada`, `prioridad` quedan iguales). No tocó ninguna otra fila ni sección de `milpa/procedencia.yaml` (incluida la línea `reparto:`, ahora stale — ver observación arriba). No editó `FP-149` ni `FP-152` (observación en Hallazgo 4, sin corrección). No adjudicó si escribir el β̂ en `milpa/` requiere firma de mesa aparte — lo declaró pendiente en `FP-176`. No tocó `canon/modelo-decision-v4_0.md`, `data/inventario-*`, `data/manifiesto.yaml`, `tools/**`, `forense/hitoD-preregistro-v2_0.md`, `forense/prereg-duelo-v2/**`.
