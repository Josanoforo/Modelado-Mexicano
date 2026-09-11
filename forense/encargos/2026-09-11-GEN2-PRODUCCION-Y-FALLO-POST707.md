# Continuación 07R · producción y fallo después de #707

ENTORNO: CAJA

Destino: Codex CLI en Windows/WSL. Continuación de D19 y 07R, no un cron nuevo. Si 07R ya está activo, incorporar este archivo en esa sesión. Sustituye las premisas operativas del documento POST704; preserva sus obligaciones pendientes.

## Resultado requerido

Explicar y tratar el fallo de adquisición del 11 de septiembre; verificar que Windows ejecuta la configuración fusionada; dejar evidencia que distinga disparo programado, ejecución manual, salida del agente y publicación. Puede correr junto a 17–22 porque posee exclusivamente el clon productivo y la tarea programada.

## Fase 1 · partir del recibo real

Leer `AGENTS.md`, el encargo completo, `.claude/commands/acto.md`, `tools/windows/GUIA-TAREA-ADQUISICION.md`, `data/adq-config.yaml`, `tools/adq_doctor.py`, `tools/adquiere_cron.sh` y las filas NC-0114/0120/0133. Archivar por el procedimiento vigente. Reportar ruta absoluta, rama, HEAD y estado del worktree y de `/home/pc0/mm-adq`.

El corte es main `cd92cb25acbb7b645a4b49ed180f042661d18e7e`. #700 y #707 ya están fusionados. `forense/censo-raiz/2026-09-11.txt` contiene:

```text
[ADQ] 2026-09-11 08:08: invocado=si motivo=- exit=1 duracion=37s commits_nuevos=0 ramas_nuevas=1 archivos_modificados=1 sha=c23dce15a917bb6fb0a4e44dabf3767e03c9ded8 publicacion=OK run_id=2026-09-11T080731-1157475
```

La ejecución ya identifica una versión que incorpora #704. No reinstalar por asumir que sigue en #677. Publicación OK acredita el recibo, no éxito del agente ni selección/adquisición de datos. La nota PDN «fuera de ventana», día 11 frente a ventana 1–3, es una exclusión esperada, no por sí sola causa de fallo.

Observar cambios locales y procesos activos. Respaldar el staging propio o ajeno con identidad recuperable antes de actualizar; no usar reset/clean ni descartar archivos. El censo incorpora documentos descargados por el usuario: no promoverlos automáticamente al manifiesto científico.

## Fase 2 · resolver el `exit=1`

Localizar stdout/stderr, estado y logs asociados al run_id. Recuperar el comando efectivo, ejecutable, versión, usuario, entorno/PATH y directorio. Contrastar la salida del proceso hijo con la del wrapper. Extraer sólo las líneas necesarias; no publicar tokens, prompts sensibles ni logs completos por comodidad.

Establecer causa con evidencia. No atribuirla sin comprobación a cuota de Claude, red, login o timeout; 37 segundos no demuestra agotamiento del límite de ejecución. Comprobar disponibilidad del ejecutor configurado. Aplicar la corrección técnica mínima que corresponda: entorno, invocación, manejo del fallo o acceso ya autorizado. Mantener modelo, identidad de cuenta y límites vigentes; si falta una credencial del titular, terminar el diagnóstico y dejar el paso local preciso, sin sustituir silenciosamente el ejecutor.

Una comprobación de versión o del doctor precede a una ejecución completa. Tras corregir una causa reproducible, hacer como máximo una ejecución funcional adicional de adquisición autorizada, con límites existentes, si es necesaria para validar. Rotularla manual cuando lo sea; no iniciar recapturas de evaluación ni un ciclo de reintentos. Una indisponibilidad externa puede dejar el pipeline correctamente diagnosticado, pero no se informa como adquisición exitosa.

## Fase 3 · instalación y atribución

Exportar la tarea existente y contrastar calendario, zona, acción, principal, política de recuperación y próxima ejecución con YAML y guía actuales. La configuración conocida es 07:30 lunes–viernes, America/Mexico_City / Central Standard Time (Mexico), principal Interactive. Respetar una decisión posterior documentada; no cambiar a S4U incidentalmente.

Comprobar que Windows apunta al clon correcto y a la acción actual, incluida la marca `ADQ_DISPARADOR=windows-task-scheduler`. Usar primero `tools/windows/instala-tarea-adquisicion.ps1 -WhatIf`; instalar sólo si el contraste muestra diferencia material. No rehacer una instalación ya acreditada.

Comprobar el canal `Microsoft-Windows-TaskScheduler/Operational` y habilitarlo cuando falte mediante el procedimiento Windows autorizado. Si se requiere elevación que esta sesión no tiene, entregar al operador el comando exacto y completar las fases independientes. Ejecutar `python3 tools/adq_doctor.py --json`.

Correlacionar evento Windows, causa, EventRecord/ActivityId disponible, run_id WSL, SHA, hora y zona, heartbeat, exit y publicación. La marca del scheduler y una hora parecida no distinguen una activación manual de una programada: usar los eventos. Si los logs históricos no existen, decir qué ya no es recuperable y habilitar evidencia prospectiva; no reconstruir un evento inventado.

Observar la siguiente ventana natural cuando ocurra durante el trabajo. No cambiar reloj, suspender ni reiniciar el equipo para fabricar una recuperación. Si la ventana queda fuera, publicar arreglo/despliegue con continuación exacta de observación; la sesión no espera indefinidamente. Distinguir corrida normal de recuperación real: acreditar una no cierra automáticamente la otra.

## Fase 4 · cerrar sólo lo cumplido

Actualizar nota de cierre y filas pertinentes de `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv` y `forense/cron/REGISTRO-CRON-v1_0.md`, con escritores/procedimientos vigentes y preservando aportaciones ajenas.

NC-0133: comprobar si ya se asentó la retirada acreditada en #668/#704; completar sólo el asiento faltante. FP-324: conciliar únicamente DD_COMPRANET_DICCIONARIOS_DE_DATOS ya obtenida, edición archivada de enero de 2025, si aún falta. No cerrar las otras recetas ni tratar esa edición como dato vivo. NC-0114/0120 conservan los alcances no demostrados. La demanda NC-0153 sigue con su estado real: no forzar PENDIENTE para fabricar actividad.

## Aceptación, perímetro y entrega

Evidencia de causa del fallo, tratamiento o dependencia externa concreta; tarea única contrastada; staging preservado; versión ejecutada identificada; estado de publicación separado del exit; atribución programada demostrada o reserva exacta. Probar sólo el camino corregido y los gates vigentes; no repetir suites enteras sin cambio que lo justifique.

Al entregar este encargo al ejecutor se autorizan sus fases técnicas, commits, push y PR propio. No autoriza merge, cambio de modelo, envío a terceros ni edición del motor/cálculos/evaluación. Revalidar cambios pertinentes antes del commit. Entregar `obligación | evidencia | estado | continuación`, PR/HEAD y un resumen que diga si la próxima adquisición ya puede contarse como operativa o qué requisito concreto falta.


**Actualización al entregar:** #708 también está fusionado; main=`e7a471bf1499a096abbe58dc298f02243e885135`. Archiva el benchmark sin firmar sus cuatro decisiones; no cambia el alcance de este encargo.

## NO-CORRIDO / RESERVAS

Se reutilizan `NC-0114` y `NC-0120`; no se abren filas gemelas.

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Habilitar `Microsoft-Windows-TaskScheduler/Operational` y recuperar `EventRecord`/`ActivityId` del run del 11/sep | `PARO-ENTORNO` — Windows exigió elevación y devolvió acceso denegado/código 5; el evento histórico no se registró y ya no es recuperable | `NC-0114` no cierra por atribución programada; una hora coincidente no distingue trigger, recuperación o clic manual | `NC-0120`: operador ejecuta `wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true` en PowerShell elevado |
| Observar la siguiente ventana natural con la acción atribuible ya desplegada | `DIFERIDO-A:NC-0114` — la siguiente ejecución es el lunes 14/sep a las 07:30 y esta sesión no espera indefinidamente ni cambia el reloj | no se declara una adquisición exitosa ni una activación programada atribuida | `NC-0114`: correlacionar evento Windows, `run_id`, `disparador`, SHA, heartbeat, exit y publicación |
| Observar una recuperación real de `StartWhenAvailable` | `NO-VERIFICABLE-AQUÍ` — no ocurrió una pérdida natural durante la sesión y no se suspende/reinicia la máquina para fabricarla | `NC-0120` conserva el alcance de recuperación; una corrida normal no lo satisface | `NC-0120`: observar una pérdida real futura con Operational habilitado |
| Ejecución funcional adicional de adquisición el 11/sep | `PARO-ENTORNO` — el ejecutor informó límite semanal hasta el 12/sep 11:00; otra corrida contra la misma indisponibilidad no valida la corrección técnica | el fallo queda diagnosticado, pero no se cuenta como adquisición exitosa | `NC-0114`: ventana natural posterior al reinicio de capacidad |
