# Registro de llaves de identificación ejercidas
### `registro-llaves-identificacion` · **v1.0** · 11 de agosto de 2026 · ENCARGO A (nube) · abre el contador que ADR-67(c) creó sin renglón

> | | |
> |---|---|
> | **ARCHIVO** | `registro-llaves-identificacion-v1_0.md` |
> | **NOMBRE ESTABLE** | **`registro-llaves-identificacion`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Registro append-only, una fila por llave de identificación (ADR-57(c)) o por diseño que la ejercería. Población de conteo propia — **`llaves de identificación ejercidas`** — abierta por ADR-67(c) (`canon/gobernanza-v1_15.md:868`), que la nombró sin darle renglón donde anotarse. |
> | **QUÉ NO ES** | No adjudica ningún veredicto de Hito D ni mueve su denominador. No sella nada: todo veredicto de aquí es **PROPUESTO** hasta que mesa lo firme. No es la taxonomía RUTA-A/I/C/SIN-RUTA (esa vive en `censo-estimabilidad-coeficientes-v1_0.md` y tampoco está sellada por ADR). |
> | **VERIFICAS ASÍ** | §4 trae el comando de conteo, corrido contra este mismo archivo antes de escribirse aquí — salida esperada hoy: `0`. |

---

## 0 · Qué es una llave

`ADR-57(c)` (`canon/gobernanza-v1_15.md:623`) sella la compuerta de identificación: cualquier afirmación de intervención ("si se interviene X, pasa Y") exige una **llave de identificación declarada y sellada**, de una de tres clases, citadas aquí verbatim de esa misma línea:

> "(i) panel con el desenlace en el instrumento (mismos sujetos entre olas); (ii) experimento natural con grupo de comparación sobre encuestas repetidas; (iii) diseño experimental de terceros (evaluaciones aleatorizadas publicadas, clase Progresa/Oportunidades), usado como evidencia (a) con su cita."

Un coeficiente o regla clasificado `RUTA-I` en `forense/censo-estimabilidad-coeficientes-v1_0.md` (definición en su §1, línea 26: *"Identificada, llave sellada y no ejercida"*) tiene la llave **sellada y no ejercida**: la vía existe y está verificada para ese caso concreto, pero ningún diseño que la use ha corrido todavía. **Ejercerla** es correr un diseño pre-registrado que use esa llave — no basta con nombrarla, y una fase meramente descriptiva sobre el mismo panel tampoco basta si no llega a emitir un veredicto de identificación.

Fuente de la taxonomía de rutas: `forense/censo-estimabilidad-coeficientes-v1_0.md`. Acto que crea este contador: `ADR-67(c)`.

---

## 1 · La regla de contadores — verbatim de ADR-67(c), no reinterpretada

`canon/gobernanza-v1_15.md:868` (ADR-67, inciso (c)), citado sin editar:

> "el denominador **27 no se toca** (cuenta fichas del pre-registro original, y `R5.1`→`A` de ADR-58 queda como historia con su estampa de universo — diseño transversal por recepción declarada, régimen de 5 instrumentos, con la reserva que ADR-58 dejó escrita); la métrica del renglón nuevo es **llaves de identificación ejercidas** (hoy 0), que `R5.1-D2` movería a 1 si corre conforme a su pre-registro sellado."

Este registro es una **población de conteo distinta** de la de Hito D. Ninguna fila de aquí mueve `13 de 27` (Hito D, `estado-programa-v1_10.md:95`), `15 coeficientes, cero medidos` (misma línea — el "0 de 15" que cita el encargo que abrió este acto es una paráfrasis; el texto vigente en el archivo dice literalmente "15 coeficientes, cero medidos", corregido aquí sin editar la fuente), `9 de 14` (corregido de `8 de 14`, vencido desde el 4/ago/2026; fuente vigente `modelo-decision-v4_0.md:277`, Encargo K, 4/ago/2026) ni `4 de 144` (`estado-programa-v1_10.md:97`).

Un veredicto anotado en la tabla de abajo es **PROPUESTO** hasta que mesa lo firme — la clase `A`–`E` del Hito D **no aplica aquí**; la escala de cada fila es la que su propio pre-registro declaró (Bloque B-bis, `instrucciones-proyecto-v2_4.md`).

---

## 2 · Vocabulario de `estado` — cerrado

| estado | significa |
|---|---|
| `SELLADA_NO_EJERCIDA` | pre-registro sellado, diseño no corrido |
| `EJERCIDA_CORROBORA` | corrió y el falsador no refutó; la regla queda corroborada en el alcance declarado |
| `EJERCIDA_ACOTA` | corrió, no refutó, y el resultado acota el alcance de la regla — se dice a qué |
| `EJERCIDA_REFUTA` | corrió y refutó |
| `EJERCIDA_INDECISA` | corrió y el falsador resultó demasiado débil para decir nada — se dice por qué |
| `NO_EJECUTABLE` | el diseño no se pudo correr; se dice si fue por dato, por entorno o porque nadie corrió el mecanismo (las tres son hallazgos distintos y no se colapsan) |

Solo `EJERCIDA_*` cuenta como llave ejercida.

---

## 3 · Tabla de llaves

Filas iniciales: la que el censo clasifica `RUTA-I` (1 de las 15 filas de coeficientes de generador, verificado en §4 con la receta del propio censo) más la fila que ADR-67(c) nombró y dejó sin renglón, `R5.1-D2`. Ambas nacen `SELLADA_NO_EJERCIDA` — ninguna llave de la lista está ejercida hoy (`gobernanza:623`, verbatim).

| llave_id | coeficiente_o_regla | diseño | preregistro_ref | estado | veredicto | escala_del_veredicto | fecha | ADR | clase_ADR57c |
|---|---|---|---|---|---|---|---|---|---|
| `CAL-G3` | `G3 → horizonte_temporal` (−0.60), fila 5 de `censo-estimabilidad-coeficientes-v1_0.md` §5, única fila `RUTA-I` de las 15 | panel (ENNViH/MxFLS, tres olas — llave (i) de ADR-57(c)); diseño intra-persona nuevo de `ACTO CAL-G3-PUNTUAL` (primeras diferencias ponderadas, olas 2-3, módulo `PR`/`CR`) | `forense/hitoD-preregistro-v2_0.md` Nota 7 (líneas 478-524, sellada 29/jul/2026), Adenda 1 (525-553), Nota 8 (554-648), Nota 10 (649+, Fase C corrida, descriptiva); spec propia en `forense/notas/2026-08-24-cal-g3-puntual-cierre.md` (PASO 1, Commit 1, congelada 24/ago/2026) | `EJERCIDA_ACOTA` | **Primeras diferencias intra-persona ponderadas (`fac_3b`), θ=`pr02` (horizonte temporal, 1-7) → desenlace=`cr27` (tiene ahorros, 0/1), ENNViH olas 2-3 (2005-06→2009-12). N=6,305. θ=+0.0146, IC95%=[+0.0047,+0.0245] (HC1/MAS, PASO 0 AGOTADO); sensibilidad bootstrap-hogar (500 réplicas) IC95%=[+0.0056,+0.0248] — no discrepa con la primaria. Co-observación intra-persona, no coeficiente causal (A-bis). Comparado con el asignado (−0.60) solo en signo por instrucción del encargo: **signos opuestos**; magnitudes sin enlace de escala declarado, no comparables. β queda PROPUESTO, no escrito en `milpa/procedencia.yaml` — fila de tablero en `forense/firmas-pendientes.tsv` para que mesa firme su entrada al ejecutable o su rechazo. Detalle completo, con conteos de cada filtro del universo: `forense/notas/2026-08-24-cal-g3-puntual-cierre.md` PASO 2.** | pp de probabilidad de "tener ahorros" por punto de categoría ordinal de horizonte temporal, intra-persona — **no** en la escala del `−0.60` asignado (sin enlace declarado entre ambas) | 24/ago/2026 | `ADR-157` | **(i)** — panel ENNViH, mismos sujetos entre olas (ya rotulada así desde que este registro abrió). `ACTO CAL-G3-PUNTUAL` no re-adjudica la clase, solo ejerce la llave por primera vez con un diseño propio. Adjudicada `ADR-144` |
| `R5.1-D2` | la regla `R5.1` del Hito D — la pregunta sustantiva de si la elegibilidad al programa sustituye transferencia intrafamiliar hacia mayores, no la operacionalización por recepción declarada de ADR-58 | cuasi-experimental, diferencias-en-diferencias por grupo de elegibilidad (ENIGH 2018 → 2022) | `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` (sellado 4/ago/2026, §9 sin enmiendas a la fecha) | `EJERCIDA_INDECISA` | **Fila B — Ambiguo, no refuta ni confirma.** Firma de mesa (ACTO ADJ-4, 13/ago/2026): *"Adjudico fila B, `EJERCIDA_INDECISA`."* Los dos desenlaces cumplen DiD<10pp-o-signo-contrario (transferencia +2.32pp, corresidencia −0.81pp — Commit 8 §2), pero la segunda condición conjuntiva de la fila A, "monto documentado como suficiente", **no se sostiene** con la medida sellada (razón monto/`gasto_mon`, no ingreso): 29.05% media ponderada, IC95% (26.16%, 31.94%) variante dominio / (25.95%, 32.14%) variante extensión-cero — entero por debajo del piso de 33% en las dos (Commit 9 §4/§7, Commit 10 §3-4). Por la precedencia sellada `A → E → B → C → D` (ADR-71(b)), la cláusula de "monto insuficiente" de B gana sobre A y sobre E sin excepción por magnitud del DiD. Fila propuesta y verbatim citada de `forense/notas/2026-08-12-e4c-r5-1-d2-commit10-incertidumbre-razon.md:56` (§4): *"No cambia la fila propuesta (B, `EJERCIDA_INDECISA`) ni la precedencia citada en Commit 9 §7."* — **no** del transfer del 12-13/ago, cuyo titular dice "fila A" (arrastrando el veredicto retirado de Commit 8) mientras su propio cuerpo, siguiendo Commits 9-10, confirma B; el repo es la fuente, no el titular del transfer. | **INCOMPLETA — no nombra el desenlace de no-refutación.** §6 del propio pre-registro, citado verbatim: fila `A` = "DiD <10pp... **La regla se refuta a este nivel de identificación también**"; fila `B` = "DiD entre 10 y 20pp... **Ambiguo — no refuta ni confirma**"; fila `C` = archivo por panel de persona no sostenido en disco; fila `D` = archivo por diseño (hueco de identificación de la clave de pensión contributiva, o muestra insuficiente). Ninguna de las cuatro filas nombra el caso "DiD ≥20pp con identificación exitosa y monto suficiente" — evidencia limpia de que la brecha **no** converge — como corroboración: ese desenlace cae fuera de A (exige <10pp), fuera de B (exige 10-20pp explícito), fuera de C (exige que la reserva dominante sea específicamente ausencia de panel) y fuera de D (exige fallo de diseño). Es el defecto de B-bis: se ve antes de correr, no después. E4c arranca con la instrucción de **reportar** este vacío, nunca de forzar una fila que la escala sellada no contempla. **CERRADO 12/ago/2026 por ADR-71(b):** el pre-registro gana fila `E` (§9, antes apéndice suelto a §6, reubicado por E4c Paso 3 §0.1) — DiD >20pp decisivo (IC95% que despeja el umbral) en al menos uno de los dos desenlaces, monto documentado como suficiente e identificación de §2 exitosa, corroboración acotada — con precedencia sellada **A → E → B → C → D**; la cláusula de "monto insuficiente" de B gana sobre E sin excepción por magnitud del DiD, igual que ya ganaba sobre A. La escala está completa desde esa fecha; la observación original de 4/ago queda arriba, sin borrar. | 4/ago/2026 | 67(c) | **(ii)** — *experimento natural con grupo de comparación sobre encuestas repetidas*. Los tres elementos de la definición sellada están escritos, no inferidos, en `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` §2: el **corte natural** es el cambio de regla de elegibilidad de 2019 (desaparece la prueba de ingreso por pensión contributiva de $1,092/mes); el **grupo de comparación** es explícito (*«elegible en ambos regímenes»*, quien ya era elegible bajo la regla vieja); las **encuestas repetidas** son ENIGH 2018→2022, transversales, no panel. Falla (i) por definición (2018 y 2022 no son los mismos sujetos) y (iii) por definición (no hay aleatorización de terceros). Adjudicada `ADR-144`, `ACTO ADQ-ENOE-PRE2019` T3 |

| `R5.1-D3` | la misma regla `R5.1` del Hito D, misma pregunta sustantiva que `R5.1-D2` — tercer diseño sobre ella, y segundo de la familia "por regla de elegibilidad" | cuasi-experimental, diferencias-en-diferencias por grupo de elegibilidad (ENIGH 2018 → 2022), con el criterio `D-1` firmado por mesa: umbral **deflactado** a pesos constantes de 2018 ($4,034.74/trim en 2022) y hogares mixtos T/C **excluidos** del desenlace de corresidencia, con universo ACOTADO declarado (A-bis r4) y el marginal recalculado sobre ese universo; sensibilidades obligatorias pre-declaradas: (i) umbral nominal, (ii) universo completo con la regla *any-member* | `forense/bbis-r5-1-d3-v1_0.md` (COMMIT A, congelado 19/ago/2026 antes de abrir microdato) sobre `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` (sellado 4/ago/2026), firma `ADR-110(a)`/`FP-54`, benchmark `forense/BENCHMARK-R51D3-hogares-mixtos-2026-08-18.md` | `EJERCIDA_INDECISA` | **Fila B — sellada por dirección, LOTE·NUBE-DECISIONES-1/T6 (FP-69), 19/ago/2026, verbatim "FIRMO FP-69: B se sella".** Corrida primaria (universo ACOTADO × umbral deflactado): DiD corresidencia **−1.82pp**, IC95% (−5.11pp, +1.48pp) — **cruza cero**; transferencia `P040` +2.32pp, IC95% (+0.54pp, +4.10pp); identificación de `P032` exitosa. La compuerta de monto **empeora** en vez de destrabarse: razón `P104`/`gasto_mon` per cápita pasa de 29.05% (población de `R5.1-D2`) a **26.45%** (personas T en hogar T del universo `U1`/ACOTADO), IC95% (23.15%, 29.75%) — entero bajo el piso de 33%. Por la precedencia sellada `A → E → B → C → D` (`ADR-71(b)`): la primera condición de `A` (DiD<10pp o signo contrario) se satisface, la tercera (identificación de `P032`) también, pero la segunda (monto suficiente) **no se sostiene** — la cláusula de "monto insuficiente" de `B` gana sobre `A` y sobre `E` **sin excepción por magnitud del DiD**. Las tres sensibilidades obligatorias caen en la misma fila (Commit B, `forense/notas/2026-08-19-ficha-r51-d3-resultados.md`). Reserva que va con la firma, heredada del propio pre-registro: el supuesto de tendencias paralelas está escrito y **no verificado** — el placebo 2014→2018 sigue sin correr. Mapeo al vocabulario de §2 aplicado: `B`→`EJERCIDA_INDECISA`, exactamente como esta misma fila ya anticipaba antes de sellarse (columna siguiente). | Heredada verbatim del pre-registro sellado, **no re-derivada**: filas `A`/`E`/`B`/`C`/`D` de §6 tal como quedaron tras `ADR-71(b)`, con precedencia `A → E → B → C → D` y la cláusula de "monto insuficiente" de `B` ganando sobre `A` y sobre `E` sin excepción por magnitud del DiD. Mapeo al vocabulario de §2: `A`→`EJERCIDA_REFUTA` · `E`→`EJERCIDA_ACOTA` · `B`→`EJERCIDA_INDECISA` (la fila que se selló) · `C`/`D`→`NO_EJECUTABLE` o archivo por diseño. Regla de adjudicación entre corridas, declarada al sellar (`bbis-r5-1-d3` §6): **adjudica la corrida primaria** (universo ACOTADO × umbral deflactado); las sensibilidades no votan — no discreparon, las tres caen en la misma fila | 19/ago/2026 | 67(c) (regla de renglón propio); 110(a) (criterio `D-1` firmado); ADR del lote, LOTE·NUBE-DECISIONES-1/T6 (sella, no re-deriva) | **(ii)** — misma adjudicación y por la misma razón: `bbis-r5-1-d3` §6 declara el mismo corte, el mismo grupo de comparación y las mismas dos olas transversales, con el criterio `D-1` encima. Adjudicada `ADR-144`, `ACTO ADQ-ENOE-PRE2019` T3 |

| `EXP-COMPARTAMOS-1` | **NO-ENCONTRADO — ninguna.** Es el hallazgo de la fila, no un hueco de redacción: se cruzaron las **37** filas de `data/curacion-registro/necesidad-objeto-modelo.tsv` (universo completo, `A.13`) y ninguna nombra este paquete, ni microcrédito, ni una evaluación aleatorizada — 0 coincidencias, con control positivo corrido en el mismo comando. Los dos objetos de crédito que el modelo sí tiene (`dinero.credito.scoring_alternativo`, `canon/modelo-decision-v4_0.md:500`, y `dinero.credito.baja_friccion_usura_dano_downstream`, `:501`) son reglas sobre precio y daño downstream, no sobre acceso aleatorizado; la necesidad `N19` que cubre al primero cita otra fuente (`NBER_RappiCard`, `milpa/procedencia.yaml:722`). Evidencia causal de primera clase **sin consumidor declarado** | experimento aleatorizado de terceros, por **conglomerado**: expansión de colocación de crédito grupal de Compartamos Banco en zonas periféricas de Nogales, Sonora. Derivado del microdato, no supuesto — `Treatment` constante en los 238 conglomerados de la ola de seguimiento (120 tratados / 118 control, N=16,560 mujeres de 18-60) y `BTreatment` constante en los 34 de línea base (17/17); errores estándar agrupados por la unidad de aleatorización en las 60 regresiones del paquete (`Compartamos_AEJ/Main/Compartamos-AEJ-tables-2-8.do:9-79`). Cumplimiento y atrición los reporta el propio paquete: `in_admin` 12.37%, `attrited` 1,090 de 2,912 (37.43%), más una tabla de atrición diferencial completa | **Al nacer, NINGUNO** — «la llave nace sin pre-registro y por eso nace no ejercida», y así quedó escrito el 25/ago/2026. **Cubierto 25-26/ago/2026:** la spec B-bis que esta misma columna reclamaba existe y está sellada — `forense/spec-bbis-exp-compartamos-v1_0-PROPUESTA.md` (nombre estable `spec-bbis-exp-compartamos-v1_0-propuesta`; conserva el sufijo `-PROPUESTA` en el nombre de archivo porque `FP-160` fue **enmienda de estado, no de archivo**), congelada antes de tocar el microdato y sellada por mesa en `ADR-199` §L4, firma verbatim *«SELLO FP-160: la spec B-bis de EXP-COMPARTAMOS-1 queda sellada tal como está propuesta.»*. Ejercicio: `forense/resultado-exp-compartamos-v1_0.md`, dos commits (§COMMIT-1 congela el procedimiento a ciegas del dato; §COMMIT-2 reporta y adjudica, sin editar una línea del primero — 0 líneas eliminadas en el diff entre ambos). Censo de diseño previo: `data/diseno-muestral.yaml` (fila `openicpsr — Compartamos AEJ`) y `forense/notas/2026-08-25-eval-compartamos.md` | `EJERCIDA_CORROBORA` | **Fila `corrobora` de la escala B-bis §4, alcanzada recorriendo la precedencia sellada `rompe → inejecutable → acota → corrobora → no-refuta` entera y descartando cada fila con su razón.** ITT por conglomerado, `regress Y Treatment i.supercluster_xi, vce(cl cluster)`, ola de seguimiento, **N=16,560**, **G=238** conglomerados (120 tratados / 118 control, `Treatment` constante en 238 de 238), t de **237** gl, sin ponderador (0 coincidencias de `[pw/aw/fw/iw]` sobre los 14 `.do` del paquete). **Daño primario — `A_ever_late_not_cond` (*client was ever late on payments*, registro administrativo, no condicionada a haber tomado crédito): ITT = +1.1009 pp, IC95% = [+0.6423, +1.5595], EE 0.2328 pp; nivel 0.337 → 1.404 pp (28/8,298 control vs 116/8,262 tratados).** Adopción: `in_admin` +11.4735 pp, IC95% [+9.7022, +13.2448] sobre base 5.845 pp; `Q21_3_comp` +8.2199 pp, IC95% [+6.6794, +9.7603]. Los tres van en la dirección que el mecanismo postula con IC95% que excluye cero. `rompe` no dispara: el desenlace de daño primario ni cruza cero ni va en dirección contraria. `inejecutable` no dispara: la variable de daño existe por nombre. **`acota` no dispara, y esa es la parte que vale: su rama de magnitud es INEVALUABLE** — el `[MEDIA](a)` vigente de `dinero.credito.baja_friccion_usura_dano_downstream` (`canon/modelo-decision-v4_0.md:501`) **no asume ninguna magnitud**, es puramente cualitativo, y rellenarla con el «techo de mora 15-20%» de `dinero.credito.scoring_alternativo` (`:500`) está prohibido por `A-bis` regla 3 — otro objeto, otra escala, sin enlace declarado. **Tres reservas que viajan con el veredicto, sin las cuales está mal citado:** (i) el desenlace de daño **secundario** `Q9_4_soldloan_none` (invertida) da +0.9908 pp, IC95% [+0.2357, +1.7460] — **signo contrario al postulado y con IC que excluye cero**; no decidió la fila únicamente porque §COMMIT-1 ancló la adjudicación en el primario **a ciegas del dato**, y admite la lectura alternativa de que el crédito **sustituye** la venta de activos; (ii) la corroboración descansa sobre **144 eventos** de mora en total, con tasa base de 0.34%; (iii) **dos de las tres condiciones estructurales del mecanismo no se miden** — el microdato no observa CAT ni calidad del reporte al buró, de modo que la corroboración es **de dirección, no de la cláusula condicional completa**, que es justo la forma de la «lectura peligrosa» que la propia regla advierte. Atrición 37.43% declarada sin corregir; TOT/LATE no estimado. **Número PROPUESTO, no escrito**: la `RANURA DE MESA` del encargo llegó **VACÍA** — `FP-160` selló la spec pero no eligió el destino —, así que `milpa/procedencia.yaml` queda intocado (octava clase `EVIDENCIA_EXPERIMENTAL_TERCEROS` sigue VACÍA) y el `[MEDIA](a)` también; fila `FP-164` de tablero para que mesa elija (a)/(b). Mismo patrón que `CAL-G3`/`FP-127`. Detalle completo, con los cuatro controles positivos (dos de valor esperado externo, coincidencia exacta con el censo de `ADR-162`): `forense/resultado-exp-compartamos-v1_0.md` §COMMIT-2 | **Puntos porcentuales (pp) de la variable de desenlace, ITT por conglomerado** — heredada verbatim de `spec-bbis-exp-compartamos-v1_0-propuesta` §3, fijada **antes** del dato y no re-derivada aquí. Los cuatro desenlaces son indicadores `{0,1}` verificados sobre el universo efectivo, así que `ITT × 100` está en pp directamente. ⚠️ **`A-bis` regla 3, expresamente:** esta escala **jamás** se compara contra el «techo de mora regulada 15-20%» ni contra el umbral de IMOR «~25-30% sostenido» de `dinero.credito.scoring_alternativo` (`canon/modelo-decision-v4_0.md:500`) — otro objeto, otro mecanismo, otra escala; este acto **no declara ningún enlace de escala** entre las dos reglas, ni para adjudicar ni para calificar la magnitud. **ESTAMPA `A.10` — universo del veredicto:** paquete `116334-V1.zip` (`data/manifiesto.yaml:12448`, `id: 116334_v1`, raíz `descargas_mx`, sha256 `776d56bf91535beaecef9480c352b022c3aec1ec7fae36c969ccdf6c8cc89d1c`, 1,404,772 bytes, `COINCIDE` en `tests/manifiesto.py --verifica`), archivo `Compartamos_AEJ/Main/data/analysis_data_AEJ_pub.dta`, **ola de seguimiento** (`survey == "Endline"`, 16,560 de 21,523 filas), **mujeres de 18-60 años de zonas periféricas de Nogales, Sonora**, 238 conglomerados. Fuera de ese universo el número no se cita: no es panel (sin identificador de persona), no es otra geografía, no es otro producto de `dinero.credito.*`, y no informa el `[MEDIA](a)` de `scoring_alternativo` | 26/ago/2026 *(alta 25/ago/2026)* | `ADR-200` *(alta `ADR-162`; spec sellada `ADR-199`)* | **(iii)** — *«diseño experimental de terceros (evaluaciones aleatorizadas publicadas, clase Progresa/Oportunidades), usado como evidencia (a) con su cita»*, verbatim de `canon/gobernanza-v1_15.md:629` (`ADR-57(c)`, el inciso; `:623` es el título del ADR, que es como §0 lo cita). **Primera fila de esta clase en el registro** — derivado con la receta de §4 sobre el archivo antes de escribirla: 0. No es **(i)**: no hay panel con el desenlace en el instrumento (la ola de seguimiento es transversal; solo 1,823 de 16,560 personas aparecen también en línea base, y el archivo público no trae identificador de persona). No es **(ii)**: la exposición no la pone una política sobre encuestas repetidas, la pone un sorteo de terceros — que es exactamente el rasgo que define la (iii). **Ejercida 26/ago/2026 (`ACTO MAESTRA30-E3 · EJERCE-LLAVE-COMPARTAMOS`) sin re-adjudicar la clase: sigue siendo (iii), y es la primera fila de esa clase del registro en salir de `SELLADA_NO_EJERCIDA`.** |

| `LLAVE2-DECRETO` | Ninguna regla de Hito D — el experimento natural que `ADR-57(c)` nombra directamente para `ENOE`, verbatim: *"salario mínimo de franja fronteriza"* | diferencias-en-diferencias sobre transversales repetidas de `ENOE`: tratamiento = los 43 municipios del Artículo Primero del decreto de estímulos fiscales de la Región Fronteriza Norte (`DOF` 31/dic/2018), control = municipios no listados de los mismos 6 estados; ventana pre `2017T1`–`2018T4`, post `2019T2`–`2020T1`/`2020T3`–`2020T4` | `forense/notas/2026-08-25-llave2-decreto-cierre.md` (COMMIT 1 congelado 25/ago/2026, antes de abrir microdato; COMMIT 2 la misma fecha) | `EJERCIDA_REFUTA` | **Diferencias-en-diferencias ponderado (`FAC`/`FAC_TRI`), errores por conglomerado (`UPM`, sensibilidad por municipio). `log(ing_x_hrs)`: β=+0.0043, IC95%=(−0.0205,+0.0291) cluster-UPM / (−0.0340,+0.0426) cluster-municipio — dentro de `±0.05` en las dos formas. `EMP_PPAL==1` (informalidad): β=−0.0013 (−0.13pp), IC95%=(−0.0200,+0.0174) cluster-UPM / (−0.0191,+0.0165) cluster-municipio — dentro de `±5pp` en las dos formas. Los dos desenlaces caen en `REFUTA` bajo las dos formas de conglomerado — sin discrepancia que resolver. Cobertura: 34/43 municipios tratados y 128/235 de control con observación en las 14 olas; compuerta `NO_EJECUTABLE` no se activa (3,266 UPM tratadas, 108,725–157,033 personas-ola según desenlace, ≫ los umbrales pre-declarados). Refuta el efecto del **paquete** de política fronteriza 2019 (estímulo fiscal + salario mínimo diferenciado, no separables con este diseño) sobre ingreso real por hora e informalidad de la población ocupada de los municipios tratados, en esta ventana y esta población — no lo refuta fuera de ellas. Detalle completo, con las 14 olas y las dos formas de conglomerado: `forense/notas/2026-08-25-llave2-decreto-cierre.md` COMMIT 2.** | log-puntos (≈ % aproximado) para ingreso; puntos porcentuales (pp) para informalidad — **no se cruzan entre sí** (`A-bis` regla 3) | 25/ago/2026 | `ADR-165` | **(ii)** — *"experimento natural con grupo de comparación sobre encuestas repetidas"*, verbatim de `canon/gobernanza-v1_15.md:629`. A diferencia de `R5.1-D2`/`R5.1-D3` (familia "por regla de elegibilidad", DiD sobre `ENIGH`), ésta es la primera fila de la clase (ii) construida sobre el ejemplo que `ADR-57(c)` nombra literalmente para `ENOE` — corte geográfico+temporal de una política pública, no una regla de elegibilidad de programa |

**Contador vigente: `5` llaves ejercidas de `5` filas.** *(Movido 13/ago/2026, ACTO ADJ-4 — `R5.1-D2` firma `EJERCIDA_INDECISA`, primera llave que sale de `SELLADA_NO_EJERCIDA` desde que este registro abrió. Verificación en §5. Denominador movido 19/ago/2026, ACTO FICHA-R51-D3 — entra la fila `R5.1-D3` naciendo `SELLADA_NO_EJERCIDA`; el numerador no se movió en ese acto porque proponía y no firmaba. **Numerador movido de nuevo 19/ago/2026, LOTE·NUBE-DECISIONES-1/T6 (`FP-69`)** — dirección sella fila `B`/`EJERCIDA_INDECISA` para `R5.1-D3` (firma verbatim "FIRMO FP-69: B se sella"), segunda llave que sale de `SELLADA_NO_EJERCIDA`. **CORRECCIÓN DE PREMISA, material:** el encargo que autorizó este sello anticipaba "2 de 2" — verificado por la propia receta de este archivo (§4), el denominador ya había subido a 3 el 19/ago/2026 (alta de `R5.1-D3`, antes de esta firma), así que sellar su numerador da **2 de 3**, no 2 de 2; no hay una segunda fila que retirar del denominador. **Numerador movido por tercera vez 24/ago/2026, `ACTO CAL-G3-PUNTUAL`** — `CAL-G3` ejerce por primera vez con diseño intra-persona propio (primeras diferencias ponderadas, olas 2-3), firma `EJERCIDA_ACOTA`; tercera y última llave que sale de `SELLADA_NO_EJERCIDA`, `3` de `3`, sin fila `SELLADA_NO_EJERCIDA` restante en la tabla. El β resultante queda PROPUESTO, no escrito en `milpa/procedencia.yaml` — pendiente de firma de mesa (`forense/firmas-pendientes.tsv`). Verificación por la receta de §4 en §7. **Denominador y numerador movidos juntos 25/ago/2026, `ACTO LLAVE2-DECRETO`** — nace y se ejerce en el mismo acto la fila `LLAVE2-DECRETO` (clase ii), primer diseño de la tabla construido directamente sobre el ejemplo geográfico+temporal que `ADR-57(c)` nombra para `ENOE` (no la familia "por regla de elegibilidad" de `R5.1-D2`/`R5.1-D3`); firma `EJERCIDA_REFUTA` — primera fila de esta tabla en llegar a `REFUTA`, y primer veredicto no-ambiguo de la clase (ii). `4` de `5`. **Numerador movido por quinta vez 26/ago/2026, `ACTO MAESTRA30-E3 · EJERCE-LLAVE-COMPARTAMOS`** — `EXP-COMPARTAMOS-1` sale de `SELLADA_NO_EJERCIDA` con firma `EJERCIDA_CORROBORA`, **primera fila de la clase (iii) en ejercerse** y primer `CORROBORA` de esta tabla. El denominador **no** se mueve: no nace ninguna fila en este acto. Con eso **no queda ninguna fila `SELLADA_NO_EJERCIDA` en la tabla**: `5` de `5`. Derivado con la receta de §4, no tecleado — numerador `5`, denominador `5`, con los cinco estados crudos impresos uno por fila como control positivo (§13). El ITT resultante queda **PROPUESTO**, no escrito en `milpa/procedencia.yaml` — la `RANURA DE MESA` del encargo llegó VACÍA y `FP-160` no eligió destino; fila `FP-164` de tablero para que mesa firme (a) o (b).)*

---

## 4 · Receta de conteo — probada antes de escribirse

**Primer intento, ingenuo — descartado y declarado, no silenciado.** `grep -c 'EJERCIDA_' registro-llaves-identificacion-v1_0.md` sobre el archivo completo contaría también la fila `SELLADA_NO_EJERCIDA` de la tabla de vocabulario (§2) si el patrón no exigiera el guion bajo final, y colapsaría llave_id con estado si se contara por línea física en vez de por columna — el mismo modo de falla que `instrucciones-proyecto` advierte para `grep -c "^## R"`. Se corrige acotando el conteo a la sección `## 3 · Tabla de llaves` y extrayendo la columna `estado` (sexta columna de la tabla, campo 6 tras dividir por `|`) en vez de buscar la subcadena en la línea completa.

**Receta corregida:**

```
sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
  | grep -E '^\| `' \
  | awk -F'|' '{print $6}' \
  | grep -c 'EJERCIDA_'
```

Denominador (filas de datos de la tabla):

```
sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
  | grep -cE '^\| `'
```

**Corrida contra este archivo tal como quedó escrito:** numerador `0`, denominador `2`. `llaves de identificación ejercidas: 0 de 2`.

La columna `estado` nunca contiene la subcadena `EJERCIDA_` (con guion bajo final) salvo en sus cuatro valores `EJERCIDA_*` — `SELLADA_NO_EJERCIDA` termina en `EJERCIDA` sin guion bajo posterior y no coincide con el patrón, verificado arriba. Cuando la primera fila `EJERCIDA_*` aparezca, esta receta la cuenta sin tocarse.

---

### 4.1 · Verificación del denominador `RUTA-I` citado en §3 (línea 55) — corregido, Acto A′

§3 dice que la fila `RUTA-I` (1 de las 15 filas de coeficientes de generador) queda "verificado en §4 con la receta del propio censo". Esa derivación nunca se copió a este §4 — vivía solo en `forense/hallazgos.md:121` (Encargo E-CE, 4/ago/2026). Se corrige citando aquí el comando y su salida cruda, corridos contra el estado actual de `forense/censo-estimabilidad-coeficientes-v1_0.md` (su propia receta, §7 de ese archivo):

```
grep -E '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_0.md \
  | grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c
```

Salida real:

```
      3 RUTA-A
      2 RUTA-C
      1 RUTA-I
      9 SIN-RUTA
```

`3 + 2 + 1 + 9 = 15` — coincide con las 15 filas de datos del censo (`grep -cE '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_0.md` = `15`). El reparto discrimina correctamente: `RUTA-I = 1`, la cifra que §3 línea 55 cita como denominador de la primera fila de la tabla.

---

## 5 · Firma de mesa — `R5.1-D2`, 13/ago/2026 (ACTO ADJ-4)

**Firma, verbatim:** *"Adjudico fila B, `EJERCIDA_INDECISA`."* Mesa firma sobre lo que el propio repo ya tenía derivado (E4c Paso 3, Commits 8-10) — este acto no corre ningún diseño nuevo, no recalcula ningún estimador, solo adjudica cuál fila de la escala ya sellada (ADR-71(b)) gobierna el resultado ya producido. Detalle completo de la fila en §3, columnas `estado`/`veredicto` de la fila `R5.1-D2`.

**La trampa evitada, declarada.** El transfer del 12-13/ago que trajo este encargo titula la fila con el veredicto de Commit 8 ("fila A", `EJERCIDA_REFUTA`) — superado dentro del propio E4c antes de que el transfer se escribiera: Commit 9 (`forense/notas/2026-08-12-e4c-r5-1-d2-commit9-monto-gasto.md:62`) retira A y propone B con la medida correcta (`gasto_mon`, no el proxy de ingreso de Commit 8 §4), y Commit 10 (`forense/notas/2026-08-12-e4c-r5-1-d2-commit10-incertidumbre-razon.md:56`, §4) lo confirma con intervalo tras calcular el IC95% de RM: *"No cambia la fila propuesta (B, `EJERCIDA_INDECISA`) ni la precedencia citada en Commit 9 §7."* Esta firma sigue al repo (B), no al titular del transfer (A) — ni intuición, ni el encargo, deciden la fila; la decide la escala ya sellada aplicada al resultado ya corrido.

**El contador se mueve según la receta propia de este archivo (§4), no por decreto de este encargo.** Corrida contra el archivo tal como queda escrito tras esta firma:

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -E '^\| `' | awk -F'|' '{print $6}' | grep -c 'EJERCIDA_'
1
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -cE '^\| `'
2
```

**`llaves de identificación ejercidas: 1 de 2`** — coincide exacto con lo que el encargo esperaba (`0 de 2 → 1 de 2`); la receta no dijo otra cosa. Se propaga a `canon/estado-programa-v1_10.md` (línea del contador de llaves) en el mismo acto.

---

## 6 · Alta de la fila `R5.1-D3`, 19/ago/2026 (ACTO FICHA-R51-D3) — denominador movido, numerador no

**Qué entra.** La fila `R5.1-D3`, naciendo `SELLADA_NO_EJERCIDA`, igual que nacieron `CAL-G3` y `R5.1-D2`. Su pre-registro es `forense/bbis-r5-1-d3-v1_0.md` (COMMIT A), congelado antes de que la sesión abriera ningún ZIP de `data/raw`, sobre el pre-registro sellado del 4/ago y con el criterio `D-1` que mesa firmó en `ADR-110(a)` (`FP-54`).

**Por qué renglón propio y no una edición de la fila `R5.1-D2`.** Por la misma razón que `ADR-67(c)` dio para abrir aquella: *"una fila por diseño escala; una fila por pregunta obliga a sobrescribir para siempre."* `R5.1-D3` no es una re-corrida de `R5.1-D2`: cambia la regla de hogar del desenlace de corresidencia y promueve el umbral deflactado de sensibilidad a especificación primaria. Sobrescribir la fila de `R5.1-D2` borraría el `EJERCIDA_INDECISA` que `ADJ-4` firmó.

**El numerador no se mueve en este acto.** El acto **propone**, no firma — misma disciplina que `E4c` Commit 8 respetó y que `ADJ-4` cerró. Si mesa firma un `EJERCIDA_*` para `R5.1-D3`, el numerador pasa a `2` en el acto de adjudicación, no aquí.

**Corrida de la receta de §4 contra el archivo tal como queda tras esta alta** — con `command grep`, no con el `grep` del entorno (que es `ugrep -I` y descarta archivos con un byte no-UTF8 en silencio; aquí ambos coinciden, verificado, y se declara el mecanismo igual):

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $6}' | command grep -c 'EJERCIDA_'
1
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -cE '^\| `'
3
```

**`llaves de identificación ejercidas: 1 de 3`** — derivado por la receta, no tecleado. Se propaga a `canon/estado-programa-v1_10.md` en el mismo acto.

**Lo que esta alta NO hace, y su razón sellada.** No escribe ninguna línea en el bloque append-only de `hitoD-preregistro` ni mueve `13 de 27`. El encargo que abrió este acto y `ADR-110(a)` declaran que `FICHA-R51-D3` es *"la vía al 14 de 27"*; `ADR-67(c)` selló lo contrario antes, y `T18`/`T20` lo confirman por mecánica independiente (el contador es un `set` de identificadores `RX.Y`, y `R5.1` ya está dentro desde el 4/ago/2026). La contradicción queda registrada como `FP-68`, **ABIERTA** — no se adjudica desde aquí.

---

## 7 · `FP-68` se adjudica y `FP-69` se sella, 19/ago/2026 (LOTE·NUBE-DECISIONES-1/T6)

**`FP-68` — la colisión de contadores se resuelve a favor de `ADR-67(c)`, sin adjudicación nueva que hacer.** No hay dos reglas válidas compitiendo: `ADR-110(a)`/el encargo `FICHA-R51-D3` declararon que este diseño era *"la vía al 14 de 27"*, pero esa declaración nunca fue una regla sellada de mesa sobre el denominador — era una premisa heredada, no verificada contra `ADR-67(c)`, que **ya** había sellado la regla real el 10/ago/2026 (`canon/gobernanza-v1_15.md:868`): un veredicto de diseño por regla de elegibilidad **no** cuenta como veredicto de `R5.1` para el bloque append-only de `hitoD-preregistro`, el denominador **27 no se toca**, y la métrica del renglón nuevo es **llaves de identificación ejercidas** — este mismo registro, creado por ese ADR para exactamente este propósito. Confirmado además por mecánica independiente, no solo por regla escrita: `T18`/`T20` (`tests/check.py`) derivan el contador de Hito D de un `set` de identificadores `RX.Y` vía `_VEREDICTO_CANONICO`, y `R5.1` **ya está** en ese set desde el 4/ago/2026 (`R5.1`→`A`, `ADR-58(c)`) — una línea nueva para `R5.1-D3` no incrementaría `13 de 27` aunque se escribiera, y una línea con la forma literal `` `R5.1-D3` → veredicto `` no coincide con el patrón que el parser reconoce y entraría **invisible**, sin disparar ni el guardia de forma sospechosa. **Propaga, sin tocar el original:** `ADR-110(a)` (`canon/gobernanza-v1_15.md:2151`) queda con su texto intacto — su declaración de que `FICHA-R51-D3` sería "la vía al 14 de 27" se corrige por ADR nuevo que la cita, patrón `ADR-112`→`ADR-110(d)` / `ADR-122`→`ADR-113` ya precedentado; detalle completo en el ADR del lote, subsección `T6`. **Contador de llaves que resulta de aplicar esta regla:** ver `FP-69` abajo — `FP-68` por sí sola no mueve el numerador, solo confirma dónde vive.

**`FP-69` — fila `B` sellada, numerador movido a `2`.** Firma de dirección, verbatim en el mensaje de lanzamiento del lote: *"FIRMO FP-69: B se sella"*. Ejecutada en la fila `R5.1-D3` de §3 arriba: `estado` `SELLADA_NO_EJERCIDA` → `EJERCIDA_INDECISA`; `veredicto` con la narrativa completa (DiD, compuerta de monto, precedencia, reserva de tendencias paralelas). Mismo mecanismo de firma que el precedente exacto que la propia fila `FP-69` cita: `ACTO ADJ-4` sobre `R5.1-D2`, 13/ago/2026 (§5 arriba) — mesa/dirección adjudica cuál fila de una escala **ya sellada** (`ADR-71(b)`, vía `bbis-r5-1-d3` COMMIT A) gobierna un resultado **ya corrido** (`bbis-r5-1-d3` COMMIT B); este acto no corre ningún diseño nuevo ni recalcula ningún estimador.

**Contador re-derivado por la receta de §4, no tecleado:**

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -E '^\| `' | awk -F'|' '{print $6}' | grep -c 'EJERCIDA_'
2
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -cE '^\| `'
3
```

**`llaves de identificación ejercidas: 2 de 3`.** **Corrección de premisa, material:** el mensaje de lanzamiento que autorizó este sello nombraba "2 de 2" como resultado esperado — verificado contra la receta de este archivo, el denominador **ya** había subido a 3 el 19/ago/2026 (alta de `R5.1-D3`, `ACTO FICHA-R51-D3`, antes y de forma independiente de esta firma) y ninguna fila sale del denominador al sellar `B`. El resultado correcto, derivado y no supuesto, es **2 de 3**. Se propaga a `canon/estado-programa-v1_10.md` en el mismo acto.

**Hito D no se mueve — dicho sin adorno, como el propio mensaje de lanzamiento exige.** `13 de 27` queda exactamente donde estaba: esta fila nunca entra al bloque append-only de `hitoD-preregistro` (ver `FP-68` arriba), y su veredicto `EJERCIDA_INDECISA` no es un veredicto de Hito D en absoluto — es un veredicto sobre si el **diseño** identifica algo, población de conteo distinta desde que `ADR-67(c)` la abrió (§1). Ninguna línea de `canon/hitoD-preregistro-v2_0.md` se toca por este acto.

**Lo que este acto NO hace.** No re-corre ningún diseño ni recalcula ningún estimador — la corrida ya vive en `bbis-r5-1-d3-v1_0.md` COMMIT B, congelada. No verifica el supuesto de tendencias paralelas (reserva declarada, placebo 2014→2018 sigue sin correr). No edita `ADR-67(c)` ni `ADR-110(a)` — los cita. No escribe en `canon/hitoD-preregistro-v2_0.md`.

---

## 8 · Adjudicación de clase contra la taxonomía de ADR-57(c), 20/ago/2026 (`ACTO ADQ-ENOE-PRE2019`, T3)

**Qué pedía `FP-64`, verbatim:** *«R5.1-D2 … nunca fue adjudicada contra la taxonomía de tres clases — su diseño (DiD por elegibilidad sobre transversales repetidas) encaja en la definición de la (ii) pero nadie lo ha escrito»*. Este acto lo escribe. La columna `clase_ADR57c` de §3 es nueva y **va al final de la tabla a propósito**: `T24` extrae `estado` por posición (campo 6 tras dividir por `|`, §4), y una columna insertada antes de `estado` habría roto la receta congelada y el vigía a la vez.

**Universo de la adjudicación, declarado (`A.13`):** las **3** filas de §3, todas — no una muestra. Las tres clases contra las que se adjudican son las de `canon/gobernanza-v1_15.md` `ADR-57(c)`, citadas ya verbatim en §0 de este mismo archivo y no re-interpretadas aquí.

| llave | clase | por qué, y por qué no las otras dos |
|---|---|---|
| `CAL-G3` | **(i)** | Panel ENNViH/MxFLS, tres olas, mismos sujetos. Ya estaba rotulada así dentro de la columna `diseño`; este acto solo la saca a columna propia. No re-adjudicada |
| `R5.1-D2` | **(ii)** | Los tres elementos de la definición sellada están **escritos** en `r5-1-diseno-por-regla-preregistro` §2, no inferidos por parecido: corte natural (el cambio de regla de elegibilidad de 2019, que elimina la prueba de ingreso por pensión contributiva de $1,092/mes), grupo de comparación explícito (*«elegible en ambos regímenes»*) y encuestas repetidas (ENIGH 2018→2022). No es **(i)**: 2018 y 2022 no son los mismos sujetos, y el propio pre-registro lo dice al llamarse "transversales repetidas". No es **(iii)**: no hay aleatorización de terceros |
| `R5.1-D3` | **(ii)** | Misma regla, mismo corte, mismo grupo de comparación, mismas dos olas transversales, con el criterio `D-1` encima (`bbis-r5-1-d3` §6) |

### 8.1 · La consecuencia que `FP-64` no sacó, y que cambia lo que vuelve a mesa

`FP-64` abre diciendo que **la llave (ii) *«sigue sin renglón operativo en ningún archivo del programa»***. Adjudicadas las tres filas, esa frase **queda refutada por el propio registro**: la (ii) no sólo tiene renglón, tiene **dos**, y son **las dos únicas llaves ejercidas del programa**.

| clase de `ADR-57(c)` | filas | `EJERCIDA_*` |
|---|---|---|
| (i) panel | 1 (`CAL-G3`) | **0** |
| (ii) experimento natural sobre encuestas repetidas | 2 (`R5.1-D2`, `R5.1-D3`) | **2** |
| (iii) experimento de terceros | 0 | 0 |

**Leído así, el `2 de 3` del contador es enteramente (ii).** Lo que faltaba no era una llave (ii): era que alguien mirara las que ya estaban y les pusiera la etiqueta. El contador **no se mueve** — adjudicar la clase de una fila existente no toca su `estado`, y `T24` deriva numerador y denominador **sólo** de `estado`. Verificado por la receta de §4 después de escribir la columna: `2` de `3`, igual que antes.

### 8.2 · Y la tensión con `ADR-57(c)`, nombrada porque este acto tuvo que resolverla para poder ejecutar

La Razón 1 de `FP-64` —ENOE es portador de desenlaces **sin exposición θ**— se ofrece como fundamento para *«retirar ENOE como candidato de la llave (ii)»* (opción (a)). Pero `ADR-57(c)`, sellado, dice de ENOE exactamente lo contrario, verbatim (`gobernanza-v1_15.md`, mismo inciso que define las tres clases):

> "ENOE — su panel rotativo queda refutado como ruta de conducta financiera (`CAL-ENOE` Fase A, 31/jul: **el instrumento no trae reactivo de ahorro/crédito/deuda/planeación**); **permanece elegible únicamente como portador de desenlaces laborales para experimentos naturales** (p. ej. salario mínimo de franja fronteriza)."

Las dos mitades de esa frase son la Razón 1 y su consecuencia, y `ADR-57(c)` las separó a propósito: la ausencia de reactivo de θ refuta la ruta **(i)** —el panel— y **no** toca la **(ii)**, porque en un experimento natural la exposición la pone la **política**, no el cuestionario. `FP-64` aplica un hallazgo verdadero a la clase para la que `ADR-57(c)` ya había dictaminado que **no** es descalificante, y el ejemplo que `ADR-57(c)` nombra —*«salario mínimo de franja fronteriza»*— es el mismo decreto del 1/ene/2019 que este acto acaba de habilitar con la adquisición.

**Consecuencia operativa, y es la que vuelve a mesa:** el `NO-ENCONTRADO` que T2 de este acto midió (`bbis-adq-enoe-pre2019` §6, Desenlace 2) **no descarta a ENOE de la llave (ii)** bajo el texto sellado — descarta a ENOE como fuente de **exposición θ**, que es otra cosa y ya estaba dicho. Este registro **no decide** cuál de las dos lecturas gobierna: `ADR-57(c)` es firma de mesa y sólo mesa lo enmienda. Lo que este acto hace es dejar de poder ignorarlo.

---

## 9 · `CAL-G3` se ejerce, 24/ago/2026 (`ACTO CAL-G3-PUNTUAL`)

**Qué hace este acto.** Corre, por primera vez, un diseño pre-registrado (spec B-bis congelada antes de abrir el microdato) que usa la llave `CAL-G3` para producir un veredicto de identificación — no descriptivo, como lo fue `hitoD-preregistro-v2_0.md` Nota 10. Detalle completo, con conteos, en `forense/notas/2026-08-24-cal-g3-puntual-cierre.md`.

**Fila `CAL-G3` en §3: `estado` `SELLADA_NO_EJERCIDA` → `EJERCIDA_ACOTA`.** Resultado: par intra-persona por primeras diferencias ponderadas, θ=`pr02` (horizonte temporal, ordinal 1-7, módulo `PR`, olas 2-3 de ENNViH) → desenlace=`cr27` (tiene ahorros, binario), N=6,305, β=+0.0146, IC95%=[+0.0047,+0.0245] bajo supuesto MAS (PASO 0 de esa nota = AGOTADO: ENNViH no trae UPM/estrato de diseño en ningún `.dta` ni documento, confirmado independientemente en este mismo acto), con sensibilidad de remuestreo por hogar que no discrepa. Signo opuesto al asignado del generador (−0.60); comparación solo en signo por instrucción del propio encargo, escalas sin enlace declarado.

**Contador re-derivado por la receta de §4, no tecleado:**

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -E '^\| `' | awk -F'|' '{print $6}' | grep -c 'EJERCIDA_'
3
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -cE '^\| `'
3
```

**`llaves de identificación ejercidas: 3 de 3`.** Ya no queda ninguna fila `SELLADA_NO_EJERCIDA` en la tabla de §3. Se propaga a `canon/estado-programa-v1_10.md` en el mismo acto.

**Hito D no se mueve.** El veredicto `EJERCIDA_ACOTA` de `CAL-G3` no es un veredicto de Hito D — población de conteo distinta desde que `ADR-67(c)` abrió este registro (§1). `13 de 27` (o el valor vigente al momento de leer esto) queda intacto; ninguna línea de `canon/hitoD-preregistro-v2_0.md` se toca por este acto.

**Lo que este acto NO hace.** No escribe el β en `milpa/procedencia.yaml` — queda `PROPUESTO`, fila de tablero en `forense/firmas-pendientes.tsv` para que mesa firme su entrada al ejecutable o su rechazo. No reemplaza el `−0.60` asignado del generador. No re-abre la Fase C descriptiva de `hitoD-preregistro-v2_0.md` Nota 10 (queda igual, sin veredicto, como esa nota la dejó).

---

## 10 · Alta de la fila `EXP-COMPARTAMOS-1`, 25/ago/2026 (`ACTO EVAL-COMPARTAMOS-LLAVE3`) — primer renglón de la clase (iii); denominador movido, numerador no

**Qué entra.** La fila `EXP-COMPARTAMOS-1`, naciendo `SELLADA_NO_EJERCIDA` igual que nacieron las tres anteriores. Es la **primera fila de clase (iii)** del registro — *«diseño experimental de terceros (evaluaciones aleatorizadas publicadas, clase Progresa/Oportunidades), usado como evidencia (a) con su cita»*, verbatim de `ADR-57(c)` (`canon/gobernanza-v1_15.md:629`; `:623`, que es como §0 lo cita, es el título del ADR). Objeto: la expansión aleatorizada de colocación de crédito grupal de Compartamos Banco en zonas periféricas de Nogales, Sonora, cuyo paquete de réplica AEJ ya estaba en el corpus (`116334-V1.zip`, raíz `descargas_mx`, sha256 verificado contra `data/manifiesto.yaml` en el acto). Detalle completo: `forense/notas/2026-08-25-eval-compartamos.md`; censo de diseño con los cinco campos citados: `data/diseno-muestral.yaml`, fila `openicpsr — Compartamos AEJ`, estado `DISENO_EXPERIMENTAL`.

**El conteo previo de la clase, re-derivado antes de escribir la fila — y el falso positivo que atrapó.** El encargo pedía re-derivar con `grep` y pegar el conteo. Hecho, con las dos recetas:

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## 4/p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $11}' | command grep -c '(iii)'
1
$ sed -n '/^## 3 · Tabla de llaves/,/^## 4/p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $11}' | command grep -cE '^ *\*\*\(iii\)\*\*'
0
```

**La cifra correcta es `0`, y el `1` es mención, no uso.** El único `(iii)` que había en la columna `clase_ADR57c` antes de hoy está dentro de la fila `R5.1-D2`, en la frase que la **descarta**: *"Falla (i) por definición ... y (iii) por definición (no hay aleatorización de terceros)"*. Un patrón sin anclar cuenta esa mención como si fuera una fila de la clase. La receta anclada al **uso** —la clase se declara siempre como `**(iii)**` en negritas al inicio del campo, igual que `**(i)**` y `**(ii)**`— da `0`, que coincide con lo que §8.1 ya había tabulado a mano el 20/ago/2026 ("(iii) experimento de terceros | 0 | 0"). Universo del negativo, declarado (`A.13`): **1** archivo, **3** filas de datos, la tabla completa de §3, no una muestra. Con esta alta la tabla de §8.1 queda: (i) 1 fila · (ii) 2 filas · **(iii) 1 fila**.

**Por qué el id es `EXP-COMPARTAMOS-1` y no el `CAL-EXP-1` que el encargo proponía.** El propio encargo autorizó derivarlo (*"o el id que la convención del archivo mande — derívala"*). Derivada sobre las tres filas existentes: el `llave_id` nombra **el objeto del modelo al que la llave sirve** (`CAL-G3` → el generador `G3`; `R5.1-D2`/`R5.1-D3` → la regla `R5.1` del Hito D, con ordinal de diseño), y el prefijo `CAL-` pertenece a la familia de actos de **calibración de un coeficiente nombrado** (`CAL-G3`, `CAL-CONF`, `CAL-ENOE`). Aquí **no hay coeficiente nombrado**: el cruce contra `data/curacion-registro/necesidad-objeto-modelo.tsv` dio `NO-ENCONTRADO` sobre las 37 filas. Un id `CAL-EXP-1` presupondría exactamente la pieza que falta. `EXP-COMPARTAMOS-1` nombra lo que sí existe —la evidencia, su clase y su ordinal de diseño— y deja el hueco visible en la columna `coeficiente_o_regla`, que es donde tiene que verse.

**Por qué nace sin `preregistro_ref`, y qué falta para ejercerla.** Las otras tres filas nacieron apuntando a un pre-registro sellado. Ésta no puede: no hay diseño que pre-registrar mientras no se declare **qué θ o qué generador del modelo informa** esta evidencia. Esa declaración es el contenido de la spec B-bis que la fila pide en su columna `preregistro_ref`, y es también lo que `FP-132` pone ante mesa. Escribir hoy una escala de veredicto sería fijar la escala antes de tener el diseño — el defecto que la propia fila `R5.1-D2` dejó documentado en esa columna.

**El numerador no se mueve en este acto.** Misma disciplina que `ACTO FICHA-R51-D3` (§6): el acto **abre el renglón**, no ejerce la llave. Y aquí hay una segunda razón, medida en el mismo acto y peor que la primera: aunque mesa firmara mañana qué θ informa, **el motor no tiene dónde consumirlo** — `milpa/procedencia.yaml` declara siete clases de procedencia y ninguna es evidencia identificada de terceros; el contrato de celda-D cierra `diseno_datos` en siete valores que incluyen `experimento_natural` (la clase (ii)) y **no** la (iii) (`propuesta-motor-adaptativo-celda-v0_3.md:56-57`, idéntico en `v0_4.md:49-50`); `milpa/refutations.yaml` tipa A/B/C, ninguno sobre clase de evidencia. `FP-131` lleva esa propuesta a mesa; este acto no la implementa y no toca `milpa/`.

**Corrida de la receta de §4 contra el archivo tal como queda tras esta alta** — con `command grep`, no con el `grep` del entorno (que es `ugrep -I`):

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $6}' | command grep -c 'EJERCIDA_'
3
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -cE '^\| `'
4
```

**`llaves de identificación ejercidas: 3 de 4`** — derivado por la receta, no tecleado. Se propaga a `canon/estado-programa-v1_10.md` en el mismo acto. La tabla vuelve a tener una fila `SELLADA_NO_EJERCIDA`, la primera desde el 24/ago/2026.

**Hito D no se mueve, y esta alta no lo toca por ninguna vía.** Población de conteo distinta desde que `ADR-67(c)` abrió este registro (§1). Ninguna línea de `forense/hitoD-preregistro-v2_0.md` se edita; el contador de fichas del Hito D queda como esté al leer esto.

**Lo que esta alta NO hace.** No estima ningún efecto del experimento — ni siquiera la toma de tratamiento por brazo. No adjudica que los reactivos de confianza que el instrumento sí trae a nivel de columna (`Q15_2_mean_formal`, "Trust in institutions index"; `Q15_2_mean_people`, "Trust in people index") sean el mismo constructo que `confianza_institucional` o `radio_confianza` del modelo: el parecido de nombre no es identidad de constructo, y establecerla exige abrir el reactivo y una decisión de mesa (`FP-132`). No toca `milpa/`, `canon/modelo-decision-v4_0.md` ni el contrato de celda-D. No corrige `data/mapa-ext-academico-2026-08-06.tsv:4`, que dice "250 vecindarios" donde el microdato trae 238 conglomerados — discrepancia declarada en el censo de diseño, fuera del perímetro de este acto.

---

## 11 · Firma de mesa — `L1`/`FP-127`, opción `b`, 25/ago/2026 (`ACTO SELLA-AGO25-F`)

**Firma, verbatim:** *"El primer β (signo opuesto al −0.60 sin escala): b) mantener con nota + acto de escalas."* Mesa rechaza tanto revisar el asignado (opción `a`) como declarar los dos valores inconmensurables sin más trámite (opción `c`): el β **se mantiene** registrado tal como `ACTO CAL-G3-PUNTUAL` lo dejó — `PROPUESTO`, no escrito en `milpa/procedencia.yaml` (`FP-127` en `forense/firmas-pendientes.tsv`, sin tocar por esta firma en cuanto a su valor) — y se le añade nota de discrepancia y un acto de escalas sucesor.

**Nota registrada, sin tocar `milpa/`.** La fila `CAL-G3` de §3 (arriba) queda anotada aquí, no editada hacia atrás: el β resultante (+0.0146) se registra con la etiqueta descriptiva **`MEDIDO·ACOTADO`** — no una clase de `milpa/procedencia.yaml` (que sigue teniendo siete clases, ninguna nueva por esta firma), sino una anotación de este registro que distingue "medido con diseño propio, pero con escala/signo sin enlace declarado frente al asignado" de un `MEDIDO` liso. Es descriptiva, no ejecutable: no cambia el `−0.60` de `milpa/procedencia.yaml:` `G3 → horizonte_temporal`, ni el pre-registro de `CAL-G3` en §3.

**Discrepancia de signo, visible junto al `−0.60`.** El `−0.60` vive, dentro de este mismo archivo, en la fila `CAL-G3` de §3 (columna `coeficiente_o_regla`: *"`G3 → horizonte_temporal` (−0.60), fila 5 de `censo-estimabilidad-coeficientes-v1_0.md` §5, única fila `RUTA-I` de las 15"*). Nota de discrepancia, pegada al mismo lugar donde ese valor se cita en este archivo: **el β medido (+0.0146) y el asignado (−0.60) tienen signos opuestos, y esta firma de mesa no los reconcilia** — solo confirma que el β medido se mantiene, `MEDIDO·ACOTADO`, mientras un acto de escalas declare si son comparables bajo alguna transformación.

**Acto de escalas — fila nueva `FP-135`.** Entra a `forense/firmas-pendientes.tsv`, `FIRMADA`, `ejecutada_en` vacío: declarar la escala de los 15 asignados de `milpa/procedencia.yaml` (la población completa de coeficientes `ASIGNADO`, de la que `G3 → horizonte_temporal` es una fila), para que una discrepancia de signo como esta se pueda leer contra una escala declarada en vez de compararse a ciegas. Este acto no la ejecuta — es trabajo de `ACTO ESCALA-ASIGNADOS`, sin fecha de arranque fijada.

**Lo que esta firma NO hace.** No escribe nada en `milpa/procedencia.yaml`. No re-adjudica `CAL-G3` (sigue `EJERCIDA_ACOTA`, sin cambio). No mueve el contador de llaves ejercidas (`3` de `4`, sin cambio — esta firma no ejerce ni abre ninguna llave, solo anota una ya ejercida).

---

## 12 · Firma de mesa — `L8`/`FP-132`, 25/ago/2026 (`ACTO SELLA-AGO25-F`) — CORREGIDA a opción `b`

**Primera lectura (superada).** La firma inicial de la hoja —*"¿Qué necesidad/θ reclama a Compartamos? (el acto dejó el mapeo candidato) → el que el acto propuso"*— se leyó como adopción del único candidato que `ACTO EVAL-COMPARTAMOS-LLAVE3` había dejado nombrado sin afirmar (`Q15_2_mean_formal`/`Q15_2_mean_people` ~ `confianza_institucional`(`G1`)/`radio_confianza`(`G1`,`G5`)). Dirección corrigió esa lectura: la opción firmada es **`b` — se abre necesidad nueva**, no la reutilización de una θ existente.

**Firma vigente, verbatim:** *"L8:b"*, sobre las opciones de `FP-132`: *"(a) que necesidad/theta lo reclama... (b) se abre necesidad nueva; o (c) se declara evidencia sin consumidor"*. Mesa firma **(b)**: la evidencia de `EXP-COMPARTAMOS-1` no se ata a `confianza_institucional`/`radio_confianza` ni a ninguna θ ya existente en el modelo — se abre una necesidad nueva, propia, en `data/curacion-registro/necesidad-objeto-modelo.tsv`.

**Qué queda escrito, y qué falta.** La fila `EXP-COMPARTAMOS-1` (§3, §10) espera una necesidad **nueva** del curador, no una reclasificación de `G1`. La observación de §10/§8 sobre el parecido de nombre con `confianza_institucional`/`radio_confianza` **sigue sin afirmarse** como identidad de constructo — esta firma no la usa. **Esto no ejerce la llave**: `preregistro_ref` de `EXP-COMPARTAMOS-1` sigue `NINGUNO` — abrir la necesidad nueva, declarar qué θ le corresponde y escribir la spec B-bis son trabajo de un acto propio. `FP-132` cierra `FIRMADA` con esta corrección; la llave sigue `SELLADA_NO_EJERCIDA`.

**`data/curacion-registro/necesidad-objeto-modelo.tsv` — no se edita en esta firma.** Abrir la necesidad nueva es un acto de curación de datos con su propio proceso (`data/curacion-registro/`) — escribirla aquí, sin ese proceso, fabricaría una fila del curador por fuera de su propio mecanismo. Fila nueva en el tablero, `FP-147`, `FIRMADA`, sin ejecutar: ese acto de curación.

**Lo que esta firma NO hace.** No abre el reactivo `Q15_2_mean_formal`/`Q15_2_mean_people` del microdato. No escribe spec B-bis. No mueve el contador de llaves ejercidas (`3` de `4`, sin cambio). No toca `milpa/`.

---

## 13 · `EXP-COMPARTAMOS-1` se ejerce, 26/ago/2026 (`ACTO MAESTRA30-E3 · EJERCE-LLAVE-COMPARTAMOS`) — la última fila sale de `SELLADA_NO_EJERCIDA`

**Qué se movió.** El estado de la fila `EXP-COMPARTAMOS-1`, de `SELLADA_NO_EJERCIDA` a **`EJERCIDA_CORROBORA`**, con su veredicto, su escala en pp, su estampa `A.10` y su fecha. **Es la primera fila de clase (iii) del registro en ejercerse**, y el primer `CORROBORA` de esta tabla — las cuatro anteriores dieron `ACOTA` (1), `INDECISA` (2) y `REFUTA` (1). La columna `preregistro_ref`, que decía *«NINGUNO — la llave nace sin pre-registro y por eso nace no ejercida»*, queda cubierta sin borrar lo que decía: la spec B-bis que reclamaba existe, está sellada (`FP-160` `FIRMADA`, `ADR-199` §L4) y está corrida.

**Lo que la firma de mesa habilitó y lo que no.** `FP-160` planteaba dos disyuntivas y mesa resolvió **una**: selló la spec (opción (a) de esa fila) y con eso habilitó este acto. **No eligió el destino del número** entre (a) competir por el `[MEDIA](a)` de `dinero.credito.baja_friccion_usura_dano_downstream` y (b) entrar como fila nueva a la octava clase de `milpa/procedencia.yaml`. La `RANURA DE MESA` del encargo llegó **VACÍA**. Por eso el número queda **`PROPUESTO`** y `milpa/procedencia.yaml` **no se toca** — la octava clase `EVIDENCIA_EXPERIMENTAL_TERCEROS` sigue vacía, como debe estar mientras nadie elija; tampoco se toca el `[MEDIA](a)` de `canon/modelo-decision-v4_0.md:501`. Es el patrón que `CAL-G3` ya dejó sentado (§9, `EJERCIDA_ACOTA` con β `PROPUESTO`, `FP-127`). Fila **`FP-164`** abierta para que mesa elija.

**Conteo, derivado con la receta de §4 y no tecleado.** Salida cruda:

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $6}' | command grep -c 'EJERCIDA_'
5
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -cE '^\| `'
5
```

**Control positivo del mismo comando** — porque un `5` sin ver qué contó no vale (`A.13`): el mismo `awk` imprimiendo `llave_id → estado`, una fila por línea, examinó las **5** filas de datos de la tabla y ninguna otra:

```
`CAL-G3`             ->  `EJERCIDA_ACOTA`
`R5.1-D2`            ->  `EJERCIDA_INDECISA`
`R5.1-D3`            ->  `EJERCIDA_INDECISA`
`EXP-COMPARTAMOS-1`  ->  `EJERCIDA_CORROBORA`
`LLAVE2-DECRETO`     ->  `EJERCIDA_REFUTA`
```

`llaves de identificación ejercidas: **5 de 5**`. **No queda ninguna fila `SELLADA_NO_EJERCIDA` en la tabla.** (En `UBUNTU` `grep` es una función que envuelve otro binario; todos los conteos de arriba usan `command grep`, declarado.)

**Lo que este acto NO hace.** No escribe el ITT en `milpa/procedencia.yaml`. No sustituye ni edita el `[MEDIA](a)` de `dinero.credito.baja_friccion_usura_dano_downstream`. No estima TOT/LATE (`in_admin` como instrumento está prohibido y no se usó). No usa `BTreatment` ni la línea base. No corrige por atrición. No compara la escala en pp de este veredicto contra el «techo de mora 15-20%» de `dinero.credito.scoring_alternativo` — otro objeto, otra escala, sin enlace declarado (`A-bis` regla 3). No re-adjudica la clase (iii) de la fila. No mueve el Hito D.

**La reserva que hay que leer junto al `CORROBORA`.** El desenlace de daño **secundario** (`Q9_4_soldloan_none`, venta de activo para pagar un préstamo, invertida) salió con **signo contrario** al que el mecanismo postula y con IC95% que excluye cero. Que la fila sea `corrobora` y no `rompe` depende **enteramente** de que `§COMMIT-1` ancló la adjudicación en el desenlace de daño **primario** —`A_ever_late_not_cond`, la mora administrativa— y lo hizo **a ciegas del dato**, antes de que ninguno de los dos números existiera. Esa regla se obedeció tal cual. Quien cite este `CORROBORA` sin la reserva lo está citando mal. Detalle: `forense/resultado-exp-compartamos-v1_0.md` §COMMIT-2 §5.
