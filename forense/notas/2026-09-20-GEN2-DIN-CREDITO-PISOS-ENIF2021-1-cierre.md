# ACTO GEN2-DIN-CREDITO-PISOS-ENIF2021-1 · CIERRE — las 20 conductas de crédito K1–K7 tienen piso t−1 en ENIF 2021 por los seis ejes del marcador (`CALC-DIN-CREDITO-PISOS-ENIF2021-0001`, REPRODUCE/IDENTICO, `cuenta_gen2 = SI`, `envuelto_legacy = NO`)

**Universo, unidad, escala y clase de evidencia (primera línea obligatoria):** población de 18 años y más residente en viviendas particulares de México, ENIF 2021 (`TMODULO`, persona elegida, `FAC_ELE`, `EST_DIS × UPM_DIS`), 13 554 personas; unidad **P** (persona) para K1–K5 y K6-P-TENEDORES, **PR** (producto formal tenido / último crédito) para K6-PR y K7; escala: proporción ponderada en [0,1] con IC95 bootstrap; clase de evidencia **(a) dato primario en México**, GEN2, un solo procedimiento congelado antes de abrir el dato. Contadores que mueve: corridas GEN2 selladas +1 (`cuenta_gen2 = SI`, firma de mesa 21/sep/2026); RESULT +2 939; adopciones **0** (`usos.tsv`: cero filas nuevas, cero valores cambiados); `FP-404` → FIRMADA.

Encargo archivado por A.3: `forense/encargos/2026-09-21-GEN2-DIN-CREDITO-PISOS-ENIF2021-1.md` (sha256 `6f36a4a8…`; fechado 21/sep por mesa, ejecutado el 20/sep/2026 21:16–22:30 CST en CAJA).
Spec congelada (COMMIT-1 `ad93b0b3`): `forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-spec-v1_0.md` (sha256 `6119f4de…`, sidecar). Resultados (COMMIT-2 `56dc64ca`): `data/corrida0/CALC-DIN-CREDITO-PISOS-ENIF2021-0001/`.

## 0 · Arranque, compuerta, exposición

- `ENTORNO-DERIVADO = CAJA` (hook), `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, Opus 5, `tools/entorno.py --arranque` → `corpus=SI(examinados=419)`, `raices=data_raw:SI descargas_mx:SI`. Worktree nuevo `mm-gen2-din-credito-pisos-enif2021-1` sobre `origin/main` `5a888bcb` (8 commits después del SHA de redacción `04a2edeb`: `#932`–`#938`; no es PARO); `data/raw` enlazado y `raices.local.yaml` copiado a mano.
- Guard 0.c: rótulo ausente en `git ls-remote`, `git worktree list` (salvo el propio) y `gh pr list`. 0.d: 10 worktrees vivos, 8 ramas locales ya fusionadas, base al día.
- Compuerta: ninguna de merge. La única compuerta (abrir dato) es interna y se cumplió: spec md + sidecar + `spec.yaml` + `medidor.py` + test commiteados y empujados (`ad93b0b3`) antes del primer `preflight` VERDE.
- **Exposición (ADR-46):** tablas de identidad GEN2, medidores sellados de -0003 y -FORMALIDAD-0001, la tabla de comparabilidad de `#932`, y del ZIP sólo estructura (diccionario + 8 catálogos de sección 6). **Ningún microdato antes del COMMIT-1.** El `[SUPUESTO]` sobre `EST_DIS`/`UPM_DIS`/`FAC_ELE` se verificó contra el diccionario: existen con esa ortografía.
- Búsqueda «ya hecho» por objeto, repetida con acceso local: `data/corrida0` 189 entradas → 2 specs mencionan `P6_*` (`CALC-ENIF-FINTECH-0001`: el par reservado `P6_2_8 × P6_7`; `CALC-ENSAFI-DISENO-0001`: columna física) — **EXISTE-NO-SATISFACE**; `marcador-segmento.tsv` 216 filas → 0 con «cred»; `prereg-caja` 101 specs → 1 (`ENIF-FINTECH-SERIE`, el mismo par). `tools/ya_medido.py K1` → `NUNCA-MEDIDA`. El encargo no cita ningún id de regla del motor.

## 1 · P1 · Alcance y P2 · formalidad (citados, no decididos)

Reactivo, códigos, filtro y unidad de cada conducta salen de la fila `K·2021` de `data/credito-comparabilidad-texto-v1_0.tsv`, que el medidor recibe como input con sha256 y contrasta en ejecución (PARA si el reactivo no está en la fila; el test lo prueba rompiendo la fila de K5). K8 (`NO-ESTIMABLE` en 2021, verificado por el medidor) y K2-bancaria (`P6_2_2` no se lee) quedan fuera por `FP-404`. `formalidad` entra con el mapa de `PISOS-ENIF2021-formalidad-spec-v1_0.md` §1, universo quien trabaja, bajo la precedencia de `GEN2-MARCADOR-ENLACE-2` (#925): las cuatro filas `NO-CONSTRUIBLE` de la rejilla se filtran por `status`, no se editan.

## 2 · P3/P4/P5 · Resultados (`CALC-DIN-CREDITO-PISOS-ENIF2021-0001`, primera corrida, 8 s)

`enif2021_csv` (`0f314fa3…`), 13 554 personas + 6 613 filas producto; 2 011 UPM en el plan; 10 000 réplicas `PCG64(42)` en **una sola** llamada a `_estimate` (mismas llaves de diseño que -0003 y -FORMALIDAD-0001 → mismo plan). Tenedores 4 561; sin producto 8 993 (`P6_2` indefinido 0); nunca ha tenido 6 877; ex-usuarios 2 116; universo formalidad 8 805 (4 673 blanco, 76 no sabe — idéntico a -FORMALIDAD-0001). Flujo limpio: `P6_15` fuera de base 0, `P6_7` fuera de base 0 y blanco en tenedores 0, `P6_4` blanco en producto tenido 0; `P6_7 = 9` 17; `P6_4 ∈ {8,9}` 24 productos.

| conducta | U | p nacional [IC95] | n | p quien trabaja |
|---|---|---|---|---|
| K1 tenencia formal | P | 0.3125 [0.3021, 0.3228] | 13 554 | 0.3777 |
| K2-DEPARTAMENTAL | P | 0.1906 [0.1821, 0.1992] | 13 554 | 0.2242 |
| K2-NOMINA | P | 0.0209 [0.0180, 0.0239] | 13 554 | 0.0298 |
| K2-AUTOMOTRIZ | P | 0.0159 [0.0133, 0.0187] | 13 554 | 0.0219 |
| K3 informal (6.1) | P | 0.2921 [0.2816, 0.3024] | 13 554 | 0.3310 |
| K4A-AUTOEXCLUSION (6,7) | P | 0.5907 [0.5740, 0.6075] | 6 877 | 0.6139 |
| K4B-OFERTA (1,2,3) | P | 0.2831 [0.2675, 0.2991] | 6 877 | 0.2489 |
| K4B1-REQUISITOS · K4B2-ACCESO · K4B3-RECHAZO-ANTICIPADO | P | 0.2605 · 0.0136 · 0.0090 | 6 877 | 0.2282 · 0.0123 · 0.0084 |
| K5 rechazo (toda persona) | P | 0.1596 [0.1516, 0.1675] | 13 554 | 0.2010 |
| K5-ENTRE-SOLICITANTES | P | 0.3219 [0.3070, 0.3367] | 6 930 | 0.3585 |
| K6-PR atraso por producto | PR | 0.2240 [0.2072, 0.2415] | 6 589 | 0.2261 |
| K6-P-TENEDORES | P | 0.2627 [0.2457, 0.2803] | 4 543 | 0.2716 |
| K7 canal: SUCURSAL · APP · INTERNET · ESTABLECIMIENTO · PROMOTOR · OTRO | PR | 0.4860 · 0.0296 · 0.0167 · 0.3007 · 0.1548 · 0.0121 | 4 544 | 0.4928 · 0.0340 · 0.0207 · 0.2793 · 0.1624 · 0.0108 |

**Guardias (consecuencia en la spec, una sola vez):** (1) unidad: 20 `-UNIDAD` emitidas, cada celda pertenece a una sola conducta, nada se sumó ni promedió entre P y PR; (2) soporte: **360/360 celdas con n ≥ 200** (mínimo 616: K6-P-TENEDORES y K7 × edad 60+), ninguna rotulada `BAJO-N`; (3) coherencia: 240 controles (20 conductas × 6 ejes × num/den), delta máximo **3.7e-09** contra el marginal nacional (formalidad contra `UNIVERSO-TRABAJA`), el medidor no PARÓ. `B-VALIDAS = 10 000` en las 360.

Replay: `corrida0 verify` → REPRODUCE/IDENTICO; `tools/verifica_aislada.py` (proceso nuevo) → REPRODUCE/IDENTICO, 2 939/2 939 RESULT, 5/5 inputs COINCIDE, evidencia en `forense/analisis/gen2-din-credito-pisos-enif2021-1/evidencia-replay-din-credito-pisos-enif2021-2026-09-20.json`, asiento propio en `forense/replay-evidencia.tsv` antes de publicar (E.7). Registro: `corrida0 registro --verifica --escribe --lote CALC-DIN-CREDITO-PISOS-ENIF2021-0001,CALC-ENIF-0001--afbf3c76d71b` → corridas +1, resultados +2 939, `usos.tsv` +0. **`cuenta_gen2 = SI`, `envuelto_legacy = NO`** en la fila propia (inputs: `DATO=1, CODIGO=1, METADATO=3`, declarados con `funcion:` explícita; nada bajo `milpa/`). **Pisada ajena declarada (medida columna por columna contra `HEAD`):** la corrida `CALC-ENIF-0001--afbf3c76d71b` cambia `contexto_replay IDENTICO → DISTINTO` y `fuente_replay → VERIFY-NUEVO-EN-NUBE · ACTO GEN2-NUBE-PILOTO-1-bis` (1 fila en `corridas.tsv`, 188 en `resultados.tsv`, 8 en `usos.tsv`, sólo esas dos columnas). Causa verificable en `origin/main`: el asiento de `#935` (`cf1ba17f`, `forense/replay-evidencia.tsv:148`, `dependencias_distintas` numpy 2.4.6 en nube) ya estaba publicado y la vista no lo había proyectado; `verify` propio y aislado de `CALC-ENIF-0001` en esta CAJA sigue dando IDENTICO. No es un cambio de esta sesión: se nombró en `--lote` como pide `NC-0094` y se declara aquí. Ninguna otra fila ajena cambió.

Tabla de identidad propia: `forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-metadatos-v1_0.tsv` (320 filas `CONSTRUIBLE` = 20 conductas × 16 categorías, `cell_id` = RESULT `-P`, `unit` con la unidad P/PR, `consumer = PENDIENTE:piloto-credito-2024 (K)` porque el árbitro 2024 aún no tiene reglas de crédito) + sidecar. Test `tests/test_din_credito_pisos_enif2021.py` (sintético D-22 + sellado; sin corpus, `CORRE-EN-CI`), censado en `forense/analisis/ci-guardias/censo-tests.tsv`.

## 3 · P6 · Lo que el piso deja dicho (viaja al piloto de crédito)

Por conducta y eje: **n mínimo de celda · anchura máxima de IC95** (todas las celdas tienen piso; ninguna bajo soporte).

| conducta | sexo | edad | escolaridad | localidad | cuenta | formalidad |
|---|---|---|---|---|---|---|
| K1 | 6209 · 0.030 | 2774 · 0.042 | 2969 · 0.048 | 4989 · 0.027 | 6355 · 0.032 | 3852 · 0.043 |
| K2-DEPARTAMENTAL | 6209 · 0.024 | 2774 · 0.036 | 2969 · 0.045 | 4989 · 0.023 | 6355 · 0.028 | 3852 · 0.038 |
| K2-NOMINA | 6209 · 0.010 | 2774 · 0.015 | 2969 · 0.018 | 4989 · 0.008 | 6355 · 0.012 | 3852 · 0.020 |
| K2-AUTOMOTRIZ | 6209 · 0.010 | 2774 · 0.013 | 2969 · 0.019 | 4989 · 0.008 | 6355 · 0.010 | 3852 · 0.015 |
| K3 | 6209 · 0.028 | 2774 · 0.042 | 2969 · 0.045 | 4989 · 0.031 | 6355 · 0.030 | 3852 · 0.040 |
| K4A-AUTOEXCLUSION | 3056 · 0.047 | 1498 · 0.070 | 901 · 0.086 | 3111 · 0.049 | 2709 · 0.052 | 1227 · 0.069 |
| K4B-OFERTA | 3056 · 0.044 | 1498 · 0.065 | 901 · 0.075 | 3111 · 0.047 | 2709 · 0.046 | 1227 · 0.057 |
| K4B1-REQUISITOS | 3056 · 0.042 | 1498 · 0.063 | 901 · 0.065 | 3111 · 0.045 | 2709 · 0.044 | 1227 · 0.056 |
| K4B2-ACCESO | 3056 · 0.011 | 1498 · 0.022 | 901 · 0.016 | 3111 · 0.012 | 2709 · 0.011 | 1227 · 0.014 |
| K4B3-RECHAZO-ANTICIPADO | 3056 · 0.010 | 1498 · 0.016 | 901 · 0.036 | 3111 · 0.011 | 2709 · 0.010 | 1227 · 0.012 |
| K5 | 6209 · 0.025 | 2774 · 0.038 | 2969 · 0.041 | 4989 · 0.023 | 6355 · 0.024 | 3852 · 0.037 |
| K5-ENTRE-SOLICITANTES | 3368 · 0.044 | 1147 · 0.068 | 1302 · 0.064 | 1923 · 0.042 | 2437 · 0.052 | 2441 · 0.051 |
| K6-PR | 3191 · 0.049 | 824 · 0.084 | 738 · 0.078 | 1549 · 0.057 | 1472 · 0.071 | 1953 · 0.063 |
| K6-P-TENEDORES | 2145 · 0.051 | 616 · 0.089 | 623 · 0.084 | 1200 · 0.060 | 1244 · 0.071 | 1471 · 0.062 |
| K7-SUCURSAL | 2141 · 0.056 | 616 · 0.113 | 626 · 0.103 | 1207 · 0.070 | 1248 · 0.070 | 1471 · 0.067 |
| K7-APP | 2141 · 0.021 | 616 · 0.038 | 626 · 0.029 | 1207 · 0.020 | 1248 · 0.020 | 1471 · 0.025 |
| K7-INTERNET | 2141 · 0.019 | 616 · 0.034 | 626 · 0.025 | 1207 · 0.015 | 1248 · 0.031 | 1471 · 0.027 |
| K7-ESTABLECIMIENTO | 2141 · 0.050 | 616 · 0.094 | 626 · 0.086 | 1207 · 0.063 | 1248 · 0.070 | 1471 · 0.062 |
| K7-PROMOTOR | 2141 · 0.040 | 616 · 0.081 | 626 · 0.074 | 1207 · 0.043 | 1248 · 0.054 | 1471 · 0.051 |
| K7-OTRO | 2141 · 0.014 | 616 · 0.016 | 626 · 0.018 | 1207 · 0.010 | 1248 · 0.012 | 1471 · 0.014 |

Dónde un retador tiene margen: los IC más anchos (≥ 0.08) están en las conductas de tenedores (K6, K7) por `edad` y `escolaridad`, y en K4A por `escolaridad`; K2-NOMINA, K2-AUTOMOTRIZ, K4B2/K4B3, K7-APP/INTERNET/OTRO son conductas raras (p < 0.03) con IC estrechos en absoluto pero anchos en relativo — un piso de persistencia ahí acota poco y un retador que acierte el signo no gana nada.

## 4 · Auditoría (§5 de las instrucciones), tres líneas obligatorias

1. **Lo que parece psicológico y es oferta.** K1 sube de 0.282 [0.266, 0.299] sin seguridad social a 0.505 [0.483, 0.526] con ella, y de 0.226 a 0.360 entre localidad < 15 000 y ≥ 15 000; K4B1 «no cumple requisitos» baja de 0.280 (hasta primaria) a 0.195 (superior) mientras K4A «no le interesa / no le gusta endeudarse» sube de 0.550 a 0.636. Una tasa baja de crédito formal en un segmento **no dice nada sobre su preferencia** mientras K4(b) y K5 no se lean al lado: el piso se publica con esta advertencia pegada, y K4A no se lee como «cultura» (es la razón principal declarada por quien nunca tuvo crédito, después de que la oferta filtró).
2. **Sobregeneralización.** ENIF es población de 18+ en viviendas particulares y sobre-representa al urbano bancarizado; `formalidad` se restringe además a quien trabaja (8 805 de 13 554). 2021 es dato de pandemia («de julio de 2020 a la fecha»). Un marginal leído aquí no es «el mexicano», es esa población en esa ventana.
3. **Escala.** Cada cantidad lleva `-UNIDAD` (P o PR). K6-PR (0.224 de los productos) y K6-P-TENEDORES (0.263 de las personas con producto) **no son la misma cantidad** ni se comparan sin función de enlace; K7 (canal del último crédito) tampoco se cruza con K2 porque el instrumento no dice cuál producto es «el último». El piso de crédito no se compara contra el de ahorro salvo por signo y razón dentro de la misma corrida — y esta corrida no trae ahorro.

## 5 · Perímetro y contadores

| pieza | estado |
|---|---|
| P1 alcance leído de la tabla · P2 formalidad citada | hecho, en la spec §1, §3 |
| P3 COMMIT-1 | `ad93b0b3` (spec md + sidecar, spec.yaml, medidor, test; D-22 sobre sintético) |
| P4 COMMIT-2 con tres guardias | `56dc64ca` (CALC sellado, tabla de identidad, replay aislado, vistas) |
| P5 rejilla de la tabla de identidad GEN2 | hecho; `milpa/` no se lee (`envuelto_legacy = NO`) |
| P6 tabla corta | §3 de esta nota |
| enlace de la tabla de crédito al marcador | **no se hace**: `tools/marcador_segmento.py` y `marcador-segmento.tsv` son perímetro de dirección (`NC-0449`, sucesor: piloto de crédito) |
| cascada | `ADR-581`, L0, rótulo, `FP-404` FIRMADA, `NC-0449`, hallazgo, `INFRAESTRUCTURA`, censo CI |

No tocado: specs, CALC y tablas de identidad de ahorro; `milpa/` entero; `marcador-segmento.tsv`; `data/curacion-registro/celdas-d/`; `data/credito-comparabilidad-texto-v1_0.tsv` (se lee, con sha256); ENIF 2024, ENIGH, ENSAFI, ENFIH. Sucesores en el orden del encargo §10: regla de elección del cruce del piloto de ahorro (dirección) → piloto de crédito (usa esta tabla) → K8 triangulada → descriptivo rotulado de K2-bancaria → adquisición de cuestionarios 2012/2015 (`NC-0433`).

**Falsador de este acto, a tres meses:** si el piloto de crédito tiene que re-medir algún marginal de 2021 que este CALC ya selló, el piso no sirvió y se revisa el diseño de celdas.
