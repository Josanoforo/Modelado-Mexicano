# Nota de cierre · ACTO GEN2-CI-GUARDIAS-VIVAS-1 · 20/sep/2026

Tests en el repo / ejecutados por CI antes / después / saltados por corpus / fallas de verdad — los cinco derivados (§1, "una medición sin fila en la vista no cuenta como producida"; aquí no hay medición GEN2, pero el mismo principio aplica al conteo del propio acto):

- **Tests en el repo** (`ls tests/test_*.py | wc -l`): **122**.
- **Ejecutados por CI antes de este acto** (cableados en `verify.yml` o `tests/check.py`, `tools/ci_guardias.py --censo` columna `cableado_hoy`): **25**.
- **Ejecutados por CI después de este acto** (25 ya cableados + 60 nuevos en el job `guardias`): **85**.
- **Saltados por corpus**: **0** medidos hoy (ninguno de los 97 huérfanos falló por corpus ausente en este entorno; la columna `necesita_corpus_por_codigo` del censo marca 9 archivos que mencionan `data/raw` en su código pero los 9 corren limpio con fixtures propias -- el mecanismo de SKIP por corpus queda construido en `tools/ci_guardias.py --ejecuta-huerfanos` para cuando sí aparezca uno).
- **Fallas de verdad** (contenido roto, no arreglado aquí): **8** -- `tests/test_adq_descubrimiento.py`, `tests/test_celda_d_piloto_consumidor.py`, `tests/test_censo_derivado.py`, `tests/test_cierre_acto.py`, `tests/test_consulta_gen2.py`, `tests/test_motor_gen2_explicito.py`, `tests/test_motor_holdout.py`, `tests/test_relevo_encuci_f2.py` (NC-0396..NC-0403).

Resto de los 97 huérfanos: **29** `NECESITA-DEPENDENCIA` (16 `numpy`, 7 `pandas`, 2 `scipy`, 4 `pytest`) -- FP-398, decisión de mesa, no instalada aquí.

## Verificación de existencia (contra `adcfa978`)

Confirmada tal como el encargo la declaró: `ls tests/test_*.py | wc -l` → 122; grep de nombre base contra `verify.yml`/`check.py` → 97 sin coincidencia (25 cableados, no 122-97 al revés -- el encargo ya traía la cifra correcta). La corrida de los 97 sin corpus reprodujo la misma clase de fallos que el encargo reportó de memoria (imports `tools`/`milpa` sin `-m`, `jsonschema`/`pyreadstat`/`pytest` ausentes) con conteos ligeramente distintos porque el encargo los leyó a ojo del último error y este acto los deriva mecánicamente, ejecutando -- nunca adivinando -- cada archivo (§2, "ninguna cifra esperada se teclea").

## Decisiones tomadas sin esperar a mesa (baratas, D-14)

- `jsonschema`: ya declarado en `requirements.txt`; solo faltaba en el entorno de dirección, no en CI. Sin cambio.
- `openpyxl==3.1.5`: nuevo en `requirements.txt`, ~1.3s de instalación medida, destraba `tests/test_reactivos_contexto.py`.
- `tests/test_arnes_sesion.py`: reescrito de `pytest` al estilo de la casa (script, `sys.exit`) -- evita esperar la decisión de `FP-398` para una guardia que este mismo acto tenía que tocar de cualquier forma (P4).

## Decisiones que NO son de este acto (FP-398)

¿Se instala `numpy`/`pandas`/`scipy` (destraba 25 tests, ~11.8s de instalación medida en venv limpio) y/o se decide entre añadir `pytest` o reescribir los 4 archivos restantes que aún lo importan? Ninguna se decidió aquí.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Arreglar los 8 `FALLA-DE-VERDAD` (NC-0396..NC-0403) | FUERA-DE-PERÍMETRO (D-14: "no arregla tests rotos") | esas 8 guardias siguen sin gatear CI aunque ya no son huérfanas de facto -- el job `guardias` las detecta y las salta en voz alta | SIN-ASIGNAR por archivo (ver cada NC) |
| Instalar `numpy`/`pandas`/`scipy` y/o decidir la vía para `pytest` en los 4 archivos restantes | DECISIÓN-DE-MESA-PENDIENTE (FP-398) | 29 de los 97 huérfanos siguen sin correr en CI | acto que ejecute lo que mesa firme en FP-398 |
| Mover algún test entre `suite`/`adicionales` y `guardias`, o decidir si `guardias` debe entrar a branch protection además de a `needs` de `check` | FUERA-DE-PERÍMETRO (LO QUE NO HACE) | ninguno -- `check` ya depende de `guardias`, así que la protección existente (si exige `check`) alcanza al job nuevo sin cambio adicional | SIN-ASIGNAR |
| `test_relevo_encuci_f2.py`: determinar si el TIMEOUT>40s es un cuelgue real o un test simplemente lento que necesita más tiempo | NO-VERIFICABLE-AQUÍ (D-14: no se investiga contenido fuera del perímetro) | la guardia sigue sin correr en CI | SIN-ASIGNAR (NC-0403) |

## CONSUMIDO

`PR #917`. **RENUMERADO 559→560→561→562, FP-396→397→398, NC-0384..0391→NC-0396..0403**: `GEN2-PISOS-ENIF2021-FORMALIDAD-1` (`PR #915`) tomó `ADR-559`/`FP-396`/`NC-0384`-`NC-0385`; `GEN2-GUARDIAN-ENVIPE-EJES-IC-1` (`PR #916`) tomó `ADR-560`/`FP-397`/`NC-0386`-`NC-0390`; `GEN2-RELEVO-TANDA-2` (`PR #914`) fusionó tercero sobre la misma base y tomó `ADR-561`/`NC-0392`-`NC-0395` — regla de la casa, renumera quien fusiona después, así que este acto queda en `ADR-562`/`FP-398` (sigue libre)/`NC-0396`-`NC-0403`.

## ADENDA post-CI (A.10, universo creció)

El job `guardias` corrió por primera vez en CI real sobre el merge ref del PR y falló: `PR #915` trajo `tests/test_pisos_enif2021_formalidad.py`, nacido después del censo de este acto (122 archivos) y antes de que el job corriera contra el merge — el universo censado (122) quedó **VENCIDO EN ALCANCE** frente al universo real (123) sin que ninguna cifra de arriba se reescriba (A.10: se re-sella, no se edita el viejo). Re-derivado: `python3 tools/ci_guardias.py --censo` → 123 archivos, 98 huérfanos (61 `CORRE-EN-CI`, 8 `FALLA-DE-VERDAD`, 29 `NECESITA-DEPENDENCIA` — mismas ocho y mismos veintinueve; el nuevo archivo corre limpio sin corpus). `forense/analisis/ci-guardias/censo-tests.tsv` republicado con las 123 filas; el job vuelve a fallar en falso hasta el siguiente push. Esto confirma, de la peor manera posible, exactamente el mecanismo que el job existe para exigir: un test que nace sin fila en el censo detiene el job en vez de correr en silencio.

Ese mismo push reveló un segundo defecto, sin relación con el censo: `tests/test_check_parallel.py::WorkflowGate` fijaba `needs={suite,adicionales}` y dos variables de entorno del paso de compuerta -- nunca se había corrido contra el `verify.yml` real con `guardias` sumado hasta este push, porque el archivo se edita pero el test que lo verifica corre aparte. Extendido a las tres entradas (`suite`, `adicionales`, `guardias`) y sus tres variables de entorno; verificado localmente antes de repushear.

**Segunda colisión de rótulo, en el mismo push:** `origin/main` avanzó otros 11 commits (`PR #916`, `GEN2-GUARDIAN-ENVIPE-EJES-IC-1`) mientras el fix de arriba se preparaba, y ese acto tomó `ADR-560`/`FP-397`/`NC-0386`-`NC-0390` sobre la misma base que ya había tomado `ADR-559`/`FP-396`/`NC-0384`-`NC-0385` (`PR #915`). Regla de la casa, dos veces en el mismo acto: este acto queda en `ADR-562`, `FP-398`, `NC-0392`-`NC-0399`. `PR #916` también trajo `tests/test_c2_ic_envipe2025_guardia.py`, nuevo huérfano nacido durante el acto: re-censado otra vez, 124 archivos / 99 huérfanos / 62 `CORRE-EN-CI`, mismos ocho `FALLA-DE-VERDAD` y mismos veintinueve `NECESITA-DEPENDENCIA`. `python3 tools/ci_guardias.py --ejecuta-huerfanos` verificado en verde localmente (`ejecutados=62 saltados=37 fallidos=0`) antes de este push.

**Tercera colisión de rótulo:** `origin/main` avanzó otros 7 commits (`PR #914`, `GEN2-RELEVO-TANDA-2`) mientras el fix de la segunda colisión se preparaba, y ese acto tomó `ADR-561`/`NC-0392`-`NC-0395` sobre la misma base que ya había tomado `ADR-559`/`ADR-560` (`PR #915`/`#916`). Regla de la casa, tres veces en el mismo acto: este acto queda en `ADR-562`, `FP-398` (nunca colisionó, sigue libre), `NC-0396`-`NC-0403`. `PR #914` no trajo tests nuevos (confirmado: `python3 tools/ci_guardias.py --censo` sigue en 124/99/62 tras el merge). `tests/check.py --baseline --parallel` y `python3 tools/ci_guardias.py --ejecuta-huerfanos` re-verificados en verde antes de este push.
