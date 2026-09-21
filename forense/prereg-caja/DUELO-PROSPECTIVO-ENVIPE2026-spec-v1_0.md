# DUELO PROSPECTIVO NACIONAL · ENVIPE 2026 — spec congelable v1.0

### `prereg-caja-DUELO-PROSPECTIVO-ENVIPE2026` · **v1.0** · 21 de septiembre de 2026 · `ACTO GEN2-DUELO-ENVIPE2026-COMMIT-1` · contra `main = 55c8d57c`

> **Universo, unidad, escala (primera línea, como pide mesa).** Unidad de análisis **DELITO**, no persona; ponderador **`FAC_DEL`** («Factor delito», Numérico 6, `000001…999999`, `fd_envipe2023/2024/2025.pdf`, citado en `TRA-evade-norma-sxd12-spec-v1_0.md` §0.5). Universo por estimando en §1. Escala de emisión: proporción en [0,1]; todo error en **puntos porcentuales (pp)**; toda combinación de niveles en **logit** y de vuelta a proporción antes de comparar. Ninguna cantidad de unidad DELITO se compara contra una de unidad PERSONA: aquí no hay ninguna.

| | |
|---|---|
| **ARCHIVO** | `forense/prereg-caja/DUELO-PROSPECTIVO-ENVIPE2026-spec-v1_0.md` + `.sha256` |
| **QUÉ ES** | El COMMIT-1 del duelo prospectivo: diseño de MOTOR v1.0 (`DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md`, sha `e88d3192…`) + enmienda v1.1 (F7 A/B/C, D-22 ampliada, regla v0.3, respuesta de mesa «Ola anterior = 2024»), convertidos en cinco `CALC` y tres módulos. Se congela **sin abrir ENVIPE 2026**. |
| **QUÉ NO ES** | No abre 2026, no corre LLM, no adjudica. No edita ningún CALC sellado ni `milpa/`. No reescribe el guardián `tools/celda_d/marginales_reproduccion.py` ni el medidor sellado de la serie. |
| **MODO** | ABIERTO mientras se construye; lo declarado congelado en §10 queda RÍGIDO para quien ejecute COMMIT-2/3 (otra sesión, F3). |
| **VERIFICAS ASÍ** | `python3 tests/test_duelo_prospectivo.py` OK · `python3 tools/corrida0.py preflight <CALC>` por cada CALC de §8 · `python3 tools/corrida0.py verify CALC-DUELO-ENSAYO-ENVIPE2025-*` y `…-ORIGEN-MOVIL-0001` REPRODUCE · `sha256sum -c DUELO-PROSPECTIVO-ENVIPE2026-spec-v1_0.sha256`. |

## 1 · Estimandos que entran, por la regla del diseño

Regla (diseño §2): entra un estimando si tiene **R sellado por ola en ≥ 3 olas** y **universo idéntico** a lo largo de ellas. La comparabilidad se lee de la columna del archivo, no se asume.

| id | estimando | universo | olas selladas | entra |
|---|---|---|---|---|
| **ND** | `p_c1_u1` = **delito personal no denunciado**: proporción ponderada de delitos personales (`BPCOD` personales, `BP1_20 == 2`) cuya razón principal de no denuncia `BP1_23` cae en `C1_uno = {1,2,6}` sobre `C1_uno ∪ C1_cero = {1..8}` — el estimador sellado de `prereg-caja-ENVIPE-SERIE-COMPLETA` (medidor `data/corrida0/CALC-ENVIPE-SERIE-2022/medidor.py`, `codificacion` de su `spec.yaml`). | delitos personales con `BP1_20 == 2` y `BP1_23` en catálogo | 15 (`data/corrida0/envipe-serie-denuncia-v1_0.tsv`, olas 2011–2025) | SÍ; **2011 fuera** de todo ajuste y de todo objetivo: su fila trae `comparabilidad = INSTRUMENTACION-NOMINAL-Y-RESIDUALES`; las 14 restantes `NINGUNA-EN-C1-U1` (leído del archivo, columna `comparabilidad`). Serie homogénea = 2012–2025. |
| **EN** | `evade_norma` = `BP1_20 == "2" ∧ BP1_23 ∈ {04,05,06,08}` (dos dígitos; `b`/blanco → 0), la CONJUNTA sobre el universo — verbatim de `prereg-caja-ENVIPE-EVASION-NORMA` y `TRA-evade-norma-sxd12-spec-v1_0.md` §2.2. | delitos de `tmod_vic` con `BP1_20 ∈ {1,2}` | 3 (2023: `0.5215395526634797` `RESULT-TRA-SXD12-G-W23-P-NACIONAL`; 2024: `0.538725312630215` `…-W24-P-NACIONAL`; 2025: `0.5627744787844097` `RESULT-EVASIONNORMA-A-P-EVADE`, IC95 `[0.5519815599158291, 0.5734481021728013]`) | SÍ (cumple «≥ 3»); T5 y TC **NO-CONSTRUIBLE** por serie insuficiente (diseño §2), y así se asientan. 2023/2024 no tienen IC sellado: el CALC de emisiones re-deriva los tres puntos con IC por el guardián (control contra sellado a 1e-6). |

Ningún otro estimando cumple la regla (no hay tercera serie nacional sellada de ENVIPE en `data/corrida0/`, censo por `ls data/corrida0 | grep ENVIPE`, 21/sep/2026).

**K ≡ constante del motor (comprobado por comando).** `milpa/tramite.yaml:497` trae `evade_norma_envipe2025 p: 0.562774`; `RESULT-EVASIONNORMA-A-P-EVADE = 0.5627744787844097`; `|Δ| = 4.788e-07 ≤ 1e-6`. K se emite **una sola vez** para EN, rotulada «K = constante-del-motor ≡ persistencia-t−1», y el CALC de emisiones lo re-verifica (`…-G-EN-K-COINCIDE-CONSTANTE-MOTOR`). Para ND no hay constante del motor: K es persistencia t−1 a secas.

## 2 · Contendientes nacionales — todos a la vez, fórmula cerrada, sin selección posterior

Para la ola nueva `t` (2026), con la serie de puntos `(ola_i, p_i, IC95_i)` **anteriores a t y comparables**:

- **K** — `p_{t−1}`, con su IC95 sellado.
- **T3 / T5 / TC** — recta OLS en logit: `ŷ_t = ȳ + b·(t − x̄)`, `x` = `ola_encuesta`, `y = logit p`, sobre las últimas 3 / 5 / todas las olas anteriores. Ventana mínima: T3 3, T5 5, **TC 6** (con ≤ 5 puntos TC coincidiría con T3 o T5 y no sería variante; para EN, TC y T5 son NO-CONSTRUIBLE, diseño §2). **IC95**: la predicción es lineal en los `y_i` (`c_i = 1/n + (t − x̄)(x_i − x̄)/Sxx`); con `EE_i = (hi_i − lo_i)/3.92` llevado a logit por delta (`EE_i/(p_i(1−p_i))`) y olas independientes, `Var = Σ c_i²·EE²_logit,i`; `IC95 = expit(ŷ_t ± 1.96·√Var)`. Cubre la incertidumbre muestral de los puntos, **no** el error de especificación de la recta.
- Una variante no construible se emite con `p = null` y su estado (`NO-CONSTRUIBLE-SERIE-INSUFICIENTE(n<m)`); nunca se sustituye ni se rellena.

Implementación: `tools/duelo/tendencia_nacional.py` (`predice`), sin ENVIPE dentro.

## 3 · E+ — persistencia por eje + desplazamiento nacional, en logit (EN)

`logit p_eje,t = logit p_eje,t−1 + [logit T*_t − logit p_nac,t−1]`, una fila por variante `T* ∈ {T3, T5, TC}` y por celda de eje: escolaridad_proxy (S1–S4), dominio_urbano_rural (D1–D3), sexo (H, M), edad (E1–E4: 18-29, 30-44, 45-59, 60+), los ejes del guardián extendido (`GEN2-GUARDIAN-ENVIPE-EJES-IC-1`). `p_eje,t−1` y `p_nac,t−1` salen del guardián sobre la ola 2025 con réplicas compartidas; el IC95 de E+ propaga réplica a réplica el término de la ola t−1 (covarianza eje/nacional respetada) y `T*` como normal en logit con su EE, sorteo independiente `PCG64(42)`. Su competidor es la **persistencia por eje** (`p_eje,t−1`, emitida como `PERS-*`). Para ND, E+ es **NO-CONSTRUIBLE**: no hay marginal por eje sellado y el guardián mide un solo desenlace; se asienta con ese texto. Para EN sólo T3 es construible (§1), así que E+ tiene una variante construible y dos filas `null` declaradas.

## 4 · Nivel cruce — familia F7(B) y regla v0.3, genéricas sobre (instrumento, par)

Módulo de referencia: `tools/duelo/cruces_familia.py` — recibe celdas ya estimadas (punto, IC95 del árbitro, réplicas, n) y no sabe qué es ENVIPE. Para la ola nueva `t` con marginales `m_t` y la(s) ola(s) anterior(es) `t'`:

| id | contendiente | fórmula | réplicas |
|---|---|---|---|
| **C2** | piso log-aditivo (a vencer) | `expit(logit m_t(a) + logit m_t(b) − logit m_t)` — `piso_log_aditivo` del piloto 2, misma forma | réplica k de la ola t |
| **P** | persistencia | `x_t'(a,b)` (el cruce de la ola anterior, punto e IC95 del árbitro) | réplica k de t' |
| **S1** | interacción cruda | `expit(logit C2_t + Ī(a,b))`, `Ī` = media sobre las olas anteriores de `I_w = logit x_w(a,b) − [logit m_w(a) + logit m_w(b) − logit m_w]` | k con k, olas independientes |
| **Sλ** | interacción encogida | `expit(logit C2_t + λ·Ī)`, `λ = τ̂²/(τ̂² + σ̄²)`, `τ̂² = max(0, Var_entre(Ī) − σ̄²)` (ddof = 1 sobre celdas con Ī finito), `σ̄²` = media de `Var(Ī_k)` por celda — momentos, como el piloto 3 (`GOB-gobierno-digital-exe15-spec-v1_1.md` §3.1) | ídem |
| **AP** | ajuste proporcional | `expit(logit x_t'(a,b) + logit m_t − logit m_t')` — la persistencia desplazada por el cambio nacional, en logit (análogo de celda de E+; en logit por la primera línea del diseño, **no** un cociente de proporciones) | k con k |

Término fuera de (0,1) → réplica `NaN` (SIN-DEFINIR), punto `null`; nunca recorte. Se emiten los cinco de golpe.

**Pares y olas anteriores (respuesta de mesa 21/sep/2026, enmienda v1.1 §5):**

| par | ejes | ola anterior para P y AP | olas para Ī | rótulo |
|---|---|---|---|---|
| **SXD** | escolaridad_proxy × dominio_urbano_rural | 2025 (t−1) | 2024, 2025 | PERSISTENCIA-t−1 |
| **EXD** | edad × dominio_urbano_rural | 2024 (t−2) | 2023, 2024 | PERSISTENCIA-t−2 (2025 vetada por nombre, NC-0328) |

Celdas: SXD 12 (`S1xD1…S4xD3`), EXD 12 (`E1xD1…E4xD3`), rótulos del piloto 2 y del guardián. **Los 4 cruces reservados de ENVIPE 2025** (`dominio×sexo`, `edad×escolaridad`, `edad×sexo`, `escolaridad×sexo`, `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001`) **no se tocan**.

**Soporte.** `PUNTUADA` si `n ≥ 200` en la ola nueva y en cada ola anterior usada; si no, `FUERA-DE-SOPORTE`: se emite igual, no puntúa. `n = 0` → `NO-ESTIMABLE` (`null`), nunca `0.0`.

**Regla v0.3 (propuesta de dirección, verbatim en enmienda §4).** `ΔMAE(j) = MAE(C2) − MAE(j)` en pp sobre las PUNTUADAS, IC95 = percentiles 2.5/97.5 de `ΔMAE_k` con `R_k`, `C2_k`, `j_k` de la **misma** réplica k. `VENCE-RETADOR` si `IC95inf > 0.5`; `PROPUESTA-CON-RESERVA` si `0 < IC95inf ≤ 0.5`; `NADIE-VENCE` si incluye 0 (y se dice si `IC95sup < 0`: el piso se sostiene). Retador **primario: Sλ**; P, S1 y AP se adjudican con la misma regla rotulados `SECUNDARIA`. Además, por celda y candidato: error en pp, punto dentro del IC95 de R (árbitro), R dentro del IC95 del candidato — las tres, sin colapsar (diseño §5). Nada se ordena ni se escoge: `adjudica()` devuelve el veredicto de cada uno.

## 5 · Regla del LLM (diseño §3, verbatim en el diseño archivado)

Este acto **no corre LLM**. Cuenta como PROSPECTIVO sólo un modelo sin acceso web y con corte de entrenamiento anterior al 10/sep/2026, acreditado por cita del proveedor; con web o corte posterior es RETROSPECTIVO y nunca se promedia con los mecánicos; si no se acredita, `NO-ACREDITABLE`. La fila `L` de los CALC queda `NO-ENTRA` en COMMIT-2 salvo firma de mesa con la cita; su ausencia no invalida el duelo.

## 6 · B-bis — pre-registro de falsación (diseño §6, íntegro)

| si ocurre | se concluye | rótulo |
|---|---|---|
| K gana a las tres tendencias, con IC que despejan | la serie no tiene pendiente aprovechable a un año; la persistencia es el estimador adjudicado y la tendencia se retira como retador | corroborada |
| alguna T* gana a K con IC que despeja | la pendiente se transporta una ola; el retador entra a piloto por dominio, y **solo esa variante**, sin reajustar ventana | corroborada |
| T* gana en punto pero el IC no despeja | **falsador débil**: no adjudica. K sigue siendo el adjudicado (A-bis: un piso no vencido se adopta) | falsador débil |
| ningún contendiente se distingue de otro | la ola 2026 no discrimina entre estos candidatos a este n; se declara y **no se relanza sobre la misma ola** | acotada |
| E+ pierde contra persistencia por eje | el desplazamiento nacional no es común a los ejes; se acota E+ a los ejes donde ganó y se dice cuáles | acotada |
| todos los contendientes yerran en el mismo sentido y por magnitud similar | hubo un cambio de nivel en la ola (instrumento, muestra o mundo); **no es un veredicto entre candidatos** y se investiga antes de adjudicar nada | acotada |

Si dos filas pueden satisfacerse a la vez, manda la de arriba. **Operacionalización a nivel nacional** (declarada aquí, antes del dato): «IC que despeja» = IC95 de los dos contendientes **disjuntos**; «gana» = menor `|error|` en pp. El CALC de adjudicación emite la fila leída mecánicamente (`…-B-BIS-LECTURA-MECANICA`) y `…-ADJUDICA-SOLO = NO`: por F7(A) el punto de 2026 no adjudica solo; mesa lo lee con el origen móvil (§7) a la vista. A nivel cruce manda la regla v0.3 de §4.

## 7 · Origen móvil — RETROSPECTIVA-MECÁNICA (F7 A), no selecciona

`CALC-DUELO-ORIGEN-MOVIL-0001`, sólo insumos versionados: la serie ND (14 olas comparables) y los tres puntos EN sellados (§1). Para cada ola t comparable, K/T3/T5/TC predicen t sólo con olas < t; por (contendiente, t) se emite predicción, IC95, error con signo (pp), |error|, R dentro del IC del candidato, candidato dentro del IC de R; por contendiente, MAE, sesgo, cobertura con intervalo de Wilson 95 % y n, sobre todas sus olas construibles **y** sobre la ventana común (olas donde los cuatro son construibles: ND 2018–2025). Para EN sólo K (t = 2024, 2025) es construible y sin IC en 2023/2024 la cobertura es `NO-DERIVABLE`. **PARO (c) del encargo:** ninguna variante se elige, quita ni reajusta después de verlo; las cuatro van a COMMIT-2.

## 8 · CALC, commits, inputs

| CALC | commit | punto de entrada | inputs | estado al congelar |
|---|---|---|---|---|
| `CALC-DUELO-ORIGEN-MOVIL-0001` | este acto | `origen_movil` | `serie_nd` (repo, sha), `emisiones_piloto2`, `evasion_norma_v11` (repo, sha) | **sellable hoy** (cuenta según su spec: `cuenta_gen2 = SI`, no adopta) |
| `CALC-DUELO-ENSAYO-ENVIPE2025-EMISIONES-0001` | este acto (P3 i) | `emisiones`, `ola_nueva = 2025` cargada `reservada=True`, anteriores 2023/2024 | `envipe2023/2024/2025_csv`, `serie_nd` | sellable hoy; control contra piloto 2 (§9) |
| `CALC-DUELO-ENSAYO-ENVIPE2025-ADJUDICACION-0001` | este acto (P3 i), tras fijar el sha del ensayo de emisiones (COMMIT-3a del ensayo) | `adjudicacion`, abre 2025 | los mismos + `emisiones_selladas` | sellable hoy; EXD sale `NO-ADJUDICABLE-VETO` (rama terminal probada sobre oro) |
| `CALC-DUELO-ENVIPE2026-EMISIONES-0001` | **COMMIT-2, otra sesión** | `emisiones`, `ola_nueva = 2026` reservada | `envipe2023/2024/2025/2026_csv`, `serie_nd` | **NO congelado**: `envipe2026_csv` no está en el manifiesto (sin sha) — ver §10 |
| `CALC-DUELO-ENVIPE2026-ADJUDICACION-0001` | **COMMIT-3, otra sesión**; **COMMIT-3a** = fijar en su `spec.yaml` el `sha256` de `CALC-DUELO-ENVIPE2026-EMISIONES-0001/resultados.json` y nada más (previsto en el propio `spec.yaml`, `parametros.commit_3a`) | `adjudicacion`, abre 2026 | los mismos + `emisiones_selladas` | ídem |

Semilla `42`, `numpy.random.PCG64` (réplicas compartidas por ola, orden lexicográfico de estrato/UPM, 10 000; generador propio para E+); R nacional ND por el medidor sellado de la serie con su semilla `20260909`. Códigos y ponderadores: `BP1_20`, `BP1_23`, `FAC_DEL`, `EST_DIS`, `UPM_DIS`, `ID_PER`, `DOMINIO`, `SEXO`, `EDAD` de `tmod_vic`; `ID_PER`, `NIV` de `tsdem` — los del guardián y del piloto 2, leídos de los FD/catálogos citados en `TRA-evade-norma-sxd12-spec-v1_0.md` §0; para 2026 se **esperan** los mismos nombres y el sufijo de miembro `conjunto_de_datos_tmod_vic_envipe2026.csv`; si difieren, el guardián PARA en COMMIT-2 y eso es un hallazgo, no un parche.

**Guardia de una sola variable de agrupación sobre la ola nueva en emisiones:** la ola nueva se carga `reservada=True`; `marginal(ola, grupo: str)` un eje por firma; `cruce()` lanza `ReservaRota`; el medidor lo **prueba** en cada corrida (`…-G-RESERVA-GUARDIA-PROBADA`) y además prueba el veto de `edad × dominio` 2025. Emisiones **no emite** marginales crudos, nacional ni numerador de la ola nueva: sólo C2 (autorizado) y conteos que no revelan el estimando. El medidor de cada CALC es `tools/duelo/envipe_duelo.py` depositado **byte a byte** (E.5: el sello cubre el código que mide), y emite el sha256 de los módulos que importa.

## 9 · Ensayo de punta a punta sobre lo abierto (P3) — declarado antes de correrlo (E.5)

(i) «Como si 2025 fuera la ola nueva»: `ENSAYO-EMISIONES` con olas 2023/2024 abiertas y 2025 reservada debe reproducir, celda a celda a `1e-10`, el `C2` re-derivado del piloto 2 (`RESULT-TRA-SXD12-C2-P-REDERIVADO-*`), `P = C1` (`RESULT-TRA-SXD12-C1-P-*`) y `S1 = C7` (`RESULT-TRA-SXD12-C7-P-*`, la media de I23 e I24); `K` para EN = `0.538725312630215` (`…-W24-P-NACIONAL`) y para ND = fila 2024 de la serie; `ENSAYO-ADJUDICACION` debe reproducir `R` = `RESULT-TRA-SXD12-ARB-R-P-*` (12 celdas) y el nacional `G-M25-P-NACIONAL = 0.5627744787844097`, y `MAE(C2) = 1.5680517417942743` pp (`…-ARB-G-MAE-C2`) — mismo universo, misma receta, mismas 12 puntuadas. Tolerancia del tipo: `1e-10` flotante/proporción (seed y orden fijados), enteros exactos. (ii) Origen móvil §7. (iii) Sellabilidad: `_valida_outputs` vacío en cada rama terminal —incluida celda rara (`n = 0`) y `NO-ADJUDICABLE-VETO`— sobre sintético (`tests/test_duelo_prospectivo.py`) y sobre oro (los sellos del ensayo); cero no finitos (`None` y `NaN` cubiertos: todo `NaN` cae a `null` declarado).

Los sellos del ensayo son evidencia histórica de este acto (E.3); el COMMIT-2 real es un CALC distinto.

## 10 · «Congelado» según D-22 ampliada — qué queda y qué no

1. `preflight` VERDE sobre el commit final con main fusionado — **sí** para `ORIGEN-MOVIL` y los dos `ENSAYO`; **no** para los dos CALC de 2026: `envipe2026_csv` no existe en `data/manifiesto.yaml` (0 entradas, 21/sep/2026; censo de raíz `forense/censo-raiz/2026-09-21.txt`, 606 archivos, sin ENVIPE 2026; cola `data/cola-adquisicion-v1_0.tsv:158` `SOLICITUD-PRE-CONFIRMADA`, prioridad 1). El `spec.yaml` no puede fijar un input sin sha.
2. `_valida_outputs` acepta cada rama terminal sobre sintético y sobre oro — **sí** (§9 iii).
3. Todo id que el código pueda emitir nulo está declarado (`permite_no_estimable: true`) — **sí**, por lectura estática y por la prueba de celda rara.
4. Ningún input con hash sobre un archivo vivo — **sí**: los inputs repo son sellos (`resultados.json` de CALC sellados) y el TSV de la serie sellada.

**Conclusión:** el procedimiento queda **construido, ensayado y sellable**; el COMMIT-1 de 2026 queda **NO-CONGELADO por payload ausente** (requisito 1), con NC y sucesor «congelar cuando el payload entre»: al entrar `envipe2026_csv` al manifiesto con sha, la única edición autorizada es `preflight` VERDE sobre ese input — ningún parámetro, fórmula ni id cambia; si `preflight` bloquea por otra causa, se abre v1.1 por otra sesión.

## 11 · Lo que NO significa

Que una tendencia gane no dice por qué existe la regularidad. Un candidato que acierta en el nacional y falla en rural o en escolaridad baja no es buen candidato para México: por eso el desglose por eje (E+ vs persistencia; cruces) es obligatorio antes de cualquier frase de producto. Si todos yerran en el mismo sentido, es cambio de nivel del instrumento o del mundo, no veredicto. La unidad es DELITO: nada aquí se lee como «proporción de personas». Denunciar o no responde a confianza institucional, costo del trámite y tipo de delito —estructura e instituciones— antes que a disposición.

**El primer resultado que produzca este procedimiento es el que se reporta.**
