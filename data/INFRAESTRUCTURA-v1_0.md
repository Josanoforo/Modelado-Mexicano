# Índice de infraestructura interna del registro — v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `INFRAESTRUCTURA-v1_0.md` |
> | **REEMPLAZA A** | Nada — creación. Antes de este acto no existía ningún índice de infraestructura (verificado: `data/` solo tenía `UNIVERSO-MINIMO-FUENTE-v1_0.md` y `catalogo-fuentes-v2_0.md`, ninguno describe la maquinaria interna). |
> | **VERIFICAS ASÍ** | `grep -c "^## Dominio" data/INFRAESTRUCTURA-v1_0.md` da **9** (los ocho dominios originales del PASO 2 del encargo que lo construyó, más el Dominio 9 añadido por `ACTO MAESTRA31-E2`, 26/ago/2026, regla de conducto `ADR-70(c)`). No hay ADR que lo selle todavía — mesa decide si lo canoniza. |
> | **NOMBRE ESTABLE** | **`infraestructura-v1`** — cítalo así, nunca por nombre de archivo |

**Qué es.** El análogo hacia adentro de `UNIVERSO-MINIMO-FUENTE-v1_0.md`: en vez de "qué sitios recorrer antes de declarar `NO-ENCONTRADO`", esto es "qué tablas gobiernan cada dominio de escritura antes de que un encargo invente una vía". Por cada dominio de trabajo (adquirir, sondear, producir, adjudicar, sellar, registrar), lista las tablas verificadas con `ls`, su vía de escritura verificada con `grep`/`git log`, su contrato de campos verificado con `head -1`, y quién la lee verificado con `grep -rl`. Existe porque A.7 (`instrucciones-proyecto`, pendiente de canonizar) lo exige: *ningún encargo manda escribir en una tabla sin derivar antes qué tablas gobiernan ese dominio*.

**Qué no es.** No es documentación de negocio ni un tutorial del pipeline — para eso están los docstrings de cada script y las notas forenses citadas. No mide nada sobre México (contadores de medición movidos por este acto: **0**). No corrige ningún registro incompleto que encuentre — los reporta como hueco (ver `Colas de trabajo`, abajo). No crea ninguna vía faltante. No es exhaustivo a nivel de fila — es exhaustivo a nivel de tabla/mecanismo.

**Procedencia y vigencia.** Construido el 13/ago/2026, en un acto de **NUBE**, contra `origin/main = 2b13e88`. Describe el estado de la maquinaria **en ese commit**. ACTO W, R″ y V2 podían estar corriendo en paralelo y tocan tablas que este índice documenta — eso no es conflicto (este acto no escribe ninguna tabla), pero significa que una tabla puede tener una fila más de las que este índice vio verificar. Cuando un acto futuro descubra que el índice está desactualizado, se corrige el índice (regla de conducto, ADR-70(c)) — no hay barrido periódico programado.

---

## Dominio 1 · Adquirir una fuente / registrar un payload descargado

| tabla | vía de escritura | contrato (cabecera real) | quién la lee | trampa conocida |
|---|---|---|---|---|
| `data/manifiesto.yaml` | `tests/manifiesto.py --registra` (una entrada) o `--promueve` (mueve candidatos ya escaneados desde staging) — función `escribir_manifiesto` | YAML, lista de entradas: `archivo, raiz, sha256, tamano_bytes, fecha_descarga, entorno_descarga, descargado_por, url_origen, url_origen_sugerida, usado_para` | `tools/curador_registro/semantic_run.py`, `tests/{cal_enoe_fasea,dedup,manifiesto,calx_g3,indice,corpus,cruce_operables,idx_g3}.py` | Bug de mecanismo, documentado en el propio commit `84f8e30`, **dos partes, hoy con distinto estado**: (i) `--escanea` plegaba mal escalares YAML >80 caracteres (sangría de continuación de dos espacios, la misma que la clave) al escribir vía el escritor de staging — **REPARADO por `ADR-310`** (`ACTO MAESTRA36-A1`, 2/sep/2026): `_yaml_valor` pasa `width=10**9`. Antes del arreglo el staging salía corrupto **sin fallar** y reventaba después en `--promueve` con `ScannerError`, y no se curaba solo, porque `--escanea` lee el staging previo y también reventaba: había que restaurarlo a mano. El manifiesto nunca estuvo expuesto (`escribir_manifiesto` usa `yaml.dump` sobre la estructura entera). (ii) no acumula asignaciones de `--grupo` entre invocaciones separadas del mismo escaneo — **sigue sin reparar**: se evita corriendo un `--escanea` + `--promueve` por grupo, que es lo que hizo `MAESTRA36-A1` con sus siete pases. |
| `data/manifiesto-staging.yaml` | `tests/manifiesto.py --escanea <RAIZ>` (constante `STAGING_NOMBRE`) — **recursivo, `archivo` = ruta relativa a la raíz, con subcarpeta si la hay (desde `ADR-310`)**; antes era `os.listdir` y una subcarpeta entera quedaba invisible. Misma convención que `tests/corpus.py`, que es la que ya tenían las 49 entradas `Descargas Manuales/…` desde la corrección T2 del 18/ago/2026: hasta `ADR-310` los dos recorridos del proyecto no miraban el mismo árbol. `--grupo` aplica `fnmatch` sobre esa ruta relativa, no sobre el basename. | mismo esquema que `manifiesto.yaml` | `tests/manifiesto.py`, `tests/test_manifiesto_alcance.py` | el bug de plegado de arriba le pegaba directo (es su escritor primario); reparado por `ADR-310`. Trampa viva: `--escanea` **reescribe** las entradas de la raíz que escanea, así que asignar `--url`/`--usado-para` a varios grupos exige `--escanea`+`--promueve` por grupo, no varios `--escanea` seguidos. |
| `data/curacion-registro/relaciones.tsv` | **VÍA DOCUMENTADA, no script** — `tools/curador_registro/GUIA-CURADOR-REGISTRO.md` §«alta de fuente nueva en tres tablas» fija el procedimiento y la derivación de `relacion_id`/`OE-`/`PROV-`, porque las tres invariantes de `baseline.py` están acopladas y una fila suelta las rompe todas (`FP-230`, ejecutada por `ACTO MAESTRA34-N6 · CURADOR-Y-SUITE`, 1/sep/2026). Antes decía «SIN VÍA de script»; sigue sin haber script que la escriba, pero ya no sin vía. Bulk-cargado una sola vez (`16180e6`, "incorpora baseline semántico N1-N33"). Todo lo demás en `tools/curador_registro/` solo lo **lee** (`baseline.py`, `bootstrap.py`, `classify_work.py`, `derive_queue.py`, `integrate.py`, `integrate_production.py`, `semantic_run.py`, `validate.py`) — ninguno tiene un `write_tsv(..., "relaciones.tsv", ...)`. | 19 campos: `relacion_id, necesidad_id, fuente_canonica_normalizada, objeto_evidencia_id_canonico, fuente_nombre, tipo_fuente, id_manifiesto, sha256_fuente, capa1_universo_indexado, capa2_manifiesto, capa3_disco_real, capa4_apertura_mapeo, clasificacion_relacion, reason_code, evidencia_ref, evidencia_textual_breve, confianza, conflicto_material, nota` | ver lista de arriba — es la tabla más leída de todo `tools/curador_registro/` | **Caso testigo de esta regla.** Columna `capa2_manifiesto`: `grep -rn "capa2" tools/ tests/` → **0 resultados**, verificado de nuevo en este acto. **105 de 197 filas** (`awk` sobre `capa3_disco_real=NO_REFERENCIADO`) están en ese estado, esperando que algo las conecte con `manifiesto.yaml`. Nada las conecta hoy. |
| `data/curacion-registro/cola-adquisicion-registro.tsv` | `tools/curador_registro/registra_cola_adquisicion.py --cola data/cola-adquisicion-v1_0.tsv --aliases data/curacion-registro/aliases-fuentes.tsv --output <ruta>` (`ACTO MAESTRA33-A5`, 1/sep/2026, P2) | 10 campos: `fila_origen, fuente_canonica, fuente_canonica_normalizada, discordancia_alias, estado_A4A5, prioridad, url_conocida, ids_manifiesto, origen, nota` | `tools/vista_cola_adquisicion.py`, `tests/check.py` (T26) | **Es el hogar nuevo** para las cinco columnas de la cola que no tenían tabla del registro antes de este acto (`estado_A4A5, prioridad, url_conocida, origen, nota` — ver `data/curacion-registro/MAPA-COLA-ADQUISICION-v1_0.md`, P1). `fuente_canonica_normalizada` resuelve contra `aliases-fuentes.tsv`; hoy 0/79 filas tienen alias (`discordancia_alias=SIN_ALIAS`), declarado, no forzado. |

**El caso materializado que motivó A.7** (verificado en este acto, no es hipotético): `git show --stat 84f8e30` ("ACTO P·LOTE-1: WVS obtenido por el usuario, 11 archivos") tocó **únicamente** `data/manifiesto.yaml`, `data/manifiesto-staging.yaml`, `data/universo-puertas-2026-08-12.tsv` y una nota forense — **cero tablas de `data/curacion-universo/`**. Las 4 filas `ADESC-` que existen hoy en `activos-descubiertos-durante-ronda.tsv` (Dominio 3) vienen todas de `0e07179` (ENASIC/ENCUCI, 7/ago) — ninguna es de WVS. Un acto que hoy consulte la capa de activos por WVS no la encontrará ahí.

**`/adquiere`, la vista y `PAQUETE-RECETAS`** (`ADR-70(c)`, regla de conducto, registrado por `ACTO MAESTRA33-A5 · RECONCILIA-ADQUISICION-CON-CURADOR`, 1/sep/2026): `.claude/commands/adquiere.md` camina `data/cola-adquisicion-v1_0.tsv` por prioridad y actualiza sus filas; desde este acto esa tabla es una **VISTA**, no una fuente — se regenera con `python3 tools/vista_cola_adquisicion.py` a partir de `data/curacion-registro/cola-adquisicion-registro.tsv` (cabecera `# GENERADO — no editar`), y `tests/check.py::T26` falla si difieren. `PAQUETE-RECETAS-<fecha>.md` (mandato de `/adquiere` §7.2) es el artefacto de recetas de navegador ≤1 minuto para filas `NO-OBTENIDO`/`NO-ACCESIBLE`: ya materializado una vez (`forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md`, `ACTO MAESTRA33-A3`) — corrección de premisa de este acto (P2 lo daba por citable como evidencia sin haber verificado su existencia real; `find . -iname "*PAQUETE-RECETAS*"`, con comodín inicial, sí lo encuentra). Sus recetas se citan como evidencia en `cola-adquisicion-registro.tsv` (columna `nota`) para las filas que aplique, no se reinventa una tabla aparte. **Riesgo declarado, no resuelto en este acto** (fuera de perímetro): `tools/arbitra.py:83-91` (`encola_no_obtenido`) apendiza líneas de 4 columnas directamente a `data/cola-adquisicion-v1_0.tsv` fuera de la vía del registro — una corrida de `/arbitra` entre dos regeneraciones de la vista perdería esa fila apendizada en el próximo `tools/vista_cola_adquisicion.py`. Sucesor: migrar `arbitra.py` a escribir contra `cola-adquisicion-registro.tsv` antes de que la vista se regenere de rutina.

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

## Dominio 9 · Registrar una decisión de mesa pendiente / un traspaso entre sesiones

*Añadido por `ACTO MAESTRA31-E2` (26/ago/2026, ADR a re-derivar en el cierre), regla de conducto `ADR-70(c)`: este acto descubrió por comando (`grep -c`, cero aciertos, ver nota de cierre) que las tres tablas de abajo gobiernan escritura real y ninguna estaba indexada. No es barrido del índice — solo estas tres.*

| tabla | vía de escritura | contrato (cabecera real) | quién la lee | trampa conocida |
|---|---|---|---|---|
| `forense/firmas-pendientes.tsv` | **A MANO** — ninguna tabla de `tools/`/`tests/` la escribe (`grep -rn "firmas-pendientes" tools/ tests/` → 0); cada acto abre/cierra fila directamente en el TSV | 9 campos: `id, qué_se_firma, dónde, creado, gatea, estado, firmada_en, ejecutada_en, encargo` — `id` es secuencial `FP-NN` sin huecos, `estado` ∈ `{ABIERTA, FIRMADA}` | cada encargo que necesita saber si una decisión de mesa ya está resuelta antes de tratarla como pendiente (patrón repetido: tratar como abierta una fila que ya cerró) | **167 filas en `main` al momento de este acto** (verificado `wc -l`); una fila `FIRMADA` con cita de mesa verbatim en la columna `firmada_en` puede seguir pareciendo abierta si solo se lee el resumen de un encargo anterior y no la fila misma — verifica siempre la fila completa, no una referencia de segunda mano. |
| `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv` | **A MANO** — sin vía de script confirmada (`grep -rn "cruce-oferta-demanda" tools/ tests/` → 0 escritores); nace y se edita por acto de curación directo | 14 campos: `demanda_id, parametro_motor, tipo, que_convierte, fuente, instrumento_ola, reactivo, veredicto_A4, que_le_falta, palanca, rank, archivos_examinados, control_positivo, estado_fetch, revisado_en` | actos de cruce oferta↔demanda y el reloj del falsador del 8/sep (`forense/notas/2026-08-25-cruce-oferta-demanda.md`); `forense/firmas-pendientes.tsv` la cita como evidencia (p.ej. `FP-169`) | columna `veredicto_A4` es el campo de conteo A.13 real — un `grep` aislado sobre el archivo sin leer esta columna con lector de TSV de 14 campos puede contar mal (mismo modo de falla que `FP-118` en `ADR-141`, citado arriba). |
| convención de `forense/TRANSFER-*.md` + `forense/historico/TRANSFER-*.md` | **NINGUNA vía de escritura ni disciplina de commit propia.** Verificado en este acto (`git log --diff-filter=A`): los seis archivos existentes entraron **todos en el mismo commit** `8aff7cb` (25/ago/2026) — un barrido de reconstrucción del árbol, no seis actos que commitearon un transfer como entregable propio. No hay convención análoga a `forense/encargos/convencion.md` (sin cabecera obligatoria, sin ciclo `VIVO`/`CONSUMIDO`, sin regla de nomenclatura sellada) | quien arranca una sesión sucesora y busca contexto de la anterior — hoy por `grep`/lectura directa, no por índice | **el hueco es el hallazgo, no un defecto de este acto**: un transfer real de mesa (p.ej. maestra-30 → maestra-31, 26/ago/2026) puede vivir solo en una conversación, invisible al repo, salvo que alguien lo pegue a mano — mismo patrón que `forense/encargos/convencion.md` documenta para encargos huérfanos (`ENCARGO P2`, 5/ago). No se inventa vía aquí: se declara el hueco. |

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
| **voy a tocar la familia de inventarios de reactivos/texto del corpus** | `data/inventario-reactivos-v1_2.tsv` (`variable_id`/`instrumento` por payload, sucesora de `ADR-213`/`ADR-216`, `texto_reactivo` vacío en el 100% de sus filas — no trae texto; columna `instrumento` reparada dos veces: `(raiz)` por `ACTO MAESTRA31-E7`, 39 payloads `(sin-instrumento-derivable)` parcialmente por `ACTO MAESTRA32-E6`, 16 de 39 resueltos) **+** `data/inventario-fd-v1_1.tsv` (`ADR-215`/`ADR-223`, único con `texto_reactivo` poblado, 100% de sus filas, cobertura 32/33 payloads con patrón de nombre de diccionario; columna `instrumento` reparada por `ACTO MAESTRA32-E6`, 10 de 10 payloads `(raiz)` resueltos, primera vez que recibe la regla de etiqueta) **+**, si es un censo de cobertura del motor contra estas tablas por token exacto de `variable_id`, `data/cruce-inverso-v1_1.tsv` (`ADR-214`/`ADR-216`) **+**, si es un emparejamiento de texto libre (θ/desenlace de `canon/modelo-decision-v4_0.md` §2.1 contra `variable_id`/`texto_reactivo` de las dos primeras tablas, con especificación congelada antes de correr, A.4 por par), `data/emparejamiento-motor-v1_1.tsv` (`ADR-221`/`ADR-223`, `ACTO MAESTRA32-E2 · EMPAREJA-MOTOR-TEXTO` re-corrido verbatim por `ACTO MAESTRA32-E6 · ETIQUETA-v1_2` sobre las dos tablas reparadas, 0 de 9 veredictos movidos) — **ningún acto de esta familia edita `milpa/procedencia.yaml`**: cambiar `ruta:`/`nota:` de una fila exige acto sucesor con adjudicación propia (precedente `ADR-218`). Fila añadida por `ACTO MAESTRA32-E2`, regla de conducto `ADR-70(c)`: el índice (12/ago) es anterior a las tres tablas (27-28/ago), hueco declarado por dirección en la VERIFICACIÓN DE EXISTENCIA de su propio encargo. **+** `data/inventario-reactivos-ext-v1_0.tsv` (`ACTO MAESTRA32-E3 · EXTRACTOR-DTA` v2, mismo esquema de 9 columnas; rama (a) de `FP-175`: 133 payloads causa B de `data/cobertura-composicion-v1_0.tsv` — .dta/.sav/.por/.sas7bdat/.xpt vía `pyreadstat`, .dbf vía `dbfread`, .rdata/.rds vía `pyreadr`, todos `metadataonly`/`load=False`; tabla hermana, no toca las anteriores; 123/133 payloads con ≥1 fila, 63242 filas, 24035 con `texto_reactivo` no vacío). **+** `data/inventario-fd-ext-v1_0.tsv` (`ACTO MAESTRA32-E12 · EXTRACTOR-FD`, mismo esquema de 9 columnas; rama (b) de `FP-175`: 46 payloads de ficha descriptiva/diccionario en formato ≠ `.xlsx` — .pdf vía `pdfplumber` (tablas primero, texto por línea con regex de mnemónico si no hay tabla), .xls vía `xlrd`, .html vía `bs4`/`lxml`, .zip abierto con `zipfile` y sus miembros despachados por la misma regla; tabla hermana de `inventario-fd-v1_1.tsv`, no la toca; 40/46 payloads con ≥1 fila (87,0%), 10635 filas, 100% con `texto_reactivo`. Control positivo pre-registrado sobre `fd_envipe2025.pdf`/`FD_ENCUCI2020.pdf`: 75,0%/0,0% de solape contra el inventario de microdato — el parser de `.pdf` queda declarado **NO VALIDADO en general** porque uno de los dos controles cayó por debajo del umbral de 60%). |

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

---

## Serie municipal de participación y calendario de homologación (`ACTO MAESTRA34-L6`, 2/sep/2026)

Tres artefactos nuevos bajo `data/`, con su productor, su esquema, quién los lee
y la advertencia que hace falta para no malusarlos.

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/p0-calendario-ayuntamientos-v1_0.tsv` | `python3 tools/p0_calendario_pel.py` (`ACTO MAESTRA34-L6`, P0) | 12 campos: `entidad, anio_jornada, concurrente_con_federal, ayuntamientos, n_actividades_municipales, cargos_declarados, ejemplo_actividad, fuente_archivo, fuente_hoja, fuente_acuerdo_ine, handle_dspace, nota_concurrencia`; 146 filas (entidad × jornada) | `tools/p0_calendario_pel.py` (deriva de aquí la tabla de tratamiento), `tools/l6_estimador_concurrencia.py` | **`GENERADO` — no editar a mano.** Se deriva de 30 acuerdos del Consejo General del INE (`repositoriodocumental.ine.mx`), ciclos 2014-2015 a 2024-2025. `ayuntamientos=SI` **no** se lee del rótulo «Cargos a elegir» de la hoja del INE: se exige que una **actividad** nombre a la vez el cargo municipal y un acto electoral, porque el rótulo miente al menos una vez (hoja `Veracruz` del PEL 2023-2024). `concurrente_con_federal` se lee de la **fecha de jornada**, no del año: Chiapas 2015 votó el 19 de julio, y va como excepción documentada con su cita. Las 16 entidades con `ayuntamientos=INDETERMINADO` en 2015 son «no se pudo determinar el cargo», **no** «no hubo elección». |
| `data/p0-tratamiento-homologacion-v1_0.tsv` | `python3 tools/p0_calendario_pel.py` (`ACTO MAESTRA34-L6`, P0) | 9 campos: `entidad, elecciones_ayuntamiento_en_ventana, anios_no_concurrente, anios_concurrente, anio_tratamiento, cohorte, estatus, tiene_antes_y_despues, n_elecciones`; 32 filas, una por entidad | `tools/l6_estimador_concurrencia.py`, y todo acto sucesor del diseño escalonado | **`GENERADO` — no editar a mano.** `anio_tratamiento` es el primer año en que la elección municipal de la entidad fue concurrente **habiendo sido no concurrente antes**; una entidad `SIEMPRE-CONCURRENTE-EN-VENTANA` no es un control: es una unidad **siempre tratada**, y en un estimador escalonado no puede servir de comparación. El único `NUNCA-TRATADO` es Durango. |
| `data/l6-resultados-concurrencia-v1_0.json` | `python3 tools/l6_estimador_concurrencia.py` (`ACTO MAESTRA34-L6`, P3) | JSON: `beta, gamma, ic95_wild_cluster, ic95_bootstrap_municipio, att_por_cohorte, por_transicion, agregado_estatal, heterogeneidad_tamano, sensibilidad_*, controles_lectura, municipios_perdidos` | nota de cierre del acto, `milpa/tramite-ola5-propuesta-v0.yaml` (entrada `civico.participacion.contingente_escalonado_2016_2024`) | Salida cruda del estimador de la spec congelada en `forense/notas/2026-09-02-MAESTRA34-L6-P2-spec.md`. **`beta` sola no se cita**: es el promedio de dos `ATT` de signo opuesto (`att_por_cohorte`), y citarla sin ellos invierte el sentido del hallazgo. El `ic95_wild_cluster` viene de **4 conglomerados** y su `p` mínimo alcanzable es `0.125`. |

**Regla de conducto que este acto deja escrita** (vale para cualquier acto que
abra una tabla de cómputos de un OPLE): **el código HTTP no verifica un
payload.** `www.ieeags.mx` responde `200` con una página HTML a rutas
inexistentes, y un archivo entró al corpus con 33 668 B de HTML bajo un `200`;
lo atrapó `zipfile.testzip()`, no el código. Y **una columna llamada «total» no
es necesariamente el total**: la tabla de Zacatecas 2024 trae `T VOTARON` con
«Sin Dato» en 839 de 2 649 casillas y `VTOTAL` completa — la que se usa es la
que cumple una identidad aritmética comprobable (`Σ(partidos) = VTOTAL`), no la
que tiene mejor nombre.

## Tipo de boleta federal: identificación y medición (`ACTO MAESTRA35-L3`, 2/sep/2026)

Dos artefactos nuevos bajo `data/`, sucesores directos de los tres de
`ACTO MAESTRA34-L6` de la sección anterior. Se registran aquí por el mismo
motivo: quien los lea tiene que saber qué **no** puede hacer con ellos.

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/l3-tabla-identificacion-v1_0.tsv` | `python3 tools/mide_participacion_tipo_boleta.py --tabla-identificacion` (`ACTO MAESTRA35-L3`, P0) | 12 campos: `entidad, de, a, hueco, tipo_de, tipo_a, dD_pres, dD_int, clase, identifica, estatus_entidad, cohorte`; **73 filas** (una por entidad × transición consecutiva), 32 entidades | la spec de `MAESTRA35-L3` (`§0.3`, `§1.5`), y todo acto sucesor del diseño por tipo de boleta | **`GENERADO` — no editar a mano.** Se deriva de `data/p0-calendario-ayuntamientos-v1_0.tsv` más el ciclo federal (2018 y 2024 presidenciales, 2015 y 2021 intermedias). **Es una tabla del UNIVERSO, no del panel**: sus 73 transiciones incluyen entidades cuyo denominador nadie ha adquirido todavía. La cifra que hay que leer antes de diseñar cualquier sucesor es que **sólo 5** de las 73 son `STAY` —las únicas que identifican `α` sin mezcla— y **dos de esas cinco** (Aguascalientes 2016→2019, Hidalgo 2016→2020) son de entidades cuya lista nominal municipal **no existe en ninguna fuente programable** medida al 2/sep/2026. |
| `data/l3-resultados-tipo-boleta-v1_0.json` | `python3 tools/mide_participacion_tipo_boleta.py --tipo-boleta --json …` (`ACTO MAESTRA35-L3`, P2) | JSON: `control_regresion_l6, estimador{alpha,beta_pres,beta_int,wild_cluster_*,ic95_bootstrap_municipio}, variante_sin_alpha, identificacion_del_panel, por_transicion, att_por_transicion, agregado_estatal, heterogeneidad_tamano, sensibilidad, descomposicion_L4, controles_lectura, municipios_perdidos` | nota de cierre del acto, `milpa/tramite-ola5-propuesta-v0.yaml` (entrada `civico.participacion.tipo_boleta_federal_2016_2024`) | Salida cruda del estimador de la spec congelada en `forense/notas/2026-09-02-MAESTRA35-L3-spec.md`. **Ninguno de los dos `β` se cita solo con su punto**: el veredicto del falsador fue **`NO-DISCRIMINA`** porque los dos IC95 *wild cluster por entidad* contienen 0, y el bootstrap por municipio —que **no** es el que decide— discrepa en los dos. Citar `β_pres = +3.15` sin su IC conservador invierte el sentido del acto. `β_int` además **cambia de signo** entre subconjuntos y lo identifican **dos** transiciones que se contradicen: no es un número que se pueda reusar. El `control_regresion_l6` es parte del producto, no un adorno: si deja de dar `identico_byte_a_byte: true`, el panel de `L6` cambió y esta corrida ya no es comparable con la suya. |
| `data/l8-resultados-tipo-boleta-v1_0.json` | `python3 tools/l8_amplia_tipo_boleta.py --json …` (`ACTO MAESTRA35-L8`, P1) | Mismo esquema que el de `L3` de arriba, sobre el panel ampliado (9 entidades) | nota de cierre del acto, `forense/notas/2026-09-02-MAESTRA35-L8-spec.md` (`COMMIT-2`), `milpa/tramite-ola5-propuesta-v0.yaml` (bloque `relanzamiento_l8` de la misma entrada) | Sucesor de `l3-resultados-tipo-boleta-v1_0.json`, **no lo reemplaza** — el de `L3` sigue siendo la corrida de 6 entidades, éste la de 9. Veredicto **`ACOTADA`** (`L3`: `NO-DISCRIMINA`): `β_pres` cruza cero (IC wild cluster `[+0.05,+7.89]`, margen estrecho — el extremo inferior es `+0.049`), `β_int` no (`[−1.22,+1.79]`, y **cambia de signo** frente a `L3`). **`COMMIT-1` de este acto se congeló después de ver el resultado** (declarado en `forense/notas/2026-09-02-MAESTRA35-L8-spec.md §0.0`): la spec no tenía grados de libertad que el conocimiento previo pudiera sesgar, pero la garantía mecánica de "spec fijada a ciegas" no aplica a este archivo — cítese con esa salvedad, no como un `COMMIT-1`/`COMMIT-2` ordinario. Hidalgo entra al panel (`STAY` 2016→2020) sin volverse entidad tratada medible: no se le puede atribuir ningún `β`. |

**Regla de conducto que este acto añade** (complementa la de `MAESTRA34-L6`,
que decía que el código HTTP no verifica un payload y que el nombre de una
columna no garantiza su contenido): **`http_code = 000` no significa
«bloqueado».** `www.ieebc.mx` y `www.ieepco.org.mx` daban `000` con
`curl: (60) unable to get local issuer certificate` porque mandan la **cadena
TLS incompleta**; anexando el intermedio que su propio AIA declara, los dos
pasan a `200` con verificación real. **Nunca `--insecure`.** Antes de declarar
`NO-OBTENIDO` por red hay que leer el error crudo de `curl`, no sólo su código.

## Adopción de gobierno digital y respaldo personal (`ACTO MAESTRA35-L6`, 2/sep/2026)

Dos artefactos nuevos bajo `data/`. Se registran aquí por el mismo motivo que los
de las dos secciones anteriores: **quien los lea tiene que saber qué *no* puede
hacer con ellos**, y en estos dos la advertencia es la mitad del producto —
salieron de un censo que cerró con **cero `EXISTE-SATISFACE`**, así que ninguna
de sus cifras es la `p` del prior que el acto fue a buscar.

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/l6-gobierno-digital-endutih-v1_0.json` | `python3 tools/medidor_gobierno_digital_endutih.py` (`ACTO MAESTRA35-L6`, `P1`) | JSON: `acto, pieza, spec, estimador, escala, olas[]` con una entrada por ola (`2025` principal, `2024` y `2023` sensibilidad) y, en cada una, `payload, miembro, sha256_payload, n_tabla, n_usa_internet, principal, sensibilidad_A_interaccion, sensibilidad_B_universo_ampliado`; cada celda trae `p, ic95, n, numerador, estratos, upm, poblacion_expandida` | la nota de resultados del acto y `milpa/tramite-ola5-propuesta-v0.yaml` (entrada `tramite.gobierno_digital.adopcion_endutih2025`) | **No es la `p` de `tramite.gobierno_digital.coercitivo`, y citarla como tal invierte el sentido del acto**: el censo `P0` §3 cerró `EXISTE-NO-SATISFACE` en las tres olas porque ENDUTIH **no tiene** marcador de obligatoriedad ni de riesgo fiscal, **no tiene** batería de motivo colgada del bloque de gobierno, y su único ítem fiscal (`P7_36_1`) está autoseleccionado al 100 % —`16 362/16 362` en 2025— además de carecer de denominador de obligación (`no obligado ≠ rechaza`). **Tampoco se compara con el `0.673393` de `util_sin_coercion`**: aquella cifra tiene unidad **trámite** y universo `N_TRA=01` (pago de luz, ENCIG); ésta tiene unidad **persona** y universo **usuarios de internet**. Y la escala es de **usuarios de internet**, no de la población: para esa, la sensibilidad `B` (`0.178152` en 2025). Citar `0.207026` sin su universo lo convierte en otra cifra. |
| `data/l6-respaldo-enif2024-v1_0.json` | `python3 tools/medidor_puente_enif24.py` (`ACTO MAESTRA35-L6`, `P2`/`COMMIT-3`) | JSON: `acto, pieza, spec, payload, tabla, sha256_payload, estimador, eje, escala, limite, n_universo, eje_reparto, desenlaces[] (D1_ahorro_formal PRINCIPAL, D2_tenencia_cuenta, D3_credito_formal), sensibilidad_C_control_riqueza[], veredicto_del_acto, veredicto_D1, veredicto_secundarios`; cada celda con `p, ic95, n, numerador, estratos, upm` | la nota de resultados y `milpa/tramite-ola5-propuesta-v0.yaml` (entrada `dinero.ahorro.respaldo_enif2024`) | **Mide UNA de las dos condiciones del bullet** `dinero.ahorro.informal_sin_puente` + `con_puente_y_respaldo` (`canon/modelo-decision-v4_0.md:501`): el **respaldo** (`P4_9_4`, universo completo), **no** el canal personal, que es inobservable porque `P5_15_2` está gateado en tener el producto y haberlo comparado. **Acota la regla; no la cierra.** Y **el agregado de `D1'` no se cita solo**: `+5.82` pp es el promedio de dos poblaciones que van en direcciones opuestas — la sensibilidad `C`, pre-declarada, da `−7.44` pp entre quienes podrían resolver con recursos propios (`CONTRARIA`) y `+8.14` pp entre quienes no (`CORROBORADA`), los dos `IC95` sin traslape. Citar el agregado sin `C` afirma un mecanismo uniforme que el dato niega. Es **asociación dentro de una corrida (A-bis 1/2), no efecto**. El campo `veredicto_del_acto` (`ACOTADA`) lo deriva el script, no el analista. |

**Regla de conducto que este acto añade** (complementa las dos anteriores —el
código HTTP no verifica un payload, el nombre de una columna no garantiza su
contenido, `http_code = 000` no significa «bloqueado»): **el catálogo de columnas
no agota lo que el instrumento midió.** En `IFT SFD 2024` la batería «¿a través
de qué medios se enteró?» tiene cinco columnas codificadas y **ninguna** es
«familiares» — pero de las 96 respuestas del texto libre «Otro», **70 dicen
literalmente «Familiares y amigos»**, y el propio emisor publica esa categoría en
su reporte. Quien abra sólo la cabecera del `xlsx` concluye que la variable no
existe, y se equivoca. **Antes de declarar `NO-ENCONTRADO` sobre una variable hay
que abrir los campos de texto libre de la batería que la contendría.**

---

## Lote REGLAS-ACTIVOS-L2, cuatro reglas del modelo (`ACTO MAESTRA35-L7`, 2/sep/2026)

Cinco artefactos nuevos bajo `data/`, salida cruda de las cuatro piezas del
lote (una corrida consolidada, `tools/emite_resultados_l7.py`, que solo
importa y llama a los cuatro medidores ya congelados — no recalcula nada).

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/l7-resultados-v1_0.json` | `python3 tools/emite_resultados_l7.py` (`ACTO MAESTRA35-L7`) | JSON con cuatro claves `pieza_{a,b,c,d}_*`, cada una con la salida de `mide_eje`/`wratio_ic_conglomerado` (celdas, IC95, veredicto) de `forense/notas/2026-09-02-MAESTRA35-L7-spec.md` | nota de cierre del acto, `milpa/tramite-ola5-propuesta-v0.yaml` (las cuatro entradas nuevas de este acto) | **`GENERADO` — no editar a mano.** La pieza (c) trae una razón (`Σw·num/Σw·den`), no una proporción de binario — sus celdas usan el campo `p` para el valor de la razón, no para una proporción 0-1 de un indicador; el mismo campo en la pieza (a)/(d) sí es proporción. La pieza (c) D1 (`sexo_edad`) trae medias de horas continuas en el mismo campo `p` — leer el `nota`/`eje` de cada bloque antes de citar un número suelto. |
| `data/l7-log-pieza-a.txt`, `data/l7-log-pieza-b.txt`, `data/l7-log-pieza-c.txt`, `data/l7-log-pieza-d.txt` | ídem, `redirect_stdout` de cada medidor | texto plano, salida literal de cada script (incluye guardias y censos que el JSON no serializa) | auditoría/reproducción; no tiene lector programático | Es el registro más completo — el JSON resume, el log es la corrida literal. |

**Regla de conducto que este acto no añade nueva**, aplica las ya escritas: el
denominador de la pieza (c) se verificó por reconstrucción de la llave de
hogar (`FAC_PER` no es constante dentro de hogar, `FAC_HOG`/`EST_DIS`/
`UPM_DIS` sí — verificado con `groupby(...).nunique()==1`, no asumido).

## Censo de reglas activas sobre LAPOP / ENCUCI / ENIF (`ACTO MAESTRA35-L9`, 2/sep/2026)

Un artefacto nuevo bajo `data/` y **una raíz que este índice no documentaba**.
Se registra por la misma razón que las secciones anteriores: la advertencia es
parte del producto.

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/l9-censo-a4-v1_0.tsv` | rutas `--censo` de `tools/medidor_clientelismo_lapop.py`, `tools/medidor_protesta_lapop.py`, `tools/medidor_entitlement.py`, `tools/medidor_seguro_deposito_enif24.py` (`ACTO MAESTRA35-L9`, `P0`) | TSV de 16 columnas × 10 filas de datos: `pieza, regla, id_modelo, tier, fuente, payload_id, sha256_coincide, item_desenlace, item_moderador, codigos_desenlace, denominador, ponderador, diseno, unidad, veredicto, que_falta` | la spec congelada del acto y quien vuelva a plantear una pieza sobre LAPOP México | **Tres de sus diez filas son `EXISTE-NO-SATISFACE` y son el contenido, no el residuo.** (1) **Ninguna ola de LAPOP México cruza dádiva con secreto del voto**: 2019 tiene `clien1n/clien1na/clien4a/clien4b` y cero ítems de secreto; 2023 tiene `countfair3` y cero `clien*`; 2021 no tiene ninguno de los dos. Quien vuelva a proponer `R7.3`/`R7.6` **contra la dádiva** está proponiendo un cruce que no existe en el corpus. (2) **2006 no hace serie con 2019**: `PROT1`/`PROT2` son escala de frecuencia de tres niveles y `PROT2` está gateada (n = 209), frente a `prot3` binaria y ungateada; el archivo de 2006 tampoco trae ponderador. (3) **`P5_24_*` de ENIF no mide «seguro visible»**: está anidada en el «Sí» de `P5_23`, y de los 4 136 que dicen saber que sus ahorros están protegidos, **3 148 no saben nombrar la institución**; sólo 362 en toda la muestra nombran al IPAB. Además: **`wt` de LAPOP México es constante = 1** en 2019 y 2023 (muestra autoponderada), así que «proporción ponderada» ahí es idéntica a la simple y todo el efecto de diseño vive en el conglomerado, no en el peso. |

**Regla de conducto que este acto añade — hay una segunda raíz de payloads, y no
está en `data/raw`.** `data/manifiesto.yaml` declara payloads bajo
`raiz: descargas_mx`, que `forense/notas/2026-08-06-map1b-censo-raices.md:68`
resuelve a `/mnt/c/Users/PC0/Descargas MX`. Esa ruta vive en
`data/raices.local.yaml`, que **es gitignorada**: un worktree recién creado nace
sin ella, y entonces `find`/`ls` sobre `data/raw` declaran `NO-ENCONTRADO` para
payloads que están perfectamente en disco. Las cuatro olas de LAPOP México son
exactamente ese caso. **Antes de declarar que un payload del manifiesto no está,
hay que resolver su campo `raiz`** — y un medidor que dependa de una raíz no
configurada debe **PARAR diciéndolo**, nunca reportar el payload como ausente;
los cuatro medidores de este acto lo hacen. Misma familia que `A.13` y que la
trampa de `find` sin `-L` sobre el symlink de `data/raw`.

**Cuatro artefactos de resultados del mismo acto** (`COMMIT-2`), con la
advertencia que hace falta para no citarlos al revés:

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/l9-clientelismo-lapop-v1_0.json` | `python3 tools/medidor_clientelismo_lapop.py --mide` | JSON: `acto, spec, estimador, aviso_ponderador, payloads[], piezas[]` — pieza `a` con `asistencia{ofrecieron,no_ofrecieron,delta}`, `eleccion{PRI_principal,MORENA_secundario}`, `ejes_secundarios`; pieza `a-bis` con `cobertura_vb20, universo_restringido, SECRETO, OBSERVABLE, delta_diferencia`. Cada celda: `p, ic95, n, numerador, n_estratos, n_upm, control_regresion` | la nota de resultados y `milpa/tramite-ola5-propuesta-v0.yaml` (entradas `civico.clientelismo.turnout_no_vote_choice_lapop2019` y `civico.voto.agencia_lapop2023`) | **La pieza `a` salió `NO-DISCRIMINA`: sus `+3.96 pp` de asistencia NO despejan el cero** (`[−0.77, +8.62]`), así que citarlos como si la regla se hubiera corroborado invierte el resultado. **Y la brecha de elección es descriptiva DENTRO de los votantes** — condiciona en `vb2`, que es el otro desenlace: colisionador declarado en la spec. **La pieza `a-bis` salió `CONTRARIA` por la cláusula de precedencia, no porque el signo fuera negativo**: las dos ramas van hacia arriba y limpias, y eso es justo lo que refuta la separación que `R7.3`/`R7.6` afirman. La rama SECRETO se apoya en **79** tratados. **Nada de esto reabre la fila `C` de `ADR-155`.** |
| `data/l9-protesta-lapop-v1_0.json` | `python3 tools/medidor_protesta_lapop.py --mide` | JSON: `pieza, reglas, payload, eje_principal{4 celdas}, contrastes{C1,C2}, ejes_secundarios, antecedentes_no_medidos` | ídem, entrada `civico.protesta.agravio_urbano_lapop2019` | **`C2` corrobora y `C1` no existe — y `C1` es el corazón de la regla.** La celda rural-víctima tiene 65 personas y 7 que protestaron: cayó por la guardia de numerador < 10 pre-registrada. Citar el `+5.60 pp` de `C2` como si `R7.4` quedara corroborada afirma algo sobre el **entorno** que este dato no midió. Mide **dos de los cuatro** antecedentes de la regla. **No dice nada sobre `R7.5` ni reabre el `D` de `ADR-158`**, que corrió sobre datos de evento. |
| `data/l9-entitlement-encuci-v1_0.json` | `python3 tools/medidor_entitlement.py --mide` | JSON: `pieza, universo, n_universo, cobertura, eje_principal{beneficiario,no_beneficiario,delta}, eje_anidado_AP6_11, ejes_secundarios, reserva` | ídem, entrada `civico.transferencia.entitlement_encuci2020` | **`CONTRARIA`: el signo va al revés de lo que `R7.8` predice.** Los beneficiarios dicen «derecho» **menos** (54.03 % contra 60.60 %, `−6.57 pp` sin traslape). Quien cite este JSON buscando apoyo para el entitlement estará citando su refutación. El eje `AP6_11` está **anidado** en `AP6_10 = 1` y por spec **no puede voltear** el principal. Es **asociación transversal**: no separa que el programa cambie la percepción de que quien ya pensaba distinto se inscribiera más. |
| `data/l9-seguro-deposito-enif24-v1_0.json` | `python3 tools/medidor_seguro_deposito_enif24.py --mide` | JSON: `pieza, universo, n_universo, cobertura_moderador, desenlaces{D1,D2}, ejes_secundarios, eje_no_construible, hallazgo_marginal_ipab, reserva` | ídem, entrada `dinero.ahorro.seguro_deposito_enif2024` | **`NO-DISCRIMINA` en los dos desenlaces, con los puntos en el signo contrario al predicho.** El número que sí es limpio es el del bloque `hallazgo_marginal_ipab`, y no es una `p` de la regla: de 4 136 que dicen saber que sus ahorros están protegidos, **3 148 no saben nombrar la institución**, y sólo **362 de 13 502 (2.7 %)** nombran al IPAB. `P5_23` mide **creencia de que hay protección**, no la **visibilidad** que el `SI` de `R1.5` nombra. Y `P5_20` es **razón principal**: quien desconfíe pero elija otra razón dominante no cuenta como desconfiado. |

## Segundo instrumento sobre reglas de `ACTO MAESTRA35-L9` (`ACTO MAESTRA35-L11 · ROBUSTECE-L9`, 2/sep/2026)

Dos artefactos nuevos bajo `data/`, producidos por un medidor hermano que
**no toca** los cuatro medidores de `L9`.

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/l11-encuci2020-v1_0.json` | `python3 tools/medidor_l11_encuci2020.py --mide` | JSON: `acto, spec, instrumento, payload, estimador, piezas[]` — pieza `b` (`R7.3`/`R7.6`) con `ramas{SECRETO,OBSERVABLE}`, `delta_diferencia`; pieza `c` (`R7.4`) con `eje_principal{4 celdas}`, `contrastes{C1,C2}`. Mismo formato de celda que `L9` (`p, ic95, n, numerador, control_regresion`) | la nota de resultados de `L11` y `milpa/tramite-ola5-propuesta-v0.yaml` (entradas `civico.voto.agencia_con_secreto_encuci2020`, `civico.protesta.agravio_urbano_encuci2020`) | **La pieza `b` salió `CONTRARIA` otra vez, y REPLICA la de `L9`**: mismo signo, IC95 fuera de 0 en las dos ramas de los dos instrumentos → `CONTRARIA-REPLICADA` sobre una regla `[FUERTE]` (`R7.3`). **La pieza `c` tiene `C1` (entorno, el corazón de la regla) ESTIMABLE por primera vez** (numerador 188 contra 7 en `L9`), pero el IC95 roza cero (`[−0.18, +4.12]`): no discrimina. `C2` sí replica limpio. Veredicto conjunto de `C1`: `AMBIGUA-ENTRE-INSTRUMENTOS`, no nulo — el punto va en el signo esperado en los dos intentos, ninguno lo prueba. |
| `data/l11-replicacion-v1_0.json` | escrito a mano por el acto, a partir de `l9-*-v1_0.json` + `l11-encuci2020-v1_0.json` | JSON: `filas[]`, una por regla/pieza, con `l9{...}`, `l11{...}`, `veredicto_conjunto`, `justificacion_sello`; más `contador` agregado | mesa (letras g–k pendientes sobre `L9`), y el sucesor declarado `N10 · SELLA-L9` | **Es la TABLA DE REPLICACIÓN que el encargo pide, no un veredicto nuevo del motor.** Ninguna fila carga a `milpa/tramite.yaml`; las dos entradas correspondientes en la propuesta quedan `PENDIENTE-DE-MESA`. Las piezas `(a)` `R7.7` y `(d)` `R1.5`/Mexico Panel no tienen fila de segundo instrumento: `(a)` es `EXISTE-NO-SATISFACE` en los dos instrumentos disponibles (censo `P0` de `L11`); `(d)` es `NO-LANZADA` por compuerta (ICPSR 35024 ausente del manifiesto). |
| `data/l12-mps2012-v1_0.json` | `python3 tools/medidor_l12_mps2012.py` (sin flags; ejecuta la spec congelada en `forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada-bis-v3.md`) | JSON: `P0_censo_y_estampa` (sha256 de los 5 payloads contra `data/manifiesto.yaml`, censo de celdas por tabla, cuadre de los 3 marginales de control contra el codebook, estampa de segunda mano), `P1_R7_7_vote_choice` (turnout T1 + vote-change T6 con los DOS desenlaces, `umbral_no_discrimina_semiancho`, `veredicto_Bbis`), `P1_robustez_T7`, `P2_R7_3_R7_6_replica` (T3/T4 por estrato y agregado), `P3_experimento_de_lista` (dos rondas), `P4_exploratorio_T8_T9a`, `pendiente_de_mesa` | la nota de resultados de `L12` y `milpa/tramite-ola5-propuesta-v0.yaml` (entradas `civico.clientelismo.vote_change_mps2012`, `civico.clientelismo.prevalencia_lista_mps2012`) | **Instrumento de SEGUNDA MANO: es salida del tabulador en línea «Explore Data» de ICPSR 35024, no el microdato** (`35024-0001-Data.dta` exige membresía → `A.4 NO-ACCESIBLE`). Conteos **sin ponderar**, sin estrato ni UPM; tier máximo alcanzable **MEDIA con reserva**; `entra_al_motor` es `false` en todas las piezas. `P1` sale **`NO-DISCRIMINA`** por la rama de precedencia (semiancho 16.96 pp contra un umbral de 15 pp fijado antes de mirar el signo), y su hallazgo es que **el signo de Δ se voltea según se cuente el cambio por código o por bloque de partido** — las dos cifras van en el JSON, ninguna se esconde. Un campo es trampa para quien lo reuse: `P3` está gobernada por un `supuesto_no_verificado_que_lo_gobierna` — que la lista B sea la lista A más el ítem de venta del voto —, así que **no es una medición cerrada** hasta leer el texto de los ítems en el cuestionario. |

**Regla de conducto que este acto no añade nueva, la confirma**: Latinobarómetro
2024 (`data/raw/latinobarometro2024_bd_stata.zip`) se abrió por metadatos
(332 columnas, sólo nombre y etiqueta) y **no trae ningún ítem** de compra de
voto, secreto del voto, protesta/agravio localizado ni transferencia
condicionada al voto — búsqueda por etiqueta, control positivo con los términos
que sí aparecen (`voto`, `corrup`, `pais`). Es la primera vez que esta ola se
abre en el repo con ese propósito; el hallazgo queda también en
`forense/hallazgos.md`.

## Adopción de e.firma contra el padrón activo del SAT (`ACTO MAESTRA36-L13 · COERCITIVO-SAT-EFIRMA`, 3/sep/2026)

Un artefacto nuevo bajo `data/`, primera medición del programa contra una
fuente **administrativa** con denominador de obligación (las anteriores sobre
esta regla fueron encuestas de hogares, que sólo observan a quien ya hizo el
trámite — `ADR-287`, `ADR-299`).

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/l13-sat-efirma-v1_0.json` | `python3 tools/medidor_l13_sat_efirma.py --mide` | JSON: `acto, regla, prior, escala, sin_ic_de_diseno, fuentes[], anos_completos_comunes[], serie[]` (una fila por año con `n_acumulado_primeras_efirma`, `padron_total`, `padron_asalariados_pf`, `padron_obligado_aprox`, `identidad_total_menos_partes`, `p_inf`, `p_sup`), `p_inf`, `p_sup`, `tramo_*`, `veredicto`, `falsador_congelado`, `cota_superior_declarada` | mesa, y el sucesor declarado `N11 · SELLA-L13` | **Las dos `p` son PROPORCIONES ADMINISTRATIVAS AGREGADAS — campo del entorno, no probabilidad individual de conducta** (precedente: firma `p1`, mesa 2/sep/2026, `ADR-299`). Comparables con el `0.09` asignado sólo en signo y orden de magnitud, **nunca** como «difiere en Z %». **No hay IC de diseño y no es omisión**: es un censo, no una muestra; la incertidumbre es de definición de universo y va en las dos cotas. **Ambas cotas son cotas SUPERIORES de la adopción vigente**, porque el numerador acumula altas primeras desde 2004 y el certificado caduca. El veredicto es `AMBIGUA-POR-UNIVERSO`: **no adjudica**, y nada de este JSON se carga al motor. |

El medidor tiene además `--censo`, que es la pieza `P0`: imprime estructura y
verifica los seis `.xls` del SAT por `sha256` contra `data/manifiesto.yaml`
(6/6 `COINCIDE`), sin calcular ninguna tasa. Cuatro de los seis quedaron
`EXISTE-NO-SATISFACE` o fuera de escala con la razón dicha
(`forense/notas/2026-09-03-MAESTRA36-L13-P0-censo.md`).

Los payloads viven en la raíz **`descargas_mx`**, no en `data/raw`: un worktree
nuevo la resuelve con `data/raices.local.yaml`, que es **gitignorada** — sin
ella, cualquier búsqueda declara `NO-ENCONTRADO` en falso (mismo hallazgo que
`ACTO MAESTRA35-L9`).

## Tres lecturas de universo para una misma regla (`ACTO MAESTRA36-L14 · COERCITIVO-TRES-UNIVERSOS`, 3/sep/2026)

Sucesor de L13. Mesa negó el sello sobre el padrón del SAT —una **subpoblación**—
para una regla **poblacional**, y pidió el universo poblacional. El artefacto
nuevo no es una `p`: es la **tabla de las lecturas posibles con el mismo
numerador**, para que mesa elija cuál nombra la regla.

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/l14-coercitivo-universos-v1_0.json` | `python3 tools/medidor_l14_coercitivo_universos.py --mide` | JSON: `acto, regla, prior, no_adjudica, escala, trimestre_de_corte, razon_del_trimestre, numerador` (re-citado de L13), `denominadores_enoe` (por denominador: `total, filas_muestra, upm_distintas, estratos, estratos_una_upm, ee, ic95_inf, ic95_sup, cv`, más `_particion`), `lecturas` (A, A′, A″, B, C con `p` e `IC`), `incompatibilidades_de_universo[]` (cada una con `signo`), `cota`, `fuentes[]` | mesa, y el sucesor `N13 · SELLA-COERCITIVO` | **No hay clave `veredicto` y es por diseño**: el acto mide y **no adjudica**. **Las cinco `p` son cotas SUPERIORES** (el numerador acumula primeras e.firma desde 2004 y el certificado caduca). **Dos lecturas dan `p > 1`** —`A′ = 1.20`, `A″ = 9.41`— y eso **no es un error de cuenta: es la medición del desacople de universos**; leerlas como «adopción del 120 %» es el error que la fila `clase` del YAML previene. Las tres `p` de ENOE **sí** traen `IC95` por diseño (conglomerado último, estrato `est_d_tri`, UPM `upm`); las dos del SAT **no**, porque son censo. |

El medidor tiene `--censo` como pieza `P0`: imprime la estructura de SDEM, pega
los nueve campos leídos del **diccionario del propio zip** y verifica las ocho
claves contra el **catálogo del propio zip** — `discordancia → PARO`, literal del
encargo. **La guardia disparó** en su primera corrida, y el defecto era del
lector, no del catálogo: **los catálogos del zip vienen en UTF-8 y el microdato
en latin-1**, así que decodificar el zip entero con una sola codificación
convierte un acento en un `PARO` falso. Se corrigió el lector (`dec()`, UTF-8 con
caída a latin-1) antes de congelar `COMMIT-1`; quien abra otro zip de INEGI hereda
el mismo riesgo.

Nota de nomenclatura para quien lea specs viejas: no existe un campo `EST_D` en el
diccionario ENOE del corpus. Existen `est_d_tri` (trimestral) y `est_d_men`
(mensual), y con ponderador `fac_tri` el que corresponde es `est_d_tri`.

## `/mapea` gana una tercera tabla: `descargas_mx` (`ACTO MAESTRA37-L1 · INDEXA-DESCARGAS-MX-Y-REMAPEA-SALUD`, 3/sep/2026)

Hasta este acto, `tools/busca_reactivos.py` (y por tanto `/mapea`) solo
veía `data/inventario-reactivos-v1_2.tsv` + `-ext-v1_0.tsv`, ambas
derivadas de `data/raw`. La raíz `descargas_mx` (ver arriba, "hay una
segunda raíz de payloads") nunca había sido indexada para búsqueda de
reactivos — un `NO-ENCONTRADO` de `/mapea` antes de este acto era
**mudo** sobre esa raíz, no un negativo (`DE1`, `forense/hallazgos.md`,
2026-09-03).

Un worktree nuevo necesita crear `data/raices.local.yaml` a mano (es
gitignorada, no viaja con el worktree) antes de que `--raiz descargas_mx`
funcione — mismo defecto de infraestructura documentado arriba para
LAPOP México/SAT e.firma, encontrado otra vez en este acto.

| artefacto | productor | esquema | quién lo lee | advertencia |
|---|---|---|---|---|
| `data/inventario-reactivos-descargas-mx-v1_0.tsv` | `tools/inventario_reactivos.py --raiz descargas_mx` + `tools/inventario_reactivos_ext.py --raiz descargas_mx` (unión manual, mismas columnas) | TSV: `payload_id, sha256_12, instrumento, ola, archivo_miembro, variable_id, texto_reactivo, metodo, universo_declarado` — 31 674 filas de dato, 116 `payload_id` distintos con ≥1 fila de sus 138 `DECLARADO-descargas_mx` | `tools/busca_reactivos.py --tablas descargas_mx` (o `todas`), `/mapea` | `instrumento` es casi siempre `(sin-instrumento-derivable)`: los derivadores de `tools/etiqueta_v1_2.py` (`aplica_v1_1`/`aplica_v1_2`) están escritos sobre convenciones de nombre de `data/raw`, no de `descargas_mx` — declarado, no inventado. `universo_declarado` hereda literalmente `PRESENTE_EN_DATA_RAW` de los scripts fuente (no se edita esa columna); en este archivo significa "presente en la raíz indexada por el comando", no en `data/raw` específicamente |

`--raiz` en ambos scripts de inventario (default `raw` = comportamiento
exacto de antes de este acto, verificado por diff de código y por
ejecución byte a byte contra el script sin modificar sobre el mismo
estado del corpus). `--tablas` en `busca_reactivos.py` (default `hoy` =
exactamente `v1_2`+`ext`, byte a byte igual a `--fuente ambas` de antes).
