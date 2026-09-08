# `CALC-AGG-marco-M-sorteado-v1_3-ola` — dos vistas, cero colapso

`ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`, 8/sep/2026, P3(d)/(e).
Entorno **NUBE**, sin corpus y sin red. **CONTADOR: cero.**

## 1 · La métrica sellada no se toca

`procedimiento-scoring-v1_2.md` y `agregado-v1_3-resultado.json` quedan
exactamente como están: no se leen como insumo y no se reescriben. Este
agregado **añade** dos vistas informativas y no sustituye ninguna cifra de
veredicto. Una vista informativa que se cuela al veredicto es como se pierde
un pre-registro; por eso `RESULT-AGGOLA-METRICA-SELLADA` lo declara en el
propio resultado y no sólo en esta prosa.

## 2 · Vista 1 — por regla

Agrupa las celdas elegibles por su `regla` y cuenta cuántas modulan por ola
y cuántas no. **No promedia los puntos de las celdas de una regla.** Una
mediana por regla sería colapsar por la puerta de atrás: se cuentan celdas,
no se funden números. D-2 dice «no colapsamos» y eso incluye no colapsar en
una vista que se presente como inocua.

## 3 · Vista 2 — por segmento, y por qué sale en cero

Por decisión de este acto (P3a, cierre de `NC-0020`), la celda del marcador
es `regla × segmento (x, sobre los seis ejes del modelo) × ola ×
instrumento`. Las 14 celdas de hoy son el caso `x = ∅` y se conservan.

La vista por segmento reporta **0 celdas con `x ≠ ∅`**, y lo comprueba
contra el esquema del marco (no hay columna de segmento), no contra una
suposición.

Ese cero sólo es informativo junto al otro lado del conteo: la propuesta
`milpa/tramite-ola5-propuesta-v0.yaml` **sí** trae puntos por eje con IC95 —
entradas `_ejes_`, todas `SELLADA` — que **ninguna** celda del marcador
consume (verificado: ni `milpa/src/emisor.py` ni `tools/emite_m.py`
mencionan `ejes`). El hueco no es falta de dato: **es falta de cableado**, y
esta corrida lo mide en vez de describirlo.

## 4 · Cifra corregida respecto del encargo

El encargo de este acto dice «77 entradas `_ejes_` con IC por eje». Medido
contra el árbol: **7 entradas `_ejes_`**, con **24 ejes** y **74 puntos por
eje**, los 74 con `ic95`. La corrida publica las tres cifras por separado
(`ENTRADAS-EJES-EN-PROPUESTA`, `EJES-EN-PROPUESTA`,
`PUNTOS-POR-EJE-CON-IC`) para que la próxima cita no tenga que elegir cuál
de las tres quiso decir «77». La conclusión del encargo no cambia — existen
puntos por eje con IC y el marcador no consume ninguno —; la cifra sí.

## 5 · Por qué `cuenta_gen2: NO`

Por cadena: consume los `RESULT` de `CALC-M-marco-M-sorteado-v1_3-ola`, que
es corredor envuelto LEGACY. La regla E.1 es transitiva por construcción y
`corrida0` la propaga sola — no depende de que alguien se acuerde de
etiquetar esta spec.

## 6 · Determinismo

`seed.aplica: false`. Tres insumos versionados con SHA declarado; contar y
agrupar no es estocástico.
