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

`gh` **no existe** en este entorno (medido 31/ago/2026: `which gh` →
`command not found`), así que el candado es de `git` puro. No lo
sustituyas por la API de PRs ni por tu impresión de qué hay en vuelo.

### 2.a · ¿Hay un `EN-CURSO` en la cola?

```
ls forense/encargos/cola/*.md 2>/dev/null | wc -l          # universo (A.13)
grep -l '^ESTADO: EN-CURSO' forense/encargos/cola/*.md
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
termina.

Los dos comprobantes **declaran cuántos archivos y cuántas ramas
examinaron** (`A.13`): un negativo producido por un comando que no miró
nada no es un negativo.

---

## 3 · SELECCIÓN — el más antiguo, determinista

```
grep -l '^ESTADO: LISTO-NUBE' forense/encargos/cola/*.md | sort | while read f; do
  grep -q '^ENTORNO: NUBE' "$f" && echo "$f"
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
esperando, en particular los `ENTORNO: CAJA`, que listas como
**"esperando caja"** y no tocas. Una cola vacía es información de mesa:
significa que dirección no ha encolado nada.

---

## 4 · MARCA `EN-CURSO` — commit propio, empujado antes de trabajar

Rama del tick: `claude/despacha-<AAAA-MM-DD>-<CÓDIGO-DEL-ENCARGO>`.
Nunca sobre `main`.

En la **cabecera** del archivo elegido, y en ningún otro sitio:

1. `ESTADO: LISTO-NUBE` → `ESTADO: EN-CURSO`
2. Un renglón **nuevo** al final de `BITACORA:` (los de arriba no se
   reescriben nunca):
   `- <fecha> · EN-CURSO · sesión de nube <id o rama del tick>`

Commitea **solo eso** y **empújalo antes de empezar el trabajo**. Ese
push es lo que hace que el candado del siguiente tick vea que hay algo
en vuelo: si lo dejas para el final, dos sesiones pueden solaparse
justamente en la ventana que el candado existe para cerrar.

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

- **El paso 3 de `/acto` (0-bis `A.3`) ya está satisfecho.** Manda
  archivar el encargo "si el archivo todavía no existe" — y existe: es
  este mismo archivo, y llegó a `main` por un PR fusionado, que es más
  garantía de la que da el propio paso 3. **No lo copies a
  `forense/encargos/`**: `T02` normaliza el nombre de archivo sin
  distinguir directorio (`tests/check.py:187`), así que la copia sería
  un `FAIL` de la suite, no una redundancia inofensiva.
- **La COMPUERTA del paso 2 de `/acto` sí se re-verifica**, con los
  comandos que el propio encargo declare. Que mesa lo encolara autoriza
  a **ejecutarlo**; no sustituye a comprobar que su compuerta se cumple.

El encargo ejecutado corre **su propia** cascada de cierre (`/acto`
paso 4: ADR, cabecera, recifrado `L0`, rótulos, `T25`, suite en línea
base) y declara **su propio** CONTADOR. El del despacho es cero.

---

## 6 · CIERRE — `CONSUMIDO` o `PARO-REPORTADO`

Un tick termina en uno de estos dos, y los dos son resultados legítimos.

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

### En los dos casos

**Un PR, y no lo fusiones.** Su cuerpo trae, en este orden:

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
