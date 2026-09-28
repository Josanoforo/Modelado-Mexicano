# R28 · 130 COINCIDE no ciegas del lote 2 (ENBIARE 126, ENCIG 4) · expediente

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2 · `FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-04` · 28/sep/2026.

## Firma de mesa, verbatim

`forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R28 **(1)**: «Las 130 COINCIDE de ENBIARE/ENCIG del lote 2 quedan CONCUERDA-NO-APROBADA con rótulo NO-CIEGA-PENDIENTE; se re-comparan en el lote 3 con el adaptador v3 congelado antes de revelar.»

## Universo, derivado por comando

`p2_tablas.py` → `r28-130-no-ciegas.tsv`, desde `catalogo-1-ejecucion-lote2/lote2-tabla-estimadores.tsv`, filas ENBIARE/ENCIG con `estado_punto = COINCIDE`: **ENBIARE 126 · ENCIG 4 = 130**. El comando PARA si el conteo es otro.

| Grupo | Asiento vigente en `validaciones-independientes.tsv` | Qué hace R28 |
|---|---|---|
| ENBIARE 126 | CONCUERDA-NO-APROBADA (lote 2) | Rótulo `NO-CIEGA-PENDIENTE` hasta la re-comparación ciega. Son las 180 − 54 del paquete `enbiare-pisos-bienestar-0001`, así que se re-comparan dentro de P1. |
| ENCIG 4 | **PASA** de otra validación (alcance `PUNTO;…;INFERENCIA-NO-COMPROBADA`) | La comparación del lote 2 queda rotulada `NO-CIEGA`. El PASA vigente viene de otra validación y **no se toca**: degradarlo movería un contador que esta firma no mueve. |

## Re-comparación

- **ENBIARE 126:** dentro de P1, paquete ENBIARE, con la regla de comparación fijada y commiteada antes de revelar (el mismo orden E.2 de C1-LOTE-3). Al cierre de P2, P1 no ha lanzado.
- **ENCIG 4:** el lote 3 no tiene paquete ENCIG ni acceso C1 firmado a ENCIG. Su re-comparación queda para `GEN2-ASTRA6-C1-LOTE-4`, con NC propia.

## Rótulo en el libro

El libro `validaciones-independientes.tsv` admite una sola fila por `(spec_id, resultado_id)`: su lector (`tools/corrida0.py::_aplica_validaciones_independientes`) hace PARO con una duplicada. El rótulo `NO-CIEGA-PENDIENTE` de las 126 se asienta al cerrar P1, en la misma fila que registra la re-comparación, no en una fila aparte.
