# ACTO GEN2-ADQ-VERIFICACION-CAJA — cierre

**Fecha:** 2026-09-09 · **Entorno:** CAJA (Ubuntu/WSL de mesa), Opus · **Redactado contra** `origin/main = 606f6ee3`; **ejecutado contra** `origin/main = 0f62668` (verificado: `606f6ee3` es ancestro de `0f62668`).

**Compuerta:** GATED a `ACTO GEN2-LOTE-ENCIG-1` fusionado — **CUMPLIDA por producto**: `PR #664` es el merge commit `0f62668`, cabeza de `origin/main`.

**Firma de mesa (9/sep/2026, verbatim):** «Revisa esta propuesta de cableado porfa y dame los encargos, encig con adenda corriendo.»

---

## 0 · La fuente de este reporte — y su verificación posterior

El encargo manda «intenta el bloque PowerShell **del §7 de la firma**» y evalúa contra el «**criterio de aceptación 7** de la firma». **Al ejecutar este acto, el despacho `REVISION-CABLEADO-SONDA-ADQUISICION` (Astra, 9/sep) no viajó adjunto ni existía en el repo** — negativo con control positivo y código de salida:

```
git grep -l "REVISION-CABLEADO-SONDA" <todas las refs>   -> 0 resultados
git grep -l "SONDA-3" origin/main -- forense/            -> 10 resultados (control positivo)
```

Lo que sí viajó adentro es la firma verbatim, que es lo que la cláusula «si falta, PARA» protege — por eso este acto NO paró. El §7 **se reconstruyó a partir de la enumeración que el propio encargo hace de su contenido**, y así se declaró en su momento, sin fingir haberlo leído.

**VERIFICACIÓN POSTERIOR (mesa entregó el documento el mismo día; `sha256 0554bf6f8f8b530a428650f25f88b910bbf9e3eb471991224efc4b422e5082a5`).** El despacho quedó archivado por el hermano NUBE en `forense/notas/2026-09-09-REVISION-CABLEADO-SONDA-ADQUISICION-astra.md` (`PR #665`, fusionado 19:18Z) — este acto **no lo duplica**. Contrastado el §7 real contra lo que se corrió, elemento por elemento:

| §7 pide | ¿Se corrió? |
|---|---|
| `python3 /home/pc0/mm-adq/tools/adq_doctor.py --json` | Sí — y la ruta `mm-adq` se había derivado por cuenta propia del instalador, no adivinado |
| «interpretar `t_cron` junto al censo consolidado, no relanzar por su falso `CENSO-SIN-CIERRE`» | Sí — H1 no se materializó, `t_cron COMPLETO`; nada se relanzó |
| `Get-ScheduledTask` / `Get-ScheduledTaskInfo` sobre `\ModeladoMexicano\AdquiereCron` | Sí |
| `TaskName,TaskPath,State` · `Actions: Execute,Arguments,WorkingDirectory` · `Triggers *` | Sí |
| `Settings: StartWhenAvailable,WakeToRun,MultipleInstances,ExecutionTimeLimit` | Sí (y algunos más) |
| `Principal: UserId,LogonType,RunLevel` | Sí |
| `Info: LastRunTime,LastTaskResult,NextRunTime,NumberOfMissedRuns` | Sí |
| `Get-TimeZone` | Sí |
| `Get-WinEvent` Operational del día, filtrado por la tarea | Sí — canal `IsEnabled=False`, declarado |
| «si el historial está deshabilitado, declararlo; no inferir ausencia de disparo» | Sí |
| «correlacionar con `2026-09-09T073007-371` y el log local» | Sí (§1.5) |
| «comprobar que no quedó otro disparador activo» | Sí — **quedó**: el crontab legado sigue disparando |

**La reconstrucción resultó completa: el §7 real no pide nada que no se haya corrido, y no se corrió nada que el §7 no pidiera.** El criterio de aceptación 7 verbatim es «Una ejecución programada de producción se correlaciona desde Task Scheduler hasta su recibo publicado. Una invocación manual se distingue y no sustituye esa evidencia», y el 8 conserva el alcance parcial de la recuperación «hasta observarla o realizar una prueba acotada autorizada» — ambos son los que este reporte evalúa. Se deja escrito el trayecto entero, no sólo el desenlace: el acto corrió a ciegas del §7 y acertó, y eso vale menos que el hecho de que la ciega estaba declarada.

## 1 · P1 · Lectura de lo instalado — sin tocar nada

### 1.1 · Dónde se corrió el doctor, y por qué importa

`tools/adq_doctor.py` deriva su `RAIZ` de la ruta del propio script. El runner opera sobre **`/home/pc0/mm-adq`** (default `-ClonPath` del instalador, confirmado en la acción instalada). Correrlo desde el worktree de este acto habría dado `heartbeat: AUSENTE` y `lock: no existe` — un falso negativo sobre la máquina. Se corrió desde `mm-adq`.

Segundo cuidado, medido no supuesto: **el sandbox de esta sesión no lee `/mnt/c`**. Dentro del sandbox el doctor devuelve `scheduler_windows: NO-VERIFICABLE`, `tz_windows: NO-VERIFICABLE` y `descargas_mx: AUSENTE`; fuera, los tres son legibles. Las dos corridas se hicieron a propósito para separar **artefacto de sandbox** de **hecho de la máquina**. Leer la primera como «no está instalado» habría sido exactamente el error que el encargo prohíbe.

### 1.2 · Salida cruda del doctor (fuera del sandbox — la que vale)

```json
{
  "entorno": { "CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE": "(sin fijar -- CAJA)", "es_wsl_detectado": true },
  "zona_horaria": {
    "tz_sistema_etc_timezone": "America/Mexico_City",
    "offset_local_actual": "-0600",
    "ahora_america_mexico_city": "2026-09-09T12:40:23-06:00",
    "tz_windows_host_tzutil": "Central Standard Time (Mexico)"
  },
  "scheduler_windows": {
    "estado": "INSTALADA", "tarea": "\\ModeladoMexicano\\AdquiereCron",
    "State": "Ready", "LogonType": "Interactive",
    "LastRunTime": "2026-09-09T07:30:00.0000000-06:00",
    "LastTaskResult": 0,
    "NextRunTime": "2026-09-10T07:30:00.0000000-06:00"
  },
  "crontab_legado": {
    "instalado": true,
    "lineas_relevantes": [
      "# tools/adquiere_cron.sh resuelve su propio REPO_DIR por",
      "30 7 * * 1-5 cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1"
    ]
  },
  "binarios": { "git": "/usr/bin/git", "curl": "/usr/bin/curl", "python3": "/usr/bin/python3", "gh": "/usr/bin/gh", "claude": "/home/pc0/.local/bin/claude" },
  "corpus_data_raw": { "data_raw_existe": true, "es_symlink": true, "symlink_destino": "/home/pc0/mm-corpus/raw", "primer_hijo": ".claude" },
  "descargas_mx": { "estado": "OK", "ruta": "/mnt/c/Users/PC0/Descargas MX" },
  "red": { "url": "https://www.inegi.org.mx/", "codigo_http": "200" },
  "lock": { "lock_activo": false },
  "heartbeat": { "run_id": "2026-09-09T073007-371", "pid": 371, "estado": "TERMINADO", "fase": "FIN", "fecha": "2026-09-09", "codigo_salida": 0, "actualizado": "2026-09-09T07:34:01-06:00" },
  "t_cron": { "estado": "COMPLETO", "fecha_evaluada": "2026-09-09", "detalle": "censo/2026-09-09: [ADQ] invocado=si exit=0" },
  "ultimo_censo_local": { "existe": true, "archivo": "forense/censo-raiz/2026-09-08.txt", "modificado": "2026-09-09T07:30:10" }
}
```

**Advertencia H1 aplicada:** el encargo avisa que hasta que el CABLEADO fusione, `t_cron` puede arrastrar un `CENSO-SIN-CIERRE` falso con rama retirada. Hoy **no se materializó**: `t_cron` salió `COMPLETO` y coincide con el censo consolidado (`forense/censo-raiz/2026-09-09.txt`, `[ADQ] invocado=si exit=0`). No se relanzó nada.

### 1.3 · La configuración instalada (bloque §7 reconstruido)

| Campo | Valor leído |
|---|---|
| Tarea | `\ModeladoMexicano\AdquiereCron` · State `Ready` |
| Acción | `wsl.exe` `-d Ubuntu -u pc0 -- bash -lc /home/pc0/mm-adq/tools/adquiere_cron.sh` |
| Principal | UserId `PC0` · LogonType `Interactive` · RunLevel `Limited` |
| Trigger | Semanal, `StartBoundary 2026-09-07T07:30:00-06:00`, `DaysOfWeek 62` (= lunes a viernes), `Enabled True` |
| `StartWhenAvailable` | **True** |
| `WakeToRun` | False |
| `MultipleInstances` | `IgnoreNew` |
| `ExecutionTimeLimit` | `PT2H` |
| `LastRunTime` / `LastTaskResult` | `2026-09-09 07:30:00` / **0** |
| `NextRunTime` / `NumberOfMissedRuns` | `2026-09-10 07:30:00` / **0** |
| `Get-TimeZone` | `Central Standard Time (Mexico)`, `-06:00` — **coincide** con `/etc/timezone` de WSL |

Todo coincide con lo que `tools/windows/instala-tarea-adquisicion.ps1` declara en el repo. **Lo declarado y lo instalado no divergen.**

### 1.4 · Eventos del scheduler: por qué esa pierna no cierra

```
Get-WinEvent -ListLog 'Microsoft-Windows-TaskScheduler/Operational'  ->  IsEnabled = False
```

El canal **está deshabilitado**. Se intentó habilitarlo desde esta sesión y Windows lo rechazó por falta de elevación (`SaveChanges` → «Intento de realizar una operación no válida»); el estado quedó `False`, la máquina sin cambios. Esto se declara como **NO-VERIFICABLE-DESDE-ESTA-SESIÓN**: un historial operativo apagado **no** es evidencia de que la tarea no disparó (A.13). Queda como `NC-0120`.

### 1.5 · La atribución — el hallazgo central

**Hoy dispararon LOS DOS.** El log local de la caja trae dos arranques en el mismo segundo:

```
[2026-09-09 07:30:07-0600] === adquiere_cron.sh arrancando ... (run_id=2026-09-09T073007-491) ===
[2026-09-09 07:30:07-0600] === adquiere_cron.sh arrancando ... (run_id=2026-09-09T073007-371) ===
[2026-09-09 07:30:07-0600] PARO-LOCK: ... Esta invocación (run_id=...-491) no toca git ni el corpus, termina de inmediato.
[2026-09-09 07:33:59-0600] [ADQ] ... invocado=si motivo=- exit=0 duracion=228s ... run_id=2026-09-09T073007-371
```

¿Cuál fue cuál? Dos discriminadores independientes, ninguno lexical:

1. **`cron-stdout.log` sólo lo escribe el crontab.** La entrada de cron redirige `>> forense/adq-log/cron-stdout.log`; el runner **nunca** nombra ese archivo (`grep "cron-stdout" tools/adquiere_cron.sh` → 0 resultados, con control positivo `grep -c "adq-log"` → 3). Ese archivo contiene exactamente `run_id=...-491` y su `PARO-LOCK`. **Luego cron = 491, el perdedor.**
2. **Códigos de salida.** `PARO-LOCK` sale con `exit 3` (`tools/adquiere_cron.sh:104`). Task Scheduler reporta `LastTaskResult = 0`, no 3. **Luego Task Scheduler ≠ 491.**

Con sólo dos invocaciones en el día, ambas contabilizadas: **la corrida que hizo el trabajo — `run_id 2026-09-09T073007-371`, 228 s, `exit=0`, cuya huella está fusionada en `forense/censo-raiz/2026-09-09.txt` — la inició Windows Task Scheduler.** El crontab legado disparó, perdió el `flock` y no tocó ni git ni el corpus.

Correlación pedida, eslabón por eslabón:

`Task Scheduler LastRunTime 07:30:00 / LastTaskResult 0` → `log local 07:30:07 run_id ...-371` → `heartbeat.json run_id ...-371 estado TERMINADO exit 0` → `huella fusionada forense/censo-raiz/2026-09-09.txt [ADQ] invocado=si exit=0 run_id=2026-09-09T073007-371`.

El único eslabón faltante es el evento del scheduler (§1.4), y falta **por canal apagado**, no por ausencia de disparo. Esto es **invocación programada, no manual**: ninguna sesión humana lanzó el runner a las 07:30:07, y la tarea reporta haber corrido a las 07:30:00 con resultado 0.

### 1.6 · Veredictos A.4 por elemento

| Elemento | Veredicto | Apoyo |
|---|---|---|
| Tarea instalada | **EXISTE-SATISFACE** | `Get-ScheduledTask` → `Ready`; config idéntica a la declarada en el repo |
| Disparo de hoy atribuido | **EXISTE-SATISFACE** | Task Scheduler, por doble discriminador (§1.5); correlación completa salvo el evento |
| Crontab legado | **EXISTE-NO-SATISFACE** | Sigue instalado y disparando; hoy fue el perdedor del `flock`. Es ruido, no defensa |
| Política de recuperación | **NO-VERIFICABLE** (aceptación **PARCIAL** del 7/sep **conservada**) | `StartWhenAvailable=True` configurado, pero `NumberOfMissedRuns=0`: nunca se ha perdido una hora, así que **nunca se ha observado recuperar**. No se promociona |

### 1.7 · Qué se corrigió en la máquina

**Nada.** Es el resultado honesto, no una omisión: lo único que la lectura demostró necesario fue habilitar el canal Operational, y Windows lo rechazó sin elevación. La retirada del crontab **sí** tiene ya la atribución que le faltaba, pero el paso (3) de `tools/windows/GUIA-TAREA-ADQUISICION.md` exige documentarla en `forense/cron/REGISTRO-CRON-v1_0.md`, que **no está en el perímetro de este acto** — y retirar el respaldo mientras el CABLEADO modifica `adquiere_cron.sh` en paralelo agrega riesgo sin urgencia, porque el `flock` ya contiene el daño. Va como `NC-0119` con sucesor, no como atajo.

---

## 2 · P2 · El piloto SONDA-3, ejecutado de verdad

**Compuerta propia, por producto:** `.claude/commands/sonda.md` con «Segunda pasada crítica» → 1 · `.claude/commands/adquiere.md` con `SONDA-LATERAL-RECOMENDADA` → 1 · cola de registro 138 filas. Coincide con la Parte 2 del A.8. **CUMPLIDA.**

### 2.1 · Selección — por derivación, no por dedo

Se corrió el comando del encargo sobre la cola vigente (13 candidatas tras excluir RUPC) y el cruce contra `relaciones.tsv` / `necesidad-objeto-modelo.tsv`. Seis candidatas tienen consumidor vigente. Regla del encargo: consumidor real primero, luego `prioridad` ascendente →

**`CANAL_DE_ADQUISICION_REFERIDOS_FINTECH`** (`cola-adquisicion-v1_0.tsv:21`), `NO-ENCONTRADO`, prioridad **20** (la más baja de las seis), consumidor `N19` = `dinero.credito.scoring_alternativo` vía `REL-943ed2bde102c6e791588b3b`, y `R1.3` pierna 3 vía `EXT-NEG-01`.

Nota metodológica: `necesidad-objeto-modelo.tsv` dio 0 coincidencias para las 13 candidatas. **No es un lector vacío** — el archivo tiene 46 filas reales y su llave es `necesidad_id`/`objeto_modelo_origen`, no el token de fuente. Se verificó antes de usar ese 0.

### 2.2 · Estado de entrada (§1), verbatim

`data/mapa-ext-oficial-2026-08-06.tsv:17` (`EXT-NEG-01`): «Universo: BDIF CNBV, series Banxico y estudio fintech COFECE; términos canal de adquisición, alta, referidos, boca a boca; búsqueda web y cruce repo; dos vías; 2026-08-06». Unidad: institución/municipio o agregados. **Condición faltante: «porcentaje de altas por canal para fintech identificable, no mera infraestructura o mención cualitativa».**

A eso se suman, por la nota de la fila, tres sondeos más (1/sep, 3/sep, 6/sep con la base CKAN corregida) — cuatro en total, todos `NO-ENCONTRADO`.

### 2.3 · Universo adicional sondeado hoy, y el hallazgo

Los cuatro sondeos previos buscaron **un dataset** de canal de adquisición en universo de **reguladores** y en CKAN. Ninguno examinó el **lado de demanda**. Ruta lateral abierta hoy: la encuesta de hogares.

Primer mecanismo — índice local: `tools/busca_reactivos.py` sobre 241 591 filas, términos `referid`/`recomend`/`boca a boca`/`publicidad`/`se enter`/`cómo supo`/`canal`. Cero pertinentes.

**Y ahí está la causa mecánica del falso negativo.** ENIF **sí** está indexada — 382 filas, olas 2012/2015/2018/2021/2024 — y **ninguna de las 382 trae texto de reactivo** (columnas DBF/CSV sin etiqueta). Toda búsqueda por texto sobre ese índice es **ciega a ENIF por construcción**. No es que ENIF no midiera el objeto: es que el instrumento de búsqueda no puede verla.

Segundo mecanismo (§5-bis, pregunta 2) — abrir el descriptor: `enif_2024_fd.xlsx`, 4 hojas, 1 888 filas, `openpyxl`. Tercer mecanismo — abrir el microdato: `enif_2024_bd_csv.zip` → `TMODULO.csv`, 13 502 filas × 398 columnas, verificando que las columnas **existen y están pobladas** (un primer intento dio «todas AUSENTE» por parsear a mano una cabecera entrecomillada; se corrigió con `csv.reader`, y se dice aquí porque el falso negativo estuvo a un paso de escribirse).

### 2.4 · Lo que ENIF 2024 rinde

Identificación de fintech: `P6_2_8` crédito contratado por internet/app (Prestadero, Doopla, YoTePresto), `P5_4_8` cuenta contratada por internet/app (Mercado Pago, Nu, Spin de Oxxo). Canal de contratación: `P6_6`, `P5_16`. Recomendación de conocidos: `P6_11_2`, `P5_15_2`. Diseño: `EST_DIS`, `UPM_DIS`, ponderador `FAC_PER`.

**Crédito fintech × canal de contratación** (n = 200; 1 178 431 expandido):

| Canal | n | % ponderado |
|---|---|---|
| App de celular | 113 | **57.5 %** |
| Página de internet | 42 | 20.6 % |
| Sucursal | 26 | 11.5 % |
| Personal promotor | 7 | 4.2 % |
| Establecimiento comercial | 10 | 3.3 % |
| Otro | 2 | 3.1 % |

**Cuenta fintech × canal de contratación** (n = 1 407; 8 919 712 expandido):

| Canal | n | % ponderado |
|---|---|---|
| App de celular | 390 | **30.6 %** |
| Sucursal | 423 | 29.0 % |
| Página de internet | 178 | 13.9 % |
| Establecimiento (Oxxo/Walmart…) | 232 | 13.4 % |
| Vía empleador | 152 | 11.0 % |
| Personal promotor | 21 | 1.5 % |
| Programa social | 10 | 0.5 % |

Recomendación de amistades para **comparar** el producto: crédito 44.9 % Sí (n = 87), cuenta 56.8 % Sí (n = 495).

Eso **es** el «porcentaje de altas por canal para fintech identificable» que `EXT-NEG-01` declaraba faltante, y no es infraestructura ni mención cualitativa.

### 2.5 · Segunda pasada crítica (§5-bis) — y por qué el veredicto es PARCIAL

1. **¿El objeto exacto, o un proxy?** Proxy en el margen: `P6_6`/`P5_16` preguntan por el **último** crédito/cuenta contratado, sin sufijo de producto, mientras `P6_2_8`/`P5_4_8` identifican **tenencia** fintech. Lo publicado es «canal del último producto entre tenedores de producto fintech». Por eso **EXISTE-SATISFACE-PARCIAL**, no SATISFACE (`NC-0122`).
2. **¿Vía agotada con un solo mecanismo?** El índice habría cerrado en negativo; se abrieron descriptor y microdato como segundo y tercer mecanismo. Es lo que volteó el resultado.
3. **¿Un 200/000 leído como veredicto?** No se apoyó ningún veredicto en códigos HTTP: el hallazgo es local sobre bytes en corpus.
4. **¿Republicador/handoff no considerado?** Para la pierna de **reguladores** sí queda uno sin reintentar hoy — ver frontera.
5. **¿Declara frontera?** Sí, abajo.

**Frontera explícita de este sondeo (lo que NO se examinó):** no se re-probaron hoy CNBV/Banxico/COFECE ni CKAN — se heredan los cuatro sondeos previos; no se abrieron ENIF 2018/2021 para serie temporal del mismo cruce (`NC-0121`), pese a que la nota de la fila ya marcaba ENIF 2021 como `PARALELA-PARCIAL` desde el 6/sep; «referido» **no existe** como código de canal en ninguna de las dos baterías, así que esa pierna sigue **EXISTE-NO-SATISFACE**.

### 2.6 · Desenlace y escritura

**Ninguno de los tres finales del piloto en su forma literal — y por la razón buena.** No hubo adquisición porque **no hacía falta**: los payloads ya estaban en corpus. `.claude/commands/sonda.md §6` es explícito — «si la candidata NO necesita adquisición (ya está OBTENIDO/indexada) — repórtala, no la re-encoles». No se creó fila nueva, no se fabricó descarga, no se tocó el manifiesto.

La fila existente se actualizó **con el escritor canónico** (`tools/curador_registro/tsv_crudo.py::upsert_fila`, clave `fila_origen`, una sola línea tocada — verificado `1 insertion, 1 deletion`) y la vista se **regeneró** con `python3 tools/vista_cola_adquisicion.py` (138 filas), nunca a mano.

`NO-ENCONTRADO` → **`OBTENIDO-PARCIAL`** (`EXISTE-SATISFACE-PARCIAL` en la nota, mismo vocabulario que `ENSAFI_TANDAS`/`WBES`).

**Trampa H2 — fecha de descubrimiento de vía vs. fecha de intento efectivo:** la *vía* (ENIF como paralela por constructo) estaba **descubierta desde el 6/sep**, escrita en la nota de la fila como `PARALELA-PARCIAL` sobre ENIF 2021. El *intento efectivo* — abrir descriptor y microdato y computar el cruce — es de **hoy, 9/sep**. Este acto no reclama haber descubierto la dirección; reclama haberla ejercido.

`NC-0060` queda **CERRADA** con cita y estampa de universo (A.10).

---

## 3 · P3 · Reporte compuesto

| | |
|---|---|
| **Qué se atribuyó** | Criterio 7 (ejecución programada correlacionada de Task Scheduler a recibo publicado): **CUMPLIDO EN PARTE, con la parte faltante declarada**. Cadena `LastRunTime 07:30:00 / LastTaskResult 0` → `log 07:30:07 run_id ...-371` → `heartbeat TERMINADO exit 0` → `huella fusionada censo-raiz/2026-09-09.txt`. **Programada, no manual**, por doble discriminador. Falta sólo el evento del scheduler, **NO-VERIFICABLE-DESDE-ESTA-SESIÓN** porque el canal Operational está apagado — no por ausencia de disparo (A.13) |
| **Qué corrigió y por qué** | **Nada en la máquina.** Único arreglo que la lectura demostró necesario (habilitar el canal Operational) → rechazado por falta de elevación. Retirar el crontab ya tiene atribución probada pero exige `forense/cron/`, fuera de perímetro → `NC-0119`. Ni segundo scheduler, ni logon, ni energía, ni horarios |
| **Desenlace del piloto** | **Positivo parcial, sin adquisición.** `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH`: `NO-ENCONTRADO` → `OBTENIDO-PARCIAL`. Cuatro sondeos previos fallaron por una ceguera medible del índice (382 filas ENIF, 0 con texto). Cruce ponderado publicado. Manifiesto intacto |
| **Residuales** | `NC-0119` retirada del crontab (sucesor: acto con `forense/cron/`) · `NC-0120` canal Operational + recuperación real (sucesor: mesa, elevado) · `NC-0121` ENIF 2018/2021 para serie (sucesor: acto de universo N19/R1.3) · `NC-0122` canal del producto fintech en sí (sucesor: decisión de mesa) · `NC-0123` índice ciego a ENIF (sucesor: acto con `tools/`) |

**Contador:** no se movió. El piloto no adquirió payload, así que no hay cambio de manifiesto ni PR de firma por esa vía; este acto no cuenta corridas.

**Aceptación PARCIAL del 7/sep:** conservada, no promovida.
