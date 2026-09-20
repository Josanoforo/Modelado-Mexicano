ENCARGO · ACTO GEN2-PISOS-ENIF2021-FORMALIDAD-1 · LAS SEIS CELDAS QUE ESTABAN "NO CONSTRUIBLES" POR BUSCAR P3_13 DONDE SE LLAMA P3_10: PISO t−1 DE FORMALIDAD EN ENIF 2021
⚠ ENTORNO: CAJA (máquina local, corpus montado) — NO NUBE

Primera acción: python3 tools/entorno.py --sonda-red y ls data/raw | head -1. Sin corpus, PARA en una línea. Worktree nuevo: enlaza data/raw y data/raices.local.yaml; no es PARO.

CABECERA (D-12) · SHA de redacción 1bb9e2c4; re-deriva al abrir · una sola sesión, rama propia · COMPUERTA: #908 (GEN2-PISOS-ENUT2019-EJES-1) fusionado — este encargo cita su dictamen; si no está en main, PARA · MODELO: Opus (mide) · CALC-id RESERVADO: CALC-PISOS-ENIF2021-FORMALIDAD-0001; verifícalo libre en cada rama viva · payload único: ENIF 2021 (en vuelo: IC-ENIF2024 y el guardián de ENVIPE; disjuntos) · FP/ADR/NC: deriva al cierre · CONTADOR: sella una corrida; cuenta_gen2 = SI propuesto, nace PENDIENTE-DE-MESA; no adopta.

FIRMA DE MESA (20/sep/2026, verbatim)

«3. Si medimos las 6 celdas.»

DE DÓNDE SALE

El dictamen de #908 (§2.1) leyó los dos FD por texto: la pregunta 3.13 de ENIF 2024 («Por parte de su trabajo, ¿usted tiene derecho a los servicios médicos…») es la 3.10 de ENIF 2021, con el mismo residual — 2021 código 6 «No tiene servicio médico (incluye Seguro Popular, INSABI)»; 2024 código 7 «carece de derecho… (incluye IMSS-Bienestar…)» — y el ISSSTE federal/estatal fundido en un código en 2021 y partido en dos en 2024. La rejilla (#871) escribió «P3_13 comparable no existe en ENIF 2021» tras buscar por nemónico. Tercera vez que el programa paga esa trampa (P5_6/P5_7, hs02g, y ésta): A.15 la nombra y aquí volvió a atrapar.

VERIFICACIÓN DE EXISTENCIA (contra 1bb9e2c4)

PISOS-REJILLA-arbitro-metadatos-v1_0.tsv: 4 filas NO-CONSTRUIBLE de formalidad (dos desenlaces de via_informal × 2 categorías). Marcador: 2 más de horizonte_corto × formalidad, SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD. ls data/corrida0 | grep -i FORMALIDAD → 0. Medidor de referencia: tools/pisos_ejes.py y CALC-PISOS-ENIF2021-EJES-0003. Definición del eje en el árbitro: tools/medidor_ahorro_enif24.py:145 (código "7" → sin seguridad social; resto → con) y yaml :2164 (universo P3_13 ∈ {1..7}). NO-ENCONTRADO: ningún piso de formalidad existe.

PIEZAS — dos commits mínimo

P0 · Dos lecturas por texto antes de congelar, con cita de FD y cuestionario de ambas olas. (a) El eje: confirma la tabla del dictamen tú mismo — no la heredes — y fija el mapa 2021: {1..5} → con seguridad social, {6} → sin; 9 y blanco por secuencia fuera del universo, contados. Declara la única diferencia de contenido (ISSSTE fundido/partido) y por qué no mueve la dicotomía. El universo es quien trabaja (llega a la pregunta por secuencia): di el filtro de flujo de cada ola y verifica que sea el mismo. (b) El desenlace horizonte_corto: la rejilla midió via_informal en 2021, no horizonte_corto. ¿Existe en ENIF 2021 el reactivo que lo define, con el mismo texto y opciones? Si no: esas 2 celdas salen NO-CONSTRUIBLE con la diferencia escrita, y el acto mide las otras 4. No lo busques por nombre de variable. P1 · COMMIT-1 — spec + medidor + rejilla congelados juntos. Rejilla leída del yaml del árbitro; desenlaces con la misma definición que CALC-PISOS-ENIF2021-EJES-0003 (importa, no copies); cuenta y ponderador como allá. Medidor dentro del CALC o blob fijado en spec.yaml. Bootstrap de diseño. Ejecución diagnóstica: declarada aquí o no existe. «El primer resultado que produzca este procedimiento es el que se reporta.» P2 · COMMIT-2 — CALC-PISOS-ENIF2021-FORMALIDAD-0001. Un RESULT por celda (punto, IC, n, denominador ponderado) + conteo de excluidos. Control de coherencia: sobre el universo de quien trabaja, la suma de las dos celdas reproduce el total del desenlace en ese mismo universo; no se compara contra el nacional de -0003, que es otro universo (A-bis 4). Tabla de identidad propia (PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv), mismo esquema que la de rejilla. Vista y replay en el mismo acto (E.7). P3 · Enlace y trámite. Registra la tabla nueva donde el marcador lee tablas de identidad — una línea en tools/marcador_segmento.py si así lo hizo #908; si exige más, PARA esa pieza. Re-deriva el marcador y reporta sin_piso derivado. La causa errónea de las 4 filas de la rejilla no se edita (tabla sellada): se sucede por la tabla nueva y se asienta en hallazgos. Semilla PARA-v2.15: todo NO-CONSTRUIBLE por ausencia de variable cita el texto de la pregunta buscada y las secciones del FD recorridas; «no existe X» sin eso no es un negativo (A.13 + A.15).

PERÍMETRO

forense/prereg-caja/PISOS-ENIF2021-formalidad-* · data/corrida0/CALC-PISOS-ENIF2021-FORMALIDAD-0001/ · tests/test_pisos_enif2021_formalidad.py (rejilla emitida == rejilla del árbitro) · tools/marcador_segmento.py (una línea de registro) · marcador-segmento.tsv re-derivado · filas propias en corridas.tsv y replay-evidencia.tsv · derivados por comando · cascada. No toca la tabla de identidad de rejilla · CALC-PISOS-ENIF2021-EJES-* · tools/pisos_ejes.py · nada de ENIF 2024 · el yaml del árbitro. «Si te encuentras escribiendo fuera de esta lista, PARA.»

LO QUE NO HACE

No mide el error de persistencia de estas celdas (sucesor: CALC nuevo) · no adopta · no reabre el dictamen A-BIS-4 que dejó formalidad NO-EMITIBLE en el C2 compuesto — aquello es por universo restringido, y sigue siendo cierto.

MÓDULO DE AUDITORÍA (afirma sobre México: aplica completo)

"Formalidad" aquí es tener derecho a servicio médico por el trabajo — un proxy de seguridad social, no de contrato, ni de registro fiscal, ni de ingreso. El universo excluye a quien no trabaja: amas de casa, estudiantes, retirados y desocupados no están, y ahí vive buena parte del ahorro informal. Que quien carece de seguridad social ahorre más por vía informal es primero acceso — nómina bancarizada, sucursal, requisitos de cuenta — y solo después preferencia; tandas y guardaditos son también instituciones con reglas, no ausencia de ellas: ni se romantizan ni se leen como déficit. 2021 es dato de pandemia: pérdida de empleo formal e INSABI en transición mueven quién cae en cada categoría, no solo cómo ahorra. Clase (a). Sin región ni condición indígena. Ninguna cifra esperada. Peligroso leído simplista: "los informales ahorran en tandas" como rasgo cultural.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «P3 · Enlace y trámite. Registra la tabla nueva donde el marcador lee tablas de identidad — una línea en tools/marcador_segmento.py si así lo hizo #908; si exige más, PARA esa pieza.» | FUERA-DE-PERÍMETRO — la línea hace fallar `T-ENLACE-BIYECTIVO` (6 casos): `indice_identidad()` deja ganar a las 4 filas selladas NO-CONSTRUIBLE de la rejilla con la misma llave, `MAPA_CONSUMER` no conoce `horizonte_corto`, `CALC_PISOS_SELLADOS` no lista el CALC; suceder una tabla sellada es regla nueva. Revertido. | `sin_piso` 21→21, `cobertura_de_piso` 73→73; el marcador sigue transportando la causa refutada en 4 filas y SIN-CONSUMER en 2. | acto sucesor de marcador (propuesto GEN2-MARCADOR-PISOS-SUCESION-1), `NC-0384` |
| «No mide el error de persistencia de estas celdas (sucesor: CALC nuevo)» · `cuenta_gen2 = SI propuesto, nace PENDIENTE-DE-MESA` | DIFERIDO-A:CALC nuevo de error de persistencia (SIN-ASIGNAR); DECISIÓN-DE-MESA-PENDIENTE para `cuenta_gen2` | `error_piso_pp`/`clase_persistencia` vacíos para las 6 celdas; `N_resultados_gen2_sellados` no cuenta la corrida hasta firma. | `FP-396`, `NC-0385` |

## CONSUMIDO

Ejecutado por **PR #915** (`acto/gen2-pisos-enif2021-formalidad-1`), 19–20/sep/2026, CAJA, Opus 5. COMMIT-1 `977c5dd` (spec + medidor congelados antes de abrir microdato), COMMIT-2 `4a0ec38` (`CALC-PISOS-ENIF2021-FORMALIDAD-0001` sellado, tabla de identidad, test, replay aislado), cascada `468a409` (`ADR-559`, L0, `FP-396`, `NC-0384`–`NC-0385`). P3 (enlace al marcador) PARA por perímetro; ver `## NO-CORRIDO / RESERVAS`. Mesa fusiona.
