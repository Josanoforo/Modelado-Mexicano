ENCARGO E9 · ESTIMA-RUTAC — ocho actos sin estimar nada; éste estima

Dirección (maestra-31), 27/ago/2026 · Redactado contra main = 337b894 (clon propio, no espejo). GATED a que PR #389 (E8 · LOS-388) fusione, con ADR renumerado a 217 y los dos conflictos resueltos.

ENTORNO ASIGNADO: UBUNTU. NO lanzar en NUBE — abre microdato de ENVIPE 2025. Sin red, sin API (FP-165), sin descarga. Rótulo: ACTO MAESTRA31-E9 (D-6). Token pelado E9 colisiona con MAESTRA30-E9 · SCORING-V2; se censa, no se reclama.

ORDEN EN LA SECUENCIA DE CIERRE: 1 de 3. Va primero a propósito. La jornada lleva ocho actos y cero estimaciones; poner otro acto de índice delante repetiría el patrón que este encargo existe para romper.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. El clon /home/pc0/Modelado-Mexicano suele estar parado en acto/cal-g3-puntual: crea worktree propio sobre origin/main.

2 · SHA. Confirma contra qué base trabajas. Si main se movió: NO es PARO — refresca, re-deriva y reporta la diferencia antes de editar.

3 · data/raw. Para este acto sí es PARO: es su materia prima. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Excluye el ciclo data/raw/raw, no lo sigas. ⚠️ Este acto NO descarga.

4 · ENTORNO. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado sin_variable; curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/. Los dos valores crudos. NUNCA curl -I. A.2 tercera parte: ls data/raw/ 2>/dev/null | head -1. ⚠️ Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo declara cuántos archivos o filas examinó. Usa command grep y decláralo. Dirección se equivocó hoy por esto: declaró ausente data/inventario-fd-v1_0.tsv con un ls corrido sobre un árbol a medio merge --abort; el archivo existe con 17,094 filas.

5 · ESPEJO. Prohibido derivar cifras del espejo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — CONTESTADA por dirección (clon propio, 337b894, 27/ago/2026) ═══

1 · ESTRUCTURA. Gobernantes: milpa/procedencia.yaml (bloques condicionales_escalares_exposicion_violencia y condicionales_confianza_institucional, más rutas_estimabilidad_coeficiente.detalle) · canon/modelo-decision-v4_0.md (la tabla G1–G6 que asigna el coeficiente) · data/manifiesto.yaml (el payload de ENVIPE 2025). Ninguno se edita en este acto — ver PROHIBIDO.

2 · CONTENIDO — el trabajo NO está hecho, y procedencia.yaml lo dice de sí mismo. Las dos únicas filas RUTA-C del motor, citadas verbatim:

gen: G4 · coef: exposicion_violencia   · ruta: RUTA-C · prioridad: MEDIA
  nota: "candidato BP1_23/ver_oir_callar con limitación estructural declarada,
         procedencia.yaml:396-413 (limite_c2) -- pendiente adjudicación de mesa"
gen: G4 · coef: confianza_institucional · ruta: RUTA-C · prioridad: MEDIA
  nota: "mismo candidato y misma limitación que G4·exposicion_violencia"

Son las dos únicas de las 15 rutas cuyo estado es "pendiente". Las otras 13: 9 SIN-RUTA, 3 RUTA-A con nota "β̂ marginal ya corrido, Encargo W — no re-abre ruta, ver ADR-57(a)", y 1 RUTA-I que apunta a ENNViH/MxFLS, confirmado ausente del corpus por ACTO MAESTRA31-E7. Resultado A.4: NO-ENCONTRADO — ningún artefacto del árbol estima estos dos coeficientes. Universo: árbol completo salvo .git y data/raw, 27/ago/2026.

3 · Y el insumo SÍ está, medido y verificado por un acto anterior. procedencia.yaml declara para exposicion_violencia:

clase:  MEDIDO·PARCIAL(edad,dominio,formalidad,ESTRATO)
fuente: ENVIPE 2025, TPer_Vic2, 91182 filas, universo persona seleccionada 18+,
        sin condicionar a RESUL_H, cero blancos, Sección VII
        núcleo AP7_3_10/11/12/13/14 (AP7_3_09 extorsión reportada aparte)
n_util: 91182 filas, cero blancos en las seis variables.
        Join a TSDem por ID_PER: 91182 de 91182 (100%).
        De esos, 56829 (62.3%) con AP3_8="trabajó" y AP3_10 válido.

El θ está medido. Lo que falta es el β. Este acto no vuelve a medir θ.

4 · COBERTURA RETROACTIVA. El bloque condicionales_escalares_* se selló el 4/ago; rutas_estimabilidad el 24/ago; el reparto vigente el 25/ago. Todo lo que este acto toca es posterior a sus tablas gobernantes. Sin brecha.

⚠️ Si al ejecutar encuentras que estos dos ya están estimados, PARA y repórtalo.

════════════════════════════════════════════════════════════════════

OBJETO

Estimar la asociación entre θ y el desenlace para los dos coeficientes RUTA-C de G4, y establecer con dato si el obstáculo es de datos o de especificación.

Porque hay una hipótesis fuerte, derivada por dirección y que este acto debe confirmar o refutar: el bloqueo no es instrumental. Las dos filas declaran:

escala_asignado:  ESCALA_NO_DERIVABLE
escala_fuente:    canon/modelo-decision-v4_0.md:454-460 (tabla G1-G6, sin forma
                  funcional ni link declarados) y :450 («el signo... la magnitud no»)
escala_derivada:  SUBDETERMINADA (ACTO ESCALAS-COMPLETAS-P1, 25/ago/2026)

Si eso se sostiene, entonces incluso con θ medido, n suficiente y ejes disponibles, el coeficiente no se puede escribir en el motor porque el motor nunca declaró en qué escala vive. Ése sería el hallazgo del acto, más importante que el número.

PASOS

0-bis · A.3. Commitea este encargo íntegro y verbatim en forense/encargos/2026-08-27-MAESTRA31-E9-ESTIMA-RUTAC.md antes de nada. ## CONSUMIDO al cerrar, con el número de PR.

1 · COMMIT-1 — congela la especificación ANTES de abrir un solo archivo de ENVIPE. Es corrida de estimación: aplica la regla de dos commits del Bloque D sin excepción. Contiene:

Variables, citadas del bloque de procedencia.yaml con línea: núcleo AP7_3_10/11/12/13/14; AP7_3_09 fuera del núcleo y reportada aparte, tal como el bloque ya decidió — no la reincorpores.
Universo: persona seleccionada 18+, sin condicionar a RESUL_H, 91,182 filas de TPer_Vic2.
Ponderadores: cuáles, de qué columna, y qué pasa si faltan. Si el bloque no fija ponderador, PARA y reporta — no elijas uno.
Ejes de condicionamiento: edad (18-29 · 30-44 · 45-59 · 60+) × dominio (U/C/R) conjunto, 12 celdas; formalidad (AP3_8/AP3_10 vía join a TSDem) marginal; ESTRATO marginal.
Dicotomizaciones, explícitas, y de dónde salen.
La escala de cada cantidad que vas a producir (A-bis 3), declarada antes de producirla.
El estimando restringido (A-bis 4): el eje de formalidad cubre 56,829 de 91,182 (62.3%). Declara ahora que el marginal contra el que compararás las celdas de formalidad se recalcula restringido a esa misma subpoblación, no contra el poblacional. Un marginal poblacional contra celdas de subpoblación compara dos universos y no valida nada.
B-bis, antes de ver el dato: qué significa que la asociación aparezca con el signo que la tabla G1–G6 declara, qué significa que aparezca invertida, y qué significa que el condicionamiento la invierta respecto del marginal. Los tres tienen que tener fila. Y si el resultado esperado bajo corroboración es interesante, dilo ahora: sería el primer dato mexicano que sostenga la magnitud de un coeficiente que hoy solo tiene signo.
Frase de sello verbatim: «El primer resultado que produzca este procedimiento es el que se reporta.»

2 · COMMIT-2 — los resultados, sin editar el primero. Y las cuatro reglas de A-bis mandan sobre cualquier tentación de redondear la conclusión:

A-bis 1 · Co-observación no es identificación. El β̂ marginal es una asociación. Se rotula como asociación. No se escribe "el coeficiente es X".
A-bis 2 · Condicionado tampoco es correcto. Si el estratificado discrepa del marginal, lo que eso establece es que el marginal no es robusto — nada más. No se declara cuál es "el bueno" sin un argumento de identificación que las reglas de co-observación no dan.
A-bis 3 · Escala declarada, sin comparaciones entre escalas. Prohibido escribir "el medido es X, el asignado era Y, difiere en Z%" contra el valor de la tabla G1–G6: esa tabla declara signo sin forma funcional ni enlace. Es error de categoría, no medición.
A-bis 4 · Universo. Las celdas de formalidad se comparan contra el marginal restringido. Si la discrepancia se atenúa suavemente con la cobertura del eje, es problema de universo; un bug no se atenúa.
Y la contraparte: un punto que satisface un umbral con un IC que no lo despeja no adjudica. Se reporta como propuesta con la reserva escrita.

3 · El veredicto sobre la hipótesis del OBJETO. Con la escala declarada delante, di si el coeficiente se puede o no se puede escribir en milpa/ — y por qué. Si la respuesta es que no, nombra exactamente qué le falta a modelo-decision-v4_0.md para que se pudiera: forma funcional, función de enlace, rango del parámetro, o las tres.

4 · Cierre. forense/notas/2026-08-27-estima-rutac-cierre.md con los conteos A.13 · FP-176 con la RANURA de abajo · ADR (máximo re-derivado por conteo entero contra el árbol ya fusionado; renumera quien fusione segundo) · recifrado §L0 · rótulo en canon/registro-rotulos.tsv y tests/check.py si T25 lo exige · python3 tests/check.py --baseline VERDE (🚫 jamás --freeze) · PR.

RANURA M-RUTAC — precargada, la llena mesa, el ejecutor NO la anticipa

FIRMO M-RUTAC. Con las dos asociaciones estimadas y su escala declarada delante: (a) el coeficiente no se escribe en milpa/ — la escala no es derivable y escribir un número sería meterlo en una escala que la simulación consumiría mal (A-bis 3). El hallazgo entra como asociación reportada y el par sigue RUTA-C; (b) se abre acto sucesor que declare la escala en modelo-decision-v4_0.md (forma funcional + enlace + rango), y solo después se escribe el coeficiente — re-sello mayor del modelo; (c) el estimando resultó no ser el que la ruta suponía y RUTA-C se re-clasifica, con la razón escrita.

Si la RANURA llega VACÍA: se ejecutan los pasos 1-3, el acto cierra con las asociaciones reportadas, FP-176 ABIERTA, y milpa/ intacto. No se fuerza fila.

PERÍMETRO Y CONCURRENCIA

Toca: forense/encargos/2026-08-27-MAESTRA31-E9-ESTIMA-RUTAC.md · forense/notas/2026-08-27-estima-rutac-spec.md (COMMIT-1) · forense/notas/2026-08-27-estima-rutac-cierre.md (COMMIT-2 y cierre) · data/estima-rutac-v1_0.tsv (los estimados, con escala en cabecera) · forense/firmas-pendientes.tsv (solo FP-176) · forense/hallazgos.md · canon/gobernanza-v1_15.md · canon/estado-programa-v1_10.md · canon/registro-rotulos.tsv · tests/check.py (solo _T25_ARCHIVOS_CONOCIDOS).

NO toca: milpa/** — ni una línea, ni para escribir el resultado · canon/modelo-decision-v4_0.md · data/inventario-reactivos-v1_* · data/inventario-fd-v1_0.tsv · data/cobertura-composicion-v1_0.tsv · data/manifiesto.yaml · tools/** · forense/hitoD-preregistro-v2_0.md · forense/prereg-duelo-v2/** · R10.3.

Concurrencia: secuencial. E10 · TECHO-TEXTO y E11 · CIERRE-FASE van después y no arrancan hasta que éste fusione. Nada corre en paralelo con este acto: es el único que abre microdato y el único que estima.

"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

PROHIBIDO

Escribir cualquier valor en milpa/ · comparar el estimado contra el valor de la tabla G1–G6 como si fueran la misma escala · declarar "el verdadero β es X" · reincorporar AP7_3_09 al núcleo · elegir ponderador donde el bloque no lo fija · comparar celdas de formalidad contra el marginal poblacional · adjudicar la RANURA · re-medir θ · descargar, red o API · derivar cifra del espejo · ajustar la especificación tras ver el resultado.

CONTADOR

Dos asociaciones estimadas con microdato propio, con escala declarada, IC y condicionamiento — la primera estimación de la jornada tras ocho actos.

Y si el veredicto del paso 3 es que el coeficiente no se puede escribir porque la escala no es derivable, ése es el contador y es el resultado más valioso del acto: significa que el techo del programa no es de datos, y eso cambia qué hay que arreglar.

## CONSUMIDO

Ejecutado por ACTO MAESTRA31-E9 · ESTIMA-RUTAC, 27/ago/2026, PR #390. El acto pivotó de "estimar dos coeficientes RUTA-C" a hallazgo: las dos premisas de la VERIFICACIÓN DE EXISTENCIA de arriba eran falsas. El β̂ ya estaba medido desde el 4/ago/2026 (MESA-E1, `forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md`) y el campo `escala_derivada` de las dos filas RUTA-C, citado arriba solo por su fragmento truncado "SUBDETERMINADA (...)", ya declaraba ELEGIDA-CIEGA (proporción ponderada [0,1], enlace identidad) desde el 25/ago/2026 (Paso 2 de ESCALAS-COMPLETAS, `forense/escalas-eleccion-ciega-v1_0.md §4`) — dos días antes de que se redactara este encargo. Por decisión de dirección, autorizada explícitamente, no se corrió COMMIT-2: una tercera estimación sobre el mismo par no añadiría nada al 4/ago. Corrección aplicada, acotada a `ruta:`/`nota:` de las dos filas G4 en `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.detalle` (RUTA-C → RUTA-A). FP-176 nueva, ABIERTA: si escribir el β̂ ya medido en la escala ya declarada requiere adjudicación de mesa aparte, sin decidirlo. ADR-218. Detalle completo: `forense/notas/2026-08-27-estima-rutac-cierre.md`.
