# ENCARGO · GEN2-SONDA-CRON-PRODUCCION-POST693

ENTORNO: CAJA
COMPUERTA: PR #690 y PR #693 fusionados; verificar duplicado del lote 07 antes de abrir rama.
RAMA: acto/gen2-sonda-cron-produccion
MODELOS: Codex implementa; el runner productivo conserva su ejecutor configurado.

## Resultado útil y continuidad

Terminar el **lote 07 que no aparece ejecutado en los merges #687–#693**: una configuración común y evidencia de disparo, publicación y recuperación en Windows/WSL. Este documento lo actualiza; no crea una segunda tarea si hay ejecución local o PR del mismo objeto. Continuar esa rama y su encargo compatible.

Antecedente obligatorio: `forense/encargos/cola/2026-09-10-GEN2-POST-685/07-GEN2-SONDA-CRON-PRODUCCION.md`. D19 ya autorizó unificar; no volver a pedir esa firma. NC-0114/0115/0120 siguen abiertas. El cron legado ya se retiró en #668; comprobar el estado instalado sin reabrir esa decisión.

## Fase 1 · Configuración única

Leer `data/adq-config.yaml`, `tools/adq_config.py`, `tools/adq_doctor.py`, `tools/adquiere_cron.sh`, `tools/windows/instala-tarea-adquisicion.ps1`, T31 en `tests/check.py`, pruebas `test_adq_*` y runbook vigente. Conservar 07:30 America/Mexico_City y la periodicidad vigente; hacer que instalador, runner y doctor/T31 lean una sola autoridad.

Resolver la traducción Windows/IANA y días sin depender accidentalmente de la zona del host. Incorporar `claude_kill_after_segundos` con default compatible de 60 s, validación y precedencia de override. Distinguir timeout del proceso, gracia TERM→KILL y ventana de observación. Configuración inválida o degradada informa causa y valor aplicado.

Pruebas focalizadas: consumidores coinciden en próxima hora, cambio de día/zona, configuración inválida, override, proceso aislado que ignora TERM. No matar un proceso ajeno ni repetir todos los fallos históricos reparados.

## Fase 2 · Verificar e instalar en la caja real

Exportar/leer la tarea existente, identificar ruta/SHA, distribución y usuario WSL, argumentos, zona, calendario y política StartWhenAvailable. Revisar tareas/runners activos antes de probar. Actualizar sólo lo autorizado y conservar reversión. No sumar otro scheduler. Si el canal Operational requiere elevación, preparar el comando exacto y dejar al operador la acción que el SO exija; no fingir que el log quedó habilitado.

Codex CLI como ejecutor del encargo **no migra** el cron desde Claude. Comprobar la disponibilidad del cliente configurado y sus límites antes de la prueba real. La F5 ya terminó; no gastar nuevas capturas experimentales. Si el ejecutor productivo no está disponible, completar configuración, fixtures y correlación del scheduler hasta el punto alcanzable, dejando separado el residual de adquisición. No declarar producción validada con un stub.

## Fase 3 · Disparo y recuperación

Correlacionar evento Windows, instancia, inicio WSL, run_id, SHA, log, heartbeat y recibo publicado. Diferenciar manual, prueba programada y producción. Se permite un disparo controlado próximo preservando/restaurando el calendario productivo cuando sea apropiado. No reconstruir sin evidencia cuál disparador produjo el censo antiguo.

Probar recuperación de hora perdida sin reiniciar ni suspender el equipo mientras corren cálculos del usuario. Una tarea aislada acredita el mecanismo sólo con ese alcance; la atribución de producción necesita evidencia de la tarea real. StartWhenAvailable=True o un lanzamiento manual no acreditan recuperación observada. Si la observación requiere esperar el siguiente horario, dejar instrumentación y receta exactas; no mantener una sesión bloqueada horas ni inventar éxito.

Fixtures de doble lanzamiento, red, ejecutor indisponible, timeout y publicación deben dejar resultados distinguibles. Usar infraestructura ya disponible y un único intento productivo suficiente; evitar pruebas repetidas que gasten uso del cliente.

## Fase 4 · Demanda hasta recibo

Validar una demanda real de adquisición, preferentemente NC-0153 si el encargo de corrupción ya la enrutó. Si no, usar una demanda elegible existente sin esperar ese merge: el cron no depende científicamente de ella. Demostrar selección o diferimiento con causa y recibo. No clasificar como fallo de cron la inexistencia de una tarea elegible.

Fechas indeterminadas de intentos: excluirlas de reintento automático hasta conciliarlas, siguiendo la autorización y política vigentes; no convertir “intento pendiente de conciliar” en “nunca intentado”. Corregir sólo el residual si todavía se reproduce. No enviar correos, DUA o solicitudes institucionales ni aceptar términos en nombre del usuario.

## Fase 5 · Cierre con alcance real

NC-0115 cierra por código integrado que usa la configuración única. NC-0114 cierra sólo cuando la correlación exigida esté acreditada; NC-0120 mantiene residual si falta elevación u observación real de recuperación. Actualizar el lote 07 original en cabecera/bitácora y ligar esta continuación, conservando su cuerpo.

Entregar instrucciones ejecutables de instalación/verificación, evidencia breve del ensayo y de producción, y una línea de siguiente acción para lo externo. No repetir el diagnóstico entero de SONDA ni prometer adquisición diaria sólo porque el instalador pasó.

## Perímetro y aceptación

Archivos de configuración/runner/doctor/instalador/T31 y tests citados, recibos/runbook, cabecera del lote 07, filas NC/cola propias y administración común. No medidores, motor ni vistas corrida0. Coordinar filas de adquisición con encargo 11; usar siempre el registro canónico y su writer.

Aceptación: una autoridad de calendario y gracia; disparo con versión y resultado atribuibles; fallos explícitos; recuperación observada o residual delimitado; ninguna afirmación de producción basada sólo en fixtures. Cloud puede preparar Fase 1, pero el cierre operativo requiere Windows/WSL.

## Contrato común, incluido para ejecutar este archivo por separado

Autoridad: decisiones de mesa asentadas por #685 y solicitud de preparar los siguientes encargos después de los merges. Este documento es un encargo preparado por ChatGPT: se ejecuta cuando mesa lo entregue a Codex. No convierte recomendaciones metodológicas pendientes en firmas. Base consultada: `origin/main=e76f3a1d476049d0c7adcba87535e60f507c8d91`, 11/sep/2026 UTC. Los merges ocurrieron la noche del 10/sep en México. `main` acredita lo consolidado; un PR abierto acredita trabajo en curso.

**Arranque y autorización operativa.** Lee `AGENTS.md`, este archivo completo, las instrucciones vigentes y `.claude/commands/acto.md` en lo aplicable; Codex ejecuta sus comandos equivalentes sin necesitar Claude. Reporta ruta absoluta, rama, HEAD y estado. Usa un worktree propio desde el clon existente; consulta main, ramas, worktrees y PR del mismo objeto antes de crear trabajo duplicado. Continúa una rama compatible cuando proceda. Archiva el encargo por 0-bis A.3. Al lanzarlo quedan autorizados sus cambios, commits, push y PR propio revisable; **el merge pertenece a mesa**. No cerrar PR ajenos, borrar worktrees, descartar cambios ajenos ni modificar el candado de `/despacha`.

**Entorno.** `ENTORNO` en la cabecera identifica dónde terminar. Cloud/NUBE puede trabajar código, documentos públicos y resultados agregados. Los microdatos se abren únicamente en CAJA/Ubuntu, según el repo. Usa `tools/entorno.py` y las raíces configuradas; enlaza correctamente el corpus compartido antes de concluir que falta. No inventes rutas Windows/WSL, no copies microdatos ni credenciales a Git. Si una capacidad falta, completa las fases independientes y entrega la continuación exacta; no confundas NO-VERIFICABLE con AUSENTE. Dos intentos razonables y una alternativa bastan para registrar un bloqueo.

**Concurrencia e integración.** Estas son tareas manuales separadas; no cambian la regla de una sesión del despacho automático. Verifica compuertas por ascendencia y producto, conforme a ADR-277, no buscando un título en el log. No reserves números de ADR/NC/FP: derívalos contra main al cerrar. Se aplica el precedente ya utilizado en #687–#693: **quien fusiona después renumera**. Integra main en tu rama, conserva las filas ajenas por identidad y significado y reconcilia referencias del acto; nunca reemplaces un TSV completo por la copia vieja de tu rama. Los IDs que aparecen abajo son los definitivos en main al corte, no los candidatos antiguos del cuerpo de un PR.

Usa `tools/cierre_acto.py` primero en seco y luego `--aplica` cuando corresponda para la cascada existente. Conserva una única ancla L0. Ejecuta las pruebas materiales sobre la integración final; verifica también la sincronización del HEAD remoto mediante el procedimiento vigente de `/acto`. Un push posterior a la revisión requiere comprobar su delta pertinente. Serializar merges, no necesariamente todos los trabajos.

**Perímetro administrativo permitido.** Copia archivada de este encargo, una nota de cierre, sus filas de `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, cola y decisiones cuando corresponda, y la cascada existente en `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_12.md`, `canon/registro-rotulos.tsv`. Resolver renombres al lanzamiento. No crear otra plantilla, índice, tablero o ADR de política para problemas ya cubiertos. Modificar las vistas globales sólo si el encargo lo incluye; de otro modo entregar comprobantes al responsable de publicación.

**Medición y decisiones.** Corre `tools/ya_medido.py <regla>` antes de clasificar o medir una regla; conserva la salida pertinente. Para una medición nueva, congela pregunta, universo, codificación, unidad, ponderador, exclusiones, método y aceptación en un commit previo al primer resultado. Un diagnóstico posterior a ver datos se etiqueta exploratorio; no se vende como prueba confirmatoria. Usa el flujo `spec-check → preflight → run → verify` cuando corresponda. Verifica fuente, periodo, muestra, transformación y relación con el parámetro. Preserva specs, resultados, snapshots y sellos históricos; una sucesora no reescribe su antecedente. Un mismo número reutilizado o un replay técnico no es otra medición independiente. `cuenta_gen2` sigue las firmas y reglas existentes; los CALC científicos nuevos explicitan objeto y cita. **Contar, reproducir, validar independientemente y adoptar son actos diferentes.**

**Límites de gasto y comunicación externa.** Salvo el ejecutor productivo configurado del cron, estos encargos no requieren llamadas nuevas a modelos. No cambiar proveedor ni abrir gasto de API para destrabar una tarea. Las vías comerciales de tandas siguen diferidas. Preparar solicitudes no autoriza firmarlas, aceptar acuerdos o enviarlas en nombre del usuario. No fabricar identidad, afiliación o recepción. Si una fase exige una decisión científica aún abierta, dejar producto y opciones concretas; continuar las demás.

**Pruebas y parada.** Validar primero el resultado material; correr el baseline requerido sin ampliarlo para ocultar fallos. No perseguir los tres FAIL históricos por rutina. No volver a arreglar NC-0141/0148: #690 ya lo hizo. Revisar el diff después de las pruebas y añadir sólo archivos deliberados. D-14: cualquier automatización adicional debe evitar un error observado con efecto material y costar menos que su corrección repetida; si no, resolver directamente. Auditoría aproximadamente 20%, salvo riesgo material en números, identidad o decisión.

Avanza entre fases ya autorizadas sin pedir confirmación. Termina cuando entregues el resultado suficiente o un residual externo concreto. Cadena de cierre: autorización → producto → evidencia → consumidor cuando aplique → obligaciones → vistas/cola → PR → merge de mesa. Una fila mixta conserva su parte pendiente. No cerrar por palabra coincidente ni por recomendación. Respuesta final del ejecutor: resultado útil, fases cumplidas/pendientes, PR/SHA, pruebas, y tabla `obligación | evidencia | cerrada/residual | siguiente acción`.

## NO-CORRIDO / RESERVAS

- `NC-0114`: falta observar una corrida con el runner fusionado y correlacionar
  la etiqueta de disparador con el evento Windows, `run_id`, SHA y recibo.
- `NC-0120`: falta que un operador habilite el canal Operational con elevación
  y observar una recuperación real futura; la sonda aislada negativa no la
  acredita.
- `NC-0153`: PR #695 obtuvo productos parciales, no la tasa nacional exacta;
  queda para el titular pedir la llave ENCIG 8.5↔`NT_TIPO/P7_3` o un microdato
  nacional equivalente. No se envió solicitud ni se repitió la búsqueda.

## CONSUMIDO

Ejecutado el 10/sep/2026 en `acto/gen2-sonda-cron-produccion`; PR #704,
ADR-467. Configuración, pruebas y evidencia operativa en
`forense/notas/2026-09-10-GEN2-SONDA-CRON-PRODUCCION-POST693-cierre.md`.
La Fase 4 consume el resultado fusionado de PR #695 sin repetir su búsqueda:
`NC-0153` y su demanda permanecen `OBTENIDO-PARCIAL`, diferidas con causa y
recibo. `NC-0115` cierra; `NC-0114` y `NC-0120` conservan sus residuales
operativos exactos. Merge de #704 reservado a mesa.
