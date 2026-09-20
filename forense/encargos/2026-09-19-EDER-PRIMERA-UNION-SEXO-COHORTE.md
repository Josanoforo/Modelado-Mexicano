# Encargo 3 · EDER 2017: primera unión por sexo y cohorte
Rama propuesta: codex/gen2-eder2017-primera-union-sexo-cohorte-cli-1.
CALC propuesto: CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001.

## Pregunta y avance
¿Cómo varía la composición del tipo de primera unión por sexo dentro de cohortes y cuánto cambia la diferencia agregada al usar una composición común de cohortes? CALC-EDER-0003 ya mide total y cohortes marginales. La extensión nueva es sexo×cohorte, diferencias dentro de cohorte y estandarización descriptiva. No mide ENADID ni situación conyugal actual.

## Fuente y contrato
Lee CALC-EDER-0003, su medidor, y forense/prereg-caja/EDER-UNION-LIBRE-spec-v1_0.md. Fuente eder_2017_eder2017_bases_csv, hash bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3, y FD/receta oficiales manifestados.

Reutiliza el contrato de historiavida.csv (edo_civil1, anio_retro, anio_nac y llaves), antecedentes.csv (factor_per y llaves), vivienda.csv (est_dis, upm y llave). Identifica desde el FD la variable de sexo, su tabla, códigos y llave; se autoriza añadir únicamente esa columna y llaves de enlace, usando persona.csv sólo si el FD la sitúa allí. No adivines el campo ni infieras sexo desde parentesco. Congela la resolución antes de leer respuestas.

Persona y universo del padre: 20–54 años del instrumento, con primer edo_civil1 distinto de cero por orden anio_retro y factor_per válido. Mantén exactamente los conjuntos LIBRE/DIRECTO y el residual sin clasificar del padre. No uses 1−libre como matrimonio directo. Los que no tienen primera unión observada se cuentan fuera del denominador, no como directos.

## Productos que deben quedar medidos
1. Auditoría sustantiva de enlaces, persona única, pesos/diseño, sexo/cohorte desconocidos, ausencia de primera unión y primera observación de disolución. Empates incompatibles al ordenar historia no se resuelven por orden accidental.
2. Partición libre/directo/sin clasificar para total, sexos, cuatro cohortes del padre (≤1970, 1971–1980, 1981–1990, 1991+) y las ocho intersecciones sexo×cohorte. Categorías desconocidas se publican aparte y permiten reconstruir totales.
3. Cuatro contrastes mujer−hombre de proporción de primera unión libre, uno por cohorte, y diferencia agregada cruda. Cada contraste incluye puntos de ambos grupos, soporte, covarianza e IC.
4. Diferencia estandarizada mujer−hombre con ponderaciones de cohorte comunes: composición ponderada conjunta de mujeres y hombres del universo con sexo/cohorte válidos. Fija esa población de referencia antes de medir. Compara con la diferencia cruda calculada sobre exactamente ese mismo universo; entrega cambio estandarizada−cruda e IC conjunto. Si falta soporte en una celda requerida, declara no estimable; no redistribuyas automáticamente su peso.
5. Control independiente de puntos y un contraste; reconstrucción de total/cohortes del padre, incluida masa sin clasificar. Diferencias por universo se explican numéricamente.

## Precisión y lectura
Bootstrap de UPM dentro de estrato, marco completo de personas ponderables, 2,000 réplicas PCG64 y semilla congelada. Un mismo sorteo para celdas, diferencias y estandarización; recalcula en cada réplica la composición común porque es estimada de la encuesta. Publica réplicas válidas y fija antes del cálculo el criterio de precisión disponible. Conserva singleton con advertencia explícita sobre el tratamiento; no afirmes que el intervalo sea un límite matemático garantizado de incertidumbre.

Entrega perfiles y contrastes procesables, pesos de estandarización y lectura. La comparación es entre quienes tienen primera unión observada: cohortes recientes han tenido menos tiempo para unirse y la encuesta no representa a quienes fallecieron o salieron del marco. No interpretar como cambio causal generacional, riesgo de formar unión, efecto de sexo, ni como prevalencia conyugal actual. Sin sustitución de segmentaciones adoptadas.

## Ejecución y entrega obligatoria
Encargo para Codex CLI en CAJA, repositorio Josanoforo/Modelado-Mexicano. Base examinada al diseñarlo: ea88cb3b94ad820bcd92a485eae51ce24ef07fae. Trabaja en worktree propio desde main vigente y lee AGENTS.md e instrucciones del proyecto. Este texto autoriza desarrollar, ejecutar la medición delimitada, commit, push y PR; no merge ni adopción. Archiva íntegro este encargo.

Antes de abrir respuestas, contrasta el objeto con CALC, encargos y ramas vigentes por contenido, no sólo por nombre. Si una parte ya existe, reutilízala como control y completa únicamente la extensión faltante. Localiza payload por manifiesto/hash y rutas de corpus autorizadas; su ausencia en el worktree no prueba que falte en CAJA. No entregues un cascarón de código cuando puedes ejecutar con el corpus disponible.

Congela en COMMIT-1, antes del cálculo nuevo, fuentes/columnas, universos, denominadores, faltantes, estimandos, contrastes, método de precisión y salidas. Declara la exposición a resultados anteriores: no es un análisis ciego. Los nombres de CALC propuestos se verifican antes de asignarlos. Guarda el primer resultado obtenido y cualquier intento fallido; una corrección material posterior al sello requiere sucesión, nunca sobrescritura.

Entrega medidor determinista, CALC con RESULT y sello, tablas procesables completas, lectura sustantiva, control independiente dirigido y evidencia de replay de tu CALC mediante interfaces vigentes. Publica cada salida comprometida o un estado explícito de no estimabilidad con causa y soporte. Cero, desconocido, fuera de universo y no estimable son distintos. Tablas: n y masa expuestos/válidos/desconocidos, numerador y denominador, punto, EE/IC cuando procedan y diagnóstico del diseño. El control independiente no importa el medidor; comprueba al menos un punto y una varianza o contraste por una implementación separada.

La lectura debe responder la pregunta con cifras, límites de población y qué queda sin identificar. Incluye matriz alcance→artefacto→resultado/limitación y recibo con SHA, comandos y replay. No cierres como completo con sólo un plan, un diagnóstico o tests sintéticos. Si hay impedimento material, conserva lo obtenido y especifica el insumo que falta; no inventes resultados para completar la tabla.

Escribe sólo el CALC nuevo, su especificación, análisis, controles/pruebas propias y evidencia propia. Padres sellados son sólo lectura. No tocar motor, milpa, gobierno, CRON, piloto 3, ni el PR889. No abrir ENCIG2025, ENIF2024, ENVIPE2025, HOLDOUT ni reservas nuevas. No adoptar parámetros, cambiar tiers o contar celdas como fuentes independientes. CI, colisiones, sync y fetch los coordina Jonás en la sesión: no conviertas este encargo en una reparación de infraestructura. No modificar tests/check.py, baseline ni workflows. No aceptar cambios de replay ajeno con --lote.
