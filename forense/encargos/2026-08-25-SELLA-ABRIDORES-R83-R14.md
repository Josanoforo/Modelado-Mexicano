# Encargo · SELLA-ABRIDORES-R83-R14 — archivar los veredictos propuestos por #355 con firma de mesa · Hito D 18→20

*(Archivado verbatim por regla A.3. **Estado: `CONSUMIDO` (completo)** — RANURA 1 (`R8.3`) ejecutada al lanzar, `ADR-186`, 25/ago/2026; RANURA 2 (`R1.4`) llegó firmada en turno posterior el mismo día y se ejecutó como continuación del mismo acto, `ADR-187`. Ver `forense/notas/2026-08-25-sella-abridores-r83-r14-cierre.md` y su Adenda. El título hablaba de "18→20"; el resultado final, sumando las dos ranuras en dos turnos, **es exactamente 18→20** — el texto de abajo describe el estado al momento del primer lanzamiento, cuando solo `R8.3` traía firma; no se reescribe, por A.3.)*

SHA de redacción: `2b7d787` (main al redactar; verificado igual a `origin/main` al lanzar, sin avance). Dirección, 25/ago/2026. ENTORNO: NUBE (`cloud_default`). No UBUNTU, no doble. REQUERIDO al lanzar: las firmas de mesa de F0 como líneas propias — sin ellas, PARO sin tocar nada.

## Existencia (dirección, contra `2b7d787`)

Las dos propuestas EXISTÍAN y NO estaban archivadas: `forense/hitoD-R8_3-abridor-v1_0.md` §5 propone fila `A`; `forense/hitoD-R1_4-abridor-v1_0.md` propone `D` y declara una colisión de gobernanza (`ADR-55`/`ADR-56` vs. el perímetro del pack que la estableció). Registro de veredictos: `R8.3`/`R1.4` ausentes antes de este acto (por eso Hito D seguía 18).

## Perímetro

`forense/hitoD-preregistro-v2_0.md` — bloque `## Registro de veredictos archivados` (+1 entrada real, no +2: solo `R8.3` trajo firma) · `README.md:36` (18→19, desglose actualizado) · citas vivas de `canon/modelo-decision-v4_0.md` que el set de sincronía exige · gobernanza (`ADR-186` con el verbatim) · estado (L0 + línea Hito D) · tablero (`forense/firmas-pendientes.tsv`, fila `FP-155` nueva para la ranura firmada) · nota de cierre · este encargo, archivado.

## F0 · Compuertas — firmas como líneas propias, fuera de cita (candado `FP-63`)

**RANURA 1 (`R8.3`) — FIRMADA:**

> "FIRMO R8.3: se archiva el veredicto propuesto fila A por el abridor de #355, con sus reservas escritas (incluido el eje 3 en desacuerdo, que queda abierto y declarado)."

**RANURA 2 (`R1.4`) — SIN FIRMAR.** El primer turno del lanzamiento repitió dos veces la firma de `R8.3`; ningún turno posterior trajo una firma distinta para `R1.4`. No hubo `SÍ`/`NO` a la reescritura de la fila `C` de su escala, porque esa pregunta viaja dentro de la ranura que no se firmó.

**Ejecución de la compuerta:** ausente `R1.4` → se ejecuta solo `R8.3`. `A.8` en fresco: no se re-abre nada más allá de lo que la firma real cubre.

## F1 · Propagación (ejecutada)

`ADR-186` con el verbatim íntegro; la entrada al Registro con letra, fecha, acto de origen (#355) y reservas; set de sincronía completo (`README:36` → 19 de 27, citas vivas de `modelo-decision`, `estado` con nota fechada). `R1.4` sigue sin enmienda de su fila `C` — no hubo firma que la autorizara. `python3 tests/check.py --baseline` antes/después, sin `--freeze`: 19 FAIL · 128 WARN en ambos, línea base VERDE. **CONTADOR: este acto mueve Hito D +1** (`R8.3` → `A`), no +2.

## No hace

No relee las corridas ni re-estima nada. No toca `R10.1`. No adjudica el eje 3 de `R8.3` (queda reserva abierta). No toca `milpa/`, corpus, duelo ni pool. No archiva `R1.4` — sin firma, no hay compuerta que ejecutar sobre esa ranura.

---

## Adenda · 25/ago/2026 — RANURA 2 llega firmada; el encargo se cierra completo

*(Añadida al final, fechada, sin tocar el cuerpo de arriba — misma disciplina de A.3 que el resto de este archivo.)*

Mesa envió, en turno posterior, la firma que faltaba:

> "FIRMO R1.4: se archiva el veredicto propuesto D por el abridor de #355. La colisión con ADR-55/56 se resuelve así: la regla general aplica y el archivado es trámite del acto sucesor cuando el perímetro del acto que establece lo prohíbe — este acto es ese sucesor."
> "[SÍ a la reescritura de la fila C de su escala para que nombre el hueco real."

Ejecutado como continuación de este mismo acto (mismo SHA de redacción `2b7d787`, mismo entorno NUBE): `R1.4` → veredicto `D` archivado en `hitoD-preregistro`, `ADR-187` sella el verbatim y la resolución de la colisión, la fila `C` de la escala de `R1.4` recibe la enmienda fechada que el SÍ de mesa autorizó, `FP-156` nace `FIRMADA` en el tablero con `ejecutada_en` = este acto. Hito D: **19 de 27 → 20 de 27**. `python3 tests/check.py --baseline`: 19 FAIL · 128 WARN antes y después, línea base VERDE. Detalle completo: Adenda de `forense/notas/2026-08-25-sella-abridores-r83-r14-cierre.md`.

**CONTADOR total del encargo, sumando las dos ranuras: +2** (`R8.3` → `A`, `R1.4` → `D`). Título del encargo cumplido: 18→20.
