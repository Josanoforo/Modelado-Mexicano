# Nota de cierre — ACTO GEN2-TUBERIA-EFICIENCIA-1 (22/sep/2026)

Encargo: `forense/encargos/2026-09-22-GEN2-TUBERIA-EFICIENCIA-1.md` (0-bis
`0d1ba7f`, sello de cuerpo `9c4d646`). Base: `6901853c` (coincide con el
SHA de redacción). ARRANQUE: rama `claude/pensive-hamilton-xzr9gt` estaba
ya fusionada en `origin/main` (remoto borrado por política de cero ramas)
— se reinició desde `origin/main` con el mismo nombre antes de arrancar,
sin perder trabajo (no traía commits propios sin fusionar).

## Verificación de existencia (por objeto, contra `6901853c`)

- **P1** (subconjunto rápido): ya en `tests/check.py --rapido`
  (T02/T22/T25/T15/T27/T30/T34 + sidecars), 2.34s medido — resuelto por
  `GEN2-TUBERIA-CIERRE-RAPIDO-1`.
- **P2** (T16 fuera): confirmado, cero `def t16` ejecutable; el retiro y
  su razón están documentados en `tests/check.py:8183` — resuelto por el
  mismo acto.
- **P3** (baseline estricto, WARN fuera de la adjudicación): `ADR-534`
  (16/sep) ya lo estableció; el baseline actual solo adjudica por FAIL.
- **P6** (cascada de una sola corrida): `.claude/commands/acto.md` y
  `tools/cierre_acto.py` ya piden `--rapido` una sola vez antes de
  empujar.

Ninguna de las cuatro se reimplementó. Lo que sí faltaba, verificado
contra `.github/workflows/verify.yml` (sin mención de "derivado") y
`forense/no-corrido.tsv` (NC-...-3619-01/02 ABIERTA):

## P0 — sonda

No hay `gh` en este entorno. Se preguntó a mesa en una línea (vía
pregunta estructurada) mientras se seguía con el resto: **main no exige
ramas al día**. El diseño de P4 asume push directo del job derivador, sin
cola de merge.

## P4 — derivados fuera de los PR

`tools/derivados_protegidos.py`: deriva por comando (grep de la cabecera
`# DERIVADO — NO EDITAR` sobre `git ls-files`) la lista de archivos
protegidos — nunca a mano. `.github/workflows/verify.yml`: paso nuevo en
`enrutamiento-pr` que falla un PR que toque un derivado; paso nuevo en
`guardias`, solo en push a `main`, que corre `marcador_segmento.py
--escribe` y `corrida0.py demanda` (los dos derivadores deterministas sin
juicio de mesa) y commitea `[deriva]` solo si hay diff, con salida
temprana si el commit disparador ya es `[deriva]` (sin loop). Los pasos
van dentro de jobs existentes, no en jobs nuevos: un job nuevo dobla la
matriz `6**N_jobs` de `tests/test_check_parallel.py::WorkflowGate` y deja
de caber en el timeout de 10 min (medido `6**6≈100s`; con un job más no
terminó en 300s). `corrida0.py registro` (exige `--lote`, juicio de mesa)
queda deliberadamente fuera — D-19. `acto.md` no re-derivaba estos
archivos a mano; no hubo nada que quitarle. Test propio:
`tests/test_derivados_protegidos.py` (3 pruebas), censado como huérfano
en `forense/analisis/ci-guardias/censo-tests.tsv` (D-21).

## P5 — contador de celdas-D adoptadas

Nuevo indicador `celdas_d_adoptadas_activas` en `tools/tablero_programa.py`,
derivado de `champion_actual` en `data/curacion-registro/celdas-d/*.yaml`.
Antes: 0 (no existía). Después: 6, incluida la celda-D del piloto 3
(`GOB.gobierno_digital.encig2025.edad_x_escolaridad`, `champion_actual:
C2`, firma F3). Hallazgo: `celdas_validadas` ya contaba las 15 celdas del
piloto 3 desde `PR #969` (`GEN2-MARCADOR-E-INFORME-1`, criterio de
veredicto sellado) — 73→92 hoy, no un mecanismo de este acto. Se cierra
`NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-3619-02` citando ese
hallazgo. `NC-...-3619-01` queda ABIERTA: el par de
`marcador-segmento.tsv` sigue `RESERVADA` porque `tools/marcador_segmento.py`
es ajeno a este acto (§9); el contador nuevo no depende de ese
re-derivado. Ningún número ya sellado de celda-D se tocó.

## Suite

`tests/check.py --rapido`: VERDE, 0 FAIL, 2.34s (verificado antes de cada
commit). `tests/check.py --baseline --parallel` (suite completa) se lanzó
antes de empujar; el CI la vuelve a correr en el push y es el juez —
firma de mesa 21/sep citada por `GEN2-TUBERIA-CIERRE-RAPIDO-1`: "antes de
empujar, un acto corre solo el subconjunto rápido; la suite completa la
corre el CI una vez en el push y ése es el juez."

## No corrido (ver `## NO-CORRIDO / RESERVAS` del encargo archivado)

- P7 (medición de cierre sobre 20 PR post-merge): depende de que este
  lote se fusione primero. Sucesor: `EFICIENCIA-2` (ya previsto por el
  propio encargo).
- NC-...-3619-01: sigue ABIERTA, ajena a este acto (marcador-segmento.py,
  §9).
