# Nota de cierre · ACTO GEN2-CI-GUARDIAS-VIVAS-1 · 20/sep/2026

Tests en el repo / ejecutados por CI antes / después / saltados por corpus / fallas de verdad — los cinco derivados (§1, "una medición sin fila en la vista no cuenta como producida"; aquí no hay medición GEN2, pero el mismo principio aplica al conteo del propio acto):

- **Tests en el repo** (`ls tests/test_*.py | wc -l`): **122**.
- **Ejecutados por CI antes de este acto** (cableados en `verify.yml` o `tests/check.py`, `tools/ci_guardias.py --censo` columna `cableado_hoy`): **25**.
- **Ejecutados por CI después de este acto** (25 ya cableados + 60 nuevos en el job `guardias`): **85**.
- **Saltados por corpus**: **0** medidos hoy (ninguno de los 97 huérfanos falló por corpus ausente en este entorno; la columna `necesita_corpus_por_codigo` del censo marca 9 archivos que mencionan `data/raw` en su código pero los 9 corren limpio con fixtures propias -- el mecanismo de SKIP por corpus queda construido en `tools/ci_guardias.py --ejecuta-huerfanos` para cuando sí aparezca uno).
- **Fallas de verdad** (contenido roto, no arreglado aquí): **8** -- `tests/test_adq_descubrimiento.py`, `tests/test_celda_d_piloto_consumidor.py`, `tests/test_censo_derivado.py`, `tests/test_cierre_acto.py`, `tests/test_consulta_gen2.py`, `tests/test_motor_gen2_explicito.py`, `tests/test_motor_holdout.py`, `tests/test_relevo_encuci_f2.py` (NC-0384..NC-0391).

Resto de los 97 huérfanos: **29** `NECESITA-DEPENDENCIA` (16 `numpy`, 7 `pandas`, 2 `scipy`, 4 `pytest`) -- FP-396, decisión de mesa, no instalada aquí.

## Verificación de existencia (contra `adcfa978`)

Confirmada tal como el encargo la declaró: `ls tests/test_*.py | wc -l` → 122; grep de nombre base contra `verify.yml`/`check.py` → 97 sin coincidencia (25 cableados, no 122-97 al revés -- el encargo ya traía la cifra correcta). La corrida de los 97 sin corpus reprodujo la misma clase de fallos que el encargo reportó de memoria (imports `tools`/`milpa` sin `-m`, `jsonschema`/`pyreadstat`/`pytest` ausentes) con conteos ligeramente distintos porque el encargo los leyó a ojo del último error y este acto los deriva mecánicamente, ejecutando -- nunca adivinando -- cada archivo (§2, "ninguna cifra esperada se teclea").

## Decisiones tomadas sin esperar a mesa (baratas, D-14)

- `jsonschema`: ya declarado en `requirements.txt`; solo faltaba en el entorno de dirección, no en CI. Sin cambio.
- `openpyxl==3.1.5`: nuevo en `requirements.txt`, ~1.3s de instalación medida, destraba `tests/test_reactivos_contexto.py`.
- `tests/test_arnes_sesion.py`: reescrito de `pytest` al estilo de la casa (script, `sys.exit`) -- evita esperar la decisión de `FP-396` para una guardia que este mismo acto tenía que tocar de cualquier forma (P4).

## Decisiones que NO son de este acto (FP-396)

¿Se instala `numpy`/`pandas`/`scipy` (destraba 25 tests, ~11.8s de instalación medida en venv limpio) y/o se decide entre añadir `pytest` o reescribir los 4 archivos restantes que aún lo importan? Ninguna se decidió aquí.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Arreglar los 8 `FALLA-DE-VERDAD` (NC-0384..NC-0391) | FUERA-DE-PERÍMETRO (D-14: "no arregla tests rotos") | esas 8 guardias siguen sin gatear CI aunque ya no son huérfanas de facto -- el job `guardias` las detecta y las salta en voz alta | SIN-ASIGNAR por archivo (ver cada NC) |
| Instalar `numpy`/`pandas`/`scipy` y/o decidir la vía para `pytest` en los 4 archivos restantes | DECISIÓN-DE-MESA-PENDIENTE (FP-396) | 29 de los 97 huérfanos siguen sin correr en CI | acto que ejecute lo que mesa firme en FP-396 |
| Mover algún test entre `suite`/`adicionales` y `guardias`, o decidir si `guardias` debe entrar a branch protection además de a `needs` de `check` | FUERA-DE-PERÍMETRO (LO QUE NO HACE) | ninguno -- `check` ya depende de `guardias`, así que la protección existente (si exige `check`) alcanza al job nuevo sin cambio adicional | SIN-ASIGNAR |
| `test_relevo_encuci_f2.py`: determinar si el TIMEOUT>40s es un cuelgue real o un test simplemente lento que necesita más tiempo | NO-VERIFICABLE-AQUÍ (D-14: no se investiga contenido fuera del perímetro) | la guardia sigue sin correr en CI | SIN-ASIGNAR (NC-0391) |

## CONSUMIDO

PR: (se completa al abrir, mismo commit de cierre en cascada)
