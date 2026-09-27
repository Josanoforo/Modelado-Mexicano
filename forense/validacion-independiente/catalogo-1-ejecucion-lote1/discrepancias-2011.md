# ENDIREH 2011 · investigación posterior a congelación

EJECUTADO: inspección no ciega posterior al primer cálculo independiente, sin recalcular, ajustar tolerancias ni cambiar sellos. Reconstrucción congelada en commit `38fb8c5499bedb8af2436c6b41228a38ecbf510f`, SHA-256 `8f5272727f2d86f6e79c85700dac22e7a751f574710d89c781a3f589e397ee5a`; comparación conserva recibo `CONGELADO-SIN-REVELAR` y orden temporal acreditado. Fuentes: tabla-estimadores.tsv, comparación de este paquete, artefactos/reconstruir.py y ejecucion.json, universo histórico por identidad; único productor leído: CALC-ENDIREH-PISOS-2011-MODULOS-0001/spec.md y medidor.py. Resultados originales consultados selectivamente para las seis supresiones.

Los conteos por CSV/JSON de este paquete dan 1894 identidades: 1888 reconstruidas numéricamente; 683 puntos fuera de tolerancia; 1202 puntos coincidentes con IC diferente; 3 coinciden en punto e IC; 6 reconstrucciones ejecutadas con supresión de publicación. Máxima diferencia absoluta de punto: 0.3325165761353075. La agrupación siguiente es excluyente, dando prioridad al corte edad 60+; no identifica unívocamente cuánto aporta cada mecanismo cuando concurren.

| Grupo | Puntos discrepantes | Evidencia y causa plausible |
|---|---:|---|
| Ámbitos externos por agresor/lugar | 535 | medidor.py:183–189 declara negativo si cualquier casilla contiene código válido, aunque la otra sea desconocida; reconstruir.py:120–131 exige casillas válidas o vacías antes de declarar ausencia. Divergen denominadores conocidos para códigos 8/9/99 según dominio; desconocido no equivale a negativo en spec.md §ámbitos. No se atribuye toda diferencia a una casilla sin tabulación raw adicional. |
| Corte edad 60+ | 36 | medidor.py:40–46 acepta edades hasta 120; reconstruir.py:162 limita 60+ a 97. EDAD 98/99 requieren cotejo FD antes de decidir qué implementación corresponde. Peso FAC_PER es el mismo; cambia inclusión por edad. |
| Pareja período reciente | 62 | medidor.py:250 condiciona resultado reciente a que unión de vida sea conocida; reconstruir.py:79–82 clasifica reciente independientemente, conservando el salto 6.1=4. Un grupo vida desconocido pero reciente clasificable genera denominadores distintos. |
| Institución de pareja | 6 | medidor.py:259 usa solo mujeres que solicitaron alguna ayuda; reconstruir.py:87 usa todas las afectadas. Cambia el estimando: proporción de cada institución entre solicitantes vs entre afectadas. spec.md describe ayuda entre afectadas pero no explicita el condicionamiento adicional por alguna ayuda para cada institución. |
| Permisos | 34 | medidor.py:282–285 clasifica CP7_1 sin filtrar CP4_1; reconstruir.py:115 restringe a relación actual/anterior CP4_1=1/2. Puede cambiar universo cuando hay respuestas fuera del salto. No son diferencias de recodificación 1/2/3. |
| Denuncia externa | 10 | medidor.py:220 itera j en (1,4+1), es decir columnas 1 y 5; reconstruir.py:144–150 usa resultados 1–4 enlazados con solicitud institucional. Diferencia concreta de selección/mapeo de columnas y de elegibilidad, no ponderador. |

EJECUTADO: ambas implementaciones usan FAC_PER y medias ponderadas entre respuestas conocidas, sin imputar NS/NR a cero de forma general. Las divergencias documentadas son filtros y clasificación particulares. La etiqueta de identidad conducta/eje/segmento se mantuvo; las diferencias no son una permutación de llaves. No se ejecutó un cálculo contrafactual para separar magnitudes causales.

Para los 1202 casos que solo difieren en IC, la identidad bit a bit no demuestra equivalencia estadística: el productor reconstruye marco de UPM desde mujeres admitidas, orden de inserción y semilla modificada por resultado/eje/categoría; la reconstrucción usa TViviend completo, estratos/UPM lexicográficos y una matriz común de 200 réplicas con PCG64 y semilla 20260923. Su ejecucion.json declara 16910 UPM y 20 sin mujeres en módulos. Esto altera marco y realización aleatoria; explica por qué pueden diferir límites con punto idéntico, sin demostrar que la cobertura inferencial sea equivalente. Se conserva tolerancia preexistente abs=1e-10.

## Supresiones: publicabilidad, no imposibilidad de reconstrucción

PROPUESTO-POR-EJECUTOR: reclasificar estas seis identidades como DISCREPA con efecto alcance/publicabilidad. El código independiente ejecutó estimación y réplicas y aplicó los umbrales de ancho/CV; omitió punto/réplicas por la regla de publicación. Su estado NO-RECALCULABLE-DESDE-SPEC es una etiqueta de salida inadecuada para ese motivo, no evidencia D-15. No recuperar por ingeniería inversa valores no publicados ni cambiar el primer archivo congelado.

| Llave | Identidad | Original | Reconstrucción |
|---|---|---|---|
| RESULT-ENDIREH2011-MOD-TABLA#1919 | permiso_03 · entidad=01 | PUBLICABLE; n=1269; UPM=390 | SUPRIMIDO-POR-SPEC: ancho/CV |
| RESULT-ENDIREH2011-MOD-TABLA#1993 | permiso_04 · entidad=29 | PUBLICABLE; n=1094; UPM=370 | SUPRIMIDO-POR-SPEC: ancho/CV |
| RESULT-ENDIREH2011-MOD-TABLA#2039 | permiso_05 · entidad=29 | PUBLICABLE; n=986; UPM=365 | SUPRIMIDO-POR-SPEC: ancho/CV |
| RESULT-ENDIREH2011-MOD-TABLA#2067 | permiso_06 · entidad=11 | PUBLICABLE; n=1150; UPM=495 | SUPRIMIDO-POR-SPEC: ancho/CV |
| RESULT-ENDIREH2011-MOD-TABLA#2082 | permiso_06 · entidad=26 | PUBLICABLE; n=829; UPM=384 | SUPRIMIDO-POR-SPEC: ancho/CV |
| RESULT-ENDIREH2011-MOD-TABLA#606 | externo_denuncia_ultima_visita · escolaridad=superior | PUBLICABLE; n=295; UPM=293 | SUPRIMIDO-POR-SPEC: ancho/CV |

Cinco son permisos y una denuncia externa; diferencias de filtros/mapeo también pueden modificar el punto previo a supresión. En los permisos, los CV originales calculados desde se/p están próximos al umbral 0.30; denuncia externa tiene ancho original próximo a 0.20. No se puede atribuir la discrepancia de publicación exclusivamente a azar sin revisar estimando y soporte.

## Efecto y límites sobre consumidores

LEÍDO/EJECUTADO: las 1894 identidades permanecen vigentes en catálogo v1.2 según vigencia.tsv. Búsqueda dirigida encuentra 1894 referencias en canon/tabla-de-piso-v1_1.tsv; no encontró el RESULT/CALC literal en milpa/, corpus/reports-v2/ ni canon/catalogo-del-mexicano-v1_2.md. Esto acredita exposición en piso y catálogo, no ausencia de consumidores indirectos por alias.

PROPUESTO-POR-EJECUTOR: mantener las 683 discrepancias de cifra como evidencia que requiere revisión del universo/estimando antes de consumir tasas comparadas entre grupos; destacar seis instituciones por cambio del denominador y denuncia externa por columnas mal seleccionadas. No afirmar que toda conclusión cambia: no se evaluaron umbrales de reglas ni comparaciones temporales. Revisar publicabilidad de las seis supresiones y tratar los 1202 IC aparte de errores de punto; no retirar automáticamente cifras o adoptar la reconstrucción. El circuito de corrección/adopción debe conservar el sello histórico y decidir un sucesor.
