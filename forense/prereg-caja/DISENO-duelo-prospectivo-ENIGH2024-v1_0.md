# DISEÑO · Duelo prospectivo ENIGH 2024 · v1.0 — PARA FIRMA DE MESA

> **Estado: PROPUESTA, NO CONGELADA.** Este documento no es un COMMIT-1. No congela
> spec, no abre dato, no adopta nada. Lo entrega `ACTO GEN2-ENIGH2024-RESERVA-Y-DISENO-1`
> (encargo `forense/encargos/2026-09-21-GEN2-ENIGH2024-RESERVA-Y-DISENO-1.md`, sello de
> cuerpo `e165564d6a03e743`) y espera firma en
> `forense/firmas-pendientes.tsv:FP-260921-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-b7ae-02`.
> Molde: la firma **F7** del duelo prospectivo ENVIPE 2026
> (`FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-07`), citada porque
> `DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md` **NO-ENCONTRADO** en
> `forense/prereg-caja/` al redactar (universo: 56 archivos del directorio, `ls`,
> 21/sep/2026) — el encargo previó las dos ramas y ésta es la que aplicó.
>
> **ADOPTADO 22/sep/2026** por `ACTO GEN2-ENIGH2024-DUELO-COMMIT-2-3`
> (encargo `forense/encargos/2026-09-22-GEN2-ENIGH2024-DUELO-COMMIT-2-3.md` §2,
> verbatim: «Se adopta el diseño ... con el alcance que `#988` midió»), resolviendo
> `forense/firmas-pendientes.tsv:FP-260921-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-b7ae-02`
> (ahora `FIRMADA`). Única edición de este acto al documento (A.10): el resto de
> abajo permanece verbatim, incluida la palabra «PROPUESTA» del título, que
> queda histórica.

---

## 1 · Primera línea — universo, unidad, escala

> **Estimando:** proporción de **hogares** con ingreso por **remesas > 0** en el trimestre
> normalizado de referencia.
> **Universo:** hogares del universo completo de `concentradohogar`, **sin filtro adicional**.
> **Unidad:** hogar (nunca persona). **Ponderador:** `factor` de hogar, sin normalizar.
> **Escala:** proporción en `[0,1]`. **Todo contendiente compite en escala logit**
> (§4); el error se lee de vuelta en puntos de proporción, y se dice en cuál de las dos
> está cada cifra (§5 de instrucciones, módulo de auditoría v2.4).

Una sola celda, nacional, por ola. No hay marginales por eje ni cruces en este duelo —
§3 dice por qué, y no es una omisión: es el hallazgo.

---

## 2 · P1 · Inventario — qué estimandos de ENIGH tienen serie sellada en GEN2

**Regla de entrada del duelo (verbatim del encargo §5 P1):** `R` sellado en **≥ 3 olas con
universo idéntico**.

Universo del censo, declarado (A.4/A.13): las **16 filas** de `forense/replay-evidencia.tsv`
(151 filas en total) cuyo `calc_id` o cuyos inputs citan ENIGH, leídas contra el
`spec.yaml` y el `resultados.json` de cada corrida en `data/corrida0/`.

### 2.1 · Lo que SÍ pasa la regla de entrada — un solo estimando

**`remesas > 0`, proporción de hogares.** Mismo estimando, mismo universo textual, mismo
ponderador, en **cinco olas selladas**, repartidas en dos CALC que se solapan en dos olas:

| ola | P | IC95 | n | hogares expandidos | CALC que la sella | `RESULT` |
|---|---|---|---|---|---|---|
| 2014 | 0.040784 | [0.036629, 0.045136] | 19 479 | 31 671 002 | `CALC-B-MARCO-ENIGH-0001` | `SERIE-REPORTADA` |
| 2016 | 0.047459 | [0.045098, 0.049759] | 70 311 | 32 974 661 | `CALC-B-MARCO-ENIGH-0001` **y** `CALC-B-0001` | `SERIE-REPORTADA` |
| 2018 | 0.047285 | [0.045102, 0.049450] | 74 647 | 34 400 515 | `CALC-B-0001` | `SERIE-REPORTADA` |
| 2020 | 0.043775 | [0.041895, 0.045773] | 89 006 | 35 749 659 | `CALC-B-0001` | `SERIE-REPORTADA` |
| 2022 | 0.045694 | [0.043773, 0.047770] | 90 102 | 37 560 123 | `CALC-B-0001` **y** `CALC-ENIGH-0001` | `SERIE-REPORTADA` / `REPLICA-RESULTADO` |

**Los dos solapes son la validación independiente de la serie, y salen limpios:**
2016 coincide **dígito a dígito** entre `CALC-B-MARCO-ENIGH-0001` y `CALC-B-0001`
(0.04745859252351374 en ambos, mismo IC, mismo `n`, mismos expandidos); 2022 coincide entre
`CALC-B-0001` y `CALC-ENIGH-0001` con
`RESULT-ENIGH-A-DELTA-VS-B0001 = 0.0` exacto y `RESULT-ENIGH-A-REPLICA-B0001 = REPLICA-RESULTADO`
(el IC difiere en `-1.15e-05` porque `CALC-ENIGH-0001` usa `IC-DE-DISENO` y `CALC-B-0001`
bootstrap de UPM dentro de estrato — es **otro método de IC sobre el mismo punto**, no otra
medición, y el duelo lo declara en §4.4).
Replay: las tres corridas están en `forense/replay-evidencia.tsv` (líneas 29, 86, 104);
`CALC-B-MARCO-ENIGH-0001` y `CALC-ENIGH-0001` como `REPRODUCE · IDENTICO`, `CALC-B-0001`
como `REPLICA-RESULTADO · CONTEXTO-DISTINTO`.

### 2.2 · Lo que NO pasa la regla de entrada, y qué haría falta

| estimando | qué mide | unidad · ponderador | olas selladas | por qué no entra | qué acto lo arregla |
|---|---|---|---|---|---|
| `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0001/0002/0003` | composición estructural descriptiva de personas | **persona** · `poblacion.factor` | **1** (2022) | una sola ola | acto de caja que corra el mismo medidor sobre 2016, 2018 y 2020 — **no gasta nada: son olas ya abiertas** |
| `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001` | cinco descriptores de intensidad entre receptores (monto, participación) | hogar · `factor` · **pesos de 2022 por trimestre** | **1** (2022) | una sola ola **y** escala monetaria sin deflactor declarado | acto de caja de ≥3 olas **más** una decisión de mesa sobre deflactor (§7) |
| `CALC-ENIGH2022-REMESAS-CONTEXTO-0001` | incidencia + monto condicional por `est_socio` y `tam_loc` | hogar · `factor` | **1** (2022) | una sola ola | acto de caja de ≥3 olas; es el **único candidato a cruces** que existe (§3) |

**Ningún otro CALC del repo lee ENIGH.** `CALC-R-FAM-M-05/06/07` (y sus `-v2`/`-v3`)
aparecen en el censo por mencionar ENIGH como marco de la celda `FAM-M-05`, no por leer una
ola: su input es el marco-M, no un microdato de ENIGH.

### 2.3 · El corte de serie de 2016 — 2014 queda FUERA, y se dice

El encargo lo anticipa («ENIGH cambió de serie en 2016 “nueva serie”: dilo donde toque»), y
el dato sellado lo confirma sin ambigüedad: `RESULT-BM-ENIGH-2014-METADATO-VERSION` =
`identifier=MEX-INEGI.40.202.03-ENIGH-2014-NCV`, con **n = 19 479** contra **n = 70 311** en
2016 — un salto de ×3.6 en muestra que no es crecimiento poblacional sino otro diseño.

**Decisión del diseño:** la ventana del duelo es **2016 · 2018 · 2020 · 2022**, cuatro olas
de la nueva serie. 2014 **no se borra ni se refuta**: queda `VENCIDO EN ALCANCE` (A.10) para
esta prueba, y su fila sigue sellada como lo que es, historia de la serie anterior.
Cuatro olas siguen cumpliendo la regla de entrada (≥3) con margen de una.

**Consecuencia que mesa debe ver antes de firmar:** con la ventana 2016–2022, la tendencia de
serie completa se ajusta sobre **cuatro puntos**. Es poco, y el diseño no finge otra cosa —
§6 declara qué se puede y qué no se puede concluir con cuatro puntos.

---

## 3 · Por qué este duelo es SOLO NACIONAL — el hallazgo que cambia la forma

El molde de ENVIPE 2026 (firma F7, enmienda **B**) mete a nivel cruce «la misma familia del
lote ENIF —C2, persistencia, interacción cruda, interacción encogida, ajuste proporcional—
**sobre los dos pares cuyo cruce de 2025 ya está abierto**». La condición es *historia
abierta del cruce*, no *existencia del eje*.

**En ENIGH esa condición no se cumple para ningún par.** El único CALC de ENIGH que corta por
ejes es `CALC-ENIGH2022-REMESAS-CONTEXTO-0001` (`est_socio` 4 categorías × `tam_loc` 4
categorías), y está sellado en **una sola ola, 2022**. Un contendiente de cruces necesita
historia para encogerse contra ella; con un solo punto, «interacción encogida» no tiene hacia
dónde encogerse y «persistencia» no tiene de dónde persistir.

Por eso este diseño **declara el nivel cruce fuera de alcance y no lo simula**. Es la
diferencia entre «el retador perdió» y «nadie corrió el mecanismo contra esta fuente» (§2 de
instrucciones, tercer hallazgo que nunca se colapsa): aquí es lo segundo, y la fila queda
**no ocupada**, que por la regla de salida de θ (`FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-06`,
verbatim: «una fila no ocupada es "nadie corrió el mecanismo", no una derrota») **no cuenta
como derrota de la interacción**.

**Sucesor nombrado, y barato:** un acto de caja que corra
`CALC-ENIGH2022-REMESAS-CONTEXTO-0001` —el medidor ya sellado, sin cambiarlo— sobre 2016,
2018 y 2020, que son olas **ya abiertas**: no consume ninguna reserva y no cuesta una
decisión de mesa. Si ese acto cierra antes del COMMIT-1, el duelo de ENIGH 2024 **gana su
nivel de cruce** y esta sección se enmienda por escrito, no se reescribe.

---

## 4 · Contendientes mecánicos — declarados todos juntos, aquí y ahora

Lección ya firmada que este diseño obedece (F7 y lote ENIF v0.3): **todas las variantes de
tendencia entran juntas**, no se escogen después de ver el dato.

### 4.1 · La escala

Todo contendiente predice en **logit** y se devuelve a proporción para reportar:
`logit(p) = ln(p/(1-p))`. Motivo declarado antes de ver el dato: el estimando vive cerca de
0.045, donde una tendencia lineal en proporción puede cruzar cero en pocas olas y una en logit
no. **Es la escala del estimando, no del monto**: si un acto futuro trae a este duelo un
estimando de monto (§2.2), ése va en **log**, y no se compara contra éste sin función de
enlace (§4.3 de instrucciones).

### 4.2 · Los cinco contendientes, con su fuente exacta

| # | contendiente | qué usa | predicción para 2024 |
|---|---|---|---|
| **C-PISO** | **persistencia** (el piso) | `P(2022)` | `p̂ = P(2022)` |
| **C-T2** | tendencia de 2 | `P(2020), P(2022)` | extrapolación lineal en logit de los dos últimos |
| **C-T3** | tendencia de 3 | `P(2018), P(2020), P(2022)` | MCO en logit sobre tres puntos, extrapolado a 2024 |
| **C-TS** | tendencia de serie completa | `P(2016..2022)` | MCO en logit sobre los cuatro puntos de la nueva serie |
| **C-MEDIA** | media de la serie | `P(2016..2022)` | media en logit de las cuatro olas |

`C-MEDIA` no está en el molde de ENVIPE; se añade y se declara por qué: con cuatro puntos y
una serie que sube, baja y vuelve a subir (0.0475 → 0.0473 → 0.0438 → 0.0457), «la media» es
el contendiente nulo honesto, y si ninguna tendencia le gana, el resultado del duelo es
«la serie no tiene tendencia legible», que es un resultado, no un empate.

**C-PISO es el piso y se adopta salvo veto de mesa** (§4.6 de instrucciones, firma
17/sep/2026). Los otros cuatro son **retadores**: su único trabajo es acotar al piso.

### 4.3 · Lo que NO entra

- **Sin cruces** (§3). Sin marginales por eje: ninguno tiene serie.
- **Sin `C2`, sin interacción cruda, sin interacción encogida, sin ajuste proporcional**: son
  contendientes de cruce y no hay cruce. No se declaran «perdedores»: se declaran
  **no corridos**, y por la regla de salida de θ eso no cuenta contra la interacción.
- **Sin marginales públicos de la misma ola** como piso alternativo: leerlos sería leer los
  tabulados de 2024, que es exactamente lo que la reserva prohíbe.

### 4.4 · Una discordancia de método que el COMMIT-1 debe resolver ANTES de abrir dato

`CALC-B-0001` produce IC por **bootstrap de UPM dentro de estrato**; `CALC-ENIGH-0001`, por
**IC de diseño**. Sobre el mismo punto de 2022 difieren en `1.15e-05` — despreciable para el
punto, **no necesariamente para la regla de adjudicación**, que compara el error contra el
ancho del IC. El COMMIT-1 **declara cuál de los dos métodos usa para 2024 y lo usa para las
cuatro olas de la ventana**, o la comparación mezcla escalas de incertidumbre. Recomendación
del ejecutor: **bootstrap de UPM dentro de estrato**, porque es el que cubre las cuatro olas
de la ventana (`IC-DE-DISENO` solo existe para 2022).

---

## 5 · Regla de adjudicación, por nivel

**Nivel nacional — el único que este duelo ocupa.**

Lección ya firmada (F7, enmienda **A**): *a nivel nacional hay una o dos celdas por ola, y
el punto nuevo no adjudica solo*. Se lee con **dos cosas a la vista**:

1. **El punto de 2024.** Para cada contendiente, `error = p̂ − P(2024)` con signo, en
   proporción, y `dentro_IC ∈ {SI, NO}` contra el IC95 de la observada de 2024.
2. **La validación de origen móvil sobre la serie sellada**, rotulada
   **`RETROSPECTIVA-MECÁNICA`**: cada ola de 2018, 2020 y 2022 predicha **solo con las
   anteriores**, por los cinco contendientes, produciendo el error medio absoluto de cada uno
   sobre las olas que alcanza. Corre **en el COMMIT-1**, como ensayo de punta a punta, **antes
   de que exista el dato de 2024** — no la contamina, porque no toca 2024.

**Veredicto, declarado antes de ver el dato:**

- Un retador **VENCE AL PISO** si (a) su `|error|` sobre 2024 es menor que el de `C-PISO`,
  **y** (b) su error medio absoluto en la validación de origen móvil también lo es. Las dos,
  no una.
- Si vence **solo** en 2024 y no en la retrospectiva: **`PROPUESTA CON RESERVA`**, no
  adjudica. Un punto no distingue un mejor modelo de un golpe de suerte.
- Si **ningún** retador vence: **`C-PISO` se adopta**, como manda §4.6, y la fila «tendencia»
  queda **ocupada y perdida** para ENIGH — a diferencia de la de cruces, que queda no
  ocupada.
- **Un contendiente cuyo `p̂` satisfaga el criterio con un IC que no lo despeje no adjudica:
  propuesta con reserva** (§4, última línea de instrucciones).

**Nivel cruce y nivel marginal-por-eje: `NO-CONSTRUIBLE` en este duelo** (§3). No es un
veredicto sobre los contendientes de cruce; es la declaración de que nadie corrió el
mecanismo contra esta fuente.

---

## 6 · B-bis · Pre-registro de falsación — qué pasa si el falsador NO refuta

Declarado **antes** de ver el dato, como exige §5 de instrucciones. El falsador de este duelo
es el punto de ENIGH 2024.

| fila | si el falsador NO refuta | lectura |
|---|---|---|
| **B-bis-1** · «el piso de persistencia es difícil de vencer a nivel nacional» | ningún retador vence al piso con las dos condiciones de §5 | **CORROBORADA.** Tercera prueba prospectiva en que el piso aguanta; alimenta la regla de salida de θ por la vía «ninguna interacción venció», pero **solo para el nivel nacional** |
| **B-bis-2** · «la serie de remesas de ENIGH tiene tendencia legible» | `C-MEDIA` no es vencida por `C-T2`/`C-T3`/`C-TS` | **ACOTADA.** Con cuatro puntos de la nueva serie no se distingue tendencia de ruido; no dice que no la haya |
| **B-bis-3** · «la validación de origen móvil predice qué contendiente gana el punto nuevo» | el ganador de la retrospectiva es también el ganador de 2024 | **CORROBORADA**, y entonces la retrospectiva es un sustituto barato del duelo para futuras olas |
| **B-bis-4** · idem, caso contrario | el ganador de la retrospectiva **no** es el de 2024 | **FALSADOR DÉBIL.** Con una sola ola nueva no se puede separar «la retrospectiva no sirve» de «2024 fue atípico»; se declara y se espera a ENIGH 2026 |

**Si B-bis-1 y B-bis-3 pueden satisfacerse a la vez** —y pueden—, **manda B-bis-1**: la
adjudicación del estimador de la celda es la pregunta del duelo; la utilidad de la
retrospectiva es un subproducto. Declarado al sellar, como exige §5.

---

## 7 · Qué NO prueba este duelo

- **No prueba nada sobre cruces ni sobre segmentos de ENIGH.** §3.
- **No prueba nada sobre montos de remesas**, solo sobre la **incidencia** (hogar recibe /
  no recibe). El estimando de intensidad existe en una sola ola y en pesos corrientes de 2022
  sin deflactor declarado: compararlo entre olas sin resolver eso sería comparar escalas
  distintas (§4.3 de instrucciones). **Decisión de mesa pendiente** si alguien quiere
  la serie de montos.
- **No prueba nada sobre ENIGH como fuente de ingreso alto.** ENIGH sub-capta el ingreso alto
  y las remesas informales; este duelo mide la capacidad de **predecir su propia serie**, no
  la validez de la serie contra la realidad. Un modelo puede ganar el duelo prediciendo bien
  una cifra sesgada.
- **No prueba nada sobre la psicología del hogar mexicano.** §8.
- **No adopta nada al motor.** `cuenta_gen2` del COMMIT-2 se propone como
  `SI ... no adopta` — mide, no mueve el motor.
- **No toca las cuatro celdas de cruce reservadas de ENVIPE 2025 ni nada de ENVIPE 2026.**

---

## 8 · Módulo de auditoría de rigor extremo (§5 de instrucciones — este diseño afirma sobre México)

**¿Cuántos contadores movió este trabajo? Cero.** Este documento no sella corrida. Lo dice
aquí, al inicio del módulo, como manda v2.4.

**Qué parte del estimando es decisión del hogar y qué parte es precio, empleo o transferencia
(auditoría que el encargo §10 exige explícitamente, por estimando):**

Para `remesas > 0`, la respuesta honesta es que **la parte de decisión del hogar receptor es
pequeña**. Que un hogar en México reciba remesas depende, en orden de peso: de que tenga un
migrante (decisión tomada años antes, muchas veces por otra persona), del mercado laboral
**estadounidense**, del tipo de cambio, del costo de envío, y de la política migratoria de
otro país. La serie 2016–2022 atraviesa una pandemia y un auge histórico de remesas hacia
México: **lo que se mueve en esa ventana es estructura económica transnacional, no conducta**.
Este duelo mide si un modelo predice esa serie, y **el diseño prohíbe explícitamente leer el
resultado como un hallazgo sobre disposición al envío, solidaridad familiar o reciprocidad**.
Si `C-PISO` gana, eso dice que la incidencia es inercial; **no** dice que las familias sean
inerciales.

- **¿Pobreza/violencia/informalidad confundidas con cultura?** El riesgo es alto en este
  estimando y por eso §7 lo veda por escrito. Recibir remesas correlaciona con localidad
  pequeña y estrato bajo (`CALC-ENIGH2022-REMESAS-CONTEXTO-0001` mide el contraste:
  0.0839 [0.0772, 0.0908] de diferencia de prevalencia entre `tam_loc` extremos). Esa
  diferencia es **historia migratoria regional y estructura del mercado laboral**, no un
  rasgo de los hogares.
- **¿Sobregeneralización desde clase media urbana?** No aplica al revés de lo habitual: aquí
  el estimando **sobre-representa** el México rural y de estrato bajo. El sesgo de este
  diseño, si lo tiene, apunta al lado contrario del que §3 de instrucciones vigila de
  ordinario, y se declara.
- **¿Sesgo de marcos o muestras estadounidenses/europeas?** Ninguno: es medición propia sobre
  microdato primario mexicano (evidencia clase **(a)**, datos primarios en México). No entra
  ningún marco importado.
- **¿Qué cambia con foco rural/indígena/popular?** El nivel del estimando cambia mucho
  (ver el contraste de arriba); **la pregunta del duelo, no** — es de predicción de la serie
  nacional. El sistema indígena-comunal está fuera por diseño, como en todo el programa.
- **¿Qué parece psicológico y es incentivo racional?** Todo el estimando. Está dicho arriba.
- **¿Dónde hay evidencia débil e intuición fuerte?** En «la serie tiene tendencia»: cuatro
  puntos, movimiento no monótono, e intuición fuerte de que las remesas «vienen subiendo»
  (cierto en **monto agregado**, que es otra cosa que la **incidencia por hogar** — otra
  escala, §4.3). `C-MEDIA` existe precisamente para no premiar esa intuición.
- **¿Qué sería peligroso leído simplista?** «Las remesas a México son predecibles / estables»
  usado para argumentar que una política migratoria no las afectaría. El duelo mide la
  predictibilidad de una serie de cuatro puntos hacia un quinto, nada más.
- **¿Qué afirmación sobre el estado del corpus fue escrita a mano y no derivada?** Ninguna
  cifra de §2: todas salen de `resultados.json` de las corridas selladas, leídas por script en
  esta sesión, con `calc_id` y `RESULT` citados. Los conteos de universo (151 filas de
  replay, 3466 archivos, 56 del directorio) traen su comando.
- **¿Qué deuda "asumida a propósito" caducó?** La de `CALC-B-0001`: se selló con
  `contaminacion_declarada` (ADR-46 — la sesión ya había visto la serie GEN1 de las seis olas)
  y con `reglas_bajo_prueba: NINGUNA` bajo T9. **Eso no caduca y este diseño lo hereda**: la
  serie 2016–2022 que alimenta a los contendientes **no es ciega**. Lo ciego aquí es
  **2024**, que es lo que hace de esto una prueba prospectiva y no una retrospectiva. Se
  declara para que nadie lea el resultado como validación de la serie histórica.
- **¿En qué escala está cada cantidad y contra qué se compara?** §4.1 y §4.4.

---

## 9 · Fecha límite propuesta para el COMMIT-2, y por qué

**31/oct/2026**, la misma que el duelo ENVIPE 2026 (F7, enmienda C).

Dos razones, y una no es de calendario: (1) las dos pruebas prospectivas alimentan la **misma**
regla de salida de θ (`FP-...-8a1f-06`), y una que llegue después obliga a releer la otra;
(2) **la ceguera se degrada con el tiempo** — es el mismo argumento que puso a ENVIPE 2026 en
prioridad 1 de la cola. Cada semana que ENIGH 2024 pasa publicada y reservada es una semana más
de riesgo de que alguien del programa vea una cifra de 2024 en un comunicado, un resumen o una
conversación, y de que la prueba se degrade a factibilidad (E.6).

**Dependencia dura:** el COMMIT-2 no puede correr hasta que el payload de ENIGH 2024 esté en
el corpus. Hoy está en `data/cola-adquisicion-v1_0.tsv` en **prioridad 2**. Si el 31/oct
resulta inalcanzable, la causa más probable no es el diseño sino la cola, y la recomendación
del ejecutor a mesa es **subir ENIGH 2024 a prioridad 1**, por la misma razón por la que
ENVIPE 2026 ya está ahí.

---

## 10 · Secuencia propuesta (E.6 — tres commits, hay reserva de evaluación)

1. **COMMIT-1** · spec + medidor congelados juntos, **sin microdato de 2024**. Incluye: la
   ventana 2016–2022 con 2014 fuera; los cinco contendientes; la decisión de §4.4; la
   validación de origen móvil `RETROSPECTIVA-MECÁNICA` corrida de punta a punta; y la guardia
   de **una sola variable de agrupación** sobre la ola reservada que exige E.6. «Congelado» es
   **D-22 ampliada** (`FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-05`), que rige desde ya.
2. **COMMIT-2** · emisiones selladas de los cinco contendientes para 2024, **antes** de
   derivar `R`. El orden del diff es el sello.
3. **COMMIT-3** · `R` observado de 2024 y adjudicación por §5.

**Entorno: CAJA**, sin excepción — el COMMIT-2/3 abre microdato (A.2). Este diseño se redactó
en nube y no abrió ninguno.

---

## 11 · Procedencia de cada cifra de este documento

| cifra | de dónde | comando |
|---|---|---|
| serie 2014–2022 (P, IC, n, expandidos) | `data/corrida0/CALC-B-0001/resultados.json`, `data/corrida0/CALC-B-MARCO-ENIGH-0001/resultados.json`, `data/corrida0/CALC-ENIGH-0001/resultados.json` | lectura por script en sesión, 21/sep/2026, commit `b7ae01e` |
| universo, unidad, ponderador de cada CALC | el `spec.yaml` de cada corrida | idem |
| estado de replay | `forense/replay-evidencia.tsv` líneas 29, 86, 104 | `awk -F'\t'` sobre las 151 filas |
| contraste `tam_loc` 0.0839 [0.0772, 0.0908] | `CALC-ENIGH2022-REMESAS-CONTEXTO-0001/resultados.json`, `RESULT-...-CONTRASTES-JSON` | idem |
| «0 entradas de ENIGH 2024 en el manifiesto» | `data/cola-adquisicion-v1_0.tsv` fila `ENIGH_2024_NC`, campo `ids_manifiesto = SIN-ID-MANIFIESTO` | `grep` sobre la vista |
| `DISENO-...-ENVIPE2026` NO-ENCONTRADO | `forense/prereg-caja/`, 56 archivos | `ls forense/prereg-caja/` |

Ninguna cifra esperada está tecleada; ninguna sale del espejo del proyecto.

---

## 12 · Enmienda fechada — 21/sep/2026, al fusionar `main = c441c9d`

**No se reescribe nada de arriba** (A.10): se anota lo que cambió bajo los pies del documento.

**El molde apareció.** Al redactar este diseño (contra `main = fc13cdc`),
`DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md` estaba **NO-ENCONTRADO** en
`forense/prereg-caja/` — universo declarado: 56 archivos, `ls`, y por eso §0 dice que se tomó
en su lugar el texto de la firma F7. Ese negativo era cierto y **queda VENCIDO EN ALCANCE**:
PR #968 (`ACTO GEN2-DUELO-ENVIPE2026-COMMIT-1`) lo archivó después, y hoy `origin/main` trae
`DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md`, su `enmienda-v1_1.md` y
`DUELO-PROSPECTIVO-ENVIPE2026-spec-v1_0.md` (206 archivos en el directorio). Se reactiva por
re-lectura, no editando el texto viejo.

**Leído el molde real, este diseño no cambia — lo confirma en los dos puntos que importaban:**

1. **La regla de entrada es la misma, y el molde la escribe verbatim:** «Un estimando entra al
   duelo solo si tiene R sellado por ola en al menos tres olas y un universo idéntico a lo
   largo de ellas.» Es la que §2 aplicó.
2. **El trato de lo no construible es el mismo.** El molde, sobre `evade_norma`: «T5 y TC =
   NO-CONSTRUIBLE por serie insuficiente, y así se asientan. **No se sustituyen por T3, no se
   rellenan, no se omiten del marcador.**» Es exactamente lo que §3 y §4.3 hacen con el nivel
   de cruce de ENIGH. La decisión de declararlo en vez de simularlo no era una lectura
   arriesgada de la firma F7: es la regla de la casa, ya escrita.

**Dos cosas del molde que este diseño adopta, y que mejoran §5:**

- **El reporte es de tres cifras que no se colapsan**, no una: MAE en **pp**, **cobertura de
  IC95** (R dentro del IC del candidato) con su intervalo binomial, y el punto dentro del IC de
  R. §5 pedía error y `dentro_IC`; se añade la cobertura con su binomial. El COMMIT-1 las
  declara las tres.
- **La coincidencia entre contendientes se comprueba por comando antes de congelar, no se
  supone.** El molde lo aprendió en carne propia: para `evade_norma`, la constante del motor y
  la persistencia t−1 resultaron **el mismo número**, y se emiten una sola vez rotuladas como
  tal. En este duelo `C-PISO` y `C-MEDIA` **no** pueden coincidir (la serie no es plana), pero
  **el COMMIT-1 lo comprueba por comando igual**, junto con `C-T2` contra `C-T3`, y lo asienta.

**Lo que sigue siendo distinto, y por qué:** el molde de ENVIPE tiene niveles marginal (`E+`)
y cruce (`C2`) porque ENVIPE tiene marginales y cruces sellados por ola. ENIGH no los tiene
(§3), así que esos dos niveles quedan `NO-CONSTRUIBLE` aquí. Unidad: ENVIPE mide en **delito**
con `FAC_DEL`; ENIGH, en **hogar** con `factor`. **No se comparan entre sí sin función de
enlace, y en estos dos duelos no hay ninguna: no se mezclan** — ni sus errores, ni sus
marcadores.
