Eres una sesión de reconstrucción independiente. No tienes historial ni memoria, y no debes buscarlos. Tu único insumo es el directorio `./paquete/`, de solo lectura. Escribes únicamente en `./salida/`.

## Objetivo

Recalcula el punto y, donde la spec lo defina, el IC95 de cada una de las 7189 llaves de `paquete/esquema-identidades.tsv`. Implementa tú mismo el método de la spec humana `paquete/docs/spec-humana.md`, apoyándote en la documentación de `paquete/docs/`, en Python 3 (numpy, pandas). Para leer `.sav` o `.dbf` tienes `pyreadstat` y `dbfread` en `paquete/lib/` (`sys.path.insert(0, "paquete/lib")`); son lectores de terceros, sin método del programa. `.dta` se lee con `pandas.read_stata`. La spec menciona funciones de un código previo: no existe en el paquete, no debes buscarlo, y su comportamiento solo vale en la medida en que la spec lo describe en prosa. Las columnas `conducta`, `eje`, `segmento` y `ola` del esquema dicen qué estima cada llave.

- Formato de salida: `CONTRATO-v3.md` (`version` = 3).
- `FIRMAS-Y-ACCESO.md` registra qué firmó mesa y el alcance de tu acceso.

## Límites de acceso (autorización delimitada)

Del microdato puedes leer la fila de encabezados (o la lista de variables) completa, y de las filas solo estas columnas; en pandas usa `usecols` / `columns`:
- `datos/ensu_2013t3_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2013t3_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2013t4_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2013t4_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2014t1_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2014t1_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2014t2_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2014t2_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2014t3_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2014t3_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2014t4_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2014t4_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2015t1_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2015t1_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2015t2_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2015t2_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2015t3_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2015t3_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2015t4_cb.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `CD`, `EDIS`, `UPM_DIS`, `FACTOR`, `P1`, `P3_3`, `P3_4`, `P3_6`, `P4_1`, `P4_2`, `P4_3`, `P4_4`.
- `datos/ensu_2015t4_cs.dbf`: `ENT`, `CON`, `V_SEL`, `N_HOG`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2016t1_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`.
- `datos/ensu_2016t1_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2016t2_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`.
- `datos/ensu_2016t2_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2016t3_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_8_1`.
- `datos/ensu_2016t3_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2016t4_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_8_1`.
- `datos/ensu_2016t4_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2017t1_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2017t1_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2017t2_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2017t2_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDA`.
- `datos/ensu_2017t3_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2017t3_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2017t4_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2017t4_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2018t1_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2018t1_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2018t2_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2018t2_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2018t3_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2018t3_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2018t4_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2018t4_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2019t1_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2019t1_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2019t2_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`.
- `datos/ensu_2019t2_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2019t3_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2019t3_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2019t4_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`.
- `datos/ensu_2019t4_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2020t1_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`.
- `datos/ensu_2020t1_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2020t3_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEX`, `EDAD`.
- `datos/ensu_2020t3_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2020t4_cb.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEX`, `EDAD`.
- `datos/ensu_2020t4_cs.dbf`: `UPM`, `VIV_SEL`, `H_MUD`, `N_REN`, `SEX`, `EDAD`.
- `datos/ensu_2021t2_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2021t3_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2021t4_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2022t1_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2022t2_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2022t3_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2022t4_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2023t1_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2023t2_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2023t3_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2023t4_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2024t1_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2024t2_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2024t3_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2024t4_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2025t1_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2025t2_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.
- `datos/ensu_2025t3_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `SEXO`, `EDAD`.
- `datos/ensu_2025t4_cb.csv`: `UPM`, `VIV_SEL`, `H_MUD`, `R_SEL`, `CD`, `EST_DIS`, `UPM_DIS`, `FAC_SEL`, `BP1_1`, `BP1_2_03`, `BP1_2_08`, `BP1_2_09`, `BP1_3`, `BP1_4_3`, `BP1_4_4`, `BP1_4_6`, `BP1_5_1`, `BP1_5_2`, `BP1_5_3`, `BP1_5_4`, `BP1_9_1`, `BP1_8_1`, `BP3_5`, `BP3_6`, `SEXO`, `EDAD`.

Filtro de filas que pide la spec: Persona seleccionada 18+ (tabla CB, una por vivienda): FAC_SEL/FACTOR > 0 y estrato (CD + EST_DIS/EDIS) y UPM_DIS no vacios; denominadores por conducta segun lista-cerrada-P1 s3. 2020T3: solo tabla ENSU_CB_sec1_2_3_0920. Sin filtro adicional de filas en el paquete (se entregan filas completas)..

Si el método exige una columna que no está en esta lista, no la leas: marca las llaves afectadas con `BLOQUEADO-POR-ACCESO` y escribe el `motivo`. No imprimas filas de microdato; conteos y agregados sí. No uses la red ni leas nada fuera de `./paquete/`.

## Qué entregar en `./salida/`

1. `salida/resultado.json`: exactamente el documento de `CONTRATO-v3.md`; `version` = 3; `identidad` = `{"paquete": "ensu-serie-0001", "version_entrada": "validacion-continua-1", "sha256_entrada": "3fba81d9ad75421ed925fb8ca89405a81df435191207e272904709cf5d8f8522"}`; una fila por llave del esquema, con `llave` y `unidad` literales. Con estimación: `estado: "RECONSTRUIDO"`, `punto` y `estado_ic` explícito (`CALCULADO` con `ic95_inf`/`ic95_sup`, `SIN-IC` si la spec no define IC para esa llave, o `NO-IDENTIFICADA` con `motivo_ic`). Sin estimación: el estado del contrato que corresponda, con `motivo`. Números como strings `repr(float(x))`, sin redondear. No suprimas celdas por publicabilidad.
2. `salida/diagnostico.json`: por llave, n válido y exclusiones por causa; y las decisiones de implementación que tomaste donde la spec admitía más de una lectura, cada una con la frase que la motiva.
3. `salida/codigo/`: todo tu código; `python3 salida/codigo/reconstruye.py`, desde el directorio de trabajo, regenera los archivos 1–2 desde `paquete/`.
4. `salida/entorno.txt`: versiones de python, numpy, pandas y de cualquier lector usado, y `uname -a`.
5. `salida/archivos-leidos.txt`: cada ruta que abriste, una por línea.
6. `salida/insuficiencias.md`: lo que la spec humana no alcanzó a fijar, por llave o grupo; «Ninguna.» si nada.

## Reglas

- Si falta método, acceso o un dato, informa el faltante sin adivinar (`NO-RECALCULABLE-DESDE-SPEC` con `motivo`).
- El primer resultado completo que produzca tu código es el que se entrega. No tienes valores esperados y no debes buscarlos.
- Trabaja por lotes si el esquema es grande; no dejes llaves sin fila.
- Al terminar, escribe el sha256 de cada archivo de `salida/` en `salida/SELLO.txt` y no modifiques nada después.
- La última línea de tu respuesta final es `RECONSTRUCCION-TERMINADA sha256(resultado.json)=<hex>`.
