ADR-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-01 — 22/sep/2026

ACTO GEN2-DIN-CREDITO-PISOS-1870-RUN-1 re-verifica en caja el piso de
crédito ENIF 2021 recortado a 18-70
(`CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001`) sin reejecutarlo.
Ya había corrido en `17d27f82` y su fila en la vista la revirtió
`344739d1`. `verify` da REPRODUCE/IDENTICO, 2 941/2 941 RESULT a delta
0.0. No hay run nuevo, no adopta, no hay fila en la vista: los derivados
no viajan en un PR, así que el registro pasa a mesa (`NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-01`). La vista
publicada de main va 18 corridas atrás (`NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-02`). El asiento E.7 lo trae
#1004 (`NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-03`); K2 queda fuera del lote (`NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-04`). Ver
`canon/gobernanza-v1_15.md` ADR-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-01 y
`forense/notas/2026-09-22-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-cierre.md`.
