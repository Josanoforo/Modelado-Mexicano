# ENCARGO B · Derivación de `svystat.diff_ultimate_cluster` y `did_ultimate_cluster`

*12 de agosto de 2026.* Ejecutor: sesión NUBE, sobre el clon existente
`/home/user/Modelado-Mexicano`, rama `estimador/diff-ultimate-cluster`.
Base declarada por el encargo: `bfc0037` (merge de #170). Base real al
arrancar: `6a95998` (merge de #171) — main avanzó tres commits
(`b55938f`, `a933d50`, `6a95998`), ninguno toca `tests/svystat.py` ni
`tests/test_svystat.py` (`git diff bfc0037..HEAD --stat` sólo mueve
`canon/estado-programa-v1_10.md`, `forense/hallazgos.md`,
`forense/registro-llaves-identificacion-v1_0.md`). No hace falta
re-derivar nada del perímetro de este acto.

Esta nota escribe la matemática **antes** de tocar `tests/svystat.py`,
para que quien revise pueda comprobar la fórmula sin leer Python (PASO 2
del encargo).

## 0 · El problema

`R5.1-D2` (`forense/r5-1-diseno-por-regla-preregistro-v1_0.md`) es
diferencias-en-diferencias por grupo de elegibilidad, ENIGH 2018 → 2022.
Las dos olas son muestras independientes (transversal repetida, no
panel) y sus varianzas se suman sin más. **Dentro de una ola no**:
tratamiento (`T`) y comparación (`C`) salen de la misma muestra y
comparten estratos y UPM, así que `var(p_T − p_C) ≠ var(p_T) + var(p_C)`
en general — la covarianza entre `p_T` y `p_C` inducida por compartir
diseño muestral es en general distinta de cero, y su signo no es
predecible antes de mirar los datos. Sumar varianzas sin más produce un
error estándar equivocado, y como el umbral A–D de §6 del pre-registro se
evalúa con el intervalo de confianza del DiD, un SE equivocado produce un
veredicto equivocado que se ve bien (no truena, sólo miente).

`tests/svystat.py` (verificado contra `6a95998`: `grep -n "^def "
tests/svystat.py` → sólo `prop_ultimate_cluster` y `_caso_conocido`) no
tiene estimador de contraste. Este acto añade dos funciones nuevas —
`diff_ultimate_cluster` para una sola ola, `did_ultimate_cluster` para
combinar dos — sin modificar `prop_ultimate_cluster`.

## 1 · Estimando dentro de una ola

Con `T` y `C` mutuamente excluyentes (una unidad no puede estar en ambos
a la vez — lo exige la definición de grupo del pre-registro §2/§3: el
corte de $1,092 es dicotómico):

```
N̂_T = Σ wᵢ·1{i∈T}          p_T = Σ wᵢ·yᵢ·1{i∈T} / N̂_T
N̂_C = Σ wᵢ·1{i∈C}          p_C = Σ wᵢ·yᵢ·1{i∈C} / N̂_C
d = p_T − p_C
```

## 2 · Residual linealizado por unidad — el corazón del asunto

Es lo que captura la covarianza entre `p_T` y `p_C` sin tener que estimar
esa covarianza por separado: se linealiza `d = p_T − p_C` como una suma
de contribuciones por unidad, de forma que la varianza de conglomerado
último ya vigente en el archivo (agregación por UPM) se pueda aplicar
directo sobre esa suma, y la covarianza entra automáticamente cuando dos
unidades — una de `T`, una de `C` — caen en la misma UPM.

```
zᵢ = 1{i∈T}·wᵢ·(yᵢ − p_T)/N̂_T  −  1{i∈C}·wᵢ·(yᵢ − p_C)/N̂_C
```

Nótese la forma: el término de `T` es exactamente el residual de
`prop_ultimate_cluster` (`e_h_i / N̂`) restringido a las unidades de `T`;
el de `C`, el mismo residual restringido a `C`, con signo invertido. Esa
identidad de forma es la que el Caso 2 de §4 explota para probar
coherencia contra el estimador que ya existe (ver nota de resolución en
§5 de este documento).

## 3 · Agregación por UPM y varianza de conglomerado último

Idéntica en forma a la que ya vive en el archivo (`prop_ultimate_cluster`,
`tests/svystat.py:19`, fórmula de Wolter, *Introduction to Variance
Estimation*, ultimate cluster, un solo nivel de conglomerado):

```
z_hi = Σ_{i ∈ UPM (h,i)} zᵢ
var(d) = Σ_h [ m_h/(m_h−1) · Σ_i (z_hi − z̄_h)² ]
```

donde `m_h` es el número de UPM del estrato `h` (mismo símbolo que
`n_h` en el docstring de `prop_ultimate_cluster`, renombrado aquí para no
confundir con `n_T`/`n_C`, conteos de observaciones).

## 4 · Las unidades fuera de grupo permanecen en el archivo

Regla explícita, porque es donde se equivoca todo el mundo: las unidades
que no pertenecen ni a `T` ni a `C` (`grupo=None`) aportan `zᵢ = 0` y
**permanecen en el archivo**. No se filtran. Filtrarlas cambiaría la
estructura de estratos y UPM del diseño muestral, podría convertir
estratos en singleton artificiales, y alteraría los grados de libertad
del diseño — es estimación de dominio (el dominio es "T ∪ C" dentro de
una población más grande), no submuestreo. Verificado numéricamente
(scratch, no commiteado): añadir filas `grupo=None` en UPM **ya
existentes** de `T`/`C` no cambia `d_hat` ni `se` (contribuyen `zᵢ=0` a
una UPM que ya estaba). Añadir filas `grupo=None` en UPM **nuevas**
dentro de un estrato ya existente tampoco cambia `d_hat`, pero sí cambia
`se` — cambia `m_h` (número de UPM del estrato), lo que desplaza `z̄_h` y
la suma de cuadrados. Efecto real de la fórmula, no cero por casualidad
ni ruido de implementación. Esto es exactamente el Caso 4 de §4.

## 5 · Cuatro decisiones de diseño — declaradas, no implícitas

**(1) Política de singleton.** `diff_ultimate_cluster` replica la
política de `prop_ultimate_cluster`: un estrato de una sola UPM salta
(no aporta a `var(d)`) y se cuenta en `n_estratos_singleton`. El llamador
**debe** leer ese contador — un singleton no detectado baja el SE en
silencio, exactamente el riesgo que motiva el umbral A–D del
pre-registro.

Declarado aquí, sin unificarse en este acto: `tools/curador_registro/
produce.py::taylor_distribution` (línea 122) adopta la política
contraria — lanza `ValueError("ESTRATOS_UNA_UPM:...")` y aborta. Son dos
políticas para la misma condición (estrato de una sola UPM) en el mismo
programa. Esto es un hallazgo que se anota (ver `forense/hallazgos.md`),
no algo que este acto resuelva — unificarlas es una decisión de mesa,
porque cambia el comportamiento de un módulo (`produce.py`) fuera del
perímetro de escritura de este acto.

**(2) Cuantil normal.** `1.959963985`, el mismo que `prop_ultimate_
cluster` (`tests/svystat.py:79`), no `1.96`. `taylor_distribution` usa
`1.96` (`produce.py:132-133`) — los resultados de las dos vías no
coincidirán en los últimos dígitos del IC95, y eso es esperado, no un
defecto de este acto.

**(3) `rows` se recorre dos veces.** Mismo defecto potencial que ya vivió
`prop_ultimate_cluster` (Encargo MT-mantenimiento, 5/ago/2026): un
generador se agota en el primer recorrido (cómputo de `N̂_T`/`N̂_C`) y el
segundo (agregación por UPM) lo vería vacío, sin lanzar excepción —
defecto silencioso. Se resuelve igual: `rows = list(rows)` al entrar a
`diff_ultimate_cluster`. `did_ultimate_cluster` no necesita la misma
materialización explícita sobre `rows_pre`/`rows_post`: cada uno se pasa
una sola vez, completo, a `diff_ultimate_cluster`, que ya materializa por
dentro.

**(4) Grupo vacío.** Si `N̂_T = 0` o `N̂_C = 0`, `diff_ultimate_cluster`
devuelve `None` — igual que `prop_ultimate_cluster` con `N̂ = 0`. No lanza
excepción, no devuelve cero. Extensión natural, no exigida explícitamente
por el encargo pero necesaria para que `did_ultimate_cluster` no falle en
silencio: si `diff_ultimate_cluster` devuelve `None` para cualquiera de
las dos olas, `did_ultimate_cluster` también devuelve `None` — no se
puede construir un DiD con una sola pata.

## 5.1 · Contradicción encontrada entre la decisión (4) y el Caso 2 del encargo — declarada, no silenciada

El encargo pide, en su Caso 2 (§4, PASO 4): *"Con todas las unidades en
`T` y ninguna en `C`, `diff_ultimate_cluster` debe devolver `d_hat` y
`se` idénticos a `prop_ultimate_cluster` sobre las mismas filas."* Tomado
literalmente, "ninguna en `C`" significa `N̂_C = 0` — que es exactamente
la condición que la decisión (4), también dictada por el mismo encargo
("si `N̂_T = 0` o `N̂_C = 0`, devuelve `None`... No lances excepción y no
devuelvas cero"), obliga a convertir en `None`. `None` no es igual a
ningún `d_hat`/`se` numérico: **las dos instrucciones, tomadas literales,
no pueden satisfacerse a la vez.** Verificado con la implementación real
(no sólo argumentado): `diff_ultimate_cluster` sobre un dataset con todas
las filas `grupo="T"` y ninguna `grupo="C"` devuelve `None`.

**Resolución adoptada, y por qué:** la decisión (4) se mantiene tal como
el encargo la dicta — está escrita tres veces con lenguaje imperativo
inequívoco, y protege un caso real: una ola de `R5.1-D2` sin ningún caso
en uno de los dos grupos no debería producir un número que se vea válido.
Ceder ahí para que el Caso 2 pasara literalmente habría sido debilitar
una regla explícita para maquillar un test, exactamente el defecto que
este mismo encargo denuncia en otra parte (§0: "un SE equivocado que se
ve bien"). En su lugar, el Caso 2 se adapta para probar la misma
propiedad de coherencia — que el cómputo del lado `T` dentro de
`diff_ultimate_cluster` es idéntico, fórmula por fórmula, al de
`prop_ultimate_cluster` — sin chocar con la decisión (4): se añade **una**
fila a `C`, en un estrato propio de una sola UPM (`n_h=1`, por tanto
saltada por la política de singleton de la decisión (1)) con `y=0`. Con
esa construcción:

- `N̂_C > 0` (la decisión 4 no dispara `None`);
- `p_C = 0/w_C = 0` exacto, así que `d_hat = p_T − 0 = p_T`, idéntico al
  `p_hat` de `prop_ultimate_cluster` sobre las filas de `T`;
- la UPM de `C`, al ser singleton en su propio estrato, no aporta nada a
  `var(d)` — el `se` resultante es, por construcción algebraica (§2: el
  término de `T` en `zᵢ` es literalmente el residual de
  `prop_ultimate_cluster` reescalado), idéntico al `se` de
  `prop_ultimate_cluster` sobre las mismas filas de `T`.

Verificado numéricamente antes de escribir el test: con el dataset de 12
filas / 2 estratos / 5 UPM que ya usa `test_caso_sintetico_dos_estratos`,
`prop_ultimate_cluster` da `p_hat=0.59375`, `se=0.0345543086...`; la
construcción de arriba (+1 fila `C` singleton) da
`d_hat=0.59375`, `se=0.0345543086...` — diferencia `0.0` en ambos, muy
por debajo de la tolerancia `1e-12` que el encargo exige para este caso.
`n_estratos_singleton` del resultado de `diff_ultimate_cluster` es `1`
(la fila de `C`) — se reporta y no se compara contra
`prop_ultimate_cluster` (que da `0` sobre sólo las filas de `T`, dataset
distinto), para no comparar contadores que miden datasets distintos por
construcción.

## 6 · DiD entre olas independientes

```
θ = d_post − d_pre
var(θ) = var(d_post) + var(d_pre)
```

La suma es válida **solo** porque ENIGH es transversal repetida y las dos
olas son muestras independientes. Cita literal, `forense/r5-1-diseno-por-
regla-preregistro-v1_0.md:72` (§4, "Olas pre y post"):

> "No es panel. ENIGH es transversal repetida — 2018 y 2022 son muestras
> independientes, no las mismas personas."

**Límite declarado, no implícito:** si este estimador se aplicara alguna
vez a un panel (mismas personas observadas en ambas olas), la suma de
varianzas deja de valer — un panel induce covarianza entre `d_pre` y
`d_post` a través de la misma unidad medida dos veces, y esta función no
la captura. `did_ultimate_cluster` no verifica que sus dos argumentos
sean transversales independientes (no tiene forma de saberlo desde
`rows_pre`/`rows_post` solos); el límite se declara en el docstring, no
se aplica en código.

## 7 · Caso 1 — derivación de la forma cerrada SRS

Un solo estrato, una UPM por observación, pesos uniformes `w=1`, `T` y
`C` disjuntos, ninguna unidad fuera de grupo. Bajo SRS, `z̄_h = 0`
(demostrado igual que el caso degenerado ya validado de
`prop_ultimate_cluster`: con una UPM por observación, `n_h = n` es el
número total de observaciones del único estrato, y la suma de residuos
ponderados por definición de `p_T`/`p_C` es cero dentro de cada grupo).
La fórmula de §3 colapsa a:

```
var(d) = [n/(n−1)] · [ p_T(1−p_T)/n_T + p_C(1−p_C)/n_C ]      con n = n_T + n_C
```

Verificado numéricamente (scratch): `n_T=4` (`y=[1,1,0,1]`, `p_T=0.75`),
`n_C=3` (`y=[0,1,0]`, `p_C=1/3`) — `diff_ultimate_cluster` da
`d_hat=0.41666...`, `se=0.37564245378607003`; la forma cerrada de arriba
da el mismo `se` a `1e-12` (diferencia `0.0` en la corrida real). El test
de §4/Caso 1 usa un dataset concreto con esta misma estructura, con la
derivación a mano en su propio docstring (mismo estilo que
`test_caso_sintetico_dos_estratos`).

## 8 · Caso 3 — por qué el dataset elegido no es el caso degenerado

Un primer intento con `T`/`C` **perfectamente** correlacionados dentro de
cada UPM (mismo valor de `y` en `T` y en `C`, UPM por UPM) da `se=0.0`
exacto para `diff_ultimate_cluster` — matemáticamente correcto (si `d`
es constante UPM a UPM, `zᵢ` linealizado también lo es, y la varianza de
un residual constante es cero) pero un caso demasiado degenerado para
ilustrar el punto del acto: parece un caso especial, no el caso general.
El dataset final (§4 del test) usa 8 UPM con pesos desiguales y
correlación positiva **no perfecta** (una UPM rompe el patrón a
propósito) — da `se(diff_ultimate_cluster) ≈ 0.1575` contra
`sqrt(var_T+var_C) ≈ 0.2709` (razón ≈0.58), una diferencia visible y
real sin ser el caso límite.
