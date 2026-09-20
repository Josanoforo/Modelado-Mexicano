ENCARGO · ACTO GEN2-RELEVO-RECONCILIA-1 · EL CONTADOR DE LEGACY NO VE TRABAJO GEN2 QUE YA ESTÁ SELLADO: RECONCILIAR LA VISTA DE RELEVO POR IDENTIDAD DE SLOT, NO POR NÚMERO DE `RES`

Sustituye a `ENCARGO-GEN2-SENAL-Y-DIETA-1` (retirado por dirección antes de lanzarse: su premisa central era falsa).

ENTORNO: NUBE — el hook de arranque imprime `ENTORNO-DERIVADO`; si dice `CAJA` puedes correrlo igual y lo dices.

CABECERA · SHA de redacción `93f68f2e`; re-deriva · una sola sesión, rama propia · MODELO: Opus · MODO: ABIERTO · CONTADOR: `cuenta_gen2 = NO`; no mide. Este acto no adopta: propone. `dependencias_numericas_legacy_activas` y `adoptados_activos` no deben moverse en este PR; lo que se mueva lo moverá mesa en el sucesor.

1 · OBJETIVO

`dependencias_numericas_legacy_activas` (hoy 173) es la métrica de migración del programa: qué mediciones de GEN1 ya se re-hicieron en GEN2 con la trazabilidad que les faltaba (palabras de mesa, 20/sep). Hay evidencia de que subcuenta: trabajo GEN2 sellado que la vista de relevo no enlaza. El objetivo es saber, slot por slot, cuáles de los 173 ya tienen su medición GEN2 sellada y por qué la vista no la ve — para que el contador vuelva a guiar. «Hecho» significa: una tabla derivada, una fila por slot legacy, que diga `YA-REHECHO-EN-GEN2` (con CALC, RESULT, delta y estimando casado por texto) · `REHECHO-CON-DIFERENCIA` · `SIN-REHACER` (con receta y entorno de la demanda) — y la causa mecánica de la ceguera, reproducida.

2 · FIRMAS DE MESA

Propósito del contador (20/sep/2026, verbatim): «la diferencia de 173 es porque era lo que llevábamos en Gen1 antes de Gen2, y esa métrica nos había permitido guiar […] qué mediciones de Gen1 se hicieron y cuáles se re-hicieron en Gen2 pero ahora con la trazabilidad que nos faltaba.» Sobre el duelo (verbatim): «no es motor vs LLM, es motor vs LLM vs LLM con corpus.» Ninguna firma nueva se pide aquí. Se retira la propuesta de dirección de declarar las lecturas del marco M "no relevables": era contraria al propósito del contador.

3 · LO QUE DIRECCIÓN SABE

* `[EJECUTADO]` De las 173 filas `LEGACY-GEN1` de `relevo-usos-v1_0.tsv`, 70 son del marco M (`forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv`): 14 celdas × {`R`, `M`, `L:L-solo`, `L:L-corpus`, `AGREGADO`}. Las 70: `SIN-CANDIDATO`, razón `CORR-SIN-CALC-DECLARADA`.
* `[EJECUTADO]` Los 14 `celda_R` ya tienen un CALC GEN2 sellado, por identidad de celda: `CALC-R-CIV-M-{01,02,04,10,12,13}`, `CALC-R-DIN-M-01-v4`, `CALC-R-FAM-M-{01,05,06,07}-v3`, `CALC-R-TRA-M-{02,03,07}-v3` — todos `SELLADA · cuenta_gen2 = SI · REPRODUCE`. 14 de 14.
* `[EJECUTADO]` Por qué la vista no los ve, en tres casos leídos: `CALC-R-CIV-M-01/spec.yaml` dice «Releva la demanda CORR-0024 (RES-0093)»; la vista llama hoy a ese slot RES-0095 / CORR-0020. `CALC-R-FAM-M-05-v3` y `CALC-R-TRA-M-07-v3`: ningún `RES-####` en su spec. O el pin apunta a un número que se corrió, o no hay pin.
* `[LEÍDO]` NC-0343 (`ABIERTA`, sucesor `SIN-ASIGNAR`): «37 filas con `RES-####` desincronizado de su autoridad `demanda-resultados.tsv` […] corridas en uno desde que entró el slot DIN…». Los `RES` son posicionales: insertar un slot recorre a los demás. Es la misma enfermedad que la numeración contigua de ADR/NC.
* `[EJECUTADO]` El duelo de tres ya corrió en GEN2 y está sellado: `CALC-TRIADA-0001` (259 RESULT) y `CALC-TRIADA-0002` (27), `cuenta = SI`, `REPRODUCE`. `CALC-TRIADA-0002`: `U3-N = 12`; `MAE-M = 4.99 pp`, `MAE-L-SOLO = 3.96`, `MAE-L-CORPUS = 3.89`; las tres deltas pareadas `INCONCLUSO`; `VEREDICTO-GLOBAL = SIN-GANADOR-UNICO`.
* `[EJECUTADO]` La demanda nombra receta y entorno para las otras tres clases del marco: `celda_M` → NUBE `tools/emite_m.py` · `celda_L` → NUBE runner de `prereg-duelo-v2` · `celda_AGREGADO` → NUBE · (`celda_R` → CAJA `tools/arbitra.py`).
* `[SUPUESTO]` que `CALC-TRIADA-0001` contiene, por celda, los valores de `M`, `L_SOLO`, `L_CORPUS` y el agregado que corresponden a los otros 56 slots. Si es cierto, esos 56 también están rehechos y sin enlazar; si no, la tabla lo dirá.
* `[SUPUESTO]` que el mismo patrón (medición GEN2 sellada, pin ausente o corrido) afecta slots fuera del marco M. RES-0028 fue un caso (#914).
* `[REPORTADO]` por #914: escribir un pin en `tramite.yaml` para RES-0028 hizo que `status` PARARA por un insumo con `FUNCION-INDETERMINADA`. Puede haber más de una causa de ceguera.

4 · YA HECHO / YA DECIDIDO

`GEN2-RELEVO-TANDA-1` (#905) casó estimandos de 12 candidatos y dejó `P5-cobertura-19sep.tsv`; `TANDA-2` (#914) adoptó 11. Ninguno buscó por identidad de consumidor: ambos partieron de lo que la vista ya proponía. NC-0343 documenta la desincronía y nadie la tomó. Repite la búsqueda: `decisiones.tsv`, ADR y notas con «marco M», «CALC-R-», «RES desincron».

5 · PIEZAS

P1 · Reconciliación por identidad, los 173. Para cada slot legacy, busca medición GEN2 sellada por lo que el slot es —archivo consumidor, celda/conducta, instrumento, ola, universo— y no por su número `RES`. Para cada hallazgo: CALC, RESULT, valor GEN2 vs. legacy, delta por script (`relevo_candidatos_delta.py` si sirve), y estimando casado por texto en cinco dimensiones (la lección de `matrimonio_directo`: mismo número no es misma afirmación). Si [SUPUESTO-TRIADA] es falso, los 56 quedan `SIN-REHACER` con su receta NUBE, y eso es demanda lista para lanzar.

P2 · La causa, reproducida. ¿Por qué `relevo_usos.py` no enlaza? Enumera las causas distintas con un caso cada una: pin a `RES` corrido · CALC sin pin · insumo `FUNCION-INDETERMINADA` · otra. Di cuántos slots cae en cada una. No arregles la herramienta aquí salvo que sea ≤ 10 líneas y no cambie ningún contador: propón.

P3 · Propuesta de firma para mesa, por bins de la ADENDA del 15/sep. Los `YA-REHECHO` con delta dentro de tolerancia y estimando casado, listados por nombre para firma uno por uno (bin 2) o en bloque con tabla (bin 3). Los `REHECHO-CON-DIFERENCIA`, aparte, con la diferencia explicada. Este acto no escribe ningún pin en `milpa/` ni adopta.

P4 · Desglose informativo en `status` y tablero — aditivo: legacy por consumidor (`motor` · `procedencia` · `catálogo de momentos` · `marco del duelo`), todos relevables, cada uno con cuántos `YA-REHECHO` hay según P1. La suma iguala al total, que no cambia de nombre ni de valor. Si `tests/test_corrida0_oro.py` compara `status` byte a byte (`[SUPUESTO]`), regenerar el oro es parte del acto.

P5 · Métrica rectora en la primera línea del tablero. `celdas_validadas` = predicción emitida antes de ver el dato y comparada contra R con error sellado. Tres clases que no se funden: cruces C2 (20 celdas; MAE 1.47 y 1.57 pp) · persistencia `t−1` (53; por instrumento y brecha) · duelo de tres a nivel nacional (U3 = 12; MAE por contendiente y el veredicto `SIN-GANADOR-UNICO`). Sub-cifra del dominio dinero.

6 · LATITUD

Decides tú: cómo casar identidad de slot; formato de la tabla; si P4 y P5 van en este PR o en uno segundo si P1 crece. Preguntas a mesa y sigues: un slot cuyo CALC GEN2 existe pero mide otro universo. No decides: adoptar; tocar `marco-M-sorteado-v1_3.tsv` ni nada bajo `prereg-duelo-v2/`.

7 · PAROS (lista cerrada)

Escribir un pin de adopción · que un contador existente cambie de valor · editar un CALC o spec sellados · objetivo inalcanzable.

8 · COMPUERTAS

Ninguna.

9 · PERÍMETRO

Propio: `forense/analisis/relevo-reconcilia-1/` · `tools/corrida0.py` (solo `status`) · `tools/tablero_programa.py` y el tablero · NC-0343 (enmienda o cierre) · FP nuevas · tests propios. Ajeno: `milpa/**` · `relevo-usos` salvo regenerar por comando · todo CALC · `prereg-duelo-v2/**` · el esquema de numeración de `RES` (es de la conversación TUBERÍA; repórtaselo como hallazgo, no lo rediseñes).

Si te encuentras escribiendo fuera de esta lista, PARA.

10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE

No adopta · no re-mide · no arregla la numeración posicional. Sucesores: `RELEVO-TANDA-3` (ejecuta lo que mesa firme) · hallazgo a TUBERÍA: los `RES` posicionales son otro caso del impuesto de numeración. Auditoría (afirma sobre el programa): el duelo de tres dice, con 12 celdas e IC anchos, que el motor no se distingue de un LLM con o sin corpus a nivel nacional, y en el punto queda un punto porcentual por detrás. Ese resultado es del emisor v1 y de celdas nacionales; la validación por segmento (C2) es otra afirmación y no lo contradice ni lo rescata. Ningún artefacto debe escribir «el motor le gana a un LLM». Peligroso leído simplista, en las dos direcciones: «`SIN-GANADOR-UNICO`» como «el motor no sirve», o `celdas_validadas` alto como «acierta». Cascada de `/acto` · `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

| pieza | por qué | impacto | sucesor |
|---|---|---|---|
| **P5** · métrica rectora `celdas_validadas` en la primera línea del tablero | `PARO-PREMISA`. Dos de las tres clases no resuelven a un CALC sellado con la búsqueda que corrí, y §2 prohíbe teclear la cifra esperada. (a) *cruces C2, «20 celdas; MAE 1.47 y 1.57 pp»*: examiné los 2 `CALC-C2-COMPUESTO-IC` sellados y sus `resultados.json`; ambos emiten **controles de identidad** (`DELTA-N=0`, `DELTA-P-MAX≈4.8e-07`), ningún MAE de validación ni universo de 20 celdas → `EXISTE-NO-SATISFACE`. (b) *persistencia `t−1`, «53»*: `CALC-PISO-PERSISTENCIA-ERROR-0001` emite MAE por eje (10.2–11.4 pp) con N de 2 a 10; no hay agregado de 53 ni la partición por instrumento y brecha → `NO-ENCONTRADO` en los 166 directorios `CALC-*` con `spec.yaml` (A.13). | El tablero no estrena métrica rectora. **Sí** quedó derivada la clase del duelo: `U3-N = 12`, `MAE-M = 4.9866732397828875 pp`, `MAE-L-SOLO = 3.9573621816025666`, `MAE-L-CORPUS = 3.889025747112979`, `VEREDICTO-GLOBAL = SIN-GANADOR-UNICO`. | `NC-0423` → `RELEVO-TANDA-3` |
| **P2** · cuarta causa de ceguera: insumo `FUNCION-INDETERMINADA` (#914, RES-0028) | `NO-VERIFICABLE-AQUÍ`. Reproducirla exige escribir un pin en `milpa/tramite.yaml`, que es el **primer PARO** de la lista cerrada del §7. El mecanismo está localizado (`tools/corrida0.py:3623`) pero no se dispara sin el pin. No se colapsa con «no ocurre» (A.5). | Esa causa queda sin cuantificar; las otras tres sí están contadas (6 + 64 + 8). | `NC-0424` → `RELEVO-TANDA-3` |
| **P1/P3** · casar el estimando por texto en cinco dimensiones de los 9 `REHECHO-CON-DIFERENCIA` y los 21 `CANDIDATO-POR-IDENTIDAD-SIN-CASAR` | `DECISIÓN-DE-MESA-PENDIENTE`. Los 9 son puntos L de la misma escala y celda cuya diferencia es de procedimiento de agregación — explicarla es lectura de texto, no de script. Los 21 casaron por **clave de consumidor**, y un acierto de clave no es un estimando casado (A-bis.3/4). | 30 slots no llegan a propuesta de firma. Los 28 `YA-REHECHO` sí llegan (14 en bin 3 por bloque, 14 en bin 2 uno por uno). | `NC-0425` → `RELEVO-TANDA-3` |
| **P2** · arreglar `tools/relevo_usos.py` para que enlace por identidad | `FUERA-DE-PERÍMETRO`. El encargo autoriza el parche sólo si es ≤10 líneas **y** no mueve ningún contador. El arreglo mínimo (quinto canal por `parametros.id_celda`) no cabe en 10 líneas y movería `dependencias_numericas_legacy_activas`, que es el segundo PARO. | La vista sigue sin ver las 37 cifras; el contador sigue subcontando hasta que mesa firme. | `NC-0426` → `RELEVO-TANDA-3` |
| **hallazgo a TUBERÍA** · el esquema posicional de `RES-####` | `FUERA-DE-PERÍMETRO` (§9 lo declara ajeno: «repórtaselo como hallazgo, no lo rediseñes»). Medido, no rediseñado: los seis pines `CALC-R-CIV` corridos **+2 uniforme**, y el de `CIV-M-01` también en el eje `CORR`. | Se repetirá en cada slot que se inserte: toda spec sellada aguas arriba queda apuntando al slot equivocado, y E.3 impide corregirla editándola. | `NC-0427` → conversación TUBERÍA |

**`NC-0343` queda `ABIERTA`**, ahora con sucesor asignado: este acto la **toma y la mide** (no era sólo un derivado a re-derivar: es la causa de que la vista no vea 37 cifras GEN2 selladas), pero el rediseño del esquema es de TUBERÍA.

**Nada más quedó sin correr.** P1, P2, P3 y P4 se ejecutan completos.

## CONSUMIDO

Ejecutado por `ACTO GEN2-RELEVO-RECONCILIA-1` en **[PR #928](https://github.com/Josanoforo/Modelado-Mexicano/pull/928)**, rama `claude/gracious-faraday-wf9b8j`, base `dfb07b9`. `ADR-568`. Entorno NUBE `cloud_default`, corpus NO montado (archivos examinados = 0), Opus 5. `cuenta_gen2 = NO`: cero mediciones, cero adopciones, cero contadores movidos.
