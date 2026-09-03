# ACTO MAESTRA36-L12 · MPS-2012-CROSSTABS — SPEC CONGELADA (COMMIT-1)

3/sep/2026 · caja UBUNTU · rama `acto/maestra36-l12-mps2012-crosstabs` · base `origin/main = ea45e01`.
ADR candidato **311** (máx hoy 310, `canon/estado-programa-v1_11.md:105`; re-derivar antes de push).
FP candidatos **FP-260** (recibo) y **FP-261** (T9b + serie ronda 1 pendientes de mesa).

**Este commit congela variables, universo y umbral. El primer resultado que produzca este
procedimiento es el que se reporta.** COMMIT-2 trae resultados y no edita este archivo.

---

## §0.0 · SECUENCIA ROTA — declarada antes de medir, y más rota de lo que el encargo suponía

El encargo declara secuencia rota para T1–T5 («secuencia rota: spec congelada después de ver
el resultado», fórmula de L8 §0.0) y sello ciego para T6–T9. **Contra el árbol, eso no se
sostiene.**

`LEEME 2-procedencia.txt` (payload `leeme_2_procedencia`, sha256 `9f0a7da9…`) trae **tres
adendas de dirección del 2/sep** con análisis numérico ya escrito de T5, T6, T7a, T7b, T8 y
T9a: ICs, t, p, gradientes, y hasta las formulaciones prohibidas. Es decir: **ninguna de las
tablas llega ciega a este acto.** La secuencia está rota para todo el paquete, no para la
primera mitad.

Lo único que queda sin ver, y es lo que este acto añade: **la diferencia de proporción
«cambió de partido entre olas» entre ofrecidos y no ofrecidos (P1)**. Las adendas verifican
la transcripción de T6 celda a celda y advierten contra cruzar oferta con voto, pero **no
calculan ese contraste**. Ese es el hueco que L12 llena.

**Y aun así P1 no es ciega en su rama dominante.** El falsador B-bis declara NO-DISCRIMINA
por ancho de IC, y el ancho depende sólo de las n. Las n ya están a la vista en el CSV: el
panel `W2_P41=1` de T6 tiene **N=48** (no 63 — ver §0.1), y tras restringir a celdas
candidato→candidato será menor. **Se sabe antes de mirar el signo que el IC excederá ±15 pp.**
Se declara aquí, en COMMIT-1, para que COMMIT-2 no pueda presentarlo como descubrimiento: la
rama NO-DISCRIMINA de P1 es *predecible desde n*, y se congela igual porque el ancho exacto y
el signo del punto sí son información nueva.

## §0.1 · Tres premisas del encargo que el árbol refuta — guardias que PARAN

Verificadas contra disco el 3/sep; los cinco payloads coinciden en sha256 con
`data/manifiesto.yaml` en `origin/main`.

| # | Premisa del encargo | Lo que hay | Efecto sobre la spec |
|---|---|---|---|
| 1 | «T6–T9 no han sido exportadas: para ellas el sello sí es ciego» | T6, T7a, T7b, T8 y T9a **están** en `icpsr35024-ds1-w2-crosstabs-derivadas.csv`; T9b no. Corroborado por `ADR-310` y por `forense/notas/2026-09-02-MAESTRA36-A1-P1-P3-registro-y-evaluacion.md:161` | **P4 NO dispara para T6.** P1 se lanza. FP-261 cubre sólo T9b y la serie de ronda 1 |
| 2 | «los guardó … como `export_crudo_mesa_2026-09-02.txt` y `T5_lista_W2.txt`» | Ninguno de los dos nombres existe (A1: 0/224). El crudo es `export_crudo.txt`; T5 está derivado dentro del CSV de derivadas | El contenido se identifica **por sha256 e identidad**, nunca por rótulo. Discordancia 2 de A1: **RESUELTA** aquí |
| 3 | «n de ofrecidos = 63» para P1 | 63 es el marginal de `W2_P41=1` en el estudio. En **T6** el panel `Sí` tiene **N=48** (col total publicado) | El universo de P1 es 48, no 63. La reserva escrita cambia de cifra |

**Discordancia 1 de A1** (`LEEME 2` se declara «Tabla T6 … 257 celdas» y el archivo trae 371
en seis tablas): **RESUELTA** — el texto original quedó `VENCIDO EN ALCANCE` por sus propias
Adendas 1–3, que sí declaran las tablas nuevas. No es contradicción sino re-sello por
crecimiento de universo; el conteo correcto es 371 (22+257+12+58+12+10).

## §0.2 · Estampa de instrumento (obligatoria en toda cifra de este acto)

Instrumento de **segunda mano**: salida del tabulador en línea «Explore Data» de ICPSR, no el
microdato. Conteos **SIN PONDERAR** (el tablero no aplica los population weights), sin
estrato ni UPM. Ola panel (ronda 2, n≈1 555). El microdato `35024-0001-Data.dta` exige
membresía institucional → `NO-ACCESIBLE` (A.4, tres intentos en A1-3).
Clase de procedencia **(3) reportada**, marca **SIN-FETCH (A.6)**.

**Tier máximo alcanzable: MEDIA con reserva. Ninguna celda de este acto entra al motor.**

---

## §1 · P0 — Censo y cuadre de marginales

Abre los cinco payloads y verifica los tres marginales que el transfer cita como control,
contra lo declarado del codebook en `LEEME-procedencia.txt`:

- `W2_P41=1 → 63` — reconstrucción: suma de `ofrecieron=1` en T1 sobre los cuatro estratos de
  `W2_P36C`, **más** los casos sin `W2_P36C`. El LEEME declara la partición `62 + 1`.
- `W2_P7=1 → 971` — reconstrucción: N total de T8 (`W2_P53 × W2_P7`), que sólo contiene a
  quien declaró haber votado.
- `W2_P40=1 → 60` — reconstrucción: suma de `condicionaron=1` en T4 sobre los cuatro estratos.

**Criterio de cuadre, fijado ahora**: T1/T4 están **restringidos a `W2_P36C` ∈ {1,2,3,4}**, así
que el subtotal estratificado debe ser **≤** el marginal del codebook, y la diferencia se
declara como «casos sin control». Cuadra si `subtotal ≤ marginal` y el hueco queda nombrado.
**PARO de pieza** si algún subtotal **excede** su marginal, o si el N de T8 ≠ 971 exacto
(T8 no está estratificado: ahí no hay hueco admisible).

## §2 · P1 — R7.7, la mitad falsable (vote-choice)

**Fuente**: T6 de `icpsr35024-ds1-w2-crosstabs-derivadas.csv` (257 celdas), `P8` (intención
ronda 1) × `W2_P8` (voto ronda 2), control `W2_P41` ∈ {0,1}.

**Mapeo candidato**, congelado (de `LEEME-procedencia.txt`):
`PAN={01}` · `PRI={02,04,09}` · `AMLO={03,05,06,10}` · `QUADRI={07}`.
Los códigos `08` (más de una casilla de distinto partido), `11` (boleta tachada), `12`
(blanco) y `13` (no piensa votar) **no son candidato** y quedan **fuera del universo** en fila
y en columna: «cambió de partido» no está definido para ellos.

**Universo de P1**: celdas de T6 con fila **y** columna en los cuatro bloques de candidato.
**Desenlace**: `cambio = 1` sse `partido(P8) ≠ partido(W2_P8)`.
**Estadístico**: `Δ = p(cambio | ofrecido) − p(cambio | no ofrecido)`; IC95 de cada proporción
por **Wilson**, IC95 de la diferencia por **Newcombe** (híbrido de scores), sobre conteos
crudos. Sin diseño muestral: no lo hay.

**Mitad turnout**: T1 (`W2_P41 × W2_P7`, agregando los cuatro estratos),
`Δ_turnout = p(votó | ofrecido) − p(votó | no ofrecido)`, mismo par Wilson/Newcombe.

**Falsador B-bis (congelado; el semi-ancho se calcula y se declara ANTES de mirar el signo):**

1. **NO-DISCRIMINA** si el semi-ancho del IC95 de `Δ_vote-change` excede **0.15** (±15 pp).
   **Esta rama tiene precedencia sobre las otras dos.**
2. **CORROBORADA** si el IC de `Δ_turnout` **y** el de `Δ_vote-change` contienen 0.
3. **CONTRARIA** si el IC de `Δ_vote-change` queda fuera de 0.

**Reservas escritas, obligatorias en la fila de resultado**: panel no ponderado · n de
ofrecidos en T6 = 48 (no 63) · `W2_P41` es autorreporte de **oferta recibida**, no de venta ·
`W2_P41` no está asignado al azar, así que esto es **asociación, no coeficiente identificado**.
Prohibido escribir «el efecto de la compra de voto es X».

## §3 · P2 — R7.3/R7.6 como tercer instrumento, sin sello

T3 (`W2_P39B × W2_P8`) y T4 (`W2_P40 × W2_P8`), control `W2_P36C`, de
`icpsr35024_DS1_W2_crosstabs_derivado_v0.csv`. Se reportan, por estrato de secreto percibido y
en agregado, las proporciones de voto PRI con IC95 Wilson y la diferencia expuesto−no expuesto
con IC95 Newcombe.

**Las lecturas preliminares (+2.0 / −3.8 pp, n 21) ya fueron vistas por mesa y dirección →
esta pieza NO adjudica.** Rótulo obligatorio de toda cifra de §3:
**`REPLICA-DE-SEGUNDA-MANO-NO-SELLADA`**. Sirve de contexto a N10, no de sello.
No mueve el veredicto de R7.3 ni el de R7.6.

## §4 · P3 — Prevalencia por experimento de lista (T5)

`Δ = media(W2_P35B) − media(W2_P35A)` sobre los conteos de T5, excluyendo `9 = NC` como lo
hace el tabulador. Igual para la ola 1 (`P35B − P35A`).
`EE = sqrt(var_B/n_B + var_A/n_A)` con varianza muestral (denominador `n−1`); IC95 normal.
Contraste contra la pregunta directa `W2_P41` (5.5 %).

Entra a la propuesta como **`MEDIDO·Δ de segunda mano`**, **no** como `p` de regla.
**Secuencia rota declarada**: la lectura 18.8 % ya está escrita en la Adenda 3.
**Supuesto no verificado que lo gobierna todo** (Adenda 3 §D.2): que lista B = lista A + un
solo ítem, y que ese ítem sea la venta del voto. El texto de los ítems **no** está en estas
salidas. Mientras eso no se lea en el cuestionario, la cifra es **PROPUESTA CON RESERVA**.
No se escribe «subió de 6.9 % a 18.8 %»: los IC de las dos olas se traslapan y el contraste
entre olas no se corre.

## §5 · P4 — no dispara para T6

T6 está en disco (§0.1 fila 1) → **P1 se lanza**. La receta de mesa se conserva sólo para lo
que de verdad falta: **T9b** (`W2_P38A × W2_P38B`, control `P46`) y la **serie de ronda 1**
(`P40×P7`, `P40×P8`, `P38B×P8|P36C`, `P39×P8`), ninguna de las cuales usa una variable
presente en disco. Eso es **FP-261**, no un PARO de este acto.

## §6 · Perímetro

Toca: `tools/medidor_l12_mps2012.py` · `data/l12-mps2012-v1_0.json` ·
`data/INFRAESTRUCTURA-v1_0.md` (alta) · `milpa/tramite-ola5-propuesta-v0.yaml` (append,
0 líneas borradas) · `forense/notas/2026-09-03-MAESTRA36-L12-*.md` · `forense/hallazgos.md` ·
`forense/firmas-pendientes.tsv` · cascada (`canon/estado-programa-v1_11.md`).
NO toca: `milpa/tramite.yaml` · `milpa/procedencia.yaml` · `data/manifiesto.yaml` ·
`data/curacion-registro/**` · `forense/prereg-duelo-v2/**`.

**Concurrencia**: si `MAESTRA36-N10 · SELLA-L9-L11` fusiona antes sobre
`milpa/tramite-ola5-propuesta-v0.yaml`, renumera quien fusiona segundo.

**El primer resultado que produzca este procedimiento es el que se reporta.**
