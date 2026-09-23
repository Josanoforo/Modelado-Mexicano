**L0 · ACTO GEN2-TUBERIA-LOTE-ESTRICTO-1** (23/sep/2026, `ADR-260923-GEN2-TUBERIA-LOTE-ESTRICTO-1-9428-01`).

`registro --escribe --lote <ids>` acota la ESCRITURA de `corridas.tsv` /
`resultados.tsv` / `usos.tsv` a las filas del lote y a las que nunca se
publicaron; toda fila YA PUBLICADA y ajena al lote se conserva byte a byte
(`tools/corrida0.py::_acota_vistas_al_lote`), en vez de re-proyectarse
desde `replay-evidencia.tsv` como antes. Medido contra el repo real (sin
escribir): 13 corridas ajenas / 26 campos disparaban `REPLAY-PISADO` aunque
nadie las nombrara — mismo número que `ADR-260922-GEN2-TUBERIA-CANAL-
PUBLICACION-1-7d98-01` ya había medido con push sintético. Reproducido de
nuevo con push sintético en un clon desechable: antes del fix, `REPLAY-
PISADO` sobre las 13; después, `EXIT=0` y las 13 quedan byte a byte
idénticas mientras la fila del lote entra. Implementa la opción (a) que
`FP-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` dejó firmada; NC
7d98-02 cierra aquí.

Ver `ADR-260923-GEN2-TUBERIA-LOTE-ESTRICTO-1-9428-01` en
`canon/gobernanza-v1_15.md` para el detalle completo.
