# S4 · Pre-registro de `civico.voto.clientelar_si_observable` — reformulada (objeto de `N5 §2.6`)

### `prereg-caja-S4-L4` · **v1.0** · 4 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S4-L4-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S4-L4`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`, de una pieza **NUEVA** de falsación de `civico.voto.clientelar_si_observable` sobre LAPOP México 2019 (exposición a oferta clientelar × voto declarado), más la declaración explícita de por qué la tercera dimensión que el encargo pide —observabilidad percibida del voto— **no es construible en la misma ola** y de qué mide ya, para esa misma regla, el pre-registro `MAESTRA35-L9`/`L11` que sí la trae. |
> | **QUÉ NO ES** | No abre ningún `.dta`, `.sav` ni codebook — los cuatro payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve el tier de `civico.voto.clientelar_si_observable` (hoy `[MEDIA]`, `canon/modelo-decision-v4_0.md:554`) ni el de su gemela `civico.voto.agencia_con_secreto` (fila histórica `[FUERTE]`, línea 552; tier motor-consumido ya en `[MEDIA]` por la Enmienda `D2-f`, 3/sep/2026 — ver §0.3). `FP-298` ya está `EJECUTADA` (4/sep, `ACTO MAESTRA38-N6`) — esta pieza no la reabre ni la revisa. |
> | **VERIFICAS ASÍ** | Caja, al abrir `Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta`, compara el ponderador real contra §2; compara `clien1n`/`clien1na`/`vb3n`/`vb10` contra el texto de §1; compara la cifra `n=1580`/`clien1na` válidos `1578`, «sí» `271` (guardia heredada de `L9 §0.5`, ya verificada por una corrida real) contra el marginal que obtenga. |

**Acto:** `ACTO MAESTRA38-N7 · PRE-REGISTRO-CIVICO-LAPOP`, 4/sep/2026, entorno **NUBE**, sobre `origin/main = a0e06da4ece2f307c46b895fb0da226d30b9cc29` (main avanzó 2 commits hasta `2b9c90e` al escribir esta pieza — un `[TRAMITE] digesto 2026-09-04` que no toca `forense/prereg-caja/`, `data/INFRAESTRUCTURA-v1_0.md`, `forense/tablero/` ni `forense/firmas-pendientes.tsv`; no es PARO, declarado por A.8/D-13, no heredado del encargo).

---

## 0 · Ficha bajo prueba y continuidad con `L9`/`L11` — la corrección de premisa de este acto

### 0.1 · Definición vigente

`canon/modelo-decision-v4_0.md:554` (§3.7 Cívico y participación), verbatim:

> *SI hay **proximidad/focalización del reparto** O el votante **percibe que su voto puede ser monitoreado** ENTONCES **la autonomía CEDE localmente** — PORQUE cálculo racional bajo incertidumbre sobre el secreto del voto — `[MEDIA]` **(a)**.* · **id:** `civico.voto.clientelar_si_observable`

Su gemela de disyunción contraria, `canon/modelo-decision-v4_0.md:552`, id `civico.voto.agencia_con_secreto` (`[FUERTE]`), es la que afirma la autonomía **sin** proximidad ni monitoreo. `N5 §2.5` clasificó a esta última `(b) SIN-INSTRUMENTO` — no hay en el corpus un ítem de percepción de monitoreo del voto por sí solo — y señaló que "el mismo instrumento que resuelva el ítem de percepción de monitoreo sirve a las dos reglas a la vez". Esta pieza hereda esa observación en §0.3.

### 0.2 · Objeto reformulado, verbatim de `N5 §2.6`

> **Objeto reformulado:** entre quienes reportan haber sido blanco (o conocer a alguien blanco) de una oferta de beneficio por su voto (`clien1n`/`clien1na` = sí), medir si la elección de voto declarada (`vb3n`, misma ola) difiere de quienes no reportan blanco.

Es la misma reformulación que `forense/notas/2026-09-04-MAESTRA38-N5-diseno-9-reglas.md:210-214` congeló, clasificada `(a) REFORMULABLE` en su tabla `§3` fila `#6`, y aceptada por la `FIRMA` de este encargo ("la de N6 + §2 (#6 y #8 aceptadas como REFORMULABLE)").

### 0.3 · Corrección de premisa, obligatoria por A.8/D-13 — esta regla ya tiene dato, dos veces

**Lo que ni el encargo ni `N5` citan, y que existe en el árbol desde el 2/sep/2026** (verificado con `git log`, ambos commits anteriores a `N5` y a este encargo): `forense/notas/2026-09-02-MAESTRA35-L9-spec.md §3` y su `resultados.md §3` ya pre-registraron y **corrieron** una falsación directa de este mismo `id`, con el par `R7.3`/`R7.6` (`modelo-decision-v4_0.md:552,554` = líneas `:553`/`:554` citadas por `L9`), y `forense/notas/2026-09-02-MAESTRA35-L11-resultados.md §1` la **replicó** en un instrumento distinto:

| pieza | instrumento | antecedente | moderador (brazo de observabilidad) | desenlace | veredicto `B-bis` |
|---|---|---|---|---|---|
| `L9 §3` | LAPOP México **2023** | `mexwf1_19` (recibió ayuda del gobierno) | `countfair3` — percepción de voto secreto, dicotomizado `SECRETO`/`OBSERVABLE` | `vb20` (votaría por el partido del oficialismo) | **`CONTRARIA`** — `Δ_SECRETO` **+14.37 pp** `[+1.43,+27.44]`, `Δ_OBSERVABLE` **+17.98 pp** `[+10.75,+25.02]`, las dos excluyen 0 y van al mismo signo |
| `L11 §1` | ENCUCI 2020 | `AP6_10` (beneficiario de programa) | `AP7_15`, mismo dicotomizado | proxy de apoyo al oficialismo | **`CONTRARIA`** (replicada) — `Δ_SECRETO` **+6.38 pp** `[+3.82,+8.89]`, `Δ_OBSERVABLE` **+11.57 pp** `[+6.57,+16.59]` |

**Corrección post-merge (`PR #536`, tras `origin/main` = `7c04069`, `PR #535`/`ACTO MAESTRA38-N6`).** El primer sello de esta pieza citaba las dos corridas como `PENDIENTE-DE-MESA` en `FP-298` `ABIERTA` y "ningún sello de canon se ha movido todavía" — las dos afirmaciones estaban desactualizadas, y una de las dos ya lo estaba **antes** de escribirse: `canon/modelo-decision-v4_0.md §7`, **Enmienda `D2-f`** (firma de mesa **3/sep/2026**, propagada por `ACTO MAESTRA37-N8 · CONSOLIDA-DECISIONES`, un día **antes** del `SHA` de redacción `a0e06da4` de este encargo) ya declaraba, formalmente: *"`R7.3` pasa de `[FUERTE]` a `[MEDIA]` en el cálculo... Motivo: `CONTRARIA-REPLICADA` en dos instrumentos independientes... LAPOP 2023 (`civico.voto.agencia_con_secreto`) y ENCUCI 2020 (`civico.voto.agencia_con_secreto_encuci2020`)"* — exactamente las dos corridas de la tabla de arriba, con el mismo par de cifras. `FP-298` pasó además a `EJECUTADA` el 4/sep (`ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3`, `PR #535`), cargando `civico.voto.clientelar_si_observable_lapop2019` — **el mismo diseño que este documento pre-registra** — como tercera formulación complementaria en `milpa/tramite-ola5-propuesta-v0.yaml`, `situacion`/`tier` `PENDIENTE-DE-MESA` (diseño aceptado, falsador sin correr), sin reabrir `D2-f`. **Lo que sí sigue siendo cierto, re-verificado:** `D2-f` mueve el tier **motor-consumido** de `civico.voto.agencia_con_secreto` (`R7.3`, la gemela de esta regla en la disyunción), no el de `civico.voto.clientelar_si_observable` — la fila histórica de `modelo-decision-v4_0.md:554` **no se edita** por `D2-f` (mismo criterio declarado ahí: "el tier que el motor consume queda declarado aparte") y sigue en `[MEDIA]`. Esta pieza mide directamente el `id` de la línea 554, no su gemela — la corrección de arriba fortalece el argumento de §0.4 (dos brazos, dos instrumentos, mismo hallazgo) en vez de contradecirlo.

**Consecuencia para este pre-registro, declarada antes de escribir una celda:** este acto **no es la primera medición** de `civico.voto.clientelar_si_observable`. Es una **segunda pieza, deliberadamente independiente**, que ataca el **otro brazo** de la disyunción del `SI`:

- `L9`/`L11` miden el brazo **"el votante percibe que su voto puede ser monitoreado"** — antecedente = recibir una transferencia gubernamental, moderador = percepción de secreto del voto, sobre las olas 2023/ENCUCI 2020.
- Esta pieza (§1-§5) mide el brazo **"proximidad/focalización del reparto"** — antecedente = haber sido blanco directo de una oferta clientelar (`clien1n`/`clien1na`), sin moderador de observabilidad (§0.4), sobre la ola 2019 — la única que trae la batería `clien*`.

Los dos brazos comparten conjunción por «O» en el `SI`, así que **un resultado limpio en cualquiera de los dos ya mueve la regla** (§4) — no hace falta que los dos brazos midan a la vez para que el `id` se falsee o se corrobore. Esta pieza es un **segundo intento de falsación, no una repetición** de `L9`/`L11`.

### 0.4 · Por qué la celda de tres factores que pide el encargo no es construible en una sola ola, declarado y no forzado

El encargo (`SPEC`, S4) pide celdas de **recepción de oferta clientelar × observabilidad percibida × voto declarado**. Búsqueda contra `data/inventario-reactivos-descargas-mx-v1_1.tsv` (42 536 filas), verificada en esta sesión:

- La batería de oferta clientelar (`clien1n`/`clien1na`/`clien4a`/`clien4b`) existe **únicamente** en `Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` — 0 apariciones en 2021/2023/2006.
- El ítem de observabilidad percibida del voto (`countfair3`, "Percepción de una votación secreta") existe **únicamente** en `MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta`/`.sav` — 0 apariciones en 2019. La búsqueda sobre las 221 filas que el inventario trae del `.dta` 2019 no encuentra ningún ítem de secreto/observabilidad/monitoreo del voto — los tres candidatos con la palabra "observación" en 2019 (`smedia3`/`smedia6`/`smedia9`) miden exposición a redes sociales, no secreto del voto.

**No existe una sola ola LAPOP en el corpus que traiga oferta clientelar y observabilidad percibida sobre la misma persona.** Forzar una celda de tres factores exigiría suponer que las dos olas son intercambiables persona a persona, que no lo son (paneles independientes, muestras distintas, cinco años de diferencia). Esta pieza **no fuerza** esa celda: pre-registra el brazo que **sí** es medible en una ola (§1-§4) y remite el brazo de observabilidad al pre-registro que ya lo cubre (`L9 §3`, §0.3 arriba) — la comparación de los dos es de **signo entre piezas**, no de una celda conjunta, y así se declara en §4.3.

---

## 1 · Variables — texto de reactivo copiado del inventario, no parafraseado

Fuente: `data/inventario-reactivos-descargas-mx-v1_1.tsv`, payload `Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` (`sha256_12` del inventario: `c88f79ebb8e7`; sha256 completo del manifiesto en §6).

| variable | etiqueta (verbatim del inventario) |
|---|---|
| `clien1n` | «A un conocido le ofrecieron beneficio por su voto (última elección nacional)» |
| `clien1na` | «Le ofrecieron un beneficio por su voto en la última elección generales» |
| `clien4a` | «De acuerdo con dar beneficios por los votos» |
| `clien4b` | «De acuerdo con dar beneficios por los votos» |
| `vb3n` | «Decisión sobre el voto para presidente» |
| `vb10` | «Simpatiza con algún partido político» |
| `wt` | «Peso del país» |

`clien4a`/`clien4b` no entran al diseño de §3 (miden acuerdo normativo con la práctica clientelar, no exposición ni voto) — se listan porque el encargo pide "variables" en plural para el objeto de `N5 §2.6`, que las cita como parte de la batería `clien*`; quedan como **candidatas de robustez**, no como parte del estimando principal.

---

## 2 · Universo y ponderador

**Universo pre-registrado:** personas de 18+ encuestadas en LAPOP AmericasBarometer México 2019 con código válido (`∈{1,2}`) en `clien1n` **o** en `clien1na`, y con `vb3n` no vacío/no `NS/NR`. País completo (no hay estrato geográfico adicional pre-registrado aquí).

**Guardia de lectura, heredada de una corrida real ya verificada (`L9 §0.5`, no re-derivada aquí porque `L9` sí abrió el `.dta`):** `n` total de la ola = **1 580**; `clien1na` válidos = **1 578**, «sí» = **271**. Si la corrida de caja no reproduce estos marginales, **PARA** — el `.dta` no es la misma versión que `L9` leyó.

**Ponderador — declarado por nombre, con la incertidumbre de `N3` sobre el codebook:** el inventario etiqueta `wt` como «Peso del país» en este payload. `L9 §1.2` (corrida real, no declaración de segunda mano) verificó que en LAPOP México 2019 **`wt` es constante = 1** — la proporción ponderada es idéntica a la simple, y todo el efecto de diseño vive en el conglomerado (`estratopri`, `upm`). Esta pieza **hereda esa verificación** (D-13: es dato de una corrida real, no prosa) pero, siguiendo la reserva de `S2-L2-spec-v1_0.md §1.0`, deja escrito que **nadie ha abierto el codebook de 2019** (`mexico_lapop_americasbarometer_2019_codebook_v1_0_w`, §6) para confirmar por texto que no existe un segundo campo de ponderación post-estratificación distinto de `wt` — si caja lo encuentra, ese campo manda sobre `wt`, declarado y no descubierto después.

**Estrato/UPM, mismo diseño que `L9` ya usó para esta ola:** `estratopri` (4 estratos) · `upm` (129 conglomerados).

---

## 3 · Dicotomizaciones y celdas

**Tratamiento — exposición a oferta clientelar:** `EXPUESTO = 1` si `clien1n = 1` **o** `clien1na = 1` (blanco directo o blanco por conocido); `EXPUESTO = 0` si las dos son `2` (no). Códigos `8`/`9` (NS/NR) excluidos de la construcción del indicador, declarado — no se imputan.

**Desenlace — elección de voto 2018, mismo código que `L9 §2` ya fijó para esta ola (continuidad de diseño, no reinvención):** `vb3n = 103` (**PRI**, desenlace **principal** — el partido con la maquinaria clientelar clásica y el gobierno federal saliente en 2018) · `vb3n = 101` (**MORENA**, desenlace **secundario**, el ganador). Los dos se congelan ahora.

**Control:** `vb10` (identificación partidista previa) — mismo control que `se_mueve_si` de `N5 §2.6` pide. Se reporta como covariable de estratificación (`vb10` con partido/sin partido); sus categorías finas de partido quedan pendientes del codebook (§6), no inventadas aquí.

**Celdas — un solo eje 2×2, más el control:**

| | `EXPUESTO=1` | `EXPUESTO=0` |
|---|---|---|
| **votó PRI** (`vb3n=103`) | celda 1 | celda 2 |
| **votó MORENA** (`vb3n=101`) | celda 3 | celda 4 |

Cuatro celdas para el estimando principal; el control `vb10` las subdivide una vez más (con partido/sin partido) sólo como robustez declarada, no como veredicto adicional — mismo criterio que `L9 §1.4` fija para ejes sin signo pre-registrado.

**Cota de n mínima por celda — heredada de la guardia de la casa (`L9 §1.3`), no reinventada:** una celda con **numerador < 10** se reporta `NO-ESTIMABLE`, con su `n`, y no participa del veredicto.

---

## 4 · Falsador `B-bis`

**Estimando:**

```
Δ_elección = P(vb3n=103 | EXPUESTO=1) − P(vb3n=103 | EXPUESTO=0)
```

con el mismo cálculo repetido para `vb3n=101` como desenlace secundario, congelado a la vez (mismo criterio que `L9 §2` usó para no dejar que la elección de desenlace dependa del resultado).

### 4.1 · Qué signo sostiene la regla y qué signo la refuta

| | |
|---|---|
| **Signo esperado** | `Δ_elección (PRI) > 0` — el brazo de proximidad/focalización del reparto predice que quien fue blanco de una oferta clientelar vota más por el partido asociado a esa maquinaria que quien no fue blanco |
| **`CORROBORADA`** | `Δ_elección (PRI) > 0` con IC95 que **excluye** 0 |
| **`CONTRARIA`** | `Δ_elección (PRI) < 0` con IC95 que excluye 0 — quien fue blanco vota **menos** PRI, contra lo que el `SI…ENTONCES` predice para este brazo |
| **`NO-DISCRIMINA`** | el IC95 de `Δ_elección (PRI)` contiene 0 |
| **Precedencia** | si `Δ_elección (PRI)` y `Δ_elección (MORENA)` discrepan en signo y ambos limpios, manda el veredicto de **PRI** (desenlace principal, por ser el partido con la maquinaria clientelar activa en 2018) y se reporta el par completo, mismo criterio de precedencia que `L9 §2.1`/`§3.1` fija para pares de estimandos |

### 4.2 · Las dos filas que `B-bis` exige — qué pasa si no refuta

- **Si el falsador NO refuta** (`NO-DISCRIMINA`, o `CORROBORADA` con IC ancho): el brazo de proximidad/focalización **no queda descartado** por este diseño — la `n` de la rama expuesta es chica (`clien1na` «sí» = 271 sobre 1 578, y `EXPUESTO` combinando `clien1n`/`clien1na` puede ser algo mayor pero sigue siendo minoría) y el instrumento no observa quién dio la oferta ni si el votante creyó que su voto podía verificarse — misma limitación que `L9 §2` declaró para la pieza de dádiva/turnout. El `id` **sigue `[MEDIA]`**, sin evidencia nueva que la mueva en ningún sentido, y el brazo de observabilidad (`L9`/`L11`, §0.3) sigue siendo la evidencia más fuerte disponible sobre este `id` — **`CONTRARIA`**, dos veces replicada.
- **Si el falsador SÍ refuta** (`CONTRARIA`, `Δ_elección(PRI)` limpio y negativo): se suma una **tercera** pieza `CONTRARIA` sobre el mismo `id`, ahora en los dos brazos de la disyunción y en tres instrumentos distintos (LAPOP 2019, LAPOP 2023, ENCUCI 2020) — la combinación que `se_mueve_si` (§5) describe.

### 4.3 · Cómo se lee junto con `L9`/`L11` — sin fabricar una celda conjunta

Por §0.4, esta pieza **no computa** una celda de tres factores. Lo que caja reporta, además del veredicto de §4.1, es la **comparación de signo** entre esta pieza (brazo proximidad/focalización, 2019) y `L9 §3`/`L11 §1` (brazo observabilidad, 2023/ENCUCI): si los dos brazos dan `CONTRARIA` en el mismo sentido (el antecedente clientelar se asocia con votar **menos** por el partido/oficialismo asociado), la lectura de mesa es que **ningún** brazo de la disyunción sostiene la cesión de autonomía que `[MEDIA]` predice, sobre tres instrumentos. Si dan en sentidos distintos, la lectura es que los dos mecanismos (proximidad vs. observabilidad) se comportan distinto y el `id` necesita partirse — decisión de mesa, no de este pre-registro.

---

## 5 · `se_mueve_si`

Si entre `clien1n`/`clien1na`=sí la proporción que vota PRI **no es mayor** que entre `clien1n`/`clien1na`=no (controlando `vb10`), este brazo de la cesión de autonomía local **no se sostiene** con este proxy — el falsador queda planteado, no corrido (medición: cero, es diseño), y se lee junto con el veredicto ya `CONTRARIA` (×2) de `L9`/`L11` sobre el otro brazo, per §4.3.

---

## 6 · Archivos que la caja necesita abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `mexico_lapop_americasbarometer_2019_v1_0_w` | `Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` | `c88f79ebb8e73c473cd78d894eb093261f172e736a35bd7bc677b4e8b1454a57` |
| `mexico_lapop_americasbarometer_2019_codebook_v1_0_w` | `Descargas Manuales/Mexico LAPOP AmericasBarometer 2019_Codebook_v1.0_W.pdf` | `4efa5809c3fde487516a60acf782f013444889a775bf368745c8da577cba75ce` |
| `mexico_americasbarometer_2018_19_technical_report_w_100919` | `Descargas Manuales/Mexico_AmericasBarometer_2018-19_Technical_Report_W_100919.pdf` | `35aa8f4b2f2a2aae613ae6e4b7e0ee47278bfc33869568e84f708da9affb544f` |
| `abmex18_v12_0_2_5_spa_190207_w` | `Descargas Manuales/ABMex18-v12.0.2.5-Spa-190207_W.pdf` (cuestionario 2018/19) | `6319cfebeda635563cec7d70573430413e608e3366acf00fa35b61cc41362f5c` |

Los cuatro están `raiz: descargas_mx` en `data/manifiesto.yaml` — ausentes de esta sesión NUBE (sin corpus montado), ninguno abierto en ningún acto documentado salvo el `.dta` mismo, que `L9` sí abrió para la corrida de §0.3/§2.

---

## 7 · Qué NO hace este acto

No abre ningún archivo de §6. No calcula `Δ_elección` ni ningún IC95. No mueve el tier de `civico.voto.clientelar_si_observable` ni el de `civico.voto.agencia_con_secreto`. `FP-298` ya está `EJECUTADA` — esta pieza no la reabre. No reabre ni corrige los veredictos `CONTRARIA-REPLICADA` de `L9`/`L11`/`D2-f` — los cita como lo que son, evidencia ya corrida y ya sellada sobre el `id` gemelo.

**Medición: caja, acto `MAESTRA38-L4`.**

**El primer resultado que produzca este procedimiento es el que se reporta.**
