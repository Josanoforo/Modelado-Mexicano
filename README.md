# Benchmark del Mexicano

**Modelado Mexicano · Psicología del Mexicano Contemporáneo.** Benchmark auditable de predicciones y estimaciones segmentadas con encuestas oficiales de México. [Informe vigente](canon/informe-programa-v1_2.md) · [Aviso de alcance](AVISO-DE-ALCANCE.md).

## Qué es y qué no es

El repositorio reúne [reports](corpus/reports/), modelo, especificaciones previas a la lectura del desenlace, código, RESULT y sellos. Usa microdatos oficiales citados por cada cálculo. Sus unidades incluyen personas, hogares, delitos y trámites; no se promedian como si fueran iguales. El corpus temático es más amplio que las mediciones disponibles. No responde preguntas ausentes de la encuesta, no mide compras observadas ni marcas, no ofrece gemelos digitales y no promete detectar cambios entre olas.

## La prueba

Estas son **evaluaciones**, no dominios independientes ni una lista de predicciones anteriores a la publicación oficial. En el vocabulario del repositorio, «prospectiva» significa que la emisión quedó sellada antes de abrir el árbitro R de la evaluación; eso por sí solo no prueba que antecediera a la publicación de INEGI.

| Evaluación | Ola y unidad | Dictamen | Cierre |
|---|---|---|---|
| Piloto ahorro, localidad × edad; 8 celdas <!-- deriva: rg -F '8/8 celdas' forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md --> | ENIF 2024, persona | `SIN-CANDIDATO-SUPERIOR` | [Nota](forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md) |
| Piloto evasión, escolaridad × dominio; 12 celdas <!-- deriva: rg -F '12/12 celdas' forense/notas/2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md --> | ENVIPE 2025, delito | `SIN-CANDIDATO-SUPERIOR` | [Nota](forense/notas/2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md) |
| Piloto gobierno digital, edad × escolaridad; 15 celdas <!-- deriva: rg -F '3/15' forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md --> | ENCIG 2025, trámite | `FALSADOR-DEBIL` | [Nota](forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md) |
| Lote de interacción; 44 celdas puntuadas <!-- deriva: rg -F '44 celdas puntuadas' canon/informe-programa-v1_2.md --> | ENIF 2024, persona | `PROPUESTA-CON-RESERVA`: mejora puntual sin despejar umbral | [Nota](forense/notas/2026-09-21-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-cierre.md) |
| Duelo de ola nueva, sexo × dominio y edad × dominio; 12 por cruce <!-- deriva: rg -F '12 celdas puntuadas por par' forense/notas/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md --> | ENVIPE 2026, delito | `NADIE-VENCE` en ambos | [Nota](forense/notas/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md) |
| Duelo de candidatos, edad × sexo y escolaridad × sexo; ver celdas en cierre | ENCIG 2025, trámite | Agregado `FALSADOR-DEBIL` | [Nota](forense/notas/2026-09-23-GEN2-DUELO-ENCIG2025-CIERRE-1-cierre.md) |

Los retadores evaluados no superaron los **criterios de superioridad fijados en esas comparaciones**. Esto no declara equivalencia ni se extiende a modelos no evaluados. El [informe](canon/informe-programa-v1_2.md) documenta la subcobertura del piso en el lote y en marginales. Los intervalos calibrados corresponden a evaluaciones concretas, no a todos los RESULT del repositorio.

## Estado derivado

Cada contador tiene su propio universo. `status` es una vista derivada del corte disponible al ejecutar el comando, no el estado vivo de otras ramas.

| Objeto | Valor en este corte | Clave |
|---|---:|---|
| Corridas selladas | 179 | <!-- deriva: python3 tools/corrida0.py status | rg '^N_corridas_selladas=' --> `N_corridas_selladas` |
| RESULT GEN2 sellados | 61 199 | <!-- deriva: python3 tools/corrida0.py status | rg '^N_resultados_gen2_sellados=' --> `N_resultados_gen2_sellados` |
| RESULT GEN2 adoptados activos | 72 | <!-- deriva: python3 tools/corrida0.py status | rg '^N_resultados_gen2_adoptados_activos=' --> `N_resultados_gen2_adoptados_activos` |
| Celdas validadas (contador rector) | 219 | <!-- deriva: python3 tools/corrida0.py status | rg '^celdas_validadas=' --> `celdas_validadas` |
| Celdas prospectivas de esa vista | 20 | <!-- deriva: python3 tools/corrida0.py status | rg '^celdas_validadas_prospectiva=' --> `celdas_validadas_prospectiva` |
| Celdas retrospectivas de esa vista | 59 | <!-- deriva: python3 tools/corrida0.py status | rg '^celdas_validadas_retrospectiva=' --> `celdas_validadas_retrospectiva` |
| RESULT GEN2 pendientes de adopción | 10 | <!-- deriva: python3 tools/corrida0.py status | rg '^N_resultados_gen2_pendientes_adopcion=' --> `N_resultados_gen2_pendientes_adopcion` |

El [estado](canon/estado-programa-v1_15.md) y la [actualización del contador](canon/L0/ADR-260923-GEN2-CONTADORES-CONSUMO-1-988c-01.md) explican el alcance de las celdas. El total incorpora conductas agregadas de crédito y cruces ENCIG que antes no contaba; los campos prospectiva y retrospectiva de `status` no cubren todas las formas incorporadas al total. **Validada** significa emisión comparada con R, no adopción por mesa.

## Estado del modelo

Este bloque describe el **modelo heredado** y conserva la comprobación T19c
de la suite. No sustituye los contadores GEN2 de arriba.

- **26 de 27** corridas del Hito D con veredicto archivado — **14D·4B·4A·2E·2C**. <!-- deriva: python3 tests/check.py --baseline | rg 'T19c' ; fuente: forense/hitoD-preregistro-v2_0.md -->
- Condicionales medidas 12 de 15. <!-- deriva: rg -c 'clase: "MEDIDO·PARCIAL|clase: "MEDIDO·NACIONAL' milpa/procedencia.yaml ; T19c -->
- Coeficientes en escala del modelo 0 de 15. <!-- deriva: rg 'magnitud: medid' milpa/procedencia.yaml ; T19c -->

## Verifica en cinco minutos: ruta de lectura

Para inspeccionar estructura, referencias y sellos no hace falta `data/raw`. Clona el repo, lee una [nota de cierre](forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md) y compara su `spec.yaml`, `resultados.json` y `sello.json` en [corrida0](data/corrida0/). `python3 tools/corrida0.py status` reproduce la tabla. `python3 tests/check.py --baseline` verifica la línea base del repo, sin garantía de duración. La [guía](docs/verificar.md) explica el control de hashes sin abrir raw y separa la reproducción numérica: `python3 tools/corrida0.py verify <CALC-ID>` puede necesitar corpus, dependencias y más tiempo. La [receta de sello externo](docs/sello-externo.md) explica su testigo de tiempo y sus límites.

## Cobertura

El corpus contiene **31 reports temáticos**. <!-- deriva: rg --files corpus/reports -g '*.md' | wc -l --> Son documentos de evidencia, no dominios mutuamente excluyentes; [lista completa](docs/catalogo.md). El mapa U0 aún no está consolidado en este corte. Hay mediciones **selladas** sobre dinero (ENIF), trámites (ENCIG), seguridad (ENVIPE), tiempo (ENUT) e ingreso (ENIGH), trazables por [CALC y RESULT](data/corrida0/) y [estado](canon/estado-programa-v1_15.md). Sellado, validado y adoptado son estados distintos. ENOE, ENDIREH, INE/ENCUP y MOCIBA tienen líneas de trabajo pendientes de consolidación; hasta que publiquen RESULT y dictamen, no se presentan como medición publicada. U0 fijará la cobertura temática y su propietario, pero no bloquea la publicación de los productos ya fusionados. Una duda pendiente no se clasifica `NO-MEDIBLE-POR-DISEÑO`.

## Uso, límites y contribuciones

Empieza por el [informe v1.2](canon/informe-programa-v1_2.md), el [estado v1.15](canon/estado-programa-v1_15.md) y el [aviso](AVISO-DE-ALCANCE.md). El catálogo público está en construcción, sin fecha. Lee los límites de muestreo y de aplicación a personas en [Uso aceptable](USO-ACEPTABLE.md). Para retar una comparación, conserva universo, sello y criterio de victoria; ver [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencia, cita y contacto

El [LICENSE](LICENSE) vigente concede MIT al código de su sección 1 y CC BY-NC-SA 4.0 al corpus y documentación de su sección 2. Para uso comercial del corpus fuera de las excepciones expresas, escribe a **jonieqsa@gmail.com**. La propuesta de mesa de cambiar términos para todo el producto necesita una modificación autorizada de LICENSE; esta página no la sustituye. Cita según [CITATION.cff](CITATION.cff); no hay DOI asignado. Ver [autoría](AUTHORSHIP.md).

Este README deriva sus cifras; si una no coincide con `status`, el README está mal, no el contador.
