# `ACTO LOTE-RETRIAGE` · nota de cierre — 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-20-lote-retriage-cierre.md` |
> | **NOMBRE ESTABLE** | **`lote-retriage-cierre`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La nota del `ACTO LOTE-RETRIAGE` (`ADR-131`). Ejecuta el `ARRANQUE` y `T0` completos, y **para `T1`-`T5` ficha por ficha** — cinco `PARO` independientes, no un `PARO` de lote — porque la `VERIFICACIÓN A.8` mide que el trabajo que `T1`-`T5` mandan producir ya está hecho y que su producto **no puede** mover el contador que el encargo va a buscar. |
> | **QUÉ NO ES** | No adjudica, no emite y no retira ningún veredicto `RX.Y`. **No toca el bloque append-only de `hitoD-preregistro`.** No escribe ninguna `hitoD-R*-veredicto-v1_0.md`. No corrige hacia atrás ninguna ficha `B-bis` sellada por `ACTO E3-TRIAGE`: donde mide una cifra distinta, lo anota como hallazgo con su comando. |
> | **VERIFICAS ASÍ** | §2 trae los cinco puntos del `ARRANQUE` con las tres partes de `A.2`; §4 trae la receta del numerador con sus tres controles y el oráculo independiente; §5 trae 104 invocaciones `--verifica`, una por `--id`; §6 trae cinco `PARO` con evidencia propia cada uno. |

**Entorno:** UBUNTU, corpus montado (7.2 G, 289 entradas en `data/raw/`). **Base:** `origin/main = 867948c`
(`PR #297`, `ACTO ACT-PIL-2`, `ADR-130`) — compuerta del encargo, verificada por comando. **Sin `--freeze`.**

---

# §1 · El resultado, en una frase

El encargo pide correr cinco falsadores para mover `Hito D` de `13 de 27`. **Las cinco reglas que nombra
ya son cinco de esas trece.** No hay corrida que correr, no hay contador que mover, y el techo del acto
no es `+5` ni `+3` sino **`+0`** — por una razón medida, no por reserva.

---

# §2 · ARRANQUE — cinco puntos, `A.2` en sus tres partes

| # | punto | valor crudo |
|---|---|---|
| 1 | **REPO** | `/home/pc0/Modelado-Mexicano` · `b4a9b3f Merge pull request #292 …` · `git status` **limpio**, rama `main`. Clon existente, **no** cloné. No arranqué desde el home. |
| 2 | **SHA** | local `b4a9b3f` ≠ `origin/main` `867948c` → **main se movió**. No es `PARO`: refresqué (`git merge --ff-only origin/main` → `867948c`) y re-deriví todo el perímetro contra la base nueva **antes** de editar. |
| 3 | **`data/raw`** | **ya enlazada** en el clon: `data/raw -> /home/pc0/mm-corpus/raw` (symlink de 31/jul, no la creé). En el worktree nuevo `/home/pc0/mm-lote-retriage` **sí** la enlacé, porque un worktree nace sin ella. |
| 4a | **variable** | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = **sin_variable** — esperado para UBUNTU. |
| 4b | **sonda INEGI** | `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → **`200`**. Nunca `curl -I`. |
| 4c | **corpus (3ª parte de `A.2`)** | `ls data/raw/ \| head -1` → `20260813130000.export.CSV.zip`. **289 entradas · 7.2 G** → corpus **MONTADO**. Es la parte que describe *el dato* y no la red, y es la que decide que este acto va a UBUNTU. |
| 5 | **ESPEJO** | no se usó. Toda cifra de esta nota sale del clon de (1) o del worktree, con el comando a la vista. |

**`type grep`, verificado y no supuesto.** `grep` **es una función** de la caja que ejecuta
`ugrep -G --ignore-files --hidden -I --exclude-dir=.git …`. El `-I` descarta el archivo entero al primer
byte no-UTF8, **sin error y sin exit code útil**. Todo negativo de esta nota se declaró con
`command grep` y con control positivo al lado. Donde hizo falta `grep` bajo `xargs` no se usó `command`
(es builtin: `xargs -0 command grep` sale `126` sin examinar un archivo) sino la ruta absoluta
`/usr/bin/grep`.

**Dueña única.** `pgrep -af claude` → **sin salida**. Complemento por `git reflog` (una sesión de agente
concurrente no siempre aparece en `pgrep`): última escritura `19/ago 11:27`. Ninguna sesión concurrente.

---

# §3 · `VERIFICACIÓN A.8` — la premisa del encargo, medida

El encargo trae tres advertencias propias y pide *"una corrección al TRANSFER"*. Las tres advertencias
son correctas en lo que afirman y **las tres se quedan cortas**. Aquí van cuatro correcciones, cada una
con su comando.

## (1) Las cinco fichas existen — y también su corrida. Lo que falta no es la corrida: no hay corrida posible

El encargo dice *"Lo que falta es la corrida, no el triage"*. Medido: las cinco fichas `B-bis` no solo
existen, **están cerradas, con fila asignada**, y la entrada de cola que las gobierna está cerrada
también.

```
$ command grep -m1 '^\*\*Acto:\*\*' forense/hitoD-R4_1-bbis-triage-v1_0.md
**Acto:** `ACTO E3-TRIAGE`, 18/ago/2026, entorno NUBE (repo-only), sobre `origin/main = f3d3f95`.
```

`forense/registro-recalculo-v1_0.md` §1, **Entrada 3** (*"Los 7 veredictos `D` del Hito D — uno por acto,
ficha `B-bis` propia"*) está en estado **`RECALCULADO — SIN CAMBIO`**, cerrada por `ACTO E3-TRIAGE` el
18/ago/2026, con su universo declarado (672 filas de ledger, `sha256` `81b72932b406753a`) y su reparto
verbatim: **`T-1` = 2 · `T-2` = 4 · `T-3` = 2 · `T-4` = 0**.

**`T-4` es la única fila de la escala bajo la cual una corrida es posible** — es la que dice *"la pieza
está en disco y su lectura directa **sí** construye la condición: el `D` deja de ser inejecutable"*.
`T-4 = 0` no es un detalle de conteo: es la medición de que **ninguno de los siete instrumentos
construye la condición de su Umbral**. Un falsador cuya condición el instrumento no construye no se
corre mal — no se corre. Eso es exactamente lo que la letra `D` significa, y el re-triage lo confirmó
contra disco en vez de contra catálogo.

## (2) Son siete fichas, no cinco — y las dos que el encargo no nombra son las únicas interesantes

```
$ ls forense/ | command grep -i 'hitoD.*bbis'
hitoD-R1_1-bbis-triage-v1_0.md
hitoD-R4_1-bbis-triage-v1_0.md
hitoD-R4_2-bbis-triage-v1_0.md
hitoD-R4_3-bbis-triage-v1_0.md
hitoD-R7_2-bbis-triage-v1_0.md
hitoD-R9_1-bbis-triage-v1_0.md      ← el encargo no la nombra
hitoD-R9_2-bbis-triage-v1_0.md      ← el encargo no la nombra
```

Las cinco que el encargo nombra son todas `T-1`/`T-2` — `D` sostenido sin novedad sobre su razón. Las
**dos que no nombra son las dos `T-3`**, la fila que existe para anotar *"el veredicto se sostiene, pero
al menos una de las razones escritas en su Nota de archivo es **falsa** contra el instrumento real"*.
`R9.1` y `R9.2` llevaban dos semanas archivadas con una razón que otro documento del mismo repositorio
ya había refutado. **El encargo seleccionó el subconjunto que menos tenía que decir, y lo seleccionó sin
saberlo** — que es el argumento de `A.8` en su forma más limpia: el perímetro de un encargo se deriva
del árbol, no se recuerda.

## (3) El techo no es `+3`. Es `+0`, y por una razón distinta de la que el encargo supone

El encargo razona: *"Dos de las cinco ya tienen veredicto en archivo propio […]; las otras tres no. El
techo realista es +3, no +5."* Ese razonamiento confunde **el archivo propio de un veredicto** con
**el veredicto archivado**. El contador `13 de 27` no lo alimenta la existencia de un
`hitoD-R*-veredicto-v1_0.md`; lo alimenta —y `tests/check.py` `T18` lo hace mecánico desde `ADR-40`—
el bloque append-only `## Registro de veredictos archivados` al final de `hitoD-preregistro`.

Medido: **las cinco reglas del encargo están las cinco dentro de las trece** (§4). No hay `+3` porque no
hay `+1`: no se puede subir un numerador ocupando una casilla que ya se ocupa. Los dos hechos que el
encargo cita son ciertos y no implican lo que el encargo deduce de ellos — hay `5` archivos
`hitoD-R*-veredicto-v1_0.md` en el árbol (no `2`) y ninguno de los cinco es lo que el contador lee.

## (4) La ficha `hitoD-R7.2-bbis` declara `44` filas ENVIPE donde su propio universo tiene `76`

Hallazgo no pedido, encontrado al construir el conjunto de `--id` de `T0`. La ficha dice, §2: *"**44
filas** con `payload_id` de familia `envipe`, todas `PRESENTE-INTEGRO`, `estado_terminal=SI`"*. Contra
el mismo ledger, con el mismo `sha256` que la Entrada 3 declara, hoy **y** en el SHA contra el que la
ficha corrió:

```
$ sha256sum data/curacion-universo/ledger-inspecciones-barrido2.tsv | cut -c1-16
81b72932b406753a                     ← idéntico al declarado en Entrada 3
$ awk -F'\t' 'NR>1 && $3 ~ /envipe/' data/curacion-universo/ledger-inspecciones-barrido2.tsv | wc -l
76
$ git show f3d3f95:data/curacion-universo/ledger-inspecciones-barrido2.tsv | awk -F'\t' 'NR>1 && $3 ~ /envipe/' | wc -l
76
```

La otra mitad de la misma frase **sí** es exacta: años `2011`-`2025`, **quince ediciones consecutivas**,
derivado del propio `payload_id`. Y el defecto **no mueve la fila asignada**: `T-2` exige que el
instrumento esté en disco, y `76 ≥ 44` lo hace más cierto, no menos. Se declara igual, por la misma
razón que la escala de re-triage declara `T-3` aunque el veredicto no se mueva — **el archivo de un `D`
es su razón, no solo su letra**. No se corrige hacia atrás: la ficha queda como está y esta nota carga
la corrección. Abre `FP-85`.

---

# §4 · `T0.a` · El numerador, con receta probada

El encargo dice, verbatim: *"Intenté derivar cuántas de las 27 están archivadas y mi receta devolvió 3
contra el 13 que declara `estado-programa:95` — la receta está mal y no te paso una cifra que no pude
reproducir."* Correcto en no pasarla. La receta buena, y por qué es la buena:

## La receta

```
$ sed -n '/^## Registro de veredictos archivados/,$p' forense/hitoD-preregistro-v2_0.md \
  | command grep -oP '`R\d+\.\d+`\s*→\s*veredicto\s*`[A-E]`' \
  | command grep -oP 'R\d+\.\d+' | sort -u
R1.1 R1.2 R1.3 R3.1 R3.2 R4.1 R4.2 R4.3 R5.1 R5.2 R7.2 R9.1 R9.2
$ … | wc -l
13
```

No la inventé: es la receta que `tests/check.py` `T18` implementa, y `ADR-40` fija su diseño. Las dos
piezas que la hacen correcta y que un `grep` ingenuo se salta:

- **El recorte al bloque.** `ADR-40` designa `## Registro de veredictos archivados` (append-only, última
  sección) como la única sección legible. Fuera de ella, la forma canónica es cita o hipótesis. `T18`
  nació dos veces mal por esto: su segundo diseño leía cualquier prosa del archivo y *"el primer
  borrador de la propia Nota 5 que archivaba el veredicto de `R1.1` disparó su propio patrón al citar la
  narración vieja de `estado`"*.
- **`sort -u`.** El bloque tiene **14 líneas de veredicto para 13 reglas**: `R4.3` ocupa dos, mitad `A` y
  mitad `B`, y `Nota 24` las archivó así a propósito. Un `grep -c` devuelve `14`. **La diferencia entre
  `14` y `13` es exactamente `sort -u`, y es la trampa más cercana a la respuesta correcta.**

## Los tres controles, contra casos cuya respuesta conozco de antemano

| control | qué sé de antemano | resultado | exit |
|---|---|---|---|
| **positivo** · `R3.1` **debe estar** | `ADR-60` la adjudicó `B` el 4/ago, `Nota 28` | `R3.1` aparece | `0` ✓ |
| **negativo** · `R3.4` **debe faltar** | es *"Una bloqueada"* del Paso 1 — spec mal especificada de `ADR-25`, nunca corrida | no aparece | `1` ✓ |
| **negativo** · `R2.1` **debe faltar** | pre-registrada como probable `D` inejecutable, nunca corrida | no aparece | `1` ✓ |

Los dos negativos van con la prueba de que el comando **sí examinó el archivo** — el defecto que
`TRANSFER §2` mide: `sed -n '/^## Registro…/,$p' … | wc -l` → **18 líneas leídas**. Un negativo sobre
cero líneas no es un negativo.

## El oráculo independiente

```
$ python3 tests/check.py 2>&1 | command grep 'T18'
  [ ok ]  T18 T-PASO2-EJECUCION
```

`T18` **verde** significa que el declarado y el derivado coinciden — cruza frontera de archivo
(`hitoD-preregistro` contra `estado-programa`), que es justo el alcance autorreferencial que sus dos
primeros diseños no tenían.

## Control aritmético de cierre

El perímetro se deriva del mismo documento, por encabezado, y cierra exacto:

```
$ command grep -oP '^## \KR\d+\.\d+' forense/hitoD-preregistro-v2_0.md | sort -u | wc -l
27
$ comm -13 <(perímetro) <(archivadas) | wc -l
0        ← ninguna archivada cae fuera del perímetro
$ comm -23 <(perímetro) <(archivadas) | wc -l
14       ← 13 + 14 = 27
```

**`Hito D` archivadas: `13` de `27`.** Cifra derivada, no tecleada, coincidente con `estado-programa`
en sus dos sitios (`:95` narrativo y `:275`, la línea que `T18` lee).

## Lo que no pude reproducir, y lo digo

**No reproduje el `3`.** Probé nueve familias de receta contra el árbol y ninguna lo devuelve: archivos
`hitoD-*-veredicto-*.md` → `5` · `grep -c` sobre el bloque → `16` · forma canónica sobre el archivo
entero → `13` · archivos de `forense/` que citan "veredicto" → `62` · el wrapper `ugrep` sobre el bloque
→ `16` · veredictos no-`D` → `6` · Notas tituladas "Veredicto de" → `7` · `"de 27"` en `estado-programa`
→ `13` · `hitoD-*-especificacion-*.md` → `2`. Lo que sí puedo decir es que **cuatro números distintos
(`16`, `14`, `13`, `5`) viven al alcance de la mano de la misma pregunta**, y que el paso que separa el
correcto de su vecino más próximo es `sort -u`.

---

# §5 · `T0.b` · Disponibilidad del instrumento, una invocación por `--id`

`A.1` gobierna: varios `--id` en una invocación **solo verifican el último, sin aviso**. Se corrieron
**104 invocaciones, una por `--id`**. Conjunto derivado del ledger de 672 (no de memoria), por familia,
según la pieza que cada ficha declara como su instrumento.

| ficha | instrumento declarado | `--id` | `COINCIDE` | `AUSENTE` | `raíz-no-configurada` | `hash-discordante` | raíz real |
|---|---|---|---|---|---|---|---|
| `R1.1` | 4 recursos AGROASEMEX (`conf17_r1_1_*`) | 4 | **4** | 0 | 0 | 0 | `data_raw` |
| `R4.1` | SESTAD reporte 2021 (`conf17_r4_1_sestad_reporte_2021`) | 1 | **1** | 0 | 0 | 0 | `data_raw` |
| `R4.2` | ENSANUT CONTINUA 2024, 23 payloads | 23 | **23** | 0 | 0 | 0 | **`descargas_mx`** |
| `R4.3` | ENSANUT CONTINUA 2024 (mismo conjunto declarado) | 23 | **23** | 0 | 0 | 0 | **`descargas_mx`** |
| `R7.2` | ENVIPE 2011-2025 | 76 | **76** | 0 | 0 | 0 | `data_raw` |
| **total (ids únicos)** | | **104** | **104** | **0** | **0** | **0** | |

Las tres respuestas que el encargo pide no colapsar salen **las tres en cero**. Y una cuarta, que el
encargo no pidió y que no se colapsa tampoco: **23 de los 104 no viven en `data/raw`**. Están
`COINCIDE`, con `sha256` y tamaño verificados, bajo la raíz `descargas_mx` — que el manifiesto resuelve
por el campo `raiz` de la entrada. La pregunta *"¿está el instrumento en `data/raw`?"* tiene, para
`R4.2`/`R4.3`, la respuesta **"no, y sin embargo está"**: presente e íntegro bajo otra raíz configurada.
Colapsarlo a un `sí` habría escondido dónde vive el ENSANUT 2024 de este programa.

**Ninguna de las cinco fichas necesita `ENFIH` ni `ENSAFI`** — `command grep -ciE 'ENFIH|ENSAFI'` sobre
las cinco → `0`, `0`, `0`, `0`, `0`. Ninguna espera a `APERTURA-ENFIH-ENSAFI`; esa rama del encargo
queda sin objeto.

---

# §6 · `T1`-`T5` · `PARO` por ficha — cinco, no uno

**Doctrina de LOTE, verbatim del encargo: *"PARO por ficha, no por lote."*** Se acata al pie: cada fila
de abajo se evaluó por separado, contra su propia ficha y su propia evidencia de disco, y **cada una
para por sí misma**. Que las cinco coincidan es un resultado medido, no un atajo de lote.

| ficha | fila `B-bis` asignada | ¿en las 13 archivadas? | instrumento | ¿`T1`-`T5` ejecutables? | motivo del `PARO`, propio de la ficha |
|---|---|---|---|---|---|
| `R1.1` | `T-2` | **SÍ** (`R1.1` → veredicto `D`, `Nota 5`, 29/jul) | 4/4 `COINCIDE` | **NO** | Los 4 recursos AGROASEMEX están en disco, íntegros y **leídos**: ninguno llega a nivel productor y su eje temporal es fiscal, no ciclo agrícola. `T-4` descartado en la ficha. `COMMIT A` no tiene universo que congelar. |
| `R4.1` | `T-2` | **SÍ** (`Nota 23`, 4/ago) | 1/1 `COINCIDE` | **NO** | SESTAD 2021 en disco y ya clasificado `EXISTE-NO-SATISFACE` (agregado, no microdato por establecimiento). CLUES `NO-ACCESIBLE` y ausente del ledger; sin microdato de ENSANUT 2018 cae también la lectura ecológica. Lo que reabriría `R4.1` es **adquisición**, no corrida. |
| `R4.2` | `T-2` | **SÍ** (`Nota 17`, 4/ago) | 23/23 `COINCIDE` | **NO** | ENSANUT CONTINUA 2024 **completa** en disco y **sin pregunta de permiso laboral**. Ninguna fila de las 672 toca el hueco. No hay variable que dicotomizar: `COMMIT A` no puede declarar la variable que `COMMIT B` mediría. |
| `R4.3` | `T-1` (mitad A) · `T-1` (mitad B) | **SÍ** (`Nota 24`, 4/ago, ambas mitades) | 23/23 `COINCIDE` | **NO** | Único caso `T-1` del lote: el instrumento **declarado** está en disco, el que **haría falta** no existe en las 672 — ni registro de surtimiento enlazable a persona (mitad A) ni variable de cuidadora de crónico (mitad B). ENUT está y con profundidad (16 payloads), y mide otra cosa. |
| `R7.2` | `T-2` | **SÍ** (`Nota 11`, 4/ago) | 76/76 `COINCIDE` | **NO** | Quince ediciones ENVIPE en disco, 2011-2025, y **la pregunta sigue sin existir**: `BP2_1` cuelga por ruteo de `BPCOD=01`. Más instrumento no construye la condición ausente. *(Y su ficha declara `44` donde el ledger tiene `76` — §3(4), `FP-85`.)* |

**Por qué el `PARO` es la ejecución del encargo y no su incumplimiento.** `A.8` lo ordena en su propia
letra: *"Si (2) o (3) revelan que el trabajo ya está hecho, total o parcialmente: el encargo **NO** se
lanza. Se reescribe sobre el faltante real, o se cancela. Descubrirlo aquí es el rendimiento de este
bloque."* Y el `ARRANQUE` lo dice antes: *"encontrar que el terreno no es el que el encargo supone es
entregable, no interrupción."*

**Lo que habría pasado si `T1`-`T5` se ejecutan igual.** `COMMIT A` habría congelado una spec sobre una
variable que el instrumento no tiene; `COMMIT B` habría producido un `n`, un `EE` y un `IC95` sobre un
universo que no es el pre-registrado. Bajo `A-bis r4` eso se declara `ACOTADO` y no se compara contra
ningún marginal poblacional — es decir, la corrida entera habría entregado una cifra que no adjudica
nada, sobre una regla que ya está archivada, sin mover el contador. **Ese es el resultado que el `PARO`
evita, y cuesta cinco `PARO` escribirlo.**

---

# §7 · El faltante real — sobre qué se reescribe este encargo

Si el objetivo es mover `Hito D`, el perímetro no son las cinco reglas del encargo (que ya están
dentro): son las **14 que faltan**, derivadas por diferencia en §4.

```
R1.4 · R2.1 · R2.2 · R3.4 · R7.1 · R7.3 · R7.4 · R7.5 · R8.1 · R8.2 · R8.3 · R10.1 · R10.2 · R10.3
```

Lo que el árbol ya dice de ellas, sin abrir acto nuevo:

- **Ocho están pre-registradas como probable `D` inejecutable** desde el Paso 1 — `R1.4` · `R2.1` ·
  `R2.2` · `R7.4`/`R7.5` · `R8.2` · `R8.3` · `R10.2` · `R10.3` — por dato organizacional propietario,
  hueco de dato ya declarado, o límite ético. Un acto que las ataque de frente repite lo que
  `ACTO E3-TRIAGE` acaba de hacer con las otras siete.
- **`R3.4` está bloqueada** por la spec mal especificada de `ADR-25`, *"el go/no-go del programa y el
  `S2` abierto más antiguo"* — y es un hueco de **spec**, no de dato: es la única de las catorce cuyo
  desbloqueo no exige adquirir nada.
- **Quedan `R7.1` · `R7.3` · `R8.1` · `R10.1`** sin declaración previa de inejecutabilidad en el Paso 1.
  **Son las cuatro candidatas reales a mover el contador**, y ninguna ha sido triada.

Esto no se sella aquí — es material para el encargo sucesor, y va al tablero como `FP-86`.

---

# §8 · Contador

**`Hito D` archivadas: `13` → `13` de `27`.** Los dos números dichos y derivados por la receta de §4,
con sus tres controles y el oráculo `T18` verde. **El acto no mueve el contador, y no podía moverlo**:
las cinco reglas de su perímetro son cinco de las trece que el numerador ya cuenta.

Ningún otro contador se toca. `llaves de identificación ejercidas`, `candidatas del marco`,
`11 de 15`, `4 de 144` y `momentos HOLDOUT` son poblaciones de conteo distintas (`FP-68`, `ADR-67(c)`) y
este acto no las roza.

---

# §9 · Módulo de auditoría de rigor extremo

**No aplica.** `v2.3` lo acota a artefactos que afirman algo sobre México — reports, integrador, modelo,
validaciones forenses. Esta nota es un forense de proceso y un registro de medición: no hay afirmación
sobre México que auditar. Anotarlo es la regla, no una omisión.
