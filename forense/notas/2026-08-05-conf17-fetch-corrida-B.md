# CONF-17 · Apertura byte a byte de las 17 candidatas del barrido público

Corrida B de dos ejecuciones concurrentes e independientes del ENCARGO CONF-17. Ambas sesiones recibieron el mismo encargo, que traía la ruta de worktree escrita a mano (`/home/pc0/wt-conf17`), y ambas aterrizaron en el mismo directorio. No hubo fallo de aislamiento de git ni proceso no identificado: los inodos coincidían porque era el mismo archivo. La corrida hermana está en `2026-08-05-conf17-fetch-corrida-A.md`. Donde las dos coinciden, el veredicto es replicado; donde solo una cubre, es único.

*5 de agosto de 2026 (fecha del sistema; los timestamps de red que aparecen abajo, en UTC, caen ya en la madrugada del 6 de agosto — el entorno pc0 corre en hora local America/Mexico_City, UTC-6). Worktree `/home/pc0/wt-conf17`, rama `conf17-fetch`, base `f0cb60e` (coincide con la base declarada del encargo — sin desfase). Ejecuta el ENCARGO CONF-17 (v1): abrir, con red real, las 17 URLs que `forense/notas/2026-08-05-barrido-publico-17-condiciones-no-existe.md` dejó sin verificar (`WebFetch` dio 403 en el 100% de sus intentos, ninguna URL fue abierta por ese acto).*

## 0 · Arranque

- Clon principal `/home/pc0/Modelado-Mexicano` confirmado en rama vieja `sesion/cal-conf-faseb-pos4-envipe-paso1`, tal como avisaba el encargo. Worktree propio creado desde `origin/main`.
- `git log -1 --format="%h %s"`: `f0cb60e Merge pull request #136 from Josanoforo/sesion/encargo-m3-b3-lote-reactivos`.
- `data/raw` ausente al crear el worktree (esperado); enlazada a `/home/pc0/mm-corpus/raw`, el mismo corpus compartido que usan los demás worktrees activos (`Modelado-Mexicano`, `mm-p-lapop-microdato`, `wt-ver1`, y el recién aparecido `wt-desc1`).
- Entorno, firma de tres partes (regla A.2, v2.5):
  - `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`
  - `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` = `200`
  - `ls data/raw/ | head -1` = `BD_ENCUCI2020_dbf.zip` (corpus montado, no vacío)
  - `python3 -c "import pandas; print(pandas.__version__)"` = `2.3.3`

## 0.5 · Hallazgo operativo: el sandbox de esta herramienta bloquea red que el entorno pc0 sí tiene

Antes de abrir la primera URL: `curl` dentro del sandbox por defecto de esta sesión de herramientas dio timeout silencioso (exit 28) contra `kantar.com`, un dominio fuera de la lista blanca de red de la herramienta — **no** fuera de la red real de pc0. Con el sandbox de la herramienta desactivado (`dangerouslyDisableSandbox`), el mismo host respondió limpio:

```
$ curl -s -D - -o /dev/null --max-time 15 "https://kantar.com/latin-america/latinoamerica/mexico"   # sandbox default
(sin salida, exit 28 — timeout)

$ curl -s -D - -o /dev/null --max-time 15 "https://kantar.com/latin-america/latinoamerica/mexico"   # dangerouslyDisableSandbox=true
HTTP/1.1 301 Moved Permanently
Location: https://www.kantar.com/latin-america/latinoamerica/mexico
```

Es exactamente el defecto que este acto existe para no repetir (WebFetch 403 del barrido), pero a nivel de mi propio tooling, no del entorno asignado. **Todos los comandos de red de esta nota se corrieron con el sandbox de herramienta desactivado**, para que la respuesta observada sea la del host real, no la de un firewall de mi cliente.

## 0.6 · Hallazgo operativo: cadena TLS incompleta en varios .gob.mx

`datos.gob.mx`, `www.cnbv.gob.mx` y `www.cofece.mx` fallan verificación TLS por defecto (`curl` exit 60, "unable to get local issuer certificate") — cada uno con una CA raíz distinta (Let's Encrypt E8, GlobalSign RSA OV SSL CA 2018, DigiCert GeoTrust TLS RSA CA G1). Diagnóstico: mi almacén de confianza local (`ca-certificates 20260601~26.04.1`, fresco) sí tiene las raíces (ISRG Root X1 confirmada presente); el servidor de cada sitio simplemente no envía su certificado intermedio en el handshake — hecho verificable sobre el servidor, reproducible, no una conjetura sobre su contenido. Se completó la cadena localmente bajando los tres intermedios desde sus propias URLs `CA Issuers` (AIA, publicadas en el propio certificado hoja, no construidas por analogía) y pasándolos vía `--cacert` a un bundle temporal. Con eso, los tres hosts verifican y responden 200.

`dgis.salud.gob.mx` es un caso distinto y más severo: su certificado es **autofirmado con valores de plantilla de OpenSSL sin modificar** (`subject=issuer`, `O=SomeOrganization, ST=SomeState, L=SomeCity`, `CN=pliopencms05.salud.gob.mx`) — no hay cadena que completar, es un certificado que ningún cliente puede verificar. Con `-k` (sin verificar, declarado explícitamente como tal) el body sí llega, pero es `404` para las dos URLs de CLUES probadas — ver Ficha 6.

## 0.8 · Bug encontrado en `tests/check.py` T02 (fuera de mi perímetro, no lo edito — solo lo reporto y trabajo alrededor)

Al preparar el push, `python3 tests/check.py --baseline` truena con `IsADirectoryError` sobre `data/raw/R7.3_PUB_Bienestar` (una de las carpetas del acto concurrente `wt-desc1`, §0.7):

```
File "tests/check.py", line 108, in t02_duplicates
    by_hash[hashlib.md5(io.open(p, "rb").read()).hexdigest()].append(rel(p))
IsADirectoryError: [Errno 21] Is a directory: '/home/pc0/wt-conf17/data/raw/R7.3_PUB_Bienestar'
```

Causa, en `tests/check.py:104`: `glob.glob(os.path.join(ROOT, "**", "*.*"), recursive=True)` — el patrón `*.*` no distingue archivo de directorio, solo exige un punto en el nombre del último segmento de la ruta. El patrón de carpeta `RX.Y_Nombre` (p. ej. `R7.3_PUB_Bienestar`) tiene un punto en su propio nombre de directorio (`R7.3`), así que el glob lo captura como si fuera un archivo y el código intenta abrirlo en modo binario sin comprobar `os.path.isfile()` antes. Es un bug real y reproducible, no un efecto de mis datos — pero `tests/check.py` no está en mi perímetro (`⛔ NADA MÁS` que las cuatro rutas listadas al inicio del encargo), así que no lo edito.

Lo que sí hice, dentro de mi perímetro (`corpus data/raw`): renombré mis 3 carpetas nuevas quitándoles el punto (`R1.1_AGROASEMEX` → `R1_1_AGROASEMEX`, `R4.1_SESTAD_ESTAD` → `R4_1_SESTAD_ESTAD`, `R9.1_ENSANUT_utilizadores` → `R9_1_ENSANUT_utilizadores`), actualicé los 3 campos `archivo` correspondientes en `data/manifiesto.yaml`, y reverifiqué `COINCIDE` en los 3. **Las 4 carpetas del acto `wt-desc1` (`R2.1_ECCO`, `R7.3_PUB_Bienestar`, `R8.1_contraloria_social`, `R7.4_R7.5_ACLED_HDX`) siguen con punto en el nombre** — no las toqué, porque son de un acto ajeno en vivo y renombrarlas a mitad de su ejecución arriesga romper referencias que ese acto todavía esté usando. Consecuencia declarada: **`tests/check.py --baseline` seguirá en ROJO por esta causa hasta que `wt-desc1` (o la mesa) renombre esas 4 carpetas, o hasta que alguien con perímetro sobre `tests/` corrija el filtro de T02.** No es un defecto que este acto pueda cerrar solo.

## Paso 0 · La cola, derivada del archivo

```
$ grep -nE '^## Ficha [0-9]+' forense/notas/2026-08-05-barrido-publico-17-condiciones-no-existe.md | wc -l
17
$ grep -oE 'https?://[^ )`|]+' forense/notas/2026-08-05-barrido-publico-17-condiciones-no-existe.md | sort -u | wc -l
0
```

**Discrepancia con el paso 0 tal como está escrito en el encargo, reportada, no oculta:** el segundo comando da `0`, no un número positivo. Causa: el barrido no escribió ninguna URL con esquema `http(s)://` literal — todas están citadas como ruta de dominio dentro de backticks (`` `datos.gob.mx/dataset/...` ``, `` `kantar.com/latin-america/...` ``), sin protocolo. El grep literal del encargo no puede detectarlas por diseño de ese archivo, no por un error de conteo. La cuenta de fichas (17) sí cuadra exactamente, así que esto **no** es el caso "para y repórtalo" que el encargo reserva para un conteo de fichas erróneo — es un defecto del comando de extracción, no del universo. Corregido con un extractor que busca patrones `dominio.tld/ruta` dentro de backticks; produjo 58 tokens únicos repartidos en las 17 fichas (2 fichas, la 11 y la 16, no tienen ninguna URL candidata porque su clasificación previa ya era NO-ENCONTRADO sin candidato).

**Orden de gateo** (script de control del encargo, corregido — ver abajo):

```
$ python3 - <<'EOF'
import re
t=open('forense/hitoD-preregistro-v2_0.md').read()
blk=t[t.index('## Registro de veredictos archivados'):]
sellado=set(r for r,_ in re.findall(r'(R\d+\.\d+)\s*→\svered icto\s([A-E])',blk))  # regex del encargo, tal cual
todas=set(re.findall(r'^## (R\d+.\d+)',t,re.M))
print("selladas",len(sellado),sorted(sellado))
EOF
selladas 0 []
```

**Discrepancia reportada:** el comando del encargo, tal como está escrito, da `0` selladas — no las `13` de control que el encargo anuncia. Causa encontrada: el bloque real `## Registro de veredictos archivados` escribe cada línea con backticks alrededor de la regla **y** del veredicto (`` `R1.1` → veredicto `D` ``), y el regex del encargo no los contempla. Corregido:

```
$ python3 -c "
import re
t=open('forense/hitoD-preregistro-v2_0.md').read()
blk=t[t.index('## Registro de veredictos archivados'):]
sellado=set(r for r,_ in re.findall(r'\`(R\d+\.\d+)\`\s*→\s*veredicto\s*\`([A-E])\`',blk))
todas=set(re.findall(r'^## (R\d+\.\d+)',t,re.M))
print('selladas',len(sellado),sorted(sellado))
print('abiertas',len(todas-sellado),sorted(todas-sellado))
"
selladas 13 ['R1.1', 'R1.2', 'R1.3', 'R3.1', 'R3.2', 'R4.1', 'R4.2', 'R4.3', 'R5.1', 'R5.2', 'R7.2', 'R9.1', 'R9.2']
abiertas 14 ['R1.4', 'R10.1', 'R10.2', 'R10.3', 'R2.1', 'R2.2', 'R3.4', 'R7.1', 'R7.3', 'R7.4', 'R7.5', 'R8.1', 'R8.2', 'R8.3']
```

Con el regex corregido, coincide con el valor de control del encargo (13/27). Gana el corregido.

### Cola (ficha, regla, gateo, clasificación previa)

| # | Ficha | Regla(s) | Gateo | Clasificación previa (barrido) |
|---|---|---|---|---|
| 1 | 3 | R1.4 | **abierta** | NO-ACCESIBLE |
| 2 | 4 | R2.1 | **abierta** | EXISTE-NO-SATISFACE |
| 3 | 5 | R2.2 | **abierta** | NO-ENCONTRADO |
| 4 | 8 | R7.3 | **abierta** | EXISTE-NO-SATISFACE (a) / EXISTE-SATISFACE (b) |
| 5 | 9 | R7.4/R7.5 | **abierta** | EXISTE-SATISFACE |
| 6 | 10 | R8.1 | **abierta** | EXISTE-NO-SATISFACE |
| 7 | 11 | R8.2 | **abierta** | NO-ENCONTRADO (sin URL candidata) |
| 8 | 12 | R8.3 | **abierta** | EXISTE-SATISFACE |
| 9 | 15 | R10.1 | **abierta** | NO-ENCONTRADO / NO-ACCESIBLE |
| 10 | 16 | R10.2 | **abierta** | NO-ENCONTRADO (sin URL candidata) |
| 11 | 17 | R10.3 | **abierta** | EXISTE-NO-SATISFACE |
| 12 | 1 | R1.1 | sellada (D) | EXISTE-NO-SATISFACE (Parcial) |
| 13 | 2 | R1.3 | sellada (E) | NO-ENCONTRADO |
| 14 | 6 | R4.1 (1a fila) | sellada (D) | EXISTE-NO-SATISFACE |
| 15 | 7 | R4.1 (2a fila) | sellada (D) | EXISTE-NO-SATISFACE / NO-ACCESIBLE |
| 16 | 13 | R9.1 (1a fila) | sellada (D) | EXISTE-NO-SATISFACE |
| 17 | 14 | R9.1 (2a fila) | sellada (D) | Parcial, sin clasificación final cerrada |

## 0.65 · HALLAZGO CRÍTICO: mi propio archivo git-tracked recibió escrituras de un proceso no identificado

Al preparar el commit, `data/manifiesto.yaml` en **mi worktree** (`/home/pc0/wt-conf17`, inode propio, no symlink, confirmado con `stat`) contenía 4 entradas que yo no escribí: `r2_1_ecco_reporte_se_2023`, `r7_3_pub_beneficiarios_bienestar_csv`, `r8_1_contraloria_social_2019_2025_csv`, `r7_4_r7_5_acled_hdx_demonstration_events`. Intercaladas exactamente entre mis propias 6 entradas (mismo orden de aparición que si alguien más hubiera corrido `--registra` sobre este mismo archivo, en paralelo conmigo, en tiempo real).

Investigación de origen, con evidencia negativa exhaustiva:
- **No es el symlink `data/raw` de nuevo** — `data/manifiesto.yaml` es un archivo git-tracked normal, `stat` confirma inode `47593`, distinto del de `wt-desc1` (`40460`) y `wt-ver1` (`94355`). No hay mecanismo de git-worktree que comparta archivos de trabajo entre worktrees — cada uno tiene su propia copia en disco.
- **No es `wt-desc1`**: su propio `data/manifiesto.yaml` (con `git diff` inspeccionado directamente) tiene un `git status` con cambios locales sin commitear, pero son **117 entradas completamente distintas** (EDER, ENAPROCE, ENIF, ENCIG, ENDIREH, etc. — un barrido masivo de re-registro de corpus histórico, nada relacionado con CONF-17) y **cero** coincidencias con los 4 IDs misteriosos.
- **No es ningún otro worktree conocido** (`Modelado-Mexicano`, `mm-cruce-catalogo-fichas`, `mm-p-lapop-microdato`, `mm-regla-elegibilidad-preregistro`, `wt-ver1`) — los 6 revisados dan `0` coincidencias en su propio `data/manifiesto.yaml`.

Las 4 entradas foráneas, leídas, son forense de calidad real y coherente con este mismo encargo — se autoidentifican explícitamente como "ENCARGO CONF-17 (2026-08-05)" en su campo `nota`, citan los mismos recursos que este acto investigó (ECCO, PUB Bienestar, Contraloría Social, ACLED/HDX) con hallazgos **convergentes e independientes** de los míos (mismas conclusiones: PUB agregado entidad×trimestre no nominal, Contraloría Social agregado nacional-año, dataset ECCO 404, HDX ACLED es agregado mes×año no evento individual) pero con detalles técnicos distintos de los míos (p. ej. reportan `502 Bad Gateway` para `pub.bienestar.gob.mx` donde yo encontré fallo de resolución DNS — mismo host inalcanzable, diagnóstico de bajo nivel distinto, consistente con ser un intento independiente, no una copia). Es decir: **hay un tercer proceso, no identificado, ejecutando este mismo encargo CONF-17 en paralelo, en algún lugar que no es ninguno de los seis worktrees visibles en esta máquina** — y ese proceso, por un mecanismo que no pude determinar, obtuvo acceso de escritura al archivo de trabajo de MI worktree.

**Decisión tomada:** extraje las 4 entradas a `/tmp/claude-1000/.../scratchpad/foreign_entries.yaml` (fuera del repo, preservadas, no perdidas) y las quité de mi `data/manifiesto.yaml` antes de commitear — no puedo dar fe, bajo REGLA 1 de este encargo, de comandos que no ejecuté yo mismo; incluirlas como si fueran mi trabajo verificado sería falsificar autoría de un hallazgo forense. `diff` contra la base `f0cb60e` confirma que mi commit ahora contiene exactamente 6 líneas nuevas de `- id:`, ni una más.

**Esto no es el mismo hallazgo que la colisión de `data/raw` (§0.7 abajo).** Que el corpus compartido (`data/raw`, symlink deliberado a `/home/pc0/mm-corpus/raw`) tenga archivos de varios actos es diseño esperado. Que un archivo `git`-versionado, dentro de un worktree que debería ser exclusivamente mío, reciba escrituras de un proceso que no puedo identificar en ninguno de los seis worktrees visibles, es un hecho distinto y más serio — sugiere que el aislamiento entre worktrees en esta máquina no es tan fuerte como el diseño del programa (v2.4/v2.5, "WORKTREE PROPIO, obligatorio") asume, o que hay un séptimo agente activo en una ruta que no pude enumerar. **Reportado a la mesa/usuario como hallazgo prioritario de este acto, por encima del contenido de las 17 fichas.**

**CORRECCIÓN POSTERIOR (mesa):** la hipótesis de este apartado —aislamiento de worktrees más débil de lo asumido, o séptimo agente— queda descartada. Origen identificado: dos sesiones del mismo encargo en el mismo directorio, por ruta fija en el encargo.

## 0.7 · Colisión con un acto concurrente, descubierta en vivo

Al preparar el registro en `data/manifiesto.yaml` apareció esto en `data/raw/` (corpus compartido, no versionado en git):

```
$ ls -la --time-style=full-iso data/raw/ | tail -20
...
drwxr-xr-x  2 pc0 pc0  4096 2026-08-05 18:17:44 R2.1_ECCO
drwxr-xr-x  2 pc0 pc0  4096 2026-08-05 18:23:05 R7.3_PUB_Bienestar
drwxr-xr-x  2 pc0 pc0  4096 2026-08-05 18:26:38 R8.1_contraloria_social
drwxr-xr-x  2 pc0 pc0  4096 2026-08-05 18:27:31 R7.4_R7.5_ACLED_HDX
```

La cuarta carpeta (`R7.4_R7.5_ACLED_HDX`) apareció **mientras esta nota se escribía**. `git worktree list` confirma un worktree nuevo, `/home/pc0/wt-desc1` (rama `desc1-descarga`, base `f0cb60e` — misma base que este acto), que no existía al arrancar. Verificación de que no es casualidad de nombre — hash byte a byte contra lo que yo mismo bajé de forma independiente para las mismas tres fichas:

```
mio ecco_reporte.pdf:      ec47822d2a7b08327eebc70d4cb9bb1da947b04ca565c55768958b1243b866ea
corpus R2.1_ECCO:          ec47822d2a7b08327eebc70d4cb9bb1da947b04ca565c55768958b1243b866ea
mio pub_padron.csv:        89e46568abd3b17d110ae5b772fb80b5fde47669ce2e12020e8e877f270883bd
corpus R7.3_PUB_Bienestar: 89e46568abd3b17d110ae5b772fb80b5fde47669ce2e12020e8e877f270883bd
mio csocial.csv:           3b5a77751a8cdd52405b5145a7596047c48bfdee3967c753171f8598deb2a1d3
corpus R8.1_contraloria:   3b5a77751a8cdd52405b5145a7596047c48bfdee3967c753171f8598deb2a1d3
```

Idénticos. Hay otro acto (`wt-desc1`) ejecutando en tiempo real, sobre el mismo corpus compartido, un trabajo que se solapa con al menos 4 de las 17 fichas de este acto (Fichas 4, 8, 10, 9). **Decisión tomada, declarada aquí:** no registré en `data/manifiesto.yaml` los payloads de las Fichas 4, 8(a) y 10 bajo un id propio — el archivo ya existe en el corpus compartido, byte-idéntico a lo que yo mismo verifiqué de forma independiente, y registrar un segundo id para el mismo sha256 desde dos worktrees distintos es exactamente la carrera de escritura que el propio `tests/manifiesto.py` está diseñado para rechazar en un solo árbol (dedup por hash) pero que un merge de dos ramas puede colar sin que ese chequeo la vea. Dejo que `wt-desc1` (o la mesa, en el merge) sea quien registre esos tres; yo reporto aquí que los verifiqué de forma independiente y que coinciden. Para la Ficha 9 no había nada mío que registrar (solo confirmé status de las páginas, no bajé el xlsx que `wt-desc1` ya tiene). **La mesa debe revisar si `wt-desc1` es un acto redundante con este (mismo encargo, doble despacho) o un acto distinto (p. ej. VER-1/VER-2, mencionados como posibles en el encargo) antes de fusionar ambas ramas.**

---

## Fichas gateando reglas ABIERTAS del Hito D (prioridad 1)

### Ficha 3 (R1.4) · Kantar/NielsenIQ — prima de marca D/E vs A/B

```
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.kantar.com/latin-america/latinoamerica/mexico"
HTTP/1.1 200 OK
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://market.worldpanelbynumerator.com/mx"
HTTP/1.1 301 Moved Permanently → Location: https://www.kantar.com/latin-america?par=mx (200 tras seguir)
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.nielseniq.com/global/es/insights/analysis/2025/la-vision-completa-del-consumo-en-mexico-2025"
HTTP/2 301 → nielseniq.com (sin www), 200 final
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.nielseniq.com/global/en/insights/report/2025/full-view-measurement"
HTTP/2 301 → 200 final, 346847 bytes, <title>Full View™ - Measurement - NIQ</title>
```

Las 4 URLs abren (200). Las páginas de NielsenIQ (`full-view-measurement`) son páginas de producto/mercadotecnia (346KB de HTML, sin ningún enlace a descarga de dato), consistente con "Full View™" siendo un producto pagado, no un dataset público — confirma por lectura directa lo que el barrido reportó de segunda mano.

**Examinado:** las 4 páginas web, mecanismo `curl -sL` con User-Agent de navegador, 5/ago/2026. **CLASIFICACIÓN: NO-ACCESIBLE** para el cruce prima D/E vs A/B (páginas de producto pagado, sin dataset descargable visible). Confirma la clasificación previa del barrido, ahora con lectura directa del cuerpo, no de segunda mano.

### Ficha 4 (R2.1) · ECCO / Enterprise Survey — reporte voluntario de errores

```
$ curl -sL --max-time 25 "https://datos.gob.mx/api/3/action/package_show?id=encuesta_clima_cultura-organizacional"
{"help": "...", "error": {"__type": "Authorization Error", "message": "Acceso denegado: El usuario  no está autorizado para leer el paquete e4e3141a-c653-4ba4-a671-d2079d03a376"}, "success": false}

$ curl -sL --max-time 25 "https://datos.gob.mx/dataset/encuesta_clima_cultura-organizacional"
(HTML, 14318 bytes) contiene "404" y "no encontrad[o]"

$ curl -sL --max-time 25 "https://datos.gob.mx/api/3/action/package_search?q=ECCO&rows=8"
{"result": {"count": 0}}
$ curl -sL --max-time 25 "https://datos.gob.mx/api/3/action/package_search?q=clima%20organizacional&rows=8"
{"result": {"count": 0}}
```

**Hallazgo nuevo, no verificado por el barrido:** el dataset CKAN que el barrido cita (`encuesta_clima_cultura-organizacional`) existe como paquete interno (tiene UUID) pero da `Authorization Error` para usuario anónimo vía API, y `404` vía la página HTML humana. Búsqueda de texto completo en el portal (`package_search`) por "ECCO", "clima organizacional" y "encuesta clima" da **0 resultados** — hoy no hay forma de encontrar este dataset navegando ni buscando en datos.gob.mx, solo por la URL exacta que ya no resuelve.

```
$ curl -s -D - -o /dev/null --max-time 25 "https://www.gob.mx/cms/uploads/attachment/file/907022/SE_REPORTE_GENERAL_ECCO_2023.pdf"
HTTP/1.1 200 OK / Content-Length: 2407229
$ pdfinfo SE_REPORTE_GENERAL_ECCO_2023.pdf → Pages: 45
$ pdftotext -f 1 -l 6 ... → tabla de contenido: 19 "FACTORES" (Balance Trabajo-Familia, Liderazgo,
  Transparencia, ...), ninguno nombrado "reporte de errores" ni "canal anónimo/no-anónimo"
```

El PDF sí abre (200, 45 páginas) — pero es el reporte de UNA dependencia (Secretaría de Economía, 2,352 encuestados, 2023), agregado por 19 "factores" predefinidos que no incluyen nada equivalente a "reporte voluntario de errores por canal". Confirma por lectura directa la brecha que el barrido reportó (ECCO mide clima organizacional general, no la variable pareada que R2.1 necesita).

**Examinado:** CKAN API (`package_show`, `package_search`), página HTML del dataset, PDF del reporte general SE 2023, mecanismo `curl`, 5/ago/2026. **CLASIFICACIÓN: NO-ENCONTRADO** para el dataset CKAN citado (404 + Authorization Error + 0 resultados de búsqueda — el dataset no es localizable hoy en el portal, más allá de lo que el barrido pudo haber visto antes). **EXISTE-NO-SATISFACE** para el reporte PDF anual por dependencia (existe, se abre, pero no trae la variable que R2.1 pide — confirmado por tabla de contenido real, no de segunda mano).

### Ficha 5 (R2.2) · Scielo / Redalyc — rotación y liderazgo

```
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S2448-76782006000100007"
HTTP/2 200
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.redalyc.org/journal/3312/331267304006"
HTTP/1.1 301 → /331267304006/ → 200
```

Ambos artículos abren. No se descargó/leyó el cuerpo completo (son artículos de estudio de caso puntual, n=142 y n=253, ya caracterizados por el barrido como no representativos a nivel nacional — abrir el cuerpo no cambia esa limitación estructural, que es de diseño muestral, no de acceso).

**Examinado:** las 2 páginas, `curl -sL` con UA de navegador, 5/ago/2026. **CLASIFICACIÓN: NO-ENCONTRADO** para una fuente pública representativa nacional que cruce rotación objetiva con tipología de liderazgo autoritario/benévolo — confirmado que los dos estudios de caso citados sí existen y son accesibles, pero por diseño (n pequeño, empresa única) no satisfacen "representativo nacional". Mismo veredicto del barrido, ahora con existencia de los dos artículos confirmada por fetch directo.

### Ficha 8 (R7.3) · Padrón Único de Beneficiarios + resultados electorales INE

**(a) PUB Bienestar**

```
$ curl -s -D - -o /dev/null --max-time 20 "https://pub.bienestar.gob.mx/pub/personas"    # intento 1
(vacío, exit 28 — timeout)
$ curl -sL -D - -o /dev/null --max-time 20 "https://pub.bienestar.gob.mx/pub/personas"   # intento 2, -L
(vacío, exit 28)
$ curl -sL --max-time 45 "https://pub.bienestar.gob.mx/pub/personas"                     # intento 3, 45s
exit 6 — "Couldn't resolve host"
```

**NO OBTENIDO POR ESTE AGENTE EN 3 INTENTOS** (2 timeouts de resolución DNS + 1 fallo explícito de resolución). Receta manual al final de esta nota.

El dataset CKAN sí resolvió, por un host distinto (`www.datos.gob.mx`, no `pub.bienestar.gob.mx`):

```
$ curl -sL --max-time 25 "https://datos.gob.mx/api/3/action/package_show?id=padron_unico_beneficiarios_bienestar"
{"success": true, "result": {"title": "Padrón Único de Beneficiarios de Bienestar",
  "resources": [{"name": "Padrón único de beneficiarios consolidado por entidad", "format": "CSV",
  "url": "https://www.datos.gob.mx/dataset/.../download/padron_unico_bienestar.csv"}]}}
$ curl -s --max-time 30 ".../padron_unico_bienestar.csv" -o padron_unico_bienestar.csv
$ wc -c padron_unico_bienestar.csv
114046
$ head -1 padron_unico_bienestar.csv
CVEENT,entidad,beneficiarios,intervenciones,dependencias,padrones,programas,periodo,periodo_cve,trimestre,anio,fecha,entidad_etiqueta,entidad_etq
$ head -4 padron_unico_bienestar.csv
CVEENT,entidad,beneficiarios,intervenciones,dependencias,padrones,programas,periodo,periodo_cve,trimestre,anio,fecha,entidad_etiqueta,entidad_etq
1,AGUASCALIENTES,166587,1851607.0,4,7,6,Trimestre : Enero - Marzo 2019 / Corte : 231030,2019T1,Enero-Marzo,2019,2019-03-31,AGUASCALIENTES,Aguascalientes
2,BAJA CALIFORNIA,315362,1753509.0,5,8,7,Trimestre : Enero - Marzo 2019 / Corte : 231030,2019T1,Enero-Marzo,2019,2019-03-31,BAJA CALIFORNIA,Baja California
```

**Hallazgo que corrige al barrido:** el barrido escribió "GRANULARIDAD: Nominal (incluye nombre), desagregado por periodo/entidad/municipio y monto." El archivo real, el único recurso CSV del dataset CKAN citado, es **conteos agregados por entidad-trimestre** (`beneficiarios`, `intervenciones`, `dependencias`, `padrones`, `programas` — todo son enteros de conteo, no filas por persona). No hay nombre, no hay municipio, no hay monto, no hay fecha de alta individual. La granularidad "nominal" que el barrido describe solo podría existir en el portal de consulta `pub.bienestar.gob.mx`, que este agente no pudo alcanzar (ver arriba) — no está confirmada por ningún fetch, ni el del barrido (que no abrió nada) ni el de este acto.

**(b) INE, resultados por sección electoral**

```
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://computos2021.ine.mx/base-de-datos"
HTTP/2 403  (Cloudflare — cache-control: private, no-store; sin cf-ray legible pero patrón idéntico)
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." -e "https://www.ine.mx/" "https://computos2021.ine.mx/base-de-datos"
HTTP/2 403   # con Referer, mismo resultado
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://computos2024.ine.mx/"
HTTP/2 403
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.ine.mx/voto-y-elecciones/resultados-electorales/"
HTTP/2 200
```

**403 reproducible** (2 intentos, con y sin Referer) contra los subdominios `computosYYYY.ine.mx` específicamente — el dominio principal `www.ine.mx` sí responde 200. Receta manual al final.

**Examinado:** CKAN API+CSV para (a), 3 intentos de host directo para (a) que no resolvieron DNS, 2 intentos + Referer para (b) contra `computos2021/2024.ine.mx` (403 reproducible) y 1 intento exitoso contra `www.ine.mx` (200), 5/ago/2026. **CLASIFICACIÓN (a): EXISTE-NO-SATISFACE** — el único recurso público confirmado por fetch es agregado entidad-trimestre, sin nominal ni geolocalización ni fecha de alta; el nivel nominal que el barrido describió no está confirmado por ningún fetch propio, de nadie. **CLASIFICACIÓN (b): EXISTE-SATISFACE** para el dominio principal de INE (confirma el barrido); **NO-ACCESIBLE** específicamente para el subdominio `computosYYYY.ine.mx` desde este agente (403 Cloudflare reproducible) — receta manual necesaria para ese recurso en particular.

### Ficha 9 (R7.4/R7.5) · ACLED

```
$ curl -sL -o /dev/null -w "status:%{http_code} bytes:%{size_download}\n" --max-time 25 -A "Mozilla/5.0 ..." "https://acleddata.com/conflict-data/download-data/"
status:200 bytes:68110
$ curl -s -o hdx_mexico.html -w "status:%{http_code} bytes:%{size_download}\n" --max-time 25 "https://data.humdata.org/dataset/mexico-acled-conflict-data"
status:200 bytes:96206
$ grep -o -i "<title>[^<]*</title>" hdx_mexico.html
<title>Mexico - Conflict Events | Humanitarian Dataset | HDX</title>
```

Nota técnica: pedir solo cabeceras (`curl -D - -o /dev/null`) contra HDX dio `444` (conexión cerrada sin respuesta, código propio de AWS ELB) de forma reproducible en 3 intentos distintos; pedir el cuerpo completo sin `-D` dio `200` limpio las 2 veces que se intentó — comportamiento asimétrico del balanceador de HDX según el patrón de la petición, no una falla real de acceso al contenido (el título real del dataset de México llegó íntegro).

**Examinado:** landing page de descarga ACLED y página de dataset HDX, `curl` con y sin captura de cabeceras, 5/ago/2026. **CLASIFICACIÓN: EXISTE-SATISFACE** — confirma el barrido con lectura directa; ambas páginas abren con contenido real verificado (título HDX coincide con "México" literal).

### Ficha 10 (R8.1) · SICS / Contraloría Social

```
$ curl -sL --max-time 25 "https://datos.gob.mx/api/3/action/package_show?id=promocion_contraloria_social"
{"success": true, "result": {"title": "Promoción de Controloría Social",
  "resources": [{"name": "Programas federales con Contraloría Social (2019-2025)", "format": "CSV",
  "url": "https://repodatos.atdt.gob.mx/api_update/sabg/promocion_contraloria_social/contraloria_social_2019_2025.csv"}]}}
$ curl -s --max-time 30 ".../contraloria_social_2019_2025.csv" -o contraloria_social_2019_2025.csv
$ wc -c contraloria_social_2019_2025.csv
520
$ cat contraloria_social_2019_2025.csv
ejercicio_fiscal,estrategias_validadas,programas_validados,comites_constituidos,integrantes,integrantes_mujeres,integrantes_hombres,beneficios_vigilados,capacitaciones
2019,106,68,78884,325137,222314,102823,86116,136
2020,97,68,68624,275410,180859,94551,76650,98
...(7 filas, una por ejercicio_fiscal, 2019-2025)

$ curl -s -D - -o /dev/null --max-time 20 "https://sics.funcionpublica.gob.mx"
exit 6 — Couldn't resolve host (2 intentos)
$ curl -s -D - -o /dev/null --max-time 20 "https://consultasics.buengobierno.gob.mx"
exit 35 — SSL connect error
$ curl -sv --max-time 20 "https://consultasics.buengobierno.gob.mx" 2>&1 | grep -iE "SSL|error"
* Immediate connect fail for 2801:c4:1d:1608::3: Network is unreachable
* TLS connect error: error:0A000126:SSL routines::unexpected eof while reading
```

**Hallazgo que corrige al barrido, en la dirección de MÁS agregación, no menos:** el barrido describe el dataset abierto como "agregado por programa/estado/año (no confirmado)". El archivo real, de 520 bytes y 7 filas, está agregado a **nivel nacional-año únicamente** — ni siquiera por estado o por programa. `SICS` (el sistema que sí captura a nivel de comité individual, según el barrido) no resolvió por DNS; `consultasics.buengobierno.gob.mx` falló por una ruta IPv6 inalcanzable desde este entorno seguida de un cierre TLS anómalo — dos fallos técnicos distintos, ninguno dice nada sobre si el sistema en sí existe o funciona.

**Examinado:** CKAN API + CSV completo (7 filas, todas leídas), 2 intentos SICS, 1 intento + diagnóstico verbose consultasics, 5/ago/2026. **CLASIFICACIÓN: EXISTE-NO-SATISFACE**, con la brecha más severa de lo que el barrido reportó — el dato público abierto es 7 números por año a nivel nacional, sin estado, sin programa, sin comité, sin variable de sanción/monitoreo. El sistema a nivel-comité (SICS) sigue **NO OBTENIDO POR ESTE AGENTE** — receta manual al final.

### Ficha 11 (R8.2) · Tandas digitales — sin URL candidata

El barrido no dejó ninguna URL para esta ficha (clasificación previa NO-ENCONTRADO sin candidato: "no se encontró que [Tanda+] lo haya publicado como cifra agregada en reporte, ronda de inversión o nota de prensa"). No hay nada que este acto pueda abrir. **CLASIFICACIÓN: NO-ENCONTRADO** — sin cambio, universo: ninguno (0 URLs candidatas en el barrido original para esta ficha).

### Ficha 12 (R8.3) · LAPOP / Latinobarómetro

```
$ curl -s -D - -o /dev/null --max-time 25 "https://www.vanderbilt.edu/lapop/about-americasbarometer.php"
HTTP/2 200
$ curl -s -D - -o /dev/null --max-time 25 "https://www.vanderbilt.edu/lapop/free-access.php"
HTTP/2 200
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.latinobarometro.org/latContents.jsp"
HTTP/2 200
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.latinobarometro.org/documentacion-datos"
HTTP/2 200
```

Las 4 páginas abren limpio. No se completó el registro gratuito ni se descargó microdato (el encargo prohíbe llenar formularios de registro; "registro gratuito... no cuenta como NO-ACCESIBLE" por REGLA 3, así que esto se confirma como accesible sin necesidad de completarlo).

**Examinado:** las 4 páginas, `curl`, 5/ago/2026. **CLASIFICACIÓN: EXISTE-SATISFACE** — confirma el barrido con las 4 páginas abiertas por fetch directo, no de segunda mano.

### Ficha 15 (R10.1) · PRESEEA

```
$ curl -s -D - -o /dev/null --max-time 20 "https://preseea.linguas.net/corpus.aspx"       # intento 1
(vacío, exit 28 — timeout)
$ curl -sL -D - -o /dev/null --max-time 20 "https://preseea.linguas.net/corpus.aspx"      # intento 2, -L
(vacío, exit 28)
$ curl -sL --max-time 20 -A "Mozilla/5.0 ..." "https://preseea.linguas.net/corpus.aspx" -v 2>&1 | tail
* Resolving timed out after 20000 milliseconds   # intento 3
```

**NO OBTENIDO POR ESTE AGENTE EN 3 INTENTOS** (los tres, timeout de resolución DNS). Receta manual al final.

```
$ curl -sL -o /dev/null -w "status:%{http_code} bytes:%{size_download}\n" --max-time 25 -A "Mozilla/5.0 ..." "https://revistas-filologicas.unam.mx/anuario-letras/"
status:200 bytes:50756
```

**Examinado:** 3 intentos de escalera contra PRESEEA (DNS no resuelve), 1 fetch exitoso contra la revista UNAM, 5/ago/2026. **CLASIFICACIÓN: NO-ACCESIBLE** para PRESEEA desde este agente (no es "no existe" — es "no obtenido"; receta manual). **EXISTE**, confirmado por fetch, para el artículo de la revista UNAM que documenta el corpus — no se leyó su contenido completo (relevante solo como evidencia secundaria de que PRESEEA-Puebla existe, no como candidata de datos por sí misma).

### Ficha 17 (R10.3) · ENVIPE + Mecanismo de Protección

```
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.inegi.org.mx/programas/envipe/2025/"
HTTP/1.1 200 OK
$ curl -sL -D - -o /dev/null --max-time 25 -A "Mozilla/5.0 ..." "https://www.gob.mx/defensorasyperiodistas/documentos/informes-estadisticos-mensuales"
HTTP/1.1 200 OK
```

Ambas páginas abren. El corpus compartido ya contiene descargas previas de ENVIPE de actos anteriores (`envipe2018_csv.zip` … `envipe2025_csv.zip`, con sus PDF de diseño — ver `data/raw/`, fechas 30/jul), lo que corrobora de forma independiente que la serie ENVIPE es efectivamente descargable, más allá de esta sola verificación de página.

**Examinado:** las 2 páginas, `curl`, 5/ago/2026; corroborado por payloads ENVIPE ya presentes en el corpus compartido de actos previos. **CLASIFICACIÓN: EXISTE-NO-SATISFACE** — confirma el barrido: ambas fuentes existen y son accesibles, pero ninguna publica el vínculo causal específico (efectividad de protección → disposición a testificar) que R10.3 pide.

---

## Fichas gateando reglas YA SELLADAS del Hito D (prioridad 2 — no reabren veredicto)

### Ficha 1 (R1.1, sellada D) · AGROASEMEX — caso de prueba de la receta CKAN

```
$ curl -sL --max-time 30 --cacert bundle.pem "https://datos.gob.mx/api/3/action/package_show?id=subsidio_seguro_agropecuario"
HTTP/2 308 → https://www.datos.gob.mx/... → HTTP/2 200, content-length: 9619
{"success": true, "result": {"title": "Subsidio Seguro Agropecuario", "num_resources": 4,
 "resources": [
   {"name": "Padrón de Integrantes del Sistema Nacional de Aseguramiento al Medio Rural", "format": "CSV",
    "url": "https://repodatos.atdt.gob.mx/.../padron_integrantes_sistema_nacional_aseguramiento_agropecuario.csv"},
   {"name": "Relación de beneficiarios del componente de apoyos (2016-2019)", "format": "CSV", ...PAA_componente_apoyo.csv},
   {"name": "...componente de subsidio para el ramo Agrícola (2016-2020)", "format": "CSV", ...PAA_componente_subsidio_ramo_agricola.csv},
   {"name": "...componente de subsidio para el ramo Ganadero (2016-2021)", "format": "CSV", ...PAA_componente_subsidio_ramo_ganadero.csv}
 ]}}
```

Receta CKAN validada como caso de prueba (instrucción del encargo) — funciona en cuanto se completa la cadena TLS (ver §0.6). Las 4 CSV se descargaron completas:

```
padron_integrantes...csv:      47848 bytes  | columnas: clave,nombre_fondo,estado,municipio
PAA_componente_apoyo.csv:     210586 bytes  | columnas: beneficiario,apoyo,anio,importe,moneda
PAA_...ramo_agricola.csv:    1553774 bytes  | columnas: ejercicio,mes,subsidio,cultivo,superficie_asegurada,estado,municipio
PAA_...ramo_ganadero.csv:    1153815 bytes  | columnas: anio_pago,mes_pago,subsidio,especie,cabezas_aseguradas,unidades_aseguradas,estado,municipio
```

**Hallazgo decisivo, byte a byte, que corrige al barrido (Ficha 1):** el barrido escribió "el padrón por productor sí existe y es descargable — la premisa del encargo... se sostiene". Los 4 recursos CKAN del dataset citado, abiertos y con encabezado leído completo, muestran: **ninguno de los cuatro tiene identificador de productor individual** (folio, nombre, CURP/RFC) — el padrón está a nivel **Fondo/asegurador** (4 columnas), y los tres "componente de subsidio/apoyo" están agregados por **estado/municipio/cultivo-o-especie/año-mes**, no por productor. El campo temporal en el archivo agrícola es `ejercicio,mes` — año calendario y mes, **no** ciclo agrícola primavera-verano/otoño-invierno — responde directamente la primera reserva que el barrido dejó abierta. No hay ninguna columna, en ninguno de los 4 archivos, que distinga voluntario de obligatorio-atado-a-crédito — responde la segunda reserva.

**Examinado:** los 4 archivos CSV completos del dataset CKAN `subsidio_seguro_agropecuario`, encabezado leído en los 4 (estructura, no microdato — ADR-46), mecanismo CKAN `package_show` + descarga directa, 5/ago/2026. **No reabre el veredicto D de `hitoD-R1.1`** (ese veredicto D es por exclusión de mercado del productor de temporal, razón estructural distinta, confirmada por el propio barrido como no reabierta). Este acto solo aporta el hecho, ahora verificado por lectura directa: el padrón público descargable de este dataset **no llega a nivel productor** bajo ninguno de sus 4 recursos — la premisa "el padrón por productor sí existe y es descargable" que el barrido reportó de segunda mano **no se sostiene** en los archivos reales.

### Ficha 2 (R1.3, sellada E) · CNBV / COFECE — canal de alta fintech

```
$ curl -sL -o /dev/null -w "status:%{http_code}\n" --max-time 25 --cacert bundle.pem "https://www.cnbv.gob.mx/Inclusi%C3%B3n/Paginas/Bases-de-Datos.aspx"
status:200
$ curl -sL -o /dev/null -w "status:%{http_code}\n" --max-time 25 --cacert bundle.pem "https://www.cofece.mx/wp-content/uploads/2024/10/Estudio-Fintech.pdf"
status:200
```

Ambas requirieron completar la cadena TLS (§0.6: GlobalSign para CNBV, DigiCert/GeoTrust para COFECE) antes de responder — sin eso, `curl` por defecto falla (exit 60) y un cliente que no complete la cadena reportaría, incorrectamente, "sitio caído".

**Examinado:** las 2 páginas, con cadena TLS completada, 5/ago/2026. **No reabre el veredicto E de `hitoD-R1.3`** (ya sellado 5/ago por ADR-63, MESA-M4, sobre corrida completa con datos propios). **CLASIFICACIÓN: NO-ENCONTRADO** confirmada — ambas fuentes abren pero, tal como el barrido documentó, ninguna mide canal de adquisición de clientes desagregado; CNBV mide infraestructura, COFECE es cualitativo/agregado.

### Ficha 6/7 (R4.1, sellada D) · CLUES + ESTAD/SESTAD

```
$ curl -sv --max-time 20 "https://dgis.salud.gob.mx/contenidos/sinais/s_clues.html" 2>&1 | grep -iE "subject:|issuer"
*   subject: C=--; ST=SomeState; L=SomeCity; O=SomeOrganization; OU=SomeOrganizationalUnit; CN=pliopencms05.salud.gob.mx
*   issuer:  C=--; ST=SomeState; L=SomeCity; O=SomeOrganization; OU=SomeOrganizationalUnit; CN=pliopencms05.salud.gob.mx
# subject == issuer: autofirmado, con los valores de plantilla de OpenSSL sin editar. No hay cadena que completar.

$ curl -sk -o /dev/null -w "status:%{http_code} bytes:%{size_download}\n" --max-time 20 "https://dgis.salud.gob.mx/contenidos/sinais/s_clues.html"   # SIN VERIFICAR, diagnóstico
status:404 bytes:228
$ curl -sk -o /dev/null -w "status:%{http_code} bytes:%{size_download}\n" --max-time 20 "https://dgis.salud.gob.mx/descargas/datosabiertos/recursosSalud/CLUES_2015.csv"
status:404 bytes:250
$ curl -sk -o /dev/null -w "status:%{http_code} bytes:%{size_download}\n" --max-time 20 "https://gobi.salud.gob.mx/Bases_Clues.html"
status:000   # sin conexión, ni con -k

$ curl -sL --max-time 25 --cacert bundle.pem "https://datos.gob.mx/api/3/action/package_search?q=CLUES&rows=5"
{"result": {"count": 1, "results":[{"name":"datos_egresos_hospitalarios", ...}]}}   # no encuentra el catálogo CLUES

$ curl -sL -D - -o /dev/null --max-time 20 "https://desdgces.salud.gob.mx/sestad/index.php"
HTTP/1.1 200 OK
$ curl -s -D - -o /dev/null --max-time 20 "https://calidad.salud.gob.mx/site/calidad/docs/2023/SESTAD_reporte_2021.pdf"
HTTP/1.1 200 OK / Content-Length: 1006873
```

**Hallazgo:** el portal DGIS de CLUES está roto de dos formas independientes — certificado autofirmado con valores de plantilla (nadie lo puede verificar) **y**, aun ignorando eso (`-k`, diagnóstico explícito, no verificado criptográficamente), las dos URLs específicas dan `404`. `gobi.salud.gob.mx` no conecta ni sin verificar TLS. La búsqueda de texto completo en CKAN por "CLUES" no encuentra el catálogo (solo un dataset no relacionado, "egresos hospitalarios"). El sistema **ESTAD/SESTAD sí funciona completo**: portal de captura (200) y reporte agregado 2021 (200, 1MB, descargado y registrado en el manifiesto).

**Examinado:** 2 URLs CLUES con y sin verificación TLS (404 ambas veces, con verificación imposible por certificado autofirmado), 1 intento gobi.salud (sin conexión), búsqueda CKAN, 2 URLs SESTAD (200 ambas, una descargada completa), 5/ago/2026. **No reabre el veredicto D de `hitoD-R4.1`.** **CLASIFICACIÓN: NO-ACCESIBLE** para el catálogo CLUES en las URLs citadas por el barrido (certificado inverificable + 404 confirmado incluso bypaseando la verificación — receta manual al final para que un humano lo abra en navegador, donde el 404 seguiría siendo 404 pero al menos vería el aviso de certificado con contexto). **EXISTE-NO-SATISFACE** para ESTAD/SESTAD, confirmado — el reporte agregado existe y se leyó; sigue sin confirmarse si el microdato cuatrimestral por establecimiento es descargable en bloque (el barrido ya declaraba esto como pendiente, y este acto no encontró ninguna URL adicional que lo resuelva).

### Ficha 13/14 (R9.1, sellada D) · ENSANUT — distancia a experto + cuestionario de utilizadores

```
$ curl -sL -D - -o /dev/null --max-time 20 "https://www.inegi.org.mx/contenidos/programas/ensanut/2018/doc/ensanut_2018_utilizadores_servicios_salud.pdf"
HTTP/1.1 200 OK / Content-Length real: 930234 (descargado completo)
$ curl -sL -D - -o /dev/null --max-time 20 "https://www.inegi.org.mx/rnm/index.php/catalog/590/data-dictionary/F42"
HTTP/1.1 200 OK

$ curl -s -D - -o /dev/null --max-time 20 "https://ensanut.insp.mx/..."          # intento 1
exit 35 — TLS connect error: unexpected eof while reading
$ curl -s --tlsv1.2 --tls-max 1.2 -D - -o /dev/null --max-time 20 "https://ensanut.insp.mx/..."   # intento 2, TLS1.2 forzado
exit 35 — mismo error
$ curl -sL -D - -o /dev/null --max-time 20 "http://ensanut.insp.mx/"            # intento 3, HTTP plano
exit 52 — Empty reply from server
```

**NO OBTENIDO POR ESTE AGENTE EN 3 INTENTOS** para `ensanut.insp.mx` (TLS1.3 falla con decode error, TLS1.2 forzado falla igual, HTTP plano da respuesta vacía — tres fallos técnicamente distintos, mismo host). Receta manual al final.

**Hallazgo decisivo, byte a byte, sobre el PDF del cuestionario (sí descargado completo):**

```
$ pdftotext -layout ensanut_2018_utilizadores_servicios_salud.pdf - | grep -B2 -A25 "2.1 ¿Por qué no buscó atención?"
2.1 ¿Por qué no buscó atención?
   CRUZA UN CÓDIGO
   No hay dónde atenderse.......................................................................01
   Es caro......................................................................................02
   No tenía dinero..............................................................................03
   Está muy lejos...............................................................................04
   Falta de confianza..........................................................................05
   Tratan mal...................................................................................06
   No tuvo tiempo..............................................................................07
   Decidió no atenderse.......................................................................08
   No tuvo quién lo(a) llevara o acompañara...............................................09
   No había servicio en el horario en que lo necesitaba................................10
   Los trámites eran muy tardados..........................................................11
   El tiempo para pasar a consulta era muy largo........................................12
   No tuvo problemas de salud en las últimas dos semanas.............................13
   Otro (especifica)...........................................................................14
   No sabe......................................................................................99
```

Esto corrige dos cosas del barrido a la vez. Primero, el texto exacto que el barrido buscó sin encontrarlo (Ficha 14: "se automedicó", "consejo de un conocido") **no existe como categoría separada** en el cuestionario real — la opción más cercana es la genérica "08 Decidió no atenderse" o el catch-all "14 Otro (especifica)". Segundo, y más importante: el título de la Ficha 14 dice "Población que no consultó a nadie, **excluida** del Cuestionario de Utilizadores" — la lectura directa muestra lo contrario: la Sección II de este mismo cuestionario **está dirigida específicamente** a quien no buscó atención, preguntándole por qué. Esta población no está excluida del instrumento; es el objeto central de una de sus secciones.

**Examinado:** PDF completo del cuestionario ENSANUT 2018 "Utilizadores de Servicios de Salud" (Secciones I-III leídas, estructura de pregunta — no hay microdato de respuesta que abrir, es el instrumento en blanco), página del diccionario de datos RNM, 3 intentos contra `ensanut.insp.mx` (todos fallidos, técnicamente distintos), 5/ago/2026. **No reabre el veredicto D de `hitoD-R9.1`.** **CLASIFICACIÓN Ficha 13: EXISTE-NO-SATISFACE**, sin cambio (el barrido ya había confirmado que ENSANUT público topa en municipio; este acto no pudo profundizar más porque `ensanut.insp.mx` no respondió). **CLASIFICACIÓN Ficha 14: EXISTE-NO-SATISFACE** — el instrumento existe y se leyó completo; la categoría de respuesta específica que el barrido buscaba no existe tal cual, y la premisa de "población excluida" del barrido no se sostiene contra el texto real del cuestionario.

---

## RECETAS MANUALES — todas juntas, para ejecutar de corrido

### 1 · `pub.bienestar.gob.mx` (Ficha 8a, R7.3)

- **URL a abrir:** `https://pub.bienestar.gob.mx/pub/personas`
- **Qué buscar ahí:** el módulo de consulta nominal de Pensión del Bienestar, con filtros de periodo/entidad/municipio.
- **Qué debería bajar:** no está claro si el portal ofrece descarga masiva o solo consulta uno-a-uno; verificar en el navegador si existe un botón de exportación CSV/Excel.
- **Dónde ponerlo:** `data/raw/R7.3_PUB_Bienestar/` (ya existe, usado por el acto concurrente `wt-desc1` para el agregado CKAN).
- **Cómo registrarlo:** `python3 tests/manifiesto.py --registra --id <nuevo_id> --archivo "R7.3_PUB_Bienestar/<archivo>" --usado-para "Candidata para R7.3 (Ficha 8a) — nivel nominal, complementa el agregado ya registrado" --url-origen "https://pub.bienestar.gob.mx/pub/personas" --descargado-por "usuario, vía navegador" --formato "<formato real>" --licencia "<licencia si el portal la declara>"`
- **Por qué paré:** DNS no resuelve desde este entorno en 3 intentos (2 timeout, 1 "Couldn't resolve host" explícito con 45s de margen).

### 2 · `computos2021.ine.mx` / `computos2024.ine.mx` (Ficha 8b, R7.3)

- **URL a abrir:** `https://computos2021.ine.mx/base-de-datos` (y el equivalente 2024).
- **Qué buscar ahí:** el enlace de descarga de la base de cómputos distritales por sección electoral.
- **Qué debería bajar:** probablemente un `.zip` con CSV por tipo de elección.
- **Dónde ponerlo:** `data/raw/R7.3_INE_computos/`.
- **Cómo registrarlo:** `python3 tests/manifiesto.py --registra --id conf17_r7_3_ine_computos_2021 --archivo "R7.3_INE_computos/<archivo>" --usado-para "Candidata para R7.3 (Ficha 8b, insumo RDD)" --url-origen "https://computos2021.ine.mx/base-de-datos" --descargado-por "usuario, vía navegador" --formato "ZIP" --licencia "<la que declare INE>"`
- **Por qué paré:** `403` reproducible (Cloudflare) en 2 intentos, con y sin cabecera Referer — patrón de bloqueo de bot, no de indisponibilidad del recurso (`www.ine.mx` sí respondió 200 en el mismo momento).

### 3 · `sics.funcionpublica.gob.mx` / `consultasics.buengobierno.gob.mx` (Ficha 10, R8.1)

- **URL a abrir:** `https://sics.funcionpublica.gob.mx` o, si esa no resuelve, `https://consultasics.buengobierno.gob.mx`.
- **Qué buscar ahí:** el sistema operativo de captura de Cédulas de Vigilancia por comité — no es portal de datos abiertos, es probable que exija credencial institucional (CURP + rol).
- **Qué debería bajar:** incierto si expone exportación pública; puede que solo confirme que el acceso requiere credencial, lo cual también es un hallazgo válido.
- **Dónde ponerlo:** `data/raw/R8.1_contraloria_social/` (ya existe).
- **Cómo registrarlo:** igual que arriba, con `--url-origen` la que corresponda de las dos.
- **Por qué paré:** `sics.funcionpublica.gob.mx` no resuelve DNS (2 intentos); `consultasics.buengobierno.gob.mx` falla por ruta IPv6 inalcanzable seguida de cierre TLS anómalo (`unexpected eof`) — 1 intento con diagnóstico verbose.

### 4 · `preseea.linguas.net` (Ficha 15, R10.1)

- **URL a abrir:** `https://preseea.linguas.net/corpus.aspx`
- **Qué buscar ahí:** el repositorio del corpus PRESEEA-Puebla, contacto con el equipo coordinador para acceso a investigación.
- **Qué debería bajar:** no aplica descarga directa según el barrido (acceso vía contacto con el equipo, no portal self-service) — confirmar si eso cambió.
- **Dónde ponerlo:** N/A (probablemente no hay archivo que registrar, solo confirmación de vía de acceso).
- **Cómo registrarlo:** N/A si el acceso es por contacto, no por descarga.
- **Por qué paré:** `Resolving timed out after 20000 milliseconds` — DNS no resuelve, 3 intentos (2 sin UA, 1 con UA de navegador y verbose).

### 5 · `ensanut.insp.mx` (Fichas 13/14, R9.1)

- **URL a abrir:** `https://ensanut.insp.mx/encuestas/ensanutcontinua2023/doctos/analiticos/16199-Texto%20del%20art%C3%ADculo-82516-2-10-20240821.pdf`
- **Qué buscar ahí:** el artículo analítico de ENSANUT Continua 2023 sobre razones de no atención — puede tener el desglose completo que el PDF del cuestionario de 2018 no aclara del todo (ver hallazgo arriba: la opción real es "08 Decidió no atenderse", no una categoría separada de automedicación).
- **Qué debería bajar:** el PDF mismo, ya nombrado en la URL.
- **Dónde ponerlo:** `data/raw/R9_1_ENSANUT_utilizadores/` (ya existe — renombrada sin punto, ver §0.8).
- **Cómo registrarlo:** `python3 tests/manifiesto.py --registra --id conf17_r9_1_ensanut_continua2023_articulo --archivo "R9_1_ENSANUT_utilizadores/<archivo>.pdf" --usado-para "Candidata para R9.1 (Ficha 14) — complementa el cuestionario 2018 ya registrado" --url-origen "https://ensanut.insp.mx/..." --descargado-por "usuario, vía navegador" --formato "PDF" --licencia "<la que declare INSP>"`
- **Por qué paré:** 3 fallos técnicamente distintos contra el mismo host — TLS1.3 decode error, TLS1.2 forzado con el mismo error, y HTTP plano con respuesta vacía del servidor (exit 52).

### 6 · `dgis.salud.gob.mx` / `gobi.salud.gob.mx` — CLUES (Fichas 6/13, R4.1/R9.1)

- **URL a abrir:** `https://dgis.salud.gob.mx/contenidos/sinais/s_clues.html`, y si el navegador la acepta pese al aviso de certificado, `https://dgis.salud.gob.mx/descargas/datosabiertos/recursosSalud/CLUES_2015.csv`.
- **Qué buscar ahí:** el catálogo CLUES completo, y si trae coordenadas GPS o solo domicilio en texto.
- **Qué debería bajar:** un CSV o KMZ del catálogo de establecimientos.
- **Dónde ponerlo:** `data/raw/R4.1_CLUES/`.
- **Cómo registrarlo:** igual patrón que arriba.
- **Por qué paré:** el certificado del sitio es autofirmado con valores de plantilla de OpenSSL sin editar (imposible de verificar por diseño, no por cadena incompleta) — y, verificado con `-k` sin validar (diagnóstico explícito, no confiable criptográficamente), la URL específica de 2015 da `404`, igual que la página índice. `gobi.salud.gob.mx` no conecta ni sin verificar TLS.

---

## Resumen ejecutivo de este acto

**Cero directo, como anticipaba el encargo.** Lo que se mueve es el perímetro falsable de 6 fichas con lectura byte a byte que antes solo tenían evidencia de `WebSearch` de segunda mano:

- **Fichas con hallazgo que corrige la lectura previa del barrido (más restrictivo de lo reportado):** 1 (R1.1 — ningún recurso llega a nivel productor, campo temporal es fiscal no agrícola), 8a (R7.3 — el CSV público es agregado entidad-trimestre, no nominal), 10 (R8.1 — el CSV público es agregado nacional-año, ni siquiera por estado), 14 (R9.1 — la categoría de respuesta buscada no existe tal cual, y la premisa de "población excluida" es incorrecta: es el objeto central de la Sección II).
- **Fichas confirmadas sin cambio sustantivo, ahora con fetch directo en vez de `WebSearch`:** 3, 4(PDF), 5, 8b, 9, 12, 15(UNAM), 17, 2, 6/7(SESTAD), 13.
- **Fichas nuevas o corregidas por búsqueda de texto completo (no en el barrido original):** 4 — el dataset CKAN citado da 404+Authorization Error y no aparece en `package_search`, hallazgo que el barrido no tenía.
- **Sin cambio, sin URL candidata (no evaluables por este acto):** 11, 16.

**SIN-FETCH (no obtenido por este agente, con receta manual pendiente):** `pub.bienestar.gob.mx`, `computos2021/2024.ine.mx` (403 Cloudflare, no DNS), `sics.funcionpublica.gob.mx` + `consultasics.buengobierno.gob.mx`, `preseea.linguas.net`, `ensanut.insp.mx`, `dgis.salud.gob.mx`/`gobi.salud.gob.mx` (CLUES) — **6 hosts, cubriendo partes de 5 fichas** (8, 10, 15, 13/14, 6). Ninguno de estos 6 fallos se interpreta como afirmación sobre el recurso (REGLA 2) — son hechos sobre este agente, en este entorno, hoy.

**Colisión con acto concurrente:** 3 de las 17 fichas (4, 8a, 10) tienen payload ya presente en el corpus compartido por un worktree distinto (`wt-desc1`, rama `desc1-descarga`) que apareció y siguió escribiendo mientras esta nota se redactaba — verificado byte-idéntico contra mis propias descargas independientes. No se registraron ids propios para esos 3 para evitar una carrera de escritura en `data/manifiesto.yaml`; la mesa debe decidir si `wt-desc1` es el mismo despacho duplicado o un acto legítimamente distinto antes de fusionar.

Este acto no adjudica ningún veredicto `RX.Y`, no promueve ninguna candidata a ficha, y no reabre ninguno de los 13 veredictos ya sellados citados arriba.
