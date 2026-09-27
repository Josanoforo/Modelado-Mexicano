## Reglas de lectura y herramientas (ACTO GEN2-TUBERIA-RENDIMIENTO-1, P1; fuente única desde GEN2-TUBERIA-CABLEADO-SESIONES-1)

El contexto se gasta leyendo, no computando. Toda sesión:

- `wc -l` antes de abrir; nunca `cat` ni lectura completa de un archivo de más de 200 líneas: `head -n`, `tail -n`, `sed -n 'a,bp'`, o Read con `offset`/`limit`.
- `rg -c` (o `grep -c`) antes de listar coincidencias; `rg -l`, `rg --max-columns 160`.
- `git diff --stat` antes de `git diff`; `git log --oneline -n N`, nunca `git log -p` sin ruta.
- Tests: `pytest -q … | tail -n 20`; `python3 tests/check.py --rapido | tail -n 30`.
- TSV grandes solo por lector CSV (`csv.DictReader` + `itertools.islice`), nunca por línea física; JSON por `jq`, YAML por `yq` (`yq '.[] | select(.id=="<id>")' data/manifiesto.yaml`).
- Una fila, en una línea: `python3 tools/consulta.py result|corrida|celda|payload|fp|nc <id>`.

**Derivados — se consultan, no se leen** (regenerados por comando; nunca `cat`):
`data/corrida0/{corridas,resultados,usos,marcador-segmento}.tsv`, `data/corrida0/CALC-*/resultados.json`, `data/manifiesto.yaml`, `milpa/estimadores-por-segmento.yaml`, `data/curacion-universo/*.tsv`, `canon/L0/HISTORICO.md` (vista: `python3 tools/l0_vista.py`).

**Se hace cumplir, no se aconseja.** En Claude Code, `tools/hook_lectura.py` (PreToolUse sobre Bash y Read) bloquea con salida 2: `cat`/`less`/Read sin rango sobre > 200 líneas, lectura completa de un derivado, `git log -p` sin ruta y `pytest` sin `-q`. Escape declarado: `# --permitir-lectura-completa` al final del comando Bash; queda registrado. Registro de cumplimiento: `forense/analisis/cableado/bloqueos.tsv`. Codex no ejecuta hooks: `tools/ci_guardias.py --ejecuta-huerfanos` marca WARN si el diff de la rama añade `cat` de un derivado.

**Subagentes por pieza.** En un lote de ≥ 3 piezas, cada pieza corre en un subagente con perímetro propio y devuelve solo su tabla de resultado y su `git diff --stat`; el hilo principal ensambla, no relee. Ejemplo (Claude Code, herramienta Agent):
`Agent(description="P2 de LOTE-X", prompt="Ejecuta solo la pieza P2 de forense/encargos/<encargo>.md. Perímetro: <rutas>. No edites fuera. Devuelve: tabla de resultado (≤ 15 filas) y git diff --stat. Nada más.")`
En Codex: una tarea por pieza con el mismo perímetro y la misma forma de devolución.

**Arranque.** Lee `canon/MEMORIA-OPERATIVA.md` antes de explorar. Clon parcial para sesiones de nube: `docs/sesiones.md`.
