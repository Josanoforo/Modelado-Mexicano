# Validación independiente del lote de 44 celdas primarias · `GEN2-VALIDACION-INDEPENDIENTE-LOTE-v1_0`

Valida `#986` (`CALC-DIN-LOTE-ENIF2024-EMISIONES-0001` → `…-ADJUDICACION-0001`), la cifra
más grande que hoy sostiene el producto: 44 celdas primarias (5 pares: `edadxsexo`,
`escolaridadxsexo`, `localidadxsexo`, `edadxescolaridad`, `escolaridadxlocalidad`),
`ΔMAE = MAE(C2) − MAE(R2) = 0.48 pp`, `IC95 = [0.10, 0.72]` → `PROPUESTA-CON-RESERVA`.

## Veredicto

**COINCIDE.** Las 44 celdas primarias (`R`, punto empírico 2024) coinciden con el
sellado a **precisión de punto flotante** (`diff_R_pp_max = 0.0`); `C2` (composición sobre
los marginales sellados de `#971`) coincide igual (`max |Δ error C2| = 1.1e-14`); el
`ΔMAE` primario coincide a `7.8e-16 pp` (`0.479758721910…` propio vs `0.479758721910…`
sellado — la misma cifra hasta el ruido de coma flotante de Python). El único eje que no
coincide a esa tolerancia es el ancho del IC95/la cobertura — **esperado y declarado**: es
método de varianza propio (LATITUD §6 del encargo), no el mismo bootstrap del medidor
sellado. Detalle celda a celda: `comparacion-lote.json` (script: `compara_lote.py`).

| cifra | propia | sellada (`#986`) | diferencia |
|---|---|---|---|
| `MAE(C2)` pp | 1.872872 | 1.872872 | 0.0000000000000018 pp |
| `MAE(R2)` pp | 1.393113 | 1.393113 | ídem, ruido de punto flotante |
| `ΔMAE` punto pp | 0.479759 | 0.479759 | 7.8e-16 pp |
| `ΔMAE` IC95 pp | [0.0968, 0.7142] | [0.0975, 0.7151] | ancho ≈ igual (0.618 vs 0.618 pp); método propio |
| cobertura `C2` | 76.7 % (33/43) | 75.0 % (33/44*) | método propio de IC |
| cobertura `R2` | 90.7 % (39/43) | 88.6 % (39/44*) | método propio de IC |
| celdas puntuadas | 43/44 | 43/44 | idéntico — la misma celda sin soporte (`edadxescolaridad:18-29×hasta-primaria`, n=193<200) |
| veredicto primario | `PROPUESTA-CON-RESERVA` | `PROPUESTA-CON-RESERVA` | idéntico |

\* El sellado divide por 44 (`…-COBERTURA-R-EN-IC-CAND-N = 44`, la celda sin soporte cuenta
como «fuera» automáticamente); lo propio divide por 43 (sólo las puntuadas). El
**numerador es idéntico** en los dos: `33` celdas dentro del IC de `C2` (`0.75×44 = 33` =
`0.767442×43 = 33`) y `39` dentro del IC de `R2` (`0.886364×44 = 39` =
`0.906977×43 = 39`) — las MISMAS celdas, clasificadas igual; sólo cambia la convención de
denominador (44 vs 43). No es un hallazgo de fondo: se declara para que no se lea como
discrepancia.

## Independencia — cómo se probó

`valida_lote.py` se escribió y corrió, y `resultados_propios_lote.json` se **commiteó y empujó**
(`97d92016`) **antes** de abrir ningún archivo de `CALC-DIN-LOTE-ENIF2024-EMISIONES-0001` o
`…-ADJUDICACION-0001`, y en ningún momento de este acto se abrieron `medidor.py`,
`adjudicacion.py`, `tools/lote_enif2024/` ni `tools/duelo/cruces_familia.py` (INDEPENDENCIA
del encargo). El único input de un CALC sellado usado en `P1` fue el marginal POR EJE de
`CALC-ARBITRO-MARGINALES-ENIF2024-0001` (`#971`), citado por `id` de `RESULT` — exactamente
lo que la spec humana exige (§4: «no se re-miden»). Todo lo demás —el catálogo de
escolaridad, el mapa etiqueta→tramo, el universo `PILOTO-1`, la fórmula de `C2`/`R2`, el
método de remuestreo— se escribió leyendo sólo `DIN-lote-enif2024-spec-v1_0.md`,
`data/ahorro-comparabilidad-texto-v1_0.tsv` y los catálogos crudos de
`enif2021_csv.zip`/`enif2024_csv.zip`.

## Método de varianza propio (declarado, LATITUD §6 del encargo)

Bootstrap de conglomerados estratificado sobre el marco de diseño ENTERO de cada archivo
(todas las UPM presentes, `n_h` UPM con reemplazo dentro de cada `EST_DIS`), 10 000
réplicas por ola, `numpy.random.default_rng` con semilla propia por ola (2021 = 20260922,
2024 = 20260923 — muestras independientes, sin covarianza inventada); `Δ_k` se recalcula
réplica a réplica con `R_k`, `C2_k` (réplicas de marginales 2024 propias) y `R2_k` (que usa
`δ21_k` de las réplicas 2021 propias) de la misma `k`. IC95 = percentiles 2.5/97.5. Mismo
método que `#970` (`valida_pilotos.py`), por continuidad de convención entre actos de
validación.

## P3 · causas — no hay ninguna diferencia que supere la tolerancia del punto

Con las 44 celdas `R` y `C2` coincidiendo a precisión de punto flotante, no hay diferencia
de fondo que explicar. Lo único distinto es el ancho del IC95/la cobertura, y su causa está
declarada de antemano: es un método de varianza propio, no una discrepancia de datos,
universo o fórmula — LATITUD del encargo lo autoriza explícitamente («método de varianza
(declarado)»). La spec humana (`DIN-lote-enif2024-spec-v1_0.md`) **bastó** para reproducir
el punto exacto sin leer una sola línea de código: universo `PILOTO-1`, la fórmula cerrada
de `C2`/`R2` (§4), el mapa de escolaridad por etiqueta (§2) y los marginales sellados
citables por `id` (§4) dieron, en un código escrito desde cero, el mismo número hasta el
bit menos significativo del punto flotante.

## P4 · lo que cambia para el producto — con los números propios

**Se sostienen, sin matiz.** `0.48 pp` (propio: `0.4798 pp`, la misma cifra a `1e-15`),
`[0.10, 0.72]` (propio: `[0.10, 0.71]`, mismo ancho) y `75 %`/`88.6 %` (propio: mismas 33 y
39 celdas dentro del IC — ver nota de denominador arriba) son, celda por celda y en el
agregado, la misma cifra que el lote ya reportó — la validación independiente no encontró
ninguna grieta entre la spec y el código que la implementó. La spec bastó en todos los
puntos: no hay hallazgo principal que reportar sobre la spec misma (a diferencia de lo que
P4 pedía anticipar si la spec no alcanzaba).

## Auditoría — el universo real, leído del cuestionario y del catálogo crudo

`n_universo_2024 = 13492` (propio) — coincide exactamente con el `13 492` que la spec
declara en su [HALLAZGO] de §1. `n_universo_2021 = 13518` (propio, no citado antes en el
árbol). `filas_codigo_fuera_de_dominio = 0` en las dos olas (ningún código de
`P5_1_*`/`P5_6_*`/`P5_7_*` fuera de `{"1","2",""}`). Catálogo de escolaridad verificado
contra el zip crudo en las dos olas: 2021 (`catalogos/p3_1_1.csv`, 11 etiquetas, códigos SIN
cero a la izquierda — normalizados aquí) y 2024 (`catalogos/niv.csv`, 13 etiquetas, códigos
CON cero a la izquierda) — la permutación 04/05 y el desdoblamiento de 09 en 09/10/11 que
la spec anuncia en §2 son exactamente lo que los dos catálogos crudos muestran, letra por
letra.

## `cuenta_formal`/`formalidad` — fuera de este acto, por diseño de la spec (no PARO)

Los 24 pares secundarios con `formalidad` y los 28 con `cuenta_formal` no se validaron:
la spec humana (§3, `[CIERRA]`) ya los deja `NO-EMITIBLE`/`NO-ADJUDICABLE-SIN-PISO` sin
piso, sólo `P2`; el encargo (P1) pide expresamente «los 5 pares primarios», no los 14. Se
declara para que no se lea como omisión.

## Reproducir esta validación

```
cd forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-LOTE-v1_0
python3 valida_lote.py    # P1 — escribe resultados_propios_lote.json
python3 compara_lote.py        # P2 — abre el sellado, escribe comparacion-lote.json
```
