# ACTO MAESTRA38-N2 · TESTS-FRENTE-A-B — lista de tests y el defecto real que cada uno fija

Encargo: `forense/encargos/2026-09-04-MAESTRA38-N2-TESTS-FRENTE-A-B.md`.
SHA base reconfirmado: `68ce2a8d` (Merge PR #527).

Arranque (`tests/` en `68ce2a8d`): `test_manifiesto_alcance.py` es el único
test del manifiesto; **no hay ningún test del writer de cola**
(`tools/curador_registro/tsv_crudo.py`, `tools/vista_cola_adquisicion.py`,
`tools/curador_registro/registra_cola_adquisicion.py`, la parte de
`tools/arbitra.py` que toca `data/cola-adquisicion-v1_0.tsv`). Frente C sí
tiene cobertura (`tools/curador_registro/tests/test_alta_relacion.py`) — de
ahí el desbalance A/B que este acto cierra. FP-287 (AUSENCIA DE TESTS
AUTOMATIZADOS para Frente A y Frente B de MAESTRA37-INFRA-1) → EJECUTADA
por este acto.

Commit siguiente añade dos archivos, todos con fixtures `tempfile` — ningún
caso toca `data/` real:

## `tests/test_cola_writer.py`

| test | defecto real que fija |
|---|---|
| `test_upsert_fila_no_corrompe_comillas_sueltas` | **FP-258** — round-trip `csv.reader`/`csv.writer` corrompía 4/112 líneas del registro (comillas sueltas en `nota`, `forense/notas/2026-09-03-MAESTRA37-N2-control.md`). Fija que `tsv_crudo.upsert_fila` toca solo la línea que cambia, byte a byte, sin reinterpretar el resto. |
| `test_upsert_fila_reemplaza_in_place_sin_tocar_otras` | Mismo escritor canónico: un upsert de clave existente reemplaza in-place sin agregar fila ni tocar ninguna otra — la garantía que hace seguro reprocesar la misma celda dos veces (`tools/arbitra.py::encola_no_obtenido`). |
| `test_vista_es_pura_funcion_del_registro` | **arbitra.py escribía la vista** (histórico, ya corregido: ver docstring de `tools/arbitra.py::_regenera_vista_cola_adquisicion`). Fija que `vista_cola_adquisicion.build()` es función pura del registro — nunca lee ni depende de lo que ya hay en la ruta VISTA — para que un futuro escritor directo de la vista no pueda "mezclarse" con lo que había antes. |
| `test_registra_cola_adquisicion_exige_confirmacion_para_escribir` | **migrador invertido** — `registra_cola_adquisicion.py` es la migración legacy de una sola vez, dirección cola→registro (`write_tsv` trunca el SSOT); corre guardado detrás de `--confirmo-migracion-legacy`. Fija que sin esa bandera el script falla y **no escribe `--output` en absoluto**. |
| `test_arbitra_nunca_escribe_la_vista_directamente` | **arbitra.py escribía la vista** + **dos escritores el 3/sep** — analiza el AST de `tools/arbitra.py` y falla si aparece un `open(COLA, 'w'...)` fuera de `_regenera_vista_cola_adquisicion` (que delega en subprocess a `vista_cola_adquisicion.py`, el único escritor legítimo de la vista). Sin este test, reintroducir una escritura directa a la vista reabre la misma clase de defecto que ya se corrigió. |

## `tests/test_manifiesto_seguro.py`

| test | defecto real que fija |
|---|---|
| `test_registra_no_sobreescribe_id_existente` | Regla explícita de `cmd_registra`: un id que ya existe es ERROR, nunca un edit silencioso — sin test, un refactor futuro podría convertir el `sys.exit(1)` en overwrite sin que nada lo note. |
| `test_registra_no_duplica_por_sha256` | Dedup por contenido — el propio docstring de `tests/manifiesto.py` cita el caso ya ocurrido: dos entradas para el mismo PDF de ENCIG bajo dos ids, de dos sesiones que no se vieron (30/jul). Reproduce esa condición y exige que el segundo `--registra` falle. |
| `test_escritura_atomica_no_corrompe_si_falla_validacion` | `_escribir_atomico` + `_validar_manifiesto_completo`: una entrada que rompe la validación (aquí, `tamano_bytes` no entero) nunca debe tocar el archivo en disco — el temporal se valida antes de `os.replace()`. Fija la garantía del propio docstring con un caso real, no solo con la prosa. |
| `test_lock_serializa_dos_escritores_concurrentes` | **dos escritores el 3/sep** (`forense/hallazgos.md` 2026-09-03, MAESTRA37-A1: "ningún test lo atrapa") y su precedente estructural, **ACTO R/R″** (12/ago, `forense/hallazgos.md` — dos clones registraron los mismos payloads el mismo día porque nada coordinaba escrituras concurrentes). Corre dos `cmd_registra` de verdad en paralelo (hilos, no simulado en secuencia) sobre el mismo `data/manifiesto.yaml` y exige que las dos entradas sobrevivan sin pisarse — mide la protección real (`_con_lock_manifiesto`, `flock` exclusivo), no solo su existencia en el código. |

## Fuera de alcance de este acto, declarado

**PR #77** (payload que queda solo en el worktree de la sesión y no llega al
corpus compartido) no tiene un test unitario en este lote: el defecto es
sobre *dónde vive el corpus compartido* (una ruta externa al repo,
resuelta por `data/raices.local.yaml` o el entorno de la sesión), no sobre
una función pura que un fixture temporal pueda ejercitar sin tocar
infraestructura real. Queda como hueco declarado — el ARRANQUE de `/acto`
(punto 3, "verifica al cerrar que los payloads quedaron en el CORPUS
COMPARTIDO") sigue siendo la mitigación operativa vigente para ese
defecto, no un test.

## Verificación de cierre

`python3 tests/check.py --baseline`: LÍNEA BASE VERDE (19 FAIL · 171 WARN,
sin entradas nuevas frente a `tests/baseline.json`) antes y después de
añadir los dos archivos de test — ninguno de los dos participa en
`tests/check.py` (son suites independientes, corridas con
`python3 tests/test_cola_writer.py` / `python3 tests/test_manifiesto_seguro.py`,
mismo patrón que `tests/test_manifiesto_alcance.py`).
