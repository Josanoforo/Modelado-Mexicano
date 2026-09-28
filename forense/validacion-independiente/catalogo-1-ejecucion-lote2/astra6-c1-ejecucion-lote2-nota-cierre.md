# C1 lote2 · Resultado y reservas

EJECUTADO: cohorte original 425 identidades = 333 ejecutables + 92 apartadas por NC-beee-09. Las diez sesiones operativas terminaron; el intento de ENDIREH anterior a la adenda también se conserva como diagnóstico. No hay pendientes de ejecución entre las 333. C1 permanece abierto y los resultados no están adoptados.

EJECUTADO: puntos: {"COINCIDE": 275, "NO-RECALCULABLE-DESDE-SPEC": 56, "NO-EVALUADO": 92, "DISCREPA": 2}. IC: {"SIN-IC-DE-REFERENCIA": 10, "NO-RECALCULABLE-DESDE-SPEC": 312, "DISCREPA": 8, "NO-EVALUADO": 92, "COINCIDE": 3}. Estados completos (punto e incertidumbre donde existen): {"COINCIDE": 11, "NO-RECALCULABLE-DESDE-SPEC": 312, "DISCREPA": 10, "NO-EVALUADO": 92}. Coincidencia de punto no valida el estimando, la calibración del IC ni capacidad predictiva.

| Entrada | Identidades | Punto | IC |
|---|---:|---|---|
| eder-0003-v4 | 2 | {"COINCIDE": 2} | {"SIN-IC-DE-REFERENCIA": 2} |
| enbiare-pisos-bienestar-0001-v3 | 180 | {"NO-RECALCULABLE-DESDE-SPEC": 54, "COINCIDE": 126} | {"NO-RECALCULABLE-DESDE-SPEC": 180} |
| encig-0001-v5 | 4 | {"COINCIDE": 4} | {"DISCREPA": 4} |
| encodat-pisos-sustancias-0001-v3 | 130 | {"COINCIDE": 130} | {"NO-RECALCULABLE-DESDE-SPEC": 130} |
| encuci-0001-v3 | 3 | {"COINCIDE": 2, "NO-RECALCULABLE-DESDE-SPEC": 1} | {"DISCREPA": 2, "NO-RECALCULABLE-DESDE-SPEC": 1} |
| endireh-pisos-2016-pareja-fisica-0002-v2 | 92 | {"NO-EVALUADO": 92} | {"NO-EVALUADO": 92} |
| enfih-0001-v4 | 2 | {"COINCIDE": 2} | {"DISCREPA": 1, "SIN-IC-DE-REFERENCIA": 1} |
| enigh-0001-v4 | 1 | {"NO-RECALCULABLE-DESDE-SPEC": 1} | {"NO-RECALCULABLE-DESDE-SPEC": 1} |
| enigh2020-intensidad-remesas-0001-v4 | 6 | {"DISCREPA": 2, "COINCIDE": 4} | {"COINCIDE": 3, "SIN-IC-DE-REFERENCIA": 3} |
| envipe-0001-v5 | 1 | {"COINCIDE": 1} | {"DISCREPA": 1} |
| envipe-denuncia-seguro-0001-v4 | 4 | {"COINCIDE": 4} | {"SIN-IC-DE-REFERENCIA": 4} |

EJECUTADO: las dos discrepancias de punto son de ENIGH remesas y de precisión aritmética; se conserva DISCREPA bajo tolerancia cero, sin ajustar umbral ni redondear para hacer coincidir. No se demuestra efecto material en conclusión. Las ocho discrepancias IC corresponden a ENCIG, ENFIH, ENCUCI y ENVIPE: sus reconstrucciones congeladas declaran convenciones de orden/marco/consumo aleatorio no fijadas en la entrega humana. No se acredita identidad de realización ni equivalencia inferencial; no se cambia semilla ni abs. Detalle por llave: p3/discrepancias-investigadas.tsv y p3/insuficiencia-ic-exacto.tsv.

EJECUTADO: ENBIARE dejó sin punto 54 identidades por tratamiento de edades no especificadas; ENCUCI una identidad rural con segmento urbano contradictorio; ENIGH una identidad de complemento sin correspondencia explícita. Los 256 puntos restantes de ENBIARE/ENCODAT sí coinciden, pero falta la receta humana de IC remitida por la entrega. Los estados de insuficiencia se refieren a las entradas recibidas: no se presume defecto D-15 de la spec original sin distinguir omisión de empaquetado. Ninguna cifra suprimida o no reconstruible se inventó. Publicabilidad: {"CIFRA-EMITIDA": 277, "NO-DETERMINADA": 56, "APARTADA-POR-DEFECTO-DE-PAQUETE": 92}. CIFRA-EMITIDA describe emisión y referencia; no certifica la regla de publicación.

LEÍDO y EJECUTADO: #1192 está fusionado en 7fcbc2e6 y es ancestro del corte inicial 11602de8. NC-beee-09 ya advertía falta de ventana ENDIREH2016. El orquestador omitió detectar ese asiento antes del lanzamiento; no se atribuye el defecto a una novedad posterior. La adenda llegó después del commit eb3ccb61 del validador: se preservan entrada, salida, intento, hashes y orden temporal, sin relanzar ni insertar ventana. Las 92 quedan NO-EVALUADO por defecto de empaquetado, con estado original del validador separado. Registro local por identidad: p4/no-corrido-identidades-local.tsv. Sucesor ASTRA6-C1-REEMPAQUETA-VENTANA-1; sus 767 de 2021 no pertenecen a este lote.

EJECUTADO: el TSV de entrega en LF tiene SHA 75b1febc; el SHA declarado 3393c425 corresponde a los mismos bytes convertidos a CRLF en memoria. No se sustituye un hash por el otro ni se reescribe el original. Los once hashes tar/manifiesto aprobados sí coinciden; evidencia completa p2/verificacion-crlf.json. Los archivos de reconstrucción se archivan con atributos locales que preservan los bytes CRLF originales y con pruebas portables de pertenencia al commit.

EJECUTADO: adaptador y contrato congelados en 1345846f antes de lanzamiento, cinco rechazos sintéticos, once tolerancias idénticas a las originales. El paquete/lanzador no fijó columnas de salida, y nueve sesiones usaron alias numéricos incompatibles con v1. Se conservan todos los rechazos y las salidas originales; dictámenes separados por correspondencia explícita de nombres mantienen valores y tolerancias. No se modifica el adaptador congelado ni se presenta esa operación como éxito suyo. Las revisiones diagnósticas de alias ENCIG/ENBIARE quedan preservadas y superadas por v2, no son D-15. p3/interpretacion-transporte.md detalla el acto.

EJECUTADO: once sesiones nuevas con entrada mínima, contexto/archivos aislados y commits originales verificados; un fallo de infraestructura EDER antes de números y segundo intento en carpeta nueva. La red NO está aislada ni hay monitor egress o allowlist del host API. El examen de comandos no observó llamadas de red ajenas al transporte, pero no prueba ausencia de todo tráfico. La evidencia de separación y cobertura se acota a contexto/archivos y transcript; NC-beee-08 permanece como reserva de red. No se reconstruye ceguera retroactiva.

EJECUTADO: 277/425 puntos reconstruidos bajo ese alcance de separación; aportación de este lote al histórico 277/36143 y al overlay 277/43188, por separado. Son fracciones de cobertura añadida, no tasas representativas de coincidencia ni cobertura total acumulada de C1. Selección por preparación y dependencia por olas/fuentes compartidas; once paquetes no son once muestras independientes. Lote1 y sus nueve paquetes quedan fuera. Los 22 enlaces consumidores se trazan en P4 sin adoptar cambios.

PROPUESTO-POR-EJECUTOR: recibir las ejecuciones y reservas como evidencia, mantener C1 abierto, tramitar entradas sucesoras con receta IC/codificación/correspondencia suficientes y un adaptador nuevo congelado antes de otro lote. No reparar entradas ni sellos en este acto. Las consecuencias propuestas están por identidad y consumidor; ninguna coincidencia rehabilita veto o adopta estimando.

EJECUTADO: perímetro de escritura exclusivo de lote2 y auxiliares propios; recibos/NO-CORRIDO locales exportan el estado por identidad sin duplicar la NC común ni modificar contador, catálogo o sellos. El cuerpo original se consume del asiento #1191 con hash verificado; la firma Acordado ya existente no se vuelve a registrar. Adenda archivada íntegra con SHA propio.

EJECUTADO: validación propia mediante lote2_verifica.py (hash de adaptador/contrato, 425 llaves únicas, orden de recepción/revelación, once pruebas portables de salida/código y hashes de archivos); constancias de una sola conversación de usuario por validador sin outputs raw. Gate y contador final se conservan en lote2-gate-final.txt y lote2-contador-delta.json. CI no constituye prueba sustantiva.

Auditoría de alcance: comparación retrospectiva por identidad/unidad original, sin promediar hogar/persona/delito/trámite ni afirmar rasgos culturales, identificación causal o transporte a población rural/indígena. Semillas y tolerancias se conservan. Las limitaciones de incertidumbre y entrega impiden generalizar coincidencia numérica. El contador se deriva por herramienta y no se incrementa por diagnósticos.

EJECUTADO: tablas auxiliares de réplicas e inventarios JSON extensos archivados en gzip determinista. Los hashes de inventario y la prueba de commit corresponden a los bytes originales descomprimidos, verificados exactamente; los originales además permanecen en los checkouts de sesiones. No se comprimen ni modifican las reconstrucciones principales.
