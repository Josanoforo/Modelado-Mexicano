# E4c · R5.1-D2 — Commit 5: corrección de varianza en la DDD del Commit 4 §3 (Bloque D)

**No edita Commits 1, 3 ni 4.** Corrige, con la razón escrita, un defecto real que una auditoría de mesa sobre PR #176 encontró en Commit 4 §3 (triple diferencia) — atrapado antes de implementarse en `tests/`, que es exactamente para lo que sirve declarar la construcción sin implementarla primero. Verificado de forma independiente antes de aceptar el hallazgo: las dos citas de docstring y la ausencia de cobertura de test se confirmaron contra el código real, no se tomaron de la auditoría sin más.

## 1 · El defecto — verificado, no solo citado

Commit 4 §3 declaró, verbatim: *"dos llamadas a `did_ultimate_cluster` (una sobre 65+, una sobre 55-64) y la diferencia de sus `theta_hat`, con la varianza sumada por el mismo argumento de independencia entre-olas que ya sostiene `did_ultimate_cluster`."*

El argumento no se transfiere. `tests/svystat.py` distingue, en su propio código y docstring, dos situaciones con reglas de varianza opuestas — verificado línea por línea contra el archivo, no contra la cita:

- **Entre olas** (`did_ultimate_cluster`, líneas 215-218): *"var(theta_hat) = var(d_post) + var(d_pre) -- la suma es valida SOLO porque las dos olas son muestras transversales independientes, no panel."* Válida aquí porque ENIGH 2018 y ENIGH 2022 no comparten una sola unidad de muestreo.
- **Dentro de una ola, entre grupos que comparten diseño** (`diff_ultimate_cluster`, líneas 116-121): *"z_i captura la covarianza entre p_T y p_C inducida por compartir estrato/UPM -- es la razon de ser de esta funcion: T y C salen de la misma muestra dentro de una ola, así que var(p_T-p_C) != var(p_T)+var(p_C) en general."*

`θ̂(65+)` y `θ̂(55-64)` son del segundo tipo, no del primero: las dos bandas de edad salen de **la misma muestra**, los mismos estratos, las mismas UPM, en cada una de las dos olas — un hogar con una persona de 63 años y otra de 68 aporta observaciones a ambas bandas desde la misma UPM. Un choque a nivel UPM (mercado laboral local, cobertura administrativa local del programa, composición de hogares de la localidad) mueve ambas bandas a la vez dentro de la misma ola. `Cov(θ̂₆₅₊, θ̂₅₅₋₆₄) ≠ 0` en general, y sumar las varianzas tira el término `−2·Cov` — el SE queda mal, en dirección desconocida a priori (inflado si la covarianza es positiva, el caso más plausible bajo choques locales compartidos).

**Por qué esto adjudica y no es solo un detalle técnico.** El §6 sellado resuelve por decisividad: un IC95% que excluye el umbral. A-bis regla del Paso 3 (Commit 1): un punto que satisface el umbral con un IC que no lo despeja no adjudica, se reporta `PROPUESTO` con reserva. Un SE mal calculado (inflado, el caso plausible) empuja el resultado hacia "no decisivo" sin que nada sustantivo lo justifique — exactamente el desenlace que Commit 4 §7 ya declaró como el menos esperado a priori dado el estado de la literatura, y por tanto el que menos debería producirse por un artefacto de cómputo.

**Sin red que lo atrape:** `tests/test_svystat.py` no tiene ningún caso para triple diferencia — verificado (`grep -i "triple|ddd|55-64|banda"`, salida vacía). Un caso nuevo de este tipo es responsabilidad del acto que implemente, no de este commit (perímetro: no se toca `tests/`).

## 2 · La corrección — declarada, no implementada, misma disciplina que Commit 4 §3

**No hace falta un tercer nivel en `did_ultimate_cluster`.** La covarianza entre bandas de edad vive **dentro** de cada ola — es exactamente el tipo de covarianza que `diff_ultimate_cluster` ya sabe capturar, ampliada de un contraste de 2 celdas (T/C) a uno de 4 (T/C/T'/C'):

> **Dentro de cada ola**, construir un solo residual linealizado de 4 términos, agregado por UPM con la misma fórmula de conglomerado último que ya usa `diff_ultimate_cluster`:
>
> `z_i = [1{i∈T,65+}·w_i(y_i−p_T)/N̂_T − 1{i∈C,65+}·w_i(y_i−p_C)/N̂_C] − [1{i∈T',55-64}·w_i(y_i−p_T')/N̂_T' − 1{i∈C',55-64}·w_i(y_i−p_C')/N̂_C']`
>
> con `p_T, p_C, p_T', p_C'` las cuatro proporciones ponderadas de cada celda, y la varianza del contraste dentro-de-ola por la misma fórmula `sum_h [(m_h/(m_h-1)) · sum_i (z_hi − mean_i(z_hi))²]` que ya usa `diff_ultimate_cluster`. Esto captura toda la covarianza entre las cuatro celdas que comparten UPM — no solo T-vs-C, las cuatro a la vez.
>
> **Entre olas**, `DDD = d_post − d_pre` (donde `d` es ahora el contraste de 4 celdas de arriba, no de 2) con `Var(DDD) = Var(d_post) + Var(d_pre)` — y aquí sí el argumento de independencia entre-olas es el válido, sin cambio respecto a `did_ultimate_cluster`.

Conserva el argumento correcto donde ya lo era (entre olas) y pone la covarianza donde realmente vive (dentro de ola, entre las cuatro celdas) — extensión natural de `diff_ultimate_cluster`, no una función nueva de otra familia. **Sigue sin implementarse aquí** — es acto de motor pequeño sobre `tests/svystat.py` (nueva variante de 4 celdas + su caso conocido en `tests/test_svystat.py`), fuera de este perímetro. Esta declaración reemplaza, no complementa, la de Commit 4 §3 — la construcción de "dos llamadas a `did_ultimate_cluster` con varianzas sumadas" queda retirada.

## 3 · La reserva secundaria — precisión de la banda de control, decidida antes del dato

Commit 4 §3 midió la factibilidad de T'/C' (2,980 personas 55-64 sobre umbral en 2018, 4,084 en 2022) sin compararla contra el tamaño del grupo T principal (8,922 nominal / 8,877 deflactado, 2022 — Commit 3 §1.3). **T' es del orden de un tercio del tamaño de T.** Por construcción, `Var(θ̂₅₅₋₆₄)` será más grande que `Var(θ̂₆₅₊)` para un desenlace comparable — y sumado a la corrección de covarianza de §2 arriba, el DDD puede salir con un IC demasiado ancho para adjudicar en ninguna dirección, sin que eso sea un hallazgo sobre el fenómeno.

**Declaración pre-dato, ahora:** antes de correr, se declara la magnitud mínima detectable del DDD con la banda 55-64 tal como está especificada. Si no alcanza para despejar el umbral del §6 con la precisión que sí tiene el DiD principal (65+ T-vs-C, sin la resta de la cuarta celda), **el DDD entra como robustez declarada, no como estimando principal** — el §6 sigue adjudicando sobre el DiD de dos celdas, y el DDD se reporta junto con su propio IC como evidencia adicional sobre tendencias diferenciales por edad, no como el número que decide la fila. Decidido aquí, antes de ver el dato, para no tener que elegir después cuál de los dos manda.

## 4 · Lo que este commit no toca

Commits 1, 3 y 4 quedan íntegros — ninguna corrección hacia atrás. El resto de Commit 4 (§1, §2, §4, §5, §6) no se reabre: la auditoría de mesa los confirmó correctos, verificado independientemente aquí solo lo que señaló como defecto (§3). `tests/svystat.py` y `tests/test_svystat.py` no se tocan — la implementación de la variante de 4 celdas queda como acto propio de motor, con su propio caso conocido, antes de que Paso 3 pueda correr el DDD.

---

*Commit 5 de este acto (Bloque D). No edita Commits 1, 3 ni 4. Corrige la construcción de varianza de la DDD declarada en Commit 4 §3 y declara la reserva de precisión de la banda de control — ninguna implementada, ambas declaradas para cuando el acto de motor y la corrida real (Paso 3) lleguen.*
