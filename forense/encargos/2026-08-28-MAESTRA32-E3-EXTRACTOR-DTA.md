> **SUSTITUIDO por v2 (dirección, 30/ago/2026): no ejecutado, no consumido; queda como historia.**

> **RANURA M-EXTRACTOR: FIRMADA "a y b" (mesa, 30/ago/2026) — secuencia a→b; estado: EN-COLA-UBUNTU · GATED-ENTORNO (requiere corpus montado, A.2 tercera parte).** Cabecera añadida por `ACTO MAESTRA32-E5 · PROPAGA-FIRMAS-Y-COLA` al archivar este encargo (repara la grieta `A.3`: el texto vivía solo en la conversación de lanzamiento). El cuerpo de abajo es el encargo de dirección **verbatim, sin editar** — su propia "RANURA DE FIRMA DE MESA" (línea 11-17 del original, "[FIRMA M — VACÍA]") queda tal como se escribió; la resolución de esa ranura (letra "a y b", secuencia a→b, razón de mesa "Si no acabamos algo lo olvidamos.") vive en `FP-175` y en `forense/encargos/2026-08-30-MAESTRA32-E5-PROPAGA-FIRMAS-Y-COLA.md`, no aquí. Este acto no lanza la rama (a) ni la (b) — las deja `EN-COLA-UBUNTU`, gateadas a que la caja tenga el corpus montado (`A.2` tercera parte); es una de las 5 entradas de la fila-grito `FP-179`.

---

# ENCARGO · ACTO MAESTRA32-E3 · EXTRACTOR-DTA

**SHA de redacción:** `2953716` (main, merge PR #391, 27/ago/2026 21:51) · **Redactado:** 28/ago/2026, dirección maestra-32 · **Instrucciones vigentes:** v2.11 · **Estado:** NO LANZADO — **GATED doble:** (i) `MAESTRA32-E2` fusionado; (ii) RANURA M-EXTRACTOR con letra. Ranura VACÍA = PARO inmediato, cero ediciones.

**ENTORNO ASIGNADO: UBUNTU.** **NO se lanza en NUBE** — este acto abre payloads y la nube no tiene los bytes: es exactamente el par de muertes de `A.2` (E-ENCIG y S-IDG3, 5/ago, `cloud_default` correcto y cero corpus montado). La tercera parte de la firma de entorno es PARO-relevante aquí: si `ls data/raw/` no muestra el corpus enlazado, la asignación estaba mal — PARA y repórtalo, no lo resuelvas descargando.

**Serie MAESTRA32, posición 3 de 3.** Nada corre en paralelo.

---

## RANURA DE FIRMA DE MESA — se llena ANTES de lanzar

**RANURA M-EXTRACTOR — [FIRMA M — VACÍA].** Resuelve `FP-175` ("una decisión de mesa sobre si vale escribir extractores nuevos y para cuáles formatos"). Mesa marca UNA letra:

- **a — Rama estadística (recomendada por dirección):** miembros `.dta/.sav/.rdata/.dbf` dentro de zips causa B + los `.dta` sueltos hoy `NO-EXTRAIDO`. Es la rama de mayor volumen del ranking de `ADR-217` (125 miembros + 8 sueltos declarados; **el perímetro se re-deriva de `data/cobertura-composicion-v1_0.tsv` al arrancar, no se hereda esta cifra**) y son formatos de metadatos estándar (nombres + etiquetas de variable), legibles sin abrir el dato.
- **b — Rama pdf-FD:** los 32 PDF ficha-descriptiva (la de mayor densidad de valor: 25/32 alto valor, 78%) + los 46 FD no-xlsx de `FP-173`. Costo mayor (parsing de PDF, forma no uniforme).
- **c — Esperar** al resultado de E2 antes de decidir rama. `FP-175` se firma con esta letra y el acto se cierra sin ediciones salvo tablero.

---

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

**A.2, tercera parte (PARO-relevante en este acto):** `ls data/raw/ 2>/dev/null | head -1` — reporta el valor crudo. Este acto exige el corpus compartido enlazado (precedente: `/home/pc0/mm-corpus/raw`); ausente = asignación de entorno mal hecha, PARA.

**En esta caja, `grep` envuelve `ugrep -I` y tira no-UTF8 en silencio:** usa `command grep` siempre (v2.11, punto 6 del transfer), y todo negativo con su conteo de archivos (A.13).

---

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (maestra-32, 28/ago/2026, contra `2953716`) ═══

**1 · ESTRUCTURA.** Tablas gobernantes: `data/cobertura-composicion-v1_0.tsv` (la partición de los 404, nacida 27/ago) · `data/manifiesto.yaml` · `data/inventario-reactivos-v1_1.tsv` · `tools/inventario_reactivos.py` (se lee, no se toca). La entrada de índice para la familia de inventarios la añade `MAESTRA32-E2` (este acto está GATED a su merge): **al arrancar, verifica que existe** (`command grep -c "inventario" data/INFRAESTRUCTURA-v1_0.md` ≥ 1, con el conteo); si no, la premisa del gate falló — PARA y repórtalo.

**2 · CONTENIDO.** ¿Existe ya un despacho para la rama estadística, o la tabla destino? **NO-ENCONTRADO**, con universo: `tools/` (77 archivos) + `milpa/` (18): **0 hits de `pyreadstat`**; `tools/inventario_reactivos.py:48-50`: `FORMATOS_CON_CAMPOS = {.zip,.xlsx,.csv,.tsv,.txt}`, `FORMATOS_SIN_CAMPOS = {.xls,.html,.json,.pdf,.xml}` — `.dta/.sav/.rdata/.dbf` ausentes de ambos conjuntos, y la línea 129 manda todo lo demás a `NO-EXTRAIDO`. Destino `data/inventario-reactivos-ext-v1_0.tsv`: **NO-ENCONTRADO** (`ls data` = 63 entradas, 0 con `reactivos-ext`). La decisión que este acto ejecuta está pedida por el propio tablero: `FP-175.gatea` verbatim.

**3 · COBERTURA RETROACTIVA.** `cobertura-composicion-v1_0.tsv` nació el 27/ago — posterior a casi todo el corpus (payloads desde el 29/jul): por eso su partición **se re-deriva al arrancar** con la misma regla del propio E8 (nunca se hereda del `.meta` ni de este encargo). Y los veredictos de `MAESTRA32-E2` quedaron sellados sobre 316/720: **este acto es el que los vence en alcance** — el re-sello (`MAESTRA32-E4 · RE-EMPAREJA`, misma spec congelada de E2) queda declarado como sucesor, no lanzado.

═══════════════════════════════════════════════════════════════════

## 0-bis · A.3

Primer commit: este encargo verbatim, con la ranura YA LLENA, en `forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md`. Al cerrar, `## CONSUMIDO` con el PR.

## Premisas, con procedencia

1. Cobertura real del corpus: **316/720 (43.9%)**, no 97.78% — `ADR-217`, y las dos cifras se reportan juntas desde entonces. De los 404 no-OK: 204 causa A · 178 causa B · 22 causa C.
2. La rama (a) es puro metadato: nombres y etiquetas de variable, sin abrir valores. `pyreadstat` los lee con `metadataonly=True`.
3. Herramienta hermana, no cirugía sobre la existente: `MAESTRA31-E6` sentó el patrón (tabla hermana con mismo esquema; intocables verificados con `git diff --stat` vacío).
4. El único payload fallido de E6 (`mociba2020`, rótulo con salto de línea) se documentó y no se parchó — misma disciplina aquí.

**Verifica estas premisas antes de ejecutar (v2.1). Si alguna no se sostiene, PARA y repórtalo.**

## Objeto (rama a; la rama b usa la misma estructura con su perímetro)

Producir `data/inventario-reactivos-ext-v1_0.tsv` — tabla hermana del inventario general, mismo esquema de 9 columnas, `metodo="INSPECT_STATA"` (o el que corresponda por formato) — sobre el perímetro re-derivado de `cobertura-composicion-v1_0.tsv`: filas causa B con extensión de la rama + los sueltos `NO-EXTRAIDO` de la rama. Cero payloads nuevos, cero re-corrida del inventario general.

## Paso previo · herramienta disponible

`python3 -c "import pyreadstat; print(pyreadstat.__version__)"`. Si falta: `pip install pyreadstat --break-system-packages`, registra versión. Si la caja no alcanza pypi: **"NO OBTENIDO POR ESTE AGENTE EN N INTENTOS"** con las N salidas crudas (A.5) + receta manual de un minuto (descargar el wheel en otra máquina y dejarlo en el corpus compartido) — y PARA. Un fallo del agente es un hecho sobre el agente, no sobre la vía.

## COMMIT-1 — especificación congelada ANTES de abrir un solo payload

`forense/notas/2026-08-28-extractor-ext-spec.md`: (a) perímetro re-derivado por comando, con el conteo y la partición pegados; (b) regla de extracción: `variable_id` = nombre de columna; `texto_reactivo` = etiqueta de variable; `metadataonly=True`; si un formato no lo soporta, lectura mínima declarada (`row_limit=0` o equivalente) — nunca valores al inventario; (c) manejo de zips: miembro extraído a tmp, leído, tmp limpiado; un payload aporta todos sus miembros de la rama; (d) codificaciones: utf-8 → latin-1 fallback, declarado por fila; (e) **falsador: cobertura <50% del perímetro ⇒ se abandona la vía, no se itera la regla** (precedente E4/E6); (f) **B-bis:** cobertura alta = el corpus se abre en N payloads y la capa de texto crece para RE-EMPAREJA; cobertura baja = hallazgo de heterogeneidad de formato con la lista de qué falló — ambos desenlaces informativos, declarado antes de ver el dato. Cierra con: **"el primer resultado que produzca este procedimiento es el que se reporta."**

## COMMIT-2 — corrida única

La tabla + `tools/inventario_reactivos_ext.py` + cobertura verificada por comando (`awk` sobre la tabla, estilo E6: filas totales, filas con texto, payloads con ≥1 fila / perímetro). Fallos por payload: documentados con su error crudo, no parchados. Intocables verificados: `git diff --stat` vacío sobre `tools/inventario_reactivos.py`, `data/inventario-reactivos-v1_1.tsv`, `data/inventario-fd-v1_0.tsv`. Si el acto verifica integridad de algún payload contra el manifiesto: **una invocación por `--id`** (A.1), tres respuestas sin colapsar; y si el formato trae token de sesión, doble hash (A.7).

## Cierre — el defecto de PR #77

Antes de abrir el PR: confirma que la tabla, la herramienta y las notas están en el árbol commiteado (no solo en el worktree) y que ningún residuo quedó en tmp o en `data/raw` local sin declarar.

## PERÍMETRO Y CONCURRENCIA

Archivos que este acto puede tocar, y ningún otro: `forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md` · `tools/inventario_reactivos_ext.py` (nuevo) · `data/inventario-reactivos-ext-v1_0.tsv` (+ su `.meta` si el patrón de la casa lo pide) · `forense/notas/2026-08-28-extractor-ext-spec.md` · `forense/notas/2026-08-28-extractor-ext-cierre.md` · `forense/firmas-pendientes.tsv` (`FP-175` → FIRMADA con la letra; fila nueva del rango) · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · `canon/registro-rotulos.tsv` · `tests/check.py` (solo `_T25_ARCHIVOS_CONOCIDOS`). **No toca** `tools/inventario_reactivos.py`, ningún inventario existente, `milpa/**`, `hitoD-preregistro`. Concurrencia: ninguna — serie estricta. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

## FP pre-asignadas

Rango `FP-183`–`FP-184` (re-deriva el máximo real del tablero al escribir). Uso previsto: "mesa recibe la cobertura ext: 316→316+N de 720, las dos cifras juntas". Renumera quien fusiona segundo.

## ADR y cascada

Candidato re-derivado con el comando de la casa contra el árbol ya fusionado con E2 (**deriva, no heredes**). Cascada estándar: cabecera, recifrado L0, `registro-rotulos` (`MAESTRA32-E3` censado; token pelado se censa, no se reclama), T25, nota de cierre con A.13 en todos los conteos.

## CONTADOR

**Payloads con ≥1 fila: 316 → 316+N sobre 720** (las dos cifras juntas, regla de `ADR-217`) · filas de reactivo nuevas en la tabla hermana. Con letra c: cero directo, declarado.

## Lo que este acto NO hace

No re-corre el inventario general ni toca sus 178,246 filas. No empareja contra el motor (eso es RE-EMPAREJA, sucesor). No adjudica rutas ni casillas. No descarga nada. No abre valores de dato — solo metadatos. No decide la rama: la letra de mesa la decide.

## Sucesores declarados, no lanzados

`MAESTRA32-E4 · RE-EMPAREJA` (misma spec congelada de E2 sobre el universo ampliado; sus veredictos re-sellan los de E2, A.10 corolario 1) · la rama no elegida de M-EXTRACTOR queda viva en `FP-175`/su fila nueva para decisión posterior.
