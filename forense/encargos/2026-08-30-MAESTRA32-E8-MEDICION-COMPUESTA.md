Enmienda in situ 30/ago/2026 (dirección): compuerta "E3 fusionado" LEVANTADA — era de secuencia, no de datos; carril CAJA reordenado E8 → E3; input verbatim en la nota de cierre §0.

---

ENCARGO · ACTO MAESTRA32-E8 · MEDICION-COMPUESTA

SHA de redacción: 2799132 (main, merge PR #397 / ADR-225) · Redactado: 30/ago/2026 (v2, refresca el borrador del mismo día contra 2c0d4c8, que no se lanzó y queda sin efecto), dirección maestra-32 · Instrucciones vigentes: v2.11 · Estado: GATED a que MAESTRA32-E3 · EXTRACTOR-DTA (rama a) fusione — mismo carril de caja, serie estricta dentro del carril. No se lanza hasta ver el merge de E3 en main (lección de ADR-224: un acto lanzado antes de su compuerta consume rótulo y jornada).

ENTORNO ASIGNADO: UBUNTU (caja con corpus). NO se lanza en NUBE: abre microdato de ENCUCI 2020 y ENVIPE 2025. A.2 tercera parte es PARO-relevante: sin data/raw enlazada al corpus compartido, PARA.

CARRILES EN PARALELO (declarado): carril CAJA = E3 → E8 (este); carril NUBE = E11 · COBERTURA-15 (E6 ya fusionó, ADR-223; E7 retirado sin lanzar, ADR-225). Archivos que ambos carriles tocan: canon/gobernanza-v1_15.md, canon/estado-programa-v1_10.md, canon/registro-rotulos.tsv, forense/firmas-pendientes.tsv, tests/check.py (T25). Regla: renumera quien fusiona segundo, re-derivando ADR y FP contra el árbol ya fusionado. Ningún otro archivo se comparte entre carriles.

FIRMA DE MESA INTEGRADA — verbatim del proceso de decisión, 30/ago/2026

M-AGREGA, segunda vuelta → a′ (compuesto re-estimado en caja, sin valor interino). Mesa dictó para T4: "benchmark web". Dirección corrió el benchmark (fuentes en forense/notas/2026-08-30-propaga-firmas-cierre.md y en la nota de cierre de este acto): la vía estándar es formar el compuesto (media/suma de ítems, o factor scores) sobre el microdato y estimar un β̂; el ítem único post-hoc queda desaconsejado (pesos específicos de la muestra). Con la caja de vuelta, el valor interino (b′) deja de tener razón de ser. Mesa, 30/ago: "Las decisiones que tomamos intégralas ya como firmadas en los encargos." Se integra como FIRMADA: M-AGREGA = a′ — resuelve el "hasta firma posterior que adjudique cómo agregar" de ADR-220. Si mesa quisiera otra cosa, lo dice antes de lanzar; una vez lanzado, rige esto.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

A.2, tercera parte (PARO-relevante): ls data/raw/ 2>/dev/null | head -1. En la caja: command grep siempre; negativos con conteo de archivos (A.13); campos YAML íntegros con yaml.safe_load. A.1: toda verificación de hash de los dos payloads que este acto abre, una invocación por --id, salida cruda pegada; AUSENTE · raíz-no-configurada · hash-discordante no se colapsan.

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (maestra-32, 30/ago/2026, contra 2c0d4c8) ═══

1 · ESTRUCTURA. Dominio 4 (producir estimación) de data/INFRAESTRUCTURA-v1_0.md. Tablas gobernantes: milpa/procedencia.yaml sección coeficientes_generador_medidos (la de origen, 4/ago) y sección coeficientes_generador_sellados (la que consume matriz.py, ADR-220); tests/test_matriz_sellados.py.

2 · CONTENIDO. ¿Existe ya un β̂ compuesto para alguno de los dos pares? NO-ENCONTRADO, universo: las 6 entradas de la sección A leídas íntegras hoy con yaml.safe_load — G1_radio_confianza es "tres ítems por separado, no índice" (campo nota, verbatim) y G4_confianza_institucional_justicia es "por institución" (7 ítems; campo marca_c2: "no se combinan ni se promedian" — dicho de las DOS entradas G4 entre sí, no de los ítems dentro de la entrada); las 2 entradas de coeficientes_generador_sellados para estos pares traen valor_ejecutable ausente y rótulo SELLADO-ESCALA·SIN-AGREGACION (verificado hoy). ¿Existe script reutilizable? NO-ENCONTRADO: command grep -rl "AP5_1_1" tools/ → 0 sobre 77 archivos; "AP5_4_01" → 0 sobre 77. La receta del 4/ago vive en prosa: forense/notas/2026-08-04-w-coeficientes-generador-paso1.md §1.1/§3.1 y 2026-08-04-x-condicionamiento-y-forma.md §4.1 (citadas en los campos fuente/eje_condicionante de A).

3 · COBERTURA RETROACTIVA. La sección sellados nació el 28/ago (ADR-220), 24 días después de las mediciones del 4/ago: su vacío en estos dos pares no dice que no se haya intentado un compuesto — dice que el 4/ago eligió ítems separados por diseño. Este acto no contradice ese diseño: lo complementa con la operacionalización estándar, declarada antes de abrir el dato.

═══════════════════════════════════════════════════════════════════

0-bis · A.3

Primer commit: este encargo verbatim en forense/encargos/2026-08-30-MAESTRA32-E8-MEDICION-COMPUESTA.md. Al cerrar, ## CONSUMIDO con el PR.

Premisas, con procedencia (todas leídas del árbol hoy, no de memoria)
Par G1.radio_confianza. ENCUCI 2020, SEC_4_5 (21,519 filas). θ: AP5_1_1/2/3 (confianza en 0-10; el 4/ago se dicotomizó ≥6). Desenlace: tramite.mordida.discrecional = AP5_17 o AP5_18 = '1'. Universo: con contacto AP5_16_1..10 (13,435 el 4/ago — re-deriva). Marginales por ítem: −0.0102 / −0.0113 / −0.0269, solo el tercero excluye 0. El marginal no sobrevive condicionar: 33 de 39 celdas invierten a positivo (Encargo X, recontado ADR-61). marca_c3: NO usar para cooperacion.confianza.puente_personal.
Par G4.confianza_institucional[justicia]. ENVIPE 2025, TPer_Vic1 unida por ID_PER al módulo con BP1_23 (razón miedo/desconfianza para no denunciar). θ: 7 ítems AP5_4_01/02/03/05/06/07/11 dicotomizados confía{1,2}/no{3,4}. Universo: disparadores AP7_3_05-15 no denunciantes (13,023 el 4/ago — re-deriva), intersectado por ítem con "identifica la institución" (no blanco, no 9) — los universos difieren por ítem. Marginales por ítem: todos negativos, todos significativos; 6 de 49 celdas condicionadas invierten. marca_c2: comparte desenlace y universo con G4.exposicion_violencia — no se combinan entre entradas.
Estado ejecutable: ADR-220 dejó ambos pares SELLADO-ESCALA·SIN-AGREGACION; hoy la sección coeficientes_generador_sellados tiene 6 entradas, 4 con valor_ejecutable (ADR-220 + la entrada CAL-G3 de ADR-225), verificado con yaml.safe_load contra 2799132; el enlace identidad sellado hace que la escala de salida sea la de la θ (proporción [0,1]).
ADR-57(a) gobierna la clase: todo β̂ marginal es ASOCIACIÓN, no coeficiente identificado. Un compuesto no cura la confusión; cambia la operacionalización de θ. Entra con la misma reserva que E1 escribió para G1.confianza_institucional.

Verifica estas premisas contra el árbol antes de ejecutar (v2.1). Si alguna no se sostiene, PARA y repórtalo.

Objeto

Estimar, para cada par, un β̂ con θ compuesta en [0,1], con IC95, con su lectura condicionada, y escribirlo en coeficientes_generador_sellados como valor_ejecutable bajo el rótulo de asociación. Dos commits.

COMMIT-1 — especificación congelada ANTES de abrir un solo archivo de datos

forense/notas/2026-08-30-compuesta-spec.md, un commit, con:

(a) Fuentes y universos, re-derivados de las notas del 4/ago y de data/manifiesto.yaml (ids de payload y rutas resueltas por código, no tecleadas): variables, filtros de universo, ponderador (el mismo que usó el 4/ago, citado archivo:línea; si la nota no lo nombra, PARO-reporta antes de elegir uno).
(b) Definición del compuesto, primaria y secundaria, por par. G1: primaria = media de AP5_1_1/2/3 en 0-10, dividida entre 10 → [0,1] (usa toda la información; es el "sum score" de la literatura); secundaria = proporción de los 3 ítems ≥6 (comparable ítem a ítem con el 4/ago). G4: primaria = proporción de instituciones identificadas en las que confía, entre quienes identifican ≥4 de 7 (umbral declarado aquí, no ajustable); secundaria = caso completo (7 de 7 identificadas). La primaria es la candidata a valor_ejecutable; la secundaria es lectura de robustez.
(c) Estimador. Pendiente del modelo lineal de probabilidad ponderado del desenlace sobre la θ compuesta: unidades = cambio en la proporción del desenlace por unidad completa de θ (0→1), las mismas unidades que "diferencia de proporciones (θ=1 − θ=0)" del 4/ago — sin cambio de escala. IC95: el mismo método que la nota del 4/ago para comparabilidad (cítalo); si la nota no lo fija con claridad, percentil bootstrap B=10,000, seed 42 (la convención que mesa fijó vía benchmark web para FP-168), declarado.
(d) Consistencia interna. α de Cronbach sobre los ítems del compuesto (G1 en 0-10; G4 dicotómicos, KR-20 equivalente), reportado. Regla pre-registrada: α < 0.50 ⇒ el compuesto NO se escribe al ejecutable; se reporta como hallazgo de dimensionalidad. α ≥ 0.50 ⇒ se escribe.
(e) Condicionamiento, mismo patrón que el 4/ago, un eje a la vez, celdas con n≥30: G1 → formalidad, edad, ingreso; G4 → edad, dominio. Reporta signo y significancia por celda. Diagnóstico, no compuerta: no gatea la escritura, alimenta la reserva:.
(f) B-bis, antes de ver el dato: IC que incluye 0 ⇒ se escribe igual, con sufijo de rótulo ·NO-DISTINGUIBLE-DE-CERO y línea explícita en el ADR (mesa puede vetar al recibir, FP nueva). Signo discordante con los ítems individuales ⇒ hallazgo, se escribe igual con la discordancia en reserva:. Inversión bajo condicionamiento (esperada en G1) ⇒ va a reserva: verbatim, como en E1.
Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta." Un tercer commit puede decir que la spec estaba mal; nunca se edita hacia atrás.
COMMIT-2 — corrida única

tools/medicion_compuesta.py (nuevo; una corrida; salida cruda pegada en la nota de cierre) + forense/notas/2026-08-30-compuesta-cierre.md con: n por universo (re-derivado), α, β̂ primaria y secundaria con IC, tabla de celdas condicionadas, y los veredictos B-bis. Escritura al ejecutable por script (yaml.safe_load de entrada y de verificación de salida, precedente ADR-220): en las 2 entradas existentes de coeficientes_generador_sellados se añaden (no se reemplaza nada) valor_ejecutable, ic, definicion_compuesto, alpha, rotulo: ASOCIACION-MEDIDA·COMPUESTO·MARGINAL[·NO-DISTINGUIBLE-DE-CERO], reserva: (verbatim: inversión 33/39 para G1; 6/49 para G4; ADR-57(a)), fuente: (esta nota). El vector por ítem y el rótulo previo quedan intactos como historia (A.10). tests/test_matriz_sellados.py: particiones re-derivadas contra el árbol — hoy 4 override · 2 sin-agregación · 9 fallback → tras este acto 6 · 0 · 9 (deriva del test, no heredes; si otro merge movió la base, reporta la cifra real). python3 tests/check.py --baseline → VERDE obligatorio; FAIL nuevo = PARO-reporta.

Falsador del acto

Si (a) no puede reconstruir el universo del 4/ago con diferencia >2% en n, se reporta la diferencia y se sigue con el universo re-derivado — la discrepancia es hallazgo, no motivo de ajuste hacia el número viejo (A-bis 4: mismo universo declarado, no heredado).

PERÍMETRO Y CONCURRENCIA

Archivos: forense/encargos/2026-08-30-MAESTRA32-E8-MEDICION-COMPUESTA.md · forense/notas/2026-08-30-compuesta-spec.md · forense/notas/2026-08-30-compuesta-cierre.md · tools/medicion_compuesta.py (nuevo) · milpa/procedencia.yaml (solo las 2 entradas de coeficientes_generador_sellados, solo campos añadidos) · tests/test_matriz_sellados.py · forense/firmas-pendientes.tsv (fila nueva + FP-179 entradas (1) y (4) marcadas: E3 lanzado, compuesta ejecutada) · cascada (gobernanza, estado-programa, registro-rotulos, tests/check.py T25). No toca la sección A, ningún ASIGNADO, matriz.py, modelo-decision, ni nada del carril NUBE. Concurrencia: carril NUBE (E11) corre en paralelo — ver cabecera. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

FP pre-asignadas

Rango candidato FP-185–FP-186 (máximo hoy FP-182; E11 toma FP-183–FP-184; E3 toma el siguiente libre — re-deriva el máximo real al escribir, y si está tomado, sigue al siguiente libre y decláralo). Uso: "mesa recibe los 2 compuestos: β̂, α, veredictos B-bis".

ADR y cascada

Candidato re-derivado con el comando de la casa contra el árbol fusionado (deriva, no heredes). El ADR trae: la firma M-AGREGA = a′ con su cadena de decisión verbatim, la spec congelada citada, los resultados con escala declarada (A-bis 3), las reservas, y el recifrado L0 "ejecutables 3→N" derivado del test. registro-rotulos: MAESTRA32-E8 censado (token pelado E8 colisiona con MAESTRA31-E8; se censa, no se reclama).

CONTADOR

Coeficientes ejecutables con base medida: 4 → 6 (o 4→5 / 4→4 si α falla en uno o dos pares — cifra derivada del test, declarada con la razón).

Lo que este acto NO hace

No re-mide los ítems individuales del 4/ago. No combina las dos entradas G4 entre sí (marca_c2). No usa el par G1 para puente_personal (marca_c3). No toca G3.horizonte_temporal (GATE·ID-X). No descarga nada. No decide si el motor debe consumir compuestos en lugar de ítems para siempre — eso es de modelo-decision, y queda como candidato de OLA 5.

Sucesores declarados, no lanzados

Encargo medidor de FP-172 (cola diferida, entrada 3 de FP-179) — dirección lo redacta con la lista derivada del tsv, tras este merge.
