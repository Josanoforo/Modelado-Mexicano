# ACTO GEN2-ADQUISICION-CONTINUA-2 · Presupuesto real y continuación productiva

**SHA de redacción:** `e8d44b78e7817724767febd945f4e6431708b01a`, después de #777, #780 y #778.
**Entorno asignado:** CAJA, Codex CLI, Windows/WSL, corpus montado; no requiere Claude Opus.
**Estado:** CONSUMIDO por PR #782 (sin fusionar al cierre operativo).
**CONTADOR:** cero mediciones previstas; adquisiciones y reducción de brechas se reportan por separado. Ninguna adopción científica nueva autorizada.

## ARRANQUE

Worktree propio desde `origin/main`; reportar ruta absoluta, rama, HEAD y estado. Leer `AGENTS.md` y este encargo completos, conservar modificaciones ajenas —especialmente staging y corpus— y ejecutar sólo el delta pertinente contra el runtime productivo.

## VERIFICACIÓN DE EXISTENCIA

1. **Estructura:** existe un único servicio con Windows Task Scheduler, `tools/adquiere_launcher.sh`, `tools/adquiere_cron.sh`, `tools/adq_investigacion.py`, almacenamiento runtime gitignorado y lock único. No se crea scheduler, base de datos, índice ni capa de control adicional.
2. **Contenido:** contra `origin/main` `81c7f63e9a49805fb4c5d48031de2339516d7011`, el ledger todavía suma la reserva completa a `usado` y no contiene liquidación. El runtime `/home/pc0/mm-adq` conserva la reserva `1/5/3900` de `2026-09-15T104704-88296`; los logs acreditan una investigación, cero objetos/intentos y una ventana del hijo de 10:47:29 a 10:51:16.
3. **Cobertura retroactiva:** #777 sí conectó demanda/guardia/comprobación/presupuesto, #780 sí dejó la frontera de ahorro en continuación para 16/sep y #778 sí publicó el recibo y su primera corrección. Ninguna pieza posterior a la redacción liquidó reservas ni habilitó otra activación útil el mismo día. El encargo sigue materialmente vigente.

## LANZAMIENTO ARCHIVADO (Jonás, 15 de septiembre de 2026)

### Resultado encargado

Evitar que una ejecución corta consuma ficticiamente todo el presupuesto diario. Conservar los límites, liquidar reservas contra trabajo real, recuperar el cupo acreditablemente no utilizado y ejecutar una continuación útil mediante el servicio desplegado.

El resultado debe permitir que otra activación del mismo día atienda trabajo elegible con presupuesto remanente. Las pruebas verdes y una corrección del texto del recibo no bastan.

Este documento prepara el encargo. Las autorizaciones operativas de abajo se activan al recibir el prompt de lanzamiento de Jonás; no acreditan que la ejecución ya ocurrió.

### 1. Premisas verificadas; no repetir la revisión general

- #777 integró demanda independiente del cierre de NC, guardia efectiva, comprobación horaria y presupuesto diario.
- #780 dejó `DEM-AHORRO-STOCK-DURACION-01` en continua, con frontera pública concreta y revisión el 16/sep. La pausa hasta octubre ya está corregida.
- #778 publicó el recibo `2026-09-15T104704-88296`: `adq-codex-5`, Codex invocado, una investigación, duración del runner 250 s, cero objetos y cero bytes nuevos.
- La enmienda `[ADQ-CORRECCION]` del mismo recibo reconoce remanente `2/0/0s`. El texto previo `3/5/3900s` era una lectura anterior a la reserva.
- `adquiere_cron.sh` reserva `MAXIMO_FILAS` y `TIMEOUT_EJECUTOR` antes del hijo; `adq_investigacion.py::reserva_presupuesto()` los suma a usado. En el corte revisado no hay liquidación que devuelva lo no utilizado.
- Los tres consumidores `RES-0046/0048/0065` ya aparecen `PENDIENTE_DATOS_O_DECISION_DE_USO`, no disponibles y asociados a la demanda independiente. Preservar esa corrección.
- Los 62 archivos «nuevos» del censo significan no registrados en ese censo; no son 62 adquisiciones del ciclo.

Revalidar únicamente estos puntos contra `origin/main` vigente y el runtime real. Si otro cambio ya resolvió una pieza, aprovecharlo y ejecutar sólo el delta. Los ZIP de agosto no son autoridad para esta tarea.

### 2. Decisiones operativas incluidas en el lanzamiento

- Mantener el techo diario de 3 investigaciones, 5 objetos y 3,900 segundos de ejecutor, con la gracia de terminación vigente identificada por separado. El cupo se comparte entre activaciones automáticas y manuales del servicio; no se reinicia por rama, worktree ni despliegue.
- Reservado no significa consumido. Descontar las reservas activas para proteger el techo; al terminar, consolidar el consumo acreditado y devolver el resto, una sola vez por `run_id`.
- Contar trabajo iniciado, no sólo éxitos: una investigación realizada consume su unidad aunque no encuentre fuente; un objeto realmente intentado consume cupo aunque su descarga falle. No cobrar como intentados cinco objetos que sólo eran capacidad máxima. Una continuación en un hijo posterior consume otra unidad de investigación; no habilitar reintentos ilimitados de un mismo objeto por deduplicación.
- Medir tiempo del proceso ejecutor desde fuera del LLM. El recibo de 250 s corresponde al runner: no asumir que son exactamente 250 s de hijo. Medir con reloj monotónico en nuevas ejecuciones; no aceptar duración inventada en la respuesta del modelo.
- La investigación puede continuar si quedan unidades de investigación y tiempo aunque el cupo de objetos sea cero; en ese caso no descarga. La adquisición de objetos ya elegibles puede continuar si quedan objetos y tiempo aunque el cupo de investigación sea cero. Ninguna dimensión agotada debe paralizar trabajo que no la necesita.
- Autorizar una continuación anticipada y única de la frontera pendiente de ahorro, sin esperar al 16/sep, si queda cupo acreditado. Registrar esta decisión como motivo de reprogramación en el mecanismo existente. No falsear fecha, cerrar/reabrir `NC-0126`, cambiar artificialmente la versión de pregunta ni borrar su historial. Si ya venció o se atendió, seguir la agenda actual sin repetir trabajo.
- Una fuente pública que reduzca materialmente la incertidumbre puede adquirirse como documentación o evidencia parcial aunque no habilite todavía el uso final. No exigir demostrar el reactivo exacto antes de descargar el cuestionario que permitiría comprobarlo. Conservar identidad, integridad y límites de uso; no descargar archivos irrelevantes para producir un contador positivo.

Estas decisiones precisan la contabilidad operativa del encargo anterior; no aumentan su presupuesto ni cambian el estimando científico.

### 3. Perímetro y método

Perímetro principal: `tools/adq_investigacion.py`, `tools/adquiere_cron.sh` y sus pruebas dirigidas. `tools/adq_doctor.py`, `tools/adquiere_launcher.sh`, configuración e instalador Windows sólo si hacen falta para conectar o desplegar. Instrucciones de `/adquiere`, runbook y guía de tarea sólo en los párrafos modificados. Runtime, recibos, estado de investigación y proyección derivada usando sus escritores. Si aparece evidencia pertinente: corpus, manifiesto y relaciones/cola mediante mecanismos canónicos. Un encargo archivado, nota breve de cierre y asientos mínimos.

No modificar `milpa/`, `CALC`/specs/resultados sellados, adopciones, F5/F6 ni decisiones científicas. `NC-0195` y otros frentes de medición no son dependencias. No incorporar PR abiertos ajenos.

#### P1. Corregir reserva → ejecución → liquidación

Reutilizar almacenamiento runtime y lock de una instancia. Mantener estado mínimo por ejecución para distinguir reserva activa, consumo consolidado y recuperación pendiente. Escritura atómica y liquidación idempotente; sin base de datos ni segundo scheduler.

Integrar liquidación en el cierre real antes de publicar remanente, con éxito, error, timeout, fallo de autenticación o publicación. Si el hijo nunca arrancó, devolver lo no usado. Si trabajó y falló publicación, conservar cargo y reintentar publicar sin repetir trabajo.

Ante caída abrupta, no liberar reserva de proceso vivo. En siguiente activación recuperar sólo huérfanas con evidencia suficiente. Si falta evidencia, conservar provisionalmente la parte incierta y explicar acción; no resetear el día ni transportar incertidumbre a otros días. Imputar a fecha de reserva en zona configurada aunque cruce medianoche.

El límite y el informe deben concordar. Preservar checkpoints de intentos aunque el hijo termine sin JSON final; una declaración incompleta del LLM no vuelve consumo cero.

#### P2. Recuperar cupo real y encadenar siguiente activación

Consultar runtime productivo. Para `2026-09-15T104704-88296`, usar eventos/logs/recibo; mantener investigación realizada y devolver objetos no intentados. Para tiempo usar duración del hijo si existe; si sólo runner, admitirla como cota conservadora y declararla. No reconstruir todo historial ni alterar recibos: añadir enmienda enlazada al `run_id`.

Recalcular con las demás ejecuciones intactas. Si el día pasó, resolver compatibilidad sin transportar crédito. No borrar ledger, inventar `run_id` ni liberar reservas ajenas vivas.

Comprobar que siguiente activación ve remanente y despacha sólo dimensiones con cupo. Separar: sin trabajo elegible, espera con fecha/ruta, presupuesto agotado y reserva pendiente.

#### P3. Desplegar y producir continuación útil

Preparar, probar, publicar PR y desplegar SHA remoto exacto del correctivo sobre la misma tarea Windows. Autorizado antes del merge; no fusionar. Registrar revisiones de launcher y runner. Cambio funcional posterior exige redespliegue; nota documental posterior no obliga a repetir investigación.

Aplicar continuación autorizada mediante tarea existente. Prioridad: cuestionario o catálogo público de variables de `MEX_2012_FCS`; comprobar tenencia/ausencia de ahorro y duración financiable del mismo stock. Continuar desde cursor, sin búsquedas generales ni familias agotadas.

Si hay documento/dato pertinente, adquirir, comprobar hash/tamaño/legibilidad y registrar contribución/límite. Un cuestionario puede reducir brecha sin microdatos. Si no aporta, conservar negativo acotado y pasar a siguiente ruta plausible o necesidad atendible con cupo.

Tras dos ciclos sin avance material, hacer visible propuesta de uso acotado de #772 o siguiente decisión científica. No ejecutar relabel ni bloquear otros objetos.

Acreditar presupuesto antes/reserva/consumo/remanente. Ejecutar segunda activación normal: continuar trabajo elegible o emitir razón correcta sin modelo. No fabricar necesidad.

Una activación manual prueba el recorrido, no un disparo horario. Verificar configuración/próxima activación y adjuntar evento automático si ocurre; si no, dejar observación puntual pendiente sin retener PR.

### 4. Aceptación mínima

| Caso | Resultado exigido |
|---|---|
| Reserva 1/5/3900, ejecuta 1 investigación, 0 objetos y 250 s de hijo | Consumo 1/0/250; disponible 2/5/3650; segunda liquidación no cambia. Fixture, no reinterpretación del recibo histórico. |
| Segunda activación mismo día | Comparte ledger y usa remanente sin exceder techo. |
| Arranque fallido / timeout / huérfana | Devolución o cargo según evidencia; sin doble devolución ni proceso vivo liberado. |
| Publicación fallida después del trabajo | Consumo cargado; publicar después no repite investigación/descarga. |
| Una dimensión agotada | Investigación/adquisición independiente sigue si sus recursos alcanzan. |
| Producción | SHA desplegado, continuación real, liquidación visible y segunda activación explicable. |

Conservar guardia/demanda de los tres consumidores bloqueados. Ejecutar primero pruebas de presupuesto, continuidad y cierre; instalar dependencias declaradas faltantes. Comparar fallos con baseline; no limpiar suite completa.

### 5. Entrega y regla de parada

PR principal pequeño, nota de cierre y recibos. Si el servicio genera PR automático, enlazarlo; no duplicar implementación. Mesa fusiona.

El cierre empieza con: necesidad/evidencia y objetos/bytes/intentos separados; brecha reducida/uso; tabla de presupuesto antes/reservado/consumido/devuelto/disponible/próxima acción; PR/HEAD, SHA desplegado, `run_id` y segunda activación; sólo reservas materiales pendientes con acción concreta.

El correctivo termina al demostrar liquidación/continuidad. La disponibilidad del instrumento es resultado científico distinto: no fabricar adquisición ni mantener abierto el software hasta encontrar datos inexistentes. Si falta host/red/recurso, entregar implementación y comprobación pendiente exacta sin declarar producción completa.

La respuesta a «¿quedó más cerca de producir una explicación, medición, decisión o modelo mejor?» debe apoyarse en cupo recuperado utilizable, continuación ejecutada o evidencia pertinente, no en documentos/pruebas.

### Prompt de lanzamiento

> Ejecuta íntegramente ENCARGO-GEN2-ADQUISICION-CONTINUA-2.md en CAJA como continuación del servicio existente. Autorizo las decisiones operativas del encargo: liquidación del presupuesto sin elevar sus techos, recuperación sustentada del cupo no usado y una continuación anticipada de la frontera pendiente de ahorro dentro del remanente. Autorizo cambios delimitados, pruebas dirigidas, commits, push, PR, despliegue del SHA publicado y activaciones de la tarea existente para demostrar continuidad. Los merges quedan conmigo. No detengas el trabajo por firmas de tareas reversibles ya cubiertas; eleva sólo decisiones científicas nuevas o accesos realmente no autorizados. Conserva el trabajo ajeno y entrega evidencia del consumo real, la siguiente activación y la brecha atendida. No autoriza compras, contacto a terceros, privilegios nuevos ni cambios a evaluaciones o resultados sellados.

Referencias del corte: implementación #777; investigación/continuación #780; recibo/corrección de presupuesto; reserva/despacho; wrapper ejecutor; cursor vigente de ahorro.

## NO-CORRIDO / RESERVAS

Ninguna parte material quedó sin correr. La observación del próximo disparo
horario automático permanece puntual y no condiciona el cierre: la continuidad
ya se demostró con dos activaciones de la tarea existente.

## CONSUMIDO

Ejecutado el 15 de septiembre de 2026 por el PR principal #782. La evidencia
de liquidación y primera continuación está separada en #783 y #784; la mesa
conserva la decisión de fusión.
