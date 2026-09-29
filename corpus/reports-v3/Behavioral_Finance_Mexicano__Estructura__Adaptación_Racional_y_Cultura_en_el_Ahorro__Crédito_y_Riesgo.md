# Behavioral Finance Mexicano  Estructura  Adaptación Racional y Cultura en el Ahorro  Crédito y Riesgo · v3

> | | |
> |---|---|
> | **ARCHIVO** | `corpus/reports-v3/Behavioral_Finance_Mexicano__Estructura__Adaptación_Racional_y_Cultura_en_el_Ahorro__Crédito_y_Riesgo.md` |
> | **SUCEDE A** | [`corpus/reports-v2/Behavioral_Finance_Mexicano__Estructura__Adaptación_Racional_y_Cultura_en_el_Ahorro__Crédito_y_Riesgo.md`](../reports-v2/Behavioral_Finance_Mexicano__Estructura__Adaptación_Racional_y_Cultura_en_el_Ahorro__Crédito_y_Riesgo.md) · sha256 `a4823db5bb8a92dd5e6917a1d68afd72abac2dbe285ef848e7577d9913a64368` — intacto (E.1); su cuerpo va abajo sin editar |
> | **ACTO** | `GEN2-CIERRE-Y-PRODUCTO-3` (P4) · cero mediciones · la cifra se cita por RESULT del catálogo v1.4 |
> | **CARRIL** | dominio `DINERO` · motivo del v3: `DOMINIO-CON-FILAS-NUEVAS:24` |
> | **REGENERA** | `python3 forense/analisis/reports-v3/genera_reports_v3.py` |

## v3.1 · Cifras GEN2 nuevas del carril (catálogo v1.4, por RESULT)

El carril recibió 24 filas nuevas en el catálogo v1.4; se muestran hasta 12 (agregados primero, un CALC a la vez). La tabla completa se filtra por `dominio` en `canon/catalogo-del-mexicano-v1_4.tsv`. Todas son RETROSPECTIVAS y descriptivas de una ola: ninguna identifica un mecanismo (co-observación no es identificación).

- `RESULT-ALT-M23-ENSAFI2023-TABLA#CONTRASTE:solo_informal_rural_menos_urbano` · 0.085 [0.064, 0.108] · unidad: proporcion (persona) · ENSAFI 2023 · `ADOPTADO-CON-RESERVA-DE-ANCHO` · RETROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-DIN-LXE8-ARB2-C2-P-L1xE1` · 0.486 [0.451, 0.519] · unidad: VER-SPEC · ENIF 2024 · `ADOPTADO` · PROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-ALT-M23-ENSAFI2023-TABLA#formal/NACIONAL` · 0.251 [0.239, 0.264] · unidad: proporcion (persona) · ENSAFI 2023 · `ADOPTADO-CON-RESERVA-DE-ANCHO` · RETROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-DIN-LXE8-ARB2-C2-P-L1xE2` · 0.428 [0.398, 0.457] · unidad: VER-SPEC · ENIF 2024 · `ADOPTADO` · PROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-ALT-M23-ENSAFI2023-TABLA#formal/tloc=100MIL-Y-MAS` · 0.322 [0.303, 0.347] · unidad: proporcion (persona) · ENSAFI 2023 · `ADOPTADO-CON-RESERVA-DE-ANCHO` · RETROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-DIN-LXE8-ARB2-C2-P-L1xE3` · 0.377 [0.349, 0.405] · unidad: VER-SPEC · ENIF 2024 · `ADOPTADO` · PROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-ALT-M23-ENSAFI2023-TABLA#formal/tloc=15MIL-A-99MIL` · 0.260 [0.235, 0.287] · unidad: proporcion (persona) · ENSAFI 2023 · `ADOPTADO-CON-RESERVA-DE-ANCHO` · RETROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-DIN-LXE8-ARB2-C2-P-L1xE4` · 0.323 [0.293, 0.354] · unidad: VER-SPEC · ENIF 2024 · `ADOPTADO` · PROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-ALT-M23-ENSAFI2023-TABLA#formal/tloc=2500-A-15MIL` · 0.164 [0.139, 0.190] · unidad: proporcion (persona) · ENSAFI 2023 · `ADOPTADO-CON-RESERVA-DE-ANCHO` · RETROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-DIN-LXE8-ARB2-C2-P-L2xE1` · 0.403 [0.376, 0.430] · unidad: VER-SPEC · ENIF 2024 · `ADOPTADO` · PROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-ALT-M23-ENSAFI2023-TABLA#formal/tloc=MENOS-2500` · 0.143 [0.132, 0.155] · unidad: proporcion (persona) · ENSAFI 2023 · `ADOPTADO-CON-RESERVA-DE-ANCHO` · RETROSPECTIVA · procedencia (a) datos primarios en México
- `RESULT-DIN-LXE8-ARB2-C2-P-L2xE2` · 0.348 [0.325, 0.371] · unidad: VER-SPEC · ENIF 2024 · `ADOPTADO` · PROSPECTIVA · procedencia (a) datos primarios en México

## v3.2 · Contraste de las reglas del report (`canon/reglas-contrastadas-v1_1.tsv`)

| regla | dictamen | RESULT · cifra · unidad | tier declarado → evidenciado | procedencia | matiz incorporado |
|---|---|---|---|---|---|
| `RG-3d4669ddc0`: - SI la población declara poca capacidad de cubrir gastos ENTONCES proponer opciones líquidas y ahorro reversible con consentimiento antes d | **MATIZA-SIN-CRUCE** | `RESULT-TIENEAHORROS-A-P-NO-TIENE` · 0.358 (sin IC identificado) · VER-SPEC | no declarado → hipótesis razonable | (a) | marginal: 35.8% sin ahorros (sin IC en catálogo); la población con poco colchón existe pero el ENTONCES (opciones líquidas mejores) no tiene cruce ni ensayo; driver no identificado · RETROSPECTIVA · R2: ratificado |

Una regla `MATIZA` sigue siendo PROPUESTA: su texto queda en el cuerpo v2 y el matiz de arriba es la lectura vigente. `CONFIRMA` con tier evidenciado bajo media no entra al bloque de adopción (`canon/reglas-bloque-adopcion-1.md`).

2 reglas de este report quedan `PROPUESTA` sin cifra, con su instrumento pendiente (columna `instrumento_sugerido`).

## v3.3 · Firewall genético

- `RG-96a48f4369`: `NO-APLICA`
- `RG-3d4669ddc0`: `NO-APLICA`
- `RG-3630353425`: `NO-APLICA`

## v3.4 · Módulo de auditoría de rigor extremo (preguntas [v2.16] incluidas)

- **¿Cuántos contadores movió este trabajo?** Cero mediciones: el v3 cita RESULT ya sellados.
- **[v2.16] ¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA, y se mezclan en alguna frase?** PROSPECTIVA 8 · RETROSPECTIVA 16 filas del carril; ninguna frase las mezcla.
- **[v2.16] ¿Qué unidad tiene cada cifra y se promedia con otra?** `VER-SPEC`; `proporcion (persona)`. Ninguna se promedia con otra ni se compara sin función de enlace.
- **¿Sobregeneralización desde clase media urbana?** 0 filas del carril tienen universo urbano declarado en su unidad; ninguna se lee como «el mexicano».
- **¿Qué parece psicológico y es incentivo racional?** `adaptación racional a restricción de liquidez` 1.
- **¿Pobreza, violencia o informalidad confundidas con cultura?** Las cifras nuevas son descriptivas de una ola; el v3 no atribuye ningún gradiente a «cultura».
- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna cifra: todas salen del catálogo v1.4 o de las reglas contrastadas, por el generador.
- **¿Qué sería peligroso leído simplista?** Leer un piso de una ola como tendencia, o un contraste entre dos grupos como efecto causal.

---

# Cuerpo heredado de v2 (sin editar · sha256 `a4823db5bb8a92dd5e6917a1d68afd72abac2dbe285ef848e7577d9913a64368`)

# Dinero en México: ahorrar, mantener liquidez y elegir circuitos financieros

Versión editorial completa, PROPUESTO-POR-EJECUTOR; corte `11602de8e375c10b90807d1b74e088f6b9e99c8b`. Contadores movidos por esta pieza: cero. No adopta reglas ni acredita revisión independiente. Original conservado íntegro; tabla razonada y cifras se regeneran desde el paquete local de dinero.

## Resumen ejecutivo

1. **Sólido, descripción:** existe ahorro por vías formales e informales y ambas pueden coexistir. La clasificación se refiere a personas adultas y al ahorro declarado durante el periodo del cuestionario, no a hogares ni a saldos bancarios. FIN-001 se MATIZA.
2. **Sólido, límite de medición:** tener cuenta no equivale a haber ahorrado en ella. Una cuenta de nómina o apoyos puede facilitar pagos sin formar un colchón. FIN-003 y FIN-010 quedan SIN-CIFRA en este corte.
3. **Sólido, asociación:** la capacidad declarada de cubrir gastos con ahorros difiere entre quienes tienen y quienes no tienen seguridad social por su trabajo. El contraste no mide metas, disciplina ni una preferencia temporal. FIN-013 se MATIZA.
4. **Malinterpretado:** llamar óptimo al horizonte corto supera la evidencia. Puede ser adaptación a restricciones, sesgo psicológico o combinación de ambos; el agregado no decide. FIN-014 queda SIN-CIFRA por instrumento inadecuado para juzgar optimalidad.
5. **Malinterpretado:** no se puede convertir participación en tanda entre un grupo en participación entre todos los ahorradores usando porcentajes de bases diferentes. FIN-011 ROMPE esa equivalencia aritmética.
6. **Sólido, descripción restringida:** entre quienes no tienen cuenta, el reactivo de razón principal combina desconfianza y mal servicio. No mide desconfianza general ni muestra que sea el factor principal de toda exclusión. FIN-007 se MATIZA.
7. **Útil:** preguntar acceso, elegibilidad, costos y aceptación de pagos precede a atribuir preferencias por efectivo. No hay medida de oferta sellada para el ahorro de esta ola; se declara esa ausencia junto a sus marginales.
8. **Malinterpretado:** ingreso, capacidad de pago y disposición a pagar no son equivalentes. FIN-022 MATIZA la primera afirmación del original sin refutarla: no acredita aquí una relación empírica general. FIN-022-C1 ROMPE solo el argumento de que los sobreprecios demuestran valoración de conveniencia, acceso y confianza; urgencia, selección, garantías y alternativas también pueden explicar la contratación.
9. **Descripción corporativa:** actividad de una billetera muestra escala del proveedor, pero no cuántos mexicanos antes excluidos adquirieron capacidad financiera ni si son jóvenes. FIN-026 se MATIZA; FIN-025 permanece SIN-CIFRA.
10. **Útil, heterogeneidad:** género, ingreso, región, edad, escolaridad y ruralidad son ejes que deben medirse por conducta específica. No se presentan brechas GEN1 como parámetros actuales ni se atribuye mecanismo estructural a una diferencia cruda.
11. **Hipótesis conservada:** la tensión indulgencia–aversión al riesgo aparece en L31 como hipótesis razonable. FIN-029 queda SIN-CIFRA, pendiente de contraste individual y no refutada. FIN-029-C1 ROMPE exclusivamente la lectura país→persona de los índices Hofstede; no el planteamiento de la hipótesis. La tenencia de crédito, inversión o criptomonedas tampoco es una escala de riesgo.
12. **Útil, frontera:** remesas, pensiones, seguros y deuda requieren estimandos y unidades propios. Una transferencia recibida no observa planificación binacional; una cuenta de retiro no prueba horizonte largo. No se completa ninguna cifra desde otra encuesta ni se abre una ola reservada.

Los hallazgos sólidos son conductas declaradas y distinciones de medición. Las explicaciones culturales y la optimalidad son hipótesis. Las decisiones útiles son de diseño y de medición; su eficacia no se presume.

## Marco conceptual

Separar cinco objetos evita confundir inclusión con bienestar: **acceso** a una oferta, **uso** de un producto, **saldo** disponible, **resiliencia** ante interrupción del ingreso y **horizonte de metas**. La ENIF reutilizada en esta pieza observa ahorro declarado y capacidad de cubrir gastos; esta última no es una medición de planes. Ahorrar mediante una cuenta tampoco dice cuánto dinero conserva la persona o si podría disponer de él sin costo.

La psicología individual incluye preferencias, atención y memoria. Los scripts culturales regulan reciprocidad, confianza y obligaciones. La adaptación racional es una explicación condicionada a alternativas y costos efectivos, no un sinónimo de cualquier conducta popular. La estructura incorpora ingresos, empleo, oferta, infraestructura y reglas institucionales. Ninguna de estas capas elimina automáticamente las demás.

La tensión indulgencia–riesgo se conserva como hipótesis compatible, sin medición conjunta en las mismas personas. Hofstede y GLOBE son marcos agregados importados (c); trasladar sus índices a decisiones individuales sin puente medido produce falacia de nivel. Esta crítica se dirige al enlace país→persona y no refuta la hipótesis individual. WVS puede aportar respuestas individuales de una ola, pero no reemplaza una pregunta financiera ni convierte correlación entre países en mecanismo. No se usa evidencia de diáspora (b) como evidencia sobre residentes de México. Las fuentes primarias locales y el experimento mexicano se etiquetan (a), con sus poblaciones propias.

## Mapa de evidencia por tier

**Frecuencia fuerte, alcance descriptivo (a):** RESULT sellados de ahorro y resiliencia en ENIF; población elegida adulta en viviendas particulares, con filtros expresos. Adopción, integridad y validez son controles distintos. No se anuncia validación independiente de las llaves aquí usadas.

**Frecuencia media (a), auto-reportada:** comunicado corporativo de FEMSA. El conteo operativo no es estadística nacional de personas únicas y el control de integridad no audita su definición de usuario activo.

**Mecanismo con identificación local (a):** Gertler, Higgins, Malmendier y Ojeda estudian una oferta aleatoria a empresas mexicanas ya usuarias de fintech. Los recordatorios aumentan aceptación; cumplir una promesa de recordatorio es compatible con confianza. Su selección incluye el cuartil de ventas más alto entre usuarios y excluye negocios cerrados o muy contraídos durante la pandemia. El experimento identifica intervenciones, mientras la mediación psicológica tiene evidencia auxiliar. No identifica el mecanismo del ahorro doméstico ni de las tandas. Fuente primaria de 2025, pp.1–4 y 11–15, [PDF de los autores](https://seankhiggins.com/assets/pdf/BehavioralFirmsProfitableOpportunities.pdf).

**Hipótesis razonables:** compromiso social en tandas, memoria monetaria, motivos de estatus, planificación transnacional, preferencia por liquidez ante incertidumbre. El paquete distingue adquisición pendiente, ejecución pendiente, instrumento inadecuado, restricción y no comparabilidad. No hay refutación por ausencia de cifra.

**Narrativas populares:** mexicanos gastalones, pobres incapaces de ahorrar o efectivo como atraso. Tampoco se adopta su reverso universal: toda informalidad óptima, toda desconfianza racional o toda brecha explicada por estructura.

## Cifras trazables y alcance

| Conducta | Valor / IC | Denominador y n | Objeto | Estado |
|---|---|---|---|---|
| Ahorra por alguna vía formal | 28.49%; IC95 [27.42, 29.68]% | TODA la poblacion 18+ con FAC_PER valido (denominador COMPARTIDO); n=13502 | RESULT-ENIF-AHO-B-P-FORMAL-P · `CALC-ENIF-0001` | ADOPTADO; RETROSPECTIVA |
| Ahorra por alguna vía informal | 56.19%; IC95 [55.02, 57.40]% | TODA la poblacion 18+ con FAC_PER valido (denominador COMPARTIDO); n=13502 | RESULT-ENIF-AHO-B-P-INFORMAL-P · `CALC-ENIF-0001` | ADOPTADO; RETROSPECTIVA |
| Resiliencia corta con seguridad laboral | 37.31%; IC95 [34.99, 39.38]% | personas 18+ con trabajo CON seguridad social (P3_13 in {1,2,3,4}) y P4_10 valido; n=3969 | RESULT-ENIF-AHO-A-P-CORTO-CON-P · `CALC-ENIF-0001` | ADOPTADO; RETROSPECTIVA |
| Resiliencia corta sin seguridad laboral | 54.13%; IC95 [52.16, 56.19]% | personas 18+ con trabajo SIN seguridad social (P3_13='7') y P4_10 valido; n=4973 | RESULT-ENIF-AHO-A-P-CORTO-SIN-P · `CALC-ENIF-0001` | ADOPTADO; RETROSPECTIVA |
| Razón desconfianza/mal servicio; conoce protección | 6.08%; IC95 [3.77, 8.67]% | personas 18+ SIN CUENTA que SI conocen la proteccion (P5_20 valido y P5_23='1'); n=426 | RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE-P · `CALC-ENIF-0001` | ADOPTADO; RETROSPECTIVA |
| Razón desconfianza/mal servicio; no conoce protección | 5.48%; IC95 [4.57, 6.47]% | personas 18+ SIN CUENTA que NO conocen la proteccion (P5_20 valido y P5_23='2'); n=2544 | RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE-P · `CALC-ENIF-0001` | ADOPTADO; RETROSPECTIVA |
| Ahorra por ambas vías | 20.48%; sin IC propio | todas las personas 18+ con FAC_PER válido; mismo universo que familia B CALC-ENIF-0001; n=ver padre | RESULT-HVD-A-AMBAS-VIAS · `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | ADOPTADO; RETROSPECTIVA |
| Ahorra solo formal | 8.02%; sin IC propio | todas las personas 18+ con FAC_PER válido; mismo universo que familia B CALC-ENIF-0001; n=ver padre | RESULT-HVD-A-SOLO-FORMAL · `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | ADOPTADO; RETROSPECTIVA |
| Ahorra solo informal | 35.72%; sin IC propio | todas las personas 18+ con FAC_PER válido; mismo universo que familia B CALC-ENIF-0001; n=ver padre | RESULT-HVD-A-SOLO-INFORMAL · `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | ADOPTADO; RETROSPECTIVA |
| No declara ahorro por esas vías | 35.79%; sin IC propio | todas las personas 18+ con FAC_PER válido; mismo universo que familia B CALC-ENIF-0001; n=ver padre | RESULT-HVD-A-NO-AHORRA · `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | ADOPTADO; RETROSPECTIVA |

Cada porcentaje propio es descriptivo RETROSPECTIVO. Las categorías de vías comparten población, y sus exclusividades se derivaron en la corrida citada; los marginales formal/informal se solapan. No se suman las dos tasas de razón de desconfianza porque sus bases son diferentes. Los intervalos solo aparecen cuando existen en el objeto sellado; la ausencia de intervalo de un derivado no se transforma en precisión perfecta. Oferta/exclusión de ahorro: SIN-MEDIDA-DE-OFERTA-SELLADA-PARA-ESTA-OLA-Y-CONDUCTA; no inferir preferencia de canal. Las mediciones de oferta de crédito de olas históricas no se trasladan a ahorro actual.

FEMSA declara 9.9 millones de usuarios activos Spin by OXXO en 3T2025. Fuente externa `FEMSA`; cantidad tomada del comunicado, sin equivalencia a prevalencia nacional.

La cifra externa es AUTO-REPORTADA por FEMSA, fuente primaria leída el 26/sep/2026, comunicado del 28/oct/2025, sección SPIN. No es RESULT propio, no tiene adopción al motor y no establece usuarios únicos nacionales o incremento neto de inclusión. [Comunicado de resultados](https://www.femsa.com/en/press-room/press-release/femsa-results-3q-2025/).

## Patrones principales

### Ahorro por varias vías y tandas

**Descripción y a favor:** los RESULT permiten coexistencia y separación entre vías. **En contra de la lectura amplia:** ni todos combinan ni la informalidad implica exclusión bancaria; alguien puede tener cuenta y guardar dinero en casa. **Segmentos:** contrastar ingreso, sexo, región, localidad y edad con las mismas preguntas; esta pieza no asigna prevalencias de subgrupos ausentes. **Causas compatibles:** liquidez, costos de transacción, reciprocidad o compromiso. **Riesgo de mala lectura:** llamar infraestructura masiva a cualquier participación o convertir cajas digitales en equivalentes funcionales de una tanda. **Implicación:** comparar seguridad de custodia, disponibilidad y compromisos antes de trasladar una función social a un producto.

El falsador del mecanismo de compromiso requiere registrar restricciones de retiro, sanciones y cumplimiento; comparar con ahorro individual de igual ingreso y acceso, idealmente con asignación exógena de la herramienta. Si no cambia ahorro sostenido, queda acotada la ventaja de compromiso; no desaparece la utilidad de liquidez o reciprocidad.

### Resiliencia y seguridad laboral

**Descripción y a favor:** P4_10 pregunta cuánto tiempo cubren gastos los ahorros si cesa ingreso. Las categorías cortas difieren por seguridad social laboral. **En contra:** seguridad social no fue asignada y puede correlacionarse con ingreso, edad, ocupación y acceso financiero. **Segmentos:** adultos trabajadores con códigos definidos; quedan fuera otros códigos y no trabajadores. **Causas:** excedente acumulable y riesgos de ingreso son rivales plausibles de preferencias temporales. **Riesgo:** convertir falta de colchón en imprevisión o afirmar que empleo estable demuestra planificación larga. **Implicación:** medir flujo, saldo y metas por separado antes de recomendar horizonte de producto.

Un cambio exógeno de estabilidad de ingreso con medición previa y posterior separaría adaptación de composición. La simple prolongación de resiliencia no prueba cambio de metas. Si no cambia una meta directamente medida, la hipótesis de horizonte se acota, aunque mejore el colchón.

### Desconfianza, mal servicio y oferta

**A favor:** la razón principal existe entre no tenedores. **En contra:** el reactivo agrupa dos motivos y excluye tenedores, y conocimiento del seguro no fue aleatorizado. **Segmentos:** no tenedores con razón válida y conocimiento/no conocimiento válidos; no representar a todos los mexicanos. **Causas rivales:** experiencia con proveedor, comisiones, distancia, elegibilidad y percepción de protección. **Riesgo:** atribuir cada respuesta a memoria de crisis o afirmar que informar seguro bastará. **Implicación:** probar información transparente y cumplimiento verificable después de documentar oferta efectiva; no inferir cobertura legal de una licencia corporativa sin revisar entidad depositaria.

Para identificar confianza hay que separar mal servicio de creencia sobre solvencia y manipular información/cumplimiento manteniendo costos y elegibilidad. Si no cambia conducta, ese falsador puede acotar la intervención; no demuestra que la confianza carezca de papel en otro contexto.

### Crédito como recurso y posible daño

**Descripción:** el endeudamiento puede financiar gastos o inversión y generar riesgos. **A favor:** esta pieza no incorpora una trayectoria longitudinal que permita cuantificar tales desenlaces. **En contra:** atrasos transversales no identifican trampa ni destino, y tasas ofertadas no prueban pago realizado. **Segmentos:** requieren distinguir prestatarios, nunca usuarios y personas elegibles sin oferta. **Causas:** urgencia, ingreso, condiciones, garantías y prácticas de cobro. **Riesgo:** moralizar deuda o justificar precios altos como preferencia del pobre. **Implicación:** comparar costo total, disponibilidad y desenlaces antes de ofrecer crédito sin historial. Se mantienen cerradas las exposiciones reservadas ENIF2024 de crédito.

La distinción herramienta/trampa necesita seguimiento de propósito, flujos, refinanciación y pérdida de activos. Una trayectoria negativa no se atribuye al producto sin comparación adecuada. No se formula aquí consejo legal ni se publican penas o tarifas no verificadas.

### Fintech, uso y fricciones

**A favor:** FEMSA comunica actividad operativa y la literatura mexicana muestra que comunicación puede cambiar aceptación de ofertas entre negocios existentes. **En contra:** clientes no equivalen a nuevos incluidos, y actividad no equivale a saldo suficiente. **Segmentos:** población del proveedor y empresas usuarias; no generalizar a jóvenes, indígenas, rurales o mayores. **Causas:** acceso físico, costos, interoperabilidad y fricciones de atención/confianza compiten. **Riesgo:** inferir sustitución de sucursal o efectivo a partir de conteos corporativos. **Implicación:** registrar conversión, persistencia, saldo, costos y abandono por cohortes antes de escalar una propuesta.

### Seguridad, estatus, retiro y remesas

El dinero puede cumplir funciones diferentes, pero oro y guardadito no observan por sí mismos motivos. Tenencia de afore no mide aportaciones activas ni seguridad futura. Expectativas de trabajar y recibir apoyos pueden coexistir. Remesas agregadas no observan decisión binacional y no se promedian con cantidades por persona. **A favor:** son hipótesis pertinentes para instrumentos específicos. **En contra:** no hay contraste directo usado aquí. **Segmentos:** hogar receptor, persona cotizante y propietario de activos son unidades distintas. **Riesgo:** presentar intuición como prevalencia. **Implicación:** módulos de motivos y pares emisor-receptor, sin abrir ENIGH reservada ni completar números inaccesibles.

## Causas: cultura, estructura y adaptación

No hay estimación que adjudique peso dominante a estructura, cultura o adaptación. Sí hay razones para empezar por las restricciones: una opción inaccesible no puede elegirse; el excedente limita ahorro; retiro líquido y calendario de cobros modifican costos. Que estas razones existan no demuestra que la decisión concreta maximice bienestar. Atención, memoria y confianza pueden importar dentro de una oferta accesible, como muestra el experimento acotado; no deben atribuirse a identidad nacional.

La historia monetaria puede motivar una investigación de cohortes, pero una cronología no prueba memoria subjetiva ni transmisión generacional. Se retiran cifras históricas no leídas. Los scripts de reciprocidad y familia deben coobservarse con comportamiento, no deducirse de un instrumento de confianza general.

## Segmentación explícita

Región y urbanización: infraestructura y aceptación de pagos son condiciones a medir, sin trasladar promedios nacionales a localidades. Clase e ingreso: capacidad de acumular, volatilidad y oferta preceden a motivos. Edad: separar ciclo de vida de cohorte y periodo. Género: diferencia descriptiva no es efecto causal de sexo; medir trabajo, ingreso y cuidados. Escolaridad: no sustituye competencias ni información aplicada. Lengua indígena: no equivale al sistema comunal vivo, fuera por diseño; evitar ampliación indebida. Religiosidad, migración y exposición global: no hay estimandos directos usados; permanecen como ejes propuestos, no diferencias afirmadas. Seguridad laboral: contraste específico disponible, con límites de universo; no renombrarlo formalidad total.

## Comparación internacional útil

**Distintivamente mexicano:** esta pieza estudia instrumentos y proveedores mexicanos, sin evidencia comparativa que pruebe singularidad del empeño, retail-crédito o remesas. **Compartido regionalmente:** informalidad y circuitos alternativos son hipótesis comparativas; no se fija prevalencia regional sin fuente primaria armonizada. **Condiciones de desigualdad/baja confianza:** mecanismo plausible, sin jerarquía causal internacional adoptada. **Malinterpretado desde marcos anglosajones:** suponer un agente con oferta universal y liquidez abundante puede convertir restricciones en preferencias. Pero asumir adaptación óptima para toda persona comete la sobrecorrección inversa.

Se retiran las comparaciones M-Pesa/UPI/Pix: usuarios, población total y adultos no forman un denominador común. Un diseño comparable requeriría edad, periodo, actividad, entidad y acceso definidos, además de variación que separe rieles, regulación y composición. La coexistencia de tandas y ROSCAs merece literatura funcional primaria; aquí no se afirma universalidad ni equivalencia causal.

## Implicaciones aplicadas y reglas propuestas

PROPUESTO-POR-EJECUTOR, consumidor posible: ficha de producto y protocolo de investigación financiera; ninguna regla se escribe en motor.

- **SI** se evalúa inclusión de ahorro **ENTONCES** registrar por separado cuenta, ahorro reciente, saldo disponible y resiliencia — **PORQUE** miden estados distintos — **TIER descriptivo fuerte**, mecanismo no identificado. Aplicable solo con preguntas y población explícitas. Falsador: una validación que demuestre equivalencia de indicadores en el universo contratado; fuera de él no se transporta. Consumidor: evaluación de producto.
- **SI** la población declara poca capacidad de cubrir gastos **ENTONCES** proponer opciones líquidas y ahorro reversible con consentimiento antes de metas rígidas — **PORQUE** la restricción de colchón puede aumentar costo de inmovilización — **TIER hipótesis razonable**, apoyada por descripción. Aplicable cuando costos y acceso estén medidos. Falsador: evaluación de bienestar/impagos que muestre daño o ninguna ventaja respecto de opciones flexibles existentes. Consumidor: piloto autorizado futuro, sin eficacia anunciada.
- **SI** una oferta accesible tiene baja aceptación **ENTONCES** evaluar recordatorios claros y cumplimiento de promesas — **PORQUE** memoria/confianza pueden intervenir — **TIER causal local para intervención en empresas (a)**; transporte a hogares no probado. Aplicable a oferta veraz, voluntaria y población comparable; no presión artificial. Falsador: ensayo local que no mejore aceptación informada o produzca daño. Consumidor: protocolo de comunicación, sin transportar tamaño del efecto.

Seguros, aportaciones automáticas y crédito rápido son propuestas que requieren evaluar costo, liquidez, siniestralidad y consentimiento. No se promete que educación financiera resuelva oferta o seguridad, ni que bajo precio resuelva todos los motivos de rechazo.

## Mitos y sobreinterpretaciones

“No ahorran por cultura” carece de puente medido y contradice existencia de ahorro declarado. “Toda tanda es folclor” desconoce la conducta, pero “toda tanda es óptima” tampoco está probado. “Precio alto revela voluntad de pagar” confunde oferta y selección. “Falta de colchón es imprevisión” confunde capacidad y preferencia. “Toda desconfianza proviene de crisis” añade memoria no observada. “Hay crédito porque hay tarjeta” estrecha indebidamente productos; “no quiere endeudarse” entre nunca usuarios no es barrera general de acceso.

## Síntesis

Patrones defendibles: coexistencia de vías, resiliencia segmentada por seguridad laboral y razones restringidas de no tenencia. Contradicciones aparentes: cuenta sin ahorro, ahorro informal con cuenta formal y crecimiento corporativo sin inclusión incremental medida. Errores: unidades mezcladas, niveles país/persona y optimalidad inferida. Oportunidades: productos flexibles, información verificable y medición por cohortes. La tabla por afirmación conserva también lo que no pudo contrastarse: retirar firmeza no equivale a negar la conducta.

## Módulo de auditoría de rigor extremo

- **¿Pobreza, violencia o informalidad confundidas con cultura?** Se describen restricciones y se separan preferencias; tampoco se concede adaptación óptima por defecto. Violencia de cobro no se trata como cultura ni se cuantifica sin fuente.
- **¿Sobregeneralización urbana de clase media?** Empresas ya digitalizadas y usuarios corporativos no representan población nacional; la selección de ventas y supervivencia limita transporte.
- **¿Sesgo estadounidense/europeo?** Marcos (c) no generan parámetros mexicanos. El experimento (a) reduce distancia geográfica pero conserva distancia de unidad y selección. No se importa evidencia (b).
- **¿Qué cambia con foco rural, indígena o popular?** Deben medirse oferta, distancias, costos y funciones sociales; no se presume signo/magnitud de brechas ni se identifica lengua con institución comunal.
- **¿Qué parece psicológico y puede ser incentivo racional?** Liquidez, metas flexibles y no uso; comprobar opciones antes de adjudicar motivo. Optimalidad sigue sin identificación.
- **¿Dónde hay intuición fuerte y evidencia débil?** Estatus, crisis recordadas, compromiso de tanda, confianza radial y planificación binacional.
- **¿Qué sería peligroso simplificado?** Precios abusivos justificados por supuesta voluntad, inmovilización del ahorro de emergencia, culpa individual o confianza forzada por publicidad.
- **¿Qué estado del corpus fue escrito a mano?** Cobertura y conteos se derivan por productor; juicios se escribieron explícitamente. La revisión manual declara límites y no acredita aceptación independiente.
- **¿Qué deuda asumida caducó?** GEN1 daba precisión a cifras sin trazabilidad. Se reemplaza por objetos autorizados y SIN-CIFRA diferenciado; no se mantiene esa deuda como parámetro.
- **¿Contadores?** Cero: editorial, no corrida, adopción ni asientos manuales.
- **¿Escalas y comparadores?** Proporciones ponderadas de personas con filtros; actividad corporativa en millones de usuarios; no se promedian ni se confunden con hogares. IC según objeto, no extrapolado a mecanismos.
- **¿Prospectiva/retrospectiva y unidad?** Toda cifra propia es RETROSPECTIVA y descriptiva. No hay predicción ni validación futura; las reglas propuestas no reciben precisión numérica prestada. Ninguna unidad delito/trámite entra al report.

## Auditoría dirigida y reservas

Cobertura derivada: 94 decisiones explícitas, 35 filas del mapa y 59 afirmaciones adicionales o cláusulas separadas. Conteos: CONFIRMA=1, MATIZA=24, ROMPE=5, SIN-CIFRA=64. Tabla local: `afirmaciones.tsv`; juicio fuente: `decisiones.json`. Los rótulos de medibilidad del mapa no se usaron como veredictos editoriales.

Se revisaron manualmente todas las ROMPE: son inferencias invalidas, equivalencias de denominador o saltos de nivel; la ausencia de fuente no recibió ROMPE. Revisión de mecanismos centrales: resiliencia no es meta; oferta no es preferencia; confianza combinada no es rasgo; experimento empresarial no es ahorro doméstico. No se ha abierto microdato ni tabulado reservado. La reserva de crédito ENIF2024 y ENIGH2024 permanece; no se consume exposición nueva ni se pide revelarla.

Dependencia #1184 comprobada por identidad, CALC y linaje: No hay intersección de estas llaves, CALC ni padre ENIF en efectos del lote ENDIREH. No acredita validación independiente de ENIF. Mantener adopción separada de validez y precisión; no retirar por extrapolación del diagnóstico. `dependencia-1184.json` conserva llaves, archivo y hash del cotejo. Veto/adopción se comprueba en catálogo y decisiones por objeto al regenerar; ningún valor vetado se usa como piso. La ausencia de precisión independiente puede cambiar un uso futuro: no se fija tolerancia ni parámetro predictivo con estas cifras.

<!-- C3-V216:INICIO (GEN2-ASTRA-CONTINUIDAD-C3-1; generado por forense/analisis/reports-v2/continuidad-c3-1/bloque_v216.py) -->

## Módulo de auditoría · preguntas [v2.16] y firewall genético (cierre editorial C3)

**¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA, y se mezclan en alguna frase?** Ninguna cifra de este report es PROSPECTIVA: ninguna fue emitida y sellada antes de existir la referencia contra la que se lee. Toda cifra aquí es RETROSPECTIVA (lectura de una ola ya vista o de una fuente publicada); ninguna frase mezcla las dos columnas.

**¿Qué unidad tiene cada cifra y se promedia con otra?** Las cifras con `RESULT-` citado (10 ids, 2 CALC sellados) llevan la unidad que declara su spec:
- `CALC-ENIF-0001` → unidad: no declarada en su spec.yaml como persona/hogar/delito/trámite: se lee en el CALC
- `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` → unidad: no declarada en su spec.yaml como persona/hogar/delito/trámite: se lee en el CALC
Ninguna cantidad de unidad delito o trámite se promedia aquí con una de unidad persona u hogar.

**Procedencia de cifras sin RESULT.** Toda cifra de este report que no cite un `RESULT-` sellado es **cifra sin sellado: no entra al canon**; su procedencia se clasifica como (a) dato primario en México, (b) muestra mexicano-americana o de diáspora (no es evidencia sobre México) o (c) marco teórico importado en la tabla de afirmaciones del expediente, enlazada desde `corpus/reports-v2/INDICE.md`.

**Firewall genético (§3).** Prohibida la inferencia ascendencia → conducta de grupo. Nada en este report autoriza segmentar por ascendencia, origen étnico o componente genético; la única vía admitida es individual, molecular y de efecto pequeño (p. ej. alcohol, nicotina), nunca como segmentación.

<!-- C3-V216:FIN -->
