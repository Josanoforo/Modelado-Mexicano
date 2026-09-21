# DIN · lote de cruces ENIF 2024 · `ahorra_solo_informal` × 14 pares — spec humana **v1.0 · CONGELADA**

**Universo, unidad y escala, en la primera línea.** Personas **elegidas de 18 años y más**
de ENIF 2024 (tabla `TMODULO`, una fila por persona), ponderadas por `FAC_PER`, con
`EST_DIS` × `UPM_DIS` como estrato y conglomerado; **universo del piloto 1 (régimen
`PILOTO-1`, §1)**. La cantidad estimada es una **proporción de personas en `[0,1]`**; el
error se reporta en **puntos porcentuales (pp)**. No se compara contra ENCIG (unidad
trámite) ni contra el duelo nacional; ninguna cifra se suma a otra escala sin enlace.

> `ACTO GEN2-DIN-LOTE-ENIF2024-COMMIT-1`, 21/sep/2026, CAJA, rama
> `acto/gen2-din-lote-enif2024-commit-1`. **Sucede** a
> `DIN-lote-enif2024-spec-v0_1-PROPUESTA.md` (sha256
> `8c2381bed701a2aa98e58eae4ad3d3cf1ec3508d550f6f8e399669aa55a76a9f`, intacta, no se
> edita). Firmas verbatim en el repo: F1 y F2 `FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-01/-02`;
> D-22 ampliada `-8a1f-05`; enmienda v0.3 `FP-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-01`;
> **opción A** de dirección (21/sep): «R2 entra solo con λ = ½ en todo el lote; no se
> armoniza un `D8` de 2018». Lo que la PROPUESTA dejó abierto **se cierra aquí** y se marca
> con **[CIERRA]**; lo que este acto encontró distinto de lo que el encargo suponía se marca
> con **[HALLAZGO]** y va a mesa en §16.
>
> Contrato ejecutable: `data/corrida0/CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/spec.yaml`
> (COMMIT-2) y `…-ADJUDICACION-0001/spec.yaml` (COMMIT-3), generados por
> `tools/lote_enif2024/genera_specs.py` desde el árbitro y los sellos; el código que mide
> es `tools/lote_enif2024/enif_lote.py`, depositado byte a byte como `medidor.py`.
> **Ningún parámetro vive en dos sitios**: los números están en `spec.yaml`; aquí, las
> reglas.
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

---

## 1 · Qué mide, universo y régimen

**Estimando por celda.** `p(ahorra_solo_informal │ eje_A, eje_B)`: proporción ponderada de
personas del universo que, en la ventana de referencia de ENIF 2024, **ahorraron por
alguna vía informal y por ninguna vía formal** del conjunto declarado:

```
informal := alguna de P5_1_1 … P5_1_6 == "1"
formal_9 := alguna de P5_6_1 … P5_6_9 == "1"   (2024)  |  P5_7_1 … P5_7_9 (2021, mismo texto)
D9       := informal AND NOT formal_9            ← desenlace primario y único
```

Códigos `"1"` = Sí; todo lo demás (incluido blanco por secuencia del gate `P5_4_k`) cuenta
como No. Las filas con un código fuera de `{"1","2",""}` se **cuentan y se emiten**
(`…-FILAS-CODIGO-FUERA-DE-DOMINIO`), nunca se descartan en silencio. `D7` no se reabre.

**Filtros del universo — régimen `PILOTO-1`, en este orden y sin ninguno más**, idénticos
en las dos olas: (1) `18 ≤ edad ≤ 97` (`EDAD` en 2021, `EDAD_V` en 2024; `97` es «97 años y
más» en los dos FD y **cuenta como edad**; `98`/`99` son centinelas, salen del universo y
su conteo se emite); (2) `TLOC ∈ {1,2,3,4}`; (3) ponderador presente y `> 0` (`FAC_ELE`
en 2021, `FAC_PER` en 2024: el mismo objeto con otro nombre, FP-379·ENMIENDA).

**[HALLAZGO] Dos regímenes de universo conviven en el árbol y ningún código único
reproduce los dos oros bajo uno solo.** El piloto 1 (y esta spec, heredando la PROPUESTA
§1) filtra globalmente: 13 492 personas en 2024. El árbitro que selló los marginales
(`tools/medidor_ahorro_enif24.py::carga()`, `#971`, C2-IC) no filtra por TLOC ni saca
los centinelas del universo: 13 502 personas, y cada eje marca «fuera» **por eje** (edad
97/98, escolaridad 99, formalidad blanco/9). El medidor lleva el régimen como parámetro
congelado por CALC (`universo_regimen.tipo ∈ {PILOTO-1, ARBITRO-2024}`); **el lote usa
`PILOTO-1`** y sólo el oro (ii) usa `ARBITRO-2024`, para reproducir el C2-IC réplica a
réplica. Consecuencia declarada: los puntos de C2 (sellados bajo `ARBITRO-2024`) y sus
réplicas (bajo `PILOTO-1`) mezclan regímenes **exactamente como el piloto 1 lo hizo**;
la diferencia entre marginales re-derivados y sellados se emite (`…-M24-*-DELTA-SELLADO`;
en el piloto 1 el peor es 1.2e-3). Pregunta Q2 de §16.

**Los seis ejes y sus cortes** se leen del árbitro (`milpa/tramite-ola5-propuesta-v0.yaml`,
regla `dinero.ahorro.via_informal_ejes_enif2024`, líneas 1415 ss.) y viajan en
`spec.yaml` (`parametros.ejes.<eje>.orden`), en este orden de categorías:

| eje | 2021 | 2024 | categorías (orden del árbitro) |
|---|---|---|---|
| `sexo` | `SEXO` | `SEXO` | `1 Hombre` · `2 Mujer` |
| `edad` | `EDAD` | `EDAD_V` | `18-29` · `30-44` · `45-59` · `60+` (= 60–97) |
| `escolaridad` | `P3_1_1` | `NIV` | `hasta primaria` · `secundaria` · `media superior` · `superior` |
| `localidad` | `TLOC` | `TLOC` | `menor de 15 000` ({3,4}) · `15 000 y mas` ({1,2}) |
| `formalidad` | `P3_10` (1–5 con, 6 sin) | `P3_13` (1–6 con, 7 sin) | `sin seguridad social` · `con seguridad social` |
| `cuenta_formal` | `P5_4_1..9` | `P5_4_1..9` | `sin cuenta` · `con cuenta` (las nueve en blanco → fuera) |

Los nemónicos y textos de pregunta de cada ola están, fila por fila, en
`data/ahorro-comparabilidad-texto-v1_0.tsv` (`#967`).

## 2 · Escolaridad por ETIQUETA — [CIERRA]

El catálogo de `NIV`/`P3_1_1` **no es el mismo en 2021 y 2024** (04/05 permutados; 09–11
nuevos). `spec.yaml` transporta **dos catálogos (código → etiqueta)** —2021 leído de
`catalogos/p3_1_1.csv` dentro del payload `enif2021_csv`; 2024 leído del FD
`enif_2024_fd.xlsx` (sha256 `17e2ad86…`, hoja `TMODULO`, filas 30–42)— y **un solo mapa
(etiqueta → tramo)**. En 2021 el medidor **verifica el catálogo del zip contra el
declarado** y lo emite (`…-W2021-CATALOGO-ESCOLARIDAD = COINCIDE`). Un código presente
en el dato **sin etiqueta declarada PARA la corrida** (`Paro`), no se asigna por cercanía.
`No sabe` (99) va a «fuera» del eje. El colapso absorbe la permutación: `Normal básica` y
`Estudios técnicos con secundaria terminada` son ambos `media superior`; `Especialidad`,
`Maestría`, `Doctorado` y `Maestría o doctorado` son `superior`.

## 3 · Los 14 pares, clasificados — y qué piso tiene cada grupo

Nombres y orden `(a, b)` **como el marcador** (`CRUCE-GRUPO::<regla>::<par>`):

- **Primarios (5, 44 celdas):** `edadxsexo` (8) · `escolaridadxsexo` (8) · `localidadxsexo` (4)
  · `edadxescolaridad` (16) · `escolaridadxlocalidad` (8). C2 **EMITIBLE** (dictamen
  sellado `data/corrida0/c2-compuesto-dictamen-v1_0.tsv`).
- **Formalidad (4, 24 celdas), secundarios rotulados:** `formalidadxsexo` (4) ·
  `edadxformalidad` (8) · `escolaridadxformalidad` (8) · `formalidadxlocalidad` (4).
- **`cuenta_formal` (5, 28 celdas), se adjudican aparte:** `cuenta_formalxsexo` (4) ·
  `cuenta_formalxedad` (8) · `cuenta_formalxescolaridad` (8) · `cuenta_formalxlocalidad` (4)
  · `cuenta_formalxformalidad` (4). C2 EMITIBLE en los cuatro primeros; el quinto lleva
  `formalidad`.

**[HALLAZGO] El C2 sellado cubre 9 de los 14 pares (68 celdas), no 14.** Los cinco pares
que contienen `formalidad` son `NO-EMITIBLE` en el dictamen sellado (A-bis 4:
`universo_restringido: true`, cobertura 0.6897). El «C2 restringido al universo de quien
trabaja» que nombra F2 **no existe sellado**, y derivarlo exige leer 2024 por `trabaja ×
eje` para los otros cuatro ejes — una lectura de dos variables que este acto tiene vedada
(PARO a) y que ningún sello provee. **[CIERRA]** En este COMMIT-1 esos cinco pares se
congelan con `C2 = NO-EMITIBLE` (texto del dictamen en `…-<PAR>-C2-ESTADO`) y **sin piso**:
emiten sólo `P2` (persistencia), y `R1`/`R2`/`R3` quedan `null` **declarados**; en
adjudicación reciben R, soporte y cobertura de `P2`, y su veredicto es
`NO-ADJUDICABLE-SIN-PISO`. Pregunta Q1 de §16, con la opción de sellar los 13 marginales
restringidos en un acto sucesor antes del COMMIT-2.

## 4 · Contendientes — lista cerrada, fórmula cerrada, y de dónde sale cada número

`m̂24(a)`, `m̂24(b)`, `m̂24` son los marginales ponderados de ENIF 2024 **sellados en
`CALC-ARBITRO-MARGINALES-ENIF2024-0001` (`#971`)**, citados por id de RESULT en
`spec.yaml` (`parametros.marginales_sellados`) con su masa ponderada (`…-DEN-W`); **no se
re-miden**: el medidor re-deriva los marginales de un eje sólo para las **réplicas** y
emite la diferencia contra el sellado. El subíndice `21` marca ENIF 2021, ola de
desarrollo, abierta entera. Toda combinación de niveles es en **logit** y **réplica k con
réplica k** (muestras independientes entre olas; sin covarianzas inventadas).

| # | contendiente | clase | fórmula cerrada | punto | réplicas |
|---|---|---|---|---|---|
| `C2` | composición de marginales de la misma ola | **piso** | `expit(logit m̂24(a) + logit m̂24(b) − logit m̂24)` — «ausencia de interacción en escala logit» | sellados `#971` | re-derivadas |
| `P2` | persistencia | piso | `p̂21(a,b)` | 2021 | 2021 |
| `R1` | interacción histórica cruda | secundario | `expit(logit C2 + δ21(a,b))`, `δ21 = logit p̂21(a,b) − [logit m̂21(a) + logit m̂21(b) − logit m̂21]` | mixto | mixto |
| `R2` | interacción encogida, **λ = ½ fija** | **retador primario** | `expit(logit C2 + ½·δ21(a,b))` | mixto | mixto |
| `R3` | ajuste proporcional iterativo | secundario | raking, §4.1 | mixto | mixto |
| `L1` | LLM solo | secundario | mediana de k = 8, paquete §8 | mesa | — |
| `L2` | LLM con marginales | secundario | ídem | mesa | — |
| `M` | emisor del motor | `NO-DERIVABLE` | — (F2; texto en `…-G-M-ESTADO`) | — | — |

**`R2` con λ = ½ en los catorce pares, sin miembro `Sλ`** (opción A). `cruces_familia.py`
trae la encogida por momentos para el duelo; aquí **se importa `desplazada(c2, Ī, ½)`**, no
se estima λ. `Ī` es la interacción de la única ola comparable (2021).

**4.1 · `R3` — [CIERRA] el algoritmo que la PROPUESTA dejó en «criterio de paro y tope en
`spec.yaml`».** Una tabla de proporciones no tiene marginales sin una composición; la
forma bien definida es el **raking a tres vías**: la tabla ponderada 2021 `T(a,b,d)`
(`d ∈ {0,1}`, masa `W21(a,b)` y numerador `Y21(a,b)`) se escala iterativamente para casar
los márgenes `(a,d)` y `(b,d)` de 2024 —cada uno es **un marginal de un eje** sellado,
`masa(a) × [1−m̂24(a), m̂24(a)]`— normalizados a participaciones para que las dos
direcciones sean compatibles aunque sus universos válidos difieran por «fuera».
`R3(a,b) = T*(a,b,1) / T*(a,b,·)`. Conserva las razones de momios de 2021 y casa los
márgenes de 2024. Paro: cambio máximo `≤ 1e-12`; tope 2000 iteraciones; una réplica que no
converge queda `NaN` y se cuenta (`…-R3-REPS-NO-CONVERGEN`); celda con masa cero en 2021
→ `null`. Implementado en `tools/lote_enif2024/lote_familia.py::ipf_3vias`, con tests.

**Multiplicidad, dicha antes:** la comparación que adjudica es **una sola** (`C2` contra
`R2`, §7). Todo lo demás es secundario y se rotula (`…-ROL = SECUNDARIA`).

## 5 · Por qué λ = ½ y no estimada — heredado de la PROPUESTA §5

Sólo 2021 es comparable por texto (`#967`: 2012 ventanas distintas, 2015 nómina y pensión
colapsadas, 2018 `D8` con universo 18–70). Con una sola ola anterior no hay estabilidad
entre olas que estimar; F2 lo previó y dirección lo cerró (opción A). La persona elegida
es 18–70 en 2018 y 18+ desde 2021: irrelevante con λ = ½, y **queda escrito** para que
nadie lo redescubra.

## 6 · Rejilla y regla de soporte

La rejilla **se lee del árbitro** (§1) y el medidor la toma de `spec.yaml`; una categoría
que el árbitro no declare no existe; una categoría declarada **sin filas** en una ola se
emite con `n = 0` y `null` en `P` (rama probada, §12). **Soporte** por celda:
`n ≥ umbral_soporte_n` en **las dos olas** (2021 y 2024), con `umbral_soporte_n = 200`
en `spec.yaml` (el del piloto 1); declarado antes de abrir. Una celda sin soporte **no
puntúa** y se reporta con su `n`. `n` es `DESCONOCIDO` hasta que la corrida lo calcule:
esta spec no afirma que ninguna celda esté bajo el umbral. El soporte de 2021 se emite en
COMMIT-2 (`…-N21-*`, `…-SOPORTE-2021-*`); el de 2024 en COMMIT-3.

## 7 · Regla de victoria (enmienda v0.3), remuestreo y salidas

**Estadística primaria, una sola:** `Δ = MAE(C2) − MAE(R2)` en pp, sobre las celdas
**puntuadas** de los **5 pares primarios, agregadas (44 celdas nominales, un solo Δ)**,
contra el árbitro `R` de cada cruce. **IC95 por réplica**: un único plan de réplicas por
ola —`n_h` UPM con reemplazo dentro de cada estrato, `PCG64(42)`, 10 000 réplicas, estratos
y UPM en orden lexicográfico—, de modo que `Δ_k` se recalcula réplica a réplica con `R_k`,
`C2_k` y `R2_k` de la misma `k`. Calcular dos IC y restarlos está prohibido.

| IC95 de `Δ` | veredicto (`…-G-PRIMARIO-VEREDICTO-PRIMARIO`) |
|---|---|
| inferior `> 0.5` pp | `VENCE-RETADOR` |
| inferior `> 0` y `≤ 0.5` | `PROPUESTA-CON-RESERVA` |
| incluye 0 | `NADIE-VENCE` (con el signo del superior: el piso se sostiene si `< 0`) |

La misma regla se aplica, **rotulada `SECUNDARIA`**, a `P2`, `R1`, `R3` y a cada par por
separado, y al bloque `cuenta_formal` agregado; el bloque `formalidad` no tiene piso y
sólo reporta cobertura de `P2`. **El conteo de ¾ es descriptivo** (`…-TRES-CUARTOS-*`) y
no adjudica. Implementación: `cruces_familia.adjudica()` (`#968`), importada.

**Simulación de potencia — corrida en este COMMIT-1, antes de abrir nada** (§11, iii).
No cambia la regla (PARO c del encargo).

## 8 · Los dos emisores `L`

`L1` y `L2` los corre **mesa**, por CLI y sin API (FP-228), con
`forense/prereg-duelo-v2/PAQUETE-L-LOTE-ENIF2024-v1_0.md` y el `prompts.jsonl` que
`tools/lote_enif2024/genera_paquete_l.py` deriva de `spec.yaml` (rejilla) y de los
marginales sellados (`#971`): **ningún prompt se redacta a mano**. `k = 8`, mediana,
modelo/versión/temperatura fijados al correr con cita del corte de entrenamiento; capturas
selladas **antes** del COMMIT-2 mecánico. Agregador: el de `#973`
(`tools/agrega_l_v1_0.py`) cuando esté en `main` — hoy no lo está (§16, Q3).

## 9 · Cobertura — por celda y por par, con su apellido

Se reporta la cobertura del IC95 de `C2`, de `P2` **y de `R2`** (propuesta de dirección:
en el piloto 3 el retador encogido cubrió 14/15 contra 8/15 del piso): por celda
(`…-DENTRO-IC-R-*`, `…-R-DENTRO-IC-CAND-*`), por par (`…-COBERTURA-R-EN-IC-CAND-FRAC`,
5 conglomerados primarios; 14 contando secundarios) y por bloque agregado. **Las celdas no
son independientes** (una sola muestra; `edadxsexo` y `edadxescolaridad` comparten
personas): ninguna frase de producto dice «cobertura del 9X %» sin el apellido «dentro de
ENIF 2024».

## 10 · B-bis — pre-registro de falsación, antes de ver el dato

| salida | condición (lectura mecánica `…-G-BBIS-FILA`; la lee mesa) |
|---|---|
| **FALSADOR DÉBIL** | ≥ ⅓ de las celdas de los 5 pares primarios **sin soporte** — **manda** si cabe con otra |
| **CORROBORADA** | nadie vence (primaria) **y** cobertura de `C2` por par ≥ 80 % en cada par primario |
| **ACOTADA** | vence alguien sólo en pares que comparten **un** eje — se nombra el eje |

Refuta el argumento de producto: cobertura de `C2` por par < 80 % → «sé cuánto me equivoco»
queda acotado a los cruces vistos. Si ninguna fila cae, se escribe `NO-CAE-EN-NINGUNA-FILA`
con la razón.

## 11 · Los dos oros y la potencia — declarados antes de correrlos (E.5)

1. **Oro del piloto 1** (`localidad × edad`, ya abierto): el código genérico, con el régimen
   `PILOTO-1` y **los insumos del piloto** (sus marginales sellados a 6 decimales, citados
   desde su `spec.yaml` sellado), reproduce `C1 = P2` (P, IC, n), `C2` (P, IC) y la `R`
   (P, IC, n) selladas **a 1e-9**, por `corrida0 run`, en dos CALC `RETROSPECTIVA`
   (`CALC-DIN-LOTE-ORO-PILOTO1-EMISIONES-0001` → `…-ADJUDICACION-0001`) que además prueban
   la guardia sobre un par vetado. Si no reproduce, el código no es el mismo procedimiento
   y el lote no se lanza.
2. **Oro del `C2` sellado** (`CALC-C2-COMPUESTO-IC-ENIF2024-0001`): sobre los 9 pares
   EMITIBLE (68 celdas), bajo `ARBITRO-2024`, el `C2` del lote reproduce **el IC réplica a
   réplica a 1e-10**; el **punto** reproduce a `1e-5` **por una causa declarada**: el
   C2-IC tomó los puntos del yaml del árbitro (6 decimales) y el lote los toma de `#971` a
   precisión completa (el mismo número antes de redondear). `CALC-DIN-LOTE-ORO-C2IC-0001`,
   sólo `C2`: no es un COMMIT-2 con otro nombre.
3. **Potencia de la regla v0.3** (`tools/lote_enif2024/potencia_v0_3.py`, salida en
   `forense/analisis/gen2-din-lote-enif2024-commit-1/`): sobre las 35 celdas ya abiertas
   de los pilotos 1–3 (sus `R`, `EE` y errores por celda sellados), con el efecto del piloto
   3 (ΔMAE 1.47 pp, distribución por celda de `C2 − S½`) y remuestreo hacia 44 y 68
   celdas: ¿con qué probabilidad el IC95 de `Δ` despeja 0.5 pp? Se reporta la curva por
   tamaño de efecto y número de celdas. **No cambia la regla.**

Los oros son **condición de congelado** (P5 del encargo); los dry-runs previos al sello,
sobre datos ya abiertos, son ensayo del conducto y se declaran aquí.

## 12 · «Congelado» — D-22 ampliada, cumplida con salida cruda

1. `corrida0 preflight` **VERDE** sobre el commit final con `origin/main` fusionado, en
   `EMISIONES`; `ADJUDICACION` bloqueado **sólo** por `emisiones_selladas`/`emisiones_sello`
   aún inexistentes (`secuencia_commits.preflight_esperado_antes_del_commit_3a`).
2. El punto de entrada **ha corrido** sobre sintético (`tests/test_lote_enif2024.py`,
   zips fabricados por `tools/lote_enif2024/sintetico.py`) y sobre oro (§11).
3. `_valida_outputs` acepta la salida de **cada rama terminal**: todas con soporte ·
   soporte parcial · fuera de soporte global (cero puntuadas → `NO-ADJUDICABLE`, B-bis
   `FALSADOR-DEBIL`) · celda rara vaciada en una ola · marginal con masa cero en la ola
   nueva · ola nueva chica · emisiones alteradas → PARO antes de abrir R.
4. **Todo id que el código puede emitir nulo está declarado** (`permite_no_estimable`)
   por lectura estática del catálogo que el propio medidor deriva
   (`catalogo_resultados()`): `P`/`IC95INF`/`IC95SUP` de cada contendiente y celda, `IBAR`,
   `P-REDERIVADO`/`MASA`/`DELTA` de marginales, `ERROR-PP`, `MAE`/`DELTA-MAE`/`DELTA-IC`,
   `EE`, fracciones de cobertura y ¾, `DELTA` de controles. `corrida0 ensayo` no existe
   aún (F4, TUBERÍA): el ensayo va como test, como en el piloto 3 v1.3.
5. **Ningún input con hash sobre un archivo vivo**: los inputs `origen: repo` son
   `resultados.json`/`spec.yaml` de CALC sellados y dos módulos de código versionado
   (`cruces_familia.py`, `lote_familia.py`), cuyo sha se emite además como RESULT.

## 13 · Secuencia de commits y quién

**COMMIT-1 (este acto): congela.** `COMMIT-2` (otra sesión, F3): `corrida0 run
…-EMISIONES-0001`, sella, registra (E.7), empuja; **antes**, mesa sella las capturas `L`.
`COMMIT-3a` (misma sesión del 2, commit aparte): escribe los sha de `emisiones_selladas`
y `emisiones_sello` en `…-ADJUDICACION-0001/spec.yaml` y verifica `preflight` VERDE;
ninguna otra línea cambia. `COMMIT-3`: `corrida0 run …-ADJUDICACION-0001`: reproduce las
emisiones a 1e-10 (si no, PARA sin abrir R), abre los 14 cruces **por la única función
`cruce()`** y sólo los pares autorizados por el contrato, R por celda, soporte, regla
v0.3, cobertura, lectura B-bis; sella, registra.

## 14 · Guardia de reserva — código, no prosa (E.6)

En `tools/lote_enif2024/enif_lote.py`: el microdato sólo es alcanzable dentro del núcleo;
`marginal(ola, eje)` agrupa por **un** `str` atómico; `cruce()` es la única llave de dos
ejes y lanza `ReservaRota` sobre la ola reservada o un par no autorizado
(`pares_cruce_autorizados_2024`: `[]` en emisiones, `[localidad×edad]` en el oro, los 14
en COMMIT-3); la ola se re-huella antes de contar; una auditoría del AST del propio
archivo corre al arrancar `medir()` (R1–R7) y **cada regla tiene control positivo por
mutación** en el test. En cada corrida la guardia **se prueba** y su excepción se emite
(`…-G-RESERVA-GUARDIA-PROBADA`, `…-G-VETO-PROBADO`).

## 15 · Lo que NO significa · auditoría · lo que no hace

Hereda §13–§15 de la PROPUESTA sin cambio: que el piso gane no dice que la conducta sea
estable por cultura; ahorrar sólo por vías informales responde a **acceso, ingreso y
oferta antes que a preferencia**; `cuenta_formal` es estructura de acceso y `formalidad`
una posición en el mercado de trabajo, no un rasgo de la persona; el universo
sub-representa a quien no decide el dinero del hogar; ninguna cifra es «los mexicanos» sin
segmentar; nada se compara contra ENCIG ni contra el duelo nacional. Módulo de auditoría:
toda la evidencia es clase (a); `localidad` y `formalidad` existen para ver el sesgo de
clase y se reportan por eje; no se mide desconfianza; contadores que mueve este acto: los
tres oros sellados (`cuenta_gen2 = SI`, RETROSPECTIVA, no adjudican), `adoptados_activos`
no se mueve. No abre los cruces · no corre LLM · no adjudica · no toca `milpa/` ni el
marcador · no reabre el veredicto del piloto 3 (**FALSADOR DÉBIL**) · no gasta ninguna
reserva apartada.

## 16 · Preguntas a mesa — con opciones y recomendación (D-19)

- **Q1 · C2 de los 5 pares con `formalidad`.** (A, congelado aquí y **recomendado** para
  este COMMIT-1) `NO-EMITIBLE`, sin piso, sólo `P2`; consistente con el dictamen sellado y
  con PARO a. (B) Un acto sucesor sella, bajo el árbitro, los 13 marginales restringidos
  al universo `trabaja` (`sexo|T`, `edad|T`, `escolaridad|T`, `localidad|T` y nacional|T;
  cada uno una lectura de **un** eje derivado) **antes del COMMIT-2**, y una enmienda con
  archivo propio añade `C2-restringido` a esos pares. (C) Dejarlos fuera del lote.
- **Q2 · Régimen de universo.** (A, congelado, **recomendado**) `PILOTO-1` para el lote,
  como la PROPUESTA §1; la mezcla punto-sellado/réplicas-propias se emite y se cita.
  (B) `ARBITRO-2024` para el lote, coherente con `#971` y el C2-IC pero distinto del
  piloto 1 y de la PROPUESTA — toca el universo, no es del ejecutor.
- **Q3 · Agregador de L.** `#973` (`tools/agrega_l_v1_0.py`) **no está en `main`**; el
  paquete lo cita como el agregador a usar cuando se fusione (procedencia tipo 3, no se
  importa). Si `#973` no fusiona antes del sello de capturas, mesa decide agregador.
