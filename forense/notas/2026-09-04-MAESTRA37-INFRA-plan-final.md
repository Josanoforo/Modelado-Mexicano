# Nota de procedencia (añadida al incorporar este documento al repo, 4/sep/2026)

Este documento vivió como plan de ejecución **externo al repo** durante
INFRA-1/INFRA-2 — así lo cita `forense/hallazgos.md` en su entrada del
3/sep/2026 sobre `MAESTRA37-INFRA-2` ("el documento de planificación
PLAN-MAESTRA37-INFRA-1-2 (externo al repo)"). Gobernó, en este orden:

1. El encargo original de planificación `MAESTRA37-INFRA` (SSOT, manifiesto,
   alta atómica, capa física, portabilidad).
2. Una ADENDA OBLIGATORIA de 20 enmiendas (secciones A-FP259, marcadas
   `[ADENDA]` abajo) — upsert idempotente en vez de append-only, lock de
   alcance completo en `tests/manifiesto.py`, `alta_relacion.py` sin
   invocar `via_capa2.py` y sin excepción de fusión, raíz lógica
   per-entrada en `semantic_run.py`, distinción por raíz en FP-259.
3. Un AJUSTE DE DIRECCIÓN posterior, solo sobre LIBRO 2 (marcado
   `[AJUSTE DE DIRECCIÓN]` abajo) — reduce INFRA-2 a dos commits, exige
   medir antes de decidir si `--vincula` hace falta, exige sincronizar
   `baseline.json`/derivados si Frente D escribe, corrige el manejo de
   raíz no configurada en `semantic_run.py`.

Los tres PR ya fusionados que ejecutaron este plan: **PR #521**
(`claude/maestra37-infra-1-ssot-manifiesto-alta`, INFRA-1 completo, 3
commits A/B/C), **PR #522** (`claude/maestra37-infra-2-capa2-portabilidad`,
Frente E + PARO de Frente D por falta aparente de corpus) y **PR #525**
(`claude/maestra37-infra-2-frente-d`, corrige el PARO — era un falso
positivo de `git worktree add` sin symlinks/gitignorados — y ejecuta
Frente D + FP-259). Ver
`forense/notas/2026-09-04-MAESTRA37-INFRA-verificacion-post-hoc.md` para la
auditoría adversarial de los 5 commits de ejecución contra este documento.

Se incorpora aquí VERBATIM (sin editar el cuerpo por debajo de esta nota)
como registro del documento que efectivamente gobernó la ejecución.

---

# PLAN-MAESTRA37-INFRA-1-2

Sesión de **planificación pura** (sin implementar, sin commits, sin PR).
Repositorio `Josanoforo/Modelado-Mexicano`. Ejecutor previsto de LIBRO 1 y
LIBRO 2: **Claude Code CLI** (el encargo original dice "Codex CLI"; en este
proyecto el CLI que ejecuta es Claude Code — misma mecánica: worktree, rama,
commits, PR abierto sin fusionar, gobernada por `AGENTS.md`).

> **ADENDA OBLIGATORIA APLICADA** (20 enmiendas, secciones A-FP259). En caso
> de contradicción entre el cuerpo original de este documento y una tabla
> marcada `[ADENDA]` abajo, la tabla `[ADENDA]` manda. El cuerpo no
> reescrito permanece vigente tal cual.

Metodología de esta sesión: inspección directa de código (SHAs, líneas,
conteos reales) más 6 investigaciones paralelas de solo lectura, una por
frente (A-E) más FP-259, cada una citando archivo:línea. Todas las cifras de
este documento están re-derivadas hoy, no heredadas del encargo.

---

## 0 · Estado observado en `origin/main`

- `origin/main` al momento de planificar: **`2e79d153a48d6d8d4ccd9b732e018ab2ce770861`**.
- Referencia de redacción del encargo: `27647ac4bde942d766aad96a77f087a99deff2a`
  ("Merge pull request #518 ... MAESTRA37-A1").
- `main` avanzó **8 commits** desde la referencia (PR #519 MAESTRA37-N6
  censo-diario-de-raíz, PR #520 MAESTRA37-L3-BIS salud-A4). De esos 8, solo
  dos tocan rutas de este encargo:
  - `tools/curador_registro/GUIA-CURADOR-REGISTRO.md` (+13 líneas): documenta
    `DEPOSITADO-SIN-REGISTRO` como estado válido de `estado_A4A5` — explícitamente
    "vocabulario de cola, no de curación automática", "sin test propio",
    "`via_capa2.py` no lee este token". Confirmado por Frente A: 0/112 filas
    reales lo usan hoy y ningún script tiene un enum cerrado que se rompa con
    él. **No requiere ningún cambio de código en INFRA-1/2.**
  - `tools/adquiere_cron.sh` (nuevo): cron de mesa que ya invoca `resolver_raiz()`
    y `tests/manifiesto.py --escanea`; no escribe cola ni registro directamente.
    Contiene un comentario (línea 73) que afirma que `data/manifiesto-staging.yaml`
    "ya está en .gitignore" — **falso**, ver hallazgo B-4 abajo.
  - El resto (L3-BIS salud, notas forenses) es no material para este encargo.
- **Ninguna decisión cerrada de este encargo fue reabierta por el avance de `main`.**
- **LIBRO 1 debe re-fetchear y re-derivar el SHA otra vez al arrancar** — puede
  haber avanzado más desde esta sesión de planificación.

---

## 1 · Desviaciones materiales respecto al encargo (rederivadas, citadas)

### 1.1 Cifras de referencia que NO coinciden con el estado real

| Cifra del encargo | Valor real hoy | Fuente / comando |
|---|---|---|
| "219 relaciones" | **219** (coincide) | `tail -n +2 data/curacion-registro/relaciones.tsv \| wc -l` |
| "165 `NO_DETERMINADO`" | **137**, no 165 | columna `id_manifiesto`; ver Frente D — "165" no aparece en `forense/` ni en el historial git de `relaciones.tsv` (5 commits revisados); no tiene fuente localizable |
| "86 = 77 + 9" (FP-259) | **no reproducible en este entorno**; ya re-derivado una vez a "73, no 77" por un método distinto (censo por disco, no `tests/corpus.py`) el mismo 3/sep/2026 | `forense/firmas-pendientes.tsv` fila FP-259; `forense/notas/2026-09-03-MAESTRA37-L1-censo.md:19` |
| "IDs explícitos que no resuelven = 0" (implícito, criterio de éxito #9) | **YA es 0 hoy** (193 ids citados en 82 filas, los 193 resuelven contra `data/manifiesto.yaml`, 1233 entradas) | Frente D, verificado con `csv.DictReader` + `yaml.safe_load` cruzados |

**Corrección propia de esta sesión:** en una verificación inline previa a lanzar
la investigación paralela, esta sesión calculó erróneamente "0 candidatos de
enlace por SHA" comparando el valor placeholder `"NO_DETERMINADO"` de la
columna `sha256_fuente` como si fuera un hash real. Frente D corrigió esto:
`sha256_fuente` **no se usa en ningún lugar de `via_capa2.py`** y hoy coincide
1:1 con las filas que ya tienen `id_manifiesto` explícito (0 filas con SHA real
sin id). El indicador estructural correcto de "candidatos de enlace físico"
medible sin corpus es el diagnóstico por nombre/alias de `via_capa2.py`
(**98 filas** hoy), no un cruce por SHA.

### 1.2 Defectos materiales confirmados por lectura de código (no en el encargo original, pero exactamente lo que anticipa)

1. **`tools/arbitra.py::encola_no_obtenido()` (líneas 83-91)** escribe con
   `open(COLA, "a")` **directo sobre la VISTA** (`data/cola-adquisicion-v1_0.tsv`)
   una fila de **4 columnas** que no coincide con las 7 que la vista declara.
   Esto **ya estaba declarado y dejado sin resolver** por `ACTO MAESTRA33-A5`:
   `canon/gobernanza-v1_15.md:4646` dice textualmente que es "riesgo para un
   acto sucesor" — MAESTRA37-INFRA es ese acto sucesor.
2. **`.claude/commands/arbitra.md:50-51`** instruye activamente comitear el
   resultado de ese defecto ("las filas nuevas en `data/cola-adquisicion-v1_0.tsv`").
   Hay que corregir el texto junto con el código.
3. **`tools/curador_registro/registra_cola_adquisicion.py`** es el "migrador
   legacy": por defecto lee la VISTA y **trunca el SSOT** (`csv.DictWriter`
   modo `"w"`), con defaults apuntando a los archivos de producción reales y
   **sin ninguna bandera de confirmación**.
4. **`tsv_crudo.py` no tiene escritor estructurado** — solo lectura
   (`leer_dicts`) y round-trip opaco (`leer_lineas`/`escribir_lineas`). Falta
   la mitad de "escritor canónico".
5. **`.claude/commands/adquiere.md` YA cumple la arquitectura correcta**
   (verificado línea por línea: 14-21, 170-177, 186-189, 203-208) — **no se
   toca**, confirmando la instrucción del encargo.
6. **`escribir_manifiesto()` (`tests/manifiesto.py:247-252`) no valida
   esquema ni escribe atómicamente** — `open(path,"w")` directo, sin
   temporal/fsync/`os.replace`. Confirmado también por el propio repo el mismo
   día: `forense/hallazgos.md:671`.
7. **`data/manifiesto-staging.yaml` SÍ está trackeado en git** (3 commits de
   historia) pese a que `tools/adquiere_cron.sh:73` afirma en un comentario
   que está en `.gitignore` — no lo está. Su escritura (`cmd_escanea`,
   `_reescribir_staging_restante`) tampoco es atómica.
8. **Ya existe en el repo el patrón exacto** que el encargo pide para
   manifiesto y para la alta de relaciones: `tools/curador_registro/
   integrate_barrido2.py::_replace_with_rollback` (367-393) + lock
   `fcntl.flock` (474-483), y `sync_bootstrap.py::_atomic_replace_many`
   (127-150) + `_freeze_manifest` (59-86, literalmente "recifrar baseline.json").
   **No hay que inventar arquitectura nueva.**
9. **No existe ningún script de alta de relación** (`grep` de `alta_relacion`
   vacío en todo el repo); la propia guía lo declara: `GUIA-CURADOR-REGISTRO.md:41`,
   "esta sección no inventa uno". El costo del procedimiento manual es real,
   no hipotético: `data/curacion-registro/baseline.json:64` narra que
   `ACTO MAESTRA37-A1` tuvo que recifrar **dos veces en el mismo acto**
   (commit `27efeb1`) porque una corrección de `capa3_disco_real` invalidó
   los sha256 recién calculados y disparó un FAIL nuevo del check **T21** de
   `tests/check.py` (líneas 2044-2093) — un check que la guía **no menciona**
   como paso obligatorio de la alta.
10. **`via_capa2.py` no tiene ninguna bandera de cierre/promueve/vincula** —
    solo `--root` y `--escribe`, y `--escribe` nunca asigna un `id_manifiesto`
    nuevo. La asignación es hoy edición manual directa del TSV.
11. **`tests/corpus.py::c1_huerfanos()` (líneas 90-136) compara por RUTA
    RELATIVA, nunca por contenido (sha256)** — cero llamadas a `M.sha256_de`
    en todo el archivo. Confirma exactamente el defecto que describe FP-259.
12. **`tools/curador_registro/semantic_run.py:457`** es el único GENERADOR
    real de rutas absolutas de una sola máquina entre los 8 archivos
    señalados: `corpus = Path("/home/pc0/mm-corpus/raw")` se serializa, sin
    transformar, en tres artefactos JSON por tarea. Verificado con un
    artefacto YA COMMITEADO que contiene literalmente
    `"ruta":"/home/pc0/mm-corpus/raw/enbiare2021/enbiare_2021_fd.pdf"`.
    Los otros 7 archivos **no son generadores** (5 ENOE de un acto ya cerrado
    con PR propio que solo serializan basename/URL; 1 comentario inerte de
    sellado sha256; y `correr-olas-v7.py`, que **debe quedar explícitamente
    excluido** de cualquier edición — su sha256 es la prueba de cadena de
    custodia de una corrida real ya archivada, `forense/notas/2026-08-18-b2-v7.md:48-83`).
13. **El formato `<raíz_lógica>:<ruta_relativa>` ya existe en producción** —
    `tools/curador_registro/snapshot_universe.py` lo construye inline
    (`f"data_raw:{ruta}"`, líneas 183/208/295) y ya vive commiteado en
    `data/curacion-universo/declaraciones-activos-t0.tsv`. No hay que inventar
    convención.

### 1.3 Confirmaciones de entorno

- `python3 tests/check.py --baseline` está **VERDE hoy** (19 FAIL / 171 WARN,
  todos en `tests/baseline.json`). Este es el "antes" que ambos PR deben
  preservar.
- `data/raw` y `data/raices.local.yaml` **están ausentes** en cualquier sesión
  de nube/planificación (gitignorados, específicos de máquina) — confirma que
  INFRA-2 no puede ejecutarse ni verificarse fuera de la máquina Ubuntu con
  corpus.
- Hallazgo lateral no material (una línea): `data/curacion-registro/baseline.json`
  (baseline propio del curador, 67 líneas) es un archivo **distinto** de
  `tests/baseline.json` (baseline global de `tests/check.py --baseline`). Este
  plan siempre nombra la ruta completa.

---

## 2 · Supuestos que Claude Code CLI debe RE-DERIVAR, no heredar de este documento

1. **El SHA de `origin/main`** — este plan usa `2e79d153a4...`; LIBRO 1 debe
   re-fetchear y confirmar cuál es el SHA real al arrancar.
2. **Las 18 claves top-level de `data/manifiesto.yaml`** (§Commit B1) —
   medidas hoy sobre 1233 entradas. Si `main` avanzó y agregó una clave
   legítima nueva antes de que arranque LIBRO 1, re-derivar el censo con el
   mismo método (cargar YAML, `Counter` de claves) contra el manifiesto real,
   no confiar en la lista de este documento.
3. **Las 5 entradas sin `sha256`** y sus dos estructuras (documental pura vs.
   "retirada") — re-confirmar líneas/IDs si el manifiesto cambió.
4. **Los conteos de Frente D** (219 relaciones, 82 con id explícito, 137
   `NO_DETERMINADO`, 98 candidatos de diagnóstico, 0 IDs colgantes) — válidos
   en el commit `29c2c6f`/HEAD `2e79d15`. Re-derivar con los comandos citados
   antes de escribir el "antes" de INFRA-2.
5. **Las métricas de capa física reales** (COINCIDE/NO_COINCIDE/AUSENTE/
   RAIZ_NO_CONFIGURADA) — **no medidas en esta sesión** (sin corpus). La
   "medición previa a D" de LIBRO 2 (§ INFRA-2, antes de COMMIT 1) es
   exactamente la re-derivación obligatoria — no es un commit aparte.
6. **La cifra final de FP-259** ("presente bajo otra raíz" vs "sin registro")
   — ningún número de este documento (86/77/9, 73) debe copiarse como
   resultado; solo lo confirma correr `tests/corpus.py` ya corregido contra
   el corpus real.
7. **Que el PR de INFRA-1 esté realmente fusionado** antes de arrancar
   INFRA-2 (compuerta explícita, no asumir por fecha).
8. **Que `data/raices.local.yaml` en la máquina de INFRA-2 declare las
   raíces reales** (al menos `descargas_mx`) — confirmar con `cat`, no asumir.
9. **Si el conjunto de banderas CLI de `tests/manifiesto.py`
   (`--registra/--escanea/--promueve/--verifica/--compara`) cambió de nombre**
   entre esta planificación y la ejecución — confirmar con
   `python3 tests/manifiesto.py --help` antes de tocar `escribir_manifiesto`.
10. **Que ningún otro commit entre esta planificación y la ejecución haya
    tocado `tools/arbitra.py`, `tests/manifiesto.py`,
    `tools/curador_registro/{baseline,via_capa2,integrate_barrido2,
    sync_bootstrap}.py` o `tests/corpus.py`** — si sí, releer esas líneas
    antes de aplicar los pasos de este plan tal cual.

---

## LIBRO 1 · Claude Code CLI · INFRA-1 (SSOT-MANIFIESTO-ALTA)

### Compuerta de arranque

```bash
git fetch origin main
git log --oneline -1 origin/main          # confirma SHA real, no asumir 2e79d15...
git worktree add ../mm-infra1 origin/main  # o clon fresco; NUNCA reusar un worktree con cambios previos
cd ../mm-infra1
git checkout -b claude/maestra37-infra-1-ssot-manifiesto-alta
git status --short                         # debe estar vacío
python3 tests/check.py --baseline 2>&1 | tail -5   # DEBE decir "LÍNEA BASE: VERDE"
```

**PARO material si `tests/check.py --baseline` no está VERDE al arrancar**:
repórtalo tal cual, no continúes asumiendo que el rojo es previo — confirma
primero si es un FAIL ya conocido en `tests/baseline.json` (compara la lista)
o una regresión real introducida entre esta planificación y el arranque.

Archivos a **leer completos antes de editar** (no resumir de memoria):
`tools/arbitra.py`, `tools/curador_registro/tsv_crudo.py`,
`tools/curador_registro/registra_cola_adquisicion.py`,
`tools/vista_cola_adquisicion.py`, `.claude/commands/arbitra.md`,
`.claude/commands/adquiere.md` (solo para confirmar que no se toca),
`tests/manifiesto.py`, `data/manifiesto.yaml` (las 5 entradas sin sha256:
líneas ~71, 84, 417, 2819, 6646 — confirmar que siguen ahí),
`tools/curador_registro/integrate_barrido2.py` (líneas 367-393, 474-483),
`tools/curador_registro/sync_bootstrap.py` (líneas 59-86, 127-150),
`tools/curador_registro/baseline.py`, `tools/curador_registro/GUIA-CURADOR-REGISTRO.md`,
`data/curacion-registro/{relaciones,evidencias,utilidad-modelo}.tsv` (cabeceras),
`data/curacion-registro/baseline.json`.

---

### COMMIT A — Frente A · SSOT de adquisición `[ADENDA]`

**Enmiendas aplicadas: A.1-A.4 de la adenda.** El writer NO es append-only:
es **upsert idempotente** keyed por `fila_origen`, preservando byte a byte
toda fila no afectada. `arbitra.py` nunca escribe `NO-OBTENIDO` (token
inexistente en el vocabulario real de `estado_A4A5` — los valores reales
observados son `OBTENIDO`, `PENDIENTE`, `NO-ACCESIBLE`,
`NO-OBTENIDO-POR-ESTE-AGENTE(N intentos)`, `OBTENIDO-PARCIAL`, etc.);
escribe `PENDIENTE`, porque detectar ausencia de payload no es un intento
de adquisición. La bandera de `registra_cola_adquisicion.py` es
incondicional: se exige **antes de cualquier escritura**, no solo cuando el
destino ya tiene filas.

| Paso | Archivo | Cambio | Invariante protegida | Comando de prueba | Salida esperada | Continuar / Detenerse |
|---|---|---|---|---|---|---|
| A1 | `tools/curador_registro/tsv_crudo.py` | Agregar función de escritura estructurada `upsert_fila(path, fila: dict, campos: list[str], clave: str = "fila_origen")`: valida ausencia de `\t`/`\n` literal en cada valor (raise si hay); busca en las líneas existentes una fila cuyo campo `clave` coincida con `fila[clave]` — si existe, **reemplaza esa línea in-place** (mismo índice, resto de líneas byte a byte intactas); si no existe, **anexa** una línea nueva al final. Construye la línea con `"\t".join`. Usa `leer_lineas`+`escribir_lineas` internamente para preservar el resto byte a byte. | Idempotencia: llamar dos veces con la misma `fila` dos veces produce el mismo archivo (byte a byte) que llamarla una vez. Ninguna fila **no afectada** por la clave se re-serializa nunca (mismo criterio que **T26-bis**, `tests/check.py:3910-3968`). | Sobre una **copia temporal** del registro real: (a) `upsert_fila` con una clave nueva → `diff` muestra +1 línea; (b) `upsert_fila` de nuevo con la MISMA clave y datos distintos → `diff` contra (a) muestra exactamente 1 línea modificada, cero adicionales; (c) repetir (b) con los mismos datos → `diff` vacío contra (b). | (a) +1 línea. (b) 1 línea modificada, mismo total de líneas. (c) diff vacío (idempotente). | Continuar si las 3 corridas dan el resultado exacto. **Detenerse** si algún valor de producción contiene `\t`/`\n` real: no inventar un escape silencioso — es una decisión de mesa (tsv_crudo es "texto opaco sin interpretar comillas" por diseño). |
| A2 | `tools/arbitra.py` función `encola_no_obtenido()` (líneas 83-91) | Reemplazar `open(COLA, "a")` por: (1) `fila_origen = f"arbitra.py:{id_celda}"`; (2) normalizar `fuente_canonica` (el nombre de la encuesta) contra el alias index vigente — **reusar `build_alias_index()` de `registra_cola_adquisicion.py`** sobre `data/curacion-registro/aliases-fuentes.tsv`, no reimplementar; (3) si hay alias → `fuente_canonica_normalizada = alias_index[...]`, `discordancia_alias = ""`; si no hay alias → `fuente_canonica_normalizada = fuente_canonica`, `discordancia_alias = "SIN_ALIAS"`; (4) `estado_A4A5 = "PENDIENTE"` (**nunca** `"NO-OBTENIDO"` — no es un token del vocabulario real); resto de columnas (`prioridad=""`, `url_conocida=""`, `ids_manifiesto=""`, `origen="arbitra.py"`, `nota=<mensaje actual>`). Llamar `tsv_crudo.upsert_fila()` sobre `data/curacion-registro/cola-adquisicion-registro.tsv` con `clave="fila_origen"` — una celda que `arbitra.py` re-procese actualiza su propia fila, no la duplica. Al final de `main()`, si se hizo al menos un upsert, invocar `tools/vista_cola_adquisicion.py` para regenerar la vista. **Confirmar la cabecera real de 10 columnas leyendo el archivo antes de mapear.** | La vista nunca recibe escritura fuera de `vista_cola_adquisicion.py`. Reprocesar la misma celda dos veces actualiza 1 fila, nunca duplica. | Sobre un **marco de prueba desechable** (fixture) con un id sin payload, corrido **dos veces seguidas**: `python3 tools/arbitra.py <marco-fixture.tsv> <col> <id-sin-payload>` (×2) en un `tempfile.TemporaryDirectory` con copias de los datos. | Tras la 2ª corrida, el registro tiene **1 sola fila** para ese `id_celda` (no 2), con `estado_A4A5=PENDIENTE`; `data/cola-adquisicion-v1_0.tsv` es **byte-idéntico** a correr `vista_cola_adquisicion.py` aparte (T26). | Continuar si T26/T26-bis no muestran FAIL nuevo y la 2ª corrida no duplicó la fila. **Detenerse** si no hay forma de aislar un marco de prueba sin tocar datos reales — usar SIEMPRE copias en directorio temporal. |
| A3 | `.claude/commands/arbitra.md` líneas 50-51 (COMMIT-2 documentado) | Corregir el texto: comitear la fila (alta o actualización) en `data/curacion-registro/cola-adquisicion-registro.tsv` **y** la vista regenerada, nunca "las filas nuevas en `data/cola-adquisicion-v1_0.tsv`" directamente. | La documentación operativa deja de instruir comitear una corrupción de esquema. | `grep -n "cola-adquisicion-v1_0" .claude/commands/arbitra.md` | Ninguna línea debe instruir escribir directo la vista. | Revisión textual; sin criterio de PARO. |
| A4 | `tools/curador_registro/registra_cola_adquisicion.py` `main()` (líneas 74-84) | Agregar `parser.add_argument("--confirmo-migracion-legacy", action="store_true")`. **Antes de `write_tsv()`, incondicionalmente** (exista o no `args.output`, tenga o no filas): si no se pasó la bandera → abortar (mensaje explícito: este script trunca/crea el SSOT en sentido vista→registro; las altas nuevas van por el escritor canónico de A1/A2) sin escribir nada. El default vista→SSOT nunca vuelve a ser una escritura accidental, ni siquiera la primera vez. | El SSOT de producción no puede truncarse/invertirse/crearse por defecto, en ningún escenario. | Sobre **copias temporales**: `python3 .../registra_cola_adquisicion.py` (sin bandera, con y sin `--output` preexistente) → debe fallar sin escribir en AMBOS casos; con `--confirmo-migracion-legacy` → comportamiento idéntico al pre-cambio. | Sin bandera (ambos escenarios): exit≠0, ningún archivo nuevo creado, ninguno existente modificado. Con bandera: comportamiento idéntico al pre-cambio. | Continuar si los 3 escenarios (sin destino, con destino vacío, con destino poblado) fallan igual sin la bandera. |
| A5 | Cierre del commit | — | — | `python3 tests/check.py --baseline` completo; `grep -rn 'cola-adquisicion-v1_0.tsv' --include=*.py . \| grep -v vista_cola_adquisicion.py \| grep -E 'open\(\|write_text'` | `tests/check.py` sigue VERDE (cero FAIL nuevo); el grep de escritores directos da **vacío**. | Si el grep encuentra otro escritor no contemplado en este plan: **PARO material** — investígalo antes de comitear. |

**Commit A — mensaje sugerido**: `MAESTRA37-INFRA-1 Frente A (COMMIT-1): SSOT de adquisición — arbitra.py deja de escribir la vista, migrador legacy exige intención explícita`

---

### COMMIT B — Frente B · Manifiesto seguro `[ADENDA]`

**Enmiendas aplicadas: B.5-B.8 de la adenda.** El lock cubre el
read-modify-write **completo** de cada comando escritor (`cmd_registra`,
`cmd_promueve`, `cmd_escanea`), no solo la función de escritura interna —
esto es un cambio de forma, no solo de alcance: el lock se adquiere al
**inicio** de cada `cmd_*` (antes de leer el manifiesto/staging) y se
libera al **final** (después del `os.replace`), envolviendo también la
lógica de decisión intermedia. La validación previa al reemplazo es
**estructural completa**, no solo un allowlist de claves top-level.

| Paso | Archivo | Cambio | Invariante protegida | Comando de prueba | Salida esperada | Continuar / Detenerse |
|---|---|---|---|---|---|---|
| B1 | `tests/manifiesto.py` (nueva función `_validar_manifiesto_completo(entradas)`, invocada antes de todo `os.replace`) | Constante `CAMPOS_CONOCIDOS` (re-derivar el censo real con `yaml.safe_load`+`Counter` antes de fijar la lista; 18 medidas en esta sesión: `id, usado_para, url_origen, url_origen_procedencia, fecha_descarga, descargado_por, archivo, raiz, sha256, tamano_bytes, entorno_descarga, formato, licencia, nota, fecha, hecho, verificacion_tamano, retirada`). `_validar_manifiesto_completo` recorre **todas** las entradas y exige, en orden: (1) cada entrada es `dict`; (2) `id` es string no vacío; (3) los `id` son únicos en el conjunto completo (no solo la entrada nueva); (4) `set(entrada.keys()) - CAMPOS_CONOCIDOS == set()`, si no → abortar citando la(s) clave(s) sobrante(s); (5) si la entrada es de tipo **payload** (tiene `sha256`): `archivo` string no vacío, `sha256` coincide con `^[0-9a-f]{64}$`, `tamano_bytes` es `int` y `>= 0`; (6) si la entrada **no** es payload: debe satisfacer `_es_documental(entrada)` (paso B2) — si no satisface ninguna de las dos ramas estructurales, abortar. **Las 5 entradas históricas sin `sha256` son fixtures de regresión que deben pasar por estructura, nunca una allowlist de sus 5 IDs codificada en la validación.** Invocar `_validar_manifiesto_completo` sobre la lista completa de entradas (no solo la nueva) al inicio de cada `cmd_*` escritor, antes de construir el YAML de salida. | Una clave nueva no prevista, un `sha256` malformado, un `tamano_bytes` inválido o una entrada no-payload que no encaje en ninguna rama documental/retirada fallan explícito, nunca pasan mudos (cierra `forense/hallazgos.md:671`). | `python3 -c "...manifiesto._validar_manifiesto_completo([{'id':'x','clave_invento':1}])"`; casos análogos con `sha256` de 63 caracteres, `tamano_bytes=-1`, `tamano_bytes="10"` (string). | Cada caso aborta citando el campo/regla exacta violada. Una entrada 100% válida (payload o documental/retirada) valida sin error. | **Detenerse** si al re-derivar el censo contra el manifiesto real aparece una clave legítima no listada: usar la lista re-derivada. |
| B2 | `tests/manifiesto.py` | Función `_es_documental(entrada)` con **dos ramas**, no una: (a) `set(entrada.keys()) <= {"id","fecha","hecho"}`; (b) `"archivo" not in entrada and "sha256" not in entrada and "retirada" in entrada`. Consistente con el criterio ya usado por `cmd_verifica` (línea 368: `[e for e in entradas if "sha256" in e]`) — lo documenta, no lo sustituye. | La clase "sin payload exigible" se reconoce por estructura, nunca por lista cerrada de IDs. | Cargar `data/manifiesto.yaml` real (solo lectura) y confirmar que las 5 entradas sin `sha256` caen cada una en exactamente una rama. | Las 4 documentales puras caen en (a); la entrada `retirada` (línea ~6646) cae en (b); ninguna entrada con `sha256` cae en ninguna rama. | **Detenerse** si aparece una sexta entrada sin `sha256` que no encaje en ninguna rama: documentar y pedir decisión de mesa, no forzarla. |
| B3 | `tests/manifiesto.py` función `escribir_manifiesto` (247-252) | Reescribir siguiendo `integrate_barrido2.py::_replace_with_rollback` (367-393): generar YAML en memoria → `tempfile.mkstemp(prefix=".manifiesto.yaml.", dir=os.path.dirname(manifiesto_path))` → `flush()`+`os.fsync()` → releer/re-parsear con `yaml.safe_load` confirmando YAML válido y mismo nº de entradas → `os.replace()` → `finally` que borra el temporal si algo falla antes del replace. Extraer `_escribir_atomico(path, texto)` reutilizado también por la escritura de staging (`cmd_escanea` 831-832, `_reescribir_staging_restante` 956-969). Corregir el comentario falso de `tools/adquiere_cron.sh:73` sobre `.gitignore` de `manifiesto-staging.yaml`. | `data/manifiesto.yaml` (y staging) nunca queda truncado/corrupto tras un crash a mitad de escritura. | `monkeypatch` de `os.replace` para lanzar excepción a mitad de `escribir_manifiesto()` sobre copia temporal; `python3 tests/test_manifiesto_alcance.py` completo. | Archivo original intacto tras la excepción simulada; `test_manifiesto_alcance.py` en verde. | Continuar si ambos se confirman. |
| B4 | `tests/manifiesto.py`, funciones `cmd_registra`, `cmd_promueve`, `cmd_escanea` | **Lock de alcance completo, no solo sobre `escribir_manifiesto`.** Cada una de las 3 funciones adquiere `fcntl.flock(handle.fileno(), fcntl.LOCK_EX)` sobre `data/.manifiesto.lock` **al inicio de la función** (antes de la primera lectura de `data/manifiesto.yaml` o `data/manifiesto-staging.yaml`) y lo libera **al final** (después del último `os.replace` de esa invocación), envolviendo: lectura del manifiesto/staging, la lógica de decisión (dedup, resolución de raíz, derivación de id), la validación de B1, y la escritura atómica de B3. Implementar como context manager `_con_lock_manifiesto()` usado como `with _con_lock_manifiesto(): ...` al inicio de cada `cmd_*`, para no duplicar el `flock`/`release` en las 3 funciones. Comentario explícito junto al lock: *"Protege escritores que comparten este archivo de lock (mismo filesystem/máquina). No coordina clones independientes con archivos de lock distintos. No es una solución de concurrencia distribuida."* | Dos invocaciones concurrentes de `--registra`/`--promueve`/`--escanea` en la MISMA máquina no intercalan NINGUNA fase de su lectura-decisión-escritura (cierra el escenario real de `forense/hallazgos.md:669`, que fue exactamente una carrera de lectura-antes-de-escritura, no solo de escritura simultánea). | Lanzar dos invocaciones casi simultáneas de `--registra` sobre ids distintos (bash `&`) contra el mismo manifiesto de prueba; repetir con `--promueve` y con `--escanea`. | El resultado final tiene **ambas** entradas en los 3 escenarios. | **Detenerse** (documentar, no fabricar) si el mecanismo de prueba no logra forzar una carrera real de forma determinista — reportar el intento tal cual salió. |
| B5 | `.gitignore` | Agregar el archivo de lock runtime (`data/.manifiesto.lock`) — nunca debe comitearse. | El artefacto de lock es puramente de ejecución local, no versionado. | `grep -n "manifiesto.lock" .gitignore` | Presente. | — |
| B6 | Cierre del commit | — | — | `python3 tests/check.py --baseline`; `python3 tests/test_manifiesto_alcance.py`; correr `--verifica`/`--compara` reales (solo lectura) y confirmar `mtime`/hash de `data/manifiesto.yaml` sin cambio. | Todo verde; el manifiesto real no cambia de hash tras `--verifica`/`--compara`. | — |

**Commit B — mensaje sugerido**: `MAESTRA37-INFRA-1 Frente B (COMMIT-2): manifiesto seguro — validación de esquema, clase histórica por estructura, escritura atómica y lock local`

---

### COMMIT C — Frente C · Alta atómica de relaciones `[ADENDA]`

**Enmiendas aplicadas: C.9-C.12 de la adenda.** `alta_relacion.py` v1
**siempre** rechaza un `relacion_id` ya existente — se elimina por completo
la rama "salvo fusión" del diseño original (una fusión/procedencia
adicional no es una alta nueva; queda fuera de esta operación, sin excepción).
El script **no decide alias**: si la fuente no resuelve contra el alias
index y la entrada no trae ya la decisión explícita, PARO. Se **elimina
toda invocación a `via_capa2.py`** del preflight/candidato — INFRA-1 corre
en nube sin corpus, así que la validación de capa física queda fuera de
esta operación por completo (ver Commit 1 de INFRA-2 para eso). La
atomicidad es local a esta operación: además del lock y el CAS por hashes,
se documenta que **ningún otro escritor del registro debe correr en
paralelo** mientras `alta_relacion.py` está en vuelo.

| Paso | Archivo | Cambio | Invariante protegida | Comando de prueba | Salida esperada | Continuar / Detenerse |
|---|---|---|---|---|---|---|
| C1 | `tools/curador_registro/baseline.py` (junto a `relacion_id`, 48-50) | Codificar por primera vez `objeto_evidencia_id(fuente, descripcion) -> "OE-"+sha256(...)[:24]` y `procedencia_id(relacion_id, fuente, objeto, evidencia_ref) -> "PROV-"+sha256(...)[:24]`, usando **exactamente** las fórmulas de `GUIA-CURADOR-REGISTRO.md:62-63` (leer el separador/orden literal, no adivinar). | Determinismo: misma entrada → mismo ID siempre. | Test nuevo junto a `test_baseline_reusable.py`: llamar ambas funciones dos veces con la misma entrada (igual) y con una distinta (diferente). | IDs deterministas y sensibles a cualquier componente de la tupla. | — |
| C2 | `tools/curador_registro/alta_relacion.py` (nuevo) | Entrada YAML/JSON `{necesidad_id, fuente_canonica_normalizada?, alias_decidido?, objeto_evidencia_id_canonico\|descripcion_objeto, relacion:{...}, evidencia:{...}, utilidad:{...}, procedencia_nota}`. **Preflight**: (1) `necesidad_id` existe en `necesidad-objeto-modelo.tsv`, si no → abortar; (2) resolución de fuente: consultar el alias index vigente (`aliases-fuentes.tsv`) para `fuente_canonica_normalizada`; si no resuelve, la entrada **debe** traer `alias_decidido` (el operador ya tomó la decisión fuera del script) — si tampoco lo trae, **PARO explícito**: "fuente sin alias resuelto y sin `alias_decidido` en la entrada; el script no decide equivalencias por parecido"; el script nunca infiere una decisión de alias por similitud de texto; (3) `relacion_id` calculado con la terna — si **ya existe** en `relaciones.tsv` real, **abortar siempre**, sin excepción de fusión ("relación duplicada: `<relacion_id>` ya existe; una fusión/procedencia adicional no es una alta nueva y está fuera de esta operación"). **Candidato aislado**: `tempfile.TemporaryDirectory(dir=registry.parent)`, copiar las 7 tablas de `baseline.py::ARCHIVOS_TSV` + `baseline.json`, anexar filas con `csv.DictWriter` preservando fieldnames reales. **Recifrado**: `sync_bootstrap._freeze_manifest(candidate, template)` con el `template` ya modificado (nota de `procedencia.origen` **anexada**) antes de llamar. **Validación — SIN `via_capa2.py`**: (a) `validar_baseline(candidate)` debe dar `ok=True` antes de continuar; (b) si la entrada trae `id_manifiesto`, verificar **únicamente de forma estructural** (cadena de texto contra las claves `id` de `data/manifiesto.yaml`, sin tocar disco) que cada id citado existe en el manifiesto — si alguno no existe, abortar citando cuál; (c) el script **nunca** afirma nada sobre `AUSENTE`/`RAIZ_NO_CONFIGURADA`/disco físico — eso es exclusivamente competencia de `via_capa2.py --vincula` en INFRA-2. **Transacción**: `fcntl.flock` sobre `data/curacion-registro/.alta-relacion.lock`; comparar sha256 del registro real capturados al inicio vs. actuales (abortar `REGISTRO_CAMBIO_DURANTE_ALTA` si difieren); swap atómico reusando `integrate_barrido2._replace_with_rollback` **o** `sync_bootstrap._atomic_replace_many` (una de las dos, no una tercera implementación). **Post**: releer sha256 reales vs. candidato (`RELECTURA_POST_INTEGRACION_DIVERGENTE` si difiere), re-correr `baseline.py` como subprocess, escribir journal JSON (`before_sha256/after_sha256/changed/relacion_id`), y **recomendar explícitamente correr `tests/check.py` (o T21, líneas 2044-2093) antes de abrir el PR** — T21 ya causó un FAIL real tras un recifrado que `baseline.py` había aceptado (commit `27efeb1`). **Prohibido codificar en el script** (recordarlo en el docstring, y agregar la nota operativa de C.12: *"No correr ningún otro escritor de `data/curacion-registro/` [otro `alta_relacion.py`, `via_capa2.py --vincula`, `integrate_barrido2.py`, etc.] en paralelo mientras esta operación está en vuelo — el lock protege el swap, no una ejecución concurrente completa de otra herramienta sobre el mismo registro"*): no decide CANDIDATA→CONFIRMADA; no adjudica parecido nominal como identidad; no convierte presencia física en satisfacción semántica; no convierte evidencia en parámetro del modelo — `clasificacion_relacion`, `capa4_apertura_mapeo`, `confianza`, `conflicto_material` siempre vienen del YAML/JSON del operador. | Ninguna de las 4 tablas queda en estado intermedio visible; identidad estable de la relación; **cero decisiones de alias o de fusión tomadas por el script**. | `python3 tools/curador_registro/alta_relacion.py --dry-run entrada-fixture.yaml`; luego sin `--dry-run` sobre un `data/curacion-registro/` de prueba (copia completa, nunca el real); además un caso con `relacion_id` ya existente (debe abortar siempre) y un caso con fuente sin alias y sin `alias_decidido` (debe hacer PARO explícito). | `wc -l` +1 en las 3 tablas; `baseline.json` recifrado con `ok:true`; journal JSON escrito. El caso duplicado y el caso sin alias resuelto **nunca** escriben nada. | **Detenerse** si el preflight de `necesidad_id` falla: nunca asignar un N nuevo automáticamente. **Detenerse** siempre ante `relacion_id` duplicado o alias no resuelto — no hay bandera que lo fuerce en v1. |
| C3 | `tools/curador_registro/tests/test_alta_relacion.py` (nuevo) — **prueba obligatoria del encargo** | Forzar `validar_baseline(candidate)` a devolver `ok=False` (monkeypatch) **después** de que las 3 tablas + `baseline.json` ya se escribieron en el candidato pero **antes** del swap. Adicionalmente, forzar un fallo durante la revalidación **post-swap** (simulando `_replace_with_rollback`). Agregar también `test_relacion_duplicada_siempre_rechaza` (sin excepción de fusión) y `test_alias_no_resuelto_hace_paro_explicito`. | Un fallo tardío no puede dejar 1, 2 o 3 tablas adelantadas; un duplicado o un alias no resuelto nunca se escribe. | `pytest tools/curador_registro/tests/test_alta_relacion.py -v` | `relaciones.tsv`/`evidencias.tsv`/`utilidad-modelo.tsv`/`baseline.json` reales quedan **byte-idénticos** al estado previo (`diff` vacío) en el caso de fallo tardío; ningún tempdir huérfano; los casos de duplicado/alias abortan sin tocar disco. | **PARO material** si el test de rollback no logra demostrarlo completo — no se abre el PR sin esta prueba en verde. |
| C4 | Cierre del commit | — | — | `python3 tools/curador_registro/baseline.py data/curacion-registro` (sobre el registro real, sin tocar); `python3 tests/check.py --baseline` | `baseline.py` sigue `ok:true` sobre el registro real (no tocado por los tests); suite VERDE. | — |

**Commit C — mensaje sugerido**: `MAESTRA37-INFRA-1 Frente C (COMMIT-3): alta atómica de relaciones — tools/curador_registro/alta_relacion.py`

---

### Cierre de INFRA-1

```bash
python3 tests/check.py --baseline           # comando de cierre — debe seguir VERDE
git push -u origin claude/maestra37-infra-1-ssot-manifiesto-alta
```

Abrir **un solo PR** título `MAESTRA37-INFRA-1 · SSOT-MANIFIESTO-ALTA`.
**INFRA-1 termina en PR abierto — no incluye merge.**

**Evidencia que Claude Code CLI debe devolver al cerrar**:
1. Salida completa de `python3 tests/check.py --baseline` (antes y después).
2. Confirmación textual de que `.claude/commands/adquiere.md` no fue tocado.
3. Resultado de `test_fallo_tardio_no_deja_tablas_adelantadas`.
4. Grep de "cero escritores directos de la vista" (paso A5).
5. Diff resumido por commit (A/B/C) y cualquier desviación de este plan
   causada por algo que cambió entre esta planificación y la ejecución (§2).

---

## LIBRO 2 · Claude Code CLI · INFRA-2 (CAPA2-Y-PORTABILIDAD) `[AJUSTE DE DIRECCIÓN]`

> **AJUSTE DE DIRECCIÓN APLICADO** (11 puntos, posterior a la adenda
> D.13-D.15/E.16-E.18/FP259.19-20). Reduce LIBRO 2 a **dos commits
> productivos** (elimina el `COMMIT 0` independiente), condiciona la
> construcción de `--vincula` a que existan casos reales exactos medidos en
> caja (no se construye por anticipado), exige sincronizar `baseline.json`
> (y derivados, cuando aplique) tras cualquier escritura de `relaciones.tsv`,
> reduce la batería de pruebas a lo estrictamente dirigido, corrige el
> manejo de raíz no configurada en `semantic_run.py` (nunca `Path(None)`,
> nunca confundida con `ARCHIVO_NO_EXISTE`), y reemplaza el criterio de
> cierre de INFRA-2 por la lista de 9 puntos al final de este LIBRO. En caso
> de contradicción con el cuerpo `[ADENDA]` anterior de este LIBRO 2, este
> ajuste manda; los puntos de la adenda que no contradice (raíz por entrada,
> `IDENTIDAD_NO_DEMOSTRADA`, distinción por raíz en FP-259) siguen vigentes.

### Compuerta de arranque (versión corta)

1. `git fetch origin main`
2. Confirmar que INFRA-1 está fusionado: `git log --oneline -5 origin/main`
   debe mostrar el commit de merge del PR de INFRA-1. **PARO** si no está
   fusionado — INFRA-2 no puede empezar.
3. Worktree **fresco**, distinto del de INFRA-1:
   ```bash
   git worktree add ../mm-infra2 origin/main
   cd ../mm-infra2
   git checkout -b claude/maestra37-infra-2-capa2-portabilidad
   ```
4. Confirmar corpus y raíces:
   ```bash
   ls data/raw | head -3
   cat data/raices.local.yaml
   ```
   Deben existir y declarar al menos `descargas_mx`. **PARO** si cualquiera falta.
5. Correr:
   ```bash
   python3 tools/curador_registro/baseline.py data/curacion-registro
   python3 tests/check.py --baseline
   ```
   Si ambos están bien (`ok:true` y "LÍNEA BASE: VERDE"), **continuar**.
   **No volver a correr la batería específica A/B/C de INFRA-1** — el merge
   más estos dos comandos son evidencia suficiente para arrancar INFRA-2.

Archivos a **leer completos antes de editar**: `tools/curador_registro/via_capa2.py`,
`tools/curador_registro/tests/test_via_capa2.py`, `tests/corpus.py`,
`tools/curador_registro/semantic_run.py` (líneas 276-330, 450-520),
`tools/curador_registro/snapshot_universe.py` (líneas 180-300, 777),
`tests/manifiesto.py` (líneas 180-220, `resolver_raiz`),
`tools/curador_registro/sync_bootstrap.py` (`_freeze_manifest`,
`_atomic_replace_many`, y cualquier función de construcción de
`bootstrap-semantico.tsv`/`trabajo-semantico.tsv` — confirmar el nombre real
leyendo el archivo, no asumir), `data/curacion-registro/{bootstrap-semantico,
trabajo-semantico}.tsv` (cabeceras, para saber si dependen materialmente de
`relaciones.tsv`), `GUIA-CURADOR-REGISTRO.md`, `forense/firmas-pendientes.tsv`
fila FP-259, `forense/notas/2026-09-03-MAESTRA37-L1-censo.md`,
`forense/notas/2026-08-18-b2-v7.md` (para confirmar la exclusión de
`correr-olas-v7.py`).

### Medición previa a D (no es un commit independiente)

Antes de editar cualquier archivo, correr y guardar **temporalmente** (un
archivo de trabajo local, no comiteado aparte — estas cifras entran en la
nota/commit de D y en el PR, nunca en un commit propio cuyo único producto
sea congelarlas):

| Comando | Qué mide |
|---|---|
| `python3 -c "import csv; f=list(csv.DictReader(open('data/curacion-registro/relaciones.tsv',encoding='utf-8-sig',newline=''),delimiter='\t')); print(len(f), sum(1 for r in f if r['id_manifiesto']!='NO_DETERMINADO'), sum(1 for r in f if r['id_manifiesto']=='NO_DETERMINADO'))"` | relaciones totales / con `id_manifiesto` / sin (`NO_DETERMINADO`) |
| `python3 -m tools.curador_registro.via_capa2 --root .` (lectura, sin `--escribe`) | COINCIDE / NO_COINCIDE / AUSENTE / RAIZ_NO_CONFIGURADA reales + `diagnostico_candidatas_sin_id` |
| Cruce de IDs de `relaciones.tsv` contra `data/manifiesto.yaml` | IDs explícitos que no resuelven |
| `python3 tests/corpus.py` (tal cual, antes de tocar el código) | C1 "antes", sin desglose |

Rederivar los 4 números en caja — las cifras de planificación sin corpus
(137 sin `id_manifiesto`, 98 diagnósticos, 0 con SHA real sin id, 0 IDs
colgantes) son de referencia, no de contrato.

**Criterio de detenerse**: si `via_capa2.py --root .` sale con el guard de
"cero payloads verificables" pese a haber confirmado `data/raices.local.yaml`
en el paso 4 de la compuerta — configuración incompleta, no medición real;
corregir antes de continuar.

---

### COMMIT 1 — Frente D · Cierre físico y sincronización del registro

**Regla rectora: medir primero, decidir después si `--vincula` hace
falta.** No se implementa por anticipado.

**D-A · Filas que YA tienen `id_manifiesto` (vía existente, sin herramienta nueva)**

Correr `via_capa2.py --root .` sobre el corpus real. Verificar todos los IDs
ya explícitos contra `data/manifiesto.yaml`; las filas con lista de varios
IDs (`;`) exigen `COINCIDE` en **todos** antes de promover — comportamiento
ya existente de `derivar()`/`verificar_entrada()`, no se reimplementa.
Aplicar `--escribe` únicamente sobre los diffs que `derivar()` calculó de
forma legítima.

| Invariante protegida | Comando | Continuar / Detenerse |
|---|---|---|
| `capa2_manifiesto`↔`capa3_disco_real` biyectivos (ya cubierto por `test_promover_lleva_capa3_y_solo_en_las_promovidas`). | `python3 -m tools.curador_registro.via_capa2 --root . --escribe` | Continuar si `derivar()` no reveló un defecto de código nuevo. Si `via_capa2.py` no se modifica en este paso, no correr la suite completa por esto — el comportamiento no cambió. |

**D-B · Filas sin `id_manifiesto` — medir antes de construir nada**

El diagnóstico por nombre/alias (`diagnostico_candidatas_sin_id`) **no es
identidad** y no enlaza ninguna fila. Buscar, sobre el corpus real,
únicamente evidencia estructurada exacta que **ya exista** entre las filas
`NO_DETERMINADO`:

- SHA exacto ya comprometido (`sha256_fuente` coincide con un `sha256` real
  de `data/manifiesto.yaml`);
- ID de manifiesto explícitamente citado en evidencia estructurada
  (`evidencia_ref`/`evidencia_textual_breve`) aún no trasladado a `id_manifiesto`;
- decisión explícita de mesa ya registrada en alguna nota forense para esa
  relación puntual.

**Regla de bifurcación (obligatoria):**

- **Si el número de enlaces nuevos exactamente resolubles es 0**: no crear
  `--vincula`. Declarar en la nota/commit `enlaces nuevos exactamente
  resolubles = 0` y cerrar D después de D-A. Este es el resultado esperado
  por defecto, no un fracaso.
- **Si es > 0**: implementar la vía mínima `--vincula
  RELACION_ID:ID_MANIFIESTO[;ID...]` en `via_capa2.py`, acotada a los casos
  reales encontrados (no una herramienta genérica especulativa): exige
  `id_manifiesto==NO_DETERMINADO` previo; exige que todos los ids resuelvan
  contra `data/manifiesto.yaml`; exige `COINCIDE` en todos vía
  `verificar_entrada()` antes de escribir, rechazando el lote completo si
  alguno falla; reusa `aplicar_diffs()` para escribir. El diagnóstico por
  nombre/alias **nunca** es argumento válido de `--vincula`, ni siquiera
  como sugerencia sin revisión.

**D-`sha256_fuente` (solo si se implementó `--vincula`)**

- Un `id_manifiesto` único: derivar `sha256_fuente` directamente del
  `sha256` de esa entrada del manifiesto ya verificada por `COINCIDE` —
  nunca dejar `id_manifiesto=<ID_REAL>` con `sha256_fuente=NO_DETERMINADO`
  si el SHA ya está en el manifiesto.
- Una lista de varios IDs: **antes de escribir nada**, leer 2-3 filas reales
  que ya tengan lista de varios IDs y confirmar cómo representan hoy
  `sha256_fuente` para ese caso. Si el esquema vigente no representa
  múltiples hashes de forma inequívoca, **no introducir un formato nuevo en
  este acto** — documentar y continuar solo con los casos de ID único que sí
  encajan en el esquema vigente.

**D-sincronización (obligatoria si D escribió `relaciones.tsv`, por cualquiera de las dos vías)**

Cualquier cambio de `id_manifiesto`, `sha256_fuente`, `capa2_manifiesto` o
`capa3_disco_real` cambia el hash de `relaciones.tsv`:

1. Recifrar `baseline.json` reusando `sync_bootstrap._freeze_manifest` (o el
   nombre real confirmado por lectura) — no reimplementar el cálculo.
2. Correr `validar_baseline` (`tools/curador_registro/baseline.py`), exigir
   `ok:true` antes de comitear.
3. Si la regeneración vigente de `bootstrap-semantico.tsv`/
   `trabajo-semantico.tsv` depende materialmente de la relación física
   recién cerrada, regenerarlos con la herramienta ya existente
   (`sync_bootstrap`/`build_cableado`/clasificación vigente — confirmar cuál
   aplica leyendo el código, no asumir) — **no crear otra arquitectura de
   sincronización**. Si su regeneración no produce cambios, no tocarlos.
4. **Resultado obligatorio**: `python3 tools/curador_registro/baseline.py
   data/curacion-registro` → `ok: true`, con `relaciones.tsv` y
   `baseline.json` en el MISMO commit. Nunca dejar `relaciones.tsv` nuevo
   con `baseline.json` viejo.

**Pruebas de D — una dirigida, no cuatro**

Ya existen pruebas de: payload válido promueve; payload roto no promueve;
diagnóstico nominal no promueve; capa2/capa3 se mantienen juntas; listas de
`id_manifiesto` ya tratadas por la vía actual (`test_via_capa2.py`, 6
tests). **No duplicarlas.**

- Si **no se modificó `via_capa2.py`** (caso "0 enlaces nuevos"): no añadir
  tests. Confirmar que el archivo existente sigue verde:
  `pytest tools/curador_registro/tests/test_via_capa2.py -v`.
- Si **sí se implementó `--vincula`**: añadir **como máximo una** prueba
  nueva — `test_vincula_lote_invalido_no_deja_vinculacion_parcial` (un lote
  con varios pares donde uno falla `COINCIDE` no deja ninguno de los otros
  escrito) — y correr el archivo completo:
  `pytest tools/curador_registro/tests/test_via_capa2.py -v`.

**Commit 1 — mensaje sugerido**: `MAESTRA37-INFRA-2 (COMMIT-1): Frente D — cierre físico de relaciones.tsv y sincronización de baseline.json [+ derivados si aplica]`

---

### COMMIT 2 — Frente E + FP-259 · Portabilidad y clasificación de huérfanos

**Frente E — solo `tools/curador_registro/semantic_run.py`. Ningún otro de
los 8 archivos se toca** (los 5 ENOE y el comentario de
`hitod_r10_1_kappa_v2_1.py` no son generadores reales y/o pertenecen a actos
ya cerrados; `correr-olas-v7.py` está **explícitamente excluido**). Se
conserva la corrección de raíces de la adenda previa (`ruta_logica =
f"{nombre_raiz}:{row['archivo']}"`; `data_raw` → `repo/data/raw`; raíces
externas → `data/raices.local.yaml`; nunca serializar `/home/pc0/...`),
**con el ajuste siguiente sobre raíz no configurada**:

| Paso | Cambio | Invariante protegida |
|---|---|---|
| INFRA-E1 | `corpus = repo / "data" / "raw"` (default de `data_raw`; sin cambio respecto a la adenda previa). | El corpus físico de `data_raw` sigue siendo `data/raw`. |
| INFRA-E2 | `parse_manifest()`: `nombre_raiz = row.get("raiz", "data_raw")`; `ruta_logica = f"{nombre_raiz}:{row['archivo']}"`. Si `nombre_raiz != "data_raw"`, resolver con `resolver_raiz()` de `tests/manifiesto.py` — si devuelve `None`, `ruta_resuelta = None` (**nunca** envolver ese `None` en `Path(...)` más adelante — `semantic_run.py` hoy espera un `Path`, así que el llamador debe comprobar `is None` antes de construirlo). | La raíz no configurada se representa como dato explícito (`None`), nunca como una ruta inválida que reviente `Path()`. |
| INFRA-E3 | En el loop de apertura, **antes** de invocar `open_local_object()`: si `ruta_resuelta is None`, no intentar abrir ningún archivo — construir directamente el resultado: `ruta = ruta_logica`, `resultado = "RAIZ_NO_CONFIGURADA"`, `sha256 = "NO_DETERMINADO"`, `hash_reconcilia = "NO_VERIFICADO"`. **Nunca** etiquetar este caso como `ARCHIVO_NO_EXISTE` ni `NO_COINCIDE` — son hechos distintos (raíz no configurada en esta máquina vs. archivo genuinamente ausente en una raíz que sí está configurada). | Una raíz no configurada nunca se confunde con un archivo ausente o una integridad rota. |
| INFRA-E4 | Cuando `ruta_resuelta` no es `None` (raíz configurada, `data_raw` o externa): usar `open_local_object()` normalmente, serializando siempre `ruta_logica` en el campo `"ruta"` (incluida la rama `ARCHIVO_NO_EXISTE`, que sigue siendo un caso distinto de `RAIZ_NO_CONFIGURADA`). | `sha256(path)` sigue calculándose sobre la `Path` real cuando existe. |

**Prueba de E — una sola, con tres entradas dentro**

Un único test dirigido con tres entradas de manifiesto: (1) `data_raw`; (2)
raíz externa configurada; (3) raíz externa no configurada. Debe demostrar
solamente: ruta lógica correcta en las 3; apertura física correcta cuando
existe (1 y 2); `RAIZ_NO_CONFIGURADA` (no `ARCHIVO_NO_EXISTE`) en (3); cero
ruta absoluta de máquina serializada en ninguna. Eso basta.

```bash
pytest tools/curador_registro/tests/test_semantic_run.py::test_portabilidad_tres_raices -v
```

**FP-259(iii) — `tests/corpus.py`.** Se conserva la corrección conceptual
de la adenda previa: `presente_bajo_otra_raiz` **solo cuando** `sha256
igual AND raiz_declarada != raiz_actual`; un SHA duplicado bajo otra ruta de
la **misma** raíz permanece en `sin_registro` de esa ruta.

Procedimiento (sin sobreprobar):

1. `python3 tests/corpus.py` **antes** de tocar el código — guardar la salida.
2. Aplicar la reclasificación: factorizar `_indice_por_sha_y_raiz(entradas)`
   → `{sha256: [(entrada, raiz_declarada), ...]}`; en `c1_huerfanos()`,
   clasificar `presente_bajo_otra_raiz` solo si `raiz_declarada !=
   raiz_actual` para alguna coincidencia, `sin_registro` en cualquier otro
   caso (incluida la coincidencia dentro de la misma raíz).
3. `python3 tests/corpus.py` **después** — comparar.
4. **Exigir que el total de `C1` no cambie** — solo se subdivide el desglose.
5. Reportar el desglose real nuevo en la nota forense — sin forzarlo a
   coincidir con 86/77/9 ni con el 73 de MAESTRA37-L1.

**No crear un test dedicado si el corpus real ya ejercita el caso** (es
probable: FP-259 mismo documenta duplicados dentro de `descargas_mx`). Solo
si el corpus real **no** contiene ningún caso que permita verificar la
frontera misma-raíz/otra-raíz, añadir un fixture mínimo de una fila para
ese único propósito.

**Commit 2 — mensaje sugerido**: `MAESTRA37-INFRA-2 (COMMIT-2): Frente E — semantic_run.py distingue raíz no configurada; FP-259(iii) — corpus.py distingue otra-raíz de misma-raíz`

---

### Cierre de INFRA-2 (mínimo, sin batería indiscriminada)

```bash
# Solo si D modificó código (--vincula implementado):
pytest tools/curador_registro/tests/test_via_capa2.py -v

# Frente E:
pytest tools/curador_registro/tests/test_semantic_run.py::test_portabilidad_tres_raices -v

# FP-259:
python3 tests/corpus.py

# Invariantes globales (siempre):
python3 tools/curador_registro/baseline.py data/curacion-registro
python3 tests/check.py --baseline
```

Si todo lo anterior está correcto: `git push -u origin
claude/maestra37-infra-2-capa2-portabilidad` y abrir **un segundo PR**,
título `MAESTRA37-INFRA-2 · CAPA2-Y-PORTABILIDAD`, con las métricas
antes/después (medición previa a D vs. medición final de D) en el cuerpo.
**INFRA-2 termina en PR abierto — no incluye merge.** No seguir agregando
tests una vez protegidos los defectos materiales de este acto —
`python3 -m pytest tools/curador_registro/tests/ -q` (la batería completa)
**no** es parte del cierre salvo que algo de lo anterior falle y haga falta
diagnosticar más ampliamente.

### Criterio de éxito de INFRA-2 `[AJUSTE DE DIRECCIÓN]`

INFRA-2 termina cuando:

1. Todos los `id_manifiesto` ya explícitos han sido verificados (D-A).
2. Cero enlace exacto demostrable queda pendiente (no cero `NO_DETERMINADO`).
3. Ningún diagnóstico por parecido fue convertido en identidad.
4. Si D modificó `relaciones.tsv`, `baseline.json` y los derivados
   materialmente afectados quedaron sincronizados.
5. `semantic_run.py` deja de emitir rutas absolutas de máquina.
6. Una raíz no configurada se distingue explícitamente de un archivo
   ausente (nunca `ARCHIVO_NO_EXISTE` ni `NO_COINCIDE`).
7. `tests/corpus.py` distingue "presente bajo otra raíz" de "mismo
   contenido en la misma raíz".
8. `python3 tools/curador_registro/baseline.py data/curacion-registro` →
   `ok:true`.
9. `python3 tests/check.py --baseline` sin regresión material nueva.

**No se persigue `NO_DETERMINADO = 0`.** No se agrega automatización
(`--vincula` incluido) si la medición real en caja demuestra que no existe
ningún caso que la necesite.

---

## 3 · Matriz de pruebas (obligatorias, sección 14 del encargo)

| # | Prueba | Dónde | Cubierta por |
|---|---|---|---|
| A1 | Writer directo de vista = 0 | LIBRO 1 / A5 | grep dirigido |
| A2 | Registro → vista reproducible | LIBRO 1 / A2 | comparación byte a byte con T26 |
| A3 | Round-trip no altera filas ajenas | LIBRO 1 / A1 | diff +1 línea |
| A4 | `arbitra.py` usa SSOT | LIBRO 1 / A2 | ejecución sobre fixture |
| A5 | Migrador legacy requiere intención explícita | LIBRO 1 / A4 | ejecución sin/con bandera |
| A6 | `DEPOSITADO-SIN-REGISTRO` válido | ya cumplido (Frente A, confirmado 0/112 hoy, ningún enum lo rechaza) | verificación de solo lectura, sin cambio de código necesario |
| B1 | Payload válido | LIBRO 1 / B1 | test dirigido |
| B2 | Documental histórico válido | LIBRO 1 / B2 | las 5 entradas reales |
| B3 | Entrada malformed rechazada | LIBRO 1 / B1 | `clave_invento` |
| B4 | Clave top-level desconocida rechazada | LIBRO 1 / B1 | idem |
| B5 | ID duplicado rechazado | ya cubierto por dedup existente (`_index_manifiesto`) — confirmar sin romper en B3 | test_manifiesto_alcance.py |
| B6 | Escritura fallida conserva archivo previo | LIBRO 1 / B3 | monkeypatch de `os.replace` |
| B7 | Lock impide segundo escritor local | LIBRO 1 / B4 | doble invocación concurrente |
| B8 | Temporal no queda como estado válido | LIBRO 1 / B3 | `finally` + verificación de limpieza |
| C1 | +1 relación / +1 procedencia / +1 utilidad | LIBRO 1 / C2 | `wc -l` antes/después |
| C2 | IDs deterministas | LIBRO 1 / C1 | test doble llamada |
| C3 | Baseline válido | LIBRO 1 / C2/C4 | `baseline.py ok:true` |
| C4 | Fallo tardío → cero tablas adelantadas | LIBRO 1 / C3 | `test_fallo_tardio_no_deja_tablas_adelantadas` |
| C5 `[ADENDA]` | Relación duplicada **siempre** rechaza, sin excepción de fusión | LIBRO 1 / C2/C3 | `test_relacion_duplicada_siempre_rechaza` |
| C6 `[ADENDA]` | Fuente sin alias resuelto y sin `alias_decidido` → PARO explícito, nunca decisión automática | LIBRO 1 / C2/C3 | `test_alias_no_resuelto_hace_paro_explicito` |
| D1 | ID exacto puede promover | ya cubierto (`test_deriva_si_solo_con_payload_verificado`), sin duplicar | `test_via_capa2.py` (existente, no se toca salvo defecto) |
| D2 | Parecido nominal no promueve | ya cubierto (`test_diagnostico_no_promueve`), sin duplicar | idem |
| D3 `[AJUSTE]` | Listas de IDs requieren todos válidos | ya cubierto por la vía actual (`derivar()`/`verificar_entrada()`) — LIBRO 2 / D-A, sin test nuevo | `test_via_capa2.py` (existente) |
| D4 `[AJUSTE]` | `--vincula` (solo si se construye, caso ">0") rechaza un lote con un id inválido sin dejar vinculación parcial | LIBRO 2 / D-B, condicional | `test_vincula_lote_invalido_no_deja_vinculacion_parcial` (única prueba nueva permitida) |
| D5 | Después del cierre no queda enlace exacto conocido sin ejecutar | LIBRO 2 / D-A/D-B | operación + medición final documentada |
| D6 `[ADENDA]` | Caso sin identidad demostrada queda `NO_DETERMINADO` y se documenta como `IDENTIDAD_NO_DEMOSTRADA` (no se deja mudo) | LIBRO 2 / D-B | revisión de la nota forense de cierre |
| D7 `[AJUSTE]` | Si D escribió `relaciones.tsv`, `baseline.json` (y derivados materialmente afectados) quedan sincronizados en el mismo commit | LIBRO 2 / D-sincronización | `python3 tools/curador_registro/baseline.py data/curacion-registro` → `ok:true` |
| INFRA-E1 `[ADENDA+AJUSTE]` | Generador nuevo produce raíz lógica **correcta por entrada** en 3 casos (`data_raw`, externa configurada, externa no configurada); raíz no configurada nunca se confunde con `ARCHIVO_NO_EXISTE`/`NO_COINCIDE` | LIBRO 2 / INFRA-E1 a INFRA-E4 | **una sola** prueba dirigida con las 3 entradas |
| INFRA-E2 | Lector sigue tolerando referencia histórica | confirmado por Frente E: no hay lector activo que reparse estos campos hoy — no requiere cambio | verificación de solo lectura |
| FP1 `[ADENDA]` | Un SHA duplicado **dentro de la misma raíz** nunca se clasifica como "presente bajo otra raíz" | LIBRO 2 / FP-259 | caso real del corpus si lo ejercita; fixture mínimo solo si no |

---

## 4 · Criterios de PARO (material, detiene la sesión de ejecución)

**Globales (ambos libros):**
- `python3 tests/check.py --baseline` no está VERDE al arrancar o deja de
  estarlo tras un cambio (FAIL nuevo no presente en `tests/baseline.json`).
- Cualquier grep de "escritores directos" encuentra un caso no contemplado
  en este plan.
- Una prueba obligatoria (T26/T26-bis, `test_fallo_tardio_no_deja_tablas_adelantadas`,
  el test de portabilidad de INFRA-E5) no pasa.
- Aparece una clave/estructura del manifiesto, o una relación sin
  `necesidad_id` válida, que este plan no anticipó — documentar y pedir
  decisión, no forzar una rama de código improvisada.
- **`[ADENDA]`** Se intenta correr `alta_relacion.py` mientras otro escritor
  del registro (`via_capa2.py --escribe`/`--vincula`, otra invocación de
  `alta_relacion.py`, `integrate_barrido2.py`) está en vuelo sobre
  `data/curacion-registro/` — no ejecutar en paralelo (C.12); es una
  disciplina operativa, no algo que el lock por sí solo garantice contra
  otra herramienta.
- **`[ADENDA]`** `alta_relacion.py` encuentra un `relacion_id` ya existente,
  o una fuente sin alias resuelto y sin `alias_decidido` explícito — PARO
  siempre, sin bandera que lo fuerce en v1 (C.9/C.10).

**Específicos de INFRA-2:**
- La compuerta de arranque (versión corta) falla en cualquiera de sus 5 puntos.
- `via_capa2.py --root .` dispara el guard de "cero payloads verificables"
  después de confirmar `data/raices.local.yaml` — configuración incompleta,
  no medición real.
- Cualquier caso de enlace físico que dependa de "parecido" en vez de
  identidad exacta — nunca se adjudica, se documenta con razón concreta.
- El total de `tests/corpus.py::C1` cambia numéricamente tras el refactor de
  FP-259(iii) (señal de que se reclasificó un huérfano hacia OK, no permitido).
- **`[AJUSTE]`** Se implementa `--vincula` sin haber encontrado al menos un
  caso real de enlace exactamente resoluble en la medición previa a D — no
  se construye la herramienta hipotética sin un caso que la necesite.
- **`[AJUSTE]`** D escribió `relaciones.tsv` pero `baseline.json` quedó sin
  recifrar (`ok:false` o no corrido) — nunca comitear `relaciones.tsv`
  nuevo con `baseline.json` viejo.

---

## 5 · Criterios de aceptación (sección 15 del encargo, verificación explícita)

Al cerrar ambos PR (sin fusionarlos):

1. Escritores directos de `cola-adquisicion-v1_0.tsv` = 0 → grep de A5.
2. Registro↔vista reproducible → T26 verde.
3. Migrador legacy no invierte SSOT accidentalmente → A4.
4. Manifiesto validado antes de reemplazo → B1/B2.
5. Escritura de manifiesto atómica → B3.
6. Exclusión local de escritores activa → B4.
7. Alta de relación transaccional disponible → C2/C3.
8. Baseline del curador válido → C4.
9. IDs explícitos colgantes corregibles = 0 → **ya está en 0 hoy**; el
   commit debe incluir una prueba de regresión que lo mantenga en 0, no
   "corregirlo" (no hay nada que corregir).
10. Enlaces físicos exactos pendientes = 0 → LIBRO 2 / D-A y D-B (no
    `NO_DETERMINADO`=0; ver también el "Criterio de éxito de INFRA-2" al
    final de LIBRO 2, que refina este punto tras el ajuste de dirección).
11. Ambigüedad semántica no se convirtió en certeza → D-B regla dura +
    prohibiciones de C2.
12. Generadores afectados dejan de crear rutas absolutas nuevas → LIBRO 2 /
    INFRA-E1 a INFRA-E4 (solo `semantic_run.py`).
13. FP-259 queda correctamente clasificado → LIBRO 2 / procedimiento FP-259(iii).
14. Cero regresiones materiales nuevas → `tests/check.py --baseline` VERDE
    en ambos cierres.

Nota: tras el ajuste de dirección de LIBRO 2, los puntos 10-13 se verifican
en última instancia contra los 9 puntos del "Criterio de éxito de INFRA-2"
(final de LIBRO 2), que es la versión operativa y no persigue
`NO_DETERMINADO = 0` como meta.

---

## 6 · Orden de ramas / PR / merge

1. `claude/maestra37-infra-1-ssot-manifiesto-alta` desde `origin/main` (SHA
   re-derivado al arrancar) → 3 commits (A/B/C) → PR 1 abierto, sin fusionar.
2. **Mesa/dirección fusiona PR 1** (fuera del alcance de este plan — ningún
   agente se fusiona a sí mismo, per `AGENTS.md`).
3. Solo después de confirmar el merge: `claude/maestra37-infra-2-capa2-portabilidad`
   desde `origin/main` **posterior al merge de INFRA-1**, worktree fresco →
   **2 commits** (Frente D / Frente E+FP-259 — ajuste de dirección elimina
   el commit de medición independiente) → PR 2 abierto, sin fusionar.
4. Mesa/dirección fusiona PR 2 cuando decida.

No hay fusión entre INFRA-1 e INFRA-2 en paralelo — la compuerta de INFRA-2
depende explícitamente del merge de INFRA-1 (§ Compuerta de arranque).

---

## 7 · Fuera de perímetro (recordatorio, no se planifica ni se ejecuta)

SQLite, DVC, DataLad u otra base de datos; reestructuración general de
`data/`; reescritura de históricos (`correr-olas-v7.py` explícitamente
intocable); eliminación del migrador legacy (solo se gatea); resolución de
toda la adquisición pendiente; corrección de tests heredados no
relacionados; adjudicación semántica de nuevas relaciones; recalibración de
parámetros del modelo; documentación cosmética; otra capa de gobernanza.

## 8 · Hallazgos laterales no material (una línea cada uno, per AGENTS.md)

- `tools/curador_registro/via_capa2.py::cargar_raices()` duplica lógica de
  `tests/manifiesto.py::resolver_raiz()` en vez de reusarla — no se unifica
  en este encargo.
- El docstring de `via_capa2.py` cita cifras de ejemplo obsoletas del mismo
  día (13/ago y temprano el 3/sep) — riesgo de que alguien las cite como
  vigentes; se recomienda un comentario que remita a la nota fechada
  correspondiente en vez de un número fijo, pero no es parte de este encargo.
- `tools/curador_registro/via_capa2.py::aplicar_diffs()` escribe
  `relaciones.tsv` sin candado compartido con el futuro `alta_relacion.py`
  — riesgo de carrera si ambos corrieran en paralelo; fuera de perímetro de
  INFRA-1/2 (documentado como pregunta abierta de Frente C/D).
