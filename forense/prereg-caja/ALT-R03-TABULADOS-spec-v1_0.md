# R03 + R08 · ENCRIGE 2020 y ENVE 2024 · corrupción en trámites por unidad económica, tamaño y sector, con «conocimiento por terceros» como cota superior

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CALC-ALTERNOS-LOTE-1` (0-bis `795b1053`). Firmas del 28/sep/2026:
R02 ENCRIGE 2020 y R03 ENVE 2024 **ABIERTA-COMO-VISTA**; R10 I1 (d):
«ENAPROCE NO-ACCESIBLE para R03; R03 se funde con R08 sobre ENCRIGE/ENVE».
Dos CALC: `CALC-ALT-R03-ENCRIGE2020-0001` y `CALC-ALT-R03-ENVE2024-0001`.
Unidad **empresa / unidad económica**, descriptiva, **sin transferencia a
persona** (F-19). No adopta; sin retador ni θ.

## Qué hay en el corpus: tabulados, no microdato

`conjunto_de_datos_encrige_2020_csv` y `conjunto_de_datos_enve_2024_csv` son
los **tabulados** de datos abiertos (índice `0_indice_tablas_*.csv`, 392 y
413 miembros). El microdato de ENCRIGE es de Laboratorio (mapa: SOLICITUD
`TR_ENCRIGE2020`), no está en el corpus. Por eso este CALC extrae de
tabulados, con el mismo régimen que `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001`
(#826): estimaciones expandidas oficiales, sin EE/CV/n publicados, sin IC.
El cruce **tamaño × sector** no existe como tabulado: queda NO-CONSTRUIBLE
aquí (sólo tamaño y sector por separado).

## Qué ya está medido y no se repite (E.5)

#826 selló, de `t6_33` (tamaño), la prevalencia de corrupción del total y
por tamaño. Aquí `t6_33` · Participación se relee **sólo como control
positivo** (`RESULT-ENCRIGE-DES-PREVALENCIA-TOTAL-PROPORCION =
0.050985359248`, nacional), no como resultado nuevo. Lo nuevo: la
**cota superior** «conocimiento por terceros» y la «percepción de supuestos
actos» por tamaño (`t6_33`), las tres columnas por **gran sector** (`t6_34`)
y la victimización por corrupción de ENVE 2024 por sector (`t1_21`) y por
tamaño (`t1_22`).

## Tablas, columnas y filas (encabezados verbatim; ENCRIGE en latin-1, ENVE en UTF-8)

**ENCRIGE 2020** — universo: «Total de unidades económicas que realizaron al
menos un trámite o fueron sujetas a una inspección» (denominador); periodo
2020.
- `t6_33.csv` (Tamaño): dominios `Estados Unidos Mexicanos`, `Micro`,
  `Pequeña`, `Mediana`, `Grande`.
- `t6_34.csv` (Gran sector): `Estados Unidos Mexicanos`, `Comercio`,
  `Industria`, `Servicios`.
- Indicadores (numerador «…_Absolutos»; publicado «…_Tasa de prevalenciaN»
  por 10 000):
  - `PARTICIPACION` — «Participación en al menos un acto de corrupción».
  - `CONOCIMIENTO-TERCEROS` — «Conocimiento por terceros de actos de
    corrupción» (**cota superior**: «otras unidades le refirieron»).
  - `PERCEPCION` — «Percepción de supuestos actos de corrupción».

**ENVE 2024** — universo: «Unidades económicas» (denominador); año de
referencia 2023.
- `t1_21.csv` (Gran sector) y `t1_22.csv` (Tamaño), mismos dominios.
- Indicador `VICTIMA-CORRUPCION` — numerador «Víctimas por
  corrupción_Sí_Absolutos»; publicado «…_Sí_Relativos» (por 100).

## Estimando, escala, control

`p = absolutos / denominador` por dominio e indicador, proporción de unidades
económicas. Control de fórmula: `|p − publicado/escala| ≤ 5e-5` en todas
las celdas (media unidad del segundo decimal de un %, o de la unidad de una
tasa por 10 000: cubre el redondeo publicado); si alguna celda falla, el
control sale `FALLA` y se reporta, sin tocar la extracción. Un dominio o un
encabezado que no casa exactamente (normalizado sin acentos ni espacios
repetidos) detiene la corrida con error.

## Agregador (E.1)

Ninguno: una celda por (tabla, dominio, indicador). No se combinan ENCRIGE
(empresa, 2020) y ENVE (unidad económica, 2023) en una cifra.

## Qué pasa si el falsador no refuta

R03 (carga regulatoria y mordida en la MIPYME) no se prueba con tabulados de
unidad económica: la lectura es descriptiva (F-19). Si la participación en
Micro es mayor que en Grande, se reporta como gradiente descriptivo, no como
efecto del tamaño. La cota superior acota la participación declarada por
arriba; si «conocimiento por terceros» es menor que «participación» en
algún dominio, se reporta como anomalía y no se corrige.

## Auditoría v2.16

- **Unidad:** unidad económica / empresa (no persona; sin transferencia).
- **Escala:** proporción de unidades.
- **RETROSPECTIVA:** ENCRIGE 2020 y ENVE 2024, abiertas-como-vistas por
  firma (R02/R03).
- **¿Incentivo o psicología?** Conducta y conocimiento declarados por la
  empresa; el mecanismo (costo regulatorio frente a extracción) no se separa.
- **¿Clase media urbana?** Universo de establecimientos con instalaciones
  fijas; excluye informalidad sin local.
- **HOLDOUT gastado:** ninguno (R03/R08 no son momentos del catálogo).
  `holdout_gastado = NINGUNO`.
