# Recibo · ASTRA-3 U1 · ENIF oferta

## EJECUTADO

Se congelaron spec humana, cuatro `spec.yaml`, código y conmensuración en
`5ab593e7`, antes de la primera lectura de valores ENIF de esta sesión.
Después se corrieron y sellaron los cuatro CALC
`CALC-DIN-OFERTA-EXCLUSION-ENIF{2012,2015,2018,2021}-0001`.
`python3 tools/corrida0.py verify <CALC>` devolvió `REPRODUCE` y contexto
`IDENTICO` en las cuatro olas, con tolerancia absoluta 1e-10. Los commits de
emisión son `27b70b7e` (2012), `f4364011` (2015), `5f937566` (2018) y
`ee9ae846` (2021). Unidad: persona 18–70; escala P [0,1], IC95 por diseño;
generación GEN2, origen numérico MICRODATO, `cuenta_gen2: SI`, `adopta: NO`.

## LEÍDO

Los cuestionarios y FD de las cuatro olas fijaron preguntas, pases y
opciones antes del dato. Se leyeron specs y RESULT sellados de los pisos de
crédito para enlazar por identidad; no se reestimaron. Hashes de fuentes,
payloads, specs, scripts y sellos están en `originales/fuentes.sha256`,
`nota.md`, `spec.yaml` y `ejecucion.json` de cada CALC.

## REPORTADO

Entre no usuarios de crédito formal, la proporción cuya razón queda sólo en
OFERTA fue 30.2% (IC95 28.5–32.0) en 2012, 33.3% (31.4–35.2) en 2015,
35.9% (34.6–37.3) en 2018 y 34.6% (33.1–36.1) en 2021. Son porcentajes de
personas no usuarias de 18–70, no efectos causales. Las dos primeras olas
incluyen respuestas múltiples; no se equiparan a razón principal.

`enlace-pisos.tsv` enumera los 1 242 RESULT `-P` de cinco CALC históricos
pertinentes: 413 enlaces contextuales por ola, población y eje, y 829
motivos de no enlace. Cuenta formal se reporta por separado en los cuatro
CALC, sin equipararla a ahorro activo. La lectura y todas las cifras
nacionales por producto, N sin ponderar, denominador ponderado e IC están
en `nota.md`.

## NO-CORRIDO / RESERVAS

ENIF 2024 y demás olas reservadas; fuera del alcance U1. Sin ejecución de
registro, marcador, tablero, CI, celdas-D, ni adopción.

## CONSUMIDO

PR de `codex/astra3-enif-oferta-1`: se agrega tras publicarlo. Se consumieron
los cinco CALC de piso identificados en `enlace-pisos.tsv`, sólo por lectura.
