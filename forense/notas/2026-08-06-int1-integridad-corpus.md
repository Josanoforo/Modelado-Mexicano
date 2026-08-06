# ENCARGO INT-1 — Barrido de integridad del corpus (2026-08-06)

Redactado contra `origin/main` = `21cf521` (PR #144, fusión de
`tc1-corpus-010528-2` — el barrido de firma EOCD que motiva este acto).

## Arranque

### 1 · Repo y worktree

Clon: `/home/pc0/Modelado-Mexicano` (localizado por `git -C . rev-parse
--show-toplevel`, no supuesto). `git fetch --all --prune` confirmó
`origin/main` en `cbf0fb0` (PR #145, MAP-1b) al momento de arrancar.

Worktree nuevo, sufijo por timestamp: `/home/pc0/wt-int1-1786003491`, rama
`int1-integridad-1786003491`, creado desde `origin/main`. `git worktree add`
emitió dos avisos `error: could not write config file .git/config: Device or
resource busy` (exit code 0 — el worktree se registró correctamente pese al
aviso). Causa observada, no solo supuesta: `git worktree list` corrido
segundos después mostró que `/home/pc0/wt-tc1-010528-2` había avanzado de
`b8f2c5a` a `00f51ff` entre mi primer y segundo listado — hay otra sesión
escribiendo en el mismo `.git` compartido en este momento, tal como
advertía el encargo.

```
git status   -> "On branch int1-integridad-1786003491, nothing to commit, working tree clean"
git log -1   -> cbf0fb0 Merge pull request #145 from Josanoforo/map1b-censo-1786000741
git worktree list -> incluye /home/pc0/wt-int1-1786003491  cbf0fb0 [int1-integridad-1786003491]
```

### 2 · SHA

Base declarada por el encargo: `21cf521`. `origin/main` había avanzado a
`cbf0fb0` — un solo merge de diferencia (PR #145, MAP-1b),
`git merge-base --is-ancestor 21cf521 origin/main` confirma que `21cf521` es
ancestro directo (main solo avanzó, no hubo reescritura). No es PARO;
worktree ya construido sobre `origin/main` actual, sin necesidad de rebase.

### 3 · Las tres raíces

Worktree recién creado, antes de configurar nada:

```
$ ls -ld data/raw && readlink -f data/raw
ls: cannot access 'data/raw': No such file or directory
/home/pc0/wt-int1-1786003491/data/raw          # readlink -f resuelve la ruta teórica; no existe

$ cat data/raices.local.yaml
cat: data/raices.local.yaml: No such file or directory   # gitignorado, esperado en worktree fresco

$ ls -ld "/mnt/c/Users/PC0/Descargas MX"
drwxrwxrwx 1 pc0 pc0 4096 Aug  5 18:09 /mnt/c/Users/PC0/Descargas MX
```

Dos de tres no resolvían. Antes de declarar PARO, inspeccioné los worktrees
que `git worktree list` ya había enumerado: `data/raw` es symlink a
`/home/pc0/mm-corpus/raw` en **todos** los worktrees configurados
(`Modelado-Mexicano`, `mm-p-lapop-microdato`, `wt-conf17`, `wt-desc1`,
`wt-map1b-censo-1786000741`, `wt-ver1` — mismo destino, 23 bytes, en cada
uno), y `data/raices.local.yaml` solo existe en dos: el worktree principal
(`/home/pc0/Modelado-Mexicano`, 31/jul) y `wt-map1b-censo-1786000741`
(6/ago) — `diff` entre ambos: idénticos. Repliqué la convención ya
establecida por el resto de la máquina, no inventada aquí:

```
cp /home/pc0/Modelado-Mexicano/data/raices.local.yaml data/raices.local.yaml
ln -s /home/pc0/mm-corpus/raw data/raw
```

Copiado de `/home/pc0/Modelado-Mexicano` (el worktree principal, la fuente
más antigua, no la específica de otro encargo). Tras esto, las tres
resuelven:

```
data/raw -> /home/pc0/mm-corpus/raw   (destino existe, 72 entradas)
data_raw: /home/pc0/mm-corpus/raw          # documentación; el script resuelve data_raw por código, no lee esta línea
descargas_mx: /mnt/c/Users/PC0/Descargas MX
downloads: /mnt/c/Users/PC0/Downloads
/mnt/c/Users/PC0/Descargas MX  -> existe
/mnt/c/Users/PC0/Downloads     -> existe
```

Ninguna raíz quedó sin resolver. No PARO. (Verifiqué en `tests/manifiesto.py`
que `resolver_raiz()`/`raices_configuradas()` usan exactamente este
mecanismo — `data_raw` se resuelve por código vía `rutas()`, todo lo demás
por `data/raices.local.yaml` — antes de confiar en que la copia bastaba.)

### 4 · Entorno — firma de tres partes

```
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable
$ ls data/raw/ | head -1
BD_ENCUCI2020_dbf.zip
$ df -h /mnt/c | tail -1
C:\             931G  665G  266G  72% /mnt/c
$ python3 --version
Python 3.14.4
```

Sin variable de nube, corpus montado con contenido real, `/mnt/c` presente
(WSL2) — `uname -a` confirma `Linux FF-5563 6.6.87.2-microsoft-standard-WSL2`.
Ubuntu con las tres raíces montadas, tal como el encargo exige para abrir
microdato.

### 5 · Espejo

Ninguna cifra de este documento sale de un espejo. Todo lo que sigue se
deriva de comandos corridos contra este worktree (`origin/main` recién
fetcheado), con el comando citado junto al número.

### Aparte — dos verificaciones de premisa antes de barrer

El propio encargo cita **"regla A.1 de v2.5"**: que `--verifica` con varios
`--id` en la misma invocación "solo verifica el último, sin aviso", y por
eso exige una invocación por id. Antes de ejecutar así 467 veces, leí
`tests/manifiesto.py` (líneas 258–272 y 341–353): el defecto es real y está
documentado — pero fue **corregido el 2026-08-04** (ENCARGO
MT-mantenimiento, sellado en `gobernanza` ADR-62, línea 126 de
`forense/hallazgos.md`). El código actual acumula `--id` (`action='append'`)
y `--verifica` corre sobre **todos** los ids dados, con error explícito y
ruidoso — no silencio — si alguno no existe. `instrucciones-proyecto-v2_6.md`
(el canon vigente, que conserva v2.5 verbatim salvo lo marcado `[NUEVO
v2.6]`) todavía trae el texto de A.1 sin actualizar tras esa corrección: la
regla-como-procedimiento ("una invocación por id") sigue siendo prudente
como disciplina — la seguí, sin excepción — pero su premisa citada ("sin
aviso") ya no describe el código de hoy. Lo dejo escrito porque es
exactamente la clase de defecto que este acto existe para no repetir:
una afirmación del corpus/canon sobre sí mismo, no verificada contra el
archivo antes de citarla.

Segunda verificación: el encargo advierte que citar el nombre suelto
"raices.local.yaml" en backticks puede disparar T03 (referencias
colgantes) en CI, y pide verificar el patrón antes de
escribir. Leí `tests/check.py:200`
(`` `([A-Za-z0-9_\-áéíóúñÁÉÍÓÚÑ.]+\.(?:md|yaml))` `` — la clase de
caracteres no admite `/`) y el commit `183b7af` de MAP-1b, que ya reparó
exactamente este caso en su propia nota. Citar el nombre con su ruta
completa — `data/raices.local.yaml` — no coincide con el patrón en absoluto
(la barra rompe el match); en este documento se cita siempre así, nunca como
nombre suelto.

## PASO 0 — Universo declarado antes de barrer

```
$ grep -c '^- id:' data/manifiesto.yaml
471
$ grep -cE 'sha256: *[a-f0-9]{64}' data/manifiesto.yaml
467
```

471 entradas totales, **467 con payload** (confirmado también por el parseo
YAML vía `tests/manifiesto.py`'s propio `leer_manifiesto()` — mismo
conteo, dos mecanismos). Clasificación por familia, derivada de la extensión
declarada en `archivo`:

| familia | extensiones observadas | n | chequeo estructural |
|---|---|---|---|
| zip | `.zip` (317), `.xlsx` (38), `.docx` (1) | **356** | `testzip()` |
| pdf | `.pdf` | **93** | cabecera + cola |
| otros | `.csv` (6), `.xml` (1), `.xls` (7), `.html` (4) | **18** | ninguno — SOLO hash |

356 + 93 + 18 = 467. ✓

**Dos extensiones no estaban en la lista ilustrativa del encargo** para
"otros" (`.csv .dta .sav .dbf .xml .txt`): `.xls` (7) y `.html` (4).
Verificado antes de clasificar, no asumido:

- `.xls` (legado, no `.xlsx`): los 7 archivos en disco tienen cabecera
  `d0cf11e0a1b11ae1` — firma OLE2/Compound File Binary Format, **no** ZIP
  (`50 4b…`). Meterlos en familia-zip habría producido 7 `BadZipFile`
  garantizados, contaminando la clase peligrosa con falsos positivos.
  Van a "otros" — SOLO hash, sin chequeo estructural inventado para la
  ocasión (el encargo no autoriza un cuarto procedimiento de verificación,
  p.ej. cabecera OLE2).
- `.html` (4, todas `enut20{09,14,19,24}_diccionario_variables`):
  confirmado con `head -c 60`, las 4 abren con `<!DOCTYPE html><html>…` —
  HTML genuino. Van a "otros" por la misma razón: no es zip, no es PDF.

Esta tabla dice de antemano cuánto del corpus este acto NO puede verificar
estructuralmente: **18 de 467 (3.9%)**, antes de correr un solo chequeo.

## PASO 1 — Los tres chequeos, por payload

Metodología: script propio (fuera del repo, en scratchpad de sesión) que
importa `tests/manifiesto.py` como módulo para reutilizar exactamente su
`resolver_raiz()`/`raices_configuradas()` en C-EXISTE (no reimplementa la
lógica de raíces), corre C-HASH como `subprocess` — **una invocación
independiente de `python3 tests/manifiesto.py --verifica --id <id>` por
cada una de las 467 entradas**, tal como exige la disciplina de A.1 — y
corre C-ESTRUCTURA in-process (`zipfile.testzip()` / cabecera-cola PDF).
Paralelizado con `ThreadPoolExecutor(8)` (cada subprocess bloquea su propio
hilo; el hash y el `testzip()` son el mismo trabajo de fondo esté o no
paralelizado). Orden de salida = orden del manifiesto.

```
467/467 en 101.3s
LENTOS (>15s): endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf (declarado 2 895 872 B, 15.6s)
               endireh_2011_bd_endireh_2011_dta (declarado 30 383 196 B, 20.23s)
```

El primero es lento porque el archivo real pesa 102 MB, no 2.9 MB (ver PASO
2). El segundo (`endireh_2011_bd_endireh_2011_dta`) resultó **COINCIDE +
ÍNTEGRO** limpio — tamaño real idéntico al declarado (30 383 196 B), sin
discrepancia; la lentitud fue variación de I/O bajo concurrencia, no señal
de nada. Ninguno se saltó.

**Política de salida cruda, declarada:** A.1 pide pegar la salida cruda de
cada invocación. A escala de 467 (cada una incluye una sección final de
~57 líneas listando "procedencia derivada" — idéntica en cada invocación,
del manifiesto completo, no específica del id pedido) eso son >25 000
líneas de relleno repetido sin valor forense por repetición. Se preserva
íntegra la línea específica del id (`id [raíz]: VEREDICTO -- detalle`) para
las 467 en el TSV/JSON de esta sesión, y se cita textual en este documento
para toda entrada fuera de COINCIDE+ÍNTEGRO/NO_EVALUADO — donde sí aporta.
Declarado aquí, no silencioso.

Distribución cruda (los tres chequeos, sin colapsar):

| | valor | n |
|---|---|---|
| C-EXISTE | EXISTE | 467 |
| | AUSENTE / RAÍZ-NO-RESUELTA | 0 / 0 |
| C-HASH | COINCIDE | 464 |
| | NO_COINCIDE | 3 |
| C-ESTRUCTURA | ÍNTEGRO | 442 |
| | NO_EVALUADO (familia otros) | 18 |
| | CORRUPTO | 2 |
| | ERROR (no evaluable, ver PASO 2) | 5 |

Por raíz, sin colapsar (data_raw incluye las 410 implícitas + 28
explícitas): `descargas_mx` 29/29 COINCIDE+ÍNTEGRO, cero anomalía;
`data_raw` 438 entradas, 435 COINCIDE (413 ÍNTEGRO + 18 NO_EVALUADO + 5
DEFLATE64-sin-verdicto) + 3 NO_COINCIDE. Ninguna anomalía vive en
`descargas_mx`.

Entregable: `data/integridad-corpus-2026-08-06.tsv`, 467 filas + cabecera,
columnas `id · raiz · archivo · familia · bytes_declarados · bytes_reales ·
C-EXISTE · C-HASH · C-ESTRUCTURA · miembro_corrupto · mtime_real`.

## PASO 2 — Clasificación, cada clase un hecho distinto

| clase | n |
|---|---|
| COINCIDE + ÍNTEGRO | **441** |
| COINCIDE + NO EVALUADO (familia otros) | **18** |
| **COINCIDE + CORRUPTO** (la clase peligrosa) | **0** |
| NO COINCIDE | **3** |
| AUSENTE | **0** |
| RAÍZ-NO-RESUELTA | **0** |
| *(fuera de las 6 — ver abajo)* COINCIDE + no evaluable por límite de herramienta | **5** |
| **total** | **467** |

**La clase peligrosa da cero.** Los dos únicos CORRUPTO de este barrido
están en la fila NO COINCIDE, no en COINCIDE — el hash ya delataba el
problema por su cuenta en ambos casos; ningún hash declarado sella hoy un
archivo estructuralmente corrupto como si fuera bueno. Esto es válido para
las 467 entradas examinadas; no es una afirmación sobre las 18+5 = 23 nunca
evaluadas estructuralmente (ver cierre).

### NO COINCIDE — 3 de 467, detalle completo

Las tres las escribió el **mismo commit**, `ae4910b` ("ENCARGO DESC-1:
descarga priorizada TRAMO A+B desde XML de canasta nacional",
2026-08-05 19:05:57 -0600) — único commit que toca cada id en
`data/manifiesto.yaml` (`git log -S"<id>" -- data/manifiesto.yaml`, una
coincidencia cada uno, no hubo re-registro posterior.

**Corroboración independiente:** `forense/notas/2026-08-06-map1b-censo-raices.md`
§B ("Colgadas") ya había encontrado estas mismas 3 entradas por un método
distinto (censo de sha256 en disco, cruzado contra el manifiesto — no
re-verificación directa) — mismos tres ids, mismos tamaños declarados y
reales, mismos mtimes, byte por byte. Dos actos independientes, dos
metodologías, mismo resultado. Lo que este acto añade y MAP-1b no midió:
la capa C-ESTRUCTURA (testzip/cabecera-cola) — MAP-1b no abrió estos
archivos, solo contó su sha256 y tamaño.

| id | bytes decl. | bytes real | C-ESTRUCTURA | mtime real | mtime vs. commit (19:05:57) |
|---|---|---|---|---|---|
| `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` | 2 895 872 | 102 349 631 | ÍNTEGRO | 18:45:47 | **anterior** (20 min antes) |
| `envipe_2023_bd_envipe_2023_dta` | 16 221 003 | 9 289 283 | CORRUPTO | 19:14:21 | **posterior** (8 min después) |
| `envipe_2023_bd_envipe_2023_sav` | 26 786 689 | 21 495 362 | CORRUPTO | 19:17:21 | **posterior** (12 min después) |

No se explica el mecanismo (mover/sobrescribir/re-descargar) — excede este
perímetro, tal como el encargo instruye. Se reporta solo la relación
temporal, y no es uniforme entre las tres: las dos ENVIPE repiten la firma
que MAP-1b ya había nombrado para ellas (mtime posterior al commit que las
registró); la de ENDIREH-2016 —la que el propio encargo cita como ejemplo
motivador— tiene mtime **anterior** al commit, la relación opuesta. Tres
hechos, no colapsados en uno.

**Triangulación, tercer método independiente.** `origin/main` avanzó durante
este acto (ver PASO 4) e incorporó PR #146,
`forense/notas/2026-08-06-verificacion-extraccion-crc-envipe2023.md` — una
verificación ad hoc, sin ENCARGO asignado, que llegó a los mismos dos
`envipe_2023` por un tercer camino distinto (barrido de firma EOCD —
`PK\x05\x06` en la cola — sobre los 317 zips declarados, más lectura binaria
de cabeceras locales `PK\x03\x04`: 4/6 y 5/6 miembros reconocibles en cada
archivo, cero central directory en ninguno). Tres métodos — censo de sha256
(MAP-1b), re-verificación por hash + `testzip()` (este acto), y barrido de
EOCD (esa nota) — coinciden exactamente en los mismos dos ids. Esa nota
declaraba inicialmente "ningún otro zip del corpus tiene este defecto" y lo
**retiró ella misma** (commit `00f51ff`) por exceder lo que su propio
barrido podía sostener (evaluó 301/317: 299 EOCD-presente + 2 EOCD-ausente,
más 16 sin archivo en *ese* worktree — una raíz sin montar allí, no un
hecho del corpus), remitiendo explícitamente a este acto para "la respuesta
real sobre integridad". Este barrido, con las tres raíces configuradas
(Arranque §3), no tuvo esos 16 sin resolver: los 467 con payload, EOCD
incluido implícitamente en `testzip()`, se evaluaron completos.

Caracterización observable (no mecanismo) de cada archivo, porque
"NO COINCIDE" por sí solo no dice qué hay ahí:

- **`endireh_2016…dbf`** — `zipfile.testzip()` no encuentra miembro dañado;
  `infolist()` muestra 25 miembros (`fd_endireh2016_dbf.pdf` + 24 tablas
  `TB_SEC_*.dbf`, fechas internas de 2017), consistente con un paquete
  ENDIREH real y completo, solo que mucho más grande que lo declarado en el
  manifiesto (35×).
- **`envipe_2023…dta.zip`** y **`…sav.zip`** — ambos abren con cabecera
  local PK válida y nombre de miembro legible (`THogar.dta` / `THogar.sav`
  respectivamente — `file(1)` los reconoce como "Zip archive data,
  compression method=deflate"), pero **ningún End-Of-Central-Directory** en
  los últimos 4096 bytes de ninguno de los dos (`xxd` + búsqueda de la firma
  `50 4b 05 06`, ausente en ambos) — consistente con truncamiento a mitad de
  flujo, no con un archivo distinto sustituido entero.

### COINCIDE + no evaluable por límite de herramienta — 5 de 467 (fuera de las 6 clases)

Las 5 son de la misma serie, `ennvih1_2002_{hogar,local}_*`. `C-HASH` =
COINCIDE en las cinco (el archivo no cambió respecto a lo declarado).
`zipfile.ZipFile(p).testzip()` falla con
`NotImplementedError: That compression method is not supported` — no
`BadZipFile`. Verificado antes de descartar como ruido: listar
`infolist()` (que solo lee el directorio central, sin descomprimir) muestra
que casi todos los miembros usan `compress_type=9` (**DEFLATE64/Enhanced
Deflate**; unos pocos, `compress_type=8`, deflate estándar, y los
directorios vacíos `compress_type=0`) — el módulo `zipfile` de Python
3.14.4 no decodifica DEFLATE64. Verifiqué si había una herramienta
alternativa en este entorno (`unzip`, `7z`/`7za`/`7zr`): ninguna está
instalada. No se inventó un cuarto procedimiento de verificación fuera de
lo que el encargo autoriza (`zipfile.testzip()` es el método especificado
para familia-zip) — se reporta el límite y se para, como el encargo permite
explícitamente ("si testzip() resulta impracticable... para, escríbelo").

Esto **no es** "NO EVALUADO" (esa etiqueta es la política de la familia
"otros", una decisión de diseño, no un fallo de herramienta sobre una
familia que sí tiene chequeo definido) ni "CORRUPTO" (nada indica daño; el
directorio central se lee sin error) ni "ÍNTEGRO" (el chequeo nunca corrió
hasta el final). Es una séptima clase que el PASO 2 del encargo no
anticipó, y no se fuerza dentro de las seis — mismo criterio que pide el
propio encargo para las seis.

| id | archivo | bytes declarados |
|---|---|---|
| `ennvih1_2002_hogar_cb` | `ennvih/ehh02cb_all.zip` | 2 195 863 |
| `ennvih1_2002_hogar_q` | `ennvih/ehh02q_all.zip` | 3 750 632 |
| `ennvih1_2002_local_dta` | `ennvih/eloc02dta_all.zip` | 1 591 239 |
| `ennvih1_2002_local_cb` | `ennvih/eloc02cb_all.zip` | 901 067 |
| `ennvih1_2002_local_q` | `ennvih/eloc02q_all.zip` | 5 995 112 |

### AUSENTE / RAÍZ-NO-RESUELTA

Cero en ambas clases. Nada que listar.

## PASO 3 — Cierre acotado

De **467** entradas con payload: **441** verificadas por hash y estructura
(COINCIDE+ÍNTEGRO), **18** por hash solamente (familia otros, sin chequeo
estructural posible), **5** con hash verificado pero estructura no
evaluable por límite de herramienta (compresión DEFLATE64, sin decodificador
disponible en este entorno), **3** con hash discordante (de las cuales 2
además CORRUPTO por estructura, 1 ÍNTEGRO), **0** ausentes, **0** con raíz
no resuelta.

Este barrido no detecta: corrupción dentro de las 18 entradas de familia
"otros" (nunca abiertas estructuralmente); corrupción dentro de los 5
archivos DEFLATE64 (ni confirmada ni descartada — el chequeo no terminó);
sustitución de un archivo por otro válido cuyo hash se haya registrado
después del cambio (invisible a C-HASH por diseño); ni ningún defecto en
las clases AUSENTE/RAÍZ-NO-RESUELTA, hoy vacías pero no verificadas contra
ningún universo futuro. La ausencia de más casos NO COINCIDE o CORRUPTO en
las 444 entradas evaluadas por completo (441 + 3) no es evidencia de que no
los haya en las 23 (18 + 5) nunca evaluadas estructuralmente.

**Recomendación, sin ejecutar ninguna de las tres:**

1. **Exigen re-descarga:** `envipe_2023_bd_envipe_2023_dta` y
   `envipe_2023_bd_envipe_2023_sav` — el contenido actual está truncado
   (sin EOCD), no es un archivo distinto válido; no hay nada que
   re-registrar porque no hay nada completo que hashear.
2. **Solo exigen decidir si re-registrar el hash** (el archivo en disco es
   estructuralmente válido y completo, decisión de la mesa, no de este
   acto): `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` — 102 MB,
   25 miembros íntegros, consistentes con un paquete ENDIREH real; si la
   mesa confirma que es el contenido correcto, el manifiesto necesita el
   hash/tamaño de ESTE archivo, no una re-descarga.
3. **Quedan sin decidir:** los 5 `ennvih1_2002_*` — hash coincide, pero
   ningún veredicto estructural es posible con las herramientas de este
   entorno; requieren una vía DEFLATE64-capaz (`unzip`, `7z`, o
   descompresión manual con otra librería) antes de poder cerrarse en
   cualquier dirección.

## Lo que este acto no hizo

No tocó `data/manifiesto.yaml` — ni una línea, ni para las 3 entradas
NO COINCIDE. No re-descargó nada. No movió, copió (salvo
`data/raices.local.yaml` a este worktree, gitignorado, no versionado),
renombró ni borró ningún
payload. No editó `tests/`. No decidió si los 3 NO COINCIDE se resuelven
por re-descarga o re-registro — eso lo declara la recomendación, no lo
ejecuta. No corrió `unzip`/`7z` porque ninguno está instalado en este
entorno — no se instaló nada para rodear esa ausencia.

## ADDENDUM — corrección post-PR: citas sueltas de "raices.local.yaml"

Con el PR #148 ya abierto, revisión externa (dos rondas de `grep`, la
segunda con un patrón más amplio que el propio patrón de T03) encontró
varias citas del nombre suelto "raices.local.yaml" entre backticks, sin la
ruta completa — el mismo defecto que este documento afirmaba haber
evitado, reintroducido en el propio texto que lo discute (incluyendo, en
un primer intento de arreglo, una marca `{cita-ilustrativa}` colocada en
la línea siguiente por el reflow del párrafo — inválida, porque
`l[mo.end():]` en `tests/check.py:204` opera por línea física, no por
párrafo).

Política final, más simple que ir marcando cada caso: toda mención
**ilustrativa** de "raices.local.yaml" o de cualquier otro nombre corto
que T03 pudiera leer como ruta (p. ej. "estado-programa-v1_9.md", citado
más abajo como ejemplo de otro archivo) va **sin backticks** — entre
comillas o sin marcado alguno — en vez de depender de una marca sensible
al ajuste de línea. Toda mención de un archivo **real** de este acto sigue
en backticks con su ruta completa (`data/raices.local.yaml`,
`data/manifiesto.yaml`, etc.), que no coincide con el patrón de T03 porque
la diagonal rompe la clase de caracteres del regex (verificado contra
`tests/check.py:200` antes de la primera corrección, arriba en el Arranque).

Verificado, no asumido: `data/raw` y `data/raices.local.yaml` movidos a la
vez (simulacro de checkout limpio real, sin ninguno de los dos presente),
`t03_dangling_refs()` llamado directamente — no el resumen truncado de la
terminal, que solo imprime 3 ejemplos por test — para inspeccionar los 29
WARN completos, sin filtrar. Cero mencionan este documento. Restaurados
ambos; `tests/check.py --baseline` vuelve a dar `18 FAIL · 95 WARN`, VERDE.

## PASO 4 — Suite y PR

Corrida por duplicado, tal como exige el encargo (PR #145 pasó verde en su
worktree y falló en CI por operar sobre un checkout sin corpus — no se
repite ese defecto aquí):

**1) Con el corpus montado** (`data/raw` symlink a `/home/pc0/mm-corpus/raw`,
como quedó en Arranque §3):

```
[ ok ]  T01 fuente única de verdad
[ ok ]  T02 duplicados nombre/contenido
...
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```
Exit code 0.

**2) Con `data/raw` desenlazado temporalmente** (`mv data/raw
data/raw.symlink.bak`, corrida, `mv data/raw.symlink.bak data/raw` para
restaurar — reversible, nunca se borró el symlink ni su destino):

```
[ ok ]  T01 fuente única de verdad
[ ok ]  T02 duplicados nombre/contenido
...
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```
Exit code 0. `diff` entre las dos salidas completas: **idénticas, byte a
byte**. Los dos archivos nuevos de este acto (la nota y el TSV) no dependen
del corpus montado para pasar T01-T20 — mismo resultado con y sin `data/raw`
enlazado.

`forense/hallazgos.md`: una línea añadida al final (append, `merge=union`
activo en `.gitattributes`).

## ACTUALIZACIÓN — `origin/main` avanzó durante este acto

Entre el arranque (`cbf0fb0`, PR #145) y este cierre, `origin/main` avanzó a
`168af29`: PR #146 (verificación ad hoc EOCD/envipe2023, citada arriba) y
PR #147 (MAP-1: corrección de `acron()` en `tests/catalogo.py`). Ninguno de
los dos toca `data/manifiesto.yaml` ni `tests/manifiesto.py`
(`git diff cbf0fb0..168af29 --stat` sobre ambos, vacío) — el barrido de
PASO 1 sigue vigente sin re-derivar. `git fetch && git merge origin/main`:
limpio, sin conflicto (`forense/hallazgos.md` se auto-fusionó por
`merge=union` — 136 entradas, la propia incluida, ninguna duplicada).
`tests/check.py --baseline` corrido una tercera vez, después del merge:
exit 0, `18 FAIL · 95 WARN`, VERDE — igual que las dos corridas de PASO 4.
