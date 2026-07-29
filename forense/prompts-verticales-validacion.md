# Prompts verticales de validación — Ronda 4 (extender la capa de validación del modelo)

> ⚠️ **Actualizado 28/jul/2026.** Dos correcciones de referencia:
> 1. La regla de cita textual apuntaba a `modelo-decisiones-mexicano.md` — **el v1, borrado el 27/jul**. Ahora apunta a `modelo-decisiones-mexicano-v2.md §3.B`. *Una regla que manda citar un archivo inexistente no obliga a nada: es el patrón "principio sin requisito de salida" en su forma más literal.*
> 2. **La ficha canónica que se pega junto a este prompt debe ser la del 28/jul o posterior.** La anterior omitía cuatro reglas `[FUERTE]` (el dominio Familia y pareja entero, la tanda y el puente personal) y degradaba una. Si tu corrida usó una ficha previa, sus veredictos sobre esos dominios **no transfieren**.

> **⚠️ NOTA DE PARCHE · 27 de julio de 2026 · tres correcciones obligatorias antes de volver a usar esta plantilla**
>
> Las cinco corridas que salieron de aquí produjeron evidencia auditada de buena calidad —la prueba NBER, el IMOR regulado de la CNBV, los RCT de clientelismo, los expedientes de Famsa y Crédito Real—. **Lo que falló no fue la evidencia: fue la maquinaria.** Tres defectos, cada uno con la misma forma: *un principio declarado sin requisito de salida*.
>
> | # | Defecto | Consecuencia medida | Parche |
> |---|---|---|---|
> | 1 | Anti-confusión sin límite: "adaptación racional" absorbía cualquier variable psicológica | La convergencia "estructura > psicología" salía **por definición**, no por evidencia | Límite del blindaje, en LOS TRES BLINDAJES |
> | 2 | *"Descartar con rigor es el entregable"* declarado, **sin exigir la tabla** | El registro filtró 31→16 y justificó **1 de 15** descartes. Los 14 restantes son irrecuperables (PD-01). V3 no archivó ninguno | Tabla de descartes obligatoria, en ESTRUCTURA DEL REPORT |
> | 3 | Las reglas a estresar se **parafraseaban** en vez de citarse del motor | De 13 reglas, **6 no existían** en `modelo §3` y 4 divergían. Sus veredictos no transfieren | Regla de cita textual, antes del bloque vertical |
>
> El patrón: el cumplimiento dependía de la disciplina de quien corriera el prompt. V1 archivó sus descartes por buen criterio propio; V3 no archivó ninguno. **Un principio necesita un artefacto de salida que falte visiblemente si no se cumple** — es la regla `§3.3` del propio modelo, norma sin sanción creíble, operando sobre el equipo que la escribió.

*Corre cada bloque en una conversación aparte (dentro del proyecto, para cruzar con el integrador y el modelo). Pega el PREÁMBULO FORENSE una vez por conversación, luego un solo bloque vertical. Los resultados vuelven en formato compatible con la §7 del modelo (confirma / matiza / rompe).*

**Qué extiende cada uno:** V1 masstige → dominio consumo/marca (nuevo); V2 clientelismo/voto → dominio político-cívico (nuevo); V3 crédito de tienda → endurece el dominio financiero con métricas AUDITADAS; V4 BNPL → escaneo prospectivo de riesgo (forma distinta). Prioridad para salir de fintech: V1 y V2.

---

## PREÁMBULO FORENSE REUTILIZABLE — pégalo al inicio de cada conversación

```text
Estoy validando un modelo de decisión sobre el mexicano contemporáneo (anti-esencialista, segmentado por perfiles) contra desenlaces reales. Esta es una investigación forense vertical: profundiza un dominio específico. El objetivo NO es explicar por qué el mexicano decide como decide, sino VALIDAR O ROMPER reglas del modelo contra casos y datos reales. Escribe en español.

POR QUÉ ESTE ENCUADRE: casi toda la literatura de "por qué X funcionó/fracasó en México" es narrativa post-hoc —causa inventada sobre un resultado ya conocido—. Este report hace lo contrario: aísla el supuesto conductual, verifica si era correcto, y determina si su acierto/error fue plausiblemente DECISIVO frente a los factores estructurales. Se espera descartar más de lo que se conserva; descartar con rigor es el entregable, no un fracaso.

LOS TRES BLINDAJES (metodología central):
1. ANTI-CONFUSIÓN. Separa la variable psicológica de las estructurales (capital, logística, precio, regulación, timing, competencia, ejecución operativa, suerte). Un caso solo cuenta como evidencia "psicológica" si esa variable fue plausiblemente DECISIVA. Nombra los factores de confusión de cada caso; si no se puede aislar, márcalo CONFUNDIDO y trátalo como ilustrativo.

   ⚠️ LÍMITE DEL BLINDAJE (añadido 27/jul/2026 — sin esto, el blindaje se vuelve una máquina de infalsabilidad):
   - "Adaptación racional" NO es lo contrario de psicología: ES una afirmación conductual. Si reetiquetas la conducta como "adaptación racional a la estructura" y con eso la enrutas al lado "estructura", el veredicto sale a favor de la estructura POR DEFINICIÓN, no por evidencia. Ese fue el defecto de tres de las cuatro verticales previas.
   - Una creencia sobre si LA CONTRAPARTE VA A CUMPLIR es confianza, esté fundada o no. Que la desconfianza sea racional —porque el proveedor efectivamente defraudó— no la convierte en "cálculo" y no la saca del análisis. En un país donde los proveedores fallan, toda desconfianza está fundada; si lo fundado descalifica, ninguna regla sobre confianza puede falsarse jamás.
   - Distingue: creencias sobre la EFICACIA DEL PRODUCTO con independencia de quién lo ofrece (p. ej. "denunciar no sirve porque la fiscalía no investiga") = pronóstico, no confianza. Creencias sobre el DESEMPEÑO DE LA CONTRAPARTE (p. ej. "esta aseguradora no me va a pagar") = confianza.
   - Toda afirmación de "aquí decidió la estructura" debe cargar su UMBRAL DE REVERSIÓN: qué magnitud de efecto o qué contraevidencia mostraría que no. Sin umbral, es culturalismo al revés.
2. ANTI-POST-HOC. Clasifica el supuesto como DECLARADO (la organización lo dijo ANTES del resultado — es el oro), INFERIDO (reconstruido de sus acciones) o RETROSPECTIVO (solo aparece después, en prensa/análisis — el más débil, se registra pero no prueba). Prioriza DECLARADO e INFERIDO.
3. ANTI-SUPERVIVIENTE. Busca activamente lo invisibilizado: éxitos silenciosos, fracasos por razones aburridas/estructurales, y sobre todo PARES CONTRAFACTUALES (misma jugada, distinto segmento/resultado, con la estructura constante y la variable conductual visible). Los pares valen más que casos aislados.

CRITERIO DE INCLUSIÓN: SÍ casos con supuesto identificable (declarado/inferido) + desenlace conocido + información para aislar la variable psicológica. NO: "fracasó porque no entendió la cultura mexicana" sin mecanismo aislable; casos donde la única evidencia es el resultado + retrofit de un analista; fracasos puramente estructurales disfrazados de psicológicos.

DISCIPLINA ANTI-ESENCIALISTA: un supuesto formulado como "el consumidor/votante mexicano" es SEÑAL DE ALARMA — fuerza el SEGMENTO (clase, región, urbanización, generación, formalidad). Hallar que el supuesto psicológico NO importó (decidió la estructura) es un resultado VALIOSO, no nulo. No conviertas informalidad/pobreza/violencia en "cultura". Firewall: nada de ascendencia→conducta.

PLANTILLA POR CASO (para cada uno que sobreviva el filtro):
- Organización/actor y jugada (qué, cuándo, dónde).
- El supuesto conductual en juego.
- Estatus: DECLARADO / INFERIDO / RETROSPECTIVO (con cita o evidencia).
- Segmento(s) realmente involucrado(s).
- Resultado (éxito/fracaso/mixto) con métrica si existe, y su fuente (auditada vs. auto-reportada).
- Aislabilidad: AISLABLE / CONFUNDIDO / INDETERMINADO + factores de confusión nombrados.
- Veredicto: ¿el supuesto era correcto? ¿su acierto/error explica el resultado, o fue la estructura/ejecución?
- Cruce con el modelo: qué regla SI-ENTONCES / perfil / generador CONFIRMA, MATIZA o ROMPE.
- Tier del caso: [FUERTE] (declarado + aislable + métrica auditada) / [MEDIA] / [ILUSTRATIVO].

ESTRUCTURA DEL REPORT: (1) resumen ejecutivo con los patrones que emergen; (2) nota de método y riqueza del material (cuántos casos evaluados vs. conservados, sesgos de la fuente, auditado vs. auto-reportado); (3) casos que sobreviven (plantilla), agrupados por acierto/error; (4) pares contrafactuales; (5) TABLA COMPLETA DE DESCARTES (obligatoria, ver abajo); (6) qué CONFIRMA/MATIZA/ROMPE del modelo (entregable central); (7) módulo de auditoría autocrítico caso por caso, incluyendo el sesgo del propio autor.

TABLA DE DESCARTES — OBLIGATORIA (añadida 27/jul/2026):
Lista TODOS los candidatos evaluados que NO sobrevivieron, uno por fila: caso · supuesto en juego · blindaje que lo tumbó (CONFUNDIDO / POST-HOC / FUERA DE ALCANCE / SIN MATERIAL) · una línea de motivo · procedencia de esa explicación.
Un descarte sin registrar es EVIDENCIA DESTRUIDA, no un caso que "no aplicaba". El blindaje anti-superviviente no consiste en filtrar bien: consiste en que el filtro quede auditable. Si descartas 15 y solo justificas 1, tu muestra es sesgada por supervivencia con la etiqueta de que no lo es.
Precedente: el registro de apuestas filtró 31 casos a 16 y solo justificó 1 de los 15 descartes. Los otros 14 nunca se escribieron y son irrecuperables (PD-01). No lo repitas.

CÓMO SE CITAN LAS REGLAS A ESTRESAR (añadido 27/jul/2026 — regla dura):
Toda regla que este encargo te pida estresar viene CITADA TEXTUALMENTE del motor `modelo-decisiones-mexicano-v2.md §3.B` (v2.1), con su tier, su dominio y sus perfiles. Si una regla del encargo NO trae esa cita, está marcada como PROPUESTA NUEVA y tu veredicto sobre ella NO cuenta como validación del modelo — cuenta como evaluación de una hipótesis.
Si al leer el modelo encuentras que la regla real difiere de como aparece aquí (distinto alcance, dominio, segmento o tier), DILO Y JUZGA LA VERSIÓN CANÓNICA, no la del prompt.
Por qué: la Ronda 4 falló justo aquí. De 13 reglas que los cuatro verticales dijeron estresar, 6 NO EXISTÍAN en el motor y 4 divergían en alcance. Sus veredictos quedaron sin transferir. El caso extremo: una recomendación de negocio del integrador ("masstige") fue ascendida a "regla del modelo" por el prompt, con una cláusula que no aparece en ningún documento; el vertical la declaró falsa y la falsación se escribió en el modelo canónico como si se hubiera probado una regla.

A continuación, el vertical específico:
```

---

## V1 · Masstige y consumo aspiracional *(extiende a consumo/marca — prioridad alta)*

```text
VERTICAL: ¿Qué organizaciones apostaron a un supuesto sobre el consumo aspiracional del mexicano —"premium accesible", estatus, calidad con dignidad, marca extranjera vs. orgullo nacional— y acertaron o fallaron, con MÉTRICAS (no solo narrativa publicitaria)?

Reglas del modelo a estresar:
- "Calidad y dignidad por encima de 'lo más barato' en segmentos populares" (validada parcialmente por Mamá Lucha; ¿aguanta con métricas de venta en otros casos?).
- "Masstige / premium accesible funciona SOLO si la marca se aísla del descuento" (el matiz Costco vs. Sam's; ¿se replica?).
- "Marca extranjera + orgullo nacional coexisten" (contradicción del consumidor; ¿cuándo gana cada una?).
- Consumo compensatorio / señalización de estatus como driver (perfiles 2 y 3; generador G2 desigualdad/baja movilidad).

Casos candidatos a examinar (conservar solo los que sobrevivan el filtro): Starbucks México, Cinépolis (y su formato VIP/Macro XE), Liverpool y El Palacio de Hierro (aspiracional de clase media-alta), Miniso y Ikea (democratización de diseño), tiendas de conveniencia premium, marcas de cerveza/tequila premium, telefonía (iPhone en mensualidades como símbolo de estatus vía crédito), automotriz de entrada aspiracional, y cadenas de café/restaurante que fracasaron por leer mal el segmento. Busca métricas: ventas mismas-tiendas, ticket promedio, expansión, fidelidad/recurrencia (Kantar, Nielsen, reportes a la BMV), no solo premios publicitarios.

Ojo específico: distingue el ÉXITO por aspiración/estatus del éxito por precio, ubicación o falta de competencia. El dominio publicitario es rico en narrativa y pobre en falsabilidad —degrada a ILUSTRATIVO todo lo que no tenga métrica de venta atribuible—. Fuerza el segmento AMAI (A/B, C+, C, D) en cada caso; "el consumidor aspiracional mexicano" en bloque es señal de alarma.
```

---

## V2 · Clientelismo electoral y secreto del voto *(extiende a político-cívico — prioridad alta)*

```text
VERTICAL: ¿Los actores políticos que apostaron a que el clientelismo (regalos, despensas, transferencias, programas) COMPRA votos, acertaron? ¿O el votante toma el beneficio y vota con autonomía? Es la prueba directa de las reglas cívicas del modelo.

NATURALEZA DEL MATERIAL: aquí el "caso" no es corporativo sino la APUESTA de un partido/campaña, y la evidencia fuerte es sobre todo ACADÉMICA (experimentos de campo, list experiments, estudios de secreto del voto), no decks. Prioriza estudios experimentales/cuasi-experimentales sobre población mexicana; trata la prensa como contexto, no como prueba.

Reglas del modelo a estresar:
- "El clientelismo desde abajo tiene AGENCIA: se acepta el beneficio pero se conserva autonomía de voto" (hipótesis del modelo, §3.7).
- "Las transferencias directas universales se viven como derecho/gratitud al líder pero sin monitoreo ni broker" (hipótesis; ¿la evidencia la confirma o muestra compra efectiva?).
- "La participación es contingente al peso simbólico del acto" (validado por la brecha presidencial vs. judicial).
- "El voto de clase media responde a estabilidad/aspiración, no es antisistema".

Preguntas guía: ¿el vote-buying efectivamente mueve votos, o el secreto del voto lo neutraliza? ¿la condicionalidad de programas (Progresa/Oportunidades) generó lealtad electoral o solo cambió conducta de capital humano? ¿el efecto de las transferencias no condicionadas (Pensión del Bienestar, Jóvenes Construyendo el Futuro) sobre el voto es de compra o de "premio al desempeño/identidad"? Busca: literatura experimental mexicana sobre compra de votos y secreto del voto, estudios LAPOP/AmericasBarometer, evaluaciones de efecto electoral de programas sociales, trabajo sobre brokers y movilización.

Disciplina: segmenta por clase/región/urbanización (el clientelismo no opera igual en el sur rural que en la clase media urbana). Hallar que "el clientelismo NO compra el voto que se supone" es un resultado valioso que confirma la agencia del votante. Firewall anti-esencialista: "el votante mexicano se vende" es señal de alarma, no premisa.
```

---

## V3 · Crédito de tienda con métricas auditadas *(endurece el dominio financiero)*

```text
VERTICAL: El hallazgo estrella del registro previo ("utilidad + fricción baja + datos alternativos > buró tipo EE.UU. y > confianza", validado con Nu/Kueski/Aplazo/Azteca) se apoyaba en parte en métricas de morosidad AUTO-REPORTADAS por las empresas (BNPL privado no publica NPL primario). Este vertical cierra ese flanco con datos AUDITADOS/REGULADOS: el crédito de tienda de grupos que cotizan o reportan a la CNBV.

Objetivo: verificar si el modelo de crédito al segmento popular/informal es sostenible o si la morosidad lo contradice, usando datos regulados por segmento.

Reglas del modelo a estresar:
- "El hogar informal SÍ es sujeto de crédito vía evaluación relacional/datos alternativos" (¿la morosidad regulada lo sostiene o lo desmiente?).
- "Datos alternativos, no buró tipo EE.UU." (¿el desempeño crediticio real valida el scoring alternativo?).
- "Aversión al riesgo alta + horizonte corto en el segmento informal" (¿se refleja en patrones de mora?).

Casos y fuentes: Coppel / BanCoppel, Grupo Elektra / Banco Azteca, Famsa (y su quiebra — caso de FRACASO del modelo, valiosísimo), Crédito Real, Financiera Independencia, y las SOFIPOS/SOFOMES relevantes. Busca: IMOR (índice de morosidad) por cartera de consumo reportado a la CNBV, reportes anuales y a la BMV, calificadoras (HR Ratings, Fitch), y estudios académicos independientes (p. ej. el del Banco Mundial sobre Banco Azteca ya citado). Contrasta explícitamente la morosidad AUDITADA contra las cifras "de un dígito bajo" auto-reportadas por el BNPL.

Entregable clave: ¿el patrón "utilidad > confianza" se sostiene cuando se mira la morosidad regulada, o hay señales de que el modelo presta de más a un segmento que no puede pagar (la posible bomba)? El caso Famsa (quiebra 2020) es el contra-ejemplo obligado a analizar: ¿fue fracaso del supuesto conductual, de la ejecución, o del fondeo? Segmenta por producto y por NSE. Marca cada métrica como AUDITADA o AUTO-REPORTADA.
```

---

## V4 · BNPL y crédito fácil como riesgo de sobreendeudamiento *(escaneo prospectivo — forma distinta)*

```text
VERTICAL (forma distinta): esto NO es un registro de apuestas pasadas, sino un ESCANEO DE INDICADORES ADELANTADOS. La regla del modelo "el segmento popular adopta crédito fácil de baja fricción" (validada como ÉXITO de adopción) tiene una consecuencia downstream a probar: esa misma conducta —fricción baja + preferencia por el presente + red formal de protección débil— ¿está construyendo una burbuja de sobreendeudamiento? El objetivo es evaluar el RIESGO, no un desenlace ya ocurrido.

Marco: trata al modelo como hipótesis predictiva. SI el modelo acierta en que estos segmentos adoptan crédito fácil, ENTONCES deberíamos ver señales de mora creciente, refinanciamiento, o estrés financiero concentrado en esos segmentos. Busca confirmar o refutar esa cadena.

Qué medir (indicadores adelantados):
- Crecimiento y morosidad del crédito al consumo y del BNPL (Banxico, CNBV, CONDUSEF), desglosado por segmento donde sea posible.
- Quejas ante CONDUSEF/Profeco por crédito y BNPL; prácticas de cobranza.
- Encuestas de endeudamiento y estrés financiero de los hogares (ENIF, Banxico, estudios de inclusión financiera).
- Reportes de estabilidad financiera de Banxico y advertencias regulatorias sobre BNPL.
- Comparación internacional: ¿el BNPL en México sigue la trayectoria de sobreendeudamiento observada en otros mercados emergentes o desarrollados?

Reglas del modelo a estresar:
- "Utilidad + fricción baja > confianza / aversión al riesgo cede con crédito fácil" — ¿tiene un costo downstream que el modelo debería incorporar como advertencia?
- "Horizonte corto + preferencia por el presente" (§3.6, generador G3 escasez) — ¿amplifica el riesgo de sobreendeudamiento en crédito de fácil acceso?

Entregable: una evaluación de riesgo con nivel de confianza (¿hay burbuja incipiente, señal mixta, o no hay evidencia todavía?), qué segmentos están más expuestos, y qué indicador habría que monitorear. Distingue evidencia de riesgo REAL de alarmismo mediático. Firewall anti-esencialista: "los mexicanos no saben manejar deuda" es señal de alarma —el marco es estructura (fricción de diseño, ausencia de educación financiera efectiva, red de protección débil), no carácter—.
```

---

*Cómo se integran los resultados. Cada report vuelve con su sección 5 (confirma/matiza/rompe). Se doblan en la §7 del modelo: los casos con métrica auditada que confirmen suben reglas a `[FUERTE, validado]` fuera de fintech; los que rompan marcan una regla para revisión; V4 puede añadir una **advertencia downstream** a la regla de adopción de crédito. Con V1 y V2 corridos, la conclusión "utilidad > confianza" deja de ser hipótesis-fuera-de-fintech y pasa a tener evidencia en consumo y en lo cívico —o se acota por dominio si no aguanta—.*
