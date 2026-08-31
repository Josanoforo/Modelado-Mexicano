# ENCARGO · MAESTRA33-E4 · DELTA-E3 — invoca `/acto`

*(Archivado verbatim por A.3 antes de ejecutar ningún paso sustantivo. Texto tal
como lo entregó dirección el 31/ago/2026. No se edita en ningún otro punto: es el
registro de qué se pidió, para poder auditar si el ejecutor hizo lo que se le dijo.)*

---

ENCARGO · MAESTRA33-E4 · DELTA-E3 — invoca /acto
SHA de redacción: 26cb24c. ENTORNO: NUBE — NO CAJA, NO doble. COMPUERTA: el PR de la rama claude/cableado-cola-digesto-affup3 (E3) fusionado en origin/main; si no, cero commits. MODELO SUGERIDO: Sonnet (dos cambios mecánicos, cero juicio).
FIRMA DE MESA (verbatim, 31/ago/2026): «[mesa escribe aquí, tal cual, su enterado de FP-205/206/207/208/209 y su decisión sobre las dos preguntas de FP-209; si queda vacío, P1 no se ejecuta]».
A.8 (dirección contra la rama de E3): acto.md sin equivalencia COMPUERTA≡GATED (grep GATED → solo la forma vieja) y sin paso de apertura de PR (grep -i "pull request|abre UN PR|gh pr" → 0, 1 archivo). Enterados: FP-205/206/207/208 ABIERTA en el tablero de la rama. Todo lo demás de E3 v1.1 (huérfano, F/G, falsadores): EXISTE-SATISFACE, no se toca.
P0 · acto.md, dos líneas: (a) el paso 2 reconoce "COMPUERTA:" como sinónimo de "GATED a", misma consecuencia (no cumplida → cero commits); (b) el cierre termina con "empuja la rama y abre UN PR contra main titulado con el rótulo del acto; NO lo fusiones" — salvo cuando el acto corre bajo /despacha, que ya lo hace.
P1 · Propaga la firma de mesa del corchete, verbatim, a FP-205/206/207/208/209 (FIRMADA con cita) y registra la decisión de FP-209 en el runbook de despacho §0 como decisión de mesa fechada.
PERÍMETRO: .claude/commands/acto.md (paso 2 y cierre), forense/agente-despacho-v1_0.md (§0), tablero, archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: cero, declarado.
LO QUE NO HACE: no toca despacha.md ni el digesto; no ejecuta la cola; no inventa firmas.

---

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E4 · DELTA-E3`, 31/ago/2026, entorno **NUBE**,
rama `claude/acto-md-firma-mesa-ec237o`, **`PR #416`**
(https://github.com/Josanoforo/Modelado-Mexicano/pull/416). Commits: `29afe26`
(0-bis A.3, este archivo) · `c3cc262` (`P0`, `.claude/commands/acto.md`) ·
cascada (`ADR-244` candidato, `canon/gobernanza-v1_15.md` y
`canon/estado-programa-v1_10.md` recifrados 243 → 244,
`canon/registro-rotulos.tsv` censado, `tests/check.py`
`_T25_ARCHIVOS_CONOCIDOS` extendido).

Compuerta verificada mecánicamente antes de editar nada: el merge de la rama
`claude/cableado-cola-digesto-affup3` (`8b6aa85`, `PR #415`) es el tip literal
de `origin/main`, y `git merge-base --is-ancestor 8b6aa85 origin/main` →
ancestro. SHA de redacción `26cb24c` movido a `8b6aa85` (3 commits, que son
exactamente la rama de la compuerta); diferencia declarada, perímetro
re-derivado.

`P0` ejecutado (dos líneas: `COMPUERTA:` ≡ `GATED a` en el paso 2; paso 9 de
cierre que empuja y abre UN PR sin fusionarlo, salvo bajo `/despacha`).
**`P1` NO ejecutado**: el corchete de FIRMA DE MESA llegó con el texto de
instrucción a mesa y no con una firma, y este encargo fija «si queda vacío,
`P1` no se ejecuta» — `FP-205`/`FP-206`/`FP-207`/`FP-208`/`FP-209` siguen
`ABIERTA` sin tocar y `forense/agente-despacho-v1_0.md` §0 no se editó. No se
inventan firmas. Contador: cero, declarado.

`python3 tests/check.py --baseline`: **VERDE**, sin `FAIL` nuevo frente a
`tests/baseline.json` (HEAD congelado `c6a0d72`).
