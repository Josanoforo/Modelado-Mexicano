ENCARGO · MAESTRA33-E8 · SCORE-M-1 — invoca /acto
SHA de redacción: d353d82. ENTORNO: NUBE — NO CAJA. COMPUERTA: PR de MAESTRA33-E6 (EMISOR-M-1) fusionado; si no, cero commits. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 1/sep/2026): "Ya tenemos las automatizaciones que queríamos crear? o sigue algo pendiente?" — cierra la última pieza.
A.8 (dirección contra d353d82): scoring-adv1-m3.py y procedimiento-scoring-v1_0.md EXISTEN, congelados para la era v1_0 (entrada.json de corredores; "0 de 15 emitibles"). Adaptador para marco-M: NO-ENCONTRADO (ls tools/ + prereg-duelo-v2/ → 0 score*). corridas-L: 120 archivos, 0 con ids del marco-M. Configuración sellada: FP-168 (IC 0.95, seed 42), M-ENLACE=A, M-AGREGA=a′ (ADR-220/225/226), corredor E ranura no activada, F-DD (ADR-237).
P1 · tools/score_marco_m.py: construye la entrada de scoring-adv1-m3.py (SIN editarlo) desde marco-M-sorteado-v1_1 + corridas-M/M-<id>.json + corridas-R/<id>.json + corridas-L/ (si existen); excluye del puntaje las celdas VERIFICACION-NO-PUNTUA (F-DD) y las lista aparte; declara por celda qué corredores tiene (M/R/L) y puntúa solo donde haya R más al menos uno de M o L.
P2 · Regresión: reproduce el resultado v1_0 (§6 del procedimiento) desde su misma entrada, byte a byte salvo fecha. No coincide → PARO.
P3 · Primera corrida sobre v1_1 + skill .claude/commands/score.md: scoreboard-v1_1.md con celdas puntuables hoy (probablemente 0 hasta que C3 entregue R — dicho así, no maquillado), y la frase "L pendiente: 11 celdas" mientras mesa no corra L.
PERÍMETRO: tools/score_marco_m.py, score.md, forense/prereg-duelo-v2/scoreboard-v1_1.md, forense/notas propia, tablero (recibo), archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: celdas puntuadas 0→N, declarado.
LO QUE NO HACE: no edita scoring-adv1-m3.py; no emite M, R ni L; no activa el corredor E; no cambia la Configuración sellada.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E8 · SCORE-M-1`, 1/sep/2026, `ADR-253`
(candidato). PR contra `main` (número asignado al abrir, ver más abajo en
esta misma sesión de cierre). Regresión P2 PASA byte a byte; primera
corrida real sobre `marco-M-sorteado-v1_1.tsv`: **4 de 11 celdas
puntuables** (`CIV-M-01/06/08/09`), no 0 como este encargo anticipaba —
terreno movido por `ACTO MAESTRA33-C3 · CODIFICA-R-1` (`PR #423`),
fusionado antes de que este acto arrancara. Detalle:
`forense/notas/2026-09-01-score-m-1-cierre.md`.
