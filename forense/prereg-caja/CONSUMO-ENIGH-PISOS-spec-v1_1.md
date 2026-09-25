# Pisos de consumo y gasto por segmento, ENIGH 2016–2022 · spec v1.1

**Pre-registro de caja.** `ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1`, 25/sep/2026, CAJA, rama
`acto/gen2-consumo-y-gasto-pisos-1`, 0-bis `2d37b23b`. Encargo:
`forense/encargos/2026-09-25-GEN2-CONSUMO-Y-GASTO-PISOS-1.md` (P2). CALC:
`CALC-ENIGH-CONSUMO-PISOS-0002`, sucesor de `CALC-ENIGH-CONSUMO-PISOS-0001` (spec v1.0,
`forense/prereg-caja/CONSUMO-ENIGH-PISOS-spec-v1_0.md`, COMMIT-1 `5b2dc18c`, sellado en
`55d7def9`). Congelada en commit propio **antes** de correr 0002. **Esta sesión ya abrió el
microdato ENIGH 2016–2022** al correr 0001 (declarado); v1.1 no cambia qué se mide.
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0-bis · Qué cambia respecto de v1.0, y por qué (tercer commit, nunca corrección hacia atrás)

- `[EJECUTADO]` El sello de 0001 emitió `G-2016-FILAS-GASTO = G-2018-FILAS-GASTO = 1048575`
  frente a 4 484 151 (2020) y 4 645 690 (2022). El miembro
  `conjunto_de_datos_gastoshogar_enigh_{2016,2018}_ns.csv` de `enigh{2016,2018}_nc_csv` tiene
  1 048 576 líneas (encabezado + 1 048 575, límite de filas de Excel) y termina a mitad de la
  entidad 19 (`folioviv` 19…): el archivo del ZIP integrado está **truncado**. Toda conducta
  de 0001 construida desde `gastoshogar` en 2016 y 2018 (PART-EFECTIVO-EN-GASTO-DIRECTO,
  PART-CANAL-*, HOG-COMPRA-FIADO, HOG-COMPRA-TARJETA-CREDITO, HOG-COMPRA-INTERNET,
  HOG-COMPRA-INTERNET-SI-CONEXION) no es válida para esas olas, ni su τ² ni su IC calibrado
  2022. Las conductas desde `concentradohogar` y `hogares` no se afectan.
- `[EJECUTADO]` El corpus trae la descarga **por tabla**
  `cc1_inegi_enigh_2016__enigh2016_ns_gastoshogar_csv` (sha256 `e5d04873…`, miembro
  `gastoshogar.csv`, 4 190 742 líneas, termina en entidad 32) y
  `cc1_inegi_enigh_2018__enigh2018_ns_gastoshogar_csv` (`b2ac3c59…`, 4 405 251 líneas, termina
  en entidad 32), mismo encabezado. **Único cambio de v1.1:** `gastoshogar` 2016 y 2018 se
  lee de esas dos descargas. Lista cerrada, universo, ejes, estimador, semilla (20260925) y
  réplicas (1 000): idénticos. 2020 y 2022 siguen del ZIP integrado.
- **Oro interno (declarado antes de correr):** toda RESULT de 0002 que no dependa de
  `gastoshogar` (PART de rubros, PART-COMUNICA, PART-ALI-FUERA/BEBIDAS, HOG-* de
  `concentradohogar`/`hogares`, MEDIA-*) debe ser **idéntica** a la de 0001 (misma semilla,
  mismo marco de UPM); las de 2020 y 2022 desde `gastoshogar` también. Una diferencia en
  cualquiera de ellas es defecto de 0002 y se reporta, no se corrige.

## 0 · Premisas verificadas

- `[EJECUTADO]` Olas abiertas: `enigh2016_nc_csv`, `enigh2018_nc_csv`, `enigh2020_nc_csv`,
  `enigh2022_nc_csv` (sha256 del manifiesto en `spec.yaml`). ENIGH 2024 RESERVADA
  (`data/corrida0/decisiones.tsv:192`, `reserva:enigh2024`; lo liberado en `:212` es sólo
  remesas>0 nacional y no se usa): **no es input**; la medidora PARA si lo fuera. ENIGH 2012
  y 2014 existen en corpus y no entran (el encargo fija 2016–2022; NC).
- `[EJECUTADO]` Trazado: encabezados de `concentradohogar`, `hogares`, `gastoshogar`
  idénticos en las cuatro olas para las columnas usadas; catálogos `lugar_comp`, `forma_pag`,
  `educa_jefe`, `tam_loc` idénticos 2016 y 2022. Los CSV traen BOM UTF-8: se leen con
  `encoding="utf-8-sig"` (argumento de la receta, que no se edita).
- `[EJECUTADO]` Remesas: `CALC-ENIGH{2016..2022}-REMESAS-CONTEXTO-0001` y
  `-INTENSIDAD-REMESAS-0001` sellados; se citan, no se re-miden.

## 1 · Unidad, universo, diseño

Unidad: **hogar** (`concentradohogar`, una fila por `folioviv`+`foliohog`), ponderador
`factor`, estrato `est_dis`, UPM `upm` (llaves opacas). Válido: `factor > 0`, estrato y UPM
no vacíos. `hogares` se une por llave (sólo llaves únicas; no pareados en
`G-<ola>-JOIN-SIN-HOGARES`). `gastoshogar`: sólo partidas `tipo_gasto = G1` (gasto
monetario para el hogar), agregadas por hogar; partidas sin hogar válido se cuentan en
`G-<ola>-FILAS-GASTO-SIN-HOGAR` y no entran. Un hogar sin partidas G1 tiene sumas 0.
`folioviv` se completa a 10 dígitos por la izquierda antes de unir.

## 2 · Conductas (por texto)

Tabla en `forense/analisis/consumo-gasto/lista-cerrada-P1.md` §2, parte de esta spec: 20
PART-* (razón de totales), 14 HOG-* (proporción de hogares), 1 MEDIA-* (pesos corrientes
por mes, no deflactados: la comparación entre olas de esa media **no** se lee como cambio
real). PART-* se estima con la receta pasando peso `factor·den` e `y = num/den` en los
hogares con `den > 0`, que da exactamente Σ factor·num / Σ factor·den con las mismas réplicas.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO-JEFE · EDAD-JEFE · ESCOLARIDAD-JEFE · TLOC · DECIL · ENTIDAD (sólo 5
conductas), definiciones en `lista-cerrada-P1.md` §5. **DECIL**: en cada ola, hogares
válidos ordenados por `ing_cor` (orden estable), participación acumulada del factor `a`;
decil = ⌈10·a⌉ acotado a 1..10 — un hogar que cruza un corte cae entero en el decil de su
extremo superior (deciles INEGI publicados pueden diferir en el hogar frontera).

## 4 · Estimación

Razón ponderada con bootstrap de UPM dentro de `est_dis` (certeza para UPM única,
`PCG64(20260925)`, 1 000 réplicas, percentiles 2.5/97.5, contrato conservador), receta común
`tools/dominios/salud/pisos_diseno.py` por sha256. **IC calibrado de persistencia** (método
`CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` §4, función `persistencia`/`ic_calibrado` de la
receta): para cada PART-* y HOG-* y cada eje, τ² = media de Δ² en logit entre olas
consecutivas 2016→2018→2020→2022 sobre las categorías del eje; sobre el piso 2022,
IC = expit(logit p ± 1.96·√(ee_m² + τ²)). 2020 (pandemia) entra como ola más: su Δ infla τ²
y eso es lo que el método declara, no se corrige. MEDIA-* sin IC calibrado.

## 5 · Controles, secuencia

Sintético en `tests/test_consumo_pisos_gen2.py` (cubre 0001 y 0002) (todas las ramas terminales pasan
`corrida0._valida_outputs`; `resultados:` = `esquema_resultados()`; la razón de totales por
peso `w·den` coincide con Σw·num/Σw·den). Oro: ningún piso GEN2 de consumo previo
(`ls data/corrida0 | grep -ic 'ENGASTO\|CONSUMO'` = 1 al COMMIT-1, y es
`ensafi2023-fichas-consumo-v1_0.tsv`, fichas ENSAFI, no un CALC). Control externo
post-sello (no toca el procedimiento): participación de alimentos en el gasto monetario y
proporción de hogares con celular contra los tabulados publicados de ENIGH 2016–2022 si
están en corpus; si no, se declara NO-VERIFICABLE-AQUÍ. Ninguna ejecución diagnóstica sobre
microdato antes del sello.

## 6 · Auditoría (afirma sobre México)

**Escala:** PART-* son participaciones del gasto agregado (razón de totales), no la
participación del hogar típico; HOG-* son hogares, no personas; nada se traslada a persona.
**Estructura antes que cultura:** canal, crédito y fiado dependen de oferta (tamaño de
localidad, bancarización, presencia de formatos); la columna de oferta de P1 §4 va al lado de
cada marginal y la nota no lee un gradiente por decil o TLOC como «preferencia». **Precios:**
la media en pesos corrientes no se compara entre olas. **2020:** ola de pandemia; un salto
2018→2020→2022 es primero choque, no rasgo. **Autorreporte:** diario de gasto de una semana
y cuestionarios de periodo; `gasto_tri` está trimestralizado por INEGI. **Cifra escrita a
mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
