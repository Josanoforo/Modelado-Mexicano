# Receta de apertura de un commit · PEW 2025

Derivada por `expediente_apertura.escribe_receta` (GEN2-APERTURAS-PREREGISTRADAS-1). El acto de apertura no diseña nada; si un paso
no se sostiene, PARA.

1. **Firma**: la fila de mesa que autorice abrir (`firma_que_faltaria` en `data/corrida0/aperturas-pendientes-v1_0.tsv`).
2. **Caja** (A.2, E.6): `python3 tools/entorno.py --arranque` debe decir CAJA.
3. **Preflight documental** (no es abrir; E.6 permite cuestionario, FD y catálogo): para cada variable de
   `APERTURA-PEW-2025-spec.yaml::variables`, el cuestionario/catálogo de 2025 trae el mismo texto de pregunta y
   códigos; la que no, sale NO-ESTIMABLE (spec §5). Salida cruda a la nota del acto.
4. **Un commit (apertura)**:
   a. Levantar custodia de cada payload de `inputs` con `raiz: reserva_respondentes` (`corrida0` no lee esa
      raíz por construcción: `input_manifiesto_FUERA_DE_PERIMETRO`): mover el archivo a `data_raw` con la misma
      ruta relativa y, en `data/manifiesto.yaml`, quitar `estado_reserva` y poner `raiz: data_raw` (pareja que
      exige `tests/manifiesto.py`); `sha256` no cambia. Payload con `raiz` `data_raw`/`descargas_mx`: nada que mover.
   b. `mkdir data/corrida0/CALC-APERTURA-PEW-2025-0001 && cp forense/prereg-aperturas/PEW-2025/APERTURA-PEW-2025-spec.yaml
      data/corrida0/CALC-APERTURA-PEW-2025-0001/spec.yaml`.
   c. `python3 tools/corrida0.py preflight CALC-APERTURA-PEW-2025-0001` → VERDE (el expediente lo simuló sin payload:
      ver la nota del acto que lo escribió).
5. **Run**: `python3 tools/corrida0.py run CALC-APERTURA-PEW-2025-0001`. El medidor corre la auditoría AST antes
   de leer; devuelve R por celda, `-DICTAMEN`, `-K`, `-N`, Wilson, `-MAE-PUNTO`, `-MARCA`.
6. **Asiento**: registro por el job de derivados; `forense/replay-evidencia.tsv` (E.7); re-rótulo de la reserva
   de la ola en el manifiesto por el acto que lo tenga en su perímetro. Contendientes servidos a la vez (E.6):
   CALC-PEW-RELIGION-2024-0001, CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001, CALC-PEW-MIGRACION-MEX-0001.
