# Pisos por segmento Latinobarómetro 2023, México (confianza, religión, autoridad, participación) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1`, 25/sep/2026,
CAJA, rama `acto/gen2-confianza-religiosidad-capital-social-pisos-1`, 0-bis `ac7b169e`. Encargo:
`forense/encargos/2026-09-25-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1.md` (P2). CALC:
`CALC-LATINOBAROMETRO-PISOS-2023-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de Latinobarómetro 2023 para estos
reactivos (sólo metadatos: `pyreadstat` con `metadataonly=True`, y texto de cuestionarios).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Olas en manifiesto: 2023 (`latinobarometro2023_bd_stata_zip`, sha256 `7689a62d…`)
  y 2024 (`latinobarometro2024_bd_stata`, `469a94c5…`). **2024 RESERVADA (E.6)**: no es input, no
  se abrió. Se abre 2023.
- `[SUPUESTO→FALSO]` del encargo §3 «Latinobarómetro trae pesos y diseño»: trae `wt`, **no** trae
  estrato ni UPM (274 columnas; ni el cuestionario del zip documenta el diseño) → rama prevista
  por el propio encargo: «descriptivo sin IC [de diseño], dicho». Se publica IC de bootstrap
  ponderado de entrevistas, rotulado `MAS-PONDERADO`, como **cota inferior** del IC de diseño.

- `[EJECUTADO]` `corrida0 spec-check`: FAIL en todas las variables con «filas del archivo en
  inventario: 0» — el inventario de reactivos (`data/inventario-reactivos-*`) **no indexa** `Latinobarometro_2023_Esp_Stata_v1_0.dta`.
  No es un negativo (A.13: el comando no examinó el archivo). La existencia de cada columna se
  verificó con `pyreadstat` `metadataonly=True` sobre el miembro exacto (lista cerrada, cabecera);
  si falta una, el lector levanta `KeyError` y la corrida no sella.

## 1 · Unidad, universo, diseño

Unidad: **persona 18+** entrevistada en México (`idenpa = 484`; el lector descarta los demás
países antes de devolver filas). Peso `wt`. Válido: `wt > 0`. Universo: `edad` ≥ 18.

## 2 · Conductas (por texto)

Lista cerrada §3 (Latinobarómetro): 21 conductas, todas proporciones.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO · EDAD · ESCOLARIDAD (`REEEDUC_1`, 3 grupos) · TAMLOC (`tamciud`, 3 grupos) ·
CLASE-SUBJETIVA (`S2`, 4 grupos).

## 4 · Estimación

Razón ponderada (proporción o media) con bootstrap de UPM dentro de estrato (UPM única del
estrato = de certeza; sin UPM declarada, cada entrevista es su propia UPM; sin estrato, estrato
único), `PCG64(20260926)`, 2 000 réplicas, bloques de 50, percentiles 2.5/97.5, contrato
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
