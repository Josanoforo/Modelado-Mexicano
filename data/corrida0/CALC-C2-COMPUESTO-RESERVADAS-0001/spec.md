# CALC-C2-COMPUESTO-RESERVADAS-0001 — C2 compuesto sobre los cruces `RESERVADA`

**ACTO GEN2-C2-COMPUESTO-RESERVADAS-1** · 19/sep/2026 · P2 (COMMIT-2)
Spec sellada que gobierna: `forense/prereg-caja/C2-COMPUESTO-RESERVADAS-spec-v1_0.md`
(congelada en el COMMIT-1, **anterior** a esta corrida).

## 1 · Qué mide

Un punto C2 compuesto por cada celda de cada par de ejes que el dictamen
de emisibilidad (P1) declaró `EMITIBLE`, sobre los **22 cruces
`RESERVADA`** que `data/corrida0/marcador-segmento.tsv` lista.

```
C2(a, b) = expit( logit p(a) + logit p(b) − logit p )
```

La forma **se cita, no se reinventa**: el medidor llega a
`tests/test_celda_d_c2.py::piso_log_aditivo` a través de
`tools/c2_compuesto.py`, que la **importa**. Es la misma función de
referencia que `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/spec.yaml:187`
y `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001/medidor.py:149` sellaron.

## 2 · Universo, unidad y ola — los pone el árbitro

Cada emisión hereda del yaml del árbitro, no del marcador:

| ola | unidad_dato | ponderador | desenlace(s) |
|---|---|---|---|
| ENIF 2024 | PERSONA elegida 18+ | `FAC_PER` | `ahorra_solo_informal` · `informal_cualquiera` |
| ENCIG 2025 | TRÁMITE (quien pagó doce veces contribuye doce veces) | `FAC_TRA` | `adopta_encig2025_luz` |
| ENVIPE 2025 | DELITO | `FAC_DEL` | `evade_norma_envipe2025` |

**Ningún número cruza unidad.** Un punto en unidad DELITO no se lee como
personas; uno en unidad TRÁMITE tampoco.

## 3 · Incertidumbre: cero IC, y el porqué

`tipo_incertidumbre = NO-PROPAGADA-COVARIANZA-NO-SELLADA`. Los marginales
de una misma ola salen de **la misma muestra**; su covarianza **no está
sellada**, y el IC de los C2 ya adoptados se obtuvo en caja réplica por
réplica. Aquí no hay caja y no hay réplicas: **no se fabrica**.

Los `RESULT-C2COMP-DIAG-INF-…` / `…-DIAG-SUP-…` son el recorrido del punto
cuando cada marginal se mueve a los extremos de su IC95. **No son un
intervalo de confianza**: ignoran la covarianza que lo haría uno y no
tienen cobertura declarada. Llevan nombre distinto a propósito.

## 4 · Control de reproducción (independiente, sin microdato)

El par `localidad × edad` de ENIF **ya fue piloteado** — por eso NO
aparece en la lista `RESERVADA` — y `CALC-DIN-AHORRO-SOLO-INFORMAL-
EMISIONES-0001/resultados.json` trae sus ocho puntos C2 sellados. Este
medidor, con los mismos marginales citados y el mismo nacional, debe
reproducirlos al bit.

* `RESULT-C2COMP-CONTROL-ARBITRO` ∈ {`REPRODUCE`, `NO-REPRODUCE`, `NO-EJECUTABLE`}
* umbral `1e-12`, `RESULT-C2COMP-CONTROL-DELTA-MAX-ABS` con el peor delta.
* Un `NO-REPRODUCE` **no invalida las emisiones**: invalida la afirmación
  de que este medidor ejecuta la receta ya sellada. Se reporta sin
  ajustar nada.
* Las claves `…-C2-P-REDERIVADO-…` quedan **fuera** del control: re-derivan
  los marginales desde microdato en vez de citarlos, y difieren del orden
  de 1e-3 por esa razón y no por la forma.

## 5 · Estado y contador

Toda emisión nace `EMITIDA-SIN-EVALUAR`: disponible para exploración,
**excluida de la estimación adoptada del motor y de toda decisión
automática**. Emitir **no consume** la reserva — el cruce sigue
`RESERVADA` para evaluación. Una emisión **no pasa a adoptada por uso**:
sólo por piloto que la evalúe fuera de muestra o por firma de mesa con
alcance declarado.

`cuenta_gen2: SI` se **propone**; nace `PENDIENTE-DE-MESA` salvo firma.
**`adoptados_activos` no se mueve en este acto.**

## 6 · Lo que este CALC no hace

No abre microdato · no deriva ni mira `R` de ningún cruce · no adopta ·
no propaga IC (sucesor en caja) · no evalúa C2 · no elige el cruce del
piloto 3.

## 7 · Auditoría

Un C2 compuesto **supone** que no hay interacción entre los dos ejes en
escala logit; **no lo mide**. Donde la interacción sea real, la emisión
estará **sesgada hacia el centro precisamente en las celdas más
vulnerables**. Cada emisión lo lleva en `supuesto: sin-interaccion`.
Rótulo prohibido: `independencia`.

Los ejes son marcadores de estructura, no rasgos culturales. La rejilla
**no ve región ni condición indígena**: límite declarado. Clase de
evidencia **(a)**; escala **proporción**.
