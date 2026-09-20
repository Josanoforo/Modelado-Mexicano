ENCARGO · ACTO GEN2-GUARDIAN-ENVIPE-EJES-IC-1 · EL GUARDIÁN DE ENVIPE 2025 APRENDE sexo Y edad — CON EL CRUCE QUEMADO VETADO POR NOMBRE DENTRO DE cruce() — Y LAS 38 EMISIONES COMPUESTAS GANAN SU IC
⚠ ENTORNO: CAJA (máquina local, corpus montado) — NO NUBE

Primera acción: python3 tools/entorno.py --sonda-red y ls data/raw | head -1. Si no hay corpus, PARA en una línea. Si abres en un worktree nuevo: nace sin data/raw ni data/raices.local.yaml — se enlazan, no es PARO (lo documentó #907).

CABECERA (D-12) · SHA de redacción 1bb9e2c4; re-deriva al abrir · una sola sesión, rama propia; /acto PARA si ya está archivado en otra rama viva · COMPUERTA: #907 en main (cumplida) · MODELO: Opus (cambia el contrato del único código autorizado a tocar una ola reservada, y mide) · CALC-id RESERVADO: CALC-C2-COMPUESTO-IC-ENVIPE2025-0001 — #907 lo dejó libre a propósito; verifica que siga libre en cada rama viva antes de congelar · FP/ADR/NC: deriva al cierre; renumera quien fusione segundo · CONTADOR: sella una corrida; cuenta_gen2 = SI propuesto, nace PENDIENTE-DE-MESA; no adopta; adoptados_activos no debe moverse. Sucede a GEN2-C2-COMPUESTO-IC-ENVIPE2025-1 (#907, PARO-PREMISA en P0, 0 de 38). Aquel encargo de dirección suponía que el guardián cubría los ejes; dirección no lo había leído. Este se escribió después de leerlo (432 líneas, blob 80364e2a).

FIRMA DE MESA (20/sep/2026, verbatim, a la propuesta de dirección "extender el guardián por firma — añadir sexo y edad a sus ejes admitidos, con edad × dominio vetado por nombre — y después relanzar el IC")

«2 si extendemos»

VERIFICACIÓN DE EXISTENCIA (A.8; dirección contra 1bb9e2c4)
tools/celda_d/marginales_reproduccion.py:99 → EJES = ("escolaridad_proxy", "dominio_urbano_rural", "nacional"); :103 → COLUMNAS_TSDEM = ("ID_PER", "NIV"): SEXO y EDAD no se cargan. marginal() (:331-343): un str posicional, whitelist EJES, re-huella. cruce() (:355-366) admite cualquier par de EJES salvo nacional, y solo se niega si ola.reservada.
La construcción de los ejes que el árbitro selló vive en tools/ejes_maestra35_l1.py: SEXO (:51), tramos_edad (:54-60: 18–29, 30–44, 45–59, 60+ = 60 a 96), ORD_EDAD, ORD_SEXO. El guardián ya importa de ahí ESC_2DIG. tsdem_envipe2025 es la tabla demográfica (tools/censo_ejes_maestra35_l1.py:45).
Dependientes en tiempo de ejecución: CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001/medidor.py:55 y CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001/medidor.py:39 importan el módulo por ruta; tests/test_marginales_una_variable.py lo prueba. Ninguno fija su blob.
Pares a cubrir (dictamen, re-derívalos): dominio_urbano_rural × sexo (6), edad × escolaridad_proxy (16), edad × sexo (8), escolaridad_proxy × sexo (8). edad × dominio no está en el dictamen: NC-0328 lo quemó.
ls data/corrida0 | grep "C2-COMPUESTO-IC-ENVIPE" → 0. NO-ENCONTRADO.
PIEZAS — dos commits mínimo; el primero congela guardián + spec + medidor juntos

P1 · Extensión del guardián, puramente aditiva (COMMIT-1).

EJES gana "sexo" y "edad"; COLUMNAS_TSDEM gana las dos columnas crudas; los ejes se derivan dentro de carga_ola con las funciones importadas de ejes_maestra35_l1.py, no copiadas. Quien caiga fuera de banda (edad < 18, 97+, no especificado) va a FUERA, contado y reportado — misma semántica que hoy.
Veto por nombre dentro de cruce(): una constante PARES_VETADOS con {edad, dominio_urbano_rural} para 2025, citando NC-0328; cruce() lanza ReservaRota para ese par con la ola reservada o no, sin bandera que lo salte. Los cuatro pares del dictamen tampoco se abren aquí: en este acto la ola se carga reservada=True y cruce() no se llama.
No cambia ninguna firma, ningún valor por defecto, ni el orden o nombre de lo que ya devuelve. El docstring gana un párrafo fechado con esta firma; el párrafo de la Firma 2 del piloto 2 no se toca.
Tres controles de no-regresión, los tres o PARA antes de medir: (i) tests/test_marginales_una_variable.py verde sin editar sus casos; (ii) casos nuevos: marginal(ola, "sexo") y "edad" funcionan; lista o dos argumentos → TypeError; cruce(·, "edad", "dominio_urbano_rural") → ReservaRota en ola no reservada; (iii) corrida0.py verify de las dos corridas selladas del piloto 2 sigue REPRODUCE con el módulo extendido, en proceso aislado — si alguna pasa a NO-REPRODUCE, la extensión no era aditiva: PARA y reporta el diff. P2 · Spec y medidor del IC (mismo COMMIT-1). Según el encargo original (archivado por #907): medidor dentro del CALC, importa el guardián sin modificarlo más; bootstrap de diseño con réplicas y semilla leídas del piloto 2 y citadas; por réplica p_k(a), p_k(b), p_k vía marginal() — una variable por llamada, una sola replicas_compartidas por ola — y C2_k = expit(logit p_k(a) + logit p_k(b) − logit p_k); IC95 por percentiles; tratamiento de p_k ∈ {0,1} declarado aquí. Test AST: ninguna agrupación por más de una variable, ningún crosstab/pivot, ninguna lectura de payload que no sea ENVIPE 2025. «El primer resultado que produzca este procedimiento es el que se reporta.» P3 · COMMIT-2 — CALC-C2-COMPUESTO-IC-ENVIPE2025-0001. Por celda: punto, IC-LO, IC-HI, réplicas válidas. Dos controles de coherencia, los dos o no se publica IC: el punto reproduce el sellado en CALC-C2-COMPUESTO-RESERVADAS-0001; y los marginales de sexo y edad de la réplica base reproducen los R sellados del árbitro (tramite-ola5-propuesta-v0.yaml, entrada …evasion_norma_ejes_envipe2025) con cotejo() y las tolerancias del piloto 2 — ésa es la prueba de que la extensión mide lo que el árbitro midió. Registro en la vista y asiento de replay en el mismo acto (E.7). P4 · Trámite. NC-0361 (la que #907 abrió; verifica id y estado, A.17) cierra con este acto. decisiones.tsv: objeto guardian:envipe2025-ejes, con la firma. Nota: universo, unidad DELITO, escala, clase (a); cuántas de las 38 quedaron con IC — derivado.
PERÍMETRO

tools/celda_d/marginales_reproduccion.py (solo P1) · tests/test_marginales_una_variable.py (solo casos nuevos) · forense/prereg-caja/C2-COMPUESTO-IC-ENVIPE2025-spec-v1_0.md + sidecar · data/corrida0/CALC-C2-COMPUESTO-IC-ENVIPE2025-0001/ · tests/test_c2_ic_envipe2025_guardia.py · filas propias en corridas.tsv y replay-evidencia.tsv · derivados por comando · cascada. No toca ejes_maestra35_l1.py · los dos CALC del piloto 2 · marcador_segmento.py · estimadores-por-segmento.yaml · ningún payload que no sea ENVIPE 2025 · nada de ENIF (hay un acto gemelo en vuelo). «Si te encuentras escribiendo fuera de esta lista, PARA.»

LO QUE NO HACE

No llama cruce() · no ve, deriva ni imprime ningún cruce de 2025 · no adopta · no actualiza el marcador · no extiende el guardián a otras olas ni a otros ejes.

MÓDULO DE AUDITORÍA (afirma sobre México)

La unidad es el delito declarado por la víctima, no la persona: "mujeres 60+" aquí son delitos sufridos por mujeres de 60 a 96, y la composición del delito por sexo y edad (robo en transporte, extorsión, fraude) carga buena parte de cualquier diferencia en evasión. La banda alta cierra en 96: 97+ y no especificado salen del universo — la misma pregunta abierta que en ENCIG (¿edad real censurada o no respuesta?); se cuenta y se reporta, no se resuelve aquí. El IC mide ruido muestral de un estimador que supone no-interacción; no mide el error de ese supuesto. Sin región ni condición indígena. Ninguna cifra esperada. Peligroso leído simplista: "ya tiene intervalo" como "ya está validado".


## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| **P1 · «`COLUMNAS_TSDEM` gana las dos columnas crudas»** | `PARO-PREMISA`: el árbitro leyó `SEXO`/`EDAD` de **`tmod_vic`** (`tools/medidor_evasion_norma_envipe25.py:188`; `milpa/tramite-ola5-propuesta-v0.yaml:1680` «sexo y edad viven en tmod_vic y no necesitan el join»). Se cargaron en `COLUMNAS_TMOD`, declarado en la spec §3 antes del COMMIT-1; el control B lo confirma (Δn = 0 en 6/6 celdas de sexo y edad) | Ninguno sobre el resultado | `NC-0384` (CERRADA), `ADR-559` |
| **P1 · «tests/test_marginales_una_variable.py (solo casos nuevos)» / control (i) «sin editar sus casos»** | `PARO-PREMISA`: ningún caso heredado se editó (15/15 verdes), pero el fixture `fabrica_zip` ganó `SEXO`/`EDAD` en tmod_vic — sin ellas `carga_ola` PARA por columnas ausentes. Hacerlas opcionales sería un lector que devuelve vacío en vez de error | Ninguno sobre la no-regresión (15/15 + `verify` REPRODUCE ×2 de las corridas reales) | `NC-0387` (CERRADA), `ADR-559` |
| **CONTADOR · «`cuenta_gen2 = SI` propuesto, nace PENDIENTE-DE-MESA»** | `DECISIÓN-DE-MESA-PENDIENTE`: la spec lo propone; el registro aplica E.1 y lo baja a `NO` por el input legacy `milpa/tramite-ola5-propuesta-v0.yaml` (`envuelto_legacy = SI`), el mismo caso que `NC-0350` y `NC-0380` | Las 38 celdas con IC no cuentan en `N_resultados_gen2_sellados`; no se quitó el input para forzar el contador | `NC-0385`, `FP-396` (1) |
| **LO QUE NO HACE · «no actualiza el marcador»** | `DIFERIDO-A:` sucesor de nube (una línea) | Las 38 emisiones siguen con `tipo_incertidumbre = NO-PROPAGADA-COVARIANZA-NO-SELLADA` en el TSV aunque el IC existe sellado; ninguna decisión del motor depende de ello | `NC-0386`, `FP-396` (2) |
| **P2 · cableado de `tests/test_c2_ic_envipe2025_guardia.py` en CI** | `FUERA-DE-PERÍMETRO`: `tests/check.py` no auto-descubre `tests/test_*.py`; `.github/workflows/verify.yml` no está en la lista del encargo | La guardia que sí corre en cada `run`/`verify` es la del guardián; la AST del medidor y G5–G8 sólo corren a mano (11/11) | `NC-0388` (SIN-ASIGNAR: el acto que toque `verify.yml`, junto con `NC-0381`) |
| **Ejecución diagnóstica** | Ninguna: el medidor se congeló sin microdato (`medidor_ejecutado_al_congelar: NO`) y corrió una vez. El primer resultado es el que se reporta | — | — |

## CONSUMIDO

Ejecutado por **PR #916** (`acto/gen2-guardian-envipe-ejes-ic-1`, 20/sep/2026, CAJA, Opus 5), `ADR-559`. COMMIT-1 `d8adce0` (guardián extendido + spec + medidor + tests, sin microdato) · COMMIT-2 `fcbfe11` (`CALC-C2-COMPUESTO-IC-ENVIPE2025-0001`, 38/38 con IC, registro y replay) · cascada `8eb4fd5`. `NC-0361` CERRADA; `NC-0384`–`NC-0388` citan el PR. El merge es de mesa.
