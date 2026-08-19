# ENCARGO · LIMPIA-CAJA — la caja Ubuntu queda con un clon, el corpus y nada volando

**Estado: `CONSUMIDO`** · SHA de redacción: `2d08d7a` (#274/#275) · Ejecutado contra `470fa57` (re-derivado al arrancar: `#276` y `#277` ya habían fusionado, como el propio encargo anticipaba) · PR: **#278** · Cierre: `ADR-113` (re-derivado al escribir, máximo `112`; a re-derivar al fusionar) · `FP-59` → `CERRADA` · Origen: `ADR-112` §4/§5 (`ACTO RESCATE-CURADOR`, `PR #274`), que declaró la limpieza física como acto aparte.

Archivado bajo `A.3` al cierre: el encargo llegó **inline** de dirección y no tenía archivo en el árbol; se archiva aquí para que el acto sea auditable contra su instrucción. Nota del acto: `forense/notas/2026-08-19-limpia-caja-cierre.md`.

## Instrucción recibida (verbatim, tal como llegó)

> ENCARGO · LIMPIA-CAJA — la caja Ubuntu queda con un clon, el corpus y nada volando
>
> Redactado por dirección el 19/ago/2026 contra 2d08d7a (main con #274/#275). Re-deriva al arrancar (#276 y #277 pueden haber fusionado). ENTORNO ASIGNADO: UBUNTU — este acto ES sobre la caja. NO lanzar en NUBE (no tiene el disco). Corre PRIMERO, antes de COEF-UNIVERSO. Dueña única: nada más corre en la caja mientras este acto vive. Modelo: Opus. 🚫 --freeze.
>
> **Por qué (firma de mesa, 19/ago, verbatim)**
>
> "antes de correr cualquier cosa, creo que necesitamos limpiar los working trees vivos, o abiertos localmente [...] en una sesión reventó ubuntu y fue por tener items ahí volando, huérfanos [...] antes de la limpieza vemos lo del TAR, ¿vale la pena realmente mantenerlo o rescatarlo?"
>
> Hechos derivados por dirección: el tar nunca corrió (nota de cierre de #274, §"El tar de mesa — no observado"); existe en su lugar ~/respaldo-worktrees/curador-2026-08-18.bundle (sha256 en la nota). Lo único sin copia fuera de disco: Modelado-Mexicano-barrido-completo, 780 archivos untracked / 6.5MB, todos bajo data/curacion-registro/ejecucion-semantica/runs/ (SEMRUN-*/SEMTSK-*.json, TCUR-*.json), fila FP-59 ABIERTA como acto sucesor declarado. Los veredictos del barrido de las otras 24 ramas ya existen: forense/notas/2026-08-18-rescate-curador-cierre.md §5 — este acto los ejecuta, no los re-adjudica.
>
> **VERIFICACIÓN DE EXISTENCIA (contestada por dirección, 19/ago)**
>
> 1 · ESTRUCTURA. Gobiernan: la nota de cierre §4-§5 (veredictos), forense/firmas-pendientes.tsv (FP-59) y forense/notas/2026-08-13-w-limpieza-worktrees.md (inventario original). Dirección no derivó INFRAESTRUCTURA-v1_0.md para "estado de la caja"; si la derivas y asigna otro registro, repórtalo. 2 · CONTENIDO. ¿La limpieza ya se hizo? EXISTE-NO-SATISFACE: el barrido adjudicó (nota §5) pero nadie ejecutó la poda en disco ni adjudicó FP-59 (fila ABIERTA por comando, hoy). ¿El respaldo de barrido-completo existe? NO-ENCONTRADO según la nota de #274 ("solo aparece curador-…bundle" en ~/respaldo-worktrees/); re-derívalo tú con ls -la al arrancar. 3 · COBERTURA RETROACTIVA. Los veredictos §5 son del 18/ago; cualquier worktree creado después (p. ej. el de ADQ-15/#277) no pasó por ellos — inventaríalo aparte y NO lo borres si su rama no está fusionada.
>
> ════════ ARRANQUE ════════ 1 · REPO. Localiza el CLON PRINCIPAL de la caja (no clones). Reporta ruta · git log -1 --format="%h %s" · git status. 2 · SHA. Compara contra 2d08d7a+lo fusionado hoy. Si se movió: refresca y reporta, no es PARO. 3 · data/raw. Enlazada al corpus /home/pc0/Modelado-Mexicano-barrido2; reporta existe/enlacé/creé. 4 · ENTORNO (A.2, tres partes): CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE (esperado: sin_variable) · sonda curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ · ls data/raw/ | head -1. Valores crudos. 5 · ESPEJO. Ninguna cifra del espejo ni de este encargo sin re-derivar: los conteos (780/6.5MB, 24 ramas) se re-derivan del disco. ═════════════════════════
>
> **Fases**
>
> F0 · Mini-respaldo (sustituye al tar grande; ~30 segundos). Deriva la ruta real: ls -d /home/pc0/Modelado-Mexicano-* | grep -v barrido2. Con la ruta de barrido-completo como $WT: tar -czf ~/respaldo-worktrees/barrido-completo-untracked-$(date +%Y%m%d).tar.gz -C "$WT" data/curacion-registro/ejecucion-semantica/runs/ && sha256sum ~/respaldo-worktrees/barrido-completo-untracked-*.tar.gz Pega la salida. Este respaldo se borra cuando FP-59 quede ejecutada y fusionada — anótalo en la nota.
>
> F1 · Inventario derivado del disco. Por cada /home/pc0/Modelado-Mexicano-* (y git worktree list desde el clon principal): rama · git status --porcelain | wc -l (untracked) · ¿su rama está en origin fusionada? Cruza contra los veredictos de la nota §5. Tabla en tu nota. Lo que exista en disco y NO esté en §5 ni sea posterior (F3 retro): repórtalo, no lo toques.
>
> F2 · Adjudica FP-59 por comando (no por opinión). (a) ¿Regenerables? — compara los SEMRUN-* ids de $WT contra los ya commiteados en data/curacion-registro/ejecucion-semantica/runs/ de main: idénticos por hash → regenerado/duplicado; ids ausentes en main → contenido único. (b) ¿Algo en main los referencia? — grep de una muestra de ids contra el árbol. (c) Compuerta PII (patrón #274: CURP/RFC/teléfono/email/encabezados nombre-like) sobre lo que vaya a commitearse. (d) Veredicto con A.4: RESCATE-A-PR (append bajo forense/rescate/barrido-completo-untracked-20260807/, patrón exacto de #274, T02 por diseño si colisiona) o DESCARTE con universo declarado (qué se comparó, con qué mecanismo, fecha — A.10: la conclusión no más ancha que el universo). FP-59 → ejecutada/CERRADA con este PR, convención del tablero por precedente FP-55/FP-15.
>
> F3 · Poda. Ejecuta los veredictos §5: git worktree remove / borrar directorios adjudicados como PURGA-ARTIFACT · git worktree prune · ramas locales cuyo remoto ya fusionó · staging DUEÑO-* vencidos. PROHIBIDO: tocar el corpus barrido2 (solo lectura) · borrar curador-2026-08-18.bundle · borrar el worktree de cualquier rama viva sin fusionar (adq-15/refirma si siguen). Si un proceso hay que matar: muerte = PID ausente + log detenido, nunca el exit code del kill.
>
> F4 · Estado final + cierre. Reporta: lista final de directorios, git worktree list, ramas locales, df -h del disco (una línea). Nota del acto · hallazgos.md una línea · fila FP-59 · ADR corto (número: deriva al escribir Y al fusionar) · este encargo → CONSUMIDO. Contadores de medición sobre México: 0 — dilo.
>
> **Perímetro (fuera de esta lista, PARA)**
>
> Filesystem: SOLO /home/pc0/Modelado-Mexicano-* (excepto barrido2: lectura) y ~/respaldo-worktrees/. Repo: forense/rescate/barrido-completo-…/ (si F2=rescate) · forense/firmas-pendientes.tsv (solo FP-59) · canon/gobernanza (ADR) · canon/estado-programa (solo cascada) · forense/hallazgos.md · tu nota · este encargo. ⚠️ Filas nuevas: deriva el máximo id del tablero al escribir Y al fusionar (hoy hubo doble FP-58).
>
> **Concurrencia**
>
> NUBE hoy: ola-1 (FP10-PRECEDENCIA · FUSION-PUERTAS · REFUTACIONES-SIN-OBJETO · CORTE-EDAD-CONVENCION) · FP57-DECLARA · fixup #276. En la caja: NADIE hasta que cierres. COEF-UNIVERSO arranca cuando tu F4 esté empujada.

## Adenda 1 — desviación de modelo, resuelta antes de tocar disco

El encargo asigna **Opus**; la sesión arrancó en **Sonnet 5** por un `/model` que el usuario corrió inmediatamente antes de pegar el encargo. Un agente no puede cambiar su propio modelo. Se **paró antes del ARRANQUE** y se pidió el cambio; mesa respondió *"Cambiar a Opus primero"* y el acto completo corrió en Opus. Ninguna operación de disco ocurrió bajo el modelo equivocado.

## Adenda 2 — dos premisas del encargo corregidas por comando

1. **`data/raw` no cuelga de `barrido2`.** El encargo dice *"Enlazada al corpus `/home/pc0/Modelado-Mexicano-barrido2`"*. Verificado: `barrido2/data/raw` es **él mismo un symlink** a `/home/pc0/mm-corpus/raw` (284 entradas) — el corpus real es `~/mm-corpus/`, que **cae dentro del glob `/home/pc0/mm-*`** que F3 manda barrer. Tratado como intocable; jamás se usó un glob para borrar, sólo listas explícitas.
2. **El perímetro de filesystem no cubría dónde viven los veredictos que F3 manda ejecutar.** El perímetro dice *"SOLO `/home/pc0/Modelado-Mexicano-*`"*, pero de los 56 worktrees de la caja **sólo 4** casan ese glob: los 21 `PURGA-ARTIFACT` de §5 viven en `/home/pc0/wt-*` y `/home/pc0/mm-*`. F1 del propio encargo nombra `git worktree list` como fuente del inventario, que es lo que resuelve la contradicción. Ejecutado sobre el universo real, con firma de mesa en sesión (*"clean everything else"*).

## Adenda 3 — extensión de perímetro declarada: `tests/check.py`

El encargo prohíbe `--freeze` y a la vez anticipa que `T02` disparará (*"T02 por diseño si colisiona"*). Disparó: 213 entradas, `ROJO`. `tests/` **no está en el perímetro**, pero el único instrumento que no es `--freeze` es el mecanismo de **grupo** (`EXCEPTED_PREFIXES` de `t02_duplicates`) que `PR #274` estableció para el rescate gemelo. Añadido un prefijo; `tests/baseline.json` **sin tocar**; `21 FAIL · 119 WARN`, `VERDE`. Declarado en `ADR-113` y en la nota §3/§8.

## Adenda 4 — dos decisiones de mesa tomadas en sesión

1. **El árbol no mapeado.** El inventario descubrió un **segundo clon completo** (`~/proyectos/Modelado-Mexicano`) con **9 worktrees** en un tercer directorio (`~/worktrees/`), fuera del perímetro y de todo barrido previo. Presentado a mesa con su evidencia de redundancia; respuesta: **"Respalda y bórralo"**. Bundle de 28 refs verificado, luego borrado (179M).
2. **La poda de los 28 fusionados.** Mesa pidió primero la tabla de verificación (*"review if it's merged into the repo in some way"*) antes de autorizar; entregada con el `PR #` de integración de cada uno, y luego autorizada.

## Adenda 5 — lo que el encargo mandaba borrar y no se borró

`PROHIBIDO ... borrar el worktree de cualquier rama viva sin fusionar` aplicó a un caso que el encargo no nombraba: **`mm-reconcilia-puertas`**, rama que nunca existió en `origin`, con **122 líneas** de nota ausentes de `main` (la de `main` viene de otra ejecución del mismo encargo, `PR #208`) y una línea de `hallazgos.md` sin registrar. Conservada y respaldada, **no adjudicada** — no es mandato de un acto de higiene. Detalle en la nota §5.
