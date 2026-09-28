# Receta de apertura de un commit · ENSANUT 2025

Qué hace el acto de apertura (no diseña nada; si algo de esto no se sostiene, PARA):

1. **Firma**: fila de mesa que congele este expediente y autorice la apertura (`firma_que_faltaria` en `data/corrida0/aperturas-pendientes-v1_0.tsv`).
2. **Caja** (A.2, E.6): `python3 tools/entorno.py --arranque` → CAJA; verifica `spec_md_sha256`, `script_sha256`,
   `guardia_sha256` y los sha del contendiente de `APERTURA-ENSANUT-2025-spec.yaml` contra el árbol: si difieren, PARO.
3. **Preflight documental** (no es abrir): para cada columna del contendiente, el catálogo `ensanut_2025__*_catalogo_xlsx`
   trae el mismo texto de pregunta y códigos; la que no, NO-ESTIMABLE (spec §5). Salida cruda a la nota.
4. **COMMIT-1 de apertura**: copia literal de esta carpeta a `data/corrida0/CALC-APERTURA-ENSANUT-2025-0001/`
   (spec.yaml con `calc_id` e `inputs` en el formato de `corrida0`), sin editar el medidor; `corrida0 preflight` VERDE.
5. **COMMIT-3** (R y adjudicación): `python3 tools/corrida0.py run CALC-APERTURA-ENSANUT-2025-0001`; el medidor corre la
   auditoría AST antes de leer; `resultados.json` trae R por celda, `-DICTAMEN`, Wilson, MAE.
6. **Asiento**: vista (job de derivados), `forense/replay-evidencia.tsv` (E.7), y re-rótulo de `estado_reserva` de los ids
   por el acto que tenga el manifiesto en su perímetro.
