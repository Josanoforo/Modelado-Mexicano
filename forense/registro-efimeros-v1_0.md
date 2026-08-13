# Registro de refs efímeros
### `registro-efimeros` · **v1.0** · 13 de agosto de 2026 · ENCARGO A · REGISTRO-EFÍMEROS (nube) · anota lo que sobrevive al borrado

> | | |
> |---|---|
> | **ARCHIVO** | `registro-efimeros-v1_0.md` |
> | **NOMBRE ESTABLE** | **`registro-efimeros`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Registro append-only, una fila por ref efímero (una rama que va a borrarse) capturado antes de su borrado autorizado: SHA de 40 caracteres, fecha del último commit, y las tres cifras de diff contra `main` — lo mínimo que hace reversible un borrado mientras el objeto siga vivo en el reflog del servidor. Nace con los seis refs `*-huerfana-20260813`; los siguientes se añaden por fila, no por archivo nuevo. |
> | **QUÉ NO ES** | No adjudica si una rama tiene contenido único — eso lo resuelve el acto que la marcó efímera (aquí: ACTO W′ y ACTO Z, citados en §1) y este archivo lo registra, no lo re-litiga. No autoriza ni ejecuta ningún borrado — la ventana de §3 la fija mesa, no este archivo, y este acto no borra nada. No es una copia de seguridad del contenido: es la anotación mínima que permite pedir el objeto de vuelta mientras exista. |
> | **VERIFICAS ASÍ** | §1 trae, por fila, el comando exacto y el SHA de `origin/main` contra el que se corrió (`959006a`). Re-correrlo hoy con un `main` distinto dará M/D distintos — es esperado y está explicado en la nota al pie de §1, no es un defecto de esta tabla. |

---

## §1 · Los seis, con SHA completo

Comando (corrido tal cual, una vez por rama, contra `origin/main` = `959006ac212b1b955fe7fe75fe7c177bded54f20`, 2026-08-13 09:10:23 -0600 — merge de PR #206/enasic-split, el más reciente en el momento de correr esto):

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

| rama | SHA (40) | último commit | A | M | D |
|---|---|---|---|---|---|
| mapa-ext-1-huerfana-20260813 | `87ae19ad47ca0a6d7b30a607c5fe4a840efafa17` | 2026-08-06 18:43:48 -0600 | 0 | 19 | 249 |
| mapa-ext-academico-huerfana-20260813 | `1524a44f98e95b1036a62f12ffb978cbc0d81013` | 2026-08-06 18:42:13 -0600 | 0 | 18 | 249 |
| mapa-ext-civil-huerfana-20260813 | `34a50b12e7bc20b62d325e53770540309bd5f543` | 2026-08-06 18:42:12 -0600 | 0 | 18 | 249 |
| mapa-ext-integracion-huerfana-20260813 | `0be9bb575a800d7296251e5359529370e0251252` | 2026-08-06 18:59:58 -0600 | 0 | 18 | 237 |
| mapa-ext-oficial-huerfana-20260813 | `9c85f5e3f10e78c394a9cc33935ea89e82b842e9` | 2026-08-06 18:42:12 -0600 | 0 | 18 | 249 |
| med-r3-4-revalida-1-huerfana-20260813 | `bd0259c6ffef8d85747e6fb239eeddc868bcec5a` | 2026-08-06 17:19:53 -0600 | 0 | 18 | 253 |

Los seis SHA y las seis fechas coinciden exactos con la tabla de contraste del 13/ago que trae el encargo (`forense/encargos/2026-08-13-RE-registro-efimeros.md` §3) y con `git ls-remote origin` corrido antes de fetch-earlas (no había refs remotos de estas seis en este clon hasta que se pidieron por nombre — ver nota de arranque en el encargo archivado). **M y D difieren de esa tabla y se reportan como hallazgo, per instrucción del propio encargo ("si tu derivación difiere... es un hallazgo, no una molestia"):**

| | tabla del 13/ago (encargo) | esta derivación | diferencia |
|---|---|---|---|
| A | 0 en las seis | 0 en las seis | ninguna |
| M | 19/18/18/18/18/18 | 19/18/18/18/18/18 | ninguna |
| D | 247/247/247/235/247/251 | 249/249/249/237/249/253 | **+2 uniforme, las seis** |

Causa verificada, no supuesta: entre que se derivó la tabla del encargo y que se corrió la de arriba, `origin/main` avanzó por el merge de PR #206 (`9805ed2` → `959006a`). Aislado ese merge solo (`git diff --diff-filter=A --name-only 9805ed2 959006a`): añadió exactamente dos archivos, `forense/encargos/2026-08-13-ENASIC-SPLIT.md` y `forense/notas/2026-08-13-enasic-split-verificacion.md` — ninguno de los dos existe en ninguna de las seis ramas (las seis están congeladas desde el 6/ago). Dos archivos nuevos en `main` que ninguna rama tiene = dos archivos más que "`main` tiene y la rama no" = D+2 en las seis. No hay archivo perdido ni recuperado; es `main` moviéndose bajo un repo vivo, exactamente el caso que Bloque D punto 2 anticipa ("si main se movió: no es PARO, refresca y reporta la diferencia").

### A = 0 — por qué no basta por sí solo

A = 0 en las seis es la prueba barata que ya se usó como criterio de suficiencia en este programa: ACTO Z (`forense/notas/2026-08-13-z-inventario-curador.md`, puntos 4 y 7) cerró su acto sobre el clon `Modelado-Mexicano-curador` con exactamente este criterio — "`git diff --diff-filter=A --name-only origin/main HEAD | wc -l` → 0" — y "se cierra aquí... sin paso 2 ni 3". Es una prueba real: si `main` no tiene un archivo que la rama sí tiene, hay algo que buscar. Pero `--diff-filter=A` solo ve archivos que la rama tiene y `main` no — no ve **modificaciones**: una rama con A=0 puede seguir teniendo trabajo único si cambió el contenido de un archivo que `main` también tiene, de un modo que `main` nunca incorporó. Eso es exactamente lo que M mide, y es la siguiente pregunta, no una que A=0 responda por sí sola. Escrito aquí porque, tal como lo describe el encargo que abrió este acto, esa insuficiencia se presentó alguna vez como si A=0 bastara por sí mismo — y no basta: hace falta mirar M también (abajo).

*(Nota de verificación honesta: este acto buscó la cita exacta "el transfer del 12-13/ago §5.5" que el encargo nombra como fuente de esa afirmación, y no la localizó como archivo o sección propia en `forense/` bajo ese nombre — el precedente real, verificado y citable, más cercano en el repo es ACTO Z, arriba. Es posible que "el transfer" viva en conversación de mesa no comiteada al repo, uso legítimo de contexto externo per `AGENTS.md` ("documentos de traspaso... sirven como contexto"). Se declara la búsqueda y su resultado en vez de inventar la cita o callar el intento.)*

### M ≈ 18 — versiones viejas, probado por fecha en las seis ramas

Contraste de 4 archivos comunes a las seis (de los ~18-19 M de cada una), fecha del último commit que los tocó en la rama contra el último commit que los tocó en `main`:

```bash
FILES=(".gitattributes" "canon/gobernanza-v1_15.md" "canon/estado-programa-v1_10.md" "tests/check.py")
for f in "${FILES[@]}"; do
  printf '%s\t%s\n' "$f" "$(git log -1 --format='%h %ci' origin/main -- "$f")"
done
for b in $(git branch -r | grep huerfana); do
  for f in "${FILES[@]}"; do
    printf '%s\t%s\t%s\n' "$b" "$f" "$(git log -1 --format='%h %ci' $b -- "$f")"
  done
done
```

| archivo | en `main` (`959006a`) | en las seis ramas (idéntico en las seis) |
|---|---|---|
| .gitattributes | `e3781ee` — 2026-08-12 05:46:27 +0000 | `b9d9dfc` — 2026-08-05 17:11:09 +0000 |
| canon/gobernanza-v1_15.md | `2131f04` — 2026-08-13 06:41:48 +0000 | `f5d80fc` — 2026-08-05 19:09:18 +0000 |
| canon/estado-programa-v1_10.md | `2131f04` — 2026-08-13 06:41:48 +0000 | `f5d80fc` — 2026-08-05 19:09:18 +0000 |
| tests/check.py | `4cc2131` — 2026-08-13 04:09:59 +0000 | `c9d37d8` — 2026-08-06 01:11:37 -0600 |

Las cuatro, en las seis ramas, son la misma versión (mismo SHA de último-toque, misma fecha 5-6/ago) — una semana o más detrás de la versión que `main` trae hoy. Confirma exacto lo que el encargo citaba para `gobernanza`/`.gitattributes` (`f5d80fc`/`b9d9dfc`, 5/ago) y lo extiende a `estado-programa-v1_10.md` y `tests/check.py`, verificado en las seis ramas, no solo en una. Consistente con "versiones viejas, no trabajo único" — no son estas cuatro las que probarían lo contrario; ver §2 de `forense/notas/2026-08-13-z-inventario-curador.md` y `forense/notas/2026-08-13-w-prima-inventario-clones.md` §3 para la adjudicación completa de por qué las seis se marcaron efímeras.

### D ≈ 247 — la firma de la purga del 10/ago, no borrados de la rama

Documentado ya, no re-derivado aquí: `forense/hallazgos.md` (entradas del 2026-08-10, ACTO CIERRA-164/ADR-66 y el cierre de PR #164) narra `PURGA-PRIVACIDAD`, un `--force --mirror` que reescribió historia el 10/ago. El artefacto de esa purga, `canon/remapeo-shas-purga-2026-08-10.tsv` (626 líneas), vive en el repo. Las seis ramas efímeras congelaron su base el 6/ago, **antes** de esa reescritura; `main` la absorbió y siguió creciendo. La cuenta D de la tabla de §1 mide "archivos que `main` tiene hoy y la rama no" — con `main` reescrito y extendido y la rama congelada en una base pre-reescritura, la mayoría de esa cuenta es exactamente esa brecha estructural, no contenido borrado por la rama. No se reinterpreta más allá de lo que ya está escrito en esas entradas de `hallazgos.md`.

---

## §2 · Qué es y qué no es un ref efímero

Un ref borrado deja de existir; su SHA no. Mientras el objeto viva en el reflog del servidor, el SHA anotado hace el borrado reversible. Este archivo no garantiza que el objeto siga existiendo — garantiza que sabes qué pedir.

Un ref efímero, en el sentido de este archivo, es una rama que la mesa decidió que puede borrarse (juzgada sin contenido único, o superada por trabajo que ya llegó a `main` por otra vía) pero cuyo SHA vale la pena anotar antes de borrarla, precisamente porque el juicio de "sin contenido único" puede estar equivocado, o alguien puede querer revisarlo después. No es una promesa de preservación — Git no promete cuánto tiempo vive un objeto inalcanzable en el reflog del servidor antes de una recolección de basura, y este archivo no controla ni conoce esa política. Es la diferencia entre "no se puede recuperar" (sin SHA, tras el borrado, el objeto es indistinguible de cualquier otro commit huérfano) y "se puede pedir, si todavía está" (con SHA, `git fetch origin <sha>` o un ticket de soporte tienen algo concreto que buscar).

## §3 · La ventana

Borrado autorizado a partir del 12/sep/2026 por decisión de mesa del 12-13/ago. Este acto no borra.

Esa decisión no vive, verificado por búsqueda dirigida de este acto, en ningún archivo de `forense/` previo a este — nace citable aquí, y en el encargo archivado que este acto ejecuta (`forense/encargos/2026-08-13-RE-registro-efimeros.md`), per la misma lógica de A.3: un texto que solo vive en conversación de mesa es invisible para el programa hasta que se commitea. A partir de este acto, la ventana del 12/sep es la que este archivo y ese encargo declaran.

## §4 · La regla de captura, para los que vengan

Antes de borrar cualquier ref: SHA de 40 caracteres, fecha del último commit, y las tres cifras de diff contra `main`. Tres minutos. Sin eso, el borrado es irreversible.

Receta mínima, una rama a la vez:

```bash
git rev-parse <rama>                                            # SHA de 40, no %h
git log -1 --format='%ci' <rama>                                # fecha del último commit
git diff --diff-filter=A --name-only origin/main <rama> | wc -l # A
git diff --diff-filter=M --name-only origin/main <rama> | wc -l # M
git diff --diff-filter=D --name-only origin/main <rama> | wc -l # D
```

Si A > 0: mirar qué archivos son antes de decidir nada — puede ser trabajo real. Si A = 0: no cerrar ahí solo por eso (§1, arriba) — mirar si M trae contenido distinto al de `main`, no solo versiones viejas. Anotar las cinco cifras en una fila de este archivo. Solo entonces borrar, y solo si la ventana de mesa ya abrió.

## §5 · El patrón que hace falsas las verificaciones

`cd` a un worktree hermano sin volver. El 13/ago un acto afirmó que `tools/curador_registro/produce.py` no existía en `19d885d`. Era falso: verificado de nuevo, independientemente, en este acto —

```bash
$ git cat-file -e 19d885d:tools/curador_registro/produce.py && echo EXISTE
EXISTE
$ git log --diff-filter=A --format='%h %ci %s' -- tools/curador_registro/produce.py | tail -1
59d6c40 2026-08-10 14:15:13 -0600 BARRIDO-COMPLETO (N1-N33): commit de preservación, cubeta (i)
```

— el archivo existía, y el único commit que lo añade en toda la historia es `59d6c40`. La causa reconstruida por el propio acto (`forense/hallazgos.md`, entrada "ACTO ENASIC-SPLIT, segunda corrección"; detalle completo en `forense/notas/2026-08-13-enasic-split-verificacion.md`, sección "SEGUNDA CORRECCIÓN"): hizo `cd /home/pc0/wt-abrir4-1786051186` para inspeccionar los commits de un worktree hermano y no volvió. Los `git ls-tree` posteriores corrieron contra ese directorio — HEAD `2895d5a` (6/ago, anterior a `59d6c40`, donde el archivo legítimamente no está, pero esa no era la pregunta). Devolvieron salida, sin error, así que se sintieron verificados. Y la adenda escrita para corregirlo fabricó una segunda afirmación falsa —que un acto concurrente los había "restaurado"— por inferir desde un diff sin verificar la inferencia.

Es primo del defecto del espejo que `instrucciones-proyecto` ya nombra (v2.1/v2.4: el espejo engaña porque es una copia vieja que parece el repo). Este patrón engaña por la razón contraria: es *el mismo repo*, exactamente donde se supone que hay que mirar, solo que en la rama equivocada — y el comando nunca falla. No hay excepción, código de salida ni mensaje que lo distinga de una consulta legítima. Contesta con salida limpia, bien formada, sobre la pregunta que nadie hizo.

**Contramedida, en una línea de ARRANQUE:** `pwd` antes de cualquier comando de estado del repositorio, y `git -C <ruta>` en vez de `cd` cuando haya que mirar otro árbol — no depende de recordar volver. Un `git ls-tree`/`git cat-file`/`ls` en el directorio equivocado no falla: contesta otra pregunta, con la misma confianza que si hubiera contestado la correcta. Segundo modo, casi siempre junto al primero: un `2>/dev/null` puesto por hábito sobre un comando de verificación silencia el error real (rama borrada tras merge, por ejemplo) y colapsa "no existe" con "no se pudo preguntar" en la misma salida vacía — no usar `2>/dev/null` en un comando de verificación de existencia sin haber mirado primero qué error, si alguno, se estaría silenciando.

**Nota sobre dónde vive esto ya:** este acto llegó a escribir esta sección después de verificar que `forense/hallazgos.md` ya trae, desde antes de que este acto empezara, una entrada con el mismo encuadre — "Patrón, no incidente" — commiteada como cierre del propio ACTO ENASIC-SPLIT (`4a0c363`, fusionado a `main` en el mismo PR #206 que trae `origin/main` a `959006a`). Esa entrada es más extensa que esta sección y ya cubre el segundo modo (`2>/dev/null`) y la contramedida. Esta sección no la duplica en `hallazgos.md` — el registro nuevo de ese hallazgo es la entrada que este acto sí añade ahí, y que apunta aquí y a `4a0c363` en vez de renarrar. Se deja esta sección en este archivo de todos modos porque su función es distinta: `hallazgos.md` es la bitácora cronológica del acto que lo encontró; este archivo es el sitio append-only, indexado por `NOMBRE ESTABLE`, donde un acto futuro que va a hacer `cd` a un worktree hermano puede encontrarlo *antes* de repetirlo — que es, literalmente, el contador que cierra este acto (§6, abajo).

---

## §6 · Contador

Refs con SHA capturado: **0 → 6** (tabla de §1). Y un patrón de falsa verificación escrito donde se lea antes de repetirlo — en dos sitios ahora: la bitácora (`forense/hallazgos.md`, `4a0c363` y la entrada que cierra este acto) y este registro estable (§5, arriba).

---

*Append-only. Nueva fila o nueva sección = nueva entrada, nunca edición de lo ya escrito salvo para llenar un campo de estado al cerrarlo. Este archivo no adjudica ni borra — registra.*
