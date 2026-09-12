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

    Hora, días y zona vienen de `data/adq-config.yaml:calendario`. El
    instalador traduce días con el lector común y exige que `tzutil /g`
    coincida con el id Windows asociado a la zona IANA antes de registrar.

    La acción usa un único PowerShell oculto y no interactivo como envoltura
    de `wsl.exe`. La envoltura espera al proceso WSL real y devuelve su código
    de salida; Task Scheduler no confunde "se creó el proceso" con "terminó
    bien la adquisición". No cambia el principal ni sus permisos.

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

.PARAMETER WindowsUser
    Principal de Windows. Si se omite y la tarea ya existe, conserva su
    UserId actual; sólo usa la identidad de la consola al crearla por primera
    vez. Esto evita cambiar el principal si el instalador se lanza con UAC.

.PARAMETER DeploymentRevision
    SHA publicado que debe conservarse mientras main no lo contenga. El
    launcher cambia automáticamente a origin/main cuando ese SHA ya es
    ancestro de main. Vacío significa seguir main.

.PARAMETER ClonPath
    Ruta ABSOLUTA de Linux al clon de mesa dentro de WSL (default:
    /home/pc0/mm-adq).

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
    [string]$WindowsUser = "",
    [string]$ClonPath = "/home/pc0/mm-adq",
    [string]$NombreTarea = "\ModeladoMexicano\AdquiereCron",
    [string]$DeploymentRevision = "",
    [ValidateSet("Interactive", "S4U")]
    [string]$LogonType = "Interactive"
)

$ErrorActionPreference = "Stop"

# Una sola autoridad: PowerShell no parsea YAML ni repite calendario. El
# lector compartido valida, normaliza días y entrega el id Windows asociado
# a la zona IANA. Un respaldo compatible siempre queda declarado.
$CalendarioJson = & wsl.exe -d $Distro -u $LinuxUser -- `
    python3 "$ClonPath/tools/adq_config.py" --calendario-json
if ($LASTEXITCODE -ne 0) {
    throw "No se pudo leer data/adq-config.yaml mediante tools/adq_config.py (exit=$LASTEXITCODE)."
}
$Calendario = $CalendarioJson | ConvertFrom-Json
$ZonaWindowsActual = (& tzutil.exe /g).Trim()
if ($ZonaWindowsActual -ne $Calendario.zona_windows) {
    throw ("Zona Windows incompatible: actual='{0}', configuración IANA='{1}' " +
           "requiere Windows='{2}'. No se registra una hora accidental del host." -f `
           $ZonaWindowsActual, $Calendario.zona_iana, $Calendario.zona_windows)
}
if ($Calendario.degradada) {
    Write-Warning ("CONFIG-DEGRADADA: {0}; valores aplicados: {1} {2}, días={3}, " +
                   "zona_windows={4}" -f $Calendario.causa, $Calendario.hora,
                   $Calendario.zona_iana, ($Calendario.dias_semana -join ','),
                   $Calendario.zona_windows)
}

$partes = $NombreTarea.Trim('\') -split '\\'
if ($partes.Count -eq 1) {
    $TaskFolder = "\"
    $TaskName = $partes[0]
} else {
    $TaskFolder = "\" + ($partes[0..($partes.Count - 2)] -join '\') + "\"
    $TaskName = $partes[-1]
}

$Existente = Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolder -ErrorAction SilentlyContinue
if ([string]::IsNullOrWhiteSpace($WindowsUser)) {
    if ($Existente) {
        $WindowsUser = $Existente.Principal.UserId
    } else {
        $WindowsUser = $env:USERNAME
    }
}

Write-Host "Tarea:            $TaskFolder$TaskName"
Write-Host "Distro WSL:       $Distro"
Write-Host "Usuario Linux:    $LinuxUser"
Write-Host "Clon:             $ClonPath"
Write-Host "Calendario:       $($Calendario.hora) $($Calendario.zona_iana) [$($Calendario.dias_semana -join ',')]"
Write-Host "Zona Windows:     $ZonaWindowsActual (traducción configurada: $($Calendario.zona_windows))"
Write-Host "Principal:        $WindowsUser (LogonType=$LogonType)"
Write-Host "Revision:         $($DeploymentRevision -replace '^$', 'origin/main')"

$Variables = "ADQ_DISPARADOR=windows-task-scheduler"
if (-not [string]::IsNullOrWhiteSpace($DeploymentRevision)) {
    $Variables += " ADQ_DEPLOY_REVISION=$DeploymentRevision"
}
$ArgumentosWsl = ("-d $Distro -u $LinuxUser -- env $Variables " +
                  "bash -lc $ClonPath/tools/adquiere_launcher.sh")

# Task Scheduler corre con LogonType=Interactive porque es la identidad ya
# acreditada de esta caja. Eso no obliga a mostrar una consola: PowerShell se
# inicia oculto y sin interacción, invoca WSL de forma síncrona y propaga su
# código real. El operador `&` espera a wsl.exe; no se usa Start-Process sin
# -Wait ni un cmd /c start que pudiera devolver éxito al mero arranque.
$ComandoOculto = @"
& wsl.exe $ArgumentosWsl
if (`$null -eq `$LASTEXITCODE) { exit 1 }
exit [int]`$LASTEXITCODE
"@
$ComandoCodificado = [Convert]::ToBase64String(
    [Text.Encoding]::Unicode.GetBytes($ComandoOculto))
$PowerShellExe = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$ArgumentosPowerShell = ("-NoLogo -NoProfile -NonInteractive " +
                         "-WindowStyle Hidden -EncodedCommand $ComandoCodificado")
$Action = New-ScheduledTaskAction -Execute $PowerShellExe -Argument $ArgumentosPowerShell

$HoraParsed = [datetime]::ParseExact($Calendario.hora, "HH:mm", $null)
$DiasWindows = @($Calendario.dias_windows)
$Trigger = New-ScheduledTaskTrigger -Weekly `
    -DaysOfWeek $DiasWindows `
    -At $HoraParsed

$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

$Principal = New-ScheduledTaskPrincipal -UserId $WindowsUser -LogonType $LogonType -RunLevel Limited

if ($PSCmdlet.ShouldProcess("$TaskFolder$TaskName", "Register-ScheduledTask")) {
    Register-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolder `
        -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal `
        -Description ("Runner de adquisicion (tools/adquiere_cron.sh). Calendario autoritativo " +
                       "data/adq-config.yaml: $($Calendario.hora) $($Calendario.zona_iana), " +
                       "dias=$($Calendario.dias_semana -join ','). StartWhenAvailable habilitado.") `
        -Force | Out-Null
    Write-Host ""
    Write-Host "Tarea registrada/actualizada: $TaskFolder$TaskName"
    Write-Host ""
    Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolder | Format-List TaskName, State
    Get-ScheduledTaskInfo -TaskName $TaskName -TaskPath $TaskFolder | Format-List LastRunTime, LastTaskResult, NextRunTime
} else {
    Write-Host ""
    Write-Host "-WhatIf: no se registró nada. Argumentos que se habrían usado:"
    Write-Host "  $PowerShellExe -NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -EncodedCommand <omitido>"
    Write-Host "  comando síncrono codificado: & wsl.exe $ArgumentosWsl; exit `$LASTEXITCODE"
    $existente = Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolder -ErrorAction SilentlyContinue
    if ($existente) {
        Write-Host ""
        Write-Host "(la tarea ya existía antes de este -WhatIf, estado actual:)"
        $existente | Format-List TaskName, State
    }
}
