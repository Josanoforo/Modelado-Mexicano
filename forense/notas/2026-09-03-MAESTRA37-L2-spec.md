# ACTO MAESTRA37-L2 · MPS-CODEBOOK-Y-P3 — SPEC CONGELADA (COMMIT-1)

**Fecha:** 3/sep/2026 · **Caja:** UBUNTU con corpus · **Base:** `origin/main` = `27647ac`
(idéntico al SHA de redacción del encargo) · **COMPUERTA:** ninguna · **ADR candidato:** ver cierre.

Esta spec se escribe **antes de abrir `35024-Questionnaire-spanish.pdf`**. Lo único leído
hasta este commit son las salidas de `MAESTRA36-L12` (que ya estaban en `main`), la fila
`FP-263` de `forense/firmas-pendientes.tsv`, y las tres entradas del manifiesto registradas
por `MAESTRA37-A1`. **Ni una línea del cuestionario, ni una celda del CSV, se ha leído.**

---

## 0 · Lo que no cambia, declarado antes de abrir nada

Se repite aquí porque el insumo nuevo **no lo altera**:

1. Los conteos del CSV son **SIN PONDERAR**.
2. El CSV es un **instrumento de segunda mano** (export del tabulador en línea de ICPSR),
   no microdato.
3. **`35024-0001-Data.dta` sigue sin obtenerse.** Nada de lo que produzca este acto es
   medición de primera mano.
4. Este acto **no mide, no pondera, no re-calcula nada de L12**. Adjudica **por texto**.

---

## 1 · Universo declarado (`P0`)

| pieza | archivo | `sha256` declarado en manifiesto | raíz |
|---|---|---|---|
| tabulados | `ICPSR35024-ds1-w2-tabulados-T5-T9-derivados-2026-09-02.csv` | `304507711d11…` | `descargas_mx` |
| procedencia | `LEEME-ICPSR35024-ds1-w2-tabulados-T5-T9-procedencia-2026-09-02.txt` | `55a038587186…` | `descargas_mx` |
| **cuestionario** | `ICPSR_35024/35024-Questionnaire-spanish.pdf` | `fe5be81eb534…` | `descargas_mx` |

La raíz `descargas_mx` se resuelve por `data/raices.local.yaml` (**gitignorada**): sin ella
toda búsqueda declara `NO-ENCONTRADO` en falso (hallazgo de `MAESTRA35-L9`). Ya está copiada
al worktree de este acto.

**Productos de `P0`:**

- `data/l2-mps2012-cuestionario-v1_0.txt` — `pdftotext -layout` sobre el PDF, con cabecera
  que lleva `sha256_12` y número de páginas (mismo patrón que `data/l3-ensanut2024-cuestionarios-v1_0.txt`
  de `MAESTRA37-L3`). Si pesa demasiado para el repo, **sólo `sha` + ruta**, y se dice.
- `data/l2-mps2012-items-v1_0.tsv` — anexo: `ítem · texto · opciones · tabla(s) donde aparece`.
- Lista de las once tablas del CSV **por comando**, no a ojo.
- **`A.13` en una línea** por cada negativo: cuántos archivos / cuántas páginas examinó el
  comando que lo produjo.

---

## 2 · Qué ítems necesita cada pieza — **congelado por número, antes de leer**

### `P1` — `FP-263`

`FP-263` pide **tres** cosas, y su control negativo (medido por L12, no supuesto) era:
*«ninguna tabla del disco usa `P40`, `P39` ni `P38B` como variable de fila o de columna»*.

| # | lo que `FP-263` pide | veredicto `A.4` que este acto debe emitir |
|---|---|---|
| (i) | **T9b**: fila `W2_P38A`, columna `W2_P38B`, control `P46` | `EXISTE-SATISFACE` / `EXISTE-NO-SATISFACE` / `NO-ENCONTRADO` |
| (ii) | **ronda 1 completa**: `P40×P7`, `P40×P8`, `P38B×P8` (control `P36C`), `P39×P8` | idem, **una por una: cuatro veredictos, no uno agregado** |
| (iii) | **texto de los ítems** `P35A` / `P35B` / `W2_P35A` / `W2_P35B` | idem |

**Regla de cierre de `FP-263`, congelada:** la fila pasa a `EJECUTADA` **sólo si las tres
partes (i), (ii) y (iii) salen `EXISTE-SATISFACE`**. Basta que una quede corta para que
`FP-263` siga `ABIERTA`, y entonces se dice **qué falta exactamente**. `FP-263` no se cierra
"en lo esencial": se cierra o no se cierra.

⚠️ **Guardia contra el falso positivo de rótulo** (`feedback: identifica el contenido por una
identidad, no por su rótulo`): que el CSV traiga una tabla **rotulada** `T9b` no prueba que sea
`W2_P38A × W2_P38B` con control `P46`. La identidad se verifica por **las variables de fila,
columna y control que la tabla declara**, no por su encabezado. Lo mismo para las cuatro de
ronda 1.

⚠️ **Guardia `A.13`:** el control negativo de L12 (*«ninguna tabla usa P40/P39/P38B»*) se
**re-corre** sobre el CSV nuevo, declarando cuántas tablas examinó el comando. Un negativo
heredado de L12 no vale sobre un archivo que L12 nunca leyó.

### `P2` — L12 `P2` (R7.3 / R7.6, tercer instrumento)

L12 midió, sobre `W2_P39B` (Oportunidades) y `W2_P40` (condicionaron el programa), con
desenlace voto PRI (`W2_P8`) y control `W2_P36C` (secreto percibido, 1–4):

| tabla | expuesto a | Δ agregado | IC95 |
|---|---|---:|---|
| T3 | `W2_P39B` | +0.39 pp | [−7.13, +7.92] |
| T4 | `W2_P40` | −6.86 pp | [−20.39, +6.68] |

**Ítems cuyo texto se necesita:** `W2_P39B`, `W2_P40`, `W2_P8`, `W2_P36C`.

**Qué texto sostiene y qué texto tumba — congelado:**

- Se **SELLA** (`REPLICA-DE-SEGUNDA-MANO-SELLADA`) si el texto confirma que: `W2_P39B` mide
  **recepción/exposición al programa Oportunidades**; `W2_P40` mide **condicionamiento del
  programa al voto**; `W2_P8` es **voto por el PRI** (desenlace, no intención genérica); y
  `W2_P36C` es **secreto percibido del voto** en escala 1–4. Es decir: los cuatro constructos
  que R7.3/R7.6 nombran son los que estas cuatro variables preguntan.
- Se **RECHAZA** (`REPLICA-DE-SEGUNDA-MANO-RECHAZADA`) si alguno de los cuatro pregunta
  **otra cosa** que la que la réplica le atribuye — p. ej. si `W2_P40` no pregunta por
  condicionamiento sino por conocimiento del programa, o si `W2_P8` no es voto sino simpatía
  partidista.
- Sigue **`NO-SELLADA`** si el cuestionario **no trae** el texto de alguno de los cuatro, o lo
  trae de forma que no permite decidir. En ese caso se dice **cuál** y **por qué**.

**No re-calcula nada de L12. Lee.** Las cifras de arriba se citan verbatim de
`forense/notas/2026-09-03-MAESTRA36-L12-resultados.md` §3 y no se recomputan.

### `P3` — L12 `P3` (experimento de lista)

L12 midió, `NC(9)` excluido: ronda 1 (marzo, `P35A`/`P35B`) Δ = **0.0688**, IC95
[−0.027, +0.165], **cruza 0**; ronda 2 (julio, `W2_P35A`/`W2_P35B`) Δ = **0.1876**, IC95
[+0.085, +0.290]. Contra la pregunta directa `W2_P41` (5.5 %), factor 3.41.

L12 declaró el supuesto que gobierna la pieza entera: **que lista B = lista A + UN ítem, y que
ese ítem sea la venta del voto**; y que *«si el cuarto ítem no es el sensible, la pieza entera
se cae»*.

**Ítems cuyo texto se necesita:** `P35A`, `P35B`, `W2_P35A`, `W2_P35B`, y `W2_P41` (la directa,
para el punto de constructo).

**Veredicto congelado — dos condiciones, ambas necesarias:**

1. **Condición de diseño:** lista B = lista A **+ exactamente un** ítem (las listas coinciden
   en todos los demás), en **cada** ronda.
2. **Condición de contenido:** ese ítem añadido es **la venta / compra del voto** (conducta
   propia de vender el voto, o su equivalente literal).

- Si **(1) y (2)** se cumplen → **`CORROBORADA-EN-TEXTO`**, con el texto del ítem **citado
  verbatim** y su número.
- Si falla **(2)** (la lista B sí añade un ítem, pero no es la venta del voto) → **`VENCIDA EN
  ALCANCE`**, y se nombra **el ítem real**: la aritmética de L12 sigue siendo correcta, pero
  no mide compra de voto.
- Si falla **(1)** (las listas difieren en más de un ítem, o el ítem no es aditivo) → **`VENCIDA
  EN ALCANCE`** por diseño, y se dice en cuántos ítems difieren. El Δ deja de ser atribuible a
  un ítem.
- Si el cuestionario **no trae** las listas → la pieza sigue como L12 la dejó
  (**`PROPUESTA CON RESERVA`**), y se dice qué páginas se examinaron (`A.13`).

⚠️ **Las dos rondas se adjudican por separado.** Que la ronda 2 (julio) cumpla no implica que
la ronda 1 (marzo) cumpla: son dos pares de listas distintos.

⚠️ Lo que este acto **no** toca de L12 `P3`: los cuatro puntos pegados a la cifra (secuencia
rota en las dos rondas, no-escritura de «subió de 6.9 % a 18.8 %», y la mezcla de subreporte
con diferencia de constructo del factor 3.41) siguen **vigentes tal cual**. Corroborar el
texto del ítem **no los levanta**.

---

## 3 · Frase de sello

> **El texto del cuestionario ICPSR 35024 (`sha256` `fe5be81eb534…`) se leyó con `pdftotext
> -layout` sobre las páginas que este acto declara, y los veredictos de arriba se emiten
> contra ese texto citado verbatim y no contra ninguna paráfrasis, resumen ni recuerdo. Ningún
> veredicto de este acto es medición: el instrumento sigue siendo de segunda mano, los conteos
> siguen SIN PONDERAR, y `35024-0001-Data.dta` sigue sin obtenerse.**

---

## 4 · Perímetro (verbatim del encargo)

**Toca:** `data/l2-*` (nuevos) · `milpa/tramite-ola5-propuesta-v0.yaml` (**sólo enmiendas
append** en las dos entradas de L12) · `data/INFRAESTRUCTURA-v1_0.md` ·
`forense/notas/2026-09-03-MAESTRA37-L2-*.md` · `forense/hallazgos.md` ·
`forense/firmas-pendientes.tsv` · `A.3` · cascada.

**NO toca:** `milpa/tramite.yaml` · `forense/prereg-duelo-v2/**` · `data/manifiesto.yaml` ·
las salidas de L12 (se leen, no se editan) · `data/l3*` / `data/l3bis*`.

**No descarga; no re-exporta de ICPSR.** Si el ejecutor se encuentra escribiendo fuera de esta
lista: **PARA**.

Las dos entradas `PENDIENTE-DE-MESA` de L12 en `milpa/tramite-ola5-propuesta-v0.yaml` ganan una
**enmienda fechada en append, 0 líneas borradas** — **no** un cambio de `situacion`, que es de
`N7`.

---

## 5 · Contador declarado (se re-declara con el real en COMMIT-2)

- piezas de L12 adjudicadas: **0 → 2** (esperado; el real va en los veredictos)
- `FP-263`: **ABIERTA →** `EJECUTADA` o razón
- cargas al motor: **0**
- medición: **cero directo** (adjudicación por texto, sin microdato)
