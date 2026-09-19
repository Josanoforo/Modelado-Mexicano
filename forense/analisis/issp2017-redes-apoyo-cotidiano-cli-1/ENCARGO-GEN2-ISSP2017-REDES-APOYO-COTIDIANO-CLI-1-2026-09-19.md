# GEN2-ISSP2017-REDES-APOYO-COTIDIANO-CLI-1

## Mandato

Mide a quién acudirían primero las personas entrevistadas en México ante cinco necesidades cotidianas y cómo se combina la ausencia declarada de una persona a quien recurrir. Entrega medición descriptiva GEN2, CALC sellado, tablas y PR. Permite distinguir apoyo familiar, amistades y otras relaciones donde el cuestionario sí las separa.

CAJA local, Josanoforo/Modelado-Mexicano. Rama `codex/gen2-issp2017-redes-apoyo-cotidiano-cli-1`; CALC propuesto `CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001`, comprobando unicidad y equivalentes por contenido antes de congelar. Worktree propio desde origin/main actualizado; informa ruta, rama, HEAD y estado, lee AGENTS.md. Al pegar este encargo se autoriza commit/push/PR; no merge/adopción.

Base revisada: `8e455bd6a3870566d6776fef19834c4da16d2fa9`, 19/sep/2026. CALC-ISSP2017-APOYO-MONETARIO-0001 ya mide Q8a/v26, donde familiares y amigos son una categoría combinada. No repetirlo. La apertura de agosto documenta Q7a-e/v21-v25 para necesidades de hogar/jardín, enfermedad, ánimo deprimido, consejo familiar y ocasión social. Son cinco situaciones distintas, no una escala psicológica validada.

## Fuente, revisión y congelamiento

Lee `data/apertura-issp-variables-2026-08-13.tsv`, secciones pertinentes de su nota, demanda vigente y spec/medidor/resultados del CALC monetario. Busca Q7, v21-v25 y redes de apoyo en CALC, análisis e historia pertinente y ramas activas. Si hay equivalentes completos, referéncialos; completa solo lo faltante. La apertura histórica pudo haber mostrado distribuciones: declara exposición; no presentar esto como diseño ciego.

Fuente esperada: `za6980_v2_0_0_dta`, ISSP 2017 ZA6980 v2.0.0, DOI 10.4232/1.13322. Verifica hash/miembro, cuestionario mexicano ZA6980_q_mx, backgroundvar mexicano y Variable Report integrado disponible que ya se usó en el CALC monetario. Acredita el mapa Q7a-e↔v21-v25 y texto/códigos con páginas antes de leer respuestas. No inferir columnas por posición. No abrir filas de otros países.

Identidad México por `c_alphan=MX` y `country=484`, más identidad del estudio/versión/DOI del precedente. Verifica llave CASEID y unidad persona adulta; edad desconocida no se excluye automáticamente si el marco documentado ya es adulto. Usa WEIGHT conforme a documentación, que en el precedente mexicano es 1/no weighting. No inventes ajuste poblacional.

Congela en COMMIT-1 spec humana/YAML, hashes de código, medidor, pruebas sintéticas, categorías/denominadores, RESULT y reglas de no estimación antes de abrir respuestas. COMMIT-2 publica ejecución/resultados/sello. El primer resultado es reportado; correcciones materiales preservan intento y siguen sucesión vigente.

## Productos en una sola corrida

P1. Para cada situación de Q7, distribución de las siete respuestas sustantivas, cobertura válida y faltantes; total y por SEX=1/2. Verificar catálogo: familiar cercano, familiar más lejano, amigo cercano, vecino, compañero de trabajo, alguien más, ninguno. `No puedo elegir` y no respuesta son estados distintos de ninguno. Conservar categorías con cero observaciones. Sexo desconocido permanece en el total y como residuo explícito de reconstrucción.

P2. Para cada ítem, agregado explícito de familiar cercano+lejano y contraste descriptivo mujeres menos hombres, conservando además la distribución nativa completa. Describe preferencia declarada de primera persona a quien acudir: no mide apoyo recibido, dinero, calidad del vínculo ni obligación familiar. No llamar familismo a todo apoyo ni sumar amigos a familia en Q7.

P3. Sobre quienes tengan las cinco respuestas válidas, distribución 0..5 del número de situaciones donde responden ninguno, y proporciones con ninguna/en alguna/en todas las situaciones sin destinatario declarado. Publica matriz de coocurrencia de ninguno para las diez parejas de situaciones sobre ese MISMO universo completo, más su cobertura respecto de todos los entrevistados. Los ceros indican respuestas válidas distintas de ninguno; desconocidos no entran como cero. El conteo es descriptivo de amplitud de situaciones, no índice validado de soledad, aislamiento, depresión o capital social.

Publica n, masa, numerador/denominador y unidad en cada fila. Las distribuciones por ítem usan su denominador válido específico; P3 usa casos completos. No comparar puntos entre esos universos sin indicar selección. No imputar no respuesta ni ajustar pesos para compensarla.

## Precisión y comprobaciones

El precedente documenta que no se acreditaron UPM/estratos ejecutables para México. Reutiliza ese límite salvo documentación nueva concreta: puntos y contrastes con `EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO`. No bootstrap iid, tamaño efectivo inventado, prueba de significación ni afirmación de representatividad nacional que exceda el marco. La falta de IC no impide publicar descripción correctamente rotulada.

Controles materiales: identidad y selección México, llave única, catálogo cerrado, peso válido, cada partición suma uno en su universo, total reconstruido por sexo más no clasificado, distribución del conteo exhaustiva, matriz simétrica y diagonales compatibles con marginales sobre casos completos. Recalcula puntos/denominadores representativos mediante implementación separada sin importar el medidor. Pruebas sintéticas para todos-desconocidos, cero válido, no puedo elegir y sexo faltante. No suite general por inercia.

La lectura responde en qué situaciones la familia o amistad ocupa el primer lugar y si no tener destinatario declarado se concentra en una situación o coocurre en varias. No comparar 2012 contra 2017 como panel, no calcular coeficientes del generador y no enlazar respuestas de personas entre encuestas. No consumir F6, M/L, HOLDOUT ni piloto 3.

## Perímetro, publicación y cierre

Escritura: nuevo CALC y sucesores propios, `forense/prereg-caja/ISSP2017-REDES-APOYO-COTIDIANO-*`, `forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1/`, test propio, encargo verbatim y cierre; asientos de replay propios, derivados solo mediante comandos vigentes. No escribir milpa, motor, canon, decisiones, NC globales, corrida0.py, tests/check.py, workflows ni CALC monetario.

Preflight, ejecución, sello, replay dirigido y registro en el mismo acto por interfaces existentes. No usar --lote para aceptar evidencia ajena. Si registro bloquea por otra corrida, entrega el CALC y PR con publicación pendiente y evidencia, sin ampliar perímetro ni afirmar consumo activo. Contador/adopción PENDIENTE-DE-MESA. Claude recibe e integra; mesa adjudica. Vistas compartidas se regeneran al sincronizar, sin edición manual ni reejecución caprichosa del sello.

Cierre: tablas, RESULT→significado/universo, ejecución/sello/replay, hashes, validaciones y lectura sustantiva; CONSUMIDO y NO-CORRIDO / RESERVAS; qué aporta a la necesidad familismo_apoyo y qué no mide; URL de PR y SHA. Auditoría alrededor del 20% salvo riesgo material. No fusionar.
