# S5 · Pre-registro de `civico.protesta.agravio_urbano` — reformulada (objeto de `N5 §2.8`)

### `prereg-caja-S5-L5` · **v1.0** · 4 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S5-L5-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S5-L5`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`, de una pieza **multi-ola** que mide los **cuatro** antecedentes del `SI` de `civico.protesta.agravio_urbano` — agravio, falla estatal, red previa, entorno urbano — donde `MAESTRA35-L9`/`L11` (ya corridos, `PENDIENTE-DE-MESA`) sólo midieron **dos**. |
> | **QUÉ NO ES** | No abre ningún `.dta`/`.sav` — los diez payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve el tier de `civico.protesta.agravio_urbano` (hoy `[MEDIA-FUERTE]`, `canon/modelo-decision-v4_0.md:558`). No reabre la fila `D` de `R7.4` (`ADR-158`, Hito D) ni dice nada sobre `civico.autodefensa.agravio_rural` (rama rural, línea 559) — mismas dos exclusiones que `L9 §4` ya declaró y que esta pieza no relaja. |
> | **VERIFICAS ASÍ** | Caja, al abrir cada payload de §6, compara variable y texto contra §1; compara marginales contra las guardias heredadas de `L9 §0.5` donde existan (`prot3` válidos `1576`, «sí» `112`, ola 2019) y reporta como hallazgo nuevo, no como guardia, los marginales de 2004/2006 que ningún acto anterior verificó. |

**Acto:** `ACTO MAESTRA38-N7 · PRE-REGISTRO-CIVICO-LAPOP`, 4/sep/2026, entorno **NUBE**, sobre `origin/main = a0e06da4ece2f307c46b895fb0da226d30b9cc29` (main avanzó 2 commits hasta `2b9c90e` al escribir esta pieza, mismo `[TRAMITE] digesto` ajeno al perímetro que `S4 §Acto` ya declaró — no PARO).

---

## 0 · Ficha bajo prueba y continuidad con `L9`/`L11`

### 0.1 · Definición vigente

`canon/modelo-decision-v4_0.md:558` (§3.7 Cívico y participación), verbatim:

> *SI hay **agravio personal/familiar + falla estatal palpable + red previa** Y el entorno es **urbano con espacio público disponible** ENTONCES se suma a **protesta** (8M: mujeres jóvenes urbanas; colectivos de búsqueda: familiares) — PORQUE G4 (destructor selectivo) — `[MEDIA-FUERTE]` **(a)**.* · **id:** `civico.protesta.agravio_urbano`

El `SI` tiene **cuatro** antecedentes conjuntos (agravio, falla estatal, red previa, entorno urbano), no dos.

### 0.2 · Objeto reformulado, verbatim de `N5 §2.8`

> **Objeto reformulado:** igual al original — este es el caso donde la reformulación es de encuadre, no de contenido: el objeto no cambia, se ancla a reactivos reales por cada término del SI…ENTONCES. **Reactivo:** `VIC1`/`vicbar4a` (agravio) + `AOJ12` (falla estatal) + `CP6`/`CP9`/`LAPOP-E8` (red previa) + `TAMANO` (urbano) → `PROT1`/`PROT2`/`prot3` (protesta).

Clasificada `(a) REFORMULABLE` en `forense/notas/2026-09-04-MAESTRA38-N5-diseno-9-reglas.md §3` fila `#8`, aceptada por la `FIRMA` de este encargo.

### 0.3 · Corrección de premisa por A.8/D-13 — `L9`/`L11` ya midieron la mitad de esta regla, dos veces

`forense/notas/2026-09-02-MAESTRA35-L9-spec.md §4` y `-resultados.md §4`, más `forense/notas/2026-09-02-MAESTRA35-L11-P0-censo.md`/`-resultados.md §2`, ya pre-registraron y **corrieron** un diseño 2×2 sobre este mismo `id` (`R7.4` en su nomenclatura), en dos instrumentos:

| pieza | instrumento | eje | `n`/celda más chica | `C1` (entorno, con agravio) | `C2` (agravio, en urbano) | veredicto |
|---|---|---|---|---|---|---|
| `L9 §4` | LAPOP 2019 | `ur`×`vic1ext` | rural-víctima, `n=65`, numerador `7` | **`NO-ESTIMABLE`** (bajo guardia de numerador `<10`) | **+5.60 pp** `[+2.32,+8.96]`, excluye 0 | **`CORROBORADA-PARCIAL`** |
| `L11 §2` | ENCUCI 2020 | `ur`×`AP6_9`-agravio (proxy) | rural-agravio, `n=2050`, numerador `188` | **+2.03 pp** `[−0.18,+4.12]`, contiene 0 | **+3.72 pp** `[+2.22,+5.22]`, excluye 0 | **`CORROBORADA-PARCIAL`**, `C1` declarado `AMBIGUA-ENTRE-INSTRUMENTOS` |

Las dos corridas están `PENDIENTE-DE-MESA` (`FP-298`, `ABIERTA`) — ningún sello de canon movió la línea 558. `L9 §4` es explícito: *"mide **dos de los cuatro** antecedentes de la regla — «red previa» y «falla estatal palpable» **no están en el instrumento**"* (verbatim, `resultados.md:174-175`).

**Lo que esta pieza corrige, con comando a la vista (A.6):** la afirmación de `L9` de que red previa y falla estatal "no están en el instrumento" fue verdadera **contra el universo de búsqueda que `L9` examinó el 2/sep** (LAPOP 2019/2023 + ENCUCI 2020, sin `busca_reactivos.py`). El censo de `N5` (3-4/sep, contra `data/inventario-reactivos-descargas-mx-v1_1.tsv`, superset indexado el 3/sep) **sí encuentra** los tres reactivos: `AOJ12` (falla estatal, olas 2004/2006/2023) y `CP6`/`CP9`/`LAPOP-E8` (red previa, olas 2004/2006). No es que `L9` se haya equivocado — es que el inventario que los trae **no existía todavía** cuando `L9` corrió (`data/inventario-reactivos-descargas-mx-v1_1.tsv` nace el 3/sep, `ACTO MAESTRA37-A1 P4`, un día después de `L9`). Cobertura retroactiva declarada por A.8(3): el hueco de `L9` no prueba ausencia, prueba que su búsqueda fue anterior a la tabla que sí los tiene.

**Consecuencia:** esta pieza no repite `C2` (agravio-en-urbano, ya `CORROBORADA` dos veces) ni vuelve a intentar `C1` con el mismo diseño de dos factores que ya cayó por guardia de numerador. Pre-registra el contraste **de cuatro factores** que `L9`/`L11` declararon no poder construir — es la pieza que **completa**, no que repite, el par de corridas ya hechas.

### 0.4 · Corrección de la caracterización de `LAPOP-E8`, verbatim contra el inventario

`N5 §2.8` agrupa `CP6`/`CP9`/`LAPOP-E8` bajo "asistencia a reuniones de organización religiosa/profesional/comunitaria" (asistencia propia, tres reactivos de la misma familia `CP`). El texto verbatim de `LAPOP-E8` en el inventario (2004 y 2006, únicas olas donde existe) es distinto en clase:

> *«¿Con qué firmeza aprobaría o desaprobaría que las personas participen en una organización o grupo para tratar de resolver los problemas de las comunidades»* (2004) / *«Que las personas participen en una organización o grupo para tratar de resolver los problemas de las comunidades»* (2006)

Es un ítem de **aprobación normativa de que otros participen** (batería `E` de tolerancia/apoyo a la acción colectiva de LAPOP), no de **asistencia propia** — que es lo que `CP6`("¿Asiste...?") y `CP9`("¿Asiste...?") sí preguntan, en primera persona, verbatim. Meter `LAPOP-E8` al mismo indicador que `CP6`/`CP9` mezclaría actitud con conducta. **Esta pieza corrige la agrupación**: `CP6`/`CP9` son el operacionalizador de "red previa" (§3); `LAPOP-E8` se mide aparte, como eje secundario de disposición normativa, y no entra al indicador principal ni a ninguna celda del falsador de §4.

---

## 1 · Variables, texto de reactivo verbatim, y la lista cerrada de olas

**Búsqueda contra `data/inventario-reactivos-descargas-mx-v1_1.tsv`, verificada por variable y por ola en esta sesión — no todas las olas traen los cuatro antecedentes:**

| ola | payload | agravio | falla estatal | red previa | entorno | protesta |
|---|---|---|---|---|---|---|
| **2004** | `1658622845Mexico 2004 Export Version.sav` / `642348348mexico 2004 export version.dta` | `vic1` | `aoj12` | `cp6`, `cp9` (`lapop-e8` aparte, §0.4) | `tamano` | `prot1` **solo** (sin `prot2`) |
| **2006** | `1008973606Mexico_LAPOP_final 2006 data set 092906.sav` / `518939279…dta` | `VIC1` | `AOJ12` | `CP6`, `CP9` (`LAPOP-E8` aparte) | `TAMANO`, `UR` | `PROT1` **y** `PROT2` |
| **2019** | `Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` | `vic1ext`, `vicbar4a` | `aoj12` | `cp6` **solo** — `cp9`/`lapop-e8` **ausentes**, verificado (0 filas en el inventario) | `tamano`, `ur` | `prot3` |
| 2021 | `MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta` | `vic1ext` | ausente | ausente | ausente | ausente — **excluida del falsador** |
| 2023 | `MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta`/`.sav` | `vic1ext` | `aoj12` | ausente | ausente | ausente — **excluida del falsador** |

**Lista cerrada de olas para el falsador de §4: 2004, 2006, 2019.** 2021 y 2023 quedan fuera — ninguna trae variable de protesta, verificado por búsqueda exhaustiva (`--regex prot|manifestacion|protesta` sobre cada payload, 0 filas en ambas).

### 1.1 · Texto de reactivo, verbatim del inventario

| variable | ola(s) | etiqueta verbatim |
|---|---|---|
| `prot1` | 2004 | «¿Ha participado Ud. en una manifestación o protesta pública?.» |
| `PROT1` | 2006 | «PROT1.¿Ha participado usted en una manifestación o protesta pública? ¿Lo ha hecho algunas veces, casi nunca o nunca?» |
| `PROT2` | 2006 | «PROT2.¿En el último año, ha participado en una manifestación o protesta pública? ¿Lo ha hecho algunas veces, casi nunca o nunca?» |
| `prot3` | 2019 | «Participó en una protesta» |
| `vic1` | 2004 | «¿Ha sido víctima de algún acto de delincuencia en los últimos 12 meses?» |
| `VIC1` | 2006 | «VIC1.¿Ha sido víctima de algún acto de delincuencia en los últimos 12 meses?» |
| `vic1ext` | 2019 | «Víctima de delincuencia en los últimos 12 meses» |
| `vicbar4a` | 2019 | «Un miembro de Familiy fue víctima de extorsión» *(sic — error de captura del extractor sobre "Family"; texto tal como está en el inventario, no corregido aquí)* |
| `aoj12` / `AOJ12` | 2004/2006/2019 | «Si fuera víctima de un robo o asalto, ¿cuánto confiaría en que el sistema judicial castigaría al culpable?» (2004/2006, verbatim con "robo o asalto"); 2019: «Confianza en que el sistema judicial castigue a los culpables» (etiqueta corta del mismo ítem) |
| `cp6` / `CP6` | 2004/2006/2019 | «Por favor, dígame si asiste a reuniones de alguna organización religiosa. ¿Asiste…?» (2004); «CP6. ¿Reuniones de alguna organización religiosa? Asiste ...» (2006); «Asistencia a reuniones de una organización religiosa» (2019, etiqueta corta) |
| `cp9` / `CP9` | 2004/2006 | «Por favor, dígame si asiste a reuniones de una asociación de profesionales, comerciantes o productores. ¿Asiste...?» (2004); «CP9. ¿De una asociación de profesionales, comerciantes, productores, y/o organizaciones campesinas? Asiste...» (2006) |
| `tamano` / `TAMANO` | 2004/2006/2019 | «Tamaño del lugar» |

### 1.2 · La variable de protesta cambia de forma entre olas — recodificación declarada

`prot1`/`PROT1`/`PROT2` (2004/2006) traen, por su propio texto, una escala de **frecuencia** («algunas veces, casi nunca o nunca») — no binaria. `prot3` (2019) es la variable ya armonizada del módulo core de LAPOP, verificada binaria por `L9` (`prot3 = 1` «Participó en una protesta», `= 2` en caso contrario, marginal `1576`/`112`). **Nadie ha abierto el codebook 2006** (§6) para confirmar los códigos exactos de `PROT1`/`PROT2` — se pre-registra aquí, antes de abrir nada, la recodificación que caja aplica si la escala trae 3 niveles: `"algunas veces" = 1` (protestó) · `"casi nunca"` + `"nunca" = 0` (no protestó) — lectura conservadora, consistente con el corte binario que `prot3` ya trae. Si el codebook revela una escala distinta (más niveles, orden invertido), esta recodificación **no se hereda a ciegas** — caja lo declara como hallazgo antes de calcular nada.

**2006 trae dos preguntas de protesta con ventana temporal distinta** (`PROT1` sin ventana explícita/histórica, `PROT2` "en el último año") — se tratan como dos piezas separadas, no se promedian ni se combinan en un solo indicador.

---

## 2 · Universo y ponderador, por ola — declarado, no heredado a ciegas

**Universo pre-registrado, por ola:** personas de 18+ con código válido en la variable de protesta de esa ola y en las variables de antecedente que esa ola trae (tabla §1). País completo; `TAMANO` es el estrato de entorno (§3), no un filtro de universo.

**Ponderador — búsqueda exhaustiva por payload, ninguna heredada de prosa:**

| ola | resultado de la búsqueda | declaración |
|---|---|---|
| 2004 | `wt` existe (ambos formatos), **sin etiqueta** en el inventario | nombre consistente con la convención LAPOP; **no confirmado por codebook** — ninguna corrida real lo ha verificado (a diferencia de 2019/2023, que `L9` sí abrió) |
| 2006 | **0 filas** con `wt`/`weight`/`peso`/`wgt` en las 225 variables que el inventario indexa del `.sav` (misma búsqueda, 225 del `.dta`) | **ponderador NO_DETERMINABLE desde el inventario** — hallazgo declarado, no supuesto; caja lo busca en el codebook o en el `.dta` mismo antes de estimar nada. Si no aparece, se reporta **sin ponderar**, declarado como tal (mismo criterio de `S2-L2-spec-v1_0.md §1.0`) |
| 2019 | `wt` = «Peso del país», **verificado constante = 1** por `L9 §1.2` (corrida real) | heredado como dato verificado, no como prosa — mismo criterio que `S4 §2` |

**Estrato/UPM, por ola:** 2006 trae `ESTRATOPRI`/`UPM`/`CLUSTER` explícitos en el inventario. 2004 trae `mestrat` (estrato) sin UPM/clúster visible en la búsqueda — declarado, pendiente de codebook. 2019 usa `estratopri`(4)/`upm`(129), mismo diseño que `L9` ya verificó.

---

## 3 · Dicotomizaciones y celdas

**`AGRAVIO`** = 1 si `vic1`/`VIC1` = 1 (2004/2006) **o** (`vic1ext` = 1 **o** `vicbar4a` = 1) (2019); 0 si todas las aplicables a esa ola son «no». `vicbar4a` (agravio **familiar** directo) es, dentro de 2019, la operacionalización más próxima al "agravio personal/familiar" del `SI` — se reporta también como sub-eje.

**`FALLA_ESTATAL`** = `AOJ12` dicotomizada BAJA/ALTA confianza en que el sistema de justicia castigaría al culpable. **Corte exacto pendiente de codebook** (§6) — el inventario no trae el mapa de valores. Se pre-registra la regla conceptual: la mitad inferior de la escala de confianza = `BAJA` (falla estatal palpable); la mitad superior = `ALTA`. Caja declara el corte real usado en cuanto abra el codebook, antes de calcular ninguna celda.

**`RED_PREVIA`** = 1 si `cp6`/`CP6` **o** `cp9`/`CP9` indican asistencia con cualquier frecuencia distinta de "nunca" (regla conceptual, corte exacto también pendiente de codebook — mismo criterio que `FALLA_ESTATAL`). `2019` sólo tiene `cp6`; `RED_PREVIA` en esa ola se construye **solo** con `cp6`, declarado como cobertura parcial. `LAPOP-E8` (§0.4) se reporta aparte, nunca sumado a este indicador.

**`URBANO`** = `TAMANO` dicotomizada (categoría(s) de ciudad/capital = urbano; resto = rural) — corte exacto pendiente de codebook, misma regla que los dos anteriores. Donde exista `ur`/`UR` binaria ya provista por LAPOP (2006, 2019), se reporta **en paralelo** como verificación cruzada de la dicotomización de `TAMANO`, sin sustituirla — el encargo pide `TAMANO` como estrato, no `ur`.

### 3.1 · Celdas — diseño de cuatro factores, decompuesto para que sea estimable

Cruzar `AGRAVIO`×`FALLA_ESTATAL`×`RED_PREVIA`×`URBANO` a la vez son **16 celdas** sobre una `n` de ola de ~1500-1600 — inviable de entrada (la celda más chica de sólo dos factores, en `L9`, ya cayó con `n=65`). Este pre-registro fija, **antes de ver ningún dato**, el mismo criterio de decomposición que `N5 §2.8` describe en su `se_mueve_si`:

**Celda principal (2 celdas) — el subgrupo de "alto riesgo" contra sí mismo por entorno:**

Dentro de quienes cumplen los tres antecedentes no-espaciales a la vez (`AGRAVIO=1` **y** `FALLA_ESTATAL=BAJA` **y** `RED_PREVIA=1`), comparar la tasa de protesta entre `URBANO=1` y `URBANO=0`:

```
C_completo = P(protesta | AGRAVIO∧FALLA_ESTATAL_BAJA∧RED_PREVIA, URBANO) −
             P(protesta | AGRAVIO∧FALLA_ESTATAL_BAJA∧RED_PREVIA, RURAL)
```

**Guardia de celda, anticipada:** el subgrupo que cumple los tres antecedentes a la vez es, por construcción, minoritario — sobre la `n` más chica de la tabla (2004, ola con menos casos totales entre las tres), es razonable esperar que la rama rural del subgrupo caiga bajo la guardia de numerador, igual que ocurrió en `L9` con un cruce de sólo dos factores. Se declara ahora, no después.

**Celdas diagnósticas (una por antecedente, 2×2 cada una, contra `URBANO`)** — para que la caída de `C_completo` por guardia no deje la pieza sin nada que reportar, igual que `L9 §4` hizo con `C2` cuando `C1` cayó:

- `C_agravio` = agravio × entorno (repite el diseño ya corrido de `L9`/`L11`, no se recuenta como hallazgo nuevo — se reporta como replicación de tercera ola).
- `C_falla` = falla estatal × entorno (**nuevo** — antecedente que `L9` no tenía).
- `C_red` = red previa × entorno (**nuevo** — antecedente que `L9` no tenía).

**Cota de n mínima por celda:** numerador `< 10` ⇒ `NO-ESTIMABLE`, misma guardia que `S4 §3` y `L9 §1.3` fijan — no se reinventa un umbral distinto para esta pieza.

---

## 4 · Falsador `B-bis` — las dos filas que exige, declaradas antes de correr

| | |
|---|---|
| **Signo esperado** | `C_completo > 0`, `C_falla > 0`, `C_red > 0` — cada antecedente, sumado al entorno urbano, empuja la protesta hacia arriba frente al mismo antecedente en entorno rural. `C_agravio` se congela con el mismo signo que `L9`/`L11` ya corroboraron (`> 0`) |
| **`CORROBORADA`** | `C_completo` estimable, con IC95 que **excluye** 0 en signo positivo |
| **`CONTRARIA`** | `C_completo` estimable, con IC95 que excluye 0 en signo **negativo** — el entorno urbano, entre quienes ya tienen los tres antecedentes, se asocia con **menos** protesta que el rural, contra lo que el `SI` predice |
| **`NO-DISCRIMINA`** | IC95 de `C_completo` contiene 0 |
| **`NO-ESTIMABLE`** | la celda rural (o urbana) del subgrupo de alto riesgo cae bajo la guardia de numerador — **fila que `B-bis` exige, qué pasa si no refuta:** el veredicto sale de las tres celdas diagnósticas (`C_agravio`, `C_falla`, `C_red`) tomadas juntas, no de `C_completo`, y se declara explícitamente que **el corazón de la regla de cuatro factores — que los tres antecedentes juntos, y no por separado, son los que el entorno urbano canaliza — no se midió**, mismo criterio de declaración que `L9 §4.1` fijó para su `C1` |
| **Precedencia entre las tres diagnósticas** | si las tres van limpias y en el mismo signo positivo, se reporta como corroboración **del patrón por partes**, nunca como corroboración de `C_completo` — no se sustituye lo compuesto por la suma de lo simple. Si alguna diagnóstica da signo negativo limpio, manda `CONTRARIA` sobre esa pieza específica y se reporta el desacuerdo, sin forzar un veredicto único para las tres |

**Qué significaría corroborar `C_completo`.** Sería la primera vez que los cuatro antecedentes del `SI` —no dos— se miden juntos y en la misma dirección sobre una muestra con diseño, algo que ni `L9` ni `L11` pudieron intentar por falta de los reactivos de falla estatal y red previa en su universo de búsqueda de entonces (§0.3). Cerraría, con reserva de instrumento (una sola ola con los tres antecedentes completos y celda urbano/rural estimable — 2004 o 2006, a determinar por caja según cuál de las dos tenga el numerador más grande), la brecha que `L9 §4` dejó escrita como pendiente.

**Reserva, declarada antes de medir.** Es, otra vez, una asociación transversal sin identificación causal — mismo tipo de limitación que `L9`/`L11` ya declararon para `C2`. Y el ponderador de 2006 es `NO_DETERMINABLE` desde el inventario (§2): si caja no lo encuentra en el codebook, la corrida de 2006 sale **sin ponderar**, declarado, y su IC95 no incorpora el efecto de diseño más allá del conglomerado que sí esté documentado.

---

## 5 · `se_mueve_si`

Si entre quienes cumplen los tres antecedentes no-espaciales (víctimas, con confianza baja en la justicia, con membresía en organización) la tasa de protesta en entorno urbano **no es mayor** que en entorno rural, la regla se rompe — verbatim de `N5 §2.8`, ahora con la celda formalizada en §3.1 y su guardia anticipada en §3.1/§4. Si `C_completo` cae por guardia (`NO-ESTIMABLE`), `se_mueve_si` se lee sobre las tres diagnósticas juntas, per §4.

---

## 6 · Archivos que la caja necesita abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `1658622845mexico_2004_export_version` | `Descargas Manuales/1658622845Mexico 2004 Export Version.sav` | `e725383552753223d263a1d65e2aaf9549a59859eb1b5777b666f32728700c99` |
| `642348348mexico_2004_export_version` | `Descargas Manuales/642348348mexico 2004 export version.dta` | `ef46b8f5a3c565c931d8ab1d173b2ee34f9f9459987159861ee4e24bf01b9880` |
| `1671516622cam_mexico_questionnaire_2004` | `Descargas Manuales/1671516622CAM Mexico Questionnaire 2004.pdf` (cuestionario 2004) | `452677a69fe522b8ae9f4eaa779bb62f1b9a8a7df0ca8a359d3028715dd55843` |
| `682647031technical_information_mexico_2004` | `Descargas Manuales/682647031Technical information_Mexico_2004.pdf` | `327716b8bc4eee1f4efe011cd41c18ef80c7416e279294807eedf3fffa48d8da` |
| `1008973606mexico_lapop_final_2006_data_set_092906` | `Descargas Manuales/1008973606Mexico_LAPOP_final 2006 data set 092906.sav` | `f43fcf78533febabe4eacb539f0ed03470c8320d606f29f54c220cda5abb3039` |
| `518939279mexico_lapop_final_2006_data_set_092906` | `Descargas Manuales/518939279mexico_lapop_final 2006 data set 092906.dta` | `e426210067f9dba8aca87a0df2161bc7389cc5aaf9e5516aa7ebf9cb52f149fa` |
| `1390537077technical_information_mexico_2006` | `Descargas Manuales/1390537077Technical information_Mexico_2006.pdf` | `521cba1bd010dedecbb1df0e9ad5ced7f57f21da1f47b56b2656be54b874af60` |
| `mexico_lapop_americasbarometer_2019_v1_0_w` | `Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta` | `c88f79ebb8e73c473cd78d894eb093261f172e736a35bd7bc677b4e8b1454a57` |
| `mexico_lapop_americasbarometer_2019_codebook_v1_0_w` | `Descargas Manuales/Mexico LAPOP AmericasBarometer 2019_Codebook_v1.0_W.pdf` | `4efa5809c3fde487516a60acf782f013444889a775bf368745c8da577cba75ce` |
| `abmex18_v12_0_2_5_spa_190207_w` | `Descargas Manuales/ABMex18-v12.0.2.5-Spa-190207_W.pdf` (cuestionario 2018/19) | `6319cfebeda635563cec7d70573430413e608e3366acf00fa35b61cc41362f5c` |

No hay codebook 2004/2006 registrado por separado en el manifiesto — los dos "technical information" de arriba son el único documento de estructura disponible para esas dos olas; si no traen el mapa de valores de `PROT1`/`PROT2`/`AOJ12`/`CP6`/`CP9`/`TAMANO`, los cortes de §3 quedan sin confirmar hasta que caja abra el `.dta`/`.sav` mismo.

---

## 7 · Qué NO hace este acto

No abre ningún archivo de §6. No calcula ninguna celda ni IC95. No mueve el tier de `civico.protesta.agravio_urbano`. No reabre la fila `D` de `R7.4` (`ADR-158`) ni dice nada sobre `civico.autodefensa.agravio_rural`. No repite como hallazgo nuevo lo que `L9`/`L11` ya corrieron (`C_agravio`/`C2`) — lo cita como evidencia existente, `PENDIENTE-DE-MESA`. No resuelve los cortes de `FALLA_ESTATAL`/`RED_PREVIA`/`URBANO` — quedan pendientes de codebook, declarado, no inventado.

**Medición: caja, acto `MAESTRA38-L5`.**

**El primer resultado que produzca este procedimiento es el que se reporta.**
