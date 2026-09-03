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

Ejecuta los cinco bloques de abajo, en orden. Cada uno es instrucción
ejecutable para esta sesión, no prosa de referencia.

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
5. **Perímetro duro, cerrado**, y son tres rutas:
   - `forense/firmas-pendientes.tsv`
   - `forense/digesto/`
   - la sección `## CONSUMIDO` de archivos en `forense/encargos/`
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
   Trabaja sobre una rama del día (`claude/tramite-<AAAA-MM-DD>`), nunca
   sobre `main`.
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

Si sale con **código 2**, no escribió nada: su auto-verificación de
marcadores detectó que un rótulo pelado o un marcador de `T22(b)`
sobrevivió a la neutralización. Eso es un defecto de `tools/digesto_
tramite.py`, y **arreglarlo está fuera de tu perímetro**: reporta la
salida cruda y termina con cero commits.

Lee el digesto entero antes de seguir. Las cuatro acciones del bloque 3
se deciden con lo que dice, no con lo que recuerdas.

---

## 3 · LAS CUATRO ACCIONES PERMITIDAS

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

---

## 4 · EL PR

**Uno solo**, título `[TRAMITE] digesto <AAAA-MM-DD>`. No lo fusiones y
no lo apruebes.

El cuerpo trae, en este orden y sin adornos:

1. **Resumen del digesto**: filas `ABIERTA` y la más antigua con sus
   días · veredicto de la suite · ramas ≠ `main` · encargos sin marca
   (accionables y pasivo, por separado).
2. **Qué se movió, con su cita.** Una línea por fila, con el
   `archivo:línea` de la firma. Si no se movió nada: "cero movimientos"
   — y está bien que sea cero.
3. **Qué NO se hizo y por qué.** La lista de lo que requirió juicio, tal
   como aparece en el digesto. Esta sección es el producto principal del
   agente, no un apéndice: es lo que mesa tiene que ver.
4. **`CONTADOR: cero mediciones, declarado (infraestructura).`**
5. **Perímetro tocado**, con `git diff --stat`. Si aparece una ruta
   fuera de las tres, el PR no se abre: se reporta el error de perímetro.

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
perímetro de tres rutas —a juicio de mesa, con el caso citado—, se
revisa la pieza que falló y se anota.
