ENCARGO E6 · DICCIONARIOS-FD — la capa de texto que falta, y es la única vía a 13 parámetros

Dirección (maestra-31), 27/ago/2026 · Redactado contra main = 07b1452 (clon propio, no espejo). No gated. Es el acto sucesor que ACTO MAESTRA31-E4 reveló y su propio encargo le prohibió hacer.

ENTORNO ASIGNADO: UBUNTU. NO lanzar en NUBE — ahí corre MAESTRA31-E5, y este acto necesita data/raw montada. Sin red, sin API (FP-165), sin descarga. Rótulo: ACTO MAESTRA31-E6 (D-6). Token pelado E6 colisiona; se censa, no se reclama.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Crea worktree propio sobre origin/main.

2 · SHA. Confirma contra qué base trabajas. Si main se movió: NO es PARO — refresca, re-deriva y reporta la diferencia antes de editar.

3 · data/raw. Para este acto sí es PARO: es su materia prima. Reporta: existe / la enlacé a <ruta> / la creé. Si no se puede montar, PARA — la asignación de entorno estaría mal y eso es de mesa. ⚠️ Este acto NO descarga.

4 · ENTORNO. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado sin_variable; curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/. Los dos valores crudos. NUNCA curl -I. A.2 tercera parte: ls data/raw/ 2>/dev/null | head -1. ⚠️ Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo declara cuántos archivos examinó. Usa command grep y decláralo.

5 · ESPEJO. Prohibido derivar cifras del espejo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — CONTESTADA por dirección (clon propio, 07b1452, 27/ago/2026) ═══

1 · ESTRUCTURA. Tabla gobernante: data/inventario-reactivos-v1_0.tsv (ADR-213). Este acto la extiende con una tabla hermana, no la edita. Extractor de referencia: tools/inventario_reactivos.py, producido por E4 — se lee, se entiende su regla de "primera fila de cada hoja", y no se modifica.

2 · CONTENIDO — el hueco está medido y revelado, por el propio E4. No es hipótesis de dirección; es la enmienda F1 de ADR-213, derivada con comando en la misma sesión que lo produjo:

awk -F'\t' 'NR>1 && length($7)>0' data/inventario-reactivos-v1_0.tsv | wc -l
  → 0    (texto_reactivo vacío en las 178,246 filas, cero excepciones)

payloads con variable_id > 60 chars vía INSPECT_XLSX
  → 30   (*_fd.xlsx, Diccionario_*, Glosario_*: ENASEM, ENDUTIH, MOCIBA,
          ENVIPE, ENIF, ENADID, CNBV — 352 filas, 0.2% del total)

Mecanismo, confirmado en 3 de los 30 abriendo el archivo (2 CNBV por contenido, ENASEM 2018 por estructura con openpyxl): las fichas descriptivas de INEGI abren cada hoja con un bloque de título de 5-6 filas (INEGI. Encuesta Nacional… / ESTRUCTURA DEL ARCHIVO / nombre / Tabla de datos: <hoja> / vacía) antes de la tabla real de variables. La regla de "primera fila de cada hoja" captura ese título como un variable_id falso de 100+ caracteres y nunca llega a las filas por variable. Los otros 27 comparten patrón de nombre y síntoma; no se abrieron uno por uno, y esa distinción se conserva (A.5).

Resultado A.4 sobre el entregable: NO-ENCONTRADO — ninguna tabla del repo tiene el texto por variable de las fichas descriptivas. Universo: árbol completo salvo .git y data/raw, 27/ago/2026.

3 · COBERTURA RETROACTIVA. El inventario nació el 26/ago y estos 30 payloads cuentan hoy como cubiertos en su cifra de 97.78%. Están cubiertos solo al nivel del bloque de título. La cifra no es falsa; es ambigua, y FP-171 ya la lleva con sus dos números.

Y por qué esto vale un acto, medido y no supuesto. forense/perimetro-alcanzable-v1_0.md (ADR-212) estableció 12 de 30 alcanzables, con 13 ASIGNADO_PROBABILIDAD de juicio puro sin ruta. Esos 13 no citan ninguna variable — por eso E5, que empareja por token exacto, no puede alcanzarlos ni con más corpus. El texto es la única vía posible hacia parámetros que no citan variables, y los 30 archivos de este acto son exactamente los que contienen ese texto. El extractor cegado a la semántica falló justo en los archivos cuya única función es semántica.

⚠️ Si al ejecutar encuentras que esto ya está hecho, PARA y repórtalo.

════════════════════════════════════════════════════════════════════

OBJETO

Recuperar la capa de texto de los archivos de ficha descriptiva y diccionario del corpus, en data/inventario-fd-v1_0.tsv: una fila por variable con texto_reactivo poblado. Tabla hermana del inventario, no sustituta.

Lo que este acto NO hace: no reescribe tools/inventario_reactivos.py · no re-corre el inventario general · no toca las 178,246 filas existentes · no empareja contra el motor (eso es E5) · no adquiere nada.

PASOS

0-bis · A.3. Commitea este encargo íntegro y verbatim en forense/encargos/2026-08-27-MAESTRA31-E6-DICCIONARIOS-FD.md antes de nada. ## CONSUMIDO al cerrar, con el número de PR.

1 · Deriva el perímetro real, no heredes el 30. La cifra de 30 es de E4 y viene de un síntoma (variable_id > 60 chars vía INSPECT_XLSX), no de un censo. Deriva el conjunto por comando, y reporta las tres cifras por separado, sin colapsarlas:

payloads que casan el patrón de nombre (*_fd.xlsx, Diccionario_*, Glosario_*, y las variantes que encuentres);
de ésos, cuántos presentan el síntoma y cuántos no — E4 no derivó el converso y sin él el perímetro está sesgado hacia arriba;
si hay fichas descriptivas o diccionarios en PDF, .txt o .doc dentro del corpus y cómo salieron en el inventario. Si el bloque de título es convención de INEGI y no del formato, el hueco no es solo de xlsx — y eso cambia el alcance de este acto, así que se mide antes de empezar.

2 · COMMIT-1 — congela la especificación ANTES de abrir un solo archivo.

Cómo se detecta el fin del bloque de título y el inicio de la tabla de variables. Dirección no prescribe la regla: obsérvala en al menos tres archivos de instituciones distintas antes de escribirla, y decláralo. Una regla derivada de un solo archivo es una regla de un solo archivo.
Qué se hace con los que no casan la regla: van a NO-EXTRAIDO con la razón, y esa lista es entregable.
El esquema, hermano del inventario: payload_id · sha256_12 · instrumento · ola · archivo_miembro · variable_id · texto_reactivo · metodo · universo_declarado. Misma forma, para que las dos tablas se puedan unir sin traducción.
El denominador de cobertura y qué cuenta como cubierto.
B-bis, antes de ver el dato: qué significa cubrir casi todos y qué significa cubrir pocos. Si la regla resulta uniforme entre instituciones, dilo ahora — sería un resultado más útil que el propio texto extraído, porque generaliza.
Frase de sello verbatim: «El primer resultado que produzca este procedimiento es el que se reporta.»

3 · COMMIT-2 — la tabla. Sin editar el primero. Universo declarado en la cabecera (A.10). Y una verificación que E4 aprendió a su costa: confirma por comando que texto_reactivo está efectivamente poblado (awk -F'\t' 'NR>1 && length($7)>0' | wc -l) y pega la salida. No lo afirmes en prosa sin el conteo.

4 · Cierre. Nota forense/notas/2026-08-27-diccionarios-fd-cierre.md con los conteos A.13 · FP-173 con la cobertura ante mesa · línea en forense/hallazgos.md · ADR (máximo re-derivado por conteo entero; candidatea máximo+1; renumera quien fusione segundo) · recifrado §L0 · rótulo en canon/registro-rotulos.tsv y tests/check.py si T25 lo exige · python3 tests/check.py --baseline VERDE (🚫 jamás --freeze) · PR.

REGLA DE TOPE

Este acto sí está autorizado a escribir código de extracción —es su objeto y por eso es acto propio y no un parche dentro de E4—, y por eso el tope importa más, no menos.

1 · Un extractor, para un patrón, sobre un conjunto acotado. El bloque de título de las fichas descriptivas. No es una mejora general de inspect_xlsx ni del inventario. Si te encuentras generalizando a formatos fuera del perímetro derivado en el paso 1, PARA.

2 · tools/inventario_reactivos.py no se toca, y tools/curador_registro/** tampoco. Se leen. El código nuevo vive en su propio archivo.

3 · El inventario general no se re-corre ni se edita. Las 178,246 filas quedan. La tabla nueva es hermana; la unión la hace quien consulte.

4 · Cero semántica automatizada. Se extrae el texto que el archivo declara. No se clasifica, no se normaliza a constructos, no se empareja contra el motor, no se llama a ningún modelo (FP-165).

5 · Una vuelta, con falsador declarado antes de correr. Si la cobertura queda por debajo de la mitad del perímetro derivado en el paso 1, se conserva lo producido, se anota en hallazgos.md y se abandona la vía: significa que las fichas descriptivas no tienen estructura común y el texto hay que sacarlo de otro lado. No se itera sobre la regla para subir el número.

PERÍMETRO Y CONCURRENCIA

Toca: forense/encargos/2026-08-27-MAESTRA31-E6-DICCIONARIOS-FD.md · data/inventario-fd-v1_0.tsv (nuevo) · el script nuevo de extracción, en archivo propio (tools/inventario_fd.py o equivalente) · forense/notas/2026-08-27-diccionarios-fd-cierre.md (nuevo) · forense/firmas-pendientes.tsv (solo FP-173) · forense/hallazgos.md · canon/gobernanza-v1_15.md · canon/estado-programa-v1_10.md · canon/registro-rotulos.tsv · tests/check.py (solo _T25_ARCHIVOS_CONOCIDOS).

NO toca: data/inventario-reactivos-v1_0.tsv ni su .meta · tools/inventario_reactivos.py · tools/curador_registro/** · milpa/** · data/manifiesto.yaml · data/curacion-universo/** · forense/prereg-duelo-v2/** · forense/perimetro-alcanzable-v1_0.md · R10.3.

Concurrencia: MAESTRA31-E5 · CRUCE-INVERSO corre en NUBE en paralelo. Colisión posible en gobernanza / estado / registro-rotulos / tests/check.py. Tablero separado: E5 FP-172, este acto FP-173. ADR: renumera quien fusiona segundo, con el máximo re-derivado contra el árbol ya fusionado.

"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

PROHIBIDO

Editar el inventario general, su .meta o su extractor · tocar tools/curador_registro/** o milpa/** · generalizar el extractor fuera del perímetro derivado · clasificar, normalizar o emparejar el texto extraído · llamar a cualquier modelo o red · descargar · afirmar que el texto quedó poblado sin el conteo al lado · iterar tras un resultado bajo · adjudicar casilla, letra o tier (D-i vigente) · derivar cifra del espejo.

CONTADOR

Variables con texto recuperado, sobre el perímetro derivado en el paso 1 — la primera capa semántica del corpus, y la única vía posible hacia los 13 parámetros que no citan ninguna variable.

Si el falsador se dispara y la vía se abandona, ese hallazgo es el contador y se dice con esa palabra: las fichas descriptivas del corpus no comparten estructura, y el texto de los diccionarios no es recuperable por regla.

## CONSUMIDO
Ejecutado por `ACTO MAESTRA31-E6 · DICCIONARIOS-FD`, 27/ago/2026. PR: https://github.com/Josanoforo/Modelado-Mexicano/pull/387
