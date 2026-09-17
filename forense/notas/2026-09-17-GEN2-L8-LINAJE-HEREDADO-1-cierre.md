# Cierre · GEN2-L8-LINAJE-HEREDADO-1

## Resultado

Se corrigió la clasificación de la única fuente numérica de
`CALC-L8-CONVERSION-0001`: la identidad exacta
`data/l8-resultados-tipo-boleta-v1_0.json` ahora se reconoce `HEREDADO`. La
ruta existente propaga ese origen a
`RESULT-L8CONV-A-P-MINIMO`, `RESULT-L8CONV-A-P-MAXIMO` y
`RESULT-L8CONV-A-P-MEDIA`.

El cambio no crea una fuente nueva, no modifica categorías de linaje, no abre
una excepción a `MEDICION-GEN2` y no altera el JSON, la spec, los resultados,
el redondeo, la ejecución ni los sellos L8. Una ruta desconocida o de nombre
parecido permanece `INDETERMINADO`; bytes con otro SHA permanecen rechazados.

Evidencia y decisión propuesta:
`forense/analisis/l8-linaje-heredado-1/antes-despues.md`.

## Estado preciso

- **PREPARADO:** correctivo mínimo, regresión y evidencia en rama propia.
- **EJECUTADO:** clasificación y propagación comprobadas sobre el árbol real;
  el arnés dirigido queda verde.
- **SELLADO:** `CALC-L8-CONVERSION-0001` ya estaba sellada y conserva sus bytes;
  este acto no produce ni reescribe un sello.
- **INTEGRADO:** no hasta que Jonás fusione el PR.
- **ADOPTADO:** no; `milpa/tramite.yaml` no se modifica y los tres consumidores
  siguen sin cita GEN2.

## Cascada y reserva

`CIERRE COMPARTIDO DIFERIDO`: no se editan `forense/no-corrido.tsv`,
`decisiones.tsv`, firmas, hallazgos, PARA, gobernanza, estado, rótulos,
tableros, contadores, colas ni registros globales. Después del trámite de
Opus, la integración serial sólo necesita: (1) reflejar que la indeterminación
técnica de NC-0253 está resuelta sin cerrar su decisión de consumo y (2), si
mesa acepta la propuesta, registrar por separado el uso `DESCRIPTIVO` y la
cita futura de los tres resultados. No se reserva numeración.

## Decisión pendiente de mesa

Una sola: aceptar o rechazar conservar los tres resultados como legado
explícito bajo `DESCRIPTIVO`. La aptitud de linaje no decide compatibilidad del
estimando ni validez causal. Mientras no haya decisión/cita, se mantienen sin
consumo GEN2.

## Verificación

- `python3 tests/test_corrida0.py`: 93 casos, 93 ok, 0 fallos.
- `python3 tools/corrida0.py verify CALC-L8-CONVERSION-0001`: sello e inputs
  `COINCIDE`, contexto `IDENTICO`, resultado `REPRODUCE`; los tres del encargo
  tienen delta `0.0`.
- Derivación de `registro(escribe=False, imprime=False)`: los tres RESULT
  pasan de `INDETERMINADO` a `HEREDADO` por `IN-L8-JSON:DATO`.
- `python3 tools/corrida0.py status --json`: envueltos 21→22; dependencias
  heredadas activas 183→183; adoptados activos 24→24.
- `python3 tests/check.py --baseline`: `LÍNEA BASE: VERDE`, 3 FAIL y 4351 WARN
  heredados; T32 `T-CORRIDA0` queda verde.
- `git diff --check`: única advertencia en la línea 3 del encargo archivado,
  por los dos espacios finales presentes en el original y preservados para
  mantenerlo verbatim; código, prueba, análisis y cierre sin errores de
  whitespace.

No se ejecutó el productor del panel L8, microdatos, cron, trámite ni
escritores globales.
