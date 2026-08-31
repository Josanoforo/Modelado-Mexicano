# ENCARGO · ACTO MAESTRA32-E3 · EXTRACTOR-DTA — v2 (sustituye al texto del 28/ago)

SHA de redacción: 2799132 (main, merge PR #397 / ADR-225) · Redactado: 30/ago/2026 (v2), dirección maestra-32 · Instrucciones vigentes: v2.11 · Estado: LISTO PARA LANZAR cuando la sesión de MAESTRA32-E8 en la caja haya cerrado (con su PR abierto o fusionado — no hace falta esperar el merge: E3 no toca milpa/; si E8 fusiona después, renumera quien fusiona segundo). Sin ranuras. La firma de mesa viene abajo, verbatim del tablero.

Qué cambia respecto al texto archivado el 28/ago (forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md, no consumido, no ejecutado): (1) el perímetro se re-derivó hoy de data/cobertura-composicion-v1_0.tsv: 133 payloads = 125 .zip + 8 .dta sueltos (no "125 miembros"); (2) pyreadstat no lee .dbf ni .rdata — el texto viejo lo suponía; v2 despacha por formato con tres bibliotecas; (3) los intocables incluyen las tablas nuevas de E6 (inventario-reactivos-v1_2.tsv, inventario-fd-v1_1.tsv); (4) la ruta del corpus se cita de las notas del repo, no de memoria; (5) el resolutor de payloads se importa de tools/inventario_reactivos.py, no se reescribe; (6) carril CAJA reordenado E8 → E3; (7) rangos FP/ADR re-derivados. El cuerpo v1 queda como historia: en el paso 0-bis se le añade UNA línea de cabecera ("SUSTITUIDO por v2, dirección 30/ago/2026 — no ejecutado") y no se toca nada más.

ENTORNO ASIGNADO: UBUNTU (caja con corpus). NO se lanza en NUBE — abre payloads; la nube no tiene los bytes (A.2, muertes de E-ENCIG y S-IDG3). Clon de la caja: /home/pc0/Modelado-Mexicano (reportado por el ejecutor de E8 el 30/ago); corpus = data/raw de ese clon (/home/pc0/Modelado-Mexicano/data/raw, ruta citada en forense/notas/). La tercera parte de la firma de entorno es PARO-relevante: si ls data/raw/ no muestra payloads, la asignación está mal — PARA.

CARRILES EN PARALELO (declarado): carril CAJA = E8 → E3 (este); carril NUBE = E11 · COBERTURA-15. Compartidos: solo la cascada (gobernanza, estado-programa, registro-rotulos, firmas-pendientes, tests/check.py T25). Renumera quien fusiona segundo. Un acto no se lanza hasta que su condición esté visible en main o en la caja (lección de ADR-224).

FIRMA DE MESA — verbatim de forense/firmas-pendientes.tsv, fila FP-175 (FIRMADA, propagada por ADR-222)

"FIRMO FP-175 (mesa, ranura M-EXTRACTOR, 30/ago/2026): letra "a y b" — se autorizan las dos ramas de extractor, razón de mesa verbatim: "Si no acabamos algo lo olvidamos." Secuencia operativa fijada por dirección: (a) primero, (b) después." Este acto es la rama (a): formatos estadísticos .dta/.sav/.por/.sas7bdat/.xpt (Stata/SPSS/SAS), .dbf (dBase) y .rdata/.rds (R), sueltos o como miembros de zip. La rama (b) (PDF ficha-descriptiva + 46 FD no-xlsx de FP-173) es la entrada (2) de FP-179: dirección la redacta al cierre de este acto.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

A.2, tercera parte (PARO-relevante): ls data/raw/ 2>/dev/null | head -3 — debe listar payloads. En la caja: command grep siempre (el grep de la caja envuelve ugrep -I y tira no-UTF8 en silencio); todo negativo con su conteo de archivos (A.13); los TSV de data/ llevan cabecera # — sáltala antes de csv.DictReader. T03: cita archivos con ruta completa entre backticks.

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (maestra-32, 30/ago/2026, contra 2799132) ═══

1 · ESTRUCTURA. Tablas gobernantes: data/cobertura-composicion-v1_0.tsv (404 filas: causa A 204 · B 178 · C 22; columnas payload_id, formato, bucket, causa, causa_detalle, …), data/manifiesto.yaml, la familia de inventarios (inventario-reactivos-v1_0/v1_1/v1_2, inventario-fd-v1_0/v1_1), tools/inventario_reactivos.py (se importa, no se edita). La familia de inventarios está en data/INFRAESTRUCTURA-v1_0.md desde ADR-221: verifica con command grep -c "inventario" data/INFRAESTRUCTURA-v1_0.md ≥ 1 (reporta el conteo) y añade la tabla nueva a esa entrada si la entrada lista tablas.

2 · CONTENIDO.

Perímetro de la rama (a), derivado hoy (csv.DictReader sobre las 404 filas): causa B por formato = .zip 125 · .pdf 32 · .xls 7 · .dta 8 · .json 4 · .tab 1 · .gz 1; bucket SIN_CAMPOS 168 · NO_EXTRAIDO 10. Los 125 .zip llevan en causa_detalle la frase genérica "miembros .dta/.sav/.rdata/.dbf" — la extensión real de cada miembro no está en la tabla: se deriva en la caja con zipfile.namelist(). Rama (a) = 125 zips + 8 .dta sueltos = 133 payloads; muestra de ids: enaproce2015/ejem_base_micro_ciega_dta.zip, engasto2012/gasto_sav.zip, ennvih/ehh05dta_all.zip. Re-deriva al arrancar; no heredes 133.
Despacho existente: tools/inventario_reactivos.py:48-50: FORMATOS_CON_CAMPOS = {.zip,.xlsx,.csv,.tsv,.txt}, FORMATOS_SIN_CAMPOS = {.xls,.html,.json,.pdf,.xml}; la rama zip solo abre miembros de esos formatos; lo demás cae a NO_EXTRAIDO. NO-ENCONTRADO despacho para .dta/.sav/.dbf/.rdata: 0 hits de pyreadstat en tools/ + milpa/ (95 archivos .py, contados hoy). Funciones reutilizables verificadas: enumerar_universo() (L64, recorre data/raw excluyendo el bucle data/raw/raw), sha256_file_12() (L56), filas_desde_objetos() (L85), sanitiza_celda() (L39).
Tabla destino data/inventario-reactivos-ext-v1_0.tsv y herramienta tools/inventario_reactivos_ext.py: NO-ENCONTRADO (ls data, ls tools, 0 coincidencias con reactivos-ext).
Esquema a replicar (cabecera real de data/inventario-reactivos-v1_2.tsv): payload_id · sha256_12 · instrumento · ola · archivo_miembro · variable_id · texto_reactivo · metodo · universo_declarado. ola es constante NO_DETERMINADO (inventario_reactivos.py:110).
FP-175 FIRMADA "a y b" (ADR-222); FP-179 entrada (1) = este acto, ABIERTA.

3 · COBERTURA RETROACTIVA. cobertura-composicion nació el 27/ago, posterior a casi todo el corpus: por eso su partición se re-deriva al arrancar. Las etiquetas de instrumento (v1_1 28/ago, v1_2 30/ago) nacieron después de la partición: la tabla nueva aplica la regla de etiqueta vigente, no la de v1_0. El extractor general nunca vio estos 133 payloads con campos: el "0 filas" de esos payloads es un hecho sobre el despacho, no sobre el dato (A.5).

═══════════════════════════════════════════════════════════════════

0-bis · A.3

Primer commit: este encargo verbatim en forense/encargos/2026-08-30-MAESTRA32-E3-EXTRACTOR-DTA-v2.md, y UNA línea en la cabecera del archivo v1 (forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md): "SUSTITUIDO por v2 (dirección, 30/ago/2026): no ejecutado, no consumido; queda como historia." Al cerrar, ## CONSUMIDO con el PR en v2.

Premisas, con procedencia
Cobertura real del corpus: 316/720 (43.9%), las dos cifras juntas desde ADR-217; de los 404 sin filas, 178 son causa B. Re-deriva ambos números.
Metadato puro: nombres (y etiquetas donde el formato las tenga) de variable; no se abre ningún valor.
Herramienta hermana, no cirugía: patrón de MAESTRA31-E6 (tabla hermana, mismo esquema, intocables con git diff --stat vacío).
Fallos por payload se documentan, no se parchan (precedente mociba2020, E6).

Verifica estas premisas antes de ejecutar (v2.1). Si alguna no se sostiene, PARA y repórtalo.

Paso previo · herramientas, por formato (una biblioteca por familia; cada una es opcional e independiente)
.dta/.sav/.por/.sas7bdat/.xpt → pyreadstat, metadataonly=True (nombres + etiquetas de variable, sin cargar datos).
.dbf → dbfread (DBF(path, load=False).field_names: solo cabecera; sin etiquetas — texto_reactivo queda vacío y se declara).
.rdata/.rds → pyreadr (pyreadr.list_objects(path): nombres de objeto y columnas, sin cargar; sin etiquetas — igual que .dbf).

Para cada una: python3 -c "import X; print(X.__version__)"; si falta, pip install X --break-system-packages, registra versión. Si la caja no alcanza pypi para alguna: "NO OBTENIDO POR ESTE AGENTE EN N INTENTOS" (A.5) con salida cruda + receta manual de un minuto (wheel descargado en otra máquina, copiado al clon), PARO solo para esa familia de formatos — el acto continúa con las que sí tenga y lo declara en el B-bis. Prohibido derivar conclusiones sobre pypi del conocimiento previo del modelo.

COMMIT-1 — especificación congelada ANTES de abrir un solo payload

forense/notas/2026-08-30-extractor-ext-spec.md: (a) perímetro re-derivado por comando, con conteos por formato y la lista de payload_id; (b) regla de extracción por familia (arriba) y regla de despacho: para cada payload de la rama, si es zip → zipfile.namelist(), miembros de las tres familias se extraen a tmp, se inspeccionan, tmp se limpia; miembros de otros formatos se cuentan y se ignoran (ya los vio o los descartó el inventario general); (c) columnas: variable_id = nombre de columna/campo; texto_reactivo = etiqueta de variable si existe, si no vacío; metodo = INSPECT_STATA | INSPECT_SPSS | INSPECT_SAS | INSPECT_DBF | INSPECT_RDATA; instrumento por la misma regla de etiqueta vigente (tools/etiqueta_v1_2.py importado si expone función; si no, regla v1_1 + v1_2 copiadas con cita y declaradas) con (sin-instrumento-derivable) como resto, sin forzar; payload_id, sha256_12, archivo_miembro, universo_declarado con las funciones importadas de tools/inventario_reactivos.py; (d) codificaciones: la que la biblioteca detecte; fallo → fila de error, no parche; (e) falsador: cobertura < 50% del perímetro (payloads con ≥1 fila / 133 re-derivado) ⇒ se abandona la vía, no se itera la regla (precedente E4/E6); (f) B-bis, declarado antes de ver el dato: se reportan dos coberturas — payloads con ≥1 fila, y filas con texto_reactivo no vacío (las familias .dbf/.rdata solo dan nombres) — alta = el corpus se abre en N payloads para RE-EMPAREJA; baja = hallazgo de heterogeneidad de formato con la lista de qué falló; ambos informativos. Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

COMMIT-2 — corrida única

tools/inventario_reactivos_ext.py (nuevo; importa de tools/inventario_reactivos.py, no lo edita) → data/inventario-reactivos-ext-v1_0.tsv (cabecera comentada con regla y acto, luego las 9 columnas exactas). Cobertura verificada por comando (awk/Python: filas totales, filas con texto, payloads con ≥1 fila sobre el perímetro, por familia de formato). Fallos por payload con su error crudo. Intocables con git diff --stat vacío: tools/inventario_reactivos.py, tools/etiqueta_v1_2.py, data/inventario-reactivos-v1_0/v1_1/v1_2.tsv, data/inventario-fd-v1_0/v1_1.tsv, data/cobertura-composicion-v1_0.tsv. Si verificas integridad contra el manifiesto: tests/manifiesto.py --verifica, una invocación por --id (A.1), tres respuestas sin colapsar; formatos con token de sesión, doble hash (A.7).

Cierre — el defecto de PR #77

Antes de abrir el PR: tabla, herramienta y notas commiteadas (no solo en el worktree); ningún residuo en tmp ni archivo nuevo en data/raw local sin declarar. FP-179: entrada (1) → EJECUTADA por este acto, con PR; si E8, por la secuencia vieja, la marcó "lanzado", corrígelo con enmienda fechada.

PERÍMETRO Y CONCURRENCIA

Archivos: forense/encargos/2026-08-30-MAESTRA32-E3-EXTRACTOR-DTA-v2.md · forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md (solo la línea de cabecera) · tools/inventario_reactivos_ext.py (nuevo) · data/inventario-reactivos-ext-v1_0.tsv (nuevo, + .meta si el patrón de la casa lo pide) · forense/notas/2026-08-30-extractor-ext-spec.md · forense/notas/2026-08-30-extractor-ext-cierre.md · data/INFRAESTRUCTURA-v1_0.md (solo la tabla nueva en la entrada de inventarios) · forense/firmas-pendientes.tsv (FP-179(1); fila nueva de recibo) · cascada. No toca milpa/**, ningún inventario existente, hitoD-preregistro, nada de E8 ni de E11. Concurrencia: E11 en nube en paralelo; E8 en esta misma caja, ya cerrado. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

FP pre-asignadas

FP-187–FP-188 (máximo hoy FP-182; E11 tiene 183-184, E8 185-186; re-deriva y sigue al siguiente libre si están tomadas, declarado). Uso: "mesa recibe la cobertura ext: 316 → 316+N de 720, las dos cifras juntas".

ADR y cascada

Candidato re-derivado con el comando de la casa (deriva, no heredes; renumera quien fusiona segundo). El ADR trae la firma de FP-175 verbatim, el perímetro re-derivado, las dos coberturas del B-bis, los formatos NO OBTENIDOS si los hubo, y la sustitución v1→v2. registro-rotulos: MAESTRA32-E3 censado por primera vez (token pelado E3 colisiona con MAESTRA30-E3/MAESTRA31-E3 — se censa, no se reclama). T25.

CONTADOR

Payloads con ≥1 fila: 316 → 316+N sobre 720 (las dos cifras juntas, ADR-217) · filas de reactivo nuevas · filas con texto no vacío.

Lo que este acto NO hace

No re-corre el inventario general ni toca sus filas. No empareja contra el motor (E4 · RE-EMPAREJA, sucesor con la spec congelada de E2 sobre el universo ampliado). No adjudica rutas. No descarga nada. No abre valores de dato — solo metadatos. No ejecuta la rama (b).

Sucesores declarados, no lanzados

MAESTRA32-E4 · RE-EMPAREJA (misma spec de E2, universo ampliado; re-sella los veredictos de E2/E6, A.10 corolario 1) · rama (b) PDF-FD, encargo de dirección al cierre de este acto (FP-179(2)).
