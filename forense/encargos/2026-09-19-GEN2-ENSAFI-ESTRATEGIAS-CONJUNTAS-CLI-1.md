# Encargo 1 · ENSAFI 2023: combinaciones de estrategias ante insuficiencia
Rama propuesta: codex/gen2-ensafi2023-estrategias-conjuntas-cli-1.
CALC propuesto: CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001.

## Pregunta y avance
¿Cuántas estrategias declara simultáneamente la persona ante insuficiencia de ingreso, cuáles coexisten y cuánto cambia la lectura por respuestas incompletas? El padre CALC-ENSAFI-DISENO-0001 ya publica ocho marginales. Este encargo produce la distribución conjunta y su incertidumbre; no vuelve a presentar las marginales como producto nuevo.

## Fuente y contrato
Lee el padre y forense/prereg-caja/ENSAFI-ATRASO-AFRONTAMIENTO-DISENO-spec-v1_0.md. Fuente ensafi2023_bd_csv_zip, hash c0594079ddf4733d4f574d00f5e84290c62c5330eab0567dd867c26d42fafacd; TMODULO.csv, LLAVEMOD, P6_9, P6_10_1..8, FAC_ELE, EST_DIS, UPM_DIS. Confirma etiquetas y saltos con descriptor/cuestionario manifestados antes de congelar. No enlazar THOGAR ni incorporar otras variables.

Universo: persona elegida de 18+ con P6_9=2. Respuestas 1/2 válidas; no convertir blancos, códigos especiales o fuera de dominio en no. Peso de persona FAC_ELE. Conserva el marco completo de TMODULO para diseño, con aportaciones cero fuera de dominio.

## Productos que deben quedar medidos
1. Cobertura del vector completo: n/masa y proporción de personas con las ocho respuestas válidas entre elegibles; distribuye también el número de respuestas desconocidas.
2. Entre vectores completos, distribución ponderada del número de estrategias 0..8, media del conteo, P(al menos una), P(al menos dos) y P(al menos cuatro). Las nueve categorías sí forman una partición; las ocho marginales no.
3. Para las 28 parejas de estrategias, tabla 2×2 sobre el mismo universo de vectores completos, P(ambas) y ambas probabilidades condicionales. Publica ceros y denominadores vacíos sin seleccionar únicamente combinaciones llamativas. No sumar los 28 cruces como si fueran personas distintas.
4. Sensibilidad de cada pareja al universo con sólo esas dos respuestas válidas: cobertura, P(ambas), diferencia respecto al vector completo e IC de la diferencia con covarianza. Es una sensibilidad de selección por faltantes, no otra muestra.
5. Sin imputación, límites de identificación para P(conteo≥1), ≥2 y ≥4 sobre todos los elegibles: mínimo=afirmaciones conocidas, máximo=mínimo+desconocidas. El límite inferior cuenta mínimos que superan el umbral; el superior, máximos. Publica esos límites separados de los IC de muestreo.
6. Controles: partición 0..8, media del conteo igual a suma de marginales sobre vector completo, reconstrucción de tablas 2×2 y recuperación de las marginales originales usando exactamente sus denominadores originales.

## Precisión y lectura
Usa la linealización por UPM/estrato del contrato padre, t de diseño, sin FPC no documentada. Para diferencias entre universos calcula la influencia conjunta, nunca suma de varianzas independientes. Declara singleton y diseño faltante; probabilidades de frontera no reciben un IC de anchura cero como precisión acreditada. Los IC son puntuales, sin selección de “parejas significativas” ni ranking inferencial.

Entrega tablas de conteos, parejas completas, sensibilidad y límites por faltantes. No llames al conteo índice de estrés/severidad; las estrategias no tienen la misma naturaleza ni costo. No infieras secuencia, causalidad, productos de deuda ni cierres NC-0164.

## Ejecución y entrega obligatoria
Encargo para Codex CLI en CAJA, repositorio Josanoforo/Modelado-Mexicano. Base examinada al diseñarlo: ea88cb3b94ad820bcd92a485eae51ce24ef07fae. Trabaja en worktree propio desde main vigente y lee AGENTS.md e instrucciones del proyecto. Este texto autoriza desarrollar, ejecutar la medición delimitada, commit, push y PR; no merge ni adopción. Archiva íntegro este encargo.

Antes de abrir respuestas, contrasta el objeto con CALC, encargos y ramas vigentes por contenido, no sólo por nombre. Si una parte ya existe, reutilízala como control y completa únicamente la extensión faltante. Localiza payload por manifiesto/hash y rutas de corpus autorizadas; su ausencia en el worktree no prueba que falte en CAJA. No entregues un cascarón de código cuando puedes ejecutar con el corpus disponible.

Congela en COMMIT-1, antes del cálculo nuevo, fuentes/columnas, universos, denominadores, faltantes, estimandos, contrastes, método de precisión y salidas. Declara la exposición a resultados anteriores: no es un análisis ciego. Los nombres de CALC propuestos se verifican antes de asignarlos. Guarda el primer resultado obtenido y cualquier intento fallido; una corrección material posterior al sello requiere sucesión, nunca sobrescritura.

Entrega medidor determinista, CALC con RESULT y sello, tablas procesables completas, lectura sustantiva, control independiente dirigido y evidencia de replay de tu CALC mediante interfaces vigentes. Publica cada salida comprometida o un estado explícito de no estimabilidad con causa y soporte. Cero, desconocido, fuera de universo y no estimable son distintos. Tablas: n y masa expuestos/válidos/desconocidos, numerador y denominador, punto, EE/IC cuando procedan y diagnóstico del diseño. El control independiente no importa el medidor; comprueba al menos un punto y una varianza o contraste por una implementación separada.

La lectura debe responder la pregunta con cifras, límites de población y qué queda sin identificar. Incluye matriz alcance→artefacto→resultado/limitación y recibo con SHA, comandos y replay. No cierres como completo con sólo un plan, un diagnóstico o tests sintéticos. Si hay impedimento material, conserva lo obtenido y especifica el insumo que falta; no inventes resultados para completar la tabla.

Escribe sólo el CALC nuevo, su especificación, análisis, controles/pruebas propias y evidencia propia. Padres sellados son sólo lectura. No tocar motor, milpa, gobierno, CRON, piloto 3, ni el PR889. No abrir ENCIG2025, ENIF2024, ENVIPE2025, HOLDOUT ni reservas nuevas. No adoptar parámetros, cambiar tiers o contar celdas como fuentes independientes. CI, colisiones, sync y fetch los coordina Jonás en la sesión: no conviertas este encargo en una reparación de infraestructura. No modificar tests/check.py, baseline ni workflows. No aceptar cambios de replay ajeno con --lote.

