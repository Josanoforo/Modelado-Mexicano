ESTADO: GATEADO
ENTORNO: NUBE
ENCOLADO: 2026-09-08 · ACTO GEN2-T7-CIERRE reemplaza este encargo por "E6 · ACTO GEN2-E6 · AUTOMATIZA-GEN2-2 · v1.3", texto de `ENCARGOS-GEN2-v1_3-readiness-primero-2026-09-07.md` (adjunto por el operador). Sustituye a la versión v1.0 que estaba en la cola.
BITACORA:
- 2026-09-08 · GATEADO. Sustituye a la v1.0 porque dirección emitió `ENCARGOS-GEN2-v1_3-readiness-primero-2026-09-07.md`, que reordena la automatización antes de los cálculos: T-REPRO en v1.3 se endurece contra el esquema de E3.1 (spec_yaml_sha256, input_sha256 efectivos, resultado_replay, contexto_replay) e incorpora los checks 11.1/11.2 de inmutabilidad estructural, y elimina el hardcode histórico del tablero. COMPUERTA: `git ls-tree -d --name-only origin/main data/corrida0/ | grep -c "^data/corrida0/CALC-000"` ≥ 2 — hoy es 0, así que queda `GATEADO`.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

## E6 · ACTO GEN2-E6 · AUTOMATIZA-GEN2-2 · v1.3 — registro, status, tablero, T-REPRO sobre el esquema endurecido

Cabecera: **NUBE** · **Opus** · COMPUERTA por producto: `git ls-tree -d --name-only origin/main data/corrida0/ | grep -c "^data/corrida0/CALC-000"` ≥ 2. NO se lanza en UBUNTU.
Qué hace: `cmd_registro` (une `demanda-*.tsv` + `decisiones.tsv` + `CALC-*/` → `corridas.tsv · resultados.tsv · usos.tsv`, `# DERIVADO — NO EDITAR`; campos del esquema de E3.1: `spec_yaml_sha256 · input_sha256 efectivos · resultado_replay · contexto_replay · estado (…SELLADA | SUPERADO→sucesor)`; validaciones que paran: ids duplicados, RESULT sin CALC, uso a RESULT inexistente, CALC sin spec, RESULT sin sello, hash ausente, ciclo, consumidor activo apuntando a LEGACY; avisan: RESULT sin consumidor, CALC sin consumidor activo, legacy sin sucesor; `CALC-SMOKE-*` con `cuenta_gen2 = NO`) · `cmd_status` (§9 del plan) · `tools/tablero_programa.py` deriva de `status` y **elimina el hardcode histórico** (marco anterior al v1.3) · **T-REPRO** en `tests/check.py` (`T33`): cada RESULT activo GEN2 con cadena completa; consumidor→RESULT→CALC resolubles; `valor materializado == RESULT` dentro de tolerancia por tipo; **más** (11.1) todo CALC activo con `spec_yaml_sha256`, `script_blob_sha256`, `input_sha256` completos y (11.2) inmutabilidad estructural — artefactos sellados coinciden con su sello, sin reejecutar microdato. Línea base congela GEN1; si E5 pidió cambios de esquema, se declaran y el gate entra en la versión siguiente.
Perímetro: `tools/corrida0.py` (`cmd_registro`, `cmd_status`) · `tools/tablero_programa.py` · `tests/test_corrida0.py` · `tests/check.py` · `data/corrida0/{corridas,resultados,usos}.tsv` · cascada. Si te encuentras escribiendo fuera de esta lista, PARA.
Contador: cero directo; el tablero pasa a derivar GEN2.
