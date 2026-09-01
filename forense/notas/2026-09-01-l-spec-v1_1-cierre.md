# Cierre — `ACTO MAESTRA33-E9 · L-SPEC-v1_1`

1/sep/2026, SHA de redacción `a71c9ea` (= HEAD al arrancar, sin diferencia que re-derivar). Entorno `NUBE` (`cloud_default`), `COMPUERTA: ninguna`.

## Arranque (resumen, detalle en el encargo)

- Repo: `/home/user/Modelado-Mexicano`, HEAD `a71c9ea`, working tree limpio.
- `data/raw/`: ausente, normal en clon fresco nube — no es PARO.
- Entorno: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (desviación del esperado `sin_variable`, declarada, sin consecuencia — este acto no toca microdato ni red real). Sonda: `curl … https://www.inegi.org.mx/` → `000`. `ls data/raw/` — 0 archivos examinados (A.13), directorio no existe.
- Espejo: no usado.

## A.8 verificado

- `pipeline-L-adv1-m2.py` existe, sellado (`llamar_modelo` lanza `NotImplementedError`), escrito para el marco piloto (`SpecCelda` con columnas `encuesta/ola/universo/variable/estimador/escala/frase_discriminacion`).
- `corridas-L/`: 120 archivos, todos `CIV-08__*` u otros ids del marco piloto — 0 del marco-M.
- `ls forense/prereg-duelo-v2/ | grep L-spec` — vacío antes de este acto.
- 11 celdas `elegible_v1_1=SI` en `marco-M-sorteado-v1_1.tsv` (verificado por script, `csv.DictReader` sobre la columna 32).
- 4 de esas 11 (`CIV-M-01/06/08/09`) tienen `R` en `forense/prereg-duelo-v2/corridas-R/` — verificado con `ls corridas-R/ | grep CIV-M`, `scoreboard-v1_1.md` nunca abierto.

## P1 — `L-spec-v1_1.json`

`forense/prereg-duelo-v2/genera_l_spec_v1_1.py` deriva `pregunta_L` mecánicamente (plantilla única `derivar_pregunta_l`, parametrizada por `conducta`/`universo`/`encuesta`/`ola`/`escala`). Reproducibilidad verificada: dos corridas consecutivas, `diff` vacío. `sha256sum -c L-spec-v1_1.sha256 --strict` → `OK`.

## P2 — `carga_l_v1_1.py`

Importa `pipeline-L-adv1-m2.py` por ruta de archivo (`importlib.util.spec_from_file_location`), sin editar el pipeline — verificado `git status --porcelain -- forense/prereg-duelo-v2/pipeline-L-adv1-m2.py` vacío tras el acto. Único modo `--dry-run`:

```
OK -- 11 celdas x 2 variantes x k=8 = 176 rutas de salida verificadas
OK -- 22 prompts construidos vía construir_prompt() (pipeline-L-adv1-m2.py, sin editar)
OK -- esquema de salida verificado contra CIV-08__L-solo__01.json
OK -- llamar_modelo() NO se invocó ni se implementó en este acto (NotImplementedError intacto)
Ejemplo de ruta: forense/prereg-duelo-v2/corridas-L/L-CIV-M-01-M__L-solo__01.json
```

## P3 — `PAQUETE-L-v1_1.md`

Comandos exactos para sesión limpia fuera del proyecto: compuerta de hashes, parámetros sellados (`claude-opus-4-6`, `temperatura=1.0`, `k=8`, ambas variantes — idénticos a `prereg-corrida-v1_0.md` F2, no re-declarados), comando de `carga_l_v1_1.py`, cómo trae los 176 archivos al repo (PR `[L] corridas v1_1`, el revisor comenta, no fusiona), prohibición explícita de abrir `corridas-R/`/`scoreboard-v1_1.md` durante la corrida.

## Archivos abiertos durante este acto (declarado, LO QUE NO HACE del encargo)

`marco-M-sorteado-v1_1.tsv`, `pipeline-L-adv1-m2.py`, `sorteo_v2.py`, un archivo de ejemplo de `corridas-L/CIV-08__L-solo__*.json`, `mesa-pendientes.md`, `lanzamiento-L-v1_0.md`, `prereg-corrida-v1_0.md`, `firmas-pendientes.tsv` (grep, no lectura completa). **Nunca abiertos:** `forense/prereg-duelo-v2/corridas-R/*.json`, `forense/prereg-duelo-v2/scoreboard-v1_1.md` (solo `ls`, confirmando existencia, nunca `cat`/`Read`).

## Cascada

- ADR re-derivado por comando: máximo `253` → candidato `254`, contiguo. Sin otro acto en vuelo conocido.
- `canon/gobernanza-v1_15.md` §4: entrada `ADR-254` insertada antes de `ADR-253` (texto viejo intacto). Cabecera `253 → 254 ADR`.
- `canon/estado-programa-v1_10.md`: `L0` recifra `253→254`, anotación nueva insertada antes de la de `ADR-253`/`SCORE-M-1`.
- `canon/registro-rotulos.tsv`: `MAESTRA33-E9` censado.
- `tests/check.py --baseline`: ver salida cruda en el cierre del PR — sin `FAIL` nuevo (verificado antes de push).
- Anti-`PR#77`: no aplica — este acto no descarga nada (no ejecuta `L`).
- `## CONSUMIDO` añadido a `forense/encargos/2026-09-01-MAESTRA33-E9-L-SPEC-V1_1.md` con el número de PR.
