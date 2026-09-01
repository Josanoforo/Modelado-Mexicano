ENCARGO · MAESTRA33-E11 · CRITERIOS-Y-VENCIMIENTOS v1.1 — invoca /acto
SHA de redacción: c7fa424. ENTORNO: NUBE — NO CAJA. COMPUERTA: PR #429 (E10) fusionado; si no, cero commits. MODELO SUGERIDO: Opus.
FIRMAS DE MESA (verbatim, 1/sep/2026): «3. De acuerdo, pasan a extrerno/adquisicion de datos y asigna el área» · «4. Dato informativo.» · «5. Esa semana, pero ponle fecha no quiero que se quede volando» · «6. Tachemos los dos … deja claro y estipulado cuales quedan pendientes» · «7. Se cierra.» · «9.Si pero dejando claro cuando se abren o bajo qué criterios se abren» · «10. Banca, pero deja claro los criterios de avance».
A.8 (dirección contra c7fa424): S1 propagó FP-213 y las 6 filas de adquisición; NO propagó firmas 3/4/6/7 (FP-190, FP-179, FP-212/214/215 siguen ABIERTA, verificado). Criterios de apertura de dominio y de activación del corredor E: NO-ENCONTRADO en canon/motor-nucleo-medible-v1_0.md. "vence:" en el digesto: NO-ENCONTRADO (tools/digesto_tramite.py, 0 menciones).
P0 · Propaga: FP-190 → fase 2-A cerrada (firma 3), EMP-05 asignada a R5.3 (modelo-decision-v4_0.md:537, sin G# explícito, declarado), TIC-01 "cita sin uso, sin generador"; corresidencia_actual → θ informativa en procedencia.yaml (escala [0,1], universo jefes/cónyuges) y entrada de propuesta APARCADA (firma 4); FP-179 → (1)(2) EJECUTADAS, (5) "verificar contra ADR-134 — C7", (3)(4) como filas C8/C9 con vence 2026-09-07 / 2026-09-08 (firma 6); FP-212/214/215 FIRMADAS (firma 7).
P1 · Enmienda fechada en canon/motor-nucleo-medible-v1_0.md: (a) Ola 6 — un dominio se abre cuando existe scoreboard agregado con L sobre los 4 activos, el candidato tiene ≥2 encuestas en corpus con ≥3 reglas candidatas EXISTE-SATISFACE por /mapea, y hay caja libre; primera evaluación: al primer agregado con L o el 15/sep, lo primero (firma 9). (b) Corredor E — se activa cuando L y M tienen puntos en ≥8 celdas comunes y el scoring v1_1 está sellado; revisión: al publicarse el agregado o el 30/sep (firma 10).
P2 · Digesto v1_2: parsea "vence: AAAA-MM-DD" en la columna gatea; abre con "VENCIDAS" y "vencen esta semana"; el WARN de T22 trae días de retraso.
P3 · Filas con vencimiento: L-CORRIDA-v1_1 (mesa; vence 2026-09-04), SELLO-SCORING-v1_1 (mesa; vence 2026-09-03 — si E10 ya abrió la suya, añade el vence ahí, no dupliques), EVALUACION-OLA6 (dirección; 2026-09-15), REVISION-CORREDOR-E (dirección; 2026-09-30), REVISION-FALSADORES (dirección; 2026-09-30).
PERÍMETRO: tablero, milpa/procedencia.yaml, milpa/tramite-ola5-propuesta-v0.yaml (estado), motor-nucleo-medible-v1_0.md (enmienda), tools/digesto_tramite.py, runbook de trámite §2, notas, A.3, cascada. Frase exacta vigente. FP/ADR: deriva. CONTADOR: cero, declarado.
LO QUE NO HACE: no abre dominios; no activa E; no corre L; no cambia la puerta de activación sellada; no inventa firmas — solo las siete de arriba.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E11 · CRITERIOS-Y-VENCIMIENTOS`, 1/sep/2026,
entorno **NUBE** (`cloud_default`), rama
`claude/maestra33-e11-criterios-lzmrvc`, **`PR #432`**
(https://github.com/Josanoforo/Modelado-Mexicano/pull/432). Commits:
`354b5ce` (0-bis A.3, este archivo) · `c22557c` (P0 + P3: tablero
`FP-190`/`FP-179`/`FP-212`/`FP-214`/`FP-215` enmendados, `FP-217`..
`FP-222` nuevas; `milpa/procedencia.yaml`; `milpa/tramite-ola5-
propuesta-v0.yaml`; `mesa-pendientes.md` §5) · `0ebce01` (P1:
`canon/motor-nucleo-medible-v1_0.md` §3) · `5ed335f` (P2: `tools/
digesto_tramite.py` v1.2, `tests/check.py::t22_firmas`, `forense/
agente-tramite-v1_0.md` §2) · `203f9e3` (nota de cierre) · `f291ebb`
(cascada: `ADR-258`, recifrado `L0`, `registro-rotulos.tsv`, `T25`).

`COMPUERTA: PR #429 (E10) fusionado` — **CUMPLE**, verificada contra
`origin/main = 02ec20b` al arrancar (el propio `HEAD` de `origin/main`
es el merge commit de `PR #429`); sin drift durante el acto
(`origin/main` seguía en `02ec20b` al cerrar). `SHA de redacción
c7fa424` — `main` había avanzado 3 commits antes de arrancar (fusión de
`PR #429`/`ACTO MAESTRA33-E10` + la resolución de colisión de
`ADR-255`), ninguno tocó el perímetro de este acto (los tres solo
tocan las tablas de cascada que este mismo cierre vuelve a tocar).

P0/P1/P2/P3 entregados tal como el encargo los pidió; las siete firmas
de mesa (3, 4, 5, 6, 7, 9, 10) propagadas verbatim, ninguna inventada.
`FP-179` C7/C8/C9 y la tensión declarada (no resuelta) de `FP-218`
sobre (4) quedan documentadas en detalle en la nota de cierre.
CONTADOR: cero (ningún corredor corrido, ningún microdato abierto,
declarado). `python3 tests/check.py --baseline`: **VERDE**, `19 FAIL ·
168 WARN`, sin entrada nueva frente a `tests/baseline.json` (dos
hallazgos nuevos del propio cierre — `T15`, segunda cita de conteo de
ADR sin recifrar; `T25`, `E10` pelado en dos archivos nuevos — ambos
corregidos en el camino, declarados). Detalle completo, con cita de
línea por punto: `forense/notas/2026-09-01-criterios-y-vencimientos-
cierre.md`. PR abierto contra `main`, **no fusionado por este acto** —
el merge es de mesa.
