# ENCARGO · ACTO 1 · PURGA-EJECUTA — ejecuta `FP-143` (destrucción de `~/mm-purga.git`)

> | | |
> |---|---|
> | **REDACTADO POR** | dirección/mesa, 25/ago/2026 — transmitido en dos mensajes al ejecutor de este worktree: FASE A (solo lectura y medición) y FASE B (escritura), ambos citados y pegados verbatim abajo |
> | **FIRMA QUE EJECUTA** | `FP-143`, `FIRMADA` desde `ADR-168` (`L5`/`FP-63`, `firmas-pendientes.tsv:141`) — cadena verbatim `AUTORIZO DESTRUIR mm-purga.git`, dada por mesa en el lanzamiento de `ACTO SELLA-AGO25-F` |
> | **SHA DE REDACCIÓN** | `26ea239` (`origin/main` al escribirse; el acto corrió íntegro contra esta base en el worktree `/home/pc0/mm-purga-ejecuta`, rama `purga-ejecuta`) |
> | **ENTORNO ASIGNADO** | **UBUNTU** — la destrucción física de `~/mm-purga.git` exige acceso de disco al espejo. **NO NUBE**, explícito en el propio texto del acto y en la columna `gatea` de `FP-143` |
> | **ESTADO** | **CONSUMIDO** — ver `forense/notas/2026-08-25-purga-ejecuta.md` y `ADR-169` (`canon/gobernanza-v1_15.md`) |
> | **PEGADO VERBATIM** | Los bloques "Texto del acto" y "Reglas comunes del PACK" de abajo son el mensaje del coordinador tal como llegó, sin editar (`A.3`) |

---

## Texto del acto, verbatim

ACTO 1 · PURGA-EJECUTA — ejecuta FP-143 (L5, cadena ya registrada) (Sonnet; contador: cero) TAREAS: (1) lee la cadena verbatim del registro de #338 (fila FP-143/ADR — cítala del repo, no de memoria); (2) verifica una última vez la premisa refutada (el espejo no conserva historia: git -C ~/mm-purga.git log --oneline | head y fsck, pega salidas); (3) destruye ~/mm-purga.git; (4) FP-143 y FP-63 → ejecutadas con las salidas crudas; una línea en hallazgos. PERÍMETRO: tablero · gobernanza · estado · nota 2026-08-25-purga-ejecuta.md · encargo · el directorio ~/mm-purga.git (fuera del repo, destino declarado).

## Reglas comunes del PACK, verbatim

🚫 --freeze · pgrep -af claude · iconv -f utf-8 -t utf-8 -c · ⚠️ [v2.11] A.13 en todo negativo · nada del espejo · ADR re-derivado, renumera si colisiona · recifrado con punto fijo · suite VERDE con tail · encargo CONSUMIDO · fuera del perímetro: PARA.

## ARRANQUE (A.2, tres partes) — medido por el supervisor antes del lanzamiento

`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → `sin_variable` (env sin `ANTHROPIC_*`) · sonda `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200` · `ls data/raw/ | head -1` → `2005trim1_csv.zip` (321 entradas, corpus montado). `pgrep -af claude` → solo el propio shell. Repo: `/home/pc0/mm-purga-ejecuta`, rama `purga-ejecuta`, `HEAD = 26ea239` al arrancar FASE A, sin PARO.

## VERIFICACIÓN DE EXISTENCIA (Parte 2 de `A.8`, `instrucciones-proyecto-v2_7.md` Bloque D-ter)

**1 · ESTRUCTURA.** Tabla que gobierna este dominio: `forense/firmas-pendientes.tsv` (el tablero de firmas; `A.12`) y `canon/gobernanza-v1_15.md` (el registro de ADR). Este encargo escribe ambas, más el recifrado obligatorio en `canon/estado-programa-v1_10.md` y una línea en `forense/hallazgos.md`. Deliberadamente no escribe ningún índice de `data/INFRAESTRUCTURA-v1_0.md`: el acto ejecuta una compuerta física sobre un artefacto fuera del repositorio, no mide nada sobre México.

**2 · CONTENIDO.** Comando y salida que demuestran que la ejecución no existía ya, corridos antes de escribir: `awk -F'\t' '$1=="FP-143"{print $8}' forense/firmas-pendientes.tsv` → cadena vacía (columna `ejecutada_en`, `NO-ENCONTRADO`: se buscó y no había ejecución previa registrada). `test -e ~/mm-purga.git` (FASE A, antes de la destrucción) → `EXISTE-SATISFACE` (exit 0): el objeto a destruir estaba ahí. `awk -F'\t' '$1=="FP-63"{print $8}'` → cadena vacía, mismo vocabulario.

**3 · COBERTURA RETROACTIVA.** `FP-143` nace el 25/ago/2026 (`git log --diff-filter=A -- forense/firmas-pendientes.tsv` la sitúa en el mismo commit que abre `ADR-168`, `PR #338`), misma fecha en que este acto corre: sin hueco retroactivo que declarar.

## PERÍMETRO

`forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · `forense/hallazgos.md` · `forense/notas/2026-08-25-purga-ejecuta.md` · este encargo · el directorio `~/mm-purga.git` (fuera del repositorio, destino declarado de la destrucción, ejecutada por el supervisor) y, solo en lectura, `~/BACKUP-mm-mirror-2026-08-10.git`. Fuera de esta lista: PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo. Concurrencia detectada y declarada: `origin/main` avanzó de `26ea239` a `96dcc6c` durante el acto (`PR #339` — `ACTO PROPAGA-330-337`, `ACTO ESCALA-ASIGNADOS`, `ACTO SORTEO-V2-PROPUESTA`); no toca ninguno de los archivos de este perímetro salvo `forense/firmas-pendientes.tsv` (dos filas ajenas, `FP-96`/`FP-97`/`FP-133`/`FP-134`/`FP-141`/`FP-145` reciben `ejecutada_en`, y nacen `FP-149`/`FP-150`) y `canon/estado-programa-v1_10.md` (zona distinta a la tocada aquí, verificado línea por línea antes de editar); renumera quien fusiona segundo.

## Desviación de nomenclatura, declarada por el ejecutor

El encargo lleva el sufijo `-espejo` que su propio nombre de archivo exige (`convencion.md`: "el archivo de encargo lleva el código del acto como prefijo tras la fecha"); la nota no lo lleva (`2026-08-25-purga-ejecuta.md`) — normalizados por `T02` (`unicodedata` + `[^a-z0-9]` fuera) dan `20260825purgaejecutaespejomd` y `20260825purgaejecutamd`, distintos: sin colisión. Mismo patrón que `ACTO U2-CRUCE` fijó con el sufijo `-cierre`.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-25-PURGA-EJECUTA-espejo.md" canon/gobernanza-v1_15.md` → 2: citado bajo ADR-169 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
