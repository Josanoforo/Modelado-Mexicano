# ACTO GEN2-B-MARCO · EL TERCER BRAZO DEJA DE SER TESTIGO DE DOS CELDAS — nota de cierre del lote

**Fecha:** 14/sep/2026 · **Entorno:** CAJA (Ubuntu/WSL), corpus montado (`tools/entorno.py`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · red=200 · corpus=SI(examinados=412)`) · **Base:** `origin/main = 11c8783` (`PR #754`) · **Rama:** `acto/gen2-b-marco` · **Encargo:** `forense/encargos/2026-09-14-GEN2-B-MARCO.md` · **Spec sellada:** `prereg-caja-B-MARCO` (`forense/prereg-caja/B-MARCO-spec-v1_0.md`, `sha256 e61969b9…`) · **Compuerta:** ninguna.

## 0 · Qué se pidió y qué salió

| pieza | pedido | salió |
|---|---|---|
| **P1** | censo de extensibilidad de `B` a las 12 celdas sin `B`, con cita; spec familia congelada con reglas por serie | **HECHO.** 8 construibles (6 ENVIPE, 1 ENCIG, 1 ENIGH), 4 no (DIN-M-01, FAM-M-01, TRA-M-02, TRA-M-03), cada una con cita al codebook (§1). Spec sellada en `COMMIT-1` (`040ad64`) antes de abrir microdato, con la frase de sello |
| **P2** | `CALC-B` por serie construible, embudo, escala, `MAE_pp(B)` con su `n` | **HECHO.** `CALC-B-MARCO-ENVIPE-0001` (226 RESULT), `-ENCIG-0001` (45), `-ENIGH-0001` (45), `-MAE-0001` (155): las cuatro `SELLADA`, `verify REPRODUCE · CONTEXTO=IDENTICO`. `MAE_pp(B)`: **0.9229 pp (n = 10, PERSISTENCIA)** y **0.6515 pp (n = 5, OPERATIVO)** |
| **P3** | asiento para el próximo duelo: cobertura antes/después, tabla por celda, §0.2 propagada, frontera; cierre de `NC-0079` | **HECHO.** Cobertura **2 → 10 de 14** (PERSISTENCIA), **0 → 5** (OPERATIVO). Tabla en §3. `NC-0079` CERRADA con cita. La tríada **no** se re-corre |

**Contador, sin adornos:** se movió. Tres CALC-B de serie **GEN2 limpios** con firma de contador con objeto (`decisiones.tsv`, citando el párrafo del encargo; el merge de mesa la perfecciona): `N_corridas_selladas 59 → 62`, `N_resultados_gen2_sellados 2 497 → 2 813`. El asiento (`MAE`) es `envuelto_legacy = SI` por construcción (lee `corridas-R`): `corredores_envueltos_legacy 17 → 18`, sin firma, como la spec pre-declaró en §7.7. Cero adopciones (`usos.tsv`: 0 filas nuevas).

## 1 · P1 · El censo, y las cuatro celdas que no se rellenan

La regla es la de la familia (`CALC-B-0001`): persistencia de la **última ola de la MISMA serie disponible al corte**, selector `tools/baseline_temporal.py` sin tocar, dos brazos (`OPERATIVO` = versión en corpus; `PERSISTENCIA` = cierre de la ola), bootstrap de UPM dentro de estrato copiado verbatim, misma semilla. Una celda es construible sólo si existe predecesora de la misma serie **sin crosswalk** — el selector lo dice en su docstring y esta spec lo tomó como criterio único.

| celda | veredicto | por qué (cita en la sellada §1) |
|---|---|---|
| CIV-M-01/02/04/10/12/13 (ENVIPE) | **CONSTRUIBLE** | predecesoras 2011 (`BP1_21`, renombre nominal), 2012, 2014 (DBF, `EST`/`UPM`), 2020, 2022, 2023 (CSV, `EST_DIS`/`UPM_DIS`); descriptores DBF y cabeceras CSV verificados |
| TRA-M-07 (ENCIG 2021) | **CONSTRUIBLE** | ENCIG 2019 `P8_3_1`, texto idéntico al de 2021 (`encig19_estructura_base_datos.pdf` reactivo 220) |
| FAM-M-05 (ENIGH 2016) | **CONSTRUIBLE** | ENIGH 2014 NCV `concentradohogar.remesas` (misma definición), ponderador `factor_hog` (renombre). Es la extensión hacia atrás que `B-REMESAS` §0.1 dejó a un sucesor |
| DIN-M-01 (ENNViH-1 2002) | **NO** · primera ola del panel | 29 entradas ENNViH en el manifiesto, ninguna anterior a 2002 |
| FAM-M-01 (ENIF 2018) | **NO** · reactivo ausente en 2015 y 2012 | la batería 9.9 («En su vejez, ¿piensa cubrir sus gastos con… dinero de familiares?») **nace en 2018**; `enif_2015_fd.xlsx` y `fd_enif2012.xlsx`: 0 coincidencias fuera de un motivo de ahorro (`P5_17_8`) |
| TRA-M-02 (ENCUCI 2020) | **NO** · serie de una sola ola | 2 entradas ENCUCI, ambas 2020. Un `B` desde ENCIG sería crosswalk (y ENCUCI mide pedir∨dar; ENCIG sólo pedir) |
| TRA-M-03 (ENCIG 2013) | **NO** · reactivo ausente en 2011 | ENCIG 2011 no tiene sección VIII: sólo `P4_13` **por trámite** en `03_ENCIG2011_TRAMITES` (otra unidad, otro reactivo, otro universo) |

**Lo que la prueba sintética atrapó antes de congelar** (y por eso hubo un solo `COMMIT-1`, sin `-bis`): el selector valida `disponible_desde ≥ periodo_fin`, y ENVIPE se publica en **septiembre** del año de encuesta (`Modified = 2020-12-10` < `2020-12-31`). Se declaró en §3 de la sellada la acotación `disponible_desde(OPERATIVO) = max(versión, cierre de ola)`, que nunca cambia la selección. Otro hallazgo de formato: los CSV de ENVIPE 2020–2024 terminan línea con `\r` solo.

## 2 · P2 · Las series, medidas — y los dos controles positivos

### 2.1 · Control de familia (sellada §6.3): ENIGH 2016 reproduce a `CALC-B-0001` **al bit**

| RESULT | `CALC-B-MARCO-ENIGH-0001` | `CALC-B-0001` | |
|---|---|---|---|
| `…-2016-P` | 0.04745859252351374 | 0.04745859252351374 | IDÉNTICO |
| `…-2016-IC-LO` | 0.04509768667793412 | 0.04509768667793412 | IDÉNTICO |
| `…-2016-IC-HI` | 0.049758949295394074 | 0.049758949295394074 | IDÉNTICO |
| `…-2016-N` | 70 311 | 70 311 | IDÉNTICO |

El bootstrap es el de la familia, no una re-implementación. Y ENIGH 2014 da `P = 0.040784`, que es la cifra GEN1 de `serie_olas` (`B-REMESAS` §0.2, ya leída entonces) al sexto decimal.

### 2.2 · Control positivo por celda (sellada §6.1): **10 de 10 `REPRODUCE-EXACTO`**, `Δ = 0.0` en las diez

`RESULT-BM-MAE-<celda>-CONTROL-R-DELTA = 0.0` (no `≈ 0`: cero exacto en `float64`) para CIV-M-01/02/04/10/12/13, FAM-M-05/06/07 y TRA-M-07. El medidor mide **el mismo estimando que el árbitro `R`** de cada celda, bit a bit — y los `N` por ola coinciden con `n_efectivo` de `corridas-R` (2012: 26 848 · 2013: 40 889 · 2015: 39 286 · 2021: 32 967 · 2023: 31 012 · 2024: 33 108 · ENCIG 2021: 39 763 · ENIGH 2016: 70 311). Sin este control, un `err_pp(B)` chico podría ser un `B` bueno o un estimando distinto; con él, `err_pp(B)` es comparable con los `err_pp` de `M` y `L` por construcción.

### 2.3 · ENVIPE — diez olas, seis objetivos

| ola | `P` | IC95 (bootstrap) | `N` | leídas | fuera de código | veredicto |
|---|---|---|---|---|---|---|
| 2011 (`BP1_21`) | 0.256514 | [0.241766, 0.272378] | 22 485 | 27 186 | 4 701 | SERIE-REPORTADA |
| 2012 | 0.258999 | [0.245775, 0.271521] | 26 848 | 32 493 | 5 645 | SERIE-REPORTADA |
| 2013 | 0.243400 | [0.231782, 0.255847] | 40 889 | 47 117 | 6 228 | SERIE-REPORTADA |
| 2014 | 0.275212 | [0.259526, 0.290388] | 38 068 | 43 478 | 5 410 | SERIE-REPORTADA |
| 2015 | 0.243668 | [0.229860, 0.258437] | 39 286 | 44 699 | 5 413 | SERIE-REPORTADA |
| 2020 | 0.203809 | [0.193398, 0.213680] | 33 717 | 38 575 | 4 858 | SERIE-REPORTADA |
| 2021 | 0.204934 | [0.196516, 0.214319] | 32 967 | 37 156 | 4 189 | SERIE-REPORTADA |
| 2022 | 0.213125 | [0.203427, 0.222328] | 32 052 | 36 144 | 4 092 | SERIE-REPORTADA |
| 2023 | 0.208112 | [0.199447, 0.217463] | 31 012 | 35 135 | 4 123 | SERIE-REPORTADA |
| 2024 | 0.194612 | [0.184809, 0.204783] | 33 108 | 37 614 | 4 506 | SERIE-REPORTADA |

`N-SIN-PONDERADOR = 0` y `N-SIN-DISENO = 0` en las diez. «Fuera de código» = NS/NR + blanco (quien sí denunció): el embudo completo está en `resultados.json`.

| objetivo (celda) | `OPERATIVO` | `PERSISTENCIA` |
|---|---|---|
| 2012 (CIV-M-01) | `SIN_BASELINE` (2011 versionada 2013-08-12) | EMITE desde 2011 · `B = 0.256514` · dentro del IC95 observado (margen +0.0107) |
| 2013 (CIV-M-02) | `SIN_BASELINE` (2012 y 2011 versionadas en 2013) | EMITE desde 2012 · `B = 0.258999` · fuera (−0.0032) |
| 2015 (CIV-M-04) | **EMITE desde 2013** (2014 versionada 2015-06-24; la última disponible está dos olas atrás) · `B = 0.243400` · dentro (+0.0135) | EMITE desde 2014 · `B = 0.275212` · fuera (−0.0168) |
| 2021 (CIV-M-10) | EMITE desde 2020 · `B = 0.203809` · dentro (+0.0073) | ídem |
| 2023 (CIV-M-12) | EMITE desde 2022 · `B = 0.213125` · dentro (+0.0043) | ídem |
| 2024 (CIV-M-13) | EMITE desde 2023 · `B = 0.208112` · fuera (−0.0033) | ídem |

`N-PREDICCIONES`: OPERATIVO 4, PERSISTENCIA 6 — **exactamente lo que §6.2 de la sellada derivó de los metadatos antes de correr.** Lectura B-bis: `MIXTO` en los dos brazos.

### 2.4 · ENCIG y ENIGH

- **ENCIG:** 2019 `P = 0.084484` [0.079475, 0.089706] (`N` 39 454 de 39 625 leídas, 171 fuera de código); 2021 `P = 0.071815` [0.067500, 0.076639] (`N` 39 763 de 39 930, 167 fuera). Los dos brazos EMITEN desde 2019 (`Modified 2020-05-21`, acotado a 2019-12-31): `B = 0.084484`, fuera del IC observado (margen −0.0078). Lectura `PISO-BAJO` en ambos.
- **ENIGH:** 2014 `P = 0.040784` [0.036629, 0.045136] (`N` 19 479, 0 nulos), 2016 `P = 0.047459` [0.045098, 0.049759] (`N` 70 311, 0 nulos). `OPERATIVO` `SIN_BASELINE` (2014 versionada 2019-10-03); `PERSISTENCIA` EMITE desde 2014, `B = 0.040784`, fuera del IC (margen −0.0043). `PISO-BAJO`.

## 3 · P3 · El asiento — cobertura, tabla por celda, y la frontera

**Cobertura de `B` antes/después:** `PERSISTENCIA` **2 → 10 de 14**; `OPERATIVO` **0 → 5 de 14** (`CALC-B-0001` no emitía `OPERATIVO` en 2018 ni 2020). Las 4 restantes `SIN-B` con su razón (§1), sin rellenar.

**Advertencia §0.2, propagada** (y ampliada por el encargo): `B` **no es ciego**. `B-REMESAS` §0.2 ya había leído la serie GEN1 de remesas; este acto declara contaminación TOTAL — los `R`/`M`/`L` de las 14 celdas están en el repo — y por eso su regla es fija, tonta y pre-declarada por serie, sin ningún parámetro que una sesión pueda calibrar hacia un resultado. Toda lectura de `B` viaja con esta advertencia.

**La tabla por celda — descriptiva.** `err_pp = 100·(punto − R)`, puntos porcentuales de una proporción ponderada (A-bis.3). `B` de este acto y de `CALC-B-0001`; `M`, `L_SOLO`, `L_CORPUS` y `EE_R` copiados de `CALC-C0D-MARCADOR-v3` (sellado, no re-corrido). La última columna dice si `|err_pp(B)| ≤ 1.96·EE_R·100`, es decir si `B` cae dentro del ruido muestral del propio árbitro — descripción, no adjudicación.

| celda | `R` | `B`·PERSISTENCIA | `B`·OPERATIVO | `M` | `L_SOLO` | `L_CORPUS` | 1.96·EE_R (pp) | `B` dentro del ruido de `R` |
|---|---|---|---|---|---|---|---|---|
| CIV-M-01 | 0.258999 | **−0.2485** | — | +3.5314 | −1.2749 | +4.1001 | 1.3663 | SÍ |
| CIV-M-02 | 0.243400 | **+1.5599** | — | +5.0913 | +60.6600 | +53.9934 | 1.2226 | NO |
| CIV-M-04 | 0.243668 | +3.1544 | **−0.0269** | +5.0645 | — | +61.3832 | 1.4668 | NO (PERS) · SÍ (OP) |
| CIV-M-10 | 0.204934 | **−0.1125** | −0.1125 | +8.9379 | +17.0066 | +49.8066 | 0.9356 | SÍ |
| CIV-M-12 | 0.208112 | **+0.5014** | +0.5014 | +8.6201 | +1.6888 | +25.5013 | 0.9330 | SÍ |
| CIV-M-13 | 0.194612 | **+1.3500** | +1.3500 | +9.9701 | +18.3960 | +9.9763 | 1.0567 | NO |
| DIN-M-01 | 0.155581 | — | — | +1.9223 | +5.3794 | +18.1919 | 0.9450 | — |
| FAM-M-01 | 0.557193 | — | — | −9.9486 | −28.8443 | −32.9693 | 1.3263 | — |
| FAM-M-05 | 0.047459 | −0.6675 | — | **−0.1765** | −0.1334 | −0.1584 | 0.2474 | NO |
| FAM-M-06 | 0.047285 | **+0.0173** | — | −0.1591 | +0.1465 | −0.0035 | 0.2343 | SÍ |
| FAM-M-07 | 0.043775 | +0.3510 | — | **+0.1919** | +0.9100 | +0.7850 | 0.1983 | NO |
| TRA-M-02 | 0.126025 | — | — | −4.0907 | +2.5225 | +2.3975 | 0.9918 | — |
| TRA-M-03 | 0.044538 | — | — | +4.0580 | +7.7962 | +7.6712 | 0.5569 | — |
| TRA-M-07 | 0.071815 | **+1.2669** | +1.2669 | +1.3303 | +7.2435 | +7.5185 | 0.4697 | NO |

(`FAM-M-06 +0.0173` es, al dígito, la cifra que `NC-0079` citaba como «el dato que lo hace urgente» y la que `CALC-C0D-MARCADOR-v3` sella en `RESULT-C0D-B-FAM-M-06-PERSISTENCIA-ERRPP`: tres cadenas, un número.)

**`MAE_pp(B)`, con su `n`, y los otros brazos SOBRE EL MISMO UNIVERSO (A-bis.4) — descriptivo, sin IC, sin ordenación adjudicada:**

| universo | `MAE_pp(B)` | `MAE_pp(M)` | `MAE_pp(L_SOLO)` | `MAE_pp(L_CORPUS)` | celdas con `|B| < |M|` | con `|B| < |L_SOLO|` |
|---|---|---|---|---|---|---|
| 10 celdas con `B`·PERSISTENCIA | **0.9229** (n=10) | 4.3073 (n=10) | 11.9399 (n=9; CIV-M-04 sin punto `L_SOLO`) | 21.3226 (n=10) | 8 de 10 | 8 de 9 |
| 5 celdas con `B`·OPERATIVO | **0.6515** (n=5) | 6.7846 (n=5) | 11.0837 (n=4) | 30.8372 (n=5) | 5 de 5 | 4 de 4 |

Los `MAE` de `M`/`L` sobre 14 y 13 celdas del marcador (`4.5066`, `11.6925`, `19.6040` marginales) **no se comparan** contra estos: otro universo. Las dos celdas donde `M` le gana a `B` son las dos de remesas con ola previa a 2018 (FAM-M-05, FAM-M-07); en las seis de ENVIPE y en la de ENCIG la línea base tonta yerra menos que `M` y que los dos `L`.

**Lo que esta tabla NO hace:** no re-adjudica la tríada. `RESULT-C0D-VEREDICTO-PAREADA = NO-DISCRIMINA` y `RESULT-C0D-ADJUDICACION-HALLAZGO = INCONCLUSO` quedan intactos; `SIN-GANADOR-UNICO` no se toca. **Frontera:** `B` extendido —`RESULT-BM-MAE-<celda>-{PERSISTENCIA,OPERATIVO}-P-B` y los `RESULT-BM-<SERIE>-…-P` que lo respaldan— queda **DISPONIBLE** para la próxima corrida de tríada que mesa autorice, con piso de 10 celdas bajo `PERSISTENCIA`; **este acto no re-corre ningún duelo.**

## 4 · Registro GEN2 — lo que se escribió, y las pisadas medidas

`python3 tools/corrida0.py registro --verifica --escribe --lote …`. La guardia `NC-0094` paró la primera escritura: seis corridas **ajenas** cambiarían de veredicto de replay. Cada causa se verificó contra `origin/main` antes de nombrar nada (y `git log acto/gen2-b-marco --not origin/main -- tools/baseline_temporal.py milpa/procedencia.yaml milpa/tramite.yaml` → 0 commits míos):

| corrida | transición | causa verificada | ¿en `--lote`? |
|---|---|---|---|
| `CALC-B-0001` | `REPRODUCE/IDENTICO → REPLICA-RESULTADO · CONTEXTO-DISTINTO/DISTINTO` | `input_cambiado=IN-B-SELECTOR`: `tools/baseline_temporal.py` cambió en `origin/main` en `67aa13d` (11/sep, «autentica selecciones de transferencia»). El **resultado reproduce**; el contexto no | SÍ |
| `CALC-MOTOR-celdas-semilla` / `-v2` | contexto `IDENTICO → DISTINTO` | `input_cambiado=IN-PROCEDENCIA`: `milpa/procedencia.yaml` cambió en `15e02c4` (11/sep) | SÍ |
| `CALC-F5-REANALISIS-0001`, `CALC-SHED2025-BNPL-DANO-0001` | `NO-VERIFICADO → REPRODUCE/IDENTICO` | columnas blanqueadas por un `registro` anterior sin `--verifica` (defecto conocido); `--verifica` las llena con lo observado | SÍ |
| `CALC-M-marco-M-sorteado-v1_3` | proyectó `NO-REPRODUCE` en la primera pasada; `REPLICA-RESULTADO` en la segunda y en `verify` aislado (2 de 2) | veredicto **inestable dentro del proceso** de `registro --verifica`; en aislamiento reproduce | **NO** — no se publica un veredicto que no se sostiene aislado |

**Pisadas medidas** (`git show origin/main:<tsv> | grep -v B-MARCO` vs. árbol, columna por columna): `corridas.tsv` 70 filas ajenas cambian **sólo** en `fuente_replay` (`HEREDADO-DEL-REGISTRO-PUBLICADO → VERIFY-EN-ESTA-SESION`: las 70 se re-verificaron de verdad, con corpus) más las 5 transiciones autorizadas; `resultados.tsv` 2 503 filas, misma columna única; `usos.tsv` 16 filas, misma columna única, **0 filas nuevas** (cero adopciones, mecánicamente). Los dos `NO-VERIFICADO` heredados quedaron en 0. Tres avisos `REPLAY-CONTRADICE-ASIENTO` persisten (`forense/replay-evidencia.tsv` sigue diciendo `IDENTICO` para `CALC-B-0001` y los dos `MOTOR`): actualizar ese asiento está **fuera del perímetro** de este acto → `NC` en §6.

## 5 · Contadores

| contador | antes (`origin/main`) | después | por qué |
|---|---|---|---|
| `N_corridas_selladas` | 59 | 62 | los tres CALC-B de serie, GEN2 limpios |
| `N_resultados_gen2_sellados` | 2 497 | 2 813 | +226 +45 +45 |
| `corredores_envueltos_legacy` | 17 | 18 | `CALC-B-MARCO-MAE-0001`, por construcción (lee `corridas-R`) |
| `cuenta_gen2 = SI` (firma con objeto) | — | 3 | `decisiones.tsv`, citando el párrafo del encargo; el merge perfecciona |
| adopciones | — | 0 | ningún RESULT de `B` es una `p` de conducta, coeficiente, corte ni momento |
| `no_corrido_abiertas` | 61 | 61 + 4 − 1 | `NC-0079` CERRADA; cuatro filas nuevas (§6) |

## 6 · Registro de filas

- **`NC-0079` — CERRADA** por este acto: `B` cubre 10 de 14 (PERSISTENCIA), `MAE_pp(B)` se calcula con su `n` (`RESULT-BM-MAE-PERSISTENCIA-MAE-PP = 0.9229`, `-N-CELDAS = 10`), y `B` entra a un asiento comparable por celda (§3). Lo que la fila pedía como sucesor («acto propio que extienda B fuera de la serie ENIGH × recibe_remesas — un B nuevo por serie») es exactamente este acto.
- **Nuevas** (`forense/no-corrido.tsv`): (a) las 4 celdas no-construibles — `PARO-PREMISA`, sucesor: mesa, si autoriza un `B` por crosswalk (fuera de la familia); (b) la próxima tríada con `B` de cobertura real — `DECISIÓN-DE-MESA-PENDIENTE`; (c) los tres asientos de `replay-evidencia.tsv` desactualizados por inputs cambiados en `origin/main` — `FUERA-DE-PERÍMETRO`; (d) el veredicto inestable de `CALC-M-marco-M-sorteado-v1_3` dentro de `registro --verifica` — `NO-VERIFICABLE-AQUÍ`.

## 7 · Contaminación declarada (ADR-46)

Total, por el encargo y por §0.2 de la sellada. Al congelar, esta sesión leyó **estructura**: descriptores DBF, cabeceras CSV, metadatos, FD/PDF/XLSX de codebooks, y las llaves de definición de `corridas-R/*.json` por un extractor que excluyó `R`, `EE_R`, `cv`, `ic95_*`. Los valores de `R` entraron **después** de sellar los tres CALC de serie, sólo en `CALC-B-MARCO-MAE-0001`; los de `M`/`L` sólo para la tabla descriptiva de §3, ya con todo sellado. Ninguna decisión de la spec depende de un valor: no hay umbral, ventana ni filtro elegido. Lo que no puedo probar: que no recordara las tres cifras que `NC-0079` cita en prosa.

## 8 · A.13 — qué se examinó, y con qué

`data/manifiesto.yaml`: 1 608 entradas (77 ENVIPE · 38 ENCIG · 22 ENIF · 29 ENNViH · 2 ENCUCI · 6 ENIGH). `data/corrida0/`: 94 directorios (2 con `CALC-B` por subcadena, 1 `B` real). Microdato leído por los medidores: ENVIPE 10 tablas `TMod_Vic` (379 597 filas, 5 DBF + 5 CSV), ENCIG 2 tablas (79 555), ENIGH 2 (89 790). `spec-check`: 40 · 8 · 8 pares (miembro, variable) `OK`, 0 `FAIL` sobre 317 718 filas de inventario. `registro --verifica`: 163 corridas re-verificadas en esta caja. Negativos declarados con su universo: batería 9.9 en ENIF 2015/2012 (todas las hojas de dos FD, 0 coincidencias); sección VIII en ENCIG 2011 (FD completo, 3 tablas); ola previa a 2002 en ENNViH y a 2020 en ENCUCI (manifiesto completo).

## 9 · Higiene e incidentes

1. `git push -u` falló al escribir `.git/config` («Device or resource busy», sandbox): la rama se empujó igual; se usó refspec explícito en adelante.
2. Ningún `.claude/` espurio: se verificó `forense/prereg-caja/.claude` y `data/corrida0/.claude` ausentes; todos los `git add` por ruta explícita.
3. `tests/check.py --baseline` no dejó `demanda-*.tsv` modificados (`git status --porcelain` vacío antes y después).
4. Un worktree ajeno `mm-gen2-diseno-fase1-cierre` (rama `acto/gen2-diseno-fase1-cierre`, `HEAD = 11c8783`, limpio, sin commits) existía al arrancar: es el sucesor gateado a este merge; no se tocó.
5. El clon padre `/home/pc0/Modelado-Mexicano` estaba en `censo/2026-09-11`, 317 commits detrás: la caja se creó sobre `origin/main` fresco y `/acto` se leyó desde ella.
