# ACTO `GEN2-CELDA-D-PILOTO-2` v1.1 (relanzamiento) · nota de cierre

**17/sep/2026 · CAJA · `ADR-542` (candidato, derivado por `tools/cierre_acto.py` Fase A sobre `origin/main = e46e7e4`; renumera quien fusiona segundo) · PR: ver `## CONSUMIDO` del encargo.**
Encargo verbatim: `forense/encargos/2026-09-17-GEN2-CELDA-D-PILOTO-2-V1_1.md` (0-bis `A.3`, commit `e2d252d`).
Spec: `forense/prereg-caja/TRA-evade-norma-sxd12-spec-v1_0.md` (`sha256 45bca167…`), **una sola versión, sin enmienda**.

---

## 0 · Arranque: la rama vieja, el agente fresco y la base

* El encargo ordenaba PARAR si `acto/gen2-celda-d-piloto-2` seguía viva con el encargo v1.0. **Estaba viva en local** (worktree `mm-gen2-celda-d-piloto-2`, HEAD `73477a4` «ABORTADO antes de COMMIT-1», con un merge a medias y conflictos `UU`), **no en origin**. Se PARÓ, se reportó con SHAs y estado del árbol, y **mesa autorizó borrarla** («borrala, yo ya la borré del repo»): `git worktree remove` + `git branch -D` (`was 73477a4`), sin resguardo en origin por instrucción. Nada de esa rama se leyó más allá de la primera línea del encargo archivado y los asuntos de commit.
* Chequeo de agente fresco: el mensaje de lanzamiento traía sólo el encargo v1.1 (más la salida local de `/model`). Sin resumen, cifras ni hallazgos heredados.
* Base: el encargo se redactó contra `9207cb2`; al abrir, `origin/main = e46e7e4` (13 commits de `ADQ`/`CENSO`/`DERIVADOS`, ninguno en el perímetro). COMPUERTA `#856` verificada por producto (`bc24316` ancestro de `origin/main`; encargo de REGISTRO-CAJA-1 con `## CONSUMIDO`). `A.8`: `python3 tools/ya_medido.py tramite.evasion_norma` → **`MEDIDA-EN: tramite-ola5-propuesta-v0.yaml, tramite.yaml`** (nacional y por eje; el cruce de dos ejes no existía).

## 1 · Qué se pidió, qué se hizo, y en qué orden

| pieza | commit | qué quedó | microdato |
|---|---|---|---|
| 0-bis | `e2d252d` | encargo verbatim | — |
| **`COMMIT-1`** | **`2ff0283`** | spec v1.0 + sidecar; **`tools/celda_d/marginales_reproduccion.py`** (guardia de una variable); `tests/test_marginales_una_variable.py` (15 casos, zips fabricados); contrato + medidor de emisiones (514 `RESULT`, `spec-check 27 OK · 0 FAIL`) | **ninguno** |
| **`COMMIT-2`** | **`cdd78f9`** | `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001--2ff028319eed` sellado; `verify REPRODUCE`, 514/514 | 2023 y 2024 enteras; 2025 **sólo marginales, por el módulo** |
| `COMMIT-3a` | `7e86d93` | contrato + medidor del árbitro (369 `RESULT`, `spec-check 9 OK`) | ninguno |
| **`COMMIT-3`** | **`9b5c371`** | `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001--7e86d93722ec` sellado; `verify REPRODUCE`, 369/369; celda-D; fila `M05`; test del consumidor | 2025, cruce |

**El orden lo prueba el historial, no esta nota** (lección `NC-0313`): `data/corrida0/CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001/` no existe en `cdd78f9` (`git ls-tree cdd78f9 -- <dir>` vacío), y `tests/test_celda_d_piloto2_consumidor.py::test_las_emisiones_se_sellaron_antes_de_que_r_existiera` lo asierta con `git log --diff-filter=A` + `merge-base --is-ancestor`. **Ningún `RESULT` de este acto es un snapshot del árbol**; `verify` de las emisiones debe dar `REPRODUCE` de forma permanente.

**La guardia de Firma 2 no es prosa.** `marginal(ola, grupo: str)` admite **un** `str` posicional (dos → `TypeError`; lista → `TypeError`; eje inventado → `ValueError`); la `Ola` lleva huella (`sha256` de `ID_DEL`) y una ola filtrada o reordenada lanza `ReservaRota`; `cruce()` lanza sobre una ola cargada `reservada=True`. El medidor de emisiones **lo prueba en cada corrida** —intenta el cruce y registra que fue rechazado— y lo sella: `RESULT-TRA-SXD12-G-RESERVA-CRUCE-2025-DERIVADO = "NO"`, `G-RESERVA-GUARDIA-PROBADA = "ReservaRota: ENVIPE 2025 está RESERVADA…"`. Es función del código, replica.

**`E.5` cumplido de verdad:** antes del `COMMIT-1` sólo corrió `tests/test_marginales_una_variable.py` y un generador de `spec.yaml` que valida el medidor **contra zips fabricados** (miembro, BOM y `\r` como los reales; valores aleatorios). El primer byte de microdato lo abrió `corrida0 run` en el `COMMIT-2`.

## 2 · El resultado

`R` = árbitro, ENVIPE 2025, 12 celdas, receta del árbitro (`wprop_ic_conglomerado`, `FAC_DEL`, `EST_DIS/UPM_DIS`, 10 000, seed 42). `d` en **pp**.

| celda | `n₂₅` | `R` | IC95 | `EE` | `d(C1)` | `d(C2)` | `d(C6)` | `d(C7)` | C6 vs C1 / C2 | C7 vs C1 / C2 |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|
| `S1xD1` hasta primaria × Rural | 792 | **0.3926** | `[0.3458, 0.4405]` | 0.0242 | 0.32 | 5.44 | 5.21 | 4.64 | PISO / INDEC | INDEC / INDEC |
| `S1xD2` × Complemento urbano | 871 | **0.4893** | `[0.4217, 0.5569]` | 0.0345 | 5.68 | 3.69 | 3.35 | 6.60 | INDEC / INDEC | INDEC / INDEC |
| `S1xD3` × Urbano | 1 828 | **0.5368** | `[0.4932, 0.5788]` | 0.0218 | 3.32 | 1.29 | 3.10 | 3.35 | INDEC / INDEC | INDEC / INDEC |
| `S2xD1` secundaria × Rural | 1 221 | **0.4263** | `[0.3849, 0.4678]` | 0.0212 | 4.37 | 1.85 | 5.17 | 5.09 | INDEC / PISO | INDEC / PISO |
| `S2xD2` | 1 884 | **0.5270** | `[0.4924, 0.5604]` | 0.0173 | 6.96 | 0.02 | 0.18 | 0.56 | **CHAL** / INDEC | **CHAL** / INDEC |
| `S2xD3` | 4 634 | **0.6137** | `[0.5879, 0.6391]` | 0.0131 | 3.59 | 1.65 | 0.46 | 0.00 | **CHAL** / INDEC | **CHAL** / INDEC |
| `S3xD1` media superior × Rural | 985 | **0.3767** | `[0.3243, 0.4319]` | 0.0274 | 2.59 | 0.79 | 1.82 | 0.16 | INDEC / INDEC | INDEC / INDEC |
| `S3xD2` | 2 412 | **0.5094** | `[0.4757, 0.5415]` | 0.0168 | 0.64 | 0.69 | 2.30 | 0.20 | INDEC / INDEC | INDEC / INDEC |
| `S3xD3` | 8 079 | **0.5722** | `[0.5434, 0.5992]` | 0.0142 | 0.75 | 0.14 | 0.38 | 0.14 | INDEC / INDEC | INDEC / INDEC |
| `S4xD1` superior × Rural | 769 | **0.4161** | `[0.3631, 0.4685]` | 0.0269 | 12.25 | 1.44 | 10.99 | 9.32 | INDEC / PISO | **CHAL** / PISO |
| `S4xD2` | 2 847 | **0.5433** | `[0.5128, 0.5740]` | 0.0156 | 7.27 | 0.66 | 0.91 | 1.48 | **CHAL** / INDEC | **CHAL** / INDEC |
| `S4xD3` | 13 858 | **0.6078** | `[0.5896, 0.6255]` | 0.0092 | 4.03 | 1.16 | 0.35 | 0.45 | **CHAL** / INDEC | **CHAL** / INDEC |

### 2.1 · Veredicto de celda-D: **`SIN-CANDIDATO-SUPERIOR`**

* **12/12 celdas `PUNTUADA`**, 0 `FUERA-DE-SOPORTE` en ninguna ola (`n₂₀₂₅` 769-13 858; `n₂₀₂₄` 859-12 116; `n₂₀₂₃` 819-10 905). El «≈ 300» esperado para hasta primaria × Rural resultó **792**.
* **Ningún challenger vence a los dos pisos en ninguna celda (0 de 12).** `C6` vence a `C1` en 4 y a `C2` en **0**; `C7` vence a `C1` en 5 y a `C2` en **0**. Contra `C2` quedan `INDECIDIBLE` en 10 (`C6`) y 9 (`C7`) y pierden en 2 y 3.
* **`MAE`: `C2` 1.5681 pp · `C7` 2.6650 · `C6` 2.8529 · `C1` 4.3146.** Skill (se reporta, no adjudica): `C6` +0.339 vs `C1`, **−0.819 vs `C2`**; `C7` +0.382 vs `C1`, **−0.700 vs `C2`**.
* `champion_actual = NINGUNO`. **Este acto no adopta nada.**

**`B-bis`, declarado antes de correr y leído mecánicamente (`RESULT-TRA-SXD12-ARB-G-B-BIS-LEIDO`), dos cláusulas:**

1. **Nadie vence a `C1`** → la persistencia anual queda corroborada como piso en `TRA`.
2. **Nadie vence a `C2`** → «marginales actuales sin interacción» es el estimador honesto de celda para esta familia; **la interacción de olas previas no aporta bajo estos candidatos** — resultado de programa, cambia el marcador. Y sólo eso dice (`H5`): no identifica ausencia de interacción ni una propiedad de la población.

**Lo que el resultado añade sobre el primer piloto:** aquí los challengers **sí** explotan una interacción medida (no una elicitación), y **añadirla al piso marginal lo empeora**: de 1.57 pp a 2.85 (`C6`) y 2.66 (`C7`). La razón se ve en las emisiones: las interacciones por celda son **inestables entre olas** — sólo 4 de 12 `I₂₄` y 5 de 12 `I₂₃` tienen IC95 que excluye 0, y en `S1xD2` cambia de signo (`I₂₃` −0.250, `I₂₄` +0.014). Promediar dos olas (`C7`) ayuda algo respecto de una (`C6`), en la dirección que la cláusula «`C7` vence y `C6` no» anticipaba, **pero no alcanza**: la cláusula no se dispara porque ninguno vence.

### 2.2 · `C5` · diagnóstico puro, fuera de competencia

`|0.562774 − R|` por celda: de **0.94 pp** (`S3xD3`) a **18.61 pp** (`S3xD1`). El emisor sigue siendo el árbitro con otro nombre (`tramite.yaml:497`) y no entra en ninguna adjudicación. Signo de la modulación respecto del nacional: `ESTABLE` en 7/12 (`C1`), 10/12 (`C2`), 6/12 (`C6`), 8/12 (`C7`); el resto `AMBIGUA`; ninguna `CONTRARIA`.

## 3 · El control de reproducción: `REPRODUCE`, y por qué vale

Control declarado antes del dato (spec §0.7), ejecutado por el módulo congelado sobre los ocho marginales sellados de ENVIPE 2025:

| grupo | `n` sellado | `Δn` | `Δp` | `ΔIC95inf` | `ΔIC95sup` |
|---|---:|---:|---:|---:|---:|
| hasta primaria | 3 491 | 0 | +3.1e-07 | −4.1e-07 | +3.6e-07 |
| secundaria | 7 739 | 0 | +1.2e-07 | +6.8e-08 | +9.7e-08 |
| media superior | 11 476 | 0 | −4.0e-07 | −3.7e-07 | +4.7e-07 |
| superior | 17 474 | 0 | −3.9e-07 | +1.2e-07 | −3.5e-07 |
| Rural | 3 770 | 0 | +3.2e-07 | +1.2e-08 | −2.4e-07 |
| Complemento urbano | 8 039 | 0 | +4.0e-07 | −3.4e-07 | −2.5e-07 |
| Urbano | 28 471 | 0 | −2.2e-07 | +1.9e-07 | −2.4e-07 |
| nacional | 40 280 | 0 | +4.8e-07 | −4.4e-07 | +1.0e-07 |

**`|Δp|` máx `4.79e-07`, `|ΔIC|` máx `4.70e-07`** — el residuo es el redondeo a seis decimales de la cifra sellada. **Punto E IC reproducen**, porque el módulo importa la misma función del árbitro (`tools/calibracion_mordida_encig_serie.py::wprop_ic_conglomerado`) y la construcción del eje (`tools/ejes_maestra35_l1.py::ESC_2DIG`) como objetos, no como copias. A diferencia del primer piloto, aquí **no hay universo dual**: los `Δn = 0` en los ocho lo acreditan.

## 4 · Lo que la lectura por archivo encontró (antes de congelar), y una premisa del encargo corregida

* **1.20 y 1.23 son idénticas palabra por palabra en 2023/2024/2025** (FD en PDF); los códigos `04`/`05`/`06`/`08` tienen el **mismo texto** en las tres olas — los únicos cambios de texto (lenguaje incluyente en `01`/`02`) quedan fuera del conjunto. **A.15c no se dispara.**
* `NIV` (catálogo de 12 claves) y `DOMINIO` (`U`/`C`/`R`) idénticos en las tres; `FAC_DEL`/`EST_DIS`/`UPM_DIS` presentes en las tres, con `UPM_DIS` de longitud 5 en 2023 y 7 en 2024/2025 (se agrupa por el par `(EST_DIS, UPM_DIS)` dentro de cada ola; nunca entre olas).
* **Premisa del encargo corregida por archivo:** «leerla del acto que la selló, `MAESTRA35-L5`». El acto que selló `escolaridad_proxy` es **`MAESTRA35-L1 · P4`** (`milpa/tramite-ola5-propuesta-v0.yaml:1672-1731`, campo `acto:`; código en `tools/ejes_maestra35_l1.py:42-46`; censo `forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md` §4.1). `L5` es `R-DIN-M-01`, otro objeto. Se cita por archivo, como el encargo pedía; no cambia nada del diseño.
* La cita «nacional `:1677`» del encargo apunta, en este árbol, a la línea `universo:` del bloque de ejes; el nacional sellado vive en `milpa/tramite.yaml:497` (+`:522` el IC) y `milpa/tramite-ola5-propuesta-v0.yaml:871`. Se citó eso.
* Universo 2025: **40 280 filas de `tmod_vic`, las 40 280 en el universo** (`BP1_20` sin blancos), 0 delitos sin persona, 100 con escolaridad `(fuera)` — exactamente el árbitro.

## 5 · El registro GEN2: bloqueado, reportado, no forzado

`python3 tools/corrida0.py registro --escribe --lote CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001,CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001` → **`PARO · REPLAY-PISADO (NC-0094): escribir borraria o cambiaria evidencia de replay de 25 corrida(s) AJENA(s) al lote autorizado (50 campo(s)). No se escribio ninguna vista.`** (`rc=1`, `git status` limpio después). Es lo que `ADR-540`/`NC-0315` midieron; el encargo lo prevé: **las dos `CALC` quedan `SELLADA-EN-DISCO`, `NO-REGISTRADA` en el CONTADOR**, no se fuerza. La proyección en seco (`registro` sin `--escribe`) **sí** las deriva con `cuenta_gen2 = SI` («etiqueta de la spec»). `status`: `N_corridas_selladas` **80 → 82** (deriva de disco).

## 6 · Los seis checks del GO de `E.5`, por nombre

| check | emisiones | árbitro |
|---|---|---|
| `PAYLOAD-RESUELTO` | 6/6 `COINCIDE` | 2/2 `COINCIDE` (uno es el `resultados.json` sellado de las emisiones, input de repo con sha `5d120c1f…`) |
| `CONTRATO-EJECUTABLE-COMPLETO` | `ENDURECIDO` | `ENDURECIDO` |
| `OUTPUTS-VALIDADOS` | **514/514** | **369/369** |
| `CALC-INMUTABLE` | `SIN-SELLO-PREVIO` al correr | `SIN-SELLO-PREVIO` al correr |
| `SELLO-COMPLETO` | `COINCIDE` | `COINCIDE` |
| `VERIFY-CONTEXTO+RESULTADO` | **`IDENTICO · REPRODUCE`** | **`IDENTICO · REPRODUCE`** |

`spec-check`: 27 OK · 0 FAIL · 317 718 filas (emisiones); 9 OK · 0 FAIL (árbitro).

## 7 · Productos, y lo que NO se movió

* **Dos corridas GEN2 selladas**, `cuenta_gen2 = SI` en la etiqueta de las dos (el encargo lo autoriza), **883 `RESULT` GEN2** nuevos (514 + 369), **no registradas** en la vista (§5).
* **Celda-D nueva** `data/curacion-registro/celdas-d/TRA.evade_norma.envipe2025.escolaridad_x_dominio.yaml` (v0.5; `estado_decidibilidad: PUNTUADA`, `margen_material: 1.568052`, `champion_actual: NINGUNO`, `requiere_decision_mesa: false`); **5/5 celdas-D validan** (`tests/test_celdas_d.py`); `T-MOTOR-EJECUTABLE` 6/6. `unidad_objetivo: persona` (la del modelo) con la unidad del dato —DELITO— declarada en cada candidato: el enum v0.5 §3 no tiene `delito`, y la regla modela la conducta de una persona ante una norma. `data/INFRAESTRUCTURA-v1_0.md` D5 recibe la enmienda fechada que `T27` exige (4 → 5).
* **La fila `M05` del catálogo pasa de `NO-VERIFICADO` a `DERIVADO-Y-SELLADO-GEN2`** con `spec_ref`, universo, instrumentos, cómputo y reserva declarados — **una sola línea cambiada** (`git diff --numstat` → `1 1`), editada por línea sin `csv`, **rol `AJUSTE` intacto**. Segunda fila del catálogo con estimador derivado: `22 de 23 NO-VERIFICADO` → **21 de 23**.
* **El test lo prueba:** `tests/test_celda_d_piloto2_consumidor.py`, **10/10** — el consumidor lee la fila sin cambiar código, las otras 22 no cambiaron un byte respecto de `cdd78f9`, la regla existe una vez en `tramite.yaml`, `_consumidores_momentos` la deriva sin ambigüedad, **el muro sigue en pie** (`valor_de(M05)` lanza `NotImplementedError`: una cifra sellada en `corrida0` no se vuelve insumo del motor), append-only de roles, la celda-D valida, y el falsador de orden se lee del historial.
* **NO se tocó:** `milpa/tramite.yaml` · `milpa/tramite-ola5-propuesta-v0.yaml` · `milpa/src/` · la spec previa · el marcador · el crosswalk · `tests/baseline.json`. **Adopción al motor: cero. `L`: no se elicitó.** El cruce `edad × dominio` **no se usó** y sus números no están en ninguna parte de este acto.

## 8 · Concurrencia y numeración

* `origin/main` no se movió durante el acto (`git rev-list --count HEAD..origin/main` → 0 al abrir y al cerrar la cascada). Actos en paralelo declarados por el encargo: `GEN2-MARCADOR-REDISENO-1` y `GEN2-REGISTRO-BANDERA-1` (nube), sin archivo común salvo el tablero. Números tomados: `ADR-542`, `FP-385`, `NC-0328`–`NC-0331` — quien fusione segundo renumera.
* T25: el encargo verbatim trae `M05` pelado (id de fila del catálogo); exención documentada en `_T25_ARCHIVOS_CONOCIDOS`. La spec propia nombra la fila por su regla.

## 9 · Hallazgos que quedan con sucesor (`## NO-CORRIDO / RESERVAS`)

1. **`NC-0328`** · P4 del encargo: `edad × dominio` ENVIPE 2025, `RESERVA-CONSUMIDA-SIN-PILOTO` (17/sep/2026), asentada sin números.
2. **`NC-0329`** · registro de las dos `CALC` bloqueado por `NC-0094` (§5); sucesor: el mismo de `NC-0315`.
3. **`NC-0330`** · `tests/test_celda_d_piloto_consumidor.py` (primer piloto) cablea «22 filas `NO-VERIFICADO`» y **falla** al pasar `M05` a derivada — el mismo defecto de conteo literal que ese acto corrigió en `test_motor_ejecutable.py`. Fuera de perímetro: **no se editó**; ni `check.py` ni CI lo corren.
4. **`NC-0331`** · los dos tests nuevos no están cableados en `.github/workflows/verify.yml` (fuera de perímetro): «un test que nadie corre es decoración». Sucesor: un acto de mantenimiento que añada los dos pasos.

## 10 · Sucesores

1. **Consumo por el marcador rediseñado** (`FP-383`, `GEN2-MARCADOR-REDISENO-1`): la celda-D y la fila `M05` están listas para leerse.
2. `C6`/`C7` **no ganaron**: la cláusula «si C6/C7 ganan, el mismo candidato sobre una celda DIN nueva» no se dispara.
3. Lo que este resultado sí sugiere para un sucesor, sin decidirlo: probar la interacción **agregada** (no por celda) o encogida hacia 0 — el ruido por celda es lo que hunde a `C6`/`C7`.

**CONTADOR, sin disfraz (regla de señal v2.3):** **+2 corridas GEN2 selladas** (`cuenta_gen2 = SI`; **NO registradas**: `NC-0329`), **883 `RESULT`**, **segunda celda-D adjudicada sin campeón**, **segunda fila del catálogo con estimador derivado (`M05`)**, `FP-385` nace `FIRMADA`. **Cero adopciones. Cero cambios al motor. Cero `L`.**
