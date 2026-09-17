# ENCRIGE 2020 · alcance, intensidad y concentración por tamaño

## Respuesta

La incidencia publicada no resume una sola diferencia. Frente a Micro,
Pequeña y Mediana combinan una fracción menor de empresas afectadas con más
trámites o inspecciones con corrupción por empresa afectada; ambos componentes
casi se cancelan. Grande, en cambio, presenta mayor prevalencia y mucha mayor
intensidad condicional, y esta última domina aritméticamente su brecha de
incidencia.

| Tamaño | Empresas afectadas entre expuestas (`p`) | Trámites/inspecciones con corrupción por expuesta (`m`) | Por empresa afectada (`r`) |
|---|---:|---:|---:|
| Micro | 5.51% | 0.237 | 4.30 |
| Pequeña | 2.24% | 0.233 | 10.38 |
| Mediana | 4.41% | 0.234 | 5.31 |
| Grande | 6.69% | 1.168 | 17.46 |

`r` es un cociente de recuentos transversales: trámites o inspecciones con
experiencia de corrupción divididos entre empresas con al menos un acto. No es
reincidencia temporal, riesgo por interacción, dinero perdido ni número de
actos por persona. Que supere uno es válido.

## Qué compone la diferencia frente a Micro

Los términos siguientes están en trámites/inspecciones con corrupción por
empresa expuesta. Son contribuciones aritméticas simétricas, no efectos del
tamaño.

| Contraste | Diferencia de `p` (pp) | Término prevalencia | Término intensidad condicional | Diferencia total de `m` | Lectura |
|---|---:|---:|---:|---:|---|
| Pequeña − Micro | −3.271 | −0.240 | +0.236 | −0.004 | Casi cancelación; prevalencia domina apenas en magnitud absoluta. |
| Mediana − Micro | −1.101 | −0.053 | +0.050 | −0.003 | Casi cancelación; prevalencia domina apenas en magnitud absoluta. |
| Grande − Micro | +1.177 | +0.128 | +0.803 | +0.931 | Domina intensidad condicional; ambos términos elevan la incidencia. |

Por ello, la similitud de `m` entre Micro, Pequeña y Mediana no implica el
mismo patrón subyacente. En Pequeña, sobre todo, una prevalencia mucho menor
queda casi compensada por un `r` más de dos veces mayor. Para Grande, cerca de
0.803 de la brecha total de 0.931 corresponde al término de intensidad
condicional; el término de prevalencia aporta 0.128.

## Dónde se concentra cada volumen

| Tamaño | Participación en exposición | Participación en empresas afectadas | Participación en trámites/inspecciones con corrupción |
|---|---:|---:|---:|
| Micro | 85.74% | 92.73% | 84.62% |
| Pequeña | 12.33% | 5.43% | 11.96% |
| Mediana | 1.54% | 1.33% | 1.50% |
| Grande | 0.39% | 0.52% | 1.92% |

La prioridad descriptiva cambia con la pregunta. Si se mira la proporción
afectada, Grande tiene el punto más alto. Si se mira cuántas empresas están
afectadas, Micro concentra 92.73% por su peso en el universo. Si se mira el
volumen de trámites/inspecciones con corrupción, Micro sigue dominando con
84.62%, mientras Grande sube a 1.92% del volumen pese a representar sólo 0.39%
de la exposición. Pequeña muestra el patrón inverso en alcance —5.43% de las
afectadas— pero concentra 11.96% del volumen, casi su 12.33% de exposición.

Esto permite priorizar preguntas descriptivas, no asignaciones óptimas de
recursos: el volumen señala dónde se acumulan interacciones corruptas
estimadas; la prevalencia señala qué fracción de empresas expuestas resulta
afectada.

## Qué dato faltaría para distinguir explicaciones

La observación decisiva sería el total de **todas** las interacciones con el
gobierno por empresa y tamaño —corruptas o no—, idealmente con su distribución
entre empresas afectadas y por tipo de trámite/inspección. Ese denominador
permitiría separar si un `r` alto refleja más oportunidades de interacción por
empresa afectada, mayor riesgo de corrupción por interacción o una mezcla. Los
tabulados usados no contienen ese denominador ni permiten una probabilidad por
trámite.

## Alcance y límites

El universo son empresas privadas con instalaciones fijas en industria,
comercio y servicios cubiertos por ENCRIGE, que realizaron al menos un trámite
o fueron sujetas a una inspección entre enero y la entrevista de 2020. Los
absolutos son estimaciones expandidas, no `n` muestrales. La representación
CSV no ofrece EE, CV o IC utilizables: no se afirma significancia, causalidad,
tendencia ni generalización fuera del universo.

Los cuatro tamaños reconstruyen exactamente los nacionales de `N`, `A` y `T`
al grano publicado; el nacional no se incluyó como quinta parte. Las tablas
completas, controles y figura están en este directorio. Reproducción:

```bash
python3 tools/encrige_carga_intensidad.py
```

