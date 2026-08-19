# Índice de infraestructura interna del registro — v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `INFRAESTRUCTURA-v1_0.md` |
> | **REEMPLAZA A** | Nada — creación. Antes de este acto no existía ningún índice de infraestructura (verificado: `data/` solo tenía `UNIVERSO-MINIMO-FUENTE-v1_0.md` y `catalogo-fuentes-v2_0.md`, ninguno describe la maquinaria interna). |
> | **VERIFICAS ASÍ** | `grep -c "^## Dominio" data/INFRAESTRUCTURA-v1_0.md` da **8** (los ocho dominios de PASO 2 del encargo que lo construyó). No hay ADR que lo selle todavía — mesa decide si lo canoniza. |
> | **NOMBRE ESTABLE** | **`infraestructura-v1`** — cítalo así, nunca por nombre de archivo |

**Qué es.** El análogo hacia adentro de `UNIVERSO-MINIMO-FUENTE-v1_0.md`: en vez de "qué sitios recorrer antes de declarar `NO-ENCONTRADO`", esto es "qué tablas gobiernan cada dominio de escritura antes de que un encargo invente una vía". Por cada dominio de trabajo (adquirir, sondear, producir, adjudicar, sellar, registrar), lista las tablas verificadas con `ls`, su vía de escritura verificada con `grep`/`git log`, su contrato de campos verificado con `head -1`, y quién la lee verificado con `grep -rl`. Existe porque A.7 (`instrucciones-proyecto`, pendiente de canonizar) lo exige: *ningún encargo manda escribir en una tabla sin derivar antes qué tablas gobiernan ese dominio*.

**Qué no es.** No es documentación de negocio ni un tutorial del pipeline — para eso están los docstrings de cada script y las notas forenses citadas. No mide nada sobre México (contadores de medición movidos por este acto: **0**). No corrige ningún registro incompleto que encuentre — los reporta como hueco (ver `Colas de trabajo`, abajo). No crea ninguna vía faltante. No es exhaustivo a nivel de fila — es exhaustivo a nivel de tabla/mecanismo.

**Procedencia y vigencia.** Construido el 13/ago/2026, en un acto de **NUBE**, contra `origin/main = 2b13e88`. Describe el estado de la maquinaria **en ese commit**. ACTO W, R″ y V2 podían estar corriendo en paralelo y tocan tablas que este índice documenta — eso no es conflicto (este acto no escribe ninguna tabla), pero significa que una tabla puede tener una fila más de las que este índice vio verificar. Cuando un acto futuro descubra que el índice está desactualizado, se corrige el índice (regla de conducto, ADR-70(c)) — no hay barrido periódico programado.

---

## Dominio 1 · Adquirir una fuente / registrar un payload descargado

| tabla | vía de escritura | contrato (cabecera real) | quién la lee | trampa conocida |
|---|---|---|---|---|
| `data/manifiesto.yaml` | `tests/manifiesto.py --registra` (una entrada) o `--promueve` (mueve candidatos ya escaneados desde staging) — función `escribir_manifiesto` | YAML, lista de entradas: `archivo, raiz, sha256, tamano_bytes, fecha_descarga, entorno_descarga, descargado_por, url_origen, url_origen_sugerida, usado_para` | `tools/curador_registro/semantic_run.py`, `tests/{cal_enoe_fasea,dedup,manifiesto,calx_g3,indice,corpus,cruce_operables,idx_g3}.py` | Bug de mecanismo, documentado en el propio commit `84f8e30`: `--escanea` pliega mal escalares YAML >80 caracteres (indentación de continuación incorrecta) al escribir vía el escritor de staging; y no acumula asignaciones de `--grupo` entre invocaciones separadas del mismo escaneo. Ninguno de los dos se reparó, solo se evitó. |
| `data/manifiesto-staging.yaml` | `tests/manifiesto.py --escanea <RAIZ>` (constante `STAGING_NOMBRE`) | mismo esquema que `manifiesto.yaml` | `tests/manifiesto.py`, `tests/test_manifiesto_alcance.py` | mismo bug de plegado que arriba — le pega directo, es su escritor primario. |
| `data/curacion-registro/relaciones.tsv` | **SIN VÍA de script** — bulk-cargado una sola vez (`16180e6`, "incorpora baseline semántico N1-N33"). Todo lo demás en `tools/curador_registro/` solo lo **lee** (`baseline.py`, `bootstrap.py`, `classify_work.py`, `derive_queue.py`, `integrate.py`, `integrate_production.py`, `semantic_run.py`, `validate.py`) — ninguno tiene un `write_tsv(..., "relaciones.tsv", ...)`. | 19 campos: `relacion_id, necesidad_id, fuente_canonica_normalizada, objeto_evidencia_id_canonico, fuente_nombre, tipo_fuente, id_manifiesto, sha256_fuente, capa1_universo_indexado, capa2_manifiesto, capa3_disco_real, capa4_apertura_mapeo, clasificacion_relacion, reason_code, evidencia_ref, evidencia_textual_breve, confianza, conflicto_material, nota` | ver lista de arriba — es la tabla más leída de todo `tools/curador_registro/` | **Caso testigo de esta regla.** Columna `capa2_manifiesto`: `grep -rn "capa2" tools/ tests/` → **0 resultados**, verificado de nuevo en este acto. **105 de 197 filas** (`awk` sobre `capa3_disco_real=NO_REFERENCIADO`) están en ese estado, esperando que algo las conecte con `manifiesto.yaml`. Nada las conecta hoy. |

**El caso materializado que motivó A.7** (verificado en este acto, no es hipotético): `git show --stat 84f8e30` ("ACTO P·LOTE-1: WVS obtenido por el usuario, 11 archivos") tocó **únicamente** `data/manifiesto.yaml`, `data/manifiesto-staging.yaml`, `data/universo-puertas-2026-08-12.tsv` y una nota forense — **cero tablas de `data/curacion-universo/`**. Las 4 filas `ADESC-` que existen hoy en `activos-descubiertos-durante-ronda.tsv` (Dominio 3) vienen todas de `0e07179` (ENASIC/ENCUCI, 7/ago) — ninguna es de WVS. Un acto que hoy consulte la capa de activos por WVS no la encontrará ahí.

---

## Dominio 2 · Registrar una puerta o portal sondeado

18 tablas candidatas, todas confirmadas con `ls`. Ninguna tiene vía de escritura por script — las 18 son **A MANO**, con precedente de commit. La distinción real no es "vía" sino **vigente vs. snapshot muerto**, y **quién la lee**:

| tabla | estado | precedente (primer commit) | quién la lee |
|---|---|---|---|
| `universo-puertas-2026-08-12.tsv` | **VIGENTE** (8 commits, el último `bcd8a66` el 12/ago) | `772f09c` | **0** en `tools/`/`tests/` — solo prosa forense |
| `universo-puertas-2026-08-08.tsv` | snapshot muerto (1 commit, `977097c`) | `977097c` | 0 |
| `crosswalk-fuente-puerta-2026-08-13.tsv` | **VIGENTE** (2 commits, `563e928`→`bcd8a66`) | `563e928` | 0 |
| `universo-cota-2026-08-12.tsv` | snapshot único, "propuesta a mesa, no sellada" | `93a64b8` | 0 |
| `cola-adquisicion-2026-08-12.tsv` | snapshot único (54 fuentes `NO_REFERENCIADO`) | `cf6cd71` | 0 |
| `cola-aperturas-externas-2026-08-06.tsv` | snapshot muerto | `ef6ce0b` | 0 |
| `cola-ext-academico-2026-08-06.tsv` | snapshot muerto | `50a313b` | 0 |
| `cola-ext-civil-2026-08-06.tsv` | snapshot muerto | `a88a2b6` | 0 |
| `cola-ext-general-2026-08-06.tsv` | snapshot muerto | `8d2f66e` | 0 |
| `cola-ext-oficial-2026-08-06.tsv` | snapshot muerto | `a12927d` | 0 |
| `exploracion-puertas-2026-08-07.tsv` | snapshot muerto (EXPLORA-1) | `ddd3c3b` | 0 |
| `exploracion-puertas-2026-08-08.tsv` | snapshot muerto (EXPLORA-2, esquema con 2 campos más) | `8c882e4` | 0 |
| `mapa-fuentes-2026-08-06.tsv` | snapshot único, **con lector** | `2d53160` | `tests/indice.py:21` (ruta hardcodeada) |
| `mapa-fuentes-externas-consolidado-2026-08-06.tsv` | snapshot muerto | `ef6ce0b` | 0 |
| `mapa-ext-academico-2026-08-06.tsv` | snapshot único, **con lector** | `50a313b` | `tools/curador_registro/semantic_run.py:324` |
| `mapa-ext-civil-2026-08-06.tsv` | snapshot muerto (mismo prefijo que academico/general, sin lector) | `a88a2b6` | 0 |
| `mapa-ext-general-2026-08-06.tsv` | snapshot único, **con lector** | `8d2f66e` | `tools/curador_registro/semantic_run.py:324` |
| `mapa-ext-oficial-2026-08-06.tsv` | snapshot muerto (mismo prefijo que academico/general, sin lector) | `a12927d` | 0 |

**Trampas confirmadas de este dominio:**
1. **No hay nombre estable ni resolución dinámica.** `grep -rn "glob(" tools/ tests/` sobre estos prefijos → 0. Los dos lectores reales (`tests/indice.py:21`, `tools/curador_registro/semantic_run.py:324`) usan **rutas literales completas con fecha**. Si mañana aparece `mapa-ext-general-2026-08-20.tsv`, esos lectores seguirán leyendo la versión del 6/ago sin error ni aviso.
2. **`mapa-fuentes-2026-08-06.tsv` no está en la lista de chequeo de existencia** de `tests/indice.py` (línea 23 solo valida `IDX_5AGO, IDX_CANASTAS, MANIFIESTO, ALIAS`) — si faltara, el fallo sería un `FileNotFoundError` crudo, no el mensaje controlado que tienen los otros cuatro.
3. **Asimetría dentro de la propia familia `mapa-ext-*`**: `academico` y `general` tienen lector; `civil` y `oficial`, con el mismo prefijo y la misma fecha, no tienen ninguno.
4. **`crosswalk-fuente-puerta-2026-08-13.tsv`: la fecha del nombre no coincide con la fecha real.** Sus dos commits (`563e928`, `bcd8a66`) están fechados **12/ago**, no 13/ago — no hay rename (`git log --follow` da la misma lista). Quien busque "el crosswalk de hoy" por convención de nombre puede no encontrarlo bajo su fecha.
5. **`cola-adquisicion-2026-08-12.tsv` no es lo mismo que `decisiones-adquisicion.tsv` (Dominio 3)**, pese al vocabulario compartido — son dos mecanismos desconectados. Verificado: `grep -n "relaciones\|cola.adquisicion\|capa2" tools/curador_registro/decide_acquisition.py` → vacío. Uno opera sobre el universo T0 de activos; el otro es una cola derivada de `relaciones.tsv` en el dominio manifiesto/puerta.
6. **Cuando dos filas de `universo-puertas-2026-08-12.tsv` describen la misma fuente, manda la de `fecha_sondeo` más reciente cuyo `universo_declarado` cite un portal, no una tabla interna del programa.** Las 62 filas `gap_mapeo_map_b` (verificado en sesión, `13/ago`) declaran universo interno por construcción (MAP-B) y quedan superadas por cualquier sondeo de portal posterior — no se retiran solo por quedar superadas; retirarlas es acto propio (tipo MAP-B). Precedente: `ACTO SONDA-1` (PR #197) sondeó 15 de esas 62 fuentes contra portales reales (9 EXISTE-SATISFACE + 2 EXISTE-NO-SATISFACE + 4 NO-OBTENIDO, cifra autorreportada en su nota y en su propio mensaje de commit — no rederivada por fecha en este acto porque otras actos del mismo día también escriben filas con `fecha_sondeo` 12/13-ago y confunden un conteo por fecha); `ACTO P-LOTE-2` añadió 4 filas más de adquisición real el 13/ago para un subconjunto de esas 15.

---

## Dominio 3 · Registrar un activo descubierto y su decisión de adquisición

Ámbito: `data/curacion-universo/` (14 archivos, todos confirmados con `ls`). Motor: `tools/curador_registro/{snapshot_universe,inspect_assets,derive_recovered,decide_acquisition,validate}.py`.

| tabla | vía de escritura | contrato (campos clave) | quién la lee | trampa conocida |
|---|---|---|---|---|
| `activos-descubiertos-durante-ronda.tsv` | **A MANO, con precedente:** `0e07179` ("ENASIC·922 y ENCUCI·647 entran como activos T0, vía post-T0, sin regenerar snapshot"). `snapshot_universe.py` solo la inicializa vacía si no existe (líneas 677-683), nunca la reescribe. | `activo_descubierto_id, fecha, origen, localizador, estado, reserva` | `snapshot_universe.py`, `validate.py`, `tools/curador_registro/tests/test_barrido_completo.py` | **Es el escape hatch diseñado**: no participa de `core_componentes_sha256` ni de `hashes_outputs` del snapshot — por eso se puede editar a mano sin invalidar `snapshot_t0_sha256`, verificado en el propio commit `0e07179`. Hoy tiene 4 filas `ADESC-*`. |
| `decisiones-adquisicion.tsv` | `tools/curador_registro/decide_acquisition.py --universe <universo-declarado-t0.tsv> --discovered <activos-descubiertos-durante-ronda.tsv> --output <ruta>` | `decision_adquisicion_id, activo_id, familia_logica_id, accion, razon, beneficio_informativo, costo, riesgo, autoridad_requerida, criterio_parada, estado` | **0** en `tools/`/`tests/` — solo prosa forense | **Vía existe pero está desactualizada**, distinto de SIN VÍA: tiene 4 filas, ninguna corresponde a las 2 filas `ADESC-*` más recientes (`0e07179`); el script no se ha vuelto a correr desde el bootstrap `59d6c40`. |
| `estado-activos.tsv` | `inspect_assets.py --output-dir ...` (reescritura completa, línea 497) | `activo_id, objeto_logico_id, estado_descriptivo, adquirido, inspeccionable, tarea_observacion_id, reporte_inspeccion_ref, excepcion_inspeccion_ref, evidencia, reserva` | `validate.py`, `derive_recovered.py`, `inspect_assets.py`, `test_barrido_completo.py` | reescritura completa (no merge); un solo commit desde bootstrap (`59d6c40`). |
| `familias-activos.tsv` | `snapshot_universe.py` (línea 666, reescritura completa) | `activo_id, objeto_logico_id, familia_logica_id, tipo_relacion, evidencia_estructural, reserva` | `semantic_run.py`, `snapshot_universe.py`, `validate.py`, `test_barrido_completo.py` | su hash vive en `snapshot-t0.json`; regenerarla sola desincroniza el ancla. |
| `fuentes-t0.tsv` | `snapshot_universe.py` (línea 656) | `input_id, ruta, tipo, hash_input, parser, declaraciones_encontradas, declaraciones_parseadas, errores, reserva` | `snapshot_universe.py`, `validate.py` | ninguna adicional a la del grupo. |
| `snapshot-t0.json` | `snapshot_universe.py` (líneas 757-760, función `build_snapshot()`) | claves top-level: `conteos, core_componentes_sha256, corpus_root, effort_efectivo, hashes_outputs, modelo_efectivo, rotulacion_denominadores, routing_modelos_verificado, snapshot_t0_sha256, t0_congelado` | `integrate.py`, `semantic_run.py`, `snapshot_universe.py`, `validate.py`, `derive_recovered.py`, y 4 tests de `tools/curador_registro/tests/` | **`snapshot_t0_sha256` es un ancla frágil**: regenerarlo invalida expedientes ya sellados (`t0-89f4c3a49c00c0e1`, Dominio 4) — mecanismo verificado en `integrate.py:375` (`EXPEDIENTE_SNAPSHOT_OBSOLETO`) y documentado de primera mano en `0e07179`. |
| `universo-declarado-t0.tsv` | `snapshot_universe.py` (líneas 661-665) | `activo_id, fuente_programa, edicion_periodo, objeto_logico_id, objeto_logico, formato, url_localizador_principal, estado_adquisicion, ruta_local, hash_local, estado_inspeccion, reporte_inspeccion_ref, familia_logica_id, observaciones` | `integrate.py`, `snapshot_universe.py`, `validate.py`, `derive_recovered.py`, `decide_acquisition.py`, 3 tests | input `--universe` de `decide_acquisition.py`; si cambia sin re-correr ese script, el `scope_hash` de las decisiones existentes queda obsoleto. |
| `declaraciones-activos-t0.tsv` | `snapshot_universe.py` (líneas 657-660) | `declaracion_id, input_id, localizador_declarado, identificador_declarado, activo_id, metodo_reconciliacion, evidencia_reconciliacion, estado_reconciliacion` | `snapshot_universe.py`, `validate.py`, 2 tests | ninguna adicional. |
| `objetos-recuperados-t0.tsv` | `tools/curador_registro/derive_recovered.py --universe-dir --output [--ledger] [--corpus-root]` | `activo_id, objeto_logico_id, ruta_local, hash_local, tarea_observacion_id, reporte_inspeccion_ref, resultado_inspeccion, afirmaciones_emitidas, resultado_estructural, frontera_inspeccion, origen_recuperacion` | solo `tools/curador_registro/tests/test_t0_identity.py` | mismo script también valida/materializa `ledger-inspecciones-t0.tsv` en la misma corrida; docstring advierte que no reclasifica las 509 inspecciones vigentes como reutilizadas solo por existir. |
| `tablero-cobertura.json` | `validate.py --write-dashboard <ruta>` | claves: `baseline, coberturas, diagnosticos, errores, metrica_historica, ok, reservas, snapshot_t0_sha256` | `tools/curador_registro/tests/test_barrido_completo.py` (con fixture, no la tabla real) | es un **agregador de snapshot puntual** — lee casi todas las demás tablas de este dominio; si `decisiones-adquisicion.tsv` está stale, el tablero no lo refleja hasta la próxima corrida. |
| `candidatos-reconciliacion-activos.tsv` | `snapshot_universe.py` (líneas 669-672) | `candidato_reconciliacion_id, activos_implicados, declaraciones_implicadas, similitud_observada, razon_candidata, evidencia_pendiente, estado_revision` | `snapshot_universe.py`, `validate.py` | ninguna adicional. |
| `objetos-observados-no-representados.tsv` | `inspect_assets.py` (línea 501) — **siempre escribe lista vacía** | `objeto_observado_id, tarea_observacion_id, activo_id, objeto_logico_id, objeto_observado, reporte_inspeccion_ref, localizador, descripcion_literal, posible_necesidad, razon_inferencia` | `validate.py`, `inspect_assets.py`, `test_barrido_completo.py` | el mecanismo de detección existe en el contrato pero no está poblado por ninguna lógica activa hoy — 1 línea (solo cabecera). |

**Nueve de estos 14 archivos** (`estado-activos`, `familias-activos`, `fuentes-t0`, `snapshot-t0.json`, `universo-declarado-t0`, `declaraciones-activos-t0`, `objetos-recuperados-t0`, `tablero-cobertura.json`, `candidatos-reconciliacion-activos`) tienen **un único commit en toda su historia** (`59d6c40`) — ninguno se ha regenerado desde el bootstrap del pipeline.

### Dominio 3-bis · Cobertura material BARRIDO-2 *(FP-35, sellada por `ADR-108`, `ACTO B2-SEMANTICO`, 18/ago/2026)*

Ámbito: `data/curacion-universo/*barrido2*`. Motor: `tools/curador_registro/{barrido2_material,inspect_assets,write_barrido2_w0,write_barrido2_material,validate}.py`. Todo corre bajo `unshare -Urn`: el propio baseline declara `network_habilitada=false` y la validación lo exige.

| tabla | vía de escritura | contrato (campos clave) | quién la lee | trampa conocida |
|---|---|---|---|---|
| `ledger-inspecciones-barrido2.tsv` | `write_barrido2_material.py --output-root` | 21 campos; `representacion_id, payload_id, root_id, sha256, estado_e0, grado_inspeccion, objetos_e1, objetos_e2, excepciones, estado_terminal` | `integrate_barrido2.preflight`, `tareas_barrido2`, `cierre-28-barrido2.py` | su `reporte_neutral_ref` es el **lote** `E2B-*`, **no** el descriptor material; el descriptor `TASK-B2-*.json` se resuelve por `representacion_id`, no por esta columna |
| `reportes-inspeccion-barrido2-v1_0.tsv` | `write_barrido2_material.py` | 18 campos; una fila **por grupo** `(representacion, objeto_tipo, estado, privacidad, frontera)`, con un registro-muestra | `integrate_barrido2`, `build_cableado.py`, T23 | 2 717 filas resumen 1 833 802 objetos: `objeto_logico_id` es el objeto de la **muestra**, no un objeto compartido. La redacción destruye la cardinalidad en 496 filas |
| `baseline-material-barrido2.json` | `write_barrido2_material.py` | `base_sha, manifest_sha, e2_index_sha256, ledger_sha256, counts{13}, parsers, reports, network_habilitada=false` | `integrate_barrido2.preflight` (join de hash), `cierre-28-barrido2.py` | congelado por el gate del §15; **no se regenera** en la fase semántica |
| `prisma-material-barrido2.md` | `write_barrido2_material.py` / `write_barrido2_w0.py` | tabla Métrica/Cifra/Denominador/Comando | lectura humana | el comando declarado es el literal `CMD-MATERIAL`, no una línea ejecutable |
| `prisma-semantico-barrido2.md` | `data/curacion-universo/prisma-semantico-derivar.py --repo .` | dos tablas: PRISMA semántico y PRISMA de M-APERTURA absorbido | lectura humana | las «esperadas» son `destino=APERTURA-PENDIENTE` (17); las 2 de `PROPUESTA-A-COLA` llevan denominador propio |
| `muestra-adversarial-barrido2.tsv` | `data/curacion-universo/muestra-adversarial-derivar.py` + `-comparar.py` | muestra por ola, `max(3, ceil(5%))`, tope 20 | lectura humana | el veredicto 39/39 vive en prosa forense, no en la tabla |
| `cierre-28-barrido2.py` | **es script, no tabla** | imprime los 22 criterios del §28 con estado, evidencia y comando | lectura humana, cierre de acto | un criterio sin insumo sale `NO-VERIFICABLE`, nunca «cumple» |


---

## Dominio 4 · Producir una estimación (especificación → expediente → producción)

Ámbito: `data/curacion-registro/{especificaciones-produccion.json, expedientes-produccion/, produccion-modelo.tsv, necesidad-objeto-modelo.tsv, utilidad-modelo.tsv, trabajo-semantico.tsv, reglas-clasificacion-trabajo.json, ejecucion-semantica/}`.

**Secuencia de escritura (orden real, inferido de las firmas CLI):**
1. `prepare_production.py --config especificaciones-produccion.json --snapshot ... --baseline ... --output-root expedientes-produccion/t0-<hash>/` → escribe `especificacion-recibida.json` por expediente (versión cegada para el "analista": excluye campos `FORBIDDEN` como `supervisor_link`, `necesidad_id`, `decision_pendiente`, etc.).
2. `produce.py --spec <expediente>/especificacion-recibida.json --output-dir <expediente>/` → el "analista" escribe `resultado.tsv`, `resumen.json`, `hashes.json`, `analisis-reproducible.py`.
3. `integrate_production.py --config ... --snapshot ... --baseline ... --analyst-root ... --output produccion-modelo.tsv [--validate-existing]` → el "supervisor" **reproduce todo de forma independiente** (no confía en `hashes.json` del analista) y escribe la tabla final.
4. En paralelo: `classify_work.py --bootstrap --baseline --rules reglas-clasificacion-trabajo.json --output trabajo-semantico.tsv`.
5. Aguas abajo: `semantic_run.py --repo . [--output ejecucion-semantica] [--network]`.

| tabla | vía de escritura | contrato | quién la lee | trampa conocida |
|---|---|---|---|---|
| `especificaciones-produccion.json` | **SIN VÍA** (insumo maestro, A MANO, precedente `59d6c40`) | `{"specifications": [...]}` | `validate.py`, 2 tests de `tools/curador_registro/tests/`, y dinámicamente vía `--config` | campos `FORBIDDEN` explícitos que el analista no debe ver (ver arriba). |
| `expedientes-produccion/t0-89f4c3a49c00c0e1/` | `prepare_production.py` + `produce.py` (ver secuencia) | patrón un-directorio-por-corrida (`t0-<snapshot_sha256_prefijo>`), hoy solo uno, con 3 expedientes `ESP-OPACA-{A,B,C}` | `validate.py`, `test_produccion_correctiva.py`, `tests/check.py` | `tests/check.py` T02 excepta explícitamente este prefijo de la detección de duplicados por nombre — cada expediente reusa nombres genéricos (`resumen.json`, `hashes.json`) por diseño. |
| `produccion-modelo.tsv` | `integrate_production.py --output` (línea ~400) | 49 columnas — incluye `produccion_id, especificacion_id, estimando, estimacion, incertidumbre, poblacion, dominio, n, suma_pesos, hash_microdato, snapshot_t0_sha256, ..., estado_uso_modelo, requiere_decision` | `validate.py`, `integrate_production.py` (self-check `--validate-existing`), `test_produccion_correctiva.py`, `test_barrido_completo.py` | 11 filas hoy; el test exige que filas `CALCULO_REPRODUCIBLE` no tengan `NO_DETERMINADO` en `{n, suma_pesos, unidad, incertidumbre}`. |
| `necesidad-objeto-modelo.tsv` | **SIN VÍA** (A MANO, precedente único `59d6c40`) | `necesidad_id, objeto_modelo_origen, fuentes_verificacion, reserva` | solo `test_barrido_completo.py` (exige 37 filas, `N1..N33`) | 0 lectores fuera del test. |
| `utilidad-modelo.tsv` | **SIN VÍA** (A MANO, precedente `16180e6`, mismo commit que `relaciones.tsv`) | `relacion_id, necesidad_id, fuente_canonica_normalizada, objeto_evidencia_id_canonico, clasificacion_relacion, estado_productivo, uso_actual, evidencia_disponible, reserva, verificacion_requerida, requiere_decision, decision_id, siguiente_accion, evidencia_ref` | `semantic_run.py`, `bootstrap.py`, `validate.py`, `baseline.py`, `classify_work.py`, `test_semantic_run.py` | `baseline.py` valida que sea proyección 1:1 de `relaciones.tsv`. |
| `trabajo-semantico.tsv` | `classify_work.py --output` | `relacion_id, tipo_trabajo, siguiente_accion, ..., regla_clasificacion_id, reserva_clasificacion` (16 campos) | `semantic_run.py`, `validate.py`, `test_semantic_run.py` | ninguna adicional confirmada. |
| `reglas-clasificacion-trabajo.json` | **SIN VÍA** (A MANO, precedente único `59d6c40`) | `{"rules": [...]}` | solo `classify_work.py`, vía `--rules` (nombre no hardcodeado — 0 hits de grep literal, se consume dinámicamente) | búsqueda textual del nombre de archivo no encuentra su lector real. |
| `ejecucion-semantica/` | `semantic_run.py --repo --output [--network]` — `run_id` determinista (`stable_id("SEMRUN", seed)`) | `manifest.json` + `schemas/` (6 JSON schema) + `runs/<SEMRUN-id>/*` | `integrate.py`, `semantic_run.py` (se relee a sí mismo), `validate.py`, `test_semantic_run.py`, `tests/check.py` | **run huérfano confirmado**: `runs/` tiene 2 directorios (`SEMRUN-354ccb9d...` y `SEMRUN-1d73f40d...`), pero `manifest.json` declara como vigente solo el primero. `grep -rn "SEMRUN-1d73f40d5db91bcb0da9f3d2"` → 0 fuera de su propio contenido. `validate.py` sigue el `run_id` de `manifest.json` y nunca itera `runs/` para detectar huérfanos. |
| `data/curacion-registro/expedientes-produccion/evidencia-neutral-produccion.json` | **SIN VÍA** (A MANO, precedente único `59d6c40`) | `{"esquema": ..., "fuentes": [...]}` | 0 por grep literal; **sí se abre dinámicamente** vía `evidencia_neutral_ref` resuelto desde `especificaciones-produccion.json` (`prepare_production.py:74`, `integrate_production.py:176,64`) | una búsqueda textual ingenua del nombre de archivo no encuentra sus lectores reales — hay que seguir la indirección. |

### Dominio 4-bis · Semántica e integración BARRIDO-2 *(FP-35, sellada por `ADR-108`, `ACTO B2-SEMANTICO`, 18/ago/2026)*

Ámbito: `data/curacion-registro/ejecucion-semantica/barrido2/` y `data/cableado-universo-v1_0.tsv`. Motor: `tools/curador_registro/{tareas_barrido2,integrate,integrate_barrido2,build_cableado}.py`.

**Secuencia real (no se puede saltar un paso: cada uno verifica el anterior por hash):**
1. `tareas_barrido2.py fuentes` → `cobertura-fuentes-barrido2.tsv` (+ `-detalle`).
2. `tareas_barrido2.py paquetes --index <índice E2> --apertura <lista-apertura>` → fragmentos por payload y **ficha de lectura por relación**, ambos bajo `.barrido2/private/` (gitignored).
3. `tareas_barrido2.py tareas --elecciones <del curador>` → `tareas-semanticas-barrido2.tsv`.
4. `tareas_barrido2.py propuestas --veredictos <del supervisor>` → `propuestas-barrido2.tsv`.
5. `integrate.py --barrido2 ... [--apply]` → `decisiones-integracion-barrido2.tsv`, `journal-…json`, `integracion-validada-…json`.
6. `build_cableado.py` → `data/cableado-universo-v1_0.tsv`; lo juzga `tests/check.py --require-cableado` (T23).

| tabla | vía de escritura | contrato (campos clave) | quién la lee | trampa conocida |
|---|---|---|---|---|
| `cobertura-fuentes-barrido2.tsv` (+ `-detalle`) | `tareas_barrido2.py fuentes --output` | 10 campos; `fuente_canonica, regla_resolucion, payloads_n, evidencia_resolucion, estado_cobertura` | `tareas_barrido2.py paquetes`/`tareas` | la cascada de reglas era de **primer match** y ocultaba la segunda entrada de programa; desde `ADR-108` la regla es **unión R1 ∪ R7** y `regla_resolucion` puede traer dos nombres unidos por `+` |
| `tareas-semanticas-barrido2.tsv` | `tareas_barrido2.py tareas` | `TASK_FIELDS`, 20 campos | `integrate_barrido2.preflight`, `build_cableado.py`, T23 | `material_tarea_id` ≠ `tarea_id`: el primero nombra el descriptor material, y dos relaciones pueden apoyarse en la misma representación |
| `propuestas-barrido2.tsv` | `tareas_barrido2.py propuestas` | `PROPOSAL_FIELDS`, **22 campos del §17**, orden exacto | `integrate_barrido2.preflight` (compara la lista completa), T23 | `decision_mesa_id` sólo admite `FP-24` o `NO-APLICA`: un valor como `FP-24/ADR-93` revienta schema, preflight y T23 a la vez. La cita del ADR va en `razon_gate` |
| `decisiones-integracion-barrido2.tsv` | `integrate.py --barrido2 --output-dir` | `PROPOSAL_FIELDS` + `estado_integracion, razon_integracion, journal_id` (25) | T23 (condición 14), `build_cableado.py` | el estado se decide **por relación**, no por propuesta: basta una `dependencia_fp24=SI` o un veredicto discordante para que toda la relación cambie de estado |
| `journal-integracion-barrido2.json` | `integrate.py --barrido2` | hashes anterior/nuevo de los 10 archivos del registro | rollback, auditoría | sin `--apply` se escribe el journal pero **no** se toca el registro |
| `data/cableado-universo-v1_0.tsv` | `build_cableado.py --output` | **26 columnas del §21**, orden exacto, cero celdas vacías | `tests/check.py` T23 | el ensamblador mantiene su **propia** copia de la cabecera, separada de la de `check.py`, para que un error no se valide a sí mismo; `test_build_cableado.py` compara ambas |

**Quién lo sella:** `ADR-108` (`ACTO B2-SEMANTICO`, `PR #268`). Es la respuesta a `FP-35`, que pedía decidir «qué dominios del índice ganan las tablas nuevas de BARRIDO-2 y quién lo sella» **después de observar los mecanismos reales** — condición que sólo se cumplió al correrlos de punta a punta en este acto.


---

## Dominio 5 · Registrar una celda-D del piloto

`data/curacion-registro/celdas-d/` — hoy **2 archivos**: `G5.familismo_obligacion.actitud.yaml`, `G5.radio_confianza.encuci_vs_enbiare.yaml`. El propio validador documenta que el piloto va a escribir 10-15 más.

- **Vía de escritura:** A MANO, con precedente — 5 commits tocan el directorio (`6fdccb5` semilla `radio_confianza`, `c4639bd`, `9a0f1b7`, `24e7a80`, `8565c17` el más reciente, `familismo_obligacion.actitud`). **SIN VÍA de script**: `grep -rln "celdas-d\|celdas_d" tools/ tests/` → único hit `tests/test_celdas_d.py`, que es exclusivamente lector/validador (`yaml.safe_load`, ningún `open(..., "w")`).
- **Contrato:** 24 claves top-level bajo `celda_d:`, consistentes entre los 2 archivos: `id, estimando, tipo_adjudicacion, dominio, poblacion_objetivo, unidad_objetivo, universo_candidatos, candidatos, criterio_adjudicacion, momentos_holdout_refs, champion_actual, output_nativo, incertidumbre, supuesto_transporte, fuerza_coeficiente, procedencia_condicional, vocabulario_version, calibrado, estado_operativo, requiere_decision_mesa, fecha_declaracion, commit_declaracion, fecha_adjudicacion, commit_adjudicacion, relacion_complemento`. Nombre de archivo = `<celda_d.id>.yaml`.
- **Quién la lee:** `tests/test_celdas_d.py` (único).
- **Trampa conocida — la más quisquillosa del índice.** `tests/test_celdas_d.py` exige, entre otras cosas: 23 de las 24 claves top-level obligatorias (`vocabulario_version` es la única opcional); 9 subcampos obligatorios por candidato; 7 enums cerrados (`tipo_adjudicacion`, `dominio`, `unidad_objetivo`, `estado_operativo`, `rol`, `diseno_datos`, `estrategia`); prohibición explícita de que `fuente(s)`/`diseno(_datos)` vivan al nivel `celda_d` (solo dentro de `candidatos`); y la regla condicional más filosa: si `rol == "COMPLEMENTO"`, `resultado` debe ser **exactamente** `"NO-APLICA"`. El contrato formal en prosa vive en la serie de documentos propuesta-motor-adaptativo-celda, versiones 0.1 a 0.4 (vigente: `propuesta-motor-adaptativo-celda-v0_4.md`) — no hay JSON Schema separado, el validador es el esquema ejecutable de facto.

---

## Dominio 6 · Adjudicar un veredicto del Hito D

`forense/hitoD-*` — 9 archivos: 1 preregistro (`hitoD-preregistro-v2_0.md`, 1071 líneas), 2 especificaciones, 5 veredictos, 1 revisión. Patrón: `hitoD-R<N>_<M>-<tipo>-v<X>_<Y>.md`.

- **Vía de escritura:** A MANO — los 9 archivos comparten el mismo y único commit `b72980c` (merge de PR #135) en su `git log`; no hay script que los escriba (`tests/hitoD_r7_2_ocho_olas.py` solo los **cita** en docstring/prints, su único `open(` real es sobre un ZIP de microdato ENVIPE).
- **Contrato:** cabecera tipo tabla equivalente al ADR-36 de canon — `ARCHIVO / REEMPLAZA A / VERIFICAS ASÍ / NOMBRE ESTABLE` — replicada en los 6 documentos de veredicto/revisión/preregistro.
- **Quién la lee/valida:** `tests/check.py` (T17, T18, T19c, T20), `canon/{gobernanza-v1_15,estado-programa-v1_10,modelo-decision-v4_0}.md`.
- **Trampa conocida — la adjudicación NO es escribir el archivo.** Dos de los veredictos (`R1_3`, `R3_1`) se autodeclaran explícitamente "propuesta, no adjudicada". La fuente única y canónica del conteo/adjudicación es el bloque append-only `## Registro de veredictos archivados` al final de `hitoD-preregistro-v2_0.md` (línea 1054) — solo cuenta la forma exacta `` `RX.Y` → veredicto `Z` `` **dentro** de ese bloque (verificado: 15 líneas con esa forma en todo el archivo, 13 reglas distintas archivadas tras deduplicar `R4.3` mitad A/B — coincide con "13 de 27" citado en `canon/estado-programa-v1_10.md`). Escribir/editar un `hitoD-R<N>-veredicto-*.md` individual no basta: falta el ADR de mesa (`canon/gobernanza-v1_15.md`) y la línea nueva en ese bloque append-only.

---

## Dominio 7 · Sellar una decisión de gobierno (ADR + cascada)

`canon/gobernanza-v1_15.md` §4 ("Registro de decisiones") — 71 ADR hoy, todos dentro de una sección madre única (no hay `## ADR-N` por entrada).

- **Vía de escritura:** A MANO, exclusivamente — `grep -rln "canon/gobernanza\|canon/estado-programa" tools/ tests/` no encuentra ningún escritor; `tests/check.py` solo lee. Formato de cada entrada: `**ADR-N · <decisión en una frase>.** Decisión de mesa del autor, <fecha>, sobre <fuente/encargo>. ... → **Vigente.**`, cerrando con bloque de metadata en cursiva (perímetro declarado: qué archivos SÍ se tocaron y cuáles NO).
- **Numeración:** estrictamente secuencial sin huecos, validada por T15 (regex `^\*\*ADR-(\d+)`, `tests/check.py:482-507`). Episodio real de colisión: ADR-71 tuvo que renumerarse dos veces (71→70→71) porque otro PR selló un ADR con el mismo número mientras esta rama corría.
- **Cascada real (verificada en ADR-59 y ADR-60):** como mínimo, el ADR mismo + cabecera de conteo en `canon/gobernanza-v1_15.md` (línea 2) y el contador en `canon/estado-programa-v1_10.md` (líneas 27, 99). Si el ADR toca reglas/tiers del motor, también `canon/modelo-decision-v4_0.md`. `canon/protocolo-sesion-v1_0.md` **no** participa nunca de la cascada de ADR (0 apariciones en `grep "cascada"`).
- **Quién la lee/valida:** `tests/check.py` T13 (cabecera ADR-36), T15 (secuencia de ADR), T16 (cifra de suite vigente vs. real).
- **Trampa conocida — confirmada con la propia corrida de este acto.** T16 hoy reporta 4 divergencias: `canon/estado-programa-v1_10.md:130,222` declara "101 WARN"/"18 FAIL·101 WARN" vigente; `canon/gobernanza-v1_15.md:760,852` declara "18 FAIL·95 WARN" — la corrida real (verificada en el PASO 1 de este acto) da **18 FAIL · 104 WARN**. Las cifras ni siquiera coinciden entre los dos archivos que deberían ir sincronizados por cascada. Ya está congelada como deuda conocida en `tests/baseline.json` (por eso `--baseline` da VERDE), pero **cualquier ADR nuevo que no recalcule y actualice esa cifra en ambos archivos arriesga sumar una 5ª línea NO congelada, que sí rompe `python3 tests/check.py --baseline`.**

---

## Dominio 8 · Registrar un hallazgo o una nota de acto

- **`forense/hallazgos.md`** — append-only, **una línea por hallazgo** (`- **AAAA-MM-DD** · texto libre...`), sin campos/ID/estado/ADR estructurados (la convención lo dice explícitamente en su propia cabecera, regla de R0/ADR-48). **Vía:** A MANO en cada commit — `grep -rl "hallazgos.md" tools/ tests/` solo encuentra citas en comentarios (`tests/manifiesto.py`, `tests/baseline.json`), ningún escritor de código. **Quién la lee:** nadie programáticamente — es para humanos/futuros actos, citado en comentarios para trazabilidad.
- **`forense/notas/`** — 150 archivos, convención `AAAA-MM-DD-<código-de-acto>-<tema>.md` (sin autor en el nombre). Única excepción: `_p3_lca/` es un subdirectorio técnico de checkpoints de pipeline (`tests/p3_lca_{run,stage}.py`), no una nota narrativa.
- **`forense/encargos/convencion.md`** — fuente de verdad para archivar encargos (no notas ni hallazgos): cabecera obligatoria **SHA de redacción / Entorno asignado / Estado (`VIVO`/`CONSUMIDO`)**; texto completo pegado inline, nunca solo un enlace o resumen; un encargo consumido nunca se borra.
- **Trampa conocida — confirmada en `.gitattributes`.** `forense/hallazgos.md` y `forense/bitacora.md` llevan `merge=union` (driver interno de Git, verificado empíricamente dos veces, 5/ago y 12/ago). **El botón "Merge pull request" de GitHub NO lo honra del lado servidor** — dos PRs reales (#175, #179) mostraron conflicto falso en la interfaz mientras el mismo merge resolvía limpio en clon local. Única vía garantizada: `git merge` local, main hacia la rama. **Nunca resolver en el editor web de conflictos** — ahí es donde se borra la entrada ajena. (`hitoD-preregistro-v2_0.md` es append-only pero **no** lleva `merge=union`, a propósito: duplicaría silenciosamente veredictos archivados en vez de conflictuar — se fusiona a mano.)

---

## Si tu encargo hace X, escribe en Y

| Si tu encargo... | Escribe en... |
|---|---|
| **acabo de bajar un archivo** | `data/manifiesto.yaml` (`tests/manifiesto.py --registra`/`--promueve`) **+** si el objeto pertenece al universo T0, `activos-descubiertos-durante-ronda.tsv` (a mano, sin regenerar snapshot) **+** `decisiones-adquisicion.tsv` (`decide_acquisition.py` — verifica primero si sigue corriéndose; hoy está stale) **+** fila en `universo-puertas-2026-08-12.tsv` (a mano). Si la fuente entra por manifiesto/portal y **no** por el universo T0 (como WVS), la capa de activos puede quedar sin tocar — decide cuál de los dos mundos aplica, no asumas que uno cubre al otro. |
| **sondeé un portal, no descargué nada** | fila en `data/universo-puertas-2026-08-12.tsv` (VIGENTE — no en `-08-08`, que es snapshot muerto). Si es fuente externa fuera de INEGI, evalúa `cola-adquisicion-2026-08-12.tsv` o si ya hay continuación más reciente de los `mapa-ext-*`/`cola-ext-*` (hoy todos congelados). |
| **voy a estimar algo** | especificación en `especificaciones-produccion.json` → expediente vía `prepare_production.py` → resultado del "analista" vía `produce.py` → `produccion-modelo.tsv` vía `integrate_production.py` (nunca el mismo acto hace de analista y supervisor). |
| **voy a registrar una celda-D** | archivo nuevo `data/curacion-registro/celdas-d/<celda_d.id>.yaml`, a mano, y corre `tests/test_celdas_d.py` antes de darla por buena — 23 claves, 7 enums cerrados, regla `COMPLEMENTO→"NO-APLICA"`. |
| **voy a adjudicar un veredicto del Hito D** | no basta con `hitoD-R<N>-veredicto-*.md` (puede quedar "propuesta, no adjudicada"). Necesitas (1) un ADR de mesa en `canon/gobernanza-v1_15.md` y (2) una línea nueva en el bloque append-only `## Registro de veredictos archivados` de `hitoD-preregistro-v2_0.md`, con el contador de `canon/estado-programa-v1_10.md` actualizado a juego. |
| **voy a sellar una decisión de gobierno** | entrada `**ADR-N · ...**` en `canon/gobernanza-v1_15.md` §4 (numeración secuencial, sin huecos) + cascada declarada explícita: como mínimo cabecera de conteo de `gobernanza-v1_15.md` y contador de `canon/estado-programa-v1_10.md`; si toca reglas/tiers, también `canon/modelo-decision-v4_0.md`. Recalcula y actualiza la cifra `N FAIL · M WARN` vigente en ambos archivos si cambió. |
| **encontré un defecto que no impide medir** | una línea en `forense/hallazgos.md` (merge local siempre, nunca botón/editor web de GitHub). |
| **encontré un defecto que sí impide medir** | para, y repórtalo — no se registra como hallazgo suelto, se detiene el acto. |
| **necesito una nota extendida de lo que hizo mi acto** | `forense/notas/AAAA-MM-DD-<código-de-acto>-<tema>.md`. |
| **lancé un encargo** | cópialo literal, con cabecera SHA/Entorno/Estado, en `forense/encargos/` — antes o junto con su lanzamiento (`forense/encargos/convencion.md`). |
| **quiero saber si mi fuente "está referenciada"** | `data/curacion-registro/relaciones.tsv`, columna `capa2_manifiesto` — pero hoy **nada la escribe** (SIN VÍA, 105 filas `NO_REFERENCIADO`). No inventes una vía: repórtalo como hueco. |

---

## Colas de trabajo (no son defectos de este acto)

**Tablas/columnas `SIN VÍA` de escritura por script, confirmadas con `grep`/`ls`:**
- `data/curacion-registro/relaciones.tsv` (bulk-cargada una vez, `16180e6`; ningún script la reescribe) — y, dentro de ella, la columna **`capa2_manifiesto`** es el caso testigo citado por el propio encargo que abrió este índice: `grep -rn "capa2" tools/ tests/` → 0, **105 filas `NO_REFERENCIADO`**.
- `data/curacion-registro/utilidad-modelo.tsv` (mismo patrón, precedente `16180e6`).
- `data/curacion-registro/necesidad-objeto-modelo.tsv` (precedente único `59d6c40`).
- `data/curacion-registro/reglas-clasificacion-trabajo.json` (precedente único `59d6c40`).
- `data/curacion-registro/especificaciones-produccion.json` (precedente único `59d6c40`).
- `data/curacion-registro/expedientes-produccion/evidencia-neutral-produccion.json` (precedente único `59d6c40`).

**Vía existe pero no se ha vuelto a correr (distinto de SIN VÍA):**
- `data/curacion-universo/decisiones-adquisicion.tsv` — `decide_acquisition.py` funciona; le faltan las 2 decisiones más recientes.
- `data/curacion-registro/ejecucion-semantica/runs/SEMRUN-1d73f40d5db91bcb0da9f3d2` — run huérfano, no referenciado desde `manifest.json` ni desde ningún otro archivo del repo.

**Tablas que nadie lee en `tools/`/`tests/` (confirmado con `grep -rl`, 0 resultados):**
`universo-puertas-2026-08-12.tsv` (la vigente) · `universo-puertas-2026-08-08.tsv` · `universo-cota-2026-08-12.tsv` · `cola-adquisicion-2026-08-12.tsv` · `cola-aperturas-externas-2026-08-06.tsv` · `cola-ext-{academico,civil,general,oficial}-2026-08-06.tsv` · `exploracion-puertas-2026-08-07.tsv` · `exploracion-puertas-2026-08-08.tsv` · `mapa-fuentes-externas-consolidado-2026-08-06.tsv` · `mapa-ext-civil-2026-08-06.tsv` · `mapa-ext-oficial-2026-08-06.tsv` · `crosswalk-fuente-puerta-2026-08-13.tsv` · `data/curacion-universo/decisiones-adquisicion.tsv` · `data/curacion-universo/objetos-recuperados-t0.tsv` (solo un test) · `data/curacion-registro/necesidad-objeto-modelo.tsv` (solo un test) · `forense/hallazgos.md` y `forense/notas/*.md` (por diseño — son para humanos, no es un defecto).

---

## Cierre

**Base:** `origin/main = 2b13e88`, confirmado por `git log -1` al escribir. **Entorno:** NUBE, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (firma correcta sin sonda de red, ADR-59(b)) — este acto no tocó microdato ni red. **`data/raw`:** ausente, como se espera en un clon fresco; este acto no descargó nada, no se creó ni se enlazó.

```
$ python3 tests/check.py --baseline
────────────────────────────────────────────────────────────────────────
  22 FAIL · 104 WARN
────────────────────────────────────────────────────────────────────────
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e7cd99da7ae1d776a499f9d5009c061b1be73770)
```

**Contadores de medición movidos: 0.** Este acto no midió nada sobre México — documentó la maquinaria.

**Lo que este acto NO hizo:** no creó ninguna vía faltante (las nombró); no modificó ninguna tabla; no corrigió el registro incompleto de WVS (queda para ACTO R″); no añadió tests; no selló ningún ADR — si mesa quiere canonizar A.7, es acto propio y de una línea.

**Nota fuera de perímetro, para quien selle A.7.** El texto de A.7 (Parte 1 del encargo que abrió este acto) se numeró a sí mismo `A.7`, pero `instrucciones-proyecto-v2_6.md` **ya tiene un A.7** vigente ("La identidad de un artefacto es su contenido, no su envoltura", línea 265) — el nuevo texto se pega después de A.6 (línea 251, antes del A.7 existente), lo que implica renumerar el A.7 actual a A.8 (y arrastrar su corolario). Esto no bloqueó este acto porque `instrucciones-proyecto-v2_6.md` está fuera de su perímetro — solo se reporta aquí para que el acto que canonice A.7 no colisione con el mismo patrón que ADR-71 ya mostró con la numeración de ADR.

**PR:** `infra/indice-v1` — **NO FUSIONAR sin mesa.**
