# `SORTEO-V2-PROPUESTA` · rediseño del sorteo de `ACT-PIL-3` bajo la cuota rota — 25/ago/2026

**Acto:** `SORTEO-V2-PROPUESTA` (`FP-145`, `L9-c`). **Solo redacción — ningún sorteo real corre en este acto.** Entorno NUBE. Ejecuta la opción `c` que `L9`/`FP-133` firmó (`canon/gobernanza-v1_15.md` `ADR-168(h)`, línea `3351`): *"el marco de candidatas no se poda ni se re-congela; `ACT-PIL-3` debe diseñarse para que su sorteo respete el tope del 20% sin tirar candidatas."*

## 0 · Perímetro y qué NO hace este documento

Este documento **propone** un algoritmo. No modifica `forense/marco-candidatas-piloto-v1_0.tsv`, no corre ningún sorteo, no amplía el marco (autoridad semántica pendiente, `AUTORIDAD-SEMANTICA-MARCO`, ver `PROPAGA-330-337`), y no toca `milpa/`. Cuando mesa lo firme, el acto sucesor que lo ejecute deriva el sorteo real de este pseudocódigo, no de una reinterpretación.

## 1 · Estado del marco vigente (verificado, no supuesto)

Fuente: `forense/marco-candidatas-piloto-v1_0.tsv`, 60 filas, columna `estrato` = `dominio|grado_dependencia|dificultad` (`ADV1-M1`, diseño de `ACT-PIL-2`/`ADR-130`).

```
$ awk -F'\t' 'NR>1{print $17}' forense/marco-candidatas-piloto-v1_0.tsv | sort | uniq -c | sort -rn
     10 dinero|P2|DIFICIL
      6 dinero|P2|MEDIA
      4 trabajo|P1|MEDIA
      4 salud|P2|MEDIA
      4 civico|P1|MEDIA
      4 civico|P0|MEDIA
      3 trabajo|P2|MEDIA
      3 dinero|P1|MEDIA
      3 comunicacion|P2|MEDIA
      2 tramite|P0|MEDIA
      2 salud|P0|MEDIA
      1 tramite|P2|MEDIA
      1 tramite|P1|MEDIA
      1 tiempo|P2|MEDIA
      1 tiempo|P1|MEDIA
      1 tiempo|P1|DIFICIL
      1 informacion|P2|MEDIA
      1 informacion|P2|DIFICIL
      1 familia|P2|MEDIA
      1 familia|P2|DIFICIL
      1 familia|P1|DIFICIL
      1 familia|P0|MEDIA
      1 dinero|P2|FACIL
      1 dinero|P1|FACIL
      1 dinero|P0|MEDIA
      1 cooperacion|P1|MEDIA
```

26 estratos (coincide con `canon/estado-programa-v1_10.md:99`). Columna `publicada`:

```
$ awk -F'\t' 'NR>1{split($10,a," "); print a[1]}' forense/marco-candidatas-piloto-v1_0.tsv | sort | uniq -c
     24 NO
      8 PENDIENTE-FUERA-DE-INDICE
     28 SI
```

28 de 60 (46.7%) `SI`; 8 `PENDIENTE-FUERA-DE-INDICE`; 24 `NO`. El marcador puntuable es de 50 (`P0=10` fuera del marcador, `P1=17`, `P2=33`); sobre el marcador puntuable, 22/50 = 44.0% `SI`. Ninguna de las dos cifras cumple el tope del 20% de `ADV1-M1` — es exactamente la ruptura que `FP-133` midió.

**P0/P1/P2** son la columna `grado_dependencia` del marco (`ADV1-M1`): prioridad/dependencia de la celda respecto al motor, no publicación ni dificultad. `P0` (10 filas) queda fuera del marcador puntuable (anexo de plomería); `P1` (17) y `P2` (33) son las 50 puntuables. El sorteo de este documento opera **sobre el marcador puntuable de 50** — las 10 `P0` no son elegibles salvo que un acto futuro las incorpore al marcador, fuera de este perímetro.

**Las 8 `PENDIENTE-FUERA-DE-INDICE`** son las filas cuyo publicador (Banxico/CNBV/BMV/HR Ratings) el diseño de dos pasos de `FP-93` no alcanza por construcción (`FP-134`, `canon/gobernanza-v1_15.md:3353`, `ADR-168(i)`). **Regla de elegibilidad:** estas 8 celdas son elegibles para el sorteo **si y solo si `FP-146` (índice nuevo Banxico/CNBV/BMV) las resuelve a `SI`/`NO` antes de que corra el sorteo real.** Mientras sigan `PENDIENTE-FUERA-DE-INDICE`, el algoritmo de §2 las trata como **no elegibles** (ni cuentan en `n_estrato` ni pueden salir sorteadas) — no se tratan como `publicada=SI` ni como `publicada=NO` por default, porque ninguna de las dos es verificada.

---

### Enmienda in situ, 25/ago/2026, `ACTO ENMIENDA-CUADRO-SORTEO` — las 8 `PENDIENTE-FUERA-DE-INDICE` de arriba quedan resueltas, texto original intacto

El texto de §1 arriba **no se toca**: es el registro de lo que el marco era cuando esta propuesta se escribió,
25/ago/2026, antes de que `FP-146` corriera. `ACTO INDICE-NO-INEGI` (`PR #345`, mismo día, más tarde) resolvió
las 8 `PENDIENTE-FUERA-DE-INDICE` a **5 `SI` + 3 `NO`** (`DIN-07/08/09/10/12` → `SI`; `DOC-03/05/06` → `NO`,
todas `P2|dinero`, verificado contra `forense/marco-candidatas-piloto-v1_0.tsv` columnas `id`/`grado_dependencia`/
`dominio`) — `forense/notas/2026-08-25-indice-no-inegi.md`. Esto es **propagación de hecho, no una decisión
nueva**: las §2-§2.3 (reglas duras, pseudocódigo, protocolo de semilla) que este documento propone no cambian en
absolutamente nada — la regla de elegibilidad de arriba ya preveía este caso ("elegibles ... si y solo si
`FP-146` las resuelve"), y lo que sigue es exactamente esa cláusula ejecutándose.

**Cuadro vigente, re-derivado directo de `forense/marco-candidatas-piloto-v1_0.tsv` (framework v1_0), no copiado
de la nota de `FP-146`:**

```
$ awk -F'\t' 'NR>1{split($10,a," "); print a[1]}' forense/marco-candidatas-piloto-v1_0.tsv | sort | uniq -c
     27 NO
     33 SI
(0 PENDIENTE — verificado: sin filas PENDIENTE-FUERA-DE-INDICE que queden)

$ awk -F'\t' 'NR>1 && ($9=="P1"||$9=="P2"){split($10,a," "); print a[1]}' forense/marco-candidatas-piloto-v1_0.tsv | sort | uniq -c
     23 NO
     27 SI
(marcador puntuable, 50 filas — P1 ∪ P2)
```

| | filas | `SI` | % `SI` | tope 20% | exceso |
|---|---|---|---|---|---|
| marco completo | 60 | 33 | 55.0 % | 12 | +21 |
| marcador puntuable (P1∪P2) | 50 | 27 | 54.0 % | 10 | +17 |

**Discrepancia declarada, no callada.** El cuadro de `forense/notas/2026-08-25-indice-no-inegi.md` §5 reporta
*"SI sobre el marcador 50: 33/50 = 66.0 %, exceso +23"* — esa cifra usa el total de `SI` del marco completo (33,
que incluye las 6 `SI` de las 10 filas `P0`) dividido entre el denominador del marcador puntuable (50), no el
conteo de `SI` **dentro** del marcador puntuable. Re-derivado directo del framework arriba: el marcador
puntuable tiene **27** `SI` (no 33), así que la cifra correcta es **27/50 = 54.0 %**, exceso **+17** (no +23).
El marco completo (33/60 = 55.0 %, exceso +21) sí coincide con la nota de `FP-146` — la discrepancia está
acotada al recorte por `P0`/`P1`/`P2`. Este documento usa el número **re-derivado aquí**, no el de la nota,
porque §1 ya declaraba (antes de esta enmienda) que el algoritmo de §2 opera **solo** sobre el marcador
puntuable de 50 — es la cifra que este documento necesita, y la que el propio marco produce al filtrarse por
`grado_dependencia`.

**Lectura para el sorteo (§2, sin tocarla).** El cierre del filtro (i) no alivia la cuota bajo ninguna de las
dos lecturas: el marco pasa de **28/60 (46.7 %) con 8 sin evaluar** a **33/60 (55.0 %) con cero sin evaluar**, y
el marcador puntuable de **22/50 (44.0 %) con 8 sin evaluar** (de los cuales las 8 pendientes eran todas del
marcador puntuable) a **27/50 (54.0 %) con cero sin evaluar**. El algoritmo de §2 —cuota como restricción
**dura**, no objetivo blando— sigue siendo exactamente el mecanismo correcto para un marco con exceso de `SI`;
nada de §2-§2.3 necesita cambiar para acomodar esta cifra, la restricción dura ya estaba diseñada para un marco
que la rebasa.

**La rama de exclusión de §1 queda satisfecha, no cerrada por decisión.** Ya no hay ninguna fila `marco` en
estado `PENDIENTE-FUERA-DE-INDICE`: las 8 quedaron resueltas a `SI`/`NO` reales por `FP-146`, así que la regla
de elegibilidad de arriba ("si y solo si `FP-146` las resuelve") se cumplió por sí sola — no fue necesario que
mesa decidiera nada nuevo. `FP-150` (sello de mesa sobre `sorteo-v2`) sigue **ABIERTA**: lista para sello sobre
estas cifras post-`#345`, no firmada en este acto.

## 2 · Algoritmo — cuota como restricción DURA del muestreo

**Entradas:**
- `marco`: filas del marcador puntuable (`grado_dependencia` ∈ {P1, P2}) con `publicada` ∈ {SI, NO} (las `PENDIENTE-FUERA-DE-INDICE` sin resolver por `FP-146` se excluyen de `marco` por completo, no se muestrean ni se cuentan — §1).
- `estrato(fila)`: columna `estrato` del marco (`dominio|grado_dependencia|dificultad`).
- `n_sorteo`: tamaño objetivo del set v1, `12 ≤ n_sorteo ≤ 15` (`ADV1-M1`).
- `cuota_max = floor(0.20 * n_sorteo)`: máximo de filas `publicada=SI` admitidas en el sorteo — **restricción dura**, no objetivo blando.
- `semilla`: entero derivado por el protocolo de §3.

**Reglas duras (rechazadas si se violan, no relajadas):**
1. `|resultado| == n_sorteo`.
2. `count(resultado, publicada=SI) ≤ cuota_max`.
3. Todo estrato con al menos una fila en `marco` recibe **al menos una** fila en `resultado` si `n_sorteo ≥ n_estratos_no_vacios` (asignación proporcional con piso 1, resto por remanente más grande — método de Hamilton/mayor resto); si `n_sorteo < n_estratos_no_vacios`, se sortea sin reposición **cuáles** estratos entran (mismo generador, semilla derivada) antes de sortear filas dentro de ellos, y se declara qué estratos quedaron fuera con la excusa `SIN CUPO EN n_sorteo`, no una segunda clase de `SKIP`.
4. Sin reposición: cada `id` sale como máximo una vez.
5. Determinista: la misma `semilla` y el mismo `marco` (mismo contenido, mismo orden de filas en el TSV) producen siempre el mismo `resultado` — se fija el orden de iteración por `id` ascendente antes de aplicar cualquier permutación pseudoaleatoria.

### 2.1 · Pseudocódigo

```
función sortear(marco, n_sorteo, cuota_max, semilla):
    # 1. Particionar el marco elegible por estrato y por publicada
    estratos = group_by(marco, key=estrato)
    for e in estratos:
        estratos[e].publicadas = [f for f in estratos[e] if f.publicada == "SI"]
        estratos[e].no_publicadas = [f for f in estratos[e] if f.publicada == "NO"]

    # 2. Cuota de asientos por estrato (Hamilton / mayor resto), sobre |marco|
    asientos = asignar_asientos_proporcional(estratos, n_sorteo)  # §2.2

    # 3. Verificar infactibilidad ANTES de sortear una sola fila (§2.3)
    para cada estrato e con asientos[e] > 0:
        si len(estratos[e].no_publicadas) == 0 y asientos[e] > 0:
            marcar_estrato_infactible(e)  # el estrato SOLO tiene publicadas
    si hay estratos infactibles:
        aplicar FALLBACK (§2.3) -- puede reasignar asientos entre estratos
        recalcular asientos tras el fallback

    # 4. Sorteo determinista dentro de cada estrato, sin exceder la cuota GLOBAL
    resultado = []
    presupuesto_publicadas = cuota_max
    rng = PRNG_determinista(semilla)  # p.ej. numpy.random.Generator(PCG64(semilla))

    # 4a. Primero se sortean las NO-publicadas de cada estrato (nunca gastan cuota)
    para cada estrato e en orden estable (por nombre de estrato):
        elegidas_no = sorteo_sin_reposicion(estratos[e].no_publicadas, rng,
                                             k=min(asientos[e], len(estratos[e].no_publicadas)))
        resultado += elegidas_no
        asientos[e] -= len(elegidas_no)

    # 4b. Asientos restantes por estrato se llenan con publicadas, sin exceder
    #     ni el asiento del estrato ni el presupuesto GLOBAL de la cuota
    para cada estrato e en el mismo orden estable:
        si asientos[e] > 0:
            k = min(asientos[e], len(estratos[e].publicadas), presupuesto_publicadas)
            elegidas_si = sorteo_sin_reposicion(estratos[e].publicadas, rng, k)
            resultado += elegidas_si
            presupuesto_publicadas -= len(elegidas_si)
            asientos[e] -= len(elegidas_si)
            si asientos[e] > 0:
                registrar SKIP(estrato=e, motivo="cuota global agotada o publicadas insuficientes",
                                faltan=asientos[e])

    # 5. Verificación final -- las reglas duras son postcondición, no esperanza
    assert len(resultado) <= n_sorteo
    assert count(resultado, publicada="SI") <= cuota_max
    devolver resultado, log_de_skips
```

### 2.2 · Asignación de asientos por estrato (Hamilton / mayor resto)

```
función asignar_asientos_proporcional(estratos, n_sorteo):
    total = sum(len(estratos[e]) for e in estratos)
    cuota_exacta[e] = n_sorteo * len(estratos[e]) / total   # para cada estrato
    asientos[e] = floor(cuota_exacta[e])                    # piso
    restantes = n_sorteo - sum(asientos.values())
    # reparte el remanente a los `restantes` estratos con mayor parte fraccionaria,
    # desempate determinista por orden alfabético de `estrato` (nunca al azar)
    orden = sort_by(estratos, key=lambda e: (-frac(cuota_exacta[e]), e))
    para e en orden[:restantes]:
        asientos[e] += 1
    devolver asientos
```

### 2.3 · Regla explícita de infactibilidad por estrato

Un estrato `e` es **infactible bajo cuota dura** si `asientos[e] > 0` y `estratos[e].no_publicadas == []` — es decir, **todas** las filas elegibles de ese estrato tienen `publicada=SI`, así que llenar su asiento sin publicadas es imposible por construcción (no es una cuestión de PRNG, es aritmética: `0` `NO`-elegibles disponibles).

**Fallback declarado (elegido antes de necesitarlo, no post-hoc):** cuando un estrato es infactible bajo la regla 3, sus asientos **se reasignan a los demás estratos con `no_publicadas` disponible**, por el mismo criterio de mayor resto de §2.2 restringido al subconjunto de estratos no infactibles — el estrato infactible pasa a tener `asientos[e] = 0` (0 filas de ese estrato en el sorteo, **no** una excepción a la cuota) y esto se declara explícitamente en el log de skips como `ESTRATO EXCLUIDO POR INFACTIBILIDAD DE CUOTA`, con el conteo de sus filas `SI`/`NO`. **Lo que este fallback NO hace:** no eleva `cuota_max` para acomodar al estrato, no saca una fila `SI` de ese estrato "porque no hay de otra" (eso violaría la cuota dura, exactamente lo que `L9-c` prohíbe), y no descarta filas del marco de 60 — las filas del estrato excluido siguen en el marco, solo no salen sorteadas *esta vez*; un sorteo futuro (tras `FP-146` u otra ampliación) puede reevaluarlas.

Si **todos** los estratos con asiento resultan infactibles a la vez (degenerado: cuota global de 0 con `cuota_max ≥ 1` filas publicadas necesarias en algún estrato para llenar `n_sorteo`), el algoritmo **PARA y no sortea** — se reporta `INFACTIBLE GLOBAL`, mesa decide (subir `n_sorteo`, aceptar menos de `n_sorteo` celdas, o esperar a que más filas se resuelvan a `NO`/`SI` reales).

## 3 · Protocolo de la semilla — no un número fijo

**Semilla = el SHA de merge del commit del acto que congele `marco` + `sorteo` a la vez.** No se fija un entero en este documento — sería exactamente el defecto que anuló `867948c` (`ADR-135(d)`, `canon/gobernanza-v1_15.md:2706`): una semilla derivada de un árbol que después cambió deja de tener sentido criptográfico como compromiso. Protocolo:

1. El acto sucesor que ejecuta el sorteo real escribe el algoritmo de §2 aplicado, pero **no corre el PRNG** hasta que su propio PR esté listo para fusionar.
2. La semilla entera se deriva determinísticamente del SHA de merge una vez que existe: `semilla = int(sha256(sha_de_merge_hex).hexdigest(), 16) % (2**63)` (mismo patrón que `derivar_seed_scope` de `forense/prereg-duelo-v2/scoring-adv1-m3.py:685` ya usa para derivar semillas hijas de una semilla base — reutilizar la función, no reinventar el hash).
3. Esto significa que el sorteo real **no puede correr en el mismo acto que lo propone** — el SHA de merge no existe hasta después de fusionar. El acto sucesor: (a) fusiona `marco` (si `FP-146` lo actualizó) y este algoritmo sin ejecutar el sorteo, (b) toma el SHA de merge resultante, (c) corre el sorteo con esa semilla en un segundo commit sobre la misma rama o en un acto inmediatamente posterior, declarando el SHA usado.
4. `867948c` queda citado aquí solo como antecedente histórico anulado — no se reutiliza aunque el marco terminara siendo idéntico (mismo criterio que `ADR-135(d)` ya fijó).

## 4 · Interacción con P0/P1/P2

Ver §1: el sorteo opera sobre el marcador puntuable (`P1` ∪ `P2`, 50 filas). `P0` (10 filas, "anexo de plomería") queda **fuera del marcador y fuera del sorteo** por la misma razón que queda fuera del denominador de `60`/`50` en `canon/estado-programa-v1_10.md:99` — no es una exclusión nueva de este acto, es la que el marco ya trae. Si mesa decide en el futuro que `P0` entra al marcador puntuable, ese cambio se declara en el marco (columna `grado_dependencia`) antes de que el sorteo lo vea — este algoritmo no distingue `P1` de `P2` para nada más que estar dentro o fuera del universo elegible; la cuota y la estratificación tratan `P1`/`P2` igual dentro de `marco`.

## 5 · Casos de prueba

Estratos de ejemplo abreviados para legibilidad (formato `estrato: [publicada,...]`, cada elemento una fila del marco).

### Caso 1 — normal (cuota se cumple sin fallback)

```
marco de ejemplo, n_sorteo = 12, cuota_max = floor(0.20*12) = 2

dinero|P2|DIFICIL:   [NO,NO,NO,NO,NO,NO,NO,SI,SI,SI]   (10 filas: 7 NO, 3 SI)
dinero|P2|MEDIA:     [NO,NO,NO,NO,SI,SI]                (6 filas: 4 NO, 2 SI)
trabajo|P1|MEDIA:    [NO,NO,NO,SI]                       (4 filas: 3 NO, 1 SI)
civico|P0|MEDIA:     -- fuera de marco (P0, §4) --

asientos (Hamilton sobre 20 filas elegibles, n_sorteo=12):
  dinero|P2|DIFICIL ~ 12*10/20 = 6.0 -> 6
  dinero|P2|MEDIA   ~ 12*6/20  = 3.6 -> 3 (+1 por mayor resto) = 4
  trabajo|P1|MEDIA  ~ 12*4/20  = 2.4 -> 2

Ningún estrato es infactible (todos tienen >=1 `NO`).
4a) NO-publicadas primero: dinero|P2|DIFICIL toma hasta 6 NO (hay 7, sortea 6);
    dinero|P2|MEDIA toma hasta 4 NO (hay 4, toma las 4);
    trabajo|P1|MEDIA toma hasta 2 NO (hay 3, sortea 2).
    -> 6+4+2 = 12 = n_sorteo. Asientos agotados sin tocar la cuota.
4b) presupuesto_publicadas sigue en 2 (no se gastó nada).

RESULTADO: 12 filas, 0 publicadas, cuota (2) no agotada -- válido.
(Si algún estrato no hubiera tenido suficientes NO para llenar su asiento,
 el remanente de asiento se llena con SI hasta agotar presupuesto_publicadas=2,
 mismo mecanismo del paso 4b.)
```

### Caso 2 — infactibilidad por estrato

```
marco de ejemplo, n_sorteo = 12, cuota_max = 2

tiempo|P2|MEDIA:      [SI, SI]                (2 filas, AMBAS publicadas -- 0 NO)
familia|P2|DIFICIL:   [SI]                    (1 fila, publicada -- 0 NO)
dinero|P2|DIFICIL:    [NO,NO,NO,NO,NO,NO,NO,SI,SI,SI]  (10 filas: 7 NO, 3 SI)

asientos iniciales (Hamilton sobre 13 filas, n_sorteo=12):
  tiempo|P2|MEDIA    ~ 12*2/13  = 1.85 -> 1 (+1 mayor resto) = 2
  familia|P2|DIFICIL ~ 12*1/13  = 0.92 -> 0 (+1 mayor resto) = 1
  dinero|P2|DIFICIL  ~ 12*10/13 = 9.23 -> 9

Verificación de infactibilidad (§2.3):
  tiempo|P2|MEDIA:    asientos=2 > 0 y no_publicadas=[] -> INFACTIBLE
  familia|P2|DIFICIL: asientos=1 > 0 y no_publicadas=[] -> INFACTIBLE
  dinero|P2|DIFICIL:  asientos=9 > 0 y no_publicadas=7  -> factible (parcial, ver abajo)

FALLBACK: tiempo|P2|MEDIA y familia|P2|DIFICIL quedan con asientos=0,
  registradas "ESTRATO EXCLUIDO POR INFACTIBILIDAD DE CUOTA" (2+1=3 filas
  publicadas, cero elegibles). Los 3 asientos liberados se reasignan al
  único estrato factible: dinero|P2|DIFICIL pasa de 9 a 12 asientos --
  pero dinero|P2|DIFICIL solo tiene 10 filas totales (7 NO + 3 SI).

  4a) NO-publicadas: dinero|P2|DIFICIL toma sus 7 NO (agota sus 7 NO).
  4b) Quedan 12-7=5 asientos del estrato, pero solo hay 3 SI disponibles
      y presupuesto_publicadas=2 (cuota global) -- toma min(5,3,2)=2 SI.
      Quedan 3 asientos sin llenar -> SKIP(estrato=dinero|P2|DIFICIL,
      motivo="cuota global agotada", faltan=3).

RESULTADO: 7 NO + 2 SI = 9 filas (< 12 = n_sorteo), 3 SKIP declarados,
  cuota (2) exactamente al límite -- válido bajo la restricción dura;
  el sorteo entrega menos de n_sorteo en vez de violar la cuota.
```

### Caso 3 — caso límite de la cuota del 20%

```
marco de ejemplo, n_sorteo = 15 (techo de ADV1-M1), cuota_max = floor(0.20*15) = 3

Un único estrato grande, dinero|P2|DIFICIL: [NO]*7 + [SI]*3 (10 filas)
más otros tres estratos chicos con solo NO, sumando 5 filas NO adicionales.

Total elegible = 15 filas (10+5). n_sorteo = 15 = total elegible ->
asientos = todas las filas del marco (Hamilton trivial: cada fila entra).

RESULTADO: 12 NO + 3 SI = 15 filas. count(SI) = 3 = cuota_max exacto --
  la cuota se toca en el límite, no lo excede: 3 <= floor(0.20*15) = 3.
  Válido -- este es el caso donde la restricción dura se satura sin
  margen, y por eso el algoritmo compara con <= (no <) en la postcondición
  del paso 5: un sorteo que aterriza EXACTO en el tope es tan válido
  como uno que queda por debajo, y no dispara SKIP ni fallback.
```

## 6 · Fila nueva `A.12` y cierre de `FP-145`

`instrucciones-proyecto-v2_11.md:354` (`A.12`) exige fila de tablero para hacer visible que la mesa aún tiene que sellar este diseño antes de que corra. Se añade `FP-150` (`ABIERTA`) — *«mesa sella sorteo-v2»* — en `forense/firmas-pendientes.tsv`, apuntando a este documento.

`FP-145` (`FIRMADA` desde `ADR-168(h)`, sin ejecutar) se marca **ejecutada** en el sentido declarado por el encargo: **la propuesta fue redactada** — el sorteo real, con datos y semilla, no se ha realizado y no corre hasta que mesa selle `FP-150` y exista el SHA de merge del §3.

## 7 · Lo que este acto NO hace

No corre ningún sorteo real, con datos ni con semilla simulada. No amplía el marco de 60. No resuelve las 8 `PENDIENTE-FUERA-DE-INDICE` (`FP-146`, acto aparte). No modifica `forense/marco-candidatas-piloto-v1_0.tsv`. No toca `milpa/`. No toca ningún directorio de espejo (no existe tal directorio en el árbol).
