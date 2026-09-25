---
description: Ejecuta el Bloque D (ARRANQUE + COMPUERTA + 0-bis A.3 + EJECUCIÓN + CIERRE en cascada) sobre un encargo de forense/encargos/. Uso — /acto forense/encargos/<archivo>.md
argument-hint: <ruta al encargo, en forense/encargos/>
---

# `/acto` — el Bloque D se ejecuta, no se transcribe

Sellada por `ADR-237` (`ACTO MAESTRA32-E19 · SELLA-CAMINO-1`, 31/ago/2026,
D-10 de `instrucciones-proyecto-v2_12.md`). Esta skill vive en el repo,
versionada — no hay copia en el proyecto de Claude que sincronizar (la
clase de desfase que A.9 vigila no le aplica). El texto verbatim del
ARRANQUE vive una sola vez, aquí; los encargos la invocan.

El argumento (`$ARGUMENTS`) es la ruta al archivo del encargo dentro de
`forense/encargos/`. Si el archivo todavía no existe en el repo pero el
operador lo pegó en el mensaje que invoca esta skill, el paso 3 (0-bis
A.3) es el que lo escribe — no un prerrequisito de este primer párrafo.

Ejecuta, en este orden, los cuatro bloques de abajo. Cada uno es
instrucción ejecutable para esta sesión, no prosa de referencia.

---

## 1 · ARRANQUE — hazlo antes de leer el resto del encargo

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas.
Encontrar que el terreno no es el que el encargo supone es entregable,
no interrupción — pero qué hacer con ese hallazgo lo decide la sección
4: si toca qué se mide o una firma de mesa, PARA y repórtalo; si es
logística (main movido, `data/raw` sin enlazar, un clon superficial) y
el objetivo sigue alcanzable, resuélvelo, síguele y decláralo.

0 · GUARD DE ARRANQUE — cuatro comprobaciones, antes de crear la rama
    (`ACTO GEN2-E3 · AUTOMATIZA-GEN2-1`, 7/sep/2026, plan v2.0 §8 Fase I).
    Las cuatro son mecánicas: se corren, se pegan crudas, y ninguna se
    sustituye por "lo miré".

    **0.a · BASE AL DÍA.** `git fetch --prune`, y luego confirma que tu
    base es el `HEAD` de `origin/main`:
    ```
    git fetch --prune
    git rev-list --count HEAD..origin/main
    ```
    Si el conteo **no** es 0: **no es PARO** — `git merge origin/main`
    **antes de nada**, y reporta la diferencia. Arrancar sobre una base
    atrasada y descubrirlo al cerrar cuesta el acto entero; descubrirlo
    aquí cuesta un merge.

    **0.b · ÁRBOL LIMPIO.** `git status --porcelain` vacío antes del
    0-bis. Si no lo está, resuélvelo (commit, stash o descarte
    deliberado) y dilo — con la salvedad D-d de abajo: nunca
    `git reset --hard` con `data/manifiesto-staging.yaml` modificado.

    **0.c · DUPLICADO — el mismo rótulo corriendo dos veces.** El rótulo
    es el identificador del encargo/acto (p. ej. `MAESTRA38-N14`,
    `GEN2-E3`) o el nombre de rama que ibas a usar. Se busca en **tres**
    sitios, no en uno:
    ```
    git ls-remote --heads origin | grep -i "<rótulo>"     # rama remota
    git worktree list                                      # worktree local
    ```
    más los **PR abiertos** (por el tool de GitHub disponible, o
    `gh pr list --search "<rótulo>" --state open` donde exista `gh`).
    Cualquiera de los tres con coincidencia → **PARA / RESUELVE
    DUPLICADO** antes del 0-bis: reporta qué encontraste y termina con
    cero commits, o resuelve el duplicado explícitamente (retomar esa
    rama, cerrar el PR muerto, borrar el worktree olvidado) y dilo. Ya
    hay una sesión corriendo esto y dos sesiones sobre el mismo rótulo
    producen dos ADR con el mismo número. Buscar solo la rama remota
    **no** basta: un worktree olvidado o un PR abierto sobre una rama ya
    borrada del remoto son el mismo defecto y no aparecen ahí.

    **0.d · HIGIENE, en modo reporte.** Pega la salida cruda de:
    ```
    python3 tools/limpia_arbol.py --reporta
    ```
    (worktrees vivos · ramas locales ya fusionadas y vivas · cuántos
    commits detrás está la base). **Solo reporta** — el `--aplica` que
    borra es `E4`/Fase IV y hoy sale con código 2; borrar un worktree o
    una rama no se decide desde aquí.

    Pasadas las cuatro: crea la rama y de inmediato
    `git push -u origin <rama>` con el 0-bis (aunque no haya más commits
    todavía), para que el rótulo sea visible a cualquier segunda sesión
    desde el primer minuto.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no
    haya ninguno, y si clonas, dilo.
    Reporta:  ruta absoluta  ·  `git log -1 --format="%h %s"`  ·  `git status`
    Si clonas en la nube: clon parcial por la receta de `docs/sesiones.md` §1
    (`GEN2-TUBERIA-RENDIMIENTO-1`), e instalación con `uv` (§2).
    ⚠️ No arranques desde el home. Si el cliente avisa "launched in your
    home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el
    encargo declara. Si main se movió: NO es PARO — refresca, re-deriva
    lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta
    por código; un clon fresco siempre nace sin ella. Se crea o se enlaza.
    Reporta:  existe / la enlacé a `<ruta>` / la creé.
    ⚠️ Si el worktree nace sin `data/raw` y sin `data/raices.local.yaml`,
    enlázalos desde el clon padre ANTES de evaluar cualquier compuerta —
    corrige el defecto observado en PR #522 (una compuerta evaluada contra
    un worktree sin raíz enlazada lee la raíz como vacía y falla en falso).
    ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads
    quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el
    defecto de PR #77 y no lo atrapa ningún test.
    ⚠️ D-d (`ACTO MAESTRA38-CRON-2 · REGISTRO-Y-HUELLA`, 6/sep/2026): nunca `git reset --hard` con `data/manifiesto-staging.yaml` modificado; `git stash` primero.
    ⚠️ A.8 contra la raíz, no sólo contra el manifiesto (`ADR-326`,
    `MAESTRA37-N6`). Todo acto que PIDA una descarga a mesa, o que declare
    un payload `NO-ENCONTRADO`/`AUSENTE-EN-RAIZ`, cita el último
    `forense/censo-raiz/*.txt` (fecha + línea "nuevos") además del
    manifiesto. **Un `AUSENTE-EN-RAIZ` sin censo del día es
    `NO-VERIFICADO`, no `AUSENTE`.** Si el censo lista el archivo, no se
    pide — se registra.
    ⚠️ A.8 contra medición ya corrida (`ADR-340`, `MAESTRA38-N9`, defecto
    real repetido dos veces la misma semana: `MAESTRA38-N5` clasificó dos
    reglas ya medidas como `SIN-INSTRUMENTO`; `MAESTRA38-N7` llamó
    «territorio virgen» a dos ids que `MAESTRA35-L9`/`L11` ya habían
    falsado dos días antes). Todo acto que CLASIFIQUE, PRE-REGISTRE,
    CARGUE o SELLE una regla del motor (por `id` o por `R-n` del canon)
    pega en su A.8 la salida de `python3 tools/ya_medido.py <id-de-
    regla|R-n>` — una línea de regla, no una compuerta nueva; `T-YAMEDIDO`
    (`tests/check.py`) lo exige mecánicamente para todo encargo archivado
    desde hoy que cite un id/R-n en su SPEC.

4 · ENTORNO — tres partes, no dos (A.2). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`
    describe el entorno; la sonda de red describe la red; ninguna de las
    dos describe el dato.
    - `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → esperado: `sin_variable`
    - `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/`
      (NUNCA `curl -I`)
    - Tercera parte (A.2): `ls data/raw/ 2>/dev/null | head -1` — ¿está
      montado el corpus compartido? Se espera ausente en la nube. Todo
      acto que abra microdato va a Ubuntu, sin excepción.
    Reporta los tres valores crudos. Si este acto no toca microdato ni
    red, dilo y salta este punto.
    ⚠️ Las tres partes se derivan de una sola invocación, y se pega su
    salida CRUDA (`ACTO GEN2-E3 · AUTOMATIZA-GEN2-1`, 7/sep/2026):
    ```
    python3 tools/entorno.py              # JSON + la línea
    python3 tools/entorno.py --sonda-red  # además prueba la red
    ```
    ⚠️ Fuente única con dos vías (hook `SessionStart`, `.claude/settings.json`):
    si la salida de `python3 tools/entorno.py --arranque` ya está pegada en
    el contexto de esta sesión (el hook la corrió al arrancar/reanudar),
    pégala CRUDA tal cual aquí — es la misma firma, no se re-deriva. Si no
    está disponible (sesión multi-repo donde este repo no es el que fija
    `.claude/settings.json`, o una sesión vieja sin el hook), córrela a mano:
    `python3 tools/entorno.py --arranque`. Cualquiera de las dos vías basta;
    no se pega dos veces.
    Trae `git_commit · git_status · python · dependencias materiales ·
    variables de entorno relevantes · sonda de red (opt-in) · raíces
    lógicas (`raiz_logica · configurada · config_sha256`, **nunca** la
    ruta física) · acceso a corpus con los archivos examinados (A.13).
    La sonda de red es opt-in a propósito: una sonda que nadie pidió es
    I/O que nadie declaró. La misma firma la incorpora `corrida0 run` a
    `ejecucion.json` bajo `firma_entorno`, así que el entorno del
    ARRANQUE y el de una corrida se leen con el mismo vocabulario.
    ⚠️ A.13 — Un negativo producido por un comando que no examinó
    archivos no es un negativo. Todo veredicto negativo —incluida la
    sonda de este punto— declara cuántos archivos examinó el comando que
    lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está
    versiones atrás del repo y contiene archivos que el repo nunca tuvo.
    Toda cifra sale del clon de (1), con el comando a la vista.

---

## 2 · COMPUERTA

Busca en el encargo (el argumento de esta skill) una línea que declare
`GATED a …`, `Estado: GATED a …` o `COMPUERTA: …` — las tres formas son la
MISMA cosa y tienen la MISMA consecuencia (no cumplida → cero commits); el
formato corto v2.12 escribe `COMPUERTA:` y el largo escribía `GATED a`, y
reconocer solo una de las dos formas es no compuertar el acto. Si no hay
ninguna de las tres, el encargo no está compuertado — continúa al paso 3.
`COMPUERTA: ninguna` (o `ninguna de merge`) es una declaración explícita de
que no hay compuerta: no dispara verificación.

**Rótulo ambiguo.** Si la línea `GATED a X` / `COMPUERTA: X` cita un rótulo
sin serie — `E<n>`, `C<n>`, `A<n>`, `S<n>` pelado, sin el prefijo
`MAESTRA<nn>-` — la compuerta es AMBIGUA: no se resuelve por inferencia ni
por "el más reciente que calce". **PARO con cero commits**, con el texto
`rótulo ambiguo: cita MAESTRA<nn>-…`. Precedente: PR #437 resolvió `E13` a
`MAESTRA32-E13` — antes de ese PR, `E13` solo podía significar eso mismo si
alguien lo derivaba a mano; esta regla evita repetir esa derivación
implícita en cada acto.

Si hay una línea `GATED a X` / `COMPUERTA: X`:

1. `git fetch origin main` (o la rama que el encargo declare como base).
2. Verifica **por los comandos que el propio encargo declare** — nunca
   por defecto genérico — que `X` está fusionado/en el estado que el
   encargo exige contra `origin/main` real. La verificación es **por
   PRODUCTO**: el archivo o entrada concreta que el acto gateado debió
   producir (`git cat-file -e origin/main:<ruta>` o
   `git show origin/main:<ruta>`), o `git merge-base --is-ancestor`
   contra el SHA de merge que el encargo declare, o el mecanismo
   explícito que el encargo nombre. `git log --oneline origin/main |
   grep -c "X"` queda como **indicio, no como prueba**: `ADR-277` midió
   un falso positivo con este comando — el commit `bb54f99` ([COLA],
   asunto que nombra varios rótulos) hace que el `grep` cuente aciertos
   para rótulos que el commit solo menciona, no que el commit ejecutó.
3. Si la compuerta **no** se cumple: reporta con A.4/A.13 (qué se
   examinó, con qué comando, en qué fecha) y **termina con cero
   commits**. No adelantes ningún paso del acto "por si acaso" — el
   defecto que esta skill existe para dejar de pagar dos veces
   (`ADR-224`, `ADR-234`) es exactamente arrancar sin haber verificado
   la compuerta mecánicamente.
4. Si se cumple: repórtalo (comando + salida) y continúa al paso 3.

---

## 3 · 0-bis A.3

Primer commit del acto: el encargo, verbatim, en
`forense/encargos/<fecha>-<ROTULO>.md` — si el texto del encargo llegó
pegado en el mensaje que invocó esta skill y el archivo todavía no existe
en el repo, este commit es el que lo crea. Si el archivo ya existe (lo
creó un paso anterior de la misma sesión), no se re-escribe.

No se ejecuta ningún paso sustantivo del encargo antes de este commit.

**Sello del CUERPO, en este mismo commit** (`ACTO
GEN2-TUBERIA-SIDECAR-CUERPO-1`, 21/sep/2026; firmas de mesa D-a1, D-a2,
D-a3, D-a5, D-a6):

```
python3 tools/sella_sha256.py --cuerpo <encargo>
```

- **Qué cubre y cómo se normaliza (D-a1).** El sello cubre el CUERPO del
  encargo —lo que se pidió—, no lo que el ejecutor añada después. Se
  calcula sobre `N(texto)`: se quita al final todo blanco y toda línea de
  solo `---`, y se termina en exactamente un salto de línea. `N` se
  aplica IGUAL al sellar y al verificar.
- **Candidatos por hash, sin centinela (D-a2 + D-a5).** Al verificar, los
  candidatos son el prefijo anterior a CADA línea que empieza en `^## `,
  más el archivo entero; pasa si alguno, normalizado, casa. El hash
  desambigua solo: un encargo con dos líneas `## NO-CORRIDO` no obliga a
  escoger delimitador. La verificación reporta CUÁL candidato casó, y
  emite WARN —no FAIL— si lo que sigue al cuerpo sellado abre con un
  encabezado distinto de `## NO-CORRIDO` o `## CONSUMIDO` (D-16: los WARN
  se listan, no adjudican).
- **Sufijo propio (D-a3).** El sidecar se llama `X.cuerpo.sha256`.
  `sha256sum -c` no es su verificador, y el nombre lo dice. Quien los
  revisa en conjunto es `python3 tools/verifica_sidecars.py`, cableado en
  CI sobre `forense/encargos/` y `forense/notas/`.

**ESTE SELLO NO SE REGENERA NUNCA: ni al cierre, ni tras una
renumeración, ni para que un verificador pase.** Nace aquí, en el 0-bis, y
aquí se queda. Vale verbatim la advertencia del 7/sep de
`tools/sella_sha256.py`: «que el cierre reselle un archivo no vuelve
aceptable un cambio accidental en una spec». Un sello que no casa es un
hallazgo sobre el texto, no un sidecar que arreglar — se declara, y el
testigo viejo queda VENCIDO EN ALCANCE (A.10), nunca editado ni borrado.

**Adendas — archivo propio, nunca pegadas al encargo** (firma de mesa
`ADENDAS`, 21/sep/2026). Una adenda de mesa que llega con el acto ya
corriendo se archiva como `<encargo>-ADENDA-N.md`, junto a su encargo, en
forma plana, con su propio `.cuerpo.sha256`, **sellada al recibirse**. `N`
es `max+1` sobre las adendas ya archivadas de ese encargo (un solo
escritor por encargo, D-17). El encargo cita sus adendas **desde el
CIERRE, nunca desde el cuerpo**: el cuerpo no se toca ni para eso.

---

## 4 · EJECUCIÓN — premisas, latitud y paros

Lee el `MODO` de la cabecera. Si el encargo no lo trae (es anterior a
v2.15): trátalo como `RÍGIDO` si congela o ejecuta una spec con reserva,
`ABIERTO` en cualquier otro caso, y dilo.

1. **Verifica las premisas según su rótulo, antes de construir sobre
   ellas.** `[EJECUTADO]` y `[LEÍDO]`: compruébalas de pasada.
   `[EXISTE]`, `[SUPUESTO]` y `[REPORTADO]`: son tuyas de verificar —
   dirección no sabe si funcionan. Un encargo sin rótulos: trata toda
   premisa como `[SUPUESTO]`. Repite la búsqueda de «ya hecho / ya
   decidido» **por objeto** con tu acceso, que es mejor que el de
   dirección. Si está hecho, el entregable es decirlo y hacer lo que
   falte.

2. **Una premisa falsa no es, por sí sola, un PARO.**
   - Toca **qué se mide** (estimando, universo, código, umbral) o una
     **firma de mesa** → PARA y reporta. Nunca se ajusta el
     procedimiento para que cuadre.
   - Toca **logística o estado del repo** y el OBJETIVO sigue
     alcanzable → replantea, sigue, y declara en la nota qué premisa
     cayó y qué hiciste en su lugar. Si el encargo previó la rama («si
     X resulta falso, entonces Y»), tómala.
   - El OBJETIVO dejó de ser alcanzable o de tener sentido → PARO, y
     ése es el entregable.

3. **PAROS: lista cerrada.** (a) abrir, derivar o imprimir dato de una
   ola reservada fuera del código autorizado · (b) borrar, forzar
   (`-D`, `--force`, `clean`) o reescribir algo sellado · (c) adoptar, o
   mover un contador que el encargo veda · (d) cambiar estimando,
   universo, umbral, candidato o código de un procedimiento congelado ·
   (e) entorno equivocado · (f) objetivo inalcanzable. En `RÍGIDO` se
   añade (g): el código congelado no corre → no se parcha.
   **Fuera de esta lista no se para: se resuelve o se pregunta.**

4. **Latitud.** Decides tú, y lo dices: el cómo, el orden, las
   herramientas, los nombres; remover obstáculos reversibles y baratos
   (enlazar `data/raw`, `git fetch --unshallow`, instalar una
   dependencia, regenerar un derivado por comando, corregir una cita
   rota); arreglar un defecto adyacente de ≤ 10 líneas que te impide
   terminar. **Preguntas a mesa** —con 2 o 3 opciones y tu
   recomendación— cuando una bifurcación no prevista cambia qué se
   entrega, **y sigues con lo demás mientras contesta**: una pregunta no
   es un PARO. La respuesta de mesa se copia verbatim a la nota.

5. **Perímetro de cierre — permanente, aunque el encargo no lo
   enumere.** Cablear en CI el test propio (hoy: `tools/ci_guardias.py
   --censo`, job `guardias`) · publicar en la vista las filas propias y
   su asiento de replay (E.7) · registrar en
   `data/INFRAESTRUCTURA-v1_0.md` la tabla propia · la cascada de la sección
   5 · hallazgos, NC y FP propios. `FUERA-DE-PERÍMETRO` como razón de
   una NC queda para lo que de verdad es de otro acto; si la usas, di de
   cuál.

6. **Compuertas.** Cada una declara qué protege: abrir dato · congelar
   spec · adoptar · borrar. Una "compuerta" que no proteja una de esas
   cuatro es un orden sugerido: puedes adelantar lo que no dependa de
   ella, y lo dices.

---

## 5 · CIERRE — cascada estándar

Al terminar el objeto del encargo (o al cerrar por hallazgo, si el acto
no llega a arrancar), en el mismo commit o en el commit de cascada:

**Orden, en actos R de sesión ciega** (2/sep/2026, firma de mesa sobre
`FP-244`, `ACTO MAESTRA35-L2`, `ADR-292`): la cascada corre **después** de
commitear `corridas-R/*.json`; nunca antes — las entradas de ADR de
`canon/gobernanza-v1_15.md` citan `p` del motor verbatim, así que cerrar el
acto antes de escribir los `R` contamina la sesión que los va a producir.

1. **ADR con raíz de acto** (`ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1`,
   21/sep/2026, firma de mesa D-2 del 21/sep: «los ids de ADR, NC y FP
   pasan todos a raíz de acto; la forma se congela ya y no se renumera
   nunca más»). Forma: `ADR-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>`, `hhhh` = 4
   hex del commit de 0-bis. `python3 tools/cierre_acto.py` (Fase A,
   dry-run, nunca escribe) deriva y reporta el candidato de raíz contra
   el 0-bis ya commiteado, FP máximo/filas abiertas, el rótulo esperado y
   si ya está en `registro-rotulos.tsv`, y corre
   `tests/check.py --rapido` (P-A, ACTO GEN2-TUBERIA-CIERRE-RAPIDO-1,
   21/sep/2026: la sesión verifica en segundos, el CI juzga con la suite
   completa en el push). **Un id con raíz de acto no se
   renumera nunca.** El espacio numérico viejo (`ADR-<n>`, `max+1`) queda
   CERRADO desde este acto — ningún `ADR` existente se toca ni se
   renumera; si un id NUMÉRICO acuñado antes del cierre choca al fusionar
   (dos actos tomaron el mismo candidato numérico en vuelo), el que
   fusiona segundo **se re-acuña con raíz**, no renumera el numérico.
2. **Entrada nueva.** En `canon/gobernanza-v1_15.md` §4 (Registro de
   decisiones), con `ADR` de raíz de acto (punto 1) y el encargo citado
   (archivado por A.3, SHA de redacción) y, si aplica, el bloque **Gate
   verificado**. **Sin tocar la cabecera** `### \`gobernanza\` · ... ·
   **N ADR**` — ese contador es histórico desde P-B, abajo. Esto lo
   redacta el ejecutor — el tool no entiende semántica de ADR.
3. **L0, histórica y por fragmentos** (`ACTO
   GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1`, 21/sep/2026, P-A/P-B). La ÚNICA
   FUENTE DE ESTADO vigente es `canon/estado-programa-v1_16.md`
   (`v1_13`/`v1_12` retiradas del árbol por `T01`, ver `ADR-497`; `v1_15`
   NO retirada — `ACTO GEN2-ESTADO-V16-1`, 23/sep/2026, la deja intacta
   en el árbol por encargo explícito); su
   línea `L0` dejó de escribirse a mano y es un **puntero corto** al
   contenido histórico congelado (`canon/L0/HISTORICO.md`, hash fijado,
   guarda `T49`) más los fragmentos por acto. **La anotación de este
   acto va en `canon/L0/<ADR-raíz-de-este-acto>.md`** (archivo nuevo, uno
   por acto) — nunca en la línea `L0` compartida ni en `HISTORICO.md`.
   La vista completa (histórico + fragmentos) se obtiene por comando:
   `python3 tools/l0_vista.py`. Los TRES contadores mecánicos que antes
   reconciliaba `python3 tools/cierre_acto.py --aplica` — el conteo de la
   línea `L0`, la cabecera de `gobernanza` y la fila `gobernanza` de la
   tabla de `estado-programa` §0 — quedaron **HISTÓRICOS** al congelar
   (P-B): `--aplica` ya no los escribe (verificable con `git status`
   tras correrlo); el conteo vigente se deriva por comando
   (`python3 tools/estado_comun.py --adr-max` o
   `python3 tools/l0_vista.py --conteo`), nunca de esos tres textos.

   **`estado-programa` deja de tocarse en el cierre** (`ACTO
   GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2`, 21/sep/2026, P2; guarda `T52`).
   Medido sobre los 11 PR de primer padre anteriores a `#962` que
   modifican el archivo: además de la `L0`, un cierre seguía escribiendo
   a mano la fila `gobernanza` de la tabla §0 (11 de 11) y una línea
   `*Anotación L0 (fecha): …` nueva en §0 (6 de 11). Las dos reciben el
   mismo trato que la `L0`: las 96 anotaciones existentes y esa fila
   quedan **HISTÓRICAS** con su hash fijado (`T52`), y la anotación del
   acto **va sólo** a `canon/L0/<ADR-raíz>.md`. **Un cierre estándar no
   modifica `canon/estado-programa-v1_16.md`** — compruébalo con
   `git status` antes de empujar; si el archivo sale modificado, lo que
   escribiste va al fragmento.
4. **`registro-rotulos`.** `canon/registro-rotulos.tsv`: censa el rótulo
   del acto (`ESPACIO-Nn`) y cualquier token pelado nuevo que el encargo
   o las notas de cierre traigan sin prefijo (D-6/ADR-128) — deriva con
   el mismo regex que T25 usa, no a ojo.
5. **T25.** Si el archivo nuevo trae un rótulo `M`/`E` pelado (verificado
   con el regex de `tests/check.py::_T25_ROTULO_BARE`), añádelo a
   `_T25_ARCHIVOS_CONOCIDOS` con el comentario que explica de dónde sale
   cada mención — mismo patrón que el resto de la lista. Un encargo
   verbatim (A.3) nunca se edita para complacer al test.
6. **`python3 tests/check.py --rapido`** en VERDE (P-A, ACTO
   GEN2-TUBERIA-CIERRE-RAPIDO-1, 21/sep/2026: el subconjunto rápido —T02,
   T22, T25, T15, T27, T30, T34 y el verificador de sidecars, ≤15s— es lo
   que la sesión corre antes de empujar; la suite completa la corre el CI
   en el push, y **ése es el juez**. Si el CI falla: la sesión corrige y
   vuelve a empujar), o PARO-reporta con la salida cruda si el subconjunto
   mismo falla — nunca se sigue con un `FAIL` nuevo sin reportarlo primero.
7. **Anti-PR#77.** Si este acto descargó algo: verifica que los payloads
   quedaron en el corpus compartido y no solo en el worktree de esta
   sesión, antes de dar el acto por cerrado.
8. **Empuja la rama.** `git push -u origin <rama>` con la cascada de
   arriba ya cerrada en el commit (o los commits) de esta sesión.
   Excepción única: cuando el acto corre bajo `/despacha`, que ya
   conserva la propiedad del push — no lo dupliques.
9. **Abre UN PR.** Abre **UN** PR contra `main` titulado con el rótulo
   del acto y toma su número real — nunca lo inventes, nunca antes de
   que exista. `## CONSUMIDO` (paso 10) depende de este número: ningún
   paso anterior a este lo necesita, y ninguno de los siguientes lo
   sustituye por inferencia. **NO lo fusiones** — el merge es de mesa, y
   es la autorización, no un trámite del ejecutor. Excepción única:
   cuando el acto corre bajo `/despacha`, que ya hace este paso — no lo
   dupliques.
10. **`## NO-CORRIDO / RESERVAS`** (A.14, `ACTO GEN2-T8`, 8/sep/2026,
    `forense/encargos/2026-09-08-GEN2-T8-A14-CERO-RAMAS-RETROFIT.md`).
    **Precede** a `## CONSUMIDO` — se escribe en el mismo encargo
    archivado, antes de esa sección, y nunca después. **La sección de
    cierre se añade al final del encargo archivado; nada por encima de
    ella se edita.** (D-a6, 21/sep/2026: es lo que mantiene válido el
    sello de cuerpo del 0-bis — medido sobre los 56 encargos tocados del
    19 al 21/sep, cinco de los nueve sellos rotos lo fueron por la
    cascada de cierre del propio acto.) Lo que no se corrió
    se asienta, o el acto no cierra: una fila por pieza no ejecutada,
    parcial, distinta de lo pedido, o con reserva —
    "Ninguno." si de verdad no hay nada. Cada fila trae:
    - **qué** — la pieza citada, verbatim del encargo.
    - **por qué** — una de siete, sin inventar otras:
      `PARO-ENTORNO` · `PARO-PREMISA` · `FUERA-DE-PERÍMETRO` ·
      `SUSTITUIDO-POR:<acto>` · `DIFERIDO-A:<sucesor>` ·
      `NO-VERIFICABLE-AQUÍ` · `DECISIÓN-DE-MESA-PENDIENTE`.
      `FUERA-DE-PERÍMETRO` **nombra de qué otro acto es la pieza**; si no
      puedes nombrarlo, no era de otro acto y te toca a ti (D-21).
      El token va **al principio** de la razón, no en medio de la prosa
      (A.16): `tools/nc_por_razon.py` cuenta por prefijo exacto.
    - **impacto** — qué contador o consumidor no se mueve por esto.
    - **sucesor** — acto, fila FP, o `SIN-ASIGNAR` — nunca vacío.
    Un `SUSTITUIDO-POR` que no enumere qué absorbe el sustituto y qué
    queda huérfano es una fuga de deuda: dilo explícitamente en la fila,
    no lo dejes implícito. El mismo texto va, verbatim, en el cuerpo del
    PR (paso 9, plantilla `.github/pull_request_template.md`) y como filas
    `NC-NNNN` en `forense/no-corrido.tsv` con `estado = ABIERTA` (o
    `CERRADA` si este mismo acto la cierra). `tools/cierre_acto.py`
    (Fase A) reporta `NO-CORRIDO-AUSENTE` si el encargo llega a
    `## CONSUMIDO` sin esta sección, y `NC-HUÉRFANA` si una fila de
    `forense/no-corrido.tsv` no tiene sucesor resoluble — ninguno de los
    dos bloquea el commit por sí solo, pero se reporta antes de cerrar.
11. **`## CONSUMIDO`.** En un commit **posterior** sobre la misma rama,
    añade esta sección al final del encargo archivado en el paso 3,
    **después** de `## NO-CORRIDO / RESERVAS` (paso 10, nunca antes),
    citando el número real del PR del paso 9 (o el commit, si el acto no
    abre PR) que lo ejecutó, y empuja ese commit. El encargo no se borra
    ni se edita en ningún otro punto: es el registro de qué se pidió,
    para poder auditar si el ejecutor hizo lo que se le dijo. Excepción
    única: cuando el acto corre bajo `/despacha`, que ya escribe
    `## CONSUMIDO` (junto con `ESTADO`/`BITACORA`) en su propia
    secuencia — no lo dupliques.

    **Política de cero ramas** (A.14): un acto termina con su rama
    **fusionada o borrada**. Trabajo único sin PR se absorbe en `main`
    como histórico rotulado (`## HISTÓRICO — NO EJECUTADO` con origen y
    fecha) o se borra con decisión explícita; nunca se preserva como
    rama. Esto deroga, por enmienda fechada y no por reescritura, la
    variante `historico/` de `GEN2-E4` D1 y del plan v2.0 §6. Si el PR de
    este acto ya fusionó al llegar a este paso: `git push origin --delete
    <rama>` en el mismo momento en que se escribe `## CONSUMIDO`.
    `tools/limpia_arbol.py --reporta` cuenta toda rama remota sin PR
    abierto como `fuera_de_politica`.
12. **`python3 tests/check.py --rapido`** una última vez, después del
    commit del paso 10, en VERDE — el CI del push sobre este PR es el
    juez de la suite completa (P-A) — o PARO-reporta con la salida cruda,
    nunca se declara el PR listo con un `FAIL` nuevo sin reportarlo
    primero.
13. **Guard final de HEAD** (`ACTO AUTOMATIZA-2-A · BLINDA-HEAD-PR`,
    `forense/encargos/2026-09-07-AUTOMATIZA-2-A-BLINDA-HEAD-PR.md`).
    Defecto real que corrige: `PR #572` se fusionó contra un `HEAD`
    anterior al último commit de cierre — el `## CONSUMIDO` quedó fuera y
    se incorporó después vía `PR #576`. Tras el último push susceptible
    de alterar `HEAD` (el del paso 10), corre:
    ```
    python3 tools/verifica_head_remoto.py
    ```
    Sólo si reporta `PR_HEAD_SINCRONIZADO` se declara el PR listo para
    mesa. Si reporta `PR_HEAD_DESACTUALIZADO`: un `git push origin
    <rama>` más y **una** repetición del guard; si persiste
    desactualizado, o si el guard reporta `RAMA_AUSENTE_EN_ORIGIN` o
    `HEAD_REMOTO_NO_VERIFICABLE`, termina con `NO FUSIONAR` y repórtalo
    en el PR — sin loop, sin segundo PR. Excepción única: cuando el acto
    corre bajo `/despacha`, que ya conserva la propiedad de este guard en
    su propia secuencia de push/PR — no lo dupliques.

Falsador y caducidad de esta skill (D-13, `instrucciones-proyecto-v2_12.md`):
si en un mes la skill no evita ni un solo acto perdido por compuerta, o el
tamaño mediano de encargo no baja al menos 50%, o un lote deja pasar un
defecto de contenido que el formato largo habría atrapado — a juicio de
mesa, con el caso citado —, se revierte la pieza que falló y se anota.

Enmienda fechada (2/sep/2026, firma DE1, `ACTO MAESTRA34-N9 ·
PROPAGA-FIRMAS-Y-SELLOS`): D-12 (formato corto) se conserva; su meta
declarada se re-declara al valor medido por `MAESTRA34-E1` (`PR #463`)
— reducción −20.6%, no el ≤40% original — sin abrir ningún acto de
revisión de reglas operativas en adelante (los falsadores de operación
se leen en el digesto, no en actos con fecha). Registrada también en
`forense/hallazgos.md` bajo `PARA-v2.13`: `instrucciones-proyecto-v2_12.md`
no se edita acto por acto (firma de mesa, 2/sep/2026).
