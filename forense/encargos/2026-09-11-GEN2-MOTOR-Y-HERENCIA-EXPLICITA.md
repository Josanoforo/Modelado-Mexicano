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

---

# Adenda al encargo 18 · consumidores ya autorizados y límites pendientes

ENTORNO: NUBE
DESTINO: ejecutor actual de `acto/gen2-motor-herencia-explicita`.

**Esta adenda va dentro de 18. No lanzar una segunda tarea sobre el mismo motor.** Si 18 ya terminó al recibirla, comprobar su diff y ejecutar sólo el residual en una continuación identificada. Mantiene su contrato de autoridad, linaje, pruebas y cierre; no sustituye la dependencia de 17.

Corte comprobado: main #707, `cd92cb25acbb7b645a4b49ed180f042661d18e7e`. #700 está fusionado. #708 se fusionó durante el cierre de este paquete; main avanzó a `e7a471bf1499a096abbe58dc298f02243e885135`. Archiva `BENCHMARK-WEB-CUATRO-DECISIONES-GEN2-2026-09-11.md`; archivar el benchmark no constituye una firma. Localizar su archivo incorporado y usarlo como evidencia/propuesta con ese estado.

## 1 · S6: trasladar una limitación ya acreditada

Verificar `milpa/tramite-ola5-propuesta-v0.yaml`, entrada `salud.atencion.grave_ennvih2002`, frente a #702 y `forense/prereg-caja/S6-L16-spec-v1_5.md`. Incorporar la enmienda fechada y referencia vigente si todavía faltan. Expresar `IC-SENSIBILIDAD-LOCALIDAD-NO-DISENO-OFICIAL` donde se describe la incertidumbre existente, preservando veredicto_Bbis histórico y tier R4.4 MEDIA.

Es una corrección de alcance acreditado, no una firma de la opción A o B. FP-372 conserva su estado real; no promover conclusiones nuevas basadas exclusivamente en ese IC. NC-0156 sigue el expediente oficial que continúa 21. La decisión DIN/FP-371 es distinta y no firma S6 por extensión.

## 2 · Fintech: D10 ya está decidida

Incorporar para el contexto de R1.6 la procedencia de `CALC-ENIF-FINTECH-0001--5b92cee28946` y la propuesta de #706, comprobando identidad y contrato actual. Uso `DESCRIPTIVO-NO-CALIBRA`: cuenta 2021/2024 lado a lado sin delta no acreditado; crédito como comparación descriptiva.

No convertir 2018 NO-ESTIMABLE en cero, no inventar la categoría faltante del antecedente 2024 y no sustituir la probabilidad de R1.6 por este proxy. NC-0122 conserva su límite estructural. D10 no se vuelve a preguntar.

## 3 · Identidad documental y tandas

Corregir la etiqueta ENCIG2023 de las entradas pertinentes de NC-0106 conforme al payload ya usado; no cambia ola ni medición. Si el cambio ya entró, registrar evidencia y no repetirlo.

#700 ya puede consultarse como antecedente fusionado. Incorporar sólo lo que su autoridad permite: el escenario de tandas no se convierte en parámetro adoptado por haber fusionado código, documentación o un arreglo de CI. D18 sigue difiriendo la vía comercial; la vía académica conserva su alcance.

## 4 · Las cuatro decisiones del benchmark conservan su estado

| Objeto | Qué sí se puede terminar ahora | Qué no se da por firmado |
|---|---|---|
| DIN / FP-371 | Linaje, punto descriptivo permitido, limitación de diseño y solicitud oficial | Uso del EE/IC aproximado como referencia inferencial |
| S6 / FP-372 | Enmienda de alcance y consumo descriptivo ya permitido | Elección entre opciones de uso inferencial |
| Complemento / NC-0085 | Contrato de dependencia con el padre y rechazo fuera de universo; preservar evidencia | Adopción concreta del complemento propuesto |
| Corrupción / NC-0107 | Impedir atribuir respuestas por tipo de trámite a un evento; conservar exclusiones ya vigentes | Adopción de nueva regla o proxy como probabilidad por evento |

Si se analiza el complemento, verificar la unidad/persona y el universo exactos del padre. Una persona con un delito por miedo y otro por otra razón puede tener padre=1 y complemento=0; ese complemento no significa «tuvo alguna otra razón». Mantener dependencia y no contarlo como observación independiente.

Para corrupción, la restricción a un dominio no identifica por sí sola una probabilidad condicional por evento. La variante r2 puede estudiarse como contexto/proxy con su alcance; no promoverla silenciosamente a riesgo por evento. Si el benchmark recomienda algo más restrictivo que el contrato firmado, mostrar esa diferencia y completar la protección técnica ya autorizada. Aplicar nuevas opciones sólo cuando exista respuesta literal de mesa, registrando objeto, fecha y alcance.

## Aceptación

Tabla `decisión o límite acreditado | RESULT/fuente | consumidor | uso efectivo | prueba | cierre/residual`. S6 y fintech llegan al lugar donde se usan; el modo Gen2 no sustituye una ausencia por números legacy ni por el árbitro. Pruebas dirigidas de dominio, linaje y ausencia; ningún congelado histórico cambia.

Mantener perímetro y PR de 18, sin duplicar resolver de 17 ni evaluación de 19. Cero llamadas nuevas, cero envíos a terceros y ninguna firma científica inferida. Los encargos 20–22 aportarán fuentes, expedientes y validación; no bloquean terminar estas incorporaciones ya autorizadas.

## NO-CORRIDO / RESERVAS

- Los 191 usos legacy se re-derivaron y agruparon por causa. No se ejecutaron
  191 mediciones ni se promovieron números históricos por cuota; la ruta
  `HISTORICO` conserva su identidad y dependencias.
- `NC-0157` queda CERRADA por la consulta efectiva del contrato de 17 desde el
  emisor. `NC-0158` permanece ABIERTA: confirmación independiente y roles
  retenidos pertenecen a `GEN2-EVALUACION-SIN-FUGAS`.
- `FP-371`, `FP-372` y `NC-0156` permanecen: no se firmó uso inferencial de
  sensibilidades DIN/S6 ni se inventó diseño oficial.
- `NC-0085` permanece: se implementó el contrato del complemento ENVIPE y su
  rechazo sin firma, no su adopción científica.
- `NC-0107`/`NC-0153` permanecen: r2 sólo sirve como proxy descriptivo; no se
  obtuvo ni adoptó una probabilidad nacional por evento/canal.
- `NC-0122` permanece: D10 describe el canal del último producto entre
  tenedores fintech, no el canal exacto del producto fintech.
- El escenario de tandas no se adoptó. No se ejecutaron llamadas a modelos,
  microdatos, solicitudes externas ni cierres de PR ajenos.
