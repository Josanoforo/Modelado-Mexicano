# Extractos saneados

Corte inicial: 2026-09-19T15:48:13-06:00. No se incluyen tokens, JSONL del
ejecutor, prompts, microdatos ni el XML completo de la tarea.

## Tarea antes de corregir

```text
tarea=\ModeladoMexicano\AdquiereCron
estado=Ready
principal=PC0 logon=Interactive run_level=Limited
accion=powershell.exe oculto/no interactivo -> wsl.exe -d Ubuntu -u pc0
revision_solicitada=3f759e5e2feee0d5b42892b88bb19b2b0b8542e6
triggers=diario 07:30 (7 días); repetición PT1H; inicio de sesión
StartWhenAvailable=true MultipleInstances=IgnoreNew ExecutionTimeLimit=PT2H
LastRunTime=2026-09-19T15:00:01-06:00
LastTaskResult=1
NextRunTime=2026-09-19T16:00:00-06:00
```

Exportación previa preservada localmente en
`C:\Users\PC0\AppData\Local\Temp\AdquiereCron-before-20260919.xml`, SHA-256
`5AE50FD0F7A40E32C65906464A1025FB345E0C45EBC6AE66653F1EB229D7F7A5`.

El crontab real sólo contiene `PATH=...` y comentarios: no contiene línea
ejecutable ni segundo disparador.

## Correlación TaskScheduler / WSL

```text
2026-09-18 08:29:49-06  Event 119 Record 16021
Activity {5a6080b1-2c28-4e9a-93cf-2b4b7e86f10f}: inicio por logon PC0
WSL run_id=2026-09-18T083018-433, inicio=08:30:18, fin=08:51:58
Event 201 Record 16554: ResultCode=0

2026-09-19 13:00:01-06  Event 107 Record 19341
Activity {36edcf5d-2fa2-405a-bbe8-5d9757892025}: trigger horario
WSL run_id=2026-09-19T130002-152997, fin=13:00:04, exit=1

2026-09-19 14:00:01-06  Event 107 Record 19447
Activity {ce20a9a4-6015-4976-8f39-153263058849}: trigger horario
WSL run_id=2026-09-19T140002-207775, fin=14:13:54, exit=1

2026-09-19 15:00:01-06  Event 107 Record 19572
Activity {6c85e5a9-e780-4aa0-9586-7ca22244b7a1}: trigger horario
WSL run_id=2026-09-19T150008-343, fin=15:14:27, exit=1
```

Los `ResultCode=2147942401` de Windows equivalen a la salida `1` propagada por
PowerShell; el log WSL identifica el fallo real. Los eventos 100/200 y 201/102
comparten ActivityId con cada inicio/cierre. La atribución no depende de la
variable `ADQ_DISPARADOR`.

## Excepción material

```text
ValueError: Invalid isoformat string:
'EVENTO: firma de mesa sobre el pin canónico de RES-0047/RES-0049'
fase=COMPROBACION-LIGERA motivo=comprobacion-fallida exit=1
```

El valor proviene del estado versionado de `NC-0244`. Es una espera por evento
humano válida, no una fecha mal capturada. Se observó desde la activación de
09:00 del 18/sep y en todas las comprobaciones posteriores.

## Último trabajo real anterior

```text
run_id=2026-09-18T083018-433 exit=0
investigaciones seleccionadas/iniciadas/validadas=3/3/3
objetos intentados/adquiridos=0/0; bytes nuevos=0
evidencia nueva=3; reducción de brecha=0
publicacion_trabajo=publicada; resultado=descubrimiento_documentado
validador=candidatos_validos_iguales; last-message y handoff válidos
presupuesto reservado=3/5/3900s; consumido=3/0/620s;
devuelto=0/5/3280s; reserva activa=0
```

La ref de trabajo `426ef41ebcf3b7b8176dbb53fa68d2f361b46d20` y su
merge `9eff694ecff8e74d2aed05fe5fac9e4d530363fc` son ancestros de
`origin/main`. La rama diaria ya fue eliminada; la publicación permanece en
la historia consolidada.

## Prueba manual separada

```text
DERIVA_PUBLICAR=0 MM_TRAMO=derivacion ADQ_DISPARADOR=manual \
ADQ_CAUSA_DISPARO=verificacion-operativa \
ADQ_DEPLOY_REVISION=6ab4cbe78ca31aa70eb93c490a1d43af01219736 \
bash tools/adquiere_launcher.sh

run_id launcher=2026-09-19T155327-51633
run_id derivación=2026-09-19T155328-51770
sha efectivo=6ab4cbe78ca31aa70eb93c490a1d43af01219736
resultado=NADA-QUE-HACER-YA-COMPLETADO; exit=0; publicación desactivada
```

El primer intento manual, a las 15:53:06, falló en `LAUNCHER-FETCH` con
`exit=128` porque la red del sandbox no resolvió GitHub; se conservó como
evidencia y se repitió una vez con red autorizada. No invocó modelo ni tocó
presupuesto.

Ya sobre el SHA efectivo, `python3 tools/adq_investigacion.py
--comprueba-despacho` terminó `exit=0` y produjo JSON válido. Fue una
comprobación determinista: no invocó modelo, no descargó y no consumió
presupuesto.

## Trigger natural posterior a la corrección

```text
2026-09-19 16:00:01-06  Event 107 Record 19901
Activity {2cc74291-aaf4-469c-bcf9-ec8e55cf1f7a}: trigger horario
Events 100/200 Records 19903/19904: instancia y acción iniciadas
WSL run_id=2026-09-19T160001-63807
revision efectiva=6ab4cbe78ca31aa70eb93c490a1d43af01219736
derivación run_id=2026-09-19T160003-63890 exit=0 duración=927s
resultado derivación=CAMBIOS-DIFERIDOS-PR-DIARIO-YA-FUSIONADO
selección=DEM-AHORRO-STOCK-DURACION-01,NC-0202,NC-0253
NC-0244=excluida por revisión basada en EVENTO
2026-09-19 16:25:01-06  Events 201/102 Records 20004/20005
código Windows=2147942465; código hijo=65
```

El código 65 no reproduce el defecto reparado. El ejecutor publicó el commit
de trabajo `247eee150e2968dbaa317f8ad1268350dea3665d` en el PR #885 y el
launcher reutilizó el PR de censo #884, pero el cierre falló cerrado:

```text
origen=ninguno causa=sin_candidato_valido
last-message y handoff: presentes, iguales e inválidos
error 1=resultado textual del intento UCLA ausente de las evidencias citadas
error 2=declarado intentos_documentados; calculado descubrimiento_documentado
presupuesto reservado=3/5/3900s; consumido=3/1/524s;
devuelto=0/4/3376s; reserva activa=0
```

La barrera operacional hallada durante ese trabajo tampoco se corrige aquí:
`data/manifiesto.yaml` contiene cuatro entradas con `estado_reserva`, mientras
`tests/manifiesto.py:CAMPOS_CONOCIDOS` no reconoce la clave. El PDF UCLA ya
existe y fue descargado dos veces con hash idéntico; repetir red no aporta nada.
El encargo limita correcciones de código al cron/runner/doctor/handoff o
instalador, por lo que manifiesto e inventarios quedaron intactos.

Estado posterior (`adq_doctor.py --json`, 16:31): tarea `Ready`,
`LastRunTime=16:00:01`, `LastTaskResult=65`, `NextRunTime=17:00:00`, lock
inactivo, heartbeat `FAILED/LAUNCHER-HANDOFF`, `t_cron=RESULTADO-INVALIDO`.

## Correctivo de reactivación por evento

Reproducción antes del segundo correctivo:

```text
caso=EVENTO + cambios_materiales={NC-A}
selecciona -> tools/adq_investigacion.py:450 -> _fecha(revision)
ValueError: Invalid isoformat string: 'EVENTO: firma de mesa'
```

El mismo riesgo existía al reactivar por
`evidencia_nueva_identificada`. `7791a5a75f9465d1fedcc8959db7eebe945869a8`
mantiene `espera_evento` separado de `proxima`: una revisión por evento espera
sin parsearse o avanza por una señal válida con `proxima=None`. El ruteo
`ESPERA_NUEVA_PISTA` usa la misma distinción; las barreras humanas retornan
antes de ambas señales.

```text
revision-evento espera/cambio/evidencia/barrera: OK
test_adq_handoff_resultado.py: 13 pruebas, 0 fallos
test_adq_cierre_verificable.py: 13 casos, 0 fallos
py_compile: OK
git diff --check: OK
suite test_adq_descubrimiento.py: 1 aserción heredada del mapa de necesidades;
la regresión nueva pasa aislada
```

Incorporación remota verificada:

```text
PR #886 contiene correctivo=7791a5a75f9465d1fedcc8959db7eebe945869a8
PR #884 head=699ec1ba0531e0ff329eae6a80fe6674fa976838; contiene 7791a5a
PR #885 head=8aaf45c173a613ff575c084bd3ae4024f5f480f8; contiene 7791a5a
```

La tarea se actualizó por el instalador soportado, sin cambiar calendario ni
principal. Respaldo previo:
`C:\Users\PC0\AppData\Local\Temp\AdquiereCron-before-7791a5a.xml`, SHA-256
`F6D5096A14764F3A6F406BA37156A034B15690F6CFC9550633AAEB0C20003484`.
La acción instalada solicita `7791a5a75f9465d1fedcc8959db7eebe945869a8`;
permanece `Ready`, con el `LastTaskResult=65` histórico intacto y siguiente
trigger a las 17:00.
