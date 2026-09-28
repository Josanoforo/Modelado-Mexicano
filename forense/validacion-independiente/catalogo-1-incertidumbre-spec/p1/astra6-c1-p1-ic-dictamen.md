# P1 · dictamen de incertidumbre

REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA. Corte leído 11602de8; derivación desde el lote histórico, sin alterar productor, reconstrucciones, tolerancias, sellos o catálogo. Protocolo independiente PROPUESTO-POR-EJECUTOR en protocolo-propuesto.md, con hash previo a ejecución sintética en congelacion-protocolo.json. No se aplicó a pares históricos para adjudicar ni escoger tolerancias. Fuentes ejecutables locales de ambos lados, con líneas y hashes, en algoritmos-fuentes.json; llave y comparación en evidencia-ic.tsv. Los conteos están derivados por deriva_evidencia.py/resumen.json.

Se derivaron 1873 identidades con punto coincidente e IC discrepante. MARCO-DIFERENTE-DOCUMENTADO: 1202; RNG-Y-ORDEN-DIFERENTES-MARCO-NO-COTEJADO: 562; MARCO-DIFERENTE-EN-REGLA: 109. Ninguna se reclasifica como COINCIDE.

| Bloque | Solo IC |
|---|---:|
| endireh-pisos-2011-modulos-0001 | 1202 |
| endireh-pisos-2021-ayuda-0001 | 116 |
| endireh-pisos-2021-decisiones-0001 | 138 |
| endireh-pisos-2021-discriminacion-0001 | 258 |
| endireh-pisos-2021-familiar-0001 | 50 |
| endireh-pisos-2021-nofisica-bc-0001 | 109 |


El dictamen no acepta ningún IC como defendible por coincidir con código. Conserva DISCREPA bajo abs=1e-10 y recomienda no presentar equivalencia inferencial acreditada. El punto coincidente puede conservarse como descripción provisional en estas identidades, sujeto al eje conceptual/spec y publicabilidad del ensamblaje. Una realización aleatoria distinta basta para romper identidad numérica; no basta para diagnosticar invalidez. Diferente marco sí cambia la ley de replicación y exige resolver el diseño antes de declarar equivalencia.

## Reconstrucción de los algoritmos

Todos los productores comparten la familia `_aggregate`: construyen estratos y conglomerados con todas las filas admitidas, antes de elegir dominio y respuesta conocida; cada UPM ajena al dominio permanece con numerador/denominador cero. No es correcto describirlos como bootstrap solo de mujeres del dominio. El marco ya sufrió filtros en la lectura (instrumento, edad, peso y diseño válido). Remuestrean n_h UPM completas con reemplazo dentro del estrato, sin reescalamiento ni FPC; razón de totales ponderados. Singleton queda fijo (sus sorteos siempre seleccionan esa UPM), sin justificación de certeza. No finitud de alguna réplica causa supresión, sin descartar réplicas para mejorar CV. Cuantil NumPy por defecto lineal, sd ddof=1; misma regla de soporte/ancho/CV que la propuesta reproduce sintéticamente.

Productor: PCG64/default_rng con semilla base 20260923 más suma de códigos Unicode del nombre de outcome/axis/categoría (familiar omite outcome). Orden de estratos/UPM por inserción de filas; bucle réplica→estrato; reinicia RNG por identidad. El offset no cambia el estimando ni la ley ideal de sorteos; sí cambia límites finitos. La suma de caracteres puede producir colisiones entre nombres; no asegura independencia de flujos ni simultaneidad de intervalos. Reconstrucciones: un flujo base común y orden lexicográfico; algunas iteran estrato→matriz B×n_h, otras réplica→estrato. Usar PCG64 y semilla iguales no garantiza mismos sorteos cuando cambian orden, número de llamadas y marco. Réplicas compartidas además cambian dependencia entre identidades frente a los reinicios del productor: esto importa para diferencias entre celdas, aunque cada IC marginal fuese equivalente.

| Bloque | Marco independiente frente al productor | Réplicas fijadas en spec efectiva | Orden independiente / singleton |
|---|---|---|---|
| 2011 módulos | TViviend completo frente a mujeres admitidas por módulo; FAC_PER | 200 ambos | estrato→B×n_h; singleton fijo |
| Ayuda 2021 | XIV A1/A2 antes de filtros edad/actos frente a admitidas A1/A2; FAC_MUJ | 500 ambos | estrato→B×n_h; singleton explícito sin consumir RNG |
| Decisiones 2021 | XV A1/A2 antes de filtros frente a admitidas A1/A2; FAC_MUJ | 500 ambos | estrato→B×n_h; singleton explícito sin consumir RNG |
| Discriminación 2021 | VIII completo antes de elegibilidad laboral frente a admitidas válidas; FAC_MUJ | 200 ambos | estrato→B×n_h; singleton fijo |
| Familiar 2021 | XI completo antes de elegibilidad frente a admitidas válidas; FAC_MUJ | 200 ambos | réplica→estrato mediante choice; singleton fijo |
| No física BC 2021 | XIV completo, C2 incluida; productor admite A1/A2/B1/B2/C1 y excluye C2 | 200 ambos | estrato→B×n_h; assertion sin singleton en reconstrucción |
| Comunitaria 2021 | IX después de elegibilidad y antes de dominio; FAC_MUJ | 200 ambos | réplica→estrato mediante choice; singleton fijo |
| Escolar 2021 | VII completo antes de elegibilidad/dominio; FAC_MUJ | 200 ambos | réplica→estrato mediante choice; singleton explícito sin RNG |
| Laboral 2021 | VIII completo antes de elegibilidad/dominio; FAC_MUJ | 200 ambos | estrato→B×n_h; singleton fijo |

No usar el valor por defecto de `measure_rows` como contrato: decisiones tiene default 500 y comunitaria/escolar/laboral también default 500 en productor, pero `run` recibe spec.yaml, que fija 500 para decisiones y 200 en los otros tres. Los bloques con identidad D-15 no pasan a IC por tener réplicas semánticas auxiliares. Marco y peso no resuelven horizonte o recodificación ausentes.

## Marco 2011 y efecto inferencial

El archivo primario del acto anterior `.../reconstrucciones/endireh-pisos-2011-modulos-0001/artefactos/...--ejecucion.json` registra TViviend con 16910 UPM, 574 estratos, cero singleton y 20 UPM no presentes en los módulos de mujeres. Su código `design` forma pares de TViviend y calcula explícitamente la diferencia con módulos. El productor `_base` admite mujeres con peso, edad y diseño válidos y `_aggregate` arma marco con esas filas. La observación histórica de las 20 UPM no se vuelve nueva medición en esta sesión: LEÍDO, no replay nuevo. La falta de mujeres de módulo no es razón automática para eliminar una UPM del marco del diseño.

Agregar una UPM de contribución (0,0) altera n_h y probabilidades de multiplicidad de las UPM contribuyentes. El punto conserva suma de numerador/suma de denominador, pero distribución de razones, denominadores cero y varianza pueden cambiar. El test `test_marco_extra_cambia_ley` lo demuestra con enumeración exacta y el test de dominio cero conserva masa no estimable: no atribuye una dirección o magnitud a los históricos. Para identificar cuánto de cada límite corresponde al marco o al RNG se necesita cotejo por UPM y contrafactual de diagnóstico expresamente firmado, sin sustituir el primer intento. No se buscó semilla equivalente.

## Para convertir reproducción en inferencia defendible

Falta una decisión documental sobre marco del diseño (vivienda, mujeres del instrumento o submuestra), incluidos ceros por selección/no respuesta; igualdad efectiva de pares y totales por UPM entre implementaciones; probabilidades por etapa, fracciones y pertinencia de FPC; qué variabilidad de calibración/no respuesta deben reproducir los pesos; corrección del bootstrap n_h para el diseño realmente empleado; singleton de certeza o política de varianza fundada; tratamiento predefinido de denominadores cero; y demostración de cobertura nominal en poblaciones/diseños declarados. Fuentes locales disponibles para empezar: specs humanas de los paquetes lote1, cuestionarios/FD entregados y contratos spec.yaml; no contienen por sí solos prueba de cobertura. La fuente faltante debe ser documentación técnica INEGI o decisión inferencial firmada, no el productor elegido por coincidencia.

Para consumidores: no usar estos IC como prueba de diferencias entre segmentos, cambios temporales o signo concluyente. No está probado que cambie una conclusión pública; sí cambia la incertidumbre disponible y puede cambiar publicación cerca de CV/ancho. El carril P2 adjudica esas fronteras separadamente. El protocolo nuevo permite decidir si se autoriza una comparación de leyes y un estimador de varianza defendible futuro; su referencia empírica es diagnóstica, no sustituto automático de la documentación del diseño.

EJECUTADO: 14 pruebas sintéticas completas (ley binomial exacta, orden, pesos, semilla fija, singleton, ceros de dominio, marco ampliado, denominadores cero, percentil lineal, fronteras CV/ancho/soporte, punto cero, guardias). LEÍDO: replays congelados del acto anterior, 9/9 idénticos, sin repetirlos. NO-CORRIDO: nuevos contrastes históricos del protocolo propuesto, atribución causal cuantitativa y cobertura nominal. No hay recertificación ni cambio de tolerancia.
