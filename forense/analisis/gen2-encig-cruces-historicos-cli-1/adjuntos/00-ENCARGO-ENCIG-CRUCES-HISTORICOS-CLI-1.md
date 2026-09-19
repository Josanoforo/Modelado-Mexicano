# GEN2-ENCIG-CRUCES-HISTORICOS-CLI-1

## Mandato y autoridad

Ejecuta el brief de dirección adjunto, aprobado por mesa según su cabecera: mide los tres cruces históricos de ENCIG 2023 y, si es documentalmente comparable, ENCIG 2021. Produce CALC, incertidumbre conjunta y aplicación mecánica de la regla de elección. No ejecuta el piloto 3 ni abre ENCIG 2025. Este texto desarrolla la implementación; no reemplaza ni amplía las firmas del brief.

Repositorio Josanoforo/Modelado-Mexicano. CAJA local, una sesión y un worktree, rama sugerida `codex/gen2-encig-cruces-historicos-cli-1`, desde origin/main actualizado. Reporta ruta absoluta, rama, HEAD y estado antes de editar. Lee AGENTS.md e instrucciones aplicables. Autorizados commit, push y PR sin merge. No gobierno, motor ni adopción. Mantén contador PENDIENTE-DE-MESA salvo firma vigente explícita que realmente corresponda a este objeto.

Base del brief y de la revisión técnica: `8e455bd6a3870566d6776fef19834c4da16d2fa9`. Re-deriva el estado actual, comprueba trabajo equivalente en main y ramas activas y evita duplicarlo. Los anteriores encargos ENIGH, ENUT, ENFIH, ENCUCI, ISSP y CRON siguen separados; ninguno es dependencia de este cálculo. La emisión C2 compuesta pertenece a Claude; su trabajo no bloquea esta medición histórica.

Archiva verbatim este encargo y los cuatro adjuntos, con SHA-256 y procedencia. Careo esperado: `796689c4dce6f43d31892b1972e774562a8fb649bd6481adbfd72607bdf256bc`. Los diseños A/B son antecedentes: en conflictos manda el brief aprobado, después el careo aprobado; no mezcles umbrales de los diseños descartados.

## P0. Contrato y congelamiento

Lee CALC-PISOS-ENCIG2023-EJES-0002/spec.*, medidor.py, resultados/sello y la tabla PISOS-REJILLA-arbitro-metadatos-v1_0.tsv. Son insumos de solo lectura. Verifica los payloads de manifiesto `encig23_base_datos_csv` y `encig2021_csv` con corpus compartido y hashes. Documentación primero: cuestionario, FD, unidad, FAC_TRA, estrato/UPM, llaves, catálogos y temporalidad. Una ruta sin configurar no prueba ausencia del payload.

Congela en COMMIT-1, antes de abrir respuestas de cualquier ola: spec humana y YAML por CALC, código propio completo/hash, contrato de la regla reproducido verbatim, categorías, tratamiento de faltantes y casos degenerados, método de incertidumbre y pruebas sintéticas. Propuestas de IDs, sujetas a unicidad: CALC-ENCIG2023-CRUCES-HISTORICOS-0001 y CALC-ENCIG2021-CRUCES-HISTORICOS-0001. Un archivo de resultados de selección derivado debe declarar los CALC exactos que consume y sus sellos; no introducir dependencia circular.

El primer resultado que produzca este procedimiento es el que se reporta. Si necesitas una ejecución diagnóstica, declárala antes, indicando exactamente qué verifica y qué no mira. No recalibrar cortes, semilla, método o regla después del dato. Conserva intentos y sigue la sucesión vigente ante defecto material; no modificar CALC-PISOS ni sellos históricos.

## P1. Universo 2023 y rejilla

Mismo universo del piso: N_TRA normalizado == 1 y P7_3 válida en {1,2,4,5,6}; evento {4,5}; FAC_TRA positivo y diseño válido. Unidad trámite. Verifica el significado documental de N_TRA y no lo interpretes como conteo de trámites de una persona por su nombre.

El medidor sellado une `encig2023_04_sec_7.csv` a residentes `encig2023_02_residentes_sec_2.csv` por ID_PER, m:1. Conserva cardinalidad, informa faltantes y no duplica personas para llenar celdas. Diseño mediante EST_DIS/UPM_DIS, llaves textuales; cualquier normalización debe quedar declarada y no fusionar identificadores distintos.

Rejillas heredadas, sin colapsos oportunistas:

- Sexo: códigos 1/2 según catálogo.
- Edad: 18–29, 30–44, 45–59, 60–96. El piso etiqueta la última 60+, pero el código excluye edades >96; conserva el límite efectivo y decláralo. No meter 98/99 al último tramo.
- Escolaridad: hasta_primaria, secundaria, media_superior, superior. El mapa de NIV del medidor es {0,1,2}/{3}/{4,5,6,7}/{8,9}. Acredita el catálogo y su correspondencia con esos agregados; no llamarlos categorías nativas si son agrupaciones. Una discrepancia material contra el documento produce PARO con evidencia; no corregir el piso fuera de alcance.

Tres cruces completos: sexo×edad (8), sexo×escolaridad (8), edad×escolaridad (16). Conservar celdas vacías y desconocidos separados, no reasignarlos. Congela orden canónico e identidades de cada celda.

## P2. Coherencia de universos y marginales

Por cada cruce informa cuántos trámites y qué masa se pierden por cada eje inválido. Calcula controles marginales sobre el universo exacto de cada eje del piso, y reconstruye esos controles desde celdas conjuntas más residuos explícitos del otro eje desconocido. No compares una media de casos completos contra otra con cobertura distinta ni toleres la discrepancia como redondeo.

Para calcular δ del cruce, p(a,b), p(a), p(b) y p deben tener un universo común y documentado. Comprueba que los marginales reconstruidos desde la rejilla sustantiva reproducen los puntos y denominadores sellados exigidos por el brief. Congela tolerancia justificada a partir de la precisión publicada antes de mirar respuestas; no ampliarla para conseguir coincidencia.

Si solo coincide al añadir residuos fuera de rejilla, distingue: el control del lector pasó, pero la coherencia de universo de la rejilla exigida por el brief no. Aplica su PARA: preserva el diagnóstico y pide definición a dirección para ese cruce; no sustituir silenciosamente los marginales, imputar categorías o emitir un δ incompatible. Se puede continuar con cruces independientes que sí satisfagan el contrato, sin elegir ganador mientras una ambigüedad material impida comparar todos los candidatos.

## P3. Estimación conjunta y precisión

Para cada celda publica un RESULT por cantidad: n de trámites; personas distintas; personas con evento y personas sin evento; numerador y denominador ponderados; p, EE e IC95; δ, EE e IC95; número de réplicas válidas y causa de no estimación cuando corresponda.

Una persona puede tener trámites con y sin evento: esos dos conteos de personas pueden solaparse. No exigir que sumen personas distintas. Añade el solapamiento como control si aparece, sin cambiar la unidad del estimando.

δ = logit p(a,b) − logit p(a) − logit p(b) + logit p.

Fija un plan de réplicas de diseño compartido por TODOS los marginales y los tres cruces de una ola. Recalcula los cuatro términos de δ en cada réplica. Respeta estratos, UPM, FAC_TRA y dependencia de trámites de una persona: conserva conjuntamente sus registros al remuestrear UPM, verificando pertenencia coherente al diseño; no añadas un segundo bootstrap independiente de filas/personas. Conserva marco de diseño al estimar dominios. Documenta singleton, semilla, generador, número de réplicas y definición exacta de EE/IC.

No usar clipping, pseudocuentas ni suavizado para hacer existir logit. Probabilidad puntual 0/1, denominador cero o diseño insuficiente se reportan con causa; conserva p cuando sea estimable y deja δ o precisión sin número cuando no lo sean. No eliminar silenciosamente réplicas con logit infinito y presentar su distribución restante como IC incondicional. Congela el tratamiento de estas degeneraciones antes de medir. Un puntaje no definido no se convierte en cero ni infinito para ordenar candidatos: selección pendiente de regla aplicable, distinta del resultado SIN-PODER-DE-FALSACION.

Guarda réplicas AGREGADAS o un artefacto equivalente reproducible de covarianzas/δ que permita propagar incertidumbre histórica después. Nunca filas de microdatos ni identificadores de personas en Git. No estimar todavía S½, Sλ, R ni emisiones de 2025.

## P4. ENCIG 2021, primero comparabilidad documental

Cita texto de cuestionario y FD para el desenlace, códigos, N_TRA, periodo, ponderación y categorías demográficas de 2021; no basta igualdad del nombre P7_3. Si coincide materialmente, mide los mismos tres cruces en CALC separado con el mismo contrato conceptual. Si hay incompatibilidad, declara NO-CONSTRUIBLE por ola/cruce con la diferencia concreta; no adivines una recodificación puente. Un faltante de fuente/documentación no se rotula ausencia del fenómeno.

No fabricar correspondencia entre UPM de olas distintas por tener códigos parecidos. El desempate de signos usa puntos comparables, no requiere asumir un panel de personas. Cualquier comparación con incertidumbre entre olas exige documentar la dependencia; no se agrega a este encargo por inercia.

## P5. Ejecutar la regla aprobada y declarar sus límites

Incluye verbatim §2 del brief en la spec. Conserva elegibilidad de soporte: TODAS las celdas con n2023≥200 trámites sin ponderar. Sin rescatar categorías ni excluir celdas para puntuar. Publica elegibilidad de cada cruce, puntaje media no ponderada de |δ|/EE, lista de candidatos y comparación del empate relativo <10% del mayor.

El desempate aprobado usa concordancia de signo 2021–2023 cuando 2021 sea construible; fija antes de los datos su cómputo sobre TODAS las celdas comparables de cada cruce, sin seleccionar significativas, y declara signo cero aparte. Si no puede compararse simétricamente la concordancia entre los candidatos, no inventes una ventaja por cobertura. Sin 2021, usa menos celdas tal como manda el brief.

El brief no resuelve todas las ramas del algoritmo: ninguno elegible, puntajes degenerados, empate que persiste entre las dos rejillas de ocho celdas, o concordancia empatada. No añadas como firma de mesa una prioridad lexicográfica, sorteo o preferencia de instrumento. En esos casos entrega resultados completos y `SELECCION-PENDIENTE-DE-REGLA`, con conjunto candidato y causa; no abras la ola reservada. Distingue explícitamente `NINGUN-CRUCE-ELEGIBLE-POR-SOPORTE` de la ausencia de señal en un cruce elegido.

Cuando exista ganador inequívoco, aplica exclusivamente a él la condición aprobada: ninguna celda con IC95 de δ que excluya 0 → `SIN-PODER-DE-FALSACION`. No rescatar el segundo clasificado porque tenga una celda significativa. Ese token es el criterio operativo de mesa para no lanzar el piloto; NO acredita un cálculo formal de potencia ni equivalencia de δ con cero. La selección entre múltiples celdas/cruces también impide presentar un IC puntual significativo como evidencia confirmatoria independiente. No cambiar a Bonferroni ni introducir un umbral nuevo sin nueva decisión; explica el alcance exploratorio de esta selección histórica.

## P6. Guardias, publicación y cierre

Allowlist explícita de payloads/documentación de 2021/2023. Test negativo de insumos para cualquier alias, versión o archivo que corresponda a ENCIG 2025, además de patrones encig25/encig_2025. Resolver manifiesto y verificar año/identidad, no solo prefijo. No abrir 2025 ni para bandas; no leer resultados reservados a través de otro artefacto.

Pruebas materiales: cardinalidad del join, particiones/residuos, reconstrucción ponderada por NUM/DEN (nunca promedio simple de tasas), δ calculado con réplicas compartidas, identidad de celdas, soporte y ramas de empate/degeneración. Contrasta un punto y una varianza con cálculo independiente focalizado. La prueba de selección usa datos sintéticos y no condiciona el código a resultados observados.

Escritura autorizada: CALC nuevos, specs en forense/prereg-caja, `tools/encig_cruces_historicos.py` y su test, análisis/nota propios, archivo verbatim de encargo/adjuntos con hashes, asientos propios de replay y derivados por comandos existentes. `corridas.tsv` se genera por comando, no a mano. No tocar gobierno, milpa, marcador, corrida0.py, tests/check.py ni CALC-PISOS. No abrir auditoría general; presupuesto de auditoría aproximado 20% salvo riesgo material.

Sella, ejecuta replay dirigido, registra por interfaces vigentes y comprueba estabilidad de segunda proyección. No aceptar replay ajeno mediante --lote. Un bloqueo externo de registro se informa con evidencia y resultado conservado, sin afirmar publicación exitosa ni consumo activo.

PR sin merge: tablas 2023/2021, comparabilidad, control de coherencia, réplicas agregadas/precisión, RESULT de selección o su límite exacto, contratos/código/sellos/replay y lectura sustantiva. Primera línea de la nota: universo, unidad trámite, escala de proporción/logit y evidencia clase (a). Incluye `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO`, adjuntos y hashes, pruebas, URL y SHA. Interacciones son residuos descriptivos; no efectos causales ni psicología de grupos. ENCIG 2025 y sus tres cruces permanecen RESERVADA. El siguiente acto de IC de C2 sigue diferido a su encargo propio tras la fusión de C2-COMPUESTO-RESERVADAS-1.
