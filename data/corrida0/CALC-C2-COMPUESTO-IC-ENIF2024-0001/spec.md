# CALC-C2-COMPUESTO-IC-ENIF2024-0001 — IC réplica por réplica de las emisiones C2 de ENIF 2024

**ACTO GEN2-C2-COMPUESTO-IC-ENIF2024-1** · 19/sep/2026 · CAJA · P1 (COMMIT-1)
Spec humana que gobierna: `forense/prereg-caja/C2-COMPUESTO-IC-ENIF2024-spec-v1_0.md`
(congelada en este mismo commit, **antes** de abrir una sola respuesta de ENIF 2024).

## 1 · Qué mide

Un IC95 por celda para cada emisión C2 compuesta de ENIF 2024 que
`CALC-C2-COMPUESTO-RESERVADAS-0001` selló con
`tipo_incertidumbre = NO-PROPAGADA-COVARIANZA-NO-SELLADA`. El número de celdas
**se deriva** del dictamen (`data/corrida0/c2-compuesto-dictamen-v1_0.tsv`,
filas `ola = ENIF 2024`, `veredicto = EMITIBLE`) y del yaml del árbitro, no se
copia: `RESULT-C2IC-ENIF2024-G-N-CELDAS-EMITIBLES`.

```
C2_k = expit( logit p_k(a) + logit p_k(b) − logit p_k )     k = 1 … 10 000
IC95 = [ percentil 2.5, percentil 97.5 ] de las réplicas definidas
```

`p_k(a)`, `p_k(b)` y `p_k` son marginales de **un eje cada uno** (y el nacional),
estimados en la **misma réplica k** del **mismo remuestreo** de la ola: la
covarianza entre marginales de la misma muestra viaja en las réplicas, no se
inventa ni se supone cero. Es el estándar de las 20 celdas ya adoptadas
(`IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS`, piloto 1
`CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001`, piloto 2
`CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001`).

El **punto** de cada celda no se re-deriva: es `piso_log_aditivo` sobre los
marginales **sellados** del árbitro y el nacional citado — el mismo número que
el CALC de emisiones publicó — y el control 1 lo verifica. `…-P-REDERIVADO`
(C2 sobre los marginales de la réplica base) se emite como informativo.

## 2 · Universo, unidad, ola, ponderador — los pone el árbitro

| campo | valor | de dónde |
|---|---|---|
| ola | ENIF 2024 | `milpa/tramite-ola5-propuesta-v0.yaml`, regla `dinero.ahorro.via_informal_ejes_enif2024` |
| payload | `enif_2024_bd_csv.zip` :: `TMODULO.csv` (manifiesto `enif_2024_enif_2024_bd_csv`) | el que leyó el árbitro (`tools/medidor_ahorro_enif24.py:30-31`) |
| unidad | PERSONA elegida 18+ | idem |
| universo | todas las filas de TMODULO tras las guardias del árbitro (`carga()`: `EDAD_V` ≥ 18 y numérica, `FAC_PER` > 0, alguna de las 15 variables de la sección 5 no en blanco; cualquier violación **PARA**) | `tools/medidor_ahorro_enif24.py::carga` |
| ponderador | `FAC_PER`; estrato `EST_DIS`; UPM `UPM_DIS` | idem |
| desenlaces | `ahorra_solo_informal` (PRINCIPAL: alguna `P5_1_1..6 == "1"` y ninguna `P5_6_1..9 == "1"`) · `informal_cualquiera` (SECUNDARIO: alguna `P5_1_1..6 == "1"`) | `tools/medidor_ahorro_enif24.py::desenlaces` |
| ejes | `sexo`, `edad`, `escolaridad`, `localidad`, `cuenta_formal` — cada celda derivada por el `Eje.deriva` del árbitro (`EJES_P2`, `EJE_CUENTA_PRINCIPAL`; `cuenta_formal` usa la misma `deriva` para los dos desenlaces) | `tools/medidor_ahorro_enif24.py:130-181`, `tools/ejes_maestra35_l1.py` |

`formalidad` **no se admite**: `NO-EMITIBLE` por universo restringido
(A-bis 4); el encargo lo dice: no se intenta rescatar.

## 3 · Desviación escrita (mesa, 19/sep/2026)

El encargo manda que el medidor importe `tools/celda_d/marginales_reproduccion.py`
y obtenga los marginales por su `marginal()`. **P0 encontró que ese módulo es
ENVIPE-only**: `carga_ola()` lee `tmod_vic`/`tsdem` con universo `BP1_20` y
`FAC_DEL`; `EJES` admite `escolaridad_proxy`, `dominio_urbano_rural`, `nacional`
y **ninguno** de los cinco ejes del dictamen. Bajo la regla literal de P0 las
136 celdas saldrían `IC-NO-CONSTRUIBLE`. Mesa autorizó (respuesta a la pregunta
de alcance, 19/sep/2026) que el medidor lleve **su propia guardia de una
variable con la misma semántica** — `marginal_enif(ola, grupo: str)`: str
posicional único, whitelist de ejes, huella de la ola, sin `cruce()` — e importe
del árbitro (`tools/medidor_ahorro_enif24.py`) universo, desenlaces y ejes.
`marginales_reproduccion.py` no se modifica; de él se importa `cotejo()`
(control 2) y `marginal()` como sonda mecánica del hallazgo
(`RESULT-C2IC-ENIF2024-G-P0-MODULO-GUARDADO-*`).

## 4 · Réplicas y tratamiento de réplicas degeneradas

Un remuestreo por ola, compartido: `n_h` UPM con reemplazo dentro de cada
estrato, `numpy.random.PCG64(42)`, estratos en orden lexicográfico de `EST_DIS`
y UPM de `UPM_DIS`, **10 000** réplicas — la receta de
`tools/celda_d/marginales_reproduccion.py::replicas_compartidas` (líneas
256-286), citada en `forense/prereg-caja/TRA-evade-norma-sxd12-spec-v1_0.md:166`
y en `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/spec.yaml:171` (10 000) y
`:133-142` (seed 42, PCG64). Se re-escribe en el medidor (`replicas_enif`)
porque la firma del módulo exige una `Ola` de ENVIPE (huella por `ID_DEL`).

Una réplica es **válida** para una celda si sus tres marginales están en el
abierto (0, 1) y tienen denominador (no `NaN`). Las inválidas se **excluyen**
(no se recortan, no se sustituyen) y se cuentan (`…-REPLICAS-VALIDAS`,
`G-REPLICAS-SIN-DEFINIR-TOTAL`). Si las válidas son **menos de 9 900** de
10 000, la celda sale `IC-NO-CONSTRUIBLE:REPLICAS-VALIDAS-<n><9900` con IC
`null`. Si el **punto** es SIN-DEFINIR (`MarginalDegenerado`), la celda sale
`IC-NO-CONSTRUIBLE:PUNTO-SIN-DEFINIR`. Declarado aquí, antes del dato.

## 5 · Dos controles de coherencia — los dos, o no se publica IC

1. **Punto**: `…-P` debe reproducir `RESULT-C2COMP-…` de
   `CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json` a **1e-12** en todas
   las celdas (misma función `piso_log_aditivo`, mismos marginales sellados,
   mismo nacional citado). `G-CONTROL-1-PUNTO-VEREDICTO`.
2. **Árbitro**: cada marginal de la réplica base (la ola entera, sin remuestrear)
   debe reproducir el R sellado del yaml del árbitro — `p` a **1e-6**, `IC95`
   a **1e-4**, `n` **exacto** — en **todas** las celdas de los ejes usados, por
   desenlace, más el nacional citado (`tools/c2_compuesto.py::NACIONALES`).
   Se coteja con `marginales_reproduccion.py::cotejo` (importado), y el
   punto/IC de cada marginal sale de `wprop_ic_conglomerado` (la receta del
   árbitro, importada). `G-CONTROL-2-ARBITRO-VEREDICTO`.

Si cualquiera de los dos es `NO-REPRODUCE`, **todos** los IC salen `null` con
`IC-ESTADO = IC-NO-PUBLICADO:<causa>` y `G-IC-PUBLICADO = NO`: el hallazgo es
ese, se sella como corrida y no se ajusta nada. Un `NO-REPRODUCE` no invalida
las emisiones: invalida la afirmación de que este medidor ejecuta la receta
sellada.

## 6 · Guardia de reserva como código (E.6; NC-0328)

* `marginal_enif`: `TypeError` con dos posicionales o una lista; `ValueError`
  con un eje fuera de la whitelist; `ReservaRota` si la ola fue filtrada,
  reordenada o alterada, o si las réplicas son de otra ola.
* `auditoria_ast()` — dentro del medidor, corrida por `medir()` sobre su propio
  archivo **antes** de abrir el zip, y por
  `tests/test_c2_ic_enif2024_guardia.py` con **un control positivo por regla**:
  R1 imports fuera de lista · R2 `groupby`/`crosstab`/`pivot`/`merge`/`open`/
  `getattr`/… · R3 `.df` fuera del núcleo guardado · R4 ningún nodo combina dos
  comparaciones (`&`, `|`, `*`, `and`, `or`) · R5 `OlaEnif(`/`carga()`/
  `deriva()` sólo donde la spec los pone · R6 `marginal_enif` con un grupo
  atómico · R7 ninguna función de cruce · R8 ninguna constante de archivo o
  instrumento fuera de ENIF 2024 (TMODULO) y ningún `inputs[…]` no declarado.
  Si falla, `SystemExit("PARO · guardia AST …")` con 0 filas leídas.

## 7 · Estado y contador

Las emisiones a las que este IC acompaña siguen `EMITIDA-SIN-EVALUAR`; los
pares siguen `RESERVADA`; este CALC **no adopta**, **no evalúa** C2 contra ningún
R de cruce, **no actualiza el marcador**. `cuenta_gen2: SI` se **propone**; nace
`PENDIENTE-DE-MESA` salvo firma. `adoptados_activos` no se mueve.

## 8 · Lo que este CALC no hace

No toca `marginales_reproduccion.py`, `marcador_segmento.py`,
`estimadores-por-segmento.yaml`, `CALC-C2-COMPUESTO-RESERVADAS-0001` ni
`tools/corrida0.py` · no abre ningún payload que no sea `enif_2024_bd_csv.zip`
:: `TMODULO.csv` · no deriva, no ve, no imprime ningún cruce · no toca
ENCIG 2025 ni ENVIPE 2025.

«El primer resultado que produzca este procedimiento es el que se reporta.»
