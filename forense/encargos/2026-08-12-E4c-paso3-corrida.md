# ENCARGO · E4c PASO 3 — la corrida real de R5.1-D2, con dos correcciones previas de canon

- **SHA de redacción:** `f8eb2e3` (merge de #182)
- **Entorno asignado:** CAJA LOCAL Ubuntu CC (microdato ENIGH, seis olas en disco). NO nube.
- **Estado:** CONSUMIDO — PR de la rama `mesa/e4c-paso3-corrida`, detalle en `forense/notas/2026-08-12-e4c-r5-1-d2-commit7-especificacion-ejecucion.md` y `forense/notas/2026-08-12-e4c-r5-1-d2-commit8-resultado.md`

---

12/ago/2026 · base declarada: origin/main = f8eb2e3 (merge #182) · suite VERDE 22 FAIL · 104 WARN, baseline en e7cd99d — verificados por comando al escribir

REVISIÓN DEL COMMIT 6 (ec8c1e2, ya en main vía #176): CORRECTO, y la reconciliación es la buena. Verificado: no edita los commits 1, 3, 4 ni 5 — solo apendiza su nota y una línea de hallazgos. Leyó la fila E del apéndice real y no de memoria. Y su conclusión se sostiene contra el texto: fila E es de un solo nivel (no distingue "decisivo en uno" de "decisivo en ambos"), así que EJERCIDA_CORROBORA propia queda correctamente retirada; y la precedencia sellada contradice la propuesta del Commit 1 §3 — monto insuficiente gana sobre E sin excepción por magnitud. Que el Commit 3 la hubiera retirado como propuesta en vez de dejarla como regla es lo que evitó que un ejecutor fijara por su cuenta algo que mesa decidió al revés.

El commit 6 señaló dos defectos fuera de su perímetro. Los dos son reales, verificados aquí, y uno es error mío al redactar el encargo de M-6. Van corregidos en el PASO 0 de abajo, antes de correr nada.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

ENTORNO ASIGNADO — y el que NO. Caja local (microdato ENIGH, seis olas en disco). NO nube. NO en paralelo en otro entorno. Firma 403 · host_not_allowed en sesión de microdato es PARO.

PERÍMETRO. SOLO: forense/r5-1-diseno-por-regla-preregistro-v1_0.md (PASO 0.1, movimiento de apéndice) · forense/registro-llaves-identificacion-v1_0.md (PASO 0.2, columna escala_del_veredicto de la fila R5.1-D2) · forense/notas/ (notas de los commits 7 y 8) · forense/hallazgos.md (append) · forense/encargos/. NO toca tests/, tools/, canon/, milpa/, data/, el bloque ## Registro de veredictos archivados de hitoD-preregistro, ni las notas de los commits 1-6. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

CONCURRENCIA. claude/new-session-xer383 y mesa/s-svystat-4celdas pueden seguir vivas — ninguna toca estos archivos, verifícalo. Único solapamiento posible: forense/hallazgos.md (merge=union). El merge va local, fusionando main HACIA tu rama, nunca por el botón de GitHub ni por su editor web — verificado y ahora canónico en .gitattributes (#182).

PASO 0 · Dos correcciones de canon, ANTES de abrir dato — commit propio, separado

Van en un commit aparte, antes del commit 7. No se mezclan con la corrida: son correcciones de ubicación y de estado, no de diseño, y deben poder auditarse solas.

0.1 · El apéndice de ADR-71(b) está en el lugar equivocado — y el error es del encargo de M-6, no de M-6

Verificado: el apéndice vive en :106, dentro del cuerpo de §6, antes del separador que lleva a §7. Pero §9 · Enmiendas (:142-146) dice, verbatim: "cualquier cambio a §2… §4… §5… o §6 (umbral/escala) posterior a la fecha del sello se anexa aquí como enmienda" — y §9 sigue diciendo "Ninguna a la fecha del sello" pese a que existe una enmienda real en el documento.

Causa, declarada: el encargo de M-6 instruyó "apendiza al §6 un apartado nuevo" sin verificar que el documento tenía una sección de enmiendas con regla explícita. M-6 ejecutó lo que se le pidió. El defecto es del encargo.

Arreglo: mueve el bloque del apéndice a ## 9 · Enmiendas, sustituyendo "Ninguna a la fecha del sello" por la enmienda fechada, con su texto verbatim, sin reescribirlo ni una palabra — el contenido lo selló ADR-71(b) y no se toca. En §6, donde estaba, deja una línea de puntero: "§6 fue enmendado el 12/ago/2026 por ADR-71(b) — fila E y precedencia A → E → B → C → D. Ver §9."

⚠️ Verifica después de mover: grep -c "fila \E`" forense/r5-1-diseno-por-regla-preregistro-v1_0.md` y que la fila E siga siendo localizable por su texto. Si el movimiento rompe alguna referencia cruzada, PARA y repórtalo.

0.2 · El registro de llaves quedó desactualizado por el sello

forense/registro-llaves-identificacion-v1_0.md:60, fila R5.1-D2, columna escala_del_veredicto, dice hoy: "INCOMPLETA — no nombra el desenlace de no-refutación" — fechada 4/ago/2026. Esa afirmación era correcta cuando se escribió y dejó de serlo el 12/ago, cuando ADR-71(b) selló precisamente la fila que le faltaba.

Arreglo: actualiza esa celda declarando que la escala está completa desde ADR-71(b), con la fila E y el orden A → E → B → C → D, y conservando la observación original con su fecha — no se borra un registro que era correcto, se le añade su cierre. estado sigue SELLADA_NO_EJERCIDA: la llave no se ejerce en este paso.

No inventes columnas ni cambies el estado. Si la fila no admite el texto sin cambiar su forma, PARA y repórtalo.

PASO 1 · Premisas de la corrida — corre y pega crudo
```bash
git log -1 --format="%h %s"                                          # f8eb2e3 o posterior
grep -c "def diff4_ultimate_cluster" tests/svystat.py                # 1 — ACTO S, ya en main
grep -c "fila \`E\`" forense/r5-1-diseno-por-regla-preregistro-v1_0.md   # ≥1 — ADR-71(b)
python3 tests/test_svystat.py                                        # 13 casos
python3 tests/check.py --baseline                                    # VERDE
ls data/raw | head                                                    # las seis olas de ENIGH
```

PARO si diff4_ultimate_cluster no está en main, o --baseline arranca en ROJO, o falta alguna ola que tu ventana necesite.

PASO 2 · Commit 7 — especificación de ejecución congelada, ANTES de abrir dato

No re-abre los commits 1-6; los cita y añade solo lo que falta para correr. Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

La llamada exacta. diff4_ultimate_cluster por ola; la resta entre olas con Var = Var(d4_post) + Var(d4_pre), hecha por el llamador. No implementes un did4_ — no está en tu perímetro y el Commit 5 §2 ya dejó dicho por qué no hace falta.
La magnitud mínima detectable del DDD, declarada antes de ver el dato (Commit 5 §3). Si no alcanza para despejar el umbral del §6 con la precisión que sí tiene el DiD de dos celdas, el DDD entra como robustez declarada y el §6 adjudica sobre el DiD principal. Decídelo aquí.
Los contadores de singleton de cada llamada, como salida obligatoria del reporte. El docstring lo exige: un singleton no detectado baja el SE en silencio.
El ancho de folioviv. El arreglo de ACTO J deriva el ancho de la propia concentradohogar de cada ola; no uses un zfill(10) fijo — corrompería 2012, que tiene esquema C(6) autoconsistente. Declara qué olas toca tu ventana y qué ancho resolvió cada una.
La escala de veredicto vigente, citada de §9 tras el PASO 0.1: orden A → E → B → C → D; fila E de un solo nivel; "monto insuficiente" de B gana sobre E sin excepción por magnitud. Y el estado de registro es EJERCIDA_ACOTA aunque los dos desenlaces resulten decisivos — se reporta cuántos cruzaron, sin promoverlo a un nivel que el diseño sellado no declaró (Commit 6 §2).

PASO 3 · Commit 8 — resultados, sin editar el 7

DiD y DDD con sus IC, en escala declarada (A-bis regla 3), más la sensibilidad (a) nominal junto a (b) deflactado, como el Commit 4 §1 comprometió.
La fila del §6 que corresponda, PROPUESTA a mesa. Nunca adjudicada aquí.
Si el punto satisface un umbral con un IC que no lo despeja: no adjudica. Se reporta como propuesta con la reserva escrita — contraparte de A-bis, por encima de toda la escala.
Si cae en la fila A, el Commit 4 §7 ya subió la vara: hay que explicar por qué difiere de tres estimaciones publicadas (86% / 37% / ~30%). No basta anotar el número.
Si aparece el caso de monto insuficiente con DiD decisivo: ya no se para para preguntar — ADR-71(b) lo resolvió, y resuelve a B (ambiguo). Se anota así, citando la precedencia sellada, y se declara en una línea que el resultado habría caído en E bajo la propuesta retirada del Commit 1 §3. Ese contraste es registro forense, no disputa.

Mesa adjudica en acto propio. Este acto no escribe en el bloque append-only de hitoD-preregistro.

PASO 4 · Cierre

Siete líneas · --baseline cruda · PR mesa/e4c-paso3-corrida, NO FUSIONAR sin mesa. Contador esperado: el primer resultado de R5.1-D2 medido con microdato. Es el que mide; los pasos 0 y 1 no.

Nota para mesa — una decisión que este acto NO toma y que ya tiene sus números

ACTO J midió que el join corregido deja R5.1 → A (ADR-58) expuesto en 2016 y 2018, y D5 → INESTABLE (ADR-53) NO expuesto — efecto cero, confirmado dos veces. Su propia estimación de costo: "cómputo trivial, minutos; el costo real es de adjudicación."

R5.1 y R5.1-D2 son fichas distintas —el Commit 1 §0 ya declaró la diferencia de diseño— así que la corrida de este encargo no depende de esa decisión y no debe esperarla. Pero cuando ambas existan, conviene que mesa las lea juntas: una regla cuyo veredicto original está expuesto por un defecto de join, y su diseño de falsación corriendo con el join ya arreglado.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-12-E4c-paso3-corrida.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-14-t-firmas.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
