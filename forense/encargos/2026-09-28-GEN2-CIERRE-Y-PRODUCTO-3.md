# ENCARGO · ACTO GEN2-CIERRE-Y-PRODUCTO-3 · El cierre de la semana del 27–28/sep como acto de producto entero, no como cuatro documentos: todo lo sellado esta semana entra al catálogo v1.4 y a la tabla de piso v1.3; las reglas con cifra pasan a bloque de adopción; el informe v1.6 cuenta la semana con la validación ciega del lote 3, los dominios que ganaron estimador y las reglas con evidencia; los reports v2 cuyo carril recibió cifras nuevas salen como v3 con el contraste incorporado; el frente público (README, Pages, one-pager, deck, tablero de carriles) se regenera; y la receta de release queda lista. La sesión decide estructura, orden y profundidad: el criterio es que un lector externo pueda ver qué sabe el programa sobre México hoy y qué no

> ENTORNO: **NUBE** — sellados, vistas, catálogo, reports, docs. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `9d2550b9` (re-deriva al abrir) · una sesión, rama propia; los PR que el volumen pida (catálogo · informe/estado · reports v3 · frente público) · MODELO: **Opus** · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0; mesa 28/sep: «guía explorador», no «niño explorador») · ids con raíz de acto · D-21 aplica.
CONTADOR: cero mediciones; **consume lo sellado** — la adopción de cifras es por merge de mesa (ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR) y este PR es el bloque; la adopción de reglas también es por merge y por bloque (E.2). Versiones anteriores intactas (E.1). **NC solo por D-19.**

## 1 · OBJETIVO
(P1) **Catálogo v1.4 y tabla de piso v1.3.** Entra todo RESULT sellado con fila en la vista desde el catálogo v1.3 (`git log` sobre `data/corrida0/` y vistas desde `65da69fd`): pisos de ENCIG confianza (PISOS-Y-ADENDAS-1), relevo de trámite (RELEVO-TRAMITE-CAJA-1), momentos (CALC-ALTERNOS-LOTE-1; con `holdout_gastado` visible), dominios y reglas (PISOS-DOMINIOS-Y-REGLAS-1), y las suspensiones/acotaciones que C1-SUCESORES-Y-LOTE-3 proponga; cada fila con estado de adopción propuesto por instrumento y con su validación ciega si la tiene. Cifras por comando y test como en v1.3. Derivado: `mapa11_dominios_medidos` recalculado y explicado.
(P2) **Reglas: bloque de adopción.** `canon/reglas-contrastadas-v1_1.tsv`: las CONFIRMA con tier evidenciado ≥ media forman el bloque (formato de ADOPCION-BLOQUE-Y-PINES-1) y, si mesa fusiona, entran a `milpa/tramite.yaml` como reglas vivas con su RESULT; las MATIZA se reescriben en su report con el matiz y la cifra; las ROMPE con la corrección; las SIN-CIFRA quedan PROPUESTA con su instrumento pendiente. Todo en la unidad de la regla, con procedencia (a)/(b)/(c).
(P3) **Informe v1.6, estado v1.19, «Dónde cambió el mexicano» v1.1.** Qué cambió esta semana: dominios con estimador (de 17 a lo que salga), reglas con evidencia, validación ciega (lote 1 + lote 3 asentados: cifras «dentro de tolerancia» vs exactas, rótulo por contexto), legacy relevado, demanda dictaminada, familias 2027 listas; PROSPECTIVA y RETROSPECTIVA en columnas; unidad por cifra. Con módulo de auditoría v2.16 completo.
(P4) **Reports v3 y frente público.** Cada report v2 cuyo carril recibió cifras o contrastes nuevos esta semana sale como v3: la cifra GEN2 citada por RESULT, el contraste de sus reglas, el módulo de auditoría con las preguntas [v2.16], firewall donde toque, procedencia por afirmación; los demás no se tocan. README, `docs/` (Pages), one-pager, deck y el tablero de carriles regenerados por comando; receta de release al número siguiente de la serie (`git ls-remote --tags` decide), sin publicar (mesa).

«Hecho», por comando sobre el commit final con `origin/main` fusionado: catálogo v1.4, tabla v1.3, informe v1.6, estado v1.19 con 0 cifras sin comando (tests) y `diff` vacío en las versiones previas · bloque de reglas con `resultado_id` existente por regla · reports v3 solo para carriles con cifra nueva (lista derivada en la nota) y cada uno pasa el test de procedencia · `mapa11_dominios_medidos` recalculado y citado · frente público regenerado (tests de README/Pages verdes) · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
ADENDA-1 de TRAMITE-FIRMAS-21 (78 renglones: HOLDOUT (b), reservas, R17–R28 sobre reglas y contratos), beee-01/02, FIRMAS-20 A1–A6, adopción por instrumento (§4). Mesa 28/sep: «dame encargos robustos … tratémoslo como guía explorador». Lo que no está firmado y no se hace aquí: publicar el release y el DOI (mesa, R49, mañana), adoptar por fuera del merge.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `9d2550b9` · consumidos hoy: PISOS-Y-ADENDAS-1, RELEVO-TRAMITE-CAJA-1, CACHE-PARQUET-1, C2-EJECUCION-1, C1-LOTE-3, C1-SUCESORES-Y-LOTE-3, CALC-ALTERNOS-LOTE-1, PISOS-DOMINIOS-Y-REGLAS-1, DEMANDA-DICTAMEN-1, REGLAS-Y-RESULT-1, PENDIENTES-3, TABLERO-CARRILES-1, TUBERIA-3, TRAMITE-FIRMAS-21. `status`: adoptados 138 (vista con el canal en cola), validación independiente 215 (490+ filas en el TSV), `mapa11_dominios_medidos` 17 (lee el catálogo: sube solo con v1.4). `reglas-contrastadas-v1_1.tsv`: CONFIRMA 6, MATIZA 7, MATIZA-SIN-CRUCE 8, SIN-CIFRA 141. NC 334, FP 17. `forense/tablero/TABLERO-CARRILES.md` existe.
- [LEÍDO] CIERRE-SEMANAL-1 y -2 (formato, derivador, receta de release; `origin` sin tags al 27/sep). `mapa-dominios-v1_1.tsv` (`report`, `clase`), `crosswalk-carriles-v1_0.tsv` (TABLERO-CARRILES-1).
- [SUPUESTO] Que el derivador de README/informe lee las vistas del canal; si el `[deriva]` en cola no ha publicado al abrir, la sesión cita la vista del commit final y declara la fecha de la vista (como hizo v1.5).

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'CIERRE-SEMANAL-3\|CIERRE-Y-PRODUCTO'` → 0. CIERRE-SEMANAL-1/-2 consumidos (modelo). ADOPCION-BLOQUE-Y-PINES-1 (formato de bloque). C3-1 (reports v2 con índice; **no relanzar reports**, solo v3 donde hay cifra nueva). En vuelo: MEDICION-CARRILES-2 y VALIDACION-Y-2027-1 (caja; lo que sellen después de tu apertura va al cierre siguiente, no a este), el `[deriva]`.

## 5 · PIEZAS
Las decide la sesión. Sugerencia, no orden: P1 → P2 → P3 → P4. Rama prevista: RESULT sellado sin fila en la vista → «sellado en disco, no registrado», NC para el canal, no entra; report cuyo carril no recibió cifra → no se toca.

## 6 · LATITUD — de guía
Estructura del catálogo y del informe, qué cuenta como «cifra nueva» para un carril, cómo se presenta la validación ciega, formato del bloque de reglas, orden de PR: tuyos, declarados en la nota. Puedes proponer cambios de forma al producto (secciones nuevas, columnas) y hacerlos si no tocan lo sellado. PREGUNTA A MESA: ninguna prevista; la adopción es su merge. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato · b) editar versiones previas, sellos, vistas, reports v1 · c) teclear una cifra; adoptar fuera del merge; fundir PROSPECTIVA con RETROSPECTIVA · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Cifras con comando y test» protege **congelar** · «Solo lo sellado y registrado entra; adopción por merge» protege **adoptar** · «Versiones previas y reports v1/v2 intactos» protege **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `canon/{catalogo-del-mexicano-v1_4.*, tabla-de-piso-v1_3.tsv, informe-programa-v1_6.md, estado-programa-v1_19.md, donde-cambio-el-mexicano-v1_1.md, reglas-bloque-adopcion-1.*}`, `milpa/tramite.yaml` (solo el bloque de reglas, por el escritor de relevo), `corpus/reports-v3/` (nuevo; INDICE por productor), README, `docs/`, one-pager, deck, `firmas-pendientes.tsv` (append), nota, L0, cascada. Ajeno: sellos, vistas, specs, `prereg-*`, `validacion-independiente/`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no publica release ni DOI, no toca reports sin cifra nueva, no abre reservas. Sucesores: cierre siguiente; reports v3 restantes cuando MEDICION-CARRILES-2 selle. Módulo de auditoría v2.16 en catálogo, informe y cada report v3. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-CIERRE-Y-PRODUCTO-3-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

Sin filas NC nuevas: el encargo (cabecera) dice «NC solo por D-19» y ninguna fila de abajo es un PARO de la lista cerrada. Cada fila deja rastro en `forense/hallazgos.md` o en su FP.

- **qué:** P2 «si mesa fusiona, entran a `milpa/tramite.yaml` como reglas vivas con su RESULT» · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: el bloque de reglas 1 depende del criterio de CONFIRMA (`FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01`, ABIERTA), y `tools/escribe_relevo_consumo.py` no tiene modo para crear reglas desde `reglas-contrastadas` (hallazgo 28/sep) · **impacto:** 0 reglas vivas nuevas en `milpa/tramite.yaml`; el bloque existe en `canon/reglas-bloque-adopcion-1.*` · **sucesor:** FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01.
- **qué:** P4 «el tablero de carriles regenerado» con la cifra de v1.4 · **por qué:** FUERA-DE-PERÍMETRO: la fuente `F2` del tablero es `canon/crosswalk-carriles-v1_0.tsv`, de GEN2-TABLERO-CARRILES-1, y apuntarla a v1.4 lo reescribe en su sitio; el tablero se regeneró con su fuente vigente (v1.3) · **impacto:** el semáforo del tablero no ve los cuatro dominios nuevos · **sucesor:** SIN-ASIGNAR (hallazgo 28/sep).
- **qué:** «Hecho»: `check.py --baseline` VERDE · **por qué:** NO-VERIFICABLE-AQUÍ: el juez es el CI del push (P-A). En local, `check.py --rapido` 0 FAIL; `test_informe_derivado` (138 comandos), `test_estado_derivado` (57), `test_readme_derivado`, `test_tablero_carriles` y `verifica_sidecars` en verde; la batería unittest de catálogo, reports v3 y frente público dio 1 error que la sesión no llegó a aislar antes de la interrupción del operador · **impacto:** ninguno sobre cifras; el PR no se declara listo hasta que el CI lo juzgue · **sucesor:** CI del PR #1337.
