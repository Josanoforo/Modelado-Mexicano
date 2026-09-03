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
