# Nota de cierre · ACTO GEN2-TUBERIA-RENDIMIENTO-1

ADR: `ADR-260924-GEN2-TUBERIA-RENDIMIENTO-1-ae2a-01` (raíz `ae2a` = 0-bis `ae2a11e1`).
Encargo: `forense/encargos/2026-09-24-GEN2-TUBERIA-RENDIMIENTO-1.md` (sello de cuerpo en su `.cuerpo.sha256`). Fuente: `forense/encargos/fuentes/HERRAMIENTAS-rendimiento-y-consumo-2026-09-24.md` (+ `.sha256`).

Contadores movidos: **cero mediciones**; ningún número de ninguna vista cambia. Se movieron solo contadores de tiempo (abajo).

## ARRANQUE
- Repo `/home/user/Modelado-Mexicano`, base `8358b891` = SHA de redacción; al cerrar main avanzó 8 commits (merge limpio, ninguno toca `corrida0.py`, `marcador_segmento.py` ni las vistas).
- Entorno NUBE (hook: `ENTORNO-DERIVADO = NUBE`, `senal-corpus: montado=NO archivos_examinados=0`, `red: DENEGADA-POR-POLITICA` a INEGI; PyPI sí respondió). Cero microdato.
- Rama: la fijada por la plataforma, `claude/new-session-6fcgwp` (el encargo lo permite; se declara). Duplicado: `git ls-remote --heads origin | grep -i rendimiento` → 0.

## Premisas que cayeron (logística, declaradas)
1. `[EJECUTADO] CLAUDE.md no existe` — **falsa**: existía con 11 líneas (PR #1050). Se añadió la sección de reglas, no se creó.
2. `[SUPUESTO] el cuello es pandas/joins → DuckDB/Polars` — **el perfil lo refutó**: el cuello es parseo YAML en Python puro. DuckDB/Polars no se usaron (D-14; «el perfil manda»).
3. `pytest -n auto en check.py/CI para los 1 349 tests` — `check.py` no es pytest; los archivos pytest corren uno por uno por `tools/ci_guardias.py` (fuera de §9). Ver NO-CORRIDO.
4. Las vistas publicadas en main ya no coinciden con lo que su derivador produce hoy (`registro --escribe` PARA por 13 veredictos de replay ajenos; `marcador_segmento --escribe` reescribe 459 líneas). Es deriva previa, no de este acto; se restauró con `git checkout` y **no se publica** (PARO b). La equivalencia se probó por eso código-viejo vs código-nuevo sobre los mismos insumos, no contra el archivo commiteado.

## P3 · perfil (py-spy, 50 Hz) y cuello
`registro` (seco) antes: 71.0 % en `_yaml_safe_load` → PyYAML **sin libyaml** (paquete de sistema `/usr/lib/python3/dist-packages`); el código ya prefería `CSafeLoader` pero caía al loader Python. Segundo cuello tras resolver el primero: 23.6 % propio en `corrida0.py:4117`, un `next(...)` lineal sobre `spec["resultados"]` por cada RESULT (O(n²)) → índice por CALC con la misma semántica de primera coincidencia.
`marcador_segmento`: 83 % en `_regla_ola5` re-parseando `milpa/tramite-ola5-propuesta-v0.yaml` **una vez por celda** → se parsea una vez por proceso; `_yaml` usa `CSafeLoader` si existe.

hyperfine (3 corridas, nube, 4 núcleos):
| comando | antes | después | razón |
|---|---|---|---|
| `corrida0.py registro` | 65.53 s ± 0.33 | 16.54 s ± 0.08 | 4.0× |
| `marcador_segmento.py` | 11.82 s ± 0.17 | 0.77 s ± 0.06 | 15.4× |
| `check.py --baseline --parallel` (una corrida) | 654.5 s | 261.2 s | 2.5× |
«Antes» = árbol `ae2a11e1` con libyaml ocultado por `sitecustomize` (el estado real de esta imagen). En CI, `pip` ya instalaba PyYAML con libyaml, así que ahí la ganancia es solo la del índice y la del marcador.

**Equivalencia byte a byte — VERDE.** sha256 de los textos de `corridas`/`resultados`/`usos` (vía `_texto_vista`, en memoria) y de `marcador-segmento.tsv` + `milpa/estimadores-por-segmento.yaml` (escritos y restaurados), código viejo sin libyaml vs código nuevo con libyaml: idénticos (`corridas 88919cc5…`, `resultados f2755b24…`, `usos fa0a53a8…`, `marcador-segmento 8ab89bb2…`, `estimadores 84486882…`). Además la salida de `registro` en seco es idéntica byte a byte. Guarda permanente: `tests/test_consulta.py::test_libyaml_equivale_a_loader_python`.

## P1 · CLAUDE.md
Sección «Reglas de lectura» + lista de derivados que se consultan. Guarda `tests/test_claude_md_lectura.py` (falla si `CLAUDE.md`, `.claude/**`, `docs/**` o un encargo instruye `cat <vista>`; hoy 0 hallazgos).

## P2 · tools/consulta.py
`result · corrida · celda · payload · fp · nc`, una línea, lector CSV en streaming, sin índice en disco (D-23; D-14: stdlib basta, 0.04 s por consulta; 0.3 s `payload`). Negativo con `filas examinadas=N` (A.13). Defecto encontrado por su test: `corridas.tsv` trae campos > 128 KB (límite de `csv`), se sube el límite. 10 tests.

## P4 · uv
Instalación de `requirements.txt` en venv limpio sin caché: pip 12.9 s → uv 1.3 s. Los cinco `pip install` de `verify.yml` pasan a `uv pip install --system`. `requirements-dev.txt` nuevo (uv, pytest-xdist, py-spy, yq). `ripgrep`/`jq` no se instalan en CI: ningún paso los usa (D-14).

## P6 · clon parcial
`docs/sesiones.md`: completo 28.6 s / 712 MB (.git 134 MB) → parcial 12.2 s / 601 MB (.git 80 MB). `/acto` ARRANQUE lo cita. Nota: `docs/` es el sitio de Pages; `sesiones.md` se publicará ahí (sin datos sensibles).

## Gate D-14 por pieza
P1/P2: defecto = lectura de vistas enteras; barato. P3: > 5 min medidos; 4×/15×. P4: minutos de instalación por job. P6: tiempo y disco de arranque. P5: diferido (abajo).
