# ENCARGO E5 · SELLA-FP164-OCTAVA — propaga la firma de mesa: el ITT de `EXP-COMPARTAMOS-1` entra como fila NUEVA bajo la octava clase de `milpa/procedencia.yaml`

Dirección (maestra-30), 26/ago/2026 · SHA de redacción `8b317d3` (verificado vivo: `origin/main` tras fusionar #373/#374; clon propio, `git status` limpio) · Cifras: clase (1), derivadas en esta sesión con el comando a la vista.

ENTORNO ASIGNADO: NUBE (`cloud_default`, repo-only). NO lanzar en UBUNTU ni en Codex. No abre microdato ni red. Puede correr en paralelo con `E6` (otra caja); ver PERÍMETRO.

RANURA DE MESA — FIRMA, precargada con el verbatim ya dictado

FIRMA M-FP164: «FIRMO FP-164: opción (b) — "Entonces a tu pregunta, entra a fila nueva con la octava clase." (mesa, chat de dirección, 26/ago/2026).»

Compuerta: vacía o alterada a algo que no sea (b) afirmativo → el acto solo archiva el encargo (A.3) y reporta; nada se escribe en `milpa/`.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.
2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.
3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.
4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: cloud_default (este acto es NUBE) curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.
5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — la contesta quien ESCRIBE el encargo [NUEVO v2.8] ═══ CONTESTADA por dirección, 26/ago/2026, clon en `8b317d3`:

1 · ESTRUCTURA. Dominio: procedencia del motor. Gobernante: `milpa/procedencia.yaml` — la octava clase `EVIDENCIA_EXPERIMENTAL_TERCEROS` está definida en `:59` (sellada 25/ago/2026, `ADR-184`; `cita`+`llave_id` obligatorios, "no admite llave pendiente") y su llave ya está `EJERCIDA_CORROBORA` en `forense/registro-llaves-identificacion-v1_0.md` — la condición de la clase se cumple. Tablero: `forense/firmas-pendientes.tsv` (A.12). `INFRAESTRUCTURA-v1_0.md` no gobierna `milpa/` — declarado.
2 · CONTENIDO.

* `awk -F'\t' '$1=="FP-164"{print $6}' forense/firmas-pendientes.tsv` → ABIERTA (única del tablero). La fila trae el número completo, verbatim: ITT +1.1009 pp sobre `A_ever_late_not_cond` ("client was ever late on payments", registro administrativo de Compartamos), IC95% [+0.6423, +1.5595], N=16,560, G=238 conglomerados, t de 237 gl, ola de seguimiento del paquete `116334-V1` (Angelucci, Karlan & Zinman, AEJ:Applied, openICPSR 116334-V1); primera etapa: adopción administrativa +11.4735 pp [+9.7022, +13.2448] sobre base 5.845 pp; escala pp, "JAMÁS comparada contra el techo de mora 15-20% ni contra el umbral de IMOR 25-30% de `dinero.credito.scoring_alternativo`".
* La fila que este encargo manda crear NO existe: `grep -n "EVIDENCIA_EXPERIMENTAL_TERCEROS" milpa/procedencia.yaml` → 2 hits sobre 1 archivo (patrón completo, A.13): `:59` (definición, VACÍA) y `:744` (excepción fechada de `Progresa_RCT`, que NO es fila de la clase) → NO-ENCONTRADO como entrada de datos.
* Insumo pineado: `forense/resultado-exp-compartamos-v1_0.md`, sha256 `513925ecff6cfcbc…`, 207 líneas — todo número que escribas sale de ahí o de la fila FP-164, nunca de memoria.

3 · COBERTURA RETROACTIVA. Clase nace 25/ago (`ADR-184`); resultado nace 26/ago (#374). Nada anterior pudo pasar por la clase; sin brecha.

════════════════════════════════════════════════════════════════════

OBJETO

Escribir la primera fila de datos de la octava clase — estrena el conducto que `ADR-184` dejó vacío — y cerrar `FP-164` → `FIRMADA`. Tablero en 0 ABIERTA. Un PR.

PASOS

0-bis · A.3: commitea este encargo íntegro en `forense/encargos/2026-08-26-E5-SELLA-FP164-OCTAVA.md`; al cerrar, `## CONSUMIDO` con el PR.
1 · Compuertas: pega la fila `FP-164` y el grep de la clase (2 hits, definición+excepción); verifica el sha del resultado contra `513925ecff6cfcbc…` — discordante → PARO (A.7: di qué campo).
2 · La entrada nueva en `milpa/procedencia.yaml`, bajo la regla `dinero.credito.baja_friccion_usura_dano_downstream`, con clase `EVIDENCIA_EXPERIMENTAL_TERCEROS`. Campos: exactamente los que la definición de la clase (`:59` y su bloque) enumera — léelos ahí y usa el molde de las otras clases del archivo para el estilo; no inventes campos ni omitas los obligatorios. Contenido, todo citado del resultado/fila: `llave_id: EXP-COMPARTAMOS-1` · `cita:` Angelucci, Karlan & Zinman (AEJ: Applied), openICPSR `116334-V1` · el ITT, IC, N, G, gl, ola y variable de arriba, verbatim · escala: pp de `A_ever_late_not_cond`, ITT por conglomerado — sin enlace declarado hacia ninguna otra escala (A-bis 3) · primera etapa de adopción como contexto · `que_sostiene`: corrobora la dirección del mecanismo (baja fricción + expansión de acceso → daño downstream medible); NO calibra ni sustituye la magnitud del `[MEDIA](a)` vigente (`canon/modelo-decision-v4_0.md:501` queda intacto — sustituirlo sería acto propio de mesa, no éste) · estampa A.10 (universo: este paquete, esta ola, este N; un experimento/estado/producto) · fecha y ADR.
3 · `FP-164` → `FIRMADA`: `firmada_en` = el verbatim de la RANURA + fecha; `ejecutada_en` = ADR de este acto. Tablero: 0 ABIERTA — dilo en la nota.
4 · Si algún test asumía la clase vacía y truena, ajuste mínimo declarado en la nota, cero lógica nueva (mismo patrón que #373/#374 con T25). Nada más de `tests/` se toca.
5 · Nota `forense/notas/2026-08-26-sella-fp164-cierre.md` · ADR (máximo re-derivado por `re.findall` — hoy 203, sin huecos → candidatea `ADR-204`; renumera al fusionar si `E6`/`E7` u otro toman el número) + recifrado `estado §L0` · `tests/check.py --baseline` verde · PR.

PERÍMETRO Y CONCURRENCIA

Toca SOLO: `milpa/procedencia.yaml` (una entrada nueva) · `forense/firmas-pendientes.tsv` (fila FP-164) · nota nueva · `forense/encargos/…E5….md` (A.3) · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · `tests/` solo bajo el paso 4, declarado. Concurrentes: E6 (caja con red; `forense/prereg-duelo-v2/corridas-L/`) y E7 (UBUNTU, posterior a E6) — colisión esperada solo en gobernanza/estado por recifrado ADR: renumera quien fusiona segundo, conserva íntegro lo ajeno. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

PROHIBIDO

Tocar el `[MEDIA](a)` de `modelo-decision:501` o cualquier línea de `canon/modelo-decision-v4_0.md` · tocar `milpa/refutations.yaml` · reclasificar la excepción `Progresa_RCT` (`:744` queda como está) · comparar el ITT contra escalas de otras reglas · reescribir una sola cifra de memoria.

CONTADOR

Cero directo, declarado — el número ya se midió en #374; este acto lo aloja en el ejecutable. Tablero 1→0 ABIERTA. La octava clase pasa de VACÍA a 1 fila (primer consumo formal de evidencia clase (iii) del programa).

## CONSUMIDO

Ejecutado 26/ago/2026 por `ACTO E5-SELLA-FP164-OCTAVA` (ADR-204). Ver `forense/notas/2026-08-26-sella-fp164-cierre.md` para el detalle de verificación y cierre. PR: ver historial de este branch (`claude/sella-fp164-octava-firma-jeywm9`).
