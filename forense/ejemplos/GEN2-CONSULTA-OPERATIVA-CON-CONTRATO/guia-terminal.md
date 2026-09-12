# Guía de consulta operativa GEN2

`tools/consulta_gen2.py` consulta una salida del emisor GEN2 por su identidad
exacta. No genera un snapshot, no modifica capturas y no usa el número
histórico, cero o R como sustituto. `NO_COVERAGE` es una respuesta válida y
explica la causa.

## Descubrir consumidores y dominio

Desde la raíz del repositorio:

```bash
python3 tools/consulta_gen2.py --lista-consumidores
```

En JSON:

```bash
python3 tools/consulta_gen2.py --lista-consumidores --json
```

Cada fila informa la identidad que debe copiarse completa, la generación del
enlace, el RESULT y los campos/valores de dominio requeridos. Un contexto vacío
también debe declararse de forma explícita como `{}`.

## Consulta desde terminal

Ejemplo de lectura humana:

```bash
python3 tools/consulta_gen2.py \
  --consumidor 'milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:recibe_remesas' \
  --proposito consulta \
  --contexto-json '{}' \
  --uso MEDICION-GEN2
```

Resultado esperado: `estado: EMITE`,
`RESULT-B-ENIGH-2022-P`, punto `0.04569409956405095` y
`validación independiente: PASA`.

Para salida máquina, añadir `--json`. También se puede guardar una petición
individual como objeto JSON y pasarla con `--peticion ruta.json`.

## Transferencia

Una transferencia exige `seleccion` completa con
`contrato_version=SELECCION-TEMPORAL-v1`, objetivo, corte temporal, serie,
periodos y evidencia de procedencia. Con banderas, se entrega como JSON o como
archivo:

```bash
python3 tools/consulta_gen2.py \
  --consumidor 'milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:recibe_remesas' \
  --proposito transferencia \
  --contexto-json '{}' \
  --uso MEDICION-GEN2 \
  --seleccion-json @seleccion.json \
  --json
```

El wrapper transporta la selección, pero no confía en ella: el selector de
#720 la reproduce contra spec, ejecución, resultados, registro y adopción
sellados. Los parámetros sueltos se rechazan.

## Recorrido reproducible

[`peticiones.json`](peticiones.json) contiene:

- una consulta válida de CIV, DIN, FAM y TRA;
- dominio falso e intento legacy en GEN2;
- transferencia ENIGH 2020→2022 válida;
- intento ENVIPE→remesas por parámetros sueltos;
- selección posterior al corte;
- complemento adoptado con padre y transformación `1-p`;
- proxy descriptivo solicitado como medición GEN2.

Reproducir y comparar las respuestas versionadas:

```bash
python3 tools/consulta_gen2.py \
  --lote forense/ejemplos/GEN2-CONSULTA-OPERATIVA-CON-CONTRATO/peticiones.json \
  --verifica forense/ejemplos/GEN2-CONSULTA-OPERATIVA-CON-CONTRATO/respuestas.json
```

Resultado esperado:

```text
OK respuestas reproducibles: forense/ejemplos/GEN2-CONSULTA-OPERATIVA-CON-CONTRATO/respuestas.json
```

Este dorado fue regenerado después de #731 desde la misma vista común que usa
la consulta. Los 16 RESULT directos devuelven `PASA`; `RESULT-B-ENIGH-2020-P`
conserva `NO-HECHA` únicamente en el recorrido de transferencia histórica,
porque no forma parte de esos 16 RESULT ni del overlay nuevo.

Para persistir otro recorrido, usar un destino propio con `--salida`. Si el
archivo ya existe, el comando se niega a reemplazarlo salvo que se añada
`--sobrescribir`; esta opción nunca escribe snapshots.

## Límites de interpretación

La respuesta JSON incluye estado, RESULT y fuente, población, unidad, evento,
periodo, transformación, dependencias, aptitud, validación independiente,
alcance, versión/hash del contrato y referencias leídas. `valor` sólo aparece
cuando el estado es `EMITE`; una abstención conserva
`motivo_no_cobertura` y no publica un fallback numérico.

Las proporciones describen el universo poblacional indicado. No son un
diagnóstico individual ni una probabilidad personalizada validada. Este
comando no calibra, no adopta parámetros, no abre F6 y no convierte una
consulta en evaluación de generalización.
