# Scoreboard marco-M v1.2 — AGREGADO sellado

`ACTO MAESTRA36-N2 · CIERRA-N3-AGREGA-2`, 3/sep/2026. Ejecuta P1/P2 de
`ACTO MAESTRA34-N3 · AGREGA-2` (`forense/encargos/cola/2026-09-01-MAESTRA34
-N3-AGREGA-2.md`, cuerpo líneas 24-27 + ENMIENDA 5). Producido por
`python3 forense/prereg-duelo-v2/agregado_v1_2.py` sobre las **14 celdas**
de `marco-M-sorteado-v1_2.tsv`, aplicando el procedimiento SELLADO
`procedimiento-scoring-v1_1.md` (unidades `z=(punto-R)/EE(R)`, `delta=0.5`,
`nivel_ic=0.95`, `seed=42`, `replicas=10000`) **sin cambiar un parámetro y
sin editar `agregado_v1_1.py`, `tools/score_marco_m.py` ni el
procedimiento** — `agregado_v1_2.py` importa `agregado_v1_1.py` por ruta
(mismo patrón que `agregado_v1_1b.py` ya usa para v1.1) y sobreescribe,
por monkeypatch quirúrgico, el marco, el universo y las fuentes de `M` y
`L`. Resultado completo, reproducible, en
`forense/prereg-duelo-v2/agregado-v1_2-resultado.json`. Este acto no
re-emite `M`, `R` ni `L`; no reabre el sorteo; no abre dominios; no activa
`E`; no recalcula la doble `EE` de `DIN-M-01` (la cita).

## 0 · Qué cambió respecto a `scoreboard-v1_1-AGREGADO-b.md`

Universo: **11 → 14 celdas** (`marco-M-sorteado-v1_2.tsv`; las 7 nuevas de
v1.2 son `CIV-M-02`, `CIV-M-04`, `CIV-M-10`, `DIN-M-01`, `FAM-M-05`,
`FAM-M-06`, `FAM-M-07` — sustituyen a `CIV-M-06`, `CIV-M-08`, `CIV-M-09`,
`CIV-M-11`, `TRA-M-05`, que no están en el sorteado v1.2, más `DIN-M-01`
que sí lo estaba en v1.1 pero llegaba sin `M` hasta el levantamiento de la
exclusión por firma `d2`). `M` de las 7 celdas heredadas se lee del mismo
archivo `M-<id>.json` que v1.1 (no cambió de valor entre versiones del
marco); `M` de las 7 nuevas se lee de `M-<id>__v1_2.json`. `L` se lee de
`forense/prereg-duelo-v2/L-extraido-v1_2.tsv` (extractor
`tools/extrae_l_v1_1.py`, parcheado por PR #497/ENMIENDA 3, sha
`efb71de1…`): **191 de 224 réplicas EXTRAIBLE** (L-solo 91/112, L+corpus
100/112 — detalle completo en `L-extraido-v1_2-notas-cierre.md`), frente a
171/176 en v1.1. Colapso por (celda, variante): media de las réplicas
EXTRAIBLE, misma regla que v1.1/v1.1b.

**CONTADOR — celdas puntuadas v1.2: 0 → 14 de 14** (0 `VERIFICACION-NO-
PUNTUA` bajo F-DD, 0 `AMBIGUA-POR-DISEÑO`). **CONTADOR — celdas pareadas
`L_SOLO_vs_M`: 0 → 13** de 14 (`CIV-M-04` sin `L-solo`: sus 8 réplicas
`L-solo` son **todas** `NO-EXTRAIBLE` en `L-extraido-v1_2.tsv` —
consecuencia mecánica del dato, anticipada por
`procedimiento-scoring-v1_1.md` §6, no de una decisión de este acto;
`CIV-M-04` sí tiene `L+corpus`, así que cuenta en el conteo `L∩M`
de abajo). **CONTADOR — celdas pareadas `L_CORPUS_vs_M`: 14 de 14.**

## 1 · Por celda (14 celdas, universo `marco-M-sorteado-v1_2.tsv`)

`0` de `14` celdas marcadas `VERIFICACION-NO-PUNTUA` bajo F-DD (verificado
contra `grado_DD` de las 14 filas — todas `P1 PUNTUA`).

| id_celda | M | R | EE(R) | z_M | z_M en banda [-0.5,0.5] | L-solo | z_L_solo | L+corpus | z_L_corpus |
|---|---|---|---|---|---|---|---|---|---|
| CIV-M-01 | 0.29431 | 0.25900 | 0.00697 | +5.07 | NO | 0.24625 | -1.83 | 0.30000 | +5.88 |
| CIV-M-02 | 0.29431 | 0.24340 | 0.00624 | +8.16 | NO | 0.85000 | +97.25 | 0.78333 | +86.56 |
| CIV-M-04 | 0.29431 | 0.24367 | 0.00748 | +6.77 | NO | NO-DISPONIBLE | NO-DISPONIBLE | 0.85750 | +82.02 |
| CIV-M-10 | 0.29431 | 0.20493 | 0.00477 | +18.72 | NO | 0.37500 | +35.63 | 0.70300 | +104.34 |
| CIV-M-12 | 0.29431 | 0.20811 | 0.00476 | +18.11 | NO | 0.22500 | +3.55 | 0.46313 | +53.57 |
| CIV-M-13 | 0.29431 | 0.19461 | 0.00539 | +18.49 | NO | 0.37857 | +34.12 | 0.29437 | +18.50 |
| DIN-M-01 | 0.17480 | 0.15558 | 0.00482 | +3.99 | NO | 0.20938 | +11.16 | 0.33750 | +37.73 |
| FAM-M-01 | 0.45771 | 0.55719 | 0.00677 | -14.70 | NO | 0.26875 | -42.63 | 0.22750 | -48.72 |
| FAM-M-05 | 0.04569 | 0.04746 | 0.00126 | -1.40 | NO | 0.04612 | -1.06 | 0.04587 | -1.25 |
| FAM-M-06 | 0.04569 | 0.04729 | 0.00120 | -1.33 | NO | 0.04875 | +1.23 | 0.04725 | -0.03 |
| FAM-M-07 | 0.04569 | 0.04378 | 0.00101 | +1.90 | NO | 0.05287 | +9.00 | 0.05163 | +7.76 |
| TRA-M-02 | 0.62000 | 0.12602 | 0.00506 | +97.62 | NO | 0.15125 | +4.99 | 0.15000 | +4.74 |
| TRA-M-03 | 0.62000 | 0.04454 | 0.00284 | +202.54 | NO | 0.12250 | +27.44 | 0.12125 | +27.00 |
| TRA-M-07 | 0.62000 | 0.07182 | 0.00240 | +228.76 | NO | 0.14425 | +30.23 | 0.14700 | +31.37 |

(cifras completas, sin redondeo, en `agregado-v1_2-resultado.json`, campo
`celdas.<id>`.) Ninguna de las 14 celdas cae dentro de la banda
`[-0.5,+0.5]` bajo ningún corredor medido. `FAM-M-06` bajo `L+corpus`
(`z=-0.03`) es la más cercana a la banda de las 41 combinaciones
celda×corredor disponibles — sigue fuera, pero por un margen mínimo, a
diferencia del resto (`|z|` de un dígito a varios cientos).

## 2 · Agregado por corredor — proporción en banda y mediana `|z|`

**`M`** — `n_celdas = 14`.
- Proporción dentro de banda `[-0.5,+0.5]`: **0.0** (IC 95% bootstrap,
  `seed=42`, `replicas=10000`: **[0.0, 0.0]**).
- Mediana de `|z_M|`: **11.43** (IC 95%: **[3.99, 18.72]**).

**`L_SOLO`** — `n_celdas = 13` (`CIV-M-04` sin punto, ver §0).
- Proporción dentro de banda: **0.0** (IC 95%: **[0.0, 0.0]**).
- Mediana de `|z_L_solo|`: **11.16** (IC 95%: **[3.55, 34.12]**).

**`L_CORPUS`** — `n_celdas = 14`.
- Proporción dentro de banda: **0.071** — **1 de 14** (`FAM-M-06`, IC 95%:
  **[0.0, 0.214]**).
- Mediana de `|z_L_corpus|`: **29.19** (IC 95%: **[6.25, 53.57]**).

Los tres corredores sobre-estiman `R` de forma masiva; `L_CORPUS` es el
único con una celda dentro de banda hoy (`FAM-M-06`), y su IC de
proporción SÍ cruza valores distintos de cero por ese único caso — no se
adjudica nada por una celda de 14.

## 3 · Comparación principal `L_SOLO_vs_M` — la pregunta doble, mitad 1

**La comparación principal del contrato F1 sigue siendo `L_SOLO_vs_M`**
(`procedimiento-scoring-v1_1.md` §3, única sellada). Universo pareado:
**13 celdas** (`CIV-M-04` fuera, sin `z_L_solo`). Diferencia pareada
`z_L_solo - z_M`:
- Punto: **-28.99**
- IC 95% bootstrap: **[-74.02, +9.40]**

**El IC cruza cero → no se adjudica.** Veredicto formal:
**`INDETERMINADO`** (no `EQUIVALENTES-EN-BANDA` ni
`L-MAS-ALTO-QUE-M`/`M-MAS-ALTO-QUE-L`) — el IC no cae dentro de
`[-0.5,+0.5]` ni queda enteramente de un lado.

## 3bis · Comparación secundaria `L_CORPUS_vs_M` — la pregunta doble, mitad 2

**Diagnóstico adicional, no la comparación principal del contrato F1**
(esa sigue siendo únicamente §3, arriba) — el encargo (cuerpo línea 26)
pide ambos pareados para la pregunta doble del whitepaper.
`agregado_v1_2.py` la calcula reutilizando, sin copiar ni editar,
`_bootstrap_pareado_z`/`_adjudicar` de `agregado_v1_1.py` con los pares
`(z_L_corpus, z_M)`. Universo pareado: **14 celdas** (las 14, todas con
`z_L_corpus` y `z_M`). Diferencia pareada `z_L_corpus - z_M`:
- Punto: **-13.09**
- IC 95% bootstrap: **[-59.70, +27.05]**

**El IC cruza cero → no se adjudica.** Veredicto formal:
**`INDETERMINADO`**.

## 4 · `VERIFICACION-NO-PUNTUA` (F-DD)

Vacía: `0` de las 14 celdas del universo trae `grado_DD =
"VERIFICACION-NO-PUNTUA"` hoy (verificado contra la columna `grado_DD` de
`marco-M-sorteado-v1_2.tsv` para las 14 filas — todas `P1 PUNTUA`).
Declarado, sin efecto observable en este agregado. Ver también §6(b)
abajo (reserva F-DD, distinta de esta exclusión mecánica).

## 5 · La pregunta doble del whitepaper — una línea por mitad, con su IC

`milpa/milpa-whitepaper-v0_1.md:207-209` (§10, sellado `ADR-237`): *"La
pregunta del programa es doble: ¿explicitar y calibrar añade valor
predictivo sobre preguntar directo?, y ¿cuánto del conocimiento implícito
del LLM sobrevive al pasar por esa disciplina?"*

- **¿Explicitar y calibrar (M) añade valor predictivo sobre preguntar
  directo (L)?** **Indeterminado con los datos de hoy, en las dos
  variantes de `L`.** `L_SOLO_vs_M`: IC `[-74.02, +9.40]` en
  `z_L_solo - z_M` (n=13) — cruza cero. `L_CORPUS_vs_M`: IC `[-59.70,
  +27.05]` en `z_L_corpus - z_M` (n=14) — cruza cero. Ninguna de las dos
  diferencias pareadas permite decir que `M` haga mejor NI peor que `L`
  en esta muestra; los dos puntos (`-28.99`, `-13.09`) apuntan a que `L`
  se aleja más de `R` que `M` en promedio, pero la incertidumbre
  bootstrap no lo descarta.
- **¿Cuánto del conocimiento implícito del LLM sobrevive al pasar por la
  disciplina de M?** Con los tres corredores medibles hoy (`M`, `L_solo`,
  `L_corpus`, `n=14`/`13`/`14` respectivamente contra `R`): **poco, por
  esta muestra, en los tres** — proporción en banda **0.0** (`M`,
  `L_SOLO`) y **0.071** (`L_CORPUS`, una sola celda de 14); mediana `|z|`
  **11.43** (`M`, IC **[3.99, 18.72]**), **11.16** (`L_SOLO`, IC **[3.55,
  34.12]**), **29.19** (`L_CORPUS`, IC **[6.25, 53.57]**). La disciplina
  de `M` no empeora claramente respecto de `L` (comparación de arriba,
  `INDETERMINADO` en ambas mitades), pero tampoco hay evidencia en esta
  muestra de que la mejore de forma concluyente.

## 6 · Reservas

**(a) `d1` sobre `DIN-M-01` (`FP-249` FIRMADA).** `DIN-M-01` puntúa en
este agregado con `EE_R` (la aproximada, cota inferior; factor de diseño
medido `0.004821494748362768 / 0.004018626879101259` =
**1.1997866170250338**, `exclusiones-v1_2.md:36-47`). La reserva `d1`
exige declarar si el veredicto de banda de la celda cambia al usar
`EE_R_sin_diseno` en vez de la aproximada: **NO cambia**
(`FUERA-DE-BANDA` con ambas `EE`) — calculado y firmado por
`forense/prereg-duelo-v2/din_m_01_doble_ee.py` (ENMIENDA 5,
`din-m-01-doble-ee-resultado.json`), **no recalculado por este acto**.
Por eso `DIN-M-01` cuenta como puntuada y no queda
`AMBIGUA-POR-DISEÑO`.

**(b) F-DD.** `0` de las 14 celdas del universo está excluida por
`grado_DD = "VERIFICACION-NO-PUNTUA"` (§4). Ninguna otra celda trae una
reserva F-DD activa hoy — la única reserva F-DD viva en
`forense/prereg-duelo-v2/exclusiones-v1_2.md` (rangos de ola para
`DIN-M-01`, `FP-234`) ya fue LEVANTADA por firma `d2` antes de este acto
(§0 arriba, §6(a)); el sucesor de rangos de ola sigue abierto
(`FP-234`, gateado a `MAESTRA34-E1`, 8/sep/2026) pero no bloquea a
`DIN-M-01` en este ciclo.

**(c) 96 capturas reanudadas sin `sha256_prompt` (ENMIENDA 2).** De las
224 capturas reales de `corridas-L/` para v1.2, **96 son reanudadas** de
la corrida v1.1 (`ba7bfa7`) y **no traen `sha256_prompt`/`params`** (la
corrida v1.1 las perdió — 0 de 176; control positivo: las 8 del piloto
`CIV-08` sí las traen); las **128** nuevas de `ACTO L-CORRIDAS-v1_2` sí
los traen. Su equivalencia de prompt con las 128 nuevas quedó
**re-derivada, no verificada**, en
`forense/notas/2026-09-02-L-corridas-v1_2-cierre.md` §3 (ENMIENDA 2,
`forense/encargos/cola/2026-09-01-MAESTRA34-N3-AGREGA-2.md:76-78`). Este
acto no re-verifica esa equivalencia — la cita como reserva abierta sobre
el 43% (96/224) de las capturas que alimentan este scoreboard.

## 7 · `FP-220`/`FP-260` (sucesora de `FP-221`) — conteo real `L∩M`, v1.2

`conteo_l_interseccion_m_fp221` (celdas con punto real simultáneo en `L`,
cualquier variante, y `M`): **`n = 14` de 14** (`CIV-M-04` entra por
`L+corpus` aunque no tenga `L-solo`). `umbral_activacion_corredor_e = 8`
→ **`cumple_umbral = true`**. Recibos actualizados en
`forense/firmas-pendientes.tsv`: `FP-220` (conteo v1.2 añadido a su
`ejecutada_en`) y `FP-260` (nueva, sucesora de `FP-221`, que ya reportó
`n=11` para v1.1 el 2/sep). El criterio de activación del corredor `E`
(`canon/motor-nucleo-medible-v1_0.md` §3.b: `L`/`M` en ≥8 celdas comunes
Y scoring v1_1 sellado) **se cumple** con este conteo — una línea lo
declara en el canon (§3, sin activar el corredor: eso es firma de mesa
aparte). **Este acto NO activa el corredor `E`** (`LO QUE NO HACE` del
encargo).

## Deriva de

`forense/prereg-duelo-v2/procedimiento-scoring-v1_1.md` (procedimiento
sellado, `ADR-262`, sin cambiar) ·
`forense/prereg-duelo-v2/agregado_v1_1.py` (base, sin editar) ·
`forense/prereg-duelo-v2/agregado_v1_2.py` (este acto, importa la base
por ruta) · `forense/prereg-duelo-v2/L-extraido-v1_2.tsv` (PR #497) ·
`forense/prereg-duelo-v2/exclusiones-v1_2.md` (firmas `d1`/`d2`,
`FP-249`) · `forense/prereg-duelo-v2/din_m_01_doble_ee.py` y
`din-m-01-doble-ee-resultado.json` (ENMIENDA 5, reserva `a`) ·
`forense/prereg-duelo-v2/agregado-v1_2-resultado.json` (salida completa
de este documento) · `milpa/milpa-whitepaper-v0_1.md:207-209` (pregunta
doble) · `canon/motor-nucleo-medible-v1_0.md` §3 (criterios de Ola 6 y
corredor E) · `forense/prereg-duelo-v2/scoreboard-v1_1-AGREGADO-b.md`
(precedente de formato, v1.1).
