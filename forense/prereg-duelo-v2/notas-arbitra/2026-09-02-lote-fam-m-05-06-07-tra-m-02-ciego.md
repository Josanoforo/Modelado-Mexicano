# Lote ciego · FAM-M-05 · FAM-M-06 · FAM-M-07 · TRA-M-02 — COMMIT-1, specs congeladas

ACTO MAESTRA35-L4 · R-v1_2-CIEGA · 2 de septiembre de 2026 · caja `/home/pc0/mm-maestra35-l4`, rama `acto/maestra35-l4-r-v1_2-ciega`, base `9cbd8d8` (`origin/main`, merge PR #485; el encargo se redactó contra `0fd6b4c`, 100 commits atrás — main se movió, no es PARO). Encargo archivado verbatim: `forense/encargos/2026-09-02-MAESTRA35-L4-R-v1_2-CIEGA.md` (commit `da20d03`).

Redactada bajo la enmienda de `/arbitra §COMMIT-1` (firma de mesa sobre FP-243, ADR-292): el insumo del lado R es la **proyección ciega**, no el marco sorteado. `marco-M-sorteado-v1_2.tsv` **no se abrió**; tampoco `canon/`, `milpa/`, `corridas-M/`, `corridas-L/`, `scoreboard*`, `L-extraido*`, ni ningún encargo o nota de los actos vetados por el encargo. Sesión nueva (ADR-46), sin haber visto M ni el motor.

## §0 · Insumo y control de ceguera (P0 a, b)

**(a) sha256 del insumo** — es la prueba de que se leyó la proyección y no el marco:

```
b2dacd8a4f66ccb29eb97e448c2d0e9cf1b70002669d0c5770a49def061beb53  forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv
```

(commit `db69b98`, «Proyeccion ciega del marco v1_2», PR #470.)

**(b) Control de ceguera**, repetido sobre los dos insumos que este acto abre. Barrido de cifras tipo `0.dddd+` y de pares `letra=valor` (`p`/`M`/`L`/`z`), con los valores enmascarados en el propio comando: imprime conteos por archivo y columna, nunca el valor. Esperado 0 en la proyección; 0 también en las filas de codificación (si hubiera aparecido alguna, PARO sin abrirla).

Proyección (archivo completo, 14 filas, 14 columnas):

```
archivo=forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv lineas=15 total_0.dddd=0 total_letra=val=0
columnas=14: id | encuesta | ola | universo | variable | estimador | ponderador | escala | cv_arbitro | n_no_ponderado | dominio | en_corpus | elegible | elegible_v1_1
  col[0] id: 0.dddd=0 letra=val=0
  col[1] encuesta: 0.dddd=0 letra=val=0
  col[2] ola: 0.dddd=0 letra=val=0
  col[3] universo: 0.dddd=0 letra=val=0
  col[4] variable: 0.dddd=0 letra=val=0
  col[5] estimador: 0.dddd=0 letra=val=0
  col[6] ponderador: 0.dddd=0 letra=val=0
  col[7] escala: 0.dddd=0 letra=val=0
  col[8] cv_arbitro: 0.dddd=0 letra=val=0
  col[9] n_no_ponderado: 0.dddd=0 letra=val=0
  col[10] dominio: 0.dddd=0 letra=val=0
  col[11] en_corpus: 0.dddd=0 letra=val=0
  col[12] elegible: 0.dddd=0 letra=val=0
  col[13] elegible_v1_1: 0.dddd=0 letra=val=0
  filas_con_ncols_distinto=0 []
```

Cabecera (línea 1) + las cuatro filas de `codificacion-R-v1_0.tsv` obtenidas por `grep -P '^(FAM-M-0[567]|TRA-M-02)\t'`, ya con la fila `TRA-M-02` de este acto anexada:

```
archivo=- lineas=5 total_0.dddd=0 total_letra=val=0
columnas=12: #id | payload_id | tabla | variable | codificacion | universo_filtro | ponderador | estrato | upm | fuente | estado | fecha
  col[0] #id: 0.dddd=0 letra=val=0
  col[1] payload_id: 0.dddd=0 letra=val=0
  col[2] tabla: 0.dddd=0 letra=val=0
  col[3] variable: 0.dddd=0 letra=val=0
  col[4] codificacion: 0.dddd=0 letra=val=0
  col[5] universo_filtro: 0.dddd=0 letra=val=0
  col[6] ponderador: 0.dddd=0 letra=val=0
  col[7] estrato: 0.dddd=0 letra=val=0
  col[8] upm: 0.dddd=0 letra=val=0
  col[9] fuente: 0.dddd=0 letra=val=0
  col[10] estado: 0.dddd=0 letra=val=0
  col[11] fecha: 0.dddd=0 letra=val=0
  filas_con_ncols_distinto=0 []
```

Ambos: **0** cifras. Además, sobre `codificacion-R-v1_0.tsv` esta sesión leyó, aparte de esas cuatro filas, **sólo** la línea 1 (cabecera, para escribir una fila bien formada) y las columnas `#id`, `estado` y `fecha` de todas las filas (para conocer la convención de estado: ninguna fila del archivo lleva `COMPUTADA` salvo `DIN-M-01b`, cuyo estado es `SUSTITUYE-A DIN-M-01 · COMPUTADA (ACTO MAESTRA35-L5)`); las tres columnas pasaron el mismo barrido con 0 cifras. Ninguna otra columna de ninguna otra fila fue leída.

Declaración adicional (declarar más, no menos): el índice de memoria del ejecutor, que el cliente carga automáticamente al arrancar, contiene una cifra `p` del acto MAESTRA33-C1 (corresidencia, `RE-SPEC`), ajena a las cuatro celdas de este lote y al sorteado v1_2. Ninguna cifra de motor de `FAM-M-05`, `FAM-M-06`, `FAM-M-07` ni `TRA-M-02` ha sido vista por esta sesión al momento de este commit. Las notas de memoria propias que se consultaron se barrieron antes con el mismo detector y se abrieron sólo las que dieron 0 (incluida la nota propia sobre MAESTRA35-L2: 0 cifras); las que dieron >0 no se abrieron.

## §1 · Las cuatro filas de `espec-R-ciega-v1_2.tsv`, verbatim (cabecera + filas, TSV)

```tsv
id	encuesta	ola	universo	variable	estimador	ponderador	escala	cv_arbitro	n_no_ponderado	dominio	en_corpus	elegible	elegible_v1_1
FAM-M-05	ENIGH	2016	hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2016 Nueva Serie, sin filtro adicional. Desenlace recibe_remesas = 1 si concentradohogar.remesas > 0, 0 si = 0; la rama NA de la dicotomizacion no existe (`remesas` trae cero nulos en las 6 olas, verificado, no supuesto).	remesas	proporcion ponderada (declarado por la regla; NO estimado en este acto)	factor	binaria	remesas	70311	familia	SI	SI	SI
FAM-M-06	ENIGH	2018	hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2018 Nueva Serie, sin filtro adicional. Desenlace recibe_remesas = 1 si concentradohogar.remesas > 0, 0 si = 0; la rama NA de la dicotomizacion no existe (`remesas` trae cero nulos en las 6 olas, verificado, no supuesto).	remesas	proporcion ponderada (declarado por la regla; NO estimado en este acto)	factor	binaria	remesas	74647	familia	SI	SI	SI
FAM-M-07	ENIGH	2020	hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2020 Nueva Serie, sin filtro adicional. Desenlace recibe_remesas = 1 si concentradohogar.remesas > 0, 0 si = 0; la rama NA de la dicotomizacion no existe (`remesas` trae cero nulos en las 6 olas, verificado, no supuesto).	remesas	proporcion ponderada (declarado por la regla; NO estimado en este acto)	factor	binaria	remesas	89006	familia	SI	SI	SI
TRA-M-02	ENCUCI	2020	universo con contacto AP5_16_1..10, ENCUCI 2020 SEC_4_5, 21519 filas, n útil 13375/13393/13365 de 13435 con contacto	AP5_17|AP5_18	proporción ponderada	FAC_SEL	binaria	AP5_1_1/AP5_1_2/AP5_1_3		tramite	SI	SI	SI
```

## §2 · Las cuatro codificaciones, tal como están en `codificacion-R-v1_0.tsv` (cabecera + `grep`, TSV)

```tsv
#id	payload_id	tabla	variable	codificacion	universo_filtro	ponderador	estrato	upm	fuente	estado	fecha
FAM-M-05	enigh2016_nc_csv	conjunto_de_datos_concentradohogar_enigh_2016_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh_2016_ns.csv	remesas	y=1 si remesas > 0; y=0 si remesas == 0 -- UMBRAL NUMERICO, no conjunto de codigos: remesas es monto continuo en pesos con 1313 valores distintos en 2016	hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2016 Nueva Serie, sin filtro adicional (asi lo declara el marco v1_2); 70311 filas leidas, 0 vacios en remesas	factor	est_dis	upm	verificado LEYENDO el CSV de datos (70311 filas): remesas PRESENTE con 1313 valores distintos (66183 en cero, 4128 positivos, 0 vacios); factor, est_dis y upm PRESENTES, upm_dis AUSENTE. BLOQUEO: la dicotomizacion es un UMBRAL (>0) y arbitra.py solo acepta conjuntos literales (_PATRON_BINARIO / _PATRON_BINARIO_SET), asi que parsea_codificacion_binaria devuelve None y la celda sale NO-EJECUTABLE en vez de dar un numero equivocado; estima() compara pertenencia a conjunto, no orden	PROPUESTA	2026-09-01
FAM-M-06	enigh2018_nc_csv	conjunto_de_datos_concentradohogar_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh_2018_ns.csv	remesas	y=1 si remesas > 0; y=0 si remesas == 0 -- UMBRAL NUMERICO, no conjunto de codigos: remesas es monto continuo en pesos con 1424 valores distintos en 2018	hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2018 Nueva Serie, sin filtro adicional (asi lo declara el marco v1_2); 74647 filas leidas, 0 vacios en remesas	factor	est_dis	upm	verificado LEYENDO el CSV de datos (74647 filas): remesas PRESENTE con 1424 valores distintos (70063 en cero, 4584 positivos, 0 vacios); factor, est_dis y upm PRESENTES, upm_dis AUSENTE. BLOQUEO: la dicotomizacion es un UMBRAL (>0) y arbitra.py solo acepta conjuntos literales (_PATRON_BINARIO / _PATRON_BINARIO_SET), asi que parsea_codificacion_binaria devuelve None y la celda sale NO-EJECUTABLE en vez de dar un numero equivocado; estima() compara pertenencia a conjunto, no orden	PROPUESTA	2026-09-01
FAM-M-07	enigh2020_nc_csv	conjunto_de_datos_concentradohogar_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh_2020_ns.csv	remesas	y=1 si remesas > 0; y=0 si remesas == 0 -- UMBRAL NUMERICO, no conjunto de codigos: remesas es monto continuo en pesos con 1389 valores distintos en 2020	hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2020 Nueva Serie, sin filtro adicional (asi lo declara el marco v1_2); 89006 filas leidas, 0 vacios en remesas	factor	est_dis	upm	verificado LEYENDO el CSV de datos (89006 filas): remesas PRESENTE con 1389 valores distintos (83766 en cero, 5240 positivos, 0 vacios); factor, est_dis y upm PRESENTES, upm_dis AUSENTE. BLOQUEO: la dicotomizacion es un UMBRAL (>0) y arbitra.py solo acepta conjuntos literales (_PATRON_BINARIO / _PATRON_BINARIO_SET), asi que parsea_codificacion_binaria devuelve None y la celda sale NO-EJECUTABLE en vez de dar un numero equivocado; estima() compara pertenencia a conjunto, no orden	PROPUESTA	2026-09-01
TRA-M-02	encuci2020_bd_dbf	SEC_4_5	AP5_17|AP5_18	y=1 si AP5_17=='1' o AP5_18=='1'; y=0 si AP5_17=='2' y AP5_18=='2' -- COMPUESTO OR de dos variables (_PATRON_COMPUESTO_OR); resto FUERA (cae en n_codigo_no_valido, no se reclasifica): 9 = No sabe/no responde, b = blanco (salto del cuestionario) y cualquier otra combinacion; codigos verificados en el FD (AP5_17 y AP5_18: 1 Si, 2 No, 9 No sabe/no responde, b blanco)	persona seleccionada (informante de 15 anios y mas, tabla SEC_4_5) con contacto en los ultimos 12 meses = alguna de AP5_16_1..AP5_16_10 == '1' (codigos del FD: 1 Si, 2 No, 9 No sabe/no responde); 21519 filas leidas y 13435 con contacto segun la proyeccion ciega (guardias: se reportan, no se ajustan). El filtro NO se ejecuta como codigo (limite declarado de arbitra.py): lo aplica el salto del cuestionario -- sin contacto AP5_17/AP5_18 van en blanco y caen FUERA por la codificacion	FAC_SEL	EST_DIS	UPM_DIS	espec-R-ciega-v1_2.tsv (sha256 b2dacd8a4f66ccb29eb97e448c2d0e9cf1b70002669d0c5770a49def061beb53) + FD encuci2020_fd_pdf (manifiesto:1022), payload encuci2020_bd_dbf (manifiesto:992); tabla logica SEC_4_5 = unico miembro ENCUCI_2020_SEC_4_5.dbf del zip (listado de nombres, sin abrir datos); FAC_SEL (Numerico 1-999999), EST_DIS (Caracter 001-999) y UPM_DIS (Caracter 0000001-9999999) en la seccion de diseno muestral de SEC_4_5 del FD; escrita sin abrir el marco ni ningun otro archivo del lado M	PROPUESTA (ACTO MAESTRA35-L4)	2026-09-02
```

- `FAM-M-05`, `FAM-M-06`, `FAM-M-07`: filas `PROPUESTA` del 2026-09-01, EXISTE-SATISFACE; **no se editan**. Codificación de umbral («y=1 si remesas > 0; y=0 si remesas == 0») que `_PATRON_UMBRAL` (reparado en MAESTRA35-L2/P1) calza.
- `TRA-M-02`: fila **nueva** de este acto (P0 c), escrita desde la proyección y el FD `FD_ENCUCI2020.pdf` (`encuci2020_fd_pdf`, manifiesto:1022) sin abrir nada más. Verificado en el FD, sección `ENCUCI_2020_SEC_4_5`: `AP5_16_1`…`AP5_16_10` Numérico con códigos 1 Sí, 2 No, 9 No sabe/no responde; `AP5_17` y `AP5_18` Numérico con códigos 1 Sí, 2 No, 9 No sabe/no responde, b blanco; `FAC_SEL` Numérico 1-999999 (ponderador del informante seleccionado), `EST_DIS` Caracter 001-999 (estrato de diseño; **no** `ESTRATO` 1-4, que es socioeconómico), `UPM_DIS` Caracter 0000001-9999999 — los tres en «Campos empleados para el diseño muestral» de `SEC_4_5`. El FD dice '1'/'2' donde el encargo lo supone; no hubo que corregir. Parser: `parsea_codificacion_binaria()` devuelve un callable por `_PATRON_COMPUESTO_OR` (y no por `_PATRON_BINARIO`, `_PATRON_BINARIO_SET` ni `_PATRON_UMBRAL`), verificado en seco sobre 12 combinaciones sintéticas de (`AP5_17`, `AP5_18`) sin tocar datos. `tabla` lógica `SEC_4_5` resuelve a un único miembro del zip (`ENCUCI_2020_SEC_4_5.dbf`, por listado de nombres). `dbfmini.read_dbf` entrega todos los campos como cadenas latin-1 con `strip`, así que '1'/'2' comparan como cadenas y el blanco queda ''.

## §3 · Guardias con valor esperado — se reportan; **no se ajustan**

| celda | guardia | esperado | de dónde sale el esperado |
|---|---|---|---|
| FAM-M-05 | `n_filas_leidas` | 70311 | fila de codificación (2026-09-01) y `n_no_ponderado` de la proyección |
| FAM-M-05 | `n_codigo_no_valido` | 0 | 0 vacíos en `remesas` (fila de codificación) |
| FAM-M-05 | y=1 / y=0 (no ponderado) | 4128 / 66183 | fila de codificación |
| FAM-M-06 | `n_filas_leidas` | 74647 | ídem |
| FAM-M-06 | `n_codigo_no_valido` | 0 | ídem |
| FAM-M-06 | y=1 / y=0 (no ponderado) | 4584 / 70063 | ídem |
| FAM-M-07 | `n_filas_leidas` | 89006 | ídem |
| FAM-M-07 | `n_codigo_no_valido` | 0 | ídem |
| FAM-M-07 | y=1 / y=0 (no ponderado) | 5240 / 83766 | ídem |
| TRA-M-02 | `n_filas_leidas` | 21519 | proyección, columna `universo` |
| TRA-M-02 | n con contacto (alguna `AP5_16_x == '1'`) | 13435 | proyección, columna `universo` |
| TRA-M-02 | `n_efectivo` | > 0 y ≤ 13435 | salto del cuestionario: sin contacto, `AP5_17`/`AP5_18` en blanco (FD: código b) |

`arbitra.py` no ejecuta `universo_filtro` (límite declarado). Para `TRA-M-02` la guardia de contacto y la tabla de valores no válidos (cuántos y qué combinaciones de `AP5_17`/`AP5_18`, sin reclasificar) se cuentan **después** de la corrida con un script auxiliar de sólo lectura que reutiliza `dbf_zip` de `corridas-R/correr-R.py`; su salida va a COMMIT-2. Si la guardia de contacto no da 13435, o si aparecen filas sin contacto con `AP5_17`/`AP5_18` en {1,2} (que la codificación contaría dentro de R), se reporta la desviación con su tamaño y no se toca nada.

## §4 · Procedimiento (P1), tal cual se correrá

```
python3 tools/arbitra.py --produce forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv FAM-M-05 FAM-M-06 FAM-M-07 TRA-M-02
```

Estimador: proporción ponderada con EE de conglomerado último (`tests/svystat.py::prop_ultimate_cluster`) vía `corridas-R/correr-R.py::estima`, ponderador/estrato/UPM de la fila de codificación; `--produce` lee de la proyección sólo `id`, `encuesta` y `ola`, y rehúsa sobreescribir un `corridas-R/<id>.json` existente. Si `--produce` exigiera el sorteado, PARO y reporte (no se abre el sorteado).

COMMIT-2 = los cuatro `corridas-R/*.json` + una fila de estado por celda en `codificacion-R-v1_0.tsv`, por append: copia íntegra de la fila de codificación con `estado` = `COMPUTADA (ACTO MAESTRA35-L4)` y `fuente`/`fecha` nuevas (las filas `PROPUESTA` no se editan; `lee_codificacion()` toma la última fila por id, así que la copia tiene que reproducir el JSON — se verifica con `--regresion` sobre las cuatro, sin escribir). Ese commit se hace **antes** de tocar canon (firma de FP-244).

> Specs congeladas para este lote, copiadas verbatim del marco citado arriba — léase, por la enmienda de FP-243, de la proyección ciega `espec-R-ciega-v1_2.tsv` cuyo sha256 encabeza esta nota —, antes de ejecutar `tools/arbitra.py`. Ninguna se edita después de este commit.

**El primer resultado que produzca este procedimiento es el que se reporta.**


---

## §5 · COMMIT-2 · resultados (P1) — escrito antes de tocar canon

Orden verificable en git: COMMIT-1 = `e96c25e`; la corrida de abajo se lanzó después de ese commit y este §5 viaja en COMMIT-2 junto con los cuatro `corridas-R/*.json` y las cuatro filas de estado. Ningún archivo de `canon/`, `marco-M-*`, `milpa/`, `corridas-M/`, `corridas-L/`, `scoreboard*` ni `L-extraido*` se ha abierto hasta aquí.

### Salida cruda de `python3 tools/arbitra.py --produce forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv FAM-M-05 FAM-M-06 FAM-M-07 TRA-M-02` (exit 0)

```
FAM-M-05: ESCRITO COMPUTADO
    R=0.04745859252351374
    advertencia: FAM-M-05: universo_filtro es informativo, NO se ejecuta como filtro ('hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2016 Nueva Serie, sin filtro adicional (asi lo declara el marco v1_2); 70311 filas leidas, 0 vacios en remesas') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
FAM-M-06: ESCRITO COMPUTADO
    R=0.04728548395278385
    advertencia: FAM-M-06: universo_filtro es informativo, NO se ejecuta como filtro ('hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2018 Nueva Serie, sin filtro adicional (asi lo declara el marco v1_2); 74647 filas leidas, 0 vacios en remesas') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
FAM-M-07: ESCRITO COMPUTADO
    R=0.04377543852935772
    advertencia: FAM-M-07: universo_filtro es informativo, NO se ejecuta como filtro ('hogares -- universo completo de concentradohogar (folioviv+foliohog) de ENIGH 2020 Nueva Serie, sin filtro adicional (asi lo declara el marco v1_2); 89006 filas leidas, 0 vacios en remesas') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
TRA-M-02: ESCRITO COMPUTADO
    R=0.12602486953090247
    advertencia: TRA-M-02: universo_filtro es informativo, NO se ejecuta como filtro ("persona seleccionada (informante de 15 anios y mas, tabla SEC_4_5) con contacto en los ultimos 12 meses = alguna de AP5_16_1..AP5_16_10 == '1' (codigos del FD: 1 Si, 2 No, 9 No sabe/no responde); 21519 filas leidas y 13435 con contacto segun la proyeccion ciega (guardias: se reportan, no se ajustan). El filtro NO se ejecuta como codigo (limite declarado de arbitra.py): lo aplica el salto del cuestionario -- sin contacto AP5_17/AP5_18 van en blanco y caen FUERA por la codificacion") -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: TRA-M-02: tabla logica 'SEC_4_5' resuelta a miembro fisico 'ENCUCI_2020_SEC_4_5.dbf' dentro de BD_ENCUCI2020_dbf.zip

real	0m5.083s
user	0m4.877s
sys	0m0.196s
```

`--produce` leyó de la proyección sólo `id`/`encuesta`/`ola`; no exigió el sorteado. Las cuatro celdas salieron `COMPUTADO` a la primera; es el primer y único resultado que produjo el procedimiento, y es el que se reporta.

### Los cuatro R (de `corridas-R/<id>.json`, redondeados aquí; el JSON trae los flotantes completos)

| celda | estado | R | EE_R | IC95 | cv % | n_filas_leidas | n_efectivo | n_codigo_no_valido | n_sin_ponderador | n_estratos | n_upm_total | singleton |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FAM-M-05 | COMPUTADO | 0.047459 | 0.001262 | [0.0450, 0.0499] | 2.66 | 70311 | 70311 | 0 | 0 | 536 | 7891 | 0 |
| FAM-M-06 | COMPUTADO | 0.047285 | 0.001195 | [0.0449, 0.0496] | 2.53 | 74647 | 74647 | 0 | 0 | 543 | 8377 | 0 |
| FAM-M-07 | COMPUTADO | 0.043775 | 0.001012 | [0.0418, 0.0458] | 2.31 | 89006 | 89006 | 0 | 0 | 558 | 10118 | 0 |
| TRA-M-02 | COMPUTADO | 0.126025 | 0.005060 | [0.1161, 0.1359] | 4.02 | 21519 | 13412 | 8107 | 0 | 281 | 3003 | 1 |

### Guardias (§3) contra lo medido — todas dentro de lo esperado; nada se ajustó

Script auxiliar de sólo lectura (reusa `csv_zip`/`dbf_zip`/`num` de `corridas-R/correr-R.py`; no escribe, no toca la spec). Corrido **después** de `--produce`.

```
## FAM-M-05 · enigh2016_nc_csv.zip
n_filas_leidas=70311 (esperado 70311) | remesas>0=4128 (esperado 4128) | remesas==0=66183 (esperado 66183) | no numerico o negativo=0 (esperado 0) 
factor nulo/<=0: 0 | est_dis vacio: 0 | upm vacio: 0
## FAM-M-06 · enigh2018_nc_csv.zip
n_filas_leidas=74647 (esperado 74647) | remesas>0=4584 (esperado 4584) | remesas==0=70063 (esperado 70063) | no numerico o negativo=0 (esperado 0) 
factor nulo/<=0: 0 | est_dis vacio: 0 | upm vacio: 0
## FAM-M-07 · enigh2020_nc_csv.zip
n_filas_leidas=89006 (esperado 89006) | remesas>0=5240 (esperado 5240) | remesas==0=83766 (esperado 83766) | no numerico o negativo=0 (esperado 0) 
factor nulo/<=0: 0 | est_dis vacio: 0 | upm vacio: 0
```

```
n_filas_leidas=21519 (esperado 21519) | n_con_contacto=13435 (esperado 13435) | n_sin_contacto=8084
valores numericos AP5_16_x (10 col x filas): {1.0: 32880, 2.0: 181601, 9.0: 709}
valores crudos AP5_17: {'': 8084, '1': 1193, '2': 12225, '9': 17} | AP5_18: {'': 8084, '1': 839, '2': 12579, '9': 17}
n_efectivo CON contacto=13412 | n_efectivo SIN contacto (entrarian en R fuera del universo)=0 | FUERA con contacto=23 | FUERA sin contacto=8084
tabla (AP5_17, AP5_18) -> n, CON contacto (-> y):
   ('1', '1'): 606  -> 1
   ('1', '2'): 586  -> 1
   ('1', '9'): 1  -> 1
   ('2', '1'): 233  -> 1
   ('2', '2'): 11986  -> 0
   ('2', '9'): 6  -> None
   ('9', '2'): 7  -> None
   ('9', '9'): 10  -> None
tabla (AP5_17, AP5_18) -> n, SIN contacto (-> y):
   ('', ''): 8084  -> None
```

Lectura: `TRA-M-02` reproduce exactamente las dos cifras de la proyección (21519 filas, 13435 con contacto). Las 8084 filas sin contacto traen `AP5_17`/`AP5_18` en blanco (salto del cuestionario, código b del FD) y caen FUERA; **ninguna** fila sin contacto entra en R, así que el universo queda aplicado por el salto aunque `arbitra.py` no ejecute `universo_filtro`. `n_codigo_no_valido` = 8107 = 8084 (sin contacto, blanco-blanco) + 23 (con contacto, código 9 «No sabe/no responde» en alguna de las dos: 6 + 7 + 10); no se reclasifica ninguna. `n_efectivo` = 13412 = 1426 (y=1: 606 + 586 + 1 + 233) + 11986 (y=0). En FAM, `n_codigo_no_valido` = 0 en las tres olas y las frecuencias de `remesas` (>0 / ==0) coinciden una a una con las que la fila de codificación del 1/sep ya publicaba.

**Declarado, no ocultado — una corrección a la guardia, no a la spec ni a la R.** La primera corrida del script auxiliar comparó `AP5_16_x` como cadena (`== '1'`) y dio `n_con_contacto = 0`: en el DBF esos diez campos son `N` de ancho 19 con **15 decimales**, y `dbfmini` entrega su texto crudo (`1.000000000000000`). Se corrigió la guardia a comparación por valor numérico (`num(v) == 1.0`) y dio 13435 exacto. La R **no** depende de `AP5_16_x` (la codificación compuesta usa sólo `AP5_17`/`AP5_18`), así que la corrección no toca ningún resultado; es exactamente el modo de falla «un lector nuevo devuelve vacío, no error» y por eso se deja escrito.

Descriptores de campo del DBF `ENCUCI_2020_SEC_4_5.dbf` (cabecera, no datos; 21519 registros, 164 campos): `AP5_17` y `AP5_18` son **`C` ancho 6** (el FD los llama «Numérico»; por eso `=='1'` compara bien y el blanco llega como `''`); `AP5_16_1`…`AP5_16_10` son `N` 19,15; `FAC_SEL` es `N` 19,10; `EST_DIS`, `UPM_DIS` y `ESTRATO` son `C` 7. Si alguna codificación futura de ENCUCI usa `AP5_16_x` con comparación de cadena, dará R vacía sin error — va como hallazgo.

### Filas de estado (append, sin editar las `PROPUESTA`) y regresión

Cuatro filas anexadas a `codificacion-R-v1_0.tsv` (`git diff --numstat` → `4 0`): copia íntegra de la fila de codificación de cada celda con `estado` = `COMPUTADA (ACTO MAESTRA35-L4)`, `fuente` nueva y `fecha` 2026-09-02. Como `lee_codificacion()` toma la última fila por id, la copia es la que responderá por la celda en adelante; `--regresion` sobre las cuatro (no escribe) confirma que reproduce el JSON:

```
FAM-M-05: COINCIDE
    R: nuevo=0.04745859252351374 == existente=0.04745859252351374
    EE_R: nuevo=0.0012623608446458148 == existente=0.0012623608446458148
    n_efectivo: nuevo=70311 == existente=70311
    n_estratos: nuevo=536 == existente=536
    n_upm_total: nuevo=7891 == existente=7891
FAM-M-06: COINCIDE
    R: nuevo=0.04728548395278385 == existente=0.04728548395278385
    EE_R: nuevo=0.0011954757147624008 == existente=0.0011954757147624008
    n_efectivo: nuevo=74647 == existente=74647
    n_estratos: nuevo=543 == existente=543
    n_upm_total: nuevo=8377 == existente=8377
FAM-M-07: COINCIDE
    R: nuevo=0.04377543852935772 == existente=0.04377543852935772
    EE_R: nuevo=0.0010115874166924878 == existente=0.0010115874166924878
    n_efectivo: nuevo=89006 == existente=89006
    n_estratos: nuevo=558 == existente=558
    n_upm_total: nuevo=10118 == existente=10118
TRA-M-02: COINCIDE
    R: nuevo=0.12602486953090247 == existente=0.12602486953090247
    EE_R: nuevo=0.005060007385450377 == existente=0.005060007385450377
    n_efectivo: nuevo=13412 == existente=13412
    n_estratos: nuevo=281 == existente=281
    n_upm_total: nuevo=3003 == existente=3003

real	0m4.927s
user	0m4.735s
sys	0m0.192s
```

### Archivos abiertos por esta sesión entre COMMIT-1 y COMMIT-2

- Datos (nivel contenido, ADR-46, declarado): `data/raw/enigh2016_nc_csv.zip`, `enigh2018_nc_csv.zip`, `enigh2020_nc_csv.zip` (los tres CSV de `concentradohogar`) y `data/raw/BD_ENCUCI2020_dbf.zip` (`ENCUCI_2020_SEC_4_5.dbf`) — por `tools/arbitra.py --produce` y `--regresion`, y por el script auxiliar de guardias (conteos; no se imprimió ninguna fila).
- Código: `tests/dbfmini.py` (lectura), `tests/check.py` líneas 1300-1345 (bloque `_T22_ARCHIVOS_CONOCIDOS`, sólo para saber si algún test parsea `codificacion-R`; ninguno lo hace), `tools/calibracion_mordida_encig_serie.py` (sólo el contexto de su mención a `codificacion-R`, un docstring).
- Los cuatro JSON nuevos de `corridas-R/` (propios).
- Metadatos: `gh pr view 486` y `gh pr diff 486 | grep -oE` de los ids `ADR-`/`FP-` que reclama (PR abierto del carril MAESTRA35-L7, reclama `ADR-302` y `FP-252`); nada más de ese diff se leyó.
