# ENCARGO B2-RELEVO · recuperar BARRIDO-2 del corte de Codex y continuar desde C4

- **SHA de redacción:** `1282ae3` (origin/main, merge #247) · **Fecha:** 2026-08-17 · **Estado:** SUPERADO — materialmente, por `PR #255` (ACTO B2-V7) y `PR #260` (ACTO GATE-DURABLE-V7), 18/ago/2026.
- **Evidencia de supersesión (derivada del árbol, ACTO CONF-07-CIERRE 18/ago/2026):** este relevo pedía retomar BARRIDO-2 "desde C4" y seguir a C5/C6 en el worktree Ubuntu. Los dos actos que sí corrieron ahí lo hicieron: `forense/encargos/2026-08-18-B2-V7-generacion-v7-y-tres-cifras.md:5` declara *"CONSUMIDO — ACTO B2-V7, `PR #255` (rama `acto-b2-v7`), 18/ago/2026. Sella `ADR-98`"*, sobre el mismo worktree `/home/pc0/Modelado-Mexicano-barrido2`; y `forense/hallazgos.md` (entrada 2026-08-18) registra que *"`ACTO GATE-DURABLE-V7` cierra el eje durable y el gate material vuelve a verde tras tres generaciones rotas"* (`PR #260`, `6178bf9`). El bloqueo de C5 lo levantó además `ACTO INTEGRATE-T23` (hallazgos.md, 2026-08-18). El diagnóstico del corte que este relevo aporta se conserva: no se borra, no se relanza.
- **Entorno asignado:** LA MISMA CAJA Ubuntu/WSL2 donde corría Codex. Worktree existente
  `/home/pc0/Modelado-Mexicano-barrido2`, rama `codex/barrido-2`. **Modelo: Opus.**
- **Entorno NO asignado:** nube · checkout Windows · `/home/pc0/Modelado-Mexicano-curador` ·
  cualquier clon fresco.
- **Relación con el encargo madre:** este relevo NO reescribe el encargo de BARRIDO-2. Aquél
  sigue congelado en la rama desde `8c11c35`
  (`forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md`, 1641 líneas,
  autocontenido) y es el que rige. El relevo sólo aporta el diagnóstico del corte y lo que
  cambió bajo los pies.
- **Ejecución:** ver `forense/notas/2026-08-17-b2-relevo.md`.

## Decisiones de mesa dadas dentro del acto

Cuatro preguntas estructuradas, respondidas por mesa antes de avanzar. Procedencia declarada sin
adorno: son selecciones sobre opciones redactadas por el ejecutor, no cita verbatim de texto
libre — mismo criterio de honestidad que `ADR-86`/`ADR-88`/`ADR-90`/`A.9`.

1. **Agentes de la etapa semántica:** *"Subagentes: curadores + supervisor"*. Fiel a §11/§17 del
   encargo madre; la supervisión conserva independencia real y el expediente puede afirmarlo sin
   reserva.
2. **Alcance de C4:** *"Cobertura total: A+B+C, las 199"*. No se acota a las 17 aperturas
   absorbidas ni al subconjunto con payload declarado.
3. **Índice E2 sin nombres de variable en formatos tabulares:** *"Corregir y reejecutar las
   179"*. Es el caso A del §15 del encargo madre y `ADR-92(a)` inciso 2 ya autoriza tocar
   inspección E2.
4. **Expedientes de producción invalidados por el cambio de baseline:** *"Declarar y darle fila
   FP-38"*. No se re-firman.

---

## Texto completo del relevo, verbatim

ENCARGO B2-RELEVO · recuperar BARRIDO-2 del corte de Codex y continuar desde C4
SHA de redacción: 1282ae3 (origin/main, merge #247) · Fecha: 17/ago/2026 · Estado: VIVO
Entorno asignado: LA MISMA CAJA Ubuntu/WSL2 donde corría Codex. Worktree existente /home/pc0/Modelado-Mexicano-barrido2, rama codex/barrido-2.
Entorno NO asignado: nube · checkout Windows · /home/pc0/Modelado-Mexicano-curador · cualquier clon fresco.
Modelo: Opus. Lo mecánico ya se hizo: las 672 inspecciones están cerradas. Lo que queda —capa 4 fail-closed, integración, decisiones, idempotencia— es la parte con juicio.
⛔ LO PRIMERO, Y NO ES NEGOCIABLE: NO CLONES

El trabajo de BARRIDO-2 no está todo en el remoto. .gitignore de la rama incluye .barrido2/, y el PRISMA declara que el comando maestro depende justo de ahí:

```sh
unshare -Urn -- python3 tools/curador_registro/write_barrido2_material.py \
  --snapshot .barrido2/private/t0/snapshot-v2.json \
  --task-ledger .barrido2/private/t0/ledger-v2.tsv \
  --task-root .barrido2/tasks-v2 --staging-root .barrido2/staging-v2 \
  --private-index .barrido2/private/e2-neutral-index.jsonl ...
```

Nada de eso está en origin. Tampoco data/raw/, data/raices.local.yaml, data/secretos.local.yaml, data/catalogo_derivado.json, data/catalogo_unico.json.

Un clon fresco arranca sin el índice E2, sin el snapshot y sin staging. Codex se quedó sin cuota; la máquina no se perdió. Ve al worktree que ya existe.

§1 · DIAGNÓSTICO — cinco comandos, antes de tocar nada

Reporta las cinco salidas crudas. Si algo no cuadra, PARA y repórtalo.

1 · El worktree sigue ahí y qué tiene sin commitear.

```sh
cd /home/pc0/Modelado-Mexicano-barrido2 && pwd
git status --short --branch
git log -1 --format="%h %ci %s"
```

Esperado: rama codex/barrido-2, HEAD 93160c3. Si git status muestra archivos modificados o sin rastrear dentro del perímetro, ése es trabajo de Codex que nunca llegó al remoto — inventaríalo antes de nada y no lo borres.

2 · Lo que quedó sin empujar.

```sh
git fetch origin
git log --oneline origin/codex/barrido-2..HEAD
```

Vacío = todo empujado. No vacío = commits locales que solo existen en esta máquina.

3 · El estado gitignorado, que es el que no se recupera de ningún lado.

```sh
ls -la .barrido2/ .barrido2/private/ .barrido2/tasks-v2/ .barrido2/staging-v2/ 2>&1 | head -40
wc -l .barrido2/private/t0/ledger-v2.tsv .barrido2/private/e2-neutral-index.jsonl 2>&1
ls data/raw/ | head -3
```

Si .barrido2/ no existe, PARA. Reconstruirlo significa re-correr W0–W3 sobre 672 payloads y eso es una decisión de mesa, no un arranque.

4 · Entorno material.

```sh
echo ${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}
unshare -Urn -- true ; echo "unshare rc=$?"
ls "/home/pc0/mm-corpus/raw" | head -3
ls "/mnt/c/Users/PC0/Descargas MX" | head -3
```

Las dos raíces materiales autorizadas son ésas. Downloads y cualquier otra quedan fuera.

5 · Si Codex dejó rastro de dónde iba.

```sh
ls -lat .barrido2/ | head
find .barrido2 -name "*.log" -o -name "*progress*" -o -name "*todo*" 2>/dev/null | head
```

No lo asumas presente. Si no hay, el estado se deriva del ledger (§2) y ya.

§2 · DÓNDE SE QUEDÓ — derivado, no supuesto

Ya lo derivé contra origin/codex/barrido-2. Re-derívalo tú y compara; si difiere, manda lo tuyo.

El plan del encargo son seis commits, C1–C6 (forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md, líneas 1430–1475). Mapeo contra los seis commits empujados:

    Contenido    Commit    Estado
C1    multirraíz · identidades · E2 · offline · ledger · partición de olas · pruebas materiales    8c11c35 + 03f68ac    ✅
C2    W0 · censo · fuera-de-disco · baseline preliminar · PRISMA W0    62e67ed    ✅
C3    W1–W5 · índice E2 · reportes · excepciones · PRISMA material · baseline congelado    ec5a787    ✅
C4    merge de main · bootstrap sync · tareas semánticas · propuestas · supervisión · FP-24 derivado · M-APERTURA absorbido    2f14c92 + 93160c3    ⏸ a la mitad
C5    capa4 fail-closed · high path solo con PROPUESTA_ALTA validada · integración · decisiones · idempotencia    —    pendiente
C6    cableado final · T-CABLEADO · PRISMA total · INFRAESTRUCTURA actualizada · cierre    —    pendiente

La evidencia de que C3 cerró completo, con dato: ledger-inspecciones-barrido2.tsv tiene 672 filas, las 672 con estado_e0 = PRESENTE-INTEGRO y las 672 con grado_inspeccion = E2. Reparto de olas: W3=396 · W2=246 · W1=26 · W4=4. El PRISMA declara la partición cerrada: "W1∪W2∪W3∪W4=universo físico; intersecciones vacías; W5 sin reintentos." No hay reintentos pendientes.

La evidencia de que C6 no empezó: data/cableado-universo-v1_0.tsv no existe en la rama.

Lo que C4 tiene enfrente: data/curacion-registro/trabajo-semantico.tsv, 147 filas — BUSQUEDA_DIRIGIDA 109 · CURADURIA_FUENTE 19 · APERTURA_EXTRACCION 17 · ANALISIS_MEDICION 2.

§3 · CONTINUAR — desde el punto exacto

El encargo NO se reescribe. Está congelado en la rama desde 8c11c35, íntegro, 1641 líneas, autocontenido. Léelo de ahí (forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md), no de este documento. Este relevo solo aporta el diagnóstico y lo que cambió bajo los pies.

Arranca por lo que ya es el primer punto de C4: main avanzó otra vez. El último merge de la rama (2f14c92, 14:53) trajo main hasta antes de #246. Desde entonces entraron #246 (ACTO FUENTE-UNICA-DECISIONES: ADR-91, tablero a 37 filas, baseline recongelado a 6f78d06) y #247 (CELDA-D-COMPLEMENTO). Son 8 commits que la rama no tiene.

```sh
git fetch origin && git merge origin/main    # LOCAL, main HACIA la rama
```

Merge local, siempre. forense/hallazgos.md lleva merge=union y el botón de GitHub no lo honra del lado servidor — dos PR reales dieron conflicto falso en la interfaz y limpio en local. El editor web de conflictos está prohibido: ahí es donde se borra la entrada ajena.

⚠️ Después del merge, tests/check.py --baseline compara contra el congelado nuevo (6f78d06), no contra 408a3d1. Si sale ROJO, es lo esperable del cambio de base — decláralo, no lo recongeles. Recongelar exige ADR de mesa (ADR-76(f)) y este relevo no lo trae firmado.

Después: C4 hasta el final, luego C5, luego C6, con la regla del encargo — git push después de cada commit coherente y validado, PR borrador se mantiene borrador, nunca se fusiona.

§4 · LO QUE CAMBIÓ BAJO LOS PIES Y EL ENCARGO NO PODÍA SABER

FP-24 ya no está donde el encargo la dejó. Su §"Decisiones de mesa propagadas" punto 4 dice que sigue ABIERTA y que la dependencia se determina propuesta por propuesta. Sigue siendo cierto — verificado contra el tablero tras #246: FP-24 = ABIERTA. Pero el tablero pasó de 25 a 37 filas, y ADR-91 lo selló como fuente única de decisiones: "toda decisión pendiente tiene fila ahí o no existe". Si C4 o C5 producen una decisión pendiente, le toca fila — y firmas-pendientes.tsv ya no es perímetro ajeno en disputa, porque E-DEC cerró.

El ADR de BARRIDO-2 se numera al fusionar, no ahora. Máximo hoy: 91, cero huecos. Derívalo con la receta de T15 contra el main real del momento; T15 falla sobre huecos, no solo sobre el máximo.

M-APERTURA sigue absorbido, SUPERADO POR BARRIDO-2 · decisión de mesa 2026-08-17, con sus 17 aperturas vivas como subconjunto obligatorio post-E2. Está en el propio encargo, punto 2.

Nadie más está tocando tu perímetro. No hay ramas vivas fuera de codex/barrido-2; los dos E-DEC cerraron en #246 y CELDA-D en #247. data/** y tools/** son tuyos otra vez, sin la restricción de solo-lectura que los actos de hoy declararon.

§5 · PERÍMETRO Y REGLAS QUE NO CAMBIAN

Rigen las del encargo congelado, sin ampliar. Las tres que más cuestan si se olvidan:

Privacidad: límite durable de 160 caracteres, prohibición de valores individuales y PII, [REDACTADO-PRIVACIDAD], preservación de filas y estado.
Aislamiento: todo proceso que abre, indexa, caracteriza o cura material corre bajo unshare -Urn. Git y GitHub quedan fuera del namespace.
No empujes staging ni datos sensibles. .barrido2/ es local por diseño y así se queda.

Antes de cada commit: git diff · pruebas relevantes · privacidad · perímetro · git diff --check.

§6 · Cierre del relevo

Nota propia en forense/notas/2026-08-17-b2-relevo.md con las cinco salidas del diagnóstico crudas · una línea en forense/hallazgos.md · este encargo archivado en forense/encargos/ (A.3) · jamás te auto-fusionas.

Contadores del programa que mueve este relevo: 0. El relevo no mide; devuelve el acto a la vía.

Anexo · El hallazgo que este corte deja, y vale registrarlo

El estado material de un acto de barrido vive fuera de git por diseño, y eso lo hace irrecuperable si se pierde la máquina. .barrido2/ está gitignorado con razón —es staging y contiene material sin curar— pero significa que 672 inspecciones E2 dependen de un directorio que ningún remoto tiene. El corte de cuota de Codex no lo tocó; un disco sí lo habría hecho.

No propongo instrumentar nada: por la regla de señal, una salvaguarda que nadie pidió se paga en sesiones que no midieron. Pero es un hecho medido y merece su línea en forense/hallazgos.md, para que la próxima mesa que diseñe un acto material decida con él a la vista.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-17-B2-RELEVO-recuperar-barrido2-desde-c4.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-18-sello-conf07-y-rotulos.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
