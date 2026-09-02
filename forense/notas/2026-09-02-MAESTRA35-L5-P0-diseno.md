# ACTO MAESTRA35-L5 · R-DIN-M-01 — P0: ceguera, payloads y DISEÑO congelado

Fecha: 2/sep/2026. Ejecutor: sesión ciega (ADR-46) en UBUNTU, worktree propio
`mm-maestra35-l5`, rama `claude/maestra35-l5-r-din-m-01`.
Encargo archivado por A.3: `forense/encargos/2026-09-02-MAESTRA35-L5-R-DIN-M-01.md`.
SHA de redacción declarado por dirección: `792b7ef`. Base real de este worktree:
`4d7bd1e` (merge PR #474) — `main` se movió hacia adelante entre la redacción y el
lanzamiento; no es PARO (D-10/§1.2), se re-deriva el perímetro al cerrar.

Este commit se escribe **antes de computar nada**. Ninguna cifra de desenlace
aparece aquí.

---

## §0 · ARRANQUE (D-10 §1), salidas crudas

1 · REPO. `/home/pc0/mm-maestra35-l5` (worktree creado con
`git worktree add`, no un clon nuevo).
`git log -1 --format="%h %s"` → `4d7bd1e Merge pull request #474 from Josanoforo/claude/maestra35-n2-launch-jip2j0`.
`git status --porcelain | wc -l` → `0` al arrancar.

2 · SHA. `git merge-base --is-ancestor 792b7ef HEAD` → exit 0.
`git log --oneline 792b7ef..HEAD | wc -l` → 26 commits (PR #471–#478 y sus merges).

3 · data/raw. **La enlacé.** El worktree nace sin ella (raíz integrada,
gitignorada). `ln -s /home/pc0/Modelado-Mexicano/data/raw data/raw`
→ `data/raw -> /home/pc0/Modelado-Mexicano/data/raw -> /home/pc0/mm-corpus/raw`.
Este acto **no descarga nada**: no aplica la guardia anti-PR#77.

4 · ENTORNO — tres partes (A.2):
- `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → `sin_variable` (esperado: Ubuntu).
- `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`.
- Tercera parte: `ls data/raw/ | head -1` → `2005trim1_csv.zip`; `ls data/raw/ | wc -l` → `370`.
  Corpus compartido **montado**.
- Dependencia declarada por el encargo: `python3 -c "import pyreadstat"` → OK,
  **pyreadstat 1.3.6 ya instalado** (con pandas 2.3.3). **No hice `pip install`**;
  se confirma lo que MAESTRA34-L2 §4 reportó.

5 · ESPEJO. No se usó. Toda cifra de esta nota sale del worktree de (1).

## §0-bis · COMPUERTA (D-10 §2) — verificación POR PRODUCTO

```
$ git fetch origin main
$ git cat-file -e origin/main:forense/prereg-duelo-v2/corridas-M/M-DIN-M-01__v1_2.json
$ echo $?
0
$ git ls-tree -l origin/main forense/prereg-duelo-v2/corridas-M/M-DIN-M-01__v1_2.json
100644 blob ba74d52df9d1c30a7c0391702b6276437cc68689    3457	forense/prereg-duelo-v2/corridas-M/M-DIN-M-01__v1_2.json
$ git log --oneline --diff-filter=A -- forense/prereg-duelo-v2/corridas-M/M-DIN-M-01__v1_2.json
67c9238 P2 (MAESTRA35-N2): emite M-DIN-M-01__v1_2.json
```

**COMPUERTA CUMPLIDA.** Se verificó **existencia**, nunca contenido: el archivo
está en la lista ciega y no se abrió. `git cat-file -e` no imprime el blob.

---

## §1 · (a) Hash de la proyección ciega y control de ceguera

```
$ ls -l forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv
-rw-r--r-- 1 pc0 pc0 4563 Sep  2 16:33 forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv
$ sha256sum forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv
b2dacd8a4f66ccb29eb97e448c2d0e9cf1b70002669d0c5770a49def061beb53  forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv
```

**Control de ceguera** (el que `FP-243`/`ADR-292` motivan: el marco sorteado
incrusta la `p` del motor en la columna de prosa `razon_DD`; la proyección ciega
es el insumo obligatorio precisamente porque no la lleva). Aplicado a la
proyección completa **y** a la fila `DIN-M-01` de la codificación, con las cifras
enmascaradas y **con control positivo** — un negativo cuyo comando no examinó
nada no es un negativo (A.13, y la regla de la casa sobre `xargs -0 command grep`):

```
=== CONTROL DE CEGUERA (L2 / FP-243) — cifras enmascaradas ===

(i) forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv
    archivos examinados: 1 · lineas examinadas: 15
    columnas: 14 -> ['id', 'encuesta', 'ola', 'universo', 'variable', 'estimador', 'ponderador', 'escala', 'cv_arbitro', 'n_no_ponderado', 'dominio', 'en_corpus', 'elegible', 'elegible_v1_1']
    'razon_DD' en la cabecera: False   (FP-243: es la columna que incrusta la p del motor)
    aciertos patron-decimal: 0   aciertos patron-token: 0

(ii) forense/prereg-duelo-v2/codificacion-R-v1_0.tsv — solo la fila 'DIN-M-01\t'
    archivos examinados: 1 · lineas examinadas: 37 · filas seleccionadas: 1
    aciertos patron-decimal: 0   aciertos patron-token: 0
    ENMASCARADA (fila entera, todo digito -> '#'):
      DIN-M-##	ennvih#_####_hogar_dta	ehh##dta_all/ehh##dta_b#b/iiib_cr.dta	cr##	y=# si cr##=='#' (Si); y=# si=='#' (No); # y # (no sabe / no responde) fuera	##### filas del libro #B (seccion CR) de ENNViH-# ####; cr## tiene etiqueta 'TIENE AHORROS' con #### en '#', ##### en '#', ## en '#' y # nulos; sin filtro adicional	fac_#b (NO esta en esta tabla: vive en ehh##w_all/ehh##w_b#b.dta, JOIN por folio+ls ...

(iii) CONTROL POSITIVO — misma regex, cadena sintetica que SI contamina
    aciertos patron-decimal: 1   aciertos patron-token: 2
    (si estos dos fueran 0, la regex no examina nada y el negativo de arriba no valdria)

VEREDICTO: CEGUERA INTACTA (esperado 0, obtenido 0, con control positivo que dispara)
=== EXITCODE=0 ===
```

Patrones: decimal `(?<![\d.])0\.\d{2,}|(?<![\d.])1\.0{2,}(?![\d])|\d[eE][-+]\d`;
token `razon_DD|\bp\s*=|\bp_dd\b|\bz\s*=|\bIC9[05]\b|posterior|verosimil` (case-insensitive).

**Esperado 0, obtenido 0.**

### Declaración de lecturas (ADR-46) — se sobre-declara, no se minimiza

Lo que esta sesión abrió del lado prohibido/limitado, con su alcance exacto:

- `codificacion-R-v1_0.tsv`: además del `grep -P '^DIN-M-01\t'` que el encargo
  autoriza, corrí **`cut -f1,11,12`** (id, estado, fecha) sobre el archivo entero,
  para derivar la convención del campo `estado` antes de escribir `DIN-M-01b`.
  Esas tres columnas no contienen ninguna cifra de desenlace ni del motor; la
  salida se conserva en este commit sólo como el hecho de que existen los estados
  `DERIVADA`, `PROPUESTA` y `SUSTITUYE-A <id>`. **Es una lectura más amplia que la
  que el encargo autorizó y se declara como tal**, no se esconde.
- `corridas-R/*.json`: se leyeron por la vía de `tools/arbitra.py --regresion`
  (§P1), que imprime R y EE de celdas ajenas. Son valores del lado **R**, no del
  motor; la ceguera que este acto protege es contra `M`/`L`/`p`/`z`.
- **NO** se abrió: `marco-M-*`, `canon/gobernanza*`, `canon/estado-programa*`,
  `milpa/`, `corridas-M/` (incluido `M-DIN-M-01__v1_2.json`), `corridas-L/`,
  `scoreboard*`, `L-extraido*`, ni encargos/notas de MAESTRA34-L1/L5/N1/N4/N9 ni
  de MAESTRA35-N1/L1/L2/N2/N3/N4. En particular **no** se abrió
  `forense/prereg-duelo-v2/notas-arbitra/2026-09-01-lote-fam-m-05-06-07-din-m-01.md`,
  que es de MAESTRA35-L2 y nombra esta misma celda: aparece en un `ls` y ahí se quedó.

## §2 · (b) Verificación de los dos payloads (A.1: una invocación por id)

```
$ python3 tests/manifiesto.py --verifica --id ennvih1_2002_hogar_dta
Entorno de verificación: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4

ennvih1_2002_hogar_dta [data_raw]: COINCIDE -- sha256 y tamaño (17534918 bytes) verificados contra data/manifiesto.yaml

Por raíz (sin colapsar):
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
[exit 0]

$ python3 tests/manifiesto.py --verifica --id ennvih1_2002_ponderador
Entorno de verificación: Linux 6.18.33.2-microsoft-standard-WSL2 (x86_64) · Python 3.14.4

ennvih1_2002_ponderador [data_raw]: COINCIDE -- sha256 y tamaño (755310 bytes) verificados contra data/manifiesto.yaml

Por raíz (sin colapsar):
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
[exit 0]
```

Ambos **COINCIDE**. (Las dos corridas imprimen además el bloque estándar
«Procedencia derivada, NO confirmada por el autor: 149 entrada(s) de 1039», que
es del manifiesto completo y no de estos dos ids.)

## §3 · (c) DISEÑO — congelado aquí, no se cambia después de ver R

### 3.1 · Lo que dice el PDF de diseño (prosa)

`data/raw/ennvih_diseno/ennvih-1_muestra.pdf` (56 225 bytes, 16 págs.,
«DISEÑO MUESTRAL — ENNViH Línea Basal (2002)», INEGI, Dirección de Diseño y
Marcos Estadísticos, 2004):

- p. 2: «El diseño de la muestra para la ENNViH-1 se caracteriza por ser
  probabilístico… A su vez el diseño es **polietápico, estratificado y por
  conglomerados**, donde la **unidad última de selección es la vivienda** y la
  unidad de observación es el hogar.» Marco muestral: el de la ENE.
- p. 3 (§4.1.2): «Las **UPM's se clasifican en 3 estratos; alto, medio y bajo**,
  con base a las siguientes variables captadas durante el levantamiento de la
  Encuesta Nacional de Empleo (ENE) del 2do. trimestre del 2001» — 14 indicadores
  socioeconómicos.
- p. 9–10 (§8.1): «Dentro de cada entidad y estrato se seleccionaron n_rh **UPM**
  con probabilidad proporcional al tamaño»; «N_reh = Es el número total de **UPM**
  en el h-ésimo estrato, de la e-ésima entidad, de la r-ésima región.»

Segundo documento: `data/raw/ennvih_diseno/calculo-de-factores-de-expansion.pdf`
(337 947 bytes, 11 págs.): muestreo trietápico (ENEU) / bietápico (resto),
ajuste por no respuesta, proyección CONAPO-INEGI y calibración
(raking ratio, Deville-Särndal 1992).

**Consecuencia leída del PDF, no supuesta:** el estrato de diseño (alto/medio/bajo,
construido con 14 indicadores de la ENE 2001) y la UPM **no se publican como
variables del microdato**. La `estrato` que sí existe en el paquete (tabla `c_ls`,
documentada en `data/raw/ennvih/guiausuariov1.pdf` y en
`data/raw/ennvih/doc/ehh02cb_bc.pdf`) es una recodificación **post-hoc por tamaño
de localidad** (1 = >100 000 hab.; 2 = 15 000–100 000; 3 = 2 500–15 000;
4 = <2 500) — **no** es el estrato de selección. Y `grep -i upm` sobre
`guiausuariov1.pdf`, `ehh02cb_bc.pdf` y `eloc02cb_bcc.pdf` da **0 aciertos en los
tres**: no hay variable de UPM en ninguna parte del paquete público.

### 3.2 · Lo que traen las dos tablas que la fila de codificación nombra (sólo NOMBRES)

Censo hecho con `pyreadstat.read_dta`, **sin imprimir ni calcular ningún valor de
`cr27`** (sólo nombre y etiqueta):

| tabla | zip | miembro | filas | cols |
|---|---|---|---|---|
| desenlace | `data/raw/ennvih/ehh02dta_all.zip` | `ehh02dta_all/ehh02dta_b3b/iiib_cr.dta` | **19 802** | 49 |
| ponderador | `data/raw/ennvih/ehh02w_all.zip` | `ehh02w_all/ehh02w_b3b.dta` | 35 677 | 3 |

- `iiib_cr.dta`: 47 columnas `cr*` (entre ellas `cr27 | TIENE AHORROS`) **más
  exactamente dos** identificadores: `folio | IDENTIFICADOR DEL HOGAR` y
  `ls | IDENTIFICADOR INDIVIDUAL`. **Nada** de `fac_*`, `estrato`, `upm`, `psu`,
  `cluster`, `ent`, `mpio`, `loc`, `id_loc`, tamaño de localidad.
- `ehh02w_b3b.dta`: exactamente `folio`, `ls`, `fac_3b | FACTOR DE EXPANSIÓN LIBRO 3B`.
  **Nada** de estrato, UPM, entidad, municipio ni localidad.
- Corrección de una lectura que el nombre invita a hacer mal: **`ls` NO es
  localidad ni segmento** — su etiqueta es `IDENTIFICADOR INDIVIDUAL` y su rango
  es 1–16 en la tabla de desenlace (1–17 en la de ponderadores). Es la línea de
  la persona dentro del hogar. Quien lea «JOIN por folio+ls» como un join
  hogar×localidad estará leyendo mal: es un join **persona-libro**.
- Unicidad de la llave: 19 802 filas / 19 802 combinaciones `folio+ls` distintas
  en el desenlace; 35 677 / 35 677 en ponderadores. **`folio+ls` es llave única en
  ambas.** `folio` distintos: 8 059 (desenlace) vs. 8 440 (ponderadores) — el
  archivo de pesos cubre más hogares/individuos que los que contestaron la sección CR.

### 3.3 · La rama del encargo que aplica, y por qué

El encargo congela dos ramas: (i) si hay identificadores de entidad y
localidad/UPM **en la tabla o en el archivo de ponderadores**, entonces
estrato = entidad y UPM = localidad; (ii) si no existen, **DISENO-APROXIMADO**.

**No existen en ninguna de las dos.** Aplica la rama (ii).

**DISEÑO CONGELADO:**

- **UPM = `folio`** (el hogar), tal como la rama (ii) del encargo lo fija.
- **estrato = CONSTANTE (un solo estrato).** Aquí me aparto de la letra de la
  rama (ii), que dice «estrato = entidad», y digo por qué en vez de forzarlo:
  **`entidad` no existe en ninguna de las dos tablas autorizadas.** La variable
  `ent` vive en `c_ls`, una **tercera** tabla del paquete que la fila de
  codificación no nombra; traerla exigiría un **segundo** join no congelado por
  el encargo, y el encargo mismo ordena parar antes de salirse de lo calculado.
  Un solo estrato es la lectura honesta de «no existen»: es lo que la rama (ii)
  produce cuando su propio antecedente tampoco se cumple.
- **`fac_3b`** como ponderador, traído por JOIN 1:1 `folio+ls` desde
  `ehh02w_all/ehh02w_b3b.dta` (gramática formalizada en §P1).

**RESERVA declarada (lo que esta EE no mide):** `EE_R` bajo este diseño es una
**cota inferior** de la EE verdadera, por dos vías que no se compensan:

1. La UPM real es un **conglomerado de viviendas** seleccionado con probabilidad
   proporcional al tamaño (PDF §8.1). Tomar el **hogar** como UPM trata como
   independientes hogares que la muestra eligió en racimo: se pierde
   precisamente la covarianza intra-conglomerado, que es positiva en encuestas de
   hogares. Esto **subestima** la varianza, y es el término dominante.
2. Con un solo estrato se pierde la ganancia de la estratificación. Este segundo
   efecto empuja en dirección contraria (sobreestima), pero es de segundo orden
   frente a (1) y **no** lo cancela.

Por eso se reporta **también `EE_R_sin_diseno`**: un solo estrato y **una UPM por
fila** (persona), que por la nota §2 de `tests/svystat.py` colapsa exactamente a
la varianza ponderada tipo SRS, `p(1-p)/(n-1)`. Las dos cifras acotan por abajo:
ninguna de las dos es la EE de diseño completo, que **este microdato público no
permite calcular**. Esa es la afirmación fuerte de esta nota, y sale del PDF y
del censo de columnas, no de una preferencia del ejecutor.

**Esta elección queda congelada en este commit y no se cambia después de ver R.**

---

## §4 · Lo que este commit NO hace

No computa `R`. No abre el motor. No toca `canon/`, `milpa/`, `corridas-M/`,
`corridas-L/` ni `exclusiones-v1_2.md`. No emite `M`. No puntúa.
