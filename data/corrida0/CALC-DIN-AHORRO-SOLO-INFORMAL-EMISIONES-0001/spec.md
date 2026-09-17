# DIN · `ahorra_solo_informal` × (localidad × edad) — pre-registro de las 8 celdas del primer piloto celda-D

### `prereg-caja-DIN-AHORRO-SOLO-INFORMAL-LXE8` · **v1.1** · 16 de septiembre de 2026

> **SUCEDE A `v1.0` (`sha256 = f54c3170fc653607b3b916ccc3857bc960c3578bfdd4dd40306725e1110f19e9`), QUE NO SE EDITA.**
> `v1.0` se congeló en el `COMMIT-1` de este mismo acto (`3461c46`) y queda **intacta como historia**.
> Esta `v1.1` existe porque **`FP-379` (firma de mesa, 16/sep/2026) llegó después de ese commit y enmienda `C2`** —
> y la casa amienda un pre-registro sellado **con un archivo propio**, nunca in situ (`E.3`; precedente `NC-0094`).
> **Ninguna corrida se había sellado contra `v1.0`**: cuando `FP-379` llegó, el árbol tenía `COMMIT-1` cerrado,
> `medidor.py` sin escribir y cero `RESULT` producidos. **No hubo mezcla de diseños: la fórmula multiplicativa
> nunca se implementó.** Qué cambia exactamente: §0.7.

### `prereg-caja-DIN-AHORRO-SOLO-INFORMAL-LXE8` · v1.0 → **v1.1** · 16 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/DIN-ahorro-solo-informal-lxe8-spec-v1_1.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-DIN-AHORRO-SOLO-INFORMAL-LXE8`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, **congelado antes de abrir un solo byte de microdato**, del primer piloto de celda-D: `p(ahorra_solo_informal │ localidad, edad)` en **8 celdas de cruce**, con tres candidatos emisores (`C1` persistencia ENIF 2021, `C2` piso marginal de ENIF 2024, `C3` elicitación de `L` en dos dietas), un cuarto `INEJECUTABLE` y un quinto `NO-APLICA`. Gobierna **dos** CALC: `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` (las emisiones) y `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001` (el árbitro `R` del cruce y la adjudicación). |
> | **QUÉ NO ES** | **No adopta nada al motor.** No toca `milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`, `milpa/src/`, el marcador ni el crosswalk. No firma `FP-376` (viene firmada). No re-discute el diseño v1.1 de dirección. **No deriva `R` antes de que las emisiones estén selladas.** No calcula `formalidad` (sale del diseño por el hallazgo 1 del careo). No corona un campeón: `champion_actual = NINGUNO` y adoptar es de mesa. |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py spec-check CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` en VERDE (0 FAIL) sobre **este** contrato; después `preflight` → `run` → `verify` sobre cada uno de los dos CALC. Los seis checks del GO de `E.5` se reportan por nombre en la nota de cierre. |

**Acto:** `ACTO GEN2-CELDA-D-PILOTO-1`, 16/sep/2026, entorno **CAJA** (Ubuntu/WSL2, corpus montado, `archivos_examinados = 414`). Bajo **FP-378** (FIRMADA, `ADR-533`) y **FP-376** (FIRMADA), verbatim en `forense/encargos/2026-09-16-GEN2-CELDA-D-PILOTO-1.md`. Diseño vigente: `forense/notas/insumos-direccion/CELDA-D-PILOTO-diseno-direccion-v1_1-post-careo-2026-09-17.md` (sha256 del cuerpo `68a794936ef2ca47cf052b3a1e64ca002c87fb7d9e8cefb8ae998220c99f19cb`), **sucedido operativamente** por `forense/notas/2026-09-17-GEN2-CELDA-D-CAREO-1-CORRECTIVO-PRE-EMISION.md` en todo lo que toca *cómo se calcula o qué se concluye* (regla de lectura de esa nota).

---

## 0 · Lo que la lectura por archivo encontró, antes de congelar nada

`A.15c` del diseño v1.1 §1 ordena, literalmente, que «los códigos se verifican **por archivo** en los FD de 2021 y 2024 antes de COMMIT-1». Se hizo. **Devolvió tres hechos que cambian el contrato**, y los tres se escriben aquí antes de cualquier número.

### 0.1 · `P5_6_k` **no mide lo mismo** en ENIF 2021 y en ENIF 2024 — y el equivalente de 2021 es `P5_7_k`

Leído del diccionario de datos de cada payload del manifiesto (`enif2021_csv` → `conjunto_de_datos_tmodulo_enif_2021/diccionario_de_datos/diccionario_datos_tmodulo_enif_2021.csv`; `enif2024_csv` → `conjunto_de_datos_tmodulo_enif_2024/diccionario_de_datos/diccionario_datos_tmodulo_enif2024.csv`), **verbatim**:

| variable | ola | texto del reactivo, verbatim del FD |
|---|---|---|
| `P5_6_1` | **2021** | «¿Con su cuenta o tarjeta de nómina (donde depositan su sueldo) **tiene tarjeta de débito** (tarjeta de plástico con la que puede retirar dinero)?» |
| `P5_7_1` | **2021** | «De julio de 2020 a la fecha, ¿usted **guardó o ahorró** en su cuenta o tarjeta de nómina (donde depositan su sueldo)?» |
| `p5_6_1` | **2024** | «De junio de 2023 a la fecha, ¿usted **guardó o ahorró** en su cuenta o tarjeta de nómina (donde depositan su sueldo)?» |

La correspondencia es **de texto, no de rótulo**: el reactivo de 2024 `p5_6_k` es, palabra por palabra salvo la fecha de referencia, el reactivo de 2021 `P5_7_k`. El `P5_6_k` de 2021 es **otra pregunta** — tenencia de tarjeta de débito asociada a la cuenta, condicionada a tener la cuenta (`P5_4_k`).

**Consecuencia inmediata.** El desenlace que el diseño v1.1 §1 declara «idéntico en las dos olas» **no lo es si se lee por rótulo**: leído así, en 2021 mediría *posesión de plástico* y en 2024 *conducta de ahorro*. Eso no es una diferencia de grano: son dos eventos distintos bajo la misma escala — la fila 12 de la tabla fundida del careo (`forense/hallazgos.md:842`), otra vez.

**Corrección que este pre-registro aplica, y su alcance exacto.** Mesa firmó (D2(a) de la hoja del 16/sep) un **conjunto de siete tipos de cuenta** — `{nómina, pensión, apoyos de gobierno, ahorro, cheques, cuenta contratada por Internet/app, otro}`, los índices `{1,2,3,4,5,8,9}`. Ese conjunto se conserva **intacto**. Lo único que se corrige es **qué variable lo transporta en cada ola**, que es un hecho del archivo y no una decisión:

* **2021:** `P5_7_{1,2,3,4,5,8,9}`
* **2024:** `p5_6_{1,2,3,4,5,8,9}`

Precedente de la casa para exactamente esta clase de corrección: «el diseño cambia de nombre, no de existencia — vínculo por ola, no se edita la guardia».

### 0.2 · Los **nueve** códigos SÍ existen en 2021 — la razón por la que el correctivo rechazó la vía (b) es falsa

El careo (hallazgo 2, atribuido a Opus §1.6) y el correctivo §7 **D1(b)** rechazan redefinir el desenlace sobre los nueve códigos porque «`P5_6_6` y `P5_6_7` no existen en 2021». Es cierto de `P5_6_*` y **falso del constructo**: `conjunto_de_datos_tmodulo_enif_2021.csv` trae **`P5_7_1 … P5_7_9`, los nueve**, incluidos

* `P5_7_6` — «De julio de 2020 a la fecha, ¿usted guardó o ahorró en su **depósito a plazo fijo** (sólo puede retirar en determinadas fechas)?»
* `P5_7_7` — «De julio de 2020 a la fecha, ¿usted guardó o ahorró en su **fondo de inversión** (tener acciones en casa de bolsa)?»

**Este pre-registro NO adopta la vía (b).** Redefinir el desenlace del piloto a nueve códigos es exactamente lo que mesa decidió en otro sentido (D2(a), D5), y un ejecutor no revoca una firma con un hallazgo. Lo que sí hace, porque es barato, reversible y **declarado antes del dato**, es emitir el desenlace de **nueve** tipos como **objeto secundario y paralelo** (`D9`, §2.2) junto al primario de siete (`D7`), en las dos olas y también en el árbitro. Con eso, `D5` deja de ser una decisión a ciegas: mesa verá la magnitud exacta de la brecha `D7 ↔ D9` en las mismas 8 celdas, medida, en vez de decidir sobre un supuesto. `NC-0283`. *(Nota `v1.1`: `FP-379` resolvió `D1` por la vía (a) — marginales de siete códigos derivados —, así que `D9` ya no es el desenlace de `C2`; queda como diagnóstico de brecha y como base del control de reproducción del árbitro, §0.8.)*

### 0.3 · `FAC_PER` **no existe** en ENIF 2021 — el ponderador de esa ola es `FAC_ELE`

El encargo y el diseño v1.1 §1 declaran `FAC_PER` como ponderador de las dos olas. Verificado contra los tres inventarios canónicos vigentes y contra el FD:

| ola | archivo | ponderador presente | texto del FD |
|---|---|---|---|
| 2021 | `conjunto_de_datos_tmodulo_enif_2021.csv` | **`FAC_ELE`** (no hay `FAC_PER`) | «Factor de expansión», `5,C,fac_ele,,00000...99999` |
| 2024 | `conjunto_de_datos_tmodulo_enif2024.csv` | **`fac_per`** | «Factor de expansión a nivel persona», `6,C,fac_per,,126...106896` |

`FAC_PER` no aparece en **ningún** archivo de `enif2021_csv` (los ponderadores de esa ola son `FAC_ELE` en `TMODULO`, `FAC_HOG` en `THOGAR`/`TSDEM`, `FAC_VIV` en `TVIVIENDA`). `FAC_ELE` es el factor de la **persona elegida**, que es exactamente la unidad del universo. Se declara y se usa `FAC_ELE` en 2021. Es corrección de archivo, no de diseño.

### 0.4 · La variable de edad también cambia de nombre entre olas

2021: `EDAD` («Pregunta EDAD ¿Cuántos años cumplidos tiene (NOMBRE)?», rango `00...99`). 2024: `EDAD_V` («Edad verificada de la persona elegida», rango `18...98`). Catálogos leídos del zip, verbatim:

* `enif2021_csv :: conjunto_de_datos_tmodulo_enif_2021/catalogos/edad.csv` → `0 = Menos de un año`, `01...96 = Años cumplidos`, `97 = 97 años y más`, **`98 = Edad no especificada en personas de 18 años y más`**, **`99 = Otra edad no especificada`**.
* `enif2024_csv :: conjunto_de_datos_tmodulo_enif_2024/catalogos/edad_v.csv` → `18...95 = Años cumplidos`, `97 = 97 años y más`, **`98 = Edad no especificada en personas de 18 años y más`**.

`98` y `99` **no son edades**: quedan fuera del universo con la razón escrita (§3.1), y la cobertura resultante se reporta como `RESULT`.

### 0.5 · `TLOC` es idéntica en las dos olas, y el corte de 15 000 es exacto

`catalogos/tloc.csv` de cada ola, verbatim, cuatro claves en las dos:

| `cve` | 2021 | 2024 |
|---|---|---|
| `1` | 100 000 y más habitantes | 100 000 y más habitantes |
| `2` | 15 000 a 99 999 habitantes | 15 000 a 99 999 habitantes |
| `3` | 2 500 a 14 999 habitantes | 2 500 a 14 999 habitantes |
| `4` | Menor de 2 500 habitantes | Menor a 2 500 habitantes |

El corte `≥ 15 000 = {1,2}` / `< 15 000 = {3,4}` cae **en la frontera de una clase del catálogo**: no hay recodificación aproximada. (Diferencia de redacción «Menor de» / «Menor a» en `cve = 4`: cosmética, mismo umbral.) `localidad` conserva su corte del modelo `MAPEO-N-A-1` bajo `FP-376` FIRMADA; el marcador no consume esta celda por eso, y el piloto corre igual.

### 0.6b · `EST_DIS` / `UPM_DIS` existen en las dos olas, con rango distinto

`EST_DIS` 2021 `001...235` / 2024 `001...190`; `UPM_DIS` 2021 `0000001...0002013` / 2024 `00001...02172`. Son **llaves opacas**: no se interpretan, se usan como estrato y conglomerado del re-muestreo. El diseño no cambia de existencia entre olas, sólo de rango.

### 0.7 · `FP-379` — qué enmienda, dónde alcanzó al árbol, y qué NO cambia

**Firma de mesa, 16/sep/2026, verbatim:**

> «**D1:** los marginales de `C2` se derivan con los siete códigos comunes en `COMMIT-2` (opción **a**); se declara que `C2` deja de ser "lo que todos ya vieron" y pasa a ser "marginales 2024 sin interacción". **D2:** `C2` toma la forma log-aditiva `expit(logit p_l + logit p_e − logit p)`, rango `(0,1)` por construcción, rechazo explícito si algún marginal es `0` o `1`, sin recorte silencioso; se rotula "ausencia de interacción en escala logit", no "independencia". **D3:** la incertidumbre de `C2` se propaga réplica por réplica con el mismo bootstrap de los marginales, sin covarianzas inventadas y sin derivar el cruce. La admisión de `C2` (`D6` de v1.1 §7) queda condicionada a estas tres. **Repliegue** si (a) no es construible: `C2` pasa a diagnóstico y el piloto pregunta sólo si alguien vence a la persistencia.»

**Dónde alcanzó al árbol, para que sea auditable que no hubo mezcla.** `FP-379` llegó con `COMMIT-1` ya cerrado (`3461c46`: `v1.0` + sidecar + `spec.md` + `spec.yaml`), con `medidor.py` **sin escribir**, con **cero `RESULT` producidos** y con `C2` **sin una sola línea de código**. La forma multiplicativa **nunca se implementó**; no hubo nada que recalcular. Lo único vivo en ese momento eran las capturas de `C3` (`L-solo`), que `FP-379` no toca.

**Lo que cambia:**

| | `v1.0` (bajo `FP-378`) | **`v1.1` (bajo `FP-379`)** |
|---|---|---|
| insumos de `C2` | los marginales **sellados** de `tramite-ola5-propuesta-v0.yaml`, **citados** | los marginales de ENIF 2024 **derivados en `COMMIT-2`** con la misma receta que `R` |
| desenlace de `C2` | `D9` (nueve códigos, el del marginal público) | **`D7`** (los siete comunes) — **`H1` se disuelve**: `C2`, `C1` y `R7` miden el mismo evento |
| forma | log-aditiva (ya en `v1.0` por `D2` del correctivo) | log-aditiva, **confirmada por firma** |
| incertidumbre | `NO-ACREDITADA`, punto sin banda | **IC95 por bootstrap réplica-por-réplica**, marginales compartidos |
| dieta de `C2` | «lo que todos ya vieron» | **«marginales 2024 sin interacción»** — se declara el cambio |

**Lo que NO cambia:** la reserva (el **cruce** `p(Y│l,e)` de 2024 **no se deriva** en `COMMIT-2`; los marginales no son el cruce — correctivo §1(a) verbatim: *«No toca la reserva: la reserva es el cruce `p(Y│l,e)`, no los marginales»*); el desenlace primario `D7` de `R` y `C1`; el orden de los tres commits; `C1`, `C4`, `C5`; el criterio de adjudicación; la parada.

**Consecuencia sobre la prohibición del encargo.** El encargo escribía: «Prohibido en este commit: cualquier lectura de ENIF 2024 que no sea `FAC_PER`/diseño». `FP-379 D1` la **enmienda por firma posterior**: `COMMIT-2` abre ENIF 2024 **exclusivamente para marginales de un solo eje** (`localidad`, `edad`, nacional). **Guardia mecánica, no promesa:** el medidor de `COMMIT-2` no construye en ningún punto una llave `(localidad, edad)` sobre 2024; emite `RESULT-DIN-LXE8-G-C2-CRUCE-2024-DERIVADO = "NO"` y `RESULT-DIN-LXE8-G-R-EXISTE-AL-CERRAR = "NO"`, y ningún `RESULT` de este CALC lleva un valor de celda de cruce de 2024. Si alguna de las dos saliera distinta de `"NO"`, el falsador del §7 se dispara y el piloto degrada a factibilidad.

**Rótulo obligatorio.** En la spec, en el contrato y en las emisiones, `C2` se rotula **«ausencia de interacción en escala logit»**. **Nunca «independencia» a secas** (`D2` lo prohíbe): la independencia de `localidad` y `edad` como variables **no identifica** `P(Y│localidad, edad)`.

### 0.8 · Control de reproducción del árbitro marginal, declarado antes de correr

Derivar los marginales de 2024 abre, gratis, un control que `v1.0` no podía hacer: los mismos marginales bajo **`D9`** (nueve códigos) deben **reproducir** los que el árbitro selló. Se emite con las dos ramas escritas **antes** del dato:

* **REPRODUCE** si `|Δ| ≤ 1e-6` en las seis celdas marginales (`edad` ×4, `localidad` ×2) — entonces la cadena completa (payload, filtros, ponderador, dicotomización, agregación) queda validada extremo a extremo contra una cifra GEN1 sellada, y de paso queda probado que `enif2024_csv` y `enif_2024_enif_2024_bd_csv` son el mismo microdato (§2.1).
* **NO-REPRODUCE** en otro caso — se reporta el `Δ` con signo por celda **y no se ajusta nada** para que coincida. Un `NO-REPRODUCE` aquí **no invalida el piloto**: invalida la afirmación de que este medidor reproduce la receta del árbitro, que es un hecho aparte y se declara como tal.

---

## 1 · Estimando, población, unidad

**Estimando.** `p(ahorra_solo_informal │ localidad, edad)` — **proporción ponderada en `[0,1]`** de personas elegidas de 18 años y más que, en la ventana de referencia de su ola, **ahorraron por alguna vía informal y por ninguna vía formal** del conjunto declarado.

**Unidad de observación y de análisis:** **persona elegida** (`TMODULO`, una fila por persona seleccionada). No hay colapso de menciones: cada persona entra una vez, con su factor.

**Población objetivo:** las **8 celdas de cruce**

```
localidad ∈ { L1 = "<15 000"  (TLOC ∈ {3,4}),
              L2 = ">=15 000" (TLOC ∈ {1,2}) }
   ×
edad      ∈ { E1 = 18-29, E2 = 30-44, E3 = 45-59, E4 = 60+ }
```

Los ocho rótulos, fijos y en este orden: `L1xE1 · L1xE2 · L1xE3 · L1xE4 · L2xE1 · L2xE2 · L2xE3 · L2xE4`.

**Tramos de edad:** los del árbitro marginal (`milpa/tramite-ola5-propuesta-v0.yaml:1437-1444`), sin corte del modelo. `E4 = 60+` incluye `97` («97 años y más»).

**Ventanas de referencia, distintas por ola y declaradas:** 2021 = «de julio de 2020 a la fecha»; 2024 = «en los últimos 12 meses, de junio de 2023 a la fecha» (`P5_1_*`) y «de junio de 2023 a la fecha» (`p5_6_*`). La ventana de 2021 es **más larga y no anclada a 12 meses**. Es un supuesto de transporte de `C1`, no una equivalencia: se declara aquí y viaja con la cifra.

---

## 2 · Variables y códigos, por archivo y por ola (A.15b/c)

Todo lo de esta sección se leyó de FD, diccionario de datos y catálogos. **Cero microdato.**

### 2.1 · Archivos

| rol | ola | payload (manifiesto) | miembro |
|---|---|---|---|
| microdato persona | 2021 | `enif2021_csv` (`data/raw/enif2021_csv.zip`, sha256 `0f314fa3…5cd9`) | `conjunto_de_datos_tmodulo_enif_2021/conjunto_de_datos/conjunto_de_datos_tmodulo_enif_2021.csv` |
| FD / estructura | 2021 | `enif2021_fd_zip` (`data/raw/enif_2021_fd_pdf.zip`, sha256 `6f4e3aab…9457`) | `enif_2021_estructura_del_archivo.{xlsx,pdf}` |
| microdato persona | 2024 | `enif2024_csv` (`data/raw/enif2024_csv.zip`, sha256 `a3507b40…2e4c`) | `conjunto_de_datos_tmodulo_enif_2024/conjunto_de_datos/conjunto_de_datos_tmodulo_enif2024.csv` |
| FD / estructura | 2024 | `enif2024_fd_xlsx` (`data/raw/enif_2024_fd.xlsx`, sha256 `17e2ad86…5db2`) | — |

**Nota de identidad de payload, declarada y no escondida.** El árbitro marginal sellado (`tramite-ola5-propuesta-v0.yaml`) declara `sha256_payload = 00e4b0b4…f039`, que es el payload `enif_2024_enif_2024_bd_csv` (miembro `TMODULO.csv`), **no** `enif2024_csv` (`a3507b40…`). Son dos empaquetados del **mismo microdato** de INEGI: los inventarios canónicos registran para los dos **398 variables** en el módulo, con la misma nomenclatura salvo la caja de las letras (`FAC_PER`/`fac_per`). Este pre-registro usa los **cuatro payloads que el encargo nombra**, y declara el hecho para que un `verify` que compare hashes de input contra el asiento del árbitro no lo lea como divergencia oculta. Reconciliación por columnas, no por nombre de archivo.

### 2.2 · Los dos desenlaces

**`D7` — PRIMARIO, el que mesa firmó (siete tipos de cuenta).**

```
informal   := alguna de P5_1_1 … P5_1_6 == "1"
formal_7   := alguna de los SIETE tipos {1,2,3,4,5,8,9} con "guardó o ahorró" == "1"
D7         := informal  AND  NOT formal_7
```

**`D9` — SECUNDARIO, declarado en §0.2 (los nueve tipos).**

```
formal_9   := alguna de los NUEVE tipos {1,…,9} con "guardó o ahorró" == "1"
D9         := informal  AND  NOT formal_9
```

`D9` es el desenlace **conmensurable con el marginal público del árbitro** (`tramite-ola5-propuesta-v0.yaml:1426`, definición verbatim «alguna P5_1_1..P5_1_6 == '1' Y ninguna P5_6_1..P5_6_9 == '1'»).

**Relación entre los dos, y su falsador.** `formal_7 ⊆ formal_9` (siete tipos contra nueve), luego `¬formal_9 ⊆ ¬formal_7`, luego **`D9 ⊆ D7`** y **`p̂(D7) ≥ p̂(D9)` en toda celda y en toda ola**. Concretamente: quien ahorró por vía informal y cuya única vía formal fue plazo fijo (`6`) o fondo de inversión (`7`) cuenta `D7 = 1` («no usó ninguno de los siete») y `D9 = 0` («sí usó una vía formal»). **Esta desigualdad es un falsador del propio medidor**: si alguna celda la viola, el medidor está mal y la corrida se declara `NO-CONSTRUIBLE` — no se reporta el número.

**Tabla de variables, por ola y por archivo.** Presencia verificada contra los tres inventarios canónicos **vigentes** (`inventario-reactivos-v1_2.tsv`, `inventario-reactivos-descargas-mx-v1_2.tsv`, `inventario-reactivos-ext-v1_0.tsv`); nunca `v1_0`/`v1_1`.

| rol | 2021 (`conjunto_de_datos_tmodulo_enif_2021.csv`) | 2024 (`conjunto_de_datos_tmodulo_enif2024.csv`) |
|---|---|---|
| ahorro informal (6) | `P5_1_1 … P5_1_6` | `p5_1_1 … p5_1_6` |
| vía formal, siete (`D7`) | `P5_7_1 P5_7_2 P5_7_3 P5_7_4 P5_7_5 P5_7_8 P5_7_9` | `p5_6_1 p5_6_2 p5_6_3 p5_6_4 p5_6_5 p5_6_8 p5_6_9` |
| vía formal, los dos extra (`D9`) | `P5_7_6 P5_7_7` | `p5_6_6 p5_6_7` |
| localidad | `TLOC` | `tloc` |
| edad | `EDAD` | `edad_v` |
| ponderador | **`FAC_ELE`** | `fac_per` |
| estrato de diseño | `EST_DIS` | `est_dis` |
| UPM de diseño | `UPM_DIS` | `upm_dis` |

**Códigos de respuesta**, idénticos en las dos olas para `P5_1_*` y para la familia «guardó o ahorró»: dominio declarado `"1,2"` en el FD — `1 = Sí`, `2 = No`. **No hay código de no-respuesta declarado en el dominio.** Regla congelada: un valor distinto de `"1"` (incluido vacío) **no** cuenta como Sí; y la fila que traiga algún valor fuera de `{"1","2",""}` en cualquiera de las 6 + 9 variables se cuenta y se reporta como `RESULT` (`…-G-FILAS-CODIGO-FUERA-DE-DOMINIO`), sin descartarla en silencio.

**Gate de cuestionario, declarado (no es un defecto, es la estructura).** `P5_4_k` («¿usted tiene…?») gatea a `P5_5_k`/`P5_6_k`/`P5_7_k`. Quien no tiene la cuenta `k` no responde la pregunta de ahorro en `k`, y entra al desenlace como «no usó esa vía formal» — que es lo que el árbitro sellado ya hace y lo que su propia nota declara (`eje: cuenta_formal`, «`P5_4_*` gatea a `P5_6_*`, así que sin cuenta el desenlace se reduce a `informal_cualquiera` por construcción del cuestionario»). **Se hereda tal cual, no se corrige**: cambiarlo produciría otro estimando y rompería la comparación con el árbitro.

---

## 3 · Universo, filtros, ponderador, diseño

### 3.1 · Universo

Personas **elegidas de 18 años y más** del módulo (`TMODULO`), una fila por persona. Filtro, en este orden y sin ninguno más:

1. edad válida: `EDAD` (2021) / `edad_v` (2024) numérica, **`18 ≤ edad ≤ 97`**. Excluye `98` y `99`, que el catálogo declara «no especificada». 2021 además excluye `< 18` si apareciera (el catálogo de `edad.csv` admite `0…17`, aunque el universo del módulo es 18+; el filtro es explícito y no se supone).
2. `TLOC` ∈ `{1,2,3,4}`.
3. ponderador presente y `> 0`.

**Nada más.** No se filtra por tenencia de cuenta, ni por respuesta a `P5_1_*`: quien no ahorró de ninguna forma es un `0` legítimo del desenlace.

**Cobertura** = (filas del universo tras el filtro) / (filas del archivo), ponderada y sin ponderar, reportada como `RESULT` en cada ola. El diseño v1.1 cita cobertura `0.998889` para el eje `edad` del árbitro: si la cobertura medida aquí en 2024 se aparta de esa cifra en más de `0.002` absolutos, se reporta el hecho — **no se ajusta el filtro para hacerla coincidir**.

### 3.2 · Ponderador

2021 `FAC_ELE`; 2024 `fac_per` (§0.3). Todas las proporciones son **razones de totales ponderados**:

```
p̂(celda) = Σ_{i ∈ celda} w_i · y_i  /  Σ_{i ∈ celda} w_i
```

### 3.3 · Diseño muestral e intervalo

**Bootstrap de conglomerados estratificado**, misma receta que el árbitro marginal declara (`tramite-ola5-propuesta-v0.yaml:1420-1423`: `ponderador: FAC_PER`, `estrato: EST_DIS`, `upm: UPM_DIS`, `estimador: "bootstrap conglomerado estratificado, 10 000 réplicas, seed 42"`): re-muestreo **con reemplazo de `UPM_DIS` dentro de cada `EST_DIS`**, `n_h` UPM por estrato, **10 000 réplicas**, **seed 42**.

* RNG declarado: `numpy.random.Generator(numpy.random.PCG64(42))`. Un solo generador, consumido en orden determinista (estratos ordenados lexicográficamente por `EST_DIS`, UPM ordenadas lexicográficamente por `UPM_DIS`, réplicas `0…9999`, y dentro de cada réplica todas las celdas del mismo re-muestreo).
* **Las 8 celdas de una ola comparten las mismas 10 000 réplicas** — es el mismo re-muestreo de la misma muestra. Esto es deliberado (`H3` del correctivo, mecanismo mínimo de `RONDA1:66`): permite propagar réplica por réplica sin inventar covarianzas.
* **IC95** = percentiles `2.5` y `97.5` del vector de 10 000 réplicas (`numpy.percentile`, interpolación lineal, el default).
* `EE(R)` = `(IC95_sup − IC95_inf) / 3.92` — la definición que el criterio de adjudicación usa (diseño v1.1 §3).
* Estrato con **una sola UPM** en la celda: el re-muestreo de ese estrato es degenerado y aporta varianza cero. Se **cuenta y se reporta** (`…-G-ESTRATOS-UPM-UNICA`) y el IC se lee como **conservador**, no como exacto — mismo tratamiento que `ENCIG-MORDIDA-spec-v1_0.md` §3.7 ratificó como estándar de familia (`NC-0112`, `D3` de mesa 9/sep/2026). No se colapsan estratos, no se descartan.

### 3.4 · Soporte, umbral y salida predefinida (H4)

**El umbral y la salida se fijan aquí, antes de ver un solo `n`.**

* **Umbral:** `n_2021(celda) ≥ 200` filas del universo. (`n` sin ponderar, que es lo que el umbral gobierna.)
* **Cota de Fréchet–Hoeffding sobre los márgenes ya sellados** (`:1437-1470`), que es lo único que los márgenes acreditan: con `N = 13 487`, las **ocho cotas inferiores son `0`** — los márgenes publicados son compatibles con una celda vacía. Por tanto **`n` queda `DESCONOCIDO` hasta que `C1` lo calcule**, y este pre-registro **no** afirma que ninguna celda esté bajo el umbral.
* **Salida predefinida si `n_2021(celda) < 200`:** la celda se rotula `FUERA-DE-SOPORTE`; **se emite igual** su punto y su IC, marcados; **no puntúa** en la adjudicación; y cuenta para la parada `FUERA-DE-SOPORTE` del correctivo §5 si ocurre en **≥ 3 de las 8**.
* Si una celda tiene `n = 0`: punto y IC `NO-ESTIMABLE` (`null`, con `permite_no_estimable: true` en el contrato), nunca `0.0`.
* El soporte de **2024** lo informa `COMMIT-3` junto con `R`, con el mismo umbral; una celda `FUERA-DE-SOPORTE` en 2024 no puntúa aunque lo esté en 2021.

**Los umbrales, las celdas y los candidatos no se tocan después de ver el `n`.**

---

## 4 · Los cinco candidatos, su dieta y su incertidumbre

### 4.1 · `C1` — `BASELINE_INGENUO`, persistencia ENIF 2021

Mismo desenlace (`D7`, y `D9` en paralelo), mismo cruce, mismo estimador, ola **2021**. `estrategia: transversal_con_seleccion`; `regla_composicion:` **identidad temporal `p_2021 → p_2024`**, declarada el 2026-09-17.

*Hueco de vocabulario declarado, no rellenado con un valor inventado:* «persistencia» no está en el enum `estrategia` de `vocabulario v0.3 §3`. Se registra como falsador del vocabulario (`NC-0284`), no como categoría nueva.

**Incertidumbre:** IC muestral propio, bootstrap §3.3 sobre la muestra de 2021. **El IC de `C1` no incluye** el error de la extrapolación temporal 2021→2024, que es un supuesto sin varianza estimable aquí: se dice, no se ensancha el intervalo a ojo.

**Dieta:** microdato ENIF 2021 completo. `C1` **no** ve nada de 2024.

### 4.2 · `C2` — `BASELINE_INGENUO`, piso marginal de ENIF 2024 · **bajo `FP-379`**

**Dieta, declarada y cambiada respecto de `v1.0`:** `C2` ya **no** es «lo que todos ya vieron». Es **«marginales 2024 sin interacción»**: siete cantidades derivadas **dentro del piloto**, en `COMMIT-2`, con la misma receta que `R`, sobre el desenlace **`D7`** — los siete códigos comunes que mesa firmó. `FP-379 D1`, opción (a).

**Insumos, y sólo éstos — tres marginales de UN SOLO EJE cada uno, nunca el cruce:**

| marginal | definición | grupos |
|---|---|---|
| `p̂_l` | `p(D7 │ localidad)` en ENIF 2024 | `L1` (`tloc ∈ {3,4}`), `L2` (`tloc ∈ {1,2}`) |
| `p̂_e` | `p(D7 │ edad)` en ENIF 2024 | `E1`, `E2`, `E3`, `E4` |
| `p̂` | `p(D7)` nacional en ENIF 2024 | — |

Receta idéntica a la de `R` y a la del árbitro marginal: universo §3.1, ponderador `fac_per`, diseño `est_dis`/`upm_dis`, bootstrap §3.3 (**10 000 réplicas, seed 42**).

**`C2` no abre el cruce, y hay guardia mecánica.** Ninguna de las tres cantidades cruza los dos ejes. El medidor de `COMMIT-2` **no construye la llave `(localidad, edad)` sobre 2024** en ningún punto, y lo declara en dos `RESULT` de texto (`…-G-C2-CRUCE-2024-DERIVADO`, `…-G-R-EXISTE-AL-CERRAR`, ambos `"NO"`). Correctivo §1(a), verbatim: *«No toca la reserva: la reserva es el cruce `p(Y│l,e)`, no los marginales.»*

**`H1` queda disuelto, y se dice.** Con `FP-379`, `C2`, `C1` y `R7` miden **el mismo evento** (`D7`). La objeción del correctivo §1 — «un error absoluto de `C2` contra `R` mezcla lo que la independencia no capta con lo que dos definiciones del desenlace separan» — **deja de aplicar**. `C2` es ahora puntuable contra `R7` sin reserva de constructo.

**Los marginales sellados de nueve códigos ya no alimentan `C2`.** Se conservan en este pre-registro **sólo** como referencia del control de reproducción de §0.8:

| marginal | valor | IC95 | `n` | línea verificada en este árbol |
|---|---|---|---|---|
| `edad 18-29` | `0.432063` | `[0.407039, 0.457410]` | `2924` | `:1447` |
| `edad 30-44` | `0.375709` | `[0.354484, 0.396905]` | `4256` | `:1448` |
| `edad 45-59` | `0.327505` | `[0.307291, 0.347765]` | `3411` | `:1449` |
| `edad 60+` | `0.277317` | `[0.254739, 0.300803]` | `2896` | `:1450` |
| `localidad <15 000` | `0.409255` | `[0.387307, 0.429960]` | `4646` | `:1472` |
| `localidad ≥15 000` | `0.329868` | `[0.315113, 0.344834]` | `8856` | `:1473` |
| **nacional** | `0.357153` | — (`sin IC propio`) | `13 502` | `tramite.yaml:1312` / `propuesta:1127` |

*Corrección de cita, declarada:* el encargo sitúa estos marginales en `:1437-1470`. En el árbol de este acto (`origin/main = 0189562`) están en **`:1447-1450`** (edad) y **`:1472-1473`** (localidad); el bloque `desenlaces.principal` empieza en `:1425` y su `definicion` en `:1426`. El rango del encargo apunta al mismo bloque con las líneas corridas; se cita por **contenido verificado**, no por el número heredado.

**Aritmética de coherencia, verificada antes de usar los insumos:** `2924 + 4256 + 3411 + 2896 = 13 487` (universo del eje `edad`, cobertura declarada `0.998889`), `4646 + 8856 = 13 502` (universo del eje `localidad`, cobertura `1.000000`), y `13 487 / 13 502 = 0.998889…`. Cierra. `N = 13 487` es el que entra en las cotas de Fréchet de §3.4.

**Estas siete cifras NO entran en `C2`.** Bajo `FP-379` alimentan únicamente el **control de reproducción** de §0.8, y su definición de nueve códigos es la razón por la que ese control se corre sobre `D9` y no sobre `D7`.

**Forma, `FP-379 D2` (y `D2` del correctivo) — log-aditiva, declarada como modelo distinto:**

```
logit(x) = ln(x/(1−x))      expit(z) = 1/(1+e^(−z))
p̂(l,e)  = expit( logit(p̂_l) + logit(p̂_e) − logit(p̂) )
```

*Rechazo explícito*, nunca recorte: si `p̂`, `p̂_l` o `p̂_e` ∈ `{0,1}` — **en el punto o en cualquiera de las 10 000 réplicas** — el logit diverge → esa evaluación es `SIN-DEFINIR`. Si el **punto** de una celda es `SIN-DEFINIR`, la celda se declara **`NO-CONSTRUIBLE` con la razón escrita**, `null` en el `RESULT` (`permite_no_estimable: true`), y **no se fuerza un valor**. Contrato pinado con fixtures sintéticos en `tests/test_celda_d_c2.py` (`piso_log_aditivo`, `DesenlaceIncompatible`, `MarginalDegenerado`); **el medidor de `C2` importa esa función de referencia y no reimplementa la fórmula**, para que el contrato y el ejecutable no puedan divergir. Como los tres marginales entran ahora con el **mismo** `desenlace_id` (`D7`), la guardia `DesenlaceIncompatible` de esa función queda satisfecha por construcción — y sigue armada.

*Qué supone, dicho, con el rótulo que `FP-379 D2` impone:* **ausencia de interacción en la escala logit**. **Nunca «independencia» a secas** — la independencia de `localidad` y `edad` como variables **no identifica** `P(Y│l,e)`, ni con esta forma ni con la anterior. Es un piso: una construcción declarada, reproducible y sólo-marginal, que un challenger debe vencer para poder decir que la interacción aporta algo explotable.

**Diagnóstico de rango, agregado y no por celda.** La forma multiplicativa de v1.1 §9 (`p̂_l·p̂_e/p̂`) se evalúa sobre **los mismos marginales derivados** y se emite como **dos escalares**: cuántas de las 8 celdas caen fuera de `[0,1]` (`…-G-C2-MULT-FUERA-DE-RANGO`) y el valor máximo alcanzado (`…-G-C2-MULT-MAX`). **No hay un `RESULT` multiplicativo por celda**: `FP-379` ordena no mezclar las dos formas en el mismo CALC, y un escalar de control no es un candidato. Existe sólo para que la razón del cambio de forma quede auditable sin recalcularla.

**Incertidumbre de `C2`: IC95 por bootstrap réplica-por-réplica (`FP-379 D3`).** Los tres marginales salen de la **misma muestra** y del **mismo re-muestreo**: la réplica `r` produce `p̂_l^(r)`, `p̂_e^(r)` y `p̂^(r)` **a la vez**, y se empujan juntas por la fórmula log-aditiva. El IC95 son los percentiles `2.5`/`97.5` del vector de 10 000 valores resultante. **Sin delta, sin supuesto de independencia entre estimadores, sin covarianzas inventadas** — y **sin exponer `R`**, porque las réplicas son de los marginales, no del cruce. Es el mecanismo mínimo de `RONDA1:66`, aplicado.

*Enmienda declarada:* el encargo de este acto escribía «IC propagado por **delta** desde los marginales». `FP-379 D3` lo sustituye por réplicas compartidas. La vía (c) del correctivo (`incertidumbre: NO-ACREDITADA`, punto sin banda), que la `v1.0` de esta spec había adoptado, **queda superada por firma** y no se ejecuta.

**Repliegue declarado (`FP-379`).** Si la construcción no es viable —porque algún marginal sale exactamente `0` o `1`, o porque los marginales de los siete códigos comunes no resultan derivables— **`C2` pasa a `DIAGNÓSTICO`**, deja de ser piso admisible del piloto, y la pregunta de fondo pasa a ser **«¿algo vence a la persistencia (`C1`)?»** en vez de la comparación contra dos pisos. Se declara en la nota de cierre; el piloto **sigue siendo válido**.

### 4.3 · `C3` — `CHALLENGER`, elicitación de `L`, dos dietas

Protocolo **ADV1** (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B) y **`PAQUETE-L-v1_1.md` §2**, invariantes sin re-declarar con otro valor: cliente `claude -p` (Claude Code CLI, modo print), `modelo_id` alias `opus`, `--tools ""`, prompt de sistema reemplazado por la cadena mínima sellada, **`k = 8` corridas por (celda, variante)**, orden de captura contrabalanceado con `SEMILLA_ORDEN = 42`, hasta `2` reintentos por captura, **cero descarte** (toda corrida se registra, incluidas las de rechazo). Prompt construido **mecánicamente** por `construir_prompt()` de `pipeline-L-adv1-m2.py`, nunca a mano por celda. Extracción de `valor_extraido` por la regla **congelada** `tools/extrae_l_v1_1.py::extraer_valor` (`regla-extraccion-L-v1_1.md`), sin tocar el script.

**Dietas:**

* **`L-solo`** — memoria del modelo. `corpus_id_si_aplica = None` (el `__post_init__` de `ParametrosCorredorL` lo exige: «`L-solo` no debe traer corpus adjunto — rompería el ciego»). Los marginales públicos **no** se le entregan en esta variante.
* **`L+corpus`** — idem + corpus documental F5 **sin ENIF 2024**, ensamblado desde `paquete-corpus-F5-v1_0/manifiesto.json` con el corte temporal de la celda.

**Escala declarada al modelo:** `proporción en [0,1]` más **intervalo subjetivo al 80 %**, pedido por el campo `escala` de la `SpecCelda` (parámetro de la plantilla congelada, no una edición de la plantilla). El nivel `80 %` viene del diseño v1.1 §4; la plantilla sellada sólo pide «un intervalo de confianza subjetivo», así que el nivel viaja por el único canal que no toca bytes sellados.

**Extracción, y lo que NO se extrae — declarado antes de mirar una sola captura.** `valor_extraido` sale de la regla **congelada** `tools/extrae_l_v1_1.py::extraer_valor`, que devuelve **un punto** por captura. **El intervalo al 80 % que se le pide a `L` NO se extrae en este CALC**: la regla congelada no lo contempla, y escribir una segunda regla de extracción *después* de leer las 64 capturas sería una regla post-hoc sobre datos ya vistos. El intervalo queda **en el texto crudo** de cada captura, íntegro, para un sucesor que pre-registre su regla. Fila `NC-0286`.

**Lo que sí se emite por celda, con las `k = 8` puntos extraídos:** la **mediana** (punto de `C3`), el **mínimo** y el **máximo** — la dispersión entre corridas, que es *un resultado y no un problema a limpiar* (ADV1-M2). Más `k_extraibles`, el conteo de capturas de las que la regla congelada pudo sacar un número. Una celda con `k_extraibles = 0` es `NO-ESTIMABLE` (`null`), nunca `0.0`.

**Incertidumbre:** dispersión entre las `k = 8` corridas (mín–máx). **No es un IC muestral y no se presenta como tal.** La cobertura empírica del intervalo declarado por `L` contra `R` queda **sin medir en este acto**, por la razón de arriba; el diseño v1.1 §4 la promete y aquí se declara no cumplida (`NC-0286`), en vez de producirla con una regla improvisada.

**Control de memoria (H6, y su alcance exacto).** Se buscó, **antes de elicitar**, si INEGI publicó el cruce `tamaño de localidad × grupo de edad` para este desenlace de ENIF 2024:

* en el árbol: `git grep -icE "localidad ?[x×] ?edad"` sobre los archivos rastreados → las coincidencias son **de este piloto y del careo**, ninguna es un tabulado; el control positivo (`git grep -cE "eje: localidad" -- milpa/`) devuelve `2` archivos, así que el patrón sí acierta cuando hay algo.
* fuera del árbol: búsqueda web dirigida sobre los productos de ENIF 2024 (comunicado `ENIF2024_CP.pdf`, `ENIF2024_RR.pdf`, reporte CNBV, portal del programa). **La publicación oficial desagrega por tamaño de localidad y por sexo, a nivel nacional; no aparece el cruce `localidad × edad` para este desenlace.**

**Veredicto congelado:** `CONTROL-MEMORIA = NO-PUBLICADO-EN-LO-ALCANZADO`. Si un sucesor encontrara el tabulado, las celdas de `C3` pasan a `CONTROL-MEMORIA` y **el piloto sigue válido para `C1`/`C2`** — así queda escrito antes de correr. **Lo que esto acredita, y sólo esto:** que el cruce no está en el árbol ni en los productos que la búsqueda alcanzó. **No** acredita que ningún modelo lo haya visto nunca. La reserva es **operacional**.

### 4.4 · `C4` — `CHALLENGER`, matriz `B·θ(x) → h_r` · `INEJECUTABLE`

`estrategia: momentos`. **Cuatro faltantes, por nombre** (diseño v1.1 §2 C4):

1. `h_r` **inexistente** — `milpa/src/emisor.py:364`.
2. `G3.horizonte_temporal` bajo `GATE·ID-X` — `procedencia.yaml:1116`.
3. `G3.aversion_riesgo` `SIN-RUTA` — `procedencia.yaml:1172`.
4. `θ` de `G3.familismo_apoyo` **por celda de `localidad × edad` no medido** — sólo existe `β̂` marginal `0.0279` (`modelo-decision-v4_0.md:466`).

Bajo `ADR-531` compite si puede; no puede; **se escribe como resultado, no se omite**. `INEJECUTABLE` no es un `NO-REPRODUCE` piadoso ni un candidato que perdió.

### 4.5 · `C5` — `COMPLEMENTO`, emisor `M` (x = ∅) · `NO-APLICA`

Fuera de la competencia por el hallazgo 3 del careo: el emisor **es el árbitro con otro nombre** — `milpa/tramite.yaml:712` declara que la entrada de segmentación está «copiada verbatim» de `tramite-ola5-propuesta-v0.yaml:1162-1346`. Adjudicarlo sería puntuarse contra sí mismo.

**Se reporta sólo como diagnóstico:** `|p_nacional − p_celda|` por celda, con `p_nacional = 0.357153` (`tramite.yaml:1312`, `clase: DERIVADO … no es MEDIDO`) y `p_celda = R` de la celda. Se emite en `COMMIT-3` junto con `R`. **No entra en ninguna adjudicación** y no mueve ningún contador.

---

## 5 · Criterio de adjudicación — escrito antes del dato

**Por celda**, error absoluto en **puntos porcentuales** contra `R` del mismo desenlace. Bajo `FP-379`, **los tres candidatos ejecutables (`C1`, `C2`, `C3`) y el árbitro `R7` viven en `D7`**: la adjudicación primaria ocurre entera en el desenlace que mesa firmó. `D9` (`C1-D9` contra `R9`) se reporta **sólo como diagnóstico de la brecha `D7 ↔ D9`** (§0.2) y **no adjudica**.

**`INDECIDIBLE`, las dos condiciones verbatim** de `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38`:

> «**INDECIDIBLE** si ambos caen dentro del IC de `R` o si `|d_L−d_M| < 0.5·EE(R)`.»

Aquí los pares son **challenger contra cada piso**. `EE(R) = (IC95_sup − IC95_inf)/3.92`.

**Skill** contra cada piso: `1 − MAE/MAE(b)`. **Se reporta, no adjudica.**

**A nivel celda-D:** un challenger **gana** sólo si vence a **los dos pisos** en **≥ 6** celdas `PUNTUADA`, **y** las `PUNTUADA` son **≥ 6 de 8**. No hay valor-p: son 8 celdas de una misma muestra, no independientes; el umbral es de conteo. Familia declarada: 8 celdas × 2 challengers.

**Precedencia:** si dos filas se satisfacen, manda `INDECIDIBLE`.

**Paradas admisibles, todas terminales, ninguna con adopción forzada** (correctivo §5; el conjunto está pinado en `tests/test_celda_d_c2.py::PARADAS_ADMISIBLES`):

| salida | cuándo |
|---|---|
| `ADJUDICADA` | un challenger vence a los dos pisos bajo el conteo de arriba |
| `INDECIDIBLE` | se cumplen las condiciones verbatim, **o** hay `< 6` celdas `PUNTUADA` |
| `SIN-CANDIDATO-SUPERIOR` | todos ejecutaron y ninguno vence a los pisos |
| `FUERA-DE-SOPORTE` | el soporte de §3.4 no alcanza en `≥ 3` de las 8 |

**`B-bis`, declarado antes de correr.** Si nadie vence a `C1` → la **persistencia** queda corroborada como piso en `DIN`. Si nadie vence a `C2` → **los candidatos ensayados no superaron este piso, bajo esta evaluación, en estas ocho celdas** — y eso es **todo** lo que dice (`H5`). **No** identifica ausencia de interacción, ni ausencia de información aprovechable por otros métodos, ni una propiedad de la población.

**Límite que la propia evaluación se impone (`H5`, fila 7 de la tabla fundida).** Si el ganador se **elige** con las ocho celdas, esa misma evaluación **no lo valida de forma independiente**. El resultado se reporta como **selección más desempeño conjunto**, nunca como desempeño independiente del ganador.

---

## 6 · Tolerancias, determinismo, y qué cuenta como reproducción

| objeto | tipo | tolerancia |
|---|---|---|
| proporciones (`p̂`, IC, MAE, skill, deltas) | `proporcion` / `flotante` | `abs ≤ 1e-10` |
| conteos (`n`, numeradores, estratos, UPM, réplicas) | `entero` | **exacto**, sin epsilon |
| bootstrap | — | **exacto por semilla**: `seed = 42`, `numpy.random.PCG64`, orden de consumo fijado en §3.3. `tolerancia.exacto_por_seed: true` |
| rótulos, veredictos, sha256 | `texto` | exacto |

Dos corridas del mismo código sobre los mismos bytes de input **deben** dar los mismos 10 000 vectores de réplica. Si no los dan, es defecto del medidor, no ruido.

---

## 7 · Orden de los commits — el orden del diff es el sello

* **`COMMIT-1`** (este archivo + sidecar + `spec.yaml`): la spec congelada. **Cero microdato abierto.** Sólo FD, diccionarios, catálogos e inventarios.
* **`COMMIT-2`**: `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` — `C1`, `C2`, `C3` emitidos y sellados; `C4` `INEJECUTABLE`; `C5` `NO-APLICA`. **De ENIF 2024 se leen, y sólo, los marginales de un eje** (`localidad`, `edad`, nacional), bajo `FP-379 D1`; **el cruce `(localidad, edad)` de 2024 no se construye en ningún punto**, con guardia mecánica y `RESULT` de texto que lo declaran (§0.7). Al cerrar este commit, **`R` no existe en el árbol**.
* **`COMMIT-3`**: `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001` — `R` del cruce (`R7` y `R9`), adjudicación por celda, celda-D actualizada, fila del catálogo de momentos, test del consumidor, diagnóstico `C5`.

**Falsador del propio piloto, declarado antes de correr:** un `R` del cruce derivado **antes** de que `COMMIT-2` cierre — aquí o en cualquier otro acto — **degrada el piloto a factibilidad y se declara en la nota**. No lo anula.

---

## 8 · Lo que este pre-registro NO promete

* No promete cegamiento absoluto: la reserva es **operacional** (`H6`).
* No promete que el piso `C2` identifique `P(Y│l,e)`: es **ausencia de interacción en escala logit**, no independencia, y no estima la verdad (`FP-379 D2`).
* No promete que el IC de `C2` cubra el error de especificación del piso: cubre el **muestreo** de sus marginales, propagado réplica por réplica (`FP-379 D3`).
* No promete que `C2` siga siendo «lo que todos ya vieron»: bajo `FP-379 D1` su dieta cambió a **«marginales 2024 sin interacción»**, derivados dentro del piloto, y se declara.
* No promete soporte: `n` es `DESCONOCIDO` hasta que `C1` lo calcule, y las ocho cotas inferiores de Fréchet son `0` (`H4`).
* No promete un ganador: cuatro paradas son terminales y ninguna adopta (`H5`).
* No promete transporte temporal: la identidad `p_2021 → p_2024` es el supuesto que `C1` **es**, no un resultado.
* No adopta nada al motor, no mueve ningún `p`, no firma nada.

---

**Sello de congelación.** Este procedimiento queda fijado aquí, con su sidecar `sha256`, antes de abrir microdato: **el primer resultado que produzca este procedimiento es el que se reporta.**
