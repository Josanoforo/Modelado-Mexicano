# CALC-AGG-marco-M-sorteado-v1_3 — el agregado del marcador, derivado

ACTO GEN2-E7 · READINESS-2 · Pieza A, A4.

## 1 · Qué es

Una corrida **derivada**: no mide nada, agrega `RESULT-R/M/L` por celda que
otras corridas ya sellaron. Hoy consume dos insumos, ambos `origen: repo` y
ambos versionados:

- `data/corrida0/CALC-M-marco-M-sorteado-v1_3/resultados.json` — los
  `RESULT-M-*` de las 14 celdas.
- `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv` — el marco vigente, que
  fija **cuáles** son las celdas del universo.

## 2 · `ci_replayable: true`

Todos sus insumos son archivos del árbol con SHA declarado. No hay corpus, no
hay red, no hay clave, no hay directorio listado en disco. Cualquiera con el
repositorio reproduce esta corrida.

## 3 · Qué lo separa de `agregado_v1_3.py` (LEGACY)

`agregado_v1_3.py` resuelve sus insumos por **convención de nombre de
archivo** sobre el legado GEN1 —
`ORDEN_RESOLUCION_M = ("M-{id}__v1_3.json", "M-{id}.json", "M-{id}__v1_2.json")`—
y lista `corridas-M/`, `corridas-R/` y `corridas-L/`. Un archivo suelto en
cualquiera de esos tres directorios entra a la cifra sin que nada lo declare,
y su `a13_conteo_archivos_examinados` arrastra un doble conteo heredado que el
propio script documenta y no corrige.

Este sucesor consume **solo lo declarado**. `agregado_v1_3.py` queda LEGACY y
vive como smoke (`CALC-SMOKE-0001`), no como productor.

## 4 · Los ejes que hoy no se pueden estimar

Ni R ni L tienen corrida GEN2:

- **R** necesita corpus (`data/raw/`), que no vive en NUBE. Su corrida va a
  caja, en E5 o después. `tools/arbitra_gen2.py` deja lista la resolución
  exacta y la spec de `CALC-R-<celda>`; no las ejerce.
- **L** necesita al modelo. `forense/prereg-duelo-v2/corredor_l_v1_2.py` deja
  listo el plan de 224 corridas; CONTADOR cero, ninguna llamada hecha.

Este agregado **no rellena ese hueco**. Reporta `RESULT-AGG-N-CON-R = 0`,
`RESULT-AGG-N-CON-L = 0` y deja `RESULT-AGG-EJE-M-VS-R` y
`RESULT-AGG-EJE-M-VS-L` en `NO-ESTIMABLE` con el motivo escrito. Lo que puede
afirmar de M lo afirma; lo que no, lo declara.

El día que existan `CALC-R-*` y `CALC-L-*`, entran **por la spec** — se
agregan como inputs `IN-CALC-R-RESULTADOS` / `IN-CALC-L-RESULTADOS` y su SHA
los identifica. El medidor ya los consume si están; no hay que tocarlo.
`tests/test_corredores_gen2.py::t_agg_entra_R_y_L_cuando_existen_sin_tocar_el_medidor`
ejerce ese camino hoy, para que el hueco no se descubra el día que importe.

## 5 · El delta contra GEN1

**No se calcula aquí.** Mientras R y L no tengan corrida GEN2, un delta contra
`agregado-v1_3-resultado.json` compararía dos cosas distintas: un agregado de
tres ejes contra uno de un eje. Cuando exista, el encargo permite esa lectura
como input `valor_legacy` — una lectura declarada en la spec, no un insumo del
cálculo. Hoy ninguna spec de este acto la declara.

## 6 · `RESULT-AGG-M-P-DISTINTOS`

Se re-deriva aquí desde los `RESULT-M-*`, en vez de copiar
`RESULT-M-P-DISTINTOS`. Es a propósito: si el agregado y el corredor no
coinciden, algo se movió entre las dos corridas y el `verify` de ambas lo
dice. Copiar el número haría imposible notarlo.

## 7 · Determinismo

`seed.aplica: false` — agregar no es estocástico. Sin bootstrap: los IC del
agregado legado salían de replicar sobre las tres corridas; con un solo eje
disponible no hay nada que replicar, y fabricar un IC de un eje solo sería
inventar precisión. `verify` debe dar `REPRODUCE / IDENTICO`.
