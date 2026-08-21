# HITO D · `R7.1` — corrida completa del falsador y propuesta de fila

### `hitoD-R7.1-veredicto` · **v1.0** · 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7_1-veredicto-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R7.1-veredicto`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La corrida (COMMIT B) del falsador pre-registrado de `R7.1`, contra la base electoral por sección de Calderón-Hernández et al. (Zenodo `14991955`), ejecutada sin desviación de `hitoD-R7.1-especificacion`. |
> | **QUÉ NO ES** | **No adjudica.** Propone fila `A`. El bloque append-only de `hitoD-preregistro` **no se toca por este documento** y el contador `13 de 27` **no se mueve** por él. |
> | **VERIFICAS ASÍ** | `python3 tests/hitod_r7_1_concurrencia.py` reproduce cada cifra de abajo; salida cruda íntegra en `forense/notas/2026-08-20-r7-1-concurrencia-salida.txt`. |

**ESTAMPA DE UNIVERSO (`A.10`).** Sello tomado sobre `origin/main = 54da215`, 20/ago/2026, entorno **UBUNTU**. Universo examinado: **un** instrumento — `data/raw/zenodo_electoral_precinct_level_mexico_municipal.zip`, archivo interno `Final Data/all_states_final.zip → all_states_final.csv`, verificado `COINCIDE` (`sha256 8998b4dc…`) en este acto. Denominador del universo de medición: **454,546 filas sección×año**, **31** entidades, **1994–2019**. Denominador del universo de **instrumentos** para esta pregunta: **no existe** y se escribe en vez de omitirse — nadie ha censado cuántas bases electorales por sección hay para México, y `CONF-17` (5/ago) dejó `R7.1` explícitamente **sin candidata** (*"ninguna de las 17 fichas del barrido la toca"*). Este sello **no rige** ninguna elección posterior a 2019 ni ninguna elección judicial: ver §6.

---

## 1 · Qué se corrió, y contra qué

La spec congelada de COMMIT A, sin una sola desviación. El instrumento no había sido conectado nunca con `R7.1`: se adquirió el 12/ago/2026 por `ACTO P·LOTE-2` con el `usado_para` *"P-LOTE-2 (N25) … palanca 31"*, y ningún acto lo cruzó con el pre-registro del Hito D. **`R7.1` era la única de las 14 reglas abiertas sin candidata declarada en ningún barrido** — `CONF-17` la dejó fuera a propósito y lo escribió; `EXPLORA-1` (7/ago) la listó entre las nueve *"sin candidata desde ninguna de las 6 puertas"*; `matriz-impacto-universal` la marcó `MAPEADO-NO-SATISFACE`. Este acto cierra ese hueco con un instrumento que ya estaba en disco desde hacía ocho días.

---

## 2 · Control de canalización — antes de leer ningún resultado

La spec exigía no heredar la columna `turnout` sino recalcularla. Resultado: sobre las **454,546** filas del universo, `|total/registered_voters − turnout|` tiene **máximo 0.0000000000** y **cero** filas por encima de `1e-6`. La columna publicada **es** el cociente, byte a byte. La canalización queda validada contra el propio instrumento, que es el sustituto de ancla externa que este estimando no tiene.

**Contabilidad completa del universo, sin filas desaparecidas en silencio:** 456,051 filas crudas → 1,465 no parseables (**1,464 de ellas por `registered_voters` no numérico** — sin lista nominal no hay denominador; 3 por `state_code`/`mun_code`, 2 por `year`, 2 por `total`) → 31 excluidas por `registered_voters ≤ 0` → 9 por `precinct` ausente → **454,546**.

---

## 3 · El resultado

**Estimador primario — diferencia pareada dentro de la misma sección electoral:**

| | valor |
|---|---|
| **Δ̄ (concurrente − no concurrente)** | **6.5330 pp** |
| **EE (cluster-robusto CR1 por estado)** | **2.7490 pp** |
| **IC95% (t, G−1 = 17 gl)** | **[0.7331 pp, 12.3329 pp]** |
| **n** | **40,162 secciones pareadas** |
| **G (conglomerados)** | **18 estados** |

**Diseño aplicado.** Censo administrativo, **sin ponderador**: no hay `FAC_*`, `EST_DIS` ni `UPM_DIS` porque no hay muestra que expandir — declarado así en COMMIT A §4 y confirmado en la corrida. El tratamiento se asigna a nivel **estado×año** (el calendario electoral local es decisión de estado), y por eso el conglomerado del EE primario es el **estado**.

**El marginal, obligatorio y reportado:**

| estimador | Δ̄ | EE | IC95% | n | G |
|---|---|---|---|---|---|
| marginal, universo completo | 4.2140 pp | 1.5056 | [1.1392, 7.2889] | 454,546 | 31 |
| **marginal recalculado sobre el universo pareado (`A-bis r4`)** | **4.3664 pp** | **1.4719** | **[1.2610, 7.4717]** | **299,476** | **18** |

Medias crudas: participación **59.5210 pp** en elecciones municipales concurrentes, **55.3070 pp** en no concurrentes.

**No hay discordancia marginal/pareado que obligue a rotular ASOCIACIÓN por esa vía**: los dos estimadores tienen el mismo signo, magnitudes de 4.2 y 6.5 pp, y ambos IC95% quedan enteros por debajo del Umbral. Se reportan los dos, como el encargo exige, y **no se «elige el bueno»**. Lo que sí se rotula, y por otra razón, está en §5.

---

## 4 · Sensibilidades pre-declaradas, las cinco, más dos controles no pre-registrados

| # | prueba | Δ̄ | IC95% | n |
|---|---|---|---|---|
| **primario** | pareado por sección | **6.5330** | [0.7331, 12.3329] | 40,162 |
| S1 | marginal (§3) | 4.2140 | [1.1392, 7.2889] | 454,546 |
| S2 | pareado con la unidad agregada a municipio | 6.0752 | [0.6615, 11.4888] | 1,477 |
| S3 | secciones con ≥2 observaciones en cada brazo | 6.4628 | [2.6929, 10.2328] | 10,147 |
| S4 | solo observaciones desde 2015 (post-reforma) | 4.6531 | [0.5522, 8.7541] | 14,823 |
| S5 | par de años más cercano, separados ≤6 años | 6.3109 | [−1.3381, 13.9598] | 40,100 |

**Las cinco caen entre 4.21 y 6.53 pp y las cinco tienen su IC95% con tope por debajo de 15 pp.** Ninguna invierte la conclusión; ninguna sustituye al primario.

**Control post-hoc 1, declarado como NO pre-registrado.** La spec no anticipó filas con participación > 100% (`total > registered_voters`, desfase entre corte de lista nominal y jornada). Son **2,965 filas, 0.652%** del universo. Excluyéndolas: Δ̄ = **6.6811 pp**, IC95% [0.9579, 12.4042], n = 40,089. **No sustituye al primario** — la spec no se corrige hacia atrás.

**Control post-hoc 2, adversarial sobre el EE.** Bootstrap por conglomerado (2,000 réplicas, remuestreo de los 18 estados, semilla `20260820`): EE **2.6454 pp** contra los **2.7490 pp** del CR1 —concordantes—, IC95% percentil **[0.9970, 11.5544]**, y **0 de 2,000 réplicas alcanzan 15 pp**. El EE cluster-robusto con 18 conglomerados no está inflando ni desinflando la conclusión.

---

## 5 · Universo real contra universo pre-registrado — `ACOTADO` declarado

El universo pre-registrado era el archivo completo. El universo del **estimador primario** no lo es, y la diferencia no es cosmética:

- **Falta una entidad entera del instrumento: `09` Ciudad de México.** No tiene municipios —tiene alcaldías— y el paquete no la cubre. El universo son **31** entidades, no 32.
- **Solo 18 de esas 31 entidades tienen variación temporal de régimen** y pueden aportar secciones pareadas: Baja California Sur, Coahuila, Chiapas, Chihuahua, Guerrero, Jalisco, México, Michoacán, Morelos, Oaxaca, Puebla, Quintana Roo, Sinaloa, Tabasco, Tamaulipas, Veracruz, Yucatán, Zacatecas.
- **Las 13 restantes no aportan ninguna** porque su calendario municipal completo cae de un solo lado del corte: Aguascalientes, Baja California, Campeche, Colima, Durango, Guanajuato, Hidalgo, Nayarit, Nuevo León, Querétaro, San Luis Potosí, Sonora, Tlaxcala.

**Por `A-bis r4`, el resultado primario se declara `ACOTADO` a esas 18 entidades**, y por eso el marginal se recalculó sobre ese mismo universo (§3) en vez de compararse contra el nacional. La comparación que `A-bis r4` prohíbe —pareado de 18 estados contra marginal de 31— **no se hace**, y se dice que no se hace.

---

## 6 · Límites que este sello NO cubre, escritos antes de que alguien los herede

1. **No cubre elecciones judiciales.** La segunda mitad de la regla habla de *"elección técnica/judicial percibida como decidida"*. El instrumento llega a **2019** y contiene **elecciones municipales**, no judiciales. La elección judicial federal mexicana es posterior al techo del paquete. **Este acto no adjudica esa mitad de la regla**, y su resultado no debe leerse como si lo hiciera.
2. **La media de 55.31 pp en no concurrentes no refuta la cláusula de *"abstención >85%"*, y decirlo es obligación.** Esa cláusula está escrita sobre elecciones técnicas/judiciales, no sobre municipales no concurrentes. Se reporta la cifra porque es el marginal del brazo de control, no como contraejemplo de una cláusula que este diseño no toca.
3. **Concurrencia por año es proxy de concurrencia por fecha** (límite 1 de la spec §7). S4 lo acota sin eliminarlo.
4. **Las secciones se redistritan** (límite 2 de la spec §7). S5 lo acota sin eliminarlo.
5. **Oaxaca aporta al pareado, y sus municipios de usos y costumbres no votan por partidos** — están estructuralmente ausentes del instrumento, no excluidos por este acto. El estimando es sobre la vía de elección por partidos.
6. **Esto es asociación, no identificación (`A-bis r1`).** La concurrencia no se asigna al azar: arrastra consigo la campaña federal entera. La sección es su propio control, lo cual absorbe todo lo fijo de la sección, y **nada de lo que varía con el año**.

---

## 7 · Propuesta de fila, contra el árbol congelado en COMMIT A

**Rama 1 → fila `A`.** El IC95% del estimador primario **[0.7331, 12.3329]** queda **entero** por debajo del Umbral de 15 pp. La lectura, en las palabras de la propia ficha: **`A` — *"<15 puntos con electorado pareado"***, y su consecuencia declarada en el Umbral: ***"el tipo de acto no está haciendo el trabajo"***.

**Verificado, sin solape de filas.** `B` exige diferencia **grande**; no la hay, así que no se satisface junto con `A` — la partición del corte de 15 pp las hace mutuamente excluyentes, como COMMIT A §5.4 fijó. `C` (*"exigiría serie municipal pareada — granularidad municipal es hueco declarado"*) **no aplica**: la serie pareada existe, a granularidad **más fina** que municipio, y se corrió; la precedencia fijada al sellar dice que `A`/`B` mandan sobre `C` cuando el hueco está cerrado. `D` (*"posible por ese hueco"*) queda **excluida por construcción**, exactamente como COMMIT A §5.4(2) declaró antes de correr.

**Lo que `A` significa aquí, y lo que no.** Significa que el canal por el que la regla explica la participación diferencial —el peso percibido del acto, operacionalizado con el candidato que la propia ficha nombró— produce **6.5 puntos** sobre el mismo electorado, no los ~45 que la aritmética de la regla implica (*"~60%"* contra *"abstención >85%"*). **No significa que la concurrencia no haga nada**: el efecto es distinguible de cero (IC95% con piso en 0.73 pp) en cuatro de las seis especificaciones. Significa que **su tamaño no sostiene el peso teórico que `R7.1` le carga**. Es la diferencia entre *"el mecanismo no existe"* y *"el mecanismo existe y es un orden de magnitud más chico de lo declarado"* — y lo segundo es lo medido.

**Convergencia no buscada, anotada sin sobreinterpretar.** La media de participación en municipales concurrentes es **59.52 pp**, y la regla declara *"participación ~60%"* para el acto de alto peso. Coincide. Se anota como convergencia descriptiva del brazo tratado, **no** como corroboración: la regla no se cae ni se sostiene por su nivel, sino por la **diferencia**, que es lo que su Umbral pone bajo prueba.

**No se adjudica.** Una fila `A` es una afirmación sobre México, no sobre nuestros instrumentos: por el criterio que `ADR-55` fijó verbatim (*"se propone, mesa adjudica"*) y que `ADR-58`/`ADR-60`/`ADR-63` ejecutaron, **este documento propone y no archiva**. El bloque append-only de `hitoD-preregistro` no se toca aquí y el contador **no se mueve por `R7.1`**.

---

## 8 · Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** Todo el resultado, si se leyera como psicología. La concurrencia es una regla del calendario electoral —estructura pura— y lo que mide es cuánto arrastra la campaña federal a la urna municipal. Que el arrastre sea de 6.5 pp no dice nada sobre cómo un votante mexicano *siente* el peso de un acto; dice cuánto se mueve la conducta cuando la boleta viene acompañada.

**¿Qué sobregeneraliza desde clases medias urbanas?** Poco, y es la fortaleza del instrumento: 40,162 secciones de 18 entidades incluyen rural profundo, y el pareado da a cada sección su propio control. El sesgo va en la otra dirección: las 13 entidades sin variación de régimen —con Nuevo León, Guanajuato y Querétaro entre ellas— quedan fuera del primario, y son de las más urbanas del país.

**¿Qué cambiaría con foco rural, indígena o popular?** La ausencia estructural de los municipios oaxaqueños de usos y costumbres (§6.5) recorta justo el caso donde *"el peso del acto"* tendría otro significado. No es un hueco de este acto: es un hueco del régimen electoral, y `ADR-10` ya lo pone fuera del modelo.

**¿Qué parece psicológico pero es un incentivo racional?** El propio hallazgo. Ir a votar cuando ya vas a la casilla por la federal es barato; ir en un domingo dedicado a la municipal cuesta un viaje entero. 6.5 pp es un costo de transporte, no una jerarquía de significados.

**¿Qué afirmación de este artefacto describe el estado del corpus y no fue derivada?** Ninguna. Cada cifra de este documento sale de `tests/hitod_r7_1_concurrencia.py` y aparece en `forense/notas/2026-08-20-r7-1-concurrencia-salida.txt`. Las dos cifras que no produce este acto —`sha256` y bytes del instrumento— son del manifiesto y se verificaron `COINCIDE` en la corrida de `T0`.

---

**el primer resultado que produjo este procedimiento es el que se reporta.**
