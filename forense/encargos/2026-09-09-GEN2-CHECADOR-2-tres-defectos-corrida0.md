# ENCARGO · ACTO GEN2-CHECADOR-2 · TRES DEFECTOS MEDIDOS DEL MISMO APARATO, UN LOTE — el contexto que caduca por diseño, la fotocopiadora armada, y el detector que confunde «ausente» con «no lo veo»

**SHA de redacción:** `351fd25f` — `origin/main` al momento de redactar. Al arrancar este acto `origin/main` había avanzado a `c5b89a9` (9 commits: cascada de `GEN2-SONDA-3 · ESCALAMIENTO-LATERAL`, `ADR-418`, ficha `GEN2-RETRO-SELLO-SONDA-CAJA-1`). Ninguno de esos 9 commits toca `tools/corrida0.py`, `tests/test_corrida0.py`, `forense/firmas-pendientes.tsv` ni `forense/no-corrido.tsv` en las filas que este acto usa (verificado: `git diff --stat 351fd25f origin/main -- tools/corrida0.py tests/test_corrida0.py` → vacío) — sin divergencia sobre el perímetro de este acto, sin merge necesario.
**Entorno asignado:** NUBE, Opus (rediseño acotado de herramienta con falsadores; cero microdato) · COMPUERTA: ninguna.
**Estado:** VIVO

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2)

Comprobado contra `origin/main` vigente (`c5b89a9`) al arrancar:

- `tools/corrida0.py::_evalua_contexto`, `::status`, `::registro`, `::preflight` → existen (`grep -n "^def " tools/corrida0.py`).
- `FP-358`, `FP-359` → existen en `forense/firmas-pendientes.tsv`, estado `ABIERTA`, ambas citando `forense/encargos/2026-09-08-GEN2-E5-1-VERIFICADOR-CALC0003V2-FIRMA.md` como origen.
- `FP-352` → existe en `forense/firmas-pendientes.tsv`, estado `ABIERTA` (`PROPUESTA`), citando `forense/notas/2026-09-08-codebooks-abiertos-y-specs-congeladas.md §6` y `forense/encargos/2026-09-08-GEN2-E5-0-SPECS-EJECUTABLES.md`.
- `NC-0051` (FP-358) y `NC-0052` (FP-359) → existen en `forense/no-corrido.tsv`, `estado=ABIERTA`, sucesor citado como decisión de diseño de mesa.
- `ADR-410` → existe en `canon/gobernanza-v1_15.md` (línea 7127), procedimiento recomendado «simula la firma de mesa EN MEMORIA, sin escribir nada» para `ACTO GEN2-E5 · CALC-0001..0003`.
- `data/corrida0/CALC-0001`, `CALC-0002`, `CALC-0003-v2` → existen, sellados (`ejecucion.json`/`resultados.json`/`sello.json`/`sello.sha256`).
- Cobertura retroactiva: `forense/firmas-pendientes.tsv` (filas `FP-352`, `FP-358`, `FP-359` completas, no solo el id) y `forense/encargos/2026-09-08-GEN2-E5-1-VERIFICADOR-CALC0003V2-FIRMA.md` (las tres filas de `## NO-CORRIDO / RESERVAS` que citan estas tres FP) leídas completas antes de tocar código.

---

FIRMA DE MESA, verbatim del 8/sep/2026: «Reparación en 1 lote.» — resuelve FP-358, FP-359 y FP-352 en un solo acto D-11.

PIEZAS (cada una con su falsador; los tres defectos ya están medidos con control positivo en las propias FP — pegarlos como casos de test, no re-descubrirlos)

P1 · FP-358 — el contexto compara identidad, no calendario. `_evalua_contexto` deja de comparar `git rev-parse HEAD` contra el commit del sello. `CONTEXTO=IDENTICO` pasa a derivarse de lo que identifica la corrida: blob del medidor + sha de spec.yaml + dependencias declaradas + firma material del entorno — si nada de eso cambió, el contexto ES idéntico aunque hayan caído cien commits ajenos. El commit se conserva como dato informativo, no como criterio. Falsador con el control positivo medido en FP-358: mismo CALC, un commit ajeno después → antes REPLICA-RESULTADO·commit_distinto, ahora REPRODUCE·IDENTICO; y un caso donde el blob del medidor SÍ cambió → DISTINTO con razón `codigo_distinto`. Re-correr verify sobre CALC-0001/0002/0003-v2 y pegar la tabla: esperado REPRODUCE·IDENTICO pleno por primera vez sobre corridas viejas.

P2 · FP-359 — la fotocopiadora se desarma. `status` pasa a lectura pura (deriva en memoria, no escribe TSV); `registro` solo escribe con bandera explícita (`--escribe`), y sin ella imprime el diff que escribiría. La recomendación de `ADR-410` («simula la firma en memoria») queda CORREGIDA en la nota con la cita: la simulación que escribe está prohibida; el control positivo de cableado se hace contra copia temporal fuera del árbol. Falsador: correr `status` dos veces y verificar cero bytes cambiados en los tres TSV (hash antes/después); y `registro` sin bandera → cero escritura.

P3 · FP-352 — el detector aprende la diferencia. `preflight` distingue `input_manifiesto_AUSENTE` (la raíz resuelve y el archivo no está) de `NO-VISIBLE-EN-ESTE-CONTEXTO` (la raíz lógica no resuelve desde este proceso — el caso sandbox//mnt/c). El segundo NO es BLOQUEADO: es aviso con la instrucción de correr fuera del sandbox. Falsador simulando raíz no-resoluble por variable de entorno. Más una línea al runbook de caja documentando el rodeo ya en uso (E5 corrió así, declarado).

P4 · Registro. FP-358/359/352 → EJECUTADAS con la firma; NC de reserva de E5-1 que dependan de estas piezas se actualizan con cita, no se cierran de más.

PERÍMETRO: `tools/corrida0.py` (solo `_evalua_contexto`, `status`, `registro`, `preflight`) · `tests/test_corrida0.py` (falsadores nuevos) · runbook de caja (una línea) · `forense/{firmas-pendientes,no-corrido}.tsv` · nota · 0-bis · cascada. No toca sellos, CALC, `decisiones.tsv`, specs ni T35. Si escribes fuera de la lista, PARA. CONTADOR: cero GEN2 — aparato declarado, pagado: tres defectos reales medidos, dos de ellos capaces de publicar una firma falsa o de negarle REPRODUCE a una corrida correcta para siempre.

## NO-CORRIDO / RESERVAS obligatoria.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| **P1 · «Re-correr verify sobre CALC-0001/0002/0003-v2 y pegar la tabla: esperado REPRODUCE·IDENTICO pleno por primera vez sobre corridas viejas»** | `PARO-ENTORNO`. Re-corrido de verdad, en NUBE: las tres corridas confirman que `commit_distinto`/`commit_no_verificable` YA NO aparecen en ningún `razon:` (el defecto de `FP-358` está reparado) pero ninguna llega a `REPRODUCE · IDENTICO` — `CALC-0001`/`CALC-0002` salen `NO-VERIFICABLE` (`input_no_verificable=...:RAIZ_NO_CONFIGURADA`, `descargas_mx`/`data_raw` no montados en NUBE) y las tres traen además `dependencias_distintas` (`numpy`/`pandas`/`scipy` `AUSENTE` en NUBE contra la versión real al sellar) y `RESULT: NO-EJECUTABLE` (`ModuleNotFoundError: No module named 'numpy'`). Las tres causas son AJENAS a `FP-358`/`FP-359`/`FP-352` y a este acto, que declara cero microdato. | `verify REPRODUCE · IDENTICO` sobre las tres corridas reales sigue sin demostrarse punta a punta. Lo que SÍ queda probado, aislado y con control positivo verificable sin microdato (`T-VERIFY-CONTEXTO-FP358`), es exactamente el eje que `FP-358` pedía: el commit deja de gatear. | `NC-0061`. CAJA (worktree con corpus montado + `numpy`/`pandas`/`scipy` instalados) — `SIN-ASIGNAR` de acto puntual. |
