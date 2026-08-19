# ACTO FP63-CIERRA — la afirmación falsa de `ADR-113`, corregida; el espejo, re-verificado en fresco y **no destruido**

**Estampa de universo (`A.10`).** SHA: **`e25f2bd`** (`origin/main` al arrancar y al cerrar; re-derivado, no heredado — el encargo lo declaraba y coincidió). Universo: **el espejo `~/mm-purga.git` completo** (3,053 objetos · 167 refs · 6 artefactos `filter-repo/`), barrido entero y no por muestra; más el árbol trackeado de `e25f2bd` (1,702 archivos) para el rastreo de la cifra `1,737`. Denominador: existe, y son esas tres cifras. Fecha: **19/ago/2026**.

**Mecanismo de toda búsqueda negativa, declarado antes de usarlo.** `command grep`, **nunca** el `grep` de esta caja: aquí `grep` es una **función** que envuelve `ugrep -I --exclude-dir=.git` (`type grep`, pegado en §0), y `-I` descarta en silencio cualquier archivo con un byte no-UTF8. Ningún `NO-ENCONTRADO` de esta nota se declara sin su mecanismo y su control positivo — ver §5, donde un negativo estuvo a punto de reportarse sin haber examinado un solo archivo.

**Resultado en una línea:** los tres bloques de la re-verificación coinciden **sin una sola diferencia** con lo que `FP-63` registró, la compuerta de firma **no** se abrió (segunda vez, misma razón), y `~/mm-purga.git` **sigue intacto**. `ADR-122` corrige a `ADR-113` sin tocarlo.

---

## §0 · Arranque

```
$ pwd; git log -1 --oneline; git status --short
/home/pc0/Modelado-Mexicano
4281688 Merge pull request #284 from Josanoforo/caja-residuos
[fin de la salida: 0 líneas — árbol limpio]

$ git fetch origin --prune; git log --oneline -1 origin/main
 - [deleted]  (none) -> origin/claude/doc-backfill-launcher-nube-co5qiy
 - [deleted]  (none) -> origin/claude/u2-ev1-external-validation-szb9wl
   4f39912..e25f2bd  main -> origin/main
e25f2bd Merge pull request #289 from Josanoforo/claude/u2-ev1-external-validation-szb9wl
```

**El SHA del encargo (`e25f2bd`) es el `origin/main` real de hoy — coincide, re-derivado.** El clon principal estaba dos merges atrás (`4281688`); se sincronizó por `--ff-only` antes de nada.

**Dueña única.** `pgrep -af claude` devuelve **solo el propio shell de esta sesión** — y ese instrumento **no basta y se dice**: este proyecto ya midió que `pgrep` no ve una sesión de agente concurrente. La verificación real es `git worktree list` (5 worktrees, todos de actos ya cerrados o de este mismo turno) más `git reflog`, cuya última entrada ajena es del 18/ago 23:07. Las dos ramas que corrían en nube al lanzarse el acto anterior (`DOC-BACKFILL`, `U2-EV1`) **están fusionadas y sus ramas remotas borradas** — visible en el `fetch` de arriba. Caja libre.

**A.2, las tres partes, crudas.**

```
(1) variable de entorno
    CLAUDE_ENV=[<vacía>]  CLAUDE_CODE_ENV=[<vacía>]  HOSTNAME=[FF-5563]  USER=[pc0]
    Linux FF-5563 6.18.33.2-microsoft-standard-WSL2 ... x86_64 GNU/Linux

(2) sonda INEGI
    $ curl -sS -o /dev/null -w "http=%{http_code} tiempo=%{time_total}s ip=%{remote_ip}\n" \
        --max-time 25 https://www.inegi.org.mx/
    http=200 tiempo=0.664125s ip=127.0.0.1

(3) $ ls data/raw/ | head -1
    20260813130000.export.CSV.zip
```

**`data/raw`: no se abre microdato.** El único contacto con él es el symlink del worktree al corpus compartido (`data/raw -> /home/pc0/mm-corpus/raw`) para que la suite corra igual que en cualquier otro acto, y el `ls` de arriba que el propio arranque pide. **Ningún ZIP se abrió. El corpus no se toca.**

**`type grep` — el instrumento de esta caja, pegado porque gobierna §5:**

```
$ type grep
grep is a function
grep () { ... exec -a ugrep "$_cc_bin" -G --ignore-files --hidden -I \
          --exclude-dir=.git --exclude-dir=.svn ... }
```

**Espejo del proyecto: ninguno.** Toda cifra de abajo se re-deriva del disco, con el comando a la vista.

---

## §1 · `T2` · Re-verificación en fresco — el trío del encargo, crudo

Corrida **antes** de tocar nada, `2026-08-19T15:58:02Z`.

### (a) Identidad del espejo

```
$ ls -ld ~/mm-purga.git ; du -sh ~/mm-purga.git
drwxr-xr-x 8 pc0 pc0 4096 Aug 10 15:21 /home/pc0/mm-purga.git
12M	/home/pc0/mm-purga.git

$ git -C ~/mm-purga.git rev-parse HEAD refs/heads/main
ed46c26abd8513f18a5c097822f32e6ced88d3d4
ed46c26abd8513f18a5c097822f32e6ced88d3d4
```

`ed46c26` es exactamente la columna `new` de `ref-map` para `refs/heads/main` — el sha **posterior** a la purga, no el anterior (`47210df`).

### (b) `fsck --unreachable --dangling` · `count-objects` · reflogs · alternates

```
$ git -C ~/mm-purga.git fsck --unreachable --dangling
[fin de la salida: 0 líneas]

$ git -C ~/mm-purga.git count-objects -vH
count: 0
size: 0 bytes
in-pack: 3053
packs: 1
size-pack: 11.09 MiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes

$ ls -l ~/mm-purga.git/objects/info/alternates
ls: cannot access '...': No such file or directory
$ ls -ld ~/mm-purga.git/logs
ls: cannot access '...': No such file or directory
```

**Idéntico a lo que `FP-63` registró**, celda por celda: 0 líneas de `fsck`, 0 sueltos, 0 `garbage`, 0 `prune-packable`, 3,053 en pack, sin reflogs y sin `alternates`.

### (c) Conteo de refs vs. `ref-map` — barrido completo, no conteo

```
$ git -C ~/mm-purga.git for-each-ref | wc -l         → 167
$ wc -l < forense/purga-privacidad/filter-repo/ref-map → 168
```

**La diferencia de uno está resuelta, no glosada:** la línea 1 de `ref-map` es el **encabezado** (`old  new  ref`), única línea no conforme al patrón `sha40 sha40 refs/…` — `command grep -cvE` sobre el archivo da exactamente **1**. 168 = 1 encabezado + **167** filas de datos, que es la cifra que `FP-63` registró.

Y la comparación que importa no es el conteo sino la **dirección**:

```
   refs del disco:              167
   coinciden disco == NEW:      167
   coinciden disco == OLD:        0
   en disco y NO en NEW:          0
```

**Las 167 refs apuntan al sha NUEVO. Ninguna al viejo.**

### (d) Los 599 commits reescritos — barrido completo

```
$ awk 'NR>1 && $1!=$2 {print $1}' .../commit-map | git -C ~/mm-purga.git cat-file --batch-check
-- pares en commit-map (sin encabezado): 603
-- de ellos old != new (reescritos):     599
-- de ellos old == new (sin cambio):       4
-- PRESENTES como commit: 0
-- AUSENTES (missing):  599
0076d3ce1cd18c40241791b19ebf24284d8cb7c0 missing
00f51ff92c0e9f155e927ad470c2256c12967ff2 missing
015af3a65ec3b62205f9931a2d1d964467b1e1e3 missing
```

### (e) `9301e59` — uno de los cuatro `old == new`

```
$ awk 'NR>1 && $1==$2 {print $1}' .../commit-map
09bfb0597648fc388adbd5432690fb146af9f08f
231ea7b2384eddd47d2388dc4a5ef417529721f9
343d589811b0434e12da5ca445d424775ff7143b
9301e59203b01243e76fe2de47eaad93667a9514

$ git merge-base --is-ancestor 9301e59 origin/main && echo SI
SI (ya público)
```

### (f) Los 6 artefactos — byte-idénticos, con `sha256` contra el manifiesto sellado

```
   already_ran            89ec7d62…0c00   IDENTICO
   changed-refs           dcf85936…1dde   IDENTICO
   commit-map             756e9a91…3c2b   IDENTICO
   first-changed-commits  3200188c…24de   IDENTICO
   ref-map                142d59b2…5c15   IDENTICO
   suboptimal-issues      f7bae299…e4b2   IDENTICO
-- byte-idénticos (cmp -s): 6 de 6
```

Los seis `sha256` coinciden además, uno a uno, con los que `forense/purga-privacidad/MANIFIESTO-PURGA.tsv` selló en **`0a90cc8`**.

> ### ✅ Veredicto de `T2`: **nada difiere de lo que `FP-63` registró.** No hay PARO. La fila no se re-abre; se ejecuta lo que el encargo ordena para el caso de coincidencia.

---

## §2 · La medición nueva que cierra el caso sin depender de ningún patrón

`FP-63` había medido el espejo contra el **remote-tracking** del clon base y encontró 20 objetos no presentes, de los cuales 6 blobs con 0 líneas de dato personal. Este acto lo mide contra el **almacén de objetos completo** del clon base — denominador más estricto, y `origin/main` avanzó desde entonces:

```
$ git -C ~/mm-purga.git cat-file --batch-check --batch-all-objects --unordered | awk '{print $1}' \
    | git -C /home/pc0/Modelado-Mexicano cat-file --batch-check
-- objetos en el espejo:      3053
-- presentes en el clon base: 3047
-- SOLO en el espejo:            6

$ git -C ~/mm-purga.git cat-file --batch-check < solo_espejo.txt | sort -k2
20342597…  commit 1233   "Encargo T: sella cruce catálogo × fichas del Hito D…"  ← refs/pull/87/head
8e34849f…  commit  250   "Delete forense/cruce-catalogo-fichas-v1_0.md"          ← refs/pull/138/head
d43ee532…  commit  250   "Delete forense/cruce-catalogo-fichas-v1_0.md"          ← refs/pull/137/head
d341411b…  commit  347   "Merge 59d6c40f… into ed46c26…"                          ← refs/pull/164/merge
4074dcfc…  commit 3572   "Hito D: adjudicar R5.1 a veredicto A (ADR-55)…"        ← refs/pull/85/head
5b1fa9cc…  tree   1059   (árbol raíz del merge de PR #164)

$ ... | awk '$2=="blob"' | wc -l
0
```

> ### ⚠️ **CERO blobs viven solo en el espejo.**
>
> Los 5 commits exclusivos son los **mismos cinco** que `FP-63` identificó, colgando de `refs/pull/{85, 87, 137, 138, 164}` de GitHub. El único objeto adicional es un **tree** — el árbol raíz del merge de `PR #164` —, y todas sus entradas son blobs y trees que el clon base ya tiene.
>
> **La consecuencia es la que cierra el asunto, y no depende de qué patrón de dato personal se busque:** el espejo **no contiene ningún contenido de archivo** que el clon público no tenga ya. No hay dónde alojar 1,737 filas de datos personales que no estén también en `main`.

*(Barrido de patrones sobre los 1,081 blobs del pack, corrido igualmente: 0 CURP-shaped, 0 RFC-shaped, y hits de email / 10-dígitos / cabeceras que —por lo anterior— están **todos** en contenido que el clon base ya tiene. Se anota que se corrió; no se usa como argumento, porque el argumento estructural de arriba es más fuerte y no depende de la calibración de ningún patrón.)*

---

## §3 · `T1` · La afirmación de `ADR-113`, partida en tres

Texto citado verbatim (`canon/gobernanza-v1_15.md:2208`), bajo el rótulo *"Reportado, no tocado, **por estar fuera de perímetro**"*:

> *"`~/mm-purga.git` (12M, espejo bare de `PURGA-PRIVACIDAD` con sus artefactos `filter-repo/`) **conserva historia pre-purga** (`9301e59`) — es decir, el estado del repositorio que todavía contiene las 1,737 filas de datos personales que la purga retiró de lo público."*

| fragmento | veredicto | evidencia |
|---|---|---|
| *"12M … con sus artefactos `filter-repo/`"* | **CIERTO** | §1(a) y §1(f) |
| *"conserva historia pre-purga (`9301e59`)"* | **FALSO como está escrito** | §1(d) y §1(e): la historia pre-purga real son los 599 `old != new`, **599 de 599 ausentes**; `9301e59` es uno de los 4 `old == new` y **ya es ancestro de `origin/main`** |
| *"todavía contiene las 1,737 filas de datos personales"* | **FALSO** | §1(b) y **§2**: 0 inalcanzables, 0 reflogs, 0 `garbage`, y **0 blobs exclusivos** |

**Clasificación (`ADR-122(b)`): `AFIRMACIÓN HEREDADA SIN UNIVERSO PROPIO` — caso degenerado del Corolario 2 de `A.10`.** No es `VENCIDO EN ALCANCE`: ese estado es para un sello correcto cuyo universo creció por debajo, y aquí el universo **no creció** — `filter-repo` corrió el 10/ago y el espejo tenía el 19/ago el mismo contenido que hoy. La afirmación **nació falsa**. Y no es el Corolario 2 en su forma típica porque `ADR-113` **no declara universo alguno** para esa frase: la escribe explícitamente *fuera de perímetro*, sin medirla. Universo declarado = ∅, y toda conclusión es más ancha que ∅.

**El original no se toca** — patrón `ADR-112` → `ADR-110(d)`: la corrección vive en un ADR nuevo que cita, clasifica y mide. Borrar el texto destruiría la prueba de qué se creía y con qué alcance.

---

## §4 · La cifra `1,737` no tiene derivación en el árbol — universo y mecanismo declarados

```
$ command grep -rln --exclude-dir=.git "1,737" .     # 1,702 archivos trackeados en e25f2bd
./canon/gobernanza-v1_15.md                                  (ADR-113, y la cita de ADR-120(d))
./forense/encargos/2026-08-18-RESCATE-CURADOR.md
./forense/encargos/2026-08-19-CAJA-RESIDUOS.md
./forense/firmas-pendientes.tsv                              (FP-63)
./forense/hallazgos.md
./forense/notas/2026-08-18-rescate-curador-cierre.md
./forense/notas/2026-08-19-caja-residuos-cierre.md
./forense/notas/2026-08-19-limpia-caja-cierre.md
```

**Las ocho son citas. Ninguna deriva el número.** La más antigua del árbol (`RESCATE-CURADOR`, 18/ago) ya lo afirma sin derivarlo. El acto que lo produciría, `PURGA-PRIVACIDAD` (10/ago), **no tiene registro propio en el árbol**: de él viven solo sus artefactos (`forense/purga-privacidad/`) y sus dos TSV de canon (`remapeo-shas-purga`, `citas-sha-obsoletas-purga`) — verificado con `git ls-files | command grep -i purga`.

**Lo que esto establece y lo que no.** Establece que **el árbol no puede verificar el conteo**. **No** establece que la purga no retirara filas personales de lo público: eso ocurrió, y sus artefactos lo prueban. Lo refutado es **dónde están hoy** —§2: en ninguna parte del espejo—, no **que hayan existido**.

---

## §5 · Hallazgo de método: `xargs -0 command grep` devuelve VACÍO, no error legible

El primer barrido de §4 se escribió así, y devolvió **cero archivos**:

```
$ git ls-files -z | xargs -0 command grep -ln "1,737"
-- fin de la lista --            ← creíble, y completamente falso
```

El control positivo lo destapó:

```
$ command grep -c "1,737" canon/gobernanza-v1_15.md
2                                 ← hay coincidencias, y el barrido decía que no

$ git ls-files -z | xargs -0 command grep -ln "1,737" ; echo "exit=$?"
xargs: command: Permission denied
exit=126
```

**`command` es un builtin de shell**: `xargs` intenta ejecutarlo como binario y falla — sin una sola línea en `stdout`. Es un modo de falla **distinto** del ya registrado para el `grep` de esta caja (`ugrep -I`, que tira archivos no-UTF8 en silencio) y **peor en un sentido**: aquí no se examina **ningún** archivo, y el resultado se ve idéntico a *"no hay coincidencias"*.

**Regla operable que este acto deja escrita:** todo negativo que vaya a declararse se corre **con su control positivo al lado** —una cadena que se sabe presente— y con el `exit code` a la vista. Sin control, un `NO-ENCONTRADO` no es un hallazgo: es un comando que no corrió.

---

## §6 · `T3` · ⛔ La compuerta NO se abrió — segunda vez, misma razón

El encargo exige la cadena verbatim `AUTORIZO DESTRUIR mm-purga.git` en el mensaje de lanzamiento. **El lanzamiento no la trae como autorización.** Su única aparición está **dentro de la definición de la propia compuerta** — *"destruyes SOLO si el mensaje de lanzamiento trae la cadena verbatim …"* —, que es la **especificación citándose a sí misma**: el mismo *autocaptura verbatim* que `T22` ya reconoce en media docena de notas del proyecto, y que `ACTO CAJA-RESIDUOS` adjudicó **exactamente igual el día anterior, sobre esta misma compuerta**.

Tomar la definición por firma habría destruido un artefacto **irreversiblemente** bajo una autorización que nadie dio. Que la razón de la destrucción ya no sea peligro sino redundancia **no cambia la irreversibilidad**, que es lo que la compuerta protege.

**`~/mm-purga.git` queda intacto.** Como el encargo dice: **eso no es fracaso**.

**Estado de la fila.** El encargo nombra el token `FIRMADA-PENDIENTE-EJECUCIÓN`. **No se escribe literal**, con la razón en `ADR-122(g)`: el tablero tiene tres valores (`FIRMADA` 51 · `CERRADA` 8 · `ABIERTA` 7) y `T22` vigila exactamente dos condiciones — fila `ABIERTA`, y fila `FIRMADA` con `ejecutada_en` vacía. Un token nuevo no cae en ninguna, y `FP-63` habría quedado **muda en cada corrida**: el limbo silencioso contra el que va la firma de mesa que creó el tablero. Se implementa en el vocabulario que la máquina ya entiende y que dice lo mismo: **`estado=FIRMADA`** (la decisión está tomada) **+ `ejecutada_en` vacía** (no se ha ejecutado), que `T22(c)` imprime como *«`FP-63` FIRMADA sin ejecutar desde 2026-08-19»*. Verificado: `T22` sigue con **9 señales** = 7 `ABIERTA` + 2 `FIRMADA` sin ejecutar, `FP-63` entre ellas.

---

## §7 · `T4` · Vacío por su propia condición: `~/mm-paso5` ya no existe

```
$ ls -ld ~/mm-paso5
ls: cannot access '/home/pc0/mm-paso5': No such file or directory
```

El encargo lo pedía *"de paso y **solo si sigue existiendo**"*. **No existe:** `ACTO CAJA-RESIDUOS` (`PR #284`, `ADR-120(c)`) lo podó el día anterior con su doble verificación pegada — `HEAD` `f420498` ancestro de `origin/main`, `status --porcelain` de 0 líneas — más cuatro redes que aquel encargo no pedía (0 `stash`, 0 commits sin empujar, 0 tags locales ausentes de `origin`, 0 no-trackeados con `-uall`). **La condición no se cumple: nada que destruir, nada que re-derivar.** Se anota porque el encargo lo nombraba como si pudiera seguir vivo — herencia menor de un estado superado el día anterior, del mismo tipo que este acto corrige a mayor escala.

---

## §8 · Estado final · lo que se tocó y lo que no

| | |
|---|---|
| **En disco** | **Nada destruido.** `~/mm-purga.git` intacto por compuerta; `~/mm-paso5` ya inexistente |
| **`canon/gobernanza-v1_15.md`** | `ADR-122` (nuevo) + cabecera de conteo **121 → 122**, derivada por `T15` |
| **`canon/estado-programa-v1_10.md`** | **Solo** el contador de ADR. La suite **no se recifra**: sigue en **21 FAIL · 122 WARN** |
| **`forense/firmas-pendientes.tsv`** | Solo `FP-63`: `ABIERTA` → `FIRMADA` con `ejecutada_en` vacía |
| **`forense/hallazgos.md`** | Dos líneas |
| **`forense/encargos/2026-08-19-FP63-CIERRA.md`** | Archivado y `CONSUMIDO` en el mismo acto (`A.3`) |
| **NO se tocó** | `data/`, `milpa/`, `corpus/`, `tests/`, `instrucciones-proyecto`, `README.md`, el corpus `~/mm-corpus/`, y el texto de `ADR-113` |

**Colisión de numeración declarada, no descubierta al fusionar.** `PR #290` (`ACTO FICHA-R51-D3`, abierto al escribir esto) ya reclama `ADR-122` en su rama; el máximo en `origin/main` es `121`, así que **ambos nacen `122` y el segundo en fusionar renumera**. Tomar `123` aquí habría dejado un hueco en la secuencia que `T15` marca `FAIL` — peor que la colisión, que el proyecto ya sabe resolver (`ADR-121` se renumeró dos veces; `ADR-116` nació `115`). Re-derivado al escribir y antes de fusionar.

**Autocolisión `T02` entre encargo y nota, atrapada y resuelta.** La nota nació `2026-08-19-fp63-cierra.md` y `T02` la marcó de inmediato: normaliza a `20260819fp63cierramd`, idéntico al del encargo `2026-08-19-FP63-CIERRA.md` — el nombre del acto lleva ya la palabra que la convención usa para distinguir la nota. Renombrada a `2026-08-19-fp63-verificacion-espejo.md` (`20260819fp63verificacionespejomd`), y las cuatro referencias actualizadas por comando. Es la trampa conocida del proyecto, disparando por segunda vez.

**Contadores de medición sobre México: `0`.** Este acto corrige una afirmación de privacidad y re-verifica disco. No midió ninguna hipótesis del programa.

---

*`ACTO FP63-CIERRA`, 19/ago/2026. Entorno UBUNTU, caja con corpus, dueña única. `T1` y `T2` ejecutados; `T3` **detenido por compuerta de mesa, sin firma**; `T4` vacío por su propia condición; `T5` cerrado.*
