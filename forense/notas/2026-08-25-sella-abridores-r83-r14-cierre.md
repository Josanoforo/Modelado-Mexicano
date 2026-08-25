# Nota de cierre · `ACTO SELLA-ABRIDORES-R83-R14`, 25/ago/2026

**Encargo:** `forense/encargos/2026-08-25-SELLA-ABRIDORES-R83-R14.md`. **SHA de redacción declarado:** `2b7d787` — verificado igual a `origin/main` al lanzar (merge de `PR #356`). **Entorno:** NUBE.

## Qué pedía el lanzamiento

Archivar en `hitoD-preregistro` los dos veredictos que `ACTO PACK-UBUNTU-2` propuso sin archivar (`ADR-181` para `R8.3` → fila `A`; `ADR-182` para `R1.4` → fila `D`), condicionado a que el lanzamiento trajera las firmas de mesa de F0 como líneas propias, fuera de cita, por el candado `FP-63`. Ausente cualquiera de las dos ranuras → se ejecuta solo la firmada; ausentes las dos → PARO sin tocar nada.

## Qué llegó firmado

Solo **RANURA 1** (`R8.3`) trajo firma de mesa verbatim:

> "FIRMO R8.3: se archiva el veredicto propuesto fila A por el abridor de #355, con sus reservas escritas (incluido el eje 3 en desacuerdo, que queda abierto y declarado)."

**RANURA 2** (`R1.4`) llegó sin firma — el primer envío del usuario repitió la misma línea de `R8.3` dos veces, y el segundo turno no trajo ninguna firma de `R1.4`. Por regla de la propia compuerta, se ejecuta solo la firmada. `R1.4` **no se toca**: sigue como propuesta de `ADR-182`, con la colisión de gobernanza (`ADR-55`/`ADR-56` vs. perímetro del pack que la estableció) sin resolver, para mesa.

## Qué se ejecutó

1. **`forense/hitoD-preregistro-v2_0.md`** — línea nueva en el bloque append-only `## Registro de veredictos archivados`: `R8.3` → veredicto `A`, con el verbatim de la firma y la reserva del eje 3 (ISSP multipaís, `d = +16.62 pp`, apunta al revés) declarada **abierta**, tal como la propia firma la nombra — esta firma no la adjudica.
2. **`README.md:36`** — 18 de 27 → **19 de 27**, desglose `10D·2B·3A·2E·1C` → `10D·2B·4A·2E·1C`.
3. **`canon/gobernanza-v1_15.md`** — `ADR-186` nuevo, sella la firma con el verbatim íntegro, ejecuta la propuesta de `ADR-181`, declara `R1.4` sin firmar; cabecera del documento y las tres citas vivas del Hito D (§4, tabla de deuda) re-derivadas a 19/27 y 186 ADR. Cascada: candidateó contra el máximo re-derivado (`185`, sin huecos) → `186`.
4. **`canon/estado-programa-v1_10.md`** — L0 (185→186 ADR, nota nueva), L5 (18→19 de 27, línea `R8.3`→`A` añadida a la lista, correction chain cerrada, aviso de "dos propuestas esperando firma" reescrito a solo `R1.4`), líneas 204 y 280 (contadores de "sin corrida" y "Paso 2" re-derivados: 31→30 de 49, 9→8 de 27 sin corrida).
5. **`canon/modelo-decision-v4_0.md`** — las tres citas vivas del set de sincronía (§0.1 banner de estado, §7, tabla del changelog v4.0) re-derivadas a 19/27 con `R8.3`→`A` añadido.
6. **`forense/firmas-pendientes.tsv`** — fila nueva `FP-155` (la ranura de esta firma), nacida `FIRMADA` con el verbatim, `ejecutada_en` = este acto.

## Qué NO se tocó

`R1.4`, la fila `C` de su escala (no hubo `SÍ`/`NO` a la reescritura porque la ranura entera llegó sin firmar), `milpa/`, corpus, duelo, pool, `data/raw` (ausente, no se usó), ninguna corrida ni re-estimación, el eje 3 de `R8.3` (queda reserva abierta, no adjudicada).

## Verificación

`python3 tests/check.py --baseline` antes y después de los cambios: **19 FAIL · 128 WARN** en ambos casos, línea base VERDE, sin `--freeze`. `T18`/`T20` (Hito D, cascada marcada) pasan limpio tras la propagación completa; `T15` (conteo de ADR) y `T16` (autoverificación FAIL/WARN) también, una vez sincronizados los conteos de ADR y de Hito D en los cinco sitios que los citan.

**CONTADOR: +1** — única corrida que este acto mueve (`R8.3` → `A`). `R1.4` sigue en 0.

---

## Adenda · 25/ago/2026 — RANURA 2 (`R1.4`) llega firmada; continuación del mismo acto

*(Añadida al final, fechada, sin tocar el cuerpo de arriba — misma disciplina que las notas de otros actos de este programa.)*

Mesa envió, en turno posterior, la firma que faltaba:

> "FIRMO R1.4: se archiva el veredicto propuesto D por el abridor de #355. La colisión con ADR-55/56 se resuelve así: la regla general aplica y el archivado es trámite del acto sucesor cuando el perímetro del acto que establece lo prohíbe — este acto es ese sucesor."

seguida de:

> "[SÍ a la reescritura de la fila C de su escala para que nombre el hueco real."

**Cómo se leyó la resolución de la colisión.** `ADR-182` había declarado que, bajo `ADR-55`/`ADR-56`, un veredicto `D` lo archiva el acto que lo establece — pero el perímetro de `ACTO PACK-UBUNTU-2` (el acto que estableció la propuesta) lo prohibía expresamente, así que no se archivó ahí. La firma de mesa no crea una excepción: fija que la regla general sigue gobernando, y que cuando el establecedor tiene el perímetro cerrado, el trámite pasa al **acto sucesor** que sí trae el perímetro abierto. Este acto (`ACTO SELLA-ABRIDORES-R83-R14`) es ese sucesor.

### Qué se ejecutó, además de lo ya narrado arriba

1. **`forense/hitoD-preregistro-v2_0.md`** — línea nueva en el Registro: `R1.4` → veredicto `D`, con el verbatim y la razón medida (Umbral no construible: 0 columnas de marca/sustituto en 425 archivos `.dta`, contra 1274 columnas de control positivo). **Enmienda fechada de la fila `C`** en la propia ficha de `R1.4` (§3.1): texto viejo *"exigiría panel D/E de consumo popular — hueco declarado"* → nuevo *"identificación de marca y el par de sustitutos funcionales dentro del acto de compra — hueco real"*, con el SÍ de mesa citado inline.
2. **`README.md:36`** — 19 de 27 → **20 de 27**, desglose `10D·2B·4A·2E·1C` → `11D·2B·4A·2E·1C`.
3. **`canon/gobernanza-v1_15.md`** — `ADR-187` nuevo, sella la firma con el verbatim íntegro, ejecuta la propuesta de `ADR-182` y documenta la resolución de la colisión; cabecera (187 ADR) y las dos citas vivas del Hito D re-derivadas a 20/27. Cascada: candidateó contra el máximo re-derivado (`186`, sin huecos) → `187`.
4. **`canon/estado-programa-v1_10.md`** — L0 (186→187 ADR, nota nueva), L5 (19→20 de 27, línea `R1.4`→`D` añadida, aviso de "propuesta esperando firma" reescrito: ya no queda ninguna pendiente), líneas 204 y 280 re-derivadas (30→29 de 49, 8→7 de 27 sin corrida).
5. **`canon/modelo-decision-v4_0.md`** — las tres citas vivas re-derivadas a 20/27 con `R1.4`→`D` añadido.
6. **`forense/firmas-pendientes.tsv`** — fila nueva `FP-156` (la ranura de esta firma), nacida `FIRMADA` con el verbatim, `ejecutada_en` = este acto.

### Verificación

`python3 tests/check.py --baseline` antes y después: **19 FAIL · 128 WARN** en ambos, línea base VERDE, sin `--freeze`. `T15`/`T16`/`T18`/`T20` limpios tras la segunda propagación.

**CONTADOR: +1 adicional** (`R1.4` → `D`) — Hito D queda en **20 de 27**, cerrando por completo el encargo `SELLA-ABRIDORES-R83-R14` (las dos ranuras, en dos turnos).
