# P7 · Pruebas de aceptación en caja — `ACTO ADQ-CRON-V2`

No se cierra con otra corrida manual como única evidencia (instrucción explícita
del encargo). Nueve puntos pedidos; ocho con evidencia directa, uno con
evidencia parcial declarada como tal — sin inflar el resultado.

## Método

Los puntos 3-7 se corrieron contra un **clon aislado** (bare repo local,
`git clone --bare` de este mismo repo hacia un directorio de scratch, con
`origin` apuntando a ese bare local, nunca a GitHub) con un binario `claude`
sustituido por un doble controlable (éxito inmediato, cuelgue, exit code
arbitrario). Esto permite inyectar fallos/timeouts sin gastar cuota real de
`claude -p` ni escribir censos de prueba en `censo/<fecha>` de producción.
El código ejercitado es el real (`tools/adquiere_cron.sh` de esta rama,
copiado por el propio `git clone`), no una reescritura para la prueba.

Los puntos 1 y 8 se corrieron contra el **Windows Task Scheduler real** de
la caja de mesa, con tareas temporales (`SmokeTest-*`, desinstaladas al
terminar) que invocan `wsl.exe` igual que la tarea de producción
(`AdquiereCron`), pero con una acción inocua (escriben una línea con
timestamp en `forense/adq-log/estado/`, gitignorado) en vez de correr el
runner completo.

## 1-2 · Disparo automático sin interacción humana — **PASS**

Tarea `SmokeTest-Future` (`\ModeladoMexicano\`), trigger `-Once` a 3 minutos
de su registro (20:01:41), sin tocarla después de registrarla:

```
LastRunTime    : 07/09/2026 08:01:41 p. m.
LastTaskResult : 0
```

y el archivo de prueba en WSL con el timestamp correcto:
`SMOKE-FUTURE FF-5563-2026-09-07T20:01:42-06:00` — Windows Task Scheduler
invocó `wsl.exe`, WSL2 despertó y ejecutó el comando, sin ninguna acción
humana entre el registro y la corrida.

## 3 · Reintento el mismo día, sin `force push` ni pérdida de historia — **PASS**

Clon aislado, corpus falso presente (`data/raw/dummy_corpus_file.txt`),
`claude` stub con éxito inmediato. Dos corridas consecutivas:

```
RUN1 -> censo/2026-09-07: + [ADQ-PDN] + [ADQ]   (2 commits nuevos)
RUN2 -> censo/2026-09-07: + [ADQ-PDN] + [ADQ]   (2 commits MÁS, ambos push limpios)
```

`git log origin/censo/2026-09-07 --oneline -8` tras RUN2 muestra las CUATRO
commits de ambas corridas, en orden, sin ningún `rejected`/non-fast-forward
en ninguno de los dos logs. `grep -n "push.*-f\|push.*--force"
tools/adquiere_cron.sh` → ningún resultado: el script no tiene ninguna ruta
de force-push.

Esto es la corrección directa del defecto real medido el 6/sep
(`censo/2026-09-06` divergió 9 commits locales contra 1 remoto por
`checkout -B` reiniciando el puntero de la rama en cada corrida — ver P3 en
el commit `52bd37cc`).

## 4 · `main` local no recibe commits `[CENSO]` — **PASS**

Mismo clon aislado, corrida con `data/raw` oculto (fuerza `PARO-CORPUS`):

```
git log main --oneline -5   (antes y después de la corrida, IDÉNTICO)
git status --short          (limpio)
```

`main` no se movió ni una sola vez durante ninguna de las corridas del
punto 3 tampoco: las cuatro commits del punto 3 viven exclusivamente en
`censo/2026-09-07`.

## 5 · Fallo controlado → huella `FAILED` — **PASS**

Misma corrida de PARO-CORPUS: exit code `1`,
`forense/adq-log/estado/heartbeat.json`:

```json
{"run_id": "...", "estado": "FAILED", "fase": "PARO-CORPUS", "codigo_salida": 1, ...}
```

## 6 · Lock con dos invocaciones simultáneas — **PASS**

Un subproceso sostiene `flock` sobre `forense/adq-log/estado/
adquiere_cron.lock` durante 8s; `tools/adquiere_cron.sh` lanzado en ese
intervalo termina en **0.112s** con exit `3`, log:

```
PARO-LOCK: ya hay una instancia de adquiere_cron.sh corriendo (... tomado).
Esta invocación (run_id=...) no toca git ni el corpus, termina de inmediato.
```

Heartbeat confirma `estado=PARO-LOCK`, sin ningún `git fetch` previo en el
log — la instancia bloqueada no llega a tocar el repo.

## 7 · Timeout — **PASS**

`CLAUDE_TIMEOUT_SEGUNDOS=3` + `claude` stub que cuelga
(`sleep 999999`):

```
[...] claude -p agotó el timeout de 3s (timeout(1) lo mató, exit 124)
[...] claude -p terminó con código 124
[ADQ] ...: invocado=si motivo=- exit=124 duracion=4s ...
```

Heartbeat: `estado=FAILED, codigo_salida=124`. `timeout(1)` mató al
proceso colgado sin que el lock quedara tomado indefinidamente.

## 8 · Recuperación de una ejecución programada perdida — **PASS PARCIAL, declarado**

Verificado por configuración, no por simulación en vivo completa:

- `StartWhenAvailable=true` confirmado en la tarea real de producción
  (`schtasks /Query /XML`, ver commit de P2) — el ajuste de Windows
  documentado exactamente para "correr en cuanto sea posible si el
  sistema no estuvo disponible en la hora programada", el mecanismo que
  faltó el 7/sep (P0).
- **Medido, no asumido**: un trigger `-Once` cuyo `StartBoundary` ya pasó
  al momento de registrarlo NO se recupera solo (probado dos veces:
  registro directo con hora pasada, y registro con hora futura +
  deshabilitar + esperar a que pase + rehabilitar — ninguna de las dos
  disparó). `StartWhenAvailable` en triggers de una sola vez no cubre
  "creado ya vencido"; la semántica de recuperación de Microsoft para
  triggers recurrentes (diarios/semanales, como el de producción) es
  la documentada para "el sistema estaba dormido/apagado cuando llegó la
  hora programada", un caso distinto al que se pudo simular aquí sin
  privilegios de administrador (no se puede reiniciar el servicio
  "Task Scheduler" ni suspender la máquina real de mesa desde esta
  sesión sin riesgo/alcance excesivo).
- Conclusión honesta: la CONFIGURACIÓN correcta está verificada y es la
  documentada para el caso real; la RECUPERACIÓN EN VIVO de un disparo
  semanal perdido queda pendiente de observar la primera vez que
  ocurra de verdad (o de una prueba futura con privilegios de
  administrador que permita reiniciar el servicio de programación).

## 9 · CI con T-CRON no completo, visible pero sin bloquear baseline — **PASS**

Evidencia real, no local: PR #606, run de GitHub Actions
`34178385463`, job `check`:

```
[warn]  T31 T-CRON  (1 warn)
  · T-CRON: 1
      SIN-HUELLA -- censo/2026-09-07 no existe (ni local ni remota) -- ver forense/cron/REGISTRO-CRON-v1_0.md §5
...
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

T-CRON visible en el resumen de la suite, CI pasó (`check pass`).

## Resumen

| # | criterio | resultado |
|---|---|---|
| 1-2 | disparo automático sin interacción | PASS |
| 3 | reintento mismo día, sin force-push/pérdida | PASS |
| 4 | `main` no mutado | PASS |
| 5 | huella `FAILED` | PASS |
| 6 | lock, dos invocaciones simultáneas | PASS |
| 7 | timeout | PASS |
| 8 | recuperación de disparo perdido | PASS parcial (configuración verificada; catch-up en vivo no observable sin privilegios de admin ni riesgo de suspender la caja real) |
| 9 | CI visible, baseline no bloqueado | PASS |
