# Nota de cierre — `ACTO MAESTRA33-E8 · SCORE-M-1`

1/sep/2026. Worktree `/home/pc0/mm-worktrees/maestra33-e8-score-m-1`,
rama `acto/maestra33-e8-score-m-1`, creada fresh sobre `origin/main`.

## ARRANQUE

1. **REPO.** Clon existente, worktree limpio en `65dcd0d` al iniciar.
2. **SHA.** El encargo se redactó contra `d353d82`; `origin/main` avanzó
   25 commits (`HEAD` real `65dcd0d`). No es PARO, pero cambia el terreno
   de A.8 de forma material — ver §"Terreno movido" abajo.
3. **data/raw.** Enlazado a `/home/pc0/mm-corpus/raw` (corpus montado).
   Este acto no abre microdato ni descarga nada (NUBE, sin red sustantiva).
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacío
   (`sin_variable`); `curl -s -o /dev/null -w "%{http_code}" --max-time
   10 https://www.inegi.org.mx/` → `200`; `ls data/raw/ | head -1` no
   vacío (corpus montado, aunque este acto no lo usa).
5. **ESPEJO.** No consultado; todas las cifras de esta nota salen del
   clon de (1) con el comando a la vista.

## COMPUERTA

`COMPUERTA: PR de MAESTRA33-E6 (EMISOR-M-1) fusionado`. Verificado:
`git log --oneline origin/main | grep -c maestra33-e6-emisor-m-1` → 1
commit de merge (`e754043`, `PR #422`). **CUMPLIDA.**

## Terreno movido contra A.8 del encargo (declarado, no escondido)

El encargo asumía (A.8, contra `d353d82`): "corridas-L: 120 archivos, 0
con ids del marco-M" y "probablemente 0 celdas puntuables hasta que C3
entregue R". En los 25 commits que pasaron entre `d353d82` y `65dcd0d`:

- `ACTO MAESTRA33-C3 · CODIFICA-R-1` (`PR #423`) ya corrió y produjo `R`
  real para 19 celdas (`corridas-R/`): 15 del marco anterior a F-DD
  (`CIV-08`, `DIN-03/05/07/11`, `DOC-06`, `EMP-02/04/05`, `SFT-04/06`,
  `TIC-01/06/08/12`) más **4 del marco v1.1** (`CIV-M-01/06/08/09`).
- `ACTO MAESTRA33-E6 · EMISOR-M-1` (`PR #422`, la propia compuerta de
  este acto) ya emitió 13 puntos `M` (`corridas-M/M-<id>.json`) para el
  universo v1.1 completo (11 celdas) más `TRA-M-01/02` del marco v1.0.
- `corridas-L/` sigue en 120 archivos, **0** con ids del marco-M v1.1 —
  esa parte de A.8 sigue vigente sin cambio.
- `FP-168` (`nivel_ic`/`seed` del bootstrap de `scoring-adv1-m3.py`) —
  A.8 la cita como "sellada"; verificado por `grep -n "FP-168" ...`:
  **sí está `FIRMADA`** desde `ACTO MAESTRA32-E9 · PROPAGA-2`
  (30/ago/2026), `nivel_ic=0.95`, `seed=42`. A.8 acertó en esto.

Consecuencia: la premisa "probablemente 0 celdas puntuables" del encargo
ya no era cierta al arrancar este acto. Se reporta el número real (§P3
abajo), no el anticipado.

## 0-bis A.3

Primer commit (`2675c0e`): encargo archivado verbatim en
`forense/encargos/2026-08-31-MAESTRA33-E8-SCORE-M-1.md`.

## P1 · `tools/score_marco_m.py`

Construye la entrada de `scoring-adv1-m3.py` (sin editarlo) desde
`marco-M-sorteado-<sufijo>.tsv` + `corridas-M/M-<id>.json` +
`corridas-R/<id>.json` + `corridas-L/*__<id>__*.json` (glob invertido,
ver código — el nombre de archivo de L es `<id>__L-<variante>__NN.json`).
Declara por celda banderas `M`/`R`/`L` y excluye del puntaje toda celda
con `grado_DD` conteniendo `NO-PUNTUA` (F-DD, `ADR-237`) — 0 de 11
celdas del universo v1.1 caen en esa categoría (todas `P1 PUNTUA`; las 5
celdas `P0 VERIFICACION-NO-PUNTUA` de `marco-M-congelado-v1_1.tsv` no
fueron sorteadas en v1.1 y no aparecen en este universo). Regla de
puntaje aplicada: **R presente Y (M o L presente)**; verificado que sin
`R` la celda no puntúa aunque tenga `M` (11 de las 11 tienen `M`, solo 4
tienen `R`, así que las 7 restantes no puntúan pese a tener `M`).

## P2 · Regresión — **PASA**

Se tomó `documento_de_entrada` de
`forense/prereg-duelo-v2/corridas-M/_intento-scoring-v1_1.json`
(el mismo documento verbatim que produjo el resultado de v1.0, §6 de
`procedimiento-scoring-v1_0.md`) y se invocó `ejecutar_scoring` de
`scoring-adv1-m3.py` directamente (sin editarlo), en vivo:

```json
{"resultado": "ErrorScoring", "codigo": "CONFIGURACION_INVALIDA", "mensaje": "faltan parámetros obligatorios: delta, nivel_ic, seed"}
```

**Idéntico byte a byte** (mismo `codigo`, mismo `mensaje`, misma
estructura) al resultado verbatim citado en
`procedimiento-scoring-v1_0.md §6`. Regresión conforme — **no hay PARO**,
se continúa a P3.

## P3 · Primera corrida sobre v1.1

`python3 tools/score_marco_m.py` sobre `marco-M-sorteado-v1_1.tsv` (11
celdas): **4 celdas puntuables** (`CIV-M-01/06/08/09`, las únicas con
`R` real), **no 0** como el encargo anticipaba — declarado tal cual, sin
maquillar. `L pendiente: 11 celdas` (recalculado contra el árbol, no
copiado del "11" del encargo — coincide por tamaño de universo, no por
herencia de texto).

Con la `entrada_scoring` real (`nivel_ic=0.95`, `seed=42` ya sellados por
`FP-168`, `delta` deliberadamente ausente), se invocó `ejecutar_scoring`
en vivo sobre las 4 celdas puntuables (`mediciones={}` por ausencia de
baseline `B`, mismo hallazgo estructural que `E9`):

```json
{"resultado": "ErrorScoring", "codigo": "CONFIGURACION_INVALIDA", "mensaje": "faltan parámetros obligatorios: delta"}
```

**Un parámetro menos que en v1.0** — la sella de `FP-168` sí redujo el
bloqueo real de tres campos a uno. `delta` sigue sin cita como escalar
único de corrida en ningún documento del árbol (misma búsqueda
exhaustiva de `procedimiento-scoring-v1_0.md §3`, repetida: sin
resultado nuevo). No se inventa aquí.

Aritmética directa `M` vs `R` (sin pasar por `ejecutar_scoring`, mismo
método declarado que `procedimiento-scoring-v1_0.md §5`) para las 4
celdas puntuables: entregado en
`forense/prereg-duelo-v2/scoreboard-v1_1.md §2`. Ninguna de las 4 cae
dentro de su banda TOST (`±0.5·EE(R)`); `M` sobre-estima a `R` en las
cuatro.

`.claude/commands/score.md` creada, documentando el uso de
`tools/score_marco_m.py` para corridas futuras.

## CIERRE — cascada

- **ADR.** Máximo re-derivado por comando: `252` (contiguo, sin huecos,
  `ADR-252` ya en el árbol por `ACTO MAESTRA33-C4`, fusionado). Candidato
  `ADR-253`.
- **Gobernanza §4** — entrada `ADR-253` con este acto, citando el
  encargo archivado y el Gate verificado.
- **Recifrado L0** — `canon/estado-programa-v1_10.md`, conteo `252 →
  253`, anotación insertada antes de la de `ADR-252`.
- **`registro-rotulos.tsv`** — censa `MAESTRA33-E8`.
- **T25** — revisado; sin rótulo `M`/`E` pelado nuevo que requiera
  entrada en `_T25_ARCHIVOS_CONOCIDOS` (el encargo y esta nota citan
  `E8`/`E6`/`E7`/`C3` siempre con prefijo `MAESTRA33-`, verificado con el
  mismo regex que `tests/check.py::_T25_ROTULO_BARE` usa).
- **`tests/check.py --baseline`** — ver salida cruda al pie de esta nota.
- **Anti-PR#77** — N/A, este acto no descarga nada.
- **`## CONSUMIDO`** — añadido al encargo archivado.
- **PR** — abierto contra `main`, sin fusionar.

## CONTADOR

Celdas puntuadas: **0 → 4** (universo `marco-M-sorteado-v1_1.tsv`, 11
celdas). `ejecutar_scoring` agregado: sigue bloqueado, ahora solo por
`delta` (antes por `delta`+`nivel_ic`+`seed`). `L pendiente: 11 celdas`.

## LO QUE ESTE ACTO NO HACE

No edita `scoring-adv1-m3.py`. No emite `M`, `R` ni `L` nuevos. No activa
el corredor `E`. No cambia la Configuración sellada (`FP-168`,
`M-ENLACE=A`, `M-AGREGA=a′`).
