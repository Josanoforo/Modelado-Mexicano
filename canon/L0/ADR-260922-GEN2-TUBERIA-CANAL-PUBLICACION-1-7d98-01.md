**L0 · ACTO GEN2-TUBERIA-CANAL-PUBLICACION-1** (22/sep/2026, `ADR-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01`).

El canal de publicación existe: el job del push a `main` (`verify.yml`) corre
`corrida0.py registro --verifica --escribe --lote <lote>`, con el lote
derivado mecánicamente (`tools/lote_desde_asientos.py`) del diff que ESE
push introdujo en `forense/replay-evidencia.tsv` — nunca tecleado. Sin
`--force`, sin `--excluye`: probado con push sintético en rama, camino
feliz (asiento nuevo, sin drift → escribe y commitea `[deriva]`) y camino
de guardia (drift preexistente entre `replay-evidencia.tsv` y
`corridas.tsv`, ajeno a este acto → `REPLAY-PISADO`, el job falla con la
lista cruda, no fuerza). `forense/replay-evidencia.tsv`,
`forense/analisis/ci-guardias/censo-tests.tsv` y `data/corrida0/
decisiones.tsv` entran a `merge=union`, cubiertos por T46/T50 (genéricas)
sin tocar `tests/check.py`.

Hallazgo: el drift preexistente (13 corridas cuyo veredicto en
`replay-evidencia.tsv` ya no coincide con lo publicado) significa que el
PRIMER push real por este canal probablemente dispara la guardia antes de
registrar nada — no es un defecto del mecanismo, es exactamente lo que el
mecanismo existe para atrapar. Queda una pregunta a mesa: ¿lote estricto
en `corrida0.py` o un catch-up explícito primero?

Ver `ADR-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` en
`canon/gobernanza-v1_15.md` para el detalle completo.
