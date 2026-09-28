# ENCARGO · ACTO GEN2-APERTURAS-PREREGISTRADAS-1 · Toda ola reservada del corpus (las 19 que entraron con CORPUS-COMPLETO, las cinco que mesa decidió el 28/sep, ENVIPE 2026, ENCO, el último periodo de ENOE y ENSU, ENSANUT 2024, ENCODAT 2025, ENDUTIH 2025, ENIF 2024 m7, y las que OBTENCION-EXTERNA-1 trajo) tiene hoy una sola forma legítima de abrirse: el código congelado de una prueba pre-registrada, o mesa por escrito. Ninguna tiene esa prueba escrita. Este acto deja, por ola reservada, el expediente de apertura completo —qué contendientes sellados la esperan, qué familia 2027 la usa como R, la spec humana y el spec.yaml del cálculo que se haría al abrir, la guardia de una sola variable de agrupación probada por mutación sobre sintético— de modo que cuando mesa abra una ola, la apertura sea un commit y no un acto. Nada se abre aquí

> ENTORNO: **NUBE** — cuestionarios, FD, descriptores, specs, sellos; ningún microdato reservado ni tabulado ni comunicado de ola reservada (E.6). Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA. El preflight en caja lo hace la apertura, no este acto.

CABECERA · SHA de redacción `9d2550b9` (re-deriva al abrir) · una sesión, rama propia; PR por programa · MODELO: **Opus** (cada expediente es diseño de prueba) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto · D-21 aplica.
CONTADOR: cero mediciones; no adopta; no abre. **NC solo por D-19.**

## 1 · OBJETIVO
(P1) **Inventario de reservadas por id** (A.15): del manifiesto, toda entrada cuya ola esté reservada (campo `reserva` o el que TRAMITE-FIRMAS-21 haya dejado: verificar el nombre y el vocabulario y declararlos), agrupada por programa × ola, con: contendientes ya sellados que la nombran como R (`prereg-*`, familias 2027, CALC con `reserva_de_evaluacion`), cruces vistos que la anteceden, y qué la abriría (código congelado de prueba pre-registrada · firma de mesa · ninguna razón para abrirla aún).
(P2) **Expediente de apertura por ola** en `forense/prereg-aperturas/<programa>-<ola>/`: spec humana (+ sidecar) que baste para recalcular sin leer código (D-15) — estimandos que se medirían al abrir, universo, unidad, escala, códigos por texto de pregunta del cuestionario de esa ola (permitido: cuestionario y FD sí se leen), ponderador y diseño desde el descriptor, agregador; spec.yaml; el medidor con la **guardia de una sola variable de agrupación** y su prueba por mutación sobre un sintético que imite el esquema de la ola (E.6); la regla y el umbral de adjudicación fijados antes; la lista de contendientes que la apertura serviría a la vez, con una sola comparación primaria (E.6: «una apertura sirve a todos los sellados antes»). Para olas sin contendiente ni familia que las use: expediente mínimo (inventario + «sin prueba pre-registrada: solo mesa por escrito») y nada más.
(P3) **Vista y receta.** `data/corrida0/aperturas-pendientes-v1_0.tsv` (programa · ola · ids · contendientes · familia · expediente · qué la abre · firma que faltaría), registrada en INFRAESTRUCTURA y leída por el tablero de carriles como stopper RESERVA con su expediente; y por ola, la receta de apertura de un commit (qué correr en caja, en qué orden: preflight → COMMIT-3 → adjudicación → asiento) para que el acto de apertura no diseñe nada.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: toda ola reservada del manifiesto tiene fila en `aperturas-pendientes-v1_0.tsv` (ids sin fila: 0) · toda ola con contendiente o familia tiene expediente con spec, yaml, medidor con guardia y prueba por mutación verde sobre sintético · ningún archivo de microdato, tabulado ni comunicado de ola reservada leído (lista de archivos leídos en la nota; test de que ningún payload reservado aparece en ella) · el tablero de carriles lee la vista · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
E.6 completo (toda ola nueva nace reservada; la levanta solo código congelado de prueba pre-registrada o mesa por escrito; bajar y hashear no es abrir; tabulados y comunicados tampoco se leen; una apertura sirve a todos los sellados antes) · ADENDA-1 de TRAMITE-FIRMAS-21 (R04/R05/R06 reservadas; R02/R03 vistas; R09; R15 reserva de C1 por paquete) · regla 6 (los contendientes son los ya sellados; ninguno nuevo) · D-15, D-22, D-24. **Nada se abre**: eso es de mesa o del código congelado, después.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `9d2550b9` · manifiesto: 0 entradas con `reserva` que empiece por RESERV; el 27/sep había 175 con campo de reserva (cc1 138, ENSANUT 24, oe1 6, ENCODAT 3, ENOE 2, ENCO 2). TRAMITE-FIRMAS-21 escribió el campo para nueve olas: el nombre o el vocabulario cambió y **se verifica por id antes de nada** (A.15); es el primer hallazgo del acto, no PARO.
- [LEÍDO] Transfer 26/sep §6: «ENVIPE 2026, ENCO, último periodo de ENOE/ENSU y las 19 olas nuevas del corpus, intocables». Expediente de familias 2027 v1.1 (VALIDACION-Y-2027-1 hará v1.2): qué ola usa cada familia como R. `forense/prereg-duelo-v2/` y `prereg-caja/` (formato de spec y de guardia; MOTOR-3 y ENIGH2024 como precedente de guardia por mutación).
- [SUPUESTO] Que los cuestionarios y FD de las olas reservadas están en el corpus (bajar documentación es legítimo); si falta alguno, se baja desde milpa-inegi y se registra.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'APERTURAS-PREREG\|PREREG-APERTURA'` → 0. Consumidos y citados: CORPUS-COMPLETO-1 (19 reservadas), ENIGH2024 (apertura parcial C7: modelo de expediente), C2-EJECUCION-1 y ASTRA-CONTINUIDAD-C2-1 (familias con guardia), TRAMITE-FIRMAS-21. En vuelo: VALIDACION-Y-2027-1 (caja: familias; **no dupliques sus specs**: cítalas como contendientes), MEDICION-CARRILES-2, CIERRE-Y-PRODUCTO-3, MAPA-DOMINIOS-Y-LICENCIAS-1 (manifiesto: solo `licencia`; tú solo lees).

## 5 · PIEZAS
P1 → P2 por programa, primero las olas con contendiente o familia (ENVIPE 2026, ENCIG 2025 fuera del árbitro, ENIF 2024 m7, ENSANUT 2024, ENOE/ENSU último periodo, ENDUTIH 2025, CSES M5, ENCODAT 2025) → P3. Rama prevista: cuestionario de la ola reservada ausente y no descargable → expediente sobre el cuestionario de la ola anterior, rotulado y con la diferencia declarada al abrir.

## 6 · LATITUD — de guía
Formato del expediente, qué estimandos incluir por ola, cómo modelar el sintético, orden: tuyos. PREGUNTA A MESA: ninguna; la vista muestra qué firma abriría cada ola. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) leer microdato, tabulado o comunicado de una ola reservada · b) editar un sello, una emisión, un `prereg-*` existente, el manifiesto · c) adoptar; declarar una ola abierta; añadir un contendiente nuevo · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Ningún archivo de ola reservada en la lista de leídos» protege **abrir dato** (E.6) · «Guardia probada por mutación antes de existir la apertura» protege **congelar** · «Contendientes solo los ya sellados» protege **adoptar** (regla 6).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-aperturas/` (nuevo), `data/corrida0/aperturas-pendientes-v1_0.tsv` (registrado en INFRAESTRUCTURA), `tools/tablero_carriles.py` (≤ 10 líneas para leer la vista, declaradas), documentación nueva por `/adquiere`, nota, L0, cascada. Ajeno: `familias-2027/` (VALIDACION-Y-2027-1), `prereg-caja/` (MEDICION-CARRILES-2), sellos, manifiesto salvo documentación nueva. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No abre, no mide, no adopta, no pide firmas (la vista las muestra). Sucesores: cada apertura, cuando mesa firme o el código congelado la haga, como acto de un commit sobre su expediente; `APERTURAS-PREREGISTRADAS-2` cuando entren olas nuevas. Módulo de auditoría v2.16 en cada spec (afirman qué se medirá sobre México): PROSPECTIVA por construcción; unidad; segmentación. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-APERTURAS-PREREGISTRADAS-1-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

- Ninguno.
