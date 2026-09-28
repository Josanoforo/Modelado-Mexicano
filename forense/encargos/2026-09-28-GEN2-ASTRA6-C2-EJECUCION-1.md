# ENCARGO · ACTO GEN2-ASTRA6-C2-EJECUCION-1 · Continuación del carril C2 de Codex (familias 2027) con Claude: cinco de las ocho familias del expediente están BLOQUEADAS solo por tres firmas de forma que mesa ya dio (B4, E3, E4: control ENIF, identidad ENCIG, unidad de remuestreo ENVIPE). Este acto ejecuta esas tres firmas, lleva cada familia desbloqueada a COMMIT-1 (spec humana + spec.yaml congelados sin microdato de 2027) y a COMMIT-2 (emisiones selladas desde las olas vistas, PROSPECTIVAS por construcción) con potencia, y deja el expediente en v1.1 con el gate que le queda a cada una: la ola 2027

> ENTORNO: **CAJA** — las emisiones se calculan desde olas vistas (ENIF 2021/2024 abiertas, ENCIG 2023, ENVIPE 2024/2025 según lo que sus árbitros abrieron) bajo spec congelada; ninguna ola 2027 existe aún y ninguna reservada se abre. Hook imprime ENTORNO-DERIVADO; si dice cloud_default o milpa-inegi, PARA. Sesión pesada (ENVIPE); tercera de caja: **cabe si CORPUS-CACHE-PARQUET-1 ya cerró o si mesa levanta el tope; si no, espera.**

CABECERA · SHA de redacción `16ba3d02` (re-deriva al abrir) · una sesión, rama propia; un PR por familia (tres commits: spec → emisiones → nada de R, E.6) · MODELO: **Opus** (frente prospectivo; no baja) · MODO: **RÍGIDO** por familia desde su COMMIT-1 · ids con raíz de acto · D-21 aplica.
CONTADOR: **cero cifras para el canon** (las emisiones son predicciones selladas, no RESULT adoptables); `celdas_validadas` no se mueve (no hay R). No adopta.

## 1 · OBJETIVO
(P1) **Ejecutar las tres firmas** (letras de la hoja de NC-DECISIONES-1, firmadas «firmado» 28/sep, ADENDA-1 de HOJA-FIRMAS-21-1): B4 (tres firmas de forma para el COMMIT-3 de Astra C2: control ENIF, identidad ENCIG, precisión), E3 (opción 1: envoltura de control ENIF y reconocimiento ENCIG), E4 (opción 1: unidad de remuestreo de ENVIPE fijada en spec y código antes de habilitar R, con la medida de oferta al lado): cada una como cambio de spec humana/yaml en `forense/analisis/familias-2027/astra6-{enif,encig,envipe}/` y marcado FIRMADA de sus FP `f2e5-*` (A.12).
(P2) **COMMIT-1 por familia desbloqueada** (ENIF-AHORRO-FORMAL, ENIF-HORIZONTE-AHORRO, ENCIG-SOLICITUD-MORDIDA, ENVIPE-DENUNCIA-U4, ENVIPE-EVASION-NORMA): spec humana que baste para recalcular (D-15), spec.yaml, códigos por texto de pregunta, unidad, universo, candidatos declarados juntos con una sola comparación primaria (E.6), regla y umbral de adjudicación fijados antes, guardia de la ola reservada en el medidor (una sola variable de agrupación, prueba por mutación).
(P3) **COMMIT-2: emisiones selladas** desde las olas vistas (piso: ola anterior por eje; retador solo si ya estaba pre-registrado en el expediente de Astra — **ninguno nuevo**, regla 6), con potencia calculada, `sello.json`, y fila en la vista o CONTADOR «sellada en disco, no registrada». PROSPECTIVA por construcción: la R (2027) no existe.
(P4) **Expediente v1.1.** `familias-2027-estado-v1_1.tsv` con las cinco en `LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA (gate: DATO-2027-AUSENTE)`, ENCIG-PAGO-DIGITAL suspendida (gate vigente), ENOE-INFORMALIDAD y ENSU-CAMPECHE en NO-LANZAR-TODAVIA con su contrato pendiente; atestación externa: `.ots` del manifiesto de sellos sigue siendo de mesa (SELLO-EXTERNO-2); hoja RH con lo que quede para mesa (contratos de ENOE/ENSU; PAGO-DIGITAL).

«Hecho», por comando sobre el commit final con `origin/main` fusionado: por familia desbloqueada, tres commits en orden (spec → emisiones), `corrida0 preflight` VERDE, `sello.json`, potencia en el expediente, guardia con prueba por mutación verde · FP de B4/E3/E4 FIRMADA con este PR · expediente v1.1 con las ocho familias y ningún gate vacío · ninguna ola reservada abierta (cruce con el manifiesto) · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
Mesa 28/sep «firmado» → ADENDA-1 de HOJA-FIRMAS-21-1: «B4 las tres · E3 1 · E4 1» (opciones de la hoja de NC-DECISIONES-1; texto de cada una en `forense/analisis/nc-decisiones/hoja-2026-09-27.md`) · MISION-ASTRA-6 + ADENDA-1 (C2) · regla 6 · E.6 (tres commits; guardia; candidatos declarados juntos; una comparación primaria) · `71cf-01` (frontera recibida sin adoptar) · ASTRA-CONTINUIDAD-C2-1 (expediente v1.0, hoja). **No firmado y no se hace aquí:** contratos de ENOE-INFORMALIDAD y ENSU-CAMPECHE; reactivación de PAGO-DIGITAL; apertura de cualquier ola.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `16ba3d02` · `forense/analisis/familias-2027/familias-2027-estado-v1_0.tsv`: 8 filas; gate `FIRMA-DE-MESA(f2e5-…)` en ENIF-AHORRO-FORMAL, ENIF-HORIZONTE-AHORRO, ENCIG-SOLICITUD-MORDIDA, ENVIPE-DENUNCIA-U4, ENVIPE-EVASION-NORMA; ENCIG-PAGO-DIGITAL SUSPENDIDA (contexto/gate); ENOE-INFORMALIDAD y ENSU-CAMPECHE NO-LANZAR-TODAVIA (CONTRATO-FIRMADO pendiente). Expedientes por instrumento: `astra6-enif/`, `astra6-encig/`, `astra6-envipe/`, `astra6-cierre-material-1/`.
- [LEÍDO] Hoja de C2 (`hoja-c2-para-mesa-v1_0.md`) y `EXPEDIENTE-v1_0.md`: qué está congelado con sha y qué falta por familia. Transfer de Astra §7: «no asumir que manifiesto de sellos equivale a OTS».
- [SUPUESTO] Que las specs de Astra para las cinco familias existen como archivo y solo les falta la forma firmada; si una es prosa, COMMIT-1 la reescribe como spec (PROPUESTO-POR-EJECUTOR, declarado) sin cambiar estimando.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'C2-EJECUCION\|FAMILIAS-2027-COMMIT'` → 0. Consumidos y citados: ASTRA6 C2 de Codex (#1195 frontera, #1222 ENOE, cierre material), ASTRA-CONTINUIDAD-C2-1. En vuelo en caja: PISOS-Y-ADENDAS-1, CORPUS-CACHE-PARQUET-1, C1-LOTE-3 (ENDIREH; disjunto), RELEVO-TRAMITE-CAJA-1 (ENIF 2024 también: **coordinar por archivo**, no por rama; sus specs viven en `prereg-caja/`, las tuyas en `familias-2027/`).

## 5 · PIEZAS
P1 → por familia (ENIF ×2, ENCIG, ENVIPE ×2): COMMIT-1 → COMMIT-2 → P4. Rama prevista: potencia insuficiente para adjudicar → se sella igual con la potencia declarada y la familia queda LISTA con reserva; módulo de ENIF 2024 cerrado por reserva → la emisión usa 2021 como piso y lo declara.

## 6 · LATITUD
Orden de familias, un PR por familia o dos, formato de potencia: tuyos, declarados antes del COMMIT-1 de cada una. PREGUNTA A MESA: ninguna fuera de la hoja. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir una ola reservada o un módulo cerrado · b) editar una emisión ya sellada, un `prereg-*`, un sello, una fila FIRMADA · c) adoptar; añadir un retador nuevo; derivar una R · d) cambiar spec tras COMMIT-1 · e) NUBE · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«COMMIT-1 con guardia probada antes de tocar dato» protege **abrir dato** y **congelar** · «Emisiones selladas antes de que exista la R» protege **adoptar** (PROSPECTIVA) · «Sin retadores nuevos» protege **adoptar** (regla 6) · «Reservadas intactas» protege **abrir dato**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/analisis/familias-2027/` (expediente v1.1, hoja, specs por familia), `data/corrida0/CALC-<llave>/` de las emisiones, `firmas-pendientes.tsv` (marcar FIRMADA B4/E3/E4), nota, L0, cascada. Ajeno: `prereg-caja/` (RELEVO-TRAMITE), `validacion-independiente/` (C1), sellos existentes, vistas (canal). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No abre olas 2027 ni reservadas, no adopta, no reactiva PAGO-DIGITAL, no firma contratos de ENOE/ENSU, no deriva R. Sucesores: SELLO-EXTERNO-2 (`.ots`, mesa); apertura por familia cuando llegue su ola (COMMIT-3); FIRMAS-22. Módulo de auditoría v2.16 en cada spec (afirma qué predice el programa): PROSPECTIVA; unidad; oferta antes que preferencia en ENIF. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-ASTRA6-C2-EJECUCION-1-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «(P2) COMMIT-1 por familia desbloqueada …» y «(P3) COMMIT-2: emisiones selladas desde las olas vistas …» | SUSTITUIDO-POR:ASTRA6-C2-ENIF-1+ASTRA6-C2-ENCIG-1+ASTRA6-C2-ENVIPE-1 — ya sellados el 26/09. **Absorbe:** COMMIT-1 (spec v1_3 + spec.yaml) y COMMIT-2 (emisión sellada) de las cinco familias. **Huérfano:** nada; verificado aquí (sellos 5/5 COINCIDE, guardias y mutación verdes). Mesa 28/sep: «YA-HECHO: verificar». | ningún contador; no se sella contendiente nuevo (regla 6) | COMMIT-3 por familia cuando llegue su ola |
| «Hecho: … `corrida0 preflight` VERDE» por familia | NO-VERIFICABLE-AQUÍ — los cinco CALC ya están sellados: preflight BLOQUEADO por `CALC-INMUTABLE-YA-SELLADO`, y los dos de ENVIPE no siguen el esquema corrida0 (NC …ba6c-02). En su lugar: SELLO_COINCIDE 5/5. El único COMMIT-1 nuevo (oferta ENIF 2024) sí dio preflight VERDE. | ninguno | COMMIT-3 por familia (CALC nuevo con su propio preflight) |
| medida de exclusión por oferta junto al marginal de **canal** (ENCIG-PAGO-DIGITAL) | DIFERIDO-A:reactivación de ENCIG-PAGO-DIGITAL — la familia está SUSPENDIDA; la de ahorro (ENIF) sí se midió | el marginal de canal no se publica mientras esté suspendida | FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01 |
| `tests/test_din_oferta_enif2024.py` en CI | NO-VERIFICABLE-AQUÍ — corre en CAJA (14 passed); en CI se salta por NECESITA-DEPENDENCIA(numpy), fila copiada de `test_astra6_encig.py` | la guardia de mutación del CALC de oferta no la juzga el runner | FP-398 (dependencias del runner; FIRMADA, ejecución pendiente) |

## CONSUMIDO

Ejecutado por PR #1279 (rama `acto/gen2-astra6-c2-ejecucion-1`, ADR-260928-GEN2-ASTRA6-C2-EJECUCION-1-e897-01), 28/sep/2026. Adendas recibidas: ninguna. Decisiones de mesa de la sesión, verbatim, en `forense/notas/2026-09-28-GEN2-ASTRA6-C2-EJECUCION-1-cierre.md` §1.
