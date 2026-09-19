# Entrega a `GEN2-MARCADOR-REDISENO-1`

Fecha: 19/sep/2026. Este documento es antecedente técnico, no adopción.

## Pisos corregidos

El carril A es dueño de publicar los sucesores de los pisos y su mapa técnico. Mientras no esté fusionado, su SHA y las identidades finales son **PENDIENTES DE INTEGRACIÓN**; no se sustituyen con los cuatro originales de #866. Esos cuatro originales quedan vetados de forma exacta:

- `CALC-PISOS-ENCIG2023-EJES-0001`
- `CALC-PISOS-ENCIG2023-EJES-0001-v1_1`
- `CALC-PISOS-ENIF2021-EJES-0001`
- `CALC-PISOS-ENVIPE2024-EJES-0001`

El veto no se hereda a sucesores. La relación técnica sucesora tampoco decide el contador: `FP-386` conserva pendiente si el ENCIG original pasa a `SUPERADO`, deja `cuenta_gen2=SI` o cambia clasificación. Acceso y evidencia se separan: ENCRIGE/ENSANUT pueden seguir `NO-VERIFICABLE` aunque su asiento exista.

## Veinte C2 y NC-0313

Mesa adoptó como estimador por celda los 20 pisos C2 representados por ADR-538/ADR-542: ocho DIN y doce TRA, con decisión, representación y consumo activo como etapas distintas. El marcador Claude debe citar el piso propio de cada celda; no hay un estimador global por defecto. `NC-0313` no desaparece: el control global DIN conserva `NO-REPRODUCE/IDENTICO` porque el snapshot de orden cambia después de COMMIT-3, mientras 220/221 resultados sustantivos —incluidos puntos e IC de C2— reproducen. No se debe convertir ese falsador global en exclusión de los puntos que sí reproducen.

## Medición disponible no es consumo

Los resultados de un `CALC` sellado o publicado son oferta. Sólo una cita efectiva del consumidor acredita uso activo. Ni el veto de los cuatro originales ni la medición de un sucesor adoptan automáticamente los pisos en el marcador. El universo del emisor es 97 con cinco `SIN-CONTRAPARTE`; sumar los 20 C2 para declarar 117 mezcla objetos y queda prohibido.

## PR #868: propuesta a revisar, no herencia

PR #868 está abierto en `9e9e89225f0d986cf51b955940ebee7526809f1b` y reporta un check fallido. Su diff contra la base incluye vistas corrida0, `data/corrida0/marcador-segmento.tsv`, `milpa/estimadores-por-segmento.yaml`, `milpa/src/estimadores_segmento.py`, `milpa/src/motor.py`, `tools/corrida0.py`, `tools/marcador_segmento.py`, `tools/tablero_programa.py` y `tests/test_estimadores_segmento.py`, además de cambios documentales y retiros de instrucciones. Todo ello es trabajo propuesto: debe revisarse por identidad, contrato y pruebas; no es válido ni adoptado por provenir de una rama anterior. En particular, no se importaron sus vistas con OURS/THEIRS.

## Pendientes reales antes del marcador

- resolver por celda la identificación y el estimador adjudicado en el catálogo de momentos;
- respetar estados del crosswalk: `EQUIVALENTE`, `MAPEO-N-A-1`, `NO-EQUIVALENTE`, `SIN-CORRESPONDENCIA`;
- mantener las reservas consumidas sin volver a derivarlas;
- resolver `NC-0300` (lado emisor) y los alcances aún abiertos de NC-0024/0076/0239;
- comprobar el mapa final de pisos sucesores y la reserva de contador tras el merge de A.

No se sella informe v1.1 hasta que el marcador y sus consumidores efectivos existan en `main`.
