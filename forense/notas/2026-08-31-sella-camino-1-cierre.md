# Nota de cierre · ACTO MAESTRA32-E19 · SELLA-CAMINO-1

31/ago/2026. Redactado contra `main = aa920f1` al arrancar; sin drift al
cerrar (CARRILES del encargo: "solo este acto; nada en paralelo hasta su
merge" — verificado, ningún otro merge llegó a `origin/main` durante la
sesión).

## ARRANQUE

1 · REPO: `/home/user/Modelado-Mexicano` (clon existente, no se clonó
otro). `git log -1` → `aa920f1 Merge pull request #408 from
Josanoforo/acto/maestra32-e18-reglas-ola5-fase1`. `git status`: limpio,
rama `claude/maestra32-e19-launch-nza01w` ya existente.
2 · SHA: coincide con el declarado por el encargo (`aa920f1`, merge PR
#408/`ADR-236`). Sin drift.
3 · `data/raw`: ausente (`ls data/raw/ 2>/dev/null | head -1` → sin
salida). No es PARO — este acto no descarga ni abre microdato.
4 · ENTORNO: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`. Este
acto no toca microdato ni red (repo-only, per encargo) — sonda de red no
corrida, declarado en vez de simulada (A.13: cero archivos examinados no
es un negativo, así que no se reporta ningún veredicto de red).
5 · ESPEJO: no se derivó ninguna cifra del espejo del proyecto; las
fracciones `ASIGNADO` de `canon/motor-nucleo-medible-v1_0.md` se
derivaron con `yaml.safe_load` contra `milpa/procedencia.yaml` y
`milpa/tramite.yaml` del clon, comando a la vista en el propio archivo.

A.2 tercera parte: `ls data/raw/ 2>/dev/null | head -1` → sin salida
(ausente), consistente con el punto 3.

## Verificación de existencia — re-verificada al arrancar

`.claude` (`ls -d .claude`) → no existía. `canon/motor-nucleo-medible-v1_0.md`
y `forense/encargos/PLANTILLA-LOTE-v1_0.md` (`ls canon/
forense/encargos/`) → NO-ENCONTRADO, confirmando el barrido de dirección.
`ls instrucciones-proyecto-v2_*.md | sort -V` → `v2_4` … `v2_9` `v2_10`
`v2_11`, máximo `v2_11` — confirmado, no hay PARO.

## Hallazgo de ARRANQUE: `.gitignore` ignoraba `.claude/`

D-10 exige que la skill `/acto` "viva en el repo, versionada". `.gitignore`
línea 14 (antes de este acto) traía `.claude/` a secas, bajo el bloque
"dotfiles de entorno del sandbox, ajenos al repo, nunca trackeados" — un
terreno distinto al que el encargo supone (A.1). Sin corregirlo, `git add
.claude/commands/acto.md` fallaba en silencio (o exigía `-f`, que habría
sido el atajo equivocado: hubiera versionado el archivo sin arreglar la
regla, y el próximo archivo nuevo bajo `.claude/` habría vuelto a
fallar). Fix aplicado: `.claude/*` + `!.claude/commands/` — destraba solo
la carpeta de skills, el resto de `.claude/` (settings locales, estado de
sesión) sigue fuera del repo. Verificado con `git check-ignore -v`: la
skill queda trackeable, un archivo de prueba bajo `.claude/otro/` sigue
ignorado.

## Fracciones `ASIGNADO` — re-derivación (ver también `canon/motor-nucleo-medible-v1_0.md` §2)

Coeficientes: **8 de 15**, confirma la cifra de mesa (F-ALCANCE).
Reglas de `milpa/tramite.yaml`: **5 de 5** hoy — difiere de la "4 de 5"
de mesa. No es una corrección de mesa: es la distinción entre "medido en
algún punto del árbol" (que sí activa el dominio trámite, F-ALCANCE §1) y
"cargado en el archivo que el motor ejecuta" (que sigue en 0 de 5 hasta
que `FP-200` selle la carga de `tramite-ola5-propuesta-v0.yaml`). Ambas
cifras quedan escritas, con su universo y su comando, en
`canon/motor-nucleo-medible-v1_0.md` §2.2-2.3.

## A.9 — condición previa sin verificar en esta sesión

El encargo exige una línea declarativa fechada, en el mensaje de
lanzamiento, de que mesa pegó el delta v2.12 en las instrucciones del
proyecto de Claude — para que el ADR la cite verbatim. Este ejecutor
recibió el archivo completo de v2.12 (adjunto al lanzamiento) y lo usó,
verbatim, para construir `instrucciones-proyecto-v2_12.md` — pero ningún
mensaje de esta sesión trae esa línea declarativa con fecha. No se
inventa la cita: `FP-203` queda `ABIERTA` para que mesa la declare. El
resto del acto se sella igual, porque el repo es la fuente de verdad para
todo lo que no sea esa condición específica (A.9 la exige como condición
del sello de la *versión de instrucciones*, no del resto del acto).

## F-DD — fuentes web (benchmark pedido por mesa: "haz benchmark web de cómo manejarlo")

**Calibration target (P0) vs. validación externa (P1) — el estándar
adoptado es la distinción de validez del reporte ISPOR-SMDM Task
Force-7:**

- Eddy DM, Hollingworth W, Caro JJ, Tsevat J, McDonald KM, Wong JB.
  "Model transparency and validation: a report of the ISPOR-SMDM
  Modeling Good Research Practices Task Force–7." *Value in Health*,
  2012. El reporte distingue face validity, verificación/validez
  interna, cross-validity (contra otros modelos), **validez externa**
  (contra resultados del mundo real) y **validez predictiva**
  (contra eventos observados prospectivamente) — nombrando estas dos
  últimas como las formas más fuertes de validación. Es la base directa
  de la regla operativa de F-DD: una celda de la misma ola/instrumento
  que calibró `p` es verificación (P0, no puntúa); una celda de otra
  ola u otro instrumento es validación externa (P1, puntúa).
  - ISPOR (resumen oficial): https://www.ispor.org/heor-resources/good-practices/article/model-transparency-and-validation
  - PubMed: https://pubmed.ncbi.nlm.nih.gov/22990088/
  - ScienceDirect (artículo): https://www.sciencedirect.com/science/article/pii/S1098301512016567

**"Targeted validation" — el conjunto de validación se elige por
relevancia, no por conveniencia:**

- Sperrin M, Riley RD, Collins GS, Martin GP. "Targeted validation:
  validating clinical prediction models in their intended population
  and setting." *Diagnostic and Prognostic Research*, 2022. El paper
  nombra explícitamente el defecto que F-DD evita: validar con datasets
  "elegidos por conveniencia" en vez de por relevancia al uso
  pretendido del modelo, lo que produce hallazgos potencialmente
  engañosos. Es la base de que el marco-M puntúe con celdas de otra
  ola/instrumento *relevante* al desenlace, no con cualquier celda
  externa disponible.
  - PMC (texto completo): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9773429/
  - Diagnostic and Prognostic Research (artículo): https://diagnprognres.biomedcentral.com/articles/10.1186/s41512-022-00136-8
  - PubMed: https://pubmed.ncbi.nlm.nih.gov/36550534/

## Cascada — resumen (detalle en `canon/gobernanza-v1_15.md`, `ADR-237`)

`ADR-237` (236→237 ADR, sin huecos). `canon/estado-programa-v1_10.md`:
recifra en `L0` y en la tabla de artefactos de §0. `forense/firmas-pendientes.tsv`:
`FP-202` (recibo), `FP-203` (A.9 sin verificar), ambas nuevas, `ABIERTA`.
`canon/registro-rotulos.tsv`: `MAESTRA32-E19` y `E20` censados. `tests/check.py`:
`_T25_ARCHIVOS_CONOCIDOS` extendido con el encargo (bare `E18`/`E20` en
prosa narrativa, `E18` ya censado). `python3 tests/check.py --baseline`:
**VERDE**, sin `FAIL` nuevo (19 FAIL/152 WARN preexistentes, sin cambio).
Anti-PR#77: no aplica, este acto no descarga nada.

## `## CONSUMIDO`

Pendiente de PR — se añade al encargo archivado
(`forense/encargos/2026-08-31-MAESTRA32-E19-SELLA-CAMINO-1.md`) en el
mismo commit que abre o referencia el PR de este acto.
