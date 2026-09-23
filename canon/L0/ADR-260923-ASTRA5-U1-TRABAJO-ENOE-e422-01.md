# ADR-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01

**Acto:** ASTRA5-U1-TRABAJO-ENOE. **Fecha:** 23/sep/2026.
**Entorno:** CAJA, corpus montado. **Modo:** rígido para COMMIT-1/COMMIT-2.
**Raíz D-24:** `e422`, commit del encargo archivado. **Compuerta:**
ninguna de merge; el encargo autoriza push y PR, pero mesa fusiona y decide
adopción. Base al abrir `origin/main=8e41f72fa8b00a20e83f28c92f6b2964e66b0081`.

Se reciben tres afirmaciones U0 de `8f7e8de0` y se registra el diseño ENOE
N. Se congeló la matriz de 13 conductas por 43 olas elegibles y la spec de
pisos antes del dato. Dos intentos iniciales de adapter fallaron sin RESULT:
v1.0 por BOM 2022T2 y v1.1 por alias de entidad 2025T3/T4; sucesores
documentados y congelados antes de reejecutar. `CALC-ENOE-PISOS-0003`
sella 26,273 celdas, 13 conductas, 43 olas. `CALC-ENOE-PERSISTENCIA-0001`
sella 20,304 pares agregados dentro de era, 12 conductas, origen móvil.
Ambos `verify` dan `REPRODUCE · CONTEXTO=IDENTICO`, con asiento en
`forense/replay-evidencia.tsv`. No adopta. No se modifica el motor ni las
vistas globales. Los CALC quedan **sellados en disco, no registrados** hasta
la derivación por el canal vigente.

La última ola del corpus 2026T1 queda reservada en ambos ids del manifiesto
y sin abrir; 2026T2, publicado oficialmente al corte, está ausente del
corpus. Los pisos 2024T3 confirman solo la mayoría en empleo informal,
dejan sin contraste directo la frase de contratos por cambio de universo y
matizan el componente semanal de >50 horas. Prevalencia no es transición.
Cuidados específicos, transición formal/informal, ingreso real e IC
predictivo calibrado quedan no identificados con los insumos sellados,
asentados en cuatro NC exactas. La evaluación de persistencia es
retrospectiva, no validación predictiva.

**Cascada:** `forense/notas/2026-09-23-ASTRA5-U1-TRABAJO-ENOE-cierre.md`
contiene números, RESULT/CALC/hash, corte U0, saltos, reservas, pruebas y
recibo Codex→Claude. `forense/firmas-pendientes.tsv` gana una FP por
instrumento (`FP-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01`) para adopción de
mesa; `forense/no-corrido.tsv` gana cuatro NC de límites y reserva.
`canon/registro-rotulos.tsv` gana un rótulo GEN2. `celdas_validadas` no se
toca: no hubo duelo ni predicción predeclarada validada. Reportar 13
conductas distintas y 26,273 celdas por separado. Mesa fusiona el PR y
resuelve la FP; fusionarlo no abre 2026T1.
