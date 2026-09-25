# Cobertura por clase AMAI v1.1 · calibración ENIGH 2024 y eje NSE del marcador · GEN2-CLASE-AMAI-2 · RETROSPECTIVA

Generado por `python3 -m tools.dominios.amai.calibracion` desde los `resultados.json` sellados; sucede a `cobertura-por-clase-v1_0.md` (que no se toca). Tablas: `calibracion-2024-v1_0.tsv`, `cobertura-u1-por-clase-v1_1.tsv`, `resumen-p4-v1_1.json`.

## 1 · Distribución NSE nacional por hogares, ENIGH 2024 (apertura acotada C7)

`CALC-AMAI-NSE-ENIGH-2024-0001`: BAJO 44.3 % · MEDIO 34.2 % · ALTO 21.5 %; contra la Figura 1 de AMAI (ENIGH 2022, la única publicada): desvío máximo por grupo 4.74 pp → **APROXIMACION-CONFORME** (umbral 5.0 pp, congelado en COMMIT-1). Masa de BAJO a MEDIO y ALTO en dos años: deriva de bienes y de red (internet), no error del medidor.

## 2 · Calibración de cada instrumento contra ENIGH 2024 (descriptiva)

| CALC | Eje (firma A4) | Validación Figura 1 | Desvío máx. grupo vs Figura 1 (pp) | vs ENIGH 2024 (pp) |
|---|---|---|---:|---:|
| `CALC-AMAI-NSE-ENIGH-2022-0001` | EJE | CALCULABLE-REPRODUCE-AMAI | 0.07 | 4.81 |
| `CALC-AMAI-NSE-ENIF-2021-0001` | FUERA-SIN-CONDUCTA-ADOPTABLE | APROXIMACION-CONFORME | 0.35 | 4.85 |
| `CALC-AMAI-NSE-ENIF-2024-0001` | EJE | APROXIMACION-CONFORME | 3.01 | 1.72 |
| `CALC-AMAI-NSE-ENDUTIH-2023-0001` | EJE-APROXIMACION | APROXIMACION-CONFORME | 4.72 | 1.78 |
| `CALC-AMAI-NSE-ENDUTIH-2024-0001` | FUERA-DESVIADA | APROXIMACION-DESVIADA | 6.97 | 3.47 |
| `CALC-AMAI-NSE-ENDUTIH-2025-0001` | FUERA-DESVIADA | APROXIMACION-DESVIADA | 9.72 | 4.98 |

## 3 · Eje NSE en el marcador (P3)

`tools/marcador_segmento.py::filas_eje_nse` deriva **84** filas de tipo `EJE-NSE` (instrumento · conducta · grupo), R e IC por id de los CALC sellados: ENDUTIH 2023 30 · ENIF 2024 51 · ENIGH 2022 3. Por estado: `MEDIDA-POR-NSE` 52 · `MEDIDA-POR-NSE-APROXIMACION` 24 · `MEDIDA-POR-NSE-APROXIMACION-CIRCULAR` 6 · `SUPRIMIDA-N` 2. ENDUTIH 2024–25 y ENIF 2021 no entran (A4). `internet` y `celular` de ENDUTIH llevan `-CIRCULAR` (el NSE contiene internet fijo). No son marginales t-1: no hay ola anterior con NSE; ningún contador de piso ni `celdas_validadas` se mueve.

## 4 · Cobertura del catálogo U1 por clase

Identidades U1 de conducta: 55; con piso por NSE: 17; **en el eje NSE del marcador: 17**. Celdas conducta × grupo publicables: 49 de 165. Sin cambio respecto de v1.0 en lo que no tiene corte AMAI (ENVIPE, ENCIG: NO-CONSTRUIBLE).

## Auditoría de rigor extremo

El eje compara grupos de bienes y escolaridad del hogar, no clases sociológicas; cada fila es asociación descriptiva de la misma ola (A-bis), RETROSPECTIVA, unidad de su conducta (hogar en ENIGH, persona en ENIF y ENDUTIH) y nunca se promedia entre unidades. La calibración contra 2024 mezcla deriva real con el error de aproximación de cada instrumento; no se separan aquí.
