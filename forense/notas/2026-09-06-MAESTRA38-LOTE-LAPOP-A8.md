# `ACTO MAESTRA38-LOTE-LAPOP` · A.8 — `ya_medido.py` sobre los tres `id` que este lote mide

Corrido el 6/sep/2026 desde el worktree del acto, sobre `origin/main = a5350e59`, ANTES de
abrir ningún `.dta`. Salida cruda, sin editar. Las tres specs y su `sha256` verificado:

| spec | `sha256` declarado | recomputado | |
|---|---|---|---|
| `prereg-caja-S4-L4` | `7847e35ab37ef30ba1356c21ad1e151fd92773e7cad80e791cc8eafd2b5ae1ff` | `7847e35ab37ef30ba1356c21ad1e151fd92773e7cad80e791cc8eafd2b5ae1ff` | **COINCIDE** |
| `prereg-caja-S5-L5` | `74816097008b84a14a04d83dbcce850f0bb3644ae34bfe0867ab5d928ded1eb6` | `74816097008b84a14a04d83dbcce850f0bb3644ae34bfe0867ab5d928ded1eb6` | **COINCIDE** |
| `prereg-caja-S8-L18` | `a836582d0d6e3c7e96623b85d89280fd003c2925d4cb9e5602708d8337aa4d20` | `a836582d0d6e3c7e96623b85d89280fd003c2925d4cb9e5602708d8337aa4d20` | **COINCIDE** |

Resumen: `civico.voto.clientelar_si_observable` y `civico.protesta.agravio_urbano` están
**MEDIDA-EN** por `L9`/`L11` (y `L12`) — pero sobre **otro brazo / otro contraste** de la
misma regla, que este lote cita y no reabre (ver §0 de cada nota de resultados).
`comunicacion.inseguridad.ver_oir_callar` es **NUNCA-MEDIDA**: `MAESTRA38-L18` es su primera
falsación real.

---

## `civico.voto.clientelar_si_observable`

```
$ python3 tools/ya_medido.py civico.voto.clientelar_si_observable
=== ya_medido: civico.voto.clientelar_si_observable ===
  resuelto por canon: civico.voto.clientelar_si_observable -> R7.6 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): civico.voto.clientelar_si_observable, R7.6

-- milpa/tramite.yaml --
  (sin apariciones)

-- milpa/tramite-ola5-propuesta-v0.yaml --
  milpa/tramite-ola5-propuesta-v0.yaml:2284  situacion=PENDIENTE-DE-MESA tier=PENDIENTE-DE-MESA veredicto=veredicto_Bbis=CONTRARIA; veredicto_del_acto=> p=0.658228
      id: civico.voto.agencia_lapop2023
  milpa/tramite-ola5-propuesta-v0.yaml:2555  situacion=PENDIENTE-DE-MESA tier=PENDIENTE-DE-MESA veredicto=veredicto_Bbis=CONTRARIA; veredicto_del_acto=> p=0.321633
      id: civico.voto.agencia_con_secreto_encuci2020
  milpa/tramite-ola5-propuesta-v0.yaml:2842  situacion=SELLADA-SIN-CARGA tier=MEDIA veredicto=veredicto_Bbis=NO-APLICA p=0.187641
      id: civico.clientelismo.prevalencia_lista_mps2012
  milpa/tramite-ola5-propuesta-v0.yaml:3059  situacion=SELLADA-SIN-CARGA tier=PENDIENTE-DE-MESA p=0.540795
      id: tramite.gobierno_digital.coercitivo_tabla_de_universos
  milpa/tramite-ola5-propuesta-v0.yaml:3276  situacion=PENDIENTE-DE-MESA tier=PENDIENTE-DE-MESA
      id: civico.voto.clientelar_si_observable_lapop2019

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:762  tier=[MEDIA]
      | `R7.6` | L268 | Proximidad/focalización o monitoreo percibido → autonomía cede localmente | `[MEDIA]` | No |
  canon/modelo-decision-v4_0.md:804  tier=[MEDIA]
      **`FP-298` (firma de mesa, 4/sep/2026, propagada por `ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3`).** Mesa acepta la clasificación con evidencia de `MAESTRA38-N5` sobre las 9 reglas `NO-ENCONTRADO` 

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-02-MAESTRA35-L11-P0-censo.md:49  
      ## §3 · Pieza (b) · `R7.3`/`R7.6` — ENCUCI sí la satisface; Latinobarometro no
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:18  tier=[FUERTE]  [CONTRARIA]
      | (b) | `R7.3`/`R7.6` agencia con secreto | `[FUERTE]`/`[MEDIA]` | ENCUCI 2020 | SECRETO **+6.38 pp** · OBSERVABLE **+11.57 pp** | `[+3.82, +8.89]` · `[+6.57, +16.59]` | **`CONTRARIA`** |
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:28  
      ## §1 · Pieza (b) · `R7.3`/`R7.6` sobre ENCUCI 2020 — la separación vuelve a no aparecer
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:162  
      `R7.3`/`R7.6` (`b`) y `R7.4` (`c`). `R7.7` (`a`) y `R1.5` (`d`) no llegaron a
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:166  tier=[FUERTE]  [CONTRARIA-REPLICADA]
      - **`CONTRARIA-REPLICADA`: 1** (`R7.3`/`R7.6`, contra una `[FUERTE]`).
  forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md:78  
      ## §3 · Pieza (a) — `R7.7`, y el muro entre `R7.3`/`R7.6` y la dádiva
  forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md:94  
      (`agencia_con_secreto`) y `R7.6` (`clientelar_si_observable`) piden el moderador
  forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md:111  
      **Lo que sí queda en pie para `R7.3`/`R7.6`, y por qué es otra cosa.** El
  forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md:116  
      `vb20` (intención de voto en la próxima presidencial, 1 414) el par `R7.3`/`R7.6`
  forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md:199  
      pasan a `COMMIT-1`: **5** — (a) `R7.7`, (a-bis) `R7.3` y `R7.6`, (b) `R7.4`,
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:21  tier=[FUERTE]  [CONTRARIA]
      | (a-bis) | `R7.3` / `R7.6` agencia con secreto | `[FUERTE]` / `[MEDIA]` | SECRETO **+14.37 pp** · OBSERVABLE **+17.98 pp** | `[+1.43, +27.44]` · `[+10.75, +25.02]` | **`CONTRARIA`** |
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:97  
      ## §3 · Pieza (a-bis) · `R7.3`/`R7.6` — la separación que el par afirma no aparece
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:120  
      signo que `R7.6` predice, pero es **pequeña frente a la brecha que ya existe en
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:269  
      3. **`R7.3`/`R7.6` no se miden contra la dádiva** sino contra la transferencia:
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:303  
      - **Reglas del modelo con dato (pendiente sello): 6** — `R7.7`, `R7.3`, `R7.6`,
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:310    [CONTRARIA]
      - **Veredictos `B-bis`:** 2 `CONTRARIA` (`R7.3`/`R7.6` y `R7.8`),
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:27  
      (`ADR-158`). Las otras cuatro (`R7.6`, `R7.7`, `R7.8`, `R1.5`) están **fuera del
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:224  
      ## §3 · Pieza (a-bis) · `R7.3` / `R7.6` — la agencia se conserva con secreto y cede sin él
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:229  
      Es **un solo cruce leído por sus dos ramas**: `R7.3` y `R7.6` son el par
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:265  
      ### 3.1 · Pre-registro `B-bis` de `R7.3` y `R7.6`
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:269  
      | **Signo esperado** | `Δ_SECRETO ≈ 0` (la agencia se conserva: `R7.3`) **y** `Δ_OBSERVABLE > 0` (la agencia cede: `R7.6`), luego `Δ_diferencia > 0` |
  forense/notas/2026-09-03-MAESTRA36-L12-resultados.md:133  
      ## 3 · P2 — R7.3 / R7.6: réplica que **no adjudica**, y que **no reproduce** la lectura preliminar
  forense/notas/2026-09-03-MAESTRA36-L12-resultados.md:143  
      Los dos IC contienen 0. **Ninguno mueve el veredicto de R7.3 ni el de R7.6** —que ya venían con
  forense/notas/2026-09-03-MAESTRA36-L12-resultados.md:228  
      - **R7.3/R7.6: +1** tercer instrumento (`REPLICA-…-NO-SELLADA`, no adjudica).
  forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada-bis-v3.md:125  
      ## §E · P2 (v3) — R7.3/R7.6, no adjudica
  forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada.md:114  
      ## §3 · P2 — R7.3/R7.6 como tercer instrumento, sin sello
  forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada.md:124  
      No mueve el veredicto de R7.3 ni el de R7.6.
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:12  
      Resumen: `civico.voto.clientelar_si_observable` y `civico.protesta.agravio_urbano` están
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:20  
      ## `civico.voto.clientelar_si_observable`
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:23  
      $ python3 tools/ya_medido.py civico.voto.clientelar_si_observable
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-L4-resultados.md:1  
      # `ACTO MAESTRA38-L4` · `civico.voto.clientelar_si_observable` (`R7.6`) sobre LAPOP México 2019 — resultados
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-L4-resultados.md:13  
      `python3 tools/ya_medido.py civico.voto.clientelar_si_observable` → **`MEDIDA-EN: L11, L12, L9, S4`**
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-L4-resultados.md:150  tier=[MEDIA]
      No mueve el tier de `civico.voto.clientelar_si_observable` (`[MEDIA]`, `modelo-decision-v4_0.md:554`)

-- forense/prereg-caja/S*-spec-*.md --
  forense/prereg-caja/S2-L2-spec-v1_0.md:9  
      > | **QUÉ ES** | Dos ramas congeladas del futuro acto que abre el microdato de primera mano de ICPSR 35024 (`35024-0001-Data.dta`): **MEDICIÓN** (variables, ponderador, universo, dicotomizaciones, cel
  forense/prereg-caja/S2-L2-spec-v1_0.md:10  
      > | **QUÉ NO ES** | No abre el `.dta`. No abre el codebook/cuestionario (ambos registrados en manifiesto, físicamente ausentes de esta sesión NUBE). No mueve el tier de `R7.3`/`R7.6`. No decide cuál r
  forense/prereg-caja/S2-L2-spec-v1_0.md:22  tier=[MEDIA]
      > `R7.6` · L268 · *Proximidad/focalización o monitoreo percibido → autonomía cede localmente* · tier `[MEDIA]` · **no tiene ficha hitoD** — sólo aparece definida en `modelo-decision-v4_0.md:762` y ope
  forense/prereg-caja/S2-L2-spec-v1_0.md:49  
      ### 1.1 · Variables por número de ítem — `R7.3`/`R7.6`
  forense/prereg-caja/S2-L2-spec-v1_0.md:56  
      | **R7.6** | T4 | `W2_P40` (condicionaron el programa: sí/no) | `W2_P8` | `W2_P36C` |
  forense/prereg-caja/S2-L2-spec-v1_0.md:76  
      - **Celdas:** 4 (una por nivel de `W2_P36C`) por cada una de T3 y T4 — 8 celdas totales para la rama R7.3/R7.6, más las 2 celdas del contraste lista-vs-directa (ronda 1 y ronda 2) para el experimento 
  forense/prereg-caja/S2-L2-spec-v1_0.md:104  
      | **T4** | `W2_P40`×`W2_P8`, control `W2_P36C` | **R7.6** (§1.1) | NO ENCONTRADO — solo paráfrasis ("condicionaron el programa") |
  forense/prereg-caja/S2-L2-spec-v1_0.md:115  
      2. **Prioridad 2 — T3/T4 (R7.3/R7.6).** Leer el wording de `W2_P39B`, `W2_P40`, `W2_P36C`, `W2_P8` — no bloquea la ejecución de MEDICIÓN (el diseño no depende de un supuesto de composición como T5), p
  forense/prereg-caja/S2-L2-spec-v1_0.md:116  
      3. **Prioridad 3 — T9a.** Confirmar si «en mi comunidad los políticos compran votos» es cita literal de `W2_P36D` o paráfrasis — no bloquea R7.3/R7.6/lista, pero corrige la tabla de §2.1 para el sigui
  forense/prereg-caja/S2-L2-spec-v1_0.md:125  
      2. **MEDICIÓN §1.1 (R7.3/R7.6, T3/T4) puede correr en paralelo o después de TEXTO prioridad 1** — no depende de su resultado, sólo de TEXTO §2.2 prioridad 2 para anotar la calidad de la medición, no p
  forense/prereg-caja/S2-L2-spec-v1_0.md:132  
      No abre el `.dta` ni el codebook — ambos están fuera de esta sesión (NUBE, sin corpus). No calcula ningún IC95, ningún `Δ`, ninguna celda. No mueve el tier de `R7.3`/`R7.6`. No cierra `FP-263` (el suc
  forense/prereg-caja/S4-L4-spec-v1_0.md:1  
      # S4 · Pre-registro de `civico.voto.clientelar_si_observable` — reformulada (objeto de `N5 §2.6`)
  forense/prereg-caja/S4-L4-spec-v1_0.md:9  
      > | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`, de una pieza **NUEVA** de falsación de `civico.voto.clientelar_si_observable` sobre LAPOP México 2019 (exposición a oferta client
  forense/prereg-caja/S4-L4-spec-v1_0.md:10  tier=[MEDIA]
      > | **QUÉ NO ES** | No abre ningún `.dta`, `.sav` ni codebook — los cuatro payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna cel
  forense/prereg-caja/S4-L4-spec-v1_0.md:23  tier=[MEDIA]
      > *SI hay **proximidad/focalización del reparto** O el votante **percibe que su voto puede ser monitoreado** ENTONCES **la autonomía CEDE localmente** — PORQUE cálculo racional bajo incertidumbre sobr
  forense/prereg-caja/S4-L4-spec-v1_0.md:35  
      **Lo que ni el encargo ni `N5` citan, y que existe en el árbol desde el 2/sep/2026** (verificado con `git log`, ambos commits anteriores a `N5` y a este encargo): `forense/notas/2026-09-02-MAESTRA35-L
  forense/prereg-caja/S4-L4-spec-v1_0.md:42  tier=[FUERTE]
      **Corrección post-merge (`PR #536`, tras `origin/main` = `7c04069`, `PR #535`/`ACTO MAESTRA38-N6`).** El primer sello de esta pieza citaba las dos corridas como `PENDIENTE-DE-MESA` en `FP-298` `ABIERT
  forense/prereg-caja/S4-L4-spec-v1_0.md:44  
      **Consecuencia para este pre-registro, declarada antes de escribir una celda:** este acto **no es la primera medición** de `civico.voto.clientelar_si_observable`. Es una **segunda pieza, deliberadamen
  forense/prereg-caja/S4-L4-spec-v1_0.md:165    [CONTRARIA-REPLICADA]
      No abre ningún archivo de §6. No calcula `Δ_elección` ni ningún IC95. No mueve el tier de `civico.voto.clientelar_si_observable` ni el de `civico.voto.agencia_con_secreto`. `FP-298` ya está `EJECUTADA

-- canon/registro-rotulos.tsv (alias) --
  canon/registro-rotulos.tsv:140  
      L	MAESTRA35-L9
  canon/registro-rotulos.tsv:141    [CONTRARIA-REPLICADA]
      L	MAESTRA35-L11
  canon/registro-rotulos.tsv:146    [CONTRARIA-REPLICADA]
      L	MAESTRA36-L12
  canon/registro-rotulos.tsv:170  
      N	MAESTRA38-N9

========================================
MEDIDA-EN: L11, L12, L9, S4
```

---

## `civico.protesta.agravio_urbano`

```
$ python3 tools/ya_medido.py civico.protesta.agravio_urbano
=== ya_medido: civico.protesta.agravio_urbano ===
  resuelto por canon: civico.protesta.agravio_urbano -> R7.4 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): civico.protesta.agravio_urbano, R7.4

-- milpa/tramite.yaml --
  milpa/tramite.yaml:1212  situacion=SELLADA tier=FUERTE veredicto=veredicto_Bbis=NO-DISCRIMINA,; veredicto_Bbis=CORROBORADA, p=0.112192
      id: civico.protesta.agravio_urbano_encuci2020

-- milpa/tramite-ola5-propuesta-v0.yaml --
  milpa/tramite-ola5-propuesta-v0.yaml:2356  situacion=SELLADA-SIN-CARGA tier=MEDIA veredicto=veredicto_Bbis=CORROBORADA}; veredicto_Bbis=CORROBORADA-PARCIAL; veredicto_del_acto=> p=0.105727
      id: civico.protesta.agravio_urbano_lapop2019
  milpa/tramite-ola5-propuesta-v0.yaml:2623  situacion=CARGADA-A-MOTOR tier=FUERTE veredicto=veredicto_Bbis=NO-DISCRIMINA}; veredicto_Bbis=CORROBORADA}; veredicto_Bbis=CORROBORADA-PARCIAL p=0.112192
      id: civico.protesta.agravio_urbano_encuci2020
  milpa/tramite-ola5-propuesta-v0.yaml:3059  situacion=SELLADA-SIN-CARGA tier=PENDIENTE-DE-MESA p=0.540795
      id: tramite.gobierno_digital.coercitivo_tabla_de_universos
  milpa/tramite-ola5-propuesta-v0.yaml:3306  situacion=PENDIENTE-DE-MESA tier=PENDIENTE-DE-MESA
      id: civico.protesta.agravio_urbano_multiola

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:704  tier=[MEDIA]
      - **49 reglas** *(42 en v2 · 43 en v2.1 por conf.07 · 44 en v2.3 al partir la diagonal)*. **Hito D (perímetro de 27 reglas, subconjunto de las 49): 26 de 27 corridas archivadas**<!-- T20:HITO-D pob=re
  canon/modelo-decision-v4_0.md:725  tier=[MEDIA]
      **Registro congelado de IDs *(v3.3, cambio 35)*.** El esquema anterior derivaba el ID de (posición, tier): las 24 fichas de `hitoD-preregistro` numeran secuencialmente solo entre reglas de perímetro, 
  canon/modelo-decision-v4_0.md:766  tier=[MEDIA-FUERTE]
      | `R7.4` | L272 | Agravio + falla estatal + red previa + entorno urbano → protesta | `[MEDIA-FUERTE]` | Sí |
  canon/modelo-decision-v4_0.md:804  tier=[MEDIA]
      **`FP-298` (firma de mesa, 4/sep/2026, propagada por `ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3`).** Mesa acepta la clasificación con evidencia de `MAESTRA38-N5` sobre las 9 reglas `NO-ENCONTRADO` 

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-02-MAESTRA35-L11-P0-censo.md:85  
      ## §4 · Pieza (c) · `R7.4` — ENCUCI la satisface con dos sustituciones; Latinobarometro no
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:19  tier=[MEDIA-FUERTE]  [CORROBORADA-PARCIAL]
      | (c) | `R7.4` protesta y agravio urbano | `[MEDIA-FUERTE]` | ENCUCI 2020 | `C1` +2.03 pp (contiene 0) · `C2` **+3.72 pp** | `[−0.18, +4.12]` · `[+2.22, +5.22]` | **`CORROBORADA-PARCIAL`** |
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:87  
      ## §2 · Pieza (c) · `R7.4` sobre ENCUCI 2020 — el corazón de la regla sigue sin discriminar, y la mitad urbana vuelve a corroborar
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:114  
      celda rural-agravio, contra 65 en LAPOP), y el punto va en el signo que `R7.4`
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:135  tier=[MEDIA-FUERTE]
      la regla de sello de mesa, `R7.4` es `[MEDIA-FUERTE]` y su sub-claim de entorno
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:140  
      mismo signo, ninguno lo prueba. `R7.4` sigue **acotada**, no cerrada, en su
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:162  
      `R7.3`/`R7.6` (`b`) y `R7.4` (`c`). `R7.7` (`a`) y `R1.5` (`d`) no llegaron a
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:167    [AMBIGUA-ENTRE-INSTRUMENTOS]
      - **`AMBIGUA-ENTRE-INSTRUMENTOS`: 1** (el corazón de `R7.4`, contraste
  forense/notas/2026-09-02-MAESTRA35-L11-resultados.md:170    [CORROBORADA-REPLICADA]
      - **`CORROBORADA-REPLICADA` (sub-claim): 1** (`C2` de `R7.4`, agravio dentro
  forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md:127  tier=[MEDIA-FUERTE]
      **(b) `R7.4 · civico.protesta.agravio_urbano` `[MEDIA-FUERTE]`** —
  forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md:199  
      pasan a `COMMIT-1`: **5** — (a) `R7.7`, (a-bis) `R7.3` y `R7.6`, (b) `R7.4`,
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:22  tier=[MEDIA-FUERTE]  [CORROBORADA-PARCIAL]
      | (b) | `R7.4` protesta y agravio urbano | `[MEDIA-FUERTE]` | `C1` **NO-ESTIMABLE** · `C2` **+5.60 pp** | — · `[+2.32, +8.96]` | **`CORROBORADA-PARCIAL`** |
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:143  
      ## §4 · Pieza (b) · `R7.4` — el corazón de la regla no se midió, y estaba previsto
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:162  
      de delito contra 4.97 % entre no víctimas. Pero `R7.4` afirma que **el entorno
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:304  
      `R7.4`, `R7.8`, `R1.5`. Las seis que el encargo nombraba. Ninguna se carga al
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:311    [CORROBORADA-PARCIAL]
      1 `CORROBORADA-PARCIAL` (`R7.4`), 2 `NO-DISCRIMINA` (`R7.7`, `R1.5`).
  forense/notas/2026-09-02-MAESTRA35-L9-resultados.md:318  
      instrucciones. No reabrió las filas `C` de `R7.3` ni `D` de `R7.4`.
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:26  
      `R7.3` está archivada en fila **`C`** (`ADR-155`) y `R7.4` en fila **`D`**
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:37  
      - El `D` de `R7.4` dice que **ninguna de las tres fuentes de EVENTO** adquiridas
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:283  
      ## §4 · Pieza (b) · `R7.4` — protesta, agravio y entorno urbano
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:312  
      trae. Mide **dos de cuatro**: agravio y entorno. Acota `R7.4`; no la cierra.
  forense/notas/2026-09-02-MAESTRA35-L9-spec.md:314  
      ### 4.1 · Pre-registro `B-bis` de `R7.4`
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:12  
      Resumen: `civico.voto.clientelar_si_observable` y `civico.protesta.agravio_urbano` están
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:57  
      `R7.3`/`R7.6` (`b`) y `R7.4` (`c`). `R7.7` (`a`) y `R1.5` (`d`) no llegaron a
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:69  
      pasan a `COMMIT-1`: **5** — (a) `R7.7`, (a-bis) `R7.3` y `R7.6`, (b) `R7.4`,
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:105  
      Resumen: `civico.voto.clientelar_si_observable` y `civico.protesta.agravio_urbano` están
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:173  
      ## `civico.protesta.agravio_urbano`
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:176  
      $ python3 tools/ya_medido.py civico.protesta.agravio_urbano

-- forense/prereg-caja/S*-spec-*.md --
  forense/prereg-caja/S5-L5-spec-v1_0.md:1  
      # S5 · Pre-registro de `civico.protesta.agravio_urbano` — reformulada (objeto de `N5 §2.8`)
  forense/prereg-caja/S5-L5-spec-v1_0.md:9  
      > | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`, de una pieza **multi-ola** que mide los **cuatro** antecedentes del `SI` de `civico.protesta.agravio_urbano` — agravio, falla est
  forense/prereg-caja/S5-L5-spec-v1_0.md:10  tier=[MEDIA-FUERTE]
      > | **QUÉ NO ES** | No abre ningún `.dta`/`.sav` — los diez payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve el
  forense/prereg-caja/S5-L5-spec-v1_0.md:23  tier=[MEDIA-FUERTE]
      > *SI hay **agravio personal/familiar + falla estatal palpable + red previa** Y el entorno es **urbano con espacio público disponible** ENTONCES se suma a **protesta** (8M: mujeres jóvenes urbanas; co
  forense/prereg-caja/S5-L5-spec-v1_0.md:35  
      `forense/notas/2026-09-02-MAESTRA35-L9-spec.md §4` y `-resultados.md §4`, más `forense/notas/2026-09-02-MAESTRA35-L11-P0-censo.md`/`-resultados.md §2`, ya pre-registraron y **corrieron** un diseño 2×2
  forense/prereg-caja/S5-L5-spec-v1_0.md:42  situacion=CARGADA-A-MOTOR`, tier=FUERTE`,  [CORROBORADA-REPLICADA]
      **Corrección post-merge (`PR #536`, tras `origin/main` = `7c04069`, `PR #535`/`ACTO MAESTRA38-N6`).** El primer sello de esta pieza citaba las dos corridas como `PENDIENTE-DE-MESA` (`FP-298`, `ABIERTA
  forense/prereg-caja/S5-L5-spec-v1_0.md:192  tier=[FUERTE]
      No abre ningún archivo de §6. No calcula ninguna celda ni IC95. No mueve el tier de `civico.protesta.agravio_urbano`, ni el de `civico.protesta.agravio_urbano_encuci2020` (`[FUERTE]`, `CARGADA-A-MOTOR
  forense/prereg-caja/S8-L18-spec-v1_0.md:114  
      **Los tres proxies del antecedente se tratan como operacionalizaciones alternativas de un mismo constructo** —"contexto de inseguridad/autoridad no confiable"—, no como antecedentes conjuntos que deba

-- canon/registro-rotulos.tsv (alias) --
  canon/registro-rotulos.tsv:140  
      L	MAESTRA35-L9
  canon/registro-rotulos.tsv:141    [CONTRARIA-REPLICADA]
      L	MAESTRA35-L11
  canon/registro-rotulos.tsv:170  
      N	MAESTRA38-N9

========================================
MEDIDA-EN: L11, L9, S5
```

---

## `comunicacion.inseguridad.ver_oir_callar`

```
$ python3 tools/ya_medido.py comunicacion.inseguridad.ver_oir_callar
=== ya_medido: comunicacion.inseguridad.ver_oir_callar ===
  resuelto por canon: comunicacion.inseguridad.ver_oir_callar -> R10.3 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): comunicacion.inseguridad.ver_oir_callar, R10.3

-- milpa/tramite.yaml --
  (sin apariciones)

-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:727  
      **Decisión: los IDs son un registro CONGELADO, no una fórmula.** (a) Los **24 IDs ya usados en fichas** (`R1.1`–`R10.3`, ver `hitoD-preregistro`) quedan exactamente como están; nunca se recomputan. (b
  canon/modelo-decision-v4_0.md:778  tier=[FUERTE]
      | `R10.3` | L299 | Inseguridad/autoridad no confiable → "ver, oír y callar" | `[FUERTE]` | Sí |

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-03-MAESTRA37-L1-censo.md:96  
      - `comunicacion.inseguridad.ver_oir_callar`: `--regex "(no denuncio\|por miedo).{0,35}(represalia\|autoridad\|denunciar)"` · `--regex "denunci\w+"` · `--regex "no dijo nada\|prefirio callar\|guardar s
  forense/notas/2026-09-03-MAESTRA37-L1-remapeo.md:60  
      | `comunicacion.inseguridad.ver_oir_callar` | 0·9·0 | **EXISTE-NO-SATISFACE como máximo**, no verificado |
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:15  
      `comunicacion.inseguridad.ver_oir_callar` es **NUNCA-MEDIDA**: `MAESTRA38-L18` es su primera
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:295  
      ## `comunicacion.inseguridad.ver_oir_callar`
  forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md:298  
      $ python3 tools/ya_medido.py comunicacion.inseguridad.ver_oir_callar

-- forense/prereg-caja/S*-spec-*.md --
  forense/prereg-caja/S6-L16-spec-v1_0.md:202  tier=[MEDIA]
      No abre ningún archivo de §6. No calcula ninguna celda ni IC95. No mueve el tier de `salud.atencion.grave` (`[MEDIA]`, línea 527) ni sella `MEDIBLE-COMO-ESTÁ`. No decide cuál de las dos ramas (`ENNVIH
  forense/prereg-caja/S7-L17-spec-v1_0.md:179  tier=[FUERTE]
      No abre ningún archivo de §6. No calcula ninguna celda, proporción ni IC95. No mueve el tier de `salud.vacunacion.disponible` (`[FUERTE]`, línea 575) ni sella `MEDIBLE-COMO-ESTÁ`. No corrige el domini
  forense/prereg-caja/S8-L18-spec-v1_0.md:1  
      # S8 · Pre-registro de `comunicacion.inseguridad.ver_oir_callar` — medible como está (hallazgo nuevo de `N10`)
  forense/prereg-caja/S8-L18-spec-v1_0.md:9  
      > | **QUÉ ES** | Pre-registro, congelado antes de abrir ningún `.dta`/`.sav`, de un falsador **de una sola ola (LAPOP México 2004)** para `comunicacion.inseguridad.ver_oir_callar` (`R10.3`): contexto 
  forense/prereg-caja/S8-L18-spec-v1_0.md:10  tier=[FUERTE]
      > | **QUÉ NO ES** | No abre ningún `.dta`/`.sav` — los payloads de §6 están fuera de esta sesión (NUBE, sin corpus montado). No calcula ninguna proporción, ningún IC95, ninguna celda. No mueve el tier
  forense/prereg-caja/S8-L18-spec-v1_0.md:23  tier=[FUERTE]
      > *SI el contexto es de inseguridad/autoridad no confiable ENTONCES "ver, oír y callar" — PORQUE G4 (adaptación racional, no timidez) — `[FUERTE]`.* · **id:** `comunicacion.inseguridad.ver_oir_callar`
  forense/prereg-caja/S8-L18-spec-v1_0.md:28  
      $ python3 tools/ya_medido.py comunicacion.inseguridad.ver_oir_callar
  forense/prereg-caja/S8-L18-spec-v1_0.md:29  
      === ya_medido: comunicacion.inseguridad.ver_oir_callar ===
  forense/prereg-caja/S8-L18-spec-v1_0.md:30  
      resuelto por canon: comunicacion.inseguridad.ver_oir_callar -> R10.3
  forense/prereg-caja/S8-L18-spec-v1_0.md:33  
      -- canon/modelo-decision-v4_0.md §7 -- R10.3 | L299 | ... | [FUERTE] | Sí
  forense/prereg-caja/S8-L18-spec-v1_0.md:195  tier=[FUERTE]
      No abre ningún archivo de §6. No calcula ninguna celda ni IC95. No mueve el tier de `comunicacion.inseguridad.ver_oir_callar` (`[FUERTE]`, línea 585) ni sella la clasificación `MEDIBLE-COMO-ESTÁ` que 

-- canon/registro-rotulos.tsv (alias) --
  canon/registro-rotulos.tsv:173  
      N	MAESTRA38-N11

========================================
NUNCA-MEDIDA
```

