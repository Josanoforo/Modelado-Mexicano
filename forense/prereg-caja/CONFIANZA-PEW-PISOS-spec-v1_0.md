# Pisos por segmento PEW Global Attitudes México 2013–2024 (religiosidad, autoridad, confianza) con IC calibrado de persistencia · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1`, 25/sep/2026,
CAJA, rama `acto/gen2-confianza-religiosidad-capital-social-pisos-1`, 0-bis `ac7b169e`. Encargo:
`forense/encargos/2026-09-25-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1.md` (P2). CALC:
`CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de PEW Global Attitudes 2013–2024 para estos
reactivos (sólo metadatos: `pyreadstat` con `metadataonly=True`, y texto de cuestionarios).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Manifiesto por prefijo `pew_`: 9 ids (el encargo dice 9): 7 microdatos
  `pew_gas_spring{2013,2015,2017,2018,2023,2024,2025}` + 2 PDF 2025 (topline y nota de
  confianza social, que **no se leen**: traen cifras de la ola reservada). sha256 de los 7 zip
  COINCIDE (espejo). **2025 RESERVADA (E.6).**
- `[EJECUTADO→FALSO]` PEW *Religion in Latin America* (2014): NO está en corpus
  (`tabla-final-v1_0.tsv`: «NO OBTENIDO… REGISTRO-REQUERIDO»). La religiosidad PEW se mide con
  la serie Global Attitudes; el estudio de 2014 va a NC con receta.
- `[EJECUTADO]` Estructura: `estructura-pew.md` + auditoría (encontró la edad 2013/2015 que el
  informe omitió).
- Concurrencia (§9): FAMILIA lee PEW en lectura para migración; este acto sólo toma religiosidad,
  autoridad y confianza. Ningún archivo compartido se escribe.

- `[EJECUTADO]` `corrida0 spec-check`: FAIL en todas las variables con «filas del archivo en
  inventario: 0» — el inventario de reactivos (`data/inventario-reactivos-*`) **no indexa** los seis `.sav` de PEW Global Attitudes.
  No es un negativo (A.13: el comando no examinó el archivo). La existencia de cada columna se
  verificó con `pyreadstat` `metadataonly=True` sobre el miembro exacto (lista cerrada, cabecera);
  si falta una, el lector levanta `KeyError` y la corrida no sella.

## 1 · Unidad, universo, diseño

Unidad: **persona 18+** entrevistada en México. Diseño por ola y regla de UPM con faltantes:
lista cerrada §3 (PEW). Universo: edad ≥ 18.

## 2 · Conductas (por texto)

Lista cerrada §3 (PEW): 7 conductas, 23 celdas conducta×ola.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO · EDAD · ESCOLARIDAD (sólo 2017+: 2013/2015 no traen escolaridad de México).

## 3-bis · Persistencia

τ² por (conducta, eje) sobre las olas con texto IDÉNTICO (lista cerrada §3 y §6); IC calibrado
`expit(logit p ± z·√(ee_m² + τ²))` sobre la última ola (2024). Método de
`CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` (#1009/#1041), el mismo que ENSANUT en #1124.

## 4 · Estimación

Razón ponderada (proporción o media) con bootstrap de UPM dentro de estrato (UPM única del
estrato = de certeza; sin UPM declarada, cada entrevista es su propia UPM; sin estrato, estrato
único), `PCG64(20260927)`, 2 000 réplicas, bloques de 50, percentiles 2.5/97.5, contrato
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
