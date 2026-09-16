ENCARGO · ACTO GEN2-FIRMAS-MESA-3 · DOS PUNTOS, F-17 Y F-18, LLEGADOS PEGADOS EN EL LANZAMIENTO DE ACTO GEN2-E1-DISENO-CALIBRACION-1

CABECERA · archivado verbatim por 0-bis A.3 dentro de la misma sesión que ejecuta `ACTO GEN2-E1-DISENO-CALIBRACION-1` (rama `claude/nube-acto-gen2-e1-design-yee31q`, base `origin/main = 9fd59d0`) · ENTORNO: NUBE — no abre microdato, no toca red · COMPUERTA: ninguna (este archivo ES el producto que otro acto cita como compuerta, no algo que dependa de una compuerta ajena) · El ejecutor propaga/archiva, no decide (mismo criterio SELLA-3 que GEN2-FIRMAS-MESA-1/2): si un punto no se puede ejecutar tal como está escrito, va a NO-CORRIDO con la razón, no se reinterpreta.

Los dos puntos llegaron uno tras otro, en el mismo canal, mientras esta sesión ejecutaba el `ARRANQUE`/`COMPUERTA` de `ACTO GEN2-E1-DISENO-CALIBRACION-1` (que cita `gated a F-18`). Se transcriben íntegros abajo, en el orden en que llegaron.

PUNTOS FIRMADOS (transcripción íntegra; no se resumen)

F-17 · NC-0226 renumerada — mesa, 16 de septiembre de 2026, verbatim:

"FIRMA DE MESA, mesa, 16 de septiembre de 2026 — OBJETO (F-17, NC-0226 renumerada): ningún eje del árbitro se declara equivalente a un corte del modelo por parecido de nombre. Se ratifica formalidad ≡ formalidad. Se autoriza verificar por definición, no por nombre, los dos únicos pares candidatos (dominio_urbano_rural ↔ urbanizacion, localidad ↔ urbanizacion) y traer el resultado a firma; edad espera FP-53; el resto queda SIN-CORRESPONDENCIA declarado. Con esto, el marcador por segmento tiene hoy un eje comparable, y se dice."

F-18 · Abrir el diseño de E1 → misma cabecera — mesa, 16 de septiembre de 2026, verbatim:

"FIRMA DE MESA, mesa, 16 de septiembre de 2026 — OBJETO (F-18, NC-0239): la ley E0 («el motor no calibra; E1+ espera el cierre de BARRIDO-2», milpa/src/theta.py y motor.py) queda VENCIDA EN ALCANCE: su universo era el programa sin dato propio y hoy hay 80 corridas GEN2 selladas. Se autoriza el DISEÑO de la calibración E1 de Θ(x) sobre resultados GEN2 sellados: nombre por nombre de procedencia.yaml, con escala, universo y argumento de identificación o su ausencia declarada (A-bis 1/2: co-observación no es identificación; condicionar tampoco es correcto). Ningún número hasta que la spec de identificación esté congelada; la corrida es acto de caja posterior. theta.py no se toca en el diseño."

VERIFICACIÓN DE EXISTENCIA (A.8, dirección)

F-18 cita `NC-0239`: `awk -F'\t' '$1=="NC-0239"' forense/no-corrido.tsv` → fila presente, `estado=ABIERTA`, sucesor citado verbatim: "acto de calibracion que haga theta cargable por celda (E1+), despues el crosswalk de ejes firmado, despues el marcador por segmento." F-18 es exactamente ese sucesor. `NC-0239` fue abierta por `ACTO GEN2-MARCADOR-C0-D` (`ADR-520`, 15/sep/2026): `theta.valor()` lanza `ThetaNoDisponible` en 43/43 entradas.

F-17 cita `NC-0226 renumerada`. Verificado: `awk -F'\t' '$1=="NC-0226"' forense/no-corrido.tsv` → fila **ya existe y ya está `CERRADA`**, con objeto **distinto**: "la HOJA DE FIRMAS 2 y el cierre de sus NC" / "propagar la hoja de firmas 2 en data/corrida0/decisiones.tsv y cerrar las NC que esa hoja resuelva" (cerrada por `ACTO de PR #792`). El contenido de F-17 (crosswalk eje-árbitro↔eje-modelo, `dominio_urbano_rural↔urbanizacion`, `localidad↔urbanizacion`) coincide en cambio, palabra por palabra, con `NC-0240` (abierta por `ADR-520` el mismo 15/sep/2026, columna `sucesor`: "firma de mesa sobre el crosswalk eje-arbitro <-> eje-modelo; en particular si `localidad` y `dominio_urbano_rural` son `urbanizacion`"). **`F-17` cita un número de NC que no corresponde a su propio objeto** — `NC-0226` está cerrada y es de otro asunto; el número que sí encaja es `NC-0240`, abierta y sin firma. Por A.4/A.13 (no se resuelve una discrepancia de numeración por inferencia ni por "el más parecido"), este acto NO reescribe `NC-0226` ni reabre su fila, y NO cierra `NC-0240` en nombre de F-17: la firma se archiva verbatim (arriba, íntegra) y la discrepancia se declara en `## NO-CORRIDO / RESERVAS`. Mesa decide si `F-17` decía `NC-0240` y hubo un lapsus de dedo, o si de verdad hay un objeto distinto que amerita reabrir `NC-0226` con una razón nueva.

PIEZAS

P1 · F-17 (crosswalk de ejes): registro verbatim de la firma; NO se propaga a ningún archivo de trabajo (`milpa/tramite-ola5-propuesta-v0.yaml`, `NC-0240`, `NC-0226`) por la discrepancia de numeración de arriba — ver `## NO-CORRIDO / RESERVAS`. Fuera del perímetro de `ACTO GEN2-E1-DISENO-CALIBRACION-1`, que es el acto que produjo esta hoja: la calibración de Θ(x) y el crosswalk de ejes son dos piezas independientes del mismo sucesor de `NC-0239`, con dueños de acto distintos.

P2 · F-18 (abrir el diseño de E1): es la compuerta verificada de `ACTO GEN2-E1-DISENO-CALIBRACION-1` — este mismo commit es el producto contra el que ese acto verifica `gated a F-18` (`git show HEAD:forense/encargos/2026-09-16-GEN2-FIRMAS-MESA-3.md`). El diseño mismo se ejecuta y se archiva en el 0-bis A.3 propio de ese acto, no aquí.

PERÍMETRO Y CONCURRENCIA: este archivo únicamente; no toca `milpa/`, `data/`, `canon/`, `forense/no-corrido.tsv` ni `forense/firmas-pendientes.tsv` — la propagación de F-17 (una vez resuelta la numeración) y el cierre eventual de `NC-0239`/`NC-0240` son trabajo de sus actos sucesores, no de esta hoja.

CONTADOR: cero mediciones propias, cero adopciones. Ambos puntos quedan registrados; solo F-18 se ejecuta, por el acto que la cita como compuerta. CIERRE: cascada + ## NO-CORRIDO / RESERVAS + ## CONSUMIDO.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| **F-17 · NC-0226 renumerada** — verificar por definición los dos pares candidatos (`dominio_urbano_rural↔urbanizacion`, `localidad↔urbanizacion`) y traer el resultado a firma | `DECISIÓN-DE-MESA-PENDIENTE`, registrada como `NC-0254` | El número de NC que F-17 cita (`NC-0226`) está `CERRADA` y es de otro objeto (propagación de la Hoja de Firmas 2); el objeto real de F-17 coincide con `NC-0240` (abierta, crosswalk de ejes), que sigue sin firma resuelta por este acto. El marcador por segmento (`NC-0239`/`NC-0240`) no gana su crosswalk hoy | mesa aclara si F-17 quería decir `NC-0240`, o si `NC-0226` se reabre con objeto propio; después, acto que ejecute la verificación por definición de los dos pares |
| **F-17** — verificación por definición en sí (comparar `milpa/tramite-ola5-propuesta-v0.yaml` ejes contra `milpa/src/celdas.py::CORTES_C1` para los dos pares candidatos) | `FUERA-DE-PERÍMETRO` | No es objeto de `ACTO GEN2-E1-DISENO-CALIBRACION-1` (calibración de Θ, no vocabulario de ejes); mezclar los dos perímetros en un solo acto viola A.10 | acto propio de crosswalk, una vez resuelta la numeración de la fila de arriba |

## CONSUMIDO

Pendiente — se añade en el commit de cierre de `ACTO GEN2-E1-DISENO-CALIBRACION-1`, que es el acto que consume `F-18` de esta hoja.
