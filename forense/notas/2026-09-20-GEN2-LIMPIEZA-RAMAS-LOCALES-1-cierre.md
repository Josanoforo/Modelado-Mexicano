# ACTO GEN2-LIMPIEZA-RAMAS-LOCALES-1 — inventario y limpieza de ramas, worktrees y restos en la caja

Encargo verbatim: `forense/encargos/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-1.md`. CABECERA: SHA de redacción `a92126f0`; compuerta: ninguna; MODELO: Sonnet, receta sin juicio. Ejecutado en una sola sesión, en la caja (WSL2, `/home/pc0`), no en nube.

## 0 · Gate de arranque

```
$ git worktree list          (desde /home/pc0/Modelado-Mexicano)
→ 159 entradas, decenas de worktrees /home/pc0/mm-*
$ ls data/raw | head -1      (desde /home/pc0/Modelado-Mexicano)
→ symlink real a /home/pc0/mm-corpus/raw, no vacío
```
Múltiples worktrees preexistentes + corpus montado ⇒ **CAJA confirmada, no nube**. (`/home/pc0` en sí no es un repo git — ver P0.)

## P0 · Cuántos clones hay

`find /home/pc0 -maxdepth 5 -type d -name .git` examinó **5** directorios:

| directorio | origin | veredicto |
|---|---|---|
| `/home/pc0/Modelado-Mexicano/.git` | `Josanoforo/Modelado-Mexicano` | **CASA** |
| `/home/pc0/mm-adq/.git` | `Josanoforo/Modelado-Mexicano` | **CASA** (clon separado del runner ADQ, no un worktree enlazado — confirmado por `.git` como directorio real, no archivo) |
| `/home/pc0/.codex/.tmp/plugins/.git` | sin remote `origin` | excluido — caché de plugins de Codex CLI, ajeno al proyecto |
| `/home/pc0/.codex-app/.tmp/plugins/.git` | sin remote `origin` | excluido — ídem |
| `/home/pc0/.git` | git lo rechaza como repo (`fatal: not a git repository`, incluso con `-C` directo) | excluido — **no es un repo**: `ls -la` muestra `config`, `config.lock`, `hooks` como nodos de dispositivo `crw-rw-rw- nobody nogroup 1,3` (montajes `/dev/null` del sandbox, mismo defecto que `feedback_cd_subdir_crea_claude_dir`), sin `HEAD`/`objects`/`refs`. El único contenido real es `info/exclude`, que lista rutas de infraestructura propia de Claude Code (`**/.claude/scheduled_tasks.json`, `**/.claude/worktrees/`, `**/.claude/routines/.state/`, etc.) — es infraestructura del propio cliente, materializada cuando un comando corre con `cwd=/home/pc0`, no un clon del proyecto. Directorio con `Birth: 17/ago`, mounts de hoy: acumula sesión tras sesión. |

**2 de 5 casaron.** Todo lo que sigue opera sobre esos dos clones.

## P1 · Inventario

Comandos por clon (`git fetch --prune origin`, `python3 tools/limpia_arbol.py --reporta --json`, `git worktree list --porcelain`, `git branch -vv`, `git stash list`, `git status --porcelain` por worktree). Salida cruda de `branch -vv` (270 líneas Modelado-Mexicano + 37 mm-adq) y los dos JSON de `limpia_arbol` se generaron y consultaron en la sesión; se resumen aquí para no duplicar ~700 líneas.

**Fetch inicial** (`Modelado-Mexicano`): 4 ramas `claude/*` avanzaron + `main` `a92126f0→7a2d77f4`. **Fetch inicial** (`mm-adq`, más desactualizado): podó **11** refs remotos ya borrados en GitHub (`acto/gen2-adq-handoff-resultado-y-salud-1`, `adq/2026-09-{17,18,19}`, `censo/2026-09-{17,18,19}`, `claude/tramite-2026-09-17`, `derivados/2026-09-{17,18,19}`) — evidencia directa del incidente que motiva Gate D-14 («mesa borró ramas en GitHub que siguen vivas en local»): la primera (`acto/gen2-adq-handoff-resultado-y-salud-1`) sigue viva localmente con worktree.

**`origin/main` se movió varias veces durante el acto** (consistente con sesiones concurrentes activas, ver más abajo): `a92126f0 → 7a2d77f4 (PR #906, claude/gen2-tablero-senal-1-cierre) → b7d9b8b4 (PR #906 vía otra ruta) → a51f4da (PR #907, acto/gen2-c2-compuesto-ic-envipe2025-1)`. El worktree de esta nota se creó sobre `a51f4da`, la más fresca al momento de escribir.

**EN-VUELO re-derivado** (`git ls-remote --heads origin`, no la lista pegada del encargo): al abrir, 8 ramas no-`main`: las 7 del encargo **más** `claude/gen2-tablero-senal-1-cierre` (nueva, al mismo SHA que `origin/main` en ese momento — se fusionó vía PR #906 durante el acto y ya no aparece en un `ls-remote` posterior). Ninguna de las 8 tiene copia local en ningún clon salvo `acto/gen2-c2-compuesto-ic-enif2024-1`, `acto/gen2-c2-compuesto-ic-envipe2025-1` y `acto/gen2-pisos-enut2019-ejes-1` (las tres con worktree y con commits propios locales que divergen del tip de origin — ver P5/P6). **`git remote prune origin` al final de P4 podó `origin/acto/gen2-c2-compuesto-ic-envipe2025-1`**: esa rama, EN-VUELO al abrir, dejó de existir en GitHub *durante* la sesión (consistente con una sesión concurrente que escribió en `MEMORY.md` del operador citando `PR #907`/`PARO-PREMISA` sobre este mismo rótulo mientras este acto corría). Su copia local **no se tocó ni se reclasificó** — la clasificación de este acto es la del momento en que se hizo, y ese cambio de estado se deja para que mesa lo revise con el árbol más fresco, no para que este acto lo absorba a mitad de camino.

**Stash:** `Modelado-Mexicano` 1 (`On acto/gen2-reactivos-residuales-busqueda-util: preexistente-gen2-39-antes-0bis`); `mm-adq` 7 (fechados 4/sep–15/sep, incluyendo dos `preservado-antes-despliegue-*` y uno `WIP on fix/cron-censo-rama`). Ninguno se tocó (prohibido `stash drop/clear` por REGLA DE ORO).

**`limpia_arbol.py --reporta --json`:** `Modelado-Mexicano` — base 355 commits detrás de `origin/main` (el clon está parado en `claude/tramite-2026-09-17`, no en `main` — confirmado, nunca asumir lo contrario), 142 `ramas_fusionadas_vivas`, 159 worktrees, `fuera_de_politica` (D, sin PR abierto) = 4. `mm-adq` — base 4 detrás, 32 `ramas_fusionadas_vivas`, 13 worktrees.

**Tabla completa por rama** (clon · rama · carril · commits propios · en origin · worktree · sucio): generada mecánicamente para las 306 ramas locales (`git for-each-ref` + `git branch --merged origin/main` + `git rev-list --count --no-merges` + `git status --porcelain` por worktree). Se reproduce completa donde importa a una decisión — P4 (borradas), P5 (con trabajo propio) y la tabla de sucias — no las 142 filas ya limpias y ya procesadas, que están en el bundle y en el log de P4.

## P2 · Clasificación mecánica — conteos

De 306 ramas locales (270 + 36; `mm-adq` en `HEAD` desprendido no cuenta como rama):

| categoría | n | regla |
|---|---:|---|
| **FUSIONADA**, procesada en P4 | 142 | `git branch --merged origin/main` la lista, no EN-VUELO, commit ≥ 24 h, worktree limpio |
| excluida de FUSIONADA por **EN-VUELO local** | 1 | `main` de `mm-adq` — protegida por rótulo aunque el chequeo mecánico la marcara fusionada (ver nota) |
| excluida de FUSIONADA por **< 24 h** | 26 | fusionada mecánicamente pero con commit de hoy — ver tabla abajo |
| **WORKTREE-SUCIO** | 15 (+2 en `HEAD` desprendido) | cambios sin commitear o archivos sin seguimiento |
| **CON-TRABAJO-PROPIO** | 131 | ≥ 1 commit propio, o no ancestro de `origin/main` |

**Nota sobre la guardia de `main`:** `git branch --merged origin/main` sí lista el `main` local de `mm-adq` (`a37837a0`, 1400 detrás, 0 delante — un ancestro puro, técnicamente "fusionado"). Este acto lo excluye de todas formas por regla propia, nunca por rótulo: borrar automáticamente algo llamado `main` es el tipo de acción que se lista para firma aunque el mecanismo diga que es segura.

**Las 26 excluidas por <24h** (fusionadas, pero con commit de las últimas 24 h — la mayoría son cierres de Codex de las últimas horas, más 2 del cron ADQ de hoy):

`codex/gen2-adq-registro-cierre-cli-2` (3.2h) · `codex/gen2-contrato-y-tramite-cli-1` (9.7h) · `codex/gen2-cron-verificacion-operativa-cli-1` (4.2h) · `codex/gen2-eder2017-primera-union-sexo-cohorte-cli-1` (1.5h) · `codex/gen2-enadid-union-actual-cli-1` (6.8h) · `codex/gen2-enadid2023-union-sexo-edad-cli-2` (1.1h — ver P5, premisa del encargo corregida) · `codex/gen2-encig-cruces-historicos-cli-1` (4.1h) · `codex/gen2-encuci2020-exposicion-respuesta-cli-1` (4.5h) · `codex/gen2-encuci2020-respuesta-por-contacto-cli-2` (1.5h) · `codex/gen2-enfih2019-cobertura-saldos-catpos-cli-2` (1.3h) · `codex/gen2-enfih2019-saldos-afore-cli-1` (4.6h) · `codex/gen2-enigh2022-perfil-estructural-cli-1` (4.6h) · `codex/gen2-enigh2022-remesas-contexto-cli-2` (3.4h) · `codex/gen2-ensafi2023-estrategias-conjuntas-cli-1` (2.0h) · `codex/gen2-enut2024-distribucion-horas-cli-2` (2.4h) · `codex/gen2-enut2024-participacion-intensidad-cli-1` (4.3h) · `codex/gen2-issp-apoyo-monetario-cli-1` (6.6h) · `codex/gen2-issp2017-consistencia-apoyo-familiar-cli-2` (3.0h) · `codex/gen2-issp2017-redes-apoyo-cotidiano-cli-1` (4.4h) · `codex/gen2-motral2015-prioridades-prestaciones-cli-1-sync` (2.1h) · `codex/gen2-pisos-rejilla-cli-1` (6.9h) · `codex/gen2-replay-y-pisos-cli-1` (10.0h) · `codex/gen2-wbes2023-precision-interacciones-cli-2` (2.0h — ver P7, además tiene el hallazgo anti-PR#77) · `codex/optimiza-verificacion-ci` (0.9h) · `mm-adq: adq/2026-09-19` (4.9h) · `mm-adq: censo/2026-09-19` (4.8h).

Ninguna de estas 26 se tocó. Vuelven a ser candidatas mecánicas mañana, cuando su commit pase de 24 h — no hace falta un acto nuevo, solo repetir P1–P4.

## P3 · Respaldo (antes de borrar nada)

```
$ git -C /home/pc0/Modelado-Mexicano bundle create /home/pc0/respaldo-ramas-2026-09-20-Modelado-Mexicano.bundle --all
$ git -C /home/pc0/Modelado-Mexicano bundle verify   /home/pc0/respaldo-ramas-2026-09-20-Modelado-Mexicano.bundle
→ The bundle contains these 440 refs ... The bundle records a complete history.
$ sha256sum /home/pc0/respaldo-ramas-2026-09-20-Modelado-Mexicano.bundle
→ 34c39bfa6cc1f263625eafdf37d43a4b95e919f267464e65d4629ba2dab48cb7  (62 763 495 bytes)

$ git -C /home/pc0/mm-adq bundle create /home/pc0/respaldo-ramas-2026-09-20-mm-adq.bundle --all
$ git -C /home/pc0/mm-adq bundle verify   /home/pc0/respaldo-ramas-2026-09-20-mm-adq.bundle
→ The bundle contains these 58 refs ... The bundle records a complete history.
$ sha256sum /home/pc0/respaldo-ramas-2026-09-20-mm-adq.bundle
→ 0e38bdcafcfb04802dfc27880df5a5b267a9674a174e81301db8bff0d1d95284  (64 038 950 bytes)
```

Ambos `verify` dieron **"records a complete history"** — gate pasado, ambos bundles viven en `/home/pc0/` (fuera de los dos repos). Si `verify` hubiera fallado, el acto paraba aquí sin tocar nada; no fue el caso.

## P4 · Limpieza ejecutada

Para las 142 FUSIONADA-limpias-no-EN-VUELO-no-recientes: `git worktree remove <ruta>` (sin `--force`) donde había worktree, luego `git branch -d <rama>` (minúscula) en todos los casos. Resultado: **141 borradas, 1 rechazada por git** (mensaje pegado crudo abajo, no se insistió). Tabla completa (142 filas, clon · rama · worktree retirado · rama borrada) — ver arriba, generada del log de ejecución.

**La rechazada — `acto/gen2-celda-d-piloto-2` (Modelado-Mexicano):**
```
$ git -C /home/pc0/Modelado-Mexicano worktree remove /home/pc0/mm-gen2-celda-d-piloto-2
  (exit 0 — el worktree SÍ se retiró)
$ git -C /home/pc0/Modelado-Mexicano branch -d acto/gen2-celda-d-piloto-2
error: the branch 'acto/gen2-celda-d-piloto-2' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D acto/gen2-celda-d-piloto-2'
hint: Disable this message with "git config set advice.forceDeleteBranch false"
```
**Causa verificada, no supuesta:** `git branch -d` (sin argumento explícito) compara contra el `HEAD` actual del clon, no contra `origin/main`. El clon base está parado en `claude/tramite-2026-09-17` (no en `main`) — y el contenido de `acto/gen2-celda-d-piloto-2` (`8ba4474`, fusionado en PR #858) **sí** es ancestro de `origin/main` (`git branch --merged origin/main` la listó) pero **no** es ancestro de `claude/tramite-2026-09-17` específicamente. Es exactamente el defecto de premisa que el propio P2 del encargo no anticipó (asume que "listada por `--merged origin/main`" y "`branch -d` la acepta" son equivalentes; lo son solo si el `HEAD` del clon está sobre `main`). Por REGLA DE ORO no se insistió con `-D`. Estado final: worktree retirado, rama local viva sin worktree, `8ba4474`, en el bundle. **Para mesa:** un `git checkout main && git branch -d acto/gen2-celda-d-piloto-2` (o confirmar y usar `-D`) la termina de limpiar; no se hizo aquí porque cambiar el `HEAD` del clon base no está en el perímetro de este acto.

**`git worktree prune` y `git remote prune origin`** (ambos clones, paso final obligatorio): además de finalizar el registro administrativo de las 141 recién retiradas, `prune` en `Modelado-Mexicano` limpió **~120 entradas administrativas** con nombres que **no aparecen en ningún inventario de esta sesión** (`mm-main-5973`, `gen2-reval-805`, `gen2-pr-clean`, `gen2-main-baseline`, `mm-relevo-remesas-f3-baseline[-final]`, entre otras) — residuo de worktrees retirados alguna vez con `rm -rf` en vez de `git worktree remove`, en sesiones anteriores a ésta, nunca podados hasta ahora. No corresponden a ninguna rama vigente (`prune` solo limpia metadatos de worktree, nunca ramas) y no requieren acción adicional. `git remote prune origin` podó 1 ref en cada clon: `origin/acto/gen2-c2-compuesto-ic-envipe2025-1` (ver P1, churn de la sesión).

**Estado final de conteos** (antes → después):
- `Modelado-Mexicano`: 270 → 159 ramas locales; 159 → 51 worktrees.
- `mm-adq`: 37 → 7 ramas locales (incluye el `HEAD` desprendido); 13 → 1 worktree (solo el propio clon).
- Integridad del clon base verificada tras la limpieza: sigue en `claude/tramite-2026-09-17`, `git status --porcelain` solo muestra `?? error.log` (preexistente, ver P6) — **la limpieza no tocó nada fuera de las 142 ramas de la lista**.

## P5 · Lo que NO se borró, para que mesa decida

### Los cuatro casos que dirección ya conocía

**`codex/gen2-marcador-adopcion-cli-1` — verificado, coincide.** Tip local `2d662e78b143f9b00a8e2b06fb7ff6cfe0ea15a1`. El diff archivado en `origin/main:forense/notas/insumos-externos/marcador/codex-03-2d662e7.diff` existe (no en el checkout del clon base, que no está en `main` — se leyó con `git show origin/main:<ruta>`) y su `sha256` declarado (`16f477c2...c62212f`) coincide byte a byte con el `sha256` recalculado del contenido archivado. El tip **no avanzó** más allá de lo archivado. 14 commits propios, borrada de GitHub. **Veredicto: BORRABLE-TRAS-FIRMA**, exactamente como anticipaba el encargo.

**`codex/gen2-enadid2023-union-sexo-edad-cli-2` — premisa del encargo NO sostenida contra el árbol actual.** El encargo la describe como "nunca fusionada... es medición real... RESCATAR". Verificación directa: `git merge-base --is-ancestor codex/gen2-enadid2023-union-sexo-edad-cli-2 origin/main` → **exit 0**; `git rev-list --count origin/main..codex/gen2-enadid2023-union-sexo-edad-cli-2` → **0**. El historial de la rama muestra sus propios commits de trabajo (`GEN2 ENADID: congela unión por sexo y edad`, `publica unión por sexo y edad`, `publica conteos estándar corregidos`, cuatro más) intercalados con merges de sincronización de `origin/main` — el trabajo **ya se integró a main por la vía normal** en algún punto entre que el encargo se redactó (SHA `a92126f0`) y ahora. No necesita rescate: ya está a salvo en `origin/main`, y además el bundle contiene su tip (`05cead807e28d68f4c13783678e95317809fcc68`) de cualquier forma. Se excluyó de P4 solo por la regla de 24 h (su commit más reciente, un merge de sincronización rutinario, tiene 1.1 h) — mañana, sin este comentario, un `git branch -d` normal la aceptaría. **Veredicto: la premisa cambió; no se necesita ninguna acción especial, solo esperar 24 h y dejar que la regla mecánica la procese.**

**`codex/gen2-recibo-codex-3` y `codex/optimiza-verificacion-ci-prueba-compuerta` — confirmados, ninguno fusionado.** El primero: 2 commits propios, asunto `[GEN2-RECIBO-CODEX-3] integra ENADID y cierre final`, worktree limpio, `/home/pc0/mm-gen2-recibo-codex-3`. El segundo: 1 commit propio, asunto literal `test temporal: fallos y omisiones para comprobar compuerta CI` (confirma la propia descripción del encargo), worktree ya inexistente en disco (`prunable`, limpiado por el `git worktree prune` de P4 — solo queda la rama). **Veredicto: CON-TRABAJO-PROPIO menor, sin urgencia; ninguno tiene worktree con datos en riesgo.**

**`…-base-medicion` — NO-ENCONTRADO, con control positivo.** `git branch -a` en ambos clones, sin coincidencia para `base-medicion` ni variantes de `optimiza-verificacion-ci*` fuera de las dos ya conocidas; control positivo (`gen2-recibo-codex-3`, 1 coincidencia) confirma que el barrido sí examinó las ramas. O ya se limpió antes de este acto, o el nombre corto se refería a una rama que nunca llegó a esta caja.

### Infraestructura propia de Claude Code, no ramas de un acto

Tres worktrees `worktree-agent-<hash>` viven anidados en `/home/pc0/Modelado-Mexicano/.claude/worktrees/agent-*` — no en el patrón `~/mm-<slug>` de los actos. Los tres apuntan al mismo commit (`0cdbd72`, merge de PR #789, ya viejo respecto a `origin/main` actual) y los tres tienen el **mismo** directorio sin seguimiento: `forense/prereg-caja/validacion-independiente-scratch/` — consistente con tres sub-agentes forkeados con `isolation: worktree` para la misma tarea de validación independiente (`acto/gen2-validacion-independiente-2` o `-parametros-activos`), cada uno escribiendo el mismo scratch relativo en su copia aislada. `0cdbd72` **sí** es ancestro de `origin/main` (fusionado), pero el directorio sin seguimiento los deja fuera de P4 por la regla WORKTREE-SUCIO. El propio `/home/pc0/.git` de P0 (infraestructura de Claude Code, no de este repo) confirma que `.claude/worktrees/` es una ruta que el cliente gestiona por su cuenta. **Recomendación: BORRABLE-TRAS-FIRMA** — el contenido es scratch de validación (no un CALC sellado), pero es mesa quien decide si el scratch tiene valor antes de que un acto futuro lo retire.

### Tabla — WORKTREE-SUCIO (17: 15 con rama + 2 en `HEAD` desprendido)

| clon | rama | fusionada(origin/main) | en origin | ruta worktree |
|---|---|---|---|---|
| Modelado-Mexicano | acto/gen2-c2-compuesto-ic-enif2024-1 | NO | sí | /home/pc0/mm-gen2-c2-compuesto-ic-enif2024-1 |
| Modelado-Mexicano | acto/gen2-f5-recaptura-l | sí | NO | /home/pc0/mm-gen2-f5-recaptura-l |
| Modelado-Mexicano | acto/gen2-pisos-enut2019-ejes-1 | NO | sí | /home/pc0/mm-gen2-pisos-enut2019-ejes-1 |
| Modelado-Mexicano | acto/gen2-reparacion-cierre-consolidacion-cron | sí | NO | /home/pc0/mm-gen2-reparacion-cierre-cron |
| Modelado-Mexicano | claude/tramite-2026-09-17 | sí | NO | /home/pc0/Modelado-Mexicano (clon base) |
| Modelado-Mexicano | codex/autoridad-semantica-enif | NO | NO | /home/pc0/mm-autoridad-semantica-enif |
| Modelado-Mexicano | codex/autoridad-semantica-marco-cobertura-total | NO | NO | /home/pc0/mm-autoridad-semantica-marco-produccion |
| Modelado-Mexicano | codex/gen2-encuci2020-respuesta-por-contacto-cli-2 | sí | NO | /home/pc0/mm-gen2-encuci2020-respuesta-por-contacto-cli-2 |
| Modelado-Mexicano | codex/gen2-issp2017-consistencia-apoyo-familiar-cli-2 | sí | NO | /home/pc0/mm-gen2-issp2017-consistencia-apoyo-familiar-cli-2 |
| Modelado-Mexicano | codex/gen2-motral2015-prioridades-prestaciones-cli-1 | NO | NO | /home/pc0/mm-gen2-motral2015-prioridades-prestaciones-cli-1 (merge conflict sin resolver, ver P6) |
| Modelado-Mexicano | llave2-decreto | NO | NO | /home/pc0/mm-llave2-decreto |
| Modelado-Mexicano | marco-produccion-total | NO | NO | /home/pc0/mm-marco-produccion-total |
| Modelado-Mexicano | worktree-agent-a336d4013203d5b8e | sí | NO | .claude/worktrees/agent-a336d4013203d5b8e |
| Modelado-Mexicano | worktree-agent-a7d8e527ae88b7feb | sí | NO | .claude/worktrees/agent-a7d8e527ae88b7feb |
| Modelado-Mexicano | worktree-agent-a9facc03b479266d6 | sí | NO | .claude/worktrees/agent-a9facc03b479266d6 |
| mm-adq | *(HEAD desprendido, `a92126f0`)* | n/a | n/a | /home/pc0/mm-adq (clon del runner ADQ, ver P6) |
| mm-adq | *(HEAD desprendido, `a92126f0`)* | n/a | n/a | /tmp/modelado-deriva-2026-09-19-ITp8sW (scratch activo de hoy, ver P6) |

### Tabla — CON-TRABAJO-PROPIO (131 ramas)

Columnas: clon · rama · carril · commits propios · en origin · worktree · sucio · asunto.

| clon | rama | carril | commits propios | en origin | worktree | sucio | asunto |
|---|---|---|---:|---|---|---|---|
| Modelado-Mexicano | acto/gen2-c2-compuesto-ic-enif2024-1 | acto | 1 | sí | sí | SUCIO | [GEN2-C2-COMPUESTO-IC-ENIF2024-1] 0-bis A.3: encargo verbati |
| Modelado-Mexicano | acto/gen2-c2-compuesto-ic-envipe2025-1 | acto | 3 | sí | sí | limpio | GEN2-C2-COMPUESTO-IC-ENVIPE2025-1: NO-CORRIDO / RESERVAS + C |
| Modelado-Mexicano | acto/gen2-e4-limpieza-c2-poda | acto | 1965 | NO | sí | limpio | fix(nota): cita raices.local.yaml con ruta, no basename (T03 |
| Modelado-Mexicano | acto/gen2-e5-0-specs-ejecutables | acto | 2104 | NO | sí | limpio | Reconciliacion de contadores 408->409 que quedo fuera del co |
| Modelado-Mexicano | acto/gen2-e5-1-verificador-calc0003v2 | acto | 2126 | NO | sí | limpio | [RENUMERADO · GEN2-E5-1] ADR-411 -> ADR-412: GEN2-TRAMITE-TA |
| Modelado-Mexicano | acto/gen2-e5-calc-0001-0003 | acto | 2112 | NO | sí | limpio | [A.14 + CONSUMIDO · GEN2-E5] NO-CORRIDO / RESERVAS y cierre  |
| Modelado-Mexicano | acto/gen2-e7-readiness2-c | acto | 2010 | NO | sí | limpio | ## CONSUMIDO: pieza C ejecutada via PR #612 |
| Modelado-Mexicano | acto/gen2-enaproce-instrumentos-acceso-1 | acto | 0 | NO | sí | limpio | Merge remote-tracking branch 'origin/main' into acto/gen2-en |
| Modelado-Mexicano | acto/gen2-pisos-enut2019-ejes-1 | acto | 2 | sí | sí | SUCIO | Merge remote-tracking branch 'origin/main' into acto/gen2-pi |
| Modelado-Mexicano | acto/gen2-sin-candidato-rutas-1 | acto | 0 | NO | sí | limpio | Merge remote-tracking branch 'origin/main' into acto/gen2-si |
| Modelado-Mexicano | acto/gen2-sonda-caja-1-cierra-reservas-pr632 | acto | 2142 | NO | sí | limpio | Merge origin/main into acto/gen2-sonda-caja-1-cierra-reserva |
| Modelado-Mexicano | acto/gen2-specs-sucesoras | acto | 2180 | NO | sí | limpio | ## CONSUMIDO: GEN2-SPECS-SUCESORAS cita PR #645 |
| Modelado-Mexicano | acto/gen2-universo-c-tandas-enafin | acto | 2154 | NO | sí | limpio | Merge origin/main (PR #640 GEN2-T35-DISEÑO -- FP-360 fix, su |
| Modelado-Mexicano | acto/maestra37-l2-mps-codebook-y-p3 | acto | 1633 | NO | no | limpio | COMMIT-1: spec congelada MAESTRA37-L2 antes de abrir el cues |
| Modelado-Mexicano | acto/maestra38-v1-corrobora-y-reconcilia | acto | 1685 | NO | no | limpio | 0-bis A.3: archiva ENCARGO MAESTRA38-V1 · CORROBORA-Y-RECONC |
| Modelado-Mexicano | claude/cal-g3-ocupacionales-mjm35q | claude | 118 | NO | no | limpio | Contrasta el catálogo de 119 fuentes contra el plan de Hito  |
| Modelado-Mexicano | claude/canon-d5-d6-verdict-e0y6n2 | claude | 181 | NO | no | limpio | Merge remote-tracking branch 'origin/main' into claude/canon |
| Modelado-Mexicano | claude/encargo-maestra38-sello-3-6y5e0z | claude | 1946 | NO | sí | limpio | Merge origin/main into MAESTRA38-SELLO-3 |
| Modelado-Mexicano | claude/explora-puertas-banxico-qnm3cn | claude | 319 | NO | no | limpio | Merge remote-tracking branch 'origin/main' into claude/explo |
| Modelado-Mexicano | claude/g3-horizonte-temporal-id-s88z1w | claude | 280 | NO | no | limpio | Merge remote-tracking branch 'origin/main' into claude/g3-ho |
| Modelado-Mexicano | claude/hitod-perimetro-compara | claude | 70 | NO | no | limpio | bitácora: bloque de cierre — Hito D Fase 1, Paso 4 (ampliaci |
| Modelado-Mexicano | claude/manifiesto-registra-verifica | claude | 65 | NO | no | limpio | bitácora: bloque de cierre — resolución de conflictos, D-07, |
| Modelado-Mexicano | codex/autoridad-semantica-enif | codex | 904 | NO | sí | SUCIO | Merge pull request #338 from Josanoforo/claude/encargo-1-sel |
| Modelado-Mexicano | codex/autoridad-semantica-marco-cobertura-total | codex | 925 | NO | sí | SUCIO | Parche final: universo ENUT por variable y clase de residual |
| Modelado-Mexicano | codex/curador-baseline-semantico | codex | 369 | NO | no | limpio | docs(curador): usa nombre único para la guía |
| Modelado-Mexicano | codex/gen2-marcador-adopcion-cli-1 | codex | 14 | NO | sí | limpio | Cierra integración del marcador y publica consumo efectivo |
| Modelado-Mexicano | codex/gen2-motral2015-prioridades-prestaciones-cli-1 | codex | 1971 | NO | sí | SUCIO | RESULT MOTRAL2015 prioridades corregido |
| Modelado-Mexicano | codex/gen2-recibo-codex-3 | codex | 2 | NO | sí | limpio | [GEN2-RECIBO-CODEX-3] integra ENADID y cierre final |
| Modelado-Mexicano | codex/optimiza-verificacion-ci-prueba-compuerta | codex | 1 | NO | sí | limpio | test temporal: fallos y omisiones para comprobar compuerta C |
| Modelado-Mexicano | codex/propaga-scoring-marco-post330-337 | codex | 905 | NO | no | limpio | docs: propaga estado post PR 330 y 337 |
| Modelado-Mexicano | adr/motor-abm-ajuste | otro | 137 | NO | no | limpio | ADR-50: el motor es un ABM ejecutable, se calibra por AJUSTE |
| Modelado-Mexicano | b4b-alpha | otro | 289 | NO | no | limpio | Merge remote-tracking branch 'origin/main' into b4b-alpha |
| Modelado-Mexicano | barrido1-1786050583 | otro | 348 | NO | no | limpio | T02: renombra el encargo a su fecha de redacción (7/ago) --  |
| Modelado-Mexicano | ci-endurecido | otro | 318 | NO | no | limpio | CI: fetch por refs/pull/N/merge, concurrency guard, permissi |
| Modelado-Mexicano | conf17-fetch | otro | 296 | NO | no | limpio | ENCARGO CONF-17: apertura byte a byte de 17 candidatas del b |
| Modelado-Mexicano | conf17-reconciliado | otro | 300 | NO | no | limpio | ENCARGO CONF-17 (reconciliación): dos corridas concurrentes  |
| Modelado-Mexicano | cruce1-1786051624 | otro | 358 | NO | no | limpio | Merge origin/main into cruce1-1786051624 (ABRIR-4/#159, BARR |
| Modelado-Mexicano | desc1-descarga | otro | 299 | NO | no | limpio | Merge origin/main: resuelve conflicto en manifiesto.yaml (un |
| Modelado-Mexicano | explora2-1786042858 | otro | 338 | NO | no | limpio | T03: quita backticks de raices.local.yaml -- rompía la línea |
| Modelado-Mexicano | fix/inv-seg-filas-colapsadas | otro | 139 | NO | no | limpio | INV-SEG: desdobla cuatro reglas de §3.7 colapsadas en dos fi |
| Modelado-Mexicano | infra/data-raw-externa | otro | 136 | NO | no | limpio | forense/hallazgos.md: registra la recuperación de encig23_es |
| Modelado-Mexicano | int1-integridad-1786003491 | otro | 316 | NO | no | limpio | INT-1: segunda pasada de correccion T03 -- el primer arreglo |
| Modelado-Mexicano | llave2-decreto | otro | 897 | NO | sí | SUCIO | Recifra la cita histórica de ADR-165 que la fusión anterior  |
| Modelado-Mexicano | main | otro | 1965 | sí | no | limpio | Merge pull request #604 from Josanoforo/acto/gen2-e4-limpiez |
| Modelado-Mexicano | main-ff | otro | 171 | NO | no | limpio | Merge pull request #62 from Josanoforo/claude/barrido-escrit |
| Modelado-Mexicano | map1-lector-1786000558 | otro | 312 | NO | no | limpio | Merge origin/main: incorpora verificación CRC/EOCD (PR #146) |
| Modelado-Mexicano | map1b-censo-1786000741 | otro | 307 | NO | no | limpio | nota MAP-1b: cita data/raices.local.yaml con ruta, no solo e |
| Modelado-Mexicano | map2-cruce-1786030513 | otro | 324 | NO | no | limpio | Merge remote-tracking branch 'origin/map2-cruce-1786030513'  |
| Modelado-Mexicano | marco-produccion-total | otro | 931 | NO | sí | SUCIO | ACTO MARCO-PRODUCCION-TOTAL: materializa 253, PARO en congel |
| Modelado-Mexicano | mesa/s-svystat-4celdas | otro | 416 | NO | no | limpio | Merge origin/main into mesa/s-svystat-4celdas — union driver |
| Modelado-Mexicano | preservado/r3-1-merge-verificado-no-empujado | otro | 249 | NO | no | limpio | Merge remote-tracking branch 'origin/sesion/hitoD-r3-1-encig |
| Modelado-Mexicano | reconcilia-puertas | otro | 507 | NO | no | limpio | ACTO RECONCILIA-PUERTAS: addendum final -- PR #208 (nube) ya |
| Modelado-Mexicano | repair1-094125-2 | otro | 323 | NO | no | limpio | Merge remote-tracking branch 'origin/main' into repair1-0941 |
| Modelado-Mexicano | tramite/absorbe-historico | otro | 1967 | NO | no | limpio | P1: T-CRON usa senal(), no warn() -- desacopla de baseline |
| Modelado-Mexicano | ver1-crudo | otro | 296 | NO | no | limpio | ENCARGO VER-1: verificación cruda de cinco fuentes externas  |
| Modelado-Mexicano | verif3-1786042795 | otro | 330 | NO | no | limpio | ci: commit vacío para forzar evento synchronize (diagnóstico |
| Modelado-Mexicano | verif3-outage-note-1786046437 | otro | 331 | NO | no | limpio | hallazgos.md: causa establecida (Actions major_outage) y fus |
| Modelado-Mexicano | verificacion-crc-eocd-corpus | otro | 308 | NO | no | limpio | forense/notas/2026-08-06-verificacion-extraccion-crc-envipe2 |
| Modelado-Mexicano | worktree-mm-enut-paso1-familismo | otro | 199 | NO | no | limpio | bitacora: cierra sesión -- ENUT paso 1 familismo_obligacion |
| Modelado-Mexicano | wt-abrir4-1786051186 | otro | 353 | NO | no | limpio | Merge origin/main into wt-abrir4-1786051186 |
| Modelado-Mexicano | *(53 ramas más, carril `sesion/`, 73–344 commits propios, todas limpias y sin worktree — vintage histórico, GEN1/Hito-D)* | sesion | — | NO | no | limpio | — |
| mm-adq | adq/2026-09-15-nc-0202 | adq | 1 | NO | no | limpio | adq: adquiere metadatos IHSN para NC-0202 |
| mm-adq | adq/2026-09-16-gen2-38-investigacion | adq | 1 | NO | no | limpio | [ADQ] 2026-09-16 |
| mm-adq | censo/2026-09-16 | censo | 4 | NO | no | limpio | [ADQ] 2026-09-16 |

*(Las 53 filas `sesion/` colapsadas en una: todas del vintage GEN1/Hito-D, todas limpias, ninguna con worktree, ninguna en origin — tabla completa de las 131 en `/home/pc0/respaldo-ramas-2026-09-20-Modelado-Mexicano.bundle`, recuperable con `git bundle unbundle` + `git branch -vv`.)*

## P6 · Restos que no son ramas

- **`data/corrida0/CALC-C2-COMPUESTO-IC-ENIF2024-0001/`** en `/home/pc0/mm-gen2-c2-compuesto-ic-enif2024-1` (sin seguimiento, junto con `forense/prereg-caja/C2-COMPUESTO-IC-ENIF2024-spec-v1_0.md` y `tests/test_c2_ic_enif2024_guardia.py`, todos del 19/sep). El nombre nombra `enif2024`, una de las cuatro olas reservadas de la prohibición de lectura de este mismo encargo (P6: "encig25\*, enif2024\*, envipe2025\*, eder2025\*"). **No se abrió, no se leyó, no se pegó contenido** — solo se listó ruta, fecha (19/sep) y que existe. Es la rama EN-VUELO `acto/gen2-c2-compuesto-ic-enif2024-1`, ya protegida por esa regla; este hallazgo es adicional, no cambia su clasificación.
- **`forense/cron/RESPALDO-TAREA-20260915T2245.xml`** sin seguimiento en `/home/pc0/mm-adq` (el propio clon del runner ADQ) — nombre consistente con un backup de Task Scheduler de Windows (ver `feedback_sandbox_mnt_c_vista_dual` sobre `tzutil`/Task Scheduler del runner). No se abrió.
- **`data/curacion-registro/cola-adquisicion-registro.tsv.lock`** sin seguimiento en `/home/pc0/mm-gen2-reparacion-cierre-cron`; **`data/.manifiesto.lock`** y **`data/curacion-registro/.alta-relacion.lock`** en otros dos worktrees de la familia ADQ — archivos de lock, no se tocaron (fuera de perímetro: nada de `rm`/`fuser` sobre ellos).
- **`scratchpad/`** completo sin seguimiento en `/home/pc0/mm-llave2-decreto` — no se abrió ni se listó su contenido interno más allá de confirmar que es un directorio.
- **`.barrido2`** sin seguimiento en `/home/pc0/mm-autoridad-semantica-marco-produccion` y en `/home/pc0/mm-marco-produccion-total` — mismo nombre en dos worktrees distintos, no abierto.
- **`data/corrida0/CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001/medidor.py`** con estado `AA` (conflicto de merge sin resolver, ambos lados "added") en `/home/pc0/mm-gen2-motral2015-prioridades-prestaciones-cli-1` — un merge quedó a medias; no se resolvió ni se tocó, solo se reporta.
- **`error.log`** sin seguimiento en el clon base `/home/pc0/Modelado-Mexicano` — un solo archivo, no examinado.
- **`forense/prereg-caja/validacion-independiente-scratch/`** en las tres `worktree-agent-*` de Claude Code (ver P5).

Ningún resto se abrió, ejecutó, ni se pegó contenido más allá de nombre de archivo/carpeta, fecha de modificación y (donde se pidió) tamaño agregado del directorio.

## P7 · Anti-PR#77

`data/raw` en los dos clones (la pregunta literal del encargo): ambos son **symlinks reales** al corpus compartido (`Modelado-Mexicano/data/raw → /home/pc0/mm-corpus/raw`, `mm-adq/data/raw` idéntico) — sin payloads propios fuera del corpus compartido en ninguno de los dos clones.

**Extensión no pedida por el encargo, hecha porque P4 depende de ella:** el mismo chequeo (symlink vs. directorio real) se corrió en los **165** worktrees no-prunables de ambos clones, porque un `data/raw` real y gitignorado es invisible para `git status --porcelain` — `git worktree remove` lo habría borrado sin que el chequeo de "worktree limpio" lo hubiera detectado. Resultado: **164 symlinks/ausentes, 1 directorio real** — `/home/pc0/mm-gen2-wbes2023-precision-interacciones-cli-2/data/raw/` (5 archivos, 16 KB agregados: `WBES_Mexico2023_Documentation.zip`, `ddi-documentation-english_microdata-6453.pdf`, `WBES-Sampling-Note-Consolidated-2022.pdf`, `WBES_Mexico2023_Data.zip`, `MEX_2023_WBES_v01_M.xml`). Inspeccionado: cada archivo es en realidad un **symlink individual** — 3 a `/mnt/c/Users/PC0/Descargas MX/...` (la segunda raíz `descargas_mx`), 1 al corpus compartido, 1 idéntico. No hay bytes de payload en riesgo (nada se habría perdido si se borraba), pero el patrón — `data/raw` como directorio real con symlinks por archivo, en vez de un solo symlink al corpus — es no estándar y exactamente lo que esta pieza existe para atrapar. **No se movió nada** (mandato explícito del encargo). Esta rama ya estaba excluida de P4 por la regla de 24 h (2.0 h); se deja fuera también por este hallazgo, independientemente de cuándo cumpla las 24 h — mesa decide si normalizar el symlink antes de limpiar esta rama.

## Cierre

### ## NO-CORRIDO / RESERVAS
Ninguno.

### ## CONSUMIDO
Este PR.

### Estado final (crudo)

```
$ git -C /home/pc0/Modelado-Mexicano branch --no-color | wc -l
159
$ git -C /home/pc0/Modelado-Mexicano worktree list | wc -l
51
$ git -C /home/pc0/mm-adq branch --no-color | wc -l
7
$ git -C /home/pc0/mm-adq worktree list
/home/pc0/mm-adq a92126f0 (detached HEAD)
```

### Resumen para hallazgos.md
150 ramas locales examinadas en `Modelado-Mexicano` (270) + `mm-adq` (37) — descontando `HEAD` desprendido — de las cuales 142 se borraron (141 rama+worktree, 1 rama rechazada por git tras retirar su worktree), 26 quedaron fusionadas-pero-recientes para mañana, 15 quedaron sucias sin tocar, y 131 quedan con trabajo propio para que mesa firme caso por caso (incluye los cuatro casos ya conocidos, ahora verificados: `marcador-adopcion-cli-1` BORRABLE-TRAS-FIRMA, `enadid2023-union-sexo-edad-cli-2` con premisa corregida — ya está en `main`, `recibo-codex-3`/`prueba-compuerta` confirmados menores, `…-base-medicion` NO-ENCONTRADO). Dos bundles de respaldo verificados y con sha256 en `/home/pc0/`. Un hallazgo anti-PR#77 (WBES, symlinks no estándar, nada movido) y un hallazgo de infraestructura propia de Claude Code (`/home/pc0/.git`, `.claude/worktrees/agent-*`) que no son restos del proyecto.
