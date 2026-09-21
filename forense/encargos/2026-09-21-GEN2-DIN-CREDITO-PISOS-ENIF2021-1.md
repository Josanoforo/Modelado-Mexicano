# ENCARGO · ACTO `GEN2-DIN-CREDITO-PISOS-ENIF2021-1` · al cerrar, cada conducta de crédito de la serie tiene piso medido en 2021, con el mismo marco que el piso de ahorro

> ENTORNO: **CAJA** — el hook de arranque imprime `ENTORNO-DERIVADO`. Si no dice `CAJA`, PARA en una línea. Este acto abre microdato de ENIF **2021** y de ninguna otra ola.

**CABECERA** · SHA de redacción `04a2edeb`; re-deriva al abrir y si main se movió no es PARO · **una sola sesión, rama propia** · **MODELO: Opus** (mide; D-13 prohíbe bajar) · **MODO: ABIERTO hasta el COMMIT-1, RÍGIDO desde el COMMIT-2** — congelada la spec, la latitud es sobre logística y nunca sobre el procedimiento, y «el código congelado no corre» es PARO (g), no se parcha · **CONTADOR: `cuenta_gen2 = SI`**, firmado por mesa con objeto (§2). Cuenta, **no adopta**: ningún `adoptados_activos` debe moverse · **CALC-id reservado:** `CALC-DIN-CREDITO-PISOS-ENIF2021-0001` · **FP/ADR/NC:** deriva al cierre, no heredes.

---

## 1 · OBJETIVO

Medir en **ENIF 2021** las proporciones marginales de las conductas de crédito **K1–K7** por los ejes de segmento del marcador, reutilizando el marco ya sellado del piso de ahorro 2021, para que cada celda de crédito deje de nacer `SIN-PISO`.

Hoy el dominio crédito **no tiene un solo piso**: sin marginales de 2021 no hay piso de persistencia para 2024, y sin piso no hay nada que acote a los retadores. Este acto es el cuello de botella del dominio.

**«Hecho» significa:** `CALC-DIN-CREDITO-PISOS-ENIF2021-0001` sellado, `verify` → `REPRODUCE`, un `RESULT` por celda y por cantidad (punto, IC95 inferior, IC95 superior, n sin ponderar, masa ponderada), la unidad declarada por conducta, el control de coherencia de §5 P4 en verde, y **la corrida registrada sin `envuelto_legacy`** (si el registro la marca así al regenerar, el contador baja a NO y el objetivo no se cumplió). Más nota, filas propias en la vista y su asiento de replay, y la cascada de `/acto`.

---

## 2 · FIRMAS DE MESA — verbatim

**LANZAMIENTO · FP-404** (mesa, 21/sep/2026) — «(1) K8 "destino del último crédito" sale de la serie ENIF: no tiene instrumento en 2021 ni 2024 y en 2012–2018 solo 2018 está verificado por texto. Opción (i): se triangula en ENSAFI 2023 / ENFIH 2019 en acto propio; no se construye serie 2012–2018. (2) K2 familia bancaria: opción (iii) para la serie —no se compara 2021↔2024, es CAMBIO-DE-INSTRUMENTO— y (i) rotulado para el descriptivo. La cifra del corpus "bancaria +5.2 pp desde 2021" no se cita sin esa frontera.» — «FP-404 queda FIRMADA: el alcance del encargo es el que trae escrito; nada queda pendiente.»

**FIRMA DE CONTADOR** (mesa, 21/sep/2026) — «`cuenta_gen2 = SI` para `CALC-DIN-CREDITO-PISOS-ENIF2021-0001`; cuenta, no adopta.»

**NOTAS DE DIRECCIÓN** (21/sep/2026), a verificar antes del COMMIT-1 — «a) `formalidad` en ENIF 2021: la contradicción entre specs selladas ya tiene regla — ENLACE-2 (#925): si dos tablas hablan de la misma celda manda la más reciente y se dice en la fuente. La spec PISOS-ENIF2021-formalidad (#915) y el dictamen de #908 (3.13 de 2024 = 3.10 de 2021) suceden a la fila de la rejilla (#871). Cítalo; no lo re-dictamines. Universo: quien trabaja.» — «b) Si el medidor lee la rejilla de categorías de `milpa/tramite-ola5-propuesta-v0.yaml`, el registro marcará la corrida `envuelto_legacy` y bajará `cuenta_gen2` a NO al regenerar (caso FP-395/396/397). Lee la rejilla de la tabla de identidad GEN2 de pisos (`forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` y la de formalidad), o declara por qué no se puede.» — «ENIF 2024 no se abre en este acto, ni su sección de crédito ni ninguna otra.»

**RESERVA** (20/sep/2026) — «La sección de crédito de ENIF 2024 queda RESERVADA desde hoy, con el hueco declarado: el par "crédito por app" (n=200) está visto y consumido; no se relanza sobre él.»

**D2** (20/sep/2026) — «2018 entra a la serie de crédito solo donde el texto de la pregunta lo permita; se acepta por adelantado que varias conductas cierren NO-CONSTRUIBLE en 2018, con la cita del texto buscado (A.15).»

**ORDEN** (20/sep/2026) — «Primero el encargo de comparabilidad por texto de crédito. El piloto de ahorro después.» Este acto es su sucesor 1.

---

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo

- `[LEÍDO]` `forense/prereg-caja/PISOS-ENIF2021-ejes-spec-v2_1.md` (`sha256 38b38baa865a545ec347641591032d6bcf9160c9dad6f3c1ded9b228991ebfea`, 21 líneas, leídas todas): el marco del piso de ahorro 2021 es **`FAC_ELE`, `EST_DIS × UPM_DIS`, 10 000 remuestras `PCG64(42)`, un solo plan de réplicas compartido por todos los desenlaces y todas las celdas**. **Ese marco es el que este acto reutiliza**, con el desenlace cambiado.
- `[LEÍDO]` **`formalidad` en 2021 está resuelta y no se re-dictamina.** La regla es la de **`GEN2-MARCADOR-ENLACE-2` (#925)** —ojo, no el acto `ENLACE-2` del 14/ago sobre `capa2`, que comparte nombre y no tiene que ver—: `forense/notas/2026-09-20-GEN2-MARCADOR-ENLACE-2-cierre.md`, líneas 57, 60 y 71. `TABLAS_IDENTIDAD` se lee en orden cronológico de sello, **manda la más reciente**, la fuente lo dice con `SUCEDE-A:<cell_id>`, y lo prueba `T-PRECEDENCIA`. `PISOS-ENIF2021-formalidad-spec-v1_0.md` (`sha256 50b471e3e0521336…`) cita el dictamen de #908 en sus líneas 8 y 29. **Universo del eje: quien trabaja** (`P3_10 ∈ 1..6`). Que la spec de ejes v2.1 diga `NO-CONSTRUIBLE` es la fila sucedida, no una contradicción viva.
- `[LEÍDO]` **La rejilla sale de la tabla de identidad GEN2, no del trámite.** `forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` (`sha256 1715da9303957dac…`, 32 filas que mencionan ENIF 2021; columnas `cell_id · input_id · outcome · source_instrument · source_edition · … · axis · category · status · reason · consumer · metadata_source · metadata_source_sha256`) y, para formalidad, `PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv` (`sha256 8cf59f8ba487ac35…`). `FP-395`, `FP-396` y `FP-397` son los tres casos en que un CALC leyó de otro sitio y el registro le bajó `cuenta_gen2` a NO.
- `[LEÍDO]` `data/credito-comparabilidad-texto-v1_0.tsv` (40 filas, `ACTO GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1`, `PR #932`): **de ahí salen el reactivo, el texto, los códigos, el filtro, la unidad y la población base de cada conducta en 2021.**
- `[LEÍDO]` misma tabla, fila `K4 · 2021`: la base de K4 es **«nunca ha tenido»**, no «no tiene hoy» — los ex-usuarios sin crédito hoy caen fuera de `P6_15` y tienen su propia partición en `6.16`.
- `[LEÍDO]` misma tabla, fila `K7 · 2021`: K7 es **`PR`** (último crédito, una observación por persona con producto formal), y el instrumento no dice cuál producto es «el último».
- `[EJECUTADO]` `data/corrida0/marcador-segmento.tsv`: **ninguna fila es de crédito.** El dominio entra sin piso.
- `[EJECUTADO]` `ls data/corrida0 | grep -iE "cred|deuda|prest|moros"` sobre 187 entradas: ningún CALC mide crédito con microdato de ENIF a nivel persona.
- `[SUPUESTO]` que `EST_DIS`, `UPM_DIS` y `FAC_ELE` están en el `TMODULO` de 2021 con la misma ortografía que la spec de ahorro. **Si resulta falso**, manda el header del archivo, se declara y se sigue: no es PARO.
- `[SUPUESTO]` que la rejilla de identidad cubre todos los ejes que K1–K7 necesitan en 2021. **Si resulta falso para alguno**, ese eje no se inventa: se declara por qué no se puede, como pide la nota b), y los demás se miden.
- `[REPORTADO]` de los reportes del corpus, como hipótesis y nunca como control: ~37.3% con crédito formal, departamental 22.6% > bancaria 15.7%, «no le gusta endeudarse» 38.4%. **Ninguna valida ni invalida una medición.** La cifra «bancaria +5.2 pp desde 2021» no se cita, por `FP-404`.

---

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO

Busqué el objeto **«marginales de crédito de ENIF 2021 a nivel persona»** y el objeto **«piso de crédito en el marcador»**.

| dónde | universo | resultado |
|---|---|---|
| `data/corrida0/` | 187 entradas | `EXISTE-NO-SATISFACE` — cuatro CALC de pisos ENIF 2021, los cuatro de **ahorro** |
| `forense/prereg-caja/` | 100 specs humanas | `EXISTE-NO-SATISFACE` — el marco y la rejilla de 2021 existen; ninguno cubre conductas de crédito |
| `data/corrida0/marcador-segmento.tsv` | 216 filas | `NO-ENCONTRADO` — cero filas de crédito |
| `forense/no-corrido.tsv` | 435 NC | `NC-0433` (2012/2015 sin cuestionario) apunta a adquisición, no aquí |

**Al ejecutor: repítela con tu acceso.** Si algo ya cubre una conducta de crédito, el entregable es decirlo y medir sólo lo que falte.

---

## 5 · PIEZAS — resultado esperado, no receta

**P1 · Alcance cerrado, leído de la tabla.** Entran **K1, K2 (familias departamental, nómina y automotriz), K3, K4, K5, K6, K7**. **No entran, por `FP-404` firmada:** K8 —sale de la serie ENIF y se triangula en acto propio— y la familia **bancaria** de K2 —fuera de la serie; su descriptivo rotulado no es de este acto. *Queda bien si*: el reactivo, los códigos, el filtro y la unidad de cada conducta se citan **desde `data/credito-comparabilidad-texto-v1_0.tsv`**, con la fila de la que salen. Ningún identificador de variable se teclea desde este encargo.

**P2 · `formalidad` se cita, no se decide.** El eje entra con la definición de `PISOS-ENIF2021-formalidad-spec-v1_0.md` y el dictamen de #908 (`3.13` de 2024 = `3.10` de 2021), universo **quien trabaja**, bajo la regla de precedencia de `GEN2-MARCADOR-ENLACE-2`. La spec nueva lo dice con la cita. **Ninguna spec sellada se edita.**

**P3 · COMMIT-1 · la spec y el medidor, congelados antes de abrir `TMODULO` 2021.** «El primer resultado que produzca este procedimiento es el que se reporta.» La spec declara: estimando por conducta **con su unidad** (`P` o `PR`) y su base poblacional —K4 sobre «nunca ha tenido», dicho así—; universo; los ejes y sus cortes; el método de IC; y el criterio de soporte. Hereda verbatim del marco de ahorro `FAC_ELE`, `EST_DIS × UPM_DIS`, 10 000 remuestras `PCG64(42)` y **un solo plan de réplicas compartido por todas las conductas y todas las celdas** — es lo que hace conmensurables los pisos de crédito y de ahorro, y no se cambia. **D-22: el punto de entrada corre sobre un payload sintético antes de congelarse**, y la spec declara sobre qué corrió. Una ejecución diagnóstica se declara **antes** de correrla o cuenta como primer resultado.

**P4 · COMMIT-2 · medir, con tres guardias cuya consecuencia vive en un solo sitio (la spec) y en ninguna otra parte.**
1. **Unidad.** K7 es `PR` y K6 es `PR` agregable; sus proporciones **no se promedian ni se suman** con las de las conductas `P`. Una tasa de personas y una de productos no se comparan sin función de enlace (A-bis 3). Consecuencia declarada: emitir a la unidad de la fila; si el medidor las mezclara, **PARA**.
2. **Soporte.** Celda con `n` sin ponderar por debajo del piso de la casa → se emite rotulada, **no se colapsan categorías para rescatarla**. Consecuencia declarada: rótulo, no exclusión silenciosa.
3. **Coherencia.** Los marginales que salgan de agregar las celdas de un eje deben reproducir el marginal nacional de la misma conducta a tolerancia de redondeo. Consecuencia declarada: si no, **PARA** — dice si el denominador se movió sin que nadie lo notara. Para `formalidad`, cuyo universo es quien trabaja, el control se hace contra el marginal nacional **de ese universo**, no del de 18+.

**P5 · La rejilla sale de la tabla de identidad GEN2, nunca del trámite.** Cortes, categorías y metadatos de cada eje se leen de `PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` y, para formalidad, de `PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv`, citados con su `sha256`. **El medidor no lee `milpa/tramite-ola5-propuesta-v0.yaml` ni ningún otro archivo del trámite**: si lo hace, el registro marca la corrida `envuelto_legacy` y el contador firmado baja a NO (`FP-395/396/397`). *Rama prevista*: si un eje o una categoría no está en la tabla de identidad, se declara por qué no se puede y esa celda sale acotada; no se inventa el corte.

**P6 · Lo que el piso deja dicho.** Al cerrar, una tabla corta: por conducta y eje, si hay piso, con qué `n` y qué anchura de IC. Es lo que el piloto de crédito va a usar para saber dónde un retador tiene margen, y es lo único de este acto que viaja hacia adelante.

---

## 6 · LATITUD

**Decides tú, y lo dices en la nota:** el orden de las piezas · la organización del medidor · nombres de archivo · enlazar o crear `data/raw` · instalar una dependencia · regenerar un derivado por comando · arreglar un defecto adyacente de ≤ 10 líneas que te impida terminar, declarándolo.

**Preguntas a mesa con 2–3 opciones y recomendación, y sigues con lo demás:** cualquier bifurcación que cambie qué conductas o qué ejes entran.

**No decides:** nada de §7, ni el alcance de P1, que está firmado.

---

## 7 · PAROS — lista cerrada

- **(a)** Abrir, derivar o imprimir **cualquier** miembro de datos de **ENIF 2024** —su sección de crédito y cualquier otra—. Este acto vive en 2021 y nada más.
- **(b)** Borrar, forzar (`-D`, `--force`, `clean`) o reescribir algo sellado. Las specs y tablas de pisos de ahorro y de identidad **no se editan**.
- **(c)** Adoptar cualquier cosa, o mover un contador distinto del firmado.
- **(d)** Cambiar estimando, universo, umbral o código de un procedimiento congelado — incluido el propio, desde el COMMIT-2.
- **(e)** `ENTORNO-DERIVADO ≠ CAJA`.
- **(f)** El objetivo dejó de ser alcanzable, y eso es el entregable.
- **(g)** Desde el COMMIT-2: **el código congelado no corre → no se parcha.** El sucesor es un COMMIT-1 v1.1 de otra sesión. Esto mató al piloto 3.

---

## 8 · COMPUERTAS

**«`spec.yaml` y medidor congelados, con su sidecar verificado y el `ejecutado_al_congelar` declarando sobre qué payload sintético corrió» protege: abrir dato.** Sin eso no se toca `TMODULO` de 2021.

Lo demás en este encargo es orden sugerido, no compuerta.

---

## 9 · PERÍMETRO

**Propio:** `data/corrida0/CALC-DIN-CREDITO-PISOS-ENIF2021-0001/` (spec, medidor, sello, resultados) · su spec humana en `forense/prereg-caja/` con sidecar · filas propias en `corridas.tsv`, `resultados.tsv` y `replay-evidencia.tsv` · su test y el cableado en CI · nota de cierre · NC y FP propias · `forense/hallazgos.md` · **la fila `FP-404` de `forense/firmas-pendientes.tsv`, que pasa a `FIRMADA` con el PR de este acto (A.12)** · el archivo verbatim de este encargo con su `sha256` (0-bis, A.3) · la cascada de `/acto`.

**Ajeno, no se toca y por qué:** las specs, CALC y tablas de identidad de pisos de ahorro de ENIF 2021 — son la referencia, no el objeto · `milpa/` entero — ni se escriben reglas ni se lee la rejilla de ahí · `data/corrida0/marcador-segmento.tsv` y `data/curacion-registro/celdas-d/` — perímetro de DIRECCIÓN · `data/credito-comparabilidad-texto-v1_0.tsv` — se lee, no se edita · el sidecar roto de `#932` — es de TUBERÍA · ENIF 2024 · ENIGH, ENSAFI y ENFIH.

**Perímetro de cierre, permanente (D-21):** test en CI · filas propias publicadas en la vista **en el mismo acto que las sella** (E.7) · asiento de replay · `## NO-CORRIDO / RESERVAS` con «Ninguno.» obligatorio si no hay, antes de `## CONSUMIDO`.

**«Si te encuentras escribiendo fuera de esta lista, PARA.»**

---

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE

**No hace:** no abre 2024 · no adjudica ninguna celda ni corona ningún candidato · no escribe reglas en el motor · no mide K8 ni la familia bancaria · no produce el descriptivo rotulado de bancaria · no toca el piloto de ahorro ni elige su cruce · no adquiere nada.

**Sucesores, en orden:**
1. La **regla de elección del cruce** del piloto de ahorro, que escribe dirección cerrando los dos huecos de ENCIG: la consecuencia de cada guardia en un solo sitio, y `congelado` sólo si el punto de entrada ya corrió (D-22).
2. El **piloto de crédito**: con este piso en mano, congelar la predicción para 2024 con su regla de adjudicación y su B-bis, y sólo entonces abrir 2024.
3. **K8 triangulada** en ENSAFI 2023 / ENFIH 2019, en acto propio y rotulada como triangulación, no como serie (`FP-404` (1)).
4. **Descriptivo rotulado de K2-bancaria** con su frontera 2021↔2024 declarada (`FP-404` (2)).
5. Adquisición de los cuestionarios de ENIF 2012 y 2015 (`NC-0433`) → mesa → NUBE-MEDICIÓN.

**Auditoría (§5 de las instrucciones), completa porque este acto sí afirma sobre México.** Tres líneas obligatorias en la nota. (1) **Lo que parece psicológico y es oferta:** una tasa baja de crédito formal en un segmento no dice nada sobre su preferencia mientras K4(b) y K5 —requisitos y rechazo— no se lean al lado; el piso se publica con esa advertencia pegada. (2) **Sobregeneralización:** ENIF es población de 18+ en viviendas y sobre-representa al urbano bancarizado; el eje `formalidad` además se restringe a quien trabaja. Un marginal leído ahí no es «el mexicano», es esa población. (3) **Escala:** cada cantidad sale con su unidad, `P` o `PR`, y no se compara con otra escala sin función de enlace — y el piso de crédito **no** se compara contra el de ahorro salvo por signo y razón dentro de la misma corrida.

**Cierre:** cascada de `/acto` · primera línea de la nota: universo, unidad, escala y clase de evidencia.

---

**Falsador de este encargo, a tres meses:** si el piloto de crédito tiene que re-medir algún marginal de 2021 que este acto ya selló, el piso no sirvió y se revisa su diseño de celdas.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Perímetro de cierre (D-21): enlazar la tabla de identidad propia (`forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-metadatos-v1_0.tsv`) a `TABLAS_IDENTIDAD` de `tools/marcador_segmento.py` y re-derivar `data/corrida0/marcador-segmento.tsv` | `FUERA-DE-PERÍMETRO` — de DIRECCIÓN: §9 de este encargo declara `data/corrida0/marcador-segmento.tsv` y `data/curacion-registro/celdas-d/` perímetro de dirección; además el árbitro 2024 no tiene reglas de crédito que consuman estas celdas (`consumer = PENDIENTE:piloto-credito-2024`) y añadirla daría `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD` | `sin_piso` del marcador no baja por crédito todavía (0 de 216 filas son de crédito); el piloto de crédito lee el piso del CALC y de la tabla | `NC-0447` · `SIN-ASIGNAR` (piloto de crédito, sucesor 2 de §10) |
| Reserva: `registro --verifica --escribe` nombró en `--lote` la corrida ajena `CALC-ENIF-0001--afbf3c76d71b` | no es pieza no corrida: su `contexto_replay` pasa `IDENTICO→DISTINTO` porque el asiento NUBE de `#935` (`cf1ba17f`, `forense/replay-evidencia.tsv:148`) ya estaba en `origin/main` sin proyectar; `verify` en esta CAJA sigue IDENTICO. Declarado en la nota §2 y en `forense/hallazgos.md`; ninguna otra fila ajena cambió | ninguno sobre contadores propios | — |

## CONSUMIDO

Ejecutado por `PR #943` (`acto/gen2-din-credito-pisos-enif2021-1`, 20/sep/2026, CAJA): COMMIT-1 `ad93b0b3`, COMMIT-2 `56dc64ca`, cascada `ADR-577`; `CALC-DIN-CREDITO-PISOS-ENIF2021-0001` sellado, `cuenta_gen2 = SI`, `envuelto_legacy = NO`; `FP-404` FIRMADA; `NC-0447`. Nota: `forense/notas/2026-09-20-GEN2-DIN-CREDITO-PISOS-ENIF2021-1-cierre.md`.
