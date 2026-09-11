Encargo final · adquisición con Codex y puesta en producción

ENTORNO: CAJA
DESTINO: Codex CLI en Windows/WSL de Jonás.
OBJETO: continuar 07R/#711 hasta dejar adquisición operativa con Codex.
RESULTADO DE CIERRE: configuración instalada y una adquisición real disparada por Windows durante esta misma puesta en marcha, con resultado y publicación verificables.

0 · Autoridad, cambio de dirección y modo de trabajo

Instrucción de Jonás del 11 de septiembre de 2026, fuente de este encargo:

«por qué no lo habilitamos desde el principio?, ahorita se detuvo por el limite de claude, pero no necesita usar claude, puede usar codex. Dame un encargo para resolverlo y no quiero que sigamos haciendo cosas en tests y tests y luego en producción. Así que dame el encargo final para hacer la revisión completa del clon (en caso de que lo necesitas para hacer los ajustes) o el ajuste para que codex cli ejecute los cambios».

Esta instrucción autoriza Codex CLI como ejecutor principal de adquisición, revisión y ajustes del clon productivo, configuración local necesaria, habilitación de eventos por el procedimiento administrativo de Windows, despliegue local reversible y ejecución real de adquisición. Sustituye las restricciones anteriores de conservar Claude y esperar exclusivamente a la ventana del lunes. No hace falta otra firma científica para estas operaciones.

El encargo autoriza commits, push y PR, y el despliegue local de su revisión identificada aun si su PR sigue abierto. El merge permanece con Jonás. El cambio se limita al agente de adquisición: no cambia el modelo competidor de F5, las capturas, árbitros, parámetros, firmas científicas ni los candados Gen1→Gen2.

Ejecuta las fases como un único trabajo. Prioriza reparar y operar. Haz una comprobación breve antes del despliegue y demuestra el resultado con la tarea real; no entregues sólo tests, -WhatIf, una receta de instalación o «pendiente de probar en producción». Reutiliza #711 y lo ya resuelto. Si la sesión de 07R sigue abierta, continuar allí; no crear dos operadores del mismo clon.

1 · Revisar el clon real y resolver accesos al comienzo

Leer AGENTS.md, .claude/commands/acto.md, este encargo y los archivos de su perímetro. Reportar ruta absoluta, rama, HEAD y git status --short tanto del worktree de edición como de /home/pc0/mm-adq. Comprobar el estado actual de #711 y cambios posteriores pertinentes. La última consulta de preparación vio #711 abierto, HEAD 6a52c57015c9bb830ddefd9111013a1bb5900682; la revisión de contenido anterior fue sobre 5230086. No repetir ni descartar sus aportaciones si avanzó.

Revisar de extremo a extremo la instalación de adquisición, no todo el proyecto científico:

Pieza

Comprobación y arreglo permitido

Clon y versión

Remoto, rama, trabajo ajeno, actualización, ruta que Windows realmente ejecuta y versión que llega al hijo

Windows/WSL

Tarea, principal, distro/usuario, acción, calendario, eventos, entorno y permisos efectivos

Codex

Binario real, versión, autenticación, configuración de ejecución y disponibilidad en el contexto del scheduler

Corpus/red

Raíz real, enlaces, acceso y escritura en destinos de adquisición, herramientas ya instaladas

Procedimiento

Prompt, selector, SONDA→cola, escritores canónicos, permisos Git y publicación

Vida de la corrida

Lock, heartbeat, timeout/terminación, resultado del agente y recibo final

Archivos iniciales: tools/adquiere_cron.sh, tools/adq_config.py, tools/adq_doctor.py, data/adq-config.yaml, tools/windows/instala-tarea-adquisicion.ps1, tools/windows/GUIA-TAREA-ADQUISICION.md, forense/agente-adquisicion-v1_0.md, .claude/commands/adquiere.md y el cierre de #711. Abrir otros sólo si resuelven una dependencia material.

Preservar staging, corpus, trabajos y procesos ajenos. #711 ya documentó restitución del staging por hash: volver a observar, no asumir ni repetir un stash a ciegas. No usar reset --hard, clean ni borrar datos para facilitar el arranque. Edición en worktree propio; el clon productivo se modifica mediante despliegue controlado. Coordinar la ventana corta sobre ese clon sin detener 17–22 en otros worktrees.

Resolver el permiso de eventos ahora. Exportar la tarea actual. Comprobar Operational y, si falta, habilitarlo con un proceso PowerShell elevado por el mecanismo normal de Windows. Preparar un script breve, visible y acotado; solicitar la confirmación UAC del titular en la misma sesión si el sistema la exige. El motivo es el código 5/acceso denegado que documenta #711, no una nueva aprobación de proyecto.

Comandos sustantivos de ese paso:

wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true
Get-WinEvent -ListLog Microsoft-Windows-TaskScheduler/Operational |
  Select-Object LogName,IsEnabled,RecordCount,LastWriteTime

Confirmar IsEnabled=True; persistir evidencia mínima. La elevación sirve para esta operación administrativa, no para cambiar el usuario del agente a administrador. El instalador actual usa $env:USERNAME: si UAC usa otra cuenta, conservar explícitamente el principal original de la tarea y el usuario Linux pc0. No modificar su identidad por accidente ni cambiar Interactive a S4U como efecto lateral.

Si no existe una credencial administrativa disponible, no evadir Windows ni declarar habilitado el canal: pedir únicamente esa intervención concreta al titular y mantener este mismo encargo abierto para continuar. Completar los arreglos independientes mientras tanto.

2 · Configurar Codex para ejecutar adquisición sin interacción

Observar bajo el mismo usuario y entorno que usará Task Scheduler: command -v codex, codex --version, codex exec --help y codex login status. Usar la instalación real; no suponer una ruta o flags por memoria. Si falta una versión compatible, instalar/actualizar por la vía oficial preservando configuración y sesión de Jonás, y volver a comprobar.

codex exec es la invocación para trabajo no interactivo. Puede recibir el prompt por stdin con -, emitir eventos JSONL y escribir el mensaje final con --output-last-message; reutiliza autenticación guardada. Ajustar la sintaxis a la versión local comprobada. OpenAI Docs: modo no interactivo.

Usar el acceso de ChatGPT de Jonás ya configurado en CLI y el modelo disponible de su configuración, registrando el identificador efectivo. No inferir el modelo por llamarse «Codex» ni por el nombre de esta conversación. No migrar silenciosamente a una API de pago. Si hace falta login, completar el flujo oficial con el titular durante esta sesión. login status verifica autenticación, no garantiza cuota disponible: la ejecución real será la comprobación funcional. OpenAI Docs: autenticación, referencia de comandos.

Configurar un ámbito de ejecución de adquisición, conservando intacta la configuración general de las otras sesiones. Debe permitir lo que el trabajo necesita: leer corpus, descargar a destinos previstos, actualizar sus registros y publicar su rama/recibo. Verificar red y permisos desde el proceso hijo, no sólo desde el shell padre. No dejar prompts de aprobación esperando dentro del job programado. Resolver permisos por los mecanismos admitidos; no ignorar reglas administradas ni desactivar protecciones globales para ocultar una denegación.

Para los permisos locales usar la configuración documentada y compatible con la versión instalada. El modo de escritura explícito sustituye en scripts nuevos al flag --full-auto, actualmente de compatibilidad. No asumir que autorizar escritura en el worktree otorga también red o escritura en un corpus enlazado. OpenAI Docs: permisos de ejecución.

Portar el procedimiento, no sólo el nombre del binario. El prompt actual dice «Corre /adquiere» y remite a .claude/commands/adquiere.md. Construir un prompt explícito para Codex que lea y ejecute ese procedimiento y sus referencias, sin depender de que exista un slash command registrado. Reutilizar la única definición vigente; no mantener una copia divergente de la lógica de selección. Mantener los candados de entorno CAJA verificando ubicación/corpus reales, sin depender exclusivamente de la ausencia de una variable propia de Claude.

Codex queda como principal y una cuota agotada de Claude deja de bloquear el preflight. No implementar rotación de cuentas ni fallback silencioso. Si se conserva un selector de ejecutor, sólo una configuración explícita puede activar Claude; no es una dependencia obligatoria del camino Codex.

3 · Ajustar runner, diagnóstico y publicación como un recorrido único

Centralizar en la configuración vigente el ejecutor efectivo y límites del proceso. Migrar los nombres ligados a Claude donde sea necesario, preservando compatibilidad explícita para valores antiguos sin mantener dos autoridades. Conservar inicialmente 1800 segundos de ejecución, 60 de gracia de terminación, el límite Windows vigente y el máximo de cinco filas; un requisito nuevo debe tener motivo concreto, no aumentar gasto por defecto.

Actualizar conjuntamente runner, doctor, runbook e instalador/guía donde corresponda. El doctor debe comprobar el binario/autenticación requeridos por el ejecutor seleccionado; no declarar el sistema roto porque falta Claude cuando está seleccionado Codex. Mantener legibles los recibos históricos. Ajustar al nuevo recibo el lector T-CRON sólo si lo necesita; no rehacer la suite del proyecto.

El recibo y heartbeat deben identificar al menos: run_id, causa/identidad del disparo, ejecutor, versión CLI, modelo configurado/efectivo cuando sea observable, versión del runner, SHA del árbol usado, inicio/fin, salida del proceso, resultado sustantivo y publicación. No inventar un modelo resuelto cuando el runtime no lo expone. Conservar stderr/eventos localmente sin publicar credenciales ni sesiones completas.

Distinguir exit=0 de trabajo cumplido: exigir evidencia de selección y resultado. Para filas elegibles, presentar intentos y objetos/recetas resultantes; para cola vacía, lista y causas verificables. No aceptar como éxito un mensaje que sólo diga que no pudo escribir, que dejó un plan o que necesita lanzar otra sesión. Mantener resultado del agente y publicación separados: un fallo de cualquiera queda visible, con causa y salida no exitosa donde corresponda.

Conservar exclusión mutua, manejo de timeout, heartbeat y publicación incluso al fallar el hijo. No permitir que el agente hijo vuelva a invocar el mismo runner y genere recursión. Las publicaciones autorizadas son commits, ramas y PR de adquisición; no envíos de solicitudes a terceros ni firmas de contratos de datos.

4 · Instalar una versión que realmente sobreviva al arranque

Resolver un riesgo concreto del código actual: adquiere_cron.sh hace checkout/pull de main después de arrancar. Una edición que sólo vive en una rama puede perderse antes de invocar Codex, y la versión inicial del shell puede diferir del árbol del hijo.

Implementar el camino más corto que garantice una versión coherente: actualización/despliegue antes de ejecutar la lógica mutable, o arranque controlado que ejecute una sola vez la revisión resuelta y conserve el lock. Registrar por separado las versiones si hay un launcher estable. No crear una plataforma nueva de releases.

Si el cambio ya está fusionado, desplegar ese main. Si el PR aún está abierto, queda autorizado desplegar localmente su SHA publicado mediante una referencia explícita de despliegue, con el rollback registrado. No fingir que ese SHA ya es main. El arranque debe respetarlo; no aceptar como solución editar archivos que el siguiente pull sobrescribirá. La tarea recurrente debe seguir en la versión con Codex después de la sesión.

Si se usa una revisión fijada mientras el PR está abierto, implementar en ese mismo mecanismo la transición automática a main cuando main contenga la revisión desplegada. Hasta entonces conserva la revisión autorizada e informa ese estado. No exigir otro encargo después del merge, permitir un descenso silencioso a la versión Claude ni dejar una segunda implementación manual fuera de Git.

Publicar el código y desplegarlo de forma reversible en /home/pc0/mm-adq, preservando trabajo ajeno. Exportar la tarea después de instalar y comprobar que apunta al clon, usuario y versión previstos. Mantener la tarea \ModeladoMexicano\AdquiereCron, la marca del scheduler, calendario y zona vigentes. No crear otro scheduler diario.

5 · Ejecutar una adquisición real desde Windows en esta sesión

Antes de gastar la corrida, comprobar sintaxis/configuración y sólo las regresiones directamente afectadas que pueden ocultar un fallo o dañar datos. No volver a probar repetidamente lo ya acreditado ni dedicar el encargo a alcanzar una suite global verde. Después, avanzar a producción.

No esperar al lunes. Con Operational activo y el nuevo código instalado, añadir a la misma tarea un disparo único unos minutos en el futuro. Conservar el trigger semanal original y guardar una exportación recuperable. El disparo añadido debe ejecutar la acción productiva, no un marcador, doble de Codex o tarea ficticia.

Comprobar que no hay otra instancia activa ni una colisión inmediata con el calendario normal. Dejar que Windows dispare por tiempo. Rotular el recibo como ejecución programada de puesta en marcha; no presentarlo como la corrida semanal de las 07:30 ni como recuperación de una hora perdida. Un clic en «Ejecutar» o Start-ScheduledTask puede servir para diagnóstico, pero no sustituye esta atribución.

Ejecutar el trabajo de adquisición autorizado con la selección vigente, máximo cinco filas y resultados reales. Evitar duplicar objetos que otro encargo está obteniendo, comprobando el estado actual y coordinando únicamente esos objetos. No cambiar firmas ni estados para fabricar una fila elegible. Si la cola queda vacía, Codex debe recorrer y documentar esa selección real; es un resultado válido, no una adquisición nueva.

Correlacionar evento Windows/RecordId/ActivityId y causa con run_id WSL, proceso Codex, versiones, selección, resultado, heartbeat y publicación. Confirmar que la ejecución no invocó Claude. Abrir el recibo publicado y contrastarlo con lo sucedido localmente.

Si aparece un fallo de implementación, corregir la causa en este mismo encargo, desplegar la revisión y repetir únicamente el tramo o corrida necesario. No encadenar reintentos idénticos ante cuotas o autenticación no resueltas. Mantener los límites y reportar el consumo/intentonas reales.

Retirar sólo el disparo único añadido por esta sesión, incluso al manejar un error; restaurar y verificar calendario/principal/acción definitivos. Confirmar próxima ejecución normal, Operational activo y ausencia de procesos/locks abandonados. No terminar con la tarea deshabilitada, un trigger extra olvidado o el clon vuelto a la versión anterior.

6 · Cerrar con resultado y sin duplicar pendientes

Actualizar la autoridad vigente del runbook y registro cron: adquisición usa Codex por esta decisión de Jonás. Preservar el fallo histórico de Claude como antecedente, sin reescribirlo como si Codex hubiera corrido entonces. Propagar estado y cierres con las herramientas existentes y sólo sobre filas propias.

NC-0114: registrar el recorrido programado de producción demostrado ahora y el tipo exacto de trigger. La decisión actual sustituye esperar al lunes para la puesta en marcha; no inventa una observación semanal pasada.

NC-0120: registrar la habilitación efectivamente completada. Una corrida normal no acredita recuperación: conservar únicamente ese alcance si todavía falta, sin convertirlo en un bloqueo para operar con Codex ni volver a encargar la migración. No reiniciar, suspender ni cambiar el reloj para fabricar evidencia.

NC-0133 y la receta CompraNet: conservar sus cierres acreditados en #711; no repetirlos. Las otras demandas de datos mantienen su estado real.

Entregar una tabla breve:

Resultado requerido

Evidencia de aceptación

Codex instalado como principal

Configuración efectiva, ruta/versión del binario y autenticación bajo el usuario de la tarea

Despliegue persistente

SHA instalado y mecanismo que evita que el arranque lo sustituya por Claude

Eventos habilitados

IsEnabled=True y evento del disparo real

Adquisición ejecutada

run_id, selección, resultado útil o cola vacía acreditada, salida de Codex

Recibo accesible

Publicación verificada y separación entre trabajo y publicación

Tarea lista para continuar

Trigger único retirado, calendario normal conservado y próxima ejecución

Trabajo ajeno preservado

Estado/huellas antes y después, sin descartes

El cierre principal debe decir «INSTALADO Y EJECUTADO CON CODEX» sólo si existe esa cadena. Si falta una credencial/elevación o hay indisponibilidad externa real, decir exactamente qué falta y continuar en esta misma sesión cuando el titular lo resuelva; no declarar entrega terminada con «LISTO-PARA-PROBAR».

Entregar PR/HEAD, revisión desplegada, recibo y reserva material restante. Los detalles rutinarios de sincronización/numeración no son una nueva decisión de mesa. El resultado de esta tarea es adquisición operativa; no otra ronda de auditoría general.
