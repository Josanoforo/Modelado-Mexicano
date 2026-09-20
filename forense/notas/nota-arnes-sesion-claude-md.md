# ARNES SESSION-START-HOOK + CLAUDE.md · nota de cierre

**20/sep/2026 · NUBE, Sonnet 5 · sin corpus montado, cero microdato abierto por este acto.**
El entorno de esta sesión es **NUBE**, confirmado por `tools/entorno.py --arranque` (abajo):
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, `data/raw` ausente.

## 0 · Perímetro tocado

- `.claude/settings.json` (nuevo) — un hook `SessionStart`.
- `tools/entorno.py` — añadida `--arranque`, reusando `sonda_red()`/`acceso_corpus()`/`_git()` ya existentes.
- `.claude/commands/acto.md` — solo el punto 4 (ARRANQUE), con la doble vía hook/manual.
- `CLAUDE.md` (nuevo).
- `AGENTS.md` — solo la cabecera, sin tocar el resto.
- `tests/test_arnes_sesion.py` (nuevo).
- Esta nota.

Nada más se tocó. No se crearon skills, subagentes, plugins ni reglas `deny`/`allow`. No se configuraron entornos de nube ni Remote Control.

## 1 · `tools/entorno.py --arranque` — salida cruda de esta sesión

```
$ python3 tools/entorno.py --arranque
ENTORNO-DERIVADO = NUBE
senal-corpus: montado=NO archivos_examinados=0
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, via_proxy=SI)
head-vs-origin/main: detras=535 adelante=487 (sin fetch)
worktrees: 1
es-worktree: NO
ramas-locales-con-commits-propios: 1/2
data-raw-en-este-worktree: NO
SI EL ENCARGO DECLARA OTRO ENTORNO QUE ENTORNO-DERIVADO: PARA ANTES DE CUALQUIER OTRA COSA.
```

9 líneas (≤12), corrida en 0.3s (<15s), código de salida 0.

El campo `red` usa `%{http_connect}` de curl, no solo `%{http_code}`: cuando el proxy
rechaza el `CONNECT` antes de que la petición HTTPS llegue a viajar, `http_code` queda
en `000` (nunca se completó una petición) pero `http_connect` trae el código real del
`CONNECT` (`403` aquí). Sin esa distinción, `DENEGADA-POR-POLITICA` se confundiría con
`SIN-RED`.

## 2 · Citas de documentación (consultadas hoy, 20/sep/2026)

Todas por `WebFetch` (disponible en esta sesión) contra `code.claude.com`.

1. **Import de `CLAUDE.md`** — `https://code.claude.com/docs/en/memory` (VERIFICADO):
   > "CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported
   > files are expanded and loaded into context at launch alongside the CLAUDE.md that
   > references them."
   Se usó: `CLAUDE.md` trae `@instrucciones-proyecto-v2_14.md`, no solo un puntero de
   texto — el archivo está dentro del working directory, así que no dispara la
   aprobación de "external imports".

2. **`stdout` de `SessionStart`, códigos de salida, timeouts** —
   `https://code.claude.com/docs/en/hooks` (VERIFICADO):
   > "For most events, Claude Code writes stdout to the debug log and doesn't show it in
   > the transcript. The exceptions are `UserPromptSubmit`, `UserPromptExpansion`,
   > `SessionStart`, and `PostModelSwitch`, where Claude Code adds plain-text stdout as
   > context that Claude can see and act on."
   Exit 0 → stdout se agrega como contexto; exit 2 → bloquea el arranque de la sesión;
   cualquier otro código → error no bloqueante, la sesión sigue. Timeout por defecto de
   un hook `command` en `SessionStart`: 600s (se puede acotar con el campo `timeout`,
   no se acotó aquí porque `--arranque` ya corre en <1s). Un hook `mcp_tool` no puede
   correr en `SessionStart` al arrancar (los servidores MCP aún no están disponibles);
   por eso el hook usa `type: "command"`.

3. **Multi-repo en la nube y `.claude/settings.json`** —
   `https://code.claude.com/docs/en/settings` (VERIFICADO):
   > "Shared project settings (`.claude/settings.json`): read in a session with one
   > repository, because the file is part of the clone and the session starts inside it.
   > [...] A session with several repositories starts above the clones, so from each
   > repository's `.claude/settings.json` it loads only the plugins and marketplaces the
   > file declares, not permission rules, hooks, `env`, or other keys."
   Es decir: en una sesión de un solo repo, el hook de este repo corre. En una sesión
   multi-repo, **el hook NO corre** — de ahí que el punto 4 de `/acto` conserve la vía
   manual (`python3 tools/entorno.py --arranque`) como respaldo, no como adorno.

## 3 · Tabla — qué superficie carga qué hook / `CLAUDE.md`

| superficie | `.claude/settings.json` (hooks) de este repo | `CLAUDE.md` de este repo |
|---|---|---|
| nube, un repo | LEÍDO-EN-DOC: sí, se lee (settings.md, "read in a session with one repository") | LEÍDO-EN-DOC: sí (cloud-environments, "What carries over": `CLAUDE.md` viaja) |
| nube, multi-repo | LEÍDO-EN-DOC: no para hooks/permisos/env — solo `plugins`/`marketplaces` de cada `.claude/settings.json` | LEÍDO-EN-DOC: no verificado explícitamente en esta consulta para el caso multi-repo (la doc solo distingue `settings.json`); se trata como riesgo, de ahí la vía manual en `/acto` |
| local (máquina propia) | LEÍDO-EN-DOC: sí, siempre (misma máquina, mismos archivos) | LEÍDO-EN-DOC: sí, siempre |
| Remote Control | OBSERVADO-AQUÍ: no aplica — Remote Control dirige una sesión LOCAL desde el teléfono/navegador; no es una sesión de nube, así que lee lo mismo que "local" (LEÍDO-EN-DOC, por descarte de la doc de `claude-code-on-the-web` que distingue Remote Control de sesiones de nube) |

Esta misma sesión es NUBE, un solo repo (`Modelado-Mexicano`): el hook de `.claude/settings.json`
que este acto acaba de crear **no se pudo observar en ejecución dentro de esta sesión**
(se creó durante la sesión; un hook `SessionStart` corre al arrancar/reanudar, no a mitad
de sesión) — la fila correspondiente queda LEÍDO-EN-DOC, no OBSERVADO-AQUÍ, y así se
declaró arriba.

## 4 · Los 5 archivos que citan `instrucciones-proyecto-v2_13.md` (solo listados, sin arreglar)

Vía `git grep -l "instrucciones-proyecto-v2_13.md"`, filtrando encargos/notas archivadas
(que citan el nombre como historial, no como puntero vigente):

1. `canon/estado-programa-v1_14.md`
2. `canon/gobernanza-v1_15.md`
3. `canon/informe-programa-v1_0.md`
4. `canon/registro-rotulos.tsv`
5. `data/INFRAESTRUCTURA-v1_0.md`

(El grep también trae `forense/encargos/*` y `forense/hallazgos.md`, que quedan fuera de
esta lista por ser encargos/notas, tal como pide el encargo.) Fuera de perímetro — no se
tocan aquí.

## 5 · Hallazgo — rótulo "red caída" del incidente #894

**Ya está asentado**, no hace falta re-rotularlo desde este acto. `canon/estado-programa-v1_14.md`
(anotación L0 de `ADR-555`, `ACTO GEN2-CELDA-D-PILOTO-3-P0`, 20/sep/2026) ya declara,
verbatim:

> "el `sonda_red = 000` que `#894` leyó como «red caída» es artefacto de `curl` sin proxy
> — la compuerta del entorno devuelve `gateway answered 403 to CONNECT (policy denial)`
> para `www.inegi.org.mx:443`, es decir `inegi.org.mx` no está en la política de salida,
> no un fallo transitorio."

Esta pieza (P1, `tools/entorno.py --arranque`) implementa exactamente esa distinción de
forma mecánica y reutilizable: el estado `DENEGADA-POR-POLITICA` (vía `%{http_connect}`)
en vez de colapsar todo `000` en "sin red", así que el próximo incidente similar no
necesita que alguien lo re-derive a mano.

## 6 · No verificado

- El caso "nube, multi-repo" para `CLAUDE.md` específicamente (no solo `.claude/settings.json`)
  no aparece distinguido explícitamente en la página de settings consultada; se infiere
  de "What carries over" (`cloud-environments`) que `CLAUDE.md` sí viaja, pero no se
  fetcheó esa página con el detalle multi-repo por límite de alcance de esta nota.
- No se corrió esta sesión dentro de un contenedor multi-repo real para observar el
  comportamiento directamente — todo lo relativo a multi-repo es LEÍDO-EN-DOC.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Fetch explícito de `cloud-environments#what-carries-over-from-your-setup` para el detalle exacto de `CLAUDE.md` en multi-repo | NO-VERIFICABLE-AQUÍ (fuera del alcance de las tres citas pedidas por el encargo; la cita de `settings.md` ya resuelve el punto central de hooks) | La fila "nube, multi-repo / CLAUDE.md" de la tabla §3 queda con un matiz sin fetch directo | SIN-ASIGNAR |
| Arreglo de los 5 archivos que citan `instrucciones-proyecto-v2_13.md` | FUERA-DE-PERÍMETRO (el encargo pide solo listarlos) | Esos 5 archivos siguen citando una versión no vigente | SIN-ASIGNAR |

## CONSUMIDO

Sin PR (el encargo no lo pidió): commit(s) en `claude/session-start-hook-claude-md-ncxwc7`,
empujados con `git push -u origin claude/session-start-hook-claude-md-ncxwc7`.
