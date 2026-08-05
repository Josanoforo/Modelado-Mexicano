# ENCARGO M-1 — adjudicar `R3.1`→`B` y sellar ADR-60: la premisa 2 NO sostiene, PARO antes de Commit 1

**Contadores movidos: 0.** El propio encargo instruye lanzar este acto
*después* de que mesa fusione los PR de `sesion/hitoD-r3-1-encig` y
`sesion/pb-descargas-f2`, y declara en su premisa 2 que si la Nota 27 no
está en `main`, el acto para. Ninguno de los dos PR está fusionado. El
entregable de este acto es este reporte — "encontrar que el terreno no es
el que el encargo supone es entregable, no interrupción" (texto del propio
encargo, §1).

ENCARGO M-1, mesa #20, redactado 4/ago/2026 contra `origin/main = 4dca34c`
(ADR máximo declarado 59). Rama `claude/adjudicar-r3-1-adr-60-4as2g0`.

## 0 · Bloque de arranque (§1 del encargo)

```
$ pwd
/home/user/Modelado-Mexicano
$ git log -1 --format="%h %s"
4dca34c Merge pull request #103 from Josanoforo/claude/bloque-arranque-verificacion-n1byxs
$ git status
On branch claude/adjudicar-r3-1-adr-60-4as2g0
nothing to commit, working tree clean
$ git fetch origin main
 + 9301e59...4dca34c main -> origin/main (forced update)
$ git log -1 --format="%h %s" origin/main
4dca34c Merge pull request #103 from Josanoforo/claude/bloque-arranque-verificacion-n1byxs
$ git merge-base --is-ancestor 4dca34c HEAD && echo ancestor
ancestor
```

1. **Repo.** Clon existente en `/home/user/Modelado-Mexicano` — no se clonó
   ninguno nuevo. `git log -1` y `git status` arriba.
2. **SHA.** `main` no se movió: HEAD == `origin/main` == `4dca34c`, exacto
   contra lo que el encargo declara. No hubo que re-derivar nada.
3. **`data/raw`.** Ausente (`ls data/raw` → `No such file or directory`).
   No es PARO — este acto no la usa.
4. **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — valor
   correcto en nube (ADR-59 cláusula b). Sonda de microdato/red: saltada,
   como instruye el encargo.
5. **Espejo.** No se derivó ninguna cifra de espejo alguno — todo lo de
   este reporte sale del clon de (1), comando a la vista.

**Fecha.** `TZ=America/Mexico_City date` → `2026-08-04 19:54 CST`. El reloj
del entorno de nube marca 2026-08-05; el repo fecha por el huso de Mesa
(UTC-6, ADR-59 "Convención de fecha"), donde sigue siendo 4/ago — mismo
patrón de deriva que `forense/hallazgos.md:113` ya documentó para otro
acto. Este archivo y su línea en `hallazgos.md` llevan fecha `2026-08-04`.

### 0.1 · Concurrencia derivada

```
$ git branch -r
  origin/claude/adjudicar-r3-1-adr-60-4as2g0
  origin/main
  origin/sesion/hitoD-r3-1-encig
  origin/sesion/pb-descargas-f2
```

PRs abiertos contra `main` (`list_pull_requests`, GitHub MCP, `state=open`):

| # | Rama | Título | Base sha | Head sha |
|---|---|---|---|---|
| 104 | `sesion/hitoD-r3-1-encig` | "R3.1: corrida de falsación contra ENCIG 2023 -- propuesta B, no adjudicada" | `4dca34c` | `2828ec7` |
| 105 | `sesion/pb-descargas-f2` | "P-B: 4 descargas verificadas (ENDIREH FD+BD, ENDUTIH, MOCIBA); 26 restantes nombradas, no reconstruidas" | `4dca34c` | `047ebe8` |

Ambos siguen `state: open` — **ninguno de los dos está fusionado**. `W1-P`
(perímetro `tests/`, `forense/notas/(w1-p)`, `milpa/procedencia.yaml`,
`hallazgos.md`) no dejó rastro en `branch -r` ni en PRs abiertos al momento
de este reporte — no hay colisión de perímetro que declarar más allá de la
dependencia ya nombrada por el encargo.

## 1 · ADR máximo, receta T15

```
$ grep -hoE '^\*\*ADR-[0-9]+' canon/gobernanza-v*.md | grep -oE '[0-9]+' | sort -n -u | tail -5
55
56
57
58
59
```

Sin huecos (verificado con `awk` sobre la secuencia completa). ADR máximo
= **59**, exacto contra lo que el encargo declara — de proceder, ADR-60
sería el siguiente número derivado, no una constante. No se sella nada:
no hay premisa 2 que lo sostenga.

## 2 · Verificación de premisas (§2 del encargo)

| # | Premisa | Verificación |
|---|---|---|
| 1 | `main` reportado, ADR máximo = 59 | **Sostiene.** §0/§1 arriba |
| 2 | Nota 27 de `R3.1` está en `main`, con propuesta `B` | **NO sostiene.** Ver §3 abajo |
| 3 | `R3.1` sin veredicto archivado | **Sostiene** (verificado igual, por completitud) — ver §4 |
| 4 | Precedente `R3.2` = `B` archivado + tier `[FUERTE]` en `modelo` §7 | **Sostiene** — ver §4 |

Premisas 1, 3 y 4 sostienen. **Premisa 2 no sostiene** → PARO, por
instrucción explícita y verbatim del propio encargo ("Si no está, PARA: el
PR de `sesion/hitoD-r3-1-encig` no se fusionó y este acto no tiene sobre
qué adjudicar").

## 3 · Por qué la premisa 2 no sostiene

```
$ git grep -n "Nota 27" origin/main -- forense/
(sin resultados)
$ git show origin/main:forense/hitoD-preregistro-v2_0.md | grep -n "^### Nota" | tail -3
731:### Nota 14 · 4/ago/2026 — Ficha de `R3.1`, pre-registrada antes de consultar ninguna serie
878:### Nota 16 · ...
938:### Nota 21 · ...
950:### Nota 22 · ...
962:### Nota 23 · ...
970:### Nota 24 · ...
978:### Nota 25 · ...
986:### Nota 26 · 4/ago/2026 — Adenda de plantilla: fila E prospectiva y regla de precedencia (ADR-58)
```

La última Nota en `main` es la 26. No hay Nota 27 en `main` bajo ningún
nombre. `R3.1` en `main` sigue exactamente donde Encargo O la dejó (Nota
14): ficha pre-registrada, **"no tiene fila propia... este acto no
reordena, solo añade"**, sin corrida, sin propuesta, sin veredicto.

```
$ git fetch origin sesion/hitoD-r3-1-encig
$ git show origin/sesion/hitoD-r3-1-encig:forense/hitoD-preregistro-v2_0.md | grep -n "Nota 27"
998:### Nota 27 · 4/ago/2026 — `R3.1`, corrida completa sobre ENCIG 2023: propuesta `B`, no adjudicada
```

La Nota 27 existe **solo** en la rama sin fusionar del PR #104. Confirma,
letra por letra, la razón que el encargo mismo anticipó para este PARO.

## 4 · Premisas 3 y 4, verificadas por completitud

**Premisa 3.** El bloque `## Registro de veredictos archivados` de `main`
(`forense/hitoD-preregistro-v2_0.md:1002-1013`) trae 12 líneas / 11 fichas
(`R1.1`, `R3.2`, `R7.2`, `R4.2`, `R4.1`, `R9.1`, `R4.3`×2, `R9.2`, `R5.1`,
`R5.2`, `R1.2`) — exacto contra lo que el encargo declara ("11 fichas / 12
líneas"). `R3.1` no aparece. Sostiene.

**Premisa 4.** `forense/hitoD-preregistro-v2_0.md:1003`: `` `R3.2` →
veredicto `B` — *(archivado 29/jul/2026...)* ``. `canon/modelo-decision-v4_0.md:675`:
`` | `R3.2` | L233 | Digitalización/testigos/registrable → baja la mordida | `[FUERTE]` | Sí | ``.
`python3 tests/check.py --baseline` (completo en §6) marca `T12 conteos
del motor` en `[ ok ]`. El precedente que la cláusula (b) del ADR
proyectado necesitaría existe y está intacto. Sostiene.

Ninguna de las dos cambia el resultado: la premisa 2 basta sola para el
PARO, y es la que el encargo mismo señala como el gate.

## 5 · Sesión limpia

Esta sesión no abrió ENCIG, ningún cuestionario, ninguna serie de
microdato ni `milpa/procedencia.yaml`. Se leyó únicamente: el pre-registro
en `main` y en la rama del PR #104 (vía `git show`, sin checkout), el
registro de veredictos, `canon/modelo-decision-v4_0.md` (grep dirigido),
`canon/gobernanza-v1_15.md` (grep dirigido, receta T15), y la salida de
`tests/check.py --baseline`. Queda habilitada para pre-registrar contra
cualquier fuente.

## 6 · Suite, corrida al cierre (referencia — no hay adjudicación que verificar)

```
$ python3 tests/check.py --baseline
...
  [ ok ]  T12 conteos del motor
  [ ok ]  T15 T-ADR-COUNT
  [ ok ]  T18 T-PASO2-EJECUCION
...
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

Corrida sobre el estado real de `main`/rama, sin cambios de este acto —
sirve como punto de referencia limpio para cuando mesa fusione los dos PR
pendientes y M-1 se relance.

## 7 · Lista para mesa

1. **Fusionar PR #104** (`sesion/hitoD-r3-1-encig`) — trae la Nota 27 con
   la corrida y propuesta `B` que la premisa 2 exige.
2. **Fusionar PR #105** (`sesion/pb-descargas-f2`) — el encargo lo exige
   igual como condición de lanzamiento, aunque no toca el pre-registro de
   `R3.1`; no se investigó su contenido a fondo porque está fuera del
   perímetro de este acto y la premisa 2 ya basta para el PARO.
3. **Relanzar M-1** contra el nuevo `main` una vez fusionados ambos. Todo
   el trabajo de adjudicación (§3-§6 del encargo original: bloque
   append-only, ADR-60 con sus seis cláusulas, cascada de `de 27`/`de 49`,
   cierre de la deuda de ADR-58 en `gobernanza:358,683`) sigue pendiente,
   sin empezar.

## 8 · Perímetro

Se tocó únicamente esta nota y una línea de `forense/hallazgos.md`. No se
tocó `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`,
`canon/modelo-decision-v4_0.md`, `README.md`, ni el cuerpo o las Notas del
pre-registro (append-only o no) — no hay adjudicación que registrar en
ellos. No se tocó `milpa/`, `tests/` ni `data/`.
