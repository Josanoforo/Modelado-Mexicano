# ACTO GEN2-F5-PANEL-VIABLE-Y-PRESUPUESTO · cierre

Fecha: 11 de septiembre de 2026.

Entorno: NUBE/WSL2; inventario estático y documentación pública, sin abrir
valores R reservados, capturar L, emitir M ni llamar modelos.

Base: `70c64d9ead92384ece0eaf18cbfb53372bb88a74` (`origin/main` al arranque).
Entrega: [PR #722](https://github.com/Josanoforo/Modelado-Mexicano/pull/722).

## Decisión ejecutable

La opción recomendada es **autorizar FP-373 en un acto posterior**, después de
que Jonás firme modelo, cliente, tarifa y llamadas, CAJA materialice los
paquetes fuente-nativos y el sucesor verifique la interfaz fusionada del
encargo 23. Son 32 llamadas lógicas y, con máximo dos reintentos exclusivamente
técnicos por posición, hasta 96 solicitudes facturables.

La mesa **no debe autorizar FP-374 hoy**. El snapshot explícito de #712 contiene
16 salidas directas, agrupadas en diez familias fuente-estimando; las diez eran
conocidas durante desarrollo y ninguna tiene rol retenido ejecutable. Sólo
cinco tienen al menos dos celdas. El máximo acreditado para transferencia es,
por tanto, **cero familias disponibles** y faltan 18/18 familias disjuntas para
el mínimo de seis piloto más doce confirmatorias.

La ampliación nominal no se convirtió en panel por rótulo: OECD Trust PUM es
una candidata potencialmente reservable, pero carece todavía de acceso,
celdas exactas, consumidor M y split; Mexico Panel Study 2012 ya figuró en el
desarrollo; ENJUVE permanece indeterminada. Las fuentes financieras recientes
se excluyen por unidad, evento o consumidor incompatibles. El inventario
completo y sus exposiciones están en
`forense/prereg-duelo-v2/F5-panel-candidatos-v1_0.tsv`.

## FP-373 · fuentes y pregunta

Pregunta: si entregar el archivo fuente-nativo del estimando aumenta la
cobertura de puntos trazables en `DIN-M-01` y `TRA-M-07` frente a contexto
contemporáneo. Esto mide recuperación/verificación documental, no
generalización.

| celda | paquete nominal | situación |
|---|---|---|
| DIN-M-01 | ENNViH-1: cuestionario, codebook, libro 3B, `fac_3b` y nota de muestra | cinco IDs registrados; diseño de varianza oficial sigue pendiente en FP-371 |
| TRA-M-07 | ENCIG 2021: cuestionario, estructura y CSV con `P8_3_1`, `FAC_P18`, `EST_DIS`, `UPM_DIS` | tres IDs registrados; no sustituir por tasa general, P8_4, otra ola o tabla derivada |

Las fuentes están identificadas y hasheadas en el corpus compartido, pero
NUBE no tiene `data/raw`: CAJA debe materializar miembros, verificar hashes y
probar que el cliente abre los formatos sin truncar. Si falta una fuente o
falla el transporte, se cancelan ambos brazos de esa celda, sin sustitutos.
El brazo contextual recibe sólo tarjeta y paquete #698; el dirigido añade
únicamente los archivos nativos de su celda. Ninguno recibe M, R, `CALC-R`,
tabulaciones del objetivo ni archivos de la otra celda.

## FP-374 · protocolo corregido y presupuesto no autorizado

La unidad inferencial es la familia; dos celdas y ocho réplicas no multiplican
`n`. Para `d_f=error_M-error_L_SOLO`, el protocolo fija
`H0:E[d_f]>=-0.02`, éxito si el límite superior del IC95 bilateral es menor que
`-0.02`, efecto de planeación `-0.04` y brecha al borde nulo `g=0.02`. El tamaño
confirmatorio se fija antes de abrir R con
`ceil(((z_0.975+z_0.80)*sigma_plan/g)^2)`, mínimo 12 y máximo 30 familias.

El piloto requeriría seis familias disjuntas y 192 llamadas. La confirmación,
doce a treinta familias distintas y 384–960 llamadas. Total no autorizado:
576–1,152 llamadas lógicas, 1,728–3,456 solicitudes máximas con reintentos y
36–72 emisiones M/R. Las abstenciones M cuentan contra cobertura como
`NO_COVERAGE`; los faltantes salen del error pero no del denominador de
cobertura; sin varianza R defendible una celda queda descriptiva; menos de
doce familias analizables no adjudica. No existe parada temprana por resultado.

No se publica costo monetario especulativo. La spec expresa llamadas y fórmula
de tokens; el sucesor calculará moneda sólo tras congelar modelo, endpoint,
cliente, caché/batch, ventana, límites y tarifa oficial verificable.

## Interfaz del encargo 23

La sincronización final consume el encargo 23 fusionado como PR #720 en el
commit de `main` `6cda0282079e9623425529f51c2bea171657b0cf`. Contiene
`SELECCION-TEMPORAL-v1`, `seleccionar_transferencia`, el parámetro estructurado
`seleccion_transferencia`, el rol `OBSERVACION-SERIE-PREVIA` y un snapshot
v1.1. Este último conserva las 16 emisiones directas de v1.0 y no crea reserva,
familias ni consumidores. Antes de cualquier ejecución el acto sucesor debe
verificar ascendencia, fijar el snapshot y registrar la interfaz real. Este
acto consume el contrato sin modificar el emisor por cuenta propia.

## Productos

- tabla nominal de 19 candidatos/exclusiones con familia, fuente, ola,
  población, unidad, evento, códigos, diseño, acceso, M, R y exposición;
- mapa de capacidad y protocolo unificado en
  `F5-panel-viabilidad-presupuesto-spec-v1_0.md`;
- fichas ejecutables de FP-373/374 en `forense/firmas-pendientes.tsv`;
- encargo `GEN2-F5-DOCUMENTAL-EJECUCION` en cola, explícitamente pendiente de
  firma y sin autoridad de lanzamiento.

## Verificación y límites

- `tests/test_f5_sin_fugas.py`: 23/23 pruebas OK.
- `tests/check.py --baseline`: línea base verde; sólo los tres fallos heredados
  T06×2/T08×1, sin fallo nuevo ni recifrado.
- Integridad tabular: 19/19 filas con 19 columnas; 363/363 filas de
  `firmas-pendientes.tsv` con nueve columnas.
- `git diff --check`: limpio.
- SHA-256 de `snapshot-M-gen2-explicito-v1_0.json`, `CALC-TRIADA-0002/resultados.json`
  y `CALC-F5-REANALISIS-0001/resultados.json` sin cambio; diff histórico vacío.

No cierra `NC-0160/0161/0162`, no firma `FP-373/374`, DIN, S6, complementos o
deduplicación ENCIG, no autoriza F6 y no altera TRIADA-0002 ni el reanálisis.
El siguiente encargo sigue pendiente de firma de Jonás.
