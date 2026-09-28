# Nota de cierre · ACTO GEN2-TRAMITE-HOJA-FIRMAS-21-1 · 28/sep/2026 · NUBE

ADR-260928-GEN2-TRAMITE-HOJA-FIRMAS-21-1-9739-01 (raíz `9739`, 0-bis `9739fbde`). Base `65da69fd` (origin/main al arrancar); el encargo se redactó sobre `643a8198`, que es ancestro: re-derivé todo.

## Contadores
Cero mediciones. No firma, no asienta, no adopta. No cambia el estado de ninguna FP ni NC ajena.

## Premisas
- [EJECUTADO → cayó, logística] «56 FP ABIERTA»: hoy son **65** (lector CSV sobre `forense/firmas-pendientes.tsv`). La diferencia son las filas nuevas de los actos de continuidad C1 (26a2-01..05), C2 (ba6c-01) y C3 (26bb-01..03), y de PENDIENTES-2 (3fc6-01). Los tres actos de continuidad ya están en main, así que entran como renglones y no como «espera».
- [LEÍDO → se sostiene] las cinco olas no traen campo de reserva: 21 ids del manifiesto (ENCRIGE 2020 5, ENVE 2024 5, CSES M5 3, ENDUTIH 2025 2, ENIF 2024 6), 0 con `estado_reserva`.
- [EJECUTADO] HOLDOUT: `milpa/catalogo-momentos-v0_1.tsv` trae M09–M23 como HOLDOUT (15); M23 ya consumido. El expediente C2 (`forense/analisis/familias-2027*`, 181 archivos) no cita ningún M09–M23 ni «HOLDOUT» (0 coincidencias). Por eso la opción «gastar solo los que ninguna familia 2027 use» hoy equivale a gastarlos todos, y la hoja lo dice.
- [REPORTADO → cayó, logística] el adjunto `HOJA-FIRMAS-21-v2-opciones-2026-09-27.md` no llegó (en uploads hay 2 archivos: el encargo y la ADENDA-1; no está en el repo). Las 30 letras y sus opciones se tomaron de `forense/analisis/nc-decisiones/hoja-2026-09-27.md`, que las contiene verbatim. NC `…-9739-01`.
- [LEÍDO] RECIBO-ASTRA6-3 «decisiones sin fila»: tres de #1241 ya tienen fila (26a2-01, 26a2-02, 26a2-03 de C1) y se fundieron ahí; las 9 PROP-C3 de #1243 se fundieron en 26bb-01 (inventario de 107 reglas).

## Hallazgos A.17 (van en la hoja, no se editó ninguna fila)
- Ocho FP firmadas o cerradas el 27/sep por la ADENDA-1 de RECIBO-ASTRA6-2 siguen ABIERTA en el TSV: ee49-01, ee49-02, 13c5-01, 13c5-02, 9df0-01, 71cf-01, 157c-03 y 157c-04 (esta última cerrada por producto). Van como YA-CUBIERTA-POR / SUPERADA.
- La hoja C2 dice que 71cf-01 «NO está firmada». Lo dice porque lee solo el TSV; la firma está en la ADENDA-1 de RECIBO-ASTRA6-2.

## Lo hecho
`forense/analisis/hoja-firmas-21/`: `arma_hoja.py` (fuente única) → `decisiones-21.tsv` y `hoja-para-mesa-firmas-21.md`. 85 renglones anclados a un objeto cada uno:

| tipo | pide firma | cubierta o firmada | total |
|---|---|---|---|
| APERTURA-DE-DATO | 16 | 3 | 19 |
| ADOPCION-VETO | 14 | 5 | 19 |
| CONTRATO-PROCEDIMIENTO | 15 | 20 | 35 |
| ACCION-CON-IDENTIDAD | 5 | 1 | 6 |
| FORMA | 6 | 0 | 6 |
| total | 56 | 29 | 85 |

Los 56 que piden firma incluyen los 6 del frente. Las 22 letras de la ADENDA-1 van como `FIRMADA-EN-CHAT` en 21 renglones (B2 y B3 se funden con c3fa-05: una decisión, un renglón). Qué acto asienta cada una va en su texto (A.12).
Fusiones por objeto: E1 + 43d6-01 + registros con identidad · F2 + H3 + 3d56-01 (respaldo) · B2 + B3 + c3fa-05 (alianza) · 4296-01 + 8914-03 (publicación) · I1 + solicitud (g).
Las 19 letras de PENDIENTES-2 van en un renglón por NC, con opciones PROPUESTO-POR-EJECUTOR: el acto de origen dejó preguntas sin opciones.

## Criterio de «hecho» (`python3 forense/analisis/hoja-firmas-21/arma_hoja.py --verifica`)
```
FP ABIERTA: 65 · ids sin renglón: 0 []
renglones: 85 · duplicados por objeto: 0
renglones con <2 opciones o sin texto: 0 []
decisiones P2 al frente: 6 (HOLDOUT + 5 olas) · estado de reserva por id coincide con la hoja: True
hoja existe: True
```
`python3 tests/check.py --rapido`: 0 FAIL (tres T25 de rótulos M09/E2 citados se censaron en `_T25_ARCHIVOS_CONOCIDOS`). La suite completa la juzga el CI.

## Actualización tras fusionar origin/main (28/sep)
Main trajo `FP-260928-GEN2-TRAMITE-INSTRUCCIONES-V217-1-3e59-01` (pegar v2.17 y plantilla v2.2 en el proyecto). Entra como renglón ACCION-CON-IDENTIDAD. Ahora: FP ABIERTA 66, ids sin renglón 0, 86 renglones (57 piden firma, 29 cubiertos), duplicados por objeto 0 (`arma_hoja.py --verifica`).
