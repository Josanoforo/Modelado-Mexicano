# ENCARGO · ACTO MAESTRA32-E12 · EXTRACTOR-FD (rama b de FP-175)

SHA de redacción: 19ace88 (main, merge PR #400 / ADR-228) · Redactado: 30/ago/2026, dirección maestra-32 · Instrucciones vigentes: v2.11 · Estado: LISTO PARA LANZAR — sin compuerta, sin ranuras. Es la entrada (2) de FP-179 ("rama (b) — dirección redacta al cierre de E3(a)"); E3(a) cerró (ADR-228).

ENTORNO ASIGNADO: UBUNTU (caja con corpus). NO se lanza en NUBE — abre payloads. Clon /home/pc0/Modelado-Mexicano, corpus en su data/raw (A.2 tercera parte PARO-relevante).

CARRILES EN PARALELO (declarado): carril CAJA = E12 (este); carril NUBE = E4 · RE-EMPAREJA. Compartidos: solo la cascada. Renumera quien fusiona segundo.

FIRMA DE MESA — verbatim de forense/firmas-pendientes.tsv, fila FP-175 (FIRMADA, ADR-222)

"FIRMO FP-175 (mesa, ranura M-EXTRACTOR, 30/ago/2026): letra "a y b" — se autorizan las dos ramas de extractor, razón de mesa verbatim: "Si no acabamos algo lo olvidamos." Secuencia operativa fijada por dirección: (a) primero, (b) después." La rama (a) corrió (ADR-228, 123/133). Este acto es la rama (b): fichas descriptivas / diccionarios que no son .xlsx (PDF, .xls, .html, .zip con esos miembros).

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

A.2, tercera parte (PARO-relevante): ls data/raw/ 2>/dev/null | head -3 — debe listar payloads. En la caja: command grep siempre; negativos con conteo (A.13); TSV con cabecera #. T03: rutas completas entre backticks.

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (maestra-32, 30/ago/2026, contra 19ace88) ═══

1 · ESTRUCTURA. Familia de inventarios (indexada); data/inventario-fd-v1_1.tsv (17,094 filas, 29 instrumentos con FD .xlsx, esquema de 9 columnas) es la tabla hermana a extender; data/cobertura-composicion-v1_0.tsv da el perímetro.

2 · CONTENIDO. (i) Perímetro de la rama (b), derivado hoy: causa B con formato=.pdf = 32 payloads (muestra: FD_ENCUCI2020.pdf, fd_envipe2025.pdf, endireh2021/endireh2021_fd.pdf, enut2002_fd.pdf, eder2017/eder2017_fd.pdf); FP-173 registra además 46 payloads con patrón de nombre FD fuera de .xlsx: 34 pdf, 6 xls, 4 html, 2 zip — los conjuntos se solapan; el perímetro es su unión, deduplicada por payload_id, re-derivada al arrancar (pdf causa B ∪ nombres fd_*/*_fd en cualquier formato ≠ .xlsx). (ii) Despacho existente: tools/inventario_reactivos.py:50 manda .pdf/.html/.xls a FORMATOS_SIN_CAMPOS — 0 filas por diseño (A.5: hecho sobre el despacho, no sobre el dato); tools/inventario_fd*.py/E6 solo leyeron .xlsx (ID_LABELS). (iii) Tabla destino data/inventario-fd-ext-v1_0.tsv y herramienta tools/inventario_fd_ext.py: NO-ENCONTRADO (ls data, ls tools, 0 coincidencias). (iv) Control positivo disponible, verificado: envipe2025 tiene 1,770 filas de microdato en data/inventario-reactivos-ext-v1_0.tsv y encuci2020 458 en el inventario general — los variable_id que el parser saque de fd_envipe2025.pdf / FD_ENCUCI2020.pdf se pueden contrastar contra esos conjuntos.

3 · COBERTURA RETROACTIVA. La convención INEGI del bloque de título ("Nombre \n (mnemónico)") es del contenido, no del formato — FP-173 lo dejó escrito. Ningún acto ha intentado parsear un FD en PDF; los 0 de estos payloads son del despacho.

═══════════════════════════════════════════════════════════════════

0-bis · A.3

Primer commit: este encargo verbatim en forense/encargos/2026-08-30-MAESTRA32-E12-EXTRACTOR-FD.md. Al cerrar, ## CONSUMIDO con el PR.

Paso previo · herramientas (opcionales e independientes, A.5 si pypi no responde)

pdfplumber (tablas + texto por página) para PDF; xlrd para .xls; lxml o beautifulsoup4 para .html; zipfile (stdlib) para miembros. python3 -c "import X; print(X.__version__)"; si falta, pip install X --break-system-packages; si la caja no alcanza pypi: "NO OBTENIDO POR ESTE AGENTE EN N INTENTOS" + receta manual, PARO solo para ese formato.

COMMIT-1 — congela ANTES de abrir un solo payload

forense/notas/2026-08-30-fd-ext-spec.md: (a) perímetro re-derivado, por formato, con la lista de ids; (b) regla de extracción, cerrada: en PDF, primero tablas (pdfplumber.extract_tables) buscando columnas cuyo encabezado contenga "nemónico/mnemónico/nombre/variable" y "descripción/pregunta/etiqueta"; si no hay tablas, texto por línea con un regex de mnemónico declarado aquí (mayúsculas/dígitos/guion bajo, 2-20 chars, p.ej. ^[A-Z][A-Z0-9_]{1,19}$) y la línea siguiente/adyacente como texto_reactivo; .xls vía xlrd con la misma búsqueda de encabezados que E6 usó para .xlsx (ID_LABELS, cita archivo:línea); .html tablas <table>; zip → miembros por las mismas reglas; (c) columnas y metodo = INSPECT_PDF_FD | INSPECT_XLS_FD | INSPECT_HTML_FD; instrumento por la regla vigente (tools/etiqueta_v1_2.py, funciones aplica_v1_1/aplica_v1_2), resto (sin-instrumento-derivable); payload_id, sha256_12 con las funciones de tools/inventario_reactivos.py; (d) control positivo, pre-registrado: para fd_envipe2025.pdf y FD_ENCUCI2020.pdf, el conjunto de variable_id extraído debe solapar ≥ 60% con los variable_id del mismo instrumento en el inventario de microdato; si un control cae por debajo, el parser se reporta como NO VALIDADO para ese formato y sus filas entran marcadas validacion=NO; no se ajusta el regex tras ver el resultado; (e) falsador: cobertura < 50% del perímetro (payloads con ≥1 fila) ⇒ se abandona la vía, no se itera; (f) B-bis: dos coberturas (payloads con ≥1 fila; filas con texto), por formato; alta = la capa de texto crece para RE-EMPAREJA; baja = hallazgo de heterogeneidad de las fichas, con la lista. Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

COMMIT-2 — corrida única

tools/inventario_fd_ext.py (nuevo; importa, no edita) → data/inventario-fd-ext-v1_0.tsv (cabecera comentada + las 9 columnas exactas de inventario-fd-v1_1). Cobertura por comando; fallos por payload con error crudo, no parchados; control positivo con sus dos porcentajes. Intocables con git diff --stat vacío: los tres inventarios de reactivos, inventario-fd-v1_0/v1_1, cobertura-composicion, tools/inventario_reactivos.py, tools/inventario_reactivos_ext.py, tools/etiqueta_v1_2.py. Cierre anti-PR#77: nada en tmp, nada nuevo en data/raw local sin declarar. FP-179: entrada (2) → EJECUTADA por este acto.

PERÍMETRO Y CONCURRENCIA

Archivos: forense/encargos/2026-08-30-MAESTRA32-E12-EXTRACTOR-FD.md · tools/inventario_fd_ext.py (nuevo) · data/inventario-fd-ext-v1_0.tsv (nuevo) · forense/notas/2026-08-30-fd-ext-spec.md · forense/notas/2026-08-30-fd-ext-cierre.md · data/INFRAESTRUCTURA-v1_0.md (solo la tabla nueva en la entrada de inventarios) · forense/firmas-pendientes.tsv (FP-179(2); fila nueva de recibo) · cascada. No toca milpa/**, ningún inventario existente, nada de E4. Concurrencia: E4 en nube en paralelo. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

FP pre-asignadas

FP-189–FP-190 (máximo hoy FP-186; E4 tiene 187-188; re-deriva; siguiente libre si están tomadas, declarado).

ADR y cascada

Candidato re-derivado (deriva, no heredes; renumera quien fusiona segundo). El ADR trae la firma de FP-175 verbatim, el perímetro por formato, las dos coberturas, el control positivo y los formatos NO OBTENIDOS si los hubo. registro-rotulos: MAESTRA32-E12 (token pelado E12 — censar, no reclamar). T25.

CONTADOR

Payloads con ≥1 fila: 439 → 439+N de 720 (las dos cifras juntas) · filas FD nuevas · filas con texto · control positivo: % de solape en los dos controles.

Lo que este acto NO hace

No lee microdato (solo lo consulta en el inventario para el control positivo). No empareja (E4 y su siguiente re-corrida). No re-etiqueta tablas existentes. No parchea el parser tras ver el control.

Sucesores declarados, no lanzados

Segunda re-corrida de la spec de E2 con la capa FD ampliada (nube) · ETIQUETA-ext para las filas sin instrumento de las tablas ext.

## CONSUMIDO

PR #401. Cobertura 40/46 payloads (87,0%), 10635 filas nuevas, 100% con texto. Control positivo: `fd_envipe2025.pdf` 75,0% (validado) / `FD_ENCUCI2020.pdf` 0,0% (no validado) → parser `.pdf` declarado NO VALIDADO en general. `ADR-229`. `FP-179` entrada (2) → EJECUTADA; `FP-189` nueva. Detalle: `forense/notas/2026-08-30-fd-ext-cierre.md`.
