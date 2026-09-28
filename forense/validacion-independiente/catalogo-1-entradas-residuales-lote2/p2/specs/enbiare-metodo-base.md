# ENBIARE · base humana recibida, conservada para lectura conjunta

Estado: RESTAURACION-DE-ENTREGA. Complementar con ventanas y contrato de edades separado. IC pendiente de contrato P3.

# Método: extracción fiel de especificación humana

## 1 · Unidad, universo, diseño

Unidad: **persona elegida de 18+** (TENBIARE), ponderador `FAC_ELE`, estrato `EST_DIS`, UPM
`UPM_DIS` (llaves opacas). SEXO, EDAD, NIVEL de TSDEM por llave `FOLIO`+`VIV_SEL`+`HOGAR`+
`N_REN` (sólo llaves únicas en TSDEM; no pareados en `G-JOIN-SIN-SOCIODEMOGRAFICO`). Válido:
`FAC_ELE > 0`, estrato y UPM no vacíos. Universo: EDAD ≥ 18.

## 2 · Conductas (por texto)

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

 Escalas 0–10 (PA1, PA5, PB1_01, PB1_02, PB1_04, PB1_11) se publican como **media**
(fuera de 0–10 → fuera). CESD-7 (PD2_1–7, 0–3, PD2_6 invertido): ≥ 9 (18–59) / ≥ 5 (60+),
mismos cortes que ENSANUT. GAD-2 (PD3_1–2, 0–3): suma ≥ 3. PB2_x: 1 → 1; 2 y 3 («no tiene
familia») → 0. ASISTE-SERVICIO-RELIGIOSO: PG7 1/2, y PG6 = 2 → 0 (blanco por secuencia).

|---|---|---|
| SATISFACCION-VIDA | PA1 «qué tan satisfecho(a) se encuentra actualmente con su vida» 0–10 | media |
| ESCALERA-CANTRIL | PA5 «¿En qué escalón siente que su vida se ubica actualmente?» 0–10 | media |
| DEPRESION-CESD7 | PD2_1–PD2_7 (0–3), PD2_6 invertido | ≥ 9 (18–59) / ≥ 5 (60+) → 1 |
| ANSIEDAD-GAD2 | PD3_1, PD3_2 (0–3) | suma ≥ 3 → 1 |
| CONFIANZA-MAYORIA-GENTE | PB1_01 «¿cuánto confía en la mayoría de la gente?» 0–10 | media |
| CONFIANZA-GENTE-CONOCIDA | PB1_02 | media |
| CONFIANZA-POLICIA-MUNICIPAL | PB1_04 | media |
| CONFIANZA-PARTIDOS | PB1_11 | media |
| CUENTA-APOYO-FAMILIA | PB2_1 «¿…siempre contará con la ayuda de personas de su familia?» | 1 → 1; 2, 3 («no tiene familia») → 0 |
| CUENTA-APOYO-AMISTADES | PB2_2 | ídem |
| TIENE-RELIGION | PG6 «¿Usted tiene una religión?» | 1 / 2 |
| ASISTE-SERVICIO-RELIGIOSO | PG7 «¿Acostumbra asistir a su iglesia, templo o servicio religioso?» | 1 → 1; 2 → 0; PG6 = 2 (blanco por secuencia) → 0 |

Cortes CESD-7 (≥ 9 en adultos, ≥ 5 en 60+): los de la validación del CESD-7 que usa el
INSP para ENSANUT (Salinas-Rodríguez et al., Salud Pública Mex 2013/2014), fijados aquí,
antes del dato, e idénticos en ENSANUT y ENBIARE. GAD-2 ≥ 3: corte de Kroenke et al.
