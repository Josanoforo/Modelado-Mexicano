# ENCARGO C · NUBE · Registrar el universo mínimo de búsqueda por fuente — la regla que faltaba, no el conocimiento

- **SHA de redacción:** `385884e` (merge de #173, `origin/main`, 11/ago/2026)
- **Entorno asignado:** NUBE. **NO** la caja local — ahí corren los actos de E4. Este acto no toca microdato, no descarga nada y no necesita `data/raw`.
- **Estado:** CONSUMIDO — PR #175. *(Re-verificado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS, contra `f3873c2`: `git merge-base --is-ancestor 3e071f0 f3873c2` OK; `canon/gobernanza-v1_15.md:928` [ADR-69] cita este mismo PR #175 al sellarse, y `data/UNIVERSO-MINIMO-FUENTE-v1_0.md` está en el árbol. Coincide con lo que la ADENDA de este mismo archivo ya reportaba.)*
- **Decisión de mesa que lo autoriza:** dictada por escrito el 11/ago/2026 en el hilo de dirección, tras el hallazgo de E4b. Este acto **no decide nada nuevo: registra lo decidido.**

**EL DEFECTO, DICHO CON PRECISIÓN — y la primera versión de este diagnóstico era falsa.** Una lectura preliminar afirmó que la Red Nacional de Metadatos del INEGI "no estaba en el universo de búsqueda de ningún acto del programa". **Es falso, verificado con `grep -rlni "rnm/index.php\|Red Nacional de Metadatos"`: aparece en diez archivos.** El programa la conoce bien — `forense/notas/2026-08-07-explora1.md` documenta que `/rnm/index.php/catalog/` **responde HTML real y es navegable por curl**, a diferencia de `/programas/`, que es una SPA; hay uso registrado de su API de búsqueda (`/rnm/index.php/api/catalog/search`) y de sus descargas directas (`/catalog/{id}/download/{n}`) para ENDIREH (801), ENADID, ENUT y ENCUP.

El defecto real es más fino y peor: **ese conocimiento vivió en notas de acto y nunca se convirtió en paso obligatorio.** El 11/ago, E4b declaró `periodo_levantamiento = NO_DETERMINADO` para ENASIC 2022 tras barrer, con rigor y universo declarado, el descriptor de 6 hojas y el PDF de 26 páginas. El dato estaba en `https://www.inegi.org.mx/rnm/index.php/catalog/922`, en una tabla, sección *Recolección de Datos*: **`Levantamiento · 2022-10-24 · 2022-12-16`**. El acto hizo todo bien salvo saber que había un tercer sitio, porque nadie se lo puso en la receta.

Un `NO-ENCONTRADO` con universo declarado pero incompleto es exactamente el defecto más caro de esta clase de trabajo: **el reporte queda impecable y la conclusión es falsa.**

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status` ⚠️ No arranques desde el home.

2 · SHA. Confirma contra qué base trabajas y compáralo con el declarado. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar. Hay tres ramas de E4 vivas; cuenta con que main avance.

3 · data/raw. AUSENTE NO ES PARO. Este acto no la necesita. Reporta y sigue.

4 · ENTORNO. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` · `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/`. Reporta los dos valores crudos. NUNCA `curl -I`. Este acto no toca red; los valores son para dejar la firma del entorno registrada. Sigue con cualquier resultado — **y si la sonda da 200, NO aproveches para descargar nada: eso es otro acto, con su propio perímetro.**

5 · ESPEJO. Prohibido derivar cifras del espejo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

**PERÍMETRO.** SOLO escribe: `data/UNIVERSO-MINIMO-FUENTE-v1_0.md` (nuevo) · `canon/gobernanza-v1_15.md` (append de ADR-69 + cascada T15 que la receta derive) · `canon/estado-programa-v1_10.md` (solo sitios de cascada del conteo de ADR) · `forense/hallazgos.md` (append) · `forense/encargos/2026-08-12-C-universo-minimo.md` (copia literal de este encargo). **NO** toca `data/inventarios/`, `data/manifiesto.yaml`, `data/curacion-*/`, `milpa/`, `tools/`, `tests/`, ni ninguna nota de acto previo. **Concurrencia:** `e4a`, `e4b` y `e4c` pueden estar vivas — perímetro disjunto salvo `forense/hallazgos.md`; si al rebasar hay conflicto, re-aplica tu entrada al final y **jamás resuelvas borrando la ajena**. Si te encuentras escribiendo fuera de esta lista, PARA.

---

## PASO 1 · Verificación de premisas

```bash
git log -1 --format="%h %s"                                          # esperado 385884e o posterior
grep -c -E "ADR-69|ADR-70" canon/gobernanza-v1_15.md                 # esperado 0 (si >=1, PARA: alguien ya selló)
grep -oE "^\*\*ADR-([0-9]+)" canon/gobernanza-v1_15.md | sed 's/.*ADR-//' | sort -n | tail -1   # esperado 68
grep -rlni "rnm/index.php|Red Nacional de Metadatos" --exclude-dir=.git . | wc -l   # reporta el valor
ls data/UNIVERSO-MINIMO-FUENTE*.md 2>/dev/null                       # esperado: no existe
grep -rnoE "[0-9]+ ADR\b" canon/*.md                                 # sitios de cascada T15, repórtalos uno a uno
```

Y la verificación que le da fundamento al ADR — **córrela y pega la salida cruda**, porque el encargo afirma un hecho sobre notas del repo:

```bash
grep -rn "navegable por curl\|SPA\|api/catalog/search" forense/notas/2026-08-07-explora1.md forense/notas/2026-08-08-explora2.md
```

Si esas notas **no** dicen lo que este encargo afirma, **PARA y repórtalo**: el ADR se fundaría en una cita falsa.

## PASO 2 · `data/UNIVERSO-MINIMO-FUENTE-v1_0.md` — el artefacto operativo

Archivo nuevo. Su función es que un acto pueda **citarlo y demostrar que lo recorrió**, no que alguien lo lea y se acuerde.

**Cabecera.** Qué es: la lista de sitios que un acto debe barrer **antes** de declarar `NO-ENCONTRADO` sobre un campo material de una fuente. Qué no es: una lista de dónde buscar fuentes nuevas (eso es `data/inventarios/` y `catalogo-fuentes-v2_0.md`, y no se toca aquí). Cita el caso que lo motiva: ENASIC 2022, 11/ago/2026, PR #173.

**La lista, para fuentes INEGI, en orden de costo creciente:**

1. **El payload y su descriptor** en `data/raw` — el ZIP de microdatos y el FD (`*_fd.xlsx` o equivalente).
2. **El PDF "Conociendo la base de datos"** de la edición, si existe.
3. **La ficha de la Red Nacional de Metadatos** — `https://www.inegi.org.mx/rnm/index.php/catalog/{id}`. Contiene, en secciones estructuradas: *Muestreo* (marco, estratificación, tamaño y selección de muestra), *Recolección de Datos* (**periodo de ejecución, periodo de levantamiento y periodo de referencia, en tablas con fecha inicio/fin**), factores de expansión **por tabla, con nombre exacto de columna**, tasa de respuesta, cuestionarios por sección, y política de acceso. Metadatos exportables en `/rnm/index.php/metadata/export/{id}/json` y `/ddi`.
4. **Los indicadores de calidad publicados** de esa ficha — coeficiente de variación, error estándar e intervalo de confianza oficiales, típicamente en `/rnm/index.php/catalog/{id}/download/{n}`. **Son un validador externo del estimado propio**, del mismo tipo que `validar_contra_publicado()` es para ENIGH.
5. **Los documentos de la biblioteca** que la ficha cite: Diseño muestral, Informe operativo y de procesamiento, Diseño conceptual — en `https://www.inegi.org.mx/app/biblioteca/ficha.html?upc={id}`.
6. **El DOF**, cuando la cifra buscada sea un umbral, un índice o una regla de programa — no un dato de encuesta.

**Anota el hecho de mecanismo que ya está documentado y que ahorra tiempo:** `/rnm/index.php/catalog/` responde HTML real y es navegable por `curl`; `/programas/` es una SPA y no. Cita la nota de origen, no lo re-descubras.

**Y la regla, en una frase:** *un acto que declare `NO-ENCONTRADO` sobre un campo material de una fuente INEGI enumera cuáles de estos seis niveles recorrió y cuáles no, con el mecanismo y la fecha. Un nivel no recorrido no es un hallazgo negativo: es un pendiente.*

**Caso resuelto, como ejemplo trabajado y no como adorno.** ENASIC 2022, ficha RNM 922, abierta el 11/ago/2026: `periodo_levantamiento` = `2022-10-24/2022-12-16`; `periodo_referencia` para variables sin ventana retrospectiva = *"El mismo día de la entrevista, de acuerdo a la variable"*; `FAC_ELE` confirmado como *"Ponderador de la población de 15 a 60 años. Tabla TPER_ELE"*. **Con la discrepancia interna declarada:** el apartado *Supervisión* de esa misma ficha dice *"del 24 de octubre al 10 de diciembre de 2022"*, seis días antes que la tabla estructurada. Se registran las dos y se dice cuál se toma y por qué. **No la resuelvas tú ni la ocultes** — es material para el acto de E4b, no para éste.

## PASO 3 · ADR-69 en `canon/gobernanza-v1_15.md`

Append después de ADR-68, con la forma `**ADR-69 · …**` al inicio de línea (T15 lo exige). El texto debe decir, en tus palabras y con las citas verificadas en el PASO 1:

- Qué sella: el universo mínimo de búsqueda por fuente como **requisito de un `NO-ENCONTRADO` sobre campo material**, con el artefacto operativo en `data/UNIVERSO-MINIMO-FUENTE-v1_0.md`.
- **La corrección de premisa, explícita:** el conocimiento sobre la RNM existía en el repo desde el 7/ago y fue el diagnóstico preliminar de mesa el que erró al decir que no. Lo que faltaba era la regla, no el conocimiento. **Corolario que sube a doctrina: un hallazgo que se queda en `forense/notas/` y no llega a una receta no protege de nada — el programa lo vuelve a pagar completo.**
- Qué **no** hace: no reabre ningún cierre negativo en bloque. Se aplica de aquí en adelante y, hacia atrás, **solo** donde un `NO-ENCONTRADO` esté hoy bloqueando un cálculo o una ficha — el resto se anota y se queda como está. Es el mismo corolario acotado de A.6, y existe para no repetir la jornada del 30/jul.
- Contadores que NO se mueven, declarado: `13 de 27`, `15 coeficientes cero medidos`, `9 de 14`, `4 de 144`, llaves ejercidas `0 de 2`.

**Cascada.** Los sitios de `N ADR` que la receta de T15 derive, `68 → 69`, reportados uno a uno.

## PASO 4 · `forense/hallazgos.md` — una entrada

El caso ENASIC con la cita de la tabla RNM; que el `NO-ENCONTRADO` de #173 era correcto dentro de su universo y que el universo era el defecto; la corrección de la premisa preliminar de mesa, con el conteo de archivos que la refuta; qué desbloquea (E4b puede completar su campo en un tercer commit — **no lo hagas tú, no es tu perímetro**); y la línea de contadores.

## PASO 5 · Propuesta para instrucciones v2.7 — redactada, no incorporada

Al final de tu nota de cierre, deja el texto listo para que mesa lo pegue en `instrucciones-proyecto` como **A.8**, en el estilo de A.4-A.6: una regla, su medición, y el caso que la pagó. Las instrucciones viven fuera del repo; **este acto no las edita**, solo entrega el párrafo.

## PASO 6 · Archivar, suite, git, PR — NO FUSIONAR

Copia este archivo literal a `forense/encargos/2026-08-12-C-universo-minimo.md` con la cabecera de `forense/encargos/convencion.md`. Corre `python3 tests/check.py --baseline`: entradas nuevas se reportan, **jamás se silencian** — un archivo nuevo en `data/` puede levantar WARN de nomenclatura. Vigila T15 y T19b: ninguno debe cambiar salvo el conteo de ADR.

Rama `regla/universo-minimo-fuente`. Commits: (1) el artefacto operativo, (2) ADR-69 + cascada, (3) hallazgos + encargo archivado. PR: *"ADR-69: universo mínimo de búsqueda por fuente — NO FUSIONAR sin mesa"*.

## PASO 7 · Cierre — siete líneas

Qué cambió · por qué importa · qué habilita · qué falta (el tercer commit de E4b; A.8 en instrucciones) · pruebas (suite cruda y la salida del grep de premisas) · reservas (la discrepancia de seis días en la ficha 922, sin resolver aquí) · **contadores sustantivos movidos: 0 esperado, dilo explícito.**

---

## ADENDA · Cierre real de PASO 1 — el encargo se fundaba en una cita falsa, corregida antes de sellar

*(Añadida por el acto que ejecutó este encargo, 12/ago/2026. La convención de este archivo prohíbe reescribir un encargo consumido; esto no reescribe el texto de arriba — lo deja intacto tal como se lanzó — sino que registra, al pie, lo que el PASO 1 encontró al correrlo. Ver `forense/hallazgos.md`, entrada del 12/ago/2026, "ENCARGO C", y `canon/gobernanza-v1_15.md` ADR-69(b), para el detalle completo.)*

El comando de la línea 40 arriba (`grep -rlni "rnm/index.php|Red Nacional de Metadatos"`, pipe sin escapar) no hace alternancia — da 0, no diez. Con el `\|` escapado que sí usa el párrafo de cabecera de este mismo encargo, da 34, no diez; buscando exclusivamente la frase `"Red Nacional de Metadatos"` sí da exactamente diez, que es lo que la cabecera afirma.

La verificación de fundamento (párrafo bajo el PASO 1, "córrela y pega la salida cruda") dio **sin resultados**: ni `forense/notas/2026-08-07-explora1.md` ni `2026-08-08-explora2.md` contienen `"navegable por curl"`, `"SPA"` ni `"api/catalog/search"`. Leídas completas, esas dos notas documentan lo contrario para su propia sesión. La cita real del hecho de mecanismo — verificada, y con el título literal *"El catálogo de microdatos (`/rnm/index.php/catalog/`) SÍ es navegable por curl"* — es `forense/notas/2026-07-31-perimetro-descarga.md` §4, no las dos notas de agosto que este encargo citaba. La lista de encuestas del párrafo de cabecera ("ENDIREH, ENADID, ENUT y ENCUP") tampoco coincide con la fuente real (`2026-07-31-cola-descarga-rederivada.md:110-111`, ENDIREH/ENADID/ENASEM/ENSU, y esos cuatro enlaces resultaron ser un producto-señuelo explícitamente no registrado — "nada bajado", línea 147).

Por instrucción propia del PASO 1 ("si esas notas no dicen lo que este encargo afirma, PARA y repórtalo: el ADR se fundaría en una cita falsa"), el acto se detuvo en este punto y reportó el hallazgo a mesa antes de escribir ningún archivo del perímetro. Mesa revisó y confirmó: el hecho de mecanismo subyacente es correcto y se refuerza con la cita corregida (cuatro contactos documentados con la RNM, no dos); el error era de cita, no de sustancia. Instrucción de mesa: corregir y continuar. El resto de este acto — `data/UNIVERSO-MINIMO-FUENTE-v1_0.md`, ADR-69, la entrada de `forense/hallazgos.md` — usa las citas corregidas, declaradas como tales en cada sitio.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-12-C-universo-minimo.md" canon/gobernanza-v1_15.md` → 0 (sin cita en ningún ADR). Rastro fuera de gobernanza, sin nota de cierre propia: tests/check.py. Insuficiente para CONSUMIDO, insuficiente para NO-EJECUTADO — rótulo/evidencia parcial, se lista para mesa.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
