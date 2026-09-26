# Modelado Mexicano

Repo de investigación forense-estadística sobre encuestas de México (INEGI y afines).

Instrucciones vigentes del proyecto: @gobierno/instrucciones-proyecto-v2_16.md

Todo acto entra por `/acto`.

Todo va en español.

Cadena de mando: mesa → dirección → sesión.

## Reglas de lectura (ACTO GEN2-TUBERIA-RENDIMIENTO-1, P1)

El contexto se gasta leyendo, no computando. Toda sesión:

- `wc -l` antes de abrir; nunca `cat` ni lectura completa de un archivo de más de 200 líneas: `head -n`, `tail -n`, `sed -n 'a,bp'`, o Read con `offset`/`limit`.
- `rg -c` (o `grep -c`) antes de listar coincidencias; `rg -l`, `rg --max-columns 160`.
- `git diff --stat` antes de `git diff`; `git log --oneline -n N`, nunca `git log -p` sin ruta.
- Tests: `pytest -q … | tail -n 20`; `python3 tests/check.py --rapido | tail -n 30`.
- TSV grandes solo por lector CSV (`csv.DictReader` + `itertools.islice`), nunca por línea física; JSON por `jq`, YAML por `yq` (`yq '.[] | select(.id=="<id>")' data/manifiesto.yaml`).
- Una fila, en una línea: `python3 tools/consulta.py result|corrida|celda|payload|fp|nc <id>`.

**Derivados — se consultan, no se leen** (regenerados por comando; nunca `cat`):
`data/corrida0/{corridas,resultados,usos,marcador-segmento}.tsv`, `data/corrida0/CALC-*/resultados.json`, `data/manifiesto.yaml`, `milpa/estimadores-por-segmento.yaml`, `data/curacion-universo/*.tsv`, `canon/L0/HISTORICO.md` (vista: `python3 tools/l0_vista.py`).

Clon parcial para sesiones de nube: `docs/sesiones.md`.
