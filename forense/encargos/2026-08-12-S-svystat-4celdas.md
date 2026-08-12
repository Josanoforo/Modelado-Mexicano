# ENCARGO · ACTO S · svystat: la variante de 4 celdas que el Commit 5 de E4c declaró y no implementó

- **SHA de redacción:** `3e071f0` (merge de #175)
- **Entorno asignado:** Cualquiera con el repo — no toca microdato ni red
- **Estado:** CONSUMIDO — PR de la rama `mesa/s-svystat-4celdas`, detalle en `forense/notas/2026-08-12-acto-s-svystat-4celdas.md`

---

12/ago/2026 · base declarada: origin/main = 3e071f0 (merge #175), 69 ADR, suite VERDE 22 FAIL · 101 WARN — los tres verificados por comando al escribir

POR QUÉ EXISTE ESTE ACTO. El Commit 5 de E4c (19c9b42, PR #176) retiró la construcción de varianza del DDD que el Commit 4 §3 había declarado, y declaró la correcta — sin implementarla, por perímetro. Esa implementación es ahora dependencia dura del Paso 3 de E4c (la corrida real): sin ella no hay forma de calcular el DDD con la varianza que el propio acto ya declaró como la válida.

PROCEDENCIA, verificada contra el repo al escribir este encargo — re-derívala en PASO 1:

19c9b42 no edita los commits 1, 3 ni 4: solo apendiza forense/hallazgos.md y una nota nueva. El sello de Bloque D aguanta.
ADR-68(a) no aplica. Su texto literal congela tools/curador_registro/; este acto toca tests/, que está fuera de ese alcance. ADR-62 es precedente directo y explícito, no analogía: modificó tests/svystat.py y añadió el carril de CI para tests/test_svystat.py, como mantenimiento de aparato.
grep -i "triple\|ddd\|55-64\|banda" tests/test_svystat.py → vacío. No hay caso conocido para triple diferencia.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

ENTORNO ASIGNADO — y el que NO. Cualquiera con el repo. No toca microdato ni red → dilo y salta el punto 4 del ARRANQUE. NO se lanza en dos entornos a la vez.

PERÍMETRO. SOLO: tests/svystat.py (una función nueva; las existentes no se modifican) · tests/test_svystat.py (casos nuevos) · forense/notas/ (1 nota) · forense/hallazgos.md (1 entrada) · forense/encargos/2026-08-12-S-svystat-4celdas.md. NO toca tools/, canon/, data/, milpa/, ni ninguna nota de E4c. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

CONCURRENCIA. e4c/r5-1-d2 (#176) y remediacion/brecha-documental vivas; ninguna toca tests/svystat.py — verifícalo antes de escribir. Único solapamiento: forense/hallazgos.md, que resuelve merge=union. El merge va local (git merge con .gitattributes en el árbol), nunca por el botón de GitHub ni por su editor web de conflictos — verificado el 12/ago en #175: GitHub no honra el driver del lado servidor.

PASO 1 · Premisas — corre y pega crudo
```bash
git log -1 --format="%h %s"                                          # 3e071f0 o posterior
git log --oneline origin/main..origin/e4c/r5-1-d2 | head -1          # 19c9b42 o posterior
grep -c "def diff_ultimate_cluster\|def did_ultimate_cluster" tests/svystat.py   # esperado: 2
grep -i "triple\|ddd\|55-64\|banda" tests/test_svystat.py            # esperado: vacío
git diff --stat origin/main...origin/e4c/r5-1-d2 -- tests/           # esperado: vacío — e4c no toca tests/
git diff --stat origin/main...origin/remediacion/brecha-documental -- tests/svystat.py  # esperado: vacío
python3 tests/check.py --baseline                                     # esperado: VERDE 22 FAIL · 101 WARN
python3 tests/test_svystat.py                                         # esperado: pasa (carril de CI de ADR-62(b))
```

PARO si: alguna rama viva ya toca tests/svystat.py · o --baseline arranca en ROJO · o test_svystat.py arranca fallando.

PASO 2 · La función — extensión de diff_ultimate_cluster, no familia nueva

Implementa una función nueva (nombre sugerido diff4_ultimate_cluster; el ejecutor puede proponer otro y justificarlo). Ninguna función existente se modifica — prop_, diff_ y did_ultimate_cluster quedan byte a byte como están, y sus llamadores actuales no se tocan.

Contrato, tomado verbatim del Commit 5 §2 de E4c — no lo reinterpretes:

Dentro de una ola, un solo residual linealizado de 4 términos, agregado por UPM con la misma fórmula de conglomerado último que ya usa diff_ultimate_cluster:

z_i = [1{i∈T,65+}·w_i(y_i−p_T)/N̂_T − 1{i∈C,65+}·w_i(y_i−p_C)/N̂_C] − [1{i∈T',55-64}·w_i(y_i−p_T')/N̂_T' − 1{i∈C',55-64}·w_i(y_i−p_C')/N̂_C']

con p_T, p_C, p_T', p_C' las cuatro proporciones ponderadas, y var = sum_h [(m_h/(m_h−1)) · sum_i (z_hi − mean_i(z_hi))²].

Entre olas no se implementa nada nuevo: DDD = d_post − d_pre con Var = Var(d_post) + Var(d_pre) es la resta que el llamador hace con dos salidas de esta función, y ahí el argumento de independencia entre-olas sí es el válido — sin cambio respecto a did_ultimate_cluster.

Cinco decisiones que heredas de diff_ultimate_cluster y que se declaran explícitamente en el docstring, sin inventar política nueva:

Unidades fuera de grupo (grupo=None) permanecen y aportan residual cero. No se filtran: cambiar la estructura de estratos/UPM alteraría los grados de libertad. Es estimación de dominio, no submuestreo.
Singleton: un estrato de una sola UPM salta y se cuenta. El docstring repite la advertencia existente, palabra por palabra en espíritu: el llamador DEBE leer ese contador; un singleton no detectado baja el SE en silencio. La política contraria de produce.py::taylor_distribution (aborta con ESTRATOS_UNA_UPM) sigue anotada y no se unifica en este acto.
Cuantil 1.959963985, igual que las funciones hermanas, no 1.96.
rows = list(rows) — se recorre más de una vez; un generador se agotaría y fallaría en silencio.
Grupo vacío → None, extensión de la misma regla: no se construye un contraste de 4 celdas al que le falte una pata. Declara en el docstring qué pasa con cada una de las cuatro por separado, sin colapsarlas en un solo None sin diagnóstico.

El docstring cita, con número de línea, el Commit 5 de E4c como origen del contrato y dice por qué el argumento de independencia entre-olas no aplica dentro de una ola — para que nadie vuelva a hacer la resta ingenua.

PASO 3 · Los casos conocidos — la parte que decide si esto sirve

tests/test_svystat.py gana casos nuevos. Mínimo tres, y el segundo es el que importa:

Degenerado a lo ya probado. Si T' y C' están vacíos, la salida debe coincidir exactamente con diff_ultimate_cluster sobre las mismas filas. Prueba de que la extensión no rompió el caso de 2 celdas.
El caso que demuestra el defecto que este acto corrige. Construye un dato sintético con covarianza positiva conocida entre bandas dentro de UPM y verifica que el SE de 4 celdas es estrictamente menor que la suma ingenua √(Var(θ̂₆₅₊) + Var(θ̂₅₅₋₆₄)). Sin este caso, nada en la suite distingue la implementación correcta de la que se acaba de retirar — y el defecto puede volver sin que ningún test se ponga rojo.
Singleton. Un estrato de una sola UPM: la función salta, cuenta, y el contador sale en la salida.

Y el chequeo que hace verificable la fórmula, no solo el código: si es factible, un caso SRS donde el valor esperado se pueda derivar a mano —mismo criterio que _caso_conocido() ya usa— y se compare contra él. Si no es factible, dilo y explica por qué; no lo sustituyas por un test de regresión contra tu propia salida, que solo prueba que el código no cambió, no que está bien.

PASO 4 · Cierre

Siete líneas. --baseline cruda en el cuerpo del PR, más python3 tests/test_svystat.py crudo (el carril de CI de ADR-62(b) es independiente de check.py). Jamás silencies: si --baseline gana entradas, repórtalas con las entradas a la vista.

Lo que este acto habilita, declarado: el Paso 3 de E4c (la corrida real de R5.1-D2) deja de estar bloqueado por la varianza del DDD. Lo que NO hace: no corre nada de R5.1-D2, no toca sus notas, no adjudica ninguna fila del §6.

Contadores de medición movidos: 0. Este acto es aparato. El que mide es el Paso 3 de E4c, después.

PR mesa/s-svystat-4celdas, NO FUSIONAR sin mesa.

Nota de dependencias — cómo queda el tablero con este acto dentro
acto · estado · bloquea
M-6 · sello y escala · listo para lanzar · Paso 3 de E4c (la fila E del §6)
S · svystat 4 celdas · este encargo, listo para lanzar · Paso 3 de E4c (la varianza del DDD)
V · vocabulario celda-D · tras el merge de M-6 · E0 del piloto
Paso 3 de E4c · bloqueado por M-6 y S, los dos · —
J · folioviv · no corre por ahora — la maestra de Fable estructura remediación y dependencias, con más contexto · —

M-6 y S son independientes entre sí (perímetros disjuntos: canon/+ficha vs tests/) y pueden correr en paralelo. El Paso 3 de E4c necesita los dos fusionados.
