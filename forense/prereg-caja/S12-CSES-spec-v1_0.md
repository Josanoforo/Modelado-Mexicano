# S12 · Pre-registro de `R7.3`/`R7.6` sobre CIDE-CSES 2015 — zanahoria, garrote y encuadre de secreto del voto

### `prereg-caja-S12` · **v1.0** · 7 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S12-CSES-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S12`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.sav`, de dos falsadores paralelos sobre `R7.3`/`R7.6` con la encuesta **CIDE-CSES 2015** (tres levantamientos: `cide_cses2015_nacional_poselectoral`, `cide_cses2015_nacional_preelectoral`, `cide_cses2015_estatal_preelectoral`): (1) los dos brazos de clientelismo condicionado — zanahoria (`pcyc13`, oferta) y garrote (`pcyc14`, amenaza) — como pieza principal (§1-§4), nunca sumados; (2) el experimento de encuadre sobre secreto del voto (`pvoto1`/`pvoto2`/`pvoto3`), como pieza aparte con su propio B-bis (§2-bis). |
> | **QUÉ NO ES** | No abre ningún `.sav` — NUBE, sin corpus montado. No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve tier de `R7.3` (`[MEDIA]`, D2-f) ni de `R7.6` (`[MEDIA]`, D2-g) — hereda ambos sin movimiento. No reescribe D2-g (la reescribe `TRAMITE-6`; esta pieza solo escribe la spec que esa cláusula nombrará). No adjudica cuál de los tres `.sav` de CSES 2015 es "el" archivo canónico del lote — cita los tres, con la incompatibilidad de variable declarada (§0.2), y deja a caja abrir el que corresponda a cada brazo. |
> | **VERIFICAS ASÍ** | Caja abre primero `cide_cses2015_nacional_poselectoral.sav` (donde `pcyc13`/`pcyc14` conviven con la etiqueta de zanahoria/garrote consistente, §0.2) y confirma códigos de respuesta contra el cuestionario completo antes de dicotomizar. Para §2-bis, abre `cide_cses2015_estatal_preelectoral.sav` — el único de los tres con `pvoto1`/`pvoto2`/`pvoto3` — y confirma que el diseño experimental (si lo hay: rotación de ítem, no de wording) está descrito en el cuestionario, no asumido. |

**Acto:** `ACTO MAESTRA38-N20-N21 · DOS-SPECS-CSES-R10-3`, 7/sep/2026, entorno **NUBE**, sobre `origin/main = 3d6dee3` (base refrescada; `7e0fb716` declarado en el encargo quedó `9f5b3cd..3d6dee3` detrás, sin tocar el perímetro de este acto — verificado, `git diff 7e0fb716 origin/main --stat` solo toca `canon/estado-programa-v1_12.md`/`canon/gobernanza-v1_15.md`).

---

## 0 · Ficha bajo prueba y corrección de premisa (A.8/D-13)

### 0.1 · Definiciones vigentes y tiers

`canon/modelo-decision-v4_0.md` §7, tabla (líneas 761-762):

| id de regla | tier de tabla (histórico) | tier vigente (enmienda) | `id` de propuesta citado por FP-329 |
|---|---|---|---|
| `R7.3` | `[FUERTE]` | **`[MEDIA]`** — D2-f (línea 781): CONTRARIA-REPLICADA en LAPOP 2023/ENCUCI 2020 | `civico.voto.agencia_con_secreto` (canon), `agencia_lapop2023`/`agencia_con_secreto_encuci2020` (propuesta, brazo observabilidad) |
| `R7.6` | `[MEDIA]` | **`[MEDIA]`**, partida por lectura en dos brazos — D2-g (línea 783), ninguno movido | brazo observabilidad: piezas de arriba · brazo proximidad: `civico.voto.clientelar_si_observable_lapop2019` |

`python3 tools/ya_medido.py R7.3` y `R7.6` (corridos al redactar esta spec, salida completa en el registro de sesión): ambos resuelven por canon a `civico.voto.agencia_con_secreto`; las tres piezas gemelas de la propuesta (`agencia_lapop2023`, `agencia_con_secreto_encuci2020`, `clientelar_si_observable_lapop2019`) están `SELLADA-SIN-CARGA`/`tier: SELLADA` (heredan `[MEDIA]`, comentario D2-g). Ninguna de las tres se toca — esta spec no re-mide LAPOP/ENCUCI, mide un instrumento distinto (CIDE-CSES 2015) todavía sin spec ni corrida (§0.2 de A.8 del encargo: `grep -rlI "CSES" forense/prereg-caja/` → tres menciones incidentales en `S1`/`S3`/`S11`, ninguna es spec de CSES).

**FP-329(b) — motivo de esta pieza, verbatim:** *"los tres constructos de R7.3/R7.6 quedan CUBIERTO los tres, y no por LAPOP: por CIDE-CSES 2015 […] trae la rama de zanahoria (pcyc13 le ofreció incluirlo en un programa a cambio de que votara) Y la de garrote (pcyc14 lo amenazó con quitarle el programa si no votaba), más un experimento de encuadre sobre el secreto del voto (pvoto1/pvoto2/pvoto3)."* Esta spec pre-registra exactamente esos tres constructos, sin adjudicar el tier — eso lo hace `TRAMITE-6`/mesa cuando exista una corrida.

### 0.2 · Corrección de premisa — `pcyc13`/`pcyc14` NO tienen el mismo significado en los tres `.sav` (verificado, no asumido)

El manifiesto y `FP-329` citan "CIDE-CSES 2015" como una sola fuente, pero el corpus trae **tres levantamientos distintos** bajo ese nombre (`data/manifiesto.yaml:24357-24410`, tres ids de `cide_cses2015_*`, sha256 distintos, tamaños distintos). Verificado variable por variable contra `data/inventario-reactivos-descargas-mx-v1_2.tsv`:

| archivo | `pcyc13` (texto verbatim) | `pcyc14` (texto verbatim) |
|---|---|---|
| `cide_cses2015_nacional_poselectoral.sav` | «...¿algún candidato o miembro de algún partido político **le ofreció incluirlo** en alguno de los programas... **a cambio de que Usted votara** por ese partido?» — **zanahoria** | «...¿algún candidato o miembro de algún partido político **lo amenazó con quitarle** alguno de los programas mencionados **si Usted no votaba** por ese partido?» — **garrote** |
| `cide_cses2015_nacional_preelectoral.sav` | idéntico a `poselectoral` (misma pregunta, mismo texto) — **zanahoria** | idéntico a `poselectoral` — **garrote** |
| `cide_cses2015_estatal_preelectoral.sav` | «...¿algún candidato o miembro de algún partido político **lo ha amenazado con quitarle** alguno de los programas mencionados **si Usted no vota** por ese partido?» — **esto es GARROTE, no zanahoria** | `pcyc14_1`...`pcyc14_8` — batería de tipo de servicio médico (Seguro Social/ISSSTE/Seguro Popular/privado), **sin relación con clientelismo** |

**El nombre de variable no es estable entre los tres archivos.** En `estatal_preelectoral`, `pcyc13` trae el texto de garrote (no de zanahoria) y `pcyc14` no es la pregunta de amenaza — es una batería de afiliación a servicios de salud, reutilizando el prefijo `pcyc14_*` para un tema distinto. **Los dos brazos zanahoria+garrote, con la lectura de FP-329(b), sólo coexisten limpios en `nacional_poselectoral` y `nacional_preelectoral`** (mismo cuestionario, confirmado idéntico en las dos filas de arriba); `estatal_preelectoral` no sirve para el par §1 y se declara fuera de esa pieza. Caja abre `nacional_poselectoral` o `nacional_preelectoral` para §1 — nunca `estatal_preelectoral` para esta parte — y confirma contra el cuestionario en pantalla, no contra el nombre de columna solamente, antes de dicotomizar cualquiera de las dos ramas (mismo criterio que `S1-A2 §0`/`S6 §0.4` fijaron para ambigüedades de instrumento).

`nacional_preelectoral` y `nacional_poselectoral` son levantamientos **distintos** (sha256 distintos: `85432d32...` vs `1ef01a17...`; tamaños 2 912 016 vs 1 864 581 bytes) pese a compartir cuestionario para `pcyc13`/`pcyc14` — no reportar como una sola muestra: si caja corre ambos, cada uno es su propia fila, nunca agrupados (mismo criterio de universo separado que `S6 §1.3` fija para `bx`/`b3b`).

### 0.3 · `pvoto1`/`pvoto2`/`pvoto3` viven en un archivo distinto al del par zanahoria/garrote

Verificado contra el mismo inventario: `pvoto1`/`pvoto2`/`pvoto3` aparecen **únicamente** en `cide_cses2015_estatal_preelectoral.sav` — 0 filas en `nacional_poselectoral`/`nacional_preelectoral` (búsqueda exacta por `variable_id`). El archivo que trae el experimento de encuadre de secreto del voto es el mismo que **no** sirve para el par zanahoria/garrote de §0.2 (su `pcyc13`/`pcyc14` no son la pareja de FP-329(b)). §2-bis se pre-registra, por tanto, como pieza **completamente separada por archivo**, no solo por sección — nunca se cruza `pvoto*` de `estatal_preelectoral` con `pcyc13`/`pcyc14` de `nacional_pos/preelectoral`: son muestras distintas (sha256 `7cf0e9e9...` vs `1ef01a17.../85432d32...`), no la misma persona respondiendo ambas baterías.

`nacional_poselectoral` sí trae un ítem de secreto del voto propio, con texto distinto — `p5`: «¿Usted cree que el gobierno o los partidos políticos pueden descubrir por quién votó?» (una sola pregunta, sin las tres variantes de encuadre de `pvoto1-3`) — se cita como evidencia de que el constructo de secreto percibido existe también en ese archivo, pero **no sustituye** el experimento de encuadre de §2-bis, que exige las tres variantes juntas para comparar entre condiciones.

---

## 1 · Disparadores — dos brazos separados, nunca sumados

Fuente: `cide_cses2015_nacional_poselectoral.sav` (preferido — es el levantamiento post-electoral, más cercano en tiempo al comportamiento de voto que el `ENTONCES` de `R7.3`/`R7.6` predicen) o `cide_cses2015_nacional_preelectoral.sav` como réplica del mismo cuestionario sobre otra muestra — **nunca agrupados** (§0.2).

* **Brazo zanahoria (`OFERTA`)** = 1 si `pcyc13` indica que sí le ofrecieron incluirlo en un programa a cambio del voto; 0 en caso contrario. Código exacto de `pcyc13` (Sí/No/NS-NC) no confirmado sin abrir el `.sav`/codebook — se pre-registra la regla conceptual, caja declara el mapeo real antes de calcular (mismo criterio que `S8 §3` fija para `aoj1`).
* **Brazo garrote (`AMENAZA`)** = 1 si `pcyc14` indica que sí lo amenazaron con quitarle el programa si no votaba; 0 en caso contrario. `pcyc14` está condicionado en el cuestionario a haber respondido antes que recibe algún programa (la pregunta dice «si Usted recibe alguno de estos beneficios») — caja verifica el filtro real (probablemente sobre receptores de programas sociales, subuniverso, no la muestra completa) antes de fijar el denominador, mismo criterio de gateo que `S8 §0.3` aplicó a `aoj1`/`vic1`.

Los dos brazos se reportan como **dos filas separadas del falsador** (§4) — nunca como un solo índice sumado. Motivo: son mecanismos con predicción de signo potencialmente distinta (oferta condicionada vs. amenaza condicionada), y `S4 §4.3`/D2-g ya fijaron que cuando LAPOP/ENCUCI dieron signos opuestos entre brazos de `R7.6`, la regla de la casa fue partir por lectura, no sumar — esta pieza aplica el mismo criterio desde el pre-registro, antes de que exista el número que lo obligue.

---

## 2 · Desenlace — declarado `NO-CONSTRUIBLE-SIN-CODEBOOK`, no inventado

Ninguna variable del inventario liga explícitamente el resultado de `pcyc13`/`pcyc14` a un desenlace de voto por el partido que ofreció/amenazó, en el mismo registro. Candidatos más cercanos, verificados uno por uno contra `data/inventario-reactivos-descargas-mx-v1_2.tsv` (`cide_cses2015_nacional_poselectoral.sav`):

| variable | texto verbatim | por qué no basta por sí sola |
|---|---|---|
| `p9` | «Independientemente del partido por el que usted vota, ¿usted normalmente se considera panista, priista, perredista, verde-ecologista, de Morena o de otro partido?» | identificación partidista, no voto — y no dice si coincide con el partido que ofreció/amenazó en `pcyc13`/`pcyc14` |
| `p6` | «¿hubo algún o algunos partidos por los que usted NUNCA hubiera votado?» | negativo, no positivo; no liga al partido oferente |
| `p8a` | «¿Y en la elección presidencial del 2012, por cuál partido votó?» | elección de 2012, tres años antes de la campaña que `pcyc13`/`pcyc14` preguntan (2015) — desalineado en el tiempo |

**Ninguno de los tres ata el voto a el mismo partido/candidato que la pregunta de clientelismo nombra** (`pcyc13_1`/`pcyc13_2`, `pcyc14_1`/`pcyc14_2` — sub-ítems «¿de cuál partido?» que si acaso identifican al oferente, no al voto emitido). El cuestionario completo del CSES Módulo 5 (`data/manifiesto.yaml`, id `cses5_modulo5_2016_2021_cuestionario`, y el propio texto de la encuesta CIDE 2015 al que el `.sav` pertenece) puede traer una pregunta de intención/recuerdo de voto explícita que el inventario, por sí solo (censo de nombres y etiquetas truncadas, no el cuestionario completo), no deja ver con certeza — **se declara `NO-CONSTRUIBLE-SIN-CODEBOOK`, no `NO-CONSTRUIBLE` a secas**: caja abre el cuestionario completo (mismo patrón que `S8 §6` cita el PDF de 2004 para confirmar códigos) antes de decidir si el desenlace existe. Si al abrir el `.sav`/cuestionario ninguna variable liga voto emitido con el partido nombrado en `pcyc13_1`/`pcyc14_1`, el falsador principal (§4, fila `OFERTA`/`AMENAZA`) queda `NO-ESTIMABLE` por ausencia de desenlace — declarado ahora, no después.

**Candidato de reserva, declarado como tal:** `p9` (identificación partidista) puede usarse como desenlace *débil* si el cuestionario no trae voto directo — mide alineamiento declarado, no conducta de voto, y cualquier corrida que lo use debe declarar esa sustitución en el reporte, no reportarla como si fuera "voto por el oferente".

---

## 2-bis · Experimento de encuadre — secreto del voto (`pvoto1`/`pvoto2`/`pvoto3`)

Fuente exclusiva: `cide_cses2015_estatal_preelectoral.sav` (§0.3 — no está en los otros dos archivos).

| variable | texto verbatim (encuadre) |
|---|---|
| `pvoto1` | «...Después [de la] elecc[ión] 2012, observadores electorales internacionales certificaron [que los ciuda]d[a]nos gozaron de garantías para ejercer voto secreto, pensando [en la] elecc[ión] 2015, si Ud decide votar, ¿cree que gob[ierno] o p[arti]dos podrán descubrir por quién votó Ud?» — encuadre de **garantía institucional confirmada** |
| `pvoto2` | «...Sin embargo, hubo reportes [de la] elecc[ión] 2012 [de] fun[ciona]rios d[e] casilla [que] marcaron boletas p[ara] p[o]der descubrir cómo votó. Ahora, pensando [en la] elecc[ión] 2015, si Ud decide votar, ¿cree que gob[ierno] o p[arti]dos podrán descubrir por quién votó Ud?» — encuadre de **violación reportada** |
| `pvoto3` | «...Ahora, pensando en las elecciones intermedias que se llevarán a cabo en junio de 2015, si Usted decide ir a votar, ¿cree que el gobierno o los partidos podrán descubrir por quién votó Usted?» — **neutral**, sin encuadre previo |

**Diseño no confirmado sin cuestionario/codebook:** el patrón de tres variantes de wording sobre la misma pregunta de fondo es consistente con un split-ballot/experimento de encuadre (cada respondiente recibe una sola variante, no las tres) — pero esta pieza no tiene, en el inventario, confirmación de que así se implementó (podría ser three ítems corridos secuencialmente sobre el mismo respondiente, un diseño distinto con otra lectura). Caja confirma el diseño real al abrir el `.sav` (tasas de no-respuesta por variable: si es split-ballot, cada `pvoto*` tendrá ~1/3 de la muestra con dato válido y el resto missing por diseño, no por no-respuesta) **antes** de calcular cualquier contraste entre condiciones — si las tres variables tienen cobertura completa (no partición de la muestra), el diseño es secuencial, no experimental, y el B-bis de esta pieza (§2-bis, tabla) se declara `NO-ESTIMABLE-DISEÑO-NO-EXPERIMENTAL`.

**Desenlace del experimento:** la propia respuesta dicotomizada de cada `pvoto*` (`CREE_QUE_DESCUBREN` = 1 si la respuesta indica que sí creen que pueden ser descubiertos; código exacto pendiente de codebook). El B-bis de §2-bis compara la proporción de `CREE_QUE_DESCUBREN=1` entre condiciones de encuadre (si el diseño es split-ballot confirmado):

| | `pvoto1` (garantía) | `pvoto2` (violación) | `pvoto3` (neutral) |
|---|---|---|---|
| **`CORROBORADA` (efecto de encuadre)** | proporción menor que en `pvoto3` (garantía reduce percepción de descubrimiento), IC95 de la diferencia excluye 0 | proporción mayor que en `pvoto3` (violación reportada aumenta percepción), IC95 excluye 0 | referencia |
| **`NO-DISCRIMINA`** | IC95 de la diferencia contra `pvoto3` contiene 0, cualquiera de los dos brazos | | |
| **`NO-ESTIMABLE`** | numerador `<10` en cualquier celda, o diseño no confirmado como split-ballot (ver arriba) | | |

Esta pieza es evidencia sobre el **mecanismo de secreto percibido**, no sobre `R7.3`/`R7.6` directamente — es la misma variable de moderación (agencia-con-secreto) que D2-f ya usó con LAPOP/ENCUCI, ahora con un tercer instrumento y, además, con manipulación experimental de encuadre en vez de solo medición transversal. Si corrobora un efecto de encuadre, es evidencia de que la percepción de secreto es maleable por el propio wording de la pregunta — relevante para interpretar por qué LAPOP/ENCUCI (D2-f) encontraron que la brecha secreto/no-secreto es chica: parte de esa brecha puede ser artefacto de instrumento, no solo comportamiento real. Esta lectura se declara aquí como hipótesis a discutir por mesa si el B-bis corrobora — esta spec no la adjudica.

---

## 3 · Universo y ponderador

**Universo:** población adulta encuestada en el levantamiento CSES 2015 elegido (`nacional_poselectoral`/`nacional_preelectoral` para §1; `estatal_preelectoral` para §2-bis) — sin restricción adicional salvo el filtro de `pcyc14` sobre receptores de programa (§1, declarado, no confirmado el tamaño del subuniverso).

**Ponderador — tres candidatos por archivo, ninguno confirmado sin codebook:**

| archivo | candidatos de ponderador (inventario) | nota |
|---|---|---|
| `cide_cses2015_nacional_poselectoral.sav` | `PONDFIN` («Ponderador nacional»), `PONDOM` («Ponderador por dominio»), `PONDDOM`, `PONDSEX` | `PONDFIN` es el candidato de ponderador global — caja lo confirma contra el codebook/cuestionario antes de usarlo, mismo criterio que `S2-L2 §1.0`/`S8 §2` fijan para `wt` no etiquetado |
| `cide_cses2015_nacional_preelectoral.sav` | `PONDFIN` («Ponderador Global»), `PONDOM1` («Ponderador para estados gobernados por...»), `PONDOM2` («Ponderador por TIPO DE ELECCIÓN»), `PONDDOM1`, `PONDDOM2`, `PONDSEX`; estrato: `dominio` («Estratos de diseño muestral») | más candidatos que el poselectoral — nombre distinto de la misma familia (`PONDFIN` reaparece con etiqueta explícita aquí) |
| `cide_cses2015_estatal_preelectoral.sav` | mismos nombres que `nacional_preelectoral` (`PONDFIN`, `PONDOM1`, `PONDOM2`, `PONDDOM1`, `PONDDOM2`, `PONDSEX`, `dominio`) | consistente con ser, por diseño muestral, el mismo levantamiento estatal-preelectoral de la misma casa |

**Ninguno de los cortes ni ponderadores está confirmado sin codebook — caja los declara al abrir, y si la variable no existe en el archivo, PARA** (cláusula S6, verbatim del encargo).

---

## 4 · Escala de falsación `B-bis` — brazo zanahoria y brazo garrote, filas separadas

| | Brazo zanahoria (`OFERTA` → desenlace) | Brazo garrote (`AMENAZA` → desenlace) |
|---|---|---|
| **Signo esperado (lectura R7.6, brazo observabilidad/monitoreo percibido, D2-g)** | mayor alineamiento con el partido oferente entre quienes recibieron oferta que entre quienes no | mayor alineamiento con el partido amenazante entre quienes recibieron amenaza que entre quienes no |
| **`CORROBORADA`** | proporción de alineamiento mayor bajo `OFERTA=1`, IC95 de la diferencia excluye 0 en signo positivo | ídem sobre `AMENAZA=1` |
| **`CONTRARIA`** | IC95 excluye 0 en signo negativo (oferta asociada a MENOR alineamiento) | ídem, amenaza asociada a menor alineamiento |
| **`NO-DISCRIMINA`** | IC95 contiene 0 | ídem |
| **`NO-ESTIMABLE`** | numerador `<10` en alguna celda, **o** el desenlace resulta `NO-CONSTRUIBLE-SIN-CODEBOOK` tras abrir el cuestionario completo (§2) — en ese caso el falsador principal no corre y se declara así, no se sustituye por `p9` sin decirlo | ídem |

**Cota de n mínima por celda:** numerador `<10` ⇒ `NO-ESTIMABLE`, misma guardia que `S4`/`S5`/`S8` fijan.

**Qué significaría corroborar cualquiera de los dos brazos (B-bis).** Sería la primera medición mexicana con zanahoria y garrote sobre el mismo instrumento, medidos por separado — a diferencia de LAPOP/ENCUCI (D2-f/D2-g), que miden agencia-con-secreto y proximidad/focalización, pero no una oferta y una amenaza explícitas del mismo cuestionario. Si los dos brazos dan el mismo signo, es evidencia convergente sobre el mecanismo de `R7.6` (monitoreo percibido, cualquiera que sea el vehículo — promesa o amenaza); si dan signos opuestos, es una cuarta pieza `CONTRARIA` entre brazos, en la línea de lo que D2-g ya vio entre LAPOP 2019/2023 — un hallazgo para mesa, no una resolución de esta spec.

---

## 5 · `se_mueve_si`

Cláusula que sustituye a la D2-g reescrita por `TRAMITE-6` (esta pieza no la redacta, la nombra):

**Brazo zanahoria:** si la proporción de alineamiento con el partido oferente **no es mayor** entre quienes recibieron oferta (`OFERTA=1`) que entre quienes no, este brazo no sostiene el mecanismo de observabilidad de `R7.6`. **Brazo garrote:** mismo criterio sobre `AMENAZA=1`. **Si ambos brazos corroboran en el mismo sentido** que LAPOP 2023/ENCUCI 2020 (D2-f: la brecha secreto/no-secreto es chica frente a la asociación base) — es decir, si CSES 2015 también encuentra que la promesa/amenaza mueve el voto declarado independientemente de si el votante cree que su voto es secreto —, es un tercer y cuarto instrumento corroborando el mismo patrón que D2-f ya citó como motivo de degradar `R7.3` a `[MEDIA]`; si CSES 2015 **discrepa** (brecha grande entre condiciones de secreto, o brazos con signos opuestos entre sí), es evidencia `CONTRARIA` sobre el patrón de D2-f/D2-g, y mesa decide si eso reabre la enmienda. Esta spec no adjudica ninguno de los dos desenlaces — los declara como los dos caminos posibles del `se_mueve_si` para que la cláusula que `TRAMITE-6` redacte los cite.

---

## 6 · Archivos que la caja necesita abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `cide_cses2015_nacional_poselectoral` | `UNIVERSO-2026-09/CSES/cide_cses2015_nacional_poselectoral.sav` | `1ef01a17fe6ca10b73db9e988ac4dacac766a6b0759af43f1fd690d3f60d4d80` |
| `cide_cses2015_nacional_preelectoral` | `UNIVERSO-2026-09/CSES/cide_cses2015_nacional_preelectoral.sav` | `85432d32266ac68f887bdf87fdd18f4673c3583b420ff518e42805079fdaef55` |
| `cide_cses2015_estatal_preelectoral` | `UNIVERSO-2026-09/CSES/cide_cses2015_estatal_preelectoral.sav` | `7cf0e9e9262f9797e6e39d8485e98cd73d49a276859cc57fa21e3c82a81fbd9b` |

Sin codebook registrado por separado en el manifiesto para ninguno de los tres — el cuestionario completo (si existe en el corpus como PDF/texto, no confirmado por esta spec) es lo que caja abre para resolver §2 (desenlace) y confirmar el diseño de §2-bis; si no existe, caja lo declara ausente antes de dar por perdido el desenlace.

---

## 7 · Qué NO hace este acto

No abre ningún `.sav` de §6. No calcula ninguna celda ni IC95. No mueve el tier de `R7.3` (`[MEDIA]`, D2-f) ni de `R7.6` (`[MEDIA]`, D2-g, ambos brazos). No reescribe D2-g — esa cláusula la escribe `TRAMITE-6`; esta spec solo pre-registra el contenido que esa cláusula citará (§5). No adjudica cuál de los tres `.sav` de CSES 2015 es el canónico para el par zanahoria/garrote — declara que solo dos de los tres (`nacional_poselectoral`/`preelectoral`) sirven, y que el tercero (`estatal_preelectoral`) es el único con `pvoto1-3`. No inventa un desenlace de voto que el inventario no confirma — declara `NO-CONSTRUIBLE-SIN-CODEBOOK` y dos candidatos de reserva declarados como tales. No toca `canon/modelo-decision-v4_0.md`, `milpa/**`, `data/**` ni `forense/hallazgos.md`. No abre ni toca `S13-R10-3-spec-v1_0.md` (pieza N21, mismo lote, archivo separado).

**El primer resultado que produzca este procedimiento es el que se reporta.**
