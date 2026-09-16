# Cierre · `ACTO GEN2-CAJA-REACTIVOS-FD-1`

`NC-0245` + `NC-0235`, en CAJA. 15-16/sep/2026, Opus. `ADR-525`.
Encargo archivado verbatim por 0-bis A.3 en `forense/encargos/2026-09-15-GEN2-CAJA-REACTIVOS-FD-1.md`.

---

## 0 · ARRANQUE (Bloque D, salidas crudas)

**0.a · Base al día.** `git fetch --prune` · `git rev-list --count HEAD..origin/main` → **0** contra
`9fd59d0` (merge de `PR #806`). **`origin/main` se movió a media faena** (`PR #807`/`#808`/`#809`,
hasta `05977ef`): se re-fetcheó y se fusionó; consecuencia material abajo (§6.1).

**0.b · Árbol limpio.** `git status --porcelain` vacío antes del 0-bis.

**0.c · Duplicado, en los tres sitios.** `git ls-remote --heads origin | grep -iE "reactivos|fd-1"` →
sin coincidencia. `git worktree list` → sólo los dos worktrees ajenos
(`mm-gen2-reactivos-contexto-busqueda`, `mm-gen2-reactivos-residuales-busqueda-util`), ninguno con
este rótulo. `gh pr list --state open` → un solo PR abierto (`#805`, `adq/2026-09-15-nc-0202`), que
es precisamente el que el lanzamiento declara fuera. Sin duplicado.

**0.d · Higiene (`tools/limpia_arbol.py --reporta`, sólo reporte).** base al día (`al_dia=SI`,
0 commits detrás); 2 ramas remotas sin PR abierto → `fuera_de_politica`
(`acto/gen2-f6-panel-caja-1` —el acto hermano, viva— y `censo/2026-09-15`). No se borró nada: el
`--aplica` no se decide desde aquí.

**1 · Repo.** Clon existente `/home/pc0/Modelado-Mexicano`; worktree del acto creado en
`/home/pc0/mm-gen2-caja-reactivos-fd-1` sobre `origin/main` fresco. No se clonó nada nuevo. El
worktree principal estaba en `b510c6b` (rama `censo/2026-09-11`), **50+ commits atrás** — por eso
`.claude/commands/acto.md` se leyó desde el worktree NUEVO, no desde el padre.

**2 · SHA.** Base declarada en el encargo = base real = `9fd59d0` al arrancar.

**3 · `data/raw`.** Nació ausente (gitignorada) y **no es PARO**: `ln -s /home/pc0/mm-corpus/raw
data/raw` + copia de `data/raices.local.yaml` desde un worktree hermano, **antes** de evaluar
cualquier cosa de datos. Este acto **no descarga nada**, así que el anti-PR#77 no aplica (§7).

**4 · Entorno (`python3 tools/entorno.py`, salida cruda).**

```
ENTORNO · commit=9fd59d063242 · git_status=LIMPIO(0) · python=3.14.4 ·
numpy=2.3.5 pandas=2.3.3 scipy=1.16.3 yaml=6.0.3 pyreadstat=1.3.6 ·
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable CHECK_SELFCHECK_CHILD=sin_variable
MODELADO_RAICES=sin_variable PYTHONHASHSEED=sin_variable TZ=sin_variable ·
red=no-ejecutada · raices=data_raw:SI descargas_mx:SI · corpus=SI(examinados=413)
```

**Red no sondeada a propósito**: este acto no descarga ni consulta nada en línea; una sonda que
nadie pidió es I/O que nadie declaró. **A.13:** el `corpus=SI` viene de **413 archivos examinados**,
no de la presencia del symlink.

**5 · Espejo.** Ninguna cifra de esta nota sale del espejo del proyecto. Todas salen del clon de (1)
con el comando a la vista.

**COMPUERTA.** `COMPUERTA: ninguna` — el lanzamiento no declara `GATED a`, `Estado: GATED a` ni
`COMPUERTA:` en ninguna de las tres formas. No dispara verificación.

---

## 1 · El terreno, medido antes de escribir (A.8)

`NC-0245` dejó **7 620** filas ciegas con dos motivos y una tesis: son diferencia **«MATERIAL, no de
ortografía»**, y «NUBE resuelve ortografía, no semántica». La tesis es correcta. Lo que la medición
de este acto añade es que **«material» no implica «irrecuperable»**, y que la mezcla escondía cuatro
poblaciones que sólo se separan **abriendo el descriptor**:

```
$ (data/reactivos-fd-recuperado-residual-v1_0.tsv, 7620 filas)
  TABLA_SIN_FD    5482   «la hoja no existe en el descriptor indexado»
  VARIABLE_SIN_FD 2138   «la hoja empareja; la variable no aparece en ella»
```

Y el hueco del lado de `NC-0235`: `tools/actualiza_reactivos_contexto.py` traía
`PRIORITY = ("envipe","ennvih","encuci","enif","ensafi")` y **ninguna** de las cinco está entre los
26 grupos del censo de `ADR-519`. Nunca se había corrido sobre ellos.

Ningún crosswalk de tablas existía en el árbol: `ls data | grep -i crosswalk` sólo devuelve
`crosswalk-fuente-puerta-2026-08-1{3,4}.tsv`, que es otro objeto (fuente↔puerta).

**A.8 · medición ya corrida.** Este acto no clasifica, no pre-registra, no carga y no sella ninguna
regla del motor, y no cita ningún `id` de regla ni `R-n`: `tools/ya_medido.py` no aplica.
**A.8 · raíz.** No se pide ninguna descarga y no se declara ningún `AUSENTE-EN-RAIZ`; los 30
descriptores de los 26 grupos se verificaron **presentes** en la raíz montada al derivar la tabla de
fuentes. Censo de raíz del día citado igualmente: `forense/censo-raiz/2026-09-15.txt` — «Total en
disco: 524 · nuevos: 62 · ya registrados: 462 · conflicto de nombre: 0 · fuera de alcance de dato: 0
· clones: 0».

---

## 2 · P1 · El crosswalk, leído del FD real (`NC-0245`)

`tools/crosswalk_tablas_fd.py` → `data/crosswalk-tablas-fd-v1_0.tsv` +
`data/crosswalk-tablas-fd-residual-v1_0.tsv`.

```
$ python3 tools/crosswalk_tablas_fd.py
 "descriptores_abiertos": 37,
 "emparejamientos": 56,
 "instrumentos": 16,
 "por_metodo": { "FD-DECLARA-TABLA": 26, "FD-NOMBRE-DE-HOJA": 13, "IDENTIDAD-DE-VARIABLES": 17 },
 "filas_ciegas_cubiertas": 5062,
 "filas_ciegas_residuales": 2558,
 "por_motivo": { "EJE-TRANSPUESTO": 2172, "IDENTIDAD-INSUFICIENTE": 190,
                 "MIEMBRO-ES-EL-PROPIO-FD": 150, "NO-ES-TABLA-DE-DATOS": 46 }
```

### 2.1 · Lo que el descriptor sí dice, y que ninguna heurística de nombres iba a encontrar

- **Censo 2020.** La hoja `CAAS_Alojamientos` declara, en una celda, **`TABLA: TR_ALO_CAAS`** — y el
  miembro del payload es `TR_ALO_CAAS_00.csv`. Igual `CAAS_Usuarios` → `TABLA: TI_USU_CAAS` y
  `CAAS_Trabajadores` → `TABLA: TI_TRA_CAAS`. El nombre de la hoja **no** se parece al del archivo;
  la declaración interna sí lo dice, literalmente.
- **CNBV BDIF.** El FD trae una columna llamada **`Nombre de la BD`**: `BD Acceso Edo`,
  `BD Uso Mun`, `USO EACP NAL`… y el payload es `52Sep2022_BD_Acceso_Edo.csv`. La única diferencia
  es el **sello de publicación** (`52Sep2022_`), que el FD nunca escribe.
- **CNBV Ahorro/Financiamiento.** El FD declara `4. Sección` → `Ahorro financiero` / `Financiamiento`.

### 2.2 · Donde el FD NO nombra la tabla: identidad por conjunto de variables

El FD de ENDUTIH 2025 **no menciona el DBF en ninguna parte**. Su `Indice` lista
`tic_2025_viviendas … tic_2025_usuarios2`, cada hoja repite `Tabla: tic_2025_hogares`, y el
`Diagrama Entidad - Relación` usa un **tercer** vocabulario (`TR_2025_HOGARES`). El payload se llama
`ti25hog.dbf`. Adivinar la abreviatura habría sido exactamente lo que `NC-0245` prohibió.

La identidad se acredita por el **conjunto de variables**, con emparejamiento **mutuo**, cobertura
≥ 0.95 y margen ≥ 0.30 sobre la segunda candidata:

| miembro | hoja del FD | comunes | margen |
|---|---|---|---|
| `ti25hog.dbf` | `tic_2025_hogares` | 104/104 | 0.89 |
| `ti25usu.dbf` | `tic_2025_usuarios` | 240/240 | 0.93 |
| `ti25usu2.dbf` | `tic_2025_usuarios2` | 108/108 | 0.83 |
| `ti25res.dbf` | `tic_2025_residentes` | 27/28 | 0.36 |
| `ti25viv.dbf` | `tic_2025_viviendas` | 21/22 | 0.50 |

### 2.3 · Dos normalizaciones de variable, cada una con su causa material

Misma clase que el truncado a 31 caracteres de `ADR-522` — **vocabulario, no contenido**:

- **Caja.** MOCIBA escribe `upm`/`p1` en el `.sav` y `UPM`/`P1` en el `.dbf` y en el FD.
- **Sufijo de ola.** ENASEM escribe `A13A_18` donde el FD escribe `A13A`. El sufijo se **deriva del
  nombre del instrumento** (`enasem2018` → `2018`/`18`), nunca se adivina. El FD es inconsistente
  consigo mismo —`B4B_18` conserva el sufijo— así que la regla prueba la forma exacta primero.

### 2.4 · Lo que NO se publicó, y por qué eso es el hallazgo

**2 368 de las 2 558 filas residuales (92%) son irrecuperables por construcción, no deuda:**

- **`EJE-TRANSPUESTO`, 2 172 filas** — el bloque más grande de todo el residual,
  `ADQ15_CNBV_AhorroFinanciero_Financiamiento`. Sus «variables» son **periodos**:
  `2000-09-01`, `2000-12-01`, `2001-03-01`… La tabla pone los conceptos en filas y los trimestres en
  columnas, mientras el FD describe los conceptos. **Para una columna que es una fecha no hay
  enunciado de reactivo que recuperar, ni lo habrá.** Estas 2 172 filas llevaban contadas como
  «ciegas, pendientes de acreditación» y nunca podían dejar de serlo.
- **`MIEMBRO-ES-EL-PROPIO-FD`, 150 filas** — el «miembro» vive dentro de un descriptor, no de un
  payload de datos, y sus «variables» son los rótulos de columna del FD. Medido:
  `('ACCESO DEM NAL', payload = Glosario_Datos_Abiertos_DGASF.xlsx)` tiene 8 variables, que son
  `Descripción`, `Nombre de la BD`, `Nombre de la columna`, `Tipo de dato`.
- **`NO-ES-TABLA-DE-DATOS`, 46 filas** — `Indice`, `Diagrama Entidad - Relación_img`,
  `Modelo de datos`, `tc_cve_catalogo_entidad`, `COD_TC_Rasgo`, `nota_bases_datos_enadid_2023.txt`.

**Lo genuinamente abierto son 190 filas**, no 7 620 (`NC-0258`). Y el umbral no se aflojó para
inflar la cifra: `MOCIBA2015.sav` (159 filas) se ve «obviamente» igual a `TCiberacoso`, pero da
cobertura **0.86** y su hoja tiene un miembro mejor (el `.dbf`) — **sale al residual**.

### 2.5 · Una errata del FD de CNBV, registrada al pasar

La hoja `ACCESO DEM NAL` del `Diccionario_DGPASF.xlsx` declara en su columna `Nombre de la BD` el
valor **`USO DEM NAL`**, que no es el nombre de su propia hoja ni el del payload
(`52Sep2022_ACCESO_DEM_NAL.csv`). El emparejamiento se resolvió por título de hoja
(`FD-NOMBRE-DE-HOJA`, cobertura 1.00, 12/12 variables) y la declaración interna **se ignoró en ese
caso concreto**. Se anota aquí, no se «corrige» el FD: es de la fuente. Mismo espíritu que la errata
`tperviv ↔ TPer_Vic` que `TABLE_IDENTITIES` ya llevaba comentada para ENVIPE 2012.

Nota adicional: los dos descriptores de CNBV BDIF (`Diccionario_DGPASF.xlsx` y
`Glosario_Datos_Abiertos_DGASF.xlsx`) traen **221 filas cada uno** y el mismo contenido — son dos
copias del mismo descriptor publicadas con nombres distintos.

---

## 3 · P2 · La extensión del extractor a los 26 (`NC-0235`)

Tres cambios en `tools/actualiza_reactivos_contexto.py`, ninguno que reescriba lo existente:

1. `--fuentes` y `--verificados` pasan a ser **repetibles** (`action="append"`), con el mismo valor
   por defecto de antes cuando no se pasan.
2. `--crosswalk` (por defecto `data/crosswalk-tablas-fd-v1_0.tsv`): donde el crosswalk dice algo,
   `compatible_table` acredita **esa** hoja y **excluye** a las demás; donde calla, el
   comportamiento histórico (`TABLE_IDENTITIES`) queda intacto — con su falsador en el test.
3. `data/reactivos-contexto-fuentes-fd26-v1_0.tsv`: **30 descriptores, 26 instrumentos** (los 18
   `CABLEAR-CAPA-FD-YA-EN-REPO` + los 8 `CANDIDATA-FD-EXT-POR-VERIFICAR`), con `formato` en el
   vocabulario real de `extract_source()` — los 6 PDF van por `fd_pdf_index` porque los 6 están en
   `inventario-fd-ext-v1_0.tsv`, y ese extractor **verifica** esa capa localizando cada variable en
   una página real del PDF, que es lo que `CANDIDATA-FD-EXT-POR-VERIFICAR` pide.

### 3.1 · El control que mide si el crosswalk era necesario

```
$ ... --objeto endutih2025 --fuentes ...fd26... --crosswalk /nonexistent.tsv
  "filas_con_texto_publicadas": 0,
  "motivos_residuales": { "CORRESPONDENCIA_AMBIGUA": 499, "ETIQUETA_TECNICA_NO_ACREDITADA": 10 }

$ ... --objeto endutih2025 --fuentes ...fd26...        (crosswalk por defecto)
  "filas_con_texto_publicadas": 499,
  "motivos_residuales": { "ETIQUETA_TECNICA_NO_ACREDITADA": 10 }
```

**0 → 499.** Sin el crosswalk el extractor veía varias candidatas para `ti25hog.dbf` y, correctamente,
no publicaba ninguna.

### 3.2 · La corrida sobre los 26

```
"filas_metadato_perimetro": 36707, "filas_con_texto_publicadas": 17888,
"filas_sin_texto_residual": 18819, "grupos_residuales": 370,
"motivos_residuales": { "CORRESPONDENCIA_AMBIGUA": 9396,
                        "ETIQUETA_TECNICA_NO_ACREDITADA": 7108,
                        "PREGUNTA_NO_LOCALIZADA": 2315 }
```

**17 888 enunciados**, todos `texto_tipo = PREGUNTA_DICCIONARIO`, con cita a la hoja y al
`sha256_12` del FD real, en 18 instrumentos: `endireh2011` 7 240 · `enasem2024` 2 212 ·
`enasic2022` 1 319 · `enut2019` 1 303 · `enut2024` 885 · `enadid2023` 682 · `enfih2019` 664 ·
`endutih2025` 499 · `endutih2024` 477 · `endutih2023` 467 · `mociba2016` 414 · `enasem2018` 383 ·
`censo2020` 375 · `mociba2017` 342 · `cnbv_bdif` 209 · `enasem2021` 176 · `mociba2015` 158 ·
`elcos2012` 83.

Los 8 `CANDIDATA-FD-EXT-POR-VERIFICAR` quedan **verificados contra su PDF/XLS real**, con lo que
eso dé: `elcos2012` publica **83** (`NC-0235` lo daba por sospechoso: «29 filas y CERO reactivos» en
la capa indexada) y `enpol2021` publica **0** (`NC-0235` decía que «mezcla reactivos con
encabezados» — se confirma: 1 135 `PREGUNTA_NO_LOCALIZADA`).

---

## 4 · P3 · Consumo: 18 instrumentos dejan de ser ciegos

Clave **explícita** `contexto_fd26` en `tools/busca_reactivos.py::TABLAS` — nunca en `vigente` ni en
`--fuente`, mismo convenio que `fd`/`fd_ext`/`fd_recuperado`/`contexto_v1_0`. El crosswalk **no**
entra al buscador: su grano es la tabla, no el reactivo.

```
instrumentos con ≥1 reactivo con texto buscable:  antes = 38  →  después = 56   (+18)
```

Y por término, `vigente` vs `vigente + contexto_fd26`:

| término | antes | después |
|---|---|---|
| `internet` | 408 | **1 097** |
| `cuidado` | 150 | **567** |
| `celular` | 421 | **594** |
| `redes sociales` | 196 | **245** |
| `ciberacoso` | 12 | **18** |
| `trabajo doméstico` | 4 | **10** |
| `soborno` | 3 | 3 |
| `hostigamiento` | 106 | 106 |

Los dos últimos no se mueven, y se dejan a la vista: la capa nueva cubre 18 instrumentos concretos,
no el corpus entero, y un término ajeno a ellos no gana nada.

**La cobertura del lote prioritario sigue siendo 43 020/55 895.** Son otros instrumentos y otro
grado de promesa; sumarlos inflaría una cifra que mide otra cosa.

---

## 5 · Un defecto propio, medido y corregido antes de publicar

La primera versión del crosswalk contaba la cobertura **por clave de variable** y no **por
variable**. Como cada variable genera varias claves (plegada y sin sufijo de ola), el denominador se
duplicaba: ENASEM 2018 salía con cobertura **0.50** —bajo el umbral— cuando la verdadera es
**0.99**, y **nueve tablas** caían al residual por aritmética propia, no por falta de evidencia.

También se corrigieron, antes de publicar, dos cosas más de la primera versión: `FD-DECLARA`
fundía en un solo rótulo la declaración interna del FD y el simple parecido de títulos (ahora son
`FD-DECLARA-TABLA` y `FD-NOMBRE-DE-HOJA`, y la primera gana), y 150 filas cuyo «miembro» es el
propio descriptor entraban como emparejamientos válidos consigo mismas.

Los tres casos quedan como falsadores en `tests/test_crosswalk_tablas_fd.py`.

---

## 6 · Desviaciones declaradas

### 6.1 · `origin/main` se movió: `ADR-524` lo tomó otro acto

Al arrancar, `tools/cierre_acto.py` daba candidato **524**. Durante la faena entraron `PR #807`,
`#808` y `#809`; `GEN2-PINS-REPRODUCE-1` fusionó primero y se quedó con `ADR-524`. Este acto
**renumeró a `ADR-525`** —regla de la casa, renumera quien fusiona segundo— y corrigió las dos citas
que ya lo mencionaban en `data/INFRAESTRUCTURA-v1_0.md`. La cabecera del encargo archivado
**no se editó** (A.3 verbatim): dice `9fd59d0` y `ADR real 523` porque eso era verdad al redactarlo.

También se movieron las cifras de la cabecera: `NC` máxima era `NC-0252` al arrancar y `NC-0256` al
cerrar, por lo que las filas nuevas de este acto son `NC-0257`/`0258`/`0259`. Hay al menos tres
ramas más en vuelo (`claude/nube-acto-gen2-cierres-mxbm65`,
`claude/nube-acto-gen2-e1-design-yee31q`, `adq/2026-09-16-gen2-38-investigacion`): si alguna fusiona
antes, renumera este PR.

### 6.2 · «Sin archivo común» con el acto hermano: verificado, no supuesto

`GEN2-F6-PANEL-CAJA-1` tiene abiertos `data/reactivos-contexto-fuentes-v1_0.tsv` y
`data/reactivos-contexto-verificados-v1_0.tsv`, que son **salidas por defecto** del tool que este
acto extiende:

```
$ git diff --name-only origin/main...origin/acto/gen2-f6-panel-caja-1
canon/gobernanza-v1_15.md · data/reactivos-contexto-fuentes-v1_0.tsv
data/reactivos-contexto-verificados-v1_0.tsv · forense/encargos/2026-09-15-GEN2-F6-PANEL-CAJA-1.md
forense/no-corrido.tsv · forense/notas/2026-09-15-GEN2-F6-PANEL-CAJA-1-cierre.md
forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv
```

Por eso la extensión escribe en rutas **propias** (`-fd26-`) y `--fuentes` se hizo repetible en vez
de editar la tabla histórica. Los tres archivos de cascada que sí son comunes
(`canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_13.md`, `forense/no-corrido.tsv`) se
resolverán con la convención de la casa si chocan: entrada de `origin` primero, la propia después,
verbatim.

### 6.3 · Suite: local ROJO, CI VERDE — y la cifra **no** se corrigió

Medido tres veces, en este orden, y las tres cifras se dejan a la vista porque la diferencia
entre ellas **es** el hallazgo:

```
# (1) árbol SIN los cambios de este acto, sobre origin/main 9fd59d0, worktree limpio aparte
  4 FAIL · 4358 WARN   ·  T16 rojo  ·  LÍNEA BASE ROJO
# — y CI sobre ese mismo main daba otra cifra: el T16 ya venía heredado, no lo trajo este acto.

# (2) árbol CON toda la cascada de este acto, worktree de CAJA tal cual
$ python3 tests/check.py --baseline
  4 FAIL · 4356 WARN  ·  T16 rojo  ·  LÍNEA BASE ROJO

# (3) el MISMO árbol, con el único archivo gitignorado movido a un lado (control positivo)
$ mv data/raices.local.yaml $TMPDIR/ && python3 tests/check.py --baseline
  3 FAIL · 4357 WARN  ·  LÍNEA BASE VERDE — nada nuevo frente a tests/baseline.json
$ mv $TMPDIR/raices.local.yaml data/                                        # restaurado, 514 bytes
```

**(3) es la cifra declarada en `ADR-525`**, porque es la que CI medirá.

**Diagnóstico.** `data/raices.local.yaml` está **gitignorado** (`grep data/raices .gitignore`), se
copia a mano en cada worktree de CAJA y **no existe en CI**. `T03` avisa cuando un `.md` cita un
`.md`/`.yaml` ausente del árbol, y dos notas de cierre lo citan entre comillas invertidas
(`2026-09-14-GEN2-LOTE-MEDICION-PENDIENTE-1-cierre.md:12` y
`2026-09-15-GEN2-MEDICION-DEMANDA-1-cierre.md:13`). Su presencia **suprime** ese WARN, así que la
caja mide uno menos que CI.

**Control cruzado contra CI, no contra una suposición.** El último run de CI sobre `main`
(`run 35065438470`, `05977ef`) reporta **`3 FAIL · 4356 WARN` · LÍNEA BASE VERDE**. El control
positivo (3) reprodujo esa cifra **exactamente** sobre este mismo árbol antes de escribir la
cascada, y da `4357` después — el `+1` es la fila `ABIERTA` neta que esta cascada añade a
`forense/no-corrido.tsv` (3 nuevas − 2 cerradas), no una entrada de test nueva. **LÍNEA BASE VERDE
en las dos**: este acto no añade ni una entrada nueva frente a `tests/baseline.json`.

Es el simétrico del defecto que `ADR-520`/`523`/`524` ya pagaron tres veces (sandbox **sin**
`jsonschema` → un WARN de **más**): aquí es un archivo gitignorado **presente** → un WARN de
**menos**. **La cifra vigente se declaró con la del control (`4357`), no con la de la caja (`4356`)**:
declarar la de la caja habría puesto CI en rojo, que es justo el defecto que `T16` existe para
atrapar. La cifra de `ADR-524` se marcó `{cita-historica}` en vez de corregirse — mismo patrón que
`ADR-524` aplicó a la de `ADR-523`. Queda como fila para quien decida si `T03` debe
ignorar los archivos gitignorados (`NC` no abierta: es un defecto de la suite, no de este perímetro
— se anota en `forense/hallazgos.md`).

**Test propio:** `python3 -m unittest tests.test_crosswalk_tablas_fd` → **28/28 OK**, incluidos los
tres falsadores del §5 y el de que `contexto_fd26` no entre en `vigente`.

---

## 7 · Contador y anti-PR#77

**Contador científico: cero.** Ninguna corrida, ningún `RESULT`, ninguna adopción, ningún parámetro,
cero llamadas a modelo, cero descargas, **cero microdato abierto**: el crosswalk abrió **37**
descriptores `xlsx`/`xls` y el extractor **30** fuentes (21 `xlsx` + 3 `xls` + 6 `pdf`); un
descriptor no es microdato. `N_corridas_selladas`,
`N_resultados_activos`, `adoptados_activos` y la cobertura del lote (43 020/55 895) quedan
**exactamente** como estaban.

**Anti-PR#77:** no aplica — este acto no descargó nada. Los 37 descriptores leídos ya estaban en el
corpus compartido (`/home/pc0/mm-corpus/raw`), citado por el censo de raíz del día.

**ADR-46 · contaminación.** Esta sesión leyó **estructura** (descriptores de archivo, índices de
hojas, listas de variables) de los 26 instrumentos del perímetro. Se declara por si alguna sesión
futura quisiera pre-registrar hipótesis ciegas contra ellos: ésta ya no puede.

---

## 8 · Qué queda abierto

- **`NC-0257`** — la adquisición de los 55 grupos `REQUIERE-FD-EN-CORPUS` (92 941 filas), la otra
  mitad del sucesor de `NC-0235`. El cableado que este acto publicó es lo que las hará utilizables
  el día que su FD entre a la raíz; la adquisición es el único paso que falta.
- **`NC-0258`** — las 190 filas `IDENTIDAD-INSUFICIENTE`. No se publicaron a propósito.
- **`NC-0259`** — `data/reactivos-ciegos-81-v1_0.tsv` sigue contando como ciegas las 2 368 filas que
  este acto acreditó como sin enunciado posible. Ese censo está fuera del perímetro declarado.
- **`NC-0136`** sigue `ABIERTA`. **`NC-0202`** no se tocó: la tomó el servicio en
  `adq/2026-09-15-nc-0202` (`PR #805`).
