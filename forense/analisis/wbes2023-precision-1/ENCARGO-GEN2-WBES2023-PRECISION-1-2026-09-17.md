# ENCARGO · GEN2-WBES2023-PRECISION-1

**Entorno:** Codex CLI en CAJA; lectura metodológica también posible en Claude Cloud, pero una sola ejecución y un PR.  
**Producto:** una extensión de precisión del resultado descriptivo WBES 2023 de #832, con intervalo justificado cuando sea calculable y diagnóstico concreto de su alcance. Resolver la limitación real del resultado; no repetir su extracción como nueva medición independiente.

## 1. Pregunta y base

`CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001` ya produce el compuesto propio de solicitudes/expectativas de pagos informales y seis tasas separadas. Usa wmedian. El total entre clasificables es aproximadamente 15.24%; sus límites de faltantes 14.89%–17.21% **no son IC**. El estudio no acreditó procedimiento operativo completo de varianza por dominio y estratos singulares.

La pregunta de este acto: **¿qué precisión muestral se puede sostener para el total y los cuatro tamaños ya publicados, con el diseño y datos disponibles?** No redefine el compuesto, no intenta reproducir el agregado oficial distinto ni abre otra ola. Se conocen los puntos: ésta es extensión metodológica descriptiva, no confirmación ciega.

Leer:

- `forense/analisis/wbes2023-descriptiva-1/lectura-TRA-WBES2023.md`, especialmente limitaciones.
- `data/corrida0/CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001/`: spec, medidor, resultados y sellos.
- Cuatro objetos ya registrados: `wbes_mexico_2023_ddi_xml`, `wbes_mexico_2023_ddi_pdf`, `wbes_mexico_2023_microdato_dta_zip`, `wbes_mexico_2023_documentacion_zip`. Resolver por manifiesto, no volver a descargarlos.
- Del ZIP documental, *Mexico 2023 ES Implementation Report*, §§II.1–II.2 y III.6–III.8, más cuestionario/DDI en lo que corresponda al diseño.

## 2. Resolver diseño antes de elegir varianza

1. Identificar diseño real de México 2023: estratificación, etapa(s), unidad(es) de muestreo, marco, selección con/sin reemplazo, sobrerrepresentación y ajustes de peso/no respuesta. Verificar cómo se materializa en columnas del archivo. No inferir estratos de a6a (tamaño publicado) ni fabricar UPM de un identificador único sin que el diseño lo sostenga.
2. No exigir una variable UPM si la documentación acredita muestreo de establecimientos en una sola etapa; sí exigir el vínculo correcto entre la selección descrita y el estimador empleado. Estrato de selección y dominio de publicación son objetos distintos.
3. Primero agotar los cuatro documentos disponibles. Si falta una receta operativa, buscar **sólo documentación metodológica oficial de Enterprise Surveys/World Bank** aplicable a México 2023. Se autoriza una búsqueda acotada, hasta tres documentos relevantes, sin nuevas bases ni otra ola, sin cuentas/contratos/correos. Descargar sólo lo que aporte diseño, pesos o varianza; un texto genérico no se presenta como acreditación de una implementación mexicana particular.
4. Comprobar si los singleton existen en la muestra completa o aparecen por filtrar al dominio. Construir la varianza desde la muestra elegible para el diseño, conservando contribuciones cero fuera del dominio. No descartar primero a los no expuestos y después fingir que ése era todo el muestreo.
5. Seleccionar antes del nuevo IC la vía mejor respaldada: replicación provista oficialmente, linealización bajo diseño acreditado, o aproximación explícita bajo supuestos declarados. Documentar fuente/página, estimador y tratamiento de singleton/fpc/grados de libertad. No hace falta que el reporte oficial prescriba cada decisión computacional para usar una aproximación estadística defendible, pero los supuestos deben quedar visibles.
6. Distinguir tres resultados legítimos: `IC-DISEÑO-ACREDITADO`, `IC-APROXIMADO-CONDICIONAL-A-SUPUESTOS` o `PRECISION-NO-ESTIMABLE-CON-ESTE-DATO`. No llamar oficial a un IC propio, ni detener la descripción por no lograr la opción más fuerte.

Presupuesto: resolver la documentación con una pasada y una alternativa directa. Si falta una pieza estructural irrecuperable públicamente, terminar con su nombre exacto y el efecto sobre el resultado, conservando puntos/límites existentes. No redactar otra política de muestreo ni ampliar una campaña de solicitudes.

## 3. Contrato estadístico acotado

El alcance numérico es **cinco dominios del compuesto propio**: total, pequeña, mediana, grande y extra grande. Mantener filtros, códigos, elegibilidad, wmedian, tratamiento de faltantes y denominadores del padre. No optimizar su definición para estrechar el IC.

- Punto entre clasificables: `sum(w*I[positivo])/sum(w*I[clasificable])`. Al calcular varianza, el numerador y denominador comparten observaciones y diseño. La incertidumbre de la razón no se obtiene suponiendo independencia entre ambos.
- Dominio expuesto, elegibilidad desconocida y desenlace desconocido se conservan separados. La precisión de ese punto condicionado a clasificables no elimina el sesgo por no respuesta ni lo transforma en una estimación plenamente identificada para todos los expuestos.
- Emitir intervalo 95% y EE cuando tengan sentido, n no ponderado, masa, número de estratos/unidades de muestreo y singleton relevantes. Definir transformación/tratamiento de proporciones frontera antes de ejecutar; no presentar un IC [0,0] como certeza por ausencia de eventos.
- Los límites lógicos por faltantes del padre deben conservarse en columnas separadas. **No son** el IC del punto ni se mezclan con él como una sola banda sin cobertura definida. No se requiere construir un IC conjunto del conjunto identificado en este acto.
- No comparar tasas WBES y ENCRIGE, ni inferir significancia entre tamaños mediante traslape de IC marginales. Este encargo entrega precisión; no realiza una batería de pruebas o rankings de tamaño.
- Si una política de singleton requiere supuestos materiales, fijar como máximo dos escenarios defendibles de antemano y mostrar ambos, sin escoger el de menor error estándar. No colapsar estratos por cercanía de tasas. Una aproximación con reemplazo debe etiquetarse y no presentarse automáticamente como cota garantizada.

## 4. Implementación y ejecución

1. Crear un sucesor propio, sugerido `CALC-WBES2023-PRECISION-0001`, con spec humana/mecánica que cite padre e inputs exactos. El padre y su sello quedan intactos. Añadir sólo campos de diseño y resultados de precisión necesarios.
2. **COMMIT 1:** contrato y código probado con sintéticos antes de generar los IC reales. Reutilizar transformación del padre sin editarlo; si importar su medidor no es viable, contrastar las cinco cantidades de punto/denominador después y exigir reproducción al grano/tolerancia declarados. Un punto que cambie se investiga antes de atribuir el cambio a «más precisión».
3. Implementar con una librería de encuestas o rutina existente adecuada; preferir una vía probada antes que escribir un motor de varianza. Verificar documentación de la versión usada. Si hace falta una implementación pequeña, comprobar contra un caso analítico y un cálculo independiente acotado; no implementar simultáneamente tres métodos para buscar coincidencia.
4. **COMMIT 2:** una ejecución real y verify dirigido. Publicar tabla padre/sucesor con puntos idénticos y precisión nueva o limitación concreta. Conservar la identidad y el tipo de los límites por faltantes.
5. Entregar lectura de máximo dos páginas: qué precisión se agregó, qué supuestos cuesta, qué comparaciones siguen injustificadas y cómo cambió la interpretación del resultado. No editar aún el informe TRA canónico: entregar una inserción lista.

## 5. Pruebas y perímetro

Pruebas necesarias: razón ponderada con pesos desiguales; varianza de dominio que conserva las unidades de contribución cero; singleton real frente a singleton creado por filtro; rechazo de campo de diseño inventado/ausente; reproducción exacta de los puntos del padre; límites por faltantes no etiquetados como IC. Las pruebas cubren el problema, no nomenclatura.

Permitidos: CALC sucesor y prueba focal propios; `forense/analisis/wbes2023-precision-1/`; encargo y cierre propios. Documentación nueva pública, si es indispensable, fuera de Git en corpus con **adiciones precisas de manifiesto** (máximo tres), sin tocar las entradas ENCO. Conservar ambas adiciones al sincronizar; no regenerar inventarios globales.

Prohibidos: modificar CALC/medidor/sellos/CSV del padre, datasets, pesos originales, motor, panel F6, `tools/corrida0.py`, `tools/relevo_usos.py`, registros globales, cron y análisis ENCRIGE en curso. Cero datos WBES 2006/2010/panel/2026 y cero llamadas experimentales.

Cierre suficiente: las cinco estimaciones tienen precisión defendible y tipada, o una limitación estructural demostrada con receta mínima y sin falso IC. No basta repetir «no hay IC»: explicar qué se intentó, qué variable o supuesto falta y por qué impediría el método. Si el diseño sí es operativo, **calcular y sellar**, no cerrar con una propuesta para otro encargo. La incertidumbre no se mejora por cambiar una etiqueta ni por añadir un sello nuevo.

## Autoridad, arranque y trabajo simultáneo

Encargo para lanzar por Jonás · emitido 17/sep/2026 UTC (la sesión en CDMX puede seguir fechada 16/sep). Repositorio: `Josanoforo/Modelado-Mexicano`. Base consultada: `main @ fe223a9d5f14c609327d7d30181295b4469d43ae`. Las premisas descritas corresponden a ese corte; al ejecutar manda `origin/main` vigente. Este documento no es una firma ya registrada: su prompt final define lo autorizado al lanzarlo.

1. Lee este archivo completo, `AGENTS.md` y las instrucciones aplicables a los archivos del perímetro. Reporta worktree absoluto, rama, HEAD y `git status --short`. Haz fetch y consulta PR/ramas del rótulo para no duplicar una ejecución. Revalida sólo las premisas materiales.
2. **Puedes continuar en la misma sesión CLI.** Si su PR anterior fue fusionado, usa un worktree y una rama sucesora desde `origin/main` para este encargo. No reaproveches el nombre de una rama fusionada para esconder un acto nuevo. Si hay cambios posteriores sin publicar, consérvalos: determina con diff cuáles corresponden a este encargo y traslada sólo esos cambios con commits/parches explícitos, sin reset, limpieza ni stash de árboles ajenos. Si ya corre exactamente este encargo, continúa su rama y PR; no abras un duplicado. Un squash merge no acredita ancestralidad por sí solo: compara el contenido pertinente.
3. No ejecutes este encargo encima de otro todavía activo. Sincronizar cambios propios y resolver conflictos locales de implementación está autorizado; no interpretar una contradicción científica como conflicto de texto resoluble automáticamente.
4. Los corpus se resuelven con `tools/entorno.py`, las raíces existentes y `tools/prepara_corpus.py` según sus opciones reales. Un worktree sin `data/raw` no significa que falten archivos en CAJA. No copies microdatos a Git ni expongas rutas privadas, credenciales o identificadores individuales en entregables.
5. Al lanzar quedan autorizados los cambios delimitados, pruebas pertinentes, commits, push sin force y un PR por encargo. **Las fusiones quedan con Jonás.** No enviar correos, mensajes ni solicitudes a terceros. Cero llamadas de brazos experimentales a modelos; usar CLI para desarrollar no equivale a emitir L.

### Separación respecto del trabajo en curso

Opus conserva CAREO / CELDA-D-PILOTO-1 / TRÁMITE-4, firmas, crosswalk, corte de edad, θ y magnitud de G5. WBES2023-DESCRIPTIVA-1 (#832) y L8-LINAJE-HEREDADO-1 (#833) ya están fusionados. ENCO-DOS-OLAS-RESERVADAS-1 (#834) sigue abierto en el corte revisado. RELEVO-REMESAS-F3-1 y ENCRIGE-CARGA-INTENSIDAD-1 se consideran en curso: conservarles tools/relevo_usos.py, la vista de relevos y su análisis ENCRIGE. ENCIG agregado (#831) y ENVIPE-RES0028-U4 (#830) están fusionados; no repetirlos. MEDICION-DEMANDA-3 mantiene su dueño y alcance ENADID/remanente; no tomarlo desde esta tanda. F6 mantiene sus reservas.

**No abrir ni derivar ENIF 2024 localidad × edad**, ni leer las capturas o resultados reservados del piloto. No leer desenlaces retenidos de MOCIBA/ISSP, ENCRIGE 2016 ni WBES 2026. Antes de correr comandos generales, comprobar que no abran/deriven esas reservas como efecto lateral. El corpus de los brazos L no se amplía.

Excepción temporal de cascada autorizada al lanzar: archivar el encargo verbatim con procedencia/consumo fuera del bloque y publicar su producto, pero diferir `decisiones.tsv`, `forense/no-corrido.tsv`, firmas, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar numeración ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --escribe`. Cada PR enumerará únicamente las propagaciones necesarias después del trámite de Opus, bajo **CIERRE COMPARTIDO DIFERIDO**. En esta tanda no se edita la vista de relevos. Sólo WBES admite adiciones de manifiesto de documentos metodológicos realmente adquiridos, según su perímetro; no autoriza registro global ni cambios de otras entradas.

Una modificación de SHA o un defecto de nomenclatura no detiene el producto. Resolver un bloqueo con uno o dos intentos razonables, una alternativa directa y una receta concreta; continuar las piezas independientes. No ampliar a auditoría general. Aproximadamente 20% del esfuerzo como máximo en control, salvo riesgo material de datos.

## Cierre y entrega comunes

Sincroniza `origin/main` antes del push final; revisa diff y ejecuta las verificaciones afectadas. No rehagas mediciones por cambios documentales. No debilites checks ni recongeles baseline. Compara fallos heredados con la base sólo cuando afecten la entrega; corrige dependencias declaradas del entorno antes de atribuir el fallo al código. Si CI exige una escritura compartida fuera de alcance, entrega el producto probado y el impedimento exacto para integración serial, sin fingir verde.

Devuelve: qué producto cambió y qué decisión permite; enlace al PR y artefactos; SHA base/final; comandos realmente ejecutados; pruebas/CI; reservas materiales y máximo tres decisiones pendientes con su objeto preciso. Distingue PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR o un sello no constituye adopción científica. Una tabla de planes sin ejecutar lo disponible no satisface el encargo.

Termina cuando exista el producto usable y siguiente acción clara; no refines por inercia. Explica en una frase si quedó más cerca una medición, explicación o decisión mejor.



## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-WBES2023-PRECISION-1 en CAJA. Autorizo resolver el diseño con documentación existente y hasta tres documentos metodológicos públicos imprescindibles, registrar sólo esas adiciones de manifiesto, comprometer método y código, y calcular/sellar precisión para los cinco dominios del compuesto propio sin cambiar sus puntos. Autorizo pruebas, commits, push y PR; fusión conmigo. No redefinas el estimando, mezcles límites por faltantes con IC, leas otras olas ni ejecutes adopciones. Aplica cascada diferida y conserva la concurrencia con ENCO/F-3/ENCRIGE. Si el diseño permite un cálculo defendible, ejecútalo; si no, devuelve la pieza faltante y la limitación concreta, sin fabricar incertidumbre.
