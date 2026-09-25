# ENCARGO · ACTO GEN2-TUBERIA-RENDIMIENTO-1 · Menos tokens por sesión y menos minutos por derivación: reglas de lectura en `CLAUDE.md`, herramientas de consulta de una línea, perfil del derivador y migración del cuello a DuckDB/Polars con equivalencia byte a byte, `uv` y suite en paralelo — todo medido antes/después

> ENTORNO: **NUBE** — código, tests, CI, documentación; cero microdato (la caché Parquet de microdato es una pieza declarada para CAJA, ver P5). Hook imprime ENTORNO-DERIVADO; si dice CAJA, solo corre P5.

CABECERA · SHA de redacción `8358b891` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-tuberia-rendimiento-1` (o la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** (cláusula v1.0 `3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta; **ningún número de ninguna vista cambia** (test de equivalencia byte a byte de `corridas.tsv`, `resultados.tsv`, `usos.tsv`, `marcador-segmento.tsv` antes/después de cualquier migración). Los contadores que este acto mueve son de tiempo: segundos de `registro --escribe`, del marcador y de la suite, medidos con `hyperfine` y pegados.

## 1 · OBJETIVO
Gate D-14 por pieza: defecto real ya observado · puede cambiar una medición o decisión · cuesta menos que corregirlo. Las seis piezas lo pasan; la nota lo declara por pieza.
- **P1 · Tokens: `CLAUDE.md` con reglas de lectura** (hoy no existe; `AGENTS.md` no las tiene). Defecto real: sesiones que hacen `cat` de `resultados.json` (1 346 filas) o de `manifiesto.yaml` (15 000+ líneas) para leer un dato. Reglas: `wc -l` antes de abrir; nunca `cat`/`view` completo de un archivo > 200 líneas; `head`/`tail`/`sed -n`; `grep -c`/`rg -c` antes de listar; `git diff --stat` antes de `git diff`; `pytest -q | tail`; TSV grandes solo por lector CSV con `islice`; JSON/YAML por `jq`/`yq`; consultas de RESULT por `tools/consulta.py` (P2). Más: qué archivos son derivados y no se leen (las vistas se consultan, no se leen).
- **P2 · `tools/consulta.py`**: subcomandos de una línea de salida: `result <id>` (valor, unidad, tipo, CALC, hash, `cuenta_gen2`, adopción), `corrida <CALC>` (sello, spec, n RESULT, replay), `celda <celda-D>` (champion, dictamen, n), `payload <id>` (manifiesto: sha, estado, reserva), `fp <id>` / `nc <id>` (fila del TSV). Lee las vistas y el manifiesto por índice (DuckDB sobre los TSV, o un `sqlite` de caché regenerado por comando y marcado derivado), nunca `cat`. Test por subcomando.
- **P3 · Perfil y cuello**: `py-spy record` sobre `registro --escribe` y `marcador_segmento.py --escribe` (hoy > 5 min juntos); tabla de dónde se va el tiempo; migrar **solo el cuello** (lectura/escritura de vistas, joins, agregaciones) a DuckDB o Polars, con equivalencia byte a byte de las cuatro vistas y `hyperfine` antes/después. Si el cuello es I/O de JSON, `orjson`; si es pandas, Polars; si es el join de vistas, DuckDB. El perfil manda, no la preferencia.
- **P4 · Instalación y suite**: `uv` (`requirements.txt` + `uv.lock`; `uv pip install` en CI y en `/acto`), `pytest-xdist` (`-n auto`) en `check.py`/CI para los 1 349 tests; `ripgrep`, `jq`, `yq` en `requirements-dev`/apt de CI. Tiempo de instalación y de suite antes/después.
- **P5 · Caché Parquet de microdato (CAJA)**: `tools/cache_parquet.py <id>`: convierte el payload del manifiesto (`.dta`/`.sav` vía `pyreadstat`, `.dbf` vía `dbfread`, `.csv`) a `data/cache/parquet/<id>.parquet` con el sha del payload origen en el nombre o en metadatos; **fuera del manifiesto y del corpus sellado** (es caché: se regenera; el sello sigue siendo el payload); `.gitignore`. Los medidores pueden leerla si existe y caer al payload si no; ningún RESULT cambia (test sobre un CALC sellado: mismo `resultados.json` leyendo de Parquet y de origen). Si la sesión es de nube, P5 se declara `DIFERIDO-A: sesión de caja` y no es PARO.
- **P6 · Clones parciales**: receta y comando en `docs/sesiones.md` (`git clone --filter=blob:none` + `sparse-checkout` por tipo de acto: nube sin `corpus/` ni `data/curacion-universo/`); `/acto` ARRANQUE la cita. Medir tamaño y tiempo de clon antes/después.
«Hecho» sobre el commit final con origin/main fusionado: `CLAUDE.md` en raíz con las reglas y un test que falla si un `.md` de encargo o skill dice «cat» de una vista · `tools/consulta.py` con cinco subcomandos y tests · perfil pegado y cuello migrado con equivalencia byte a byte VERDE y `hyperfine` antes/después (al menos 2× en el cuello; si no se logra, la nota dice por qué y qué se migró) · `uv.lock` y `pytest -n auto` en CI con tiempos · `docs/sesiones.md` con la receta de clon parcial · P5 hecho o `DIFERIDO-A` con razón · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas, verbatim
**Mesa, 24/sep (chat):** «Necesito que revises qué otros programas o descargas podemos usar para mejorar el desempeño o reducir el impacto en consumo de las sesiones» y aprobación del documento `HERRAMIENTAS-rendimiento-y-consumo-2026-09-24.md` (dirección; se archiva como fuente). **D-14** (gate de automatización) y **D-23** (una herramienta de verificación no muta el clon; un comando que deriva no escribe estado) rigen cada pieza. **No cambia**: sha256 en el manifiesto; sin Git LFS; sin bases servidas.

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` (`8358b891`): `requirements.txt` = PyYAML, xlrd, markdown, jsonschema, openpyxl, numpy, pandas, pyreadstat, pytest; 103 módulos importan pandas/numpy (36 pandas, 33 numpy); `.git` 363 MB; archivos > 5 MB: vistas y TSV de curación (8–13 MB cada uno); 271 archivos de tests, 1 349 tests; `check.py` tiene `--rapido` y `--parallel` (solo T35). Microdato: 1 973 zips, 861 `.dta`, 593 `.csv`, 292 `.dbf`, 187 `.sav`. `CLAUDE.md` no existe; `AGENTS.md` sin reglas de lectura. `registro --escribe` + marcador: > 300 s en la máquina de dirección (comando abortado por límite). `[SUPUESTO]` que DuckDB y Polars instalan en nube (PyPI tiene egress, #1069) y que la CI tiene `apt`. `[SUPUESTO]` que ningún consumidor depende del orden de bytes de las vistas más allá de lo que el test de equivalencia captura; si uno sí, se declara.
ADJUNTOS: `HERRAMIENTAS-rendimiento-y-consumo-2026-09-24.md` (sha256 al lado; se archiva en `forense/encargos/fuentes/`).

## 4 · YA HECHO / YA DECIDIDO
`ls CLAUDE.md tools/consulta.py uv.lock 2>/dev/null` → nada. `grep -c xdist requirements*.txt tests/check.py` → 0. `git ls-remote --heads origin | grep -i rendimiento` → 0. VISTA-2/-3 (#1113, #1121) ya normalizaron `resultados.tsv` (< 50 MB re-derivado): P3 parte de ahí.

## 5 · PIEZAS
P1 → P2 → P3 (perfil primero, migración después) → P4 → P6 → P5 (caja, o diferido). Cada pieza con su medición antes/después en la nota.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar. 7. El «Hecho» no se rebaja; lo no alcanzado va a NO-CORRIDO. Elección de librería (DuckDB vs Polars vs orjson): la decide el perfil; si el perfil no distingue, DuckDB. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir microdato reservado para probar la caché (P5 usa solo olas abiertas) · b) cambiar un byte de una vista publicada, un sello, un RESULT, o el algoritmo de hash del manifiesto · c) mover contadores a mano · d) cambiar un procedimiento de medición (los medidores sellados no se tocan; la caché es transparente) · e) —

## 8 · COMPUERTAS
«Equivalencia byte a byte de las cuatro vistas antes de fusionar cualquier migración» protege: **congelar** (una vista distinta es una publicación distinta). «Caché Parquet fuera del manifiesto y del corpus; mismo `resultados.json` con y sin caché» protege: **congelar** (E.2: el sello es el payload). «Perfil antes de migrar» protege: **borrar** (D-14: no se construye lo que no ataca un defecto medido).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `CLAUDE.md` (nuevo), `docs/sesiones.md`, `tools/consulta.py` + tests, `tools/cache_parquet.py` + test (P5), `tools/corrida0.py` **solo** en las funciones que el perfil marque (lectura/escritura de vistas) y `tools/marcador_segmento.py` ídem, con equivalencia probada, `requirements.txt`/`requirements-dev.txt`/`uv.lock`, `tests/check.py` (paralelismo), `.github/workflows/verify.yml` (instalación con `uv`, `apt` de `ripgrep`/`jq`, `pytest -n auto`), `.gitignore` (`data/cache/`), `.claude/commands/acto.md` (una línea en ARRANQUE citando `docs/sesiones.md`), `forense/encargos/fuentes/HERRAMIENTAS-…md`, nota, L0, cascada. Ajeno: medidores sellados (`data/corrida0/CALC-*/medidor.py`), vistas (solo por derivador), manifiesto, `registro`'s semántica (solo su rendimiento), el paso de derivados que TABLERO-EN-CANAL-1 está editando (**coordinar: si TABLERO-EN-CANAL no ha fusionado, P4 no toca ese paso; rebasa y añade `uv`/`-n auto` en el suyo**). En vuelo: TABLERO-EN-CANAL-1 (CI), INFORME-V1-3-1, RELEVO-MOTOR-34-1, FRONT-2 (nube; sin archivos comunes salvo `verify.yml`), los cinco de caja (P5 puede ejecutarse en una de esas sesiones al cerrar, si les sobra tiempo; se declara quién).

## 10 · LO QUE NO HACE · SUCESORES
No reescribe los 103 módulos de pandas; no cambia formatos de publicación (TSV sigue siendo la vista humana); no adopta ni mide. Sucesores: `-2` si el perfil revela un segundo cuello después del primero; `docs/sesiones.md` se actualiza por quien toque `/acto`.

## NO-CORRIDO / RESERVAS

- P5 · caché Parquet de microdato — DIFERIDO-A:sesión de caja — medidores siguen leyendo el payload — sucesor: GEN2-TUBERIA-RENDIMIENTO-2 (`NC-260924-GEN2-TUBERIA-RENDIMIENTO-1-ae2a-01`)
- P4 · `pytest -n auto` en check.py/CI; apt ripgrep/jq — DIFERIDO-A:GEN2-TUBERIA-RENDIMIENTO-2 — check.py no es pytest; los pytest corren por `tools/ci_guardias.py` (fuera de §9) — sucesor: GEN2-TUBERIA-RENDIMIENTO-2 (`…-ae2a-02`)
- P4 · `uv.lock` — DIFERIDO-A:GEN2-TUBERIA-RENDIMIENTO-2 — requiere `pyproject.toml` (fuera de §9) — sucesor: GEN2-TUBERIA-RENDIMIENTO-2 (`…-ae2a-03`)
- P3/P4 · tiempos de CI antes/después — NO-VERIFICABLE-AQUÍ — se leen en los logs de CI del PR — sucesor: GEN2-TUBERIA-RENDIMIENTO-2 (`…-ae2a-04`)

## CONSUMIDO

Ejecutado por PR #1131 (`claude/new-session-6fcgwp`), ADR `ADR-260924-GEN2-TUBERIA-RENDIMIENTO-1-ae2a-01`. Nota: `forense/notas/2026-09-24-GEN2-TUBERIA-RENDIMIENTO-1-cierre.md`.
