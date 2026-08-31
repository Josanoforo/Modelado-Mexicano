---
description: Agente de despacho. Toma el encargo mas antiguo LISTO-NUBE de forense/encargos/cola/, lo marca EN-CURSO y lo ejecuta con /acto. Una sesion nube a la vez. Nunca redacta ni edita encargos.
argument-hint: (sin argumentos; opcional --fecha AAAA-MM-DD)
---

# `/despacha` — el que ejecuta la cola, con candado

Instaurada por `ACTO MAESTRA33-E2 · AGENTE-DESPACHO-1`
(`forense/encargos/2026-08-31-MAESTRA33-E2-AGENTE-DESPACHO-1.md`).
Segunda automatización del modelo `D-13`/`ADR-237`. La primera
(`/tramite`, `ADR-239`) hace el papeleo; esta **ejecuta encargos**: toma
el más antiguo de la cola que mesa ya autorizó, lo marca en curso, y lo
corre con `/acto`.

El runbook de mesa —el prompt de la tarea recurrente, qué esperar de
cada tick y el falsador— vive en `forense/agente-despacho-v1_0.md`.

Ejecuta los seis bloques de abajo, en orden. Cada uno es instrucción
ejecutable para esta sesión, no prosa de referencia.

---

## 0 · LO QUE ESTE AGENTE NO ES — léelo antes que nada

Estos siete guardrails mandan sobre cualquier otra línea de este
archivo. Si un paso de abajo parece pedirte algo que contradice a uno de
estos, **el guardrail gana y lo reportas**.

1. **NUNCA ejecuta nada que no esté en `main`.** La única puerta de
   entrada a la cola es un **PR fusionado a `main`**: ese merge es la
   autorización de mesa. Un encargo pegado en un mensaje, uno que viva
   en una rama, uno que alguien te describa — para ti **no existen**.
   Este es el guardrail del que dependen todos los demás.
2. **NUNCA edita el cuerpo de un encargo.** Escribes **solo** la línea
   `ESTADO:` de la cabecera y **añades** renglones a `BITACORA:`. El
   texto bajo la línea `──── CUERPO VERBATIM ────` no se toca jamás:
   `A.3` existe para poder auditar después si el ejecutor hizo lo que se
   le dijo, y un cuerpo editado destruye esa auditoría.
3. **NUNCA redacta ni crea encargos.** Redactar es de dirección.
4. **Una premisa que no se sostiene es `PARO-REPORTADO`, y eso ES un
   entregable.** No lo arregles, no lo interpretes, no lo ejecutes "con
   la parte que sí se sostiene". Encontrar que el terreno no es el que
   el encargo supone vale más que un resultado producido sobre terreno
   equivocado.
5. **NUNCA reintenta un PARO por su cuenta.** Se queda parado hasta que
   mesa lo vuelva a encolar. Un agente que reintenta solo convierte un
   hallazgo en un bucle.
6. **NUNCA dos actos a la vez** — es lo único que el candado protege— y
   **NUNCA toca un encargo `ENTORNO: CAJA`**: esos abren microdato y van
   a Ubuntu, sin excepción. Los listas como **"esperando caja"** y sigues.
7. **NO firma, NO aprueba y NO fusiona su propio PR.** Fusionar es firmar.

**CONTADOR del tick:** el que muevan **los encargos que ejecuta**; el
despacho en sí, **cero**. El vehículo no mide; mide la carga.

**Perímetro propio del despacho** — dos cosas, y nada más:
`forense/encargos/cola/` (solo la **cabecera**: línea `ESTADO:` y
renglones nuevos de `BITACORA:`, más el `## CONSUMIDO` del cierre) y lo
que el **encargo ejecutado** declare como suyo. Si te encuentras
escribiendo fuera de esas dos, **PARA** — el perímetro estaba mal
calculado y saberlo vale más que el atajo.

---

## 1 · ARRANQUE LIGERO

No es el ARRANQUE de cinco puntos de `/acto`: el despacho en sí no abre
microdato, no descarga nada y no toca `data/raw`. Dos líneas, y no
empieces sin ellas. (El encargo que ejecutes correrá **su propio**
ARRANQUE completo en el bloque 5; ahí es donde eso importa.)

1. **CLON.** Localiza el clon existente; no clones uno nuevo salvo que
   no haya ninguno, y si clonas, dilo. Reporta ruta absoluta y
   `git log -1 --format="%h %s"`.
2. **SHA.** `git fetch origin main` y compara `HEAD` con `origin/main`.
   Si `main` se movió, **refresca antes de nada**: la cola que vas a
   leer tiene que ser la de `main` de ahora, no la de tu clon de hace un
   rato. Reporta la diferencia.

---

## 2 · EL CANDADO — mecánico, antes de tocar nada

Dos comprobaciones. Si **cualquiera** de las dos da positivo: **reporta
y termina con cero commits**. Una sesión de nube a la vez.

`gh` **no existe** en este entorno (medido 31/ago/2026: `which gh` no
imprime nada y sale con 1; `gh --version` → `command not found`), así que
el candado es de `git` puro. No lo sustituyas por la API de PRs ni por tu
impresión de qué hay en vuelo.

**Las dos comprobaciones no son redundantes: cubren casos distintos, y
quitar cualquiera de las dos abre el hueco.** `2.b` es la que atrapa a una
sesión **viva**, porque durante todo un tick el `EN-CURSO` vive en una
rama sin fusionar y `main` no lo ha visto todavía. `2.a` atrapa el caso
contrario: un `EN-CURSO` que **sí llegó a `main`** —una sesión que empujó
su cerrojo, mesa lo fusionó, y el acto nunca terminó—. Si alguna vez te
parece que `2.a` "nunca salta" y sobra, es justo al revés: es la que
queda cuando la rama ya no está.

### 2.a · ¿Hay un `EN-CURSO` en la cola?

Se lee **de `origin/main`, no del árbol de trabajo**, y sin tocar nada:
es la misma regla dura del guardrail 1 aplicada al propio candado — lo
que no está en `main` no cuenta, ni siquiera para bloquearte.

```
git fetch origin main
git ls-tree -r --name-only origin/main -- forense/encargos/cola/ | wc -l   # universo (A.13)
for f in $(git ls-tree -r --name-only origin/main -- forense/encargos/cola/); do
  git show "origin/main:$f" | grep -q '^ESTADO: EN-CURSO' && echo "EN-CURSO: $f"
done
```

**Uno o más → CANDADO CERRADO.** Otra sesión está trabajando ese
encargo. Reporta cuál, con la fecha de su renglón de `BITACORA:`, y
termina.

⚠️ **Un `EN-CURSO` viejo NO lo limpias tú.** Si una sesión murió a
media ejecución, su `EN-CURSO` se queda y bloquea todos los ticks
siguientes — que es el comportamiento correcto: preferimos parados que
duplicados. Pero **decidir que una sesión murió es de mesa**, no tuya.
Lo que sí haces, siempre: **reportar su antigüedad** ("`EN-CURSO` desde
`<fecha>`, hace N días") para que mesa lo vea y lo desatasque. Un
candado que se bloquea en silencio es un candado roto; uno que dice
desde cuándo está cerrado es información.

### 2.b · ¿Hay una rama de acto abierta en el remoto?

```
git ls-remote --heads origin                                # estado VIVO
```

Es la **única** fuente primaria. `git for-each-ref refs/remotes/origin`
refleja el último `fetch` y puede listar ramas que el remoto ya borró:
úsalo **solo** si el remoto no responde, y **decláralo RESPALDO** en el
reporte (mismo criterio que la sección C de `/tramite`).

Una rama distinta de `main` **no basta** para parar: una rama fusionada
y no borrada seguiría ahí para siempre y te dejaría apagado. **"Abierta"
= no contenida en `main`**, y se prueba:

```
git fetch origin <rama>
git merge-base --is-ancestor FETCH_HEAD origin/main   # 0 = ya fusionada, no cuenta
```

**Alguna rama no contenida en `main` → CANDADO CERRADO.** Repórtala y
termina — **con su fecha**, igual que en `2.a`:
`git log -1 --format='%h %ci %s' FETCH_HEAD`. En régimen estable esta va
a ser la causa **más frecuente** de candado cerrado, porque el guardrail 7
te prohíbe fusionar tu propio PR: entre que un tick abre su PR y mesa lo
fusiona, la rama sigue abierta y la cola no avanza. Eso es deliberado —la
cola avanza al ritmo al que mesa firma—, pero mesa solo puede decidir si
le urge cuando ve **desde cuándo** está esperando. Un candado que se
cierra en silencio es un candado roto.

Los dos comprobantes **declaran cuántos archivos y cuántas ramas
examinaron** (`A.13`): un negativo producido por un comando que no miró
nada no es un negativo.

---

## 3 · SELECCIÓN — el más antiguo, determinista

También de `origin/main`, por la misma razón:

```
for f in $(git ls-tree -r --name-only origin/main -- forense/encargos/cola/ | sort); do
  c=$(git show "origin/main:$f")
  echo "$c" | grep -q '^ESTADO: LISTO-NUBE' && echo "$c" | grep -q '^ENTORNO: NUBE' && echo "$f"
done
```

El **primero** de esa lista es el tuyo: el nombre de archivo empieza por
la fecha (`AAAA-MM-DD-…`), así que `sort` ordena por antigüedad y los
empates del mismo día se rompen por el resto del nombre. Es
determinista, y esa es toda la gracia: dos sesiones que leyeran la misma
cola elegirían el mismo encargo, así que la exclusión la da el candado,
no la suerte.

**Si la lista sale vacía → COLA VACÍA.** Termina con cero commits, y
reporta las dos cosas: cuántos archivos examinaste (`A.13`) y qué hay
esperando. Los `ENTORNO: CAJA` se listan con su propio comando —siempre,
tanto si la cola tiene trabajo para ti como si no— y **no se tocan**:

```
for f in $(git ls-tree -r --name-only origin/main -- forense/encargos/cola/ | sort); do
  git show "origin/main:$f" | grep -q '^ENTORNO: CAJA' && echo "esperando caja: $f"
done
```

⚠️ Si el directorio `forense/encargos/cola/` **todavía no existe en
`main`**, estos comandos devuelven cero y el tick termina en COLA VACÍA.
Eso es correcto, no un error: la cola nace cuando mesa fusiona el PR que
la crea, igual que cualquier otro elemento suyo. Una cola vacía es información de mesa:
significa que dirección no ha encolado nada.

---

## 4 · MARCA `EN-CURSO` — commit propio, empujado antes de trabajar

Rama del tick: **`claude/despacha-<CÓDIGO-DEL-ENCARGO>`**, derivada del
nombre del archivo elegido y **no de la fecha de hoy**. Que sea invariante
es el mecanismo, no un detalle de estilo: dos sesiones que corran a la vez
eligen el mismo encargo (la selección es determinista), así que derivan
**el mismo nombre de rama**, y el segundo `push` lo **rechaza el remoto**.
Con la fecha dentro, dos sesiones que crucen la medianoche producirían
nombres distintos y ese freno desaparecería.

```
git fetch origin main
git checkout -B claude/despacha-<CÓDIGO> origin/main   # nunca sobre main
```

En la **cabecera** del archivo elegido, y en ningún otro sitio:

1. `ESTADO: LISTO-NUBE` → `ESTADO: EN-CURSO`
2. Un renglón **nuevo** al final de `BITACORA:` (los de arriba no se
   reescriben nunca):
   `- <fecha> · EN-CURSO · sesión de nube <id o rama del tick>`

Commitea **solo eso** y **empújalo antes de empezar el trabajo**, sin
forzar nunca:

```
git push origin claude/despacha-<CÓDIGO>          # JAMÁS --force ni --force-with-lease
```

Ese push es lo que hace que el candado del siguiente tick vea que hay algo
en vuelo: si lo dejas para el final, dos sesiones pueden solaparse
justamente en la ventana que el candado existe para cerrar.

**Si el `push` es RECHAZADO, has perdido la carrera: CEDES.** Otra sesión
llegó primera al mismo encargo. No fuerces, no renombres la rama, no
reintentes: descarta tu commit local (`git checkout -q origin/main`),
reporta **CANDADO CERRADO (perdida la carrera en el push)** y termina. Un
push rechazado no es un error de la herramienta: es el candado
funcionando, y es el único punto de todo el tick que es **atómico**, por
eso se le deja decidir.

### 4-bis · RE-VERIFICA el candado ya con tu cerrojo puesto

Entre el bloque 2 y este punto pasan segundos, y en esa ventana otra
sesión pudo pasar su propio candado. Con tu rama ya empujada, **vuelve a
correr `2.b`**:

```
git ls-remote --heads origin
```

Si aparece **otra** rama de acto abierta además de la tuya, **cede**:
deshaz tu marca (`git push origin --delete claude/despacha-<CÓDIGO>` solo
si el `EN-CURSO` es tuyo y de este tick), reporta y termina. Empatar y que
los dos sigan es el único desenlace que esta pieza no puede permitirse;
ceder de más solo cuesta un tick.

---

## 5 · EJECUTA — `/acto`, verbatim

```
/acto forense/encargos/cola/<archivo>.md
```

El cuerpo bajo la línea `──── CUERPO VERBATIM ────` es el encargo. Se
ejecuta **tal como está**. No lo resumas, no lo mejores, no lo
completes.

Dos costuras con `/acto` que hay que tener claras, porque son donde el
engranaje podría patinar:

- **El paso 3 de `/acto` (0-bis `A.3`) SE OMITE por completo.** No es una
  aclaración: es una instrucción. Manda archivar el encargo "si el archivo
  todavía no existe" — y existe: es este mismo archivo, y llegó a `main`
  por un PR fusionado, que es más garantía de la que da el propio paso 3.
  Ese paso nombra la ruta `forense/encargos/<fecha>-<ROTULO>.md`, sin el
  `cola/`, así que un ejecutor que lo siguiera al pie de la letra no
  encontraría el archivo ahí y **lo crearía**. **No lo copies a
  `forense/encargos/`**: `T02` agrupa por **basename normalizado**,
  descartando el directorio (`tests/check.py:183`; el `FAIL` se emite en
  la `:187`), así que la copia sería un `FAIL` de la suite, no una
  redundancia inofensiva.
- **La COMPUERTA del paso 2 de `/acto` sí se re-verifica**, con los
  comandos que el propio encargo declare. Que mesa lo encolara autoriza
  a **ejecutarlo**; no sustituye a comprobar que su compuerta se cumple.
  ⚠️ **El paso 2 de `/acto` busca una línea `GATED a …`, y los encargos de
  esta cola escriben su compuerta como `COMPUERTA: …`** (verificado:
  `grep -n GATED` sobre el primer elemento no da nada; `grep -n COMPUERTA`
  da su línea). No son dos cosas distintas: **`COMPUERTA:` ES la línea de
  compuerta** a efectos del paso 2, y se trata como tal. Que no haya
  ninguna `GATED a` **no** significa que el encargo no esté compuertado —
  leerlo así sería adelantar el acto sin verificar, que es exactamente el
  defecto que `/acto` existe para dejar de pagar dos veces
  (`ADR-224`, `ADR-234`).
- **`MODELO SUGERIDO`.** Los encargos declaran con qué modelo conviene
  correrlos (`grep -n 'MODELO SUGERIDO' <archivo>`). Tú **no cambias de
  modelo** —el de la sesión lo fija la tarea recurrente de mesa—, pero
  **lo lees y lo reportas**, y si no coincide con el de esta sesión lo
  dices en el PR. Un encargo que pide una receta congelada corrido con un
  modelo que se pone a opinar, o al revés, es un resultado que mesa tiene
  derecho a poder descartar sin tener que adivinar por qué.

El encargo ejecutado corre **su propia** cascada de cierre (`/acto`
paso 4: ADR, cabecera, recifrado `L0`, rótulos, `T25`, suite en línea
base) y declara **su propio** CONTADOR. El del despacho es cero.

---

## 6 · CIERRE — `CONSUMIDO` o `PARO-REPORTADO`

Un tick termina en uno de estos **tres**, y los tres son resultados
legítimos. El tercero —**CANDADO CERRADO**, incluido el tardío del
bloque 4 y el del `push` rechazado— ya se trató arriba: cero commits
empujados, y se reporta sin abrir PR.

### 6.a · `CONSUMIDO`

El encargo se ejecutó y su acto cerró. En la **cabecera**:

1. `ESTADO: EN-CURSO` → `ESTADO: CONSUMIDO`
2. Renglón nuevo de `BITACORA:`:
   `- <fecha> · CONSUMIDO · ejecutado por PR #N`

Y al **final del archivo**, la sección `## CONSUMIDO` que manda el paso
4.8 de `/acto`, citando el PR. Va **en el archivo de la cola** — es el
archivo `A.3` de ese encargo, no hay otro.

### 6.b · `PARO-REPORTADO`

Una premisa del encargo no se sostiene, su compuerta no se cumple, o el
terreno no es el que supone. **Es un entregable.** En la cabecera:

1. `ESTADO: EN-CURSO` → `ESTADO: PARO-REPORTADO`
2. Renglón nuevo de `BITACORA:`:
   `- <fecha> · PARO-REPORTADO · <la razón, verbatim, con el comando que la produjo>`

La razón va **verbatim y con su comando**, no parafraseada: es lo que
permite a mesa decidir si reencola, corrige el encargo o lo retira.

**Ojo con el "cero commits" de `/acto`.** Cuando la compuerta de un
encargo falla, `/acto` manda terminar con cero commits: eso se refiere a
**los pasos sustantivos del acto**, que no se adelantan "por si acaso".
Tus commits de cabecera (`EN-CURSO` → `PARO-REPORTADO`) **no son** pasos
del acto: son la contabilidad de la cola, viven en tu perímetro propio,
y son precisamente el entregable del tick. Sin ellos el `EN-CURSO` se
queda colgado y bloquea todos los ticks siguientes.

### El orden del PR y del número que se cita

Hay un orden y solo uno, porque un número de PR no existe hasta que el PR
está abierto, y el paso 4.8 de `/acto` pide citarlo dentro del archivo:

1. Empuja la rama con el trabajo del acto ya cerrado (cascada incluida).
2. **Abre el PR** — este, el del tick, es el **único** PR: `/acto`
   invocado desde aquí **no abre uno propio**. Toma su número.
3. En un commit **posterior**, sobre la misma rama, escribe la línea
   `ESTADO:`, el renglón de `BITACORA:` y el `## CONSUMIDO` **citando ese
   número**, y empuja.
4. Corre `python3 tests/check.py --baseline` por última vez **después** de
   ese commit, y pega el veredicto en el PR.

Si tu sesión no puede abrir el PR (`gh` no existe aquí), cita en su lugar
**la rama y los commits**, dilo en el reporte, y deja la rama empujada:
mesa abre el PR. Lo que no se hace nunca es inventar un número.

### En los dos casos

**Un PR, y no lo fusiones.** `gh` no existe aquí, así que el PR se abre
con el mecanismo que traiga la sesión (la integración de GitHub del
entorno, o la URL de `git push`, que el propio remoto imprime al crear la
rama). Si esta sesión no tiene ninguno, **no inventes uno**: deja la rama
empujada y repórtalo — la rama es el entregable y mesa abre el PR. Su
cuerpo trae, en este orden:

1. **Qué encargo se tomó** y por qué ese (el más antiguo `LISTO-NUBE`
   con `ENTORNO: NUBE`), con el conteo de la cola examinada (`A.13`).
2. **El candado**, con sus dos salidas crudas y sus conteos.
3. **El resultado**: `CONSUMIDO` con su PR, o `PARO-REPORTADO` con la
   razón verbatim.
4. **Lo que quedó esperando**, en particular los `ENTORNO: CAJA`.
5. **`CONTADOR`**: el del encargo ejecutado; el del despacho, cero.
6. **Perímetro tocado**, con `git diff --stat`. Si aparece una ruta
   fuera de la cabecera de la cola y del perímetro del encargo
   ejecutado, el PR **no se abre**: se reporta el error de perímetro.

Antes de abrir el PR corre `python3 tests/check.py --baseline` y pega el
veredicto. Si el tick dejó la suite fuera de línea base, **no abras el
PR**: reporta con la salida cruda.

Falsador y caducidad de esta skill (`forense/agente-despacho-v1_0.md`
§3): si en un mes el despachador ejecuta algo fuera de la cola o fuera
de `main`, o dos sesiones de nube coinciden por su causa —a juicio de
mesa, con el caso citado—, **se apaga la tarea recurrente** y se anota.
Mismo criterio que `D-10`..`D-13`.
