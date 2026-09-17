# ENCIG 2023 · agregado condicional de `P8_4`

**Estado:** `TASA-REPORTADA-CON-RESERVA`. El resultado es descriptivo y
condicional al flujo que hizo observable `P8_4`; no es una tasa de toda la
población ni de todo trámite. La derivación usa el mismo payload y desenlace
que la medición por canal previa y no cuenta como fuente estadística
independiente.

## Resultado fijado

| universo | n eventos | masa denominador `FAC_TRA` | masa `P8_4=1` | p | IC95 p | q | IC95 q |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Primario: todos los canales observados** | 23,100 | 63,712,439 | 13,024,773 | **0.204431** | [0.191577, 0.217767] | **0.795569** | [0.782233, 0.808423] |
| Secundario: PRE∪DIG | 16,857 | 47,482,305 | 4,054,591 | 0.085392 | [0.074586, 0.098137] | 0.914608 | [0.901863, 0.925414] |

Restringir a PRE∪DIG conserva 72.97% de los eventos y 74.53% de la masa del
universo primario. Excluye 6,243 eventos y masa 16,230,134. El punto baja
11.90 puntos porcentuales; por eso ni el promedio simple de las tasas PRE/DIG
ni la selección de uno de esos brazos reconstruye el estimando sin canal.

## Descomposición que reconstruye el primario

| parte de `P7_3` | n | masa denominador | masa numerador | p | q |
|---|---:|---:|---:|---:|---:|
| PRE `{1}` | 10,852 | 27,406,509 | 3,584,675 | 0.130796 | 0.869204 |
| DIG `{3,4,5}` | 6,005 | 20,075,796 | 469,916 | 0.023407 | 0.976593 |
| OTRO `{2,6,7,8,9}` | 2,332 | 8,912,353 | 2,239,816 | 0.251316 | 0.748684 |
| Canal faltante | 3,911 | 7,317,781 | 6,730,366 | 0.919728 | 0.080272 |
| **Total primario** | **23,100** | **63,712,439** | **13,024,773** | **0.204431** | **0.795569** |

Las sumas de `n`, denominador y numerador cierran exactamente. “Canal
faltante” no se reasigna a PRE/DIG: es una parte explícita del universo
primario y explica materialmente la distancia respecto de la sensibilidad.
Un `P8_4` faltante, en cambio, queda fuera de ambos universos y nunca se trata
como cero.

## Cobertura, unión e incertidumbre

- Unión: 123,186/123,186 eventos de `sec_7`, 100% por conteo y por masa;
  control compuesto coincidente, cero eventos sin pareja, cero pesos inválidos.
- Desenlace observado: 23,100/123,186 = **18.7521%** por conteo y **15.8400%**
  por masa. Los otros 100,086 eventos unidos tienen `P8_4` faltante. La unión
  perfecta no elimina esta reserva de observación.
- IC: 2,000 réplicas PCG64, semilla 20260915, UPM dentro de estrato, cociente
  completo por réplica. Primario: 308 estratos, 3,195 UPM, 48 estratos con una
  UPM; PRE∪DIG: 301, 2,990 y 45. Hubo cero filas sin diseño y cero réplicas no
  estimables. Las UPM únicas se remuestrean a sí mismas y aportan variación
  cero; se declara la limitación sin llamar automáticamente “cota inferior” a
  los intervalos.

## Correspondencia concreta que queda por decidir

Si mesa acepta **el universo primario ya fijado** como proxy del consumidor
único sin canal, la correspondencia coherente sería:

- `RES-0008` → `RESULT-ENCIG23-AGCOND-PRIMARIO-P` = 0.2044306136200499
  (`tramite.mordida.con_registro:paga_mordida`);
- `RES-0007` → `RESULT-ENCIG23-AGCOND-PRIMARIO-Q` = 0.7955693863799501
  (`tramite.mordida.con_registro:tramite_normal`).

Los dos valores comparten exactamente el denominador 63,712,439 y suman uno.
Esta es una **propuesta para decisión**, no un enlace ni una adopción. El
secundario PRE∪DIG queda como sensibilidad preanunciada; escogerlo después de
ver la diferencia cambiaría el universo y requiere una decisión explícita de
mesa. También son opciones todavía abiertas conservar el prior actual o
partir el consumidor por canal. `RES-0001/0002` pertenecen a otra familia y no
reciben ninguna correspondencia de este CALC.

## Cadena

- Base de trabajo: `4fff914f286021574ac0897273ee0e6971b38f04` (`origin/main`).
- Commit previo a abrir el agregado: `b347743353b276b2ea7f0aa90a459c32ae9ecac3`.
- Payload: `encig23_base_datos_csv`, SHA-256
  `af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d`.
- Spec humana: `253391b6a9a58de9f9ee2c65c60566c0be11b8f3e14b7b9390cd2b1d15970f66`.
- Script: `7bdbe8c43bb83988e66ddd03bb060450612bdcafec58e1a9fb9eb3d216c2eb48`.
- Sello: `4c55dbdee9d9015ad2c64c40bf5f3cc172de6fa80b378612283409c82bc68696`.
- Verificación dirigida: `REPRODUCE`, contexto y 65 resultados idénticos.

## Propagación diferida para integración serial

Después de CAREO/TRÁMITE-4, mesa debe registrar una decisión entre adoptar el
primario, redefinir explícitamente el consumidor a PRE∪DIG, partir por canal o
conservar el prior. Sólo si adopta, la integración serial debe enlazar ambos
RESULT complementarios, conservar `CON-RESERVA`, registrar la validación
independiente aún `NO-HECHA` y entonces propagar los archivos compartidos de
decisión/estado/rótulos/manifiesto/tableros/contadores que correspondan. Este
acto no ejecuta esa cascada ni reserva numeración.
