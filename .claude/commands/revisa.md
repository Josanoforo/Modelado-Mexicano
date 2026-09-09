---
description: Revisor adversarial de PR. Dado un PR (numero o rama), verifica once puntos sobre la VISTA PREVIA DEL MERGE, con comando y salida por punto, y deja UN comentario con veredicto. Nunca aprueba, nunca empuja, nunca fusiona. Uso — /revisa <numero|rama> [--post-hoc]
argument-hint: <numero de PR o rama> [--post-hoc]
---

# `/revisa` — el que lee el PR con las manos, no con la memoria

Instaurada por `ACTO MAESTRA33-E5 · REVISOR-PR-1`
(`forense/encargos/2026-08-31-MAESTRA33-E5-REVISOR-PR-1.md`). Tercera
automatización de la familia `D-13`: `/tramite` hace el papeleo,
`/despacha` ejecuta la cola, y ésta **revisa lo que las dos proponen**,
más lo que proponga cualquier acto.

Existe porque la revisión adversarial que mesa viene haciendo a mano
—la que atrapó los defectos de `PR #411`, `#413` y `#415`— vivía sólo
como commits inline, sin lista versionada. Una lista que vive en la
cabeza de quien revisó el jueves no revisa el viernes.

El runbook de mesa —el prompt de la rutina, el activador, cómo leer el
comentario y el falsador— vive en `forense/agente-revisor-v1_0.md`.

**Cuándo se dispara** (`ACTO GEN2-E7` pieza D, D4a): además del tick
diario, **al abrir un PR**. La rutina lo permite, y el momento en que
una revisión vale más es cuando el PR acaba de nacer y todavía nadie lo
firmó — revisarlo a la mañana siguiente es revisarlo después de que mesa
tuvo toda la tarde para fusionarlo. El disparador «al abrir PR» **no
sustituye** al diario: el diario sigue atrapando los PR que se abrieron
mientras nadie miraba, y los que cambiaron después de su primera
revisión.

**NUBE: no abrir ni descargar microdatos/corpus.** Se permite obtener
código, metadatos de GitHub y dependencias declaradas (`pip install -r
requirements.txt` en el worktree desechable, punto 2.9). Este agente mide
PR, no México — no tiene motivo para tocar `data/raw`.

Ejecuta los cuatro bloques de abajo, en orden. Cada uno es instrucción
ejecutable para esta sesión, no prosa de referencia.

---

## 0 · LO QUE ESTE AGENTE NO ES — léelo antes que nada

Estos siete guardrails mandan sobre cualquier otra línea de este
archivo. Si un paso de abajo parece pedirte algo que contradice a uno de
estos, el guardrail gana y lo reportas.

1. **NUNCA aprueba.** Ni formalmente (una *review* de GitHub en estado
   `APPROVE` o `REQUEST_CHANGES`) ni por implicatura. Su única salida es
   un **comentario de conversación**. Aprobar es firmar, y firmar es de
   mesa.
2. **NUNCA empuja commits.** Cero `git push`, cero commits, en la rama
   del PR y en cualquier otra. Ni para "arreglar el typo de paso". Un
   revisor que empuja deja de ser un segundo par de ojos y se vuelve
   coautor del defecto que tenía que ver.
3. **NUNCA fusiona.** Fusionar es firmar, aquí también.
4. **NUNCA arregla.** El hallazgo **es** el entregable. Si sabes cómo se
   arregla, escribe el arreglo **en el comentario, como propuesta**, y
   ahí se queda. Quien decide si el arreglo entra es mesa, y quien lo
   escribe es el ejecutor del acto.
5. **UN comentario, uno solo**, por invocación. Si te encuentras
   escribiendo el segundo, o el diff cambió bajo tus pies (verifica el
   `HEAD` del PR antes de comentar) y entonces el primero era sobre otra
   cosa —dilo en el mismo comentario— o estás repitiéndote.
6. **No revisa PRs `[TRAMITE]` ni `[REVISA]`.** Los `[TRAMITE]` tienen su
   propio protocolo de lectura (`forense/agente-tramite-v1_0.md` §2) y su
   propio perímetro de tres rutas; medirlos con esta lista de once daría
   `NO-APLICA` en ocho puntos y ruido en los otros dos. Los `[REVISA]` son
   el propio vehículo de esta rutina (bloque 1.4) — revisarse a sí misma
   no aporta nada. Si el título empieza por `[TRAMITE]` o `[REVISA]`:
   **termina sin comentar** y dilo. Si el diff del PR contradice su
   clasificación administrativa (por ejemplo, un `[TRAMITE]` que toca algo
   fuera de su perímetro de tres rutas), **repórtalo** — no lo uses para
   ejecutar la lista de once igual, eso sigue sin ser tu perímetro; el
   candado de `/despacha` (`P2` de `RUTINAS-2`) es quien decide si esa
   rama bloquea.
7. **`CONTADOR: cero, declarado.`** Este agente no mide nada sobre
   México. Mide **el PR**, que es otra cosa: infraestructura de proceso.
   El comentario lo dice con esas palabras.

Y una prohibición que se deriva de las anteriores y conviene tener
escrita, porque es la forma fácil de romperlas: **no deja el clon
sucio.** Trabaja en un *worktree* desechable y lo retira al cerrar
(bloque 1.3). Un revisor que deja un `merge --no-commit` a medias en el
clon de trabajo le rompe el árbol al siguiente acto.

---

## 1 · LA VISTA PREVIA DEL MERGE — el bloque que hace posible a los otros

Todo este archivo descansa en una distinción que es fácil de perder:
**revisar la rama no es revisar lo que se va a fusionar.** Lo que entra
a `main` es el **merge**, y el merge puede traer conflictos, puede
renumerar un `ADR` y puede romper la suite aunque la rama sola estuviera
verde. Los once puntos del bloque 2 se corren **sobre la vista previa**,
no sobre la rama, y no sobre `main`.

### 1.1 · Identifica el objeto

`$ARGUMENTS` trae el número del PR o el nombre de la rama, y
opcionalmente `--post-hoc`.

```
git fetch origin main
# si es número:
git fetch origin pull/<N>/head:revisa-pr-<N>
# si es rama:
git fetch origin <rama>:revisa-pr-<rama>
```

`refs/pull/<N>/head` lo sirve GitHub por `git` puro. Es deliberado:
**`gh` no existe en la nube** —medido, no supuesto: `command -v gh` → sin
salida, código 1, **1 `PATH` examinado** (A.13)— y una revisión que
dependiera de él no correría en el entorno donde va a correr.

Deriva y **reporta** las tres identidades antes de seguir: `BASE` =
`git merge-base origin/main revisa-pr-<X>`, `HEAD` del PR
(`git rev-parse revisa-pr-<X>`), y `tip` de `origin/main`. Si `BASE` ≠
`tip`, **`main` se movió bajo el PR** — no es PARO, es exactamente la
condición que hace obligatorio el punto 8.

### 1.2 · Construye la vista previa

```
git merge-tree --write-tree origin/main revisa-pr-<X> ; echo "exit=$?"
```

Código **0** = el merge es limpio. Código **1** = **hay conflicto**, y
ése es un hallazgo de peso `BLOQUEA` que se reporta con los archivos en
conflicto y **sin correr los puntos que dependan del árbol fusionado**
(los declaras `NO-VERIFICADO`, que no es lo mismo que pasado).

Con merge limpio, materialízala para poder correr comandos dentro:

```
git worktree add --detach <ruta-desechable> origin/main
cd <ruta-desechable> && git merge --no-ff --no-commit --no-edit revisa-pr-<X>
```

**Ese** directorio es el universo de los once puntos. Cuando un punto de
abajo dice "sobre la vista previa", es aquí.

### 1.3 · Retira el worktree al cerrar

`git worktree remove --force <ruta-desechable>` y
`git branch -D revisa-pr-<X>`, siempre, incluso si la revisión termina
en `NO-FUSIONAR` o en PARO. El guardrail 0 lo exige.

### 1.4 · Modo `--post-hoc`

Sobre un PR **ya fusionado**: la vista previa no se construye, **es** el
merge que ya ocurrió (`<merge>^1..<merge>^2` para los commits,
`<merge>^1 <merge>` para el diff). En este modo **no se comenta en
GitHub**: el veredicto se escribe en `forense/notas/` y nada más. Es el
modo de calibración —comprobar que la lista atrapa lo que mesa atrapó a
mano— y es también el modo correcto para auditar un merge viejo sin
resucitar su conversación.

**Cómo llega ese veredicto a mesa** (`ACTO GEN2-E7` pieza D, D4b): en un
**PR propio**, titulado `[REVISA] post-hoc #<n>`, que contiene
**únicamente** la nota `forense/notas/<fecha>-revisa-<rótulo>.md`. Un
solo archivo en el diff, y ninguno más.

**Nunca commits sobre la rama revisada.** El guardrail 2 del bloque 0
sigue mandando aquí con esas mismas palabras —*«NUNCA empuja commits.
Cero `git push`, cero commits, en la rama del PR y en cualquier otra»*—
y este modo **no lo relaja**: lo satisface. La rama del PR `[REVISA]` es
**tuya**, nueva, `claude/revisa-post-hoc-<n>`, sacada de `origin/main`;
la rama revisada no se toca, no se checkoutea para escribir y no recibe
un solo byte. Si te encuentras a punto de commitear sobre la rama que
revisas, **PARA**: eso es exactamente el desenlace que el guardrail 2
existe para impedir, y ningún inciso de este bloque lo autoriza.

Un PR `[REVISA]` **no se fusiona solo** (guardrail 3) y **no aprueba
nada** (guardrail 1): es el vehículo para que la nota llegue al árbol,
no una firma.

### 1.5 · Selección en el barrido diario — `ACTO RUTINAS-2 · COORDINACION-Y-REVISION-VIGENTE` (P1)

El disparador «al abrir PR» (bloque 0) revisa el PR que lo disparó, punto.
Esta sección aplica **solo** al tick diario, que barre todos los PR
abiertos: filtra primero (excluye borradores y títulos `[TRAMITE]`/
`[REVISA]`, guardrail 6) y, del resto, elige el PR **elegible con
revisión pendiente desde hace más tiempo** — antigüedad del PR
(`created_at`), nunca antigüedad de su último comentario.

**Una revisión está pendiente** si no hay resultado vigente para las
referencias actuales del PR: helper compartido
`tools/rutinas.py::revision_esta_vigente` compara `(pr, HEAD, tip de
main, hash normalizado del cuerpo)` contra la última marca publicada
(§1.6). Mismo HEAD/main/cuerpo → vigente, no se vuelve a comentar.
Cualquiera de los tres distinto → pendiente.

**Sin candidato: `NADA-QUE-REVISAR`.** No hay salto automático a
`--post-hoc` — ese modo es solo por petición explícita de mesa (bloque
1.4). Si el PR del evento se fusionó mientras corría la revisión
ordinaria (verificado con `gh pr view <n> --json state` si `gh` está
disponible en este entorno, o releyendo `git ls-remote` de su rama):
termina `PR-YA-FUSIONADO` y **no** abras un PR `[REVISA]` de nota
automáticamente por eso.

### 1.6 · Identidad y marca del comentario — P1

Una revisión identifica **cuatro cosas**: número de PR, `HEAD` revisado,
`tip` de `origin/main` usado para construir la vista previa, y el hash
normalizado del cuerpo del PR (`tools/rutinas.py::body_sha256` —
detecta cambios de alcance o de `## NO-CORRIDO / RESERVAS` aunque el
código no cambie). El comentario del veredicto lleva, en una línea
propia, la marca:

```text
<!-- MM-REVISA:v2 pr=<n> head=<sha40> main=<sha40> body_sha256=<sha256> -->
```

Constrúyela con `tools/rutinas.py::construye_marca_revisa`, no a mano —
valida la forma de los tres hashes.

**Un comentario vigente por PR, no uno por revisión.** Busca, entre los
comentarios existentes del PR, el que traiga esta marca **y** la
identidad de la cuenta con la que esta sesión publica — no «cualquier
comentario de la cuenta»: `/tramite` y `/despacha` publican con la misma
cuenta y no dejan esta marca. Si lo hay: **actualízalo** (no publiques
uno nuevo) y conserva, en una línea breve, la referencia a la marca
anterior que reemplazas — no la borres del historial del hilo, el
comentario editado la lleva junto a la nueva. Si no lo hay, o el que hay
no trae marca reconocible (`tools/rutinas.py::parsea_marca_revisa` →
`None`): trátalo como si no hubiera revisión previa — **no presumas
vigencia sin evidencia de versión**, aunque el texto "se lea" como un
veredicto viejo de esta rutina.

**Relee antes de publicar.** Entre que empezaste la revisión y el
momento de comentar pueden haber pasado minutos: vuelve a derivar
`HEAD`, `tip` de main y el hash del cuerpo, y vuelve a leer el
comentario propio. Si algo cambió, **no publiques el veredicto como
vigente**: declara la revisión desactualizada y termina — el siguiente
evento o barrido la retoma. No entres en un bucle de revalidaciones. Si
otro disparo dejó ya el mismo veredicto (mismas cuatro identidades)
mientras corrías, no dupliques: esta sesión no tiene garantía de
exclusión mutua sobre otras (el entorno no la da), así que la relectura
final es la única defensa contra el duplicado — decláralo con esas
palabras si no puedes verificarlo.

---

## 2 · LOS ONCE PUNTOS

Reglas que valen para los once, y que son la mitad del valor de esta
skill:

- **Comando y salida, por punto.** Un punto sin comando pegado no está
  verificado; está opinado. Recorta la salida si es larga y **di que la
  recortaste**, pero nunca la parafrasees.
- **Un punto que no se pudo correr es `NO-VERIFICADO`, no un punto
  pasado**, y arrastra `RESERVA` por sí solo. Es la misma disciplina de
  A.13 aplicada al revisor: un negativo que nadie midió no es un
  negativo.
- **`NO-APLICA` se declara con su razón**, nunca en silencio. Los once
  puntos aparecen siempre en el comentario, los once, aunque ocho digan
  `NO-APLICA`.
- **Cada punto trae su peso**: `BLOQUEA` o `RESERVA`. El peso no lo
  eliges tú al final para que cuadre el veredicto; está fijado abajo,
  punto por punto, antes de conocer el PR.

### 2.1 · Encargo archivado verbatim (A.3), y coherente con el reporte

```
git diff --name-only origin/main...revisa-pr-<X> -- forense/encargos/
git log --oneline --reverse origin/main..revisa-pr-<X> | head -1
git log --oneline origin/main..revisa-pr-<X> -- <archivo-del-encargo>
```

Tres cosas, y las tres son mecánicas:

1. **El 0-bis es el primer commit.** El `git log --reverse | head -1`
   tiene que ser el que crea el archivo del encargo. Un acto que empezó
   a trabajar antes de archivar lo que le pidieron es un acto cuyo
   encargo ya no se puede auditar contra lo que hizo.
2. **El cuerpo no se editó.** Si el encargo aparece en más de un commit,
   el segundo sólo puede tocar líneas **después** de `## CONSUMIDO`.
   Verifícalo: `git diff <c1> <c2> -- <encargo>` y mira dónde caen las
   líneas.
3. **Coherencia con el reporte.** Lee los `P1`/`P2`/`P3`… del encargo y
   busca, para cada uno, el cambio que lo cumple. Un `P` que el reporte
   da por hecho y el diff no muestra es el hallazgo más caro de todos, y
   el único que ningún test de la suite atrapa. Un `P` **declarado no
   ejecutado, con su razón** (como `MAESTRA33-E4` declaró su `P1` al
   llegar vacío el corchete de firma) **no es defecto**: es la ranura
   funcionando.

**Peso: `BLOQUEA`** en los tres casos. El precedente de por qué (2) es
duro y no formal: `2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md` estuvo a un
paso de recibir un `## CONSUMIDO` falso que contradecía por escrito una
decisión de mesa ya registrada, y `grep -n CONSUMIDO tests/check.py` no
da nada — la suite no lo habría visto.

### 2.2 · Orden de commits: spec congelada ANTES de resultados

Sólo aplica **en actos que miden**. Deriva si mide, del propio encargo:
la línea `CONTADOR:`. `CONTADOR: cero, declarado` → `NO-APLICA`, y lo
dices con esa razón.

```
git log --format='%h %ad %s' --date=iso --reverse origin/main..revisa-pr-<X>
git log --format='%h' origin/main..revisa-pr-<X> \
  | while read c; do git show --name-only --format='' $c; done \
  | sort | uniq -c | sort -rn | head -20
```

El segundo comando es el que hace el trabajo: **todo archivo que aparece
en más de un commit es candidato a edición hacia atrás**, y se lee uno
por uno. Dos preguntas:

- ¿El commit que **congela la spec** (pre-registro, criterio, umbral,
  universo) es **anterior** al que reporta resultados?
- ¿La spec se tocó **después** de que los resultados existieran? Aunque
  el cambio "sólo aclare la redacción": una spec que se mueve después de
  ver el resultado deja de ser pre-registro, y el resultado deja de ser
  falsable. Nadie puede reconstruir después cuál de las dos versiones se
  usó.

**Peso: `BLOQUEA`.** Una edición hacia atrás sobre una spec no se
compensa con nada en el mismo PR.

### 2.3 · Perímetro declarado vs. archivos tocados

```
sed -n '/^PERÍMETRO/,/^LO QUE NO HACE/p' <archivo-del-encargo>
git diff --name-only origin/main...revisa-pr-<X> | sort
```

Compara los dos conjuntos **en las dos direcciones**, porque las dos
dicen algo:

- **Tocado y no declarado** → desbordamiento. Si el PR **lo declara con
  su razón** en el cuerpo o en el ADR (la casa lo hace: *"fuera de
  perímetro, reportado"*), es `RESERVA` y mesa decide. **Si no lo
  declara, `BLOQUEA`** — no por el archivo, sino porque el ejecutor no
  se dio cuenta, y lo que no se ve una vez no se ve dos.
- **Declarado y no tocado** → o el `P` no se hizo (vuelve a 2.1) o el
  perímetro estaba mal calculado. `RESERVA`, y se nombra cuál de las
  dos.

La frase vigente que este punto hace cumplir, verbatim de
`instrucciones-proyecto-v2_12.md:228`: *"si te encuentras escribiendo
fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo
vale más que el atajo."*

### 2.4 · Negativos con conteo de archivos (A.13)

Un negativo producido por un comando que no examinó archivos no es un
negativo. Localiza los negativos del reporte y de los documentos nuevos:

```
git diff --name-only origin/main...revisa-pr-<X> | grep -E '\.(md)$' \
  | while read f; do grep -nE 'cero|ninguno|ninguna|NO-ENCONTRADO|sin coincidencias|→ *0\b' "$f" /dev/null; done
```

Para cada uno, la pregunta única: **¿dice cuántos archivos examinó el
comando que lo produjo?** El modelo de la casa, verbatim de `ADR-243`:
*"0 coincidencias sobre 4 archivos `milpa/*.yaml` y 2413 líneas
examinadas"* — y, además, qué significa el cero (*"`milpa/` no usa hoy
ninguna de esas cinco claves — no es que las traiga en `false`"*).

**Peso: `RESERVA`**, salvo cuando el negativo es **portante** —una
premisa `A.8` sobre la que el acto construyó, un `NO-ENCONTRADO` que
justifica crear una pieza nueva—, y entonces **`BLOQUEA`**: si la
premisa era falsa, el acto entero se apoya en aire.

### 2.5 · Toda cifra del reporte, re-derivada por comando

**Ninguna cifra se acepta.** Ni las del encargo, ni las del ADR, ni las
de la nota de cierre. Lista las afirmaciones con número y re-deriva cada
una **sobre la vista previa**, con su comando a la vista. Al final
declara **cuántas re-derivaste y cuántas no pudiste**, con la razón de
cada una que no.

Este punto tiene el caso más limpio del repo, y es del lado bueno: el
encargo de `MAESTRA33-A1` declaraba *"15 filas `EXISTE-NO-VERIFICADO`"*;
el ejecutor no la heredó, corrió el `grep`, obtuvo **42** —coincidencias
léxicas en texto narrativo de otras columnas— y al leer la fila entera
descubrió que la respuesta real era **cero desde el 19/ago**. Una cifra
de dirección, re-derivada por el ejecutor, resultó falsa **en las dos
direcciones a la vez**. Eso es exactamente lo que este punto busca.

**Peso: `BLOQUEA`** para toda cifra que la re-derivación **contradiga**.
`RESERVA` para toda cifra **no re-derivable**, con la razón escrita.

### 2.6 · Originales intactos donde el encargo lo exija

```
git diff --numstat origin/main...revisa-pr-<X> | awk '$2 != 0 {print $2, $3}'
```

La segunda columna de `--numstat` son **líneas borradas**. Cruza esa
lista contra lo que el encargo exija preservar —*"absorbe las 5 colas
SIN borrarlas"*, *"quedan como histórico con puntero"*, *"el cuerpo
verbatim no se toca"*, *"la anotación nueva insertada antes de la
anterior, nunca reescribiendo la que ya estaba"*—. Para todo archivo
protegido, **líneas borradas = 0**, y el cero se pega.

Ojo con el falso positivo honesto: reindentar o reordenar un archivo
protegido produce borrados sin perder contenido. Sigue siendo hallazgo
—`RESERVA`— porque destruye la trazabilidad de `git blame`, que es la
mitad de por qué el original se conserva.

**Peso: `BLOQUEA`** si se perdió contenido. `RESERVA` si sólo se movió.

### 2.7 · Escala y universo declarados en cada cantidad medida (A-bis 3/4)

Toda cantidad medida declara **en qué escala** está (unidad, base,
denominador) y **sobre qué universo** se midió. Un `22` sin universo no
es un dato: es un carácter.

```
git diff origin/main...revisa-pr-<X> -- '*.md' | grep -nE '^\+.*[0-9]' | head -60
```

Para cada cantidad nueva: ¿trae unidad? ¿trae el conjunto sobre el que
se contó? ¿trae `N`? La suite ya vigila una consecuencia de no hacerlo
—`T06` lista hoy *"7 valores distintos de **Gini** en el corpus"* y
*"12 valores distintos de **confianza interpersonal**"*—, y esos números
divergen precisamente porque en su día entraron sin universo.

**Peso: `RESERVA`**, y **`BLOQUEA`** cuando la cantidad es una cifra
sobre México que entra al corpus o al canon — que es la clase que `T06`
lleva contando y la casa no quiere seguir pagando.

### 2.8 · ADR/FP candidatos, y renumeración si `main` se movió

```
# sobre la vista previa
grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1
grep -oE 'FP-[0-9]+' forense/firmas-pendientes.tsv | grep -oE '[0-9]+' | sort -n | tail -1
# contra origin/main, para detectar colisión
git show origin/main:canon/gobernanza-v1_15.md | grep -oE '^\*\*ADR-[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1
git show origin/main:forense/firmas-pendientes.tsv | grep -oE 'FP-[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1
# contigüidad: sin huecos
grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | uniq | awk 'NR>1 && $1 != prev+1 {print "hueco: " prev " -> " $1} {prev=$1}'
```

Cuatro comprobaciones:

1. **Colisión.** Si `origin/main` ya tiene el número que el PR
   candidatea, **el PR fusiona segundo y renumera** — regla de la casa.
   No es hipotética: `MAESTRA33-E3` renumeró `ADR-242→243` y
   `FP-209→210` porque `PR #414` fusionó primero, y con el número se
   movieron sus **tres** referencias cruzadas.
2. **Referencias cruzadas.** Renumerar y olvidar una cita deja el canon
   apuntando a un ADR que es otro. Búscalas todas:
   `grep -rn "ADR-<viejo>" canon/ forense/ .claude/` y declara el
   conteo de archivos examinados.
3. **Contigüidad.** Sin huecos.
4. **Cabeceras de conteo.** El `**N ADR**` de `canon/gobernanza-v1_15.md`
   línea 2 y el conteo de la línea `L0` de la ÚNICA FUENTE DE ESTADO vigente
   (`canon/estado-programa-v1_11.md`; `v1_10` retirada del árbol por `T01`,
   ver `ADR-301`) tienen que **coincidir entre sí** y
   con el máximo re-derivado.

**Peso: `BLOQUEA`** para colisión no renumerada, referencia cruzada
huérfana y cabeceras descuadradas — los tres meten al canon un error que
sobrevive al merge. `RESERVA` para hueco de contigüidad.

### 2.9 · `tests/check.py --baseline` sobre la vista previa

```
cd <ruta-desechable> && python3 tests/check.py --baseline ; echo "exit=$?"
git diff --stat origin/main...revisa-pr-<X> -- tests/baseline.json
```

`pip install -r requirements.txt` en `<ruta-desechable>` **antes** de correr
lo de arriba (A4, `ACTO GEN2-T11 · RUTINAS-FIX`, 8/sep/2026) — defecto real
medido: el `/revisa` post-hoc de `#619` corrió sin instalar `jsonschema`
(que sí está en `requirements.txt`) y su cifra de `WARN` no era re-derivable
por quien leyó su nota. Si el entorno no permite instalar (sin red, sin
permiso), no se deriva la cifra a ojo: se declara **`NO-VERIFICABLE`** con
el conteo A.13 de qué se examinó y por qué, nunca un número que nadie pudo
reproducir.

Dos cosas, y la segunda es la que importa:

- **VERDE** sobre la vista previa, no sobre la rama. Un PR verde en
  solitario puede ponerse rojo al fusionar; es la razón entera del
  bloque 1.
- **¿Cambió `tests/baseline.json`?** Si sí, el PR tiene que **decir por
  qué**, y la razón tiene que ser que una entrada se resolvió — nunca
  que estorbaba. Mover la línea base para que el rojo desaparezca es
  borrar el hallazgo y quedarse con el defecto.

Y una lección que la casa ya pagó **dos veces** y que a un revisor le
toca conocer: `T22(b)` y `T25` recorren `canon/` y `forense/`, así que
**la prosa que explica un marcador puede disparar el marcador**. Los
patrones exactos viven en `tests/check.py:1289-1291` y `:2320` — léelos
ahí, y no los copies a tu comentario: copiarlos es cometer el defecto
mientras lo describes.

**Peso: `BLOQUEA`** para rojo nuevo y para `baseline.json` movido sin
razón escrita.

### 2.10 · "Lo que NO hace", respetado

```
sed -n '/^LO QUE NO HACE/,$p' <archivo-del-encargo> | head -5
```

Convierte **cada** prohibición en un comando, y pega los diez ceros si
son diez. *"No toca `milpa/`"* →
`git diff --name-only origin/main...revisa-pr-<X> | grep -c '^milpa/'` →
tiene que dar `0`. *"No empuja a ramas ajenas"* →
`git log --oneline origin/main..revisa-pr-<X>` sólo sobre la rama del
PR. *"No aprueba ni fusiona"* → la lista de commits no trae ningún
merge a `main`.

Una prohibición que **no se puede convertir en comando** se declara así,
con esas palabras, y se verifica leyendo — pero se declara, no se salta.

**Peso: `BLOQUEA`.** Es la única sección del encargo que dirección
escribió pensando exactamente en lo que temía; violarla es hacer algo
que se prohibió por escrito.

---

### 2.11 · `## NO-CORRIDO / RESERVAS` cotejado contra el diff y el encargo — `ACTO GEN2-E7` pieza D (D4c)

**Peso: `BLOQUEA`.**

`A.14` dice: *«Lo que no se corrió se asienta, o el acto no cierra.»* El
punto 2.10 comprueba que el PR respetó su *«lo que NO hace»* declarado;
éste comprueba lo contrario y es el que faltaba: que **lo que el encargo
pidió y el diff no tocó** aparezca asentado, con su fila.

Tres lecturas, en este orden:

```
# (a) las piezas que el encargo archivado PIDE
git show <base>:forense/encargos/<archivo>.md | grep -nE '^\(?[A-Z][0-9]+\)?|^## '
# (b) lo que el diff REALMENTE toca
git diff --stat <base> <cabeza>
# (c) lo que el PR ASIENTA como no corrido
git diff <base> <cabeza> -- forense/no-corrido.tsv
```

El cotejo:

- Una pieza **pedida por el encargo**, **no tocada por el diff** y **sin
  fila** en `## NO-CORRIDO / RESERVAS` ni en `forense/no-corrido.tsv`
  → **`BLOQUEA`**. No es «se le olvidó documentar»: es una pieza que
  desapareció entre el encargo y el reporte sin que nadie lo diga, que
  es precisamente la forma en que un acto se declara completo sin serlo.
- Una pieza pedida, no tocada, **con** su fila y su razón → correcto.
  Ese es el mecanismo funcionando; no es un hallazgo.
- Una fila de `NO-CORRIDO` **sin** pieza que la respalde (asienta como
  no corrido algo que el encargo nunca pidió) → **`RESERVA`**: no es
  falso, pero infla el contador y merece decirse.
- Encargo sin piezas enumerables (los hay) → `NO-APLICA` **con su
  razón**, nunca en silencio.

**Cuidado con el falso positivo del entorno.** Un encargo de dos
entornos —piezas de nube y piezas de caja en el mismo texto— reparte su
trabajo en **dos PR**. Una pieza de caja ausente del PR de nube **no
bloquea**: se comprueba que el propio PR lo declare (cabecera del
encargo, o el reporte) y se anota como `NO-APLICA — pieza de <entorno>,
va en otro PR`. Bloquear ahí sería exigirle a un PR el trabajo que su
encargo mandó explícitamente a otra máquina.

---

## 2-bis · REVISA-CALC — el bloque que lee un cálculo, no sólo un diff — `ACTO GEN2-REVISA-CALC`

Especialización del mismo informe/comentario único de arriba, no un
segundo revisor ni una segunda rutina. Se aplica **dentro** de la misma
invocación de `/revisa`, con el mismo veredicto final y el mismo
guardrail 2 (nunca commitea, nunca empuja) — la evidencia de calibración
de este bloque la entrega el **ejecutor del acto** que lo redactó, en su
propio PR, no este agente.

### Activación

Cuando la vista previa del merge toca alguno de:

- `data/corrida0/CALC-*/`
- `forense/prereg-caja/`
- decisiones o vistas de corrida (`canon/estado-programa*`,
  `forense/no-corrido.tsv` con filas de CALC, registros de sello)
- afirmaciones de **ejecución**, **sucesión** o **adopción** en el cuerpo
  del PR
- citas nuevas `corrida0_*` añadidas a un consumidor

Un medidor compartido (`medidor.py` reutilizado por varios CALC) amplía
la revisión **solo a los consumidores afectados demostrables por sus
dependencias declaradas** — nunca dispara replay de todo el programa. Una
fila cambiada del TSV global de no-corrido/registro se resuelve por
identidad (qué CALC/RESULT cambió esa fila), no obliga a revisar todos
los CALC del árbol. `CONTADOR: cero` (guardrail 7) describe lo que este
agente mide sobre México — no excluye un CALC de la revisión: un cálculo
envuelto legacy puede declarar `CONTADOR: cero` y aun así requerir
revisión de sello y de conclusión.

Si nada de lo anterior aplica: `NO-APLICA`, sin peso, y el resto de este
bloque se omite del comentario.

### Comprobaciones — mecánica reutilizada + lectura humana

| Pieza | Comprobación mecánica reutilizada | Lectura humana necesaria |
|---|---|---|
| Identidad/sucesión | `python tools/corrida0.py estado <CALC>`; cadena del registro; sellos de antecesoras intactos | Qué objeto cubre la sucesora y qué residual conserva |
| Congelación | Orden por ascendencia de commits (`git log --ancestry-path`), no sólo timestamps; hashes y archivos gobernantes | Si un cambio posterior es spec sucesora declarada |
| Sello | Validador existente sobre recibo, sidecar y archivos cubiertos | Concordancia entre lo que el PR afirma y lo que quedó sellado |
| Replay | `python tools/corrida0.py verify` **sólo si el entorno lo permite** (nunca abre microdato en NUBE); conservar sus **tres** componentes — `contexto`, `resultado`, `veredicto` — y sus razones. `REPLICA-RESULTADO · CONTEXTO-DISTINTO` no se colapsa a un solo rótulo | Qué queda sin corroborar y si eso cambia la conclusión |
| Registro/status | `python tools/corrida0.py registro` / `status`, en modo lectura | Firma y clase E.1 explican por qué puede no moverse un contador |
| Adopción | Cita, generación, grano declarado, consumidor real, con los controles de adopción existentes | Compatibilidad del estimando con el parámetro; una nota no es una ranura de p |
| Inferencia | Resultados/cobertura y pruebas locales existentes de ramas del medidor | ¿La conclusión excede al intervalo, al universo o al diseño? ¿Una secundaria modifica indebidamente la primaria? |

### Entorno

En NUBE, este bloque verifica **estáticamente** contratos, sellos y
registro. Ver un payload listado en un censo no levanta la prohibición
del guardrail de abrir/descargar microdato (bloque 0 de `/revisa` y A.2
del acto). Lo que exige CAJA (un `verify` con lectura real de microdato,
por ejemplo) sale en el comentario como `NO-VERIFICADO` con **causa** y
**receta para caja** — y esa observación **no se escribe como estado
nuevo de ningún CALC**: es una nota de este revisor, no una entrada del
registro del programa.

Seis estados de fallo que no se confunden entre sí, ni se colapsan a
"no reproduce": **sello inválido** · **contexto no verificable** ·
**biblioteca ausente** · **input no visible** · **fallo de ejecución** ·
**divergencia numérica**. Cada uno tiene una causa distinta y una
receta distinta; usar el rótulo equivocado le da a mesa la corrección
equivocada.

### Pesos

- Contradicción **material** de identidad, sello, adopción o conclusión
  → **`BLOQUEA`**.
- Replay inaccesible por frontera declarada de entorno (CAJA requerida,
  corremos en NUBE) → **`NO-VERIFICADO`/`RESERVA`** — nunca degradado a
  aprobado ni a silencio.
- Falta legítima de firma o de adopción, **fuera del perímetro del
  encargo que se revisa** → explicación en el comentario, no defecto.

Estos pesos se combinan con los del bloque 3.1 (el veredicto sale de los
pesos, no del ánimo): un `BLOQUEA` de REVISA-CALC bloquea el PR igual que
un `BLOQUEA` de los once puntos.

### Calibración documental — cuatro casos, no receta congelada

Este bloque se calibró contra casos ya ocurridos, no contra una
especificación abstracta. Quien lo aplique puede releerlos como vara:

- **#634/#644** — semántica de verificación: qué distingue un `verify`
  que corroboró de uno que sólo no encontró motivo para objetar.
- **#647** — adopción con delta al grano: un cambio de representación no
  es automáticamente un cambio material.
- **#649 → #651**, el caso negativo y el positivo en la misma cadena:
  #649 **pasó la reproducción, 152/152 resultados exactos**, y aun así
  necesitó corrección — la reproducción prueba la transformación, no
  valida la inferencia que se construyó sobre ella. La corrección real
  fue de **adjudicación** (qué rama estadística mereció qué rótulo), un
  defecto que ningún replay mecánico iba a encontrar por sí solo. Este
  bloque no exige que la máquina lo descubra; exige que la **lectura
  humana** de la fila "Inferencia" de la tabla de arriba lo haga visible
  y lo cite cuando aplique a la revisión en curso. #651 es el positivo de
  la misma cadena: sucesión correcta reconocida sin pedir reescritura
  histórica, sellos de #649 intactos, y dos `RESULT` de destino
  corregidos sin abrir un segundo defecto.

**Pasa cuando** el bloque: detecta una afirmación material falsa (aunque
la reproducción numérica sea exacta) · reconoce una sucesora correcta sin
pedir que se reescriba la historia · conserva una reserva de entorno
declarada sin inventar una divergencia que no se pudo verificar. Una
calibración documental contra estos cuatro casos **no se rotula como
replay de CAJA** — es lectura del historial ya fusionado, no ejecución
nueva.

### Límite heredado del guardrail 2

El guardrail 2 (arriba, bloque 0) prohíbe absolutamente commits y push,
incluso en modo `--post-hoc` (bloque 1.4). Esta especialización no lo
relaja: si una calibración o una revisión de este bloque produce
evidencia que valdría la pena registrar en el árbol, esa evidencia la
**registra el ejecutor del acto que la originó, en su propio PR** —
nunca este agente. Cualquier cambio futuro a ese permiso queda explícito
en el encargo de dirección que lo autorice, nunca tácito ni inferido de
este bloque.

---

## 3 · EL VEREDICTO Y EL COMENTARIO

### 3.1 · El veredicto sale de los pesos, no del ánimo

- **`NO-FUSIONAR`** — hay al menos **un** hallazgo de peso `BLOQUEA`.
- **`FUSIONABLE-CON-RESERVA`** — cero `BLOQUEA`, al menos un `RESERVA`
  (y `NO-VERIFICADO` cuenta como `RESERVA`).
- **`FUSIONABLE`** — cero hallazgos, y los **once** puntos con su
  comando y su salida pegados.

No hay cuarto veredicto, y **`FUSIONABLE` no significa "fusiona"**:
significa que la lista no encontró nada. Fusionar sigue siendo de mesa,
y sigue siendo la autorización.

### 3.2 · El comentario

**Uno solo.** En la nube se publica con la herramienta de GitHub de la
sesión (`mcp__github__add_issue_comment` — un comentario de
conversación, **no** una *review*, que es lo que mantiene vivo el
guardrail 1). Deriva qué herramienta tienes antes de usarla; no la
supongas.

Estructura, en este orden y sin adornos:

1. **`VEREDICTO: <uno de los tres>`**, en la primera línea, y debajo el
   recuento: `N BLOQUEA · M RESERVA · K NO-VERIFICADO · J NO-APLICA`.
2. **Las tres identidades** del bloque 1.1 (`BASE`, `HEAD` del PR, `tip`
   de `origin/main`) y el código de `merge-tree`. Sin esto, nadie sabe
   qué se revisó. **Y la marca de §1.6**, `<!-- MM-REVISA:v2 ... -->`, en
   su propia línea — es lo que hace vigente a esta revisión y lo que el
   próximo disparo lee para decidir si hay que repetirla.
3. **Hallazgos numerados**, ordenados por peso. Cada uno: **qué punto**,
   **qué se esperaba**, **qué se encontró**, **el comando y su salida**,
   y —si la tienes— **la propuesta de arreglo**, marcada como propuesta.
4. **La tabla de los once puntos**, los once, con su estado
   (`PASA` / `BLOQUEA` / `RESERVA` / `NO-VERIFICADO` / `NO-APLICA`) y su
   comando. Ésta es la parte que hace la revisión auditable: quien la
   lea dentro de un mes puede correr los mismos comandos.
5. **`CONTADOR: cero mediciones, declarado (infraestructura).`**
6. **Qué NO revisó este pase**, con su razón. Un revisor que no declara
   sus puntos ciegos se lee como si hubiera mirado todo.

Y la línea que cierra siempre, porque es el guardrail hecho texto:
**"Este comentario no aprueba, no fusiona y no empuja nada. Fusionar es
firmar, y firmar es de mesa."**

---

## 4 · CIERRE

Este agente **no** corre la cascada de `/acto`: no deriva `ADR`, no toca
`canon/gobernanza-v1_15.md`, no recifra `L0`, no censa rótulos, no abre
filas del tablero. Una revisión **no decide nada** —propone una
lectura—, así que no hay decisión que registrar. Si un día una revisión
necesitara un `ADR`, eso significa que dejó de ser revisión y se
convirtió en acto: **PARA y repórtalo**, no lo selles.

En `--post-hoc` sí hay un artefacto: el veredicto va a
`forense/notas/<fecha>-revisa-<rótulo>.md`, y **nada** se publica en
GitHub.

Retira el worktree y la rama local (bloque 1.3) antes de dar la revisión
por cerrada, pase lo que pase con el veredicto.

Falsador y caducidad (`forense/agente-revisor-v1_0.md` §3): si en un mes
mesa fusiona un PR con un defecto que esta lista habría atrapado, **se
añade el punto y se anota**; si la lista bloquea en falso **tres veces**,
se revisa la lista. Los dos criterios necesitan el caso citado.
