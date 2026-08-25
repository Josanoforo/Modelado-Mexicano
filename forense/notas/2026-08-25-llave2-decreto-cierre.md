# LLAVE2-DECRETO · Pre-registro y corrida — el experimento natural del decreto de la Región Fronteriza Norte sobre ENOE

### `llave2-decreto` · **v1.0** · 25 de agosto de 2026 · ACTO LLAVE2-DECRETO · ejecuta FP-109 opción (a) (mesa, ADR-155, 24/ago/2026)

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-25-llave2-decreto-cierre.md` |
> | **NOMBRE ESTABLE** | **`llave2-decreto`** — cítalo así, nunca por nombre de archivo |
> | **CORRECCIÓN DE NOMBRE DECLARADA** | El encargo pide `2026-08-25-llave2-decreto.md` (sin `-cierre`). Normalizado (`T02`, `tests/check.py:111-112`, minúsculas + solo alfanumérico) ese nombre colisiona byte a byte con `forense/encargos/2026-08-25-LLAVE2-DECRETO.md` (el archivo del propio encargo, que este mismo acto crea en el cierre) — `"20260825llavedecretomd"` en ambos casos. Es el mismo defecto que [[feedback_t02_autocolision_encargo_nota]] ya documentó (`ACTO T02` autocolisión encargo↔nota): se corrige con el sufijo `-cierre`, verificado abajo en §6. |
> | **QUÉ ES** | Pre-registro (COMMIT 1, congelado antes de abrir microdato) y corrida (COMMIT 2) de un diseño de diferencias-en-diferencias sobre encuestas repetidas — llave de clase **(ii)** de `ADR-57(c)` — usando el decreto de estímulos fiscales de la Región Fronteriza Norte (`DOF` 31/dic/2018, vigor 1/ene/2019) como corte natural sobre `ENOE`. |
> | **QUÉ NO ES** | No adjudica ningún veredicto de Hito D (`27` no se toca). No escribe nada en `milpa/procedencia.yaml` — el efecto queda `PROPUESTO`. No re-abre `FP-64` ni enmienda `ADR-57(c)`. |

---

## 0 · ARRANQUE y VERIFICACIÓN DE EXISTENCIA — antes de leer el resto del encargo

**1 · REPO.** Clon existente: `/home/pc0/Modelado-Mexicano` (la base estaba en `acto/cal-g3-puntual`, una rama ajena — **no** se usó). Worktree nuevo de este acto: `/home/pc0/mm-llave2-decreto`, rama `llave2-decreto`, creado desde `origin/main`. `git log -1 --format="%h %s"` al arrancar → `bd70166 Merge pull request #333 from Josanoforo/bibliotecario-56`. `git status` → limpio.

**2 · SHA.** `origin/main = bd70166` al arrancar (`PR #333`, `ACTO BIBLIOTECARIO-56`, `ADR-163`). Es la punta real — no hay diferencia que re-derivar.

**3 · `data/raw`.** Ausente en el worktree nuevo (esperado, gitignorado). Enlazado: `ln -s /home/pc0/mm-corpus/raw data/raw`. `ls data/raw | wc -l` → `321` entradas (corpus compartido montado). Este acto **no descarga** microdato de encuesta — sólo dos documentos de referencia externos (el propio decreto y el catálogo geoestadístico de INEGI, ninguno es microdato de encuesta, ver §3.1).

**4 · ENTORNO, firma de tres partes (`A.2`).** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → `sin_variable`. `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`. `ls data/raw/` → `321` entradas, no vacío. **UBUNTU confirmado, sin `PARO`.**

**5 · ESPEJO.** No se derivó ninguna cifra del espejo del proyecto — todo lo citado abajo sale de este clon o de fuentes externas citadas con URL+sha256+fecha.

**VERIFICACIÓN DE EXISTENCIA (§1 ESTRUCTURA):** el dominio "llaves de identificación ejercidas" lo gobierna `forense/registro-llaves-identificacion-v1_0.md` — verificado por uso, no por invención: 5 ADR lo citan como fuente (`ADR-67(c)`, `ADR-144`, `ADR-110(b)`) y 2 firmas de mesa lo sellan (`FP-69`, `ACTO ADJ-4`). **Hallazgo menor declarado:** `data/INFRAESTRUCTURA-v1_0.md` (el índice de qué tabla gobierna cada dominio, `A.7`) **no** indexa este dominio — `grep -in "registro-llaves\|llaves de identificacion" data/INFRAESTRUCTURA-v1_0.md` da **0** líneas; sus 8 dominios cubren adquisición/curación, no el registro de llaves. Es un hueco del propio índice, no de este acto — se declara y no se repara aquí (fuera de perímetro).

**§2 CONTENIDO — ¿existe ya este pre-registro?** `command grep -rln "franja\|fronteriza\|decreto" --include=*.md --include=*.tsv --include=*.yaml .` (excluyendo `.git`) da **9 archivos**, todos ya leídos en este acto (§3 abajo); ninguno contiene un pre-registro congelado ni una corrida — todos son hallazgos previos que **declaran el hueco**, el más explícito: `forense/notas/2026-08-20-adq-enoe-pre2019-resultados.md:109`, verbatim: *"El decreto no se verificó aquí. No se leyó el DOF, no se derivaron los municipios de la franja, no se fijó el grupo de tratamiento."* **`NO-ENCONTRADO`, universo declarado: 9/9 archivos examinados con control positivo** (el propio término "frontera" aparece en los 9). El trabajo **no** está hecho — el encargo se lanza.

**§3 COBERTURA RETROACTIVA.** `registro-llaves-identificacion-v1_0.md` nació el 11/ago/2026 (`ADR-67(c)`) — anterior al decreto siendo citado como candidato ENOE (`ADR-57(c)`, 4/ago, ya lo nombraba antes incluso). No hay trabajo previo a esa fecha que la tabla no pudiera ver.

---

## 0.1 · Contaminación de esta sesión — declarada antes que nada (`ADR-46`)

**Lo que esta sesión abrió antes de congelar esta ficha, y por qué no es contaminación de datos:**

- **Estructura de ENOE** (Universo B de `ADQ-ENOE-PRE2019`, ya contaminada por esa sesión y heredable): `data/raw/fd_c_bas_amp_15ymas.pdf` (era clásica) y `data/raw/enoe_325_fd_c_bas_amp.pdf` (ENOEN) — diccionarios de datos, **no microdato**. Se citan nombres de campo, tipos y catálogos de código. No se abrió ningún `.csv`/`.dbf` de microdato de ninguna ola.
- **Dos documentos de referencia externos, adquiridos en este acto** (no son ENOE, no son encuesta — catálogos/normativa de terceros):
  1. El propio decreto: `DOF` 31/dic/2018, "DECRETO de estímulos fiscales región fronteriza norte". Descargado de `https://www.gob.mx/cms/uploads/attachment/file/650984/1_DOF_-_DECRETO_de_est_mulos_fiscales_regi_n_fronteriza_norte.pdf` (mismo texto que `https://dof.gob.mx/nota_detalle.php?codigo=5547485&fecha=31/12/2018`, confirmado por contenido), consultado 25/ago/2026. `sha256`: `8576016468a512861fefe38e92d34ffaabca66f0eac9e88658bc23f7e420fb96`. Guardado en `scratchpad/decreto-rfn-2018-12-31.pdf` (no en `data/manifiesto.yaml` — fuera de perímetro de este acto, declarado).
  2. Catálogo Único de Claves de Áreas Geoestadísticas Municipales de INEGI, vía su servicio web público `https://gaia.inegi.org.mx/wscatgeo/mgem/<cve_ent>`, consultado 25/ago/2026 para los 6 estados fronterizos (`02,05,08,19,26,28`). Guardado en `scratchpad/mgem_{02,05,08,19,26,28}.json`.
- **`dof.gob.mx` con TLS roto tras el proxy de sandbox** (mismo síntoma que `bbis-adq-enoe-pre2019-v1_0.md` §2 ya midió: la sesión previa reportó redirección a otra fecha; aquí el fallo es `curl: (60)` de verificación de certificado, resuelto con `-k`, `301` reproducible). Declarado, no oculto.

**Ninguna tabla de microdato ENOE (`.csv`/`.dbf`, cualquier ola) se abrió antes de congelar este COMMIT 1.**

---

## 1 · Diseño — congelado antes de abrir microdato

**Tipo.** Diferencias-en-diferencias (DiD) sobre transversales repetidas de `ENOE` — llave **(ii)** de `ADR-57(c)`, verbatim (`canon/gobernanza-v1_15.md:629`): *"experimento natural con grupo de comparación sobre encuestas repetidas"*.

### 1.1 · Corte natural y grupo de tratamiento

El decreto (`DOF` 31/dic/2018, `scratchpad/decreto-rfn-2018-12-31.pdf`, Artículo Primero, `sha256` arriba) define **43 municipios** como "región fronteriza norte". Emparejados por nombre normalizado (acentos plegados) contra el Catálogo Único de INEGI — **43 de 43 emparejan**, cero sin resolver (script `scratchpad/derive_municipios.py`, corrido y verificado en este acto):

| ent | mun | estado | municipio |
|---|---|---|---|
| 02 | 001 | Baja California | Ensenada |
| 02 | 002 | Baja California | Mexicali |
| 02 | 003 | Baja California | Tecate |
| 02 | 004 | Baja California | Tijuana |
| 02 | 005 | Baja California | Playas de Rosarito |
| 05 | 002 | Coahuila de Zaragoza | Acuña |
| 05 | 012 | Coahuila de Zaragoza | Guerrero |
| 05 | 013 | Coahuila de Zaragoza | Hidalgo |
| 05 | 014 | Coahuila de Zaragoza | Jiménez |
| 05 | 022 | Coahuila de Zaragoza | Nava |
| 05 | 023 | Coahuila de Zaragoza | Ocampo |
| 05 | 025 | Coahuila de Zaragoza | Piedras Negras |
| 05 | 038 | Coahuila de Zaragoza | Zaragoza |
| 08 | 005 | Chihuahua | Ascensión |
| 08 | 015 | Chihuahua | Coyame del Sotol |
| 08 | 028 | Chihuahua | Guadalupe |
| 08 | 035 | Chihuahua | Janos |
| 08 | 037 | Chihuahua | Juárez |
| 08 | 042 | Chihuahua | Manuel Benavides |
| 08 | 052 | Chihuahua | Ojinaga |
| 08 | 053 | Chihuahua | Praxedis G. Guerrero |
| 19 | 005 | Nuevo León | Anáhuac |
| 26 | 002 | Sonora | Agua Prieta |
| 26 | 004 | Sonora | Altar |
| 26 | 017 | Sonora | Caborca |
| 26 | 019 | Sonora | Cananea |
| 26 | 039 | Sonora | Naco |
| 26 | 043 | Sonora | Nogales |
| 26 | 048 | Sonora | Puerto Peñasco |
| 26 | 055 | Sonora | San Luis Río Colorado |
| 26 | 059 | Sonora | Santa Cruz |
| 26 | 060 | Sonora | Sáric |
| 26 | 070 | Sonora | General Plutarco Elías Calles |
| 28 | 007 | Tamaulipas | Camargo |
| 28 | 014 | Tamaulipas | Guerrero |
| 28 | 015 | Tamaulipas | Gustavo Díaz Ordaz |
| 28 | 022 | Tamaulipas | Matamoros |
| 28 | 024 | Tamaulipas | Mier |
| 28 | 025 | Tamaulipas | Miguel Alemán |
| 28 | 027 | Tamaulipas | Nuevo Laredo |
| 28 | 032 | Tamaulipas | Reynosa |
| 28 | 033 | Tamaulipas | Río Bravo |
| 28 | 040 | Tamaulipas | Valle Hermoso |

**Trampa declarada:** `"Guerrero"` nombra **dos** municipios distintos del decreto (`05-012`, Coahuila, y `28-014`, Tamaulipas) — cualquier unión debe hacerse por el par numérico `(ent,mun)`, nunca por nombre.

### 1.2 · Grupo de comparación — elegido ahora, con razón

**Municipios no listados de los mismos 6 estados** (`02,05,08,19,26,28` — Baja California, Coahuila de Zaragoza, Chihuahua, Nuevo León, Sonora, Tamaulipas). Universo candidato: `278` municipios totales en esos 6 estados menos los `43` tratados = **235 municipios candidatos de control**. Se elige sobre la alternativa de "banda de distancia" porque `ENOE` no publica coordenadas de vivienda en el microdato público (verificado en el diccionario, §0.1) — una banda de distancia exigiría un cruce geoespacial con un insumo que no está en el corpus. Se declara la asimetría conocida (no se resuelve aquí): Nuevo León aporta 1 tratado (`Anáhuac`) contra 50 municipios de control candidatos, incluida la zona metropolitana de Monterrey — la composición **realizada** (cuáles de los 235 sobreviven con clave de municipio no vacía) se mide en COMMIT 2, no se supone aquí.

### 1.3 · Ventana temporal

**Pre: `2017T1`–`2018T4`** (8 olas), tal como el encargo la fija. **Post: `2019T2`–`2020T1`, `2020T3`–`2020T4`** (6 olas), excluyendo `2019T1` (transición/anuncio — el propio encargo la excluye del post, simétrico al hallazgo ya documentado de que `2018T4` es "potencialmente contaminado por anticipación", `bbis-adq-enoe-pre2019-v1_0.md` §2) y `2020T2` (suspensión de `ENOE` por pandemia, hueco ya documentado, `bbis-adq-enoe-pre2019-v1_0.md` §2). **Cota de la ventana post, citada del propio decreto** (`scratchpad/decreto-rfn-2018-12-31.pdf`, Transitorio Primero, verbatim): *"El presente Decreto entrará en vigor el 1 de enero de 2019 y estará vigente durante 2019 y 2020."* — se usa la vigencia **original** del decreto (antes de su prórroga de dic/2020, que este acto no trata) como frontera de la ventana post, en vez de una fecha arbitraria.

**Ruta de distribución, uniforme para las 14 olas (evita el defecto de `FP-110`):** las 8 olas pre vienen de `data/raw/{2017,2018}trim{1..4}_csv.zip` (`/microdatos/`, adquisición de `ADQ-ENOE-PRE2019`). Las 6 olas post vienen de `data/raw/enoe_microdatos_post2019/{2019trim{1..4},2020trim1,enoe_n_2020_trim{3,4}}_csv.zip` — la ruta canónica declarada por `ADR-152` — **no** las copias homónimas `conjunto_de_datos_enoe_*_csv.zip` que siguen en `data/raw/` por la ruta `/datosabiertos/` vieja (esas se ignoran deliberadamente en este diseño).

### 1.4 · Variables — nombres exactos, con cita de campo

Todas viven en la tabla `SDEMT<PERIODO>.DBF` de cada ola (una sola tabla, sin unión necesaria). Dos eras, dos juegos de nombres — verificado en los dos diccionarios del corpus:

| variable | era clásica (`fd_c_bas_amp_15ymas.pdf`, hasta `2020T1`) | era ENOEN (`enoe_325_fd_c_bas_amp.pdf`, desde `2020T3`) | qué es |
|---|---|---|---|
| municipio | `MUN`, C(3), `001-575` (línea 232) | `CVE_MUN`, C(3), `001-575` (línea 147) | Municipio según entidad. **Blanco = se omite por baja densidad poblacional** en las dos eras — la cobertura realizada se mide, no se supone |
| entidad | `ENT`, C(2) (línea 302) | `ENT` (misma, verificado presente) | Estado |
| ponderador | `FAC` (línea 399 del PDF clásico, vía `data/diseno-muestral.yaml:487`) | `FAC_TRI` (líneas 347-349, misma fuente) | Factor de expansión trimestral |
| estrato de diseño | `EST_D` (línea 239) | `EST_D_TRI` (línea 155) | Estrato de diseño |
| UPM | `UPM`, C(7) (línea 340) | `UPM` (línea 276, mismo nombre en las dos eras) | Unidad primaria de muestreo |
| horas trabajadas | `HRSOCUP`, N(3) (línea 1213) | `HRSOCUP` (línea 1206, mismo nombre) | Horas trabajadas en la semana |
| ingreso mensual | `INGOCUP`, N(6) (línea 1215) | `INGOCUP` (línea 1208) | Ingreso mensual nominal, "el mismo captado en la pregunta 6B" |
| ingreso por hora | `ING_X_HRS`, N(17.5) (línea 1218) | `ING_X_HRS` (línea 1211) | Ingreso mensual / horas semanales — **nominal** |
| informalidad | `EMP_PPAL`, N(1): `1`=empleo informal, `2`=empleo formal (línea 1305) | `EMP_PPAL` (línea 1299, mismos códigos) | "Clasificación de empleos formales e informales de la primera actividad" |
| transfronterizo | `TRANS_PPAL`, N(1): `1`=extranjero/embajada/consulado, `2`=dentro del país (línea de la tabla `SDEM`) | mismo nombre y códigos (no re-verificado línea a línea; misma tabla, mismo bloque de campos ~100-104) | Filtra trabajo físicamente fuera de México |

### 1.5 · Universo de persona

**Población ocupada, 15 años y más** (universo nativo de `ENOE`), operacionalizado como: `EMP_PPAL` no vacío (por diseño de INEGI ese campo sólo se llena para ocupados — es la definición operativa, no una regla inventada) **Y** `TRANS_PPAL = 2` (excluye trabajo transfronterizo físico en EE.UU. — relevante precisamente en municipios como Tijuana/Mexicali/Cd. Juárez/Nogales, donde la exclusión evita confundir el mercado laboral mexicano con el estadounidense) **Y** `MUN`/`CVE_MUN` no vacío (municipio identificable — quién queda fuera por supresión de baja densidad es hallazgo de COMMIT 2, no descarte silencioso).

### 1.6 · Ponderador, diseño y errores estándar

Ponderador por ola (`FAC` o `FAC_TRI` según era, §1.4), estimación trimestral (no se anualiza). **Primario:** errores estándar por conglomerado sobre `UPM` (con `EST_D`/`EST_D_TRI` como estrato, HC1, mismo mecanismo que `CAL-G3-PUNTUAL`/`R7.1` ya usan en este programa). **Sensibilidad, pre-declarada:** clustering por municipio `(ent,mun)` — es el nivel al que el tratamiento se asigna (Bertrand-Duflo-Mullainathan), y con ~43 clústeres tratados es una prueba más conservadora que `UPM`; se reporta junto a la primaria, no en su lugar (mismo patrón que este programa ya usa para sensibilidades, `A-bis` contraparte).

---

## 2 · Desenlaces — máximo dos, escala declarada (`A-bis` regla 3: no se cruzan)

**1 · Ingreso laboral por hora, en logaritmo natural — `log(ING_X_HRS)`.** Escala: log-puntos, interpretable como efecto porcentual aproximado. **Por qué logaritmo y no nivel deflactado, declarado antes de correr:** en un DiD aditivo sobre niveles, deflactar por un índice de precios nacional **no** es neutro — `DiD_real = (1/P_post)·ΔY_post − (1/P_pre)·ΔY_pre ≠ DiD_nominal` en general (la división por el índice de cada período no cancela en la doble diferencia). En logaritmos sí cancela exactamente: `DiD[log(Y/P)] = DiD[log Y] − [log(P_post) − log(P_pre)] − [−(log(P_post) − log(P_pre))] = DiD[log Y]` — el término de precios aparece con signo idéntico en tratamiento y control y se cancela en la resta externa. Se elige `log` **porque** evita depender de una serie de deflactor (`INPC`) que esta sesión no pudo re-derivar limpiamente de fuente primaria en el tiempo disponible (la `API` de indicadores de INEGI exige token por correo, ya documentado como no completable por `E4c Commit 4`; la vía alterna de ese mismo acto, boletines mensuales de `DOF`, exigiría ~14 lecturas individuales) — no por preferencia, por invarianza algebraica declarada. Universo: población ocupada de §1.5, con `ING_X_HRS` no vacío.

**2 · Informalidad — `EMP_PPAL == 1`.** Escala: proporción (puntos porcentuales, pp) de la población ocupada de §1.5 en empleo informal.

---

## 3 · Identificación honesta (`A-bis`)

**Regla 1 (co-observación ≠ identificación).** Aquí la exposición **no** la pone un reactivo co-observado en el cuestionario — la pone la geografía (municipio de residencia) cruzada con la fecha (antes/después del decreto). Es exactamente el mecanismo que `ADR-57(c)` reserva para la llave (ii): el DiD identifica el efecto de la política **si** el supuesto de tendencias paralelas se sostiene (inspeccionado, no probado, ver abajo) — no hay condicionamiento sobre un θ que pudiera confundir la lectura.

**Tendencias paralelas — se inspecciona, no se prueba.** Las 8 olas pre (`2017T1`–`2018T4`) se usan para tabular la brecha tratamiento-menos-control **por ola**, antes de calcular ningún DiD post — un placebo. Si la brecha pre-tendencia se mueve de forma marcada y sistemática antes del corte, se reporta como reserva del diseño, no se oculta ni se re-especifica hacia atrás (COMMIT 3 si hiciera falta).

**El estimando es el efecto del PAQUETE, no de un mecanismo aislado — declarado antes de ver el dato.** `ADR-57(c)` mismo (`gobernanza:629`) nombra *"salario mínimo de franja fronteriza"* como el ejemplo de esta llave para `ENOE` — el 1/ene/2019 la Región Fronteriza Norte recibió **simultáneamente** este decreto fiscal (`IEPS`/`ISR`/`IVA`) **y** un salario mínimo diferenciado más alto, misma zona, misma fecha, ninguno de los dos separable del otro con el diseño de este acto. Lo que este DiD mide es el efecto combinado del paquete de política fronteriza 2019 sobre la zona — no el mecanismo fiscal aislado, y no un mecanismo psicológico. Se dice aquí, antes de correr, para que nadie lea el resultado como atribuible a un solo instrumento.

**Regla 4 (subpoblación, no poblacional).** El efecto queda acotado a la población ocupada de los municipios de §1.1/§1.2 (6 estados fronterizos) en la ventana `2017`–`2020`(T4) — no se compara ni se extrapola contra ninguna cifra nacional de `ENOE` ni contra ningún θ poblacional del modelo.

**Regla 3 (escalas no se cruzan).** Informalidad en pp e ingreso en log-puntos se reportan y adjudican **por separado** — nunca "el uno equivale a X del otro".

---

## 4 · Escala de falsación (`B-bis`) — declarada antes de correr

Por cada desenlace, por separado (regla 3), cinco filas con su fila de no-refutación y su umbral de magnitud, pre-declarados:

**Ingreso (`log(ING_X_HRS)`), dirección predicha: positiva** (el paquete —estímulo fiscal + salario mínimo— empuja el ingreso hacia arriba por los dos mecanismos, no hay tensión teórica). Umbral de magnitud: `|β| ≥ 0.05` (≈5%, log-puntos).

**Informalidad (`EMP_PPAL==1`), sin dirección predicha — declarado así, no por omisión.** El decreto premia la formalización (el estímulo fiscal exige contribuyente registrado); el salario mínimo más alto puede empujar hacia la informalidad (evasión del piso salarial). Los dos mecanismos del mismo paquete tiran en direcciones opuestas sobre este desenlace — se declara sin predicción de signo, y el signo que salga es el hallazgo. Umbral de magnitud: `|β| ≥ 5` pp.

| fila | qué significa (aplicado a cada desenlace, por separado) |
|---|---|
| `NO_EJECUTABLE` | **Se verifica primero, es compuerta de datos, no de resultado.** Si tras aplicar §1.5 quedan menos de 15 UPM tratadas distintas, o menos de 300 observaciones persona-ola tratadas, en el conjunto pre+post pooled — domina sobre cualquier punto estimado |
| `EJERCIDA_CORROBORA` | IC95% excluye cero **y** el punto cae del lado del umbral de magnitud predicho en dirección **y** (para informalidad) el propio dato fija la dirección |
| `EJERCIDA_ACOTA` | IC95% excluye cero pero bajo el umbral de magnitud — **o** un desenlace corrobora y el otro no (el paquete tuvo efecto en una dimensión, no en las dos: es acotamiento, no ambigüedad) |
| `EJERCIDA_REFUTA` | IC95% angosto, centrado cerca de cero, que **excluye** el umbral de magnitud en las dos direcciones — evidencia de que el paquete no movió este desenlace, con precisión |
| `EJERCIDA_INDECISA` | IC95% cruza cero **y** también cruza el umbral de magnitud — el falsador es demasiado débil para decir nada |

**Precedencia, declarada al sellar:** `NO_EJECUTABLE` (gate de datos) → después, la fila que corresponda por outcome. **Veredicto de la LLAVE (la fila del registro, que es una sola por los dos desenlaces):** si los dos desenlaces caen en la misma fila o en filas compatibles (ambos `CORROBORA`, o uno `CORROBORA` y otro `ACOTA`), la fila de la llave es la **más fuerte de las dos que corrobora menos** (`ACOTA` si hay discrepancia, nunca se promedia). Si cualquiera de los dos cae en `NO_EJECUTABLE`, la llave entera es `NO_EJECUTABLE` — un desenlace no ejecutable no se descarta en silencio para quedarse solo con el otro.

**Contador que gobierna esta fila:** `forense/registro-llaves-identificacion-v1_0.md` §3, receta de §4. Vigente al congelar este COMMIT 1: **`3` llaves ejercidas de `4` filas** (`CAL-G3`=(i) `EJERCIDA_ACOTA`, `R5.1-D2`/`R5.1-D3`=(ii) ambas `EJERCIDA_INDECISA`, `EXP-COMPARTAMOS-1`=(iii) `SELLADA_NO_EJERCIDA`). Esta fila es la **quinta** de la tabla y la **tercera** de clase (ii) — el denominador sube a `5` con este COMMIT 1 (nace `SELLADA_NO_EJERCIDA`) y el numerador se moverá en COMMIT 2 si el veredicto cae en cualquier `EJERCIDA_*`.

**El primer resultado que produzca este procedimiento es el que se reporta.**
