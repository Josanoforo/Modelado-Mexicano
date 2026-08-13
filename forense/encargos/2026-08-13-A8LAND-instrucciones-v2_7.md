Nota de archivado (A.3, `forense/encargos/convencion.md`). Este archivo no se commiteó "antes o junto con" el lanzamiento del acto, como pide la convención — el propio encargo A8-LAND no incluyó su archivo de encargo en su lista de perímetro declarada (omisión que sí incluyen sus precedentes recientes, p. ej. `2026-08-13-adr-provisionalidad.md:14`). Se detecta la brecha durante COMMIT 2 y se corrige aquí, en el mismo acto que la encuentra, en vez de dejarla pasar — es exactamente el tipo de hallazgo que A.8/A.9 (que este mismo acto sella) piden no pasar por alto. Declarado, no oculto. El texto de abajo es el encargo tal como se recibió, verbatim, sin editar.

---

# ACTO A8-LAND · sella `instrucciones-proyecto-v2_7.md` — A.8 y A.9

- **SHA de redacción**: `8b30306` (`origin/main`, merge #216 · ACTO SELLA / ADR-76 · verificado por comando el 13/ago/2026).
- **Entorno asignado**: **repo-only, NUBE.** NO requiere caja, NO requiere red, NO requiere `data/raw`. **NO lo lances en la caja** — ahí el turno es de `R5.1-D3`.
- **Estado**: `VIVO`.
- **Perímetro y concurrencia**: crea `instrucciones-proyecto-v2_7.md`; edita `canon/gobernanza-v1_15.md` (un ADR), `canon/estado-programa-v1_10.md` (cascada), `forense/encargos/convencion.md` (una línea), `forense/hallazgos.md`, `forense/notas/2026-08-13-a8-land.md`. **NO toca** `data/`, `milpa/`, `tests/`, `README.md`, `modelo-decision`, ni `instrucciones-proyecto-v2_6.md` (las versiones son append-only).
  Al escribirse: **cero ramas vivas**, verificado con `git branch -r`. Si al arrancar hay alguna que toque `canon/gobernanza`, **PARA** — dos actos sellando ADR contra la misma base es la colisión que ya ocurrió cuatro veces.
  Con la frase obligatoria: **"si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."**

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

**1 · REPO.** Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status`
⚠️ No arranques desde el home. ⚠️ `pwd` antes de todo comando de estado, y `git -C <ruta>` en vez de `cd` — el `cd` a un worktree hermano sin volver ya produjo una afirmación falsa que se sintió verificada porque el comando devolvió salida.

**2 · SHA.** Confirma contra qué base trabajas y compáralo con `8b30306`. Si `main` se movió: NO es PARO — refresca, **re-deriva el número de ADR con la receta de T15**, y reporta la diferencia antes de editar.

**3 · data/raw.** AUSENTE NO ES PARO y **este acto no la necesita**. Reporta el hecho y salta.

**4 · ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → reporta el valor crudo. **Este acto no toca microdato ni red: salta la sonda HTTP y dilo.** (Ver A.2: la firma tiene TRES partes; la tercera, `ls data/raw/`, tampoco aplica aquí.)

**5 · ESPEJO.** Prohibido derivar cifras del espejo del proyecto. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada aquí, por quien escribe ═══

**1 · ESTRUCTURA.** Dominio: *sellar una decisión de gobierno* (Dominio 7 de `data/INFRAESTRUCTURA-v1_0.md`). Tablas que gobiernan: `canon/gobernanza-v1_15.md` §4 + cascada obligatoria a `canon/estado-programa-v1_10.md`. **Escribe** las dos. **No escribe** `canon/modelo-decision-v4_0.md` — A.8/A.9 no tocan reglas ni tiers. **No escribe** `README.md` — no cita conteo de ADR (verifícalo antes de asumirlo).

**2 · CONTENIDO.** Verificado contra `8b30306`, salida cruda:
```
$ ls instrucciones-proyecto-v2_7.md
ls: cannot access 'instrucciones-proyecto-v2_7.md': No such file or directory
$ grep -c "A\.8" instrucciones-proyecto-v2_6.md                    → 0
$ grep -c "A\.9" instrucciones-proyecto-v2_6.md                    → 0
$ grep -c "VERIFICACIÓN DE EXISTENCIA" instrucciones-proyecto-v2_6.md → 0
```
**`NO-ENCONTRADO`** — buscado por nombre de archivo y por rótulo de regla en la versión vigente, 13/ago/2026.

**3 · COBERTURA RETROACTIVA.** `instrucciones-proyecto-v2_6.md` nació el **2026-08-05** (`git log --diff-filter=A`). Es la vigente y contiene A.4–A.7. No hay brecha: A.8 y A.9 gobiernan **hacia adelante** y **no reabren ningún encargo pasado** — reabrirlos en bloque sería la jornada del 30/jul otra vez.

════════════════════════════════════════════════════════════════════

## §0 · Qué hace este acto

Crea `instrucciones-proyecto-v2_7.md` = **copia exacta de `instrucciones-proyecto-v2_6.md`** con **cuatro inserciones** y **una sustitución de una línea**, todas dadas verbatim abajo. Después lo sella con un ADR.

**No edites `v2_6.md`.** Las versiones son append-only, mismo criterio que v2.4→v2.5→v2.6.

**El texto completo va inline en este encargo** (regla A.3): un encargo que necesita un texto que no está en el repo lo trae pegado, o no se lanza.

---

## COMMIT 1 — el archivo

### SUSTITUCIÓN 1 · línea 158 de `v2_6.md`

**Dice:**
```
Regla. Todo encargo abre con el bloque de abajo, textual y sin resumir. Un encargo sin él está mal escrito y quien lo reciba puede pedirlo antes de ejecutar.
```
**Queda:**
```
Regla. Todo encargo abre con los DOS bloques de abajo, textuales y sin resumir. Un encargo sin ellos está mal escrito y quien lo reciba puede pedirlos antes de ejecutar.
```

### INSERCIÓN 1 · el bloque nuevo de Bloque D

Va **inmediatamente después** de la línea de cierre `════...════` que sigue al punto `5 · ESPEJO` (línea 193 de `v2_6.md`), y **antes** de `Dos líneas más que el encargo debe traer, fuera del bloque.` (línea 195). Esa última línea cambia a: `Dos líneas más que el encargo debe traer, fuera de los bloques.`

```
═══ VERIFICACIÓN DE EXISTENCIA — la contesta quien ESCRIBE el encargo [NUEVO v2.7] ═══

1 · ESTRUCTURA. Qué tablas gobiernan este dominio, derivado de
    data/INFRAESTRUCTURA-v1_0.md (no de memoria). Cuáles escribe este
    encargo y cuáles deliberadamente no, con la razón de cada omisión.
    Si el índice no cubre el dominio: ese hueco es el entregable, y el
    encargo se detiene ahí.

2 · CONTENIDO. Comando ejecutado y salida cruda que demuestra que lo que
    este encargo manda producir NO existe ya. Un encargo que dice "no
    existe" sin comando está mal escrito. Resultado por objeto, con el
    vocabulario de A.4: EXISTE-SATISFACE / EXISTE-NO-SATISFACE /
    NO-ENCONTRADO (con dónde y con qué términos) / NO-ACCESIBLE.

3 · COBERTURA RETROACTIVA. Fecha de nacimiento de cada tabla gobernante
    (git log --diff-filter=A) contra la fecha del trabajo que se va a
    tocar. Si la tabla es posterior, decláralo: ese trabajo nunca pasó
    por ella y su ausencia NO prueba que no exista.

⚠️ Si (2) o (3) revelan que el trabajo ya está hecho, total o
   parcialmente: el encargo NO se lanza. Se reescribe sobre el faltante
   real, o se cancela. Descubrirlo aquí es el rendimiento de este bloque.

════════════════════════════════════════════════════════════════════
```

### INSERCIÓN 2 · nota de numeración en A.7

Va dentro de Bloque D-ter, **después** del párrafo que cierra *"Es la misma regla A.5 aplicada a un artefacto en vez de a un portal."* y **antes** de *"El costo de esta versión, contado. Tres reglas."* (línea 271).

```
⚠️ Nota de numeración. El rótulo A.7 está disputado: además de esta regla vigente, existen dos borradores sin sellar que reclaman el mismo número — el índice de infraestructura (absorbido por A.8, ver abajo) y la estampa de universo de ADR-67, cuyo texto no está en el repo y por tanto no es sellable. Quien selle cualquiera de los dos tiene que renumerar. Registrado en ADR-76(h).
```

Y en esa misma línea 271, `Tres reglas.` pasa a `Cuatro reglas.` y `manda sobre las tres` pasa a `manda sobre las cuatro` — el bloque tiene A.4, A.5, A.6 y A.7, y el conteo estaba mal desde que se escribió.

### INSERCIÓN 3 · Bloque D-quater, al final del archivo

```
Bloque D-quater · Delta v2.7 [NUEVO v2.7]

Por qué v2.7. Las seis versiones anteriores enseñaron a verificar lo que se afirma. Ninguna enseñó a verificar lo que ya existe, ni a comprobar que las reglas llegaron a quien tiene que leerlas. El 13/ago/2026 la dirección entregó una cola de descarga manual de 19 fuentes ordenada por palanca, y las dos primeras —GESIS/ISSP y WVS— ya estaban descargadas y registradas desde el día anterior. Ese mismo día se midió que las instrucciones que la conversación de dirección tenía cargadas estaban tres versiones atrás de las del repo. Las dos reglas de abajo salen de esos dos defectos. No retira nada.

A.8 · Ningún encargo se escribe sin verificar qué ya existe — la estructura y el contenido [NUEVO v2.7].

El defecto, medido y no concebido. El 13/ago/2026 la dirección entregó una cola de descarga manual de 19 fuentes ordenada por palanca. Las dos primeras — GESIS/ISSP y WVS — ya estaban descargadas y registradas desde el 12/ago: 16 y 11 entradas respectivamente en data/manifiesto.yaml, raíz descargas_mx, con url_origen poblado. El usuario las habría vuelto a bajar.

La causa no fue descuido, y por eso hace falta una regla. La cola se derivó de data/acceso-puertas-2026-08-13.tsv, que mide quién puede alcanzar el portal, cruzada con data/curacion-registro/necesidad-objeto-modelo.tsv, que dice para qué sirve. Nunca se cruzó contra data/manifiesto.yaml, que dice qué ya tenemos. Dos tablas de tres, y la que faltaba era la barata. Verificado además: acceso-puertas no tiene ninguna columna que ligue al manifiesto y ningún script la lee — el cruce no existe ni a mano ni por código.

La regla, en tres preguntas que todo encargo contesta antes de escribirse, en este orden.

(1) ¿Existe ya la estructura? Se deriva de data/INFRAESTRUCTURA-v1_0.md — qué tablas gobiernan el dominio del encargo — no de memoria. Si el índice no cubre el dominio, ese hueco es el entregable: se reporta y el encargo se detiene ahí, en vez de inventar una vía.

(2) ¿Existe ya el contenido? No basta saber dónde se escribe: hay que consultar la tabla gobernante por los objetos concretos que el encargo va a tocar, y pegar el comando y su salida. Un encargo que manda producir algo que ya está produce trabajo duplicado en el mejor caso y una entrada duplicada en el peor.

(3) ¿La estructura es posterior al trabajo que va a tocar? Si la tabla gobernante nació después del trabajo, ese trabajo nunca pasó por ella y su ausencia de la tabla no significa que no exista. Se declara la brecha con las dos fechas. Esto no es hipotético: manifiesto.yaml nació el 29/jul; relaciones.tsv el 7/ago; decisiones-adquisicion.tsv el 10/ago; universo-puertas el 11/ago; acceso-puertas, INFRAESTRUCTURA, crosswalk y cola-adquisicion el 12/ago; censo-explotacion el 13/ago. Todo lo trabajado entre el 29/jul y el 11/ago es invisible para las tablas de agosto salvo que alguien lo haya subido a mano.

Y la contraparte, para quien ejecuta. Si el encargo omite el bloque de VERIFICACIÓN DE EXISTENCIA (Bloque D, arriba), o afirma que algo no existe sin el comando que lo demuestra, se para y se reporta — igual que con cualquier premisa mal fundada. Encontrar que el trabajo ya estaba hecho es entregable, no interrupción.

Vocabulario: el de A.4, sin invento nuevo. EXISTE-SATISFACE · EXISTE-NO-SATISFACE · NO-ENCONTRADO (con dónde y con qué términos) · NO-ACCESIBLE. Prohibido escribir "no existe" o "falta" sin el comando al lado.

Qué le habría costado a un lector (impuesto de v2.3, pagado). Una tarde de descargas ya hechas, y —peor— entradas duplicadas en el manifiesto bajo ids distintos, que es exactamente el defecto de ACTO R / ACTO R″ del 12/ago: dos actos registraron los mismos payloads desde dos clones, y hubo que retractar uno.

Falsador y caducidad. Si en tres meses ningún encargo se detiene por esta regla y ninguna duplicación se evita, A.8 se retira y se anota. Si un encargo se detiene por ella y resulta que el contenido no existía —la tabla consultada no gobernaba ese dominio—, el índice estaba mal: se corrige el índice, no la regla.

Lo que A.8 deliberadamente NO hace. No añade un test: qué tabla gobierna qué dominio y qué contiene no es verificable desde la suite sin duplicar la lógica del propio índice. No exige mantener el índice al día por barrido periódico — se actualiza cuando un acto descubre que le falta algo (regla de conducto, ADR-70(c)). No se audita a sí misma: no hay pregunta nueva en el módulo de auditoría de rigor extremo. No reabre encargos pasados en bloque — gobierna hacia adelante.

Nota de numeración. A.8 absorbe el borrador del índice de infraestructura que reclamaba el rótulo A.7 — su regla es la pregunta (1) de arriba — de modo que ese rótulo queda disputado por dos y no por tres. La estampa de universo de ADR-67 conserva su reclamo y sigue sin poder sellarse hasta que su texto esté commiteado (ADR-76(h)).

A.9 · Una versión de instrucciones no está sellada hasta que está en los dos lados [NUEVO v2.7].

El defecto, medido el 13/ago/2026. Las instrucciones cargadas en la conversación de dirección estaban en v2.4 con A.4–A.6 pegadas a mano; el repo estaba en v2.6. Faltaban enteras A.1, A.2, A.3 y A.7, y el corolario retroactivo de A.6 estaba truncado — la mitad que dice que un tier bajo por falta de información es tan revisable como un NO-ENCONTRADO no estaba. No fue un desfase inerte: produjo tres defectos ese día. Cuatro encargos salieron sin instrucción de archivarse (A.3). El punto 4 del ARRANQUE se usó con dos partes en vez de tres (A.2). Y el alcance de A.6 se leyó acotado cuando el texto vigente lo tiene ancho.

La regla, y es una frase. Toda versión nueva de instrucciones se pega en el proyecto de Claude en el mismo acto que la sella en el repo. Si no está en los dos lados, no está sellada — y el ADR que la sella lo declara explícitamente, con la fecha del pegado.

Por qué hace falta y no basta con acordarlo. El repo avanza por PR y el proyecto de Claude se edita a mano; no hay mecanismo que los ate y ningún test puede verlo — el proyecto vive fuera del repositorio, misma exención que Bloque D. Lo único que cierra la brecha es que el mismo acto haga las dos cosas.

Falsador y caducidad. Si en tres meses ninguna sesión encuentra desfase entre las dos copias, A.9 se retira y se anota. Si se encuentra desfase habiendo A.9 sellada, el problema es que el ADR no lo declaró: se corrige la plantilla del ADR, no la regla.

El costo de esta versión, contado. Dos reglas y un bloque de plantilla. Las dos salen de defectos del mismo día: uno le habría costado al usuario una tarde de trabajo duplicado y al manifiesto una entrada duplicada; el otro ya costó tres defectos de dirección en una sola jornada. Si en tres meses ninguna ha atrapado nada, se retiran. La regla de señal manda sobre las dos: cada sesión produce una medición, o produce nada.
```

### INSERCIÓN 4 · cierre de la Nota de alcance

Va al final del archivo, después de todo lo anterior.

```
[NUEVO v2.7] Y la v2.7 atiende dos tropiezos que ninguna versión anterior podía ver, porque todas miran hacia la afirmación. Las reglas de procedencia preguntan "¿de dónde sacaste eso?". A.8 pregunta "¿ya lo teníamos?" — una afirmación puede estar impecablemente derivada de dos tablas correctas y seguir mandando a rehacer un trabajo hecho, porque la tercera tabla, la que dice qué hay, nunca se consultó. Y hay un agravante estructural que la pregunta (3) nombra: las tablas de este programa nacieron en fechas distintas, así que la ausencia de algo en una tabla joven no prueba nada sobre un trabajo viejo. A.9 pregunta algo aún más elemental y por eso nadie lo preguntó: "¿la regla llegó a quien tiene que leerla?" — un cuerpo de reglas impecable en el repo no gobierna nada si la sesión que dirige está leyendo una copia de hace tres versiones. Verificar la existencia cuesta un grep; verificar que las dos copias coinciden cuesta un diff. No verificarlas costó, el mismo día, una tarde del usuario y tres defectos de dirección.
```

---

## COMMIT 2 — el sello y la cascada

**Número de ADR.** Deriva **al sellar, contra el `main` real**, con la receta de T15 y **sin dejar hueco**:

```bash
python3 - <<'EOF'
import re, collections
t=open("canon/gobernanza-v1_15.md",encoding="utf-8").read()
n=[int(x) for x in re.findall(r"^\*\*ADR-(\d+)", t, re.M)]
print("únicos:",len(set(n)),"max:",max(n),"dups:",sorted(k for k,c in collections.Counter(n).items() if c>1),"huecos:",sorted(set(range(1,max(n)+1))-set(n)))
EOF
```
Contra `8b30306` da `únicos: 76 · max: 76 · dups: [] · huecos: []` → el tuyo es **77**. **T15 falla sobre huecos, no solo sobre el máximo.** La colisión ha ocurrido cuatro veces; si otro acto fusiona primero, renumera al fusionar `origin/main`.

**El ADR incorpora `instrucciones-proyecto-v2_7.md` verbatim** — precedente exacto: **ADR-59 hizo eso con v2.4**. Y declara en su cuerpo, explícitamente:

- **(a)** A.8, con el defecto medido que la origina.
- **(b)** A.9, **y en la misma línea la fecha en que el texto se pegó en el proyecto de Claude.** Si al sellar no se ha pegado, el inciso dice `PENDIENTE — no sellada hasta el pegado`, y no se marca vigente. Es la propia regla aplicada a sí misma en su primer uso.
- **(c)** que A.8 **absorbe** el borrador del índice de infraestructura, dejando el rótulo `A.7` disputado por dos y no por tres — coherente con ADR-76(h), que registró la colisión de tres vías.
- **(d)** que **ningún contador de medición sobre México se mueve**: `13 de 27` · `9 de 14` · `0 de 15` · `1 de 2` · `4 de 144`. **Ninguno.** Decláralo uno por uno.

**Cascada.** Cabecera de conteo en `canon/gobernanza-v1_15.md:2` · contador en `canon/estado-programa-v1_10.md` (tabla + párrafo §L0 · Gobierno). Derívalos y reporta la salida cruda:

```bash
grep -rn "[0-9]\+ ADR" canon/ README.md
```

**La cifra `N FAIL · M WARN` se recalcula por corrida real, nunca se copia.** Cuatro sitios del canon declararon cifras viejas el 13/ago y T16 los cazó.

**Una línea en `forense/encargos/convencion.md`:** todo encargo archivado lleva, además de la cabecera SHA/Entorno/Estado, el bloque de VERIFICACIÓN DE EXISTENCIA de Bloque D.

## Cierre

`python3 tests/check.py --baseline` VERDE, cifra reportada, **corrido antes y después**. Una línea en `forense/hallazgos.md` nombrando los dos defectos de origen. Nota del acto en `forense/notas/2026-08-13-a8-land.md` con los contadores movidos y los declaradamente no movidos.

**Merge local**, `main` HACIA la rama; el editor web de conflictos de GitHub está prohibido — no honra `merge=union` y `hallazgos.md` aparece como conflicto falso.

⚠️ **Y lo último, que es la regla estrenándose:** al cerrar el PR, entrega en el reporte **el texto íntegro de `instrucciones-proyecto-v2_7.md`**, listo para pegar en el proyecto de Claude. Sin eso, A.9 dice que la versión no está sellada — y el primer acto que la incumpla sería el que la escribió.
