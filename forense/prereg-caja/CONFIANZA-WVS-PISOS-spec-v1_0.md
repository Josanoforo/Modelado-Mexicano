# Pisos por segmento WVS ola 7 México 2018 (confianza, capital social, religiosidad, autoridad, tolerancia) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1`, 25/sep/2026,
CAJA, rama `acto/gen2-confianza-religiosidad-capital-social-pisos-1`, 0-bis `ac7b169e`. Encargo:
`forense/encargos/2026-09-25-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1.md` (P2). CALC:
`CALC-WVS-PISOS-2018-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de WVS 2018 para estos
reactivos (sólo metadatos: `pyreadstat` con `metadataonly=True`, y texto de cuestionarios).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` WVS ola 7 México 2018 en el manifiesto desde el 12/ago/2026 bajo ids `f000…`
  (el encargo la suponía «bajo otros ids o pendiente»): microdato Stata
  `f00013084_wvs_wave_7_mexico_stata_v5_1`, sha256 `a676a760…` COINCIDE (copia en el espejo
  `mm-corpus/descargas_mx_espejo`). Una sola ola en corpus → E.6: se abre y se declara; sin IC de
  persistencia.
- `[EJECUTADO]` Estructura: `forense/analisis/confianza-capital-social/estructura-wvs.md`
  (1 741 × 403, metadatos) + auditoría propia de cada código usado.

## 1 · Unidad, universo, diseño

Unidad: **persona 18+** entrevistada. Peso `W_WEIGHT` (post-estratificación por sexo, edad y
escolaridad, según la ficha de diseño). UPM `I_PSU` (punto de levantamiento). **El archivo
público no trae estrato:** bootstrap de UPM con estrato único (más conservador que el diseño
estratificado real). Válido: peso > 0 y UPM no vacía. Universo: `Q262` ≥ 18.

## 2 · Conductas (por texto)

Tabla en `forense/analisis/confianza-capital-social/lista-cerrada-P1.md` §3 (WVS), parte de esta
spec: 32 conductas (30 proporciones, 2 medias 1–10).

## 3 · Ejes (uno a la vez)

TOTAL · SEXO · EDAD 18–29/30–44/45–59/60+ · ESCOLARIDAD (ISCED 2011, lista cerrada §3) ·
TAMLOC (`G_TOWNSIZE2`, 5 tramos) · INGRESO-SUBJETIVO (`Q288R`).

## 4 · Estimación

Razón ponderada (proporción o media) con bootstrap de UPM dentro de estrato (UPM única del
estrato = de certeza; sin UPM declarada, cada entrevista es su propia UPM; sin estrato, estrato
único), `PCG64(20260925)`, 2 000 réplicas, bloques de 50, percentiles 2.5/97.5, contrato
conservador (una réplica degenerada → sin EE ni IC). Receta común por sha256:
`tools/dominios/salud/pisos_diseno.py` (GEN2-SALUD-Y-BIENESTAR-PISOS-1) +
`tools/dominios/confianza/motor_pisos.py` (este acto). Un eje a la vez; nunca cruces.

## 5 · Controles, secuencia

Sintético en `tests/test_confianza_pisos_gen2.py` (todas las ramas terminales por
`corrida0._valida_outputs`; guardia de ola reservada con prueba de mutación). Ninguna ejecución
diagnóstica sobre el dato: la primera corrida es `corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala:** cada cifra en la escala de su instrumento; una proporción de «mucha o algo» de
confianza (1–4) no se compara con una de «6 ó 7» (1–7) ni con una media 0–10 de ENBIARE: sin
función de enlace no hay comparación entre instrumentos, sólo dirección descriptiva y rotulada.
**Estructura ≠ cultura:** baja confianza en policía, tribunales o partidos es evaluación de
instituciones con desempeño medible (victimización, impunidad), adaptación racional posible; un
gradiente por escolaridad o tamaño de localidad es primero ingreso, servicios y exposición, no
«carácter». La religiosidad declarada no es moral ni conducta. **Evidencia:** (a) datos primarios
en México (estas encuestas de hogares/personas) — nada aquí es (b) diáspora ni (c) marco
importado; WVS y Hofstede como MARCO se citan con crítica, nunca como hecho (Hofstede no se mide:
es un índice de empleados de IBM). **Firewall genético:** ninguna segmentación por ascendencia,
color de piel o etnia. **Foco rural/indígena/popular:** el eje de localidad lo aproxima; no hay
muestra indígena propia. **Temporalidad:** todo es RETROSPECTIVO; ninguna cifra es PROSPECTIVA.
**Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
