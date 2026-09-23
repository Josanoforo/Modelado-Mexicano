## ADR-260923-GEN2-DIN-CREDITO-CELDAS-D-2-f6a3-01

Nueve celdas-D de crédito 2024 (una por conducta) registradas desde
`CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002` (bloque `ADJ16`, 16
celdas del eje puntuadas), con `-ADJUDICACION-0001` citado como oro por
hash. Corrige el conteo de conductas del NC predecesor (`…e6b2-01`: 7 →
9, re-derivado por lector JSON). `champion_actual: PERSISTENCIA` en las
9 (nadie vence; `PROPUESTA-CON-RESERVA` en K1/K6-P-TENEDORES no adopta).
Marcador `RETROSPECTIVA-MECÁNICA` (origen móvil sin selección de
variante, no emisión prospectiva nueva).

`tools/celdas_validadas.py` (ajeno) no admite esta unidad (clase 1
CRUCE exige RESULT por celda, esta unidad emite por conducta agregada):
`celdas_validadas` 92 → 92, sin cambio, declarado en
`clase_1_celdas_d_sin_contar`. Pregunta a mesa si vale extender el
contador (TUBERÍA) queda en `NC-…-f6a3-02`. Cierra por `DECISIÓN-DADA`
los NC `…e6b2-01` y `…0af9-02`.

Detalle completo: `forense/notas/nota-2026-09-23-gen2-din-credito-celdas-d-2.md`.
Ver también `canon/gobernanza-v1_15.md` (entrada completa).
