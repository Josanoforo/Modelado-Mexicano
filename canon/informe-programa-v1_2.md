# Informe del programa · v1.2

**Modelado Mexicano — «Psicología del Mexicano Contemporáneo».**
Documento del programa, escrito para mesa y para un comprador escéptico.
22 de septiembre de 2026.

### `informe-programa` · **v1.2** · DOCUMENTO DEL PROGRAMA

> | | |
> |---|---|
> | **ARCHIVO** | `informe-programa-v1_2.md` |
> | **REEMPLAZA A** | `informe-programa-v1_1.md` (21/sep/2026), que **no se edita** — E.3: una pieza sellada es evidencia histórica. La v1.1 es anterior al lote ENIF 2024, al árbitro 1/2 de marginales, al backtest de crédito, al dictamen ENCIG y a la validación independiente de los pilotos, y queda **VENCIDA EN ALCANCE** (A.10): su universo creció, no fue refutada. |
> | **VERIFICAS ASÍ** | cada cifra de este documento trae, en su propia línea o al pie de su tabla, el `RESULT` sellado o el comando que la reproduce. Las cifras del lote ENIF 2024 salen de `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001/resultados.json` (PR #986); las de marginales de `CALC-ARBITRO-PERSISTENCIA-ERROR-0001` (PR #971/#989); las de crédito de `CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001` (PR #987); ENCIG de `CALC-ENCIG-ORIGEN-MOVIL-0001` (PR #972); el marcador de `tools/marcador_segmento.py`. |
> | **NOMBRE ESTABLE** | **`informe-programa`** — cítalo así, **nunca por nombre de archivo** |

> **Estampa de universo (A.10), global.** Derivado contra `origin/main =
> bda6b60c` (merge de `PR #989`, 21/sep/2026 tarde; incluye `#986`, `#987`,
> `#988`, `#976`, `#972`, `#970`, `#971`, `#969` como ancestros). Acto de
> **NUBE sin corpus montado** (`tools/entorno.py`: `raices=data_raw:NO`,
> `corpus=NO(examinados=0)`, red no ejecutada). **Fuentes: sólo el registro
> derivado y las corridas selladas que ya viven en el repo.** Este documento
> no abre microdato, no llama a ningún modelo, no sella ninguna corrida y
> **no adjudica nada**.
>
> **Lo que este documento NO es.** No es SALIDA para cliente: es su insumo.
> No re-abre ningún veredicto. No adopta ningún candidato. El veredicto del
> lote ENIF 2024 sigue siendo `PROPUESTA-CON-RESERVA` para `R2`; el del
> piloto 3 sigue `FALSADOR-DEBIL` con `champion_actual: NINGUNO`; nada de lo
> que se lee abajo los mueve.

---

## 0 · En una página

**La pregunta que este informe contesta sigue siendo una sola: ¿el motor sabe
predecir una celda que no ha visto, y sabe cuánto se equivoca?** Con el lote
ENIF 2024 adentro, la respuesta se afina:

- **Sí, en cruces, cuatro veces, con 79 celdas puntuadas** (35 de los tres
  pilotos + 44 del lote ENIF 2024). El piso `C2` erró entre 1.47 y 3.41 pp en
  los pilotos, y 1.87 pp en el lote (§2).
- **El lote es la primera prueba grande (14 cruces, 96 celdas) contra un
  retador con interacción, y el retador no venció limpio: `PROPUESTA-CON-
  RESERVA`.** `R2` (interacción histórica 2021↔2024 encogida) bajó el error a
  1.39 pp (ΔMAE 0.48 pp, IC95 [0.10, 0.72]) pero el IC no despeja el umbral de
  0.5 pp (§3).
- **El piso mismo subcubre en el lote: 75.0% en vez del ≥80% que el B-bis
  exigía.** Por eso el B-bis `NO-CAE-EN-NINGUNA-FILA` y mesa lo lee en §4: el
  argumento «sé cuánto me equivoco» queda acotado a los cruces vistos.
- **En marginales (persistencia t−1), la cobertura es 14/57 = 25%** —
  bastante más débil que en cruces — y varía muchísimo por encuesta: ENIF
  6/32, ENVIPE 8/15, ENCIG 0/10 (§2.4).
- **Crédito: persistencia gana el backtest 2021→2024 en 7 de 9 marginales**
  (PR #987) — el primer resultado donde el piso simple gana claramente, sin
  retador de por medio.
- **ENCIG (pago de luz por canal digital) tiene un salto de nivel de 2019 a
  2025 que ningún candidato explica: dictamen `SALTO-SIN-EXPLICAR`** (§3.4).
- **No sabe cuánto se equivoca fuera de cruces**, por decisión de mesa del
  21/sep, y este informe sigue sin prometerlo.
- **Regla de salida de θ: dos de tres pruebas ya corrieron y ninguna dio
  victoria a un retador con interacción** (piloto 3: `FALSADOR-DEBIL`; lote
  ENIF 2024 `R2`: `PROPUESTA-CON-RESERVA`, cuenta como «no venció», segunda
  prueba de tres). Falta el duelo ENVIPE 2026 (§5).

**Contadores que movió el trabajo que produjo este informe** (v2.16 del
módulo de auditoría): **cero** de los contadores rectores del programa
(`celdas_validadas` sigue en **92**, `marcador_segmento.total_filas` sigue en
**230**, `sin_piso` sigue en **15** — todo re-derivado por comando, `python3
tools/tablero_programa.py` / `python3 tools/marcador_segmento.py`). Lo que sí
se movió: la **sub-razón** de 15 filas `SIN-PISO` del marcador (11 ENUT + 4
EDER), que pasó de `NO-CONSTRUIBLE`/`SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD` a
`SIN-PISO-POR-DISEÑO:<causa>` por F-ENUT/F-EDER (§1.2), y dos filas de
`forense/no-corrido.tsv` (`NC-0377`, `NC-0411`) que cerraron.

---

## 1 · El marcador, con el lote adentro

### 1.1 · Dos columnas que nunca se mezclan (heredado de v1.1, sin cambio)

`prospectividad`: **20 PROSPECTIVA · 59 RETROSPECTIVA · 89 IDENTICO-EMISOR-
ES-ARBITRO · resto SIN-EMISION/EMITIDA-SIN-R**, sobre las 214 filas que ya
traía v1.1 (`tools/marcador_segmento.py`, bloque `resumen.prospectividad`).
Las 44 celdas puntuadas del lote ENIF 2024 y las celdas de marginales nuevas
que entraron con `#971`/`#989` **no viven en `marcador-segmento.tsv`**: el
lote vive en su propio CALC (`CALC-DIN-LOTE-ENIF2024-*`), reservado, y sus 14
pares — 9 `ADJUDICADO`, 5 `SIN-PISO-SOLO-P2` — no pasan por el derivador de
marginales `_ejes_`. Esa es la razón, verificada por objeto: `tools/
marcador_segmento.py` sólo lee `milpa/tramite-ola5-propuesta-v0.yaml` (reglas
`_ejes_`) y las tres fuentes de §5; el lote es su propio universo, congelado
aparte (E.6), y el informe lo reporta en §3, no en el marcador.

### 1.2 · `SIN-PISO-POR-DISEÑO`, rotulado por comando (F-ENUT + F-EDER)

Antes de este acto, 15 de las 230 filas del marcador salían `SIN-PISO` sin
distinguir «nadie midió el piso» de «el diseño de la ola no admite un piso
t−1». `SIN-PISO-POR-DISEÑO` entra ahora al vocabulario `status` de las tablas
de identidad (firma F7 del trámite 5, `FP-260921-GEN2-TRAMITE-FIRMAS-5-958c-
02`) y se transporta al marcador por el mismo mecanismo de siempre —
`tools/marcador_segmento.py::_piso_de_fila` ahora expone el `status` literal
de la fila en vez de forzar el prefijo `NO-CONSTRUIBLE:` para cualquier
status ≠ `CONSTRUIBLE` — sin escribir ningún rótulo a mano:

| grupo | n | tabla que lo sella | razón |
|---|---:|---|---|
| ENUT 2024, `familia.cuidado.reparto_mujeres40_ejes_enut2024` | 11 | `forense/prereg-caja/PISOS-ENUT2019-ejes-metadatos-v1_1.tsv` (SUCEDE a `v1_0`, A.10) | C1 `CAMBIO-DE-INSTRUMENTO` sellada en `#976`: ENUT 2024 (`*_CON_CP`) no es comparable por texto con 2019 |
| EDER 2017, `familia.union.libre_ejes_eder2017` | 4 | `forense/prereg-caja/PISOS-EDER2017-cohorte-metadatos-v1_0.tsv` (nueva) | dictamen §2.2 (`forense/notas/2026-09-19-GEN2-PISOS-ENUT2019-EJES-1-dictamen.md`): EDER no es serie anual, el eje es cohorte re-observada, no ola anterior |

`sin_piso` **sigue en 15** — las 15 filas ya eran `SIN-PISO` antes; sólo
cambió la causa que `piso_fuente` reporta. La tabla `v1_0` de ENUT 2019
**no se edita ni se borra**: queda sellada, `VENCIDA EN ALCANCE` para esta
lectura (A.10), y `sucesiones_identidad()` la nombra `SUCEDE-A` en el
`piso_fuente` de cada una de las 11 filas.

**Lo que sigue sin piso, mismo estado que v1.1.** El cruce
`reparto_hogar × sexo_edad` de ENUT sigue `RESERVADA` (no lo toca esta
firma). Las **celdas hermanas** sobre el núcleo común (`ENUT-NUCLEO-ejes-
spec-v1_0.md`, C2 `CAMBIO-MENOR`) con piso 2019 y R 2024 — el objeto que P2
pedía registrar «por RESULT» — **no tienen CALC sellado en este universo**:
`data/corrida0/` no trae ningún `CALC-ENUT2019-NUCLEO-EJES-*` ni `CALC-ENUT-
NUCLEO-*` con `resultados.json`; `NC-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-
01` (ABIERTA, PR #976) ya declaraba esto: el núcleo común quedó como
**diseño** (opción A de mesa), no como corrida sellada, con sucesor «en CAJA
que re-derive el R de las 21 celdas sobre el núcleo». No hay RESULT que citar
sin fabricarlo — se declara en `## NO-CORRIDO / RESERVAS`, no se inventa.

---

## 2 · Cobertura por candidato — pilotos, lote y marginales, con IC binomial

**Intervalo binomial: Wilson (score), z = 1.959964** — heredado de v1.1, sin
`scipy` en este entorno de nube.

> **ADVERTENCIA QUE VIAJA CON TODO INTERVALO DE ABAJO (heredada de v1.1).**
> Las celdas de una misma ola comparten marco muestral, estratos, UPM y
> réplicas de bootstrap. **No son ensayos independientes.** Todos estos
> intervalos son demasiado angostos.

### 2.1 · Los tres pilotos (§2 de v1.1, sin cambio — se cita, no se re-mide)

| piso C2 | cobertura | Wilson 95% |
|---|---:|---|
| piloto 1 · ENIF 2024, persona | 7/8 | [0.529, 0.978] |
| piloto 2 · ENVIPE 2025, delito | 11/12 | [0.646, 0.985] |
| piloto 3 · ENCIG 2025, trámite | 8/15 | [0.301, 0.752] |
| **los tres** | **26/35 = 0.743** | **[0.579, 0.858]** |

### 2.2 · Lote ENIF 2024 (14 cruces, 44 celdas puntuadas de 96 — PROSPECTIVA)

Fuente: `forense/notas/2026-09-21-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-cierre.md`
(PR #986). Universo primario: **5 pares EMITIBLE, 44 celdas puntuadas de una
sin soporte**; 5 pares más (24 celdas) quedan `SIN-PISO-SOLO-P2` por
restricción de universo (`formalidad`, 68.97%, A-bis 4) — no adjudicables
aquí.

| candidato | MAE (pp) | cobertura (R dentro del IC del candidato) |
|---|---:|---:|
| `C2` · piso (marginales sin interacción) | 1.8729 | **75.0%** |
| **`R2` · interacción histórica encogida (λ=1/2)** | **1.3931** | **88.6%** |
| `R1` | — (`ΔMAE` vs `C2` = 0.57 pp, `NADIE-VENCE`) | — |
| `R3` (raking IPF) | — (`ΔMAE` vs `C2` = 0.61 pp, `NADIE-VENCE`) | — |
| `P2` (piso 2024 sin interacción, descriptivo) | 2.34 | — |

*Cobertura tal como el CALC sellado la reporta, en el mismo orden que §1 de
v1.1 («R dentro del IC del candidato»): `C2` = 75.0%, `R2` = 88.6%. La nota
de cierre trae además la lectura inversa (candidato dentro del IC de R:
`C2` 84.1%, `R2` 97.7%), que **no** es cobertura en el sentido de este
informe y no se usa aquí (§2 de v1.1: son dos preguntas distintas).*

**Comparación primaria: `ΔMAE(C2−R2) = 0.4798 pp, IC95 [0.0975, 0.7151]`.**
Despeja 0 pero **no** despeja el umbral de 0.5 pp declarado antes de abrir el
dato ⇒ **`VEREDICTO-PRIMARIO = PROPUESTA-CON-RESERVA`** (no `VENCE-RETADOR`).
Secundarias sobre las mismas 44: `P2` `ΔMAE=−0.42 pp` `NADIE-VENCE`; `R1`
`ΔMAE=0.57 pp` `NADIE-VENCE`; `R3` (raking IPF) `ΔMAE=0.61 pp` `NADIE-VENCE`.
Ninguna secundaria vence.

**B-bis (falsación pre-registrada, §10 de la spec): `NO-CAE-EN-NINGUNA-FILA`**
— razón mecánica: cobertura de `C2` < 80% en un par primario refuta el
argumento de producto. `ADJUDICA-SOLO = NO`. **Lectura de mesa (F-LOTE, este
acto):** el piso `C2` sigue adjudicado (A-bis 6: nadie venció); su intervalo
**subcubre** (75.0% < 80%) y así se dice; `R2` cubre 88.6% y yerra menos, pero
es **retador no adjudicado** — ninguna frase de producto cita 88.6% sin esa
etiqueta. El argumento «sé cuánto me equivoco» queda **acotado a los cruces
ya vistos** (lote y pilotos), no como propiedad general del método.

### 2.3 · Crédito 2021→2024, backtest de persistencia (PR #987)

`CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001`. Título del PR (verbatim,
única cita disponible sin abrir microdato en este entorno de nube): **la
persistencia gana el backtest en 7 de 9 marginales**. Es un backtest, no una
prueba prospectiva sobre 2024 real (la nota de cierre citada en el encargo
—`nota-2026-09-21-gen2-din-credito-prediccion-2024-commit-1.md`— es de la
pieza COMMIT-1, sin las cifras de 2024): **no se cita el detalle por celda ni
el ΔMAE con IC aquí** porque no está en el archivo alcanzable en NUBE sin
abrir el CALC de COMMIT-2/3; se declara el hallazgo agregado (7/9) por el
propio título del merge y se marca la falta de detalle en
`## NO-CORRIDO / RESERVAS`.

### 2.4 · Marginales, persistencia t−1 (PR #971/#989) — **14/57 = 25%**

`forense/notas/2026-09-21-GEN2-ARBITRO-MARGINALES-1-cierre.md` §2. Cobertura
= punto R dentro del IC95 del piso.

| encuesta (brecha, unidad) | N | cobertura (Wilson 95%) |
|---|---:|---|
| ENIF 2024 (3 años, persona) | 32 | **6/32 = 0.19** [0.09, 0.35] |
| ENVIPE 2025 (1 año, delito) | 15 | **8/15 = 0.53** [0.30, 0.75] |
| ENCIG 2025 (2 años, trámite) | 10 | **0/10 = 0.00** [0.00, 0.28] |
| **los tres** | **57** | **14/57 = 0.246** |

*Escala: proporción de celdas, no se promedia con la cobertura de §2.1/§2.2
(universos y candidatos distintos: aquí es persistencia t−1 vs marginal, no
`C2`/`R2` de cruce). ENCIG en 0/10 es el mismo hallazgo que §3.4 explica
desde el origen: la persistencia falla porque el nivel saltó, no porque el
orden entre categorías se perdiera (el gradiente por escolaridad persiste).*

---

## 3 · Qué enseñaron el lote, ENCIG y crédito

**(a) El piso simple aguanta más de lo que el piloto 3 solo sugería.** En el
lote, `C2` (1.87 pp) sigue siendo el punto de referencia contra el que se mide
todo; ninguna secundaria (`P2`, `R1`, `R3`) lo vence. En crédito, la
persistencia **gana** 7 de 9 sin que un retador entre siquiera a competir.

**(b) La interacción encogida es señal repetida — piloto 3 y lote — y sigue
sin adjudicar.** `S-LAMBDA` del piloto 3 (ΔMAE 1.465 pp, IC95 [0.439, 2.115],
14/15 cobertura) y `R2` del lote (ΔMAE 0.48 pp, IC95 [0.10, 0.72], 88.6%
cobertura) son la misma forma de resultado dos veces: mejora medida, IC que
no toca cero, pero el criterio de victoria (¾ celdas en piloto 3; 0.5 pp de
IC-inferior en el lote) no se satisface. Dos «no venció» de tres para la
regla de salida de θ.

**(c) Nadie explica los saltos de nivel.** `SALTO-SIN-EXPLICAR` (ENCIG, PR
#972): pago de luz por canal digital, serie 2015-2025 (0.504→0.521→0.524→
0.573→0.560→0.673), con un origen móvil de cuatro pisos sin parámetros en
logit — persistencia 6.03 pp, tendencia-2 7.49, tendencia-3 5.07, tendencia-
serie 4.89 pp de MAE sobre {2021,2023,2025}×11 celdas; `ΔMAE` máximo +1.15 pp
< 3.0 pp declarados como umbral de tendencia; **en 2025 ningún piso cubre
ninguna celda**. Dictamen: ni `CAMBIO-DE-INSTRUMENTO` ni `TENDENCIA` — un
salto de una sola ola sin causa medida. Lo que persiste es el **orden** entre
categorías (gradiente de escolaridad), no el **nivel**. El mismo patrón
explica el 0/10 de cobertura de persistencia en §2.4.

**(d) Lectura que NO se debe hacer.** «88.6% de cobertura con R2» no es una
frase de producto usable sola: es el retador **no adjudicado** de una prueba
`PROPUESTA-CON-RESERVA`, cuya B-bis cayó en `NO-CAE-EN-NINGUNA-FILA` porque el
piso mismo subcubre (75.0% < 80%). Cualquier frase que cite 88.6% sin decir
«retador, no adjudicado, umbral no despejado» es la lectura que F-LOTE
prohíbe explícitamente.

---

## 4 · Qué puede afirmar el producto hoy, y qué no

**Puede afirmar, con corrida sellada detrás (heredado de v1.1 + lote):**

1. Que predice celdas de cruce que no ha visto, **cuatro veces** (tres
   pilotos + el lote ENIF 2024), con **79 celdas puntuadas**, y que el error
   del piso va de 1.47 a 3.41 pp en pilotos y **1.87 pp** en el lote.
2. Que en esos cruces **sabe cuánto se equivoca**: cobertura 26/35 en pilotos,
   75.0% (`C2`) en el lote — con el intervalo binomial y su advertencia de
   dependencia, y **acotado a los cruces ya vistos** (F-LOTE, §2.2).
3. Que la interacción encogida **mejora medida y repetida** al piso, dos veces
   (piloto 3, lote), sin que eso adjudique nada todavía.

**No puede afirmar, y este informe lo dice antes de que lo pregunten:**

- **No le gana a un modelo de lenguaje en el nivel nacional** (heredado de
  v1.1, sin corrida nueva que lo toque).
- **No conoce su error fuera de cruces con la misma confianza.** La
  cobertura de persistencia en marginales es **14/57 = 25%**, muy por debajo
  de la de cruces, y varía de 0% (ENCIG) a 53% (ENVIPE): un piso t−1 que
  «no vencido se adopta» (A-bis 6) **no** es garantía de acierto frecuente.
- **No explica por qué el nivel salta entre olas.** ENCIG lo dejó sellado:
  `SALTO-SIN-EXPLICAR`, y ninguna de las cuatro formas de piso probadas
  (persistencia, tendencia-2, tendencia-3, tendencia-serie) lo cubre.
- **La regla de salida de θ no está resuelta.** Dos de tres pruebas
  corrieron y ninguna dio victoria a un retador con interacción; falta el
  duelo ENVIPE 2026 (fecha límite 31/oct/2026).
- **No compone por segmento.** Sin cambio respecto a v1.1 (ADR-91/ADR-531).

---

## 5 · Lo que viene

- **Duelo prospectivo ENVIPE 2026** — tercera y última prueba de la regla de
  salida de θ. Fecha límite del COMMIT-2: **31/oct/2026** (`FP-…-8a1f-07`).
  Si tampoco vence un retador con interacción, `g()` y `Theta.valor` se
  retiran (`FP-…-8a1f-06`).
- **Crédito 2024** — el backtest de persistencia (7/9) es COMMIT-1; falta el
  COMMIT-2/3 con las cifras de 2024 reales, que este informe **no** tiene
  disponibles en NUBE (§2.3, declarado en NO-CORRIDO).
- **ENIGH 2024** — diseño y reserva ya sellados (`#988`); el CALC de
  emisiones/adjudicación no corrió todavía (`FP-260921-GEN2-ENIGH2024-SERIE-
  Y-COMMIT-1-7492-01`, ABIERTA: pendiente de que mesa confirme si el
  lanzamiento del encargo ya cuenta como adopción del diseño).
- **Núcleo común de ENUT** — el diseño (opción A de mesa) sigue sin CALC
  sellado que produzca el RESULT de las celdas hermanas que F-ENUT pide
  registrar; sucesor en `NC-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-01`.

---

## 6 · Módulo de auditoría de rigor extremo

*Obligatorio en todo artefacto que afirme algo sobre México (§5 de las
instrucciones). Contestado, no rellenado.*

**¿Se confunde pobreza, violencia o informalidad con cultura?** No, sin
cambio respecto a v1.1: este documento sigue sin afirmación causal sobre
conducta. El riesgo de fondo sigue siendo el mismo (evasión urbana vs.
rural, §6 de v1.1).

**¿Sobregeneralización desde clase media urbana formal?** Sin cambio: el
piloto 3 (ENCIG, universo 18+ en ciudades de 100 mil+) es el más expuesto.
El lote ENIF 2024 hereda el universo del piloto 1: cubre localidad y tamaño
de localidad, incluye rural.

**¿Sesgo de marcos o de muestras estadounidenses/europeas?** No en este
informe: todo lo citado es microdato INEGI (ENIF, ENVIPE, ENCIG, ENUT,
crédito Banxico vía el backtest).

**¿Qué cambiaría con foco rural, indígena o popular?** El piloto 3 y ENCIG
en general (universo urbano) desaparecerían. El lote ENIF 2024 y el
backtest de crédito conservan cobertura rural en la medida en que ENIF la
tiene. El sistema indígena-comunal vivo sigue fuera por diseño.

**¿Qué parece psicológico y es incentivo racional?** El salto sin explicar
de ENCIG es el ejemplo nuevo: un salto de nivel de +7.7 a +13.4 pp en pago
de luz digital entre 2023 y 2025 se lee más fácil como **cambio de oferta**
(despliegue del canal, promoción del banco/CFE) que como cambio de
disposición individual — el propio dictamen lo dice: «puede persistir la
oferta y no un rasgo» (cita heredada del cierre de #971).

**¿Dónde hay evidencia débil e intuición fuerte?** En la lectura de «R2
funciona» del lote: ΔMAE favorable (0.48 pp) e IC que no toca cero, pero
sobre **44 celdas, un solo lote, prospectivo por primera vez a esta escala**
— y el propio piso que se compara subcubre (75.0%), lo que debilita la
referencia misma. El veredicto sellado es `PROPUESTA-CON-RESERVA`, no
`VENCE`, precisamente por esto.

**¿Qué sería peligroso leído en simple?** Cuatro frases: (1) «el lote probó
que la interacción funciona» — no, `NO-CAE-EN-NINGUNA-FILA`, el B-bis no se
satisfizo; (2) «88.6% de cobertura con R2» sin el calificativo de retador no
adjudicado (§3d); (3) «14/57 en marginales» leído como una sola cifra de
confianza del programa — son tres encuestas con cobertura de 0% a 53%, no se
promedian; (4) «persistencia gana en crédito» leído como que el motor predice
crédito 2024 — es un backtest 2021→2024, no una prueba sobre 2024 real.

**[v2.16] ¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA, y se mezclan en
alguna frase?** El lote ENIF 2024 (§2.2, §3) es **PROSPECTIVA**: la spec y
los contendientes se congelaron en `#979` antes de abrir el dato (E.6). Los
tres pilotos (§2.1) son PROSPECTIVA, heredado de v1.1. El backtest de
crédito (§2.3) es **RETROSPECTIVA** por construcción (predice 2021→2024 ya
observado); el origen móvil de ENCIG (§3.c) es **RETROSPECTIVA-MECÁNICA**
(cuatro pisos sin parámetros, sin selección de variante) — ambos así
etiquetados en su propia fila y nunca sumados con las cifras prospectivas de
§2.1/§2.2. Ninguna frase de este documento mezcla las dos columnas.

**[v2.16] ¿Qué unidad tiene cada cifra y se promedia con otra?** §2.1:
persona/delito/trámite, no se promedian entre sí (heredado). §2.2: persona
(ENIF), no se promedia con §2.1. §2.3: crédito es unidad **persona/producto**
(marginal de tenencia), no se promedia con nada de §2.1/§2.2/§2.4. §2.4:
persona (ENIF), delito (ENVIPE), trámite (ENCIG) — el 14/57 agregado es un
**conteo de celdas evaluadas**, no una cifra en pp, y por eso sí se puede
sumar entre encuestas (es la misma pregunta binaria «¿cubrió?»), mientras que
los MAE de cada fila de §2.4 **no** se promedian entre encuestas.

**[v2.4, heredada] ¿En qué escala está cada cantidad?** Declarado al pie de
cada tabla, como en v1.1. Todo lo nuevo de este informe (§2.2–§2.4) está en
puntos porcentuales para MAE/ΔMAE, y en proporción de celdas para cobertura.

**[v2.3, heredada] ¿Cuántos contadores movió este trabajo?** **Cero** de los
contadores rectores (§0). Sub-razón de 15 filas `SIN-PISO` cambiada por
comando (§1.2); dos filas de `no-corrido.tsv` cerradas.

---

## 7 · Lo que este informe deja abierto

- **El detalle por celda del backtest de crédito 2024 (COMMIT-2/3, §2.3) no
  está en este informe** — no alcanzable en NUBE sin abrir el CALC completo;
  se cita el agregado del título del PR (7/9) y nada más, declarado en
  `## NO-CORRIDO / RESERVAS` del encargo que produjo este documento.
- **Las celdas hermanas de ENUT sobre el núcleo común no tienen RESULT que
  citar** (§1.2): el diseño existe, la corrida no. Sucesor: `NC-260921-
  GEN2-ENUT-PISOS-Y-SERIE-1-308c-01`.
- **El intervalo binomial correcto sigue pendiente**, heredado de v1.1:
  Wilson es lo que hay sin `scipy`.
