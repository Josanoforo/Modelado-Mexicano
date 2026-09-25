# Pisos de consumo y gasto por segmento, ENIGH 2016–2022 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1`, 25/sep/2026, CAJA, rama
`acto/gen2-consumo-y-gasto-pisos-1`, 0-bis `2d37b23b`. Encargo:
`forense/encargos/2026-09-25-GEN2-CONSUMO-Y-GASTO-PISOS-1.md` (P2). CALC:
`CALC-ENIGH-CONSUMO-PISOS-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor
de microdato ENIGH (de los CSV sólo se leyó la primera línea; catálogos y diccionarios sí).
**El primer resultado que produzca este procedimiento es el que se reporta.**

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

Sintético en `tests/test_consumo_pisos_gen2.py` (todas las ramas terminales pasan
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
