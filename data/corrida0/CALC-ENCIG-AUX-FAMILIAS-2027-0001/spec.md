# ENCIG · auxiliar histórico y protocolo de dominios · v1.0

PROPUESTO-POR-EJECUTOR antes de leer registros. Autorización: encargo ASTRA6-C2-ENCIG-1 firmado y archivado, §5 P1–P3. Solo ENCIG2025 abierta. No cambia productor ni sellos históricos.

## Estimandos y lectura

Dos unidades separadas: persona adulta residente en localidades urbanas de 100 mil habitantes o más, SOL1 P8_3_1=1 sobre {1,2}, FAC_P18; evento de pago de luz N_TRA=1, canal {4,5} sobre {1,2,4,5,6}, FAC_TRA. La proporción mayor denota más solicitud declarada o más pago digital/autoservicio, respectivamente. No inferencia nacional, causal ni psicológica. Residuo incluye códigos restantes, blancos y no numéricos, contado y pesado contra todo el universo potencial con ponderador positivo. Peso ausente invalida soporte; ningún cero lo sustituye.

La lista blanca son dos tablas y únicamente las columnas de lector.py: ID_PER y diseño para marco/persona; ID_PER, ID_TRA+NT_TIPO, N_TRA y canal para evento. No abre otras tablas ni segmentos. Persona única y evento único, sin deduplicar. Se verifica igualdad de llaves opacas EST_DIS/UPM_DIS entre cada evento y su ID_PER. Mismatch: NO-COMPARABLE, sin reparar claves mirando el dato.

## Incertidumbre antes del dato

Bootstrap con reemplazo dentro de estrato, n UPM en cada réplica. El marco es TODA la tabla persona, previo a filtrar cualquier outcome. Cada UPM aporta dos pares numerador/denominador; se conserva cero fuera del dominio. Las multiplicidades se comparten por llaves de diseño reales, nunca por índice entre olas. UPM única en dominio no implica UPM única del marco. Si hay UPM única en el marco completo, se informa y se prohíbe dictaminar con varianza cero: IC nulo/NO-ESTIMABLE. No se colapsan estratos ni inventan UPM. Aproximación con reemplazo por conglomerados últimos, sin fracciones de selección ni replicación de ajustes de no respuesta; no certifica cobertura nominal. Diseño oficial ENCIG2025 §10, y método bootstrap ya propuesto v1.2. Especificar el marco completo conserva su método, no reescribe un procedimiento histórico sellado.

2000 réplicas PCG64, seed y gates están únicamente en spec.yaml. IC percentil95 de R_k−p0, p0 fijo. No incertidumbre histórica propagada al primario. Pérdida relevante es diferencia con signo y absoluta; ΔMAE y B-bis NO-APLICABLE sin retador. No se elige variante por potencia. N efectivo de Kish es diagnóstico del ponderador, no tamaño efectivo del diseño completo.

## Gate y dictamen

Comparabilidad antes del ZIP futuro: instrumento/ola, urbano100mil/18+, unidad, reactivos/saltos, códigos, pesos y descriptor cotejados; autorización de ola reservada, un acto y una apertura para ambas familias. Hash de código y payload verificados. Sin equivalencia: NO-COMPARABLE. Equivalencia nominal exige adaptación documentada antes de ejecución; cambio sustantivo no se adapta. La guardia es una condición necesaria; el asiento firmado y su revisión pertenecen al circuito de mesa, ningún diccionario suministrado autoriza por sí mismo.

Soporte fijo de v1.2: n≥10000, estratos≥100, UPM≥1000, residuo digital≤1% y solicitud≤2%, ningún peso ausente, ≥1000 réplicas válidas y denominador positivo en≥95%. Ausencia de soporte/IC: NO-ESTIMABLE. Todas las salidas nulas (p, IC, diferencia, fracción, residuo relativo, Kish) se enumeran; NaN/Inf nunca salen en JSON. Con intervalo válido [L,U] de R−p0: COMPATIBLE-CON-TOLERANCIA si −.02≤L y U≤.02; DESVÍO-MATERIAL si U<−.02 o L>.02; INDETERMINADO en resto. Fronteras inclusivas para compatibilidad, estrictas para desvío.

## Conducto y evidencia

El auxiliar sella puntos, soporte y REF a tabla de 2000 réplicas, sin individuos. Oro: cotejo de puntos contra RESULT históricos/hash con tolerancia1e−12; no se espera reproducir IC históricos calculados sobre otro marco de dominio, ni esto cuenta como validación ciega. Reproducción de emisiones se verifica aparte por corrida0 verify. Una comparación futura compatible permite solo compatibilidad local, jamás CALIBRADO.

## Auditoría de alcance

La encuesta mide declaraciones y canales disponibles, no cultura ni preferencias independientes de oferta. Excluye rural/localidades menores e indígena-comunal por diseño urbano; generalizar a todo México sería peligroso. No usa muestras importadas ni variables de ascendencia. Dos unidades no se mezclan y sus outcomes son dependientes por el marco. Los pisos son retrospectivos; las emisiones preceden la R futura y no demuestran capacidad predictiva. No hay adopciones ni contadores manuales.
