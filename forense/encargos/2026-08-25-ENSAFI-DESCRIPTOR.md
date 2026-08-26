# ENCARGO ENSAFI-DESCRIPTOR — una descarga quirúrgica (el descriptor/FD de ENSAFI 2023) y el re-censo C1 que FP-157 está esperando

> **Archivado verbatim (`A.3`) por `ACTO ENSAFI-DESCRIPTOR`, 26/ago/2026.**
> **Estado: CONSUMIDO.** Ejecutado íntegro; cierre en
> `forense/notas/2026-08-26-ensafi-descriptor-cierre.md`, adjudicado en `ADR-198`.

---

SHA de redacción: dad74ee. Dirección, 25/ago/2026. ENTORNO: UBUNTU — descarga + apertura de corpus; la NUBE no puede ninguna de las dos. No NUBE, no doble. FIRMA: ninguna — ejecuta el paso que el cierre de #365 dejó escrito; FP-157 la adjudica mesa después, con el veredicto real en la mano.

Por qué existe, del canon. #365 (R34-ENSAFI-CENSA) cerró C1 = NO-ACCESIBLE: el microdato está completo y abierto, pero los 354 códigos P no son buscables por término porque ENSAFI 2023 no tiene descriptor en el corpus (987 archivos: 0 descriptores ENSAFI, 32 de otras encuestas como control). La respuesta está encerrada, no ausente — y su nota lo dice verbatim: la opción de adquisición de FP-157 «depende enteramente de si el descriptor es obtenible, y mesa no puede decidir a ciegas». Este acto lo obtiene y re-corre el escaneo. La ruta ya está pavimentada: la nota de adquisición del 12/ago (forense/notas/2026-08-12-acto-m-adq-ensafi-enfih.md) verificó byte a byte que el portal publica los cuestionarios por sección (pestaña «Materiales de Referencia») y localizó el patrón de FD (…/programas/ensafi/2023/microdatos/ensafi_2023_fd.xlsx, candidata FP-115(c) derivada por patrón, SIN-FETCH hasta hoy).

════ ARRANQUE ════ 1·REPO. 2·SHA vs dad74ee; si avanzó: refresca y reporta. 3·data/raw sustantiva: corpus enlazado y reportado. ⚠️ Este acto DESCARGA: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree (defecto PR #77). 4·ENTORNO tres partes (A.2): sin_variable · sonda INEGI cruda (nunca curl -I) · ls data/raw/; sin corpus → PARO. 5·Cero cifras del espejo. Negativos con conteo + control positivo (A.13). ════

═══ EXISTENCIA (dirección, contra dad74ee) ═══ Descriptor ENSAFI en corpus: 0 (el censo de #365 lo estableció con control 32). En manifiesto: ensafi2023_bd_csv_zip y compañía (la BD), ningún id de FD/cuestionario — verifícalo (grep -n "ensafi" data/manifiesto.yaml, pega la salida). Si el descriptor ya está registrado al arrancar → salta a F2 y decláralo (A.8). ═══

F1 · La descarga, con la disciplina completa
Intenta la candidata por patrón: https://www.inegi.org.mx/contenidos/programas/ensafi/2023/microdatos/ensafi_2023_fd.xlsx (deriva la URL exacta del patrón vivo del manifiesto para ENASIC/ENFIH, no la teclees de aquí). Si 404: deriva desde la página del programa (/programas/ensafi/) y su pestaña de Materiales de Referencia — el cuestionario por secciones que el 12/ago se verificó byte a byte también sirve como descriptor de términos si el FD no existe como archivo aparte.
Todo fallo: «NO OBTENIDO POR ESTE AGENTE EN N INTENTOS» + salida cruda + receta manual de 1 minuto por pieza (mesa ya ha bajado a mano lo que agentes declararon inexistente — la receta es el entregable de mayor rendimiento, medido).
Lo obtenido: al corpus compartido, registrado en data/manifiesto.yaml con --registra, verificación A.1: una invocación por --id, salida cruda pegada.
F2 · El re-censo C1, sobre el descriptor

Corre el MISMO escaneo que #365 dejó parametrizado (sus 16 términos: SAT, FISC, IMPUEST, VIGIL, RASTRE, etc.) sobre el descriptor/cuestionario, con control positivo (términos financieros que SÍ deben aparecer). Veredicto A.4 real por constructo — el que #365 no pudo dar: EXISTE-SATISFACE (ítem fiscal presente: pega la pregunta verbatim, el código P que mapea, el universo del módulo y el formato de respuesta — la spec-candidata para el medidor de B queda servida) o EXISTE-NO-SATISFACE/NO-ENCONTRADO (ENSAFI no lo trae: el censo de la condición B queda exhaustivo — ENIF, ENDUTIH, IFT, ENCIG, ECF, ENAFIN y ENSAFI, todas abiertas — y FP-157 se decide sobre terreno completo).

F3 · Cierre

Anexo-2 por append a forense/ficha-r34-condBC-v1_0.md («Anexo ENSAFI-descriptor, fecha, veredicto») · enmienda fechada a FP-157: «descriptor obtenido y censado; veredicto C1 real = ___ — mesa puede adjudicar» · nota -cierre con tabla término·hit·pregunta-verbatim · ADR · estado · tablero (solo esa enmienda) · suite --baseline · encargo CONSUMIDO. CONTADOR: cero, declarado — este acto le da a mesa el terreno; el gate lo mueve su firma.

Perímetro y NO-hace

Lista cerrada: corpus compartido + data/manifiesto.yaml (alta del descriptor) · ficha condBC (append) · tablero (FP-157 enmienda) · gobernanza · estado · notas · encargo. "Fuera de esta lista, PARA." No mide B (eso es el medidor, dos commits, acto aparte). No adjudica FP-157. No toca tests/aceptacion_r3_4.py. No baja nada más que el descriptor/cuestionario de ENSAFI 2023.
