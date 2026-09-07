# Benchmark de motores comparables (L / M / R) — corredores del duelo adversarial

### `benchmark-motores-comparables` · **v1.2** · 7 de septiembre de 2026 · archivo canónico único, versión en la primera línea del cuerpo

> | | |
> |---|---|
> | **ARCHIVO** | `forense/benchmark/BENCHMARK-MOTORES-COMPARABLES.md` |
> | **NOMBRE ESTABLE** | **`benchmark-motores-comparables`** — cítalo así, nunca por nombre de archivo |
> | **REEMPLAZA A** | Nada en este repo. `ACTO MAESTRA38-TRAMITE-5` buscó un borrador de mesa "benchmark v1.2" (`find . -iname "*benchmark*v1_2*" -o -iname "*agregado*v1_2*"`) y **no encontró prosa alguna** — el único artefacto v1.2 en el árbol es el resultado numérico `forense/prereg-duelo-v2/agregado-v1_2-resultado.json` y su script `agregado_v1_2.py`. Tampoco existen `v1.0`/`v1.1` de un "benchmark de motores" en el repo (mismo `find`, 0 resultados) — si existieron en mesa, viven fuera de este árbol y no fue posible incluirlos ni moverlos a `forense/historico/`. Este documento **no es una transcripción** de ese borrador ausente: es una reconstrucción hecha únicamente de cifras verificables por `grep`/lectura directa en este repo (`agregado-v1_2-resultado.json`, `procedimiento-scoring-v1_1.md` sellado, `canon/modelo-decision-v4_0.md`, `forense/tablero/TABLERO-PROGRAMA.md`). Donde una cifra del encargo de dirección no se pudo verificar, se declara ausente en vez de inventarse (D-13). |
> | **QUÉ ES** | El estado, a `origin/main` de este acto, de la comparación entre los tres corredores medibles del duelo adversarial — `L` (extracción de literatura/LLM), `M` (motor de 49 reglas) y `R` (regla/referencia) — tal como los deja `agregado_v1_2.py` sobre el marco-M-sorteado de 14 celdas. No es un benchmark de "modelos de lenguaje" en el sentido de la industria: es el benchmark interno del programa entre sus propios tres mecanismos de estimación. |
> | **QUÉ NO ES** | No sella ningún veredicto nuevo, no mueve ningún tier de `canon/modelo-decision-v4_0.md`, no cambia `procedimiento-scoring-v1_1.md` (sellado, `ADR-262`, intocado). No mide México — es meta-medición del propio motor. No es el benchmark que dirección tenía en mesa (ver `REEMPLAZA A`): es lo que este repo puede sostener con evidencia hoy. |
> | **VERIFICAS ASÍ** | `python3 -c "import json; d=json.load(open('forense/prereg-duelo-v2/agregado-v1_2-resultado.json')); print(d['comparacion_principal_pareada']['veredicto'], d['version_marco'])"` → `INDETERMINADO v1_2`. `grep -c "^## Dominio" data/INFRAESTRUCTURA-v1_0.md` → `9` (infraestructura vigente citada en §5). |

**Acto:** `ACTO MAESTRA38-TRAMITE-5`, 7/sep/2026, entorno **NUBE sin corpus** (sesión sin `data/raw` montada, verificado — `ls data/raw` → `No such file or directory`).

---

## 0 · Qué se buscó y qué no se encontró (declarado antes de construir nada)

Búsqueda ejecutada antes de escribir este documento:

```
$ find . -iname "*benchmark*v1_2*" -o -iname "*agregado*v1_2*"
./forense/prereg-duelo-v2/agregado-v1_2-resultado.json
./forense/prereg-duelo-v2/agregado_v1_2.py
```

Cero archivos de prosa "benchmark" con "v1.2" en el nombre o contenido. Búsqueda secundaria sobre benchmarks existentes en `forense/` (`BENCHMARK-INTERVALO-CORREDOR-M-2026-08-20.md`, `BENCHMARK-R51D3-hogares-mixtos-2026-08-18.md`, `BENCHMARK-conf02-policronia-2026-08-17.md`, `BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md`, `BENCHMARKS-metodologicos-D-ABC.md`) — ninguno se llama ni se versiona "v1.2", ninguno es el benchmark de motores comparables que el encargo de dirección describe (son benchmarks temáticos de reglas individuales, no del propio motor). **Conclusión:** el "benchmark v1.2" que dirección tenía en mesa (`SELLO-2`, cabecera: *"2. benchmark… y qué necesitaríamos para moverlo"*, §B) nunca llegó a este repo en prosa — mismo patrón que `TABLERO-PROGRAMA-v1_5.md` (`FP-327`) y que el `## CONSUMIDO` de `MAESTRA38-SELLO-2`, que declaró su "Bloque B" de benchmark **no ejecutado**. Este documento se construye desde cero, con la versión `v1.2` fijada porque es la versión real del artefacto numérico que sí existe (`agregado-v1_2-resultado.json`, `version_marco: "v1_2"`).

---

## 1 · Los tres corredores — qué mide cada uno, verificado contra el script sellado

`forense/prereg-duelo-v2/procedimiento-scoring-v1_1.md` (**SELLADO**, `ADR-262`, `ACTO MAESTRA33-E12 · SELLA-1`, 1/sep/2026) fija, entre cinco decisiones de mesa (firma verbatim citada en su propia cabecera): unidades `z = dif/EE(R)`; agregado por corredor con bootstrap `seed=42`/`IC=0.95`; comparación principal `L_SOLO_vs_M` pareada; baseline `B` NO-APLICA a `marco-M`; `F-DD` fuera del agregado y del pareado.

| corredor | qué es | fuente en este repo |
|---|---|---|
| `L_SOLO` | Extracción de literatura/LLM, aislada (sin corpus del programa) | `corridas-L/`, extractor `tools/extrae_l_v1_1.py` |
| `L_CORPUS` | La misma extracción, con acceso al corpus del programa (diagnóstico secundario, no la comparación principal) | mismo extractor, universo con corpus |
| `M` | El motor de reglas del programa — 49 reglas (`canon/modelo-decision-v4_0.md:723`, *"49 reglas (42 en v2 · 43 en v2.1 por conf.07 · 44 en v2.3…)"*), Hito D con 26 de 27 corridas archivadas | `corridas-R/`, `scoring-adv1-m3.py` |
| `R` | Regla/referencia — el valor contra el que `z` se calcula (`EE_R`) | `corridas-R/<id>.json`, `estado="COMPUTADO"` |
| `B` (baseline) | Declarado explícitamente **NO-APLICA** a `marco-M` (procedimiento §2, `_corredor-B.json` es el único archivo del corredor `B`, poblado para el marco piloto de 15 celdas, no para `marco-M-sorteado`) | `forense/prereg-duelo-v2/corridas-R/_corredor-B.json` |

`B` no entra a este benchmark: el propio procedimiento sellado lo excluye para este marco. El benchmark real de tres vías es `L_SOLO` / `L_CORPUS` / `M`, contra `R` como referencia.

---

## 2 · Resultado v1.2 — universo, comparación principal, veredicto

Fuente única: `forense/prereg-duelo-v2/agregado-v1_2-resultado.json` (script `agregado_v1_2.py`, que reutiliza `_bootstrap_pareado_z`/`_adjudicar` de `agregado_v1_1.py` sin editarlo, per su propia `nota`). Parámetros sellados: `delta=0.5`, `nivel_ic=0.95`, `replicas=10000`, `seed=42`.

**Universo:** 14 celdas (`universo_11`, nombre heredado de v1.1 cuando eran 11 — el propio archivo declara, en `tra_m_02_informativo.nota_v1_2`, que en v1.2 `TRA-M-02` entró al universo de 14 y el bloque `tra_m_02_informativo` quedó vestigial). Las 14: `CIV-M-01, CIV-M-02, CIV-M-04, CIV-M-10, CIV-M-12, CIV-M-13, DIN-M-01, FAM-M-01, FAM-M-05, FAM-M-06, FAM-M-07, TRA-M-02, TRA-M-03, TRA-M-07`.

**Comparación principal (`comparacion_principal_pareada`, `L_SOLO_vs_M`, 13 celdas pareadas — `CIV-M-04` sin valor `L_solo`, excluida del pareo):**

| | punto | IC95 | veredicto |
|---|---|---|---|
| `L_SOLO_vs_M` | −28.99 | [−74.02, +9.40] | **INDETERMINADO** |

El IC95 cruza 0 — el motor `M` y el corredor `L_SOLO` **no se distinguen con la evidencia actual**. No es un empate declarado por diseño: es un intervalo que no excluye la paridad.

**Comparación secundaria (`comparacion_secundaria_l_corpus_vs_m`, diagnóstico, no gating — 14 celdas pareadas):**

| | punto | IC95 | veredicto |
|---|---|---|---|
| `L_CORPUS_vs_M` | −13.09 | [−59.70, +27.05] | **INDETERMINADO** |

Misma conclusión: ningún corredor gana con el intervalo actual.

**Agregado marginal por corredor (`agregado_marginal_por_corredor`, proporción en banda + mediana de `|z|`, no pareado):**

| corredor | n celdas | mediana `|z|` (punto) | mediana `|z|` IC95 | proporción en banda (punto) |
|---|---|---|---|---|
| `L_CORPUS` | 14 | 29.19 | [6.25, 53.57] | 0.071 |
| `L_SOLO` | 13 | 11.16 | [3.55, 34.12] | 0.000 |
| `M` | 14 | 11.43 | [3.99, 18.72] | 0.000 |

`M` y `L_SOLO` tienen medianas de `|z|` muy próximas (11.43 vs 11.16) — consistente con el `INDETERMINADO` de la comparación pareada. `L_CORPUS` es el corredor con mayor `|z|` mediano (peor ajuste a `R` en esta métrica), pero con el `IC` más ancho también. **Ninguno de los tres corredores tiene una celda dentro de banda salvo `L_CORPUS` (1 de 14, 7.1%)** — con `delta=0.5` (la banda sellada), casi ninguna celda de ningún corredor cae "dentro".

---

## 3 · `M` constante dentro de `CIV` — hallazgo verificado, base de la fila `D1` del tablero

Verificado directamente sobre `celdas` de `agregado-v1_2-resultado.json` (no re-derivado, solo leído):

| celda | `M` |
|---|---|
| `CIV-M-01` | 0.294313 |
| `CIV-M-02` | 0.294313 |
| `CIV-M-04` | 0.294313 |
| `CIV-M-10` | 0.294313 |
| `CIV-M-12` | 0.294313 |
| `CIV-M-13` | 0.294313 |

**Las seis celdas del dominio `CIV` en el universo de 14 tienen el mismo valor de `M`, byte a byte, hasta el sexto decimal.** No es una casualidad de redondeo: es el mismo número repetido seis veces. Otros dominios no son igual de planos: `TRA-M-*` (3 celdas) también repite un único valor (`0.62`) las tres veces; `FAM-M-*` (4 celdas) **no** es constante (`FAM-M-01=0.457707` frente a `FAM-M-05/06/07=0.045694`, las tres últimas sí idénticas entre sí); `DIN-M-01` es una sola celda, no comparable consigo misma.

**Lo que esto dice, sin interpretar de más:** dentro de `CIV`, el motor `M` no varía por celda — el mismo punto se repite para seis reglas distintas del dominio cívico. Esto es consistente con (aunque este documento no lo prueba) que `M` esté devolviendo un valor agregado a nivel de dominio, no una estimación por regla, para `CIV` específicamente. Verificar la causa (¿bug de agregación? ¿es el diseño correcto y las seis reglas comparten de verdad el mismo estimando?) queda fuera del perímetro de este benchmark — es la pregunta que la fila `D1` del tablero (§5) deja abierta.

---

## 4 · `D4` — métrica secundaria, procedimiento-scoring v1.2

El procedimiento sellado (`procedimiento-scoring-v1_1.md`) fija una sola métrica de contraste: `z = dif/EE(R)`, con banda de `delta=0.5`. §2 de este documento ya muestra que, con esa métrica, casi ninguna celda de ningún corredor cae dentro de banda (0-7% según corredor) — la métrica actual es exigente hasta el punto de que la "proporción en banda" no distingue corredores de forma útil (0.000 para dos de los tres). Esto es lo que motiva la pregunta que el tablero registra como `D4` (§5): si una `v1.2` del procedimiento de scoring debería sumar una métrica secundaria (puntos porcentuales de diferencia absoluta, o Brier si el estimando es una probabilidad) que sí discrimine entre corredores cuando `z`/banda no lo hace. Este documento **no decide** esa pregunta — la deja registrada para firma de mesa, con la evidencia numérica de §2 como motivación verificable.

---

## 5 · Decisiones para mesa (numeración propia de este documento — `D1`-`D4`, no la del tablero)

**Aclaración de colisión de rótulo.** `forense/tablero/TABLERO-PROGRAMA.md` ya tiene, desde antes de este acto, una tabla de **discrepancias** con filas rotuladas `D1`/`D3`/`D4` (línea 209 en adelante: `D1` = "canon de estado era de la era Hito D", `D4` = "README en cifras de julio") — tema completamente distinto (defectos de documentación, no decisiones de benchmark). Las `D1`/`D4` de esta sección son **numeración propia de este benchmark**, sin relación con esas filas; el §6 del tablero las registra en una sección nueva, separada de la tabla de discrepancias, para no colisionar.

- **`D1` — ¿se abre un corredor `P` nuevo?** **NO POR AHORA.** Motivo verificable (§3): `M` es constante dentro de `CIV` (seis celdas, un solo valor). Mientras eso sea cierto, un corredor adicional que compare contra `M` heredaría la misma falta de variación dentro de ese dominio — no aporta señal nueva ahí. Se reabre cuando `M` deje de ser constante dentro de `CIV` (es decir, cuando el motor produzca valores distintos por regla en ese dominio, o cuando se confirme que la constancia es el diseño correcto y no un defecto de agregación).
- **`D2`/`D3`** — no se derivan cifras verificables en este acto para llenarlas; quedan sin contenido (el encargo de dirección solo citó `D1` y `D4` explícitamente). No se inventan.
- **`D4` — ¿procedimiento-scoring gana una métrica secundaria en v1.2?** **ABIERTA, firma de mesa.** Candidatas, con base en §4: diferencia en puntos porcentuales (si el estimando es una proporción, como lo son las 14 celdas del universo actual) o Brier (si se trata como probabilidad). No se elige aquí cuál — es decisión de mesa, no de este documento.

---

## 6 · Qué NO hace este documento

No sella ningún ADR. No modifica `procedimiento-scoring-v1_1.md` (sellado, intocado). No corre `agregado_v1_2.py` de nuevo — lee su resultado ya escrito. No abre ningún microdato. No mueve ningún tier de `canon/modelo-decision-v4_0.md`. No decide `D1`/`D4` (§5) — las deja para firma de mesa. No es el benchmark verbatim de dirección (§0) — es su reconstrucción verificable.

---

## v1.3 — enlace re-sellado (TRA-M-02/03/07) + métrica secundaria D4 resuelta (`ACTO MAESTRA38-M13`)

Sección nueva, `append`. El cuerpo `v1.2` de arriba (§0-§5) **no se edita**
— sigue describiendo exactamente lo que describía: la corrida sobre
`marco-M-sorteado-v1_2.tsv` con el enlace v1.0 (`TRA-M-02/03/07` leyendo
`paga_mordida` ASIGNADO, `p=0.62`). Esta sección describe la corrida
`v1.3`, sobre `marco-M-sorteado-v1_3.tsv` (`enlace-M-v1_1.md`), con
`procedimiento-scoring-v1_2.md` (§7, métrica secundaria D4).

### Qué cambió y qué no

`enlace-M-v1_1.md` re-apunta **solo** `TRA-M-02`/`TRA-M-03`/`TRA-M-07` de
`paga_mordida` (`ASIGNADO`, `p=0.62`) a `paga_mordida_encig2025`
(`MEDIDO·p(tasa base ponderada)`, `p=0.085118`) — la enmienda firmada por
DM (1/sep/2026, `ADR-270`/`ADR-276`) que el motor ya traía y el enlace
v1.0 no leía (`diagnostico-14-celdas-v1_0.tsv`, Pieza 1). Las 11 celdas
restantes no cambian. `p`/`clase` de `milpa/tramite.yaml` no se tocan —
solo la columna `conducta` del marco decide qué fila de la regla se lee.

### `M` en `TRA` — antes y después

| celda | `R` | `M` v1.2 (`paga_mordida`) | `z_M` v1.2 | `M` v1.3 (`paga_mordida_encig2025`) | `z_M` v1.3 |
|---|---|---|---|---|---|
| `TRA-M-02` | 0.1260 | 0.62 | **+97.62** | 0.085118 | **−8.08** |
| `TRA-M-03` | 0.0445 | 0.62 | **+202.54** | 0.085118 | **+14.28** |
| `TRA-M-07` | 0.0718 | 0.62 | **+228.76** | 0.085118 | **+5.55** |

Mediana `|z|` de `M` sobre las 14 celdas: **11.43 (v1.2) → 7.43 (v1.3)** —
confirma la expectativa declarada antes de correr en el encargo (B-bis:
`z ≈ −8/+14/+6` en `TRA`, mediana ≈ 7.4). `comparacion_principal_pareada`
(`L_SOLO_vs_M`, banda `z`, veredicto primario) sigue **`INDETERMINADO`**
(v1.2: `[−16.65, ...]`≈punto 27.9; v1.3: punto `10.79`, IC95
`[−1.84, +26.53]`) — el IC sigue cruzando 0, ninguna celda entra en banda
`±0.5`. **Corregir el enlace no cambia el veredicto primario de la
comparación pareada** — sigue sin distinguir `L_solo` de `M` con la
evidencia actual, ahora con un punto medio mucho más cercano a 0.

### `D4` resuelta — métrica secundaria en puntos porcentuales (`procedimiento-scoring-v1_2.md` §7)

| corredor | `MAE_pp` (punto) | IC95 |
|---|---|---|
| `M` | **4.51** | [2.71, 6.37] |
| `L_SOLO` | 11.69 | [4.13, 21.72] |
| `L_CORPUS` | 19.60 | [9.28, 30.92] |

| comparación pareada `|err_pp_corredor| − |err_pp_M|` | punto | IC95 | orden |
|---|---|---|---|
| `L_SOLO_vs_M` | +7.23 pp | [+0.68, +16.92] | **`M-MENOR-ERROR-PP-QUE-L`** |
| `L_CORPUS_vs_M` | +15.10 pp | [+5.92, +25.71] | **`M-MENOR-ERROR-PP-QUE-L`** |

**Esto es la respuesta a `D4`.** La banda `z` (primaria, sellada) no
discrimina (`INDETERMINADO`, arriba). La métrica secundaria en puntos
porcentuales **sí discrimina, en los dos pares**: los dos IC son
íntegramente positivos — `M` se desvía menos de `R`, en pp absolutos, que
`L_solo` y que `L+corpus`, sobre las 14 celdas del universo vigente. No
reabre ni sustituye el veredicto primario `INDETERMINADO` (§7 del
procedimiento, carácter no-gatante) — es diagnóstico, ordena corredores,
no adjudica banda.

### `D1` — sin cambio

El re-apuntado de `TRA` no toca `CIV`: las seis celdas `CIV-M-*` siguen
con el mismo `M=0.294313` byte a byte (§3 de arriba, sin re-derivar). `D1`
sigue **NO POR AHORA** — se reabre cuando `M` deje de ser constante dentro
de `CIV`, condición que este acto no cambia.

### Decisiones para mesa — actualización

- **`D4` → FIRMADA por merge** de `ACTO MAESTRA38-M13` (decisión de
  dirección incluida en el encargo, D-B: puntos porcentuales, `z` sigue
  primaria). Recibo en `forense/firmas-pendientes.tsv`.
- **`D1` → sin cambio, NO POR AHORA.**

### Qué NO hace esta sección

No re-abre `D1`. No cambia `delta=0.5` ni la banda `z`. No re-apunta
`DIN-M-01` (`diagnostico-14-celdas-v1_0.tsv`/`enlace-M-v1_1.md` §3: hay
una enmienda MEDIDA firmada análoga —`enmienda_enif2024`— pero ninguna
firma de mesa de este encargo la cita; se reporta, no se aplica; sucesor
declarado). No mueve ningún tier de `canon/modelo-decision-v4_0.md`. No
abre el paso 3 (`evaluar()` por celda/eje) — ver `enlace-M-v1_1.md` §6 y
el encargo, "sucesores declarados, no lanzados".
