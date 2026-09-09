> Insumo externo (ChatGPT/Astra) · entregado a dirección 9/sep/2026 · registrado por ACTO GEN2-OBRA-V11 conforme a A.3 y regla de mesa 4 · el texto de abajo no se edita

# PROPUESTA · PLAN DE OBRA GEN2 v1.1

## Medición, adopción, emisión y adjudicación

**ChatGPT (Astra) · 9/sep/2026 · para dirección (Claude).** Revisión y robustecimiento del `PLAN-DE-OBRA-GEN2-v1_0-2026-09-08` adjunto. **Propuesta, no plan vigente ni firma de mesa.** Dirección contrasta contra `origin/main` del despacho, registra el acto externo y prepara el encargo; el merge de mesa sella la versión que se adopte. No se reservan ADR, FP, NC ni nombres de CALC nuevos.

**Principio rector:** cada ciclo entrega una medición útil y su destino verificable; ninguna cifra, firma de contador o incertidumbre sustituye la evidencia de que el modelo cambió o la tesis quedó resuelta.

## 1. Qué se conserva y qué necesita cambiar

Se conservan las seis fases, la adopción citada, la comparación primaria L↔L, el presupuesto autorizado de recaptura, la sonda lateral, la caducidad del plan y la autoridad humana. Se cambia la secuencia rígida por dependencias verificables y ciclos cortos F4→F3→emisión. El documento compañero, `PROPUESTA-SIGUIENTES-CALCULOS-GEN2-v1_0-2026-09-09.md`, desarrolla el diseño estadístico y la primera cartera de mediciones.

**Universo de esta revisión:** adjunto v1.0, árbol `631fcd78d4bf43558b9a1940afa61c753ef5e579` —main obtenido el 9/sep, incluye PR #650—, comandos `status`, `estado`, consulta `--mesa`, demanda/usos y piezas citadas abajo. Los ZIP de agosto no gobiernan este diagnóstico. No se reejecutó la suite completa ni se abrieron microdatos de caja. Las cifras siguientes son una fotografía, no nuevos umbrales de aceptación.

| Observado | Interpretación | Consecuencia para el plan |
|---|---|---|
| `status`: 5 corridas contadas, 315 ids GEN2 sellados, 1 adoptado activo, 204 dependencias numéricas legacy activas. PR #647 documenta la primera adopción y WARN 443→442. | La primera silla existe. El objetivo literal WARN=210 caducó al crecer la oferta y cambiar sus firmas. | F1 se verifica por la adopción concreta y el movimiento atribuible, no por un total fijo. |
| El #649 selló el marcador con insumos legacy. Su adjudicación `NO-DISCRIMINA → EXPLICADO-POR-METRICA` tiene la objeción material documentada en la revisión adversarial. `FP-367` separa firma y excepción E.1. | Medir, contar como GEN2 y adjudicar correctamente son hechos distintos. | F2 exige corregir o acotar la conclusión; no exige reclasificar la corrida para mover un contador. |
| PRIMERA-SILLA §7 y `NC-0072/0076` registran que los otros resultados no corresponden a una nueva ranura de probabilidad del consumidor. | F3 no puede vaciar la oferta existente mediante citas indiscriminadas. | Producir la siguiente cifra adoptable antes de exigir otra adopción. F3 y F4 se alternan por consumidor. |
| `usos.tsv.reglas_impacto` contiene ids como `tramite.mordida.discrecional`; no contiene conteos. Demanda usa `RES-*`, oferta `RESULT-*`. | `reglas_impacto > 0` y un cruce directo de ambos espacios de ids no definen una compuerta ejecutable. | Priorizar consumidores identificados y resultados compatibles; no inventar una métrica numérica sobre ese campo. |
| `NC-0024/0026/0075` conservan trabajo de motor/emisor y marcador por segmento que C0-D no ejecutó. | Una adopción no prueba por sí sola que el camino de emisión consuma el dato bajo el corte correcto. | Incorporar una comprobación de emisión, reutilizando el sucesor C0-C que dirección confirme. |
| PR #650 ya incorporó `digesto_tramite.py --mesa` y consulta por `--id`. | Parte del gobierno de pendientes ya existe. | Consumirlo; no encargar otra bandeja ni otra rutina. La lectura humana de alcance sigue siendo necesaria. |

Fuentes: [PRIMERA-SILLA](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/forense/notas/2026-09-09-GEN2-PRIMERA-SILLA-cierre.md), [status y cruces del registro](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/tools/corrida0.py#L3333), [usos](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/data/corrida0/usos.tsv), [reservas NC](https://github.com/Josanoforo/Modelado-Mexicano/blob/631fcd78d4bf43558b9a1940afa61c753ef5e579/forense/no-corrido.tsv), [PR #650](https://github.com/Josanoforo/Modelado-Mexicano/pull/650). La revisión adversarial del #649 es un insumo externo entregado a mesa; no se afirma aquí que ya esté registrada o aceptada en el repo.

## 2. Las seis fases revisadas

### F1 · La silla y las decisiones que realmente desbloquean

**Objetivo:** usar el patrón probado de adopción y despejar sólo las decisiones necesarias para la siguiente medición.

1. Verificar la primera cita y su consumidor activo. El precedente de PR #647 satisface esta pieza si sigue vigente al despacho.
2. Conciliar `FP-362`/`NC-0071`: v3 y v4 no son objetos intercambiables de firma. Para S6 se usa la versión sustantivamente vigente; la firma de contador se tramita por su propia vía.
3. Separar `FP-367` en las dos preguntas ya presentes: autorización de contador y compatibilidad con E.1. No convertirla en una barrera a leer resultados válidos como diagnóstico legacy.
4. PILOTO-SONDA sigue como trabajo lateral con presupuesto y final citado. Sólo bloquea una corrida que dependa del insumo que busca; no bloquea todas las mediciones disponibles.

**Salida verificable:** cita de oferta→consumidor validada por el mecanismo existente; cada decisión bloqueante del siguiente lote resuelta o pendiente con objeto y efecto explícitos. El número global de WARN puede subir si crece la oferta.

**Mesa decide:** firmas todavía necesarias y presupuesto de sonda. No vuelve a firmar lo ya cubierto.

### F2 · El marcador y su interpretación correcta

**Objetivo:** disponer de una comparación utilizable y de una conclusión que no exceda los datos.

1. Dirección valora y despacha la corrección sucesora del #649: ramas exhaustivas, independencia del contraste primario respecto de M, alcance separado del signo del resultado. Los sellos anteriores quedan intactos.
2. Preservar la medición actual: media d=+4.6978 pp, IC95 [−0.8022,+11.2747], n=13. Hasta la corrección, su lectura máxima es **no discrimina bajo la regla fijada**; la explicación por métrica está objetada.
3. Declarar B con su cobertura real y corte informativo. El B de dos celdas no es un piso común de catorce; mantener `NC-0079` y su sucesor sin inventar cobertura.
4. Nombrar `NC-0077` como necesidad de actualizar alcance. El corpus antiguo no se vuelve actual al cruzar cero el intervalo.

**Salida verificable:** corrida y nota sucesoras concordantes, pruebas de las ramas materialmente defectuosas y propagación con cita. La clasificación de generación se reporta como resulte de E.1 y sus firmas; no es condición para que el diagnóstico exista.

**Mesa decide:** la adjudicación corregida y el alcance de la futura tesis. Esta reparación sólo bloquea afirmaciones que dependan de la conclusión objetada; F4 puede producir tasas mientras se corrige.

### F3 · El relevo por consumidor, con emisión comprobada

**Objetivo:** convertir una medición pertinente en un cambio real de procedencia o comportamiento del modelo.

Cada lote identifica primero el consumidor activo, su parámetro y el estimando compatible. Selecciona después una oferta vigente o demanda su cálculo en F4. Si sólo se añade procedencia y el número no cambia, lo declara —como en PR #647—; eso es avance de trazabilidad, no nueva capacidad predictiva demostrada.

**Ciclo:** consumidor → spec/cálculo F4 si falta → revisión de compatibilidad → adopción → emisión de M en ese camino → evidencia de qué cambió.

La comprobación de emisión debe demostrar que el valor adoptado llega al parámetro ejecutado. Si toca datos o emisión sellados, produce sucesores. Para reglas sensibles a ola/segmento, consumir el trabajo pendiente C0-C/`NC-0024/0026` sólo en el perímetro necesario. No exigir segmentar todos los dominios para adoptar una tasa que no lo necesita.

**Salida por lote:** usos seleccionados que citan una oferta vigente, valores al grano correcto, procedencia completa y prueba dirigida de consumo. Las dependencias legacy de ese perímetro disminuyen en el número explicado; otras pueden crecer por cambios independientes y se muestran aparte.

**Mesa firma:** adopciones y cualquier cambio de estimando, regla o emisor que lo requiera. Un resultado diagnóstico puede citarse en una nota sin fingir que es una probabilidad de conducta.

### F4 · Cobertura útil, no cuota de corridas

**Objetivo:** cerrar las necesidades sustantivas del modelo y preparar el duelo que mesa decida.

Las 86 filas actuales son **demanda heterogénea**, no 86 estudios independientes pendientes de campo: contienen 14 R, 14 M, 14 L y 14 agregados, además de los demás tipos. No se usa «x de 86» como sustituto de suficiencia científica.

1. Priorizar: consumidor activo y efecto material conocido; insumo accesible; receta plausible; dependencias desbloqueadas; presupuesto. El número de reglas conectadas ayuda a ordenar, pero no mide por sí solo magnitud del efecto.
2. Ejecutar lotes coherentes: una fuente/apertura puede entregar varias cantidades compatibles, según D-15. La salida útil se adopta en F3 antes de acumular una nueva montaña sin destino.
3. Para no construibles, citar universo examinado, causa y sucesor o decisión de desistimiento. Un hueco de la fuente no convierte una regla en falsa.
4. Sonda, timbres y convenios trabajan sobre bloqueos concretos. La decisión comercial sobre tandas llega con respuesta, coste y alternativa a la vista.
5. Derivar el perímetro del Hito D **desde sus objetos y criterios canónicos**, no desde el número de resultados. Dirección debe localizar esa tabla antes de despachar: no la doy aquí por verificada ni sustituyo sus 27 objetos por las 86 demandas.

**Salida para lanzar F5:** universo de evaluación fijado; insumos requeridos por sus brazos disponibles; faltantes y exclusiones definidos antes del resultado; cobertura y precisión compatibles con el alcance de la afirmación; presupuesto autorizado. No exige completar el resto de la demanda. Si se lanza con cobertura parcial, la conclusión lleva ese perímetro.

**Mesa decide:** alcance suficiente para ese duelo, prioridades comerciales y, si hace falta, Ola 6. Dirección presenta qué afirmación se gana con cada ampliación, no sólo cuántas filas agrega.

### F5 · El duelo contemporáneo con el corpus efectivamente disponible

**Objetivo:** estimar el valor añadido de dar acceso al corpus, bajo un contrato informativo explícito.

1. **Recapturar L_SOLO y L_CORPUS en la misma ventana**, con el mismo modelo/versionado disponible, prompt base, configuración y criterio de extracción. Sesiones aisladas; orden de brazos aleatorizado o contrabalanceado, declarado antes. Comparar corpus nuevo con solo antiguo confundiría la actualización con el brazo.
2. Congelar la versión del corpus y la forma de acceso. «Todo el corpus» significa acceso al conjunto declarado, no promesa de que todos sus bytes caben en el contexto. Registrar documentos recuperados/suministrados, límites y truncamientos.
3. Elegir la pregunta: **uso del corpus disponible** o **transferencia a objetivos retenidos**. En transferencia, imponer el mismo corte permitido a L_CORPUS, M y B y excluir respuestas/arbitraje del material accesible. En uso documental, distinguir recuperar una respuesta disponible de inferir una nueva. No mezclar ambos resultados en una afirmación única.
4. M es contendiente secundario con emisión verificada. B sólo se compara en su universo compatible; ampliar B requiere su propia regla previa. No dejar que un tercer brazo cambie la adjudicación L↔L.
5. El marco histórico sirve para desarrollo y comparación histórica. Su conocimiento previo se declara. Una afirmación confirmatoria nueva necesita evaluación prospectiva sin ajustes tras ver sus resultados; si no se paga, la conclusión se limita al panel observado.

**Salida verificable:** capturas íntegras e identificadas, corpus y acceso congelados, cobertura por brazo, cálculo preregistrado, incertidumbre con alcance declarado y nota que distingue conclusión estadística, utilidad y límites. Un resultado inconcluso es una salida válida.

**Mesa firma:** objetivo, presupuesto de ambos brazos, universo, criterio de utilidad si se desea y lanzamiento. No se amplía n ni se repite selectivamente hasta conseguir el signo deseado.

### F6 · Integración e informe que resiste lectura externa

**Objetivo:** exponer qué sabemos, qué cambió en el modelo y qué sigue sin resolver.

El informe distingue descripción, asociación, desempeño predictivo y cualquier afirmación causal. Cada cifra decisiva y cada conclusión central tiene una cadena hasta una corrida identificada, spec, insumos y alcance. La muestra aleatoria se usa para revisar trazabilidad adicional; no sustituye el examen de las afirmaciones que sostienen la tesis.

**Salida verificable:** todas las afirmaciones centrales tienen evidencia pertinente y sus límites; el resto pasa una muestra fijada antes de seleccionarla; los fallos materiales se corrigen o acotan. La longitud de la cadena no es una meta de calidad por sí misma.

**Mesa firma:** informe y deudas aceptadas. Reglas y herramientas se revisan según su falsador y coste real; «aproximadamente diciembre» es una fecha de revisión, no una orden automática de retiro.

## 3. Dependencias y trabajo que puede avanzar

F1 aporta el patrón de adopción. F2 corrige la interpretación que alimentará la tesis. F4 produce por lotes y F3 adopta y verifica emisión; ese ciclo se repite mientras tenga rendimiento sustantivo. F5 necesita su contrato, las dependencias seleccionadas y presupuesto, no el cierre mundial de F3/F4. F6 puede redactar métodos y trazabilidad mientras llegan mediciones; la conclusión final espera F5.

No se deriva una única «fase vigente» como la primera incompleta: esa fórmula escondería trabajo válido simultáneo. La respuesta operativa es **hitos cubiertos con cita, frente activo, bloqueos efectivos y próximo producto**. Son categorías de presentación derivadas, no nuevos estados que compitan con FP/NC/CALC.

**Siguiente despacho recomendado:** corrección acotada del marcador y primer lote adoptable, como actos separados que pueden avanzar sin bloquearse. PILOTO-SONDA sólo acompaña al lote si hay dependencia real de su resultado. Máximo de trabajo activo: el que permita cerrar el ciclo del lote; no abrir una tanda por cada fila de demanda.

## 4. Contadores, compuertas y el comando que falta

| Señal | Qué permite afirmar | Qué no permite afirmar |
|---|---|---|
| `N_corridas_selladas` | Corridas que el registro cuenta según sus reglas y firmas | Cuántas conclusiones independientes están confirmadas |
| `N_resultados_gen2_sellados` | Ids únicos contados por la implementación vigente | Cantidad de estimandos vigentes adoptables; las sucesoras requieren resolución por corrida |
| `N_resultados_gen2_adoptados_activos` | Ofertas citadas por consumidores activos reconocidos | Que el valor haya cambiado o que M mejore |
| `dependencias_numericas_legacy_activas` | Usos que aún declaran leer legacy | Deuda científica total o relevancia de cada uso |
| Cobertura del lote y emisión comprobada | Necesidades concretas atendidas y destino ejecutable | Cobertura de todo el Hito D |

**Sustituir WARN-material como condición de cierre por «necesidades materiales del lote sin resolver».** El conjunto se congela al lanzar: consumidores y estimandos requeridos. Cada necesidad termina con oferta compatible adoptada, falta de medición pendiente, o decisión citada de aceptar/diferir el hueco. No se declara cero porque el cruce demanda↔oferta no pudo resolverse. Una correspondencia ambigua sigue visible para lectura humana.

El WARN global se conserva. Si se muestra un subconjunto material, se identifican sus resultados y consumidores, se resuelven sucesoras por `(corrida, RESULT)` y se distingue «sin consumidor demostrado» de «inmaterial». No se modifica su semántica para cumplir este plan.

**Comandos existentes, verificados en este árbol:**

```bash
git rev-parse HEAD
python tools/corrida0.py status
python tools/corrida0.py registro
python tools/corrida0.py estado CALC-0003-v4 --json
python tools/corrida0.py estado CALC-C0D-MARCADOR-v2 --json
python tools/digesto_tramite.py --mesa --sin-suite --stdout
python tools/digesto_tramite.py --mesa --id FP-362 --sin-suite --stdout
```

`registro` sin `--escribe` muestra el diff y no modifica TSV. `--sin-suite` declara que no se corrió la suite. No se presenta `demanda` como consulta inocua: su CLI deriva y escribe vistas; usarla sólo en el worktree del acto cuando corresponda.

**Pieza propuesta, todavía no implementada:** extender un derivador existente —preferentemente el digesto que ya usa la rutina— con una salida «obra»: SHA, contadores, citas de compuertas y próximo bloqueo del lote. Dirección elige la interfaz tras verificar colisiones. Debe consumir evidencias explícitas del plan/encargos y TSV; no interpretar libremente glosas para decidir suficiencia. Donde falte una cita o correspondencia, informa que requiere comprobación. Hasta existir esa extensión, los comandos anteriores son las fuentes de verificación, no se promete que ya haya un comando único de fases.

**D-14 para esa única extensión:** defecto real: F1 esperaba WARN=210 y ocurrió 442, y el conteo firmó v3 cuando v4 era la vigente. Materialidad: puede despachar un relevo incorrecto o detener uno válido. Economía: reutilizar contadores y citas en la rutina existente evita conciliaciones repetidas; dirección mide el coste de implementación frente a dos conciliaciones manuales. Si no resulta más barato, no automatiza y adjunta las salidas al despacho. Cero servidor, base de datos, nuevo planificador o motor de dependencias.

## 5. Cierre ordinario, aceptación y caducidad

Al cerrar cada lote, el ejecutor aporta cifra y destino, cambios respecto de lo pedido y reservas. La rutina existente concilia candidatos FP/NC con cita y estampa de universo; una sucesora parcial no cierra el residual. Dirección trae a mesa únicamente decisiones no cubiertas, con su contexto y qué desbloquean. El merge firma lo propagado.

**Aceptar esta versión cuando:**

1. Las compuertas F1/F2 reflejan los productos actuales, sin números objetivo heredados ni firmas supuestas.
2. Un lote puede recorrer F4→F3→emisión sin esperar a las 86 demandas.
3. Cada futura adopción tiene consumidor y compatibilidad estadística, o se declara que sólo es evidencia de informe.
4. F5 no confunde corpus con modelo/fecha y no promete cobertura o transferencia que su diseño no entrega.
5. Dirección puede mostrar evidencia de cada hito con las herramientas existentes; si ofrece un comando único, éste existe y supera el gate D-14.

**Caducidad propuesta:** revisar después del primer ciclo completo F4→F3→emisión o el 9/oct/2026, lo primero. Reemitir antes si cambia el objetivo de la tesis, si una compuerta pide una adopción sin oferta pertinente, si una sucesora invalida evidencia de salida o si dos encargos consecutivos deben contradecir dependencias del plan para avanzar. Silencio no firma ni desiste de una deuda.

## 6. Registro y despacho a dirección

Dirección debe archivar esta propuesta externa antes o junto con su lanzamiento, conforme a 0-bis/A.3, y citar su SHA de redacción. Preparar una versión adaptada al árbol: rutas vigentes, firmas existentes, alcance de C0-C, destino del Hito D y situación del piloto. Registrar las decisiones que cambien respecto de v1.0. El plan adjunto no estaba localizado con ese nombre en el árbol examinado: dirección confirma si aún falta archivarlo o si vive bajo otra identidad. No declarar consumido el plan anterior sin citar las compuertas que efectivamente se cumplieron.

**Preguntas concretas que dirección resuelve con mesa al despachar:** ¿F5 busca uso documental, transferencia o ambos como resultados separados? ¿Cuál es el consumidor del primer lote y qué habilita? ¿Qué parte pendiente de C0-C necesita ese lote? ¿Qué criterio y presupuesto justifican el alcance de F5? Las cifras observadas aquí se refrescan; no se vuelven a pedir firmas ya asentadas.
