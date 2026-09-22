# ENCARGO · ACTO GEN2-MARCO-M-CONSUMIDOR-1 · Qué se rompe si `marco-M-sorteado-v1_3.tsv` deja de ser consumidor activo: medido archivo por archivo, con el mapa de migración escrito — sin retirar nada

> ENTORNO: **NUBE** — el hook de arranque imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA de redacción `ccd7c0eb` (22/sep/2026) · una sola sesión (D-17) · MODELO: Opus (lectura de ocho herramientas y 70 lecturas legacy: juicio) · MODO: **ABIERTO** · CONTADOR: cero mediciones; **no** mueve `adoptados_activos`, `dependencias_numericas_legacy_activas` ni la vista (este acto no retira: mide y propone) · FP/ADR/NC candidatos: raíz de acto (D-24), los deriva `tools/cierre_acto.py`.

## 1 · OBJETIVO
Que mesa pueda decidir P6.1 del plan de aceleración —«¿el marco M sigue siendo consumidor activo?»— con una lista, no con una intuición: qué herramientas y tests leen `marco-M-sorteado-v1_3.tsv`, qué dejaría de funcionar si el archivo se retirara o se rotulara HISTÓRICO, qué consumidor sustituye a cada lectura (el marcador por segmento sobre el catálogo, FP-383; `milpa/estimadores-por-segmento.yaml`), y qué pasa con las 70 lecturas legacy activas que viven ahí. Habilita: la decisión de retiro y, con ella, bajar `dependencias_numericas_legacy_activas` (184 al redactar) sin romper GO-MARCADOR.
«Hecho» = sobre el commit final con `origin/main` fusionado: existe `forense/notas/<fecha>-GEN2-MARCO-M-CONSUMIDOR-1-mapa.tsv` con una fila por lectura (`archivo:línea · qué lee · qué se rompe si falta · sustituto · estado`), y `awk -F'\t' 'NR>1' <mapa> | wc -l` ≥ el conteo de `grep -rn "marco-M-sorteado" tools/ tests/ milpa/` (cada referencia tiene fila); una FP con raíz de acto abre la decisión de retiro con vocabulario cerrado.

## 2 · FIRMAS DE MESA
- Ya en el repo, verbatim: `FP-383` (17/sep/2026, `data/corrida0/decisiones.tsv` objeto `marcador:emisor-fuera`): «el marcador se rediseña sobre el catálogo de momentos — estimadores adjudicados por celda-D contra R». Y el diseño del marcador firmado (`MARCADOR-SEGMENTO-diseno-direccion-v1_0`, §1 (iii)): «la columna de segmento en `marco-M-sorteado-v1_3.tsv` queda sin objeto… el marco del marcador ya no es el marco M sorteado».
- Propuesta de dirección, marcada como tal: «Este acto abre la FP de retiro con vocabulario cerrado —`RETIRAR-CON-MAPA` / `HISTÓRICO-SIN-RETIRO` / `CONSUMIDOR-VIGENTE`— y mesa la firma después de leer el mapa; el acto no ejecuta ninguna de las tres.»

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
- `[EJECUTADO]` `grep -rln "marco-M-sorteado" tools/ tests/ milpa/` → 8 archivos fuente: `tools/corrida0.py`, `tools/pines_mesa.py`, `tools/tablero_programa.py`, `tools/tablero_vista.py`, `tools/score_marco_m.py`, `tools/arbitra.py`, `tools/emite_m.py`, `tools/arbitra_gen2.py` (más `.pyc`). `grep -rn … | wc -l` → 29 referencias.
- `[EJECUTADO]` `awk -F'\t' '$0 ~ /marco-M-sorteado/ && $0 ~ /\tSI\t/' data/corrida0/usos.tsv | wc -l` → **70** lecturas activas que citan el marco M como consumidor (el plan del 20/sep las contó igual: 70 de 173 legacy).
- `[LEÍDO]` `forense/notas/2026-09-15-GEN2-MARCADOR-C0-D-A8-hueco.md` §7: «la columna de segmento en `marco-M-sorteado-v1_3.tsv`» era el tercer prerrequisito del marcador; `tests/gonogo_marcador.py` (6 checks) acredita el eje `x = ∅` leyendo el marco.
- `[EXISTE]` `milpa/estimadores-por-segmento.yaml` (lo cita la FP `…ARBITRO-MARGINALES-1-ed7d-02`: «sólo lo escribe el marcador tras firma»). No sé qué contiene ni si algún consumidor lo lee ya.
- `[SUPUESTO]` Retirar el marco M rompe GO-MARCADOR y `emite_m.py`, y no rompe nada del catálogo ni de las celdas-D. Por qué lo creo: las 29 referencias están en herramientas del eje `x = ∅`; las celdas-D no lo citan. Si resulta falso —una celda-D o el marcador por segmento lo lee—, rama prevista: la fila del mapa lo dice y el dictamen no puede ser RETIRAR-CON-MAPA sin sustituto nombrado.
- `[REPORTADO]` Plan de aceleración §P6 (dirección, 20/sep): «`[SUPUESTO]` GO-MARCADOR aún lo lee para su eje — hay que ver qué se rompe antes de retirarlo». Este acto es ese «ver».
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO
- `grep -rln "MARCO-M-CONSUMIDOR\|retiro del marco M\|marco M como consumidor" forense/ canon/` → reporta; al redactar, ninguna nota con ese objeto (universo `forense/notas/`, `forense/encargos/`, `canon/`).
- `decisiones.tsv`: `grep -i "marco-M\|marco M" data/corrida0/decisiones.tsv` → reporta; al redactar, solo la fila de FP-383 (que lo saca del marcador, no del programa).
- Al ejecutor: **repítela tú.** Si un acto ya hizo el mapa, el entregable es citarlo y hacer solo lo que falte.

## 5 · PIEZAS — resultado esperado, no receta
- **P1 · El mapa de lecturas.** Una fila por referencia en código (29) y por lectura legacy activa que cite el marco (70, por `resultado_id`): qué lee, para qué, qué se rompe si el archivo desaparece, y el **sustituto** cuando exista (`marcador-segmento` para celdas por eje, `estimadores-por-segmento.yaml` para adjudicados, `arbitra_gen2` para lo que `arbitra` hacía). Queda bien si cada fila de código trae `archivo:línea` y cada lectura legacy trae su `resultado_id` y el consumidor que la lee. Las lecturas sin sustituto se marcan `SIN-SUSTITUTO` y se cuentan: son el costo real del retiro.
- **P2 · La prueba en seco.** Sin retirar nada: un test que renombra el archivo en un directorio temporal (copia del árbol, nunca el clon) y corre `tests/gonogo_marcador.py`, `emite_m.py --help` y `corrida0.py status` — qué falla, con salida cruda. Queda bien si la lista de fallos coincide con las filas `se rompe = SÍ` del mapa (y si no coincide, el mapa se corrige, no el test).
- **P3 · La FP de retiro.** Raíz de acto, vocabulario cerrado (§2), con el costo contado: N filas `SIN-SUSTITUTO`, M herramientas que habría que adaptar, y las 70 lecturas legacy clasificadas por lo que el relevo ya decidió (YA-ADOPTADO / CANDIDATO-GEN2 / SIN-CANDIDATO, de `relevo-usos`). Recomendación del ejecutor permitida, marcada como tal.
- «si `[SUPUESTO]` resulta falso»: un consumidor GEN2 lee el marco → el mapa lo dice, la FP nace con `CONSUMIDOR-VIGENTE` como opción recomendada y el acto termina igual.

## 6 · LATITUD
DECIDES TÚ: el formato del mapa (TSV), el orden, cómo construir la copia temporal para P2, regenerar derivados por comando, arreglar ≤ 10 líneas adyacentes declarándolo.
PREGUNTAS A MESA (con opciones y recomendación, y sigues): si `estimadores-por-segmento.yaml` está vacío porque la adopción de marginales (`FP-…ARBITRO-MARGINALES-1-ed7d-02`) sigue abierta, ¿el sustituto se declara «previsto, no existente» (recomendado) o el mapa espera a esa firma?
NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada
a) no aplica (no hay ola reservada) · b) borrar, forzar o reescribir algo sellado — **retirar el marco M es borrar**: PARO; este acto solo copia en temporal · c) adoptar o mover `adoptados_activos` / `dependencias_numericas_legacy_activas` · d) no aplica · e) entorno equivocado · f) OBJETIVO inalcanzable → PARO como entregable.

## 8 · COMPUERTAS
«P2 corre solo sobre copia temporal del árbol — protege: borrar.» Ninguna otra.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/notas/<fecha>-GEN2-MARCO-M-CONSUMIDOR-1-mapa.tsv` (nuevo) · nota de cierre · `tests/test_marco_m_en_seco.py` (nuevo, huérfano en CI: `ci_guardias --ejecuta-huerfanos`) · `forense/firmas-pendientes.tsv` (una FP nueva) · `canon/L0/<ADR-raíz>.md` · hallazgos/NC propios.
Ajeno que no se toca: `marco-M-sorteado-v1_3.tsv` (sellado; ni se mueve ni se rotula aquí), las ocho herramientas (solo lectura), `usos.tsv` (derivado; se lee), `estimadores-por-segmento.yaml` (lo escribe el marcador).
Archivos que OTRO ACTO EN VUELO esté tocando ahora: **ninguno verificado** (sin ramas vivas al redactar).
«Si te encuentras escribiendo fuera de esta lista, PARA.»
PERÍMETRO DE CIERRE — permanente (D-21).

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE
No hace: no retira, no adapta herramientas, no adopta, no toca el marcador ni el relevo.
Sucesores: el acto que ejecute la opción firmada (si RETIRAR-CON-MAPA: adaptar las herramientas del mapa y rotular el marco HISTÓRICO, un acto de tubería); la adopción de marginales (`…ed7d-02`) llena el sustituto.
Auditoría de rigor extremo: no aplica (afirma sobre el aparato).
Cierre: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` los añade /acto; adendas como archivo propio.

## NO-CORRIDO / RESERVAS

Ninguno. Las tres piezas (P1-P3) se ejecutaron completas, en MODO ABIERTO,
sin disparar ningún PARO de la lista cerrada de §7. La pregunta de LATITUD
del §6 (¿sustituto «previsto, no existente» o esperar la firma de
marginales?) quedó resuelta de facto: `milpa/estimadores-por-segmento.yaml`
no está vacío — ya tiene 20 celdas emitidas por `tools/marcador_segmento.py`
(19/sep/2026) que no citan el marco M — así que no hizo falta preguntar
nada a mesa; el `[SUPUESTO]` §3 se verificó con un matiz de granularidad
(por subcomando de `corrida0.py`, no por archivo) que el mapa ya recoge.
