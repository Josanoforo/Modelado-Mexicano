# Cierre · GEN2-CONTRATO-DE-SELECCION-Y-EMISION

Fecha: 11/sep/2026  
Entorno: NUBE, compatible con Codex CLI  
PR: #720  
ADR: ADR-479

## Resultado

El emisor ya no acepta que el llamador convierta un RESULT ajeno en el valor
de un consumidor. En propósito `consulta`, cualquier selección externa
produce `NO_COVERAGE`; el único valor elegible es el RESULT adoptado por el
consumidor. En `transferencia`, los parámetros sueltos producen
`NO_COVERAGE` y se exige un contrato `SELECCION-TEMPORAL-v1`.

El contrato transporta objetivo, estimando, unidad, población, codificación,
transformación, periodo, disponibilidad, corte temporal y evidencia de
procedencia. `emitir_binaria_contrato` no confía en compatibilidad ni rol
declarados por el llamador: verifica la selección contra la spec y ejecución
selladas, el registro vigente, la adopción del consumidor, la serie exacta,
el corte y el historial completo que alimentó al selector. El rol se deriva
como `OBSERVACION-SERIE-PREVIA`; un RESULT operativo, renombrado o dependiente
del objetivo no adquiere por eso aptitud de transferencia.

El contraejemplo exacto `RESULT-R-CIV-M-01-P-C1-U1` de ENVIPE 2012/FAC_DEL
hacia `familia.seguro.volatilidad_ausencia_estado` / `recibe_remesas` devuelve
`NO_COVERAGE` tanto en consulta como en transferencia. La transferencia
legítima ENIGH 2020→2022 conserva `0.04377543852935772`. Los complementos
declaran el padre y la transformación `1-p`; las emisiones directas GEN2 se
siguen derivando del registro y mantienen 16/16 en el árbol de esta revisión.

## Evidencia reproducible

- `python3 -m unittest tests.test_motor_gen2_explicito tests.test_baseline_temporal -v`: 23/23.
- `python3 -m unittest tests.test_motor_usos_complementos`: 16/16.
- `env PYTHONPATH=. python3 tests/test_corrida0.py`: 91/91.
- `python3 -m tools.snapshot_motor_gen2 --verifica forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_1.json`: `OK`.
- El snapshot v1.1 conserva las 16 tuplas directas `(consumidor, RESULT, valor,
  estado)` del v1.0. El SHA-256 del v1.0 sigue siendo
  `05350667baa245c79c3ed487aeb1403d74b4612fcae69e16845b8d42f1a5eaa8`.
- `pytest` dirigido sobre fidelidad y emisor_m2: 15/16; el único fallo es histórico y
  espera cinco reglas donde el motor vigente tiene 22, sin relación con este
  cambio.

## Sucesión y registros

Se publica únicamente
`forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_1.json`; el v1.0 y todos
los RESULT históricos quedan intactos. `NC-0157` permanece cerrada y registra
la conciliación del defecto posterior. `NC-0158` permanece abierta por roles
retenidos de confirmación independiente, objeto no satisfecho por este acto.
El rótulo y L0 apuntan a ADR-479. No se crean capturas F5, adopciones ni firmas
metodológicas; contador científico cero. La única obligación restante es la
fusión del PR por Jonás. El PR #722, abierto en paralelo y sin tocar el emisor,
candidatea también ADR-479; si se fusiona primero, este PR debe renumerar a
ADR-480 y actualizar las tres anclas conforme a la regla vigente.
