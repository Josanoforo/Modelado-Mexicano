<#
.SYNOPSIS
    Habilita únicamente el canal Operational de Task Scheduler y deja evidencia.

.DESCRIPTION
    Debe ejecutarse elevado. No registra ni modifica tareas, principales,
    acciones o triggers. La elevación se limita a `wevtutil sl ... /e:true`.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$EvidencePath
)

$ErrorActionPreference = "Stop"
$channel = "Microsoft-Windows-TaskScheduler/Operational"

& wevtutil.exe sl $channel /e:true
if ($LASTEXITCODE -ne 0) {
    throw "wevtutil terminó con código $LASTEXITCODE"
}

$log = Get-WinEvent -ListLog $channel
$evidence = [ordered]@{
    recorded_at = (Get-Date).ToString("o")
    elevated_identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    log_name = $log.LogName
    is_enabled = $log.IsEnabled
    record_count = $log.RecordCount
    last_write_time = $log.LastWriteTime
    scope = "event-channel-only; scheduled task unchanged"
}

$evidence | ConvertTo-Json | Set-Content -LiteralPath $EvidencePath -Encoding UTF8
$evidence | ConvertTo-Json

if (-not $log.IsEnabled) {
    throw "$channel continúa deshabilitado"
}
