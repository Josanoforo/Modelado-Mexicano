ENCARGO · MAESTRA33-C4 · REGLAS-OLA5-FASE2-A — invoca /acto
SHA de redacción: d353d82. ENTORNO: CAJA — NO NUBE, NO doble. COMPUERTA: ninguna de merge; corre DESPUÉS de C3 en la misma máquina (un acto de caja a la vez). MODELO SUGERIDO: Opus (medidor de dos commits).
FIRMA DE MESA: ejecuta la fase 2 de FP-190 acotada a lo que E7 dejó EXISTE-SATISFACE; lanzamiento de mesa = firma.
A.8 (dirección contra d353d82): forense/notas/2026-09-01-mapeo-fp190.md — SFT-04: EXISTE-SATISFACE (eder2017 historiavida.dta baniar/baniar_d); TIC-01 θ y EMP-05 θ: EXISTE-SATISFACE con candidata recomendada en su sección. CIV-08, TIC-06, DIN-07: EXISTE-NO-SATISFACE; DIN-11, SFT-06: NO-ENCONTRADO — fuera de este acto. milpa/tramite.yaml: 8 reglas, ninguna de SFT (grep sft → 0 de 8).
P1 · SFT-04, regla con p medida: COMMIT-1 congela — regla SI-ENTONCES redactada desde la definición verbatim de FP-190, variable y dicotomización tomadas de la recomendación de E7 (valores que cuentan y los que quedan fuera), universo, ponderador, ola, escala [0,1], frase de sello. Si la variable recomendada mide otra conducta que la de la celda (dificultad ≠ ayuda recibida), PARO-reporta EXISTE-NO-SATISFACE con qué falta — no fuerces. COMMIT-2: p + IC95 (seed 42) + n, entrada NUEVA en milpa/tramite-ola5-propuesta-v0.yaml, clase MEDIDO·p, PENDIENTE-DE-MESA.
P2 · θ TIC-01 y θ EMP-05: cita en procedencia.yaml desde la candidata de E7 — encuesta, ola, variable, valor, n — con escala declarada (A-bis 3). Si la θ se mide (no solo se cita), mismo régimen de dos commits que P1.
P3 · Tablero: FP-190 pasa a "fase 2-A ejecutada" con los 3 objetos y deja explícitos los 5 restantes con su vocabulario A.4 y lo que les falta.
PERÍMETRO: milpa/tramite-ola5-propuesta-v0.yaml, milpa/procedencia.yaml (θ), tools/ (script del medidor), forense/notas propia, tablero (FP-190 + recibo), archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: reglas con p medida en propuesta +1 · θ citadas +2, declarado.
LO QUE NO HACE: no carga nada al motor (sellar es de mesa); no toca las 5 celdas/θ no satisfechas; no abre corridas-R ni corridas-M.

## CONSUMIDO

`PR #424`, 1/sep/2026. A.8 del encargo (SFT-04 EXISTE-SATISFACE) contradicho por
la propia nota de mapeo citada: la candidata con texto real mide DIFICULTAD, no
AYUDA — PARO aplicado tal como el propio P1 lo previó; SFT-04 revierte a
EXISTE-NO-SATISFACE, cero reglas nuevas. TIC-01 θ y EMP-05 θ citadas (no
medidas, sin G# formal) en `milpa/procedencia.yaml:candidatas_theta_citadas_fp190`.
`FP-190` enmendada (fase 2-A ejecutada). `ADR-251` (candidato). Detalle:
`forense/notas/2026-08-31-reglas-ola5-fase2a-spec.md`.
