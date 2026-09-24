# Pisos por segmento ENBIARE 2021 (bienestar subjetivo, salud mental, confianza, apoyo, religiosidad) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1`, 24/sep/2026, CAJA, rama
`acto/gen2-salud-y-bienestar-pisos-1`, 0-bis `6d56f7ff`. Encargo:
`forense/encargos/2026-09-24-GEN2-SALUD-Y-BIENESTAR-PISOS-1.md` (P3). CALC:
`CALC-ENBIARE-PISOS-BIENESTAR-0001`. Congelada en el COMMIT-1, **antes** de leer un solo
valor de la base ENBIARE (de los CSV sólo se leyó la primera línea). **El primer resultado
que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` ENBIARE en el manifiesto: una ola, 2021 (`enbiare2021_bd_csv_zip`,
  `enbiare2021_fd_pdf`), sha256 COINCIDE. E.6 del encargo: con una sola ola en corpus no hay
  historia que reservar → se abre y se declara. Sin IC de persistencia.
- `[EJECUTADO]` Estructura: FD completo (`pdftotext`, 2 326 líneas) y encabezados de las 4
  tablas: `forense/analisis/salud-bienestar/estructura-enbiare.md`. El `.zip` no trae
  diccionario aparte; el FD es la autoridad de códigos.
- «Facilidad para cubrir gastos» (afirmación CLASE-040): NO-CONSTRUIBLE — el FD completo no
  tiene el ítem (búsqueda `gasto|ingreso|alcanza|dificultad|facilidad|económic|cubrir`,
  apartados A–J recorridos); PF2 es un monto de ingreso suficiente, no una escala de
  facilidad.

## 1 · Unidad, universo, diseño

Unidad: **persona elegida de 18+** (TENBIARE), ponderador `FAC_ELE`, estrato `EST_DIS`, UPM
`UPM_DIS` (llaves opacas). SEXO, EDAD, NIVEL de TSDEM por llave `FOLIO`+`VIV_SEL`+`HOGAR`+
`N_REN` (sólo llaves únicas en TSDEM; no pareados en `G-JOIN-SIN-SOCIODEMOGRAFICO`). Válido:
`FAC_ELE > 0`, estrato y UPM no vacíos. Universo: EDAD ≥ 18.

## 2 · Conductas (por texto)

Tabla en `forense/analisis/salud-bienestar/lista-cerrada-P1.md` §2 (ENBIARE), parte de esta
spec. Escalas 0–10 (PA1, PA5, PB1_01, PB1_02, PB1_04, PB1_11) se publican como **media**
(fuera de 0–10 → fuera). CESD-7 (PD2_1–7, 0–3, PD2_6 invertido): ≥ 9 (18–59) / ≥ 5 (60+),
mismos cortes que ENSANUT. GAD-2 (PD3_1–2, 0–3): suma ≥ 3. PB2_x: 1 → 1; 2 y 3 («no tiene
familia») → 0. ASISTE-SERVICIO-RELIGIOSO: PG7 1/2, y PG6 = 2 → 0 (blanco por secuencia).

## 3 · Ejes (uno a la vez)

TOTAL · SEXO (1/2) · EDAD 18–29 / 30–44 / 45–59 / 60+ · ESCOLARIDAD (`NIVEL`):
HASTA-PRIMARIA {00 ninguno, 01 preescolar, 02 primaria}, SECUNDARIA {03, 04 técnica con
secundaria}, MEDIA-SUPERIOR {05 normal básica, 06 preparatoria, 07 técnica con
preparatoria}, SUPERIOR {08 licenciatura, 09 especialidad, 10 maestría o doctorado}; 99 y
blanco fuera · TLOC (1 ≥ 100 mil, 2 15 000–99 999, 3 2 500–14 999, 4 < 2 500).

## 4 · Estimación

Razón ponderada (proporción o media) con bootstrap de UPM dentro de `EST_DIS` (certeza para
UPM única, `PCG64(20260924)`, 2 000 réplicas, percentiles 2.5/97.5, contrato conservador),
receta común por sha256.

## 5 · Controles, secuencia

Sintético en `tests/test_salud_pisos_gen2.py`. Oro: no hay piso GEN2 previo de ENBIARE
(`ls data/corrida0 | grep -ci enbiare` = 0 al COMMIT-1). Ninguna ejecución diagnóstica.

## 6 · Auditoría (afirma sobre México)

**Escala:** medias 0–10 y proporciones de personas 18+; una media de satisfacción no se
compara con una proporción. **Precariedad ≠ cultura:** un gradiente de satisfacción por
escolaridad o tamaño de localidad es primero ingreso y servicios, no «carácter»; la nota no
lo lee como rasgo. **Marcos importados:** CESD-7 y GAD-2 son escalas de cribado, no
diagnóstico; la comparación internacional de «satisfacción alta» (EMOC-028) no se hace aquí.
**Confianza:** baja confianza en policía o partidos es evaluación de instituciones (adaptación
racional posible), no desconfianza «cultural». **Una ola:** ninguna tendencia. **Cifra escrita
a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
