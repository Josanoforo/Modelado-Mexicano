# GEN2-SONDA-CRON-PRODUCCION-POST693 · evidencia y cierre de alcance

Fecha local: 2026-09-10. Entorno: CAJA, Ubuntu/WSL2 y Windows host.

## Resultado de configuración

`data/adq-config.yaml:calendario` es la autoridad única de hora, días y
traducción de zona: 07:30, lunes-viernes, `America/Mexico_City` y
`Central Standard Time (Mexico)`. `tools/adq_config.py` valida y normaliza
esa autoridad para instalador, runner, doctor y T31. Una configuración
inválida declara causa, fuente y valor de respaldo aplicado.

Los límites ya no se confunden:

| límite | valor vigente | precedencia |
|---|---:|---|
| proceso del ejecutor | 1800 s | `CLAUDE_TIMEOUT_SEGUNDOS` > YAML > respaldo compatible |
| gracia TERM→KILL | 60 s | `CLAUDE_KILL_AFTER_SEGUNDOS` > YAML > respaldo compatible |
| observación de huella después de 07:30 | 45 min | calendario YAML > respaldo compatible |

El runner fija `TZ` desde el calendario, etiqueta `disparador`, conserva
`run_id` y SHA en heartbeat/recibo, y diferencia `TIMEOUT-PROCESO` de
`TIMEOUT-KILL`. El instalador añade
`ADQ_DISPARADOR=windows-task-scheduler` a la acción y se rehúsa a registrar
si `tzutil /g` no coincide con la traducción configurada.

## Estado real antes de instalar el cambio

Consulta de solo lectura a `\ModeladoMexicano\AdquiereCron`:

| campo | observado |
|---|---|
| estado / principal | `Ready` / `PC0`, `Interactive`, `Limited` |
| acción | `wsl.exe -d Ubuntu -u pc0 -- bash -lc /home/pc0/mm-adq/tools/adquiere_cron.sh` |
| calendario | inicio `2026-09-07T07:30:00-06:00`, máscara `62` (lunes-viernes) |
| zona Windows | `Central Standard Time (Mexico)` |
| política | `StartWhenAvailable=True`, `MultipleInstances=IgnoreNew`, límite `PT2H` |
| última / próxima | `2026-09-10T09:05:41-06:00`, resultado `0` / `2026-09-11T07:30:00-06:00` |

El clon productivo era `/home/pc0/mm-adq`, rama `main`, HEAD `899dd536`
(merge #677), con `data/manifiesto-staging.yaml` modificado y ajeno. No se
descartó ni se movió. No había proceso `adquiere_cron.sh` ni `claude -p`
activo; sí había cálculos Codex ajenos, que no se interrumpieron. El crontab
legado no contiene el runner: conserva sólo el `PATH` histórico.

El instalador nuevo se ejecutó una vez con `-WhatIf` contra el worktree de
esta rama. Leyó 07:30, cinco días y ambas zonas del YAML, confirmó la zona
Windows y mostró la nueva acción atribuible; `ShouldProcess` confirmó que no
registró cambios. La instalación productiva se difiere hasta que este código
esté fusionado y `/home/pc0/mm-adq` pueda actualizarse sin perder su staging.

## Corrida real ya existente y alcance de atribución

`LastRunTime` coincide al segundo con el log WSL:

| eslabón | evidencia |
|---|---|
| instancia de la tarea | inicio informado por Windows: `2026-09-10 09:05:41 -06:00`, resultado `0` |
| runner WSL | `/home/pc0/mm-adq`, `run_id=2026-09-10T090541-261457` |
| versión | `HEAD tras pull: 899dd536` |
| cierre | `2026-09-10 09:21:44 -06:00`, heartbeat `TERMINADO`, fase `FIN`, exit `0` |
| publicación | commit/recibo `a2c6ca642431682e3220bf9e4ae7c3366882cfde`, rama `censo/2026-09-10` |
| demanda | `DD_COMPRANET_DICCIONARIOS_DE_DATOS`, tres XLSX públicos obtenidos y manifestados por la corrida |

Esto acredita que la tarea Windows lanzó la acción que inició el runner, por
coincidencia exacta de ruta y tiempo. No acredita si esa instancia fue el
disparo semanal, una recuperación tardía o un clic manual: el runner anterior
no escribía `disparador` y el canal Operational estaba deshabilitado.

## Recuperación y canal Operational

`Microsoft-Windows-TaskScheduler/Operational` devolvió
`IsEnabled=False`, sin registros consultables. Habilitación exacta, a ejecutar
en PowerShell **elevado** por el operador:

```powershell
wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true
Get-WinEvent -ListLog Microsoft-Windows-TaskScheduler/Operational |
  Select-Object LogName,IsEnabled,RecordCount,LastWriteTime
```

Se hizo una sonda aislada, sin runner ni modelo: tarea temporal con trigger
dos minutos vencido, `StartWhenAvailable=True` y acción que sólo escribía un
marcador en `%TEMP%`. Tras 20 s no ejecutó (`LastRunTime` centinela de 1999,
`LastTaskResult=267011`, marcador ausente, `NumberOfMissedRuns=0`). La tarea y
el marcador se eliminaron en `finally`. Resultado: recuperación **no
observada**; no se generaliza desde `StartWhenAvailable=True` ni desde esta
sonda negativa. Verificación posterior: `RecoveryProbesRemaining=0`; la tarea
productiva siguió `Ready`, con sus argumentos originales y
`StartWhenAvailable=True`.

## Pruebas y continuación

- `test_adq_config.py`: 7/7; próxima hora, cambio de día/zona, inválidos y override.
- `test_t_cron.py`: 10/10.
- `test_adq_doctor.py`: 7/7; incluye coincidencia/divergencia de tarea.
- `test_adq_cableado.py`: 27/27; incluye doble lanzamiento, red y proceso
  aislado que ignora TERM sin matar procesos ajenos.
- `test_adq_contrato_fix.py`: 20/20; incluye ejecutor/publicación fallidos.
- `bash -n tools/adquiere_cron.sh` y `git diff --check`: sin errores.
- `python3 tests/check.py --baseline`: sin delta nuevo; sólo los tres FAIL
  históricos T06×2/T08×1.

Fase 4 queda compuertada al merge de PR #695 por instrucción adicional de
mesa. No se duplica su investigación de NC-0153. Después del merge se integra
`origin/main` y se consume la fila/resultado real para demostrar selección o
diferimiento y recibo.

Instalación productiva, después del merge de este cambio y preservando primero
`data/manifiesto-staging.yaml` en `/home/pc0/mm-adq`:

```powershell
cd \\wsl.localhost\Ubuntu\home\pc0\mm-adq
powershell -ExecutionPolicy Bypass -File tools\windows\instala-tarea-adquisicion.ps1 -WhatIf
powershell -ExecutionPolicy Bypass -File tools\windows\instala-tarea-adquisicion.ps1
```

Luego se verifica `scheduler_windows` y la siguiente corrida con:

```bash
python3 tools/adq_doctor.py --json
```
