ENCARGO · MAESTRA33-C2 · ARBITRO-R-1 — invoca /acto
SHA de redacción: 8b6aa85. ENTORNO: CAJA (máquina de mesa, data/raw montado; firma A.2 de tres partes) — NO NUBE, NO doble. COMPUERTA: ninguna de merge. MODELO SUGERIDO: Opus (medidor de dos commits).
FIRMA DE MESA (verbatim, 31/ago/2026): "Dame las siguientes automatizaciones".
A.8 (dirección contra 8b6aa85): corridas-R/ EXISTE (23 archivos, era v1_0, esquema JSON reutilizable). Herramienta genérica de árbitro: NO-ENCONTRADO (tools/ + prereg-duelo-v2/: corredor-B, corredor-E, scoring — ninguno calcula R por celda). marco-M-congelado-v1_1.tsv: 27 filas con encuesta/ola/universo/variable/estimador/ponderador/escala por celda — spec congelada, sin ejecutor.
P1 · tools/arbitra.py: lee el marco (congelado v1_1; el sorteado cuando exista); por celda elegible SIN corridas-R/<id>.json: localiza el payload en data/manifiesto.yaml por encuesta/ola (ausente → NO-OBTENIDO + fila en data/cola-adquisicion-v1_0.tsv para /adquiere, sin inventar); aplica el estimador declarado sobre universo y ponderador declarados; escribe corridas-R/<id>.json con el esquema de los existentes (léelo de un archivo, no de memoria) + n, IC95 seed 42 (FP-168), sha256 del payload, escala declarada.
P2 · .claude/commands/arbitra.md: lote ≤4 celdas por corrida (D-11); COMMIT-1 congela las specs del lote copiadas verbatim del marco + frase de sello; COMMIT-2 resultados; si una spec estaba mal, COMMIT-3 lo dice, nunca hacia atrás. CIEGO: jamás abre corridas-M/ ni milpa/tramite.yaml; lista los archivos abiertos al cierre.
P3 · Regresión ANTES de producir nada nuevo: recalcula 3 celdas que ya tienen R en corridas-R con este mecanismo y diff contra lo existente. Coincide → herramienta aceptada. No coincide → PARO-reporta las cifras y el comando; no ajusta.
PERÍMETRO: tools/arbitra.py, arbitra.md, corridas-R/ (solo archivos nuevos), data/cola-adquisicion-v1_0.tsv (filas nuevas), forense/notas propia, tablero (recibo), archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: puntos R nuevos 0→N — declara N; si este acto solo alcanza la regresión, 0 y dicho.
LO QUE NO HACE: no sortea; no emite M; no compara M contra R (scoring es otro acto); no toca el marco.
SUCESORES: caminatas /arbitra sobre las celdas de B″ (entran a la cola como ENTORNO: CAJA).

## CONSUMIDO

Commits `26fdfd5` (0-bis A.3), `411e3fa` (P1/P2, P3 PARO) y el commit de
cascada de este mismo acto, en la rama `acto/maestra33-c2-arbitro-r-1`
`PR #417`. `ADR-245` (renumerado de 244: `PR #416`/`ACTO MAESTRA33-E4 · DELTA-E3` fusionó primero y tomó el 244). Veredicto: **PARO en P3**
(regresión no coincide) — `tools/arbitra.py` y `.claude/commands/arbitra.md`
entregados; 0 puntos R nuevos, declarado. Detalle:
`forense/notas/2026-08-31-arbitro-r-1-paro-regresion.md`.
