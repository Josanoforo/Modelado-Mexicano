# Encargo — `ENCARGO E4 · DISEÑO-ENSAFI`, 26/ago/2026

**Estado: EN CURSO.** (Se marca `## CONSUMIDO` con el PR al cerrar, A.3.)

Transcripción íntegra del encargo tal como lo emitió la dirección (maestra-30), antes de ejecutar.

---

ENCARGO E4 · DISEÑO-ENSAFI — abre el FD ya descargado y cierra la fila ENSAFI de data/diseno-muestral.yaml a MAPEADO

Dirección (maestra-30), 26/ago/2026 · SHA de redacción 186f090 (verificado vivo; clon propio, git status limpio) · Cifras: clase (1), derivadas en esta sesión.

ENTORNO ASIGNADO: UBUNTU (el FD vive en el corpus). NO lanzar en NUBE ni en Codex. En la caja UBUNTU corre PRIMERO (acto corto, un PR); E3 corre después. Sin ranuras de mesa: cero firmas nuevas. No estima nada.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo. A.2, tercera parte: ls data/raw/ 2>/dev/null | head -1 — el corpus DEBE estar montado (precedente: raíz compartida ln -s /home/pc0/mm-corpus/raw, nota ENSAFI-DESCRIPTOR §0); en UBUNTU grep envuelve ugrep -I: usa command grep y decláralo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — la contesta quien ESCRIBE el encargo [NUEVO v2.8] ═══ CONTESTADA por dirección, 26/ago/2026, clon en 186f090:

1 · ESTRUCTURA. Dominio: censo de diseño muestral. Gobernante, derivada de data/INFRAESTRUCTURA-v1_0.md (no de memoria): data/diseno-muestral.yaml; el inventario de payloads lo gobierna data/manifiesto.yaml. Ninguna otra tabla del índice escribe este dominio — omisión declarada.

2 · CONTENIDO.

La fila objetivo EXISTE-NO-SATISFACE (existe, le falta el cierre): sed -n '977,997p' data/diseno-muestral.yaml → fuente: ENSAFI …, estado: PENDIENTE, con la reserva escrita: «SIGUE PENDIENTE tras ACTO RECENSO-DISENO-14 (…) por falta de DESCRIPTOR, no por falta de payload. Verificación cruda (2000 filas por tabla): FAC_VIV/FAC_HOG/FAC_ELE, EST_DIS y UPM_DIS no vacíos en el 100% de las cuatro tablas. (…) Con el FD en mano esta fila debería cerrar a MAPEADO en minutos. Ver FP-115.»
El FD YA EXISTE en el corpus — la receta A.5 de esa fila caducó (v2.2): grep -n "ensafi2023_fd" data/manifiesto.yaml → id ensafi2023_fd_xlsx_zip (:15428), url_origen …/ensafi_2023_fd_xlsx.zip, fecha_descarga: 2026-08-25, COINCIDE (ACTO ENSAFI-DESCRIPTOR, ADR-198, #370 — la API declaraba formato _xlsx.zip, no .xlsx; la extensión era el obstáculo).
Lectura previa del FD, ya en el árbol y citable: forense/ficha-r34-condBC-v1_0.md Anexo 2 (:288 en adelante; :377: «el FD trae FAC_ELE, UPM_DIS y EST_DIS»).
El cierre que este encargo manda NO existe aún: la fila sigue PENDIENTE (comando de arriba) — no hay trabajo duplicado.

3 · COBERTURA RETROACTIVA. La fila nació antes del FD: su estado PENDIENTE y su receta A.5 son de cuando el FD se creía no publicado (FP-95/ADR-135(f), FP-115); el FD llegó el 25/ago (ADR-198). La ausencia de MAPEADO no prueba nada — es exactamente la brecha que este acto cierra. Declarado con las dos fechas.

════════════════════════════════════════════════════════════════════

OBJETO

Abrir el FD desde el corpus, verificar byte a byte (A.6: encontrado-por-lectura-previa no es verificado por este acto) que define los tres ponderadores, EST_DIS y UPM_DIS como variables de diseño, y cerrar la fila a MAPEADO. Un PR, sin estimación.

PASOS

0-bis · A.3: commitea este encargo íntegro en forense/encargos/2026-08-26-E4-DISENO-ENSAFI.md; al cerrar, ## CONSUMIDO con el PR. 1 · Compuerta cero: pega sed -n '977,997p' data/diseno-muestral.yaml (debe seguir PENDIENTE; si ya dice MAPEADO, PARA y repórtalo — el trabajo estaba hecho) y verifica el hash del payload ensafi2023_fd_xlsx_zip contra el manifiesto, una invocación (A.1). 2 · Abre el FD (resuelve la ruta física vía manifiesto + data/raices.local.yaml; unzip -l primero): localiza en el descriptor la definición de FAC_VIV, FAC_HOG, FAC_ELE (universo de cada uno: vivienda / hogar / persona elegible — cita hoja y celda/fila del FD, no lo infieras), EST_DIS (estrato de diseño) y UPM_DIS (UPM de diseño). Si el FD no define alguno como variable de diseño, eso es el hallazgo: la fila NO pasa a MAPEADO — pasa a lo que el FD sostenga, con la cita. 3 · Cierra la fila: estado: MAPEADO (o el que (2) sostenga); campos ponderador/estrato/upm reescritos citando el FD (ensafi2023_fd_xlsx_zip, hoja:celda); en notas, añade párrafo fechado 26/ago/2026 — sin borrar el texto viejo — con: estampa A.10 (universo = este FD + la verificación cruda 2000 filas/tabla ya citada en la fila + Anexo 2 de ficha-r34-condBC), la deuda A.5 caducada por ADR-198, y FP-115 citada sin tocarla (esa fila cubre tres fuentes; aquí se resuelve solo la parte ENSAFI — el tablero no se edita en este acto). 4 · Nota forense/notas/2026-08-26-diseno-ensafi-cierre.md (A.13 en todo negativo; comandos crudos) · ADR (máximo re-derivado; renumera al fusionar — E1/E2/E3 también emiten) + recifrado estado §L0 · tests/check.py --baseline verde · PR.

PERÍMETRO Y CONCURRENCIA

Toca SOLO: data/diseno-muestral.yaml (una fila) · forense/notas/2026-08-26-diseno-ensafi-cierre.md (nueva) · forense/encargos/…E4….md (A.3) · canon/gobernanza-v1_15.md · canon/estado-programa-v1_10.md. Concurrentes: E3 (misma caja, después; registro-llaves/milpa) · E1/E2 (NUBE) — colisión esperada solo en gobernanza/estado por recifrado ADR: renumera quien fusiona segundo. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

PROHIBIDO

Descargar (el FD ya está; hash discordante = PARO, no re-descarga) · estimar o abrir valores del microdato de datos (ensafi_2023_bd_csv.zip no se abre aquí) · tocar otras filas del YAML o el tablero · inferir universos de ponderador desde otras encuestas de INEGI.

CONTADOR

Cero directo, declarado — habilita la varianza de diseño de ENSAFI para todo acto futuro que la mida (incluidas reaperturas de R3.4 sembradas en la ficha).
