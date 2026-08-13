# ACTO CAPA3-RECONCILIA — Commit 1: especificación congelada, antes de abrir el TSV

**SHA de redacción del encargo:** `dcc4f6a` (`origin/main`, HEAD al momento de escribir — confirmado: es exactamente el commit sobre el que se abrió este worktree).
**Entorno:** CAJA con corpus (Ubuntu/WSL, worktree `~/mm-capa3-reconcilia`, `git worktree add ... origin/main` desde `/home/pc0/Modelado-Mexicano`).

## §1 · Arranque — verificación de entorno

`data/raices.local.yaml` es gitignorado y no se hereda al crear un worktree nuevo — se copió a mano desde `/home/pc0/Modelado-Mexicano/data/raices.local.yaml`:

```
$ test -f data/raices.local.yaml && grep -c "descargas_mx" data/raices.local.yaml
1
```

Defecto adicional encontrado y corregido, no declarado por el encargo: `data/raw` en el clon base es un symlink (`data/raw -> /home/pc0/mm-corpus/raw`) que **tampoco** se hereda — `data/raw/` está en `.gitignore` y el symlink no viaja con `git worktree add`. Sin él, `--verifica` sobre cualquier id anclado a la raíz `data_raw` (uno de los cuatro de este acto, ver abajo) da `AUSENTE` en vez de `COINCIDE`, que habría sido un falso positivo de "capa3 realmente ausente". Se recreó a mano:

```
$ ln -s /home/pc0/mm-corpus/raw data/raw
```

Con las dos correcciones, las dos verificaciones de arranque exigidas por el encargo:

```
$ python3 tests/manifiesto.py --verifica --id za6980_v2_0_0_dta
za6980_v2_0_0_dta [descargas_mx]: COINCIDE -- sha256 y tamaño (3144289 bytes) verificados contra data/manifiesto.yaml

$ python3 tests/manifiesto.py --verifica --id cses5_modulo5_2016_2021_csv
cses5_modulo5_2016_2021_csv [data_raw]: COINCIDE -- sha256 y tamaño (16604927 bytes) verificados contra data/manifiesto.yaml
```

Ambas `COINCIDE`. Entorno correcto, corpus montado, se procede.

## §2 · Las 19 filas — derivadas por `awk`, no por juicio

```
$ awk -F'\t' 'NR==1{next} $10=="SI" && $11!="EXISTE;COINCIDE;INTEGRO" {print}' data/curacion-registro/relaciones.tsv | wc -l
19
```

Distribución por fuente (columna `fuente_nombre`): ISSP 12 · CSES 5 · WVS 2 — coincide exacto con lo que el encargo declaró en §0.

| relacion_id | necesidad_id | fuente_nombre | id_manifiesto | capa3_disco_real (antes) |
|---|---|---|---|---|
| REL-02b8ee6d0e13dfb6dc7d3331 | N27 | CSES Module 5 México 2018 | cses5_modulo5_2016_2021_cuestionario | NO_REFERENCIADO |
| REL-162b116abdb2212886430f08 | N25 | CSES Module 5 México 2018 | cses5_modulo5_2016_2021_cuestionario | NO_REFERENCIADO |
| REL-3d6a985a8dafc13fdbd39e4a | N5 | World Values Survey | f00006635_wvs7_questionnaire_mexico_2018_spanish | NO_REFERENCIADO |
| REL-48285fd8e0a22a38147245ed | N17 | CSES Module 5 México 2018 | cses5_modulo5_2016_2021_cuestionario | NO_REFERENCIADO |
| REL-57df012cdba3e281563c1068 | N15 | World Values Survey | f00006635_wvs7_questionnaire_mexico_2018_spanish | NO_REFERENCIADO |
| REL-62c97ccb92d0e95c8120d776 | N28 | ISSP Social Networks and Social Resources 2017 México | za6980_q_mx | NO_REFERENCIADO |
| REL-72ff714a3ba6d0bab952e05f | N2 | ISSP Social Networks and Social Resources 2017 México | za6980_q_mx | NO_REFERENCIADO |
| REL-75b2ff53a19d8058eba2dbb7 | N13 | ISSP Social Networks and Social Resources 2017 México | za6980_q_mx | NO_REFERENCIADO |
| REL-7751c832c7e30e4e4d7603cc | N12 | ISSP Social Networks and Social Resources 2017 México | za5900_q_mx | NO_REFERENCIADO |
| REL-845a93bc24990147a394f897 | N2 | ISSP Social Networks and Social Resources 2017 México | za6980_q_mx | NO_REFERENCIADO |
| REL-8d2952203ec3678f3bd0c473 | N30 | ISSP Social Networks and Social Resources 2017 México | za6980_q_mx | NO_REFERENCIADO |
| REL-9dfab617c356df5594575a3c | N12 | ISSP Social Networks and Social Resources 2017 México | za6980_q_mx | NO_REFERENCIADO |
| REL-b034b04e9ba040bd02e39b8b | N14 | ISSP Social Networks and Social Resources 2017 México | za6980_q_mx | NO_REFERENCIADO |
| REL-c0ffdbcc616f342880df820a | N26 | CSES Module 5 México 2018 | cses5_modulo5_2016_2021_cuestionario | NO_REFERENCIADO |
| REL-cd0d1c5fd7e85418603c73cd | N13 | ISSP Social Networks and Social Resources 2017 México | za5900_q_mx | NO_REFERENCIADO |
| REL-d630dc1ea394364e53631401 | N13 | ISSP Social Networks and Social Resources 2017 México | za5900_q_mx | NO_REFERENCIADO |
| REL-e95e26820797a0f55c9246d7 | N12 | ISSP Social Networks and Social Resources 2017 México | za6980_q_mx | NO_REFERENCIADO |
| REL-ee1e829631a8bb7de93bcfd3 | N26 | CSES Module 5 México 2018 | cses5_modulo5_2016_2021_cuestionario | NO_REFERENCIADO |
| REL-f219eb1a0e1b71beb5a36f6f | N30 | ISSP Social Networks and Social Resources 2017 México | za5900_q_mx | NO_REFERENCIADO |

Las 19 filas resuelven a solo **4** valores distintos de `id_manifiesto` (columna 7):

```
$ awk -F'\t' 'NR==1{next} $10=="SI" && $11!="EXISTE;COINCIDE;INTEGRO" {print $7}' data/curacion-registro/relaciones.tsv | sort | uniq -c
      5 cses5_modulo5_2016_2021_cuestionario
      2 f00006635_wvs7_questionnaire_mexico_2018_spanish
      4 za5900_q_mx
      8 za6980_q_mx
```

Una invocación de `--verifica` por id (no por fila) basta para derivar las 19.

## §3 · Vocabulario de capa3 — leído de las 24 filas que ya lo tienen

```
$ awk -F'\t' 'NR==1{next} $10=="SI"{print $11}' data/curacion-registro/relaciones.tsv | sort | uniq -c
     24 EXISTE;COINCIDE;INTEGRO
     19 NO_REFERENCIADO
```

Un solo valor "positivo" ya en uso: `EXISTE;COINCIDE;INTEGRO`. No se inventa variante.

## §4 · Las cuatro verificaciones — salida cruda

Salida completa de cada invocación guardada; se pega aquí el bloque de veredicto (líneas 1-6 de cada una — el resto de la salida, idéntico en las cuatro invocaciones salvo la línea 3, es el listado boilerplate "Procedencia derivada" de las 554 entradas completas del manifiesto, ajeno al id consultado; verificado con `diff` entre dos invocaciones que solo difiere esa línea).

```
$ python3 tests/manifiesto.py --verifica --id cses5_modulo5_2016_2021_cuestionario
Entorno de verificación: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4

cses5_modulo5_2016_2021_cuestionario [data_raw]: COINCIDE -- sha256 y tamaño (117737 bytes) verificados contra data/manifiesto.yaml

Por raíz (sin colapsar):
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```

```
$ python3 tests/manifiesto.py --verifica --id f00006635_wvs7_questionnaire_mexico_2018_spanish
Entorno de verificación: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4

f00006635_wvs7_questionnaire_mexico_2018_spanish [descargas_mx]: COINCIDE -- sha256 y tamaño (96941 bytes) verificados contra data/manifiesto.yaml

Por raíz (sin colapsar):
  descargas_mx: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```

```
$ python3 tests/manifiesto.py --verifica --id za5900_q_mx
Entorno de verificación: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4

za5900_q_mx [descargas_mx]: COINCIDE -- sha256 y tamaño (228950 bytes) verificados contra data/manifiesto.yaml

Por raíz (sin colapsar):
  descargas_mx: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```

```
$ python3 tests/manifiesto.py --verifica --id za6980_q_mx
Entorno de verificación: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4

za6980_q_mx [descargas_mx]: COINCIDE -- sha256 y tamaño (247978 bytes) verificados contra data/manifiesto.yaml

Por raíz (sin colapsar):
  descargas_mx: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```

Las cuatro dan `COINCIDE`. Cero `AUSENTE`, cero hash discordante — no hay PARO.

## §5 · Mapeo fila → valor a escribir (Commit 2)

Las cuatro `id_manifiesto` distintas resuelven las 19 filas: `EXISTE;COINCIDE;INTEGRO` en las 19, ninguna excepción. El mecanismo de escritura será `split`/`join` por `\t` sobre las líneas exactas de la tabla de §2, nunca `csv.writer` (defecto conocido del 13/ago, re-citó comillas y corrompió 7 filas ajenas de universo-puertas). Commit 2 escribe, corre `git diff --unified=0` y confirma que el diff toca exactamente 19 líneas, un campo por línea.

Frase de cierre de siempre.

## §6 · Commit 2 — escritura

Autocorrección declarada antes de escribir: el archivo de encargo de §0 (A.3) se había commiteado en Commit 1 como `forense/encargos/2026-08-13-capa3-reconcilia.md` — nombre normalizado idéntico al de esta nota, y `tests/check.py` (T02) lo marcó como colisión real (no falso positivo: son dos archivos de contenido distinto con el mismo nombre normalizado). Renombrado en este commit a `forense/encargos/2026-08-13-encargo-c-capa3-reconcilia.md`, vía `git mv` — mismo contenido, sin tocar Commit 1 ya empujado.

Escritura por `split`/`join` de `\t` (script Python de una sola pasada, sin `csv.writer`), sobre las 19 líneas exactas identificadas en §2/§5:

```
$ git diff --unified=0 -- data/curacion-registro/relaciones.tsv | grep -c '^[+-][^+-]'
38
```

38 líneas de diff = 19 líneas lógicas (una `-` y una `+` por fila), confirmado línea por línea contra la tabla de §2 — en cada una, el único campo que cambia es `capa3_disco_real`, de `NO_REFERENCIADO` a `EXISTE;COINCIDE;INTEGRO`. Diff completo en el commit.

Distribución `capa2_manifiesto` × `capa3_disco_real`, antes/después:

| | antes | después |
|---|---|---|
| `SI` × `EXISTE;COINCIDE;INTEGRO` | 24 | 43 |
| `SI` × `NO_REFERENCIADO` | 19 | 0 |
| `SI_O_REFERENCIADO` × `SI_O_PARCIAL` | 68 | 68 (sin tocar) |
| `NO_REFERENCIADO` × `NO_REFERENCIADO` | 86 | 86 (sin tocar) |

Contador central del encargo: filas con `capa2=SI` y `capa3` en desacuerdo: **19 → 0**. Ninguna volvió `AUSENTE` — verificado sobre la tabla completa (no solo las 19), 0 filas con `AUSENTE` o `NO_COINCIDE` en `capa3_disco_real`.

`python3 tools/curador_registro/via_capa2.py`:

```
Filas en relaciones.tsv: 197
Diffs propuestos (capa2_manifiesto): 0
```

0 diffs — capa2 no se movió, como exige el perímetro.

`tests/check.py --baseline` contra `948ad70` (línea base congelada por ENLACE-1 · Commit 4):

```
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 948ad70343320b62f000d31fd39e2b2b68336ad9)
```

(22 FAIL · 105 WARN en la corrida cruda — la misma cuenta pre-existente que ENLACE-1 · Commit 2 ya declaró ROJA/preexistente contra el baseline congelado más viejo; contra el freeze real de `948ad70` esta corrida da VERDE, incluido el T02 ya corregido arriba.)

## §7 · TRASPASO — no arreglado aquí, dirigido a APERTURA-ISSP y a ENLACE-2

Hallazgo de paso, fuera del perímetro de este acto (que verifica procedencia, `capa2` vs `capa3`, no suficiencia semántica, que es `capa4`): de las 19 filas, las 12 ISSP resuelven a `za6980_q_mx` (8 filas) y `za5900_q_mx` (4 filas) — ambos **cuestionarios**, no codebooks. Pero **7 de las 12** declaran en `siguiente_accion` (`data/curacion-registro/utilidad-modelo.tsv` / `evidencias.tsv`) que lo que piden es abrir un **codebook**, no releer el cuestionario:

| relacion_id | necesidad_id | id_manifiesto apuntado | `siguiente_accion` declarada |
|---|---|---|---|
| REL-72ff714a3ba6d0bab952e05f | N2 | za6980_q_mx | "Obtener codebook México 2017." |
| REL-845a93bc24990147a394f897 | N2 | za6980_q_mx | "Abrir codebook." |
| REL-8d2952203ec3678f3bd0c473 | N30 | za6980_q_mx | "Abrir codebook." |
| REL-9dfab617c356df5594575a3c | N12 | za6980_q_mx | "Obtener codebook." |
| REL-b034b04e9ba040bd02e39b8b | N14 | za6980_q_mx | "Abrir codebook." |
| REL-cd0d1c5fd7e85418603c73cd | N13 | za5900_q_mx | "Consolidar codebook." |
| REL-d630dc1ea394364e53631401 | N13 | za5900_q_mx | "Obtener codebook." |

Para el módulo ZA5900 el codebook **ya existe como payload en el corpus, sin que ninguna fila lo referencie**:

```
$ python3 tests/manifiesto.py --verifica --id za5900_cdb
za5900_cdb [descargas_mx]: COINCIDE -- sha256 y tamaño (5971210 bytes) verificados contra data/manifiesto.yaml
```

`za5900_cdb` (`ZA5900_cdb.pdf`, 5.97 MB, `usado_para` en el manifiesto: *"ISSP 2012 Family and Changing Gender Roles IV, Mexico -- codebook completo... N13 (familismo_obligacion) candidato mas fuerte de los 3 modulos ISSP... N12 (familismo_apoyo) tematicamente adyacente"*) — describe con precisión N13/N12, pero las dos filas N13 de arriba (`REL-cd0d1c5fd7e85418603c73cd`, `REL-d630dc1ea394364e53631401`) siguen apuntando a `za5900_q_mx` (el cuestionario), no a `za5900_cdb`. Para ZA6980 no existe ningún `id_manifiesto` de tipo codebook en `data/manifiesto.yaml` (`grep -n "za6980.*cdb\|za6980_cdb"` → 0 resultados) — las 5 filas que piden codebook de ese módulo no tienen a qué apuntar todavía, distinto del caso ZA5900 donde el payload ya está y solo falta el enlace.

No se corrige aquí: `capa2=SI` es una afirmación de procedencia (el `id_manifiesto` resuelve a un payload íntegro en disco), no de suficiencia — si el objeto de evidencia pedía otro documento, eso vive en `capa4_apertura_mapeo`, que sigue vacía en las 19 filas de este acto. Traspaso explícito para que no se pierda como pasó con ABRIR-4 (cinco días sin verse): **APERTURA-ISSP** (dueña de `capa4` en estas filas) debería decidir si las 2 filas N13/ZA5900 deben reapuntar `id_manifiesto` a `za5900_cdb`, y si las 5 filas ZA6980 necesitan que alguien adquiera/registre su codebook antes de poder cerrar `capa4`; **ENLACE-2** debería considerar el mismo hallazgo al absorber los veredictos de `capa4` en su pasada sobre `relaciones.tsv`.

Frase de cierre de siempre.
