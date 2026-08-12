# E4c · R5.1-D2 — Especificación congelada (Commit 1)

**Acto:** ENCARGO E4c, T1-A — correr `R5.1-D2` conforme a su pre-registro sellado.
**Pre-registro:** `forense/r5-1-diseno-por-regla-preregistro-v1_0.md`, sellado 4/ago/2026, §9 sin enmiendas a la fecha (verificado: `grep -n "Ninguna a la fecha del sello"` → línea 137).
**Autoriza:** ADR-67(c), `canon/gobernanza-v1_15.md:868` — "RENGLÓN PROPIO", identificador `R5.1-D2`.
**SHA base:** `931997c` = `origin/main` al momento de este acto (coincide exacto con el declarado por el encargo, sin desfase).
**Rama:** `e4c/r5-1-d2`.

## 0 · Estado de dependencias — ACTO A no satisfecho, desviación autorizada por mesa

El encargo declara dependencia dura de **ADR-67(c)** (satisfecha — sellada y fusionada, PR #169) **y del ACTO A**, el registro de llaves de identificación (`forense/registro-llaves-identificacion-v1_0.md`). Verificado el 11/ago/2026 contra `origin/main` tras `git fetch --all --prune`: ese archivo **no existe** — ni en el árbol commiteado, ni en ninguna rama remota, ni en ningún PR abierto o fusionado, ni mencionado por ese nombre en ningún `.md` del repo. El vocabulario que el encargo pide usar (`EJERCIDA_CORROBORA`/`EJERCIDA_ACOTA`/`EJERCIDA_REFUTA`/`EJERCIDA_INDECISA`) tampoco está canonizado en ningún otro archivo — solo aparece en el texto del encargo. `forense/hallazgos.md`, entrada del 11/ago sobre ADR-67, es explícito: *"Contadores movidos: 0 — habilita; los mueven los actos E4 y T1-A"* — confirma que sellar el ADR no creó el registro; eso queda para un acto de ejecución aparte que no ha corrido.

El encargo es explícito y repetido en que la ausencia de este archivo es PARO, y prohíbe el rodeo obvio (improvisar una fila en `forense/hitoD-preregistro-v2_0.md`, que infla el denominador 27 que ADR-67(c) prohíbe tocar). Presentado el hallazgo a mesa (usuario), con la evidencia de arriba y el diagnóstico de qué parte del encargo es separable, **mesa autorizó ejecutar solo este commit** — la especificación congelada, que no toca el registro de llaves ni ningún contador — **y diferir los Pasos 3-7 del encargo E4c como "parte 2"**, explícitamente pendiente de que `forense/registro-llaves-identificacion-v1_0.md` exista en `origin/main`. Este commit no produce resultado, no escribe fila en ningún registro, no adjudica.

**ACTUALIZACIÓN, antes de comitear — `origin/main` avanzó durante la redacción de este mismo commit.** `git fetch` posterior detecta PR #170 fusionado (`bfc0037`, 11/ago 19:58 -0600), con dos commits — `e38554e` ("RENGLÓN: registro de llaves de identificación") y `5549de5` ("Contador de llaves ejercidas en estado + hallazgos + encargo archivado") — que **crean exactamente el ACTO A** que faltaba: `forense/registro-llaves-identificacion-v1_0.md` ya existe, con `R5.1-D2` sembrada como `SELLADA_NO_EJERCIDA` y una nota que identifica, **de forma independiente y por otra sesión**, el mismo vacío de §6 que la §3 de este documento resuelve abajo (el registro cita el problema y explícitamente deja su resolución a este acto, E4c: *"E4c arranca con la instrucción de reportar este vacío, nunca de forzar una fila que la escala sellada no contempla"*). El vocabulario oficial de `estado` (§2 del registro) coincide con el que este documento infirió por su cuenta antes de leerlo — convergencia, no copia.

**El gate original queda resuelto — pero con una complicación nueva.** Existe una rama sin fusionar, `claude/acto-a-correccion-post-170-ipy2fg` (commit `b55938f`, 11/ago 20:07 -0600, ~9 minutos después de que #170 se fusionara): *"ACTO A′: corrige referencia rota §3→§4 y cascada 8→9 de 14 heredada de #170"*. Indica que otra sesión, activa muy recientemente, ya encontró un defecto en lo que #170 fusionó — incluyendo un movimiento de `8 de 14` a `9 de 14`, un contador que este mismo encargo (Paso 4) exige dejar intacto. Ese commit **no está fusionado a `origin/main`** al momento de escribir esto. Dado el volumen de actividad concurrente sobre exactamente los archivos que Pasos 3-7 tocarían (`registro-llaves-identificacion-v1_0.md`, `canon/estado-programa-v1_10.md`), este commit 1 se cierra y se reporta a mesa antes de tocar Pasos 3-7 — no se improvisa una re-autorización de "parte 2" sin decisión explícita, mismo criterio que el resto de este acto.

Este worktree se re-sincronizó contra el `origin/main` post-#170 (`git merge origin/main`, fast-forward limpio, sin commits propios previos que reconciliar) antes de este commit. Nada de la especificación de abajo (§2) depende de contenido tocado por #170 o por la corrección pendiente — ambos son archivos fuera del perímetro de este commit (el registro de llaves y el contador de estado, reservados para Paso 3+) — así que no hay nada que re-derivar en la especificación misma.

Ambas olas ENIGH verificadas contra `data/manifiesto.yaml`, hash real crudo:

| id | archivo | sha256 declarado | sha256 real | tamaño |
|---|---|---|---|---|
| `enigh2018_nc_csv` | `enigh2018_nc_csv.zip` | `5026cd95...43d636` | **coincide** | 43,339,807 B |
| `enigh2022_nc_csv` | `enigh2022_nc_csv.zip` | `3b2b0bc9...092c9e06` | **coincide** | 90,030,937 B |

## 1 · Procedencia de este commit — qué se abrió, qué no

Se abrió, de cada ZIP (listado de nombres vía `python3 -m zipfile`, sin `unzip`/`7z` disponibles en este entorno — no es el defecto DEFLATE64 de INT-1, aquí `zipfile` de Python sí pudo listar y extraer sin error):

- `conjunto_de_datos_ingresos_enigh_2018_ns/diccionario_de_datos/diccionario_datos_ingresos_enigh_2018_ns.csv` y su análogo 2022
- `conjunto_de_datos_ingresos_enigh_2018_ns/catalogos/ingresos_cat.csv` (catálogo de claves de percepción) y su análogo 2022, más el catálogo paralelo de `ingresos_jcf_enigh2022_ns` (tabla nueva de 2022, ver §2.1)
- `conjunto_de_datos_concentradohogar_enigh_2018_ns/diccionario_de_datos/...csv` y su análogo 2022, más `catalogos/clase_hog.csv` de ambas olas
- `conjunto_de_datos_poblacion_enigh_2018_ns/diccionario_de_datos/...csv` y su análogo 2022

**No se abrió** ninguna tabla `conjunto_de_datos/*.csv` (el microdato real: filas de hogares/personas/ingresos) de ninguna ola. Todo lo anterior es diccionario de datos y catálogo de claves — metadato que describe la estructura del instrumento, no observaciones. Es la misma distinción que `v2.2 corolario 1` traza y que el encargo pide respetar en su orden: diccionario antes que microdato. Bajo ADR-46, esto es "estructura", no "dato" — se declara la apertura, no oculta.

## 2 · Especificación

### 2.1 Claves de ingreso exactas — verificadas por ola, no asumidas

**La clave es la misma en las dos olas: `P032` ("Jubilaciones y/o pensiones originadas dentro del país"), columna `ingresos.clave`, monto en `ingresos.ing_tri`.** Confirmado contra el catálogo `ingresos_cat.csv` de cada ola por separado — no heredado de la ola 2018 a la 2022.

**Hallazgo no trivial, documentado aquí porque el pre-registro pidió reportarlo antes de aplicar el corte:** aunque `P032` es estable, la familia de códigos vecina (programas no contributivos para adultos mayores) **cambió de numeración y de nombre entre olas**:

| Concepto | 2018 | 2022 |
|---|---|---|
| Jubilaciones y/o pensiones (nacional) | `P032` | `P032` (sin cambio) |
| Programa "65 y más" / Bienestar Adultos Mayores | `P044` | `P104` |
| Otros programas para adultos mayores | `P045` | `P045` (sin cambio) |
| Tarjeta Sin Hambre (PAL) | `P046` | *(código retirado, programa descontinuado)* |
| Empleo Temporal | `P047` | *(código retirado)* |
| — | — | `P101`–`P108` nuevas (becas Bienestar, Jóvenes Construyendo el Futuro, etc.) |

2022 además reorganiza la tabla `ingresos` como una **construcción derivada** (nota del propio diccionario 2022): filtra `P108` de la fuente `TR_ENIGHV2022_INGRESO` y le agrega registros de una tabla nueva `ingresos_jcf` cuando `ct_futuro = 9`. Esto no afecta a `P032` (el filtro es específico de `P108`, un programa juvenil), pero se declara porque cambia la procedencia técnica del archivo entre olas — no es el mismo pipeline de construcción, aunque el resultado para esta clave sea equivalente.

**Sobre "contributivo": el catálogo no usa esa palabra.** La etiqueta de `P032` es genérica ("jubilaciones y/o pensiones"), sin calificarla de contributiva. La inferencia de que `P032` aísla el régimen contributivo (IMSS, ISSSTE u otro sistema formal) se apoya en que los programas **no contributivos** para adultos mayores tienen código propio y separado en ambas olas (`P044`→`P104`, `P045`) — el instrumento los pregunta como conceptos distintos, no como sub-categorías de `P032`. Esto es evidencia de diseño, no una etiqueta textual explícita. Se reporta así, sin homologar a certeza — exactamente la granularidad que el pre-registro (§2) pidió declarar antes de correr el corte. Si esta inferencia resulta insuficiente al momento de adjudicar, es la fila D de §6 (identificación fallida), no un motivo para forzar una aproximación.

**Corte monetario, unidades declaradas ahora:** el pre-registro fija el umbral en pesos **mensuales** ($1,092). La única variable de monto disponible es `ing_tri` (trimestral normalizado, confirmado por el diccionario: *"Ingreso trimestral normalizado de acuerdo a la decena de levantamiento"*). Conversión declarada aquí, no en la corrida: **corte = $1,092 × 3 = $3,276 trimestrales**, aplicado sobre la suma de `ing_tri` de todas las filas con `clave = P032` de la persona (se declara ahora, por si acaso, que si una persona tuviera más de una fila `P032` —no esperado bajo la estructura de la tabla, que admite como máximo una fila por combinación persona×clave— se sumarían; hallazgo a reportar si ocurre).

### 2.2 Grupos de tratamiento y comparación — por regla, como §2-§3 los definen

Sobre el universo de personas de 65+ años (`poblacion.edad ≥ 65`, columna `edad` confirmada N(3) idéntica en ambas olas):

- **Tratamiento ("nuevo elegible por regla"):** `ingresos.ing_tri` sumado sobre `clave = P032` **> $3,276/trimestre** (equivalente a >$1,092/mes).
- **Comparación ("elegible en ambos regímenes"):** `ing_tri` sobre `clave = P032` **≤ $3,276/trimestre, o nulo** (la persona no tiene ninguna fila `P032`).

Mutuamente excluyentes dentro de la misma ola, por construcción — no hay tercera categoría en este corte (§3). La regla manda sobre cualquier variable de recepción declarada de programas sociales: no se usa `P044`/`P104` ni ninguna otra clave de programa no contributivo para clasificar tratamiento/comparación — esas claves miden si la persona *cobró* un programa distinto, no la regla de elegibilidad que este diseño aísla.

### 2.3 Universo compartido

Personas de 65+ años, en hogares con al menos una fila en `ingresos` (cualquier clave). Se excluye —y se cuenta cuántas, en la corrida— a quien no tenga ninguna fila en `ingresos`: para esa persona el corte de §2.1 no es aplicable, no es cero por definición (§3 del pre-registro, citado literal).

### 2.4 Los dos desenlaces, por separado — nunca combinados en índice

Prohibición explícita heredada de §5 del pre-registro, respetada:

1. **Corresidencia intergeneracional:** `concentradohogar.clase_hog ∈ {3, 4}`. Catálogo verificado **idéntico en ambas olas** (`clase_hog.csv`: 1 Unipersonal, 2 Nuclear, 3 Ampliado, 4 Compuesto, 5 Corresidente — mismos códigos, mismas etiquetas 2018 y 2022). El diccionario 2022 documenta además la fórmula booleana exacta de construcción (2018 solo la describe en prosa) — misma regla, mejor documentada en la ola nueva, no una diferencia de fondo.
2. **Transferencia intrafamiliar hacia mayores:** persona 65+ con `ingresos.clave = P040` ("Donativos en dinero provenientes de otros hogares") y `ing_tri > 0`. Código `P040` verificado presente, mismo texto, en el catálogo de ambas olas — sin cambio.

**Estimador:** DiD ponderado, conglomerado último, vía `tests/svystat.py` (reutilizado sin modificar). Se reporta brecha tratamiento−comparación en 2018, la misma brecha en 2022, y la diferencia de las dos brechas, con IC95%, para cada desenlace por separado — nunca un índice combinado.

### 2.5 Ponderadores, estrato y conglomerado — nombre exacto, por ola

Fuente declarada: tabla `concentradohogar`, ambas olas (2022 documenta explícitamente que sus copias son "iguales a la variable X de la tabla `viviendas`"; 2018 no trae esa nota pero expone las mismas tres columnas al mismo nivel, se usa la misma fuente por consistencia entre olas).

| Columna | 2018 | 2022 |
|---|---|---|
| Estrato | `est_dis`, tipo `C(7)` | `est_dis`, tipo `C(3)` |
| Conglomerado (UPM) | `upm`, tipo `C(5)` | `upm`, tipo `C(7)` |
| Ponderador | `factor`, tipo `N(5)` | `factor`, tipo `N(5)` |

Mismos nombres de columna en ambas olas; **ancho de campo declarado distinto** (`est_dis`/`upm` cambian de longitud de cadena entre olas) — cosmético para el join (son strings, no se truncan al usarlas como llave de agrupación), pero se declara para que no se lea como omisión si alguien lo nota en la corrida. `ingresos` de 2022 trae además su propia copia de `est_dis`/`upm`/`factor` (más `entidad`) directamente en la tabla — no usada aquí, se declara la fuente única (`concentradohogar`) para no mezclar dos copias potencialmente no bit-idénticas sin verificarlo primero.

### 2.6 Universo y escala de cada cantidad — A-bis regla 3

- **DiD de corresidencia** y **DiD de transferencia**: ambos son diferencias de **proporciones** (puntos porcentuales, pp) — proporción de personas/hogares del grupo que satisface el criterio del desenlace. Misma escala entre sí (no se combinan, pero si se compararan necesitarían función de enlace — no aplica, se reportan separados).
- **"Monto documentado como suficiente"** (criterio heredado de la fila A de §6, vía la nota del 4/ago: monto / gasto per cápita del hogar tratado): escala de **pesos**, no de proporción. Es un gate independiente, no se mezcla numéricamente con el DiD — ambos deben sostenerse por separado para la fila A (o las filas nuevas de §3 de este documento), nunca se combinan en un solo número.
- Universo de cada cantidad: el universo compartido de §2.3, restringido a la ola correspondiente (2018 para la brecha 2018, 2022 para la brecha 2022; el DiD usa ambas).

### 2.7 Ejes de estratificación — declarados antes de correr

Dos ejes, ninguno más, declarados ahora:

1. **Ámbito urbano/rural** — derivable de `folioviv` (dígito 3: código≠6 urbano, código=6 rural; documentado en la propia descripción de `folioviv` del diccionario de `concentradohogar`, ambas olas, sin necesitar `tam_loc` como proxy).
2. **Sexo de la persona de 65+** — `poblacion.sexo` (`C(1)`, valores `{1,2}` Hombre/Mujer, columna idéntica en ambas olas).

Cualquier estratificación por un eje no declarado aquí, si se hace después, se rotula como análisis exploratorio (regla del encargo, respetada).

### 2.8 Cierre de la especificación

**El primer resultado que produzca este procedimiento es el que se reporta.**

## 3 · Premisa de §6 — la fila que falta, declarada antes de ver el dato

**¿Tiene §6 una fila para el desenlace en que el falsador NO refuta?** No. Las cuatro filas del pre-registro cubren: refutación (**A** — DiD<10pp o signo contrario), ambigüedad (**B** — DiD 10-20pp, o monto insuficiente, o las dos medidas en direcciones opuestas sin significancia clara), la reserva de panel (**C** — solo si la reserva dominante de A/B débil es específicamente ausencia de panel) y falla de identificación o muestra (**D** — precedencia absoluta). Ninguna fila nombra el caso DiD≥20pp en la dirección de sustitución predicha con IC95% que excluya claramente el umbral — el caso en que el falsador claramente no refuta. Mismo defecto que motivó el Bloque B-bis el 4/ago para la ficha original.

**Declaración, ahora, antes de ver el dato — dos filas nuevas, subordinadas a la escala de §6, que no la enmiendan (este acto no toca el archivo sellado):**

- **EJERCIDA_ACOTA** — DiD≥20pp en la dirección predicha con IC95% decisivo en **uno** de los dos desenlaces (no ambos), identificación de §2.1 exitosa. Acotada explícitamente a: (i) el desenlace específico que cruza el umbral, nombrado en el resultado; (ii) si además el "monto documentado" resultara insuficiente por el criterio heredado de §6, esa combinación (DiD grande y decisivo + monto pequeño) se lee como evidencia del canal de **elegibilidad/certeza** que el propio §2 del pre-registro plantea como hipótesis distinguible ("si el patrón... responde a la elegibilidad... y no solo al cobro efectivo"), no como el canal de monto — se declara esta lectura ahora para no improvisarla después de ver el número; (iii) las limitaciones ya heredadas y no resueltas por este acto: diseño no-panel (§4), `P040` no distingue donante familiar de no familiar (§5), banda de la escala copiada del original sin re-derivar para este diseño (nota de vigilancia de §6).
- **EJERCIDA_CORROBORA** — como el anterior, pero decisivo en **ambos** desenlaces simultáneamente. La lectura más limpia que este diseño puede producir; sigue acotada a (iii) arriba.
- Si el punto cae en la zona ≥20pp pero el IC95% no excluye con claridad el umbral (ancho, cruza 20pp): no es ninguna de las dos anteriores — es **EJERCIDA_INDECISA**, mecanismo distinto de la ambigüedad de banda de la fila B (aquí sí se cruzó la banda, pero el IC no lo sostiene), y coincide con la regla del Paso 3 del encargo ("si el punto satisface el umbral pero el IC no despeja, no adjudica, PROPUESTO con reserva").
- Umbral **20pp declarado ARBITRARIO aquí, no después** — extensión natural del límite superior ya fijado por la propia fila B del pre-registro, mismo criterio de honestidad que usó el umbral de tamaño mínimo de muestra de la fila D (también declarado ahí como arbitrario).

**¿Es interesante el desenlace de corroboración, dicho antes de verlo? Sí — más que la refutación de la fila A.** La fila A repetiría, con mejor identificación, un resultado que la corrida por recepción declarada del 4/ago ya adelantó (fila A, "no hay retroceso" — `2026-08-04-hitoD-r5-1-pension-bienestar.md`). Un resultado `EJERCIDA_ACOTA`/`EJERCIDA_CORROBORA` sería, en cambio, la primera vez que el programa completo produce un hallazgo corroborante con un argumento de identificación causal — regla de elegibilidad exógena, no solo asociación — y es exactamente el sentido en que el propio encargo titula este acto "la primera llave de identificación ejercida del programa". Se declara esto ahora, antes del dato, precisamente para que un resultado corroborante no se lea como fracaso frente a la refutación de A.

**Precedencia, declarada ahora (no al sellar el resultado):**

1. **D** (falla de identificación de §2.1, o muestra insuficiente por el criterio ya arbitrario de §6) manda sobre todo lo demás, sin excepción — igual que en el §6 original.
2. Si D no aplica: un DiD decisivo (IC95% excluye el umbral) en ≥20pp en la dirección predicha, en uno o ambos desenlaces, resuelve a `EJERCIDA_ACOTA`/`EJERCIDA_CORROBORA` **incluso si la cláusula de "monto insuficiente" de B también aplicaría** — un DiD grande y decisivo con monto pequeño no cae por default en B; se lee como el canal de elegibilidad/certeza (ver arriba) y se declara así en el resultado, no se fuerza a "ambiguo". Esta es la resolución explícita del solape entre las filas nuevas y B, hecha ahora.
3. Si no hay DiD decisivo ≥20pp: se cae a la escala original en su propio orden, `A → B → C`.
4. **C** conserva su condición propia (solo si la reserva dominante de un A/B débil es específicamente ausencia de panel) — no compite con las filas nuevas porque su precondición no se cumple cuando estas aplican.

---

*Commit 1 de 2 (Bloque A-bis / v2.4). Solo especificación — ningún resultado, ninguna tabla de datos abierta. No se edita jamás. El Paso 3 (corrida, veredicto, fila del registro de llaves, celda-D, contador, suite, PR) queda diferido como "parte 2" de este encargo, pendiente del ACTO A — autorizado por mesa el 11/ago/2026.*
