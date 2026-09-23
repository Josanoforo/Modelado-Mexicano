# PR #1087 · conservación de bytes de dos inputs ENOE

**Corrección de transporte Git, 23/sep/2026.** La spec y los resultados
sellados de `CALC-ENOE-PISOS-0003` no cambiaron. El problema estaba en
`.gitattributes`: `* text=auto eol=lf` hizo que Git guardara los dos TSV
preparatorios como LF, aunque la corrida consumió sus bytes CRLF. El checkout
de la rama que ejecutó la medición conservaba CRLF, pero un checkout nuevo
restauraba LF y por eso los hashes de los inputs no coincidían. El problema
era reproducible con `git show HEAD:ruta | sha256sum` antes de la corrección.

| Input | Blob previo LF | Blob nuevo y checkout CRLF, igual a spec |
| --- | --- | --- |
| `data/enoe-reactivos-olas-v1_0.tsv` | `cc9617b670405ee0b51d3fd7fcf966fdb7e254734fff46012a9b123429dcc549` | `735615561ecdc27b6ad511c399b6176a80cfa35f66f26e9a8215279bfce16463` |
| `data/enoe-olas-elegibles-preparacion-v1_0.tsv` | `b793a6f4960d9b85ac748ea10b36cc5911c6a922fb9ca31cc6a9956c34175855` | `bead9676b166040dba4bc6ec29047d173ad710d92d77dfea1f807874a3f1b35b` |

La corrección `429978956c3f59eebfa1805f505e0dfa16d6d0c3` fija `-text
whitespace=cr-at-eol` **solo** para esos dos archivos y coloca los bytes CRLF
en el blob de Git. Al convertir los nuevos blobs CRLF a LF se obtienen
exactamente los blobs anteriores, línea por línea (560 y 44 líneas). `git
ls-files --eol` devuelve `i/crlf w/crlf attr/-text` para ambos. No se alteró
ninguna definición ni se ajustó un hash sellado para hacerlo coincidir.

## Replay desde checkout limpio en CAJA

Se creó `git worktree add --detach /tmp/astra5-enoe-verify-42997895 HEAD`
en `429978956c3f59eebfa1805f505e0dfa16d6d0c3`. Se montó únicamente el
enlace ignorado `data/raw -> /home/pc0/mm-corpus/raw`; `git status
--porcelain --untracked-files=all` permaneció vacío antes y después del
replay. `sha256sum` de ambos archivos extraídos coincide con la spec y con
`git show HEAD:ruta | sha256sum`. `2026T1` permanece fuera de la spec y de los
inputs; no se abrió ninguno de sus dos paquetes.

`python3 tools/corrida0.py preflight CALC-ENOE-PISOS-0003` cotejó los 48
inputs, incluidos los dos TSV, y el sello previo. Termina `BLOQUEADO
calc_ya_sellado=CALC-INMUTABLE-YA-SELLADO`, como corresponde a la guarda que
impide repetir `run` sobre un CALC sellado. Se usó `verify` para reproducirlo:

| CALC | Inputs | RESULT | Sello | Contexto | Veredicto |
| --- | ---: | ---: | --- | --- | --- |
| `CALC-ENOE-PISOS-0003` | 48/48 COINCIDE | 5/5 REPRODUCE | COINCIDE | IDENTICO | REPRODUCE |
| `CALC-ENOE-PERSISTENCIA-0001` | 3/3 COINCIDE | 3/3 REPRODUCE | COINCIDE | IDENTICO | REPRODUCE |

En ambos, código, parámetros, semilla y dependencias dan `IDENTICO`. El
verificador marca `commit_informativo=DISTINTO` por el commit de transporte;
FP-358 no lo usa como gate y el propio verificador declara contexto efectivo
`IDENTICO`. El JSON
`forense/analisis/dominios/enoe/evidencia-checkout-limpio-42997895.json`
conserva los IDs de los 51 inputs y ocho RESULT cotejados, SHA-256 de ambos
logs completos, hashes de specs/resultados/sellos y estado limpio del
checkout. Los logs completos se generaron bajo `/tmp` sin guardar microdatos
ni identificadores de personas en el repo.
`python3 tests/check.py --baseline` volvió a dar **LÍNEA BASE: VERDE, sin
FAIL nuevos** (los tres FAIL heredados permanecen). `git diff --check`
también pasa con `whitespace=cr-at-eol` para estos dos blobs CRLF.

**No procede CALC sucesor:** el mismo procedimiento y los mismos bytes
sellados reproducen exactamente los resultados existentes una vez que Git
conserva esos dos inputs. Ambos CALC, specs, `resultados.json` y sellos
permanecen íntegros. Siguen vigentes las reservas y límites del cierre:
2026T1 cerrada, sin transición individual de panel, sin ingreso real ni
cuidados específicos identificados, y sin IC predictivo calibrado.

## Guarda adicional detectada por CI

El job `adicionales` de #1087 expuso un error independiente del replay: el
sidecar `.cuerpo.sha256` del encargo archivado citaba la **ruta completa**
del `.md`, mientras el contrato de `sella_sha256 --cuerpo` exige su
**basename**. Su hash de contenido `bf42d6b5...` era y sigue siendo el hash
correcto del archivo entero normalizado. Se corrigió solo el campo de nombre
del sidecar, sin modificar el encargo ni recalcular su hash. Las pruebas
`python3 tools/sella_sha256.py --cuerpo --verifica ...` dan
`SELLO_COINCIDE`, y `python3 tests/test_verifica_sidecars.py` termina
`11 casos OK`. Esta corrección tampoco toca ningún sello de CALC.
