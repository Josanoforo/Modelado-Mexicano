# Encargo 20 · fuentes financieras y series utilizables

ENTORNO: CAJA
RAMA SUGERIDA: acto/gen2-fuentes-financieras-20
MODELOS: cero llamadas nuevas.

## Resultado útil y autoridad

Obtener y dejar utilizable la serie oficial de morosidad de crédito al consumo; explotar los archivos CONDUSEF que ya existen; resolver qué documentación ENCRIGE falta realmente. D17 autorizó mover la obtención de datos. Este encargo concreta esa autorización y permite extracción descriptiva, código, commits, push y PR; no firma parámetros del motor ni cambia los criterios científicos pendientes.

Puede correr junto a 17–19, 21 y 22. No necesita las cuatro firmas del benchmark. Gen1 aporta preguntas y nombres de consumidores, no valores objetivo que deban reproducirse.

## Fase 1 · resolver fuentes y consumidores sin redescubrirlos

Leer `AGENTS.md`, `.claude/commands/acto.md`, este encargo y sólo estos antecedentes y sus referencias pertinentes:

- `forense/notas/2026-09-06-MAESTRA38-A6-PAQUETE-RECETAS-11.md`;
- `forense/notas/2026-09-10-GEN2-ADQUISICION-DIRIGIDA-cartera.md`;
- filas `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` y `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF` en `data/curacion-registro/cola-adquisicion-registro.tsv`;
- sus entradas de `data/manifiesto.yaml`, consumidores R1.6 / `dinero.credito.scoring_alternativo` y N34 / `dinero.credito.baja_friccion_usura_dano_downstream`.

Reportar worktree absoluto, rama, HEAD, estado y corpus. Partir de main actual; corte de preparación #707, `cd92cb25acbb7b645a4b49ed180f042661d18e7e`. Comprobar ramas/PR del mismo objeto y tomar sólo residuales. Si Cloud recibió este encargo, puede resolver documentación/código, pero debe trasladar la extracción al CLI con corpus; no afirmar que una ausencia en Cloud implica falta de datos del proyecto.

Los 29 CSV CONDUSEF ya se adquirieron. Verificar sus identidades y aprovecharlos. No volver a descargar ENAFIN, WBES, Findex o ENVIPE; ya se revisó su cobertura. No incorporar como fuentes empíricas los documentos de encargos que aparecen entre los nuevos archivos del censo #707.

## Fase 2 · CNBV: obtener la serie y hacerla legible

Usar el portal oficial vigente y la receta existente. La barrera anterior incluyó cadena TLS y un reporte ASP.NET con selección/postback, no un CSV estático. Usar certificados oficiales y el flujo del portal; no desactivar verificación TLS ni repetir peticiones a un enlace que sólo devuelve el formulario. Si la descarga requiere interacción normal de navegador, preparar o ejecutar ese paso en el entorno autorizado.

Fijar antes de extraer: indicador IMOR, periodicidad mensual, institución/universo, productos y tramo temporal que el archivo realmente ofrece. Preferir la serie histórica disponible del reporte solicitado; no ampliar por cuota a toda CNBV. Mantener separados total de consumo y desgloses de producto cuando existan; no inventarlos ni asignar a un segmento poblacional un producto de crédito.

Entregar bytes originales fuera de Git, URL/fecha/edición/hash y un extractor reproducible. Producir tabla ordenada con fecha, producto/universo, indicador, valor, unidad, fuente y notas de ruptura/revisión. Distinguir porcentaje de fracción. Registrar faltantes explícitos; no rellenarlos con cero ni interpolarlos para aparentar continuidad. Revisar duplicados de periodo/producto y contrastar puntos de principio, medio y final contra la fuente original.

El IMOR referido a saldos es una razón de cartera, no una probabilidad individual de impago. Las cifras históricas «15–20%» o «25–30%» del antecedente no son umbrales autorizados de Gen2 ni criterios para elegir una serie. La entrega debe permitir comparar evidencia con aquella hipótesis, sin calibrar el motor con ella.

## Fase 3 · CONDUSEF y ENCRIGE: producir evidencia con la unidad correcta

Leer diccionarios y los 29 CSV existentes. Seleccionar las columnas realmente presentes de periodo, institución/producto, causa, trámite y conteo. Determinar la granularidad y si hay totales y subtotales superpuestos antes de sumar. Entregar agregados reproducibles que respondan qué tipos de reclamación se observan y cómo se distribuyen en las unidades disponibles.

No presentar conteos de reclamaciones como prevalencia entre clientes sin denominador; no convertir causa de reclamación en hecho judicial ni atribuir BNPL/usura donde no exista esa clasificación. Si los archivos impiden una comparación temporal homogénea, mostrar los cortes compatibles y la ruptura exacta.

Para ENCRIGE, verificar primero productor, edición y existencia real de la ola rotulada «2020». Un HTTP 200 con HTML de error no es ficha de diseño obtenida. Consultar catálogo y documentación oficial vigente; registrar si la receta tiene año o nombre erróneo sin renombrar retrospectivamente otro instrumento para hacerla coincidir. Identificar si la pregunta relevante observa a la empresa acreedora, a la deudora o a otro actor. Ese universo no se sustituye por el de reclamantes CONDUSEF.

Si el documento es público, adquirirlo e identificar reactivo, universo, ponderador/diseño y utilidad. Si requiere solicitud institucional, entregar al encargo 21 una ficha final con objeto exacto, evidencia de ausencia pública y campos requeridos; no abrir otro expediente paralelo. La entrega principal de series y tablas continúa aunque este documento siga fuera de alcance.

## Fase 4 · uso y cierre

Dejar un breve mapa `fuente | unidad/periodo | hallazgo descriptivo | consumidor posible | qué no identifica | siguiente uso`. Una extracción no se convierte automáticamente en adopción. Si una cifra nueva requiere el circuito CALC, fijar su definición antes de calcularla y usar el circuito vigente en espacio propio; no modificar el resolver que posee 17. No necesitas crear un CALC para cada celda de una tabla fuente.

Incorporar los objetos obtenidos con el escritor canónico correspondiente, regenerando sólo su proyección pertinente. Actualizar los residuales de sus recetas y FP-324 únicamente en el alcance satisfecho. Archivo obtenido, utilidad satisfecha y parámetro adoptado son estados diferentes. No dejar una receta marcada pendiente de una firma que D17 ya resolvió; tampoco cerrar la demanda científica por haber obtenido un archivo que no la satisface.

## Aceptación y límites

Serie CNBV utilizable o barrera externa demostrada con exportación manual exacta; agregados CONDUSEF efectivos sobre bytes existentes; identidad/alcance ENCRIGE resueltos; trazabilidad y unidades correctas. Si falla una vía tras uno o dos intentos razonables, usar la alternativa directa y continuar los otros productos. No cerrar con otra lista genérica de URLs cuando se dispone de los datos para extraer.

Pruebas dirigidas de extracción, unidades, duplicación y faltantes; contrastes contra el original. No tests con totales fijos del árbol. Payloads fuera de Git, temporales/salidas propios y corpus ajeno preservado. Sin cambios a motor, capturas, R, sellos históricos, cron ni métodos pendientes de firma. Sin envíos a terceros.

Archivar el encargo, nota de cierre y filas afectadas por el procedimiento vigente. Derivar identificadores al integrar y conciliar archivos compartidos sobre main reciente sin pisar filas ajenas. Entregar PR/HEAD, tablas y comandos de reproducción, más `obligación | evidencia | alcance satisfecho | residual`. El merge queda con Jonás.


**Actualización al entregar:** #708 también está fusionado; main=`e7a471bf1499a096abbe58dc298f02243e885135`. Archiva el benchmark sin firmar sus cuatro decisiones; no cambia el alcance de este encargo.

## NO-CORRIDO / RESERVAS

- **qué:** `Fase 2 · CNBV: obtener la serie y hacerla legible`; **por qué:** `NO-VERIFICABLE-AQUÍ`; **impacto:** el corte 2021-12 queda utilizable, pero R1.6 sigue `NUNCA-MEDIDA`, no se obtiene la serie mensual ni se mueve el motor; **sucesor:** `ACTO GEN2-CNBV-IMOR-HISTORICO` deberá usar acceso institucional CNBV o una publicación oficial estática equivalente, con spec previa a cualquier CALC.
- **qué:** `Fase 3 · CONDUSEF y ENCRIGE: producir evidencia con la unidad correcta` para satisfacer N34; **por qué:** `DIFERIDO-A:ACTO GEN2-N34-CONSUMIDOR-DEUDOR`; **impacto:** la adquisición queda trazada y los agregados son utilizables, pero N34/R1.7 sigue `NUNCA-MEDIDA` y sin adopción; **sucesor:** `ACTO GEN2-N34-CONSUMIDOR-DEUDOR` deberá localizar una fuente que observe causa/BNPL/usura del lado consumidor con denominador compatible y fijar su definición antes de calcular.

## CONSUMIDO

PR #717 ejecuta este encargo en `acto/gen2-fuentes-financieras-20` y deja el
merge a mesa. Resultado: CNBV `OBTENIDO-PARCIAL` con corte R16 2021-12 y
barrera histórica demostrada; ENCRIGE+CONDUSEF `OBTENIDO` en adquisición,
29/29 CSV verificados, diseño ENCRIGE oficial y seis tablas reproducibles.
ADR-476; FP-324 registra ejecutadas las recetas 2, 3 y 4 y conserva abiertas
1 y 5. R1.6 y R1.7 siguen `NUNCA-MEDIDA`; contador científico cero y ninguna
adopción. Cierre completo en
`forense/notas/2026-09-11-GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES-cierre.md`.
