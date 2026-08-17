# ACTO E-HIG · HIGIENE-VIVOS — reconciliar el estado de los encargos archivados contra el árbol

Ejecuta el encargo `forense/encargos/2026-08-17-EHIG-higiene-vivos.md` (transferido por dirección, SHA de redacción `f3873c2`). Entorno: nube, `cloud_default`, repo-only. NO toca `data/**` ni `tools/curador_registro/**` (perímetro de BARRIDO-2) ni ningún archivo `*BARRIDO-2*` ni `2026-08-12-encargos-finales-plan-descargas-completo*.md`.

## 0 · ARRANQUE

```
$ pwd
/home/user/Modelado-Mexicano
$ git log -1 --format="%h %s"
f3873c2 Merge pull request #240 from Josanoforo/claude/tablero-firmas-mecanismo-tocpwi
$ git status
On branch claude/higiene-vivos-4vsf9w
nothing to commit, working tree clean
$ git diff f3873c2 HEAD --stat
(vacío — la rama nace exacta en el SHA declarado)
```

`data/raw`: no se toca. `ESPEJO`: prohibido para cifras — cada cifra de esta nota sale de este clon, comando a la vista.

**Nota metodológica, declarada porque casi produce un PARO falso.** El clon en el que arrancó esta sesión era **superficial** (`git rev-parse --is-shallow-repository` → `true`, `.git/shallow` con 12 commits frontera, entre ellos `11083af`). Contra ese clon, `git merge-base --is-ancestor` daba **negativo** para tres PR (#172, #173, #175) que en realidad sí están fusionados — no porque no lo estén, sino porque el clon no tenía la historia completa para probarlo. Diagnosticado antes de escribir ningún veredicto (`git rev-list --count 11083af` → `1`, commit sin padres — la huella de una frontera superficial, no de una reescritura de historia) y corregido con `git fetch --unshallow origin` (`git rev-parse --is-shallow-repository` → `false` después). Todo el trabajo de abajo corre contra el clon ya completo. Se declara aquí porque, sin este paso, tres de los diecisiete veredictos habrían salido `VIVO` por un artefacto de herramienta, exactamente la clase de error que este acto existe para atrapar en otros — y el criterio (iii) de abajo no hace excepción por la fuente del error.

## 1 · Qué gobierna

`forense/encargos/convencion.md` (leída íntegra): ciclo de vida `VIVO` → `CONSUMIDO`, con el PR que lo ejecutó; un encargo consumido no se borra. Precedente directo: `forense/notas/2026-08-13-e2-cierre.md` §5 corrigió tres `VIVO` falsos con el mismo método (`git log --grep="#N"` → merge commit, `git merge-base --is-ancestor <merge> <HEAD>` → confirma). Este acto repite ese método a escala del ANEXO completo.

## 2 · Commit 1 — criterios congelados ANTES de adjudicar

**(i) La lista de candidatos es el ANEXO del encargo, cerrada.** Diecisiete archivos, ninguno añadido ni quitado por esta sesión:

`2026-08-05-m5bis-cierre-inventarios-catalogo-cruce` · `2026-08-11-A-renglon-llaves` · `2026-08-11-E4b` · `2026-08-12-B-estimador-contraste` · `2026-08-12-C-universo-minimo` · `2026-08-12-sonda1-mapa-barreras-lote2` · `2026-08-12-veredicto-pr185-mapeo-universo-map-b` · `2026-08-13-BE-benchmark-enlace-invarianza` · `2026-08-13-ENASIC-SPLIT` · `2026-08-13-MOTOR-COND-v2-encargos-finales` · `2026-08-13-PROC-10-BIS-clase-septima-y-anexos` · `2026-08-13-RP-reconcilia-puertas` · `2026-08-13-censo-v1_1` · `2026-08-13-encargo-c-capa3-reconcilia` · `2026-08-13-enlace1-mapeo-id-manifiesto` · `2026-08-13-r5-1-d3` · `2026-08-14-RECONCILIA-SPEC-encargo`.

**(ii) Vocabulario, cerrado, sin inventos:**

- `CONSUMIDO — PR #N` exige merge verificado: `git log --grep="#N"` (o el nombre de rama que el propio encargo declara) → commit de merge · `git merge-base --is-ancestor <merge> f3873c2` → `OK` · y correspondencia acto↔encargo **leída** (el PR cierra exactamente lo que este encargo pedía — nombre de rama, archivos del perímetro, o cita cruzada en otro documento del repo), no supuesta por coincidencia de fecha o de tema.
- `SUPERADO POR <acto> · decisión de mesa <fecha>` exige cita textual de la decisión. Único precedente utilizable hoy: las decisiones del encargo BARRIDO-2 — que, verificado (`grep -rl "BARRIDO-2" forense/`), **no está archivado todavía** en `forense/encargos/` (corre en paralelo, ejecutado por Codex, fuera del perímetro de este acto). Sin una decisión citable disponible hoy, este vocabulario no se usa en ningún veredicto de abajo — no porque no aplique en principio, sino porque no hay cita que pegar.
- `VIVO` se queda `VIVO` anotando razón + gate vigente. Los gateados por la ley de mesa —todo lo que calcule: `E4a`, `E4b`, `E4c-commit4`, `B-estimador-contraste`, `r5-1-d3`, `BE-benchmark` (lista de dirección; de estos, `E4a` y `E4c-commit4` no están en el ANEXO de este acto)— se anotan `VIVO — gateado por ley de mesa hasta cierre de BARRIDO-2` **solo si el comando no muestra ya un merge**. Ver (iii): tres de los seis nombrados por dirección resultaron ya fusionados al comprobarlo, y el veredicto es el que el comando produjo, no el que la lista presumía.
- La frase: **"el primer resultado que produzca este procedimiento es el que se reporta."**

**(iii) Nada se marca por memoria, espejo o transfer: cada veredicto lleva su comando — incluida la propia clasificación de dirección.** La lista de "gateados por ley de mesa" que trae el encargo es una presunción de dirección, no una verificación; se trató como tal. Resultado al comprobar los cuatro nombres de esa lista que sí caen en el ANEXO:

- `E4b`: **fusionado** (PR #173 + PR #185) — la clasificación de partida era incorrecta.
- `B-estimador-contraste`: **fusionado** (PR #172) — incorrecta. Además, el propio encargo declara en su cierre "este acto no mueve ningún contador sustantivo: entrega el mecanismo, no la medición" — nunca fue una cifra de canon a gatear.
- `BE-benchmark`: **fusionado** (PR #210) — incorrecta. Su perímetro nunca tocó `canon/` ("sellar D-ABC es de mesa con este benchmark enfrente"); lo que se gatea es sellar `D-ABC`, un acto futuro distinto, no este encargo.
- `r5-1-d3`: **sin evidencia de ejecución propia** — la clasificación de partida se sostiene. (Su gate original, `ADJ-4`, sí fusionó — PR #209 — pero eso no es lo mismo que R5.1-D3 haberse ejecutado; el diseño con pre-registro propio no tiene un solo commit en el árbol.)

No se corrige la lista de dirección en el encargo — sería editar cuerpo ajeno fuera de perímetro. Se corrige el veredicto de cada archivo, con su comando, y se declara la discrepancia aquí y en `hallazgos.md`.

**(iv) "El primer resultado que produzca este procedimiento es el que se reporta."** Un solo pase por archivo; ningún veredicto se re-corre buscando el resultado que "se sentía" más probable.

## 3 · Commit 2 — aplicación

Diecisiete veredictos, cada uno con su comando, aplicados **solo** a la línea de cabecera de `Estado` (+ una línea de evidencia) de cada archivo del ANEXO. Ningún otro texto de ningún encargo se edita. Detalle completo comando-por-comando abajo; resumen:

| # | Archivo | Veredicto |
|---|---|---|
| 1 | m5bis-cierre-inventarios-catalogo-cruce | `VIVO` — no ejecutado (gate M1-M4 propio nunca satisfecho; `forense/cruce-catalogo-fichas-v3_0.md` no existe) |
| 2 | A-renglon-llaves | `CONSUMIDO — PR #170` |
| 3 | E4b | `CONSUMIDO — PR #173` (+ PR #185, tercer commit autorizado por ADR-69(b)) |
| 4 | B-estimador-contraste | `CONSUMIDO — PR #172` |
| 5 | C-universo-minimo | `CONSUMIDO — PR #175` |
| 6 | sonda1-mapa-barreras-lote2 | `CONSUMIDO — PR #197` |
| 7 | veredicto-pr185-mapeo-universo-map-b | `CONSUMIDO — PR #189` (alcance: §3/MAP-B, lo único que el acto ejecuta) |
| 8 | BE-benchmark-enlace-invarianza | `CONSUMIDO — PR #210` |
| 9 | ENASIC-SPLIT | `CONSUMIDO — PR #206` |
| 10 | MOTOR-COND-v2-encargos-finales | mixto — desglose por sección (§2 ya `CONSUMIDO`; §3 → `CONSUMIDO — PR #235`; §4 → `CONSUMIDO PARCIAL — PR #232`; §5 → `CONSUMIDO — PR #233`; §6 sigue `VIVO`; ranura D3 → `RESUELTA`) |
| 11 | PROC-10-BIS-clase-septima-y-anexos | mixto — desglose por sección (§1 ya `CONSUMIDO`; §2 anotación aplicada río abajo; §3 → `CONSUMIDO PARCIAL — PR #232`) |
| 12 | RP-reconcilia-puertas | `CONSUMIDO — PR #208` |
| 13 | censo-v1_1 | `CONSUMIDO — PR #198` (ya corregido por ACTO E2 el 13/ago; reformateado para que la cabecera sea grep-detectable) |
| 14 | encargo-c-capa3-reconcilia | `CONSUMIDO — PR #202` |
| 15 | enlace1-mapeo-id-manifiesto | `CONSUMIDO — PR #196` (Commit 2 sí se completó, en sesión posterior con corpus montado) |
| 16 | r5-1-d3 | `VIVO — gateado por ley de mesa hasta cierre de BARRIDO-2` (gate original, ADJ-4/PR #209, ya satisfecho; sin ejecución propia en el árbol) |
| 17 | RECONCILIA-SPEC-encargo | `CONSUMIDO — PR #238` |

Los comandos de cada fila viven en el diff de cada archivo (línea de evidencia junto a `Estado`), no repetidos aquí para no duplicar la fuente.

## 4 · Conteo final

**13 `CONSUMIDO`** (archivo completo) · **2 `VIVO`** (m5bis, r5-1-d3, ambos con razón y gate) · **2 archivos mixtos** (`MOTOR-COND-v2`, `PROC-10-BIS`; de sus 9 sub-partes: 6 `CONSUMIDO`/`CONSUMIDO PARCIAL`, 1 `VIVO` [§6 MOTOR-2, mesa no ha sellado], 1 anotación no-ejecutable-por-sí-misma ya aplicada río abajo, 1 ranura resuelta) · **0 `SUPERADO`** (sin decisión de mesa citable disponible hoy, per (ii)).

## 5 · Suite y perímetro

```
$ python3 tests/check.py --baseline
```
Salida cruda y veredicto de línea base: ver cierre del PR. `git diff --check`: sin conflictos de espacio en blanco.

Perímetro respetado: cabeceras de `Estado` (+evidencia) de los 17 archivos del ANEXO · esta nota · `forense/hallazgos.md` (una entrada) · `forense/encargos/2026-08-17-EHIG-higiene-vivos.md` (A.3). Ningún cuerpo de encargo editado. `data/**`, `tools/curador_registro/**`, cualquier archivo `*BARRIDO-2*` y `2026-08-12-encargos-finales-plan-descargas-completo*.md` no se tocaron — verificado en el diff final antes de commitear.

**Contadores del programa movidos: 0.**
