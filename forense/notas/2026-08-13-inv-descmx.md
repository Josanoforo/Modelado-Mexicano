# ACTO INV-DESCMX · inventario de Descargas MX contra el manifiesto

SHA de redacción del encargo: `e90a7a6` (merge #218). `origin/main` se
había movido a `1cb6e3e` (merge #219, TRIAGE-63) al arrancar este acto —
no es PARO por instrucción explícita del encargo; se refresca y re-deriva
abajo.

Entorno: CAJA (Ubuntu, WSL2), corpus montado. Estado: CERRADO.

## ARRANQUE

**1 · REPO.** Clon existente en `/home/pc0/Modelado-Mexicano` (hub de
worktrees). No se arrancó ahí: ese checkout estaba en
`sesion/cal-conf-faseb-pos4-envipe-paso1` (302ac5a), una rama ajena en
vuelo, sin `tests/corpus.py` en su árbol (existe en `origin/main`, no en
esa rama vieja). Se creó un worktree nuevo dedicado a este acto:

```
$ git worktree add --no-track /home/pc0/mm-inv-descmx origin/main -b inv-descmx
```

`--no-track` fue necesario porque `.git/config` del hub está bajo
contención de escritura compartida entre las ~40 sesiones que tienen
worktree abierto ahí mismo (ver `[[project_modelado_mexicano_git_config_contention]]`
en memoria) — `git worktree add` normal fallaba con
`error: could not lock config file .git/config` incluso tras limpiar un
`.git/config.lock` residual (un character-device apuntando a `/dev/null`,
dueño `nobody:nogroup` — artefacto, no un lock legítimo). Sin
`--no-track` el registro del worktree se abortaba completo, sin dejar
directorio. Con `--no-track`, el worktree se creó limpio; el único costo
es que la rama no quedó con upstream configurado (irrelevante hasta el
push).

Ruta absoluta: `/home/pc0/mm-inv-descmx`
`git log -1 --format="%h %s"`: `1cb6e3e Merge pull request #219 from Josanoforo/triage-63`
`git status`: limpio tras el worktree add (antes de los commits de este acto).

**2 · SHA.** `origin/main` avanzó de `e90a7a6` (#218) a `1cb6e3e` (#219,
TRIAGE-63) más `dc75d74` (#220, PROC-10) antes de que este acto arrancara.
`tests/check.py` no cambió entre `e90a7a6` y `origin/main` (`git diff
--stat e90a7a6 origin/main -- tests/check.py` vacío). La línea base
congelada (`tests/baseline.json`, HEAD `3d0d1e5fd05567e...`) tampoco se
tocó desde `536650b` (ACTO A8-LAND), anterior a `e90a7a6` — la cifra que
el encargo cita (`3d0d1e5`) es correcta, verificada directamente contra
`data['head']` en este worktree (basado en `origin/main`), no contra el
hub compartido, que resultó tener una copia de `tests/baseline.json`
distinta por estar en una rama vieja no fusionada (`sesion/cal-conf-...`,
cuya copia de ese archivo apunta a un HEAD diferente porque nunca
incorporó los últimos freezes de main) — falso rastro autodetectado y
descartado antes de reportarlo, no una discrepancia real de `origin/main`.

**3 · data/raw.** Ausente en el worktree nuevo (gitignorado, por
worktree). Se enlazó al corpus compartido de la máquina, mismo destino
que usan los worktrees hermanos:

```
$ ln -s /home/pc0/mm-corpus/raw data/raw
```

**4 · ENTORNO**, las tres partes crudas:

```
$ echo "$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE"
(vacío)
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
$ ls data/raw/ | head -1
20260813130000.export.CSV.zip
```

Tercera parte NO vacía → CAJA confirmado, no PARO.

```
$ python3 -c "import sys;sys.path.insert(0,'tests');import manifiesto as M;print(M.raices_configuradas('.'))"
{}
```

Vacío en el worktree recién creado porque `data/raices.local.yaml` es
gitignorado *por worktree*, no compartido vía el repo — cada worktree
necesita su propia copia local. Se copió del hub (mismo contenido,
mismo entorno físico, misma máquina):

```
$ cp /home/pc0/Modelado-Mexicano/data/raices.local.yaml data/raices.local.yaml
$ python3 -c "...M.raices_configuradas('.')"
{'descargas_mx': '/mnt/c/Users/PC0/Descargas MX', 'downloads': '/mnt/c/Users/PC0/Downloads'}
```

`descargas_mx` presente → no PARO.

**5 · ESPEJO.** Toda cifra de esta nota sale de `/home/pc0/mm-inv-descmx`,
comandos a la vista.

## Compuerta REG-LOTE3 — resuelta, no bloqueante

El encargo advertía correr después de REG-LOTE3 o reportar como huérfanos
"los 23 archivos que ese acto está por registrar". Verificación exhaustiva
antes de correr nada: REG-LOTE3 no existe en ningún branch, commit, PR ni
worktree de este repo (`git log --all --grep`, `-S`, `git ls-remote
--heads origin`, `find` por filesystem — los cinco vacíos o negativos).

Lo que sí existe: `descargas_mx/Descargas Manuales/`, 53 archivos, mtime
entre `2026-08-13T12:00:47` y `2026-08-13T13:41:41` — un lote de
adquisición manual completado ~70 minutos antes de que este acto
arrancara, cuyo contenido (LAPOP, GPS, IEPEP/LFEPIE/ECEPIE) coincide con
fuentes `CANDIDATA` de `data/cola-adquisicion-2026-08-12.tsv`. Corrección
de mesa recibida a mitad de este acto: el "23 archivos" del encargo era
una captura tomada ~12:04, antes de que el lote terminara (13:33–13:40);
no es una discrepancia que investigar, es una cifra vencida al momento de
escribirse. Instrucción de mesa: el cluster completo (53) es el lote
pendiente de registro de REG-LOTE3, se segrega como bloque, se reporta
como **PENDIENTE-DE-REGISTRO** (no como HUÉRFANO), no se registra aquí
(eso es REG-LOTE3, que sigue sin correr), y el delta contra MAP-1b se
calcula solo sobre los huérfanos que quedan fuera del cluster.

## COMMIT 1 — extensión de C1

Hecho en `tests/corpus.py`, commit `4f90f61`. `c1_huerfanos()` ahora
barre `RAIZ_INTEGRADA` más todo lo que `M.raices_configuradas()`
devuelva, cada raíz emparejada solo contra las entradas que declaran esa
misma raíz. Sobre raíces en `M.RAICES_QUE_EXIGEN_GRUPO` (`downloads`) se
acota por `M.EXTENSIONES_DATO_RAICES_NO_CURADAS` (filtro ya existente,
no reinventado) y se reporta solo cuenta, nunca nombres. El límite
declarado de 2026-08-06 queda como registro histórico, con una ENMIENDA
fechada encima, no borrado. C2/C3 sin tocar. Sigue fuera de
`tests/check.py`, sigue WARN-only, sigue sin `--freeze`.

## COMMIT 2 — la corrida, el inventario y el delta

### Salida cruda completa

```
$ python3 tests/corpus.py
============================================================================
  CORPUS: archivo -> entrada (complemento de manifiesto.py --verifica)
============================================================================
  manifiesto: 582 entradas totales, 578 con payload (sha256)
  por raíz, tal cual declarado: data_raw=43 · descargas_mx=57 · SIN CAMPO raiz (=data_raw por convención)=478
  raíces visibles a C1 (RAIZ_INTEGRADA + configuradas en data/raices.local.yaml): data_raw, descargas_mx, downloads

  [warn]  C1 huérfanos  (96 warn)  -- alcance: todas las raíces configuradas, ver ENMIENDA en cabecera
    · [data_raw] DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] eder2025/889463930242.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] enaproce2018/ejem_base_micro_ciega_csv.zip -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] enaproce2018/ejem_base_micro_ciega_dta.zip -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] enaproce2018/ejem_base_pyme_ciega_csv.zip -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] enaproce2018/ejem_base_pyme_ciega_dta.zip -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh02cb_b2.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh02cb_b3a.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh02cb_b3b.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh02cb_bc.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh02q_b2.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh02q_b3a.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh05cb_b2.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh05cb_b3a.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh05cb_b3b.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh05cb_bc.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh05q_b2.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh05q_b3a.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh09cb_b2.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh09cb_b3a.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh09cb_b3b.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh09cb_bc.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/ehh09q_b2.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/eloc02cb_bcc.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/eloc02q_bcc.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/eloc05cb_bcc.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/eloc05q_bcc.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/eloc09cb_bcc1.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/eloc09cb_bcc2.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [data_raw] ennvih/doc/eloc09q_bcc1.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] BD_ENCUCI2020_dbf.zip -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] DescargaMasiva_582026_175614.zip -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] DescargaMasiva_682026_95355.zip -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] DescargaMasiva_682026_9540.zip -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] DescargaMasiva_682026_95418.zip -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] DescargaMasiva_682026_95423.zip -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] DescargaMasiva_682026_9548.zip -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] Descargas Manuales/... (53 rutas, ver bloque PENDIENTE-DE-REGISTRO abajo — no se repiten aquí)
    · [descargas_mx] FD_ENCUCI2020.pdf -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] ITER_NAL_2020_csv.zip -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] ZA5900_cdb (1).pdf -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] ZA6980_q_mx (1).pdf -- ningún id del manifiesto lo declara para esta raíz
    · [descargas_mx] descargas.php -- ningún id del manifiesto lo declara para esta raíz
    · [downloads]: 1 huérfano(s) -- solo cuenta, sin nombres (raíz no curada, ver ENMIENDA 2026-08-13)
  [ ok ]  C2 duplicado por contenido
  [ ok ]  C3 entrada sin archivo

  96 WARN  (C1=96 · C2=0 · C3=0)
  Ninguna comprobación de este script emite FAIL: no gatea nada,
  no toca tests/baseline.json, no tiene --freeze.
```

Las 53 rutas completas de `Descargas Manuales/` sí salieron en la
corrida real (el script no sabe de PENDIENTE-DE-REGISTRO, esa
clasificación es de esta nota, no del mecanismo); se omiten de la
transcripción de arriba por brevedad — están listadas íntegras en la
sección siguiente.

### (a) Huérfanos por raíz — con nombres, tamaño, mtime

**Huérfanos reales, `data_raw` (30):** las 30 rutas de arriba
(`DescargaMasivaOD_582026...`, `eder2025/...`, `enaproce2018/...` ×4,
`ennvih/doc/...` ×24). Fuera del alcance de este acto (INV-DESCMX es
inventario de Descargas MX); se listan por ser parte de la salida cruda
de C1 ahora que barre `data_raw` también, no se analizan más.

**Huérfanos reales, `descargas_mx` (12):**

| archivo | bytes | mtime | sha256 (12) |
|---|---:|---|---|
| `BD_ENCUCI2020_dbf.zip` | 6 913 684 | 2026-07-30T10:51:49 | `0414fd59e2af` |
| `DescargaMasiva_582026_175614.zip` | 658 933 | 2026-08-05T17:56:22 | `cc0f61049a9e` |
| `DescargaMasiva_682026_95355.zip` | 605 512 | 2026-08-06T09:53:57 | `0052d3788283` |
| `DescargaMasiva_682026_9540.zip` | 604 834 | 2026-08-06T09:54:02 | `d40383d2e939` |
| `DescargaMasiva_682026_95418.zip` | 688 618 | 2026-08-06T09:54:20 | `62d6fd429bce` |
| `DescargaMasiva_682026_95423.zip` | 602 522 | 2026-08-06T09:54:26 | `026acbadd261` |
| `DescargaMasiva_682026_9548.zip` | 602 173 | 2026-08-06T09:54:11 | `56ca8b51849f` |
| `FD_ENCUCI2020.pdf` | 1 758 249 | 2026-07-30T10:51:59 | `6cd6f7475a0b` |
| `ITER_NAL_2020_csv.zip` | 36 604 573 | 2026-08-03T13:21:56 | `ff39bb1d1b6e` |
| `ZA5900_cdb (1).pdf` | 5 971 210 | 2026-08-12T16:10:33 | `5c288f3c0872` |
| `ZA6980_q_mx (1).pdf` | 247 978 | 2026-08-12T16:08:44 | `61bc0c804155` |
| `descargas.php` | 141 181 | 2026-07-30T11:19:34 | `361ac35fa637` |

**PENDIENTE-DE-REGISTRO, `descargas_mx/Descargas Manuales/` (53, bloque,
no HUÉRFANO):** 65 838 388 bytes (62.8 MiB), mtime 2026-08-13T12:00:47 a
2026-08-13T13:41:41 — un solo lote continuo. Lista completa de las 53
rutas (con tamaño y mtime), cruda:

```
$ python3 -c "
import os, datetime
raiz = '/mnt/c/Users/PC0/Descargas MX/Descargas Manuales'
for fn in sorted(os.listdir(raiz)):
    p = os.path.join(raiz, fn)
    st = os.stat(p)
    print(f'{st.st_size:>10d}  {datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec=\"seconds\")}  {fn}')
"
```
(salida omitida aquí por longitud — 53 líneas, reproducible con el
comando de arriba; los 53 nombres ya aparecen íntegros en la salida
cruda de `corpus.py` pegada más arriba, sección C1.)

No se registra nada de este bloque en `data/manifiesto.yaml` — eso es
REG-LOTE3, que sigue sin correr.

**`downloads` (1):** solo cuenta, filtrado por
`EXTENSIONES_DATO_RAICES_NO_CURADAS`, sin nombre — política de esta
raíz no curada, ver COMMIT 1 y ENMIENDA en `tests/corpus.py`.

### (b) Delta contra MAP-1b (6/ago) — solo sobre huérfanos reales

MAP-1b (`data/censo-raices-2026-08-06.tsv`, `forense/notas/2026-08-06-map1b-censo-raices.md`)
encontró **2 huérfanos en `descargas_mx`**: `DescargaMasiva_582026_175614.zip`
y `descargas.php` (su total de 54 = 52 `data_raw` + 2 `descargas_mx`; el
TSV committeado no tiene filas `downloads` pese a que la nota de MAP-1b
describe haber censado esa raíz también — el detalle de `downloads` quedó
solo en prosa, `data/censo-raices-2026-08-06.tsv` nunca la incluyó, ver
nota abajo).

**Los 2 persisten sin cambio, 8 días después**, ambos siguen huérfanos
hoy: nadie los ha registrado ni movido.

**10 aparecen "nuevos" hoy en la tabla de huérfanos reales, pero no son
10 hallazgos nuevos en partes iguales:**

- **3 son reclasificación de método, no bytes nuevos:**
  `BD_ENCUCI2020_dbf.zip`, `FD_ENCUCI2020.pdf`, `ITER_NAL_2020_csv.zip`
  ya estaban en disco el 6/ago y MAP-1b ya los vio — pero los clasificó
  como **Categoría D (duplicación física entre raíces)**, no como
  huérfano, porque su método de "en_manifiesto" empareja por
  sha256+nombre a través de toda la tabla, sin importar qué `raiz`
  declara la entrada que hace match. C1 extendido es más estricto: una
  entrada declarada `raiz: data_raw` no cubre el mismo contenido bajo
  `descargas_mx` — son ubicaciones físicas distintas, cubrir una no
  cubre la otra. Confirmado por sha256: los tres archivos de disco
  coinciden byte a byte con las entradas `encuci2020_bd_dbf`,
  `encuci2020_fd_pdf`, `cpv2020_iter_nal_csv`, las tres declaradas
  `raiz: data_raw` (ausente = por convención) — exactamente los mismos
  tres que MAP-1b ya listó en su Categoría D relevante-al-programa
  (líneas 445, 446, 448 de su nota). No es un archivo nuevo; es una
  diferencia de criterio entre dos mecanismos, y el más estricto
  (C1 extendido) es el correcto: un duplicado físico entre raíces sigue
  siendo un archivo sin entrada *para esa raíz*.
- **5 son genuinamente nuevos desde el 6/ago:** los cinco
  `DescargaMasiva_682026_*.zip`, mtime `2026-08-06T09:53:57`–`09:54:26`
  — misma fecha calendario que el censo de MAP-1b pero ausentes de sus
  34 filas `descargas_mx`; llegaron después de esa corrida o quedaron
  fuera de su alcance por otra razón no determinada aquí (no es
  necesario para el delta). Los cinco tienen sha256 distintos entre sí
  (no son copias unos de otros) y no matchean ningún sha256 del
  manifiesto — contenido sin explicar todavía, mismo patrón
  "`DescargaMasivaOD_*`/`DescargaMasiva_*`: paquete bajo demanda del
  portal, sin URL persistente" que ya documentan las 5 entradas
  `descargamasiva_3072026_*` registradas.
- **2 son duplicados de re-descarga del navegador, de contenido
  registrado DESPUÉS del 6/ago:** `ZA5900_cdb (1).pdf` y
  `ZA6980_q_mx (1).pdf` (sufijo `" (1)"`, mtime 2026-08-12) son
  byte-idénticos a `za5900_cdb`/`za6980_q_mx`, registrados por
  APERTURA-ISSP (PR #200, fusionado después del censo de MAP-1b) — no
  podían aparecer en un censo de 8/ago antes, y no reflejan un vacío de
  registro, solo una descarga repetida del mismo PDF.

**Grupos de duplicación física (Categoría D):** MAP-1b reportó 5 grupos
relevantes al programa. Los 3 de arriba (BD_ENCUCI2020/FD_ENCUCI2020/
ITER_NAL_2020) siguen exactamente igual — mismos sha256, mismas dos
raíces. Los otros 2 de MAP-1b (`encig23_base_datos_csv.zip`
`data_raw`+`downloads`; `eder2025/...` interno a `data_raw`) no
involucran `descargas_mx`, fuera del alcance de este barrido, no
re-verificados aquí. Nuevos grupos hoy que sí involucran `descargas_mx`:
los 2 pares ISSP `" (1)"` de arriba, más el testigo de la sección (c).

### (c) Duplicados por contenido entre disco y manifiesto

sha256 de los 65 huérfanos-crudos de `descargas_mx` (12 reales + 53 del
cluster) cruzado contra el sha256 de las 582 entradas del manifiesto
completo. 7 coincidencias:

| archivo en disco (descargas_mx) | sha256 (12) | == entrada del manifiesto | raíz declarada |
|---|---|---|---|
| `BD_ENCUCI2020_dbf.zip` (real) | `0414fd59e2af` | `encuci2020_bd_dbf` (`BD_ENCUCI2020_dbf.zip`) | `data_raw` |
| `FD_ENCUCI2020.pdf` (real) | `6cd6f7475a0b` | `encuci2020_fd_pdf` (`FD_ENCUCI2020.pdf`) | `data_raw` |
| `ITER_NAL_2020_csv.zip` (real) | `ff39bb1d1b6e` | `cpv2020_iter_nal_csv` (`ITER_NAL_2020_csv.zip`) | `data_raw` |
| `ZA5900_cdb (1).pdf` (real) | `5c288f3c0872` | `za5900_cdb` (`ZA5900_cdb.pdf`) | `descargas_mx` |
| `ZA6980_q_mx (1).pdf` (real) | `61bc0c804155` | `za6980_q_mx` (`ZA6980_q_mx.pdf`) | `descargas_mx` |
| `Descargas Manuales/ASQ Questionnaires.zip` (cluster) | `3ea807864522` | `wb2661_asq_questionnaires` (`wb2661_ASQ_Questionnaires.zip`) | `data_raw` |
| `Descargas Manuales/ABMex2023-Mexico-Questionnaire-V9.2.3.0-Spa-230511-W.pdf` (cluster) | `0cf179c783d7` | `lapop_abmex2023_cuestionario_mexico` (`lapop_abmex2023_cuestionario.pdf`) | `data_raw` |

**Testigo esperado confirmado:** `ASQ Questionnaires.zip` (nombre del
portal, dentro de `Descargas Manuales/`) es byte-idéntico a
`wb2661_ASQ_Questionnaires.zip`, ya registrado bajo `data_raw` con
nombre distinto (prefijo `wb2661_`, la clave que le dio DESC-1). La
dedup por sha256 lo detectó, como anticipaba el encargo. Consecuencia
para REG-LOTE3, no decidida aquí: al menos 2 de los 53 archivos del
cluster (`ASQ Questionnaires.zip` y el cuestionario ABMex2023) ya tienen
contenido registrado bajo otro nombre en `data_raw` — REG-LOTE3 puede
optar por no duplicar el registro, deduplicar, o registrar de todos
modos con procedencia cruzada anotada; no es decisión de este acto.

### (d) Entradas de `descargas_mx` sin archivo en disco

`tests/manifiesto.py --verifica` (una sola invocación, sin `--id`, las
582 entradas del manifiesto completo — la restricción "una invocación
por --id" que el encargo cita (A.1) describe un defecto ya corregido el
2026-08-04 (ADR-62, comentario verbatim en `tests/manifiesto.py:368-374`);
INT-1 (6/ago) ya lo verificó y lo dejó anotado en su propia entrada de
`forense/hallazgos.md`. Se corrió sin el filtro artificial):

```
Por raíz (sin colapsar):
  data_raw: coincide=520 · no_coincide=1 · ausente=0 · sin_configurar=0
  descargas_mx: coincide=57 · no_coincide=0 · ausente=0 · sin_configurar=0
```

**Las 57 entradas de `descargas_mx`: 57 COINCIDE, 0 AUSENTE, 0
raíz-no-configurada, 0 hash-discordante.** Limpio, completo, sin
excepción — ninguna de las tres respuestas separadas que pedía el
encargo tiene un solo caso que reportar caso por caso.

Nota fuera de alcance: el 1 `no_coincide` es `data_raw`, no
`descargas_mx` — `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf`,
una de las 3 "colgadas" que MAP-1b/INT-1 ya diagnosticaron el 6-7/ago;
REPAIR-1 registró el contenido real bajo id nuevo
(`..._redescarga`) sin editar la entrada original — el `NO COINCIDE` es
esperado y ya está documentado, no es un hallazgo nuevo de este acto.

### (e) Barrido de completitud por módulo

Confirmado contra disco (`os.walk` sobre `descargas_mx` completo,
buscando `ZA5900`/`ZA6980`/`ZA7600` en cualquier nombre, más
`data/raw`, cero resultados ahí):

| módulo | archivos registrados | sufijos presentes | sufijos ausentes frente a ZA5900 |
|---|---:|---|---|
| ZA5900 | 10 | `backgroundvar_mx` · `bq` · `cdb` · `mr` · `overview` · `q_mx` · `questionnaire_development_report` · microdato (`.dta`/`.por`/`.sav`) | — (plantilla) |
| ZA6980 | 4 | `backgroundvar_mx` · `q_mx` · microdato (`.dta`/`.sav`, sin `.por`) | `_bq` · `_cdb` · `_mr` · `_overview` · `_questionnaire_development_report` · `.por` |
| ZA7600 | 2 | microdato (`.dta`/`.sav`, sin `.por`) | todo lo documental, incluidos `_q_mx` y `_cdb` |

Confirmado, no solo derivado: ningún archivo `ZA6980_bq*`, `*_cdb*`,
`*_mr*`, `*_overview*`, `*_questionnaire_development_report*` ni
`ZA6980*.por` existe en ningún lugar del disco (ni `descargas_mx` ni
`data_raw`, huérfano o registrado) — no es "se bajó y no se registró",
es SIN-FETCH real. Mismo resultado para toda la documentación de ZA7600.
ZA7600 tiene microdato sin codebook ni cuestionario: sin diccionario no
se puede localizar un reactivo, está en disco y es inservible tal cual.

**Reserva obligatoria (A.6):** la ausencia de un sufijo frente a un
módulo hermano es evidencia de segunda mano — GESIS podría no publicar
`cdb`/`mr` para todos los módulos del ISSP. Se rotula SIN-FETCH, no
"falta". Receta manual para quien priorice la adquisición:

- https://www.gesis.org/en/issp/data-and-documentation/social-inequality/2019
- https://www.gesis.org/en/issp/data-and-documentation/social-networks/2017

No se encontró otra familia multi-módulo con huecos en `descargas_mx`
(ENSANUT 2024, sus 5 poblaciones × formatos, todas COINCIDE; WVS, un
solo wave con variantes de formato, no de módulo) — ISSP es el único
caso con sufijos ausentes hoy.

## Cierre

```
$ python3 tests/check.py --baseline    # ANTES de este acto (antes de tocar corpus.py y el árbol)
...
  20 FAIL · 107 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 3d0d1e5fd05567e59f8df65b2e1495b43bbcfc3c)
```

```
$ python3 tests/check.py --baseline    # DESPUÉS de COMMIT 1 + COMMIT 2
...
  20 FAIL · 107 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 3d0d1e5fd05567e59f8df65b2e1495b43bbcfc3c)
```

Idéntico antes y después — esperado: este acto no toca `canon/`, no
edita `data/manifiesto.yaml`, `tests/corpus.py` está fuera de
`tests/check.py` por diseño.

## Lo que este acto NO hizo

No registró nada en `data/manifiesto.yaml` (eso es REG-LOTE3, incluido
el bloque completo de `Descargas Manuales/`, reportado como
PENDIENTE-DE-REGISTRO, no huérfano). No borró, movió, copió ni renombró
ningún archivo de ninguna raíz. No descargó nada. No selló ADR. No metió
`corpus.py` a la suite. No emitió FAIL. No clasificó ningún archivo como
"sobra" ni "basura". No decidió si REG-LOTE3 debe deduplicar los 2
archivos del cluster que ya tienen contenido registrado bajo otro
nombre (sección c) — se deja anotado para quien lo corra.

**Hueco de índice, entregable de este acto:** `data/INFRAESTRUCTURA-v1_0.md`
no tiene dominio para "inventariar una raíz" — ocho dominios, ninguno
cubre este mecanismo (`tests/corpus.py`, C1/C2/C3). No se resuelve aquí,
se reporta (A.8 pregunta 1).

**Contadores que NO se movieron:** 13 de 27 · 9 de 14 · 0 de 15 · 1 de 2
· 4 de 144 — ninguno.

**Contador que sí se instituye:** archivos de raíces no integradas con
entrada de manifiesto / archivos presentes. Hoy, `descargas_mx`: 57
entradas con payload / 122 archivos en disco (69 archivos, 1 subcarpeta
`Descargas Manuales/` con 53) → 57 cubiertas, 12 huérfanas reales, 53
pendientes-de-registro (cluster REG-LOTE3). Precedente contra el cual
medir la próxima vez: MAP-1b, 6/ago, 29 de 34 (2 huérfanas, 3 que hoy se
saben duplicados físicos de `data_raw`).
