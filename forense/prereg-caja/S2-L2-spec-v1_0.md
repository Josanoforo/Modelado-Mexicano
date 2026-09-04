# S2 · Pre-registro de `MAESTRA38-L2` — rama MEDICIÓN y rama TEXTO, congeladas antes del `.dta`

### `prereg-caja-S2-L2` · **v1.0** · 4 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S2-L2-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S2-L2`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Dos ramas congeladas del futuro acto que abre el microdato de primera mano de ICPSR 35024 (`35024-0001-Data.dta`): **MEDICIÓN** (variables, ponderador, universo, dicotomizaciones, celdas para `R7.3`/`R7.6`/experimento de lista) y **TEXTO** (qué ítems, por su wording, sostienen o tumban cada lectura de `ACTO MAESTRA36-L12`). |
> | **QUÉ NO ES** | No abre el `.dta`. No abre el codebook/cuestionario (ambos registrados en manifiesto, físicamente ausentes de esta sesión NUBE). No mueve el tier de `R7.3`/`R7.6`. No decide cuál rama corre primero salvo lo que §3 fija. |
> | **VERIFICAS ASÍ** | Caja, al abrir el `.dta`/codebook, compara la variable de ponderación real contra §1.0; compara los números de ítem contra §1.1–§1.3; compara el wording real contra la tabla de §2. |

**Acto:** `ACTO MAESTRA38-N3 · PRE-REGISTRO-DE-CAJA`, 4/sep/2026, entorno **NUBE**, sobre `origin/main = 0ff3d7106793e7352df92bd658e3e25293a025db`.

---

## 0 · Ficha bajo prueba y continuidad de rótulo, declarada

**Definiciones vigentes** (`canon/modelo-decision-v4_0.md:761-762`):

> `R7.3` · L267 · *Transferencia sin proximidad/monitoreo → conserva autonomía del voto* · tier `[MEDIA]` (degradado desde `[FUERTE]`) · **sí tiene ficha hitoD** (`forense/hitoD-R7_3-*`, pero ese falsador es sobre RDD/Padrón del Bienestar — **no** sobre MPS-2012; ver §0.1)
> `R7.6` · L268 · *Proximidad/focalización o monitoreo percibido → autonomía cede localmente* · tier `[MEDIA]` · **no tiene ficha hitoD** — sólo aparece definida en `modelo-decision-v4_0.md:762` y operacionalizada en `tools/medidor_l12_mps2012.py:425` (`salida["_reglas"] = ["R7.3 (FUERTE)", "R7.6 (MEDIA)"]`) y en `necesidad-objeto-modelo.tsv` **no aparece en absoluto** (`grep -n "R7\.6"` → 0 filas).

**La autorización explícita para este acto** — `canon/modelo-decision-v4_0.md:781`, enmienda D2-f, verbatim:

> *`R7.3` pasa de `[FUERTE]` a `[MEDIA]` en el cálculo... `se_mueve_si` (verbatim, firma de mesa 3/sep/2026): "medición de primera mano en ICPSR 35024 .dta (D6) o un tercer instrumento CORROBORADA con IC fuera de 0 → vuelve a FUERTE; un tercero CONTRARIA → REFUTADA."*

Esta cláusula es la que autoriza y define el objetivo de este pre-registro: sólo una medición de primera mano sobre el `.dta` de ICPSR 35024, con veredicto `CORROBORADA`/`CONTRARIA`, mueve el tier — no una nueva corrida sobre los mismos crosstabs de segunda mano.

**§0.1 · Continuidad de rótulo, declarada.** El sucesor de esta pieza ya está nombrado tres veces en el árbol — `canon/gobernanza-v1_15.md:5494`, `forense/hallazgos.md:664`, `forense/encargos/2026-09-03-MAESTRA37-N3-SELLA-CIVICA-COERCITIVO-Y-PROPAGA.md:17`, `forense/encargos/2026-09-03-MAESTRA37-A1-REGISTRA-ENSANUT-V2-Y-MANUALES.md:17` — como **`MAESTRA37-L2 · MPS-CODEBOOK-Y-P3`**, nunca lanzado. El encargo que ordena este pre-registro (`2026-09-04-MAESTRA38-N3-PRE-REGISTRO-DE-CAJA.md:8`) lo re-cita bajo la serie vigente, **`MAESTRA38-L2`**. Este documento adopta `MAESTRA38-L2` como el rótulo que se sella (la serie de actos ya avanzó de `MAESTRA37` a `MAESTRA38`), y declara la continuidad explícitamente para que quien audite no lea dos piezas donde hay una.

---

## 1 · Rama MEDICIÓN

### 1.0 · P0 obligatorio — ponderador, antes de tocar el `.dta`

**Hallazgo crítico:** en ningún archivo de texto del repo se documenta el nombre de la variable de ponderación del microdato real. Todas las menciones existentes (`tools/medidor_l12_mps2012.py:172`, `milpa/tramite-ola5-propuesta-v0.yaml:2782-2888` dos veces, `forense/notas/2026-09-03-MAESTRA36-L12-*`, `canon/gobernanza-v1_15.md:5494`) son declaraciones de **ausencia** de ponderador en los datos de **segunda mano** ya usados — ninguna cita el campo de peso del `.dta`.

**Paso P0, obligatorio antes de cualquier estimación:** abrir el codebook ya registrado —

- `icpsr35024_mexico_panel_study_2012_codebook_es_zip` (`data/manifiesto.yaml:16130`, `archivo: 35024-0001-Codebook-spanish.pdf.zip`, `sha256: f27c3f8853b70081bde06e8fec306b980d59a64f66478600cc38f96d1242180c`), o
- `35024_questionnaire_spanish` (`data/manifiesto.yaml:23971`, `archivo: ICPSR_35024/35024-Questionnaire-spanish.pdf`, `sha256: fe5be81eb5345327d3d08db73709d8de9c9ab3ee6fced8bf144b568f595a5573`)

y **extraer el nombre literal del campo de ponderación (si existe) antes de leer una sola fila del `.dta`**. Ninguno de los dos archivos ha sido abierto en ningún acto documentado — es lectura de estructura, no de valor, y no contamina la sesión (mismo criterio que `hitoD-R7_3-especificacion-v1_0.md §1`, que permite leer encabezados de `.dta` sin contaminar).

**Ponderador esperado, declarado antes de abrir (A.4):** si el codebook no trae campo de ponderación explícito para el panel completo (posible: la propia FD del estudio podría documentar el diseño como panel sin peso post-estratificación, igual que las tablas de segunda mano ya heredan), el ponderador esperado es **NINGUNO**, y cualquier estimación de este acto se reporta **sin ponderar, declarado como tal** — nunca se inventa un peso ni se hereda silenciosamente el `NINGUNO` de segunda mano sin haber mirado el codebook primero.

### 1.1 · Variables por número de ítem — `R7.3`/`R7.6`

Derivadas de `tools/medidor_l12_mps2012.py:372-427` (pieza `P2`, ya corrida sobre segunda mano) y de las cuatro notas de `MAESTRA36-L12` (`spec-congelada.md:114-117`, `spec-congelada-bis-v3.md:125-127`):

| regla | tabla | fila (variable) | columna (desenlace) | control/estratificador |
|---|---|---|---|---|
| **R7.3** | T3 | `W2_P39B` (expuesto/no expuesto a Oportunidades) | `W2_P8` (voto declarado, ronda 2) | `W2_P36C` (secreto percibido, 1–4) |
| **R7.6** | T4 | `W2_P40` (condicionaron el programa: sí/no) | `W2_P8` | `W2_P36C` |

**Réplica exacta del diseño de segunda mano, declarado a propósito**: la cláusula `se_mueve_si` (§0) pide "medición de primera mano", no un diseño distinto — este pre-registro fija T3/T4 con las mismas variables, para que el contraste primera-mano-vs-segunda-mano sea sobre el mismo diseño y no sobre un diseño nuevo que invalidaría la comparación.

### 1.2 · Experimento de lista

Ítems, verbatim de `tools/medidor_l12_mps2012.py:444-445` y `forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada.md:128-129`:

- **Ronda 1 (marzo):** `P35A` (lista A), `P35B` (lista B).
- **Ronda 2 (julio):** `W2_P35A` (lista A), `W2_P35B` (lista B).
- Excluir código `9` (NC) de ambas rondas antes de calcular.
- Contraste: pregunta directa `W2_P41` (oferta recibida, autorreporte).

**Condición de entrada, heredada verbatim de `l12-mps2012-v1_0.json:775` y `resultados.md:176-179`, no relajada aquí:** *"que lista B = lista A + UN ítem, y que ese ítem sea la venta del voto... si el cuarto ítem no es el sensible, la pieza entera se cae."* Esta rama de MEDICIÓN **no puede ejecutarse con veredicto válido** hasta que la rama TEXTO (§2) confirme o refute ese supuesto — ver §3.

### 1.3 · Universo, dicotomizaciones, celdas

- **Universo pre-registrado (heredado de segunda mano, a confirmar contra el `.dta` real):** ola panel, ronda 2 (julio 2012), `n≈1555`. Para T3/T4: personas con código de voto válido y `W2_P36C` no vacío. Para el experimento de lista: personas con código válido (≠9) en la lista asignada.
- **Si el `.dta` real reporta un `n` distinto:** se usa el `n` real, declarado — el `n≈1555` de arriba es la única cifra disponible hoy (de segunda mano) y **no** se hereda como supuesto si el microdato dice otra cosa.
- **Dicotomizaciones:** T3/T4 son tablas `2×2` (expuesto/no-expuesto × votó-PRI/no), estratificadas en 4 celdas por `W2_P36C∈{1,2,3,4}` — mismo diseño que produjo `salida["_reglas"]` en segunda mano.
- **Celdas:** 4 (una por nivel de `W2_P36C`) por cada una de T3 y T4 — 8 celdas totales para la rama R7.3/R7.6, más las 2 celdas del contraste lista-vs-directa (ronda 1 y ronda 2) para el experimento de lista.

### 1.4 · Falsador y precedencia — heredados de B-bis, no relajados

Mismo árbol que `forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada-bis-v3.md` ya congeló para segunda mano, aplicado ahora a primera mano:

- **`CORROBORADA`** si el IC95 de `Δ` (T3 y T4) **excluye** 0 en la dirección que la regla predice.
- **`CONTRARIA`** si el IC95 excluye 0 en la dirección contraria.
- **`NO-DISCRIMINA`** si el semiancho del IC95 supera **±15 pp** (mismo umbral que B-bis ya fijó) — y manda sobre las otras dos.

**Consecuencia sobre el tier (§0), declarada, no ejecutada aquí:** `CORROBORADA` → `R7.3` vuelve a `[FUERTE]` (por `se_mueve_si`). `CONTRARIA` → `R7.3` queda `REFUTADA`. `NO-DISCRIMINA` → tier no se mueve, mismo estado que hoy. Este acto de pre-registro **no aplica** ningún cambio de tier — eso lo hace el acto que produzca el primer resultado.

---

## 2 · Rama TEXTO

**Hallazgo central, verificado exhaustivamente** (los cuatro documentos de `L12`, `data/l12-mps2012-v1_0.json` completo, `tools/medidor_l12_mps2012.py` completo, `data/manifiesto.yaml`, y el filesystem de esta sesión): **el repo no contiene el wording literal de ningún ítem de ICPSR 35024.** Lo único parecido a texto verbatim en todo el corpus:

1. Las etiquetas de respuesta de `P8`/`W2_P8` (candidato/partido, 13 códigos) — `spec-congelada-bis-v3.md:74-86`.
2. Una frase entre comillas, ligada a `W2_P36D`/T9a: *«en mi comunidad los políticos compran votos»* (`resultados.md:199`) — **sin marca explícita de si es cita literal del cuestionario o paráfrasis del analista**; tratarla como tal hasta confirmar contra el cuestionario real.

### 2.1 · Tabla — ítem → lectura de L12 que sostiene → disponibilidad del texto

| tabla | variables | lectura(s) de `L12` que sostiene | texto disponible en el repo hoy |
|---|---|---|---|
| T1 | `W2_P41`×`W2_P7`, control `W2_P36C` | cuadre de marginales; base de turnout (R7.7) | NO ENCONTRADO — solo paráfrasis |
| T2 | 32 celdas, sin fila/col asignada | ninguna — nunca usada en P0–P4 | N/A |
| **T3** | `W2_P39B`×`W2_P8`, control `W2_P36C` | **R7.3** (§1.1) | NO ENCONTRADO — solo paráfrasis ("Oportunidades") |
| **T4** | `W2_P40`×`W2_P8`, control `W2_P36C` | **R7.6** (§1.1) | NO ENCONTRADO — solo paráfrasis ("condicionaron el programa") |
| T6 | `P8`×`W2_P8`, control `W2_P41` | cambio de voto entre olas, R7.7 | **Sí, parcial**: 13 etiquetas de candidato/partido verbatim del tabulador |
| T7a/T7b | `W2_P41`×`W2_P7`/`W2_P8`, control `W2_PX8` | robustez urbano/rural de R7.7 | NO ENCONTRADO para `W2_P41`/`W2_P7`; `W2_PX8` sí tiene etiquetas de estrato (1 urbano/2 rural/3 mixto) |
| T8 | `W2_P53`×`W2_P7` | sobrerreporte de participación | NO ENCONTRADO — solo paráfrasis |
| T9a | `W2_P36D`×`W2_P41` | gradiente percepción-compra-de-voto × oferta | Posible cita literal, sin confirmar: «en mi comunidad los políticos compran votos» |
| T9b (no en disco) | `W2_P38A`×`W2_P38B`, control `P46` | pendiente (L13) | NO ENCONTRADO |
| **T5 (lista)** | `P35A`/`P35B`, `W2_P35A`/`W2_P35B` | prevalencia por lista (§1.2) | **NO ENCONTRADO, declarado explícitamente como faltante por el acto mismo, tres veces** (`resultados.md:177-179`, `l12-mps2012-v1_0.json:775,930`, `medidor_l12_mps2012.py:474,568-569`) |

### 2.2 · Lo que la rama TEXTO tiene que resolver, en orden de prioridad

1. **Prioridad 1 — T5 (lista).** Leer el wording exacto de `P35A`, `P35B`, `W2_P35A`, `W2_P35B` en el cuestionario/codebook (§1.0). Verificar: ¿lista B = lista A + exactamente un ítem? ¿ese ítem es venta del voto? Si cualquiera de las dos respuestas es NO, **la pieza de experimento de lista completa de MEDICIÓN (§1.2) se cae** — se declara `PROPUESTA-REFUTADA-POR-DISEÑO`, no se fuerza un veredicto.
2. **Prioridad 2 — T3/T4 (R7.3/R7.6).** Leer el wording de `W2_P39B`, `W2_P40`, `W2_P36C`, `W2_P8` — no bloquea la ejecución de MEDICIÓN (el diseño no depende de un supuesto de composición como T5), pero sí determina si "condicionaron el programa" (T4/R7.6) y "expuesto a Oportunidades" (T3/R7.3) miden lo que la regla necesita o algo adyacente.
3. **Prioridad 3 — T9a.** Confirmar si «en mi comunidad los políticos compran votos» es cita literal de `W2_P36D` o paráfrasis — no bloquea R7.3/R7.6/lista, pero corrige la tabla de §2.1 para el siguiente acto que use T9a.

---

## 3 · Las dos ramas en un archivo — la caja declara cuál corre

Este documento fija ambas ramas; **la caja, al ejecutar, declara explícitamente el orden**, pero con esta restricción pre-registrada, no negociable en el momento de correr:

1. **TEXTO §2.2 prioridad 1 corre primero**, siempre — es lectura de estructura del codebook (P0, §1.0), no contamina, y determina si la sub-pieza de lista de MEDICIÓN (§1.2) es ejecutable en absoluto.
2. **MEDICIÓN §1.1 (R7.3/R7.6, T3/T4) puede correr en paralelo o después de TEXTO prioridad 1** — no depende de su resultado, sólo de TEXTO §2.2 prioridad 2 para anotar la calidad de la medición, no para bloquearla.
3. **MEDICIÓN §1.2 (lista) sólo corre si TEXTO §2.2 prioridad 1 confirma el supuesto.** Si lo refuta, el commit que cierre esta pieza declara `PROPUESTA-REFUTADA-POR-DISEÑO` sobre el experimento de lista y no calcula ningún `Δ` nuevo.

---

## 4 · Qué NO hace este acto

No abre el `.dta` ni el codebook — ambos están fuera de esta sesión (NUBE, sin corpus). No calcula ningún IC95, ningún `Δ`, ninguna celda. No mueve el tier de `R7.3`/`R7.6`. No cierra `FP-263` (el sucesor declarado que este documento continúa). No toca `milpa/tramite.yaml` (el motor) — sólo la enmienda de `milpa/tramite-ola5-propuesta-v0.yaml` que el encargo pide aparte (fuera de esta spec).

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
