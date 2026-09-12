# Windows Task Scheduler como disparador autoritativo del cron de adquisición

`ACTO ADQ-CRON-V2 · DISPARO-PERSISTENTE-Y-RUNNER-IDEMPOTENTE` (P2, 7/sep/2026).

## Por qué

El 7/sep/2026 la VM ligera de WSL2 quedó suspendida durante la ventana de
las 07:30 y el cron clásico (`vixie-cron`), que corre DENTRO de esa VM,
nunca tuvo oportunidad de dispararse ni de reintentar — no tiene
semántica de recuperación. Diagnóstico completo, con la evidencia cruda
del journal: `forense/notas/2026-09-07-ADQ-CRON-V2-diagnostico.md`
(clasificación: `SCHEDULER-NO-LANZO`).

Windows Task Scheduler corre en el host, no dentro de la VM que puede
suspenderse, e invocar `wsl.exe` desde una tarea **sí arranca la VM** si
estaba dormida (comportamiento nativo de WSL2) — y trae
`StartWhenAvailable`, que recupera un disparo perdido en cuanto Task
Scheduler vuelve a poder evaluar la tarea.

## Instalar / actualizar

Desde una consola de PowerShell en Windows (no hace falta ser
Administrador — ver "Tipo de logon" abajo):

```powershell
cd \\wsl.localhost\Ubuntu\home\pc0\mm-adq
powershell -ExecutionPolicy Bypass -File tools\windows\instala-tarea-adquisicion.ps1 -WhatIf   # revisa primero
powershell -ExecutionPolicy Bypass -File tools\windows\instala-tarea-adquisicion.ps1            # instala de verdad
```

Mientras una revisión autorizada siga en PR, pásala de forma explícita:

```powershell
powershell -ExecutionPolicy Bypass -File tools\windows\instala-tarea-adquisicion.ps1 `
  -WindowsUser PC0 -LinuxUser pc0 -DeploymentRevision <SHA-publicado>
```

La tarea llama `tools/adquiere_launcher.sh`. El launcher toma el mismo lock,
actualiza referencias y sólo entonces carga el runner de ese SHA. Cuando
`origin/main` ya contiene la revisión fijada, cambia automáticamente a main;
no hay descenso a una versión Claude entre ambos pasos. Un checkout que
choque con trabajo ajeno aborta sin `reset` ni `clean`.

El launcher crea el `run_id` y el heartbeat local antes de `git fetch` y
propaga esa misma identidad al runner. Así, un fallo de fetch/checkout conserva
fase, revisión conocida o desconocida, timestamps, motivo y el código original;
el doctor no reutiliza como si fuera actual el éxito de una corrida anterior.
Una segunda instancia rechazada por el lock sólo escribe en `launcher.log` y no
pisa el heartbeat del dueño.

La acción registrada no abre una consola: un solo `powershell.exe` con
`-NonInteractive -WindowStyle Hidden` invoca `wsl.exe` sin desprenderlo, espera
su terminación y sale con su código real. `Interactive` describe la sesión y el
principal de la tarea, no una ventana visible ni éxito al mero arranque. El
timeout de Task Scheduler conserva así el árbol de procesos bajo la tarea; el
runner mantiene además `flock`, `timeout --kill-after` y los logs locales.

Si el selector determinista devuelve cero elegidos, el runner publica la
selección, sus exclusiones y el recibo `invocado=no` sin llamar a ningún LLM.
`publicacion_trabajo` (objetos/intentos del agente) y `publicacion` (recibo del
wrapper) son cierres distintos.

El script es idempotente (`Register-ScheduledTask ... -Force`): correrlo
de nuevo actualiza la tarea existente, no la duplica.

Si la tarea existe, su principal se conserva aunque la consola actual sea una
cuenta elevada distinta. `-WindowsUser` permite declararlo explícitamente; en
esta caja productiva es `PC0`, `Interactive`, `Limited`, y el usuario WSL es
independientemente `pc0`.

Hora, días y traducción de zona se leen únicamente de
`data/adq-config.yaml:calendario` mediante `tools/adq_config.py`. El
instalador compara `tzutil /g` con `calendario.zona_windows` y se detiene
si no coincide: no registra 07:30 en la zona accidental del host.

## Tipo de logon: `Interactive` (default) vs. `S4U`

Medido en esta máquina, no supuesto: `S4U` (correría con la sesión de
Windows cerrada, sin contraseña almacenada) exige el privilegio "Log on
as a batch job" — en esta cuenta (usuario estándar, no administrador),
`Register-ScheduledTask -LogonType S4U` sale con **"Acceso denegado"
(0x80070005)**, incluso sin elevar PowerShell.

Default de este instalador: `-LogonType Interactive`. Registra sin
admin, con esta contrapartida real: **la tarea solo dispara si hay una
sesión de Windows iniciada de esa cuenta en ese momento** — no es
"corre pase lo que pase", es "corre sin que nadie tenga que tocar nada,
mientras la sesión esté abierta" (lo normal en una estación de trabajo
personal).

Para que corra también con la sesión cerrada:
1. Conceder el privilegio a la cuenta: `secpol.msc` → Directivas locales
   → Asignación de derechos de usuario → "Iniciar sesión como trabajo por
   lotes" → añadir la cuenta.
2. Volver a correr el instalador con `-LogonType S4U`.

(O ejecutar el instalador una sola vez como Administrador — elevar
PowerShell suele bastar para que `Register-ScheduledTask -LogonType S4U`
no choque con el mismo permiso.)

## Verificar

```powershell
schtasks /Query /TN "\ModeladoMexicano\AdquiereCron" /V /FO LIST
```

o, desde WSL, con el reporte de solo lectura de este mismo programa:

```bash
python3 tools/adq_doctor.py
```

(sección `scheduler_windows` — reporta `NO-VERIFICABLE`, nunca
`no instalado`, si `/mnt/c` no es legible desde donde corre `adq_doctor`,
p.ej. dentro de un sandbox restringido).

## Retirar el crontab de WSL (después de verificar P7)

**No se retira solo con instalar esta tarea.** `P2` pide "evitar un
segundo scheduler diario activo que pueda duplicar ejecuciones" — el
propio lock de instancia única de `tools/adquiere_cron.sh` (`flock`, P3)
evita una corrida duplicada si ambos disparadores coincidieran alguna
vez, pero mantener los dos activos indefinidamente es ruido, no defensa.

Orden recomendado:
1. Confirmar, con evidencia real (no solo "el `-WhatIf` se veía bien"),
   que esta tarea disparó sola al menos una vez sin intervención humana
   (`python3 tools/adq_doctor.py` → sección `t_cron` en `COMPLETO`, o el
   heartbeat/log del día con `run_id` que no corresponda a una invocación
   manual).
2. Retirar la línea de `crontab -e` en `mm-adq` (la de
   `forense/cron/REGISTRO-CRON-v1_0.md` §2) — dejar el resto del crontab
   (tareas de sistema como `cron.hourly`) intacto.
3. Documentar la retirada (fecha, quién, con qué evidencia de (1)) en
   `forense/cron/REGISTRO-CRON-v1_0.md`.

## Desinstalar

```powershell
Unregister-ScheduledTask -TaskName "AdquiereCron" -TaskPath "\ModeladoMexicano\" -Confirm:$false
```

## Parámetros del instalador

Ver `Get-Help .\instala-tarea-adquisicion.ps1 -Full` — todos tienen
default sensato para esta máquina (`Distro=Ubuntu`, `LinuxUser=pc0`,
`ClonPath=/home/pc0/mm-adq`,
`NombreTarea=\ModeladoMexicano\AdquiereCron`, `LogonType=Interactive`).
`WindowsUser` conserva el principal existente y `DeploymentRevision` permite
fijar un SHA publicado hasta que main lo incorpore.

El calendario efectivo se consulta con `python3 tools/adq_doctor.py --json`
en `configuracion_operativa`; `scheduler_windows` contrasta hora, máscara de
días, argumentos atribuibles, envoltura oculta, espera/propagación,
`StartWhenAvailable` y ausencia de triggers temporales contra la tarea
instalada. Zona, tarea y estado del canal Operational comparten una sola
consulta PowerShell oculta por ejecución del doctor; para observar progreso se
lee `forense/adq-log/estado/heartbeat.json`, sin sondear Windows repetidamente.
