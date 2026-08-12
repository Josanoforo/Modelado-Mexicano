# ENCARGO A · NUBE · Abrir el renglón de "llaves de identificación ejercidas" — el contador que ADR-67(c) creó y que hoy no tiene casilla

- **SHA de redacción:** `931997c` (merge de PR #169, `origin/main`, 11/ago/2026)
- **Entorno asignado:** NUBE. **NO** se lanza en la caja local Ubuntu CC — ahí corren E4a/E4b/E4c, que sí tocan microdato, y este acto no lo toca. No se lanzan los dos carriles sobre los mismos archivos.
- **Estado:** VIVO
- **Bloquea a:** E4c (`R5.1-D2`). Sin este renglón, E4c produce un veredicto sin fila donde escribirlo.

**PROCEDENCIA DEL ENCARGO.** Todo lo de abajo fue derivado con comando contra un clon de `931997c` el 11/ago/2026. El defecto que lo motiva: `grep -rn "R5.1-D2"` devuelve solo prosa (`gobernanza:868`, `hallazgos:179`, `estado:99`, `propuesta-…-v0_3:218`) y ninguna casilla; y el parser canónico T18 (`tests/check.py`) matchea `` `R\d+\.\d+` → veredicto `[A-E]` ``, patrón que **no captura** `R5.1-D2` — el sufijo rompe el backtick de cierre. Verifica ambas cosas tú mismo antes de obedecer este encargo.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · `git log -1 --format="%h %s"` · `git status` ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a `<ruta>` / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` · `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` Reporta los dos valores crudos. NUNCA `curl -I`. **Este acto no toca microdato ni red**: reporta los dos valores para dejar la firma del entorno nube registrada (hoy `forense/hallazgos.md` tiene tres firmas y ninguna es concluyente sobre la nube) y sigue sin importar qué devuelvan.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

**PERÍMETRO Y CONCURRENCIA.** SOLO escribe: `forense/registro-llaves-identificacion-v1_0.md` (nuevo) · `canon/estado-programa-v1_10.md` (una línea de contador) · `forense/hallazgos.md` (append al final) · `forense/encargos/2026-08-11-A-renglon-llaves.md` (copia literal de este encargo, por `convencion.md`). **NO** toca `canon/gobernanza-*.md`, `canon/modelo-decision-*.md`, `milpa/`, `tools/`, `tests/`, `data/`, ni `forense/hitoD-preregistro-v2_0.md`. En paralelo puede estar corriendo E4a en la caja local Ubuntu (perímetro disjunto salvo `forense/hallazgos.md`): **si al rebasar hay conflicto en `hallazgos.md`, re-aplica tu entrada al final y jamás resuelvas borrando la ajena.** Si te encuentras escribiendo fuera de esta lista, PARA.

---

## PASO 1 · Verificación de premisas

```bash
git log -1 --format="%h %s"                                    # esperado: 931997c o posterior
grep -c "ADR-67" canon/gobernanza-v1_15.md                     # esperado: >=1 (si 0, PARA: #169 no está)
grep -rn "R5.1-D2" --exclude-dir=.git . | wc -l                # reporta el valor; esperado: solo prosa, ninguna casilla
grep -n "R5.1-D2" forense/hitoD-preregistro-v2_0.md            # esperado: ninguna línea (no debe entrar al 27)
sed -n '862,875p' canon/gobernanza-v1_15.md | grep -c "RENGLÓN PROPIO"   # ancla de ADR-67(c)
ls forense/registro-llaves-identificacion*.md 2>/dev/null      # esperado: no existe (si existe, PARA: alguien ya lo abrió)
```

Y la comprobación que decide el denominador — **no la teclees, derívala**:

```bash
grep -n "RUTA-I" forense/censo-estimabilidad-coeficientes-v1_0.md
```

`RUTA-I` está definido ahí como *"Identificada, llave sellada y no ejercida"*. **Deriva del censo cuántos de los 15 coeficientes de generador están clasificados RUTA-I y reporta el comando junto al número.** Si la receta que se te ocurra no discrimina limpiamente (el censo mezcla prosa y tabla), **reporta el valor crudo y el comando que lo produjo** en vez de afirmar una cifra: es preferible un denominador declarado como derivación imperfecta que uno tecleado. Si no se puede derivar de forma defendible, el denominador se escribe `POR DERIVAR` y se nombra como pendiente — no se inventa.

## PASO 2 · Crear `forense/registro-llaves-identificacion-v1_0.md`

Archivo nuevo, append-only por diseño, con esta estructura:

**Cabecera.** Qué es una llave: la compuerta de identificación que ADR-57(c) sella (`gobernanza-v1_15.md:623`) nombra tres vías (panel con el desenlace en el instrumento / experimento / diseño cuasi-experimental con regla exógena). Un coeficiente en `RUTA-I` tiene la llave **sellada y no ejercida**; ejercerla es correr un diseño pre-registrado que la use. Cita `forense/censo-estimabilidad-coeficientes-v1_0.md` como fuente de la taxonomía y `ADR-67(c)` como el acto que crea este contador.

**La regla de contadores, verbatim de ADR-67(c) y no reinterpretada.** El denominador `27` del Hito D **no se toca**; este registro es una población de conteo distinta. Ninguna fila de aquí mueve `13 de 27`, `0 de 15`, `9 de 14` ni `4 de 144`. Un veredicto anotado aquí es **PROPUESTO** hasta que mesa lo firme — la clase `A`–`E` del Hito D no aplica; la escala de cada fila es la que su propio pre-registro declaró (Bloque B-bis).

**La tabla.** Una fila por llave, columnas: `llave_id` · `coeficiente_o_regla` · `diseño` (panel / experimento / cuasi-experimental) · `preregistro_ref` (archivo:línea) · `estado` · `veredicto` · `escala_del_veredicto` · `fecha` · `ADR`.

Vocabulario de `estado`, cerrado y con la lección de B-bis incorporada — **la escala tiene fila para el caso en que el falsador no refuta**:

| estado | significa |
|---|---|
| `SELLADA_NO_EJERCIDA` | pre-registro sellado, diseño no corrido |
| `EJERCIDA_CORROBORA` | corrió y el falsador no refutó; la regla queda corroborada en el alcance declarado |
| `EJERCIDA_ACOTA` | corrió, no refutó, y el resultado acota el alcance de la regla — se dice a qué |
| `EJERCIDA_REFUTA` | corrió y refutó |
| `EJERCIDA_INDECISA` | corrió y el falsador resultó demasiado débil para decir nada — se dice por qué |
| `NO_EJECUTABLE` | el diseño no se pudo correr; se dice si fue por dato, por entorno o porque nadie corrió el mecanismo (las tres son hallazgos distintos y no se colapsan) |

Solo `EJERCIDA_*` cuenta como llave ejercida.

**Filas iniciales.** Las que el censo clasifique `RUTA-I`, todas en `SELLADA_NO_EJERCIDA`, más la fila de `R5.1-D2`:

- `llave_id`: `R5.1-D2`
- `coeficiente_o_regla`: la regla `R5.1` del Hito D — la pregunta sustantiva, no la operacionalización de ADR-58
- `diseño`: cuasi-experimental, diferencias-en-diferencias por grupo de elegibilidad (ENIGH 2018 → 2022)
- `preregistro_ref`: `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` (sellado 4/ago/2026, §9 sin enmiendas)
- `estado`: `SELLADA_NO_EJERCIDA`
- `escala_del_veredicto`: la de §6 del propio pre-registro — **cítala verbatim y no la reconstruyas**. Si su escala no contempla el desenlace "el falsador no refuta", **dilo en la fila y en el hallazgo**: es el defecto de B-bis y hay que verlo antes de correr, no después. En ese caso la fila queda con `escala_del_veredicto: INCOMPLETA — no nombra el desenlace de no-refutación`, y E4c arranca con la instrucción de reportarlo, nunca de forzar una fila.
- `ADR`: 67(c)

**La receta de conteo, al pie del archivo, probada.** Escribe el comando que deriva `llaves ejercidas N de M` desde la tabla y **córrelo antes de escribirlo**, contra un caso donde conozcas la respuesta (hoy N debe dar 0). Si tu primera receta cuenta el encabezado o una fila de ejemplo, corrígela y **deja escrito que la corregiste** — la advertencia de `instrucciones-proyecto` sobre `grep -c "^## R"` existe por esto.

## PASO 3 · Una sola línea en `canon/estado-programa-v1_10.md`

Añade el contador donde viven los demás (vecindad de `estado:95`, junto a `0 de 15` y `9 de 14`), con esta forma exacta y la cifra **derivada por tu receta del PASO 2, no tecleada**:

> **Llaves de identificación ejercidas: `0` de `N`.** *(Población de conteo propia, abierta por ADR-67(c); no toca el denominador 27 del Hito D. Registro: `forense/registro-llaves-identificacion-v1_0.md`; cifra derivada por la receta al pie de ese archivo.)*

**No añadas marcador `T20` ni test nuevo.** T20 hoy solo conoce `pob=reglas`; una población nueva exige tocar `tests/check.py`, que está fuera del perímetro, y bajo la regla de suficiencia de v2.3 un test se paga declarando el defecto real que atrapó — este contador todavía no se ha desajustado nunca. Déjalo como **pendiente nombrado para mesa**, a decidir cuando el contador se mueva por primera vez.

## PASO 4 · `forense/hallazgos.md` — una entrada, al final

Debe contener, sin adornos: que `R5.1-D2` se creó por ADR-67(c) **sin renglón donde anotarse** y que T18 no lo captura por construcción del patrón; qué archivo abre este acto; el denominador derivado con su comando (o `POR DERIVAR` si no se pudo, dicho así); si la escala de §6 del pre-registro de R5.1 cubre o no el desenlace de no-refutación; y `Contadores movidos: 0 — abre la casilla; la mueve E4c.`

## PASO 5 · Archivar el encargo

Copia **este archivo completo, literal**, a `forense/encargos/2026-08-11-A-renglon-llaves.md`, con la cabecera de `forense/encargos/convencion.md` (SHA · entorno · estado `VIVO`). Y añade a tu entrada de hallazgos una línea: los encargos del 10-11/ago (sellado ADR-67/68, pipeline-universo-motor, adenda celda-D) **no están archivados** en `forense/encargos/`, contra lo que esa convención exige desde el 5/ago. No los archives tú — están fuera de tu perímetro; solo deja constancia.

## PASO 6 · Suite, git, PR — NO FUSIONAR

`python3 tests/check.py --baseline`. La línea base está congelada sobre `2cf3e28`; **entradas nuevas se reportan en el PR, jamás se silencian**. Un archivo nuevo en `forense/` puede levantar WARN de nomenclatura o de mapa de evidencia: si aparece, se reporta con su texto crudo y se dice si se corrigió o se aceptó.

Rama `renglon/llaves-identificacion`. Commits: (1) el registro nuevo, (2) contador en estado + hallazgos + encargo archivado. PR: *"RENGLÓN: registro de llaves de identificación (ADR-67(c)) — abre la casilla de R5.1-D2 — NO FUSIONAR sin mesa"*.

## PASO 7 · Cierre — siete líneas

Qué cambió · por qué importa · qué habilita (E4c) · qué falta (marcador T20 si mesa lo quiere; la escala de §6 si resultó incompleta) · pruebas (suite cruda + la receta de conteo con su salida) · reservas (denominador derivado o pendiente; firma del entorno nube) · **contadores sustantivos movidos: 0 esperado, dilo explícito.**
