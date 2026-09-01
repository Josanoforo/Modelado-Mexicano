# Cierre — `ACTO MAESTRA33-E10 · PROCEDIMIENTO-SCORING-v1_1-PROPUESTA`

1/sep/2026. SHA de redacción del encargo: `a71c9ea`. `main` se movió a
`b3c6a1d` antes de arrancar (fusión de `PR #427`, `ACTO MAESTRA33-E9 ·
L-SPEC-v1_1`) — refrescado antes de escribir nada sustantivo, sin
diferencia de perímetro (el encargo no dependía de ningún contenido de
`L-spec-v1_1.json`, solo de que existiera fusionado). Entorno `NUBE`
(`cloud_default`). `COMPUERTA: PR de MAESTRA33-E9 fusionado`.

## Arranque

- Repo: `/home/user/Modelado-Mexicano`, working tree limpio al arrancar.
- `data/raw/`: presente (clon no fresco en este punto de la sesión) —
  no examinado, este acto no toca microdato.
- Entorno: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`. Este acto
  no toca microdato ni red real (perímetro: un `.md` de propuesta, un
  cargador sin ejecutar, notas, tablero) — sonda de red y `ls data/raw/`
  saltadas por esa razón, declarado en vez de corridas.
- Espejo: no usado: toda cita de este acto sale del clon, con el comando o
  la ruta+línea a la vista.

## COMPUERTA — verificada mecánicamente antes de escribir

`git fetch origin main` (1/sep/2026, ~04:45 UTC): `origin/main` avanzó de
`a71c9ea` a `b3c6a1d`. Cuatro verificaciones independientes, buscando
`maestra33-e9`/`MAESTRA33-E9`, todas positivas:

1. `git log --oneline origin/main | grep -i "maestra33-e9"` → 3 líneas
   (`## CONSUMIDO: MAESTRA33-E9 ejecutado, PR #427`; `Cascada: ADR-254...`;
   `A.3: archiva ENCARGO MAESTRA33-E9 · L-SPEC-v1_1 verbatim`), sobre 309
   commits examinados (`git log --oneline origin/main | wc -l`).
2. `search_pull_requests` (GitHub, `repo:Josanoforo/Modelado-Mexicano
   maestra33-e9 in:title,body`) → `PR #427`, título `[MAESTRA33-E9]
   L-spec-v1_1`, `state: closed` (fusionado — el merge commit `b3c6a1d`
   en `origin/main` lo confirma, un PR cerrado sin fusionar no deja merge
   commit).
3. `canon/registro-rotulos.tsv`: fila `MAESTRA33-E9` ya censada.
4. `mesa-pendientes.md` §4: recibo de `L-spec-v1_1.json` ya asentado.

**CUMPLE.** Antes de esta verificación (turno anterior de esta misma
sesión), la misma compuerta se había verificado como NO CUMPLIDA — cero
commits en ese momento, declarado y reportado sin escribir ningún archivo
(ni `A.3`). Este acto es el re-lanzamiento, tras confirmar el merge real de
`PR #427`.

## P1 — `procedimiento-scoring-v1_1-PROPUESTA.md`

Cinco puntos, cada uno con cita de línea del texto sellado del que deriva
(ver el documento para la tabla completa de citas). Idea central: la banda
ya sellada (`Δ_material = 0.5·EE(R)`, `FP-163`/`ADR-199`) no cambia — la
unidad de medición sí (`z = dif/EE(R)`), y esa reexpresión es lo único que
hace representable el escalar `delta` que `Configuracion.delta`
(`scoring-adv1-m3.py:87`) exige. El agregado (ii) y la comparación pareada
(iii) reutilizan las primitivas de bootstrap del motor sellado
(`generar_indices_bootstrap`/`derivar_seed_scope`) sin tocarlas, adaptando
solo la cantidad que remuestrean (de `skill` a `z`) porque `skill` exige un
`baseline` que (iv) declara NO-APLICA para marco-M — verificado en este
acto contra `corridas-R/_corredor-B.json` (0 de 0 celdas marco-M tienen
entrada) y contra `milpa-whitepaper-v0_1.md` §10 (asimetría declarada: `L`
y `M` comparten familia de LLM). PASO 1 de `adjudicar_secuencia`
(`scoring-adv1-m3.py:927-937`, requiere `skill`) se omite explícitamente
por esa misma razón; solo PASO 2 (regla `±delta`) se reutiliza. (v) hereda
la exclusión de `VERIFICACION-NO-PUNTUA` que `tools/score_marco_m.py` ya
aplica, sin redefinirla.

Corrección declarada: dos citas a `ACTO MAESTRA33-E8` quedaron sin el
prefijo de espacio en la redacción inicial — detectado por la misma regex
que `T25` usa, corregido antes de la cascada, sin registrar excepción
(D-6/ADR-128).

## P2 — cabecera + `carga_scoring_v1_1_propuesta.py`

Cabecera del documento declara **4 celdas M-vs-R visibles en `main` al
redactar** (`CIV-M-01/06/08/09`, `scoreboard-v1_1.md` §2, líneas 63-68,
`ACTO MAESTRA33-E8 · SCORE-M-1`) y que ninguna cifra de esas 4 celdas
(`p`, `R`, `EE(R)`, `dif`) se usó para fijar `delta=0.5`: la banda que lo
produce se selló el 26/ago/2026 (`FP-163`/`ADR-199`), cinco días antes de
que la corrida del 1/sep que produjo esas 4 cifras existiera — no hay ruta
causal posible.

`carga_scoring_v1_1_propuesta.py`: importa `tools/score_marco_m.py` por
ruta de archivo (mismo patrón que `carga_l_v1_1.py` con `pipeline-L
-adv1-m2.py`), sin editarlo (`git status --porcelain -- tools/
score_marco_m.py` vacío tras este acto). Le añade el único campo que esa
función deja deliberadamente ausente (`configuracion.delta = 0.5`);
`celdas`/`mediciones` no se tocan. **Este script no se ejecutó en este
acto** — ni siquiera un `--dry-run`: el perímetro del encargo dice "el
cargador (sin ejecutar)", léase literal.

## P3 — `mesa-pendientes.md` §5

Fila nueva, cinco decisiones enumeradas, con espacio para la firma de mesa
en una línea (`**Firma de mesa:** _(pendiente)_`). Declarado en la propia
fila: firmarla no ejecuta nada — `tools/score_marco_m.py` y
`scoring-adv1-m3.py` siguen intocados.

## Archivos abiertos durante este acto (declarado)

`procedimiento-scoring-v1_0.md`, `scoring-adv1-m3.py`, `scoreboard-v1_1.md`,
`tools/score_marco_m.py`, `.claude/commands/score.md`, `marco-M-sorteado
-v1_1.tsv` (header), `corridas-R/_corredor-B.json`, `corridas-R/CIV-M-01
.json` (esquema), `milpa/milpa-whitepaper-v0_1.md` §10, `mesa-pendientes
.md`, `PAQUETE-L-v1_1.md`, `L-spec-v1_1.json` (cabecera), `carga_l_v1_1.py`
(patrón de `importlib`), `canon/gobernanza-v1_15.md`, `canon/estado
-programa-v1_10.md`, `canon/registro-rotulos.tsv`, `tests/check.py`
(regex `_T25_ROTULO_BARE`). **No se abrió** `corridas-M/` más allá del
conteo ya público en `scoreboard-v1_1.md`; no se abrió ninguna celda de
`corridas-L/` (no existen para marco-M todavía, `L pendiente: 11 de 11`).

## Cascada

- ADR re-derivado por comando: `grep -oE '^\*\*ADR-[0-9]+'
  canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1` →
  `254`, sin huecos → candidato **`ADR-255`**. Sin otro acto en vuelo
  conocido **en ese momento** — declarado antes de abrir el PR, no
  garantía contra lo que se fusione mientras el PR sigue abierto.
- **Colisión real, detectada al sincronizar antes de cerrar.** Entre abrir
  `PR #429` y este `git merge origin/main`, dos actos más fusionaron:
  `PR #426`/`ACTO MAESTRA33-C5` tomó `ADR-255` (el mismo candidato de este
  acto) y `PR #428`/`ACTO MAESTRA33-S1` tomó `ADR-256` — ambos antes de
  que este PR se fusionara, así que por regla de la casa (renumera quien
  fusiona segundo) este acto renumera de `ADR-255` a **`ADR-257`**,
  contiguo al nuevo máximo. Conflicto real de `git merge` en las tres
  tablas de cascada (`gobernanza`, `estado-programa`, `registro-rotulos`)
  — ninguna de las tres inserciones de `C5`/`S1` se descartó, se conservan
  íntegras; solo la posición y el número de la entrada de este acto
  cambiaron.
- `canon/gobernanza-v1_15.md`: entrada `ADR-257` insertada antes de
  `ADR-256` (`MAESTRA33-S1`, ya fusionada) — texto de `ADR-256`/`ADR-255`
  /`ADR-254` intacto. Cabecera `256 → 257 ADR`.
- `canon/estado-programa-v1_10.md`: `L0` recifra `256→257`, anotación
  nueva insertada antes de la de `ADR-256`/`SORTEO-v3-Y-PROPAGA`.
- `canon/registro-rotulos.tsv`: `MAESTRA33-E10` censado, espacio `E`.
- `tests/check.py --baseline`: ver salida cruda al pie de este cierre —
  sin `FAIL` nuevo.
- Anti-`PR#77`: no aplica — este acto no descarga nada.
- `## CONSUMIDO` añadido a `forense/encargos/2026-09-01-MAESTRA33-E10
  -PROCEDIMIENTO-SCORING-V1_1-PROPUESTA.md` con el número de PR, en un
  commit posterior a abrirlo (el número no existe antes de eso).

**CONTADOR: cero** — ningún corredor corrido, `ejecutar_scoring` no
invocado, `tools/score_marco_m.py`/`scoring-adv1-m3.py` sin diff. La
propuesta reconcilia reglas; no produce una sola medición nueva.
