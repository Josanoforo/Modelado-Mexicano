<#
.SYNOPSIS
    Instala/actualiza la tarea de Windows Task Scheduler que reemplaza a
    cron dentro de WSL como disparador autoritativo del runner de
    adquisición (ACTO ADQ-CRON-V2 · DISPARO-PERSISTENTE-Y-RUNNER-
    IDEMPOTENTE, P2, 7/sep/2026).

.DESCRIPTION
    Por qué existe: el 7/sep/2026 la VM ligera de WSL2 quedó suspendida
    durante la ventana de las 07:30 y el cron clásico (vixie-cron), que
    corre DENTRO de esa VM, nunca tuvo oportunidad de dispararse ni de
    reintentar -- no tiene semántica de recuperación (ver
    forense/notas/2026-09-07-ADQ-CRON-V2-diagnostico.md). Windows Task
    Scheduler corre en el HOST, no dentro de la VM que puede
    suspenderse, e invocar `wsl.exe` desde una tarea SÍ arranca la VM si
    estaba dormida (comportamiento nativo de WSL2) -- y trae
    `StartWhenAvailable`, que este script activa explícitamente, para
    recuperar una hora perdida (p.ej. la máquina encendió tarde) en
    cuanto Task Scheduler pueda volver a evaluar la tarea.

    `bash -lc <script>`, no el script suelto: `wsl.exe -- <comando>` NO
    ejecuta como shell de login por defecto y no hereda el `PATH` de
    `~/.profile`/`~/.bashrc` -- exactamente la misma lección ya aprendida
    con el `PATH=` explícito del crontab (`forense/cron/
    REGISTRO-CRON-v1_0.md` §2/§5.5): sin `-l`, `claude`
    (`/home/pc0/.local/bin/claude`) no resuelve.

    Tipo de logon -- medido en esta máquina, no supuesto: `S4U` (correría
    sin sesión interactiva ni contraseña almacenada) exige el privilegio
    "Log on as a batch job", que en esta cuenta (usuario estándar, no
    administrador) `Register-ScheduledTask` rechaza con "Acceso
    denegado" (0x80070005) incluso sin elevar PowerShell -- confirmado
    con una tarea de prueba mínima antes de fijar el default. `Interactive`
    (el default de este script) SÍ registra sin admin, con la
    contrapartida real: la tarea solo dispara si hay una sesión de
    Windows iniciada de esa cuenta en ese momento -- no es "siempre
    corre pase lo que pase", es "corre sin que nadie tenga que hacer
    nada, mientras la sesión esté abierta" (lo normal en una estación de
    trabajo personal). Si más adelante se concede el privilegio de logon
    por lote a esta cuenta (Política de seguridad local → Asignación de
    derechos de usuario → "Iniciar sesión como trabajo por lotes") o se
    ejecuta este instalador una vez como Administrador, pasar
    `-LogonType S4U` habilita el disparo también con la sesión cerrada.

    `MultipleInstances=IgnoreNew` es una segunda capa sobre el lock
    propio de `flock` que ya trae `tools/adquiere_cron.sh` (P3) -- si
    Task Scheduler mismo intenta lanzar una segunda instancia mientras la
    primera sigue viva, ni siquiera llega a invocar `wsl.exe`.

    NO instala un segundo scheduler activo en paralelo por sí solo: este
    script no toca el crontab de WSL. Retirar el crontab, una vez
    verificado que esta tarea corre de verdad (P7), es un paso manual --
    ver `tools/windows/GUIA-TAREA-ADQUISICION.md`.

.PARAMETER Distro
    Nombre de la distro de WSL a invocar (default: "Ubuntu").

.PARAMETER LogonType
    "Interactive" (default, no requiere admin -- ver arriba) o "S4U"
    (corre con la sesión cerrada, requiere el privilegio de logon por
    lote en esta cuenta o ejecutar el instalador elevado).

.PARAMETER LinuxUser
    Usuario DENTRO de WSL bajo el que corre el runner (default: "pc0").
    No tiene por qué coincidir con la cuenta de Windows que registra la
    tarea -- son dos identidades distintas.

.PARAMETER ClonPath
    Ruta ABSOLUTA de Linux al clon de mesa dentro de WSL (default:
    /home/pc0/mm-adq).

.PARAMETER HoraLocal
    Hora de disparo en HH:mm, hora LOCAL del sistema Windows (default
    07:30). Task Scheduler dispara en hora local del sistema, no lleva
    zona horaria explícita -- este script asume que el reloj de Windows
    ya está en America/Mexico_City (mismo supuesto que el resto del
    programa hace del lado de WSL); `python3 tools/adq_doctor.py`
    reporta la zona horaria de ambos lados para poder verificarlo.

.PARAMETER NombreTarea
    Ruta completa de la tarea dentro de Task Scheduler (default:
    "\ModeladoMexicano\AdquiereCron"). Debe coincidir con
    ADQ_TASK_SCHEDULER_NOMBRE que lee `tools/adq_doctor.py` si se cambia.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\windows\instala-tarea-adquisicion.ps1
    powershell -ExecutionPolicy Bypass -File tools\windows\instala-tarea-adquisicion.ps1 -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Distro = "Ubuntu",
    [string]$LinuxUser = "pc0",
    [string]$ClonPath = "/home/pc0/mm-adq",
    [string]$HoraLocal = "07:30",
    [string]$NombreTarea = "\ModeladoMexicano\AdquiereCron",
    [ValidateSet("Interactive", "S4U")]
    [string]$LogonType = "Interactive"
)

$ErrorActionPreference = "Stop"

$partes = $NombreTarea.Trim('\') -split '\\'
if ($partes.Count -eq 1) {
    $TaskFolder = "\"
    $TaskName = $partes[0]
} else {
    $TaskFolder = "\" + ($partes[0..($partes.Count - 2)] -join '\') + "\"
    $TaskName = $partes[-1]
}

Write-Host "Tarea:            $TaskFolder$TaskName"
Write-Host "Distro WSL:       $Distro"
Write-Host "Usuario Linux:    $LinuxUser"
Write-Host "Clon:             $ClonPath"
Write-Host "Hora local:       $HoraLocal (asume reloj de Windows ya en America/Mexico_City)"
Write-Host "Principal:        $env:USERNAME (LogonType=$LogonType)"

$Argumentos = "-d $Distro -u $LinuxUser -- bash -lc $ClonPath/tools/adquiere_cron.sh"
$Action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument $Argumentos

$HoraParsed = [datetime]::ParseExact($HoraLocal, "HH:mm", $null)
$Trigger = New-ScheduledTaskTrigger -Weekly `
    -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
    -At $HoraParsed

$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType $LogonType -RunLevel Limited

if ($PSCmdlet.ShouldProcess("$TaskFolder$TaskName", "Register-ScheduledTask")) {
    Register-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolder `
        -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal `
        -Description ("ACTO ADQ-CRON-V2 (7/sep/2026) -- disparador autoritativo del runner de " +
                       "adquisicion (tools/adquiere_cron.sh), reemplaza a cron dentro de WSL. " +
                       "StartWhenAvailable recupera una hora perdida.") `
        -Force | Out-Null
    Write-Host ""
    Write-Host "Tarea registrada/actualizada: $TaskFolder$TaskName"
    Write-Host ""
    Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolder | Format-List TaskName, State
    Get-ScheduledTaskInfo -TaskName $TaskName -TaskPath $TaskFolder | Format-List LastRunTime, LastTaskResult, NextRunTime
} else {
    Write-Host ""
    Write-Host "-WhatIf: no se registró nada. Argumentos que se habrían usado:"
    Write-Host "  wsl.exe $Argumentos"
    $existente = Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolder -ErrorAction SilentlyContinue
    if ($existente) {
        Write-Host ""
        Write-Host "(la tarea ya existía antes de este -WhatIf, estado actual:)"
        $existente | Format-List TaskName, State
    }
}
