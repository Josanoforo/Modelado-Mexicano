# Nota · ACTO PURGA-EJECUTA — ejecución de `FP-143`, `~/mm-purga.git` destruido, segundo espejo descubierto

25/ago/2026. Worktree `/home/pc0/mm-purga-ejecuta`, rama `purga-ejecuta`, base `origin/main = 26ea239`. FASE A (solo lectura y medición) y FASE B (escritura) corridas por el mismo ejecutor; la destrucción física (§3) la ejecutó el supervisor, fuera de este worktree, bajo entorno UBUNTU. Encargo: `forense/encargos/2026-08-25-PURGA-EJECUTA-espejo.md`. Ejecuta `FP-143`, fila madre `FP-63`.

---

## §1 · Cadena verbatim de autorización

Cadena exacta registrada en `firmada_en` de `FP-143` (`forense/firmas-pendientes.tsv:141`, TSV desescapado con `csv.reader` sobre un campo que sí usa comillas dobladas RFC4180 — lectura, no reescritura):

> `2026-08-25, mesa, hoja de las diez letras, L5/FP-63, verbatim: "¿Escribes «AUTORIZO DESTRUIR mm-purga.git»? → sí"`

Fuente primaria — `forense/encargos/2026-08-25-SELLA-AGO25-F-HOJA.md:19` (tabla de dos columnas, el archivo se declara a sí mismo en `:11` como *"Redactado por dirección... Transcripción verbatim de la hoja, tal como llegó"*):

> `| L5 63 · ¿Escribes «AUTORIZO DESTRUIR mm-purga.git»? (premisa refutada, 12M de ruido) | sí |`

Registro canónico — `canon/gobernanza-v1_15.md:3343` (`ADR-168`, inciso `(d)`, "L5/`FP-63`, sí"):

> "La cadena verbatim `AUTORIZO DESTRUIR mm-purga.git` llega en el lanzamiento de la hoja como autorización dada — no como mención de la propia compuerta, que es lo único que existía hasta hoy... Se registra aquí, verbatim, como la primera aparición de la cadena que sí es autorización."

Nota de PR #338 — `forense/notas/2026-08-25-sella-f-hoja.md:29` (rama `claude/encargo-1-sella-ago25-f-75gu88`, la misma que el merge commit `26ea239` cita): mismo texto, y añade *"Se registra en `ADR-168`"* — es decir, la nota ya sabía, al escribirse, que el ADR real era `168` y no `166`.

### El matiz: autorización dada, no mención de la propia compuerta

Los dos precedentes de "solo mención de la propia compuerta" — el patrón que paró a `CAJA-RESIDUOS` y a `FP63-CIERRA` — están verificados línea por línea:

- `canon/gobernanza-v1_15.md:2349`: la cadena aparecía solo dentro de *"Solo procede si el launcher/mensaje de mesa trae la firma verbatim: …"* — la especificación citándose a sí misma.
- `canon/gobernanza-v1_15.md:2409`: mismo patrón, segunda vez.
- `forense/notas/2026-08-19-fp63-verificacion-espejo.md:267` y `forense/notas/2026-08-19-caja-residuos-cierre.md:93`: mismo texto, confirmado.

En esos dos casos la cadena NUNCA apareció en un mensaje real de mesa sobre una decisión concreta — solo en la definición abstracta de la compuerta. En el caso de `FP-143`, la cadena aparece dentro de un mensaje real y fechado de dirección/mesa (la hoja), en el contexto de una decisión concreta (`L5`), acompañada de una respuesta afirmativa "sí". Es estructuralmente distinto del autocaptura: no es la especificación citándose a sí misma, es mesa citando la especificación y respondiéndola.

Matiz declarado y no resuelto por este acto: mesa no escribió la cadena como enunciado declarativo libre ("AUTORIZO DESTRUIR mm-purga.git."), la escribió embebida dentro de una pregunta con guillemets («»), respondida con la palabra "sí" — no con la repetición de la cadena. Si la compuerta original exigía literalmente que "el mensaje de mesa TRAIGA la firma verbatim" (texto de `gobernanza:2349` y `:2409`), el mensaje de la hoja sí trae la cadena verbatim (dentro de la pregunta) y sí trae una afirmación de mesa sobre ella ("sí") — cumple la letra citada, aunque no adopta la forma de una orden imperativa aislada. Es la lectura que adoptó `ADR-168`, no un hecho autoevidente; se reporta el matiz, no se re-adjudica.

---

## §2 · Última re-verificación de la premisa, en fresco, antes de tocar nada

Contra `HEAD=26ea239`, worktree limpio, corridos EXACTAMENTE los comandos que el acto exige, salidas crudas íntegras.

```
$ git -C /home/pc0/mm-purga.git log --oneline | head
ed46c26 Merge pull request #139 from Josanoforo/sesion/regla-elegibilidad-preregistro-r5-1
eed1bd1 Merge pull request #163 from Josanoforo/codex/curador-baseline-semantico
3f9cfe4 docs(curador): usa nombre único para la guía
16180e6 data(curacion): incorpora baseline semántico N1-N33
170ae93 feat(curador): incorpora curador reusable
86d5d04 Merge pull request #162 from Josanoforo/mapa-ext-integracion-20260806-184619
7d58acf MAPA-EXT: corrige conteos y estados consolidados
ef6ce0b MAPA-EXT: consolida fuentes externas y cola de aperturas
a88a2b6 MAPA-EXT: mapea fuentes civiles para México
50a313b MAPA-EXT: consolida fuentes académicas para México

$ git -C /home/pc0/mm-purga.git log --oneline | wc -l
597

$ git -C /home/pc0/mm-purga.git fsck --unreachable --dangling 2>&1
(salida vacía — 0 líneas)

$ git -C /home/pc0/mm-purga.git count-objects -v
count: 0
size: 0
in-pack: 3053
packs: 1
size-pack: 11352
prune-packable: 0
garbage: 0
size-garbage: 0

$ git -C /home/pc0/mm-purga.git for-each-ref | wc -l
167

$ du -sh /home/pc0/mm-purga.git
12M	/home/pc0/mm-purga.git

$ ls /home/pc0/mm-purga.git/logs 2>&1; ls /home/pc0/mm-purga.git/objects/info/alternates 2>&1
ls: cannot access '/home/pc0/mm-purga.git/logs': No such file or directory
ls: cannot access '/home/pc0/mm-purga.git/objects/info/alternates': No such file or directory
```

Sin una sola diferencia frente a lo que `FP-63`/`FP63-CIERRA` midieron el 19/ago.

**Medición derivada — universo declarado (`A.13`/`A.4`): los 3053 objetos del espejo, examinados uno por uno contra el clon base `/home/pc0/Modelado-Mexicano` (repo real, no bare, `remote origin = github.com/Josanoforo/Modelado-Mexicano.git`):**

```
$ git -C /home/pc0/mm-purga.git cat-file --batch-all-objects --batch-check='%(objectname) %(objecttype)' | wc -l
3053
$ ... | awk '{print $2}' | sort | uniq -c
   1081 blob
    603 commit
   1369 tree

$ awk '{print $1}' mirror-all-objects.txt | git -C /home/pc0/Modelado-Mexicano cat-file --batch-check='%(objectname) %(objecttype)' | wc -l
3053    (objetos examinados = 100% del universo del espejo)

$ ... | awk '{print $2}' | sort | uniq -c
   1081 blob
    598 commit
      6 missing
   1368 tree
```

Controles (`A.13`): positivo — un blob marcado "presente" reverificado individualmente con `git cat-file -e`, exit 0. Negativo/mecanismo — un sha40 de ceros deliberado devuelve literalmente `missing`, confirmando que el comando distingue presente de ausente y no está roto (cero-sobre-cero no es este caso: 3053/3053 examinados). Aritmética cerrada: `1081+598+1368+6=3053`.

Los 6 objetos ausentes en el clon base, identificados y tipados contra el espejo:

```
20342597cb0365a89cef177250f999c9a63ae4da commit  → refs/pull/87/head
4074dcfc5984eb9e012c1a1fcca6f6e74c7e0e86 commit  → refs/pull/85/head
8e34849ff141063e3fa6cdde8486ae1d40064410 commit  → refs/pull/138/head
d341411b0652ca17dd09c8e39332d8b0ae86a6cc commit  → refs/pull/164/merge
d43ee5326ced349268f1050090715df635432cf6 commit  → refs/pull/137/head
5b1fa9cce7f292d323a80abbd1056c96a621ba8e tree    (alcanzable desde uno de los 5 commits anteriores)
```

5 commits, exactamente `refs/pull/85,87,137,138,164` · 1 tree · **0 blobs**. Coincide, objeto por objeto, con lo que `FP63-CIERRA` reportó el 19/ago.

**Los 6 artefactos `filter-repo/`, byte-identidad verificada tres veces:**

```
sha256(forense/purga-privacidad/filter-repo/*) == sha256(/home/pc0/mm-purga.git/filter-repo/*) == sha256 registrado en MANIFIESTO-PURGA.tsv
  already_ran            89ec7d62...cae0c00  MATCH
  changed-refs           dcf85936...ac01dde  MATCH
  commit-map             756e9a91...4c33c2b  MATCH
  first-changed-commits  3200188c...4f924de  MATCH
  ref-map                142d59b2...c6cc5c15 MATCH
  suboptimal-issues      f7bae299...9cee4b2  MATCH
```

`cmp -s` (bytes) entre la copia en el repo y la copia viva del espejo: exit 0 en los 6. Objetos examinados: 6 de 6 filas del manifiesto (universo completo).

**Veredicto de premisa: sigue refutada, sin drift.** Conteo de objetos examinados (`A.13`): 3053/3053 del espejo contra el clon base (universo completo, no muestra); 6/6 artefactos `filter-repo/` contra el manifiesto. Ningún negativo se declaró sobre un universo de cero.

---

## §3 · La destrucción

Ejecutada por el supervisor, fuera de este worktree, bajo entorno UBUNTU con acceso de disco al espejo — el ejecutor de FASE A/B no corrió ningún comando destructivo.

**Huella pre-destrucción** (reportada por el supervisor; `du -sh`=12M y `rev-parse HEAD`=`ed46c26...` coinciden exactamente con lo que este mismo acto midió en fresco en §2 — verificado por este ejecutor antes de la destrucción, no solo citado; los conteos de `find` no son re-derivables hoy porque el objeto ya no existe, se citan como reportados):

```
$ du -sh /home/pc0/mm-purga.git      → 12M	/home/pc0/mm-purga.git
$ find /home/pc0/mm-purga.git -type f | wc -l → 32
$ find /home/pc0/mm-purga.git | wc -l         → 45
$ git -C /home/pc0/mm-purga.git rev-parse HEAD → ed46c26abd8513f18a5c097822f32e6ced88d3d4
```

**Re-medición independiente del supervisor, inmediatamente antes de la destrucción** (reproduce exactamente §2 de esta nota, corrida por separado):

```
objetos del espejo: 3053 · examinados contra el clon base: 3053
1081 blob · 598 commit · 6 missing · 1368 tree
los 6 missing: 20342597cb0365a89cef177250f999c9a63ae4da · 4074dcfc5984eb9e012c1a1fcca6f6e74c7e0e86 ·
  5b1fa9cce7f292d323a80abbd1056c96a621ba8e · 8e34849ff141063e3fa6cdde8486ae1d40064410 ·
  d341411b0652ca17dd09c8e39332d8b0ae86a6cc · d43ee5326ced349268f1050090715df635432cf6
CONTROL NEGATIVO: 0000000000000000000000000000000000000000 missing
CONTROL POSITIVO: 26ea23925ee85cd547d69256f55e2b13ea2879a0 commit
```

**Destrucción:**

```
$ rm -rf /home/pc0/mm-purga.git      → exit 0
$ ls -d /home/pc0/mm-purga.git       → ls: cannot access '/home/pc0/mm-purga.git': No such file or directory · exit 2
$ test -e /home/pc0/mm-purga.git     → NO EXISTE — destruido
CONTROL POSITIVO del propio test: test -e /home/pc0/BACKUP-mm-mirror-2026-08-10.git → EXISTE (el test sí distingue)
$ du -sh /home/pc0/mm-purga.git      → du: cannot access '/home/pc0/mm-purga.git': No such file or directory
```

**Verificación independiente de este ejecutor, corrida de nuevo tras recibir el reporte** (no solo aceptada del mensaje):

```
$ ls -d /home/pc0/mm-purga.git 2>&1; echo "exit=$?"
ls: cannot access '/home/pc0/mm-purga.git': No such file or directory
exit=2
$ test -e /home/pc0/mm-purga.git; echo "test -e exit=$?"
test -e exit=1
$ test -e /home/pc0/BACKUP-mm-mirror-2026-08-10.git; echo "test -e exit=$?"
test -e exit=0
```

Confirmado, independientemente, en este worktree: `~/mm-purga.git` no existe; `~/BACKUP-mm-mirror-2026-08-10.git` (control positivo del propio mecanismo de verificación) sí existe.

---

## §4 · El segundo espejo — `~/BACKUP-mm-mirror-2026-08-10.git`

Descubierto por el supervisor durante la destrucción; ninguna fila del tablero lo había nombrado nunca — ni `FP-63`, ni `FP-143`, ni `ADR-113`, ni `ADR-120`. Re-medido de cero por este ejecutor, mismo método y mismos controles que §2, antes de escribir nada en el tablero.

```
$ git -C /home/pc0/BACKUP-mm-mirror-2026-08-10.git log --oneline | wc -l
597
$ git -C /home/pc0/BACKUP-mm-mirror-2026-08-10.git fsck --unreachable --dangling 2>&1
(salida vacía — 0 líneas)
$ git -C /home/pc0/BACKUP-mm-mirror-2026-08-10.git count-objects -v
count: 0
size: 0
in-pack: 3053
packs: 1
size-pack: 12574
prune-packable: 0
garbage: 0
size-garbage: 0
$ git -C /home/pc0/BACKUP-mm-mirror-2026-08-10.git for-each-ref | wc -l
167
$ du -sh /home/pc0/BACKUP-mm-mirror-2026-08-10.git
13M	/home/pc0/BACKUP-mm-mirror-2026-08-10.git
$ ls /home/pc0/BACKUP-mm-mirror-2026-08-10.git/logs 2>&1; ls .../objects/info/alternates 2>&1
ls: cannot access '.../logs': No such file or directory
ls: cannot access '.../objects/info/alternates': No such file or directory
```

Estructuralmente idéntico a lo que `~/mm-purga.git` tenía: 3053 objetos in-pack, 167 refs, 597 commits, 0 sueltos/garbage/prune-packable, sin `logs/` ni `alternates`. Creado `2026-08-10 14:46:45` (timestamp del directorio, `ls -la`) — **~33 minutos antes** que `~/mm-purga.git` (`15:19-15:21` según `ls -la` de FASE A).

**Medición contra el clon base, 3053/3053 objetos examinados, mismo método que §2:**

```
$ git -C /home/pc0/BACKUP-mm-mirror-2026-08-10.git cat-file --batch-all-objects --batch-check='%(objectname) %(objecttype)' | wc -l
3053
$ ... | awk '{print $2}' | sort | uniq -c
   1081 blob
    603 commit
   1369 tree

$ ... | git -C /home/pc0/Modelado-Mexicano cat-file --batch-check='%(objectname) %(objecttype)' | wc -l
3053
$ ... | awk '{print $2}' | sort | uniq -c
   1081 blob
    602 commit
      2 missing
   1368 tree
```

Controles: positivo — un blob "presente" reverificado con `git cat-file -e`, exit 0. Negativo — sha40 `111...1` deliberado, devuelve `missing`. Aritmética: `1081+602+1368+2=3053`.

Los 2 objetos ausentes en el clon base:

```
1e65182c5521fb25d280d73a3e8bde6769d96e1e commit → refs/pull/164/merge
8afe2df8ad29214a006928e35d06a00a9a8a1602 tree
```

**CERO blobs exclusivos** — exactamente la misma conclusión que `FP-63`/`FP63-CIERRA` alcanzaron para `~/mm-purga.git`.

**Los dos espejos NO comparten conjunto de objetos ausentes.** Intersección de los 6 ausentes de `~/mm-purga.git` (§2) contra los 2 ausentes de este espejo:

```
$ comm -12 <(sort missing-shas.txt) <(sort backup-missing-shas.txt)
(salida vacía — cero elementos en común)
```

El commit ausente de este espejo también cuelga de `refs/pull/164/merge` — la misma ref de PR que uno de los 6 ausentes de `~/mm-purga.git` — pero con un sha **distinto** (`1e65182c...` aquí, `d341411b...` en `mm-purga.git`): consistente con que `refs/pull/164/merge` es un commit de fusión efímero que GitHub recalcula, y este espejo capturó ese ref ~33 minutos antes que el otro.

**Lo que esto significa, sin decidirlo:** la cadena verbatim que mesa firmó (`AUTORIZO DESTRUIR mm-purga.git`, §1) nombra literalmente `mm-purga.git`. Este archivo se llama `BACKUP-mm-mirror-2026-08-10.git` — no lo cubre, letra por letra. Redundante por la misma medición (0 blobs exclusivos), pero sin firma de mesa propia. Fila nueva `FP-151`, `ABIERTA`, sin `firmada_en` ni `ejecutada_en`: la decisión queda planteada para mesa, no tomada por el ejecutor. **No se toca.**

---

## §5 · Discrepancias

**(a) La cita `ADR-166` en `dónde` de `FP-143` está stale.** `forense/firmas-pendientes.tsv:141` cita `canon/gobernanza-v1_15.md (ADR-166)`. Verificado por comando (`command grep -n "ADR-166" canon/gobernanza-v1_15.md`): `ADR-166` es hoy `ACTO LLAVE2-DECRETO` (`gobernanza:3405`, DiD sobre `ENOE`/decreto fronterizo de estímulos fiscales — sin relación con esta compuerta). El acto que sí candidateó `ADR-166` para registrar esta autorización fue **renumerado a `ADR-168`** al fusionar `origin/main` (colisión doble con `ACTO U2-CRUCE`/`ADR-165` y `ACTO LLAVE2-DECRETO`/`ADR-166`, regla de la casa: renumera quien fusiona segundo — `gobernanza:3335`, `:3363`). La nota del mismo acto (`forense/notas/2026-08-25-sella-f-hoja.md:29`) ya lo sabía y dice *"Se registra en ADR-168"* — pero la fila del tablero nunca se actualizó. Corregido en la celda `ejecutada_en` de `FP-143` (nueva, sin reescribir `dónde`) y en esta nota; registrado también en `ADR-169`.

**(b) La fila se anunció como "FP-137" y la fila real es "FP-143".** El propio `FP-63` (`firmas-pendientes.tsv:64`, texto `ACTUALIZADA 2026-08-25`) dice textualmente: *"Fila mínima UBUNTU nueva, FP-137, FIRMADA, ejecutada_en vacío"*. El "Cierre" del encargo `2026-08-25-SELLA-AGO25-F-HOJA.md:33` repite el mismo número: *"FP-137 (destrucción de ~/mm-purga.git...)"*. Verificado por comando (`awk -F'\t' '$1=="FP-137"' forense/firmas-pendientes.tsv`): **no existe fila `FP-137`** en el tablero — cero resultados. La fila real, existente y hoy ejecutada, es **`FP-143`** (`firmas-pendientes.tsv:141`), consistente con `canon/gobernanza-v1_15.md:3343` y `forense/notas/2026-08-25-sella-f-hoja.md:29`, ambos con "FP-143" explícito. Causa raíz: el mismo colapso de numeración de (a) — las seis filas que el acto abría como `FP-135`-`FP-140` se renumeraron a `FP-141`-`FP-146` al fusionar (`FP-143 = FP-137 + 6`, aritmética exacta y consistente en las seis filas). El "Cierre" del encargo y el texto de `FP-63` quedaron con la etiqueta pre-renumeración; la entrada canónica de gobernanza (`ADR-168`) y la nota del PR #338 sí llevan la etiqueta correcta. Corregido en la celda `ejecutada_en` de `FP-63` (nueva, sin reescribir `firmada_en`).

**(c) Sin discrepancia en la medición técnica del espejo.** Cada cifra re-verificada en fresco en §2 (refs, `fsck`, `count-objects`, tamaño, ausencia de `logs`/`alternates`, 6/6 artefactos, 6 objetos-de-3053 ausentes en base) coincide exactamente con lo que `FP-63`/`FP63-CIERRA` ya habían registrado — cero drift, en dos pasadas independientes (FASE A de este acto, y de nuevo antes de la destrucción).

**(d) Colisión de numeración con `origin/main`, detectada y evitada por adelantado.** `origin/main` avanzó de `26ea239` a `96dcc6c` durante este acto (`PR #339`: `ACTO PROPAGA-330-337`, `ACTO ESCALA-ASIGNADOS`, `ACTO SORTEO-V2-PROPUESTA`). Máximo de ADR en el árbol fusionado: `168`, sin cambio — sin colisión, `ADR-169` queda limpio. Máximo de `FP-` en el árbol fusionado: `150` (no `148`, el máximo local) — `FP-149`/`FP-150` ya los había tomado `PR #339` mientras este acto medía/escribía. La fila del segundo espejo nace directamente `FP-151`, no `FP-149`, re-derivada contra el árbol fusionado antes de escribir (regla de la casa: renumera quien fusiona segundo). Ninguna de las filas que `PR #339` sí tocó (`FP-96`, `FP-97`, `FP-133`, `FP-134`, `FP-141`, `FP-145`) se cruza con `FP-143`/`FP-63`/`FP-151`, verificado fila por fila.

**(e) `ADR-113` — ya corregido, no vuelto a corregir.** La afirmación de privacidad de `ADR-113` (`gobernanza:2200`; citada verbatim en `ADR-120(d)`, `gobernanza:2351`: *"conserva historia pre-purga"* y *"las 1,737 filas de datos personales"*) ya fue corregida sin editar su texto por `ADR-120` (`gobernanza:2341`) y clasificada por `ADR-122` (`gobernanza:2391`, `:2405`) como `AFIRMACIÓN HEREDADA SIN UNIVERSO PROPIO`, el 19/ago/2026. No estaba viva al arrancar este acto — la re-verificación de §2, corrida hoy de nuevo en fresco, reconfirma sin diferencia la corrección ya sellada. No se abre enmienda nueva a `ADR-113`: no hay nada que `ADR-120`/`ADR-122` no hayan dejado ya escrito.
