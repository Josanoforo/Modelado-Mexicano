# ENCARGO · ACTO GEN2-MAPA-DOMINIOS-V1-1-1 · Con 131 programas nuevos en el corpus, el mapa se re-dictamina afirmación por afirmación: lo que era «medible con adquisición» pasa a «medible en corpus» con programa, ola y pregunta concretos, y sale la cola de medición por dominio que las unidades siguientes ejecutan

> ENTORNO: **NUBE** — mapa, manifiesto, cuestionarios y FD (documentos, no microdato). Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `40058c09` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie, con esas palabras.
CONTADOR: cero mediciones; mueve las columnas del mapa por su derivador (`censa_afirmaciones.py` o el que U0 dejó): `MEDIBLE-EN-CORPUS` sube desde 208; `MEDIBLE-CON-ADQUISICIÓN` baja desde 768; el conteo lo da el derivador. `canon/mapa-dominios-v1_0.tsv` intacto (sucesor v1_1).

## 1 · OBJETIVO
CORPUS-COMPLETO-1 (#1145) dejó 148 programas catalogados y 131 con olas adquiridas (`forense/analisis/corpus-completo/tabla-final-v1_0.tsv`); el mapa v1.0 (#1079) dictaminó con el manifiesto de antes y con `instrumento` en texto libre (INEGI 22, ENCUESTA 6, WORLD 7…). (P1) Normalizar `instrumento` de cada afirmación MEDIBLE-CON-ADQUISICIÓN a `programa_id` del catálogo de CORPUS-COMPLETO (tabla de equivalencias declarada; lo que no case, NO-ENCONTRADO con el texto). (P2) Re-dictamen por afirmación: si el programa y una ola con la pregunta están en corpus (verificado **por texto de pregunta** en el cuestionario/FD del payload, A.15; no por nombre de programa) → `MEDIBLE-EN-CORPUS` con `programa_id`, `ola`, `variable`, `texto_pregunta`, `unidad`; si el programa está pero la pregunta no → `NO-CONSTRUIBLE-EN-CORPUS` con la pregunta buscada y secciones recorridas; si el programa no se obtuvo → sigue `MEDIBLE-CON-ADQUISICIÓN` con la receta de CORPUS-COMPLETO. Los 420 NO-MEDIBLE-POR-DISEÑO no se revisan salvo que un programa nuevo los cubra (se dice si ocurre). (P3) **Cola de medición por dominio**: `forense/analisis/dominios/cola-medicion-v1_0.tsv` (dominio · programa · ola · N afirmaciones · reports que sostiene · prioridad = afirmaciones FUERTE/MEDIA cubiertas), que es el insumo de las unidades siguientes. (P4) Cobertura de 31 dominios recalculada (misma tabla que el catálogo v1.1 consume).
«Hecho»: `canon/mapa-dominios-v1_1.tsv` con 0 filas sin dictamen y `--verifica` byte a byte · equivalencias `instrumento → programa_id` con 0 NO-ENCONTRADO sin texto · cola de medición con una fila por (dominio, programa) · cobertura recalculada · v1.0 intacto · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
F-ASTRA-5-2/3, aprobación en bloque 23/sep (ASTRA-5 U0 y su vocabulario cerrado), C4 de FIRMAS-16 (boletín ENOE 2026T1 consumido: ninguna afirmación de informalidad puede usarlo para preparación ciega; el mapa lo rotula).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` mapa v1.0: 1 396 afirmaciones (208/768/420); `instrumento` texto libre. Manifiesto: ids con prefijos heterogéneos (`inegi_`, `descargamasiva_`, `encuesta_`…): **la equivalencia es por `programa_id` del catálogo de CORPUS-COMPLETO, no por prefijo**. Tabla final: 131 adquiridos, 19 reservados, 8 NO OBTENIDO/NO-APLICA. `[SUPUESTO]` que los cuestionarios y FD vienen dentro de los payloads (INEGI los incluye): si uno falta, se baja desde nube (permitido: no es microdato).

## 4 · YA HECHO / YA DECIDIDO
`ls canon | grep -c mapa-dominios-v1_1` → 0. `ls forense/analisis/dominios | grep -c cola-medicion` → 0.

## 5 · PIEZAS
P1 equivalencias → P2 re-dictamen (lotes por dominio, como U0) → P3 cola → P4 cobertura.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir microdato (este acto lee cuestionarios, no bases) · b) editar v1.0 a mano · c) no aplica · d) cambiar el vocabulario de dictamen · e) CAJA.

## 8 · COMPUERTAS
«Dictamen MEDIBLE-EN-CORPUS solo con texto de pregunta verificado» protege: **congelar** (A.15). «Mapa por derivador» protege: **congelar** (D-23).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `canon/mapa-dominios-v1_1.tsv`, `forense/analisis/dominios/` (equivalencias, cola, cobertura), su derivador (extensión declarada), tests, nota, L0, cascada. Ajeno: v1.0, manifiesto, CALC. En vuelo: las unidades de medición de esta tanda (leen v1.0 y su propio texto de pregunta; cuando v1.1 fusione, lo citan).

## 10 · LO QUE NO HACE · SUCESORES
No mide, no adquiere (lo que falte: `ASTRA5-U5-ADQUISICION-2`). Sucesores: las unidades por dominio en el orden de la cola.
