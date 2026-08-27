ACTO MAESTRA31-E3, ENCARGO E3 · PERÍMETRO-ALCANZABLE

---
ENCARGO E3 · PERÍMETRO-ALCANZABLE — el número que la fase de cálculo necesita y que seis censos contradicen

Dirección (maestra-31), 26/ago/2026 · Redactado contra main = e5a36ab (clon propio, no espejo). No gated. PR #381 y #382 ya fusionados; este acto arranca sobre lo que dejaron.

ENTORNO ASIGNADO: UBUNTU. NO lanzar en NUBE — ahí corre MAESTRA31-E2. Este acto no descarga ni llama red; abre payload solo si el paso 4 lo exige, y por eso necesita el corpus montado. Rótulo: ACTO MAESTRA31-E3 (D-6). El token pelado E3 colisiona (hay habitante previo, E3-TRIAGE); se censa, no se reclama.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada. Nota derivada de E1 y E9: el clon /home/pc0/Modelado-Mexicano suele estar parado en acto/cal-g3-puntual. Crea worktree propio sobre origin/main.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Este acto NO descarga.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. A.2 tercera parte: ls data/raw/ 2>/dev/null | head -1 — corpus montado. Si sale vacío y el paso 4 lo necesita, PARA ahí, no antes. ⚠️ Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo declara cuántos archivos examinó el comando que lo produjo. En esta caja usa command grep y decláralo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

OBJETO

Producir forense/perimetro-alcanzable-v1_0.md: una sola cifra, derivada y no supuesta, de cuántos de los 30 parámetros del motor tienen hoy ruta a base medida, con las contradicciones entre los seis censos nombradas y adjudicadas o declaradas irreconciliables.

Contexto: la fase de cálculo está abierta desde el 20/ago (ADR-132). Tres hallazgos de las últimas 48h — M emite 1 de 60, el cruce da 0 de 49, la palanca #1 da 0 de 8 — podrían ser una sola cosa medida por separado. Este acto lo decide con dato.

Lo que este acto NO hace: no re-especifica ningún censo, no promueve nada a acto medidor, no adjudica qué hacer con el número, no toca el motor.

Las seis fuentes a re-derivar (NO confíes en las cifras de dirección, re-derívalas tú con comando):
- milpa/procedencia.yaml (parámetros del motor por clase de procedencia, y su rutas_estimabilidad_coeficiente.detalle)
- forense/censo-estimabilidad-coeficientes-v1_2.md (24/ago, tools/censo_estimabilidad.py)
- forense/cobertura-motor.md (24/ago) — reglas con valor numérico
- data/coef-universo-v1_0.tsv — veredicto A.4 por celda de coeficiente
- data/curacion-registro/cruce-oferta-demanda-v0_1.tsv — veredicto A.4 por demanda del motor
- forense/prereg-duelo-v2/enlace-M-v1_0.md — celdas donde el motor emite

PASOS

0-bis · A.3. Commitea este encargo íntegro y verbatim en forense/encargos/2026-08-26-MAESTRA31-E3-PERIMETRO-ALCANZABLE.md antes de nada (usa el texto completo de este mensaje como contenido del encargo, con su cabecera). ## CONSUMIDO al cerrar, con el número de PR.

1 · Re-deriva las seis cifras arriba. Deriva cada una con comando propio, pega comando y salida cruda, y prueba cada receta contra un caso conocido antes de correrla completa. Si tu cifra difiere de la de dirección (abajo), manda la tuya y dilo:
   Cifras de dirección (a re-verificar, pueden estar mal): procedencia.yaml → 30 parámetros: 4 medidos·6 derivados·13 asignados_probabilidad·1 experimental_terceros·6 asignados_coeficiente; rutas: 3 RUTA-A·2 RUTA-C·1 RUTA-I·9 SIN-RUTA. censo-estimabilidad-v1_2 → 3 RUTA-A·5 RUTA-C·1 RUTA-I·6 SIN-RUTA. cobertura-motor.md → 15 de 49 reglas con valor (refuta el 18/31 que procedencia.yaml declara). coef-universo-v1_0.tsv → 27 EXISTE-SATISFACE·21 EXISTE-NO-SATISFACE·10 NO-ENCONTRADO (58 filas). cruce-oferta-demanda-v0_1.tsv → 0 EXISTE-SATISFACE·7 EXISTE-NO-SATISFACE·41 NO-ENCONTRADO·1 NO-ACCESIBLE (49 filas). enlace-M-v1_0.md → 1 de 60 celdas emite.

2 · Adjudica estas tres contradicciones, una por una, cada una con veredicto ÚNICAMENTE uno de: RECONCILIADA (di cuál está desactualizada, fecha y acto), DOMINIOS DISJUNTOS (di qué mide cada una exactamente, citando definición del documento, por qué no son comparables — hipótesis de trabajo para C2), o IRRECONCILIABLE CON EL DATO DISPONIBLE (di qué haría falta y para ahí):
   C1. procedencia.yaml (2 RUTA-C·9 SIN-RUTA hoy) vs censo-estimabilidad-v1_2 (5 RUTA-C·6 SIN-RUTA, 24/ago) — 3 coeficientes cambiaron de clase sin anotar, o una cifra es falsa.
   C2. coef-universo (27/58 EXISTE-SATISFACE) vs cruce-oferta-demanda (0/49) — mismo vocabulario A.4, ¿mismo universo?
   C3. cobertura-motor.md ya refutó el 18/31 de procedencia.yaml por escrito, y ese estado: sigue diciendo 18/31 en el árbol dos días después.

3 · Construye la cifra final, estampa de universo (A.10): una fila por cada uno de los 30 parámetros de procedencia.yaml con: clase de procedencia · si tiene valor hoy · ruta declarada (RUTA-A/C/I/SIN-RUTA donde aplique) · veredicto A.4 de la fuente gobernante para ese parámetro (según adjudicación del paso 2) · contradicción que lo toca si alguna. Cierra con: N de 30 alcanzables, universo declarado en la misma línea (SHA, censos consultados, fecha), denominador explícito. Si un parámetro no cae limpio, fila SIN-CLASIFICAR con razón — no fuerces.

4 · Solo si el paso 2 lo exige: si adjudicar C2 requiere abrir un payload para saber qué mide realmente una tabla, ábrelo (mínimo, universo declarado). Si no, dilo y no abras ninguno.

5 · Cierre — produce TODO esto:
   - forense/perimetro-alcanzable-v1_0.md (entregable, el paso 3)
   - forense/notas/2026-08-26-perimetro-alcanzable-cierre.md con conteos A.13
   - FP-170 nueva fila en forense/firmas-pendientes.tsv: la cifra ante mesa, con las tres adjudicaciones
   - FP-169: pásala a FIRMADA-PARCIAL con esta condición textual: "se reabre si y solo si la adjudicación de C2 confirma que el cero es real" (ver RANURA M-RELOJ abajo)
   - FP-168: corrige SOLO la columna "desbloquea" (ver punto 6 abajo), nada más de esa fila
   - una línea en forense/hallazgos.md por cada contradicción que resulte real
   - enmienda FECHADA (no edición) al final de forense/notas/2026-08-25-cruce-oferta-demanda.md si tu hallazgo la toca — nunca alteres su texto original
   - ADR nuevo: número = máximo ADR existente + 1, re-derivado contando el árbol real (no confíes en un número que alguien te dé)
   - recifrado de la sección §L0 de gobernanza si esa sección existe y el proceso del proyecto lo exige (busca cómo se hace esto en ADRs recientes — es un mecanismo de hashing/checksum del canon, revisa un ADR reciente para ver el patrón exacto antes de tocarlo)
   - censo de rótulo en canon/registro-rotulos.tsv (añade fila para ACTO MAESTRA31-E3) y en tests/check.py SOLO en _T25_ARCHIVOS_CONOCIDOS si T25 lo exige
   - corre python3 tests/check.py --baseline y exige VERDE (nunca --freeze)
   - abre PR (no mergees)

6 · Corrección de una línea en FP-168: su columna "desbloquea" dice que firmar nivel_ic/seed sería suficiente para que ejecutar_scoring produzca resultado agregado. El §4 de ACTO MAESTRA30-E9 (búscalo en el árbol, forense/) establece por lectura de código que fallaría igual con SIN_CELDAS_PAREADAS. Corrige la columna "desbloquea" de FP-168 para que diga que hacen falta TRES cosas, no una (identifica las tres leyendo esa fuente). No toques el resto de la fila.

RANURA M-RELOJ (firmada por dirección, se propaga sin reinterpretar): FP-169 pasa a FIRMADA-PARCIAL con dos mitades ya decididas por dirección — (1) Alcance: lectura ACOTADA al cruce #363, "medición lanzada" cuenta solo lo que el cruce cite como evidencia, el falsador del 2026-09-08 no se dispara y se anota por enmienda fechada en la nota del cruce, sin editar el original. (2) Instrumento: NO se re-especifica todavía; se reabre si y solo si tu adjudicación de C2 (paso 2) confirma que el cero del cruce es real (no artefacto de dominio disjunto). Solo propaga esta firma tal cual a FP-169; si al ejecutar encuentras que la condición está mal fundada, PARA y repórtalo en vez de decidir tú.

PERÍMETRO Y CONCURRENCIA

Toca: forense/encargos/2026-08-26-MAESTRA31-E3-PERIMETRO-ALCANZABLE.md · forense/perimetro-alcanzable-v1_0.md (nuevo) · forense/notas/2026-08-26-perimetro-alcanzable-cierre.md (nuevo) · forense/firmas-pendientes.tsv (FP-170 nueva · FP-169 a FIRMADA-PARCIAL · columna desbloquea de FP-168 solamente) · forense/notas/2026-08-25-cruce-oferta-demanda.md (solo enmienda fechada al final) · forense/hallazgos.md · canon/gobernanza-v1_15.md · canon/estado-programa-v1_10.md · canon/registro-rotulos.tsv · tests/check.py (solo _T25_ARCHIVOS_CONOCIDOS).

NO toca: milpa/** (ni para corregir el 18/31 ya refutado — eso es de un sucesor con firma) · data/coef-universo-v1_0.tsv · data/curacion-registro/cruce-oferta-demanda-v0_1.tsv · forense/cobertura-motor.md · forense/censo-estimabilidad-coeficientes-v1_2.md · forense/prereg-duelo-v2/** · forense/hitoD-preregistro-v2_0.md · R10.3 ni de refilón.

Concurrencia: MAESTRA31-E2 corre en NUBE en paralelo (índice de infraestructura, alcance reducido). Colisión posible en gobernanza/estado/registro-rotulos/tests/check.py. E2 no abre fila de firmas; este acto toma FP-170. Quien fusione segundo re-numera su ADR contra el árbol ya fusionado.

"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

PROHIBIDO: editar cualquiera de los seis censos para que cuadren entre sí (la contradicción es el dato) · promover cualquier fila a acto medidor · decidir qué hacer con la cifra resultante · corregir procedencia.yaml · re-especificar el disparador riesgo_fiscal_percibido · adjudicar casilla/letra/tier (D-i vigente) · red/API/descarga · derivar cifra del espejo · escribir "no existe" sin comando y universo al lado.

CONTADOR: N de 30 con estampa de universo, más tres adjudicaciones de contradicción. Hito D, tiers y llaves: sin movimiento por diseño. Si las tres contradicciones son dominios disjuntos y la cifra no se puede construir sin séptimo censo, ESE hallazgo es el contador — no inventes una cifra.
---

## CONSUMIDO

PR #384 -- `ACTO MAESTRA31-E3 · PERIMETRO-ALCANZABLE`, 26/ago/2026.
