# Reservas de interpretación · potencia ENCIG

EJECUTADO: código congelado en COMMIT-1 `0dbe658d`; 2000 réplicas históricas conjuntas, 81 escenarios y 36 MDE. Estos resultados consumen únicamente auxiliares agregados, no abren una ola futura.

LEÍDO del auxiliar sellado: PAGO-DIGITAL es **NO-ESTIMABLE**: residuo ponderado `0.011175751658793141` supera el gate congelado 0.01. SOLICITUD-MORDIDA es **ESTIMABLE**, residuo `0.0022577799879037706`. Los puntos reproducen el oro; esa coincidencia no elimina la falta de soporte del primer estimando.

La potencia digital describe únicamente el comportamiento hipotético del estimador de casos válidos bajo escenarios y condicionado a superar gates. **No acredita activar PAGO-DIGITAL**: el oro histórico es NO-ESTIMABLE. No se retira residuo, cambia umbral ni selecciona variante para obtener activabilidad; una propuesta de enmienda material requiere su firma y nuevo protocolo. El objeto poblacional incompleto limita el traslado de esta distribución al futuro.

Para SOLICITUD-MORDIDA, el oro supera soporte, pero la activación futura sigue condicionada a identidad, comparabilidad, reserva y código autorizado, además de soporte de esa ola. Potencia de escenario no acredita eficacia predictiva ni cobertura nominal; la aproximación bootstrap y su traslado temporal no están certificados por simulación de cobertura.

Dependencia: ambas familias comparten sorteos del marco completo de `9172` UPM y `442` estratos; el marco tiene `0` estratos de UPM única. Unidades y ponderadores siguen separados. Correlación residual empírica `0.05508470280546991`. Se añade ruido temporal común solo como sensibilidad; no empareja olas reales.

La probabilidad de DESVÍO con shift cero y SD temporal cero es falso desvío respecto a igualdad al piso. Cuando SD temporal es positivo, incluye desviaciones reales aleatorias y deja de ser error tipo I puro. MDE y probabilidades informativas se reportan sin cambiar banda ±2 pp ni gates.

Los multiplicadores 0.5, 1 y 2 escalan el EE (varianzas 0.25, 1 y 4), conforme a spec previa; no son estimaciones de inflación futura. La normal temporal 0/1/2 pp tampoco está estimada a partir de series comparables.

Fuentes mecánicas: `data/corrida0/CALC-ENCIG-AUX-FAMILIAS-2027-0001/tablas/replicas.json`, `pisos.json` y `potencia.json`; hashes completos de entradas y código dentro de potencia.json. `potencia.md` es salida íntegra del código congelado.
