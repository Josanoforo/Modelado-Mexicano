# ENCARGO 18 · GEN2-MOTOR-Y-HERENCIA-EXPLICITA

ENTORNO: NUBE
RAMA: acto/gen2-motor-herencia-explicita
COMPUERTA: fase 1 inmediata; integrar contrato de linaje de 17 antes del cierre ejecutable.
MODELOS: cero llamadas. MICRODATOS: sólo continuación CAJA si se identifica una medición faltante.

## Resultado útil

Hacer que una salida anunciada como Gen2 sólo use parámetros con cadena y contrato adecuados, y mostrar la cobertura que realmente alcanza. Conservar el motor histórico/mixto como baseline identificado. Gen1 puede aportar arquitectura e hipótesis; sus cifras, priors, umbrales y grados de evidencia no se transfieren automáticamente.

No crear un segundo motor divergente ni reescribir todas las reglas. Reutilizar el emisor y factorizar la selección/aptitud. Es importante distinguir `milpa/src/motor.py` (rebanada matricial de estados E0) de `milpa/src/emisor.py` y `tools/emite_m.py` (emisión probabilística usada por el duelo).

## Fase 1 · Mapa del motor que se usa realmente

Partir de consumidores activos y de los recorridos ejecutables. Al corte, registro deriva 207 usos: 16 con adopción GEN2 y 191 legacy. Re-derivar, no congelar esos números como test. Cubrir cada salida activa con sus parámetros, transformaciones y antecedentes materiales; priorizar las familias CIV/TRA/FAM/DIN del duelo y las adopciones ya hechas.

Entregar una tabla reproducible `consumidor | parámetro/regla | origen numérico | fuente y RESULT | unidad/evento/universo/ola | uso permitido | condición de activación | estado`. Diferenciar los parámetros medidos, hipótesis heredadas, supuestos asignados explícitamente y metadatos de clasificación. Los 191 usos no equivalen a 191 cálculos faltantes: agrupar por causa y misma medición compartida.

Trazar lo que entra a la salida, no sólo el campo `p`: complementos, condicionales, coeficientes, reglas de selección de ola y tiers que el reporte muestre. Un RESULT actualizado no acredita automáticamente toda una regla cuyos otros componentes siguen heredados. Reutilizar `demanda/usos` y el resolver de 17; no mantener una lista manual paralela.

## Fase 2 · Emisión explícita y cobertura verificable

Agregar al recorrido vigente un modo/contrato explícito de emisión Gen2. Para producir número exige fuente/resultados aptos para el uso, dominio/evento compatibles, generación/origen trazados y corte temporal cuando aplique. Ante falta, devolver `NO_COVERAGE` con motivo; nunca rellenar con el p viejo, cero o el árbitro.

La ruta histórica/mixta permanece accesible con identidad propia y reporta las dependencias heredadas. No cambiar silenciosamente la semántica de comandos anteriores ni sus archivos congelados. Las nuevas ejecuciones que se presenten como Gen2 seleccionan el modo explícito y guardan versión/hash del motor y estado de aptitud por salida.

Una hipótesis estructural puede mantenerse como heredada mientras se evalúa. Un supuesto nuevo asignado sólo entra si su justificación y autoridad están explícitas; no se convierte en “medido”. Si la falta de definición de un supuesto cambia el resultado, entregar opciones con impacto y esperar esa decisión sólo para el componente afectado.

## Fase 3 · Selección contractual, sin consultar el objetivo para mejorar el error

Implementar para las familias realmente consumidas la selección por encuesta, año, unidad, población, evento y transformación. Usar las mejoras ya integradas en #689/#691. Incorporar el diagnóstico de #698 si sigue válido, sin convertir su sensibilidad post-hoc en evaluación nueva.

Para consulta documental de una ola exacta, una medición de esa ola puede responderla; si la misma cifra sirve luego como R, eso es verificación/recuperación, no validación predictiva independiente. Para transferencia temporal, conservar “última estrictamente anterior”, disponibilidad del dato al corte y exclusión de valores usados como árbitro; mismo año calendario no siempre prueba disponibilidad. No seleccionar “ola más cercana” ni sustituir un estimando sólo por nombre parecido.

Complementos: conservar universo y dependencia del padre; no contarlos como otra observación independiente. ENCUCI solicitud/entrega y ENCIG por evento/canal conservan contratos y reservas actuales; no imputar a un evento una respuesta disponible sólo a nivel de tipo de trámite. S6/DIN: consumir como descriptivo donde esté permitido, sin inventar intervalos oficiales ni adelantar la decisión de 16/FP-371.

## Fase 4 · Relevos por grupos de consumidores

Con lo ya medido y adoptado, producir un snapshot **nuevo** de las salidas Gen2 aptas y su cobertura. No exigir igualar las probabilidades históricas como criterio de aceptación; exigir identidad con el RESULT correcto y su contrato. No modificar el snapshot M que usó TRIADA-0002.

Para lo restante, agrupar encargos de medición sólo cuando no exista resultado apto en el repo. Fijar fuente, propósito y método antes de mirar el control histórico. No adoptar automáticamente valores de series que fueron árbitros de evaluación; separar uso operativo de uso en evaluación. Entregar propuestas de adopción nuevas con consumidor e impacto, sin firmarlas por cuenta de mesa.

Si una regla se apoya solamente en la conclusión de Gen1, dejarla como hipótesis a contrastar o excluirla del perfil que exige evidencia medida, según el contrato. No borrar conocimiento histórico ni rebajar tiers arbitrariamente. Proponer reemplazar una regla cuando falle su medición/contrato, no para perseguir un ganador.

## Fase 5 · Pruebas y cierre

Casos obligatorios: parámetro nuevo apto emite; legacy puro no se cuela al modo Gen2; regla mixta identifica sus componentes; falta de un RESULT o dominio produce NO_COVERAGE; complemento no crea independencia; elegir ola futura falla en transferencia; reetiquetar R no elimina su historia; un caso operativo legítimo sigue funcionando; cambio de p sin RESULT se detecta; el resultado histórico de F5 no cambia.

Reportar cobertura antes/después por consumidor y familia, no sólo total de RESULT. Tabla de decisiones nuevas únicamente si faltan: opciones, recomendación, efecto y dato que resolvería la elección. La meta es un motor más útil y honesto sobre lo que puede emitir, no completar un inventario por cuota.

## Perímetro y concurrencia

Emisor/selector y pruebas de consumo; metadatos mínimos en reglas activas cuando sean necesarios y no cambien una decisión científica. Sin cambios a medidores/sellos de CALC existentes. 17 posee registro/T35/vistas; 18 consume su contrato. El análisis inicial puede ir en paralelo, pero no duplicar su resolver. 14/15/16 y adquisición continúan. Coordinar cualquier edición de milpa con otras adopciones aún abiertas.

Aceptación: una salida Gen2 no usa números heredados silenciosamente; herencia estructural queda visible; snapshot nuevo con linaje y cobertura; el operador distingue consulta/transferencia/baseline; deuda restante agrupada en relevos concretos. La falta de corpus en Cloud deja una continuación CAJA exacta, sin impedir entregar el código y las emisiones ya acreditables.

## Contrato de ejecución, incluido para usar este archivo por separado

**Autoridad y lanzamiento.** La mesa pidió comprobar los candados GEN1→GEN2 y ajustar Gen2 aun si exige trabajo más robusto. Este encargo concreta esa solicitud; al entregarlo al ejecutor autoriza el perímetro descrito, commits, push y PR propio. El merge sigue siendo de mesa. No concede nuevas adopciones científicas, gasto de modelos ni una declaración de superioridad. Las decisiones previas válidas se conservan; una firma de contador no certifica independencia numérica.

**Arranque.** Lee `AGENTS.md`, este encargo completo, `.claude/commands/acto.md` y sólo las instrucciones sustantivas pertinentes. Reporta ruta absoluta, rama, HEAD y `git status --short`. Consulta main, PR y ramas por objeto para evitar duplicados; usa worktree propio. Archiva por el 0-bis vigente. El corte de preparación fue main #694, SHA `4816101e506f527d018dd2c47467a8b57bfbd487`, con #695–699 abiertos. Revalida únicamente cambios posteriores que afecten tu perímetro. Los ZIP de agosto son historia, no la base operativa.

**Integración.** Deriva ADR/NC/FP al cerrar, sin reservar números; quien integra después renumera y concilia sólo sus filas. Conserva filas ajenas por identidad y significado. Usa `tools/cierre_acto.py` según el procedimiento vigente, primero en seco; deja una sola ancla L0. No cambies `/despacha`, cierres PR ajenos ni borres worktrees. Actualiza las vistas globales sólo donde se autoriza expresamente; jamás reemplaces un TSV por una copia vieja. Los merges se serializan.

**Datos e historia.** Cloud trabaja código, documentos y agregados. Microdatos sólo en CAJA, con raíces y hashes del manifiesto. No reescribir specs, scripts, snapshots, capturas, resultados ni sellos congelados: usa sucesoras y enmiendas de alcance. Un control histórico no selecciona receta, filtro, ponderador ni variante por cercanía. Recalcular sobre la misma muestra puede ser trabajo GEN2, pero no es automáticamente evidencia independiente. Procedencia, reproducción, validación, adopción y uso en evaluación son estados distintos.

**Perímetro administrativo.** Encargo archivado, nota de cierre, filas directamente afectadas de decisiones/no-corrido/firmas/cola y cascada existente en gobernanza/estado/rótulos. No crear otra plataforma de gobernanza, base de datos o coordinador de tareas. Automatiza sólo defectos materiales reproducidos y con mantenimiento menor que el coste de repetición.

**Pruebas y cierre.** Pruebas materiales dirigidas, baseline requerido y diff final. No reparar fallos históricos ajenos para obtener una suite cosméticamente verde. Las pruebas adversariales adjuntas documentan defectos: después del arreglo sus salidas deberán cambiar según el contrato, no preservarse como oráculo del comportamiento correcto. Ninguna prueba escribe sobre el árbol científico real. Entrega `obligación | evidencia | consumidor/alcance | cierre o residual` y PR/HEAD. Una reserva mixta conserva su residual. No cerrar por nombre coincidente, sello o firma de contador solamente.

Continúa entre fases autorizadas. Ante una decisión científica nueva, prepara opciones concretas y termina las fases independientes; no conviertas una recomendación en firma. Cero llamadas nuevas a modelos y cero envío de solicitudes a terceros en estos tres encargos.


**Actualización comprobada al cierre:** main avanzó a `a63fd4ccc40204cf5215d466a593b4e1491bdda6` por #699 y #696. No cambió el código objeto de las sondas. 09 ya está fusionado: partir de sus vistas y no repetir su publicación. 14–16 están encolados por #699. Esta actualización prevalece sobre referencias de coordinación redactadas al corte inicial.
