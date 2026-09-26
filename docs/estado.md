---
title: Estado y prueba
---

# Estado del programa y la prueba

[Portada]({{ '/' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }})

Segundo nivel de la portada: la tabla técnica de evaluaciones, los contadores derivados y el estado del modelo heredado, con sus comandos. Heredado del README de FRONT-1 por el acto GEN2-FRONT-3-PORTADA-1: el contenido no cambia, solo su lugar. Las cifras de la frase de portada (evaluaciones, instrumentos, celdas) salen del censo del informe v1.3, `python3 forense/analisis/informe-v1_3/censo_evaluaciones.py`; la tabla de abajo es la lista de evaluaciones que publicó FRONT-1 y no coincide fila a fila con ese censo (ver la nota de cierre del acto).

## La prueba

Estas son **evaluaciones**, no dominios independientes ni una lista de predicciones anteriores a la publicación oficial. En el vocabulario del repositorio, «prospectiva» significa que la emisión quedó sellada antes de abrir el árbitro R de la evaluación; eso por sí solo no prueba que antecediera a la publicación de INEGI.

| Evaluación | Ola y unidad | Dictamen | Cierre |
|---|---|---|---|
| Piloto ahorro, localidad × edad; 8 celdas <!-- deriva: rg -F '8/8 celdas' forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md --> | ENIF 2024, persona | `SIN-CANDIDATO-SUPERIOR` | [Nota](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md) |
| Piloto evasión, escolaridad × dominio; 12 celdas <!-- deriva: rg -F '12/12 celdas' forense/notas/2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md --> | ENVIPE 2025, delito | `SIN-CANDIDATO-SUPERIOR` | [Nota](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md) |
| Piloto gobierno digital, edad × escolaridad; 15 celdas <!-- deriva: rg -F '3/15' forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md --> | ENCIG 2025, trámite | `FALSADOR-DEBIL` | [Nota](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md) |
| Lote de interacción; 44 celdas puntuadas <!-- deriva: rg -F '44 celdas puntuadas' canon/informe-programa-v1_2.md --> | ENIF 2024, persona | `PROPUESTA-CON-RESERVA`: mejora puntual sin despejar umbral | [Nota](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-21-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-cierre.md) |
| Duelo de ola nueva, sexo × dominio y edad × dominio; 12 por cruce <!-- deriva: rg -F '12 celdas puntuadas por par' forense/notas/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md --> | ENVIPE 2026, delito | `NADIE-VENCE` en ambos | [Nota](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md) |
| Duelo de candidatos, edad × sexo y escolaridad × sexo; ver celdas en cierre | ENCIG 2025, trámite | Agregado `FALSADOR-DEBIL` | [Nota](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-23-GEN2-DUELO-ENCIG2025-CIERRE-1-cierre.md) |

Los retadores evaluados no superaron los **criterios de superioridad fijados en esas comparaciones**. Esto no declara equivalencia ni se extiende a modelos no evaluados. El [informe](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/informe-programa-v1_3.md) documenta la subcobertura del piso en el lote y en marginales (heredado de `v1.2`, sin cambio). Los intervalos calibrados corresponden a evaluaciones concretas, no a todos los RESULT del repositorio.

## Estado derivado

Cada contador tiene su propio universo. `status` es una vista derivada del corte disponible al ejecutar el comando, no el estado vivo de otras ramas. Esta página lista la clave y el comando, sin valor impreso: un valor copiado aquí envejecería en silencio. Las dos cifras de `status` que usa la portada viven en el bloque derivado de [README.md](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/README.md), que refresca el job `guardias` de CI (`python3 tools/readme_derivado.py --escribe`).

| Objeto | Clave | Comando |
|---|---|---|
| Corridas selladas | `N_corridas_selladas` | `python3 tools/corrida0.py status \| rg '^N_corridas_selladas='` |
| RESULT GEN2 sellados | `N_resultados_gen2_sellados` | `python3 tools/corrida0.py status \| rg '^N_resultados_gen2_sellados='` |
| RESULT GEN2 adoptados activos | `N_resultados_gen2_adoptados_activos` | `python3 tools/corrida0.py status \| rg '^N_resultados_gen2_adoptados_activos='` |
| Celdas validadas (contador rector) | `celdas_validadas` | `python3 tools/corrida0.py status \| rg '^celdas_validadas='` |
| Celdas prospectivas de esa vista | `celdas_validadas_prospectiva` | `python3 tools/corrida0.py status \| rg '^celdas_validadas_prospectiva='` |
| Celdas retrospectivas de esa vista | `celdas_validadas_retrospectiva` | `python3 tools/corrida0.py status \| rg '^celdas_validadas_retrospectiva='` |
| RESULT GEN2 pendientes de adopción | `N_resultados_gen2_pendientes_adopcion` | `python3 tools/corrida0.py status \| rg '^N_resultados_gen2_pendientes_adopcion='` |

El [estado](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/estado-programa-v1_17.md) y la [actualización del contador](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/L0/ADR-260923-GEN2-CONTADORES-CONSUMO-1-988c-01.md) explican el alcance de las celdas. El total incorpora conductas agregadas de crédito y cruces ENCIG que antes no contaba; los campos prospectiva y retrospectiva de `status` no cubren todas las formas incorporadas al total. **Validada** significa emisión comparada con R, no adopción por mesa.

## Estado del modelo

Este bloque describe el **modelo heredado** y conserva la comprobación T19c
de la suite. No sustituye los contadores GEN2 de arriba.

- **26 de 27** corridas del Hito D con veredicto archivado — **14D·4B·4A·2E·2C**. <!-- deriva: python3 tests/check.py --baseline | rg 'T19c' ; fuente: forense/hitoD-preregistro-v2_0.md -->
- Condicionales medidas 12 de 15. <!-- deriva: rg -c 'clase: "MEDIDO·PARCIAL|clase: "MEDIDO·NACIONAL' milpa/procedencia.yaml ; T19c -->
- Coeficientes en escala del modelo 0 de 15. <!-- deriva: rg 'magnitud: medid' milpa/procedencia.yaml ; T19c -->

## Verifica en cinco minutos: ruta de lectura

Para inspeccionar estructura, referencias y sellos no hace falta `data/raw`. Clona el repo, lee una [nota de cierre](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md) y compara su `spec.yaml`, `resultados.json` y `sello.json` en [corrida0](https://github.com/Josanoforo/Modelado-Mexicano/tree/main/data/corrida0/). `python3 tools/corrida0.py status` reproduce la tabla. `python3 tests/check.py --baseline` verifica la línea base del repo, sin garantía de duración. La [guía](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/docs/verificar.md) explica el control de hashes sin abrir raw y separa la reproducción numérica: `python3 tools/corrida0.py verify <CALC-ID>` puede necesitar corpus, dependencias y más tiempo. La [receta de sello externo](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/docs/sello-externo.md) explica su testigo de tiempo y sus límites.

## Cobertura

El corpus contiene **31 reports temáticos**. <!-- deriva: rg --files corpus/reports -g '*.md' | wc -l --> Son documentos de evidencia, no dominios mutuamente excluyentes; [lista completa](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/docs/catalogo.md). El mapa U0 aún no está consolidado en este corte. Hay mediciones **selladas** sobre dinero (ENIF), trámites (ENCIG), seguridad (ENVIPE), tiempo (ENUT), ingreso (ENIGH), trabajo (ENOE) y tecnología (ENDUTIH, MOCIBA), trazables por [CALC y RESULT](https://github.com/Josanoforo/Modelado-Mexicano/tree/main/data/corrida0/) y [estado](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/estado-programa-v1_17.md). La [medición ENOE](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-23-ASTRA5-U1-TRABAJO-ENOE-cierre.md) ofrece pisos trimestrales y persistencia descriptiva retrospectiva; adopta NO y no acredita transición individual ni cobertura predictiva calibrada. Los [pisos de tecnología](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/analisis/dominios/tecnologia/cierre-comun.md) describen ENDUTIH 2023–2025 y MOCIBA 2015–2017 en universos distintos; son retrospectivos, sin adopción ni IC predictivo calibrado, y no acreditan cambios futuros. El [eje regional v1.0](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/eje-regional-v1_0.md) publica filas retrospectivas de ENIF, ENCIG y ENVIPE con supresión por tamaño muestral; es propuesta sin adopción y no cubre todas las conductas ni olas. Sellado, validado y adoptado son estados distintos. ENDIREH e INE/ENCUP siguen pendientes de medición consolidada; no se presentan como medición publicada. U0 fijará la cobertura temática y su propietario, pero no bloquea la publicación de los productos ya fusionados. Una duda pendiente no se clasifica `NO-MEDIBLE-POR-DISEÑO`.

## Uso, límites y contribuciones

Empieza por el [informe principal v1.4](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/informe-programa-v1_4.md) (v1.3 más el cierre del 22–26/sep; antecesores [v1.3](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/informe-programa-v1_3.md) y [v1.2](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/informe-programa-v1_2.md), no editado, E.3), su [anexo de evidencia v1.3](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/informe-programa-v1_3-ANEXO.md), el [estado v1.17](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/estado-programa-v1_17.md) y el [aviso](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/AVISO-DE-ALCANCE.md). El anexo lee RESULT sellados y no emite una nueva adjudicación ni sustituye la versión del informe principal. El catálogo público está en construcción, sin fecha. Lee los límites de muestreo y de aplicación a personas en [Uso aceptable](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/USO-ACEPTABLE.md). Para retar una comparación, conserva universo, sello y criterio de victoria; ver [CONTRIBUTING.md](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/CONTRIBUTING.md).
