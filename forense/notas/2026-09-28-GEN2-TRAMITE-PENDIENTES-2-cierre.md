# Nota de cierre — ACTO GEN2-TRAMITE-PENDIENTES-2 — 28/sep/2026

Contador: cero mediciones; no adopta. `no_corrido_abiertas`: +10 por filas invisibles que vuelven a contar, −16 por cierres verificados por producto, +3 por NC propias (465 → 475 → 459 → 462). `celdas_validadas`, `adoptados` y `legacy` no se mueven.

## Arranque
- [EJECUTADO] ENTORNO-DERIVADO = NUBE (hook). Base `a8c3e341` (origin/main), SHA de redacción `11602de8`: main se movió y **NC-DECISIONES-1 ya fusionó** (PR #1213); universo re-derivado sobre su resultado (§6). 0-bis `3fc6684e`. Rama `claude/new-session-rd97rz`.
- Premisas que cayeron (logística): a `a8c3e341` las filas con `estado` vacío son 10 (6 de 12 campos + 4 de 11) y 2 de 10 campos, como dijo dirección; SUCESOR-YA-FUSIONADO era 51, no 67 (NC-DECISIONES-1 cerró filas en medio).
- Adjuntos (TABLERO y PENDIENTES): no llegaron; no archivados (NC-…-3fc6-01).

## P0
[EJECUTADO] `tools/nc_por_clase.py`: modo exacto se conserva; se añade modo frontera (`nombre-` como prefijo) que **no resuelve** si el prefijo es familia (el token siguiente difiere entre candidatos: `GEN2-TUBERIA`, `GEN2-LOTE`, `GEN2-ADQUISICION` citaban familias y se habrían contado como corridas — hallazgo de este acto, 8+ falsos positivos evitados). Estados de encargo: CONSUMIDO · ARCHIVADO-SIN-CONSUMIR · EN-COLA. `NC-0012` → «acto sucesor GEN2-E4 tiene nota de cierre». SUCESOR-YA-FUSIONADO: 51 → 91 (P0) → 96 (P0 + filas de P2).

## P2
12 filas recolocadas sin cambiar texto: 6 de 12 campos sin `que_no_se_corrio` (se inserta vacío en su sitio; `pieza`, `razon`, `impacto`, `sucesor`, `estado` corren una columna), 4 `fa47` (igual, 11→12), 2 `673c` (10→12, se añaden `cerrado_por`/`fecha_cierre` vacíos). `673c-02` se reparó porque NC-DECISIONES-1 ya estaba en main. Guardia: `tests/test_no_corrido_estructura.py` (FAIL campos/estado; WARN token; prueba de mutación), huérfano.

## P1
Universo: 96 SUCESOR-YA-FUSIONADO + 1 de §L (`NC-260923-ASTRA5-U3-POLITICA-COMPLETAR-d459-01`, CALC-ENCUP-PISOS-2012-0003 con fila) = 97. Cuatro lectores por lote (25/25/25/22), consolidado aquí. Dictámenes: CERRADA-POR-PRODUCTO 15 · SUCESOR-SIN-PRODUCTO 65 · NO-VERIFICABLE-AQUÍ 13 · SIN-OBJETO 4. Cerradas 16 (12 + 4); **3 retenidas** (NC-0085: `consulta.py result RES-0028` dice PENDIENTE; ef6f-01: pidió SI y salió N; 9641-03: falta la enmienda en 9a2c-01). Tabla: `forense/analisis/pendientes-2/vencidas-dictamen.tsv`.
Hallazgo: el censo de tests está rancio (NC-…-3fc6-03); varios sucesores nombrados no tienen encargo (RELEVO-CONSUMIDORES-4, ENUT-ENLACE-MARCADOR-1, CONTADORES-CONSUMO-3, ASTRA5-U5-ADQUISICION-2).

## P3
78 razones con token A.14 al inicio; prosa íntegra tras ` · `. 31 por grafía (sin acento) y 47 por juicio, de las cuales 10 que piden decisión de mesa van con `DIFERIDO-A` (no se convierten a DECISIÓN-DE-MESA-PENDIENTE, §4). Tabla: `razones-normalizadas.tsv`.

## Hoja de firmas
`forense/analisis/pendientes-2/hoja-firmas-2026-09-28.md` (18 letras de decisión + 1 de asignación de dueño) · fila `FP-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-01`.
