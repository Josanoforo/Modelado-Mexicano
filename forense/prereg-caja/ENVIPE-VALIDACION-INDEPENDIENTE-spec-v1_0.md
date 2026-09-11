# ENVIPE · validación independiente de ocho puntos y lectura 2010–2024

### `prereg-caja-ENVIPE-VALIDACION-INDEPENDIENTE-v1_0` · 10 de septiembre de 2026

Esta receta se congela antes de ejecutar `tools/valida_envipe_independiente.py`
y antes de crear cualquiera de sus salidas. Los valores publicados por los
ocho CALC ya son conocidos: es una validación técnica independiente, no un
arbitraje ciego ni una medición científica adicional.

## 1. Objeto, autoridad y separación

Se reconstruye exclusivamente

`p(C1,U1) = sum(FAC_DEL * 1[respuesta en {01,02,06}]) / sum(FAC_DEL)`

donde `U1` contiene delitos personales, `BP1_20=2`, respuesta `01..08` y
`FAC_DEL` finito y positivo. La unidad es **delito**. La autoridad semántica es
el cuestionario y la especificación sellada
`forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md`; el archivo canónico
`data/corrida0/envipe-serie-denuncia-v1_0.tsv` aporta la serie a graficar.

El validador no importa `tools/medidor_envipe_serie_completa.py`,
`tests/svystat.py`, los `medidor.py` de los CALC ni código de bootstrap. Usa
`zipfile`/`csv` de la biblioteca estándar, un lector mínimo de cabecera,
descriptores y registros dBase III/IV, y `decimal.Decimal` para acumular las
masas. Los CALC, sus specs y el motor son de lectura.

## 2. Mapa congelado

| ola | año hecho | ZIP / SHA256 | miembro | formato | respuesta | personales | estrato / UPM |
|---:|---:|---|---|---|---|---|---|
| 2011 | 2010 | `envipe2011/base_de_datos_envipe_2011_dbf.zip` / `d6c660f00ca2179dcabf59a9af166d7605793eed48c6eb84bcd8d24f39bd2ce4` | `tmod_vic.DBF` | DBF | `BP1_21` | `04..14` | `EST` / `UPM` |
| 2014 | 2013 | `envipe2014/bd_envipe2014_dbf.zip` / `8f1d0eb519a0ceabe36d187d9a49734dbef97f219b86eea9084ebd1818973f77` | `bd_envipe2014/bd_envipe2014/TMod_Vic.dbf` | DBF | `BP1_23` | `05..15` | `EST` / `UPM` |
| 2016 | 2015 | `envipe2016/bd_envipe2016_dbf.zip` / `8c939550590bbb7941c65a2c9a3d87d8654cfe529e969f51265fe65974ef68a4` | `TMod_Vic.dbf` | DBF | `BP1_23` | `05..15` | `EST_DIS` / `UPM_DIS` |
| 2017 | 2016 | `envipe2017/bd_envipe2017_dbf.zip` / `86df9910dae338d4c4487e6760e8e3ba1a752c8a8fcda967a8af152ad49d8f74` | `BASE_DE_DATOS_ENVIPE_2017_en/TMod_Vic.dbf` | DBF | `BP1_23` | `05..15` | `EST_DIS` / `UPM_DIS` |
| 2018 | 2017 | `envipe2018_csv.zip` / `aa279993bfeaaa0bf0d821e964887140ef444f6e695e4e1767f6512e4d2c4723` | `conjunto_de_datos_tmod_vic_envipe_2018/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe_2018.csv` | CSV | `BP1_23` | `05..15` | `EST_DIS` / `UPM_DIS` |
| 2019 | 2018 | `envipe2019_csv.zip` / `24bb83987f2ba57912a3f55c8ff3bb48e5f39f2292cd167997312c1fd77207f3` | `conjunto_de_datos_TMod_Vic_ENVIPE_2019/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2019.csv` | CSV | `BP1_23` | `05..15` | `EST_DIS` / `UPM_DIS` |
| 2020 | 2019 | `envipe2020_csv.zip` / `26f468da631bfdb94994a9e5051fa973468608f0da56612b6897df16a2797b9d` | `conjunto_de_datos_TMod_Vic_ENVIPE_2020/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2020.csv` | CSV | `BP1_23` | `05..15` | `EST_DIS` / `UPM_DIS` |
| 2022 | 2021 | `envipe2022_csv.zip` / `3a6e0f3a05dd4120efe8072de519402a39f4ed1690593433a68bb2ee137e77bb` | `conjunto_de_datos_TMod_Vic_ENVIPE_2022/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2022.csv` | CSV | `BP1_23` | `05..15` | `EST_DIS` / `UPM_DIS` |

En todas las olas las otras variables son `BPCOD`, `BP1_20` y `FAC_DEL`.
La rama 2011 conserva `BP1_21`, personales `04..14`, residuos `88/98/99` y
diseño `EST/UPM`; 2014 comprueba la otra lectura DBF; 2018–2022 comprueban la
rama CSV. El hash del ZIP se verifica antes de leer.

## 3. Embudo, salidas y aceptación

Cada fila recibe una sola salida en este orden: (1) `BPCOD` no personal; (2)
`BP1_20` distinto de 2; (3) respuesta fuera de `01..08`; (4) ponderador no
finito o no positivo; (5) incluida. Los excluidos se tabulan por etapa y código.
Por ola se escriben numerador ponderado, denominador ponderado, `n` incluido,
punto reconstruido, referencias selladas y diferencias.

La tolerancia se fija ahora y no se ajustará tras ver salidas:

- punto: diferencia absoluta `<= 1e-10` (equivale a `1e-8` puntos
  porcentuales, muy por debajo de la precisión publicada);
- `n`: igualdad exacta;
- denominador `FAC_DEL`: igualdad decimal exacta con
  `MASA-FAC-DEL-U1` del CALC.

Una diferencia mayor se conserva como discrepancia material y se rastrea por
universo, código y peso; no se reescribe el resultado sellado.

## 4. Comprobación de incertidumbre

Caso representativo preelegido: ola **2019** (CSV, `EST_DIS/UPM_DIS`). Se
calcula una linealización directa de la razón: para cada UPM se totaliza
`z=w(y-p)` y dentro de cada estrato se suma
`m_h/(m_h-1) * sum((z_hi - mean_h)^2)`; los estratos de UPM única aportan cero,
se declaran y hacen que la anchura sea límite inferior. El EE es la raíz de esa
varianza dividida por el denominador; el IC de referencia usa `p ± 1.96*EE`,
recortado a `[0,1]`.

Esta receta es materialmente distinta del bootstrap percentil original y no
pretende reproducir sus 2,000 réplicas. Se compara además con el IC analítico
sellado sólo para diagnosticar implementación. Se considera diferencia capaz
de cambiar la lectura si el EE difiere más de 10% o algún extremo más de 0.002
(0.2 puntos porcentuales). No se exige igualdad con el IC bootstrap. No se
hace contraste formal entre años: requeriría una hipótesis propia de
covarianza entre olas.

## 5. Producto descriptivo

La figura y su tabla de trazabilidad leen el TSV canónico, sin crear una serie
alternativa. Mostrarán año del hecho 2010–2024, punto e IC bootstrap, y
marcarán la ruptura nominal/residual de la ola 2011. La etiqueta completa dirá
que es la proporción ponderada por `FAC_DEL` de motivos `01/02/06` entre
delitos personales no denunciados con respuesta `01..08`. La lectura será
descriptiva y exploratoria: no es tasa general de denuncia, no adopta un
parámetro y no atribuye causalidad.
