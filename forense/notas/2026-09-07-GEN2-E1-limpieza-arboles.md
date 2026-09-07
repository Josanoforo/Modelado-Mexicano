# GEN2-E1 · LIMPIEZA-C1 — inventario de árboles, ramas y raíces (solo lectura)

Acto de solo-lectura: cero borrados, cero `git push`, cero cambios a ramas o
worktrees ajenos. La única escritura de este acto es esta nota, la fila nueva
de `forense/firmas-pendientes.tsv` y el cierre `## CONSUMIDO` del encargo
archivado — todo dentro de `mm-gen2-e1-limpieza-c1` (worktree propio de este
acto, creado desde `origin/main`, rama `acto/gen2-e1-limpieza-c1`). No se abre
PR (el encargo pide explícitamente "no empuja nada"): el resultado queda
committeado localmente para que mesa lo revise en esta misma máquina, y firme
la poda en un acto de mesa aparte (ver el encargo archivado para el rótulo de ese siguiente paso).

## §0 · Premisas y autodeclaraciones

- **`$HOME` = `/home/pc0`.** El barrido de clones corrió con `find "$HOME"
  -maxdepth 4 -type d -name .git`, tal como pide el encargo.
- **Corrección de método, declarada antes de leer resultado alguno:** ese
  comando literal solo puede encontrar clones cuyo `.git` es un *directorio*
  — el `.git` de un worktree enlazado (`git worktree add`) es un *archivo*
  (`gitdir: ...`), invisible a `-type d`. El comando encontró exactamente 2
  clones reales (`Modelado-Mexicano`, `mm-adq`) más 2 repos ajenos a este
  proyecto (plugins internos de `.codex`/`.codex-app`, no tocados ni
  explorados) más `/home/pc0/.git`, que **no es un repositorio funcional**
  (ver §4.1). El inventario real de árboles (Tabla 1) se construyó con `git
  worktree list --porcelain` sobre los 2 clones reales — eso sí encuentra los
  118 worktrees enlazados — y se contrastó contra el listado completo de
  `$HOME` para detectar huérfanas de verdad. Sin esta corrección, el barrido
  literal habría reportado "2 clones, 0 worktrees" y ocultado exactamente el
  problema que la mesa pidió investigar.
- **Esta misma caja.** `mm-gen2-e1-limpieza-c1` (rama
  `acto/gen2-e1-limpieza-c1`) aparece en la Tabla 1 con 1 commit propio y 1
  commit no empujado — es el commit A.3 de este mismo acto, por diseño ("no
  empuja nada"). No es hallazgo, se autodeclara para que un inventario futuro
  no lo confunda con un árbol huérfano.
- **PARO esperado.** `claude/encargo-maestra38-sello-3-6y5e0z` aparece en la
  Tabla 3 como rama remota sin worktree local, con un único commit cuyo
  asunto es literalmente `PARO: acto MAESTRA38-SELLO-3 ya en curso en otra
  rama` — confirma la expectativa del encargo, con evidencia directa (no solo
  el nombre de la rama).
- **Todo negativo con control positivo.** El primer barrido de "commits no
  empujados" corrió antes de un `git fetch` completo de `origin` (solo se
  había hecho `git fetch origin main`) y marcó 2 falsos positivos que
  desaparecieron al reintentar tras `git fetch origin
  '+refs/heads/*:refs/remotes/origin/*'`. Los números de la Tabla 1 son
  **post-fetch-completo**, reconfirmados dos veces con metodología distinta
  (por rama explícita, no `--not --remotes` sin punto de partida).

## §1 · Tabla 1 — clones y árboles (worktrees)

**2 clones reales:**

| clon | rama actual del propio clon | HEAD | commits atrás de `origin/main` |
|---|---|---|---|
| `Modelado-Mexicano` | `acto/maestra38-c1-re-asiento` | `1066145` | 111 |
| `mm-adq` | `acto/automatiza-2-e4-pdn-compara` | `62e9422` | 0 (7 propios encima) |

`Modelado-Mexicano` (el clon base) sigue posado en la rama de su última
tarea — cuyo PR **#577 ya se fusionó hoy, 2026-09-07 02:36 UTC** (verificado
con `gh pr view 577`). No es un árbol podable (es el clon base), pero
conviene devolverlo a `main` como higiene, no como hallazgo urgente. `mm-adq`
tiene 1 línea de `git status` sin comittear (`data/manifiesto-staging.yaml`)
y 7 commits propios ya empujados (0 no empujados) — trabajo vivo, no tocar.

**119 worktrees en total** (`git worktree list --porcelain`, contrastado
contra el listado completo de `$HOME` — coincide 100%, **0 prunable, 0
locked, 0 declarados-pero-ausentes-en-disco** según el propio git). De los
119: 2 son los clones de arriba, **117 son worktrees de tarea** (`worktree-
per-task`), en 3 patrones de ubicación distintos:

- 114 como hermanos directos de `$HOME` (`mm-<slug>` o `Modelado-Mexicano-
  <slug>`) — el patrón esperado.
- 2 anidados en `Modelado-Mexicano/.claude/worktrees/agent-<hash>` — creados
  por el propio mecanismo `isolation:"worktree"` del Agent tool de Claude
  Code, no por el flujo manual `mm-<slug>`. Ambos con PR ya fusionado
  (`#553`, `#552`).
- 1 anidado en `mm-worktrees/maestra33-e8-score-m-1` — SÍ está registrado
  correctamente en `git worktree list` (no es huérfana), solo vive en una
  ubicación no convencional un nivel más profundo.

**Clasificación de los 117 worktrees de tarea, cruzando cada rama contra el
historial COMPLETO de PRs del repo (598 PRs, no solo los de ramas que
siguen vivas en `origin` — ver nota metodológica en §3):**

| categoría | n | qué significa |
|---|---:|---|
| PR ya `MERGED` | 113 | trabajo ya aterrizado en `main`; el worktree es puro remanente |
| sin PR, 0 commits propios | 1 | nunca divergió de un punto viejo de `main`; nada que perder |
| **sin PR, con commits propios no empujados** | **2** | **evidencia real de trabajo en riesgo — ver §5, fila ABIERTA** |
| esta misma caja (acto en curso) | 1 | autodeclarada, ver §0 |

Tabla completa (119 filas, ruta relativa a `$HOME`, rama, HEAD corto,
commits atrás de `origin/main`, commits propios desde la base, commits NO
empujados (post-fetch-completo, ver §0), líneas de `git status --porcelain`,
estado de `data/raw`, PR si lo hay):

| ruta (bajo $HOME) | rama | HEAD | atrás de main | propios | no empujados | status | data/raw | PR |
|---|---|---|---:|---:|---:|---:|---|---|
| mm-autoridad-semantica-enif | codex/autoridad-semantica-enif | 26ea239 | 1456 | 0 | 0 | 5 | ausente | — |
| mm-gen2-e1-limpieza-c1 | acto/gen2-e1-limpieza-c1 | 59c5d76 | 0 | 1 | 1 | 0 | ausente | — |
| mm-maestra37-l2-mps-codebook | acto/maestra37-l2-mps-codebook-y-p3 | 05e6bef | 440 | 2 | 2 | 0 | OK-compartida | — |
| mm-maestra38-v1 | acto/maestra38-v1-corrobora-y-reconcilia | fd6e5bc | 365 | 1 | 1 | 0 | OK-compartida | — |
| Modelado-Mexicano | acto/maestra38-c1-re-asiento | 1066145 | 111 | 0 | 0 | 0 | OK-compartida | #577(MERGED) |
| Modelado-Mexicano-barrido2 | cond-atrib | 387ad82 | 1804 | 0 | 0 | 0 | OK-compartida | #263(MERGED) |
| Modelado-Mexicano-cruce-oferta-demanda | codex/cruce-oferta-demanda | 4679d30 | 1373 | 0 | 0 | 0 | ausente | #363(MERGED) |
| Modelado-Mexicano-maestra31-e4-orden-superior | maestra31-e4-orden-superior | 47c7de1 | 1275 | 0 | 0 | 0 | OK-compartida | #385(MERGED) |
| Modelado-Mexicano/.claude/worktrees/agent-a45c7ec89ca02c496 | acto/maestra38-a5-pdn-bulk-y-proxy | 986c63c | 211 | 0 | 0 | 0 | OK-compartida | #553(MERGED) |
| Modelado-Mexicano/.claude/worktrees/agent-a4f8a030e1f577254 | acto/maestra38-a4-adquiere-todo-lo-publico | 3908484 | 236 | 0 | 0 | 0 | OK-compartida | #552(MERGED) |
| mm-a4-registra-descargas | acto/maestra33-a4-registra-descargas-manuales | 98b9643 | 897 | 0 | 0 | 0 | OK-compartida | #440(MERGED) |
| mm-act-pil-2 | act-pil-2 | c2f8347 | 1625 | 0 | 0 | 0 | OK-compartida | #297(MERGED) |
| mm-adq | acto/automatiza-2-e4-pdn-compara | 62e9422 | 0 | 7 | 0 | 1 | OK-compartida | #580(MERGED) |
| mm-adq-corre-r74r75 | adq-corre-r74r75 | 0256c1a | 1510 | 0 | 0 | 0 | OK-compartida | #326(MERGED) |
| mm-adq-diseno-1 | adq-diseno-1 | b42355c | 1530 | 0 | 0 | 0 | OK-compartida | #320(MERGED) |
| mm-adq-enoe-pre2019 | adq-enoe-pre2019 | 7167cec | 1555 | 0 | 0 | 0 | OK-compartida | #310(MERGED) |
| mm-agente-adquisicion-1 | acto/maestra33-a1-agente-adquisicion-1 | 1efd335 | 1089 | 0 | 0 | 0 | OK-compartida | #414(MERGED) |
| mm-apertura-enfih-ensafi | apertura-enfih-ensafi | cd1169c | 1597 | 0 | 0 | 0 | OK-compartida | #302(MERGED) |
| mm-apertura-verifica | acto/maestra33-c7-apertura-verifica | f60bfc6 | 965 | 0 | 0 | 0 | OK-compartida | #431(MERGED) |
| mm-arbitra-r-lote-2 | acto/maestra33-c5-arbitra-r-lote-2 | 91652c8 | 996 | 0 | 0 | 0 | OK-compartida | #426(MERGED) |
| mm-arbitra-r-lote-3 | acto/maestra33-c6-arbitra-r-lote-3 | a90824e | 932 | 0 | 0 | 0 | OK-compartida | #436(MERGED) |
| mm-arbitro-r-1 | acto/maestra33-c2-arbitro-r-1 | fd20b4c | 1073 | 0 | 0 | 0 | OK-compartida | #417(MERGED) |
| mm-autoridad-semantica-marco | codex/autoridad-semantica-marco-enif | b3035ab | 1440 | 0 | 0 | 0 | ausente | #343(MERGED) |
| mm-autoridad-semantica-marco-produccion | codex/autoridad-semantica-marco-cobertura-total | 130ee53 | 1423 | 0 | 0 | 1 | OK-compartida | #349(MERGED) |
| mm-bibliotecario-56 | bibliotecario-56 | 523306f | 1486 | 0 | 0 | 0 | OK-compartida | #333(MERGED) |
| mm-c1-respec-corresidencia | acto/maestra33-c1-respec-corresidencia | 7c73afb | 1104 | 0 | 0 | 0 | OK-compartida | #412(MERGED) |
| mm-c8-medidor-fp172 | acto/maestra33-c8-medidor-fp172-diferidas | 546f45d | 961 | 0 | 0 | 0 | OK-compartida | #434(MERGED) |
| mm-codifica-r-1 | acto/maestra33-c3-codifica-r-1 | 40b1329 | 1022 | 0 | 0 | 0 | OK-compartida | #423(MERGED) |
| mm-coef-universo | coef-universo | e09bf17 | 1676 | 0 | 0 | 0 | OK-compartida | #287(MERGED) |
| mm-cola-enmienda3 | cola/enmienda-3-n3 | 5bf4df4 | 565 | 0 | 0 | 0 | ausente | #496(MERGED) |
| mm-corre-r10-1 | acto/corre-r10-1-v2-faseb | 7c1ee84 | 1321 | 0 | 0 | 0 | OK-compartida | #376(MERGED) |
| mm-e1-reloj-cruce | acto/e1-reloj-cruce | 5acb1b6 | 1291 | 0 | 0 | 0 | OK-compartida | #382(MERGED) |
| mm-e16-medidor-familismo | acto/maestra32-e16-medidor-familismo | 68a0570 | 1147 | 0 | 0 | 0 | OK-compartida | #406(MERGED) |
| mm-e18-p3-ola6 | acto/maestra33-e18-p3-reglas-ola6-activos-l1 | 7d0d79e | 857 | 0 | 0 | 0 | OK-compartida | #447(MERGED) |
| mm-e3-ejerce-compartamos | acto/e3-ejerce-llave-compartamos | f59b3a2 | 1326 | 0 | 0 | 0 | OK-compartida | #374(MERGED) |
| mm-e4-diseno-ensafi | acto/e4-diseno-ensafi | 5eab344 | 1336 | 0 | 0 | 0 | OK-compartida | #373(MERGED) |
| mm-e6-l-run | acto/e6-l-run | 11318e5 | 1314 | 0 | 0 | 0 | ausente | #377(MERGED) |
| mm-e7-r-scoring | acto/e7-r-scoring | 6572afd | 1307 | 0 | 0 | 0 | OK-compartida | #378(MERGED) |
| mm-e9-scoring-v2 | acto/e9-scoring-v2 | 93a2f41 | 1297 | 0 | 0 | 0 | OK-compartida | #381(MERGED) |
| mm-ensafi-descriptor | acto/ensafi-descriptor | e7426dd | 1351 | 0 | 0 | 0 | OK-compartida | #370(MERGED) |
| mm-eval-compartamos | eval-compartamos | 1066b2a | 1494 | 0 | 0 | 0 | OK-compartida | #331(MERGED) |
| mm-extractor-dta | acto/maestra32-e3-extractor-dta | b16833f | 1185 | 0 | 0 | 0 | symlink-indirecto | #400(MERGED) |
| mm-extractor-fd | acto/maestra32-e12-extractor-fd | 0ee032b | 1178 | 0 | 0 | 0 | OK-compartida | #401(MERGED) |
| mm-ficha-r51-d3 | ficha-r51-d3 | 6a5b115 | 1663 | 0 | 0 | 0 | OK-compartida | #290(MERGED) |
| mm-fp63-cierra | fp63-cierra | 6121036 | 1669 | 0 | 0 | 0 | OK-compartida | #291(MERGED) |
| mm-gemelas-20 | gemelas-20 | f1ed541 | 1444 | 0 | 0 | 0 | OK-compartida | #344(MERGED) |
| mm-generador-marco | codex/generador-marco | a8bc940 | 1496 | 0 | 0 | 0 | ausente | #332(MERGED) |
| mm-generador-marco-corpus-real | codex/generador-marco-corpus-real | 4a3a7d3 | 1470 | 0 | 0 | 0 | ausente | #337(MERGED) |
| mm-indice-no-inegi | indice-no-inegi | f8b0afb | 1443 | 0 | 0 | 0 | OK-compartida | #345(MERGED) |
| mm-l-corridas-v1-1 | acto/l-corridas-v1_1 | ba7bfa7 | 904 | 0 | 0 | 0 | ausente | #442(MERGED) |
| mm-l1-mordida-serie | acto/maestra34-l1-mordida-serie | b479ce3 | 839 | 0 | 0 | 0 | OK-compartida | #451(MERGED) |
| mm-l11-robustece-l9 | acto/maestra35-l11-robustece-l9 | f4e7ea5 | 570 | 0 | 0 | 0 | OK-compartida | #494(MERGED) |
| mm-l14-coercitivo | acto/maestra36-l14-coercitivo-tres-universos | 45bf1dc | 489 | 0 | 0 | 0 | OK-compartida | #508(MERGED) |
| mm-l16-bis-2 | acto/maestra38-l16-bis-2 | f45961e | 41 | 0 | 0 | 0 | ausente | #590(MERGED) |
| mm-l16-bis-paro | acto/maestra38-l16-bis | 3ecf2d4 | 87 | 0 | 0 | 0 | OK-compartida | #581(MERGED) |
| mm-l2-arbitra-v1_2 | acto/maestra34-l2-arbitra-v1_2 | 8300d9b | 833 | 0 | 0 | 0 | OK-compartida | #452(MERGED) |
| mm-l2-lista | acto/maestra38-l2-lista | 8f40a85 | 220 | 0 | 0 | 0 | OK-compartida | #554(MERGED) |
| mm-l3-corpus-sano | acto/maestra34-l3-corpus-sano-y-cngmd | dbc909f | 803 | 0 | 0 | 0 | OK-compartida | #458(MERGED) |
| mm-l3-salud | maestra37-l3-salud-a4 | e8a5372 | 453 | 0 | 0 | 0 | OK-compartida | #516(MERGED) |
| mm-l3bis | acto/maestra37-l3bis-salud-a4-v2 | ebc1d07 | 433 | 0 | 0 | 0 | OK-compartida | #520(MERGED) |
| mm-l4-civica-corpus | acto/maestra34-l4-civica-y-corpus | 694edd6 | 775 | 0 | 0 | 0 | OK-compartida | #464(MERGED) |
| mm-l5-gobierno-digital | acto/maestra34-l5-gobierno-digital-evasion-ahorro | 2ac29de | 746 | 0 | 0 | 0 | OK-compartida | #467(MERGED) |
| mm-l6-fuente-coercitivo | acto/maestra35-l6-fuente-coercitivo-y-puente | a5a9710 | 646 | 0 | 0 | 0 | OK-compartida | #480(MERGED) |
| mm-l6-homologacion | acto/maestra34-l6-civica-homologacion-escalonada | 81c22a1 | 738 | 0 | 0 | 0 | OK-compartida | #468(MERGED) |
| mm-l9-activos-l3 | claude/encargo-acto-maestra35-l9 | be3a139 | 580 | 0 | 0 | 0 | OK-compartida | #491(MERGED) |
| mm-limpia-caja | limpia-caja | e7ed4b8 | 1717 | 0 | 0 | 0 | OK-compartida | #278(MERGED) |
| mm-llave2-decreto | llave2-decreto | 28eacac | 1472 | 0 | 0 | 1 | OK-compartida | #336(MERGED) |
| mm-lote-cruce | acto/maestra38-lote-cruce | 472e494 | 104 | 0 | 0 | 0 | OK-compartida | #578(MERGED) |
| mm-lote-lapop | acto/maestra38-lote-lapop | 9ec8bf5 | 225 | 0 | 0 | 0 | OK-compartida | #551(MERGED) |
| mm-lote-retriage | lote-retriage | a4cf8fd | 1622 | 0 | 0 | 0 | OK-compartida | #298(MERGED) |
| mm-maestra31-e3-perimetro-alcanzable | acto/maestra31-e3-perimetro-alcanzable | 4c0a671 | 1282 | 0 | 0 | 0 | OK-compartida | #384(MERGED) |
| mm-maestra31-e6-diccionarios-fd | acto/maestra31-e6-diccionarios-fd | 2c4c947 | 1262 | 0 | 0 | 0 | OK-compartida | #387(MERGED) |
| mm-maestra31-e8-los-388 | acto/maestra31-e8-los-388 | b22f89a | 1246 | 0 | 0 | 0 | OK-compartida | #389(MERGED) |
| mm-maestra31-e9-estima-rutac | acto/maestra31-e9-estima-rutac | ccc21ed | 1240 | 0 | 0 | 0 | OK-compartida | #390(MERGED) |
| mm-maestra33-a3-adquiere2 | acto/maestra33-a3-adquiere-2-rutas-multiples | 0d66ea5 | 944 | 0 | 0 | 0 | OK-compartida | #433(MERGED) |
| mm-maestra34-a1-registra-2 | acto/maestra34-a1-registra-evalua-descargas-2 | 7f9c1d4 | 825 | 0 | 0 | 0 | OK-compartida | #453(MERGED) |
| mm-maestra35-a1 | acto/maestra35-a1-relanza | f79d109 | 639 | 0 | 0 | 0 | OK-compartida | #483(MERGED) |
| mm-maestra35-l1 | acto/maestra35-l1-recorre-y-segmenta | 45ec50a | 713 | 0 | 0 | 0 | OK-compartida | #471(MERGED) |
| mm-maestra35-l2 | acto/maestra35-l2-r-v1_2-completa | 9ea47ae | 701 | 0 | 0 | 0 | OK-compartida | #470(MERGED) |
| mm-maestra35-l3 | acto/maestra35-l3-civica-tipo-de-boleta | 8049879 | 691 | 0 | 0 | 0 | OK-compartida | #476(MERGED) |
| mm-maestra35-l4 | acto/maestra35-l4-r-v1_2-ciega | 1070274 | 590 | 0 | 0 | 0 | OK-compartida | #490(MERGED) |
| mm-maestra35-l5 | claude/l5-espejo-estado-programa | 0a96747 | 658 | 0 | 0 | 0 | symlink-indirecto | #482(MERGED) |
| mm-maestra35-l7 | acto/maestra35-l7-reglas-activos-l2 | 7373f30 | 611 | 0 | 0 | 0 | OK-compartida | #486(MERGED) |
| mm-maestra35-l8 | acto/maestra35-l8-civica-8-entidades | 98d3e77 | 620 | 0 | 0 | 0 | OK-compartida | #487(MERGED) |
| mm-maestra36-a1 | acto/maestra36-a1-escanea-recursivo | 17ca607 | 540 | 0 | 0 | 0 | OK-compartida | #500(MERGED) |
| mm-maestra36-l12 | acto/maestra36-l12-mps2012-crosstabs | 5756f59 | 513 | 0 | 0 | 0 | OK-compartida | #506(MERGED) |
| mm-maestra36-l13 | acto/maestra36-l13-coercitivo-sat-efirma | 36fdab1 | 521 | 0 | 0 | 0 | OK-compartida | #502(MERGED) |
| mm-maestra37-a1 | acto/maestra37-a1-registra-ensanut-v2 | 1bc9162 | 441 | 0 | 0 | 0 | OK-compartida | #518(MERGED) |
| mm-maestra37-a2-revisa-cola | acto/maestra37-a2-revisa-cola-a-detalle | 8eb341e | 399 | 0 | 0 | 0 | OK-compartida | #526(MERGED) |
| mm-maestra37-infra1 | claude/maestra37-infra-1-ssot-manifiesto-alta | f62a761 | 429 | 0 | 0 | 0 | ausente | #521(MERGED) |
| mm-maestra37-infra2 | claude/maestra37-infra-2-capa2-portabilidad | 9ca9da0 | 425 | 0 | 0 | 0 | ausente | #522(MERGED) |
| mm-maestra37-infra2-frented | claude/maestra37-infra-2-frente-d | 5a84f88 | 422 | 0 | 0 | 0 | OK-compartida | #525(MERGED) |
| mm-maestra37-l1-indexa | acto/maestra37-l1-indexa-descargas-mx-y-remapea-salud | a83ad41 | 474 | 0 | 0 | 0 | OK-compartida | #514(MERGED) |
| mm-maestra38-a1 | acto/maestra38-a1-sonda-y-descarga-universo-1 | 6838b5d | 381 | 0 | 0 | 0 | OK-compartida | #524(MERGED) |
| mm-maestra38-a2 | acto/maestra38-a2-recenso-y-regulariza-perimetro-real | e89d77a | 264 | 0 | 0 | 0 | OK-compartida | #543(MERGED) |
| mm-maestra38-a2-bis | acto/maestra38-a2-bis | 9659aa0 | 246 | 0 | 0 | 0 | OK-compartida | #549(MERGED) |
| mm-maestra38-a6 | acto/maestra38-a6-resondeo-negativos | 4d6bf07 | 192 | 0 | 0 | 0 | OK-compartida | #561(MERGED) |
| mm-maestra38-l2 | maestra38-l2-mps2012 | d3c368f | 168 | 0 | 0 | 0 | OK-compartida | #564(MERGED) |
| mm-maestra38-lote-ensanut | acto/maestra38-lote-ensanut | ce8f29d | 158 | 0 | 0 | 0 | OK-compartida | #565(MERGED) |
| mm-marco-m-sortea | acto/maestra32-e14-marco-m-sortea | 68eea44 | 1164 | 0 | 0 | 0 | ausente | #404(MERGED) |
| mm-marco-produccion-total | marco-produccion-total | 3d17ad4 | 1414 | 0 | 0 | 1 | OK-compartida | #352(MERGED) |
| mm-marco-satura-codex | acto/marco-satura-codex | 6e0b357 | 1526 | 0 | 0 | 0 | OK-compartida | #323(MERGED) |
| mm-pack-ubuntu2-r83-r14 | acto/pack-ubuntu2-r83-r14 | 96fbae3 | 1403 | 0 | 0 | 0 | OK-compartida | #355(MERGED) |
| mm-propaga-scoring-marco-post330-337 | codex/propaga-scoring-marco-post330-337-v2 | fc7ae47 | 1450 | 0 | 0 | 0 | ausente | #340(MERGED) |
| mm-purga-2 | acto/purga-2 | 4800e00 | 1430 | 0 | 0 | 0 | OK-compartida | #348(MERGED) |
| mm-purga-ejecuta | purga-ejecuta | 7f26983 | 1447 | 0 | 0 | 0 | OK-compartida | #341(MERGED) |
| mm-pypdf-rebarrido-b | pypdf-rebarrido-b | 8800840 | 1520 | 0 | 0 | 0 | symlink-indirecto | #324(MERGED) |
| mm-r34-bc-mecanismo | acto/r34-bc-mecanismo | 9985c4e | 1386 | 0 | 0 | 0 | OK-compartida | #359(MERGED) |
| mm-r34-conda-v2 | r34-conda-v2 | 2c3115c | 1504 | 0 | 0 | 0 | OK-compartida | #328(MERGED) |
| mm-r34-ensafi-censa | r34-ensafi-censa | 5fc1c7f | 1366 | 0 | 0 | 0 | OK-compartida | #365(MERGED) |
| mm-recenso-diseno-14 | recenso-diseno-14 | 455d4aa | 1536 | 0 | 0 | 0 | OK-compartida | #317(MERGED) |
| mm-recenso-diseno-2 | recenso-diseno-2 | 3bae09f | 1528 | 0 | 0 | 0 | OK-compartida | #321(MERGED) |
| mm-reglas-ola5-fase2-a | acto/maestra33-c4-reglas-ola5-fase2-a | 52a460f | 1014 | 0 | 0 | 0 | OK-compartida | #424(MERGED) |
| mm-retriage-4 | retriage-4 | b380ebe | 1562 | 0 | 0 | 0 | OK-compartida | #311(MERGED) |
| mm-scoring-adv1-m3 | codex/scoring-adv1-m3 | 6dddf67 | 1466 | 0 | 0 | 0 | ausente | #330(MERGED) |
| mm-serie-homogenea | serie-homogenea-codi | 654a940 | 1445 | 0 | 0 | 0 | OK-compartida | #342(MERGED) |
| mm-u2-cruce | u2-cruce | 2cd0787 | 1478 | 0 | 0 | 0 | OK-compartida | #335(MERGED) |
| mm-ubuntu-adq1 | ubuntu-adq-1 | 99ef456 | 1649 | 0 | 0 | 0 | OK-compartida | #294(MERGED) |
| mm-worktrees/maestra33-e8-score-m-1 | acto/maestra33-e8-score-m-1 | c23238f | 1011 | 0 | 0 | 0 | OK-compartida | #425(MERGED) |

`data/raw`: 104 symlink directo a la raíz compartida real, 3 symlink
*indirecto* (apuntan a `Modelado-Mexicano/data/raw`, que a su vez es symlink
a la raíz — resuelve bien hoy, pero depende de que ese otro worktree nunca se
borre; fragilidad menor, no ruptura), 15 ausente (0 directorio real
duplicando datos — ningún worktree copió el corpus, buena noticia de
espacio), 0 sin clasificar.

## §2 · Tabla 2 — raíces

**`data/raices.local.yaml`, por clon** (archivo local, no versionado —
por eso se compara por sha256 y no se asume que sea el mismo archivo en los
dos clones; **no se pega ninguna ruta física de este archivo en esta nota**,
solo raíz lógica declarada y si está configurada):

| clon | sha256 de `data/raices.local.yaml` | raíces lógicas declaradas |
|---|---|---|
| `Modelado-Mexicano` | `42f48a2c…4fa503f` | `data_raw` (documentación inerte, ver nota abajo) · `descargas_mx` · `downloads` |
| `mm-adq` | `a89149af…8aaa0814b` | `descargas_mx` únicamente |

**Divergencia real, no solo de hash:** el archivo de `mm-adq` **no declara
`data_raw` ni `downloads`** — dos claves menos que el de `Modelado-Mexicano`.
`data_raw` es documentación inerte en ambos casos de todas formas (el propio
comentario del archivo dice que `tests/manifiesto.py` resuelve la raíz real
por código, vía el symlink `data/raw`, y que `raices_configuradas()` filtra
esa clave explícitamente) — pero la ausencia de `downloads` en `mm-adq` sí es
una divergencia de configuración real entre los dos clones, sin evidencia de
que sea intencional.

**Barrido presentes-no-registrados** (`tools/barrido_descargas_vs_
manifiesto.py`, sha256 contra `data/manifiesto.yaml`, sobre las 3 raíces
reales — rutas físicas usadas para ejecutar el script, no pegadas aquí salvo
la ya pública `data/raices.local.yaml` de arriba):

| raíz | examinados | REGISTRADO | NO-REGISTRADO | MISMO-NOMBRE-OTRO-SHA |
|---|---:|---:|---:|---:|
| corpus compartido (`data_raw` real) | 1233 | 1233 | **0** | 0 |
| `descargas_mx` | 599 | 461 | **138** | 0 |
| `downloads` | 228 | 1 | **227** | 0 |

- **Corpus compartido: limpio.** 0 archivos sin registrar — ninguna señal de
  payload huérfano en la raíz que sí importa.
- **`descargas_mx`, 138 no-registrados — pero 137 de esos 138 son el
  contenido íntegro de un clon git (`ACADEMICO-list-cran/`: código fuente R,
  documentación, `.git/` completo con objetos y hooks) que se descargó
  *para extraer* exactamente 2 archivos de datos (`data/mexico.tab`,
  `man/mexico.Rd`), y esos 2 SÍ están registrados por separado
  (`list_cran_mexico_tab`, `list_cran_mexico_rd`). Candidatos reales de PR
  #77 en esta raíz: **0** — es ruido metodológico de barrer un repo git
  completo, no payloads nuevos. Recomendación: si se elimina el clon
  `ACADEMICO-list-cran/` (dejando solo los 2 archivos ya registrados, o
  moviéndolos fuera), este barrido deja de generar 137 falsos positivos en
  cada corrida futura.
- **`downloads` (carpeta genérica de Windows, NO dedicada al proyecto),
  227 no-registrados de 228 — y aquí sí importa cómo se reporta.** Esta
  carpeta mezcla, sin ninguna separación: (a) varias decenas de documentos de
  planeación/handoff del propio proyecto guardados sueltos (nombres con
  patrón `TRANSFER-*`, `ENCARGO-*`, `TABLERO-*`, `BENCHMARK-*`, `PLAN-*` — no
  son payloads de datos, no necesitan registro), (b) **un hallazgo
  potencialmente accionable:** 4 copias del mismo archivo `ICPSR_35024-
  V1.zip` (~14.7 MB cada una, mismo tamaño) — coincide con el objeto
  `ICPSR 35024` que `FP-314` deja como receta abierta #1 ("ya existe la
  cuenta, falta elegir el paquete correcto de datos"); vale que un acto
  futuro confirme si esta descarga ya es el paquete correcto y cierra esa
  receta, y (c) **una porción sustancial de archivos personales y sin
  relación aparente con el proyecto** — documentos, imágenes, y algunos
  scripts cuyo nombre sugiere manejo de credenciales — que esta nota
  **deliberadamente no lista por nombre**: los scripts de este acto solo
  tocaron nombre/tamaño/sha256 para el cruce contra el manifiesto, nunca
  contenido, y esta nota no reproduce esos nombres para no filtrar
  información ajena al proyecto hacia un repositorio público. Recomendación
  de higiene: `downloads` no tiene NINGUNA entrada en el manifiesto bajo esa
  raíz (ver `--verifica` abajo, 0/0) — nunca ha sido una raíz de staging
  real del proyecto. Vale que mesa decida retirarla de `data/raices.local.yaml`
  en vez de seguir declarándola como raíz del proyecto.

**Verifica registrados-ausentes** (`tests/manifiesto.py --verifica`, todas
las entradas del manifiesto, recalculando sha256 contra la raíz real):

```
data_raw:      coincide=1229 · no_coincide=0 · ausente=0
descargas_mx:  coincide=0    · no_coincide=0 · ausente=334
downloads:     (0 entradas del manifiesto declaran esta raíz)
```

- **`data_raw`: 1229/1229 coincide, 0 ausente.** Corpus íntegro. (La cifra
  1229 vs. las 1233 del barrido no es una discrepancia real: una cuenta
  entradas del manifiesto, la otra archivos físicos — no son la misma
  unidad y no tienen por qué coincidir exacto.)
- **`descargas_mx`: 334 ausente — y el propio script ya lo anota como
  esperado**, línea por línea: *"no está en la raíz 'descargas_mx' (no es un
  error: el payload no se commitea)"*. Es decir: 334 entradas del manifiesto
  registran de dónde vino un payload que ya se promovió al corpus permanente
  — no se espera que el archivo siga viviendo en la carpeta de descargas
  temporal. **No es pérdida de datos, es el diseño previsto del flujo
  descarga→promoción.**

## §3 · Tabla 3 — ramas remotas

**`git ls-remote --heads origin` (tras fetch completo): exactamente 3 ramas
además de `main`.** Ninguna de las 3 tiene worktree local en esta máquina.

| rama | último commit (asunto) | fecha | PR | clasificación |
|---|---|---|---|---|
| `claude/encargo-maestra38-sello-3-6y5e0z` | `PARO: acto MAESTRA38-SELLO-3 ya en curso en otra rama` | 2026-09-07 05:35 UTC | ninguno | **PARO**, confirmado por el propio mensaje del commit — coincide con lo que el encargo esperaba |
| `claude/encola-plan-encargos-repo-mkg5z0` | `[COLA] GEN2-E0 PARCIAL: aterriza plan + indice + 6 encargos; PARA en suite` | 2026-09-07 16:14 UTC | ninguno | **verificado (`git merge-base --is-ancestor`): SU COMMIT YA ES ANCESTRO DE `origin/main`** — se fusionó completo pese al "PARCIAL" del mensaje: `forense/encargos/cola/2026-09-07-GEN2-E1-LIMPIEZA-C1.md` y sus 5 hermanas viven hoy en `origin/main`. "PARCIAL...PARA en suite" describe que la cascada de cierre no llegó a correr la verificación de línea base, no que el contenido quedara sin aterrizar. Es el origen directo de este mismo acto (GEN2-E1). Al estar ya fusionada, es tan redundante como cualquier rama de la Tabla 1 con PR `MERGED` — no se poda aquí porque podar una rama remota es un `push`, fuera del perímetro de este acto, pero queda declarada como candidata igual de segura |
| `claude/tramite-2026-09-07` | `[TRAMITE] digesto 2026-09-07` | 2026-09-07 14:21 UTC | **#598 (OPEN)** | trabajo vivo — trámite de cierre en curso |

**Nota metodológica importante:** clasificar "fusionada en main" solo con
`git branch -r --merged origin/main` sobre las ramas que hoy siguen vivas en
`origin` habría sido casi inútil — GitHub borra la rama remota al fusionar
un PR (comportamiento normal de este repo), así que de los 117 worktrees de
tarea, **solo 3 tienen rama remota viva hoy, y ninguna de esas 3 es un
worktree local**. La clasificación real (Tabla 1) se hizo cruzando cada
rama LOCAL contra el historial COMPLETO de PRs (`gh pr list --state all`,
**598 PRs en total**, números 1–598 sin huecos) — no solo contra los PRs de
ramas que siguen existiendo. Primer intento con `--limit 500` devolvió
exactamente 500 (verificado como truncado: el mínimo de número de PR
devuelto era 99, no 1) — quedó corregido con `--limit 1000` antes de
construir la Tabla 1. Cualquier auditoría futura que use un límite bajo por
default se arriesga al mismo truncamiento silencioso.

## §4 · Hallazgos adicionales (no piden tabla, pero son evidencia real)

**§4.1 — `/home/pc0/.git` no es un repositorio.** El barrido lo encontró
como directorio `.git` real, pero `git status` sobre `$HOME` falla con
`fatal: not a git repository`. Causa: `config`, `config.lock` y `hooks`
dentro de ese `.git` son **dispositivos de caracteres apuntando a
`/dev/null`** (`crw-rw-rw- nobody nogroup 1, 3`), no archivos reales — algo
en este entorno (no identificado por este acto de solo-lectura; podría ser
un artefacto del propio sandbox de la sesión) lo dejó así. No se tocó, no se
investigó más allá de leer sus metadatos — está fuera del perímetro de un
acto de solo lectura sin autoridad para decidir si es seguro tocarlo.

**§4.2 — El propio `git worktree add` de este acto chocó con el mismo tipo
de anomalía.** Al crear `mm-gen2-e1-limpieza-c1`, git reportó dos veces
`error: could not write config file .git/config: Device or resource busy`
sobre `Modelado-Mexicano/.git/config` (el archivo real, no un stub — se
verificó que el archivo sigue íntegro). El worktree quedó registrado
correctamente, pero el tracking de rama (`branch.acto/gen2-e1-limpieza-c1.
remote`) **nunca se escribió** — confirmado con `git config --get`, vacío.
No bloquea este acto (no se iba a empujar de todas formas), pero es
evidencia de que esta máquina puede fallar silenciosamente al escribir
`.git/config` bajo concurrencia — cualquier otro worktree creado en
condiciones similares podría tener el mismo tracking ausente sin que nadie
lo haya notado.

**§4.3 — Restos sueltos que no son árboles git, en `$HOME`:**

| ruta | qué es | tamaño | fecha |
|---|---|---:|---|
| `mm-corre-r10-1-SELLO` | 2 archivos sueltos (`.md`+`.tsv`), sello manual, no es repo | 8.6 KB | 25/ago |
| `respaldo-worktrees/` | 4 git bundles + 1 `.tar.gz` + 1 script — respaldo de una limpieza anterior (uno se llama literalmente `limpia-caja-todas-las-ramas-20260818.bundle`) | ~64 MB | 18/ago |
| `BACKUP-mm-mirror-2026-08-10.tar.gz` | respaldo suelto en la raíz de `$HOME` | 12.8 MB | 10/ago |
| `barrido-completo-snapshot-staging-2026-08-10.tar.gz` | snapshot suelto en la raíz de `$HOME` | 431 KB | 10/ago |
| `untracked_barrido.txt` | reporte de texto de un barrido viejo, suelto en la raíz de `$HOME` | 111 KB | 10/ago |

Ninguno es un árbol git — no entran en la poda de worktrees, pero si mesa
quiere limpiar disco además de árboles, aquí está el inventario con
evidencia. `mm-corpus/` (la raíz compartida real) y `L-run/` **no son
hallazgos** — son, respectivamente, la raíz de datos legítima y una carpeta
de resultados de corridas sin relación con este inventario de árboles.

**§4.4 — Dos repos ajenos al proyecto, encontrados por el `find` literal del
encargo:** `~/.codex/.tmp/plugins/.git` y `~/.codex-app/.tmp/plugins/.git`
— internos de otra herramienta (Codex CLI), no de Modelado-Mexicano. No se
exploraron más allá de confirmar que existen, por respeto al perímetro que
la propia mesa pidió no cruzar ("no me gustaría que se jalara info o data de
otros trabajos en la máquina local").

**§4.5 — `Modelado-Mexicano/.git/config` acumula docenas de secciones
`[branch "x"]` de ramas que ya no existen** (historial de todo el proyecto,
nunca podado). No rompe nada, es basura inofensiva.

## §5 · Lista propuesta de poda (para firma de mesa, paso siguiente)

**114 worktrees de tarea, cada uno con PR ya `MERGED` en `main` (113) o sin
ninguna divergencia propia y sin PR (1) — cero riesgo de perder trabajo si
se ejecuta `git worktree remove` sobre cada ruta:**

| ruta (bajo $HOME) | rama | evidencia (PR / estado) |
|---|---|---|
| mm-autoridad-semantica-enif | codex/autoridad-semantica-enif | sin PR, 0 commits propios (nunca divergió) |
| Modelado-Mexicano-barrido2 | cond-atrib | #263 MERGED |
| Modelado-Mexicano-cruce-oferta-demanda | codex/cruce-oferta-demanda | #363 MERGED |
| Modelado-Mexicano-maestra31-e4-orden-superior | maestra31-e4-orden-superior | #385 MERGED |
| Modelado-Mexicano/.claude/worktrees/agent-a45c7ec89ca02c496 | acto/maestra38-a5-pdn-bulk-y-proxy | #553 MERGED |
| Modelado-Mexicano/.claude/worktrees/agent-a4f8a030e1f577254 | acto/maestra38-a4-adquiere-todo-lo-publico | #552 MERGED |
| mm-a4-registra-descargas | acto/maestra33-a4-registra-descargas-manuales | #440 MERGED |
| mm-act-pil-2 | act-pil-2 | #297 MERGED |
| mm-adq-corre-r74r75 | adq-corre-r74r75 | #326 MERGED |
| mm-adq-diseno-1 | adq-diseno-1 | #320 MERGED |
| mm-adq-enoe-pre2019 | adq-enoe-pre2019 | #310 MERGED |
| mm-agente-adquisicion-1 | acto/maestra33-a1-agente-adquisicion-1 | #414 MERGED |
| mm-apertura-enfih-ensafi | apertura-enfih-ensafi | #302 MERGED |
| mm-apertura-verifica | acto/maestra33-c7-apertura-verifica | #431 MERGED |
| mm-arbitra-r-lote-2 | acto/maestra33-c5-arbitra-r-lote-2 | #426 MERGED |
| mm-arbitra-r-lote-3 | acto/maestra33-c6-arbitra-r-lote-3 | #436 MERGED |
| mm-arbitro-r-1 | acto/maestra33-c2-arbitro-r-1 | #417 MERGED |
| mm-autoridad-semantica-marco | codex/autoridad-semantica-marco-enif | #343 MERGED |
| mm-autoridad-semantica-marco-produccion | codex/autoridad-semantica-marco-cobertura-total | #349 MERGED |
| mm-bibliotecario-56 | bibliotecario-56 | #333 MERGED |
| mm-c1-respec-corresidencia | acto/maestra33-c1-respec-corresidencia | #412 MERGED |
| mm-c8-medidor-fp172 | acto/maestra33-c8-medidor-fp172-diferidas | #434 MERGED |
| mm-codifica-r-1 | acto/maestra33-c3-codifica-r-1 | #423 MERGED |
| mm-coef-universo | coef-universo | #287 MERGED |
| mm-cola-enmienda3 | cola/enmienda-3-n3 | #496 MERGED |
| mm-corre-r10-1 | acto/corre-r10-1-v2-faseb | #376 MERGED |
| mm-e1-reloj-cruce | acto/e1-reloj-cruce | #382 MERGED |
| mm-e16-medidor-familismo | acto/maestra32-e16-medidor-familismo | #406 MERGED |
| mm-e18-p3-ola6 | acto/maestra33-e18-p3-reglas-ola6-activos-l1 | #447 MERGED |
| mm-e3-ejerce-compartamos | acto/e3-ejerce-llave-compartamos | #374 MERGED |
| mm-e4-diseno-ensafi | acto/e4-diseno-ensafi | #373 MERGED |
| mm-e6-l-run | acto/e6-l-run | #377 MERGED |
| mm-e7-r-scoring | acto/e7-r-scoring | #378 MERGED |
| mm-e9-scoring-v2 | acto/e9-scoring-v2 | #381 MERGED |
| mm-ensafi-descriptor | acto/ensafi-descriptor | #370 MERGED |
| mm-eval-compartamos | eval-compartamos | #331 MERGED |
| mm-extractor-dta | acto/maestra32-e3-extractor-dta | #400 MERGED |
| mm-extractor-fd | acto/maestra32-e12-extractor-fd | #401 MERGED |
| mm-ficha-r51-d3 | ficha-r51-d3 | #290 MERGED |
| mm-fp63-cierra | fp63-cierra | #291 MERGED |
| mm-gemelas-20 | gemelas-20 | #344 MERGED |
| mm-generador-marco | codex/generador-marco | #332 MERGED |
| mm-generador-marco-corpus-real | codex/generador-marco-corpus-real | #337 MERGED |
| mm-indice-no-inegi | indice-no-inegi | #345 MERGED |
| mm-l-corridas-v1-1 | acto/l-corridas-v1_1 | #442 MERGED |
| mm-l1-mordida-serie | acto/maestra34-l1-mordida-serie | #451 MERGED |
| mm-l11-robustece-l9 | acto/maestra35-l11-robustece-l9 | #494 MERGED |
| mm-l14-coercitivo | acto/maestra36-l14-coercitivo-tres-universos | #508 MERGED |
| mm-l16-bis-2 | acto/maestra38-l16-bis-2 | #590 MERGED |
| mm-l16-bis-paro | acto/maestra38-l16-bis | #581 MERGED |
| mm-l2-arbitra-v1_2 | acto/maestra34-l2-arbitra-v1_2 | #452 MERGED |
| mm-l2-lista | acto/maestra38-l2-lista | #554 MERGED |
| mm-l3-corpus-sano | acto/maestra34-l3-corpus-sano-y-cngmd | #458 MERGED |
| mm-l3-salud | maestra37-l3-salud-a4 | #516 MERGED |
| mm-l3bis | acto/maestra37-l3bis-salud-a4-v2 | #520 MERGED |
| mm-l4-civica-corpus | acto/maestra34-l4-civica-y-corpus | #464 MERGED |
| mm-l5-gobierno-digital | acto/maestra34-l5-gobierno-digital-evasion-ahorro | #467 MERGED |
| mm-l6-fuente-coercitivo | acto/maestra35-l6-fuente-coercitivo-y-puente | #480 MERGED |
| mm-l6-homologacion | acto/maestra34-l6-civica-homologacion-escalonada | #468 MERGED |
| mm-l9-activos-l3 | claude/encargo-acto-maestra35-l9 | #491 MERGED |
| mm-limpia-caja | limpia-caja | #278 MERGED |
| mm-llave2-decreto | llave2-decreto | #336 MERGED |
| mm-lote-cruce | acto/maestra38-lote-cruce | #578 MERGED |
| mm-lote-lapop | acto/maestra38-lote-lapop | #551 MERGED |
| mm-lote-retriage | lote-retriage | #298 MERGED |
| mm-maestra31-e3-perimetro-alcanzable | acto/maestra31-e3-perimetro-alcanzable | #384 MERGED |
| mm-maestra31-e6-diccionarios-fd | acto/maestra31-e6-diccionarios-fd | #387 MERGED |
| mm-maestra31-e8-los-388 | acto/maestra31-e8-los-388 | #389 MERGED |
| mm-maestra31-e9-estima-rutac | acto/maestra31-e9-estima-rutac | #390 MERGED |
| mm-maestra33-a3-adquiere2 | acto/maestra33-a3-adquiere-2-rutas-multiples | #433 MERGED |
| mm-maestra34-a1-registra-2 | acto/maestra34-a1-registra-evalua-descargas-2 | #453 MERGED |
| mm-maestra35-a1 | acto/maestra35-a1-relanza | #483 MERGED |
| mm-maestra35-l1 | acto/maestra35-l1-recorre-y-segmenta | #471 MERGED |
| mm-maestra35-l2 | acto/maestra35-l2-r-v1_2-completa | #470 MERGED |
| mm-maestra35-l3 | acto/maestra35-l3-civica-tipo-de-boleta | #476 MERGED |
| mm-maestra35-l4 | acto/maestra35-l4-r-v1_2-ciega | #490 MERGED |
| mm-maestra35-l5 | claude/l5-espejo-estado-programa | #482 MERGED |
| mm-maestra35-l7 | acto/maestra35-l7-reglas-activos-l2 | #486 MERGED |
| mm-maestra35-l8 | acto/maestra35-l8-civica-8-entidades | #487 MERGED |
| mm-maestra36-a1 | acto/maestra36-a1-escanea-recursivo | #500 MERGED |
| mm-maestra36-l12 | acto/maestra36-l12-mps2012-crosstabs | #506 MERGED |
| mm-maestra36-l13 | acto/maestra36-l13-coercitivo-sat-efirma | #502 MERGED |
| mm-maestra37-a1 | acto/maestra37-a1-registra-ensanut-v2 | #518 MERGED |
| mm-maestra37-a2-revisa-cola | acto/maestra37-a2-revisa-cola-a-detalle | #526 MERGED |
| mm-maestra37-infra1 | claude/maestra37-infra-1-ssot-manifiesto-alta | #521 MERGED |
| mm-maestra37-infra2 | claude/maestra37-infra-2-capa2-portabilidad | #522 MERGED |
| mm-maestra37-infra2-frented | claude/maestra37-infra-2-frente-d | #525 MERGED |
| mm-maestra37-l1-indexa | acto/maestra37-l1-indexa-descargas-mx-y-remapea-salud | #514 MERGED |
| mm-maestra38-a1 | acto/maestra38-a1-sonda-y-descarga-universo-1 | #524 MERGED |
| mm-maestra38-a2 | acto/maestra38-a2-recenso-y-regulariza-perimetro-real | #543 MERGED |
| mm-maestra38-a2-bis | acto/maestra38-a2-bis | #549 MERGED |
| mm-maestra38-a6 | acto/maestra38-a6-resondeo-negativos | #561 MERGED |
| mm-maestra38-l2 | maestra38-l2-mps2012 | #564 MERGED |
| mm-maestra38-lote-ensanut | acto/maestra38-lote-ensanut | #565 MERGED |
| mm-marco-m-sortea | acto/maestra32-e14-marco-m-sortea | #404 MERGED |
| mm-marco-produccion-total | marco-produccion-total | #352 MERGED |
| mm-marco-satura-codex | acto/marco-satura-codex | #323 MERGED |
| mm-pack-ubuntu2-r83-r14 | acto/pack-ubuntu2-r83-r14 | #355 MERGED |
| mm-propaga-scoring-marco-post330-337 | codex/propaga-scoring-marco-post330-337-v2 | #340 MERGED |
| mm-purga-2 | acto/purga-2 | #348 MERGED |
| mm-purga-ejecuta | purga-ejecuta | #341 MERGED |
| mm-pypdf-rebarrido-b | pypdf-rebarrido-b | #324 MERGED |
| mm-r34-bc-mecanismo | acto/r34-bc-mecanismo | #359 MERGED |
| mm-r34-conda-v2 | r34-conda-v2 | #328 MERGED |
| mm-r34-ensafi-censa | r34-ensafi-censa | #365 MERGED |
| mm-recenso-diseno-14 | recenso-diseno-14 | #317 MERGED |
| mm-recenso-diseno-2 | recenso-diseno-2 | #321 MERGED |
| mm-reglas-ola5-fase2-a | acto/maestra33-c4-reglas-ola5-fase2-a | #424 MERGED |
| mm-retriage-4 | retriage-4 | #311 MERGED |
| mm-scoring-adv1-m3 | codex/scoring-adv1-m3 | #330 MERGED |
| mm-serie-homogenea | serie-homogenea-codi | #342 MERGED |
| mm-u2-cruce | u2-cruce | #335 MERGED |
| mm-ubuntu-adq1 | ubuntu-adq-1 | #294 MERGED |
| mm-worktrees/maestra33-e8-score-m-1 | acto/maestra33-e8-score-m-1 | #425 MERGED |

**Explícitamente EXCLUIDOS de esta lista de poda** (no tocar sin decisión
propia):

- `Modelado-Mexicano`, `mm-adq` — son los clones base, no árboles de tarea.
- `mm-gen2-e1-limpieza-c1` — es la caja de este mismo acto, en uso ahora mismo.
- **`mm-maestra37-l2-mps-codebook` y `mm-maestra38-v1`** — ver §6, fila ABIERTA.

## §6 · Contador nuevo: `arboles_fuera_de_politica`

**Definición (nace en este acto):** número de worktrees de tarea
(`worktree-per-task`) cuya retención ya no sirve ningún propósito bajo la
política del proyecto — porque su PR ya se fusionó en `main`, o porque nunca
tuvieron ningún commit propio y tampoco PR — y que por tanto son candidatos
directos a `git worktree remove` sin riesgo de pérdida. Excluye por
definición: los clones base, la caja del acto que mide el contador, y
cualquier worktree con commits propios no empujados y sin PR (ese caso es
una decisión de mesa, no un candidato automático).

**Primer valor medido: `arboles_fuera_de_politica = 114`** (de 117
worktrees de tarea existentes hoy, 2026-09-07).

## Fila ABIERTA — requiere decisión de mesa

Esta nota cierra como RECIBO en su mayor parte, pero **dos hallazgos exigen
decisión antes de tocar nada**, tal como el propio encargo anticipó
("fila ABIERTA solo si aparece... un commit no empujado"):

1. **`mm-maestra37-l2-mps-codebook`** (rama `acto/maestra37-l2-mps-codebook-
   y-p3`): 2 commits, **ninguno empujado a ningún remoto**. El segundo
   (`05e6bef`, 2026-09-03) es un **COMMIT-1 del patrón de dos commits**: una
   spec congelada completa (`forense/notas/2026-09-03-MAESTRA37-L2-spec.md`,
   182 líneas) escrita "antes de abrir el cuestionario" — exactamente el
   tipo de artefacto que, por diseño del patrón de dos commits, no se
   vuelve a redactar. Si este worktree se borra sin rescatar el commit, esa
   spec pre-registrada se pierde. Búsqueda de PR por título (`L2-MPS-
   CODEBOOK`) confirma: nunca se abrió PR.
2. **`mm-maestra38-v1`** (rama `acto/maestra38-v1-corrobora-y-reconcilia`):
   1 commit, no empujado — solo el archivo 0-bis A.3 (encargo archivado
   verbatim), ningún trabajo sustantivo todavía. Menor riesgo que el
   anterior, pero también sin PR y sin rescatar.

Mesa decide, para cada uno: empujar la rama a un ref huérfano (`git push
origin <sha>:refs/heads/<nombre>-huerfana`, sin abrir PR, para preservarlo
sin re-arrancar el acto) y luego podar el worktree, o descartarlo
explícitamente. Ninguna de las dos rutas la toma este acto por su cuenta.

Además, quedan dos recomendaciones de higiene sin urgencia (no bloquean
nada, no gatean ningún acto en vuelo): retirar `downloads` de
`data/raices.local.yaml` como raíz del proyecto (§2), y devolver el clon base
`Modelado-Mexicano` a `main` (§1).
