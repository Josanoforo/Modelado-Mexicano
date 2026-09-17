# Lectura CIV acotada · C2/U4 en ENVIPE 2012, 2013, 2015 y 2025

## Resultado

La comparación de puntos es semánticamente admisible: en las cuatro olas U4
es persona seleccionada con al menos un delito personal no denunciado cuya
razón válida está en 01–08; C2={01,02,06,08}, el colapso es máximo y el peso es
`FAC_ELE`. La costura de 2012 usa `BPCOD` 04–14, acreditado como correspondencia
uno-a-uno del 05–15 posterior sin residuo dentro del bloque personal. Las rutas
físicas de identidad cambian —2012 requiere hogar+`R_SEL` y confirmación en
`TSDem`; 2013 usa la persona seleccionada de `TPer_Vic`; 2015 y 2025 disponen de
`ID_PER`—, pero las nuevas olas tuvieron vínculo 100%, cero llaves ambiguas y
cero pérdidas por identidad, peso o diseño.

| victimización (ola) | p(C2,U4) | q | p(C1,U4) | n personas | p(C2,U1), delito | persona − delito |
|---|---:|---:|---:|---:|---:|---:|
| 2011 (2012) | 33.84% | 66.16% | 30.70% | 9 854 | 32.85% | +0.99 pp |
| 2012 (2013) | 37.32% | 62.68% | 32.34% | 10 905 | 34.02% | +3.30 pp |
| 2014 (2015) | 36.68% | 63.32% | 30.62% | 11 316 | 35.41% | +1.27 pp |
| 2024 (2025) | 29.43% | 70.57% | 25.62% | 13 023 | 26.72% | +2.71 pp |

Fuentes exactas y precisión están en `tabla-cronologica-u4.tsv`. Los puntos de
2012/2025 se reutilizan de corridas selladas; no se reestimaron.

## Lectura temporal permitida

Entre las olas antiguas, C2/U4 sube 3.48 pp de victimización 2011 a 2012 y
baja 0.64 pp de 2012 a 2014; no hay monotonicidad. El rango antiguo es 3.48 pp.
Al añadir 2024, el rango observado llega a 7.89 pp: máximo 37.32% en 2012 y
mínimo 29.43% en 2024. Esto describe variación entre cortes transversales y
ventanas distintas; no sigue a la misma cohorte, no identifica una tendencia
continua en el hueco 2014–2024 y no atribuye causas.

La unidad importa. En las cuatro olas el punto persona excede al punto delito,
pero por una magnitud variable (0.99–3.30 pp). No son estimandos sustituibles:
la persona cuenta una sola vez y toma el máximo entre sus eventos, mientras el
estimando delito pondera cada evento con `FAC_DEL`. Por ello la serie histórica
por delito queda aquí por debajo de C2/U4 y no puede llenar las dos olas persona.

## Precisión y límite

Para 2013 y 2015, las sensibilidades de C2 son respectivamente 35.62–38.96% y
35.19–38.23%; las de q invierten exactamente esos extremos. Conservan todas las
personas observadas antes de restringir U4 y dan cero fuera del dominio. Son
`NO-APROBADAS` para inferencia plena: falta acreditar el roster completo de UPM
seleccionadas o un servicio oficial y una política de estratos singulares
(`NC-0159`). No son límites inferiores. Los intervalos sellados de 2012/2025
usan una implementación previa y se muestran sólo como legado no armonizado;
no se comparan entre sí ni se restan extremos.

La lectura, por tanto, mejora la medición descriptiva temporal de C2/U4 y su
complemento, pero no calibra θ, no crea un piso de persistencia y no modifica ni
adopta RES-0027/0028.

## Reproducción dirigida

```bash
python3 tests/test_envipe_u4_2013_2015.py
python3 tools/corrida0.py verify CALC-ENVIPE-U4-2013-0001
python3 tools/corrida0.py verify CALC-ENVIPE-U4-2015-0001
```
