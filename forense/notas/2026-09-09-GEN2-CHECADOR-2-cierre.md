# ACTO GEN2-CHECADOR-2 · TRES-DEFECTOS-CORRIDA0 — nota de cierre

**Encargo:** `forense/encargos/2026-09-09-GEN2-CHECADOR-2-tres-defectos-corrida0.md`
(archivado verbatim en `9e481ae`). **Entorno:** NUBE, Opus, cero microdato.
**Perímetro:** `tools/corrida0.py` (solo `_evalua_contexto`, `status`, `registro`,
`preflight`) · `tests/test_corrida0.py` (falsadores nuevos) · `forense/runbook-caja.md`
(nuevo, una pieza) · `forense/{firmas-pendientes,no-corrido}.tsv` · esta nota · el
0-bis · la cascada (incluye `tests/check.py::_T25_ARCHIVOS_CONOCIDOS`, mecánico,
igual que en todos los actos anteriores de esta serie).

Firma de mesa citada por el encargo, verbatim del 8/sep/2026: «Reparación en 1
lote.» — resuelve `FP-358`, `FP-359` y `FP-352` en un solo acto D-11.

---

## P1 · FP-358 — el contexto compara identidad, no calendario

`_evalua_contexto` dejó de comparar `git rev-parse HEAD` de hoy contra
`ejecucion.json.git_commit`. El commit se sigue calculando y reportando (línea
`[4/5 CONTEXTO] ... commit_informativo=... (FP-358: no gatea)`) pero ya no entra
a `razones_contexto` ni fuerza `NO-VERIFICABLE`: lo que identifica la corrida
sigue siendo el blob del medidor (`script_blob_sha256`), el `spec.yaml`, los
inputs, los parámetros/seed y las dependencias materiales declaradas por el
CALC (`dependencias_materiales_calc`) — nada de eso depende de cuántos commits
ajenos cayeron después del sello.

**Falsadores nuevos** (`tests/test_corrida0.py`):
- `T-VERIFY-CONTEXTO-FP358` — mismo control positivo medido en `FP-358` sobre
  `CALC-0003-v2`: un CALC sellado con `git_commit` distinto del `HEAD` de hoy
  (todo lo demás igual) da `CONTEXTO=IDENTICO`, sin razón alguna. Antes de este
  acto habría dado `DISTINTO` con razón `commit_distinto`, y `verify` lo habría
  degradado a `REPLICA-RESULTADO · CONTEXTO-DISTINTO`.
- `T-VERIFY-CONTEXTO-FP358-CODIGO` — el otro lado: si el blob del medidor SÍ
  cambió, `CONTEXTO` sigue `DISTINTO`, con razón `codigo_distinto` (renombrada
  desde `script_cambiado`, para que la razón nombre lo que cambió — el código —
  y no quede pegada al nombre de una variable interna vieja).

**Re-corrido `verify` sobre las tres corridas reales, en NUBE** (esta sesión,
`python3 tools/corrida0.py verify <CALC>`):

| CALC | `razon:` (extracto) | ¿aparece `commit_distinto`/`commit_no_verificable`? |
|---|---|---|
| `CALC-0001` | `input_no_verificable=...:RAIZ_NO_CONFIGURADA` (×3) · `dependencias_distintas` | **NO** |
| `CALC-0002` | `input_no_verificable=...:RAIZ_NO_CONFIGURADA` (×3) · `dependencias_distintas` | **NO** |
| `CALC-0003-v2` | `input_cambiado=ennvih1_2002_hogar_dta` · `input_cambiado=ennvih1_2002_ponderador` · `dependencias_distintas` | **NO** |

Antes de este acto, las tres habrían traído además `commit_distinto` (los
12/12 sellados del árbol tienen `git_commit != HEAD` de hoy, medido en
`FP-358`) — eso ya no ocurre en ninguna. Lo que SÍ sigue apareciendo —
`RAIZ_NO_CONFIGURADA` (`descargas_mx`/`data_raw` no montados en NUBE) y
`dependencias_distintas` (`numpy`/`pandas`/`scipy` `AUSENTE` aquí contra la
versión real que quedó sellada) — es **ajeno a `FP-358`**: son exactamente las
dos cosas que este acto declara no tocar («cero microdato», NUBE sin corpus).
Con ellas presentes, ninguna de las tres puede llegar hoy a
`REPRODUCE · IDENTICO` completo — **`NC-0062`**, sucesor CAJA (ver
`## NO-CORRIDO / RESERVAS` del encargo archivado). Lo que este acto SÍ prueba,
aislado y con control positivo verificable sin microdato, es exactamente lo que
`FP-358` pedía: el eje commit deja de gatear.

`NC-0051` (la reserva de diseño que `GEN2-E5-1` dejó abierta para esta FP)
→ **CERRADA**, citando este acto.

---

## P2 · FP-359 — la fotocopiadora se desarma

`registro(escribe=False, ...)` es ahora el valor por defecto (antes
`escribe=True`). Escribir las tres vistas (`corridas.tsv`, `resultados.tsv`,
`usos.tsv`) exige el `True` explícito — en la CLI, la bandera `--escribe`
reemplaza a `--seco` (que invertía el sentido: antes había que pedir
explícitamente *no* escribir). Sin la bandera, `registro` deriva, valida e
imprime el **diff** que escribiría (`_texto_vista`/`_imprime_diff_vista`,
`difflib.unified_diff` contra el archivo real en disco, o contra `""` si el
archivo todavía no existe) — nunca toca un TSV. `status` ya derivaba en
memoria vía `_filas_registro` desde `ACTO GEN2-E6` (confirmado con falsador,
sin cambio de código: no llama a `registro()` ni a `_escribe`).

**Corrección de `ADR-410`, con la cita.** El procedimiento que `ADR-410`
documentó como recomendado — «Control positivo con la firma **simulada en
memoria y nada escrito en disco**» (`canon/gobernanza-v1_15.md`, entrada
`ADR-410 · ACTO GEN2-E5 · CALC-0001..0003`) — **SÍ escribía**, porque
`registro()` escribía por defecto y `status`/el control positivo no tenían
forma de evitarlo sin pasar por ahí (`FP-359`, medido por `GEN2-E5-1`: el
commit de cascada `d598210` publicó `cuenta_gen2=SI`/«FIRMA SIMULADA» en las
tres vistas derivadas, sin que mesa hubiera firmado nada). **Queda corregido
hacia adelante, aquí:** la simulación que escribe queda PROHIBIDA tal como
`ADR-410` la describió; el control positivo de cableado — probar que la
canalización completa (demanda+oferta → tres vistas → contadores) reacciona
correctamente a una firma — se hace contra una **copia temporal fuera del
árbol** (exactamente el patrón que ya usan `t_registro_punta_a_punta` y el
falsador nuevo de abajo: `C.VISTA_CORRIDAS`/`VISTA_RESULTADOS`/`VISTA_USOS`
apuntados a un directorio temporal, nunca a `data/corrida0/`), o -- si de
verdad hace falta simular sobre el árbol real -- se usa `registro()` sin
`escribe=True`, que ahora sí es un modo que garantiza cero escritura.

**Falsador nuevo:** `T-FOTOCOPIADORA` — `status()` corrido dos veces deja cero
bytes cambiados (hash antes/después, vía `_sha256_archivo`) en los tres TSV;
`registro()` sin `escribe=True` (el default nuevo) también deja cero bytes;
`registro(escribe=True)`, como control positivo, SÍ los cambia — para que el
falsador no sea vacuo.

`NC-0052` (la reserva de la trampa de `ADR-410`) → **CERRADA**, citando este
acto.

---

## P3 · FP-352 — el detector aprende la diferencia

`preflight` distingue ahora dos `AUSENTE` de manifiesto muy distintos, para
todo input con `raiz_logica` **configurada** (a diferencia del caso ya cubierto
por `T-MANIFIESTO-AUSENTE-BLOQUEA`, un id que ni siquiera está en el
manifiesto, donde `raiz_logica` sale `None` y el bloqueo real no cambia):

- **`input_manifiesto_AUSENTE`** — la raíz física SÍ resuelve (existe como
  directorio desde este proceso) y el archivo simplemente no está ahí. Sigue
  BLOQUEANDO preflight, sin cambio.
- **`input_manifiesto_NO-VISIBLE-EN-ESTE-CONTEXTO`** (nueva) — la raíz lógica
  está configurada, pero su raíz física **no resuelve desde este proceso** (el
  caso medido en `FP-352`: `/mnt/c` es invisible dentro del sandbox de Bash de
  Claude Code). Esto ya **no bloquea**: sale como AVISO, con instrucción de
  correr fuera del sandbox.

La distinción se calcula dentro de `preflight` mismo (perímetro: solo esa
función), reutilizando `payload_resolver.M.resolver_raiz` — ya importado por
`corrida0.py` como `_PR.M` — para re-derivar la raíz física del `raiz_logica`
de cada entrada `AUSENTE` y comprobar si esa ruta existe como directorio
*ahora mismo*; no se tocó `tests/payload_resolver.py` ni `tests/manifiesto.py`.

**Falsador nuevo:** `T-PREFLIGHT-FP352` — mockea `resolver_payload`/
`resolver_raiz` (mismo patrón que `T-SNAPSHOT-INPUT-UNICO`, sin tocar disco
real ni `/mnt/c`) para los dos lados: raíz física que no resuelve → aviso, no
bloqueo; raíz física que sí resuelve (directorio temporal real) con el archivo
ausente → sigue bloqueando. Los dos casos son necesarios: el primero prueba
que el fix corrige el falso positivo, el segundo que no se volvió ciego al
caso real.

**Runbook de caja** (`forense/runbook-caja.md`, nuevo — no existía ninguno con
ese nombre en el árbol; búsqueda exhaustiva antes de crearlo, declarada):
una línea documentando el rodeo ya en uso — `dangerouslyDisableSandbox: true`
(parámetro del tool `Bash` de Claude Code) para que `/mnt/c` sea visible,
declarado ya por `ACTO GEN2-E5` (`ADR-410`, «Todo `run`/`verify` corrió fuera
del sandbox») y por `ACTO GEN2-SONDA-CAJA-1`
(`forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md`: «Todas las sondas de red de
este acto se ejecutaron con `dangerouslyDisableSandbox`»). Si mesa ya tenía en
mente otro archivo con ese nombre, este puede fusionarse ahí — declarado como
decisión de este acto, no oculto.

---

## P4 · Registro

`FP-352`, `FP-358`, `FP-359` → `EJECUTADA` en `forense/firmas-pendientes.tsv`,
citando este acto (`ACTO GEN2-CHECADOR-2`, PR pendiente al momento de este
commit — se completa en `## CONSUMIDO`). `NC-0051` (FP-358) y `NC-0052`
(FP-359), las dos reservas de `GEN2-E5-1` que dependían de estas piezas,
quedan `CERRADA` con la misma cita. Una reserva nueva se abre, no se cierra de
más: `NC-0062` — la tabla `REPRODUCE · IDENTICO` plena sobre las tres corridas
reales, que este acto no puede producir desde NUBE (perímetro propio: cero
microdato) y que queda para un acto en CAJA con corpus montado y
`numpy`/`pandas`/`scipy` instalados.

---

## Suite

`python3 tests/test_corrida0.py` → `68 casos · 68 ok · 0 FALLOS` (64 previos +
4 falsadores nuevos, cero regresiones). `python3 tests/check.py --baseline` →
`LÍNEA BASE: VERDE` (3 FAIL preexistentes, sin ninguno nuevo; el único WARN/FAIL
nuevo que apareció al escribir el 0-bis — `T25` sobre el rótulo pelado GEN2-E5
citado en el propio encargo verbatim — se resolvió como manda `/acto` §4.5: censando el archivo en
`tests/check.py::_T25_ARCHIVOS_CONOCIDOS`, sin editar el encargo).
