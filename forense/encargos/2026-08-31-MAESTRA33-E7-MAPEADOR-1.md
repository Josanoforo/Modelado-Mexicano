ENCARGO · MAESTRA33-E7 · MAPEADOR-1 — invoca /acto · ESTADO: LISTO-NUBE
SHA de redacción: a6d8504. ENTORNO: NUBE — NO CAJA. COMPUERTA: ninguna. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 31/ago/2026): "Dame las siguientes automatizaciones".
A.8 (dirección contra a6d8504): data/inventario-reactivos-v1_1.tsv y -ext EXISTEN (capa de texto). Búsqueda genérica: NO-ENCONTRADO (ls tools/ → etiqueta_v1_2, censo_r34_bc, barrido_enoe_*; ninguno genérico ni reutilizable por celda).
P1 · tools/busca_reactivos.py: consulta por palabras o regex sobre texto del reactivo + nombre de variable, filtros encuesta/ola/tipo; salida TSV: id, encuesta, ola, tabla, variable, texto, tipo, en_corpus (cruce con manifiesto); declara filas examinadas (A.13).
P2 · .claude/commands/mapea.md: dada la definición de una celda o θ, corre ≥3 formulaciones, devuelve tabla de candidatas con vocabulario A.4 por candidata (EXISTE-SATISFACE / EXISTE-NO-SATISFACE con qué falta / NO-ENCONTRADO con términos) y una recomendación que DIRECCIÓN revisa. Propone, no decide.
P3 · Primera corrida: las 5 celdas (CIV-08, DIN-11, SFT-04, SFT-06, TIC-06) y las 3 θ (DIN-07, TIC-01, EMP-05) de FP-190, con sus definiciones verbatim de la fila → forense/notas/…-mapeo-fp190.md.
PERÍMETRO: tools/busca_reactivos.py, mapea.md, forense/notas propia, tablero (recibo), archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: cero (insumo de dirección), declarado.
LO QUE NO HACE: no escribe reglas ni specs; no abre microdato; no toca milpa/ ni el marco.
