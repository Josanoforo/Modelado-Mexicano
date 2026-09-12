# `CALC-SHED2025-BNPL-DANO-0001` — BNPL, daño y universos SHED 2025

**Acto:** `GEN2-SHED-BNPL-DANO-UNIVERSOS` (11/sep/2026).  
**Población:** personas adultas encuestadas en Estados Unidos por SHED 2025.  
**Unidad:** persona. **Corte:** transversal. **Ponderador:** `weight`.  
**Uso:** descripción y asociación; no causal, no transportable a México y sin adopción al motor.

## Fuente y versión congeladas

El cálculo usa `public2025.csv` del ZIP público SHED 2025, 12,934 filas y
815 columnas, SHA-256 `a4ab3f7d…`. La codificación y los textos se fijan con
el codebook del 4/sep/2026 (`3094d147…`) y el cuestionario oficial Appendix A
recuperado el 11/sep/2026 (`21965841…`). Los tres IDs completos viven en
`spec.yaml` y se resuelven por manifiesto.

El codebook indica que `weight`/`weight_pop` corresponden al corte de un año y
que `panel_weight`/`panel_weight_pop` son sólo para participantes de 2024 y
2025. Se usa `weight`: una razón de masas ponderadas. No se estima total
poblacional y no se usa ningún peso de panel.

## Codificación y faltantes

El CSV analizado usa etiquetas textuales. La traducción congelada es:
`Yes → 1/sí`, `No → 0/no`, `Refused → rechazo`, `Don't know → no sabe` y
vacío → no aplica o faltante determinado por la ruta. Los literales numéricos
`"1"` y `"0"` en el CSV son inválidos: pertenecerían a la cara numérica del
codebook y mezclarlos con etiquetas podría invertir o vaciar un estimando.

Un vacío fuera de ruta nunca se convierte en no. Dentro de un universo se
separan rechazo, no sabe y ausencia sin clasificar. `shedid` debe ser único;
`weight` y `weight_pop` deben ser finitos y positivos.

## Rutas y cinco estimandos

1. **Uso BNPL.** Todas las personas con `BNPL1` válido; numerador `Yes`.
2. **Atraso.** `BNPL1=Yes` y `BNPL3` válido; numerador `BNPL3=Yes`.
3. **Cargo por atraso.** `BNPL1=Yes`, `BNPL3=Yes` y `BNPL3A` válido;
   numerador `BNPL3A=Yes`. Appendix A también pregunta `BNPL3A` si `BNPL3`
   fue rechazado: esas respuestas se publican aparte y no entran en esta tasa.
4. **Sobregiro atribuido a BNPL.** `BK1=Yes` habilita `BK2_f`; el estimando
   exige `BNPL1=Yes`, `BK2_f=Yes` y `BNPL1A` válido. Su numerador es
   `BNPL1A=Yes`. No se completa con ceros a los demás usuarios BNPL.
5. **Asequibilidad y atraso.** Entre usuarios con `BNPL4_e` y `BNPL3`
   válidos, tabla ponderada 2×2 y diferencia descriptiva
   `P(BNPL3=Yes | BNPL4_e=Yes) − P(BNPL3=Yes | BNPL4_e=No)`.

Cada estimando entrega `n` elegible, válido y positivo; masa elegible, válida
y positiva; punto, faltantes por razón y definición. La tabla 2×2 entrega
conteo y masa por celda, tasas por fila y diferencia.

## Precisión y límites

No se producen EE ni IC. Los pesos de postestratificación permiten los puntos,
pero por sí solos no acreditan todo el diseño ni una varianza oficial; no se
inventa UPM, estrato o bootstrap de filas. No se construye “cualquier daño”,
no se interpreta `BNPL4_e` como tratamiento, no se transporta una tasa a
México y no se mezcla el atraso autodeclarado con default CFPB a 120 días.

El acto autoriza explícitamente este objeto nuevo y su spec descriptiva; por
eso cuenta como una medición GEN2. Esa autoridad no adopta ningún resultado ni
cierra `NC-0164`.
