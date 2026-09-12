# 43 · GEN2 · SHED: BNPL, daño y universos correctos

ENTORNO: CAJA — Codex CLI Windows/WSL  
RAMA: `acto/gen2-shed-bnpl-dano-universos`  
OBJETO NUEVO: `CALC-SHED2025-BNPL-DANO-0001` (comprobar que no exista o continuar su entrega equivalente).  
PRODUCTO: medición descriptiva de uso, atraso, cargo y sobregiro BNPL en Estados Unidos, con la ruta de preguntas resuelta y límites explícitos para N34.

## Contrato autónomo de ejecución

Repositorio: `Josanoforo/Modelado-Mexicano`. Preparado para Jonás el 12/sep/2026 contra `main=6e634aaaa3dec6ed536bae1ef142a4f7ff56cfae` (#741, paquete 39/40 encolado). 39 y 40 están corriendo. Este archivo se puede entregar solo a Codex CLI en CAJA Windows/WSL.

Al despacharlo, Jonás autoriza abrir y congelar la spec de los estimandos descriptivos definidos en este encargo, adquisición pública pertinente, implementación, ejecución completa con datos reales, registro, commits, push y PR propio. Esa instrucción resuelve la apertura de spec para este objeto; no volver a solicitarla porque un antecedente dijera «mesa decide si abre especificación». No autoriza adopción al motor, causalidad nueva, cambio de tiers, experimento F5, gasto de proveedor, compras o contacto externo. Las fusiones quedan con Jonás.

Lee `AGENTS.md`, el encargo entero y el procedimiento pertinente de `.claude/commands/acto.md`. Reporta worktree absoluto, rama, SHA y estado; usa una tarea por worktree/rama/PR y archiva por el 0-bis vigente. Revisa sólo entregas posteriores del mismo objeto y ejecuta el residual si ya hubo avance. La coordinación conocida de las dos ramas de 39 queda con su sesión; no investigarla ni intervenirla.

Comprueba los IDs de entrada con el resolvedor y manifiesto. Existen las raíces lógicas `data_raw` y `descargas_mx`; no todas las fuentes viven bajo la misma ruta. El corpus compartido de `data_raw` está en `/home/pc0/mm-corpus/raw`. Resuelve montaje, permisos de lectura y dependencias antes de declarar ausencia. Recupera únicamente objetos faltantes o documentos nuevos pertinentes; no rehagas las olas de descarga. Bytes y microdatos permanecen fuera de Git; publica agregados, código e identidades según la vía vigente.

Congela fuente/versión, población, unidad, codificación, pesos, filtros, faltantes, transformaciones y salidas antes del cálculo. Los códigos provienen del documento exacto de cada edición. No ajustes definiciones para recuperar una cifra histórica. Separa estimación nueva, reproducción de un cálculo existente y transcripción de una tabla publicada. No vuelvas a sellar un resultado viejo como medición nueva.

Continúa todas las fases sin pedir otro encargo. Cuando falte una elección científica fuera del contrato, completa primero las partes independientes y entrega opciones concretas. Un fallo de transporte o acceso requiere uno o dos intentos razonables, alternativa directa y residual con objeto/acción; no inventes un dato ni detengas el resto. No enviar solicitudes ni aceptar compromisos de acceso en nombre de Jonás.

Perímetro excluido de los tres encargos: `tools/adq_*`, `tools/adquiere_*`, `data/adq-*`, Task Scheduler, configuración de SONDA, extractor/overlay/buscador de 39, consumidores y emisor de 40, capturas y congelados F5. Reutiliza lectores existentes sin modificarlos cuando sea posible. Cada frente escribe su propio medidor/spec/resultados; los cambios indispensables a un helper compartido se coordinan por archivo y se mantienen mínimos.

Registros y cierres se integran por clave con los escritores canónicos. 40 conserva la conciliación de NC-0165, la proyección general y el cierre global de NC-0164; estos frentes le entregan evidencia consumible, no sobrescriben esa NC ni la cierran por producir una capa parcial. Banxico y SHED actualizan únicamente su propia relación N34. N35 actualiza su relación específica y preserva sus reservas. Las altas de manifiesto/cola y la cascada se concilian sobre el árbol combinado, sin reemplazar tablas enteras.

Finaliza spec → ejecución → CALC/RESULT y sello cuando corresponda → comprobación material → agregados y ficha de uso → registros propios → nota/cierre existente → PR. Propaga contador científico sólo con la autoridad de objeto exigida por el procedimiento; no confundir autorización de cálculo con adopción, ni contar descargas como medición. Pruebas dirigidas y gates requeridos, comparando baseline; no limpiar fallos heredados ni añadir totales rígidos. La entrega no termina en fixtures, diagnóstico o propuesta cuando puede completar la ejecución autorizada.

## Base disponible y hueco concreto

#734 ya incorporó `gen2_federal_reserve_shed_2025_public_csv` y `gen2_federal_reserve_shed_2025_codebook`. Su cierre documentó 12,934 personas y una tabla de cobertura; no midió los estimandos ahora encargados. Reutiliza la lectura de `tools/extrae_n34_producto_dano.py` sin editarla desde este frente; conserva `data/n34-producto-dano/shed-bnpl-cobertura.csv`.

La [página oficial SHED](https://www.federalreserve.gov/consumerscommunities/shed_data.htm) mantiene los objetos 2025. El [codebook](https://www.federalreserve.gov/consumerscommunities/files/SHED_2025codebook.pdf) distingue pesos transversales de pesos de panel. Se utilizará el corte transversal con `weight`; no abrir un panel o descargar todas las olas.

Se localizó el [cuestionario oficial, apéndice A](https://www.federalreserve.gov/publications/2026-supplemental-appendixes-report-economic-well-being-us-households-2025-appendix-a.htm), que resuelve el filtro pendiente de #734: `BNPL1A` se pregunta cuando `BNPL1=1` y `BK2_f=1`. También indica que `BNPL3A` se pregunta ante atraso afirmativo o rechazo de respuesta en `BNPL3`. Debes conservar esa diferencia entre elegibilidad y respuesta válida.

## Fase 1 · Completar documentación y contratos

Verifica los dos IDs existentes. Recupera y registra el apéndice A como documento fuente si aún no está en corpus; el HTML oficial puede bastar, no se exige PDF si añade los mismos datos. Resuelve `BK2_f`, bancos/filtros precedentes, `BNPL1`, `BNPL3`, `BNPL3A`, `BNPL1A` y `BNPL4_e` contra cuestionario, codebook y CSV exactos.

El CSV puede usar etiquetas textuales mientras el codebook muestra números. Congela la traducción exacta; no reutilices ciegamente códigos de otra ola. Separa no aplica, rechazo, no sabe, no y sí. Un faltante fuera de la ruta no es respuesta negativa.

Confirma unicidad de `shedid`, pesos positivos y el universo de cada pregunta. Los conteos publicados por #734 son controles de identidad/cobertura, no porcentajes poblacionales ni umbrales científicos.

## Fase 2 · Estimandos autorizados

| Estimando | Población de análisis | Resultado |
|---|---|---|
| Uso de BNPL | Todas las personas con BNPL1 válido | Proporción ponderada de uso durante el periodo preguntado |
| Atraso BNPL | Usuarios BNPL con BNPL3 válido | Proporción ponderada de atraso |
| Cargo por atraso | Usuarios con atraso afirmativo y BNPL3A válido | Proporción de cargo dentro de ese grupo, mostrando por separado respuestas de la ruta «rechazó BNPL3» |
| Sobregiro atribuido a BNPL | Usuarios BNPL con sobregiro previo declarado, según ruta BK2_f, y BNPL1A válido | Proporción condicional; no porcentaje de todos los usuarios BNPL |
| Asequibilidad y atraso | Usuarios BNPL con BNPL4_e y BNPL3 válidos | Tabla 2×2 ponderada y diferencia descriptiva de atraso entre respuestas sí/no al motivo |

Para todos: n elegible, n válido, positivos, masas, faltantes por razón, punto y definición exacta. Presenta los denominadores junto a los porcentajes para que la tasa condicional de cargos o sobregiros no se lea como prevalencia general.

No reconstruir una tasa global de sobregiro asignando cero a los demás usuarios ni multiplicar porcentajes de universos diferentes. Si resulta posible una cantidad global, requiere antes documentar toda la ruta y una spec sucesora fuera de este perímetro; no bloquea las cinco mediciones definidas.

No agregar un indicador compuesto «cualquier daño»: combina preguntas con bases distintas y no es necesario para entregar el producto. No interpretar el motivo de asequibilidad como tratamiento causal. No transportar tasas a México, promediar con Banxico/ENSAFI ni tomar CFPB default a 120 días como el mismo desenlace de atraso autodeclarado.

La entrega principal son puntos y asociación descriptiva. EE/IC sólo si existe procedimiento acreditado aplicable; pesos de postestratificación por sí solos no identifican todo el diseño. No inventar UPM o presentar un bootstrap de filas como varianza oficial.

## Fase 3 · Cálculo real y contraste

Congela y ejecuta `CALC-SHED2025-BNPL-DANO-0001`, con agregados propios, por ejemplo `data/shed2025-bnpl-dano/`. Completa las cinco salidas; si falla una ruta, termina las demás y cuantifica qué registros/campos impiden la afectada.

Verifica un cociente de uso y uno condicional de forma independiente. Añade protección dirigida contra el error real de usar todos los usuarios como denominador de BNPL1A y contra mezclar códigos numéricos con etiquetas. Revisa que las observaciones con BNPL3 rechazado no entren como atraso afirmativo a la tasa de cargo.

Contrasta los puntos con una tabla oficial sólo si tiene idéntico universo/definición. Una discrepancia de denominador se explica; no se ajustan exclusiones para igualarla. Cita los resultados estadounidenses como descriptivos de ese instrumento, sin aseveración causal.

## Fase 4 · Producto y cierre

Entrega CALC/RESULT, tabla legible de numeradores/denominadores, ficha de uso extranjero, documento fuente del filtro y un gráfico sencillo con las bases explícitas si facilita lectura. Actualiza por clave únicamente la relación `REL-85fc542cc3c6ac0bb4b0d34c`, objeto `OE-6eb9c3712c56d21187da0e70`.

40 recibe resultados exactos y evidencia de la ruta; conserva el cierre global de NC-0164. 41 mantiene Banxico. No modificar el lector compartido, archivos de Banxico, corpus CFPB ni registros de 39. Si una mejora común resulta indispensable, aislarla y acordar su dueño antes de editar, continuando el medidor propio mientras tanto.

Aceptación: cinco mediciones reales o residual específico por la afectada, filtro de sobregiro acreditado desde fuente oficial, denominadores correctos, ninguna tasa mexicana inferida y PR. El cron sólo es útil si falta el nuevo apéndice o un ID de entrada; no necesita otra descarga general de SHED.

## Prompt de lanzamiento

> Ejecuta completo el encargo 43 en CAJA y worktree propio. Autorizo abrir/congelar la spec descriptiva SHED 2025, obtener el apéndice oficial que falte, calcular las cinco salidas con sus universos y entregar CALC/RESULT, informe y PR. Resuelve BNPL1A desde BNPL1 y BK2_f; no uses todos los usuarios como denominador ni conviertas faltantes en no. Todo resultado conserva Estados Unidos y uso no causal. 41 posee Banxico y 40 demanda/motor/NC global; tu propiedad es SHED y su relación. El merge queda conmigo.
