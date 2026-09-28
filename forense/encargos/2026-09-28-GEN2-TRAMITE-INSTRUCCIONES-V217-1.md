# ENCARGO · ACTO GEN2-TRAMITE-INSTRUCCIONES-V217-1 · Instrucciones del proyecto v2.17: el cuerpo operativo absorbe lo que esta semana cambió el régimen (cláusula de autonomía y modo amplio, D-19 estricta, canal por PR, recibo obligatorio, adopción por instrumento, marca de definición de contadores, memoria operativa, búsqueda por archivo, cita el objeto, decide-primero, obtención antes de decidir, instrumento alterno antes de negativo, HOLDOUT no se gasta sin firma, estructura de los TSV de gobierno), la HISTORIA absorbe el delta v2.15→v2.16, y sale la PLANTILLA-ENCARGO v2.2 — con el texto listo para que mesa lo pegue en el proyecto y el ADR que sella con la fecha del pegado

> ENTORNO: **NUBE** — solo `gobierno/`, `forense/encargos/PLANTILLA-*`, ADR y canon. Cero dato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `643a8198` (re-deriva al abrir) · una sesión, rama propia · MODELO: **Opus** (redacción normativa: cada regla con su defecto y su falsador) · MODO: **ABIERTO**, cláusula v1.0 (`3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica.
CONTADOR: cero mediciones; no adopta. Cambia `instrucciones_vigentes` a v2.17 **solo** en el segundo commit, después del pegado de mesa (A.9).

## 1 · OBJETIVO
(P1) **Cuerpo v2.17** (`gobierno/instrucciones-proyecto-v2_17.md`): parte del v2.16 operativo, mismos rótulos (A.N, A-bis N, D-N, E.N; no cambian de sentido), y absorbe **con su defecto y su falsador a tres meses** cada regla nueva del delta de §3. Toda regla nueva declara qué defecto real ya ocurrido atrapa y qué le habría costado a un lector (§1: «el aparato tiene costo»); si no le habría costado nada, se anota y no se instrumenta. El delta v2.15→v2.16 que hoy va al pie del cuerpo sale del cuerpo y entra a la HISTORIA.
(P2) **HISTORIA** (`gobierno/instrucciones-proyecto-v2_17-HISTORIA.md`): la v2.16-HISTORIA más el delta v2.15→v2.16 absorbido y el delta v2.16→v2.17 con fecha, PR y hallazgo por regla. Los dos cuerpos comparten rótulos; ante duda de sentido manda el histórico.
(P3) **PLANTILLA-ENCARGO v2.2** (`forense/encargos/PLANTILLA-ENCARGO-v2_2.md`): v2.1 más: bloque ADJUNTOS con sha calculado al recibir (no en el chat: mesa 28/sep, «deja de darme sha's aquí, eso se supone ya va dentro del encargo»); bloque «archivos que otro acto en vuelo está tocando» obligatorio; ENTORNO con la regla de caja para microdato y corpus montado; sección de opciones cuando el encargo lleva una decisión a mesa (situación · opciones con costo · recomendación · texto de firma); modo AUTÓNOMO-AMPLIO como valor de MODO; lista de PAROS con (e) invertible según entorno. Sin campos que se rellenen al cierre.
(P4) **Sello en dos lados.** Commit 1: v2.17, HISTORIA, plantilla, y un archivo `gobierno/PEGAR-EN-PROYECTO-v2_17.md` con el texto exacto (y su sha) que mesa pega en las instrucciones del proyecto de Claude. Mesa pega y contesta «pegado <fecha>». Commit 2 (mismo acto, tras la respuesta): ADR con la línea verbatim de mesa, `instrucciones_vigentes = v2.17`, retiro del delta del cuerpo v2.16 (queda histórico, no se edita: se archiva). Si mesa no contesta en la sesión, el acto cierra en commit 1 con NC `DECISIÓN-DE-MESA-PENDIENTE` y sucesor `-2` que hace el commit 2.

«Hecho», por comando: los tres archivos existen · `diff` entre v2.16 y v2.17 solo añade o reescribe reglas del delta de §3 (cada rótulo de v2.16 sigue presente: `grep -c` por rótulo = igual o mayor) · cada regla nueva tiene «defecto:» y «falsador:» en la HISTORIA (`grep -c` = número de reglas nuevas) · `PEGAR-EN-PROYECTO-v2_17.md` con sha · tras el pegado: ADR con la línea de mesa y `instrucciones_vigentes=v2.17` en el archivo que `status`/`tramite` leen · `check.py --baseline` VERDE (T-tests de instrucciones, si existen, pasan).

## 2 · FIRMAS DE MESA — dadas
A.9 («una versión no está sellada hasta que está en los dos lados, y el ADR lo declara con la fecha del pegado») · §9 (sello de versión) · cláusula de autonomía v1.0 (24/sep) y AUTÓNOMO-AMPLIO (26/sep: «la sesión decide orden, agrupación y profundidad; una hoja de firmas al cierre») · mandatos verbatim de mesa esta semana, que son la fuente del delta: 21/sep «microdato desde caja»; 24/sep cláusula; 26/sep «no más microencargos; es Opus 5.5, no Haiku»; 27/sep «todo lo que requiera búsqueda de fuentes, datos etc, lo hacemos para obtenerlos antes de decidir nada»; 27/sep «probablemente no existe con el instrumento exacto que tenemos hoy pero puede existir otro instrumento que resuelva las mismas incógnitas»; 27/sep «ni opciones me diste para cada una, solo la recomendación»; 28/sep «deja de darme sha's aquí». **El pegado en el proyecto es de mesa**; nada más se firma.

## 3 · LO QUE DIRECCIÓN SABE — el delta v2.16 → v2.17, regla por regla, con origen
- [LEÍDO] `gobierno/instrucciones-proyecto-v2_16.md` (con sidecar) y `-HISTORIA.md` existen; `PLANTILLA-ENCARGO-v2_1.md` existe. El delta v2.15→v2.16 sigue al pie del cuerpo v2.16 (§«DELTA»), como ese cuerpo prevé.
- Delta (origen entre paréntesis; el acto lo verifica en cada objeto antes de escribir la regla):
  1. §0/§6 · **Cláusula de autonomía v1.0** y **MODO AUTÓNOMO-AMPLIO**: el ejecutor resuelve discrepancias con el repo, sigue la intención de una firma cuando la letra choca (INTERPRETACIÓN-DECLARADA), redacta lo que falte rotulado PROPUESTO-POR-EJECUTOR, ejecuta la opción recomendada, PARA solo por D-19; una hoja de firmas al cierre (mesa 24 y 26/sep; `CLAUSULA-AUTONOMIA-v1_0`).
  2. D-19 · **estricta**: «objetivo inalcanzable» solo sin ruta legítima (cláusula).
  3. D-10/E.7 · **Canal por PR `[deriva]`** con auto-merge; las vistas las publica solo el canal; tablero derivado en CI; guarda de tamaño; resumen nocturno de la suite en archivo (CI-TIEMPO-1/2, RESUMEN-SUITE-1; transfer 26/sep regla 6).
  4. §6 · **Recibo obligatorio antes de fusionar `codex/*`**; el recibo de Codex no sustituye al de Claude; un recibo post-merge lo dice en su primera línea (FIRMAS-15 R(a), FIRMAS-20 D; ~20 PR fusionados sin recibo 22–28/sep).
  5. §4/E.2 · **Adopción por instrumento**: ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR (FIRMAS-11…-20).
  6. E.4 · **Marca de definición de contadores**: todo contador cuya definición cambie publica `<contador>_definicion_desde=<commit>` (celdas_validadas 38dd709; legacy en RESUMEN-SUITE-1); una celda validada prospectivamente no deja de serlo porque su piso se re-mida.
  7. §0 · **Memoria operativa** (`canon/MEMORIA-OPERATIVA.md`) regenerada por `/tramite`, `CLAUDE.md` que la importa, hook que bloquea lecturas > 200 líneas (transfer 26/sep regla 8).
  8. §0/A.8 · **Un acto se busca por su archivo en `forense/encargos/`, nunca por rama** (transfer 26/sep regla 1: cinco actos dados por «no lanzados»; dos cuerpos reescritos).
  9. §2 · **Cita el objeto, no la NC que lo cita** (tres encargos parados por premisas de notas; `e760-10` apuntaba a una tabla sin esos RES).
  10. §0 · **Decide primero, encargo después**: hoja RH (situación · qué se pide · opciones con costo · recomendación · plazo · texto de firma); mesa contesta por letra; la firma viaja verbatim en el encargo que la ejecuta (FIRMAS-14…-20; mesa 27/sep: «ni opciones me diste»).
  11. A.4/A.5 · **Obtención antes de decidir**: ninguna letra que cierre o difiera por «no hay dato / no vale buscarlo» se firma sin un acto de obtención con universo, términos y receta; «la fuente no existe en lo que tenemos» no es «no existe» (mesa 27/sep; OBTENCION-PREVIA-1, EXTERNA-1).
  12. A.15 · **Instrumento alterno antes de negativo**: un negativo sobre una incógnita declara qué instrumentos del corpus se cruzaron **por texto de pregunta** con otra unidad u otra ola, y con qué dictamen A.4 (mesa 27/sep; `canon/mapa-instrumentos-alternos-v1_0.tsv`; ENCRIGE/ENVE ya estaban para R03).
  13. §4/E.6 · **HOLDOUT**: un momento con `rol_calibracion = HOLDOUT` no se calcula sin firma de mesa; calcularlo lo convierte en visto y lo declara (hoja del mapa §«Antes de firmar»). Una ola sin campo de reserva pero más reciente de un programa con historia se trata como no abierta hasta que mesa decida (E.6, las cinco olas).
  14. §6 · **Entorno por lo que el acto toca**: microdato o corpus montado → caja; documentación y portales → nube (mesa 21/sep; dirección puso dos actos en nube por inercia el 27/sep y mesa lo corrigió).
  15. A.14/A.16 · **TSV de gobierno**: número de campos = cabecera y `estado` del vocabulario (guardia en CI, PENDIENTES-2: 10 filas invisibles); token A.14 al inicio de `razon`, prosa después; ninguna cifra sobre un TSV con `awk` por línea física.
  16. §0 · **Sin sha en el chat**: los sha viajan dentro del encargo o su sidecar; el acto calcula el sha de lo que recibe (mesa 28/sep).
  17. §4 · **Regla 6** (memoria operativa): sin retadores, pilotos ni duelos sobre olas vistas; frente prospectivo = familias 2027; cruce visto sirve para describir y calibrar, rotulado (transfer 26/sep regla 5).
  18. D-11 · **Lotes grandes**: un encargo agrupa piezas afines aunque excedan cuatro si la sesión decide los PR (mesa: «no más microencargos»); D-11 pasa de tope a mínimo por PR/ADR.
- [REPORTADO] Transfer 26/sep §5.4 lista los ocho primeros; los diez restantes son de esta semana y dirección los verificó en los actos citados.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'INSTRUCCIONES-V2'` → 0 (V216 fue trámite anterior: léelo como modelo del sello). En vuelo: HOJA-FIRMAS-21-1 (misma fecha; disjunto), continuidad C1/C2/C3 (no tocan `gobierno/`).

## 5 · PIEZAS
P1 → P2 → P3 → P4. Rama prevista: si una regla del delta ya está en v2.16 con otro rótulo, se cita y no se duplica; si un origen citado no se sostiene al abrir el objeto, la regla entra como PROPUESTA-SIN-DEFECTO-CITADO y no se instrumenta (§1).

## 6 · LATITUD
Redacción, orden dentro de cada sección, qué va a cuerpo y qué a HISTORIA: tuyos, con un criterio: el cuerpo operativo no crece más de lo que el delta exige. PREGUNTA A MESA: solo el pegado. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) editar v2.16 o su HISTORIA (se archivan), un ADR previo, un sello · c) declarar vigente v2.17 sin la línea de mesa; cambiar el sentido de un rótulo existente · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Vigente solo con pegado en el proyecto y ADR con fecha» protege **adoptar** (A.9) · «Rótulos no cambian de sentido; v2.16 no se edita» protege **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `gobierno/instrucciones-proyecto-v2_17.md` (+ sidecar), `-HISTORIA.md`, `PEGAR-EN-PROYECTO-v2_17.md`, `forense/encargos/PLANTILLA-ENCARGO-v2_2.md` (+ sidecar), el archivo que registra `instrucciones_vigentes`, ADR, L0, cascada. Ajeno: todo `forense/` salvo la plantilla, `canon/`, `data/`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No cambia ninguna regla de contenido (§3), de medición (§4) ni E.1–E.3/E.6 salvo las adiciones del delta; no toca `CLAUDE.md` ni la memoria (los regenera `/tramite` después). Sucesores: `-2` si el commit 2 queda pendiente; `/tramite` para memoria y `CLAUDE.md` con v2.17. Sin módulo de auditoría. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-TRAMITE-INSTRUCCIONES-V217-1-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS
- **qué:** P4, «Commit 2 (mismo acto, tras la respuesta): ADR con la línea verbatim de mesa, `instrucciones_vigentes = v2.17`, retiro del delta del cuerpo v2.16». **por qué:** DECISIÓN-DE-MESA-PENDIENTE: mesa contestó «Todavía no» al pegado (28/sep/2026). **impacto:** v2.16 sigue vigente; v2.17 y su HISTORIA quedan en `gobierno/pendiente-de-pegado/` (INTERPRETACIÓN-DECLARADA, ver ADR); `instrucciones_vigentes` no se mueve. **sucesor:** `GEN2-TRAMITE-INSTRUCCIONES-V217-2`; `NC-260928-GEN2-TRAMITE-INSTRUCCIONES-V217-1-3e59-01`; `FP-260928-GEN2-TRAMITE-INSTRUCCIONES-V217-1-3e59-01`.

## CONSUMIDO
PR #1265 (commit 1 y cascada; ADR-260928-GEN2-TRAMITE-INSTRUCCIONES-V217-1-3e59-01). Sin adendas.
