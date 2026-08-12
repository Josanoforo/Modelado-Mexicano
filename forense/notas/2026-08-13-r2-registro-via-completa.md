# ACTO R″ · Registro de descargas por la vía completa

Sustituye a ENCARGO-R-prima (no lanzado). Base declarada por el encargo: `origin/main = 2b13e88`.

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/pc0/proyectos/Modelado-Mexicano` (branch `main`, local en `f542c93`, detrás de origin). `git fetch origin main` → `a6fcf9d..2b13e88`. Worktree nuevo `git worktree add -b acto-r2prima/registro-via-completa-20260812-162554 /home/pc0/worktrees/mm-acto-r2prima-20260812-162554 origin/main`.
2. **SHA.** `git log -1` → `2b13e88 Merge pull request #189 from Josanoforo/map-b/crosswalk-fuente-puerta` — coincide exacto con la base que declara el encargo, sin deriva que re-derivar.
3. **data/raw.** Ausente al crear el worktree (esperado, gitignorado). Enlazado: `ln -s /home/pc0/mm-corpus/raw data/raw` (6.4G, corpus real). `data/raices.local.yaml` (gitignorado) copiado de un worktree hermano — `descargas_mx: /mnt/c/Users/PC0/Descargas MX`, confirmado montado con contenido.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir → `sin_variable` (esperado). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200` (hay red en esta caja; no bloqueante — este acto no descarga nada, solo lee lo que el usuario ya bajó).
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de este worktree, del corpus compartido, o de `/mnt/c/Users/PC0/Descargas MX`, comando a la vista.

Discrepancia de fecha notada y no bloqueante: el encargo se titula 13/ago, el reloj de la caja marcó `2026-08-12 16:25 CST` al abrir. El propio `main` en `2b13e88` ya contiene notas fechadas 2026-08-13 (`forense/notas/2026-08-13-map-b-crosswalk.md`, parte de PR #189) — la convención de fecha del proyecto en esta sesión ya corría un día adelante del reloj del sistema antes de que este acto empezara. Se sigue esa convención para el nombre de este archivo.

## 1 · Premisas y precedente (comandos, PASO 1)

```
$ git log -1 --format="%h %s"
2b13e88 Merge pull request #189 from Josanoforo/map-b/crosswalk-fuente-puerta

$ grep -c "ZA6980\|ZA7600" data/manifiesto.yaml data/curacion-universo/activos-descubiertos-durante-ronda.tsv
data/manifiesto.yaml:0
data/curacion-universo/activos-descubiertos-durante-ronda.tsv:0

$ wc -l data/curacion-universo/activos-descubiertos-durante-ronda.tsv data/curacion-universo/decisiones-adquisicion.tsv
   5 activos-descubiertos-durante-ronda.tsv   (4 filas ADESC- + header)
   4 decisiones-adquisicion.tsv                (3 filas DADQ- + header)

$ python3 -c "import json;print(json.load(open('data/curacion-universo/snapshot-t0.json'))['snapshot_t0_sha256'])"
89f4c3a49c00c0e1ba1f07013e0af10bbc3289fdddc48dde816c37d3da1a742b
```

`git show 0e07179` leído completo (el precedente): dos filas ADESC- añadidas a mano (ENASIC·922, ENCUCI·647), `origen=ADR70_P2_FICHA_RNM_VERIFICADA_PREVIAMENTE`, `activo_descubierto_id` derivado con `snapshot_universe.stable_id()` (mismo mecanismo que las dos entradas previas, `size=24`). `snapshot_t0_sha256` verificado byte a byte sin cambio antes/después.

**Hallazgo mid-PASO-1, antes de decidir nada:** `ls "/mnt/c/Users/PC0/Descargas MX"` muestra que el usuario descargó **tres** estudios ISSP, no dos — `ZA5900` (2012, 11 archivos) además de `ZA6980` (2017) y `ZA7600` (2019). `ZA7600` además trae sus `.dta.zip`/`.sav.zip` reales (16:11), no solo la ficha que el encargo asumía que el usuario había "abierto". El encargo se escribió sin ver esto — se reporta aquí y se incorpora al alcance del acto (mismo espíritu que extender a ZA7600: dejarlo fuera habría sido un hueco previsible, no una fidelidad al encargo).

## 2 · PASO 2 — veredicto sobre el alcance de WVS/ISSP, con evidencia

El encargo planteaba dos lecturas del precedente, (a) "un payload no es un activo descubierto" vs (b) "WVS quedó a medio registrar". Ninguna de las dos, tal como estaban planteadas, resultó exacta — la resolución real es más precisa que el binario.

**Paso 1 de la verificación — leer `forense/notas/2026-08-12-acto-p-lote1-adquisicion.md` completo (18KB, la "nota de ACTO P" que el encargo cita).** §5.0 de esa nota ya investigó esta pregunta exacta, para las mismas 5 fuentes internacionales del lote (ISSP, WVS, EARLY_CHILDHOOD/Banco Mundial, GPS, CSES): `tools/curador_registro/decide_acquisition.py` (leído, no tocado — fuera de perímetro para escritura) opera sobre `universo-declarado-t0.tsv` + `activos-descubiertos-durante-ronda.tsv`, produciendo decisiones `NO_ADQUIRIR_AHORA`/`BUSQUEDA_DIRIGIDA` para el dominio T0 — **"el motor declarado no tiene vía para este mecanismo... aplica a las 5 fuentes por igual"**. Consistente con esto: ninguna de las 5 fuentes de ese lote (incluida WVS, ya `EXISTE-SATISFACE` con 11 archivos reales desde el commit `84f8e30`) tiene fila en `activos-descubiertos-durante-ronda.tsv` ni en `decisiones-adquisicion.tsv`.

**Paso 2 — un nivel más abajo de lo que el PASO 1 del encargo pedía verificar.** `data/curacion-universo/universo-declarado-t0.tsv` (35,709 filas) — nadie lo había mirado para esta pregunta — ya contiene ISSP y WVS como activos T0 declarados **desde antes de esta sesión**:
- ISSP Social Networks 2017 (el módulo de ZA6980): **6 filas** distintas (`ACT-81fb4bca...`, `ACT-83e6726d...`, `ACT-91400343...`, `ACT-a57367e4...`, `ACT-f209be68...`, `ACT-f3e91ab6...` — esta última con `url_localizador_principal` idéntica a la de `data/cola-adquisicion-2026-08-12.tsv`), todas `duplicado_verificado=NO`.
- ISSP Social Inequality 2019 (ZA7600): 2 filas (`ACT-4bd24874...`, `ACT-5e96311e...`).
- ISSP Family/Gender Roles 2012 (ZA5900, el estudio que el encargo no sabía que existía): 6 filas.
- WVS: 9 filas.

Confirmado ejecutando `tools/curador_registro/decide_acquisition.py` contra un `--output` de prueba (no el real) y comparando: el script **jamás** genera una decisión para una fila individual de `universo-declarado-t0.tsv` — solo las colapsa en un agregado por hash (`CONJUNTO_T0_NO_ADQUIRIDO:n=...`) o emite una fila por cada `activo_descubierto_id` YA en `activos-descubiertos-durante-ronda.tsv`. No hay, ni en principio, un mecanismo para que ISSP reciba su propia decisión individual.

**Veredicto:** `activos-descubiertos-durante-ronda.tsv` es el canal para activos **fuera** del universo T0 declarado — la propia reserva del precedente lo dice ("no se añade al denominador"). ISSP (los tres módulos) y WVS ya estaban **dentro** del universo T0 declarado, simplemente sin adquirir. Añadir una fila ADESC- aquí sería un error de categoría: declararía "descubierto post-T0" algo que el corpus ya conocía. La acción correcta al adquirir sería voltear la(s) fila(s) correspondiente(s) de `universo-declarado-t0.tsv` de `DECLARADO_NO_ADQUIRIDO` a `ADQUIRIDO` — pero ese archivo **no está en el perímetro de este acto**. Por tanto: **PASO 5.1 y 5.2 no producen filas nuevas**, no por default sino por verificación estructural. El encargo anterior (ACTO P) tampoco estaba incompleto en este punto — hizo lo correcto por la razón correcta, aunque no la haya articulado así.

**Hallazgo colateral, reportado y NO reparado (fuera de perímetro):** regenerar `decisiones-adquisicion.tsv` hoy (verificado con `--output` de prueba) produciría 5 filas, no 3 — faltan las 2 `BUSQUEDA_DIRIGIDA` de ENASIC/ENCUCI que `0e07179` añadió a `activos-descubiertos` y que nadie propagó — y el agregado cambiaría de `n=35517` a `n=35199` (318 activos pasaron a `ADQUIRIDO` desde el `0e07179`). El archivo vigente está desincronizado de sus propias fuentes. Se reporta a mesa.

## 3 · PASO 3 — identidad de ZA6980, por su documento

`ZA6980_q_mx.pdf`, página 1 (portada, sin numerar): *"Mexico / ISSP 2017 – Social Networks and Social Resources / Questionnaire"*. Inequívoco, sin ambigüedad que resolver.

Contenido (Q1 generador de posición — conoce a alguien de tal ocupación; Q5 participación en grupos/asociaciones; Q7/Q8 a quién recurriría para ayuda en 5+4 situaciones; Q9 soledad/aislamiento; Q11 confianza generalizada): candidato razonable para **N2/N12/N14** (`radio_confianza`/`familismo_apoyo`, Q7/Q8/Q11 son baterías clásicas de esos constructos) y parcialmente para **N30** (R8.3, "puente personal→confianza en desconocido": Q1+Q11 son temáticamente relevantes, sin ser una medición directa del mecanismo del falsador). **N13** (`familismo_obligacion`, deber normativo) y **N28** (R8.1, monitoreo+sanción específico) están tematicamente débiles aquí — el cuestionario mide conducta/preferencia revelada de apoyo, no obligación normativa, y Q5 no pregunta por mecanismos de sanción dentro de los grupos.

## 4 · PASO 4 — apertura de los ZIP y verificación de México en el dato (el núcleo del acto)

Inventario sin extraer (`zipfile.namelist()`, equivalente a `unzip -l` — `unzip`/`7z` no están instalados en esta caja, confirmado con `command -v`; `python3 -c "import zipfile"` sí):

```
ZA6980_v2-0-0.dta.zip  → ZA6980_v2-0-0.dta (30341248 B) + _missing.txt
ZA6980_v2-0-0.sav.zip  → ZA6980_v2-0-0.sav (64788182 B)
ZA5900_v4-0-0.dta.zip  → ZA5900_v4-0-0.dta (deflate) + _missing.txt
ZA5900_v4-0-0.por.zip / ZA5900_v4-0-0.sav.zip
ZA7600_v3-0-0.dta.zip  → ZA7600_v3-0-0.dta (deflate) + _missing.txt
ZA7600_v3-0-0.sav.zip  → ZA7600_v3-0-0.sav (deflate)
```

Variable de país derivada leyendo la lista de columnas en cada caso (`pandas.io.stata.StataReader`, alternativa que el propio encargo ofrecía a `pyreadstat` — no instalado, `pip install` no fue necesario) — **nunca tecleada de memoria**, y con razón: el nombre cambia entre releases.

| Estudio | Módulo | Variable país real | México | N | Verdicto A.4 |
|---|---|---|---|---|---|
| **ZA6980** | ISSP 2017 Social Networks | `c_alphan` (min.) + `country` (num., ISO 484) | **SÍ** | **1002** de 44,492 | **EXISTE-SATISFACE** |
| **ZA5900** | ISSP 2012 Family/Gender Roles IV | `C_ALPHAN` (MAYÚS. — release más vieja, esquema distinto) | **SÍ** | **1527** de 61,754 | **EXISTE-SATISFACE** |
| **ZA7600** | ISSP 2019 Social Inequality V | `c_alphan` + `country` | **NO** | **0** de 44,975 (29 países, MX nunca aparece) | **EXISTE-NO-SATISFACE** |

Comandos (ejemplo ZA6980, mismo patrón para los otros dos):
```python
with zipfile.ZipFile("ZA6980_v2-0-0.dta.zip") as z, z.open("ZA6980_v2-0-0.dta") as f:
    reader = pd.io.stata.StataReader(f, convert_categoricals=False)
    df = reader.read()
df['c_alphan'].value_counts()   # MX  1002
df['country'].value_counts()    # 484 1002  (ISO 3166 numérico de México, coincide exacto)
```
`studyno`/`doi`/`version` embebidos en cada archivo confirman identidad sin ambigüedad (6980/`10.4232/1.13322`/2.0.0; 7600/`10.4232/1.14009`/3.0.0; ZA5900 usa `V1`/`DOI` en vez de `studyno`/`doi` minúsculas — 5900/`10.4232/1.12661`).

`ZA5900` no traía cuestionario descargado en el encargo original — se leyó su propia portada (`ZA5900_q_mx.pdf`, p.1: *"Mexico / ISSP 2012 – Family and Changing Gender Roles IV / Questionnaire"*) al incorporarlo. Contenido: V27 *"Adult children are important source of help for elderly parents"*, V35/V36 provisión/costo de cuidado a mayores — es el candidato **más directo de los tres módulos** para **N13** (`familismo_obligacion`), más que ZA6980.

Duplicados de descarga del navegador, byte-idénticos por `sha256sum`, deliberadamente **no** registrados: `ZA6980_q_mx (1).pdf`, `ZA5900_cdb (1).pdf`.

**Qué le pasa a la asignación de 7 necesidades (N2,N3,N12,N13,N14,N28,N30) que la cola atribuye a "ISSP" como fuente única: SE ACOTA, no se cae ni se confirma en bloque.** La cola trataba "ISSP" como una sola fuente_canonica con una sola URL conocida (el módulo 2017); en realidad son 3 módulos con estados distintos. `N3` está explícitamente ligada por el propio texto de la cola a "release final ISSP 2019, 29 países" — es decir, a ZA7600 — y ZA7600 **confirma con el dato real** (no solo con el sondeo web del 2026-08-06 que la cola ya citaba) que México está ausente: `N3` no se sirve desde ISSP. Las otras 6 necesidades quedan repartidas entre los módulos 2012 y 2017 (ambos con México presente) sin que el corpus haya distinguido antes cuál corresponde a cuál con precisión de item — eso excede lo que este acto puede cerrar sin abrir cada reactivo contra cada necesidad, y es justamente el trabajo de una apertura a nivel variable (M-APERTURA), no de este acto. Reportado a mesa; la cola (`data/cola-adquisicion-2026-08-12.tsv`) no se edita — fuera de perímetro.

## 5 · PASO 5 — registro

**5.1/5.2 (activos descubiertos / decisiones de adquisición): sin filas nuevas.** Justificación completa en §2. No es un default — es la conclusión de verificar el mecanismo real.

**5.3 · Manifiesto**, vía `tests/manifiesto.py`. Corrección de mecanismo frente a lo que el encargo asumía: las 11 entradas de WVS (`84f8e30`) **no** se registraron con `--registra` (esa ruta, en esta versión del script, solo resuelve contra `data/raw/` — verificado leyendo `cmd_registra`, sin parámetro `--raiz`) — se registraron vía `--escanea <raiz> --grupo/--promueve`, la única vía que soporta `raiz: descargas_mx`. Se siguió el mismo mecanismo aquí, en pares `--escanea`(taggeado)+`--promueve` **inmediatos** por grupo de estudio (nunca N `--escanea` seguidos de un `--promueve` al final — el defecto de acumulación que ACTO P encontró y documentó). Valores largos (URL de ZA5900, 90 caracteres) mantenidos fuera de `--escanea`/`--promueve` para no disparar el defecto de plegado YAML de `manifiesto-staging.yaml` (>78 caracteres) — patchados después directamente vía `escribir_manifiesto()` importada del propio script (misma vía segura que usó ACTO P), nunca reimplementada ni tecleada a mano.

16 payloads reales registrados (4 ZA6980 + 10 ZA5900 + 2 ZA7600; excluidos los 2 duplicados byte-idénticos): `za6980_q_mx`, `za6980_backgroundvar_mx`, `za6980_v2_0_0_dta`, `za6980_v2_0_0_sav`, `za5900_q_mx`, `za5900_backgroundvar_mx`, `za5900_bq`, `za5900_cdb`, `za5900_mr`, `za5900_overview`, `za5900_questionnaire_development_report`, `za5900_v4_0_0_dta`, `za5900_v4_0_0_por`, `za5900_v4_0_0_sav`, `za7600_v3_0_0_dta`, `za7600_v3_0_0_sav`. `sha256`/`tamano_bytes`/`entorno_descarga` derivados por el script; `usado_para` refleja las necesidades que el PASO 4 dejó en pie (no las 7 crudas de la cola); `nota` documenta el veredicto de México y N para cada estudio, y para los archivos no abiertos a nivel de contenido (bq/cdb/mr/overview/questionnaire_development_report de ZA5900) lo declara explícitamente en vez de sobre-afirmar. `git diff --stat data/manifiesto.yaml`: 314 inserciones, 0 borrados — 538→554 entradas, ninguna de las 538 preexistentes tocada. Las 16 verificadas `--verifica`: **16/16 COINCIDE**.

**5.4 · Puertas**, edición directa de `data/universo-puertas-2026-08-12.tsv` (ningún script lo escribe, verificado — `grep -rl universo-puertas *.py` vacío). ⚠️ Corrección de método a mitad de este paso: un primer intento usó el módulo `csv` de Python para reescribir el archivo, y `csv.writer` re-citó (comillas dobladas) cualquier campo con `"` interno — corrompió 7 filas ajenas (Mejoredu, CIDE, ICPSR, COLEF, MCCI, Mexico Evalúa, PNT, WORLD_BANK_ENTERPRISE_SURVEY) que no usan esa convención de escape. Detectado con `git diff` antes de commitear, revertido con `git checkout --`, reescrito con split/join manual por `\t` (mismo patrón que el resto del archivo ya usa). Diff final: exactamente 1 fila modificada + 1 fila nueva, verificado con `git diff --unified=0` mostrando solo esas dos líneas.

- Fila `GESIS_ISSP` (nueva, `organismo_internacional`): resume los 3 módulos, `necesidad_que_sirve=N2,N3,N12,N13,N14,N28,N30`, `clasificacion_a4=EXISTE-SATISFACE` a nivel puerta (2/3 módulos sirven México real), con la excepción de N3/ZA7600 declarada en el campo de observaciones, no escondida detrás de una palabra sola.
- Fila `WorldBank_MEX_ECEPIE_2012_2014_catalogo2661` (existente): actualizada — el usuario confirmó (en esta sesión, no verificable por este agente vía Gmail — mismo bloqueo del clasificador de auto-mode que documentó ACTO P) haber activado la cuenta NADA por correo el 13/ago. `clasificacion_a4` se mantiene `EXISTE-NO-SATISFACE` **a propósito**: el microdato nuclear ("Get Microdata") sigue sin descargarse y este acto no descarga nada (fuera de perímetro) — subir a `EXISTE-SATISFACE` habría sobre-declarado. `fecha_sondeo` → `2026-08-13`.

## 6 · Verificación de cierre (defecto PR #77)

Para `raiz: descargas_mx` el "corpus compartido" **es** `/mnt/c/Users/PC0/Descargas MX` en sí — un folder real de Windows montado por WSL, no una copia por-worktree; nunca se copió nada a `data/raw` de este worktree para este acto (`git status --short data/raw` solo muestra el symlink sin trackear, sin archivos ISSP dentro). Las 16 entradas se verificaron con `tests/manifiesto.py --verifica`, que resuelve la ruta real vía `data/raices.local.yaml` — no hay ruta alternativa donde el defecto de PR #77 pudiera esconderse aquí.

## 7 · Cierre

Ver mensaje de cierre al usuario (7 líneas) fuera de este archivo. `snapshot_t0_sha256` re-verificado idéntico:
```
$ python3 -c "import json;print(json.load(open('data/curacion-universo/snapshot-t0.json'))['snapshot_t0_sha256'])"
89f4c3a49c00c0e1ba1f07013e0af10bbc3289fdddc48dde816c37d3da1a742b
```
`python3 tests/check.py --baseline cruda`: **LÍNEA BASE VERDE** — 22 FAIL · 104 WARN, nada nuevo frente a `tests/baseline.json` (HEAD congelado `e7cd99da7ae1d776a499f9d5009c061b1be73770`).

Sin push, sin PR abierto en esta sesión.
