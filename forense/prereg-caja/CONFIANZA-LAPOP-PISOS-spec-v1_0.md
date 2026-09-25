# Pisos por segmento LAPOP México 2004/2006/2019 (confianza interpersonal e institucional, participación, religión, autoridad, tolerancia) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1`, 25/sep/2026,
CAJA, rama `acto/gen2-confianza-religiosidad-capital-social-pisos-1`, 0-bis `ac7b169e`. Encargo:
`forense/encargos/2026-09-25-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1.md` (P2). CALC:
`CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de LAPOP 2004/2006/2019 para estos
reactivos (sólo metadatos: `pyreadstat` con `metadataonly=True`, y texto de cuestionarios).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` El encargo cuenta `lapop_` = 1 por prefijo (sólo el cuestionario 2023); los
  microdatos viven bajo otros ids (`642348348mexico_2004_export_version`,
  `518939279mexico_lapop_final_2006_data_set_092906`, `mexico_lapop_americasbarometer_2019_v1_0_w`,
  `mex_2021_…`, `mex_2023_…`), sha256 COINCIDE (espejo). Ya había 8 CALC LAPOP sellados
  (`ls data/corrida0 | grep -ic 'LAPOP\|LATINOBAR\|WVS\|PEW'` = 8, todos LAPOP): marginales
  nacionales de `b18`, `b21`, `eff1/2`, `pol1`, `d1–d4`, `clien1n` — se citan, no se repiten.
- **E.6:** 2023 es la ola más reciente → RESERVADA para los reactivos de este CALC. 2021 fuera
  (lista cerrada §1).
- **FIRMAS-15 T:** LAPOP sin serie hasta dictamen de equivalencia → pisos por ola, sin τ²; el
  dictamen textual por ola va en la lista cerrada §6 como PROPUESTO-POR-EJECUTOR.

## 1 · Unidad, universo, diseño

Unidad: **persona 18+** entrevistada. Diseño por ola: el de `LAPOP-PISOS-OLAS-spec-v1_0.md`
(2004 peso 1, `mestrat`, UPM `mprov`×`msec`; 2006 peso 1, `ESTRATOPRI`, `UPM`; 2019 `wt`,
`estratopri`, `upm`). Válido: peso > 0, estrato y UPM no vacíos. Universo: `q2` ≥ 18.

## 2 · Conductas (por texto)

Lista cerrada §3 (LAPOP): 20 conductas distintas; 18 en 2004 y en 2006 (12 comunes + 6 sólo
2004/2006), 14 en 2019 (12 comunes + 2 sólo 2019).

## 3 · Ejes (uno a la vez)

TOTAL · SEXO · EDAD · ESCOLARIDAD (años `ed`) · UR.

## 4 · Estimación

Razón ponderada (proporción o media) con bootstrap de UPM dentro de estrato (UPM única del
estrato = de certeza; sin UPM declarada, cada entrevista es su propia UPM; sin estrato, estrato
único), `PCG64(20260928)`, 2 000 réplicas, bloques de 50, percentiles 2.5/97.5, contrato
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
