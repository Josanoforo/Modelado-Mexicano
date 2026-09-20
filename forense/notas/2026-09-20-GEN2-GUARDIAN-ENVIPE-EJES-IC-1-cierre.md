# ACTO GEN2-GUARDIAN-ENVIPE-EJES-IC-1 · nota de cierre

**20/sep/2026 · CAJA (Ubuntu/WSL2, corpus montado) · Opus 5 · `ADR-560` · rama `acto/gen2-guardian-envipe-ejes-ic-1`**
Encargo (A.3): `forense/encargos/2026-09-20-GEN2-GUARDIAN-ENVIPE-EJES-IC-1.md` · base `1bb9e2c4` (se movió 20 commits; fusionado en `c0f500d`).
Sucede a `GEN2-C2-COMPUESTO-IC-ENVIPE2025-1` (`PR #907`, `ADR-553`, PARO-PREMISA, 0 de 38). Firma de mesa, verbatim: **«2 si extendemos»**.

**Contadores movidos:** `N_corridas_selladas` +1 (`CALC-C2-COMPUESTO-IC-ENVIPE2025-0001`). `cuenta_gen2` nace NO por E.1 (`FP-397`). `adoptados_activos`: 0 (no adopta). `NC-0361` CERRADA; `FP-390` FIRMADA.

## 1 · Qué se hizo, en orden

1. **P1 · guardián extendido** (`tools/celda_d/marginales_reproduccion.py`, `80364e2a` → `d8adce0`): `EJES += ("sexo", "edad")`, derivados en `carga_ola` con `SEXO` y `tramos_edad` de `tools/ejes_maestra35_l1.py` (importados; `mr.SEXO is l1.SEXO`), desde **`tmod_vic`** (ver §4). `PARES_VETADOS[2025] = {edad, dominio_urbano_rural}` (`NC-0328`): `cruce()` lanza `ReservaRota` para ese par antes de mirar `reservada`, sin bandera. Ninguna firma, valor por defecto ni salida previa cambia; `meta` gana `sexo_fuera`/`edad_fuera`.
2. **Tres controles de no-regresión, los tres antes de medir:** (i) 15/15 casos heredados verdes sin editar un caso; (ii) 7 casos nuevos (sexo/edad con el orden del árbitro; lista o dos posicionales → `TypeError`; veto por nombre en ola libre de 2025 con `NC-0328` en el mensaje, y 12 celdas en otra ola; los cuatro pares del dictamen prohibidos en reservada; réplicas para los ejes nuevos); (iii) `corrida0 verify` de `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` y `…-ARBITRO-CRUCE-0001` con el módulo extendido, en proceso aislado: **REPRODUCE las dos**.
3. **P2 · COMMIT-1** (`d8adce0`): spec humana `forense/prereg-caja/C2-COMPUESTO-IC-ENVIPE2025-spec-v1_0.md` + sidecar (`5f500c53…`), `spec.yaml` (357 RESULT generados desde el TSV derivado de emisiones, no tecleados), `medidor.py`, `tests/test_c2_ic_envipe2025_guardia.py` (11 guardias AST/sha, cero microdato). `spec-check` 11 OK. CALC-id libre en 7/7 ramas remotas (0 directorios). Sin microdato en el commit.
4. **P3 · COMMIT-2** (`fcbfe11`): `preflight` VERDE → `run` (11 s) → `verify` aislado REPRODUCE, `CONTEXTO=IDENTICO`. Registro E.7: `registro --verifica --lote CALC-C2-COMPUESTO-IC-ENVIPE2025-0001 --escribe`; asiento en `forense/replay-evidencia.tsv`. Tras fusionar `origin/main` (`#908`/`#911`/`#912`), re-derivado: **0 filas ajenas modificadas o borradas** (medido contra `origin/main` fresco excluyendo las propias); las 5 corridas + 16 RESULT ajenos que el árbol traía sin derivar ya los publicó `#911` (`NC-0382`).
5. **P4 · trámite:** `ADR-560`, L0, rótulo, `FP-390` FIRMADA, `FP-397`, `NC-0361` CERRADA, `NC-0386`–`NC-0390`, `decisiones.tsv` objeto `guardian:envipe2025-ejes`, esta nota.

## 2 · Universo, unidad, escala, clase

* Payload: `envipe2025_csv.zip` (sha256 `8a7a99fd90ce9d03…`), miembros `tmod_vic` (`utf-8`) y `tsdem`. Ola cargada `reservada=True`.
* **Unidad: el DELITO** declarado por la víctima, no la persona. Universo `BP1_20 ∈ {1,2}`: **n = 40,280** (= filas del archivo; 0 fuera; 0 delitos sin persona). Numerador 21,761. `FAC_DEL`; `EST_DIS`/`UPM_DIS`: 739 estratos, 10,694 UPM, 23 estratos con UPM única.
* Desenlace `evade_norma = (BP1_20 == 2) ∧ (BP1_23 ∈ {04,05,06,08})`, la conjunta. **Escala: proporción en [0,1]. Clase (a): datos primarios en México.**
* Fuera de banda, contado y reportado: escolaridad 100, **edad 94** (= 40 280 × (1 − 0.997666), la cobertura que el árbitro selló: 97+ y no especificado), sexo 0, dominio 0.

## 3 · Resultado: 38 de 38 con IC — derivado

`G-IC-PUBLICADO = SI` · celdas con IC **38** / sin IC 0 · NO-CONSTRUIBLES 0 · réplicas SIN-DEFINIR (suma sobre las 38) 0 · `cruce()` llamado: **NO**.

Un remuestreo (`PCG64(42)`, 10,000) compartido por cinco `marginal()` de una variable; `C2_k = expit(logit p_k(a) + logit p_k(b) − logit p_k)`; IC95 = percentiles 2.5/97.5.

### Controles de coherencia (los dos, o no se publica)

**A · punto = sellado** en `CALC-C2-COMPUESTO-RESERVADAS-0001`: REPRODUCE, |Δ| máx 0.0 en 38/38.
**B · réplica base = R del árbitro** (`cotejo()`, tol_p 1e-6, tol_ic 1e-4): REPRODUCE; |Δp| máx 4.95e-07, |ΔIC| máx 4.70e-07, **Δn = 0 en 13/13 celdas de eje**.

| eje | veredicto | \|Δp\| máx | \|ΔIC\| máx |
|---|---|---|---|
| escolaridad_proxy | REPRODUCE | 4.03e-07 | 4.70e-07 |
| dominio_urbano_rural | REPRODUCE | 3.98e-07 | 3.38e-07 |
| nacional | REPRODUCE | 4.79e-07 | 4.40e-07 |
| sexo | REPRODUCE | 1.04e-07 | 1.60e-07 |
| edad | REPRODUCE | 4.95e-07 | 4.66e-07 |

### Las 38 celdas

| celda (par · a × b) | C2 punto | IC95 inf | IC95 sup | anchura | réplicas válidas |
|---|---|---|---|---|---|
| `DOMINIO-URBANO-RURALXSEXO-COMPLEMENTO-URBANO-X-1-HOMBRE` | 0.5574 | 0.5352 | 0.5792 | 0.0440 | 10000 |
| `DOMINIO-URBANO-RURALXSEXO-COMPLEMENTO-URBANO-X-2-MUJER` | 0.4897 | 0.4681 | 0.5109 | 0.0428 | 10000 |
| `DOMINIO-URBANO-RURALXSEXO-RURAL-X-1-HOMBRE` | 0.4379 | 0.4090 | 0.4669 | 0.0580 | 10000 |
| `DOMINIO-URBANO-RURALXSEXO-RURAL-X-2-MUJER` | 0.3725 | 0.3459 | 0.4008 | 0.0549 | 10000 |
| `DOMINIO-URBANO-RURALXSEXO-URBANO-X-1-HOMBRE` | 0.6265 | 0.6104 | 0.6417 | 0.0312 | 10000 |
| `DOMINIO-URBANO-RURALXSEXO-URBANO-X-2-MUJER` | 0.5611 | 0.5429 | 0.5783 | 0.0355 | 10000 |
| `EDADXESCOLARIDAD-PROXY-18-29-X-HASTA-PRIMARIA` | 0.4503 | 0.4160 | 0.4852 | 0.0692 | 10000 |
| `EDADXESCOLARIDAD-PROXY-18-29-X-MEDIA-SUPERIOR` | 0.5004 | 0.4693 | 0.5303 | 0.0610 | 10000 |
| `EDADXESCOLARIDAD-PROXY-18-29-X-SECUNDARIA` | 0.5247 | 0.4980 | 0.5505 | 0.0524 | 10000 |
| `EDADXESCOLARIDAD-PROXY-18-29-X-SUPERIOR` | 0.5479 | 0.5240 | 0.5714 | 0.0474 | 10000 |
| `EDADXESCOLARIDAD-PROXY-30-44-X-HASTA-PRIMARIA` | 0.5116 | 0.4748 | 0.5481 | 0.0733 | 10000 |
| `EDADXESCOLARIDAD-PROXY-30-44-X-MEDIA-SUPERIOR` | 0.5616 | 0.5384 | 0.5845 | 0.0461 | 10000 |
| `EDADXESCOLARIDAD-PROXY-30-44-X-SECUNDARIA` | 0.5853 | 0.5604 | 0.6094 | 0.0489 | 10000 |
| `EDADXESCOLARIDAD-PROXY-30-44-X-SUPERIOR` | 0.6078 | 0.5879 | 0.6273 | 0.0394 | 10000 |
| `EDADXESCOLARIDAD-PROXY-45-59-X-HASTA-PRIMARIA` | 0.5327 | 0.4926 | 0.5723 | 0.0797 | 10000 |
| `EDADXESCOLARIDAD-PROXY-45-59-X-MEDIA-SUPERIOR` | 0.5822 | 0.5522 | 0.6113 | 0.0591 | 10000 |
| `EDADXESCOLARIDAD-PROXY-45-59-X-SECUNDARIA` | 0.6057 | 0.5759 | 0.6341 | 0.0582 | 10000 |
| `EDADXESCOLARIDAD-PROXY-45-59-X-SUPERIOR` | 0.6277 | 0.6006 | 0.6534 | 0.0529 | 10000 |
| `EDADXESCOLARIDAD-PROXY-60-X-HASTA-PRIMARIA` | 0.4965 | 0.4487 | 0.5437 | 0.0950 | 10000 |
| `EDADXESCOLARIDAD-PROXY-60-X-MEDIA-SUPERIOR` | 0.5466 | 0.5160 | 0.5776 | 0.0616 | 10000 |
| `EDADXESCOLARIDAD-PROXY-60-X-SECUNDARIA` | 0.5706 | 0.5361 | 0.6032 | 0.0671 | 10000 |
| `EDADXESCOLARIDAD-PROXY-60-X-SUPERIOR` | 0.5933 | 0.5643 | 0.6223 | 0.0579 | 10000 |
| `EDADXSEXO-18-29-X-1-HOMBRE` | 0.5554 | 0.5335 | 0.5770 | 0.0435 | 10000 |
| `EDADXSEXO-18-29-X-2-MUJER` | 0.4876 | 0.4627 | 0.5121 | 0.0494 | 10000 |
| `EDADXSEXO-30-44-X-1-HOMBRE` | 0.6150 | 0.5962 | 0.6332 | 0.0370 | 10000 |
| `EDADXSEXO-30-44-X-2-MUJER` | 0.5489 | 0.5302 | 0.5674 | 0.0372 | 10000 |
| `EDADXSEXO-45-59-X-1-HOMBRE` | 0.6348 | 0.6079 | 0.6603 | 0.0523 | 10000 |
| `EDADXSEXO-45-59-X-2-MUJER` | 0.5698 | 0.5442 | 0.5942 | 0.0501 | 10000 |
| `EDADXSEXO-60-X-1-HOMBRE` | 0.6006 | 0.5719 | 0.6283 | 0.0564 | 10000 |
| `EDADXSEXO-60-X-2-MUJER` | 0.5339 | 0.5044 | 0.5636 | 0.0592 | 10000 |
| `ESCOLARIDAD-PROXYXSEXO-HASTA-PRIMARIA-X-1-HOMBRE` | 0.5287 | 0.4936 | 0.5624 | 0.0688 | 10000 |
| `ESCOLARIDAD-PROXYXSEXO-HASTA-PRIMARIA-X-2-MUJER` | 0.4609 | 0.4261 | 0.4968 | 0.0707 | 10000 |
| `ESCOLARIDAD-PROXYXSEXO-MEDIA-SUPERIOR-X-1-HOMBRE` | 0.5784 | 0.5552 | 0.6012 | 0.0459 | 10000 |
| `ESCOLARIDAD-PROXYXSEXO-MEDIA-SUPERIOR-X-2-MUJER` | 0.5111 | 0.4860 | 0.5352 | 0.0492 | 10000 |
| `ESCOLARIDAD-PROXYXSEXO-SECUNDARIA-X-1-HOMBRE` | 0.6019 | 0.5793 | 0.6235 | 0.0442 | 10000 |
| `ESCOLARIDAD-PROXYXSEXO-SECUNDARIA-X-2-MUJER` | 0.5353 | 0.5111 | 0.5587 | 0.0476 | 10000 |
| `ESCOLARIDAD-PROXYXSEXO-SUPERIOR-X-1-HOMBRE` | 0.6240 | 0.6039 | 0.6427 | 0.0388 | 10000 |
| `ESCOLARIDAD-PROXYXSEXO-SUPERIOR-X-2-MUJER` | 0.5584 | 0.5398 | 0.5768 | 0.0370 | 10000 |

Anchura: mín 0.0312, mediana 0.0512, máx 0.0950. `P-REDERIVADO` (C2 sobre los marginales re-derivados aquí) difiere del punto sellado en ≤ 1.39e-6: el redondeo a 6 decimales de los R públicos.

## 4 · Desviación declarada (A.8 contra el árbol) — `NC-0386`

El encargo decía «`COLUMNAS_TSDEM` gana las dos columnas crudas». El árbitro las leyó de `tmod_vic` (`tools/medidor_evasion_norma_envipe25.py:188`; `milpa/tramite-ola5-propuesta-v0.yaml:1680`). Se cargaron de `COLUMNAS_TMOD`, se declaró en la spec §3 antes del COMMIT-1, y el control B es la prueba de que era la tabla correcta: Δn = 0 en `1 Hombre` 19 399 / `2 Mujer` 20 881 / `18-29` 11 871 / `30-44` 15 214 / `45-59` 8 620 / `60+` 4 481.

## 5 · Módulo de auditoría (afirma sobre México)

* **La celda no es una persona.** «Mujeres 60+» son delitos sufridos por mujeres de 60 a 96; la composición del delito por sexo y edad (robo en transporte, extorsión, fraude) carga buena parte de cualquier diferencia en evasión. Ninguna de estas 38 cifras se lee como rasgo de un grupo.
* **La banda alta cierra en 96.** 94 delitos (97+ y no especificado) salen del universo del eje edad; la misma pregunta abierta que en ENCIG (¿edad real censurada o no respuesta?) se cuenta y no se resuelve aquí.
* **El IC mide ruido muestral de un estimador que supone no-interacción en escala logit; no mide el error de ese supuesto.** Rótulo prohibido: «independencia». Sin región ni condición indígena. Ninguna cifra esperada se tecleó: el punto es el sellado y el IC salió de la primera corrida.
* **Peligroso leído simplista:** «ya tiene intervalo» como «ya está validado». Las 38 siguen `EMITIDA-SIN-EVALUAR`, fuera de la estimación adoptada del motor; ningún R de cruce de 2025 se ha visto.
* **¿Qué afirmación sobre el estado del corpus fue escrita a mano?** Ninguna: conteos de celdas, pares, n, fuera de banda y anchuras salen de `resultados.json` de la corrida sellada.
