# ACTO MAESTRA36-L12 — SPEC CONGELADA **BIS**, contra el encargo **v3** (COMMIT-1-bis)

3/sep/2026 · rama `acto/maestra36-l12-mps2012-crosstabs` · base `origin/main = ea45e01`.
Sustituye operativamente a `2026-09-03-MAESTRA36-L12-spec-congelada.md` (COMMIT-1, `b6efa1f`),
que **no se edita**: queda como está, y este archivo declara qué de aquél sigue vivo y qué no.

**Este commit congela la spec v3 y NO corre el medidor sobre las piezas nuevas.
El primer resultado que produzca este procedimiento es el que se reporta.**

---

## §A · Por qué hay un bis, y qué se rompió con eso

COMMIT-1 se congeló contra la **v1/v2** del encargo, que era la que dirección había pasado al
ejecutor. Al ir a archivar el encargo (A.3) apareció que el árbol ya traía **la v3**
(`forense/encargos/2026-09-03-MAESTRA36-L12-MPS-2012-CROSSTABS.md`, commit `7ff61e8`),
autocontenida y que «**sustituye íntegras las v1 y v2**». **La v3 manda.** Diferencias que
cambian el procedimiento, no sólo la prosa:

| | v1/v2 (lo que congeló COMMIT-1) | **v3 (lo que manda)** |
|---|---|---|
| Compuerta | `grep -c 'icpsr35024_crosstabs' … > 0` (da 0) | **ninguna**, cumplida por producto |
| ADR / FP | 311 · FP-260/261 | **313** · **FP-262** (recibo), **FP-263** sólo si P0 para |
| Desenlace de P1 | `partido(P8) ≠ partido(W2_P8)` con mapeo PAN/PRI/AMLO/QUADRI | **`P8 ≠ W2_P8` sobre el código**, en universo de códigos partidarios |
| IC de la diferencia | Newcombe | **normal (Wald)** sobre conteos crudos |
| P1 robustez | — | **T7a/T7b** por `W2_PX8`, rotulado `ROBUSTEZ` |
| P4 | receta para mesa de T6–T9 | **T8 y T9a**, inventario `EXPLORATORIO`, sólo a la nota |
| P2 fuente | `…derivado_v0.csv` | `export_crudo.txt` (T1–T4) |

**Lo que esto rompe, y se declara antes de medir:** COMMIT-1 ya se ejecutó, así que **el
contraste de P1 bajo el desenlace de mapeo de partido ya fue visto** (Δ = −2.13 pp, n 35/605).
El desenlace de la v3 es **distinto** —cuenta `02→04` (Peña Nieto por casilla PRI y por casilla
PVEM) como cambio, y el mapeo no— pero es **un vecino muy cercano** del ya visto. Por tanto:

> **P1 bajo la v3 NO es ciega.** Lo es menos que lo que la v3 supone y menos de lo que COMMIT-1
> podía prometer. Se congela igual, se corre igual, y **las dos cifras se publican juntas** en
> el artefacto: la de la v3 adjudica por autoridad del encargo, la de COMMIT-1 se reporta como
> lo que es, un resultado ya visto bajo una spec anterior. Ninguna se esconde.

## §B · Lo que sigue vivo de COMMIT-1, sin cambio

- **§0.0 — la secuencia está rota para las nueve tablas, no para T1–T5.** La v3 **repite** la
  premisa de la v1 («T6–T9 no han sido leídas en valor por nadie … para ellas el sello es
  ciego, y por eso T6 es la que adjudica») y **la premisa sigue siendo falsa**:
  `LEEME 2-procedencia.txt` (payload `leeme_2_procedencia`, ya en el manifiesto desde
  `ADR-310`) trae **tres adendas de dirección fechadas el 2/sep** con ICs, `t`, `p` y
  gradientes **en valor** de **T5, T6, T7a, T7b, T8 y T9a**, y hasta las formulaciones
  prohibidas. Concretamente: T7a/T7b con prevalencias por ámbito y participación declarada;
  T8 con el 67.6 % corroborado y el desglose de los cinco estados; T9a con el gradiente
  9.8/6.3/2.2/0.0 %; T5 con `0.0688` y `0.1876`, sus EE, sus `t` y sus IC. **Lo único que
  ninguna adenda calcula es el contraste de vote-change de P1** — ése es el hueco real, y es
  el que este acto llena.
- **§0.1 fila 2 — los rótulos de archivo del transfer no existen.** La v3 ya lo incorpora para
  `T5_lista_W2.txt`. Se mantiene la regla: **el contenido se identifica por sha256, no por
  rótulo.**
- **§0.2 — la estampa de instrumento**, íntegra: segunda mano · sin ponderar · sin estrato ni
  UPM · procedencia clase (3) · marca `SIN-FETCH (A.6)` · **tier máximo MEDIA con reserva** ·
  **ninguna celda entra al motor**.
- **El criterio de cuadre de P0** (§1 de COMMIT-1): T1/T4 están restringidos a
  `W2_P36C ∈ {1,2,3,4}`, así que el subtotal debe ser **≤** el marginal del codebook y el hueco
  se declara; **T8 cuadra exacto o PARO**. La v3 dice sólo «discordancia → PARO»; este criterio
  lo hace operativo y **es más estricto**, no más laxo.

## §C · P0 (v3) — censo, estampa y **códigos fijados antes de abrir T6**

Marginales de control: `W2_P41=1 → 63` · `W2_P7=1 → 971` · `W2_P40=1 → 60`, con el criterio de
cuadre de §B.

**Códigos de `P8`/`W2_P8` que cuentan como voto por partido**, fijados aquí, antes de T6, desde
las etiquetas del propio tabulador:

| código | etiqueta | ¿partidario? |
|---|---|---|
| `01` | Josefina Vázquez Mota — PAN | **sí** |
| `02` | Enrique Peña Nieto — casilla PRI | **sí** |
| `03` | AMLO — casilla PRD | **sí** |
| `04` | Enrique Peña Nieto — casilla PVEM | **sí** |
| `05` | AMLO — casilla PT | **sí** |
| `06` | AMLO — casilla Mov. Ciudadano | **sí** |
| `07` | Gabriel Quadri — Nueva Alianza | **sí** |
| `09` | tachó más de una casilla **de Peña Nieto** | **sí** (atribuible a una sola coalición) |
| `10` | tachó más de una casilla **de AMLO** | **sí** (atribuible a una sola coalición) |
| `08` | tachó más de una casilla **de diferente partido** | **no** — no atribuible |
| `11` | tachó toda la boleta / la rayó | **no** — anuló |
| `12` | dejó en blanco | **no** |
| `13` | mencionó que no piensa votar | **no** — no votó |

`W2_P41`: `1` = le ofrecieron, `0`/`2` = no. (En el CSV el control viene codificado `0`/`1`;
el `2` del codebook y el `0` del tabulador son la misma categoría «No».)

## §D · P1 (v3) — R7.7, vote-choice sobre T6

**Universo**: celdas de T6 con `P8` **y** `W2_P8` en los nueve códigos partidarios de §C.
**Desenlace primario (v3)**: `cambió = 1` sse **`P8 ≠ W2_P8`** (comparación de **código**).
**Desenlace secundario (COMMIT-1, ya visto)**: `partido(P8) ≠ partido(W2_P8)` con
`PAN={01}`, `PRI={02,04,09}`, `AMLO={03,05,06,10}`, `QUADRI={07}`. **Se publica junto al
primario, rotulado `YA-VISTO-BAJO-SPEC-ANTERIOR`.**

**Estadístico**: `Δ = p(cambió | ofrecido) − p(cambió | no ofrecido)`; IC95 **Wilson** en cada
proporción, IC95 de la diferencia **normal (Wald)** sobre conteos crudos: `Δ ± 1.96·√(p₁q₁/n₁ + p₀q₀/n₀)`.
Sin diseño muestral: no lo hay.

**Complemento, misma pieza**: turnout desde T1 (`W2_P41 × W2_P7`, agregando los cuatro
estratos), `Δ_turnout` con el mismo par Wilson/Wald.

**Falsador B-bis, congelado (el semiancho se calcula y se declara ANTES de mirar el signo):**

1. **NO-DISCRIMINA** si el semiancho del IC95 de `Δ` (vote-change) supera **0.15** (±15 pp).
   **Precedencia sobre las otras dos.** La v3 declara por adelantado que *«con n de ofrecidos
   ≈ 63 es el desenlace más probable»*; se hace constar que el n real del universo de la pieza
   es **menor que 63** (63 es el marginal del estudio; el panel «Sí» de T6 es 48), así que la
   predicción de la v3 es, si acaso, más segura de lo que ella misma creía.
2. **CORROBORADA** si el IC de `Δ_turnout` **y** el de `Δ` contienen 0.
3. **CONTRARIA** si el IC de `Δ` queda fuera de 0.

**Robustez (v3), sin adjudicar**: T7a (`W2_P41 × W2_P7`) y T7b (`W2_P41 × W2_P8`) con control
`W2_PX8` (1 urbano / 2 rural / 3 mixto): `Δ_turnout` y nivel de voto por estrato, con IC.
Rótulo **`ROBUSTEZ`**. No mueve el veredicto.

**Reservas escritas, obligatorias**: panel **sin ponderar** · **n de ofrecidos** (se reporta el
del universo de la pieza, no el 63 del marginal) · **la selección de quién recibe oferta no es
aleatoria** → **asociación, no coeficiente identificado**. Prohibido escribir «el efecto de la
compra de voto es X».

## §E · P2 (v3) — R7.3/R7.6, no adjudica

T3 (`W2_P39B × W2_P8`) y T4 (`W2_P40 × W2_P8`), control `W2_P36C`. Proporciones de voto PRI con
IC95 Wilson por estrato y en agregado; diferencia expuesto−no expuesto con IC95 Wald.
Lecturas ya vistas (+2.0 / −3.8 pp, n 21) → **no adjudica**. Rótulo obligatorio:
**`REPLICA-DE-SEGUNDA-MANO-NO-SELLADA`**. Contexto para `N10`, no sello.

*Nota de fuente*: la v3 pide leerlo de `export_crudo.txt`; este acto lo lee de
`icpsr35024_DS1_W2_crosstabs_derivado_v0.csv`, que es **la transcripción de dirección de las
mismas tablas** (así la describe la propia v3) y viene ya en formato largo. Es la misma
información por otra vía; se declara para que se pueda reproducir por la vía que la v3 nombra.

## §F · P3 (v3) — experimento de lista (T5)

`Δ = media(B) − media(A)` en las dos rondas: `W2_P35B − W2_P35A` (ronda 2) y `P35B − P35A`
(ronda 1). `NC(9)` excluido, como lo hace el tabulador. `EE = √(var_B/n_B + var_A/n_A)` con
varianza muestral (`n−1`); **IC95 normal**. Contraste contra la pregunta directa (5.5 %).

Entra como **`MEDIDO·Δ de segunda mano`**, **no** como `p` de regla.
**Secuencia**: la de **ronda 2** (18.8 %) **ya fue vista** (Adenda 3) → rota, declarada.
**La de ronda 1 la v3 la da por no vista**; y **tampoco lo es**: la misma Adenda 3 trae
`0.0688`, `EE 0.0490`, `t 1.40`, `IC [−0.027, 0.165]`. **Las dos rondas están vistas.**
**Supuesto no verificado que gobierna la pieza entera**: que lista B = lista A + **un** ítem y
que ese ítem sea la venta del voto — el texto de los ítems **no** está en estas salidas.
Hasta leerlo en el cuestionario, **PROPUESTA CON RESERVA**, no prevalencia medida.
No se escribe «subió de 6.9 % a 18.8 %»: los IC se traslapan y el contraste entre olas no se corre.

## §G · P4 (v3) — T8 y T9a, `EXPLORATORIO`, sólo a la nota

`W2_P53` (marca en credencial) × `W2_P7`, y `W2_P36D` (percepción de compra de voto) × `W2_P41`:
tabla de proporciones con IC95 Wilson, rótulo **`EXPLORATORIO`**, **sin veredicto**.
**Entra sólo a la nota; no entra a la propuesta.**
Se hará constar lo que la Adenda 2 ya midió y que limita T8: la columna «no votó» es **cero** en
las seis filas (`W2_P53` sólo se preguntó a quien declaró haber votado), así que **T8 no puede
calibrar sobrerreporte de participación**, que era la función que el plan le asignaba.

## §H · Perímetro (v3) y numeración

Toca: `tools/medidor_l12_mps2012.py` · `data/l12-mps2012-v1_0.json` ·
`data/INFRAESTRUCTURA-v1_0.md` · `milpa/tramite-ola5-propuesta-v0.yaml` (append, **0 líneas
borradas**) · `forense/notas/2026-09-03-MAESTRA36-L12-*.md` · `forense/hallazgos.md` ·
`forense/firmas-pendientes.tsv` · cascada.
NO toca: `milpa/tramite.yaml` · `milpa/procedencia.yaml` · `data/manifiesto.yaml` ·
`data/curacion-registro/**` · `forense/prereg-duelo-v2/**` · los payloads (lectura).

**ADR candidato 313** · **FP-262** (recibo) · **FP-263** sólo si P0 para. Re-derivar al fusionar.
**Concurrencia**: `MAESTRA36-L13` también hace append al pie de la propuesta y escribe
`firmas-pendientes.tsv`; **renumera quien fusiona segundo**.

**El primer resultado que produzca este procedimiento es el que se reporta.**
