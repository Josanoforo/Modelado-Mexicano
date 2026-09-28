# Insuficiencias de la spec humana

## 1. Escalas 0–10 con unidad «proporcion» — 90 llaves (NO-RECALCULABLE-DESDE-SPEC)

Conductas afectadas, 15 llaves cada una (TOTAL, SEXO×2, EDAD×4, ESCOLARIDAD×4, TLOC×4):
satisfaccion-vida (PA1), escalera-cantril (PA5), confianza-mayoria-gente (PB1_01),
confianza-gente-conocida (PB1_02), confianza-policia-municipal (PB1_04), confianza-partidos (PB1_11).

`esquema-identidades.tsv` pide para estas identidades `unidad=proporcion` y sufijo `-P`. En cambio, la spec de punto
(`enbiare-metodo-base.md`: «se publican como **media**»; tabla: «0–10 | media») y el módulo IC firmado
(«Escalas0..10 medias; demás conductas proporciones») solo definen una media en escala 0–10. Ningún documento
fija el corte o la categoría que convertiría la escala en proporción (p. ej. «≥ k»), y publicar la media bajo
`unidad=proporcion` contradice «proporciones están en0..1» y «sin … convertir escala». Para cerrar el faltante
hace falta una de dos cosas: que el esquema corrija la unidad a media, o que una spec fije la dicotomización.
No se adivinó ninguna de las dos. El n válido y las exclusiones bajo la validez 0–10 están en `diagnostico.json`.

## 2. Observaciones que no bloquearon el cálculo

- Se aplicó el contrato P3 firmado, que desplaza a la base en la semilla de IC (20260924 → 20260923) y en el
  tratamiento de UPM única («certeza»). Ver D07.
- Denominador cero: el contrato de edades dice NO-ESTIMABLE y CONTRATO-v3 ofrece DENOMINADOR-CERO. Se eligió
  el de v3 (D11). No ocurrió ningún caso.
- La traducción de un singleton a `estado_ic` no está fijada textualmente; se eligió NO-IDENTIFICADA (D10).
  El marco tiene 0 singletons, así que no se activó.
- La integridad del payload `enbiare2021_bd_csv_zip` (sha256 `afe9013a…`) no se pudo verificar: el paquete
  entrega los CSV ya extraídos, sin el zip.
- La firma R26b limita el IC a reproducibilidad diagnóstica: «no certifica cobertura del 95%».
