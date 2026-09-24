# ENCARGO · ACTO GEN2-CORPUS-COMPLETO-1 · Todo el microdato público que el programa puede usar entra al corpus de una vez: INEGI completo (hogares, establecimientos, censos), INSP, CONEVAL, Banxico/CNBV, Latinobarómetro, LAPOP, WVS — 2.5 TB disponibles, cada ola nueva nace reservada, ninguna se abre

> ENTORNO: **CAJA** — `/adquiere`, corpus compartido, manifiesto. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `474a126e` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-corpus-completo-1` (o la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta; no abre microdato (bajar y hashear no es abrir, E.6). Mueve el manifiesto (payloads VERIFICADOS con sha) y la columna `existencia_documento`/`datos_id_estado` del mapa por derivador. Objetivo numérico: las 768 afirmaciones MEDIBLE-CON-ADQUISICIÓN del mapa dejan de tener instrumento ausente.

## 1 · OBJETIVO
U5 (`acto/gen2-astra5-u5-adquisicion-1`, en vuelo: 705 ENSANUT, 26 ENCOVID, 16 ENCODAT, ENBIARE, Latinobarómetro…) sigue la hoja del mapa. Este acto va más allá de la hoja: **el catálogo entero de microdatos públicos** relevantes al comportamiento reportado, para que ninguna afirmación futura quede en «medible con adquisición» por falta de archivo. (P1) Inventario por comando del catálogo INEGI de microdatos (programas de hogares y establecimientos, todas las olas publicadas: ENOE trimestral completa, ENIGH, ENSU, ENVIPE, ENCIG, ENDIREH, ENADID, ENUT, ENCUCI, ENBIARE, ENASIC, ENVE, ENAPROCE, ENAFIN, ENDUTIH, MOCIBA, ECOPRED, ENADIS, ENSAFI, ENFIH, ENESS, ENAPE, ENIF, ENCO, MOTRAL, ENCEVI, ENCUR, ENTI, censos y conteos de población con muestra, censos económicos con microdato), más INSP (ENSANUT todas), CONEVAL (pobreza multidimensional por año), Banxico/CNBV (series y encuestas con microdato), Latinobarómetro (todas las olas), LAPOP México (todas), WVS/EVS México (olas 1–7), CEEY EMOVI (si exige solicitud: receta y NC), Pew (Religion in Latin America). Tabla `forense/analisis/corpus-completo/catalogo-v1_0.tsv`: programa · ola · URL · tamaño · licencia · ¿ya en manifiesto? · prioridad = número de afirmaciones del mapa que lo citan. (P2) Escribir el registro de la cola (nunca la vista), regenerar, y `/adquiere` en tandas por prioridad hasta agotar el catálogo, con sha, `estado: VERIFICADO`, y **la ola más reciente de cada programa con historia en corpus nace RESERVADA** (E.6); las históricas abiertas. (P3) Verificación al cerrar: cada payload en el corpus compartido coincide con el sha del manifiesto (PR #77); mapa regenerado por derivador. (P4) Tabla final: programas × olas adquiridas / no obtenidas (con `NO OBTENIDO POR ESTE AGENTE EN N INTENTOS` + receta) / con licencia que impide copia (constancia externa).
«Hecho»: catálogo con ≥ 25 programas y todas sus olas listadas por comando · manifiesto con N payloads nuevos = adquiridos (derivado, citado; cero tecleado) · `grep -c 'estado_reserva: RESERVADA' data/manifiesto.yaml` = número de programas con ola nueva (uno por programa) · mapa regenerado: `MEDIBLE-CON-ADQUISICIÓN` con instrumento en corpus → columna de existencia actualizada por derivador · verificación PR #77 pegada · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas, verbatim
**Mesa, 24/sep (chat):** «Que el volumen de descarga no sea un stopper, tengo 2.5 teras de espacio.» **F-ASTRA-5-2** (orden: ENSANUT+ENCODAT, ENBIARE primero — ya lo lleva U5; este acto sigue por prioridad del mapa). **F-ASTRA-5-3** (la reserva es de la ola nueva; el histórico se abre). **E.6** (ola nueva nace RESERVADA; tabulados de reservada no se leen).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` manifiesto a `474a126e`: 0 ensanut/encodat/emovi/censo, 2 enbiare, 3 latinobarometro (U5 los trae en rama: 15 194 líneas nuevas de manifiesto). Mapa: 768 MEDIBLE-CON-ADQUISICIÓN; el campo `instrumento` es texto libre (INEGI 22, ENSU 8, ENSANUT 7, CENSO 7, ENCODAT 7, PEW 7, OECD 7, CEEY 9, INE 8, WORLD 7…): P1 lo normaliza. `[LEÍDO]` `/adquiere` lee solo `data/cola-adquisicion-v1_0.tsv` regenerada desde el registro (`tools/vista_cola_adquisicion.py`); `tools/dominios/hoja_a_cola.py` (U5, en rama) normaliza `instrumento_ola` con reglas en `hoja_a_cola_reglas.tsv`: **se reutiliza, no se duplica** (fusiona U5 antes o toma su script de la rama con cita). `[SUPUESTO]` que INEGI expone microdatos por URL estable por programa/ola (sí para hogares; verificar en establecimientos y censos).

## 4 · YA HECHO / YA DECIDIDO
`git ls-remote --heads origin | grep -i 'corpus\|adq'` → U5 (se coordina: mismo manifiesto; quien fusiona segundo rebasa; U5 primero). `ls data/raw | wc -l` → reporta.

## 5 · PIEZAS
P1 catálogo por comando → P2 registro + `/adquiere` por tandas (prioridad = afirmaciones del mapa; ENOE completa y ENSU completas son las series largas: van temprano) → P3 verificación PR #77 y mapa regenerado → P4 tabla final y recetas.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja; lo no alcanzado va a NO-CORRIDO. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir microdato o leer tabulados de una ola que nace RESERVADA · b) editar la vista de la cola o el mapa a mano; reescribir un sha · c) no aplica · d) no aplica · e) NUBE.

## 8 · COMPUERTAS
«Registro → vista; mapa → derivador» protege: **congelar**. «Ola nueva RESERVADA al entrar» protege: **abrir dato**. «Sha verificado en el corpus al cerrar» protege: **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/analisis/corpus-completo/`, `data/curacion-registro/cola-adquisicion-registro.tsv`, `data/cola-adquisicion-v1_0.tsv` (regenerada), `data/manifiesto.yaml` (por `/adquiere`), corpus compartido, `canon/mapa-dominios-v1_0.tsv` (por derivador), TSV de gobierno, nota, L0, cascada. Ajeno: CALC, `milpa/`, reports. En CAJA: U5 (mismo manifiesto: U5 fusiona primero), PISOS-GEN2-2 y SALUD-Y-BIENESTAR (leen olas ya abiertas; no escriben manifiesto).

## 10 · LO QUE NO HACE · SUCESORES
No mide, no abre, no cambia dictámenes. Sucesor: `-2` para lo NO OBTENIDO con receta; las unidades de medición por dominio sobre lo adquirido.
