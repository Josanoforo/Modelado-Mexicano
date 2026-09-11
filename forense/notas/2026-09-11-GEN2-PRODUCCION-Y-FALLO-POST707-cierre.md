# GEN2-PRODUCCION-Y-FALLO-POST707 · causa, despliegue y reserva de atribución

Fecha local: 2026-09-11. Entorno: CAJA, Ubuntu/WSL2 y host Windows.

## 1 · Estado recibido y preservación

El clon productivo es `/home/pc0/mm-adq`. Al abrir estaba en `main`, HEAD
`c23dce15a917bb6fb0a4e44dabf3767e03c9ded8`, con una modificación ajena de
`data/manifiesto-staging.yaml` (392 líneas añadidas y una eliminada). Antes de
actualizar se preservó como `stash@{0}`, objeto
`1900f77da97e9be002d46b719266622a232e8a92`, mensaje
`07R-pre-update-staging-2026-09-11`; el archivo previo tenía SHA-256
`c72508bc0fd29a83348730d6cdc10087b3d281e7cb2b08f61080a4e405be6597`.
No se usó `reset`/`clean`, no se descartó ningún payload y los 33 documentos
que el censo marcó como nuevos no se promovieron al manifiesto científico.
Al cerrar se reaplicó el stash sin borrarlo: el archivo volvió a la misma
huella SHA-256 y al mismo diff 392/1, y el objeto `1900f77d…` permanece como
respaldo recuperable adicional.

Después de `git fetch --prune`, `main` estaba ocho commits detrás y avanzó por
fast-forward a `a37837a0df69240e35c160a53c5c1de209f9be01` (merge de #709), más
reciente que los cortes `cd92cb25` y `e7a471bf` del encargo. El acto corre en
`acto/gen2-produccion-fallo-post707`; el encargo quedó archivado verbatim en el
primer commit `d6de9f8802fd375b32ad2cb8c0af7fd7bbf35ce4`. El benchmark de #709
queda archivado en `forense/notas/BENCHMARK-WEB-CUATRO-DECISIONES-GEN2-2026-09-11.md`;
este acto no firma sus cuatro decisiones.

## 2 · Qué falló el 11 de septiembre

La cadena mínima recuperable del run es:

| eslabón | evidencia |
|---|---|
| tarea Windows | `LastRunTime=2026-09-11T08:07:31-06:00`, `LastTaskResult=1` |
| wrapper WSL | mismo segundo, `/home/pc0/mm-adq`, `run_id=2026-09-11T080731-1157475` |
| actualización | el proceso arrancó con el runner de `899dd536` (#677), hizo fast-forward y entregó al hijo el árbol `c23dce15` (#700), que contiene el merge `b04c3881` de #704 |
| comando efectivo | `timeout --kill-after=60s 1800s claude --add-dir /home/pc0/mm-corpus -p "$PROMPT"` |
| ejecutor | `/home/pc0/.local/bin/claude`, Claude Code `2.1.267`, usuario Linux `pc0`; el PATH contiene `/home/pc0/.local/bin` |
| prerrequisitos | corpus montado; sonda INEGI `curl exit=0`, `HTTP 200`; PDN `fuera de ventana (día 11, ventana 1-3)` |
| salida del hijo | `You've hit your weekly limit · resets Sep 12, 11am (America/Mexico_City)` |
| salida del wrapper | `claude -p` terminó con código `1`; no hay marca de timeout; resultado compuesto: trabajo `exit=1`, publicación `OK` |
| heartbeat | `FAILED`, fase `FIN`, código `1`, actualizado `2026-09-11T08:08:15-06:00` |
| recibo | commit `f27bf374` en `censo/2026-09-11`; huella fusionada con SHA usado `c23dce15`, duración `37s`, `publicacion=OK` |

La causa comprobada es el límite semanal de la cuenta del ejecutor, no red,
login, ausencia del binario, timeout ni la exclusión mensual de PDN. El límite
anunció reinicio el 12 de septiembre a las 11:00, antes de la siguiente ventana
natural (lunes 14 de septiembre, 07:30). No se cambió modelo, cuenta ni límites,
no se sustituyó el ejecutor y no se gastó otra corrida funcional contra una
indisponibilidad externa ya explicada.

El campo `sha=c23dce15` identifica el árbol que consumió el hijo después del
`pull`, no la versión del shell ya cargado en memoria. Esto explica que la
huella/heartbeat históricos no tengan `disparador`: el proceso había cargado
el runner `899dd536`, anterior a esa instrumentación, aunque el agente recibió
un árbol que ya incorporaba #704.

## 3 · Tarea instalada, antes y después

La tarea existente se exportó en memoria antes de tocarla. Export SHA-256
`3f0ac617bb60fb54948284691d049d68aa177eda7891226262c62f4dafab1a7f`:

| campo | observado antes |
|---|---|
| nombre / estado | `\ModeladoMexicano\AdquiereCron` / `Ready` |
| principal | `PC0`, `Interactive`, `Limited` |
| acción | `wsl.exe -d Ubuntu -u pc0 -- bash -lc /home/pc0/mm-adq/tools/adquiere_cron.sh` |
| calendario | `07:30`, máscara `62` (lunes–viernes), host `Central Standard Time (Mexico)` |
| recuperación / concurrencia / límite | `StartWhenAvailable=True`, `IgnoreNew`, `PT2H` |
| próxima ejecución | `2026-09-14T07:30:00-06:00` |

La única divergencia material era la acción sin
`ADQ_DISPARADOR=windows-task-scheduler`. El instalador actual se ejecutó primero
con `-WhatIf`; leyó la configuración fusionada, mostró la acción corregida y no
registró cambios. Después se ejecutó una vez sin `-WhatIf`. La exportación
posterior, SHA-256
`714e03dee7d4a2bd67ce1461902c8238eecedd203fe0f4c373f0872713eeb7d7`,
conserva los demás campos materiales (el `StartBoundary` se reemitió con fecha
11/sep, sin cambiar hora, días ni próxima ejecución) y cambia la acción a:

```text
wsl.exe -d Ubuntu -u pc0 -- env ADQ_DISPARADOR=windows-task-scheduler bash -lc /home/pc0/mm-adq/tools/adquiere_cron.sh
```

`python3 tools/adq_doctor.py --json`, ejecutado con acceso real al host, confirma
zona coincidente, tarea `INSTALADA`, días/hora coincidentes, acción atribuible,
red `200`, lock libre y próxima ejecución el 14 de septiembre a las 07:30.

El doctor reportó inicialmente el cron legado como instalado porque un
comentario histórico aún menciona `adquiere_cron.sh`. `crontab -l` completo
confirma que sólo quedan esos comentarios y la asignación `PATH`; no existe una
línea ejecutable. Se corrigió el falso positivo para ignorar comentarios y se
añadió el caso de regresión.

## 4 · Atribución y recuperación que aún no pueden afirmarse

`Microsoft-Windows-TaskScheduler/Operational` estaba deshabilitado y sin
registros consultables. El intento autorizado de habilitarlo devolvió
`Acceso denegado`, código `5`; el estado siguió `IsEnabled=False`. Por ello ya
no es recuperable un `EventRecord`/`ActivityId` del 11 de septiembre. La
coincidencia exacta entre `LastRunTime`, inicio WSL y resultado `1` relaciona la
instancia de la tarea con el runner, pero no distingue si la activación fue el
trigger semanal, una recuperación de `StartWhenAvailable` o una ejecución
manual desde Task Scheduler.

El operador debe ejecutar en PowerShell **elevado** antes del lunes:

```powershell
wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true
Get-WinEvent -ListLog Microsoft-Windows-TaskScheduler/Operational |
  Select-Object LogName,IsEnabled,RecordCount,LastWriteTime
```

En la ventana natural siguiente se debe correlacionar el evento Windows
(`RecordId`, `ActivityId`, hora y causa), el `run_id`, `disparador`, SHA,
heartbeat, exit del hijo y `publicacion`. Una corrida normal atribuida no prueba
por sí sola la recuperación real de un disparo perdido; `NC-0120` conserva ese
residual y no se fabricó suspendiendo, reiniciando o cambiando el reloj.

## 5 · Conciliaciones acotadas

- `NC-0133` cierra: esta nota y `forense/cron/REGISTRO-CRON-v1_0.md` §9
  asientan canónicamente la retirada ya acreditada por #668 y comprobada de
  nuevo sobre el crontab real.
- `FP-324` permanece `FIRMADA-PARCIAL`, pero deja de decir que las cinco recetas
  siguen abiertas: la receta `DD_COMPRANET_DICCIONARIOS_DE_DATOS` quedó
  ejecutada el 10 de septiembre con tres XLSX manifestados. Son capturas
  Wayback del 16 de enero de 2025; no se presentan como edición viva. Las otras
  cuatro recetas permanecen abiertas.
- `NC-0114` sigue abierta porque falta un evento Windows que distinga la causa
  de activación. `NC-0120` sigue abierta porque el canal requiere elevación y
  aún no se observó una recuperación real. `NC-0153` conserva su estado
  `ABIERTA / OBTENIDO-PARCIAL-F3-EJECUTADA`; no se forzó a `PENDIENTE`.

## 6 · Obligaciones

| obligación | evidencia | estado | continuación |
|---|---|---|---|
| explicar `exit=1` | salida del hijo: límite semanal; wrapper `exit=1`, publicación `OK` | CUMPLIDA | capacidad se reinicia antes de la próxima ventana; no reintentar hoy |
| identificar versión y entorno | runner cargado `899dd536`; árbol del hijo `c23dce15`; Claude Code `2.1.267`, `pc0`, PATH y cwd recuperados | CUMPLIDA | ninguna |
| tarea única y configuración fusionada | exportaciones antes/después, `-WhatIf`, instalación única y doctor real | CUMPLIDA | observar la ventana del 14 de septiembre |
| atribución programada | acción futura marcada; Operational sigue apagado y el evento histórico no existe | RESERVA EXACTA | habilitar canal elevado y correlacionar evento↔run |
| recuperación real | `StartWhenAvailable=True`, pero ninguna pérdida real observada | ABIERTA (`NC-0120`) | esperar una pérdida natural; no fabricarla |
| staging ajeno | stash identificado por objeto; reaplicado con el mismo SHA y diff 392/1; respaldo retenido | PRESERVADO Y RESTITUIDO | ninguna |
| retiro del cron legado | `crontab -l` sin línea ejecutable; registro §9 | CUMPLIDA (`NC-0133`) | ninguna |
| diccionarios CompraNet | tres ids manifestados, snapshot 2025-01-16 | CUMPLIDA SÓLO PARA ESA RECETA | edición viva no afirmada; cuatro recetas de `FP-324` siguen abiertas |

La próxima adquisición está técnicamente desplegada para correr con la
configuración vigente, siempre que la sesión Windows `Interactive` permanezca
abierta y haya capacidad del ejecutor. No puede contarse todavía como corrida
programada **atribuida** hasta habilitar Operational y observar la ventana
natural.
