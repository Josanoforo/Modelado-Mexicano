- **SHA de redacción:** `dcc4f6a` (`origin/main` — confirmado contra el clon en esta sesión: es el HEAD exacto sobre el que se abrió el worktree de este acto, `git worktree add /home/pc0/mm-capa3-reconcilia -b capa3-reconcilia origin/main`).
- **Entorno asignado:** CAJA con corpus (exige `data/raices.local.yaml` con `descargas_mx`, gitignorado, no heredado por worktree). **NO** en nube — no tiene los bytes. Ejecutado en esta ocasión en Ubuntu/WSL, worktree `~/mm-capa3-reconcilia`, con `data/raices.local.yaml` y el symlink `data/raw` recreados a mano (ninguno de los dos viaja con `git worktree add` — ver `forense/notas/2026-08-13-capa3-reconcilia.md` §1).
- **Estado:** CONSUMIDO — PR #202 (rama `capa3-reconcilia`). *(Re-verificado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS, contra `f3873c2`: `git merge-base --is-ancestor e993752 f3873c2` OK.)*

---

Texto completo del encargo, tal como se lanzó (verbatim):

---

ENCARGO C · CAPA3-RECONCILIA — las 19 filas que ENLACE-1 dejó a medias
SHA de redacción: dcc4f6a. Entorno: CAJA con corpus. Exige data/raices.local.yaml con descargas_mx. NO en nube (no tiene los bytes).
Será el tercer commit en la historia de relaciones.tsv.

§0 · Por qué — derivado hoy, nadie lo ha reportado

Antes de #196, capa2_manifiesto y capa3_disco_real coincidían en las 197 filas. Después:

capa2=SI · capa3=EXISTE;COINCIDE;INTEGRO  →  24   (las de antes)
capa2=SI · capa3=NO_REFERENCIADO          →  19   ← ISSP 12 · CSES 5 · WVS 2

ENLACE-1 movió una columna y dejó la de al lado atrás. Es el mismo defecto de conducto, una estación más abajo, y lo detectó de paso la sesión de APERTURA-ISSP.

Y es mecánico, no de juicio: capa3 es lo que tests/manifiesto.py --verifica --id <X> responde. ACTO R″ ya reportó 16/16 COINCIDE para ISSP. Este acto no decide nada: deriva y escribe.

§1 · PERÍMETRO

ESCRIBE: data/curacion-registro/relaciones.tsv (SOLO la columna capa3_disco_real, SOLO en filas con capa2=SI) · forense/notas/2026-08-13-capa3-reconcilia.md · hallazgos · encargos (A.3).

NO ESCRIBE: ninguna otra columna de relaciones.tsv —ni capa2, ni capa4, ni id_manifiesto, ni nota— · data/manifiesto.yaml · canon/** · tools/** · tests/**.

⚠️ relaciones.tsv es de un solo escritor y hoy está libre. Verifica antes de empezar: git log --oneline -3 -- data/curacion-registro/relaciones.tsv y git branch -r. Si aparece una rama viva tocándolo, PARA.

⚠️ APERTURA-ISSP corre en la misma caja y su perímetro le prohíbe este archivo — no colisiona. Pero si su nota propone veredictos de capa4 para estas mismas filas, NO los escribas aquí. Este acto es de una columna.

§2 · ARRANQUE

Los cinco puntos, con el 3 crítico y distinto:

3 · CORPUS. Los payloads de ISSP están en raiz: descargas_mx, no en data/raw, y data/raices.local.yaml es gitignorado — no se hereda al crear worktree. Cópialo. Verifica y reporta crudo:

bash
test -f data/raices.local.yaml && grep -c "descargas_mx" data/raices.local.yaml
python3 tests/manifiesto.py --verifica --id za6980_v2_0_0_dta      # esperado COINCIDE
python3 tests/manifiesto.py --verifica --id cses5_modulo5_2016_2021_csv

Si no dan COINCIDE: PARA — entorno equivocado. Este acto no puede escribir capa3 sin verificar disco.

§3 · COMMIT 1 — la especificación, congelada antes de abrir el TSV
Las 19 filas, derivadas en sesión (no de este encargo): awk sobre relaciones.tsv para capa2==SI && capa3!="EXISTE;COINCIDE;INTEGRO". Reporta relacion_id, necesidad_id, fuente, id_manifiesto.
El valor a escribir se deriva de --verifica, una invocación por id, con la salida cruda pegada. Las tres respuestas no se colapsan: COINCIDE → EXISTE;COINCIDE;INTEGRO · AUSENTE → PARA y reporta (significa que capa2=SI está mal, y eso es un hallazgo mayor que este acto) · hash discordante → PARA.
El vocabulario de capa3 se lee de las 24 filas que ya lo tienen, verbatim. No se inventa una variante.
Mecanismo de escritura: split/join por \t, NUNCA csv.writer. El 13/ago csv.writer re-citó comillas y corrompió 7 filas ajenas de universo-puertas; se detectó con git diff antes de commitear. Verifica con git diff --unified=0 que el diff toque exactamente 19 líneas y solo un campo por línea.

Frase de cierre de siempre.

§4 · COMMIT 2

Escritura + git diff --unified=0 pegado + la distribución capa2×capa3 antes y después + python3 tools/curador_registro/via_capa2.py (debe seguir en 0 diffs — este acto no toca capa2) + suite --baseline VERDE contra 948ad70.

Contador: filas con capa2 y capa3 en desacuerdo: 19 → 0. Y si alguna vuelve AUSENTE, ese número es el titular y este acto se convierte en un reporte, no en una escritura.

§5 · NO HACE

No toca capa4 (es de APERTURA-ISSP y su propagación). No toca capa2 (ya está bien). No enlaza ninguna fila nueva (eso es ENLACE-2). No abre ningún payload — solo verifica hash.

LO QUE NO SE PUEDE LANZAR TODAVÍA, y por qué
acto    bloqueo
P·LOTE-2    PR #197 sin fusionar. SONDA-1 entregó la firma reordenada por evidencia —6 fuentes agente-ejecutables, un carril usuario+navegador, GDELT/UCDP como decisión de ingeniería previa. Esa firma es de mesa. Lanzarlo antes es volver a apostar por palanca a ciegas.
ENLACE-2    Espera a APERTURA-ISSP para absorber sus veredictos de capa4 en una sola pasada sobre relaciones.tsv, en vez de dos. Y su alcance (78 hoy) mejora con el ENCARGO B.
APERTURA-ISSP fase 2 / los 7 veredictos D    Entrada 3 del registro; gate: entradas 1 y 2.
ADJ-3    Tres firmas de mesa, no de ejecutor.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-13-encargo-c-capa3-reconcilia.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-13-capa3-reconcilia.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
