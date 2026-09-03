# ACTO MAESTRA36-L12 · MPS-2012-CROSSTABS — RESULTADOS (COMMIT-2)

3/sep/2026 · caja UBUNTU · **`ADR-314`** · **`FP-264`** (recibo) · **`FP-265`** (pendiente de mesa).

> **NUMERACIÓN RE-DERIVADA DESPUÉS DEL REINICIO, y no es la que la spec congelada dice.** La spec
> de COMMIT-1-bis (`§H`) y el propio medidor (`tools/medidor_l12_mps2012.py:574`, campo `"FP"` del
> JSON) citan `ADR-313`/`FP-262`/`FP-263`: eran los candidatos correctos cuando se congelaron.
> Entre ese congelamiento y este COMMIT-2, **`PR #502` (`ACTO MAESTRA36-L13`) fusionó** llevándose
> `ADR-312` y `FP-261`, y **`PR #505` (`ACTO MAESTRA36-A2`) quedó abierto** reclamando `ADR-313`,
> `FP-262` y `FP-263`. Re-derivado contra `origin/main = 18fd2bd3`:
> `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1` →
> `312`, sin duplicados; máximo de `forense/firmas-pendientes.tsv` → `261`. Con `#505` en vuelo, este
> acto toma **`ADR-314`**, **`FP-264`** (recibo) y **`FP-265`** (lo que falta). **La spec y el medidor
> NO se editan** — están congelados y COMMIT-2 no toca COMMIT-1 —, así que el campo `"FP": "FP-263"`
> del JSON queda como está y **se lee `FP-265`**; esta línea es la que manda. Si `#505` fusionara
> después de este PR, renumera `#505`, que es quien fusionaría segundo.
Encargo **v3**, `forense/encargos/2026-09-03-MAESTRA36-L12-MPS-2012-CROSSTABS.md` (`7ff61e8`).
Specs congeladas: `…-spec-congelada.md` (COMMIT-1, `b6efa1f`) y **`…-spec-congelada-bis-v3.md`
(COMMIT-1-bis, `bdd25d1`, la que manda)**. Este commit **no edita** ninguna de las dos.
Artefacto: `data/l12-mps2012-v1_0.json`.

**Estampa que gobierna cada cifra de abajo**: instrumento de **segunda mano** (tabulador
«Explore Data» de ICPSR, **no** el microdato — `35024-0001-Data.dta` exige membresía,
`A.4 NO-ACCESIBLE`) · conteos **SIN PONDERAR**, sin estrato ni UPM · ola panel ronda 2 (n≈1 555) ·
procedencia clase **(3) reportada**, marca **`SIN-FETCH (A.6)`** · **tier máximo alcanzable
MEDIA con reserva**. **Cargas al motor: 0.**

---

## 0 · Dos cosas de procedimiento que hay que decir antes de las cifras

**(a) Hubo un COMMIT-1 contra una versión superada del encargo.** Se congeló la spec contra la
**v1/v2** y se corrió. Al archivar el encargo (A.3) apareció que el árbol ya traía la **v3**,
que «sustituye íntegras las v1 y v2» y que cambia el procedimiento: compuerta **ninguna** (no
la que la v1 daba, que era incumplible por construcción), ADR **313** y FP **262/263** (no
311/260/261), desenlace de P1 **sobre el código** (no sobre el mapeo de partido), IC de la
diferencia **Wald** (no Newcombe), más una pieza de **`ROBUSTEZ`** (T7) y un **`EXPLORATORIO`**
(T8/T9a) que la v1 no pedía. Se re-congeló en COMMIT-1-bis y se volvió a correr.
**Consecuencia que no se esconde: P1 bajo la v3 no es ciega**, porque su desenlace es un vecino
cercano de uno ya visto. Las dos cifras se publican juntas (§2).

**(b) La premisa de ceguera de la v3 es falsa, y es la misma que traía la v1.** La v3 afirma que
«T6–T9 no han sido leídas en valor por nadie». `LEEME 2-procedencia.txt` — payload
`leeme_2_procedencia`, en el manifiesto desde `ADR-310` — trae **tres adendas de dirección
fechadas el 2/sep** con ICs, `t`, `p` y gradientes **en valor** de **T5, T6, T7a, T7b, T8 y T9a**,
y hasta las formulaciones prohibidas. **Lo único que ninguna adenda calcula es el contraste de
vote-change de P1.** Ése es el hueco real que este acto llena, y es más chico que el que el
encargo creía tener. Consecuencia de forma: **cuando el procedimiento manda leer la procedencia
del payload en P0 y esa procedencia contiene el análisis, el sello ciego es imposible por
diseño** — hay que decirlo en la spec, no después.

## 1 · P0 — censo y cuadre: **CUADRA en los tres marginales**

| control | marginal del codebook | reconstruido | casos sin `W2_P36C` | veredicto |
|---|---:|---:|---:|---|
| `W2_P41=1` | 63 | **62** (T1, cuatro estratos) | 1 | CUADRA |
| `W2_P40=1` | 60 | **53** (T4, cuatro estratos) | 7 | CUADRA |
| `W2_P7=1` | 971 | **971** (N de T8) | — | **CUADRA-EXACTO** |

El `62 + 1` es exactamente la partición que `LEEME-procedencia.txt` declaraba del codebook.
T8 no está estratificado y cuadra **exacto**, que era el criterio duro. **Sin PARO de pieza.**

Los **cinco payloads** coinciden en sha256 con `data/manifiesto.yaml` en `origin/main`:
`icpsr35024_ds1_w2_crosstabs_derivado_v0` (`96330f03…`), `icpsr35024_ds1_w2_crosstabs_derivadas`
(`a85c59ae…`), `export_crudo` (`daa29e0b…`), `leeme_procedencia` (`c98ce68b…`),
`leeme_2_procedencia` (`9f0a7da9…`). Censo: T1 16 · T2 32 · T3 32 · T4 32 en el derivado;
T5 22 · T6 257 · T7a 12 · T7b 58 · T8 12 · T9a 10 = **371** en las derivadas.

**Las dos discordancias de procedencia que A1 dejó a L12, cerradas — ninguna era un error:**

1. `LEEME 2` se declara «Tabla T6 … 257 celdas» y el archivo trae 371 en seis tablas. **No es
   contradicción**: las Adendas 1–3 del propio archivo declaran T7a/T7b/T8/T9a/T5 y marcan el
   texto original `VENCIDO EN ALCANCE`. Es **re-sello por crecimiento de universo** — la
   disciplina de la casa funcionando. El conteo correcto es 371 (22+257+12+58+12+10).
2. `export_crudo_mesa_2026-09-02.txt` y `T5_lista_W2.txt` no existen en disco: el crudo es
   `export_crudo.txt` y T5 está derivado dentro del CSV de derivadas. **Cerrada por sha256, no
   por nombre.** (La v3 ya había incorporado la mitad de esto.)

## 2 · P1 — R7.7 `[MEDIA]`: **`NO-DISCRIMINA`**, y el signo depende de cómo se cuente el cambio

Universo: T6 restringido a celdas con `P8` **y** `W2_P8` en los nueve códigos partidarios
fijados en COMMIT-1-bis §C (`01,02,03,04,05,06,07,09,10`; fuera `08` casillas de distinto
partido, `11` anuló, `12` blanco, `13` no votó). Eso excluye 216 casos y deja **605** no
ofrecidos y **35** ofrecidos. IC de la diferencia: **Wald**, como pide la v3.

| contraste | ofrecidos | no ofrecidos | Δ | IC95 (Wald) | semiancho |
|---|---|---|---:|---|---:|
| **turnout** (T1) | 52/62 = 83.87 % | 906/1 056 = 85.80 % | **−1.92 pp** | [−11.32, +7.47] | 9.39 pp |
| **vote-change, primario v3** (`P8 ≠ W2_P8`, código) | 16/35 = 45.71 % | 246/605 = 40.66 % | **+5.05 pp** | [−11.91, +22.01] | **16.96 pp** |
| **vote-change, `YA-VISTO-BAJO-SPEC-ANTERIOR`** (mapeo de partido) | 11/35 = 31.43 % | 203/605 = 33.55 % | **−2.13 pp** | [−17.96, +13.71] | 15.83 pp |

**Veredicto B-bis: `NO-DISCRIMINA`**, por la rama de precedencia: el semiancho del IC del
contraste primario es **16.96 pp**, contra el umbral **15 pp** congelado antes de correr.
**El veredicto es robusto**: los tres contrastes tienen el cero bien dentro, y las dos
codificaciones de vote-change superan el umbral (16.96 y 15.83 pp). La v3 había anunciado que
`NO-DISCRIMINA` era «el desenlace más probable»; lo es, y por más margen del que ella suponía,
porque el n del universo de la pieza es **35**, no los 63 del marginal del estudio.

**Lo que sí es un hallazgo y hay que decirlo: el signo del punto se voltea con la codificación.**
Contar el cambio **sobre el código** da **+5.05 pp** (los ofrecidos cambian *más*); contar sobre
el **mapeo de partido** da **−2.13 pp** (cambian *menos*). La diferencia entera está en los pares
`02↔04` y `03↔05↔06`: **cambiar de casilla dentro de la misma coalición** —Peña Nieto por PRI o
por PVEM, AMLO por PRD, PT o Movimiento Ciudadano— es «cambio» bajo el desenlace de la v3 y no
lo es bajo el del mapeo. **Con n=35 ninguno de los dos signos significa nada**; lo que el par
demuestra es que **en este instrumento el signo de R7.7 es una decisión de codificación, no un
dato**. Cualquier futuro intento sobre estas tablas tiene que fijar esa decisión —y justificarla
sustantivamente— antes de mirar, o no está midiendo nada.

**Sustantivamente los dos halves son nulos**: −1.9 pp de turnout y ±2–5 pp de vote-choice, todos
con el cero dentro. Lo que R7.7 predice —que la dádiva mueva **turnout** y **no** vote-choice—
**no se ve**, porque no mueve ninguno de los dos. **La regla sale igual de sin probar que entró**,
ahora con un tercer instrumento que lo dice con IC y con el primer dato mexicano de vote-choice
sobre **la misma persona** entre dos olas.

**Reservas, obligatorias donde vaya la cifra**: panel **no ponderado** · **n de ofrecidos = 35**
(el panel «Sí» completo de T6 es 48; el marginal del estudio es 63 — el encargo, v1 y v3, supuso
63 y es la cifra equivocada para esta pieza) · `W2_P41` es autorreporte de **oferta recibida**,
no de venta: la prevalencia bruta es un piso · **la selección de quién recibe oferta no es
aleatoria** → **asociación, no coeficiente identificado**. **Prohibido escribir «el efecto de la
compra de voto es X».**

### 2-bis · `ROBUSTEZ` (T7a/T7b por `W2_PX8`) — no adjudica

| ámbito | prevalencia de oferta | turnout ofrecidos | turnout no ofrecidos | Δ | IC95 |
|---|---:|---|---|---:|---|
| Urbano | 5.4 % (45/835) | 37/45 = 82.2 % | 667/790 = 84.4 % | −2.21 pp | [−13.7, +9.2] |
| Rural | 5.4 % (16/297) | 13/16 = 81.3 % | 244/281 = 86.8 % | −5.58 pp | [−25.1, +13.9] |
| Mixto | 16.7 % (2/12) | 2/2 | 8/10 | +20.00 pp | [−4.8, +44.8] |

**Urbano y rural tienen prevalencia de oferta prácticamente idéntica (5.4 % y 5.4 %)**, lo que
corre en contra de la narrativa de *targeting* rural; sostener lo contrario exige otra fuente.
Los tres Δ de turnout contienen el cero y las celdas de ofrecidos son de una o dos decenas de
casos: **descriptivo, no efecto**. La celda «Mixto» tiene n=2 y n=10: no sostiene nada.

## 3 · P2 — R7.3 / R7.6: réplica que **no adjudica**, y que **no reproduce** la lectura preliminar

Rótulo obligatorio de todo lo de abajo: **`REPLICA-DE-SEGUNDA-MANO-NO-SELLADA`**.
Desenlace: voto PRI (`W2_P8`); control `W2_P36C` (secreto percibido, 1–4); IC de la diferencia Wald.

| tabla | expuesto a | expuesto | no expuesto | Δ agregado | IC95 |
|---|---|---|---|---:|---|
| **T3** | `W2_P39B` (Oportunidades) | 86/204 = 42.16 % | 365/874 = 41.76 % | **+0.39 pp** | [−7.13, +7.92] |
| **T4** | `W2_P40` (condicionaron el programa) | 19/53 = 35.85 % | 243/569 = 42.71 % | **−6.86 pp** | [−20.39, +6.68] |

Los dos IC contienen 0. **Ninguno mueve el veredicto de R7.3 ni el de R7.6** —que ya venían con
`CONTRARIA-REPLICADA` por L9+L11— y por spec no podían.

**Hallazgo lateral que `N10` necesita: las cifras preliminares del encargo no se reproducen.**
El encargo (v1 y v3) cita «+2.0 / −3.8 pp, n 21». Agregando los cuatro estratos sale
**+0.39 / −6.86**, con n de expuestos 204 y 53. **Ninguna celda por estrato da el par
(+2.0, −3.8)**; lo más cercano es T3 estrato 2 (+2.47 pp). No se resuelve aquí —la spec prohíbe
que esta pieza adjudique—, se deja **medido** para que `N10` sepa que el par preliminar no tiene
respaldo reproducible en estas tablas.

Dos celdas degeneradas, declaradas para que nadie las cite: **T4 estrato 4** tiene expuestos
`n=0` (sin IC posible) y **T4 estrato 3** es `0/8` contra `13/37` — un IC que roza el cero **con
numerador cero** no es evidencia de nada.

## 4 · P3 — experimento de lista (T5): **`MEDIDO·Δ de segunda mano`**, no `p` de regla

| ronda | lista A | lista B | Δ | EE | t | IC95 |
|---|---|---|---:|---:|---:|---|
| 1 · marzo (`P35A`/`P35B`) | 1.3035 (n=649) | 1.3723 (n=650) | **0.0688** | 0.0490 | 1.40 | [−0.027, +0.165] — **cruza 0** |
| 2 · julio (`W2_P35A`/`W2_P35B`) | 1.5532 (n=573) | 1.7409 (n=575) | **0.1876** | 0.0523 | 3.59 | [+0.085, +0.290] |

`NC(9)` excluido, como lo hace el tabulador. **Reproduce exactamente** los cuatro medios, las dos
diferencias, los dos EE y los dos IC de la Adenda 3: la aritmética de dirección es correcta y
ahora es reproducible desde el CSV con un script, no a mano.

Lectura admitida: en julio **~18.8 %** de la submuestra afirma el ítem sensible sin declararlo
directamente; en marzo la estimación es **6.9 %** y **no se distingue de cero**. Contra la
pregunta directa (`W2_P41`, 5.5 %) eso es un factor de **3.41**.

**Cuatro cosas van pegadas a esa cifra, o la cifra no se usa:**

1. **Secuencia rota en las DOS rondas.** La v3 daba la de ronda 1 por no vista; la Adenda 3 ya
   traía `0.0688`, `EE 0.0490`, `t 1.40` e `IC [−0.027, 0.165]`. **Las dos estaban vistas.**
2. **Supuesto no verificado que gobierna la pieza entera**: que lista B = lista A + **un** ítem, y
   que ese ítem sea la venta del voto. **El texto de los ítems no está en estas salidas.** Hasta
   leerlo en el cuestionario, **PROPUESTA CON RESERVA**, no prevalencia medida. Si el cuarto ítem
   no es el sensible, **la pieza entera se cae**.
3. **No se escribe «subió de 6.9 % a 18.8 %»**: los IC de las dos rondas se traslapan y el
   contraste entre rondas no se corrió.
4. El factor **3.41 mezcla subreporte con diferencia de constructo** — `W2_P41` pregunta si le
   **ofrecieron**; el ítem de la lista, si el supuesto 2 se sostiene, pregunta por **conducta
   propia** — y estas tablas no permiten repartirlo entre los dos.

## 5 · P4 — T8 y T9a, `EXPLORATORIO`, sin veredicto (sólo a esta nota)

**T8 · marca en credencial × voto declarado** (n=971). La columna «no votó» es **cero en las seis
filas**: `W2_P53` sólo se preguntó a quien declaró haber votado. **T8 no puede calibrar
sobrerreporte de participación**, que era la función que el plan le asignaba — no hay no-votantes
en el denominador. Lo que sí mide, que es otra cosa: entre quienes declararon votar,
**656/971 = 67.6 %** queda corroborado por marca. El 32.4 % restante **no se colapsa**: «no tiene
marca» (27) y «afirma haber votado sin marca» (38) son evidencia contra el autorreporte; «no pudo
ver» (60), «no trae credencial» (129) y «se niega a mostrar» (61) son **`NO-VERIFICABLE`, no
falso**, y colapsarlos produciría una tasa de mentira inflada por rechazo a mostrar identificación.

**T9a · percepción de compra de voto × oferta recibida** (n=1 134):

| «en mi comunidad los políticos compran votos» | recibió oferta | % |
|---|---|---:|
| Totalmente de acuerdo | 37/379 | 9.76 % |
| Algo de acuerdo | 21/333 | 6.31 % |
| Algo en desacuerdo | 4/179 | 2.23 % |
| Totalmente en desacuerdo | 0/150 | 0.00 % |
| NS | 0/93 | 0.00 % |

Gradiente monótono en las cuatro categorías sustantivas; prevalencia global **62/1 134 = 5.47 %**.
**Prohibido escribir «la percepción de compra de voto es sobre todo vivencia»**: las dos variables
son de la **misma ola** (sin orden temporal), el sentido más probable es el inverso —recibir el
regalo produce el reporte—, y **aun entre quienes están totalmente de acuerdo, el 90.2 % no
recibió oferta**. La percepción **excede a la experiencia por un orden de magnitud**. `NS` no se
colapsa con «en desacuerdo»: una celda con numerador 0 sostiene «ninguna observada en esta
muestra», no «cero ofertas».

## 6 · Lo que de verdad falta (**FP-265**; el JSON, congelado, la llama `FP-263`)

**T9b** (`W2_P38A × W2_P38B`, control `P46`) y la **serie de ronda 1** (`P40×P7`, `P40×P8`,
`P38B×P8|P36C`, `P39×P8`). **Control negativo**: ninguna tabla del disco usa `P40`, `P39` ni
`P38B` como variable de fila o columna. Receta (≤1 min por tabla): *Explore Data → Crosstabs*;
T9b es fila `W2_P38A`, columna `W2_P38B`, control `P46`, exportar.
Y lo que desbloquea P3 no es una tabla sino una lectura: **el texto de los ítems de
`P35A`/`P35B`/`W2_P35A`/`W2_P35B` en el cuestionario de ICPSR 35024.**

## 7 · Contador

- **R7.7 vote-choice: +1 veredicto** (`NO-DISCRIMINA`) — primer dato mexicano sobre la misma
  persona, con el hallazgo de que el signo depende de la codificación.
- **R7.3/R7.6: +1** tercer instrumento (`REPLICA-…-NO-SELLADA`, no adjudica).
- **Lista: +2 Δ** (ronda 1 y ronda 2).
- **Entradas nuevas en la propuesta: +2**, ambas `PENDIENTE-DE-MESA`, **0 líneas borradas**.
- **Cargas al motor: 0.**

## 8 · Lo que este acto NO hizo

No selló nada · no cargó al motor · no descargó nada · no ponderó lo que no trae ponderador ·
no tocó las entradas de L9/L11 · no leyó T6 antes de que COMMIT-1 estuviera en el árbol ·
no tocó `data/manifiesto.yaml`, `milpa/tramite.yaml`, `milpa/procedencia.yaml`,
`data/curacion-registro/**` ni `forense/prereg-duelo-v2/**` · no modificó los payloads (lectura).
