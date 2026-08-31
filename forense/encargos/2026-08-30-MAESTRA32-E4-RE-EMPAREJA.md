ENCARGO · ACTO MAESTRA32-E4 · RE-EMPAREJA

SHA de redacción: 19ace88 (main, merge PR #400 / ADR-228) · Redactado: 30/ago/2026, dirección maestra-32 · Instrucciones vigentes: v2.11 · Estado: LISTO PARA LANZAR — sin compuerta, sin ranuras. Es el sucesor que FP-186.gatea nombra ("el sucesor MAESTRA32-E4 (RE-EMPAREJA) sobre el universo ampliado") y que E2, E3 y E6 declararon; su rótulo estaba reservado desde el 28/ago.

ENTORNO ASIGNADO: NUBE (cloud_default). NO se lanza en UBUNTU — todo versionado: data/inventario-reactivos-v1_2.tsv, data/inventario-reactivos-ext-v1_0.tsv, data/inventario-fd-v1_1.tsv, forense/notas/2026-08-28-empareja-spec.md. No abre payloads, no mide.

CARRILES EN PARALELO (declarado): carril NUBE = E4 (este); carril CAJA = E12 · EXTRACTOR-FD (rama b). Compartidos: solo la cascada. Renumera quien fusiona segundo.

FIRMAS — ninguna nueva. Este acto ejecuta sucesores ya declarados y sellados

ADR-221 (E2: spec congelada), ADR-223 (E6: re-corrida por etiqueta reparada, 0 de 9 movimientos), ADR-228 (E3 v2: universo ampliado 316 → 439 de 720). A.10, corolario 1: los veredictos de E2/E6 quedan intactos como historia; este acto los re-sella sobre el universo nuevo.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

A.2, tercera parte: ls data/raw/ 2>/dev/null | head -1 — se espera ausente. Los TSV llevan cabecera #: sáltala antes de csv.DictReader. Búsquedas en Python UTF-8 (A.13). T03: rutas completas entre backticks.

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (maestra-32, 30/ago/2026, contra 19ace88) ═══

1 · ESTRUCTURA. Familia de inventarios (indexada desde ADR-221) + data/emparejamiento-motor-v1_0/v1_1.tsv. Verifica command grep -c "inventario" data/INFRAESTRUCTURA-v1_0.md ≥ 1 y reporta.

2 · CONTENIDO. (i) data/inventario-reactivos-ext-v1_0.tsv existe: 63,345 filas, mismo esquema de 9 columnas que v1_2 (verificado columna a columna hoy), 35 instrumentos etiquetados, 18,390 filas (sin-instrumento-derivable) (top: endireh2011/2016/2021/2006, envipe2025). (ii) data/emparejamiento-motor-v1_2.tsv: NO-ENCONTRADO (ls data | grep emparejamiento → solo v1_0, v1_1). (iii) La spec de E2: forense/notas/2026-08-28-empareja-spec.md existe, congelada, con la co-observación corregida ("exige instrumento identificado", ADR-221). (iv) El código de re-corrida de E6 vive solo dentro de forense/notas/2026-08-30-etiqueta-v1_2-cierre.md (bloque "Re-corrida VERBATIM de la especificación congelada de MAESTRA32-E2"; tools/ no lo tiene: 0 hits sobre 77+ archivos). (v) Estado de los 9 pares hoy: E2 0/9, E6 0/9 (6 EXISTE-NO-SATISFACE con media pareja nombrada, 3 NO-ENCONTRADO); G3.horizonte_temporal sigue FUERA (RUTA-I, ya en el ejecutable por ADR-225).

3 · COBERTURA RETROACTIVA. E2 (28/ago) y E6 (30/ago) corrieron sobre 316 payloads con filas; la tabla ext (30/ago, ADR-228) añade 123. Además: 18,390 filas de la tabla ext no tienen instrumento — la spec exige instrumento identificado para co-observación, así que esas filas solo pueden aportar candidatos EXISTE-NO-SATISFACE, nunca EXISTE-SATISFACE. Se declara aquí para que un "0 movimientos" no se lea como "la tabla ext no sirvió": el techo de etiqueta es propio y medible (a re-etiquetar por un sucesor si vale la pena).

═══════════════════════════════════════════════════════════════════

0-bis · A.3

Primer commit: este encargo verbatim en forense/encargos/2026-08-30-MAESTRA32-E4-RE-EMPAREJA.md. Al cerrar, ## CONSUMIDO con el PR.

Objeto

Re-correr la spec congelada de E2 verbatim sobre el universo ampliado: tabla de reactivos = v1_2 ∪ ext-v1_0 (mismo esquema; se concatenan como filas adicionales, sin deduplicar por diseño — un mismo payload_id no aparece en ambas), tabla FD = v1_1. Reportar deltas por par contra v1_1.

COMMIT-1 — congela ANTES de correr

forense/notas/2026-08-30-reempareja-spec.md: (a) universo exacto: las tres tablas con sus conteos re-derivados por comando; regla de concatenación; (b) cero cambios a términos, regex, criterios de candidato, circularidad y prioridad de E2 — cita la spec archivo:sección; (c) elevación del código: el bloque de re-corrida de E6 se copia a tools/reempareja.py con la cita a la nota de origen, y la única edición permitida es leer una tabla más — se declara el diff; (d) B-bis, antes de ver el dato: los veredictos solo pueden subir o quedarse (un universo más grande no quita coincidencias; si alguno baja, es bug y PARO); 0 movimientos = informativo, con el techo de etiqueta de la tabla ext cuantificado; ≥1 EXISTE-SATISFACE = habilita un medidor de caja sucesor (no este acto). Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

COMMIT-2 — corrida única

data/emparejamiento-motor-v1_2.tsv (mismo esquema que v1_1), tabla de deltas por par (v1_1 → v1_2, universo declarado), y forense/notas/2026-08-30-reempareja-cierre.md con A.13 en todo conteo: filas examinadas por tabla, candidatos nuevos por par y por tabla de origen (v1_2 vs ext), cuántos candidatos de ext caen en filas sin instrumento. Intocables con git diff --stat vacío: emparejamiento-motor-v1_0/v1_1.tsv, los tres inventarios, la spec de E2, tools/etiqueta_v1_2.py, tools/inventario_reactivos_ext.py.

PERÍMETRO Y CONCURRENCIA

Archivos: forense/encargos/2026-08-30-MAESTRA32-E4-RE-EMPAREJA.md · forense/notas/2026-08-30-reempareja-spec.md · forense/notas/2026-08-30-reempareja-cierre.md · tools/reempareja.py (nuevo) · data/emparejamiento-motor-v1_2.tsv (nuevo) · forense/firmas-pendientes.tsv (fila nueva de recibo) · cascada. No toca milpa/**, inventarios, la spec de E2, procedencia.yaml. Concurrencia: E12 en caja en paralelo. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

FP pre-asignadas

FP-187–FP-188 (máximo hoy FP-186; re-deriva; siguiente libre si están tomadas, declarado).

ADR y cascada

Candidato re-derivado (deriva, no heredes; renumera quien fusiona segundo). El ADR declara el re-sello por universo ampliado (A.10), los deltas, y el techo de etiqueta de ext. registro-rotulos: MAESTRA32-E4 censado (token pelado E4 colisiona con MAESTRA31-E4 — se censa, no se reclama). T25.

CONTADOR

Pares con EXISTE-SATISFACE nuevo: N de 9 (incluido cero) · candidatos nuevos aportados por la tabla ext.

Lo que este acto NO hace

No mide, no edita rutas, no re-etiqueta la tabla ext (si el techo de etiqueta resulta decisivo, se declara como sucesor), no toca G3.horizonte_temporal.

Sucesores declarados, no lanzados

Medidor de caja por cada EXISTE-SATISFACE nuevo · ETIQUETA-ext si ≥1 candidato dominante cae en fila sin instrumento.

## CONSUMIDO

Ejecutado en la rama `claude/maestra32-e4-re-empareja-61n9iu`. [PR #402](https://github.com/Josanoforo/Modelado-Mexicano/pull/402) (abierto desde la interfaz de Claude Code tras el push de esta sesión, no por esta sesión). Resultado: re-corrida VERBATIM de la spec congelada de `MAESTRA32-E2` (`forense/notas/2026-08-28-empareja-spec.md`) sobre el universo ampliado `data/inventario-reactivos-v1_2.tsv` ∪ `data/inventario-reactivos-ext-v1_0.tsv` (`ADR-228`) + `data/inventario-fd-v1_1.tsv` (258685 filas examinadas, A.13) — `tools/reempareja.py` nuevo (única edición: leer una tabla más, elevado desde el bloque de re-corrida de `MAESTRA32-E6`). `data/emparejamiento-motor-v1_2.tsv`: **2 de 9** `EXISTE-SATISFACE` nuevo (`G5.familismo_apoyo` co-observado en `eder2017`/`endireh2016`; `G5.radio_confianza` co-observado en `endireh2016`), 2 pares suben de `NO-ENCONTRADO` a `EXISTE-NO-SATISFACE`, 5 quedan iguales, **0 regresiones** frente a `v1_1` (B-bis pre-registrado verificado, sin PARO). 481 candidatos nuevos, todos de la tabla ext (control positivo: 0 nuevos/perdidos de `v1_2`/`fd-v1_1`); 284 de esos 481 (59.0%) caen en filas sin instrumento, techo de etiqueta cuantificado por par. Reserva declarada, no bloqueante, sobre `G5.radio_confianza`: la co-observación en `endireh2016` usa un ítem que lee como confianza institucional, homónimo probable de radio de confianza interpersonal, sin cribar por `DESCARTES` (empareja por tupla exacta, no cubre filas nuevas de `ext`) — condiciona el medidor de caja sucesor declarado arriba, no bloquea este acto. `ADR-230` (renumerado de `ADR-229`: carril CAJA `MAESTRA32-E12 · EXTRACTOR-FD`, `PR #401`, candidateó el mismo número contra el mismo `main = 19ace88` sin ver este acto y fusionó primero; regla de la casa, renumera quien fusiona segundo); `FP-187` nueva en `forense/firmas-pendientes.tsv` (sin colisión — `E12` tomó `FP-189`); `MAESTRA32-E4` censado en `canon/registro-rotulos.tsv`; `tests/check.py --baseline` → LÍNEA BASE: VERDE, sin FAIL nuevo. Intocables verificados con `git diff --stat` vacío: `emparejamiento-motor-v1_0/v1_1.tsv`, los tres inventarios, la spec de E2, `tools/etiqueta_v1_2.py`, `tools/inventario_reactivos_ext.py`, `milpa/procedencia.yaml`. Detalle completo: `forense/notas/2026-08-30-reempareja-spec.md` (COMMIT-1) y `forense/notas/2026-08-30-reempareja-cierre.md` (COMMIT-2, A.13 completo, tabla de deltas, control positivo, salida cruda del script).
