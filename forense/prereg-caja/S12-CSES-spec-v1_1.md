# S12 · Pre-registro de `R7.3`/`R7.6` sobre CIDE-CSES 2015 — zanahoria, garrote y encuadre de secreto del voto

### `prereg-caja-S12` · **v1.1** · 8 de septiembre de 2026 · `sucesora_de: v1_0`

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S12-CSES-spec-v1_1.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S12`** — cítalo así, nunca por nombre de archivo |
> | **SUCESORA DE** | **`v1.0`** (`forense/prereg-caja/S12-CSES-spec-v1_0.md`, `sha256 = 870522a34d9538454b5b774ddc33e46f9cd8e8d62a20f31b2d972f9755447336`). **El sello de `v1.0` no se edita** (E.3): sus bytes quedan intactos y su sidecar sigue verificando. `CALC-0001`, que corrió contra `v1.0`, **sigue siendo una corrida válida de `v1.0` y NO se re-corre** — ver la última fila de esta tabla. |
> | **QUÉ ES** | El mismo pre-registro de `v1.0` sobre **CIDE-CSES 2015**, con el papel puesto al día por lo que la caja encontró **al abrir** el `.sav` y el cuestionario: dos diferencias, listadas abajo y desarrolladas en §0.4 y §4. |
> | **LAS DOS DIFERENCIAS** | **(a) §2 — el desenlace SÍ existe** y `v1.0` lo declaró `NO-CONSTRUIBLE-SIN-CODEBOOK`. Es **`peledip`** («El pasado 7 de junio de 2015 fueron las elecciones para DIPUTADOS FEDERALES, ¿Por cuál partido votó usted?»), en `nacional_poselectoral`. Con él vienen dos correcciones más de premisa: `nacional_preelectoral` **trae ítems post-electorales pese a su nombre**, y por eso **no es réplica del desenlace** (§0.4). **`FP-350`.** · **(b) §4 — el contraste pre-registrado NO ES ESTIMABLE con esta fuente**, y no por `n` corta: el brazo control **carece de desenlace por construcción del cuestionario**. Se declara `NO-ESTIMABLE-CON-ESTA-FUENTE` con la evidencia verbatim. **`FP-357`.** |
> | **DOS ANOTACIONES, NO DIFERENCIAS** | §1 y §3 de `v1.0` dejaron cuatro cosas «no confirmadas sin abrir el `.sav`» (códigos de `pcyc13`/`pcyc14`, filtro real de `pcyc14`, ponderador, estrato/UPM). **`CALC-0001` las resolvió todas**, y `v1.1` las **cita al pie de cada sección sin borrar el texto que declaró la incertidumbre** — ese texto es el registro de qué se sabía al congelar. Son anotaciones de resolución, no cambios de criterio: nada de lo que la spec decide se mueve por ellas. |
> | **QUÉ NO CAMBIA** | Todo lo demás, verbatim de `v1.0`: §0.1 (fichas y tiers), §0.2 (los tres `.sav` no son intercambiables), §0.3 (`pvoto1-3` viven en otro archivo), §1 (los dos brazos, nunca sumados), §2-bis (el experimento de encuadre y su guardia de diseño), §3 (universo y ponderador), §5 y §6. **No mueve el tier de `R7.3` (`[MEDIA]`, D2-f) ni el de `R7.6` (`[MEDIA]`, D2-g, ambos brazos).** No reescribe D2-g. |
> | **QUÉ NO ES** | **No es una spec nueva.** El contraste **acotado a receptores** que §4.1 nombra como salida posible **cambia el estimando** y por tanto **no se cuela aquí**: se deja como **fila de decisión de mesa**, no como cláusula de esta versión. **No re-corre `CALC-0001`** — ver abajo. No toca `canon/`, `milpa/**` ni `data/**`. No abre ni toca `S13-R10-3-spec-v1_0.md`. |
> | **`CALC-0001` NO SE RE-CORRE** | **Sus 54 `RESULT` no cambian: el defecto era del papel, no del cálculo.** `CALC-0001` abrió el cuestionario, encontró el desenlace que `v1.0` daba por inexistente, construyó el crosswalk de partido que hacía falta, corrió los cuatro brazos y publicó `N-T0 = 0` en los cuatro con `VEREDICTO = NO-ESTIMABLE` — que es **la respuesta correcta**, obtenida por el camino correcto. Lo que estaba mal era la spec que lo gobernaba, y eso es lo que esta `v1.1` repara. `corrida_id = CALC-0001--174c269a07b6`, sello `aa48aac50e75b5cad3170649f1e46dcda0c18aeab5f8e3005b2e46abe221fbcf`, **intacta**. |
> | **ACTO QUE LA CONGELA** | `ACTO GEN2-SPECS-SUCESORAS · S6 v1.3 + S12 v1.1`, 8/sep/2026, **UBUNTU (caja)**, sobre `origin/main = c5b89a9`. Firma de mesa que la autoriza, verbatim del 8/sep/2026: «si hagamos las specs sucesoras..» |
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


### 0.4 · Las tres correcciones de premisa que trajo abrir el `.sav` — **`FP-350`**

`v1.0` §2 declaró el desenlace `NO-CONSTRUIBLE-SIN-CODEBOOK` e instruyó: *«caja
abre el cuestionario completo … antes de decidir si el desenlace existe»*. **Se
abrió y existe.** El inventario —censo de nombres con etiquetas truncadas— no lo
mostraba; el metadato del `.sav` sí:

| archivo | variable | etiqueta verbatim | qué es |
|---|---|---|---|
| `nacional_poselectoral` | **`peledip`** | «El pasado 7 de junio de 2015 fueron las elecciones para DIPUTADOS FEDERALES, ¿Por cuál partido votó usted?» | **voto emitido**, elección federal — la misma campaña que `pcyc13`/`pcyc14` preguntan |
| `nacional_preelectoral` | `pelegob` · `pelemun` | «El pasado 7 de junio de 2015 fueron las elecciones para gobernador/pdte mun / PRESIDENTE MUNICIPAL, ¿Por cuál partido votó usted?» | **voto emitido**, elección **local** — otro cargo |
| `estatal_preelectoral` | `pelegob` · `pelemun` | «**Si hoy fueran** las elecciones … ¿por cuál partido **votaría** usted?» | **intención**, no voto emitido |

**(1) El desenlace de §2 sí existe.** Los tres candidatos que `v1.0` §2 examinó
—`p9` (identificación partidista), `p6` (partido por el que nunca votaría),
`p8a` (voto presidencial de 2012)— quedan **fuera**: hay un voto emitido, del
año correcto y con partido nombrado, que ninguno de los tres igualaba. **El
«candidato de reserva» `p9` que `v1.0` §2 dejó abierto queda retirado por
innecesario**, no por inválido.

**(2) El nombre del archivo miente sobre su contenido.** `nacional_preelectoral`
trae ítems **post**-electorales de voto emitido (`pelegob`/`pelemun`, en
pasado). Se identifica por el contenido, nunca por el rótulo del archivo.

**(3) `nacional_preelectoral` NO es réplica del desenlace.** `v1.0` §1 la ofrece
como *«réplica del mismo cuestionario sobre otra muestra»*: lo es **para el
disparador** (`pcyc13`/`pcyc14` idénticos, §0.2), **no para el desenlace** — no
trae `peledip`; su voto emitido es de **otro cargo**. Se corre como fila aparte
y se rotula como tal, jamás agrupada.

### 0.5 · El crosswalk de partido es obligatorio, y por qué

`pcyc13_1`/`pcyc14_1` («¿de cuál partido?») y `peledip`/`pelegob`/`pelemun`
(«¿por cuál partido votó?») **usan esquemas de código distintos**. Cinco códigos
coinciden en número y **discrepan en partido**:

| código | `pcyc13_1`/`pcyc14_1` | `peledip`/`pelegob`/`pelemun` |
|---|---|---|
| `3` | PRD | *(no existe)* |
| `4` | **PT** | **PRD** |
| `8` | **MORENA** | **PT** |
| `9` | **Partido Humanista** | **PVEM** |
| `10` | **Encuentro Social** | **OTRO** |
| `12` | **Otro** | **NO SABE** |

Una igualdad directa `pcyc13_1 == peledip` produciría alineamientos falsos **en
silencio, sin error**. `CALC-0001` congeló el crosswalk código a código, en el
único sentido `oferente → voto`; esta versión lo incorpora al papel como
**requisito del desenlace**, no como detalle de implementación.
---

## 1 · Disparadores — dos brazos separados, nunca sumados

Fuente: `cide_cses2015_nacional_poselectoral.sav` (preferido — es el levantamiento post-electoral, más cercano en tiempo al comportamiento de voto que el `ENTONCES` de `R7.3`/`R7.6` predicen) o `cide_cses2015_nacional_preelectoral.sav` como réplica del mismo cuestionario sobre otra muestra — **nunca agrupados** (§0.2).

* **Brazo zanahoria (`OFERTA`)** = 1 si `pcyc13` indica que sí le ofrecieron incluirlo en un programa a cambio del voto; 0 en caso contrario. Código exacto de `pcyc13` (Sí/No/NS-NC) no confirmado sin abrir el `.sav`/codebook — se pre-registra la regla conceptual, caja declara el mapeo real antes de calcular (mismo criterio que `S8 §3` fija para `aoj1`).
* **Brazo garrote (`AMENAZA`)** = 1 si `pcyc14` indica que sí lo amenazaron con quitarle el programa si no votaba; 0 en caso contrario. `pcyc14` está condicionado en el cuestionario a haber respondido antes que recibe algún programa (la pregunta dice «si Usted recibe alguno de estos beneficios») — caja verifica el filtro real (probablemente sobre receptores de programas sociales, subuniverso, no la muestra completa) antes de fijar el denominador, mismo criterio de gateo que `S8 §0.3` aplicó a `aoj1`/`vic1`.

⚠️ **Anotación de resolución (no reescribe el pre-registro).** Los dos «no confirmado sin abrir el `.sav`» de arriba **ya se resolvieron**, y `v1.1` los cita en vez de dejar al lector con la duda — sin borrar el texto que declaró la incertidumbre, porque ese texto es el registro de qué se sabía cuando se congeló. Verificado por `CALC-0001` en `nacional_poselectoral` y `nacional_preelectoral`, **idénticos en los dos**: `pcyc13` y `pcyc14` codifican `1 = Sí` · `2 = No` · `9 = Ns/NC`, y **no existe el código `0`** — la forma `== 0` habría seleccionado el conjunto vacío en silencio. `OFERTA = 1` si `pcyc13 == 1`, `OFERTA = 0` si `pcyc13 == 2`; el `9` y el faltante quedan **fuera de los dos grupos y se cuentan**; ídem `AMENAZA` sobre `pcyc14`. **El filtro de `pcyc14` también:** el texto de la pregunta —«Y si Usted recibe alguno de estos beneficios…»— lo gatea sobre la batería que la antecede, `pcyc12` (LICONSA) · `pcyc12a` (PROCAMPO) · `pcyc12b` (PROSPERA).

Los dos brazos se reportan como **dos filas separadas del falsador** (§4) — nunca como un solo índice sumado. Motivo: son mecanismos con predicción de signo potencialmente distinta (oferta condicionada vs. amenaza condicionada), y `S4 §4.3`/D2-g ya fijaron que cuando LAPOP/ENCUCI dieron signos opuestos entre brazos de `R7.6`, la regla de la casa fue partir por lectura, no sumar — esta pieza aplica el mismo criterio desde el pre-registro, antes de que exista el número que lo obligue.

---

## 2 · Desenlace — **`peledip`**, verificado; `v1.0` lo daba por no construible

**Diferencia (a) con `v1.0`, `FP-350`.** `v1.0` §2 examinó el inventario, no
halló ninguna variable que ligara `pcyc13`/`pcyc14` a un voto por el partido
nombrado, y declaró —correctamente para lo que había mirado—
`NO-CONSTRUIBLE-SIN-CODEBOOK`, con la instrucción de abrir el cuestionario antes
de dar el desenlace por perdido. **Se abrió. El desenlace existe** (§0.4).

**Desenlace congelado por `v1.1`:**

> **`ALINEADO` = 1** si el partido por el que la persona **votó** —`peledip` en
> `nacional_poselectoral`— **corresponde**, vía el crosswalk de §0.5 y en el
> único sentido `oferente → voto`, al partido que le **ofreció** (`pcyc13_1`) o
> que la **amenazó** (`pcyc14_1`). **`ALINEADO` = 0** en cualquier otro voto
> emitido con contraparte posible. `29 = PRI-PVEM` (coalición) cuenta como
> alineado si el oferente fue PRI (`2`) o PVEM (`5`). `11 NINGUNO` ·
> `12 NO SABE` · `13 BLANCO` · `14 ANULADO` · `39 CANDIDATO INDEPENDIENTE` no
> tienen contraparte de oferente y cuentan `ALINEADO = 0`. `97 Ninguno` y
> `99 NS/NC` del **oferente** son **faltante del brazo**, no un cero.

**Fila aparte, jamás agrupada:** `nacional_preelectoral` sirve **para el
disparador** pero **no replica el desenlace** (§0.4 punto 3): su voto emitido es
de otro cargo (`pelegob`/`pelemun`). Se corre y se rotula como fila propia.

🛑 **Y aun con el desenlace en la mano, el contraste no se puede estimar.** Eso
no es una consecuencia de §2 sino de cómo el cuestionario gatea las
sub-preguntas, y va en §4 — donde la escala de falsación lo declara con su
evidencia. **Que el desenlace exista y que el contraste sea estimable son dos
cosas distintas, y `v1.0` no las separaba.**

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

⚠️ **Anotación de resolución (no reescribe el pre-registro).** También resuelto por `CALC-0001`, contra la etiqueta del metadato y no contra el nombre: el ponderador global es **`PONDFIN`** en los **tres** archivos («Ponderador nacional» en `poselectoral`, «Ponderador Global» en los dos `preelectoral`), el estrato es **`dominio`** y la UPM es **`upmmn`**. `PONDOM`/`PONDDOM`/`PONDOM1`/`PONDOM2`/`PONDDOM1`/`PONDDOM2` son ponderadores **por dominio**, no globales: no entran. `PONDSEX` y `ponde` **no traen etiqueta y no se usan** — un nombre no es una etiqueta.

---

## 4 · 🛑 `NO-ESTIMABLE-CON-ESTA-FUENTE` — el brazo control no tiene desenlace, por construcción

**Diferencia (b) con `v1.0`, `FP-357`.** `v1.0` §4 pre-registró una escala
`B-bis` de cuatro filas (`CORROBORADA` / `CONTRARIA` / `NO-DISCRIMINA` /
`NO-ESTIMABLE`) para los dos brazos, con la cota de `n < 10` por celda. **Esa
escala no se puede aplicar con esta fuente**, y la razón no es `n` corta.

### 4.0 · La evidencia, verbatim de la corrida sellada

`CALC-0001` (`corrida_id = CALC-0001--174c269a07b6`, 54 `RESULT`, sello
`aa48aac50e75b5cad3170649f1e46dcda0c18aeab5f8e3005b2e46abe221fbcf`) corrió los
cuatro brazos. Los cuatro salieron `VEREDICTO = NO-ESTIMABLE`:

| brazo | `N-T1` | `N-T0` | `N-NSNC` | `P-T1` (proporción ponderada) | `P-T0` |
|---|---|---|---|---|---|
| POSEL · OFERTA  | 42 | **0** | 12   | 0.37922545290553505 | — |
| POSEL · AMENAZA | 14 | **0** | 11   | 0.438740191776023   | — |
| PREEL · OFERTA  | 23 | **0** | 1207 | 0.2468700731109074  | — |
| PREEL · AMENAZA | 10 | **0** | 1213 | 0.18369940751162478 | — |

**`N-T0 = 0` no es una `n` corta ni un filtro mal escrito: es estructural.** El
desenlace `ALINEADO` se construye sobre `pcyc13_1` / `pcyc14_1` («¿qué partido
le ofreció / lo amenazó?»), preguntas que **sólo existen para quien contestó que
sí**. El brazo control no tiene partido con el cual alinearse, así que el
desenlace está **indefinido ahí por construcción**.

**Control positivo sobre el dato crudo, para separar esto de un código mal
resuelto** — el código `2 = No` existe y es mayoritario:

```
poselectoral   pcyc13: {1: 58, 2: 1130, 9: 12}   NaN=0
               pcyc14: {1: 24, 2: 1165, 9: 11}   NaN=0
preelectoral   pcyc13: {1: 63, 2: 1130, 9: 7}    NaN=1200
               pcyc14: {1: 23, 2: 1164, 9: 13}   NaN=1200
```

Es decir: **había 1 130 y 1 165 personas en el brazo control, y ninguna podía
tener desenlace.** No es rescatable con `n`: multiplicar la muestra por diez
multiplicaría por diez un `N-T0` que seguiría siendo **cero**.

### 4.1 · Lo que esta versión declara, y lo que deliberadamente NO hace

> **`S12` §4 queda `NO-ESTIMABLE-CON-ESTA-FUENTE`.** El contraste
> `ALINEADO | T=1` vs `ALINEADO | T=0` sobre CIDE-CSES 2015 no se estima —ni en
> `nacional_poselectoral` ni en `nacional_preelectoral`— porque el brazo control
> carece de desenlace definido por construcción del cuestionario, no por tamaño
> de muestra. Ninguna corrida futura sobre estos tres `.sav` puede reclamar
> haber medido `S12` §4.

**Y lo que NO se cuela aquí.** Existe una salida obvia —**acotar el universo a
receptores de oferta/amenaza** y contrastar, dentro de ellos, alineados contra
no alineados—, y **no se adopta en esta versión**: ese contraste **cambia el
estimando**. Ya no compara «expuestos vs. no expuestos», sino la composición
interna de los expuestos; responde una pregunta distinta, con una `se_mueve_si`
distinta y una lectura distinta de `R7.6`. **Si mesa lo quiere, es una spec
nueva con su propia pregunta** — se deja como **fila de decisión**, no como
cláusula de `v1.1`. Meterlo aquí sería sustituir el contraste pre-registrado por
otro después de saber que el primero no corre, que es exactamente lo que el
patrón de dos commits existe para impedir.

**Qué sobrevive de `v1.0` §4.** La cota de `n < 10` por celda y las cuatro
etiquetas de la escala **siguen vigentes como escala** —esta versión no las
deroga— y **son las que `§2-bis` sigue usando**. Lo que queda anulado es su
aplicabilidad al par zanahoria/garrote **con esta fuente**.

### 4.2 · Qué NO concluye este `NO-ESTIMABLE`

**No es evidencia contra `R7.3` ni contra `R7.6`.** Es **ausencia de medición**,
y se reporta como tal: los tiers `[MEDIA]` de D2-f y D2-g quedan **exactamente
donde estaban**, y las tres piezas gemelas de la propuesta
(`agencia_lapop2023`, `agencia_con_secreto_encuci2020`,
`clientelar_si_observable_lapop2019`) no se tocan. **Tampoco invalida el
instrumento:** CIDE-CSES 2015 mide muy bien la **prevalencia** de oferta y
amenaza —58 y 24 casos declarados en el poselectoral— y `§2-bis` sigue en pie
sobre otro archivo. Lo que no soporta es **este** contraste.

---

## 5 · `se_mueve_si` — **conservada verbatim, y declarada INEJECUTABLE con esta fuente**

El texto de `v1.0` §5 **no se reescribe** (queda íntegro abajo): reescribir una
cláusula de falsación después de saber que no dispara sería elegir el criterio
con el resultado a la vista. Se conserva, y se declara qué le pasa.

`v1.0` §5, verbatim:

> *«**Brazo zanahoria:** si la proporción de alineamiento con el partido
> oferente **no es mayor** entre quienes recibieron oferta (`OFERTA=1`) que
> entre quienes no, este brazo no sostiene el mecanismo de observabilidad de
> `R7.6`. **Brazo garrote:** mismo criterio sobre `AMENAZA=1`. **Si ambos brazos
> corroboran en el mismo sentido** que LAPOP 2023/ENCUCI 2020 (D2-f […]) […] es
> un tercer y cuarto instrumento corroborando el mismo patrón […]; si CSES 2015
> **discrepa** […] es evidencia `CONTRARIA` sobre el patrón de D2-f/D2-g, y mesa
> decide si eso reabre la enmienda. Esta spec no adjudica ninguno de los dos
> desenlaces […].»*

🛑 **La cláusula compara con «quienes no» — y «quienes no» no tienen desenlace
definido en esta fuente (§4).** Por tanto, con CIDE-CSES 2015:

> **`se_mueve_si` es INEJECUTABLE. `R7.3` y `R7.6` no se mueven, en ninguna
> dirección, por esta spec.** No es que el criterio se haya cumplido o
> incumplido: es que **no puede evaluarse**, y una `se_mueve_si` que no se
> evalúa **no es una `se_mueve_si` cumplida**. La cláusula queda viva para
> cualquier fuente futura que sí traiga un brazo control con desenlace.

**La lección que sí queda escrita**, y que ninguna cifra de `v1.0` anticipaba:
*una `se_mueve_si` puede estar bien redactada, ser falsable en principio, y ser
inejecutable en la fuente sobre la que se pre-registró — porque el cuestionario
gatea el desenlace al mismo ítem que define el tratamiento.* Comprobarlo cuesta
una corrida; no comprobarlo cuesta un veredicto inventado.

---

## 6 · Archivos que la caja necesita abrir

| id de manifiesto | archivo | sha256 |
|---|---|---|
| `cide_cses2015_nacional_poselectoral` | `UNIVERSO-2026-09/CSES/cide_cses2015_nacional_poselectoral.sav` | `1ef01a17fe6ca10b73db9e988ac4dacac766a6b0759af43f1fd690d3f60d4d80` |
| `cide_cses2015_nacional_preelectoral` | `UNIVERSO-2026-09/CSES/cide_cses2015_nacional_preelectoral.sav` | `85432d32266ac68f887bdf87fdd18f4673c3583b420ff518e42805079fdaef55` |
| `cide_cses2015_estatal_preelectoral` | `UNIVERSO-2026-09/CSES/cide_cses2015_estatal_preelectoral.sav` | `7cf0e9e9262f9797e6e39d8485e98cd73d49a276859cc57fa21e3c82a81fbd9b` |

Sin codebook registrado por separado en el manifiesto para ninguno de los tres — el cuestionario completo (si existe en el corpus como PDF/texto, no confirmado por esta spec) es lo que caja abre para resolver §2 (desenlace) y confirmar el diseño de §2-bis; si no existe, caja lo declara ausente antes de dar por perdido el desenlace.

---

## 7 · Qué NO hace esta versión

**No re-corre `CALC-0001`. Sus 54 `RESULT` no cambian: el defecto era del papel,
no del cálculo.** `CALC-0001` abrió el cuestionario que `v1.0` §2 mandó abrir,
encontró el desenlace, construyó el crosswalk que hacía falta, corrió los cuatro
brazos y publicó `N-T0 = 0` con `VEREDICTO = NO-ESTIMABLE` en los cuatro — la
respuesta correcta, por el camino correcto. Lo que estaba mal era la spec que lo
gobernaba. Su sello queda intacto.

**No edita `v1.0`** — queda íntegra en su ruta, con su sidecar verificando (E.3).
**No adopta el contraste acotado a receptores** (§4.1): cambia el estimando y es
materia de una spec nueva, no de esta versión. **No reescribe `se_mueve_si`**
(§5). **No mueve el tier de `R7.3`** (`[MEDIA]`, D2-f) **ni el de `R7.6`**
(`[MEDIA]`, D2-g, ambos brazos). **No reescribe D2-g** — esa cláusula la escribe
`TRAMITE-6`. **No adjudica cuál de los tres `.sav` es el canónico** — mantiene
lo que `v1.0` §0.2 estableció. **No toca `§2-bis`**: el experimento de encuadre
sigue exactamente como `v1.0` lo pre-registró, y su guardia de diseño ya disparó
en `CALC-0001` (`RESULT-C2BIS-DISENO = NO-ESTIMABLE-DISENO-NO-EXPERIMENTAL`,
cobertura `0.1325` contra el `cobertura_split_min = 0.2` congelado). **No toca**
`canon/modelo-decision-v4_0.md`, `milpa/**`, `data/**` ni `forense/hallazgos.md`.
**No abre ni toca** `S13-R10-3-spec-v1_0.md`.

**El primer resultado que produzca este procedimiento es el que se reporta.**
