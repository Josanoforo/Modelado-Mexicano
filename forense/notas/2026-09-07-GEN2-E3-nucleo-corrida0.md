# `ACTO GEN2-E3 · AUTOMATIZA-GEN2-1` — nota de cierre

7/sep/2026 · entorno **NUBE**, sin corpus ni red · `ADR-389` ·
encargo: `forense/encargos/cola/2026-09-07-GEN2-E3-AUTOMATIZA-GEN2-1.md`
(archivado verbatim por `/encola` en `ACTO GEN2-E0`).

**CONTADOR GEN2: cero.** El smoke no cuenta y sus etiquetas lo dicen.

---

## 1 · A.8 — el terreno antes de tocarlo

Las tres comprobaciones que el encargo exige, con su salida cruda:

```
$ grep -c "def preflight\|def run\|def verify\|def spec_check\|def negativo" tools/corrida0.py
0
$ ls tools/entorno.py tools/limpia_arbol.py
ls: cannot access 'tools/entorno.py': No such file or directory
ls: cannot access 'tools/limpia_arbol.py': No such file or directory
$ grep -n "duplicado\|mismo rótulo" .claude/commands/acto.md
(sin salida)
```

Las tres confirman el terreno que el encargo supone. Después del acto: el
primer `grep` da **5**, los dos archivos existen, y el tercero da **3**.

## 2 · Compuerta — cumplida por producto, con una salvedad del comando

`COMPUERTA: GEN2-E2 fusionado`. (El encargo la escribe con el rótulo pelado de
la serie; aquí se cita en la forma larga obligatoria que
`canon/registro-rotulos.tsv` fija para GEN2 — la forma pelada sólo vive
dentro del verbatim, y por eso los siete encargos GEN2 llevan exención de
`T25` por archivo y esta nota no la necesita.)

```
$ git log --oneline origin/main -3
7df7dfd Merge pull request #600 from Josanoforo/claude/gen2-e2-demanda-derivation-wu2cfp
521ecb8 GEN2-E2 C0-A: nota, cascada T27 y recibo FP-338 + ABIERTA FP-339
d60c726 GEN2-E2 C0-A: tools/corrida0.py demanda + demanda-*.tsv derivados
$ git show origin/main:tools/corrida0.py | grep -c "def demanda"
0
$ git show origin/main:tools/corrida0.py | grep -n "def cmd_demanda\|set_defaults(func=cmd_demanda)"
542:def cmd_demanda(args) -> int:
632:    d.set_defaults(func=cmd_demanda)
```

**El producto exigido existe** — `demanda` está implementado y cableado al
parser en `origin/main`, fusionado por `PR #600`. **El comando literal del
encargo devuelve `0`, no `1`**: `GEN2-E2` nombró sus funciones con el patrón
`cmd_<subcomando>`, y `"def demanda"` no es subcadena de `"def cmd_demanda"`.

Se anota en vez de silenciarse porque una compuerta cuyo comando no puede
pasar nunca es peor que ninguna: la siguiente sesión que la corra al pie de
la letra para en falso, sobre un árbol correcto. La compuerta se dio por
cumplida **por producto**, que es el mecanismo que `/acto` §2.2 declara
preferente (`git show origin/main:<ruta>`), y no por el `grep` — que la
propia skill degrada a «indicio, no prueba» desde `ADR-277`.

## 3 · Lo que se construyó

| pieza | archivo | qué hace |
|---|---|---|
| P1 | `tools/corrida0.py` | `preflight` · `run` · `verify` |
| P2 | `tools/corrida0.py` | `spec-check` |
| P3 | `tools/corrida0.py` · `tools/entorno.py` | `negativo` · firma del entorno |
| P4 | `.claude/commands/acto.md` · `tools/limpia_arbol.py` | guard de arranque · higiene en modo reporte |
| smoke | `data/corrida0/CALC-SMOKE-0001/` | replay sellado de `agregado_v1_3.py` |
| tests | `tests/test_corrida0.py` · `tests/check.py` | 22 casos, `T32 · T-CORRIDA0` |

### Tres decisiones de diseño que no son las literales del encargo

**(a) `spec.md` frente a `main`: tres estados, no uno.** El encargo pide que
`preflight` exija «sha del md en `main` == el citado en yaml». Implementado
como `EN-MAIN-COINCIDE` / `EN-MAIN-DISCORDA` (bloquea) / `NO-EN-MAIN`
(declara, no bloquea). La razón es aritmética: la primera corrida de una spec
ocurre **por definición** antes de que la spec esté fusionada, así que exigir
`main` haría que ninguna spec nueva pudiera pasar `preflight` jamás — el
propio smoke de este acto sale `NO-EN-MAIN`. El estado viaja a
`ejecucion.json` como `spec_md_estado`: no se da por fusionada, se dice.

**(b) `inputs` con dos orígenes.** El encargo dice «inputs en manifiesto con
hash», pero también dice que el smoke «corre sobre insumos versionados». Son
dos cosas distintas y se implementaron como dos: `origen: manifiesto` va por
`tests/manifiesto.py --verifica` (todos los ids en una invocación, salida
cruda, tres estados A.1 sin colapsar) y `origen: repo` se rehashea contra el
árbol y se exige commiteado. Colapsarlas habría obligado a registrar en el
manifiesto seis archivos del propio repo, que no son payloads.

**(c) La tolerancia se aplica por tipo del VALOR, no por tipo de la spec.**
`CALC-SMOKE-0001` declara `tipo: flotante`, pero tres de sus nueve `RESULT`
son enteros (`N-CELDAS-UNIVERSO`, `REPLICAS`, `SEED`) y se comparan **exacto**.
Una spec no debería poder aflojar la comparación de un entero declarando
`flotante` en la cabecera.

## 4 · El caso de prueba obligatorio (P2)

```
$ python3 -c "…spec_check con iiib_hs.dta::hs02g y p_hs.dta::hs02g…"
  [ OK ] iiib_hs.dta :: hs02g
         etiqueta: INTERNADO CENTRO RURAL
         etiqueta: ULT 12MES INTERNADO:CENTRO SALUD RURAL
  [ OK ] p_hs.dta :: hs02g
         etiqueta: INTERNADO CENTRO SALUD RURAL
         etiqueta: INTERNADO DIF
```

**Etiquetas distintas, detectadas.** El mismo `variable_id` en dos miembros
del mismo instrumento no es el mismo reactivo, y el check resuelve cada par
contra **su** archivo. Es el defecto que `spec-check` existe para atrapar.

`IMMS` → `FAIL` **con** `[WARN] ¿IMSS?` (distancia 1). La sugerencia sale a
la vista y **no cierra el `FAIL`**: no se da por hallada, no edita la spec,
no sustituye nada en el resultado. `t_spec_check_imms_warn` lo afirma
explícitamente (`item["estado"] == "FAIL"`).

Contra la spec del smoke, `spec-check` reporta **0 pares declarados sobre
317 718 filas examinadas** — vacío **declarado** (`spec.md` §6), no olvidado:
este cálculo no lee reactivos de ningún instrumento.

## 5 · El smoke, y lo que no se puede reclamar de él

`preflight` **VERDE** (único aviso: `spec_md_no_esta_en_origin_main`, el que
corresponde) → `run` → `verify` **`REPRODUCE`**, los nueve `RESULT`, `delta
0.0`.

`delta 0.0` **no** es la razón por la que la tolerancia es `1e-10`. La
tolerancia existe por el `3·10⁻¹⁵` en `ic_hi` observado el 7/sep, que es
redondeo de `float64` en una suma reasociada; que esta reejecución diera cero
exacto es un hecho de esta corrida, no una garantía del cálculo. Una
tolerancia calibrada a lo que salió hoy sería una tolerancia inútil mañana.

**Ninguna cifra del smoke es nueva y ninguna es GEN2.** `generacion =
LEGACY-GEN1 · tipo = REPLAY-SMOKE · cuenta_gen2 = NO ·
validacion_independiente = NO-HECHA`, selladas en `ejecucion.json`. Lo que el
smoke prueba es el aparato. La comparación primaria del duelo sigue siendo la
de `ADR-388` y sigue `INDETERMINADO`.

## 6 · Exenciones nuevas en `tests/check.py`, y por qué

Dos, ambas sobre `data/corrida0/CALC-*/` y por la misma razón: `T27` (cita en
`INFRAESTRUCTURA-v1_0.md`) y `T02` (colisión de nombre normalizado).

Un recibo de corrida se llama `spec.md`/`spec.yaml`/`medidor.py`/
`ejecucion.json`/`resultados.json`/`sello.json` **siempre** — el nombre lo
fija `corrida0 run`, no quien escribe la spec. `CALC-0001/resultados.json` y
`CALC-0002/resultados.json` colisionarán por diseño en cuanto `GEN2-E5` escriba la
segunda corrida, igual que `conjunto_de_datos.csv` bajo `data/raw`; y exigir
una fila de `INFRAESTRUCTURA` por corrida convertiría ese archivo en el
registro de corridas que `corrida0 registro` (`GEN2-E6`) va a ser.

**La custodia no se pierde y no se mueve a ninguna parte vaga**: cada
directorio trae su `sello.sha256` verificable con
`python3 tools/sella_sha256.py --verifica data/corrida0/<CALC>/sello.json`, y
su `ejecucion.json` fija `git_commit` + `script_blob_sha256` +
`input_sha256`. `data/corrida0/demanda-*.tsv` (`GEN2-E2`) **no** queda exento
de nada.

## 7 · Límites declarados

1. **El test no cubre el smoke de punta a punta.** `run` exige árbol limpio y
   la suite corre casi siempre con el árbol sucio; un test que lo intentara
   fallaría por el motivo equivocado. El smoke se corre a mano y su recibo
   queda versionado. Escrito en `tests/check.py::t32_corrida0` y aquí.
2. **`inputs` del smoke no es exhaustivo, y lo dice.** `agregado_v1_1.py` lee
   `corridas-{R,M,L}/` completos; esos archivos no se enumeran uno por uno.
   Su identidad colectiva la fija `git_commit`. Un `inputs` que aparentara ser
   exhaustivo sin serlo valdría menos que uno corto con su límite escrito
   (`spec.md` §5).
3. **`verify` no re-verifica los inputs de manifiesto.** Los hashea
   `preflight` vía `tests/manifiesto.py`; `verify` lo declara en su salida
   (`[MANIFIESTO] input … -- lo verifica preflight`) en vez de callarlo o de
   duplicar el mecanismo.
4. **El guard de duplicado no puede consultar PRs por sí mismo.** El paso
   `0.c` de `/acto` nombra los tres sitios (rama remota, worktree, PR
   abierto), pero los dos primeros son comandos y el tercero depende del tool
   de GitHub disponible en la sesión. Se declara así en la skill en vez de
   fingir un comando único.
5. **`limpia_arbol` no hace `fetch`.** A propósito: el ARRANQUE ya corre
   `git fetch --prune` antes, y un fetch escondido haría que el conteo de
   «commits detrás» dependiera de cuándo se llamó al script y no del estado
   que el operador acaba de mirar.

## 8 · Sucesores

- `GEN2-E4` — `limpia_arbol.py --aplica` (hoy código 2, `NO-IMPLEMENTADO`).
- `GEN2-E5` — `CALC-0001`/`0002`/`0003`, las primeras corridas que **sí** cuentan.
- `GEN2-E6` — `registro` · `status` · `vigencia` · `delta`, y `T-REPRO`.
