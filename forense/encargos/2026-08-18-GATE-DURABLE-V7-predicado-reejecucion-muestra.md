# ENCARGO · ACTO GATE-DURABLE-V7 — el predicado, la reejecución y la muestra que faltaba

**SHA de redacción:** `3e4c9f7` (`origin/main`) · rama del acto anterior `acto-b2-v7` = `6b6d43a` (`PR #255`, sin fusionar al redactar)
**Entorno asignado:** UBUNTU, worktree `/home/pc0/Modelado-Mexicano-barrido2`. NO en la nube: necesita `.barrido2/` (~19 GB) y el corpus, que no están en ningún remoto.
**Estado:** VIVO — **PARO en el ARRANQUE 1**, verificado el 18/ago/2026: `PR #255` sigue `OPEN` (`mergedAt: null`, `mergeCommit: null`), y el propio encargo ordena parar en ese caso. De este encargo se ejecutó **únicamente su `COMMIT 0`**, y sobre la rama de `#255` en vez de sobre rama nueva — desviación de secuencia declarada en `ADR-98` (enmienda in situ) y en la §7 de `forense/notas/2026-08-18-b2-v7.md`, forzada por una dependencia circular: `#255` no podía fusionar porque su CI fallaba por las dos entradas que ese `COMMIT 0` arregla, y este encargo exige `#255` fusionado para arrancar. El resto (`COMMIT 1` a `COMMIT 4`) queda sin ejecutar, esperando la fusión.
**Autoriza (D-2, mesa, al lanzar):** editar `tools/curador_registro/barrido2_material.py` sabiendo que invalida los 672 expedientes (`MATERIAL_BUILD_SHA256`) y exige re-corrida de olas (~67 min) + W0 + material.

> Archivado bajo A.3 por la sesión a la que se lanzó. Texto verbatim; lo único añadido es esta cabecera y la marca de estado.

---

## Texto verbatim del encargo

SHA de redacción: 3e4c9f7 (origin/main) · rama del acto anterior acto-b2-v7 = 6b6d43a (PR #255, sin fusionar al redactar) Entorno asignado: UBUNTU, worktree /home/pc0/Modelado-Mexicano-barrido2. Es la continuación natural de la sesión de barrido. NO lo lances en la nube: necesita .barrido2/ (~19 GB) y el corpus, que no están en ningún remoto. Estado: VIVO Autoriza (D-2, mesa, al lanzar): editar tools/curador_registro/barrido2_material.py sabiendo que invalida los 672 expedientes (MATERIAL_BUILD_SHA256) y exige re-corrida de olas (~67 min) + W0 + material.

════════ ARRANQUE ════════
1 · REPO. El worktree existente. git fetch origin --prune. Reporta ruta · git log -1 · git status --short. Si PR #255 ya fusionó: arranca rama nueva desde origin/main (git worktree o branch local gate-durable-v7). Si #255 NO ha fusionado: PARA y repórtalo — mesa fusiona primero; este acto no continúa el PR cerrado de otro.
2 · SHA. Compara contra el que declara este encargo; si main se movió, re-deriva y reporta antes de editar.
3 · .barrido2/ + corpus. Reporta crudo: du -sh .barrido2/ · ls .barrido2/private/t0/snapshot-v4.json .barrido2/private/t0/ledger-v7.tsv · ls -d .barrido2/tasks-v7 .barrido2/staging-v7 · ls data/raw/ | head -3. Si snapshot-v4 no está o solo hay v2: PARO.
4 · ENTORNO (A.2, tres partes): CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE crudo · sonda INEGI (curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/, nunca -I) · ls data/raw/ | head -1. Firma esperada: sin_variable + 200 + corpus montado.
5 · ESPEJO. Toda cifra sale del worktree con comando a la vista. Red cero durante apertura de material (unshare -Urn, §6 del encargo madre, sigue vigente).
════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe ═══
Estructura. Gobiernan: tools/curador_registro/barrido2_material.py (escritor+validador, predicado único exento_estructural() en :283), el contrato data/curacion-universo/contrato-barrido2-v1_0.json, el ledger v7 y los productos durables de data/curacion-universo/. Este acto escribe todos ellos. NO escribe: tests/check.py ni integrate_barrido2.py (carril de cloud, ACTO INTEGRATE-T23, corre en paralelo — cero archivos en común), ni forense/firmas-pendientes.tsv. Contenido, derivado contra 3e4c9f7:

Arreglo del eje durable: NO-ENCONTRADO — exento_estructural() solo cubre nombre/hoja/tabla (estructural); value_labels/definicion (durable) se evalúan con los 11 patrones completos.
Diagnóstico ya hecho, no lo repitas: forense/notas/2026-08-18-b2-v7.md §4 — una sola cláusula falla (matches_task), E2_PII_NO_REDACTADA ×13,953, tres fuentes, todas metadato de máquina, cero PII real, verificado campo por campo y patrón por patrón.
Muestra adversarial: las 41 tareas selladas son de ledger-v2/-v3 (snapshot-v2); 0 existen en v7. EXISTE-NO-SATISFACE — re-sortear, no re-hashear.
La doctrina de exención ya escrita en el propio módulo (:73-95): "la exención no es por clase de patrón sino por FORMA DE LA CADENA", con el precedente de los 44 nombres reales de candidatos en los .dta electorales de Veracruz que la motivan. El arreglo la extiende, no la contradice. Cobertura retroactiva. El validador durable nació dentro del bloque 2 (17-18/ago); todo lo anterior nunca pasó por él.
═══════════════════════════

PERÍMETRO. tools/curador_registro/barrido2_material.py + tools/curador_registro/tests/ · .barrido2/** (fuera del repo) · data/curacion-universo/** · data/censo-explotacion-*.tsv · canon/gobernanza-v1_15.md (ADR) · canon/estado-programa-v1_10.md solo :27/:101 (cascada de conteo de ADR — ⚠️ es FP-48: cláusula por cláusula en cualquier merge) · forense/notas/ · forense/hallazgos.md (append) · forense/encargos/. Paralelo: INTEGRATE-T23 en cloud toca integrate_barrido2.py + tests/check.py — disjunto; la colisión de número de ADR entre los dos actos es esperada: re-deriva al fusionar, renumera, dilo (protocolo usado cinco veces). 🚫 No corras --freeze. Si el CI sale rojo, desglose por test y sigue.

COMMIT 0 · La cascada que #255 dejó redactada

Las dos entradas rojas de la línea base tienen una sola causa declarada: estado-programa:27/:101 citan 97 ADR y gobernanza tiene 98. Las dos líneas ya están redactadas en forense/notas/2026-08-18-b2-v7.md §7 — escríbelas tal cual. python3 tests/check.py --baseline debe quedar VERDE. Si no queda, algo más cambió: repórtalo antes de seguir.

COMMIT 1 · El arreglo, con la forma que el módulo ya declaró

El problema: en los campos durables (value_labels, definicion) viven cadenas compuestas de metadato de máquina — codigo_hex=3120202020202020;label=Sí, crc=2719796586;zip_slip=NO — y los patrones 3 (teléfono: (?:\+?52[ -]?)?(?:\d[ -]?){10}) y 5 (\d{11,18}) disparan sobre el checksum y el hex.

El diseño, y no otro: exención por segmento con llave declarada, lista cerrada — codigo_hex=, crc=, zip_slip=, y las demás llaves de máquina que el propio escritor emite (derívalas del código, no las inventes). Un segmento cuya llave está en la lista y cuyo valor tiene forma de código queda exento de los patrones de identificador numérico; el segmento label= y cualquier texto libre siguen evaluándose con los once patrones, siempre. Todo dentro del predicado único que escritor y validador comparten — separarlos ya costó una reejecución (399 de 672), está escrito en el docstring de exento_estructural().

Controles obligatorios antes de tocar el índice real — pega la salida cruda de cada uno:

    #    entrada    debe
    P1    crc=2719796586;zip_slip=NO    sobrevivir entero
    P2    codigo_hex=0000000000c05840;label=Sí    sobrevivir entero
    N1    label=RAÚL GONZÁLEZ GARCÍA    redactarse (el precedente Veracruz)
    N2    codigo_hex=abc;label=555 812 4930    redactar el label=, conservar la llave
    N3    8711234567 suelto, sin llave declarada    redactarse
    N4    telefono_contacto=8711234567 (llave NO declarada)    redactarse — la lista es cerrada

Luego, contra el índice real: el conteo de activaciones por campo/patrón que la nota §4 derivó debe caer a cero en las tres fuentes de máquina y solo en ellas. Si cae algo más, el arreglo se pasó: PARA.

COMMIT 2 · La reejecución completa, en este orden y no en otro

Congela el sha nuevo de barrido2_material.py y decláralo: es el MATERIAL_BUILD_SHA256 de la generación.
Olas con tools/curador_registro/correr-olas-v7.py (ya archivado, sha probado) — ~67 min, espera 672/672.
Segundo --barrido2-materialize CON --staging-root (sin él: LEDGER_NO_TERMINAL).
Gate validate.py --barrido2-material --require-complete: espera 672 terminal · PII 0 · rc=0. Córrelo primero contra 3-4 expedientes (remedio de método) y luego completo.
W0 antes que material. 6. Material. 7. Productos durables + baseline-material-barrido2.json congelado + PRISMA reconciliado. Respaldo del ledger antes de cada paso destructivo, como hizo el acto anterior (.pre-mat2.bak con sha).

COMMIT 3 · La muestra adversarial, ahora sí contra lo sellado

Solo después del build nuevo — sortearla antes era repetir el defecto 1.0-vs-1.1. Por ola, §12 del encargo madre: max(3, ceil(5%)), tope 20 (con 26·246·396·4 ≈ 3+13+20+3; si una ola tiene <3, todas). Semilla declarada y lista congelada en un commit ANTES de re-inspeccionar (patrón COMMIT A/B). Re-inspección independiente, comparación por hash, veredicto escrito — incluidas las prioridades del §12 (primer lote por inspector, excepciones, promociones). Cierra la exigencia 4 del §15. Si una evidencia no coincide: el protocolo del §12 (cuarentena, ampliar, repetir lote), no el pánico.

COMMIT 4 · Cierre

ADR (re-deriva el número al escribirlo, espera colisión con el carril de cloud) · cascada :27/:101 · nota del acto con: los conteos antes/después del gate, la tabla de la adversarial, y el delta 17→19 de INDEXADO-NO-DESCARGADO derivado (¿las 2 extra son de M-APERTURA o de otra cosa? — es lectura del relaciones.tsv, barato, y la fase semántica lo necesita sabido) · línea en hallazgos.md · encargo CONSUMIDO.

Módulo de auditoría — lo aplicable: contadores de medición sobre México: cero, dilo en una línea. Contadores de aparato que sí mueve: gate 296→672 terminal esperado, PII falsos 13,953→0, adversarial 0/41 inválida → n/n contra build sellado, exigencia §15.4 de insatisfecha a satisfecha. Ninguna cifra tecleada: todo con comando.

Lo que NO hace: no toca integrate_barrido2.py ni tests/check.py (cloud) · no arranca C4-semántico/C5/C6 · no corrige capa 4 de las 17 (vía §19) · no cierra FP-47/48 · no congela.
