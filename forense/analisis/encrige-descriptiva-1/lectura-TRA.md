# ENCRIGE 2020 · corrupción experimentada por unidades económicas

Pregunta: **¿Cómo se distribuye la corrupción experimentada en unidades económicas por tamaño en el universo ENCRIGE 2020?**

## Resultado

Entre las unidades económicas que durante 2020 —de enero a la fecha de entrevista— realizaron por lo menos un trámite o fueron sujetas a una inspección, la tasa oficial equivale a **5.10% con experiencia de al menos un acto de corrupción**. El cuadro de tamaño muestra 6.69% en empresas grandes, 5.51% en micro, 4.41% en medianas y 2.24% en pequeñas.

| Dominio | Unidades expuestas (expandido) | Unidades con ≥1 acto (expandido) | Prevalencia oficial por 10 000 | Prevalencia derivada | Incidencia oficial por 10 000 | Experiencias por unidad expuesta |
|---|---:|---:|---:|---:|---:|---:|
| Total nacional | 4 006 729.285 | 204 284.532 | 509.854 | 5.10% | 2 399.902 | 0.240 |
| Micro | 3 435 208.519 | 189 424.313 | 551.420 | 5.51% | 2 368.670 | 0.237 |
| Pequeña | 494 118.994 | 11 084.740 | 224.333 | 2.24% | 2 327.625 | 0.233 |
| Mediana | 61 618.868 | 2 719.369 | 441.321 | 4.41% | 2 342.969 | 0.234 |
| Grande | 15 782.904 | 1 056.109 | 669.148 | 6.69% | 11 682.740 | 1.168 |

Los absolutos son estimaciones expandidas, no `n` muestrales. La prevalencia se transformó como `tasa / 10 000` y después a porcentaje. La incidencia se transformó como `tasa / 10 000`; su numerador es el total de trámites o inspecciones con experiencia de corrupción, por lo que su unidad es experiencias por unidad económica expuesta, no una proporción.

## Lectura descriptiva

La brecha puntual más amplia de prevalencia aparece entre grandes y pequeñas: 4.45 puntos porcentuales. Las micro están 0.42 puntos por encima del total nacional. Aun así, el volumen expandido se concentra en micro: representan 85.7% del denominador expuesto y 92.7% de las unidades que experimentaron al menos un acto. Esto concilia dos hechos distintos: la prevalencia puntual más alta está en grandes, pero la gran mayoría del número expandido de unidades afectadas está en micro.

La incidencia es cercana a 0.23-0.24 experiencias por unidad expuesta en micro, pequeñas y medianas. En grandes llega a 1.168. Esto no significa que 116.8% de las empresas grandes sean víctimas: una empresa puede reportar experiencias en más de un trámite o inspección. El contraste también puede reflejar diferencias en el número y tipo de interacciones con el gobierno; los tabulados no permiten atribuirlo a tamaño por sí solo.

## Población cubierta

La unidad es la empresa, que puede reunir uno o más establecimientos. El universo son empresas privadas del país con instalaciones fijas en industria, comercio y servicios cubiertos por ENCRIGE. Se excluyen agricultura, cría y explotación de animales, aprovechamiento forestal, pesca, caza y gobierno. El denominador analítico excluye empresas sin al menos un trámite o inspección durante el periodo de referencia.

Los tamaños conservan los cortes oficiales de personal ocupado: micro, 0-10 en los tres grandes sectores; pequeña, 11-50 en industria y servicios y 11-30 en comercio; mediana, 51-250 en industria, 51-100 en servicios y 31-100 en comercio; grande, 251 o más en industria y 101 o más en comercio y servicios.

## Alcance y reservas

La tabla permite describir puntos y diferencias entre dominios dentro del universo ENCRIGE 2020. No permite concluir que una diferencia sea estadísticamente distinta de cero: la representación CSV no publica EE, CV, IC ni `n` muestral. Las notas ODT describen umbrales de semaforización por CV, pero no preservan la asignación de color a cada celda; la incertidumbre queda honestamente como `NO-DISPONIBLE-EN-REPRESENTACION-CSV`.

Tampoco permite inferir causalidad, generalizar a sectores excluidos, confundir empresas con personas, comparar numéricamente estas tasas con ENCIG, ni validar o calibrar el motor. Es un resultado oficial reproducido mediante extracción determinista; no una reestimación del diseño de INEGI.

## Procedencia y reproducción

Fuente: INEGI, tabulados oficiales ENCRIGE 2020, cuadros `t6_33`, `t6_36` y `t6_41`; cuestionario general, secciones VIII-IX; diseño muestral, secciones 2-7. El archivo completo con valores originales, transformaciones, localizadores y estados de incertidumbre es `encrige-corrupcion-por-tamano.csv`.

Reproducción dirigida desde la raíz del repositorio:

```bash
python3 tools/corrida0.py preflight CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001
python3 tools/corrida0.py run CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001
python3 tools/corrida0.py verify CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001
```

La localización de los cuadros exigió ver sus valores antes de congelar la spec. Esta exposición es compatible con una descripción de tabulados públicos; no constituye evaluación ciega ni habilita F6.
