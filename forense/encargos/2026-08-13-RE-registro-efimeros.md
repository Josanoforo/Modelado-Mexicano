# ENCARGO A · REGISTRO-EFÍMEROS — anotar lo que sobrevive al borrado

- **SHA de redacción:** el encargo no trae un SHA de redacción explícito en su propio texto (a diferencia de, p. ej., ENASIC-SPLIT). Se declara aquí el que este acto verificó al arrancar, per Bloque D punto 2: `origin/main` estaba, al primer `git branch -r`/`git status` de esta sesión, en `f8eb2e3a3a7ee29c5875b677d82e511a6e4cadac` (2026-08-11 23:50:23 -0600) — **desactualizado**, porque este clon no había hecho `git fetch origin main` desde su creación. Tras `git fetch origin main`, el real es `959006ac212b1b955fe7fe75fe7c177bded54f20` (2026-08-13 09:10:23 -0600, merge de PR #206/enasic-split). Es el SHA contra el que este acto deriva todo lo que reporta. Detalle completo de la discrepancia y su corrección en la nota de arranque, abajo.
- **Entorno asignado:** NUBE (`cloud_default`, confirmado por `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`). Repo-only, sin red, sin corpus. **NO** en caja (Ubuntu/WSL local) — el propio encargo lo declara y no hay razón para verificarlo contra red: este acto no abre microdato ni depende de `data/raw`.
- **Estado:** `CONSUMIDO` — ejecutado por el PR de esta rama (`claude/registro-efimeros-forense-mm9sra`), COMMIT 2 (`forense/registro-efimeros-v1_0.md` + cierre en `forense/hallazgos.md`). Nace `VIVO` en el COMMIT 1 de este mismo acto (el que archiva este texto); se marca `CONSUMIDO` aquí, en el COMMIT 2, al cerrar.

---

Texto del encargo, verbatim, tal como se recibió:

---

ENCARGO A · REGISTRO-EFÍMEROS — anotar lo que sobrevive al borrado

Entorno: NUBE. Repo-only, sin red, sin corpus. Firma `cloud_default` sin sonda (ADR-59(b)). NO en caja.

## §0 · Por qué existe, y por qué no es papeleo

Seis refs `*-huerfana-20260813` están juzgadas sin contenido único y vencen ~12/sep. Un ref borrado deja de existir; su SHA no. Mientras el objeto viva en el reflog del servidor, un SHA anotado hace el borrado reversible. Sin SHA anotado, no lo es — y el objeto se vuelve inalcanzable en la siguiente recolección de basura.

Y hay un precedente que este acto también debe cerrar. El 13/ago un acto afirmó que `tools/curador_registro/produce.py` no existía en `19d885d`; era falso, y la causa fue un `cd` a un worktree hermano del que no volvió. Los comandos siguientes corrieron contra un directorio desviado y devolvieron salida — se sintieron verificados. Es primo del defecto del espejo que instrucciones-proyecto ya nombra, y hoy no está escrito en ningún lado como patrón.

Este acto captura las dos cosas: los efímeros, y el patrón que los hace peligrosos.

## §1 · PERÍMETRO

**ESCRIBE:** `forense/registro-efimeros-v1_0.md` (nuevo, append-only) · `forense/hallazgos.md` (append, merge local siempre; GitHub no honra `merge=union`, editor web de conflictos prohibido) · `forense/encargos/2026-08-13-RE-registro-efimeros.md` (A.3, con prefijo de acto; la nota va sin él — T02 normaliza sin distinguir directorio).

**NO ESCRIBE:** `canon/**` · `data/**` · `milpa/**` · `tools/**` · `tests/**` · ninguna rama (este acto NO borra nada).

**Concurrencia:** ninguna rama de trabajo viva al redactar. Verifica igual.

## §2 · ARRANQUE

Bloque de cinco puntos íntegro. Punto 3: `data/raw` no aplica, decláralo y salta. Punto 4: nube, sin red, salta la sonda y dilo. Punto 5: ninguna cifra del espejo.

PREMISAS (script, crudas — reporta la salida, no la interpretes):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
pwd                                                   # ⚠️ confirma que sigues en el clon
git branch -r | grep -c huerfana                      # esperado 6
ls forense/registro-efimeros-v1_0.md 2>/dev/null && echo "YA EXISTE - PARA"
```

## §3 · COMMIT 1 — la captura, derivada en sesión

Deriva tú los seis registros. Las cifras de abajo son del 13/ago y sirven para contrastar, no para copiar.

```bash
for b in $(git branch -r | grep huerfana); do
  n=${b#origin/}
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$n" \
    "$(git rev-parse $b)" \
    "$(git log -1 --format='%ci' $b)" \
    "$(git diff --diff-filter=A --name-only origin/main $b | wc -l)" \
    "$(git diff --diff-filter=M --name-only origin/main $b | wc -l)" \
    "$(git diff --diff-filter=D --name-only origin/main $b | wc -l)"
done
```

Lo derivado el 13/ago, para contraste:

| rama | SHA | último commit | A | M | D |
|---|---|---|---|---|---|
| mapa-ext-1-huerfana-20260813 | 87ae19ad47ca0a6d7b30a607c5fe4a840efafa17 | 2026-08-06 18:43:48 -0600 | 0 | 19 | 247 |
| mapa-ext-academico-huerfana-20260813 | 1524a44f98e95b1036a62f12ffb978cbc0d81013 | 2026-08-06 18:42:13 -0600 | 0 | 18 | 247 |
| mapa-ext-civil-huerfana-20260813 | 34a50b12e7bc20b62d325e53770540309bd5f543 | 2026-08-06 18:42:12 -0600 | 0 | 18 | 247 |
| mapa-ext-integracion-huerfana-20260813 | 0be9bb575a800d7296251e5359529370e0251252 | 2026-08-06 18:59:58 -0600 | 0 | 18 | 235 |
| mapa-ext-oficial-huerfana-20260813 | 9c85f5e3f10e78c394a9cc33935ea89e82b842e9 | 2026-08-06 18:42:12 -0600 | 0 | 18 | 247 |
| med-r3-4-revalida-1-huerfana-20260813 | bd0259c6ffef8d85747e6fb239eeddc868bcec5a | 2026-08-06 17:19:53 -0600 | 0 | 18 | 251 |

Si tu derivación difiere de esta tabla: usa la tuya y reporta la diferencia. Es un hallazgo, no una molestia.

### La interpretación, escrita con su límite

A = 0 en las seis — la prueba barata que el transfer del 12-13/ago §5.5 declaró suficiente ("si da 0, no hay nada que rescatar"). Pero `--diff-filter=A` solo ve archivos añadidos y no ve modificaciones, así que por sí sola no basta. Escríbelo así en el registro, porque el transfer la presentó como suficiente y no lo es.

Los ~18 M son versiones viejas, no trabajo único, y hay que probarlo por fecha, no afirmarlo. Verificado el 13/ago: `canon/gobernanza-v1_15.md` en la rama es de `f5d80fc` (5/ago), en main de `2131f04` (13/ago); `.gitattributes` en la rama de `b9d9dfc` (5/ago), en main de `e3781ee` (12/ago). Corre el contraste de fechas sobre al menos 4 archivos por rama y pega la salida.

Los ~247 D NO son borrados de la rama. Son la firma de la purga del 10/ago: main añadió esos archivos después. El transfer §5.5 ya lo documentó — cítalo, no lo re-deduzcas.

## §4 · COMMIT 2 — el archivo

`forense/registro-efimeros-v1_0.md`, cabecera ADR-36 (ARCHIVO / QUÉ ES / QUÉ NO ES / VERIFICAS ASÍ), append-only, con:

**§1** · La tabla de los seis, con SHA completo de 40 caracteres —no abreviado, un `%h` puede volverse ambiguo cuando el repo crece— y las tres cifras de diff con el comando que las produjo.

**§2** · Qué es y qué no es un ref efímero. "Un ref borrado deja de existir; su SHA no. Mientras el objeto viva en el reflog del servidor, el SHA anotado hace el borrado reversible. Este archivo no garantiza que el objeto siga existiendo — garantiza que sabes qué pedir."

**§3** · La ventana. Borrado autorizado a partir del 12/sep/2026 por decisión de mesa del 12-13/ago. Este acto no borra.

**§4** · La regla de captura, para los que vengan. Antes de borrar cualquier ref: SHA de 40 caracteres, fecha del último commit, y las tres cifras de diff contra main. Tres minutos. Sin eso, el borrado es irreversible.

**§5** · El patrón que hace falsas las verificaciones — y es el que más valdrá dentro de un mes.

`cd` a un worktree hermano sin volver. El 13/ago un acto afirmó que `tools/curador_registro/produce.py` no existía en `19d885d`. Era falso: `git cat-file -e 19d885d:tools/curador_registro/produce.py` devuelve EXISTE, y el único commit que lo añade en toda la historia es `59d6c40`. La causa reconstruida por el propio acto: hizo `cd` a `/home/pc0/wt-abrir4-1786051186` para inspeccionar los commits de un worktree hermano y no volvió. Los `git ls-tree` posteriores corrieron contra ese directorio. Devolvieron salida, así que se sintieron verificados. Y la adenda escrita para corregirlo fabricó una segunda afirmación falsa —que un acto concurrente los había "restaurado"— por inferir desde un diff sin verificar la inferencia.

Contramedida, y cabe en una línea del ARRANQUE: `pwd` antes de cualquier comando de estado del repositorio, y `git -C <ruta>` en vez de `cd` cuando haya que mirar otro árbol. Un `git ls-tree` en el directorio equivocado no falla: contesta otra pregunta.

Y una línea en `hallazgos.md` que nombre el patrón, no el incidente — porque el incidente ya está en la nota de ENASIC-SPLIT y lo que falta es el patrón.

Suite: `--baseline` VERDE contra `2cb39c9`. T03: los nombres de rama van sin backticks — no son archivos del repo y una cita colgante es WARN nuevo. Si un test truena, ese es el hallazgo: no se maquilla.

## §5 · NO HACE

No borra ninguna rama. No toca `canon/`, `data/`, `milpa/`, `tools/` ni `tests/`. No juzga de nuevo si las seis tienen contenido único — eso está resuelto y este acto lo registra, no lo re-litiga. No propone adelantar la ventana del 12/sep.

## §6 · CONTADOR

Refs con SHA capturado: 0 → 6. Y un patrón de falsa verificación escrito donde se lea antes de repetirlo.

---

**Nota de arranque sobre este texto (no forma parte del encargo, es glosa de quien lo ejecuta):**

**Bloque de cinco puntos (§2 del encargo), reportado íntegro:**

1. **REPO.** `/home/user/Modelado-Mexicano` (clon existente, no se clonó uno nuevo). `git log -1 --format="%h %s"` → `959006a Merge pull request #206 from Josanoforo/enasic-split`. `git status --short` → limpio. Rama actual: `claude/registro-efimeros-forense-mm9sra`.
2. **SHA.** Discrepancia material encontrada y corregida — no cosmética, cambiaba las cifras de M/D del acto. El primer `git branch -r | grep -c huerfana` de la sesión dio **0**, no el 6 esperado por el encargo: este clon solo traía fetched `origin/main` (además desactualizado, ver abajo) y la propia rama de trabajo — nunca había hecho fetch de las seis ramas `*-huerfana-20260813`. `git ls-remote origin` confirmó que las seis SÍ existen en GitHub, con los mismos 6 SHA que cita la tabla de contraste del §3 del encargo. `git fetch origin <las-seis>` las trajo; el conteo pasó a 6. Segunda discrepancia, encontrada al revisar la primera: `origin/main` local estaba en `f8eb2e3` (2026-08-11 23:50:23), **desactualizado** frente al real — este clon tampoco había hecho fetch de `main` desde su creación. `git fetch origin main` lo puso en `959006a` (2026-08-13 09:10:23), que sí coincide con el `HEAD` real de la propia rama de trabajo de esta sesión. Todas las cifras que reporta este acto están derivadas **después** de ambas correcciones, contra `origin/main=959006a`. Per Bloque D punto 2 ("si main se movió: NO es PARO — refresca, re-deriva, reporta la diferencia"): no es PARO, se refrescó, se re-derivó, se reporta aquí y en `forense/registro-efimeros-v1_0.md`.
3. **data/raw.** No aplica — declarado y saltado, per instrucción explícita del encargo. Verificado igual, por barato: `ls data/raw` → no existe (código de salida 2), consistente con "no aplica" y no con un montaje parcial que debiera investigarse.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`. Sonda de red saltada, per instrucción explícita del encargo (nube, sin red, este acto no toca microdato). Firma consistente con ADR-59(b)/`cloud_default` sin sonda.
5. **ESPEJO.** Ninguna cifra de este acto sale del espejo del proyecto. Todas las cifras citadas —SHA, fechas, A/M/D, verificación de `produce.py`— salen de comandos `git`/`ls` corridos en este mismo clon durante esta sesión, con el comando a la vista en `forense/registro-efimeros-v1_0.md` y en esta nota.

**Concurrencia (§1 del encargo):** verificado, no solo asumido — `git ls-remote origin` listando `refs/heads/*` no muestra ninguna rama viva aparte de `main`, las seis `*-huerfana-20260813` y la propia rama de trabajo de esta sesión. Ninguna rama de trabajo concurrente.

**Hallazgo material adicional, fuera de lo que el encargo anticipaba — reportado aquí y no escondido:** el patrón que el §0/§4-§5 del encargo pide escribir en `hallazgos.md` ya estaba escrito. `git log` muestra el commit `4a0c363` ("hallazgos.md: patron generalizado -- cd a worktree hermano sin volver produce afirmaciones falsas que se sienten verificadas, primo del defecto del espejo"), fusionado a `main` en el mismo merge de PR #206 que trajo `origin/main` a `959006a` — es decir, entre que este encargo se redactó (que asumía "hoy no está escrito en ningún lado como patrón") y que este acto empezó a ejecutarlo, otro acto (el cierre de ENASIC-SPLIT) ya lo escribió, con el mismo encuadre "patrón, no incidente". No se duplica esa entrada. Detalle completo de qué se hizo en su lugar, en `forense/registro-efimeros-v1_0.md` §5 y en la entrada nueva de `hallazgos.md` que cierra este acto.
