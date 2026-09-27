# ASTRA-6 · Propuesta final para Claude

**De:** Astra → Claude / dirección y Jonás / mesa  
**Fecha:** 26 de septiembre de 2026  
**Estado:** propuesta para acordar y convertir en encargos; no constituye firma de mesa, adopción ni autorización de fusión.  
**Base de lectura:** `main` consultado en `34949751113358869be981e2220f25d97e8097bd`, misión y transfer adjuntos del 26/sep. Los ejecutores actualizarán las premisas materiales al arrancar.

## 1. Dictamen y objetivo

Acepto los tres carriles de MISION-ASTRA-6. La misión es ambiciosa y útil. Propongo conservar su alcance completo y ajustar el método para que termine en tres productos: resultados cuya credibilidad conocemos, pruebas futuras informativas y una explicación revisada del comportamiento en México.

La pregunta rectora será: **¿qué podemos afirmar después de este trabajo que antes no podíamos sostener, qué debemos retirar y qué observación futura cambiaría nuestra conclusión?**

No convierto los carriles en una auditoría general. Los controles adicionales de C1 forman parte de la validación independiente solicitada; fuera de ese propósito rige el presupuesto habitual de auditoría. Priorizaremos defectos que alteren cifras, alcance o decisiones.

## 2. Correcciones comunes antes del lanzamiento

- **Universos distintos:** filas de adopción, CALC, RESULT, registros dentro de tablas y afirmaciones del catálogo no son intercambiables. El censo mínimo de cada carril los distinguirá. Las 136 filas de decisiones citadas en la misión no se usarán como denominador de estimadores sin expandir su alcance.
- **Estado consolidado:** las cifras del transfer que incluyan trabajo en vuelo son contexto. Cada entrega declarará su commit de corte, sin esperar indefinidamente a los demás carriles.
- **Autoridad:** Astra propone diseños y dictámenes; Codex ejecuta; Claude emite el recibo exigido para las corridas; mesa adopta y fusiona. La revisión técnica no sustituye la decisión humana.
- **Resultado central:** coincidencia numérica, validez del estimando, adopción y capacidad predictiva son preguntas diferentes. Cada conclusión indicará cuál contesta.
- **Sin nueva burocracia:** usar los registros y formatos existentes. Automatizar vínculos y conteos; reservar el juicio para discrepancias y conclusiones.

## 3. C1 · Credibilidad de lo adoptado

**Pregunta:** ¿qué afirmaciones publicables sobreviven una reconstrucción independiente desde las especificaciones y qué discrepancias cambian una conclusión?

### Universo y ejecución

Congelar el universo adoptado y vigente en un commit, excluyendo vetos y sucesores retirados según las decisiones aplicables. Construir una tabla mínima que enlace decisión → CALC → RESULT/registro de tabla → afirmación o uso. Deduplicar reutilizaciones del mismo estimador. La unidad de implementación será la familia de cálculo; la cobertura se reportará por estimador y por afirmación central.

El objetivo sigue siendo **todo el universo adoptado de ese corte**. Se ejecutará por lotes, comenzando por los resultados de mayor exposición pública y los métodos con más riesgo material: denominadores, ponderadores, NS/NR, módulos y olas, escalas, intervalos y transformaciones. El primer lote no sustituye el resto.

### Independencia efectiva

Esta sesión de Astra ya leyó resultados. Puede diseñar el trabajo y analizar discrepancias, pero no se presentará como ejecutor ciego. Los recálculos corresponden a sesiones nuevas, sin historial heredado y con un paquete de entrada que contenga únicamente spec humana, cuestionario, descriptor, identificación de insumos autorizados y datos de olas abiertas.

El entorno ciego no incluirá el repositorio completo, el código productor, los resultados esperados, los reports que los revelan ni sus historiales. El paquete se revisará para retirar filtraciones de valores objetivo sin completar silenciosamente una spec insuficiente. Si la separación no puede garantizarse, el lote se rotulará **reimplementación independiente no ciega** y no contará como validación ciega.

El código propio y los números se congelan antes de abrir la comparación. Un comparador separado aplica tolerancias preexistentes y documentadas. Si faltan, se declara la carencia y se fija el criterio antes de revelar valores esperados; nunca se ajusta para obtener coincidencia. Para métodos aleatorios se distingue equivalencia estadística de identidad bit a bit.

**El historial de Git acredita el orden de commits, no prueba ausencia de lecturas.** La evidencia de ceguera será la separación de entradas y sesiones, con sus límites declarados; no una búsqueda `git log -p -S` sobre archivos sin cambios.

### Dictamen y cierre

Estados numéricos: `COINCIDE`, `DISCREPA`, `NO-RECALCULABLE-DESDE-SPEC`. Una falta de acceso será `BLOQUEADO-POR-ACCESO`; una fila aún no trabajada, `NO-EVALUADO`. Ninguna de las dos se hará pasar por insuficiencia de spec ni por validación.

Además del estado numérico, cada discrepancia indicará su efecto: cambia cifra, incertidumbre, alcance, conclusión o ninguno material. Coincidir con una spec errónea no valida el estimando: los defectos conceptuales se reportan aparte, con consecuencia concreta.

**Entrega:** código independiente; resultados congelados; tabla completa del universo; evidencia en los mecanismos existentes; incidencias agrupadas por causa cuando un defecto afecte muchas filas; y dictamen de producto sobre qué sostener, corregir, acotar o proponer suspender. No se reescriben sellos ni se cambian adopciones desde este carril.

Si se entrega una muestra intermedia, declarar selección, semilla cuando aplique y cobertura. No extrapolar una tasa global desde selección dirigida por riesgo. El cierre completo exige cero `NO-EVALUADO` y cero bloqueos de acceso pendientes; un corte parcial útil no se anunciará como validación de todo el catálogo.

## 4. C2 · Pruebas futuras que puedan cambiar una decisión

**Pregunta:** ¿qué emisiones podemos congelar hoy y qué resultados futuros discriminarían alternativas relevantes?

Mantener las seis familias existentes. Para cada una: estimando, unidad, población, ola objetivo, horizonte, pérdida primaria, incertidumbre, umbral sustantivo, regla ante datos faltantes, criterio de parada y contrato de datos. Congelar COMMIT-1 y emisiones COMMIT-2 con las olas históricas autorizadas; no abrir ninguna reserva.

### Ajustes de diseño

- **Familia no equivale a ola:** reportar ambos conteos y la dependencia entre pruebas que compartan muestra. No afirmar seis oportunidades independientes si proceden de menos publicaciones.
- **Calendario honesto:** citar fecha oficial cuando exista; de lo contrario, ventana esperada y fuente. No inventar fechas de 2027.
- **Compatibilidad futura:** preparar el lector contra un esquema explícito y probarlo con sintéticos y la ola histórica. Si cambian nombres sin cambiar significado, admitir adaptación de cableado documentada; si cambia el estimando o cuestionario, detener esa prueba y dictaminar comparabilidad. No prometer que necesariamente solo faltará COMMIT-3.
- **Potencia relevante:** las réplicas muestrales históricas no representan por sí solas el cambio temporal. Evaluar escenarios de cambio y dependencia, con supuestos rotulados; informar cambio mínimo detectable y probabilidad de una conclusión informativa. No modificar umbrales después de ver el desenlace.
- **Prueba del conducto:** verificar por separado la reproducción de emisiones congeladas y la ejecución completa contra oro histórico. Ninguna acredita todavía acierto sobre la ola futura.
- **Retador opcional:** máximo uno externo por familia, conforme a la excepción de C2 de la misión. Solo si representa una hipótesis estructural distinta y añade una comparación útil. No se reabre la fabricación de retadores sobre olas vistas.
- **Hasta cuatro familias nuevas:** evaluar ENSU, ENOE, ENSANUT y MOCIBA por comparabilidad, horizonte y valor informativo. Proponer únicamente las defendibles, para firma; no llenar un cupo.

### Entrega y cierre

Seis expedientes con emisiones selladas o dictamen explícito de inviabilidad y propuesta de retiro; código probado; calendario; escenarios de potencia; activación por familia; hoja de firmas para propuestas nuevas y decisiones pendientes.

Distinguir `SELLADO-INTERNAMENTE`, `ENVIADO-A-ATESTACION` y `ATESTIGUADO-EXTERNAMENTE`. La incorporación a un manifiesto no equivale a atestación externa; conservar el comprobante verificable cuando exista. Si depende de la acción de mesa, entregar el paquete terminado y declarar esa dependencia sin detener C1 o C3.

Frase de producto derivada: **«N familias con emisiones congeladas para M olas futuras; K con atestación externa verificada; fechas confirmadas o ventanas esperadas identificadas».**

## 5. C3 · Reports v2 que revisen la explicación

**Pregunta:** ¿qué tesis sobre México se sostienen, cuáles cambian y cuáles aún carecen de una prueba adecuada?

Se conserva el objetivo de **31 reports v2 y un índice**, con los originales intactos. La entrega será por lotes completos y utilizables. Comenzar por confianza, capital social, religiosidad, consumo y familia: ya contienen resultados que obligan a revisar afirmaciones. Después cubrir los demás dominios hasta completar el universo.

### Método editorial y analítico

1. Vincular cada afirmación identificada del v1 con evidencia y dictamen. Las afirmaciones materiales ausentes del mapa también se registran en la tabla del carril, sin alterar el mapa ajeno ni inventarles un estado consolidado.
2. Usar `CONFIRMA`, `MATIZA`, `ROMPE` y `SIN-CIFRA`, con razones diferenciadas para esta última: adquisición pendiente, falta de ejecución, instrumento inadecuado, no comparabilidad, restricción del proyecto o imposibilidad justificada del estimando. Ausencia de evidencia no equivale a refutación.
3. Reescribir las tesis y mecanismos cuando cambie su sustento. Distinguir descripción, asociación, predicción e identificación causal. Explicitar qué observación separaría explicaciones rivales.
4. Cada cifra propia llevará CALC, RESULT y, cuando corresponda, referencia exacta a la fila de tabla, unidad, periodo y estado. Respetar vetos y reservas. Los resultados sellados no adoptados podrán discutirse como evidencia provisional explícita, sin presentarlos como producto adoptado.
5. Las cifras externas llevarán fuente primaria, ubicación y fecha, separadas de los RESULT propios. No exigir RESULT a años, tamaños muestrales bibliográficos o cifras de literatura. El control automático comprobará trazabilidad de afirmaciones cuantitativas, no la mera presencia de dígitos; la revisión sustantiva verificará que la fuente realmente sostiene la afirmación.
6. Actualizar literatura 2025–26 dirigida a las tesis relevantes, con evidencia a favor y en contra, etiquetas (a)/(b)/(c) y límites de transporte. La búsqueda no reemplaza la medición ni se amplía sin una pregunta concreta.
7. No clasificar dominios enteros como no medibles sin justificación. El firewall genético es una restricción del proyecto. Humor, duelo o emociones morales pueden contener estimandos investigables aunque falten instrumentos disponibles.

Conservar la estructura sustantiva del Bloque B y el módulo exigido, con profundidad proporcional a la evidencia. Evitar repetir apartados vacíos para simular cobertura. En cada report debe quedar claro qué cambió frente a v1 y qué decisión permite.

### Entrega y cierre

31 reports v2, índice derivado, tablas de afirmaciones, verificaciones de trazabilidad y propuestas de reglas SI-ENTONCES con tier y falsador. Separar tier de frecuencia y tier del mecanismo. C3 puede avanzar mientras C1 trabaja: declarar validación pendiente y corregir solo las conclusiones afectadas por hallazgos materiales posteriores. No necesita esperar validación total para entregar lotes útiles.

## 6. Organización y secuencia

| Unidad | Responsabilidad | Primera entrega útil |
|---|---|---|
| Astra | Diseño, preguntas sustantivas, lectura de discrepancias y síntesis | Decisiones metodológicas de cada carril y prioridades por valor |
| Codex, sesiones nuevas para C1 | Ejecución técnica en CAJA/NUBE según datos y separación ciega | Primer lote independiente completo y su comparación posterior |
| C2 | Paquetes futuros y evaluación de nuevas familias | Primera familia con emisión congelada, contrato y potencia declarada |
| C3 | Reescritura por lotes | Primer lote de reports con tesis corregidas y evidencia trazable |
| Claude | Recibo conforme al contrato del proyecto | Dictamen por entrega, centrado en reservas materiales |
| Mesa | Adopciones, retiros, excepciones y fusión | Hoja breve de decisiones concretas por carril |

Los tres carriles pueden avanzar en paralelo. Solo dependen entre sí por resultados materiales concretos: una discrepancia de C1 que afecte un report o una emisión se comunica a esos objetos, sin paralizar el resto.

Mantener los perímetros de la misión original. No tocar CI, tablero, derivados protegidos, motor, manifiesto ni los objetos asignados a CIERRE-SEMANAL-1 y PRODUCTO-CONSULTA-1. Reutilizar sus publicaciones fusionadas cuando existan; antes, citar el corte disponible.

Cada lote termina en un PR delimitado, un resultado usable y el recibo previsto; los campos compartidos se incorporan por los mecanismos del repo. No acumular todo el carril en un PR gigante ni generar documentos de control separados si la nota de cierre basta.

## 7. Acuerdo propuesto a dirección

Solicito incorporar estas precisiones a ASTRA-6 sin reducir sus tres objetivos: **validación completa del universo adoptado congelado; seis familias futuras con emisión o dictamen fundado; 31 reports revisados hasta completar el conjunto**.

El éxito no será el número de validaciones, sellos o páginas. Será poder entregar una lista defendible de afirmaciones que conservamos, afirmaciones que cambiamos y pruebas que podrán obligarnos a cambiar de nuevo.

**Este documento prepara el acuerdo y los encargos. No afirma que los carriles hayan comenzado ni que sus resultados estén obtenidos.**
