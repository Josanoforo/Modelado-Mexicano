# Vejez y cuidado intergeneracional en México: familia, capacidad funcional y protección efectiva

Reports v2 · Bloque B · corte `11602de8` · C3-CUIDADO-MIGRACION-PAREJA-1. Contadores movidos por esta pieza: cero. Evidencia de frecuencia descriptiva retrospectiva; ninguna emisión prospectiva y ninguna adopción de reglas en este report. `decisiones.json` contiene el juicio explícito por cláusula; `tabla-afirmaciones.tsv` es su vista reproducible.

## Resumen ejecutivo

1. **Sólido dentro de su universo:** hay cuidado familiar observado; ENASIC permite separar receptor y proveedor. La tabla siguiente sostiene esta descripción, con las reservas de la adopción.
2. **Sólido y útil:** el cuidador principal de una persona mayor elegible suele ser mujer. Eso no equivale a afirmar que todas las cuidadoras mexicanas tienen una edad, parentesco o jornada modal determinada.
3. **Malinterpretado:** convivir con familiares no demuestra cuidados suficientes, protección económica o bienestar. El “seguro familiar” sigue siendo una hipótesis sobre protección efectiva.
4. **Útil:** hogar que necesita cuidados y persona que recibe ayuda son unidades distintas. Ninguna tasa de hogar sustituye una tasa de personas dependientes.
5. **Malinterpretado:** el parentesco del cuidador no demuestra piedad filial, obligación aceptada o preferencia libre. Oferta disponible y recursos preceden a esa atribución.
6. **Matizado:** estructura, guion de género y adaptación pueden contribuir al reparto del cuidado; su jerarquía causal no está identificada por los pisos descriptivos.
7. **Útil:** cuidado recibido durante una semana no identifica necesidad no satisfecha de largo plazo. Ausencia de ayuda observada puede incluir autonomía, falta de necesidad o carencia.
8. **Matizado por literatura reciente:** el trabajo de cuidadores y su malestar requieren atención, pero una muestra electrónica de conveniencia no produce prevalencias nacionales ni efectos del cuidado sobre depresión.
9. **Malinterpretado:** el porcentaje ENASEM2021 y la población CONAPO2025 citada en el v1 no comparten base temporal. El absoluto queda sin confirmar hasta recuperar población, año y denominador compatibles; su refutación aritmética se retira.
10. **Matizado:** recibir remesas, vivir solo y estar acompañado son dimensiones separadas. No se sostiene una causalidad general “migración de hijos → abandono”.
11. **Útil:** ingreso disponible y capacidad funcional deben medirse por separado. Una transferencia monetaria no es una medida de horas, calidad o continuidad del cuidado.
12. **Límite material:** se retiran del cuerpo afirmativo cifras de fecundidad, demencia, geriatras, pensiones y costos sin lectura primaria o RESULT adecuado. Las cifras retiradas siguen visibles como testimonios del v1 en las decisiones.

## Marco conceptual

La vejez es una etapa del curso de vida, no un diagnóstico de dependencia. Este report usa el corte de personas de 60 años y más de ENASIC para describir conductas observadas. La necesidad funcional, el cuidado efectivamente recibido, su suficiencia y la autonomía decisional son resultados diferentes. También distingue la persona mayor, la persona cuidadora y el hogar que organiza recursos.

“Seguro familiar” puede designar una red que responde a un choque de salud o ingreso. Para acreditar seguro se necesita observar el choque, la respuesta y el desenlace protegido: necesidades satisfechas, consumo, salud o continuidad del apoyo. Corresidencia, transferencias o una declaración de deber no bastan. La hipótesis adaptativa predice que cambios en servicios accesibles alterarán arreglos y costos de cuidado; la hipótesis normativa predice persistencia de determinadas obligaciones aun con alternativas de calidad y precio comparables. Ambas pueden operar simultáneamente. Un cambio de oferta con grupo comparable y observación antes/después permitiría separarlas mejor que un marginal nacional.

Psicología individual (malestar y sentido), guiones culturales (deberes), adaptación (organización ante restricciones), estructura (ingreso, empleo, vivienda) e instituciones (servicios y reglas) son planos analíticos distintos. Ninguno autoriza inferir conducta desde ascendencia. El sistema indígena comunal vivo queda fuera del marco del proyecto; no se generaliza a él desde habla de lengua indígena o encuestas nacionales.

## Mapa de evidencia por tier y procedencia

**Frecuencia fuerte dentro del estimando, no mecanismo fuerte:** (a) pisos ENASIC 2022 de `CALC-ENASIC-CUIDADOS-VEJEZ-0001`, catálogo v1.2, adoptados **CON-RESERVA-DE-ANCHO** por `FP-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-02`. Una sola ola, cuidador principal con muestra pequeña y sin localidad utilizable. El objeto sellado y la firma prevalecen sobre la vista atrasada de `consulta.py`, que no encontró este CALC. No se altera ninguna vista.

**Asociación media, sin tasa nacional transportable:** (a) estudio original de cuidadores publicado en 2025, componente mexicano, reclutamiento de conveniencia mediante redes de apoyo y cuestionario electrónico. Examina síntomas depresivos con PHQ-9 y covariables; selección por alfabetización, dispositivo y participación voluntaria. Su diseño transversal no identifica causalidad. Los componentes Puerto Rico y Colombia no son muestras de México; tampoco la introducción sobre diáspora convierte al componente mexicano en evidencia (b). [Métodos, resultados y limitaciones del estudio][VEJ-M1].

**Descripción nacional de otra población:** (a) boletín ENASEM 2021 leído, con población de 53 años y más en sus resultados generales. No justifica trasladar automáticamente un porcentaje a todas las personas de 60 años y más. No se obtuvo del documento el denominador necesario para conservar las tasas de satisfacción y soledad del v1. [Boletín primario ENASEM 2021][VEJ-E1].

**Hipótesis razonables:** seguro familiar imperfecto, adaptación a falta de oferta y reparto según guion de género. **(b)** No se usa aquí una muestra de diáspora como evidencia nacional. **(c)** “Familismo desprotegido”, Hofstede y la autonomía residencial como ideal son marcos importados: ayudan a formular preguntas, no calibran protección, preferencia o rasgo mexicano.

### Cifras propias, poblaciones y denominadores

| Clave · estimando | Punto · IC95 de diseño · N | Denominador, unidad y estado |
|---|---|---|
| R-MUJER · Cuidador principal mujer | 68.36% · [63.60; 72.74]% · N=422 | Personas60+ con cuidador principal del hogar pareado y sexo válido; persona receptora; ADOPTADO-CON-RESERVA-DE-ANCHO. `RESULT-ENASIC-CUIDADOS-VEJEZ-AM60-CUIDADOR-PRINCIPAL-MUJER-2022-TOTAL-TODOS-P` |
| R-HIJA · Cuidador principal hija | 30.54% · [24.35; 37.01]% · N=422 | Personas60+ con cuidador principal del hogar y parentesco válido; persona receptora; ADOPTADO-CON-RESERVA-DE-ANCHO. `RESULT-ENASIC-CUIDADOS-VEJEZ-AM60-CUIDADOR-PRINCIPAL-HIJA-2022-TOTAL-TODOS-P` |
| R-CONYUGE · Cuidador principal cónyuge/pareja | 49.29% · [42.51; 55.16]% · N=422 | Personas60+ con cuidador principal del hogar y parentesco válido; persona receptora; ADOPTADO-CON-RESERVA-DE-ANCHO. `RESULT-ENASIC-CUIDADOS-VEJEZ-AM60-CUIDADOR-PRINCIPAL-CONYUGE-2022-TOTAL-TODOS-P` |
| R-DENTRO · Cuidado por alguien del hogar | 15.61% · [12.80; 18.34]% · N=2276 | Personas60+ con P4_42=1/2; excluye hogar unipersonal/código3/blancos; persona60+; ADOPTADO-CON-RESERVA-DE-ANCHO. `RESULT-ENASIC-CUIDADOS-VEJEZ-AM60-CUIDADO-POR-ALGUIEN-DEL-HOGAR-2022-TOTAL-TODOS-P` |
| R-FUERA · Cuidado por persona de otro hogar | 7.77% · [6.51; 9.17]% · N=2623 | Personas60+ con P4_45=1/2; excluye blancos; persona60+; ADOPTADO-CON-RESERVA-DE-ANCHO. `RESULT-ENASIC-CUIDADOS-VEJEZ-AM60-CUIDADO-POR-PERSONA-DE-OTRO-HOGAR-2022-TOTAL-TODOS-P` |
| R-HOGAR60 · Hogar con60+ que necesita cuidados | 31.97% · [30.33; 33.67]% · N=6508 | Hogares con HN_C60MA=1/2 y diseño válido; hogar; ADOPTADO-CON-RESERVA-DE-ANCHO. `RESULT-ENASIC-CUIDADOS-VEJEZ-HOGAR-CON-60MAS-QUE-NECESITA-CUIDADOS-2022-TOTAL-TODOS-P` |
| R-HOGAR · Hogar que necesita cuidados | 78.10% · [76.93; 79.37]% · N=6508 | Hogares con HN_C=1/2 y diseño válido; hogar; ADOPTADO-CON-RESERVA-DE-ANCHO. `RESULT-ENASIC-CUIDADOS-VEJEZ-HOGAR-NECESITA-CUIDADOS-2022-TOTAL-TODOS-P` |

Todos los puntos e intervalos provienen del objeto sellado, no de transcripción de prensa. Los intervalos son de diseño, no intervalos de predicción temporal. Factor `FAC_HOG`, estrato `EST_DIS`, UPM `UPM_DIS`; personas enlazadas al diseño del hogar por `LLAVEHOG`. Los N son observaciones sin ponderar del denominador particular, no población expandida. La corrida usa bootstrap de UPM dentro de estrato. La firma no convierte la precisión del piso en validación independiente del mecanismo.

`R-MUJER`, `R-HIJA` y `R-CONYUGE` condicionan a una persona mayor con cuidador principal del hogar identificable y pareado. No tienen como denominador todas las personas cuidadoras nacionales. “Hija” es categoría específica, no “hija o nieta”. `R-HOGAR60` se refiere a hogares, no a todas las personas mayores dependientes. La lista cerrada P1 distingue estas codificaciones de la agregación del boletín oficial [ENASIC 2022, definición y resultados][A1]. No fusionar ni sumar los puntos de ayuda dentro y fuera del hogar: pueden corresponder a las mismas personas y sus exclusiones difieren.

## Patrones principales

### Familia observable, protección por demostrar

**Descripción y evidencia a favor:** las relaciones de cuidado del hogar incluyen cónyuge e hija, según `R-CONYUGE` y `R-HIJA`. **En contra de la lectura fuerte:** se condiciona a tener cuidador; las personas sin ayuda o sin pareo no aparecen en esos denominadores. No se observan aquí necesidades totalmente cubiertas. **Segmentos:** edad del receptor, capacidad funcional, tamaño del hogar, presencia de pareja y recursos requieren observación conjunta; estos pisos de un eje no ofrecen esas interacciones. **Causas compatibles:** proximidad, vivienda compartida, afecto y restricciones de oferta. **Riesgo:** usar convivencia para negar demanda pública o vida independiente para diagnosticar abandono. **Implicación:** evaluar suficiencia y elección además de arreglo residencial. **Falsador del mecanismo:** si ante choques comparables la red no amortigua necesidades o consumo, “seguro” pierde contenido predictivo.

### Feminización del cuidador principal

**Descripción:** `R-MUJER` sostiene una mayoría femenina dentro del universo condicionado. **A favor:** el sexo del cuidador se obtiene del renglón pareado, no del sexo del jefe ni del receptor. **En contra:** existen cuidadores hombres; no se demuestra una jornada nacional ni que hija sea la categoría predominante sobre cónyuge. **Segmentos:** receptor por edad/sexo y disponibilidad de apoyo; parentesco no identifica género del cónyuge. **Causas compatibles:** oportunidades laborales, accesibilidad de servicios, horarios y deber familiar. **Riesgo:** tratar a toda mujer como cuidadora disponible o asignar causalidad al marianismo sin medición. **Implicación:** identificar a quien cuida realmente y su costo de oportunidad. **Falsador:** una expansión accesible de servicios que no alterase distribución o costo exigiría revisar la versión estrictamente adaptativa, considerando utilización y calidad antes de interpretarla.

### Ayuda recibida y necesidad funcional

**Descripción:** `R-DENTRO` y `R-FUERA` observan ayuda, cuidado o acompañamiento en la semana de referencia. **A favor:** distinguen origen de la persona que cuida. **En contra:** la codificación de cuidado dentro excluye hogar unipersonal; ayuda fuera conserva otro universo. Una tasa menor no prueba rechazo o abandono. **Segmentos:** dependencia, enfermedad, vida en solitario y alternativas de apoyo. **Causas compatibles:** autonomía, ayuda no necesaria, barreras o déficit de disponibilidad. **Riesgo:** llamar desprotegida a toda persona sin cuidado. **Implicación:** preguntar por dificultad funcional y demanda no satisfecha antes de ofertar un servicio. **Falsador:** contrastar necesidades expresadas y tareas no cubiertas con la clasificación de ausencia de cuidado; si no coinciden, retirar la equivalencia.

### Malestar del cuidador y límites de transporte

**Descripción:** el estudio de 2025 estudia asociaciones con síntomas y reconoce límites de generalización. **A favor:** cuestionario estandarizado y componente mexicano. **En contra:** conveniencia y acceso digital; no hay asignación de cuidado ni prevalencia nacional. **Segmentos:** la evidencia no alcanza para calibrar población rural sin conectividad o cuidados indígenas. **Causas compatibles:** intensidad, salud previa y carga laboral son rivales del efecto del rol en sí. **Riesgo:** convertir tamizaje en diagnóstico o usar el porcentaje de una clínica como parámetro nacional. **Implicación:** la oferta debe permitir evaluación y referencia, con consentimiento y capacidad de atención. **Falsador causal:** un diseño longitudinal que mida estado previo, entrada al cuidado y dependencia del receptor, o una intervención, podría separar selección y daño atribuible. Hasta entonces “cuidar enferma” es demasiado amplio.

### Ingreso, migración y compañía

**Descripción:** el v1 reúne dinero, pensión, remesas, residencia y soledad bajo un mismo seguro. **A favor conceptual:** financiar una tarea puede ampliar alternativas. **En contra empírica:** ENASIC no identifica en esta corrida el efecto de migración de hijos ni suficiencia del ingreso. Los artículos etnográficos citados en v1 no fueron leídos aquí y sus cantidades no se conservan como hechos. **Segmentos:** receptor/proveedor, origen del dinero, frecuencia, uso y posibilidad de contratar apoyo. **Causas compatibles:** remesas y cuidado presencial pueden complementar o sustituir tareas diferentes. **Riesgo:** imputar abandono a hogares migrantes o suficiencia a quien recibe dinero. **Implicación:** separar seguridad económica, cuidado físico y vínculo emocional en el producto. **Falsador:** observar simultáneamente cambios de migración, remesas, necesidad y apoyo con control de selección; una correlación municipal no resuelve el efecto individual.

## Causas: cultura, estructura y adaptación

La falta de servicios y las restricciones de ingreso son condiciones que deben medirse antes de atribuir preferencia. El piso ENASIC describe reparto; no demuestra que la estructura sea causalmente primaria. Los guiones pueden afectar negociación, utilización de servicios o sentimiento de obligación, pero la etiqueta “marianismo” suele apoyarse en literatura (b) y no se incorpora como rasgo individual mexicano estimado. La adaptación racional es una hipótesis con costos y alternativas definidos: disponibilidad, precio, calidad, distancia y horarios. Sin observar esas alternativas, toda conducta puede parecer adaptativa y el mecanismo se vuelve infalsable.

La comparación que falta no es simplemente hogares con/sin familia: debe igualar necesidad y recursos. Cambios de oferta de cuidado, con observación de utilización y resultados, permitirían contrastar mecanismos; permanecer con familia puede expresar tanto elección como restricción. No se deduce ausencia de afecto de una motivación económica.

## Segmentación explícita

| Eje | Qué admite este corte y qué exige un sucesor |
|---|---|
| Región | No ranking causal ni de suficiencia; requiere oferta local y estimaciones comparables. |
| Clase | Ingreso y capacidad de pago son condiciones, no etiquetas que determinan cuidado comprado. NSE no construido en este CALC. |
| Edad | Receptor60+; edades avanzadas requieren medir funcionalidad, no presumirla. |
| Género | Sexo del proveedor pareado distinto del receptor; no trasladar la tasa entre ambos. |
| Escolaridad | Puede afectar acceso a información; no efecto estimado. Muestra electrónica excluye parte de la población. |
| Urbanización | ENASIC no aporta localidad utilizable en estos pisos; no estimar brecha rural/urbana. |
| Religiosidad | Espiritualidad autorreportada en conveniencia no identifica religiosidad mexicana ni efecto protector. |
| Migración | Sin vínculo causal en este CALC; requerir trayectorias y selección de hogar. |
| Exposición global | Sin medición apropiada; no deducir adopción de apps o ideales de envejecimiento. |

## Comparación internacional útil

**Específicamente mexicano en este producto:** instrumento, cuestionario y firma de pisos ENASIC, no una esencia ni una excepcionalidad del cuidado. **Compartido regionalmente:** los arreglos de cuidado son preguntas comparables; el estudio multinacional de conveniencia no establece diferencias poblacionales entre países. **Asociado a condiciones estructurales:** comparar primero servicios, ingreso y capacidad funcional, sin usar PIB o “baja confianza” como causa automática. **Malinterpretado por marco importado:** independencia residencial no es bienestar por definición y corresidencia no es protección por definición.

El v1 propone Uruguay, sur de Europa y Japón. Sin normas primarias y estimandos armonizados leídos, esta versión los deja como agenda comparativa. No sostiene cifras de gasto, velocidad demográfica o suficiencia fiscal importadas. El contraste defendible consistiría en personas con necesidad funcional semejante, alternativas de atención descritas y desenlaces equivalentes; no una analogía histórica que asigne a México el futuro de otro país.

## Implicaciones aplicadas

Para servicios de salud y municipios, una entrevista de necesidad funcional y tareas no cubiertas es más útil que inferir necesidad por edad o hogar. Identificar al proveedor real permite ofrecer evaluación de carga y rutas de apoyo; antes de tamizar hay que garantizar una respuesta asistencial posible. Respiro y atención domiciliaria son propuestas a evaluar por acceso, aceptación y desenlaces del receptor y del cuidador; esta evidencia no demuestra su costo-efectividad ni fija una cuota fiscal.

Para producto y RH, coordinar turnos, contactos y tareas puede ser razonable cuando existe una red y capacidad digital, pero debe admitir canal asistido y cuidadores hombres. La privacidad, consentimiento de la persona mayor y acceso práctico son condiciones del consumidor, no detalles de implementación. No diseñar el servicio suponiendo que una hija estará disponible. Mercado de vejez: segmentar por necesidad y capacidad de pago observadas; ningún porcentaje de PIB sin método sirve para dimensionar demanda.

## Mitos y auditoría final

“La familia cuida, luego no hacen falta servicios”: no sigue de una frecuencia condicionada. “Vivir solo es abandono”: confunde arreglo residencial, voluntad y necesidad. “Una pensión resolvió la vejez”: confunde recursos monetarios y función. “El cuidado enferma a todos”: convierte asociación seleccionada en efecto universal. “Las remesas compran compañía”: confunde financiamiento y presencia. “La estructura es la causa primaria”: excede la identificación disponible.

**Pobreza/cultura:** no se etiqueta la restricción económica como tradición. **Clase media urbana:** la muestra electrónica reciente no calibra la población popular desconectada. **Marcos EE.UU./Europa:** PHQ-9 y tipologías requieren transporte explícito; tamizaje no diagnóstico. **Rural/indígena/popular:** no hay localidad en estos pisos ni validación específica leída; reconocer el límite, sin declarar inválidas todas las escalas. **Psicología/incentivo:** decisiones de convivencia y provisión requieren observar costos y oferta. **Intuición/evidencia débil:** debilitamiento longitudinal del seguro familiar, daño causal y silencio del mayor permanecen preguntas. **Lectura peligrosa:** romantizar familia puede legitimar carga; patologizarla puede ocultar preferencias.

**Estado del corpus:** datos de cobertura de esta pieza son generados desde decisiones/mapa; no se inventa aceptación del lote. La deuda del v1 de cifras sin fuente caduca como autorización para afirmarlas: se preserva el testimonio y se retira el uso. Cero contadores movidos. **Escalas/unidades:** proporciones ponderadas con IC, observaciones N sin ponderar, persona y hogar separados. Todo es RETROSPECTIVO-DESCRIPTIVO; no hay afirmación de acierto futuro. **C1:** ninguna de las llaves ENASIC usadas figura en #1184/lote1 ni en el recibo posterior disponible; eso significa no evaluadas allí, no COINCIDE ni validación independiente. Se cruzan las llaves contra catálogo, exclusiones, firmas y recibo en `dependencias.tsv`. Un retiro posterior de una llave obliga a regenerar la conclusión correspondiente, no a retirar todo ENDIREH; este report no depende de ENDIREH.

### Revisión dirigida de ROMPE y mecanismos

`V-020-*`: revisión manual mantiene porcentaje y absoluto sin confirmar. La multiplicación entre ENASEM2021 y CONAPO2025 no sostiene ROMPE; se retira en `revision-dirigida.md` y se requiere población, año y denominador compatibles. `V-007-*` y `V-010-*`: lectura manual retira causalidad y preferencia forzada, conserva hipótesis rival y falsador. `V-008-*`: receptor con cuidador del hogar no representa a toda la población cuidadora. `V-013-*` y `V-014-*`: no usar tasas clínicas no leídas. `V-036-*`: propuestas sin cuota numérica ni garantía de eficacia. Cuantitativas principales: puntos e intervalos contrastados con objeto, catálogo y adopción. No se abrió microdato. Hubo exposición al boletín ENADID 2023 antes de identificar la reserva específica P1; se declaró en `incidente-exposicion.md` y no alimenta el report ni sus dictámenes sustantivos. No constituye autorización retroactiva.

## Síntesis y reglas propuestas

Patrones conservados: cuidado observado en la red familiar y mayoría femenina del proveedor principal dentro de un universo condicionado. Contradicción útil: esa red puede coexistir con necesidades no satisfechas y costo de oportunidad, sin que el piso estime su magnitud. Errores corregidos: unidad hogar/persona, porcentaje/absoluto, frecuencia/mecanismo, síntoma/diagnóstico y oferta/preferencia. Oportunidad: construir medición de protección efectiva y evaluación accesible, no fijar un rasgo cultural.

**PROPUESTO-POR-EJECUTOR, sin adopción ni motor:**

| SI · ENTONCES · PORQUE | Tier/consumidor/condición | Falsador y limitaciones |
|---|---|---|
| SI una persona60+ solicita apoyo, ENTONCES evaluar funcionalidad y tareas no cubiertas antes de clasificarla por hogar, PORQUE ayuda recibida y necesidad son distintas. | Frecuencia descriptiva(a); ficha de atención municipal/primer nivel. Aplicar con consentimiento y ruta de respuesta. | Si una clasificación residencial predijera suficientemente necesidades en validación externa y no perdiera casos, revisar valor añadido; no fija umbral diagnóstico. |
| SI hay cuidador principal identificado, ENTONCES ofrecer evaluación de carga y coordinación a esa persona, PORQUE sexo y parentesco del receptor no identifican al proveedor. | Frecuencia(a); diseño de servicio de apoyo. Pareo confirmado, contacto accesible y consentimiento. | Si la identificación no coincide con provisión real de tareas en validación, retirar regla de asignación; no presupone cuidadora mujer ni tasa nacional de malestar. |
| SI se usa dinero o remesa como indicador de protección, ENTONCES exigir un desenlace de suficiencia separado, PORQUE recursos y cuidado no son el mismo estimando. | Hipótesis razonable; ficha de medición/cola futura. Observar simultáneamente necesidad y destino/continuidad del apoyo. | Si el ingreso midiera consistentemente suficiencia en poblaciones comparables podría simplificarse; aquí no hay efecto causal ni tamaño propuesto. |

[A1]: https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2023/ENASIC/ENASIC_23.pdf
[VEJ-M1]: https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1610733/full
[VEJ-E1]: https://mhasweb.org/resources/DOCUMENTS/Fact%20Sheet/Press%20Release/PRESS%20RELEASE%20July%202023%20-%20MHAS-ENASEM%20%26%20MEX-COG%202021.pdf
