# Spec · DINERO-SERIES-IMOR v1.0 · ACTO GEN2-DINERO-SERIES-CNBV-BANXICO-1

Encargo: `forense/encargos/2026-09-25-GEN2-DINERO-SERIES-CNBV-BANXICO-1.md`
(0-bis `8dbe1f9`). Gobierna dos CALC:
`CALC-BANXICO-SERIES-IMOR-0001` y `CALC-CNBV-SERIES-IMOR-R16-0001`.

«El primer resultado que produzca este procedimiento es el que se reporta.»
Esta spec se congela (COMMIT-1) antes de ejecutar ningún medidor sobre los
insumos; ninguna ejecución diagnóstica se declara.

## 1 · Qué es y qué no es

- **SERIE-ADMINISTRATIVA.** Unidad de observación: **saldo de cartera** de
  crédito al consumo de la banca, agregado a nivel sistema. No es encuesta,
  no es persona, no es hogar, no es probabilidad individual de impago.
- Ningún RESULT de estos CALC se promedia, suma ni compara sin función de
  enlace con un piso de persona (ENIF, ENSAFI, Banxico-satisfacción): §4
  v2.16. Comparable sin enlace: nivel contra nivel **de la misma serie**, y
  signo/orden entre productos de la misma serie y el mismo mes.
- IMOR ≠ IMORA. Ninguna de las dos series publica IMOR ajustado por
  castigos (IMORA); una afirmación sobre IMORA no se contesta con IMOR: se
  dictamina aparte.
- No es prospectiva: ambas series son históricas y públicas; todo cotejo con
  las afirmaciones es **RETROSPECTIVA**.

## 2 · Insumos — constancias congeladas (E.6/D-22)

Ninguna serie viva se sella: se sella la descarga con fecha y sha, copiada a
`insumos/` del CALC.

| input_id | archivo en `insumos/` | sha256 | origen | fecha de descarga |
|---|---|---|---|---|
| `IN-BANXICO-IMOR-CONSUMO-MENSUAL` | `banxico-imor-consumo-mensual.csv` | `772f9d0b9da57b18ef9abdd5824b0824b6191e65668103e3a8329171d3df88e9` | extracción de `gen2_banxico_imor_consumo_producto_mensual_2026t1_html` (manifiesto; HTML sha `c9691762…c4b2`), Banxico, Informe Trimestral ene–mar 2026, <https://www.banxico.org.mx/TablasWeb/informes-trimestrales/enero-marzo-2026/B133C3DC-462F-40C1-B2BA-04086A1CFAB1.html>; copia byte a byte de `data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv` | 2026-09-11 |
| `IN-CNBV-R16-IMOR-CONSUMO-202112` | `cnbv-imor-consumo.csv` | `e61c97a3acd6634e2c0cabdad18a9fbde06ff58f1c2363a3e290c3cc40e23400` | extracción de `gen2_cnbv_040_1a_r16_imor_tipo_cartera` (manifiesto; XLS sha `3b6ac444…1629`), CNBV Portafolio de Información, reporte 040-1A-R16, <https://portafolioinfdoctos.cnbv.gob.mx/Documentacion/minfo/XLS/40/040_1a_R16.xls>; copia byte a byte de `data/fuentes-financieras-20/cnbv-imor-consumo.csv` | 2026-09-11 |

Definición oficial citada (la «verificación de texto» de una serie):
- Banxico: IMOR = saldo de cartera vencida (2016-01..2021-12) o clasificada
  en etapa 3 (2022-01 en adelante, IFRS9) / saldo de cartera total del mismo
  producto, en porcentaje; universo «banca comercial; incluye Sofomes ER
  subsidiarias de instituciones bancarias y grupos financieros; excluye CI
  Banco»; productos: Consumo total, Tarjetas de crédito, ABCD (incluye
  bienes muebles y automotriz), Nómina, Personales; mensual.
- CNBV R16: IMOR = cartera vencida / cartera total del segmento, en
  porcentaje; Total Banca Múltiple; foto 2021-12 (el XLS cacheado no es serie
  histórica); 9 tipos de cartera, «Ops de Arrendamiento Capitalizable» vacío
  en el original.

La ruptura de definición 2021-12 → 2022-01 (IFRS9) ya la documentó
`CALC-IMOR-CONTEXTO-0001` (se cita, no se repite). Ningún cambio de esta
spec cruza esa ruptura: el único cambio (interanual 2026-03 vs 2025-03) cae
entero en IFRS9.

## 3 · Procedimiento — CALC-BANXICO-SERIES-IMOR-0001

1. Verificar sha256 del insumo; 615 filas; `indicador = IMOR`, `unidad =
   porcentaje`; sin duplicados (producto, fecha); valores en [0, 100].
2. Para cada producto `CON` Consumo total · `TDC` Tarjetas de crédito ·
   `ABCD` · `NOM` Nómina · `PER` Personales:
   - **nivel** en cada periodo fijado: 2026-03 (último dato), 2025-09,
     2024-12, 2024-03, 2024-02, 2023-12 — cada uno es el mes que cita alguna
     afirmación (§5) o el último publicado;
   - **media 2025**: media aritmética simple de los 12 meses 2025-01..12
     (cada mes pesa igual; no es ratio de saldos, que no se publican);
   - **cambio interanual 2026-03**: nivel 2026-03 − nivel 2025-03, en puntos
     porcentuales.
3. Redondeo: medias y diferencias a 12 decimales; niveles tal cual (dos
   decimales en origen).

## 4 · Procedimiento — CALC-CNBV-SERIES-IMOR-R16-0001

1. Verificar sha256; toda fila con `fecha = 2021-12` y `unidad = porcentaje`;
   exactamente un vacío, «Ops de Arrendamiento Capitalizable» (se declara, no
   se imputa; no emite RESULT); valores en [0, 100].
2. Nivel 2021-12 de: `CON` Cartera total de consumo · `TDC` Tarjeta de
   Crédito · `PER` Personales · `NOM` Nómina · `ABCD` · `AUT` Automotriz ·
   `BM` Adq. de Bienes Muebles · `OTR` Otros Créditos de Consumo.

## 5 · Uso previsto (se fija antes de correr)

Cotejo RETROSPECTIVO contra las afirmaciones que citan IMOR **de sistema**
por producto: ASTRA5-U0-CRPOP-002, -006, -012 (parte sistema), -044 (parte
sistema), -055 (parte IMOR simple), -007/-018 (comparador de sistema, no la
cifra de institución), ASTRA5-U0-CRFAC-003 (solo como IMOR; la afirmación
es IMORA). Dictamen con vocabulario cerrado: **CONFIRMA** (la cifra de la
afirmación cae a ≤ 0.5 pp del RESULT del mismo mes y producto) · **MATIZA**
(orden o signo se sostiene pero la cifra, el universo o la definición
difieren) · **ROMPE** (orden o signo contrario) · **NO-CONTESTA** (la serie
no tiene el concepto). Si una afirmación satisface CONFIRMA y MATIZA a la
vez (cifra cercana pero universo distinto), **manda MATIZA**.

## 6 · Nulos y no finitos (D-22.3)

Ningún RESULT puede ser nulo: el medidor aborta ante faltante, duplicado o
valor fuera de rango; el único vacío conocido (CNBV arrendamiento) no emite
id. None y NaN: ninguno.

## 7 · Etiquetas

`cuenta_gen2: SI` · `adopta: NO` · `tipo: SERIE-ADMINISTRATIVA` ·
`evaluacion: RETROSPECTIVA` · validación independiente pendiente.
