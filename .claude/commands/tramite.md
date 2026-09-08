---
description: Agente de tramite. Corre la suite en linea base, emite el digesto del dia y redacta UN PR [TRAMITE] para firma de mesa. Nunca firma ni decide.
argument-hint: (sin argumentos; opcional --fecha AAAA-MM-DD)
---

# `/tramite` — el agente de fondo, con actor y con correa

Instaurada por `ACTO MAESTRA33-E1 · AGENTE-TRAMITE-1`
(`forense/encargos/2026-08-31-MAESTRA33-E1-AGENTE-TRAMITE-1.md`).
Implementa la práctica que `D-13` de `instrucciones-proyecto-v2_12.md`
dejó registrada sin implementar: un agente recurrente que corre la
suite, lista lo que envejece y redacta los PRs de trámite para firma de
mesa, para que el WARN diario deje de depender de que alguien abra la
suite a mano.

El runbook de mesa —el prompt de la tarea recurrente, cómo leer el PR y
el falsador— vive en `forense/agente-tramite-v1_0.md`.

**NUBE: no abrir ni descargar microdatos/corpus.** Se permite obtener
código, metadatos de GitHub y dependencias declaradas; instala requisitos
en el entorno según el flujo vigente, y si no se puede, declara la
limitación de la suite en el reporte.

Ejecuta los cinco bloques de abajo, en orden. Cada uno es instrucción
ejecutable para esta sesión, no prosa de referencia.

**Un `PARO` no autoriza reparar código.** Registra primero la huella
permitida (bloque 3.5) y reporta el fallo. Distingue registro local de
registro publicado: no afirmes que la huella quedó visible remotamente si
el `push` falló. Un bloqueo de la suite no justifica fusionar ni publicar
otros cambios como si hubieran pasado.

---

## 0 · LO QUE ESTE AGENTE NO ES — léelo antes que nada

Estos seis guardrails mandan sobre cualquier otra línea de este archivo.
Si un paso de abajo parece pedirte algo que contradice a uno de estos,
el guardrail gana y lo reportas.

1. **NUNCA firma.** Una firma es de mesa. Este agente solo puede
   PROPAGAR una firma que **ya existe verbatim en el repo**, citando el
   `archivo:línea` donde vive. Sin cita, la fila no se mueve.
2. **NUNCA decide.** No decide si un pendiente "ya no aplica", si una
   rama vieja se borra, si un encargo quedó sin efecto, ni si un WARN
   importa. Todo eso es de mesa/dirección.
3. **Lo que requiera juicio no se ejecuta — va como fila del digesto.**
   Esta es la regla que convierte una duda en entregable en vez de en un
   error. Ante la duda, no actúes: repórtalo.
4. **CONTADOR: cero, declarado.** Este agente no mide nada. Es
   infraestructura. El PR lo dice con esas palabras.
5. **Perímetro duro, cerrado**, y son cuatro rutas:
   - `forense/firmas-pendientes.tsv`
   - `forense/digesto/`
   - la sección `## CONSUMIDO` de archivos en `forense/encargos/`
   - `forense/rutinas.tsv` (una línea apendada por tick, bloque 3.5;
     `ACTO GEN2-E7` pieza D)
   **Nada más.** Ni `canon/`, ni `tests/`, ni `milpa/`, ni `tools/`, ni
   `.github/`, ni `data/`, ni este archivo. Si te encuentras escribiendo
   fuera de esa lista, **PARA** — el perímetro estaba mal calculado y
   saberlo vale más que el atajo.
6. **NO fusiona su propio PR**, y no lo aprueba. Fusionar es firmar.

Dos prohibiciones que se derivan de las anteriores y conviene tener
escritas, porque son las dos formas fáciles de romperlas:

- **No abre filas nuevas del tablero.** Abrir una fila es declarar que
  algo requiere firma, y eso es decidir. Un pendiente que este agente
  encuentre va como fila del **digesto**, y mesa decide si merece fila
  del tablero.
- **No edita un encargo archivado fuera de su sección `## CONSUMIDO`.**
  `A.3` lo prohíbe: el encargo es el registro verbatim de qué se pidió,
  y es lo que permite auditar después si el ejecutor hizo lo que se le
  dijo.

---

## 1 · ARRANQUE LIGERO

No es el ARRANQUE de cinco puntos de `/acto`: este agente no abre
microdato, no descarga nada y no toca `data/raw`. Tres líneas, y no
empieces sin ellas.

1. **CLON.** Localiza el clon existente; no clones uno nuevo salvo que
   no haya ninguno, y si clonas, dilo. Reporta ruta absoluta y
   `git log -1 --format="%h %s"`.
2. **SHA.** `git fetch origin main` y compara `HEAD` con `origin/main`.
   Si `main` se movió, refresca antes de editar y reporta la diferencia.

   **Rama: busca antes de crear** (`ACTO RUTINAS-2 ·
   COORDINACION-Y-REVISION-VIGENTE`, P3 — sustituye "siempre crea la
   rama del día"). Antes de tocar una rama, busca el PR `[TRAMITE]`
   abierto correspondiente a esta rutina y este repositorio, con rama y
   perímetro comprobados (`gh pr list --state open --search
   "[TRAMITE]"` si `gh` está disponible; si no, deriva por
   `git ls-remote --heads origin | grep claude/tramite-` y el estado de
   cada rama contra `main`). Pasa el resultado por
   `tools/rutinas.py::decide_pr_tramite`:
   - **`REUSA`** — un PR abierto: continúa **su rama real**, aunque el
     nombre lleve una fecha anterior. `git fetch origin <esa-rama>` y
     trabaja sobre su tip; **nunca** `git checkout -B ... origin/main`
     para reiniciarla — eso descarta sus commits. Push normal, nunca
     forzado.
   - **`CREA`** — ninguno abierto: usa la rama administrativa válida
     pendiente si existe; si tampoco, crea `claude/tramite-<AAAA-MM-DD>`
     desde `main`.
   - **`DUPLICADO`** — más de uno abierto: **declara la duplicidad con
     los números**, no crees otro ni cierres los existentes
     automáticamente. Termina y repórtalo — esto es juicio de mesa.

   Un PR `[TRAMITE]` anterior ya fusionado o cerrado no se reactiva: si
   `decide_pr_tramite` dice `CREA` porque el único que había ya cerró,
   el ciclo nuevo es exactamente eso — nuevo, no una continuación.

   Trabaja en un **worktree administrativo separado** del worktree de
   cualquier acto en curso; no cambies de rama encima de cambios
   pendientes ni muevas archivos de un encargo para poder registrar la
   huella.
3. **SUITE.** `python3 tests/check.py --baseline`.
   - **VERDE** → sigue.
   - **ROJO** → **PARO**. Termina con cero commits y reporta la salida
     cruda. Un agente de trámite que commitea sobre una línea base rota
     mete su ruido encima del hallazgo de otro. La suite roja no es tuya
     para arreglarla: es un hallazgo, y va al reporte.

---

## 2 · EL DIGESTO

```
python3 tools/digesto_tramite.py
```

(añade `--fecha AAAA-MM-DD` si la tarea la fija; por defecto es hoy).

Escribe `forense/digesto/DIGESTO-<fecha>.md`. Es determinista y de solo
lectura sobre el árbol: no toca nada fuera de `forense/digesto/`.

Si sale con **código 2**, no escribió nada. Dos causas posibles, ambas
fuera de tu perímetro para reparar (reporta la salida cruda y termina con
cero commits):
- su auto-verificación de marcadores detectó que un rótulo pelado o un
  marcador de `T22(b)` sobrevivió a la neutralización;
- `forense/no-corrido.tsv` tiene cambios locales sin commitear (P1.6,
  `ACTO AUTO-DIGESTO-1 · CAMBIOS-DESDE-EL-ULTIMO-CORTE`, 8/sep/2026): el
  generador no puede atribuir ese contenido a ningún SHA de árbol en modo
  publicación. Versiona el TSV primero (fuera de tu perímetro: eso lo
  decide quien lo tocó) o, para una lectura de diagnóstico sin escribir,
  usa `--stdout`.

**Sección H, digesto incremental** (misma pieza): desde el 8/sep/2026 la
sección H ya no vuelca todo `forense/no-corrido.tsv` como si fuera
novedad -- compara por `id` contra el último digesto versionado en
`forense/digesto/` y reporta NUEVA / CAMBIO-DE-ESTADO / MODIFICADA /
AUSENTE-EN-CORTE-ACTUAL / SIN-CAMBIOS / `SIN-BASE-COMPARABLE`. Esto no
cambia tu perímetro ni tus acciones: sigue siendo lectura, tú sigues sin
decidir nada de lo que H nombre. `--base-nc-ref <sha>` es un flag de
diagnóstico (nunca lo necesitas en la corrida normal): fuerza la
comparación contra un SHA de árbol explícito en vez de auto-seleccionar
el último digesto; una ref inválida es error, código 2, nada se escribe.

Lee el digesto entero antes de seguir. Las cinco acciones del bloque 3
se deciden con lo que dice, no con lo que recuerdas.

---

## 3 · LAS CINCO ACCIONES PERMITIDAS

Son cuatro, cerradas. Cualquier otra cosa que se te ocurra hacer es
**fila del digesto**, no acción.

### 3.1 · Mover una fila a `FIRMADA`

Solo si su firma o su enterado **ya existe verbatim en el repo**, con
fecha. La prueba es mecánica: tienes que poder escribir el
`archivo:línea` de dónde sale, y el texto que copies a la columna
`firmada_en` tiene que ser el de esa línea, no una paráfrasis.

- Sí: mesa dijo "enterado x 8" en un encargo archivado por `A.3`, con
  fecha, y la fila es una de esas ocho.
- No: la fila "parece cumplida", "ya se hizo en el PR tal", "es obvio
  que mesa está de acuerdo". Eso es juicio → fila del digesto.

Al mover: `estado` → `FIRMADA`, y `firmada_en` con la cita y su fecha.
`ejecutada_en` **no** se rellena por parecido: una firma resuelve la
pregunta, no escribe el archivo (`ADR-94`; es lo que `T22(c)` vigila).

### 3.2 · Cerrar recibos

Un recibo es una fila cuyo `qué_se_firma` empieza por "Mesa recibe …":
lo que gatea no es una decisión sino el **enterado** de mesa. Mismo
criterio y misma prueba que 3.1 — el enterado verbatim, con fecha, y su
`archivo:línea`. Un recibo sin enterado en el repo **se queda abierto**
y va al digesto. La antigüedad no lo cierra; nada lo cierra salvo mesa.

### 3.3 · Añadir una marca `## CONSUMIDO` faltante

Solo sobre encargos que el digesto liste en **D.1** (en o después del
piso derivado). Los de **D.2** son pasivo histórico: nacieron antes de
que la convención existiera, y decidir cuál "ya no aplica" es de mesa.
**Enmienda (2026-09-03, ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166): el
pasivo histórico de D.2 quedó auditado — de aquí en adelante D.2 reporta
0, o únicamente lo que quede `## INDETERMINADO` tras esa auditoría
(ver `forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md`).**

**Puerta 0 — la bandera del digesto manda.** Una entrada de D.1 marcada
`⚠️ NO MARCAR` **no se toca nunca**, pase lo que pase con los pasos de
abajo. Va como fila del digesto y ahí se queda.

**Puerta 1 — el rótulo tiene que ser único.**

```
ls forense/encargos/ | grep -c '<ROTULO-DEL-ENCARGO>'
```

Si da **algo distinto de 1**, PARA con este encargo: fila del digesto.
Dos encargos que comparten rótulo comparten también el resultado del
`git log` de abajo, así que un mismo `PR` satisface la derivación para
los dos y uno de los dos recibiría una marca falsa.

**Puerta 2 — hay que LEER el archivo antes de escribir en él.** Si trae
`SUSTITUIDO`, `DEVUELTA-POR-MESA`, "no ejecutado", "no consumido" o
"queda como historia", entonces **no fue consumido y no se marca** —
por más que el `git log` diga que sí. Fila del digesto.

**Puerta 3 — la derivación del PR, y no vale otra:**

```
git log --all --merges --format='%h %s' --grep='<ROTULO-DEL-ENCARGO>'
git show --stat <merge> -- forense/encargos/<archivo>.md
```

- **Exactamente un** `Merge pull request #N`, **y** ese merge toca **ese
  archivo concreto**, **y** toca archivos además de él → añade al final
  del archivo una sección `## CONSUMIDO` citando `PR #N`. Nada más del
  archivo se toca.
- **Cero, o más de uno** → fila del digesto. No elijas entre candidatos:
  elegir es decidir.

Por qué cuatro puertas y no una — el caso que las obligó, medido en este
árbol el 31/ago/2026. `2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md` y
`2026-08-30-MAESTRA32-E3-EXTRACTOR-DTA-v2.md` comparten el rótulo
`MAESTRA32-E3`. El `git log` de la puerta 3 da **exactamente un** merge
(`PR #400`), y ese merge toca **los dos** archivos además de otros once:
la derivación "exactamente un candidato" se satisface, literalmente,
para ambos. Pero el v1 dice desde ese mismo `PR`, en su primera línea:
"**SUSTITUIDO por v2 (dirección, 30/ago/2026): no ejecutado, no
consumido; queda como historia.**" Un ejecutor que siguiera solo la
puerta 3 le habría escrito `## CONSUMIDO (PR #400)` encima —
**una falsedad que contradice por escrito una decisión de mesa ya
registrada**, y ningún test de la suite la habría atrapado (`grep -n
CONSUMIDO tests/check.py` → nada). El único freno habría sido que mesa
lo leyera al fusionar, que es exactamente la dependencia en la memoria
de alguien que `A.12` y `T22` existen para eliminar.

**Tope: 5 marcas por PR**, y el PR declara cuántas quedaron sin
proponer. Un PR de trámite que reescribe medio directorio deja de ser
revisable en dos minutos, que es la única razón por la que mesa lo
fusiona sin releer todo.

### 3.4 · Commitear el digesto

`forense/digesto/DIGESTO-<fecha>.md`. Siempre; es el entregable del día
aunque las otras tres acciones queden en cero. Un día sin nada que hacer
también es información, y sin el archivo no queda registro de que se
miró.

### 3.5 · Apendar la huella propia — `ACTO GEN2-E7` pieza D (D5d)

Una línea en `forense/rutinas.tsv`, **siempre**, incluidos los días en
que las otras cuatro acciones quedan en cero:

```
<fecha>	tramite	<resultado>	<detalle en una línea>
```

`<resultado>`: `HIZO:<PR>` si abriste el PR del día (o dejaste la rama, y
lo dices en el detalle) · `NADA-QUE-HACER` si el digesto salió y no hubo
nada que mover · `PARO:<razón>` si no pudiste cerrar.

Es la misma razón que en `/despacha`: un día sin movimientos y un día en
que la rutina **no corrió** se ven idénticos desde fuera, y la sección
`I` del digesto —que lee este archivo— sólo puede distinguirlos si la
línea está. Nunca reescribes una línea anterior; sólo apendas.

**Vocabulario normalizado — P4.** Usa `tools/rutinas.py::traduce_
resultado_rutina` para el token: `ABRIO`/`ACTUALIZO` de este agente y
`COMENTO`/`ACTUALIZO` corroborados de `/revisa` se registran como
`HIZO:<PR>`, con la acción y la URL en el detalle; `CANDADO`, `PARO` y
`PROMOVIO` conservan su significado sin traducir. Esto normaliza
**huellas nuevas** — no corrige filas antiguas del TSV.

**Huellas de `/revisa` — P4.** El revisor no escribe commits de huella:
su evidencia es el comentario marcado (`<!-- MM-REVISA:v2 ... -->`) y su
sesión. Consulta los comentarios marcados, revisiones anteriores
identificables por esa marca, y PR `[REVISA]` en la ventana de **7
días**, con `gh` si está disponible o con la entrada JSON temporal que
esta sesión obtenga por su integración de GitHub — nunca credenciales
nuevas en el repo. Deduplica por la identidad de revisión (`pr`, `head`,
`main`, `body_sha256`) y puedes incorporar sus referencias a
`forense/rutinas.tsv` como **filas nuevas**; nunca reescribas datos
históricos ni inventes ticks a partir solo de la fecha de un PR. Declara
repositorio, ventana, momento de consulta y si la paginación quedó
completa. Si el acceso es incompleto, no presentes un inventario
exhaustivo: di lo que faltó.

Sin GitHub disponible: declara `GITHUB-NO-VERIFICADO` y muestra las
huellas que sí hay en el TSV local — no mantengas fija la afirmación de
que `gh` no existe (se comprueba cada vez), y no informes "cero
revisiones" solo porque el TSV no tiene filas de `revisa`: una sesión sin
candidato puede legítimamente no dejar comentario ni fila.

**El archivo entra al perímetro de esta skill**: es la cuarta ruta del
bloque 0.

---

## 4 · EL PR

**Uno solo**, título `[TRAMITE] digesto <AAAA-MM-DD>`. Si el bloque 1
(punto 2) reusó un PR abierto, **actualízalo**: añade el digesto del día
nuevo conservando los digestos previos y su historial de commits, y
actualiza el título a `[TRAMITE] digesto <fecha más reciente>` — no abras
uno nuevo. No lo fusiones y no lo apruebes.

Si otro escritor avanzó la rama entre tu lectura y tu push: releé una vez
y reaplica únicamente tu huella propia si no existe ya (usa una clave
estable — el ID de sesión disponible; si no hay, deriva una del instante
original, actor y SHA observado, y consérvala durante el reintento). Ante
conflicto, **para sin sobrescribir**. Si `main` avanzó, intégralo solo si
es sin conflictos y vuelve a validar el diff final; un conflicto real es
resolución explícita, fuera de este trámite rutinario.

El cuerpo trae, en este orden y sin adornos:

1. **Resumen del digesto**: filas `ABIERTA` y la más antigua con sus
   días · veredicto de la suite · ramas ≠ `main` · encargos sin marca
   (accionables y pasivo, por separado).
   **Corrección de conteo (2026-09-04, restauración post-#527):** cuenta
   `ABIERTA` por **prefijo**, no por igualdad exacta de `estado` — varias
   filas cierran su estado con una glosa (`ABIERTA -- pendiente de firma
   de mesa`, `ABIERTA -- vence 2026-09-10`, …) y una igualdad exacta las
   pierde. La receta correcta:
   `awk -F'\t' '$6 ~ /^ABIERTA/' forense/firmas-pendientes.tsv` (no
   `$6=="ABIERTA"`, que hoy subcuenta: 2 de 6 filas realmente abiertas).
2. **Qué se movió, con su cita.** Una línea por fila, con el
   `archivo:línea` de la firma. Si no se movió nada: "cero movimientos"
   — y está bien que sea cero.
3. **Qué NO se hizo y por qué.** La lista de lo que requirió juicio, tal
   como aparece en el digesto. Esta sección es el producto principal del
   agente, no un apéndice: es lo que mesa tiene que ver.
3-bis. **Rutinas y revisiones** (secciones `I` y `J` del digesto, `ACTO
   GEN2-E7` pieza D). De `I`, las rutinas **sin huella** en la ventana de
   7 días, nombradas: una rutina sin huella no es una rutina sana, es una
   de la que no se sabe nada, y mesa es quien puede reactivarla. De `J`,
   las notas `[REVISA]` y las ramas `claude/revisa-*` de la ventana —
   declarando que son **huellas**, no el conjunto de PR, porque `gh` no
   existe en este entorno.
4. **`CONTADOR: cero mediciones, declarado (infraestructura).`**
5. **Perímetro tocado**, con `git diff --stat`. Si aparece una ruta
   fuera de las cuatro, el PR no se abre: se reporta el error de perímetro.

Antes de abrir el PR, corre `python3 tests/check.py --baseline` otra vez
y pega el veredicto. Si el digesto del día hizo que la suite deje de
estar VERDE, **no abras el PR**: reporta con la salida cruda. Es
exactamente el modo de falla contra el que P1 se blinda, y si aun así
ocurre, mesa tiene que enterarse el mismo día.

---

## 5 · CIERRE

Este agente **no** corre la cascada de `/acto`: no deriva ADR, no toca
`canon/gobernanza-v1_15.md`, no recifra `L0`, no censa rótulos. Un PR de
trámite no es un acto: no decide nada, así que no hay decisión que
registrar. Si un día un PR `[TRAMITE]` necesitara un ADR, eso significa
que dejó de ser trámite — **PARA y repórtalo**, no lo selles.

Falsador y caducidad (`forense/agente-tramite-v1_0.md` §3): si en un mes
un PR `[TRAMITE]` requiere retrabajo de mesa, o toca algo fuera del
perímetro de cuatro rutas —a juicio de mesa, con el caso citado—, se
revisa la pieza que falló y se anota.
