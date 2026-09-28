# ENCARGO · ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · El informe v1.5 dice que solo 17 de los 28 dominios del mapa tienen estimador adoptado, y REGLAS-Y-RESULT-1 encontró que 145 de 162 reglas del motor no tienen ninguna cifra GEN2 detrás. Este lote de caja mide lo que cierra las dos brechas a la vez: pisos descriptivos RETROSPECTIVOS, por dominio sin estimador y por regla sin cifra, sobre los instrumentos del corpus que el mapa y la tabla de reglas ya identificaron por texto de pregunta — con spec y COMMIT-1 por instrumento, sin retadores, sin abrir reservas, y decidiendo lo reversible en vez de abrir NC

> ENTORNO: **CAJA** — abre microdato de olas vistas o abiertas-como-vistas (según el manifiesto tras TRAMITE-FIRMAS-21) bajo spec congelada; usa `tools/corpus_loader.py` donde haya caché. Hook imprime ENTORNO-DERIVADO; si dice cloud_default o milpa-inegi, PARA. Sesión pesada; respeta el tope que fijó CACHE-PARQUET-1.

CABECERA · SHA de redacción `98f80cc7` (re-deriva al abrir) · una sesión, rama propia; PR por instrumento, dos commits por CALC (D-24) · MODELO: **Opus** (mide; no baja) · MODO: **RÍGIDO** por CALC desde COMMIT-1; ABIERTO para agrupar · ids con raíz de acto · D-21 aplica.
CONTADOR: **cuenta_gen2 = SÍ**; no adopta (mesa por merge). Mueve `mapa11_dominios_medidos` (informe) y `reglas_con_cifra` (tabla de reglas) hacia arriba solo por RESULT sellados con fila en la vista. **NC solo por D-19**; lo reversible se decide y se declara.

## 1 · OBJETIVO
(P1) **Universo, derivado, no tecleado.** Los 11 dominios sin estimador adoptado = complemento de `python3 forense/analisis/informe-v1_5/cifra_v1_5.py mapa11_dominios_medidos` (que hoy imprime 17) sobre los 28 dominios de `canon/mapa-dominios-v1_1.tsv`; por cada uno, sus afirmaciones `MEDIBLE-EN-CORPUS` (235 en total en el mapa) con instrumento y ola. Las reglas: filas `SIN-CIFRA-GEN2` de `canon/reglas-contrastadas-v1_0.tsv` cuya columna de instrumento nombra uno del corpus (excluidas «ninguno», «NO-APLICA», vacías, y **toda regla del dominio GENETICA**: firewall §3, no se mide ascendencia → conducta bajo ninguna forma). Tabla de apertura: dominio · regla_id o afirmación · instrumento · ola · reactivo (texto, sección) · unidad · estado de reserva por id.
(P2) **Specs por instrumento.** Una spec humana (+ sidecar) y un spec.yaml por instrumento × ola, que agrupe todas las afirmaciones y reglas que ese instrumento sostiene: estimando por celda, universo, unidad, escala, códigos por texto de pregunta (A.15), ponderador y diseño desde codebook, agregador (E.1), pre-registro de falsación por regla (qué pasa si el piso no la sostiene: CONFIRMA / MATIZA / ROMPE en la unidad de la regla), oferta antes que preferencia donde sea mercado. COMMIT-1 antes de abrir dato. Lo ya sellado se cita (E.5): ENCIG confianza (PISOS-Y-ADENDAS-1), pisos de ENIF/ENCUCI/ENIGH (RELEVO-TRAMITE-CAJA-1), momentos (CALC-ALTERNOS-LOTE-1, en vuelo: **sus llaves no se repiten**; coordina por spec).
(P3) **Corridas y contraste.** RESULT sellados, fila en la vista (E.7); para cada regla medida, el dictamen CONFIRMA / MATIZA / ROMPE con punto e IC en su unidad, escrito en `canon/reglas-contrastadas-v1_1.tsv` (versión nueva; la v1.0 no se edita); para cada dominio, la fila de `mapa-dominios` que pasa a «estimador adoptado» queda **propuesta** hasta el merge.
(P4) **Cierre.** Conteos por comando: dominios que ganan estimador, reglas que pasan de SIN-CIFRA a dictamen, NO-CONSTRUIBLE (texto y secciones) y diferidos por reserva; bloque candidato de adopción para CIERRE-SEMANAL-3; hoja RH solo si queda algo irreversible.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: por CALC, dos commits en orden, `corrida0 preflight` VERDE, `sello.json`, fila en la vista · `cifra_v1_5.py mapa11_dominios_medidos` (o su sucesor) mayor que 17 tras el merge, y la nota dice cuánto y por qué CALC · `reglas-contrastadas-v1_1.tsv` con `SIN-CIFRA-GEN2` menor que 145 y cada cambio con `resultado_id` existente · ninguna ola reservada abierta · ninguna regla GENETICA medida · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
Mesa 28/sep «firmado» (ADENDA-1 de TRAMITE-FIRMAS-21): R01 HOLDOUT (b) — este acto **no** mide momentos; R02/R03 ENCRIGE 2020 y ENVE 2024 abiertas-como-vistas; R04/R05/R06 reservadas; R09 D1 (a); R19 (1) — las 107 reglas de C3 son inventario de propuestas, aquí se contrastan, no se adoptan. §3 (firewall genético; procedencia; segmentación), §4 (pisos; regla 6; unidad; RETROSPECTIVA), §5 (regla sin RESULT queda PROPUESTA), E.2, E.5, E.6, D-15, D-22. Adopción: por merge, con CIERRE-SEMANAL-3.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `98f80cc7` · `cifra_v1_5.py mapa11_dominios_medidos` → 17 (de 28). `reglas-contrastadas-v1_0.tsv`: 162 reglas; SIN-CIFRA-GEN2 145, MATIZA-SIN-CRUCE 8, MATIZA 6, CONFIRMA 3; columna de instrumento: vacía 26, NO-APLICA 17, «ninguno» 4, resto con instrumento nombrado (ENIF, ENADID/ENIGH, ENASIC, ENDUTIH…); por dominio: CONSUMO 13, GENETICA 12, CONFIANZA 9, TRABAJO 8, INTERACCION 8, CAPITAL_SOCIAL 7, FAMILIA_CUIDADOS 7, FAMILIA 7, TECNOLOGIA 6, POLITICA 6, SEGURIDAD 5. `mapa-dominios-v1_1.tsv`: 1 396 afirmaciones, MEDIBLE-EN-CORPUS 235.
- [EJECUTADO] `corrida0 demanda` tras DEMANDA-DICTAMEN-1: corridas requeridas 0 (105 no requeridas por dictamen), pendientes 63 (SIN-BASE-GEN2 17, CELDA-D-ADJUDICADA 17, ESPERA-FIRMA-HOLDOUT 15 — ya decidido (b) —, ESPERA-FIRMA-MESA 5). La demanda de relevo está agotada; la demanda de producto es esta: dominios y reglas sin cifra.
- [EXISTE] `tools/corpus_loader.py`, `data/cache/constancias.tsv` (CACHE-PARQUET-1), `prereg-caja/` con las specs de RELEVO-TRAMITE-CAJA-1 y PISOS-Y-ADENDAS-1 (modelo y cita).
- [SUPUESTO] Que la columna de instrumento de la tabla de reglas basta para localizar el reactivo; si no, se cruza con el mapa de instrumentos alternos por texto y se declara.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'PISOS-DOMINIOS\|REGLAS-CAJA\|DOMINIOS-FALTANTES'` → 0. Consumidos y citados: REGLAS-Y-RESULT-1, MAPA-INSTRUMENTOS-ALTERNOS-1, PISOS-Y-ADENDAS-1, RELEVO-TRAMITE-CAJA-1, DEMANDA-DICTAMEN-1, CIERRE-SEMANAL-2 (catálogo v1.3). En vuelo en caja: CALC-ALTERNOS-LOTE-1 (momentos: llaves distintas; mismo instrumento posible: coordinar por archivo de spec) y C1-SUCESORES-Y-LOTE-3 (ENBIARE/ENCODAT: disjunto). Nube: TUBERIA-3.

## 5 · PIEZAS
P1 → P2/P3 por instrumento, del que más dominios cubre al que menos → P4. Rama prevista: instrumento con reserva vigente → DIFERIDO-A apertura en la nota; regla con unidad distinta de la del instrumento → INCOMPARABLE con el enlace que faltaría; dominio cuyo único instrumento está reservado → queda sin estimador y la nota lo dice con id.

## 6 · LATITUD — amplia
Agrupación, orden, PR, qué reglas entran en qué spec: tuyos, declarados en cada spec antes del COMMIT-1. Lo reversible se decide y se declara. PREGUNTA A MESA: ninguna; adopción por merge. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir ola reservada; abrir antes del COMMIT-1 · b) editar sellos, `reglas-contrastadas-v1_0`, el mapa · c) adoptar; retador; medir un momento HOLDOUT; medir una regla GENETICA · d) cambiar spec tras COMMIT-1 · e) NUBE · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«COMMIT-1 antes de abrir» protege **abrir dato** y **congelar** · «Primer resultado es el que se reporta» protege **adoptar** · «Firewall genético» protege **adoptar** (§3) · «Lo sellado se cita» protege **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/` (specs nuevas), `data/corrida0/CALC-<llave>/`, `canon/reglas-contrastadas-v1_1.tsv`, `forense/analisis/pisos-dominios-1/` (tabla de apertura, conteos, bloque), nota, L0, cascada. Ajeno: vistas (canal), `canon/mapa-dominios-*`, `canon/catalogo-*` (CIERRE-SEMANAL-3), llaves de CALC-ALTERNOS, `validacion-independiente/`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No adopta, no toca momentos, no abre reservadas, no mide genética, no edita el mapa de dominios (lo hace el cierre semanal con lo adoptado). Sucesores: CIERRE-SEMANAL-3 (catálogo v1.4, informe v1.6 con dominios medidos y reglas con cifra), `PISOS-DOMINIOS-Y-REGLAS-2` con las olas que se abran. Módulo de auditoría v2.16 en cada spec (afirman sobre México): unidad, escala, RETROSPECTIVA, segmentación, ¿incentivo o psicología?, ¿clase media urbana?, ¿qué sería peligroso leído simplista? El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-ADENDA-N.md`, selladas al recibirse.
