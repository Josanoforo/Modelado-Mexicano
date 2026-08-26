# Encargo `E3 · EJERCE-LLAVE-COMPARTAMOS` — ejerce `EXP-COMPARTAMOS-1` bajo la spec sellada; llaves de identificación 4→5 de 5

**Archivado verbatim (A.3) por el acto que lo consume. Dirección (maestra-30), 26/ago/2026 · SHA de redacción `186f090`.**

---

ENCARGO E3 · EJERCE-LLAVE-COMPARTAMOS — ejerce EXP-COMPARTAMOS-1 bajo la spec sellada; llaves de identificación 4→5 de 5

Dirección (maestra-30), 26/ago/2026 · SHA de redacción 186f090 (verificado vivo; clon propio, git status limpio) · Cifras: clase (1), derivadas en esta sesión.

ENTORNO ASIGNADO: UBUNTU (corpus montado; el microdato vive ahí). NO lanzar en NUBE ni en Codex. En la caja UBUNTU corre DESPUÉS de E4 (E4 es corto y toca otro archivo; secuencial evita dos merges simultáneos desde la misma caja). Acto de estimación: rige la regla de dos commits del Bloque D.

RANURA DE MESA — DESTINO del número (disyuntiva §1 de la spec; precargada VACÍA)

DESTINO M-EXPCOMP: VACÍA — mesa escribe (a) o (b) antes de lanzar, o la deja VACÍA. (a) = el ITT compite por el sitio del [MEDIA](a) vigente de dinero.credito.baja_friccion_usura_dano_downstream (sustituirlo sigue exigiendo acto propio de mesa) · (b) = entrada NUEVA en milpa/procedencia.yaml bajo la octava clase EVIDENCIA_EXPERIMENTAL_TERCEROS (cita+llave_id obligatorios), sin tocar el [MEDIA](a).

Compuerta: la firma de FP-160 (ADR-199, opción (a) de esa fila) selló la spec y habilitó este acto — no eligió el destino de §1. Con la ranura VACÍA, el acto ejerce la llave igual (el registro de llaves es el entregable), el número queda PROPUESTO con fila A.12 nueva para mesa, y milpa/ no se toca — mismo patrón que CAL-G3 (EJERCIDA_ACOTA con β PROPUESTO, FP-127). Solo con (b) escrito se escribe la entrada en milpa/.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo. A.2, tercera parte: ls data/raw/ 2>/dev/null | head -1 — el corpus DEBE estar montado; en UBUNTU grep envuelve ugrep -I: usa command grep y decláralo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — la contesta quien ESCRIBE el encargo [NUEVO v2.8] ═══ CONTESTADA por dirección, 26/ago/2026, clon en 186f090:

1 · ESTRUCTURA. Dominio: ejercicio de llave de identificación clase (iii). Gobernantes: forense/spec-bbis-exp-compartamos-v1_0-PROPUESTA.md (SELLADA por estado — FP-160 FIRMADA, ADR-199, opción (a) de la fila: «pasa a v1.0 congelada, habilita el acto EJERCE-LLAVE posterior en UBUNTU»; enmienda de estado, no de archivo — el nombre conserva -PROPUESTA) · forense/registro-llaves-identificacion-v1_0.md (fila EXP-COMPARTAMOS-1, hoy SELLADA_NO_EJERCIDA) · milpa/procedencia.yaml (octava clase :59, nace VACÍA, cita+llave_id obligatorios, ADR-184) · data/manifiesto.yaml (payload). INFRAESTRUCTURA-v1_0.md indexa data/ — cubre manifiesto; el resto es forense//milpa/, fuera de su dominio, declarado.

2 · CONTENIDO.

Payload: grep -n "116334" data/manifiesto.yaml → id 116334_v1 (:12448), archivo: Descargas Manuales/116334-V1.zip, url_origen openICPSR — EXISTE-SATISFACE; el censo de ADR-162 ya lo abrió a nivel de columna (124 variables, 21,523 filas; Treatment constante por conglomerado 238=120/118; seguimiento N=16,560).
Resultado previo del ejercicio: grep -rl "EJERCE-LLAVE" forense/ --include="*.md" → 3 hits sobre 1,558 archivos examinados (A.13), los tres leídos: la spec misma, hitoD-preregistro-v2_0.md y la nota de CIERRA-4-FIRMAS — referencias al acto futuro, ningún resultado → NO-ENCONTRADO. Ningún forense/resultado-exp-compartamos* (find, mismo universo).
Octava clase: grep -n "EVIDENCIA_EXPERIMENTAL_TERCEROS" milpa/procedencia.yaml → :59 (definición, VACÍA) y :744 (excepción fechada Progresa_RCT, no fila de la clase) — el conducto existe y está vacío, como debe.
Llaves ejercidas hoy (registro, filas leídas): CAL-G3=EJERCIDA_ACOTA · R5.1-D2=EJERCIDA_INDECISA · R5.1-D3=EJERCIDA_INDECISA · decreto RFN (ADR-166)=EJERCIDA_REFUTA → 4 ejercidas; EXP-COMPARTAMOS-1 es la única SELLADA_NO_EJERCIDA.

3 · COBERTURA RETROACTIVA. La spec (25/ago) y la octava clase (25/ago) son posteriores a la adquisición del payload (fila 110 del catálogo, Descargas Manuales/) — por eso el payload no las cita; no es hueco. Sin más brechas.

════════════════════════════════════════════════════════════════════

OBJETO

Correr exactamente el §2 de la spec sobre el microdato, adjudicar por la escala §4 con su precedencia, actualizar la fila del registro de llaves a EJERCIDA_*, y darle destino al número conforme a la RANURA. Llaves 5 de 5.

PASOS

0-bis · A.3: commitea este encargo íntegro en forense/encargos/2026-08-26-E3-EJERCE-LLAVE-COMPARTAMOS.md; al cerrar, ## CONSUMIDO con el PR. 1 · Compuerta cero: pega la fila FP-160 (estado FIRMADA) y la cita de ADR-199; verifica el hash del payload 116334_v1 contra el manifiesto, una invocación tests/manifiesto.py --verifica (A.1; las tres respuestas AUSENTE / raíz-no-configurada / hash-discordante no se colapsan). 2 · COMMIT-1 — especificación congelada, ANTES de abrir un solo valor (forense/resultado-exp-compartamos-v1_0.md, §COMMIT-1): universo = ola de seguimiento, N=16,560, unidad persona (mujer 18-60); tratamiento = Treatment; estimador = ITT por conglomerado, EE agrupados por conglomerado (vce(cl cluster) o equivalente exacto en tu stack), sin ponderador adicional salvo que los .do del propio paquete lo usen (cítalo si sí); desenlaces = lista cerrada derivada SOLO de nombres/etiquetas del codebook y los .do del paquete (permitido leer nombres y etiquetas; prohibido mirar un valor antes de este commit): adopción (in_admin, Q21_3_comp) + toda variable que el codebook nombre como mora/atraso/cobranza (daño downstream) — si ninguna variable de daño existe por nombre, decláralo aquí (candidato inejecutable §4, mesa ya autorizó la escala). Cierra con la frase, verbatim: «el primer resultado que produzca este procedimiento es el que se reporta». 3 · COMMIT-2 — resultados, sin editar el COMMIT-1: ITT en pp por desenlace, IC95% agrupado, N y conglomerados efectivos por corrida; adjudicación por §4 con la precedencia sellada rompe → inejecutable → acota → corrobora → no-refuta — nunca fuerces una fila por cercanía; IC que no despeja el umbral en ninguna dirección = no-refuta con la reserva A-bis escrita. Si la especificación resultó mal, tercer commit lo dice; nunca se corrige hacia atrás. 4 · Registro de llaves: fila EXP-COMPARTAMOS-1 → EJERCIDA_<mapa §4> (corrobora→EJERCIDA_CORROBORA · acota→EJERCIDA_ACOTA · rompe→EJERCIDA_REFUTA · no-refuta→EJERCIDA_INDECISA · inejecutable→queda SELLADA_NO_EJERCIDA con la razón y NO cuenta como ejercida — dilo), con resultado, escala pp declarada (A-bis 3: jamás comparada contra el «techo de mora 15-20%» de scoring_alternativo, que es otra escala y otro objeto), estampa A.10 (universo: este zip, esta ola, este N) y fecha. 5 · Destino según RANURA: (b) → entrada nueva en milpa/procedencia.yaml octava clase con cita (Angelucci, Karlan & Zinman, AEJ:Applied, openICPSR 116334-V1) + llave_id: EXP-COMPARTAMOS-1 + escala + estampa; (a) → milpa/ intocado, número PROPUESTO para competir por el [MEDIA](a) con fila A.12 nueva (mesa decide la sustitución); VACÍA → milpa/ intocado, número PROPUESTO, fila A.12 nueva («mesa elige destino (a)/(b) del ITT de EXP-COMPARTAMOS-1»). 6 · Nota forense/notas/2026-08-26-ejerce-llave-compartamos-cierre.md · ADR (máximo re-derivado; renumera al fusionar — E1/E2/E4 también emiten) + recifrado estado §L0 (línea de llaves: 4→5 de 5 si aplica) · tests/check.py --baseline verde · PR.

PERÍMETRO Y CONCURRENCIA

Toca SOLO: forense/resultado-exp-compartamos-v1_0.md (nuevo) · forense/registro-llaves-identificacion-v1_0.md (una fila) · milpa/procedencia.yaml (solo si RANURA=(b)) · forense/firmas-pendientes.tsv (solo fila A.12 nueva si (a)/VACÍA) · nota nueva · forense/encargos/…E3….md (A.3) · canon/gobernanza-v1_15.md · canon/estado-programa-v1_10.md. Concurrentes: E4 (misma caja, antes; data/diseno-muestral.yaml) · E1/E2 (NUBE) — colisión esperada en gobernanza/estado/tablero por recifrado: renumera quien fusiona segundo. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

PROHIBIDO

TOT/LATE (in_admin como instrumento) · BTreatment/línea base salvo declaración explícita §2 con su propia justificación · abrir un valor del microdato antes del COMMIT-1 · comparar el ITT contra escalas de otras reglas sin enlace declarado · tocar el [MEDIA](a) de modelo-decision · segundo intento de especificación · descargar nada (el payload ya está; si el hash no COINCIDE, es PARO, no re-descarga).

CONTADOR

Llaves de identificación ejercidas 4→5 de 5 (salvo inejecutable, que se reporta como tal). Hito D: sin movimiento. Es una medición — la sesión cumple la regla de señal por sí sola.

---

## CONSUMIDO

**CONSUMIDO** por `ACTO MAESTRA30-E3 · EJERCE-LLAVE-COMPARTAMOS`, 26/ago/2026, `ADR-203`, **PR #374**. Veredicto: `EXP-COMPARTAMOS-1` → `EJERCIDA_CORROBORA`, llaves de identificación `4` de `5` → `5` de `5`; el ITT queda `PROPUESTO` (la `RANURA DE MESA` llegó VACÍA), `milpa/procedencia.yaml` y el `[MEDIA](a)` intocados, fila `FP-164` `ABIERTA`. Ver `forense/resultado-exp-compartamos-v1_0.md` y `forense/notas/2026-08-26-ejerce-llave-compartamos-cierre.md`.

*(Nota sobre el rótulo: este archivo conserva verbatim el texto de dirección, que lanzó el acto como «E3». `D-6`/`T25` exige que un rótulo nuevo no sea letra+número pelado —`E3` ya tiene dos habitantes censados—, así que el acto se declara `MAESTRA30-E3` en todos los archivos que escribe y se censa en `canon/registro-rotulos.tsv`; el texto de dirección no se edita para complacer a un test. Ver nota del acto §8.)*
