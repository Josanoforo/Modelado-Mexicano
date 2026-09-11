# ENCARGO · GEN2-ENIF-POBLACION-Y-ADOPCION

## A/A → no trabajadores → uso poblacional

Fecha de preparación: 10 de septiembre de 2026. Corte verificado: `486eda19944a94d978791eb423559144de98d16b` (merge de #685).

**Destino:** CLI con microdatos. Cloud puede preparar spec, código y fixtures y dejar continuación en la misma rama. **Integra:** E05; D04 A/A y D05 A+B; NC-0124/0126/0128. **Rama:** `acto/gen2-enif-poblacion`.

## Resultado y perímetro

Adoptar el concepto GEN2 elegido y medir la celda adicional de no trabajadores, conservando el cálculo anterior. Leer `data/corrida0/CALC-ENIF-0001/`, `forense/encargos/2026-09-09-GEN2-LOTE-ENIF-1.md`, su nota de cierre, cuestionario, manifiesto, consumidores y decisión #685. Editar nuevas specs/medidores/resultados ENIF, consumidores exactos y procedencia. No hacer un segundo lote ENIF completo ni modificar la definición histórica.

**Observado:** A/A y la celda adicional están autorizadas. **Interpretación:** falta ejecución/adopción, no volver a votar los cortes. **Consecuencia:** priorizar reutilización del CALC sellado cuando mida exactamente A/A.

## Fase 0 · Correspondencia y reuso

Verificar etiquetas literales de P4_10 {1,2}, seguridad social P3_13 {1..4} frente a {7}, y grupos residuales. Comparar con CALC-ENIF-0001 y sus RESULT. Si la estimación ya coincide y tiene evidencia válida, reutilizarla. Si cambian fuente/universo/codificación, declarar la diferencia y crear sucesora.

No desagregar “sin ahorro” de una categoría que lo combina con un horizonte mínimo. NC-0126 es una limitación del instrumento: mostrarla, no inventar una tasa más fina.

## Fase 1 · Spec de la celda no trabajadora

Examinar saltos del cuestionario: población a la que se pregunta ahorro, definición de no trabajador, códigos válidos, ponderador y diseño. No responder P3_13 por imputación. Definir un dominio independiente para no trabajadores y el alcance exacto que puede medir.

Si se quiere presentar la población total, construir una partición que incluya también residuales entre trabajadores y faltantes; trabajadores con/sin SS más no trabajadores podrían no agotarla. Publicar masas ponderadas y cobertura. El total, si es estimable, combina por masa poblacional y covarianza, no promedia tasas de celdas.

**Compuerta:** spec congelada, fuente disponible y dominio definido. Si el desenlace no existe para no trabajadores, documentar el salto y remitir una demanda precisa al lote 06; conservar las adopciones A/A que sí puedan hacerse.

## Fase 2 · Medir y verificar

Implementar el nuevo estimador en el mecanismo corrida0. Probar numeradores, denominadores, pesos, grupos disjuntos, categorías de no respuesta y soporte del diseño. Ejecutar preflight, run y verify. Comparar contra el resultado ya disponible sólo donde los estimandos coincidan.

Preservar dependencia entre tasas/complementos y los IC por el método elegido. No convertir un diseño aproximado en exacto para que el código termine. Si hay una reserva material, acotar el uso y mantener el punto donde sea válido.

## Fase 3 · Adopción y cierre

Actualizar consumidor y procedencia con etiqueta nueva, universo, RESULT y decisión D04/D05. Coordinar etiquetas/compatibilidad con lote 02. Mantener histórico B/B identificable y sin sustitución silenciosa. Un parámetro A/A no es automáticamente útil para toda persona del motor; aplicar su dominio.

Entregar tabla en lenguaje de negocio: qué personas representa cada tasa, cuáles faltan y qué decisión del motor alimenta. Capturar evidencia estructurada del verify para lote 08. Cerrar NC-0124 al propagar la adopción; NC-0128 sólo con celda medida o no estimabilidad demostrada y tratamiento explícito; no cerrar por haber redactado la spec.

**Validación final:** cálculo reproducible o reuso sustentado, históricos intactos, cobertura poblacional sincera, consumidor correcto. No hace falta un automatismo nuevo: extender los medidores/registro existentes. Cualquier helper adicional debe justificar D-14 con defecto observado, efecto y costo menor.

## Contrato de ejecución incluido en este encargo

Este archivo es autocontenido. Su fuente de autoridad es la instrucción de mesa registrada en `forense/encargos/2026-09-10-MESA-CONCILIACION-E01.md` y la solicitud posterior: «dame los siguientes encargos, multi encargos, multifase, para correr en codex cloud o codex cli». E01 y el diagnóstico #684 ya están fusionados: no repetirlos.

**Alcance del despacho:** implementar las fases autorizadas, hacer commits y presentar el resultado en una rama/PR propios para revisión. El merge pertenece a mesa. No ejecutar otro encargo, hacer merges automáticos ni cerrar PR ajenos. Si la plataforma publica el PR por una acción propia, preparar la rama y el contenido para esa misma entrega; no duplicar el PR.

**Arranque obligatorio y corto:** informar ruta absoluta, rama, HEAD y `git status --short`; leer `AGENTS.md` y este archivo; consultar origin/main y PR/rama con el mismo objeto. Reutilizar o continuar el trabajo compatible. Usar un worktree propio, sin limpiar ni cambiar la rama de otra ejecución. Archivar este encargo por 0-bis A.3 antes de modificar el objeto. Las rutas aquí son las verificadas al corte: resolver renombres y colisiones sin reconstruir toda la historia.

**Fases:** avanzar a la siguiente cuando se cumpla su compuerta objetiva; no pedir confirmación entre fases ya autorizadas. Si una depende de caja, credenciales personales, datos ausentes o una decisión científica no tomada, completar el resto y entregar el punto exacto de continuación. No llamar “terminado” al encargo entero si sólo quedó preparado en Cloud. El destino depende de capacidades comprobadas, no del nombre del producto.

**Perímetro administrativo común:** archivo de este encargo, nota de cierre, sus filas FP/NC/cola, referencias de decisiones y cascada vigente en `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_12.md` y `canon/registro-rotulos.tsv`. Cada sección añade archivos sustantivos. Conservar los IDs históricos E02–E11 como antecedentes y apuntarlos al lote correspondiente; no crear una segunda obligación por cambiar el nombre del encargo.

**Cambios concurrentes:** el perímetro es propio aunque otros lotes avancen. Antes de integrar, actualizar con main y reconciliar sólo colisiones de IDs, registros y archivos compartidos del propio acto. No copiar una versión antigua del TSV completo. No relajar el candado del despacho automático. Las entradas congeladas de un experimento se resuelven por versión/hash aunque el árbol avance.

**Medición:** reutilizar resultados sellados cuando coincidan estimando e insumos; para un cálculo nuevo, congelar spec y método en un commit anterior al primer resultado. Resolver datos por manifiesto/raíz configurada; no inventar `/home/...`, no subir microdatos restringidos ni credenciales. Registrar unidad, universo, ponderador, exclusiones, incertidumbre y uso. Los cambios a código usado por un sello exigen preservar su reproducción por la vía existente o crear una sucesora explícita; no romper históricos para modernizar una herramienta.

**Objeto de firma al merge:** propagación de las decisiones de mesa citadas y de los resultados del encargo. Para CALC científicos nuevos, aplicar `cuenta_gen2=SI` con objeto y cita explícitos conforme al contrato vigente; los sucesores técnicos no inflan mediciones independientes. Contar no equivale a adoptar: sólo se activa en el motor lo autorizado por la decisión concreta y sustentado por su evidencia.

**Pruebas y cierre:** validar primero el riesgo material; ejecutar el gate requerido sobre la integración, sin limpiar deuda ajena ni cambiar baseline. Revisar `git diff` después de las pruebas; nunca incorporar con `git add -A` una derivación accidental. Mientras NC-0141 siga viva, registrar y preservar cualquier cambio previo del usuario antes de aislar efectos de la suite; no restaurar a ciegas sobre trabajo ajeno.

Cada fase termina con resultado o bloqueo preciso y prueba. Cierre completo: autorización → resultado/cambio → evidencia → consumidor, si aplica → FP/NC → vistas/cola → PR y merge. Una decisión firmada no cierra una ejecución pendiente. Registrar fecha real, cita y universo; nada se borra ni se rejuvenece por traslado. Si falta una pieza, usar el vocabulario vigente y sucesor concreto.

**Formato final del ejecutor:** resultado útil en cinco líneas; fases realizadas/pendientes; PR y SHA; pruebas; tabla `obligación | evidencia | cerrada/residual | siguiente acción`. No parar en un inventario cuando el entorno permite ejecutar. No continuar por inercia después de satisfacer el resultado.

---

## NO-CORRIDO / RESERVAS

- `P4_10=1` combina «menos de una semana» y «no tiene ahorros» ·
  `NO-VERIFICABLE-AQUÍ` · ninguna tasa puede desagregar ambos componentes;
  `NC-0126` sigue ABIERTA · sucesor: `SIN-ASIGNAR`, requiere otro reactivo.
- Vistas corrida0 (`corridas.tsv`, `resultados.tsv`, `usos.tsv`) ·
  `DIFERIDO-A:GEN2-PRUEBAS-LIMPIAS-Y-REPLAY` · el candado `NC-0094` detectó
  32 transiciones ajenas y escribió cero vistas; el CALC, demanda y evidencia
  fuente sí quedan versionados · sucesor: `ENCARGO-E08` / `NC-0154`.

## CONSUMIDO

PR #691, rama `acto/gen2-enif-poblacion`; commits de arranque y sustancia
`7ccdb8a`, `5f5469b`, `c11e0c7`, `88bd2e6`, `d69d3b7`.

Resultado: D04/D05 ejecutadas; celdas A/A exactas reutilizadas de
`CALC-ENIF-0001`; `CALC-ENIF-0002` sellado y reproducido para no trabajadores;
motor y procedencia adoptados por dominio; B/B conservado como histórico.
`NC-0124` y `NC-0128` cierran; `NC-0126` permanece abierta. `NC-0154` registra
la única pieza diferida: publicación global de vistas corrida0 por lote08,
después de que el candado NC-0094 impidiera 32 transiciones ajenas.

Validación: prueba dirigida 2/2; spec-check 8 OK/0 FAIL; preflight VERDE;
run exit 0; verify REPRODUCE/CONTEXTO=IDENTICO 59/59; smoke del emisor por tres
dominios; `tests/check.py --baseline` exit 0; `git diff --check` limpio. El PR
queda abierto para mesa; el ejecutor no lo fusiona. Colisión conocida con PR
#687 tomó los candidatos ADR-455/NC-0152; este acto renumeró a ADR-456/NC-0153; PR #688, #690 y #689 ocuparon después ADR-456 a ADR-458 y este acto renumera finalmente a ADR-459/NC-0154.
