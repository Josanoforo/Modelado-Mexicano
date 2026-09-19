# Intentos y sucesión

## Intento 1 · 2023 · no produjo resultado

- CALC: `CALC-ENCIG2023-CRUCES-HISTORICOS-0001`
- Código congelado: commit `9049339`, sha256
  `e2b2f6a17f6163d9bd272e1a008e3dd7826d6121dbd57e01452232d3a74abb6e`.
- Preflight: VERDE; hashes de inputs coincidentes.
- Fallo antes de estimar o sellar: `medidor_fallo:KeyError: 'guardia'`.
- Causa: `contrato_ejecutable()` sólo entrega los campos sustantivos canónicos;
  el medidor intentó leer un campo superior personalizado que la interfaz no
  transmite.
- Sucesor: `CALC-ENCIG2023-CRUCES-HISTORICOS-0002`. El cambio mueve metadatos
  operativos a `parametros`, que sí forma parte de la interfaz. No cambia dato,
  estimando, rejillas, semilla, réplicas, degeneraciones ni regla de elección.

`CALC-ENCIG2021-CRUCES-HISTORICOS-0001` no se ejecutó; se sucede en paralelo
por `-0002` para mantener una implementación idéntica entre olas.

