# El clasemediero mexicano: identidad, posición y riesgo de caída — v2

Corte de lectura: `1eeb855272b933642177e3f32d51adc89f1009a0`; documental NUBE, sin microdatos. Contadores de medición movidos: cero. Dictámenes editoriales del ejecutor: revisión humana solicitada, no concedida. La tabla completa y sus exclusiones viven en [afirmaciones.tsv](../../forense/analisis/reports-v2/trabajo-movilidad-1/clase/afirmaciones.tsv). No se adopta ninguna regla ni se declara capacidad predictiva.

## Resumen ejecutivo

La clase media no puede representarse con una sola etiqueta psicológica. El original mezclaba recursos del hogar, percepción personal, pertenencia de mercado y seguridad económica. Esta versión conserva la pregunta sobre vulnerabilidad, pero separa qué se observa de qué mecanismo se propone.

1. **Sólido:** NSE AMAI clasifica hogares mediante recursos y características; no mide directamente ingreso, prestigio ni identidad. Su etiqueta no diagnostica temor.
2. **Sólido:** la distribución AMAI sellada de ENIGH abierta aporta composición de hogares. La cifra no constituye panel ni riesgo de descenso.
3. **Malinterpretado:** C-, C y C+ no forman una definición universal de clase media. El agrupador propio llama MEDIO a C-/C y ALTO a C+/A/B; conservar el nombre del agrupador evita reemplazarlo silenciosamente.
4. **Útil:** ingreso, NSE, autoposición y temor deben captarse por separado, con fecha y unidad.
5. **Sólido con alcance:** CEEY documenta persistencia intergeneracional de recursos y heterogeneidad regional y de género; también documenta ascensos. No permite decir que el origen determina todo destino.
6. **Malinterpretado:** baja movilidad intergeneracional no estima la probabilidad anual de perder clase media ni irreversibilidad de una caída.
7. **Hipótesis:** proteger estabilidad puede ser una respuesta a riesgos y restricciones. No identifica ansiedad individual ni acredita optimalidad de cada deuda o decisión educativa.
8. **Malinterpretado:** clientes endeudados de una empresa no son una muestra de mexicanos; un cociente de deuda acumulada e ingreso mensual no mide gasto corriente.
9. **Útil:** el crédito debe analizarse junto con costo, acceso, liquidez y obligaciones antes de atribuir búsqueda de estatus.
10. **Sólido con alcance:** Banxico encuentra asociaciones macroeconómicas con morosidad de sofipos; no mide la personalidad del deudor ni acredita la afirmación original de importancia sistémica del sector.
11. **No establecido:** prevalencia nacional de autoposición, temor, compra de protección, preferencias electorales o motivos de pagar escuela privada.
12. **Útil:** las propuestas de protección deben probar acceso y beneficio; riesgo material no basta para declarar demanda comercial enorme.

## Marco conceptual

**Ingreso:** flujo monetario o corriente, por hogar o por persona; requiere periodo, precios y ajuste por tamaño. Los deciles son posiciones relativas elegidas para describir una distribución: no constituyen por sí mismos una definición oficial de clase media. La seguridad económica exige además patrimonio líquido, obligaciones, redes y protección ante shocks.

**NSE:** clasificación de hogares basada en características observables. **Autoposición:** respuesta de una persona a una categoría, pregunta y escala concretas. **Temor a caer:** experiencia o expectativa individual que necesita medición propia. Ninguna de las primeras identifica la última mediante una traducción automática.

Psicología individual, scripts culturales, adaptación e instituciones son niveles distintos. “Dar a los hijos lo que uno no tuvo” puede organizar una narración familiar; el pago observado de una colegiatura no demuestra que ese guion haya causado la elección. Necesidad, seguridad, calidad educativa, localización y señalización siguen siendo explicaciones rivales.

## Mapa de evidencia y trazabilidad

Frecuencia y mecanismo tienen tiers separados. La composición AMAI tiene respaldo descriptivo **fuerte (a)** en hogares de su ola; el mecanismo temor → consumo tiene tier **hipótesis**, sin medida conjunta. Literatura primaria mexicana **(a)** de CEEY aporta asociaciones retrospectivas; Banxico aporta asociaciones agregadas de cartera, no tasas psicológicas individuales. No se consumen muestras de diáspora **(b)** para describir México. Ehrenreich, Hofstede, GLOBE y ansiedad de estatus son marcos importados **(c)**: se conservan como preguntas, no hechos nacionales ni fuentes primarias efectivamente leídas en este lote.

La [pregunta frecuente de AMAI](https://www.amai.org/NSE/index.php?queVeo=preguntas), apartados sobre definición y qué no es NSE, distingue bienestar del hogar de ingreso y prestigio. Consultada el 26/sep/2026; sin fecha editorial visible. Su regla considera escolaridad y componentes de equipamiento; esto permite segmentar recursos, no inferir estilos de vida ni estabilidad temporal.

La tabla siguiente deriva exclusivamente de registros por identidad, con valores redondeados para lectura. Unidad: porcentaje de hogares ENIGH 2022 con NSE válido; descripción RETROSPECTIVA, ninguna predicción. CALC `CALC-AMAI-NSE-ENIGH-2022-0001`; estado adoptado con reserva de instrumento por `FP-260924-GEN2-CLASE-AMAI-1-e773-01`. Vista de consulta atrasada: `consulta.py result` no encontró estas identidades; se cotejó objeto sellado, spec y firma. Hash de `resultados.json`: `c932ec88ca4b92aa38792719fcee580cef7f6b31f78f57a9e01a148ef32bfbe8`. No se modificó la vista.

| NSE | % hogares | RESULT / registro |
|---|---:|---|
| E | 8.7 | `RESULT-AMAI-NSE-ENIGH-2022-DIST-E-P` |
| D | 25.4 | `RESULT-AMAI-NSE-ENIGH-2022-DIST-D-P` |
| D+ | 14.9 | `RESULT-AMAI-NSE-ENIGH-2022-DIST-D+-P` |
| C- | 16.4 | `RESULT-AMAI-NSE-ENIGH-2022-DIST-C--P` |
| C | 15.3 | `RESULT-AMAI-NSE-ENIGH-2022-DIST-C-P` |
| C+ | 12.0 | `RESULT-AMAI-NSE-ENIGH-2022-DIST-C+-P` |
| A/B | 7.3 | `RESULT-AMAI-NSE-ENIGH-2022-DIST-A/B-P` |


Los faltantes de componentes y las reglas de validez están en la spec del objeto. No se interpreta esta distribución como toda persona ni se mezcla su denominador con votantes, matrícula escolar o cartera crediticia. El nivel C+ pertenece a ALTO en el agrupador sellado; una agregación alternativa debe identificarse como decisión analítica distinta.

## Patrones

### Identidad y posición: relación pendiente de medición conjunta

**Descripción:** es posible que autoposición y recursos no coincidan. **A favor:** sus definiciones observan cosas distintas. **En contra:** diferencia conceptual no acredita el tamaño ni dirección de la brecha. Las cifras de encuestas privadas originales quedan SIN-CIFRA porque no se leyeron aquí sus fichas primarias. **Segmentos:** edad, educación y localidad pueden cambiar las categorías de referencia, pero no se asignan gradientes sin cruce. **Causas rivales:** comparación social, interpretación de la pregunta, entorno local o posición económica. **Riesgo:** llamar aspiracional o fantasiosa a toda discrepancia. **Implicación:** preguntar categoría subjetiva junto con recursos y composición del hogar. **Falsador:** una medición conjunta representativa puede mostrar concordancia y refutar la generalización de disonancia mayoritaria.

### Seguridad material y temor: compatibilidad sin identificación

**Descripción:** ingreso discontinuo y obligaciones pueden volver costosa una pérdida de recursos. **A favor:** riesgos de crédito son compatibles con condiciones económicas. **En contra:** no hay estimando de miedo en este lote ni comparación que pruebe que prestaciones pesan más que salario. **Segmentos:** hogar con un perceptor, cuidados, activos y acceso a protección son dimensiones propuestas, no prevalencias medidas. **Causa:** restricciones institucionales, preferencias y estados emocionales pueden coexistir. **Riesgo:** declarar cualquier conducta óptima o patologizar a quien busca estabilidad. **Implicación:** revisar oferta y costo de protección, y medir bienestar y uso real. **Falsador:** manteniendo riesgo observado, una oferta accesible que no cambie temor/decisiones debilitaría ese mecanismo; no demostraría ausencia de necesidades.

### Consumo, educación y origen: canales distintos

**Descripción:** cada canal puede contribuir a posición o reconocimiento. **A favor:** recursos del hogar y escolaridad forman parte de la estratificación. **En contra:** el índice no cuantifica prestigio ni motivos; deuda no prueba apariencia y matrícula no prueba sacrificio. **Segmentos:** no se asigna consumo a jóvenes, credencial a profesionales y origen a piel clara sin datos conjuntos. **Causas rivales:** liquidez, calidad, disponibilidad territorial, discriminación o señalización. **Riesgo:** naturalizar el origen como destino o convertir tono de piel en causalidad biológica. **Implicación:** medir tratamientos discriminatorios y alternativas reales. **Falsador:** si la señal visible deja de predecir decisiones manteniendo recursos, se debilita su papel propuesto; no desaparece por ello la desigualdad.

### NSE entre olas: composición, no itinerario de hogares

**Descripción:** una distribución cambia cuando cambian composición, recursos o clasificación. **A favor:** el corte sellado describe hogares de su ola. **En contra:** no sigue a cada hogar; activos acumulados y educación tienen distinta sensibilidad al shock que el flujo de ingreso. **Segmentos:** rural/urbano debe conservar diseño e instrumento. **Causas rivales:** creación/disolución de hogares, renovación de bienes, error o cambio de regla. **Riesgo:** narrar movimientos C→C- o downgrade masivo desde saldos agregados. **Implicación:** sólo estimar transiciones con seguimiento válido o reconstrucción específicamente diseñada. **Falsador:** panel con pérdida de seguimiento auditada podría estimar frecuencia y reversibilidad; el presente corte no lo sustituye.

### Política: no derivar preferencias de etiqueta económica

**Descripción:** no se acredita homogeneidad ni volatilidad electoral individual. **A favor:** pertenencia económica y voto son constructos distintos. **En contra:** las salidas electorales del original no fueron leídas en su fuente primaria; una correlación no significativa no acredita efecto cero y resultados de alcaldías no identifican votantes. **Segmentos:** entidad, elección y definición de clase importan. **Causas rivales:** evaluación económica, oferta partidaria y preferencias. **Riesgo:** vender a la clase media como bloque opositor o gubernamental. **Implicación:** excluir aquí parámetros partidarios. **Falsador:** medición repetida individual y modelos con potencia declarada permitirían evaluar estabilidad y gradientes.

## Causas y actualización primaria dirigida

El [CEEY, presentación del Informe de movilidad social 2025](https://ceey.org.mx/wp-content/uploads/2025/07/PRESENTACION-Informe-de-Movilidad-Socia-en-Mexico-2025.pdf), diapositivas 6, 8 y 9, describe recursos de origen y destino en ESRU-EMOVI 2023. Reporta **50%** de permanencia en el quintil inferior entre quienes nacieron en él y **2%** de llegada al superior. Son porcentajes condicionados al origen, no riesgo de caída de la clase media ni probabilidad prospectiva. La presentación muestra heterogeneidad regional y de género. Eso MATIZA “origen es destino”; la irreversibilidad de una caída queda SIN-CIFRA porque no se observó recuperación posterior a un descenso. No identifica discriminación causal por tono. Fuente (a), consultada 26/sep/2026.

El [CEEY, informe sobre movilidad y cuidados 2026](https://ceey.org.mx/wp-content/uploads/2026/03/CEEY_Informe-de-movilidad-social-y-cuidados_2026.pdf) incorpora un módulo de cuidados a ESRU-EMOVI 2023 (introducción, pp. 8–9; diseño, p. 15). Se usa como actualización temática, sin incorporar cifras no cotejadas por página: no es prueba de estrés financiero ni miedo, y no convierte cuidados en rasgo femenino esencial.

El [Banco de México, recuadro de sofipos](https://www.banxico.org.mx/publicaciones-y-prensa/reportes-sobre-el-sistema-financiero/recuadros/%7BBF224D96-2D2C-22A1-328E-2D98D71E3532%7D.pdf), publicado 10/dic/2025, secciones metodología y consideraciones finales, analiza asociaciones macroeconómicas con morosidad. Describe baja interconexión y ausencia de importancia sistémica del sector; ROMPE esa calificación del original. No valida el IMOR puntual original ni extrapola clientes a población. Fuente (a) administrativa agregada; consultada 26/sep/2026. La adaptación sigue siendo explicación compatible; no se cuantifica cuánto del temor proviene de instituciones o cultura.

## Segmentación y comparación internacional

Región, género y recursos de origen tienen heterogeneidad documentada por CEEY. Edad, escolaridad, ruralidad y composición del hogar deben observarse conjuntamente antes de atribuir temor. Religiosidad, migración y exposición global no tienen cruces utilizables aquí: se excluyen como parámetros, no se consideran efectos nulos. El objeto no queda restringido automáticamente a clase media urbana digital; la evidencia de hogares es nacional bajo su diseño, mientras los mecanismos siguen sin medición representativa.

**Específicamente mexicano:** se identifican instituciones y fuentes mexicanas; no singularidad causal frente a otros países. **Compartido regionalmente:** vulnerabilidad es un marco pertinente, pero no se importan umbrales PPP antiguos ni cifras brasileñas sin armonización. **Sociedades desiguales:** ansiedad de estatus es hipótesis comparada, sin prevalencia mexicana. **Marco importado:** “fear of falling” puede orientar preguntas, pero no permite decidir que todo miedo mexicano es material y todo estadounidense simbólico. Hofstede y GLOBE requieren límites de muestra; WVS es un programa de encuestas y no debe confundirse con una muestra de empleados IBM.

## Implicaciones, mitos y síntesis

Protección financiera, vivienda, salud y educación son posibles consumidores de investigación; no se anuncia rentabilidad, eficacia ni demanda enorme. RH debe medir preferencias y restricciones antes de cambiar paquetes salariales. Comunicación política requiere datos propios. El masstige no queda validado como estrategia óptima.

“México es clase media” necesita definición y universo; no se refuta con un intervalo no cotejado. “NSE es seguridad” y “saldo entre olas es trayectoria” sí se descartan por incompatibilidad de estimandos. “Deuda demuestra frivolidad” y “deuda demuestra racionalidad” son lecturas igualmente no identificadas. Una fuente partidaria no vuelve falso un resultado; la procedencia y el método se evalúan directamente.

Se conserva la oportunidad de estudiar seguridad económica; cambia su condición de tesis psicológica demostrada a agenda contrastable. La oportunidad práctica es separar recursos, expectativas, acceso y bienestar. La principal contradicción del original era declarar evidencia fuerte mientras admitía no tener medición del miedo. Las cifras retiradas permanecen en la tabla histórica con motivo, sin reproducirse como actuales. Los dictámenes ROMPE refutan una conclusión o enlace determinado, no todo el fenómeno social.

## Reglas SI–ENTONCES — PROPUESTO-POR-EJECUTOR

**Si** un consumidor quiere usar NSE AMAI para segmentar hogares, **entonces** conserve instrumento, ola y unidad y mida por separado liquidez/autoposición/temor, **porque** clasificación material no identifica seguridad o emoción. Tier: fuerte para definición, hipótesis para vínculo conductual. Consumidor: investigación de producto/RH. Condición: aplicación del mismo esquema validado; falsador de la utilidad propuesta: medición conjunta que no aporte información adicional sobre el desenlace declarado. Limitación: no cambia motor ni adopta segmentos nuevos.

**Si** se propone protección anticaída para un segmento, **entonces** probar acceso, precio y reducción efectiva de daño antes de atribuir preferencia, **porque** riesgo observado no equivale a demanda solvente. Tier: propuesta, sin tasa estimada. Consumidor: piloto de política o producto autorizado por otro acto. Condición: alternativas accesibles y desenlace fijado antes; falsador: oferta adecuada sin beneficio o con daño neto. Sin refutación, sólo quedaría acotada al contexto probado; no se corroboraría una personalidad nacional.

## Auditoría de rigor extremo

- **Pobreza/violencia/informalidad vs cultura:** no se convierten condiciones materiales en personalidad; informalidad no estima temor.
- **Clase media urbana:** no se extrapolan motivos desde consumidores privados; la cobertura geográfica de una encuesta no garantiza cobertura de un constructo.
- **Sesgo importado:** marcos estadounidenses/europeos son (c), sin prevalencias mexicanas derivadas.
- **Rural/indígena/popular:** no se predice la dirección de cambios sin observarlos; sistemas comunales requieren diseño propio. Ascendencia nunca explica conducta de grupo.
- **Psicología vs incentivos:** buscar protección puede ser compatible con restricciones; optimalidad no está identificada.
- **Intuición fuerte/evidencia débil:** miedo, señalización, escuela privada y volatilidad política no tienen estimando utilizable aquí.
- **Peligro simplista:** convertir NSE en diagnóstico, vender seguros por “ansiedad” o naturalizar discriminación.
- **Estado del corpus:** conteos derivados por productor; no se afirma cobertura instrumental exhaustiva nacional.
- **Deuda asumida:** desaparece la licencia de presentar cifras de prensa como piso; pendientes permanecen localizados.
- **Contadores:** no se ejecutaron mediciones nuevas ni se movió contador; éste es producto documental.
- **Escala y comparación:** NSE es proporción de hogares; CEEY es porcentaje de personas condicionado al origen; Banxico es asociación de cartera. No se promedian.
- **Tiempo:** toda evidencia utilizada es RETROSPECTIVA; no hay emisión ni validación PROSPECTIVA.
- **Unidad:** hogares, personas y cartera son universos distintos; no hay panel de NSE ni diagnóstico individual.

Revisión humana de las tesis y recibo independiente: **SOLICITADOS**, sin firma concedida. Exposición incidental pública a ENIGH2024 se documenta y excluye de evidencia, cifras e inferencias conforme a la precisión de reserva; no se invoca autorización retroactiva.
