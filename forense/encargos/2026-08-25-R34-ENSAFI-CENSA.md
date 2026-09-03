# ENCARGO `R34-ENSAFI-CENSA` — archivado verbatim (`A.3`)

> **Estado: `CONSUMIDO`** · consumido el 25/ago/2026 por el acto homónimo.
> Cierre: `forense/notas/2026-08-25-r34-ensafi-censa-cierre.md` · `ADR-194` ·
> anexo en `forense/ficha-r34-condBC-v1_0.md` («Anexo ENSAFI, 25/ago/2026»).
> **CONTADOR: cero**, declarado en el propio encargo.

---

## Texto verbatim, tal como llegó de dirección

Encargo R34-ENSAFI-CENSA — abrir ENSAFI 2023 (ya en corpus) y censarla a nivel reactivo contra B/C de R3.4 · el insumo que FP-157 espera

SHA de redacción: ba0a7e4. Dirección, 25/ago/2026. ENTORNO: UBUNTU — abre microdato/documentación del corpus; la NUBE no tiene los bytes. No NUBE, no doble. FIRMA: ninguna — censa y propone; FP-157 la adjudica mesa después, mejor informada.

Por qué existe. #359 cerró B/C en cero EXISTE-SATISFACE con una sola ausencia colgando de todo: ningún instrumento censado mide percepción de riesgo fiscal/vigilancia al usar un medio de pago o gobierno digital. Su vía más barata era ENSAFI 2023 — la única candidata NO-ACCESIBLE por no abierta, no por no existir (verbatim de la ficha condBC). A.8 hizo su trabajo antes de pedir descargas: ENSAFI ya está descargada y registrada (data/manifiesto.yaml:3939, id ensafi2023_bd_csv_zip; 6 menciones ensafi sobre 15,426 líneas; portal resuelto vía /programas/ensafi/). Lo que nadie ha hecho es abrirla contra la pregunta. Eso, y solo eso, hace este acto.

════ ARRANQUE ════ 1·REPO: clon existente; git log -1·status. 2·SHA vs ba0a7e4; si avanzó: refresca y reporta. 3·data/raw sustantiva: enlaza al CORPUS COMPARTIDO y reporta cuál. 4·ENTORNO tres partes (A.2): CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado sin_variable · sonda curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ (NUNCA curl -I) · ls data/raw/; corpus no montado → PARO (la asignación de entorno falló — precedente medido 5/ago). 5·Cero cifras del espejo. Todo negativo con conteo de archivos y control positivo (A.13, estándar #359). ════

═══ EXISTENCIA (dirección, contra ba0a7e4) ═══ Payloads: ensafi2023_* en manifiesto (arriba). Censo B/C sobre ENSAFI: NO EXISTE — #359/ficha-r34-condBC-v1_0.md la deja explícitamente sin abrir; ningún anexo ENSAFI en la ficha (re-córrelo con conteo). FP-157 ABIERTA (única del tablero). Si al arrancar el censo ya existe o FP-157 ya se adjudicó → PARA y reporta (A.8). ═══

F0 · Compuertas
Verificación de payloads A.1: una invocación por --id (tests/manifiesto.py --verifica --id ensafi2023_bd_csv_zip, y cada id ensafi* que el manifiesto liste), salida cruda pegada; las tres respuestas sin colapsar (AUSENTE / raíz-no-configurada / hash-discordante — tres remedios distintos).
A.8 en fresco (bloque de existencia).
F1 · El censo, a nivel reactivo

Abre FD/cuestionario/documentación y, donde haga falta, cabeceras de la BD. Busca los cuatro constructos, cada uno con su control positivo (un término que SÍ debe estar — p. ej. "ahorro" o "crédito" para probar que el extractor lee):

Percepción de riesgo fiscal / SAT / vigilancia al usar pagos digitales o servicios financieros digitales — la pieza que apaga B.
Razones de no-uso de pagos/servicios financieros digitales (¿CoDi nombrado?).
Fricción declarada (dificultad, requisitos, fallas).
Confianza: canal personal vs institucional (¿misma batería, mismos individuos?). Por constructo: veredicto A.4 con la pregunta verbatim, el universo del módulo (a quién se le pregunta — filtros), y si es respuesta única o múltiple (el defecto que mató a ENIF para la conjunción de B — decláralo explícito).
F2 · Entrega — censar, no medir

Si el ítem fiscal aparece EXISTE-SATISFACE: 🚫 NO midas — entrega la spec-candidata (reactivo verbatim · universo · ponderador/diseño desde data/diseno-muestral.yaml o su ausencia declarada · qué conjunción permite) para el acto medidor de B (aparte, dos commits, A-bis completo), y añade enmienda fechada a la fila FP-157: «oferta nueva hallada en ENSAFI; gate re-evaluable — mesa decide con esto a la vista». Si no aparece: el NO-ENCONTRADO/EXISTE-NO-SATISFACE con universo completa el censo de #359 y FP-157 se decide sobre terreno ya exhaustivo — también es entregable. Cierre: anexo por append a forense/ficha-r34-condBC-v1_0.md («Anexo ENSAFI, fecha») + nota -cierre con la tabla constructo·reactivo·veredicto·universo · ADR · estado (línea R3.4) · tablero (solo la enmienda a FP-157) · suite --baseline (🚫 jamás --freeze) · encargo CONSUMIDO. CONTADOR: cero, declarado — este acto fabrica la información con la que mesa mueve el gate.

PERÍMETRO Y CONCURRENCIA

Lista cerrada: ficha condBC (append) · forense/notas/ (cierre) · gobernanza · estado · tablero (FP-157 enmienda) · encargo archivado · data/raw en LECTURA. "Fuera de esta lista, PARA." Concurrencia: Codex-CLI (disjunto), CORRE-R10.1 y SPEC-EXPCOMP-BBIS en paralelo — renumera quien fusiona segundo. No hace: no mide, no adjudica FP-157, no toca tests/aceptacion_r3_4.py, no descarga nada nuevo (si un archivo del zip faltara: NO OBTENIDO EN N INTENTOS + receta A.5, y para).

## CONSUMIDO

Derivado mecánicamente por `/tramite` (puertas 1–3 de la acción 3.3): único merge que introduce este archivo y toca otros además de él — `PR #365` (`e3bbaab1`, 2026-08-25, `Merge pull request #365 from Josanoforo/r34-ensafi-censa`, 6 files changed).
