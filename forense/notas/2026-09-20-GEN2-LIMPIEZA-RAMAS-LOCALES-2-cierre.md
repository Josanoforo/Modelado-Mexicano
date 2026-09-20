# ACTO GEN2-LIMPIEZA-RAMAS-LOCALES-2 — las 131 CON-TRABAJO-PROPIO: qué ya está en main, qué es medición sin rescatar, qué es historia

Encargo verbatim: `forense/encargos/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-2.md`. Solo lectura — nada se borró en disco. Tabla completa adjunta: `forense/notas/limpieza2_tabla.tsv` (131 filas).

**Compuerta.** `PR #910` (LIMPIEZA-RAMAS-LOCALES-1) fusionado (`mergedAt: 2026-09-20T04:53:21Z`, verificado por producto: `git cat-file -e origin/main:forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-1-cierre.md`). El primer intento de este acto (`PR #913`) paró aquí mismo por compuerta no cumplida — ver ese PR para el detalle; este documento es la continuación tras fusionarse `#910`.

## P0 · Punto de partida

Ambos bundles de `#910` siguen íntegros (`git bundle verify` → "records a complete history") y su `sha256` coincide con lo declarado. **Conteo de ramas corregido** (pedido por este mismo encargo): **306** es la cifra correcta (270 en `Modelado-Mexicano` + 36 en `mm-adq`, descontando la línea pseudo-rama de `HEAD` desprendido) — no 307 (contaba de más esa línea) ni 150 (sin derivación reconstruible, error simple de la nota de `#910`).

**Hallazgo de arranque no pedido por el encargo, pero necesario para que P1 signifique algo: `/home/pc0/Modelado-Mexicano` era un clon superficial (`git rev-parse --is-shallow-repository` → `true`, límite en `017ac24`/8-sep).** Antes de corregirlo, `git merge-base origin/main <rama>` fallaba con `no merge base` para **120 de las 131** ramas — no porque tuvieran historia disjunta, sino porque a la caja le faltaban 16 commits que resultan ser un punto de injerto crítico por el que pasa la ascendencia de docenas de ramas hacia `main`. Corregido con `git fetch --unshallow origin` (16 s, 5785→5801 commits). **Esto también significa que la propia clasificación FUSIONADA/CON-TRABAJO-PROPIO de `#910` pudo tener el mismo punto ciego** — pero las 141 `git branch -d` que `#910` sí ejecutó siguen siendo válidas (un clon superficial solo puede producir falsos negativos de ancestría, nunca falsos positivos: si `-d` aceptó borrar algo, esa rama era ancestro de verdad). Lo que sí cambia es que, de las 131 aquí analizadas, **17 resultan ser ancestros puros de `origin/main` hoy** (`git merge-base --is-ancestor` con historia completa) — `git branch -d` las aceptaría ahora mismo, algo invisible para `#910`. Ver [[feedback_sandbox_enmascara_git_config_en_worktree_add]] y el nuevo hallazgo de clon superficial en `hallazgos.md`.

## P1–P2 · Metodología y cubetas

Por rama: `git cherry origin/main <rama>` (equivalencia de parche) + comparación directa de árbol (`git ls-tree -r` rama vs. `origin/main`, no el diff de tres puntos) para "archivos que main no tiene" — el diff de tres puntos se descartó como señal primaria tras descubrir que dos ramas (`acto/gen2-enaproce-instrumentos-acceso-1`, `acto/gen2-sin-candidato-rutas-1`) tienen **múltiples bases de fusión** (topología criss-cross con `origin/main`) que hacen que `git diff --stat origin/main...rama` liste archivos como "propios" que en realidad **ya existen en `main`** por otra ruta — verificado con `git cat-file -e` directo. La comparación de árbol, sin ambigüedad de base, es la que manda.

**Resultado, 131 ramas → 4 cubetas:**

| cubeta | n |
|---|---:|
| CONTENIDO-EN-MAIN | 102 |
| HISTORIA-GEN1 | 22 |
| REVISAR-A-MANO | 5 |
| MEDICION-SIN-RESCATAR | 2 |

**La hipótesis del encargo sobre `sesion/` — verificada, no supuesta, y refinada.** Hay **68** ramas `sesion/` (no 53). De ellas, **65 verifican como CONTENIDO-EN-MAIN** (prueba más fuerte: equivalencia de contenido directa contra `main`, no solo edad) y solo **3** (`sesion/cruce-catalogo-fichas`, `sesion/indice2-1786050152`, `sesion/p-lapop-microdato`) caen en HISTORIA-GEN1 propiamente. El destino de firma es el mismo para ambas cubetas (P5), pero la razón verificada es más específica que la supuesta: no es que sean viejas y no midan GEN2, es que su contenido literalmente ya está en `main`.

**Tres excepciones EN-VUELO dentro de CONTENIDO-EN-MAIN, por la regla de 24 h (no de `#910`, de este mismo acto sucesor):** `acto/gen2-c2-compuesto-ic-enif2024-1`, `acto/gen2-c2-compuesto-ic-envipe2025-1` y `acto/gen2-pisos-enut2019-ejes-1` ya no están en `origin` (sus PR se fusionaron y GitHub borró la rama remota — `#911`, `#907`→cerrado por `PARO-PREMISA`, `#908` respectivamente) pero su último commit tiene **2.1–2.4 horas** — protegidas por la misma regla de 24 h que `#910` aplicó a otras 26. Mañana, sin acto nuevo, son borrables.

## P3 · Los tres bultos grandes

- **`acto/gen2-e5-calc-0001-0003`** — los "2 112 commits propios" que citaba `#910` eran artefacto puro del clon superficial (ver P0): con historia completa, es **ancestro puro de `origin/main`** (`cherry` 0/0, diff vacío). Su propio commit de tip ya lo decía: `[A.14 + CONSUMIDO · GEN2-E5] NO-CORRIDO / RESERVAS y cierre por PR #631` — cerró correctamente hace tiempo, solo nunca se limpió la rama local. **CONTENIDO-EN-MAIN.**
- **`marco-produccion-total`** — mismo artefacto (los "931 commits propios" eran del clon superficial); el contenido **commiteado** es ancestro puro de `main` (CONTENIDO-EN-MAIN). Pero el **worktree** sigue sucio (`?? .barrido2/`, sin commitear) — la rama es segura de borrar, el directorio físico no, hasta que alguien revise ese scratch.
- **`preservado/r3-1-merge-verificado-no-empujado`** — el nombre es autoexplicativo y se verificó, no se supuso: es un snapshot local de `Merge remote-tracking branch 'origin/sesion/hitoD-r3-1-encig'` (4/ago/2026), la rama que llevó la adjudicación de la ficha **R3.1** (Hito D, "canal de confianza personal → adopción fintech") a `origin/main` vía **PR #104** el mismo día (`hallazgos.md`, entradas del 4/ago que documentan la adjudicación, sellada en `ADR-60` vía `PR #106`). Este merge local se hizo para **verificar** que ese merge funcionaría limpio antes de que el PR real se fusionara en GitHub — y nunca hizo falta empujarlo porque la integración real ocurrió directo. Confirmado ahora: 245 de 249 commits con equivalente ya en `main`, solo 1 archivo trivial exclusivo. El propósito que el nombre declara se cumplió hace 47 días. **CONTENIDO-EN-MAIN.**

## P4 · Worktrees sucios (17 de `#910`, estado re-verificado hoy) y el conflicto MOTRAL

Dos de los 17 ya no están sucios (su contenido se fusionó a `main` mientras tanto y llegó también a estos worktrees vía fetch/merge): `acto/gen2-c2-compuesto-ic-enif2024-1` y `acto/gen2-pisos-enut2019-ejes-1` (0 cambios ahora). El scratch de `/tmp/modelado-deriva-2026-09-19-ITp8sW` también se limpió solo. Estado actual de los que siguen sucios:

| rama/worktree | archivos sucios | zona |
|---|---:|---|
| `claude/tramite-2026-09-17` (clon base) | 1 | `error.log` |
| `acto/gen2-f5-recaptura-l` | 1 | `data/` |
| `acto/gen2-reparacion-cierre-consolidacion-cron` | 1 | `data/` |
| `codex/autoridad-semantica-enif` | 5 | `data/`, `tools/` |
| `codex/autoridad-semantica-marco-cobertura-total` | 1 | `.barrido2` |
| `codex/gen2-encuci2020-respuesta-por-contacto-cli-2` | 1 | `forense/` |
| `codex/gen2-issp2017-consistencia-apoyo-familiar-cli-2` | 1 | `forense/` |
| `codex/gen2-motral2015-prioridades-prestaciones-cli-1` | 1 | `data/` (ver abajo) |
| `llave2-decreto` | 1 | `scratchpad/` |
| `marco-produccion-total` | 1 | `.barrido2` |
| `worktree-agent-{a336d401,a7d8e527,a9facc03}` (×3, Claude Code) | 1 c/u | `forense/` |
| `mm-adq` (clon del runner) | 2 | staging + cron |

**El conflicto MOTRAL, identificado por hash de blob, no resuelto:** `data/corrida0/CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001/medidor.py` está en `AA` con marcadores de conflicto literales en el archivo. **No es un conflicto contra `origin/main`** (que ni siquiera tiene este CALC-id — `ls-tree origin/main:data/corrida0/` solo lista `CALC-MOTRAL2015-VALORACION-SS-0001`, confirmando textualmente lo que el encargo ya sospechaba). Es un conflicto **dentro de la misma rama**, entre dos de sus propios commits: el reflog muestra `rebase (start): checkout origin/main` seguido de `rebase (abort): returning to refs/heads/codex/gen2-motral2015-prioridades-prestaciones-cli-1` — un intento de rebasar esta rama sobre `origin/main`, abortado, que dejó el índice sin limpiar. Verificado por hash de blob exacto: el lado `HEAD`/`ours` (stage 2, `cdac79b3`) es **el tip real y actual de la rama** (`914e92f3`, *"RESULT MOTRAL2015 prioridades corregido"*, 19/sep 18:01:33); el lado `7a64858`/`theirs` (stage 3, `bb089b4`) es **un commit anterior de la misma rama** (`7a648587`, *"SPEC MOTRAL2015 prioridades prestaciones congelada"*, 19/sep 18:00:18 — 75 segundos antes). La rama committeada está intacta; el defecto vive solo en el árbol de trabajo de este worktree, residuo de un abort incompleto. No se tocó.

## P5 · Propuesta de firma para mesa (texto listo, no ejecutado)

**CONTENIDO-EN-MAIN (102) + HISTORIA-GEN1 (22) = 124 ramas: se borran con `-D`; el bundle `34c39bfa6cc1f263625eafdf37d43a4b95e919f267464e65d4629ba2dab48cb7` (`/home/pc0/respaldo-ramas-2026-09-20-Modelado-Mexicano.bundle`, `sesion/inv-seg` y las demás `Modelado-Mexicano`) o `0e38bdcafcfb04802dfc27880df5a5b267a9674a174e81301db8bff0d1d95284` (`mm-adq`, según clon) las conserva.** Excepción temporal: 3 de las 102 (`acto/gen2-c2-compuesto-ic-enif2024-1`, `-envipe2025-1`, `acto/gen2-pisos-enut2019-ejes-1`) esperan a pasar las 24 h. Excepción de worktree: `marco-produccion-total` necesita que alguien revise `.barrido2/` antes de retirar el worktree (la rama en sí es segura). Lista completa en el TSV adjunto, columna `cubeta`.

**MEDICION-SIN-RESCATAR (2): no se borran; pasan a un acto de rescate, una por una.**
- `codex/gen2-marcador-adopcion-cli-1` — **corrige el veredicto de `#910`** (que decía "BORRABLE-TRAS-FIRMA" mirando solo el diff del marcador ya archivado): esta rama también trae `data/corrida0/CALC-PISOS-ENIF2021-EJES-0002/` sellado el 19/sep ("Mide piso corregido de ENIF 2021"), ausente de `main`, sin colisión de id. Rescatable.
- `codex/gen2-motral2015-prioridades-prestaciones-cli-1` — `data/corrida0/CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001/` sellado, ausente de `main` (que solo tiene `VALORACION-SS`, confirmado arriba), sin colisión de id. El conflicto de P4 vive en el worktree, no en la rama — un acto de rescate puede leer el commit `914e92f3` directamente sin pasar por el worktree sucio.

**REVISAR-A-MANO (5), lista corta para dirección:**
- `codex/gen2-recibo-codex-3` — 2 commits, `[GEN2-RECIBO-CODEX-3] integra ENADID y cierre final`; ya confirmado en `#910` como trabajo de cierre legítimo sin fusionar.
- `codex/optimiza-verificacion-ci-prueba-compuerta` — 1 commit, literalmente `test temporal: fallos y omisiones para comprobar compuerta CI`; sin worktree (ya limpiado).
- `mm-adq: adq/2026-09-15-nc-0202`, `adq/2026-09-16-gen2-38-investigacion`, `censo/2026-09-16` — 1, 1 y 4 commits respectivamente, sin worktree, contenido de investigación ADQ que no llegó a fusionarse por la vía normal; ninguno trae un CALC sellado.

## Cierre

### ## NO-CORRIDO / RESERVAS
Ninguno.

### ## CONSUMIDO
Este PR (`#913`, continuado tras el PARO inicial).

### Estado final (crudo)
```
$ git -C /home/pc0/Modelado-Mexicano rev-parse --is-shallow-repository
false
$ python3 -c "import json; d=json.load(open('limpieza2_resultados.json'));
  from collections import Counter; print(Counter(r['cubeta'] for r in d))"
Counter({'CONTENIDO-EN-MAIN': 102, 'HISTORIA-GEN1': 22, 'REVISAR-A-MANO': 5, 'MEDICION-SIN-RESCATAR': 2})
```
