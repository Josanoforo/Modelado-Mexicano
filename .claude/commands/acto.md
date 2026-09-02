---
description: Ejecuta el Bloque D (ARRANQUE + COMPUERTA + 0-bis A.3 + CIERRE en cascada) sobre un encargo de forense/encargos/. Uso — /acto forense/encargos/<archivo>.md
argument-hint: <ruta al encargo, en forense/encargos/>
---

# `/acto` — el Bloque D se ejecuta, no se transcribe

Sellada por `ADR-237` (`ACTO MAESTRA32-E19 · SELLA-CAMINO-1`, 31/ago/2026,
D-10 de `instrucciones-proyecto-v2_12.md`). Esta skill vive en el repo,
versionada — no hay copia en el proyecto de Claude que sincronizar (la
clase de desfase que A.9 vigila no le aplica). El texto verbatim del
ARRANQUE vive una sola vez, aquí; los encargos la invocan.

El argumento (`$ARGUMENTS`) es la ruta al archivo del encargo dentro de
`forense/encargos/`. Si el archivo todavía no existe en el repo pero el
operador lo pegó en el mensaje que invoca esta skill, el paso 3 (0-bis
A.3) es el que lo escribe — no un prerrequisito de este primer párrafo.

Ejecuta, en este orden, los cuatro bloques de abajo. Cada uno es
instrucción ejecutable para esta sesión, no prosa de referencia.

---

## 1 · ARRANQUE — hazlo antes de leer el resto del encargo

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo
no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el
encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no
    haya ninguno, y si clonas, dilo.
    Reporta:  ruta absoluta  ·  `git log -1 --format="%h %s"`  ·  `git status`
    ⚠️ No arranques desde el home. Si el cliente avisa "launched in your
    home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el
    encargo declara. Si main se movió: NO es PARO — refresca, re-deriva
    lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta
    por código; un clon fresco siempre nace sin ella. Se crea o se enlaza.
    Reporta:  existe / la enlacé a `<ruta>` / la creé.
    ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads
    quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el
    defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO — tres partes, no dos (A.2). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`
    describe el entorno; la sonda de red describe la red; ninguna de las
    dos describe el dato.
    - `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → esperado: `sin_variable`
    - `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/`
      (NUNCA `curl -I`)
    - Tercera parte (A.2): `ls data/raw/ 2>/dev/null | head -1` — ¿está
      montado el corpus compartido? Se espera ausente en la nube. Todo
      acto que abra microdato va a Ubuntu, sin excepción.
    Reporta los tres valores crudos. Si este acto no toca microdato ni
    red, dilo y salta este punto.
    ⚠️ A.13 — Un negativo producido por un comando que no examinó
    archivos no es un negativo. Todo veredicto negativo —incluida la
    sonda de este punto— declara cuántos archivos examinó el comando que
    lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está
    versiones atrás del repo y contiene archivos que el repo nunca tuvo.
    Toda cifra sale del clon de (1), con el comando a la vista.

---

## 2 · COMPUERTA

Busca en el encargo (el argumento de esta skill) una línea que declare
`GATED a …`, `Estado: GATED a …` o `COMPUERTA: …` — las tres formas son la
MISMA cosa y tienen la MISMA consecuencia (no cumplida → cero commits); el
formato corto v2.12 escribe `COMPUERTA:` y el largo escribía `GATED a`, y
reconocer solo una de las dos formas es no compuertar el acto. Si no hay
ninguna de las tres, el encargo no está compuertado — continúa al paso 3.
`COMPUERTA: ninguna` (o `ninguna de merge`) es una declaración explícita de
que no hay compuerta: no dispara verificación.

**Rótulo ambiguo.** Si la línea `GATED a X` / `COMPUERTA: X` cita un rótulo
sin serie — `E<n>`, `C<n>`, `A<n>`, `S<n>` pelado, sin el prefijo
`MAESTRA<nn>-` — la compuerta es AMBIGUA: no se resuelve por inferencia ni
por "el más reciente que calce". **PARO con cero commits**, con el texto
`rótulo ambiguo: cita MAESTRA<nn>-…`. Precedente: PR #437 resolvió `E13` a
`MAESTRA32-E13` — antes de ese PR, `E13` solo podía significar eso mismo si
alguien lo derivaba a mano; esta regla evita repetir esa derivación
implícita en cada acto.

Si hay una línea `GATED a X` / `COMPUERTA: X`:

1. `git fetch origin main` (o la rama que el encargo declare como base).
2. Verifica **por los comandos que el propio encargo declare** — nunca
   por defecto genérico — que `X` está fusionado/en el estado que el
   encargo exige contra `origin/main` real. La verificación es **por
   PRODUCTO**: el archivo o entrada concreta que el acto gateado debió
   producir (`git cat-file -e origin/main:<ruta>` o
   `git show origin/main:<ruta>`), o `git merge-base --is-ancestor`
   contra el SHA de merge que el encargo declare, o el mecanismo
   explícito que el encargo nombre. `git log --oneline origin/main |
   grep -c "X"` queda como **indicio, no como prueba**: `ADR-277` midió
   un falso positivo con este comando — el commit `bb54f99` ([COLA],
   asunto que nombra varios rótulos) hace que el `grep` cuente aciertos
   para rótulos que el commit solo menciona, no que el commit ejecutó.
3. Si la compuerta **no** se cumple: reporta con A.4/A.13 (qué se
   examinó, con qué comando, en qué fecha) y **termina con cero
   commits**. No adelantes ningún paso del acto "por si acaso" — el
   defecto que esta skill existe para dejar de pagar dos veces
   (`ADR-224`, `ADR-234`) es exactamente arrancar sin haber verificado
   la compuerta mecánicamente.
4. Si se cumple: repórtalo (comando + salida) y continúa al paso 3.

---

## 3 · 0-bis A.3

Primer commit del acto: el encargo, verbatim, en
`forense/encargos/<fecha>-<ROTULO>.md` — si el texto del encargo llegó
pegado en el mensaje que invocó esta skill y el archivo todavía no existe
en el repo, este commit es el que lo crea. Si el archivo ya existe (lo
creó un paso anterior de la misma sesión), no se re-escribe.

No se ejecuta ningún paso sustantivo del encargo antes de este commit.

---

## 4 · CIERRE — cascada estándar

Al terminar el objeto del encargo (o al cerrar por hallazgo, si el acto
no llega a arrancar), en el mismo commit o en el commit de cascada:

1. **ADR re-derivado por el comando de la casa** — nunca heredado de
   prosa ni de lo que "hoy daría":
   `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1`
   → candidato = máximo + 1, contiguo (sin huecos). Declara si hay otro
   acto en vuelo conocido que pueda tomar el mismo número primero — regla
   de la casa, renumera quien fusiona segundo.
2. **Cabecera.** Entrada nueva en `canon/gobernanza-v1_15.md` §4
   (Registro de decisiones), con el encargo citado (archivado por A.3,
   SHA de redacción) y, si aplica, el bloque **Gate verificado**.
3. **Recifrado L0.** `canon/estado-programa-v1_10.md`: el conteo de ADR
   de la línea `L0` sube (N → N+1), con la anotación nueva insertada
   antes de la anterior — nunca reescribiendo la que ya estaba. Cabecera
   de conteo de `gobernanza` (`**N ADR**`, línea 2) recifrada igual.
4. **`registro-rotulos`.** `canon/registro-rotulos.tsv`: censa el rótulo
   del acto (`ESPACIO-Nn`) y cualquier token pelado nuevo que el encargo
   o las notas de cierre traigan sin prefijo (D-6/ADR-128) — deriva con
   el mismo regex que T25 usa, no a ojo.
5. **T25.** Si el archivo nuevo trae un rótulo `M`/`E` pelado (verificado
   con el regex de `tests/check.py::_T25_ROTULO_BARE`), añádelo a
   `_T25_ARCHIVOS_CONOCIDOS` con el comentario que explica de dónde sale
   cada mención — mismo patrón que el resto de la lista. Un encargo
   verbatim (A.3) nunca se edita para complacer al test.
6. **`python3 tests/check.py --baseline`** en VERDE (sin `FAIL` nuevo
   contra `tests/baseline.json`), o PARO-reporta con la salida cruda —
   nunca se sigue con un `FAIL` nuevo sin reportarlo primero.
7. **Anti-PR#77.** Si este acto descargó algo: verifica que los payloads
   quedaron en el corpus compartido y no solo en el worktree de esta
   sesión, antes de dar el acto por cerrado.
8. **`## CONSUMIDO`** — añade esta sección al final del encargo
   archivado en el paso 3, con el PR (o el commit, si el acto no abre
   PR) que lo ejecutó. El encargo no se borra ni se edita en ningún otro
   punto: es el registro de qué se pidió, para poder auditar si el
   ejecutor hizo lo que se le dijo.
9. **Empuja y abre UN PR.** `git push -u origin <rama>` y abre **UN** PR
   contra `main` titulado con el rótulo del acto; **NO lo fusiones** — el
   merge es de mesa, y es la autorización, no un trámite del ejecutor.
   Excepción única: cuando el acto corre bajo `/despacha`, que ya hace
   este paso — no lo dupliques.

Falsador y caducidad de esta skill (D-13, `instrucciones-proyecto-v2_12.md`):
si en un mes la skill no evita ni un solo acto perdido por compuerta, o el
tamaño mediano de encargo no baja al menos 50%, o un lote deja pasar un
defecto de contenido que el formato largo habría atrapado — a juicio de
mesa, con el caso citado —, se revierte la pieza que falló y se anota.
