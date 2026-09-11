# Siguiente tanda · paralelos después de #707

Preparado para Jonás el 11 de septiembre de 2026. Corte comprobado: `main=cd92cb25acbb7b645a4b49ed180f042661d18e7e`, merge de [#707](https://github.com/Josanoforo/Modelado-Mexicano/pull/707). [#700](https://github.com/Josanoforo/Modelado-Mexicano/pull/700) ya está fusionado. Actualización final: [#708](https://github.com/Josanoforo/Modelado-Mexicano/pull/708) también está fusionado; main avanzó a `e7a471bf1499a096abbe58dc298f02243e885135` para archivar el benchmark. Revalidar únicamente los cambios posteriores que afecten al encargo.

## Qué es aparte y qué continúa

**20, 21 y 22 son encargos adicionales independientes de 17–19. 07R es una continuación actualizada del despliegue existente. La adenda de 18 se entrega a su ejecutor actual; no se abre otra tarea de motor.** Los números 20–22 identifican este paquete, no reservan ADR, NC ni firmas.

| Archivo | Resultado útil | Destino | Relación con tareas activas |
|---|---|---|---|
| [07R-GEN2-PRODUCCION-Y-FALLO-POST707.md](07R-GEN2-PRODUCCION-Y-FALLO-POST707.md) | Causa y tratamiento del `exit=1` de hoy; tarea instalada y recorrido acreditable | CLI Windows/WSL | Continuación de 07R. Si ya corre, pasar este archivo al mismo ejecutor |
| [20-GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES.md](20-GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES.md) | Serie pública de IMOR y explotación descriptiva de CONDUSEF; resolver la identidad de ENCRIGE | CLI con corpus y acceso web | Fuentes y extracciones; no modifica motor ni evaluación |
| [21-GEN2-EXPEDIENTES-ACCESO-LISTOS.md](21-GEN2-EXPEDIENTES-ACCESO-LISTOS.md) | Expedientes técnicos completos para acceso a datos y diseño muestral | Cloud | Continúa solicitudes existentes; entrega al titular lo que realmente requiere identidad, firma o envío |
| [22-GEN2-VALIDACION-R-ENVIPE-CSV.md](22-GEN2-VALIDACION-R-ENVIPE-CSV.md) | Validación independiente de punto e incertidumbre de los tres R de ENVIPE 2021/2023/2024 | CLI con corpus | NC-0096; no repite las ocho olas de #697 ni modifica R congelados |
| [ADENDA-18-CONSUMOS-Y-BENCHMARK.md](ADENDA-18-CONSUMOS-Y-BENCHMARK.md) | S6, fintech y etiquetas llegan a sus consumidores con el alcance correcto | Ejecutor actual de 18 | Mismo worktree/PR de 18, salvo que ya haya terminado |

Las ramas publicadas de 17–19 están activas al corte: `acto/gen2-linaje-adopcion`, `acto/gen2-motor-herencia-explicita` y `acto/gen2-evaluacion-sin-fugas`. Su publicación acredita trabajo en curso, no implementación terminada. No hay una rama publicada de 07R que permita confirmar si existe una sesión local activa.

## Lanzamiento

Se pueden iniciar **20, 21 y 22 a la vez**, además de continuar 07R. La dependencia de 18 con el contrato de 17 permanece. Ninguno de estos encargos necesita esperar las cuatro firmas del benchmark para producir su resultado técnico.

Adjunta un archivo por tarea y usa:

> Ejecuta este encargo completo en un worktree propio desde main actual. Verifica sólo cambios posteriores pertinentes y ramas del mismo objeto para no duplicar trabajo. Continúa entre fases autorizadas y entrega un PR revisable. No fusiones. Conserva decisiones científicas pendientes y evidencia histórica. Si una fase necesita CAJA, prepara su continuación exacta y sigue con lo ejecutable; no declares completada una medición que no corriste.

Para 07R, si ya está trabajando una sesión, envía allí el archivo como actualización. Para la adenda de 18, envíala directamente al ejecutor actual. No lanzar otro `/despacha` general para cada frente ni crear un segundo cron.

## Concurrencia real

Cada tarea usa worktree, rama y directorio de salidas propios. El corpus existente se comparte en lectura; no se extrae encima de otra tarea. Las descargas nuevas de 20 usan temporal y destino propio, comprobando identidad antes de incorporar bytes al corpus. 07R es el único que toca tarea programada y clon productivo.

20 y 21 pueden consultar las mismas filas de adquisición; cada uno modifica sólo sus objetos. Si 20 detecta que ENCRIGE requiere un oficio, entrega una ficha a 21: no redactan dos solicitudes. 21 puede completar sus otros expedientes sin esperar esa ficha.

17 mantiene el resolver y las vistas globales; 18 el consumo del motor; 19 la evaluación. 20–22 entregan evidencias y cambios mínimos en sus registros mediante los escritores existentes. No implementan otro resolver, otro registro ni otra adjudicación.

**Los merges y la conciliación final de archivos compartidos se hacen uno por uno.** Cada ejecutor actualiza su rama al integrar, conserva las filas ajenas por identidad y significado y deriva los identificadores disponibles. No reemplaza un TSV por una copia anterior. Si dos trabajos locales compiten por RAM o disco, se escalonan sus lecturas pesadas; eso no crea una dependencia científica.

## Firmas y evidencia que no deben confundirse

D17 ya autorizó avanzar obtención; D19 ya autorizó unificar operación. D10 ya autorizó fintech como proxy descriptivo. Estas decisiones no se vuelven a pedir.

Las cuatro decisiones del benchmark siguen abiertas: DIN/FP-371, S6/FP-372, complemento/NC-0085 y corrupción/NC-0107. [#708](https://github.com/Josanoforo/Modelado-Mexicano/pull/708) ya está fusionado y archiva el benchmark: no firma sus recomendaciones. Estos encargos no cambian ese estado por inferir aprobación de «encargos corriendo».

#707 publica una huella con `sha=c23dce15a917bb6fb0a4e44dabf3767e03c9ded8`, `publicacion=OK`, `exit=1` y duración de 37 segundos. Esto corrige la premisa antigua de un clon observado en #677. Demuestra ejecución identificada y publicación del recibo; todavía hay que explicar el fallo del agente y comprobar el disparador. Los 33 archivos nuevos del censo incluyen documentos de trabajo: no son evidencia de 33 adquisiciones científicas nuevas.

Este paquete contiene encargos listos para despacho. No se ha modificado el repositorio ni se han abierto PR desde esta revisión.
