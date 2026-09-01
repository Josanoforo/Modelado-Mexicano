ENCARGO · MAESTRA33-S1 · SORTEO-v3-Y-PROPAGA — invoca /acto · ESTADO: LISTO-NUBE
SHA de redacción: a71c9ea. ENTORNO: NUBE. COMPUERTA: ninguna. MODELO SUGERIDO: Sonnet.
FIRMAS DE MESA (verbatim): «[FP-213: tu firma de la opción A, con el número correcto]» · «[FP-190: cierre de fase 2-A y enrutado a adquisición, si apruebas D2]».
P1 · forense/prereg-duelo-v2/sorteo_v3.py: piso 1 por estrato no vacío y Hamilton sobre el resto; sorteo_v2.py intacto. Regresión: reproduce B′ (v1_0) byte a byte si el piso no ligaba ahí; sobre la semilla de v1_1 reporta qué habría cambiado, SIN escribir ningún sorteado nuevo (opción A: v1_1 se acepta tal cual).
P2 · reglamento-sorteo-v1_1-PROPUESTA.md: regla 3 con su implementación exacta, PENDIENTE-DE-MESA.
P3 · Propaga FP-213 verbatim (declara la renumeración 212→213) y, si viene la segunda firma, cierra FP-190 fase 2-A y escribe las 6 filas nombradas en data/cola-adquisicion-v1_0.tsv con qué instrumento satisfaría cada una (de E7 y C4).
PERÍMETRO: sorteo_v3.py, reglamento-sorteo-v1_1-PROPUESTA.md, tablero, cola-adquisicion, notas, A.3, cascada. Frase exacta vigente. CONTADOR: cero. LO QUE NO HACE: no re-sortea v1_1; no toca marco ni sorteado; no edita sorteo_v2.py.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-S1 · SORTEO-v3-Y-PROPAGA`, 1/sep/2026, entorno
**NUBE** (`cloud_default`), rama `claude/maestra33-sorteo-v3-propaga-zb84bu`,
**`PR #428`** (https://github.com/Josanoforo/Modelado-Mexicano/pull/428).
Commits: `98899dd` (0-bis A.3, este archivo) · `a4ed6c8` (`P1`,
`sorteo_v3.py` + `tests_sorteo_v3.py` + nota de regresión) · `b5ad2ae`
(`P2`, `reglamento-sorteo-v1_1-PROPUESTA.md`) · `baa4b75` (`P3`, `FP-213`
firmada + `FP-190` fase 2-A cerrada + 6 filas de `data/cola-adquisicion-
v1_0.tsv`) · `19bbebb` (merge de `origin/main`, `PR #426`/`PR #427`, sin
conflicto, sin tocar el perímetro) · `af8e5ea` (cascada: `ADR-256`,
`estado-programa` `L0`/tabla de artefactos, `registro-rotulos.tsv`
`MAESTRA33-S1`, `T25`/`T22`).

`COMPUERTA: ninguna` — declarada por el encargo, sin gate que verificar.
`SHA de redacción a71c9ea` = tip literal de `origin/main` al arrancar, sin
drift. `main` avanzó 2 merges durante el acto (`ADR-255`/`MAESTRA33-C5`,
`ADR-254`/`MAESTRA33-E9`) — ninguno tocó el perímetro de este acto,
refrescado por `git merge origin/main` antes de cerrar, sin conflicto.

`P1`/`P2`/`P3` ejecutados tal como el encargo los describe. Las dos
"FIRMAS DE MESA" del encargo (bracket verbatim) se leyeron como contenido
operativo, no como placeholder sin llenar: `P1` mismo resuelve "opción A"
como hecho ("v1_1 se acepta tal cual"), y la segunda firma de `FP-190`
llegó junto con la primera en el mismo encargo — condición de `P3`
("si viene la segunda firma") satisfecha por su sola presencia. `sorteo_v3.py`
implementa la regla 3 completa (piso 1 + Hamilton sobre el resto);
regresión verificada contra datos reales (`B′`, `v1_1`), no supuesta —
detalle en `forense/notas/2026-09-01-sorteo-v3-regresion-v1_1.md`.
`reglamento-sorteo-v1_1-PROPUESTA.md` queda `PENDIENTE-DE-MESA`, con
recibo propio (`FP-216`, `ABIERTA`) para que no se pierda de vista.

`python3 tests/check.py --baseline`: **VERDE**, `19 FAIL · 162 WARN`, sin
entrada nueva frente a `tests/baseline.json`. Dos hallazgos nuevos
encontrados y corregidos en el camino del propio cierre, declarados: `T15`
(tabla de artefactos de `estado-programa` sin recifrar) y `T22`
(`reglamento-sorteo-v1_1-PROPUESTA.md` sin fila de tablero que lo citara).
Perímetro respetado: `sorteo_v2.py`, `sorteo_marco_m.py`,
`sorteo_marco_m_v1_1.py`, ambas suites de test previas y los cinco
marcos/sorteados del duelo (piloto v1_0, marco-M v1_0, marco-M v1_1) sin
diff, verificado. Anti-`PR#77`: no aplica, este acto no descargó nada. PR
abierto contra `main`, **no fusionado por este acto** — el merge es de
mesa.
