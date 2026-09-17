# TRA · `evade_norma` × (escolaridad_proxy × dominio_urbano_rural) — pre-registro de las 12 celdas del segundo piloto celda-D

### `prereg-caja-TRA-EVADE-NORMA-SXD12` · **v1.0** · 17 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/TRA-evade-norma-sxd12-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-TRA-EVADE-NORMA-SXD12`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | El `COMMIT-1` del `ACTO GEN2-CELDA-D-PILOTO-2` v1.1 (relanzamiento): spec congelada de dos `CALC` — `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` (`COMMIT-2`, cuatro candidatos emitidos sin ver el cruce de 2025) y `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001` (`COMMIT-3`, las 12 celdas de ENVIPE 2025 y la adjudicación). Todo lo sustantivo —universo, desenlace, ejes, ponderador, diseño, fórmulas, criterio— está escrito **antes de abrir un solo byte de microdato**. |
> | **QUÉ NO ES** | No es la spec previa `prereg-caja-ENVIPE-EVASION-NORMA` (`forense/prereg-caja/ENVIPE-EVASION-NORMA-spec-v1_0.md`): ésa registra la tasa nacional ya sellada; de ella se **reutilizan verbatim** desenlace y universo (§2.2, §3.1) y no se edita. No usa el cruce `edad × dominio` (reserva **CONSUMIDA-SIN-PILOTO**, Firma 2). No elicita `L` (Firma 1: «Sin L»). No adopta nada. No toca `milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`, `milpa/src/`, la spec previa, el marcador ni el crosswalk. |
> | **VERIFICAS ASÍ** | `sha256sum` de los tres payloads = §2.1; `python3 tools/corrida0.py spec-check CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` en VERDE; `python3 tests/test_marginales_una_variable.py` en OK; y —después de `COMMIT-2`— `RESULT-TRA-SXD12-G-CTRL-ARBITRO-VEREDICTO` dice si esta receta reproduce los ocho marginales sellados del árbitro. |

**Acto:** `ACTO GEN2-CELDA-D-PILOTO-2` v1.1, 17/sep/2026, entorno **CAJA** (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, corpus `montado=SI`, 419 archivos examinados), sobre `origin/main = e46e7e4` (el encargo se redactó contra `9207cb2`; 13 commits de `ADQ`/`CENSO`/`DERIVADOS` en medio, ninguno toca el perímetro). Encargo archivado verbatim: `forense/encargos/2026-09-17-GEN2-CELDA-D-PILOTO-2-V1_1.md` (0-bis `A.3`, commit `e2d252d`).

**Regla consumidora:** `tramite.evasion_norma` (`milpa/tramite.yaml:487`), `situacion: enfrenta_norma_percibida_inutil_o_extractiva`, `tier: FUERTE`. `A.8`, salida cruda de `python3 tools/ya_medido.py tramite.evasion_norma`: `milpa/tramite.yaml:487 … p=0.66 [TASA-EJECUTADA]` · `milpa/tramite-ola5-propuesta-v0.yaml:844 (id tramite.evasion_norma_envipe2025) … p=0.562774 [TASA-EJECUTADA]` · `data/corrida0: (sin apariciones)` · **`MEDIDA-EN: tramite-ola5-propuesta-v0.yaml, tramite.yaml`**. La regla está medida y sellada (nacional y por eje); lo que **no** existe es el cruce de dos ejes, y ésa es la reserva que este piloto evalúa.

---

## 0 · Lo que la lectura por archivo encontró, antes de congelar nada (A.15b/c)

Todo lo de abajo se leyó de los **catálogos y diccionarios que viajan dentro de cada zip** y de los **FD en PDF** (`fd_envipe2023.pdf` 5 545 líneas, `fd_envipe2024.pdf` 6 098, `fd_envipe2025.pdf` 7 207, vía `pdftotext -layout`). **Ningún archivo de `conjunto_de_datos/` se abrió** (`E.5`, `NC-0308`).

### 0.1 · Las preguntas 1.20 y 1.23 son **idénticas palabra por palabra** en las tres olas

| ola | FD, 1.20 (`BP1_20`) | FD, 1.23 (`BP1_23`) |
|---|---|---|
| 2023 (`fd_envipe2023.pdf`, líneas 4088-4091 / 4105-4119) | «¿Acudió ante el Ministerio Público o Fiscalía Estatal a denunciar el delito?» `1` Sí · `2` No | «¿Cuál fue la razón principal por la que no denunció o no denunciaron el delito ante el Ministerio Público o Fiscalía Estatal?» |
| 2024 (`fd_envipe2024.pdf`, 4639-4641 / 4660-4675) | idéntica | idéntica |
| 2025 (`fd_envipe2025.pdf`, 5048-5050 / 5067-5082) | idéntica | idéntica |

El **diccionario CSV** de `tmod_vic` etiqueta `BP1_20` como «Denuncia ante el MP» en 2023 y «Denuncia ante el MP o Fiscalía Estatal» en 2024/2025: cambia el **rótulo corto del diccionario**, no la pregunta (§ arriba) ni los códigos (`1`/`2` en las tres). Se declara y no altera nada.

### 0.2 · Los cuatro códigos del desenlace tienen el **mismo texto** en las tres olas (A.15c)

`tmod_vic_envipe<ola>/catalogos/bp1_23.csv`, verbatim:

| código | 2023 | 2024 | 2025 | ¿entra? |
|---|---|---|---|---|
| `01` | Por miedo al agresor | Por miedo al (a la) agresor(a) | Por miedo al (a la) agresor(a) | no |
| `02` | Por miedo a que lo extorsionaran | Por miedo a que lo (la) extorsionaran | Por miedo a que lo (la) extorsionaran | no |
| `03` | Delito de poca importancia | idem | idem | no |
| **`04`** | **Pérdida de tiempo** | **idem** | **idem** | **sí** |
| **`05`** | **Trámites largos y difíciles** | **idem** | **idem** | **sí** |
| **`06`** | **Desconfianza en la autoridad** | **idem** | **idem** | **sí** |
| `07` | No tenía pruebas | idem | idem | no |
| **`08`** | **Por actitud hostil de la autoridad** | **idem** | **idem** | **sí** |
| `09` | Otra | idem | idem | no |
| `99` | No sabe / no responde | idem | idem | no |
| `b` | blanco | idem | idem | no |

Los únicos cambios de texto entre olas son de lenguaje incluyente en `01` y `02` (2024→), **fuera del conjunto** `{04,05,06,08}`. La regla A.15c («si un código cambia de texto entre olas, la definición se ajusta por texto») no se dispara: **la definición es la misma en las tres olas por texto, no sólo por rótulo.**

### 0.3 · La variable de escolaridad y su catálogo: **idénticos** en las tres olas

`tsdem_envipe<ola>/catalogos/niv.csv`, verbatim e idéntico en 2023/2024/2025: `00` Ninguno · `01` Preescolar · `02` Primaria · `03` Secundaria · `04` Carrera técnica con secundaria terminada · `05` Normal básica (con antecedente en secundaria) · `06` Preparatoria o bachillerato · `07` Carrera técnica con preparatoria terminada · `08` Licenciatura o profesional · `09` Maestría o doctorado · `99` No sabe/no responde · `b` blanco. Diccionario: `NIV` «Nivel de instrucción», longitud 2, claves `00…09, 99, b` en las tres (tipo `Numérico` en 2023, `Carácter` en 2024/2025 — el archivo trae dos dígitos con cero a la izquierda en las tres; se lee como texto y se compara como texto).

**Construcción de `escolaridad_proxy`, la misma que el árbitro selló** — `ACTO MAESTRA35-L1 · P4` (el encargo la atribuye a `MAESTRA35-L5`; el archivo que la selló es `milpa/tramite-ola5-propuesta-v0.yaml:1672-1731`, campo `acto: "MAESTRA35-L1 · P4"`, y el código vive en `tools/ejes_maestra35_l1.py:42-46` (`ESC_2DIG`) invocado desde `tools/medidor_evasion_norma_envipe25.py:150`; censo de códigos en `forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md` §4.1 y spec `forense/notas/2026-09-02-MAESTRA35-L1-spec.md` §1.2). Verbatim:

| tramo | `NIV` |
|---|---|
| hasta primaria | `00, 01, 02` |
| secundaria | `03` |
| media superior | `04, 05, 06, 07` |
| superior | `08, 09` |
| **fuera** | `99`, blanco, y delito sin persona en `tsdem` |

Llave delito→persona: `ID_PER` (`tmod_vic` → `tsdem`), alfanumérica de 16, presente en las dos tablas en las tres olas. El módulo congelado **importa `ESC_2DIG` del mismo archivo del árbitro** (`tools/celda_d/marginales_reproduccion.py`), no lo copia.

### 0.4 · `DOMINIO`: tres claves, idénticas en las tres olas, en `tmod_vic`

`tmod_vic_envipe<ola>/catalogos/dominio.csv`: `U` Urbano · `C` Complemento urbano · `R` Rural, en 2023/2024/2025; diccionario: `Alfanumérico`, longitud 1. Como en el árbitro (`forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md` §4.5): es **eje propio**, no el corte de 15 000 habitantes, que ENVIPE no publica.

### 0.5 · `FAC_DEL` / `EST_DIS` / `UPM_DIS` existen en `tmod_vic` en las tres olas — con rango distinto

| variable | 2023 | 2024 | 2025 |
|---|---|---|---|
| `FAC_DEL` «Factor delito» | Numérico, 6, `000001…999999` | idem | idem |
| `EST_DIS` «Estrato de diseño muestral» | Alfanumérico, 3, `001…595` | Carácter, 3, `001…607` | Carácter, 3, `001…607` |
| `UPM_DIS` «Unidad primaria de muestreo» | Alfanumérico, **5**, `00001…99999` | Carácter, **7**, `0000001…9999999` | Carácter, **7** |

Se leen como texto y se agrupan por el par `(EST_DIS, UPM_DIS)` dentro de cada ola; nunca se cruzan UPM entre olas.

### 0.6 · Cobertura de `spec-check`

Los ocho pares `(archivo, variable)` por ola —`BP1_20, BP1_23, FAC_DEL, EST_DIS, UPM_DIS, ID_PER, DOMINIO` en `conjunto_de_datos_tmod_vic_envipe<ola>.csv` y `ID_PER, NIV` en `conjunto_de_datos_tsdem_envipe<ola>.csv`— existen en `data/inventario-reactivos-v1_2.tsv` (`metodo=INSPECT_ZIP`) para 2023, 2024 y 2025. `ID_DEL` (huella de la ola, §6) no se declara como variable de medición: es identificador.

### 0.7 · Control de reproducción del árbitro marginal, declarado antes de correr

`COMMIT-2` re-deriva con **esta** receta los ocho marginales de ENVIPE 2025 que el árbitro selló y los coteja contra los valores sellados **sin ajustar nada**:

| grupo | `p` sellado | IC95 sellado | `n` | fuente |
|---|---|---|---|---|
| hasta primaria | 0.493221 | [0.462397, 0.524253] | 3 491 | `milpa/tramite-ola5-propuesta-v0.yaml:1715` |
| secundaria | 0.567369 | [0.548202, 0.586405] | 7 739 | `:1716` |
| media superior | 0.543368 | [0.522009, 0.564012] | 11 476 | `:1717` |
| superior | 0.590093 | [0.574224, 0.605663] | 17 474 | `:1718` |
| Rural | 0.403310 | [0.377390, 0.428694] | 3 770 | `:1729` |
| Complemento urbano | 0.522090 | [0.503125, 0.540579] | 8 039 | `:1730` |
| Urbano | 0.592703 | [0.579102, 0.606130] | 28 471 | `:1731` |
| nacional | 0.562774 | [0.551982, 0.573448] | 40 280 | `milpa/tramite.yaml:497` (+`:522`), `milpa/tramite-ola5-propuesta-v0.yaml:871`; spec previa §1 |

Cobertura del eje escolaridad sellada: **0.997517** (100 delitos fuera); dominio: 1.000000. **Tolerancias**: `REPRODUCE` si `|Δp| ≤ 1e-6` **y** `|ΔIC| ≤ 1e-4` en los ocho; `NO-REPRODUCE` en otro caso, con cada Δ con signo y `Δn` emitidos. El IC se coteja porque el punto y el IC salen de **la misma función que usó el árbitro** (`tools/calibracion_mordida_encig_serie.py::wprop_ic_conglomerado`, seed 42, 10 000, importada): si reproducen `p` y no el IC, la diferencia está en el orden de filas o en el conjunto de UPM, y eso se quiere ver. **Un `NO-REPRODUCE` no invalida el piloto**: invalida la afirmación de que este medidor reproduce la receta del árbitro, y se reporta con la causa hasta donde el Δ la deje ver (precedente: primer piloto §3.3).

### 0.8 · La reserva y su guardia, por código

Firma 2: «toda lectura de ENVIPE 2025 antes de COMMIT-2 fuera de ese script es PARO». El script es `tools/celda_d/marginales_reproduccion.py`, congelado en este mismo commit:

* `marginal(ola, grupo: str)`: **un** `str` posicional; sin `*grupos`, sin lista. Dos → `TypeError`; lista → `TypeError`; eje inventado (`"a x b"`, columna pre-construida) → `ValueError`; el eje se deriva **dentro** desde `NIV`/`DOMINIO`.
* La `Ola` lleva **huella** (sha256 de `ID_DEL` en orden de archivo): una ola filtrada o reordenada tras cargarla lanza `ReservaRota` — el «marginal de escolaridad sobre las filas rurales» es la otra forma de cruzar.
* `cruce()` lanza `ReservaRota` sobre una ola cargada con `reservada=True`; `COMMIT-2` carga 2025 así (parámetro `ola_reservada: 2025` del contrato) y **prueba** la guardia en cada corrida, emitiendo `RESULT-TRA-SXD12-G-RESERVA-CRUCE-2025-DERIVADO = "NO"` sólo si el módulo lanzó.
* `tests/test_marginales_una_variable.py` (15 casos, fixtures fabricados) lo asierta.

**Lección `NC-0313` aplicada**: ningún `RESULT` de este `CALC` es un snapshot del árbol. Que `R` no existía al sellar `COMMIT-2` lo prueban el **commit** de `ejecucion.json` y el historial (`data/corrida0/CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001/resultados.json` no existe en ningún commit anterior al `COMMIT-3`), no un booleano recalculable.

---

## 1 · Estimando, población, unidad

**Estimando.** `p(evade_norma | escolaridad_proxy, dominio_urbano_rural)` — proporción ponderada `[0,1]` de **delitos** (`FAC_DEL`) del universo `BP1_20 ∈ {1,2}`, en **12 celdas**. Escala: proporción en todo objeto; distancias en **puntos porcentuales** (`pp = 100·|p̂ − R|`).

**Población objetivo.** 12 celdas = escolaridad_proxy {`S1` hasta primaria, `S2` secundaria, `S3` media superior, `S4` superior} × dominio_urbano_rural {`D1` Rural, `D2` Complemento urbano, `D3` Urbano}; rótulo de celda `SixDj`. Delitos sin escolaridad clasificable quedan **fuera** de las celdas, con la cobertura reportada (árbitro: 0.997517).

**Unidad.** DELITO (no persona), como la spec previa §1 (`n = 40 280` en 2025). **Universo restringido a delitos, declarado (A-bis 4)**: el estimando es la conjunta `P(no denunció ∧ razón de norma inútil o extractiva | enfrentó la norma)`, no la condicional — reserva heredada de `milpa/tramite.yaml:513-519`, no reabierta.

---

## 2 · Variables y códigos, por archivo y por ola

### 2.1 · Archivos

| input (`data/manifiesto.yaml`) | archivo | sha256 |
|---|---|---|
| `envipe2023_csv` | `envipe2023_csv.zip` | `0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404` |
| `envipe2024_csv` | `envipe2024_csv.zip` | `90776b2fab6e3666dad1cb5f5f3eb7d6a7699dbfefd4f8f04f07fb01e61a6fb2` |
| `envipe2025_csv` | `envipe2025_csv.zip` | `8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` |
| `envipe2023_fd_pdf` · `envipe2024_fd_pdf` · `envipe2025_fd_pdf` | `fd_envipe<ola>.pdf` | `743c260e…`, `f8d72038…`, `83fe0246…` (manifiesto; el runner los resuelve por sha) |

Miembros: `tmod_vic_envipe<ola>/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe<ola>.csv` y `tsdem_envipe<ola>/conjunto_de_datos/conjunto_de_datos_tsdem_envipe<ola>.csv`. Lectura como texto (`dtype=str`), UTF-8 y caída a latin-1 **declarada** (`RESULT-…-ENCODING-TMODVIC`), BOM y `\r` normalizados, columnas y valores `strip()` de espacios y comillas.

### 2.2 · El desenlace — verbatim de la spec previa §1, sin cambio

`evade_norma = 1 ⟺ BP1_20 == "2" ∧ BP1_23 ∈ {"04","05","06","08"}` (dos dígitos; `b`/blanco → vacío, nunca cuenta); `evade_norma = 0` en el resto del universo. Ninguna tercera categoría: el complemento es `1 − p`.

### 2.3 · Los dos ejes

* `escolaridad_proxy` := `ESC_2DIG[NIV]` de la persona `ID_PER` en `tsdem` (§0.3); `(fuera)` si `NIV ∉ {00..09}` o si el delito no tiene persona en `tsdem`.
* `dominio_urbano_rural` := `{U: Urbano, C: Complemento urbano, R: Rural}[DOMINIO]` de `tmod_vic` (§0.4); `(fuera)` si otro valor (no debe ocurrir; se cuenta).

---

## 3 · Universo, filtros, ponderador, diseño

### 3.1 · Universo y filtros, idénticos en las tres olas

En este orden y sin ninguno más: (1) filas de `tmod_vic` con `BP1_20 ∈ {"1","2"}` — las demás (blanco, otro) **se cuentan** (`FILAS-BP1_20-FUERA`) y salen; (2) `FAC_DEL` numérico y `> 0` — si alguna fila no lo cumple el medidor **PARA** (guardia verbatim del árbitro); (3) `EST_DIS`/`UPM_DIS` no vacíos — si falta alguno, **PARA**. No se filtra por edad, sexo ni tipo de delito. Los delitos sin persona en `tsdem` **no paran** (el árbitro paraba, con 0 huérfanos en 2025; en 2023/2024 nadie lo ha medido): se cuentan (`DELITOS-SIN-PERSONA`) y quedan `(fuera)` de escolaridad — en 2025 el control §0.7 los delata vía `Δn`. `ID_PER` no única en `tsdem` → **PARA**.

**Convención de universo por eje, la del árbitro**: los marginales y celdas de escolaridad se estiman sobre los delitos con escolaridad clasificable; los de dominio y el nacional sobre el universo entero. El cruce de 12 celdas, sobre los clasificables en ambos ejes. `I(s,d)` (§4) combina las cuatro cantidades con esta misma convención en cada ola; la pérdida es ≤ 0.3 % del universo y se reporta como cobertura por ola.

### 3.2 · Ponderador

`FAC_DEL` en las tres olas (§0.5). Toda proporción es razón de totales ponderados `Σ w·y / Σ w`.

### 3.3 · Diseño muestral e intervalos — dos objetos, declarados

1. **IC del árbitro** (`R` en `COMMIT-3` y los ocho marginales del control §0.7): `wprop_ic_conglomerado` importada de `tools/calibracion_mordida_encig_serie.py` — bootstrap de conglomerado por celda, estratificado por `EST_DIS`, UPM = `(EST_DIS, UPM_DIS)`, `n_boot = 10 000`, `seed = 42`, `numpy.random.default_rng`, percentiles por orden `[int(0.025·n)]` y `[int(0.975·n) − 1]`. **Es la receta del árbitro, el mismo objeto de código.**
2. **Réplicas compartidas por ola** (candidatos `C1`, `C2`, `C6`, `C7` e interacciones): `tools/celda_d/marginales_reproduccion.py::replicas_compartidas` — UN remuestreo por ola, `n_h` UPM con reemplazo dentro de cada estrato, `numpy.random.PCG64(42)`, estratos en orden lexicográfico de `EST_DIS` y UPM de `UPM_DIS`, 10 000 réplicas; **todos** los grupos y celdas de una ola se evalúan sobre el mismo remuestreo, de modo que `p^(r)(s)`, `p^(r)(d)`, `p^(r)`, `p^(r)(s,d)` se empujan juntos por las fórmulas (sin delta, sin independencia entre estimadores de la misma ola, sin covarianzas inventadas). Entre olas las muestras **son** independientes: la réplica `k` de 2024 se combina con la réplica `k` de 2025 (y de 2023). IC95 = percentiles 2.5 / 97.5 (`numpy.percentile`) de las réplicas definidas.

### 3.4 · Soporte, umbral y salida predefinida

`n(celda) ≥ 200` delitos **sin ponderar**, por ola: `n₂₀₂₄` y `n₂₀₂₃` en `COMMIT-2`, `n₂₀₂₅` en `COMMIT-3`. Una celda es **PUNTUADA** si `n₂₀₂₃, n₂₀₂₄, n₂₀₂₅ ≥ 200` y los cuatro candidatos tienen punto definido (2023 entra porque `C7` lo necesita). `FUERA-DE-SOPORTE` se emite marcada con su punto e IC y **no puntúa**; `n = 0` → `NO-ESTIMABLE` (`null`), nunca `0.0`. Esperado mínimo, verificado sólo cuando el dato lo permita: hasta primaria (3 491 en 2025) × Rural (~9 %) ≈ 300.

---

## 4 · Los candidatos, su dieta y su incertidumbre — y lo que no entra

Notación: `logit p = ln(p/(1−p))`, `expit z = 1/(1+e^{−z})`. **Interacción de una ola** `w`:
`I_w(s,d) := logit p_w(s,d) − [logit p_w(s) + logit p_w(d) − logit p_w]`. Rechazo explícito: si algún término es exactamente `0` o `1` (punto o réplica), esa cantidad queda **SIN-DEFINIR** en ese punto/réplica — sin recorte, sin sustitución; réplicas descartadas contadas.

| id | rol | fórmula del punto | dieta | incertidumbre |
|---|---|---|---|---|
| **`C1`** | `BASELINE_INGENUO` · persistencia | `p̂ = p₂₄(s,d)` | ENVIPE 2024, cruce | réplicas compartidas 2024 |
| **`C2`** | `BASELINE_INGENUO` · marginales 2025 sin interacción | `p̂ = expit(logit p₂₅(s) + logit p₂₅(d) − logit p₂₅)` con los **marginales sellados** de §0.7 (citados, no recalculados); se emite además `C2-P-REDERIVADO` con los re-derivados | los ocho números públicos del árbitro | réplicas compartidas de los marginales 2025 re-derivados por el módulo congelado, empujadas por la forma log-aditiva |
| **`C6`** | `CHALLENGER` · marginales 2025 + interacción 2024 | `p̂ = expit(logit C2 + I₂₄(s,d))` | `C2` + ENVIPE 2024 | réplica `k` de 2025 (logit `C2_k`) con réplica `k` de 2024 (`I₂₄,k`) |
| **`C7`** | `CHALLENGER` · marginales 2025 + interacción promediada | `p̂ = expit(logit C2 + (I₂₃(s,d) + I₂₄(s,d))/2)` | `C2` + ENVIPE 2023 + 2024 | réplica `k` de las tres olas |
| `C4` | matriz `B·θ(x) → h_r` | — | — | **INEJECUTABLE**, faltantes por nombre: `h_r` inexistente (`milpa/src/emisor.py:364`, «OLA futura, declarado»); `θ` de `G1` por celda no medido (`milpa/theta-esquema-e1-v1_0.yaml:405-416`: `G1` clase `ASIGNADO`, `identificacion: AUSENCIA_DE_FACTO`, `universo: NO-DECLARADO`) |
| `C5` | emisor, `x = ∅` | `p_nacional = 0.562774` | `milpa/tramite.yaml:497` (copia del árbitro) | **NO-APLICA**: diagnóstico puro `|0.562774 − R|` por celda en `COMMIT-3`; no compite |
| `L` | — | — | — | **no entra**, por Firma 1 («Sin L») |

`C2` importa `piso_log_aditivo` de `tests/test_celda_d_c2.py` (rango `(0,1)`, rechazo si un marginal es 0 o 1, mismo `desenlace_id` en los tres marginales); el rótulo obligatorio del supuesto es «ausencia de interacción en escala logit», nunca «independencia». Si `C2` no es construible en alguna celda, esa celda no puntúa y `C2` pasa a `DIAGNOSTICO-POR-REPLIEGUE`.

**Emitir ≠ decidir.** `COMMIT-2` emite 12 estimaciones por candidato con intervalo. **Signo de la modulación** respecto del nacional `0.5628` (`COMMIT-3`, cuando `R` existe): `ESTABLE` si todo el IC95 del candidato queda del mismo lado de `0.5628` que `R`; `AMBIGUA` si el IC lo cruza; `CONTRARIA` si queda entero del lado opuesto. Nada se adopta.

---

## 5 · Criterio de adjudicación — escrito antes del dato

1. **Árbitro `R`**: las 12 celdas de ENVIPE 2025 con la receta §3.3(1); `EE(R) = (IC95sup − IC95inf)/3.92`. **No se derivan hasta `COMMIT-3`.**
2. **Error por celda**: `d_k = 100·|p̂_k − R|` en pp, para `k ∈ {C1, C2, C6, C7}`.
3. **Cada challenger contra cada piso**, en cada celda PUNTUADA — **INDECIDIBLE** si cualquiera de las dos condiciones del programa, verbatim: «**si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R)**» (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38`; aquí `d_L` = el challenger, `d_M` = el piso, y `0.5·EE(R)` en la misma escala que `d`). Si no es INDECIDIBLE: `GANA-CHALLENGER` si `d_chal < d_piso`, `GANA-PISO` en otro caso. **Precedencia: INDECIDIBLE.**
4. **Celda-D**: un challenger **gana** sólo si vence a **los dos** pisos en **≥ 9** de las PUNTUADA **y** las PUNTUADA son **≥ 9 de 12**. Familia: 12 celdas × 2 challengers; sin valor-p. Skill `= 1 − MAE_chal/MAE_piso` por challenger y piso, sobre las PUNTUADA: **se reporta, no adjudica**.
5. **Paradas admisibles**, sin ganador forzado, evaluadas en este orden: `FUERA-DE-SOPORTE` (≥ 4 de 12 celdas sin soporte en alguna ola — es un hecho del dato y se lee antes que nada); luego `INDECIDIBLE` (PUNTUADA < 9, o todas las PUNTUADA INDECIDIBLES para ambos challengers); luego `ADJUDICADA` (algún challenger cumple 4); si no, `SIN-CANDIDATO-SUPERIOR`. Entre `INDECIDIBLE` y `ADJUDICADA` manda `INDECIDIBLE`. Si los dos challengers cumplieran 4, se declaran ambos y **mesa** elige: este acto no corona.
6. **B-bis, declarado**: nadie vence a `C1` → persistencia anual corroborada en `TRA`. Nadie vence a `C2` → «marginales actuales sin interacción» es el estimador honesto de celda para esta familia; la interacción de olas previas no aporta **bajo estos candidatos** — resultado de programa, cambia el marcador (y sólo eso dice: no identifica ausencia de interacción ni una propiedad de la población). `C6` o `C7` vencen → primer estimador por celda que explota interacción. `C7` vence y `C6` no → una ola sola trae ruido. Límite de la evaluación: el que se elige con las 12 celdas no queda validado de forma independiente por ellas.
7. **Adopción: ninguna.** `champion_actual: NINGUNO`, `requiere_decision_mesa: false` en la celda-D porque no hay decisión que tomar sobre el motor: no se propone adoptar.

---

## 6 · Tolerancias, determinismo, y qué cuenta como reproducción

* Enteros: exacto. Flotantes: `abs = 1e-10` (`tolerancia.tipo: bootstrap`, `exacto_por_seed: true`): seed 42, `PCG64` para las réplicas compartidas y `default_rng(42)` en `wprop_ic_conglomerado`, orden de consumo fijado (§3.3). Dos corridas sobre los mismos bytes dan los mismos 10 000 vectores.
* La **huella** de cada ola (`sha256` de `len` + `ID_DEL` en orden de archivo) la recalcula el módulo en cada llamada.
* `verify` sobre `COMMIT-2` debe dar `REPRODUCE` **de forma permanente**: no hay `RESULT` que dependa del estado del árbol (§0.8).

---

## 7 · Orden de los commits — el orden del diff es el sello

| commit | contenido | microdato abierto |
|---|---|---|
| **`COMMIT-1`** | esta spec + sidecar `.sha256` + `spec.md`/`spec.yaml`/`medidor.py` de `…-EMISIONES-0001` + `tools/celda_d/marginales_reproduccion.py` + `tests/test_marginales_una_variable.py` | **ninguno** (fixtures fabricados; `E.5`) |
| **`COMMIT-2`** | `preflight → run → verify` de `…-EMISIONES-0001`; sello | 2023 y 2024 enteras; 2025 **sólo marginales por el módulo** |
| **`COMMIT-3`** | `spec.yaml`/`medidor.py` de `…-ARBITRO-CRUCE-0001` (input: el `resultados.json` sellado de las emisiones, por sha), `preflight → run → verify`; celda-D; la fila de `tramite.evasion_norma` en `milpa/catalogo-momentos-v0_1.tsv`; test del consumidor | 2025, cruce |

Nada se corre en seco antes de `COMMIT-1` (`E.5`, `NC-0308`). Si al correr `COMMIT-2` esta spec resulta inejecutable por cableado (formato, columna, encoding), se sucede con `v1.1` en **archivo propio** y contrato verbatim; **esta versión no se edita** (`E.3`, `NC-0094`).

---

## 8 · Lo que este pre-registro NO promete

No promete que las 12 celdas tengan soporte en las tres olas (se mide). No promete que la receta reproduzca al árbitro a `1e-6` (se mide, §0.7). No promete un ganador (§5.5). No mide la condicional `P(razón | no denunció)`. No toca el motor.

**El primer resultado que produzca este procedimiento es el que se reporta.**
