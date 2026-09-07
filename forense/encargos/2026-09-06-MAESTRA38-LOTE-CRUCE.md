CAJA · ACTO MAESTRA38-LOTE-CRUCE · A3-cruce + N16 + C + ENVIPE + COERCITIVO + LAPOP-21/23 — invoca /acto (D-11)

COMPUERTA: ninguna · ENTORNO: UBUNTU con corpus, sin red · MODELO: Opus (el criterio «parecido nominal no cuenta» es juicio). FIRMAS — verbatim: «no quiero hacerlo al mínimo no después de haber invertido tanto en la infraestructura» (4/sep); FP-303 sonda con bytes (5/sep, explora); FP-316 (b) firmada (ADR-363: R7.4 ACOTADA, «pieza ENVIPE en el cruce»); A6 §3 «Son 29… para que el LOTE-CRUCE (pieza N16-bis) no la vuelva a derivar»; SELLO-2 §B (7/sep): LAPOP 2021/2023 «en corpus, 0 filas en el inventario» → pieza (f). A.8 al arrancar: spec de A3 = forense/notas/2026-09-05-MAESTRA38-N12-spec.md (19 instrumentos mínimos verbatim; parecido nominal no cuenta); rutas reales en manifiesto de las tres fuentes de A4 (cultura_constitucional_unam_iij/, ecopred2014/, Los mexicanos vistos por sí mismos — localizar por comando: python3 - <<'EOF' sobre archivo: con vistos|unam.*2015|mvsm; pegar) y de BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO (A6); ENVIPE (ids y olas); cuestionarios para N16: ENCUP 2012, CIDE-CSES 2015 (3 .sav), Latinobarómetro 2024, LAPOP 2019/2021/2023 (mexico_lapop_americasbarometer_2019_v1_0_w, mex_2021_lapop_americasbarometer_v1_2_w, mex_2023_lapop_americasbarometer_v1_0_w); lista C = las 29 relaciones NO-ENCONTRADO de forense/notas/2026-09-06-MAESTRA38-A6-resultados.md §3 (copiar, no re-derivar); regla tramite.gobierno_digital.coercitivo en milpa/tramite.yaml (única sin dato) y sus dos entradas coercitivo_* en la propuesta (se_mueve_si ya escrito: «instrumento de encuesta con tenencia vigente de e.firma por persona (ENCIG/ENDUTIH/ENIF, ítem nuevo)»). ya_medido.py no aplica (no se mide) — se dice. COMMIT-1: este bloque congelado como forense/prereg-caja/S11-CRUCE-spec-v1_0.md + .sha256, con universo de búsqueda declarado por pieza. COMMIT-2, por pieza (una que PARA no tumba el lote):

(a) A3-cruce (Ola 6). tools/inventario_reactivos.py --raiz descargas_mx sobre las subcarpetas de las tres fuentes de A4 + la base de protesta → data/inventario-reactivos-descargas-mx-v1_2.tsv (v1_1 intacto). Cruce de los 19 instrumentos mínimos con texto a la vista: CUBIERTO-POR (fuente, ítem, texto) / PARCIAL / SIN-COBERTURA-EN-ESTAS-FUENTES, universo por línea → data/cruce-ola6-v1_0.tsv. Enmienda append a FP-303: «A3 corrió: k de 19». modulo-propio-v0 (append) con lo SIN-COBERTURA.
(b) N16 (R7.3/R7.6). Tres constructos — beneficiario de programa social (Oportunidades/Prospera/Bienestar); «le condicionaron / le pidieron el voto a cambio»; secreto del voto percibido — sobre ENCUP 2012, CIDE-CSES 2015, Latinobarómetro 2024, LAPOP 2019/2021/2023 → data/cruce-r7-v1_0.tsv.
(c) ENVIPE (R7.4, FP-316 b). Los tres antecedentes de C_agravio tal como los define S5-L5-spec-v1_0.md §3.1 (leer, no recordar) contra ENVIPE (olas en corpus): CUBRE / PARCIAL / NO-CUBRE + n rural declarado por el FD → data/cruce-envipe-agravio-v1_0.tsv. Si CUBRE: «candidata a S5 v1.1» en la nota; la spec la escribe otro acto.
(d) Lista C (29 relaciones). Por cada NO-ENCONTRADO: constructo pedido (de relaciones.tsv) buscado por texto en v1_1 + ext + v1_2 → PARALELA-CUBRE (fuente, ítem, texto) / PARALELA-PARCIAL / NINGUNA-EN-CORPUS → data/cruce-relaciones-noencontrado-v1_0.tsv. No se editan las relaciones.
(e) coercitivo (B2, S1). El instrumento mínimo que declara la regla y sus dos entradas (tenencia vigente de e.firma por persona) cruzado contra el inventario completo → línea en data/cruce-r7-v1_0.tsv o archivo propio; CUBIERTO / PARCIAL / SIN-COBERTURA. Si SIN-COBERTURA, dirección re-especifica; si hay cobertura, spec N7.
(f) LAPOP 2021/2023 al inventario. tools/inventario_reactivos.py (o _ext) sobre mex_2021_lapop_americasbarometer_v1_2_w y mex_2023_lapop_americasbarometer_v1_0_w (raíz descargas_mx, Descargas Manuales/) → filas en v1_2; verificación: clien1n, clien1na, vb2, AOJ11, AOJ12 aparecen con su texto. Es la condición de tres se_mueve_si de SELLO-2 (R7.7, R7.6 brazo proximidad, R10.3). Sin veredicto de regla en ninguna pieza.

PERÍMETRO. Toca: data/inventario-reactivos-descargas-mx-v1_2.tsv (nuevo) · data/cruce-*.tsv (nuevos) · forense/prereg-caja/S11-* · milpa/modulo-propio-v0* (append) · INFRAESTRUCTURA · forense/notas/2026-09-0X-MAESTRA38-LOTE-CRUCE-{spec,resultados}.md · hallazgos · tablero (recibo + enmienda FP-303) · A.3 · cascada. NO toca: manifiesto · cola · relaciones · milpa/tramite*.yaml · canon (salvo ADR) · specs S1–S10 · data/l*-* · tests/*.py · tools/*.py. En paralelo: C1. CONTADOR: instrumentos mínimos de Ola 6 con cobertura conocida 0 → k de 19 · constructos R7 con instrumento fuera de MPS 0 → j de 3 · antecedentes de C_agravio en ENVIPE 0 → declara · relaciones NO-ENCONTRADO con paralela 0 → declara de 29 · coercitivo con instrumento 0 → declara · reactivos inventariados de LAPOP 2021/2023 0 → n · medición: cero (cruce).

---

## A.8 · `tools/ya_medido.py` — anexo del EJECUTOR, fuera del bloque verbatim

El bloque de arriba es el encargo VERBATIM (A.3) y no se edita. El encargo
dice «ya_medido.py no aplica (no se mide) — se dice»: este acto no clasifica,
pre-registra, carga ni sella ninguna regla — sólo cruza texto de reactivo
contra instrumentos mínimos. Aun así se corre la herramienta y se pega su
salida, porque `T-YAMEDIDO` (`tests/check.py`) la exige mecánicamente para
todo encargo archivado que cite un `id`/`R-n`, y `tests/*.py` es NO-TOCA en
el perímetro de este acto (no se puede usar el allowlist). Corrido el
6/sep/2026 en el clon de ARRANQUE·1:

```
$ for x in R7.3 R7.4 R7.6 R7.7 R10.3 tramite.gobierno_digital.coercitivo; do python3 tools/ya_medido.py "$x"; done
R7.3  -> MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md, 2026-09-07-MAESTRA38-CARGA-LAPOP-2-spec.md, L11, L12, L2, L9, N6, S2, S4, canon§7, tramite-ola5-propuesta-v0.yaml, tramite.yaml
R7.4  -> MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md, 2026-09-07-MAESTRA38-CARGA-LAPOP-resultados.md, L11, L5, L9, S5
R7.6  -> MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md, 2026-09-07-MAESTRA38-CARGA-LAPOP-2-spec.md, L11, L12, L2, L4, L9, S4, canon§7
R7.7  -> MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md, L12, L9, MAESTRA38-SELLO-2
R10.3 -> MEDIDA-EN: L18
tramite.gobierno_digital.coercitivo -> NUNCA-MEDIDA
```

Ninguna de las seis se reabre en este acto. Las cinco `MEDIDA-EN:` se citan
como estado existente; `tramite.gobierno_digital.coercitivo` sale
`NUNCA-MEDIDA`, que es exactamente la premisa de la pieza (e) («única sin
dato») y este acto la deja igual: cruza su instrumento mínimo contra el
inventario y no emite veredicto de regla.
