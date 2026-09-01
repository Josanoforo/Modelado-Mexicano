# Scoreboard marco-M v1.1 — AGREGADO sellado

`ACTO MAESTRA33-E13 · AGREGA-1`, 1/sep/2026. Producido por
`python3 forense/prereg-duelo-v2/agregado_v1_1.py` sobre las 11 celdas de
`marco-M-sorteado-v1_1.tsv`, aplicando el procedimiento SELLADO
`procedimiento-scoring-v1_1.md` (unidades `z=(punto-R)/EE(R)`, `delta=0.5`,
`nivel_ic=0.95`, `seed=42`, `replicas=10000`) sin cambiar un parámetro.
Resultado completo, reproducible, en
`forense/prereg-duelo-v2/agregado-v1_1-resultado.json`. Este acto no
re-emite `M`, `R` ni `L`; no reabre el sorteo; no abre dominios; no activa
`E`.

## 0 · Hallazgo declarado antes de leer los números

Las 176 capturas reales de `corridas-L/` para las 11 celdas de marco-M
v1.1 (2 variantes × 8 réplicas, censo exhaustivo — `n_archivos_l_examinados
= 176` en el resultado adjunto) traen **`valor_extraido = null` en las
176**, sin excepción. `runner_l_cli.py` (líneas ~124-129) y
`PAQUETE-L-v1_1.md:180` declaran que el parseo de `texto_crudo` a un punto
numérico queda para "un extractor aparte, congelado antes de aplicarse" —
ese extractor **no existe en el repo** para el marco-M v1_1 (sí existió y
corrió para el piloto: `CIV-08` trae `valor_extraido: 61.0`). Este acto no
lo construye: hacerlo a partir de prosa libre inventaría una regla de
extracción que el procedimiento sellado no pide.

**Consecuencia mecánica, no una decisión de este acto:** el universo
marginal de `L_SOLO` y de `L_CORPUS` sale de tamaño `0`; el universo
pareado `L_SOLO_vs_M` sale de tamaño `0` (`SIN_CELDAS_PAREADAS`). El propio
`procedimiento-scoring-v1_1.md` §6 anticipa exactamente este caso: *"Esa
cuenta es consecuencia del dato, no una decisión de este documento"*. Solo
el corredor `M` tiene punto real disponible en las 11 celdas hoy.

## 1 · Por celda (11 celdas, universo `marco-M-sorteado-v1_1.tsv`)

`0` de `11` celdas marcadas `VERIFICACION-NO-PUNTUA` bajo F-DD (verificado
contra `grado_DD` de las 11 filas — todas `P1 PUNTUA`).

| id_celda | M | R | EE(R) | z_M | z_M en banda [-0.5,0.5] | L-solo | L+corpus |
|---|---|---|---|---|---|---|---|
| CIV-M-01 | 0.294313 | 0.258999 | 0.006971 | +5.07 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| CIV-M-06 | 0.294313 | 0.222668 | ~0.00491 | +14.60 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| CIV-M-08 | 0.294313 | 0.234696 | ~0.00495 | +12.06 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| CIV-M-09 | 0.294313 | 0.203809 | ~0.00537 | +16.84 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| CIV-M-11 | 0.294313 | 0.213125 | ~0.00506 | +16.04 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| CIV-M-12 | 0.294313 | 0.208112 | ~0.00475 | +18.11 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| CIV-M-13 | 0.294313 | 0.194612 | ~0.00539 | +18.49 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| FAM-M-01 | 0.457707 | 0.557193 | ~0.00677 | -14.70 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| TRA-M-03 | 0.62 | 0.044538 | 0.002841 | +202.54 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| TRA-M-05 | 0.62 | 0.077024 | 0.002221 | +244.46 | NO | NO-DISPONIBLE | NO-DISPONIBLE |
| TRA-M-07 | 0.62 | 0.071815 | 0.002396 | +228.76 | NO | NO-DISPONIBLE | NO-DISPONIBLE |

(cifras exactas de `EE(R)` en `agregado-v1_1-resultado.json`, campo
`celdas.<id>.EE_R`; la tabla arriba redondea las de `~0.005` orden de
magnitud para legibilidad — el JSON es la fuente autoritativa). Ninguna de
las 11 celdas cae dentro de la banda `[-0.5,+0.5]` para `M`: los tres
corredores `CIV-M-*` sobre-estiman `R` por 5 a 18 desviaciones estándar de
`R`, y `TRA-M-03/05/07` — el ASIGNADO `p=0.62` de `paga_mordida` contra un
`R` real de ~0.05-0.08 — por más de 200. `FAM-M-01` sub-estima por ~14.7.

## 2 · Agregado por corredor

**`L_SOLO`** — `n_celdas = 0`. Proporción en banda: NO-DISPONIBLE (universo
vacío). Mediana `|z|`: NO-DISPONIBLE (universo vacío). Sin puntos L
extraídos, no hay agregado que bootstrapear.

**`L_CORPUS`** — `n_celdas = 0`. Mismo motivo que `L_SOLO`.

**`M`** — `n_celdas = 11`.
- Proporción dentro de banda `[-0.5,+0.5]`: **0.0** (IC 95% bootstrap,
  `seed=42`, `replicas=10000`: **[0.0, 0.0]**) — 0 de 11 celdas de `M` caen
  dentro de la banda de indiferencia respecto a `R`.
- Mediana de `|z_M|`: **16.84** (IC 95% bootstrap: **[14.60, 202.54]**) —
  IC muy ancho porque `n=11` y dos celdas (`TRA-M-0{3,5,7}`, en realidad 3)
  tienen `|z|` de dos órdenes de magnitud por encima del resto
  (`CIV-M-*`/`FAM-M-01`, `|z|` de un solo dígito a bajo-veintenas).

**Comparación principal `L_SOLO_vs_M` (única PASO 2, PASO 1 omitido — `B`
NO-APLICA, §4 del procedimiento sellado):** universo pareado = **0 celdas**
(ninguna celda tiene `z_L_solo` y `z_M` simultáneos). Adjudicación:
**`SIN_CELDAS_PAREADAS`** — no `INDETERMINADO` ni `EQUIVALENTES-EN-BANDA`,
que exigirían al menos un IC calculable; aquí no hay insumo para
calcularlo. Consecuencia del dato (extractor L pendiente), no del
procedimiento.

## 3 · `VERIFICACION-NO-PUNTUA` (F-DD)

Vacía: `0` de las 11 celdas del universo trae `grado_DD =
"VERIFICACION-NO-PUNTUA"` hoy. Declarado, sin efecto observable en este
agregado (misma nota que `procedimiento-scoring-v1_1.md` §5 anticipa para
un sorteo futuro con `ola_calibracion`).

## 4 · `TRA-M-02` — informativo (FP-213), fuera del universo y del pareado

`TRA-M-02` no fue sorteada en `marco-M-sorteado-v1_1.tsv` (11 celdas) —
viene del esquema `marco-M-sorteado-v1_0.tsv`, anterior a F-DD (`FP-213`).
Se reporta aparte, sin entrar a ningún agregado ni al universo pareado:

- `M = 0.62` (`ASIGNADO`, conducta `paga_mordida`, ancla ENCIG 2023 —
  `corridas-M/M-TRA-M-02.json`).
- `R`: **NO-ENCONTRADO** en `corridas-R/` (no existe `corridas-R/TRA-M-02.json`
  en el árbol de este acto). Sin `R`, `z` no se calcula para esta celda.

## 5 · La pregunta doble del whitepaper — una línea por mitad, con su IC

`milpa/milpa-whitepaper-v0_1.md:207-209` (§10, sellado `ADR-237`): *"La
pregunta del programa es doble: ¿explicitar y calibrar añade valor
predictivo sobre preguntar directo?, y ¿cuánto del conocimiento implícito
del LLM sobrevive al pasar por esa disciplina?"*

- **¿Explicitar y calibrar (M) añade valor predictivo sobre preguntar
  directo (L)?** **Indeterminado con los datos de hoy** — no por empate
  dentro de banda, sino porque el universo pareado `L_SOLO_vs_M` es de
  tamaño `0` (`SIN_CELDAS_PAREADAS`, IC no calculable): la extracción de
  `L` sobre marco-M v1_1 no existe todavía, así que esta mitad de la
  pregunta no tiene insumo para responderse, positiva o negativamente, en
  este acto.
- **¿Cuánto del conocimiento implícito del LLM sobrevive al pasar por la
  disciplina de M?** Con el único corredor medible hoy (`M` contra `R`,
  n=11): **poco, por esta muestra** — proporción en banda **0.0** (IC
  bootstrap **[0.0, 0.0]**), mediana `|z_M|` **16.84** (IC **[14.60,
  202.54]**); ninguna de las 11 celdas de `M` queda dentro de `±0.5·EE(R)`
  de `R`. El IC de la proporción en banda no cruza nada distinto de cero —
  es un `[0.0, 0.0]` genuino sobre las 11 celdas de esta muestra —, así que
  esta mitad sí sostiene una lectura, aunque sigue siendo sobre `M` en
  aislamiento: no dice nada sobre si `L` haría mejor o peor, esa
  comparación es la de arriba (`SIN_CELDAS_PAREADAS`).

## Deriva de

`forense/prereg-duelo-v2/procedimiento-scoring-v1_1.md` (procedimiento
sellado, `ADR-262`) · `forense/prereg-duelo-v2/procedimiento-scoring-v1_0.md`
(banda, contrato F1) · `forense/prereg-duelo-v2/scoring-adv1-m3.py`
(`generar_indices_bootstrap`, `derivar_seed_scope`, patrones
`bootstrap_marginal`/`bootstrap_pareado`) ·
`forense/prereg-duelo-v2/agregado_v1_1.py` (este acto) ·
`forense/prereg-duelo-v2/agregado-v1_1-resultado.json` (salida completa) ·
`milpa/milpa-whitepaper-v0_1.md:207-209` (pregunta doble) ·
`forense/prereg-duelo-v2/runner_l_cli.py:124-143` y
`forense/prereg-duelo-v2/PAQUETE-L-v1_1.md:180` (extractor L pendiente,
hallazgo §0).
