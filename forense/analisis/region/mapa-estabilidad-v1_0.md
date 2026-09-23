# Mapa descriptivo regional · RETROSPECTIVA

Generado por `python3 tools/astra/region/mapa.py` desde los `resultados.json` sellados identificados en cada fila del TSV. Evento: punto de la ola observada dentro del IC95 de diseño de la ola anterior. El intervalo anterior no es predictivo calibrado; esta comparación no demuestra estabilidad ni cambio sostenido.

| Serie | Transición | Dentro / comparables | Wilson 95 % descriptivo |
|---|---:|---:|---:|
| ENCIG canal_digital_luz | 2017→2019 | 10/32 | [0.180, 0.486] |
| ENCIG canal_digital_luz | 2019→2021 | 13/32 | [0.255, 0.577] |
| ENCIG canal_digital_luz | 2021→2023 | 14/32 | [0.282, 0.607] |
| ENIF informal_cualquiera_18a70 | 2018→2021 | 0/6 | [0.000, 0.390] |
| ENIF informal_cualquiera_18a70 | 2021→2024 | 4/6 | [0.300, 0.903] |
| ENVIPE evade_norma_envipe2025 | 2023→2024 | 18/32 | [0.393, 0.718] |
| ENVIPE evade_norma_envipe2025 | 2024→2025 | 20/32 | [0.453, 0.771] |

Wilson supone eventos Bernoulli independientes entre geografías. El diseño compartido, las regiones ENIF y la repetición de entidades entre transiciones pueden violar ese supuesto; por ello el intervalo es solo una descripción binomial condicional, no un IC de diseño ni una cobertura por conglomerado válida. No se dispone aquí de evaluación temporal calibrada libre de fuga ni de un número de transiciones independientes suficiente para inferir persistencia regional. Los 32 estados no se reinterpretan como UPM; las seis regiones ENIF tampoco.

No se aplica corrección de multiplicidad: ninguna categoría individual se presenta como hallazgo simultáneo. El mapa completo incluye SIN-COMPARABILIDAD si una de las dos olas tiene publicación suprimida.
