# P3 · Censo de fichaje de la semana códex (`cc1cfe2c..HEAD`)

ACTO GEN2-CONCILIACION-TANDA-2, 14/sep/2026. Universo declarado (A.13):
`git log --merges cc1cfe2c..HEAD` sobre `origin/main` desomerado (el clon
nació superficial en 472 commits / boundary en PR #682; `git fetch
--unshallow` lo llevó a 3992 commits, con lo que `cc1cfe2c` — `PR #668`,
fusionado 2026-09-09 — quedó alcanzable). `cc1cfe2c..38d25ad2` cubre
`PR #669` a `PR #747` (2026-09-09 a 2026-09-12/14), la semana códex que el
encargo pedía censar.

## Mecánica

```
git log --oneline --merges cc1cfe2c..HEAD | wc -l                    -> 194  (coincide con el número declarado por dirección)
git log --merges cc1cfe2c..HEAD --format="%H %s" | grep -c "Merge pull request #"        -> 78  (merges reales de PR contra main)
... | grep -vc "Merge pull request #"                                -> 116 (merge-intermedio: "Merge remote-tracking branch 'origin/main' into <rama-de-trabajo>" -- sincronías dentro de una rama de acto, nunca tocan main como destino; EXENTAS por definición del propio encargo)
```

`PR #740` (`[ADQ] 2026-09-11`) está fusionado (confirmado con
`pull_request_read`) pero su **base no era `main`** — era
`acto/gen2-descubrimiento-adquisicion-suficiencia` (PR #739) — así que nunca
aparece como "Merge pull request #740" en el primer padre de `main`; su
contenido entró a `main` cuando #739 se fusionó (`git merge-base
--is-ancestor <head-de-740> origin/main` → sí). Mismo tratamiento que un
merge-intermedio: **EXENTO**, y su fichaje viaja con el de #739 (que, por su
cuenta, es una de las EXCEPCIONES de abajo).

Para cada uno de los 78 PR reales se buscó su ficha con:
```
grep -rn "## CONSUMIDO" forense/encargos/**/*.md   # 463 de 534 encargos archivados la traen
# y dentro de esa sección, una cita "#<PR>" en cualquier punto del texto
```
`censo/*` y `claude/tramite-*` son exentos por nombre, per el propio texto
del encargo ("censo/trámite/merge-intermedio exento"). Dos categorías **no**
nombradas por el encargo se separan para que mesa decida si merecen su
propio cuarto exento:

- **EXCEPCIÓN-COLA/ADQ**: PR cuyo título es `[COLA] ...` o `[ADQ] ...` — el
  mecanismo que **entrega** encargos a `forense/encargos/(cola/)` o a
  `data/cola-adquisicion-*`, no un acto que los ejecute. Por construcción no
  tiene "obligación propia" que fichar más allá de "los archivos llegaron",
  que el propio commit ya demuestra. 10 casos.
- **EXCEPCIÓN-ACTO**: un acto GEN2 real, fusionado, sin `## CONSUMIDO`
  citando su PR en ningún encargo archivado — la fuga genuina que P3 buscaba.
  8 casos, verificados a mano uno por uno (no solo por el grep): en 5 no
  existe archivo alguno en `forense/encargos/` que mencione la rama; en 1
  (`#680`) el encargo SÍ tiene `## CONSUMIDO` pero cita el acto por nombre
  sin el dígito del PR; en 1 (`#701`) el encargo hermano existe y tiene
  `## CONSUMIDO`, pero cita el PR base (`#696`) y no la adenda (`#701`) que
  lo siguió.

## Tabla completa (78 PR)

| PR | rama | clasificación | ficha principal |
|---|---|---|---|
| #669 | `acto/gen2-f5-recaptura-l` | FICHADO | 2026-09-09-GEN2-F5-RECAPTURA-L.md (+3 más citan el mismo PR) |
| #670 | `claude/wizardly-ptolemy-pnsvsz` | FICHADO | 2026-09-09-GEN2-F5-RECAPTURA-L.md (+2 más citan el mismo PR) |
| #671 | `claude/eloquent-darwin-lpgi7d` | FICHADO | 2026-09-09-GEN2-F5-RECAPTURA-L.md (+1 más citan el mismo PR) |
| #672 | `claude/cool-lovelace-h9q74y` | FICHADO | 2026-09-10-GEN2-DERIVADORES-FIX.md (+1 más citan el mismo PR) |
| #673 | `acto/gen2-lote-encuci-1` | FICHADO | 2026-09-09-GEN2-LOTE-ENCUCI-1.md (+1 más citan el mismo PR) |
| #674 | `acto/gen2-f5-duelo-calc` | FICHADO | 2026-09-10-GEN2-F5-DUELO-CALC.md (+3 más citan el mismo PR) |
| #675 | `claude/determined-faraday-io36oz` | FICHADO | 2026-09-10-GEN2-F5-CONTRATO-TRIADA.md |
| #676 | `acto/gen2-f5-extractor-l` | FICHADO | 2026-09-10-GEN2-F5-EXTRACTOR-L.md (+1 más citan el mismo PR) |
| #677 | `claude/acto-gen2-m-snapshot-ys3vn7` | FICHADO | 2026-09-10-GEN2-M-SNAPSHOT-TRIADA.md |
| #678 | `claude/tramite-2026-09-10` | EXENTO | — |
| #679 | `censo/2026-09-10` | EXENTO | — |
| #680 | `acto/gen2-r-completa-marco` | **EXCEPCIÓN-ACTO** | ninguna |
| #681 | `claude/calc-triada-gen2-adjudicacion-s40h3r` | FICHADO | 2026-09-10-GEN2-F5-TRIADA-CALC.md (+1 más citan el mismo PR) |
| #682 | `acto/gen2-corrida0-replay-cascada` | **EXCEPCIÓN-ACTO** | ninguna |
| #683 | `acto/gen2-corrida0-cascada-post-682` | FICHADO | 2026-09-10-GEN2-F5-L-ESTIMANDO-V1-4.md |
| #684 | `acto/gen2-f5-l-estimando-v1-4` | FICHADO | 2026-09-10-GEN2-F5-L-ESTIMANDO-V1-4.md (+1 más citan el mismo PR) |
| #685 | `acto/mesa-conciliacion-e01` | FICHADO | 2026-09-10-MESA-CONCILIACION-E01.md (+1 más citan el mismo PR) |
| #686 | `claude/new-session-pk9z2m` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #687 | `acto/gen2-f5-completa` | FICHADO | 2026-09-10-GEN2-F5-COMPLETA.md (+2 más citan el mismo PR) |
| #688 | `acto/gen2-sociales-sucesoras` | FICHADO | 2026-09-10-GEN2-S6-S12-S13-SUCESORAS.md (+3 más citan el mismo PR) |
| #689 | `acto/gen2-motor-usos` | FICHADO | 2026-09-10-GEN2-MOTOR-USOS-Y-COMPLEMENTOS.md (+2 más citan el mismo PR) |
| #690 | `acto/gen2-pruebas-replay` | FICHADO | 2026-09-10-GEN2-PRUEBAS-LIMPIAS-Y-REPLAY.md (+3 más citan el mismo PR) |
| #691 | `acto/gen2-enif-poblacion` | FICHADO | 2026-09-10-GEN2-ENIF-POBLACION-Y-ADOPCION.md (+2 más citan el mismo PR) |
| #692 | `acto/gen2-envipe-serie` | FICHADO | cola/2026-09-10-GEN2-POST-685/05-GEN2-ENVIPE-SERIE-COMPLETA.md (+2 más citan el mismo PR) |
| #693 | `acto/gen2-adquisicion-dirigida` | FICHADO | cola/2026-09-10-GEN2-POST-685/06-GEN2-ADQUISICION-DIRIGIDA-Y-DIN.md |
| #694 | `acto/gen2-encola-post693` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #695 | `acto/gen2-corrupcion-unidad-fuente` | FICHADO | 2026-09-10-GEN2-CORRUPCION-UNIDAD-Y-FUENTE-GENERAL.md (+2 más citan el mismo PR) |
| #696 | `acto/gen2-publicacion-post693` | FICHADO | 2026-09-10-GEN2-PUBLICACION-POST693-Y-CIERRES.md (+1 más citan el mismo PR) |
| #697 | `acto/gen2-envipe-validacion-lectura` | FICHADO | 2026-09-10-GEN2-ENVIPE-VALIDACION-Y-LECTURA.md |
| #698 | `acto/gen2-f5-aprendizajes-sucesor` | FICHADO | 2026-09-10-GEN2-F5-APRENDIZAJES-Y-SUCESOR.md |
| #699 | `acto/gen2-encola-post694` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #700 | `acto/gen2-tandas-medicion-academica` | FICHADO | 2026-09-10-GEN2-TANDAS-MEDICION-ACADEMICA.md |
| #701 | `acto/gen2-publicacion-post693` | **EXCEPCIÓN-ACTO** | ninguna |
| #702 | `acto/gen2-s6-diseno-alcance` | FICHADO | cola/2026-09-11-GEN2-POST-694/16-GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL.md |
| #703 | `acto/gen2-encola-post701` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #704 | `acto/gen2-sonda-cron-produccion` | FICHADO | 2026-09-10-GEN2-SONDA-CRON-PRODUCCION-POST693.md |
| #705 | `acto/gen2-ya-medido-tasas` | FICHADO | cola/2026-09-11-GEN2-POST-694/14-GEN2-YA-MEDIDO-SIN-FALSOS-NEGATIVOS.md |
| #706 | `acto/gen2-enif-fintech-serie` | FICHADO | 2026-09-10-GEN2-ENIF-FINTECH-SERIE-DESCRIPTIVA.md (+2 más citan el mismo PR) |
| #707 | `censo/2026-09-11` | EXENTO | — |
| #708 | `carga/benchmark-web-cuatro-decisiones-gen2-2026-09-11` | FICHADO | 2026-09-11-GEN2-MOTOR-Y-HERENCIA-EXPLICITA.md |
| #709 | `acto/gen2-encola-post707` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #710 | `acto/gen2-linaje-adopcion` | FICHADO | 2026-09-11-GEN2-LINAJE-Y-ADOPCION.md (+2 más citan el mismo PR) |
| #711 | `acto/gen2-produccion-fallo-post707` | FICHADO | 2026-09-11-GEN2-PRODUCCION-Y-FALLO-POST707.md |
| #712 | `acto/gen2-motor-herencia-explicita` | FICHADO | 2026-09-11-GEN2-MOTOR-Y-HERENCIA-EXPLICITA.md (+1 más citan el mismo PR) |
| #713 | `acto/gen2-evaluacion-sin-fugas` | FICHADO | 2026-09-11-GEN2-EVALUACION-SIN-FUGAS.md |
| #714 | `acto/gen2-validacion-r-envipe-22` | FICHADO | 2026-09-11-GEN2-VALIDACION-R-ENVIPE-CSV.md (+1 más citan el mismo PR) |
| #715 | `acto/gen2-expedientes-acceso-21` | FICHADO | 2026-09-11-GEN2-EXPEDIENTES-ACCESO-LISTOS.md |
| #716 | `censo/2026-09-11` | EXENTO | — |
| #717 | `acto/gen2-fuentes-financieras-20` | FICHADO | 2026-09-11-GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES.md |
| #718 | `acto/gen2-adq-codex-produccion` | FICHADO | 2026-09-11-GEN2-ADQ-CODEX-PRODUCCION.md |
| #719 | `acto/gen2-adquisicion-cierre-verificable` | **EXCEPCIÓN-ACTO** | ninguna |
| #720 | `acto/gen2-contrato-seleccion-emision` | FICHADO | 2026-09-11-GEN2-CONTRATO-DE-SELECCION-Y-EMISION.md (+1 más citan el mismo PR) |
| #721 | `censo/2026-09-11` | EXENTO | — |
| #722 | `acto/gen2-f5-panel-viable-y-presupuesto` | FICHADO | 2026-09-11-GEN2-F5-PANEL-VIABLE-Y-PRESUPUESTO.md (+1 más citan el mismo PR) |
| #723 | `acto/gen2-fuentes-financieras-continuacion-efectiva` | FICHADO | 2026-09-11-GEN2-FUENTES-FINANCIERAS-CONTINUACION-EFECTIVA.md (+2 más citan el mismo PR) |
| #724 | `acto/gen2-encola-post723` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #725 | `acto/gen2-imor-contexto-temporal-por-regimen` | FICHADO | 2026-09-11-GEN2-IMOR-CONTEXTO-TEMPORAL-POR-REGIMEN.md |
| #726 | `acto/gen2-cron-demanda-dato-produccion` | **EXCEPCIÓN-ACTO** | ninguna |
| #727 | `censo/2026-09-11` | EXENTO | — |
| #728 | `acto/gen2-f5-documental-ejecucion` | **EXCEPCIÓN-ACTO** | ninguna |
| #729 | `acto/gen2-consulta-operativa-contrato` | FICHADO | cola/2026-09-12-GEN2-POST-726/37-GEN2-DELTA-COMPARACION-EXPLICITA.md |
| #730 | `acto/gen2-ensafi-medicion-descriptiva-con-diseno` | FICHADO | 2026-09-11-GEN2-ENSAFI-MEDICION-DESCRIPTIVA-CON-DISENO.md (+1 más citan el mismo PR) |
| #731 | `acto/gen2-validacion-independiente-parametros-activos` | FICHADO | cola/2026-09-12-GEN2-POST-726/37-GEN2-DELTA-COMPARACION-EXPLICITA.md |
| #732 | `acto/gen2-encola-post726` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #733 | `acto/gen2-delta-comparacion-explicita` | FICHADO | cola/2026-09-12-GEN2-POST-726/37-GEN2-DELTA-COMPARACION-EXPLICITA.md |
| #734 | `acto/gen2-n34-datos-producto-y-dano` | FICHADO | cola/2026-09-12-GEN2-POST-726/36-GEN2-N34-DATOS-PRODUCTO-Y-DANO.md |
| #735 | `acto/gen2-tandas-panel-entradas-salidas` | FICHADO | cola/2026-09-12-GEN2-POST-726/35-GEN2-TANDAS-PANEL-ENTRADAS-Y-SALIDAS.md |
| #736 | `acto/gen2-corpus-compartido-utilizable` | FICHADO | cola/2026-09-12-GEN2-POST-726/33-GEN2-CORPUS-COMPARTIDO-UTILIZABLE.md (+1 más citan el mismo PR) |
| #737 | `acto/gen2-reactivos-contexto-busqueda` | **EXCEPCIÓN-ACTO** | ninguna |
| #738 | `adq/2026-09-11-gen2-38-investigacion-codex` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #739 | `acto/gen2-descubrimiento-adquisicion-suficiencia` | **EXCEPCIÓN-ACTO** | ninguna |
| #741 | `acto/gen2-encola-post739` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #742 | `acto/gen2-reactivos-residuales-busqueda-util` | FICHADO | 2026-09-12-GEN2-REACTIVOS-PENDIENTES-Y-BUSQUEDA-UTIL.md |
| #743 | `acto/gen2-encola-post741` | EXCEPCIÓN-COLA/ADQ | ninguna |
| #744 | `acto/gen2-demanda-contratos-ejecucion-nc0165` | FICHADO | 2026-09-12-GEN2-DEMANDA-CONCILIADA-Y-EJECUCION-NC0165.md (+1 más citan el mismo PR) |
| #745 | `acto/gen2-shed-bnpl-dano-universos` | FICHADO | 2026-09-11-GEN2-SHED-BNPL-DANO-UNIVERSOS.md |
| #746 | `acto/gen2-banxico-producto-atraso-costo` | FICHADO | 2026-09-12-GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO.md |
| #747 | `acto/gen2-n35-preferencias-laborales-fuentes` | FICHADO | 2026-09-11-GEN2-N35-PREFERENCIAS-LABORALES-Y-FUENTES.md |

## Resultado

| categoría | filas | qué significa |
|---|---|---|
| Merges totales `cc1cfe2c..HEAD` | 194 | universo declarado por dirección, verificado bit a bit |
| — merge-intermedio (`Merge remote-tracking branch 'origin/main' into <rama>`) | 116 | exentos por definición del encargo — nunca tienen main como destino |
| — merges de PR reales contra `main` | 78 | `#669`–`#747`; `#740` viaja con `#739` (base ≠ main) |
| **FICHADOS** (`## CONSUMIDO` cita el PR, en su encargo o el de un acto hermano) | **54** | ok |
| **EXENTOS** (`censo/*`, `claude/tramite-*`) | **6** | por texto explícito del encargo |
| **EXCEPCIÓN-COLA/ADQ** (PR `[COLA]`/`[ADQ]`, mecanismo de entrega, sin obligación propia que fichar) | **10** | no nombrada por las tres categorías del encargo — propuesta a mesa abajo |
| **EXCEPCIÓN-ACTO** (acto GEN2 real, fusionado, sin `## CONSUMIDO` citando su PR) | **8** | la fuga genuina — total |
| **Total EXCEPCIONES** | **18** | 78 − 54 − 6 = 18 |

## EXCEPCIONES — detalle y precedente de retro-sello

Ninguna se retro-sella en este acto (fuera de perímetro: este acto no toca
código ni firma; solo censa). El precedente vigente es `NC-0054`/`NC-0058`
— los dos retro-sellos de `PR #632`/`PR #635` (`ACTO GEN2-SONDA-2`/
`GEN2-SONDA-CAJA-1`) — que **fallaron**: el texto original vivía solo en una
conversación externa (ChatGPT) y nunca se recuperó, así que ambos quedaron
`SIN-ASIGNAR` en vez de cerrarse. Estas 18 son un caso más favorable: el
código/los resultados de cada PR SÍ están en el árbol (son PR reales,
fusionados, con diff completo en GitHub) — lo que falta no es el texto del
encargo sino la sección `## CONSUMIDO` que lo cite. Mesa puede:

1. **Las 8 EXCEPCIÓN-ACTO** (`#680`, `#682`, `#701`, `#719`, `#726`, `#728`,
   `#737`, `#739`): decidir si se retro-sellan con una sola pasada que
   añada `## CONSUMIDO (PR #NNN)` a cada encargo archivado ya existente
   (`#680`: solo falta el dígito; los otros 7 necesitan que alguien lea el
   PR real en GitHub y redacte la sección) — o si, por su antigüedad y bajo
   riesgo (todas anteriores al 13/sep), se declaran huérfanas aceptadas y se
   anota la excepción sin más trabajo.
2. **Las 10 EXCEPCIÓN-COLA/ADQ**: decidir si `[COLA]`/`[ADQ]` se suman como
   cuarta categoría exenta junto a censo/trámite/merge-intermedio (lo que
   bajaría las EXCEPCIONES reales a 8), o si mesa prefiere que cada uno
   también lleve su propia línea de cierre.

Este censo **no encontró cero excepciones** — 18 de 78, ~23%. Es, en sí
mismo, el hallazgo que P3 pedía poder entregar incluso si no era cero.
