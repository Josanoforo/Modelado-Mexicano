# Pisos de actitudes hacia la ciencia por segmento, ENPECYT 2011–2015 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-LOTE-1`, 25/sep/2026, CAJA, rama `acto/gen2-cola-lote-1`,
0-bis `3a49c186`. Encargo: `forense/encargos/2026-09-25-GEN2-COLA-LOTE-1.md` (pieza P-ENPECYT). CALC:
`CALC-ENPECYT-CONOC-PISOS-0001`. Congelada en el COMMIT-1 de ENPECYT, **antes** de leer un solo
registro (sólo FD, cuestionarios y cabeceras DBF). **El primer resultado que produzca este
procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` «ENPECYT 2017, una ola → descriptivo» (encargo §1): **falso en corpus**. Están 2005,
  2007, 2009, 2011, 2013 y 2015 (`corpus-completo/inegi/enpecyt/`, ids
  `cc1_inegi_enpecyt_<año>__enpecyt<año>_bd_dbf`) además de 2017. **E.6: 2017, la más reciente,
  RESERVADA**; no es input (guardia). Las tres afirmaciones CONOC citan 2017: aquí reciben su piso
  histórico y su IC de persistencia; su cotejo con 2017 queda para la prueba que levante la reserva.
  INTERPRETACIÓN-DECLARADA.
- `[EJECUTADO]` Olas medidas: **2011, 2013, 2015** (misma familia de cuestionario S4P, tablas
  VIVHOG/CS/CB1/CB2, `FAC` en CB1). Fuera, declarado: 2009 (sin factor de expansión en su
  descriptor), 2005 y 2007 (otra estructura de tablas; 2005 sin el reactivo de interés).
- `[EJECUTADO]` Diseño: CS trae `EST_DIS` (1–4) y `UPM_DIS` en 2013 y 2015; **2011 no los trae**
  (descriptor 2011, tabla CS íntegra) → 2011 publica P ponderada y N, sin EE ni IC. Ciudad
  autorrepresentada `CD_A` (2013, 2015) / `CD` (2011). Estrato = ciudad|EST_DIS; UPM =
  ciudad|EST_DIS|UPM_DIS.
- `[EJECUTADO]` Reactivos por texto (cuestionarios 2011 `ENPECYT2011_Cuestionario.pdf` y 2013
  `enpecyt2013_cuest.pdf` dentro de sus ZIP; 2015 por FD; 2017 por cuestionario y FD, sin abrir datos):
  «El gobierno debería invertir más en investigación científica» (S4P26_1 2011/13; S4P25_1 2015),
  MUY DE ACUERDO 1 … MUY EN DESACUERDO 4, NO SABE 5; «Confiamos demasiado en la fe y muy poco en la
  ciencia» (S4P33_2_1 2011/13; S4P31_1_1 2015), misma escala; «En una escala del 1 al 10, donde 10
  equivale a "Muy respetable", ¿en México, cómo califica usted el desempeño de un…» bombero,
  enfermera, investigador (científico) (S4P14_13/_14/_4 en 2011/13; S4P14_12/_13/_16 en 2015),
  inventor sólo 2015 (S4P14_17); 11 = No sabe en 2013/15. Interés («es muy grande, grande, moderado
  o nulo», 1–4): **el texto cambia**: 2011 y 2013 «Nuevos inventos y tecnología»; 2015 y 2017
  «Nuevos inventos, descubrimientos científicos y desarrollo tecnológico». Se mide en las tres olas
  y su τ² absorbe el cambio de redacción (declarado, no corregido).

## 1 · Unidad, universo, ponderación

Persona elegida de 18+ (una fila de CB1), áreas urbanas de 100 000+ habitantes. Unión CB1–CB2–CS
por ciudad+PER+CON+V_SEL+N_HOG+N_REN, sólo llaves únicas (diagnósticos de no pareados y
duplicados). Ponderador `FAC` de CB1 > 0.

## 2 · Conductas (por texto)

INTERES-AL-MENOS-MODERADO (1–3 de 1–4) · INTERES-GRANDE-O-MAS (1–2 de 1–4) · GOB-INVERTIR-ACUERDO
(1–2 de 1–5, «no sabe» en el denominador) y -SIN-NS (1–2 de 1–4) · FE-CIENCIA-ACUERDO y -SIN-NS
(ídem) · RESPETA-10-{BOMBERO, ENFERMERA, INVESTIGADOR} (= 10 de 1–10) · RESPETA-10-INVENTOR (sólo
2015).

## 3 · Ejes (uno a la vez)

TOTAL · SEXO · EDAD (18–29, 30–44, 45–59, 60+) · ESCOLARIDAD (`NIV`: básica o menos 0–3 / media
4–6 / superior 7–10). Sin localidad: el universo es urbano ≥ 100 000.

## 4 · Estimación y persistencia

2013 y 2015: razón ponderada con bootstrap de UPM dentro de estrato (receta común, `PCG64(20260925)`,
1 000 réplicas, contrato conservador). 2011: P ponderada, sin IC. τ² por conducta × eje × categoría
sobre 2011→2013→2015; IC calibrado del piso 2015 con `ic_calibrado` de la receta:
expit(logit p ± z·√(ee_2015² + τ²)).

## 5 · Controles

Sintético en `tests/test_cola_lote_1_pisos.py`. Post-sello: la nota compara el piso 2015 con las
cifras 2017 que citan los reports (75.0 %, 92.2/92.3 %, 59.5/41.5/34.6/48.4 %, ~72 %) sólo como
dirección y orden — 2017 no se abre.

## 6 · Auditoría (afirma sobre México)

**Universo urbano ≥ 100 000**: nada de esto dice del México rural ni de menores de 18. **Actitud
declarada ≠ conducta**. **Redacción**: interés 2011–13 no es el mismo reactivo que 2015. **Cifra
escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
