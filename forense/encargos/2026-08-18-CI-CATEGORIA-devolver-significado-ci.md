ENCARGO · ACTO CI-CATEGORÍA — devolver el significado al CI

SHA de redacción: 997482b (merge #244, origin/main, verificado por git ls-remote el 18/ago/2026) Entorno asignado: NUBE (sesión nueva de Claude Code / claude.ai, clon fresco). NO lo lances en Ubuntu: ahí corre ACTO B2-V7 en paralelo. Dos actos en la misma caja ya tiraron una jornada. Estado: VIVO Precedencia: ninguna. Corre en paralelo con ACTO B2-V7; sus perímetros son disjuntos por construcción.
════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════ Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.
1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home.
2 · SHA. Este encargo se escribió contra 997482b. Si main se movió: NO es PARO — refresca, re-deriva, y reporta la diferencia antes de editar.
3 · data/raw. AUSENTE NO ES PARO, y este acto no la usa. Repórtalo y sigue.
4 · ENTORNO. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → reporta el valor crudo curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ ls data/raw/ 2>/dev/null | head -1 (tercera parte, A.2) Reporta los tres valores crudos. NUNCA curl -I. Este acto no toca microdato ni red de datos. Un 403 de INEGI aquí es un hecho sobre la allowlist de esta caja, no sobre INEGI (A.5): no lo escribas como si fuera un hallazgo sobre la fuente.
5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto. Toda cifra sale del clon de (1), con el comando a la vista. ════════════════════════════════════════════════════════════════════
═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe el encargo ═══
1 · ESTRUCTURA. Las tablas gobernantes de este dominio son tests/check.py (el vigía), tests/baseline.json (el congelado), canon/gobernanza-v1_15.md (los ADR) y forense/firmas-pendientes.tsv (el tablero, A.12). Este encargo escribe las cuatro primeras. NO escribe forense/firmas-pendientes.tsv salvo para añadir las filas del §4 — deliberadamente, porque cada fila nueva añade un WARN de T22 y eso es exactamente el fenómeno bajo arreglo; se añaden después del arreglo, no antes. data/INFRAESTRUCTURA-v1_0.md no gobierna tests/, verificado.
2 · CONTENIDO. Comandos corridos contra 997482b, salida cruda:
grep -c "require-cableado" tests/check.py                → 0
grep -n 'warn("T22"' tests/check.py                      → 1292, 1311
grep -n 'fail("T22"' tests/check.py                      → 1277, 1333
grep -n "SENAL\|def senal" tests/check.py                → (sin resultados)
El arreglo de categoría: NO-ENCONTRADO en tests/check.py — no existe ningún mecanismo para excluir una entrada de la comparación de línea base.
La regla del congelado en instrucciones: NO-ENCONTRADO en instrucciones-proyecto-v2_10.md (buscado por "congelad", "freeze", "línea base").
Las tres filas del §1 del transfer de dirección: NO-ENCONTRADO en forense/firmas-pendientes.tsv — el tablero llega hasta FP-48.
3 · COBERTURA RETROACTIVA. forense/firmas-pendientes.tsv nació el 14/ago/2026 (ADR-85); su columna encargo nació el 18/ago (ADR-94). Todo lo anterior al 14/ago es invisible para el tablero. Consecuencia medida y declarada aquí: 37 de sus 48 filas dicen SIN ENCARGO, y al menos una es falsa — FP-01..FP-06 (sello MOTOR-2) figuran SIN ENCARGO y su encargo existe en forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md. SIN ENCARGO hoy no es evidencia de ausencia. No derives nada de esa columna en este acto.
════════════════════════════════════════════════════════════════════
PERÍMETRO Y CONCURRENCIA. Este acto toca, y solo esto: tests/check.py · tests/baseline.json · canon/gobernanza-v1_15.md (ADR nuevo) · forense/firmas-pendientes.tsv (solo las filas del §4) · forense/notas/<fecha>-ci-categoria.md · forense/hallazgos.md (append, merge=union) · forense/encargos/ (marcar CONSUMIDO). En paralelo corre ACTO B2-V7 en Ubuntu, cuyo perímetro es .barrido2/ (fuera del repo), data/curacion-registro/** y forense/notas/<fecha>-b2-v7.md. Único punto de roce: tests/baseline.json. Está resuelto por instrucción explícita: B2-V7 tiene prohibido congelar. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
0 · El diagnóstico, ya hecho — no lo vuelvas a derivar
Está commiteado en main (9941adf, forense/hallazgos.md) y desarrollado en el transfer de dirección. En corto:
--baseline mete en el mismo saco regresión (defecto que esta rama introdujo) y señal (el vigía reportando deuda ya declarada). Como las trata igual, la única palanca es --freeze, que absorbe todo. T22(a) es el caso extremo y es un error de categoría: un test que dispara por diseño en cada corrida no puede ser un detector de regresiones.
Cifras, re-derivadas contra 997482b el 18/ago — y dos corrigen al hallazgo ya commiteado:
sh
git log --format="%h" -- tests/baseline.json | wc -l                                  # 29 commits tocan el archivo
git log --format="%s" -- tests/baseline.json | grep -icE "recongel|freeze|congela"     # 22 en toda la historia
git log --since="2026-08-17 00:00" --format="%h" -- tests/baseline.json | wc -l        # 7
Son 7 recongelados el 17–18/ago, no 6. 49edcd9 (17/ago 19:08 UTC) · b17abce · 5c8c806 · 565c650 · 120fbe2 · 4502461 · 1188f09 (18/ago 05:22 UTC). Diez horas, no catorce. El hallazgo de 9941adf dice "6 recongelados en 14 h"; corrígelo con enmienda fechada, sin borrar el texto original.
Ninguna ventana derivable da 14. 7 desde el 17/ago · 10 desde el 14 · 16 desde el 12 · 22 en total. Si dirección tenía "14" en mente, o es la mezcla con "catorce horas" o sale de un universo que no está declarado. Decláralo y sigue — el diagnóstico no depende de cuál sea la cifra, y discutirla sería la jornada del 30/jul otra vez.
1 · COMMIT 1 · El arreglo de categoría de T22
El mecanismo, especificado. No inventes uno distinto sin decir por qué.
Hoy hay dos buffers (tests/check.py:24) y la línea base los consume enteros (:1600, :1601, :1618). Falta una tercera categoría: la señal, que se imprime pero no compara.
Junto a FAILS, WARNS = [], [] añade SENAL = [] — el conjunto de claves (test, key) que se imprimen y quedan fuera de --freeze y --baseline.
Añade la función, con su docstring diciendo por qué existe (no qué hace):
python
   def senal(test, msg):
       """WARN de vigía: dispara por diseño en cada corrida, así que por
       construcción no puede ser un detector de regresiones. Se imprime
       igual —A.12 le encarga justamente gritar hasta que alguien atienda—
       y queda fuera de la comparación de línea base."""
       (FAILS if STRICT else WARNS).append((test, msg))
       SENAL.append((test, _baseline_key(msg)))
Cambia solo :1292 (ABIERTA desde) y :1311 (FIRMADA sin ejecutar desde) de warn("T22", …) a senal("T22", …). Deja intactos :1277 y :1333 — son fail, son la rama (b), y esa sí es regresión siempre.
Resta set(SENAL) en los tres sitios que consumen las claves: :1600, :1601 y :1618.
Los cuatro controles, y córrelos todos antes de commitear. Pega la salida cruda de cada uno.
#	qué haces	qué DEBE pasar
C1	añades una fila ABIERTA ficticia al tablero	línea base VERDE, y el WARN de esa fila sí se imprime en la corrida cruda
C2	creas un archivo en forense/ con marcador de ranura y sin fila	T22 FAIL y línea base ROJA
C3	renombras forense/firmas-pendientes.tsv	T22 FAIL (:1277) y línea base ROJA
C4	corres con fecha simulada a 2027-03-01	VERDE — no regreses el arreglo de ADR-88
C1 es el control positivo del cambio; C2 y C3 son los que prueban que no rompiste la protección. Si C2 o C3 salen verdes, el arreglo está mal y no se commitea. Revierte los cuatro escenarios antes de seguir.
Recongela una vez — y declara en el mensaje del commit que es el último recongelado autorizado bajo el régimen viejo, y que a partir del §3 rige otra regla.
2 · COMMIT 2 · T16 — y una cosa que dirección no sabía
Esto no es la colisión de clave que el transfer describe. Es anterior y más barata, y hay que resolverla primero o el arreglo de la clave se hace a ciegas.
Derivado el 18/ago contra 997482b: _suite_real() (tests/check.py:577) corre la suite en subproceso con CHECK_SELFCHECK_CHILD=1, que excluye a T16 de sí mismo — está documentado en su propio docstring: "la cifra contra la que este test compara es 'todo lo demás', no 'todo incluido yo mismo'". Por eso los tres mensajes de T16 dicen la corrida real da 19 FAIL · 132 WARN mientras el pie de la corrida imprime 22 FAIL · 132 WARN. La diferencia son exactamente los 3 FAIL del propio T16.
Consecuencia operativa, y es la trampa: quien resincronice gobernanza:1106, :1136 o :1658 copiando el total impreso escribirá 22 y T16 se queda rojo para siempre. La cifra que T16 acepta es 19.
Qué hacer, en este orden:
Verifícalo, no lo asumas. Escribe 19 FAIL · 132 WARN en una de las tres citas vigentes, corre la suite, y confirma que el punto fijo cierra: si los 3 FAIL de T16 desaparecen, el total impreso también baja a 19 y el subproceso sigue dando 19. Si no cierra, PARA y reporta — el punto fijo no existe y el remedio es otro.
Solo si cierra: resincroniza las citas vigentes y deja las históricas intactas. La distinción la hace _CAMBIO_FECHADO (:544), que solo reconoce > **vX.Y — DD/mon.** al inicio de línea. Si una histórica no lleva ese formato, no la reescribas para que pase el test — falsear el pasado para poner verde un vigía es peor que el rojo. Exenta por clave o decláralo como límite conocido.
Añade la aclaración del punto fijo como comentario en _suite_real(), con la fecha y quién lo derivó. Es la clase de cosa que se re-descubre tres veces.
Si (1) no cierra, este commit se cancela y el resto del acto sigue. No lo arrastres.
3 · COMMIT 3 · La regla, si mesa la firma
Redáctala, no la selles solo. Va a forense/firmas-pendientes.tsv como fila ABIERTA con el texto propuesto, y a gobernanza solo cuando mesa firme.
Un congelado no es la vía rutinaria al verde. Si un test obliga a congelar más de una vez, está mal categorizado: o es señal permanente y sale de la comparación, o es regresión y se arregla. El recongelado queda para el caso único y con ADR.
Falsador y caducidad, obligatorios (impuesto de v2.3): si en tres meses ningún congelado se evita por ella, se retira y se anota. Qué le habría costado a un lector: el CI dejó de distinguir regresión de señal durante toda la jornada del 17–18/ago, y en ese estado T02 cazó una colisión de nombre, T03 una cita a archivo inexistente y T15 un hueco de numeración — cualquiera de las tres pudo pasar inadvertida bajo un rojo permanente.
4 · COMMIT 4 · Las filas y el cierre
Tres filas nuevas en el tablero (§1, §2, §3 de arriba). Sí, añaden WARN de T22 — y después del COMMIT 1 ya no ponen roja la línea base, que es justamente la prueba de que el arreglo funcionó. Dilo así en la nota.
Enmienda fechada sobre el hallazgo de 9941adf: 7 recongelados en 10 h, no 6 en 14. Append, sin borrar.
Una línea en forense/hallazgos.md con el hallazgo de la columna encargo: 37 de 48 filas dicen SIN ENCARGO y al menos una es falsa (FP-01..FP-06, cuyo encargo existe en forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md); la columna nació el 18/ago y su cobertura retroactiva está sin llenar — A.8(3). Sin fila en el tablero, mismo criterio que usó el acto anterior.
ADR nuevo en gobernanza (el siguiente contiguo; hoy el máximo es 95, cero huecos — re-derívalo, no lo teclees: grep -oE "^\*\*ADR-[0-9]+" canon/gobernanza-v1_15.md).
Nota del acto en forense/notas/.
Marca este encargo CONSUMIDO con su PR.
5 · Módulo de auditoría — contesta solo lo aplicable
Este artefacto no afirma nada sobre México, así que el módulo de rigor extremo no aplica (v2.3, alcance). Contesta únicamente:
¿Cuántos contadores movió el trabajo que produjo este artefacto? La respuesta esperada es cero: 13 de 27, 0 de 15, 11 de 15 y 1 de 2 no se mueven aquí. Dilo en una línea al inicio, sin justificarlo. Este acto arregla el instrumento, no mide; su legitimidad es que desbloquea a los que sí miden.
6 · Lo que este acto NO hace
No cierra FP-47 ni FP-48. Su sustancia está intacta y sin decidir.
No congela más de una vez. Si terminas queriendo un segundo congelado, el arreglo del §1 falló: para y repórtalo.
No toca .barrido2/, data/raw, milpa/ ni tools/.
No abre las ocho etapas de FP-26. Ese disparador sigue gateado.
