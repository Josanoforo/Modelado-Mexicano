# Bandas pre-registradas · DOC-01..DOC-06 — 25/ago/2026

**Acto:** `BANDAS-DOC-6` (nube, Opus). Ejecuta `FP-94`/`FP-126` (mesa `GO`, `ADR-155`, «FP94: GO.»). **No corre el árbitro** — este documento se escribe y se congela **antes** de que `ADV1-M3`/`scoring-adv1-m3.py` corra sobre ninguna de las seis celdas `DOC-0x`.

**Regla que se ejecuta, verbatim (`ADR-135(e)`, `FP-83` `FIRMADA`):** *"Los árbitros sin error muestral llevan banda propia, pre-registrada, derivada de otra fuente de error del registro [...] revisión, redondeo de la publicación, ventana temporal — declarada en la ficha de cada celda antes de ver el dato, no post-hoc."* `FP-83` selló la regla; **no** derivó la banda celda por celda — eso es exactamente lo que este documento hace, y nada más. Ninguna banda de abajo introduce una cuarta fuente de error distinta de las tres que `FP-83` nombra (revisión / redondeo de publicación / ventana temporal).

**Por qué estas seis y no otras.** Las seis filas viven en `forense/marco-candidatas-piloto-v1_0.tsv` líneas 56–61, columna `id` = `DOC-01`..`DOC-06`. Son las únicas seis filas del marco marcadas `NO APLICA :: censo administrativo o contable dictaminado, sin error estandar muestral` en la columna `cv_arbitro` — el hueco exacto que `ADR-135(e)` declaró entre `ADV1-M1(ii)` y `ADV1-M3` (`INDECIDIBLE` si `|d_L−d_M| < 0.5·EE(R)`, que nunca dispara con `EE=0`).

**Fuente primaria de cada cifra:** `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md` (archivado `verbatim`, `FP-61`, no se re-edita ni se re-etiqueta — se cita, no se recalcula).

---

## DOC-01 · Banco Azteca — IMOR ajustado

- **Cifra registrada:** IMOR ajustado **~10.7%** (2025). Fuente: HR Ratings, *"Banco Azteca — Reporte 2024"* (5-jul-2024) vía CNBV / Whitepaper Intel, recogida en `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md:26` y `:66`.
- **Fuente de la banda:** **redondeo de la publicación.** La cifra se publica a **un decimal porcentual** (`10.7%`); el árbitro no tiene acceso al valor sin redondear, solo al publicado.
- **Ancho:** `±0.05 pp` (medio último-dígito publicado — regla estándar de redondeo: el valor real puede estar en cualquier punto de `[10.65%, 10.75%)` y colapsar a `10.7%`).
- **Banda pre-registrada:** `[10.65%, 10.75%]`.
- **Por qué ese ancho y no otro:** es la única fuente de error que `FP-83` autoriza que se pueda leer directamente del propio dato publicado, sin inventar un supuesto de diseño muestral (que no existe: es censo administrativo). No se ensancha por el matiz "~" que el propio corpus antepone a la cifra —ensanchar por esa vía exigiría cuantificar la magnitud de la aproximación de la fuente secundaria, dato que el corpus no trae, y `FP-83` prohíbe post-hoc, no autoriza inventar un segundo ancho sin fuente.

## DOC-02 · BanCoppel — IMOR ajustado

- **Cifra registrada:** IMOR ajustado **15.7%** (3T24). Fuente: HR Ratings, *"BanCoppel — Reporte Revisión 2024"* (16-dic-2024), `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md:27` y `:72`.
- **Fuente de la banda:** **redondeo de la publicación**, mismo mecanismo que `DOC-01` — un decimal porcentual.
- **Ancho:** `±0.05 pp`.
- **Banda pre-registrada:** `[15.65%, 15.75%]`.
- **Por qué ese ancho:** misma regla que `DOC-01` — redondeo del último decimal publicado, nada más. La celda también trae una **trayectoria** (`IMOR simple 8.4% (3T24) → 5.5% (3T25)`), pero la cifra que `marco-candidatas-piloto-v1_0.tsv` registra como cifra enunciada de esta celda (col. `publicada`) es el nivel ajustado `15.7%` de `3T24`, no la trayectoria del IMOR simple — la banda se deriva sobre la cifra que el marco efectivamente registró, no sobre una variable distinta.

## DOC-03 · razón Azteca / tarjeta banca múltiple — razón derivada, no enunciada

- **Cifra registrada:** razón `IMOR_ajustado(Azteca) / IMOR_ajustado(tarjeta banca múltiple)` = `10.7% / 13.7%`, jun-2025. Ningún documento la enuncia como razón — `compass-4` yuxtapone `10.7%` (`:26`) y `13.7%` (`:45`) sin dividirlos; la razón es derivación de este acto de pre-registro, no un dato adicional inventado (ambos operandos ya están en el marco).
- **Fuente de la banda:** **redondeo de la publicación**, propagado a través de la razón. Cada operando trae `±0.05 pp` por la misma regla que `DOC-01`/`DOC-02` (ambos a un decimal porcentual). Para una razón `r = a/b`, el error relativo se propaga como suma de errores relativos: `Δr/r ≈ Δa/a + Δb/b` (primer orden, sin covarianza declarada entre las dos fuentes — `HR Ratings` para ambas, pero de reportes distintos, sin correlación conocida que se pueda citar sin inventarla).
- **Cálculo, a la vista:**
  - `r = 10.7/13.7 = 0.78102...`
  - `Δa/a = 0.05/10.7 = 0.004673`; `Δb/b = 0.05/13.7 = 0.003650`
  - `Δr/r = 0.004673 + 0.003650 = 0.008323`
  - `Δr = 0.78102 × 0.008323 = 0.00650`
- **Banda pre-registrada:** `r = 0.7810 ± 0.0065`, i.e. `[0.7745, 0.7875]` (equivalente `[77.45%, 78.75%]` si la razón se expresa como porcentaje).
- **Por qué ese ancho:** es la propagación de redondeo de primer orden sobre los dos únicos operandos que la propia fuente publica — no se asume un tercer decimal ni una correlación entre los dos reportes de HR Ratings que no está declarada en ninguna parte, lo que inventaría una reducción de banda sin fuente.

## DOC-04 · FirstCash — inventario de prenda no redimida > 1 año

- **Cifra registrada:** proporción de inventario con antigüedad mayor a un año, **1%–2%** (2024–25). Fuente: SEC 10-K FirstCash, `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md:29`.
- **Fuente de la banda:** **redondeo/rango de la publicación**, en su forma más directa — la propia fuente audita y publica un **rango**, no un punto. No hay redondeo que inferir: el ancho lo trae el documento mismo.
- **Ancho:** el rango completo publicado, `1.5% ± 0.5 pp` (punto medio del rango declarado, half-width = mitad del rango).
- **Banda pre-registrada:** `[1.0%, 2.0%]`.
- **Por qué ese ancho:** a diferencia de `DOC-01`/`DOC-02`, aquí no hace falta derivar un half-unit de redondeo porque el propio 10-K entrega el rango como el dato — usar el rango publicado tal cual es la lectura más literal de "redondeo de la publicación" que permite `FP-83`, sin estrechar el rango con un supuesto de distribución interna que la fuente no declara (no se asume, por ejemplo, que el punto medio sea más probable).

## DOC-05 · Compartamos (Gentera) — castigos como fracción de cartera total promedio del ejercicio

- **Cifra registrada:** fracción **NO enunciada** en ninguna fuente del corpus — `marco-candidatas-piloto-v1_0.tsv` línea 60 ya lo declara (`sin cifra enunciada localizada`). El corpus trae el **numerador** (castigos: Ps. 542 M 4T22, Ps. 1,130 M 4T24, Ps. 2,406 M 4T25 — `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md:30`, `:84–86`) pero **no** trae el **denominador** ("cartera total promedio del ejercicio") en ninguna cita rastreada de ese archivo.
- **Fuente de la banda:** **redondeo de la publicación** — pero solo del numerador. Los tres montos de castigos se publican como enteros en millones de pesos (`542`, `1,130`, `2,406` — sin decimales en ninguno de los tres, patrón consistente de reporte contable dictaminado redondeado al millón).
- **Ancho declarado, parcial y explícito como tal:** `±0.5 M` (medio millón de pesos) sobre el numerador, por la misma regla de medio-último-dígito que `DOC-01`/`DOC-02`. **No se declara ancho para el denominador** porque la cifra de cartera total promedio del ejercicio de Compartamos no está localizada en el corpus archivado — inventar un ancho para un número que no se ha visto violaría la instrucción explícita de este acto ("sin inventos nuevos") y la de `FP-83` ("declarada... antes de ver el dato", que presupone que el dato con el que se deriva ya existe en el registro).
- **Banda pre-registrada:** **incompleta por diseño** — `±0.5 M` sobre el numerador (`Ps. 2,406 M ± 0.5 M` para la ola 4T25, la más reciente), **denominador pendiente**. El árbitro **no puede** puntuar esta celda con una banda completa hasta que el acto que corra el árbitro localice y cite la cifra de cartera total promedio del ejercicio con su propia fuente y su propio redondeo declarado — este acto no la busca (fuera de perímetro: pre-registro de banda, no adquisición de dato nuevo).
- **Por qué esta banda queda así:** es preferible declarar el hueco explícitamente, celda por celda, tal como `ADR-135(e)` exige ("declarada en la ficha de cada celda"), a producir una banda completa con un denominador inventado que un árbitro futuro no podría auditar contra ninguna fuente citada.

## DOC-06 · Financiera Independencia (Findep) — IMOR ajustado, 4T2026 (ola retenida)

- **Cifra que parametriza (no la que arbitra):** IMOR ajustado **~20%** (4T2024). Fuente: HR Ratings, *"Financiera Independencia"* (2024), `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md:31` y `:94`.
- **Cifra que arbitra:** IMOR ajustado de la cartera total de Findep al **4T2026** — no existe todavía al congelar este marco (`marco-candidatas-piloto-v1_0.tsv` línea 61: "OLA RETENIDA... el árbitro es estrictamente futuro, simétrica para L y para M").
- **Fuente de la banda:** **redondeo de la publicación** de la cifra que parametriza, único insumo hoy disponible del mismo reporte y la misma metodología que producirá la cifra de 4T2026 (mismo emisor, HR Ratings, mismo método de IMOR ajustado). La cifra de 4T2024 se publica **sin decimal** (`~20%`, no `20.x%`) — un nivel de redondeo más grueso que `DOC-01`/`DOC-02`/`DOC-03`, consistente con que el propio corpus la marca con `~` (aproximación explícita de la fuente, a diferencia de `10.7%`/`15.7%` que se citan sin tilde en la tabla de fuentes §C, línea `:94`, aunque sí la llevan en la tabla principal `:31`).
- **Ancho:** `±0.5 pp` (medio último-dígito publicado, redondeo a la unidad porcentual en vez de al decimal).
- **Banda pre-registrada (aplicada a la cifra de 4T2026 cuando exista, misma regla de redondeo del emisor):** `nivel_4T2026 ± 0.5 pp`, sin fijar hoy el nivel — este acto no calcula, ni puede calcular, un estimado puntual de una cifra que todavía no se publica; solo fija el **ancho** que regirá cuando el árbitro corra sobre la cifra real de 4T2026, bajo el supuesto declarado de que HR Ratings seguirá redondeando IMOR ajustado a la unidad porcentual (mismo patrón que sus dos reportes ya citados en este documento, `DOC-01` y `DOC-02`, que si acaso redondean más fino, a un decimal — este acto usa el redondeo más grueso, `±0.5 pp`, observado específicamente en el reporte de Findep, no el de otro emisor).
- **Por qué ese ancho:** el `ancho de redondeo se deriva de la fuente que efectivamente reportará la cifra de 4T2026` (misma casa calificadora, mismo indicador, mismo emisor), no de una fuente distinta. La ventana temporal (parametriza 4T2024, arbitra 4T2026, dos años de diferencia) es la fuente de error que `FP-83` también autoriza como admisible, pero este acto **no** la traduce en un ensanchamiento numérico adicional — hacerlo exigiría un supuesto de deriva temporal del indicador que no está en ninguna fuente citada, y sería exactamente el tipo de invención que este acto tiene prohibido. La ventana queda declarada como contexto, no como ancho.

---

## Resumen de las seis bandas

| id | cifra | fuente del ancho | ancho | banda |
|---|---|---|---|---|
| `DOC-01` | IMOR ajustado Azteca ~10.7% (2025) | redondeo publicación (1 decimal) | `±0.05 pp` | `[10.65%, 10.75%]` |
| `DOC-02` | IMOR ajustado BanCoppel 15.7% (3T24) | redondeo publicación (1 decimal) | `±0.05 pp` | `[15.65%, 15.75%]` |
| `DOC-03` | razón Azteca/tarjeta banca múltiple 10.7/13.7 (jun25) | redondeo publicación, propagado (razón) | `±0.0065` | `[0.7745, 0.7875]` |
| `DOC-04` | inventario >1 año FirstCash 1%–2% (2024-25) | rango publicado directamente | `±0.5 pp` | `[1.0%, 2.0%]` |
| `DOC-05` | castigos/cartera Compartamos (4T25) | redondeo publicación (numerador); **denominador NO localizado** | `±0.5 M` (solo numerador) | **incompleta — declarada así** |
| `DOC-06` | IMOR ajustado Findep, ola 4T2026 (futura) | redondeo publicación del emisor (unidad porcentual) | `±0.5 pp` | `nivel_4T2026 ± 0.5 pp` |

**Ningún ancho de esta tabla se deriva de una cuarta fuente de error distinta de las tres que `ADR-135(e)`/`FP-83` autoriza (revisión, redondeo de publicación, ventana temporal). `DOC-05` queda con banda incompleta por diseño, declarada como tal, no rellenada con un supuesto sin fuente. `DOC-06` fija el ancho de redondeo del emisor sin fijar el nivel, que no existe todavía.**

**Cierre: el primer resultado que produzca el árbitro contra estas bandas es el que se reporta.**
