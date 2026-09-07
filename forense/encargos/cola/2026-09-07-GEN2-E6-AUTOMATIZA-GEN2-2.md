ESTADO: GATEADO
ENTORNO: NUBE
ENCOLADO: 2026-09-07 · ACTO GEN2-E0 · ENCOLA, skill `/encola`, PR [COLA]. Gesto de encolado: precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026).
BITACORA:
- 2026-09-07 · GATEADO · encolado por PR [COLA] encola GEN2 (plan + GEN2-E1…GEN2-E6). COMPUERTA propia, por producto: GEN2-E5 fusionado — `ls data/corrida0/ | grep -c "^CALC-000"` ≥ 2. Si falta, cero commits.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

## E6 · ACTO GEN2-E6 · AUTOMATIZA-GEN2-2 — registro, status, tablero, T-REPRO

Cabecera: NUBE · **Opus** · COMPUERTA: E5 fusionado (≥2 carpetas `CALC-000*` selladas en `main`; `ls data/corrida0/ | grep -c "^CALC-000"` ≥ 2). NO se lanza en UBUNTU.
Qué hace: `corrida0.py registro` (une demanda de E2 y oferta de `CALC-*/` → `corridas.tsv · resultados.tsv · usos.tsv` con `# DERIVADO — NO EDITAR` y las validaciones de §5 del plan: paran ids duplicados, RESULT sin CALC, uso a RESULT inexistente, CALC sin spec, RESULT sin sello, hash ausente, ciclo, consumidor activo apuntando a LEGACY; avisan RESULT sin consumidor, CALC sin consumidor activo, legacy sin sucesor); `corrida0.py status` (§9 del plan); `tools/tablero_programa.py` deriva los contadores GEN2 de `status`; **T-REPRO** como test dentro de `tests/check.py`: cada RESULT activo GEN2 con id, CALC, spec, script, código fijado, inputs, hashes, parámetros, sello, consumidor; consumidor→RESULT→CALC resolubles; `valor materializado == RESULT` dentro de tolerancia para todo valor de `tramite.yaml` que lleve `corrida0_resultado_id`; línea base congela GEN1. Se activa solo si las corridas de E5 atraviesan el formato completo; si el esquema necesita cambios, se declaran y **no se congela** el gate antes.
A.8: `grep -c "def registro\|def status" tools/corrida0.py` → 0 tras E3; `grep -n "T-REPRO\|corrida0" tests/check.py` → solo la llamada al smoke.
Perímetro: `tools/corrida0.py` · `tools/tablero_programa.py` · `tests/check.py` · `data/corrida0/{corridas,resultados,usos}.tsv` · cascada. Si te encuentras escribiendo fuera de esta lista, PARA.
Contador: cero directo; el tablero pasa a mostrar los contadores GEN2 derivados.
