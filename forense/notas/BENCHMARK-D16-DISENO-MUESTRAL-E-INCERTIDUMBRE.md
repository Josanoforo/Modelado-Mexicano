# D16 · Diseño muestral incompleto e incertidumbre

Fecha: 10 de septiembre de 2026. Benchmark solicitado por mesa. Propuesta para FP-371 / DIN-M-01; no adjudica ni modifica cálculos sellados.

**Principio: disponer del punto ponderado no demuestra que se conozca su margen de error.**

## 1. Problema concreto verificado

**Observado:** FP-371 distingue expresamente el punto de DIN-M-01 de su EE/IC. La aproximación discutida usa estrato constante y folio como UPM. FP-370 no autorizó esa aproximación como referencia inferencial. El cálculo vigente citado es CALC-R-DIN-M-01-v4. [Firma pendiente](https://github.com/Josanoforo/Modelado-Mexicano/blob/e81aa27bf3999989fc029a18e49352f27088e230/forense/firmas-pendientes.tsv).

**Interpretación:** folio identifica un hogar para enlazar información; no prueba que represente el conglomerado primario de selección. Repetir un bootstrap correctamente programado sobre una unidad equivocada no identifica el diseño verdadero.

**Consecuencia:** recuperar metadatos o una alternativa oficial, y mantener separadas la estimación puntual descriptiva y la inferencia aproximada. La documentación ENNViH de muestreo citada por el repo es una pista para adquisición; en este benchmark no se obtuvo una confirmación externa nueva de los identificadores de diseño del archivo concreto.

## 2. Comparación de prácticas documentadas

| Fuente primaria | Qué aporta | Consecuencia para DIN-M-01 |
|---|---|---|
| CDC/NHANES, *Variance Estimation* | Los pesos afectan las estimaciones; estratificación y conglomeración afectan la varianza. NHANES publica unidades enmascaradas aptas para el análisis. | Buscar variables o réplicas oficiales. Una unidad enmascarada suministrada por el productor no equivale a inventar una UPM a partir del folio. [Tutorial](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx). |
| Lumley, documentación de `svydesign` | El diseño combina identificadores de muestreo, estratos, pesos y, cuando corresponde, correcciones de población finita. La identificación/anidación debe ser correcta. | Auditar correspondencia, duplicados y faltantes al construir el objeto de diseño. [Referencia](https://r-survey.r-forge.r-project.org/pkgdown/docs/reference/svydesign.html). |
| Lumley, *Lonely PSUs* | Una UPM única no seleccionada con certeza carece de un estimador insesgado ordinario de esa contribución. Tratarla como certeza, ajustar o combinar estratos son supuestos distintos. | No llamar “conservador” a asignar varianza cero por defecto. Las opciones de software no recuperan conglomerados desconocidos. [Documento](https://r-survey.r-forge.r-project.org/survey/exmample-lonely.html). |
| Lumley (2004), *Analysis of Complex Survey Samples*, Journal of Statistical Software | Presenta análisis mediante información de diseño o pesos replicados y aproximaciones por linealización o replicación. Se consultó el resumen del editor. | Base académica de las rutas disponibles; el algoritmo por sí solo no sustituye metadatos. [Artículo y DOI](https://www.jstatsoft.org/article/view/v009i08). |
| Parker y colaboradores, NCHS (2017, actualización 2021) | El informe aborda presentación de proporciones, tamaño efectivo y situaciones extremas, con referencias a Korn–Graubard. | Diferenciar precisión de tamaño bruto. Sus umbrales de publicación son institucionales; no se trasladan automáticamente al programa. [Informe completo](https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf). |

El informe NCHS se leyó en texto completo; de los artículos Lumley (2004) y West et al. (2008, citado en D11) se consultaron los resúmenes editoriales. No se afirma haber realizado una revisión exhaustiva de todos los métodos ni haber leído los papers citados indirectamente por esas fuentes.

## 3. Rutas, ordenadas por lo que permiten afirmar

| Ruta | Requisito | Uso defendible |
|---|---|---|
| Diseño real o variables públicas oficiales para varianza | Confirmación de ola, población, pesos, estratos y UPM; tratamiento documentado de unidades especiales | Inferencia basada en el diseño, con sus supuestos y límites declarados. |
| Pesos replicados oficiales | Réplicas entregadas por el productor y especificación de método, escala y grados de libertad | Inferencia conforme al procedimiento oficial; no exige reconstruir identificadores restringidos si el productor avala esta vía. |
| Información parcial + diseño aproximado | Supuestos explícitos, comparación de alternativas plausibles y alcance restringido | Sensibilidad exploratoria. No se presenta como margen de error certificado. |
| Sólo pesos y variables de respuesta | Integridad del peso, universo y enlace verificada | Punto ponderado descriptivo; falta justificar una inferencia de diseño. |

No son estados nuevos del registro: son condiciones que se escriben en la spec, el RESULT y su uso.

## 4. Correcciones y casos límite

**Hogar no es automáticamente UPM.** Si distintos hogares comparten conglomerado, remuestrear hogares como independientes puede omitir dependencia entre ellos. Sin los identificadores no sabemos cuánto. Tampoco se puede garantizar el sentido neto del error al omitir simultáneamente estratificación y conglomeración. Esta es una inferencia metodológica de la estructura del problema, no una medición del sesgo de este archivo.

**UPM única no significa certeza.** Certeza se acredita por selección/diseño, no por observar una sola unidad. Si un procedimiento heredado llama “conservador” a suprimir una contribución de varianza sin ese fundamento, se debe corregir la explicación en una nota sucesora. No se borran ni resellan resultados históricos. [Tratamientos diferenciados](https://r-survey.r-forge.r-project.org/survey/exmample-lonely.html).

**Dominios y saltos.** Personas elegibles para cr27 forman un dominio; hay que conservar la información necesaria del diseño completo. Un faltante de diseño en un registro incluido no se elimina en silencio para producir un intervalo. Ponderadores de otra ola o de un panel retenido requieren demostrar su correspondencia con la población objetivo.

**Identificadores repetidos.** Una UPM con el mismo código en dos estratos puede representar unidades diferentes. Verificar el anidamiento. Un `folio` útil para el join sigue teniendo una función distinta del identificador de diseño. [Contrato de `svydesign`](https://r-survey.r-forge.r-project.org/pkgdown/docs/reference/svydesign.html).

**Proporciones extremas.** El Wald simétrico puede salir de [0,1]; tampoco basta recortarlo. La documentación de `svyciprop` ofrece métodos alternativos, pero advierte limitaciones cuando la proporción es exactamente cero o uno. El método y la salida para esos casos se fijan antes de ejecutar. [Documentación](https://r-survey.r-forge.r-project.org/pkgdown/docs/reference/svyciprop.html).

**Sensibilidad con DEFF.** Se pueden mostrar escenarios explícitos de inflación de varianza; no estiman el DEFF real ni reparan la falta de diseño. No elegir el escenario que dé el veredicto deseado.

**No mezclar incertidumbres.** La variación entre respuestas de un LLM, el remuestreo de celdas de una evaluación y el error muestral de la encuesta R son niveles distintos. Ocho capturas por celda no crean ocho encuestas ni ocho celdas independientes. Una mejora futura de R no altera por sí sola el árbitro congelado de la comparación actual.

## 5. Encargo de adquisición y prueba

**Objeto:** resolver la disponibilidad del diseño de DIN-M-01 y producir la mejor inferencia sustentable, preservando su cálculo anterior.

**Entradas:** FP-371; CALC-R-DIN-M-01-v4 y manifiesto de sus insumos; documentación ENNViH citada en el expediente; este benchmark; recetas ya registradas. Revisar el enlace por folio/identificador de persona, `cr27`, respuestas válidas y factor `fac_3b` contra la spec efectiva antes de implementar.

**Pasos:**

1. Buscar primero en el corpus y sus metadatos estratos, UPM, ponderador correcto, réplicas y manual de varianza. Identificar archivo/ola/población; una mención de “diseño complejo” no basta.
2. Si faltan, llevar la demanda exacta a SONDA/adquisición: variables o pesos replicados oficiales y método aplicable, incluyendo si existe una versión pública enmascarada. Reutilizar solicitudes documentadas.
3. Si llega el diseño, congelar una spec sucesora. Verificar enlaces sin multiplicación de filas, faltantes de diseño, unidades por estrato, pesos y grados de libertad. Reproducir el punto cuando el estimando no haya cambiado y explicar cualquier diferencia.
4. Contrastar la incertidumbre con una implementación de referencia del mismo diseño. Usar fixtures de dominio, UPM única y agrupación entre hogares para comprobar que el procedimiento responde al diseño.
5. Si no llega, entregar el punto y sensibilidades identificadas como aproximadas, con la evidencia del bloqueo. No sustituir una variable inexistente por un identificador cómodo y declarar la reserva resuelta.

**Criterio de cierre:** el encargo de búsqueda se cierra por sus resultados y alcance, incluso si determina inaccesibilidad. FP-371 sólo se resuelve cuando mesa acepta/rechaza un uso inferencial concreto, o cuando la aproximación deja de ser necesaria por un sucesor con diseño acreditado y se documenta esa sucesión.

## 6. Recomendación a mesa

Mantener disponible el punto ponderado y avanzar de inmediato la recuperación del diseño. Mientras tanto, tratar cualquier EE/IC con folio y estrato constante como sensibilidad aproximada, fuera del papel de referencia inferencial. Esto es una recomendación derivada del benchmark; la solicitud D16 autorizó investigar, no firmó todavía su adopción.

No hace falta paralizar la evaluación que utiliza el punto de R: FP-371 declara que no la bloquea. Sí hace falta una spec prospectiva si la próxima comparación incorpora la incertidumbre de R a su veredicto.
