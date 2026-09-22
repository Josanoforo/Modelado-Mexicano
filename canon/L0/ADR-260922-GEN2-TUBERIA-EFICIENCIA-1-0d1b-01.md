ADR-260922-GEN2-TUBERIA-EFICIENCIA-1-0d1b-01 — 22/sep/2026

ACTO GEN2-TUBERIA-EFICIENCIA-1 cierra las dos piezas del lote de eficiencia
de tubería que `GEN2-TUBERIA-CIERRE-RAPIDO-1` dejó `NO-CORRIDO`: P4
(derivados fuera de los PR — guarda en `enrutamiento-pr`, re-derivación en
`guardias` en push a `main`, `tools/derivados_protegidos.py`) y P5
(`celdas_d_adoptadas_activas` en `tools/tablero_programa.py`, 0→6,
incluida la celda-D del piloto 3). P1/P2/P3/P6 ya estaban resueltos por
actos anteriores — verificado, no reimplementado. P0: mesa respondió sin
`gh`, main no exige ramas al día. P7 queda para el sucesor `EFICIENCIA-2`
tras el merge. Ver `canon/gobernanza-v1_15.md` ADR-260922-GEN2-TUBERIA-EFICIENCIA-1-0d1b-01
y `forense/notas/2026-09-22-gen2-tuberia-eficiencia-1-cierre.md`.
