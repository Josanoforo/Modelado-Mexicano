# E4c · R5.1-D2 — Commit 3: ajuste pre-ejecución (Bloque D)

**No enmienda ni edita `2026-08-11-e4c-r5-1-d2-especificacion.md` (Commit 1).** Cuatro puntos que mesa planteó tras revisar ese commit, cada uno resuelto hasta donde le corresponde a quien ejecuta y detenido, con la razón escrita, donde la decisión es de diseño y no de ejecución. Ningún resultado del diseño R5.1-D2 se produce aquí — todo lo que sigue es diagnóstico para especificar correctamente, no falsación.

---

## 1 · Umbral nominal vs. real entre olas — tres opciones, sin elegir

**El problema, tal como mesa lo planteó:** el corte de $1,092/mes viene del régimen 2014-2018. Clasificar a una persona de 2018 contra él es directo; clasificar a una de 2022 es contrafactual, y para que identifique la misma población en ambas olas el umbral tiene que ser comparable en términos reales. `ing_tri` está normalizado *dentro* del año (por decena de levantamiento), no deflactado *entre* años — Commit 1 §2.1 no lo distinguía.

### 1.1 · ¿El programa lo indexó de hecho? — verificado, no supuesto

Ya hay una nota en este repo que responde esto de forma directa: `forense/notas/2026-08-04-regla-elegibilidad-pension-adultos-mayores.md` §2, que leyó DOF primario, no un resumen. El umbral de $1,092/mes aparece **verbatim e idéntico** en tres cortes verificados contra la fuente primaria:

| Ejercicio fiscal | DOF | Cita literal (§3.2 Población Objetivo) |
|---|---|---|
| 2014 | Acuerdo 29/dic/2013, código DOF 5328387 | "...que no reciban pensión mayor a **$1,092 pesos mensuales**..." |
| 2015 | Acuerdo 27/dic/2014, código DOF 5377505 | "...que no reciban pensión mayor a **$1,092 pesos mensuales**..." (idéntico) |
| 2018 | Acuerdo 28/dic/2017, código DOF 5509626 | "...que no reciban pensión mayor a **$1,092 mensuales**..." (idéntico) |

2016 y 2017 no se abrieron en esa nota (huecos declarados ahí, no aquí) — con tres cortes idénticos (inicio, medio, fin del rango) la nota declaró continuidad inferida, no verificada línea por línea. **El umbral no se movió ni un peso en los cinco ejercicios fiscales en que existió (2014-2018), hasta que el requisito de ingreso se eliminó por completo en 2019** (misma nota, §3: "una pensión no contributiva de tendencia universal", sin prueba de ingreso).

**Conclusión para la opción (c): el programa nunca indexó este umbral mientras existió.** No hay una "regla de indexación de hecho" que extrapolar — (c) colapsa en evidencia hacia (a), no hacia una tercera vía independiente. Se declara así, no se decide con eso: que el umbral nunca se haya indexado es un argumento a favor de (a) ("el umbral administrativo nunca se indexó" — literalmente lo que mesa anticipó como su defensa), pero no es lo mismo que mesa decidiendo (a).

### 1.2 · El deflactor de (b) — INPC citado, no tecleado

**Fuente:** INPC (Índice Nacional de Precios al Consumidor), base 2ª quincena julio 2018 = 100, INEGI/Banxico. Los niveles crudos del índice (no solo variaciones porcentuales) no están expuestos en el comunicado de prensa de INEGI (`inpc_1q2022_11.pdf`, núm. 701/22 — reporta variación % quincenal/anual, no nivel) ni en las herramientas interactivas de INEGI (`CalculadoraInflacion.aspx` y el explorador `Estructura.aspx` requieren interacción de formulario que `WebFetch` no ejecuta — declarado, no rodeado con un número inventado). Los valores de nivel se obtuvieron de dos compilaciones independientes que citan INEGI/Banxico como fuente (`contaduriaccii.com.mx/inpc-historico/`, `cefa.com.mx/inpc.php`) — **coinciden exactas a 3 decimales entre sí**, y el valor de noviembre 2022 coincide además con un tercer fragmento de búsqueda independiente. Triangulación de tres fuentes, no una cifra sola:

| Mes | INPC (base jul-2018=100) |
|---|---|
| Noviembre 2018 | **102.303** |
| Noviembre 2022 | **125.997** |

Razón = 125.997 / 102.303 = **1.231606** → inflación acumulada nov-2018→nov-2022 = **23.16%**. (Mesa mencionó "del orden de 25-27%" como estimado de referencia; la cifra sourced da 23.16% — se declara la diferencia, no se ajusta la cita de mesa ni el número medido para que coincidan.)

**Umbral deflactado, opción (b):** $1,092/mes × 1.231606 = **$1,344.91/mes** ≈ **$4,034.74/trimestre** sobre la escala de `ing_tri` (vs. $3,276/trimestre nominal de Commit 1 §2.1).

### 1.3 · Cuántas personas cambian de grupo en 2022, (a) vs (b) — medido

Sobre el universo clasificable de 2022 (65+, con ≥1 fila en `ingresos`; ver §2.3 de Commit 1):

| | valor |
|---|---|
| Universo clasificable 2022 | 28,626 |
| Tratamiento bajo (a) nominal ($3,276/trim) | 8,922 |
| Tratamiento bajo (b) deflactado ($4,034.74/trim) | 8,877 |
| **Personas que cambian de grupo (a)→(b)** | **45** |
| — de ellas, T bajo (a) y C bajo (b) (dirección esperada: el corte sube) | 45 (100%) |
| Excluidos del universo (65+, 0 filas en `ingresos`), 2022 | 1,348 de 29,974 (4.50%) |

**45 de 28,626 = 0.157%.** Por el criterio que el propio mesa fijó ("si son pocas, la decisión es barata"), el conteo crudo de reclasificación es barato. Se declara igual, sin usarlo para decidir: 45 personas concentradas justo en la banda entre los dos cortes pueden pesar más de lo que su conteo sugiere si el desenlace de esas 45 personas específicamente es atípico — eso no se verificó aquí (exigiría abrir sus desenlaces, que es la corrida misma, no este diagnóstico).

### 1.4 · Las tres opciones, sin elegir — PENDIENTE mesa

- **(a) Nominal en ambas olas.** Defendible porque el umbral administrativo nunca se indexó mientras existió (§1.1) — la regla original tampoco distinguía inflación, así que aplicarla nominal reproduce literalmente el criterio 2014-2018. Reclasifica 45 personas menos que (b) tomaría como comparación.
- **(b) Deflactar a pesos constantes de la ola base (2018).** Umbral 2022 equivalente: $4,034.74/trim, fuente INPC citada en §1.2. Más defendible en el sentido de "misma vara real en las dos olas", como el DiD lo exige para no confundir tratamiento con cambio de composición.
- **(c) Indexar como el programa indexó de hecho.** Investigado en §1.1: el programa **no** indexó este umbral en ningún momento de su vigencia (2014-2018, tres cortes verbatim). No hay una regla de indexación real que seguir — (c) no es una tercera vía independiente de (a)/(b), es evidencia de que la premisa de (c) no se sostiene.

**No se elige. Queda para mesa, con los tres números puestos en la mesa: 0 (indexación real encontrada), 23.16% (inflación acumulada citada), 45 personas (costo de reclasificación).**

---

## 2 · Unidad de análisis — persona vs. hogar

### 2.1 · Ponderador `poblacion.factor` vs. `concentradohogar.factor` — medido

2018 no tiene `factor` en `poblacion` (confirmado contra el diccionario, Commit 1 §2.5 ya lo declaraba) — no hay comparación posible ahí, `concentradohogar` es la única fuente. **2022 sí tiene ambos.** Comparación fila a fila para las 29,974 personas de 65+ de 2022:

**Idénticos: 29,974 de 29,974. Discrepancias: 0.**

No hay ambigüedad de estimando que resolver en la práctica — aunque las dos columnas existen por separado en el diccionario, contienen el mismo valor. Se reporta el resultado crudo (no se asumió); Commit 1 §2.5 queda confirmado, no corregido: `concentradohogar.factor` sigue siendo la fuente declarada, por consistencia entre olas (2018 no tiene alternativa).

### 2.2 · Hogares con personas 65+ en grupos distintos — medido, regla PENDIENTE mesa

**El defecto que mesa señaló es real y no es marginal.** Bajo la clasificación de tratamiento/comparación a nivel persona (Commit 1 §2.2, umbral nominal usado aquí para medir — no prejuzga §1 de este commit), hogares con 2+ personas de 65+ clasificadas:

| Ola | Hogares con ≥1 persona 65+ clasificada | — con exactamente 1 | — con ≥2 | — de esos, con grupo MIXTO (T y C simultáneos) |
|---|---|---|---|---|
| 2018 | 16,469 | 12,286 | 4,183 | **1,312 (31.4% de los hogares con ≥2)** |
| 2022 | 22,363 | 16,274 | 6,089 | **2,201 (36.1% de los hogares con ≥2)** |

Casi un tercio (2018) a más de un tercio (2022) de los hogares con dos o más personas de 65+ tiene, bajo la regla de §2.2, una persona en tratamiento y otra en comparación **a la vez**. No es un caso de esquina.

**Tres reglas candidatas, sin elegir (mismo criterio que §1 de este commit — no lo decide el ejecutor):**

1. **Excluir los hogares mixtos** del desenlace de corresidencia. Reduce el universo de ese desenlace específicamente (no el de transferencia, que es coherente a nivel persona) en 1,312 (2018) / 2,201 (2022) hogares — y exige, si se adopta, decidir si ese universo restringido se declara como el desenlace ACOTADO de A-bis regla 4, o si el marginal completo (con todos los hogares) es el que se reporta con una reserva.
2. **Asignar el hogar por la persona de mayor ingreso contributivo** (`P032`) entre sus 65+. Mantiene el universo completo, pero el criterio de asignación ("el hogar es tratamiento si su persona 65+ de mayor pensión contributiva lo es") no está en §2 del pre-registro ni en Commit 1 — sería una regla nueva, declarada aquí, no heredada.
3. **El hogar entra en ambos grupos** (una vez en el numerador de T, otra en el de C, ponderado igual en los dos). Formalmente posible con `diff_ultimate_cluster` (nada impide que la misma UPM/estrato aporte a ambos lados), pero rompe la exclusividad mutua que Commit 1 §2.2 declaró como propiedad del diseño — un hogar "cuenta dos veces" no es neutral para la varianza.

**No se elige aquí.** Cualquiera de las tres es ejecutable; ninguna es gratis. Queda para mesa, con los conteos puestos en la mesa: 1,312 y 2,201 hogares, no una fracción que se pueda despachar como residual.

---

## 3 · El estimador — contrato, uso correcto, y una prueba de sensibilidad medida

### 3.1 · Disponibilidad

`tests/svystat.py` ya trae `diff_ultimate_cluster` y `did_ultimate_cluster` — PR #172 (`ENCARGO B`, fusionado en `origin/main` durante la redacción de este mismo commit; commit `0ce39cd`). Se leyó el código y su docstring completos antes de usarlo, no solo la firma.

### 3.2 · El contrato — tal como mesa lo señaló, verificado contra el código

`diff_ultimate_cluster(rows)` espera `rows` = `(estrato, upm, peso, y, grupo)`, `grupo ∈ {"T","C",None}`, **sin filtrar**: "unidades fuera de grupo (grupo=None) permanecen en el archivo y aportan residual cero — no se filtran (cambiar la estructura de estratos/UPM del diseño alteraría los grados de libertad; esto es estimación de dominio, no submuestreo)" (docstring, `svystat.py:100-103`). `did_ultimate_cluster(rows_pre, rows_post)` llama a `diff_ultimate_cluster` una vez por ola y devuelve, sin colapsar, `n_estratos_singleton_pre`/`n_estratos_singleton_post` por separado — exactamente para que un singleton de una sola ola no quede escondido detrás de un total sumado (docstring, `svystat.py:236-240`).

**Regla de uso, declarada para cuando corra Paso 3:** pasar TODAS las personas de la ola (`poblacion` completo, ambas olas, no filtrado a 65+), con `grupo="T"`/`"C"` para quien clasifique y `grupo=None` para el resto (menores de 65, o 65+ excluidos del universo por §2.3). El estrato/UPM/peso salen de `concentradohogar` (Commit 1 §2.5).

### 3.3 · Medido, no asumido: filtrar vs. no filtrar

Corrida de prueba con el desenlace de transferencia (`P040`, a nivel persona — no tiene la ambigüedad de §2 de este commit) y el umbral **nominal** de Commit 1 §2.1 (esta corrida es una prueba del mecanismo del estimador, no un resultado de R5.1-D2 — no usa el umbral que finalmente decida mesa en §1, no resuelve el desenlace de corresidencia, y no se reporta en `registro-llaves-identificacion-v1_0.md` bajo ningún concepto):

| | SIN filtrar (correcto) | FILTRADO a 65+ clasificados |
|---|---|---|
| `theta_hat` | 0.023228 | 0.023228 (idéntico — esperado, el punto no depende de quién más esté en el archivo) |
| `se` | 0.009089 | 0.009066 |
| IC95% | (0.005413, 0.041043) | (0.005459, 0.040996) |
| `n_estratos_singleton_pre` (2018) | **0** | 38 |
| `n_estratos_singleton_post` (2022) | **0** | 34 |

**La diferencia de SE es pequeña en esta corrida específica** (0.009089 vs. 0.009066, ~0.25% relativo) — se documenta como tal, no se oculta ni se exagera. **Pero el mecanismo que mesa describió es real y grande, no hipotético:** filtrar antes de estimar convierte 38 y 34 estratos (2018 y 2022 respectivamente) en singletons artificiales que la especificación correcta no tiene (0 y 0). Que el efecto neto sobre el SE haya sido chico en esta combinación de desenlace/umbral no garantiza que lo sea en otra — la regla de §3.2 se sigue siempre, no solo cuando el atajo se nota. Corrida extra: segundos, como mesa anticipó.

**Nota sobre el IC, tal como mesa la pidió:** `diff_ultimate_cluster`/`did_ultimate_cluster` no acotan su IC a `[-1,1]` (a diferencia de `prop_ultimate_cluster`, que sí acota a `[0,1]` — visible en el código, líneas 90 vs. 202). Para el veredicto de R5.1-D2 esto juega a favor: un IC sin acotar es más conservador al evaluar si excluye el umbral de §6 — no se acorta artificialmente cerca de un límite. Declarado para que no se lea como defecto cuando aparezca un IC más ancho de lo que un lector acostumbrado a proporciones esperaría.

### 3.4 · Hallazgo colateral, encontrado al preparar esta prueba — no es de R5.1-D2, se declara igual

**`poblacion` e `ingresos` de la ola 2018 pierden el cero inicial de `folioviv` para las entidades 01-09; `concentradohogar` no.** `folioviv` es `C(10)` por diseño (dos dígitos de entidad al frente). En el CSV real de 2018: 83,070 de 269,206 filas de `poblacion` (30.9%) y 107,549 de 348,487 filas de `ingresos` (30.9%) traen `folioviv` de 9 caracteres en vez de 10 — el cero inicial de las entidades 01-09 se perdió en algún paso de exportación de esas dos tablas específicamente. `concentradohogar` (74,647 filas) está íntegro, siempre 10 caracteres.

**Efecto medido:** un join ingenuo `poblacion`/`ingresos` ↔ `concentradohogar` por `folioviv` pierde el estrato/UPM/peso de esas 83,070 personas silenciosamente (`NaN`, no error) — exactamente el 31% que apareció la primera vez que se corrió la prueba de §3.3 sin este arreglo. **`poblacion` ↔ `ingresos` entre sí no se ve afectado** (los dos truncan igual, verificado: la tasa de "sin ninguna fila en `ingresos`" es 34.0% para las personas con `folioviv` de 9 caracteres contra 31.4% para las de 10 — comparable, no la caída a ~100% que un join roto produciría). **2022 no tiene este defecto** (`poblacion.factor` == `concentradohogar.factor` sin una sola discrepancia en 29,974 filas, §2.1 arriba, verificado con las llaves de join tal como vienen).

**Arreglo declarado, aplicado en este commit y en la prueba de §3.3:** `folioviv.str.zfill(10)` sobre `poblacion` e `ingresos` de 2018 antes de cualquier join contra `concentradohogar`. Reconstruye el valor real (`"100013601"` → `"0100013601"`, verificado contra el valor real que trae `concentradohogar` para el mismo hogar). **No se corrigió en ningún archivo de datos ni de otro acto** — es una regla de lectura para quien procese estas tres tablas de 2018 juntas, no una edición del corpus. Se declara aquí porque cualquier acto previo de este repo que haya cruzado `poblacion`/`ingresos` 2018 con `concentradohogar` 2018 por `folioviv` sin este ajuste tiene el mismo punto ciego — no se auditó el resto del repo por estar fuera del perímetro de este acto; se deja constancia para que mesa decida si amerita una revisión aparte.

---

## 4 · La regla de precedencia 2 de Commit 1 §3 — reformulada como propuesta, no como regla decidida

Commit 1 §3 declaró: *"un DiD decisivo (IC95% excluye el umbral) en ≥20pp... resuelve a `EJERCIDA_ACOTA`/`EJERCIDA_CORROBORA` incluso si la cláusula de 'monto insuficiente' de B también aplicaría."*

Mesa señaló, correctamente, que esto **modifica** la escala sellada de §6 del pre-registro (`A → B → C → D`, con "monto insuficiente" como cláusula de B sin excepción escrita) — no la aclara. El argumento de fondo (un DiD grande y decisivo con monto pequeño apunta al canal de elegibilidad/certeza de §2, no al canal de monto) puede ser correcto, pero decidir que ese argumento **basta para saltarse la cláusula de B** es una decisión sobre el propio §6 sellado, y §6 no se enmienda desde este acto (perímetro del encargo, Commit 1 lo declaró igual).

**Reformulado:**

> **PROPUESTA A MESA, no regla vigente:** si en la corrida real ocurre el caso "DiD≥20pp, dirección predicha, IC95% decisivo, identificación de §2.1 exitosa, PERO monto documentado insuficiente" — la situación exacta que Commit 1 §3 pretendía resolver por adelantado — este acto **no la adjudica**. Se para, se reporta el hallazgo crudo (los cuatro elementos: magnitud del DiD, dirección, IC, monto) y se espera la decisión de mesa sobre si ese patrón cae en `EJERCIDA_ACOTA` (canal de elegibilidad, como proponía Commit 1) o en `EJERCIDA_INDECISA`/fila B literal (monto insuficiente, sin excepción). No se autoadjudica por el ejecutor bajo ninguna lectura.

**El resto de Commit 1 §3 queda tal cual — mesa lo confirmó explícitamente correcto:** declarar las dos filas nuevas (`EJERCIDA_ACOTA`/`EJERCIDA_CORROBORA`) antes de ver el dato, mapeadas al vocabulario canónico del registro de llaves (confirmado idéntico en `forense/registro-llaves-identificacion-v1_0.md` §2, verbatim, verificado tras el merge de PR #170), con el umbral de 20pp declarado arbitrario. Es exactamente lo que B-bis pedía. Solo la regla de precedencia 2, específicamente su cláusula de excepción sobre "monto insuficiente", pasa de regla a propuesta.

---

## 5 · Qué queda pendiente — nada de esto corre hasta que se resuelva

- **§1 (umbral):** PENDIENTE mesa — (a)/(b)/(c), con (c) evidenciado como no viable de forma independiente.
- **§2 (unidad de análisis, hogares mixtos):** PENDIENTE mesa — tres reglas candidatas, sin default.
- **§3 (estimador):** RESUELTO — disponible, contrato entendido, regla de uso declarada (no filtrar, `grupo=None`), defecto de `folioviv` 2018 encontrado y con arreglo declarado.
- **§4 (precedencia 2):** PROPUESTA a mesa, no regla — si el caso ocurre en la corrida real, se para y se reporta, no se autoadjudica.

Paso 3 del encargo E4c (la corrida real, el veredicto, la fila del registro, la celda-D) sigue diferido como "parte 2" — ahora bloqueado no solo por el estado del terreno (ya resuelto, ver Commit 1 §0) sino por estas cuatro decisiones de diseño, tres de las cuales son de mesa.

---

*Commit 3 de este acto (Bloque D). No edita Commit 1. Si mesa resuelve §1/§2/§4, la resolución se registra en un commit propio que cite este documento — tampoco se edita este archivo retroactivamente.*
