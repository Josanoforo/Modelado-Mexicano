ENCARGO · ACTO MAESTRA32-E14 · MARCO-M-SORTEA (ACTO B′)

SHA de redacción: 9bd3932 (main, merge PR #401 / ADR-229) · Redactado: 31/ago/2026, dirección maestra-32 · Instrucciones vigentes: v2.11 · Estado: GATED por construcción a que MAESTRA32-E13 · MARCO-M-CONGELA fusione en main: la semilla se deriva del SHA de ese merge (semilla_desde_sha_merge(SHA_A, "MARCO-M-v1")), y sin SHA no hay semilla. Sin ranuras. Todo lo que este acto ejecuta quedó pre-registrado en el COMMIT-1 de E13 (§e), antes de ver N_elegibles.

ENTORNO ASIGNADO: CAJA (repo-only; NUBE reservada a E4 mientras corra). Si al lanzar E4 ya cerró, CAJA sigue siendo el asignado: no se lanza en NUBE.

CARRILES EN PARALELO (declarado): carril CAJA = E13 → E14 (este); carril NUBE = E4. Compartidos: solo la cascada. Renumera quien fusiona segundo.

FIRMAS — ninguna nueva

Ejecuta la firma F2 de E13 (D1′ = (ii)) bajo el reglamento sellado ADR-178/FP-150. Sin decisiones de este acto: n_sorteo, cuota_max, scope_id y la regla de tamaño están fijados en forense/notas/2026-08-31-marco-M-spec.md §e; este acto los lee, no los elige.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

Además del ARRANQUE, la compuerta: git log --oneline origin/main | command grep -c "MAESTRA32-E13" ≥ 1 y git merge-base --is-ancestor <SHA_A> HEAD verdadero, donde SHA_A es el commit de merge del PR de E13. Sin eso, PARA: no hay semilla que derivar.

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (maestra-32, 31/ago/2026, contra 9bd3932, con la parte que solo E13 puede cerrar declarada como tal) ═══

1 · ESTRUCTURA. Igual que E13: familia forense/prereg-duelo-v2/, reglamento sorteo-act-pil-3-v2-PROPUESTA.md, mecanismo sorteo_v2.py, precedente sorteo-resultados-v1_0.md (el ACTO B original: pre-registro de SHA_A, semilla derivada, invocación exacta, "el primer resultado que produzca este procedimiento es el que se reporta", salida íntegra en el segundo commit).

2 · CONTENIDO. (i) Un sorteo del marco-M: NO-ENCONTRADO hoy (no existe el marco-M; E13 lo crea). (ii) sorteo_v2.py:cargar_marco trae assert n=50 contra el congelado original: no aplica al marco-M y no se edita — este acto escribe forense/prereg-duelo-v2/sorteo_marco_m.py, que importa sortear y semilla_desde_sha_merge de sorteo_v2.py y carga marco-M-congelado-v1_0.tsv con assert n == N_elegibles leído de CONGELADO-M-v1_0.sha256. (iii) tests_sorteo_v2.py sigue siendo la prueba del mecanismo; el cargador nuevo se prueba con un caso propio (mismo estilo).

3 · COBERTURA RETROACTIVA. El sorteo original (ACTO B, PR #353→merge 887508a) es el precedente exacto; su semilla anulada (ADR-135(d)) no se reutiliza. La regla §3.4 del reglamento (no reutilizar semillas) se hereda: scope_id distinto (MARCO-M-v1) garantiza semilla distinta.

═══════════════════════════════════════════════════════════════════

0-bis · A.3

Primer commit: este encargo verbatim en forense/encargos/2026-08-31-MAESTRA32-E14-MARCO-M-SORTEA.md. Al cerrar, ## CONSUMIDO con el PR.

COMMIT-1 — pre-registro ANTES de correr el PRNG (patrón sorteo-resultados-v1_0.md)

forense/prereg-duelo-v2/sorteo-marco-M-resultados-v1_0.md, sección "Pre-registro del primer commit": SHA_A (merge de E13, verificado ancestro de HEAD); scope_id = "MARCO-M-v1"; semilla derivada por semilla_desde_sha_merge(SHA_A, "MARCO-M-v1"), impresa; N_elegibles leído de CONGELADO-M-v1_0.sha256 y el sha256 recomputado que debe coincidir (PARO si no); n_sorteo y cuota_max aplicando la regla de tamaño de E13 §e, con la aritmética a la vista; la invocación exacta a ejecutar; y la frase: "el primer resultado que produzca este procedimiento es el que se reporta." Más sorteo_marco_m.py y su prueba.

COMMIT-2 — una sola corrida

Salida íntegra de sortear(marco_M, n_sorteo, cuota_max, semilla) en la misma nota (segunda sección), + forense/prereg-duelo-v2/marco-M-sorteado-v1_0.tsv (las filas sorteadas, columnas del marco) + verificación de las tres invariantes del reglamento (tamaño, publicada=SI ≤ cuota_max, piso 1 por estrato no vacío si aplica). Si N_elegibles < 15, el "sorteo" es la identidad y se sella igual (E13 §e). Intocables (git diff --stat vacío): sorteo_v2.py, tests_sorteo_v2.py, marco-M-congelado-v1_0.tsv, CONGELADO-M-v1_0.sha256, todo el duelo original, milpa/**.

PERÍMETRO Y CONCURRENCIA

Archivos: forense/encargos/2026-08-31-MAESTRA32-E14-MARCO-M-SORTEA.md · forense/prereg-duelo-v2/sorteo_marco_m.py (nuevo, + su prueba) · forense/prereg-duelo-v2/sorteo-marco-M-resultados-v1_0.md · forense/prereg-duelo-v2/marco-M-sorteado-v1_0.tsv · forense/firmas-pendientes.tsv (fila de recibo) · cascada. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

FP pre-asignadas

FP-193–FP-194 (re-deriva contra el árbol ya fusionado con E13 y E4; siguiente libre, declarado).

ADR y cascada

Candidato re-derivado (deriva, no heredes; renumera quien fusiona segundo). El ADR trae SHA_A, semilla, n_sorteo/cuota_max con su regla, las celdas sorteadas por estrato, y las invariantes verificadas. registro-rotulos: MAESTRA32-E14. T25.

CONTADOR

Celdas del marco-M sorteadas: n_sorteo (o N_elegibles si < 15) — el lado M del duelo deja de tener 0 celdas en su cancha.

Lo que este acto NO hace

No emite puntos M, no calcula R, no corre L, no toca el sorteo original, no elige parámetros.

Sucesores declarados, no lanzados

EMITE-M (nube: el motor emite su punto por celda sorteada, motor congelado, clases a la vista) · R-MARCO-M (caja: el árbitro calcula R por celda desde el microdato, dos commits) · L-MARCO-M (pipeline L sobre las mismas celdas) · scoring con FP-168 ya firmada cuando M, R y L existan.

## CONSUMIDO

Cerrado por `PR #404`. `SHA_A=f4d9b7f506aa5205231f6e7b355645d1206dd031` (merge de `MAESTRA32-E13`/`PR #403`, `ADR-231`, verificado ancestro y tip literal de `origin/main` al re-lanzar). `N_elegibles=2 < 15` → identidad, sin PRNG: `TRA-M-01`/`TRA-M-02` entran completas. `ADR-232`, `FP-193` (recibo, `FP-194` reservada), `MAESTRA32-E14` censado en `canon/registro-rotulos.tsv`.
