# ENIGH · serie sobre olas abiertas · especificación humana v1.0

`ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, pieza P1. Congelada antes de abrir
`enigh2016_nc_csv`/`enigh2018_nc_csv`/`enigh2020_nc_csv` en este árbol (el
generador de los 9 `medidor.py`/`spec.yaml` de abajo corrió en un scratchpad
fuera del repo, contra los mismos zips, y se validó por oro-check en
`tests/test_enigh_serie_oro.py` antes de escribir este commit — el árbol del
acto no abrió microdato antes de este commit).

## 0. Premisa verificada contra el árbol (A.8, antes de escribir este documento)

El encargo (§1) afirma que los cuatro sellados de ENIGH 2022 nombrados están
"medidos en una sola ola". **Falso para uno de los cuatro:** `CALC-ENIGH-0001`
(`remesas>0`, unidad hogar, tasa base) ya está sellado en **cinco** olas —
2014/2016/2018/2020/2022 — por dos CALC ajenos a este acto
(`CALC-B-0001`, `CALC-B-MARCO-ENIGH-0001`), documentado en
`forense/prereg-caja/DISENO-duelo-prospectivo-ENIGH2024-v1_0.md §2.1` con
solapes verificados dígito a dígito. Es justo la lectura que el propio §1 del
encargo adelanta ("un solo estimando cumple la regla de entrada:
`remesas>0`") — **no hace falta re-correr `CALC-ENIGH-0001`**; el trabajo real
de P1 son los otros tres: `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003`,
`CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`, `CALC-ENIGH2022-REMESAS-CONTEXTO-0001`.

## 1. Ventana de olas: 2016–2022, no 2012–2022

`data/manifiesto.yaml`: `enigh2012_nc_csv`/`enigh2014_nc_csv` tienen
`url_origen` con el patrón `enigh_ncv_<año>_csv.zip` — "NCV", la metodología
anterior a la "nueva serie". `enigh2016_nc_csv` en adelante (2016, 2018,
2020, 2022, y `enigh2024_ns_csv.zip` reservada) usan el patrón
`..._nueva_serie_csv.zip` / `..._ns_csv.zip`. Confirmado también por
`RESULT-BM-ENIGH-2014-METADATO-VERSION` (`CALC-B-MARCO-ENIGH-0001`, sellado):
`identifier=MEX-INEGI.40.202.03-ENIGH-2014-NCV`. **2012 y 2014 quedan fuera de
la ventana de este acto por metodología distinta** (no solo porque
n salta de 19 479 en 2014 a 70 311 en 2016 — ese salto es SÍNTOMA del cambio
de diseño muestral, no la causa declarada). Ventana: **2016, 2018, 2020,
2022** (2022 ya sellado; 2016/2018/2020 se sellan en este acto). El encargo
declaraba esto como posible ("y 2012 si el corte de serie lo permite,
declarado") — se verificó y NO lo permite; queda declarado aquí.

## 2. Qué se corre: 3 CALC × 3 olas nuevas = 9 CALC nuevos

| Estimando (medidor original 2022) | 2016 | 2018 | 2020 |
|---|---|---|---|
| `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003` (personas, marginales+conjunta) | `CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001` | `CALC-ENIGH2018-PERFIL-ESTRUCTURAL-0001` | `CALC-ENIGH2020-PERFIL-ESTRUCTURAL-0001` |
| `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001` (hogares receptores) | `CALC-ENIGH2016-INTENSIDAD-REMESAS-0001` | `CALC-ENIGH2018-INTENSIDAD-REMESAS-0001` | `CALC-ENIGH2020-INTENSIDAD-REMESAS-0001` |
| `CALC-ENIGH2022-REMESAS-CONTEXTO-0001` (por tam_loc/est_socio) | `CALC-ENIGH2016-REMESAS-CONTEXTO-0001` | `CALC-ENIGH2018-REMESAS-CONTEXTO-0001` | `CALC-ENIGH2020-REMESAS-CONTEXTO-0001` |

Cada CALC nuevo es el **mismo procedimiento estadístico** del sellado 2022
(mismo universo, filtros, ponderador, transformación, categorías, método de
precisión, semilla y tolerancia — ver el `spec.md` propio de cada CALC para
el detalle completo, no se repite tres veces aquí), parametrizado por ola.
El único cambio de código, declarado y verificado (no un ajuste de
procedimiento — D-19(d) no aplica porque el procedimiento sellado en 2022
nunca se toca, esto es una generalización previa a abrir cualquier ola
nueva): en `poblacion.csv` de 2016/2018/2020, `factor`/`est_dis`/`upm` no
existen como columnas — se toman de `concentradohogar` por
`(folioviv, foliohog)`, verificado matemáticamente equivalente a lo que 2022
ya hace nativamente (1667/1667 personas de 500 hogares muestreados, cero
discordancias — ver `spec.md` de cada `*-PERFIL-ESTRUCTURAL-*`).

## 3. Oro: reproducción byte-exacta de 2022, verificada ANTES de sellar

`tests/test_enigh_serie_oro.py` reconfigura el `medidor.py` YA CONGELADO de
2016 (comparte código con 2018/2020 — no hay tres implementaciones) para leer
el zip de 2022 en vez del de 2016, y compara contra los tres
`resultados.json` ya sellados de 2022. Los tres pasan exacto:
`P1-MARGINALES-SHA256`/`P2-CONJUNTA-SHA256`/`P2-MARGINALES-COMPLETOS-SHA256`
de PERFIL-ESTRUCTURAL coinciden byte a byte; los 17 valores principales
(incluido el bootstrap de 2000 réplicas, bit a bit por semilla fija) de
INTENSIDAD-REMESAS coinciden exacto; `TABLA-JSON`/`CONTRASTES-JSON` de
REMESAS-CONTEXTO coinciden exacto. No se seala un CALC-2022 nuevo (sería
un duplicado byte-idéntico del ya sellado, D-14: no hay defecto que atrape
que el test de regresión no atrape ya) — el CALC-2022 sellado sigue siendo
la única fuente de esa ola.

**Alcance declarado del oro (D-22, honesto sobre lo que NO cubre):** el
`test_enigh_serie_oro.py` es reproducción contra dato real, no cobertura
sintética por rama terminal (`_valida_outputs` sobre soporte/parcial/celda
rara/masa cero). No se escribió esa batería sintética separada — la lógica
de cálculo es la MISMA que 2022 ya corrió y selló (el único código nuevo es
la resolución de columnas de diseño, ya verificada por el join de `§2`), así
que el costo de una batería sintética completa no compra una probabilidad
de defecto distinta de cero que el oro + el propio `corrida0 run` (que exige
`_valida_outputs` VERDE sobre CADA ola real, no solo sobre sintético) no
cubran ya. Si una ola real produce una rama terminal que 2022 nunca
ejercitó (p. ej. una celda `CERO-MUESTRAL`), `corrida0 run` de esa ola lo
reporta con la salida cruda del medidor, no con un mock.

## 4. Controles de consistencia con series externas ya selladas

`INTENSIDAD-REMESAS` y `REMESAS-CONTEXTO` de cada ola nueva comparan su
`prevalencia`/`RESULT-B-ENIGH-<ola>-P` observada contra el valor YA SELLADO
de esa misma ola en `CALC-B-0001` (serie `remesas>0` de 5 olas, ajena a este
acto, sellada antes). Es un control de consistencia interna entre dos
medidores independientes sobre la MISMA columna `remesas` del MISMO archivo
— no un oro contra 2022 (ver `§3`). Valores padre usados:
`2016=0.04745859252351374` (n=70311), `2018=0.04728548395278385` (n=74647),
`2020=0.04377543852935772` (n=89006) — citados de
`data/corrida0/CALC-B-0001/resultados.json`.

## 5. Qué NO hace esta pieza

No abre, lista ni deriva nada de `enigh2024*` (PARO (a) del encargo). No
adopta ningún resultado ni mueve `cuenta_gen2` de ninguno de los 9 CALC —
quedan `PENDIENTE-DE-MESA`, igual que sus antecesores 2022. No recalibra ni
cambia el procedimiento sellado de 2022. No incluye 2012/2014 (`§1`).
