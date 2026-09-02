# `ACTO MAESTRA34-L6 · CIVICA-HOMOLOGACION-ESCALONADA` — cierre

2/sep/2026 · entorno **UBUNTU** · `ADR-288` · **compuerta `GATED a MAESTRA34-L5`
verificada por producto**
Encargo: `forense/encargos/2026-09-02-MAESTRA34-L6-CIVICA-HOMOLOGACION-ESCALONADA.md`
(dirección/Fable, `SHA de redacción 29ab80a`, archivado verbatim por A.3 en el
primer commit del acto, `51c7009`). Ejecutado con `/acto` (`ADR-237`).
La tabla de tratamiento vive en
`forense/notas/2026-09-02-MAESTRA34-L6-P0-tabla-tratamiento.md`; la spec
congelada y la medición, en `…-P2-spec.md` (dos commits).

---

## 0 · Lo que este acto encontró que no esperaba encontrar

**El número que venía a identificar se le deshizo en las manos, y eso es el
resultado.** `MAESTRA34-L4` midió `+10.4790 pp` de más participación cuando la
elección local coincide con la federal, y declaró —antes de medir— que no podía
separar concurrencia de año. Este acto fue a separarlas con el diseño escalonado
que la propia firma `DC1-d` nombró como sucesor. Las separó, y **la
concurrencia no es lo que mueve la participación**: `β = +0.0149 pp`, con los dos
intervalos conteniendo cero.

Pero el cero no dice «no pasa nada». Dice algo más específico y más útil: el
promedio esconde **dos efectos de signo opuesto**. Cuando la elección municipal
se junta con una **presidencial**, la participación sube `+2.41 pp` sobre la
tendencia; cuando se junta con una **intermedia**, **baja** `−5.69 pp`. Ninguno
de los dos intervalos cruza cero. **Nayarit votó más en su elección local sola de
2017 (61.03 %) que concurriendo con la federal intermedia de 2021 (52.36 %).** Lo
que mueve la participación municipal no es compartir la boleta: es **qué trae la
boleta federal con la que se comparte**.

Y la prueba que no usa ninguna entidad tratada: **Zacatecas es concurrente en las
tres elecciones de su serie** y su participación agregada hace
**64.74 → 50.68 → 59.39**. Catorce puntos abajo y ocho arriba con el tratamiento
fijo en 1. Ese vaivén es del tamaño del efecto que se le atribuía a la
concurrencia, y la concurrencia no lo puede explicar.

---

## 1 · Compuerta y ARRANQUE

`Estado: GATED a MAESTRA34-L5 fusionado`, verificada **por producto**, que es lo
que el propio encargo manda:

```
$ git show origin/main:milpa/tramite-ola5-propuesta-v0.yaml | grep -n "…_encig2025\|…_envipe2025\|…_enif2024"
684:  - id: tramite.gobierno_digital.util_sin_coercion_encig2025
742:  - id: tramite.evasion_norma_envipe2025
803:  - id: dinero.ahorro.tiene_ahorros_enif2024
```

`PR #467` fusionado en `11af678`. **CUMPLIDA.** `HEAD` = `origin/main` =
`11af678`, **18 commits por delante** del `29ab80a` que el encargo declara — no es
PARO; perímetro re-derivado y las **cinco** premisas A.8 re-corridas contra el
árbol de este acto: **las cinco verdaderas**. El negativo se respaldó con un
barrido byte a byte de **2 810 archivos / 206 681 585 bytes**, no con `ugrep`
(A.13). Entorno UBUNTU (`sin_variable`, sonda INEGI `200`, `data/raw` enlazada,
368 entradas).

---

## 2 · `P0` — la tabla que no existía, y las dos trampas que trae su fuente

Detalle completo en `…-P0-tabla-tratamiento.md`. Aquí, lo que sirve fuera:

**El SICEE no está caído: esta caja está bloqueada.** `siceef.ine.mx`,
`siceen21.ine.mx`, `computos2024.ine.mx`, `portalanterior.ine.mx` y
`prep2021.ine.mx` devuelven **la misma página** del CAU del INE —403, 163 097 B—
con el texto verbatim «**Bloqueo IP: 187.13.205.53**». No es Tableau
(`ADR-278`, `ADR-280`) ni Cloudflare (`ADR-284`). `www.ine.mx` y
`repositoriodocumental.ine.mx` **no** lo sufren, y de ahí salió todo.

**Fuente elegida y por qué es primaria:** los **30 acuerdos del Consejo General
del INE** que aprueban el Plan Integral y los Calendarios de Coordinación de cada
Proceso Electoral Local, **todos los ciclos de 2014-2015 a 2024-2025**, por la
**API REST de DSpace 6.4** del repositorio documental. El encargo nombraba
SICEE/OPLE/DOF: SICEE está bloqueado, el DOF no publica fechas locales (son de
derecho estatal) y los OPLE son 32 portales; el INE co-organiza cada PEL y su
acuerdo declara, entidad por entidad, los cargos a elegir. A.7 en los 30, **0
diferencias**.

**Trampa 1 — el rótulo miente y la actividad no.** La hoja `Veracruz` del anexo
del PEL 2023-2024 declara, verbatim, «Cargos a elegir: Gubernatura, y
ayuntamientos» y **no tiene ni una actividad municipal**, mientras las 31 hojas
restantes con ayuntamientos traen todas «Campaña para Ayuntamientos». Se resolvió
**con una tercera fuente, no a ojo**: el anexo del PEL 2024-2025 contiene sólo
dos entidades, Durango y Veracruz, y Veracruz trae ahí **17** actividades
municipales. Los ayuntamientos de Veracruz son de **2025**. Leer el rótulo habría
metido al universo una elección que no existió.

**Trampa 2 — la concurrencia es una fecha, no un año.** **Chiapas votó el 19 de
julio de 2015**, no el 7 de junio (cita verbatim del acuerdo del CG de
14/oct/2015). Y se verificó A.13 que no hay más excepciones: la fecha de fin de
campaña es **una sola por ciclo** en las **30 / 32 / 32** entidades de 2018, 2021
y 2024.

**Resultado:** `data/p0-calendario-ayuntamientos-v1_0.tsv` (146 filas) y
`data/p0-tratamiento-homologacion-v1_0.tsv` (32). **14 entidades tratadas** con
antes y después (`g2018` = 8, `g2021` = 5, `g2024` = 1) y **una sola nunca
tratada**, Durango.

**Y la consecuencia que obligó a cambiar la spec antes de medir:** como en un año
federal **todas** las locales caen el mismo día, en 2018/2021/2024 **no existe ni
un municipio no tratado**. El tratamiento es colineal con el año y los efectos
fijos de año electoral que la firma proponía **no identifican nada**. La spec los
sustituyó por una tendencia lineal estimada sólo de las transiciones sin cambio
de tratamiento, y lo declaró como el supuesto principal, no como un detalle.

---

## 3 · `P1` — cobertura, contada como el encargo pide

**Cobertura: 4 entidades medibles de las 14 tratadas que `P0` identificó; 2 de
ellas tratadas.** El mínimo del encargo era ≥8, así que **`P3` corrió ACOTADO** y
así se declara.

| entidad | serie obtenida | ¿entra? | por qué |
|---|---|:--:|---|
| Coahuila | 2017, 2018, 2021 (+2024 de `L4`) | **sí** | lista nominal en la fuente |
| Nayarit | 2017, 2021, 2024 + 3 PDF de listado nominal | **sí** | el denominador vive en archivo aparte |
| Zacatecas | 2018, 2021, 2024 | **sí** | lista nominal por casilla |
| Durango | 2016, 2019 | **sí, con reserva** | el archivo de 2016 cubre **sólo la capital** |
| Aguascalientes | 2019, 2021 (22 archivos) | **no** | **ninguna tabla trae lista nominal** |
| Hidalgo | 2016, 2020, 2024 | **no** | **ninguna tabla trae lista nominal**; el 2016 es `.rar` y no hay extractor en esta caja |
| TEPJF 1991-2018 | — | **no** | `NO-OBTENIDO`, 4 rutas probadas, receta de navegador en la cola |

**43 payloads** `OBTENIDO`, A.7 en los 43 con `sha256` idéntico y **0
diferencias**. Registro por las tres capas: manifiesto **983 → 1029**, registro
del curador **84 → 92 filas** (escritas **por línea**, nunca con el módulo `csv`:
`numstat` 8 añadidas / **0 borradas**), vista regenerada con
`tools/vista_cola_adquisicion.py` (T26).

**Anti-PR#77:** los 76 payloads del acto viven en
`/home/pc0/mm-corpus/raw/electoral_calendario_pel_ine/` (33) y
`/home/pc0/mm-corpus/raw/electoral_local_municipal_serie/` (43), **no** en el
worktree. `tests/manifiesto.py --verifica`:
`data_raw: coincide=918 · no_coincide=0 · ausente=0`.

**Dos defectos de anfitrión, medidos:** `www.ieeags.mx` responde **HTTP 200 con
una página HTML** a rutas inexistentes — un archivo entró al corpus con 33 668 B
de HTML bajo un `200`, y lo atrapó `zipfile.testzip()`, **no** el código. Y el
bitstream `CGex202110-20-ap-4-Calendario.xlsx` del repositorio del INE **es un
PDF servido con extensión `.xlsx`** (`%PDF` en el byte 0): no está roto, está mal
nombrado en origen.

---

## 4 · `P2`/`P3` — la medición

Detalle en `…-P2-spec.md` (§1 spec congelada, §2-§12 resultados). Aquí, sólo el
resultado y su reserva:

| | |
|---|---|
| **`β` (efecto de la concurrencia)** | **+0.0149 pp** |
| **IC95 wild cluster por entidad** (el que la spec designó) | **[−3.3765, +3.4064]** |
| IC95 bootstrap por municipio | **[−1.3865, +1.3312]** |
| ¿cruzan cero? | **los dos, sí** |
| n | 269 obs. municipio × transición · 8 transiciones · 4 entidades |
| **`ATT` Coahuila 2017→2018 (presidencial)** | **+2.4113 pp** [+1.53, +3.28] |
| **`ATT` Nayarit 2017→2021 (intermedia)** | **−5.6914 pp** [−6.94, −4.38] |

**Controles, todos corridos antes de mirar el estimador:** reagregar casilla →
municipio en Coahuila da `|Δvotos| = 0` y `|Δlista nominal| = 0`; la `% PART`
publicada vs recalculada difiere **0.000000 pp** en los 38 municipios de 2021 y
de 2024; la suma de los 38 municipios de Coahuila 2018 reproduce **exactamente**
la fila `TOTALES` de su propia tabla; **0** municipios fuera de `(0, 100]`.

**Un defecto de fuente que sólo el control atrapa:** la tabla de Zacatecas 2024
trae dos columnas de total. `T VOTARON` dice «Sin Dato» en **839 de 2 649
casillas (31.7 %)**, en 29 de 58 municipios; `VTOTAL` está en 2 646 y cumple
`Σ(partidos) = VTOTAL` en **todas**. Se usó `VTOTAL`. Con la otra, medio
Zacatecas se habría hundido sin aviso.

**Dos reservas, las dos escritas antes de medir y no movidas después:**

1. Con **4 conglomerados**, el wild cluster de Rademacher tiene `2⁴ = 16`
   patrones de signo y su **`p` mínimo alcanzable es 0.125**: no podía rechazar
   al 5 % pasara lo que pasara. El veredicto se sostiene porque el bootstrap por
   municipio —que no sufre eso— **también** contiene cero, con un intervalo
   cuatro veces más estrecho.
2. La spec avisó en `§1.10` que no separaría la concurrencia de un choque
   nacional coincidente con los años federales **no capturado por una tendencia
   lineal**. Los resultados muestran que ese choque **existe, es grande y no es
   lineal**: es el ciclo presidencial/intermedia. La `γ` lineal lo absorbe mal y
   por eso `β` pooled es inestable (sin Coahuila, `−5.69`). **El acto reporta el
   número que su procedimiento congelado produjo y declara el defecto del
   procedimiento en vez de cambiarlo después de ver el resultado.**

---

## 5 · `P4` — propuesta a mesa, en formato RH. **Redactada, no ejercida.**

Registrada como **`FP-239`** en `forense/firmas-pendientes.tsv`.

> ### Qué número, y contra qué benchmark
>
> El efecto de que la elección municipal comparta día con la federal, medido con
> variación escalonada en 4 entidades, es **+0.01 pp**, con IC95 de
> **[−1.39, +1.33]** por municipio y **[−3.38, +3.41]** por entidad. **Cero, y con
> precisión suficiente para excluir tanto el ≈+10 pp alemán (Leininger, Rudolph y
> Zittlau 2018) como el +36 pp estadounidense (Hajnal y Lewis 2003).** El
> benchmark nacional del TEPJF queda `NO-OBTENIDO` y **no se cita de memoria**.
>
> El número **no** dice que la participación municipal no se mueva: se mueve
> hasta 14 pp entre elecciones. Dice que **no se mueve por compartir la boleta**.
> Lo que la mueve, y esto es lo que el diseño escalonado permitió ver por primera
> vez, es **si la boleta federal trae presidencia**: `+2.41 pp` cuando la
> concurrencia es con presidencial, `−5.69 pp` cuando es con intermedia.
>
> ### Qué firma cargaría al motor, y cómo se convertiría a probabilidad
>
> **Ninguna, y la recomendación es explícita.** La dirección proponía que el
> motor consuma «participa» como tasa base municipal más un `Δ` por concurrencia.
> **La segunda mitad de esa propuesta ya no tiene sustento**: el `Δ` por
> concurrencia acaba de quedar refutado como causal, y cargarlo sería cargar el
> defecto. La primera mitad —una **tasa base municipal** de participación— sí
> tiene dato (§3 de la spec, 12 celdas entidad × año), pero **este acto no la
> propone**: es una decisión de modelo, y convertir una tasa observada en la
> probabilidad de un agente segmentado es exactamente la conversión que
> **firma mesa, no el acto**.
>
> ### Qué decidir, en tres piezas
>
> **(a)** Aceptar o no el veredicto **`REFUTADA-COMO-CAUSAL`** y el tier de la
> entrada nueva (propuesta: `PENDIENTE-DE-MESA`, sin carga).
> **(b)** Qué pasa con la entrada de `MAESTRA34-L4`, que **este acto no editó**:
> hoy dice tier `MEDIA`, situación `APARCADA-HASTA-IDENTIFICACION`, por firma
> `DC1-d`. Su sucesora la contradice. Moverla es de mesa.
> **(c)** Autorizar el sucesor con **el diseño corregido**: sustituir la
> tendencia lineal por un **efecto fijo de tipo de año federal** (presidencial /
> intermedia / sin federal), y adquirir las **12 entidades tratadas** que `P1` no
> alcanzó. **Primera prioridad, y es barata: Hidalgo.** Es la única cohorte
> `g2024`, tiene **dos huecos de 4 años iguales** (2016 → 2020 no concurrente,
> 2020 → 2024 concurrente) sobre los **mismos 84 municipios**, y es por eso el
> caso más limpio de todo el diseño. Sus tres tablas de cómputos **ya están en el
> corpus**; lo único que falta es el **denominador**, porque ninguna trae lista
> nominal.

---

## 6 · Contador

| | antes | después |
|---|---|---|
| payloads en `data/manifiesto.yaml` | 953 | **1029** (+76) |
| filas del registro de la cola | 84 | **92** (+8) |
| entidades con calendario de tratamiento de fuente primaria | 0 | **32** |
| entidades tratadas identificadas | 0 | **14** |
| entidades con serie municipal medible | 0 | **4** (2 tratadas) |
| **reglas con `Δ` identificado** | 0 | **+1** (`civico.participacion.contingente`) |
| firmas nuevas | — | **+1** (`FP-239`) |
| cargas al motor | 0 | **0** |
| corridas de Hito D | — | **0** |

Hito D **sin movimiento**: esto no es una corrida de falsador de Hito D. Es el
ejercicio del falsador `B-bis` que la propia spec de este acto congeló, y su
veredicto se propone a mesa, no se archiva.

## 7 · A.13 por pieza

| pieza | qué examinó, contado |
|---|---|
| A.8 | **2 810 archivos / 206 681 585 bytes** leídos byte a byte (sin `ugrep`), 18 884 líneas de `data/manifiesto.yaml` |
| `P0` | **30** payloads, **14** ciclos de PEL, **146** filas entidad × jornada, **32** entidades; fin de campaña contado en **30 / 32 / 32** entidades de 2018 / 2021 / 2024 |
| `P1` | **43** payloads con A.7 (86 descargas) + 3 de negativo documentado, **41** contenedores verificados + 2 `.txt`; **15** portales de OPLE sondeados, **5** hosts del INE probados |
| `P3` | **269** observaciones municipio × transición, **8** transiciones, **4** entidades, **116** municipios distintos; **2 509** casillas de Zacatecas 2018, **2 649** de 2024, **2 488** de Durango 2019, **1 096** de Durango capital 2016 |
| suite | `tests/check.py --baseline` → **VERDE** (19 FAIL · 167 WARN, nada nuevo) |
