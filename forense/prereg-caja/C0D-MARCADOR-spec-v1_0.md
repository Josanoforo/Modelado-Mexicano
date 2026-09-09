# C0D-MARCADOR · Pre-registro del **marcador GEN2** — la pareada `L_SOLO ↔ L_CORPUS` como comparación de primera clase

### `prereg-caja-C0D-MARCADOR` · **v1.0** · 9 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/C0D-MARCADOR-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-C0D-MARCADOR`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de calcular una sola cifra, de `CALC-C0D-MARCADOR`: el marcador GEN2 que hace, **por primera vez en el programa, la comparación pareada `L_SOLO ↔ L_CORPUS`** sobre las 14 celdas del marco sellado `marco-M-sorteado-v1_3.tsv`. Es la comparación que D-2 / `FP-348` declara de primera clase y que **el diagnóstico D4 vigente nunca hizo**: `agregado_v1_3.py::_metrica_secundaria_pp` sólo parea `L_SOLO vs M` y `L_CORPUS vs M`. |
> | **QUÉ NO ES** | **No re-captura nada.** No toca `corridas-L/`, ni `corridas-M/`, ni `corridas-R/`, ni el motor, ni ningún `CALC` previo ni sus sellos. No re-ejecuta `agregado_v1_3.py` ni edita una línea suya. No mueve ninguna regla ni ningún `tier`: **ninguna cifra de este marcador entra a un veredicto de regla** (`T9`). No adjudica la banda `z` primaria del duelo, que sigue siendo la de `agregado_v1_2.main()` y **no se toca**. |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight CALC-C0D-MARCADOR` en VERDE antes de correr; después `python3 tools/corrida0.py run CALC-C0D-MARCADOR` y `python3 tools/corrida0.py verify CALC-C0D-MARCADOR`. El **control de convergencia** de §3.4 —re-derivar los puntos `L` desde las 224 capturas crudas y compararlos contra los que `agregado-v1_3-resultado.json` ya selló— es el control positivo externo de que este marcador lee lo mismo que el duelo. |

**Acto:** `ACTO GEN2-C0-D · EL MARCADOR`, 9/sep/2026, entorno **CAJA (UBUNTU)**, corpus montado, sobre `origin/main = b711ee0` (`PR #647`, `ACTO GEN2-PRIMERA-SILLA`, `ADR-424`).

**Firma que lo autoriza, verbatim de mesa (D-2 / `FP-348`, FIRMADA):** *«la idea central de todo este proyecto es un LLM puede superar a LLM con dato (todo el corpus), si esto no está claro ahorita entonces no estamos comparando correctamente.»*

---

## 0 · Premisas del encargo verificadas contra el árbol

Las cuatro se verifican **antes** de congelar, con el comando a la vista. Dos se reproducen, dos no — y ninguna de las dos que no se reproducen bloquea, pero **las dos cambian el alcance de lo que este marcador puede afirmar**, así que se congelan aquí como límites y no se descubren al escribir la nota.

### 0.1 · «la pareada `L_SOLO ↔ L_CORPUS`» — SE REPRODUCE que NO existe hoy

```
$ command grep -c "L_SOLO_vs_L_CORPUS\|L_solo_vs_L_corpus" forense/prereg-duelo-v2/agregado_v1_3.py
0
```

`agregado_v1_3.py::_metrica_secundaria_pp` construye exactamente dos conjuntos pareados —`pares_l_solo_m` y `pares_l_corpus_m`— y dos comparaciones —`L_SOLO_vs_M` y `L_CORPUS_vs_M`. **La pareada entre los dos brazos de `L` no está implementada en ningún lado del árbol.** El hallazgo que dirección asentó el 8/sep (`L_CORPUS 19.60 · L_SOLO 11.69 · M 4.51`) es, por construcción, una comparación de **marginales** `MAE_pp`, no una pareada. Ésa es la razón por la que hoy es marginal y no veredicto, y es lo que este acto existe para arreglar.

### 0.2 · «B de `CALC-B-0001` como piso» — SE REPRODUCE, pero cubre **2 de 14 celdas**, no 14

El encargo pide `B` como «piso común de los tres». Verificado contra el árbol:

```
$ python3 -c "…csv marco-M-sorteado-v1_3.tsv… (id, encuesta, ola, conducta)"
FAM-M-05  ENIGH 2016  recibe_remesas
FAM-M-06  ENIGH 2018  recibe_remesas
FAM-M-07  ENIGH 2020  recibe_remesas
… (11 celdas restantes: ENVIPE, ENNViH/MxFLS, ENIF, ENCUCI, ENCIG — otras conductas)
$ python3 -c "…json data/corrida0/CALC-B-0001/resultados.json… ids con -P"
RESULT-B-PERSISTENCIA-{2018,2020,2022}-P · RESULT-B-OPERATIVO-{2018,2020,2022}-P
```

`CALC-B-0001` predice la ola objetivo a partir de la anterior de la MISMA serie (ENIGH · `recibe_remesas`). Por tanto:

| celda | ola | `B` disponible | por qué |
|---|---|---|---|
| **FAM-M-06** | 2018 | **SÍ** — `RESULT-B-PERSISTENCIA-2018-P` / `RESULT-B-OPERATIVO-2018-P` | tiene ola previa (2016) dentro del universo congelado de `B` |
| **FAM-M-07** | 2020 | **SÍ** — `RESULT-B-PERSISTENCIA-2020-P` / `RESULT-B-OPERATIVO-2020-P` | tiene ola previa (2018) |
| FAM-M-05 | 2016 | **NO** — `SIN-BASELINE-PRIMERA-OLA` | 2016 es la primera ola del universo congelado de `B`; no hay ola anterior. No se fabrica una con 2014, que `B-REMESAS` §0.1 dejó deliberadamente fuera |
| las otras 11 | — | **NO** — `SIN-BASELINE-FUERA-DE-SERIE` | `B` es una línea base **temporal de la misma serie**; ENVIPE/ENNViH/ENIF/ENCUCI/ENCIG no están en su universo. Un `B` para ellas sería un `B` nuevo, no éste |

**Consecuencia congelada:** `B` entra a este marcador como **piso citado sobre 2 celdas**, con su `corrida0_resultado_id`, y **`MAE_pp(B)` NO se calcula ni se compara contra los otros tres corredores** — `n = 2` no sostiene un agregado, y compararlo contra un `MAE` de 14 celdas violaría A-bis 4. Se reporta como `PISO-CITADO-COBERTURA-PARCIAL`. Extender `B` al resto del marco es un acto sucesor, no una decisión que este marcador tome sobre la marcha.

### 0.3 · «capturas vigentes del duelo» — SE REPRODUCE; y su corpus es **anterior a GEN2**

```
$ python3 -c "…json corridas-L/*.json… (variante, fecha_congelacion, timestamps)"
L+corpus  n=152  fecha_congelacion=2026-09-01  ts 2026-09-01T20:35 → 2026-09-02T16:20
L-solo    n=152  fecha_congelacion=2026-09-01  ts 2026-09-01T20:30 → 2026-09-02T16:17   (marco-M)
L-solo    n=120  fecha_congelacion=2026-08-26  ts 2026-08-26T19:53 → 2026-08-26T20:27   (piloto, 15 celdas SIN brazo L+corpus)
modelo_id = claude-opus-4-6 · temperatura = 1.0 · k_corridas = 8, en los tres bloques
```

**Los dos brazos del marco-M se capturaron en la MISMA ventana (1–2/sep/2026), con el mismo modelo, la misma temperatura y la misma `k`.** Eso es lo que hace lícita la pareada: el brazo no está confundido con la fecha ni con el modelo.

**Y ése es exactamente el límite de alcance:** el corpus que vio el brazo `L+corpus` es el corpus **al 1–2 de septiembre de 2026**. Los actos de adquisición y de registro GEN2 posteriores no estaban en él. Este marcador mide, por tanto, **el efecto del corpus de esa fecha**, no el del corpus GEN2. `RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES` cuantifica la brecha contando entradas de `data/manifiesto.yaml` con `fecha_descarga > 2026-09-02`, y §5.3 fija qué hace la adjudicación con ese número **antes** de conocerlo.

### 0.4 · «14 celdas» — SE REPRODUCE, y las 14 tienen los dos brazos completos

Las 14 filas de `marco-M-sorteado-v1_3.tsv` traen `grado_DD = "P1 PUNTUA"` **todas**, así que la exclusión `VERIFICACION-NO-PUNTUA` del §5 del procedimiento sellado no retira ninguna. Y las 14 tienen 8 capturas en cada brazo (`L-<id>-M__L-solo__01..08` y `…__L+corpus__01..08`): 224 archivos. Las 15 celdas del piloto (`CIV-08`, `DIN-03/05/07/11`, `DOC-06`, `EMP-02/04/05`, `SFT-04/06`, `TIC-01/06/08/12`) **sólo tienen brazo `L-solo`** y quedan **FUERA** del universo de este marcador, declarado aquí y no descubierto al correr.

---

## 1 · La cantidad que se mide

Todo lo de esta sección se copia, sin reinterpretar, del procedimiento **ya sellado** `procedimiento-scoring-v1_2.md` §7 tal como `agregado_v1_1.py` y `agregado_v1_3.py` lo implementan. **Este marcador no inventa métrica; inventa la comparación que faltaba.**

### 1.1 · Punto por celda y corredor

- **`L_SOLO` / `L_CORPUS`** — media de `valor_extraido` sobre las réplicas del brazo con `valor_extraido` no nulo, de las 8. Si las 8 son nulas, el punto es `NO-DISPONIBLE`; **no se sustituye por 0 ni por nada** (verbatim de `agregado_v1_1._leer_l_variante`).
- **`M`** — `valor_punto` del archivo que resuelve el orden §16 de `MAESTRA38-M13`: `M-<id>__v1_3.json` → `M-<id>.json` → `M-<id>__v1_2.json`, primera coincidencia exacta, sin otra heurística.
- **`R`** — campo `R` de `corridas-R/<id>.json` cuando `estado == "COMPUTADO"`; su `EE_R` acompaña. Si no es `COMPUTADO`, la celda no tiene patrón oro y **sale de todo agregado**.
- **`B`** — §0.2: `RESULT-B-PERSISTENCIA-<ola>-P` (brazo primario) y `RESULT-B-OPERATIVO-<ola>-P` (secundario) de `CALC-B-0001`, citados por `corrida0_resultado_id`, sólo en `FAM-M-06` y `FAM-M-07`.

### 1.2 · Error, escala declarada (A-bis 3)

`err_pp(corredor, celda) = 100 · (punto − R)`, **con signo**. Unidad: **puntos porcentuales de una proporción ponderada**. No es probabilidad de conducta, no es efecto, no es coeficiente: es la distancia de un corredor al patrón oro de su celda, dentro de una misma corrida. Comparable entre celdas del mismo marco porque **todas** las 14 son `escala = binaria` y su `R` es una proporción — verificado en §0.4, no supuesto.

### 1.3 · La guardia de universo (A-bis 4) — y por qué es el corazón de este acto

`agregado_v1_3.py` calcula `MAE_pp` de cada corredor sobre *«el universo de 14 **o el subconjunto con punto de corredor disponible**»*, **independientemente por corredor**. Es decir: `MAE_pp(L_SOLO)`, `MAE_pp(L_CORPUS)` y `MAE_pp(M)` **pueden estar calculados sobre conjuntos de celdas distintos**, y su comparación directa —que es la que produjo `19.60 / 11.69 / 4.51`— sería entonces una comparación entre universos distintos.

Este marcador, por tanto, emite **dos familias de `MAE_pp`**, y las distingue en el `id` del RESULT:

- `RESULT-C0D-MAE-MARGINAL-<corredor>` — cada corredor sobre **su propio** subconjunto disponible. **Reproduce D4 y sirve sólo para comparar contra él.**
- `RESULT-C0D-MAE-COMUN-<corredor>` — cada corredor sobre el **universo común** `U∩`: las celdas donde `R`, `L_SOLO`, `L_CORPUS` y `M` tienen los cuatro punto. **Ésta es la única que A-bis 4 autoriza a comparar entre corredores.**

Y emite el diagnóstico mecánico de si la distinción muerde: `RESULT-C0D-UNIVERSOS-IDENTICOS` (`SI`/`NO`) y el `n` de cada uno.

---

## 2 · La comparación primaria: la pareada `L_SOLO ↔ L_CORPUS`

**Universo:** `U_LL` = celdas con `R` computado **y** punto en `L_SOLO` **y** punto en `L_CORPUS`. Misma celda, misma escala, mismo `R`, misma ventana de captura, mismo modelo — **la única diferencia entre los dos números que se restan es si el corredor tenía el corpus delante** (§0.3).

**Diferencia por celda, con signo:**

```
d_i = |err_pp(L_CORPUS, i)|  −  |err_pp(L_SOLO, i)|
```

**`d_i > 0` significa que el corpus ALEJÓ a `L` del patrón oro en esa celda.** El signo se fija aquí, antes del dato, para que no haya lectura de conveniencia después.

**Estadístico:** media de `d_i` sobre `U_LL`, con IC95 por **bootstrap no paramétrico sobre celdas**, con la maquinaria **ya sellada** del duelo, consumida desde los bytes verificados por `sha256` de `forense/prereg-duelo-v2/scoring-adv1-m3.py` — `generar_indices_bootstrap`, `derivar_seed_scope`, `_cuantil_7` — y con los mismos parámetros sellados: **`seed = 42`**, **`replicas = 10000`**, **`nivel_ic = 0.95`**, `scope_id = "mae_pp::pareado::L_CORPUS_vs_L_SOLO::c0d_v1_0"`. Ni un parámetro se elige aquí: se citan.

---

## 3 · Comparaciones secundarias — se reportan como tales, no adjudican

Multiplicidad declarada al modo de `S6`: **la primaria decide; las secundarias se reportan y no mueven el veredicto.** Se calculan sobre `U∩` salvo donde se diga.

### 3.1 · `L_SOLO ↔ M` y `L_CORPUS ↔ M`

Mismo estadístico, `d_i = |err_pp(L, i)| − |err_pp(M, i)|`, con sus `scope_id` propios. Reproducen las dos pareadas que D4 sí hace — **sobre `U∩`**, que es donde son comparables entre sí.

### 3.2 · `M ↔ B`

Sólo sobre las 2 celdas de §0.2, brazo `PERSISTENCIA` como primario y `OPERATIVO` como secundario. **`n = 2`: se emite el par de errores crudo y NO un IC** — un bootstrap sobre dos celdas no es un intervalo, es un adorno. Se reporta `NO-ADJUDICA-POR-N`.

### 3.3 · La guardia de conmensurabilidad de `B` (A-bis 4)

`B` mide su propia observada de la ola (`RESULT-B-ENIGH-<ola>-P`, universo completo de `concentradohogar`). El duelo mide `R` de la misma ola con **su** universo y **su** estimador. Antes de usar `B` como piso, el marcador comprueba mecánicamente que las dos son la misma cantidad:

- Si `|RESULT-B-ENIGH-<ola>-P − R(celda)| ≤ 1.96 · EE_R(celda)` → `PISO-CONMENSURABLE`.
- Si no → **`PISO-NO-CONMENSURABLE`**: `B` se reporta con su cita y su cifra, **y no entra a ninguna comparación**. No se ajusta, no se re-escala, no se explica al vuelo.

### 3.4 · Control de convergencia — el marcador contra el agregado sellado

El medidor re-deriva los 28 puntos `L` (14 celdas × 2 brazos) **desde las 224 capturas crudas** con la regla de §1.1, y los compara contra los que `agregado-v1_3-resultado.json` ya selló. Emite `RESULT-C0D-CONTROL-CONVERGENCIA-L` = `CONVERGE` / `DIVERGE:<lista>` y `RESULT-C0D-CONTROL-MAXDIF-L`.

**`DIVERGE` no es un fallo del marcador: es el hallazgo de que el agregado vigente está desfasado de las capturas**, y en ese caso §5.4 manda. Se declara aquí porque *«convergencia entre dos lecturas corrobora la LECTURA, no el mecanismo»*: este control dice que estoy leyendo las mismas capturas que el duelo, y **nada más que eso**.

---

## 4 · B-bis — las tres ramas de la pareada, escritas ANTES del dato

Sea `IC95(media d)` = `[lo, hi]` sobre `U_LL`, y `n_LL = |U_LL|`.

**Precedencia — se evalúa en este orden y la primera que aplica decide:**

| # | rama | condición mecánica | lectura |
|---|---|---|---|
| **0** | **`NO-ESTIMABLE-POR-COBERTURA`** | `n_LL < 10` | **No adjudica, cualquiera que sea el intervalo.** Una pareada sobre menos de 10 de las 14 celdas del marco no sostiene un veredicto sobre «el corpus»; se reporta el punto y se nombra sucesor. Esta guardia **precede a todas las demás** y existe porque una spec congelada puede salir degenerada por cobertura sin que nadie lo note. |
| **1** | **`CORPUS-ESTORBA`** | `lo > 0` | El corpus **aleja** a `L` del patrón oro, pareado y con el mismo universo. Es la rama que **CONFIRMA** el hallazgo del 8/sep. |
| **2** | **`CORPUS-AYUDA`** | `hi < 0` | El corpus **acerca** a `L` al patrón oro. Es la rama que refuta el hallazgo del 8/sep y sostiene D-2 en su lectura directa. |
| **3** | **`NO-DISCRIMINA`** | `lo ≤ 0 ≤ hi` | La pareada **no distingue** los dos brazos. El hallazgo del 8/sep no sobrevive como veredicto: era una diferencia entre marginales que la pareada no confirma. |

**Ninguna otra rama existe.** Si el cómputo produce algo que no cae en las cuatro (por ejemplo `U_LL` vacío), el veredicto es `NO-ESTIMABLE-POR-COBERTURA` por la rama 0, con `n_LL = 0` escrito.

**Y la lectura que NO se autoriza:** que `CORPUS-ESTORBA` signifique *«el corpus es malo»*. Este marcador mide **un modelo, una ventana de captura, 14 celdas, un corpus fechado**; A-bis 1–2 (asociación, no efecto) aplican íntegras. El enunciado máximo que la rama 1 autoriza es: *«con el corpus del 1–2/sep delante, este corredor se alejó más del patrón oro en estas 14 celdas»*.

---

## 5 · La adjudicación del hallazgo `corpus-empeora` — pre-declarada

El encargo pide que este acto convierta el hallazgo en veredicto **o lo explique**. Las ramas se fijan aquí, antes del dato.

**Precedencia — la primera que aplica decide:**

### 5.1 · `EXPLICADO-POR-UNIVERSO`
Si `RESULT-C0D-UNIVERSOS-IDENTICOS = NO` **y** el orden de los tres `MAE-COMUN` difiere del orden de los tres `MAE-MARGINAL`. Lectura: `19.60 / 11.69 / 4.51` comparaba corredores medidos sobre conjuntos de celdas distintos (A-bis 4); corregido el universo, la ordenación cambia. El hallazgo era un artefacto de universo.

### 5.2 · `EXPLICADO-POR-METRICA`
Si los universos son idénticos (o su corrección no cambia el orden) **pero** la pareada cae en `NO-DISCRIMINA`. Lectura: la diferencia entre marginales `MAE_pp` existe, pero **no sobrevive al pareo** — es decir, no es una diferencia por celda sino la sombra de unas pocas celdas con error grande. Se nombra cuáles (`RESULT-C0D-CELDAS-DOMINANTES`: las de mayor `|d_i|`).

### 5.3 · `CONFIRMADO-CON-ALCANCE`
Si la pareada cae en `CORPUS-ESTORBA`. **El alcance es obligatorio y ya está escrito** (§0.3): *el corpus del 1–2 de septiembre de 2026*, un modelo (`claude-opus-4-6`), `k = 8`, temperatura 1.0, 14 celdas del marco `v1_3`. `RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES` cuantifica cuánto corpus entró después. **Sea cual sea ese número, el sucesor se nombra igual** —re-captura `L_CORPUS` con corpus GEN2, fase 5 del plan de dirección— y **no se ejecuta aquí**; el número sólo gradúa la urgencia, no la existencia del sucesor.

### 5.4 · `NO-ADJUDICA-POR-CONTROL`
Si `RESULT-C0D-CONTROL-CONVERGENCIA-L = DIVERGE`. Entonces el agregado vigente y las capturas no dicen lo mismo, y **eso** es el hallazgo que se reporta primero: adjudicar sobre una lectura desfasada sería adjudicar sobre nada. Precede a 5.1–5.3 en la escritura de la nota **aunque se evalúe al final**, porque invalida el insumo de todas.

### 5.5 · `NO-ESTIMABLE-POR-COBERTURA`
Rama 0 de §4.

---

## 6 · Lo que el marcador emite

Todo `RESULT` con `tipo`, `unidad` y escala declarada, según `data/corrida0/CALC-C0D-MARCADOR/spec.yaml`, que es la cara mecánica de este documento. Las familias:

1. **Por celda** (14 × 6): `R`, `EE_R`, `err_pp` de los tres corredores, y `d_i` de la pareada.
2. **`MAE_pp`** marginal y común, por corredor, con su `n` y su IC95.
3. **Las tres pareadas** (`punto`, `ic_lo`, `ic_hi`, `n`): la primaria `L_CORPUS ↔ L_SOLO` y las dos secundarias contra `M`.
4. **`B`**: cita, cifra, conmensurabilidad y error, en las 2 celdas de §0.2.
5. **Veredictos**: `RESULT-C0D-VEREDICTO-PAREADA` (§4) y `RESULT-C0D-ADJUDICACION-HALLAZGO` (§5).
6. **Controles y alcance**: convergencia, universos, payloads posteriores.

---

## 7 · Lo que esta spec explícitamente NO autoriza

- No autoriza re-capturar `L` con otro corpus: eso es el sucesor de §5.3.
- No autoriza tocar la banda `z` primaria del duelo ni `agregado_v1_*.py`.
- No autoriza mover ninguna regla, `tier`, `p` ni veredicto del motor (`T9`).
- No autoriza extender `B` fuera de la serie ENIGH·remesas (§0.2).
- No autoriza incorporar las 15 celdas del piloto, que no tienen brazo `L+corpus` (§0.4).
- No autoriza aflojar `tolerancia.abs` para que una adopción pase (precedente `PRIMERA-SILLA` §1: para eso existe `tolerancia_adopcion`).

---

## 8 · Sello

**Parámetros congelados:** `seed = 42` · `replicas = 10000` · `nivel_ic = 0.95` · `n_minimo_pareada = 10` · `k_umbral_conmensurabilidad = 1.96` · `tolerancia_convergencia_L = 1e-9`.

**Frase de sello, verbatim:** *el primer resultado que produzca este procedimiento es el que se reporta.*
