# ACTO MAESTRA35-L5 · P1 — regresión del corredor R, salida cruda

Fecha: 2/sep/2026. Control obligatorio del encargo: tras añadir el lector `.dta`,
el ruteo por contenido y la gramática de join, **ninguna R existente puede
moverse**. Se corrió sobre las **29** celdas con `corridas-R/<id>.json` (todas
las que hay, sin `_*`), no sólo sobre las del sorteado — es el máximo honesto.

Comando:

```
IDS=$(ls -1 forense/prereg-duelo-v2/corridas-R/*.json | xargs -n1 basename \
      | sed 's/\.json$//' | grep -v '^_' | tr '\n' ' ')
python3 tools/arbitra.py --regresion $IDS
```

## Veredicto

- **19 COINCIDE · 10 NO-COINCIDE**, exit 1.
- **El diff contra la misma corrida ANTES del cambio es VACÍO, byte a byte.**
  Es el control que importa: los 10 `NO-COINCIDE` ya estaban ahí en `4d7bd1e`,
  no los produjo este acto.
- Las **9** celdas del sorteado `v1_2` que ya tenían R (`CIV-M-01/02/04/10/12/13`,
  `FAM-M-01`, `TRA-M-03`, `TRA-M-07`): **9 de 9 COINCIDE**.
- Los 10 `NO-COINCIDE`, clasificados: **6** «sin fila en `codificacion-R-v1_0.tsv`»
  (`DIN-07`, `DOC-06`, `EMP-02`, `EMP-04`, `EMP-05`, `TIC-06` — se calcularon a
  mano en `correr-R.py`, nunca desde la tabla); **3** «tabla declara join»
  (`DIN-03`, `TIC-01`, `TIC-12` — el join va en la columna `tabla`, que esta
  gramática no toca: sólo se formalizó el join del **ponderador**); **1**
  diferencia numérica (`DIN-05`), que es el límite ya declarado por
  `/arbitra` §CODIFICA-R-1 — esa celda necesita el filtro real `TLOC=='4'` y
  `universo_filtro` es prosa informativa, no código.

Ninguno de los tres motivos es un efecto de este acto, y ninguno cambió.

## Salida cruda completa

```
CIV-08: COINCIDE
    R: nuevo=0.6187957719383738 == existente=0.6187957719383738
    EE_R: nuevo=0.0026966819047004064 == existente=0.0026966819047004064
    n_efectivo: nuevo=90488 == existente=90488
    n_estratos: nuevo=607 == existente=607
    n_upm_total: nuevo=13085 == existente=13085
    advertencia: CIV-08: universo_filtro es informativo, NO se ejecuta como filtro ('poblacion de 18 anios y mas (TPer_Vic1)') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
CIV-M-01: COINCIDE
    R: nuevo=0.25899878251638075 == existente=0.25899878251638075
    EE_R: nuevo=0.006970703455227148 == existente=0.006970703455227148
    n_efectivo: nuevo=26848 == existente=26848
    n_estratos: nuevo=358 == existente=358
    n_upm_total: nuevo=9129 == existente=9129
    advertencia: CIV-M-01: universo_filtro es informativo, NO se ejecuta como filtro ("delitos captados en TMod_Vic, seccion 'I. Todos los tipos de delito' (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es 'b' (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido, sin necesidad de filtrar por BP1_20 aparte") -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-01: tabla logica 'TMod_Vic' resuelta a miembro fisico 'Tmod_Vic.DBF' dentro de envipe2012/base_de_datos_envipe_2012_dbf.zip
CIV-M-02: COINCIDE
    R: nuevo=0.24339981393062482 == existente=0.24339981393062482
    EE_R: nuevo=0.0062378246817035195 == existente=0.0062378246817035195
    n_efectivo: nuevo=40889 == existente=40889
    n_estratos: nuevo=268 == existente=268
    n_upm_total: nuevo=10526 == existente=10526
    advertencia: CIV-M-02: universo_filtro es informativo, NO se ejecuta como filtro ('delitos captados en TMod_Vic, seccion I. Todos los tipos de delito (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es b (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-02: tabla logica 'TMod_Vic' resuelta a miembro fisico 'tmod_vic.dbf' dentro de envipe2013/bd_envipe13_dbf.zip
CIV-M-04: COINCIDE
    R: nuevo=0.24366832225578466 == existente=0.24366832225578466
    EE_R: nuevo=0.007483508419929803 == existente=0.007483508419929803
    n_efectivo: nuevo=39286 == existente=39286
    n_estratos: nuevo=238 == existente=238
    n_upm_total: nuevo=9477 == existente=9477
    advertencia: CIV-M-04: universo_filtro es informativo, NO se ejecuta como filtro ('delitos captados en TMod_Vic, seccion I. Todos los tipos de delito (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es b (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-04: tabla logica 'TMod_Vic' resuelta a miembro fisico 'TMod_Vic.dbf' dentro de envipe2015/bd_envipe2015_dbf.zip
CIV-M-06: COINCIDE
    R: nuevo=0.22266825355486683 == existente=0.22266825355486683
    EE_R: nuevo=0.004906857683604998 == existente=0.004906857683604998
    n_efectivo: nuevo=39480 == existente=39480
    n_estratos: nuevo=589 == existente=589
    n_upm_total: nuevo=10631 == existente=10631
    advertencia: CIV-M-06: universo_filtro es informativo, NO se ejecuta como filtro ("delitos captados en TMod_Vic, seccion 'I. Todos los tipos de delito' (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es 'b' (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido, sin necesidad de filtrar por BP1_20 aparte") -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-06: tabla logica 'TMod_Vic' resuelta a miembro fisico 'BASE_DE_DATOS_ENVIPE_2017_en/TMod_Vic.dbf' dentro de envipe2017/bd_envipe2017_dbf.zip
CIV-M-08: COINCIDE
    R: nuevo=0.23469647267758384 == existente=0.23469647267758384
    EE_R: nuevo=0.00494511307367627 == existente=0.00494511307367627
    n_efectivo: nuevo=40768 == existente=40768
    n_estratos: nuevo=231 == existente=231
    n_upm_total: nuevo=10599 == existente=10599
    advertencia: CIV-M-08: universo_filtro es informativo, NO se ejecuta como filtro ("delitos captados en TMod_Vic, seccion 'I. Todos los tipos de delito' (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es 'b' (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido, sin necesidad de filtrar por BP1_20 aparte") -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-08: tabla logica 'TMod_Vic' resuelta a miembro fisico 'conjunto_de_datos_TMod_Vic_ENVIPE_2019/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2019.csv' dentro de envipe2019_csv.zip
CIV-M-09: COINCIDE
    R: nuevo=0.20380888238780775 == existente=0.20380888238780775
    EE_R: nuevo=0.005373888352139425 == existente=0.005373888352139425
    n_efectivo: nuevo=33717 == existente=33717
    n_estratos: nuevo=598 == existente=598
    n_upm_total: nuevo=9785 == existente=9785
    advertencia: CIV-M-09: universo_filtro es informativo, NO se ejecuta como filtro ("delitos captados en TMod_Vic, seccion 'I. Todos los tipos de delito' (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es 'b' (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido, sin necesidad de filtrar por BP1_20 aparte") -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-09: tabla logica 'TMod_Vic' resuelta a miembro fisico 'conjunto_de_datos_TMod_Vic_ENVIPE_2020/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2020.csv' dentro de envipe2020_csv.zip
CIV-M-10: COINCIDE
    R: nuevo=0.20493399286059008 == existente=0.20493399286059008
    EE_R: nuevo=0.004773432921089039 == existente=0.004773432921089039
    n_efectivo: nuevo=32967 == existente=32967
    n_estratos: nuevo=597 == existente=597
    n_upm_total: nuevo=9903 == existente=9903
    advertencia: CIV-M-10: universo_filtro es informativo, NO se ejecuta como filtro ('delitos captados en TMod_Vic, seccion I. Todos los tipos de delito (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es b (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-10: tabla logica 'TMod_Vic' resuelta a miembro fisico 'conjunto_de_datos_TMod_Vic_ENVIPE_2021/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2021.csv' dentro de envipe2021_csv.zip
CIV-M-11: COINCIDE
    R: nuevo=0.2131254114226205 == existente=0.2131254114226205
    EE_R: nuevo=0.0050611745257689526 == existente=0.0050611745257689526
    n_efectivo: nuevo=32052 == existente=32052
    n_estratos: nuevo=602 == existente=602
    n_upm_total: nuevo=9897 == existente=9897
    advertencia: CIV-M-11: universo_filtro es informativo, NO se ejecuta como filtro ('delitos captados en TMod_Vic, seccion I. Todos los tipos de delito (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es b (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-11: tabla logica 'TMod_Vic' resuelta a miembro fisico 'conjunto_de_datos_TMod_Vic_ENVIPE_2022/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2022.csv' dentro de envipe2022_csv.zip
CIV-M-12: COINCIDE
    R: nuevo=0.20811159524290274 == existente=0.20811159524290274
    EE_R: nuevo=0.004760266232118154 == existente=0.004760266232118154
    n_efectivo: nuevo=31012 == existente=31012
    n_estratos: nuevo=602 == existente=602
    n_upm_total: nuevo=9745 == existente=9745
    advertencia: CIV-M-12: universo_filtro es informativo, NO se ejecuta como filtro ('delitos captados en TMod_Vic, seccion I. Todos los tipos de delito (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es b (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-12: tabla logica 'TMod_Vic' resuelta a miembro fisico 'tmod_vic_envipe2023/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2023.csv' dentro de envipe2023_csv.zip
CIV-M-13: COINCIDE
    R: nuevo=0.1946118021509308 == existente=0.1946118021509308
    EE_R: nuevo=0.005391415046889411 == existente=0.005391415046889411
    n_efectivo: nuevo=33108 == existente=33108
    n_estratos: nuevo=600 == existente=600
    n_upm_total: nuevo=9654 == existente=9654
    advertencia: CIV-M-13: universo_filtro es informativo, NO se ejecuta como filtro ('delitos captados en TMod_Vic, seccion I. Todos los tipos de delito (aplica a todo tipo de delito, no solo a uno); sin filtro adicional mas alla de la codificacion -- BP1_23 es b (blanco) para quien SI denuncio (BP1_20==1), caso que ya queda fuera por codigo no valido') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: CIV-M-13: tabla logica 'TMod_Vic' resuelta a miembro fisico 'tmod_vic_envipe2024/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2024.csv' dentro de envipe2024_csv.zip
DIN-03: NO-COINCIDE
    motivo: DIN-03: tabla declara join ('stmodulo2_e2.dbf  (join stsdem_e2.dbf por CONTROL+VIV_SEL+HOGAR+R_SEL=N_REN)'), no reproducible desde la tabla de codificacion sola
DIN-05: NO-COINCIDE
    R: nuevo=0.025232664961309593 != existente=0.017270753258714914
    EE_R: nuevo=0.0011884869624616695 != existente=0.0020262787920031222
    n_efectivo: nuevo=40940 != existente=8629
    n_estratos: nuevo=407 != existente=52
    n_upm_total: nuevo=3270 != existente=229
    advertencia: DIN-05: universo_filtro es informativo, NO se ejecuta como filtro ("personas de 18+ en localidades menores de 2 500 habitantes (TLOC=='4')") -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
DIN-07: NO-COINCIDE
    motivo: DIN-07: sin fila en codificacion-R-v1_0.tsv
DIN-11: COINCIDE
    R: nuevo=0.4583913965555015 == existente=0.4583913965555015
    EE_R: nuevo=0.007241245036334212 == existente=0.007241245036334212
    n_efectivo: nuevo=12446 == existente=12446
    n_estratos: nuevo=182 == existente=182
    n_upm_total: nuevo=1908 == existente=1908
    advertencia: DIN-11: universo_filtro es informativo, NO se ejecuta como filtro ('personas de 18 a 70 anios, persona elegida del hogar (la tabla ya es ese universo)') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
DOC-06: NO-COINCIDE
    motivo: DOC-06: sin fila en codificacion-R-v1_0.tsv
EMP-02: NO-COINCIDE
    motivo: EMP-02: sin fila en codificacion-R-v1_0.tsv
EMP-04: NO-COINCIDE
    motivo: EMP-04: sin fila en codificacion-R-v1_0.tsv
EMP-05: NO-COINCIDE
    motivo: EMP-05: sin fila en codificacion-R-v1_0.tsv
FAM-M-01: COINCIDE
    R: nuevo=0.5571925669683186 == existente=0.5571925669683186
    EE_R: nuevo=0.006766711249146834 == existente=0.006766711249146834
    n_efectivo: nuevo=12054 == existente=12054
    n_estratos: nuevo=182 == existente=182
    n_upm_total: nuevo=1908 == existente=1908
    advertencia: FAM-M-01: universo_filtro es informativo, NO se ejecuta como filtro ('la tabla ya es ese universo (personas seleccionadas de tmodulo2, seccion 9.9); sin filtro adicional declarado en el diccionario') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
    advertencia: FAM-M-01: tabla logica 'tmodulo2' resuelta a miembro fisico 'conjunto_de_datos_tmodulo2_enif_2018/conjunto_de_datos/conjunto_de_datos_tmodulo2_enif_2018.csv' dentro de enif2018_csv.zip
SFT-04: COINCIDE
    R: nuevo=0.0604055335123943 == existente=0.0604055335123943
    EE_R: nuevo=0.004140846076745225 == existente=0.004140846076745225
    n_efectivo: nuevo=10103 == existente=10103
    n_estratos: nuevo=128 == existente=128
    n_upm_total: nuevo=4555 == existente=4555
    advertencia: SFT-04: universo_filtro es informativo, NO se ejecuta como filtro ('personas de 50+ y conyuge, entrevista directa (la tabla ya es ese universo)') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
SFT-06: COINCIDE
    R: nuevo=0.5644892941458121 == existente=0.5644892941458121
    EE_R: nuevo=0.014451235132239474 == existente=0.014451235132239474
    n_efectivo: nuevo=6380 == existente=6380
    n_estratos: nuevo=4 == existente=4
    n_upm_total: nuevo=4093 == existente=4093
    advertencia: SFT-06: universo_filtro es informativo, NO se ejecuta como filtro ('personas de 50+ y conyuge, entrevista directa (la tabla ya es ese universo)') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
TIC-01: NO-COINCIDE
    motivo: TIC-01: tabla declara join ('COE1 join SDEM'), no reproducible desde la tabla de codificacion sola
TIC-06: NO-COINCIDE
    motivo: TIC-06: sin fila en codificacion-R-v1_0.tsv
TIC-08: COINCIDE
    R: nuevo=0.9044714694763597 == existente=0.9044714694763597
    EE_R: nuevo=0.0023885166040940498 == existente=0.0023885166040940498
    n_efectivo: nuevo=47240 == existente=47240
    n_estratos: nuevo=437 == existente=437
    n_upm_total: nuevo=8741 == existente=8741
    advertencia: TIC-08: universo_filtro es informativo, NO se ejecuta como filtro ('persona elegida de 6 anios y mas (tabla tic_2024_usuarios)') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
TIC-12: NO-COINCIDE
    motivo: TIC-12: tabla declara join ('COE1 join SDEM'), no reproducible desde la tabla de codificacion sola
TRA-M-03: COINCIDE
    R: nuevo=0.04453797671500066 == existente=0.04453797671500066
    EE_R: nuevo=0.002841169356265617 == existente=0.002841169356265617
    n_efectivo: nuevo=22081 == existente=22081
    n_estratos: nuevo=180 == existente=180
    n_upm_total: nuevo=6510 == existente=6510
    advertencia: TRA-M-03: universo_filtro es informativo, NO se ejecuta como filtro ("de los 33000 registros de la tabla (roster de vivienda+persona), 4617 son menores de 18 (FAC_P18<=0, correctamente fuera del universo 18+); de los 28383 restantes (18 anios y mas), 22653 (79.8%) tienen respuesta individual valida en la seccion VIII y 5730 (20.2%) quedan en blanco en P8_3 pese a que la vivienda muestra R_DEF=00 (entrevista de vivienda completa) -- no-respuesta a nivel PERSONA (R_ELE con codigo distinto de 01 en su mayoria), distinta de la no-respuesta a nivel vivienda; arbitra.py los excluye igual que a cualquier codigo invalido (blanco no calza '1' ni '2'), tratamiento estandar de no-respuesta. R se calcula sobre los 22653 adultos con respuesta valida. Este patron NO aparece en 2017/2021 (~0.2-0.4% en blanco): las tablas de datos abiertos de esas olas ya vienen filtradas al informante entrevistado, mientras que la tabla de 2013 conserva una fila por cada miembro del hogar en el roster, responda o no la seccion VIII -- diferencia de estructura de tabla entre olas, no de universo pretendido (las tres apuntan a poblacion de 18 anios y mas)") -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
TRA-M-05: COINCIDE
    R: nuevo=0.07702449888267587 == existente=0.07702449888267587
    EE_R: nuevo=0.0022211223298215415 == existente=0.0022211223298215415
    n_efectivo: nuevo=39085 == existente=39085
    n_estratos: nuevo=357 == existente=357
    n_upm_total: nuevo=9138 == existente=9138
    advertencia: TRA-M-05: universo_filtro es informativo, NO se ejecuta como filtro ('la tabla ya es el universo de la seccion VIII (39165 filas = 36091 No + 2994 Si + 80 No sabe, exacto, cero blancos); sin filtro adicional') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
TRA-M-07: COINCIDE
    R: nuevo=0.07181522879909936 == existente=0.07181522879909936
    EE_R: nuevo=0.002396371861039179 == existente=0.002396371861039179
    n_efectivo: nuevo=39763 == existente=39763
    n_estratos: nuevo=353 == existente=353
    n_upm_total: nuevo=9190 == existente=9190
    advertencia: TRA-M-07: universo_filtro es informativo, NO se ejecuta como filtro ('la tabla ya es el universo de la seccion VIII (39930 filas = 37168 No + 2595 Si + 167 No sabe, exacto, cero blancos); sin filtro adicional') -- si esta celda necesita un filtro real, este calculo sera incorrecto y debe salir NO-COINCIDE.
```

## Diff contra la corrida previa al cambio

```
$ diff regresion-ANTES.txt regresion-DESPUES.txt
$ echo $?
0
```

Vacío. El lector `.dta`, el ruteo por magic de Stata y la gramática de join no
alteran ni una cifra de las 29 celdas ya corridas.

---

## Segunda corrida — tras resolver `SUSTITUYE-A` (P1-bis)

`--produce forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv DIN-M-01`, que es lo
que el encargo manda correr, tiene que usar la fila `DIN-M-01b` y escribir
`corridas-R/DIN-M-01.json` — `DIN-M-01` es el id de la celda en el sorteado y es
el nombre por el que la puntuación la buscará; `DIN-M-01b` es sólo la fila de
codificación que la sustituye. Sin resolver `SUSTITUYE-A`, pedir `DIN-M-01`
seguía entregando la fila vieja (ponderador en prosa, diseño
`NO-DECLARADO-EN-LA-FUENTE`) y la corrida habría salido `SIN_FILAS`.

`lee_codificacion()` ahora resuelve la convención. Efecto medido sobre la tabla:

```
DIN-M-01  -> DIN-M-01b | fac_3b@ehh02w_all/ehh02w_b3b.dta[folio+ls]
DIN-M-01b -> DIN-M-01b
TRA-M-13  -> TRA-M-13b | TRA-M-14 -> TRA-M-14b
n ids: 37
```

`TRA-M-13`/`TRA-M-14` también cambian de fila — la convención ya estaba en el
archivo desde el 2/sep y **ninguna herramienta la leía**. Ninguna de las dos
tiene `corridas-R/*.json`, así que no toca ninguna R existente. Se declara aquí
porque es un efecto de este acto sobre celdas ajenas, aunque hoy sea inerte.

Regresión repetida sobre las mismas 29 celdas:

```
COINCIDE=19  NO-COINCIDE=10
$ diff regresion-ANTES.txt regresion-DESPUES2.txt
$ echo $?
0
```

**Sigue vacío.** Ni el lector, ni el ruteo por contenido, ni el join, ni la
resolución de `SUSTITUYE-A` mueven una sola cifra de las 29 R ya corridas.
