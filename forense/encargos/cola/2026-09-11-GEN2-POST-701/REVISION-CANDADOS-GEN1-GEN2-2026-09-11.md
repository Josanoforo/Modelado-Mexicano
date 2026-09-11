# Revisión de los candados GEN1 → GEN2

**Fecha:** 11/sep/2026. **Corte:** main #694, `4816101e506f527d018dd2c47467a8b57bfbd487`. Se consultaron también los PR abiertos #695–699. Dictamen: **los candados existen, pero no cubren toda la cadena; no corresponde presentar el motor completo ni F5 como Gen2 numéricamente independiente.** Hay mediciones nuevas útiles y fallos reparables, sin necesidad de borrar Gen1 o reiniciar el proyecto.

## Qué se comprobó y qué significa

El [plan GEN2 v2.0](https://github.com/Josanoforo/Modelado-Mexicano/blob/4816101e506f527d018dd2c47467a8b57bfbd487/forense/notas/PLAN-FINAL-GEN2-v2_0-2026-09-07.md), §§1–3 y 7, exige corridas nuevas selladas, receta no elegida por valores GEN1 y cadena hasta el consumidor. Las reglas E.1 y la adenda T9 excluyen los corredores que envuelven números antiguos, distinguen fuente del árbitro y exigen olas estrictamente anteriores para transferencia. Una firma posterior puede autorizar contar trabajo sellado; no cambia el origen del número.

La revisión fue dirigida a tres recorridos: medición→registro→adopción; datos/hipótesis→motor→snapshot; corpus/modelos/árbitros→evaluación. Se inspeccionó el contenido de los contratos, se ejecutaron pruebas existentes y se hicieron contraejemplos temporales. No se abrieron microdatos, no hubo llamadas a modelos, no se modificó el repo ni se interrumpieron encargos. Los dos ZIP adjuntos son de agosto y no contienen el diseño GEN2; el repo actual manda para este diagnóstico.

| Candado | Estado observado | Alcance real |
|---|---|---|
| Specs, hashes, sellos e inmutabilidad | Operativo en la validación dirigida | Protege los artefactos declarados; no demuestra por sí solo que se declararon todas las lecturas. |
| Separación de replay y medición | Parcial | Los dos smokes conservan LEGACY-GEN1/cuenta=NO. E.1 detecta varias envolturas, pero su clasificación depende de rutas literales. |
| Adopción con RESULT y valor coincidente | Operativo con hueco material | T35 detecta citas rotas y valores distintos. No rechaza una cita a un wrapper numéricamente heredado cuya etiqueta formal sigue GEN2. |
| Independencia M respecto del árbitro | Existe en contratos y corredores anteriores | El calculador de F5 completa no consulta los estados de contaminación e identidad del snapshot. |
| Corpus fijo y brazos L separados | Integridad verificada: 14 paquetes | Hashes verifican contenido. Reutilizar informes de contexto no los convierte en nueva evidencia primaria; no se hizo auditoría bibliográfica de todas sus afirmaciones. |
| AJUSTE/HOLDOUT del motor matricial GEN2-E0 | Muro funcional en cinco pruebas; reserva histórica de cronología | Es otra ruta del motor. No protege automáticamente el emisor M ni el nuevo calculador F5. |

**No confundir cuatro cosas:** reutilizar código contrastado; reestimar con microdatos; heredar una cifra; evaluar con datos ya usados para diseñar/ajustar. Tienen consecuencias diferentes. Un algoritmo estadístico de Gen1 puede reutilizarse con pruebas; copiar una tasa y cambiar su carpeta no crea una medición. Las hipótesis fundacionales pueden mantenerse como hipótesis, sin heredar automáticamente confirmación, tier o validez causal.

## Hallazgos materiales

### H1 · El motor operativo sigue en migración: 191 usos heredados y 16 con adopción GEN2

Derivado por `corrida0.status(imprime=False)` y `_filas_registro(False)`: 207 usos activos, 191 `LEGACY-GEN1`, 16 `GEN2`. Son filas de uso registradas, no 207 reglas ni 207 predicciones, y no constituyen todavía una auditoría de todo cierre transitivo oculto.

El [emisor](https://github.com/Josanoforo/Modelado-Mexicano/blob/4816101e506f527d018dd2c47467a8b57bfbd487/milpa/src/emisor.py) carga probabilidades, condiciones y tiers del YAML vigente. Su salida transporta algunos RESULT, pero no impone una modalidad que excluya todo insumo numérico legacy. La [rebanada matricial](https://github.com/Josanoforo/Modelado-Mexicano/blob/4816101e506f527d018dd2c47467a8b57bfbd487/milpa/src/motor.py) es diferente: evalúa tres celdas-semilla y estados; no es el emisor probabilístico completo del duelo. Que sus tests de HOLDOUT funcionen no acredita la separación en el otro camino.

**Consecuencia:** el rótulo GEN2 del programa o la fecha de ejecución no certifican todas las salidas del motor. La migración declarada no es fraude ni vuelve falsos los 191 usos; sí impide afirmar que el conjunto está renovado. La siguiente mejora debe producir un emisor explícitamente Gen2 para los consumidores que ya tengan cadena apta, dejando visible lo mixto.

### H2 · E.1 pierde linaje y también bloquea reutilización legítima por ubicación

En [corrida0.py](https://github.com/Josanoforo/Modelado-Mexicano/blob/4816101e506f527d018dd2c47467a8b57bfbd487/tools/corrida0.py), `_inputs_legacy_de` coteja prefijos literales; `_propaga_envuelto` sigue sólo `data/corrida0/CALC-…/resultados.json` y padres ya marcados `envuelto_legacy=SI`.

Contraejemplos reproducidos:

- `milpa/tramite.yaml` → cuenta NO; `./milpa/tramite.yaml` y `milpa/../milpa/tramite.yaml` → SI. Es la misma ruta material bajo una escritura distinta.
- Un hijo de un CALC declarado `LEGACY-GEN1`, pero sin input que active esos prefijos, no hereda la marca. Caso sintético; no se afirma que ya exista tal adopción en main.
- `snapshot-M-triada-v1_0.json` no activa el detector. El snapshot declara 14 puntos `REUTILIZADA`, hashes de milpa y fuentes de `corridas-M`. TRIADA-0001 figura `envuelto_legacy=SI`, TRIADA-0002 `NO`, pese a reutilizar el mismo snapshot M. Su firma válida de contador no elimina ese antecedente.
- Ocho CALC-R sucesores aparecen envueltos al declarar como código `corridas-R/correr-R.py`. Sus medidores calculan desde fuentes; la ruta del programa por sí sola no demuestra copia de un resultado. Debe verificarse su uso y función, no retirarse esa marca a ciegas ni mover el código de carpeta para hacerlo pasar.

**Corrección:** reconocer identidad normalizada y función del insumo —dato, código, metadato, referencia histórica— y propagar origen numérico por los intermediarios realmente usados. No sustituir el detector por otra lista de nombres ni declarar todas las ramas limpias por llevar hashes.

### H3 · T35 permite adoptar como GEN2 un resultado envuelto legacy

Se construyó un fixture con sello real, `generacion=GEN2`, `cuenta_gen2=NO`, input legacy y por ello `envuelto_legacy=SI`. Su consumidor cita el RESULT y materializa exactamente 0.5. El registro lo acepta y **T35 devuelve cero fallos**.

La razón: registro/T35 rechazan el destino cuya `generacion` literal es `LEGACY-GEN1`, pero no su origen numérico heredado. La prueba demuestra una entrada abierta; **no acredita que las 16 adopciones actuales la hayan utilizado**.

**Corrección prioritaria:** decidir la aptitud del RESULT para el uso solicitado desde su cadena, no desde `cuenta_gen2` ni una sola etiqueta. Una excepción de contador puede contar un análisis de números antiguos y aun así no habilitarlo como parámetro renovado.

### H4 · F5 completa no aplica el estado de contaminación/identidad

En [calcula_f5_completa.py](https://github.com/Josanoforo/Modelado-Mexicano/blob/4816101e506f527d018dd2c47467a8b57bfbd487/tools/calcula_f5_completa.py), `calcular()` extrae `id_celda→punto_M`, descartando `estado_firewall` e `identidad_confirmada`. U3 se forma por disponibilidad numérica.

En copias temporales, marcar CIV-M-01 como `CONTAMINADO-POR-OBJETIVO` o poner `identidad_confirmada=false` **no cambia U3=12 ni el MAE**; la salida sigue `SIN-GANADOR-UNICO`. Esto contradice la protección material de los contratos F5, aunque las 14 filas del snapshot publicado estén rotuladas limpias.

**Corrección prioritaria:** una sucesora debe excluir o parar por el control roto según una regla explícita previa, incluyendo estado desconocido y procedencia insuficiente. Preservar el calculador histórico y su resultado; no declarar retrospectivamente contaminadas las 12 celdas sólo porque faltaba el guard.

### H5 · El sello F5 declara cinco entradas, pero el medidor lee otras 238 salidas JSON

La [spec TRIADA-0002](https://github.com/Josanoforo/Modelado-Mexicano/blob/4816101e506f527d018dd2c47467a8b57bfbd487/data/corrida0/CALC-TRIADA-0002/spec.yaml) declara cinco inputs. La sonda de aperturas del medidor registró además **224 capturas y 14 resultados R**, abiertos por rutas del plan/universo. El medidor devuelve sus 27 RESULT incluso recibiendo `inputs={}`: usa el árbol y no el mapa resuelto que entrega corrida0.

El commit de ejecución conserva los bytes históricos, por lo que esto **no demuestra pérdida de las capturas originales**. El defecto es que la identidad de replay y el grafo de inputs no representan esas dependencias materiales al mismo nivel que las cinco entradas. Así, una auditoría del mapa no basta para comprobar aislamiento y no permite heredar bien el linaje R/M/L.

**Corrección:** fijar la clausura efectiva por rutas+hashes y hacer que el medidor consuma el snapshot resuelto. Puede usarse un manifiesto colectivo que verifique todas sus entradas; una lista de nombres sola no basta. Una captura alterada con la misma identidad de prompt debe detectarse antes de puntuar. Los controles de acceso observados en algunos wrappers son instrumentación de auditoría, no un sandbox contra código malicioso.

### H6 · La evaluación conocida sirve para diagnóstico; ajustar con ella requiere otra validación

El [PR #698](https://github.com/Josanoforo/Modelado-Mexicano/pull/698), todavía propuesto al corte, identifica que CIV enfrenta distintos estimandos y que el snapshot M no equivale al motor corregido actual. Rotula sus mejoras simuladas como exploratorias y propone 32 posiciones para acceso documental: esa prudencia debe conservarse.

El corpus y las capturas se pueden mejorar usando lo aprendido. Pero el panel de 14 celdas ya conocido, el piso B con exposición declarada y la selección de variantes no se vuelven una prueba ciega por abrir otra conversación o sellar otra corrida. El riesgo de ajustar la selección al mismo criterio de evaluación está documentado por [Cawley y Talbot, JMLR 2010](https://www.jmlr.org/papers/v11/cawley10a.html). La aplicación al repo es una inferencia metodológica, no una prueba de manipulación.

**Corrección científica:** contratos M/R iguales en unidad, población, evento, ola y transformación; separar prueba de consulta documental de transferencia temporal/generalización. Los datos y resultados de ajuste, diagnóstico y evaluación retenida tienen identidades y roles explícitos. Un R publicado no pierde su historia de uso porque un medidor nuevo lo reproduzca. No se conoce por completo qué vio un LLM durante preentrenamiento; el aislamiento acreditable es el del experimento y su equipo, con ese límite declarado.

## Pruebas y límites

- `tests/test_corredores_gen2.py`: **35/35**.
- `tests/test_corrida0.py`: **84/84**.
- Constructor de corpus F5 `--verificar`: **14 paquetes íntegros**.
- `tests/test_motor_holdout.py`: cinco comprobaciones pasan; falla la de anterioridad catálogo/motor. La reserva ya está documentada en gobernanza (ACTO GEN2-T9, mismo commit histórico), y este clon es shallow: no se vende como hallazgo nuevo ni se reconstruye la cronología desde historia truncada.
- [PRUEBAS-CANDADOS-GEN2.py](PRUEBAS-CANDADOS-GEN2.py) y [resultado JSON](RESULTADOS-PRUEBAS-CANDADOS-GEN2.json): casos descritos arriba, con fixtures y snapshots temporales. Las suites verdes no cubrían estos contraejemplos.

No se ejecutó suite general ni una nueva evaluación con modelos. No se certificó independencia causal, validez externa ni todas las adopciones sólo con esta revisión. El dictamen es sobre los recorridos examinados y sus contraejemplos.

## Ajustes y orden de trabajo

| Encargo | Producto | Dependencia / ejecución |
|---|---|---|
| [17 · Linaje y adopción](17-GEN2-LINAJE-Y-ADOPCION.md) | Clasificación por origen y uso; evita que una envoltura se adopte como medición nueva | Cloud. Puede empezar ya; coordinar escritura de vistas con 09/#696. |
| [18 · Motor Gen2 explícito](18-GEN2-MOTOR-Y-HERENCIA-EXPLICITA.md) | Emisiones con contrato y cadena completa; cobertura nueva y herencia visibles | Cloud para mapa y código; CAJA sólo si faltan mediciones. Implementación final integra el contrato de 17. |
| [19 · Evaluación protegida](19-GEN2-EVALUACION-SIN-FUGAS.md) | Sucesora del calculador, entradas cerradas, exclusiones efectivas y diseño de evaluación nueva | Cloud. Arranca pruebas/diseño en paralelo; integra 17/18 antes de evaluar un M renovado. |

**Lo que puede seguir:** adquisiciones/cron, medidas ya autorizadas, validación ENVIPE, fintech, ya-medido y S6. No se usan los árbitros retenidos para corregir cifras del motor. Los PR #695–699 no reparan estos nuevos huecos sólo por estar verdes; su trabajo documental o de medición no necesita desecharse.

**Lo que reordenaría:** antes de nuevas adopciones que dependan de un origen dudoso, integrar 17. Antes de otra adjudicación de superioridad, terminar los controles de 19 y comprobar el M de 18. El experimento de 32 posiciones de #698 es una propuesta de cobertura, no autorización para convertirlo en confirmación general ni para gastar ahora.

No se requiere otra firma para investigar y reparar los fallos mecánicos aquí probados. Sí habrá decisiones sustantivas si una nueva receta, prior, universo o tier cambia: 18 las devolverá con impacto y opciones. Las firmas de complemento/DIN/corrupción de la bandeja anterior siguen como estaban, sin inferir aprobación de este pedido.

**Prompt de lanzamiento:** “Ejecuta el encargo adjunto completo. Contrasta sólo avances posteriores pertinentes; continúa entre sus fases autorizadas. Gen1 conserva su historia; ninguna etiqueta o sello sustituye el linaje ni la validación. Entrega un PR revisable, sin fusionar.”


## Actualización de integración al cierre

La comprobación final encontró `origin/main=a63fd4ccc40204cf5215d466a593b4e1491bdda6`: **#699 (encolado de 14–16) y #696 (publicación 09) ya están fusionados**. Se cotejó el delta desde el SHA de las pruebas: no cambió corrida0, T35, el calculador F5, las pruebas examinadas ni milpa/src. Los contraejemplos siguen aplicando al código vigente. Las vistas recién publicadas confirman los mismos 191 usos legacy y 16 GEN2. Se conserva el SHA original en el JSON de pruebas para no atribuirle una ejecución distinta.

Por tanto, **no volver a encargar 09** ni esperar su merge: 17 parte de la publicación de #696. Los análisis de #695/#697/#698 se trataron como propuestas; no se presume aquí su integración posterior. 14–16 ya están en cola; no duplicarlos.
