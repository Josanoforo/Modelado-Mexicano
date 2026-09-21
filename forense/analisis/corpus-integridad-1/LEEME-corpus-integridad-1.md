# corpus-integridad-1 · ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1 (21/sep/2026)

| archivo | qué es |
|---|---|
| `censo_integridad.py` | P1: censo por entrada del manifiesto (reusa `tests/payload_resolver`); sólo lee |
| `censo-2026-09-21.tsv` / `.log` | salida de P1: 1 632 filas, clase por entrada, tamaño real vs declarado, dónde se halló lo que no estaba en su raíz |
| `verifica-2026-09-21.txt` | salida cruda de `python3 tests/manifiesto.py --verifica` (A.1, tres estados sin colapsar) |
| `propuestas-manifiesto-2026-09-21.tsv` | tabla de propuestas de raíz/manifiesto para mesa (este acto no edita el manifiesto) |
| `respaldo_corpus.py` | P3: `--indexa` / `--copia` / `--verifica` / `--restaura N`; sólo lee el corpus |
| `indice-juego-2026-09-21.tsv`, `SHA256SUMS-juego-2026-09-21` | índice del juego generado desde los archivos (1 914 archivos, 19 817 841 648 B) |
| `respaldo-*-2026-09-21.log` | salidas crudas de los cuatro pasos (indexa, copia, verifica, restaura ×2) |
| `INSTRUCCION-RESPALDO.md` | instrucción de una página para repetirlo |
| `irrecuperables.py`, `irrecuperables-2026-09-21.tsv` / `.log` | P4: clase de re-obtención por entrada, sin tocar la red |

Guardia: `tests/test_corpus_integridad_respaldo.py` (corpus sintético; corre en CI como huérfana censada).
