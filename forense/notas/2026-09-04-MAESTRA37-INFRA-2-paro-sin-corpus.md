# MAESTRA37-INFRA-2 · PARO de Frente D (y de la parte de FP-259 que exige corpus real)

Sesión ejecutada en un entorno de nube/planificación, sin la máquina Ubuntu
con corpus montado. Confirmado con los mismos dos comandos que la compuerta
de arranque exige, en el worktree fresco `../mm-maestra37-infra2` (rama
`claude/maestra37-infra-2-capa2-portabilidad`, desde `origin/main` en
`ff68b9f`, merge de PR #521/INFRA-1):

```
$ ls data/raw
ls: cannot access 'data/raw': No such file or directory
$ cat data/raices.local.yaml
cat: data/raices.local.yaml: No such file or directory
```

Ambos ausentes — coincide exactamente con lo que el propio documento de
planificación PLAN-MAESTRA37-INFRA-1-2 (entregado fuera del repo, no
versionado aquí) §1.3 ya había observado en su sesión de
planificación ("data/raw y data/raices.local.yaml están ausentes en
cualquier sesión de nube/planificación... confirma que INFRA-2 no puede
ejecutarse ni verificarse fuera de la máquina Ubuntu con corpus"), y con la
compuerta de arranque (versión corta) del AJUSTE DE DIRECCIÓN de LIBRO 2,
punto 4: "Deben existir y declarar al menos `descargas_mx`. PARO si
cualquiera falta."

## Qué queda bloqueado

**Frente D completo** (COMMIT-1 del AJUSTE): tanto D-A (verificar
`via_capa2.py --root .` contra el corpus real y promover los diffs
legítimos) como D-B (medir si hay ≥1 enlace nuevo exactamente resoluble
antes de decidir si construir `--vincula`) exigen correr `via_capa2.py`
contra payloads reales en disco. No hay disco que medir aquí — no se
fabrica una cifra ni se decide "0 enlaces nuevos" sin haber corrido nada:
eso sería inventar una medición, exactamente lo que la regla de señal del
proyecto prohíbe.

**FP-259(iii), la parte que mide contra archivos reales**: `tests/corpus.py`
no truena sin corpus (barre un `os.walk` que simplemente no encuentra nada
bajo una raíz ausente/no configurada), así que en principio corre — pero
el "antes"/"después" que el procedimiento pide comparar sería 0=0 trivial,
sin ejercitar el caso real de "mismo sha, misma raíz" vs. "mismo sha, otra
raíz" que la reclasificación necesita demostrar. El plan sí permite un
fixture mínimo cuando "el corpus real no contiene ningún caso que permita
verificar la frontera" — pero el usuario decidió explícitamente acotar
esta sesión a **solo Frente E** y dejar D y FP-259 para la máquina con
corpus, así que FP-259 tampoco se tocó aquí, aunque un fixture-only habría
sido técnicamente viable. Queda para cuando se retome en la máquina
correcta (o, si se prefiere, se puede hacer el fixture-only de FP-259
desde una sesión de nube — es una decisión de mesa, no una limitación
técnica).

## Qué SÍ se ejecutó

Frente E (COMMIT-1 de esta rama, `54a1b70`): `semantic_run.py` deja de
resolver `data_raw` contra una ruta de una sola máquina hardcodeada, y
distingue explícitamente `RAIZ_NO_CONFIGURADA` de `ARCHIVO_NO_EXISTE`. Es
corpus-independiente (fixture sintético bajo `tempfile`), y por eso sí fue
posible medirlo/probarlo aquí. Detalle completo en el mensaje del commit.

## Para retomar

En la máquina Ubuntu con corpus: `git fetch origin main`, confirmar que
este PR (o el commit `54a1b70`/su equivalente fusionado) ya está en
`origin/main`, `git worktree add` fresco desde ahí, y ejecutar la
compuerta de arranque completa del AJUSTE DE DIRECCIÓN de LIBRO 2 —
confirmará `data/raw`/`data/raices.local.yaml` con `descargas_mx`
declarada, y desde ahí Frente D (con la medición previa obligatoria) y,
si se decide, el fixture o medición real de FP-259.
