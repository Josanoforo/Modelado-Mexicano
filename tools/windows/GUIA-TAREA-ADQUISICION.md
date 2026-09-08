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

El script es idempotente (`Register-ScheduledTask ... -Force`): correrlo
de nuevo actualiza la tarea existente, no la duplica.

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
`ClonPath=/home/pc0/mm-adq`, `HoraLocal=07:30`,
`NombreTarea=\ModeladoMexicano\AdquiereCron`, `LogonType=Interactive`).

**Supuesto que el script NO verifica solo**: que el reloj/zona horaria de
Windows ya está en `America/Mexico_City` — Task Scheduler dispara en hora
LOCAL del sistema, sin campo de zona horaria explícito como cron.
`python3 tools/adq_doctor.py` reporta la zona horaria del lado de WSL;
compárala contra `tzutil /g` en Windows si hay duda.
