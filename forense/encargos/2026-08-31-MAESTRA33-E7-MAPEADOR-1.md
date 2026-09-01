ENCARGO · MAESTRA33-E7 · MAPEADOR-1 — invoca /acto · ESTADO: LISTO-NUBE
SHA de redacción: a6d8504. ENTORNO: NUBE — NO CAJA. COMPUERTA: ninguna. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 31/ago/2026): "Dame las siguientes automatizaciones".
A.8 (dirección contra a6d8504): data/inventario-reactivos-v1_1.tsv y -ext EXISTEN (capa de texto). Búsqueda genérica: NO-ENCONTRADO (ls tools/ → etiqueta_v1_2, censo_r34_bc, barrido_enoe_*; ninguno genérico ni reutilizable por celda).
P1 · tools/busca_reactivos.py: consulta por palabras o regex sobre texto del reactivo + nombre de variable, filtros encuesta/ola/tipo; salida TSV: id, encuesta, ola, tabla, variable, texto, tipo, en_corpus (cruce con manifiesto); declara filas examinadas (A.13).
P2 · .claude/commands/mapea.md: dada la definición de una celda o θ, corre ≥3 formulaciones, devuelve tabla de candidatas con vocabulario A.4 por candidata (EXISTE-SATISFACE / EXISTE-NO-SATISFACE con qué falta / NO-ENCONTRADO con términos) y una recomendación que DIRECCIÓN revisa. Propone, no decide.
P3 · Primera corrida: las 5 celdas (CIV-08, DIN-11, SFT-04, SFT-06, TIC-06) y las 3 θ (DIN-07, TIC-01, EMP-05) de FP-190, con sus definiciones verbatim de la fila → forense/notas/…-mapeo-fp190.md.
PERÍMETRO: tools/busca_reactivos.py, mapea.md, forense/notas propia, tablero (recibo), archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: cero (insumo de dirección), declarado.
LO QUE NO HACE: no escribe reglas ni specs; no abre microdato; no toca milpa/ ni el marco.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E7 · MAPEADOR-1`, 31/ago-1/sep/2026, entorno
**NUBE** (`cloud_default`), rama `claude/mapeador-fp190-automatizaciones-2b1e30`,
**`PR #420`** (https://github.com/Josanoforo/Modelado-Mexicano/pull/420).
Commits: `6e34e9b` (0-bis A.3, este archivo) · `b7300bc` (`P1`,
`tools/busca_reactivos.py`) · `257e350` (`P2`, `.claude/commands/mapea.md`) ·
`4339623` (`P3`, `forense/notas/2026-09-01-mapeo-fp190.md`) · `3245e21`
(cascada: `ADR-247` candidato, `canon/gobernanza-v1_15.md` y
`canon/estado-programa-v1_10.md` recifrados 246→247,
`canon/registro-rotulos.tsv` censado, `forense/firmas-pendientes.tsv`
`FP-212` nueva).

`COMPUERTA: ninguna` — declarada por el encargo, sin línea `GATED a X`, sin
gate que verificar. SHA de redacción `a6d8504` = tip literal de
`origin/main` verificado al arrancar (`git fetch origin main`) y de nuevo
al cerrar (sin PR nuevo fusionado en el intervalo) — sin drift que
re-derivar.

`P1`/`P2`/`P3` ejecutados tal como el encargo los describe. Resultado de
`P3` (propuesta, no sellada): `EXISTE-SATISFACE` en `SFT-04`/`TIC-01`
θ/`EMP-05` θ; `EXISTE-NO-SATISFACE` en `CIV-08`/`TIC-06`/`DIN-07` θ;
`NO-ENCONTRADO` en `DIN-11`/`SFT-06` — ver
`forense/notas/2026-09-01-mapeo-fp190.md` para el detalle por candidata y
la recomendación de cada una. DIRECCIÓN decide.

`python3 tests/check.py --baseline`: **VERDE**, `19 FAIL · 158 WARN`, sin
entrada nueva frente a `tests/baseline.json`. Perímetro respetado: no se
abrió microdato, no se tocó `milpa/` ni el marco congelado ni
`procedencia.yaml`/`tramite.yaml`, no se escribió ninguna regla ni spec.
PR abierto contra `main`, **no fusionado por este acto** — el merge es de
mesa.
