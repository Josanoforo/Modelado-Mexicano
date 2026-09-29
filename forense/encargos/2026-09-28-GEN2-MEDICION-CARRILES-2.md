# ENCARGO · ACTO GEN2-MEDICION-CARRILES-2 · El frente de medición entero, con la latitud de un investigador principal: el tablero de carriles marca qué reports están en rojo o amarillo y qué afirmaciones, reglas y dominios siguen sin cifra; el corpus tiene 7 000 payloads, caché columnar y 41 GB de microdato; la sesión mide **todo lo que el corpus permite** —afirmaciones MEDIBLE-EN-CORPUS aún sin RESULT, las 141 reglas sin cifra con instrumento, los dominios sin estimador, y la segmentación que §3 exige (región, clase, edad, género, escolaridad, urbanización) sobre los pisos ya adoptados—, baja y registra lo público que falte para lo que no, y deja el frente listo para el cierre siguiente. Decide qué, en qué orden y con qué profundidad; lo que no mida, dice por qué con vocabulario A.4

> ENTORNO: **CAJA** — microdato de olas vistas o abiertas-como-vistas bajo spec congelada; `tools/corpus_loader.py` para todo lo que tenga caché; descargas públicas por `/adquiere`. Hook imprime ENTORNO-DERIVADO; si dice cloud_default o milpa-inegi, PARA. Sesión pesada; el tope de sesiones lo fijó CACHE-PARQUET-1 y las ramas hijas van **en serie o dos en paralelo**.

CABECERA · SHA de redacción `9d2550b9` (re-deriva al abrir; el tablero de carriles se regenera al abrir y es tu tabla de apertura) · una sesión, rama principal del acto con hijas por instrumento (una hija = un PR = un ADR; fusionada y borrada antes de la siguiente, salvo dos en paralelo) · MODELO: **Opus** (mide; no baja) · MODO: **RÍGIDO** por CALC desde COMMIT-1; **AUTÓNOMO-AMPLIO** para todo lo demás · ids con raíz de acto · D-21 aplica.
CONTADOR: **cuenta_gen2 = SÍ**; no adopta (mesa por merge, por instrumento). Mueve `payloads` por `/adquiere` con sha y licencia. **NC solo por D-19**; lo reversible se decide y se declara.

## 1 · OBJETIVO
(P1) **Tabla de apertura desde el tablero.** `python3 tools/tablero_carriles.py --actualiza` y, de ahí, por carril rojo o amarillo: afirmaciones `MEDIBLE-EN-CORPUS` sin RESULT (del mapa, 235 en total), reglas `SIN-CIFRA-GEN2` con instrumento (`reglas-contrastadas-v1_1.tsv`), dominios sin estimador, y cruces de segmentación que faltan sobre pisos adoptados (catálogo v1.3/v1.4: por cada piso marginal, qué ejes de §3 tiene y cuáles no). Estado de reserva por id para cada instrumento × ola. Lo que ya está sellado se cita, no se re-mide (E.5).
(P2) **Medición.** Una spec humana (+ sidecar) y spec.yaml por instrumento × ola que agrupe todo lo que ese instrumento sostiene (afirmaciones, reglas, cruces), con estimando por celda, universo, unidad, escala, códigos por texto de pregunta (A.15), ponderador y diseño desde codebook, agregador (E.1), pre-registro de falsación por regla, oferta antes que preferencia donde sea mercado, firewall genético (nada de ascendencia → conducta). COMMIT-1 antes de abrir; RESULT sellados; fila en la vista (E.7); contraste CONFIRMA / MATIZA / ROMPE por regla en `reglas-contrastadas-v1_2.tsv`. Sin retadores ni θ (regla 6); momentos HOLDOUT solo los marcados GASTABLE-COMO-PISO en el catálogo de momentos y declarados.
(P3) **Adquisición de lo que falte y sea público.** Para afirmaciones y reglas cuyo instrumento no está en el corpus pero la cola o el mapa lo nombran con URL pública: bajar por `/adquiere` (sha, licencia, `url_origen`), registrar, y si la ola es nueva de un programa con historia, dejarla RESERVADA y no medirla. Lo que exija identidad queda en la lista de solicitudes de OBTENCION-EXTERNA-1 (no se duplica); lo que no exista en ningún portal: NO-ENCONTRADO con dónde y términos.
(P4) **Cierre de frente.** Conteos por comando (afirmaciones medidas, reglas con dictamen, dominios con estimador, cruces por eje, payloads nuevos, NO-CONSTRUIBLE con texto y secciones, diferidos por reserva) y el bloque candidato de adopción por instrumento para el cierre siguiente; hoja RH solo con lo irreversible (aperturas que convendría pedir, con opciones).

«Hecho», por comando sobre el commit final con `origin/main` fusionado: por CALC, dos commits en orden, `corrida0 preflight` VERDE, `sello.json`, fila en la vista · `tablero_carriles.py --actualiza` en el commit final muestra menos carriles rojos que al abrir, y la nota explica cada cambio por CALC · `reglas-contrastadas-v1_2.tsv` con SIN-CIFRA-GEN2 menor que 141 y cada cambio con `resultado_id` existente · cruces nuevos por eje listados con su RESULT · ninguna ola reservada abierta (cruce con el manifiesto) · payloads nuevos verificables por id · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
ADENDA-1 de TRAMITE-FIRMAS-21 (HOLDOUT (b); ENCRIGE 2020 y ENVE 2024 abiertas-como-vistas; CSES M5, ENDUTIH 2025, ENIF 2024 m7 reservadas; CAAS/ENGPEE/MSM liberadas; R19 reglas como propuestas), `ee49` y el acceso a ENBIARE/ENCODAT (C1: no aplica aquí salvo como olas vistas para pisos), §3, §4, E.2, E.5, E.6, D-15, D-22. Mesa 28/sep: «guía explorador … la vasta y casi infinita posibilidad que tiene». Adopción: por merge, por instrumento.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `9d2550b9` · `mapa11_dominios_medidos` 17 de 28 (subirá con el catálogo v1.4); `reglas-contrastadas-v1_1.tsv`: SIN-CIFRA-GEN2 141, MATIZA-SIN-CRUCE 8, MATIZA 7, CONFIRMA 6; `mapa-dominios-v1_1.tsv`: MEDIBLE-EN-CORPUS 235, MEDIBLE-CON-ADQUISICIÓN 717 (611 sin equivalencia de instrumento: no son descargas); cola de adquisición 952 fuentes, OBTENIDO ~96 %; `forense/tablero/TABLERO-CARRILES.md` y `canon/crosswalk-carriles-v1_0.tsv` existen; `tools/corpus_loader.py` y `data/cache/` existen.
- [LEÍDO] Notas de cierre de PISOS-DOMINIOS-Y-REGLAS-1 (10 piezas por instrumento, ENVIPE 2025 diferida), CALC-ALTERNOS-LOTE-1 y RELEVO-TRAMITE-CAJA-1: sus specs en `prereg-caja/` son modelo y cita; sus NO-CONSTRUIBLE no se repiten sin motivo nuevo.
- [SUPUESTO] Que el tablero de carriles marca semáforo por carril con la regla declarada; si su regla resulta demasiado laxa o estricta para decidir qué medir, la sesión usa su criterio, lo declara y lo propone como cambio al tablero.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'MEDICION-CARRILES'` → 0. Consumidos y citados: todos los actos de caja de esta semana (§3), MAPA-INSTRUMENTOS-ALTERNOS-1, OBTENCION-EXTERNA-1, CORPUS-LICENCIAS-1. En vuelo: CIERRE-Y-PRODUCTO-3 (nube: consume lo sellado hasta su apertura; lo tuyo va al cierre siguiente), VALIDACION-Y-2027-1 (caja: `validacion-independiente/` y `familias-2027/`, disjunto; comparte el tope de sesiones), el `[deriva]`.

## 5 · PIEZAS
Las decide la sesión. Criterio sugerido: primero lo que más carriles saca de rojo por instrumento, luego cruces de segmentación de los pisos más citados, luego adquisición. Rama prevista: variable sin etiqueta → NO-CONSTRUIBLE con texto y secciones; instrumento reservado → DIFERIDO-A apertura con la firma que lo abriría en la hoja; memoria insuficiente → una hija a la vez.

## 6 · LATITUD — de guía
Qué medir primero, cómo agrupar specs, qué ejes de segmentación, qué NO medir y por qué, cuántos PR, cuándo parar el frente: tuyos, declarados en la nota y en cada spec antes del COMMIT-1. Puedes proponer instrumentos y cruces que el mapa no listó (PROPUESTO-POR-EJECUTOR). PREGUNTA A MESA: solo aperturas de reserva, en la hoja, con opciones. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir ola reservada; abrir antes del COMMIT-1 · b) editar sellos, catálogo, el mapa, `reglas-contrastadas-v1_1` · c) adoptar; retador; momento no GASTABLE; medir genética · d) cambiar spec tras COMMIT-1 · e) NUBE · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«COMMIT-1 antes de abrir» protege **abrir dato** y **congelar** · «Primer resultado es el que se reporta» protege **adoptar** · «Reservadas intactas; ola nueva nace reservada» protege **abrir dato** · «Lo sellado se cita» protege **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/`, `data/corrida0/CALC-<llave>/`, `canon/reglas-contrastadas-v1_2.tsv`, `data/manifiesto.yaml` (append por `/adquiere`), `data/raw/`, `forense/analisis/medicion-carriles-2/`, nota, L0, cascada. Ajeno: vistas (canal), `canon/catalogo-*` (cierre), `validacion-independiente/`, `familias-2027/`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No adopta, no abre reservadas, no valida a ciegas (VALIDACION-Y-2027-1), no escribe el catálogo (cierre). Sucesores: el cierre siguiente; `MEDICION-CARRILES-3` cuando se abran olas o lleguen respuestas de solicitudes. Módulo de auditoría v2.16 en cada spec. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-MEDICION-CARRILES-2-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

- **qué:** «(P3) Adquisición de lo que falte y sea público» — **por qué:** DIFERIDO-A:GEN2-MEDICION-CARRILES-3 — el frente se cerró tras tres hijas por instrumento (decisión del ejecutor, latitud §6); ninguna descarga corrida — **impacto:** payloads nuevos 0; afirmaciones MEDIBLE-CON-ADQUISICIÓN sin mover — **sucesor:** GEN2-MEDICION-CARRILES-3.
- **qué:** «(P2) Medición … por instrumento × ola» para 108 afirmaciones MEDIBLE-EN-CORPUS pendientes (ENOE 11, ENDUTIH 9, ENIGH 9, ENUT 7, ENCUCI 7, ENADID 7, ENDIREH 5 y resto; `forense/analisis/medicion-carriles-2/tabla-apertura-mc2-v1_0.tsv`, decisión PENDIENTE-*) — **por qué:** DIFERIDO-A:GEN2-MEDICION-CARRILES-3 — **impacto:** 108 afirmaciones sin RESULT propio; carriles AMARILLOS de TRABAJO, TECNOLOGIA, MOVILIDAD sin cifra nueva — **sucesor:** GEN2-MEDICION-CARRILES-3.
- **qué:** afirmaciones APUEST-030, APUEST-032, CONS-010 (ENIF 2024 módulo 7) — **por qué:** DIFERIDO-A:GEN2-MEDICION-CARRILES-3 — módulo 7 RESERVADO por R06; apertura parcial propuesta en `forense/analisis/medicion-carriles-2/hoja-rh.md` — **impacto:** 3 afirmaciones sin RESULT — **sucesor:** GEN2-MEDICION-CARRILES-3 (tras firma de la hoja RH).
- **qué:** «Hecho»: «`tablero_carriles.py --actualiza` en el commit final muestra menos carriles rojos que al abrir» — **por qué:** DECISIÓN-DE-MESA-PENDIENTE — la regla ROJO cuenta sólo cifra adoptada (`tools/tablero_carriles.py:53`); ningún acto que mide sin adoptar la mueve; propuesta NARANJA en la nota §3 y la hoja RH — **impacto:** contador ROJO 7 → 7 — **sucesor:** FP-260928-GEN2-MEDICION-CARRILES-2-8fdf-01 (mesa decide la regla del tablero).

## CONSUMIDO

Consumido por `ACTO GEN2-MEDICION-CARRILES-2` en tres PR por instrumento: #1311 (ENIF 2024, fusionado), #1314 (ENSANUT 2024, fusionado) y #1316 (ENVIPE 2025 + cierre). ADR `ADR-260928-GEN2-MEDICION-CARRILES-2-8fdf-01..03`. Nota: `forense/notas/2026-09-28-GEN2-MEDICION-CARRILES-2-cierre.md`.
- Adenda: `2026-09-28-GEN2-MEDICION-CARRILES-2-ADENDA-1.md` (firma R06 m7 ABIERTA-PARCIAL), consumida por #1317 (ADR `…-8fdf-04`).
- Cierre final: hijas #1324 (NARANJA), #1327 (ENOE), #1336 (ENIGH), #1339 (ENUT), #1346 (ENDUTIH) y este PR de cierre (ADR `…-8fdf-06..10`); ADENDA-2 consumida.
