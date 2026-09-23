# GEN2-FRONT-1 · cierre técnico

Worktree `/home/pc0/mm-gen2-front-1`, rama `acto/gen2-front-1`; base al abrir `8e41f72f`, encargo redactado sobre `7722b9c1`. CONTADOR: cero mediciones y ninguna adopción. Firma de entorno: `tools/entorno.py --arranque` produjo `INDETERMINADO`, corpus NO (0 archivos), sonda sin red; no produjo CAJA ni se abrió microdato.

## Piezas

P1 README GEN2 con cifras de `status` y seis casos enlazados; P2 aviso, uso aceptable y CFF; P4 `docs/` para Pages. P3 queda con excepción por referencias selladas: no se hicieron movimientos de archivos de la raíz. Los límites de `USO-ACEPTABLE.md` se preservaron byte por byte. LICENSE queda intacta: MIT para código, CC BY-NC-SA para corpus y documentación. La propuesta de mesa de otros términos requiere acto legal separado.

`PLAN-VISIBILIZACION-2026-09-23.md`: **NO-RECIBIDO**. Se buscó en el repositorio y en `/mnt/c/Users/PC0/Downloads/`; sólo estaba el input FRONT-1. El mapa U0 tampoco estaba en `origin/main` al abrir. No se asignó `NO-MEDIBLE-POR-DISEÑO` sin él.

## P3 · inventario de rutas que permanecen

La raíz tenía **48 archivos** de primer nivel al abrir (`find . -maxdepth 1 -type f | wc -l`); `ls -1 | wc -l` daba 53 entradas incluyendo carpetas. Cada candidato se cotejó por nombre con `rg -l -F` sobre `canon data forense tools tests corpus milpa docs AGENTS.md CLAUDE.md`. La referencia listada es un testigo, no la lista completa. Un sidecar sin cita textual sigue unido al cuerpo que sella.

| Archivo que se mantiene en raíz | Referencias | Consumidor o razón |
|---|---:|---|
| `PROPUESTA-cola-sondeo27-2026-08-14.md` | 6 | `forense/firmas-pendientes.tsv` |
| `PROPUESTA-reconciliacion-universo-puertas.md` | 11 | `canon/gobernanza-v1_15.md` |
| `PROPUESTA-remediacion-brecha-documental.md` | 20 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_10.md` | 35 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_11.md` | 22 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_12.md` | 62 | `forense/agente-revisor-v1_0.md` |
| `instrucciones-proyecto-v2_13-DELTA-2026-09-08.md` | 4 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_13-DELTA-2026-09-08.md.sha256` | 0 | `sidecar de sello; se mantiene junto al cuerpo` |
| `instrucciones-proyecto-v2_13.md.sha256` | 3 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_14-HISTORIA.md` | 6 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_15-HISTORIA.md` | 4 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_15-HISTORIA.md.sha256` | 0 | `sidecar de sello; se mantiene junto al cuerpo` |
| `instrucciones-proyecto-v2_15.md` | 8 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_15.md.sha256` | 0 | `sidecar de sello; se mantiene junto al cuerpo` |
| `instrucciones-proyecto-v2_4.md` | 10 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_5.md` | 13 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_6.md` | 23 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_7.md` | 8 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_8.md` | 16 | `canon/gobernanza-v1_15.md` |
| `instrucciones-proyecto-v2_9.md` | 18 | `canon/gobernanza-v1_15.md` |
| `propuesta-motor-adaptativo-celda-v0_1.md` | 9 | `tests/baseline.json` |
| `propuesta-motor-adaptativo-celda-v0_2.md` | 8 | `canon/gobernanza-v1_15.md` |
| `propuesta-motor-adaptativo-celda-v0_3.md` | 28 | `canon/gobernanza-v1_15.md` |
| `propuesta-motor-adaptativo-celda-v0_4.md` | 19 | `canon/gobernanza-v1_15.md` |
| `propuesta-motor-adaptativo-celda-v0_5.md` | 20 | `canon/gobernanza-v1_15.md` |
| `propuesta-motor-adaptativo-celda-v0_6.md` | 7 | `tests/test_celdas_d.py` |
| `propuesta-motor-como-contexto-2026-07-30.md` | 2 | `forense/RONDA-M-motor-matriz-veredicto-opus-2026-08-13-v1_0.md` |
| `propuesta-motor-matriz-v0_1.md` | 25 | `canon/gobernanza-v1_15.md` |
| `revision-programa-2026-07-31.md` | 50 | `canon/gobernanza-v1_15.md` |
| `revision-publicacion-2026-07-30.md` | 8 | `canon/gobernanza-v1_15.md` |

`AGENTS.md`, `CLAUDE.md`, `instrucciones-proyecto-v2_16.md` y su historia siguen en la raíz por vigencia. El objetivo de 12 se exceptúa: el mínimo seguro con este perímetro sigue por encima; no se reescribieron canon, data, specs ni encargos sellados para forzarlo.

## Receta Pages y verificaciones

Tras fusionar el PR, mesa activa GitHub Pages en Settings → Pages → Deploy
from a branch → `main` / `docs`. La portada queda en
`https://josanoforo.github.io/Modelado-Mexicano/`; las páginas remiten a
`canon/` y al resto del repositorio mediante URL del archivo versionado.
Zenodo y el DOI se asientan en un acto posterior.
`docs/guia-lectura-publica.md` cumple la pieza de informe: el nombre
`docs/informe.md` chocaba por nombre normalizado con un informe forense
y `docs/lectura-resultados.md` con un análisis de datos existente (T02).
Se eligió un nombre único para conservar la línea base sin editar el validador.

`python3 -m unittest tests.test_readme_derivado tests.test_enlaces_archivo`
contrasta los comandos permitidos de la portada y sus enlaces locales.
`python3 tests/check.py --baseline` sobre el árbol actualizado con
`origin/main` terminó **LÍNEA BASE: VERDE**, sin FAIL nuevos; T02 y T19c
pasaron. El registro de esa corrida está en
`/tmp/gen2-front-1-baseline-unique.log` durante esta sesión.
`CITATION.cff` se leyó como YAML 1.2 y no declara DOI, versión ni fecha
de release inventadas. El bloque «Límites declarados» de
`USO-ACEPTABLE.md` se comparó byte por byte con `origin/main`. No hay
`jekyll` ni `cffconvert` instalados aquí; se comprobó Markdown y YAML,
no el HTML completo de Pages ni el esquema CFF con `cffconvert`.

## NO-CORRIDO / RESERVAS

- P3, movimientos de instrucciones y propuestas: `FUERA-DE-PERÍMETRO` corregir referencias selladas; impacto: raíz conserva archivos; sucesor: acto de migración de rutas con autorización de los consumidores.
- PLAN-VISIBILIZACION: `NO-RECIBIDO`; impacto: no se archivó ni se usó; sucesor: mesa lo aporta si desea incorporarlo.
- Pages y Zenodo: `DECISIÓN-DE-MESA-PENDIENTE`; impacto: landing preparada sin activación ni DOI; sucesor: mesa.
- Render local Jekyll: `NO-VERIFICABLE-AQUÍ` si no está instalado; impacto: se validan Markdown y enlaces dirigidos, no HTML final.

## CONSUMIDO

`forense/encargos/2026-09-23-GEN2-FRONT-1.md`, lado de corrección SOL6 y original verbatim; SHA del 0-bis en su sidecar.
