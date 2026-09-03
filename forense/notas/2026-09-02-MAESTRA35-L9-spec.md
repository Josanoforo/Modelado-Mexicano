# `ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3` — spec congelada (`COMMIT-1` del lote, `D-11`)

> | | |
> |---|---|
> | **ACTO** | `MAESTRA35-L9 · REGLAS-ACTIVOS-L3` |
> | **ENCARGO** | `forense/encargos/2026-09-02-MAESTRA35-L9-REGLAS-ACTIVOS-L3.md` (A.3), SHA de redacción `9cbd8d8` |
> | **CENSO PREVIO** | `forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md` + `data/l9-censo-a4-v1_0.tsv` (commit `418a22f`) |
> | **QUÉ ES** | La spec de las cinco piezas y el pre-registro `B-bis` de las seis reglas, **congelados antes de cruzar nada contra el desenlace**. |
> | **PRECEDENTE DE FORMA** | `MAESTRA35-L1` (`forense/notas/2026-09-02-MAESTRA35-L1-spec.md` §1.1–§1.3) — vocabulario de veredicto, precedencia y tramos se heredan verbatim, no se reinventan. |

---

## §0 · Premisas

### 0.1 · Qué mide este lote y qué no

Las seis reglas son del **modelo** (`canon/modelo-decision-v4_0.md` §7), no del
motor: el censo verificó que **ninguna de las seis está cargada** en
`milpa/tramite.yaml` y que la propuesta de ola 5 no tiene ninguna entrada de
estas familias. Este acto les da **un dato**, que entra al **pie de
`milpa/tramite-ola5-propuesta-v0.yaml`** con `situacion/tier
PENDIENTE-DE-MESA`. **No carga al motor.** No abre Ola 6 (`ADR-265` vigente).

### 0.2 · Dos de las seis ya tienen veredicto de Hito D archivado, y esto no lo toca

`R7.3` está archivada en fila **`C`** (`ADR-155`) y `R7.4` en fila **`D`**
(`ADR-158`). Las otras cuatro (`R7.6`, `R7.7`, `R7.8`, `R1.5`) están **fuera del
perímetro de 27** y no tienen ficha (`canon/modelo-decision-v4_0.md:735,762-766`).

Este acto **no re-abre ninguna de las dos filas archivadas y no propone
cambiarlas**. Lo que produce es de otra clase y sobre otra unidad:

- El `C` de `R7.3` dice que **el RDD que su falsador exige** no es construible
  con ninguna fuente pública en disco. Aquí no se construye ningún RDD: se
  estima una **asociación descriptiva** entre transferencia recibida, secreto
  percibido e intención de voto, sobre la persona.
- El `D` de `R7.4` dice que **ninguna de las tres fuentes de EVENTO** adquiridas
  (Mass Mobilization, UCDP, GDELT) codifica entorno y forma de respuesta sobre
  el mismo caso. Aquí la unidad no es el evento sino la **persona
  auto-reportada** en una encuesta con diseño muestral, que es un instrumento
  que aquel falsador no examinó porque no servía para su pregunta (protesta
  *vs* autodefensa) — y sigue sin servir para ella: esta pieza **no dice nada
  sobre `R7.5`** ni sobre la rama de autodefensa.

Quien lea las cifras de este acto como una revisión de esas dos filas las está
leyendo mal. La distinción se repite en las entradas de la propuesta.

### 0.3 · Contaminación declarada (`ADR-46`)

Está escrita en el censo (`P0` §0) y no se repite: esta sesión leyó estructura,
catálogos de valor y **marginales univariados** de los seis payloads, más los
**denominadores** de los ejes; **no** leyó ninguna tabla cruzada del desenlace
contra el moderador. Esta spec se congela con lo primero y sin lo segundo.

### 0.4 · Alcance, declarado como falta

Todo lo de abajo son **asociaciones dentro de una corrida** (`A-bis` 1–4). No
son efectos causales, no hay diseño de identificación y **no se ajusta por
ninguna covariable**: las celdas son proporciones dentro de subgrupos definidos
por el eje. La escala va declarada en cada entrada de la propuesta.

### 0.5 · Guardias de lectura, congeladas con valor esperado (antes de correr)

Un lector nuevo devuelve vacío, no error. Cada medidor **PARA** si alguna de
estas no se cumple exactamente:

| guardia | valor esperado |
|---|---|
| LAPOP 2019 · filas | 1 580 |
| LAPOP 2019 · `clien1na` válidos / «sí» | 1 578 / 271 |
| LAPOP 2019 · `prot3` válidos / «sí» | 1 576 / 112 |
| LAPOP 2023 · filas | 1 622 |
| LAPOP 2023 · `mexwf1_19` válidos / «sí» | 1 615 / 363 |
| LAPOP 2023 · `countfair3` válidos | 1 542 |
| ENCUCI 2020 · filas sección 6 · emparejadas con diseño | 21 519 · 21 519 (0 sin par) |
| ENCUCI 2020 · `AP6_9` marginal | 1: 8 685 · 2: 12 183 · 3: 299 · 9: 352 |
| ENIF 2024 · filas `TMODULO` | 13 502 |
| ENIF 2024 · `P5_23` marginal | 1: 4 136 · 2: 9 366 |
| ENIF 2024 · universo `P5_20` | 2 970 |

---

## §1 · Reglas comunes a las cinco piezas

### 1.1 · Estimador

**Proporción ponderada** dentro de cada celda. **IC95 por bootstrap de
conglomerado, 10 000 réplicas, `seed = 42`**, remuestreando **UPM con reemplazo
dentro de cada estrato** — nunca personas: remuestrear personas ignora el efecto
de diseño y estrecha el IC de mentira. Un estrato con una sola UPM entra tal
cual y se cuenta aparte. Percentiles 2.5 / 97.5.

Para **diferencias** entre dos ramas del mismo eje, el remuestreo de UPM es
**el mismo para las dos ramas** en cada réplica: comparten estrato y UPM, y
tratarlas como independientes sobreestima la varianza de la diferencia (mismo
argumento que `tests/svystat.py::diff_ultimate_cluster` hace en su versión
analítica).

**Control de regresión:** cada proporción principal se recalcula además con
`tests/svystat.py::prop_ultimate_cluster` (linealización). Si el punto no
coincide byte a byte, **PARA**: el bootstrap y la linealización tienen que dar
el mismo `p_hat`, sólo el IC puede diferir.

### 1.2 · Ponderador y diseño, por fuente

| fuente | ponderador | estrato | UPM |
|---|---|---|---|
| LAPOP México 2019 | `wt` — **CONSTANTE = 1** | `estratopri` (4) | `upm` (129) |
| LAPOP México 2023 | `wt` — **CONSTANTE = 1** | `strata` = `estratopri` (4) | `upm` (130) |
| ENCUCI 2020 | `FAC_SEL` | `EST_DIS` (281) | `UPM_DIS` (3 096) |
| ENIF 2024 | `FAC_PER` | `EST_DIS` (190) | `UPM_DIS` (2 164) |

**Declaración que no se puede omitir al citar las cifras de LAPOP:** `wt` es
constante en las dos olas mexicanas, así que **«proporción ponderada» ahí es
idéntica a la proporción simple**, y todo el efecto de diseño vive en el
conglomerado. No es un defecto del cálculo: es cómo LAPOP publica el archivo de
país. Se dice ahora para que nadie lo lea después como un ponderador que se
olvidó de aplicar.

### 1.3 · Tope de ejes y cobertura

- **Cinco ejes por pieza, cuatro celdas por eje** (`A-bis`).
- **Cobertura < 90 % ⇒ universo restringido (`A-bis 4`)** para ese eje: sus
  celdas **no** se reconcilian contra ningún marginal poblacional.
- **Guardia de celda:** una celda con **numerador < 10** se reporta
  `NO-ESTIMABLE`, con su `n`, y **no participa de ningún veredicto**. Que la
  variable exista no es que la `n` alcance.

### 1.4 · Vocabulario de veredicto por eje y su precedencia *(verbatim de `L1 §1.1`)*

- **`CORROBORADA`**: las celdas extremas van en el signo esperado y sus IC95 **no
  se traslapan**.
- **`NO-DISCRIMINA`**: los IC95 de las celdas extremas se traslapan.
- **`DISCRIMINA`**: los IC95 no se traslapan, pero el eje no traía signo
  pre-registrado (o el signo no es evaluable).
- **`CONTRARIA`**: van en signo opuesto al esperado, sin traslape.
- **Precedencia:** `CONTRARIA` manda sobre `CORROBORADA` cuando un mismo eje da
  ambas en tramos distintos; se reporta además como **no monótono**. «Tramos
  distintos» se recorre como **pares consecutivos** en el orden declarado del
  eje (operacionalización fijada por `L1` en su commit de resultados).

### 1.5 · Tramos de escolaridad *(consistentes con `L1 §1.2`)*

| tramo | ENIF 2024 (`NIV`) | ENCUCI 2020 (`NIV`) |
|---|---|---|
| hasta primaria | `00,01,02` | `00,01,02` |
| secundaria | `03` | `03` |
| media superior | `04,05,06,07` | `04,05,06,07` |
| superior | `08,09,10,11` | `08,09` |
| **fuera** | `99`, blanco | blanco |

Tramos de edad: `18-29 · 30-44 · 45-59 · 60+`.

---

## §2 · Pieza (a) · `R7.7` — la dádiva compra asistencia, no elección

**Fuente:** LAPOP México 2019 (`mexico_lapop_americasbarometer_2019_v1_0_w`).
**Unidad:** persona de 18+. **Elección de referencia:** la general de **2018**,
la misma en los tres ítems.

**Tratamiento (eje principal):** `clien1na` — «Le ofrecieron un beneficio por su
voto en la última elección generales». `1 = Sí` (271) · `2 = No` (1 307).

**Dos piernas, una corrida.** La regla afirma una **separación**, así que las
dos se estiman juntas y el veredicto sale del par, no de una sola:

- **Pierna ASISTENCIA.** Universo: `clien1na ∈ {1,2}` y `vb2 ∈ {1,2}`.
  Desenlace `y = 1` si `vb2 = 1` (votó).
  Estimando: `Δ_asistencia = P(votó | ofrecieron) − P(votó | no ofrecieron)`.
- **Pierna ELECCIÓN.** Universo: los anteriores **que además votaron**
  (`vb2 = 1`) y con `vb3n` válido.
  Desenlace **principal** `y = 1` si `vb3n = 103` (**PRI**, el partido que tenía
  el gobierno federal en 2018 y la maquinaria clientelar clásica).
  Desenlace **secundario, también pre-registrado aquí** `y = 1` si `vb3n = 101`
  (**MORENA**, el ganador). Los dos se congelan ahora para que la elección de
  cuál mirar no dependa del resultado.
  Estimando: `Δ_elección = P(votó PRI | ofrecieron) − P(votó PRI | no)`.

**Ejes secundarios** (sólo sobre la pierna de asistencia): `ur`, escolaridad
(`ed`, recodificada a los cuatro tramos por años: 0-6 · 7-9 · 10-12 · 13+),
sexo (`q1`). Tres ejes, dentro del tope.

**Limitación declarada antes de correr, no después.** La pierna de elección
**condiciona en haber votado**, y votar es justamente el otro desenlace: si la
oferta mueve la asistencia, condicionar en ella abre un camino de colisionador.
El `Δ_elección` de este acto es **descriptivo dentro de los votantes**, no un
efecto sobre la elección de voto de la población. Se reporta con esa etiqueta.

**Segunda limitación:** el instrumento **no observa quién dio la dádiva**. Por
eso el desenlace de la pierna de elección es el voto por un partido
pre-registrado, no «el que dio» — que es el enunciado literal de la regla y
**no es medible con este instrumento**. La pieza acota `R7.7`, no la cierra.

### 2.1 · Pre-registro `B-bis` de `R7.7`

| | |
|---|---|
| **Signo esperado** | `Δ_asistencia > 0` **y** `Δ_elección ≈ 0` |
| **`CORROBORADA`** | `Δ_asistencia > 0` con IC95 que **excluye** 0, **y** el IC95 de `Δ_elección` **contiene** 0 |
| **`CONTRARIA`** | el IC95 de `Δ_elección` **excluye** 0 (en cualquier dirección) — la regla afirma que la dádiva **no** mueve la elección, así que un movimiento limpio de la elección la contradice —, **o** `Δ_asistencia < 0` con IC95 que excluye 0 |
| **`NO-DISCRIMINA`** | los IC95 de las dos piernas contienen 0: el diseño no separa nada |
| **Precedencia** | si las dos piernas dan señales opuestas (asistencia limpia a favor **y** elección limpia distinta de 0), manda **`CONTRARIA`**, y se reporta el par completo |

**Qué significaría corroborar, dicho con todas sus letras.** Sería el **primer
dato mexicano de encuesta**, con diseño muestral y IC, que **separa turnout de
vote-choice** para la oferta de dádiva. Hoy el sitio de `civico.voto.clientelar`
en `canon/estado-programa-v1_11.md` §4 lo ocupa una cifra de **laboratorio**
(Ascencio-Chang 2025: la probabilidad de voto clientelar sube de 0.06 a **0.63**
cuando el votante cree que su voto puede observarse), **degradada a MEDIA** por
ser de laboratorio. Un dato de encuesta la **sustituiría** en ese sitio.

**Reserva sobre esa sustitución, escrita antes de medir.** La cifra 0.63 es de
un experimento con **monitoreo del voto** como manipulación. Esta pieza **no
tiene el ítem de monitoreo** (censo `P0` §3: no existe en la ola con la batería
clientelar). Así que lo que este acto puede sustituir es **el sitio de
`R7.7`** —turnout *vs* vote-choice—, **no** la condición de observabilidad que
el 0.63 mide. Si al cerrar el contador se anota «cifra de laboratorio sustituida
por dato de encuesta», tiene que ser con esta reserva pegada, o el contador
miente.

---

## §3 · Pieza (a-bis) · `R7.3` / `R7.6` — la agencia se conserva con secreto y cede sin él

**Fuente:** LAPOP México 2023 (`mex_2023_lapop_americasbarometer_v1_0_w`).
**Unidad:** persona de 18+.

Es **un solo cruce leído por sus dos ramas**: `R7.3` y `R7.6` son el par
contrario del modelo (`:553` y `:554`), y por eso comparten corrida.

- **Antecedente:** `mexwf1_19` — «Recibir ayuda (dinero en efectivo, alimentos,
  productos básicos) del gobierno». `1 = Sí` (363) · `2 = No` (1 252).
- **Moderador:** `countfair3` — «Percepción de una votación secreta», dicotomizado
  **ahora**: rama **`SECRETO`** = `1` (Siempre, n = 398) · rama **`OBSERVABLE`**
  = `2` o `3` (Algunas veces / Nunca, n = 1 144).
- **Desenlace:** `vb20 = 2` — «Votaría por el candidato o partido del actual
  presidente». Universo: `vb20 ∈ {1,2,3,4}` (1 414).

**Por qué `vb20` y no `vb3n`.** En la ola 2023 `vb3n` pregunta por la
presidencial de **2018**, cinco años antes de que se midiera el moderador. Un
moderador de 2023 sobre un desenlace de 2018 no es un cruce, es un anacronismo.
`vb20` es prospectivo y contemporáneo del moderador.

**Estimandos:**

```
Δ_SECRETO    = P(vb20=2 | ayuda=Sí, SECRETO)    − P(vb20=2 | ayuda=No, SECRETO)
Δ_OBSERVABLE = P(vb20=2 | ayuda=Sí, OBSERVABLE) − P(vb20=2 | ayuda=No, OBSERVABLE)
Δ_diferencia = Δ_OBSERVABLE − Δ_SECRETO
```

**Cobertura y universo restringido.** `vb20` tiene 1 414 / 1 622 = **87.2 %**,
por debajo del 90 %: la pieza corre **bajo universo restringido (`A-bis 4`)** y
**no reconcilia** sus celdas contra ningún marginal poblacional. Declarado aquí,
no descubierto después.

**Ejes secundarios:** `ur`, `estratosec`. Con el principal, tres.

**Guardia de celda que muy probablemente muerda:** la celda (ayuda = Sí ×
SECRETO) tiene **91** casos antes de exigir `vb20` válido. Si su numerador cae
bajo 10, se reporta `NO-ESTIMABLE` y `Δ_SECRETO` **no se estima** — en cuyo caso
el par entero queda `NO-DISCRIMINA` por insuficiencia, no por hallazgo.

### 3.1 · Pre-registro `B-bis` de `R7.3` y `R7.6`

| | |
|---|---|
| **Signo esperado** | `Δ_SECRETO ≈ 0` (la agencia se conserva: `R7.3`) **y** `Δ_OBSERVABLE > 0` (la agencia cede: `R7.6`), luego `Δ_diferencia > 0` |
| **`CORROBORADA`** (el par) | IC95 de `Δ_SECRETO` **contiene** 0 **y** IC95 de `Δ_OBSERVABLE` **excluye** 0 por arriba |
| **`CONTRARIA`** (el par) | el patrón invertido — IC95 de `Δ_SECRETO` excluye 0 por arriba **y** el de `Δ_OBSERVABLE` contiene 0 — **o** `Δ_OBSERVABLE` excluye 0 **por abajo** |
| **`NO-DISCRIMINA`** | los dos IC95 contienen 0, o alguna celda cae bajo la guardia de numerador |
| **Precedencia** | si `Δ_SECRETO` y `Δ_OBSERVABLE` dan las dos limpias y en el mismo signo, la separación que el par afirma no existe: manda **`CONTRARIA`** |

**Qué significaría corroborar.** Que la **observabilidad percibida del voto**
—no la dádiva, que aquí no se observa— es la condición bajo la cual recibir una
transferencia se asocia con votar por el oficialismo. Sería el primer dato
mexicano de encuesta que pone esa condición en una `[FUERTE]` (`R7.3`) que hasta
hoy la enuncia sin medirla en población.

---

## §4 · Pieza (b) · `R7.4` — protesta, agravio y entorno urbano

**Fuente:** LAPOP México 2019. **Unidad:** persona de 18+.
**Desenlace:** `prot3 = 1` («Participó en una protesta»), universo
`prot3 ∈ {1,2}` (1 576, 112 sí).

**Eje principal (4 celdas):** `ur` × `vic1ext` —
urbano-víctima (455) · urbano-no-víctima (807) · rural-víctima (65) ·
rural-no-víctima (252).

**Contrastes pre-registrados:**

```
C1 (entorno, con agravio) = P(protesta | urbano, víctima) − P(protesta | rural, víctima)
C2 (agravio, en urbano)   = P(protesta | urbano, víctima) − P(protesta | urbano, no víctima)
```

**Ejes secundarios:** `estratosec` (tamaño de municipalidad, 3 celdas), sexo
(`q1`), edad (`q2` en los cuatro tramos). Con el principal, cuatro.

**Guardia que se espera que muerda.** La celda rural-víctima tiene `n = 65` y,
a la tasa marginal de protesta (7.1 %), numerador esperado ≈ **5** — bajo el
umbral de 10. Si cae, `C1` **no se estima** y se reporta `NO-ESTIMABLE` con su
`n`. Está escrito antes de correr para que su caída sea un resultado previsto y
no una sorpresa que tiente a bajar el umbral.

**Lo que esta pieza no hace:** no dice nada sobre `R7.5` (autodefensa, rama
rural), no reabre el `D` de `ADR-158`, y no mide «red previa» ni «falla estatal
palpable» — dos de los cuatro antecedentes de la regla, que este instrumento no
trae. Mide **dos de cuatro**: agravio y entorno. Acota `R7.4`; no la cierra.

### 4.1 · Pre-registro `B-bis` de `R7.4`

| | |
|---|---|
| **Signo esperado** | `C1 > 0` (el entorno urbano canaliza el agravio hacia la protesta) y `C2 > 0` (el agravio mueve la protesta dentro de lo urbano) |
| **`CORROBORADA`** | el contraste estimable va en el signo esperado con IC95 que excluye 0 |
| **`CONTRARIA`** | va en signo opuesto con IC95 que excluye 0 |
| **`NO-DISCRIMINA`** | IC95 contiene 0 |
| **Precedencia** | si `C1` y `C2` discrepan en signo, ambos limpios, manda **`CONTRARIA`** |
| **Si `C1` cae por la guardia** | el veredicto sale de `C2` solo, y se declara que el contraste de entorno —el corazón de la regla— **no se midió** |

---

## §5 · Pieza (c) · `R7.8` — la transferencia se vive como derecho

**Fuente:** ENCUCI 2020, sección 6 unida a `ENCUCI_2020_SD.dbf` por `ID_PER`
(join total: 21 519 de 21 519). **Unidad:** persona de 15+.

**Desenlace:** `AP6_9 = 2` («Los programas sociales son un **derecho de los
ciudadanos**»), contra `AP6_9 = 1` («son una **ayuda que da el gobierno**»).
**Universo:** `AP6_9 ∈ {1,2}` — se excluyen `3 = Ninguna` (299) y `9 = NS/NR`
(352). Cobertura **20 868 / 21 519 = 96.98 %**, sobre el 90 %: la pieza **no**
corre bajo universo restringido.

**Eje principal:** `AP6_10` — beneficiario de un programa social en los últimos
12 meses. `1 = Sí` (5 789) · `2 = No` (15 676).

```
Δ_entitlement = P(derecho | beneficiario) − P(derecho | no beneficiario)
```

**Eje secundario ANIDADO, y declarado como tal:** `AP6_11` — «¿A usted le
pidieron algo (dinero, documentos personales, favores o que votara por algún
partido) a cambio de entrar o permanecer en algún programa?». Sólo existe dentro
de `AP6_10 = 1` (n = 5 789: 297 sí / 5 477 no / 15 NS). **Se interpreta sólo
dentro de los beneficiarios** y no se compara contra el marginal general — un
eje anidado en el desenlace no refuta la regla, la matiza.

**Ejes secundarios no anidados:** sexo (`SEXO`), edad (`EDAD`, cuatro tramos),
escolaridad (`NIV`, §1.5). Con el principal y el anidado, cinco: en el tope.

### 5.1 · Pre-registro `B-bis` de `R7.8`

| | |
|---|---|
| **Signo esperado** | `Δ_entitlement > 0` — quien recibe la transferencia la vive como derecho más que quien no |
| **`CORROBORADA`** | `Δ_entitlement > 0` con IC95 que excluye 0 |
| **`CONTRARIA`** | `Δ_entitlement < 0` con IC95 que excluye 0 |
| **`NO-DISCRIMINA`** | IC95 contiene 0 |
| **Eje anidado `AP6_11`** | signo esperado: quien recibió una **condición** a cambio dice «derecho» **menos** que quien no — la condicionalidad contradice el entitlement. Su veredicto se reporta aparte y **no** puede voltear el del eje principal |

**Qué significaría corroborar.** `R7.8` es `[HIPÓTESIS]`: el glosario `conf.07`
la separó de `civico.voto.agencia_con_secreto` justamente porque *«se vive como
derecho»* no tenía identificación, y `MAESTRA33-E18` descartó ENASEM por medir
afiliación y no percepción. Corroborar aquí sería **el primer dato de percepción**
de la regla, sobre 20 868 personas con diseño muestral — y el ancla jurídica ya
existe (pensión universal en el artículo 4.º constitucional desde 2020), así que
lo que faltaba era exactamente esto: que el beneficiario **lo viva así**.

**Reserva:** es una **asociación transversal**. Que el beneficiario diga
«derecho» más que el no beneficiario es compatible con que el programa cambie la
percepción **y** con que quien ya pensaba así se inscribiera más. Este diseño no
los separa, y la entrada de la propuesta lo dirá.

---

## §6 · Pieza (d) · `R1.5` — el seguro de depósito atenúa la aversión

**Fuente:** ENIF 2024, `TMODULO.csv`. **Unidad:** persona de 18 a 70 años.

**Universo del desenlace:** las **2 970** personas **sin cuenta** a las que se
les pregunta `P5_20` («¿Cuál es la razón principal por la que no tiene una
cuenta o tarjeta?»).

**Desenlaces (los dos, congelados ahora):**

- **Principal `D1`:** `P5_20 = 03` — «No confía en instituciones financieras o le
  dan mal servicio» (n = 183 en el universo).
- **Secundario `D2`:** `P5_20 ∈ {03, 05}` — añade «Prefiere otras formas de
  ahorro (tanda, guardar en su casa)» (n = 183 + 143 = 326). `D2` es la lectura
  amplia de «aversión» que el encargo nombra («desconfianza en bancos / prefiero
  efectivo»).

**Moderador (eje principal):** `P5_23` — «Los bancos o instituciones financieras
como todas las empresas pueden cerrar o quebrar, ¿sabe si en ese caso sus
ahorros están protegidos?». `1 = Sí` · `2 = No`. **Se pregunta al universo
completo** (13 502, 100 %), y **2 970 de 2 970** del universo del desenlace lo
tienen: la spec **no** sale degenerada. Verificado en el censo, no supuesto.

```
Δ_seguro = P(D1 | conoce protección) − P(D1 | no conoce)
```

**Ejes secundarios:** escolaridad (`NIV`, §1.5), edad (`EDAD_V`, cuatro tramos),
`TLOC` (tamaño de localidad). Con el principal, cuatro.

**Eje que el encargo pide y que NO se puede construir:** «celdas por tenencia de
cuenta». El desenlace `P5_20` **sólo existe para quien no tiene cuenta**, así
que la tenencia no varía dentro del universo. No se sustituye por nada; se
declara.

**Sensibilidad IPAB — cerrada en `P0` y no se intenta.** `P5_24_1` (nombra al
IPAB) está anidada en el «Sí» de `P5_23` y sólo cubre 426 de los 2 970 (14.3 %).
El marginal que sí se reporta, como hallazgo y no como celda: de los **4 136**
que dicen saber que sus ahorros están protegidos, **3 148 no saben nombrar la
institución**, y sólo **362 en toda la muestra** (2.7 %) nombran al IPAB.

### 6.1 · Pre-registro `B-bis` de `R1.5`

| | |
|---|---|
| **Signo esperado** | `Δ_seguro < 0` — donde la protección se percibe, la desconfianza pesa **menos** como razón para no tener cuenta |
| **`CORROBORADA`** | `Δ_seguro < 0` con IC95 que excluye 0, en `D1` |
| **`CONTRARIA`** | `Δ_seguro > 0` con IC95 que excluye 0 |
| **`NO-DISCRIMINA`** | IC95 contiene 0 |
| **Precedencia** | si `D1` y `D2` discrepan en signo, ambos limpios, manda **`CONTRARIA`** y se reporta el par |

**Qué significaría corroborar.** `R1.5` es `[MEDIA]` y **`ASIGNADO` sin dato**:
su moderador estaba identificado en el propio modelo (`:283`) pero nadie lo había
cruzado contra una medida de aversión. Corroborar sería la primera cifra
mexicana que ata la **visibilidad de la protección de depósitos** a la
**composición de razones para quedarse fuera del sistema financiero**.

**Reserva fuerte, escrita antes de medir.** `P5_23` mide una **creencia sobre
que existe protección**, no la **visibilidad del seguro** que el `SI` de la regla
nombra — y el marginal de `P5_24` muestra que las dos cosas se separan de verdad
(3 148 de 4 136 no saben quién protege). Aunque `D1` corrobore, la pieza **acota**
`R1.5`; no la cierra. Y `P5_20` es de **razón principal**: quien tenga
desconfianza pero elija otra razón como principal no cuenta como desconfiado —
el desenlace mide la **razón dominante**, no la presencia del motivo.

---

## §7 · Sello

Las cinco piezas, sus universos, sus dicotomizaciones, sus ejes, sus guardias de
cobertura y de celda, y los cinco pre-registros `B-bis` con su precedencia,
quedan congelados en este commit. Ningún cruce del desenlace contra el moderador
se ha calculado todavía.

**El primer resultado que produzca este procedimiento es el que se reporta.**
