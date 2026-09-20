# GEN2-LIMPIEZA-RAMAS-LOCALES-3 · cierre (P1–P4, tras el fix de P0)

Continuación, en la misma rama y el mismo PR (`#923`), del PARO-PREMISA documentado en
`forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-3-paro.md` — sellada por adenda de
dirección (20/sep/2026): el P0 duro era correcto según el texto del encargo, pero el remedio
(`git fetch --unshallow`, aditivo, 16 s) era seguro; se levantó y el acto continuó.

## Causa y arreglo (resumen; detalle completo en `hallazgos.md` y el commit `fix(check.py)`)

Confirmado con salida cruda: `tests/check.py::_t_cron_ref_censo` corría `git fetch --depth=100`
con `cwd=ROOT` (el clon real, no un scratch). Reproducido en un clon completo recién clonado de
`origin`: el mismo comando lo vuelve superficial y produce **9** fronteras en `.git/shallow` —
el mismo número que ya tenía `/home/pc0/Modelado-Mexicano`. El `mtime` de su `.git/shallow`
(`2026-09-20 14:44:05 -0600`) cae 6m43s antes del merge de `#913` (`20:50:48Z`), la ventana de
su `tests/check.py --baseline` de cierre. Corregido (`--depth=100` retirado; prueba nueva en
`tests/test_t_cron.py` con repos locales reales, sin red, que falla contra el código viejo y
pasa con el fix — verificado a mano con `git stash` del cambio). `git fetch --unshallow`
restauró la historia completa (492→4731 commits en `Modelado-Mexicano`); `mm-adq` nunca fue
superficial.

## P1 · Borrado, cubeta por cubeta

Re-derivación de hoy sobre las 124 ramas `CONTENIDO-EN-MAIN`/`HISTORIA-GEN1` de
`limpieza2_tabla.tsv` (metodología idéntica a `#913`: `git cherry origin/main <rama>` +
comparación DIRECTA de árbol — nunca diff de tres puntos). Corrección de método sobre la marcha:
la primera pasada comparó por **hash de blob** contra el árbol *actual* de `origin/main` y dio
falsos positivos masivos (`canon/estado-programa-v1_9.md`… hasta `v1_13.md`, `canon/gobernanza-
v1_13.md`/`v1_14.md`, `instrucciones-proyecto-v2_13.md`, `data/catalogo-fuentes-v1_0.md`,
`forense/encargos/cola/…`) — son documentos-singleton versionados que main **rota** (sella `vN+1`
y borra `vN`, convención `REEMPLAZA A … — borrar`) o colas ya procesadas; ausentes del árbol
*actual* pero presentes en su *historia*, y por tanto sin valor exclusivo real. Corregido
comparando por **ruta contra la historia completa de `origin/main`** (`git log -1 -- <ruta>`),
no solo su snapshot de hoy — la metodología de `#913` ("archivos que main no tiene") no
distinguía este caso porque corrió horas antes, cuando main aún no había rotado esos archivos.

**Resultado:** 124 evaluadas · **116 SAFE-BORRA** · **8 EXCLUIDAS** (lista completa, ninguna
oculta):
- 3 `EN-VUELO` (regla de 24h; último commit 17.1–18.4h): `acto/gen2-c2-compuesto-ic-enif2024-1`,
  `acto/gen2-c2-compuesto-ic-envipe2025-1`, `acto/gen2-pisos-enut2019-ejes-1` — mismas tres que
  `#913` ya había protegido por la misma regla, hoy todavía dentro de la ventana.
- 4 `WORKTREE-SUCIO` (mismas que el P4 de `#913`, re-verificadas hoy, ninguna se limpió sola):
  `codex/autoridad-semantica-enif`, `codex/autoridad-semantica-marco-cobertura-total`,
  `llave2-decreto`, `marco-produccion-total`.
- 1 `REVISADO-A-MANO`: `claude/encargo-maestra38-sello-3-6y5e0z` — su único `cherry_plus` (commit
  `8be17ee2`, un PARO de 0-bis que archiva `forense/encargos/2026-09-07-MAESTRA38-SELLO-3.md`)
  se verificó a mano como redundante (`git cat-file -e origin/main:<esa-ruta>` → presente, vía
  otra rama que sí ejecutó el acto), pero el criterio mecánico (`cherry_plus==0`) no lo acredita.
  Fuera del lote automático por disciplina; se lista para mesa en vez de forzar el criterio.

`git branch -D` sobre las 116 (incluye la rama local literal `main`, distinta de
`origin/main` — no checked out en ningún worktree, `[behind 2276]`, contenido íntegramente
superado — y `main-ff`). 10 de las 116 tenían worktree vivo: los 10 pasaron el chequeo de
`#910`/de este encargo (`data/raw` symlink o ausente) antes de `git worktree remove` (sin
`--force`). **0 fallos.**

**Estado final crudo:**
```
$ git -C /home/pc0/Modelado-Mexicano branch | wc -l
50
$ git -C /home/pc0/Modelado-Mexicano worktree list | wc -l
48
```

Ni `codex/gen2-marcador-adopcion-cli-1` ni `codex/gen2-motral2015-prioridades-prestaciones-cli-1`
(las 2 `MEDICION-SIN-RESCATAR`), ni las 5 `REVISAR-A-MANO`, se tocaron.

## P2 · Rescate de MOTRAL — NO se rescata

Rama efímera `acto/gen2-rescate-motral2015-prioridades-prestaciones-1` desde `origin/main`,
`data/corrida0/CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001/` traído desde el commit `914e92f3`
(no desde el worktree sucio, que tiene un rebase abortado — confirmado por `#913`: el conflicto
es interno a la propia rama, no contra `main`). `git cat-file -e
origin/main:data/corrida0/CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001/spec.yaml` → ausente:
sin colisión de id, confirmado.

`python3 tools/corrida0.py verify CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001` → **NO-EJECUTABLE**
(no un `NO-REPRODUCE` piadoso, pero tampoco reproduce lo que el sello declara): con el input real
localizado (`/mnt/c/Users/PC0/Descargas MX/UNIVERSO-2026-09/MOTRAL/motral2015_bases_datos_dbf.zip`
— el sandbox de esta sesión no lee `/mnt/c` en absoluto, comando repetido con el sandbox
desactivado para este paso puntual), la reejecución del `medidor.py` sellado produce
`outputs_faltantes` (41 de los ~42 `RESULT-…` que el `spec.yaml` sellado declara: los cinco `P17`
por sexo/edad/total, los 25 `P16-FIRST` por categoría×segmento, y la mayoría de los diagnósticos
de ranking) y **`outputs_no_declarados`** (`RESULT-MOTRAL15-RANKING-COMPLETOS`,
`RESULT-MOTRAL15-RANKING-JSON`, `RESULT-MOTRAL15-RANKING-N-ELEGIBLES`). Verificado el
`resultados.json` **ya sellado** (19/sep) directamente: solo trae esos mismos 3 keys de
diagnóstico — **nunca tuvo, ni siquiera al sellarse, los resultados P17/P16 que su propio
`spec.yaml` contrata.** `sello.json` es un manifiesto de hashes puro, sin campo de estado que
ates a que el contrato se satisfizo. No es un efecto del entorno (drift desde el sellado): el
propio sello nació incompleto frente a su contrato.

**No se rescata** (regla del encargo: "si verify no reproduce, no se rescata: NC con la salida
cruda"). `NC-0420` (`forense/no-corrido.tsv`) actualizada con esta razón y la salida cruda citada
arriba. Rama y worktree efímeros de este intento, limpiados (`git worktree remove` sin `--force`
tras vaciar el índice a mano — sin contenido de valor: todo lo generado en la sesión era mío,
del intento fallido; `git branch -D`).

## P3 · La colisión que `#913` no vio — dictamen

**(a) Archivo de evidencia.** `data/corrida0/CALC-PISOS-ENIF2021-EJES-0002/` de
`codex/gen2-marcador-adopcion-cli-1` (tip `2d662e78`), commit de sellado `7ebc7e11` ("Mide piso
corregido de ENIF 2021", `2026-09-19T12:31:18-06:00`), extraído a
`forense/notas/insumos-externos/pisos-enif2021-0002-rama-codex/pisos-enif2021-0002-codex-2026-
09-20-{ejecucion,medidor,resultados,sello,sello.sha256,spec.yaml}` + `-SHA256SUMS.txt` (nombres
con acto+fecha para no colisionar por basename contra `T02`, ver `tests/check.py::t02_duplicates`
— mismo defecto que `feedback_asienta_replay_aislado_escribe_sin_args`). Archivado como evidencia, no como `CALC`: no
se toca `data/corrida0/` en esta rama.

**Primer hecho no anticipado por el encargo: hay DOS versiones de `-0002`, no solo la de la rama
Codex.** `origin/main` también tiene un directorio `CALC-PISOS-ENIF2021-EJES-0002/` — pero solo
`medidor.py` + `spec.yaml` (sin `sello.json` ni `resultados.json`: nunca corrió), congelado en
`e2d8d167` ("1: congela sucesores y rejilla de pisos", `2026-09-19T12:45:49-06:00`). La propia
`corridas.tsv` de `main` lo confirma: fila `CALC-PISOS-ENIF2021-EJES-0002`, `corrida_id` sin
sufijo de hash (nunca ejecutado), estado `SUPERADO→CALC-PISOS-ENIF2021-EJES-0003`, y la fila de
`-0003` cita textualmente "sucesor/repetición de `CALC-PISOS-ENIF2021-EJES-0002` (`NO-CORRIDA`,
nunca sellada ni publicada)". Así que hay tres objetos a comparar: `-0002` en `main` (spec, nunca
corrida), `-0002` en la rama Codex (spec + corrida sellada), y `-0003` en `main` (spec + corrida
sellada).

**(b) ¿Qué es la "corrección posicional"?** El `medidor.py` de la rama Codex es un envoltorio de
108 bytes que importa `tools/pisos_ejes_v2.py::enif_v2` (módulo nuevo, exclusivo de esa rama,
ausente de `main` por completo) — implementación **textualmente independiente**, no derivada del
script de `main`. La comparación relevante para "corrección posicional" es entre las DOS
versiones de `-0002`/`-0003` DENTRO de `main`, que sí comparten código: `git diff` entre
`origin/main:…/CALC-PISOS-ENIF2021-EJES-0002/medidor.py` y
`origin/main:…/CALC-PISOS-ENIF2021-EJES-0003/medidor.py` da **una sola función distinta**,
`_formal()`:
```python
# -0002 (main, nunca corrida):
out.loc[(a.eq("2")|s.eq("2")).all(axis=1)&~yes]=False
# -0003 (main, sellada):
no=((a.eq("2").to_numpy()|s.eq("2").to_numpy()).all(axis=1))
out.loc[no&~yes]=False
```
`a` (columnas `P5_4_1..9`, cuentas) y `s` (columnas `P5_7_1..9`, ahorro) son dos `DataFrame`
**con nombres de columna distintos**. `a.eq("2")|s.eq("2")` en pandas **alinea por ETIQUETA de
columna**, no por posición: como ninguna columna de `a` se llama igual que ninguna de `s`, el
resultado de `|` es la UNIÓN de las 18 columnas con relleno `NaN` en las que no coinciden en cada
lado — no el "o" fila-a-fila entre el ítem *i* de cuentas y el ítem *i* de ahorro que el diseño
pretende. La corrección fuerza alineación POSICIONAL con `.to_numpy()` antes del `|`. **Es
exactamente lo que "corrección posicional" describe: un defecto de alineación pandas
(etiqueta vs. posición), no un error de captura de dato ni de codificación de reactivo.**

**(c) ¿Qué celdas cambian, y cuánto, entre la `-0002` sellada de Codex y la `-0003` de `main`?**
51 `RESULT-…` con id idéntico entre las dos (más los que solo difieren en formato de etiqueta —
`LOCALIDAD-15000-Y-MAS` vs `LOCALIDAD-15-000-Y-MAS`, `CUENTA-FORMAL-*` vs `CUENTA-*` — mapeados a
mano, mismo eje y categoría). **Las 10 celdas `-P` (punto) que sí tienen id idéntico: delta =
0.0000 en las 10, a 4 decimales.** Ampliando el chequeo con mapeo de etiqueta a las celdas de
`LOCALIDAD` y `CUENTA`: **coinciden a precisión completa de `float64`** (ej.
`LOCALIDAD-15000-Y-MAS-P`: `0.35308795215693956` en ambas, sin truncar). Los intervalos de
confianza (`-IC-LO`/`-IC-HI`, que dependen del *bootstrap*, no solo del punto) **también
coinciden bit a bit** (ej. `EDAD-18-29`: `[0.45211696980803534, 0.49630138194185036]` idéntico en
las dos). Esto no es sospechoso ni indica copia entre ramas: ambas implementaciones siguen la
misma convención de la casa para este tipo de estimador (bootstrap por estrato, `seed=42`,
`PCG64`, `10000` réplicas en bloques de 50 — verificado línea por línea en
`tools/pisos_ejes_v2.py:67-92` de la rama Codex contra `_estimate()` del script de `main`); dado
el mismo diseño, el mismo estrato/UPM y la misma clasificación correcta por persona, dos
implementaciones distintas de la misma fórmula determinista producen el mismo número. **Ninguna
celda comparable difiere entre la `-0002` de Codex y la `-0003` de `main`.** `main -0003` además
calcula un desenlace secundario (`INFORMAL-CUALQUIERA`) que la `-0002` de Codex no calcula en
absoluto — ausencia, no discrepancia.

**(d) ¿La corrección se hizo después de haber visto los resultados de `-0002`?**
Cronología (todos los commits citados, verbatim):
- `12:31:18` — rama Codex: `-0002` sellada (`7ebc7e11`, código y sellado en el mismo segundo).
- `12:45:49` — `main`: `-0002` congelada (`e2d8d167`) — **nunca llegó a correr ni sellarse en
  `main`.**
- `12:50:35` — `main`: `-0003` "congela corrección posicional" (`26204660`) — 4m46s después de
  `e2d8d167`, 19m17s después del sellado de Codex.
- `12:51:11` — `main`: `-0003` sellada (`2d0a8b29`).

**Veredicto: `CORRECCION-INDEPENDIENTE-DEL-RESULTADO`.** Dos razones, ninguna sola bastaría, las
dos juntas sí: (i) la `-0002` de `main` **nunca produjo un resultado** — no hay, dentro del linaje
de `main`, ningún número de `-0002` que alguien pudiera haber "visto" antes de escribir `-0003`;
el único resultado sellado de `-0002` en toda la caja vive en una rama distinta con
implementación textualmente no relacionada. (ii) Esa implementación de Codex ni siquiera comparte
íntegramente el vocabulario de ids (`CUENTA-FORMAL` vs `CUENTA`, ausencia total de
`INFORMAL-CUALQUIERA`) — reconstruir a mano, en los ~19 minutos entre el sellado de Codex y el
`COMMIT-1` de `-0003`, el defecto exacto de alineación pandas de un script *diferente* a partir
de números con id parcialmente distinto es un camino mucho menos parsimonioso que la explicación
directa: alguien leyó o corrió su propio borrador (`-0002` de `main`), notó (por inspección de
código o por una salida con columnas de más / `NaN` inesperados — el síntoma típico de este
defecto) el error de alineación en `_formal()`, y lo corrigió antes de sellar. El propio hecho de
que el `COMMIT-1` de `-0003` llegue 4m46s después de la propia redacción de `-0002` (no 19
minutos, que sería el tiempo desde Codex) apunta al mismo origen: revisión del propio borrador,
no del ajeno. **No aplica la reserva de `CORRECCION-POSTERIOR-A-VER-RESULTADO`; `-0003` no lleva
FP ni reserva por este hallazgo.**

## Enmienda a `#913` (por este acto, sin editar su nota — A.3)

`#913` (`forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-2-cierre.md`, sección P5) afirmó
que `CALC-PISOS-ENIF2021-EJES-0002` de `codex/gen2-marcador-adopcion-cli-1` "trae también
`data/corrida0/CALC-PISOS-ENIF2021-EJES-0002/` sellado el 19/sep …, ausente de `main`, **sin
colisión de id**. Rescatable." **Corrección: sí hay colisión de id.** `main` tiene su propio
directorio `CALC-PISOS-ENIF2021-EJES-0002/` (spec + medidor, congelado en `e2d8d167`, nunca
corrido) — mismo id, contenido distinto (ver dictamen arriba). No cambia la recomendación
operativa de `#913` (el directorio de Codex no se adopta como `CALC` — ver P3(a)), pero sí su
premisa: no es "rescatable sin fricción", es un id ya ocupado en `main` por una spec nunca
ejecutada, superada formalmente por `-0003`. La corrección no invalida `-0003` (ver dictamen (d)).

## Estado final

`## NO-CORRIDO / RESERVAS` del encargo archivado, actualizado: `NC-0419` (P1) se cierra —
ejecutado; `NC-0420` (P2) se cierra con razón real (`NO-EJECUTABLE`, MOTRAL no se rescata);
`NC-0421` (P3) se cierra — dictaminado; `NC-0422` (P4) se cierra — enmienda asentada arriba.
