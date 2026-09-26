---
title: One-pager
---

# Benchmark del Mexicano — one-pager

[Portada]({{ '/' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }}) · [Reto público]({{ '/reto.html' | relative_url }}) · [PDF de esta página](one-pager.pdf)

## Qué es

Un benchmark auditable de cómo se comporta el mexicano, medido con microdato oficial (INEGI, Banxico y afines) y segmentado por sexo, edad, escolaridad, localidad y formalidad. Cada cifra publicada trae su código, sus insumos y su sello; cualquiera puede reproducirla o intentar vencerla.

## La prueba

**6 evaluaciones** <!-- deriva: rg -c '^\| Pilot|^\| Duelo|^\| Lote' docs/estado.md --> selladas antes de comparar contra el árbitro de la ola, sobre dinero, trámites, seguridad y gobierno digital. Los retadores evaluados no superaron los criterios de superioridad fijados en esas comparaciones; esto no declara equivalencia ni se extiende a modelos nunca evaluados.

| Evaluación | Ola | Dictamen |
|---|---|---|
| Piloto ahorro, localidad × edad | ENIF 2024 | `SIN-CANDIDATO-SUPERIOR` |
| Piloto evasión, escolaridad × dominio | ENVIPE 2025 | `SIN-CANDIDATO-SUPERIOR` |
| Piloto gobierno digital, edad × escolaridad | ENCIG 2025 | `FALSADOR-DÉBIL` |
| Lote de interacción, 44 celdas | ENIF 2024 | `PROPUESTA-CON-RESERVA` |
| Duelo de ola nueva | ENVIPE 2026 | `NADIE-VENCE` |
| Duelo de candidatos | ENCIG 2025 | `FALSADOR-DÉBIL` agregado |

Detalle y cierre de cada una en el [estado y prueba]({{ '/estado.html#la-prueba' | relative_url }}).

## Estado del corte

| Objeto | Valor |
|---|---:|
| Corridas selladas | 246 <!-- deriva: python3 tools/corrida0.py status | rg '^N_corridas_selladas=' --> |
| RESULT GEN2 sellados | 66 582 <!-- deriva: python3 tools/corrida0.py status | rg '^N_resultados_gen2_sellados=' --> |
| RESULT GEN2 adoptados (piso publicado) | 72 <!-- deriva: python3 tools/corrida0.py status | rg '^N_resultados_gen2_adoptados_activos=' --> |
| Celdas validadas (contador rector) | 219 <!-- deriva: python3 tools/corrida0.py status | rg '^celdas_validadas=' --> |
| Reports de evidencia en el corpus | 31 <!-- deriva: rg --files corpus/reports -g '*.md' | wc -l --> |
| Áreas de consulta con estimador adoptado (de 5 en el catálogo) | 4 <!-- deriva: python3 -c "import csv;print(len({r['area_consulta'] for r in csv.DictReader(open('canon/tabla-de-piso-v1_0.tsv'),delimiter='\t')}))" --> |

El catálogo completo tiene 1 537 filas de estimando/segmento/ola; la mayoría es piso histórico de contexto o propuesta sin adopción, no estimador vigente. La [tabla de piso](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/tabla-de-piso-v1_0.tsv) filtra las 72 adoptadas — ésa es la línea que el [reto público]({{ '/reto.html' | relative_url }}) invita a vencer.

## Qué obtiene cada audiencia

- **Bancos y fintech.** El piso de dinero y crédito (27 filas adoptadas) junto con su medida de exclusión por oferta al lado — nunca un marginal de conducta sin su oferta comparable.
- **Gobierno.** Estabilidad frente a salto: dónde un indicador persiste ola a ola y dónde hay un `SALTO-SIN-EXPLICAR` que ningún candidato explica (ENCIG, pago de trámites por canal digital).
- **Agencias y encuestadoras.** La línea base contra la que un gemelo digital o un modelo sintético debería medirse antes de venderse como sustituto de encuesta — no vendemos gemelos, publicamos el comparador.
- **Academia.** Sellos verificables sin confiar en el repositorio ni en GitHub: 344 sellos con manifiesto y testigo de tiempo (OTS/TSA o firma GPG del merge cuando no hubo egress), más validación independiente que recalcula desde la spec humana sin leer el código que produjo la cifra.

## Qué no hacemos

No respondemos preguntas que las encuestas oficiales no hicieron. No prometemos detectar cambios de conducta entre olas. No medimos compras observadas ni marcas. No vendemos gemelos digitales. No tratamos a los mexicanos como bloque homogéneo: toda cifra viene segmentada, y el sesgo de sobre-muestreo del clasemediero urbano formal se declara, no se esconde.

## Cómo verificar

Clona el repo y corre `python3 tests/check.py --baseline`; elige un `CALC-ID` de [`data/corrida0/`](https://github.com/Josanoforo/Modelado-Mexicano/tree/main/data/corrida0) y compara su `spec.yaml`, `resultados.json` y `sello.json` con `sha256sum`. La guía completa, con la ruta sin microdato y la ruta de reproducción numérica, está en [«Verifica en 5 minutos»]({{ '/verificar.html' | relative_url }}).

## Cómo citar

Usa [`CITATION.cff`](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/CITATION.cff). DOI: **pendiente** (Zenodo, activación de mesa).

## Contacto y términos

El [LICENSE](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/LICENSE) vigente aplica MIT al código y CC BY-NC-SA 4.0 al corpus y documentación, con excepciones expresas para ciertos usos comerciales del corpus — uso no comercial libre con atribución; para uso comercial fuera de esas excepciones, escribe a **jonieqsa@gmail.com**. Lee [Uso aceptable](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/USO-ACEPTABLE.md) y el [aviso de alcance](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/AVISO-DE-ALCANCE.md) antes de aplicar una cifra.
