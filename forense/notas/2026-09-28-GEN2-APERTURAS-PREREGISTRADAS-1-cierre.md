# Nota de cierre · ACTO GEN2-APERTURAS-PREREGISTRADAS-1 · 28/sep/2026

ADR-260928-GEN2-APERTURAS-PREREGISTRADAS-1-68b3-01 · rama `claude/new-session-bhqoo8` · 0-bis `68b3c611` · base `9d2550b9` (= SHA de redacción; 0 commits detrás).

**Contadores movidos: cero.** No abre, no mide, no adopta, no pide firmas.

## ARRANQUE
- [EJECUTADO] Entorno (hook): `ENTORNO-DERIVADO = NUBE`, `montado=NO archivos_examinados=0`, red `DENEGADA-POR-POLITICA`. Coincide con el encargo (NUBE). `data/raw` ausente: no se crea (nada se descarga).
- [EJECUTADO] Duplicado: `git ls-remote --heads origin | grep -ic APERTURAS` → 0; un worktree.

## P1 · Inventario por id
- [EJECUTADO] Premisa §3 caída (logística, prevista): el campo no es `reserva` sino `estado_reserva`. Vocabulario (conteo por lector YAML sobre 7198 entradas): `RESERVADA-NO-ABIERTA-NO-INDEXAR-L` 173 · `RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO-ABRIR` 4 · `DOCUMENTACION-ESTRUCTURAL-NO-RESPUESTAS` 45 (documentación, no reserva de respuestas: fuera).
- [EJECUTADO] `python3 forense/prereg-aperturas/inventario_aperturas.py --escribe` → `filas=30 ids=198`: 27 programa×ola con campo (177 ids) + 3 por firma/encargo sin campo (ENVIPE 2026, ENIGH 2024, ENIF 2024).
- [EJECUTADO] `cruces_vistos` derivado de todo `data/corrida0/CALC-*/spec.yaml`.

## P2 · Expedientes
- [LEÍDO] `forense/analisis/familias-2027/familias-2027-estado-v1_0.tsv`: las 8 familias apuntan a olas 2027 → **ninguna ola hoy reservada es R de una familia**.
- Contendientes sellados que nombran una ola reservada como R: `CALC-ENSANUT-PISOS-SALUD-0001` (spec.yaml:22 `ola_reservada: ENSANUT 2025`; piso 2024 con ICC, spec §4) y `CALC-ENCODAT-PISOS-SUSTANCIAS-0001` (spec.yaml:22). Expediente completo en `forense/prereg-aperturas/{ENSANUT,ENCODAT}-2025/`: `APERTURA-<X>-spec-v1_0.md` + sidecar, `APERTURA-<X>-spec.yaml`, `medidor_apertura_<x>.py`, `RECETA-APERTURA-<X>.md`.
- Rama prevista del encargo tomada: los cuestionarios 2025 están en el manifiesto pero no montados (NUBE); códigos fijados sobre el cuestionario de la ola del piso, rotulado; regla fijada: columna sin texto/códigos iguales en el catálogo 2025 → NO-ESTIMABLE al abrir.
- Guardia común `forense/prereg-aperturas/guardia_apertura.py`: auditoría AST (groupby/value_counts multi-llave, crosstab, pivot, pivot_table, unstack, lectura fuera de `lee_payload_reservado`), agregador único de una variable, adjudicación de cobertura (Wilson; CALIBRADO/SUBCUBRE/SOBRECUBRE/NO-ESTIMABLE).
- [EJECUTADO] `python3 -m pytest -q tests/test_prereg_aperturas.py` → `29 passed`: 8 mutaciones × 2 medidores detectadas, borrado de la auditoría detectado, cruce rechazado, cuatro ramas del dictamen, medidores sobre sintético con el esquema de cada ola, vista cubre todo id reservado, ningún payload reservado en la lista de leídos.
- 27 expedientes mínimos (`EXPEDIENTE-<X>.md`).

## Premisas caídas (no PARO; declaradas)
- **ENVIPE 2026 ya abierta**: `CALC-DUELO-ENVIPE2026-ADJUDICACION-0001` (ejecucion.json `2026-09-22T20:19:14Z`, veredictos `NADIE-VENCE`/`PISO`) y `-MARGINALES-ADJUDICACION-0001` (`2026-09-23T01:01:47Z`). Fila `PREMISA-CAIDA-YA-ABIERTA`.
- **ENIF 2024 ya abierta** por `CALC-C2-COMPUESTO-IC-ENIF2024-0001` y otros cuatro CALC. Fila `PREMISA-CAIDA-YA-ABIERTA`.
- **ENIGH 2024**: apertura parcial ya hecha (AMAI C7 y duelo nacional de remesas); resto: solo mesa.
- **ENDUTIH 2025**: RESERVADA en el campo, consumida por tres CALC sellados (hallazgo en `forense/hallazgos.md`).
- **ENCIG 2025 fuera del árbitro, ENSU/ENOE último periodo, CSES módulo 5**: sin contendiente sellado que las use como R → expediente mínimo (solo mesa por escrito). ENCIG 2025 está abierta según la memoria y no tiene id reservado: sin fila.

## P3 · Vista y tablero
- `data/corrida0/aperturas-pendientes-v1_0.tsv` registrada en `data/INFRAESTRUCTURA-v1_0.md`.
- `tools/tablero_carriles.py`: F15, 9 líneas añadidas (≤ 10). [EJECUTADO] `--json` → el stopper RESERVA cita el expediente (ENCODAT-2025, ENDUTIH-2025, ENOE-2026T2). `--verifica` da `NO-CASA` en md/html **también sin mi cambio** (el job derivados lo regenera).

## Archivos leídos
`forense/prereg-aperturas/archivos-leidos-v1_0.txt` (test: ningún id ni archivo reservado del manifiesto aparece).

## Auditoría (v2.16)
PROSPECTIVA por construcción en los dos expedientes (contendiente sellado antes de R); unidad persona; un eje a la vez; oferta antes que preferencia en conductas de uso de servicios; nada se mezcla con RETROSPECTIVO. Cifras a mano: ninguna.
