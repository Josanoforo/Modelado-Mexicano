# HITO D · Paso 2 · Veredicto **R7.2**
### `hitoD-R7.2` · **v1.0** · 4 de agosto de 2026 · **Delito sin seguro → no denuncia**

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7.2-veredicto-v1.0.md` |
> | **REEMPLAZA A** | — *(nuevo)* |
> | **VERIFICAS ASÍ** | el veredicto es **D**, trae la verificación empírica (no solo textual) de que `BP2_1` es degenerada fuera de `BPCOD=01`, y declara — sin adjudicar — el hallazgo adyacente dentro de esa única clase |
> | **NOMBRE ESTABLE** | **`hitoD-R7.2`** |

> ⚠️ **ARTEFACTO FORENSE FECHADO — append-only.** Registra lo hallado el 4/ago/2026 contra microdato de ENVIPE 2025 (tabla `TMod_Vic`, ya abierta por la sesión que produjo `PR #57` — `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md`, contaminada para pre-registrar contra ella). No se actualiza: reescribirlo para que cuadre con el estado posterior sería la racionalización post-hoc que el Bloque C prohíbe.

---

## 0 · Verificación de premisas del encargo

**Ficha citada, verificada literal contra `forense/hitoD-preregistro-v2_0.md:178-188` en `origin/main` `6a09a37`** (`a05650f` — el commit que el encargo cita como verificado por "maestra #17" — es ancestro directo; `git diff a05650f HEAD -- forense/hitoD-preregistro-v2_0.md canon/estado-programa-v1_9.md` no da salida: el archivo no cambió entre ambos commits). La cita literal del encargo (SI-ENTONCES, falsador, umbral, reserva de cifra negra, escala A-D) coincide carácter por carácter con el archivo. Tipo (1).

**Contador de Hito D, verificado, no copiado:** `canon/estado-programa-v1_9.md:93` — *"2 de 27 corridas archivadas — `R1.1` → veredicto `D`, `R3.2` → veredicto `B`"* — coincide con el bloque append-only de este mismo archivo (líneas 693-694 antes de esta edición). **Contador de condicionales, verificado y NO tocado por este acto:** `canon/modelo-decision-v4_0.md:275,619` — *"~~6~~ 8 de 14"*, vigente tras `CAL-CONF` Fase B pos. 5-6. Este veredicto no mide ninguna de las 14 condicionales declaradas — no hay razón para moverlo, y no se mueve.

**Manifiesto, re-verificado esta sesión (no heredado sin comprobar):**
```
$ python3 tests/manifiesto.py --verifica | grep envipe2025_csv
envipe2025_csv [data_raw]: COINCIDE -- sha256 y tamaño (17600019 bytes) verificados contra data/manifiesto.yaml
```
Mismo hash y tamaño que reportó `PR #57` — mismo archivo, sin alteración entre sesiones.

---

## 1 · Lo que estaba pre-registrado *(citado literal, para probar que no se movió)*

> **Regla.** `hitoD-preregistro:179`: *"SI el delito no tiene cobertura de seguro y el agresor es identificable ENTONCES no denuncia — PORQUE miedo + inutilidad percibida (denunciar rinde 0.8%); SI es robo de vehículo asegurado ENTONCES sí denuncia"* — `[FUERTE]`.
>
> **Falsador.** *"Una clase de delito sin cobertura de seguro con tasa de denuncia alta, o una con cobertura con tasa baja."*
>
> **Umbral.** *"Brecha de denuncia entre delitos asegurados y no asegurados <20 puntos, pareando gravedad e identificabilidad del agresor."*
>
> **Reserva definicional (respetada en este acto, ver §2.6):** *"la cifra negra de 93.2% NO es P(no denuncia)... El falsador usa tasa de denuncia, no cifra negra."*
>
> **Escala de la propia ficha.** *"**A** brecha <20 puntos con pareo · **B** brecha presente sin parear gravedad · **C** ENVIPE desagregada por delito × cobertura × identificabilidad · **D** si ENVIPE no cruza cobertura de seguro con tipo de delito."*

**Nota sobre la escala:** a diferencia del legend genérico del encabezado del documento (`A` refutada · `B` sostenida no cerrada · `C` cerrada con búsqueda exhaustiva · `D` inejecutable), esta ficha define su propia escala específica, citada arriba — es la que gobierna este veredicto, siguiendo la instrucción explícita del encargo ("con la escala de la ficha") y el precedente de `hitoD-R3.2` (que también usó la redacción propia de su ficha, no el legend genérico).

---

## 2 · Veredicto: **D**

### 2.1 · Las tres variables, verificadas por descriptor literal contra el FD y el diccionario de datos — no por parecido de nombre

*(Aplicando explícitamente la lección `CAAS`/`CEU` del 3/ago — `forense/hallazgos.md:62` — "verificado sin abrir microdato... no se asume qué es sin verificar su descriptor": aquí sí se abrió microdato, pero la misma disciplina de leer el descriptor literal antes de usar una variable por su nombre corto se mantiene.)*

- **Tipo de delito → `BPCOD`.** Diccionario de datos, `NOMBRE_CAMPO`: *"Códigos para delitos"*. FD (`fd_envipe2025.pdf`, índice de `TMod_Vic`, l.4461). Catálogo completo (`bpcod.csv`), 15 clases, del `01` (robo total de vehículo) al `15` (otros delitos). Vive en `TMod_Vic`, universo completo: 40 280/40 280 filas con código válido.

- **Cobertura de seguro → `BP2_1`.** Diccionario de datos, `NOMBRE_CAMPO`: *"Vehículo robado asegurado"* — no *"cobertura de seguro"* en general. Vive en `TMod_Vic` (misma tabla). Catálogo: `1` Sí · `2` No · `9` No especificado · `b` blanco.

- **Identificabilidad del agresor → no existe una sola variable con ese nombre; dos candidatas con descriptor literal correspondiente:**
  - `BP1_12_1`…`BP1_12_5` — *"Delincuentes desconocidos"* / *"conocidos de vista solamente"* / *"conocidos de poco trato"* / *"conocidos cercanos"* / *"familiar(es)"* (multi-marca, pregunta 1.12 del cuestionario: *"¿Me podría decir si el (los) delincuente(s) era(n) para usted... desconocido(s)? / conocido(s) de vista solamente? / ... / familiar(es)?"*).
  - `BP1_13` — *"Reconocimiento de los (las) delincuentes"* (pregunta 1.13: *"¿Podría reconocer al (los) delincuente(s) si lo(s) viera?"* Sí/No).
  - **Elegida como proxy principal: `BP1_12` (conocido vs. desconocido), no `BP1_13`.** El mecanismo declarado por la regla es miedo a represalia de un agresor **identificable** — eso exige saber **quién es** (relación previa), no solo poder **reconocer su cara** si es un desconocido. `BP1_13` se reporta como robustez, no como variable primaria.

### 2.2 · `BP2_1` es degenerada fuera de `BPCOD=01` — verificado empíricamente, no solo por texto del cuestionario

**Verificación estructural (cuestionario, `cuest_modulo_envipe2025.pdf`):** la pregunta 2.1 vive en *"SECCIÓN II. ROBO TOTAL DE VEHÍCULO (Código 01)"*, precedida por la instrucción de salto *"SI EL CÓDIGO DEL DELITO ES 02, 03, 10, 11, 14 o 15 TERMINE EL MÓDULO SOBRE VICTIMIZACIÓN"* (es decir, para esos códigos el módulo ya terminó **antes** de llegar a la Sección II) y seguida, tras responder "Sí", de la instrucción **"TERMINE MÓDULO"**. No es una pregunta que se salte por no-respuesta: el instrumento no la formula para ninguna otra clase de delito.

**Verificado contra el microdato, no asumido del texto (`Counter` sobre las 40 280 filas):**

```
n válido de BP2_1 por BPCOD: {'01': 1028, todas las demás: 0}
Total BP2_1 válido = 1028 == n(BPCOD='01') = 1028, exacto.
```

**1 028 de 40 280 filas (2.6%) tienen `BP2_1` observable — el 100% de ellas son `BPCOD=01`.** Para las 14 clases de delito restantes (97.4% de la tabla), `BP2_1` no es "no aplica por no-respuesta": es un blanco estructural — el instrumento no tiene, para esas clases, un concepto de "cobertura de seguro" que preguntar.

### 2.3 · Por qué esto es **D** y no C

La ficha exige, para pasar de D a un caso evaluable, que *"ENVIPE [esté] desagregada por delito × cobertura × identificabilidad"* — una desagregación en la que la **cobertura varíe entre clases de delito** (es la lectura que exige el propio falsador: *"una clase de delito sin cobertura... o una con cobertura..."*, en plural, comparando clases). Lo que existe en `TMod_Vic` es lo contrario: `BPCOD` varía (15 clases), pero `cobertura de seguro` **no varía entre clases** — solo existe, como concepto medido, para una única clase. No hay "delito sin cobertura de seguro" como categoría poblada por el instrumento fuera de `BPCOD≠01`: no es que esas 14 clases tengan `BP2_1=No`, es que la pregunta nunca se les hizo. Cruzar `BPCOD` (15 valores) contra un `BP2_1` que solo tiene masa en un valor de `BPCOD` sería fabricar un cruce que la fuente no da — exactamente lo que el encargo instruye no hacer.

**Veredicto: `D` — "si ENVIPE no cruza cobertura de seguro con tipo de delito"**, aplicado literal: no lo cruza, en el sentido de variación conjunta que el falsador necesita para parear gravedad e identificabilidad **entre clases**. Es un `D` por diseño de instrumento, no por hueco de dato accidental — el patrón es el mismo que `hitoD-R1.1` documentó como "hueco de mercado, no hueco de dato": aquí es **hueco de instrumento** (ENVIPE solo formula "¿estaba asegurado?" donde, en México, el seguro contra ese delito es un producto real y extendido — el automotriz — y no lo pregunta donde no lo es).

Compuesto por una segunda capa, verificada en el mismo acto: **la identificabilidad (`BP1_12`) tampoco es universal.** Su `n` válido por `BPCOD` va de `0` (07 fraude bancario, 08 fraude al consumidor — el cuestionario los salta directo a la pregunta de denuncia, 1.20, sin pasar por la batería de descripción del delincuente) a `100%` (05 asalto en calle/transporte, 11-14 delitos de contacto violento — el cuestionario asume "Sí" en "¿estuvo presente?"/"¿pudo observar?" para esas clases), pasando por fracciones minoritarias (3-25%) en las clases de robo sin contacto (01, 02, 04, 06) — la identificabilidad ahí solo se observa para la submuestra que **presenció** el delito, y ver un vehículo o una casa robados sin estar presente es la norma, no la excepción. Aun si `BP2_1` no fuera degenerada, esta segunda capa de condicionamiento haría el cruce de tres vías (delito × cobertura × identificabilidad) aún más estrecho de lo que ya lo hace `BP2_1` por sí sola.

### 2.4 · Hallazgo adyacente — declarado, no adjudicado: la comparación que sí existe, dentro de `BPCOD=01`

**Esto no cambia el veredicto D** (no es la prueba que el falsador, tal como está escrito — comparando clases de delito — pide), pero es un cruce real que la fuente sí da y que prueba directamente el propio "disparador de vuelco" que la ficha cita como lo que la hace falsable (*"SI es robo de vehículo asegurado ENTONCES sí denuncia"*):

**Denuncia (`BP1_20`) por cobertura (`BP2_1`), dentro de `BPCOD=01` — ponderado `FAC_DEL`, IC95% por conglomerado último (`UPM_DIS`/`EST_DIS`), validado contra caso conocido (§2.7):**

| `BP2_1` | n | % denunció | SE | IC95% |
|---|---|---|---|---|
| Asegurado (1) | 402 | 79.1% | 2.15pp | [74.9%, 83.3%] |
| No asegurado (2) | 614 | 67.2% | 1.77pp | [63.7%, 70.7%] |
| *(No especificado, `9`, excluido)* | 12 | — | — | — |

**Brecha: 11.9 puntos, en la dirección predicha por el vuelco de la regla (asegurado → denuncia más), dentro de una sola clase de delito.** No alcanza a probar el falsador tal como está escrito porque no compara **clases de delito** — compara asegurados vs. no asegurados **dentro de** robo de vehículo, que es un universo mucho más angosto que "delitos sin cobertura de seguro" en general.

**Confundidor declarado, no descartado: identificabilidad difiere entre los dos grupos, y con `n` pequeño.** Dentro de `BPCOD=01`, la submuestra con `BP1_12_1` observable (quienes estuvieron presentes) es pequeña de cada lado (n=121 asegurados, n=124 no asegurados — la mayoría de robos de vehículo ocurre sin el dueño presente, §2.3). En esa submuestra, `%conocido` es 1.5% (asegurado) vs. 5.1% (no asegurado) — ambos bajos (consistente con robo de vehículo siendo mayoritariamente obra de desconocidos), pero no idénticos, y el pareo por identificabilidad que el umbral exige no se ejecuta aquí por ausencia de tamaño de muestra suficiente para condicionar tres vías dentro de una sola clase de delito.

### 2.5 · Contexto ya vivo en canon/milpa — señalado, no editado (fuera de perímetro de este acto)

**Esta misma regla ya tiene dos ids en `milpa/procedencia.yaml`** (`civico.denuncia.sin_seguro` + `civico.denuncia.con_seguro`), anomalía ya registrada en `forense/hallazgos.md:42` (31/jul) como uno de los tres casos conocidos de "dos ids, una regla" — no se toca aquí.

- **`procedencia.yaml:346,361`** — `civico.denuncia.sin_seguro` usa **exactamente** la cifra negra (0.93) como `no_denuncia`, con su propia reserva ya escrita en el archivo: *"RIESGO DEFINICIONAL... Usarla como P(no denuncia) confunde dos cantidades distintas... Verificar contra la tasa de denuncia publicada"* — la misma reserva que la ficha de este falsador repite. **Este acto no la verifica ni la corrige** (no se edita `milpa/`, fuera de perímetro) — solo confirma, con esta corrida, que la tasa de denuncia publicada (medida aquí para las 15 clases, §2.6) es la magnitud correcta a usar, y que no coincide con `1 − 0.93`.
- **`procedencia.yaml:448`** — `civico.denuncia.con_seguro` trae `valores: [0.78, 0.22]`, `ASIGNADO`, con nota propia: *"ENVIPE no publica esta condicional en esa forma"*. **Este veredicto confirma esa nota, y de paso ofrece el número que faltaba**: la tasa medida aquí para asegurado dentro de `BPCOD=01` es **79.1%** — a 1.1pp del valor asignado 0.78. Coincidencia notable, **no adjudicada**: cerrar ese `ASIGNADO` con este número es decisión de mesa, fuera del perímetro de un acto de Hito D (que no edita `milpa/`).

### 2.6 · Tabla de contexto — tasa de denuncia por clase de delito, las 15 (declarada, no es la prueba del falsador)

*(Ninguna de estas filas prueba ni refuta el falsador — el falsador exige variación conjunta de cobertura, que no existe fuera de `BPCOD=01`, §2.3. Se reporta como contexto declarado, mismo principio que `hitoD-R1.1 §6` usó para tablas de descarte.)*

| `BPCOD` | Delito | n | % denunció | SE | %conocido (n) |
|---|---|---|---|---|---|
| 01 | Robo total de vehículo | 1 028 | 72.1% | 1.47pp | 3.9% (255) |
| 02 | Robo accesorios/refacciones | 5 782 | 8.8% | 0.49pp | 11.8% (199) |
| 03 | Vandalismo | 4 799 | 2.4% | 0.28pp | 36.0% (229) |
| 04 | Robo casa habitación | 3 909 | 14.0% | 0.69pp | 30.4% (862) |
| 05 | Robo/asalto calle o transporte | 4 014 | 8.7% | 0.62pp | 6.1% (4 014) |
| 06 | Robo otra forma | 1 298 | 12.7% | 1.24pp | 10.0% (180) |
| 07 | Fraude bancario | 3 754 | 4.8% | 0.63pp | SIN DATO (salta a 1.20) |
| 08 | Fraude al consumidor | 3 070 | 4.3% | 0.43pp | SIN DATO (salta a 1.20) |
| 09 | Extorsión | 5 334 | 5.2% | 0.47pp | 8.8% (3 396) |
| 10 | Amenazas | 3 942 | 12.7% | 0.78pp | 55.2% (3 362) |
| 11 | Golpes/lesión por agresión | 1 316 | 19.4% | 1.58pp | 56.3% (1 316) |
| 12 | Secuestro | 76 | 23.0% | 2.62pp | 8.4% (76) |
| 13 | Hostigamiento/intimidación sexual | 1 606 | 2.6% | 0.39pp | 25.2% (1 606) |
| 14 | Violación sexual | 135 | 32.1% | 4.92pp | 63.1% (135) |
| 15 | Otros delitos | 217 | 19.2% | 4.17pp | 32.2% (145) |

Nótese que la clase con cobertura de seguro (01) tiene, sin condicionar por nada más, la segunda tasa de denuncia más alta de las 15 (72.1%) y una de las tasas de identificabilidad más bajas (3.9%) — consistente en dirección con la regla, pero **confundido con todo lo demás que distingue a un robo de vehículo de las otras 14 clases** (valor económico, existencia de trámite administrativo posterior — placas, tarjeta de circulación —, etc.), no aislado por este acto.

### 2.7 · Estimador validado contra caso conocido — antes de tocar nada nuevo

*(Regla de v2.1 — validar contra un caso ya conocido, la misma disciplina que ola 1/ola 2/`PR #57` aplicaron, sin el número de regla "v2.3" que el encargo cita y que no existe en `instrucciones-proyecto-v2.md` — nota igual a la que `PR #57 §0.1` ya dejó por escrito.)*

**Caso 1 — sintético.** `tests/svystat.py` corrido tal cual (commiteado en la ola 2, reutilizado sin modificar):
```
OK -- caso conocido (SRS, n=200, k=80, PSU=persona):
  p_hat calculado = 0.400000 (esperado 0.400000)
  se calculado    = 0.034728 (formula SRS p(1-p)/(n-1) = 0.034728)
Coincide a 9 decimales. Validado.
```

**Caso 2 — reproducción exacta de `PR #57` sobre la misma tabla (`TMod_Vic`), antes de calcular nada nuevo.** Esta sesión reprodujo la tabla marginal de `DOMINIO` de `BP1_20` que `PR #57 §3.1` ya publicó, con el mismo pipeline (lectura de CSV, ponderador `FAC_DEL`, estimador de conglomerado último):

```
Complemento urbano: n=8 039  p=9.2%  SE=0.55pp
Rural:               n=3 770  p=8.9%  SE=0.76pp
Urbano:              n=28 471 p=9.0%  SE=0.31pp
```

Coincide número por número con `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md §3.1` (marginal `DOMINIO`). Valida la lectura del CSV, el ponderador y el estimador de este acto contra un resultado ya publicado y a su vez validado por esa sesión — antes de aplicar el mismo pipeline a `BPCOD`/`BP2_1`/`BP1_12`, que ninguna sesión anterior había tabulado.

---

## 3 · Por qué **D** y no A / B / C

| | Por qué no |
|---|---|
| **A · brecha <20pp con pareo** | Exigiría que la brecha se calculara entre **clases de delito** pareadas por gravedad e identificabilidad, con cobertura variando entre ellas — no ejecutable (§2.3) |
| **B · brecha presente sin parear gravedad** | Misma razón: "brecha entre delitos asegurados y no asegurados" presupone cobertura variando entre clases, que no existe |
| **C · ENVIPE desagregada por delito × cobertura × identificabilidad** | La desagregación por `BPCOD` existe; la de cobertura, no varía entre clases (§2.2-2.3) — no es la desagregación conjunta que C describe |
| **D · si ENVIPE no cruza cobertura de seguro con tipo de delito** ✅ | Verificado empíricamente: `BP2_1` válida en 1 028/40 280 filas, 100% de ellas `BPCOD=01`. No hay variación de cobertura entre clases de delito que cruzar |

---

## 4 · Tabla de propagación *(ADR-34)*

| Veredicto | Regla / ítem del canon, citado | Edición que exige | Aplicado |
|---|---|---|---|
| **Archiva** | `hitoD-preregistro-v2_0.md` — bloque append-only, ADR-40 | Añadir línea `R7.2` → `D` | ✅ este acto |
| **Propaga** | `canon/estado-programa-v1_9.md` — contador de Hito D (§L5, §7) | `2 de 27` → `3 de 27`, listar `R7.2` → `D` junto a `R1.1`/`R3.2` | ✅ este acto (único contador que este acto mueve) |
| **No propaga** | `canon/modelo-decision-v4_0.md` — contador de condicionales (`~~6~~ 8 de 14`) | Ninguna — este veredicto no mide ninguna de las 14 condicionales | — (no tocado, por instrucción explícita) |
| **Señala, no adjudica** | `milpa/procedencia.yaml:346,361,448` — `civico.denuncia.sin_seguro`/`con_seguro`, dos ids ya conocidos (`forense/hallazgos.md:42`) | Decisión de mesa: si el hallazgo adyacente de §2.4-2.5 (79.1% medido vs. 0.78 asignado) cierra el `ASIGNADO` de `con_seguro`, y si la reserva ya escrita de `sin_seguro` sobre la cifra negra se resuelve con la tabla de §2.6 | ⬜ pendiente, fuera de perímetro de Hito D |
| **No toca** | `ENIGH` | — | — (fuera de perímetro, otra sesión Ubuntu corre P3 sobre ese instrumento) |

---

## Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** El mecanismo que la regla declara (miedo + inutilidad percibida) es explícitamente racional, no un rasgo cultural — y el propio hallazgo de este acto lo refuerza desde otro ángulo: la razón por la que ENVIPE no permite probar la versión general de la regla no es que "los mexicanos no aseguran nada" (lectura culturalista), sino que el seguro contra el delito, como producto de mercado en México, existe de forma extendida casi únicamente para vehículos — un hecho de estructura de mercado de seguros, no de cultura, y el mismo tipo de hallazgo que `hitoD-R1.1` ya documentó para el seguro agrícola.

**¿Qué sobregeneraliza desde clases medias urbanas?** Menos que otros falsadores de este perímetro: `TMod_Vic` cubre los tres dominios (`Urbano`, `Complemento urbano`, `Rural` — n=3 770 en rural, tabla §2.6 de `PR #57`), a diferencia de ENCIG 2023 (`hitoD-R3.2`), que excluye por diseño muestral a poblaciones fuera de ciudades de 100 000+ habitantes. Este veredicto D no depende de ningún corte geográfico — es un hallazgo sobre el instrumento mismo, válido para toda la muestra.

**¿Qué está sesgado por marcos o muestras extranjeras?** Ninguno — ENVIPE 2025, encuesta mexicana, población mexicana.

**¿Qué cambiaría con foco rural, indígena o popular?** Nada en el veredicto D mismo (es un hallazgo de diseño de instrumento, no de subpoblación) — pero sí en el hallazgo adyacente de §2.4: no se exploró si la brecha de 11.9pp dentro de `BPCOD=01` varía por `DOMINIO`, y con n=402/614 dividido tres formas la potencia se degradaría rápido. Declarado, no ejecutado — decisión de alcance de este acto.

**¿Qué parece psicológico y es incentivo racional?** Todo el mecanismo declarado por la regla ya es incentivo racional por diseño (miedo a represalia de un agresor identificable + rendimiento bajo de denunciar) — no hay riesgo de leerlo como rasgo aquí. La cifra "denunciar rinde 0.8%" que cita el `PORQUE` de la regla (`canon/integrador-psicologia-mexicano.md:60`) **no se verificó en este acto** — no era necesario para llegar al veredicto D, y no se afirma ni se descarta.

**¿Dónde hay evidencia débil pero intuición social fuerte?** Aquí, de forma literal: la intuición de que "el miedo a un agresor identificable sin seguro impide denunciar" es fuerte y generalizable a cualquier tipo de delito — pero ENVIPE simplemente no construyó el instrumento para poder probarlo fuera del robo de vehículo. Es exactamente el tipo de caso que el Módulo de auditoría pide señalar: la ausencia de evidencia no es evidencia de ausencia del mecanismo, es un hueco de instrumento declarado.

**¿Qué sería peligroso mal usado?** Tres lecturas, las tres incorrectas. **(1)** *"R7.2 fue refutada"* — no: D es inejecutable-como-está-especificada, no refutación; la propia ficha ordena archivar D "nunca como confirmación" (legend genérico) y, simétricamente, tampoco como refutación. **(2)** *"El 79.1% vs. 67.2% de §2.4 confirma R7.2"* — no: esa es una comparación dentro de una sola clase de delito (robo de vehículo asegurado vs. no asegurado), no la brecha entre clases que el falsador, tal como está redactado, exige. **(3)** *"`BP2_1` mide cobertura de seguro contra el delito en general"* — no: mide, exclusivamente, si un vehículo robado estaba asegurado — verificado por descriptor literal (§2.1) y por diseño de cuestionario (§2.2), no por parecido de nombre.
