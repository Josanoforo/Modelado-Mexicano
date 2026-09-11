# 30 · GEN2 · Validación independiente de parámetros activos

ACTO: GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS  
ENTORNO: CAJA  
Estado de despacho: **EJECUTABLE TRAS MERGE DE #720**.  
Resultado: evidencia numérica independiente, enlazada al registro, para los RESULT que alimentan las salidas directas GEN2 vigentes.


## Contrato de ejecución

Repositorio: `Josanoforo/Modelado-Mexicano`. Este documento es un encargo autónomo: no requiere la conversación previa.

Al despacharlo, Jonás autoriza el alcance expresamente indicado, su implementación, comprobación dirigida, archivo del encargo, commits, push y apertura/actualización de PR. **La fusión corresponde a Jonás.** Una recomendación metodológica ajena a este alcance no queda firmada.

Lee `AGENTS.md` y las instrucciones aplicables. Usa worktree y rama propios; reporta ruta absoluta, rama, HEAD y estado inicial. Comprueba en `origin/main` y PR abiertos qué parte ya existe. Si otro trabajo resolvió el objeto, consúmelo y concilia el residual; no lo dupliques. No reconstruyas el historial completo.

Los PR predecesores abiertos son dependencias, no hechos consolidados. Puedes preparar el encargo desde ahora; ejecuta sus fases dependientes sobre el commit efectivo fusionado. Resuelve conflictos de integración ordinarios dentro de la tarea. Si el entorno necesario falta, resuelve su acceso antes de la fase productiva y evita presentarla como terminada.

Reutiliza registros, resolvedores, escritores canónicos y herramientas existentes. No reescribas artefactos sellados, datos ajenos ni historial compartido. Un resultado sucesor lleva su propia identidad. Conserva replay, evidencia independiente y reservas existentes al regenerar proyecciones.

La validación debe responder riesgos concretos del resultado. Ejecuta las comprobaciones dirigidas y gates aplicables; no amplíes el alcance para limpiar CI heredada. Una vez suficientemente comprobado, entrega el resultado.

Cierra la cadena vigente: encargo → implementación/resultado → evidencia → registros y vistas pertinentes → nota de cierre → ADR/L0/rótulo cuando corresponda → PR. Usa IDs disponibles al integrar, sin reservar números desde este documento. Cierra sólo obligaciones acreditadas; conserva residual, causa y siguiente acción. No confundas commit, merge, validación, adopción y nueva medición.

No envíes mensajes/formularios externos, aceptes compromisos institucionales ni realices compras desde este encargo. La descarga pública y el uso de accesos previamente autorizados sí pueden avanzar. Los secretos y microdatos permanecen fuera de Git según el contrato del corpus.


## Propósito y autoridad

Los snapshots #712/#720 comprueban que M transporta los RESULT correctos; sus salidas directas todavía declaran validación independiente NO-HECHA en el corte revisado. Este encargo autoriza comprobar los puntos desde las fuentes mediante una implementación independiente. No es otra ejecución del mismo medidor.

El resultado no crea una muestra nueva, no demuestra causalidad, no renombra parámetros conocidos como HOLDOUT y no habilita FP-374/F6. Tampoco incorpora automáticamente las nuevas cifras ENSAFI/IMOR de los encargos 27/28.

## Fase 1 · Congelar el conjunto útil

Toma el snapshot efectivo posterior a #720 y sus usos activos. En el corte revisado son 16 consumidores directos. Fija sus identidades; deduplica por RESULT y dependencia numérica para evitar calcular dos veces el mismo punto.

Consulta la evidencia existente. Si un RESULT exacto ya tiene validación independiente suficiente por `(spec_id, resultado_id)`, reutilízala y verifica su vínculo; no vuelvas a medirlo por cuota.

Produce una tabla corta de trabajo: consumidor, RESULT, fuente, definición, factor, transformación, evidencia existente y trabajo faltante. Es un instrumento para ejecutar; no el entregable final.

El investigador conoce los resultados publicados. Declara independencia de implementación, no cegamiento respecto de cifras ni independencia de muestra.

## Fase 2 · Protocolo e implementación independientes

Fija antes del contraste:
- población y unidad;
- eventos/códigos y no respuesta;
- llaves y multiplicidad;
- ponderador;
- transformación;
- tolerancia numérica justificable por escala y precisión, no por el residuo observado;
- qué resultado acredita la comparación.

Leer los originales de las fuentes y sus definiciones. Puedes reutilizar resolvedores de archivos, hashing y lectores genéricos. No importes el medidor original, el extractor decisivo ni el RESULT para producir el valor que luego se compara.

Trabaja por familia/tabla cuando comparta datos, evitando reabrir el corpus por consumidor. Un complemento se valida desde su padre y transformación; no se presenta como otra medición independiente.

Reutiliza el patrón de #714 y el overlay común, sin copiar sus cifras ni presumir que sus tres R validan estos M. El objetivo inicial es punto y las cantidades necesarias para acreditarlo; no revalidar todos los EE/IC históricos.

## Fase 3 · Ejecutar con corpus y adjudicar el contraste

Para cada RESULT pendiente, calcula el punto desde datos, conserva n/máscaras/masas necesarias y contrasta. Separa:
- concordancia del punto;
- coincidencia de universo/unidad;
- validez del enlace al consumidor;
- incertidumbre de diseño, sólo si efectivamente se comprobó.

Clasifica con los estados existentes del registro y el alcance exacto. Un punto que coincide no recibe validación inferencial por extensión.

Si hay discrepancia:
1. Localízala en fuente, códigos, join, factor, unidad o transformación.
2. Muestra el efecto sobre el consumidor.
3. Si es un defecto mecánico inequívoco, prepara el correctivo sucesor y la protección del uso afectado dentro del mismo encargo; conserva el original.
4. Si cambiaría el estimando o una decisión científica, entrega la alternativa cuantificada y el ámbito pendiente de mesa; no elijas para reproducir el número anterior.
5. Continúa con las familias independientes que sí pueden cerrarse.

No ajustes tolerancias tras ver el desacuerdo ni declares PASA desde un replay del mismo programa.

## Fase 4 · Incorporar y comprobar consumo de la evidencia

Registra la evidencia mediante `data/corrida0/validaciones-independientes.tsv` y los resolvedores vigentes. Respetar identidad completa, alcance, hashes y precedencia de evidencia.

Regenera proyecciones pertinentes sin borrar veredictos ajenos. Comprueba que la consulta/snapshot consume la validación registrada y distingue punto, inferencia e independencia experimental. No reescribas snapshots históricos; usa la política de sucesión existente cuando proceda.

El encargo 29 es dueño de la interfaz operativa. Coordina sólo si una discrepancia exige proteger un consumidor; no construyas otra consulta en esta tarea.

## Fase 5 · Cierre

Entrega:
- protocolo e implementación independiente;
- evidencia agregada y hashes, sin microdatos en Git;
- tabla por RESULT/consumidor: validado, reutilizado, discrepante o no verificable con causa;
- overlay/proyecciones coherentes;
- efecto sobre confianza y uso del motor;
- PR y cadena de cierre.

No fabriques una reserva masiva si una sola familia carece de archivo: resuelve el acceso disponible, termina las demás y especifica el objeto exacto faltante. Contador científico y de validación se derivan por separado; no contar 16 consumidores como 16 muestras nuevas.

## Dependencias y convivencia

Requiere #720 fusionado y corpus CAJA. Puede correr con 27/28/29. Su perímetro numérico se congela al inicio; no absorbe nuevas adopciones concurrentes para perseguir un total cambiante. Mantiene separadas las reservas DIN/S6, complementos pendientes y evaluación retenida.
