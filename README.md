# Benchmark del Mexicano

[![evaluaciones prospectivas](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FJosanoforo%2FModelado-Mexicano%2Fmain%2Fdocs%2Fdata%2Fbadges%2Fevaluaciones.json)](docs/estado.md) [![instrumentos oficiales](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FJosanoforo%2FModelado-Mexicano%2Fmain%2Fdocs%2Fdata%2Fbadges%2Finstrumentos.json)](docs/estado.md) [![celdas evaluadas](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FJosanoforo%2FModelado-Mexicano%2Fmain%2Fdocs%2Fdata%2Fbadges%2Fceldas.json)](docs/estado.md) [![reports de evidencia](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FJosanoforo%2FModelado-Mexicano%2Fmain%2Fdocs%2Fdata%2Fbadges%2Freports.json)](docs/estado.md)

**Lo que la gente dijo en la última encuesta oficial, por segmento, con intervalo calibrado — y la prueba pública de que ningún modelo lo ha mejorado.**

<!-- TABLERO-DERIVADO:BEGIN -->
**287** <!-- deriva[N_corridas_selladas]: python3 tools/corrida0.py status | rg '^N_corridas_selladas=' --> corridas selladas · **20** <!-- deriva[celdas_validadas_prospectiva]: python3 tools/corrida0.py status | rg '^celdas_validadas_prospectiva=' --> predicciones selladas antes de abrir la ola contra la que se comparan · **28** <!-- deriva[reports_medibles]: python3 tools/readme_derivado.py --clave reports_medibles --> de **31** <!-- deriva[reports_total]: rg --files corpus/reports -g '*.md' | wc -l --> reports con afirmaciones medibles en el corpus · todo reproducible desde este repo.
<!-- TABLERO-DERIVADO:END -->

**[Leer el informe](docs/informe.md) · [Consultar el catálogo](docs/consultar.md) · [Verificar en cinco minutos](docs/verificar.md)**

## La prueba en una frase
En **seis** <!-- deriva[n_evaluaciones]: python3 forense/analisis/informe-v1_3/censo_evaluaciones.py --clave n_evaluaciones --> evaluaciones prospectivas, sobre **cuatro** <!-- deriva[n_instrumentos]: python3 forense/analisis/informe-v1_3/censo_evaluaciones.py --clave n_instrumentos --> instrumentos oficiales y **137** <!-- deriva[n_celdas_total]: python3 forense/analisis/informe-v1_3/censo_evaluaciones.py --clave n_celdas_total --> celdas de población, la predicción más simple —repetir lo que la gente dijo en la ola anterior— nunca fue superada, con intervalo que despejara el umbral fijado de antemano, por ninguno de los modelos construidos aquí ni por un retador externo. No es un fracaso del modelado: es el hallazgo. El comportamiento reportado del mexicano es estable entre olas en los dominios medidos, y cualquier producto que prometa detectar cambios grandes entre encuestas debería probarse contra esta línea base antes de venderse. Detalle y dictámenes: [docs/estado.md](docs/estado.md).

## Para quién
- **Banca, fintech y seguros:** el piso por segmento con su margen de error y, al lado, la medida de exclusión por oferta — no hay otra en México.
- **Gobierno y evaluación:** qué cambió de verdad entre olas y qué fue el cuestionario, por conducta y por entidad.
- **Agencias e insights:** la línea base contra la que medir cualquier gemelo digital del consumidor mexicano; hay un [reto público](docs/reto.md).
- **Academia:** sellos verificables, microdato oficial, pre-registro y validación independiente.

## Qué no hacemos
No respondemos preguntas que las encuestas oficiales no hicieron. No prometemos detectar cambios de conducta entre olas. No medimos compras observadas ni marcas. No vendemos gemelos digitales. Dónde ganan los otros y por qué, en el [informe](docs/informe.md).

## Cómo funciona, en tres líneas
Cada cifra nace con su especificación sellada antes de abrir el dato, su código fijado, sus insumos con hash y su resultado con unidad e intervalo. Cada ola nueva entra reservada y solo la abre código congelado de una prueba pre-registrada. Los sellos se atestiguan con un tercero de tiempo. Todo esto se verifica desde un clon limpio: [docs/verificar.md](docs/verificar.md).

## Cita, licencia y contacto
Uso no comercial libre con atribución; uso comercial por acuerdo. Cita: `CITATION.cff` (DOI: **pendiente** <!-- deriva[doi]: rg '^doi:' CITATION.cff -->). Límites y alcance: [AVISO-DE-ALCANCE.md](AVISO-DE-ALCANCE.md) · [USO-ACEPTABLE.md](USO-ACEPTABLE.md). Contacto: el correo de `CITATION.cff`. Cómo contribuir o retar: [CONTRIBUTING.md](CONTRIBUTING.md).

<sub>Este README deriva sus cifras por comando; si una no coincide con `python3 tools/corrida0.py status`, el README está mal, no el contador. Gobierno del programa: [gobierno/](gobierno/) · histórico: [archivo/](archivo/).</sub>
