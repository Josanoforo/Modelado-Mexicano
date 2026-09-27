# Psicología de la migración México–Estados Unidos: hogares, separación, aspiraciones y bienestar

Versión editorial v2 · ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1 · corte 26/sep/2026. Propuesta para revisión de mesa; no aceptación independiente ni adopción de reglas. El título del archivo conserva la identidad del original; el análisis distingue olas históricas de literatura publicada después. No se abrieron microdatos ni reservas. Decisiones y tablas reproducibles: [migracion](../../forense/analisis/reports-v2/cuidado-migracion-pareja-1/migracion/).

## 1. Resumen ejecutivo

1. **Sólido y útil:** recepción de remesas, flujo de emigración, stock en destino y retorno son unidades diferentes. Una operación financiera no identifica una familia ni una persona migrante.
2. **Sólido descriptivo:** R1 mide concentración del ingreso por remesas entre hogares receptores en una ola abierta histórica. No mide gasto, solidaridad, protección suficiente ni desarrollo local.
3. **Malinterpretado:** la existencia de una remesa no demuestra que se conserve un vínculo afectivo funcional; su ausencia tampoco demuestra abandono.
4. **Útil:** separar a quien sale, familiares que permanecen y personas retornadas. Una misma trayectoria puede producir experiencias distintas dentro del hogar.
5. **Matizado:** la separación aparece como problema en entrevistas de una localidad maya de Yucatán (Y1); no está demostrado que sea el núcleo psicológico de toda migración mexicana.
6. **Matizado:** cuidado, comunicación y escuela aparecen como recursos en Y1. Son mecanismos compatibles y prioridades de investigación; su eficacia preventiva no está identificada.
7. **Malinterpretado:** «cultura de migración» y cálculo de oportunidades no son explicaciones excluyentes. K1 respalda aspiraciones transmitidas en redes dentro de comunidades estudiadas, sin probar una esencia nacional.
8. **Matizado:** retorno puede cambiar expectativas y relaciones; no hay en esta entrega una tasa de cambio identitario ni de gustos del retornado mexicano.
9. **Sólido en su alcance:** U1 registra preocupación por autoridades migratorias en familias de Estados Unidos, incluidas familias enteramente ciudadanas. Rompe la exclusión del original «no aplica a documentados/ciudadanos».
10. **Malinterpretado:** preocupación declarada por adultos no equivale a diagnóstico infantil de depresión o TEPT. U1 comprende familias de distintos orígenes, no exclusivamente mexicanas.
11. **Sólido documental:** I1 confirma un impuesto estadounidense sobre ciertos instrumentos usados para financiar remesas. El instrumento de fondeo importa; la marca del proveedor o una interfaz digital no bastan.
12. **Sin efecto identificado:** I1 no demuestra aceleración de bancarización, ventaja de una fintech ni desplazamiento hacia stablecoins. La recomendación comercial del original pierde ese fundamento causal.
13. **Sin cifra firme:** se retiran cantidades macroeconómicas, stocks, cifras clínicas y rankings administrativos cuya fuente primaria exacta no fue leída. La retirada no los refuta.
14. **Útil para decidir:** diseñar servicios según barreras observadas y necesidades expresadas, y evaluar su uso y resultados. No asignar propensiones psicológicas por nacionalidad.

## 2. Marco conceptual y unidad de análisis

Una familia puede repartir trabajo, dinero y cuidado entre localidades. «Transnacionalismo» y «remesas sociales» nombran hipótesis sobre vínculos y circulación de prácticas; no garantizan simultaneidad cotidiana, igualdad de poder ni cambio progresista. La capacidad de visitar, recibir dinero, acreditar identidad y acceder a servicios depende de ingreso, documentación y oferta institucional.

Las redes pueden transmitir información y expectativas. El resumen de autores de Kandel y Massey (K1, lectura limitada al resumen institucional) relaciona exposición familiar a migración con aspiraciones escolares y migratorias. Esa lectura permite conservar el problema regional, sin reclamar lectura del artículo completo ni magnitudes de efecto. Redes también pueden reproducir normas y restricciones: adaptación económica y significado cultural pueden interactuar.

Duelo migratorio, duelo ambiguo y síndrome de Ulises son marcos, especialmente (c) cuando se importan de contextos europeos. Este report no los usa como diagnósticos ni estima su prevalencia. El riesgo de una familia en origen requiere conocer duración de la separación, calidad y continuidad del cuidado, recursos y trayectoria previa; no basta saber que un miembro salió.

Se distingue descripción (R1), percepción cualitativa (Y1), asociación/experiencia declarada (U1), mecanismo hipotético y propuesta de intervención. Ninguna cifra aquí identifica el efecto causal de emigrar, retornar o recibir remesas. Hofstede, GLOBE y puntuaciones nacionales de valores no permiten asignar rasgos a hogares migrantes. Asimilación/aculturación describe dimensiones en destino, pero no sustituye la medición del origen, retorno o movilidad repetida.

## 3. Mapa de evidencia: frecuencia y mecanismo separados

| Evidencia | Procedencia y población | Qué sostiene | Tier de frecuencia / mecanismo |
|---|---|---|---|
| R1, ENIGH2020 | (a), hogares receptores en México | Concentración del ingreso por remesas | Descriptivo de ola / no identificado |
| Y1, investigación cualitativa rural | (a), participantes de Tunkás, Yucatán | Experiencias de separación, supervisión, comunicación y apoyo | No estima frecuencia / compatible, exploratorio |
| U1, WBNS diciembre2025 | (b), adultos en hogares de Estados Unidos de diversos orígenes | Preocupación también fuera del estatus indocumentado | Encuesta de su universo / causalidad no identificada |
| I1, comunicación IRS abril2026 | Norma externa, no tier psicológico | Alcance por instrumento de fondeo | No aplica / no estima comportamiento |
| K1, resumen autoral de estudio2002 | (a), estudio regional mexicano, acceso parcial | Problema de aspiraciones y redes | Magnitudes no usadas / asociación regional |

<!-- CIFRAS:INICIO -->

| RESULT y estado | Estimación histórica | Denominador y alcance |
|---|---|---|
| `RESULT-ENIGH20-REMINT-PARTICIPACION-GE50` · ADOPTADO Firma M; validación independiente pendiente | 17.49% (IC95 16.15–18.80%) de hogares con remesas equivalentes al menos a la mitad del ingreso corriente | hogares receptores con remesas>0 e ingreso corriente válido>0; ponderador factor de hogar; ENIGH2020; no todos los hogares mexicanos, personas migrantes ni gasto; bootstrap UPM dentro de estrato |

<!-- CIFRAS:FIN -->

R1 conserva la adopción por Firma M en `data/corrida0/decisiones.tsv`, objeto `CALC-ENIGH2020-INTENSIDAD-REMESAS-0001`, 24/sep/2026, frente a una vista de consulta que aún muestra PENDIENTE-DE-MESA. El catálogo v1.2 lo rotula ADOPTADO. Reproducción, validación independiente y adopción son preguntas distintas: C1 lote2 tiene esta identidad pendiente de ejecución. La tabla de efectos de #1184/lote1 no contiene su llave; ello no equivale a validación independiente favorable. Se usa para descripción histórica, sin adopción nueva ni consumidor de motor.

## 4. Patrones principales

### Separación, recursos y continuidad del cuidado

**Descripción:** Y1 recoge dificultades emocionales y de supervisión en participantes de una localidad rural maya. **A favor:** jóvenes, padres y docentes narran vínculos entre ausencia, carga del cuidador y malestar. **En contra/límite:** el diseño cualitativo seleccionado no tiene contrafactual ni mide prevalencia; mezcla migración interna e internacional. **Segmentos:** cuidado actual, comunicación, duración y trayectoria previa son condiciones a indagar, sin ordenar riesgos nacionales. **Causas compatibles:** demanda de trabajo, separación y capacidad del cuidador; no se separan sus efectos. **Riesgo:** diagnosticar por parentesco migrante o culpabilizar a la madre. **Implicación:** escuchar a jóvenes y cuidadores y evaluar necesidades concretas antes de elegir servicios.

### Remesas como ingreso y posible dependencia

**Descripción:** R1 describe hogares receptores con alta participación de remesas en ingreso. **A favor:** hace visible heterogeneidad dentro de quienes reciben; una media agregada no representa a cada hogar. **En contra/límite:** ingreso no identifica gasto, suficiencia ni estabilidad; educación y vivienda pueden tener rendimientos futuros. **Segmentos:** receptor/proveedor, regularidad, otras fuentes de ingreso y costos de cobro deben distinguirse. **Causas compatibles:** oportunidades de ingreso y arreglos familiares, no «cultura de gasto». **Riesgo:** llamar seguro efectivo a cualquier transferencia o inferir subdesarrollo por recepción. **Implicación:** evaluar exposición a interrupciones y barreras de cobro sin prometer bienestar causal.

### Aspiración y redes

**Descripción:** K1 conserva una asociación situada entre redes familiares y expectativa migratoria. **A favor:** el resumen autoral presenta transmisión social de aspiraciones. **En contra/límite:** no se leyó texto completo; no se transporta a México2025, tercera generación ni todas las regiones. **Segmentos:** acceso a redes y alternativas escolares/laborales, antes que etiqueta estatal. **Causas compatibles:** información, retorno esperado y norma social. **Riesgo:** reducir el comportamiento a pobreza o a cultura por decreto. **Implicación:** información sobre opciones reales y costos, con evaluación de decisiones y continuidad educativa.

### Amenaza migratoria y acceso a servicios

**Descripción:** U1 registra temor en Estados Unidos también en hogares sin miembros indocumentados. **A favor:** contradice directamente la exclusión categórica de ciudadanos del original. **En contra/límite:** preocupación adulta autorreportada no es diagnóstico ni efecto específico en niños mexicanos; exposición y selección pueden confundir asociaciones. **Segmentos:** estatus familiar, exposición local y experiencias previas; la nacionalidad no basta. **Causas compatibles:** amenaza directa, temor por allegados y trato percibido. **Riesgo:** interpretar evitación como desconfianza cultural innata. **Implicación:** estudiar barreras y minimización de datos que realmente reduzcan obstáculos, sin reclamar eficacia demostrada.

### Retorno y reconstrucción de relaciones

**Descripción:** volver puede exigir documentación, acceso escolar, empleo y renegociación familiar. **A favor:** los mecanismos de cambio son coherentes con trayectorias y circulación de prácticas. **En contra/límite:** no hay aquí estudio específico leído que sostenga la tipología adaptativa/restaurativa/transformativa ni porcentaje sin documentos; se retiran esas afirmaciones firmes. **Segmentos:** retorno voluntario/devolución forzada, edad, tiempo fuera, red de apoyo y recursos. **Causas compatibles:** discontinuidad institucional y exposición previa. **Riesgo:** tratar al retornado como fracaso, consumidor sofisticado o beneficiario homogéneo. **Implicación:** diagnóstico individual de barreras, con seguimiento de reintegración.

## 5. Cultura, estructura y adaptación: cómo separar explicaciones

No se conservan pesos ALTO/MEDIO/MENOR del original. Para distinguir salario de redes se requieren cambios en oportunidades laborales con redes medidas antes de la salida. Para distinguir temor de precariedad económica en remesas se necesitan trayectorias de remitentes, empleo y exposición a enforcement; un agregado anual no basta. Para distinguir norma de cálculo económico en aspiración se requiere observar alternativas y expectativas comparables, no deducir motivación desde destino elegido.

Una prueba sobre bienestar debe medir condiciones previas, separación, ingreso, cuidado y resultado con unidades compatibles. Medición longitudinal mejora secuencia temporal; por sí sola tampoco elimina selección. La interpretación «adaptación racional» debe admitir información imperfecta, vínculos y desigualdad de poder, sin convertirse en explicación inmune al contraste.

## 6. Segmentación explícita

Registrar por separado origen/destino actual, trayectoria, documento de salida y estatus vigente; flujo/stock; remitente/receptor; edad, cuidado y género; contexto rural/urbano y lengua/comunidad; alternativas escolares y laborales; retorno planeado/forzado. No usar jefatura declarada como sustituto de autonomía ni escolaridad como estatus legal. Religiosidad puede ser dimensión de apoyo, pero no hay estimación aquí de su efecto migratorio.

La localidad maya de Y1 muestra por qué el centro-occidente no agota la investigación. No demuestra que toda población indígena decida colectivamente ni que un inventario parcial pruebe subrepresentación bibliográfica global. Intercensal2015 recibido para Edomex no representa a México. MOV034a/MOVEX02 tienen correcciones y exposición reservada documentadas en #1181; no se usan como piso psicológico ni se abren para completar este report.

## 7. Comparación internacional útil

La vecindad terrestre México–Estados Unidos contextualiza redes y posibilidades de viaje; no prueba circularidad universal vigente ni singularidad «sin paralelo». Separación, cuidado a distancia y restricciones laborales también son problemas posibles en otros corredores. No se conservan rankings de narrativa heroica, proporciones remesas/PIB de años distintos ni atribuciones de driver dominante a Filipinas o Centroamérica.

Una comparación defendible necesita la misma unidad, cohorte, desenlace y definición de retorno. Los modelos centrados en asentamiento en destino capturan parte de la experiencia, pero deben ampliarse cuando el objeto es hogar en origen o retorno. No inferir que un marco estadounidense sea falso solo por su origen; evaluar su correspondencia con la trayectoria observada.

## 8. Implicaciones aplicadas

Los servicios financieros deben comparar costo total, fondeo, cobro, acceso y continuidad. I1 indica una condición normativa externa; no acredita que una app específica sea más barata ni que el receptor esté bancarizado. Una interfaz digital y un retiro en efectivo pueden coexistir. Se retiran recomendaciones de proveedores y supuesta migración fuera del radar fiscal.

Para reintegración, estudiar barreras de identidad, credenciales, escuela y empleo de cada persona; el número de centros anunciado no mide cobertura o calidad efectiva. Para bienestar, diferenciar necesidades expresadas y evaluación clínica; no recomendar normalización como sustituto de atención ante síntomas. Para comunicación, preguntar por identidad y necesidades sin imponer mexicanidad uniforme ni convertir remesa en deber moral.

## 9. Mitos y sobreinterpretaciones corregidos

«Todos quieren emigrar»: no demostrado. «Recibir remesas protege a la familia»: ingreso no acredita protección. «La madre que migra abandona»: la salida no acredita intencionalidad ni calidad del vínculo. «La amenaza solo afecta a indocumentados»: ROMPE por U1. «Digital equivale a exento»: el fondeo y alcance normativo importan. «Deportado equivale a criminal»: categorías distintas; no se sostiene aquí la proporción de arrestados sin antecedentes ni comparaciones Biden/Trump sin tabla primaria comparable.

## 10. Síntesis y reglas SI–ENTONCES

El resultado es un mapa de trayectorias y condiciones, con descripción histórica limitada del ingreso por remesas y evidencia situada de experiencias. Las contradicciones sustantivas son recursos materiales frente a separación, pertenencia frente a barreras, y circulación de prácticas frente a continuidad de normas. La oportunidad es adaptar servicios a barreras medidas, no asignar un parámetro nacional de familismo o ansiedad.

**PROPUESTO-POR-EJECUTOR; sin adopción ni edición de motor:**

| Regla y consumidor posible | Condición / fundamento | Falsador y límite |
|---|---|---|
| SI un servicio atiende al hogar receptor ENTONCES separar regularidad y concentración del ingreso antes de ofrecer ahorro/crédito | Producto financiero; R1 descriptivo, entrevista directa al hogar | Retirar si la segmentación no mejora comprensión/uso frente a información simple; no fijar umbral de solvencia desde R1 |
| SI una escuela atiende jóvenes con separación parental ENTONCES evaluar cuidado, comunicación y apoyo con participación del joven | Diseño escolar; Y1 mecanismo exploratorio, aplicable tras diagnóstico local | Comparación prospectiva no mejora continuidad/apoyo o produce estigma; no presume diagnóstico |
| SI un servicio en destino detecta temor migratorio ENTONCES indagar exposición y barreras incluso en familias ciudadanas | Diseño de acceso; U1 en su universo estadounidense | Datos locales no muestran barrera o la intervención no mejora acceso; no transportar tasa a México |

No hay coeficientes conductuales nuevos. Estas propuestas requieren evaluación prospectiva y consentimiento operativo del consumidor correspondiente.

## 11. Auditoría final y literatura efectivamente leída

El registro `decisiones.json` cubre cada identidad del mapa y ocho tesis materiales adicionales. Cada decisión distingue ausencia de cifra de refutación. La ROMPE adicional fue revisada contra U1: rompe exclusivamente la exclusión por ciudadanía; no confirma ansiedad clínica. Los mecanismos centrales se revisaron contra diseños y límites: Y1 no identifica efecto causal; K1 solo tiene lectura parcial; R1 no mide uso de remesa; I1 no mide adopción tecnológica.

Las cifras principales del original sobre remesas2025, PIB, empleo, desplazamiento, deportaciones, stocks, costos mundiales y capacidad de programas quedan SIN-CIFRA en la tabla; no se rellenan desde instrumentos distintos. El estado legal de desplazamiento no se afirma sin verificar publicación/vigencia. Ninguna página pública autoriza ENIGH2024, ENUT2024 ni olas reservadas. No se reutiliza indiscriminadamente ENDIREH ni se convierte una discrepancia C1 en refutación automática.

Y1 y U1 no representan el mismo universo. Sus fuentes permiten formular límites y preguntas, no sumarlas. El corpus de esta entrega no permite describir al mexicano promedio, identificar diferencias nacionales frente a otros países ni medir toda la heterogeneidad indígena/rural. La revisión editorial es del ejecutor; la recepción independiente permanece pendiente.

- **Y1 (a), leído 26/sep/2026:** [Examining the effects of parental migration on youth mental health and substance use](https://pmc.ncbi.nlm.nih.gov/articles/PMC11130470/), 2024. Lectura de métodos, resultados y discusión (§2–4); selección comunitaria de Tunkás, entrevistas y grupo docente, migración interna/internacional; percepciones sin prevalencia ni identificación causal. Solo se usan sus resultados propios, no cifras de terceros citadas.
- **U1 (b), leído 26/sep/2026:** [Immigration Enforcement Affected Both Immigrant and Nonimmigrant Families Across the US in2025](https://www.urban.org/research/publication/immigration-enforcement-affected-both-immigrant-and-nonimmigrant-families), Bernstein, Gonzalez y Guelespe, 8/abr/2026. Leídos Key Takeaways y How We Did It; WBNS diciembre2025, adultos de Estados Unidos, hogares de diversos orígenes; temor declarado, sin diagnóstico infantil.
- **I1, documento normativo externo, leído 26/sep/2026:** [IRS IR-2026-48](https://www.irs.gov/newsroom/treasury-irs-issue-proposed-regulations-on-the-new-remittance-transfer-tax-established-under-the-one-big-beautiful-bill), 10/abr/2026, párrafos de alcance/vigencia y propuestas reglamentarias. La tasa legal es información externa, no RESULT ni evidencia de efecto financiero.
- **K1 (a), lectura parcial 26/sep/2026:** [Kandel y Massey, resumen autoral en Princeton](https://collaborate.princeton.edu/en/publications/the-culture-of-mexican-migration-a-theoretical-and-empirical-anal/), estudio2002, Abstract. No se leyó artículo completo; no se usan cantidades, coeficientes ni prueba de tercera generación. Conservado como antecedente acotado.

La literatura2025–26 añade un contraste material con U1 y precisión documental con I1; no se presenta como actualización exhaustiva. Productor y verificador regeneran tablas desde juicios explícitos y protegen cobertura, cifra/denominador, adopción y veto. No deciden dictámenes.
