# ENCARGO · B2-SEMANTICO (v2) — C4 → C5 → C6: la mitad que cierra el barrido

- **SHA de redacción (declarado por quien escribe):** `57984b5` (`PR #262`).
- **SHA real de arranque (derivado por quien ejecuta):** `f3d3f954823e08d3b3459ecaf4a5816a7913b36c` (`origin/main`, fusión de `PR #263`/`cond-atrib`). Deriva de **8 commits** sobre el SHA declarado, clasificada abajo.
- **Entorno asignado:** caja Ubuntu/WSL2 (`Linux 6.18.33.2-microsoft-standard-WSL2 x86_64`); toda curación corre bajo `unshare -Urn`. Git/GitHub fuera del namespace material.
- **Estado:** `CONSUMIDO` — `ACTO B2-SEMANTICO`, `PR #268` (borrador, no fusionado), 18/ago/2026. `ADR-108` (unión `R1 ∪ R7`, vía `lista-apertura`, fases `tareas`/`propuestas`, `build_cableado.py`, `FP-35` ejecutada) y `ADR-109` (`FP-46` adjudicada por la condición literal de `ADR-93`; 17 aperturas absorbidas; dependencia `FP-24` derivada **0 de 37**). Cierre: `COBERTURA-MATERIAL-COMPLETA · INTEGRACION-ORDINARIA-COMPLETA · DECISIONES-FP24-PENDIENTES=0`. Detalle: `forense/notas/2026-08-18-b2-semantico.md`.
- **Worktree/rama:** `/home/pc0/mm-b2-semantico` · `b2-semantico`, creada desde `origin/main`.
- **Raíces materiales autorizadas:** `data_raw=/home/pc0/mm-corpus/raw` (273 entradas) · `descargas_mx=/mnt/c/Users/PC0/Descargas MX` (70 entradas).
- **LEY:** `forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md` §17-§23 + §4 · §11 · §24 · §27 · §28. Este relevo actualiza el terreno, no la ley.

> Archivado bajo A.3 por la sesión que lo ejecuta. Texto verbatim del relevo; lo añadido es esta cabecera, el bloque A.8 y la verificación de premisas.

## Firma de entorno · A.2 (tres partes)

1. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **sin variable** (local, no nube).
2. Aislamiento: `unshare -Urn -- true` → 0; `unshare -Urn -- python3 -c "socket.create_connection(('1.1.1.1',53),2)"` → **falla** (namespace sin salida). Ambas partes verificadas en esta sesión.
3. Corpus montado: `ls data/raw/ | head -1` → `20260813130000.export.CSV.zip`. **Montado.**

`data/raw` es symlink a `/home/pc0/mm-corpus/raw`, creado en este worktree (compartido por los tres worktrees, gitignored). No es PARO (§27: "no pares porque data/raw es symlink").

## Verificación de existencia · A.8

### 1 · Estructura

Contra `data/INFRAESTRUCTURA-v1_0.md` en la base real: Dominio 3 gobierna snapshot/universo/inspección/ledger (cerrado por el gate material `PR #260`); Dominio 4 gobierna propuestas e integración — **es el dominio de este acto**; Dominio 7 gobierna ADR y cascada; Dominio 8 gobierna encargos y notas. El índice **no cubre todavía el cableado de BARRIDO-2**: esa es exactamente `FP-35`, que este acto ejecuta en C6 "después de observar los mecanismos reales".

### 2 · Contenido

Comando ejecutado antes de crear o editar producto alguno:

```text
forense/encargos/2026-08-18-B2-SEMANTICO-C4-C5-C6.md                        NO-ENCONTRADO
data/curacion-registro/ejecucion-semantica/barrido2/propuestas-barrido2.tsv  NO-ENCONTRADO
data/cableado-universo-v1_0.tsv                                             NO-ENCONTRADO
tools/curador_registro/build_cableado.py                                    NO-ENCONTRADO
data/curacion-universo/prisma-semantico-barrido2.md                         NO-ENCONTRADO
data/curacion-universo/prisma-m-apertura-barrido2.md                        NO-ENCONTRADO
```

Antecedentes que **sí** existen y se consumen como baseline, no como producto: `ledger-inspecciones-barrido2.tsv`, `reportes-inspeccion-barrido2-v1_0.tsv`, `baseline-material-barrido2.json`, `prisma-material-barrido2.md`, `lista-apertura-enlace2-2026-08-14.tsv`, `INFRAESTRUCTURA-v1_0.md`.

`grep -rln "B2-SEMANTICO" forense/encargos/` → **NO-ENCONTRADO**: este es el primero.

### 3 · Cobertura retroactiva

La fase material de BARRIDO-2 cerró el 18/ago (`PR #260`, `ADR-103`). Todos los productos semánticos de este acto nacen después del gate material; su ausencia en tablas previas no demuestra ausencia semántica, y por eso el universo se re-deriva aquí (no se hereda del relevo).

## Verificación de premisas del relevo · contra el árbol

Regla aplicada: `instrucciones-proyecto-v2_10.md` — "Quien ejecuta verifica las premisas del encargo antes de ejecutarlo. Si una premisa no se sostiene contra el archivo, se detiene y lo reporta — no la ejecuta, y no ajusta el texto para que cuadre."

| premisa del relevo | veredicto | evidencia |
|---|---|---|
| gate material cerrado (`#260`): 672/672, 1,833,802 E2, 0 err | **SATISFACE** | `baseline-material-barrido2.json`: `objetos_e2=1830985` + `exceptions.objetos_con_excepcion=2817` = **1833802**; `representaciones_e2_terminales=672` de `representaciones_fisicas=672` |
| índice E2 nuevo, "no asumas sufijo" | **SATISFACE** | el vigente es `.barrido2/private/e2-neutral-index.jsonl` (sin sufijo, 2.9 GB). `sha256` = `6e87c0347f0d0fa8736836e4ef7521b8dc6e700bb220cf07a9c494f8bf9bb79c`, **idéntico** al `e2_index_sha256` que declara el baseline. El `-v5` (2.1 GB) es el anterior |
| `MATERIAL_BUILD` vigente | **SATISFACE** | `barrido2_material.py` sha256 `a8f7a548aca68db2d12d2b450dbadac593a5a81cc2b9b3588a02a7e6ca798db7`, igual a `parsers.build_sha256` del baseline; versión `BARRIDO2-MATERIAL-1.1` |
| ledger durable 672 E2 | **SATISFACE** | `ledger-inspecciones-barrido2.tsv`: 673 líneas = 672 + cabecera |
| `FP-24` DECIDIDA; el par se adjudica citándola; `REQUIERE_DECISION_FP24` solo para regla nueva | **SATISFACE** | `firmas-pendientes.tsv` `FP-24` `estado=FIRMADA`, `firmada_en=ADR-93, PR #249`. Texto sellado: "cada objeto_evidencia conserva su fila; la gemela NO_DETERMINADO se enlaza SOLO si su objeto es evidenciable con una entrada distinta del manifiesto" |
| `FP-46` = 20 CON PAR (ENSAFI 9 · ENFIH 8 · ENBIARE 3) | **SATISFACE, con hallazgo** | los 20 reproducen exactos. Pero el universo `capa2_manifiesto=SI_O_REFERENCIADO` hoy es **22**, no 20 — ver hallazgo (a) |
| "Bloqueo real: identidad (0/39 `id_manifiesto`→payload)" | **NO SE SOSTIENE** | ver hallazgo (b) |
| `FP-56` abierta, fuera del perímetro C4-C6 | **SATISFACE** | perímetro de `FP-56` es `milpa/refutations.yaml`; este acto no toca `milpa/` |
| deriva de `main` | **clase C (§15)** | ver abajo |

### Hallazgo (a) — el universo de `FP-46` es 20, pero `SI_O_REFERENCIADO` es 22

`data/curacion-registro/relaciones.tsv` tiene hoy **199 filas** (la nota de `FP-24` se derivó contra 197). De ellas **22** son `capa2_manifiesto=SI_O_REFERENCIADO`, no 20:

- **20** son las históricas: `ENSAFI 9 · ENFIH 8 · ENBIARE 3`, necesidades `N3/N4/N10/N12/N13/N14`. Reproducidas por comando, no heredadas.
- **2** no lo son: `REL-c3e1306bb304b019d0a94e4b` y `REL-02e6e4861871631dd29048bd`, ambas `necesidad_id=N14`, cuyo `fuente_canonica_normalizada` es literalmente **`01-`** y **`02-`** — el normalizador truncó el nombre en el primer separador. Sus `fuente_nombre` reales son `01-SintesisMHB.pdf` y `02-Heredabilidad TLP MHB.pdf`; su `id_manifiesto` es `NO_DETERMINADO` y su `tipo_fuente` es `FUENTE_CANDIDATA`.

Consecuencia: el denominador de `FP-46` es **20**, y las 2 restantes reciben veredicto propio y explícito en este acto — no se cuelan en el denominador ni se descartan en silencio.

### Hallazgo (b) — el «0/39» es real, pero no describe la columna que el §18 manda unir

El relevo declara: *"Bloqueo real: identidad (0/39 `id_manifiesto`→payload) → remedio §19 PROPUESTA_CAMBIO"*. **Refutado contra el árbol, por tres superficies independientes.**

Las 19 filas de `data/lista-apertura-enlace2-2026-08-14.tsv` declaran **41 pares** (relación, `id_manifiesto`), con **21 tokens únicos**. Uno de esos tokens es el literal `NO_DETERMINADO`, que es un marcador de ausencia, no un identificador. Los **20 identificadores reales** resuelven así:

```text
contra ledger-inspecciones-barrido2.tsv  (payload_id)     20/20
contra reportes-inspeccion-barrido2-v1_0.tsv (payload_id) 20/20
contra data/manifiesto.yaml  (^ id: <token>)              20/20
```

Es decir **39/41 pares** resuelven, y los 2 que no son el mismo placeholder `NO_DETERMINADO`. La cifra "0/39" no se reproduce por ninguna vía. Las formas son homogéneas (`mex_2011_lfepie_v01_m_spss`, `za5900_v4_0_0_dta`, `116334_v1`), no hay divergencia de prefijo ni de normalización que impida el join.

**Dónde sí vale el «0/39».** En `data/curacion-registro/relaciones.tsv`, columna `id_manifiesto`, sobre las 19 filas `INDEXADO-NO-DESCARGADO`: **12 traen `NO_DETERMINADO`** y las **otras 7 apuntan al cuestionario** (`cses5_…_cuestionario` ×3, `za6980_q_mx` ×2, `za5900_q_mx` ×2) cuando lo que abre la celda es el codebook o el microdato. Ninguna de las 19 apunta al payload que la abriría: **0 de 19**.

Ese 12/7 explica el resto: `via_capa2.py` sólo promueve cuando `id_manifiesto` resuelve a un payload `COINCIDE`, así que las 12 se quedaron en `capa2/capa3 = NO_REFERENCIADO` y las 7 que citan el cuestionario sí se promovieron — y son exactamente las 7 que hacían fallar la condición de aperturas absorbidas de T23 antes de este acto.

**Efecto sobre el acto:** el §18 **no** queda bloqueado, porque la unión que ordena (§18.3, «une por identidad vigente») es la de `lista-apertura`, que resuelve 20/20. Lo que sí queda confirmado es que el remedio del §19 —`PROPUESTA_CAMBIO`, jamás edición manual— es la vía correcta, y que **no cabe en este acto**: `_apply_layer4` escribe `capa4`, nunca `id_manifiesto`. Queda declarado como sucesor con nombre propio.

### Deriva de `main` · clasificación §15

`57984b5..origin/main` = 8 commits (`ACTO COND-ATRIB`, `PR #263`). Ficheros tocados: `README.md`, `canon/estado-programa-v1_10.md`, `canon/gobernanza-v1_15.md`, `canon/modelo-decision-v4_0.md`, `forense/encargos/2026-08-18-COND-ATRIB…md`, `forense/hallazgos.md`, `forense/notas/2026-08-18-cond-atrib-confianza-generico.md`, `milpa/procedencia.yaml`.

- **No** tocó manifiesto, raíces, parser ni contrato E2 → no es clase **A**.
- **No** tocó `relaciones.tsv`, `evidencias.tsv`, `utilidad-modelo.tsv`, `bootstrap-semantico.tsv` ni N1-N33 → no es clase **B**.
- Por tanto **clase C · NO-INVALIDA**. El material se conserva íntegro; no se reejecuta un solo byte. Lo único que la deriva mueve para este acto es la cascada (conteo de ADR a 104) y la línea de condicionales medidas.

Base de arranque: se ramifica directamente de `origin/main` ya fusionado, de modo que no hay merge pendiente ni conflicto material.

### Colisión de actos · §2 / §27

`gh pr list --state open` → **`[]`**. Cero PR abiertos; ningún acto concurrente toca `data/manifiesto.yaml`, `data/curacion-registro/**`, `data/curacion-universo/**` ni `tools/curador_registro/**`. `pgrep -af "curador|olas|barrido2|semantic"` → solo el propio shell: **ninguna marca de dueño ajena viva**.

### Estado de partida de las pruebas

`python3 tests/check.py --baseline` **antes de tocar nada**: `19 FAIL · 129 WARN`, **LÍNEA BASE VERDE** contra `tests/baseline.json` (HEAD congelado `997482bbda18b52621e24909eedbed0630c7a111`). Ésta es la referencia contra la que se atribuye todo cambio de este acto.

---

## Texto verbatim del relevo

ENCARGO · B2-SEMANTICO (v2) — C4 → C5 → C6: la mitad que cierra el barrido

SHA: 57984b5 (#262) · Entorno: UBUNTU (worktree + .barrido2/ + corpus) · Modelo: Opus (1M) · Estado: VIVO Gate: COND-ATRIB cerrado y fusionado — un solo dueño por caja (los dos drivers de 24 min son de hoy). La LEY es el encargo madre: forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md, §17-§23 (§16 ya cerró) + §4 identidades · §11 cegamiento etapa-2 · §24 privacidad · §27 paros · §28 cierre. Este relevo actualiza el terreno, no la ley. Delta v1→v2: ADR base 104 · si ESTADO-SPLIT ya fusionó, estado-programa:101 es multilínea — la cascada del conteo va donde el split la dejó: derívala, no asumas :101 · FP-56 (8 refutaciones sin objeto) quedó ABIERTA por NOTAS-P3 — no bloquea nada de C4-C6 (refutaciones están fuera de tu perímetro; dilo en la nota y sigue) · si T22 marca tus archivos nuevos, el mecanismo es _T22_ARCHIVOS_CONOCIDOS (precedente #261/#262), no un freeze. 🚫 Sin --freeze · red cero en curación (unshare -Urn) · PR final borrador, jamás lo fusionas (§29).

════ ARRANQUE ════ 1 REPO: worktree; fetch; rama nueva desde origin/main; reporta ruta·log·status. 2 SHA: contra 57984b5; deriva se clasifica por §15 (A/B/C) antes de abrir nada. 3 TERRENO POST-#260, crudo: sha vigente de barrido2_material.py (=MATERIAL_BUILD) · ls .barrido2/private/t0/ · nombre y sha del índice E2 nuevo (no asumas sufijo) · ledger durable 672 E2 · baseline material recongelado. 4 REGLA DEL PKILL (obligatoria): antes de lanzar curador/driver: pgrep -af "curador|olas|barrido2|semantic" crudo y logs sin avance 60 s. Muerte de proceso = PID ausente + log detenido, nunca el exit code del kill. Todo staging con marca DUEÑO-<pid>-<fecha>; curadores la verifican antes de escribir. PARO si hay marca ajena viva. 5 ENTORNO A.2 (3 partes) + ESPEJO.

VERIFICACIÓN (re-córrela contra el árbol)
gate material CERRADO (#260): ok:true · 672/672 · 1,833,802 E2 · 0 err · rc=0        SATISFACE
adversarial §15.4: 39/39 COINCIDE contra build sellado                                SATISFACE
integrador #256: ALTA validada = estado, no abort (+pruebas)                          SATISFACE
T23 #256: inactivo; `--require-cableado` implementado                                 SATISFACE
propuestas §17 / cableado §21: NO-ENCONTRADO — son tu C4 y tu C6
las 17(+2) §18: 19 filas INDEXADO-NO-DESCARGADO; las 2 extra = M-APERTURA SIN payload,
  denominador PROPIO (#255/#260). Bloqueo real: identidad (0/39 id_manifiesto→payload)
  → remedio §19 PROPUESTA_CAMBIO, jamás edición manual                                 SATISFACE
FP-24: texto ADR-93 + dinámica ADR-95 — DECIDIDA: par se adjudica citándola
  (decision_mesa_id=FP-24/ADR-93, dependencia=NO); REQUIERE_DECISION_FP24 solo para
  regla NUEVA. FP-46 (20 CON PAR: ENSAFI 9·ENFIH 8·ENBIARE 3) SE CONSUME AQUÍ          →este acto
integrate CLI: sin literal de ruta en el código — LEE su CLI/schemas reales (§19)      🟡 verifica
PERÍMETRO

data/curacion-registro/** solo por vía §19/§20 (journal+rollback) · data/cableado-universo-v1_0.tsv (C6) · data/curacion-universo/** (lo que §21/§23 manden) · data/INFRAESTRUCTURA-v1_0.md al cierre (C6 — ejecuta FP-35) · tools/curador_registro/ solo lista ADR-95 (altas únicamente con ≥1 ALTA validada; build_cableado.py = ensamblador determinista, prohibido decidir semántica) · gobernanza (ADR ×2) · estado-programa cascada (post-split derivada; ⚠️ si :101 sigue entero: cláusula por cláusula) · tablero (FP-46; no cierres FP-26 — eso es de mesa con las ocho etapas) · notas · hallazgos (append) · encargos. NO: FP-47/48 · milpa/ · canon sustantivo · la muestra sellada. Fuera: PARA.

C4 · Propuestas — §17/§18 tal cual

Tareas → curadores etapa-2 (reciben: índice E2 completo solo-lectura, reportes durables, N1-N33, relaciones/evidencias, subconjunto M-APERTURA, reglas; no editan baseline/cableado) → propuestas-barrido2.tsv cabecera exacta §17 → supervisor (reabre evidencia; prueba propuesta↔reporte↔tarea; escribe la prueba de toda dependencia=SI). Consistencia: dependencia=SI ⇔ (requiere=SI ∧ decision=FP-24). Las 17: ninguna cierra INDEXADO con payload observado (§18.8); identidad por PROPUESTA_CAMBIO con evidencia E2. Las 2: veredicto/denominador/PRISMA propios. Las 20 (FP-46): adjudicadas con ADR-93 citado; REQUIERE_DECISION_FP24 final se deriva, puede ser 0, cero cuotas.

C5 · Integración — §19/§20

integrate_barrido2: joins/hashes/schemas → staging → journal → aplicar con rollback → releer → baseline → decisiones → segunda corrida diff cero. T21 verde antes/después. Toda ALTA a uno de los cuatro estados; high path solo con ≥1 validada, con pruebas.

C6 · Cableado y §28 completo

build_cableado.py → cableado-universo-v1_0.tsv cabecera exacta §21, sin celdas vacías → check.py --require-cableado verde (T23 despierta) → PRISMA material+semántico+M-APERTURA (§23, todo con denominador y comando) → INFRAESTRUCTURA (FP-35 ejecutada) → §28: 22 criterios, veredicto uno por uno con comando (cierre válido: …FP24-PENDIENTES=n derivado si n>0). ADR ×2 (base 104) · cascada derivada · nota · hallazgos · CONSUMIDO · PR borrador, push por fase (§25).

PAROs: los del §27 + PII real en propuestas · cegamiento roto retroactivo · baseline cambia en transacción · marca de dueño ajena · capa4 solo-a-mano. No pares por: deriva ajena de main (clasifica §15) · cero ALTAs · cero FP-24 · WARN conocidos. Auditoría: México: cero, uno por uno. Aparato: propuestas terminadas · 17+2 absorbidas · FP-46 ejecutada · §28 de 13-14 → derívalo. Y la pregunta §29 contestada con evidencia, o no cierres.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-18-B2-SEMANTICO-C4-C5-C6.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-18-b2-semantico.md, forense/notas/nota-2026-08-25-propaga-330-337.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
