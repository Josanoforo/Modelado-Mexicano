# ACTO CONF-07-CIERRE — sellar la partición ya ejecutada de `§3.7` + higiene de cinco rótulos

**Encargo:** `forense/encargos/2026-08-18-CONF-07-CIERRE.md` · **SHA declarado:** `57984b5` (`PR #262`)
**Entorno:** NUBE, repo-only · **Modelo:** Opus 5 · **Rama:** `claude/conf-07-cierre-partition-labels-lfu6k7`
**Sello:** `ADR-106` · **PR:** `#265` · **Firma de mesa, verbatim:** *"Adopto"*

---

## §0 · Arranque — los cinco, con comando

1. **REPO.** Clon en `/home/user/Modelado-Mexicano`, **no superficial** (`git merge-base --is-ancestor 57984b5 HEAD` → cierto; la historia alcanza a `57984b5`, tres semanas atrás). `main` local refrescada con `git fetch origin main` **antes** de cualquier edición.
2. **SHA.** `57984b5` = *"Merge pull request #262 from Josanoforo/claude/sello-ficha-g3-coeficiente-tytshy"*, y **es ancestro de `HEAD`**. `main` avanzó a `f3d3f95` (`PR #263`, `COND-ATRIB`) mientras el encargo se redactaba — **no es PARO**, se re-derivó todo por contenido; la deriva material se registra en §1 y §3 (el máximo de ADR pasó de 104 a 105).
3. **`data/raw`.** Este acto **no abre microdato**: repo-only. Se salta.
4. **FIRMA DE ENTORNO, A.2 — las tres partes, no dos.**
   - `echo ${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE}` → `cloud_default`
   - sonda de red (`curl -s -o /dev/null -w "%{http_code}" https://api.github.com/`, **nunca `curl -I`**) → `200`
   - `ls data/raw/ 2>/dev/null | head -1` → **vacío**. Corpus compartido **NO montado**. Coherente: el acto no lo necesita. Asignación de entorno correcta.
5. **ESPEJO.** Prohibido. Toda cifra de abajo sale del clon, con su comando a la vista.

---

## §1 · Verificación de existencia — re-corrida, no heredada

| Fila del encargo | Veredicto re-derivado | Comando / cita |
|---|---|---|
| partición hecha | **EXISTE-SATISFACE** | `modelo-decision:437` verbatim *"se parte en dos (conf.07)"*; tiers por regla en `§3.7` |
| tiers `5F·1H·2MF·3M` | **NO SATISFACE — cifra del encargo corregida** | derivado bullet por bullet: **3F · 3M · 2MF · 1H** (9 reglas). El "5" es artefacto de `grep -o`: el bullet 7 lleva **dos `[FUERTE]` en prosa histórica**, no como tier. Coincide con `modelo-decision:664` (*"§3.7 **3**"*) |
| conf.08 | **EXISTE-SATISFACE** | `glosario:322` *"✅ Corregido en `modelo v2.3` el 28/jul"* |
| fila conf.07 | **EXISTE-NO-SATISFACE** | `glosario:323` *"⚠️ Abierto — nuevo en v5.1"* → resuelta en este acto |
| deudas §15 | **A DERIVAR → derivada** | `grep -n "conf\.07" canon/glosario-v5_6.md` → `:399` (la re-derivada por `#259`) **y `:406`** — la deuda estaba **duplicada** desde v5.1. Hallazgo colateral |
| ADR que la selle | **NO-ENCONTRADO — confirmado** | `grep "conf.07" gobernanza` → sólo `:2048`, una **fila de tabla** que la da por resuelta *sin número de ADR*. Ningún ADR la sella |
| requisito de salida | **NO-ENCONTRADO → verificado aquí, SATISFECHO** | ver §2 |
| rótulos C0 | **EXISTE-NO-SATISFACE — los cinco `VIVO`** | `grep -rln "Estado.*VIVO" forense/encargos` |

**ADR máximo, primera derivación** (contra `origin/main = f3d3f95`):
`grep -o "^\*\*ADR-[0-9]\+" canon/gobernanza-v1_15.md | grep -o "[0-9]\+" | sort -n` → **105 únicos, máximo 105, sin huecos, sin duplicados**. El encargo declaraba 104; `ADR-105` entró con `PR #263`. Este acto sella el **106**.

**`ESTADO-SPLIT`**, al arrancar: `forense/encargos/2026-08-18-ESTADO-SPLIT.md:5` decía **`VIVO`** — no había fusionado. La cascada se escribió, por tanto, **cláusula por cláusula dentro de `:101`**. ⚠️ **Esto cambió a medio acto y se rehízo — ver §7.bis.**

---

## §2 · C1 · El requisito de salida — tabla completa

Barrido: `grep -rn "3\.7" canon corpus forense milpa | grep -v "v3\.7"`. Se descartan por inspección los `3.7` que son **numeración interna de otro documento** (`hitoD-R1_3-especificacion:91`, `hitoE-campana:1157` que es `§13.7`, `notas/2026-08-12-acto-o:105`, `notas/…enut-paso1:60,123`, `RONDA1-motor-adaptativo:23`) y los decimales de cifras en `corpus/reports/` y en salidas de medición.

Clases del encargo: **(a)** regla partida con tier propio → OK · **(b)** *"§3.7 `[FUERTE]`"* en bloque → corregir con el tier de la mitad citada · **(c)** ficha del Hito D con tier dependiente del empaquetado → **PARA** (`ADR-60(b)`).

| # | Sitio | Qué dice | Clase | Acción |
|---|---|---|---|---|
| 1 | `glosario:23` | changelog v5.1: abre `conf.07` por el empaquetado | (a) | ninguna — es el acta de apertura |
| 2 | `glosario:184` | §8: *"Transferencia directa universal → conserva autonomía de voto \| **Fuerte**"* | **(a)** | ninguna — **es la mitad, con su tier** |
| 3 | `glosario:322` | fila `conf.08`, cita el `PORQUE` de la mitad de autonomía | (a) | ninguna — cita el defecto **como defecto** |
| 4 | `glosario:323` | fila `conf.07`, *"⚠️ Abierto"* | — | **resuelta** (`ADR-106`) |
| 5 | `glosario:399` / `:406` | deuda §15, **duplicada** | — | **ambas cerradas**, re-derivadas desde §11 |
| 6 | `modelo:34` | cambio 32, `R7.1` deja de ser predicción histórica | (a) | fuera de perímetro (`modelo-decision` no se toca) |
| 7 | `modelo:92` | cambio 10, *"§3.7 transferencia directa: HIPÓTESIS → FUERTE"* | (a-hist) | fuera de perímetro; ya anotado por `modelo:767` |
| 8 | `modelo:437` / `:664` / `:767` | la partición, la distribución de 20 `[FUERTE]`, el aviso | (a) | fuera de perímetro — **son la evidencia que este ADR cita** |
| 9 | `gobernanza:246` | `ADR-33`, prohíbe la diagonal, motivado por `§3.7` | (a) | ninguna |
| 10 | `gobernanza:2048` | fila `conf.07`, resuelta **sin ADR** | — | **gana su `ADR-106`** |
| 11 | **`hitoD-preregistro-v2_0.md:166`** | `R7.3 · Transferencia sin monitoreo → conserva autonomía del voto` **`[FUERTE]`**, con P-02 y P-03 | **(a)** | **ninguna — aquí se decide el requisito de salida, y lo SATISFACE**: cita la mitad, no el paquete |
| 12 | `cruce-catalogo-fichas-v2_0.md:83` | tabla `§3.7`, filas `R7.1`–`R7.5` por ficha | (a) | ninguna |
| 13 | `cobertura-motor.md:58-66` | nueve `id` de `§3.7`, **cada uno con su tier** (`[FUERTE]`, `[MEDIA-FUERTE]`, `[MEDIA]`, `[HIPÓTESIS]`) | **(a)** | ninguna — es la partición ya cableada |
| 14 | **`prompts-verticales-validacion.md:101-102`** | plantilla de Ronda 4, **en uso**: empaqueta las dos mitades en una línea bajo *"hipótesis del modelo, §3.7"*, y repite *"sin monitoreo **ni broker**"* | **(b)** | **CORREGIDA** — cada mitad con su tier; broker como en `modelo v2.3` |
| 15 | `corrida-refutaciones.md:100` / `:129` | 27/jul: la mitad de autonomía *"está en `[HIPÓTESIS]`"*; recomendación 5, *"Corregir el tier"* | (a-fósil) | **ninguna — registro fechado, verdadero en su fecha**; su recomendación 5 es lo que ejecutó el cambio 10 |
| 16 | `barrido-propagacion-forense:65` / `:75` | diagnóstico P-02/P-03 sobre el motor de entonces | (a-fósil) | ninguna — absorbido por `v2.4` |
| 17 | `hallazgos.md:42` / `:56` | anomalías de `id` en `§3.7` | (a-fósil) | ninguna |
| 18 | `notas/2026-07-31-inventario-segmentacion:321,356` · `notas/…identificabilidad-perfiles:37` | `§3.7` como dominio de cobertura | (a) | ninguna |
| 19 | `milpa/milpa-spec-v0_2.md:240` · `milpa/procedencia.yaml:674` | citan `modelo §3.7` (P-02, confusión de denuncia) | (a) | **fuera de perímetro** — `milpa/` no se toca |

**Casos de clase (c): CERO.** Ninguna ficha del Hito D tiene tier dependiente del empaquetado — `R7.3` **es** la mitad `[FUERTE]`. Por tanto **cero PARA por `ADR-60(b)`**: en este acto no se tocó ningún veredicto ni ningún perímetro.
**Casos de clase (b): UNO**, corregido (#14).

### `conf.08` — no se reabre, pero tenía una fuga

`grep -rn "ni broker"` → 7 sitios. Cinco son legítimos (`glosario:40`, `:184`, `:322` citan el defecto como defecto; `modelo:499` es la regla de *turnout buying*, que **sí** nombra al broker correctamente). El sexto era `prompts-verticales:102` — **corregido aquí**. Los dos últimos viven en `corpus/`:

- `corpus/forense/Validación_Forense_del_Clientelismo_Electoral_en_México…:121` — *"REGLA 2 — «Las transferencias directas universales se viven como derecho/gratitud al líder pero SIN mo…»"*
- `corpus/reports/Psicología_Política_y_Comportamiento_Cívico…:260`

**PARA declarado**: `corpus/` está fuera del perímetro del acto y es base de evidencia fechada; retocarlo es decisión de mesa. Queda como **`FP-57`**.

---

## §3 · C0 · Los cinco rótulos — evidencia citada, cero ejecución

Sólo se tocó el **bloque de `Estado`** de cada archivo. Ni una línea del cuerpo.

| Encargo | Rótulo | Evidencia derivada del árbol |
|---|---|---|
| `2026-08-17-EA10-a10-estampa.md` | **`CONSUMIDO` — `PR #242`** (`ea076a5`) | El entregable rige: `instrucciones-proyecto-v2_10.md:366` abre `### A.10 · Estampa de universo [NUEVO v2.10]`; `gobernanza:1173` registra `ADR-79(e)`, firma verbatim *"comitteemos el texto."*. `v2_9` no se borró, como pedía el protocolo de renombre-por-versión |
| `2026-08-17-B2-RELEVO-recuperar-barrido2-desde-c4.md` | **`SUPERADO` — `PR #255` + `PR #260`** | Pedía retomar BARRIDO-2 "desde C4" en el worktree Ubuntu. `encargos/2026-08-18-B2-V7…:5` declara *"CONSUMIDO — ACTO B2-V7, `PR #255` … Sella `ADR-98`"* sobre **ese mismo worktree**; `hallazgos.md` (18/ago) registra que *"`ACTO GATE-DURABLE-V7` cierra el eje durable y el gate material vuelve a verde"* (`PR #260`). C5 lo desbloqueó además `INTEGRATE-T23`. El diagnóstico del corte se conserva |
| `2026-08-17-EDEC-fuente-unica-decisiones.md` | **`CONSUMIDO` — `PR #246`** (`88adeb2`), sella `ADR-91` | `git log --all --grep="FUENTE-UNICA"` → `872c206` (*"ADR-91 sella el tablero como fuente unica … las 13 firmas de mesa del 17/ago"*), `6947992` (`FP-27..FP-37`), `5c8c806`, `6f78d06` |
| `2026-08-17-EHIG-higiene-vivos.md` | **`CONSUMIDO` — `PR #243`** (`4c9da5b`, 20 archivos) | El propio encargo lo pedía: *"Marcar `CONSUMIDO` con el PR que fusione este acto"* — **y el acto que fusionó nunca volvió a hacerlo**. `git merge-base --is-ancestor a9fc0a7 origin/main` → cierto; `7740015` = *"Commit 2: aplica los 17 veredictos"*; el entregable `notas/2026-08-17-higiene-vivos.md` existe |
| `2026-08-17-RUTA-SELLO-taxonomia.md` | **`CONSUMIDO` — `PR #245`** (`b653bb4`), sella `ADR-89` | `gobernanza:1455` verbatim: *"ADR-89 · Sella como canon la taxonomía RUTA-A/RUTA-I/RUTA-C/SIN-RUTA … y `FP-13` pasa a `FIRMADA`"*, con la firma `ADR-79(f)` *"sellémosla."*. El gate de arranque (`v2_10` en `origin/main`) se cumplió: `#242` antes de `#245`. La reserva `VENCIBLE EN ALCANCE al cierre de BARRIDO-2` es del ADR, no pendiente del encargo |

**Ninguno de los cinco se ejecutó, relanzó ni borró.** `E-DEC`, `E-HIG` y `RUTA-SELLO` sólo se rotulan. Ninguno resultó "genuinamente vivo": los cinco tenían evidencia de destino en el árbol, así que ninguno se dejó `VIVO` con razón fechada y ninguno abrió fila por esta vía.

**La ironía, registrada como hallazgo:** el encargo `E-HIG` fue *"reconciliar el estado de los encargos archivados contra el árbol"* — y **su propio rótulo quedó rancio**. El vigía no lo ve porque el defecto vive en la línea que el vigía usa como fuente.

---

## §4 · Auditoría de contadores de México

**Cero.** Ningún contador de medición sobre México se mueve: este acto no mide nada, no re-tieriza ninguna mitad, no toca `milpa/procedencia.yaml`, y el perímetro de 20 reglas `[FUERTE]` sigue en 20 (`modelo-decision:437` lo declara explícito y no se editó).

---

## §5 · Perímetro tocado

`canon/glosario-v5_6.md` (fila `conf.07` §11, dos líneas de §15) · `canon/gobernanza-v1_15.md` (`ADR-106` + fila `conf.07`) · `canon/estado-programa-v1_10.md` (**sólo** cascada de conteo, `:27` y `:101`) · `forense/encargos/` (**sólo** bloques de `Estado` de cinco archivos + el propio encargo archivado, A.3) · `forense/prompts-verticales-validacion.md` (la corrección (b) autorizada por el encargo) · `forense/firmas-pendientes.tsv` (`FP-57`) · esta nota · `forense/hallazgos.md`.

**NO se tocó:** `canon/modelo-decision-v4_0.md` · `forense/hitoD-*` · `milpa/` · `corpus/` · `data/` · `tools/`.

---

## §6 · Suite de verificación — antes y después, con la corrida a la vista

Línea base medida en el clon **antes de editar nada**, contra `57984b5` y contra `f3d3f95` (`origin/main`): **19 FAIL · 129 WARN**, idéntica en ambos.

Tras el acto, tres vigías se dispararon y los tres eran **defectos reales de este acto**, no ruido:

| Vigía | Qué dijo | Resolución |
|---|---|---|
| `T15` | *"`canon/gobernanza-v1_15.md:2` cita 105 ADR; gobernanza tiene 106 únicos"* | **Corregido**: la cabecera del archivo es un tercer sitio de conteo que la cascada del encargo no nombraba. Ahora dice 106 |
| `T02` | *"nombre normalizado colisiona: `forense/notas/2026-08-18-conf-07-cierre.md` · `forense/encargos/2026-08-18-CONF-07-CIERRE.md`"* | **Corregido**: la nota se renombró a `forense/notas/2026-08-18-sello-conf07-y-rotulos.md` y las referencias se actualizaron. `ADR-36`: nota y encargo del mismo acto no pueden compartir nombre normalizado |
| `T16` | *"`:129` declara 129 WARN; la corrida real da 130"* y *"`:221` declara 19 FAIL · 129 WARN; la real da 19 FAIL · 130"* | **Recifrado, no silenciado**: el WARN nuevo es de `T22`/T-FIRMAS por la fila `FP-57`. **El vigía imprime toda fila `ABIERTA`: abrir una fila *es* el WARN.** Comportamiento correcto; `estado-programa:129` y `:221` recifrados a **19 FAIL · 130 WARN** |

**Cierre: 19 FAIL · 130 WARN.** FAIL **sin cambio** contra la línea base; el único WARN nuevo es el que `FP-57` debe producir por diseño. Cero recongelados de `tests/baseline.json` — el criterio de `FP-51` (*"un recongelado no es la vía rutinaria al verde"*) no se puso a prueba porque no hizo falta.

**Segunda derivación del conteo de ADR, al cierre:** `origin/main` **no se movió** (sigue `f3d3f95`); el archivo editado da **106 únicos, máximo 106, sin huecos ni duplicados**, y `git show origin/main:canon/gobernanza-v1_15.md` sigue en **105**. **La colisión de ADR que la ola 1 hacía esperar no ocurrió**: nadie más tomó el 106.

---

## §7 · Acta de cierre — el acto en una página

*Reporte de cierre tal como se entregó a dirección, incorporado al expediente para que no viva sólo en la conversación.*

**Firma A.2, tres partes:** `cloud_default` · sonda `200` · `data/raw` **no montado** (`ls` vacío) → repo-only correcto, no se abrió microdato.

**Dos cifras del encargo las desmintió el clon** — corregidas en el sello, no heredadas:

- ADR máximo era **105**, no 104: `ADR-105` entró con `PR #263` mientras el encargo se redactaba. Este acto sella el **106**.
- Tiers de `§3.7`: **3F · 3M · 2MF · 1H**, no `5F·1H·2MF·3M`. El `5` es artefacto de `grep`: el bullet 7 lleva dos `[FUERTE]` en prosa histórica que no son tiers. Coincide exacto con `modelo-decision:664` (*"§3.7 **3**"*).

**C0 — cinco rótulos, evidencia citada, cero ejecución.** `E-A10` → CONSUMIDO `#242` (A.10 vive en `instrucciones-proyecto-v2_10.md:366`) · `B2-RELEVO` → SUPERADO por `#255`/`#260` · `E-DEC` → CONSUMIDO `#246` (`ADR-91`) · `E-HIG` → CONSUMIDO `#243` · `RUTA-SELLO` → CONSUMIDO `#245` (`ADR-89`). Ninguno resultó genuinamente vivo. Sólo bloques de `Estado`.

**C1 — el entregable duro: el requisito de salida está SATISFECHO.** 19 sitios clasificados (§2). `hitoD-preregistro:166` cita `R7.3`, **la mitad `[FUERTE]`**, no el paquete → **cero casos de clase (c), cero PARA por `ADR-60(b)`, ningún veredicto tocado**. Un solo texto vivo con el defecto (`prompts-verticales:101-102`), corregido; el resto son fósiles fechados que no se retocan.

**C2/C3.** `ADR-106` sella la partición ya ejecutada (firma de mesa *"Adopto"*) · `conf.07` resuelta en `glosario §11` y en `gobernanza` · `§15` re-derivada desde §11 · cascada `estado-programa:27`/`:101` cláusula por cláusula (`ESTADO-SPLIT` sigue VIVO, no fusionó) · `FP-57` por los dos sitios de `corpus/` con el *"ni broker"* retirado (PARA, fuera de perímetro). **Contadores de medición sobre México: cero se mueven.**

### Las tres cosas que este acto deja dichas

1. **La deuda estaba escrita dos veces.** `glosario §15` llevaba `conf.07` en `:399` **y** en `:406`, duplicada desde v5.1, invisible a toda auditoría. La delató **re-derivar** la lista desde §11 en vez de leerla.
2. **`E-HIG` dejó rancio su propio rótulo** — el encargo cuyo objeto era reconciliar rótulos contra el árbol. Su cuerpo decía *"marcar `CONSUMIDO` con el PR que fusione este acto"*, y esa instrucción es **estructuralmente inejecutable**: cuando el PR existe, el acto ya terminó. El rótulo lo tiene que poner el siguiente.
3. **Tres vigías atraparon tres defectos míos, y los tres eran reales**: `T15` (la cabecera de `gobernanza` es un tercer sitio de conteo que la cascada del encargo no nombraba), `T02` (nota y encargo colisionaban en nombre normalizado), `T16` (recifrado 129→130 WARN). Línea base **19 FAIL · 129 WARN**; cierre **19 FAIL · 130 WARN** — FAIL sin cambio, y el único WARN nuevo es `T-FIRMAS` imprimiendo `FP-57`, que es lo que debe hacer. **Cero recongelados de `tests/baseline.json`.**

---

## §7.bis · La contingencia del encargo ocurrió — fusión de `ESTADO-SPLIT` (`PR #264`)

El encargo la nombraba textualmente: *"`estado-programa:101` cláusula por cláusula **salvo que ESTADO-SPLIT ya haya fusionado** (entonces la cascada va donde el split la dejó — derívalo)"*. Al arrancar el acto, `ESTADO-SPLIT` estaba `VIVO`. **Fusionó mientras este acto corría** (`PR #264`, `c8cd649`), y `PR #265` quedó `mergeable_state: dirty`.

**Fusión local de `origin/main`, tres conflictos, los tres resueltos tomando `origin/main` como base y reaplicando encima:**

| Conflicto | Qué chocó | Resolución |
|---|---|---|
| `:101` (la narrativa de `L0`) | El split la partió en **66 cláusulas, una por línea**; mi cascada era una cláusula **dentro** de la línea única | Se toma la estructura del split y **se rehace la cascada como cláusula propia** — `- a 106 después, con ADR-106…`. Detalle de forma: `:101` abre un paréntesis en itálicas `*(` y **la última cláusula lo cierra** con `)*`; al insertarse, la 105 pasa a terminar en `;` y la 106 asume el cierre |
| `:196` (T03/WARN) | `ESTADO-SPLIT` recifró 129→**128** (ejecuta `FP-48`, −1); este acto recifró 129→**130** (abre `FP-57`, +1) | **Ninguno de los dos lados era correcto.** Re-derivado de la corrida real sobre el árbol fusionado: **129**. Aritmética limpia: 129 − 1 (`FP-48`) + 1 (`FP-57`) = 129 |
| `:288` (suite verificada) | mismo choque | idem — **19 FAIL · 129 WARN** |

**Conteo de ADR: sin colisión.** `ESTADO-SPLIT` no sella ADR. Tercera derivación, sobre el árbol ya fusionado: **106 únicos, máximo 106, sin huecos ni duplicados**. El `106` se mantiene.

**El resto de la fusión entró limpio** — incluidos `canon/glosario-v5_6.md`, `canon/gobernanza-v1_15.md`, `forense/hallazgos.md` (que lleva `merge=union`) y los cinco encargos rotulados por `C0`. `FP-48` conserva el estado que le dejó `ESTADO-SPLIT` (`FIRMADA`, ejecutada); `FP-57` sigue `ABIERTA`.

**Lo que este episodio deja dicho:** el encargo **acertó al escribir la contingencia como rama explícita** en vez de asumir un orden de fusión. El costo de que ocurriera fue una fusión local y un recifrado — no una re-derivación del acto. *Un encargo que nombra la bifurcación que puede abrirse bajo sus pies convierte una colisión en un trámite.* Corolario menos cómodo: **el WARN correcto no estaba en ninguno de los dos lados**. Dos actos concurrentes, cada uno con su cifra derivada correctamente de **su** árbol, producen dos cifras y ambas quedan mal al fusionar. La cifra sólo existe después de la fusión, y hay que volver a correr la suite para tenerla.
