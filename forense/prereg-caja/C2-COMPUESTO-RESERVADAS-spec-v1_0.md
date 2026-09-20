# C2 COMPUESTO SOBRE LOS CRUCES `RESERVADA` — spec v1.0

**ACTO GEN2-C2-COMPUESTO-RESERVADAS-1** · 19/sep/2026 · base `8e455bd6`
Encargo archivado (A.3): `forense/encargos/2026-09-19-GEN2-C2-COMPUESTO-RESERVADAS-1.md`

Esta spec congela el procedimiento ANTES de que exista una sola emisión.
Lo que sigue se escribió contra el dictamen de emisibilidad (P1) y el
COMMIT-1 lo sella; las emisiones (P2) llegan en el COMMIT-2.

> **El primer resultado que produzca este procedimiento es el que se
> reporta.** No hay segunda corrida elegible, no hay recorte, no hay
> sustitución de marginales y no hay ajuste post-hoc de la forma.

---

## 0 · Firma de mesa que autoriza (verbatim)

> "Se emite C2 compuesto para cada par `RESERVADA` cuyos marginales
> compartan desenlace, universo, unidad y ola; el resto queda
> `NO-EMITIBLE` con causa. Estado `EMITIDA-SIN-EVALUAR`: disponible para
> exploración, excluida de la estimación adoptada del motor y de toda
> decisión automática. Una emisión no pasa a adoptada por uso: solo por
> piloto que la evalúe fuera de muestra o por firma de mesa con alcance
> declarado. Ninguna ola reservada se abre."

**A.4/A.13 sobre el adjunto.** La firma cita el careo
`CAREO-PILOTO-3-direccion-2026-09-19.md` §4, sha256/16 `796689c4dce6f43d`,
"que viaja adjunto". Ese archivo **NO está en el árbol y no llegó
adjunto**: `git ls-tree -r --name-only HEAD | grep -ic "CAREO-PILOTO"` →
`0` sobre **5 769 archivos examinados**. El sha256/16 declarado por tanto
**NO se verificó** — estado `NO-VERIFICABLE-AQUÍ`, no `FALSO`. Lo que sí
está archivado verbatim, y es lo que este acto ejecuta, es el **texto
operativo** de la firma, que viaja dentro del encargo (A.3). Queda como
fila `NO-CORRIDO` con sucesor.

## 1 · Qué gobierna, y qué no se toca

| Papel | Archivo |
|---|---|
| Marginales `R` con IC95 y `n` (el árbitro) | `milpa/tramite-ola5-propuesta-v0.yaml` |
| Lista de cruces reservados | `data/corrida0/marcador-segmento.tsv` (22 `RESERVADA` + 1 `CONSUMIDA-SIN-PILOTO`) |
| Nacionales | `milpa/tramite.yaml` (ver §3) |
| Forma de C2 (sellada, se importa) | `tests/test_celda_d_c2.py::piso_log_aditivo` |

**No se toca** ningún payload de ola alguna, el yaml del árbitro, las
celdas-D, `tools/corrida0.py`, `milpa/tramite.yaml` ni
`tools/celda_d/marginales_reproduccion.py`. **Cero microdato**: la única
entrada numérica de este acto son marginales ya sellados y publicados.
`data/raw/` está ausente en este entorno (nube) y no se pidió.

## 2 · La forma de C2 — se cita, no se reinventa

```
C2(a, b) = expit( logit p(a) + logit p(b) − logit p )
```

con `p` el **nacional** del mismo desenlace, misma ola, mismo universo y
mismo ponderador. Sellada dos veces en el árbol:

* `data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/spec.yaml:187`
  (`c2_forma: "log-aditiva: expit(logit(p_l) + logit(p_e) - logit(p))"`)
* `data/corrida0/CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001/medidor.py:149`

`tools/c2_compuesto.py` **importa** `piso_log_aditivo` de
`tests/test_celda_d_c2.py`; no la reimplementa. De ahí hereda, sin
relajarlas, las dos guardias que esa función ya trae:

* los tres marginales deben declarar el **mismo** `desenlace_id`
  (`DesenlaceIncompatible`);
* ningún marginal puede ser exactamente 0 o 1 (`MarginalDegenerado`): el
  logit diverge, la celda queda **SIN-DEFINIR** y **no se recorta a
  [0,1] ni se sustituye**.

**Rótulo obligatorio del supuesto:** `sin-interaccion` (ausencia de
interacción en escala logit). **Rótulo prohibido:** `independencia`. C2 no
identifica `P(Y | a, b)`: es un piso declarado y sólo-marginal.

## 3 · El nacional que se usa, y de dónde sale

Uno por desenlace, citado y **no recalculado**. La `clase` viaja verbatim
porque distingue `MEDIDO` de `DERIVADO`, y esa distinción llega a la
emisión:

| desenlace | p | IC95 | n | clase | fuente |
|---|---|---|---|---|---|
| `ahorra_solo_informal` | 0.357153 | — (sin IC propio) | 13 502 | DERIVADO de A, B y A∪B de MAESTRA34-L5 P4 | `milpa/tramite.yaml:1312`, `milpa/tramite-ola5-propuesta-v0.yaml:1127` |
| `informal_cualquiera` | 0.561920 | [0.549922, 0.573502] | 13 502 | MEDIDO·p(tasa base ponderada) | `milpa/tramite.yaml:1317`, `milpa/tramite-ola5-propuesta-v0.yaml:1131` |
| `adopta_encig2025_luz` | 0.673393 | [0.663165, 0.683910] | 20 203 | MEDIDO·p(tasa base ponderada, universo N_TRA=01) | `milpa/tramite.yaml:400`, `:427-432` |
| `evade_norma_envipe2025` | 0.562774 | [0.551982, 0.573448] | 40 280 | MEDIDO·p(tasa base ponderada, unidad delito) | `milpa/tramite.yaml:497`, `:519-524` |

Es el **mismo** nacional que el C2 ya sellado usó (`marginales_sellados_D9.NAC`
= 0.357153, n = 13 502, `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/spec.yaml`).
Que uno de los cuatro sea `DERIVADO` y sin IC propio no lo descalifica
como nacional — descalifica cualquier lectura de su IC, que no existe.

## 4 · Criterio de emisibilidad (P1), campo por campo

La firma pone cuatro condiciones; el encargo añade el ponderador. Se leen
del yaml del árbitro, **no del marcador**:

1. **desenlace** — los dos ejes viven bajo el mismo bloque de `desenlaces:`
   (o bajo el `ejes:` plano de la regla) y hay un nacional sellado para él.
2. **universo** — el de la regla; ningún eje con `universo_restringido: true`.
3. **unidad** — la del `payload:` del árbitro.
4. **ola** — la del `payload:` del árbitro.
5. **ponderador** — el de la regla.

y las guardias de la forma: ningún marginal con `p` ausente, ni `p ∈ {0,1}`.

**Unidad: el árbitro manda, no el marcador.** El marcador escribe
`unidad_dato = persona` para ENCIG (vía `_unidad_dato()`), mientras el
árbitro declara `unidad = TRÁMITE (quien pagó doce veces contribuye doce
veces)`. La emisión hereda la del **árbitro** — que es la que el encargo
nombra ("delito / trámite / persona elegida 18+"). El dictamen conserva
las dos columnas, `unidad_dato_arbitro` y `unidad_dato_marcador`, para
que la discrepancia quede a la vista y no se resuelva en silencio.

**Un par, varios desenlaces.** El marcador agrupa por `(regla, par)` y
colapsa los desenlaces (`_camina_ejes` toma el `max` sobre bloques). La
firma emite "para cada par cuyos marginales compartan desenlace", así que
el dictamen se abre a `(par × bloque de desenlace)`: ENIF tiene
`principal` (`ahorra_solo_informal`) y `secundario` (`informal_cualquiera`),
y **los dos se emiten**, cada RESULT rotulado con su `desenlace_id`.
Emitir sólo uno sería elegir por el ejecutor cuál de dos marginales
sellados cuenta.

### Casos que dirección ya vio y que NO se fuerzan

* **ENIF `formalidad`** — `cobertura: 0.689676`, `universo_restringido:
  true` (A-bis 4): vive en el universo de quien trabaja y no reconcilia
  contra el marginal poblacional ni contra el nacional. **NO-EMITIBLE** con
  todo eje de universo completo.
* **ENUT `reparto_hogar × sexo_edad`** — `reparto_hogar` es un **estimador
  de RAZÓN** sobre 29 181 hogares (`FAC_HOG`) y `sexo_edad` una **MEDIA de
  horas/semana** sobre 74 053 personas 12+ (`FAC_PER`): distinta unidad,
  distinto universo, distinto ponderador, ningún desenlace binario común,
  ningún nacional, y valores fuera de [0,1] (hasta 28.31) donde el logit
  no existe. `sexo_edad` es además un eje **ya compuesto**. **NO-EMITIBLE**
  por cinco causas independientes; basta la primera.
* **Marginales con p = 0 o 1** — rechazo por `MarginalDegenerado`, sin
  recorte ni sustitución. Verificado: ninguno de los marginales de los 22
  pares cae en ese caso.

### Reserva que NO bloquea la emisión, y viaja con ella

ENIF, desenlace **principal**, eje `cuenta_formal`: `P5_4_*` gatea a
`P5_6_*`, así que en la celda `sin cuenta` el desenlace principal se
**reduce por construcción del cuestionario** a `informal_cualquiera`
(propuesta:1489-1492) — el eje es NO-FALSABLE contra ese desenlace. Las
cinco condiciones de la firma se cumplen y la composición es aritmética,
así que se emite; la reserva viaja en el campo `reserva` de cada RESULT.
No se convierte en `NO-EMITIBLE` por cuenta del ejecutor: la firma
enumera cuatro condiciones y ésta no es una.

## 5 · Incertidumbre: no se fabrica

Los marginales de una misma ola salen de **la misma muestra**; su
covarianza **no está sellada**, y el IC de los C2 ya adoptados se obtuvo
en caja **réplica por réplica**
(`tipo_incertidumbre: IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS`).
Aquí, sin caja y sin réplicas:

* `tipo_incertidumbre = NO-PROPAGADA-COVARIANZA-NO-SELLADA`
* `ic95_inf` y `ic95_sup` **vacíos** en las 206 celdas. Cero.

Se reporta **aparte y rotulado como diagnóstico**, en
`diagnostico_rango_inf` / `diagnostico_rango_sup` con
`diagnostico_rango_es_ic = NO`, el recorrido del punto cuando cada
marginal se mueve a los extremos de su IC95 (ocho esquinas cuando los
tres tienen IC; menos cuando el nacional no lo tiene, que es el caso de
`ahorra_solo_informal`). **Ese rango no es un intervalo de confianza**:
ignora la covarianza que lo haría uno, y por construcción no tiene
cobertura declarada. El IC real es sucesor en caja (§8).

`cotas_frechet_n` viaja como contexto de soporte — lo único que los
márgenes acreditan sobre la intersección (H4) — y **no entra al punto**.

## 6 · Estado de la emisión

`EMITIDA-SIN-EVALUAR`. Disponible para exploración; **excluida** de la
estimación adoptada del motor y de toda decisión automática. Emitir **no
consume** la reserva: el cruce sigue `RESERVADA` para evaluación, en
columna distinta. Una emisión pasa a adoptada **sólo** por piloto que la
evalúe fuera de muestra o por firma de mesa con alcance declarado —
nunca por uso. `adoptados_activos` no se mueve en este acto.

## 7 · Control de reproducción (independiente, sin microdato)

El par `localidad × edad` de ENIF **ya fue piloteado** y por eso no está
en la lista `RESERVADA` — lo que lo hace un control externo gratuito:
`CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/resultados.json` trae sus
ocho puntos C2 sellados. Este procedimiento, alimentado con los mismos
marginales citados y el mismo nacional, debe reproducirlos **al bit**.

* Umbral: `|delta| <= 1e-12` en las ocho celdas.
* Rama negativa: `NO-REPRODUCE` con el delta con signo y **sin ajustar
  nada**; no invalida las emisiones, invalida la afirmación de que este
  procedimiento ejecuta la receta ya sellada.
* Las claves `…-C2-P-REDERIVADO-…` del mismo CALC **no** entran al
  control: re-derivan los marginales desde microdato en vez de citarlos,
  y difieren del orden de 1e-3 por esa razón y no por la forma.

Congelado en `tests/test_c2_compuesto.py`.

## 8 · Lo que este acto NO hace

No abre microdato · no deriva ni mira `R` de ningún cruce · no adopta ·
no propaga IC (**sucesor en caja**: IC réplica por réplica con el módulo
guardado de una sola variable de agrupación) · no evalúa C2 · no elige el
cruce del piloto 3.

## 9 · Módulo de auditoría (afirma sobre México: aplica completo)

Un C2 compuesto **supone** que no hay interacción entre los dos ejes en
escala logit; **no lo mide**. Donde la interacción sea real — edad ×
escolaridad en gobierno digital, brecha de acceso por cohorte — la
emisión estará **sesgada hacia el centro precisamente en las celdas más
vulnerables** (mayores con baja escolaridad, localidades chicas sin
cuenta): es donde un lector aplicado más se equivocaría. Cada emisión lo
lleva encima en el campo `supuesto: sin-interaccion`.

Los ejes son **marcadores de estructura** (ingreso, formalidad, oferta
institucional), **no rasgos culturales**. La rejilla **no ve región ni
condición indígena**: límite declarado, no omisión.

Clase de evidencia: **(a)**. Escala: **proporción**. Unidad por fila;
**ningún número cruza unidad** — un punto en unidad DELITO no se lee como
personas, ni uno en unidad TRÁMITE como personas (ENCIG cuenta doce veces
a quien pagó doce veces).

Lectura peligrosa por simple: *"el motor ya estima todos los segmentos"*.
Estima **bajo un supuesto** que dos pilotos no refutaron y que **ninguno
ha probado en estos cruces**.
