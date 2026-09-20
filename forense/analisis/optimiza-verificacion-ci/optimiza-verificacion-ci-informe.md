# Optimización de verificación CI

Fecha local: 19/sep/2026; mediciones UTC: 20/sep, 01:46–02:12.
Base: `4bda996fdb2bad1d67f45210c249d52a870a4e35`.
Worktree: `/home/pc0/mm-optimiza-verificacion-ci`, rama
`codex/optimiza-verificacion-ci`, inicialmente limpia.
[PR #901](https://github.com/Josanoforo/Modelado-Mexicano/pull/901), sin fusionar.

## Resultado y decisión

En tres ejecuciones reales por variante, la mediana desde creación del run
hasta finalización del último job bajó **362 → 172 s (52,5%)**. La suma de
duraciones de jobs bajó **360 → 327 s (9,2%)** en mediana. Hay variabilidad
entre runners: se publican las seis observaciones, no una proyección.

El costo está dentro de la suite y en el marcador. Perfil local inicial:
T32 = 41,44 s, T35 = 17,44 s; T16 vuelve a ejecutar el núcleo en un proceso
independiente. El marcador adicional consume 52,15 s localmente; su paso
consumió 134 s en el primer runner. Los demás comandos adicionales sumaron
7,54 s locales. El inventario explícito y sus tiempos están en
[cobertura.tsv](cobertura.tsv): 49 controles principales y 14 comandos
adicionales, con lecturas, escrituras, dependencias y correspondencia anterior/nueva.
Las rutas de lectura describen familias de entradas; los módulos Python de
las dependencias también se leen. No se abrió microdato.

Se eligieron dos jobs, `suite` y `adicionales`, con checkout propio.
Dentro de la suite, `--parallel` ejecuta T35 mediante un worker `spawn`
mientras el proceso principal conserva la secuencia restante. T35 no
escribe producción ni comparte los globals modificados por fixtures de T32.
Sus diagnósticos se incorporan en su posición original, antes de T16 y de la
comparación completa del baseline. El modo paralelo desactiva también las
escrituras de bytecode. T31 conserva sus posibles escrituras de referencias
Git en el proceso principal; T16 empieza después del núcleo y conserva su
subproceso independiente y su timeout de 300 s.

Se conservan las dos ejecuciones del núcleo y las diez llamadas del marcador
a `deriva()`: no se eliminó ninguna comprobación ni se cachearon resultados.
No se implementó un tercer job: con medianas de 165 s para `suite` y 160 s
para `adicionales`, separar los adicionales cortos no reduce la ruta crítica
mediana observada y exige otra preparación. Los cuerpos de pruebas y los
cálculos científicos permanecen intactos.

## Equivalencia y compuerta

[equivalencia.json](equivalencia.json) fija el orden de los 49 controles,
los hashes de sus cuerpos sin cambios, los 94 casos existentes de T32 y los
hashes de los módulos de prueba anidados/adicionales. También permanecen
idénticas la clasificación, normalización, comparación y congelación del
baseline. SHA-256 de `tests/baseline.json`, antes y después:
`688a0dbdc30d3c1a2609af30af55aa49dc5613dae3aa7365441c33a528b80566`.
No se tocó ninguna tolerancia. La CLI anterior sigue siendo secuencial;
la opción nueva sólo cambia la ejecución. Cada control conserva su rótulo
y resultado, con tiempos separados para el núcleo y el hijo de T16.

En las tres comparaciones locales coinciden los multiconjuntos completos
de FAILS, WARNS y SENAL, sin perder multiplicidades: 19 FAIL heredados,
7575 WARN y salida baseline 0. En la primera, realizada en el mismo
worktree antes/después de modificar infraestructura, coincide incluso el
orden de las listas. Las otras usan checkouts distintos y difieren en
orden interno de enumeración del sistema de archivos, no en diagnósticos.
Todos los comandos adicionales dieron 0 en cada repetición.

`check` mantiene el nombre obligatorio, `needs: [suite, adicionales]` e
`if: always()`. Su shell exige literalmente ambos estados `success`.
No hay `continue-on-error`, filtros por rutas ni cambios de protección.
Se conservan checkout `--depth=1 --no-tags` con git, instalación explícita
de requirements, ausencia de marketplace y cancelación por PR.

Se añadieron dos controles bloqueantes de infraestructura: el transporte y
la compuerta en `tests/test_check_parallel.py`, más el test existente
`tests/test_suite_warn_estado.py`. Se ejecutó el shell real del agregador
contra las 36 combinaciones de success/failure/cancelled/skipped/vacío/inesperado:
sólo success/success aprobó. Un FAIL nuevo en cualquiera de los dos caminos
de la suite da baseline 1; fallo conocido y WARN nuevo conservan baseline 0.
Worker cancelado, excepción, payload ausente y T35 omitido/duplicado dan error.

Además se inyectaron fallos reversibles en Actions, en una rama temporal
separada, commit `61347a8`, con los jobs y el agregador del candidato:

| Inyección | suite | adicionales | check | Ejecución |
|---|---|---|---|---|
| salida 17 en suite | failure | success | failure | [35482959302](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482959302) |
| salida 17 en adicionales | success | failure | failure | [35482960574](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482960574) |
| omitir suite | skipped | success | failure | [35482961894](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482961894) |
| omitir adicionales | success | skipped | failure | [35482963179](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482963179) |
| cancelar run durante espera controlada | cancelled | cancelled | failure | [35482964784](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482964784) |

Las inyecciones nunca estuvieron en la rama entregable. Los estados y enlaces
por job están conservados en [mediciones-actions.json](mediciones-actions.json).
La validación posterior del informe detectó además una colisión de su nombre
genérico con un informe previo (T02, run 35483644321): se corrigió usando
el nombre específico del encargo, sin cambiar baseline ni el control.

## Mediciones y condiciones

Actions: `ubuntu-latest`, imagen ubuntu-24.04, Python 3.12.3, instalación de
requirements en cada job. Los tres antes usan exactamente el commit base;
los tres después usan `01b35f9`, cuyo diff sólo contiene infraestructura de
verificación. El primer antes es el push original; los otros cinco son
workflow_dispatch sobre referencias fijadas. No se usaron merge refs móviles
para esta comparación. La validación del PR se hizo aparte y también pasó:
[35482818253](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482818253).

| Variante/run | Total s | Espera inicial s | suite/job antiguo s | adicionales s | check final s | Costo agregado jobs s |
|---|---:|---:|---:|---:|---:|---:|
| antes [35482245209](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482245209) | 362 | 2 | 360 | incluido | incluido | 360 |
| antes [35482843438](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482843438) | 261 | 3 | 258 | incluido | incluido | 258 |
| antes [35483077343](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35483077343) | 404 | 39 | 365 | incluido | incluido | 365 |
| después [35482844734](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35482844734) | 177 | 3 | 168 | 161 | 3 | 332 |
| después [35483010742](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35483010742) | 172 | 7 | 116 | 160 | 3 | 279 |
| después [35483175259](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/35483175259) | 172 | 3 | 165 | 160 | 2 | 327 |

Total = creación → último job completado; no incluye el pequeño retraso de
actualización final de metadatos. La espera inicial incluye asignación/inicio,
no es una medida pura de cola interna. Entre grupos y agregador hubo 2–3 s
adicionales de asignación en los después. Preparación por job de pruebas:
7/8/8 s antes; suite 7/12/8 s y adicionales 8/6/7 s después. La API redondea
pasos a segundos y hay transiciones fuera de esos pasos; no se fuerza que
su suma sea exactamente la duración del job. El JSON conserva cada paso.
El costo es runner-segundos observados, no CPU ni minutos facturados.
La variabilidad impide atribuir el 9,2% agregado exclusivamente al código;
el descenso de espera sí aparece en las tres observaciones sin solaparse
con el rango anterior, incluso separando la espera inicial.

Local: WSL2, Python 3.14.4, 24 CPUs visibles, mismo entorno y dependencias
en ambos lados; PyYAML 6.0.3, jsonschema 4.19.2, xlrd 2.0.2. Markdown no
está instalado localmente y no es invocado por este inventario; Actions sí
instala requirements completo. No hay `data/raw` montado en los checkouts
aislados. Los perfiles de suite fueron 133,33/131,90/141,94 s antes y
96,51/110,09/103,62 s después. El primer después mide sólo la suite;
los otros dos incluyen contención con el job adicional concurrente.

| Comparación local completa | Total antes/después s | suite antes/después s | adicionales antes/después s | Suma tiempos de grupos antes/después s | CPU agregada antes/después s |
|---|---|---|---|---|---|
| repetición 2 | 192,51 / 110,76 | 131,90 / 110,09 | 59,86 / 62,34 | 191,76 / 172,43 | 191,87 / 201,31 |
| repetición 3 | 211,04 / 104,36 | 141,94 / 103,62 | 63,12 / 64,42 | 205,06 / 168,04 | 204,39 / 206,91 |

Mediana local completa: 201,78 → 107,56 s (46,7%). La CPU agregada sube
ligeramente: se solapa trabajo conservado, no se promete eliminarlo.
Los totales incluyen arranque/espera del arnés y serialización de diagnósticos.
La desactivación final de bytecode se validó además: 99,08 s, salida 0,
diagnósticos equivalentes; es una corrida adicional, fuera de esas medianas.
Detalle en [mediciones-locales.json](mediciones-locales.json).

Para reproducir, crear checkouts aislados de base y candidato sin microdatos,
instalar las mismas dependencias, y usar [medir-suite.py](medir-suite.py)
con `CHECKOUT /tmp/salida.json`, añadiendo `--parallel` al candidato.
[medir-adicionales.py](medir-adicionales.py) acepta los mismos dos argumentos
y ejecuta la lista explícita de 14 comandos. Alternar antes (suite y adicionales
secuenciales) y después (ambos procesos simultáneos en checkouts distintos),
esperar y comprobar ambos códigos. Guardar resultados fuera de los checkouts.
Los arneses no sustituyen el inventario ni descubren nuevas pruebas para CI.
