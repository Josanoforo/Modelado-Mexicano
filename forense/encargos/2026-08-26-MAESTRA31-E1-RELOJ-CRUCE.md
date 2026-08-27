[ENCARGO E1 · RELOJ-CRUCE — el falsador del 8/sep, contado, y la palanca #1 abierta byte a byte]

Dirección (maestra-31), 26/ago/2026 · Redactado contra `main = 6d213a6` (clon propio, no espejo).
GATED: no arranca hasta que PR #381 (ACTO MAESTRA30-E9 · SCORING-V2) esté FUSIONADO.

ENTORNO ASIGNADO: UBUNTU (la caja del corpus, /home/pc0/…). NO lanzar en NUBE ni en Codex — este acto abre payloads ya descargados y sin el corpus montado no tiene los bytes (A.2, tercera parte). No llama red ni API (FP-165).
Rótulo: ACTO MAESTRA31-E1 (D-6). El token pelado E1 colisiona; se censa, no se reclama.

ARRANQUE (hazlo antes de leer el resto):
1. REPO. Localiza el clon existente. No clones uno nuevo salvo que no haya ninguno; si clonas, dilo. Reporta ruta absoluta, `git log -1 --format="%h %s"`, `git status`. No arranques desde el home.
2. SHA. Confirma contra qué base trabajas vs la declarada (6d213a6). Si main se movió, no es PARO — refresca y reporta la diferencia.
3. data/raw. Ausente no es paro — es raíz integrada gitignorada. Reporta existe / la enlacé / la creé. Este acto NO descarga, solo lee lo ya descargado.
4. ENTORNO. Reporta `echo $CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` (esperado: vacío/sin_variable) y `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` (nunca -I). A.2 tercera parte OBLIGATORIA: `ls data/raw/ 2>/dev/null | head -1` — si sale vacío, PARA en este punto: la asignación de entorno estaba mal, repórtalo como hallazgo de mesa y no continúes con el censo de payloads (el contador sería cero con la razón escrita).
5. ESPEJO. Prohibido derivar cifras del espejo del proyecto. Toda cifra sale del clon de (1).

Si algo no cuadra en el arranque, PARA y repórtalo — encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

VERIFICACIÓN DE EXISTENCIA (ya hecha por dirección, para tu contexto — no la repitas, ejecútala si quieres confirmar pero no es el foco):
- data/INFRAESTRUCTURA-v1_0.md no lista "firmas-pendientes" ni "cruce-oferta-demanda" (grep -c da 0 en ambos). Dirección decide NO detenerse ahí: A.12 nombra forense/firmas-pendientes.tsv explícitamente (167 filas), y el cruce se gobierna por su "Regla de mantenimiento" en forense/notas/2026-08-25-cruce-oferta-demanda.md:335-339.
- Gobernantes reales: forense/notas/2026-08-25-cruce-oferta-demanda.md (el falsador y la regla de promoción), data/curacion-registro/cruce-oferta-demanda-v0_1.tsv (49 filas × 15 columnas), data/manifiesto.yaml (payloads ya descargados), forense/firmas-pendientes.tsv (A.12).
- El falsador "2026-09-08" / "catorce días" existe en UNA sola línea de forense/notas/2026-08-25-cruce-oferta-demanda.md (líneas ~321 y ~341), sin fila de tablero, sin ADR — confírmalo con: `grep -rIn --exclude-dir=.git --exclude-dir=raw -E "2026-09-08|catorce días" .` y reporta cuántos archivos de texto se examinaron.
- El cruce (TSV) y su corrección ya fueron consumidos por ADR-196 (R10.2→D) y ADR-208 (R2.1→D). Las 8 filas de la "palanca #1" tienen estado_fetch = VERIFICADO-REACTIVO y sus fuentes candidatas ya están en el manifiesto: banxico_encuesta_competencias_financieras_2024, adq15_ift_sfd_*, ENIF/ENDUTIH/ENCIG/ENAFIN/ENSAFI.

OBJETO: Tres derivaciones, CERO decisiones.
(a) Fijar el alcance exacto del falsador del 8/sep, declarado y no supuesto (lee el texto, no interpretes más allá de lo que dice).
(b) Contar contra él lo que el programa lanzó desde el 25/ago.
(c) Abrir byte a byte las 8 candidatas de la palanca #1 (disparador_sin_base:riesgo_fiscal_percibido) y decir, con vocabulario A.4 (EXISTE-SATISFACE / EXISTE-NO-SATISFACE con qué falta / NO-ENCONTRADO con dónde y con qué términos / NO-ACCESIBLE), si alguna alcanza EXISTE-SATISFACE.

NO HACES: no decides si el falsador se satisface/dispara/re-especifica (es la RANURA, de mesa), no promueves ninguna fila a acto medidor, no editas el TSV del cruce ni su nota, no lanzas ningún acto sucesor, no usas red/API/descargas nuevas, no adjudicas casilla/letra/tier.

PASOS:

0-bis (A.3): Commitea este encargo íntegro y verbatim en `forense/encargos/2026-08-26-MAESTRA31-E1-RELOJ-CRUCE.md` ANTES de abrir un solo payload. Al cerrar añade `## CONSUMIDO` con el número de PR (no lo dejes vacío — ese fue un defecto de un acto previo llamado E9).

1. Compuerta cero: confirma que PR #381 está fusionado en origin/main (usa `gh pr view 381` o `git log origin/main` — NUNCA el status de un worktree). Si no está fusionado, PARA todo el acto.

2. Alcance del falsador — declarado, no elegido. Lee COMPLETAS las secciones "## Cita de gobierno y falsador a catorce días" (líneas ~321-341) y "### Regla de mantenimiento" (líneas ~335-339) de forense/notas/2026-08-25-cruce-oferta-demanda.md. Determina por lectura literal del texto si "medición lanzada" está acotada a este cruce o es del programa entero. Si el texto no lo dice con claridad, DECLÁRALO AMBIGUO y no elijas.
   Declara también, con cita a la vista, si esta tensión se sostiene: la regla de mantenimiento exige EXISTE-SATISFACE para promover a un acto medidor, y el TSV tiene 0 de 49 en esa columna (7 EXISTE-NO-SATISFACE, 1 NO-ACCESIBLE, 41 NO-ENCONTRADO) — derívalo tú mismo con `awk` sobre la columna 8 del TSV, no confíes en el número dado aquí, verifícalo. Si se sostiene, el falsador no puede satisfacerse por la vía del propio cruce: es un defecto de clase B-bis (una escala sin fila para el desenlace que va a ocurrir).

3. Cuenta de mediciones lanzadas desde el 25/ago (A.13). Deriva por comando (pruébalo primero contra un caso donde conozcas la respuesta), pega el comando usado: ADRs con CONTADOR≠0, llaves de identificación ejercidas, fichas de Hito D archivadas — todo desde 2026-08-25. Reporta el conteo crudo BAJO LAS DOS LECTURAS del paso 2 (acotada al cruce / del programa entero), sin fusionarlas.

4. Censo de la palanca #1 — DOS COMMITS separados:
   - COMMIT-1: congela el protocolo ANTES de abrir un solo payload — lista las 8 candidatas con su instrumento_ola y que_le_falta (cópialos del TSV `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv`, filtra por la fila disparador_sin_base:riesgo_fiscal_percibido), los términos de búsqueda exactos que usarás, el control positivo, la escala de veredicto A.4, y qué pasa si ninguna satisface / si alguna sí (B-bis). Cierra con la frase verbatim: «El primer resultado que produzca este procedimiento es el que se reporta.»
   - COMMIT-2 (commit separado, no edites el primero): el resultado real de abrir cada una de las 8 candidatas byte a byte contra `data/raw/` (o donde estén los payloads ya descargados — verifica con el manifiesto), con veredicto A.4 para cada una, universo declarado (qué payload, qué archivos examinados, con qué mecanismo, en qué fecha, contra qué SHA).

5. Cierre:
   - Nota `forense/notas/2026-08-26-reloj-cruce-cierre.md` con los conteos A.13, la fila FP-169 (agrégala a forense/firmas-pendientes.tsv, SOLO esa fila — E2 en paralelo usa FP-170+), el ADR correspondiente (deriva el máximo con el comando exacto dado arriba, candidatea máximo+1, deja la nota de que quien fusione segundo debe renumerar), recifrado de §L0 de `estado` si aplica (canon/estado-programa-v1_10.md), censo del rótulo ACTO MAESTRA31-E1 en canon/registro-rotulos.tsv y en tests/check.py SOLO en `_T25_ARCHIVOS_CONOCIDOS` si T25 lo exige.
   - Deja la RANURA M-RELOJ VACÍA en tu nota de cierre — cópiala tal cual del encargo, sin llenarla, es de mesa.
   - Corre `python3 tests/check.py --baseline` y confirma VERDE (nunca uses `--freeze`).
   - Abre un PR con `gh pr create`.

PERÍMETRO — toca SOLO: forense/encargos/2026-08-26-MAESTRA31-E1-RELOJ-CRUCE.md (nuevo), forense/notas/2026-08-26-reloj-cruce-cierre.md (nuevo), forense/firmas-pendientes.tsv (solo fila FP-169), forense/hallazgos.md (una línea), canon/gobernanza-v1_15.md, canon/estado-programa-v1_10.md, canon/registro-rotulos.tsv, tests/check.py (solo _T25_ARCHIVOS_CONOCIDOS).
NO TOCA: el TSV del cruce ni su nota (los lees, no los editas), milpa/**, forense/hitoD-preregistro-v2_0.md, forense/prereg-duelo-v2/**, corridas-*, data/manifiesto.yaml.

PROHIBIDO: decidir si el falsador se satisface/dispara/re-especifica, promover cualquier fila a acto medidor, editar el TSV del cruce o su nota, lanzar el acto sucesor, usar red/API/descargar payload nuevo, adjudicar casilla/letra/tier, derivar cifra del espejo, escribir "no existe"/"no hay fuente" sin comando y universo al lado.

CONTADOR: 8 veredictos A.4 con universo declarado, derivados de payload ABIERTO (no de lectura de documento sobre el payload). Si el corpus no está montado, el acto PARA en el punto 4 del arranque, contador = 0 con la razón escrita.

## CONSUMIDO

PR #382 — `ACTO MAESTRA31-E1 · RELOJ-CRUCE`, 26/ago/2026.
