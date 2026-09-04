# MAESTRA37-INFRA · Verificación post-hoc de INFRA-1/INFRA-2 contra el plan

4/sep/2026. Auditoría adversarial, posterior a la fusión de los tres PR que
ejecutaron `forense/notas/2026-09-04-MAESTRA37-INFRA-plan-final.md`
(en adelante "el plan"). No es un `/revisa` sobre un PR abierto — los tres
PR ya están fusionados en `origin/main`; esto corrobora si lo fusionado
cumple lo planeado, con ejecución real de pruebas, no solo lectura de
diff.

## Metodología

Cinco auditorías independientes en paralelo, cada una en un worktree de
solo lectura (`git worktree add ... origin/main --detach`, HEAD `53da938`),
con instrucción explícita de correr las pruebas reales (no solo leer
código) y de ser adversarial: no dar por cumplido un requisito sin cita
archivo:línea o salida de comando real. Ninguna tocó `data/curacion-registro/`
ni `data/manifiesto.yaml` reales — las pruebas que requerían escritura
corrieron sobre copias en directorios temporales.

Antes de auditar por frente, se confirmó `python3 tests/check.py --baseline`
en el HEAD fusionado: **19 FAIL · 169 WARN, LÍNEA BASE: VERDE** (sin FAIL
nuevo frente a `tests/baseline.json`). Se repitió esa misma confirmación,
de forma independiente, dentro de cada una de las cinco auditorías.

## Veredicto por commit

| PR | Commit | Frente | Veredicto |
|---|---|---|---|
| #521 (INFRA-1) | `5ffb5ca` | A — SSOT de adquisición | **Confirmado** (núcleo técnico); 1 desviación (sin tests nuevos) |
| #521 (INFRA-1) | `eda387f` | B — manifiesto seguro | **Confirmado** (7/8); 1 desviación (sin tests nuevos) |
| #521 (INFRA-1) | `f62a761` | C — alta atómica de relaciones | **Confirmado sin desviaciones** |
| #522 (INFRA-2) | `54a1b70` | E — portabilidad de raíces | **Confirmado** (7/7); 2 notas finas, sin desviación material |
| #525 (INFRA-2) | `dbe26fb` + `5a84f88` | D + FP-259 | **Confirmado mecánicamente** (9/9); 1 reserva de juicio |

## Frente A (`5ffb5ca`) — detalle

Confirmado con ejecución real: `tsv_crudo.upsert_fila()` es idempotente
(3 corridas verificadas: alta, actualización, repetición exacta → diff
vacío); `arbitra.py::encola_no_obtenido()` dejó de escribir la vista
(`COLA` queda definida pero sin uso, verificado por grep), reusa
`build_alias_index()` sin reimplementarlo, y escribe `estado_A4A5=PENDIENTE`
— nunca el token inexistente `"NO-OBTENIDO"` en la columna controlada.
`.claude/commands/arbitra.md` corregido. `registra_cola_adquisicion.py`
exige `--confirmo-migracion-legacy` **incondicionalmente**, verificado en
los 3 escenarios (destino ausente, vacío, poblado).

**Nota, no desviación**: el literal `"NO-OBTENIDO"` sí sobrevive dentro del
texto libre de la columna `nota` (p. ej. `"arbitra.py: NO-OBTENIDO, sin
payload..."`) — el plan prohibía el token en el vocabulario controlado
(`estado_A4A5`), no en la prosa explicativa; esto es consistente con la
intención original.

**Desviación real**: ningún test automatizado nuevo. La verificación
narrada en el mensaje de commit (dos corridas idénticas de `arbitra.py`,
comparación byte a byte) fue manual, no quedó codificada en el repo.

## Frente B (`eda387f`) — detalle

Confirmado en el punto más difícil de cumplir a medias: el `fcntl.flock`
de `_con_lock_manifiesto()` se verificó con **análisis de AST** (no solo
grep) y cubre, en las tres funciones (`cmd_registra`, `cmd_escanea`,
`cmd_promueve`), desde antes de la primera lectura del manifiesto/staging
hasta el último `print` de la función — no solo la función de escritura
interna, que es la forma fácil de implementarlo a medias. `_es_documental()`
verificada como puramente estructural (grep de los 5 IDs históricos reales
dentro de la lógica de validación → 0 resultados: no hay allowlist).
Escritura atómica probada con una excepción forzada a mitad de escritura
(`os.replace` con monkeypatch) → archivo original intacto. `.gitignore`
correcto.

**Desviación real (misma que Frente A)**: ningún test automatizado nuevo
para validación de esquema, atomicidad o alcance del lock — la única
suite tocada por este commit y ejecutada (`tests/test_manifiesto_alcance.py`)
cubre un tema no relacionado (filtro de extensiones), preexistente.

## Frente C (`f62a761`) — sin desviaciones

Las 5 reglas duras de `alta_relacion.py` se sostuvieron adversarialmente
sin ninguna vía de escape encontrada: nunca invoca `via_capa2.py` (grep
confirma 0 referencias fuera de comentario); un `relacion_id` ya existente
**siempre** aborta, sin bandera de "fusión"/force; sin resolución de alias
por similitud (grep de términos de fuzzy-matching → 0); candidato aislado +
swap reusando `integrate_barrido2._replace_with_rollback` (no reimplementado);
`fcntl.flock` sobre `.alta-relacion.lock`.

La prueba de rollback (`test_fallo_tardio_no_deja_tablas_adelantadas`) se
corrió en vivo — **5/5 tests PASSED** en `test_alta_relacion.py` — y su
sub-caso más fuerte fuerza el fallo de revalidación **después** de que
`os.replace` ya escribió en disco real, confirmando restauración
byte-idéntica de las 4 tablas. Es rollback genuino, no un test que aborta
antes de tocar nada.

## Frente E (`54a1b70`) — detalle

Las 7 verificaciones del plan se confirmaron, incluida la regla central del
ajuste: ningún `Path(None)` es alcanzable (grep exhaustivo de todos los
`Path(...)` del archivo, cada uno con su chequeo `is None` precedente
identificado por línea), y `RAIZ_NO_CONFIGURADA` nunca colapsa con
`ARCHIVO_NO_EXISTE` (esta última solo alcanzable vía `open_local_object`,
que nunca se invoca cuando la raíz no está configurada). `test_portabilidad_tres_raices`
corrió en vivo (PASSED) con las 4 aserciones pedidas verificadas leyendo el
cuerpo del test, no solo el resultado del runner. Los 6 fallos preexistentes
de `SemanticRunRegressionTests` en el mismo archivo se confirmaron
independientes de este commit (comparados contra el commit padre `ff68b9f`).

**Notas finas, sin desviación material**: (a) `row.get("raiz") or "data_raw"`
en vez de `row.get("raiz", "data_raw")` — equivalente en la práctica;
(b) el plan mencionaba el string literal `"NO_COINCIDE"`, que no existe en
`semantic_run.py` — la distinción de integridad rota vive en
`hash_reconcilia` (`"SI"`/`"NO"`/`"NO_VERIFICADO"`), conceptualmente
equivalente.

**Riesgo estructural a vigilar**: `test_portabilidad_tres_raices` reimplementa
por copia (no por llamada compartida) el mismo bloque `if/else` que vive
dentro de `execute()`. Hoy ambos bloques son idénticos carácter por
carácter — la prueba refleja fielmente el comportamiento actual — pero no
hay garantía estructural de que sigan sincronizados si alguien edita solo
una de las dos copias en el futuro.

## Frente D + FP-259 (`dbe26fb` + `5a84f88`) — detalle

Mecánicamente exacto: 0 diffs de `via_capa2.py`, `--vincula` no se
construyó (grep confirma 0 referencias), `relaciones.tsv`/`baseline.json`
sin tocar — consistente con la regla del ajuste ("D-sincronización solo
aplica si D escribió"). `tests/corpus.py::_indice_por_sha_y_raiz` implementa
exactamente la regla pedida (`presente_bajo_otra_raiz` solo si alguna
coincidencia declara raíz **distinta** a la que se barre; en cualquier otro
caso, incluida la misma raíz, `sin_registro`), con un test unitario nuevo
(`tests/test_corpus.py`) que ejercita esa frontera exacta y pasó en
ejecución real. El total de `C1` no cambió (37→37).

**Reserva de juicio, no de mecánica**: de las 137 filas `NO_DETERMINADO`,
60 mencionan un id real del manifiesto en su texto; el commit las excluyó
todas de "enlace nuevo resoluble", incluidas 4 filas ENFIH (N3, N10, N13,
N14) cuya `nota` cita literalmente `enfih2019_bd_csv_zip` — una entrada
real del manifiesto (`data/manifiesto.yaml:4102`, con `sha256` propio) —
como el payload de registro de esa fila. El argumento para excluirlas se
apoya en una frase de `GEMELAS-20` ("no cabía en este acto... sigue
necesitando vía propia") que describe un límite de **alcance de
herramienta**, no necesariamente un veredicto de que el enlace sea
inválido; no se documenta haber hecho la comprobación de bajo costo
(resolver `enfih2019_bd_csv_zip` contra disco real y contrastar contra el
resto de columnas de esas 4 filas) que habría zanjado la duda. Es, como
máximo, un posible falso negativo de 4 filas sobre 137 — no invalida la
conclusión general de "0 enlaces" para el resto, pero el razonamiento
específico para estas 4 filas queda documentado aquí como abierto, no como
cerrado. Ver FP-286.

## Confirmación independiente: el PARO de Frente D en PR #522 sí era falso positivo

`dbe26fb` (PR #525) afirma que el PARO declarado en PR #522 ("sin corpus
montado") fue un falso positivo: `git worktree add` no copia archivos
gitignorados (`data/raices.local.yaml`) ni symlinks creados a mano fuera
del índice de git (`data/raw`). Confirmado independientemente: ambos están
efectivamente en `.gitignore` (líneas 5-7), y la convención ya existía en
el propio repo (`.claude/commands/adquiere.md`: "un worktree fresco siempre
nace sin él -- no es PARO"). No es una racionalización ad hoc.

## Veredicto general

El plan se cumplió con alta fidelidad en sus cinco frentes. Cero
regresiones materiales (`tests/check.py --baseline` VERDE en todo el
historial). Las únicas dos desviaciones reales — ausencia de tests
automatizados para Frente A/B, y la reserva de juicio sobre las 4 filas
ENFIH de Frente D — quedan registradas como FP-285 y FP-286 en
`forense/firmas-pendientes.tsv` para decisión de mesa; ninguna de las dos
bloquea lo ya fusionado.
