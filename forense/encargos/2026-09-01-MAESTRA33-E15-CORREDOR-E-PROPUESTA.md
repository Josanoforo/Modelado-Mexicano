ENCARGO · MAESTRA33-E15 · CORREDOR-E-PROPUESTA — invoca /acto
SHA de redacción: ee6a8a2. ENTORNO: NUBE. COMPUERTA: E13 fusionado. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 1/sep/2026): «10. Banca, pero deja claro los criterios de avance».
A.8: whitepaper:213-217 define E como "LLM con datos, sin estructura", ranura en la Configuración sellada, no activada; criterio de activación (E11): L y M con puntos en ≥8 celdas comunes + scoring v1_1 sellado — deriva el conteo real de corridas-L ∩ corridas-M al arrancar. FP-221 ABIERTA, vence 30/sep.
P1 · Si el criterio se cumple: propuesta operativa de E, PENDIENTE-DE-MESA — qué "datos" recibe exactamente el LLM (las θ y p medidas de procedencia.yaml, en texto, sin reglas SI-ENTONCES), spec derivada mecánicamente como la de L (E9), k, variantes, costo en llamadas, cargador SIN correr, y cómo entra en la Configuración sin tocar los corredores sellados. Si no se cumple: lo dice con el conteo y cierra.
P2 · FP-221 → resuelta con este acto (fecha real).
PERÍMETRO: notas, prereg-duelo-v2 (propuesta + cargador sin correr), tablero, A.3, cascada. Frase exacta vigente. CONTADOR: cero, declarado.
LO QUE NO HACE: no corre E; no edita scoring sellado; no cambia L ni M.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E15 · CORREDOR-E-PROPUESTA`, 1/sep/2026,
`ADR-264` (candidato), entorno **NUBE** (`cloud_default`), rama
`claude/propuesta-operativa-e-gshsnh`, **`PR #437`**
(https://github.com/Josanoforo/Modelado-Mexicano/pull/437). Commits:
`c490dea` (0-bis A.3, este archivo) · `f59c7cc` (P1: criterio de
activación de `E` NO cumplido — `L` y `M` con puntos en 0 celdas
comunes del marco-M-sorteado-v1_1, requerido ≥8, aunque scoring v1_1 sí
está sellado; P2: `forense/firmas-pendientes.tsv` `FP-221` →
`RESUELTA`) · `678e0a0` (cascada: `ADR-264`, recifrado `L0`,
`registro-rotulos.tsv`, `tests/check.py::_T25_ARCHIVOS_CONOCIDOS`).

`COMPUERTA: E13 fusionado` — **CUMPLE**, verificada contra
`origin/main` real (`git merge-base --is-ancestor f4d9b7f origin/main`,
`f4d9b7f` = merge commit de `PR #403`/`ACTO MAESTRA32-E13`); sin drift
de `origin/main` durante el acto (`ee6a8a2` al arrancar y al cerrar).

P1: **el criterio no se cumple** — conteo mecánico de `corridas-L/`
(120 archivos, 15 ids, exclusivamente del marco piloto de
`pipeline-L-adv1-m2.py`) contra `corridas-M/` (13 celdas con
`estado_M: EMITE`, superconjunto de las 11 del marco-M-sorteado-v1_1):
intersección = 0 celdas, requerido ≥8. No se redacta la propuesta
operativa condicional de `E` (no había base); no se creó cargador ni
se tocó `prereg-duelo-v2/` más allá de lectura. P2: `FP-221` →
`RESUELTA`, fecha real 1/sep/2026. `CONTADOR: cero` (ningún corredor
corrido, ningún microdato abierto, declarado). `python3 tests/check.py
--baseline`: **VERDE**, 19 FAIL preexistentes, sin FAIL nuevo. Detalle
completo, con comandos y salida: `forense/notas/2026-09-01-maestra33-
e15-corredor-e-propuesta-cierre.md`. PR abierto contra `main`, **no
fusionado por este acto** — el merge es de mesa.

**Renumerado post-push:** `git fetch origin main` reveló que `main`
avanzó (`PR #438`/`ACTO MAESTRA33-E17 · L-ENMIENDA-CLI`) mientras este
PR estaba en vuelo — `E17` fusionó primero y tomó el candidato
`ADR-264` (arriba); este acto renumera a **`ADR-265`**, contiguo, sin
hueco (regla de la casa, renumera quien fusiona segundo). `git merge
origin/main` con conflicto en `canon/gobernanza-v1_15.md`,
`canon/estado-programa-v1_10.md` y `canon/registro-rotulos.tsv`
(`tests/check.py` fusionó limpio), resuelto conservando las dos
inserciones (`E17`, este acto), en orden de fusión — verificado
`python3 tests/check.py --baseline`: **VERDE**, sin `FAIL` nuevo tras
resolver.
