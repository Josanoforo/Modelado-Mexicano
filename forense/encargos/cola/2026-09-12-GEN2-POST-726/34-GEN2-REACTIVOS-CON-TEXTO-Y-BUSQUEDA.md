# 34 · Hacer encontrables los reactivos que ya tenemos

ENTORNO: CAJA

## Contrato de ejecución autónomo

Repositorio: `Josanoforo/Modelado-Mexicano`. Entorno: Codex CLI en CAJA Windows/WSL. Este MD contiene el encargo completo.

Al despacharlo, Jonás autoriza las fases y el alcance expreso de este documento, los commits, push y PR. La fusión queda con Jonás. No se firman por extensión adopciones, materialidad científica, FP-371/372/373/374, F6 ni acceso comercial. No enviar correos/formularios, aceptar compromisos de terceros o comprar; sí descargar material público y usar accesos previamente autorizados.

Lee `AGENTS.md`; reporta worktree absoluto, rama, SHA y estado. Usa worktree/rama propios. Contrasta main y PR abiertos pertinentes antes de editar: los encargos 27–32 están en ejecución o integración y no deben duplicarse. Corte de esta propuesta: main `e37367581d5186ce4d4cf497377c83ebcd61cf93`, #721–724 fusionados, #725–728 abiertos. El estado cambia: toma el efectivo al comenzar.

Resuelve montaje y dependencias antes de la ejecución. El corpus compartido sirve como entrada; temporales y resultados intermedios van al directorio de cada tarea. No sobrescribas archivos que otra sesión está leyendo. Publica incorporaciones por identidad y de forma atómica con los mecanismos existentes, preservando hashes, padres, sellos y evidencia ajena. No uses salidas GEN1 como insumo numérico GEN2 ni reetiquetes datos conocidos como retenidos.

Reutiliza herramientas y decisiones existentes. Evita otra cola, otro scheduler y wrappers sin necesidad. Valida los riesgos concretos y ejecuta sobre trabajo real: no entregues sólo fixtures, un inventario o un plan. Continúa las fases sin pedir otro encargo. Si una parte depende de un acceso externo, termina las independientes y deja el objeto y acción precisos; no inventes datos ni cierre completo.

Cierra encargo → resultado → evidencia → registros/vistas pertinentes → nota → ADR/L0/rótulo cuando aplique → PR. Actualiza filas comunes por clave canónica; quien integra después concilia y deriva desde el árbol conjunto, sin restaurar tablas completas de su rama. Pruebas dirigidas y gates aplicables, sin limpiar CI heredada ni rehacer la auditoría general.

## Resultado encargado

Completar metadatos de reactivos y hacer que el buscador vigente devuelva preguntas verificables para necesidades actuales. Automatizar la actualización incremental desde fuentes conocidas, sin llamadas LLM ni lectura de valores personales.

**Antecedente:** NC-0136 documentó 102/116 instrumentos con `texto_reactivo` vacío en todas sus filas, dentro de 241,591 filas. Es un diagnóstico histórico; vuelve a medir sólo el perímetro actual. NC-0100 identifica las olas DBF de ENVIPE como caso concreto. No confundir una variable que el buscador no encuentra con una variable que el cuestionario no contiene.

## Fase 1 · Reutilizar el extractor y acotar el lote

Lee `forense/notas/2026-09-10-nc-0123-d14.md`, `tools/inventario_reactivos.py`, `tools/inventario_reactivos_ext.py`, `tools/etiqueta_v1_2.py`, `tools/busca_reactivos.py` y sus tablas vigentes.

Lote prioritario: ENVIPE (especialmente DBF), ENNViH, ENCUCI, ENIF y ENSAFI, sólo objetos conocidos del corpus. Deriva qué campos ya están completos. Instala las dependencias de lectura de metadatos en el entorno local. No lanzar otro extractor general desde cero.

## Fase 2 · Extraer texto acreditado

Usa metadatos nativos cuando existan y diccionarios/cuestionarios oficiales para formatos sin etiquetas. Conserva identidad de instrumento, ola, tabla/miembro y variable. Una etiqueta breve y la pregunta completa son piezas distintas: decláralas por su tipo/procedencia, no inventes un texto ampliado.

Cada incorporación necesita referencia al archivo y hash; para PDF, página/sección y variable exacta. No copiar por nombre de variable entre años: el código puede reutilizarse con otro significado. No inferir población o respuesta válida desde el nombre del archivo. Si no hay texto, conservar ausencia explícita y su fuente pendiente.

No abrir valores de microdatos para extraer etiquetas. OCR, si es necesario, sólo sobre documentación pública y con comprobación de la correspondencia; no tratar su salida sin revisar como texto literal del instrumento.

## Fase 3 · Actualización incremental y consumo

Reutiliza la política de sucesión de los índices existentes y actualiza el consumidor de búsqueda para leer la versión vigente, sin romper citas históricas basadas en posición. Cuando una tabla antigua tiene citas por número de fila, preservarla o publicar un sucesor con mapa de identidad; no reordenarla y fingir que las citas siguen valiendo.

Permite procesar por lista de objetos; cachea por hash de fuente + versión de extractor. Una segunda ejecución sin cambios debe evitar reprocesar archivos. Integra esta operación a la ruta existente de indexación/manual de adquisición en el punto compatible; el cambio al cierre del cron queda para después de integrar #726, sin tocarlo desde esta rama. No añadir otra tarea periódica.

## Fase 4 · Resultado real de búsqueda

Ejecuta búsquedas sobre casos respaldados por cuestionario: denuncia ENVIPE, participación en tandas ENNViH, ahorro ENIF, evento de corrupción ENCUCI y atraso/afrontamiento ENSAFI. Para cada una, mostrar antes/después, variable exacta, texto y fuente. Un cero debe declarar cuántas filas y cuánto texto se revisaron; no presentarlo como ausencia en el universo científico completo.

Entregar índices sucesores utilizables y el buscador conectado, no sólo un reporte de cobertura. Cerrar NC-0100 si queda completo su conjunto DBF; NC-0136 sólo cierra si se demuestra su alcance entero. Si se termina el lote prioritario, conservar el resto cuantificado como residual de la misma NC, sin fingir que las cinco familias son las 116.

## Concurrencia y término

Dueño de herramientas/tablas de inventario de reactivos y del buscador. No modifica motor, CALC, fuentes crudas, cron ni resultados F5. Puede correr con 27–32, 33, 35–37. Consume sólo fuentes conocidas; no indexar ni exponer paquetes retenidos de experimentos prospectivos. Leer el corpus compartido; temporales por tarea y escritura del índice en destino propio antes de publicación.
