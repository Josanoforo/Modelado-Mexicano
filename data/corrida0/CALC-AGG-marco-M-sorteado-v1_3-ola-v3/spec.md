# `CALC-AGG-marco-M-sorteado-v1_3-ola-v3` — el filtro de IC95 que el nombre prometía

> **Sucesora de `CALC-AGG-marco-M-sorteado-v1_3-ola-v2`** (`repite_de`), que
> queda `SELLADA` con sus bytes intactos — no se retoca (E.3). Mismos tres
> inputs, mismo universo, misma Vista 1/Vista 2. Única diferencia mecánica:
> `RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC` ahora filtra de verdad por `ic95`.

`ACTO GEN2-MANTENIMIENTO-3`, 16/sep/2026, `NC-0241`. Entorno **NUBE**, sin
corpus y sin red. **CONTADOR: cero.**

## 1 · El defecto que este acto corrige

`ACTO GEN2-MARCADOR-C0-D` (15/sep/2026) midió, contra el RESULT sellado de
`CALC-AGG-marco-M-sorteado-v1_3-ola-v2`: el nombre `RESULT-AGGOLA-PUNTOS-
POR-EJE-CON-IC` promete un conteo filtrado por la presencia de `ic95`, pero
`medidor.py:114` de v2 contaba `len(e["celdas"])` de cada entrada `_ejes_`
sin mirar ese campo — un `ic95: null` contaba igual que un `ic95: [lo, hi]`
real. De las 74 celdas que v2 reporta, **64 sí traen `ic95`** y **10 no**:
las 10 son una sola entrada y un solo eje —
`familia.cuidado.reparto_mujeres40_ejes_enut2024`, eje `sexo_edad` —
descriptivo por diseño (10 celdas sexo×tramo de edad, «sin signo
pre-registrado», tope declarado `DISCRIMINA`; ver su propia `nota` en
`milpa/tramite-ola5-propuesta-v0.yaml`). Importa porque `NC-0024`, la nota
de `GEN2-T9 §6.c` y la nota de cierre de `GEN2-C0-D` citaban el 74 como
premisa — la cifra defendible para «puntos **con** IC» es **64 de 74**.

`RESULT-AGGOLA-METRICA-SELLADA` de v2 sigue siendo cierto: esta corrida no
toca `procedimiento-scoring-v1_2.md` ni `agregado-v1_3-resultado.json`, y el
defecto no cambió ningún veredicto — el hueco de cableado que v2 medía
(0 celdas del marcador consumen puntos por eje) sigue siendo 0. Lo que
cambia es sólo la etiqueta correcta del numerador de una vista informativa.

## 2 · Vista 1 y Vista 2 — sin cambios

Idénticas a v2: agrupación por regla sin promediar puntos (§2 de
`CALC-AGG-marco-M-sorteado-v1_3-ola-v2/spec.md`), y la vista por segmento en
cero porque el marco vigente no trae columna de segmento (§3 de la misma).
Este acto no las toca ni las reinterpreta.

## 3 · Las cuatro cifras del lado del árbitro, publicadas por separado

Para que ninguna cita futura tenga que adivinar cuál de las cifras quiso
decir «puntos con IC»:

- `RESULT-AGGOLA-PUNTOS-POR-EJE-TOTAL` — 74, idéntico al `-CON-IC` de v2
  (control de continuidad: el universo de celdas no cambió).
- `RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC` — 64, **corregido**: sólo celdas con
  `ic95 is not None`.
- `RESULT-AGGOLA-PUNTOS-POR-EJE-SIN-IC` — 10, el complemento exacto.
- `RESULT-AGGOLA-EJES-SIN-IC` — la lista de qué entrada/eje aporta esos 10,
  para que el residuo no quede anónimo.

## 4 · `RESULT-AGGOLA-CORRECCION-NC-0241`

Campo de texto nuevo, dedicado, que declara el defecto de v2 y la cifra
corregida dentro del propio `resultados.json` — no sólo en esta prosa —
mismo criterio que `RESULT-AGGOLA-METRICA-SELLADA` usó para blindar contra
una lectura descontextualizada del RESULT.

## 5 · Por qué `cuenta_gen2: NO`

Misma cadena que v2: consume (indirectamente, vía v2 y `CALC-M-marco-M-
sorteado-v1_3-ola-v2`) corredor envuelto LEGACY. La regla E.1 es transitiva
por construcción.
