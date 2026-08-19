# Nota del acto · ACTO REFIRMA-OPACA — los cuatro expedientes se re-firman con V5, y V5 no era el número que el encargo traía escrito

**Fecha:** 19/ago/2026 · **Rama:** `refirma-opaca` · **Encargo:** `forense/encargos/2026-08-18-REFIRMA-OPACA.md` · **Origen:** `FP-47`, `D-6` de `ADR-101(j)`

---

## 0 · ARRANQUE

1. **ENTORNO.** UBUNTU, con microdato real en `/home/pc0/mm-corpus/raw/`. Es el entorno que el encargo exige: `validate_master_spec` aborta sin `input_path`/`hash_microdato` reales, y por eso la caja de nube que redactó el encargo no pudo correrlo.
2. **REPO.** Worktree nuevo `/home/pc0/mm-refirma-opaca`, rama `refirma-opaca` desde `origin/main = e563e5d`. A media ejecución `origin/main` avanzó a `e6864ed` (`PR #267`, `ACTO MESA-19AGO`); se fusionó antes de escribir nada en `forense/`, sin conflicto, y **todas las mediciones se repitieron sobre el árbol fusionado**.
3. **SHA.** El encargo declara `93a4dd9`. Re-derivado: es ancestro de `e6864ed`, avance limpio.
4. **Microdato.** Los cuatro `input_path` existen y sus `sha256` coinciden con `hash_microdato` de la maestra, verificado antes de correr nada.

---

## 1 · D-6 y V5 — la re-medición que el encargo mandó hacer, y que cambió el número

`D-6` de mesa, **verbatim**:

> **"se re-firman con V5."**

El encargo es explícito sobre qué es V5, y se manda a sí mismo desconfiar de su propia cifra:

> *"La 'V5' de mesa es el `baseline_sha256` **vigente al ejecutar**, no una constante heredada de este encargo."*
> *"Re-deriva este valor al ejecutar — no lo heredes de aquí; si `baseline.json` cambió entre este encargo y su ejecución, el valor real es otro y el expediente debe firmarse contra ese, no contra el de esta línea."*

**Cambió.** El encargo trae escrito `db88a09a…`, y `FP-47` (redactada el 17/ago) certifica que `ACTO MESA-18AGO` lo re-derivó *"SIN CAMBIO"* ese mismo día. Al ejecutar:

```
$ sha256sum data/curacion-registro/baseline.json
a8782ca10b664cccee955b07c92eff3a70a3177385ce29b4982a3ac004d7a9b2
```

Son **tres** valores distintos en la vida de este objeto, y los tres están en el árbol:

| valor | quién lo movió | qué papel juega |
|---|---|---|
| `4dd527eb…` | estado original | el que los cuatro expedientes traían incrustado |
| `db88a09a…` | bootstrap semántico de `BARRIDO-2` (`93160c3`) | el que `FP-47` y el encargo tienen escrito |
| **`a8782ca1…`** | **`620d524`, `ACTO B2-SEMANTICO` C5** | **V5 — el vigente al ejecutar, el que se firmó** |

El tercer movimiento es **legítimo y trazable**: `620d524` integró 37 relaciones por `integrate.py --barrido2`, y el `diff` de `baseline.json` es exactamente lo que una integración produce — tres `sha256` de contenido reescritos (`evidencias.tsv`, `relaciones.tsv`, `utilidad-modelo.tsv`), **conteos de filas sin mover** (200/199/199). No es deriva: es el registro cambiando porque se integró en él.

*Lección: la instrucción de re-derivar no es ceremonia. `MESA-18AGO` midió bien y su medición era correcta cuando la hizo; entre esa medición y esta ejecución corrió un acto entero con integración, y el número caducó. Un encargo que hereda una constante firma contra un pasado; uno que manda re-derivarla firma contra el presente. Este encargo mandó re-derivarla — por eso el expediente quedó bien.*

---

## 2 · Localización de `--config` y `--snapshot`

El encargo los dejó `A DERIVAR`. Derivados del propio árbol, y **corroborados de forma independiente** por el test que `FP-47` cita, que declara las mismas dos rutas en sus constantes de módulo:

| argumento | archivo | prueba |
|---|---|---|
| `--config` | `data/curacion-registro/especificaciones-produccion.json` | único archivo del repo con la clave `specifications`; contiene exactamente las cuatro `ESP-OPACA-{A,B,C,D}` |
| `--snapshot` | `data/curacion-universo/snapshot-t0.json` | declara `snapshot_t0_sha256 = 89f4c3a49c00c0e1ba1f…`, cuyo prefijo de 16 es el nombre del directorio `t0-89f4c3a49c00c0e1` |

Nota sobre la clave: el encargo la llama *"las cuatro `especificaciones`"*; en el archivo y en el código la clave es `specifications`. Mismo objeto, nombre distinto — se deja escrito para que la próxima búsqueda no falle por buscar el término en español.

---

## 3 · El perímetro del encargo no alcanza a su propio cierre — medido, no argumentado

El encargo pide dos cosas que no pueden ser ciertas a la vez:

- **ESCRIBE:** sólo `especificacion-recibida.json` · **NO ESCRIBE:** *"ningún otro archivo de `data/curacion-registro/`"*.
- **Cierre:** *"cero divergencia contra la maestra"* y `test_produccion_correctiva` *"cae de 4 fallas a 0"*.

La razón es estructural y está en el motor: **`resultado.tsv` y `resumen.json` incrustan el hash de la propia especificación** (`produce.py:230` `hash_especificacion_input`, `produce.py:260` `hash_especificacion_recibida`). Re-firmar el spec cambia su `sha256`; los otros dos artefactos quedan apuntando al spec viejo, y el supervisor —que reproduce con el motor versionado y compara byte a byte— falla igual, sólo que con otro mensaje.

Los tres estados, **corridos, no razonados**:

| estado | no pasan | causa |
|---|---|---|
| antes (`e563e5d`) | **5** (4F + 1E) | 4 × `especificación recibida difiere de maestra canónica` · 1 × `2 != 3` |
| sólo `prepare_production` (perímetro literal) | **4** (3F + 1E) | 3 × `artefacto no coincide con reproducción supervisora:…:resultado.tsv` · 1 × `2 != 3` |
| cadena completa (`prepare_production` + `produce`) | **2** | `11 != 12` · `2 != 3` |

Y un detalle que sólo aparece corriéndolo: bajo el perímetro literal **`test_3` pasa de `ok` a `FAIL`**. Es una prueba de garantía fail-closed que espera el mensaje `maestra canónica`; al arreglar a medias, el expediente empieza a fallar por otra razón y la prueba deja de ver lo que vigila.

**Ninguno de los tres estados llega a verde.** Las dos fallas residuales no son de este acto — §6.

---

## 4 · Lo autorizado, y lo ejecutado

Llevado a mesa con las tres cifras ya medidas. Mesa autorizó **ampliar el perímetro a `produce.py`**: regenerar también `resultado.tsv`, `resumen.json` y `hashes.json` de los cuatro, siempre por herramienta canónica y **nada a mano**. La ampliación es coherente con el título del encargo: *re-firma* significa volver a firmar, y la firma de un expediente **es** `hashes.json`; media firma deja el expediente internamente inconsistente.

`produce.py` no es una herramienta ajena: `execute()` es **el mismo motor** que el supervisor usa para reproducir (`integrate_production.py:185`). Correrlo no puede introducir nada que el supervisor no derive por su cuenta.

Salida cruda íntegra de la cadena, comando por comando:

```
$ sha256sum data/curacion-registro/baseline.json
a8782ca10b664cccee955b07c92eff3a70a3177385ce29b4982a3ac004d7a9b2  data/curacion-registro/baseline.json

$ python3 tools/curador_registro/prepare_production.py --config data/curacion-registro/especificaciones-produccion.json --snapshot data/curacion-universo/snapshot-t0.json --baseline data/curacion-registro/ --output-root data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/
{
  "ok": true,
  "specifications": [
    "/home/pc0/mm-refirma-opaca/data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-A-7baf278d/especificacion-recibida.json",
    "/home/pc0/mm-refirma-opaca/data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-B-d13ec4fe/especificacion-recibida.json",
    "/home/pc0/mm-refirma-opaca/data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-C-9ecb5c61/especificacion-recibida.json",
    "/home/pc0/mm-refirma-opaca/data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-D-d800e103/especificacion-recibida.json"
  ]
}

$ python3 tools/curador_registro/produce.py --spec data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-A-7baf278d/especificacion-recibida.json --output-dir data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-A-7baf278d
{
  "calculos_reproducibles": 2,
  "cegado": true,
  "especificacion_id": "ESP-OPACA-A-7baf278d",
  "hash_especificacion_recibida": "7d1f79f21b64995ad1d0868a6d6f9b85a67a8f2e8d1bc8bb049c6dca3ac6daa6",
  "hash_microdato_verificado": "afe9013a4cc26538dfe81da686f0d09e756a7d0e2fc407cd22f596fd53c0f354",
  "motor": "tools/curador_registro/produce.py",
  "no_determinado": 0,
  "ok": true,
  "variables": 2
}

$ python3 tools/curador_registro/produce.py --spec data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-B-d13ec4fe/especificacion-recibida.json --output-dir data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-B-d13ec4fe
{
  "calculos_reproducibles": 1,
  "cegado": true,
  "especificacion_id": "ESP-OPACA-B-d13ec4fe",
  "hash_especificacion_recibida": "0ba8d258f636a12306e641211c854bb91706af98e8ed304316faa449fb528c4c",
  "hash_microdato_verificado": "8a5e8c5ed2dcda6e25dfe2dd630c0ac7273e0736e7b99662a15a4ef68c3ab36e",
  "motor": "tools/curador_registro/produce.py",
  "no_determinado": 0,
  "ok": true,
  "variables": 1
}

$ python3 tools/curador_registro/produce.py --spec data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-C-9ecb5c61/especificacion-recibida.json --output-dir data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-C-9ecb5c61
{
  "calculos_reproducibles": 8,
  "cegado": true,
  "especificacion_id": "ESP-OPACA-C-9ecb5c61",
  "hash_especificacion_recibida": "570f1d5e6c8b97974376ed5f6aecf784f44830792ac7868956fb3892954757c3",
  "hash_microdato_verificado": "afe9013a4cc26538dfe81da686f0d09e756a7d0e2fc407cd22f596fd53c0f354",
  "motor": "tools/curador_registro/produce.py",
  "no_determinado": 0,
  "ok": true,
  "variables": 8
}

$ python3 tools/curador_registro/produce.py --spec data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-D-d800e103/especificacion-recibida.json --output-dir data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-D-d800e103
{
  "calculos_reproducibles": 1,
  "cegado": true,
  "especificacion_id": "ESP-OPACA-D-d800e103",
  "hash_especificacion_recibida": "0411501497522078cc671ca30b2674b575b3e9537652bd95f1674b7023bbe855",
  "hash_microdato_verificado": "8a5e8c5ed2dcda6e25dfe2dd630c0ac7273e0736e7b99662a15a4ef68c3ab36e",
  "motor": "tools/curador_registro/produce.py",
  "no_determinado": 0,
  "ok": true,
  "variables": 1
}
```

`analisis-reproducible.py` **no cambió** en ninguno de los cuatro: no incrusta hash, y el motor lo reescribe idéntico. El acto toca **16 archivos, 4 por expediente**, no 20.

---

## 5 · Controles

**Ninguna cifra se movió.** Control duro sobre `resultado.tsv`: retirada la columna `hash_especificacion_input`, las filas de los cuatro expedientes son **idénticas** a las de `HEAD` — cada proporción, cada error estándar, cada `ic95`, cada `n_categoria`, cada suma de pesos, cada `estado_celda`. El acto mueve firmas, no mediciones. Los conteos lo confirman por otra vía: 12 filas / 12 `CALCULO_REPRODUCIBLE` / 0 `NO_DETERMINADO`, **antes y después**.

**Diff total:** 16 archivos, 32 inserciones, 32 supresiones — una línea por archivo en `especificacion-recibida.json` (`baseline_sha256`) y las correspondientes de hash en los otros tres.

**Verificación supervisora independiente**, sobre el directorio real y tras la fusión de `origin/main`:

```
verify_production_bundle(...) -> OK. filas: 12 | CALCULO_REPRODUCIBLE: 12
```

Antes del acto esa misma llamada abortaba con `ValueError`. Ahora completa: **cero divergencia contra la maestra**, que es el cierre material que el encargo pedía.

**Idempotencia probada.** Segunda corrida completa de la cadena sobre el resultado de la primera: los 20 archivos del directorio dan `sha256` **idéntico byte a byte**.

**Sin daño colateral.** Los cuatro módulos de prueba que fallan en el árbol se midieron a los dos lados del acto:

| módulo | `e563e5d` prístino | con el acto |
|---|---|---|
| `test_barrido_completo` | 5 F | 5 F (igual) |
| `test_semantic_run` | 1 F + 1 E | 1 F + 1 E (igual) |
| `test_t0_identity` | 3 F | 3 F (igual) |
| **`test_produccion_correctiva`** | **4 F + 1 E** | **2 F** |

El acto mueve **un solo** módulo, y sólo hacia abajo. Los otros doce módulos de `tools/curador_registro/tests/` dan `OK`.

**`tests/check.py --baseline`: VERDE** — `21 FAIL · 119 WARN`, nada nuevo frente a `tests/baseline.json` (congelado `e24d033`). Se midió también sobre el árbol prístino y da **exactamente lo mismo**: este acto no mueve `--baseline` ni un WARN. **La cifra se recifró tres veces durante esta revisión, y las tres correcciones se dejan escritas** porque ninguna de las variaciones es de este acto: `19 FAIL · 124 WARN` sobre `e563e5d`; `19 FAIL · 118 WARN` al fusionar `e6864ed` (`PR #267`, `MESA-19AGO`, seis firmas propagadas); y `21 FAIL · 119 WARN` al fusionar `2d08d7a` (`PR #274`, `rescate/curador-untracked`, que además **recongeló** `tests/baseline.json` — el `HEAD` congelado pasa de `997482b` a `e24d033`). En los tres árboles el acto mide **idéntico con y sin él**, que es la única afirmación que le pertenece. Es literalmente la lección que `ACTO ESTADO-SPLIT` dejó escrita el 18/ago — *un contador derivado no es propiedad del acto que lo deriva, sino del árbol* —, y la única forma de tener la cifra es volver a correr la suite después de fusionar. Se volvió a correr las tres veces. Se deja escrito porque `FP-47` afirmaba *"esta fila ES la entrada que pone `--baseline` en ROJO"* — **eso ya no es cierto** al ejecutar, y no lo dejó de ser por este acto; la cascada de `B2-SEMANTICO` lo había resuelto antes. Sin `--freeze`.

---

## 6 · Lo que queda abierto, y por qué no se tocó aquí — `FP-60`

Las dos fallas que sobreviven **no son de este acto y son más viejas que el encargo**:

- `test_valid_bundle_is_independently_reproduced_without_analyst_manifest` espera `11` filas y `10` reproducibles; el árbol tiene **12 y 12**.
- `test_production_semantics_and_periods_are_preserved` espera `2` descriptivos y `1` listo para modelo, y que `ESP-OPACA-B` esté en `NO_DETERMINADO`; el árbol da **3 y 3**, y `B` reproduce.

Fechadas por comando, no por lectura: el archivo de prueba **no se ha tocado desde `59d6c40`** (`BARRIDO-COMPLETO`), y el expediente `B` pasó de `repro=0, nd=1` a `repro=1, nd=0` en **`8565c17`, `U1/E4b′ commit 2` (12/ago)** — el primer resultado calculado del programa. Ese acto movió la realidad y dejó las expectativas de la prueba donde estaban. `produccion-modelo.tsv` es **byte-idéntico** entre `93a4dd9` y hoy, así que la falla `2 != 3` existía, tal cual, cuando se redactó el encargo.

No se corrigen aquí por tres razones, en orden de peso: `tests/` está en `NO ESCRIBE`; son las cifras testigo de una **garantía fail-closed**, y ajustarlas es adjudicación de mesa, no higiene de un acto de re-firma; y el defecto nació seis días antes, en un acto ajeno. Queda como **`FP-60`**. *(Renumerada **dos veces** durante esta misma revisión, y por la misma causa: nació `FP-58`, pasó a `FP-59` al fusionar `6650047` porque `PR #275`/`ADR-111` ocupó el `FP-58`, y pasa a `FP-60` al fusionar `2d08d7a` porque `PR #274` ocupó el `FP-59`. Los dos números se derivaron del tablero fusionado, ninguno se tecleó. Es literalmente lo que la propia `FP-47` dejó escrito de sí misma tras sus dos renumeraciones — «lo que le pasa a una fila que espera mientras el tablero avanza en otras ramas» —, y ahora está documentado a los dos lados de la misma compuerta.)*

*Lección, y es la misma que el encargo ya sabía sobre `baseline.json` pero no aplicó a sus propias cifras: **un encargo redactado donde no se puede ejecutar cuenta las fallas que alcanza a ver.** La caja de nube abortaba en el primer expediente por falta de microdato, así que el mensaje de divergencia enmascaraba todo lo que venía detrás; las dos expectativas rancias eran invisibles desde ahí. La cifra "4 fallas" del encargo era correcta para las que comparten mensaje, e incompleta para el archivo.*

---

## 7 · Cierre

- Los cuatro expedientes **re-firmados contra `a8782ca1…`**, el `baseline_sha256` vigente al ejecutar, re-derivado dos veces (antes de correr y después de fusionar `origin/main`), nunca tecleado.
- **Cero divergencia contra la maestra**, verificado por `verify_production_bundle` sobre el directorio real.
- Todo por herramienta canónica; **ninguna edición a mano** de ningún artefacto.
- `FP-47` → `FIRMADA`, con `D-6` verbatim y el `baseline_sha256` real usado.
- `tests/check.py --baseline` **VERDE**.
- `FP-60` abierta por las dos expectativas rancias de `test_produccion_correctiva` (nació `FP-58`, renumerada dos veces: `PR #275` y `PR #274`).
- Encargo `CONSUMIDO`.
