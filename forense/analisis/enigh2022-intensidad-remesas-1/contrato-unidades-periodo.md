# Contrato de unidades y periodo

## Identidad acreditada

| pieza | evidencia oficial | consecuencia para esta medición |
|---|---|---|
| `remesas` | Diccionario interno del ZIP y *Descripción de la base de datos*, p. 197: suma de `ingresos.ing_tri` cuando la clave es P041; P041 es “Ingresos provenientes de otros países”. | Monto de remesas del hogar; no una marca binaria ni un flujo bancario externo. |
| `ing_cor` | Diccionario interno y *Descripción*, p. 194: suma de `ingtrab`, `rentas`, `transfer`, `estim_alqu` y `otros_ing`; `transfer` incluye `remesas`. | El denominador incluye el numerador como componente documentado. |
| periodo | *Descripción*, p. 17: todos los ingresos y gastos de `concentradohogar` son trimestrales; p. 123: `ing_tri` es trimestral y normalizado según la decena de levantamiento. | `remesas` e `ing_cor` comparten trimestre normalizado; el cociente es identificable. |
| moneda | *Nota técnica*, pp. 3-5: presenta el ingreso corriente promedio trimestral en pesos y señala las cifras comparativas en pesos de 2022. | Encabezado adoptado: “pesos de 2022 por trimestre normalizado”. No se deflacta ni anualiza. |
| unidad de análisis | Metadato interno y *Descripción*, pp. 10 y 17: hogar; llave foránea `folioviv+foliohog`. | Una fila por hogar; `factor` expande hogares. |

## Objetos registrados

- Microdato: `enigh2022_nc_csv`, SHA-256
  `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06`.
- Descripción oficial: `enigh2022_descripcion_base_pdf`, SHA-256
  `7b0c4e6bd36ceb9eae7cc852fce5a38dbcf4f2da6b133d35df6b1443fc76836c`.
- Nota técnica oficial: `enigh2022_nota_tecnica_pdf`, SHA-256
  `4f79f457d69c1f066d7fd319b1650f7b631f4008cb74e1046e6c644c65be0647`.

Los PDF son documentos metodológicos; no agregan una muestra estadística. El
miembro estadístico abierto fue únicamente el concentrado de hogares fijado en
la spec. No se abrieron tablas de población, ingresos individuales, trabajos o
gastos.

## Comprobación de componente

La tolerancia, fijada antes de leer los montos, fue `0.01` pesos. En el dominio
de participación hubo **0 hogares** y masa ponderada **0** con
`remesas > ing_cor + 0.01`. No se truncó ningún cociente ni se eliminó un
extremo para hacer cumplir la identidad.
