# ACTO MAESTRA34-L5 · P1 · `tramite.gobierno_digital.util_sin_coercion` — SPEC CONGELADA

**COMMIT-1 de la pieza P1.** Este archivo se escribe **antes de calcular ningún
desenlace**. Lo único que se ha tocado de ENCIG 2025 hasta aquí son la estructura
de la base de datos, la lista de columnas y los **denominadores por `N_TRA`**
(P0 · censo, `forense/notas/2026-09-02-MAESTRA34-L5-P0-censo.md`): en ningún
momento se ha cruzado `N_TRA` ni ningún filtro contra `P7_3`, que es la variable
de desenlace de esta pieza.

**Prior que se pone a prueba** (`milpa/tramite.yaml:177-201`, clase ASIGNADO, tier
MEDIA-FUERTE, **probabilidades explícitamente NO CALIBRADAS** según su propia
`nota_calibracion`): `adopta p=0.71` / `rechaza_servicio p=0.29`, bajo
`contexto_producto: {coercitivo: false, riesgo_fiscal_percibido: false}`.

---

## §1 · Spec

### 1.1 Payload y tabla

| campo | valor |
|---|---|
| payload | `data/raw/encig25_base_datos_csv.zip` · id de manifiesto `encig25_base_datos_csv` (`data/manifiesto.yaml:4214`) |
| tabla | `encig2025_04_sec_7.csv` (sección VII · Calidad de trámites y servicios públicos) |
| unidad de análisis | **TRÁMITE**, no persona |
| lector | `leer_csv_cr` de `tools/calibracion_mordida_encig_serie.py` (tolerante al CR suelto y embebido de INEGI), `encoding='utf-8'` — verificado en P0 que esta tabla decodifica en UTF-8 sin reemplazos |

### 1.2 Deduplicación

`sec_7` trae filas repetidas: 124 314 filas contra 113 717 `ID_TRA` únicos.
`MAESTRA34-L1` ya verificó que los 10 597 excedentes son **duplicados exactos**
en `P7_3`/`FAC_TRA`/`EST_DIS`/`UPM_DIS` (`forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`,
fila `TRA-M-13`). **Se deduplica por `ID_TRA` conservando la primera aparición**, y
la corrida **re-verifica por su cuenta** que dentro de cada `ID_TRA` repetido los
valores de `N_TRA`, `P7_3`, `FAC_TRA`, `EST_DIS` y `UPM_DIS` son idénticos. Si no
lo fueran, la pieza **PARA** y lo reporta en vez de elegir una fila.

### 1.3 Universo — el juicio declarado del acto

ENCIG 2025 **no** pregunta si el canal digital estaba disponible ni si su uso era
obligatorio (P0 · §2: cero ítems en 483 columnas de 2025 y ~100 000 de cinco
olas). La situación `le_ofrecen_servicio_gobierno_digital` y los disparadores
`coercitivo: false` / `riesgo_fiscal_percibido: false` **no los dicta el dato**:
los fija este acto restringiendo el universo a tipos de trámite (`N_TRA`) que
cumplen los tres criterios siguientes, declarados aquí y no derivados de mirar el
desenlace:

1. **Disponibilidad nacional del canal digital** — el canal existe para todo
   informante del país, no depende del municipio o del estado en que viva.
2. **Uso opcional** — existe canal presencial legalmente equivalente, así que
   elegir el digital es una conducta y no una imposición.
3. **Sin riesgo fiscal percibido** — el trámite no es ante autoridad fiscal ni
   obliga a declarar ingresos o patrimonio.

**Universo principal: `N_TRA == '01'`** — «el pago ordinario del servicio de luz».
Es el único tipo del catálogo que cumple los tres sin ambigüedad: la Comisión
Federal de Electricidad opera portal y aplicación de cobertura nacional (1), el
mismo recibo se paga en ventanilla, banco o tienda (2), y no interviene autoridad
fiscal alguna (3). Denominador contado en P0: **n = 20 392 filas** antes de
deduplicar.

**Exclusiones y su razón** (se declaran para que el juicio sea auditable, no para
justificarlo después): `02` agua y `03` predial son municipales y su canal digital
varía por municipio — falla (1), y `03` además es un impuesto — falla (3); `04`
tenencia y `05` trámites vehiculares son estatales y varias de sus piezas exigen
presencia física — falla (1) y (2); `06` trámites fiscales ante el SAT falla (2) y
(3) y es justamente el caso que P2 no pudo medir; `07`/`08` atención médica
confunden el trámite con acudir al hospital, de modo que el canal presencial queda
impuesto por el propio trámite — falla (2); `17` pasaporte exige comparecencia —
falla (2); el resto son locales o de ventanilla.

**Sensibilidad pre-declarada A — universo ampliado: `N_TRA ∈ {'01','10'}`.**
Añade «trámites en el registro civil (actas de nacimiento, defunción, matrimonio,
divorcio)», donde el acta de nacimiento sí tiene expedición digital nacional pero
las otras tres no la tienen de manera uniforme: cumple (1) solo parcialmente. Se
reporta como sensibilidad, **nunca** como resultado principal.

### 1.4 Dicotomización de la conducta

`P7_3` — «¿A qué tipo de lugar acudió o a qué medio recurrió para realizar el
trámite o pago?»

| valor de `P7_3` | etiqueta INEGI | asignación |
|---|---|---|
| `4` | Internet (página web, aplicaciones de celular, tablet) | **`adopta` = 1** |
| `5` | Cajero automático o kiosco inteligente | **`adopta` = 1** |
| `1` | Instalaciones de gobierno (oficinas, tesorería, hospital) | `adopta` = 0 |
| `2` | Banco, supermercado, tiendas o farmacias | `adopta` = 0 |
| `6` | Módulos, clínicas u oficinas temporales o móviles | `adopta` = 0 |
| `3` | Líneas de atención telefónica | **fuera del universo** |
| `7` | No se ha podido concluir el trámite o pago | **fuera del universo** |
| `8` | Otro | **fuera del universo** |
| `9` | No sabe / no responde | **fuera del universo** |
| blanco | — | **fuera del universo** |

`3` sale porque una línea telefónica es un canal remoto **atendido por una
persona**: ni servicio digital de autoservicio ni ventanilla presencial. Se
prefiere excluirlo a forzar una categoría binaria sobre un canal mixto — el mismo
criterio que `MAESTRA34-L1` aplicó a `2` y `6` en su propia pieza. `7` sale porque
es fracaso del trámite, no elección de canal.

**Divergencia explícita frente a `MAESTRA34-L1`, declarada aquí y no descubierta
después.** `TRA-M-13` clasificó `P7_3 ∈ {3,4,5}` como «digital/registrado» porque
su constructo era el **registro** — una llamada telefónica deja rastro. El
constructo de esta pieza es **adopción de un servicio digital de gobierno**
(utilidad ⇒ adopción, mecanismo del §3.3 del modelo, validado contra SPEI/CoDi),
y una llamada atendida por una persona no es un servicio digital. Misma fuente,
misma variable, distinto constructo, distinta partición: se declara para que nadie
lea las dos cifras como si midieran lo mismo.

**Sensibilidad pre-declarada B — `3` dentro del denominador como NO adopción**
(`adopta = 0`), por si mesa prefiere leer el teléfono como canal no digital en
lugar de excluirlo.

### 1.5 Ponderador, diseño e intervalo

| campo | valor |
|---|---|
| ponderador | **`FAC_TRA`** — factor de expansión de **trámite**, que es la unidad de análisis. No `FAC_P18`, que expande personas |
| estrato | `EST_DIS` |
| UPM | `UPM_DIS` |
| estimador | proporción ponderada `p̂ = Σ(w·d) / Σw` |
| IC95 | **bootstrap conglomerado estratificado**, `n_boot = 10 000`, `seed = 42`, remuestreando UPM dentro de estrato — función `wprop_ic_conglomerado` de `tools/calibracion_mordida_encig_serie.py`, importada, **no reescrita** |
| escala | proporción en [0, 1] |

### 1.6 Estimando

**p̂ = proporción, ponderada por trámite, de trámites del universo realizados por
canal digital de autoservicio.** Es la contraparte empírica de `adopta` bajo
`coercitivo: false, riesgo_fiscal_percibido: false`, con la salvedad de que la
condición no la declara el informante sino la construcción del universo (§1.3).

### 1.7 Lo que este resultado NO es, dicho antes de tener el número

- **No** es «la tasa de adopción de gobierno digital en México»: es la de un tipo
  de trámite elegido por cumplir tres criterios declarados.
- **No** se compara contra P2, porque P2 quedó en EXISTE-NO-SATISFACE (P0 · §3).
  La comparación de SIGNO y razón que el encargo pedía **no se hace**.
- **No** se compara contra el `0.91` de la regla coercitiva: son escalas distintas
  sin enlace, y el encargo lo prohíbe expresamente.
- El prior `0.71` que se contrasta es, según su propia `nota_calibracion` en
  `milpa/tramite.yaml`, una probabilidad **no calibrada** cuyo corpus «da la
  dirección, no la magnitud». Una diferencia de magnitud contra él es información
  sobre la magnitud que nunca se afirmó, y así se reportará.

---

## §2 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**

Si el procedimiento resulta equivocado, se escribe un tercer commit que lo diga;
no se corrige hacia atrás ni se reescribe esta spec.

---

## §3 · ENMIENDA 1 a la spec — la guardia disparó y tenía razón

**Escrita antes de que exista ningún resultado de esta pieza.** La spec de §1.2
mandaba deduplicar por `ID_TRA` y **PARAR** si los excedentes no eran exactos.
La corrida paró: **501 llaves `ID_TRA` con `P7_3` distinto entre sus filas**. La
spec no se corrige hacia atrás; se enmienda aquí, con el sello nuevo al final.

### 3.1 Qué resultó ser

`ID_TRA` **no es la llave de `sec_7`**. La llave es **`(ID_TRA, NT_TIPO)`**, y es
exacta:

| comprobación | comando | resultado |
|---|---|---|
| filas de `sec_7` | `len(df)` | 124 314 |
| `ID_TRA` únicos | `df['ID_TRA'].nunique()` | 113 717 |
| **`(ID_TRA, NT_TIPO)` únicos** | `df.groupby(['ID_TRA','NT_TIPO']).ngroups` | **124 314 — llave exacta** |
| filas idénticas en todas las columnas sustantivas | `len(df) - df[cols].drop_duplicates().shape[0]` | **0** |
| llaves `ID_TRA` repetidas | | 7 430 |
| …de ellas con alguna columna distinta | | **7 430 (todas)** |
| …de ellas con `P7_3` distinto | | 501 |

`NT_TIPO` es «Número de trámite · Último evento», rango 01-03 (estructura de la
base de datos de ENCIG 2025). Un informante puede reportar hasta tres **eventos**
del mismo tipo de trámite; cada evento es una fila legítima y puede haberse hecho
por un canal distinto. **En `sec_7` no hay un solo duplicado exacto.** Los 10 597
«excedentes» son 10 597 trámites distintos.

### 3.2 Qué cambia en la spec

**Se suprime la deduplicación.** El universo son las filas tal cual, con llave
`(ID_TRA, NT_TIPO)`; la corrida verifica que esa llave sea única y **PARA** si no
lo es. Es lo coherente con la unidad de análisis ya congelada (TRÁMITE) y con el
ponderador ya congelado (`FAC_TRA` expande trámites, no personas): deduplicar
habría tirado eventos reales y roto la expansión.

**Nada más cambia.** Universo (`N_TRA='01'`, sensibilidad A `{01,10}`),
dicotomización (`adopta = P7_3 ∈ {4,5}`; no adopta `{1,2,6}`; fuera `{3,7,8,9,b}`;
sensibilidad B), ponderador, diseño, bootstrap, semilla y escala quedan **tal
como se congelaron en §1**, sin tocar.

### 3.3 Hallazgo sobre un acto ya sellado — se reporta, no se repara

`forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`, fila `TRA-M-13`
(`ACTO MAESTRA34-L1`, PR #451, ADR-276), afirma textualmente: «113717 ID_TRA
unicos tras deduplicar 10597 duplicados EXACTOS -- verificado, mismos valores en
P7_3/FAC_TRA/EST_DIS/UPM_DIS». **La afirmación es falsa**, y no solo en general:
lo es **dentro del propio subconjunto de aquel acto**. Restringiendo `sec_7` a las
21 139 llaves con `P8_4 ∈ {0,1}` que su join usa, quedan 24 974 filas en 21 139
`ID_TRA`: **2 576 llaves repetidas (6 411 filas), las 2 576 con `NT_TIPO` distinto
y 160 con `P7_3` distinto**. Su deduplicación descartó 3 835 eventos de trámite
reales y, en 160 llaves, eligió un canal entre dos que difieren.

Este acto **no repara** nada de eso: `forense/prereg-duelo-v2/` está fuera de su
perímetro, y la cifra de aquel acto es de quien la selló. Queda como línea de
`forense/hallazgos.md` y como firma pendiente para mesa.

### 3.4 Sello de la enmienda

**El primer resultado que produzca el procedimiento enmendado es el que se
reporta.** Ningún desenlace de esta pieza se ha calculado al escribir estas
líneas: lo único que se ha mirado de `sec_7` son estructura de llave, conteos de
filas y el número de llaves donde `P7_3` difiere — nunca el valor de `P7_3` en el
universo `N_TRA='01'`, ni ponderado ni sin ponderar.

---

## §4 · RESULTADO (COMMIT-3 de la pieza)

Corrida: `python3 tools/medidor_gobierno_digital_encig25.py`.
Payload `data/raw/encig25_base_datos_csv.zip`,
`sha256 = 47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12`
(idéntico al que `MAESTRA34-L1` selló para el mismo ZIP — misma fuente, misma
copia). Tabla `encig2025_04_sec_7.csv`: 124 314 filas, llave `(ID_TRA, NT_TIPO)`
verificada única en la corrida, sin deduplicar (enmienda 1).

### 4.1 Principal

| campo | valor |
|---|---|
| estimando | proporción ponderada de trámites de pago ordinario de luz realizados por canal digital de autoservicio |
| **p̂** | **0.673393** |
| **IC95** | **[0.663165, 0.683910]** |
| n | 20 203 trámites (de 20 392 del tipo; 189 caen fuera por `P7_3 ∈ {3,7,8,9}`) |
| adoptan | 13 905 |
| estratos · UPM | 441 · 8 486 |
| población expandida | 120 445 646 trámites |
| ponderador | `FAC_TRA` |

### 4.2 Sensibilidades pre-declaradas

| sensibilidad | p̂ | IC95 | n |
|---|---|---|---|
| **A** · universo `N_TRA ∈ {01,10}` (+ registro civil) | 0.641048 | [0.630858, 0.651033] | 27 356 |
| **B** · teléfono (`P7_3=3`) como NO adopción | 0.666332 | [0.655955, 0.676752] | 20 367 |

Ninguna de las dos mueve la lectura: el resultado está entre 0.64 y 0.67 en las
tres variantes, y las tres excluyen tanto el doble como la mitad del prior.

### 4.3 Contraste con el prior — **no refutado**

| | prior ASIGNADO | medido | razón medido/prior |
|---|---|---|---|
| `adopta` | 0.71 | **0.673393** | **0.9484** |
| `rechaza_servicio` | 0.29 | 0.326607 | 1.1262 |

El criterio de refutación que fijó el encargo es «más del doble o mitad». La razón
es **0.95**: el prior **no queda refutado**, queda **confirmado en magnitud** con
un error relativo de **5.2 %**.

Vale la pena decir por qué esto es más de lo que parece. La `nota_calibracion` de
esa misma regla, escrita cuando se compiló, advierte: «PROBABILIDADES NO
CALIBRADAS. El corpus da la dirección (SPEI se adopta), no la magnitud —deuda
declarada de elasticidades—». Es decir, el 0.71 **nunca reclamó ser una magnitud**.
La medición dice que, además de la dirección, la magnitud asignada a ojo estaba a
un 5 % del dato. Es la primera vez que una de las tres reglas de gobierno digital
se contrasta contra microdato.

**El 0.71 cae fuera del IC95** [0.663, 0.684]. Eso **no** se reporta como
refutación y no debe leerse como tal: con n≈20 000 trámites y 8 486 UPM el
intervalo mide ±1 punto porcentual, así que excluye cualquier valor que no
coincida en dos decimales — y un prior que se declara no calibrado no afirma dos
decimales. Lo que el IC dice es que la medición es precisa, no que el prior sea
falso. Se propone `CONFIRMADA-EN-MAGNITUD`, no `REFUTADA-POR-DATO`; **sella mesa**.

### 4.4 Lo que este número no dice

- No es la adopción de gobierno digital en México: es la de **un** tipo de trámite
  escogido por cumplir los tres criterios de §1.3.
- No se compara con P2, que quedó en EXISTE-NO-SATISFACE (P0 · §3), ni con el
  `0.91` de la regla coercitiva: escalas distintas sin enlace.
- La condición «sin coerción y sin riesgo fiscal» la impone la construcción del
  universo, **no** una declaración del informante. Si mesa juzga que pagar la luz
  por la aplicación de CFE no es «servicio de gobierno digital» en el sentido del
  §3.3 del modelo, cae el mapeo, no el dato: la cifra sigue siendo válida como
  adopción de canal digital para ese trámite.
- El universo son **trámites**, no personas: quien pagó la luz doce veces en 2025
  contribuye según el diseño de la encuesta, y `FAC_TRA` expande trámites.
