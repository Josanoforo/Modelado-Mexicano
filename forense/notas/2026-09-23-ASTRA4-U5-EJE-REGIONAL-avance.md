# ASTRA4-U5 · Región · recibo Codex para Claude

**Contadores antes/después:** CALC regionales sellados `0 → 15`; filas del canon regional `0 → 584`; comparaciones retrospectivas muestrales `0 → 204` y predictivas `0 → 70`. Comandos: `python3 tools/astra/region/publica.py` y `python3 tools/astra/region/mapa.py` sobre el HEAD del PR [#1072](https://github.com/Josanoforo/Modelado-Mexicano/pull/1072). Es un **avance con reservas materiales**, no cierre integral ni adopción.

## EJECUTADO

- R1/R2 aprobadas por mesa antes del microdato y fijadas en specs humanas/ejecutables: entidades admisibles ENVIPE/ENCIG, seis regiones oficiales ENIF; publicación solo con n no ponderado ≥200, varianza estimable y regla oficial más estricta.
- Tres pisos iniciales, ocho olas históricas, un bloque de siete conductas de ahorro ENIF, el complemento ENVIPE desde RESULT sellados, cuatro consumidores ENCIG 2025 y un CALC predictivo derivado de RESULT, con sello y `python3 tools/corrida0.py verify <CALC>` = `REPRODUCE` en los quince; asiento por CALC en `forense/replay-evidencia.tsv`. Se abrió únicamente payload no reservado del perímetro ENVIPE 2023/24/25, ENCIG 2017/19/21/23/25 y ENIF 2018/21/24. El complemento y el predictivo no reabrieron raw. No hubo descarga nueva.
- Canon TSV/MD generado por comando, con 584 claves únicas, 564 estados PUBLICABLE y 20 SUPRIMIDA-N en este lote, RESULT y hash por fila. Setenta filas separadas citan el punto del piso y los límites predictivos de dos CALC. El estado de publicación no convierte n≥200 en garantía de precisión. El complemento `tiene_ahorros + no_ahorra = 1` se cotejó en las seis regiones ENIF 2024; `cumple_norma = 1−evade_norma` invierte punto, IC y réplicas en 2023/24/25. Los cuatro puntos nacionales reconstruidos de ENCIG 2025 coinciden exactamente con `CALC-ENCIG-0001`.
- Mapa descriptivo: 88/204 puntos posteriores dentro del IC muestral anterior; 116/204 fuera. Wilson binomial solo referencia condicional a independencia geográfica, que no se acredita como inferencia de diseño. Todo **RETROSPECTIVA**.
- Mapa predictivo derivado: ajuste exclusivo 2023→24 ENVIPE, 2017→19/19→21/21→23 ENCIG y 2018→21 ENIF; evaluación posterior 2025/25/24. Punto observado dentro del IC predictivo en 32/32, 29/32 y 6/6 geografías, respectivamente. Conteos descriptivos, sin IC de cobertura por conglomerado ni promesa de detección futura.
- ADENDA-1: consumida matriz U1 del commit `3d8e82fb`; 0 de 5 cuestionarios cotejados acredita regla AMAI exacta. No se activó quinta decisión, no hay NSE ni cruces región×clase. La hoja de mesa enumera los componentes ausentes.
- `python3 tools/sella_sha256.py --verifica --cuerpo` devolvió `SELLO_COINCIDE` para el encargo original y ADENDA-1 archivados.
- Se congeló snapshot U1 de 37 identidades consumidoras pertinentes, con RESULT y estado; códigos de interacción todavía requieren desdoblar el estimando. El universo general de conductas **no está cerrado** por ese número.
- Tests: `python3 -m pytest -q tests/test_astra4_region.py` → 8 passed; `python3 tools/ci_guardias.py --ejecuta-huerfanos` → 79 ejecutados, 67 saltados, 0 fallidos en el lote anterior; `python3 tests/check.py --baseline` → exit 0 con fallos T06/T08 de línea base en el lote anterior. El aviso T13 propio se corrigió. `python3 tests/check.py --rapido` → 0 FAIL en el lote anterior. CI remoto del HEAD de PR pendiente al redactar.

## LEÍDO

- Encargo archivado verbatim y su adenda sellada en `forense/encargos/`; brief de dirección, AGENTS, instrucciones vigentes y `/acto`.
- Manifiesto, fichas de diseño y cuestionarios de las olas usadas; métodos existentes de persistencia ENIF/ENCIG y módulo de réplicas compartidas fijado por SHA.
- Matriz AMAI y matriz de consumo U1 por commit `3d8e82fb` de `origin/codex/astra4-catalogo-1`, sin editar catálogo U1 ni worktree ajeno.

## REPORTADO / RESERVAS

- PR [#1072](https://github.com/Josanoforo/Modelado-Mexicano/pull/1072) en borrador, fusionable al último cotejo, para revisión de mesa. `adopta: NO`; este mandato no autoriza fusionar ni levantar reservas.
- Falta medir y dictaminar todas las conductas adoptadas/adoptables conocidas; `forense/analisis/region/cobertura-conocida-v1_0.md` y `alcance-u1-v1_0.tsv` muestran el faltante. El portafolio ENIF 18+ cubre su consumidor general y la serie informal 18–70 conserva un universo histórico distinto.
- El IC predictivo sin fuga de las tres series disponibles se produjo; una sola transición de evaluación por serie y escasas transiciones de ajuste ENVIPE/ENIF limitan la inferencia. No hay cobertura por conglomerado válida. Las comparaciones del mapa no se nombran estabilidad inferencial ni detección futura.
- Las corridas están **selladas en disco, no registradas** en vistas derivadas `data/corrida0/corridas.tsv`/`resultados.tsv` hasta el carril de publicación posterior al merge. No se editaron derivados para simular registro.
