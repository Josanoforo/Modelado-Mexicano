# ACTO CAJA-RESIDUOS — los tres residuos, adjudicados por medición; y la premisa de la compuerta, refutada

`PR #284` · `ADR-118` · Base: `origin/main` = `20c7dee` (`PR #283`) al numerar; `35c9c9f` al redactarse el encargo · Sesión **UBUNTU** · Modelo: Opus · Sin `--freeze`. **La caja no fue de dueña única — ver §4.**

Ejecuta lo que `ADR-113` §«Reportado, no tocado» nombró y declinó tocar, y lo que la nota de `PR #278` §8.2 cerró con *"Ninguna fila nueva"*.

## §0 · Arranque — el espejo del encargo estaba vencido en cinco cifras, y `origin/main` se movió dos veces

**Repo.** `/home/pc0/Modelado-Mexicano`, clon base, sin clones nuevos. Al arrancar: `470fa57` (`PR #277`), rama `main`, `git status` limpio, **4 commits detrás**.

**SHA.** El encargo se redactó contra `35c9c9f` (`PR #278`). Se movió, dos veces y durante el acto:

```
$ git fetch origin --prune && git log -1 --format='%h %s' origin/main
976b31d Merge pull request #282 ...      ← al arrancar (#279 FP57-DECLARA, #280 FUSION-PUERTAS, #282 FP10-PRECEDENCIA)
20c7dee Merge pull request #283 ...      ← antes de numerar  (#281 CORTE-EDAD, #283 REFUTACIONES-SIN-OBJETO)
$ git merge-base --is-ancestor 35c9c9f origin/main && echo ancestro
ancestro
```

`35c9c9f` verificado ancestro las dos veces. **No es PARO.**

**`data/raw`.** Este acto **no abre microdato**. El corpus no se toca: `data/raw` es un *symlink* a `/home/pc0/mm-corpus/raw` (284 entradas) y solo se leyó para la sonda `A.2`.

**Entorno (`A.2`, tres partes, valores crudos).** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **sin_variable** · sonda INEGI → **`200`** · `ls data/raw/ | head -1` → **`20260813130000.export.CSV.zip`**. `pgrep` de procesos del proyecto → **ninguno**, al arranque y al cierre — cifra correcta y conclusión equivocada: ver §4, `pgrep` no ve una sesión de agente concurrente. *(La primera corrida de `pgrep` se auto-emparejó con su propia línea de comando —el patrón `check.py` viajaba en el `eval`—; se repitió con un patrón que no se auto-captura. Se declara porque un `pgrep` que se cuenta a sí mismo es exactamente el falso positivo que haría creer que la caja no es de dueño único.)*

**Espejo — las cinco correcciones, todas re-derivadas del disco.**

| cifra del encargo | re-derivada | comando |
|---|---|---|
| `168 refs` en `mm-purga.git` | **167** | `for-each-ref`, `packed-refs` y `show-ref` dan 167; `show-ref --head` da 168 porque cuenta `HEAD`. `ref-map` trae 167 filas de datos. |
| `122 líneas` de `reconcilia-puertas` | **122 ✓** | `diff` de las dos notas: 122 líneas solo-en-rama. **Cifra correcta.** |
| `12M` / `25M` | **11.8 MB** / **34M al borrar** | `du -sb` da 11 814 155 B para el espejo. `mm-paso5` medía 25M al inventariarlo y **34M al borrarlo**: los 9M los añadió el `git fetch` que este acto corrió *dentro* de ese clon para verificar ancestría. Se declara para que no se lea como discrepancia de inventario. |
| `ABIERTAS = FP-26·57·58·60` | **FP-26·58·60** | `FP-57` pasó a `FIRMADA` con `ADR-114` (`PR #279`) antes del arranque. |
| `FUSION-PUERTAS` *"corriendo hoy en NUBE"* | **ya fusionada** | `PR #280`; cerró `FP-12` sin fusionar nada. |

**Verificación 2 del encargo, ejecutada (dirección declaró no haberla corrido).** `git ls-files | grep -iE "commit-map|ref-map"` → **cero**. Pero la pregunta de fondo —*¿los mapas de la purga ya están en el repo?*— tiene respuesta distinta y más interesante: ver §2.

## §1 · `F1` · `R3` — hecho visible, no adjudicado

Antes de empujar nada se verificó lo único que podía hacer ilegal el push: que la rama no colgara de ancestría pre-purga.

```
$ git merge-base origin/main reconcilia-puertas
fbe4e0a  (PR #204, 12/ago)   → verificado ancestro de origin/main
$ git rev-list --count origin/main..reconcilia-puertas
5                            → 9301e59 NO está entre ellos; intersección con los 599 viejos reescritos = 0
```

Push de rama, **sin merge**, y verificado en `ls-remote` y no en el texto del CLI:

```
$ git push origin reconcilia-puertas:rescate/reconcilia-puertas-local
 * [new branch]      reconcilia-puertas -> rescate/reconcilia-puertas-local
$ git ls-remote origin refs/heads/rescate/reconcilia-puertas-local
f169abd6c55c634d7392caa10602ab13fc2558fa    ← idéntico al sha local
```

**Contenido único, re-derivado y ampliado.** `ADR-113` citó 122 líneas ausentes de `main`; se confirma, y se añade la mitad que ese ADR no midió:

| | nota de `main` | nota de la rama |
|---|---:|---:|
| líneas | 191 | 165 |
| `sha256` | `05de81dc…` | `49e9f31d…` |
| líneas ausentes de la otra | 148 | 122 |

No es un superconjunto en ninguna dirección: **son dos ejecuciones distintas del mismo encargo**, la de `main` hecha en la nube (`PR #208`). Más **1 línea de `forense/hallazgos.md` verificada ausente de `main`** (`grep` = 0). Worktree retirado tras el push verificado; la rama local se conserva. La adjudicación de contenido no era de este acto: **`FP-62`**.

## §2 · `F2` · `R1` — los artefactos a salvo, la compuerta respetada, y la premisa refutada

### (a) Los seis artefactos, verbatim

Se copió el directorio `filter-repo/` **completo** —los seis, no los dos que el encargo nombra— porque bajo firma `F2(c)` destruiría la única copia de los otros cuatro, y *"los seis, verbatim"* es regla más auditable que *"dos, por criterio del ejecutor"*. **6 de 6 byte-idénticos**, `sha256` en `MANIFIESTO-PURGA.tsv`. Commit **`0a90cc8`**.

**Forma verificada por `awk`, no descrita:** `commit-map` → 603 líneas conformes `sha40 sha40`, **0 anómalas**. `ref-map` → 167 conformes `sha40 sha40 refs/…`, **0 anómalas**; sus únicos nombres de ref fuera de `refs/pull/` son `refs/heads/main` y `refs/heads/codex/barrido-completo-n1-n33`. `changed-refs` → 167 conformes.

**Compuerta PII patrón `PR #274`, cinco ángulos.** Cabeceras/llaves con `nombre|apellido|curp|rfc|teléfono|correo|email`: **0 archivos**. `CURP`-shaped: **0**. `RFC`-shaped: **0**. Email: **0**. Teléfono 10 dígitos: **1 archivo** — `suboptimal-issues`. Adjudicado **uno por uno y no por conteo**: son **11 marcas epoch del 6/ago/2026** (`1786051186` → `2026-08-06 21:19:46 UTC`, verificado con `date -d @`) que `filter-repo` listó como *"referencias a hashes ahora inexistentes"* en su propio encabezado — los dígitos decimales son hex válido, así que su heurística las tomó por hashes abreviados. Mismo criterio que `ADR-113(c)` usó con el mismo número. **Compuerta limpia.**

### (b) La verificación 2 del encargo, respondida: `commit-map` **ya estaba en el repo, al 100 %**

```
canon/remapeo-shas-purga-2026-08-10.tsv   vs   filter-repo/commit-map
  pares en cada uno:      603  /  603
  intersección:           603
  solo en commit-map:       0
  solo en canon:            0
```

El canon lo tiene con una columna extra (`cambio`) y encabezado en comentarios; los pares son los mismos. **De los seis artefactos, `ref-map` es el único cuyo contenido no existía ya en el repositorio.** `commit-map` se conserva en su forma cruda por ser contra la que un auditor externo diffea, no por añadir información — y eso queda escrito en `forense/purga-privacidad/LEEME.md` para que nadie lo cite como fuente independiente.

### (c) ⛔ La compuerta de firma NO se abrió

El encargo exige la cadena verbatim `AUTORIZO DESTRUIR mm-purga.git` en el mensaje de mesa. **El lanzamiento no la trae.** Su única aparición está dentro de la definición de la propia compuerta —*"Solo procede si el launcher/mensaje de mesa trae la firma verbatim: …"*—, que es **la especificación citándose a sí misma**: el mismo *autocaptura verbatim* que `T22` ya reconoce en media docena de notas del proyecto (`TABLERO-FIRMAS`, `CI-CATEGORIA`, `SELLO-FICHA-G3`, `NOTAS-P3`). Tomarla por firma habría destruido un artefacto irreversiblemente bajo una firma que nadie dio.

**`F2(c)` no se ejecuta. `~/mm-purga.git` queda intacto.** Como el encargo dice: eso NO es fracaso.

### (d) Y la premisa que justificaba la compuerta es falsa

`ADR-113`, la nota de `PR #278` §6 y el encargo coinciden: el espejo *"conserva historia pre-purga"*, *"contiene `9301e59`: el estado del repositorio anterior a la purga, es decir el que todavía tiene las 1,737 filas de datos personales"*, y es *"el vector de resurrección"*. Medido:

```
(i)   refs del espejo → shas NUEVOS
      $ git -C ~/mm-purga.git rev-parse refs/heads/main
      ed46c26...   ← exactamente la columna `new` de ref-map (old era 47210df)

(ii)  los 599 commits viejos reescritos, barrido completo (no muestra)
      $ awk 'NR>1 && $1!=$2 {print $1}' commit-map | git -C ~/mm-purga.git cat-file --batch-check
      PRESENTES como commit: 0    AUSENTES: 599

(iii) $ git -C ~/mm-purga.git fsck --unreachable --dangling   → 0 líneas
      $ git -C ~/mm-purga.git count-objects -vH
      count: 0 · in-pack: 3053 · prune-packable: 0 · garbage: 0
      objects/info/alternates → no existe ·  logs/ (reflogs) → no existe

(iv)  9301e59 — los 4 que filter-repo dejó SIN CAMBIO
      old == new en commit-map, y `cambio=NO` en el canon: los MISMOS 4
      $ git merge-base --is-ancestor 9301e59 origin/main  → SÍ, ya es público

(v)   3 053 objetos del espejo; 20 no están en el remote-tracking del clon base
      los 5 commits → alcanzables desde refs/pull/{85,87,137,138,164} de GitHub
      los 6 blobs   → 0 líneas con patrón de dato personal
```

`filter-repo` expiró y recolectó los originales, como hace por omisión. El patrón `/mnt/c/Users/…/Descargas MX` que sí aparece en el espejo es **la raíz declarada del proyecto**, viva hoy en `main` (52 líneas en 26 archivos trackeados), no el censo purgado.

**Refutar la justificación de una compuerta no la levanta.** La compuerta es de mesa; el ejecutor midió su premisa, la reporta y se detiene igual. **`FP-63`** sube la decisión con los hechos corregidos, para que mesa firme sobre lo medido.

## §3 · `F3` · `R2` — podado, con las dos verificaciones pegadas

```
$ git -C ~/mm-paso5 rev-parse HEAD
f42049866412973f5ac906b4757cb0a2621eb9db
$ git -C ~/mm-paso5 merge-base --is-ancestor HEAD origin/main && echo SI
SI — HEAD es ancestro de origin/main (976b31d)

$ git -C ~/mm-paso5 status --porcelain
[fin de la salida: 0 líneas — vacío]
```

Redes adicionales que el encargo no pedía, por ser un borrado irreversible: **0** entradas de `stash` · **0** commits sin empujar en ninguna rama (`log --branches --not --remotes`) · **0** tags locales ausentes de `origin` · **0** no-trackeados con `-uall` · ningún worktree colgando de ese clon.

**El primer `rm -rf` falló, y el diagnóstico no era el esperado.** Devolvió `Device or resource busy` sobre `.git/config` — el mismo texto que este equipo ya había dado por contención de `git config` entre worktrees. **No era eso:**

```
$ grep mm-paso5 /proc/mounts
/dev/sdd /home/pc0/mm-paso5             ext4 rw,...
/dev/sdd /home/pc0/mm-paso5/.git        ext4 rw,...
/dev/sdd /home/pc0/mm-paso5/.git/config ext4 ro,...   ← bind-mount de SOLO LECTURA
$ fuser -v /home/pc0/mm-paso5/.git/config
                     root     kernel mount /home/pc0/mm-paso5/.git/config
```

Es el *sandbox* del entorno de ejecución, que bind-montea todo `.git/config` como solo-lectura; el archivo no se puede desenlazar porque es un punto de montaje del kernel. Repetido fuera del sandbox: borrado limpio. **Se deja escrito porque el diagnóstico heredado —contención de git— habría llevado a matar procesos que no existían**, y este proyecto ya pagó una vez el costo de un `pkill` mal dirigido.

```
$ ls -d /home/pc0/mm-paso5
ls: cannot access '/home/pc0/mm-paso5': No such file or directory
```

## §4 · Estado final

```
$ git worktree list
/home/pc0/Modelado-Mexicano            [caja-residuos]   ← clon base, este acto
/home/pc0/Modelado-Mexicano-barrido2   387ad82 [cond-atrib]   ← corpus, solo lectura
/home/pc0/mm-coef-universo             35c9c9f [coef-universo]
/home/pc0/mm-limpia-caja               e7ed4b8 [limpia-caja]

$ ls -d ~/mm* ~/Modelado-Mexicano*
Modelado-Mexicano · Modelado-Mexicano-barrido2 · mm-coef-universo · mm-corpus · mm-limpia-caja · mm-purga.git

$ df -h /home/pc0
/dev/sdd  1007G  35G  922G  4%
```

**Worktrees: 5 → 4. Directorios del proyecto: 7 → 6.** `mm-reconcilia-puertas` (62M) y `mm-paso5` (34M) fuera; `mm-purga.git` (12M) intacto por diseño.

**La caja NO fue de dueña única — y el instrumento con que este proyecto lo comprueba no puede verlo.**

El encargo declara: *"Corre DESPUÉS de COEF-UNIVERSO (dueña única; COEF está en la caja ahora)"*. Al arrancar se verificó, y la precondición parecía no cumplirse por el otro lado:

```
$ git -C ~/mm-coef-universo log -1 --format='%h'   → 35c9c9f   (= origin/main de #278, sin commits propios)
$ git -C ~/mm-coef-universo status --porcelain     → 0 líneas
$ git ls-remote origin refs/heads/coef-universo    → vacío   ·   gh pr list → sin PR
$ pgrep de procesos del proyecto                    → ninguno
```

`COEF-UNIVERSO` **no había corrido**. Con eso —y con el propósito de la cláusula, dueña única, aparentemente satisfecho— el acto siguió. **Al cerrar, la lectura se invierte:**

```
$ git reflog show coef-universo
eb8b8e1 coef-universo@{0}: commit: ACTO COEF-UNIVERSO COMMIT 1: encargo archivado, nota (0-6), coef-universo-v1_0.tsv ...
20c7dee coef-universo@{1}: merge origin/main: Fast-forward
35c9c9f coef-universo@{2}: branch: Created from origin/main
$ git log -1 --format='%ad' eb8b8e1 --date=iso    → 2026-08-18 22:47:36 -0600
```

Esa sesión **arrancó durante este acto** y commiteó a las 22:47:36. Las dos corrieron en paralelo — exactamente lo que la cláusula de precedencia existía para impedir.

**El hallazgo metodológico, que vale más que el incidente: `pgrep` no es instrumento suficiente para «dueña única».** Detecta procesos largos; no ve una sesión de agente que ejecuta órdenes de `git` de segundos y espera. El `pgrep` del cierre volvió a dar **cero** *mientras la otra sesión ya tenía un commit en el árbol*. El único instrumento que la vio fue **`git reflog show <rama>`** sobre los worktrees de la caja, y se propone como el chequeo de dueña única a partir de aquí — barato, y mide rastro en vez de presencia.

**Interferencia observada: ninguna.** El `COMMIT 1` de `COEF-UNIVERSO` no toca **ninguno** de los cuatro archivos compartidos (`forense/firmas-pendientes.tsv`, `canon/gobernanza-v1_15.md`, `forense/hallazgos.md`, `canon/estado-programa-v1_10.md`) — verificado por `git show --name-only` — y su worktree quedó limpio; los perímetros de disco son disjuntos. **Colisión esperada, todavía no ocurrida:** su commit de cierre necesitará número de `ADR` y probablemente filas de tablero, así que **quien fusione segundo renumera**, protocolo ya establecido y ejercido tres veces esta misma jornada (`ADR-114`→`115`→`116`).

**Y el otro worktree que nadie nombra:** `mm-limpia-caja` (`e7ed4b8`), el worktree del propio `ACTO LIMPIA-CAJA`, cuya rama ya fusionó en `PR #278`. Podable, pero fuera del perímetro de este encargo: se reporta, no se toca — misma disciplina que `ADR-113` §6 aplicó a los tres residuos de hoy.

## §5 · Cierre

1. **Dos filas abiertas, ninguna cerrada.** `FP-62` (contenido de `reconcilia-puertas-local`) y `FP-63` (destino del espejo). Máximo del tablero re-derivado **al escribir y otra vez tras fusionar** — `PR #283` tomó el `FP-61` mientras este acto corría —, a re-derivar de nuevo al fusionar este PR.
2. **`ADR` re-derivado igual**, receta `T15`: únicos `118` · máx `118` · huecos `[]`. Cascada de `T15` a tres sitios (`estado:27`, `estado:101`, `gobernanza:2`), los únicos que no exime `{cita-historica}`.
3. **Cascada de `T16`, y una decisión pequeña que no es cosmética.** Las dos filas nuevas suben `T22` de 5 a 7 WARN y el total de 118 a **120**; recifrados `estado:204` y `estado:296`. Pero `:296` traía una **segunda cita interna** —*«Fusionado: **21 FAIL · 118 WARN** — neto de las dos causas»*, de `ACTO REFUTACIONES-SIN-OBJETO`— que **era cierta cuando se escribió** y que `T16` empezó a marcar `FAIL` sólo porque la cifra vigente se movió. Se **marcó `{cita-historica}`** (mecanismo de `ADR-90`) en vez de sobrescribirla hacia adelante. Sobrescribir es justo la conducta que `FP-52` tiene abierta sobre cinco narraciones de `gobernanza` reescritas entre 7 y 17 veces cada una para mantener `T16` verde; este acto declina añadir la sexta. Es el primer `{cita-historica}` de `estado-programa-v1_10.md`.
4. **Corrida final: `21 FAIL · 120 WARN` · `LÍNEA BASE: VERDE`**, sin `--freeze` —prohibido por el encargo— y `tests/baseline.json` verificado sin tocar (`git status --porcelain -- tests/` vacío). Una entrada de la línea base dejó de aparecer (mejora); no se bajó la cifra congelada.
5. **Desviación declarada — la fila de `R1` es `ABIERTA`, no `FIRMADA-PENDIENTE-EJECUCIÓN`.** El encargo pide ese valor compuesto. No se usa: (i) `FIRMADA` afirmaría una firma de mesa que **no existe** —es justo lo que `F2(b)` acaba de constatar que falta—, y (ii) `T22` compara `estado` por **igualdad exacta** de cadena (`(a)` con `ABIERTA`, `(c)` con `FIRMADA`), así que un cuarto valor compuesto **no dispararía ninguna de las dos** y la fila quedaría invisible para la memoria mecánica — el limbo que la firma de mesa que fundó el tablero mandó cerrar. El vocabulario vigente, re-derivado, tiene exactamente tres valores.
6. **Extensión de perímetro declarada:** se copiaron los **seis** artefactos de `filter-repo/`, no los dos nombrados. Todos dentro de `forense/purga-privacidad/`, que sí está en el perímetro; el razonamiento está en `(a)`.
7. **Lo que este acto NO hizo:** no adjudicó el contenido de `reconcilia-puertas`, no fusionó su rama, no destruyó el espejo, no tocó `mm-corpus/`, `mm-coef-universo`, `mm-limpia-caja` ni `Modelado-Mexicano-barrido2`, y no re-adjudicó `ADR-113` — corrigió un hecho que ese ADR afirmó sin medir.
8. **Contadores de medición sobre México que mueve este acto: 0.** Es higiene de entorno y privacidad; no midió ninguna hipótesis del programa.

`encargo` → `CONSUMIDO`.
