# ENCARGO · GEN2-ENCIG2023-FLUJO-Y-ESTIMANDO-1

**Entorno:** Codex CLI / CAJA. **Producto:** clasificación documentada y cuantificada del flujo que hace observable P8_4; dictamen de correspondencia con RES-0007/0008 y, sólo cuando la documentación lo identifique, una estimación sucesora. No es otra corrida del agregado ya publicado.

**Corte de preparación:** `Josanoforo/Modelado-Mexicano`, `main @ 018956261ca57fb5fb124f72faaf977e27e4df6e`, 17/sep/2026 UTC. Al ejecutar manda `origin/main` vigente. CAREO #827 ya está fusionado, pero no se presume que sus firmas ni el piloto estén terminados.

## 1. Problema concreto y decisión que habilita

#831 publicó `CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001`: P8_4 está observado en 23,100 de 123,186 eventos unidos (18.7521% por conteo; 15.8400% por masa). Su agregado condicionado es aproximadamente 0.204431. Son cifras del padre, no resultados de este encargo. La nota propone una eventual correspondencia con `paga_mordida` y `tramite_normal`, pendiente de mesa.

La cobertura de unión de 100% no resuelve el significado de los blancos. Hay que distinguir salto estructural, no aplicabilidad, no respuesta y contradicción. También hay que acreditar si P8_4 mide solicitud/circunstancia de corrupción o pago efectivo: **no dar por válida la etiqueta del consumidor por la similitud del nombre**. P8_6 se consultará documentalmente para establecer esa diferencia, sin abrir una nueva medición de pago.

Resultado útil: mesa puede decidir si el agregado condicionado tiene una correspondencia defendible, si requiere otro nombre/universo o si debe permanecer sólo como descripción. No se requiere adoptar ninguna alternativa en esta sesión.

## 2. Insumos y lectura acotada

- `AGENTS.md` y las instrucciones del perímetro.
- `forense/analisis/encig2023-agregado-condicional-1/01-resultados-e-interpretacion.md`.
- `data/corrida0/CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001/`: spec, medidor, resultados, sellos.
- `data/corrida0/CALC-ENCIG-2023-0001-v1_1/`: únicamente contrato de unión, códigos y ponderación.
- `data/corrida0/demanda-resultados.tsv`, filas RES-0007/0008, y regla `tramite.mordida.con_registro` de `milpa/tramite.yaml`, sólo lectura.
- `data/manifiesto.yaml`: `encig23_base_datos_csv`, SHA-256 `af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d`; `encig23_estructura_base_datos_pdf`, SHA-256 `eb89820cd58af0d8799387a376b9e60b062ed59daea74cdbea7ff3b4ee13a906`.

Resolver raíces con las utilidades existentes. Un worktree sin data/raw no acredita que falte el corpus. Buscar primero documentación ya adquirida; si falta, adquirir hasta **dos documentos oficiales de ENCIG 2023**, cuestionario y/o manual con instrucciones de salto. No usar el cuestionario 2025 como sustituto. No descargar otras olas, tabulados nuevos ni otro payload estadístico. Registrar sólo las nuevas entradas documentales efectivamente adquiridas; no regenerar el manifiesto.

## 3. Documento → contrato → cálculo

### A. Establecer qué se pregunta

1. Extraer texto, periodo, unidad, códigos y secuencia de P8_3, P8_4 y la distinción documental con P8_6. Citar documento, hash y página/sección, distinguiendo página PDF e impresa cuando difieran.
2. Dibujar el flujo mínimo de entrada a P8_4 y traducir cada instrucción a una condición explícita. El FD describe columnas; una etiqueta sola no acredita todos los saltos.
3. Distinguir: persona que declara alguna circunstancia, selección de tipo de trámite y evento particular. Verificar si la vinculación permite atribuir la respuesta a cada evento o sólo al tipo de trámite; repetir una marca de persona sobre varios eventos no crea información de evento.
4. Verificar por separado solicitud, intento, entrega/pago y ausencia de esas situaciones. Si `paga_mordida` exige pago y P8_4 no lo identifica, declarar **NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR** aunque la aritmética del padre sea correcta. No calcular P8_6 para arreglarlo por iniciativa propia.

### B. Fijar una clasificación antes de producir nuevos conteos

Crear contrato propio con categorías mutuamente excluyentes y exhaustivas:

- respuesta válida observada;
- salto documentado que permite determinar lógicamente el desenlace en la unidad objetivo;
- fuera del universo objetivo / no aplicable;
- elegibilidad no determinable con las columnas autorizadas;
- respuesta faltante pese a ser aplicable;
- código o combinación contradictoria.

No asignar cero a todos los blancos. Un salto puede implicar ausencia del evento sólo si el cuestionario lo demuestra para ese mismo desenlace y unidad. No aplicable no significa respuesta negativa. Los casos contradictorios conservan incertidumbre hasta resolver su causa.

Escribir una tabla de decisión con condición, categoría, tratamiento de numerador/denominador y evidencia. Fijar el tratamiento de pesos y duplicados; no seleccionar reglas después de ver cuánto mueven la tasa.

**COMMIT 1:** contrato, tabla de flujo y script probado con datos sintéticos. El análisis es posterior a resultados conocidos; no llamarlo pre-registro ciego ni confirmación independiente.

### C. Cuantificar sin extender innecesariamente la lectura

Miembros autorizados de `encig23_base_datos_csv`:

- `encig2023_04_sec_7.csv` y `encig2023_05_sec_8.csv` para reproducir unión y clasificar el universo del padre;
- sólo si el flujo exige antecedentes a nivel persona y no hay una reserva vigente: columnas de identidad y **P8_3_1/2/3** de `encig2023_01_sec1_A_3_4_5_8_9_10.csv`. Este lanzamiento autoriza esa ampliación acotada respecto del padre; no autoriza leer las otras secciones ni toda la tabla indiscriminadamente.

Antes de abrir el tercer miembro, comprobar las reservas científicas vigentes específicas. Una reserva todavía activa no se cancela por este encargo: ejecutar lo resoluble con dos miembros y dejar el resto como elegibilidad desconocida. No desactivar candados. No abrir `sec_11`, residentes, `sec_6`, otras olas ni el piloto ENIF.

Preservar `FAC_TRA` como peso del evento; no sustituirlo por FAC_P18. Para unir antecedentes de persona, probar cardinalidad muchos-a-uno con llave acreditada y mostrar cobertura por filas y masa. Cualquier multiplicación de filas o ambigüedad material detiene esa derivación; no tomar la primera coincidencia.

Entregar conteo y masa de cada categoría, total y las cuatro partes de canal del padre, sin tratar el canal faltante como canal sustantivo. Reconciliar contra los 123,186 eventos y sus masas del padre al mismo corte. Volver a reproducir 23,100, numerador y denominador observados; si no concilian, resolver antes de producir una conclusión.

### D. Resultado estadístico y decisión

1. Mantener el punto condicionado original como referencia inalterada.
2. Si queda acreditado un universo más amplio y el desenlace tiene sentido para todas sus unidades, publicar `W_universo`, `W_positivo_conocido`, `W_negativo_conocido` y `W_desconocido`, con sus n. Los límites lógicos son `[W_positivo/W_universo, (W_positivo+W_desconocido)/W_universo]`; sólo aplican cuando esas masas forman una partición válida del mismo universo. No confundirlos con IC.
3. Si la pertenencia al universo sigue indeterminada, no usar esa fórmula con un denominador inventado. Separar la población identificable y mostrar lo que falta para acotar la restante. No imponer independencia, missing at random ni imputación por canal.
4. Si desaparece toda indeterminación relevante, calcular el punto identificado por el contrato. Si persiste, publicar conjunto identificado o limitación. No escoger el punto medio de una banda.
5. Este acto no abre un nuevo frente de varianza: no producir un IC para el nuevo estimando si no se ha especificado y acreditado su diseño; el IC del padre no se hereda. Rotular separadamente incertidumbre por faltantes y precisión muestral no calculada.

**COMMIT 2:** ejecución real, tablas y resultado sucesor, sugerido `CALC-ENCIG2023-FLUJO-0001`, con verificación dirigida según el mecanismo actual. Preservar todos los artefactos sellados anteriores. No cuenta como nueva fuente independiente.

## 4. Entregables y cierre suficiente

En `forense/analisis/encig2023-flujo-estimando-1/`:

- contrato de flujo y evidencia documental;
- tabla reproducible de categorías, n, masas y tratamiento de observación;
- tabla original/sucesor: mismo o distinto desenlace, población, unidad, numerador, denominador y resultado;
- dictamen de máximo dos páginas para RES-0007/0008, con recomendación y reserva material. Si la incompatibilidad semántica basta para rechazar la correspondencia, decirlo claramente y conservar el análisis descriptivo útil.

Pruebas mínimas del riesgo real: salto ≠ missing; blanco no convertido a cero; unión sin multiplicación; categorías cierran el universo; la respuesta a nivel persona no se atribuye a eventos sin respaldo; límites lógicos contienen todas las asignaciones extremas de desconocidos y no se rotulan IC. Reutilizar lo existente; no crear un marco general de validación.

No cerrar con «hay que estudiar los blancos» si la documentación y corpus permiten clasificarlos. Si un documento no se obtiene, dos intentos razonables y una alternativa directa bastan: cuantificar lo posible, identificar la pieza exacta y entregar una receta, sin inventar flujo ni consumir toda la sesión buscando.

## 5. Concurrencia, autoridad y entrega Git

Una tarea, un worktree, una rama y un PR. Al arrancar: ruta absoluta, rama, HEAD, status; fetch; comprobar PR/ramas del rótulo para no duplicar. Si la rama anterior de la sesión ya fue fusionada, abrir sucesora desde origin/main, preservando cambios posteriores con commits o parches explícitos. No reset/clean/force ni manipular árboles de otras sesiones.

Permitidos: directorio propio, CALC sucesor, script/pruebas propios y hasta dos adiciones documentales de manifiesto. Archivar este encargo verbatim en una ruta propia sin duplicar nombres de archivos ya censados; metadatos de consumo fuera del bloque.

No editar padres, milpa, motor, `tools/corrida0.py`, `tools/relevo_usos.py`, vista de relevos, panel F6, cron ni corpus L. Opus conserva PILOTO-1/TRÁMITE-4, firmas, corte de edad, crosswalk y θ. ENVIPE 2013/2015, precisión WBES, ENCO #834, F-3 #835 y ENCRIGE #836 conservan sus perímetros. El encargo MOCIBA paralelo usa otros documentos y salidas; preservar ambas adiciones de manifiesto al sincronizar.

**Reserva:** no abrir ni derivar ENIF 2024 localidad × edad, ni capturas/resultados del piloto; no abrir respuestas MOCIBA/ISSP/ENCO ni olas retenidas de F6. El merge de CAREO no levanta por sí solo ninguna reserva.

Al lanzar se autorizan cambios delimitados, pruebas, commits, push sin force y PR; **la fusión queda con Jonás**. Sin comunicaciones externas ni llamadas experimentales. Excepción temporal de cascada: diferir decisiones.tsv, no-corrido.tsv, firmas, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar numeración. No correr /tramite, /despacha, /deriva, cron ni registro --escribe.

Sincronizar antes del push final, revisar diff y pruebas focales. Resolver fallos propios que afecten el producto; no debilitar checks ni recongelar baselines. Si una compuerta exige cambios compartidos fuera del alcance, reportar el impedimento concreto para integración serial. Máximo aproximado 20% del esfuerzo en control salvo un riesgo material de dato.

Retorno: producto y decisión habilitada; PR, base/HEAD, comandos realmente ejecutados, pruebas/CI, reservas y **CIERRE COMPARTIDO DIFERIDO** con sólo las propagaciones necesarias. Distinguir ejecutado, sellado, integrado y adoptado. No sustituir un resultado por una lista de tareas futuras.

## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-ENCIG2023-FLUJO-Y-ESTIMANDO-1 en CAJA. Autorizo verificar documentalmente qué mide P8_4 y su flujo, adquirir hasta dos documentos oficiales de ENCIG 2023 indispensables y registrar sólo sus adiciones, fijar contrato/código antes de nuevos conteos y clasificar/cuantificar todos los eventos del padre. Autorizo sec_7/sec_8 y, sólo si el flujo lo requiere y no existe reserva científica vigente, identidad y P8_3_1/2/3 del miembro de persona especificado. Produce límites o punto sólo cuando población y desenlace estén identificados. No conviertas blancos indiscriminadamente a cero, no midas P8_6 ni adoptes la cifra en milpa. Autorizo commits, pruebas, push y PR; fusión conmigo. Aplica cascada diferida y conserva el piloto, F6 y todos los perímetros paralelos.
