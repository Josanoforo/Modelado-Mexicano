# Decisiones y trabajo paralelo · corte posterior a #694

Revisión: 11/sep/2026 UTC. GitHub y fetch local coinciden en `main=4816101e506f527d018dd2c47467a8b57bfbd487`. #694 encoló los seis encargos POST693; no añadió mediciones. La mesa informa que están corriendo. En la primera consulta había cero PR abiertos y tres ramas remotas: publicación 09, ENVIPE 10 y corrupción 11. Durante la revisión se abrió [PR #695 de corrupción](https://github.com/Josanoforo/Modelado-Mexicano/pull/695), HEAD `2833546e8aac5fc7d3cb2e963a2cb6e4a58d59e4`. Se leyó su cierre técnico, como trabajo propuesto y no consolidado. Que aún no se vean las otras tres ramas no demuestra que estén detenidas; pueden seguir locales. No relanzarlas.

## Qué decidir ahora

Estas son opciones, no firmas ya concedidas. No bloquean las mediciones y análisis que están en curso.

| Decisión | En lenguaje de RH | Opción A recomendada | Opción B | Lo que desbloquea |
|---|---|---|---|---|
| NC-0085 / complemento ENVIPE | “El resto del grupo evaluado” no equivale a “todos los que faltan en la plantilla”. | Adoptar el complemento dentro del grupo exacto, identificado como derivado dependiente del padre. | Pedir otro indicador sobre un universo mayor, incluyendo las categorías que hoy quedaron fuera; mantener pendiente la adopción actual. | El uso concreto de RES-0028 en el motor, sin presentarlo como observación independiente o como la respuesta literal “Otra”. |
| FP-371 / DIN | Tenemos el porcentaje, pero no podemos certificar ese margen de error con el diseño disponible. | Rechazar el IC aproximado como verdad inferencial; conservar el punto y mostrar, si se necesitan, sensibilidades claramente rotuladas. | Diferir todo uso inferencial hasta recibir una estimación oficial; conservar igualmente el punto descriptivo. | Asentar el estatus de incertidumbre de DIN; el cálculo puntual y F5 ya pueden usarse en su alcance descriptivo. |
| **Nueva: NC-0107 / PR #695** | Dos reportes antiguos forzaban una sola etiqueta a trámites con varios eventos/canales, como asignar a una persona que trabajó en dos sucursales una sola sucursal por conveniencia. | Retirar las dos tasas históricas discrepantes del uso futuro, preservándolas como historia; conservar r2 únicamente con su alcance observado y continuar la fuente general. | Definir prospectivamente un estimando distinto por persona × tipo de trámite/evento y medirlo; los dos valores antiguos siguen sin adopción. | Cerrar la expectativa de adoptar RES-0009/0011 o despachar un cálculo nuevo con una unidad elegida explícitamente. |

Para elegir basta responder “complemento A, DIN A, corrupción A” o indicar las alternativas. Después se prepara un único cambio de decisión/adopción acotado, coordinado con los dueños de `milpa/` y de las vistas. No se modifica un experimento congelado al firmar la adopción actual.

**Qué aporta #695 a la tercera decisión.** El diagnóstico propuesto encuentra 501 ID_TRA con canal discordante; en el recorte observado hay 95 grupos que mezclan presencial/digital, con 0.2476% de su masa. La r2 por fila evento da 14.1041% presencial y 2.9868% digital; el colapso a ID_TRA de canal consistente da 11.5018% y 2.6635%. No es una diferencia de redondeo: cambia la unidad y su ponderación. Son resultados reportados por la rama de CAJA, no una reproducción de microdatos en esta revisión. [Cierre técnico de #695](https://github.com/Josanoforo/Modelado-Mexicano/blob/2833546e8aac5fc7d3cb2e963a2cb6e4a58d59e4/forense/notas/2026-09-10-GEN2-CORRUPCION-UNIDAD-Y-FUENTE-GENERAL-cierre.md).

La opción A no permite imputar el canal exacto al evento donde ocurrió una solicitud: P8_4 está asociado a ID_TRA y sec_7 contiene hasta tres eventos. La prueba de dominio del emisor no identifica cuál evento recibió la solicitud. Conservar esa limitación en cualquier uso de r2, junto con su condicionamiento a declarantes observados. El mismo PR ya enrutó NC-0153 a adquisición, pendiente de SONDA productiva; 07R puede consumir esa fila **después de su merge**, sin copiarla desde una rama no consolidada.

No se vuelve a preguntar D10: el proxy fintech ya está aceptado descriptivamente. Tampoco FP-361/363: S6/S12 ya se ejecutaron. FP-332 conserva texto parcial, pero su antigua rama y su reclasificación tienen sucesoras; no se propone reabrir esa decisión por el rótulo. D21/F6 sigue sin firma, pero no es necesario abrir el informe final mientras 13 produce el diagnóstico de F5.

## Hallazgo nuevo que sí puede cambiar una conclusión

S6 v1.3/v4 usa localidad como conglomerado y cuatro categorías de tamaño como estrato. Levantó una reserva de varianza bajo la premisa de haber resuelto el diseño. La nota DIN de #693 cuestiona esos sustitutos. El contraste externo verificó que la [FAQ del productor](https://ennvih-mxfls.org/faq.html) describe `estrato` por tamaño de localidad y declara UPM no pública; el [diseño oficial](https://www.ennvih-mxfls.org/assets/ennvih-1_muestra.pdf) documenta estratificación socioeconómica y 180 UPM.

**Inferencia:** la equivalencia usada para justificar los IC de S6 no está acreditada con esa evidencia. CALC-0003-v4 reporta 150 localidades; ese conteo no basta para medir cuánto cambiaría el IC. Su primaria sigue NO-DISCRIMINA y dos secundarias son CORROBORADA bajo la receta usada. No se concluye que los puntos estén mal ni que R4.4 haya cambiado de tier.

El encargo 16 resolverá el alcance y preparará la decisión precisa. No pedirte ahora que elijas una agrupación estadística a ciegas. Tandas puede continuar midiendo puntos con la reserva ya prevista; el problema no paraliza las otras fuentes.

## Tres encargos adicionales

| Encargo | Producto útil | Destino | Concurrencia |
|---|---|---|---|
| [16 · S6: diseño y alcance](16-GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL.md) | Contrastar la premisa, delimitar IC/conclusiones afectados y dejar decisión concreta | Cloud; CAJA sólo si hace falta abrir microdatos | Iniciar ahora; no toca los archivos de datos/motor de los otros actos |
| [14 · Ya medido](14-GEN2-YA-MEDIDO-SIN-FALSOS-NEGATIVOS.md) | Reparar falsos negativos para tasas ya ejecutadas | Cloud o CLI | Independiente de 09; no modifica corrida0 ni las cifras |
| [15 · ENIF fintech](15-GEN2-ENIF-FINTECH-SERIE-DESCRIPTIVA.md) | Medir el proxy 2018/2021 y comparar con 2024 donde corresponda | CLI/CAJA | Independiente de ENIF población y de los seis encargos activos |

Los tres requieren **cero llamadas nuevas a modelos**. 16 es prioritario por materialidad; 14 evita repetir trabajo; 15 produce mediciones nuevas. Están diseñados con lectura de corpus compartido y salidas propias. Los documentos no ordenan escribir simultáneamente `milpa/`, el manifiesto o las vistas globales.

Se puede lanzar 14 y 16 en dos tareas Cloud separadas, y 15 en un worktree de CLI adicional si cabe en RAM. No ampliar la concurrencia del despacho automático. Confirmar duplicados antes de iniciar, ya que las ramas pueden aparecer después de este corte.

## Adenda breve para 09, sin tarea nueva

[ADENDA-09-CIERRES-YA-ACREDITADOS.md](ADENDA-09-CIERRES-YA-ACREDITADOS.md) agrega NC-0093/0101, el alcance resuelto de NC-0087 y la adopción NC-0124 a la conciliación del 09. Sus notas reportan cierres que no llegaron a las filas del TSV. Pasársela al ejecutor actual; no abrir otra rama de conciliación ni volver a correr las olas/ENIF.

El otro enlace erróneo, NC-0129→NC-0110, lo corrige 14: el defecto de herramienta es NC-0109. La decisión de canal NC-0110 permanece cerrada.

## Integración y lo que no conviene añadir todavía

Mantener 09 como primer merge recomendado para la publicación global. 14 y 16 pueden integrarse antes si terminan y sus deltas son independientes; no hay compuerta científica que lo prohíba. 15 entrega recibos al publicador o se integra después, sobre main actualizado. Cada merge se serializa y quien llega después renumera su ADR/NC y concilia sólo sus filas. No reservar números definitivos mientras hay ramas activas.

No sumar ahora un acto de `delta`: requiere emparejamientos de consumidor y comparte `tools/corrida0.py` con publicación; no es el bloqueo más corto. No indexar de golpe los 102 instrumentos sin texto: el siguiente cálculo puede leer su FD directamente, y NC-0123 ya declaró la limitación. No ampliar B ni relanzar 224 capturas: 13 debe identificar primero qué nueva pregunta merece ese trabajo. No crear otro encargo genérico de adquisición para expedientes que esperan identidad, DUA o respuesta del titular.

## Evidencia y alcance de esta revisión

Se reconsultó main, PR abiertos y ramas; se inspeccionaron las obligaciones abiertas/firmas parciales y sus sucesoras pertinentes. Dos ejecuciones reales de `ya_medido` siguen devolviendo NUNCA-MEDIDA para `tramite.mordida.con_registro` y `dinero.ahorro.horizonte_no_corto_con_seguridad_social`. No se ejecutó suite general, no se abrieron microdatos ni se interrumpieron tareas locales. No se alteró el repositorio remoto ni se enviaron solicitudes.

Resultado: tres decisiones listas para mesa (una basada en PR #695 todavía abierto), tres frentes adicionales delimitados y una adenda al trabajo en curso. La prioridad es mejorar mediciones y su interpretación, sin abrir otra ronda de control general.
