# Spec fijada · ENCRIGE 2020, corrupción experimentada por tamaño

Estado: `FIJADA-ANTES-DE-CORRER`. Producto descriptivo para el anexo TRA previsto en F-19. No es una medición sobre microdatos, una transferencia de M, una calibración ni una evaluación F6.

## Pregunta consumidora

> ¿Cómo se distribuye la corrupción experimentada en unidades económicas por tamaño en el universo ENCRIGE 2020?

Consumidor documental: anexo descriptivo TRA previsto para el informe. Este acto no modifica el informe canónico.

## Unidad, universo y periodo

La unidad de observación y de muestreo es **la empresa**: la unidad económica bajo una sola entidad propietaria o controladora que combina recursos para producir bienes, comerciar o prestar servicios, y que puede comprender uno o más establecimientos.

Población objetivo: empresas del país con instalaciones fijas, del sector privado, que realizan actividades de industria, comercio o servicios. La cobertura sectorial publicada comprende SCIAN 2018: 21, 22, 23, 31-33, 43, 46, 48-49, 51-56, 61, 62, 71, 72 y 81. Se excluyen agricultura, cría y explotación de animales, aprovechamiento forestal, pesca, caza y gobierno. La encuesta tiene cobertura geográfica nacional; aquí sólo se usan los dominios planeados nacional y nacional-tamaño.

Periodo del desenlace: **durante 2020, es decir, de enero a la fecha de la entrevista**, como establecen las preguntas 8.2/8.11 del instrumento para trámites e inspecciones, y la pregunta 9.3 para las experiencias de corrupción. La edición 2021 de los documentos no cambia ese periodo.

## Indicadores y denominador

1. Primario, `PREVALENCIA-EXPERIENCIA-CORRUPCION`: tasa oficial de prevalencia de participación en al menos un acto de corrupción. Numerador publicado: unidades económicas que experimentaron algún acto de corrupción en al menos uno de sus trámites, pagos, solicitudes de servicios, contactos con autoridades o inspecciones. Denominador publicado: unidades económicas que realizaron por lo menos un trámite o fueron sujetas a una inspección. Unidad original: casos por 10 000 unidades expuestas. Transformación: `tasa / 10 000` para obtener proporción y `tasa / 100` para porcentaje.
2. Secundario, `INCIDENCIA-EXPERIENCIAS-CORRUPCION`: total publicado de trámites o inspecciones con experiencia de corrupción dividido entre el mismo total de unidades económicas expuestas. Unidad original: experiencias por 10 000 unidades expuestas. Transformación: `tasa / 10 000` para obtener experiencias por unidad. No se interpreta como prevalencia.

El total y los tamaños son dominios de una misma encuesta, no muestras independientes. Los absolutos publicados son estimaciones expandidas, no tamaños muestrales.

## Dominios de tamaño oficiales

Se preservan sin mapearlos a cortes del modelo:

| Tamaño | Industria | Comercio | Servicios |
|---|---:|---:|---:|
| Micro | 0 a 10 | 0 a 10 | 0 a 10 |
| Pequeña | 11 a 50 | 11 a 30 | 11 a 50 |
| Mediana | 51 a 250 | 31 a 100 | 51 a 100 |
| Grande | 251 y más | 101 y más | 101 y más |

## Cuadros y campos fijados

Fuente tabular: miembro `conjunto_de_datos_VI_Entorno_del_establecimiento_2020` del ZIP oficial registrado como `conjunto_de_datos_encrige_2020_csv`.

- `t6_33.csv`: filas `Estados Unidos Mexicanos`, `Micro`, `Pequeña`, `Mediana`, `Grande`; denominador total, absoluto de participación en al menos un acto y su tasa de prevalencia. Es la fuente primaria.
- `t6_36.csv`: las mismas cinco filas y la columna de tasa a nivel nacional. Se usa sólo como segunda lectura local de la tasa primaria.
- `t6_41.csv`: las mismas cinco filas; denominador total, total de trámites o inspecciones con experiencia de corrupción y tasa de incidencia. Es la fuente secundaria.
- `t6_33.odt`, `t6_36.odt` y `t6_41.odt`: notas oficiales de definición y semaforización.

Localizador del instrumento: cuestionario general, sección VIII (8.2/8.11) y sección IX (9.3-9.5). Localizador del universo: diseño muestral, secciones 2 a 7 y cuadro 3.

## Faltantes, supresión, redondeo e incertidumbre

- Una celda vacía se emite vacía con estado `NO-DISPONIBLE`; nunca se convierte en cero. Los símbolos de supresión, si aparecieran, se preservan y detienen la conversión numérica de esa celda.
- Los cinco dominios fijados deben existir una vez en cada cuadro. No se reconstruye el total promediando tamaños.
- Se conserva el texto decimal original. Los normalizados se calculan con aritmética decimal y se emiten a 12 decimales. La identidad `numerador / denominador * 10 000` se comprueba con tolerancia absoluta de `1e-9` en unidades de la tasa.
- Los CSV no publican `n` muestral, EE, CV ni IC. Las notas ODT dicen que las estimaciones originales fueron coloreadas por intervalos de CV, pero estos archivos no contienen una asociación recuperable entre color y celda. Por ello: `n_muestral=NO-PUBLICADO` e `incertidumbre=NO-DISPONIBLE-EN-REPRESENTACION-CSV`. No se construye un IC binomial con absolutos expandidos.

## Salida y límites

El CSV final tendrá una fila por indicador y dominio, con valor/unidad originales; fórmula y valor normalizado; numerador y denominador publicados; ausencia de n e incertidumbre; periodo; cuadro/localizador; supresión y procedencia. El extractor no abre microdatos ni reestima el diseño de INEGI.

Conclusión permitida: diferencias descriptivas entre dominios dentro del universo y periodo publicados. No permite causalidad, comparación directa con tasas de personas de ENCIG, ranking de M/L, validación del motor ni generalización a sectores excluidos o empresas sin exposición al denominador.

## Exposición previa

Para localizar los campos y comprobar que el indicador exacto existía se vieron los valores de `t6_33`, `t6_36` y `t6_41` antes de congelar esta spec. Es una extracción descriptiva de tabulados públicos, no una evaluación ciega ni un holdout.
