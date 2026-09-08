# ACTO GEN2-E3-1-1 · CABLEADO-FINAL-DEL-RUNNER — nota de cierre

**Fecha.** 8/sep/2026 · entorno NUBE · sin microdato, sin red, sin corpus.
**Base.** `origin/main` = `df9336c` (merge de PR #608, `GEN2-E3-1 ·
READINESS-DEL-RUNNER`).
**Encargo verbatim (A.3).**
`forense/encargos/2026-09-08-GEN2-E3-1-1-CABLEADO-FINAL-RUNNER.md`.
**Contador GEN2:** cero. Este acto no produce ninguna medición.

---

## 1 · Compuerta, verificada POR PRODUCTO

El encargo declara la compuerta con sus propios comandos y así se verificó —
no por `grep` sobre `git log`, que `ADR-277` ya midió como falso positivo:

```
$ git show origin/main:tools/corrida0.py | grep -q 'CALC-INMUTABLE'    → OK
$ git show origin/main:tools/corrida0.py | grep -q 'contrato_ejecutable' → OK
$ git show origin/main:tools/corrida0.py | grep -q '_verifica_sello'   → OK
```

Las tres presentes: PR #608 está fusionado. No se recreó nada de #608.

Guard de arranque: base al día (`git rev-list --count HEAD..origin/main` = 0),
árbol limpio, sin duplicado del rótulo (rama remota ausente · un solo worktree ·
cero PR abiertos, consultados por el tool de GitHub porque `gh` no existe en
este entorno), `tools/limpia_arbol.py --reporta` pegado en el PR.

## 2 · A.8 — los cuatro defectos, confirmados por lectura ANTES de tocar

Ninguno estaba corregido por un commit posterior a #608. Se leyó
`tools/corrida0.py` en `origin/main`:

| # | Defecto | Evidencia leída en `origin/main` |
|---|---|---|
| D1 | Doble resolución de payload | `preflight` → `_verifica_inputs` llama `resolver_payload`; `_inputs_para_medidor(spec)` lo vuelve a llamar por su cuenta; `_ejecuta(spec)` recibe solo `spec`. Tres hechos, no uno. |
| D2 | Omisiones silenciosas | `contrato_ejecutable` rellenaba con `spec.get(<dim>, "NO-APLICA")` para las cinco dimensiones, y `preflight` no exigía que existieran. `seed: {aplica: true, valor: 42}` pasaba sin `rng` (el bloqueo sólo miraba `valor`). |
| D3 | `verify` con tolerancia global | `tol = spec.get("tolerancia") or {}` y `_compara(previos[k], valores[k], tol)` para TODOS los RESULT; `_compara` decide entero/flotante por `tol["tipo"]`. La salida reejecutada no pasaba por `_valida_outputs`. |
| D4 | Sellador sin consecuencia | `run` corría `sella_sha256.py`, imprimía `r.returncode` y devolvía `"EJECUTADO" if exit_code == 0` — el `exit_code` del MEDIDOR. |

## 3 · Qué cambió

### P1 · Snapshot único de inputs

`_verifica_inputs` se partió en dos piezas que ya no pueden confundirse:

* **`_resuelve_inputs(spec)`** — resolución, y sólo resolución. Devuelve el
  SNAPSHOT: `{id, origen, ruta_absoluta, raiz_logica, sha256, estado}` por
  input, más `bytes` para `origen: repo` (los MISMOS bytes que el SHA
  verificado identifica: se leen una vez, se hashean, y el medidor recibe
  esos, no lo que el disco traiga un instante después). Para
  `origen: manifiesto` viene directo del resolver compartido.
* **`_bloqueos_de_inputs(snapshot, …)`** — los veredictos sobre lo ya
  resuelto. Se juzga el snapshot; no se vuelve a resolver para juzgar.

La cadena quedó:

```
run()
  preflight()            → pre["inputs_resueltos"]   (UNA resolución)
  _ejecuta(spec, inputs_resueltos)
      _inputs_para_medidor(spec, inputs_resueltos)   → transforma, no resuelve
  _construye_ejecucion(...)  input_sha256 ← el MISMO snapshot
```

`_ejecuta` e `_inputs_para_medidor` reciben el snapshot como argumento
**obligatorio, sin valor por defecto**: un llamador que no lo traiga es un
llamador que iba a resolver por segunda vez, y ahora falla al llamar en vez de
fallar en silencio. Un input declarado en la spec y ausente del snapshot se
levanta como error de cableado, no se resuelve sobre la marcha.

En `verify`, una sola resolución por invocación alimenta las DOS cosas que la
necesitaban: la comparación de CONTEXTO (`_evalua_contexto`, que antes
re-resolvía cada input de manifiesto) y la reejecución del medidor.

### P2 · Spec explícita, no `NO-APLICA` inventado

`DIMENSIONES_SUSTANTIVAS` (once campos: `variables · universo · filtros ·
ponderador · transformacion · estimando · parametros · seed ·
dependencias_materiales · resultados · tolerancia`) se exige **presente** en
`preflight` → `campo_sustantivo_ausente=<campo>`.

El test de presencia es `campo in spec`, no `spec.get(campo)`: `variables: []`
y `dependencias_materiales: []` son vacíos DECLARADOS —es lo que ambos smokes
traen— y no pueden confundirse con ausencia. `ponderador: NO-APLICA` sigue
siendo una declaración válida; `ponderador` ausente ya no lo es.

**Compatibilidad, explícita y por marca ya existente en el árbol.** Las dos
specs selladas declaran `etiquetas.generacion: LEGACY-GEN1`. Esa marca —no un
esquema nuevo— es la que exime del endurecimiento (`_esquema_endurecido()`).
El default es ENDURECIDO: una spec que no dice nada es nueva. `CALC-SMOKE-0001`
y `0002` no se tocaron, ni un byte.

`seed` acepta dos formas y ninguna más: `{aplica: false}`, o
`{aplica: true, valor: …, rng: …}`. Falta `valor` → `seed_aplica_sin_valor`;
falta `rng` → `seed_aplica_sin_rng`. No se inventa RNG por omisión: una corrida
estocástica sin RNG declarado no es reproducible, y decir que lo es sería el
defecto, no el bloqueo. Un `seed` escalar sólo lo admite el esquema legado
(`CALC-SMOKE-0001`).

Antes de abrir microdato, `preflight` valida la DECLARACIÓN del schema de
outputs (`_bloqueos_de_resultados`): id no vacío, tipo permitido, unidad no
vacía, `permite_no_estimable` booleano si aparece. La unicidad de ids ya la
comprobaba el paso 3 y no se repite. La validación de los VALORES producidos
sigue siendo de `run` (`_valida_outputs`) — son dos cosas distintas y no se
colapsan.

### P3 · `verify` realmente por RESULT

`_compara_result(previo, hoy, decl, tol)` toma el tipo autoritativo de la
entrada de `resultados:` para ESE id:

```
entero      int de Python (no bool), comparación EXACTA
texto       str, comparación EXACTA
flotante    finito, abs(delta) <= tolerancia declarada
proporcion  finito, en [0,1], abs(delta) <= tolerancia declarada
```

La tolerancia global sigue siendo la MAGNITUD por defecto (`tol["abs"]`, que es
como las specs de hoy la declaran); lo que ya no sale de ella es la SEMÁNTICA
de la comparación. Un RESULT sin declaración cae al comparador general
`_compara`, que no cambia. No se inventó un esquema de tolerancia por RESULT.

Y antes de comparar contra el recibo, los outputs REEJECUTADOS pasan
`_valida_outputs(spec, valores_replay)`. Si lo violan, `RESULTADO =
NO-EJECUTABLE` — nunca `REPRODUCE`: lo que reprodujo sería algo que la spec no
autoriza a producir.

### P4 · `EJECUTADO` sólo si el sello quedó válido

Tras escribir `ejecucion.json` / `resultados.json` / `sello.json` y correr
`tools/sella_sha256.py`, `run` exige **las dos cosas**: `r.returncode == 0`, y
que el sello RECIÉN escrito verifique con el mecanismo que ya existe
(`_verifica_sello`: sidecar + cada archivo que cubre). Sólo entonces
`veredicto = EJECUTADO`. Si falla cualquiera de las dos:
`veredicto = FALLO-SELLADO`, `exit != 0`, y el CALC **no** se declara sellado.

Los JSON intermedios quedan como intento incompleto: al no existir sello
válido, `_calc_ya_sellado()` es falso y `run` puede reintentar sobre ellos.
No se fabricó sidecar de rescate.

## 4 · Tests (P5) — siete casos nuevos, ninguno de ceremonia

`tests/test_corrida0.py`: 38 → 45 casos, todos verdes. `tests/check.py` T32 los
descubre por `corre()`, así que no hizo falta abrir ningún control nuevo.

* `t_snapshot_input_unico` (D1) — mokea `resolver_payload` para devolver A en
  la primera llamada y B en la segunda. Afirma que la segunda **no existe**, y
  que el sha/ruta A llega al medidor y a `ejecucion.json`.
* `t_snapshot_repo_trae_los_bytes` (D1) — cara `origen: repo`: los bytes del
  snapshot son los que su sha256 identifica, y llegan al medidor.
* `t_spec_no_aplica_explicito` (D2) — `NO-APLICA` declarado no bloquea;
  ausente sí. Recorre las once dimensiones **en un bucle sobre
  `DIMENSIONES_SUSTANTIVAS`**, no un test por campo. Incluye el vacío
  declarado y la exención del esquema legado.
* `t_seed_rng_obligatorio` (D2) — `aplica: true` sin `rng` → BLOQUEADO; sin
  `valor` → BLOQUEADO; completo y `{aplica:false}` → no bloquean.
* `t_preflight_valida_schema_de_resultados` (D2) — las cuatro reglas del
  schema de outputs.
* `t_verify_tipo_por_result` (D3) — con `tolerancia: {tipo: flotante, abs:
  1e-10}` global y `RESULT-N: entero`, un replay `1.0` contra `1` sellado NO
  reproduce. El caso además **afirma la premisa**: `_compara(1, 1.0, tol)`
  sigue devolviendo `True`, así que si algún día el defecto se corrigiera en
  otro sitio el test lo dice en vez de pasar por inercia. Incluye un flotante
  dentro de tolerancia (sí reproduce) y una proporción fuera de [0,1]
  (`NO-EJECUTABLE`, no `REPRODUCE`).
* `t_sellador_falla_no_ejecutado` (D4) — medidor OK + outputs OK +
  `sella_sha256` con `returncode != 0` → `FALLO-SELLADO`, y
  `_calc_ya_sellado()` falso.

Cuatro casos existentes se re-cablearon a la firma nueva (`_ejecuta`,
`_inputs_para_medidor`, `_resuelve_inputs`) sin cambiar lo que afirman.

## 5 · P6 · Smoke

**No nació `CALC-SMOKE-0003`.** Los siete casos de arriba ejercitan el
cableado de forma suficiente y sin corpus —incluidos el snapshot único (con
mock de `resolver_payload`) y el fallo del sellador (con `subprocess.run`
mokeado)—, así que un smoke nuevo sería ceremonia. `CALC-SMOKE-0001` y
`CALC-SMOKE-0002` no se tocaron.

## 6 · Comprobaciones de salida

```
python3 tests/test_corrida0.py   → 45 casos · 45 ok · 0 FALLOS
python3 tests/check.py --baseline → LÍNEA BASE: VERDE (3 FAIL heredados: T06, T08, T-CRON/T25 resueltos)

SNAPSHOT-INPUT-UNICO=PASS
SPEC-EXPLICITA=PASS
SEED-RNG-OBLIGATORIO=PASS
VERIFY-TIPO-POR-RESULT=PASS
SELLADOR-FALLA-NO-EJECUTADO=PASS
CALC-INMUTABLE-REGRESION=PASS
CALC-SMOKE-0002-INMUTABLE=PASS
BASELINE=VERDE
```

`python3 tools/corrida0.py run CALC-SMOKE-0002` sigue respondiendo
`CALC-INMUTABLE · YA-SELLADO`, con el hash del directorio idéntico antes y
después (`9b9701a4…`). `verify CALC-SMOKE-0002` devuelve
`REPLICA-RESULTADO · CONTEXTO-DISTINTO (razón: commit_distinto)` — que es la
respuesta CORRECTA tras avanzar el commit, y no se alteró el smoke para forzar
un verde cosmético.

## 7 · Máquina de estados

`estado_calc(calc_id)` **no se implementó**: no hace falta para cerrar ninguno
de los cuatro defectos, y el encargo lo autoriza explícitamente a quedar para
`GEN2-E5-0`, como ya declaró #608. Se asienta en `## NO-CORRIDO / RESERVAS`.

## 8 · Límites declarados (A.13)

* Ningún test abre microdato, red ni corpus. `data/raw` ausente (normal en la
  nube); `raices_logicas: data_raw · configurada=NO`;
  `acceso_corpus: montado=NO, archivos_examinados=0`.
* `run()` no se puede correr punta a punta sobre un fixture temporal: exige
  `preflight` VERDE, que a su vez exige `spec.yaml` COMMITEADO, y un fixture
  vive fuera del repo. `t_sellador_falla_no_ejecutado` sustituye `preflight`
  por su resultado ya calculado para ejercer el tramo posterior al medidor
  —que es justo lo que el caso mide—; es el mismo patrón que la nota de
  cabecera del archivo de tests ya declara para los catorce casos de #608.
* El endurecimiento P2 se probó contra fixtures, no contra las tres specs
  reales de `CALC-0001/0002/0003`: esas todavía no existen (`GEN2-E5-0`).

## 9 · Veredicto

```
GEN2-RUNNER-READY=SI
GO-CALC-0001=SI
```

Los siete puntos del CRITERIO DE GO se cumplen. Esta es la última modificación
del runner antes de preparar las tres specs reales.
