# B-REMESAS · Pre-registro del ENSAYO de la línea base temporal `B` sobre la serie de remesas de ENIGH 2016→2022

### `prereg-caja-B-REMESAS` · **v1.0** · 8 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/B-REMESAS-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-B-REMESAS`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de correr `CALC-B-0001`, del primer ENSAYO de `tools/baseline_temporal.py` (el selector `B`, sha `886f2da4…`, `PR #620`) sobre dato real: la proporción ponderada de hogares con remesas en las cuatro olas de ENIGH Nueva Serie 2016, 2018, 2020 y 2022 ya en corpus. Mide, ola a ola, **qué predice «la tasa de ayer» contra la observada** — el piso común contra el que `L` y `M` tendrán que competir bajo el MISMO corte informativo (D-2 / `FP-348`, FIRMADA). |
> | **QUÉ NO ES** | **No es una medición de regla y ninguna cifra suya entra a un veredicto** (`T9`, verbatim: *«Nada de promediar ni ajustar tendencias. Es modelo nuevo y va a C0-B con spec propia antes de que ninguna cifra suya entre a un veredicto.»*). No mueve `R5.1` ni ninguna otra: `familia.seguro.volatilidad_ausencia_estado` sigue con el `p` que `PR #447` le selló. No promedia olas, no ajusta tendencia, no extrapola, no imputa. No modifica el selector: lo consume tal cual está sellado. No descarga nada: las cuatro olas están en corpus desde el 30/jul/2026. |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight CALC-B-0001` en VERDE antes de correr; después `python3 tools/corrida0.py verify CALC-B-0001`. La reproducción del punto 2022 contra la cifra ya sellada del motor (`0.045694`) es el control positivo externo de que el medidor mide lo que dice medir — está pre-declarado en §6 con sus TRES ramas y su consecuencia en cada una. |

**Acto:** `ACTO GEN2-C0-B · LA BASE`, 8/sep/2026, entorno **CAJA (UBUNTU)**, corpus montado, sobre `origin/main = 017ac24` (`PR #645`).

---

## 0 · Premisas del encargo verificadas contra el árbol, y la contaminación declarada

### 0.1 · Dos premisas del encargo NO se reproducen; ninguna de las dos bloquea

El encargo declara: *«ENIGH 2016-2024 ya está en corpus (34 entradas de manifiesto, verificado)»*. Verificado contra el árbol, con el comando a la vista:

```
$ python3 -c "…yaml.safe_load(data/manifiesto.yaml)… entradas cuyo id empieza en 'enigh20'"
enigh2012_nc_csv · enigh2014_nc_csv · enigh2016_nc_csv
enigh2018_nc_csv · enigh2020_nc_csv · enigh2022_nc_csv     → 6 entradas, no 34
$ ls /home/pc0/mm-corpus/raw/ | command grep -icE "enigh"   → 6
```

1. **Son SEIS entradas de manifiesto, no 34** (2012, 2014, 2016, 2018, 2020, 2022). El «34» no se reproduce por ninguna vía: ni entradas de manifiesto, ni archivos en la raíz `data_raw`.
2. **ENIGH 2024 NO existe en ninguna de las dos raíces.** `data_raw`: 0 coincidencias. Raíz `descargas_mx`: 0 coincidencias en el censo del día (`forense/censo-raiz/2026-09-08.txt`, 466 archivos en disco, 4 nuevos, 462 ya registrados) — A.8 satisfecha con censo del día, de modo que esto es **AUSENTE-EN-RAIZ**, no `NO-VERIFICADO`.

**Ninguna de las dos bloquea este ensayo**, porque el rango que el propio encargo nombra dos veces (título de P1 y cuerpo: *«remesas ENIGH 2016→2022»*) está íntegro en corpus. El universo de esta spec es exactamente ese rango. Las olas 2012 y 2014 **existen en corpus y quedan deliberadamente FUERA** del universo congelado: alargar la serie es de un acto sucesor, no una decisión que este ensayo tome sobre la marcha (queda como fila `## NO-CORRIDO / RESERVAS`).

### 0.2 · Contaminación declarada (ADR-46) — al congelar esta spec YA se había leído la serie observada

Esta declaración es obligatoria y se escribe **antes** de cualquier cifra, no después. Al ejecutar P2 del mismo encargo (*«las DOS reglas con serie … leerla del NC completo»*) esta sesión abrió `milpa/tramite.yaml:850-856`, que publica la serie GEN1 ya sellada de **exactamente la cantidad que este ensayo va a re-medir**: la proporción ponderada de hogares con `remesas > 0` en las seis olas de ENIGH NS. Verbatim de lo leído, para que nadie tenga que confiar en el resumen:

| ola | `p` (GEN1, `serie_olas`) | `ic95` (GEN1) | `n` | ponderador |
|---|---|---|---|---|
| 2012 | 0.044704 | [0.039340, 0.050420] | 9 002 | `factor_hog` |
| 2014 | 0.040784 | [0.036551, 0.044978] | 19 479 | `factor_hog` |
| **2016** | **0.047459** | [0.045192, 0.049807] | 70 311 | `factor` |
| **2018** | **0.047285** | [0.045093, 0.049555] | 74 647 | `factor` |
| **2020** | **0.043775** | [0.041877, 0.045680] | 89 006 | `factor` |
| **2022** | **0.045694** | [0.043754, 0.047711] | 90 102 | `factor` |

**Consecuencia, dicha sin adornos: el ensayo NO es ciego.** El procedimiento obligatorio del encargo (leer el NC completo para P2) es la vía por la que la contaminación entró — es el mismo patrón que ya se pagó antes en este programa, y se asienta aquí en vez de descubrirse al cerrar.

**Qué se hace con eso, en vez de fingir que no pasó.** El criterio de lectura de §5 se ancla a una cantidad que **no se elige**: el propio IC95 de la ola objetivo, medido por esta corrida. No hay ningún umbral libre que esta sesión pueda haber calibrado hacia el resultado que ya conoce. Y las consecuencias derivables de lo ya leído se **pre-declaran explícitamente en §5.3**, como derivación de metadato ya leído y no como pronóstico ciego, para que mesa las descuente si quiere.

**Qué sigue siendo genuinamente desconocido al congelar:** los valores `float64` que produzca el medidor GEN2 (los de arriba están redondeados a seis decimales), los extremos del IC95 bajo el bootstrap de ESTA spec (semilla y método propios, distintos de los de la corrida GEN1), y por lo tanto el veredicto `DENTRO-IC` de cada objetivo — que en al menos un caso (§5.3) se juega en el quinto decimal.

### 0.3 · Un defecto de metadato del propio payload, sellado aquí antes de usarlo

Los 17 archivos `metadatos/*.txt` de `enigh2022_nc_csv.zip` declaran, los 17 igual:

```
Temporal: 2021-08-11-2021-11-28
```

Es decir: el metadato de ENIGH **2022** declara un período de levantamiento de **2021**. No es una errata de un archivo — es sistemática en el payload, y es incompatible con el `Identifier: MEX-INEGI.ESD3.03-ENIGH-2022-NS` del mismo archivo y con el patrón de sus tres olas hermanas (2016: `2016-08-11 2016-11-18`; 2018: `2018-08-21-2018-11-28`; 2020: `2020-08-21-2020-11-28`).

**Esta spec no lo corrige y no lo usa.** El período operativo de cada ola se define en §2.2 por el **año calendario de la ola**, que se deriva del `Identifier` y no del campo roto; el `Temporal` de las cuatro olas se sella verbatim como RESULT de texto para que el defecto quede en `resultados.json` y no sólo en esta prosa.

---

## 1 · La cantidad que se mide

**Serie:** proporción ponderada de hogares que reportan ingreso por remesas, por ola de ENIGH Nueva Serie.

- **Unidad de observación y de análisis:** el hogar, identificado por `folioviv` + `foliohog` en `concentradohogar`.
- **Universo:** el universo completo de `concentradohogar` de la ola, **sin filtro adicional** — idéntico al que `milpa/tramite.yaml` declara para `familia.seguro.volatilidad_ausencia_estado`, deliberadamente, para que el punto 2022 sea comparable contra la cifra ya sellada (§6).
- **Desenlace:** `recibe_remesas = 1` si `concentradohogar.remesas > 0`, `0` si `remesas == 0`. `remesas` está declarada `N (12,2)` en el diccionario de datos de las cuatro olas — *«Ingresos provenientes de otros países»* (2016, 2018) / *«REMESAS»* (2020) / *«Σ de ingresos.ing_tri cuando clave está en {P041}»* (2022).
- **Ponderador:** `factor` en las cuatro olas. No se usa `factor_hog` (que es el nombre en 2012/2014, olas fuera de este universo).
- **Estimando:** `p_ola = Σ factor·1[remesas>0] / Σ factor`, una ola a la vez, **jamás agrupadas ni promediadas**.

### 1.1 · La rama NA no existe — y eso es una guardia que PARA, no un supuesto heredado

`milpa/tramite.yaml` afirma que *«`remesas` trae cero nulos en las 6 olas (verificado, no supuesto)»*. Esta spec **no hereda esa afirmación**: la vuelve a medir y la convierte en compuerta.

- El medidor cuenta y publica `RESULT-B-ENIGH-<ola>-N-NULOS-REMESAS`.
- **Si esa cuenta es > 0 en cualquier ola, esa ola sale `VEREDICTO = NO-ESTIMABLE-NULOS-INESPERADOS`, con `p` / `IC` en `null`, y no se fabrica ninguna rama NA sobre la marcha.** La dicotomización pre-registrada tiene dos ramas y sólo dos.
- Guardia gemela sobre el ponderador: sólo entran filas con `factor` finito y `> 0`; la cuenta que entra es `RESULT-B-ENIGH-<ola>-N`.

---

## 2 · Cómo se le habla al selector `B`

El selector (`tools/baseline_temporal.py`) es **cálculo puro y no se modifica**. Consume `Serie`, `Objetivo` y una lista de `Observacion`. Esta spec congela exactamente qué se le pasa.

### 2.1 · La llave de igualdad de serie (`Serie`), idéntica para las cuatro olas

```
encuesta      = "ENIGH-NS"
reactivo      = "concentradohogar.remesas"
universo      = "hogares del universo completo de concentradohogar, sin filtro adicional"
codificacion  = "recibe_remesas = 1 si remesas > 0, 0 si remesas == 0"
segmento      = "nacional"
unidad        = "proporcion"
```

Las cuatro olas comparten llave **por construcción del diseño de ENIGH NS**, no por semejanza: mismo instrumento, misma variable derivada, mismo universo, misma escala. El selector rechaza por `OTRA_SERIE` cualquier cosa que no case campo por campo; esa igualdad se declara aquí y se sella en `spec.yaml`, no la decide el medidor.

### 2.2 · Períodos y fecha de corte — derivados del año de la ola, no del `Temporal` roto

Por la razón de §0.3:

- `periodo_inicio(ola) = <ola>-01-01`, `periodo_fin(ola) = <ola>-12-31`.
- `fecha_corte(objetivo) = <objetivo − 1>-12-31` — el último día del año anterior al de la ola objetivo. Es el corte informativo: **lo que se podía saber antes de que la ola objetivo empezara**.

Esta definición es uniforme, verificable desde el `Identifier` del payload, y **preserva el orden estricto entre olas**, que es lo único que el selector necesita de los períodos.

### 2.3 · `disponible_desde` — y por qué hay DOS brazos, no uno

El docstring del selector es explícito: *«`disponible_desde` corresponde a la versión del insumo utilizada, no necesariamente a su primera publicación ni a la ejecución CALC.»* La versión que el corpus tiene de cada ola declara su propia fecha en el campo `Modified` de sus metadatos, idéntico en los 12/17 archivos de cada zip:

| ola | `Modified` (versión en corpus) | `Temporal` (verbatim del payload) |
|---|---|---|
| 2016 | **2021-11-29** | `2016-08-11 2016-11-18` |
| 2018 | **2021-11-29** | `2018-08-21-2018-11-28` |
| 2020 | **2021-07-28** | `2020-08-21-2020-11-28` |
| 2022 | **2023-07-26** | `2021-08-11-2021-11-28` ⚠ (§0.3) |

Eso separa dos preguntas que colapsarían en una sola si sólo hubiera un brazo, y las dos importan para `C0-D`:

- **Brazo `OPERATIVO`** — `disponible_desde = Modified`. Contesta: **¿qué podía decir `B` en su momento, con las versiones que este corpus efectivamente tiene?** Es el brazo honesto sobre disponibilidad: si la versión que tenemos de una ola se publicó después del corte, `B` no podía leerla y se abstiene.
- **Brazo `PERSISTENCIA`** — `disponible_desde = periodo_fin` (el valor más temprano que el selector admite: valida `disponible_desde >= periodo_fin`). Es el contrafáctico declarado *«si cada ola hubiera estado disponible el día que cerró su levantamiento»*. Contesta: **¿cuánto vale la persistencia de una ola a la siguiente, aislada del rezago de publicación?**

Los dos brazos usan **el mismo selector sin tocarlo**: lo único que cambia es el metadato de entrada. `publicada = true` en las cuatro olas (microdato público de INEGI), en los dos brazos.

### 2.4 · Objetivos

Tres: **2018, 2020 y 2022**. La ola 2016 no tiene predecesora dentro del universo congelado y por lo tanto **no es objetivo** — no se le busca una previa fuera del universo (eso sería alargar la serie por la puerta de atrás; ver §0.1).

---

## 3 · IC95 — método, y la ranura que esta spec llena declarándolo

ENIGH NS es una muestra probabilística estratificada por conglomerados: `est_dis` (estrato de diseño) y `upm` (unidad primaria de muestreo) vienen en `concentradohogar`.

- **Método:** bootstrap de UPM **con reemplazo dentro de cada estrato**, conservando el número de UPM por estrato; percentiles 2.5 / 97.5. `B = 2000` réplicas. Semilla `20260908`, RNG `numpy.PCG64`, los dos declarados en `spec.yaml`.
- Es la **misma familia de método** que `CALC-0002` ya usó y declaró como ranura no pre-registrada por su spec sellada. Aquí se declara igual: **nadie pre-registró el método de IC para esta serie; lo elige el ejecutor sobre ranura vacía, se declara y se eleva a mesa.** No se hereda de la corrida GEN1 (cuyo método fue `bootstrap-conglomerado` de otro acto y otra implementación) y por eso **no se espera coincidencia dígito a dígito de los extremos** — sólo del punto (§6).
- `n_minimo_celda = 10`. Por debajo, IC en `null` y `VEREDICTO = NO-ESTIMABLE`.

---

## 4 · Lo que el ensayo emite

Por cada ola (2016, 2018, 2020, 2022): `P`, `IC-LO`, `IC-HI`, `N`, `N-NULOS-REMESAS`, `HOGARES-EXPANDIDOS` (Σ `factor`, control externo contra la cifra que `serie_olas` publica), `VEREDICTO`, `METADATO-TEMPORAL` (verbatim, §0.3).

Por cada objetivo (2018, 2020, 2022) **y cada brazo** (`OPERATIVO`, `PERSISTENCIA`): `ESTADO` (`EMITE` / `SIN_BASELINE`), `METODO` (el que el selector devuelva), `FUENTE` (qué ola eligió), `P` (la predicción), `ERROR` (`P_B − P_observada`, con signo), `ERROR-ABS`, `DENTRO-IC` (`SI` / `NO` / `SIN-BASELINE`) y `MARGEN-AL-BORDE` (distancia con signo de la predicción al extremo más cercano del IC95 observado; positivo = dentro).

Agregados: `N-PREDICCIONES` por brazo, `LECTURA` por brazo (§5), y los dos RESULT de la pre-declaración de adopción (§6).

---

## 5 · B-bis — la lectura, escrita ANTES de correr

### 5.1 · El criterio, por objetivo

**`B` predice bien un objetivo si su predicción cae DENTRO del IC95 de la proporción observada de esa ola.** Leído en voz alta: *la línea base no es distinguible de la verdad a la precisión que la propia encuesta permite.*

El criterio no tiene ningún parámetro que esta sesión pueda elegir: el umbral es el IC95 que esta misma corrida mide.

### 5.2 · La lectura agregada, por brazo

Sobre los objetivos que **emiten** en ese brazo (los que se abstienen no cuentan ni a favor ni en contra, y su número se reporta aparte):

| lectura | condición | qué significa para `C0-D` |
|---|---|---|
| `PISO-ALTO` | todas las predicciones del brazo caen dentro del IC95 | El piso es alto: `M` y `L` tienen **vara seria**. Ganarle a «la tasa de ayer» exige una mejora que sobreviva al IC95, no una diferencia decimal. |
| `PISO-BAJO` | ninguna cae dentro | La serie **se mueve** más de lo que la persistencia captura: el corpus y el modelo tienen algo real que ganar. |
| `MIXTO` | unas sí y otras no | El piso depende de la ola: `C0-D` no puede tratar `B` como constante y tiene que reportar la comparación **ola a ola**, nunca agregada. |
| `SIN-PREDICCIONES` | el brazo se abstiene en los tres objetivos | El resultado es sobre **disponibilidad**, no sobre persistencia: `B` no pudo hablar. Es un hallazgo del corte informativo, no una medida de calidad. |

### 5.3 · Lo que ya se puede derivar de metadato y de cifras YA LEÍDAS — declarado como derivación, no como pronóstico ciego

Por §0.2 esta sesión ya conoce la serie GEN1, y por §2.3 ya leyó los `Modified`. Sería deshonesto presentar como predicción lo que es aritmética sobre datos ya leídos. Se deja escrito **antes** de correr, para que el resultado no pueda re-narrarse después:

1. **Brazo `OPERATIVO`: se espera `SIN_BASELINE` en 2018 y en 2020.** Las versiones que el corpus tiene de 2016 y 2018 se publicaron el **2021-11-29**, posterior a los cortes `2017-12-31` y `2019-12-31`; el selector debe excluirlas por `NO_DISPONIBLE_AL_CORTE`. Para 2022 (corte `2021-12-31`) las tres previas son elegibles y debe seleccionar **2020**, que es la de `periodo_fin` mayor. Esperado: **1 predicción de 3**.
2. **Brazo `PERSISTENCIA`: se esperan las tres predicciones**, cada objetivo desde su ola inmediatamente anterior.
3. **Sobre `DENTRO-IC`, con las cifras GEN1 redondeadas de §0.2** — y sujeto a que el medidor GEN2 reproduzca esos puntos y a que el bootstrap de esta spec dé extremos propios: 2018 (`B` = 0.047459 vs. IC 2018 `[0.045093, 0.049555]`) cae dentro con holgura; 2020 (`B` = 0.047285 vs. IC 2020 `[0.041877, 0.045680]`) cae **fuera** por encima; 2022 (`B` = 0.043775 vs. IC 2022 `[0.043754, 0.047711]`) cae dentro **por 2.1 × 10⁻⁵**. Lectura agregada esperada del brazo `PERSISTENCIA`: `MIXTO`.
4. **La llamada de 2022 roza el borde y se pre-declara como tal.** Un margen de 2.1 × 10⁻⁵ es más chico que la diferencia esperable entre dos bootstraps con semillas distintas. **Si 2022 se voltea, eso NO es un hallazgo: es ruido de borde**, y el medidor lo dice solo — `MARGEN-AL-BORDE` publica el margen con signo, y la nota de cierre reporta cualquier objetivo con `|MARGEN-AL-BORDE| < 1e-4` bajo el rótulo **`ROZA-EL-BORDE`**, con las dos cifras, en vez de contarlo como si fuera una decisión limpia.

---

## 6 · Pre-declaración de adopción (P3) — escrita antes de correr, con TRES ramas

`RESULT-B-ENIGH-2022-P` mide exactamente la cantidad que
`milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:recibe_remesas`
materializa hoy con `p: 0.045694` (clase `MEDIDO·p(tasa base ponderada)`), medida por el
aparato GEN1. Es, por lo tanto, **el primer RESULT del programa que ES una probabilidad de
conducta del motor** y no un delta, un marginal de antecedente o un veredicto — y por eso es
el único candidato de adopción real que existe hoy (la derivación completa, con sus tres
hallazgos, va en la nota de cierre del acto).

La adopción sólo se escribe si puede escribirse **sin crear un `FAIL` nuevo**. `T35 (c)`
compara el valor materializado por el consumidor contra el RESULT usando la **tolerancia de
replay declarada por este CALC** (`tolerancia.abs`, §`spec.yaml`), que es la tolerancia con
que `verify` decide `REPRODUCE`. El motor materializa sus probabilidades con **seis
decimales**; la tolerancia de replay de una corrida determinista es de orden `1e-10`. Son dos
granos distintos servidos por un solo campo, y esta spec **no los colapsa ni afloja la
tolerancia de replay para que la adopción pase** — declara las tres ramas y deja el hecho a la
vista:

| rama | condición sobre `Δ = RESULT-B-ENIGH-2022-P − 0.045694` | qué se hace |
|---|---|---|
| `ADOPTABLE` | `\|Δ\| <= tolerancia.abs` | Se escribe la cita (`corrida0_resultado_id` + `corrida0_generacion: GEN2`) en ese nodo, **sin tocar `p`**. La sella el merge de mesa: **el PR ES la firma** (E.2, humana). |
| `NO-ADOPTABLE-POR-GRANO` | `tolerancia.abs < \|Δ\| < 1e-6` | La re-medición GEN2 **sí** reproduce la cifra sellada al grano con que `milpa/` materializa (seis decimales), pero no al grano con que `verify` compara. **La cita NO se escribe** — escribirla sería introducir a sabiendas un `FAIL` nuevo en `T35 (c)`. El hecho, con su `Δ`, es el hallazgo, y va a `forense/no-corrido.tsv` con sucesor nombrado. |
| `NO-ADOPTABLE-POR-DISCREPANCIA` | `\|Δ\| >= 1e-6` | La re-medición GEN2 **no** reproduce la cifra GEN1 del mismo payload. La cita no se escribe y **eso es EL hallazgo**, mayor que cualquier adopción: se reporta con las dos cifras y el signo, sin disfrazarse de otra cosa. |

El medidor publica `RESULT-B-ADOPCION-P3` (la rama) y `RESULT-B-ADOPCION-P3-DELTA` (el `Δ` con
signo), de modo que la decisión queda en `resultados.json` y no en la prosa de nadie.

**Lo que esta spec NO hace para que la adopción pase:** no afloja `tolerancia.abs`, no redondea
ningún RESULT, no reescribe el `p` del motor y no firma `data/corrida0/decisiones.tsv`. Si la
adopción no cabe hoy, el entregable es la medida exacta de por qué no cabe.

---

## 7 · Lo que esta spec explícitamente NO autoriza

1. **No mueve ninguna regla.** `R5.1` conserva su tier, su `p`, su `ic95` y su `serie_olas` intactos. Ninguna cifra de este ensayo entra a un veredicto (`T9`).
2. **No promedia ni ajusta tendencia.** `B` es persistencia de UNA ola; el selector no admite otra cosa y esta spec no le añade nada.
3. **No alarga la serie.** 2012 y 2014 quedan fuera del universo (§0.1).
4. **No corrige el metadato de INEGI** (§0.3): lo sella verbatim y lo esquiva por diseño.
5. **No firma el contador.** `etiquetas.cuenta_gen2` queda en `PENDIENTE-DE-MESA`; escribir una fila en `data/corrida0/decisiones.tsv` sería falsificar una firma de mesa, y ese archivo no está en el perímetro de este acto.

---

## 8 · Sello

Esta spec queda congelada en el `COMMIT-1` del `ACTO GEN2-C0-B`, antes de que el medidor lea un solo byte de microdato de ENIGH. **El primer resultado que produzca este procedimiento es el que se reporta.**
