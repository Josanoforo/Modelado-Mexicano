# 41 · GEN2 · Banxico: producto, atraso y costo percibido

ENTORNO: CAJA — Codex CLI Windows/WSL  
RAMA: `acto/gen2-banxico-producto-atraso-costo`  
OBJETO NUEVO: `CALC-BANXICO-PRODUCTO-DANO-0001` (comprobar que no exista; reutilizar el objeto si ya se inició legítimamente).  
PRODUCTO: mediciones ponderadas por producto y ola, con denominadores correctos, descripción de asociación y un informe utilizable para N34/R1.7.

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

## Base disponible y utilidad

#734 adquirió datos y comprobó estructura, pero no corrió estos estimandos. El cierre `forense/notas/2026-09-11-GEN2-N34-DATOS-PRODUCTO-Y-DANO-cierre.md` documenta 12,408 filas persona-ola, 2019–2024, y cinco categorías de crédito. El alcance es personas usuarias de 18–70 años en localidades de 50 mil habitantes o más: no representa automáticamente todo México rural ni población sin productos.

Entradas de manifiesto:

- `gen2_banxico_satisfaccion_usuarios_2019_2024_microdatos`.
- `gen2_banxico_satisfaccion_usuarios_2019_2024_manual`.
- `gen2_banxico_satisfaccion_usuarios_2024_informe`.

Reutiliza como referencias el lector XLSX de `tools/extrae_n34_producto_dano.py` y `data/n34-producto-dano/banxico-cobertura-producto-ola.csv`. Conserva esa extracción histórica. La relación propia es `REL-defde50a805b668d2f395b84`, objeto `OE-080f605caa1d07c7558b3d89`.

Fuente oficial para recuperar sólo lo ausente: [Banco de México, satisfacción de personas usuarias](https://www.banxico.org.mx/publicaciones-y-prensa/indicadores-de-satisfaccion-de-los-usuarios-de-ser/servicios-financieros-satis.html). Las URLs de los tres archivos ya están en el manifiesto.

## Fase 1 · Contrato fuente-variable

Confirma hoja, edición, pesos positivos y cobertura. No asumas panel longitudinal porque el XLSX contenga seis olas: trata cada una como corte separado salvo documentación que identifique seguimiento. No sumes masas de olas como una población ni sumes usuarios de productos no excluyentes como personas distintas.

Mapea `fecha`, `ponderador`, los filtros de `tdc`, `hip`, `per`, `nom`, `aut` y sus campos de comportamiento de pago, intereses, problemas y reclamación. Por cada ola, distingue variable no levantada, salto, rechazo/no sabe y respuesta válida. #734 detectó ausencia de comportamiento de pago en 2019 para hipotecario, nómina y automotriz: confirma y conserva esas salidas como no estimables, nunca cero atraso.

El manual determina qué categorías significan atraso e imposibilidad de pago. Congela el conjunto exacto y publica también la distribución completa de respuestas; no equipares pago mínimo con impago sin respaldo del reactivo.

## Fase 2 · Estimandos autorizados

Para cada producto × ola disponible:

1. Distribución ponderada del comportamiento de pago entre tenedores con respuesta válida.
2. Proporción que declara atraso o imposibilidad de pago, separando ambas categorías cuando el instrumento lo permita.
3. Proporción que reporta problemas; proporción de reclamación en el subuniverso exacto de su pregunta. Nunca usar todos los tenedores si el cuestionario sólo pregunta a quienes tuvieron un problema.
4. Distribución conjunta de costo percibido y comportamiento de pago, sobre las categorías originales de la escala de intereses; mostrar n, masa y faltantes. No convertir la calificación 0–10 en tasa, CAT o monto.

Para el corte 2024, entrega además la tasa de atraso/imposibilidad por cada nivel válido de costo percibido, dentro de producto, sin colapsar bandas para favorecer una tendencia. Las celdas pequeñas muestran su tamaño y limitación; no se imputan ni desaparecen. No estimar efectos causales ni ejecutar selección de modelos por significación.

En cada estimando: `producto | ola | variable/códigos | universo | n elegible | n válido | n positivo | masa elegible | masa válida | masa positiva | faltantes por causa | estimación | unidad | alcance`.

La meta principal son puntos ponderados. Calcula EE/IC sólo si el diseño y su procedimiento quedan acreditados por documentación/variables; no inventes UPM, estratos o supuesta representatividad inferencial. Su ausencia no bloquea estos descriptivos.

## Fase 3 · Ejecutar, verificar e interpretar

Congela la spec conforme a corrida0, ejecuta el medidor sobre los bytes de CAJA y produce agregados en un directorio propio, por ejemplo `data/banxico-producto-dano-medicion/`. La misma rutina debe recorrer todos los productos/olas compatibles; no dejar cuatro de cinco productos para otro encargo tras conseguir un ejemplo.

Comprueba de forma independiente un cociente numerador/denominador de 2024, un caso de pregunta filtrada y el caso no levantado en 2019. Usa las masas/tenedores ya comprobadas contra el cuadro oficial de #734 como control, sin repetir toda su adquisición.

Entrega una lectura breve por producto y evolución temporal sólo donde reactivo/universo sean comparables. Si cambia instrumento o universo, conserva valores separados y declara ruptura. Un cambio entre cortes no identifica transición de la misma persona ni efecto del costo.

## Fase 4 · Producto consumible y cierre

Entrega CALC/RESULT sellados según el procedimiento, tabla CSV/TSV, un gráfico agregado legible si ayuda y una ficha de consumo para 40: fuente, población, periodo, resultado exacto, propósito descriptivo/asociativo, reserva y comando de reproducción.

Actualiza sólo la relación Banxico de N34 con la medición efectivamente disponible; NC-0164 sigue abierta por producto/lender mexicano exacto, costo objetivo e identificación causal. No sustituyas la probabilidad del motor por estos puntos ni reutilices el RCT Compartamos como identificación de Banxico.

Aceptación: medición real de todas las celdas viables del contrato, distinción de faltantes, proporciones con denominadores auditables, fuente urbana explícita, oferta utilizable por 40 y PR. Si todos los insumos están montados, no se necesita activar el cron para este encargo.

## Prompt de lanzamiento

> Ejecuta completo el encargo 41 en CAJA y worktree propio. Autorizo abrir/congelar la spec descriptiva Banxico, calcular los estimandos definidos con los datos ya adquiridos, verificar los riesgos materiales, registrar y entregar PR. No es otra adquisición ni adopción automática. 40 lleva la demanda/motor y 43 la medición SHED; tu propiedad es Banxico y su relación N34. Continúa hasta medición e informe consumibles. El merge queda conmigo.

## A.8 · medición previa comprobada antes de fijar estados

```text
$ python3 tools/ya_medido.py R1.7
resuelto por canon: R1.7 -> id dinero.credito.baja_friccion_usura_dano_downstream
milpa/tramite.yaml: sin apariciones
milpa/tramite-ola5-propuesta-v0.yaml: sin apariciones
data/corrida0: sin apariciones
canon/modelo-decision-v4_0.md §7: R1.7, tier [MEDIA], medido No
NUNCA-MEDIDA
```

## NO-CORRIDO / RESERVAS

Ninguno. Se ejecutaron todas las piezas autorizadas. Las exclusiones expresas
(adopción, causalidad, cierre de `NC-0164` y merge) no son trabajo residual de
este acto.

## CONSUMIDO

Ejecutado por [PR #746](https://github.com/Josanoforo/Modelado-Mexicano/pull/746),
rama `acto/gen2-banxico-producto-atraso-costo`, HEAD al abrir el PR
`6d708d6cdbda80e3ce0501c5d818e5993a6658e0`, contra
`origin/main=cfa8c516a43952212f945f87f62d342d42010b69`. La spec y el medidor se
congelaron antes del cálculo; `CALC-BANXICO-PRODUCTO-DANO-0001` reproduce
35/35 RESULT con contexto idéntico y el control independiente coincide. Se
publicaron todos los productos/olas viables, sus denominadores y faltantes,
agregados, gráfico, ficha para 40, actualización exclusiva de la relación
Banxico N34 y cascada `ADR-491`. Cero adopciones y `NC-0164` permanece abierta.
El PR no fue fusionado por el ejecutor; la fusión queda con Jonás.

La comprobación se hizo antes de registrar el CALC de este acto. La nueva
medición es descriptiva/asociativa y no equivale a adopción de R1.7.

## NO-CORRIDO / RESERVAS

Ninguno. Se ejecutaron todas las piezas autorizadas. Las exclusiones expresas
(adopción, causalidad, cierre de `NC-0164` y merge) no son trabajo residual de
este acto.
