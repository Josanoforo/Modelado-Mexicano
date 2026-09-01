# Scoreboard marco-M v1.1 — AGREGADO-b (con L extraído)

`ACTO MAESTRA33-E21 · L-EXTRAE-v1_1`, 2/sep/2026. Producido por
`python3 forense/prereg-duelo-v2/agregado_v1_1b.py` sobre las mismas 11
celdas de `marco-M-sorteado-v1_1.tsv`, MISMO procedimiento SELLADO
`procedimiento-scoring-v1_1.md` (unidades `z=(punto-R)/EE(R)`, `delta=0.5`,
`nivel_ic=0.95`, `seed=42`, `replicas=10000`), sin cambiar un parámetro.
`agregado_v1_1.py` (base) NO se edita; `agregado_v1_1b.py` lo importa por
ruta y solo reemplaza la fuente del punto de corredor `L` — de
`valor_extraido` (null en las 176 capturas) a `L-extraido-v1_1.tsv` (P2 de
este acto, `tools/extrae_l_v1_1.py`, regla congelada en
`regla-extraccion-L-v1_1.md`). Resultado completo, reproducible, en
`forense/prereg-duelo-v2/agregado-v1_1b-resultado.json`. Este documento NO
reemplaza `scoreboard-v1_1-AGREGADO.md` (queda como registro histórico de
que, el 1/sep/2026, el extractor no existía) — es el `-b`, la
re-corrida con L cargado.

Este acto no re-emite `M`, `R` ni `L`; no reabre el sorteo; no abre
dominios; no activa `E` por sí solo; no edita las 176 capturas de
`corridas-L/`; no toca `procedimiento-scoring-v1_1.md` (sellado).

## 0 · Qué cambió respecto a `scoreboard-v1_1-AGREGADO.md`

`tools/extrae_l_v1_1.py` (P2) aplicó la regla congelada de P1 a las 176
capturas reales: **171 de 176 EXTRAIBLE, 5 NO-EXTRAIBLE** (L-solo 3/88,
L+corpus 2/88 — detalle en `L-extraido-v1_1-notas-cierre.md`). Con eso, el
colapso por (celda, variante) — media de las réplicas EXTRAIBLE, misma
regla de colapso que `agregado_v1_1.py` ya declaraba para `valor_extraido`
no-nulo — deja de dar `NO-DISPONIBLE` en las 22 combinaciones
(11 celdas × 2 variantes): las 22 tienen ahora un punto de corredor `L`.

**CONTADOR — celdas pareadas L-vs-M: 0 → 11.** (universo pareado de la
comparación principal `L_SOLO_vs_M`; las 11 celdas del universo tienen
ahora `z_M` y `z_L_solo` simultáneos, frente a 0 en `scoreboard-v1_1-AGREGADO.md`).

## 1 · Por celda (11 celdas, universo `marco-M-sorteado-v1_1.tsv`)

| id_celda | M | R | z_M | L-solo | z_L_solo | L+corpus | z_L_corpus |
|---|---|---|---|---|---|---|---|
| CIV-M-01 | 0.294313 | 0.258999 | +5.07 | 0.24625 | -1.83 | 0.30000 | +5.88 |
| CIV-M-06 | 0.294313 | 0.222668 | +14.60 | 0.50825 | +58.20 | 0.40286 | +36.72 |
| CIV-M-08 | 0.294313 | 0.234696 | +12.06 | 0.32167 | +17.59 | 0.48563 | +50.74 |
| CIV-M-09 | 0.294313 | 0.203809 | +16.84 | 0.21313 | +1.73 | 0.28438 | +14.99 |
| CIV-M-11 | 0.294313 | 0.213125 | +16.04 | 0.57000 | +70.51 | 0.58214 | +72.91 |
| CIV-M-12 | 0.294313 | 0.208112 | +18.11 | 0.22500 | +3.55 | 0.46313 | +53.57 |
| CIV-M-13 | 0.294313 | 0.194612 | +18.49 | 0.37857 | +34.12 | 0.29438 | +18.50 |
| FAM-M-01 | 0.457707 | 0.557193 | -14.70 | 0.26875 | -42.63 | 0.22750 | -48.72 |
| TRA-M-03 | 0.62 | 0.044538 | +202.54 | 0.12250 | +27.44 | 0.12125 | +27.00 |
| TRA-M-05 | 0.62 | 0.077024 | +244.46 | 0.14675 | +31.39 | 0.14675 | +31.39 |
| TRA-M-07 | 0.62 | 0.071815 | +228.76 | 0.14425 | +30.23 | 0.14700 | +31.37 |

(cifras completas, sin redondeo, en `agregado-v1_1b-resultado.json`, campo
`celdas.<id>`.) Ninguna de las 11 celdas cae dentro de la banda
`[-0.5,+0.5]` bajo ningún corredor (`M`, `L_solo` ni `L_corpus`) —
`L` reproduce el mismo patrón de sobre-estimación masiva frente a `R` que
`M`, con la única excepción de `CIV-M-01` bajo `L-solo` (`z=-1.83`, aún
fuera de banda pero de signo contrario y de magnitud mucho menor).

## 2 · Agregado por corredor — proporción en banda y mediana `|z|`

**`L_SOLO`** — `n_celdas = 11`.
- Proporción dentro de banda `[-0.5,+0.5]`: **0.0** (IC 95% bootstrap,
  `seed=42`, `replicas=10000`: **[0.0, 0.0]**).
- Mediana de `|z_L_solo|`: **30.23** (IC 95%: **[3.55, 42.63]**).

**`L_CORPUS`** — `n_celdas = 11`.
- Proporción dentro de banda: **0.0** (IC 95%: **[0.0, 0.0]**).
- Mediana de `|z_L_corpus|`: **31.39** (IC 95%: **[18.50, 50.74]**).

**`M`** — `n_celdas = 11` (sin cambio respecto a `scoreboard-v1_1-AGREGADO.md`).
- Proporción dentro de banda: **0.0** (IC 95%: **[0.0, 0.0]**).
- Mediana de `|z_M|`: **16.84** (IC 95%: **[14.60, 202.54]**).

Las tres proporciones en banda son **0.0** con IC `[0.0, 0.0]` — ni `M` ni
ninguna de las dos variantes de `L` producen, en esta muestra de 11 celdas,
una sola celda dentro de `±0.5·EE(R)` de `R`. La mediana `|z|` de `L` (30-31)
es del mismo orden de magnitud que la de `M` (16.8), ligeramente más alta en
ambas variantes de `L`.

## 3 · Comparación principal `L_SOLO_vs_M` (única PASO 2, `B` NO-APLICA)

**Universo pareado = 11 celdas** (las 11 del universo tienen `z_L_solo` y
`z_M` simultáneos — antes 0). Diferencia pareada `z_L_solo - z_M`:
- Punto: **-48.36**
- IC 95% bootstrap: **[-106.35, +3.65]**

**Adjudicación: `INDETERMINADO`** (el IC cruza cero, y no cae dentro de la
banda `[-0.5,+0.5]` ni queda enteramente fuera de un lado) — no
`EQUIVALENTES-EN-BANDA` ni `L-MAS-ALTO-QUE-M`/`M-MAS-ALTO-QUE-L`. La
diferencia pareada tiene un IC muy ancho (dominado por `FAM-M-01`, donde
`L_solo` es mucho más negativo que `M` respecto a `R`) y no es
concluyente con `n=11`.

## 4 · `VERIFICACION-NO-PUNTUA` (F-DD) y `TRA-M-02` — sin cambio

Igual que `scoreboard-v1_1-AGREGADO.md` §3-4: `0` de 11 celdas bajo F-DD;
`TRA-M-02` (informativo, FP-213) fuera del universo y del pareado, sin `R`
disponible.

## 5 · La pregunta doble del whitepaper — una línea por mitad, con su IC

`milpa/milpa-whitepaper-v0_1.md:207-209` (§10, sellado `ADR-237`): *"La
pregunta del programa es doble: ¿explicitar y calibrar añade valor
predictivo sobre preguntar directo?, y ¿cuánto del conocimiento implícito
del LLM sobrevive al pasar por esa disciplina?"*

- **¿Explicitar y calibrar (M) añade valor predictivo sobre preguntar
  directo (L)?** **Indeterminado con los datos de hoy** — ahora SÍ hay
  insumo (universo pareado `L_SOLO_vs_M` = 11 celdas, IC `[-106.35,
  +3.65]` en `z_L_solo - z_M`), pero el IC cruza cero y es demasiado ancho
  para adjudicar: no se puede decir que `M` haga mejor NI peor que `L` en
  esta muestra de 11 celdas — el punto (-48.36) apunta a que `L_solo` se
  aleja MÁS de `R` que `M` en promedio, pero la incertidumbre bootstrap no
  descarta lo contrario.
- **¿Cuánto del conocimiento implícito del LLM sobrevive al pasar por la
  disciplina de M?** Con los tres corredores medibles hoy (`M`, `L_solo`,
  `L_corpus`, todos `n=11` contra `R`): **poco, por esta muestra, en los
  tres** — proporción en banda **0.0** (IC `[0.0,0.0]`) en los tres
  corredores; mediana `|z|` **16.84** (`M`, IC **[14.60, 202.54]**),
  **30.23** (`L_solo`, IC **[3.55, 42.63]**), **31.39** (`L_corpus`, IC
  **[18.50, 50.74]**). Los tres corredores sobre-estiman `R` de forma
  masiva y ninguno queda dentro de banda en ninguna celda; la disciplina
  de `M` no empeora claramente respecto de `L` (comparación de arriba,
  `INDETERMINADO`), pero tampoco hay evidencia en esta muestra de que la
  mejore de forma concluyente.

## FP-221 — criterio de activación del corredor E, conteo real

`conteo_l_interseccion_m_fp221` (celdas con punto real simultáneo en `L`,
cualquier variante, y `M`): **`n = 11`** (antes `0`), **`ids` = las 11 del
universo**. `umbral_activacion_corredor_e = 8` → **`cumple_umbral =
true`**. Recibo actualizado en `forense/firmas-pendientes.tsv` (fila
`FP-221`) con este conteo — **este acto NO activa el corredor E por sí
solo** (LO QUE NO HACE del encargo original de FP-221 y del encargo de
este acto); deja el recibo para que dirección lo revise.

## Deriva de

`forense/prereg-duelo-v2/procedimiento-scoring-v1_1.md` (procedimiento
sellado, `ADR-262`, sin cambiar) ·
`forense/prereg-duelo-v2/agregado_v1_1.py` (base, sin editar) ·
`forense/prereg-duelo-v2/agregado_v1_1b.py` (este acto, importa la base
por ruta) · `forense/prereg-duelo-v2/regla-extraccion-L-v1_1.md` (P1) ·
`tools/extrae_l_v1_1.py` (P2) ·
`forense/prereg-duelo-v2/L-extraido-v1_1.tsv` (salida de P2) ·
`forense/prereg-duelo-v2/agregado-v1_1b-resultado.json` (salida completa
de este documento) · `milpa/milpa-whitepaper-v0_1.md:207-209` (pregunta
doble) · `forense/prereg-duelo-v2/scoreboard-v1_1-AGREGADO.md` (versión
previa, sin L, registro histórico).
