<!--
A.14 (ACTO GEN2-T8, 8/sep/2026, forense/encargos/2026-09-08-GEN2-T8-A14-CERO-RAMAS-RETROFIT.md,
cuarta entrada PARA-v2.13 en forense/hallazgos.md): "Lo que no se corrió se
asienta, o el acto no cierra." Todo PR que cierra un acto trae, verbatim,
la sección de abajo -- la misma que el encargo archivado (A.3) lleva antes
de `## CONSUMIDO`. "Ninguno." es una fila válida si de verdad no hay nada
sin correr, parcial, distinto o con reserva.
-->

## NO-CORRIDO / RESERVAS

<!--
Una fila por pieza no ejecutada, parcial, distinta de lo pedido, o con
reserva. Columnas: qué (pieza citada) · por qué · impacto · sucesor.

`por qué` es una de estas siete, verbatim (no se inventan otras):
  - PARO-ENTORNO
  - PARO-PREMISA
  - FUERA-DE-PERÍMETRO
  - SUSTITUIDO-POR:<acto>
  - DIFERIDO-A:<sucesor>
  - NO-VERIFICABLE-AQUÍ
  - DECISIÓN-DE-MESA-PENDIENTE

`impacto` = qué contador o consumidor no se mueve por esto.
`sucesor` = acto, fila FP, o SIN-ASIGNAR -- nunca vacío.

Un SUSTITUIDO-POR que no enumere qué absorbe el sustituto y qué queda
huérfano es una fuga de deuda: dilo explícitamente en la fila.

Ninguna fila aquí = escribe "Ninguno." -- no borres la sección.
-->

- Ninguno.

<!--
Cada fila de arriba se repite, literal, como fila `NC-NNNN` en
`forense/no-corrido.tsv` con `estado = ABIERTA` (o `CERRADA` si este mismo
PR la cierra). `tools/cierre_acto.py` (Fase A) y `tests/check.py::T34
T-NO-CORRIDO` verifican mecánicamente que esta sección exista antes de
`## CONSUMIDO` -- no la borres ni la dejes vacía.
-->

## Resumen

<!-- Qué hace este PR, en dos o tres líneas. -->

## Perímetro

<!-- Archivos tocados, del encargo archivado (A.3). -->

## Verificación

<!-- `python3 tests/check.py --baseline` -- pega la salida cruda. -->
