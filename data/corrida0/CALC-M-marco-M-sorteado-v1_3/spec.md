# CALC-M-marco-M-sorteado-v1_3 — el corredor M del marcador, envuelto para GEN2

ACTO GEN2-E7 · READINESS-2 · Pieza A, A1.

## 1 · Qué mide

Una corrida del **corredor M** sobre el **marco vigente**
(`forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv`, 14 celdas, columna de
elegibilidad `elegible_v1_1`). Por cada celda elegible produce el punto `p`
que `milpa/src/emisor.py::emitir_binaria` emite para su
(regla, conducta), y el `grado_DD` que `tools/emite_m.py::calcula_grado_DD`
deriva **por conducta** (la corrección de M13; antes se derivaba por regla y
colapsaba conductas distintas de una misma regla).

## 2 · Qué NO es

**No es un número nuevo del modelo.** Cada `p` de esta corrida es el mismo
que el emisor ya producía antes de este acto. Lo que este CALC agrega es la
*cadena*: spec versionada, contrato ejecutable, snapshot de inputs con SHA,
`ejecucion.json` y sello. El propósito del acto es que el **primer** número
nuevo del marcador nazca ya con esa cadena, no que este acto lo produzca.

`etiquetas.cuenta_gen2: PENDIENTE-DE-MESA` — esta corrida corre sobre insumos
de repo y no consume corpus; si cuenta o no como GEN2 del modelo es firma de
mesa en el merge, no decisión del corredor.

## 3 · Diferencia contra `emite_m.camina()` (el `regenera_todos()` histórico)

`camina()` es el camino que este wrapper **no** toma, en cuatro puntos:

| | `emite_m.camina()` | este medidor |
|---|---|---|
| marco | `marco-M-sorteado-v1_1.tsv` **cableado** en el código | input `origen: repo` declarado en la spec, con SHA |
| escritura | escribe `corridas-M/M-<id>.json` | no escribe nada; `corrida0.py run` sella la salida |
| reanudación | `if destino.exists(): YA-EXISTIA` — saltea | no hay estado previo que saltear: cada corrida es completa |
| esquema | lo lee de `corridas-M/M-TRA-M-01.json` (legado GEN1) | comprueba los campos que consume; **no abre** `corridas-M/` |

## 4 · `ciego_a_R`: verificado, no declarado

`emite_m.py` emite la cadena constante `CIEGO_A_R` en cada registro. Una
constante es una afirmación, no una prueba. Este medidor instala un
`sys.addaudithook` sobre el evento `open` **antes** de importar `emite_m` y
antes de tocar el marco, y cuenta toda apertura del proceso durante la
ventana de emisión. Si alguna ruta cae bajo `corridas-R/`, `corridas-M/`,
`corridas-L/`, `agregado_v1_3.py` o `agregado-v1_3-resultado.json`, el
medidor levanta `AperturaProhibida` y `run` no sella nada.

`RESULT-M-CIEGO-A-R` reporta el conteo de aperturas de la ventana. Su valor
es el recibo del hook, no una constante copiada.

## 5 · El número del paso 3

`RESULT-M-P-DISTINTOS` cuenta cuántos valores **distintos** de `p` produce el
marco vigente sobre sus 14 celdas. Es el dato mecánico que alimenta la
decisión de mesa sobre la unidad de celda (§ A5 del encargo y
`forense/notas/2026-09-08-GEN2-E7-paso-3-unidad-de-celda.md`). El medidor lo
**mide**; no propone ni toma la decisión.

## 6 · Insumos

Los seis inputs son `origen: repo`, versionados y con SHA declarado. Los dos
primeros los consume el medidor directamente; los cuatro restantes los abre
`emite_m` / `emisor.py` durante la emisión y se declaran para que la
identidad de la corrida los cubra: una corrida cuyo `tramite.yaml` cambió no
es la misma corrida.

Este cálculo **no** lee microdato ni resuelve payloads del manifiesto:
`variables: []` y `universo: NO-APLICA` son vacíos **declarados**.

## 7 · Determinismo

`seed.aplica: false` — la emisión no es estocástica. `emite_celda` ya
comprueba internamente que dos invocaciones de `emitir_binaria` sobre la
misma (regla, conducta) coinciden, y levanta si no. `verify` debe dar
`REPRODUCE / IDENTICO`.
