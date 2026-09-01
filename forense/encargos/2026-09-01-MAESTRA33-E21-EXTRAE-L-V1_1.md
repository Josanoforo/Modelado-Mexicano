ENCARGO · MAESTRA33-E21 · L-EXTRAE-v1_1 — invoca /acto
SHA de redacción: 39e832d (merge PR #443). ENTORNO: NUBE. COMPUERTA: ninguna. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 2/sep/2026): "Revisa los últimos Pr's y re-presentame los encargos" — habilita cerrar la mitad L del duelo con las capturas ya fusionadas (#442).
A.8 (dirección contra 39e832d): 176 capturas en corridas-L/*-M-*.json con valor_extraido = null en 176 (verificado por comando); extractor del piloto EXISTE (CIV-08 trae 61.0 — localiza el código en pipeline-L-adv1-m2.py o tools/, no lo reescribas de memoria); extractor para marco-M: NO-ENCONTRADO (PAQUETE-L §:180 lo deja "para un extractor aparte, congelado antes de aplicarse"); agregado_v1_1.py EXISTE y corre.
P1 · COMMIT-1, ANTES de aplicar: regla de extracción congelada — el formato real de texto_crudo se inspecciona en ≤5 capturas elegidas por índice fijo (1ª de cada variante de las dos primeras celdas + 1), NO por contenido; regla: sección "Estimación" → primer número en la escala declarada del marco ([0,1] o %; si %, /100), rangos → punto medio, "no sé"/sin número → NO-EXTRAIBLE; sin mirar R, M ni el scoreboard. Frase de sello.
P2 · COMMIT-2: tools/extrae_l_v1_1.py aplica la regla a las 176; salida L-extraido-v1_1.tsv (id_celda, variante, indice, valor, estado, fragmento citado) — las capturas NO se editan; conteo de NO-EXTRAIBLE por variante (A.13). Regresión: la misma regla sobre las capturas del piloto CIV-08 reproduce su valor_extraido o declara por qué no.
P3 · Re-corre agregado_v1_1.py con L cargado → scoreboard-v1_1-AGREGADO-b.md: universo pareado L-vs-M real, proporción en banda y mediana |z| para L-solo y L+corpus, y las dos líneas de la pregunta doble con IC. Actualiza FP-221 (criterio L∩M) con el conteo real.
PERÍMETRO: tools/extrae_l_v1_1.py, L-extraido-v1_1.tsv, scoreboard-v1_1-AGREGADO-b.md, agregado-v1_1b-resultado.json, notas, tablero (FP-221 + recibo), A.3, cascada. Frase exacta vigente. CONTADOR: celdas pareadas L-vs-M 0→N, declarado.
LO QUE NO HACE: no llama a ningún modelo; no re-corre L; no edita capturas ni el procedimiento sellado; no cambia M ni R.

## CONSUMIDO

Ejecutado por `/acto` en la rama `claude/extrae-l-v1-1-scoreboard-a159hn`,
`PR #446` (Josanoforo/Modelado-Mexicano), abierto contra `main` el
2/sep/2026. P1 → `forense/prereg-duelo-v2/regla-extraccion-L-v1_1.md`. P2 →
`tools/extrae_l_v1_1.py` + `forense/prereg-duelo-v2/L-extraido-v1_1.tsv`
(171 EXTRAIBLE / 5 NO-EXTRAIBLE de 176; regresión CIV-08: 3/8 coincide, 5/8
diverge, causas declaradas). P3 →
`forense/prereg-duelo-v2/agregado_v1_1b.py`,
`forense/prereg-duelo-v2/scoreboard-v1_1-AGREGADO-b.md`,
`forense/prereg-duelo-v2/agregado-v1_1b-resultado.json`; `FP-221`
actualizada (`forense/firmas-pendientes.tsv`). CONTADOR: celdas pareadas
L-vs-M 0→11. Cierre: `ADR-271` (`canon/gobernanza-v1_15.md`),
`canon/estado-programa-v1_10.md` L0 recifrado 270→271,
`canon/registro-rotulos.tsv` censa `MAESTRA33-E21`. `python3
tests/check.py --baseline` → VERDE. No fusionado por el ejecutor — el
merge es de mesa.
