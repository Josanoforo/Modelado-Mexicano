# ENVIPE-SERIE-COMPLETA · especificación de las ocho olas pendientes

### `prereg-caja-ENVIPE-SERIE-COMPLETA-v1_0` · 10 de septiembre de 2026

Esta especificación queda congelada antes del primer resultado de las ocho
olas. Es sucesora por extensión, no reescritura, de
`prereg-caja-R-ENVIPE-SERIE` y
`prereg-caja-R-ENVIPE-SERIE-DBF`. Completa el estimando secundario que esas
familias ya declararon como punto de serie; no modifica sus seis árbitros `R`
ni `CALC-ENVIPE-0001`.

## 1. Estimando y unidad

Cada fila de `TMod_Vic` es un **delito**. El punto de serie es la proporción
ponderada de delitos personales no denunciados cuya razón principal declarada
fue miedo al agresor, miedo a extorsión o desconfianza en la autoridad:

`p(C1,U1) = sum(FAC_DEL * 1[respuesta en {01,02,06}]) / sum(FAC_DEL)`.

`U1` contiene `BPCOD` personal, `BP1_20=2`, respuesta en `{01..08}` y
`FAC_DEL` finito y positivo. `09` (“otra”), NS/NR y blanco se muestran y se
excluyen. `C2` añade `08` (“actitud hostil”) sólo como diagnóstico de
sensibilidad; nunca sustituye a `C1`. El cálculo es descriptivo, no causal, no
colapsa a persona, no interpola y no promedia olas.

ENVIPE 2011 llama al reactivo `BP1_21`; desde 2012 se llama `BP1_23`. Los nueve
códigos sustantivos conservan significado. La ola 2011 agrega `88` no responde
y `98` no especificado además de `99` no sabe; los tres quedan en `N-NSNR`.
Ésta es una ruptura de **instrumentación nominal y de categorías residuales**,
no del núcleo `C1/U1`, y se marca en el producto.

## 2. Censo congelado de insumos

| ola | año del delito | payload del manifiesto | formato/miembro | reactivo | diseño | sha256 | bytes |
|---:|---:|---|---|---|---|---|---:|
| 2011 | 2010 | `envipe_2011_base_de_datos_envipe_2011_dbf` | DBF · `tmod_vic.DBF` | `BP1_21` | `EST`/`UPM` | `d6c660f00ca2179dcabf59a9af166d7605793eed48c6eb84bcd8d24f39bd2ce4` | 8,956,716 |
| 2014 | 2013 | `envipe_2014_bd_envipe2014_dbf` | DBF · `bd_envipe2014/bd_envipe2014/TMod_Vic.dbf` | `BP1_23` | `EST`/`UPM` | `8f1d0eb519a0ceabe36d187d9a49734dbef97f219b86eea9084ebd1818973f77` | 11,506,651 |
| 2016 | 2015 | `envipe_2016_bd_envipe2016_dbf` | DBF · `TMod_Vic.dbf` | `BP1_23` | `EST_DIS`/`UPM_DIS` | `8c939550590bbb7941c65a2c9a3d87d8654cfe529e969f51265fe65974ef68a4` | 18,625,348 |
| 2017 | 2016 | `envipe_2017_bd_envipe2017_dbf` | DBF · `BASE_DE_DATOS_ENVIPE_2017_en/TMod_Vic.dbf` | `BP1_23` | `EST_DIS`/`UPM_DIS` | `86df9910dae338d4c4487e6760e8e3ba1a752c8a8fcda967a8af152ad49d8f74` | 18,932,534 |
| 2018 | 2017 | `envipe2018_csv` | CSV · `conjunto_de_datos_tmod_vic_envipe_2018/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe_2018.csv` | `BP1_23` | `EST_DIS`/`UPM_DIS` | `aa279993bfeaaa0bf0d821e964887140ef444f6e695e4e1767f6512e4d2c4723` | 24,337,809 |
| 2019 | 2018 | `envipe2019_csv` | CSV · `conjunto_de_datos_TMod_Vic_ENVIPE_2019/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2019.csv` | `BP1_23` | `EST_DIS`/`UPM_DIS` | `24bb83987f2ba57912a3f55c8ff3bb48e5f39f2292cd167997312c1fd77207f3` | 19,146,940 |
| 2020 | 2019 | `envipe2020_csv` | CSV · `conjunto_de_datos_TMod_Vic_ENVIPE_2020/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2020.csv` | `BP1_23` | `EST_DIS`/`UPM_DIS` | `26f468da631bfdb94994a9e5051fa973468608f0da56612b6897df16a2797b9d` | 20,253,728 |
| 2022 | 2021 | `envipe2022_csv` | CSV · `conjunto_de_datos_TMod_Vic_ENVIPE_2022/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2022.csv` | `BP1_23` | `EST_DIS`/`UPM_DIS` | `3a6e0f3a05dd4120efe8072de519402a39f4ed1690593433a68bb2ee137e77bb` | 18,858,955 |

Los ocho archivos dieron `COINCIDE` por hash y tamaño con
`data/manifiesto.yaml`. Las cabeceras físicas contienen reactivo, `BP1_20`,
`BPCOD`, `FAC_DEL` y las llaves de diseño declaradas. Los FD/cuestionarios
confirman `01..09`; el cambio 2011 está documentado en
`fd_envipe2011.xls`, hoja `TMod_Vic`, filas 190–203.

## 3. Diseño e incertidumbre

El punto usa `FAC_DEL`. El EE e IC95 analítico usan conglomerado último por
estrato mediante `tests/svystat.py:prop_ultimate_cluster`. Para comparabilidad
con los siete puntos existentes, el producto usa además bootstrap de UPM con
reemplazo dentro de estrato, 2,000 réplicas, `numpy.PCG64`, semilla `20260909`,
percentiles 2.5/97.5. Un estrato con UPM única entra al punto y aporta varianza
cero; si existe alguno, el IC se rotula **límite inferior de anchura**, no IC de
diseño exacto. Llaves de diseño se tratan como texto opaco.

## 4. Salidas y compuertas

Cada `CALC-ENVIPE-SERIE-AAAA` emite el embudo completo, punto `P-C1-U1`, IC
analítico y bootstrap, sensibilidad `C2`, unidad, año de encuesta y año del
hecho. Falta de columna, universo vacío o diseño incompleto se reporta y no se
imputa. Todos llevan `cuenta_gen2=SI` por el objeto explícito del encargo:
“Para CALC científicos nuevos, aplicar `cuenta_gen2=SI` con objeto y cita
explícitos”. La firma se perfecciona únicamente con el merge de mesa.

El primer resultado que produzca este procedimiento es el que se reporta.
