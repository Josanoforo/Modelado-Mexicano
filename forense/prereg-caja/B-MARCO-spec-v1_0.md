# B-MARCO · Pre-registro de familia de la línea base temporal `B` extendida, por serie, a las 14 celdas del marco-M

### `prereg-caja-B-MARCO` · **v1.0** · 14 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/B-MARCO-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-B-MARCO`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir microdato, del **censo de extensibilidad** de `B` a las 12 celdas del marco-M que hoy no lo tienen, y de la **regla fija por serie** con la que `B` se construye donde su fuente lo permite. Sucesora **por extensión** de `prereg-caja-B-REMESAS` (`sha256 = 2376c21a0668a5f57db8cbddcd8cc59dd468dc7e10838f66da3b8156fb93c7ba`, `CALC-B-0001`): misma clase de regla (persistencia de la última ola de la MISMA serie disponible al corte, dos brazos, mismo selector sin tocar, mismo bootstrap), aplicada a las series ENVIPE, ENCIG y ENIGH. Gobierna cuatro CALC: `CALC-B-MARCO-ENVIPE-0001`, `CALC-B-MARCO-ENCIG-0001`, `CALC-B-MARCO-ENIGH-0001` (B puro, GEN2) y `CALC-B-MARCO-MAE-0001` (el asiento sobre el marco: `err_pp`, control positivo, `MAE_pp(B)` con su `n`). |
> | **QUÉ NO ES** | **No redefine `B`** (`CALC-B-0001` y sus 90 RESULT no se tocan: FAM-M-06 y FAM-M-07 siguen siendo suyos). **No re-corre la tríada ni toca su veredicto** (`SIN-GANADOR-UNICO` / `INCONCLUSO` quedan como están). **No mira `R`, `M` ni `L` para elegir nada**: la contaminación es TOTAL y declarada (§0.2), por eso la regla es ciega y pre-declarada. **No rellena** celdas no-construibles: una celda `NO-CONSTRUIBLE` con cita es entregable. No mueve ninguna regla del motor: ninguna cifra suya entra a un veredicto (`T9`). No descarga nada. |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight <CALC>` en VERDE antes de correr; después `run` y `verify` por CALC. Control positivo por celda cubierta: la observada propia de cada ola objetivo frente al `R` sellado de su celda (§6.1), con tres ramas y consecuencia escrita antes de correr. Control positivo de familia: la ola ENIGH 2016 de `CALC-B-MARCO-ENIGH-0001` debe reproducir **punto e IC** de `RESULT-B-ENIGH-2016-*` de `CALC-B-0001` (misma semilla, misma implementación). |

**Acto:** `ACTO GEN2-B-MARCO`, 14/sep/2026, entorno **CAJA (UBUNTU/WSL)**, corpus montado, sobre `origin/main = 11c8783` (`PR #754`). Encargo archivado: `forense/encargos/2026-09-14-GEN2-B-MARCO.md`.

---

## 0 · Premisas del encargo verificadas contra el árbol, y la contaminación declarada

### 0.1 · Las tres premisas de A.8 se reproducen

1. **Estructura — `NC-0079`**, leída del TSV con `csv`-like por columna, no por `grep`: `estado = ABIERTA`, `impacto` verbatim: *«MAE_pp(B) no se calcula y B no entra a ninguna ordenacion: RESULT-C0D-B-VEREDICTO = NO-ADJUDICA-POR-N (n=2). Y el dato que lo hace urgente: en FAM-M-06 la linea base tonta yerra +0.0173 pp donde M yerra -0.1591 y L entre +0.15 y -0.004. Con dos celdas eso se cita, no se ordena.»* Sucesor declarado en la fila: *«acto propio que extienda B fuera de la serie ENIGH x recibe_remesas (un B nuevo por serie, no este)»*. **Este acto es ese sucesor.**
2. **Contenido — `B` existe sólo para 2 celdas.** `ls data/corrida0/ | grep -i CALC-B` → **2 entradas**: `CALC-B-0001` (el único `B`) y `CALC-BANXICO-PRODUCTO-DANO-0001` (falso positivo de subcadena, no es una línea base). `prereg-caja-C0D-MARCADOR` §0.2 congeló que `B` cubre FAM-M-06 (2018) y FAM-M-07 (2020) y que las otras 12 son `SIN-BASELINE-PRIMERA-OLA` (FAM-M-05) o `SIN-BASELINE-FUERA-DE-SERIE` (11). **CALC-B por otras series: NO-ENCONTRADO** (0 de 94 directorios de `data/corrida0/` empiezan por `CALC-B-MARCO`; el comando examinó los 94 nombres).
3. **Marco — 14 celdas**, leídas de `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv` (14 filas, 32 columnas; se leyeron `id · encuesta · ola · conducta · regla · escala`, **no** `cv_arbitro` ni ningún valor): 6 ENVIPE (2012, 2013, 2015, 2021, 2023, 2024), 3 ENIGH (2016, 2018, 2020), 2 ENCIG (2013, 2021), 1 ENCUCI (2020), 1 ENIF (2018), 1 ENNViH ola 1 (2002).

### 0.2 · Contaminación declarada (ADR-46) — TOTAL, y por eso la regla es ciega

El encargo lo dice y esta spec lo repite antes de cualquier cifra: **los valores `R`, `M` y `L` de las 14 celdas están en el repo** (`corridas-R/*.json`, `M-*.json`, `L-extraido-v1_2.tsv`, `CALC-C0D-MARCADOR-v3`) y esta sesión pudo verlos. Lo que esta sesión **hizo** al congelar: leyó de `corridas-R/<celda>.json` únicamente las llaves de **definición** (`encuesta`, `ola`, `payload_id`, `tabla`, `variable`, `universo`, `codificacion`, `ponderador`, `estrato`, `upm`, conteos de embudo) por un extractor que **excluyó** `R`, `EE_R`, `cv`, `ic95_*`; no abrió `M-*.json`, `L-extraido-*`, `resultados.json` de `C0D` ni `envipe-serie-denuncia-v1_0.tsv`. Lo que **no puede probar**: que no recuerde cifras citadas en prosa del árbol (la propia `NC-0079` trae tres). **Consecuencia: ninguna decisión de esta spec depende de un valor.** La regla es la de la familia, fija y tonta; las únicas adaptaciones son las que la **fuente** obliga (nombre de variable, nombre de ponderador, formato), y cada una se declara en §1.

### 0.3 · Lo que sí se leyó, y con qué (A.13)

Codebooks y estructura, nunca valores: descriptores DBF (32 bytes de cabecera + 32 por campo) de `tmod_vic` en ENVIPE 2011–2015; primera línea de los CSV de ENVIPE 2020–2024, ENCIG 2019/2021, ENIGH 2014/2016; `metadatos/*.txt` de esos CSV (`Identifier`, `Modified`, `Temporal`); `mtime` de los miembros DBF dentro de sus zip; `fd_envipe2011.xls` y `fd_envipe2012.xls` hoja `TMod_Vic` (catálogo de `BP1_21`/`BP1_23`); `fd_encig2011.pdf`, `encig13_descripcion_archivos.pdf`, `encig19_estructura_base_datos.pdf`, `encig21_estructura_base_datos.pdf` (vía `pdftotext -layout`); `enif_2018_fd.xlsx`, `enif_2015_fd.xlsx`, `fd_enif2012.xlsx` (todas las hojas, búsqueda por texto); `diccionario_datos_enigh_ncv_2014.csv`; `data/manifiesto.yaml` (1 608 entradas; 77 ENVIPE, 38 ENCIG, 22 ENIF, 29 ENNViH, 2 ENCUCI, 6 ENIGH). Un hallazgo de formato que el medidor absorbe: **los CSV de ENVIPE 2020–2024 terminan línea con `\r` solo** (sin `\n`), lo que hace que un `split("\n")` lea el archivo entero como una línea.

---

## 1 · P1 · Censo de extensibilidad — celda por celda, con cita

**Criterio, único y previo:** una celda es `CONSTRUIBLE` si en corpus existe una ola **anterior** de la **misma serie** —mismo instrumento, mismo reactivo (o su renombre nominal documentado por el FD), mismo universo y misma codificación que el `R` de la celda declara— sobre la que la regla de la familia puede correr **sin crosswalk**. El selector lo dice en su docstring: *«No infiere equivalencias. Un crosswalk entre instrumentos tiene que resolverse antes y estar documentado por el consumidor: este selector no lo decide por semejanza.»* Construir un crosswalk sería inventar un `B`, no heredar el de la familia.

| celda | serie · ola objetivo · estimando de `R` (definición) | predecesora en corpus (payload · tabla) | regla `B` propuesta (adaptación declarada) | construible | cita |
|---|---|---|---|---|---|
| **CIV-M-01** | ENVIPE 2012 · `TMod_Vic.BP1_23` ∈ {01,02,06} / {03..05,07..09}, `FAC_DEL`, todos los delitos | ENVIPE 2011 · `envipe_2011_base_de_datos_envipe_2011_dbf` · `tmod_vic.DBF` | familia; **adaptación nominal**: el reactivo se llama `BP1_21` en 2011 y trae `88`/`98` además de `99` (todos FUERA); diseño `EST`/`UPM` | **SÍ** | `fd_envipe2011.xls` hoja `TMod_Vic` filas 192–204: `BP1_21` códigos 01..09 idénticos a `BP1_23` de 2012 (`fd_envipe2012.xls` filas 231–241); descriptor DBF: `BP1_21 C(2)`, `FAC_DEL C(6)`, `EST C(3)`, `UPM C(5)` |
| **CIV-M-02** | ENVIPE 2013 · ídem | ENVIPE 2012 · `envipe_2012_base_de_datos_envipe_2012_dbf` · `Tmod_Vic.DBF` | familia, sin adaptación (`EST`/`UPM`) | **SÍ** | descriptor DBF 2012: `BP1_23 C(2)`, `BP1_20 C(1)`, `FAC_DEL C(6)`, `EST C(3)`, `UPM C(5)`, 134 campos |
| **CIV-M-04** | ENVIPE 2015 · ídem | ENVIPE 2014 · `envipe_2014_bd_envipe2014_dbf` · `bd_envipe2014/bd_envipe2014/TMod_Vic.dbf` | familia; diseño `EST`/`UPM` en 2014 (en 2015 ya `EST_DIS`/`UPM_DIS`: cambio de nombre, no de existencia) | **SÍ** | descriptor DBF 2014: `BP1_23 C(2)`, `FAC_DEL C(6)`, `EST C(3)`, `UPM C(5)`, 121 campos; `prereg-caja-ENVIPE-SERIE-COMPLETA` §2 (misma tabla, `sha256 8f1d0eb5…`) |
| **CIV-M-10** | ENVIPE 2021 · ídem | ENVIPE 2020 · `envipe2020_csv` · `conjunto_de_datos_TMod_Vic_ENVIPE_2020` | familia, sin adaptación (`EST_DIS`/`UPM_DIS`) | **SÍ** | cabecera CSV 2020 (130 columnas): `BP1_23`, `BP1_20`, `BPCOD`, `FAC_DEL`, `EST_DIS`, `UPM_DIS` presentes; `metadatos_ENVIPE_2020.txt` `Modified=2020-12-10` |
| **CIV-M-12** | ENVIPE 2023 · ídem | ENVIPE 2022 · `envipe2022_csv` · `conjunto_de_datos_TMod_Vic_ENVIPE_2022` | familia, sin adaptación | **SÍ** | cabecera CSV 2022: las seis columnas presentes; `Modified=2022-09-08` |
| **CIV-M-13** | ENVIPE 2024 · ídem | ENVIPE 2023 · `envipe2023_csv` · `tmod_vic_envipe2023` | familia, sin adaptación | **SÍ** | cabecera CSV 2023 (129 columnas): presentes; `Modified=2023-09-11` |
| **DIN-M-01** | ENNViH-1 2002 (ola 1) · `iiib_cr.dta:cr27` | **ninguna**: 2002 es la PRIMERA ola del panel (manifiesto: `ennvih1_2002_*`, `ennvih2_2005_*`, `ennvih3_2009_*`) | — | **NO** · `SIN-BASELINE-PRIMERA-OLA` | `data/manifiesto.yaml`: 29 entradas ENNViH, ninguna anterior a 2002; misma razón por la que `C0D` §0.2 dejó FAM-M-05 sin `B` en su universo |
| **FAM-M-01** | ENIF 2018 · `tmodulo2.p9_9_4` («En su vejez, ¿piensa cubrir sus gastos con… dinero que le den su pareja, esposo(a), sus hijos u otros familiares?») | ENIF 2015 (`enif_2015_enif_2015_bd_dbf`) y ENIF 2012 (`enif_2012_bases_enif2012_dbf`) existen en corpus, pero **ninguna trae el reactivo** | — | **NO** · `REACTIVO-AUSENTE-EN-OLA-PREVIA` | `enif_2018_fd.xlsx` hoja `TModulo2`: batería 9.9 `P9_9_1..P9_9_5`; `enif_2015_fd.xlsx` (7 hojas, búsqueda por «vejez», «cubrir sus gastos», «adultos mayores», «9.9»): **0 coincidencias** fuera de `P5_17_8` («Para la vejez o retiro», motivo de AHORRO, otra pregunta); sección 8 de 2015 = Afore (`P8_1..P8_8`), sección 9 = remesas (`P9_1..`); `fd_enif2012.xlsx`: ídem, 0 coincidencias. La batería 9.9 **nace en 2018** |
| **FAM-M-05** | ENIGH 2016 NS · `concentradohogar.remesas > 0`, `factor`, universo completo | ENIGH 2014 NCV · `enigh2014_nc_csv` · `concentradohogar_enigh2014ncv/conjunto_de_datos/concentradohogar.csv` | familia; **adaptación declarada**: el ponderador de hogar se llama `factor_hog` en 2014 (`factor` en 2016). Es la extensión hacia atrás que `prereg-caja-B-REMESAS` §0.1 dejó explícitamente a un sucesor; `CALC-B-0001` no se toca | **SÍ** | `diccionario_datos_enigh_ncv_2014.csv` tabla CONCENTRADOHOGAR: fila 52 `remesas, "N (12,2)", Ingresos provenientes de otros países` (misma definición que 2016–2022); fila 9 `factor_hog, Factor de expansión del hogar, N (5)`; filas 7–8 `est_dis C(3)`, `upm C(5)`; cabecera CSV (127 columnas) las trae; `enigh_ncv_2014.txt` `modified: 2019-10-03` |
| **FAM-M-06** | ENIGH 2018 | ya cubierta por `CALC-B-0001` (`RESULT-B-PERSISTENCIA-2018-P` / `RESULT-B-OPERATIVO-2018-P`) | — (no se rehace) | ya `B` | `prereg-caja-C0D-MARCADOR` §0.2 |
| **FAM-M-07** | ENIGH 2020 | ya cubierta por `CALC-B-0001` (`…-2020-P`) | — (no se rehace) | ya `B` | ídem |
| **TRA-M-02** | ENCUCI 2020 · `SEC_4_5.AP5_17|AP5_18` | **ninguna**: ENCUCI tiene UNA ola en corpus y en el programa de INEGI | — | **NO** · `SIN-SERIE` | `data/manifiesto.yaml`: 2 entradas ENCUCI, ambas 2020 (`encuci2020_bd_dbf`, `encuci2020_fd_pdf`). Un `B` desde ENCIG 2019 sería un crosswalk entre instrumentos (y ENCUCI mide la unión pedir∨dar; ENCIG sólo pedir): prohibido por la regla de familia |
| **TRA-M-03** | ENCIG 2013 · `sec_1_3_4_5_8_9.P8_3` («Durante 2013, al realizar alguno de estos pagos o trámites ¿un empleado del gobierno intentó apropiarse de algún beneficio…?»), persona 18+, `FAC_P18` | ENCIG 2011 (`encig_2011_base_datos_encig2011_dbf`) existe, pero **no trae la sección VIII ni la pregunta a nivel persona** | — | **NO** · `REACTIVO-AUSENTE-EN-OLA-PREVIA` | `fd_encig2011.pdf`: tres tablas (`01_RESIDENTES`, `02_VIVIENDA_HOGAR`, `03_TRAMITES`); la única pregunta de mordida es **por trámite** en `03_ENCIG2011_TRAMITES` (`P4_11` «¿las condiciones lo llevaron a pagar una mordida o soborno?», `P4_13` «¿El servidor público le pidió pagar una mordida o soborno?»; 93 836 registros de trámite de 24 820 residentes). Otra unidad (trámite, no persona), otro reactivo (pedir/pagar mordida vs. intentar apropiarse de un beneficio), otro universo (residentes CON trámite). `encig13_descripcion_archivos.pdf` fila 129: `P8_3 C(1) 1-2,9` |
| **TRA-M-07** | ENCIG 2021 · `sec1_A_..._8_9_10.P8_3_1` («¿Un servidor público o empleado del gobierno intentó apropiarse o le solicitó de forma directa algún beneficio…?»), `FAC_P18` | ENCIG 2019 · `encig2019_csv` · `conjunto_de_datos_encig2019_01_sec1_3_4_5_8_9_10` | familia, sin adaptación (`P8_3_1`, `FAC_P18`, `EST_DIS`/`UPM_DIS`) | **SÍ** | `encig19_estructura_base_datos.pdf` reactivo 220: `P8_3_1` texto idéntico al de 2021 (`encig21_estructura_base_datos.pdf` reactivo 227), códigos `1 Sí / 2 No / 9 NS-NR`; cabecera CSV 2019 (235 columnas): `p8_3_1`, `fac_p18`, `est_dis`, `upm_dis`; `metadatos_ENCIG_2019.txt` `Modified=2020-05-21` |

**Resultado del censo, congelado:** de las 12 celdas sin `B`, **8 son construibles** (6 ENVIPE, 1 ENCIG, 1 ENIGH) y **4 no** (DIN-M-01, FAM-M-01, TRA-M-02, TRA-M-03), cada una con su razón citada. **La cobertura resultante se declara y no se rellena**: `B` pasará, si todo emite, de 2 a **10 de 14** bajo el brazo `PERSISTENCIA`. Lo que el brazo `OPERATIVO` pueda cubrir se deriva en §6.2 de metadatos ya leídos.

---

## 2 · La regla, por serie — heredada, no elegida

Para cada serie construible, `B(celda objetivo) = p(última ola de la MISMA serie disponible al corte)`, con `p` la proporción ponderada del **estimando del `R` de la celda**, medida por este acto sobre el microdato de la ola predecesora, **una ola a la vez, jamás promediadas**. El selector es `tools/baseline_temporal.py` (sha `83ff6a064cb0961af32178cbbbe4097358c85e5f59d7b67da138e096d3ea1b2a`, `commit 67aa13d`; sucesor del `886f2da4…` que consumió `CALC-B-0001` — la función `seleccionar_baseline` es la misma y no se modifica).

### 2.1 · ENVIPE (`CALC-B-MARCO-ENVIPE-0001`)

- **Serie:** `encuesta = ENVIPE`, `reactivo = TMod_Vic.BP1_23` (`BP1_21` en 2011, cambio nominal), `universo` = delitos captados en `TMod_Vic`, todos los tipos, sin filtro adicional; `codificacion`: y=1 si código ∈ {01,02,06}; y=0 si ∈ {03,04,05,07,08,09}; NS/NR (99; 88/98 en 2011) y blanco FUERA; `segmento = nacional`, `unidad = proporcion`. Es **verbatim** la codificación que `corridas-R/CIV-M-*.json` declara para las seis celdas.
- **Universo de olas de la serie `B`:** 2011, 2012, 2013, 2014, 2015, 2020, 2021, 2022, 2023, 2024 — las seis objetivo y sus predecesoras inmediatas. **2016–2019 y 2025 existen en corpus y quedan FUERA** (no son objetivo ni predecesora de ningún objetivo; medirlas sería alargar la serie por la puerta de atrás).
- **Objetivos:** 2012 (CIV-M-01), 2013 (CIV-M-02), 2015 (CIV-M-04), 2021 (CIV-M-10), 2023 (CIV-M-12), 2024 (CIV-M-13).
- **Ponderador:** `FAC_DEL` en las diez olas. **Diseño:** `EST`/`UPM` (2011–2014), `EST_DIS`/`UPM_DIS` (2015–2024) — llaves opacas, texto sin recortar en DBF.
- **Lo que NO se usa:** `BPCOD` (la celda no filtra por tipo de delito; el corrimiento del catálogo 2012 documentado en `prereg-caja-R-ENVIPE-SERIE-DBF` §3 no toca este estimando), `BP1_20` (redundante: el blanco de `BP1_23` ya deja fuera a quien denunció).

### 2.2 · ENCIG (`CALC-B-MARCO-ENCIG-0001`)

- **Serie:** `encuesta = ENCIG`, `reactivo = seccion VIII P8_3_1`, `universo` = personas 18+ de la tabla de la sección VIII (la tabla ya es el universo), `codificacion`: y=1 si `'1'`; y=0 si `'2'`; 9 y blanco FUERA. Verbatim de `corridas-R/TRA-M-07.json`.
- **Universo de olas:** 2019 (predecesora), 2021 (objetivo). **Objetivo:** 2021 (TRA-M-07). **Ponderador:** `FAC_P18`. **Diseño:** `EST_DIS`/`UPM_DIS`.
- 2011–2017, 2023 y 2025 quedan FUERA (§1: 2011 no tiene la pregunta; las demás no son objetivo ni predecesora).

### 2.3 · ENIGH (`CALC-B-MARCO-ENIGH-0001`)

- **Serie:** la de `CALC-B-0001`, verbatim: `encuesta = ENIGH-NS`, `reactivo = concentradohogar.remesas`, universo completo de `concentradohogar`, `recibe_remesas = 1 si remesas > 0, 0 si remesas == 0`.
- **Universo de olas:** 2014 (predecesora, NCV), 2016 (objetivo, NS). **Objetivo:** 2016 (FAM-M-05). **Ponderador:** `factor_hog` (2014) / `factor` (2016) — el ponderador de hogar de cada ola bajo el nombre de su diccionario. **Diseño:** `est_dis`/`upm`.
- **Guardia heredada §1.1 de B-REMESAS:** la rama NA no existe; `N-FUERA-CODIGO` (= nulos de `remesas`) > 0 → `NO-ESTIMABLE-NULOS-INESPERADOS`.
- 2012 queda FUERA (no es predecesora inmediata de ningún objetivo); 2018–2022 son de `CALC-B-0001`.

### 2.4 · Adaptaciones, todas declaradas y ninguna elegida

Tres, y las tres las obliga la fuente: (i) `BP1_21` por `BP1_23` en ENVIPE 2011 (renombre documentado por el FD); (ii) `factor_hog` por `factor` en ENIGH 2014 (renombre documentado por el diccionario); (iii) `EST`/`UPM` por `EST_DIS`/`UPM_DIS` en ENVIPE 2011–2014 (renombre; sólo afecta al IC). Ningún umbral, ningún filtro, ninguna ventana se eligió mirando dato alguno.

---

## 3 · Cómo se le habla al selector — dos brazos, y las fechas de versión que los separan

Idéntico a `B-REMESAS` §2.2–§2.3: `periodo(ola) = <ola>-01-01 … <ola>-12-31` (año calendario de la **encuesta**, que es el `ola` del marco), `fecha_corte(objetivo) = <objetivo − 1>-12-31`, `publicada = true`. Los dos brazos difieren **sólo** en `disponible_desde`:

- **`OPERATIVO`** — la fecha de versión de la ola en corpus. Para los CSV de datos abiertos, el campo `Modified` de `metadatos/*.txt`. **Para los DBF (ENVIPE 2011–2015), el payload no trae `metadatos/`**: se usa el `mtime` del miembro `tmod_vic` dentro del zip, que es el único metadato de versión que el propio payload lleva; se sella verbatim en `RESULT-BM-ENVIPE-<ola>-METADATO-VERSION` y se declara aquí como proxy, no como fecha de publicación de INEGI.
- **`PERSISTENCIA`** — `disponible_desde = periodo_fin` (el contrafáctico «si cada ola hubiera estado disponible el día que cerró su levantamiento»).

**Acotación declarada del brazo `OPERATIVO`.** El selector valida `disponible_desde ≥ periodo_fin`, y una versión puede llevar fecha **anterior** al cierre del año calendario de su ola (ENVIPE se publica en septiembre del año de encuesta: `Modified = 2020-12-10` para la ola 2020). Por eso `disponible_desde(OPERATIVO) = max(versión, periodo_fin)`. La acotación **nunca cambia la selección**: `periodo_fin` de una ola es ≤ `fecha_corte` de cualquier objetivo posterior, así que una versión fechada antes del cierre sigue disponible al corte. Lo atrapó la prueba sintética del medidor antes de congelar; se declara aquí y en el código.

| ola (serie) | versión en corpus (`OPERATIVO`) | fuente del metadato |
|---|---|---|
| ENVIPE 2011 | 2013-08-12 | mtime `tmod_vic.DBF` |
| ENVIPE 2012 | 2013-08-06 | mtime `Tmod_Vic.DBF` |
| ENVIPE 2013 | 2013-09-24 | mtime `tmod_vic.dbf` |
| ENVIPE 2014 | 2015-06-24 | mtime `TMod_Vic.dbf` |
| ENVIPE 2015 | 2015-09-09 | mtime `TMod_Vic.dbf` |
| ENVIPE 2020 / 2021 / 2022 / 2023 / 2024 | 2020-12-10 / 2021-09-22 / 2022-09-08 / 2023-09-11 / 2024-09-19 | `Modified` |
| ENCIG 2019 / 2021 | 2020-05-21 / 2022-05-24 (verbatim `2022-05-24.`) | `Modified` |
| ENIGH 2014 / 2016 | 2019-10-03 / 2021-11-29 | `modified` / `Modified` |

---

## 4 · IC95 — método heredado, ranura declarada

Bootstrap de UPM **con reemplazo dentro de cada estrato**, conservando el número de UPM por estrato; percentiles 2.5/97.5; `B = 2000`; **semilla `20260908`, RNG `numpy.PCG64` — la misma de `CALC-B-0001`, a propósito** (§6.3). Implementación **copiada verbatim** de `data/corrida0/CALC-B-0001/medidor.py::_boot_ic`. Nadie pre-registró un método de IC para estas series bajo `B`: se hereda el de la familia, se declara y se eleva a mesa. No se espera coincidencia dígito a dígito con los IC de `corridas-R` (ultimate cluster analítico, otra implementación). `n_minimo_celda = 10`.

**Guardias que PARAN por ola, pre-declaradas:** `N-SIN-DISENO > 0` → IC `null`, `NO-ESTIMABLE-DISENO-INCOMPLETO` (el punto se reporta); `n < 10` → `NO-ESTIMABLE`; **guardia de producto**: `p` exactamente `0.0` o `1.0` → `NO-ESTIMABLE-P-DEGENERADA` (lección de `MAESTRA35-L6`: una proporción que satura es una definición mal puesta, no una medición). Una ola no reportable entra al historial con `p = null` y el selector la excluye por `VALOR_NO_ESTIMABLE`: nada se fabrica.

---

## 5 · Lo que emite cada CALC

**Por serie** (`CALC-B-MARCO-<SERIE>-0001`, B puro, sin leer `R`): por ola, `P`, `IC-LO`, `IC-HI`, `N`, `N-FILAS-LEIDAS`, `N-FUERA-CODIGO`, `N-SIN-PONDERADOR`, `N-SIN-DISENO`, `EXPANDIDOS`, `VEREDICTO`, `METADATO-VERSION`, `METADATO-TEMPORAL` (el embudo completo, A.13); por objetivo, `CELDA`; por objetivo × brazo, `ESTADO`, `METODO`, `FUENTE`, `P`, `ERROR` (vs. observada propia), `ERROR-ABS`, `DENTRO-IC`, `MARGEN-AL-BORDE`; por brazo, `N-PREDICCIONES` y `BIS-LECTURA` (`PISO-ALTO` / `PISO-BAJO` / `MIXTO` / `SIN-PREDICCIONES`, §5.2 de B-REMESAS, verbatim). ENVIPE: 226 RESULT; ENCIG: 45; ENIGH: 45.

**El asiento** (`CALC-B-MARCO-MAE-0001`): por celda del marco (14), `ORIGEN-B` (el CALC que la sirve, o la razón `NO-CONSTRUIBLE-…`), `R` (copiado de `corridas-R`, insumo sellado), `CONTROL-R-DELTA`, `CONTROL-R-RAMA`, y por brazo `P-B`, `ERR-PP = 100·(P_B − R)` (**escala: puntos porcentuales de una proporción ponderada**, A-bis.3), `ESTADO`; por brazo, `MAE-PP`, `N-CELDAS`, `CELDAS` (la lista), `MAX-ABS-ERR-PP`, `CELDA-MAX-ABS`, `COBERTURA-DESPUES`; y `COBERTURA-ANTES = 2`, `N-CELDAS-MARCO = 14`, `N-NO-CONSTRUIBLES = 4`. Total: 155.

**Por qué el asiento es un CALC aparte, y el único envuelto.** El registro (`tools/corrida0.py`, regla E.1) marca como insumo LEGACY todo lo que cuelga de `forense/prereg-duelo-v2/corridas-R/`. Los tres CALC de serie **no leen `R`** y quedan GEN2 limpios, como `CALC-B-0001`; el asiento **sí** (es su objeto: comparar contra el árbitro), luego será `envuelto_legacy = SI` por construcción y se declara aquí, antes de correr. Sus insumos son `resultados.json` sellados de los cuatro `B` más `corridas-R/<celda>.json` de las 10 celdas con `B` más `marco-M-sorteado-v1_3.tsv` (guardia de identidad: las 14 celdas declaradas son exactamente las del marco). **Su `spec.yaml` se instancia después de que las series sellen** —declara esos `resultados.json` por sha256, que no existen al congelar—, con el mismo patrón que `CALC-C0D-MARCADOR-v3` usó para `IN-V2-RESULTADOS`; su regla es `medidor.py`, congelado **hoy**, y no cambia entre este commit y ese.

**`MAE_pp(B)` se reporta CON su `n` y con su lista de celdas, y jamás se compara contra el `MAE` de `M` o `L` sobre otra cobertura sin decirlo (A-bis.4).** La tabla por celda de la nota del lote (P3) pone `err_pp(B)` al lado de los errores de `M` y `L` **donde existan**, como descripción, y no re-adjudica la tríada.

---

## 6 · B-bis — lo que se lee, escrito ANTES de correr

### 6.1 · Control positivo por celda cubierta — tres ramas y su consecuencia

Para cada celda con `B`, la **observada propia** de la ola objetivo (`RESULT-BM-<SERIE>-<ola>-P`, o `RESULT-B-ENIGH-<ola>-P` de `CALC-B-0001` para FAM-M-06/07) se compara con el `R` sellado de la celda: `Δ = P_obs − R`.

| rama | condición | consecuencia |
|---|---|---|
| `REPRODUCE-EXACTO` | `|Δ| ≤ 1e-10` | el medidor mide el mismo estimando que el árbitro; `err_pp(B)` es comparable con los `err_pp` de `M` y `L` de esa celda por construcción |
| `REPRODUCE-AL-GRANO` | `1e-10 < |Δ| < 1e-6` | ídem, con diferencia de redondeo/orden de suma; se reporta |
| `NO-REPRODUCE` | `|Δ| ≥ 1e-6` | **es EL hallazgo de esa celda**: mi lectura del estimando difiere del árbitro. `B` se reporta igual (la regla no se toca), `err_pp` se reporta igual, y la nota lo dice con las dos cifras y el signo. **No se corrige hacia atrás** ni se re-corre; un tercer commit podría congelar un diagnóstico, nunca reescribir éste |

Este control es lo que hace lícita la comparación: **sin él, un `err_pp(B)` chico podría ser un `B` bueno o un estimando distinto.**

### 6.2 · Lo que ya se puede derivar de metadatos YA LEÍDOS — declarado como derivación, no como pronóstico

Por §3, las fechas de versión ya se conocen, y el selector es determinista sobre ellas:

1. **Brazo `OPERATIVO`: se espera `SIN_BASELINE` (`NO_DISPONIBLE_AL_CORTE`) en CIV-M-01 (2011 versionada 2013-08-12 > corte 2011-12-31; no hay ola anterior), CIV-M-02 (2012 versionada 2013-08-06 y 2011 versionada 2013-08-12, ambas > 2012-12-31) y FAM-M-05 (2014 versionada 2019-10-03 > 2015-12-31; 2012 está fuera del universo)**. En **CIV-M-04** la predecesora inmediata NO está disponible (2014 versionada 2015-06-24 > 2014-12-31) pero **2013 sí** (2013-09-24): el selector elige la **última ola disponible**, así que `EMITE` con `FUENTE = RESULT-BM-ENVIPE-2013-P` — dos olas atrás, que es exactamente lo que el brazo operativo mide. `EMITE` desde la predecesora inmediata en CIV-M-10 (2020 → 2020-12-10, acotado a 2020-12-31 ≤ corte 2020-12-31), CIV-M-12, CIV-M-13 y TRA-M-07 (2019 → 2020-05-21, acotado a 2019-12-31). **Esperado: 5 predicciones nuevas; cobertura `OPERATIVO` del marco 0 → 5** (`CALC-B-0001` no emite `OPERATIVO` en 2018 ni 2020).
2. **Brazo `PERSISTENCIA`: se esperan las 8 predicciones nuevas**, cada objetivo desde su ola inmediatamente anterior del universo; cobertura **2 → 10 de 14**.
3. **Sobre `DENTRO-IC` y sobre `err_pp`: nada se deriva ni se pronostica.** Esta sesión no abrió las cifras y no escribe expectativas sobre ellas.
4. `ROZA-EL-BORDE` (`|MARGEN-AL-BORDE| < 1e-4`) se reporta como tal, nunca como decisión limpia (B-REMESAS §5.3.4).

### 6.3 · Control positivo de familia

`RESULT-BM-ENIGH-2016-P`, `-IC-LO`, `-IC-HI`, `-N` deben coincidir con `RESULT-B-ENIGH-2016-P`, `-IC-LO`, `-IC-HI`, `-N` de `CALC-B-0001` (misma ola, mismo payload, misma lectura, misma implementación del bootstrap, misma semilla). Se verifica en la nota con las ocho cifras a la vista. Si el punto coincide y el IC no, el bootstrap no es el de la familia y **eso se reporta antes de leer nada más**.

---

## 7 · Lo que esta spec explícitamente NO autoriza

1. **No mueve ninguna regla** ni entra a ningún veredicto (`T9`).
2. **No redefine `B`** ni toca `CALC-B-0001`, sus RESULT ni `prereg-caja-B-REMESAS`.
3. **No re-corre la tríada** ni toca `CALC-C0D-MARCADOR-v3`, su veredicto ni su adjudicación. `B` extendido queda **DISPONIBLE** para la próxima corrida de tríada que mesa autorice.
4. **No construye crosswalks** (ENCUCI←ENCIG, ENCIG 2013←2011 por trámite, ENIF 2018←2015 por otra batería): las cuatro celdas no-construibles quedan sin `B` y así se reportan.
5. **No promedia, no ajusta tendencia, no interpola, no imputa** y no alarga ninguna serie más allá de la predecesora inmediata de cada objetivo.
6. **No recalibra nada tras ver resultados**: lo no fijado aquí no existe.
7. **No firma por mesa.** `cuenta_gen2 = SI` se escribe en `data/corrida0/decisiones.tsv` **citando la firma de contador con objeto del encargo** (FIRMA DE MESA 14/sep/2026, verbatim en `forense/encargos/2026-09-14-GEN2-B-MARCO.md`), para los tres CALC de serie (B puro, GEN2). Para `CALC-B-MARCO-MAE-0001` **no se escribe**: consume `R` GEN1 y la regla E.1 lo resuelve sola; forzar la firma sobre un envuelto sería miscategorizar para mover un contador.

---

## 8 · Sello

Esta spec queda congelada en el `COMMIT-1` del `ACTO GEN2-B-MARCO`, junto con `medidor.py` (probado sólo sobre datos **sintéticos**), `spec.md` y `spec.yaml` de los tres CALC de serie y `medidor.py` + `spec.md` del asiento, antes de que ningún medidor lea un byte de microdato. **El primer resultado que produzca este procedimiento es el que se reporta.**
