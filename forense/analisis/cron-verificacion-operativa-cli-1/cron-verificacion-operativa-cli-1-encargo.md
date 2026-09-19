# GEN2-CRON-VERIFICACION-OPERATIVA-CLI-1

## Encargo y autoridad

Verifica en la PC/WSL real que el servicio de adquisición y derivación sigue funcionando; corrige únicamente defectos operativos comprobados y entrega evidencia publicable del estado final. Un solo ejecutor para este encargo. Repositorio Josanoforo/Modelado-Mexicano, rama `codex/gen2-cron-verificacion-operativa-cli-1`, worktree propio para cambios; el clon productivo `/home/pc0/mm-adq` se inspecciona y despliega sin apropiarse de cambios de otra sesión.

Pegar este encargo autoriza inspección local, corrección acotada de despliegue hacia la revisión autorizada, commit/push/PR de la entrega y pruebas limitadas abajo. No autoriza merge, otra tarea programada, cambio de modelo, calendario, presupuesto, credenciales o decisiones científicas. No recrear una vigilancia de ChatGPT ni enviar mensajes externos.

Lee AGENTS.md y reporta worktree, rama, HEAD y estado. Base revisada al redactar: main `8e455bd6a3870566d6776fef19834c4da16d2fa9`, 19/sep/2026. El recibo publicado más reciente encontrado es `forense/censo-raiz/2026-09-18.txt`, run `2026-09-18T083018-433`. Reporta exit=0, tres investigaciones validadas, trabajo publicado, handoff coincidente, cero objetos adquiridos y cero reducción de brecha. Es evidencia del 18; no acredita la última activación ni toda la cadena de derivados de hoy.

## P1. Comprobar instalación y último disparo

Lee `data/adq-config.yaml`, `tools/windows/GUIA-TAREA-ADQUISICION.md`, launcher y las notas de reparación del 16 y handoff del 17 de septiembre. La configuración vigente manda: calendario diario America/Mexico_City 07:30, comprobación cada 60 minutos y recuperación al iniciar sesión. No restaurar lunes–viernes por las secciones históricas del registro cron.

Exporta la tarea existente `\ModeladoMexicano\AdquiereCron`, sus triggers, acción, principal, estado, LastRunTime, LastTaskResult y NextRunTime. Contrasta con configuración e instalador actuales. Comprueba ausencia de un crontab ejecutable duplicado. Conserva launcher, política de instancia única y propagación de salida WSL/PowerShell. No interpretar LastTaskResult aislado como salud del cálculo.

Lee eventos TaskScheduler/Operational recientes, correlacionando ActivityId/RecordId, hora con zona, causa del inicio y cierre con run_id/heartbeat/log de WSL. Selecciona la última ventana exigible según hora local y tolerancia vigente; no declarar falta antes de vencerla. Distingue trigger horario, recuperación y ejecución manual. Comprueba proceso/lock si el estado sigue en ejecución: no borrar un lock de un proceso vivo ni lanzar otro hijo.

Entrega una cronología de las últimas tres activaciones observables, incluyendo una que haya ejecutado trabajo real si existe. No es necesario esperar tres futuras. Si faltan eventos, la atribución queda no acreditada aunque exista una marca `disparador=windows-task-scheduler`; esa variable por sí sola no prueba el origen.

## P2. Verificar ambos tramos y el resultado

Derivación: SHA solicitado/cargado, revisión autorizada, heartbeat, cuatro fases deterministas y publicación requerida. Distingue NADA-QUE-HACER legítimo de fallo sin publicación. Revisa la firma que alimenta ultima-exitosa, sin borrarla para forzar trabajo. Si hace falta prueba, usa la vía documentada `DERIVA_PUBLICAR=0 MM_TRAMO=derivacion` en condiciones sin colisión; rotúlala manual, no automática.

Adquisición: selección, inicio del único ejecutor, resultado final y handoff, informe del validador, evidencia en corpus compartido, referencias publicadas y liquidación del presupuesto. Comprueba login sin exponer tokens. Respeta los límites y checkpoints vigentes. No relanzar búsquedas ya consumidas ni resetear presupuesto. Para probar transporte/validación usa artefactos existentes y pruebas sintéticas antes de gastar otra corrida real.

Revisa específicamente si el arreglo de rechazo de symlinks del corpus del 17/sep está en el SHA efectivo y si se conserva la detección de dos candidatos válidos distintos. No reconstruir un resultado perdido a partir de prosa ni reescribir el exit=65 histórico.

Reporta por activación salud de disparo, derivados, ejecución, validación, publicación y utilidad. Extrae seleccionadas/iniciadas/validadas, objetos/bytes nuevos, evidencia nueva y reducción de brecha. Un exit=0 con cero reducción sigue siendo éxito operativo sin avance sustantivo.

## P3. Corregir la causa material y cerrar

Si la instalación difiere del contrato vigente, preserva exportación anterior, usa instalador soportado y revisión autorizada, y verifica posterior. No despliegues código nuevo sin publicar ni cambies la selección de necesidades para fabricar un éxito. Si hay defecto de código, limita cambios a launcher/runner, doctor/handoff o instalador afectados y pruebas de esa causa; conserva contratos y comportamiento de reservas. No tocar motor, milpa, corrida0.py, tests/check.py, canon, decisiones, inventarios o NC globales.

No convertir una reparación de despliegue en reescritura de infraestructura. Si requiere aprobación del sistema, elevación o credenciales, usa el mecanismo permitido y registra cualquier bloqueo; no lo evadas. Si no se puede comprobar el siguiente trigger natural dentro de la sesión, entrega prueba manual separada y estado AUTOMATICO-PENDIENTE, con hora y comando de comprobación concretos; no inventes evidencia ni dejes un proceso de vigilancia permanente.

Analiza NC-0244 como ejemplo de demanda de mesa enviada a adquisición y DEM-AHORRO-STOCK-DURACION-01 tras seis ciclos sin mejora. Entrega al recibo Claude una propuesta breve con evidencia y frontera restante. No retirar esas necesidades, adjudicar procedencias ni cambiar política por cuenta propia. La corrección de ruteo, si requiere decisión científica, queda distinguida de la salud operativa.

## Entrega

Archiva este encargo verbatim y entrega `forense/analisis/cron-verificacion-operativa-cli-1/` con tabla de activaciones, extractos saneados, SHA efectivo, diagnóstico, corrección/prueba y lectura de utilidad. Runtime completo, tokens y microdatos permanecen locales. Pruebas dirigidas a la causa; nada de suites generales por inercia.

Si todo ya está correcto, no cambies código: publica la comprobación. Si hay fallo sin acceso, conserva evidencia y receta concreta. Cierre obligatorio: FUNCIONANDO-ACREDITADO / FUNCIONANDO-PARCIAL / FALLANDO / NO-VERIFICABLE, indicando fecha/hora hasta la que aplica. Incluye URL de PR y SHA; no merge. No contar esta tarea como nueva medición científica.
