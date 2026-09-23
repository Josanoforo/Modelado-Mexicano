# ASTRA4-U2 · lote L8, conversión presidencial

23/sep/2026. Tres filas afines `RES-0050/0051/0052`. La spec sellada
`forense/prereg-caja/L8-CONVERSION-PRESIDENCIAL-spec-v1_0.md` y el
`CALC-L8-CONVERSION-0001` estaban congelados y ejecutados antes de este acto.
Se coteja el resultado existente, sin cambiar fórmula ni medidor. El
`sello.json` coincide con su sidecar SHA-256
`3d16bc120b5db1419ed6847e99288fadaf381e379b839949d38b4f41e290fd45`;
`forense/replay-evidencia.tsv` registra contexto idéntico y resultado
reproducido. El insumo es el JSON versionado
`data/l8-resultados-tipo-boleta-v1_0.json`, no un microdato nuevo.

| Fila y consumidor | RESULT exacto | GEN2 | GEN1 | Diferencia |
|---|---|---:|---:|---:|
| `RES-0050`, `participa_p0_minimo` | `RESULT-L8CONV-A-P-MINIMO` | 0.345267 | 0.345267 | 0 |
| `RES-0051`, `participa_p0_maximo` | `RESULT-L8CONV-A-P-MAXIMO` | 0.750567 | 0.750567 | 0 |
| `RES-0052`, `participa_p0_media` | `RESULT-L8CONV-A-P-MEDIA` | 0.619867 | 0.619867 | 0 |

**Correspondencia:** `RESULT-L8CONV-G-P0-*` son anclas de origen, no el
valor final del consumidor. El resultado adoptable es `A-P-*`, calculado
como `clip(round(p0,4) + round(beta_pres_pp/100,6),0,1)`, con
`beta_pres_pp=4.016715486813227` y delta `0.040167`. Los tres `A-DELTA-VS-GEN1-*`
son cero y `A-REPRODUCE-GEN1=REPRODUCE`; `A-ADOPCION=LISTADO-PARA-MESA-REPRODUCE`.
Sin redondear antes el ancla, los tres valores serían 0.345263, 0.750605 y
0.619830. La identidad incluye ese grano, no se logra relajando tolerancia.

**Límite:** es una derivación determinista de la misma regla y fuente del
legado; reproduce, pero no constituye validación independiente de una
probabilidad individual. La fuente contiene 40 medias municipales y un
efecto agregado; su aplicación individual conserva la inferencia ecológica.
El IC95 sellado de `beta_pres_pp` es [0.04917010866182059,
7.887405629522231] pp, p=0.0413 y nueve conglomerados; la precisión es
frágil. `cuenta_gen2=PENDIENTE-DE-MESA`, `adopta=NO` y los tres literales
que lee el motor siguen en GEN1. Si mesa firma la adopción, el escritor
específico de `milpa/tramite.yaml` debe exigir las tres llaves, los tres
literales previos exactos, sello y resultado reproducido, escala proporción,
grano de cuatro/seis decimales y diff limitado a esas tres celdas y sus
citas; el escritor de #1080 no autoriza estas sustituciones.
