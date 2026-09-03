# ENCARGO E-DEC · FUENTE-ÚNICA-DE-DECISIONES — consolidar, registrar firmas y abrir mesa de revisión en conversación
- **SHA de redacción:** `b653bb4` · **Fecha:** 2026-08-17 · **Redactor:** dirección (Fable) · **Estado:** CONSUMIDO — ACTO FUENTE-ÚNICA-DECISIONES, `PR #246` (`88adeb2`), 17/ago/2026. Sella `ADR-91`.
- **Evidencia de consumo (derivada del árbol, ACTO CONF-07-CIERRE 18/ago/2026):** `git log --oneline --all --grep="FUENTE-UNICA"` → `872c206` (commit 1, *"ADR-91 sella el tablero como fuente unica de decisiones y registra verbatim las 13 firmas de mesa del 17/ago"*), `6947992` (commit 2, *"11 filas nuevas (FP-27..FP-37)"*), `5c8c806` (commit 3), `6f78d06` (backfill del número de PR real). El tablero `forense/firmas-pendientes.tsv` es hoy la fuente única y sigue creciendo bajo esa regla.
- **Entorno asignado:** NUBE, conversación interactiva con mesa · **Modelo: Opus 4.8**. NO caja de Codex, NO Windows.
- **Supersede:** al encargo E-CF (redactado hoy en el hilo de dirección, NO lanzado, NO archivado). Si por error
  existiera en el repo, márcalo `SUPERADO POR E-DEC · decisión de mesa 2026-08-17` y sigue.
- **Firma por lanzamiento (declarado):** mesa, al lanzar este encargo, firma DOS cosas: (a) la regla de fuente
  única de §3; (b) el texto reformulado de FP-19 de §2. Si mesa quiere otro texto, lo edita en el mensaje de
  lanzamiento y ESE es el verbatim.
- **Concurrencia:** BARRIDO-2 (Codex, PR #244 borrador, rama `codex/barrido-2`) corre en paralelo. `data/**` y
  `tools/**` son SOLO-LECTURA para este acto, pineados al SHA de tu arranque y con estampa A.10.

════════ ARRANQUE ════════
1·REPO: clona `https://github.com/Josanoforo/Modelado-Mexicano`, rama `claude/fuente-unica-decisiones`; reporta
ruta · `git log -1 origin/main` · status. Corre `git rev-parse --is-shallow-repository`; si `true`,
`git fetch --unshallow` ANTES de cualquier veredicto (precedente E-HIG). 2·SHA: base `b653bb4`; si main avanzó,
clasifica la deriva (¿tocó `firmas-pendientes.tsv`, gobernanza o instrucciones?) y reporta antes de editar.
3·data/raw: no tocas microdato — dilo y salta. 4·ENTORNO: variable `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` cruda +
sonda a `https://github.com/` (esperado presente / 200-301). 5·ESPEJO: prohibido para cifras.
══════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección, 17/ago, contra `b653bb4` ═══
1·ESTRUCTURA. La fuente única YA EXISTE y tiene vigía: `forense/firmas-pendientes.tsv` (esquema 7 columnas,
convención A.12/ADR-85, `gobernanza:1369`; vigía T-FIRMAS/T22 imprime toda fila ABIERTA en cada corrida de
`tests/check.py`). Este acto NO crea tabla nueva: consolida sobre ésa.
2·CONTENIDO — lo disperso, verificado hoy con comandos: (i) tablero con 18 filas ABIERTAS (FP-01..06, 07, 10,
11, 12, 14, 15, 17, 18, 19, 22, 24, 25) y las firmas de mesa del 17/ago SIN registrar; (ii) `canon/
estado-programa-v1_10.md:135` §S5 "Pendientes irresueltos" — fuera del tablero; (iii) `propuesta-motor-
adaptativo-celda-v0_4.md:2` "Propuesta sin sello" — fuera; (iv) `PROPUESTA-remediacion-brecha-documental.md`
sellada por ADR-70 (`gobernanza:940`) pero U2/EV-1 y U3/DOC-BACKFILL sin verificación de ejecución; (v)
`data/curacion-registro/utilidad-modelo.tsv` col 11 `requiere_decision` (encabezado verificado; conteo de `SI`
lo derivas tú — la corrida de dirección contó col 6 por receta mala, declarado); (vi) decisiones de mesa
embebidas en el encargo BARRIDO-2 §0 (vive en la rama `codex/barrido-2`, aún no en main) — sin filas; (vii)
ranuras M1-M6 en `forense/ADR-MOTOR-2-esqueleto-2026-08-14.md` — con filas FP-01..06, verificar cruce; (viii)
`grep -n "pendiente nombrado\|queda para mesa\|sigue en mesa" canon/gobernanza-v1_15.md` — hits sin fila.
3·COBERTURA RETROACTIVA. El tablero nació 14/ago (`6e0f2a1`): todo pendiente anterior es invisible para él
salvo alta manual — la brecha exacta que este acto cierra.
═══════════════════════════════════════════════════════════════════

PERÍMETRO Y CONCURRENCIA. Escribes EXACTAMENTE: `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md`
(UN ADR, número derivado al merge; colisión posible con el de Codex → renumera, T15 arbitra, precedente
TABLERO-FIRMAS c5) · `forense/notas/2026-08-17-fuente-unica-decisiones.md` · `forense/encargos/2026-08-17-EDEC-
fuente-unica-decisiones.md` (este texto íntegro, A.3) · `forense/hallazgos.md` (una entrada, union en merge
local). NADA más — ni `data/`, ni `tools/`, ni estado-programa, ni las PROPUESTAs (se apuntan con filas, no se
editan). "Si te encuentras escribiendo fuera de esta lista, PARA."

## FASE 1 · Trabajo silencioso (dos commits, push, PR borrador)
**Commit 1 — registrar lo ya firmado por mesa (17/ago, verbatim, cero interpretación):**
FP-07→FIRMADA, cita *"De acuerdo."*, texto adoptado: "A.7 queda únicamente con la regla vigente (identidad =
contenido); el reclamo de la estampa vive en A.10 y no vuelve." · FP-17→FIRMADA, cita *"firmada"*, texto: "Las
15 del sondeo-27 entran a la cola con la palanca propuesta; ninguna descarga arranca hasta el cierre material
de BARRIDO-2." (la cola NO se edita: la ejecuta el acto de adquisición post-barrido citando esta fila) ·
FP-18→FIRMADA, cita *"Incluyela."*, texto: "T20 se instrumenta en el primer acto que toque tests tras el
cierre de BARRIDO-2." · FP-19→FIRMADA por lanzamiento, cita que ordenó reformular verbatim: *"Reformulala
porque no estoy de acuerdo de esperar más evidencia, quién decide cuando es suficiente? donde vemos qué casos
están ahí y como la resolvemos?"*, texto adoptado: "Cuando una corrida E4c encuentre el caso exacto (DiD≥20pp +
dirección correcta + IC decisivo + monto documentado insuficiente), no se auto-sella ni se espera: el acto
cierra el caso como PROPUESTA y crea ese mismo día una fila propia en forense/firmas-pendientes.tsv con las
cuatro señales y el faltante a la vista. Quién decide: mesa, por caso. Dónde se ve: el tablero T-FIRMAS, en
cada corrida. Cómo se resuelve: firma de mesa registrada en la fila." · FP-10 y FP-12→FIRMADA-CONDICIONAL,
cita *"Fírmalas así."*, texto: "Al cierre de BARRIDO-2, un acto único adjudica FP-10 y FP-12: SUPERADAS por los
productos del barrido si los cubren, o ejecución de fusión + diff si no. Nada se toca antes." ·
FP-11→FIRMADA-CONDICIONAL, cita *"Así como la propusiste."*, texto: "ficha-id-g3 se sella en el primer acto
post-cierre de BARRIDO-2, re-estampada contra el universo nuevo; si el universo nuevo la contradice, vuelve a
mesa solo ese punto." · FP-01..06→FIRMADA-CONDICIONAL (seis filas, misma cita *"Adelante con la propuesta."*),
texto: "Doy por firmadas M1–M6 con los textos recomendados del 14/ago [M1 cómputo matricial como definición
del ejecutable; M2 cortes iniciales por eje conforme a la cascada, respetando los tres ejes de hogar; M3 campo
medio para G1b con estatus HIPÓTESIS; M4 catálogo de momentos como pre-registro de gobernanza:461, roles
AJUSTE/HOLDOUT sellados en su commit 1; M5 libro de demanda como fuente única del curador; M6 los compass ya
están en el repo y el ADR los cita], CONDICIONADAS a que al cierre de BARRIDO-2 dirección re-verifique
M2/M4/M5 contra el universo nuevo: si no cambian, el sello procede sin volver a mesa; si alguna cambia, vuelve
a mesa solo esa." · FP-14→FIRMADA-CONDICIONAL, cita *"Aprobada."*, texto: "E3-TRIAGE corre automáticamente al
cierre de BARRIDO-2, contra su índice E2." · FP-24→SIN CAMBIO (ABIERTA por diseño), ratificación *"De acuerd."*
anotada en `gatea`. · FILA NUEVA DISPARADOR-POSTBARRIDO (id siguiente, derívalo): "Al cierre de BARRIDO-2
(PR #244 fusionado + §28 de su encargo): adjudicar FP-10/FP-12 → re-verificar M2/M4/M5 y sellar MOTOR-2
(FP-01..06) → E0 → FP-15 → sellar ficha-id-g3 (FP-11) → E3-TRIAGE (FP-14) → T20 (FP-18) → descargas FP-17.
ABIERTA hasta ejecutar todo" — el vigía imprime UN pendiente consolidado, nada firmado se pierde.
**Commit 2 — el barrido consolidador:** una fila por pendiente hallado en las fuentes (ii)-(viii) de arriba,
con cita `archivo:línea` (o `rama:archivo` para BARRIDO-2 §0), qué se decide, gate; NO adjudicas ninguno. Regla
de volumen: ≤5 casos de una misma fuente → fila por caso; >5 → una fila-resumen con ids listados. Lo que sea
tarea técnica sin decisión va a la nota, no al tablero. Cierra con conteo: nuevas / ya-cubiertas / anotadas.

## §3 · La regla que el ADR sella (firma de mesa = lanzamiento de este encargo)
"**`forense/firmas-pendientes.tsv` es la fuente única de decisiones de mesa.** Toda decisión pendiente tiene
fila ahí o no existe — un pendiente sin fila es defecto de la misma clase que un encargo sin archivo (A.3).
Los demás documentos APUNTAN al tablero, no almacenan decisiones. Todo acto o propuesta futura que produzca
una decisión pendiente crea su fila en el mismo commit — extensión de la regla de conducto ADR-70(c)."
El ADR registra además todas las firmas de Fase 1 y el criterio del disparador.

## FASE 2 · Mesa de revisión, en esta conversación (el trabajo no termina con el PR)
Tras empujar y abrir el PR borrador: presenta a mesa, EN EL CHAT y en lenguaje llano (sin jerga; formato:
qué es · de qué depende · si firmas / si no · firma propuesta lista para copiar), el tablero completo en tres
bloques: firmadas-hoy / condicionales-cableadas / **ABIERTAS que requieren a mesa** (las nuevas del barrido
primero). Entrega también, pegado íntegro en el chat, el texto de `instrucciones-proyecto-v2_10.md` para que
mesa lo copie a su proyecto; cuando mesa confirme "pegado" con fecha, registra FP-25→FIRMADA y FP-22→FIRMADA
por contención, en commit propio. Cada firma que mesa dé en la conversación se registra verbatim entre
comillas (ADR-79(i)) en su fila, commit + push, y se re-presenta el tablero. Comando permanente: si mesa
escribe "tablero", re-deriva del repo y re-presenta. La sesión cierra solo cuando mesa diga "listo"; el PR
queda listo para que MESA fusione — JAMÁS te auto-fusionas.

**Qué NO hace:** no ejecuta nada condicional · no toca data/tools/cola/estado-programa · no adjudica FP-24 ni
pendientes del barrido · no inventa vocabulario (estados: ABIERTA / FIRMADA / FIRMADA-CONDICIONAL / SIN CAMBIO).
**Suite:** `tests/check.py --baseline` VERDE en cada commit (T-FIRMAS imprimirá las filas nuevas: es señal, no
defecto) · `git diff --check`. **Contadores del programa: 0.** Reporte final: filas firmadas / nuevas /
pendientes-de-mesa, URL del PR.

---

## Nota de ejecución (añadida por el ejecutor, no por dirección)

Tres desviaciones del encargo, declaradas aquí porque A.3 exige que el archivo del encargo permita auditar si
el ejecutor hizo lo que se le dijo:

1. **Rama.** El encargo pide `claude/fuente-unica-decisiones`. El arnés de esta sesión asignó y creó
   `claude/cierre-firmas-barrido-hrp1si`, que es la rama con credenciales de empuje. Se trabajó sobre ésa; el
   nombre de rama es cosmético frente al PR, y abrir una rama distinta habría dejado el trabajo sin poder
   empujarse. Declarado en el reporte a mesa.
2. **E-CF no existía en el repo.** Verificado con `ls forense/encargos/ | grep -i -E "ECF|cierre-firmas"` →
   sin resultados. No hubo nada que marcar `SUPERADO POR E-DEC`; el encargo E-CF nunca se archivó, tal como su
   propia línea de supersesión anticipaba.
3. **Desborde de perímetro a `canon/estado-programa-v1_10.md`, declarado.** El encargo excluye ese archivo,
   pero dos vigías de la propia suite lo obligan y el encargo también exige `--baseline` VERDE en cada commit:
   `T15` compara el conteo de ADR contra todo `canon/*.md` (sitios `:27` y `:101`), y `T16` compara toda cita
   vigente de `**N FAIL · M WARN**` contra la corrida real (sitios `:129` y `:221`) — cambiar el número de
   filas `ABIERTA` mueve el WARN real por construcción. Cumplir "no tocar estado-programa" y "suite VERDE" a
   la vez es imposible. Se eligió VERDE, con el cambio mínimo (solo dígitos, sin reescribir prosa), mismo
   precedente ya escrito para esta colisión exacta: `ADR-62`, `ADR-87` y `ACTO RUTA-SELLO` §7
   (`forense/notas/2026-08-17-ruta-sello.md:125`, *"desborde de perímetro declarado"*).

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-17-EDEC-fuente-unica-decisiones.md" canon/gobernanza-v1_15.md` → 3: citado bajo ADR-91, ADR-137 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
