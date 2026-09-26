# P3 · spec previa a réplicas y microdato

PROPUESTO-POR-EJECUTOR, ASTRA6-C2-ENCIG-1 §P3. Se congela con código en COMMIT-1, antes de leer microdatos o generar réplicas históricas nuevas. No modifica productor histórico ni primario firmado.

## Entradas y dependencia

`potencia.py` consume únicamente auxiliares JSON agregados de ENCIG 2025 abierta. Réplicas: `{joint_design:true,familias:{PAGO-DIGITAL:{p,replicas:[...]},SOLICITUD-MORDIDA:{p,replicas:[...]}}}`. Se aceptan también claves con prefijo ENCIG-. Dos columnas alineadas representan el mismo sorteo estratificado de UPM del marco persona completo. Pago usa ponderador de evento FAC_TRA y solicitud FAC_P18; contribuciones cero fuera de cada dominio conservan marco y dependencia, sin equiparar unidades. El productor auxiliar usa bootstrap ordinario con reemplazo de n UPM por estrato y 2000 réplicas conjuntas. Si el marco completo contiene un estrato de UPM única declara NO-ESTIMABLE; no le atribuye varianza cero ni agrupa estratos después de ver resultados. Este script exige al menos 100 réplicas, valores finitos [0,1] y variación positiva. No empareja olas diferentes por índice.

Pisos: `{familias:{PAGO-DIGITAL:{p0,result_id,source_sha256},SOLICITUD-MORDIDA:{p0,result_id,source_sha256}}}` obtenidos mecánicamente de RESULT sellados, nunca cifras tecleadas. Se registra hash de ambos archivos y código. Numpy es dependencia material; se registra su versión en el entorno del acto.

## Objeto y escenarios congelados

Primario: `d=R-p0` con p0 fijo; IC percentil 95% de réplicas futuras menos p0. Banda ±0.02. COMPATIBLE si IC completo dentro de banda; DESVÍO si completo estrictamente fuera; INDETERMINADO en el resto. Fronteras incluidas en COMPATIBLE y excluidas de DESVÍO. No se propaga incertidumbre histórica al primario.

Modelo de escenario: residual bootstrap histórico `r_b=p_b-p_hist`; error futuro es residual conjunto sorteado multiplicado por escala EE s, más normal temporal común a ambas familias. La media de futuro es p0+shift, no p_hist+shift. Escalas EE 0.5, 1 y 2 (multiplicadores de varianza 0.25, 1 y 4). Cambios ±0, 1, 2, 3 y 5 pp, iguales en ambas familias; SD temporal 0, 1 y 2 pp. Se reportan 81 escenarios. No se supone independencia entre las dos familias: se conserva el sorteo conjunto y ruido temporal común.

Para cada escenario, 10000 simulaciones con semilla 26092603 sortean índices históricos conjuntos y normales comunes; se reutilizan sorteos para comparaciones de sensibilidad. R se limita a [0,1]; IC simulado es R más cuantiles 2.5/97.5 del residual escalado, limitado a [0,1]. El ruido temporal cambia la media realizada, no el EE del IC de muestreo. La distribución histórica aproximada del error y anchura del IC se trasladan al futuro: supuesto explícito que no acredita cobertura, estabilidad temporal ni identificación causal. La normal temporal puede saturar extremos y el modelo aditivo no representa cambios sustantivos de cuestionario/diseño.

Salidas: probabilidad COMPATIBLE/INDETERMINADO/DESVÍO e informativa (=1−INDETERMINADO), por familia; ambas compatibles, al menos un desvío y ambas informativas. Bajo cambio cero se informa falso DESVÍO respecto a igualdad al piso; con ruido temporal incluye cambio real aleatorio, no error tipo I puro. No se confunde DESVÍO con cobertura nominal del IC.

MDE positivo y negativo: primera magnitud en rejilla 0.0005 hasta 0.20, limitada por [0,1], con probabilidad DESVÍO ≥0.80; se informa también probabilidad informativa en ese punto. Si no alcanza, NULL y límite de búsqueda. Se calcula por familia y sensibilidad; no busca un cambio causal ni ajusta banda, soporte o selección de familias.

## Ejecución y límites

`python3 tools/familias-2027/encig/potencia.py --replicas <auxiliar> --pisos <snapshot> --output-dir forense/analisis/familias-2027/astra6-encig`

Entrega `potencia.json` con tabla completa y `potencia.md` con escenario central y MDE. Potencia de escenario, no desempeño futuro observado; ausencia de series comparables deja SD temporal como sensibilidad no estimada. No abre microdatos, manifestaciones futuras ni reservas. Umbrales y escenarios no se cambian después de resultados.
