# Diagnóstico del incidente del 7/sep/2026 — `ACTO ADQ-CRON-V2` (P0)

Encargo: `forense/encargos/2026-09-07-ADQ-CRON-V2.md`. Ejecutado en `mm-adq`
(caja real, no sesión de nube), sin modificar nada del árbol antes de
recolectar la evidencia de abajo.

## Hecho a explicar

`censo/2026-09-07` no existe (ni local ni remota) — el cron de
`tools/adquiere_cron.sh`, programado lunes-viernes 07:30 hora de mesa
(`crontab -l` confirma la línea instalada por `ACTO MAESTRA38-CRON-3`,
intacta), no dejó ninguna huella el lunes 7/sep/2026.

## Evidencia recolectada

1. **`forense/adq-log/2026-09-07.log` no existe.** El script escribe su
   primera línea de log (`mkdir -p "$LOGDIR"` + `log "=== ... arrancando
   ==="`) en las primeras dos instrucciones ejecutables, antes de
   cualquier punto de fallo posible (incluso `PARO-CORPUS`, el PARO más
   temprano, ocurre después). La ausencia TOTAL del archivo — ni siquiera
   una línea — significa que el intérprete de `bash` de este script nunca
   arrancó, no que arrancó y falló de inmediato.
2. **`forense/adq-log/cron-stdout.log` no existe, y nunca ha existido**
   (no solo para hoy). Es el archivo al que la línea de crontab redirige
   `stdout`/`stderr` (`>> forense/adq-log/cron-stdout.log 2>&1`) — su
   ausencia total es consistente con (1).
3. **`crontab -l` (fuera del sandbox de Claude Code — dentro, `crontab
   -l` da `fopen: Permission denied` por cómo este entorno ejecuta el
   binario, no por el crontab real; confirmado re-corriendo el mismo
   comando con el sandbox desactivado) muestra la línea instalada y
   correcta**: `PATH=/usr/local/bin:/usr/bin:/bin:/home/pc0/.local/bin` y
   `30 7 * * 1-5 cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh >>
   forense/adq-log/cron-stdout.log 2>&1`, sin cambios desde su
   instalación (`ACTO MAESTRA38-CRON-3`, 6/sep/2026).
4. **`systemctl status cron` (fuera del sandbox) muestra el demonio
   `cron.service` activo de forma continua desde `Fri 2026-09-04
   23:07:09 CST`** (`Main PID: 132`) — nunca se cayó ni se reinstaló.
5. **El journal del propio `cron.service` (`journalctl -u cron`) tiene un
   hueco de ~11 horas la noche del 6→7 de septiembre**: la última entrada
   del 6/sep es `23:17:01` (`run-parts --report /etc/cron.hourly`, tarea
   horaria de `root`) y la siguiente entrada de CUALQUIER tipo es
   `10:17:01` del 7/sep — la ventana de las 07:30 (el disparo programado
   del cron de `pc0`) cae limpiamente dentro de ese hueco. `cron` no
   registra ni un solo intento de invocar la tarea de `pc0` en esa
   ventana — no hay línea `CRON[...]: (pc0) CMD (...)` para el 7/sep en
   absoluto (sí existe, para comparar, la línea `(pc0) RELOAD
   (crontabs/pc0)` del 6/sep a las `16:41:01`, cuando se instaló el
   crontab).
6. **El journal general (`journalctl`, todas las unidades) confirma la
   causa del hueco**: a las `10:04:49` del 7/sep se disparan de golpe
   `apt-daily.service`, `apt-daily-upgrade.service`, `dpkg-db-
   backup.service`, `logrotate.service`, `man-db.service` y `motd-
   news.service` — los seis timers de systemd con `Persistent=true` que
   "recuperan" su disparo perdido en cuanto la máquina vuelve a estar
   activa. Dos minutos después, `chronyd[214]: Forward time jump
   detected!` — la firma clásica de un reloj que salta hacia adelante al
   reanudar de una suspensión, no de un reinicio (`journalctl
   --list-boots` confirma un solo *boot id* desde el 4/sep: no hubo
   reinicio del kernel, la VM de WSL2 quedó suspendida y se reanudó).
7. **`descargas_mx` (`/mnt/c/...`, DrvFs) responde con normalidad hoy**
   (verificado fuera del sandbox), y la red externa (`curl` a
   `inegi.org.mx`) también — no hay evidencia de que la máquina Windows
   host o la red hayan estado caídas; lo que faltó fue la VM Linux de WSL2
   específicamente, en la ventana exacta de las 07:30.

## Clasificación

**`SCHEDULER-NO-LANZO`.**

El disparador (cron dentro de WSL) estaba correctamente configurado y su
demonio nunca se cayó — pero la VM ligera de WSL2 que lo hospeda estuvo
suspendida (sin avanzar su reloj ni ejecutar ningún proceso) durante la
ventana programada de las 07:30, y **`cron` clásico (vixie-cron) no tiene
semántica de recuperación**: a diferencia de los timers de `systemd` con
`Persistent=true` (que sí "alcanzan" su disparo perdido al reanudar, como
se ve en el punto 6), un `cron` cuyo minuto exacto pasó mientras el
proceso no estaba corriendo simplemente **nunca vuelve a intentar esa
ejecución** — ni un intento fallido, ni una huella parcial: cero
evidencia, porque no hubo absolutamente ningún proceso.

No se descarta con esta evidencia `RUNNER-LANZO-Y-FALLO-ANTES-DE-HUELLA`
porque esa clasificación exigiría que el archivo de log del día existiera
con al menos su primera línea — no existe ninguna. Tampoco aplica
`RUNNER-LANZO-Y-FALLO-DESPUES-DE-HUELLA` (exigiría al menos un commit en
`censo/2026-09-07`, que no existe) ni `INDETERMINADO` (la cadena de
evidencia — crontab intacto, demonio activo sin caídas, hueco exacto en
el journal, catch-up de timers de systemd a las 10:04:49, salto de reloj
en `chronyd` dos minutos después, un solo *boot id* desde el 4/sep — es
consistente y no requiere inventar ningún eslabón).

## Relación con el resto del acto

Esta es exactamente la clase de falla que **P2** (Windows Task Scheduler
como disparador autoritativo, con `StartWhenAvailable` para recuperar una
hora perdida) está diseñado para cerrar: el host Windows es mucho menos
probable que esté "suspendido" en el sentido en que lo estuvo la VM
ligera de WSL2 (que Windows puede pausar cuando no hay ninguna sesión
`wsl.exe` ni terminal abierto), y Task Scheduler sí sabe recuperar un
disparo perdido de forma nativa — algo que el `cron` de WSL, por diseño,
no ofrece.

No se fabrica ningún censo del 7/sep para compensar esta ausencia, y no
se corrió `tests/check.py --freeze` para absorberla — la ausencia queda
tal cual, con esta nota como explicación verificada.
