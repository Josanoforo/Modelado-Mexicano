# Nota del acto · ACTO FP60-ADJUDICA — las dos expectativas rancias de `test_produccion_correctiva`

**Fecha:** 19/ago/2026 · **Encargo:** `forense/encargos/2026-08-19-FP60-ADJUDICA.md` · **Origen:** `FP-60` (`ACTO REFIRMA-OPACA`, `forense/notas/2026-08-19-refirma-opaca.md` §6)

---

## 0 · ARRANQUE

1. **REPO.** Clon existente, `/home/user/Modelado-Mexicano`. `git log -1`: `20c7dee8d5bf1216c4c60be91578c904659aa3cc` — Merge PR #283, `ACTO REFUTACIONES-SIN-OBJETO`. `git status`: limpio, rama `claude/fp60-produccion-correctiva-x0tqh7`.
2. **SHA.** Encargo dice `20c7dee`. Igual — no se movió.
3. **`data/raw`.** No se toca. Este acto no lee ni escribe microdato.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — crudo, sin sonda.
5. **ESPEJO.** Nada del espejo. El "11 filas y 1…" del encargo se re-deriva abajo, del test y de la corrida.

---

## 1 · Qué esperan hoy las dos expectativas (ruta:línea, antes del acto)

```
$ sed -n '135,166p' tools/curador_registro/tests/test_produccion_correctiva.py
```

```python
    def test_valid_bundle_is_independently_reproduced_without_analyst_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            analyst = self._copy_analyst(Path(temp_name))
            for manifest in analyst.glob("*/hashes.json"):
                manifest.unlink()
            rows = verify_production_bundle(CONFIG, SNAPSHOT, BASELINE, analyst)
            self.assertEqual(11, len(rows))                                            # :141
            self.assertEqual(10, sum(row["estado"] == "CALCULO_REPRODUCIBLE" for row in rows))  # :142

    def test_production_semantics_and_periods_are_preserved(self) -> None:
        ...
        self.assertEqual(2, len(descriptive))                                          # :155
        self.assertEqual(1, len(model_ready))                                          # :156
        ...
        b_row = next(row for row in rows if row["especificacion_id"].startswith("ESP-OPACA-B"))
        self.assertEqual("NO_DETERMINADO", b_row["estado"])                            # :165
```

## 2 · Qué produce la realidad vigente

`test_produccion_correctiva.py:141-142` corre dentro de `verify_production_bundle`, que exige el microdato real (`prepare_production.validate_master_spec`). Esta caja es NUBE, repo-only, sin `/home/pc0/mm-corpus/raw/` — el mismo límite que `ACTO REFIRMA-OPACA` ya declaró para sesiones NUBE. No puede correrse aquí; su valor real ya fue medido en UBUNTU por ese mismo acto, el mismo día:

```
verify_production_bundle(...) -> OK. filas: 12 | CALCULO_REPRODUCIBLE: 12
```

(`forense/notas/2026-08-19-refirma-opaca.md` §5, "Verificación supervisora independiente".)

`test_production_semantics_and_periods_are_preserved:155-165` sólo lee `data/curacion-registro/produccion-modelo.tsv` — no toca microdato, corre en NUBE:

```
$ python3 -c "
import csv
with open('data/curacion-registro/produccion-modelo.tsv', encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
print('total rows', len(rows))
desc = {r['relacion_id'] for r in rows if r['estado_calculo_descriptivo']=='CALCULO_DESCRIPTIVO_DISPONIBLE'}
model = {r['relacion_id'] for r in rows if r['estado_uso_modelo']=='LISTA_PARA_USO_MODELO'}
print('descriptive', len(desc))
print('model_ready', len(model))
b = [r for r in rows if r['especificacion_id'].startswith('ESP-OPACA-B')]
print('B rows', [(r['especificacion_id'], r['estado']) for r in b])
"
total rows 12
descriptive 3
model_ready 3
B rows [('ESP-OPACA-B-d13ec4fe', 'CALCULO_REPRODUCIBLE')]
```

Antes de editar el test, corrida completa del módulo (con `jsonschema` instalado — no estaba disponible en la caja, `pip install jsonschema`, dependencia de `integrate_production.py`, sin relación con este acto):

```
$ python3 -m unittest tools.curador_registro.tests.test_produccion_correctiva -v
...
FAIL: test_1_result_changed_without_resigning_fails         -- microdato ausente (NUBE)
FAIL: test_2_result_changed_and_resigned_still_fails         -- microdato ausente (NUBE)
FAIL: test_3_received_spec_changed_and_resigned_still_fails  -- microdato ausente (NUBE)
FAIL: test_4_wrong_microdata_hash_in_master_fails             -- microdato ausente (NUBE)
FAIL: test_5_integrated_table_changed_after_integration_fails -- microdato ausente (NUBE)
ERROR: test_valid_bundle_is_independently_reproduced_without_analyst_manifest -- microdato ausente (NUBE)
FAIL: test_production_semantics_and_periods_are_preserved -- AssertionError: 2 != 3

Ran 8 tests in 0.119s
FAILED (failures=6, errors=1)
```

`2 != 3` confirma, por comando, la fila `FP-60` tal como la dejó `ACTO REFIRMA-OPACA`: el árbol da 3 descriptivos (no 2), 3 listos-para-modelo (no 1), y `ESP-OPACA-B` reproduce (no `NO_DETERMINADO`). Los otros seis fallos/errores son de microdato ausente — fuera del perímetro de este acto, mismo defecto que ya fallaba antes de tocar nada.

## 3 · Adjudicación

**Vocabulario A.4 aplicado a expectativas** (regla del encargo, no A.4 original sobre existencia de reactivo):

- **`RANCIA-SE-ACTUALIZA`** para las dos: la realidad nueva es la correcta. El motor canónico (`prepare_production.py`→`produce.py`→`integrate_production.py`) sobre el `baseline_sha256` vigente produce 12 filas/12 `CALCULO_REPRODUCIBLE`/3 descriptivos/3 listos-para-modelo/`B` reproduce, verificado dos veces de forma independiente (UBUNTU por `REFIRMA-OPACA`, NUBE por este acto sobre el artefacto trackeado) sin discrepancia entre ellas. No es `VIGENTE-SE-CONSERVA`: no hay defecto que reportar, las dos mediciones coinciden. No es `MAL-PLANTEADA`: ambas comparan el mismo universo (filas y estados de un mismo bundle) — el predicado no cambia, sólo el valor.
- **Causa, fechada por comando** (ya la había derivado `REFIRMA-OPACA` §6, re-verificada aquí): el archivo de prueba no se toca desde `59d6c40` (`BARRIDO-COMPLETO`); `ESP-OPACA-B` pasó de `repro=0/nd=1` a `repro=1/nd=0` en `8565c17` (`U1/E4b′` commit 2, 12/ago/2026) — el primer resultado calculado del programa. Ese acto movió la realidad; el test se quedó donde estaba.
- **No divergen entre sí** (ambas `RANCIA-SE-ACTUALIZA`), y aun así quedan en dos métodos de test separados — el test ya las tenía partidas así; este acto no las funde.

## 4 · El diff, ejecutado

```
tools/curador_registro/tests/test_produccion_correctiva.py
:141  self.assertEqual(11, len(rows))                                           -> self.assertEqual(12, len(rows))
:142  self.assertEqual(10, sum(row["estado"] == "CALCULO_REPRODUCIBLE" ...))     -> self.assertEqual(12, sum(...))
:155  self.assertEqual(2, len(descriptive))                                     -> self.assertEqual(3, len(descriptive))
:156  self.assertEqual(1, len(model_ready))                                     -> self.assertEqual(3, len(model_ready))
:165  self.assertEqual("NO_DETERMINADO", b_row["estado"])                       -> self.assertEqual("CALCULO_REPRODUCIBLE", b_row["estado"])
```

Cinco líneas, ningún otro carácter del archivo tocado.

## 5 · Verificación tras el cambio

```
$ python3 -m unittest tools.curador_registro.tests.test_produccion_correctiva.FailClosedProductionTests.test_production_semantics_and_periods_are_preserved -v
test_production_semantics_and_periods_are_preserved ... ok
```

`test_valid_bundle_is_independently_reproduced_without_analyst_manifest` sigue con `ERROR` (microdato ausente) — sin cambio atribuible a este acto, mismo error antes y después del diff (verificado: el traceback es idéntico byte a byte, la excepción se dispara antes de llegar a la línea de la aserción).

```
$ python3 tests/check.py --baseline
...
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
21 FAIL · 117 WARN
```

Sin `--freeze`.

## 6 · Cierre

- `tools/curador_registro/tests/test_produccion_correctiva.py`: las dos expectativas rancias, adjudicadas `RANCIA-SE-ACTUALIZA`, actualizadas.
- `forense/firmas-pendientes.tsv`: `FP-60` → `CERRADA`.
- `canon/gobernanza-v1_15.md`: `ADR-118`.
- `canon/estado-programa-v1_10.md`: cascada (cabecera, `L0`, lista append-only, WARN 118→117).
- `forense/hallazgos.md`: una línea.
- Encargo `forense/encargos/2026-08-19-FP60-ADJUDICA.md` → `CONSUMIDO`.
- `tests/check.py --baseline`: VERDE.
- Contadores de medición sobre México: **0**.
